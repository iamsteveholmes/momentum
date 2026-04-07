---
title: Orchestrator Deduplication Guard — Track Spawned Agents by (Story, Role)
story_key: orchestrator-deduplication-guard
status: backlog
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/skills/sprint-dev/workflow.md
change_type: skill-instruction
priority: critical
---

# Orchestrator Deduplication Guard — Track Spawned Agents by (Story, Role)

## Goal

Prevent the sprint-dev orchestrator from spawning duplicate agents for the same
(story, role) tuple. Sprint-2026-04-06 audit found 47.8% compute waste from
redundant agent spawns: `refine-skill` had 7 identical dev agents when only 1
was needed, which cascaded into 7 prompt-engineers and 17 QA reviewers. 12,981KB
and 1,662 turns wasted. 6 of 7 duplicate dev agents ended with "Stale
self-message. Task N is already completed."

The fix is a spawn registry: before spawning any agent, check whether an agent
for that (story, role) already exists. If it does, skip the spawn. This is a
workflow-level guard — no tooling changes, no schema changes, just disciplined
state tracking inside the orchestrator.

## Acceptance Criteria (Plain English)

1. The sprint-dev workflow maintains a spawn registry that tracks every agent
   spawned during the current session, keyed by (story_slug, role).
2. Before spawning an agent in Phase 2, the orchestrator checks the spawn
   registry. If an entry for (story_slug, role) already exists, the spawn is
   skipped and a log message is emitted noting the duplicate was suppressed.
3. The spawn registry is also checked before spawning retry agents in Phase 3
   failure handling — a retry replaces the existing registry entry rather than
   adding a second one.
4. The spawn registry is checked before spawning Team Review agents in Phase 5
   (QA, E2E Validator, Architect Guard) — each reviewer role is spawned at most
   once per sprint execution.
5. When Phase 3 re-enters Phase 2 for newly unblocked stories, the registry
   correctly allows spawning agents for stories that have never been spawned,
   while still blocking duplicates for stories that have already been assigned
   an agent.
6. The registry survives the Phase 2 -> Phase 3 -> Phase 2 loop — it is not
   reset between phases.
7. Suppressed duplicate spawns are logged via `momentum-tools log` with event
   type `decision` and a detail message identifying the (story, role) that was
   deduplicated.

## Dev Notes

### Root cause analysis

The sprint-dev workflow Phase 2 (step n="2") iterates unblocked stories and
spawns agents. The workflow re-enters Phase 2 from Phase 3 whenever newly
unblocked stories are found (step 3: "Return to Phase 2 to spawn agents for
newly unblocked stories"). The current workflow has no memory of which agents
have already been spawned — it simply spawns for every story with status
"ready-for-dev" or matching the unblocked criteria.

The duplication happens because:
1. Phase 2 identifies unblocked stories and spawns agents
2. Phase 3 detects completion and re-evaluates dependencies
3. Phase 3 returns to Phase 2, which re-scans for unblocked stories
4. If story status transitions are slow or the orchestrator re-reads stale
   state, stories that already have active agents get re-spawned

### Implementation approach

Add a `{{spawn_registry}}` variable initialized as an empty map in Phase 1
(step 1), alongside the existing `{{task_map}}` and `{{story_map}}`.

The registry structure is:
```
spawn_registry = {
  "story-slug::dev": { spawned: true, agent_id: "...", timestamp: "..." },
  "story-slug::dev-skills": { spawned: true, agent_id: "...", timestamp: "..." },
  "sprint::qa-reviewer": { spawned: true, agent_id: "...", timestamp: "..." },
  "sprint::e2e-validator": { spawned: true, agent_id: "...", timestamp: "..." },
  "sprint::architecture-guard": { spawned: true, agent_id: "...", timestamp: "..." }
}
```

Key format: `{story_slug}::{role}` for dev agents, `sprint::{role}` for team
review agents.

### Where to add the guard

**Phase 1 (step 1) — Initialization:**
Add `Store {{spawn_registry}} = {}` after the existing `Store {{task_map}}`
instruction.

**Phase 2 (step 2) — Dev Wave:**
Wrap the spawn loop body in a dedup check. Before spawning each agent:
1. Compute registry key: `{slug}::{specialist}`
2. If `{{spawn_registry}}[key]` exists, skip spawn, log suppression, continue
3. If not, spawn the agent, then record `{{spawn_registry}}[key] = { spawned: true }`

**Phase 3 (step 3) — Retry handling:**
When the developer chooses "Retry" for a failed agent:
1. Remove the existing registry entry for the failed (story, role)
2. Spawn the new agent
3. Record the new entry in the registry

**Phase 5 (step 5) — Team Review:**
Before spawning each of the three review agents:
1. Compute registry key: `sprint::{reviewer_role}`
2. If already in registry, skip and log
3. If not, spawn and register

### What NOT to change

- The spawn registry is an in-memory workflow variable — not persisted to disk,
  not written to the sprint record, not tracked in a separate file
- The dependency resolution logic in Phase 2 and Phase 3 is unchanged — we are
  only adding a guard around the spawn action, not changing which stories are
  considered unblocked
- Status transitions (`momentum-tools sprint status-transition`) are unchanged
- The Phase 3 -> Phase 2 loop structure is unchanged

### Why a workflow variable and not a tool

The deduplication state only matters within a single sprint execution session.
It does not need to survive across sessions (session resumption in Phase 1
already handles in-progress stories by checking worktree existence). A workflow
variable is the simplest correct solution — no new tools, no file I/O, no
schema changes.

### Requirements coverage

- Architecture: Decision 25 (Teams Over Waves) — spawn-once-per-story enforces
  the team model rather than allowing unbounded agent proliferation
- Architecture: Decision 26 (Two-Layer Agent Model) — the orchestrator layer
  is responsible for spawn discipline; the guard is an orchestrator concern
- Retro finding: 47.8% compute waste from redundant spawns in sprint-2026-04-06

## Tasks / Subtasks

- [ ] Task 1 — Add spawn registry initialization to Phase 1 (AC: 1, 6)
  - [ ] Add `Store {{spawn_registry}} = {}` instruction after `{{task_map}}` in step 1
  - [ ] Add a `<note>` explaining the registry's purpose and key format

- [ ] Task 2 — Add dedup guard to Phase 2 spawn loop (AC: 2, 5)
  - [ ] Wrap the "For each unblocked story" spawn body in a dedup check
  - [ ] Before spawning: compute key `{slug}::{specialist}`, check registry
  - [ ] If key exists: skip spawn, emit log via `momentum-tools log` with event
    `decision` and detail identifying the suppressed duplicate
  - [ ] If key absent: proceed with spawn, then register the key
  - [ ] Ensure the guard works on re-entry from Phase 3 (newly unblocked stories
    pass because they were never registered)

- [ ] Task 3 — Update Phase 3 retry handling to replace registry entry (AC: 3)
  - [ ] In the "Retry" branch of agent failure handling, delete the existing
    registry entry for the failed (story, specialist) before re-spawning
  - [ ] After spawning the retry agent, register the new entry

- [ ] Task 4 — Add dedup guard to Phase 5 Team Review spawns (AC: 4)
  - [ ] Before spawning QA Agent: check `sprint::qa-reviewer` in registry
  - [ ] Before spawning E2E Validator: check `sprint::e2e-validator` in registry
  - [ ] Before spawning Architect Guard: check `sprint::architecture-guard` in registry
  - [ ] Skip and log if already spawned

- [ ] Task 5 — Add dedup logging for suppressed spawns (AC: 7)
  - [ ] Each suppressed spawn logs via `momentum-tools log --agent impetus
    --sprint {{sprint_slug}} --event decision --detail "Dedup: skipped
    duplicate spawn for {key}"`
  - [ ] Verify log messages appear in the sprint event log

## Momentum Implementation Guide

**Change Types in This Story:**
- All tasks -> skill-instruction (workflow modifications in sprint-dev)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Before writing the workflow changes:**
1. Write behavioral evals in `skills/momentum/skills/sprint-dev/evals/`:
   - `eval-dedup-guard-blocks-duplicate.md` — Given a story that has already
     been spawned, when Phase 2 re-enters, the orchestrator does not spawn a
     second agent for the same (story, role)
   - `eval-dedup-guard-allows-new-stories.md` — Given newly unblocked stories
     that have never been spawned, the orchestrator spawns agents normally

**Then implement:**
2. Modify `skills/momentum/skills/sprint-dev/workflow.md` per tasks 1-5

**Then verify:**
3. Run evals via subagent, confirm behaviors match

**DoD items for skill-instruction tasks:**
- [ ] 2 behavioral evals written
- [ ] EDD cycle ran — all eval behaviors confirmed
- [ ] Workflow modifications follow existing XML structure and conventions
- [ ] Dedup guard does not alter dependency resolution or status transition logic
- [ ] Suppressed spawns are logged with identifying detail

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
