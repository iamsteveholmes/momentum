# Consolidator Notes — medium / haiku

Run: consolidator-medium-haiku
Document: pipeline-arch-multi-iter.md

---

## Hallucinations Filtered

**SA-HAL-001 — DISCARDED**
The adversary structural reviewer claimed Stage 3 references SLA targets that contradict the Performance Characteristics section. The finding's own evidence statement says "Stage 3 mentions SLA targets — no such text exists in Stage 3." This is self-defeating: the evidence refutes the finding rather than supporting it. Classic hallucination pattern — reviewer imagined a detail that would be interesting to find, then noted it doesn't exist. Discarded.

---

## Merge Decisions

**C1 (critical):** SE-001 and SA-001 describe the same parallel/sequential contradiction. SE-001 is slightly more specific (names exact paragraphs); kept SE-001's description as the canonical text. Severity: critical on both — no conflict.

**H1 (high):** AE-001 and AA-001 both flag the inverted batch/streaming performance claim. AE-001's description includes the domain rationale ("streaming outperforms batch at small sizes due to setup overhead"); kept as canonical. Same severity on both.

**H2 (high):** AE-002 and AA-002 both flag the 99.9% latency reduction claim. AE-002's description is more precise ("no baseline, conditions, or methodology"). Same severity.

**H3 (high):** SE-002 and SA-002 both flag the dangling Section 6 reference. SE-002's description is more detailed (notes "document ends at Conclusions"). Assigned to H3 with HIGH confidence. Note: this was originally tagged as cross_reference_integrity, which is correct — the reference does not resolve.

**M1 (medium):** AE-003 and AA-003 both flag the unattributed benchmark. These are separate from H1 — H1 is about the claim being factually wrong; M1 is about the claim lacking a source (traceability dimension). Both findings are real and distinct; kept both.

**M2 (medium):** CE-001 and CA-001 both flag pipeline/workflow terminology drift. CE-001's description is more analytical; kept as canonical with CA-001's evidence supplement.

**M3 (medium):** CE-002 and CA-002 both flag the undefined 'standard retry policy'. Both describe the same gap; CE-002's description is marginally more detailed.

---

## MEDIUM-Confidence Findings Investigated

**M4 (AE-004 only):** 5-minute polling vs sub-second latency internal contradiction. Only the Accuracy Enumerator raised this. However, the evidence is entirely internal to the document — both data points are quoted directly from the fixture. The logical contradiction is real: you cannot have meaningful sub-second delivery monitoring with 5-minute health polls. Kept.

**M5 (SA-003 only):** Conclusions future-enhancement scope contradiction with Stage 2 current content. Only the Structural Adversary raised this. Evidence from both sections is internally coherent — Stage 2 discusses streaming modes, Conclusions treat streaming as future work. Real tension; kept as medium.

**L2 (CE-003 only):** Undefined large-file threshold. Evidence is quoted directly. Legitimate completeness gap — 'large' is a relative term that needs a threshold to be operationally useful. Kept as low.

**L3 (CA-004 only):** Prometheus duplication across Stage 4 and Operational Notes. Evidence is direct quotes from both sections. This is a real redundancy. Kept as low.

---

## Cross-Check Conflicts

No conflicts in severity ratings across paired reviewers. In all HIGH-confidence pairs, both reviewers assigned the same severity level, which increases confidence in those ratings.

---

## Score Calculation

| Severity | Count | Weight | Subtotal |
|----------|-------|--------|----------|
| critical | 1     | -15    | -15      |
| high     | 3     | -8     | -24      |
| medium   | 5     | -3     | -15      |
| low      | 3     | -1     | -3       |
| **Total deduction** | | | **-57** |

**Score: 100 - 57 = 43**
**Grade: Failing — major rework needed**
**Result: continue** (score < 95 pass threshold)

---

## Summary

19 raw findings across 6 validators → 12 consolidated findings after:
- 1 hallucination discarded (SA-HAL-001)
- 8 duplicate pairs merged into single findings

The document has a genuine critical structural contradiction (parallel vs sequential execution), three high-severity issues (inverted factual claim, unsupported extraordinary claim, dangling section reference), and five medium issues including logical inconsistency, terminology drift, and undefined references. This document requires substantial revision before it could be used as a reliable architecture reference.
