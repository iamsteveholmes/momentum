# Technology Detection Heuristics

Mapping from build/config files to technology stack components. Used by discovery subagents and the orchestrator to classify detected technologies.

## Build File → Ecosystem Mapping

| File | Ecosystem | Primary Language |
|---|---|---|
| `build.gradle.kts` / `build.gradle` | JVM/Kotlin/Android | Kotlin or Java |
| `settings.gradle.kts` | Multi-module JVM/KMP | Kotlin |
| `gradle/libs.versions.toml` | Gradle version catalog | — |
| `package.json` | Node.js/JavaScript/TypeScript | JS/TS |
| `tsconfig.json` | TypeScript | TypeScript |
| `Cargo.toml` | Rust | Rust |
| `pyproject.toml` / `setup.py` | Python | Python |
| `go.mod` | Go | Go |
| `pom.xml` | Maven/JVM | Java/Kotlin |
| `Gemfile` | Ruby | Ruby |
| `composer.json` | PHP | PHP |
| `CMakeLists.txt` | C/C++ | C/C++ |
| `Package.swift` | Swift/iOS | Swift |
| `pubspec.yaml` | Dart/Flutter | Dart |
| `mise.toml` / `.tool-versions` | Tool versions (cross-ecosystem) | — |

## KMP/CMP Detection Signals

These signals indicate Kotlin Multiplatform or Compose Multiplatform — technologies with significant training data staleness as of 2025-2026.

| Signal | Technology | Where to Find |
|---|---|---|
| `kotlin("multiplatform")` plugin | KMP | build.gradle.kts plugins block |
| `org.jetbrains.compose` plugin | Compose Multiplatform | build.gradle.kts plugins block |
| `iosArm64()`, `iosSimulatorArm64()` | KMP iOS targets | build.gradle.kts kotlin block |
| `jvm()`, `js()`, `wasmJs()` | KMP additional targets | build.gradle.kts kotlin block |
| `compose.uiTest` | CMP testing | build.gradle.kts dependencies |
| `commonMain`, `commonTest` directories | KMP source sets | src/ directory structure |
| `NavDisplay`, `NavKey` imports | Navigation 3 | Kotlin source files |
| `runComposeUiTest` | CMP common testing | Test files |

## Framework Detection by Dependency

| Dependency Pattern | Framework | Notes |
|---|---|---|
| `io.kotest:kotest-*` | Kotest | Check version: 5.x vs 6.x have incompatible APIs |
| `io.insert-koin:koin-*` | Koin DI | — |
| `io.ktor:ktor-*` | Ktor | Client vs. server matters |
| `org.jetbrains.kotlinx:kotlinx-serialization-*` | kotlinx.serialization | — |
| `io.mockk:mockk` | MockK | — |
| `com.google.dagger:hilt-*` | Hilt DI | Android-specific |
| `androidx.navigation:navigation-*` | Jetpack Navigation | Check version: 2.x vs 3.x |
| `com.squareup.retrofit2:*` | Retrofit | — |
| `react` / `react-dom` | React | Check version: 18.x vs 19.x |
| `next` | Next.js | Check version: app router vs pages router |
| `vue` | Vue.js | Check version: 2.x vs 3.x |
| `@angular/core` | Angular | — |
| `fastapi` | FastAPI | — |
| `django` | Django | — |
| `flask` | Flask | — |
| `express` | Express.js | — |
| `actix-web` / `axum` | Rust web | — |

## Staleness Risk Assessment

Technologies where AI training data is most likely stale (fast-moving ecosystems with breaking changes in 2025-2026):

| Technology | Staleness Risk | Key Changes Since ~2024 Training |
|---|---|---|
| Kotlin Multiplatform | **High** | AGP 9 migration, target shortcut removal, withJava deprecated |
| Compose Multiplatform | **High** | iOS stable, Navigation 3, unified @Preview, Hot Reload 1.0 |
| Kotest | **High** | 5.x→6.x breaking changes, KSP replaces compiler plugin |
| Next.js | **High** | App Router matured, Server Actions, React 19 integration |
| React | **Medium** | React 19, use() hook, Server Components |
| Kotlin (language) | **Medium** | Context parameters, name-based destructuring, explicit backing fields |
| Gradle | **Medium** | Gradle 9.x, declarative DSL |
| AGP | **High** | AGP 9 with built-in Kotlin, android-kmp-library plugin |
| Swift/SwiftUI | **Medium** | Swift 6 concurrency, Observation framework |
| Rust | **Low** | Stable ecosystem, fewer breaking changes |
| Python | **Low** | Stable ecosystem, 3.12-3.13 are incremental |
| Go | **Low** | Stable ecosystem, incremental changes |
