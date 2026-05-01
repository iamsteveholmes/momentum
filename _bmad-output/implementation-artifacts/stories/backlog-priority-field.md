---
title: Backlog Priority Field — Add Priority to All Story Index Entries
status: ready-for-dev
epic_slug: impetus-core
story_key: backlog-priority-field
depends_on: []
touches:
  - _bmad-output/implementation-artifacts/stories/index.json
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
  - skills/momentum/skills/sprint-planning/workflow.md
change_type: code + skill-instruction
derives_from:
  - path: docs/planning-artifacts/momentum-master-plan.md
    relationship: derives_from
    section: "Part 4 Architecture Decisions — Decision 36 (table row)"
  - path: skills/momentum/references/sprint-tracking-schema.md
    relationship: derives_from
    section: "Story Priority"
---

# Story: Backlog Priority Field

Status: ready-for-dev

## Story

As a Momentum developer planning sprints,
I want every story in the backlog to carry a priority (critical, high, medium, low),
so that sprint planning can surface the most important work first and I can make informed selection decisions.

## Acceptance Criteria

### AC1: Priority Field Exists on All Stories

- Every entry in `stories/index.json` has a `priority` field
- Valid values: `critical`, `high`, `medium`, `low`
- All existing stories receive `low` as their default priority
- New stories created without an explicit priority default to `low`

### AC2: momentum-tools CLI Can Set Priority

- A new `sprint set-priority` subcommand exists: `momentum-tools sprint set-priority --story <slug> --priority <level>`
- The command validates the priority value against the allowed set (critical, high, medium, low)
- The command rejects invalid priority values with a clear error message
- The command returns structured JSON confirming the story slug, old priority, and new priority
- The command fails gracefully if the story slug doesn't exist in stories/index.json
- Both users and agents use the same CLI command; when an agent suggests a priority during workflows (e.g., create-story, epic-grooming), the agent proposes via output and the user confirms before the CLI call is made

### AC3: momentum-tools CLI Can Query by Priority

- The existing `sprint plan --operation add` workflow continues to work unchanged
- A new query capability exists: `momentum-tools sprint stories --priority <level>` returns all stories matching that priority
- `momentum-tools sprint stories --priority all` returns stories grouped by priority (critical first, then high, medium, low)

### AC4: Sprint Planning Displays Priority

- Sprint-planning workflow Step 1 (backlog presentation) displays priority alongside each story
- Stories within each epic group are sorted by: priority (critical > high > medium > low), then dependency depth (leaves first), then alphabetical
- The priority is displayed using a compact format: `[C]`, `[H]`, `[M]`, `[L]`

### AC5: Unit Tests Cover All Priority Operations

- All new momentum-tools subcommands have unit tests in `test-momentum-tools.py`
- Tests cover: set valid priority, reject invalid priority, missing story, default priority on new entries, query by priority, grouped query output
- All existing tests continue to pass (no regressions)

## Tasks / Subtasks

- [ ] Task 1: Add `priority` field to all entries in stories/index.json (AC: 1)
  - [ ] 1.1: Write migration logic in momentum-tools.py that adds `"priority": "low"` to any entry missing the field
  - [ ] 1.2: Run migration on the current stories/index.json to populate all entries
  - [ ] 1.3: Ensure the field persists through all existing read/write operations (status-transition, epic-membership, sprint plan)

- [ ] Task 2: Add `sprint set-priority` subcommand to momentum-tools.py (AC: 2, 5)
  - [ ] 2.1: Add argparse subcommand under the `sprint` group with `--story` and `--priority` arguments
  - [ ] 2.2: Implement validation against allowed values
  - [ ] 2.3: Implement JSON read-modify-write with old/new priority in response
  - [ ] 2.4: Write unit tests: valid set, invalid priority, missing story, idempotent set

- [ ] Task 3: Add `sprint stories` query subcommand to momentum-tools.py (AC: 3, 5)
  - [ ] 3.1: Add argparse subcommand `sprint stories` with `--priority` argument
  - [ ] 3.2: Implement single-priority filter (returns matching stories)
  - [ ] 3.3: Implement `--priority all` grouped output (critical → high → medium → low)
  - [ ] 3.4: Write unit tests: single filter, grouped output, empty results

- [ ] Task 4: Update sprint-planning workflow Step 1 to display priority (AC: 4)
  - [ ] 4.1: Add priority display in compact format `[C]`/`[H]`/`[M]`/`[L]` after each story title
  - [ ] 4.2: Update sort order within epic groups: priority first, then dependency depth, then alphabetical

## Dev Notes

### Key Implementation Context

**Write authority:** `momentum-tools.py` is the sole writer of `stories/index.json` fields (per architecture decision). All priority mutations must go through the CLI, not direct JSON edits by agents.

**CLI pattern:** Follow the existing subcommand structure in momentum-tools.py. The `sprint` command group has subparsers for `plan`, `activate`, `complete`, `ready`, `retro-complete`, `status-transition`, `epic-membership`, `stats`. Add `set-priority` and `stories` as new subparsers.

**Test pattern:** Tests in `test-momentum-tools.py` use subprocess calls to invoke momentum-tools.py. Each test creates a temp project directory via `setup_project()`, writes a minimal stories/index.json, runs the CLI, and asserts on the JSON output and file mutations.

**Migration approach:** The priority field should be added lazily — when momentum-tools reads stories/index.json and encounters an entry without `priority`, it should inject `"low"` as the default. However, Task 1.2 also does a one-time explicit migration to populate all existing entries, so the lazy path is a safety net.

**Sprint-planning integration:** The workflow at `skills/momentum/skills/sprint-planning/workflow.md` Step 1 currently sorts by dependency depth then alphabetical. Adding priority as the primary sort key within each epic group is a workflow instruction change (skill-instruction type, not code).

### Project Structure Notes

- `skills/momentum/scripts/momentum-tools.py` — primary code file (add subcommands)
- `skills/momentum/scripts/test-momentum-tools.py` — test file (add test cases)
- `_bmad-output/implementation-artifacts/stories/index.json` — data file (populate priority field)
- `skills/momentum/skills/sprint-planning/workflow.md` — workflow file (update Step 1 display)
- `skills/momentum/references/sprint-tracking-schema.md` — already documents priority field (no changes needed)

### References

- [Decision 36]: `docs/planning-artifacts/momentum-master-plan.md` — Backlog Priority Field decision
- [Schema]: `skills/momentum/references/sprint-tracking-schema.md` — Story Priority section
- [sprint-lifecycle-tools story]: `_bmad-output/implementation-artifacts/stories/sprint-lifecycle-tools.md` — similar pattern (added fields + CLI commands + tests)
- [momentum-tools.py]: `skills/momentum/scripts/momentum-tools.py` — existing CLI structure
- [test file]: `skills/momentum/scripts/test-momentum-tools.py` — existing test patterns

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3 → script-code (TDD)
- Task 4 → skill-instruction (EDD)

---

#### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). bmad-dev-story handles TDD natively — the implementation guidance below matches its standard approach:

1. **Red:** Write failing tests for the task's functionality first. Confirm they fail before implementing.
2. **Green:** Implement the minimum code to make tests pass. Run tests to confirm.
3. **Refactor:** Improve code structure while keeping tests green.

**Note:** Scripts in Momentum live under `skills/momentum/scripts/`. Follow the pattern in existing Momentum scripts for language choice and structure.

**DoD items for script-code tasks (bmad-dev-story standard DoD applies — listed here for reference):**
- [ ] Tests written and passing
- [ ] No regressions in existing test suite
- [ ] Code quality checks pass if configured

---

#### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/sprint-planning/evals/` (evals/ already exists):
   - One `.md` file per eval, named descriptively (e.g., `eval-priority-display.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the workflow.md

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3)
- Skill names prefixed `momentum-` (NFR12 — no naming collision with BMAD skills)

**Additional DoD items for this story:**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/sprint-planning/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed
- [ ] AVFL checkpoint on produced artifact documented

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

- `.claude/momentum/sprint-logs/sprint-2026-04-06/dev-backlog-priority-field.jsonl`

### Completion Notes List

- Task 1: `sprint migrate-priority` subcommand added; one-time migration run on stories/index.json — 109 entries updated to `priority: "low"`
- Task 2: `sprint set-priority --story <slug> --priority <level>` added; validates against critical/high/medium/low; returns old_priority and new_priority in JSON output
- Task 3: `sprint stories --priority <level>` added; `--priority all` returns stories grouped by priority (critical→high→medium→low); entries missing priority field treated as low
- Task 4: sprint-planning workflow.md Step 1 updated — priority badge `[C]/[H]/[M]/[L]` added to each story display; sort order changed to priority > dependency depth > alphabetical; 3 behavioral evals written and confirmed
- All 310 tests pass, 0 failures; no regressions in existing test suite
- EDD evals: eval-priority-display.md, eval-priority-sort-order.md, eval-priority-sort-tiebreak.md — all pass against updated workflow instructions

### File List

- `skills/momentum/scripts/momentum-tools.py` — added PRIORITY_LEVELS, ensure_priority, cmd_sprint_migrate_priority, cmd_sprint_set_priority, cmd_sprint_stories, argparse subcommands
- `skills/momentum/scripts/test-momentum-tools.py` — added 11 TDD tests for Tasks 1-3
- `_bmad-output/implementation-artifacts/stories/index.json` — migrated: all 109 stories now have `priority: "low"`
- `skills/momentum/skills/sprint-planning/workflow.md` — Step 1 updated: priority badge display + sort order
- `skills/momentum/skills/sprint-planning/evals/eval-priority-display.md` — new eval
- `skills/momentum/skills/sprint-planning/evals/eval-priority-sort-order.md` — new eval
- `skills/momentum/skills/sprint-planning/evals/eval-priority-sort-tiebreak.md` — new eval
