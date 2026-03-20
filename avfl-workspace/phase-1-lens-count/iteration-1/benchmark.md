# AVFL Phase 1 Benchmark — Lens Count
**Date:** 2026-03-20 | **Model:** claude-sonnet-4-6 | **Composition:** Mixed (Enumerator + Adversary)

## Configuration Summary

| Config | Active Lenses | Agents (full profile) |
|---|---|---|
| **2-lens** | Structural Integrity, Factual Accuracy | 4 |
| **3-lens** | + Coherence & Craft | 6 |
| **4-lens** | + Domain Fitness | 8 |

---

## Test 1: Gate — Badly-Formed Document

All configs run gate profile (1 agent, structural lens only, no fix loop).

| Config | Status | Score | Findings | Tokens | Time (s) |
|---|---|---|---|---|---|
| 2-lens | GATE_FAILED | 44 | 5 (3C, 1H, 1M) | 28,565 | 77.9 |
| 3-lens | GATE_FAILED | 51 | 5 (2C, 2H, 1M) | 28,793 | 73.5 |
| 4-lens | GATE_FAILED | 33 | 7 (3C, 2H, 2M) | 31,456 | 88.6 |

**Verdict:** All correctly GATE_FAILED. No false passes. Gate profile behaves consistently across lens variants (as expected — gate always runs structural only).

**Key observation:** Score variance of 33–51 on an *identical* gate task (same lens, same document) is pure LLM measurement noise. This is the most important finding from Test 1 — single-shot scores are not reliable. Multi-trial averaging is required before drawing conclusions from numeric scores.

---

## Test 2: Full — Clean Artifact (False Positive Rate)

All configs run full profile (2 agents per active lens, max 4 iterations).

| Config | Status | Final Score | Iter 1 Score | Findings | Tokens | Time (s) |
|---|---|---|---|---|---|---|
| 2-lens | CLEAN | 100 | 89 | 5 (0C, 0H, 3M, 2L) | 37,838 | 215.7 |
| 3-lens | CLEAN | 97 | 83 | 7 (0C, 0H, 5M, 2L) | 42,886 | 325.7 |
| 4-lens | CLEAN | 99 | 78 | 12 (0C, 0H, 5M, 7L) | 43,951 | 290.5 |

**Verdict:** All reached CLEAN status. No false positives identified — all findings were legitimate issues the document actually had.

**Key observations:**
- The "clean" fixture had real issues. This test measured *thoroughness*, not false positive rate. A truly pristine fixture is needed for a proper false-positive test.
- More lenses = more findings: 5 → 7 → 12. The additional findings from coherence and domain fitness lenses are real but increasingly lower severity.
- 4-lens fixer introduced a new bug (undocumented webhook reference) while fixing another issue — caught on iteration 2. Demonstrates why fix-loop re-validation is essential.
- Time does not scale linearly with agent count: 3-lens (325.7s) was slower than 4-lens (290.5s), likely due to consolidation complexity and subagent scheduling variance.
- False positives removed: 0 (2-lens), 0 (3-lens), 1 duplicate (4-lens).

---

## Test 3: Full — Seeded Errors (True Positive Rate)

Two seeded errors: Error 1 (factual — wrong Meta-Judge statistic, accuracy lens target), Error 2 (consistency — contradictory threshold 90 vs 95, coherence lens target).

| Config | Status | Final Score | Errors caught | Findings | Tokens | Time (s) |
|---|---|---|---|---|---|---|
| 2-lens | CLEAN | 100 | ✓ both | 5 (0C, 2H, 2M, 1L) | 38,194 | 204.1 |
| 3-lens | CLEAN | 100 | ✓ both | 6 (0C, 3H, 2M, 1L) | 39,118 | 222.6 |
| 4-lens | CLEAN | 100 | ✓ both | 5 (0C, 2H, 2M, 1L) | 38,610 | 187.2 |

**Verdict:** All caught both seeded errors at HIGH confidence (both Enumerator and Adversary found each one). All reached CLEAN in 2 iterations.

**Key observations:**
- Hypothesis falsified: 2-lens was expected to miss Error 2 (consistency/coherence). Instead the accuracy lens's `logical_soundness` dimension caught the threshold contradiction as a logic failure. Coherence is not the only path to consistency errors.
- 3-lens caught one additional finding 2-lens missed: the *downstream wrong recommendation* ("at least 3 reviewers") flowing from the factual error. Coherence lens caught the implication, accuracy caught the source. This is qualitative added value.
- Finding counts are non-monotonic (5, 6, 5) — 4-lens found fewer than 3-lens on this test. Below the single-trial noise floor.
- Token costs nearly identical across all three (~38–39k). The marginal cost of additional lenses on this document type is small.

---

## Cross-Test Summary

### Correctness (did it reach the right outcome?)
| Config | Gate correct | Seeded errors caught | Clean reached CLEAN |
|---|---|---|---|
| 2-lens | ✓ | ✓ both | ✓ |
| 3-lens | ✓ | ✓ both | ✓ |
| 4-lens | ✓ | ✓ both | ✓ |

All configs: 3/3 correct outcomes.

### Cost (full-profile runs only)
| Config | Avg tokens | Avg time (s) |
|---|---|---|
| 2-lens | 38,016 | 209.9 |
| 3-lens | 41,002 | 274.2 |
| 4-lens | 41,281 | 238.9 |

2-lens is cheapest by ~8%. 3-lens and 4-lens are similar in cost.

### Thoroughness (findings on clean artifact)
2-lens: 5 findings | 3-lens: 7 findings | 4-lens: 12 findings

More lenses surface more issues, but severity drops — the additional 7 findings in 4-lens vs 2-lens are overwhelmingly low severity.

---

## Phase 1 Analyst Observations

1. **LLM variance dominates single-shot scores.** Gate scores ranged 33–51 on identical inputs. Do not read numeric scores as precise measurements — run 3+ trials and report mean ± stddev before Phase 2 conclusions.

2. **Logical_soundness is a coherence detector.** The accuracy lens's logical_soundness dimension catches internal contradictions, not just factual errors. Coherence lens adds coverage breadth (tonal, temporal, craft) but not exclusive ownership of consistency detection.

3. **2-lens is surprisingly capable.** For the tested error types, 2-lens matched 3-lens and 4-lens on correctness at lower cost and time. The marginal value of additional lenses comes from catching secondary/downstream implications (3-lens) and lower-severity craft/domain issues (4-lens).

4. **Fix loop introduces new errors.** 4-lens fixer introduced an undocumented webhook reference that wasn't in the original. The re-validation caught it at low severity (score 99, passed). This is a known risk: fixers are LLMs operating under incomplete context. The fix loop's mandatory re-validation is correctly designed.

5. **True false-positive measurement needs a pristine fixture.** The current "clean" fixture had 5–12 real issues. Replace with a document drafted specifically to be complete, and verify it manually before using as a false-positive benchmark.

---

## Recommendations for Phase 2 (Composition: Enumerator-only vs Adversary-only vs Mixed)

- **Lock lens count at 3** for Phase 2. It offers a middle ground — catches downstream implications that 2-lens misses, without the noise floor of 12 low-severity findings that 4-lens produces.
- **Add a genuine pristine fixture** alongside the existing seeded and badly-formed ones.
- **Run 3 trials per config** given the variance observed in Phase 1. Single-shot scores are not reliable.
- **Track findings by severity separately.** Aggregate finding counts obscure the critical distinction between "caught a critical factual error" and "noticed the API guide had no curl examples."
