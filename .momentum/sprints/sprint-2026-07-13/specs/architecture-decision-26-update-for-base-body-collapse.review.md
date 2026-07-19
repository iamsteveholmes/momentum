# === VERIFICATION HEADER (Part A) ===
---
story_slug: architecture-decision-26-update-for-base-body-collapse
verification_method: document-review
harness_profile: document-review
contract_path: .momentum/sprints/sprint-2026-07-13/specs/architecture-decision-26-update-for-base-body-collapse.review.md
how_dev_self_checks: |
  Open the architecture document and read the Decision 26 entry, every Repository
  Structure directory listing, and the decision-log note that tracks the base-body
  collapse. Confirm: Decision 26 describes specialist resolution as a routing-table
  lookup rather than a classification-table canonical lookup; none of the Repository
  Structure listings still show the retired specialist body files; the collapse note
  reads as completed rather than a future action; the Two-Layer Agent Model
  description is internally consistent with the routing-table and composed-specialist
  decisions; and a text search of the document for the old classification/canonical-
  lookup language turns up only mentions that are either reconciled with the new
  model or clearly annotated as historical/superseded in the document's existing
  style.
coverage_disposition: dedicated-run
covered_by_scenario: null
acceptance_criteria_ref: .momentum/stories/architecture-decision-26-update-for-base-body-collapse.md#acceptance-criteria
platforms: [host]
---

# architecture-decision-26-update-for-base-body-collapse — Document Review Contract

**Harness Profile:** document-review

## Document Under Review

`_bmad-output/planning-artifacts/architecture.md` — the project's published architecture
decision record. This is the authoritative, versioned document that any developer or
reviewer can open directly to inspect the current state of architectural decisions; no
source-code access is required to review it.

## Required Claims

- [ ] The document's **Decision 26** entry no longer presents a specialist
      classification table (grouping the retired pre-shipped specialist roles) as a
      canonical lookup for resolving specialist bodies. It instead states that
      specialist resolution is performed as a routing-table lookup against the
      project's agent registry, with composed specialists located at a per-role path
      under the project's guidelines directory.
- [ ] Every **Repository Structure** directory listing in the document that
      previously included the retired specialist body files no longer lists them.
      Only the surviving base body file(s) remain in those listings.
- [ ] The decision-log note that tracks the base-body collapse now describes the
      collapse as **completed** rather than a pending or future action, while still
      preserving the document's existing multi-step sequence framing (with the
      collapse step marked done).
- [ ] The **Decision 26 "Two-Layer Agent Model"** description accurately describes
      the shipped composed model — a shared base body plus project-specific
      conditioning, with composed specialists in the per-role project-guidelines
      location — and is internally consistent with the document's routing-table and
      composed-specialist-pipeline decisions. It no longer implies that pre-shipped
      dev specialist bodies are the specialization mechanism.
- [ ] No surviving passage anywhere else in the document contradicts the updated
      Decision 26. Every remaining mention of the old specialist-classification /
      canonical-lookup pattern is either reconciled with the routing-table model or
      clearly annotated as historical/superseded, consistent with the document's
      existing convention for annotating superseded decisions.

## Required Sections

- [ ] A "Decision 26" entry in the document's decision log describing specialist
      resolution and the Two-Layer Agent Model.
- [ ] The Repository Structure directory-listing section(s) documenting the shipped
      `agents/` files — this document contains more than one such listing, and all
      of them must be checked.
- [ ] A decision-log entry recording the status (completed vs. pending) of the
      base-body-collapse action.
- [ ] Cross-references between Decision 26 and the document's routing-table and
      composed-specialist-pipeline decisions resolve without contradiction.

## Pass Criteria

A reviewer opens the architecture document and reads the Decision 26 entry, all
Repository Structure listings, and the base-body-collapse decision-log note. The
review passes when all five Required Claims above hold as read: no classification-
table language remains as a canonical mechanism; every Repository Structure listing
is free of the retired specialist files; the collapse is described as completed; the
Two-Layer Agent Model description reads consistently with the document's other
decisions; and a full-text search of the document for the retired classification /
canonical-lookup terminology returns no unreconciled, unannotated mentions.

## Fail Criteria

Any one of the following fails the review:

- Decision 26 still describes or implies a classification-table canonical lookup for
  resolving pre-shipped specialist bodies.
- Any Repository Structure listing still includes one or more of the retired
  specialist body files.
- The base-body-collapse decision-log note still describes the collapse as a
  future or pending action rather than completed.
- The Decision 26 description conflicts with the routing-table or
  composed-specialist-pipeline decisions, or still implies pre-shipped dev
  specialists are the specialization mechanism.
- A text search of the document turns up any mention of the old
  specialist-classification / canonical-lookup pattern that is neither reconciled
  with the new model nor annotated as historical/superseded.
