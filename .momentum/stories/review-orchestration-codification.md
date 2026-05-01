---
title: Review Orchestration Codification — Automate AVFL + Code Review Flow
story_key: review-orchestration-codification
status: backlog
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/skills/sprint-dev/workflow.md
change_type: skill-instruction
priority: high
---

# Review Orchestration Codification — Automate AVFL + Code Review Flow

## Goal

Codify the review orchestration flow in the sprint-dev workflow so the developer
does not need to manually direct the sequence of AVFL, per-story code review, and
fix passes. Currently, the workflow defines AVFL (Phase 4) and Team Review (Phase 5)
but the developer had to micromanage the actual review sequence — telling Impetus
to stop AVFL before applying fixes, then manually requesting independent code
reviews per story. This should be an automated, deterministic flow that the
orchestrator drives without user intervention.

## Problem Statement

During sprint execution, the developer had to give explicit instructions like
"Proceed but remember that the AVFL should STOP before fix... followed by feeding
into the team to make fixes. There should ALSO be independent /bmad-code-review
on each story..." This is workflow work that the orchestrator should own. The
current Phase 4 and Phase 5 do not encode:

1. **AVFL stop gate** — AVFL must complete and present findings BEFORE any fixes
   are spawned. The current workflow spawns fix agents inline, risking premature
   fixes before the full picture is known.
2. **Per-story code review** — Independent code review per story (not just the
   sprint-level Team Review in Phase 5). Each story's changes should receive an
   adversarial code review before the sprint-level reviewers run.
3. **Fix routing** — AVFL findings and code review findings need to be routed
   back to targeted fix agents with clear scope, not left for the developer to
   orchestrate.

## Acceptance Criteria (Plain English)

1. Phase 4 (AVFL) has an explicit stop gate: AVFL runs to completion and presents
   all findings to the developer before any fix agents are spawned. No fixes are
   initiated until the developer acknowledges the findings.

2. A new sub-phase exists between AVFL and Team Review that runs independent
   per-story code review using `momentum:code-reviewer` (or the project's code
   review skill). Each story's merged changeset is reviewed independently.

3. Per-story code review findings are consolidated with AVFL findings into a
   single prioritized fix queue before fix agents are spawned.

4. Fix agents are spawned only after the consolidated fix queue is presented
   and the developer confirms which items to fix vs. defer.

5. After fix agents complete, only the reviewers whose findings were addressed
   are re-run (selective re-review, not full re-run of everything).

6. The entire review-fix cycle is driven by the workflow — the developer's only
   decision points are: (a) acknowledge AVFL findings, (b) confirm which items
   to fix, (c) accept final state. No manual orchestration of review sequence.

7. The workflow handles the case where code review findings introduce new AVFL
   concerns — if fixes are substantial, a lightweight re-scan is triggered
   automatically.

## Dev Notes

### Current state of workflow.md

Phase 4 (AVFL, lines 225–265) runs AVFL and immediately offers to spawn fix
agents for findings. There is no explicit stop gate — the workflow can spawn
fixes before the developer has seen the full picture.

Phase 5 (Team Review, lines 269–333) runs QA, E2E Validator, and Architect Guard
in parallel. There is no per-story code review step — reviews are only at the
sprint level.

The gap: no per-story code review, no consolidated fix queue, and AVFL findings
flow directly into fix spawns without a deliberate pause.

### What to change

1. **Phase 4 — Add stop gate**: Restructure AVFL phase so findings are presented
   as a read-only report. Remove the inline "spawn targeted fix agents" action
   from Phase 4 entirely. Fixes move to a dedicated fix phase.

2. **New Phase 4b — Per-Story Code Review**: After AVFL, spawn `momentum:code-reviewer`
   for each story's changeset independently. Each review scopes to the files in
   that story's `touches` array (or the actual diff from the story merge).

3. **New Phase 4c — Consolidated Fix Queue**: Merge AVFL findings + code review
   findings into a single queue. Present to developer. Developer picks fix/defer
   for each item.

4. **New Phase 4d — Targeted Fixes + Selective Re-review**: Spawn fix agents for
   accepted items. After fixes, re-run only the specific reviewers that produced
   the fixed findings.

5. **Phase 5 (Team Review)**: Unchanged — still runs QA, E2E Validator, and
   Architect Guard. But now it runs on code that has already been through AVFL +
   per-story code review + fixes.

### What NOT to change

- Phase 1–3 (Initialization, Dev Wave, Progress Tracking) — untouched
- Phase 5–7 (Team Review, Verification, Sprint Completion) — structure unchanged,
  though Phase 5 now runs after the new review phases
- The AVFL skill itself — only the workflow's invocation pattern changes
- The code-reviewer skill — it's invoked as-is

### Numbering consideration

Adding sub-phases (4b, 4c, 4d) vs. renumbering all phases (4→8 phases total) is
an implementation decision. Sub-phases are preferred to avoid breaking references
to Phase 5/6/7 in other documentation and agent instructions.

## Tasks / Subtasks

- [ ] Task 1 — Restructure Phase 4 AVFL stop gate (AC: 1)
  - [ ] Remove inline fix-agent spawning from Phase 4
  - [ ] Add explicit stop gate: present findings, wait for developer acknowledgement
  - [ ] Ensure AVFL output is structured for downstream consolidation

- [ ] Task 2 — Add per-story code review sub-phase (AC: 2)
  - [ ] Add Phase 4b after AVFL
  - [ ] For each merged story, invoke `momentum:code-reviewer` scoped to that story's changeset
  - [ ] Collect structured findings from each review

- [ ] Task 3 — Build consolidated fix queue (AC: 3, 4)
  - [ ] Add Phase 4c that merges AVFL + code review findings
  - [ ] Present unified queue to developer with fix/defer choice per item
  - [ ] Spawn fix agents only for confirmed items

- [ ] Task 4 — Implement selective re-review after fixes (AC: 5, 7)
  - [ ] After fixes complete, re-run only affected reviewers
  - [ ] If fixes are substantial, trigger lightweight AVFL re-scan
  - [ ] Loop until clean or developer accepts remaining items

- [ ] Task 5 — Verify end-to-end flow is developer-hands-off (AC: 6)
  - [ ] Walk through the full Phase 4 → 4b → 4c → 4d → 5 sequence
  - [ ] Confirm developer decision points are limited to acknowledge/confirm/accept
  - [ ] Verify no manual orchestration is required for review sequencing

## Momentum Implementation Guide

**Change Types in This Story:**
- All tasks → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Before writing workflow changes:**
1. Write behavioral evals in `skills/momentum/skills/sprint-dev/evals/`:
   - `eval-avfl-stop-gate.md` — verifies AVFL presents findings before any fix spawns
   - `eval-per-story-code-review.md` — verifies each story gets independent code review
   - `eval-consolidated-fix-queue.md` — verifies findings from AVFL + code review merge into single queue

**Then implement:**
2. Modify `skills/momentum/skills/sprint-dev/workflow.md` with the new sub-phases

**Then verify:**
3. Run evals via subagent, confirm behaviors match

**DoD items for skill-instruction tasks:**
- [ ] 3 behavioral evals written
- [ ] EDD cycle ran — all eval behaviors confirmed
- [ ] workflow.md updated with stop gate, per-story review, consolidated fix queue, selective re-review
- [ ] No manual orchestration required for review sequencing (developer only acknowledges/confirms/accepts)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
