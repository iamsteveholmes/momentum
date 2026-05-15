# Turbine `awaitItem()` Timing Out on `StateFlow<LoginUiState>`

## Diagnosis

`awaitItem()` timing out on a `StateFlow` while logs show state changing is almost always one of these four root causes — in order of likelihood for a `LoginViewModel`:

### 1. `Dispatchers.Main` is not replaced (most likely)

`viewModelScope` uses `Dispatchers.Main`. In a unit test, `Main` doesn't exist, so the coroutine that mutates `_uiState` never actually runs — your logs may be from a different code path, or from the eager `init` block evaluated on the test thread. Turbine subscribes fine, but no new value ever arrives.

Fix in Kotest (no `TestWatcher`):

```kotlin
class LoginViewModelSpec : FunSpec({
    val testDispatcher = UnconfinedTestDispatcher()

    beforeTest { Dispatchers.setMain(testDispatcher) }
    afterTest  { Dispatchers.resetMain() }

    test("login emits loading then success") {
        runTest {
            val vm = LoginViewModel(fakeRepo)
            vm.uiState.test {
                awaitItem() shouldBe LoginUiState()                          // initial (replayed)
                vm.login("user", "pw")
                awaitItem() shouldBe LoginUiState(isLoading = true)
                awaitItem() shouldBe LoginUiState(isLoading = false, isLoggedIn = true)
                cancelAndIgnoreRemainingEvents()
            }
        }
    }
})
```

Or set `coroutineTestScope = true` at the spec level so Kotest installs a `TestScope` for you.

### 2. StateFlow conflation under `StandardTestDispatcher`

With `StandardTestDispatcher`, the test coroutine queues work. The VM may set `Loading` then `Success` before the Turbine collector resumes — Turbine then only sees the latest value, and the missing transition shows up as a timeout on `awaitItem()` for the intermediate state.

Fix: use `UnconfinedTestDispatcher` for the `Main` replacement (as above). `UnconfinedTestDispatcher` resumes collectors eagerly on each emission, so each state transition is observed.

If you must use `StandardTestDispatcher`, drop the assertion on the intermediate `Loading` state and assert only on the terminal state via `expectMostRecentItem()` after `advanceUntilIdle()`.

### 3. The dispatcher used inside the VM isn't the test dispatcher

If `LoginViewModel` does `withContext(Dispatchers.IO) { authRepo.login(...) }`, that work runs on a real IO thread regardless of your `Main` swap. Your logs print from there, but the state mutation that follows races your test, which times out first.

Fix: inject the dispatcher.

```kotlin
class LoginViewModel(
    private val repo: AuthRepository,
    private val io: CoroutineDispatcher = Dispatchers.IO,
) : ViewModel() { /* ... */ }

// in test
val vm = LoginViewModel(fakeRepo, io = UnconfinedTestDispatcher(testScheduler))
```

### 4. You reassigned `_uiState` instead of mutating `.value`

Subtle one: if the VM ever does `_uiState = MutableStateFlow(...)` instead of `_uiState.value = ...` (or `.update { }`), Turbine is subscribed to the old instance and will never see the new one. Verify `_uiState` is a `val` and you only ever set `.value` or use `.update { }`.

## Likely the answer for you

Given your symptom — "logs show state changing" but `awaitItem()` times out — the smoking gun is almost always **#1 combined with #2**: `Main` isn't swapped, or it's swapped to `StandardTestDispatcher` and Turbine misses the conflated intermediate emission. Use `UnconfinedTestDispatcher` for the `Main` swap and the test will go green.

## Also worth checking

- You're using `awaitItem()` not `.value` — but for a transition test, `.value` would only ever read the latest, so that's not it.
- The first `awaitItem()` always returns the initial state (StateFlow replays). If you expect the first item to be `Loading` post-action, you need `skipItems(1)` first.
- If you also test effects, use `turbineScope` with `testIn(backgroundScope)` rather than nested `.test {}` blocks:

```kotlin
turbineScope {
    val stateTurbine  = vm.uiState.testIn(backgroundScope)
    val effectTurbine = vm.effects.testIn(backgroundScope)

    stateTurbine.awaitItem() shouldBe LoginUiState()           // initial
    vm.login("user@example.com", "pw")
    stateTurbine.awaitItem() shouldBe LoginUiState(isLoading = true)
    stateTurbine.awaitItem() shouldBe LoginUiState(isLoading = false, isLoggedIn = true)
    effectTurbine.awaitItem() shouldBe LoginEffect.NavigateToHome
}
```

## BehaviorSpec gotcha

If you're using `BehaviorSpec`, `Dispatchers.setMain()` in `beforeTest` may not take effect inside `given {}` blocks (Kotest issue #3577). Put assertions in `when {}` / `then {}` blocks, or set `coroutineTestScope = true` at the spec level. For ViewModel tests, `FunSpec` is the recommended style.

## Pages consulted (nornspun-agentic-kb)

- `concepts/ViewModel StateFlow Testing Patterns.md`
- `concepts/MVI ViewModel Testing with Turbine and Kotest.md`
