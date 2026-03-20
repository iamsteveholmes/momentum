# Consolidator Notes — medium/sonnet

## Run Summary

- Config: consolidator-medium-sonnet
- Document: pipeline-arch-multi-iter.md
- Input validators: 6 (structural_enum, structural_adv, accuracy_enum, accuracy_adv, coherence_enum, coherence_adv)
- Raw findings in: 19 (before dedup/filter)
- Duplicates removed: 7
- False positives removed: 1 (hallucination)
- Final findings: 13
- Score: 40 / 100 — Failing

---

## Hallucination Filtered

**SA-HAL-001 — DISCARDED**

SA-HAL-001 claimed "The document references SLA targets in Stage 3 that are contradicted by the Performance Characteristics section." The finding's own evidence statement contradicts itself: "Stage 3 mentions SLA targets — no such text exists in Stage 3." The finding invents text it then acknowledges does not exist. This is a self-refuting hallucination. Discarded per the rule: findings without evidence are discarded, and evidence that actively contradicts the claim is disqualifying.

---

## Merge Decisions

**F-001 (critical, structural_validity)** — SE-001 and SA-001 are the same issue with different framing. SE-001 (Enumerator) quotes both contradicting passages verbatim; SA-001 (Adversary) characterizes it as "execution topology" contradiction. SE-001's evidence is more specific; SA-001's framing is useful context. Kept SE-001 evidence, incorporated SA-001's "execution topology" framing into the description.

**F-002 (high, cross_reference_integrity)** — SE-002 and SA-002 are identical. SE-002 (Enumerator) is marginally more specific about location ("final sentence"). Merged to SE-002 with no substantive change.

**F-003 (high, correctness)** — AE-001 and AA-001 are the same factual inversion claim. Both cite the same evidence. AE-001 explains the domain reasoning more fully ("batch incurs setup overhead"). Kept AE-001 as primary, severity unchanged at high from both.

**F-004 (high, correctness)** — AE-002 and AA-002 are the same claim. AE-002 provides slightly fuller evidence text; AA-002 adds the "extraordinary claim" framing. Merged.

**F-005 (medium, traceability)** — AE-003 and AA-003 are identical findings on benchmark attribution. Note: F-005 is a distinct finding from F-003 — the correctness violation (inverted claim) and the traceability violation (unsourced claim) are different dimensions, both legitimate on the same sentence.

**F-007 (medium, consistency)** — CE-001 and CA-001 are the same terminology drift issue. CA-001 adds "the document never settles on which term means what" framing. Merged descriptions.

**F-008 (medium, completeness)** — CE-002 and CA-002 are identical. Merged.

**F-012 (low, clarity)** — CE-004 and CA-003 are identical (ETL unexpanded). Merged.

---

## MEDIUM-Confidence Findings: Disposition

**SE-003 (F-011, low) — KEPT.** Single-reviewer (Enumerator only). Evidence is direct and concrete — the text states authentication is used but names no mechanism. Valid completeness gap. Kept at low severity as it is a specification gap, not a structural error.

**SA-003 (F-009, medium) — KEPT.** Single-reviewer (Adversary only). The scope tension is verifiable from the fixture: Conclusions describe streaming as a future addition, Stage 2 already covers both modes. This is a genuine internal inconsistency. Kept at medium.

**AE-004 (F-006, medium) — KEPT.** Single-reviewer (Enumerator only). The 5-minute polling interval vs. sub-second latency contradiction is logically sound and evidence is specific. The logical incompatibility is real even if it requires cross-section reasoning to see. Kept at medium.

**CE-003 (F-010, medium) — KEPT.** Single-reviewer (Enumerator only). "Large files" threshold undefined is a concrete completeness gap with direct evidence. Kept at medium.

**CA-004 (F-013, low) — KEPT.** Single-reviewer (Adversary only). Prometheus dashboard duplication is a real redundancy, evidence is specific. Kept at low (conciseness issue, not an error).

---

## Cross-Check Conflicts

No severity conflicts across pairs. In all HIGH-confidence pairs, both reviewers assigned the same severity. No escalation or downgrade was required.

---

## Scoring Detail

| Severity | Count | Weight | Total |
|----------|-------|--------|-------|
| critical | 1 | -15 | -15 |
| high | 3 | -8 | -24 |
| medium | 6 | -3 | -18 |
| low | 3 | -1 | -3 |
| **Total deduction** | | | **-60** |

**Score: 100 - 60 = 40**
**Grade: Failing (< 50)**
**Result: continue** (score < 95, not a pass; fix loop should proceed)

The document has a critical structural contradiction (F-001) that alone drops the score to 85, and three high-severity findings (inverted factual claim, unsupported extraordinary claim, dangling reference) that together produce a failing score. The medium and low findings are secondary but compound the quality gap.
