---
title: E2E Validator ToolSearch Fix — Pre-load SendMessage Schema
story_key: e2e-validator-toolsearch-fix
status: backlog
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/agents/e2e-validator.md
change_type: config-structure
priority: medium
---

# E2E Validator ToolSearch Fix — Pre-load SendMessage Schema

## Goal

7 of 14 E2E validator agents in sprint-2026-04-06 hit `InputValidationError`
when attempting to call `SendMessage` without first loading its schema via
`ToolSearch`. The error was identical every time: "This tool's schema was not
sent to the API." Each agent self-recovered by retrying after loading the
schema, but this wastes 1 turn per agent — 7 wasted turns total across the
sprint.

QA reviewers did NOT exhibit this issue, suggesting their agent definition or
prompt structure guides tool discovery more effectively. The fix is to add
explicit guidance to the E2E validator agent definition so it loads the
`SendMessage` schema via `ToolSearch` before attempting to use it.

## Acceptance Criteria (Plain English)

1. The E2E validator agent definition includes `ToolSearch` in its tools list
   so the agent has access to discover deferred tool schemas.
2. The agent definition includes an explicit instruction to load the
   `SendMessage` schema via `ToolSearch` before sending its report back.
3. After the fix, E2E validator agents no longer hit `InputValidationError`
   on `SendMessage` — the schema is loaded proactively, not reactively.

## Dev Notes

### Root cause analysis

`SendMessage` is a deferred tool — its schema is not loaded into the agent's
context at spawn time. The agent must first call `ToolSearch` to fetch the
schema, then call `SendMessage`. The E2E validator agent definition
(`skills/momentum/agents/e2e-validator.md`) does not list `ToolSearch` in its
`tools:` frontmatter and contains no instructions about tool discovery or
schema loading. The agent discovers it needs `SendMessage` only when trying
to return its report, at which point it fails, loads the schema reactively,
and retries.

The QA reviewer agent (`skills/momentum/agents/qa-reviewer.md`) has an
identical tools list and no explicit `ToolSearch` guidance either — but it
did not exhibit the error in this sprint. This may be due to prompt ordering
or the QA reviewer happening to encounter the deferred tools system reminder
before its first `SendMessage` call. Regardless, both agents should be
hardened against this issue.

### Implementation approach

Two changes to `skills/momentum/agents/e2e-validator.md`:

1. **Add `ToolSearch` to the `tools:` frontmatter list** — this gives the
   agent access to the tool discovery mechanism.

2. **Add a "Returning Results" section** to the agent body that instructs
   the agent to load the `SendMessage` schema via `ToolSearch` before
   sending its report. Place this after the "Output Format" section and
   before the "Verdict Rules" section.

### Scope consideration

The QA reviewer agent has the same potential vulnerability. However, it did
not fail in practice during this sprint. If we want to harden both agents
preventively, the same fix pattern applies to `qa-reviewer.md`. This story
scopes to the E2E validator (the observed failure) but the fix should be
applied to the QA reviewer as well to prevent the same issue from surfacing
there in future sprints.

### What NOT to change

- The E2E validator's core validation logic, process, or output format
- The agent's model or effort settings
- The Gherkin spec loading or scenario execution behavior

## Tasks / Subtasks

- [ ] Task 1 — Add ToolSearch to E2E validator tools list (AC: 1)
  - [ ] Add `ToolSearch` to the `tools:` array in the frontmatter of
    `skills/momentum/agents/e2e-validator.md`

- [ ] Task 2 — Add SendMessage pre-load instruction to E2E validator (AC: 2, 3)
  - [ ] Add a "Returning Results" section after "Output Format" that instructs
    the agent to call `ToolSearch` to load the `SendMessage` schema before
    sending the validation report
  - [ ] The instruction should be clear and imperative: load first, then send

- [ ] Task 3 — Apply the same fix to QA reviewer agent (AC: 1, 2, 3)
  - [ ] Add `ToolSearch` to `tools:` frontmatter in
    `skills/momentum/agents/qa-reviewer.md`
  - [ ] Add the same "Returning Results" section to the QA reviewer agent

## Momentum Implementation Guide

**Change Types in This Story:**
- All tasks -> config-structure (agent definition modifications)

---

### config-structure Tasks

**Implement:**
1. Edit agent frontmatter to add `ToolSearch` to tools lists
2. Add "Returning Results" section with `SendMessage` pre-load instruction

**Verify:**
3. Confirm the agent definition parses correctly (valid YAML frontmatter)
4. Confirm the new section integrates naturally with the existing agent body

**DoD items for config-structure tasks:**
- [ ] `ToolSearch` present in both agent tools lists
- [ ] "Returning Results" section present in both agent definitions
- [ ] YAML frontmatter is valid
- [ ] No changes to agent validation logic or output format

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
