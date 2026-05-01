---
title: Sprint Dev Skill — Create SKILL.md for Sprint Execution Workflow
story_key: sprint-dev-skill
status: ready-for-dev
epic_slug: plugin-migration
depends_on: []
touches:
  - skills/momentum/skills/sprint-dev/SKILL.md
  - skills/momentum/workflows/sprint-dev.md
change_type: skill-instruction
---

# Sprint Dev Skill — Create SKILL.md for Sprint Execution Workflow

## Goal

Create a proper `SKILL.md` for the sprint-dev workflow that already exists as
`skills/momentum/workflows/sprint-dev.md`. The workflow content is written and
validated (Phase 3 Round 3, story momentum-sprint-dev, plus AVFL fix pass) — this
story wraps it in a SKILL.md with correct frontmatter so it becomes an independently
invocable skill at `/momentum:sprint-dev`.

## Acceptance Criteria (Plain English)

1. `skills/momentum/skills/sprint-dev/SKILL.md` exists with valid frontmatter
   (name, description, model, effort)
2. The SKILL.md `name:` field is `sprint-dev`
3. The SKILL.md `description:` is ≤150 characters and accurately describes the
   7-phase sprint execution workflow
4. The SKILL.md references the workflow file correctly (either inlined or via
   `Follow the instructions in ./workflow.md`)
5. The workflow content from `skills/momentum/workflows/sprint-dev.md` is either
   moved into the skill directory or referenced from the SKILL.md
6. `/momentum:sprint-dev` is independently invocable (does not require Impetus
   to be running)
7. The model and effort frontmatter values are appropriate for sprint execution
   (this is a complex orchestration task — likely opus/high)

## Dev Notes

### Current state

The sprint-dev workflow exists at `skills/momentum/workflows/sprint-dev.md`. It was
created in Phase 3 Round 3 (story: momentum-sprint-dev) with an AVFL fix pass
(commit 3f8806c). The 7-phase model (Option C with Team Review):

1. **Initialization** — read active sprint, validate locked state, build dependency graph
2. **Team Spawn** — identify unblocked stories, transition to in-progress, execute
3. **Progress Tracking** — monitor tasks, propose merges, re-evaluate dependencies
4. **Post-Merge AVFL** — single AVFL scan on full codebase (Decision 31)
5. **Team Review** — QA + E2E Validator + Architect Guard in parallel (Decision 34)
6. **Verification** — developer-confirmation checklist from Gherkin scenarios
7. **Sprint Completion** — archive sprint, surface summary, suggest retro

### What to create

A thin SKILL.md wrapper:

```yaml
---
name: sprint-dev
description: "Sprint execution — dependency-driven story development, post-merge AVFL, and team review."
model: claude-opus-4-6
effort: high
---
```

Move `sprint-dev.md` from `workflows/` to `skills/sprint-dev/workflow.md`.

### What NOT to change

- Do not modify the workflow content — it's already validated with AVFL fix pass
- Do not change the 7-phase structure
- Do not add new phases or remove existing ones

### Requirements Coverage

- Architecture: Sprint Execution (Decisions 25, 31, 33, 34) — 7-phase workflow
- PRD FR62, FR63, FR64: Sprint execution, dependency ordering, sprint-level AVFL
- Master Plan: Plugin Model layout shows `sprint-dev/SKILL.md`

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral evals (EDD: before skill creation)
  - [ ] Create `skills/momentum/skills/sprint-dev/evals/eval-sprint-dev-invocable.md`
    — verifies skill loads and begins initialization when invoked directly
  - [ ] Create `skills/momentum/skills/sprint-dev/evals/eval-sprint-dev-7-phases.md`
    — verifies all 7 phases are reachable in sequence

- [ ] Task 2 — Create SKILL.md and move workflow (AC: 1–6)
  - [ ] Create `skills/momentum/skills/sprint-dev/` directory
  - [ ] Write SKILL.md with frontmatter
  - [ ] Move `workflows/sprint-dev.md` to `skills/sprint-dev/workflow.md`
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
1. Write 2 behavioral evals in `skills/momentum/skills/sprint-dev/evals/`:
   - One per eval above, testing invocability and phase coverage
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
