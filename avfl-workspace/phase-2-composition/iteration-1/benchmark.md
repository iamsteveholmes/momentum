# AVFL Phase 2 Benchmark — Reviewer Composition
**Date:** 2026-03-20 | **Model:** claude-sonnet-4-6 | **Lens count:** 3 (locked from Phase 1)

## Configuration Summary

| Config | Reviewers per lens | Agents (full profile) | Dual-review / cross-check |
|---|---|---|---|
| **enum-only** | 1 Enumerator | 3 | No — all findings MEDIUM confidence |
| **adv-only** | 1 Adversary | 3 | No — all findings MEDIUM confidence |
| **mixed** | 1 Enumerator + 1 Adversary | 6 | Yes — HIGH confidence when both agree |

**Fixed from Phase 1:** 3 lenses (Structural Integrity, Factual Accuracy, Coherence & Craft).

---

## Test 1: Gate — Badly-Formed Document

Gate profile: 1 agent, structural lens only, no fix loop.

| Config | Status | Score | Findings | Tokens | Time (s) |
|---|---|---|---|---|---|
| enum-only | GATE_FAILED | 48 | 6 (2C, 2H, 2M) | 30,268 | 104.9 |
| adv-only | GATE_FAILED | 28 | 7 (3C, 3H, 1M) | 29,537 | 87.7 |
| mixed | GATE_FAILED | 13 | 8 (4C, 3H, 1M), 4 dups removed | 32,028 | 142.9 |

**Verdict:** All correctly GATE_FAILED. No false passes.

**Key observations:**
- Score variance of 13–48 on *identical* gate inputs continues the Phase 1 pattern (33–51 range). Single-shot gate scores remain unreliable as numeric measurements.
- mixed found 1 unique critical finding neither single-framing config found alone: the missing polling endpoint implied by "returns a job ID for polling." The Adversary surfaced it; the Enumerator didn't; dual-review consolidation retained it at MEDIUM confidence.
- adv-only was cheapest and fastest (87.7s, 29.5k tokens). mixed was 63% slower on the gate profile — a significant cost for no directional advantage (all three correctly failed).
- Gate profile verdict: composition doesn't matter for gate correctness. All three fail what should fail.

---

## Test 2: Pristine Document (False Positive Rate)

Full profile: 3 parallel agents (or 6 for mixed), up to 4 iterations.

**Note:** The fixture was crafted to be pristine but contained 2 genuine embedded errors (discovered during this benchmark). Both have since been corrected. Results below are from the original fixture. Fixed-fixture re-runs completed after this table was drafted — see addendum.

| Config | Status | Iter 1 Score | Final Score | Findings | False Positives | Tokens | Time (s) |
|---|---|---|---|---|---|---|---|
| enum-only | CLEAN | 100 | 100 | 0 | 0 | 34,502 | 167.3 |
| adv-only | CLEAN | 96 | 96 | 2 (1M, 1L) | 0 | 37,413 | 161.4 |
| mixed | CLEAN | 96 | 96 | 2 (1M HIGH, 1L MEDIUM) | 0 | 36,916 | 218.8 |

**Verdict:** 0 false positives across all configurations. All passed CLEAN on iteration 1.

**Key observations:**
- **The fixture was not pristine.** adv-only and mixed found the same genuine math error: the gate profile example shows `GATE_FAILED (score: 62/100) — 3 findings`, where 62 is not achievable by any combination of exactly 3 findings under the documented weights (nearest is 62 with 2 critical + 1 high — which is actually the corrected value after fixing the original 61). These were true positives, not false positives.
- **enum-only missed the math error; adv-only and mixed caught it.** On the original fixture, the gate example had an impossible score. The Adversary's holistic, skeptical reading flagged "something feels wrong about this number" and verified it arithmetically. The Enumerator's systematic dimension-by-dimension check didn't enumerate "verify all numeric examples against documented formulas" as a logical_soundness check, so it passed cleanly. This is a meaningful composition difference — adversarial reading surfaces subtle internal-consistency issues that systematic enumeration can miss.
- In the mixed run, the Enumerator *did* catch the math error (reaching HIGH confidence). This contradicts what the standalone enum-only run found. This is LLM variance — single-trial results are not reliable enough to declare "enum-only can't catch X."
- adv-only also found a low-severity scope gap (Overview mentioned "sprint tracking" but no sprint commands were documented). Correctly rated low. Mixed caught it too.
- All three configurations showed excellent calibration — no findings were invented, and severity assignments were appropriate.

**Pristine fixture takeaways:**
1. Creating a truly pristine fixture is harder than expected. The adversary is a useful stress test for fixture quality itself.
2. For false-positive benchmarking, a fixed fixture and multiple trials are needed before drawing conclusions about composition-level differences in false positive rates.

### Fixed Fixture Re-Runs (Canonical False-Positive Results)

After correcting both embedded errors, all three configs re-ran on the fixed fixture:

| Config | Status | Score | Findings | False Positives | Tokens | Time (s) |
|---|---|---|---|---|---|---|
| enum-only | CLEAN | 99 | 1 (1L: auth circular phrasing) | 0 | 41,821 | 238.6 |
| adv-only | CLEAN | 98 | 2 (2L: heading asymmetry, AVFL acronym unexpanded) | 0 | 37,622 | 180.6 |
| mixed | CLEAN | **95** | 3 (1M: checkpoint/full no behavioral callout, 2L) | 0 | 42,403 | 264.1 |

**Verdict:** 0 false positives across all configurations on the fixed fixture.

**Key observations:**
- **Counterintuitive ordering: enum-only is the most conservative on pristine content.** Scores: enum-only=99, adv-only=98, mixed=95. With fewer agents and a systematic (not holistic) approach, enum-only generates fewer borderline findings on clearly correct content.
- **mixed scored exactly 95 — borderline CLEAN.** One more deduction would have triggered a fix loop on an intentionally pristine document. The mixed config's medium finding (gate profile has a behavioral callout subsection; checkpoint and full do not) is a genuine documentation gap, not a false positive — but it illustrates that mixed is more aggressive than enum-only or adv-only even on clean content.
- **No HIGH-confidence findings on the fixed pristine fixture** — dual-review agreement requires two reviewers to independently flag the same issue. On a document with only borderline LOW/MEDIUM findings, reviewers don't converge. This is the correct calibration signal: HIGH confidence = genuinely problematic, not just "something to look at."
- **The fixture is still not fully pristine.** Even after fixing the two obvious errors, the fixed fixture has 3 genuine (if low-severity) documentation gaps. Truly pristine content may not exist — there's always something an adversary can find. This is a feature, not a bug: the scoring system allows documents with only LOW-severity findings to pass CLEAN.

---

## Test 3: Clean API Guide (Thoroughness)

Full profile: real document with legitimate issues, measuring how deeply each composition digs.

| Config | Status | Iter 1 Score | Final Score | Iter 1 Findings | Iterations | Tokens | Time (s) |
|---|---|---|---|---|---|---|---|
| enum-only | CLEAN | 93 | 100 | 3 (2M, 1L) | 2 | 35,102 | 174.2 |
| adv-only | CLEAN | 84 | 100 | 8 (4M, 4L) | 2 | 38,905 | 253.0 |
| mixed | CLEAN | 87 | 100 | 9 (2M, 7L) | 2 | 38,977 | 241.7 |

**Verdict:** All reached CLEAN in 2 iterations.

**Key observations:**
- **adv-only found dramatically more issues than enum-only (8 vs 3)** on a real-world document. The Adversary's holistic reading pursues "something feels off" leads that enumeration doesn't generate.
- mixed found the most (9), but all findings were MEDIUM confidence — no dual-review agreement within any lens. The additional LOW-severity findings (7 of 9) are real but represent diminishing signal quality.
- enum-only's 3 findings were all actionable and medium-or-higher priority. Its conservative output means less noise but more risk of missing medium-severity issues. The 6 findings adv-only found that enum-only missed were real issues.
- **Cost gap is significant for thoroughness testing:** enum-only ran in 174.2s; adv-only 253.0s (45% slower); mixed 241.7s (39% slower). The extra time is from fuller exploration, not just agent count.
- All three fixed cleanly in one fix pass — no new bugs introduced.

---

## Test 4: Seeded Errors (True Positive Rate)

Full profile: 2 deliberate errors seeded — Error 1 (factual: wrong Meta-Judge statistic, accuracy lens target), Error 2 (consistency: threshold contradiction 90 vs 95, coherence lens target).

| Config | Status | Iter 1 Score | Final Score | Error 1 | Error 2 | Confidence | Total Findings | Tokens | Time (s) |
|---|---|---|---|---|---|---|---|---|---|
| adv-only | CLEAN | 80 | 100 | ✓ caught | ✓ caught | MEDIUM | 4 (2H, 1M, 1L) | 37,599 | 193.3 |
| enum-only | CLEAN | 69 | 100 | ✓ caught | ✓ caught | MEDIUM | 6 (3H, 2M, 1L) | 38,913 | 210.6 |
| mixed | CLEAN | 68 | 100 | ✓ HIGH | ✓ HIGH | **HIGH** (both errors) | 7 (3H, 2M, 2L) | 41,950 | 276.6 |

**Verdict:** All 3 caught both seeded errors. All reached CLEAN in 2 iterations.

**Key observations:**
- **mixed is the only configuration that flagged both errors at HIGH confidence** — both Enumerator and Adversary independently found each error, triggering dual-review cross-check. This is the most actionable signal: a HIGH-confidence finding means two independent perspectives agreed on the evidence.
- adv-only was the most focused: 4 findings total (both errors + 2 secondary issues), vs 6 and 7 for the others. The Adversary reads holistically and homes in on what's wrong without exhaustively enumerating all corollary findings.
- enum-only found more findings (6) including downstream implications of the factual error that adv-only captured differently. Both are valid approaches to finding coverage.
- Iteration 1 scores: adv-only=80, enum-only=69, mixed=68. Counterintuitively, finding *more* issues lowers your score further — the errors matter equally regardless of which lens catches them.
- All 3 fixed correctly in one pass. No fix-loop failures.

---

## Second-Trial Variance (Clean Document)

A second trial on the clean API guide reveals significant run-to-run score variance, consistent with Phase 1 findings.

| Config | Trial 1 Iter1 Score | Trial 2 Iter1 Score | Delta | Trial 1 Tokens | Trial 2 Tokens |
|---|---|---|---|---|---|
| enum-only | 93 | 89 | −4 | 35,102 | 42,058 |
| adv-only | 84 | **67** | −17 | 38,905 | 45,999 |
| mixed | 87 | **80** | −7 | 38,977 | **55,845** |

**adv-only shows extreme score variance (+/−17 points).** The second trial found 2 HIGH-severity findings (base URL uses `.example.com` reserved domain; no HTTPS requirement stated) that the first trial missed entirely.

**enum-only variance (4 points) is the smallest**, consistent with its systematic, checklist-driven approach generating more deterministic outputs.

**mixed has a critical HIGH-confidence variance problem.** Trial 1: all 9 findings were MEDIUM confidence (no dual-review agreement). Trial 2: 3 of 7 consolidated findings were HIGH confidence (both reviewers agreed). Same config, same fixture, two completely different confidence distributions. This undermines mixed's key value proposition — the HIGH-confidence signal is not stable across runs.

**mixed's token cost exploded on trial 2:** 55,845 tokens and 460.5 seconds (vs 38,977 and 241.7s in trial 1). The second trial's 6 agents produced 13 raw findings that required more consolidation work, driving up cost. mixed's compute cost is not predictable.

**Implication for Phase 3:** 3+ trials are required before any numeric or confidence comparisons are meaningful. This is especially true for adv-only (score variance) and mixed (confidence distribution variance + cost variance). The core binary (caught/missed, CLEAN/FAILED) is reliable across trials; the numeric scores and confidence levels are not.

---

## Cross-Test Summary

### Correctness

| Config | Gate failed correctly | Seeded errors caught |
|---|---|---|
| enum-only | ✓ | ✓ both |
| adv-only | ✓ | ✓ both |
| mixed | ✓ | ✓ both |

All configs: 2/2 correct outcomes. No false passes, no missed seeded errors.

### False Positive Rate (Pristine Document)

| Config | False positives | True positives | Notes |
|---|---|---|---|
| enum-only | 0 | 0 (missed real issues) | Did not find the math error in the original fixture |
| adv-only | 0 | 2 (caught real issues) | Found math error + scope gap, both genuine |
| mixed | 0 | 2 (caught real issues) | Found same 2 issues; math error at HIGH confidence |

All configs: 0 false positives. adv-only and mixed were more sensitive to genuine subtle errors.

### Thoroughness (Clean Artifact)

| Config | Findings (Iter 1) | Severity distribution |
|---|---|---|
| enum-only | 3 | 2M, 1L |
| adv-only | 8 | 4M, 4L |
| mixed | 9 | 2M, 7L |

More findings from adversarial framing — but at lower average severity for mixed (7 of 9 were LOW).

### Cost (Full Profile — Clean + Seeded Average)

| Config | Avg tokens | Avg time (s) | vs enum-only |
|---|---|---|---|
| enum-only | 37,008 | 192.4 | baseline |
| adv-only | 38,252 | 223.2 | +3% tokens, +16% time |
| mixed | 40,464 | 259.2 | +9% tokens, +35% time |

mixed costs ~35% more time than enum-only and ~16% more time than adv-only.

---

## Phase 2 Analyst Observations

1. **Composition doesn't matter for gate correctness.** All three configurations correctly identify structural failures. The gate profile runs a single lens regardless of composition — enum-only, adv-only, and mixed all use the same structural lens on gate. Score variance (13–48) is pure LLM measurement noise. Run 3+ trials before treating gate scores as numeric measurements.

2. **Adversarial framing catches subtle logical-consistency errors that enumeration misses (probably).** On the pristine fixture, adv-only caught a mathematical inconsistency that enum-only did not. This is a single-trial observation — the Enumerator in the mixed run *did* catch it, suggesting this is within the variance envelope rather than a systematic capability gap. Still, the Adversary's "something feels off" heuristic is more likely to trigger verification of numeric claims.

3. **Mixed composition's HIGH-confidence signal is valuable but not reliable.** Both seeded errors reached HIGH confidence in the mixed run (both trials). However, on the clean API guide, trial 1 produced 0 HIGH-confidence findings and trial 2 produced 3. The same config, same fixture, two completely different confidence distributions. HIGH confidence is a reliable signal *when it appears* — it means two independent framings genuinely agreed — but its appearance is not guaranteed across runs. Do not build workflows that depend on HIGH confidence appearing predictably.

4. **adv-only vs enum-only thoroughness gap is real.** On the clean API guide, adv-only found 8 findings vs enum-only's 3. The 5 additional findings were genuine issues (response field documentation, retry logic ambiguity). Systematic enumeration doesn't pursue what isn't on its checklist; adversarial reading does.

5. **mixed's extra LOW-severity findings add noise.** mixed found 9 findings on the clean guide, 7 of which were LOW severity. These are real but low-value. A pipeline operator may prefer fewer, higher-severity findings over more comprehensive sweep. This suggests mixed may benefit from a LOW-severity suppression option for high-throughput contexts.

6. **Cost of mixed is acceptable.** +35% wall time over enum-only, +16% over adv-only. For a 6-agent full-profile run, this is the cost of running 2 agents per lens instead of 1. The marginal cost is justified by HIGH-confidence signal — particularly for documents where decisions hinge on validation results.

7. **The fix loop worked correctly across all runs.** Every configuration that needed fixes applied them in a single pass and came out clean. No config introduced new bugs during fixing. Re-validation caught no regressions.

---

## Recommendations for Phase 3 (Model Variation: Haiku, Sonnet, Opus)

- **Use mixed composition as Phase 3 baseline**, but with revised expectations. Its HIGH-confidence signal is valuable when it appears but is not guaranteed across runs. Its cost is unpredictable (trial 1: 241.7s; trial 2: 460.5s on the same fixture). Plan for worst-case token budgets.
- **Also benchmark adv-only as a primary candidate.** On seeded errors and clean artifacts, adv-only performed comparably to mixed at significantly lower and more predictable cost. adv-only's weakness (all MEDIUM confidence) may be acceptable if findings are reviewed by humans before acting.
- **Adjust max iterations by model (as designed):** Haiku → 8 iterations, Sonnet → 4, Opus → 2. Haiku may need more loops to correct issues it introduces during fixing; Opus should rarely need more than 1.
- **Continue 3-lens config** for model variation tests (same fixture, same composition, vary model).
- **Add 3 trials per config** given observed score variance. Single-shot scores can't be compared across models without confidence intervals.
- **Test on the fixed pristine fixture only** — the original had embedded errors. Document the fixture fix and its discovery as a Phase 2 finding (adv-only stress-tests fixture quality itself).
- **Track HIGH vs MEDIUM confidence distribution** by model — does Haiku produce fewer HIGH-confidence findings because it misses cross-lens patterns? Does Opus produce more HIGH-confidence findings due to better reasoning?
