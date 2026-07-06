---
title: "Repair phantom story_file entries + sprint-manager invariant; backfill conduct-live-run-against-fixture-sprint with live-fixture scope"
story_key: repair-phantom-story-file-entries-and-backfill-live-fixture-scope
status: backlog
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: defect
priority: high
depends_on: []
touches: []
---

# Repair phantom story_file entries + sprint-manager invariant; backfill conduct-live-run-against-fixture-sprint with live-fixture scope

<!-- RETRO STUB: created by momentum:retro from the sprint-2026-06-28 transcript audit
     (2026-07-06), approved at the Phase 5 stub gate. It is a stub, NOT a dev-ready story.
     All sections below marked DRAFT require full rewrite by create-story. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As the practice maintainer,
I want every `story_file:true` index entry to have a backing `.md` (with an invariant preventing recurrence) and the live-fixture story backfilled with real scope,
so that sprint-planning never crashes on phantom entries and the fixture-blocked story family can finally verify PASS/FAIL instead of BLOCKED.

## Description

`stories/index.json` claims `story_file:true` for 8 slugs whose `.momentum/stories/{slug}.md` did not exist (verified via `ls` by the retro audit and independently re-confirmed by dedup verifiers, 2026-07-06): `build-guidelines-invocation-surface-in-sprint-planning`, `dag-dispatch-blast-radius-discovery`, `canvas-gate-review-surface-epic`, `conduct-live-run-against-fixture-sprint`, `verification-method-two-column-smoke-ui-model`, `re-emit-frozen-app-ui-contracts-via-producer`, `retro-audit-workflow-process-findings-return`, `endgate-format-spec-section00-alignment`.

Two scopes, deliberately asymmetric:

1. **Mechanical repair (7 slugs):** backfill a stub `.md` whose frontmatter matches the index entry. The substantive scope of those stories remains their own — repairing the phantom does NOT absorb their work (confirmed by dedup verification: e.g. `dag-dispatch-blast-radius-discovery` stays a distinct exploration story). Note: `retro-audit-workflow-process-findings-return` was already backfilled during the 2026-07-06 retro session — coordinate, don't duplicate.
2. **Bespoke content backfill (1 slug):** `conduct-live-run-against-fixture-sprint.md` gets LIVE-FIXTURE scope — a committed nornspun fixture providing a real `momentum/agents.json`, `.claude/manifests/`, and a completed-sprint sample, such that sprint-planning → build-guidelines → agent-builder can be driven to completion against it.

Plus an invariant: sprint-manager/bookkeeping verifies `story_file:true` entries have a backing file before the flag is set.

**Pain context:** the missing live fixture was sprint-2026-06-28's dominant root cause — 9/9 ACs BLOCKED on `companion-surface-pre-sprint-plan-gate`, 16/27 E2E scenarios BLOCKED, one 51-turn E2E agent with zero net-new yield; the same root cause was independently rediscovered 3+ times. Phantom entries crash the next sprint-planning pass that selects them.

## Acceptance Criteria

<!-- DRAFT: rough ACs from the retro audit return. NOT refined or validated.
     This section MUST be fully rewritten by create-story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Each phantom slug has `.momentum/stories/{slug}.md` with frontmatter matching its index entry
- `conduct-live-run-against-fixture-sprint.md` specifies the live-fixture scope (committed nornspun fixture: `momentum/agents.json`, `.claude/manifests/`, completed-sprint sample) needed by the 3 fixture-blocked stories
- A bookkeeping check (sprint-manager or create-story) verifies `story_file:true` entries have a backing file before the flag is set
- Story-level QA/E2E for the 3 affected stories reports PASS/FAIL against the fixture instead of BLOCKED-on-missing-fixture

> Note: The ACs above are rough captures from the audit. Create-story will replace them
> with validated, testable acceptance criteria.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- Retro audit return: `.momentum/sprints/sprint-2026-06-28/audit-return.json` (priority item 1 + 3, merged at the Phase 5 dedup)
- Dedup verification record: session 2026-07-06 corpus-dedup workflow `wf_7b949d2b-a8e`

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
