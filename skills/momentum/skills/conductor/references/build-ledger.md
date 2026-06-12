# Build Ledger — Event-Level Persistence

**Purpose:** Durable append-only record of every state-bearing event in a conduct build. The Conductor appends one JSONL row per event at event time. Phase 5 assembles the end-gate report from this ledger. Resume rehydrates all Conductor-scoped accumulators from it.

---

## Ledger Path

```
.momentum/sprints/{{sprint_slug}}/build-ledger.jsonl
```

One ledger per sprint. Created on first append (no pre-creation step). Sits beside existing sprint artifacts (`contract-freeze-baseline.sha256`, `coverage-plan.md`, `specs/`).

---

## Append-Only Rules

1. **Rows are only ever appended.** The Conductor never rewrites, edits, or deletes existing rows.
2. **Corrections are new rows.** When the Conductor must override a prior record (e.g., the scorecard-revert-reconciliation overriding a `fixed` disposition to `scope-reverted`), it appends a new override row referencing the original `finding_id` — the original row is preserved unchanged.
3. **Append mechanism.** A single-line Bash append per event:
   ```bash
   printf '%s\n' '{"event":"...","story_slug":"...","ts":"..."}' >> {{ledger_path}}
   ```
   No new script. No momentum-tools change. No batching.
4. **Crash-loss bound.** A crash loses at most the event in flight — never previously recorded state.

---

## Row Shape

Every ledger row is a single JSON object on one line. Every row carries:

| Field | Type | Required | Meaning |
|---|---|---|---|
| `event` | string | yes | Event type from the controlled set below. |
| `story_slug` | string | yes* | The story this event belongs to. Must be a real story slug (canonical join key, per finding-schema.md). *Exception: Conductor-level events not tied to a story — see Conductor-Level Events below. |
| `ts` | string (ISO 8601) | yes | Timestamp of the event. |

Additional fields vary by event type (see Event Type Set below). Every row uses `event` as the type discriminator — terminal rows use `event: "story-terminal"` with `outcome` as a payload field, not a top-level type discriminator. This normalization eliminates the heterogeneous `event:` vs `outcome:` mix in the current `{{build_log}}`.

### Join Key Rule

`story_slug` is the canonical join key, consistent with finding-schema.md's canonical-join-key rule. No `key` field (banned per build-results-ledger-schema.md). No prose-label values.

**Sanctioned sentinel values**: Two slug values are explicitly permitted as non-story-slug identifiers for sprint-level integration events where no single story owns the row:

| Sentinel | Used for |
|---|---|
| `e2e-integration` | E2E findings not attributable to a single story (sprint-level integration failures) |
| `sprint-integration` | AVFL and coverage-discharge findings attributable to the sprint as a whole rather than one story |

These two values are the ONLY permitted exceptions to the "must be a real story slug" rule. Any new sprint-level sentinel slug requires explicit addition to this table.

---

## Controlled Event-Type Set

Event names reuse the existing `{{build_log}}` vocabulary. No renames.

### Per-Story Pipeline Events

| Event | When appended | Additional fields |
|---|---|---|
| `story-launched` | Step 2.1 pipeline spawn | `title` |
| `stage-transition` | Stage-1 → stage-2 and stage-2 → stage-3 boundaries | `from_stage`, `to_stage` |
| `finding-disposition` | Each individual finding disposition in step 2.S3 | `finding_id`, `disposition` (fixed\|dismissed\|triaged-out\|escalated\|blocked\|scope-reverted), `summary`, `stakes_class`, `severity`. When dismissed: `dismissal_rationale` (non-empty, per Required-Rationale Rule). When escalated: `timing_tier`. |
| `stage3-fix-scope-reverted` | Write-scope guard fully discards a fix (step 2.S3) | `finding_id`, `finding_summary`, `reverted_files` |
| `stage3-escalation` | End-gate-expanded escalation recorded in step 2.S3 | `disposition: "escalated"`, `timing_tier: "end-gate-expanded"`, `finding_summary` |
| `stage3-mid-flight-escalation` | Mid-flight escalation dispatched in step 2.S3 | `disposition: "escalated"`, `timing_tier: "mid-flight"`, `finding_count` |
| `stage3-finding-blocked` | Finding exhausts retry budget in step 2.S3 | `finding_id`, `finding_summary`, `attempts` |
| `stage3-simplify-pass` | Phase C simplify cleanup completes | `findings_count`, `committed` (bool) |
| `stage3-story-blocked` | Story left unmerged after fix budget exhaustion | `leftover_count`, `stranded: true` |
| `story-terminal` | Story pipeline emits terminal signal (merged or failed/blocked/quarantined) | `outcome` (merged\|blocked\|quarantined\|contract-integrity-stop\|stranded), `title`. When merged: `findings_summary`, `escalations`. When blocked/quarantined: `reason`, `retry_count` or `merge_attempts`, `conflict_files` (quarantine). |
| `retry` | Pipeline-level retry in step 2.2 | `attempt` |
| `mid-flight-escalation` | Developer-facing mid-flight pause resolution (step 2.F) | `disposition: "escalated"`, `resolution` (fix-applied\|changed-action\|branch-aborted), `finding_summary` |
| `contract-integrity-stop` | Contract fingerprint mismatch at step 2.V | `contract_path`, `frozen_sha256`, `live_sha256` |

### Coverage Events

| Event | When appended | Additional fields |
|---|---|---|
| `coverage-disposition-deferred` | Step 2.C routes to covered-by-composition | `coverage_disposition`, `covered_by_scenario`, `title` |
| `coverage-disposition-default` | Step 2.C defaults missing/unrecognized value | `reason`, `observed_value` |
| `coverage-disposition-incomplete` | Step 2.C covered-by-composition with no named scenario | `reason`, `observed_coverage_disposition`, `observed_covered_by_scenario` |
| `coverage-deferral-discharged` | Step 3.D scenario passes all three conditions | `covered_by_scenario`, `outcome: "verified-by-composition"`, `evidence` |
| `coverage-deferral-undischarged` | Step 3.D scenario fails or not found | `covered_by_scenario`, `outcome` (scenario-not-found\|scenario-failed\|...), `evidence` |
| `coverage-discharge-consumer-complete` | Step 3.D consumer completes | `deferred_count`, `discharged_count`, `undischarged_count` |

### AVFL Events

| Event | When appended | Additional fields |
|---|---|---|
| `avfl-on-merge-complete` | Step 3.5 AVFL results recorded | `result_status`, `final_score`, `iterations`, `fixes_applied_count`, `leftovers_count`, `findings_count`, `stakes_findings_count` |
| `avfl-finding` | Step 3.3 — one row per AVFL finding (both fixed and residual) | `finding_id`, `disposition` (fixed\|residual\|escalated), `severity`, `stakes_class`, `summary`, `evidence`, `suggested_fix`, `source:"avfl-merge-review"` |

### E2E Events

| Event | When appended | Additional fields |
|---|---|---|
| `e2e-finding-auto-fixed` | Step 4.3 routine E2E finding fixed | `summary`, `disposition` |
| `e2e-mid-flight-escalation` | Step 4.3 mid-flight E2E escalation | `stakes_class`, `summary` |
| `e2e-stakes-escalation` | Step 4.3 end-gate-expanded E2E escalation | `stakes_class`, `timing_tier`, `summary` |
| `e2e-phase-complete` | Step 4.4 E2E phase summary | `scenarios_checked`, `passed`, `failed`, `blocked`, `e2e_findings_count` |

### End-Gate Events

| Event | When appended | Additional fields |
|---|---|---|
| `endgate-change-request-parsed` | Step 5.RC.1 parses developer change request | `item_count`, `items` |
| `endgate-change-workflow-pass` | Step 5.RC.2 completes a pass | `pass`, `items_resolved_this_pass`, `items_remaining` |
| `endgate-change-escalated` | Step 5.RC.2 item escalated | `fixer_id`, `stakes_class`, `summary` |
| `endgate-fix-budget-exhausted` | Step 5.RC.3 item exhausts budget | `fixer_id`, `attempts`, `summary` |
| `endgate-report-re-rendered` | Step 5.RC.4 report re-rendered | `pass`, `items_fixed`, `items_triaged_out`, `items_residual` |
| `major-residual-stub-created` | Phase 5 approve major-residual guard | `finding_id`, `severity`, `summary` |
| `scorecard-revert-reconciliation` | Phase 5 disposition override | `finding_id`, `story_slug`, `note` |

### Conductor-Level Events (no story_slug)

These events are the only permitted exceptions to the `story_slug`-required rule. Each is explicitly enumerated here — no other event type may omit `story_slug`.

| Event | When appended | Notes |
|---|---|---|
| `endgate-report-re-rendered` | Phase 5 report re-render | Sprint-level action, not per-story. |
| `coverage-discharge-consumer-complete` | Step 3.D consumer summary | Summarizes across all deferred stories. |
| `avfl-on-merge-complete` | Step 3.5 AVFL summary | Sprint-level integration review. |
| `e2e-phase-complete` | Step 4.4 E2E summary | Sprint-level E2E summary. |
| `conductor-warning` | Any phase — Conductor-detected anomaly | `story_slug` (optional — omit for sprint-level warnings), `reason` (non-empty string describing the anomaly). Used for: write-scope guard violations, invalid fixer behavior, dismissed findings with missing rationale, and similar Conductor-detected issues that are not findings in the canonical sense but must be recorded. |

For these events, `story_slug` may be omitted or set to `null`. All other events must carry a real story slug.

---

## Enum Vocabulary — By Reference

All controlled enums are defined in companion schemas and reused verbatim:

- **`disposition`**: `fixed | dismissed | triaged-out | escalated` — per finding-schema.md v1.1. Plus workflow-documented extensions: `blocked` (maps to `escalated` for schema consumers), `scope-reverted` (maps to `triaged-out` for schema consumers) — per step 2.S3 line 577-580.
- **`severity`**: `critical | major | minor | low` — per finding-schema.md v1.1 Severity Enum.
- **`type`**: 10-value closed set — per finding-schema.md v1.1 Type Enum.
- **`stakes_class`**: `security-auth-isolation | irreversible-destructive | high-blast-radius-architecture | routine` — per finding-schema.md v1.1. Default: `routine`.
- **`timing_tier`**: `end-gate-expanded | mid-flight` — per finding-schema.md v1.1. Default: `end-gate-expanded`.

Do not restate or fork these enums. Producers reference the schemas above.

### Required-Rationale Rule (inherited)

When a `finding-disposition` row has `disposition: "dismissed"`, it must carry a non-empty `dismissal_rationale` — per finding-schema.md's Required-Rationale Rule. A dismissed row with empty or missing rationale is invalid.

---

## Idempotent Re-Append Guidance (Resume)

When the Conductor resumes a build and rehydrates from an existing ledger:

1. **Read all existing rows** to rebuild Conductor-scoped accumulators.
2. **Track seen events.** Build a set of `(story_slug, event, finding_id)` tuples from existing rows.
3. **Do not re-append** events for stories that are not re-run. A story already at status `review` or `done` (merged in a prior session) will not be re-dispatched — its prior ledger rows stand.
4. **Stories that ARE re-run** (reset from `in-progress` to `ready-for-dev` by the reconcile) will produce fresh events; these are new rows and are appended normally. The prior session's rows for that story (if any) remain — they document the interrupted attempt.

This prevents duplicate rows without requiring dedup logic at read time. The ledger is a faithful timeline: prior-session events and current-session events coexist, distinguishable by timestamp.

---

## Companion Schema: Build-Results Ledger

The story-level build-results row (`skills/momentum/references/build-results-ledger-schema.md`, v1.0) and the event-level build ledger are companion schemas at different granularities. A build-results row is derivable by folding a story's event-level ledger rows (collecting terminal outcome, finding counts, disposition counts, merge status). The two schemas join on the story slug (`slug` in build-results, `story_slug` in the event ledger).

---

## Source Decisions

- **DEC-035** — One human end-gate; legible auto-fix loop; the gate this ledger makes durable.
- **DEC-036** — Stakes/timing tiers the ledger must record; mid-flight bar must not be widened.
- **Retro finding (conduct-core)** — Build-results schema drifted mid-build (structured vs prose rows). This ledger's controlled event-type set and normalization rule (every row has `event`) prevents that drift.
