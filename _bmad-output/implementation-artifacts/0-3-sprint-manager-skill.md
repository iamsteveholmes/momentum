# Story 0.3: Sprint-Manager Skill

Status: ready-for-dev

## Story

As a developer,
I want a dedicated `momentum-sprint-manager` executor subagent that is the sole writer of sprint-status.yaml,
so that all status transitions are atomic, auditable, and free from concurrent write conflicts.

## Acceptance Criteria

1. **Given** the `momentum-sprint-manager` skill is installed at `skills/momentum-sprint-manager/`
   **When** any workflow needs to update sprint-status.yaml (story status transition, sprint activation, epic membership change)
   **Then** the update is performed by spawning `momentum-sprint-manager` via Agent tool dispatch
   **And** no other agent or script writes to sprint-status.yaml directly

2. **Given** the sprint-manager receives a story status transition request
   **When** it updates sprint-status.yaml
   **Then** the story's `status` field in the `stories` section is updated
   **And** the sprint-manager validates the transition is legal (per the story state machine: backlog -> ready-for-dev -> in-progress -> review -> verify -> done)
   **And** `dropped` is accepted as a terminal state reachable from any non-terminal state
   **And** `closed-incomplete` is accepted as a terminal state reachable from any non-terminal state
   **And** illegal transitions (e.g., backlog -> done, or any transition from a terminal state without `force: true`) are rejected with an error message
   **And** the sprint-manager returns structured JSON confirmation: `{ "action": "status_transition", "story": "<slug>", "from": "<old>", "to": "<new>", "success": true }`

3. **Given** the sprint-manager receives a sprint activation request
   **When** it updates sprint-status.yaml
   **Then** the `sprints.active` section is populated with the sprint data (name, slug, stories, locked, started, waves)
   **And** the previous `sprints.planning` entry is moved to `sprints.active`
   **And** `locked` is set to `true` and `started` is set to the current date

4. **Given** the sprint-manager receives an epic membership change request
   **When** it updates sprint-status.yaml
   **Then** the story is added to or removed from the specified epic's `stories` list in the `epics` section

5. **Given** the legacy `update-story-status.sh` script exists at `skills/momentum/scripts/update-story-status.sh`
   **When** the sprint-manager skill is active
   **Then** all callers of `update-story-status.sh` are updated to invoke sprint-manager instead
   **And** the script file is marked deprecated with a comment header explaining the replacement

6. **Given** skills that currently write to sprint-status.yaml directly
   **When** the sprint-manager is deployed
   **Then** those skills are updated to delegate all sprint-status.yaml writes to sprint-manager via Agent tool dispatch
   **And** no skill retains direct write logic for sprint-status.yaml

7. **Given** the sprint-manager writes to sprint-status.yaml
   **When** the write completes
   **Then** the output YAML is valid (parseable without error)
   **And** all existing data not related to the requested change is preserved
   **And** comment blocks and section headers are preserved

8. **Given** the SKILL.md for momentum-sprint-manager
   **When** validated against Momentum NFRs
   **Then** the `description` field is <= 150 characters (NFR1)
   **And** `model:` and `effort:` frontmatter fields are present (FR23)
   **And** the skill body is <= 500 lines / 5000 tokens (NFR3)
   **And** the skill name is prefixed `momentum-` (NFR12)

## Tasks / Subtasks

- [ ] Task 1: Create `skills/momentum-sprint-manager/SKILL.md` (AC: #1, #8)
  - [ ] 1.1: Create the SKILL.md with frontmatter: `name: momentum-sprint-manager`, `description` (<= 150 chars), `model: sonnet`, `effort: medium`, `internal: true` (never invoked by users directly -- always dispatched by other skills via Agent tool). This is NOT a `context: fork` skill -- it is an executor subagent with write access. It does NOT get `allowed-tools` restrictions (unlike read-only verifiers like code-reviewer).
  - [ ] 1.2: Define the skill's input contract: it receives a structured command via its prompt (action type, target story/sprint/epic, new value). Define the supported actions: `status_transition`, `sprint_activate`, `epic_membership`, `sprint_plan`.
  - [ ] 1.3: Define the skill's output contract: structured JSON response with action, target, result, and success/failure indicator.
  - [ ] 1.4: Include the story state machine as a reference in the skill body or a references file: `backlog -> ready-for-dev -> in-progress -> review -> verify -> done` plus terminal states `dropped` and `closed-incomplete`.
  - [ ] 1.5: Include transition validation rules: only forward transitions are allowed by default; `dropped` and `closed-incomplete` are reachable from any non-terminal state; backward transitions require explicit `force: true` flag.
  - [ ] 1.6: Verify description is <= 150 characters, model/effort frontmatter present, body <= 500 lines.

- [ ] Task 2: Create `skills/momentum-sprint-manager/workflow.md` (AC: #2, #3, #4, #7)
  - [ ] 2.1: Define the workflow entry point: parse the incoming command to determine action type.
  - [ ] 2.2: Implement `status_transition` action: read sprint-status.yaml, find the story in `stories` section, validate the transition against the state machine, update the status field, write the file, return structured confirmation.
  - [ ] 2.3: Implement `sprint_activate` action: read sprint-status.yaml, move `sprints.planning` to `sprints.active`, set `locked: true`, set `started` to current date, write the file, return confirmation.
  - [ ] 2.4: Implement `epic_membership` action: read sprint-status.yaml, add/remove story from epic's stories list, write the file, return confirmation.
  - [ ] 2.5: Implement `sprint_plan` action: read sprint-status.yaml, create or update `sprints.planning` with provided stories and wave assignments, set `locked: false`, write the file, return confirmation.
  - [ ] 2.6: All actions must: validate YAML output parsability, preserve all data not related to the change, and preserve comment structure.

- [ ] Task 3: Create behavioral evals (AC: #2, #3, #7)
  - [ ] 3.1: Create `skills/momentum-sprint-manager/evals/eval-status-transition-valid.md` -- Given a story in `in-progress` status, when requesting transition to `review`, the skill should update the status and return success confirmation.
  - [ ] 3.2: Create `skills/momentum-sprint-manager/evals/eval-status-transition-invalid.md` -- Given a story in `backlog` status, when requesting transition to `done` (skipping intermediate states), the skill should reject with an error message and return success: false.
  - [ ] 3.3: Create `skills/momentum-sprint-manager/evals/eval-data-preservation.md` -- Given sprint-status.yaml with 10+ stories, when updating one story's status, the skill should preserve all other stories, epics, and sprint data unchanged.

- [ ] Task 4: Update callers of `update-story-status.sh` (AC: #5)
  - [ ] 4.1: Find all references to `update-story-status.sh` in skill files and workflows.
  - [ ] 4.2: Replace each call with Agent tool dispatch to `momentum-sprint-manager` with the appropriate `status_transition` command.
  - [ ] 4.3: Add deprecation header to `skills/momentum/scripts/update-story-status.sh`: `# DEPRECATED: Use momentum-sprint-manager skill instead. This script will be removed in a future version.`

- [ ] Task 5: Update skills that write sprint-status.yaml directly (AC: #6)
  - [ ] 5.1: Update `skills/momentum-create-story/workflow.md` -- replace direct sprint-status.yaml writes (status updates to `ready-for-dev`) with Agent dispatch to sprint-manager.
  - [ ] 5.2: Update `skills/momentum-dev/workflow.md` -- replace direct status writes (transitions during story development) with Agent dispatch to sprint-manager.
  - [ ] 5.3: Update `.claude/skills/bmad-create-story/workflow.md` -- replace direct sprint-status.yaml writes with Agent dispatch to sprint-manager.
  - [ ] 5.4: Update `.claude/skills/bmad-sprint-planning/workflow.md` -- replace direct sprint-status.yaml writes with Agent dispatch to sprint-manager.
  - [ ] 5.5: Update `.claude/skills/bmad-dev-story/workflow.md` -- replace direct sprint-status.yaml writes with Agent dispatch to sprint-manager.
  - [ ] 5.6: Update `skills/momentum-plan-audit/workflow.md` -- if it writes to sprint-status.yaml, replace with Agent dispatch. If read-only, no change needed.
  - [ ] 5.7: Review `.claude/skills/bmad-sprint-status/workflow.md` and `.claude/skills/bmad-retrospective/workflow.md` -- if they write to sprint-status.yaml, update; if read-only, no change needed.

- [ ] Task 6: Validate integration (AC: #1, #6)
  - [ ] 6.1: Verify no skill outside `momentum-sprint-manager` contains direct write logic for sprint-status.yaml (grep for Write/Edit tool calls targeting sprint-status).
  - [ ] 6.2: Verify all updated skills correctly construct the Agent dispatch command with the appropriate action type and parameters.
  - [ ] 6.3: Run the behavioral evals from Task 3 to confirm the skill functions correctly.

## Dev Notes

### Scope and Approach

This story creates a new executor subagent skill (`momentum-sprint-manager`) and migrates all sprint-status.yaml write operations across the codebase to delegate to it. The sprint-manager becomes the single point of control for all sprint-status.yaml mutations.

**Key design decision:** The sprint-manager is NOT a `context: fork` skill. Context-fork is for read-only verifiers (code-reviewer, architecture-guard) that need tool isolation. The sprint-manager needs full write access to `sprint-status.yaml` -- it is an executor subagent invoked via the Agent tool by the calling workflow.

### Architecture Compliance

**Write authority (Architecture, Architectural Boundaries section):**
> momentum-sprint-manager | sprint-status.yaml | sprint-status.yaml (sole writer)
> Impetus | sprint-status.yaml, journal.jsonl, specs, findings-ledger.jsonl | journal.jsonl, journal-view.md (NEVER writes sprint-status.yaml)
[Source: _bmad-output/planning-artifacts/architecture.md#Architectural Boundaries]

**Status update authority (Architecture, Sprint Tracking Schema section):**
> All writes to sprint-status.yaml go through `momentum-sprint-manager` -- an executor subagent with exclusive write authority over this file. No other agent or script writes to sprint-status.yaml directly. The legacy `update-story-status.sh` script is deprecated and will be removed during migration.
[Source: _bmad-output/planning-artifacts/architecture.md#Sprint Tracking Schema]

**Story State Machine (Architecture):**
```
backlog -> ready-for-dev -> in-progress -> review -> verify -> done
```
Terminal states: `dropped`, `closed-incomplete` (reachable from any non-terminal state)
[Source: _bmad-output/planning-artifacts/architecture.md#Story State Machine]

**Subagent Composition (Architecture, Decision 3a):**
> Hub-and-spoke: Impetus is the sole user-facing voice; subagents return structured output to Impetus for synthesis. Subagents cannot spawn subagents -- chains route through main conversation.
[Source: _bmad-output/planning-artifacts/architecture.md#Subagent Composition]

### Agent Dispatch Pattern

The sprint-manager is invoked via the Agent tool. The calling skill constructs a prompt like:

```
Update sprint-status.yaml:
Action: status_transition
Story: posttooluse-lint-hook
From: in-progress
To: review
```

The sprint-manager reads sprint-status.yaml, validates the transition, performs the update, and returns:

```json
{ "action": "status_transition", "story": "posttooluse-lint-hook", "from": "in-progress", "to": "review", "success": true }
```

### Skills That Currently Write sprint-status.yaml

These need to be updated to delegate writes to sprint-manager:

**Direct writers (confirmed):**
- `skills/momentum-create-story/workflow.md` -- writes `ready-for-dev` status
- `skills/momentum-dev/workflow.md` -- writes status transitions during development
- `skills/momentum/scripts/update-story-status.sh` -- shell script, deprecated
- `.claude/skills/bmad-create-story/workflow.md` -- writes `ready-for-dev` status
- `.claude/skills/bmad-sprint-planning/workflow.md` -- writes initial sprint structure
- `.claude/skills/bmad-dev-story/workflow.md` -- writes status transitions

**Possibly write (needs verification):**
- `skills/momentum-plan-audit/workflow.md`
- `.claude/skills/bmad-sprint-status/workflow.md`
- `.claude/skills/bmad-retrospective/workflow.md`

### Critical Constraints

1. **No context:fork:** The sprint-manager needs Write tool access. Do not use `context: fork` or `allowed-tools: Read` -- those are for read-only verifiers only.

2. **Structured output:** The sprint-manager must return structured JSON so callers can programmatically verify success. Free-form prose responses are not acceptable.

3. **State machine enforcement:** The sprint-manager must validate transitions. An illegal transition (e.g., `backlog -> done`) must be rejected, not silently applied.

4. **Data preservation:** Every write must preserve all data not related to the requested change. A status transition on one story must not alter any other story, epic, or sprint data.

5. **YAML validity:** Every write must produce valid YAML. The sprint-manager should validate its output before writing.

### Project Structure Notes

- **New skill directory:** `skills/momentum-sprint-manager/` (SKILL.md, workflow.md, evals/)
- **sprint-status.yaml location:** `_bmad-output/implementation-artifacts/sprint-status.yaml` (post-Story-0.2 schema)
- **Skills to update:** 6-9 workflow files that currently write sprint-status.yaml
- **Script to deprecate:** `skills/momentum/scripts/update-story-status.sh`

### References

- [Source: _bmad-output/planning-artifacts/architecture.md#Architectural Boundaries] -- read/write authority table
- [Source: _bmad-output/planning-artifacts/architecture.md#Sprint Tracking Schema] -- sole writer authority, schema
- [Source: _bmad-output/planning-artifacts/architecture.md#Story State Machine] -- valid transitions
- [Source: _bmad-output/planning-artifacts/architecture.md#Subagent Composition] -- hub-and-spoke pattern
- [Source: _bmad-output/planning-artifacts/epics.md#Epic 0: Redesign Foundation] -- story requirements, sequencing

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2 -> skill-instruction (EDD)
- Task 3 -> skill-instruction (evals, part of EDD cycle)
- Tasks 4, 5 -> skill-instruction (updating existing workflows)
- Task 6 -> config-structure (validation)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts -- unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2-3 behavioral evals in `skills/momentum-sprint-manager/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-status-transition-valid.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior -- what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the SKILL.md, workflow.md, or reference files

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context (or invoke the skill via its Agent Skills name if installed). Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match -> task complete
5. If any eval fails -> diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance -- mandatory for every skill-instruction task:**
- SKILL.md `description` field must be <= 150 characters (NFR1) -- count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3)
- Skill names prefixed `momentum-` (NFR12 -- no naming collision with BMAD skills)

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum-sprint-manager/evals/`
- [ ] EDD cycle ran -- all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description <= 150 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body <= 500 lines / 5000 tokens confirmed (overflow in `references/` if needed)
- [ ] AVFL checkpoint on produced artifact documented (momentum-dev runs this automatically -- validates the implemented SKILL.md against story ACs)

### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by inspection:

1. **Verify** no skill outside `momentum-sprint-manager` contains direct write logic for sprint-status.yaml
2. **Verify** all Agent dispatch commands are correctly structured
3. **Document** what was verified in the Dev Agent Record

**DoD items for config-structure tasks:**
- [ ] All referenced paths exist after creation
- [ ] Changes documented in Dev Agent Record

---

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
