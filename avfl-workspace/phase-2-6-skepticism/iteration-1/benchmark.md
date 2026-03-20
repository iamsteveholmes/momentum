# AVFL Phase 2.6 Benchmark — Skepticism × Framing
**Date:** 2026-03-20 | **Model:** claude-sonnet-4-6 | **Fixture:** pipeline-arch-multi-iter (2C+2H+3M+2L seeded)

## Configuration Summary

| Config | Framing | Skepticism | Agents | Variable isolated |
|---|---|---|---|---|
| **adv-skep1** | Adversary only | 1 — Conservative | 3 | Adversary at minimum intensity |
| **enum-skep1** | Enumerator only | 1 — Conservative | 3 | Enumerator at minimum intensity |
| **enum-skep3** | Enumerator only | 3 — Aggressive | 3 | Enumerator at maximum intensity |
| **adv-skep3** | Adversary only | 3 — Aggressive | 3 | Adversary at maximum intensity |

Same fixture, same profile (full), same stage (final) across all 4 runs.

---

## Results

| Config | Iter 1 Score | Iter 1 Findings | Iter 2 Score | Iter 2 Findings | Final | Seeded | Additional | Tokens | Time (s) |
|---|---|---|---|---|---|---|---|---|---|
| adv-skep1 | 48 | 9 (1C,3H,4M,1L) | 100 | 0 | CLEAN | 9/9 | 0 | 40,817 | 247.0 |
| enum-skep1 | 48 | 9 (1C,3H,4M,1L) | 100 | 0 | CLEAN | 9/9 | 0 | 41,503 | 264.2 |
| enum-skep3 | 11 | 13 (2C,5H,4M,2L) | 100 | 0 | CLEAN | 9/9 | 4 | 48,099 | 356.6 |
| adv-skep3 | 31 | 9 (2C,4H,2M,1L) | 95 | 3 (1M,2L) | CLEAN | 9/9 | 3 | 49,640 | 411.4 |

---

## Key Finding 1: At skepticism=1, framing is irrelevant

adv-skep1 and enum-skep1 produced **identical results**: 9 findings, score 48/100, 9/9 seeded issues, 0 additional findings, CLEAN in 2 iterations. The conservative filter ("report only what evidence clearly shows is wrong; skip borderline findings") suppresses the behavioral difference between systematic enumeration and holistic pattern-reading. When both framings are constrained to act only on clear evidence, they converge on the same output.

Both agents explicitly noted skipping candidate findings — the Adversary held back uncited performance figures ("50,000 events/second", "sub-second latency") and the Enumerator skipped the same because neither had evidence the figures were wrong. Same decision, different reasoning paths.

**Implication:** Dual-review at skepticism=1 produces no cross-check value. The HIGH confidence mechanism (both find it → real) only works when framings have meaningfully different detection paths. At skepticism=1 both detection paths are essentially the same: "show me the evidence first."

---

## Key Finding 2: Skepticism=3 moves both framings significantly — but through different mechanisms

Both framings find more at skepticism=3 than at skepticism=1. The size of the delta is comparable (Enumerator: +4, Adversary: +3). But **when and how** they find it differs:

**Enumerator at skepticism=3:** Additional findings arrive in **iteration 1**, via the reexamine_rule mandating a second structured pass. The reexamine directly caught ACCURACY-004 (sub-second latency contradicts 5-minute polling interval) — a finding the conservative Enumerator explicitly did not flag. The reexamine pass is a second enumeration run; it extends the checklist sweep rather than changing its nature.

**Adversary at skepticism=3:** 9 findings in iteration 1 (same count as skepticism=1), then 3 additional findings in **iteration 2**, including a fix-introduced regression (Section 6 reference not fully updated in Stage 4) and a semantic conflict in the new content (the fixer's security section routed authentication failures to the dead-letter queue, conflating security events with data pipeline events). The Adversary's additional output comes from holistic review of fixed/new content, not from a second pass over the original.

The hypothesis that "skepticism moves the needle more for the Adversary than the Enumerator" is **not supported**. The delta is similar in magnitude. What differs is the mechanism and timing.

---

## Key Finding 3: The types of additional findings differ by framing

Additional findings at skepticism=3 that were NOT in the seeded list:

**Enumerator extras (iter 1):**
- Security section entirely absent (structural completeness)
- 5-minute polling contradicts sub-second latency (logical soundness — caught on reexamine pass)
- Uncited "Benchmarks show..." claim (traceability)
- Minor redundancy between Operational Notes and Stage 4 (conciseness)

**Adversary extras (iter 2):**
- Fix-introduced regression: Stage 4 still referenced "Section 6" after Section 5 was added (structural — caught reviewing fixed content)
- Corrected benchmark claim still uses "Benchmarks show" with no citation (traceability)
- New Security section conflates security audit events with data quality events — authentication failures routed to dead-letter queue (logical soundness — semantic issue in new content)

The Enumerator's extras are structural and completeness-driven — they fit naturally on a checklist. The Adversary's extras are contextual and relational — they involve reading the fixed content against what the document now claims, noticing that the fix introduced a new conceptual problem. The latency/polling contradiction appeared in both (the Enumerator caught it on reexamine iter 1; the Adversary did not surface it until after fixes were applied).

---

## Key Finding 4: Adversary skepticism=3 catches fixer errors the Enumerator misses

The Adversary's iter-2 finding of the semantic conflict in the new Security section (authentication failures routed to dead-letter queue) is not something an enumerating checklist would produce — it requires reading the new section holistically and noticing that a data-pipeline concept was incorrectly applied to a security context. The Enumerator at skepticism=3 did not catch this: it produced 0 iter-2 findings, meaning it accepted the fixed document as correct.

This is the clearest signal of a framing-based capability difference in this benchmark: **the Adversary's holistic review of fixed content catches semantic errors that structural enumeration accepts.** This matters most for the iteration 2+ re-validation pass — where the content has changed and new content requires fresh comprehension rather than list-checking.

---

## Key Finding 5: Adversary skepticism=3 ended at 95/100, not 100

adv-skep3 exited CLEAN at 95/100 (the minimum threshold), while enum-skep3 exited at 100/100. The Adversary's iter-2 fixed 3 issues but the final document scored exactly at threshold. This suggests either a residual minor issue or that the aggressive re-examination at skepticism=3 on the already-fixed content surfaced one more borderline finding that was technically inside the passing threshold when combined with the fixed severity profile. The 95 vs 100 difference is within scoring variance — both are CLEAN.

---

## Cost

| Config | Tokens | Time (s) | vs skep1 baseline |
|---|---|---|---|
| adv-skep1 | 40,817 | 247.0 | — |
| enum-skep1 | 41,503 | 264.2 | — |
| enum-skep3 | 48,099 | 356.6 | +16% tokens, +35% time vs enum-skep1 |
| adv-skep3 | 49,640 | 411.4 | +22% tokens, +56% time vs adv-skep1 |

Skepticism=3 is materially more expensive than skepticism=1 for both framings. The Adversary at skepticism=3 is the most expensive configuration tested so far (411s, 2 full iteration loops with 3 agents each).

---

## Phase 2.6 Analyst Observations

1. **The original hypothesis was wrong.** Skepticism was not primarily an Adversary-intensity control — it has comparable magnitude effect on both framings. The design assumption that "the Enumerator at skepticism=3 just re-checks its list" was partially wrong: the reexamine_rule genuinely extends detection by mandating a second pass, which caught the latency/polling contradiction that wasn't on the first-pass checklist.

2. **The value of dual-review is skepticism-dependent.** At skepticism=1, running both framings produces no benefit over running one — they find identical issues. Dual-review's HIGH confidence signal and finding diversity only emerge when framings have differentiated detection paths, which requires skepticism ≥ 2. This has implications for the declining schedule: declining to skepticism=1 eliminates the value of having mixed composition entirely.

3. **The Adversary's unique value is in reviewing fixed content.** At skepticism=3, the Adversary's distinctive contribution was in iteration 2, not iteration 1. It found a semantic error in the fixer's newly added content that the Enumerator accepted. This suggests the Adversary should be particularly valued in re-validation passes — it's the better reviewer of *changed* content, not just of original content.

4. **Severity inflation is skepticism-driven.** Both framings at skepticism=3 assigned higher severities than at skepticism=1: M1 "standard retry policy" was upgraded from medium to high; M2 "large files" was sometimes upgraded. The approach_modifier ("default assumption: something might be wrong") combined with stage=final's completeness instruction creates a severity-escalation effect. This may overstate urgency on legitimate documentation gaps.

5. **Declining to floor=2 is now better-motivated.** At skepticism=1, framings are indistinguishable. A declining schedule that bottoms at 1 eliminates dual-review's value on the final iterations. Floor=2 preserves meaningful framing differentiation throughout the loop.

6. **Single-trial caveat.** All conclusions are single-trial. Variance is high enough (as shown in Phase 2) that the adv-skep3 iter-1 count of 9 vs enum-skep3's 13 could swap on a second run. The directional patterns (mechanisms differ, framing convergence at skep=1) are likely robust; the exact counts are not.

---

## Recommendations

1. **Revise the floor of the declining schedule from 1 to 2.** At skepticism=1 both framings are interchangeable — there's no benefit to dual-review and the framing parameter is inert. Floor=2 keeps dual-review differentiated across all iterations.

2. **Document that skepticism=3 is needed for the Adversary's cross-iteration holistic review to emerge.** The Adversary's distinctive capability (catching semantic errors in fixed content) only appeared at skepticism=3. At skepticism=1 the Adversary is indistinguishable from the Enumerator.

3. **Note severity inflation as a known skepticism=3 artifact.** Reviewers at skepticism=3 with stage=final escalate severity more aggressively. Downstream consumers of findings should be aware that severity at skepticism=3 represents a conservative (worst-case) assessment.

4. **Consider a single-framing gate profile at skepticism=2 as the new cost/quality sweet spot.** Both framings at skepticism=1 produce the same output at lower cost than either at skepticism=3, but miss the additional findings. Skepticism=2 may offer a middle path — sufficient to differentiate framings, without the full cost of skepticism=3's extra passes.
