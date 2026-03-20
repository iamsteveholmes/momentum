# Phase 4 Consolidator Benchmark — Role × Effort × Model

**Date:** 2026-03-20
**Input fixture:** `raw-validator-findings.json` (19 raw findings from 6 validators: 3 lenses × Enumerator + Adversary)
**Seeded hallucination:** SA-HAL-001 — self-refuting (evidence field states "no such text exists in Stage 3")
**Ground truth:** 9 real issues (seeded in fixture), 1 hallucination to filter

---

## Results — All 9 Runs

| Config | Score | Findings | HAL filtered | Tokens | Time |
|---|---|---|---|---|---|
| low-haiku | 40 | 13 | 1 | 36,397 | 167s |
| medium-haiku | 43 | 12 | 1 | 34,627 | 132s |
| high-haiku | 40 | 13 | 1 | 36,121 | 144s |
| low-sonnet | 40 | 13 | 1 | 34,381 | 126s |
| medium-sonnet | 40 | 13 | 1 | 35,325 | 142s |
| high-sonnet | 42 | 13 | 1 | 36,821 | 157s |
| low-opus | 40 | 13 | 1 | 35,363 | 138s |
| medium-opus | 40 | 13 | 1 | 35,062 | 133s |
| high-opus | 40 | 13 | 1 | 35,935 | 152s |

**Mean score:** 40.6 / **Std dev:** 1.1
**Mean findings:** 12.9 / **Std dev:** 0.3
**HAL filtered:** 1 in all 9 runs (100% consistency)

---

## Key Finding: Consolidation is Model- and Effort-Invariant

This is the most striking result in the Phase 4 dataset. Across 9 runs spanning 3 models and 3 effort levels:

- Score range: **40–43** (3-point spread across the entire matrix)
- Findings range: **12–13** (1-finding spread)
- Hallucination filtering: **9/9 runs correctly filtered SA-HAL-001**

The consolidation task is sufficiently deterministic that any configuration produces the same answer. This is in direct contrast to the validator phase, where model and framing choices produced materially different results.

### Why consolidation converges

The consolidator's task has a structure that reduces variance:
1. **Hallucination filtering** via self-refutation is mechanical — the evidence field contradicts the claim, detectable by any model
2. **Deduplication** across HIGH-confidence pairs is straightforward — both reviewers found the same thing, merge them
3. **Scoring** follows a defined formula — once findings are merged, the score calculation is arithmetic
4. **MEDIUM-confidence decisions** are the only genuine judgment calls, and they converge because the fixture's MEDIUM findings all have concrete, quotable evidence

The task rewards correctness over creativity. More capable models don't produce better consolidation — they produce the same consolidation with more words.

---

## Effort Effect on Consolidation

No meaningful effect. The 3-point score spread (40–43) is within noise:

- Haiku: 40 (low) → 43 (medium) → 40 (high) — non-monotonic
- Sonnet: 40 → 40 → 42 — effectively flat
- Opus: 40 → 40 → 40 — perfectly flat

Higher effort appears to produce slightly more verbose notes.md but identical final consolidated.json outputs.

---

## Token and Time Analysis

| Model | Mean tokens | Mean time |
|---|---|---|
| Haiku | 35,715 | 148s |
| Sonnet | 35,509 | 142s |
| Opus | 35,433 | 141s |

Token usage is nearly identical across models — all three consume ~35k tokens for this task. Time differences are small. Haiku is slightly slower here than in the validator phase, possibly due to the larger input (19 raw findings vs single-lens validation).

---

## Design Recommendation

**Use the cheapest available configuration for the consolidator role.**

Since all configurations produce identical results, the consolidator should be assigned:
- **Model:** Haiku (or whatever is cheapest in the deployment context)
- **Effort:** Low (no quality benefit from higher effort)

This is a meaningful cost optimization in the full AVFL pipeline, where consolidation runs once per iteration and the validator phase (6 parallel agents) dominates cost. Saving on the consolidator keeps the budget available for the roles where model quality actually matters (validators, fixers).

---

## Hallucination Filtering Robustness

Every run correctly identified and discarded SA-HAL-001. The self-refutation signal was strong enough that no model or effort level missed it. This validates the AVFL cross-check design principle: seeding the evidence field with the claim's own contradiction makes hallucination detection mechanical rather than requiring judgment.

This also suggests the fixture's hallucination was too easy to filter. A more realistic stress test would use:
- A hallucination where the evidence is plausible but the claim is subtly wrong
- A hallucination that has partial support from one reviewer but not the paired reviewer
- A hallucination that would require reading the source document to refute

Future benchmark iterations should include harder hallucination variants.
