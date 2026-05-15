# Turbine `awaitItem()` Timeout on `StateFlow<LoginUiState>` — Diagnosis and Fix

## The Short Answer

`awaitItem()` timing out even though state is changing in logs means one (or more) of three things:

1. `Dispatchers.Main` was never replaced — `viewModelScope.launch {}` never ran in the test
2. `stateIn` was never activated — no subscriber existed before you acted on the ViewModel
3. StateFlow conflation swallowed intermediate states — producer ran to completion before the collector was scheduled

---

## Root Cause 1: `Dispatchers.Main` Not Replaced

`viewModelScope` is tied to `Dispatchers.Main`. In JVM unit tests, `Main` doesn't exist. Any `viewModelScope.launch {}` block silently fails (or throws an exception Turbine surfaces as a timeout rather than a crash). This is the most common cause.

**Fix for Kotest — `beforeTest` / `afterTest` lifecycle:**

```kotlin
class LoginViewModelTest : FunSpec({
    val testDispatcher = StandardTestDispatcher()
    lateinit var viewModel: LoginViewModel

    beforeTest {
        Dispatchers.setMain(testDispatcher)      // mandatory
        viewModel = LoginViewModel(fakeRepository)
    }

    afterTest {
        Dispatchers.resetMain()                  // mandatory cleanup
    }
})
```

Use `StandardTestDispatcher` (not `UnconfinedTestDispatcher`) for `setMain` so you retain control over when coroutines advance via `advanceUntilIdle()`.

---

## Root Cause 2: `stateIn` Not Activated (the #1 gotcha)

If `LoginViewModel` exposes `uiState` via:

```kotlin
val uiState: StateFlow<LoginUiState> = _state
    .stateIn(viewModelScope, WhileSubscribed(5000), LoginUiState())
```

...then the upstream flow **does not start** until at least one collector subscribes. Asserting `.value` immediately after constructing the ViewModel only returns `initialValue`. The ViewModel's state logic never ran, which is why state changes appear in logs from other contexts but not in your test.

**Fix — Turbine's `test {}` auto-activates `stateIn`:**

The `test {}` block itself is a subscriber, so opening it immediately activates `stateIn`:

```kotlin
test("login success transitions Loading then LoggedIn") = runTest {
    viewModel.uiState.test {
        awaitItem() shouldBe LoginUiState()          // initial replayed — stateIn NOW active
        viewModel.processIntent(LoginIntent.Submit("user@example.com", "password"))
        awaitItem() shouldBe LoginUiState(isLoading = true)
        fakeRepository.completeLogin(User("user@example.com"))
        awaitItem() shouldBe LoginUiState(isLoading = false, user = User("user@example.com"))
        cancelAndIgnoreRemainingEvents()
    }
}
```

If you need `.value` assertions instead, activate `stateIn` explicitly first:

```kotlin
backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) {
    viewModel.uiState.collect {}   // empty collector — activates stateIn
}
```

---

## Root Cause 3: Conflation Swallowing Intermediate States

`StateFlow` conflates: if the ViewModel sets multiple values before the collector runs, only the most recent is seen. With `StandardTestDispatcher`, the ViewModel's coroutines may run to completion (setting both `isLoading = true` and then `isLoading = false`) before Turbine's collector gets scheduled — causing `awaitItem()` to see only the final state, not the intermediate one.

**Turbine's built-in fix:** Turbine uses `UnconfinedTestDispatcher` internally for its own collection coroutine. Each emission immediately resumes the Turbine collector before the producer can emit again. This is what makes sequential `awaitItem()` chains reliable for state transitions.

If conflation is still occurring, use a fake repository that emits on demand (explicit `emit()` call) rather than emitting synchronously:

```kotlin
class FakeAuthRepository : AuthRepository {
    private val _loginResult = MutableSharedFlow<User>()

    suspend fun completeLogin(user: User) = _loginResult.emit(user)
    fun failNextLogin(error: Throwable) { /* ... */ }

    override fun login(email: String, password: String): Flow<User> = _loginResult
}
```

---

## The Canonical Kotest + Turbine Pattern for `LoginViewModelTest`

```kotlin
class LoginViewModelTest : FunSpec({
    val testDispatcher = StandardTestDispatcher()
    lateinit var fakeRepository: FakeAuthRepository
    lateinit var viewModel: LoginViewModel

    beforeTest {
        Dispatchers.setMain(testDispatcher)
        fakeRepository = FakeAuthRepository()
        viewModel = LoginViewModel(fakeRepository)
    }

    afterTest {
        Dispatchers.resetMain()
    }

    test("login success transitions Loading then LoggedIn") = runTest {
        viewModel.uiState.test {
            awaitItem() shouldBe LoginUiState()                    // initial (stateIn activated)
            viewModel.processIntent(LoginIntent.Submit("user@example.com", "password"))
            awaitItem() shouldBe LoginUiState(isLoading = true)    // first transition
            fakeRepository.completeLogin(User("user@example.com"))
            awaitItem() shouldBe LoginUiState(isLoading = false, user = User("user@example.com"))
            cancelAndIgnoreRemainingEvents()
        }
    }

    test("login failure shows error") = runTest {
        fakeRepository.failNextLogin(RuntimeException("Network error"))
        viewModel.uiState.test {
            skipItems(1)   // skip initial
            viewModel.processIntent(LoginIntent.Submit("user@example.com", "wrong"))
            skipItems(1)   // skip loading
            awaitItem() shouldBe LoginUiState(error = "Network error")
            cancelAndIgnoreRemainingEvents()
        }
    }
})
```

---

## Additional Gotchas

### BehaviorSpec + `given {}` blocks

There is a known Kotest bug (#3577): `advanceUntilIdle()` and `Dispatchers.setMain()` do not take effect inside `given {}` blocks. If you're using `BehaviorSpec`, place all coroutine assertions inside `then {}` blocks, or switch to `FunSpec` for ViewModel tests. `FunSpec` is the recommended spec style for ViewModel tests per project standing rules.

### `coroutineTestScope = true` + `Dispatchers.setMain`

Kotest's `coroutineTestScope = true` installs a `TestDispatcher` for the test itself but does **not** replace the global `Main` dispatcher that `viewModelScope` uses. Always call `Dispatchers.setMain(testCoroutineScheduler.asTestDispatcher())` explicitly even when `coroutineTestScope = true` is set:

```kotlin
class LoginViewModelTest : FunSpec({
    coroutineTestScope = true

    beforeTest {
        Dispatchers.setMain(testCoroutineScheduler.asTestDispatcher())
        viewModel = LoginViewModel(fakeRepository)
    }

    afterTest { Dispatchers.resetMain() }
})
```

### Testing State + Effects Together

Use `turbineScope` with `testIn` on both flows — both must be subscribed **before** the ViewModel action fires:

```kotlin
test("successful login navigates to home") = runTest {
    turbineScope {
        val stateTurbine = viewModel.uiState.testIn(backgroundScope, name = "state")
        val effectTurbine = viewModel.effects.testIn(backgroundScope, name = "effects")

        stateTurbine.awaitItem()   // consume initial — both flows now active

        viewModel.processIntent(LoginIntent.Submit("user", "pass"))
        fakeRepository.completeLogin(user)

        stateTurbine.skipItems(1)  // skip loading
        stateTurbine.awaitItem() shouldBe LoginUiState(isLoggedIn = true)
        effectTurbine.awaitItem() shouldBe LoginEffect.NavigateToHome

        stateTurbine.cancelAndIgnoreRemainingEvents()
        effectTurbine.cancelAndIgnoreRemainingEvents()
    }
}
```

Named turbines (`name = "state"` / `name = "effects"`) produce clearer error messages when an assertion fails.

---

## Decision Tree

```
awaitItem() times out or hangs
  │
  ├─ Did you call Dispatchers.setMain() in beforeTest?
  │    NO → Add it. viewModelScope cannot run without Main.
  │
  ├─ Does the ViewModel use stateIn(WhileSubscribed)?
  │    YES → The stateIn is not activated. Open Turbine's test {} block
  │           before acting on the ViewModel — it auto-activates stateIn.
  │
  └─ Is the ViewModel emitting multiple values synchronously?
       YES → Conflation. Use a fake repository that emits on demand.
             Turbine's UnconfinedTestDispatcher collector prevents most
             conflation, but an eagerly-emitting fake can still race ahead.
```

---

## Sources

- `[[Research: Turbine × Kotest × MVI ViewModel Testing]]` — synthesis page from 2026-05-09 research; four-layer mental model, canonical patterns, decision tree
- `[[MVI ViewModel Testing with Turbine and Kotest]]` — concrete Kotest spec patterns for LoginViewModel-style tests
- `[[Turbine]]` — Turbine API reference; `stateIn` activation behavior, `UnconfinedTestDispatcher` internals
- `[[ViewModel StateFlow Testing Patterns]]` — dispatcher setup, conflation solutions, `backgroundScope` collector trick
