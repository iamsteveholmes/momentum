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
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
change_type: skill-instruction + script-code
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
5. Phase 4 (Validate) runs post-merge AVFL scan, then the validation team
   collaborates via task list with the Dev agent. Which validators run depends on
   change type: E2E Validator for skill-instruction (behavioral verification),
   QA for script-code (test coverage and functional verification). Both run when
   both change types are present. Dev fixes issues as they come in, validators
   re-verify. Loop until clean or developer halts.
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
- Spec impact discovery — spawn architecture + PRD discovery agents to identify
  new decisions, modified constraints, or new FRs introduced by this fix
- Spec impact updates — if impacts found, spawn architect agent to update
  architecture.md and PM agent to update prd.md. These are the sole writers of
  their respective files — the dev agent in Phase 3 never touches them
- Generate Gherkin spec (1 `.feature` file, Outsider Test) — generated AFTER spec
  updates so Gherkin can reference any new decisions or FRs
- Determine specialist from `touches` paths (same classification table as sprint-planning)
- Check guidelines in `.claude/rules/` — offer G/P/D if missing
- AVFL checkpoint on story plan + Gherkin spec
- Open the Gherkin spec in a cmux markdown surface on the right pane
- Developer reviews and approves (or requests revisions)

**Phase 3: Implement**
- Check current branch. If not `main`, warn: "You're on `{branch}`, not `main`.
  Quick-fix will branch from `main`. Continue, or switch first?"
- Create worktree off `main`: `git worktree add .worktrees/quickfix-{slug} main`
- Resolve specialist agent via `momentum-tools specialist-classify`. Spawn a single
  specialist dev agent. When a story has multiple change types (e.g., skill-instruction
  + script-code), the specialist is chosen by the dominant change type. Multi-specialist
  parallel dev is a future enhancement — v1 uses one dev agent per story.
- Pass agent: story file, all tasks, guidelines, sprint context,
  agent-skill-development-guide if touching skills/agents
- On completion, merge worktree to main (rebase + merge)
- Clean up worktree
- The dev agent configuration (specialists, guidelines) carries into Phase 4

**Phase 4: Validate**
- Post-merge AVFL scan (profile: scan, stage: final)
- Fix critical findings before proceeding
- Create an Agent Team via `TeamCreate` with these roles:
  - **Dev agent:** same specialist from Phase 3 — stays resident to fix issues
    as validators find them
  - **Validators:** determined by change types in the story:
    - `skill-instruction` → E2E Validator (behavioral verification via Gherkin specs)
    - `script-code` → QA (test coverage, edge cases, functional verification)
    - Both present → both validators join the team
- The team collaborates via task list:
  - Validators run their checks, report failures as tasks
  - Dev agent picks up tasks and fixes immediately
  - Validators re-verify fixed items
  - Loop until all validators report clean or developer halts
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

### Orchestrator purity (Decision 3d)

The quick-fix workflow is an orchestrator. It MUST NOT write files directly. Every
file change happens through:
- **Tool invocations:** `momentum-tools`, `cmux`, `git` commands via Bash
- **Subagent spawns:** architect agent writes architecture.md, PM agent writes prd.md,
  `momentum:create-story` writes story files, dev agent writes code, E2E/QA agents
  write findings reports

The workflow XML orchestrates, routes, and presents output to the developer. It
never contains direct Edit/Write actions on project files. This matches the Impetus
constraint: "Impetus reads but NEVER writes files."

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

- [ ] Task 2 — Add momentum-tools subcommands (AC: deterministic operations)
  - [ ] `momentum-tools specialist-classify --touches "path1,path2,..."` — returns
    specialist name and agent file path (or fallback to dev.md). Uses the same
    classification table as sprint-planning Step 5. Deterministic, testable,
    consistent — eliminates LLM re-derivation of pattern matching.
  - [ ] `momentum-tools quickfix register --slug {slug} --story {key}` — creates
    a lightweight quickfix entry in sprints/index.json with slug, story, started date.
    No activate lifecycle.
  - [ ] `momentum-tools quickfix complete --slug {slug}` — sets completed date on
    the quickfix entry. No sprint complete lifecycle.
  - [ ] Add tests for both subcommands

- [ ] Task 3 — Create SKILL.md and command wrapper
  - [ ] Create `skills/momentum/skills/quick-fix/SKILL.md` with frontmatter
    (name: quick-fix, model: claude-opus-4-6, effort: high)
  - [ ] Create `skills/momentum/commands/quick-fix.md` command wrapper

- [ ] Task 4 — Create workflow.md (main deliverable)
  - [ ] Write the 5-phase workflow with XML structure matching sprint-dev/sprint-planning pattern
  - [ ] Include Outsider Test rules inline for Gherkin generation
  - [ ] Workflow invokes `momentum-tools specialist-classify` instead of LLM pattern matching
  - [ ] Workflow invokes `momentum-tools quickfix register/complete` for sprint record
  - [ ] Include cmux markdown surface opening for developer review in Phase 1 and 2
  - [ ] Include Dev + E2E collaborative fix loop for Phase 4

- [ ] Task 5 — Run evals and verify
  - [ ] Run each eval via subagent
  - [ ] Confirm skill is independently invocable
  - [ ] Confirm no multi-story overhead in the workflow

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → skill-instruction (EDD)
- Task 2 → script-code (TDD)
- Tasks 3, 4, 5 → skill-instruction (EDD)

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

---

### script-code Tasks: Test-Driven Development (TDD)

**Before writing the implementation:**
1. Write failing tests for each new subcommand in `test-momentum-tools.py`:
   - `specialist-classify`: test each pattern row, test multi-match majority rule,
     test tie-breaking, test no-match fallback to dev, test empty touches
   - `quickfix register`: test creates entry in sprints/index.json, test slug
     uniqueness, test started date
   - `quickfix complete`: test sets completed date, test error if slug not found

**Then implement:**
2. Add `specialist-classify` and `quickfix register/complete` subcommands to
   `momentum-tools.py`

**Then verify:**
3. Run `python3 test-momentum-tools.py` — all tests pass

**DoD items for script-code tasks:**
- [ ] Failing tests written before implementation
- [ ] All tests pass after implementation
- [ ] QA review confirms test coverage for edge cases
- [ ] CLI help text present for new subcommands

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
