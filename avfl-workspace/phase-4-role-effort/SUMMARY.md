# Phase 4 Summary: Per-Role Effort × Model Benchmark

**Date:** 2026-03-20
**Runs:** 36 total (18 validators + 9 consolidators + 9 fixers)
**Models:** Haiku, Sonnet, Opus
**Effort levels:** low, medium, high (via skill frontmatter)
**Fixture:** `pipeline-arch-multi-iter.md` (9 seeded issues: 2C, 2H, 3M, 2L)

---

## The Central Question

Does effort level matter, and does it matter equally for each role in the AVFL pipeline?

**Answer: No — effort effect is highly role-dependent and non-monotonic for validators.**

---

## Role 1: Validators

Validators are the only role where model, framing, and effort all produce materially different outcomes.

### Finding 1: Framing matters more than model or effort for cross-section issues

The seeded critical issue (C1: Overview claims all stages run in parallel; Stage 2 requires sequential execution) requires synthesizing across sections. Enumerator validators — which traverse section-by-section — detected it inconsistently. Adversary validators — which read holistically — detected it in all 9 Adversary runs.

| | C1 detected? |
|---|---|
| All 9 Adversary runs | ✓ 9/9 |
| Enumerator runs (9 total) | ✓ 7/9 (2 misses: haiku-medium, opus-low†) |

†opus-low identified it but flagged it as out-of-scope for its lens.

### Finding 2: Haiku enum-medium is the most dangerous configuration

Haiku enum-medium produced a 92/100 false pass — the highest score in the validator dataset — while completely missing the critical parallel/sequential contradiction. This is the worst failure mode: high confidence, wrong answer. The effort effect on Haiku enum is non-monotonic: low=caught (critical), medium=missed, high=caught (high severity).

### Finding 3: Sonnet Adversary has a systematic severity miscalibration

Across all 3 effort levels, Sonnet Adversary classified C1 as "high" rather than "critical." Haiku and Opus Adversary both classified it as "critical." In a dual-reviewer pipeline, Sonnet-only Adversary runs will never produce critical-level findings from the Factual Accuracy lens.

### Finding 4: Token cost is flat across effort levels

Single-agent validator runs consume ~30-35k tokens regardless of model tier or effort level. Effort changes reasoning thoroughness without proportional output volume increase. Cost is approximately model-tier-dependent, not effort-dependent.

### Validator config recommendations

| Use case | Recommended config |
|---|---|
| Maximum recall on cross-section issues | Adversary framing (any model); Haiku/Opus for critical severity |
| Structural completeness | Enumerator, Sonnet or Opus, medium or high effort |
| Never use alone | Haiku Enumerator medium (false-pass risk) |
| Best coverage/cost | Sonnet medium for Enum; Haiku high for Adv |

---

## Role 2: Consolidator

The consolidator result is **fully invariant** across all 9 configurations tested.

| Metric | Value (all 9 runs) |
|---|---|
| Score | 40–43 (3-point spread) |
| Findings | 12–13 |
| Hallucination filtered | 1/1 (100%) |

SA-HAL-001 — a self-refuting hallucination whose own evidence field stated the referenced text didn't exist — was correctly filtered by every configuration. The consolidation task is deterministic: once findings are structured (location, evidence, suggestion), merging and scoring them requires pattern matching, not reasoning.

**Recommendation: Use cheapest available config (Haiku low).**

---

## Role 3: Fixer

The fixer result is near-invariant: 8/9 runs produced 97/100 with all 9 findings applied.

The single outlier (Sonnet low, 88/100) applied all 9 findings correctly but self-penalized for inferences — it knew it was making judgment calls (adding a Security section, specifying "API key") and said so. Other configurations made the same calls with higher confidence. Actual document quality is likely equivalent.

**Token cost:** ~31k per run, flat across effort and model. Time: ~80-97s.

**Recommendation: Haiku low for mechanical fixes (invert claim, expand acronym, define threshold). Sonnet medium or higher for generative fixes (add missing section, specify mechanism from context) — not for correctness, but for generated content quality.**

---

## Cross-Role Cost Structure

The AVFL pipeline has a clear cost hierarchy:

```
Validators     — most expensive, most variable, most impactful
Consolidator   — cheap, deterministic, model-invariant
Fixer          — cheap, deterministic, suggestion-guided
```

In the full pipeline (6 validators + 1 consolidator + 1 fixer per iteration):
- Validators: 6 × ~32k tokens = ~192k tokens
- Consolidator: ~35k tokens
- Fixer: ~32k tokens

Consolidator + fixer together = ~35% of validator cost, produce near-identical results regardless of config. Budget optimization should focus exclusively on validator configuration.

---

## Interaction with Phase 3 Findings

Phase 3 (model variation on full AVFL loop, high effort) showed:
- Haiku medium failed to converge (MAX_ITER at 84/100, 9 additional false findings)
- Sonnet low was most efficient for Sonnet tier (100/100, fewest tokens)
- Opus low reproduced seeded severity profile exactly

Phase 4 adds the role decomposition layer: the Phase 3 "Haiku medium failure" can now be attributed specifically to the **validator phase** — Haiku enum-medium's false-pass behavior would prevent the loop from knowing it needed to continue. The consolidator and fixer would have performed correctly on whatever findings they received.

---

## Revised Effort Recommendation Table

Based on combined Phase 2.x, 3, and 4 data:

| Role | Model | Effort | Rationale |
|---|---|---|---|
| Enumerator validator | Sonnet | medium | Reliable C1 detection; more findings with effort without false-pass risk |
| Adversary validator | Haiku or Opus | high | Critical severity coverage; Sonnet undersells severity |
| Consolidator | Haiku | low | Fully invariant; cheapest config |
| Fixer | Haiku | low | Sufficient for mechanical fixes; upgrade to Sonnet medium for generative content |

**Single-model deployment (cost-constrained):** Sonnet medium across all roles. Avoids the Haiku medium false-pass risk; produces reliable C1 detection; consolidator and fixer add minimal overhead.

**Quality-maximizing deployment:** Dual validator framing (Enum Sonnet medium + Adv Haiku high); Haiku low for consolidator and fixer.

---

## Open Questions for Future Benchmarks

1. **Harder hallucinations:** SA-HAL-001 was self-refuting and trivially filtered. A plausible hallucination with partial support would stress-test consolidator variance more meaningfully.
2. **Fixer misapplication rate:** With ambiguous or conflicting findings, do fixer configs diverge? Current fixture had clean, non-conflicting findings.
3. **Multi-iteration loop behavior:** Phase 3 showed Haiku medium fails to converge. Does the per-role config recommendation change loop convergence behavior?
4. **Sonnet severity calibration:** Is the Adversary critical→high downgrade consistent across document types, or specific to this fixture?
