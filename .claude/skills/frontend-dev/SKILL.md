---
name: frontend-dev
description: "Nornspun client frontend development — Compose Multiplatform (CMP), MVI architecture, Kotest/Turbine testing, SQLDelight, and Ktor client. Use when implementing screens, wiring state, writing tests, setting up navigation, querying the database, or making HTTP requests in the nornspun-client project. Also invoke when you hear 'add a screen', 'write a test', 'fix the ViewModel', 'hook up the API', or any nornspun-client implementation work."
model: claude-opus-4-6
effort: medium
---

# nornspun-client frontend-dev

Compose Multiplatform app targeting Android and Desktop. Shared UI in `composeApp/`, shared business logic and data in `shared/`. MVI architecture throughout.

**Stack:** CMP 1.10.2 · Material3 · Ktor client · SQLDelight · Kotest · Turbine · kotlinx.coroutines · kotlinx.serialization

---

## Standing Rules

### Test-Driven Development

**Red → Green → Refactor. Always in that order, always at that granularity.**

- **No production code without a failing test.** Write one test for one behavior. Watch it fail. Then write code.
- **Stop writing the test once it fails.** Compilation failure counts as failure. Don't write more test than needed to produce a red state.
- **Stop writing production code once the test passes.** Write only what makes the failing test green — nothing more.
- **Refactor under green.** Clean up structure, naming, and duplication only after the test passes. The test suite is the safety net — don't change behavior during refactor.

TDD is a development discipline, not a testing strategy. Tests drive design. Implementation follows tests, never precedes them.

### MVI Architecture

- **State is a single immutable data class.** No partial or conflicting states — loading, data, and error are mutually exclusive fields, never simultaneous truths.
- **Intents are a sealed interface.** Every user action that the ViewModel handles must be a named member of the sealed interface. No raw strings, no untyped events.
- **Effects use `Channel`, not `StateFlow`.** Navigation, toasts, and one-time events must not replay on resubscription. Use `Channel(BUFFERED).receiveAsFlow()`.
- **State flows down, intents flow up.** Composables observe `StateFlow<UiState>` and emit `Intent` — never write to state directly from a composable.
- **ViewModel owns the state machine.** No business logic in composables. A composable that calls a use case directly is an architecture violation.

### Kotest Spec Style

- **FunSpec for unit tests** — neutral, no BDD ceremony, clearest for red-green-refactor discipline.
- **BehaviorSpec for acceptance tests** — `given`/`when`/`then` naming only when the test is written against a user-facing acceptance criterion.
- **`coroutineTestScope = true` for any test touching suspend functions or virtual time.** This is non-negotiable — testing coroutine timing after the fact is not meaningful.
- **Never use FreeSpec.** Maximum flexibility is maximum discipline risk.
- **MockK state leaks between specs in `SingleInstance` mode.** Always reinitialize mocks in `beforeTest`, not `beforeSpec`.

---

## Completion Gate

Before marking any component done and moving to the next, run all three checks:

**1. Scope — only what the story explicitly requires.**
If you are about to create a file or feature not listed in the story tasks, stop. If the spec says "do not create X unless it already exists," that is a hard prohibition, not a suggestion. No extra files, no bonus abstractions.

**2. Spec fidelity — read the AC word-for-word.**
TDD verifies behavior but cannot catch tests that accidentally pass despite wrong output. After tests go green, re-read the acceptance criterion literally and check:
- String formats match exactly (`"level {n}"` not `"{n}"`)
- Types match exactly (`Int` not `String` where `Int` is specified)
- Canonical strings (closing phrases, readback templates) match character-for-character
- Visibility (`private`/`public`/`internal`) matches what the spec states

**3. Test coverage — verify assertions test the right thing.**
A test that embeds the expected value in the input (e.g. `startingLevel = "level one"` when the test should assert that the code adds `"level "`) passes without testing anything. Before moving on, verify:
- Every required test case from the AC exists by name or behavior
- Assertions test what the production code produces, not what the test itself set up
- Effects (`SharedFlow`, `Channel` emissions) are exercised with Turbine — not assumed to fire

---

## Quick Routing

Use this table first. Match your situation to a scenario and run the wiki-query before answering.

### Compose — Recomposition and Side Effects

- **Composable recomposing more than expected** → `wiki-query Compose recomposition stability Strong Skipping unstable types`
- **`LaunchedEffect` running on every recomposition instead of once** → `wiki-query Compose LaunchedEffect key recomposition side effects`
- **`DisposableEffect` or `SideEffect` — which to use** → `wiki-query Compose side effects DisposableEffect SideEffect all eight APIs`
- **`snapshotFlow` — converting Compose state to Flow for observation** → `wiki-query snapshotFlow Compose State Flow coroutine`

### Compose — Layout, Modifiers, and Lists

- **Modifier order causing unexpected visual result** → `wiki-query Compose modifiers ordering graphicsLayer drawBehind`
- **`LazyColumn` items losing state on scroll or recomposing too aggressively** → `wiki-query Compose lazy lists key contentType recomposition animateItem`
- **Pager setup or page offset effects** → `wiki-query Pager Compose HorizontalPager PagerState peek scroll effects`

### Compose — Animation

- **Choosing the right animation API** → `wiki-query Compose animation APIs animate*AsState AnimatedVisibility AnimatedContent decision tree`
- **Shared element transition between screens** → `wiki-query Compose shared element transitions sharedElement sharedBounds Nav`
- **Predictive back gesture animation** → `wiki-query Compose predictive back PredictiveBackHandler SeekableTransitionState`

### MVI and State Management

- **`StateFlow` value change not triggering recomposition** → `wiki-query MVI StateFlow collectAsStateWithLifecycle Compose lifecycle`
- **Effect (navigation, toast) firing on every recomposition instead of once** → `wiki-query MVI Effect Channel SharedFlow replay receiveAsFlow`
- **ViewModel scoping across destinations in Nav 3** → `wiki-query ViewModel CMP nav scoping initializer lambda viewModelScope`
- **`coroutines` in ViewModel — which scope, which dispatcher** → `wiki-query coroutines dispatchers viewModelScope IO Default Main`

### Navigation

- **Nav 3 back stack and `NavDisplay` setup** → `wiki-query Navigation 3 CMP NavDisplay back stack type-safe SavedStateConfiguration`
- **Deep link handling per platform** → `wiki-query CMP navigation deep links navDeepLink ExternalUriHandler platform`

### Kotest — Coroutines and Flow

- **Coroutine test hangs, or `delay()` runs in real time** → `wiki-query Kotest coroutineTestScope TestCoroutineScheduler virtual time advanceTimeBy`
- **Which spec style to use for a new test** → `wiki-query TDD Kotest spec style FunSpec BehaviorSpec coroutineTestScope forcing function`
- **Flow emissions not arriving — `awaitItem` times out** → `wiki-query Turbine awaitItem awaitComplete testIn turbineScope StateFlow`
- **Polling for an async condition in a test** → `wiki-query Kotest eventually continually retry backoff`
- **Mock state leaking between test cases** → `wiki-query Kotest isolation mode SingleInstance beforeTest MockK reset`

### Kotest — Assertions and Data

- **Asserting on a sealed class or nested data class** → `wiki-query Kotest assertion shouldBe sealed class data class inspection`
- **Soft assertions — accumulate failures instead of stopping** → `wiki-query Kotest soft assertions assertSoftly shouldBe`
- **Property-based testing — generate inputs instead of hand-writing cases** → `wiki-query Kotest property based testing Arb checkAll forAll shrinking`
- **Data-driven tests with multiple input sets** → `wiki-query Kotest data driven testing withData`

### SQLDelight

- **Query result not updating UI reactively** → `wiki-query SQLDelight asFlow mapToList coroutines dispatcher requirements`
- **Multiplatform driver setup (Android + Desktop)** → `wiki-query SQLDelight platform drivers Android desktop JVM expect actual factory`
- **Schema change requires migration** → `wiki-query SQLDelight migrations sqm versioning AfterVersion callbacks`
- **Writing a test against the database** → `wiki-query SQLDelight query testing in-memory driver cross-platform`
- **Gradle source set layout or codegen not running** → `wiki-query SQLDelight multiplatform setup Gradle source directory layout`

### Ktor Client

- **Which engine for Android vs Desktop** → `wiki-query Ktor engine selection CIO OkHttp Darwin KMP expect actual HTTP2`
- **Request failing silently, timeout, or retry behavior** → `wiki-query Ktor client error handling HttpTimeout HttpRequestRetry plugin ordering`
- **Server-sent events or streaming response** → `wiki-query SSE streaming Ktor client Flow collect reconnection buffer`
- **Serialization not working with Ktor** → `wiki-query Ktor serialization ContentNegotiation kotlinx.serialization install`

### Material3 and Adaptive Layout

- **Theme not applying or dark mode not working** → `wiki-query Material3 theming colorScheme MaterialTheme dynamic color dark`
- **Adaptive layout for different window sizes** → `wiki-query Compose adaptive layouts WindowSizeClass NavigationSuiteScaffold ListDetailPaneScaffold`
