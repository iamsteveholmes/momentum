# constitution-builder Process Notes

## Run Summary

**Skill:** constitution-builder (momentum)
**Task:** Build routing table for a compose+kotest skill covering Kotlin coroutines in tests, Kotest assertion styles, and Compose UI testing with composeTestRule.
**Date:** 2026-05-04

---

## KB Audit Results

### Covered (7 concept areas — full routing entries generated)

1. **Kotest assertion DSL** — `kotest-assertion-dsl.md` has shouldBe, shouldThrow, shouldThrowExactly, assertSoftly, inspectors, custom matchers, withClue. Comprehensive.
2. **Kotest spec styles** — `kotest-spec-styles.md` covers all 8 styles, BehaviorSpec `when` gotcha, x-prefixed disable variants.
3. **Kotest coroutine testing** — `kotest-coroutine-testing.md` covers native suspend support, `coroutineTestScope`, `testCoroutineScheduler` operations (advanceTimeBy, runCurrent, advanceUntilIdle).
4. **Kotest eventually / non-deterministic** — `Kotest Eventually and Non-Deterministic Testing.md` covers `eventually`, `continually`, `retry`, backoff strategies, suspend lambda support.
5. **Kotest project config** — `Kotest Project Configuration.md` covers isolation modes, timeouts, global coroutineTestScope, assertion mode, MockK SingleInstance gotcha.
6. **Turbine (Flow testing)** — `Turbine.md` covers awaitItem/awaitComplete/awaitError, testIn for multiple flows, turbineScope, StateFlow initial value behavior, SharedFlow zero-replay behavior.
7. **Compose UI testing (CMP)** — Two reference pages: `web-kotlinlang-org-multiplatform-compose-test.md` (runComposeUiTest, commonTest) and `web-kotlinlang-org-multiplatform-compose-desktop-ui-testing.md` (createComposeRule, desktopTest).

### Partial (2 areas — thin coverage, entries generated pointing to closest pages)

1. **composeTestRule (Android JUnit4 native)** — KB has CMP equivalents (`createComposeRule` for desktop, `runComposeUiTest` for common) but not the classic Android `@get:Rule val composeTestRule = createComposeRule()` pattern explicitly. Entries route to the closest available pages.
2. **Compose state change assertions in tests** — No dedicated "assert Compose state in a test" page. Coverage is indirect via `snapshotFlow`, `StateFlow`, `Turbine`, and `Coroutines in Compose`. Entries bridge across these pages.

### Gaps (0 — no outright gaps)

The KB has a full Kotest research synthesis (`Research: Kotest Kotlin Testing Framework.md`), a TDD × Kotest cross-domain synthesis, and all major Kotest concept pages. Kotest is well-ingested. MockK entity page covers the co-prefix pattern. No gaps requiring wiki-ingest were found.

---

## Routing Table Statistics

- **Total entries generated:** 31
- **Subsections:** 7
  - Kotest Assertion Styles: 6 entries
  - Kotest Spec Styles and Test Structure: 5 entries
  - Kotlin Coroutine Testing (Kotest + coroutineTestScope): 6 entries
  - Suspending Functions and MockK: 3 entries
  - Flow Testing with Turbine: 5 entries
  - Async / Non-Deterministic Testing with eventually: 4 entries
  - Compose UI Testing: 7 entries (split 4 composeTestRule/runComposeUiTest + 3 coroutine integration)

Within range of the 15–40 target; 31 entries is on the comprehensive side but avoids padding — each entry names a specific observable developer scenario.

---

## Notable Observations

1. **Kotest is thoroughly ingested** — The KB has a 3-round synthesis, all major concept pages, and a cross-domain synthesis with TDD. The skill will have excellent constitution coverage for Kotest scenarios.

2. **composeTestRule routing is a partial gap** — The KB focuses on CMP's `runComposeUiTest` and desktop `createComposeRule`. The Android-native `ComposeTestRule` from `compose-test-junit4` isn't a first-class page. Entries route to the correct CMP pages but won't answer pure Android (non-CMP) composeTestRule questions as precisely. Recommendation: ingest the Android Compose testing docs if the skill targets Android-native (non-CMP) projects.

3. **The `quick answer:` prefix was used selectively** (8 of 31 entries) for factual lookups (exact API names, gotcha syntax) where the answer lives in page summaries/frontmatter and doesn't require reading full page bodies.

4. **MockK entry count is intentionally low (3)** — MockK is a collaborator, not a primary topic. The three entries cover the exact developer failure mode (co-prefix for suspend) rather than general mocking usage.

5. **Turbine is well-placed** — Given that the skill covers coroutine testing, Turbine entries are critical. The KB's Turbine page is thorough and the entries map precisely to the observable failure modes a developer would encounter.

6. **Workflow ran cleanly through all 6 phases** — No interactive decisions required beyond the simulated inputs. Gap-fill was a no-op (per constraint and because KB coverage was sufficient). Review phase accepted all entries as-is.
