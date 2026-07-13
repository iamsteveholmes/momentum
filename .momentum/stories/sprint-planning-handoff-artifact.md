---
title: Add mandatory handoff artifact to sprint-planning workflow terminal step
story_key: sprint-planning-handoff-artifact
status: ready-for-dev
epic_slug: momentum-sprint-planning-to-ready
feature_slug:
story_type: practice
priority: high
depends_on: []
touches:
  - skills/momentum/skills/sprint-planning/workflow.md
  - .claude/rules/handoff-conventions.md
  - skills/momentum/skills/sprint-planning/evals/
change_type:
  - skill-instruction
  - rule-hook
verification_method_advisory: skill-invoke
---

# Add mandatory handoff artifact to sprint-planning workflow terminal step

## Story

As a developer,
I want sprint-planning's terminal step to emit a mandatory handoff artifact into
`.momentum/handoffs/` summarizing the activated sprint — goal, stories, waves, contract
locations, and where sprint state lives,
so that the build session (a fresh `/momentum:conduct` session, per the
fresh-session-before-major-workflows practice) starts from a durable bridge instead of
re-deriving planning context or losing it to session boundaries.

## Description

Sprint-planning currently ends at activation (Step 8) with no durable build-session handoff.
The practice's handoff-conventions rule (`.claude/rules/handoff-conventions.md`) names retro,
assessment, decision, and sprint-dev as handoff writers but sprint-planning emits nothing
consumable by the next session. The one artifact sprint-planning does write —
`.momentum/handoffs/{sprint-slug}-plan-gate.html` (Step 7) — is the developer approval
surface, not a build bridge: it is HTML for human sign-off, not a markdown context handoff a
fresh conductor session reads.

Major Momentum workflows run in fresh sessions (per the fresh-session-before-major-workflows
practice), so planning context — the sprint goal (DEC-039 D1), wave rationale, contract/spec
locations, and planning-time cautions — evaporates unless carried by a durable artifact. The
2026-06-28 retro corpus flagged this terminal-step gap.

The artifact is a use-then-discard bridge: it follows the `<topic>-<YYYY-MM-DD>.md` naming
convention, is intended for the immediate next build session, and is deleted after
consumption (handoffs are ephemeral — not preserved as history).

## Acceptance Criteria

1. As the terminal action of sprint-planning Step 8 — after `momentum-tools sprint activate`
   succeeds and before the workflow returns — the workflow writes a markdown handoff artifact
   into `.momentum/handoffs/`. The activation success output names the artifact's path.
2. The artifact filename follows the `<topic>-<YYYY-MM-DD>.md` convention defined in
   `.claude/rules/handoff-conventions.md` — concretely `{sprint-slug}-build-handoff-<YYYY-MM-DD>.md`
   (topic = `{sprint-slug}-build-handoff`), where the date is the activation date.
3. The artifact carries, at minimum, these four sections:
   a. **Sprint goal** — read from the sprint record `goal` field in `.momentum/sprints/index.json`
      (DEC-039 D1). If the record has no `goal` value, the section states "Sprint goal not
      captured at planning" explicitly rather than omitting the section.
   b. **Stories by wave** — each wave listed in execution order, and under each wave the story
      slugs assigned to it (derived from the sprint record's stored waves and story assignments).
   c. **Contract / spec locations** — the per-story contract path pattern
      `.momentum/sprints/{sprint-slug}/specs/{story-slug}.*` (with the actual resolved paths for
      the activated stories) and the coverage-plan path
      `.momentum/sprints/{sprint-slug}/coverage-plan.md`.
   d. **Planning-time cautions** — any warnings the build session must honor that surfaced during
      planning (e.g., coherence-gate or adversarial-guard notes from Step 3.5, ride-along
      directives, or story-specific cautions). If none were raised, the section states "No
      planning-time cautions raised."
4. The artifact opens with a one-line notice that it is a use-then-discard build bridge for the
   next `/momentum:conduct` session and should be deleted after consumption (handoffs are
   ephemeral).
5. `.claude/rules/handoff-conventions.md` lists `momentum:sprint-planning` in its "Applies to"
   line, so the rule accurately enumerates every handoff writer.
6. The write is mandatory, not best-effort: the workflow step treats emitting the artifact as a
   required terminal action of Step 8. Activation does not report success without the artifact
   path in its output.

## Tasks / Subtasks

- [ ] **Task 1 — Add handoff-artifact emission to sprint-planning Step 8 (terminal step).**
  (AC 1, 2, 6) In `skills/momentum/skills/sprint-planning/workflow.md`, add an action block at
  the end of Step 8 ("Activate the sprint"), positioned after the `momentum-tools sprint activate`
  action and its missing-approvals check, and before/into the final `## ✓ Sprint Activated`
  output. The block writes the markdown handoff to
  `.momentum/handoffs/{{sprint_slug}}-build-handoff-{{today}}.md` and adds the artifact path to
  the activation success output. Treat the write as a required step (no silent-skip branch).
- [ ] **Task 2 — Define the handoff artifact content contract in the workflow instructions.**
  (AC 3, 4) Specify, in the Step 8 emission block, the exact section skeleton the artifact
  carries: the ephemeral-bridge notice line, Sprint goal (from sprint-record `goal`, DEC-039 D1,
  with the graceful-absence wording), Stories by wave, Contract/spec locations (per-story
  `specs/{slug}.*` + `coverage-plan.md`), and Planning-time cautions (with the "none raised"
  wording). Source every field from state the workflow already holds at Step 8 — the sprint
  record (goal, waves, story_assignments), `{{selected_stories}}`, and the contract paths frozen
  in Step 8.A — so no new elicitation is introduced.
- [ ] **Task 3 — Register sprint-planning as a handoff writer in the rule.** (AC 5) Edit
  `.claude/rules/handoff-conventions.md` to add `momentum:sprint-planning` to the "Applies to"
  line alongside retro, assessment, decision, and sprint-dev. Do not change the naming convention
  or the write-location clause.
- [ ] **Task 4 — Write behavioral evals for the emission behavior.** (AC 1–4, 6) Add 2–3 evals
  under `skills/momentum/skills/sprint-planning/evals/` that assert: (a) on a successful
  activation the workflow writes a `{sprint-slug}-build-handoff-<date>.md` into
  `.momentum/handoffs/` and names it in the output; (b) the artifact contains all four required
  sections; (c) when the sprint record has no `goal`, the goal section renders the explicit
  "not captured" wording rather than being dropped.

## Dev Notes

### Decision Authority

- **DEC-039 D1 (Sprint goal captured at planning)** — the sprint goal lives on the sprint record
  (`.momentum/sprints/index.json` entry) and is approved at the plan gate. This story READS that
  `goal` field into the handoff; it does not implement goal elicitation or the record-schema
  `goal` field (those are separate DEC-039 surfaces on sprint-planning and sprint-manager). The
  handoff must degrade gracefully when the field is absent (AC 3a) rather than assume it exists.
- **`.claude/rules/handoff-conventions.md`** — governs all handoff artifacts: written to
  `.momentum/handoffs/`, named `<topic>-<YYYY-MM-DD>.md`. This story makes sprint-planning conform
  to that rule and adds it to the rule's "Applies to" enumeration (AC 5).
- **Handoffs are ephemeral** (practice standard) — bridging docs consumed by the immediately
  following session and deleted after, never preserved as history. The artifact must say so
  (AC 4).

### Current State of Affected Files

- `skills/momentum/skills/sprint-planning/workflow.md` (1258 lines) — Step 8 ("Activate the
  sprint", lines ~1152–1256) is the terminal step. It runs a pre-activation artifact gate,
  freezes contract checksums (Step 8.A), persists story_assignments, calls
  `momentum-tools sprint ready` then `momentum-tools sprint activate`, and emits the
  `## ✓ Sprint Activated` output. The new emission block is inserted before/into that final
  output (not after it), so the `## ✓ Sprint Activated` output can name the artifact path per
  AC1/AC6. Note Step 7 already writes
  `.momentum/handoffs/{{sprint_slug}}-plan-gate.html` — that is the human approval surface and is
  NOT the build handoff; do not conflate or replace it. All the data the handoff needs is already
  in scope at Step 8: `{{sprint_slug}}`, `{{selected_stories}}`, the sprint-record waves and
  `story_assignments`, and the per-story contract paths frozen in Step 8.A.
- `.claude/rules/handoff-conventions.md` (4 content lines) — the "Applies to" line currently reads
  `momentum:retro, momentum:assessment, momentum:decision, momentum:sprint-dev`. Add
  `momentum:sprint-planning`.
- `skills/momentum/skills/sprint-planning/evals/` — create if absent; add the Task 4 eval files.

### Architecture Compliance

- Read the sprint goal from the sprint record (`.momentum/sprints/index.json` entry), not from
  the plan-gate HTML or any transient variable — the record is the DEC-039 D1 source of truth.
- Do not full-read large files during implementation: `stories/index.json`,
  `sprints/index.json`, and `workflow.md` are read by targeted chunk/Grep, not whole-file loads.
- The handoff is markdown (`.md`), distinct in both format and purpose from the Step 7 plan-gate
  HTML companion surface. Keep them separate.

### Testing Requirements

- Primary verification is `skill-invoke` (advisory): invoke sprint-planning through activation on
  a fixture/active sprint and observe that the build-handoff `.md` lands in `.momentum/handoffs/`,
  is named per convention, contains all four sections, and is named in the activation output.
- The rule change (`.claude/rules/handoff-conventions.md`) verifies functionally: confirm the
  "Applies to" line now includes `momentum:sprint-planning` and the rule's format/other clauses
  are unchanged.
- EDD governs the skill-instruction work (see Momentum Implementation Guide) — write the Task 4
  evals before editing the workflow, run them after.

### Project Context Reference

- `.claude/rules/handoff-conventions.md` — the rule this story implements and amends.
- `_bmad-output/planning-artifacts/decisions/dec-039-sprint-goal-mutable-scope-2026-07-10.md` —
  D1 is the sprint-goal source.

### References

- Rule: `.claude/rules/handoff-conventions.md` (write location + `<topic>-<YYYY-MM-DD>.md` naming)
- Decision: DEC-039 D1 — sprint goal captured at planning, stored in the sprint record, carried
  to the build (`_bmad-output/planning-artifacts/decisions/dec-039-sprint-goal-mutable-scope-2026-07-10.md`)
- Handoff: `refine-complete-2026-07-10` (developer-directed sprint-planning fixes) — origin of
  this shortlist item
- Related story: `sprint-planning-activation-gate` — status `dropped` in
  `.momentum/stories/index.json`. It was flagged during planning as possibly the same
  terminal-step story; the two were split, this story owns the handoff-artifact scope only and
  the activation-gate scope was dropped rather than folded in here.
- Epic context: `momentum-sprint-planning-to-ready` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 4 → skill-instruction (EDD)
- Task 3 → rule-hook (functional verification)

A frozen verification contract exists for this story for this sprint at
`.momentum/sprints/{sprint-slug}/specs/sprint-planning-handoff-artifact.{ext}`. Before signaling
done, dev reads the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`)
as a self-check. Dev never reads the verifier body (Part B: scenarios, assertion scripts) beyond
sections `how_dev_self_checks` explicitly points to.

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/sprint-planning/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-emits-build-handoff-on-activation.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the SKILL.md, workflow.md, or reference files

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context (or invoke the skill via its Agent Skills name if installed). Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely (N/A here: this story edits `workflow.md`, not the SKILL.md description; leave the existing description untouched)
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md/workflow.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3) — the workflow is already ~1258 lines across a single workflow.md; keep the added block tight and, if it pushes structure past readability, extract the artifact skeleton to `references/`
- Skill names use `momentum:` namespace prefix (NFR12)

**Additional DoD items for skill-instruction tasks:**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/sprint-planning/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] `model:` and `effort:` frontmatter present and correct on the sprint-planning SKILL.md (unchanged by this story — confirm not broken)
- [ ] Added block keeps workflow.md readable; overflow (if any) moved to `references/`
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically)

---

### rule-hook Tasks: Functional Verification

Rules and hook configurations are declarative — they don't have unit tests. Use functional verification:

1. **Write the rule entry** per the established format in `.claude/rules/handoff-conventions.md` — add `momentum:sprint-planning` to the "Applies to" line; change nothing else.
2. **State the expected behavior** as a testable condition: "Given a reader consulting handoff-conventions.md to learn which skills write handoffs, the rule should list `momentum:sprint-planning` among them."
3. **Verify functionally:** confirm the "Applies to" line now enumerates sprint-planning, the write-location and naming clauses are unchanged, and the file remains internally consistent.
4. **Document** the verification result in the Dev Agent Record.

**Format requirements:**
- Rules files in `.claude/rules/` must follow the established markdown format
- No duplicate entries (merge, don't append)

**Additional DoD items for rule-hook tasks:**
- [ ] Expected behavior stated as testable condition (in Dev Agent Record)
- [ ] Functional verification performed and result documented
- [ ] Format matches established patterns
