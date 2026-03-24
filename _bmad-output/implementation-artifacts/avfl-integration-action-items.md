---
title: AVFL Integration — Future Action Items
created: '2026-03-23'
source: AVFL integration plan session
status: open
derives_from:
  - id: PRD-MOMENTUM-001
    path: _bmad-output/planning-artifacts/prd.md
    relationship: derives_from
  - id: EPICS-MOMENTUM-001
    path: _bmad-output/planning-artifacts/epics.md
    relationship: derives_from
---

# AVFL Integration — Future Action Items

These action items identify where AVFL (Adversarial Validate-Fix Loop) should be integrated into Momentum workflows beyond its current deployment in `momentum-dev` Step 7 (story changeset validation). Each item is a candidate for a future story or epic enhancement.

---

## AI-1: Spec Validation at Story Creation Time

**Target:** Epic 2/4 enhancement (momentum-create-story skill)
**Profile:** `gate` (fast, structural only)
**Rationale:** When momentum-create-story produces a story file, running AVFL gate profile catches structural gaps (missing ACs, incomplete derives_from, broken references) before development begins. Currently, structural issues in stories are caught during development or code review — too late in the cycle.
**Implementation sketch:** Add a step to momentum-create-story that invokes `momentum-avfl` with `profile: gate`, `stage: final`, `domain_expert: "practice engineer"`, `source_material: [epic ACs for this story]`.

---

## AI-2: Research Validation

**Target:** Epic 8 (Story 8.1 — Multi-Model Research Workflow)
**Profile:** `checkpoint` after initial consolidation, `full` on final deliverable
**Rationale:** The PRD already mentions "full VFL validation after consolidation" for research (Growth Features). Research artifacts are high-hallucination-risk — multi-model cross-validation reduces but does not eliminate fabrication. AVFL's Factual Accuracy lens with source_material cross-checking is specifically designed for this.
**Implementation sketch:** Two-pass validation: (1) `checkpoint` profile after initial provider consolidation (catches factual errors before synthesis), (2) `full` profile on final research document (catches synthesis-introduced coherence and accuracy issues). Ensure Story 8.1 ACs explicitly reference AVFL invocation.

---

## AI-3: Spec Cascade Validation

**Target:** Cross-epic enhancement (provenance infrastructure + AVFL)
**Profile:** `checkpoint`
**Rationale:** When upstream spec changes (PRD, architecture), provenance infrastructure (Epic 5) flags downstream documents as SUSPECT via hash-based staleness. But staleness detection only tells you something changed — it doesn't tell you whether the downstream doc is actually wrong. Running AVFL checkpoint on SUSPECT documents with the changed upstream doc as source_material catches propagation failures that provenance alone can't detect.
**Implementation sketch:** When Impetus detects SUSPECT downstream documents during session orientation (Story 5.3), offer to run `momentum-avfl` with `profile: checkpoint`, `source_material: [changed upstream doc]`, `output_to_validate: [SUSPECT downstream doc]`. This is advisory — developer decides whether to validate.

---

## AI-4: Upgrade Validation

**Target:** Epic 1 enhancement (Story 1.4 — Momentum Detects and Applies Upgrades)
**Profile:** `gate`
**Rationale:** When Impetus applies version upgrades (writing new rules, updating hooks config, modifying settings), AVFL gate profile on the changed files catches broken upgrades (malformed JSON, missing required fields, broken references) before they affect the user's environment.
**Implementation sketch:** After Impetus applies upgrade actions in Story 1.4, run `momentum-avfl` with `profile: gate`, `stage: final`, `output_to_validate: [diff of all changed files]`. If GATE_FAILED, roll back the upgrade and report the issue. This adds a safety net to the upgrade path.

---

## AI-5: Retrospective Validation

**Target:** Epic 6 enhancement (Story 6.5 — Practice Health Metric)
**Profile:** `checkpoint`
**Rationale:** Retrospective outputs include claims about practice health metrics, pattern detection results, and fix-level classifications. These claims should be verifiable against the findings ledger data they summarize. Running AVFL checkpoint catches unsupported claims (e.g., "upstream fix ratio improved 20%" when the ledger data shows 15%), incorrect pattern attribution, and missing context.
**Implementation sketch:** Before Impetus contributes retrospective input (Story 6.5), run `momentum-avfl` with `profile: checkpoint`, `source_material: [relevant findings-ledger.jsonl entries]`, `output_to_validate: [retrospective summary]`, `domain_expert: "practice engineer"`.
