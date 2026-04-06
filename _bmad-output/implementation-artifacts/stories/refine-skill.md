---
title: Refine Skill — Backlog Grooming with PM and Architect
story_key: refine-skill
status: ready-for-dev
epic_slug: impetus-epic-orchestrator
depends_on:
  - backlog-priority-field
touches:
  - skills/momentum/skills/refine/SKILL.md
  - skills/momentum/skills/refine/workflow.md
  - skills/momentum/skills/impetus/SKILL.md
change_type: skill-instruction
derives_from:
  - path: docs/planning-artifacts/momentum-master-plan.md
    relationship: derives_from
    section: "Decision 28 — Triage vs refinement"
  - path: docs/planning-artifacts/momentum-master-plan.md
    relationship: derives_from
    section: "Command Table — /momentum:refine"
---

# Refine Skill — Backlog Grooming with PM and Architect

## Description

Decision 28 draws the line: triage is intake (analyze, create stubs, initial
priority); refinement is organization (classify, prioritize, gap-analyze).
Sprint planning already presents the backlog and lets the developer select
stories, but it has no step for holistic backlog health — identifying gaps
against the PRD and architecture, flagging stale stories, resolving
dependency tangles, or adjusting priorities across the full backlog.

This story creates `momentum:refine` as a SKILL.md + workflow.md pair that
reads the entire backlog holistically, runs parallel discovery agents to
compare it against the PRD and architecture, presents findings to the
developer, and applies approved changes via the momentum-tools CLI. It
delegates new story creation to `momentum:create-story`.

The skill is invocable as `/momentum:refine` or through the Impetus menu
(option [2] "Refine backlog" in the no-sprint context menu).

## Acceptance Criteria (Plain English)

### AC1: Skill Is Independently Invocable

- A skill exists at `skills/momentum/skills/refine/SKILL.md` with valid
  frontmatter (name, description, model, effort)
- `/momentum:refine` works without Impetus running and without an active sprint
- SKILL.md body delegates to `./workflow.md`
- SKILL.md description is under 150 characters

### AC2: Backlog Presentation Shows Full Picture

- The workflow reads `stories/index.json` and presents all non-terminal
  stories (excludes done, dropped, closed-incomplete) grouped by epic
- Each story displays: title, status, priority (`[C]`/`[H]`/`[M]`/`[L]`),
  dependency status (satisfied/pending), and whether a story file exists
- Stories within each epic are sorted by priority (critical first), then
  dependency depth (leaves first), then alphabetical
- A summary header shows total counts: stories, epics, priority distribution

### AC3: Parallel Discovery Agents Identify Gaps

- The workflow spawns two parallel discovery subagents:
  - **PRD coverage agent** — reads `_bmad-output/planning-artifacts/prd.md`
    and `stories/index.json`, identifies PRD requirements with no
    corresponding backlog story
  - **Architecture coverage agent** — reads
    `_bmad-output/planning-artifacts/architecture.md` and
    `stories/index.json`, identifies architecture decisions with no
    corresponding implementation story
- Each agent returns structured findings: requirement/decision identifier,
  description, suggested epic, suggested priority

### AC4: Findings Presentation and Developer Approval

- The workflow presents a consolidated findings report covering:
  - Priority suggestions (stories whose priority should change based on
    dependencies and project direction)
  - Stale stories to consider dropping (status unchanged for multiple sprints,
    no dependencies on them)
  - Dependency issues (circular dependencies, missing dependency targets,
    satisfied dependencies that can be removed)
  - Coverage gaps from PRD and architecture discovery agents
  - Stories that belong in a different epic
- Each finding includes a recommended action and rationale
- The developer approves, modifies, or rejects each finding individually

### AC5: Approved Changes Applied via CLI

- Priority changes use `momentum-tools sprint set-priority --story SLUG --priority LEVEL`
- Epic reassignments use `momentum-tools sprint epic-membership --story SLUG --epic SLUG`
- Story drops use `momentum-tools sprint status-transition --story SLUG --target dropped`
- Dependency updates are out of scope — no CLI command exists for dependency mutation; dependency issues are flagged for manual resolution
- No direct JSON edits — all mutations go through the CLI (per write-authority rules)

### AC6: New Stories Delegated to create-story

- When gap analysis identifies missing stories, the workflow delegates creation
  to `momentum:create-story` (not inline story writing)
- The developer approves each proposed story before delegation
- Created stories appear in `stories/index.json` with the suggested epic and priority

### AC7: Decisions Logged

- All refinement decisions (priority changes, drops, new stories, rejections)
  are logged via `momentum-tools log` with event type `decision`
- A summary is presented at the end showing: changes applied, stories created,
  findings rejected, and backlog health delta (before/after priority distribution)

## Tasks / Subtasks

- [ ] Task 1 — Write behavioral evals (EDD: before skill creation)
  - [ ] Create `skills/momentum/skills/refine/evals/eval-refine-invocable.md`
    — verifies skill loads and begins backlog presentation when invoked
  - [ ] Create `skills/momentum/skills/refine/evals/eval-refine-gap-discovery.md`
    — verifies parallel PRD and architecture agents are spawned and return
    structured findings
  - [ ] Create `skills/momentum/skills/refine/evals/eval-refine-cli-mutations.md`
    — verifies approved changes are applied via momentum-tools CLI, not
    direct JSON edits

- [ ] Task 2 — Create SKILL.md (AC: 1)
  - [ ] Create `skills/momentum/skills/refine/SKILL.md` with frontmatter
    (name: refine, model: claude-sonnet-4-6, effort: high)
  - [ ] SKILL.md body delegates to `./workflow.md`
  - [ ] Verify description under 150 characters

- [ ] Task 3 — Create workflow.md (AC: 2-7, main deliverable)
  - [ ] Step 0: Task tracking initialization
  - [ ] Step 1: Backlog presentation with priority, dependency, and epic grouping
    (reuse patterns from sprint-planning Step 1)
  - [ ] Step 2: Parallel discovery agents for PRD and architecture coverage gaps
  - [ ] Step 3: Consolidated findings presentation with per-finding approval loop
  - [ ] Step 4: Apply approved changes via momentum-tools CLI and delegate new
    story creation to `momentum:create-story`
  - [ ] Step 5: Log all decisions and present summary

- [ ] Task 4 — Run evals and verify (AC: 1-7)
  - [ ] Run each eval via subagent
  - [ ] Confirm skill is independently invocable
  - [ ] Confirm mutations go through CLI only

## Dev Notes

### Workflow Structure (6 Steps)

**Step 0: Initialize task tracking**
- Create tasks for the 5 workflow steps
- Log workflow start via `momentum-tools log`

**Step 1: Present backlog**
- Read `stories/index.json`, filter terminal states, group by epic
- Sort within epic: priority (critical > high > medium > low), dependency depth
  (leaves first), alphabetical
- Display priority as `[C]`/`[H]`/`[M]`/`[L]` — same compact format as
  sprint-planning Step 1
- Show summary: N stories across M epics, priority distribution
  (e.g., "2 critical, 5 high, 8 medium, 12 low")

**Step 2: Run parallel discovery**
- Spawn two subagents (model: sonnet, effort: medium) in parallel:
  - PRD coverage: read prd.md, cross-reference against story titles and
    descriptions in index.json, identify uncovered requirements
  - Architecture coverage: read architecture.md, cross-reference against
    story titles and touches paths, identify unimplemented decisions
- Each returns structured output: list of {id, description, suggested_epic,
  suggested_priority}

**Step 3: Consolidate and present findings**
- Merge discovery agent outputs with locally detected issues:
  - **Priority suggestions:** stories with high-priority dependencies should
    themselves be high priority; critical-path stories sitting at low
  - **Stale candidates:** backlog stories with no story_file, no dependencies
    on them, and no priority above low
  - **Dependency issues:** circular chains (A depends B depends A), missing
    targets (depends_on slugs not in index), satisfied deps (dependency
    already done — the depends_on entry is informational noise)
  - **Epic mismatches:** stories whose touches paths align better with a
    different epic's theme
  - **Coverage gaps:** from PRD and architecture agents
- Present each finding with: category, story/requirement, recommended action,
  rationale
- Developer approves, modifies, or rejects each

**Step 4: Apply changes**
- For approved priority changes: `momentum-tools sprint set-priority --story SLUG --priority LEVEL`
- For approved epic moves: `momentum-tools sprint epic-membership --story SLUG --epic SLUG`
- For approved drops: `momentum-tools sprint status-transition --story SLUG --target dropped`
- For approved new stories: invoke `momentum:create-story` with description,
  epic_slug, and suggested priority
- Log each applied change via `momentum-tools log`

**Step 5: Summary**
- Present: changes applied (count by type), stories created, findings rejected
- Show before/after priority distribution
- Show before/after epic distribution if any moves occurred

### SKILL.md frontmatter

```yaml
name: refine
description: "Backlog refinement — prioritization, gap analysis, and story organization with PM and Architect."
model: claude-sonnet-4-6
effort: high
```

### Relationship to other skills

| Skill | Relationship |
|-------|-------------|
| `momentum:sprint-planning` | Refine improves the backlog that sprint-planning selects from. Sprint-planning Step 1 backlog presentation is the pattern to reuse. |
| `momentum:triage` | Triage is intake (Decision 28); refine is organization. Triage creates stubs, refine organizes and prioritizes them. |
| `momentum:create-story` | Refine delegates new story creation — never writes story files directly. |
| `momentum:impetus` | Impetus menu routes to refine via option [2] "Refine backlog" when no sprint is active. |

### Orchestrator purity (Decision 3d)

The refine workflow is an orchestrator. It reads files to build context and
presents information to the developer, but all mutations happen through:
- **Tool invocations:** `momentum-tools` CLI commands via Bash
- **Subagent spawns:** discovery agents for gap analysis, `momentum:create-story`
  for new stories

The workflow never uses Edit/Write on `stories/index.json` or any project file.

### Data flow

| File | Access |
|------|--------|
| `stories/index.json` | Reads (mutations via momentum-tools CLI) |
| `_bmad-output/planning-artifacts/prd.md` | Reads only (via discovery subagent) |
| `_bmad-output/planning-artifacts/architecture.md` | Reads only (via discovery subagent) |
| `intake-queue.jsonl` | Reads (checks for untriaged items to flag) |

**Note:** The master plan data flow table lists `momentum:refine` as the writer of prd.md and architecture.md. This is a data entry error — refine reads these files for gap analysis but never writes to them. They are protected planning artifacts (Decision 2a). The PreToolUse hook blocks writes to `_bmad-output/planning-artifacts/*.md` but does not block reads — discovery subagents will be able to read these files without hook interference.

### What NOT to change

- `momentum-tools.py` — no new CLI commands needed; `set-priority`,
  `epic-membership`, and `status-transition` already exist (or will after
  backlog-priority-field)
- `momentum:create-story` — invoke it, don't modify it
- Sprint-planning or sprint-dev workflows — refine is additive
- `stories/index.json` directly — write-authority belongs to momentum-tools

### Requirements Coverage

- Decision 28: Triage vs refinement — this skill implements the refinement half
- Master plan command table: `/momentum:refine` listed as Phase 5 skill
- Master plan data flow: refine reads prd.md, architecture.md, intake-queue.jsonl

## Momentum Implementation Guide

**Change Types in This Story:**
- All tasks -> skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Before writing a single line of the skill:**
1. Write 3 behavioral evals in `skills/momentum/skills/refine/evals/`:
   - One per eval above, testing invocability, gap discovery, and CLI-only mutations
   - Format: "Given [input/context], the skill should [observable behavior]"

**Then implement:**
2. Write SKILL.md and workflow.md

**Then verify:**
3. Run evals via subagent, confirm behaviors match

**NFR compliance:**
- SKILL.md `description` must be ≤150 characters (NFR1)
- `model:` and `effort:` frontmatter must be present
- SKILL.md body ≤500 lines / 5000 tokens (workflow.md can be longer)

**DoD items for skill-instruction tasks:**
- [ ] 3 behavioral evals written in `skills/momentum/skills/refine/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented)
- [ ] SKILL.md description ≤150 characters confirmed
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines confirmed
- [ ] AVFL checkpoint on produced artifact documented

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
