# AVFL Phase 3 Benchmark — Model Variation
**Date:** 2026-03-20 | **Fixture:** pipeline-arch-multi-iter (2C+2H+3M+2L seeded) | **Skill:** avfl-3lens (mixed composition) | **Skepticism:** 3 (flat)

## Configuration Summary

| Config | Model | Max Iter | Agents/Run | Variable Isolated |
|---|---|---|---|---|
| **haiku** | claude-haiku-4-5 | 8 | 6 (1 Enum + 1 Adv × 3 lenses) | Lowest-cost model tier |
| **sonnet** | claude-sonnet-4-6 | 4 | 6 (1 Enum + 1 Adv × 3 lenses) | Mid-tier model |
| **opus** | claude-opus-4-6 | 2 | 6 (1 Enum + 1 Adv × 3 lenses) | Highest-capability model tier |

Same fixture, same skill, same skepticism=3 flat, same stage=final across all 3 runs. Max iterations varied by model tier per Phase 3 design (cost-appropriate budget).

---

## Results

| Config | Iter 1 Score | Iter 1 Findings | Iter 2 Score | Iter 2 Findings | Final | Seeded | Additional | Tokens | Time (s) |
|---|---|---|---|---|---|---|---|---|---|
| haiku | 28 | 10 (3C,2H,3M,2L) | 100 | 0 | CLEAN | 9/9 | 1 | 52,601 | 239.1 |
| sonnet | 47 | 10 (1C,3H,4M,2L) | 100 | 0 | CLEAN | 9/9 | 1 | 51,127 | 332.7 |
| opus | 50 | 9 (1C,3H,3M,2L) | 97 | 1 (0C,0H,1M,0L) | CLEAN | 9/9 | 1 | 48,283 | 254.8 |

---

## Key Finding 1: All models achieve equivalent recall and convergence

All three models found all 9 seeded issues in iteration 1 (100% detection rate) and reached CLEAN in exactly 2 iterations. The primary quality metric — does the pipeline reliably find real issues? — is model-invariant on this fixture. There is no detectable quality advantage to Opus or Sonnet over Haiku for seeded issue detection.

---

## Key Finding 2: Haiku inflates severity more aggressively than Sonnet or Opus

Haiku assigned 3 criticals (iter 1 score: 28/100). Sonnet and Opus assigned 1 critical each (scores: 47 and 50). The C1 seeded issue (parallel/sequential contradiction) was called critical by all three. But Haiku also called C2 (dangling Section 6 reference) a critical — Sonnet and Opus called it high. This severity inflation produced a significantly lower initial score without reflecting a difference in actual finding quality.

This is consistent with Phase 2.6's observation that skepticism=3 with stage=final creates a severity-escalation effect. Haiku appears to amplify this effect relative to larger models, possibly because it applies the "default assumption: something might be wrong" heuristic more bluntly.

---

## Key Finding 3: Opus caught a fixer-introduced regression; Haiku and Sonnet did not

In iteration 2, Opus found that the Security Considerations section added by the fixer (to resolve C2) was placeholder-only — acceptable as a stub for a draft but incomplete for a final artifact. Haiku and Sonnet accepted the fixed document with 0 iter-2 findings (100/100). Opus exited at 97/100.

This replicates Phase 2.6's finding that re-validation of fixed content is where model comprehension quality differentiates. Opus's holistic reading caught that the fixer's added section didn't fully resolve the underlying problem — it patched the structural gap (Section 6 now exists) but left the content incomplete. Haiku and Sonnet did not notice.

All three still exited CLEAN (≥95), so the practical outcome was the same. But the nature of "clean" differed: Opus's 97/100 is a more honest score of the corrected document's actual state.

---

## Key Finding 4: Token usage is surprisingly similar across all models

| Config | Tokens | vs. cheapest |
|---|---|---|
| opus | 48,283 | — (cheapest by tokens) |
| sonnet | 51,127 | +6% |
| haiku | 52,601 | +9% |

Opus used the fewest tokens of the three, with Haiku using the most. This is counterintuitive — larger models are typically more verbose per turn. The likely explanation: Opus produces more structured, evidence-dense output per finding (fewer tokens to reach the same quality conclusions), while Haiku generates more output volume per agent turn to compensate for lower per-token capability. Token count is not a reliable proxy for cost across model tiers — Opus tokens are priced significantly higher than Haiku tokens, so the dollar cost ordering is still Opus >> Sonnet >> Haiku despite Opus using fewer tokens.

---

## Key Finding 5: Sonnet is the slowest of the three

| Config | Time (s) |
|---|---|
| haiku | 239.1 |
| opus | 254.8 |
| sonnet | 332.7 |

Sonnet was 39% slower than Haiku and 31% slower than Opus. This is unexpected — Sonnet is the mid-tier model. Possible explanations: generation speed, load balancing, or infrastructure variance at time of run. Single-trial caveat applies — this time difference may not be stable across runs.

---

## Cost

Dollar cost comparison requires applying per-token pricing. Token counts alone show Opus using fewest tokens, but at substantially higher per-token rates. Approximate relative cost ordering remains Opus >> Sonnet >> Haiku regardless of the token-count inversion.

---

## Phase 3 Analyst Observations

1. **Haiku is viable for AVFL.** 100% seeded detection, CLEAN in 2 iterations, fastest wall time. For high-volume or cost-sensitive use cases, Haiku delivers equivalent functional outcomes to larger models on this fixture.

2. **Opus adds marginal quality at higher cost.** The one differentiator — catching the fixer-introduced placeholder section — is real but small. It didn't change the CLEAN outcome. For artifacts where fixer regression detection matters (complex fixes, multi-section additions), Opus's re-validation comprehension may be worth the cost premium.

3. **Severity calibration varies by model.** Haiku's aggressive severity inflation (28/100 vs. 47-50/100) overstates urgency on legitimate findings. Users consuming raw findings scores should be aware that Haiku at skepticism=3/stage=final will produce lower scores than larger models on the same document — not because it found more or worse issues, but because it assigns higher severities.

4. **The additional findings differ by model.** Each model found a different "extra" finding: Haiku caught the latency/polling logical contradiction (correctness), Sonnet caught the unattributed benchmark claim (traceability), Opus caught the fixer-introduced placeholder (structural completeness on new content). All three are legitimate. This suggests that at equivalent recall rates, models differ in *which* non-obvious issues they surface, not whether they surface them.

5. **Single-trial caveat.** All results are single-trial. The Sonnet timing anomaly in particular requires replication before drawing conclusions.

---

## Recommendations

1. **Use Haiku as the default model for AVFL in cost-sensitive contexts.** Functional outcomes are equivalent to Sonnet and Opus for seeded detection and convergence. Accept the severity inflation as a known artifact — the findings themselves are correct.

2. **Use Opus when fixer regression detection matters.** If the fix pass involves adding substantial new content (not just corrections), Opus's iter-2 comprehension is more likely to catch semantic or completeness issues in the new material.

3. **Apply severity normalization at skepticism=3 with Haiku.** Since Haiku inflates severity more aggressively, downstream consumers should treat Haiku scores as conservative (worst-case) assessments, especially for final-stage artifacts.

4. **Investigate the Sonnet timing anomaly in Phase 4.** If variance is low across runs, there may be an infrastructure or architectural reason Sonnet is slower than both Haiku and Opus — worth understanding before recommending it for latency-sensitive workflows.
