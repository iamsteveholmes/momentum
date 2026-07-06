---
title: "Companion surface — sync project rule + wire bulk-derivation paths to template"
story_key: companion-surface-rule-sync-and-bulk-derivation
status: ready-for-dev
epic_slug: momentum-impetus-experience
feature_slug:
story_type: practice
priority: medium
depends_on: []
change_type:
  - skill-instruction
  - rule-hook
verification_method_advisory: skill-invoke
touches:
  - .claude/rules/decision-grade-presentation.md
  - skills/momentum/skills/intake/
---

# Companion surface — sync project rule + wire bulk-derivation paths to template

## Story

As the developer (the practice owner),
I want the **project-tier** decision-grade-presentation rule brought up to the global/canonical
version (Companion-Surface Obligation + presentation-form leg), and the bulk-derivation paths
(`intake` / ad-hoc plan workflows) wired to emit the companion surface from the shipped template,
so that every tier enforces what the standard now mandates and no review-document path silently
escapes the companion-surface obligation.

## Description

Part A of the parent story (extend the standard) was **delivered** on branch
`feat/companion-decision-surface-standard` (commit `da70fed`): the canonical rule
`skills/momentum/references/rules/decision-grade-presentation.md` gained §5
(Companion-Surface Obligation), §5.1 (presentation-form leg), §2.2 row 9, and the
`skills/momentum/references/templates/companion-decision-surface.html` template. This story is
the **remainder** — propagation in two parts:

1. **Project-rule drift.** The project copy `.claude/rules/decision-grade-presentation.md` is
   **stale** — it stops at the 8-surface schema table and carries no Companion-Surface
   Obligation, no presentation-form leg, and no §2.2 row 9. Its section numbering is one behind
   canonical (project §5 "Named Output Surfaces" = canonical §6). The project tier therefore
   silently under-enforces what global now requires. Sync it to the canonical version (project
   scope may tighten a cap but not loosen one, and cannot drop the non-overridable legs).
2. **Bulk-derivation wiring.** Wire the bulk-derivation paths under
   `skills/momentum/skills/intake/` (the `intake` / ad-hoc plan workflows) that emit a review
   document exceeding the Decision-card budget to **also** emit the paired companion decision
   surface, derived from `skills/momentum/references/templates/companion-decision-surface.html`
   — so a large review document is never handed over without its decision surface (the §5
   defect this closes).

**Parent / provenance:** `visual-hitl-gates-presentation-form-standard-leg` (Part A remainder);
delivered foundation in `da70fed` (canonical rule §5/§5.1 + template); stale target
`.claude/rules/decision-grade-presentation.md`.

## Acceptance Criteria

1. **Project rule carries the obligation.** `.claude/rules/decision-grade-presentation.md`
   contains the §5 section "The Companion-Surface Obligation — Large Review Documents", the §5.1
   subsection "Presentation form — the third leg (non-overridable)", and the §2.2 "Companion
   decision surface" budget row — matching the canonical
   `skills/momentum/references/rules/decision-grade-presentation.md`.
   *Observable:* `grep -c "Companion-Surface Obligation" .claude/rules/decision-grade-presentation.md`
   returns ≥ 1 (currently 0); `grep -c "Presentation form — the third leg" .claude/rules/decision-grade-presentation.md`
   returns ≥ 1; the §2.2 table contains a row whose first cell reads "Companion decision surface".

2. **No loosening of the non-overridable legs.** The synced project rule's Cascade-Order
   "What cannot be overridden at any lower scope" list includes the **companion-surface
   obligation** bullet and the **presentation-form leg** bullet, alongside the pre-existing
   caps-vs-floor boundary, three-required-fields, and core-convention bullets — matching the
   canonical Cascade-Order section. No cap value in the synced project rule is weaker than its
   canonical counterpart (project scope may only tighten, never loosen).
   *Observable:* the project rule's final "What cannot be overridden" list enumerates ≥ 5
   bullets including the obligation and presentation-form leg; a section-by-section diff of cap
   wording against canonical shows no loosened budget.

3. **Schema + numbering consistent with canonical.** The project rule's "Named Output Surfaces
   and Surface Schema" table includes the three rows "Companion decision surface", "Pre-sprint
   plan gate", and "Post-sprint results gate" (each referencing the §2.2 row-9 budget), and the
   downstream section numbering matches canonical (Companion-Surface Obligation = §5,
   Named Output Surfaces = §6, Cross-References = §7, Cascade Order = §8).
   *Observable:* `grep -c "Pre-sprint plan gate\|Post-sprint results gate" .claude/rules/decision-grade-presentation.md`
   returns ≥ 2; the heading "## 5. The Companion-Surface Obligation" and "## 8. Cascade Order"
   both appear.

4. **Bulk-derivation path emits the companion surface.** *(Applies once a qualifying path is
   confirmed-or-introduced per Task 3; if Task 3 resolves to "no over-budget path in scope", this
   AC is recorded N/A with that justification rather than left unmet.)* A bulk-derivation /
   ad-hoc-plan path under `skills/momentum/skills/intake/` that emits a review document exceeding
   the Decision-card budget (§2.2: > 5 lines of prose + > 3 bullets) **also** emits a companion
   decision surface derived from `skills/momentum/references/templates/companion-decision-surface.html`
   (purpose hero → ✓ verified line → structure → ≤ 7 What/Why/Evidence/Recommendation/Options
   forks → sign-off), with the large document linked as depth-on-demand rather than inlined.
   *Observable:* invoking the wired path on a representative multi-item input produces both the
   review document **and** a paired filled-in HTML companion surface; the surface links (does not
   inline) the large document.

5. **Document-alone is treated as a defect.** The wired workflow text makes the pairing
   **mandatory** — emitting the review document without its companion surface is stated as a
   defect / incomplete state ("has not finished"), not an optional nicety, mirroring §5 of the
   standard.
   *Observable:* the workflow instruction for the wired path states the companion surface is
   mandatory and that emitting the large document alone is a defect; a behavioral eval confirms
   the path is not considered complete after emitting only the large document.

6. **Below-budget path correctly scoped (budget-gated trigger).** The ordinary single-stub
   `intake` capture path — whose output stays under the Decision-card budget — is NOT required to
   emit a companion surface and is NOT flagged as a defect for omitting one. The obligation
   attaches only to review-document emissions that exceed the Decision-card budget.
   *Observable:* a single-item intake capture produces no companion surface and triggers no
   defect; the workflow documents the budget-gated trigger condition.

## Tasks / Subtasks

- [ ] **Task 1 — Sync the project rule body (rule-hook).** (AC1, AC2, AC3) Port the canonical
  `skills/momentum/references/rules/decision-grade-presentation.md` deltas into
  `.claude/rules/decision-grade-presentation.md`: insert the §2.2 "Companion decision surface"
  budget row; insert §5 "The Companion-Surface Obligation — Large Review Documents" and §5.1
  "Presentation form — the third leg (non-overridable)"; renumber the trailing sections
  (Named Output Surfaces → §6 with the three added schema rows: "Companion decision surface",
  "Pre-sprint plan gate", "Post-sprint results gate"; Cross-References → §7; Cascade Order → §8
  with the two added non-overridable bullets). Preserve every existing cap value — tighten only,
  never loosen.
- [ ] **Task 2 — Verify drift closed (rule-hook).** (AC1, AC3) Confirm
  `grep -c "Companion-Surface Obligation"` and `grep -c "Presentation form — the third leg"`
  against the project rule both return ≥ 1 (were 0), the §2.2 "Companion decision surface" row
  is present, and the project rule's section headings now match canonical numbering. Record the
  before/after grep counts in the Dev Agent Record.
- [ ] **Task 3 — Resolve the review-document emission point, including the null result
  (skill-instruction).** (AC4, AC6) Within `skills/momentum/skills/intake/`, determine which
  path(s) emit a review document exceeding the Decision-card budget (a bulk / multi-item plan or
  digest handed to the human for approval) vs. the ordinary single-stub capture that stays under
  budget. **Null-result handling is mandatory — today there is no over-budget path here**, so
  Task 3 must explicitly land on ONE of three resolutions and record it before Tasks 4–5 proceed:
  (A) **a qualifying over-budget path already exists** → wire it (Tasks 4–5 apply as written);
  (B) **the over-budget bulk/ad-hoc-plan capability is to be ADDED under this story** → make that
  scope explicit and design+implement it (Task 4 becomes "build + wire"); or (C) **no over-budget
  emission is in scope for intake** → AC6 is already satisfied by the existing under-budget
  single-stub path, AC4 is recorded N/A with that justification, and the bulk-path wiring is split
  to a follow-up story. Default recommendation is **(C)** pending the developer's call at the
  approval gate (see "Open product fork" in Dev Notes). Document the chosen resolution and the
  budget-gated trigger condition.
- [ ] **Task 4 — Wire the companion surface (skill-instruction).** (AC4, AC5) Wire each
  qualifying path to emit, alongside the review document, a companion decision surface derived
  from `skills/momentum/references/templates/companion-decision-surface.html` (fill placeholders;
  keep the template order; link the large document as depth-on-demand; open in the viewer per the
  HTML-in-viewer convention). Make the pairing mandatory in the workflow text — state that
  emitting the large document alone is a defect ("has not finished").
- [ ] **Task 5 — Scope the below-budget path (skill-instruction).** (AC6) Ensure the ordinary
  single-stub intake capture path is explicitly exempt (output under the Decision-card budget),
  and document the budget gate so the obligation fires only on over-budget review documents.
- [ ] **Task 6 — EDD evals (skill-instruction).** (AC4, AC5, AC6) Write 2–3 behavioral evals in
  `skills/momentum/skills/intake/evals/`: (a) a bulk / plan review-document path emits BOTH the
  document and a template-derived companion surface; (b) a single-stub capture emits no companion
  surface and is not flagged as a defect. Run the EDD cycle until behaviors are confirmed (max 3
  cycles; surface to the developer if still failing).

## Dev Notes

### Decision Authority

The authoritative source of truth for the rule sync is the canonical rule
`skills/momentum/references/rules/decision-grade-presentation.md` (§5, §5.1, §2.2 row 9, §6
schema rows, §8 cascade bullets). The project rule must become a faithful copy of the canonical
content — project scope MAY tighten a cap but MUST NOT loosen one, and MUST NOT drop any
non-overridable leg. The companion-surface obligation (§5) and presentation-form leg (§5.1) are
non-overridable at any lower scope.

The wiring half is governed by §5 of the standard: any process that emits a review document
exceeding the Decision-card budget (§2.2: > 5 lines prose + > 3 bullets) MUST also emit a
companion decision surface modeled on the canonical Pause-Ask template and the skeleton at
`skills/momentum/references/templates/companion-decision-surface.html`. The obligation attaches
to "the act of emitting a review document," not to any one skill.

### Current State of Affected Files

- `.claude/rules/decision-grade-presentation.md` (185 lines) — STALE. Stops at the 8-surface
  schema table; no §5 Companion-Surface Obligation, no §5.1 presentation-form leg, no §2.2 row 9.
  Section numbering is one behind canonical (project §5 = canonical §6). `grep -c
  "Companion-Surface Obligation"` returns 0. This is the primary edit target.
- `skills/momentum/references/rules/decision-grade-presentation.md` (249 lines) — CANONICAL,
  already carries §5/§5.1/row 9 (delivered in `da70fed`). READ-ONLY source for the sync; do NOT
  edit it in this story.
- `skills/momentum/references/templates/companion-decision-surface.html` (229 lines) — the
  shipped skeleton the wired paths must derive from. READ-ONLY source; do NOT edit it.
- `skills/momentum/skills/intake/workflow.md` (203 lines) — current intake emits a single stub
  file plus a small "Story Captured to Backlog" report (under the Decision-card budget). **As of
  today there is NO over-budget review-document emission path in this skill** — the only output is
  the single-stub capture. Task 3 must therefore first resolve whether the over-budget path
  already exists, must be introduced, or is out of scope (see "Open product fork" below).
- `skills/momentum/skills/intake/SKILL.md`, `.../references/stub-template.md`,
  `.../evals/` — supporting skill files; evals dir receives the new EDD evals.

### Architecture Compliance

- **Cascade integrity (rule sync):** per the standard's own Cascade-Order section, project scope
  cannot loosen the caps-vs-floor boundary, the three required fields, the core convention, the
  companion-surface obligation, or the presentation-form leg. The sync must carry all of these
  forward verbatim (or tighter), never weaker.
- **Companion-surface obligation (wiring):** the large document is the depth-on-demand backing,
  not the review artifact; the companion surface is what the human is handed. Render as visual
  HTML (not flat prose), lead with a plain-language purpose hero, diagram the structure, link
  (never inline) source artifacts, and force a per-fork written verdict at sign-off
  (anti-rubber-stamp).
- **HTML-in-viewer convention:** the emitted companion surface is opened in the cmux Browser
  viewer pane (reuse the existing pane as a tab), consistent with the project HTML-viewing
  convention.

### Testing Requirements

- **Rule-sync tasks (rule-hook → behavioral-trigger):** functional verification by grep/diff —
  the obligation/leg/row-9 strings are present in the project rule (were absent), and a
  section-by-section comparison against canonical shows no loosened cap and no dropped
  non-overridable leg.
- **Wiring tasks (skill-instruction → skill-invoke):** EDD. Behavioral evals confirm (a) an
  over-budget review-document path emits both the document and a template-derived companion
  surface, and (b) a below-budget single-stub capture emits no companion surface and is not
  flagged. The single frozen verification contract for this story takes the dominant `skill-invoke`
  driver (see Verification note below); the rule-hook tasks remain independently checkable via
  behavioral-trigger at the task level per verification-standard.md §1.

### Product fork — RESOLVED at the plan gate

> **RESOLVED (ratified by the developer at the `sprint-2026-06-28` plan gate): resolution (C) —
> scope intake OUT.** intake has no over-budget review-document emission today (single-stub capture
> only), so Task 3 lands on (C): the under-budget single-stub path is already-compliant (**AC6 holds,
> AC4 and AC5 are recorded N/A** with this justification, not left unmet). This story's delivered
> scope is the **project-rule sync only (AC1–AC3, AC6 + Tasks 1–2)**. The genuine bulk-derivation
> wiring — emitting a paired companion surface from an over-budget review document — is **split to a
> separate backlog story** (`companion-surface-bulk-derivation-wiring`), since the real over-budget
> emitters live in `momentum:triage` batch intake or the sprint-planning pre-sprint gate, not intake.
> Tasks 4–6 (the wiring half) are therefore out of scope for this story; do not build them here.

This story carries one genuine fork an agent cannot default purely to standards, plus two
membership observations. All three are surfaced here (the fork above is now resolved).

- **Fork — does intake actually have an over-budget review-document path to wire?**
  *What:* the wiring half (Tasks 3–6, AC4–AC6) assumes a bulk / ad-hoc-plan path under
  `skills/momentum/skills/intake/` that emits a review document exceeding the Decision-card budget.
  *Why it matters:* if no such path exists and none is added, Tasks 4–5 become no-ops and the
  story's second half delivers nothing; if a new bulk capability is silently built, the story
  quietly widens scope. Either way the dev needs a decision, not a guess.
  *Evidence:* `skills/momentum/skills/intake/` contains only `workflow.md` (single-stub capture,
  203 lines), `SKILL.md`, `references/stub-template.md`, and three single-scenario evals; the
  workflow's CRITICAL guard is "1 read, 1 write, 1 bash, no subagent spawns" and its Step 5 report
  is well under the Decision-card budget — there is no over-budget emission today.
  *Recommendation (defaulted):* take resolution **(C)** in Task 3 — treat the under-budget
  single-stub path as already-compliant (AC6 holds, AC4 N/A) and split any genuine bulk/ad-hoc-plan
  derivation surface (the real over-budget emitters are more likely `momentum:triage` batch intake
  or the sprint-planning pre-sprint gate) into a separate, correctly-scoped story.
  *Options:* (A) wire an existing path · (B) add the bulk capability under this story · (C) scope
  intake out and split the bulk-path wiring to a follow-up.

- **Epic membership (carried from the stub, not re-decided here).** This story is registered under
  `momentum-impetus-experience`, whose stated scope is Impetus's visual identity / session-opening
  personality — a project-rule sync + companion-surface wiring does not advance that scope, and the
  slug is absent from that epic's `stories` array in `epics.json`. A presentation-gate / sprint-
  orchestration epic (which already owns gate-rendering stories) or a practice-standards epic is a
  closer fit. Reassigning an epic and registering the slug in the epic's `stories` array are
  `momentum:epic-grooming` / sprint-manager operations, deliberately NOT performed by story
  creation. Flagged for the developer to reassign + register if desired.

### Project Context Reference

- Standard (canonical): `skills/momentum/references/rules/decision-grade-presentation.md` §5,
  §5.1, §2.2 row 9, §6 schema, §8 cascade.
- Template: `skills/momentum/references/templates/companion-decision-surface.html`.
- Routing: `skills/momentum/references/rules/verification-standard.md` §1 (change_type → method).
- Multi-type precedence: `skills/momentum/skills/sprint-planning/references/contract-format-guide.md`
  → "Multi-Change-Type Precedence".

#### Verification method — chosen under ambiguity

This story declares two change-types — `rule-hook` (the `.claude/rules/...` sync) and
`skill-instruction` (the `skills/momentum/skills/intake/...` wiring) — which route to two
distinct methods (`behavioral-trigger` and `skill-invoke`). Per the **Multi-Change-Type
Precedence** ordering in `contract-format-guide.md`
(`… > skill-instruction > rule-hook > config-structure > …`), `skill-instruction` is the
highest-weight type, so its method **`skill-invoke`** governs the story's single frozen contract
and is recorded as `verification_method_advisory`. Rationale (DEC-029 D1): verification weight
scales with change-type; the highest-weight type's method subsumes lighter-weight methods.
The alternative — **`behavioral-trigger`** (the rule-hook half) — was not chosen as the dominant
contract driver; per `verification-standard.md` §1 the rule-hook tasks still apply
behavioral-trigger verification to their own tasks. The developer may override the dominant driver
at the approval gate by adding a written justification to this story's frozen contract
(per `verification-standard.md` §2).

### References

- Parent story (provenance): `visual-hitl-gates-presentation-form-standard-leg` (Part A remainder)
- Delivered foundation: commit `da70fed` — canonical rule §5/§5.1 + companion-surface template
- Stale sync target: `.claude/rules/decision-grade-presentation.md`
- Companion-surface template: `skills/momentum/references/templates/companion-decision-surface.html`
- Epic context: `momentum-impetus-experience` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2 → rule-hook (functional verification)
- Tasks 3, 4, 5, 6 → skill-instruction (EDD)

---

### rule-hook Tasks: Functional Verification

Rules are declarative — they don't have unit tests. Use functional verification:

1. **Write the rule edits** per the canonical format — port §2.2 row 9, §5, §5.1, the §6 schema
   rows, and the §8 cascade bullets into `.claude/rules/decision-grade-presentation.md`,
   matching the canonical section structure and numbering.
2. **State the expected behavior** as a testable condition: "Given the project rule after sync,
   grepping for the obligation/leg strings returns ≥ 1 and a diff against canonical shows no
   loosened cap and no dropped non-overridable leg."
3. **Verify functionally:**
   - `grep -c "Companion-Surface Obligation" .claude/rules/decision-grade-presentation.md` ≥ 1
   - `grep -c "Presentation form — the third leg" .claude/rules/decision-grade-presentation.md` ≥ 1
   - §2.2 "Companion decision surface" row present; §6 schema rows present; §8 non-overridable
     list includes the obligation + presentation-form leg bullets.
   - Section-by-section comparison against canonical: no cap weakened; numbering aligned.
4. **Document** the before/after grep counts and the comparison result in the Dev Agent Record.

**Format requirements:**
- Rule file in `.claude/rules/` must follow the established markdown format and remain internally
  consistent (cross-references resolve, section numbers monotonic).
- Project scope may tighten a cap value but must not loosen one; non-overridable legs are carried
  forward verbatim.

**Additional DoD items for rule-hook tasks:**
- [ ] Expected behavior stated as a testable condition (in Dev Agent Record)
- [ ] Functional verification performed (grep + diff) and result documented
- [ ] Format and section numbering match the canonical rule

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic
LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill changes:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/intake/evals/`:
   - One `.md` file per eval, named descriptively (e.g.,
     `eval-bulk-derivation-emits-companion-surface.md`,
     `eval-single-stub-capture-emits-no-companion-surface.md`)
   - Format each eval as: "Given [input and context], the skill should [observable behavior]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Modify the intake workflow.md (and SKILL.md / references as needed) to (a) emit the companion
   surface from the template alongside any over-budget review document, (b) make the pairing
   mandatory (document-alone is a defect), and (c) exempt the below-budget single-stub path.

**Then verify:**
3. Run evals: for each eval, spawn a subagent with the eval scenario and the skill files as
   context; observe whether behavior matches.
4. All evals match → task complete. Any eval fails → diagnose, revise, re-run (max 3 cycles;
   surface to developer if still failing).

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` ≤ 150 characters (NFR1) — count precisely if SKILL.md changes
- `model:` and `effort:` frontmatter present (FR23) — preserve existing values
- workflow.md / SKILL.md body ≤ 500 lines / 5000 tokens; overflow goes to `references/` (NFR3)
- Skill name keeps the `momentum:` namespace prefix (NFR12)

**Additional DoD items for skill-instruction tasks:**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/intake/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented)
- [ ] SKILL.md description ≤ 150 chars confirmed (if SKILL.md changed)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] workflow.md / SKILL.md body ≤ 500 lines / 5000 tokens confirmed
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically)

---

**Frozen verification contract reminder:** a frozen verification contract exists for this story
during a sprint (in `.momentum/sprints/{sprint-slug}/specs/{story-slug}.{ext}`). Before signaling
done, the dev reads the Part-A header (`how_dev_self_checks`, `verification_method`,
`harness_profile`) as a self-check. The dev never reads the verifier body (Part B: scenarios,
assertion scripts) beyond sections explicitly referenced by `how_dev_self_checks`. Per the
Multi-Change-Type Precedence resolution above, the dominant driver for the single contract is
`skill-invoke`; the rule-hook tasks are independently checkable via behavioral-trigger.
