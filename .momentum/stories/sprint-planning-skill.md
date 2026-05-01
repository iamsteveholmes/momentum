---
title: Sprint Planning Skill — Create SKILL.md for Sprint Planning Workflow
story_key: sprint-planning-skill
status: ready-for-dev
epic_slug: plugin-migration
depends_on: []
touches:
  - skills/momentum/skills/sprint-planning/SKILL.md
  - skills/momentum/workflows/sprint-planning.md
change_type: skill-instruction
---

# Sprint Planning Skill — Create SKILL.md for Sprint Planning Workflow

## Goal

Create a proper `SKILL.md` for the sprint-planning workflow that already exists as
`skills/momentum/workflows/sprint-planning.md`. The workflow content is written and
validated (Phase 3 Round 2, story momentum-sprint-planning) — this story wraps it
in a SKILL.md with correct frontmatter so it becomes an independently invocable
skill at `/momentum:sprint-planning`.

## Acceptance Criteria (Plain English)

1. `skills/momentum/skills/sprint-planning/SKILL.md` exists with valid frontmatter
   (name, description, model, effort)
2. The SKILL.md `name:` field is `sprint-planning`
3. The SKILL.md `description:` is ≤150 characters and accurately describes the
   8-step sprint planning workflow
4. The SKILL.md references the workflow file correctly (either inlined or via
   `Follow the instructions in ./workflow.md`)
5. The workflow content from `skills/momentum/workflows/sprint-planning.md` is
   either moved into the skill directory or referenced from the SKILL.md
6. `/momentum:sprint-planning` is independently invocable (does not require
   Impetus to be running)
7. The model and effort frontmatter values are appropriate for sprint planning
   (this is an orchestration task requiring judgment — likely opus/high or
   sonnet/high)

## Dev Notes

### Current state

The sprint-planning workflow exists at `skills/momentum/workflows/sprint-planning.md`
(342 lines, 8 steps). It was created in Phase 3 Round 2 (story: momentum-sprint-planning)
and passed QA 16/16, Validator 29/30.

The workflow covers:
1. Backlog presentation (grouped by epic, excluding terminal states)
2. Story selection (3–8 stories with dependency warnings)
3. Story fleshing-out (spawn `momentum:create-story` for stubs)
4. Gherkin spec generation
5. Team composition (roles, guidelines, dependency graph)
6. AVFL validation of complete plan
7. Developer review
8. Sprint activation via `momentum-tools sprint activate`

### What to create

A thin SKILL.md wrapper:

```yaml
---
name: sprint-planning
description: "Sprint planning — story selection, team composition, Gherkin specs, and activation."
model: claude-sonnet-4-6
effort: high
---
```

The SKILL.md body should either:
- Reference the workflow: `Follow the instructions in ./workflow.md`
- Or inline key routing logic if the workflow needs a preamble

Move `sprint-planning.md` from `workflows/` to `skills/sprint-planning/workflow.md`.

### What NOT to change

- Do not modify the workflow content — it's already validated
- Do not change the 8-step structure
- Do not add new steps or remove existing ones

### Requirements Coverage

- Architecture: Sprint Planning (Decision 29) — 8-step workflow
- PRD FR59: Sprint planning workflow
- Master Plan: Plugin Model layout shows `sprint-planning/SKILL.md`

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral evals (EDD: before skill creation)
  - [ ] Create `skills/momentum/skills/sprint-planning/evals/eval-sprint-planning-invocable.md`
    — verifies skill loads and begins backlog presentation when invoked directly
  - [ ] Create `skills/momentum/skills/sprint-planning/evals/eval-sprint-planning-8-steps.md`
    — verifies all 8 steps are reachable in sequence

- [ ] Task 2 — Create SKILL.md and move workflow (AC: 1–6)
  - [ ] Create `skills/momentum/skills/sprint-planning/` directory
  - [ ] Write SKILL.md with frontmatter
  - [ ] Move `workflows/sprint-planning.md` to `skills/sprint-planning/workflow.md`
  - [ ] Verify SKILL.md references workflow correctly

- [ ] Task 3 — Run evals and verify (AC: 7)
  - [ ] Run each eval via subagent
  - [ ] Confirm skill is independently invocable

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Before writing a single line of the skill:**
1. Write 2 behavioral evals in `skills/momentum/skills/sprint-planning/evals/`:
   - One per eval above, testing invocability and step coverage
   - Format: "Given [input/context], the skill should [observable behavior]"

**Then implement:**
2. Write SKILL.md and move workflow file

**Then verify:**
3. Run evals via subagent, confirm behaviors match

**NFR compliance:**
- SKILL.md `description` must be ≤150 characters (NFR1)
- `model:` and `effort:` frontmatter must be present
- SKILL.md body ≤500 lines / 5000 tokens

**DoD items for skill-instruction tasks:**
- [ ] 2 behavioral evals written
- [ ] EDD cycle ran — all eval behaviors confirmed
- [ ] SKILL.md description ≤150 characters confirmed
- [ ] `model:` and `effort:` frontmatter present
- [ ] SKILL.md body ≤500 lines confirmed

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
