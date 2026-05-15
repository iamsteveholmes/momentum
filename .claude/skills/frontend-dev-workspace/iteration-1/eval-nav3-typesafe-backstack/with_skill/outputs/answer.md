# Nav 3 setup for Home + WorkoutDetail(workoutId: Long)

For nornspun-client (Android + Desktop, CMP 1.10.2), use the **multiplatform `SavedStateConfiguration` overload** of `rememberNavBackStack`. Desktop is JVM, but going through `SavedStateConfiguration` keeps the door open for iOS/Web and is the documented multiplatform path.

## 1. Define routes as `@Serializable` `NavKey`s in `commonMain`

```kotlin
// commonMain/.../navigation/Routes.kt
import androidx.navigation3.runtime.NavKey
import kotlinx.serialization.Serializable

sealed interface AppRoute : NavKey {
    @Serializable
    data object Home : AppRoute

    @Serializable
    data class WorkoutDetail(val workoutId: Long) : AppRoute
}
```

A `sealed interface` is the right pattern here — small app, single module — and it enables `subclassesOfSealed<AppRoute>()` for the serializers module.

## 2. Build a `SavedStateConfiguration` with polymorphic serializers

```kotlin
// commonMain/.../navigation/AppNavConfig.kt
import androidx.savedstate.SavedStateConfiguration
import kotlinx.serialization.modules.SerializersModule
import kotlinx.serialization.modules.polymorphic
import kotlinx.serialization.modules.subclass

internal val AppNavConfig = SavedStateConfiguration {
    serializersModule = SerializersModule {
        polymorphic(NavKey::class) {
            subclass(AppRoute.Home::class, AppRoute.Home.serializer())
            subclass(AppRoute.WorkoutDetail::class, AppRoute.WorkoutDetail.serializer())
        }
    }
}
```

This is what enables back stack persistence without reflection — the `SavedStateConfiguration` overload of `rememberNavBackStack` registers with `rememberSaveable` under the hood, and the polymorphic serializers let the saver round-trip your sealed `NavKey` hierarchy through bundled saved-state on Android (which is what survives process death / config change / low-memory kill).

> Important: do **not** use the Android-only `rememberNavBackStack(HomeRoute)` overload. It uses reflection and will not compile against `commonMain` — even though Desktop is also JVM, you want the same code path the wiki documents as the multiplatform-canonical one.

## 3. Wire `NavDisplay` in your root composable

```kotlin
// commonMain/.../App.kt
@Composable
fun App() {
    MaterialTheme {
        val backStack = rememberNavBackStack(AppNavConfig, AppRoute.Home)

        NavDisplay(
            backStack = backStack,
            onBack = { backStack.removeLastOrNull() },
        ) { key ->
            when (key) {
                is AppRoute.Home -> HomeScreen(
                    onWorkoutClick = { id -> backStack.add(AppRoute.WorkoutDetail(id)) }
                )
                is AppRoute.WorkoutDetail -> WorkoutDetailScreen(
                    workoutId = key.workoutId,
                    onBack = { backStack.removeLastOrNull() },
                )
            }
        }
    }
}
```

The back stack is a `SnapshotStateList<NavKey>` you own — navigation is just `backStack.add(...)` / `backStack.removeLastOrNull()`. No `NavController`, no string routes, no `Bundle` argument plumbing — `workoutId` is a constructor parameter on the data class.

## 4. Dependencies (`libs.versions.toml`)

```toml
[versions]
nav3 = "1.0.0-alpha05"

[libraries]
nav3-runtime = { module = "org.jetbrains.androidx.navigation3:navigation3-runtime", version.ref = "nav3" }
nav3-ui      = { module = "org.jetbrains.androidx.navigation3:navigation3-ui",      version.ref = "nav3" }
```

Add both to `commonMain` dependencies in `composeApp/build.gradle.kts`. If you later want responsive layouts, pull in `androidx.compose.material3.adaptive:adaptive-navigation3` and use `rememberListDetailSceneStrategy<NavKey>()` — but it's not needed for two screens.

## Why this satisfies "back stack survives process death"

- `rememberNavBackStack` is internally `rememberSaveable` over the `SnapshotStateList`, using the registered `SavedStateConfiguration` saver.
- Each `NavKey` is `@Serializable`, registered polymorphically on `NavKey::class` — so kotlinx.serialization knows how to encode/decode the runtime type plus its fields (`workoutId: Long`).
- On Android, this writes through to the activity's saved-state bundle and is restored on process recreation.
- On Desktop there's no process-death lifecycle, so the same setup degrades to in-memory state for the JVM session, which is what you want.

## Routing intent into the back stack (MVI alignment)

Keep the standing rule from frontend-dev intact: composables emit intents, ViewModels emit effects, the root composable observes the navigation `Effect` channel and mutates the back stack. Example:

```kotlin
LaunchedEffect(viewModel) {
    viewModel.effects.collect { effect ->
        when (effect) {
            is HomeEffect.OpenWorkout -> backStack.add(AppRoute.WorkoutDetail(effect.id))
        }
    }
}
```

Use `Channel(BUFFERED).receiveAsFlow()` for the effect stream so a config change doesn't replay the navigation.

## Stability caveat

The wiki flags this: Nav 3 multiplatform is currently `1.0.0-alpha05`. It's the right direction, but pin the version and don't be surprised by alpha churn. Nav 2 (`androidx.navigation:navigation-compose`) is still production-common in 2026.

**Pages consulted:** [[Navigation 3 CMP]]

**Gaps:** The wiki page doesn't include a worked process-death restoration test recipe — a Kotest spec that asserts the saver round-trips `AppRoute.WorkoutDetail(123L)` would be a useful addition to [[Navigation 3 CMP]].
