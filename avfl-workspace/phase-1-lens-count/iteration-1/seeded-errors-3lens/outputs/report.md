# AVFL Validation Report
## Benchmark: Phase 1 — 3-Lens Configuration

**Run date:** 2026-03-20
**Skill:** avfl-3lens (Structural + Accuracy + Coherence)
**Profile:** full
**Domain expert:** research analyst
**Task context:** research summary on AI validation techniques
**Input:** `avfl-workspace/fixtures/research-summary-seeded.md`
**Source material:** `avfl-workspace/fixtures/research-source-material.md`

---

## Final Status: CLEAN

**Final score:** 100/100
**Iteration count:** 2

---

## Score Per Iteration

| Iteration | Score | Status |
|---|---|---|
| 1 | 69 | FAIL — 3 high, 2 medium, 1 low findings |
| 2 | 100 | PASS — CLEAN |

---

## Seeded Error Detection

| Error | Description | Caught? | Lens | Confidence |
|---|---|---|---|---|
| Error 1 | Meta-Judge statistic wrong: document states "3 reviewers, 15% accuracy improvement, optimal at 3-reviewer configuration" — source states 2 reviewers achieved ~8-9% improvement and adding a 3rd decreased performance | YES | Factual Accuracy (both Enumerator and Adversary) | HIGH |
| Error 2 | Threshold contradiction: Executive Summary states 90/100, Methodology states 95/100 | YES | Coherence & Craft (both Enumerator and Adversary) | HIGH |

**Both seeded errors caught in Iteration 1.**

---

## All Findings — Iteration 1

### F-001 — HIGH confidence
- **Severity:** high
- **Dimension:** correctness
- **Location:** Key Findings → Multi-Agent Review Performance (paragraph 1)
- **Description:** Meta-Judge statistic is wrong on two counts: (1) the improvement is attributed to 3 reviewers rather than 2, and (2) the improvement is stated as 15% absolute rather than ~8-9%. Additionally, the document states "optimal performance achieved at the 3-reviewer configuration" when the source explicitly states a 3rd reviewer decreased performance below the 2-agent baseline.
- **Evidence:** Document: "Meta-Judge (2025) found that using 3 independent reviewers outperformed a single-agent approach by 15% absolute accuracy, with optimal performance achieved at the 3-reviewer configuration." Source: "Two agents with cross-checking achieved 77.26% accuracy versus 68.89% for single-agent review — approximately 8–9% absolute improvement. Adding a third reviewer decreased performance below the 2-agent baseline."
- **Seeded error:** YES — Error 1
- **Confirmed by:** Accuracy Enumerator (ACCURACY-001) + Accuracy Adversary (ACC-ADV-001)

### F-002 — HIGH confidence
- **Severity:** high
- **Dimension:** logical_soundness
- **Location:** Key Findings → Multi-Agent Review Performance (last sentence of paragraph 1)
- **Description:** Recommendation to "target at least 3 reviewers per validation pass" directly contradicts source material which identifies 2 as the optimal configuration and explicitly states a 3rd reviewer hurts performance.
- **Evidence:** Document: "Teams should therefore target at least 3 reviewers per validation pass to maximize accuracy gains." Source: "The sweet spot is 2 reviewers, not 3."
- **Seeded error:** Downstream of Error 1 (same wrong premise)
- **Confirmed by:** Accuracy Enumerator (ACCURACY-002) + Accuracy Adversary (ACC-ADV-002)

### F-003 — HIGH confidence
- **Severity:** high
- **Dimension:** consistency
- **Location:** Executive Summary (paragraph 1) vs. Methodology → Validation Threshold
- **Description:** Threshold contradiction within the same document. Executive Summary states the validation threshold is "90 out of 100" while the Methodology section states "outputs scoring below 95 out of 100 be flagged for remediation." A reader cannot reconcile which threshold applies.
- **Evidence:** Executive Summary: "a validation threshold of 90 out of 100 providing the optimal balance between quality requirements and iteration cost." Methodology → Validation Threshold: "we recommend outputs scoring below 95 out of 100 be flagged for remediation and re-validation."
- **Seeded error:** YES — Error 2
- **Confirmed by:** Coherence Enumerator (COHERENCE-001) + Coherence Adversary (COH-ADV-001)

### F-004 — HIGH confidence
- **Severity:** medium
- **Dimension:** consistency
- **Location:** Key Findings → Multi-Agent Review Performance (last sentence) vs. Methodology → Reviewer Configuration
- **Description:** Document recommends "at least 3 reviewers per validation pass" in Key Findings but "a 2-reviewer configuration per validation lens" in Methodology. Internally contradictory recommendation.
- **Evidence:** Key Findings: "Teams should therefore target at least 3 reviewers per validation pass." Methodology → Reviewer Configuration: "We recommend a 2-reviewer configuration per validation lens."
- **Note:** This is a coherence-layer manifestation of the same factual error as F-001/F-002. Resolved when F-001/F-002 were fixed.
- **Confirmed by:** Coherence Enumerator (COHERENCE-002) + Coherence Adversary (COH-ADV-002)

### F-005 — HIGH confidence
- **Severity:** medium
- **Dimension:** correctness
- **Location:** Key Findings → Multi-Agent Review Performance (PoLL paragraph)
- **Description:** PoLL finding characterized as "more reviewers produces better outcomes" — strips out the critical finding that framing diversity (not raw count) drives the accuracy improvement. Source explicitly states "different framings are essential — same-prompt reviewers capture far less benefit."
- **Evidence:** Document: "consistently showing that more reviewers produces better outcomes." Source: "Critically, different framings are essential — same-prompt reviewers capture far less benefit than differently-framed reviewers."
- **Confirmed by:** Accuracy Enumerator (ACCURACY-003) + Accuracy Adversary (ACC-ADV-003)

### F-006 — HIGH confidence
- **Severity:** low
- **Dimension:** correctness
- **Location:** Key Findings → Staged Validation Efficiency
- **Description:** "Step-level feedback is 8% more accurate" omits the greater-than qualifier present in source material.
- **Evidence:** Document: "step-level feedback is 8% more accurate." Source: "Step-level feedback is >8% more accurate."
- **Confirmed by:** Accuracy Enumerator (ACCURACY-004) + Accuracy Adversary (ACC-ADV-004)

---

## Fix Log — Iteration 1

Fixes applied in severity order (critical first, then high, medium, low).

**F-001 (high — correctness):** Corrected Meta-Judge paragraph. Changed "3 independent reviewers outperformed a single-agent approach by 15% absolute accuracy, with optimal performance achieved at the 3-reviewer configuration" to "2 independent reviewers with cross-checking outperformed a single-agent approach by approximately 8–9% absolute accuracy (77.26% vs. 68.89%), with performance declining when a third reviewer was added below the 2-reviewer baseline."

**F-002 (high — logical_soundness):** Changed "Teams should therefore target at least 3 reviewers per validation pass to maximize accuracy gains" to "Teams should therefore target 2 reviewers per validation lens to maximize accuracy gains." (Resolved as part of F-001 — same paragraph.)

**F-003 (high — consistency):** Changed Executive Summary threshold from "90 out of 100" to "95 out of 100" to match the Methodology section's threshold statement.

**F-004 (medium — consistency):** Resolved as a downstream consequence of F-001/F-002 fix. Key Findings now recommends 2 reviewers, consistent with Methodology's "2-reviewer configuration."

**F-005 (medium — correctness):** Revised PoLL paragraph to accurately characterize framing diversity as the key mechanism. Changed "consistently showing that more reviewers produces better outcomes" to "consistently showing that differently-framed reviewers produce better outcomes than a single reviewer. Critically, framing diversity — not raw reviewer count — drives the accuracy improvement."

**F-006 (low — correctness):** Changed "step-level feedback is 8% more accurate" to "step-level feedback is >8% more accurate."

---

## Fixed Document (Final State)

```markdown
# AI-Generated Content Validation: Research Summary

## Executive Summary
This document summarizes key findings on multi-agent AI validation techniques. Our analysis identifies dual-reviewer cross-checking as a high-impact quality lever, with a validation threshold of 95 out of 100 providing the optimal balance between quality requirements and iteration cost.

## Key Findings

### Multi-Agent Review Performance
Recent research demonstrates that increasing the number of independent reviewers improves validation accuracy — up to a point. Meta-Judge (2025) found that using 2 independent reviewers with cross-checking outperformed a single-agent approach by approximately 8–9% absolute accuracy (77.26% vs. 68.89%), with performance declining when a third reviewer was added below the 2-reviewer baseline. Teams should therefore target 2 reviewers per validation lens to maximize accuracy gains.

The PoLL (2024) study corroborated these findings using panel evaluations across multiple benchmarks, consistently showing that differently-framed reviewers produce better outcomes than a single reviewer. Critically, framing diversity — not raw reviewer count — drives the accuracy improvement.

### Error Propagation Risk
Huang (2023) identified a 73% probability that a single error in a pipeline step will cause downstream failure. At 90% per-step accuracy across 8 sequential steps, overall accuracy degrades to approximately 43%. This underscores the importance of catching errors early rather than relying on final-output review.

### Staged Validation Efficiency
Process Reward Models (PRMs) demonstrate that step-level feedback is >8% more accurate and 1.5–5× more compute-efficient than outcome-only evaluation, but only when validation is focused on steps where errors actually matter. The "bookend + critical gates" pattern — heavy validation at input and output, light gates in between — achieves the best cost-quality tradeoff.

### Late-Stage Fragility
ASCoT (2025) found that errors introduced at step 4 of a 4-step pipeline caused a 51.69% accuracy drop, compared to only 14.64% for errors at step 2. This "semantic commitment" effect means models lock into trajectories with reduced self-correction ability at later stages, making penultimate-step validation particularly valuable.

## Methodology

### Validation Threshold
Based on our analysis, we recommend outputs scoring below 95 out of 100 be flagged for remediation and re-validation. This threshold reflects a high-quality bar that filters noise while catching substantive issues.

### Reviewer Configuration
We recommend a 2-reviewer configuration per validation lens. The reviewers use different cognitive framings — systematic enumeration vs. adversarial skepticism — to maximize finding diversity while controlling cost. Research confirms that framing diversity, not raw reviewer count, drives the accuracy improvement.

### Staged Application
Apply validation profiles based on pipeline position:
- Input: lightweight structural check (gate)
- First interpretation step: medium-intensity check (checkpoint)
- Final output: full multi-reviewer validation

## Conclusions
The evidence supports a staged, dual-reviewer validation approach with early gate checks and comprehensive final validation. The key insight is that framing diversity between reviewers matters more than reviewer count, and that step-level validation is far more efficient than outcome-only review when focused on the right steps.
```

---

## Iteration 2 — Validation Results

All 6 validators (Structural Enumerator, Structural Adversary, Accuracy Enumerator, Accuracy Adversary, Coherence Enumerator, Coherence Adversary) returned NO FINDINGS on the fixed document.

Score: 100/100 — CLEAN

---

## Summary

| Metric | Value |
|---|---|
| Final status | CLEAN |
| Final score | 100/100 |
| Iteration 1 score | 69/100 |
| Iteration 2 score | 100/100 |
| Total iterations | 2 |
| Total findings (Iteration 1) | 6 (3 high, 2 medium, 1 low) |
| Findings fixed | 6 |
| Findings remaining | 0 |
| Error 1 caught (Meta-Judge statistic) | YES — HIGH confidence |
| Error 2 caught (threshold 90 vs 95) | YES — HIGH confidence |
| Both lenses that caught seeded errors | Accuracy (Error 1), Coherence (Error 2) |
