# LaunchedEffect Firing on Every Password Keystroke — Root Cause and Fix

## Root Cause

The bug is a `LaunchedEffect` key mistake. `LaunchedEffect` cancels and relaunches its coroutine every time its **key(s) change**. If a mutable value that changes on every password keystroke is passed as the key — or if the composable is being fully recreated on each keystroke — `viewModel.loadProfile()` fires repeatedly.

The two most common versions of this mistake on a login screen:

**Variant A — Wrong key (most likely):**  
The `LaunchedEffect` key is bound to something that changes when the user types — a `uiState` object, a `loginFormState` data class, or `passwordValue` directly:

```kotlin
// BAD: uiState changes on every keystroke → effect relaunches on every keystroke
LaunchedEffect(uiState) {
    viewModel.loadProfile()
}

// BAD: passwordValue changes with every keystroke → same problem
LaunchedEffect(passwordValue) {
    viewModel.loadProfile()
}
```

**Variant B — No stable key:**  
The composable is being fully removed and re-added to composition (e.g., due to a navigation or conditional structure issue), causing even `LaunchedEffect(Unit)` to re-run.

## The Fix

If `loadProfile()` should run **once when the screen first appears** and never again during the user's typing session, use `Unit` (or `true`) as the key:

```kotlin
// CORRECT: runs once when the composable enters composition
LaunchedEffect(Unit) {
    viewModel.loadProfile()
}
```

`LaunchedEffect(Unit)` only restarts if the composable **leaves and re-enters composition entirely** — not on recomposition caused by state changes inside the composable.

## The Rule (from the wiki)

From **[[Compose Side Effects]]**:

> **Key parameter rules:**
> - Pass all mutable variables used in the block as keys
> - Exception: wrap in `rememberUpdatedState` if the variable should update without restart
> - `LaunchedEffect(true)` or `LaunchedEffect(Unit)` = runs once for composable's lifetime

From **[[Coroutines in Compose]]**:

> **Keys**: any value that should restart the effect; use `Unit` or `true` only for truly one-time effects

The table from [[Compose Side Effects]] makes the lifecycle contract explicit:

| API | Restarts On Key Change | Typical Use |
|---|---|---|
| `LaunchedEffect` | Yes — cancel + relaunch | Suspend work tied to composition |

## When You DO Want a Key

Use a meaningful key when the effect should re-run based on a specific state transition. For example, if `loadProfile()` should re-run when the `userId` changes:

```kotlin
LaunchedEffect(userId) {
    viewModel.loadProfile(userId)
}
```

Here, every change to `userId` correctly restarts the effect. But `passwordValue` is not that — it's UI input state, not a semantic trigger for profile loading.

## Quick Diagnostic

If you're unsure what's causing the re-trigger:

1. Look at what you passed as the key to `LaunchedEffect(...)`
2. Ask: "Does this value change when the user types?" If yes — wrong key.
3. Ask: "Should `loadProfile()` re-run every time this value changes?" If no — wrong key.

For a one-time screen-open load, the answer is always `LaunchedEffect(Unit)`.

---

**Pages consulted:** [[Compose Side Effects]], [[Coroutines in Compose]], [[Compose Recomposition and Stability]]
