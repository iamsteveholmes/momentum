## Quick Routing

Use this table first. Match your situation to a scenario and run the wiki-query before answering.

### Kotest Assertion Styles

- **Using `shouldBe` / `shouldNotBe` and unsure of the full matcher set available** → `wiki-query Kotest assertion DSL matchers shouldBe shouldThrow`
- **Need to assert on exception type or message — `shouldThrow` vs `shouldThrowExactly` distinction** → `wiki-query quick answer: shouldThrow vs shouldThrowExactly Kotest subtype behavior`
- **Want to collect all assertion failures in one test block rather than failing on first** → `wiki-query Kotest assertSoftly soft assertions`
- **Testing a collection — need exact order, any order, or quantity-based inspection** → `wiki-query Kotest collection matchers shouldContainExactly forExactly inspectors`
- **Adding context to a failing assertion for better diagnostics** → `wiki-query quick answer: Kotest withClue contextual failure messages`
- **Writing a custom matcher to reuse across tests** → `wiki-query Kotest custom matcher Matcher<T> MatcherResult`

### Kotest Spec Styles and Test Structure

- **Choosing between FunSpec, DescribeSpec, BehaviorSpec — team has no prior preference** → `wiki-query Kotest spec styles FunSpec DescribeSpec BehaviorSpec decision`
- **Using BehaviorSpec for BDD given/when/then and hitting a Kotlin keyword conflict** → `wiki-query quick answer: Kotest BehaviorSpec when keyword backtick`
- **Need to inline-disable a single test or container without deleting it** → `wiki-query Kotest xtest xdescribe disable test inline`
- **Configuring timeout, isolation mode, or coroutine scope at project level** → `wiki-query Kotest AbstractProjectConfig isolation mode timeout coroutineTestScope`
- **State leaking between tests when using MockK with SingleInstance isolation** → `wiki-query Kotest MockK isolation SingleInstance clearMocks beforeTest`

### Kotlin Coroutine Testing (Kotest + coroutineTestScope)

- **Calling a suspend function in a Kotest test — unsure if runBlocking is needed** → `wiki-query Kotest native suspend support coroutine test lambdas`
- **Testing code that uses `delay()` — want to skip real wait time** → `wiki-query Kotest coroutineTestScope virtual time advanceTimeBy delay`
- **Using `testCoroutineScheduler` — which operation runs what** → `wiki-query quick answer: testCoroutineScheduler advanceTimeBy runCurrent advanceUntilIdle`
- **Enabling virtual time control globally vs per-spec vs per-test** → `wiki-query Kotest coroutineTestScope configuration scope project spec test`
- **Testing timeout behavior without waiting for real time to elapse** → `wiki-query Kotest virtual time timeout coroutine test scheduler`
- **Suspend function test fails with unexpected coroutine context or dispatcher** → `wiki-query Kotest coroutine context dispatcher test scope`

### Suspending Functions and MockK

- **Mocking a suspend function — `every` not working for coroutine calls** → `wiki-query MockK coEvery coVerify suspend function co-prefix`
- **Verifying a suspend function was called with specific args** → `wiki-query quick answer: MockK coVerify coVerifySequence suspend assertion`
- **Mock returning different values on successive suspend calls** → `wiki-query MockK coEvery returns answerList suspend multiple calls`

### Flow Testing with Turbine

- **Testing a StateFlow or SharedFlow emission sequence** → `wiki-query Turbine awaitItem awaitComplete Flow testing Kotest`
- **Testing multiple flows in parallel — state and events updating together** → `wiki-query Turbine testIn multiple flows parallel assertions`
- **StateFlow always replays its current value — test consuming initial state** → `wiki-query Turbine StateFlow initial value replay awaitItem cancelAndIgnoreRemainingEvents`
- **SharedFlow navigation event or one-shot effect not emitting in test** → `wiki-query Turbine SharedFlow replay zero awaitItem suspend`
- **Flow test failing with unconsumed events at end of block** → `wiki-query quick answer: Turbine ensureAllEventsConsumed cancelAndIgnoreRemainingEvents`

### Async / Non-Deterministic Testing with eventually

- **State not immediately consistent after action — using Thread.sleep is brittle** → `wiki-query Kotest eventually async non-deterministic testing`
- **Configuring retry interval, backoff strategy, or max attempts for eventually** → `wiki-query Kotest eventuallyConfig interval fibonacci backoff retries`
- **Asserting that a condition does NOT change over a time window** → `wiki-query quick answer: Kotest continually stability assertion duration`
- **Retrying a flaky HTTP or external call a fixed number of times** → `wiki-query Kotest retry fixed count interval suspend`

### Compose UI Testing (composeTestRule / runComposeUiTest)

- **Setting up Compose UI tests in commonTest for a CMP project** → `wiki-query runComposeUiTest CMP commonTest setup compose.uiTest dependency`
- **Using createComposeRule() for a Desktop JVM target** → `wiki-query createComposeRule desktop JUnit Compose CMP desktopTest`
- **Finding a node by test tag and asserting on its text or state** → `wiki-query Compose UI test onNodeWithTag testTag assertTextEquals performClick`
- **Setting composable content inside a test and triggering recomposition** → `wiki-query Compose test setContent ComposeUiTest receiver node interaction`
- **Asserting that a composable reacted to a state change** → `wiki-query Compose state change recomposition test snapshotFlow StateFlow Turbine`
- **Clicking a button in a Compose test and verifying a suspend side effect fired** → `wiki-query Compose UI test performClick LaunchedEffect coroutine side effect`
- **Compose test on Android — instrumented test setup with testInstrumentationRunner** → `wiki-query CMP Android instrumented test runner androidTarget KotlinSourceSetTree`

### Kotest + Compose State: Coroutine Integration

- **Collecting a ViewModel's StateFlow in a Compose test — lifecycle awareness** → `wiki-query collectAsStateWithLifecycle Compose StateFlow lifecycle test`
- **LaunchedEffect in test — controlling when coroutine launches and what it does** → `wiki-query LaunchedEffect coroutine composition Compose test`
- **Testing snapshotFlow — converting Compose state to Flow for assertion** → `wiki-query snapshotFlow Compose State Flow coroutine test`
