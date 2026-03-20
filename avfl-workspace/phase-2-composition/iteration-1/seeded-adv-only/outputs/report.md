# AVFL Validation Report — 3-Lens Adversary-Only
## Variant: avfl-3lens-adv-only

**Run date:** 2026-03-20
**Domain expert:** research analyst
**Task context:** AI validation research summary document with 2 deliberately seeded errors
**Output validated:** `/Users/steve/projects/momentum/avfl-workspace/fixtures/research-summary-seeded.md`
**Source material:** `/Users/steve/projects/momentum/avfl-workspace/fixtures/research-source-material.md`
**Profile:** full
**Active lenses:** Structural Integrity, Factual Accuracy, Coherence & Craft
**Inactive lens:** Domain Fitness
**Reviewer composition:** 1 Adversary per lens (3 agents total), no Enumerator, no dual-review cross-check

---

## Final Status

**CLEAN**

Output passed validation with score 100/100 after 2 iterations.

---

## Scores Per Iteration

| Iteration | Score | Decision |
|---|---|---|
| 1 | 81/100 | FAIL — proceed to fix |
| 2 | 100/100 | PASS — CLEAN |

**Iteration count:** 2
**Pass threshold:** 95/100

---

## All Findings (Iteration 1)

All confidence values are MEDIUM by default (adversary-only, no dual-review cross-check).

---

### ACCURACY-001

- **Severity:** HIGH
- **Dimension:** correctness
- **Location:** Key Findings → Multi-Agent Review Performance (paragraph 1)
- **Description:** The Meta-Judge improvement statistic is wrong and the optimal reviewer count conclusion is inverted. The document claims 3 reviewers give 15% absolute accuracy improvement and that 3-reviewer configuration is optimal. The source material shows 2 reviewers give ~8–9% improvement and adding a 3rd reviewer *decreases* performance below the 2-agent baseline.
- **Evidence:**
  - Document text: "Meta-Judge (2025) found that using 3 independent reviewers outperformed a single-agent approach by 15% absolute accuracy, with optimal performance achieved at the 3-reviewer configuration. Teams should therefore target at least 3 reviewers per validation pass to maximize accuracy gains."
  - Source material: "Two agents with cross-checking achieved 77.26% accuracy versus 68.89% for single-agent review — approximately 8–9% absolute improvement. Adding a third reviewer decreased performance below the 2-agent baseline. The sweet spot is 2 reviewers, not 3."
- **Suggestion:** Correct the improvement figure to ~8–9% absolute (77.26% vs 68.89%), note that a 3rd reviewer decreased performance, and recommend 2 reviewers as the sweet spot.
- **Confidence:** MEDIUM

---

### COHERENCE-001

- **Severity:** HIGH
- **Dimension:** consistency
- **Location:** Executive Summary (line 4) vs. Methodology → Validation Threshold section
- **Description:** The document states two different validation thresholds in two different sections with no acknowledgment of the discrepancy. A practitioner reading the Executive Summary would use 90 as the operational threshold; the Methodology section specifies 95. These are directly contradictory on a core operational parameter.
- **Evidence:**
  - Executive Summary: "a validation threshold of 90 out of 100 providing the optimal balance between quality requirements and iteration cost"
  - Methodology section: "we recommend outputs scoring below 95 out of 100 be flagged for remediation and re-validation"
- **Suggestion:** Align both sections to the same threshold. The Methodology section contains the rationale and should be treated as canonical; update the Executive Summary to read "95 out of 100."
- **Confidence:** MEDIUM

---

### COHERENCE-002

- **Severity:** MEDIUM
- **Dimension:** consistency
- **Location:** Key Findings → Multi-Agent Review Performance vs. Methodology → Reviewer Configuration
- **Description:** The Key Findings section recommends "at least 3 reviewers per validation pass" while the Methodology section recommends "a 2-reviewer configuration per validation lens." These are internally contradictory recommendations within the same document.
- **Evidence:**
  - Key Findings: "Teams should therefore target at least 3 reviewers per validation pass to maximize accuracy gains."
  - Methodology: "We recommend a 2-reviewer configuration per validation lens."
- **Suggestion:** Fix the factual error in ACCURACY-001 first; the corrected Meta-Judge finding will support the 2-reviewer recommendation in Methodology and eliminate the contradiction. COHERENCE-002 resolves as a side effect of ACCURACY-001 fix.
- **Confidence:** MEDIUM

---

## Findings Summary (Iteration 1)

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 2 |
| Medium | 1 |
| Low | 0 |
| **Total** | **3** |

**Score calculation:** 100 − 8 (ACCURACY-001 HIGH) − 8 (COHERENCE-001 HIGH) − 3 (COHERENCE-002 MEDIUM) = **81**

**Duplicates removed:** 0
**False positives removed:** 0

---

## Seeded Error Detection

### Error 1 — Factual (Accuracy Lens Target)

**Seeded error:** Meta-Judge statistic wrong — document claims 3 reviewers improve accuracy by 15%, source shows 2 reviewers give ~8–9% improvement and a 3rd reviewer decreases performance.

**Caught?** YES

**Finding ID:** ACCURACY-001 (HIGH)

The adversary on the Factual Accuracy lens identified this during Iteration 1. The hunch was triggered by the suspiciously clean "15%" figure and the "optimal at 3 reviewers" claim. Verification against source material confirmed both the wrong percentage (15% vs 8–9%) and the inverted conclusion (document says 3 is optimal; source says 3 decreases performance). The finding was correctly graded HIGH — a factual error against source material that directly undermines the primary recommendation of the document.

---

### Error 2 — Consistency (Coherence Lens Target)

**Seeded error:** Threshold contradiction — Executive Summary states pass threshold is 90/100, Methodology section states 95/100.

**Caught?** YES

**Finding ID:** COHERENCE-001 (HIGH)

The adversary on the Coherence & Craft lens identified this during Iteration 1 on a holistic read-through. The contradiction between "90 out of 100" in the Executive Summary and "95 out of 100" in the Methodology Validation Threshold section was flagged with direct textual evidence from both locations. Graded HIGH — an internal contradiction on a core operational parameter (the pass/fail threshold) that would directly mislead any practitioner implementing the recommendations.

---

## Phase-by-Phase Pipeline Summary

### Iteration 1

**Phase 1 — VALIDATE (parallel, 3 Adversary agents)**

| Lens | Agent | Findings |
|---|---|---|
| Structural Integrity | Adversary | NO FINDINGS — document structure is well-formed, all required sections present, all named study references resolve against source material |
| Factual Accuracy | Adversary | 1 finding: ACCURACY-001 (HIGH) — Meta-Judge statistic and reviewer-count conclusion both wrong against source |
| Coherence & Craft | Adversary | 2 findings: COHERENCE-001 (HIGH) — threshold contradiction 90 vs 95; COHERENCE-002 (MEDIUM) — reviewer count contradiction 3 vs 2 |

**Phase 2 — CONSOLIDATE**

- No dual-review; all findings default to MEDIUM confidence
- Merged 3 findings from 2 lenses
- Deduplication: ACCURACY-001 and COHERENCE-002 are related (same root cause) but distinct findings (one is factual error vs. source, the other is internal document contradiction) — both retained
- All findings have evidence — none removed
- Score: 100 − 8 − 8 − 3 = **81**
- Grade: Fair

**Phase 3 — EVALUATE**

Score 81 < 95. Iteration 1 < max 4. Decision: proceed to FIX.

**Phase 4 — FIX**

Research analyst fixed in severity order:
1. ACCURACY-001 (HIGH): Corrected Meta-Judge paragraph — changed "15% absolute accuracy" to "approximately 8–9% absolute improvement," changed "optimal at 3-reviewer configuration" to "adding a third reviewer decreased performance below the 2-agent baseline," updated recommendation from "at least 3 reviewers" to "sweet spot is 2 reviewers."
2. COHERENCE-001 (HIGH): Updated Executive Summary threshold from "90 out of 100" to "95 out of 100" to align with Methodology section.
3. COHERENCE-002 (MEDIUM): Resolved as a side effect of ACCURACY-001 fix — Key Findings now says "sweet spot is 2 reviewers," which is consistent with Methodology's "2-reviewer configuration."

---

### Iteration 2

**Phase 1 — VALIDATE (parallel, 3 Adversary agents)**

| Lens | Agent | Findings |
|---|---|---|
| Structural Integrity | Adversary | NO FINDINGS |
| Factual Accuracy | Adversary | NO FINDINGS — Meta-Judge paragraph now matches source material exactly |
| Coherence & Craft | Adversary | NO FINDINGS — threshold (95/100) consistent across Executive Summary and Methodology; reviewer count (2) consistent across Key Findings and Methodology |

**Phase 2 — CONSOLIDATE**

No findings. Score: **100**. Grade: Clean.

**Phase 3 — EVALUATE**

Score 100 ≥ 95. Decision: **CLEAN — exit.**

---

## Fix Log

| Finding ID | Change Made |
|---|---|
| ACCURACY-001 | Rewrote Meta-Judge paragraph: corrected improvement figure from 15% to ~8–9% absolute; noted 3rd reviewer decreases performance; changed recommendation from "at least 3 reviewers" to "sweet spot is 2 reviewers, not 3, with framing diversity as the key mechanism" |
| COHERENCE-001 | Updated Executive Summary threshold from "90 out of 100" to "95 out of 100" |
| COHERENCE-002 | Resolved as side effect of ACCURACY-001 fix; no separate change required |
