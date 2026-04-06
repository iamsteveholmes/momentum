---
title: Quick Fix Skill — Single-Story Tactical Workflow
story_key: quick-fix-skill
status: ready-for-dev
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/skills/quick-fix/SKILL.md
  - skills/momentum/skills/quick-fix/workflow.md
  - skills/momentum/commands/quick-fix.md
  - skills/momentum/skills/quick-fix/evals/
change_type: skill-instruction
---

# Quick Fix Skill — Single-Story Tactical Workflow

## Goal

Create `momentum:quick-fix` — a streamlined single-story workflow that combines
the essential quality steps from sprint-planning and sprint-dev into 6 phases:
Define, Specify, Review, Implement, Validate, Ship. The skill handles one fix
discovered in the moment with full spec coverage (story file, Gherkin, architecture/PRD
impact, AVFL, E2E validation) but no multi-story ceremony (no backlog, no wave planning,
no dependency graphs, no sprint activation).

After this story, a developer can invoke `/momentum:quick-fix` with a description of
a fix and walk through definition, specification, implementation, and validation in
one continuous flow.

## Acceptance Criteria (Plain English)

1. `/momentum:quick-fix` is independently invocable — does not require Impetus or
   an active sprint
2. Phase 1 (Define) creates a story via `momentum:create-story` from the user's
   prompt, registers it in stories/index.json, then opens the story spec in a cmux
   markdown surface on the right pane for developer review and approval
3. Phase 2 (Specify) generates a Gherkin `.feature` file applying the Outsider Test,
   runs spec impact analysis, determines specialist agent from touches paths, checks
   guidelines, runs AVFL checkpoint on the plan, then opens the Gherkin spec in a
   cmux markdown surface for developer review and approval
4. Phase 3 (Implement) creates a worktree off `main` (warns if not on main), spawns
   the specialist dev agent, and merges on completion. The dev agent uses the same
   guidelines and specialist configuration that carries into Phase 4
5. Phase 4 (Validate) runs post-merge AVFL scan, then the same Dev agent and E2E
   Validator collaborate via task list — E2E finds issues, Dev fixes, E2E re-verifies
   — looping until clean or developer halts
6. Phase 5 (Ship) merges to main, shows push summary, asks to push
7. The workflow never presents a backlog, selects from multiple stories, computes waves,
   builds dependency graphs, or runs sprint activation/completion lifecycle
8. If the current branch is not `main`, the workflow warns the developer and offers
   to continue or switch first — default is always worktree off `main`
9. A lightweight quickfix entry is registered in sprints/index.json for traceability
   (slug, story, started, completed) without using activate/complete lifecycle

## Dev Notes

### What this skill IS

A single-story workflow that walks through every essential quality gate from
sprint-planning and sprint-dev, adapted for a tactical single fix:

| Sprint Planning Step | Quick-Fix Adaptation |
|---------------------|---------------------|
| Step 0: Task tracking | KEEP — create tasks for 6 phases |
| Step 1: Show backlog | SKIP — story from prompt |
| Step 2: Story selection | REPLACE — user describes fix, generate slug |
| Step 3: Flesh out story | KEEP — invoke momentum:create-story once |
| Step 4: Gherkin specs | KEEP — 1 feature file, Outsider Test |
| Step 4.5: Spec impact | KEEP — architecture + PRD discovery |
| Step 5: Team composition | SIMPLIFY — single specialist, guidelines check, no waves |
| Step 6: AVFL on plan | KEEP — checkpoint profile |
| Step 7: Developer review | REDESIGN — cmux markdown surfaces |
| Step 8: Activate sprint | SKIP — no sprint lifecycle |

| Sprint Dev Phase | Quick-Fix Adaptation |
|-----------------|---------------------|
| Phase 0: Task tracking | MERGED into planning |
| Phase 1: Initialization | SIMPLIFY — create worktree off main |
| Phase 2: Spawn dev | KEEP — single specialist agent |
| Phase 3: Progress tracking | SIMPLIFY — single merge |
| Phase 4: Post-merge AVFL | KEEP — scan profile |
| Phase 5: Team Review | REDESIGN — Dev + E2E collaborative fix loop |
| Phase 6: Verification | SKIP — collapsed into Phase 5 |
| Phase 7: Completion | SIMPLIFY — merge to main, push |

### The 5 Phases

**Phase 1: Define**
- Create tasks for the 5 workflow phases
- User describes the fix. Ask for epic_slug (default "ad-hoc")
- Invoke `momentum:create-story` with the description
- Open the story spec in a cmux markdown surface on the right pane
- Developer reviews and approves (or requests revisions)

**Phase 2: Specify**
- Generate Gherkin spec (1 `.feature` file, Outsider Test)
- Spec impact analysis (architecture + PRD discovery agents)
- Determine specialist from `touches` paths (same classification table as sprint-planning)
- Check guidelines in `.claude/rules/` — offer G/P/D if missing
- AVFL checkpoint on story plan + Gherkin spec
- Open the Gherkin spec in a cmux markdown surface on the right pane
- Developer reviews and approves (or requests revisions)

**Phase 3: Implement**
- Check current branch. If not `main`, warn: "You're on `{branch}`, not `main`.
  Quick-fix will branch from `main`. Continue, or switch first?"
- Create worktree off `main`: `git worktree add .worktrees/quickfix-{slug} main`
- Resolve specialist agent file (`skills/momentum/agents/{specialist}.md`, fallback to `dev.md`)
- Spawn agent in worktree with story file, guidelines, agent-skill-development-guide if touching skills/agents
- On completion, merge worktree to main (rebase + merge)
- Clean up worktree
- The dev agent configuration (specialist, guidelines) is the same in Phase 3 and Phase 4

**Phase 4: Validate**
- Post-merge AVFL scan (profile: scan, stage: final)
- Fix critical findings before proceeding
- Dev agent + E2E Validator collaborate via task list (same dev agent config as Phase 3):
  - E2E Validator runs Gherkin scenarios, reports failures as tasks
  - Dev agent picks up tasks and fixes immediately
  - E2E re-verifies fixed scenarios
  - Loop until clean or developer halts
- Transition story to done

**Phase 5: Ship**
- Register quickfix completion in sprints/index.json (lightweight — just slug, story, started, completed)
- Show push summary: `git log @{u}..HEAD --oneline`
- Ask to push

### Reusable components (invoke, don't reimplement)

- `momentum:create-story` — story creation (Step 1 of Phase 1)
- `momentum:avfl` — validation (Phase 2 checkpoint + Phase 5 scan)
- `skills/momentum/agents/dev.md` (or specialist) — implementation agent
- `skills/momentum/agents/e2e-validator.md` — behavioral verification
- `momentum-tools.py log` — event logging
- `cmux markdown open` — review surfaces

### Outsider Test (must reproduce in workflow.md)

From sprint-planning Step 4 — the Gherkin generation rules including the Outsider
Test must be reproduced inline in the quick-fix workflow so the model has them in
context when generating specs. Key rule: "Could someone who has never seen the
source code verify this scenario by ONLY invoking skills, running commands, and
reading their outputs?"

### Specialist classification table

Reproduce from sprint-planning Step 5:
```
| Pattern                                                    | Specialist   |
|------------------------------------------------------------|-------------|
| skills/*/SKILL.md, skills/*/workflow.md, agents/*.md       | dev-skills  |
| *.gradle*, *.kts, build.gradle*                            | dev-build   |
| *compose*, *Compose*, *ui/*, *screen*                      | dev-frontend|
| (no match)                                                 | dev (base)  |
```

### What NOT to change

- `momentum:create-story` — invoke it, don't modify it
- `momentum:avfl` — invoke it, don't modify it
- Sprint-planning or sprint-dev workflows — quick-fix is additive
- Any existing agent definition files
- `momentum-tools.py` — no CLI changes needed

### Requirements Coverage

- Architecture: Decisions 26 (two-layer agent model), 35 (skills vs agents boundary)
- PRD: extends sprint execution capabilities for tactical fixes
- Master Plan: fills the gap between full sprints and ad-hoc changes

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral evals (EDD: before skill creation)
  - [ ] Create `skills/momentum/skills/quick-fix/evals/eval-quick-fix-invocable.md`
    — verifies skill loads and begins Phase 1 when invoked directly
  - [ ] Create `skills/momentum/skills/quick-fix/evals/eval-quick-fix-5-phases.md`
    — verifies all 5 phases are reachable in the workflow
  - [ ] Create `skills/momentum/skills/quick-fix/evals/eval-quick-fix-single-story.md`
    — verifies no backlog, wave planning, dependency graphs, or sprint activation

- [ ] Task 2 — Create SKILL.md and command wrapper
  - [ ] Create `skills/momentum/skills/quick-fix/SKILL.md` with frontmatter
    (name: quick-fix, model: claude-opus-4-6, effort: high)
  - [ ] Create `skills/momentum/commands/quick-fix.md` command wrapper

- [ ] Task 3 — Create workflow.md (main deliverable)
  - [ ] Write the 6-phase workflow with XML structure matching sprint-dev/sprint-planning pattern
  - [ ] Include Outsider Test rules inline for Gherkin generation
  - [ ] Include specialist classification table inline
  - [ ] Include cmux markdown surface opening for Phase 3 review
  - [ ] Include Dev + E2E collaborative fix loop for Phase 5

- [ ] Task 4 — Run evals and verify
  - [ ] Run each eval via subagent
  - [ ] Confirm skill is independently invocable
  - [ ] Confirm no multi-story overhead in the workflow

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Before writing a single line of the skill:**
1. Write 3 behavioral evals in `skills/momentum/skills/quick-fix/evals/`:
   - One per eval above, testing invocability, phase coverage, and single-story scope
   - Format: "Given [input/context], the skill should [observable behavior]"

**Then implement:**
2. Write SKILL.md, commands/quick-fix.md, and workflow.md

**Then verify:**
3. Run evals via subagent, confirm behaviors match

**NFR compliance:**
- SKILL.md `description` must be ≤150 characters
- `model:` and `effort:` frontmatter must be present
- SKILL.md body ≤500 lines (workflow.md can be longer)

**DoD items for skill-instruction tasks:**
- [ ] 3 behavioral evals written
- [ ] EDD cycle ran — all eval behaviors confirmed
- [ ] SKILL.md description ≤150 characters confirmed
- [ ] `model:` and `effort:` frontmatter present
- [ ] SKILL.md body ≤500 lines confirmed

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
