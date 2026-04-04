---
title: Sprint Dev — Dependency-Driven Execution Loop with Team Agents
status: ready-for-dev
epic_slug: impetus-core
depends_on:
  - momentum-dev-simplify
  - momentum-sprint-planning
touches:
  - skills/momentum/workflows/sprint-dev.md
  - skills/momentum/workflow.md
  - skills/momentum/scripts/momentum-tools.py
change_type: skill-instruction
---

# Sprint Dev

## Goal

Build the sprint execution workflow module that Impetus loads to run an active sprint.
Sprint-dev is the core execution loop: it reads the activated sprint record, spawns a
team of momentum-dev agents (one per unblocked story, each in its own worktree), tracks
progress via tasks, handles dependency-driven sequencing, runs post-merge AVFL, executes
black-box verification against Gherkin specs, and surfaces a sprint summary when complete.

This is the workflow that turns a sprint plan into committed, verified code.

## Acceptance Criteria

- Impetus loads `skills/momentum/workflows/sprint-dev.md` when the developer selects
  "Continue sprint" from the Mode 1 session menu
- The workflow creates a task list representing all sprint stories and their dependency
  relationships, so Impetus can track progress without losing context
- Team composition and dependency graph are read from the active sprint record in
  `sprints/index.json` — sprint-dev never invents its own team plan
- One momentum-dev agent is spawned per unblocked story (no unmet dependencies), each
  in its own git worktree at `.worktrees/story-{story-slug}`
- Each spawned agent receives its role-specific guidelines from the sprint record's
  team composition
- All agents log decisions, errors, retries, assumptions, findings, and ambiguities
  via `momentum-tools log` throughout execution
- When a story completes and merges to main, sprint-dev checks whether any previously
  blocked stories are now unblocked and spawns agents for those
- Stories are never spawned before all their dependencies have merged — dependency
  ordering is strict
- After all sprint stories have merged, a single AVFL pass runs against the full
  codebase — not per-story
- After AVFL, verification runs: verifier agents read Gherkin specs from
  `sprints/{sprint-slug}/specs/` and validate behavior against the merged codebase
- Dev agents never access the `sprints/{sprint-slug}/specs/` directory — verification
  is black-box
- In Phase 3, verification takes the form of a developer-confirmation checklist
  derived from Gherkin scenarios — full automated verification is deferred
- On successful verification, all sprint stories are transitioned to `done` via
  `momentum-tools sprint status-transition`
- The workflow surfaces a sprint summary showing story count, merge order, AVFL
  findings resolved, and verification results
- The summary suggests running a retrospective as the next step

## Dev Notes

### What exists today
- `skills/momentum/workflow.md` has Mode 1 menu item "[1] Continue sprint" that currently
  dispatches to momentum-dev (sprint-continue variant) — this is a placeholder
- `momentum-tools.py` provides `sprint status-transition`, `sprint activate`, and
  `sprint complete` subcommands
- `momentum-tools.py` will have a `log` subcommand by the time this story starts (depends
  on agent-logging-tool, which is a dependency of momentum-dev-simplify)
- momentum-dev (post-simplify) is a pure executor: worktree setup + bmad-dev-story + return
  merge-ready output — no AVFL, no status writes
- Sprint records in `sprints/index.json` will contain team composition and dependency graph
  (written by momentum-sprint-planning)
- Gherkin specs live at `sprints/{sprint-slug}/specs/{story-slug}.feature` (written during
  sprint planning, never seen by dev agents)

### What to create
- `skills/momentum/workflows/sprint-dev.md` — the workflow module, structured as a
  step-by-step instruction set that Impetus follows

The workflow must define these phases:

**Phase 1: Initialization**
1. Read the active sprint from `sprints/index.json`
2. Validate sprint is active and locked
3. Read all story entries from `stories/index.json` for stories in the sprint
4. Build the dependency graph from story `depends_on` fields
5. Create a task per story via TaskCreate with dependency metadata in the description
6. Log sprint start via `momentum-tools log --agent impetus --sprint {slug} --event decision --detail "Sprint execution started: {N} stories, {M} unblocked"`

**Phase 2: Team spawn**
1. Identify unblocked stories (no dependencies, or all dependencies already `done`)
2. Transition each unblocked story to `in-progress` via `momentum-tools sprint status-transition`
3. Spawn one momentum-dev agent per unblocked story:
   - Worktree: `.worktrees/story-{story-slug}` on branch `story/{story-slug}`
   - Pass role guidelines from sprint record's team composition
   - Pass story file path and sprint context
   - Agent logs all activity via momentum-tools log
4. Update corresponding tasks to `in_progress`

**Phase 3: Progress tracking loop**
1. Monitor spawned agents via task status
2. When a story's agent signals completion (task marked complete):
   a. Verify merge readiness (agent reports merge-ready)
   b. Propose merge to developer — wait for confirmation
   c. After merge: run `momentum-tools sprint status-transition --story {slug} --target review`
   d. Check dependency graph: find stories whose blockers are all now merged
   e. Spawn agents for newly unblocked stories (back to Phase 2 spawn logic)
   f. Log the completion and any new spawns
3. Repeat until all stories have merged

**Phase 4: Post-merge quality gate**
1. Run single AVFL pass on the full codebase (all sprint changes together)
2. If AVFL produces findings: present to developer, iterate fixes
3. Log AVFL results

**Phase 5: Verification**
1. Read all `.feature` files from `sprints/{sprint-slug}/specs/`
2. For each feature file: extract scenario names and expected behaviors
3. Present developer-confirmation checklist:
   - Each Gherkin scenario becomes a checkbox item
   - Developer confirms each behavior is present and correct
   - Any unconfirmed items become findings to address
4. Log verification results
5. On full confirmation: transition all stories to `done` via status-transition

**Phase 6: Sprint completion**
1. Run `momentum-tools sprint complete` to archive the sprint
2. Surface sprint summary:
   - Stories completed: count and list
   - Merge order (actual execution sequence)
   - AVFL findings: count found, count resolved
   - Verification: scenarios confirmed vs. total
   - Agent log location for retro
3. Suggest: "Sprint complete. Ready for retro? That's where the real learning happens."

### What to change in existing files
- Update `skills/momentum/workflow.md` Mode 1 dispatch: replace the placeholder
  "Dispatch to momentum-dev workflow (sprint-continue variant)" with
  "Load and follow `${CLAUDE_SKILL_DIR}/workflows/sprint-dev.md`"
- Ensure the `workflows/` directory exists under `skills/momentum/`

### What NOT to change
- Do not modify momentum-dev itself — it is already simplified by its own story
- Do not modify momentum-tools.py beyond what is needed (this story primarily creates
  the workflow file, not CLI changes)
- Do not implement automated Gherkin test execution — Phase 3 uses developer-confirmation
  checklist; automated verification is deferred to momentum-verify-skill
- Do not modify sprint-planning — team composition and dependency graph are its output
- Do not change the AVFL skill — invoke it as-is

### Key architectural constraints
- **Teams over waves:** Stories are spawned based on dependency resolution, not wave
  numbers. Multiple stories can run concurrently if they share no dependencies. A story
  with dependencies waits until ALL its blockers have merged.
- **Impetus always spawns:** Sprint-dev is an Impetus workflow. Impetus spawns all agents
  directly. No agent spawns another agent.
- **Exclusive write authority:** Each momentum-dev agent owns its worktree exclusively.
  Sprint-dev owns task tracking and status transitions. momentum-tools owns index.json
  mutations.
- **Merge gate:** Every merge requires explicit developer confirmation. Sprint-dev
  proposes the merge and waits — never auto-executes.
- **AVFL runs once:** After ALL stories merge, not after each. This catches cross-story
  integration issues that per-story AVFL would miss.
- **Black-box verification:** Dev agents never see Gherkin specs. Verifiers never see
  implementation details. The specs were written during planning before any code existed.

### Sprint record structure (expected from sprint-planning)
The active sprint record in `sprints/index.json` is expected to contain:
```json
{
  "active": {
    "slug": "phase-3-sprint-execution",
    "locked": true,
    "started": "2026-04-02",
    "stories": ["agent-logging-tool", "momentum-dev-simplify", ...],
    "team": {
      "roles": [
        {"role": "dev", "guidelines": "path/to/project-dev-guidelines.md"},
        {"role": "qa", "guidelines": "path/to/project-qa-guidelines.md"}
      ],
      "story_assignments": {
        "agent-logging-tool": {"role": "dev"},
        "momentum-dev-simplify": {"role": "dev"}
      }
    },
    "dependencies": {
      "momentum-dev-simplify": ["agent-logging-tool"],
      "momentum-sprint-dev": ["momentum-dev-simplify", "momentum-sprint-planning"]
    }
  }
}
```

### Error handling
- If no active sprint exists: surface error and return to session menu
- If sprint is not locked: surface error (sprint-planning did not complete activation)
- If a momentum-dev agent fails: log the failure, surface to developer, offer retry or
  skip options — do not auto-retry
- If merge conflicts occur: surface to developer with diff context — developer resolves
- If AVFL finds critical issues: block verification until resolved
- If developer declines a verification item: log as finding, offer to create a follow-up
  story
