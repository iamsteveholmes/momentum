---
title: Sprint Planning Workflow — Story Selection, Spec Generation, and Team Composition
status: ready-for-dev
epic_slug: impetus-core
depends_on:
  - agent-logging-tool
touches:
  - skills/momentum/workflows/sprint-planning.md
  - skills/momentum/workflow.md
  - _bmad-output/implementation-artifacts/sprints/index.json
change_type: skill-instruction
---

# Sprint Planning Workflow

## Goal

Create the sprint planning workflow module that Impetus loads when a developer selects
"Plan a sprint" from the session menu. This workflow takes the developer from a
prioritized backlog view through story selection, story fleshing-out, Gherkin spec
generation, team composition, AVFL validation, and sprint activation — producing a
fully specified, developer-approved sprint ready for execution.

The workflow enforces a key architectural separation: story files contain plain English
acceptance criteria (so dev agents see intent), while detailed Gherkin specs go to a
sprint-scoped specs directory that only verifiers access. Developers never see the
Gherkin during implementation — this is black-box validation by design.

## Acceptance Criteria

- Impetus displays the prioritized backlog from stories/index.json, grouped by epic,
  showing each story's title, status, dependencies, and epic membership
- Stories already in terminal states (done, dropped, closed-incomplete) are excluded
  from the backlog display
- Stories with unsatisfied dependencies are visually marked but still selectable
  (developer may know those dependencies will complete soon)
- The developer selects 3-8 stories for the sprint; Impetus validates the count and
  warns if dependency chains create risk
- For each selected story stub, Impetus spawns momentum-create-story to flesh it out
  with tasks, plain English summary ACs, and dev notes; the developer evaluates and
  approves each before proceeding
- Stories that already have full story files (story_file: true in index.json) skip
  the create-story step — Impetus surfaces their existing content for developer review
- After all stories are approved, Impetus generates detailed Gherkin specifications
  for each story and writes them to `sprints/{sprint-slug}/specs/{story-slug}.feature`
- The Gherkin specs directory is exclusively for verifier agents — the workflow does
  not expose these specs to dev agents or include them in story files
- Story markdown files retain only plain English ACs — Gherkin is never written back
  to story files
- Impetus builds an execution plan covering team composition: which agent roles the
  sprint needs, what project-specific guidelines each role receives, and which stories
  can run concurrently based on the dependency graph
- The team composition uses a two-layer model: Momentum provides generic agent roles
  (Dev, QA, E2E Validator), and the project provides stack-specific guidelines for
  each role
- The dependency graph identifies execution waves — groups of stories that can run
  in parallel because they have no inter-dependencies
- Impetus runs AVFL on the complete sprint plan (all stories together as a single
  validation pass, not per-story)
- The developer reviews the full sprint plan — stories, team composition, dependency
  graph, and execution waves — and can request adjustments before approval
- Upon developer approval, Impetus activates the sprint via `momentum-tools sprint
  activate`, storing team composition and dependency graph in the sprint record
- All planning decisions are logged via the agent logging tool throughout the workflow

## Dev Notes

### What exists today
- `skills/momentum/workflow.md` Step 7 Mode 3 menu offers "Plan a sprint" but
  dispatches to a placeholder message: "This workflow (momentum:sprint-plan) is coming
  in the next phase"
- `momentum-tools.py` has `sprint plan --operation add|remove --stories SLUG[,SLUG...]
  --wave N` for manipulating the planning sprint, and `sprint activate` for activation
- `sprints/index.json` tracks active/planning/completed sprint state
- `stories/index.json` tracks all stories with status, epic, dependencies, touches
- `momentum-create-story` skill exists and can flesh out story stubs

### What to create
- `skills/momentum/workflows/sprint-planning.md` — the workflow module document that
  Impetus loads and follows step-by-step
- The workflow should be structured as numbered steps with clear entry/exit conditions,
  developer approval gates, and Impetus voice throughout

### Workflow structure (8 steps)

**Step 1 — Backlog Presentation**
Read stories/index.json. Group by epic_slug. For each epic, list stories with:
title, status, depends_on. Exclude terminal states. Sort by: dependency depth
(leaves first), then alphabetical within depth. Display count summary at top.

**Step 2 — Story Selection**
Developer selects stories by number or slug. Validate: 3-8 stories. Flag dependency
warnings (selecting a story whose dependency is not done and not in this sprint).
Use `momentum-tools sprint plan --operation add` to register selections. Name the
sprint with a slug derived from date + sequence (e.g., `sprint-2026-04-03`).

**Step 3 — Story Fleshing-Out**
For each selected story where `story_file` is false or the story file is a stub:
spawn momentum-create-story. Present the fleshed-out story to the developer for
approval. Developer can request revisions or accept. Stories with existing full
files: surface content for review, skip create-story.

**Step 4 — Gherkin Spec Generation**
For each approved story: generate detailed Gherkin feature specs. Write to
`sprints/{sprint-slug}/specs/{story-slug}.feature`. These specs encode the
detailed behavioral expectations that verifier agents will check against. The
story markdown files are NOT modified — they keep plain English ACs only.

**Step 5 — Execution Plan and Team Composition**
Analyze the selected stories to determine:
- Agent roles needed (based on story change_type and touches paths)
- Project-specific guidelines for each role (from project config if available)
- Dependency graph: which stories block which
- Execution waves: groups of stories that can run concurrently
Store wave assignments via `momentum-tools sprint plan --wave N`.

**Step 6 — AVFL Validation**
Run AVFL on the complete sprint plan — all story files, all Gherkin specs, the
team composition, and the execution plan validated together as one unit. This
catches cross-story conflicts, gap coverage, and planning coherence issues.

**Step 7 — Developer Review**
Present the complete sprint plan:
- Sprint name and story count
- Per-story summary (title, wave assignment, agent role)
- Team composition table (role, guidelines, story assignments)
- Dependency graph (which stories block which, wave structure)
- AVFL results summary
Developer can request adjustments (add/remove stories, change waves, modify
team composition) or approve.

**Step 8 — Sprint Activation**
On developer approval: call `momentum-tools sprint activate`. This locks the
planning sprint and transitions it to active. Log the activation decision.
Present confirmation with sprint name and start date.

### What to change in existing files
- Update `skills/momentum/workflow.md` Step 7 Mode 3 dispatch for "Plan a sprint"
  to load and follow `workflows/sprint-planning.md` instead of showing the placeholder
- Create `skills/momentum/workflows/` directory if it doesn't exist

### Two-layer agent model
Momentum provides generic roles with orchestration patterns:
- **Dev** — implements stories in worktrees, logs decisions
- **QA** — reviews code against acceptance criteria
- **E2E Validator** — validates end-to-end behavior against Gherkin specs
- **Architect Guard** — checks pattern drift against architecture decisions

Projects provide stack-specific guidelines per role:
- "Frontend Dev uses Kotlin Multiplatform + Compose, TDD required"
- "Backend Dev uses PydanticAI + FastAPI, type hints on all public APIs"
- "E2E uses CMUX + Maestro, screenshot assertions required"

Sprint planning wires these together: for each story, determine which roles apply
based on `change_type` and `touches`, then attach the project's guidelines for
those roles.

### What NOT to change
- Do not modify momentum-tools.py — the existing sprint plan and activate commands
  are sufficient
- Do not modify stories/index.json schema — read it as-is
- Do not modify sprints/index.json schema — the existing planning/active/completed
  structure is sufficient
- Do not add Gherkin to story markdown files — the separation is intentional
- Do not run AVFL per-story — it runs once on the complete plan

### Sprint slug convention
Format: `sprint-YYYY-MM-DD` (date of planning). If multiple sprints planned on the
same day, append sequence: `sprint-2026-04-03-2`.

### Dependency on agent-logging-tool
All planning decisions, story approvals, and AVFL results must be logged via the
agent logging tool. The log subcommand must exist before this workflow can execute.
