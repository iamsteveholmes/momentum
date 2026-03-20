# AVFL Validation Report
## Benchmark: Phase 2 Composition — Adversary-Only (3-Lens)

| Field | Value |
|---|---|
| Variant | avfl-3lens-adv-only |
| Profile | full |
| Domain Expert | research analyst |
| Task Context | research summary on AI validation techniques |
| Artifact | research-summary-seeded.md |
| Source Material | research-source-material.md |
| Benchmark Run | Phase 2, Iteration 1 |
| Date | 2026-03-20 |

---

## Final Status: CLEAN

**Final Score: 100/100**
**Total Iterations: 2**
**Seeded Errors Caught: Both (Error 1 and Error 2)**

---

## Pipeline Execution Log

### Iteration 1 — Phase 1: VALIDATE

Three Adversary agents launched in parallel (one per lens). Profile: full. Reviewer framing: Adversary only (no Enumerator). All findings default confidence: MEDIUM (no dual-review cross-check in this variant).

#### Lens 1 — Structural Integrity (Adversary)

Dimensions checked: structural_validity, completeness, cross_reference_integrity

The document structure is complete and conventional: Executive Summary, Key Findings (4 sub-sections), Methodology (3 sub-sections), Conclusions. All named studies (Meta-Judge, PoLL, Huang, ASCoT, Process Reward Models) are present in source material — cross-references resolve. No missing required sections, no broken internal references, no schema violations.

The 90/100 vs 95/100 threshold discrepancy is visible from this lens but is a consistency issue owned by the Coherence lens — noted in scope boundary fashion, not reported as a structural finding.

**Lens 1 Result: NO FINDINGS**

---

#### Lens 2 — Factual Accuracy (Adversary)

Dimensions checked: correctness, traceability, logical_soundness

Every significant claim cross-referenced against source material.

**ACCURACY-001**
- severity: high
- dimension: correctness
- location: Key Findings > Multi-Agent Review Performance, paragraph 1
- description: Multiple statistics about Meta-Judge (2025) are wrong, and the conclusion is inverted. Document claims 3 reviewers produced 15% improvement with optimal performance at the 3-reviewer configuration. Source states 2 reviewers achieved ~8-9% improvement and adding a 3rd reviewer DECREASED performance.
- evidence: Document: "Meta-Judge (2025) found that using 3 independent reviewers outperformed a single-agent approach by 15% absolute accuracy, with optimal performance achieved at the 3-reviewer configuration. Teams should therefore target at least 3 reviewers per validation pass to maximize accuracy gains." Source: "Two agents with cross-checking achieved 77.26% accuracy versus 68.89% for single-agent review — approximately 8–9% absolute improvement. Adding a third reviewer decreased performance below the 2-agent baseline. The sweet spot is 2 reviewers, not 3."
- suggestion: Correct to: 2 reviewers, ~8-9% improvement (77.26% vs 68.89%), 3rd reviewer decreased performance, recommend 2 differently-framed reviewers not 3.

**ACCURACY-002**
- severity: medium
- dimension: logical_soundness
- location: Key Findings > Multi-Agent Review Performance, paragraph 2
- description: The PoLL summary is used to reinforce an incorrect "more reviewers = better" framing, omitting PoLL's central finding that framing diversity drives the improvement, not raw reviewer count.
- evidence: Document: "consistently showing that more reviewers produces better outcomes." Source: "Critically, different framings are essential — same-prompt reviewers capture far less benefit than differently-framed reviewers."
- suggestion: Update PoLL summary to include the framing-diversity finding. Do not use PoLL to support a "more reviewers" narrative that the source explicitly qualifies.

**ACCURACY-003**
- severity: low
- dimension: correctness
- location: Key Findings > Staged Validation Efficiency
- description: Document states "8% more accurate" but source says ">8% more accurate." Dropping the ">" symbol weakens the claim.
- evidence: Document: "step-level feedback is 8% more accurate." Source: "Step-level feedback is >8% more accurate."
- suggestion: Restore the ">" symbol: ">8% more accurate."

---

#### Lens 3 — Coherence & Craft (Adversary)

Dimensions checked: consistency, relevance, conciseness, clarity, tonal_consistency, temporal_coherence

**COHERENCE-001**
- severity: high
- dimension: consistency
- location: Executive Summary (paragraph 1) AND Methodology > Validation Threshold
- description: The document states two contradictory validation thresholds. A reader following this document cannot know whether to use 90 or 95 as their threshold.
- evidence: Executive Summary: "a validation threshold of 90 out of 100 providing the optimal balance between quality requirements and iteration cost." Methodology section: "we recommend outputs scoring below 95 out of 100 be flagged for remediation and re-validation."
- suggestion: Align both references to 95/100. The Methodology section is the appropriate location for this recommendation; update the Executive Summary to match.

No other coherence findings. Relevance, conciseness, clarity, tonal consistency, and temporal coherence are all sound.

---

### Iteration 1 — Phase 2: CONSOLIDATE

**Consolidation notes:**
- Adversary-only variant: no dual-review cross-check. All findings treated as MEDIUM confidence.
- No duplicates found across lenses.
- All four findings have mandatory evidence. All are retained after evidence review.

**Consolidated Findings (sorted by severity):**

| ID | Severity | Dimension | Location |
|---|---|---|---|
| ACCURACY-001 | high | correctness | Key Findings > Multi-Agent Review Performance ¶1 |
| COHERENCE-001 | high | consistency | Executive Summary ¶1 / Methodology > Validation Threshold |
| ACCURACY-002 | medium | logical_soundness | Key Findings > Multi-Agent Review Performance ¶2 |
| ACCURACY-003 | low | correctness | Key Findings > Staged Validation Efficiency |

**Score Calculation:**
- Starting score: 100
- ACCURACY-001 (high): −8
- COHERENCE-001 (high): −8
- ACCURACY-002 (medium): −3
- ACCURACY-003 (low): −1
- **Score: 80/100**

**Grade: Fair (70–84) — notable issues found**
**Findings count:** critical: 0, high: 2, medium: 1, low: 1, total: 4
**Duplicates removed:** 0
**False positives removed:** 0

---

### Iteration 1 — Phase 3: EVALUATE

Score 80 < threshold 95. Iteration 1 < max_iterations (4). → Proceed to FIX.

---

### Iteration 1 — Phase 4: FIX

Domain expert (research analyst) applies fixes in severity order against original source material.

**Fixed output (complete corrected document):**

---

# AI-Generated Content Validation: Research Summary

## Executive Summary
This document summarizes key findings on multi-agent AI validation techniques. Our analysis identifies dual-reviewer cross-checking as a high-impact quality lever, with a validation threshold of 95 out of 100 providing the optimal balance between quality requirements and iteration cost.

## Key Findings

### Multi-Agent Review Performance
Recent research demonstrates that reviewer framing diversity significantly improves validation accuracy. Meta-Judge (2025) found that using 2 independent reviewers with different evaluation framings outperformed a single-agent approach by approximately 8–9% absolute accuracy (77.26% vs. 68.89%). Critically, adding a third reviewer decreased performance below the 2-agent baseline — the sweet spot is 2 reviewers, not 3. Teams should therefore target 2 differently-framed reviewers per validation pass rather than maximizing reviewer count.

The PoLL (2024) study corroborated these findings across multiple benchmarks, showing that a panel outperformed single-agent review. The key mechanism is framing diversity — differently-framed reviewers capture substantially more benefit than same-prompt reviewers, confirming that how reviewers approach evaluation matters more than how many reviewers are used.

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

---

**Fix Log:**

| Finding ID | What Was Changed | Why |
|---|---|---|
| ACCURACY-001 | Key Findings > Multi-Agent Review Performance ¶1: "3 independent reviewers" → "2 independent reviewers with different evaluation framings"; "15% absolute accuracy" → "approximately 8–9% absolute accuracy (77.26% vs. 68.89%)"; removed "optimal performance achieved at the 3-reviewer configuration"; replaced "target at least 3 reviewers" → "target 2 differently-framed reviewers per validation pass" | Source states 2 reviewers achieved 77.26% vs 68.89% (~8-9% improvement); 3rd reviewer decreased performance. All three statistics in the original were wrong and the recommendation was inverted. |
| COHERENCE-001 | Executive Summary ¶1: "90 out of 100" → "95 out of 100" | Document contradicted itself — Executive Summary said 90, Methodology said 95. Methodology is the correct location for this recommendation; Executive Summary updated to match. |
| ACCURACY-002 | Key Findings > Multi-Agent Review Performance ¶2: Replaced "consistently showing that more reviewers produces better outcomes" with content that credits framing diversity as the key mechanism per PoLL's actual finding | Source explicitly states framing diversity is the critical variable; document omitted this and mischaracterized the takeaway. |
| ACCURACY-003 | Key Findings > Staged Validation Efficiency: "8% more accurate" → ">8% more accurate" | Source states ">8%"; document dropped the ">" qualifier, understating the finding. |

---

### Iteration 2 — Phase 1: RE-VALIDATE

Three Adversary agents re-validate fixed output.

**Lens 1 (Structural):** Structure unchanged and sound. NO FINDINGS.

**Lens 2 (Accuracy):**
- Meta-Judge: 2 reviewers, ~8-9% improvement, 3rd reviewer decreased performance — matches source exactly. Clean.
- PoLL: framing-diversity finding included. Matches source. Clean.
- Huang: unchanged. Clean.
- ASCoT: unchanged. Clean.
- PRMs: ">8%" present. Clean.
NO FINDINGS.

**Lens 3 (Coherence):**
- Threshold: Executive Summary = 95, Methodology = 95. Consistent. Clean.
- Reviewer count: Key Findings (2 reviewers), Methodology (2 reviewers), Conclusions (framing diversity matters more than count) — all aligned. Clean.
- All other coherence dimensions clean.
NO FINDINGS.

### Iteration 2 — Phase 2: CONSOLIDATE

No findings from any lens.
**Score: 100/100**
**Grade: Clean — production ready**

### Iteration 2 — Phase 3: EVALUATE

Score 100 ≥ threshold 95. → EXIT CLEAN.

---

## Final Report Summary

| Field | Value |
|---|---|
| Final Status | CLEAN |
| Final Score | 100/100 |
| Iteration Count | 2 |
| Score at Iteration 1 | 80/100 |
| Score at Iteration 2 | 100/100 |
| Total Findings (Iteration 1) | 4 (0 critical, 2 high, 1 medium, 1 low) |
| Findings Remaining (Iteration 2) | 0 |
| Seeded Error 1 Caught (accuracy — Meta-Judge stats) | YES — ACCURACY-001 (high) |
| Seeded Error 2 Caught (coherence — threshold contradiction) | YES — COHERENCE-001 (high) |

---

## Seeded Error Detection Summary

**Error 1 (accuracy lens): Meta-Judge wrong statistics**
- Status: CAUGHT
- Finding: ACCURACY-001 (high)
- The document claimed 3 reviewers / 15% improvement. Source says 2 reviewers / ~8-9%, with 3rd reviewer decreasing performance.
- Detected by: Lens 2 (Factual Accuracy) Adversary in Iteration 1.
- Fixed in: Iteration 1 fix pass.

**Error 2 (coherence lens): Contradictory threshold**
- Status: CAUGHT
- Finding: COHERENCE-001 (high)
- Executive Summary stated 90/100; Methodology stated 95/100. Direct internal contradiction.
- Detected by: Lens 3 (Coherence & Craft) Adversary in Iteration 1.
- Fixed in: Iteration 1 fix pass.

---

## Benchmark Observations

**Detection performance:** The Adversary-only configuration caught both seeded errors on the first validation pass. Error 1 (factual/accuracy) was caught correctly by the accuracy lens. Error 2 (consistency/coherence) was caught correctly by the coherence lens. No false positives generated.

**Additional findings:** The Adversary lenses surfaced two additional genuine issues beyond the seeded errors — ACCURACY-002 (PoLL mischaracterization, medium) and ACCURACY-003 (dropped ">" qualifier, low). Both were valid findings with evidence, consistent with Adversary framing's holistic reading approach.

**Structural lens (Lens 1):** Returned no findings, which is correct — the document has no structural issues. The Adversary correctly noted the threshold discrepancy as out-of-scope for the structural lens and deferred it to the coherence lens.

**Iteration efficiency:** Clean in 2 iterations (1 fix pass). All 4 findings from Iteration 1 were resolved by the fix pass, resulting in a score of 100 on Iteration 2.

**Scope discipline:** The structural Adversary correctly identified the threshold discrepancy as a coherence issue and noted it without claiming it as a structural finding. The coherence Adversary correctly claimed it. No lens overlap or double-reporting.
