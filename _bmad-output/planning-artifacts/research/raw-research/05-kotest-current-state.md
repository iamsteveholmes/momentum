# Kotest in 2026: Comprehensive State-of-the-Art Research

## 1. Current Version and Release Timeline

The **latest stable release is Kotest 6.1.10**, released **March 30, 2025**. The 6.1.x line has seen rapid iteration with 10 patch releases since January 2025. Version 6.2 is in development but unreleased. ([GitHub Releases](https://github.com/kotest/kotest/releases), [Changelog](https://kotest.io/docs/changelog.html))

**Minimum requirements for Kotest 6.x: JDK 11 and Kotlin 2.2.** ([Kotest 6.0 Release Notes](https://kotest.io/docs/next/release6/))

## 2. Critical Changes from 5.x to 6.x (Agent Gotchas)

An agent trained on Kotest 5.x documentation will produce **broken code**:

### Classpath Scanning Removed
`@AutoScan` is **gone**. Extensions must be explicitly registered via `ProjectConfig` or `@ApplyExtension`. ([6.0 Changes Discussion](https://github.com/kotest/kotest/issues/3918))

### ProjectConfig Location Changed
ProjectConfig is now discovered **by default at `io.kotest.provided.ProjectConfig`**. No longer auto-discovered from arbitrary packages. ([Kotest 6.0 Release Notes](https://kotest.io/docs/next/release6/))

### Compiler Plugin Replaced by KSP
For KMP (non-JVM targets), the old compiler plugin is gone. Use **KSP Gradle plugin** alongside the renamed `io.kotest` Gradle plugin. ([Setup docs](https://kotest.io/docs/framework/project-setup.html))

### JVM Runs Exclusively on JUnit Platform
On JVM, Kotest runs **exclusively on JUnit Platform**. Dependency is `kotest-runner-junit5`. ([Setup docs](https://kotest.io/docs/framework/project-setup.html))

### Data-Driven Testing Merged into Core
`kotest-framework-datatest` is no longer a separate dependency. Old 4.x-era **table-driven testing** now requires `kotest-assertions-table` explicitly. ([Kotest 6.0 Release Notes](https://kotest.io/docs/next/release6/))

### Extension Config Changed
Extensions are now `override val extensions` (a val), not `override fun extensions()` (a function). ([Kotest 6.0 Release Notes](https://kotest.io/docs/next/release6/))

### Deprecated Isolation Modes
`InstancePerTest` and `InstancePerLeaf` are **deprecated**. Use `InstancePerRoot` instead. ([Kotest 6.0 Release Notes](https://kotest.io/docs/next/release6/))

### Assertion Renames
- `io.kotest.matchers.maps.contain` renamed to `io.kotest.matchers.maps.mapcontain`
- `Matcher`, `MatcherResult`, and `and`/`or` operators moved from `kotest-assertions-api` to `kotest-assertions-shared`

### System Extensions Removed
`System.exit` and `System.env` override extensions are gone due to Java `SecurityManager` deprecation. ([Kotest 6.0 Release Notes](https://kotest.io/docs/next/release6/))

## 3. Gradle Setup (Current 6.1.x)

### JVM Only
```kotlin
plugins {
    kotlin("jvm")
}

tasks.withType<Test>().configureEach { useJUnitPlatform() }

dependencies {
    testImplementation("io.kotest:kotest-runner-junit5:6.1.10")
    testImplementation("io.kotest:kotest-assertions-core:6.1.10")
    testImplementation("io.kotest:kotest-property:6.1.10") // optional
}
```

### Kotlin Multiplatform
```kotlin
plugins {
    kotlin("multiplatform")
    id("com.google.devtools.ksp") version "<ksp-version>" // KSP MUST come first
    id("io.kotest") version "6.1.10"
}

kotlin {
    jvm()
    iosArm64()

    sourceSets {
        commonTest {
            dependencies {
                implementation("io.kotest:kotest-framework-engine:6.1.10")
                implementation("io.kotest:kotest-assertions-core:6.1.10")
            }
        }
        jvmTest {
            dependencies {
                implementation("io.kotest:kotest-runner-junit5:6.1.10")
            }
        }
    }
}

tasks.withType<Test>().configureEach { useJUnitPlatform() }
```

**JVM targets use `kotest-runner-junit5`; all non-JVM targets use `kotest-framework-engine` plus KSP/Kotest Gradle plugins.** ([Setup docs](https://kotest.io/docs/framework/project-setup.html))

## 4. Testing Styles

Kotest offers **8 testing styles**, all functionally equivalent:

| Style | Pattern | Best For |
|---|---|---|
| **FunSpec** | `test("name") { }` with `context` | General purpose. **Default recommendation.** |
| **BehaviorSpec** | `given/when/then` with `and` | BDD, acceptance-test style |
| **DescribeSpec** | `describe/it` with `context` | Ruby/JS developers |
| **ShouldSpec** | `should("name") { }` with `context` | Lightweight BDD |
| **FreeSpec** | `"name" - { }` nesting | Arbitrary depth nesting |
| **WordSpec** | `"subject" should { "verb" { } }` | Scalatest-style |
| **FeatureSpec** | `feature/scenario` | Cucumber-inspired |
| **ExpectSpec** | `expect("name") { }` with `context` | Minimal syntax |

**For TDD with an agent:** FunSpec is the safest default. BehaviorSpec is ideal for acceptance tests.

## 5. Assertions and Matchers

**350+ matchers** across categories. Primary assertion style — infix `shouldBe`:

```kotlin
name shouldBe "Steve"
list shouldHaveSize 3
result.shouldBeSuccess()
```

**Key categories:** General (`shouldBe`, `shouldBeNull`, `shouldThrow`), String, Collection, Map, Numeric, Date/Time, Concurrency, Result.

**Soft assertions:**
```kotlin
assertSoftly {
    name shouldBe "Steve"
    age shouldBe 30
}
```

## 6. Property-Based Testing

**Two generator types:**
- **`Arb<T>`** — infinite random stream with built-in edge cases
- **`Exhaustive<T>`** — finite set, every value tested

```kotlin
checkAll<String, String> { a, b ->
    (a + b) shouldHaveLength (a.length + b.length)
}
```

Built-in Arbs cover **100+ types**. ([Property-Based Testing docs](https://kotest.io/docs/proptest/property-based-testing.html))

## 7. Data-Driven Testing (withData)

In 6.1+, each spec style has **typed variants**:

```kotlin
class TempTests : FunSpec({
    withTests(
        Pair(0, 32),
        Pair(100, 212),
    ) { (celsius, fahrenheit) ->
        celsiusToFahrenheit(celsius) shouldBe fahrenheit
    }
})
```

| Spec Style | Container Variant | Leaf Variant |
|---|---|---|
| FunSpec | `withContexts` | `withTests` |
| BehaviorSpec | `withGivens`, `withWhens` | `withThens` |
| DescribeSpec | `withDescribes`, `withContexts` | `withIts` |
| FeatureSpec | `withFeatures` | `withScenarios` |

## 8. Coroutine Testing

Every Kotest test body is a **suspend function by default**. No `runTest` wrapper needed.

For **virtual time control**:
```kotlin
class MyTest : FunSpec({
    coroutineTestScope = true

    test("delays are skipped") {
        val deferred = async {
            delay(1_000)
            42
        }
        testCoroutineScheduler.advanceTimeBy(1_000)
        deferred.await() shouldBe 42
    }
})
```

## 9. Summary of What Would Trip Up an Agent

| Stale assumption | Current reality |
|---|---|
| `@AutoScan` for extension discovery | Removed. Must register explicitly. |
| `kotest-framework-datatest` dependency | Merged into core. |
| `override fun extensions()` | Changed to `override val extensions` |
| Compiler plugin for multiplatform | Replaced with KSP |
| `InstancePerTest` / `InstancePerLeaf` | Deprecated. Use `InstancePerRoot` |
| ProjectConfig auto-discovered anywhere | Must be at `io.kotest.provided.ProjectConfig` |
| Current Kotest is 5.x | Current stable is **6.1.10** |
| JDK 8 support | Requires JDK 11, Kotlin 2.2 minimum |

## Sources

- [Kotest GitHub Releases](https://github.com/kotest/kotest/releases)
- [Kotest 6.0 Release Notes](https://kotest.io/docs/next/release6/)
- [Kotest Setup / Project Configuration](https://kotest.io/docs/framework/project-setup.html)
- [Kotest Testing Styles](https://kotest.io/docs/framework/testing-styles.html)
- [Kotest Core Matchers](https://kotest.io/docs/assertions/core-matchers.html)
- [Kotest Property-Based Testing](https://kotest.io/docs/proptest/property-based-testing.html)
- [Kotest Data-Driven Testing](https://kotest.io/docs/framework/datatesting/data-driven-testing.html)
- [Setting up Kotest on KMP](https://alyssoncirilo.com/blog/kotest-kmp-setup/)
- [Kotest Coroutine Test Dispatcher](https://kotest.io/docs/framework/coroutines/test-coroutine-dispatcher.html)
