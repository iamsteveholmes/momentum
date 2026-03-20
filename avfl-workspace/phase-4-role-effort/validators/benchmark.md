# Phase 4 Validator Benchmark — Role × Effort × Model

**Date:** 2026-03-20
**Fixture:** `pipeline-arch-multi-iter.md` (9 seeded issues: 2C, 2H, 3M, 2L)
**Enum lens:** Structural Integrity (structural_validity, completeness, cross_reference_integrity)
**Adv lens:** Factual Accuracy (correctness, traceability, logical_soundness)
**Skepticism:** 3 (flat)
**C1 = seeded critical: parallel/sequential contradiction (Overview vs Stage 2)**

---

## Enumerator (Structural Integrity) — 9 Runs

| Config | Findings | Score | C1? | Seeded hits | Tokens | Time |
|---|---|---|---|---|---|---|
| enum-low-haiku | 2 (2C) | 70 | ✓ critical | ~2 | 33,833 | 65s |
| enum-medium-haiku | 1 (1H) | 92 | **✗ MISS** | 1 | 32,980 | 64s |
| enum-high-haiku | 2 (2H) | 84 | ✓ high | ~2 | 34,451 | 74s |
| enum-low-opus | 5 (1H,2M,2L) | 84 | ✗ (out-of-scope*) | ~4 | 30,466 | 91s |
| enum-medium-opus | 3 (2H,1M) | 81 | ✓ high | ~3 | 29,896 | 84s |
| enum-high-opus | 8 (3H,4M,1L) | 63 | ✓ high | ~5 | 30,850 | 90s |
| enum-low-sonnet | 5 (2H,2M,1L) | 77 | ✓ high | ~4 | 30,722 | 109s |
| enum-medium-sonnet | 7 (1C,2H,3M,1L) | 63 | ✓ (C1 as medium) | ~5 | 31,122 | 114s |
| enum-high-sonnet | 8 (3H,4M,1L) | 62 | ✓ medium | ~6 | n/a | n/a |

*Opus low: C1 was noted but classified as out-of-scope for Coherence lens — lens discipline triggered. The parallel/sequential contradiction is structural; Opus correctly identified it belongs to structural_validity but then declined to flag it. This is a framing boundary issue, not a miss.

### Enum Observations

- **Haiku medium is the only run to completely miss C1** — produced a single finding (Section 6 dangling ref) and scored 92. A false pass on a document with a critical architectural contradiction. This is the most dangerous failure mode: high confidence, wrong answer.
- **Haiku effort effect:** Low caught C1 as critical; medium missed it entirely; high caught it as high. Non-monotonic — medium effort does not improve over low for Haiku.
- **Opus effort effect:** Monotonically more findings as effort increases (5→3→8), but score drops (84→81→63). High effort Opus is most thorough but also generates more findings of uncertain value.
- **Sonnet effort effect:** More findings with more effort (5→7→8), lower scores. Sonnet consistently finds C1 across all effort levels.
- **Token cost:** Surprisingly flat across effort levels per model. ~30-35k tokens per run regardless of effort.

---

## Adversary (Factual Accuracy) — 9 Runs

| Config | Findings | Score | C1? | C1 severity | Tokens | Time |
|---|---|---|---|---|---|---|
| adv-low-haiku | 9 (1C,5H,3M) | 46 | ✓ | critical | 34,185 | 72s |
| adv-medium-haiku | 7 (1C,3H,3M) | 52 | ✓ | critical | 34,772 | 76s |
| adv-high-haiku | 7 (1C,3H,2M,1L) | 78 | ✓ | critical | 33,334 | 73s |
| adv-low-opus | 6 (1C,3H,1M,1L) | 62 | ✓ | critical | 30,507 | 95s |
| adv-medium-opus | 7 (1C,3H,2M,1L) | 62 | ✓ | critical | n/a | n/a |
| adv-high-opus | 7 (1C,2H,3M,1L) | 59 | ✓ | critical | n/a | n/a |
| adv-low-sonnet | 5 (2H,2M,1L) | 67 | ✓ | **high** | n/a | n/a |
| adv-medium-sonnet | 4 (2H,1M,1L) | 80 | ✓ | **high** | n/a | n/a |
| adv-high-sonnet | 6 (3H,2M,1L) | 61 | ✓ | **high** | n/a | n/a |

### Adv Observations

- **All 9 Adversary runs caught C1.** The Adversary framing (Factual Accuracy lens) reliably detects the parallel/sequential contradiction across all models and effort levels.
- **Sonnet Adversary severity calibration:** Consistently classifies C1 as **high** (not critical). Haiku and Opus both classify it as **critical**. This is a systematic severity calibration difference — Sonnet's Adversary role is more conservative about critical-level findings.
- **Haiku Adversary over-generation at low effort:** 9 findings, score 46 — the most aggressive output in the dataset. Haiku low generates more findings than any other configuration, not fewer.
- **Adv token cost:** ~30-35k, identical to Enum. Single-agent token cost is approximately model-dependent, not effort-dependent.

---

## Cross-Framing: C1 Detection and Severity

The parallel/sequential contradiction (C1) is the hardest seeded issue — it requires cross-section reading, not just local inspection.

| Model | Enum C1 severity | Adv C1 severity |
|---|---|---|
| Haiku | critical (low), **MISS** (med), high (high) | critical × 3 |
| Opus | ✗ out-of-scope (low), high (med), high (high) | critical × 3 |
| Sonnet | high (low), medium (med), medium (high) | **high** × 3 |

Key finding: **Framing matters more than model for C1 detection.** The Adversary framing catches C1 reliably; the Enumerator framing is inconsistent (model-dependent, effort-dependent, with one complete miss). The cross-section nature of C1 — requiring synthesis across sections — is better suited to the Adversary's holistic pattern-awareness than the Enumerator's section-by-section traversal.

---

## Score Distribution

| Metric | Enum | Adv |
|---|---|---|
| Min score | 62 (sonnet-high) | 46 (haiku-low) |
| Max score | 92 (haiku-medium) | 80 (sonnet-medium) |
| Mean score | ~76 | ~63 |
| Std dev | ~10 | ~11 |

The Enumerator mean is higher because it uses a different lens (structural) and misses some issues the Adversary catches. The Adversary's lower scores reflect its broader scope of findings on the Factual Accuracy lens.

---

## Findings Volume vs Score Discrepancy

Several runs show mismatches between stated `score` and calculated score from severity deductions:

- adv-low-sonnet: score=67, calculated=77
- adv-high-opus: score=59, calculated=69
- adv-high-sonnet: score=61, calculated=69
- enum-medium-sonnet: score=63, calculated=59

These discrepancies suggest validator subagents sometimes apply their own scoring adjustments beyond the standard deduction formula. This inconsistency should be addressed in the skill — either enforce the formula or remove the free-form score field in favor of calculated-only.

---

## Effort Effect Summary

**Effort does not monotonically improve quality** for either framing at any model tier tested.

| Model | Framing | Effort effect |
|---|---|---|
| Haiku | Enum | Non-monotonic: low=ok, medium=catastrophic miss, high=ok |
| Haiku | Adv | Volume decreases with effort (9→7→7); severity consistent |
| Opus | Enum | Finding volume increases with effort; severity decreases (3H→3H→3H) |
| Opus | Adv | Severity consistent; finding count roughly stable |
| Sonnet | Enum | Finding volume increases with effort; C1 detected at all levels |
| Sonnet | Adv | Finding count decreases with effort (5→4→6); score varies |

The clearest signal: **effort level does not correlate with finding quality or score in any predictable direction.** The Haiku enum-medium miss at 92/100 is the most dangerous outcome and is effort-related. For production use, high effort is recommended for the Enumerator role simply because the medium-effort failure mode (false pass) is worse than the high-effort failure mode (more findings).

---

## Timing and Cost Summary

| Tier | Runs with timing | Avg tokens | Avg time |
|---|---|---|---|
| Haiku (all) | 6/6 | 33,926 | 71s |
| Opus (enum only) | 3/3 | 30,404 | 88s |
| Opus (adv partial) | 1/3 | 30,507 | 95s |
| Sonnet (enum partial) | 2/3 | 30,922 | 112s |

**Cost is approximately flat across effort levels per model.** Single-agent validator runs do not consume meaningfully more tokens at higher effort. The effort parameter appears to affect reasoning thoroughness without proportional output volume increase.

---

## Recommendations for AVFL Production Config

1. **Adversary framing for cross-section issues:** Use Adversary validators for catching contradictions that span sections. The Enumerator's systematic traversal misses issues that require holistic synthesis.
2. **Never use Haiku enum-medium alone:** The combination produced a false 92/100 pass on a document with a critical flaw. If using Haiku, use high effort for Enumerator role.
3. **Dual-reviewer design validated:** The cross-check between Enumerator (structural traversal) and Adversary (holistic skepticism) is load-bearing — they catch different categories of issues. A single-framing validator would miss issues the other detects.
4. **Sonnet severity calibration note:** Sonnet Adversary systematically calls critical issues "high." In a dual-reviewer setup, this means Sonnet-only runs will never produce critical findings from the Adversary lens. Haiku or Opus Adversary reviewers provide better critical-severity coverage.
5. **Score calculation must be enforced:** Free-form score fields in validator output cause discrepancies. The consolidator should recalculate scores from finding counts rather than trusting reported scores.
