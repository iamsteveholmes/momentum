---
title: Rename base body files to canonical naming
story_key: rename-base-body-files-to-canonical-naming
status: ready-for-dev
epic_slug: momentum-agent-role-contracts
feature_slug: momentum-composable-specialist-agents
story_type: maintenance
priority: medium
change_type:
  - agent-definition
  - specification
verification_method_advisory: skill-invoke
depends_on:
  - base-body-collapse-rollback
touches:
  - _bmad-output/planning-artifacts/decisions/dec-020-universal-agent-role-taxonomy-2026-05-16.md
---

# Rename base body files to canonical naming

## Story

As a developer,
I want every surviving plugin-shipped base-body file under `skills/momentum/agents/` to be named consistently with the authoritative canonical role taxonomy, and the decision record that seeded a conflicting short-name variant to be reconciled,
so that there is exactly one canonical filename per role and no decision doc contradicts the shipped naming.

## Description

This story reconciles base-body file naming with the **authoritative canonical role taxonomy**, operating on the base bodies that survive the `base-body-collapse-rollback` sibling (hence the dependency).

**Key finding surfaced during enrichment (see `## Open Decision` below).** The original stub proposed renaming `qa-reviewer.md → qa.md` and `e2e-validator.md → e2e.md` (short role names). That short-name scheme originates in DEC-020 D1 (`architect, pm, ux, analyst, researcher, dev, sm, qa, e2e`). It was **not** the scheme the system actually shipped. Every authoritative, currently-live source uses the **descriptive** names `qa-reviewer` and `e2e-validator`:

- `momentum/agents.json` `defaults` keys are `qa-reviewer` and `e2e-validator`.
- Every call site resolves `--role qa-reviewer` / `--role e2e-validator` (sprint-dev, conductor, `momentum-tools.py`, agent-resolve evals).
- architecture.md Decision 55 / DEC-023 canonical-9 lists `dev, qa-reviewer, e2e-validator, architect-guard, ux, analyst, researcher, constitution-builder, agent-builder`.
- The epic (`momentum-agent-role-contracts`) description names "`qa-reviewer`".

Under that authoritative naming, the six surviving base bodies (`dev.md`, `qa-reviewer.md`, `e2e-validator.md`, `ux.md`, `analyst.md`, `researcher.md`) **already conform** — a rename to `qa.md`/`e2e.md` would move *away* from canonical and would require flipping the `agents.json` keys, ~10 call sites, evals, the epic text, and Decision 55.

The **default scope** of this story (Option A, recommended) is therefore: (1) verify conformance of every surviving base-body filename to its `agents.json` `defaults` role key, and (2) annotate DEC-020 D1 to record that its short-name variants were superseded by the shipped descriptive taxonomy — closing the only genuine naming contradiction in the record. The alternative (Option B: actually adopt short names) is a larger taxonomy-flip and is presented as a planning-gate fork, not silently chosen.

**Scope boundary (sibling coherence):** This story's reference set (`qa-reviewer` / `e2e-validator`) is **disjoint** from the `base-body-collapse-rollback` sibling's set (`dev-frontend` / `dev-build` / `dev-skills`). This story does **NOT** edit `architecture.md` — the `architecture-decision-26-update-for-base-body-collapse` sibling owns all architecture.md edits, including any change to the Decision 55 canonical-9 list. If (and only if) the developer selects Option B at the gate, the Decision 55 list change is handed to that sibling and a `depends_on` edge from that sibling to this one is added; under the default Option A, no such edge exists.

## Acceptance Criteria

_These ACs specify the **default (Option A)** scope. If the developer selects **Option B** at the planning gate, re-scope per `## Open Decision`. If the developer selects **Defer**, AC3 (the DEC-020 annotation) is waived and the story closes on AC1/AC2/AC4 (verification-only)._

1. Every surviving plugin-shipped base body under `skills/momentum/agents/` has a filename equal to its canonical role identity: for each key `K` in `momentum/agents.json` `defaults` (`dev`, `qa-reviewer`, `e2e-validator`, `ux`, `analyst`, `researcher`), the file `skills/momentum/agents/{K}.md` exists, and every `*.md` base body in that directory maps to exactly one `defaults` key (no orphan base body, no role key without a file).
2. `momentum-tools agent resolve --role <role>` for each `defaults` role returns the correspondingly-named surviving base-body path (no dead or mismatched path). Verified for at least `qa-reviewer` and `e2e-validator`.
3. DEC-020 (`_bmad-output/planning-artifacts/decisions/dec-020-universal-agent-role-taxonomy-2026-05-16.md`) D1 carries an annotation recording that its short-name role variants `qa` and `e2e` were superseded by the shipped descriptive names `qa-reviewer` and `e2e-validator` (per Decision 55 / DEC-023), so the decision record no longer contradicts the shipped taxonomy. The annotation follows the same supersession-annotation style already used elsewhere in the planning artifacts.
4. If any surviving base-body filename is found to diverge from its `defaults` role key, it is renamed to the canonical role key and every reference to the old filename is updated (expected count as of enrichment: **0** — the ACs above are verified to already hold; any nonzero drift discovered is reconciled here).

## Tasks / Subtasks

- [ ] **PRE-REQ GATE — Planning-gate fork** — before any other task, confirm Option A / Option B / Defer with the developer (see `## Open Decision`). This gate selects which ACs are in scope and MUST be resolved first.
- [ ] **Verify base-body naming conformance** (AC1, AC2)
  - [ ] For each `momentum/agents.json` `defaults` key, confirm `skills/momentum/agents/{key}.md` exists; confirm no orphan `*.md` base body lacks a matching key (evals/ subdir excluded)
  - [ ] Run `momentum-tools agent resolve --role qa-reviewer` and `--role e2e-validator`; confirm each returns its descriptively-named path
- [ ] **Reconcile the DEC-020 naming contradiction** (AC3) — _skipped under Defer_
  - [ ] Annotate DEC-020 D1: `qa` → `qa-reviewer`, `e2e` → `e2e-validator` superseded by Decision 55 / DEC-023 shipped taxonomy
- [ ] **Reconcile any discovered drift** (AC4)
  - [ ] If AC1/AC2 fail for any file, rename to the canonical role key and update all references (grep-driven); otherwise record "0 drift — conformance confirmed"

## Open Decision — Naming scheme fork (surface at planning gate)

**What:** Which naming scheme is canonical for the survivor base bodies — descriptive (`qa-reviewer.md`, `e2e-validator.md`) or short (`qa.md`, `e2e.md`)?

**Why it matters:** It determines whether this story is a verify-and-annotate reconciliation (Option A) or a taxonomy-wide rename touching the routing table keys, ~10 call sites, evals, the epic description, and architecture.md Decision 55 (Option B). Picking wrong either leaves a decision-record contradiction unresolved or churns the entire live routing surface.

**Evidence:** `agents.json` `defaults` keys, all `--role qa-reviewer`/`--role e2e-validator` call sites (sprint-dev/workflow.md:52,54,93,96,621,634; conductor/workflow.md:2077; momentum-tools.py:22; agent-resolve evals), the `momentum-agent-role-contracts` epic description, and architecture.md Decision 55 canonical-9 all use the **descriptive** names. The short form (`qa`/`e2e`) appears only in **doc-only** sources with **no functional call site**: DEC-020 D1 (and the original stub), plus `skills/momentum/references/sprint-tracking-schema.md:106` — whose `roles` row lists `dev`, `qa`, `e2e-validator`, `architect-guard`, itself internally inconsistent (short `qa` alongside long `e2e-validator`). The six surviving base bodies already match the descriptive names.

**Recommendation (default): Option A — descriptive naming is canonical.** The entire live system already uses it; the files already conform. Do the verification (AC1/AC2) and annotate DEC-020 (AC3). This is the enriched default scope.

**Options:**
- **A (recommended):** Keep descriptive names. This story = verify conformance + annotate DEC-020. No file renames, no call-site churn, no architecture.md change, no new sibling edge.
- **B:** Adopt short names (`qa.md`, `e2e.md`). Re-scope this story to: rename both files; flip `agents.json` `defaults` keys; update ~10 `--role` call sites + evals; update the epic description; hand the Decision 55 canonical-9 edit to the `architecture-decision-26-update-for-base-body-collapse` sibling and add a `depends_on` edge from that sibling to this one.
- **Defer:** If naming is not worth touching now, close this story as already-satisfied under Option A (files conform) and leave DEC-020 annotation to a future doc-hygiene pass.

## Dev Notes

### Decision Authority

- **architecture.md Decision 55 / DEC-023 (canonical-9, ~line 3012):** authoritative role list uses descriptive `qa-reviewer` / `e2e-validator`; `agents.json` `defaults` keys mirror it.
- **DEC-020 D1 (universal role taxonomy):** the source of the short-name variant (`qa`, `e2e`); superseded on naming by the shipped taxonomy. This story annotates it (AC3).
- **DEC-026 / Decision 56:** composed specialists live at `.claude/guidelines/agents/{role}-{domain}.md`; base bodies are the plugin-shipped role contracts this story keeps canonically named.

### Current State of Affected Files

- `skills/momentum/agents/` base bodies (post-collapse survivors): `analyst.md`, `dev.md`, `e2e-validator.md`, `qa-reviewer.md`, `researcher.md`, `ux.md`. All six already match their `agents.json` `defaults` role keys.
- `momentum/agents.json` `defaults`: `ux`, `analyst`, `researcher`, `dev`, `qa-reviewer`, `e2e-validator` → each points at `skills/momentum/agents/{key}.md`.
- DEC-020 D1 lists nine roles with short names including `qa`, `e2e` — the contradiction AC3 reconciles.
- **`touches` scope:** the only file guaranteed to be modified under the Option A default is the DEC-020 decision doc (AC3), so it is the sole `touches` entry. The six base bodies are in AC1's verification scope but are **read-only** under the default — they enter `touches` only under AC4 drift or Option B (then: the affected base bodies + `momentum/agents.json` `defaults` keys + `--role` call sites). `skills/momentum/references/sprint-tracking-schema.md:106` (the `roles` row) is a doc-only naming-drift site touched only under Option B — distinct from that file's line ~112 `specialist` enum, which the `base-body-collapse-rollback` sibling owns; the two lines/concerns never collide.

### Architecture Compliance

- Canonical rule: one base body per role, filename = the `agents.json` `defaults` role key. This story enforces/verifies that invariant; it does not invent a new scheme.
- **Do not** edit `architecture.md` in this story (sibling-owned). Editing agent-definition files or workflow references (only if drift is found under AC4) follows the `dev-skills` rule — `skills/momentum/references/agent-skill-development-guide.md`.

### Testing Requirements

Primary verification method (advisory): **skill-invoke** — the primary deliverable domain is agent base-body definitions, verified by resolving each role through `momentum-tools agent resolve` and observing the canonical filename is returned. Supplementary: grep-based conformance check (every `defaults` key has a matching file; no orphan base body) and inspection of the DEC-020 annotation (document-review for the specification portion).

### Implementation Guide

- **agent-definition (base-body files):** the default path is verification, not modification. Only under discovered drift (AC4) does a rename + reference sweep occur; then EDD-verify each resolution via agent-resolve.
- **specification (DEC-020 annotation):** direct authoring with cross-reference verification — the annotation must name Decision 55 / DEC-023 as the superseding authority and must not alter DEC-020's historical decision text (annotate, don't rewrite).
- A frozen verification contract exists for this sprint at `sprints/{sprint-slug}/specs/{story-slug}.{ext}`; read the Part-A header as a self-check before signaling done.

### Project Structure Notes

- Base bodies: `skills/momentum/agents/{role}.md` (role = `agents.json` `defaults` key). Composed specialists (not in scope): `.claude/guidelines/agents/{role}-{domain}.md`.

### References

- **Sibling — `base-body-collapse-rollback` (this story's `depends_on`):** removes the `dev-*` specialist bodies; this story operates on the survivors afterward. Disjoint reference set (never touches `qa-reviewer`/`e2e-validator`).
- **Sibling — `architecture-decision-26-update-for-base-body-collapse`:** owns all `architecture.md` edits, including the Decision 55 canonical-9 list. Under Option B only, that sibling would take the Decision 55 rename and gain a `depends_on` edge to this story.
- **Naming evidence:** `momentum/agents.json` `defaults`; `--role` call sites — `skills/momentum/skills/sprint-dev/workflow.md` (52, 54, 93, 96, 621, 634), `skills/momentum/skills/conductor/workflow.md` (2077), `skills/momentum/scripts/momentum-tools.py` (22), `skills/momentum/agents/evals/eval-agent-resolve-defaults-fallback.md`.
- **Decisions:** `_bmad-output/planning-artifacts/decisions/dec-020-universal-agent-role-taxonomy-2026-05-16.md` (D1, short names — annotate); architecture.md Decision 55 / DEC-023 (~line 3012, descriptive canonical-9).
- Epic context: `momentum-agent-role-contracts` (from _bmad-output/planning-artifacts/epics.json)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
