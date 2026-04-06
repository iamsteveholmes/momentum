---
title: Retro Skill — Sprint Retrospective with Cross-Log Discovery and Sprint Closure
story_key: retro-skill
status: ready-for-dev
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/skills/retro/SKILL.md
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/scripts/momentum-tools.py
change_type: skill-instruction + code
---

# Retro Skill — Sprint Retrospective with Cross-Log Discovery and Sprint Closure

## Description

The sprint lifecycle is planning → dev → retro → next cycle. Planning and dev
are implemented; retro is the missing piece that closes the loop. Without it,
sprints "complete" but learnings don't feed back into the practice.

Per Decision 34, retro owns sprint closure. It performs holistic cross-log
discovery across all agent JSONL logs, verifies story completion, produces
two triage outputs (Decision 27: Momentum triage + Project triage), creates
story stubs from findings, calls `momentum-tools sprint complete`, and
archives sprint artifacts.

This story creates the `momentum:retro` skill as a proper SKILL.md + workflow
pair in the plugin structure, plus any momentum-tools.py subcommands needed
to support it.

## Acceptance Criteria (Plain English)

1. A skill exists at `skills/momentum/skills/retro/SKILL.md` that is
   independently invocable via `/momentum:retro`.

2. The skill reads all agent JSONL log files from
   `.claude/momentum/sprint-logs/{sprint-slug}/` for the most recently
   completed sprint, correlating events across agent logs to build a
   holistic timeline.

3. The skill verifies that every story in the sprint reached `done` status.
   Stories that did not reach `done` are flagged as `closed-incomplete` via
   `momentum-tools sprint status-transition --story SLUG --target closed-incomplete`.

4. The skill produces two structured outputs per Decision 27:
   - **Momentum triage** — practice improvements (how the process can improve),
     written to `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/retro-momentum-triage.md`
   - **Project triage** — project-specific findings (what the code/specs need),
     written to `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/retro-project-triage.md`

5. For actionable findings in either triage output, the skill creates story
   stub entries in `stories/index.json` with status `backlog` and appropriate
   `epic_slug` assignment. The developer approves each stub before creation.

6. The skill calls `momentum-tools sprint complete` followed by
   `momentum-tools sprint retro-complete` to set the terminal sprint state
   and record the retro completion timestamp.

7. The skill presents a summary to the developer showing: stories verified,
   findings count by category, story stubs created, and sprint closure
   confirmation.

8. The SKILL.md follows plugin conventions: `name: retro`,
   description under 150 chars, `model:` and `effort:` frontmatter present,
   body delegates to `./workflow.md`.

9. The workflow uses task tracking (TaskCreate/TaskUpdate) for its phases
   and logs decisions via `momentum-tools log`.

## Dev Notes

### Workflow phases

1. **Sprint identification** — Find the most recently completed sprint in
   `_bmad-output/implementation-artifacts/sprints/index.json` (status: `done`, `retro_run_at: null`). If none,
   error with clear message. Confirm with developer which sprint to retro.

2. **Log collection and correlation** — Read all `.jsonl` files from
   `.claude/momentum/sprint-logs/{sprint-slug}/`. Parse each line as JSON.
   Sort all events by timestamp across all agent files. Build a unified
   timeline showing which agents acted when and how they responded to
   each other's outputs.

3. **Story verification** — For each story in the sprint's story list,
   check status in `stories/index.json`. Stories at `done` pass. Stories
   at any other status get flagged. Ask developer whether to force-close
   (`closed-incomplete`) or investigate.

4. **Cross-log discovery** — Analyze the correlated timeline for:
   - Patterns of errors or retries (repeated failures suggest process gaps)
   - Assumptions that turned out wrong (assumption events followed by errors)
   - Ambiguities that blocked progress
   - Decisions that had downstream consequences
   - Quality findings that weren't addressed during the sprint

5. **Triage output generation** — Classify discoveries into two buckets:
   - **Momentum triage**: process/practice improvements — things like
     "the sprint-dev workflow didn't handle X well" or "AVFL missed Y"
   - **Project triage**: code/spec findings — things like
     "architecture.md doesn't cover Z" or "test coverage gap in W"

6. **Story stub creation** — For actionable items, propose story stubs.
   Present each to the developer for approval before adding to
   `stories/index.json`.

7. **Sprint closure** — Call `momentum-tools sprint complete`. Call
   `momentum-tools sprint retro-complete`. Present final summary.

### momentum-tools.py changes

No new subcommands needed — existing commands cover the lifecycle:
- `sprint complete` — already exists
- `sprint retro-complete` — already exists
- `sprint status-transition --target closed-incomplete` — already exists
- `log` — already exists

### SKILL.md frontmatter

```yaml
name: retro
description: "Sprint retrospective — cross-log discovery, story verification, triage outputs, and sprint closure."
model: claude-sonnet-4-6
effort: high
```

### Files

- `skills/momentum/skills/retro/SKILL.md` — skill definition
- `skills/momentum/skills/retro/workflow.md` — full workflow instructions
