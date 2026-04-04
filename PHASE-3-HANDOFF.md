# Phase 3 Sprint Execution — Handoff

## Full Plans

- Redesign plan: `~/.claude/plans/ethereal-popping-sun.md`
- Sprint execution plan: `~/.claude/plans/dapper-scribbling-hejlsberg.md`

## What's Done

### Phase 2 (Complete — all stories in review)
- `momentum-tooling` — Python CLI (`momentum-tools.py`) with 5 sprint subcommands + version check. 95 tests passing.
- `impetus-identity-redesign` — KITT-like servant-partner character. Identity section + refined greeting.
- `session-open-sprint-view` — 3-mode sprint detection, 16-block fill bars, context menus.

### Phase 3 Round 1 (Complete)
- `agent-logging-tool` — `log` subcommand added to momentum-tools.py. 6 event types (decision, error, retry, assumption, finding, ambiguity). `--sprint` optional with `_unsorted/` fallback. 95 tests (65 sprint + 30 log). QA 8/8, Validator 17/17.

### Phase 3 Round 2 (Complete)
- `momentum-dev-simplify` — Stripped AVFL, status transitions, DoD, code review from momentum-dev. Added agent logging at 5 decision points + 2 error points. 314→210 lines. Pure executor: worktree + bmad-dev-story + logging + merge-ready output. QA 8/8, Validator 19/20 (1 fixed: merge conflict error log).
- `momentum-sprint-planning` — New workflow module at `skills/momentum/workflows/sprint-planning.md` (342 lines, 8 steps). Backlog display, story selection (3-8), create-story on stubs, Gherkin spec generation to `sprints/{slug}/specs/`, team composition with two-layer model, AVFL on complete plan, developer review, sprint activation. Mode 3 menu dispatch wired. QA 16/16, Validator 29/30 (1 fixed: touches overlap detection).

### Phase 3 Round 3 (NOT STARTED)
- `momentum-sprint-dev` — Sprint execution workflow module. Story file + Gherkin specs exist. Story is `ready-for-dev` in index.json.

## Current Story Statuses

| Story | Status |
|-------|--------|
| `agent-logging-tool` | review |
| `momentum-dev-simplify` | review |
| `momentum-sprint-planning` | review |
| `momentum-sprint-dev` | ready-for-dev |

## Gherkin Specs Location

`_bmad-output/implementation-artifacts/sprints/phase-3-sprint-execution/specs/`
- `agent-logging-tool.feature` — 17 scenarios
- `momentum-dev-simplify.feature` — 20 scenarios
- `momentum-sprint-planning.feature` — 30 scenarios
- `momentum-sprint-dev.feature` — 28 scenarios (for Round 3)

## Key Architecture Decisions (this session)

| # | Decision |
|---|----------|
| 24 | Agent logging — every agent writes JSONL via momentum-tools log |
| 25 | Teams over waves — dependency-driven concurrency |
| 26 | Two-layer agent model — Momentum roles + project guidelines |
| 27 | Two-output retro — Momentum triage + Project triage from logs |
| 28 | Triage vs refinement — triage = intake, refinement = organization |
| 29 | Sprint planning builds the team — roles, guidelines, dependency graph |
| 30 | Gherkin separation — plain English ACs in stories, .feature files for verifiers only |
| 31 | AVFL at sprint level — validates complete plan, not per-story |

## File Structure

```
skills/
  momentum/                          # Impetus (orchestrator)
    SKILL.md
    workflow.md                      # Main workflow (session-open, routing)
    workflows/
      sprint-planning.md             # NEW — workflow module (Round 2)
      sprint-dev.md                  # Round 3 will create this
    scripts/
      momentum-tools.py              # CLI: sprint, log, version subcommands
      test-momentum-tools.py         # 95 tests passing

  momentum-dev/                      # Dev executor (separate skill, spawned as agent)
    SKILL.md
    workflow.md                      # Simplified in Round 2

_bmad-output/implementation-artifacts/
  stories/
    index.json                       # Story registry (4 Phase 3 stories added)
    agent-logging-tool.md
    momentum-dev-simplify.md
    momentum-sprint-planning.md
    momentum-sprint-dev.md
  sprints/
    index.json                       # Sprint tracking
    phase-3-sprint-execution/
      specs/                         # Gherkin specs (verifier-only)
        *.feature

.claude/momentum/
  sprint-logs/                       # Agent logs (created at runtime)
    {sprint-slug}/
      {agent}-{story}.jsonl
```

## Concepts Clarified (Claude Code vs Momentum)

| Concept | Claude Code | Momentum |
|---------|-------------|----------|
| Skill | SKILL.md — instructions loaded into context | Same |
| Agent | Isolated execution environment (`.agent.md` or Agent tool) | "Executor" — spawned by Impetus |
| Workflow module | Not a platform concept | Instruction document Impetus reads inline |
| Sub-commands (`momentum:X`) | Not native syntax | Pattern matching within momentum skill |
| `context: fork` | Runs skill in isolated subagent context | Used for read-only reviewers |

## What's Next — Round 3

Execute `momentum-sprint-dev`:
1. Create team (dev + QA + validator)
2. Dev writes `skills/momentum/workflows/sprint-dev.md` + updates Mode 1 menu dispatch
3. QA reviews against 16 ACs
4. Validator tests against 28 Gherkin scenarios
5. Fix findings, commit, merge

Then Round 4: post-merge AVFL on full codebase, transition all stories to done.

## Cleanup Needed

- Stale team: `~/.claude/teams/phase-3-round-2/` — dev-simplify agent wouldn't shut down. Delete manually: `rm -rf ~/.claude/teams/phase-3-round-2 ~/.claude/tasks/phase-3-round-2`

## Spec Documents Updated

- `_bmad-output/planning-artifacts/architecture.md` — Decisions 24-31, write authority table, sprint orchestration
- `_bmad-output/planning-artifacts/prd.md` — FR56-FR70, sprint lifecycle, 8 existing FRs updated
- `_bmad-output/planning-artifacts/research/phase-3-architecture-discovery.md`
- `_bmad-output/planning-artifacts/research/phase-3-prd-discovery.md`
