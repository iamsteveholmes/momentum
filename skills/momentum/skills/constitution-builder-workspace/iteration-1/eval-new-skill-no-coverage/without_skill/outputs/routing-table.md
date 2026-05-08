## Quick Routing

Maps developer symptoms to wiki queries. Each entry names what you're observing or asking, then gives the query that retrieves the relevant KB content.

---

### Kotest Assertion Basics

**"How do I assert equality / check a value in Kotest?"**
→ `wiki-query kotest shouldBe assertion matchers`

**"My test passed but I'm not sure it actually asserted anything — how do I catch that?"**
→ `wiki-query kotest assertion mode AssertionMode.Error ProjectConfig`

**"I want all assertion failures in one test run, not just the first one."**
→ `wiki-query kotest assertSoftly soft assertions globalAssertSoftly`

**"How do I assert that a function throws an exception — and inspect the message?"**
→ `wiki-query kotest shouldThrow shouldThrowExactly exception assertions`

**"I need to check that every element in a list satisfies a condition — or that exactly N do."**
→ `wiki-query kotest inspectors forAll forExactly forAtLeastOne collection assertions`

**"I want to write a domain-specific matcher — e.g., `user should beActive()`."**
→ `wiki-query kotest custom matcher Matcher MatcherResult extension`

---

### Kotest Spec Structure and Style

**"Which spec style should I use — FunSpec, DescribeSpec, BehaviorSpec?"**
→ `wiki-query kotest spec styles FunSpec DescribeSpec BehaviorSpec decision`

**"I'm getting a backtick error on `when` inside BehaviorSpec."**
→ `wiki-query kotest BehaviorSpec when keyword backtick`

**"How do I skip or disable a single test without deleting it?"**
→ `wiki-query kotest xtest xdescribe xthen disable test`

**"I want deeply nested test groups — which spec style allows that?"**
→ `wiki-query kotest FreeSpec nesting arbitrary depth`

---

### Kotest Project Configuration and Lifecycle

**"How do I set a global timeout so slow tests fail automatically?"**
→ `wiki-query kotest AbstractProjectConfig timeout specTimeout`

**"My mocks are bleeding state between tests — how do I reset them reliably?"**
→ `wiki-query kotest MockK clearMocks afterTest isolation beforeTest`

**"I want each test to start with a fresh spec instance to avoid shared state."**
→ `wiki-query kotest IsolationMode InstancePerRoot SingleInstance`

**"How do I run setup and teardown code once per spec vs. once per test?"**
→ `wiki-query kotest lifecycle hooks beforeSpec afterSpec beforeTest afterEach`

**"I want to share database setup logic across multiple spec files."**
→ `wiki-query kotest TestListener BeforeSpecListener ProjectConfig extensions`

---

### Coroutines in Kotest Tests

**"Do I need `runBlocking` to call a suspend function in a Kotest test?"**
→ `wiki-query kotest suspend function native coroutine support runBlocking`

**"My code has a `delay()` call and the test takes forever — how do I skip real delays?"**
→ `wiki-query kotest coroutineTestScope virtual time TestCoroutineScheduler advanceTimeBy`

**"How do I control the virtual clock and assert that time-sensitive behavior fires at the right moment?"**
→ `wiki-query kotest testCoroutineScheduler advanceTimeBy currentTime runCurrent`

**"My coroutine test is blocking even with coroutineTestScope — what could cause that?"**
→ `wiki-query kotest blocking test mode coroutineDispatcherFactory Thread.sleep`

**"I want virtual time to apply to all tests in my spec, not just one."**
→ `wiki-query kotest coroutineTestScope spec-level project-level configuration`

---

### Testing Kotlin Flow with Turbine

**"How do I test a Flow without collecting it manually in a coroutine?"**
→ `wiki-query Turbine Flow testing awaitItem awaitComplete`

**"My ViewModel exposes a StateFlow — how do I assert on its emissions?"**
→ `wiki-query Turbine StateFlow awaitItem initial value cancelAndIgnoreRemainingEvents`

**"I need to assert on two flows in the same test — state and events."**
→ `wiki-query Turbine testIn multiple flows turbineScope`

**"How do I test a SharedFlow that fires navigation or one-shot events?"**
→ `wiki-query Turbine SharedFlow event awaitItem replay`

**"My Turbine test fails with 'No more items' — how do I debug that?"**
→ `wiki-query Turbine named turbine error messages cancelAndIgnoreRemainingEvents`

---

### Non-Deterministic and Async Testing

**"I'm testing code that retries internally or settles after a delay — how do I avoid Thread.sleep?"**
→ `wiki-query kotest eventually async non-deterministic testing`

**"I want to assert that a condition stays true for N seconds — not just that it reaches it."**
→ `wiki-query kotest continually stability assertion`

**"I only need a fixed retry count, not a duration-based eventually."**
→ `wiki-query kotest retry fixed attempts interval`

**"How do I configure eventually with exponential backoff and exception filtering?"**
→ `wiki-query kotest eventuallyConfig backoff fibonacci exponential suppressExceptions`

---

### Data-Driven and Property-Based Testing

**"I have the same test logic for 10 different inputs — how do I avoid repeating the test body?"**
→ `wiki-query kotest data-driven withData automatic test generation`

**"I want to test an invariant across hundreds of random inputs, not just a fixed list."**
→ `wiki-query kotest property-based testing Arb checkAll forAll generators`

**"I need a custom generator for my domain type — e.g., a valid `UserId`."**
→ `wiki-query kotest arbitrary custom generator bind Arb.bind`

**"My property test fails non-deterministically in CI — how do I pin the seed?"**
→ `wiki-query kotest PropTestConfig seed reproducible property test CI`

---

### Compose UI Testing

**"How do I write a Compose UI test in the `commonTest` source set?"**
→ `wiki-query runComposeUiTest commonTest compose.uiTest CMP`

**"What's the difference between `runComposeUiTest` and `createComposeRule()`?"**
→ `wiki-query runComposeUiTest createComposeRule desktop JUnit CMP common`

**"How do I find a node by text, tag, or semantic property in a Compose test?"**
→ `wiki-query ComposeUiTest onNodeWithText onNodeWithTag semantics finders`

**"My Compose test targets desktop — what source set and Gradle task do I use?"**
→ `wiki-query compose desktop UI testing desktopTest createComposeRule JUnit`

**"How do I inject state or content into a Compose test before assertions?"**
→ `wiki-query ComposeUiTest setContent rule.setContent state injection`

**"How do I assign test tags to Compose nodes so I can find them in tests?"**
→ `wiki-query Modifier.testTag testTag semantics Compose test finders`

**"My Compose UI test involves a coroutine-driven state update — how do I synchronize?"**
→ `wiki-query Compose UI test coroutine state update synchronization dispatcher`

---

### MockK Integration

**"How do I mock a suspend function with MockK in a Kotest test?"**
→ `wiki-query MockK coEvery coVerify suspend function coroutine`

**"My MockK mocks are retaining state from a previous test — how do I reset them?"**
→ `wiki-query MockK clearMocks clearAllMocks afterTest lifecycle Kotest`

---

### Cross-Cutting: TDD Practice with Kotest

**"Which Kotest spec style fits London-school (outside-in) TDD with mocks?"**
→ `wiki-query TDD Kotest spec style BehaviorSpec London school MockK`

**"Can I use property tests as acceptance-level tests in a TDD loop?"**
→ `wiki-query TDD Kotest property testing invariant red-green-refactor`

**"Why does `coroutineTestScope` push me toward writing the test first?"**
→ `wiki-query TDD Kotest coroutineTestScope forcing function specification-first`
