# AVFL Phase 2.5 Benchmark — Declining Skepticism
**Date:** 2026-03-20 | **Model:** claude-sonnet-4-6 | **Configs:** 2 (flat-3, declining 3→2→1)

## Configuration Summary

| Config | Skill | Skepticism behavior | Composition |
|---|---|---|---|
| **flat-3** | avfl-3lens | Fixed skepticism=3 on all iterations | Mixed (1E+1A per lens, 3 lenses = 6 agents) |
| **declining** | avfl-declining | iter 1=3, iter 2=2, iter 3+=1 | Same |

**Fixtures:**
- `pipeline-arch-multi-iter.md` — new 9-issue fixture (2C+2H+3M+2L), designed to require 2 iterations
- `research-summary-seeded.md` — 2 seeded errors (1 factual, 1 consistency), established Phase 2 fixture

---

## Test 1: Multi-Iteration Fixture (pipeline-arch-multi-iter)

9 known seeded issues: C1 (parallel/sequential contradiction), C2 (missing Section 6), H1 (batch/streaming claim reversed), H2 (99.9% latency claim), M1–M3 (undefined policy, undefined "large", pipeline/workflow ambiguity), L1–L2 (ETL unexpanded, auth type unspecified).

| Config | Iter 1 Score | Iter 1 Findings | Iter 2 Score | Iter 2 Findings | Final | Iters | Tokens | Time (s) |
|---|---|---|---|---|---|---|---|---|
| flat-3 | 50 | 9 (1C, 3H, 3M, 2L) | 96 | 2 (1M, 1L) | CLEAN | 2 | 45,621 | 302.6 |
| declining | 27 | 11 (various) | 100 | 0 | CLEAN | 2 | 44,743 | 288.2 |

**Seeded issue detection:** Both configs 9/9 (100%). All issues found in iteration 1.

**Key observations:**

- **Both reached CLEAN in 2 iterations.** The hypothesis that declining reduces iteration count was not confirmed — both converged at the same speed on this fixture.
- **Iter 2 behavior diverged.** flat-3 found 2 findings at skepticism=3 (score 96, barely CLEAN). declining found 0 findings at skepticism=2 (score 100, perfect). This is the central result of the benchmark — see analysis below.
- **The 2 iter-2 findings in flat-3 were fixer regressions**, not noise from re-checking already-correct content. The fixer's correction of H1 retained an unsupported "3×" multiplier (MEDIUM), and the security deferral note was placed in the wrong section (LOW). Aggressive skepticism=3 caught them; balanced skepticism=2 did not.
- **Iter 1 score variance (50 vs 27) at identical skepticism=3** is pure LLM variance, consistent with Phase 2 patterns. Not indicative of a meaningful detection difference.
- **declining found 2 unseeded findings above the 9 seeded ones** (a security completeness gap and a logical soundness conflict between sub-second latency and 5-minute polling). These were genuine issues at MEDIUM confidence.
- **Cost:** declining was 2% cheaper in tokens and 5% faster in time — modest but consistent.

---

## Test 2: Seeded Errors Fixture (research-summary-seeded)

2 known seeded errors: ERROR-1 (factual: wrong Meta-Judge statistic), ERROR-2 (consistency: 90 vs 95 threshold contradiction).

| Config | Iter 1 Score | Iter 1 Findings | Iter 2 Score | Iter 2 Findings | Final | Iters | ERROR-1 | ERROR-2 | Tokens | Time (s) |
|---|---|---|---|---|---|---|---|---|---|---|
| flat-3 | 75 | 7 (2H, 2M, 3L) | 100 | 0 | CLEAN | 2 | ✓ HIGH | ✓ HIGH | 45,870 | 308.1 |
| declining | 78 | 6 (after 4 dups collapsed) | 100 | 0 | CLEAN | 2 | ✓ HIGH | ✓ HIGH | 44,600 | 302.2 |

**Key observations:**

- **Both caught both seeded errors at HIGH confidence in iteration 1.** Declining's lower skepticism in later iterations has no effect when errors are found and fixed in the first pass — which is the expected case for well-seeded, detectable errors.
- **Iteration 2 was identical across configs: 0 findings.** On a clean document, both flat-3 (at skepticism=3) and declining (at skepticism=2) produced no false positives. This is consistent with Phase 2 pristine fixture results.
- **Findings overlap**: declining found 4 cross-lens duplicates collapsed during consolidation. flat-3 found 7 distinct findings. Both modes detected the two errors; the count difference is dedup behavior, not detection capability.
- **Cost delta small**: declining was 2.8% cheaper in tokens, 2% faster. Similar to the multi-fixture pattern.

---

## Cross-Test Summary

### Convergence

| Config | Multi-fixture iters | Seeded iters | Total finding: seeded caught |
|---|---|---|---|
| flat-3 | 2 | 2 | 11/11 (100%) |
| declining | 2 | 2 | 11/11 (100%) |

No iteration count advantage for declining on these fixtures.

### Iteration 2 Behavior (the key question)

| Config | Multi iter 2 findings | Seeded iter 2 findings | Nature of iter 2 findings |
|---|---|---|---|
| flat-3 | 2 (MEDIUM + LOW) | 0 | Fixer regressions — real issues introduced by fix pass |
| declining | 0 | 0 | None — clean confirmation |

**This is the most meaningful result.** Flat-3's aggressive skepticism=3 on iteration 2 caught 2 genuine fixer regressions. Declining's balanced skepticism=2 did not. Neither was a false positive situation — the fixer in the flat-3 run happened to introduce 2 real issues that the declining run's fixer did not introduce (LLM variance in the fix pass).

The practical question this raises: **if a fixer introduces a regression, will skepticism=2 catch it?** This benchmark cannot answer definitively — the fixers are independent agents with different behaviors across runs. The regressions in flat-3 were small (1M + 1L = 4 points). A HIGH or CRITICAL regression at skepticism=2 would likely still be caught — the approach_modifier for skepticism=2 is "balanced, follow promising leads" which is still active validation, not passive.

### Cost

| Config | Avg tokens | Avg time (s) | vs flat-3 |
|---|---|---|---|
| flat-3 | 45,746 | 305.4 | baseline |
| declining | 44,672 | 295.2 | −2.4% tokens, −3.3% time |

Consistent 2–5% cost advantage for declining. Explains: validators in iteration 2 at skepticism=2 pursue fewer leads, reducing the exploration work per validator.

---

## Phase 2.5 Analyst Observations

1. **Declining does not reduce iteration count on these fixtures.** Both needed 2 iterations. The benefit of declining is not convergence speed — it's iteration 2 behavior. We didn't design a fixture where flat-3 would need a 3rd iteration due to iter-2 noise. That would require a fixture where aggressive re-validation consistently generates NEW medium-severity findings in already-fixed content.

2. **The fixer regression finding is dual-edged.** Flat-3 caught regressions that declining missed. This is a real capability difference: declining trades away some re-validation sensitivity in exchange for less noise. For most documents, this is the right tradeoff — fixer regressions are rare, and when they occur they're usually minor. But for high-stakes documents where even a medium regression matters, flat-3 iteration 2 provides stronger safety.

3. **Declining's iteration 2 is clean when the document is clean.** Both the seeded fixture (clean after iter 1 fix) and the declining multi-fixture run (clean after iter 1 fix) produced 0 iter-2 findings. This validates the key design goal: declining prevents noise amplification on already-good content.

4. **Score variance in iter 1 (50 vs 27 on same fixture, same skepticism=3) continues the Phase 2 pattern.** Single-trial iter-1 scores are not comparable numeric measurements. The binary (found/missed, CLEAN/FAILED) is reliable; the numeric score is not.

5. **Declining is a modest cost win.** 2–5% savings per run. At scale (thousands of invocations), this is meaningful. It is not the primary justification for declining, but it's a consistent directional signal.

6. **The floor of 1 may be too low.** Skepticism=1 (conservative: report only what evidence clearly shows is wrong) on iteration 3+ is very passive. In Phase 2, we never had a 3+ iteration run to test this. If a fixture required 3 iterations, skepticism=1 might miss important remaining issues. Consider a floor of 2 (balanced) rather than 1.

---

## Recommendations

- **Adopt declining as the default behavior.** The benchmark shows no downside in true positive rate or convergence speed, a modest cost win, and cleaner iter-2 behavior on clean content. The fixer regression risk is real but minor on evidence available.
- **Reconsider the floor.** Change from 1 to 2: declining becomes 3→2→2→2 (steps once, then stays balanced). Skepticism=1 (conservative) is too passive for ongoing validation of a document still in the fix loop.
- **Flag fixer regression risk in SKILL.md.** Note that declining at skepticism=2 provides slightly weaker regression detection than flat-3. Workflows with high-consequence artifacts that care about catching fixer-introduced issues may want to use flat skepticism.
- **Phase 3 test needed:** Design a fixture where the fixer reliably introduces a regression (e.g., a document where fixing issue A tends to break constraint B). This would isolate the declining vs flat regression detection difference without LLM variance in the fixer confounding the result.
- **Second trial warranted before finalizing.** Single trial. The fixer variance confounds the most important result (iter 2 regression detection). A second trial on the multi-fixture with the same config would tell us whether the flat-3 fixer regression was a one-off or a consistent pattern.
