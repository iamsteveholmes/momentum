---
title: "Practice-Ledger + Features→Epics Cascade — Sequenced Plan"
story_key: practice-ledger-features-epics-cascade-sequenced-plan
status: ready-for-dev
epic_slug: ad-hoc
story_type: practice
change_type:
  - specification
  - skill-instruction
  - script-code
  - rule-hook
verification_method: review
depends_on: []
touches:
  - .momentum/intake-queue.jsonl
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
  - .momentum/signals/
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/features.json
  - _bmad-output/planning-artifacts/epics.md
  - .claude/rules/impetus.md
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/skills/triage/workflow.md
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/intake/workflow.md
  - skills/momentum/skills/decision/workflow.md
  - skills/momentum/skills/assessment/workflow.md
  - skills/momentum/skills/feature-breakdown/workflow.md
  - skills/momentum/skills/create-story/workflow.md
  - skills/momentum/skills/canvas/server.tsx
  - skills/momentum/skills/canvas/workflow.md
  - skills/momentum/skills/feature-grooming/
  - skills/momentum/skills/feature-breakdown/
  - skills/momentum/skills/epic-grooming/workflow.md
plan_ref: ~/.claude/plans/i-like-sequencing-the-optimized-lagoon.md
---

# Practice-Ledger + Features→Epics Cascade — Sequenced Plan

## User Story

As a Momentum developer,
I want to capture and execute a coherent cascade of changes that (a) redesigns the practice ledger as a true append-only event log with safe concurrent writes, (b) consolidates `features.json` into `epics.md` to align with Beads' epic semantics, and (c) resolves the `.momentum/signals/` overlap question,
So that the practice's state-tracking infrastructure stops drifting from its documentation, supports concurrent multi-agent writers safely, and matches the unit (epics) that Beads understands.

## Background

Over the course of an evening's planning conversation, four practice-ledger defects surfaced:

1. **Doc/code drift** — Architecture claims the ledger is append-only with full history preserved; the implementation actually does whole-file rewrites (`cmd_intake_queue_consume` reads the entire file, mutates an entry in memory, writes the entire file back).
2. **Lost-update concurrency unsafety** — No locking, no atomic write-then-rename. Two concurrent consume calls can lose one update; an interleaved append and consume can lose the appended entry.
3. **Backlog hygiene rot** — 23+ entries with titles like "superseded by DEC-..." are still `open` because no workflow ever calls `consume` on supersession.
4. **"Last 5" rule lies** — The newly-created `.claude/rules/impetus.md` reads only the most recent 5 entries, surfacing a tidy picture while hiding 47 stale entries.

In parallel, the previously-flagged plan to consolidate `features.json` into `epics.md` (to fit Beads' epic semantics, which uses epics in the way Momentum has been using features) is still undecided. The unused `.momentum/signals/` directory may overlap in purpose with the new event log and needs a verdict.

The user requested the standard Momentum process: one assessment → two decisions → create-story per discrete change → quick-fix per story. This story captures the orchestration of that cascade and serves as the process-story anchor for plan execution.

The full plan is preserved at `~/.claude/plans/i-like-sequencing-the-optimized-lagoon.md` and remains the authoritative reference for sequencing, concurrency, and per-step orchestration.

## Acceptance Criteria

1. **Assessment exists.** A single assessment document is produced at `_bmad-output/planning-artifacts/assessments/` capturing the four practice-ledger defects, the features→epics motivation, and the signals/ overlap question.
2. **Two decisions exist.** Two decision documents are produced at `_bmad-output/planning-artifacts/decisions/`:
   - Decision N1 — Practice-ledger redesign (event-log + immutability + custom escape hatch + DuckDB reader + hard-cut migration + signals/ verdict).
   - Decision N2 — Features→Epics consolidation (retires `features.json`, folds capability info into `epics.md`, names downstream skill/canvas changes).
3. **Stories exist.** Up to 8 stories (A1–A4 from Cascade A, B1–B4 from Cascade B; possibly an A5 conditional on the signals verdict) are created via `momentum:create-story`, each with a complete spec and dependency edges that match the cascade's dependency graph.
4. **Cascade A executes.** Each story in cascade A (ledger redesign + hygiene + Impetus rule update + skill workflow updates) is executed via `momentum:quick-fix`, with A1 completing before A2/A3/A4 begin.
5. **Cascade B executes.** Each story in cascade B (features→epics migration + create-story update + canvas update + feature-grooming/feature-breakdown retirement-or-absorption) is executed via `momentum:quick-fix`, with B1 completing before B2/B3/B4 begin.
6. **Architecture and PRD are updated.** Doc updates are folded into each implementation story (per the plan's choice), so by cascade completion `architecture.md`, `prd.md`, and the new `.claude/rules/impetus.md` all match the implemented system.
7. **End-to-end verification passes.**
   - `momentum-tools practice-ledger summary` returns honest open/consumed/by-source counts (not "last 5").
   - A fresh Claude Code session in the project triggers the Impetus rule; he reads via the new CLI and surfaces accurate state.
   - `momentum-tools practice-ledger history --entity <some-id>` shows the full event chain for at least one entity.
   - `features.json` is archived; `epics.md` carries the consolidated capability information.
   - `momentum:create-story` reads from epics + decisions + architecture + PRD as appropriate for the story's change_type.

## Definition of Done

- [ ] Assessment document written to `_bmad-output/planning-artifacts/assessments/`
- [ ] Decision document 1 (practice-ledger redesign) written to `_bmad-output/planning-artifacts/decisions/`
- [ ] Decision document 2 (features→epics consolidation) written to `_bmad-output/planning-artifacts/decisions/`
- [ ] Story A1 created via `momentum:create-story` — Ledger schema + CLI redesign
- [ ] Story A2 created via `momentum:create-story` — Ledger hygiene cleanup
- [ ] Story A3 created via `momentum:create-story` — Impetus rule update
- [ ] Story A4 created via `momentum:create-story` — Skill workflow updates
- [ ] Story B1 created via `momentum:create-story` — Migrate features.json into epics.md, retire features.json
- [ ] Story B2 created via `momentum:create-story` — create-story input-routing update
- [ ] Story B3 created via `momentum:create-story` — Canvas update (remove/repurpose features lens)
- [ ] Story B4 created via `momentum:create-story` — Feature-grooming + feature-breakdown retirement-or-absorption
- [ ] Possibly Story A5 (conditional on Decision 1's signals/ verdict)
- [ ] Each story executed via `momentum:quick-fix` in dependency order
- [ ] `momentum-tools practice-ledger summary` operational
- [ ] `momentum-tools practice-ledger history --entity <id>` operational
- [ ] `features.json` archived, `epics.md` carries consolidated capability information
- [ ] Architecture.md and PRD updated to match implementation
- [ ] `.claude/rules/impetus.md` updated to drop "last 5" and use honest counts

## Dev Notes

**Change type classification:**
- `specification` — assessment + decisions + architecture.md updates + PRD updates + epics.md restructure
- `skill-instruction` — workflow.md updates across 7+ skills (retro, triage, sprint-planning, intake, decision, assessment, feature-breakdown, create-story, canvas, feature-grooming, feature-breakdown, epic-grooming)
- `script-code` — momentum-tools.py CLI rewrite + test-momentum-tools.py updates
- `rule-hook` — `.claude/rules/impetus.md` update

**Verification method:** `review` — this is a process story orchestrating a cascade; verification of each leaf story happens via the leaf's own quick-fix gates (AVFL scan, code review, E2E/QA). The process story is "done" when all leaf stories are done and the end-to-end verification in the AC list passes.

**Critical sequencing:**
- A1 BLOCKS A2, A3, A4 (they consume the new CLI or read the renamed file)
- B1 BLOCKS B2, B3, B4 (they depend on epics.md being the new source of truth)
- Cascade A and Cascade B are mutually independent
- See plan file for the full sequencing and concurrency matrix

**Parallelism opportunities:**
- Phase 3 (story creation): up to 8 concurrent `momentum:create-story` sessions
- Phase 4a: A1, B1 run in parallel (2 sessions)
- Phase 4b: A2, A3, A4, B2, B3, B4 run in parallel (up to 6 sessions); realistic max 2–3 due to attention budget

**Open questions to resolve in Decisions 1 & 2:**
- Signals/ verdict: retire entirely, unify via `signal` event_type in ledger, or keep distinct?
- Custom event type policy: periodic audit step or just summary-surfacing?
- Epic schema additions: add `value_analysis`/`system_context`/`acceptance_conditions` to epic frontmatter, or fold into prose?
- Feature-grooming retirement vs. absorption: retire entirely, or restructure into `epic-grooming`?
