---
title: Impetus Allowed-Tools Restriction — Enforce Orchestrator Read-Only
story_key: impetus-allowed-tools-restriction
status: ready-for-dev
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/skills/impetus/SKILL.md
change_type: skill-instruction
derives_from:
  - path: docs/planning-artifacts/momentum-master-plan.md
    relationship: derives_from
    section: "Part 4 Architecture Decisions — Decision 3d"
---

# Impetus Allowed-Tools Restriction — Enforce Orchestrator Read-Only

## Description

Impetus is the orchestrator — it delegates all file writing to subagents. This
is already enforced by workflow instructions and the orchestrator-purity
feedback loop, but enforcement is advisory: the model can still call Write,
Edit, or other mutating tools if it drifts.

Claude Code supports an `allowed-tools` frontmatter field in SKILL.md that
deterministically restricts which tools a skill can invoke. Adding
`allowed-tools: [Read, Glob, Grep, Agent, Bash]` to the Impetus frontmatter
makes the read-only constraint structural — the harness rejects disallowed
tool calls before they execute, regardless of what the model attempts.

This is Phase 4 from the master plan: deterministic enforcement of
Architecture Decision 3d ("Impetus MUST NOT perform development, evaluation,
testing, or validation").

## Acceptance Criteria (Plain English)

1. The Impetus SKILL.md frontmatter contains an `allowed-tools` field that
   restricts Impetus to exactly: `Read`, `Glob`, `Grep`, `Agent`, `Bash`.
   No other tools (Write, Edit, Skill, etc.) are permitted.

2. All existing Impetus workflows (greeting, install, upgrade, hash-drift,
   open-threads) continue to function correctly with only these five tools.
   Every action Impetus performs today uses only Read, Glob, Grep, Agent, or
   Bash — no regressions.

3. The `Agent` tool remains available so Impetus can spawn subagents (this is
   its primary delegation mechanism). The `Bash` tool remains available for
   `momentum-tools.py` invocations. The `Skill` tool is NOT included — Impetus
   dispatches via Agent, not Skill.

## Tasks

### Task 0: Refactor Write-dependent Workflow Steps to Bash

The install, upgrade, and hash-drift restore paths in `workflow.md` currently
use model-level Write operations (e.g., "write to resolved target path",
"write installed.json"). These must be refactored to use Bash-based file
writes (`python3 -c`, `cp`, `tee`, etc.) before the restriction can ship.

Affected steps: install consent (step 2 file copies), upgrade (step 9),
hash-drift restore (step 10), gitignore fix, journal-view regeneration.

**Change type:** skill-instruction (EDD)

### Task 1: Audit Current Tool Usage

Scan `SKILL.md`, `workflow.md`, and `workflow-runtime.md` for every tool
invocation Impetus makes. Confirm each one maps to Read, Glob, Grep, Agent,
or Bash AFTER Task 0 refactoring. Flag any remaining invocation that would
be blocked by the restriction.

**Change type:** skill-instruction (EDD)

### Task 2: Add allowed-tools Frontmatter

Add `allowed-tools: [Read, Glob, Grep, Agent, Bash]` to the Impetus SKILL.md
YAML frontmatter. Place it after the `effort` field.

**Change type:** skill-instruction (EDD)

### Task 3: Verify Workflows Under Restriction

Run behavioral verification that each Impetus route (greeting, install,
upgrade, hash-drift, open-threads) dispatches correctly with the restriction
active. The key risk is that some workflow step silently used a disallowed
tool — the audit in Task 1 should catch this, but runtime verification
confirms it.

**Change type:** skill-instruction (EDD)

## Dev Notes

### The change itself

One line added to YAML frontmatter:

```yaml
---
name: impetus
description: "Impetus — Momentum practice orchestrator. ..."
model: claude-sonnet-4-6
effort: high
allowed-tools: [Read, Glob, Grep, Agent, Bash]
---
```

### Why Skill is excluded

Impetus dispatches subagents via `Agent` tool calls, not `Skill` invocations.
The `Skill` tool is used by the human to invoke top-level skills like
`/momentum:sprint-dev`. Impetus never calls Skill itself — it spawns agents
that run skills. Excluding Skill prevents Impetus from accidentally invoking
a skill directly instead of delegating to a subagent.

### Risk: Bash as an escape hatch

Bash is allowed because Impetus needs it for `momentum-tools.py` calls. In
theory, Bash could be used to write files (`echo > file`). This is acceptable
because:
- The workflow instructions already prohibit direct writes
- The `allowed-tools` restriction closes the Write/Edit vector
- Bash-based file writes would be visible in tool call logs
- Full Bash lockdown would break momentum-tools.py invocations

### Workflow files to audit

- `skills/momentum/skills/impetus/SKILL.md` — Bash (momentum-tools.py), Agent (dispatch)
- `skills/momentum/skills/impetus/workflow.md` — Bash (copy, install), Read (files), Agent (subagents). **WARNING:** install/upgrade/hash-drift steps currently use model-level Write — Task 0 must refactor these to Bash before restriction ships.
- `skills/momentum/skills/impetus/workflow-runtime.md` — Agent (subagent dispatch), Read (context loading)

## Momentum Implementation Guide

**Change type: skill-instruction — use EDD (Eval-Driven Development)**

### EDD Steps

1. **Write behavioral evals before modifying:**
   - Eval 1: Invoke Impetus with a greeting route. Verify it completes
     without attempting Write or Edit tool calls.
   - Eval 2: Invoke Impetus and select a menu item that dispatches a
     subagent. Verify the dispatch uses Agent tool, not Skill tool.
   - Eval 3: Invoke Impetus with an install route. Verify all file
     operations use Bash (cp, mkdir) rather than Write/Edit.

2. **Implement the change:** Add `allowed-tools` to SKILL.md frontmatter.

3. **Run evals to verify:** All three evals should pass. If any fail, the
   workflow is using a disallowed tool and must be refactored before the
   restriction can ship.

### NFR Compliance

- Description field: 127 chars (under 150 limit)
- `model` and `effort` frontmatter: already present, no change needed
- SKILL.md body: currently 83 lines (well under 500 limit)
