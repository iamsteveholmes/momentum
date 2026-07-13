---
title: Architecture Decision 26 update for base-body collapse
story_key: architecture-decision-26-update-for-base-body-collapse
status: ready-for-dev
epic_slug: momentum-agent-role-contracts
feature_slug: momentum-composable-specialist-agents
story_type: maintenance
priority: medium
change_type:
  - specification
verification_method_advisory: document-review
depends_on:
  - base-body-collapse-rollback
touches:
  - _bmad-output/planning-artifacts/architecture.md
---

# Architecture Decision 26 update for base-body collapse

## Story

As a developer,
I want architecture.md updated so Decision 26 (Two-Layer Agent Model), the Repository Structure listings, and the Decision 55 ARCH-3 note all reflect the base-body collapse,
so that the architecture record matches the shipped implementation and cannot re-seed the removed pre-shipped-specialist pattern.

## Description

After the `base-body-collapse-rollback` sibling removes the pre-shipped `dev-frontend` / `dev-build` / `dev-skills` specialist bodies and retires the `specialist-classify → pre-shipped body` path, `architecture.md` still documents the old model in several places. This story updates every one of them so the document is consistent with the collapsed, routing-table-only model. It is step (3) of the sequence recorded in architecture.md Decision 55 ARCH-3: (1) architect-guard ships, (2) the collapse runs, **(3) this story updates the architecture docs**, then (4) constitution-builder and agent-builder follow. Hence the `depends_on: base-body-collapse-rollback` — the doc records a collapse that must already have landed.

This is a pure document-review change to a single file (`architecture.md`). It writes no code and edits no other artifact.

**Scope boundary (sibling coherence):** This story owns **all** `architecture.md` edits related to the collapse. The `base-body-collapse-rollback` sibling deliberately excludes architecture.md (it updates skills/workflows/tools/evals only), so the two never edit the same file. Under the **default naming outcome** of the `rename-base-body-files-to-canonical-naming` sibling (Option A — descriptive names stay canonical), the Decision 55 canonical-9 **role-name list is unchanged**, so this story does **not** edit those role names and does **not** depend on the rename sibling. (Only if the developer selects the rename sibling's Option B — short names — would the Decision 55 role-name edit move here and a `depends_on: rename-base-body-files-to-canonical-naming` edge be added. Default: no such edge.)

## Acceptance Criteria

1. architecture.md **Decision 26** no longer presents the specialist classification table (`dev-skills`, `dev-build`, `dev-frontend`, `dev base`) as a canonical lookup for pre-shipped specialist bodies. The paragraph at ~line 2169 is rewritten to state that specialist resolution is performed by `momentum-tools agent resolve` against `momentum/agents.json`, with composed specialists located at `.claude/guidelines/agents/{role}-{domain}.md` (per Decision 55 / DEC-023 and Decision 56 / DEC-026).
2. The three **Repository Structure** directory listings in architecture.md (~lines 345-347, ~1230-1232, ~2304-2306) no longer list `dev-skills.md`, `dev-build.md`, or `dev-frontend.md` as shipped `agents/` files. Only `dev.md` (and the other surviving base bodies) remain in those listings.
3. The **Decision 55 ARCH-3 note** (~line 3012) is updated to record `base-body-collapse-rollback` as **completed** (the pre-shipped specialist bodies have been removed and specialist resolution is routing-table-only), rather than describing it as a future backlog action ("will REMOVE…"). The four-step sequence framing is preserved with step (2) marked done.
4. The **Decision 26 "Two-Layer Agent Model" description** accurately reflects the shipped composed model — base body + project conditioning (constitution + manifesto) with composed specialists in `.claude/guidelines/agents/` — and is internally consistent with Decision 55 (routing table) and Decision 56 (agent-builder pipeline). It no longer implies pre-shipped dev specialists are the specialization mechanism.
5. No other architecture decision contradicts the updated Decision 26. A consistency sweep of architecture.md for `specialist-classify`, "specialist classification", and "canonical lookup" confirms every surviving mention is either reconciled with the routing-table model or annotated as historical/superseded (matching the document's existing supersession-annotation style).

## Tasks / Subtasks

- [ ] **Rewrite the Decision 26 specialist-lookup paragraph** (AC1, AC4)
  - [ ] Replace the "specialist classification table … is a canonical lookup / `momentum-tools specialist-classify` is the deterministic implementation" paragraph (~line 2169) with the routing-table + composed-specialist model
  - [ ] Update the Decision 26 statement / "Two-Layer Agent Model" description to reflect the composed (base body + constitution + manifesto) model
- [ ] **Update the Repository Structure listings** (AC2)
  - [ ] Remove `dev-skills.md`, `dev-build.md`, `dev-frontend.md` from all three `agents/` directory trees (~345-347, ~1230-1232, ~2304-2306)
- [ ] **Update the Decision 55 ARCH-3 note** (AC3)
  - [ ] Change `base-body-collapse-rollback` from future ("will REMOVE…") to completed; keep the four-step sequence with step (2) done
- [ ] **Consistency sweep** (AC5)
  - [ ] Grep architecture.md for `specialist-classify`, "specialist classification", "canonical lookup"; reconcile or annotate each surviving mention

## Dev Notes

### Decision Authority

- **Decision 55 / DEC-023 (ARCH-3, ~line 3010):** authoritative sequencing — this story is step (3), after the collapse. Establishes `momentum-tools agent resolve` against `momentum/agents.json` as the canonical specialist-resolution mechanism.
- **Decision 56 / DEC-026 (~line 3040):** composed specialists at `.claude/guidelines/agents/{role}-{domain}.md`, written by agent-builder into `momentum/agents.json` `project`. This is the specialization mechanism Decision 26 must now point to.
- **`base-body-collapse-rollback` sibling:** the code/skill/tool change this story documents. This story must run after it (dependency).

### Current State of Affected Sections (grepped 2026-07-13)

- Decision 26 statement: ~line 2166-2167 ("Two-Layer Agent Model" — generic roles + project guidelines).
- Specialist-lookup paragraph: ~line 2169 ("The specialist classification table (dev-skills, dev-build, dev-frontend, dev base) is a **canonical lookup** … `momentum-tools specialist-classify` is the deterministic implementation …").
- Repository Structure `agents/` trees listing the three specialist files: ~345-347, ~1230-1232, ~2304-2306.
- Decision 55 ARCH-3 note describing the collapse as future backlog: ~line 3012.

### Architecture Compliance

- This is the authoritative record; after this story, architecture.md must describe exactly one specialist spawn path (routing table) and one specialization location (composed `.claude/guidelines/agents/`).
- Annotate rather than delete historical decision text where the document's convention is to annotate supersessions (e.g., the existing "REVISED"/"superseded" inline notes). Preserve traceability.
- Large-file protocol: architecture.md is large — Grep/chunk to locate each edit site; never full-read it.

### Testing Requirements

Primary verification method (advisory): **document-review** — this is a pure `specification` story with no executable surface. Verification is by inspection and cross-reference:

- Confirm each AC's target section reads consistently with Decision 55 (routing table) and Decision 56 (composed specialists).
- Grep gate (AC2): the three Repository Structure trees no longer contain `dev-skills.md`/`dev-build.md`/`dev-frontend.md`.
- Grep gate (AC5): the full three-term sweep — `specialist-classify`, "specialist classification", and "canonical lookup" — finds no surviving mention that contradicts the collapsed model.

### Implementation Guide

- **specification (document-review):** direct authoring with cross-reference verification. Each rewritten passage cites the governing decision (55 / 56). Do not introduce new decisions — this records an already-ratified collapse.
- A frozen verification contract exists for this sprint at `sprints/{sprint-slug}/specs/{story-slug}.{ext}`; read the Part-A header as a self-check before signaling done.

### Project Structure Notes

- Single file touched: `_bmad-output/planning-artifacts/architecture.md`. No code, no schema, no other doc.

### References

- **Sibling — `base-body-collapse-rollback` (this story's `depends_on`):** the collapse this story documents; must land first. This story is the *only* place architecture.md is edited for the collapse.
- **Sibling — `rename-base-body-files-to-canonical-naming`:** owns base-body filenames + the DEC-020 naming annotation. Under its default (Option A) the Decision 55 canonical-9 role names are unchanged, so this story does not touch them and holds no edge to the rename story; only its Option B would move that edit here.
- **Architecture edit sites:** `_bmad-output/planning-artifacts/architecture.md` — Decision 26 (~2166-2169), Repository Structure (~345-347, ~1230-1232, ~2304-2306), Decision 55 ARCH-3 (~3012).
- **Governing decisions:** Decision 55 / DEC-023 (routing table), Decision 56 / DEC-026 (composed specialists).
- Epic context: `momentum-agent-role-contracts` (from _bmad-output/planning-artifacts/epics.json)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
