# Consolidator Notes — medium / opus

Document: pipeline-arch-multi-iter.md
Config: consolidator-medium-opus
Score: 40/100 — Failing / continue

---

## Confidence Tagging

**HIGH confidence** (both Enum and Adv found it within the same lens):
- Structural: SE-001/SA-001 (parallel vs sequential contradiction), SE-002/SA-002 (dangling Section 6 ref)
- Accuracy: AE-001/AA-001 (batch/streaming inversion), AE-002/AA-002 (99.9% latency), AE-003/AA-003 (unattributed benchmark)
- Coherence: CE-001/CA-001 (pipeline/workflow drift), CE-002/CA-002 (retry policy undefined), CE-004/CA-003 (ETL unexpanded)

**MEDIUM confidence** (one reviewer only):
- SE-003: auth mechanism unspecified (Enum only)
- SA-003: streaming future vs current scope contradiction (Adv only)
- AE-004: polling interval vs sub-second latency logic conflict (Enum only)
- CE-003: large files threshold undefined (Enum only)
- CA-004: Prometheus dashboard repetition (Adv only)
- SA-HAL-001: alleged SLA text in Stage 3 (Adv only) — DISCARDED

---

## Duplicates Removed

7 duplicate findings removed during merge (one retained per pair):

| Merged Into | Sources Merged | Kept Description |
|---|---|---|
| C-001 | SE-001, SA-001 | SE-001 (more specific — names both sections precisely) |
| C-002 | SE-002, SA-002 | SE-002 (more specific location) |
| C-003 | AE-001, AA-001 | AE-001 (explicitly names the inversion mechanism) |
| C-004 | AE-002, AA-002 | AE-002 (more specific — names baseline/conditions gap) |
| C-005 | AE-003, AA-003 | AE-003 (more specific) |
| C-006 | CE-001, CA-001 | CE-001 (has exact evidence quotes) |
| C-007 | CE-002, CA-002 | CE-002 (names what's missing: retry count, backoff, timeout) |
| C-012 | CE-004, CA-003 | CE-004 (first-use specificity) |

---

## Hallucinations Filtered

**SA-HAL-001 — DISCARDED**

The adversarial structural validator claimed Stage 3 references SLA targets that contradict the Performance Characteristics section. The validator's own evidence statement reads: "Stage 3 mentions SLA targets — no such text exists in Stage 3." The evidence directly contradicts the finding — the validator asserted text exists while simultaneously stating it does not. This is a self-refuting finding and a clear hallucination. Discarded.

---

## MEDIUM-Confidence Investigations

All five MEDIUM-confidence findings were retained after investigation:

**SE-003** (auth unspecified): The quoted text "Authentication is used to verify each request before processing begins" is concrete and unambiguous — no mechanism is named. Real completeness gap. Kept as low.

**SA-003** (streaming scope contradiction): Stage 2 discusses "both batch and streaming processing modes" while Conclusions treats streaming as a future enhancement. The evidence from each location is directly contradictory. Kept as medium.

**AE-004** (polling vs latency logic): Stage 4's 5-minute polling interval is a real operational constraint. The 99.9% latency claim in Stage 3 implies sub-second delivery. These claims coexist without any scoping clarification. Kept as medium. (Note: closely related to C-004 on the latency claim itself, but addresses a distinct logical dimension — monitoring cadence vs. delivery latency.)

**CE-003** (large files threshold): "Large files are handled separately... via an overflow queue" with no threshold defined is a concrete completeness gap. Kept as medium.

**CA-004** (Prometheus duplication): Both Stage 4 and Operational Notes mention the Prometheus dashboard with near-identical phrasing. Minor but real redundancy. Kept as low.

---

## Score Breakdown

| Severity | Count | Weight | Deduction |
|---|---|---|---|
| critical | 1 | -15 | -15 |
| high | 3 | -8 | -24 |
| medium | 6 | -3 | -18 |
| low | 3 | -1 | -3 |
| **Total** | **13** | | **-60** |

**Final score: 100 - 60 = 40**
**Grade: Failing — major rework needed**
**Result: continue** (fix loop triggered; score < 95 threshold)

The document has a critical structural contradiction, three high-severity factual/accuracy issues including an inverted performance claim and an unsupported 99.9% figure, and six medium issues around scope consistency, undefined terms, and logical coherence. The accuracy findings (C-003, C-004, C-005) together represent the most substantive problem area and should be the first fix priority after the critical contradiction.
