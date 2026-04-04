# Compose Multiplatform (CMP) — State of the Art, April 2026

## Current Version

The latest stable release is **Compose Multiplatform 1.10.3** (patch on the 1.10 line released January 2026). The next major version, **1.11.0-beta01**, is in pre-release. The 1.10 line requires **Kotlin 2.1.20+** minimum, and the project has migrated to Kotlin language/API version 2.2. For Kotlin/Wasm targets, **Kotlin 2.3.10+** is required. The latest Jetpack Compose BOM for Android is **2026.03.00**.

Sources: [Compose Multiplatform 1.10.0 blog post](https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/), [What's new in 1.10.3](https://kotlinlang.org/docs/multiplatform/whats-new-compose-110.html), [Compatibility and versions](https://kotlinlang.org/docs/multiplatform/compose-compatibility-and-versioning.html), [GitHub releases](https://github.com/JetBrains/compose-multiplatform/releases)

## Platform Stability Levels (as of April 2026)

| Platform | Stability |
|---|---|
| Android | Stable (always was — it IS Jetpack Compose) |
| iOS | **Stable** since CMP 1.8.0 (May 2025) — production-ready |
| Desktop (JVM) | Stable |
| Web (Wasm) | **Beta** since CMP 1.9.0 (Sep 2025) |

**This is the single biggest change an agent with older training data would get wrong**: iOS was Alpha/Beta in 2023-2024. It has been **Stable since May 2025**.

Sources: [Stability of supported platforms](https://kotlinlang.org/docs/multiplatform/supported-platforms.html), [CMP 1.8.0 iOS Stable announcement](https://blog.jetbrains.com/kotlin/2025/05/compose-multiplatform-1-8-0-released-compose-multiplatform-for-ios-is-stable-and-production-ready/), [CMP 1.9.0 Web Beta](https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/)

## Major Features in CMP 1.10 (January 2026)

1. **Unified `@Preview` annotation** — A single `@Preview` in `commonMain` replaces three separate platform-specific annotations. All old annotations are deprecated.

2. **Navigation 3** — A new navigation library available on all CMP platforms. Key differences from Navigation 2:
   - You directly manage a `SnapshotStateList` back stack
   - Routes are serializable data objects; non-JVM platforms require **polymorphic serialization**
   - Uses `NavDisplay` composable and `rememberNavBackStack()`

3. **Compose Hot Reload 1.0 (Stable)** — Bundled with the CMP Gradle plugin, enabled by default for desktop targets.

4. **Native iOS Text Input** — Opt-in mode for `BasicTextField` that uses native iOS text input.

5. **Automatic resizing for native interop elements** on desktop and iOS.

Sources: [CMP 1.10.0 blog](https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/), [Navigation 3 docs](https://kotlinlang.org/docs/multiplatform/compose-navigation-3.html), [Hot Reload docs](https://kotlinlang.org/docs/multiplatform/compose-hot-reload.html)

## Breaking Changes an Agent Must Know About

1. **Compose Compiler fully on K2** — The old K1 compiler path is gone. The Compose compiler is part of the Kotlin compiler since Kotlin 2.0.
2. **Shader type change** — Non-Android `Shader` is now a dedicated Compose wrapper type.
3. **`Key.Home` deprecated** — Use `Key.MoveHome` instead.
4. **`NativePaint` and `NativeCanvas` typealiases deprecated**.
5. **`IdlingResource` moved** — No longer in `commonMain`; moved to android and desktop only.
6. **AGP 9 migration required** — Must migrate to `android-kmp-library` plugin.
7. **Kotlin language version 2.2** — The CMP project itself has migrated.

Sources: [CHANGELOG.md](https://github.com/JetBrains/compose-multiplatform/blob/master/CHANGELOG.md), [AGP 9 migration guide](https://kotlinlang.org/docs/multiplatform/multiplatform-project-agp-9-migration.html)

## Testing in Compose Multiplatform

### Common UI Testing (the primary approach)

CMP provides a **common test API** using the `runComposeUiTest` function:

```kotlin
import androidx.compose.ui.test.ExperimentalTestApi
import androidx.compose.ui.test.runComposeUiTest
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import kotlin.test.Test

@OptIn(ExperimentalTestApi::class)
class MyScreenTest {
    @Test
    fun buttonClickUpdatesText() = runComposeUiTest {
        setContent {
            MyScreen()
        }
        onNodeWithText("Click me").performClick()
        onNodeWithText("Clicked!").assertExists()
    }
}
```

**Gradle setup** — In `build.gradle.kts`, add to commonTest:

```kotlin
kotlin {
    sourceSets {
        commonTest.dependencies {
            implementation(kotlin("test"))
            @OptIn(org.jetbrains.compose.ExperimentalComposeLibrary::class)
            implementation(compose.uiTest)
        }
    }
}
```

**Key limitations:**
- The API is still **`@ExperimentalTestApi`**
- Common tests cannot run via Android local test configurations
- JUnit-specific APIs (`createComposeRule()`) are only available in desktop test source sets
- Same finders, assertions, actions as Jetpack Compose testing

Sources: [Testing Compose Multiplatform UI](https://kotlinlang.org/docs/multiplatform/compose-test.html), [Desktop UI testing with JUnit](https://kotlinlang.org/docs/multiplatform/compose-desktop-ui-testing.html)

### Desktop-Only Testing (JUnit-based)

For desktop targets specifically, a JUnit4-based API is available using `compose.desktop.uiTestJUnit4`:

```kotlin
sourceSets {
    val desktopTest by getting {
        dependencies {
            implementation(compose.desktop.uiTestJUnit4)
            implementation(compose.desktop.currentOs)
        }
    }
}
```

### Screenshot/Snapshot Testing

- **Roborazzi** — Supports CMP including iOS and Desktop targets.
- **Paparazzi** — JVM-based rendering, primarily Android-focused.
- **ComposablePreviewScanner** — Auto-generates screenshot tests from `@Preview` annotations.

## Project Setup — Recommended Approach (2026)

1. Use the Kotlin Multiplatform wizard in IntelliJ IDEA or at [kmp.jetbrains.com](https://kmp.jetbrains.com)
2. Select all needed targets: Android, iOS, Desktop, Web
3. Project structure: `composeApp` module with source sets: `commonMain`, `androidMain`, `iosMain`, `jvmMain`, `wasmJsMain`, `commonTest`
4. Do NOT auto-upgrade AGP when the IDE prompts
5. Minimum versions: Kotlin 2.1.20+, Gradle 7.6+, Java 11+

Sources: [Create your first CMP app](https://kotlinlang.org/docs/multiplatform/compose-multiplatform-create-first-app.html), [Project structure](https://kotlinlang.org/docs/multiplatform/multiplatform-discover-project.html)

## Summary: What an AI Agent Would Get Wrong from Older Training Data

| Topic | Old/Wrong | Current (April 2026) |
|---|---|---|
| iOS stability | Alpha or Beta | **Stable** since May 2025 |
| Web stability | Alpha | **Beta** since Sep 2025 |
| Compose compiler | Separate artifact to version-match | Built into Kotlin compiler since Kotlin 2.0 |
| Preview annotation | Separate per-platform annotations | **Unified `@Preview`** in commonMain |
| Navigation | Only Navigation 2 | **Navigation 3** available and recommended |
| Hot Reload | Experimental or nonexistent | **Stable 1.0**, bundled by default |
| UI testing API | Desktop-only or very experimental | **Common `runComposeUiTest`** across all targets |
| Kotlin version | 1.9.x or 2.0.x | **2.1.20+ minimum**, 2.2 for latest features |
| AGP compatibility | Standard android library/app plugins | Must use new **android-kmp-library** plugin |
| Compose for Web target | `jsMain` with DOM API | **`wasmJsMain`** with Wasm as primary |

## Sources

- [Compose Multiplatform 1.10.0 Blog](https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/)
- [CMP 1.8.0: iOS Stable](https://blog.jetbrains.com/kotlin/2025/05/compose-multiplatform-1-8-0-released-compose-multiplatform-for-ios-is-stable-and-production-ready/)
- [CMP 1.9.0: Web Beta](https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/)
- [Navigation 3 Docs](https://kotlinlang.org/docs/multiplatform/compose-navigation-3.html)
- [Compose Hot Reload Docs](https://kotlinlang.org/docs/multiplatform/compose-hot-reload.html)
- [CMP Testing Docs](https://kotlinlang.org/docs/multiplatform/compose-test.html)
- [CMP Compatibility and Versioning](https://kotlinlang.org/docs/multiplatform/compose-compatibility-and-versioning.html)
- [GitHub Releases](https://github.com/JetBrains/compose-multiplatform/releases)
