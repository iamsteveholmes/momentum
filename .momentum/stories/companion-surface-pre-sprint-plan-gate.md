---
title: "Companion surface — pre-sprint plan gate emitted by sprint-planning"
story_key: companion-surface-pre-sprint-plan-gate
status: ready-for-dev
epic_slug: momentum-impetus-experience
feature_slug:
story_type: practice
priority: high
depends_on: []
touches:
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/sprint-planning/SKILL.md
  - skills/momentum/skills/sprint-planning/references/plan-gate-renderer.md
  - skills/momentum/skills/sprint-planning/evals/
change_type:
  - skill-instruction
verification_method_advisory: skill-invoke
---

# Companion surface — pre-sprint plan gate emitted by sprint-planning

## Story

As the developer (the practice owner),
I want `momentum:sprint-planning` to emit a **visual, purpose-first pre-sprint plan gate**
(an HTML companion decision surface, sibling of `endgate-report.html`) as its final step,
so that at the single highest-leverage steering moment I can understand and shape a sprint in
seconds instead of skim-then-rubber-stamping an ad-hoc concatenation of full story specs.

## Description

The pre-sprint plan review is one of Momentum's two highest-leverage HITL gates. Today
`sprint-planning` selects, specs, and activates stories but its developer-review step (Step 7)
emits a **flat-text plan summary** followed by an `A/M/R` prompt — and the human reviews the
substance by opening whatever they open (an unmeasured, ad-hoc path). For one 8-story sprint
that ad-hoc path was a ~37,500-word concatenation of full specs — a log file, not a decision
document.

The global decision-grade-presentation standard now **requires** this surface:
`skills/momentum/references/rules/decision-grade-presentation.md` §2.2 row 9 (Companion
decision surface) names the "pre-sprint plan gate (`sprint-planning`, final step)" as a
mandatory named instance (§6 surface schema); §5 states the companion-surface obligation; and
§5.1 (presentation-form leg, non-overridable per §8) requires it render as **visual HTML**, lead
with a **plain-language purpose hero**, and **diagram the structure** (deps/waves/status). A
reusable, fully-styled skeleton already ships at
`skills/momentum/references/templates/companion-decision-surface.html`. This story makes
`sprint-planning` actually emit the gate, modeled on the existing sibling pattern (the
Conductor's `endgate-report.html`, specified in
`skills/momentum/skills/conductor/references/endgate-report-renderer.md`).

**Decisions already ratified (honored below):**
- Emitted at the **developer-review step (Step 7) of `momentum:sprint-planning`** — the final
  human gate before activation (Step 8) — which already holds the selected-story set + wave/dep
  graph + authored contracts + AVFL result; generation is a synthesis step, not a new pipeline.
- Generation is **synthesis-now**: read and extract the fork callouts, stakes, value lines, and
  wave/dep structure story authors already write and that sprint-planning already computes;
  **defer** any `stakes:`/`value_line:`/`delta:` story-frontmatter contract on `create-story`
  until the gate's shape proves out over 2–3 sprints.
- The gate **links to** the canonical story `.md` files (and their specs); it **never inlines or
  edits** them, so `momentum:dev` / `bmad-dev-story` keep their source-of-truth machine band
  intact.

## Acceptance Criteria

1. **Final-step emission.** When `momentum:sprint-planning` reaches its developer-review step, it
   writes a self-contained HTML plan-gate file (inline CSS/JS, zero external deps) to
   `.momentum/handoffs/{{sprint_slug}}-plan-gate.html` and opens it in the cmux viewer pane as a
   browser tab (existing pane reused, not a new structural pane). Observable: the file exists
   after the step runs and is opened for the developer.
2. **Purpose hero first.** The gate's first content block is a plain-language purpose hero that
   states what the sprint accomplishes — readable by a non-implementer in seconds — appearing
   before any table, list, or decision card (exec-summary-first; standard §5.1).
3. **Structure diagrammed, not described.** The gate renders the dependency/wave structure as an
   inline-SVG diagram (not prose), and visibly marks any single-point-of-failure / critical-path
   story (e.g., the ⚠ hub treatment from the template).
4. **Scannable story table.** Every selected story appears exactly once in an at-a-glance table
   carrying stakes · wave · dep · ★CALL-vs-✓batch verdict; as-specified / routine stories
   collapse to a single line each rather than expanding inline.
5. **Decision card per genuine fork only (≤ 7).** A decision card is rendered only for genuine
   forks — choices an agent cannot default to standards — capped at 7. Each card carries all
   **five** required fields inline per the standard's Pause-Ask template (§5 item 4):
   **What · Why-it-matters · Evidence · Recommendation · Options** — with no bare handles (the
   substance is quoted/summarized, never "per X"). "Options" enumerates the per-fork resolution
   paths (e.g., Approve-as-specified / Modify / Remove-from-sprint). Everything defaultable is
   defaulted silently and accounted for in a "defaulted to standards" collapsible.
6. **Anti-rubber-stamp sign-off.** Sign-off requires a written one-line verdict + reason per
   genuine fork before the sprint can activate; a blanket "approve all" is insufficient. When
   there are zero genuine forks, the batch-approve path enables without per-fork forcing
   (clean-plan path). Approve routes to activation (current Step 8); the modify / re-run-AVFL
   paths are preserved.
7. **Links, never inlines.** The gate links to the canonical story `.md` files (and their
   `specs/` contracts) as depth-on-demand; it never inlines their full body or edits them. The
   machine band (full Tasks/Subtasks, Dev Notes, Design-Fidelity ACs) stays reachable for the dev
   agent but stays out of the review surface.
8. **Synthesis-now generation.** Gate fields (per-story stakes, one-line value, ★CALL-vs-✓batch
   verdict, fork cards) are synthesized from content sprint-planning already holds — story ACs /
   fork callouts, computed waves, `depends_on`, authored contracts, AVFL result. No new
   `create-story` story-frontmatter contract (`stakes:` / `value_line:` / `delta:`) is required
   for v1.
9. **Standard-conformant companion surface.** The emitted gate satisfies the
   decision-grade-presentation standard for a Companion decision surface (§2.2 row 9, §5, §5.1):
   it is built from the shipped skeleton `references/templates/companion-decision-surface.html`,
   keeps the canonical section order (purpose hero → ✓ verified line → structure diagram →
   items-at-a-glance → decision cards → risks (optional) → defaulted-to-standards → sign-off), and
   treats the large machine band as depth-on-demand backing rather than the review artifact.

## Tasks / Subtasks

_Task order honors EDD: the renderer contract (Task 1) defines the shape, evals (Task 2) are
authored before the workflow implementation (Task 3), then SKILL.md metadata (Task 4)._

- [ ] **Task 1 — Author the plan-gate renderer reference doc** (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9)
  - Create `skills/momentum/skills/sprint-planning/references/plan-gate-renderer.md`, a
    data-contract + rendering spec modeled on the Conductor's
    `references/endgate-report-renderer.md`. Author this first — it defines the card/section
    contract the Task 2 evals assert against.
  - Specify the **input data contract**: what the developer-review step already has in context
    (selected story set + titles, computed waves, `depends_on` edges, authored contracts +
    coverage dispositions, AVFL result, and the per-story fork callouts / stakes / one-line
    values synthesized from each story file).
  - Specify the **fixed section spine** matching the shipped template: purpose hero → ✓ verified
    (mechanically-checkable) line → inline-SVG structure diagram (mark SPOF/critical-path) →
    items-at-a-glance table (routine collapse to one line) → decision cards (≤ 7 genuine forks,
    each carrying **What / Why-it-matters / Evidence / Recommendation / Options** inline) → risks
    (optional — where the reviewer should spend skepticism) → "defaulted to standards"
    collapsible → anti-rubber-stamp sign-off.
  - Specify the **synthesis rules**: how to derive each story's stakes, one-line value, and
    ★CALL-vs-✓batch verdict from existing story content; how to decide what is a genuine fork vs
    a defaulted-to-standards choice; and how to populate each fork card's **Options** (the
    resolution paths, e.g. Approve-as-specified / Modify / Remove-from-sprint).
  - Specify **output path** `.momentum/handoffs/{{sprint_slug}}-plan-gate.html` and the cmux
    viewer-open command (browser tab in the existing pane, per handoff conventions).
- [ ] **Task 2 — Write the behavioral evals (EDD — before the workflow implementation)** (AC1–AC9)
  - Per the EDD rule (skill-instruction: evals precede implementation), write 2–3 behavioral evals
    in `skills/momentum/skills/sprint-planning/evals/` asserting observable gate behavior against
    the Task 1 contract (e.g., given a planned sprint with one genuine fork and several routine
    stories, the developer-review step emits an HTML gate whose first block is a purpose hero,
    renders an SVG wave diagram with the critical-path story marked, shows exactly one decision
    card carrying What/Why/Evidence/Recommendation/Options, collapses routine stories to one line
    each, and presents a sign-off that rejects a blanket approve-all).
- [ ] **Task 3 — Wire the gate into sprint-planning developer-review (Step 7)** (AC1–AC9)
  - In `skills/momentum/skills/sprint-planning/workflow.md`, modify Step 7 (developer review) to
    load `references/templates/companion-decision-surface.html` + the new
    `references/plan-gate-renderer.md`, synthesize the gate data from in-context plan state,
    render the self-contained HTML, write it to the handoffs path, and open it in the viewer.
  - Replace the flat-text plan summary + `A/M/R` prompt with the **gate's sign-off as the
    approval mechanism**, preserving the existing control semantics: Approve → Step 8 activation;
    Modify → adjust selection/waves/team then re-render; Re-run AVFL → return to Step 6.
  - Enforce: links to canonical story files (never inline/edit), ≤ 7 fork cards each carrying
    What/Why/Evidence/Recommendation/Options, routine stories collapsed, anti-rubber-stamp written
    verdict per fork, clean-plan path when zero forks.
  - Run the EDD verify cycle against the Task 2 evals (max 3 revise/re-run cycles).
- [ ] **Task 4 — Update the skill description** (AC1, AC2)
  - In `skills/momentum/skills/sprint-planning/SKILL.md`, update the `description` to reflect that
    the developer-review step now emits a visual companion plan gate. Keep `description` ≤ 150
    chars; preserve `model:` and `effort:`.

## Dev Notes

### Decision Authority

This story implements the ratified decisions captured in its parent
(`visual-hitl-gates-presentation-form-standard-leg`, Part B) and is **governed** by the
decision-grade-presentation standard:
`skills/momentum/references/rules/decision-grade-presentation.md` — §2.2 row 9 (Companion
decision surface budget), §5 (companion-surface obligation), §5.1 (presentation-form leg). §5.1
and the caps-vs-floor boundary are listed as **non-overridable at lower scope** in §8 — the dev
agent may not trade away the purpose-hero / SVG-diagram / floor requirements to hit a cap.

Ratified and binding: (1) emit at the **developer-review step (Step 7) of sprint-planning** (the
final human gate before Step 8 activation); (2) **synthesis-now** generation (no new frontmatter
contract in v1); (3) the gate **links to** — never inlines or edits — the canonical story files.

### Current State of Affected Files

- `skills/momentum/skills/sprint-planning/workflow.md` — Step 7 (`Developer review of complete
  sprint plan`) currently emits a flat-text block (`Sprint Plan — {{sprint_slug}}` with stories
  grouped by wave, team composition, dependency graph, contract/spec counts, AVFL result) and an
  `A/M/R` `<ask>`. Step 8 (`Activate the sprint`) runs the activation gate + `momentum-tools
  sprint activate`. This story rewrites Step 7's presentation/approval into the visual gate while
  leaving Step 8 activation intact; Approve must still route into Step 8.
- `skills/momentum/skills/sprint-planning/SKILL.md` — `name: sprint-planning`, `model:
  claude-sonnet-4-6`, `effort: high`; `description` is the only field changing.
- `skills/momentum/skills/sprint-planning/references/plan-gate-renderer.md` — **new file** (does
  not exist yet; only `contract-format-guide.md` is in `references/` today).
- `skills/momentum/references/templates/companion-decision-surface.html` — **read-only input**,
  already ships. It is the styled skeleton to fill (purpose hero, stat tiles, SVG diagram, story
  cards, decision cards, defaulted-to-standards `<details>`, anti-rubber-stamp gate). Do not edit
  it.

### Architecture Compliance

- Mirror the established sibling pattern: the Conductor's end-gate
  (`skills/momentum/skills/conductor/references/endgate-report-renderer.md`) is the precedent for
  a self-contained single-`.html` decision surface written to `.momentum/handoffs/` and opened as
  a cmux browser tab. Match its conventions (assume-nothing voice, inline `<style>`/`<script>`,
  warm-parchment palette already present in the template, no external dependencies).
- Honor `.claude/rules/handoff-conventions.md`: handoff artifacts live under `.momentum/handoffs/`.
- Honor cmux rules: open the HTML as a **tab in the existing viewer pane** via `cmux browser new
  … --focus false`; never create a new structural pane.

### Testing Requirements

- **Verification method (routing): `skill-invoke`.** Per
  `skills/momentum/references/rules/verification-standard.md` §1, `change_type:
  skill-instruction` routes to `skill-invoke`. Routing is unambiguous (the story's only change
  type is `skill-instruction`); no override justification is needed. Verification means invoking
  `momentum:sprint-planning` (or driving its final step with a representative planned sprint in
  context) and observing that the gate file is emitted with the required structure and behavior —
  inspection of the emitted HTML against ACs 2–9 is subsumed under this invocation, not a
  separate document-review.
- **EDD, not TDD** (skill-instruction): see the Momentum Implementation Guide below.
- **AVFL checkpoint** on the produced skill artifacts runs automatically when `momentum:dev`
  implements this story.

### Project Context Reference

This is the Momentum practice module (markdown + bash; no compiled app, no Compose UI). The
"visual" governance for this surface is the decision-grade-presentation standard plus the shipped
`companion-decision-surface.html` template — **not** a Compose `docs/ux/design-system/DESIGN.md`.
The standard create-story design-fidelity pass (Compose/canvas-oriented) therefore does not apply
to this story; visual correctness is governed by the standard + template named above.

### References

- Parent story: `visual-hitl-gates-presentation-form-standard-leg` (Part B) — `.momentum/stories/visual-hitl-gates-presentation-form-standard-leg.md`
- Governing standard: `skills/momentum/references/rules/decision-grade-presentation.md` §2.2 row 9 + §5 + §5.1 (presentation-form leg) + §6 (surface schema) + §8 (non-overridable)
- Reusable template to fill: `skills/momentum/references/templates/companion-decision-surface.html`
- Sibling surface + renderer precedent: `skills/momentum/skills/conductor/references/endgate-report-renderer.md` (and the `endgate-report.html` it produces)
- Verification routing: `skills/momentum/references/rules/verification-standard.md` §1 (`skill-instruction → skill-invoke`)
- Target skill: `skills/momentum/skills/sprint-planning/workflow.md` (Step 7) + `SKILL.md`
- Epic context: `momentum-impetus-experience` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/sprint-planning/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-final-step-emits-visual-plan-gate.md`, `eval-anti-rubber-stamp-rejects-blanket-approve.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the SKILL.md, workflow.md, or reference files (Tasks 1, 3, 4 — renderer reference, workflow.md, SKILL.md)

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context (or invoke the skill via its Agent Skills name if installed). Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3) — this story deliberately puts the renderer spec in `references/plan-gate-renderer.md`, keeping `workflow.md` lean
- Skill names use `momentum:` namespace prefix (NFR12 — no naming collision with BMAD skills)

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/sprint-planning/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed (overflow in `references/` if needed)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the implemented skill against story ACs)

**Frozen verification contract reminder:** A frozen verification contract exists for this sprint
at `.momentum/sprints/{{sprint-slug}}/specs/{{story-slug}}.{ext}`. Read the **Part-A header**
(`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signaling
done. Do **not** read the verifier body (Part B: scenarios / assertion scripts / Gherkin) beyond
sections explicitly referenced by `how_dev_self_checks`.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
