# LaunchedEffect firing on every keystroke — what's wrong and how to fix it

## The root cause

`LaunchedEffect`'s behavior is driven entirely by its **keys**. The rule is:

- When any key changes (by `equals`), Compose cancels the running coroutine and launches a new one.
- When keys are stable across recompositions, the coroutine runs exactly once.

If `viewModel.loadProfile()` is firing on every keystroke into the password field, then one of your keys is changing on every recomposition. The almost-certain culprits are:

1. **You used a state value as a key that changes whenever the user types**, e.g.
   ```kotlin
   LaunchedEffect(uiState) { viewModel.loadProfile() }   // uiState changes on every keystroke
   LaunchedEffect(password) { viewModel.loadProfile() }  // obvious
   ```
2. **You used `Unit` or a literal but wrapped the effect in a lambda that re-creates a key object**, e.g.
   ```kotlin
   LaunchedEffect(viewModel) { ... }   // fine *if* viewModel is stable; broken if it's recreated on recomposition
   LaunchedEffect(SomeWrapper()) { ... } // new instance every recomposition → fires every time
   ```
3. **You passed no keys at all and got compile-time defaults wrong** — `LaunchedEffect` requires at least one key. People sometimes pass `key = uiState.someField` thinking it's stable when it isn't.

The password field is a red herring — it's just the thing causing recompositions. The bug is that your effect's key changes with those recompositions.

## The fix — one-shot effect on screen entry

For a "load profile when this screen enters composition" effect in our MVI architecture, use `Unit` (or any constant) as the key:

```kotlin
@Composable
fun LoginScreen(viewModel: LoginViewModel) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    LaunchedEffect(Unit) {
        viewModel.onIntent(LoginIntent.LoadProfile)
    }

    // ...rest of the screen
}
```

This runs the block exactly once when the composable enters the composition, and cancels it if the composable leaves. Recompositions caused by typing into the password field will not re-fire it because `Unit` never changes.

## But — the MVI-correct fix is different

A `LaunchedEffect` calling `viewModel.loadProfile()` from the composable is an architecture smell. Our standing rule says: **state flows down, intents flow up — composables emit `Intent`, they don't invoke ViewModel methods directly.** Two cleaner options:

### Option A — Load in the ViewModel's `init` block

If `loadProfile()` should fire exactly once per ViewModel lifecycle (the usual case), do it in the ViewModel itself:

```kotlin
class LoginViewModel(...) : ViewModel() {
    private val _state = MutableStateFlow(LoginState())
    val state: StateFlow<LoginState> = _state.asStateFlow()

    init {
        loadProfile()
    }

    private fun loadProfile() {
        viewModelScope.launch { /* ... */ }
    }
}
```

Now the composable has no side-effect plumbing at all. The ViewModel survives configuration changes / process recreation correctly, and you can't accidentally re-fire it from the UI.

### Option B — Emit a `ScreenEntered` intent once

If you genuinely want the trigger to come from the UI (e.g. because the same ViewModel backs multiple entry paths and only one of them should load), keep `LaunchedEffect(Unit)` but route through an intent:

```kotlin
LaunchedEffect(Unit) {
    viewModel.onIntent(LoginIntent.ScreenEntered)
}
```

…and handle `ScreenEntered` in the ViewModel's intent reducer. This preserves "intents flow up" while still triggering the load from composition.

## Summary checklist

- Find your `LaunchedEffect(...)` and look at the keys.
- If a key is `uiState`, `password`, or any value that changes on user input → that's the bug. Replace with `Unit` (or a stable id like `userId` if you actually want a reload when it changes).
- Prefer moving one-shot loads into the ViewModel's `init` block.
- If the load must originate from the UI, emit an intent — don't call ViewModel methods directly from the composable.

## Related gotchas worth knowing

- `rememberCoroutineScope().launch { ... }` inside a button `onClick` is fine — that's user-driven, not recomposition-driven. Don't confuse the two.
- If you later need an effect that re-runs when, say, the logged-in user changes: `LaunchedEffect(userId) { viewModel.loadProfile(userId) }` — pick a key that represents the thing the work depends on.
- For cleanup on disposal (cancelling subscriptions, closing resources), use `DisposableEffect`, not `LaunchedEffect`.
