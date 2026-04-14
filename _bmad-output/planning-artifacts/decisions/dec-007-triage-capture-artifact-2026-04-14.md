---
id: DEC-007
title: Triage Capture Artifact — Unified Intake-Queue JSONL Event Log
date: '2026-04-14'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-04-14'
prior_decisions_reviewed:
  - DEC-005 (Momentum Cycle Redesign — D10 excluded gap-check from triage/intake, left capture artifact unresolved)
architecture_decisions_affected:
  - architecture.md triage-inbox contract (lines ~1671–1698) superseded by unified intake-queue.jsonl
  - architecture.md skill inventory intake row (line ~197) — will be split; intake describes capture only, triage gains its own row
  - architecture.md Decision 28 (Triage vs Refinement) — predates DEC-005; needs cross-reference to DEC-005 D10 and this SDR
stories_affected:
  - triage-skill
  - retro-triage-handoff
---

# DEC-007: Triage Capture Artifact — Unified Intake-Queue JSONL Event Log

## Summary

Two aspirational artifact contracts competed in Momentum's docs — `intake-queue.jsonl` (master-plan.md) and `triage-inbox.md` (architecture.md) — neither implemented. Both were intended to hold triage-adjacent items that don't become stories immediately (shape/watch/reject outcomes, retro→triage handoff items). This decision unifies them into a single JSONL event log, `intake-queue.jsonl`, with `source` and `kind` discriminators. The retro→triage handoff reads and writes the same artifact. The developer's stated aim: `intake` and `triage` should work together, and downstream workflows should read from a single source of truth. This retires `triage-inbox.md` before it is built and gives `momentum:triage` an unambiguous capture target for its non-ARTIFACT classifications (SHAPING, DEFER, REJECT) — a prerequisite for Story A (`triage-skill` rewrite).

---

## Decisions

### D1: Triage capture artifact — unify or separate? — ADOPTED (option a: one unified JSONL)

**Developer framing:** Triage needs a durable home for observations that don't become stories immediately — SHAPING, DEFER, REJECT outcomes — and for retro→triage handoff items. Two aspirational contracts exist (`intake-queue.jsonl` in master-plan, `triage-inbox.md` in architecture). The question is whether to unify, keep both with a boundary, replace with flagged index entries, replace with a markdown watchlist, or drop both and not capture these outcomes at all.

**Decision:** Adopt option (a) — one unified JSONL artifact. Single `_bmad-output/implementation-artifacts/intake-queue.jsonl` event log with per-event `source` discriminator (values: `triage`, `retro`, `assessment`, future upstreams) and `kind` discriminator (values: `shape`, `watch`, `rejected`, `handoff`). `momentum:triage` is the primary writer for shape/watch/rejected; `momentum:retro` writes `handoff` entries. Any skill that surfaces pending triage items (triage at start of session, sprint-planning during backlog synthesis, refine during hygiene) reads from this single file. The `triage-inbox.md` contract is retired.

**Rationale:**
I want intake and triage to work together and for downstream workflows to read from a single source.

---

## Phased Implementation Plan

| Phase | Focus | Timing | Key Stories |
|-------|-------|--------|-------------|
| 1 | Define the `intake-queue.jsonl` schema and implement write path in `momentum:triage` | Next sprint (when Story A is scheduled) | triage-skill |
| 2 | Add read path in `momentum:triage` to re-surface pending shape/defer items | Same sprint as Phase 1 | triage-skill |
| 3 | Wire `momentum:retro` to write `handoff` entries in the same artifact | After triage-skill ships | retro-triage-handoff |
| 4 | Update `momentum:sprint-planning` to optionally read `handoff` entries when synthesizing next sprint backlog | After retro-triage-handoff ships | retro-triage-handoff |

---

## Decision Gates

| Gate | Timing | Question | Criteria |
|------|--------|----------|----------|
| Gate 1 | After Phase 1–2 ship (triage-skill merged) | Is the single-artifact model actually working in practice? | Triage sessions produce readable, filterable events; developer can find pending items without searching multiple files; no friction reported in sprint retros |
| Gate 2 | After Phase 3 ships (retro handoff writes to queue) | Is the unified schema expressive enough for retro's needs? | All retro handoff items fit the schema without forcing special cases or drop-downs into free-form text fields |
