# Consolidator Notes — high / opus

**Run:** consolidator-high-opus
**Document:** pipeline-arch-multi-iter.md
**Input:** 6 validators (3 lenses × Enumerator + Adversary per lens), 18 raw findings

---

## Merge Decisions

### Structural lens (SE-* / SA-*)

**SE-001 + SA-001 → F-001 (critical, HIGH confidence)**
Both found the parallel/sequential execution contradiction. SA-001 provided slightly sharper framing ("execution topology"), SE-001 had more precise location. Merged keeping SE-001's location specificity and SA-001's description framing. Severity: critical from both — no adjudication needed.

**SE-002 + SA-002 → F-002 (high, HIGH confidence)**
Both found the dangling Section 6 reference. SE-002 was more precise on location ("final sentence"). Kept SE-002 location, merged evidence. Severity: high from both.

**SE-003 → F-011 (low, MEDIUM confidence)**
Enumerator-only finding. Evidence is present and specific. Authentication type gap is a real completeness issue in a final architecture doc. Severity downgraded from consideration of its low practical consequence vs. the low baseline — kept at low. Retained.

**SA-003 → F-007 (medium, MEDIUM confidence)**
Adversary-only finding about future/current streaming scope tension. The evidence is internally coherent: Conclusions describes streaming as future while Stage 2 describes it as current. This is a genuine structural_validity issue (scope contradiction between sections), not a stylistic concern. Retained at medium.

**SA-HAL-001 → DISCARDED**
Self-defeating finding: the evidence field states "no such text exists in Stage 3" while the description claims Stage 3 references SLA targets. The finding's own evidence refutes its claim. Discarded as hallucination. Fixture notes confirm this was the planted hallucination for consolidator testing.

### Accuracy lens (AE-* / AA-*)

**AE-001 + AA-001 → F-003 (high, HIGH confidence)**
Both found the inverted batch/streaming claim. Both correctly identified the domain knowledge basis (batch setup overhead disadvantages batch at small sizes). AA-001 was marginally more precise in articulating the mechanism. Merged using AA-001's description with AE-001's evidence framing. Severity: high from both.

**AE-002 + AA-002 → F-004 (high, HIGH confidence)**
Both found the 99.9% latency reduction claim as unsupported. Descriptions were nearly identical. Merged. Severity: high from both.

**AE-003 + AA-003 → F-005 (medium, HIGH confidence)**
Both found the unattributed benchmark claim. This is treated as a separate finding from F-003 (which addresses the factual inversion of the same claim): correctness and traceability are distinct dimensions. A claim can be both factually wrong AND unattributed — both issues need to be fixed independently. Retained as a separate medium finding.

**AE-004 → F-006 (medium, MEDIUM confidence)**
Enumerator-only logical soundness finding. The cross-section contradiction (5-minute polling vs. sub-second latency) is logically sound: you cannot have sub-second delivery SLAs when your health polling granularity is 5 minutes. The evidence is concrete and the reasoning is valid. Retained at medium.

Note: F-006 involves the same latency claim as F-004 but is a different type of finding — F-004 is about the claim being unsupported; F-006 is about a cross-section logical contradiction. Both are legitimate, distinct issues.

### Coherence lens (CE-* / CA-*)

**CE-001 + CA-001 → F-008 (medium, HIGH confidence)**
Both found pipeline/workflow terminology drift. CA-001 framed it more holistically ("never settles on which term means what"). Merged using CA-001's description framing with CE-001's location specifics. Severity: medium from both.

**CE-002 + CA-002 → F-009 (medium, HIGH confidence)**
Both found the undefined "standard retry policy." Descriptions nearly identical. Merged. Severity: medium from both.

**CE-003 → F-010 (medium, MEDIUM confidence)**
Enumerator-only. "Large files" threshold is genuinely undefined — a concrete, actionable gap in a final architecture document. Evidence is specific. Retained at medium.

**CE-004 + CA-003 → F-012 (low, HIGH confidence)**
Both found ETL unexpanded. Minor clarity issue but confirmed by both reviewers. Retained at low.

**CA-004 → F-013 (low, MEDIUM confidence)**
Adversary-only. Prometheus dashboard duplication between Stage 4 and Operational Notes is a real conciseness issue with concrete evidence. Retained at low.

---

## Hallucinations Filtered

**1 hallucination removed:** SA-HAL-001

The finding claimed Stage 3 mentions SLA targets contradicted by the Performance Characteristics section. However, the evidence field of the finding itself states: "Stage 3 mentions SLA targets — no such text exists in Stage 3." This is a self-refuting finding — the validator asserted something exists and then acknowledged in the evidence that it does not. Classic validator hallucination pattern: the validator generated a plausible-sounding cross-section contradiction but could not produce real evidence because the text does not exist.

---

## Cross-Check Conflicts

No direct severity conflicts between Enumerator and Adversary pairs. Where both found the same issue, both assigned the same severity in every case. No adjudication required on severity.

One framing difference noted: SA-003 (future/current streaming scope, medium) touches similar territory to CE-001/CA-001 (pipeline/workflow terminology drift) in that both involve inconsistent scope language in the Conclusions section. These are distinct issues: SA-003 is about contradictory capability claims (has streaming vs. will add streaming); CE-001/CA-001 is about undefined terminology. Both retained.

---

## Scoring Summary

| Severity | Count | Weight | Deduction |
|---|---|---|---|
| critical | 1 | -15 | -15 |
| high | 3 | -8 | -24 |
| medium | 6 | -3 | -18 |
| low | 3 | -1 | -3 |
| **Total** | **13** | | **-60** |

**Score: 100 - 60 = 40**
**Grade: Failing — major rework needed**
**Result: continue** (score < 95; fix loop proceeds)

The document has a critical structural contradiction (parallel vs. sequential execution), three high-severity issues (dangling reference, inverted performance claim, unsupported latency claim), and six medium issues. The critical finding alone (F-001) represents a fundamental architectural ambiguity that makes the document unusable as a specification. The high-severity correctness issues compound this significantly.
