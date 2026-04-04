# Kotlin Multiplatform (KMP) — State of the Art, April 2026

## 1. Current Kotlin Version Timeline

The **current stable release is Kotlin 2.3.20** (March 16, 2026). The **latest EAP is Kotlin 2.4.0-Beta1** (March 31, 2026).

| Version | Date | Type |
|---------|------|------|
| **2.4.0-Beta1** | Mar 31, 2026 | EAP/Beta |
| **2.3.20** | Mar 16, 2026 | Tooling (current stable) |
| 2.3.10 | Feb 5, 2026 | Bug fix |
| 2.3.0 | Dec 16, 2025 | Language release |
| 2.2.20 | Sep 10, 2025 | Tooling release |
| 2.2.0 | Jun 23, 2025 | Language release |

Release cadence since 2.0: language releases (2.x.0) every 6 months, tooling releases (2.x.20) 3 months after, bug-fix releases as needed. ([Kotlin release process](https://kotlinlang.org/docs/releases.html))

## 2. Critical Breaking Changes (Things That Make Old Docs Wrong)

### A. AGP 9 — The Android Target Plugin Swap

**AGP 9.0 breaks the old way of declaring Android targets in KMP.**

- The old `androidTarget {}` block in the KMP Gradle plugin is **deprecated** (warning in 2.3.0, will be removed).
- Android targets now use Google's **`com.android.kotlin.multiplatform.library`** plugin instead.
- You must rename `androidTarget` to `android` in your build scripts.
- AGP 9.0 requires **Gradle 9.1.0+** and **JDK 17+**.
- Legacy APIs will be **fully removed in AGP 10** (expected H2 2026).

Sources: [AGP 9 migration guide](https://kotlinlang.org/docs/multiplatform/multiplatform-project-agp-9-migration.html), [JetBrains blog](https://blog.jetbrains.com/kotlin/2026/01/update-your-projects-for-agp9/), [Google KMP Android plugin docs](https://developer.android.com/kotlin/multiplatform/plugin)

### B. Apple x86_64 Targets Being Removed

- In **Kotlin 2.3.0**, `macosX64`, `iosX64`, `tvosX64`, `watchosX64` were demoted to **support-tier 3**.
- **Kotlin 2.4.0 plans to remove x86_64 Apple targets entirely.**
- Minimum Apple OS versions raised: iOS/tvOS from 12.0 to **14.0**, watchOS from 5.0 to **7.0**.
- The old `ios()`, `watchos()`, `tvos()` shortcut functions were **removed in 2.2.0**.

Source: [What's new in Kotlin 2.3.0](https://kotlinlang.org/docs/whatsnew23.html), [Compatibility guide](https://kotlinlang.org/docs/multiplatform/multiplatform-compatibility-guide.html)

### C. `withJava()` Phased Out

- From Kotlin 2.1.20, Java source sets are created **by default** in JVM targets.
- `withJava()` is deprecated (warning in Kotlin 2.1.20, error in Gradle 9.0).
- The Gradle `Application` plugin no longer works with KMP from Gradle 8.7+.

### D. `kotlin-android` Plugin Deprecated

- AGP 9.0.0 includes **built-in Kotlin support**.
- The standalone `kotlin-android` Gradle plugin is deprecated and no longer needed with AGP 9+.

### E. Target Presets API Removed

- The `presets` property, `KotlinTargetPreset` interface, and `fromPreset()` were **removed in Kotlin 2.2.0**.

### F. Bitcode Embedding DSL Removed

- `embedBitcode` DSL was **removed in Kotlin 2.3.0** (Apple dropped bitcode in Xcode 15).

### G. Language Version Floor Raised

- Kotlin 2.3.0 dropped support for `-language-version=1.8` entirely, and `-language-version=1.9` on non-JVM platforms.

## 3. Major New Features (2025-2026)

### A. Context Parameters (Stable in 2.4.0)

```kotlin
context(logger: Logger)
fun process() {
    logger.info("Processing...")
}
```

Kotlin 2.4.0 also adds **explicit context arguments** to resolve ambiguity.

Source: [Context parameters docs](https://kotlinlang.org/docs/context-parameters.html)

### B. Name-Based Destructuring (Kotlin 2.3.20)

A new destructuring mode that matches by **property name** instead of positional `componentN()` functions.

Source: [Kotlin 2.3.20 release](https://blog.jetbrains.com/kotlin/2026/03/kotlin-2-3-20-released/)

### C. Explicit Backing Fields (Experimental, 2.3.0)

```kotlin
// New (experimental, opt-in with -Xexplicit-backing-fields)
val city: StateFlow<String> field = MutableStateFlow("")
```

### D. Swift Export (Available by Default in 2.2.20)

Translates Kotlin code **directly into Swift** without the Objective-C intermediary layer.

Source: [Swift export docs](https://kotlinlang.org/docs/native-swift-export.html)

### E. Swift Package Manager Dependencies (2.4.0-Beta1)

KMP projects can now **declare Swift packages as dependencies** in Gradle configuration.

Source: [Adding Swift packages as dependencies](https://kotlinlang.org/docs/multiplatform/multiplatform-spm-import.html)

### F. Kotlin/Wasm Now Beta (2.2.20)

`wasmJs` and `wasmWasi` targets are now Beta with built-in browser debugging support.

## 4. Project Setup — The Current Recommended Way (2026)

Three official paths:
1. **Kotlin Multiplatform Wizard** (web tool) — generates template project
2. **Android Studio New Project wizard** — File > New > Project > Kotlin Multiplatform
3. **Adding KMP to existing Android project** — "Kotlin Multiplatform Shared Module" template

Key notes:
- Install the **Kotlin Multiplatform Android Studio Plugin** from JetBrains
- Use **JetBrains Runtime (JBR)** as the project JDK
- KMP is **officially supported by Google** for sharing business logic

Source: [KMP quickstart](https://kotlinlang.org/docs/multiplatform/quickstart.html), [Android KMP setup](https://developer.android.com/kotlin/multiplatform/setup)

## 5. Version Compatibility Matrix (Current)

| Kotlin | Gradle | AGP | Xcode |
|--------|--------|-----|-------|
| 2.3.20 | 7.6.3 -- 9.3.0 | 8.2.2 -- 9.0.0 | 26.0 |
| 2.3.10 | 7.6.3 -- 9.0.0 | 8.2.2 -- 9.0.0 | 26.0 |

## 6. Summary: What Would Trip Up an Agent

1. `androidTarget {}` is deprecated — use Google's plugin with `android {}`
2. `ios()` / `watchos()` / `tvos()` shortcuts no longer exist
3. `withJava()` is deprecated — Java source sets created by default
4. `fromPreset()` API is gone
5. Apple x86_64 targets are tier-3 and about to be removed
6. Minimum iOS/tvOS is 14.0, watchOS is 7.0
7. Swift Export exists and is available by default (experimental)
8. Current stable Kotlin is **2.3.20**, not 2.0.x or 2.1.x
9. Context parameters are a new language feature (stable in 2.4.0)
10. Name-based destructuring is new (2.3.20)

## Sources

- [Kotlin Releases](https://kotlinlang.org/docs/releases.html)
- [What's New in Kotlin 2.3.0](https://kotlinlang.org/docs/whatsnew23.html)
- [Kotlin 2.3.20 Released](https://blog.jetbrains.com/kotlin/2026/03/kotlin-2-3-20-released/)
- [KMP Compatibility Guide](https://kotlinlang.org/docs/multiplatform/multiplatform-compatibility-guide.html)
- [AGP 9 Migration Guide](https://kotlinlang.org/docs/multiplatform/multiplatform-project-agp-9-migration.html)
- [KMP Quickstart](https://kotlinlang.org/docs/multiplatform/quickstart.html)
- [Context Parameters Docs](https://kotlinlang.org/docs/context-parameters.html)
- [Swift Export Docs](https://kotlinlang.org/docs/native-swift-export.html)
