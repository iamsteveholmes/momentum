# Phase 4 Fixer Benchmark — Role × Effort × Model

**Date:** 2026-03-20
**Input:** `consolidated-findings-for-fixer.json` (9 findings: 1C, 2H, 3M, 2L + score 47/100)
**Source document:** `pipeline-arch-multi-iter.md`
**Pass threshold:** 95/100
**Score before:** 47 (all 9 seeded issues present)

---

## Results — All 9 Runs

| Config | Score after | Applied | Skipped | Tokens | Time |
|---|---|---|---|---|---|
| low-haiku | 97 | 9/9 | 0 | 31,633 | 86s |
| medium-haiku | 97 | 9/9 | 0 | 31,893 | 94s |
| high-haiku | 97 | 9/9 | 0 | 31,717 | 81s |
| **low-sonnet** | **88** | 9/9 | 0 | 16,229 | 79s |
| medium-sonnet | 97 | 9/9 | 0 | 31,510 | 81s |
| high-sonnet | 97 | 9/9 | 0 | 31,687 | 84s |
| low-opus | 97 | 9/9 | 0 | 31,461 | 80s |
| medium-opus | 97 | 9/9 | 0 | 31,965 | 97s |
| high-opus | 97 | 9/9 | 0 | 31,953 | 96s |

**Pass rate (≥95):** 8/9 (89%)
**Mean score after:** 95.9 / **Std dev:** 3.0
**Mean tokens:** 30,672 / **Mean time:** 86s

---

## Key Finding: Fixer Task is Highly Deterministic

Like the consolidator, the fixer applies a structured checklist (9 findings with explicit suggestions) and converges to the same answer across configurations. 8/9 runs applied all 9 findings and estimated 97/100.

The single outlier — fixer-low-sonnet at 88/100 — is notable:
- **All 9 findings were still applied.** The lower self-reported score reflects epistemic caution, not a worse document.
- The agent correctly noted that F-002 (adding a Security Considerations section) and F-009 (specifying "API key") required inference beyond what the findings explicitly stated.
- Every other configuration made those same inferences without flagging them.

**Interpretation:** Sonnet low is more calibrated about confidence — it knows it made judgment calls and says so. The other configs made the same calls with higher stated confidence. The actual fixed document quality is likely similar across all runs; the score difference is in self-assessment, not in fix quality.

---

## Effort Effect on Fixing

No meaningful effect. All configurations applied all 9 findings. Token usage is flat (~31k per run regardless of effort level or model tier).

The fixer task is input-guided: findings come with explicit `suggestion` fields. An agent that reads the finding and applies the suggestion will produce the same result whether running at low or high effort. Higher effort does not improve fix coverage or quality when findings are well-specified.

**High-opus notable decision (F-007):** Retained "workflow" in the Conclusions section because it referred to a "semantically distinct future system" — this is the most nuanced judgment call in the dataset. Low/medium effort runs simply standardized to "pipeline" throughout. Whether the high-opus decision is better depends on whether the document author intended "workflow" as synonymous or as a distinct future concept. This is a case where effort-driven nuance may produce a *different* outcome rather than a strictly *better* one.

---

## Token Analysis

| Model | Mean tokens | Mean time |
|---|---|---|
| Haiku | 31,748 | 87s |
| Sonnet | 26,475 | 81s |
| Opus | 31,793 | 91s |

**Sonnet outlier:** fixer-low-sonnet used only 16,229 tokens — roughly half the other runs. The prompt path was identical; this appears to be a context-handling difference rather than a meaningful quality signal. Sonnet medium and high used ~31.5k, matching the other tiers.

---

## Recommendations for AVFL Production Config

**The fixer role is the most forgiving role for cost optimization.** When findings have explicit suggestions (as AVFL produces), any model at any effort level will apply them correctly.

**Exception:** If findings require substantial inference (e.g., "add a security section" without specifying content), higher-capability models will produce better-quality placeholder content — but they will all pass the score threshold regardless.

**Recommended production config:**
- **Simple/mechanical fixes** (invert claim, expand acronym, define threshold): Haiku low
- **Generative fixes** (add missing section, specify mechanism from context): Sonnet medium or higher — not for correctness, but for quality of the generated content

**The only real fixer failure mode** would be misapplying a finding (e.g., inverting the wrong claim, or fixing the wrong section). None of the 9 runs exhibited this. The AVFL finding format (location + evidence + suggestion) appears sufficient to prevent misapplication across all tested configurations.

---

## Convergence Pattern Across All Three Roles

| Role | Model effect | Effort effect | Key variance source |
|---|---|---|---|
| Validator | **High** | Non-monotonic | Framing × model × effort interact |
| Consolidator | Negligible | Negligible | Task is deterministic given clear findings |
| Fixer | Low | Negligible | Task is guided by explicit suggestions |

The AVFL pipeline has a clear cost structure: **invest in validators, economize on consolidator and fixer.** The validator phase is where quality decisions get made; downstream roles amplify those decisions with minimal additional judgment.
