# Nav 3 Type-Safe Routes + Process-Death-Surviving Back Stack (CMP: Android + Desktop)

## Wiki Source

Answer grounded in wiki pages consulted via `wiki-query`:
- **[[Navigation 3 CMP]]** — core concept page (high confidence, extracted 0.90)
- **[[projects/nornspun-agentic-kb/references/web-kotlinlang-org-multiplatform-compose-navigation-3]]** — official CMP docs distillate (extracted 0.96)
- **[[source-navigation3-cmp-johnoreilly]]** — practical walkthrough (extracted 0.88)
- **[[MVI Pattern in Compose]]** — grep pass for Channel/Effect pattern

---

## What Nav 3 Is

Navigation 3 is a complete redesign of the AndroidX navigation library. The back stack is a **user-owned `SnapshotStateList<NavKey>`** — you add and remove entries directly. `NavDisplay` renders whichever entry is on top. It is not a version bump of Nav 2; the programming model is substantially different.

- Alpha version: `1.0.0-alpha05`
- CMP support (Android, iOS, Desktop, Web) added in **CMP 1.10**

---

## Dependencies

```toml
# gradle/libs.versions.toml
[versions]
nav3 = "1.0.0-alpha05"

[libraries]
nav3-ui = { module = "org.jetbrains.androidx.navigation3:navigation3-ui", version.ref = "nav3" }
# Optional: scoped ViewModels per destination
nav3-lifecycle-viewmodel = { module = "androidx.lifecycle:lifecycle-viewmodel-navigation3", version = "2.10.0-alpha05" }
```

Add `nav3-ui` to `commonMain` dependencies.

---

## Step 1 — Define Type-Safe Routes

Routes implement `NavKey` and are annotated with `@Serializable`. Arguments are constructor parameters — no Bundles, no String encoding.

```kotlin
// commonMain
import androidx.navigation3.runtime.NavKey
import kotlinx.serialization.Serializable

@Serializable
data object Home : NavKey

@Serializable
data class WorkoutDetail(val workoutId: Long) : NavKey
```

For a two-route app, grouping under a sealed interface enables the `subclassesOfSealed` shortcut:

```kotlin
@Serializable
sealed interface Route : NavKey

@Serializable
data object Home : Route

@Serializable
data class WorkoutDetail(val workoutId: Long) : Route
```

---

## Step 2 — SavedStateConfiguration (Required for Process Death + Multiplatform)

`rememberNavBackStack` has two overloads:

| Overload | Platform | Process Death |
|---|---|---|
| `rememberNavBackStack(Home)` | JVM only (reflection) | No |
| `rememberNavBackStack(config, Home)` | All platforms | Yes |

Always use the `SavedStateConfiguration` overload. It uses `rememberSaveable` internally, which survives Android process death. Desktop has no process death, but identical code across targets means no platform divergence.

```kotlin
// commonMain — define once at the app level
private val navConfig = SavedStateConfiguration {
    serializersModule = SerializersModule {
        polymorphic(NavKey::class) {
            subclassesOfSealed<Route>()   // works when routes share a sealed interface
        }
    }
}
```

If routes are not sealed, register each explicitly:

```kotlin
private val navConfig = SavedStateConfiguration {
    serializersModule = SerializersModule {
        polymorphic(NavKey::class) {
            subclass(Home::class, Home.serializer())
            subclass(WorkoutDetail::class, WorkoutDetail.serializer())
        }
    }
}
```

---

## Step 3 — Wire Up Back Stack and NavDisplay

```kotlin
// commonMain — App entry point
@Composable
fun App() {
    val backStack = rememberNavBackStack(navConfig, Home)

    NavDisplay(
        backStack = backStack,
        onBack = { backStack.removeLastOrNull() }
    ) { key ->
        when (key) {
            is Home -> HomeScreen(
                onWorkoutClick = { id ->
                    backStack.add(WorkoutDetail(workoutId = id))
                }
            )
            is WorkoutDetail -> WorkoutDetailScreen(
                workoutId = key.workoutId,
                onBack = { backStack.removeLastOrNull() }
            )
        }
    }
}
```

Navigation operations:
- **Navigate forward**: `backStack.add(WorkoutDetail(workoutId = id))`
- **Navigate back**: `backStack.removeLastOrNull()`

---

## MVI Integration

The wiki ([[MVI Pattern in Compose]]) documents `Channel<Effect>` for one-shot navigation events. However, the wiki explicitly flags this as an **open question**:

> "MVI + Navigation 3 (CMP): Where does navigation live when back stack is user-owned `SnapshotStateList`? `Channel<Effect>` pattern uncertain."

Two approaches consistent with standing MVI rules:

### Option A — ViewModel emits NavigateToDetail effect, composable handles it (recommended)

```kotlin
// ViewModel
sealed interface WorkoutEffect {
    data class NavigateToDetail(val workoutId: Long) : WorkoutEffect
}

private val _effects = Channel<WorkoutEffect>(Channel.BUFFERED)
val effects: Flow<WorkoutEffect> = _effects.receiveAsFlow()

fun onWorkoutClicked(id: Long) {
    viewModelScope.launch {
        _effects.send(WorkoutEffect.NavigateToDetail(id))
    }
}

// Composable — collects effects and mutates backStack
LaunchedEffect(Unit) {
    viewModel.effects.collect { effect ->
        when (effect) {
            is WorkoutEffect.NavigateToDetail ->
                backStack.add(WorkoutDetail(workoutId = effect.workoutId))
        }
    }
}
```

This preserves unidirectional data flow: ViewModel does not hold a reference to the back stack.

### Option B — Composable passes navigation callback into ViewModel

Since the back stack is a plain `SnapshotStateList`, the composable can pass navigation lambdas as callbacks into intents. Simpler for small apps, but couples the ViewModel to navigation more directly.

Option A is the safer choice for strict MVI.

---

## Summary Table

| Concern | Solution |
|---|---|
| Type-safe routes | `@Serializable data class/object : NavKey` |
| Process death | `SavedStateConfiguration` + explicit `SerializersModule` |
| Back stack | `rememberNavBackStack(navConfig, Home)` |
| NavDisplay | `NavDisplay(backStack, onBack) { key -> when(key) {...} }` |
| Navigate forward | `backStack.add(WorkoutDetail(workoutId = id))` |
| Navigate back | `backStack.removeLastOrNull()` |
| MVI effects | `Channel<Effect>` → composable collects → mutates backStack |

---

## Known Gaps

- The wiki does not resolve the MVI + Nav 3 backstack ownership question with a canonical pattern. Option A above is consistent with the MVI standing rules but is not wiki-verified.
- Nav 3 is still in alpha (`1.0.0-alpha05`). Evaluate stability before committing to production use.
