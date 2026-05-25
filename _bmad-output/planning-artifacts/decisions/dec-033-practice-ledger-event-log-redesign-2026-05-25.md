---
id: DEC-033
title: Practice-Ledger Event-Log Redesign
date: '2026-05-25'
status: decided
source_research:
  - path: _bmad-output/planning-artifacts/assessments/aes-003-practice-ledger-defects-and-epic-unification-2026-05-25.md
    type: assessment
    date: '2026-05-25'
prior_decisions_reviewed:
  - DEC-007 (Unified Triage/Retro Capture Artifact — intake-queue.jsonl event log)
  - DEC-031 (Legibility Before Automation — Canvas Gate Surface; informs the discipline framing)
  - Architecture Decision 1c (Findings Ledger — same hidden defect class as Decision 52 / DEC-007)
  - Architecture Decision 52 (DEC-007 intake-queue Schema Contract)
  - PRD FR120 (.momentum/signals/ Ledger Directory contract)
  - PRD FR114–FR117 (triage/intake-queue/retro handoff/sprint-planning handoff queue read)
architecture_decisions_affected:
  - Architecture Decision 52 — SUPERSEDED: intake-queue.jsonl renamed to practice-ledger.jsonl; schema rewritten; true append-only enforced; consume becomes an appended event, not a whole-file rewrite
  - Architecture Decision 1c — AMENDED: Findings Ledger inherits the event-log shape established here; future implementation must use the event_id + entity_id pattern, never whole-file rewrites
  - Architecture .momentum/ State Layout section — UPDATED: signals/ subsection retired (absorbed into ledger); intake-queue.jsonl renamed; entity_id semantics added
  - Architecture Read/Write Authority table — UPDATED: intake-queue.jsonl row renamed; signals/ rows removed; producer set expanded to reflect signal use cases now flowing through ledger
  - PRD FR115 — REWRITTEN: new schema, new filename, new reader CLI subcommands, hard-cut migration
  - PRD FR114, FR116, FR117 — UPDATED: reference new filename + CLI subcommand names; closure-discipline expectations added
  - PRD FR120 — SUPERSEDED: signals/ directory retired; signal use cases absorbed into practice-ledger as entries with appropriate source + payload
stories_affected:
  - practice-ledger-features-epics-cascade-sequenced-plan (process story tracking the cascade)
  - All 4 cascade A stories to be created (A1 ledger schema + CLI; A2 hygiene cleanup; A3 Impetus rule update; A4 skill workflow updates)
---

# DEC-033: Practice-Ledger Event-Log Redesign

## Summary

The current `.momentum/intake-queue.jsonl` carries four production defects: architecture-vs-code drift (Decision 52 claims append-only; the consume code path does whole-file rewrites), lost-update concurrency unsafety (no locking, no atomic write-then-rename), backlog rot (12 of 52 open entries are stale because no workflow auto-closes anything), and a surfacing defect in the recently-authored Impetus "last 5" rule (90% of open entries hidden; the 5 surfaced are mostly test scaffolding). A latent fifth defect lives in the design of Decision 1c (Findings Ledger) — same JSONL-rewrite pattern would inherit if that ledger ships without remediation. AES-003 captured all five.

This decision adopts a unified event-log design that fixes all four production defects and pre-empts the latent fifth. The practice-ledger becomes a true append-only event log with first-class `event_id` (immutable per row) and `entity_id` (repeats across rows for the same logical entity) distinction; status transitions are new events, never mutations; closure is a hard discipline backed by a 15-day TTL with automatic `closed_stale` events emitted by a daily Claude Code Routine. The unused `.momentum/signals/` directory is absorbed into the unified ledger — every open entry is the attention surface; closure discipline replaces the need for a separate attention-filter mechanism. The reader becomes DuckDB-backed so state queries are cheap regardless of ledger size. Migration is hard-cut: the existing 88 entries freeze as a pre-2026-05 archive; the new file starts empty under the new schema and filename.

The Impetus surfacing model drops the "last 5" anti-pattern in favor of honest counts and recurrence patterns, with drill-down via CLI. The Findings Ledger (architecture Decision 1c) gets a forward pointer to this decision so future activation reproduces the correct pattern rather than the latent defect.

The 10 sub-decisions below were ratified directionally during the AES-003 assessment conversation; this document formalizes them and links them to downstream cascade work.

---

## Decisions

### D1: True append-only event log — ADOPTED

**Research recommended:** Rename `.momentum/intake-queue.jsonl` to `.momentum/practice-ledger.jsonl`. Make records immutable. Status transitions become new events appended with the same `entity_id` as the original. Eliminate whole-file rewrites entirely. Implementation uses POSIX `open('a')` with O_APPEND for all writes; "consume" becomes "append a `consumed` event referencing the original entity_id."

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. The current consume path's whole-file rewrite is the root cause of the lost-update unsafety and the architecture-vs-code drift; eliminating the rewrite pattern resolves both at the schema layer. JSONL's POSIX-atomic-append safety only applies to true append-only — restoring that property restores the concurrency guarantee the architecture originally promised.

### D2: Schema with first-class event_id and entity_id distinction — ADOPTED

**Research recommended:** Schema fields per row:
- `event_id` — immutable per row, unique, never reused
- `entity_id` — identifies the logical thing events are about; repeats across rows for the same entity
- `ts` — ISO-8601 UTC
- `event_type` — fixed enum (see D3) plus custom escape
- `custom_event_type` — present only when event_type=custom
- `source` — the producer skill or workflow
- `actor` — human or agent identity
- `payload` — event-type-specific structured data

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. The event_id/entity_id distinction is the load-bearing primitive: event_id identifies the immutable row; entity_id identifies the logical thing whose lifecycle is the chain of events. Closing an entity = appending a closure event referencing the entity_id, never mutating the original row. "Open" becomes a derived state (last event for an entity_id is non-terminal), not a stored field.

### D3: Seven event types, with closure as first-class — ADOPTED

**Research recommended:** Enum values:
- `created` — entity born; sets the clock for TTL
- `updated` — non-status field changed (title, payload, source enrichment)
- `consumed` — actively resolved with outcome reference
- `rejected` — explicitly won't-do (reason in payload)
- `closed_stale` — auto-emitted when TTL elapses without resolution
- `reopened` — previously-closed entity brought back; uses the same entity_id
- `custom` — escape hatch; `custom_event_type` field carries the actual name

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. `closed_stale` is first-class (not a payload field on `consumed`) so attention-debt patterns are directly queryable — recurring closed_stale of the same entity shape is itself a triage signal. `reopened` reusing the original entity_id preserves the full attention/inattention history rather than fragmenting it across IDs. The `custom` escape with `custom_event_type` makes ad-hoc extensions visible and auditable.

### D4: Closure discipline — every record has a closure condition, 15-day TTL default — ADOPTED

**Research recommended:** Originating skill is responsible for emitting closure events on resolution (consumed/rejected). If 15 days elapse with the entity still open, the close-stale process emits a `closed_stale` event for it. Other closure conditions can be defined per event_type. No record may be created without a closure path.

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. The current intake-queue rot (12 of 52 open are stale) is the direct consequence of no closure discipline. A 15-day TTL is aggressive enough to keep the open list bounded but generous enough that genuine work can land. "Closed due to lack of attention" is a real and meaningful state — distinct from `consumed` (actively resolved) and `rejected` (explicitly won't-do) — and worth tracking because recurring stale closure of the same entity shape is signal that the practice has a structural gap.

### D5: Routine-driven auto-close with session-start safety net — ADOPTED

**Research recommended:** Primary mechanism: Claude Code Routine (via `CronCreate`) runs `momentum-tools practice-ledger close-stale --age-days 15` daily on a fixed schedule. Secondary mechanism: Impetus session-start reads the timestamp of the last close-stale run; if older than 24h, invokes the close-stale CLI itself before surfacing state. Both invocations are idempotent.

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. Routines are in-ecosystem (no separate cron/launchd to install) and make the closure cadence visible alongside other practice automation. The session-start safety net handles the case where Routines miss a day or the developer hasn't opened Claude Code for an extended period — closure happens reliably regardless of operational gaps.

### D6: Signals/ absorbed entirely into practice-ledger — ADOPTED

**Research recommended:** Retire `.momentum/signals/` directory. The two existing signal use cases (`triage-uncleared`, `avfl-finding-pending-upstream-fix`) become entries in practice-ledger with `source: triage` / `source: avfl` and appropriate payload. Every open entry in the ledger IS the attention surface — no separate attention filter, no separate read path. PRD FR120 marks superseded.

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. The signals/ infrastructure was designed as a complementary attention-flag surface distinct from the persistent event log, but producers were never shipped (ARCH-8). With closure discipline (D4) and honest count-based surfacing (D9), the unified ledger handles the attention-surface job natively — an open entry IS something demanding attention. Maintaining a parallel "attention vs. history" surface adds coordination cost without providing functionality the ledger doesn't already give us. One artifact, one schema, one CLI.

### D7: DuckDB-backed reader CLI — ADOPTED

**Research recommended:** `momentum-tools practice-ledger` gets subcommands:
- `summary` — counts by source / event_type / age
- `open` — entities whose current (last) event is non-terminal
- `history --entity <id>` — full event chain for one entity
- `since <ts>` — events after a timestamp
- `by-source <source>` — filter by producer

Reader queries fold events by entity_id to derive current state via SQL. State is computed, never stored — derivation is the source of truth.

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. DuckDB is already a required dependency (Decision 27 — retro transcript audit) so no new infrastructure cost. State-by-derivation eliminates "stored state goes out of sync with event history" failure modes inherent to mixed mutation/append schemas. Query performance is single-digit milliseconds at any realistic ledger scale (88 entries today; even 10K entries ≈ 3 MB → still instant).

### D8: Hard-cut migration — ADOPTED

**Research recommended:** Existing 88 entries freeze as `.momentum/practice-ledger-pre-2026-05.jsonl` (informational; readers can glob both files). New `.momentum/practice-ledger.jsonl` starts empty under the new schema. Reader paths are glob-ready from day one for future rotation. The rename itself is the migration boundary — no in-place schema transformation.

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. Synthesizing event histories for the existing 88 entries would invent chronology we don't have (the original entries were mutated in place, so prior-state history is already lost). Hard cut is honest: the pre-2026-05 file stays readable for archeology; the new file starts clean under the correct schema. The glob-ready reader pattern also future-proofs for log rotation when the new file eventually grows large enough to warrant it.

### D9: Impetus surfacing — honest counts, no inline enumeration — ADOPTED

**Research recommended:** Session-start surfaces structured counts in Impetus voice:
- "N open entries (X this week, Y older than 30 days, Z near auto-close)"
- Recurring patterns from history ("'X' has been closed_stale 4 times in 60 days")

Developer drills in via CLI when curious. No inline enumeration of entries. Drops the "last 5" anti-pattern entirely.

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. The "last 5" pattern surfaced the wrong 5 (mostly test scaffolding) and hid the rot — exactly the failure mode it was meant to prevent. Honest counts cannot lie about backlog size, cannot hide stale entries behind newer junk, and cannot pretend the practice is tidier than it is. Recurring patterns are a meta-signal worth surfacing because they point at structural practice gaps that won't fix themselves.

### D10: Findings Ledger (architecture Decision 1c) pre-empted — ADOPTED

**Research recommended:** When Epic 6 flywheel work eventually ships, the Findings Ledger at `~/.claude/momentum/findings-ledger.jsonl` inherits the event-log shape from this decision (event_id + entity_id, append-only, no whole-file rewrites). Architecture Decision 1c gets a forward pointer to DEC-033 so future implementation reproduces the correct pattern instead of the latent defect.

**Decision:** Adopted as stated.

**Rationale:** Per AES-003 assessment. The Findings Ledger has zero shipped code today, so the defect is purely in the design. Cheap to pre-empt now; expensive to fix after activation. The flywheel use case (cross-project pattern detection over findings history) benefits from the same event-log semantics — event_id for individual finding records, entity_id for the underlying issue or pattern that recurs across stories. Naturally fits.

---

## Phased Implementation Plan

The cascade plan at `~/.claude/plans/i-like-sequencing-the-optimized-lagoon.md` covers the implementation sequencing. Headline shape:

1. **Cascade A — Practice-ledger** (this decision)
   - **A1** Ledger schema + CLI redesign (blocks A2/A3/A4)
   - **A2** Hygiene cleanup (one-time pass closing the 12 stale entries)
   - **A3** Impetus rule update (drop "last 5"; honest counts; absorb signals/ awareness)
   - **A4** Skill workflow updates (retro, triage, sprint-planning, intake, decision, assessment, feature-breakdown — point to new CLI)
2. **Decision 2 — Epic-layer consolidation** (separate decision document, authored next)
3. **Post-cascade batch AVFL** scan-profile pass on integrated final state per `feedback_avfl_post_merge_strategy.md` convention

Cascade A respects concurrency constraints captured in the plan: serialized index writes (max 2 parallel create-story sessions; max 1 quick-fix at a time touching architecture.md). A1 is the blocking foundation story; A2/A3/A4 run in pairs after A1 lands.

---

## Decision Gates

The following conditions, if reached, would warrant re-opening this decision:

- **Routines prove too expensive at the actual scale.** If the daily Routine spinning up a full Claude agent for the close-stale pass is cost-disproportionate to the work (which is just a CLI shell-out), revisit and consider native launchd / cron instead.
- **DuckDB query latency exceeds ~200ms regularly.** Trigger to add log rotation (move active file → archive when over a size threshold; readers continue globbing `practice-ledger*.jsonl`).
- **The 15-day TTL produces excessive closed_stale noise.** If the developer is constantly re-opening entities the TTL closed, the TTL is too short — adjust per event_type or globally.
- **Custom event_types proliferate beyond the fixed enum's capacity.** If the `custom` escape becomes the majority of writes, the enum has missing primitives — revisit to promote frequently-used custom types into the fixed set.
- **Findings Ledger activation reveals the event-log pattern doesn't fit.** If Epic 6 work discovers semantic gaps (e.g., needs cross-entity correlation the schema doesn't support), revisit D10's inheritance assumption.
