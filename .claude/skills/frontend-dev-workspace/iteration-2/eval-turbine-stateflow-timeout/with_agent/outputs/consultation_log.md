# Consultation Log — Turbine `awaitItem()` Timeout Diagnosis

## Query

**Routing table match:** "Flow emissions not arriving — `awaitItem` times out"
**Query terms used:** `Turbine awaitItem awaitComplete testIn turbineScope StateFlow`
**Skill invoked:** `wiki-query` via the Skill tool

---

## Step 1: hot.md Pre-Check

**File:** `/Users/steve/projects/nornspun-agentic-kb/hot.md`

Found a directly relevant entry:

> [2026-05-09T00:00:00Z] WIKI_RESEARCH topic="Turbine + StateFlow + Kotest MVI ViewModel testing" — 3 rounds, 10 sources. Key: stateIn activation requires a subscriber (backgroundScope or Turbine test{}); Turbine uses UnconfinedTestDispatcher internally (prevents conflation); two assertion strategies (.value for final state, awaitItem() for transitions); turbineScope + testIn for dual state+effects testing; Kotest BehaviorSpec has a known bug with Dispatchers.setMain in given{} blocks — use FunSpec or put assertions in then{} blocks. 7 pages created, 1 updated.

This confirmed dedicated pages exist and narrowed the search immediately.

---

## Step 2: Index Pass (Grep)

**Command:** `grep -r -l "Turbine\|turbineScope\|awaitItem\|testIn" /Users/steve/projects/nornspun-agentic-kb/ --include="*.md"`

**Top candidates identified:**
- `synthesis/Research: Turbine × Kotest × MVI ViewModel Testing.md` — primary synthesis page
- `concepts/MVI ViewModel Testing with Turbine and Kotest.md` — concrete Kotest patterns
- `concepts/Turbine.md` — Turbine API reference
- `concepts/ViewModel StateFlow Testing Patterns.md` — dispatcher setup and conflation patterns

---

## Step 3: Full Read (4 pages)

Escalated directly to Step 4 (full read) on all four candidates — the query is specific enough that section-grep would miss the interaction patterns between pages.

### Page 1: `synthesis/Research: Turbine × Kotest × MVI ViewModel Testing.md`

**Key insights extracted:**
- `Dispatchers.setMain(testDispatcher)` in `beforeTest` is mandatory — `viewModelScope` uses `Main`, which doesn't exist in JVM unit tests
- `stateIn(WhileSubscribed(5000))` does not activate without a subscriber — this is the "#1 gotcha" and the most likely root cause of the symptom described
- Turbine uses `UnconfinedTestDispatcher` internally, which prevents conflation by making the collector run eagerly on each emission
- Conflation is dispatcher-driven: `StandardTestDispatcher` lets the producer run to completion before the collector is scheduled
- Two valid assertion strategies: `.value` for final state (simpler), `awaitItem()` for transitions (requires Turbine)
- `turbineScope` + `testIn` for dual state+effects testing — both flows must be subscribed before the action fires
- Kotest BehaviorSpec has a known bug (#3577): assertions in `given {}` blocks fail; use `FunSpec` or put assertions in `then {}` blocks

### Page 2: `concepts/MVI ViewModel Testing with Turbine and Kotest.md`

**Key insights extracted:**
- Concrete `LoginViewModelTest : FunSpec` template with `beforeTest`/`afterTest` dispatcher setup
- Kotest matchers compose naturally with Turbine: `awaitItem() shouldBe LoginUiState(isLoading = true)`
- Fake repository pattern using `MutableSharedFlow` gives tests explicit control over emission timing
- `coroutineTestScope = true` alternative — still requires explicit `Dispatchers.setMain(testCoroutineScheduler.asTestDispatcher())`
- Complete `turbineScope` + `testIn` example for state + effects simultaneous testing
- Named turbines (`name = "state"`) produce clearer error messages: "No more items for `state`"

### Page 3: `concepts/Turbine.md`

**Key insights extracted:**
- Turbine's `test {}` block automatically activates `stateIn` — it is itself a subscriber
- `StateFlow` always replays current value to new subscribers: the first `awaitItem()` always returns the initial value
- `skipItems(n)` for skipping initial/intermediate values; `expectMostRecentItem()` for final-state-only assertions
- `awaitComplete()` is for finite/cold flows — `StateFlow` never completes so `awaitComplete()` will always timeout on `StateFlow`
- `turbineScope` ensures all turbines are properly closed even if the test throws

### Page 4: `concepts/ViewModel StateFlow Testing Patterns.md`

**Key insights extracted:**
- The exact `backgroundScope.launch(UnconfinedTestDispatcher(testScheduler)) { viewModel.uiState.collect {} }` pattern for activating `stateIn` without Turbine
- Conflation root cause: with `StandardTestDispatcher`, producer runs to completion before collector is scheduled — only most recent value seen
- Dispatcher injection pattern for `IO`/`Default` dispatchers inside ViewModel — inject `TestDispatcher` for hermetic tests
- Dependencies snapshot: `kotlinx-coroutines-test:1.8.0`, `turbine:1.2.1`, `kotest-runner-junit5:5.9.1`

---

## Routing Decision

The routing table match was exact:
- Symptom: "Flow emissions not arriving — `awaitItem` times out"
- Table entry: `wiki-query Turbine awaitItem awaitComplete testIn turbineScope StateFlow`
- Mode used: `wiki-query` (not direct answer), because the question is API-specific and project-convention-specific

The wiki had dedicated research pages from a 2026-05-09 research session specifically on this topic. The answer was grounded entirely in wiki content with no training-knowledge fallback needed.

---

## Escalation Path

- Step 1 (hot.md): Found directly relevant entry — confirmed pages exist
- Step 2 (index/grep): Identified 4 candidate pages
- Step 4 (full read): Read all 4 pages — no escalation to vault-wide grep needed
- Total pages read: 4
- Mode: normal
- Escalated: false
