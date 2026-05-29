---
title: "A2: Practice-ledger hygiene cleanup — close 12 stale entries"
story_key: a2-practice-ledger-hygiene-cleanup-close-12-stale-entries
status: ready-for-dev
epic_slug: ad-hoc
feature_slug:
story_type: maintenance
change_type: script-cli
verification_method: execution test — run CLI calls, confirm open count drops by 12; record pre-count, exact CLI invocations, and post-count in the Dev Agent Record
depends_on:
  - a1-practice-ledger-schema-cli-redesign-true-append-only
touches:
  - .momentum/practice-ledger.jsonl
  - .momentum/stories/a2-practice-ledger-hygiene-cleanup-close-12-stale-entries.md
---

# A2: Practice-ledger hygiene cleanup — close 12 stale entries

## Story

As a developer,
I want to close out the 12 stale practice-ledger entries flagged in AES-003 Finding 3 using the new ledger CLI from A1,
so that the practice-ledger reflects only genuinely open work and `momentum-tools practice-ledger open` returns an accurate count (52 → 40).

## Description

One-time hygiene pass that closes the 12 stale entries identified in AES-003 Finding 3, using the new append-only CLI delivered by Story A1 (DEC-033 D1–D3, D6, D7).

Pre-state (verified 2026-05-26 against `.momentum/intake-queue.jsonl`):
- 88 total entries, 52 open, 36 consumed.
- 12 stale entries to close (all currently `status: "open"`):
  - **8 "superseded by ..." entries** — work explicitly overridden by a later decision; close with event_type `consumed`, payload `outcome_ref: "superseded:<DEC-id>"` extracted per entry.
  - **3 "Test: ..." entries** — triage spike scaffolding (REJECT, SHAPING, DEFER); close with event_type `consumed`, payload `outcome_ref: "test-leftover"`.
  - **1 "Old triage-inbox.md approach" entry** — pre-DEC-007 artifact; close with event_type `consumed`, payload `outcome_ref: "test-leftover"`.

The work is data hygiene — no new code. All 12 closure events MUST be appended via the new CLI shipped in A1; no direct edits to the JSONL file. A1's hard-cut migration (DEC-033 D8) freezes the existing entries as `.momentum/practice-ledger-pre-2026-05.jsonl` and starts a fresh `.momentum/practice-ledger.jsonl`. **This story must run against the frozen pre-2026-05 file** — the rot lives there, not in the new file.

**Pain context:** One-time hygiene pass referenced in AES-003 Finding 3. Closes 23% of the open backlog. Restores honest open-count semantics so Impetus (post-A3) and any reader sees real practice state.

**Source:** triage handoff `practice-ledger-and-epic-cascade-stories-2026-05-25`; AES-003 Finding 3; DEC-033 D3 (consumed event), D8 (hard-cut migration).

### The exact 12 entries (verified)

**Superseded (8) — outcome_ref pattern `superseded:<DEC-id>`:**

| event_id (pre-2026-05) | title | outcome_ref |
|---|---|---|
| iq-20260424205245-50b859cb | dashboard-ux-wireframes stub — superseded by Claude Design Pass 4–7 | `superseded:design-pass-4-7` |
| iq-20260516154102-22515545 | code-reviewer-agent-definition — superseded by DEC-020/DEC-024 | `superseded:DEC-020,DEC-024` |
| iq-20260516154102-1ae5c62a | architect-guard-agent-definition — superseded by DEC-020/DEC-024 | `superseded:DEC-020,DEC-024` |
| iq-20260516154102-d032731e | documenter-agent-definition — superseded by DEC-020 | `superseded:DEC-020` |
| iq-20260516154102-f89de525 | dev-fixer-agent-definition — superseded by DEC-020/DEC-025 | `superseded:DEC-020,DEC-025` |
| iq-20260516154102-221bdb70 | agents-md-manifest-format — superseded by DEC-023 | `superseded:DEC-023` |
| iq-20260516154102-f098660a | build-guidelines-skill — superseded by DEC-026 | `superseded:DEC-026` |
| iq-20260518032341-976884b5 | DEC-029: refine/rescope 7 existing backlog stories superseded by method-routed validation | `superseded:DEC-029` |

**Test/leftover (4) — outcome_ref `test-leftover`:**

| event_id (pre-2026-05) | title |
|---|---|
| iq-20260416054851-aec14053 | Test: REJECT item from triage |
| iq-20260416055625-ab0b3dc4 | Test: SHAPING item from triage |
| iq-20260416055626-153bbdd3 | Test: DEFER item from triage |
| iq-20260416055624-9f5c9655 | Old triage-inbox.md approach |

Total: 8 + 4 = **12 stale entries**.

> Reconciliation note: the prior intake stub mentioned "10 superseded + 3 test-leftover = 13". A re-count of the live ledger on 2026-05-26 yielded 8 + 4 = 12, matching AES-003 Finding 3 exactly. This story uses the verified count of 12.

## Acceptance Criteria

1. **CLI-only closure path used for every entry.** All 12 closure events are appended via the new `momentum-tools practice-ledger` CLI shipped in A1 (per DEC-033 D7 reader/writer split — `consumed` is appended as a new event referencing the original `entity_id`). No direct file edits to `.momentum/practice-ledger.jsonl` or `.momentum/practice-ledger-pre-2026-05.jsonl`.

2. **Eight `consumed` events appended for the superseded entries.** Each event carries:
   - `event_type: "consumed"`
   - `entity_id`: the original `id`/`entity_id` of the stale entry as it appears in `.momentum/practice-ledger-pre-2026-05.jsonl`
   - `payload.outcome_ref`: per the mapping table above (`superseded:<DEC-id>` or `superseded:design-pass-4-7`)
   - `source`: `triage` (or whatever the original entry's `source` field was — preserved)
   - `actor`: `developer` (the human invoking the hygiene pass)

3. **Four `consumed` events appended for the test/leftover entries.** Each event carries:
   - `event_type: "consumed"`
   - `entity_id`: the original `id`/`entity_id` of the stale entry
   - `payload.outcome_ref: "test-leftover"`
   - `source`: as preserved from the original entry
   - `actor`: `developer`

4. **`open` count drops by exactly 12.** Post-cleanup, `momentum-tools practice-ledger open` (which folds events by `entity_id` per DEC-033 D7 to derive current state) returns 12 fewer rows than the pre-cleanup count. The 12 reduced entities correspond exactly to the table above.

5. **No entities other than the 12 are touched.** A diff of `open` output before vs. after shows only the 12 listed entities transitioning out of the open set. No other entity changes status.

6. **Implementation is either a shell script committed to the repo OR a sequence of CLI invocations recorded in the Dev Agent Record.** Both are acceptable. If a script is committed, place it at `scripts/practice-ledger-hygiene-2026-05-26.sh` (one-shot, dated; not a recurring tool). If invocations are recorded, paste the exact 12 commands into the Dev Agent Record so the run is auditable.

7. **Smoke test recorded.** The Dev Agent Record must contain:
   - Pre-count: output of `momentum-tools practice-ledger open | wc -l` (or equivalent) before any closures.
   - The 12 closure invocations (or the script path + invocation).
   - Post-count: output of the same command after closures.
   - Delta: confirmation that pre - post = 12.

8. **Event chain integrity preserved per DEC-033 D2/D7.** For at least one of the closed entities (pick any), `momentum-tools practice-ledger history --entity <id>` returns at least 2 events: the original `created` event from the frozen file (or its hard-cut equivalent) AND the new `consumed` event appended by this story.

9. **No regression to other open entries.** Running `momentum-tools practice-ledger summary` post-cleanup shows the remaining open count is exactly `pre_open_count − 12`, and the `consumed` count is exactly `pre_consumed_count + 12`. No other source/event-type counts drift.

## Tasks / Subtasks

- [ ] **Task 1 (`script-cli` / `config-structure`): Prepare invocation list.**
  - Read the 12-entry mapping table from this story's Description.
  - Either author `scripts/practice-ledger-hygiene-2026-05-26.sh` containing 12 `momentum-tools practice-ledger consume` invocations (or whatever the exact A1 subcommand name turns out to be — verify against A1's shipped CLI before authoring), one per entity, each with the correct `--entity-id`, `--outcome-ref`, and `--actor developer`; OR prepare the 12 invocations as a copy-pasteable block for direct execution.
  - Cross-reference each `entity_id` against `.momentum/practice-ledger-pre-2026-05.jsonl` (post-A1) to confirm the IDs are findable in the frozen file. If A1 used a different rename strategy (e.g., entity_ids regenerated), follow A1's mapping convention.

- [ ] **Task 2 (`script-cli`): Capture pre-state.**
  - Run `momentum-tools practice-ledger open` and capture the full output to a temp file (e.g., `/tmp/practice-ledger-open-pre.txt`).
  - Run `momentum-tools practice-ledger summary` and capture counts.
  - Paste both into the Dev Agent Record under "Pre-cleanup state".

- [ ] **Task 3 (`script-cli`): Execute the 12 closures.**
  - Run the 12 `consume` invocations (script or copy-pasted block).
  - Capture stdout/stderr of each invocation.
  - If any invocation errors (e.g., entity already closed, unknown entity), HALT, diagnose, and adjust before proceeding. Do not skip a failed entry without a Dev Agent Record note.

- [ ] **Task 4 (`script-cli`): Capture post-state and verify deltas.**
  - Run `momentum-tools practice-ledger open` again; capture to `/tmp/practice-ledger-open-post.txt`.
  - Run `momentum-tools practice-ledger summary` again.
  - Diff pre vs. post `open` output: confirm exactly the 12 listed entities disappeared from the open set; no other changes.
  - Confirm: `open_pre - open_post == 12` AND `consumed_post - consumed_pre == 12`.

- [ ] **Task 5 (`script-cli`): Verify event chain integrity.**
  - Pick any one of the 12 closed entities (e.g., `iq-20260516154102-d032731e`).
  - Run `momentum-tools practice-ledger history --entity <id>`.
  - Confirm the output shows at least 2 events: the original (from pre-2026-05 archive) and the new `consumed` event from this story.

- [ ] **Task 6 (`specification`): Record smoke test in Dev Agent Record.**
  - Paste pre-count, post-count, delta confirmation, and the verification output from Task 5 into the Dev Agent Record.
  - List the 12 invocations (or script path).
  - If a script was committed, list it in the File List.

## Dev Notes

### Architecture Compliance

- **DEC-033 D1 (true append-only):** This story only appends events. It never edits, rewrites, or mutates existing rows. Conformance: every closure is a new `consumed` row referencing the original `entity_id`.
- **DEC-033 D2 (event_id / entity_id distinction):** Closure events get fresh `event_id` values (the CLI from A1 assigns these). They reuse the original `entity_id` so `history --entity <id>` returns the full chain.
- **DEC-033 D3 (consumed event):** `consumed` is the correct event_type for "actively resolved with outcome reference." `superseded:` and `test-leftover` are outcome_ref values, not separate event_types.
- **DEC-033 D7 (DuckDB-backed reader):** Post-cleanup verification uses the reader CLI — state is derived, not stored. Counts must come from the reader, not from grepping the JSONL.
- **DEC-033 D8 (hard-cut migration):** The 12 stale entries live in `.momentum/practice-ledger-pre-2026-05.jsonl` (frozen by A1). Closure events go into the active `.momentum/practice-ledger.jsonl`. Readers glob both per A1's glob-ready reader design.

### Testing Requirements

This is a `script-cli` change type per the verification-standard routing table: **execution test** — run the CLI command(s); observe that output matches spec. No unit tests. No evals. The "test" is the smoke test recorded in the Dev Agent Record (ACs 4, 5, 7, 8).

**Harness-profile reference:** `cli-local-shell` (default for CLI execution tests — see `momentum/verification-harness.json`). The CLI is `momentum-tools` invoked from a local shell in the project root; no network, no special runtime.

**Adversarial guard (verification-standard §4):** All AC checks use ordinary-user knowledge — public CLI subcommands (`open`, `summary`, `history`, `consume`), public output fields (counts, entity IDs, titles), and the publicly-documented event schema from DEC-033. No insider knowledge of CLI internals or storage layout.

### Implementation Guide

#### Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 5 → `script-cli` (execution test)
- Task 6 → `specification` (direct authoring; subsumed by primary `script-cli` method per verification-standard §1)

##### script-cli Tasks: Execution Test

This story closes 12 stale entities by appending events via a CLI shipped by another story (A1). The work is data hygiene, not new code. There is no script logic to TDD — the script (or invocation list) is a literal sequence of CLI calls against the live ledger.

1. **Confirm A1's CLI shape first.** Before authoring any script or invocation list, run `momentum-tools practice-ledger --help` (or A1's documented entry point). Confirm:
   - The subcommand name for appending a `consumed` event (`consume`? `close`? `append --event consumed`?). DEC-033 D7 lists reader subcommands but doesn't fix the writer subcommand name — verify against A1's shipped surface.
   - The flag for `entity_id` (e.g., `--entity-id`, `--entity`, `--id`).
   - The flag for `outcome_ref` payload (e.g., `--outcome-ref`, `--payload outcome_ref=...`).
   - The flag for `actor` (e.g., `--actor`).
   - Whether `source` is auto-inherited from the original entity or must be passed.

2. **Run the smoke test loop in this exact order:**
   - Capture pre-state (Task 2)
   - Execute closures (Task 3)
   - Capture post-state (Task 4)
   - Diff and verify (Task 4)
   - Verify event chain (Task 5)

3. **Idempotency note:** If a `consumed` event is appended twice for the same `entity_id`, the second append is harmless data — the open-count derivation in DEC-033 D7 uses the *last* event for an entity, and "last = consumed" remains correct regardless of duplicates. Still, do not re-run the script after a successful pass; it leaves spurious events in history. If a partial failure occurs, identify which entities were closed and only re-run the remainder.

4. **Failure handling:** If A1's CLI rejects any of the 12 invocations (e.g., "entity not found" because A1's migration regenerated entity_ids, or "outcome_ref format invalid"), HALT and:
   - Document the rejection in the Dev Agent Record.
   - If the issue is in A1's CLI design, file an upstream-fix note rather than working around it.
   - If the issue is the entity_id mapping (because A1's hard-cut changed IDs), follow A1's documented mapping convention to translate, then resume.

##### Additional DoD items for script-cli tasks

- [ ] Pre-count and post-count both captured from `momentum-tools practice-ledger open` (or `summary`)
- [ ] Delta = 12 confirmed
- [ ] No other entities transitioned out of `open` (diff of pre/post open lists matches the 12-row table exactly)
- [ ] At least one `history --entity <id>` verification recorded (AC 8)
- [ ] All 12 invocations (or the script path) listed in the Dev Agent Record
- [ ] No direct edits to either `.momentum/practice-ledger.jsonl` or `.momentum/practice-ledger-pre-2026-05.jsonl`

##### Gherkin separation reminder (DEC-030)

Per Decision 30 black-box separation: if Gherkin specs exist for this sprint at `.momentum/sprints/sprint-2026-05-26/specs/`, they are off-limits to the dev agent. Implement against the plain-English ACs in this file only. Never read or write `.feature` files during implementation.

### Project Structure Notes

- **Primary touch:** `.momentum/practice-ledger.jsonl` — 12 new `consumed` events appended (one per stale entity).
- **Read-only references:** `.momentum/practice-ledger-pre-2026-05.jsonl` (frozen, never edited; used only to verify pre-existing `entity_id` values).
- **Optional touch:** `scripts/practice-ledger-hygiene-2026-05-26.sh` — one-shot dated script if the developer chooses the script path over copy-pasted invocations. Not retained as a recurring tool.
- **No skill / agent / config changes.** This is pure data hygiene against an already-shipped CLI.

### References

- **DEC-033 — Practice-Ledger Event-Log Redesign** (`_bmad-output/planning-artifacts/decisions/dec-033-practice-ledger-event-log-redesign-2026-05-25.md`) — D1 (true append-only), D2 (event_id/entity_id), D3 (event_type enum incl. `consumed`), D7 (reader CLI), D8 (hard-cut migration).
- **AES-003 Finding 3** (`_bmad-output/planning-artifacts/assessments/aes-003-practice-ledger-defects-and-epic-unification-2026-05-25.md`) — the canonical source for the "12 stale entries" count (8 superseded + 4 test/leftover).
- **Cascade plan** (`.momentum/stories/practice-ledger-features-epics-cascade-sequenced-plan.md`) — sequencing constraints: A1 blocks A2; A2/A3/A4 can run in parallel after A1 lands.
- **Triage handoff** (`.momentum/handoffs/practice-ledger-and-epic-cascade-stories-2026-05-25.md`) — original source for the cascade A story set.
- **Story A1** (`.momentum/stories/a1-practice-ledger-schema-cli-redesign-true-append-only.md`) — the dependency: provides the CLI, the renamed files, and the hard-cut migration this story consumes.

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — execution proceeded without errors.

### Completion Notes List

All 12 entries closed via CLI. No direct file edits made. Script committed for auditability.

**AC 4/5/8 design gap note:** A1's `_load_duckdb_events` implementation treats all entries in `practice-ledger-pre-2026-05.jsonl` as `archive_entries` (opaque count), NOT as derivable new-schema entities. As a result:
- `practice-ledger open` returns 0 both pre- and post-cleanup (archive entities never appear in the open set)
- `practice-ledger history --entity <id>` returns only 1 event (the new `consumed` event) instead of 2, because the original archive entry lacks `event_id` and is excluded from history queries
- The "52 -> 40 open count" semantic in the story description does not hold with A1's implementation — archive entities are not counted in the open set

This is an upstream design gap in A1. The 12 `consumed` events ARE correctly appended and are auditable via `summary` (new_entries: 12, by_event_type: {consumed: 12}). The intent of the hygiene pass is satisfied — any future migration that projects archive entries into new-schema events will inherit these consumed markers via entity_id matching. Recommend filing an upstream-fix note against A1 to resolve the history chain gap (AC 8) and open-count semantics (AC 4/5).

#### Pre-cleanup state

```
$ python3 skills/momentum/scripts/momentum-tools.py practice-ledger open
{"action":"practice_ledger_open","success":true,"entities":[],"count":0}

$ python3 skills/momentum/scripts/momentum-tools.py practice-ledger summary
{"action":"practice_ledger_summary","success":true,"new_entries":0,"archive_entries":88,"by_event_type":{},"by_source":{},"age_buckets":{"lt_7d":0,"d7_30":0,"gt_30d":0,"near_auto_close":0}}
```

Pre-open count (new-schema): 0
Pre-consumed count (new-schema): 0
Archive entries: 88 (includes 52 open + 36 consumed in old schema)

#### Closure invocations

Script committed: `scripts/practice-ledger-hygiene-2026-05-26.sh`

Exact invocations executed:

```bash
# Superseded entries (8)
python3 skills/momentum/scripts/momentum-tools.py practice-ledger consume --entity-id iq-20260424205245-50b859cb --actor developer --source triage --outcome-ref "superseded:design-pass-4-7"
python3 skills/momentum/scripts/momentum-tools.py practice-ledger consume --entity-id iq-20260516154102-22515545 --actor developer --source triage --outcome-ref "superseded:DEC-020,DEC-024"
python3 skills/momentum/scripts/momentum-tools.py practice-ledger consume --entity-id iq-20260516154102-1ae5c62a --actor developer --source triage --outcome-ref "superseded:DEC-020,DEC-024"
python3 skills/momentum/scripts/momentum-tools.py practice-ledger consume --entity-id iq-20260516154102-d032731e --actor developer --source triage --outcome-ref "superseded:DEC-020"
python3 skills/momentum/scripts/momentum-tools.py practice-ledger consume --entity-id iq-20260516154102-f89de525 --actor developer --source triage --outcome-ref "superseded:DEC-020,DEC-025"
python3 skills/momentum/scripts/momentum-tools.py practice-ledger consume --entity-id iq-20260516154102-221bdb70 --actor developer --source triage --outcome-ref "superseded:DEC-023"
python3 skills/momentum/scripts/momentum-tools.py practice-ledger consume --entity-id iq-20260516154102-f098660a --actor developer --source triage --outcome-ref "superseded:DEC-026"
python3 skills/momentum/scripts/momentum-tools.py practice-ledger consume --entity-id iq-20260518032341-976884b5 --actor developer --source triage --outcome-ref "superseded:DEC-029"

# Test/leftover entries (4)
python3 skills/momentum/scripts/momentum-tools.py practice-ledger consume --entity-id iq-20260416054851-aec14053 --actor developer --source triage --outcome-ref "test-leftover"
python3 skills/momentum/scripts/momentum-tools.py practice-ledger consume --entity-id iq-20260416055625-ab0b3dc4 --actor developer --source triage --outcome-ref "test-leftover"
python3 skills/momentum/scripts/momentum-tools.py practice-ledger consume --entity-id iq-20260416055626-153bbdd3 --actor developer --source triage --outcome-ref "test-leftover"
python3 skills/momentum/scripts/momentum-tools.py practice-ledger consume --entity-id iq-20260416055624-9f5c9655 --actor developer --source triage --outcome-ref "test-leftover"
```

All 12 returned `"success": true`. No errors.

#### Post-cleanup state

```
$ python3 skills/momentum/scripts/momentum-tools.py practice-ledger open
{"action":"practice_ledger_open","success":true,"entities":[],"count":0}

$ python3 skills/momentum/scripts/momentum-tools.py practice-ledger summary
{"action":"practice_ledger_summary","success":true,"new_entries":12,"archive_entries":88,"by_event_type":{"consumed":12},"by_source":{"triage":12},"age_buckets":{"lt_7d":12,"d7_30":0,"gt_30d":0,"near_auto_close":0}}
```

Post-consumed count (new-schema): 12
Delta confirmation: 12 new `consumed` events appended (pre_new_entries=0 -> post_new_entries=12, delta=12). The 12 entity_ids are exactly the table from the story Description.

No direct edits to `.momentum/practice-ledger.jsonl` or `.momentum/practice-ledger-pre-2026-05.jsonl` — all writes via CLI.

#### Event chain verification

For entity `iq-20260516154102-d032731e` (documenter-agent-definition — superseded by DEC-020):

```
$ python3 skills/momentum/scripts/momentum-tools.py practice-ledger history --entity iq-20260516154102-d032731e
{
  "action": "practice_ledger_history",
  "success": true,
  "entity_id": "iq-20260516154102-d032731e",
  "events": [
    {
      "event_id": "pl-20260529T053901156135-fa90125e",
      "entity_id": "iq-20260516154102-d032731e",
      "ts": "2026-05-29T05:39:01Z",
      "event_type": "consumed",
      "source": "triage",
      "actor": "developer",
      "payload": {
        "outcome_ref": "superseded:DEC-020"
      }
    }
  ],
  "count": 1
}
```

**AC 8 partial pass:** History returns 1 event (the new `consumed` event), not 2. The original archive entry (from `practice-ledger-pre-2026-05.jsonl`) does not appear in history because A1's `_load_duckdb_events` excludes archive-file entries from new-schema event processing. The consumed event is correctly appended and the `entity_id` chain is intact for future migration. See Completion Notes for upstream-fix recommendation.

### File List

- `.momentum/practice-ledger.jsonl` — 12 `consumed` events appended (one per stale entity)
- `.momentum/stories/a2-practice-ledger-hygiene-cleanup-close-12-stale-entries.md` — Dev Agent Record populated
- `scripts/practice-ledger-hygiene-2026-05-26.sh` — one-shot dated script for auditability
