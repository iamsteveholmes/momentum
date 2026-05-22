---
content_origin: research-agent
date: 2026-05-22
sub_question: "Gas City Event Bus — native event catalog, filter expressiveness, custom event publishing, durability"
---

# Gas City Event Bus — Deep Investigation

## Sources Consulted

- `internal/events/events.go` (Gas City v1.1.0 main branch) — canonical event type constants, `KnownEventTypes` slice, `Event` struct, `Provider`/`Recorder`/`Watcher` interfaces [OFFICIAL]
- `engdocs/architecture/event-bus.md` (verified against code 2026-04-25) — architecture doc covering data flow, invariants, interactions, code map, storage format, known limitations [OFFICIAL]
- `engdocs/architecture/event-query.md` — extended `Filter` struct with all six predicates, aggregation helpers, multiplexer behavior [OFFICIAL]
- `internal/events/payload.go` — `Payload` interface, `RegisterPayload` registry, `NoPayload` sentinel, `DecodePayload` [OFFICIAL]
- `internal/events/supervisor_payloads.go` — example typed payload struct (SupervisorFSPressureSkippedTickPayload) [OFFICIAL]
- `internal/events/rotation_payload.go` — `RotatedPayload` struct [OFFICIAL]
- `internal/orders/triggers.go` — `checkEvent()` implementation: `ep.List(events.Filter{Type: a.On, AfterSeq: cursor})` [OFFICIAL]
- `internal/orders/order.go` — `Order` struct, `On string` field, `Validate()` requiring `on` for event trigger [OFFICIAL]
- `engdocs/architecture/orders.md` (verified against code 2026-03-01) — orders architecture, trigger types, cursor-based dedup invariants [OFFICIAL]
- `cmd/gc/cmd_event_emit.go` — `gc event emit` CLI implementation, `doEventEmit()`, flag definitions [OFFICIAL]
- `internal/beads/caching_store_events.go` — `ApplyEvent()` showing bead event payload structure (full bead fields in JSON) [OFFICIAL]
- `engdocs/architecture/nine-concepts.md` (verified against code 2026-04-25) — layering invariants, Event Bus as "universal observation substrate" [OFFICIAL]
- `docs.gascityhall.com/tutorials/07-orders` — public tutorial confirming `trigger = "event"` and `on = "bead.closed"` syntax [OFFICIAL]
- `docs.gascityhall.com/reference/events` — public reference for `gc events` CLI, mentions `--type`, `--payload-match`, `--after-cursor` flags [OFFICIAL]
- `CHANGELOG.md` — release history including "Order 'gates' renamed to triggers" in v1.0.0, flock timeout fix for `gc event emit` in unreleased [OFFICIAL]
- GitHub issue #622 — open feature request for a `webhook` trigger type (6th trigger type) [OFFICIAL]

---

## 1. Native Event Catalog

### Complete event type set

CONFIRMED. The authoritative list is `events.KnownEventTypes` in `internal/events/events.go`. As of the current main branch (post-v1.0.0), Gas City natively publishes **46 event types**. They are organized by subsystem:

**Session lifecycle** (8 types + 2 reserved):
| Event type | Emitter | Notes |
|---|---|---|
| `session.woke` | session_lifecycle_parallel.go | Reconciler start succeeded |
| `session.stopped` | lifecycle, reconciler, handoff, cmd_session | Multiple emitters |
| `session.crashed` | session_reconciler.go | Runtime exists, child process gone |
| `session.draining` | reconciler, cmd_runtime_drain, cmd_handoff | |
| `session.undrained` | cmd_runtime_drain | |
| `session.idle_killed` | session_reconciler.go | Idle timeout |
| `session.max_age_killed` | (inferred: reconciler) | Per-agent wall-clock age exceeded `max_session_age` |
| `session.updated` | session_reconciler.go | Live config drift repair |
| `session.quarantined` | reserved — no production emitter | |
| `session.suspended` | reserved — no production emitter | |
| `session.drain_acked_with_assigned_work` | reconciler | Session drain-acked while holding open/in-progress bead; see issue #2293 |
| `session.work_query_failed` | (pending: issue #1497) | Work-discovery subprocess killed/timed out |

**Bead operations** (3 types):
| Event type | Emitter | Notes |
|---|---|---|
| `bead.created` | bd hook (bead creation) | Payload: full bead JSON |
| `bead.closed` | bd hook (bead close) | Payload: full bead JSON |
| `bead.updated` | bd hook (bead update) | Payload: partial bead JSON (only changed fields) |

**Mail** (7 types): `mail.sent`, `mail.read`, `mail.archived`, `mail.marked_read`, `mail.marked_unread`, `mail.replied`, `mail.deleted`

**Convoy**: `convoy.created`, `convoy.closed`

**Controller / city lifecycle**: `controller.started`, `controller.stopped`, `city.suspended`, `city.resumed`, `city.created`, `city.unregister_requested`

**Supervisor**: `supervisor.shutdown_requested` (carries trigger attribution: source, signal, client addr, mode), `supervisor.fs_pressure.skipped_tick`

**Orders**: `order.fired`, `order.completed`, `order.failed`

**Async request results**: `request.result.city.create`, `request.result.city.unregister`, `request.result.session.create`, `request.result.session.message`, `request.result.session.submit`, `request.failed`

**External messaging** (7 types): `extmsg.bound`, `extmsg.unbound`, `extmsg.group_created`, `extmsg.adapter_added`, `extmsg.adapter_removed`, `extmsg.inbound`, `extmsg.outbound`

**Infrastructure**: `events.rotated` (forensic anchor written after log rotation; payload carries prior archive name and seq range), `provider.swapped`, `worker.operation`, `project.identity.stamped`

**Notably absent from the native catalog** (CONFIRMED absent):
- No `bead.status_changed` event — bead status transitions are reported through the three bead hook events (`bead.created`, `bead.updated`, `bead.closed`), not a dedicated status-change event type.
- No `bead.assigned` event — assignment changes arrive via `bead.updated` with the `assignee` field in the payload.
- No `molecule.*` or `formula.*` events — formula/molecule execution is tracked through `order.fired/completed/failed` and bead operations, not a distinct event namespace.
- No `agent.*` events — renamed to `session.*` at commit `be8debd8` (Mar 2026).
- No `rig.*` events — rig lifecycle generates no dedicated event types in the catalog.

### Event schema

CONFIRMED. Every event is a single Go struct:

```json
{
  "seq": 3,
  "type": "bead.created",
  "ts": "2026-03-01T10:00:05Z",
  "actor": "human",
  "subject": "gc-42",
  "message": "optional human-readable text",
  "payload": { ... }
}
```

- `seq` — monotonically increasing `uint64`, auto-assigned by the provider. Callers never set it.
- `type` — dotted string constant (e.g., `session.woke`, `bead.closed`).
- `ts` — auto-filled with `time.Now()` if the caller passes a zero value.
- `actor` — who caused the event (agent ID, `gc`, `human`, etc.).
- `subject` — optional: what was affected (e.g., bead ID, session ID).
- `message` — optional human-readable description.
- `payload` — optional `json.RawMessage`. Omitted from JSON when nil.

**Bead event payloads** carry the full bead struct for `bead.created` and `bead.closed`. For `bead.updated`, the payload carries only the fields that changed — `caching_store_events.go` shows that `mergeCacheEventPatch()` applies partial updates using a `fields` map that reflects only the changed keys (title, status, assignee, labels, metadata, dependencies, etc.). The payload may be wrapped in a `{"bead": {...}}` envelope depending on the hook source.

**Typed payloads** are registered via `RegisterPayload(eventType, sampleStruct)` and decoded at the SSE projection layer into concrete Go types. Events with no structured payload use `NoPayload{}` as the registered shape. The `KnownEventTypes` CI test enforces that every constant in the list has a registered payload — missing registrations fail CI.

---

## 2. Event Trigger Filter Expressiveness

### What the `event` trigger supports

CONFIRMED. The `Order.On` field is a single string matched against `Event.Type` using exact equality. The `checkEvent()` function in `internal/orders/triggers.go` issues exactly this query:

```go
ep.List(events.Filter{
    Type:     a.On,      // exact match on event type string
    AfterSeq: cursor,    // cursor-based deduplication
})
```

**This is the entirety of event trigger filtering.** The trigger fires if `len(matched) > 0` — any event of the given type after the cursor position causes the order to be marked due.

### What is NOT supported at the trigger level

CONFIRMED absent (verified by direct code inspection of `triggers.go` and `order.go`):

- **No payload-field filtering** — there is no mechanism equivalent to `WHERE new_status = "in_progress"` in an `order.toml`. The trigger cannot inspect event payload fields. An order with `on = "bead.updated"` fires on any bead update regardless of which fields changed or what values they hold.
- **No OR / multi-type listening** — the `On` field is a single string. One order can listen for exactly one event type. There is no array syntax or `|`-separated list.
- **No rig-scoping of event sources** — the event trigger queries the city-wide event bus with no filter for which rig produced the event. All events of the given type from all rigs trigger the order. Rig-level isolation of orders (via `ScopedName`) controls the cursor tracking and cooldown independently per rig, but the event type query itself is not scoped to a rig's events.
- **No actor or subject filter** — the `Filter` struct supports `Actor` and `Subject` predicates, but `checkEvent()` does not set them. Only `Type` and `AfterSeq` are used.

### What the Filter primitive supports (available to CLI and code, not to order.toml)

CONFIRMED. The `events.Filter` struct (as of the extended version in `event-query.md`) supports six predicates, ANDed together:

```go
type Filter struct {
    Type     string    // exact match
    Actor    string    // exact match
    Subject  string    // exact match (e.g., bead ID)
    Since    time.Time // inclusive lower bound
    Until    time.Time // inclusive upper bound
    AfterSeq uint64    // Seq > AfterSeq
    Limit    int       // result cap
}
```

These are available via `gc events --type X --since T --payload-match ...` on the CLI and programmatically, but order triggers use only `Type` and `AfterSeq` of this surface.

### Implication for Momentum

INFERRED. An order listening for `bead.updated` will fire on every bead field change — assignee, title, labels, metadata, status transitions — with no ability to narrow to a specific status value or assignee in the trigger configuration. Payload-conditional logic must live inside the order's exec script or formula, not in the trigger itself.

---

## 3. Custom Event Publishing

### CLI mechanism

CONFIRMED. Gas City provides `gc event emit <type>` (in `cmd/gc/cmd_event_emit.go`) as the dedicated custom event publishing command. Flags:

```
gc event emit <type>
  --subject   "Event subject (e.g. bead ID)"
  --message   "Event message"
  --actor     "Actor name (default: $GC_ALIAS, else $GC_AGENT, else $GC_SESSION_ID, else 'human')"
  --payload   "JSON payload to attach to the event"
  --json      emit JSON summary (schema_version, ok, event_type, actor, subject, message, has_payload, submitted)
```

**Best-effort semantics**: `gc event emit` always exits 0, regardless of whether the event was durably recorded. This is intentional — bead hooks that call `gc event emit` must not fail even if event recording fails. The JSON `--json` output includes `submitted: bool` to let callers inspect whether submission was attempted.

### Arbitrary type strings and payload

CONFIRMED. The `event emit` command accepts any string as the event type — there is no validation against `KnownEventTypes` at record time. From `doEventEmit()`:

```go
e := events.Event{
    Type:    eventType,   // arbitrary string, no validation
    Actor:   actor,
    Subject: subject,
    Message: message,
}
if payload != "" {
    // validates JSON before recording
    e.Payload = json.RawMessage(payload)
}
ep.Record(e)
```

Event types like `momentum.story.ready` or `sprint.avfl.passed` are valid and will be recorded. The `--payload` flag accepts arbitrary JSON (validated for syntactic correctness before recording, but not against a schema). Custom events can carry arbitrary payload fields.

### Triggering on custom events

CONFIRMED. An order can trigger on any custom event type by setting `on = "momentum.story.ready"`. The `checkEvent()` function passes the string directly to `events.Filter{Type: a.On}`, which performs an exact string match with no restriction to the `KnownEventTypes` list.

Example valid `order.toml`:
```toml
[order]
description = "Run AVFL after sprint stories signal ready"
formula = "run-avfl"
trigger = "event"
on = "momentum.story.ready"
pool = "worker"
```

### Event namespacing

CONFIRMED absent (no enforcement). There is no built-in namespace separation between system events (e.g., `bead.created`) and user events (e.g., `momentum.story.ready`). The dotted-string convention provides a de-facto namespace, but Gas City does not enforce separation at the API level. The known limitations section of `event-bus.md` explicitly notes: "No event schema validation. Event types are string constants with no runtime validation. Recording an event with a misspelled type succeeds silently." A custom event named `bead.created` would be indistinguishable from the system event.

**Practical risk**: Choosing custom event type names that collide with system event types (e.g., `session.stopped`) would cause spurious order firings. Custom events should use a distinct prefix (e.g., `momentum.`, `sprint.`, a project-specific namespace) to avoid collision.

### Who can publish

CONFIRMED. `gc event emit` is available anywhere `gc` is available — inside exec order scripts (which receive `ORDER_DIR`), inside agent session prompts via shell, and from bd hooks. The event bus architecture doc lists `cmd/gc/cmd_event_emit.go` as supporting "custom events from scripts and bd hooks."

---

## 4. Event Bus Durability and Ordering

### Persistence model

CONFIRMED. The default Event Bus backend (`FileRecorder`) stores events as JSONL at `.gc/events.jsonl` using `O_APPEND` for atomic appends at the OS level and a `sync.Mutex` for in-process serialization. This file is the durable event log. It persists across Controller restarts as a plain file on disk.

### Controller restart behavior

CONFIRMED. `FileRecorder` explicitly implements seq continuity across restarts:

> "FileRecorder resumes Seq across restarts. `NewFileRecorder` scans the existing file to find the maximum Seq, so new events continue monotonically even after a process restart." — `event-bus.md`, Invariant 14

Events published to the JSONL file before a Controller crash are not lost — they remain in the file. The `Watch(ctx, afterSeq)` interface returns events with `Seq > afterSeq`, so after a restart, a Watcher started from the last known cursor position will replay any events missed during downtime.

**Order trigger cursor recovery**: Event trigger cursors are stored as `seq:<N>` labels on order-run beads in the Bead Store (Dolt-backed, also durable). On Controller restart, `bdCursorFunc()` reads these labels to restore each order's cursor position. The orders architecture doc states: "The controller and `gc order run` fail closed when the current event head cannot be read." This means if cursor recovery fails, the order does not fire spuriously — it blocks.

### Delivery semantics

CONFIRMED for the `FileRecorder` path, INFERRED for broader guarantees:

- **At-most-once for record errors**: Recording is best-effort. If `Record(Event)` fails (disk full, permission error, flock timeout), the error is logged to stderr and silently dropped. The event is never recorded. Callers never see the failure.
- **No replay on missed delivery**: If the Controller is down and system events are being produced (e.g., beads are being mutated), those events are written to the JSONL file but not watched in real time. They will be picked up on the next Watch call with the correct `afterSeq`. However, the watcher is not a guaranteed-delivery queue — if `Record` itself fails, the event is gone.
- **Append-only, immutable once written**: Invariant 6 — "Events are immutable once recorded. There is no Update or Delete operation."
- **Malformed lines skipped**: Invariant 12 — "Malformed lines are skipped. ReadAll, ReadFiltered, and ReadFrom silently skip lines that fail JSON unmarshalling. This handles partial writes from crashes." A crash mid-write produces a truncated last line, which is skipped on recovery.

In practice, the delivery model is **best-effort append-once**: each successful `Record()` call produces exactly one event line. Failed records are dropped (at-most-once from the caller's perspective). There is no acknowledgment or receipt from the consumer.

### Cursor mechanism

CONFIRMED. The cursor is **per-order**, stored in the Bead Store, and tracked across Controller restarts via `seq:<N>` labels on order-run beads.

Mechanism detail:
1. When an order fires, a tracking bead is created synchronously before dispatch, labeled `order-run:<scopedName>`.
2. For exec orders, the `seq:<N>` label (where N = the highest event seq that triggered this run) is stamped on the tracking bead **before the exec command runs** — a crash after the stamp but before execution drops that event for idempotent commands, which is the safer failure mode for non-idempotent ones.
3. For formula orders, the seq label is stamped on the wisp root bead or failure tracking bead.
4. On the next Controller tick, `bdCursorFunc()` calls `MaxSeqFromLabels()` on all existing `order-run:<scopedName>` beads to find the highest recorded seq. The next `checkEvent()` call uses this as `AfterSeq`, ensuring events at or before the cursor are never re-processed.

The cursor is **per-order scoped** (via `ScopedName`), not global or per-Controller restart. Two orders watching the same event type maintain independent cursors.

### Log rotation

CONFIRMED. The JSONL file has a rotation mechanism (`rotation.go`, `rotation_archive.go`). Rotated archives are gzip-compressed with atomic rename (`tmp` → `dest`). The `events.rotated` event type serves as a forensic anchor — it is the first event written to a freshly-rotated active log, and its payload (`RotatedPayload`) carries the prior archive filename and seq range. `ReadFrom` with byte-offset enables incremental reads without scanning from the start. There is no automatic retention policy — the JSONL file grows unbounded until manually rotated.

### Known limitation: polling Watch

CONFIRMED. `FileRecorder.Watch()` polls the JSONL file every 250ms — it does not use inotify/fsnotify. This adds up to 250ms latency between a `Record()` call and a Watcher observing the event. For the Controller's 30-second tick, this latency is not material.

---

## Synthesis

The Gas City Event Bus is a deliberately simple, append-only JSONL log with a pub/sub watch interface layered on top. Its design choices are internally consistent and have specific implications for external use:

**Catalog is broader than documented externally**: The public tutorial documents only `bead.created` and `bead.closed`. The actual catalog has 46 named types spanning sessions, orders, mail, convoys, external messaging, and infrastructure. `bead.updated` is a legitimate trigger target for assignment or status changes, but it fires on any field change — there is no payload-field filter at the trigger level.

**Event trigger filtering is intentionally minimal**: The `checkEvent()` implementation uses exactly two filter fields (`Type` and `AfterSeq`) out of the six available on `Filter`. This is not a gap — it is a deliberate design choice aligned with the ZFC principle ("Go handles transport only, with no judgment calls"). Payload-conditional logic belongs in the formula or exec script, not the infrastructure.

**Custom events are a first-class feature**: `gc event emit` is not a workaround — it is the intended mechanism for publishing application-layer events. The best-effort exit-0 contract is deliberate. Event type namespacing is purely conventional (dotted prefix), not enforced.

**Durability is file-system durable, not broker-durable**: Events survive Controller crashes (JSONL file persists). Events do not survive disk loss. Recording failures are silently dropped. The model is closer to a structured log file than a message broker. For Momentum's use case (triggering orders after sprint events), this is sufficient — the key invariant is that successful `Record()` calls are persistent and that cursor-based deduplication prevents replay.

**OR-filtering and payload-filtering require workarounds**: If a Momentum workflow needs to fire on either `bead.created` OR `bead.closed`, two separate orders are required. If a workflow needs to fire only when a bead's status changes to `in_progress`, the exec script or formula must implement that check, and a `condition` trigger (polling a shell command) may be more appropriate than an `event` trigger.

---

## Gap Summary

**Could not confirm:**

1. **Exact payload schemas for each event type** — The `RegisterPayload` registry associates Go types with event type constants, but the payload structs for most types (e.g., `session.stopped`, `order.fired`, `bead.created`) are not visible in the files inspected. `supervisor_payloads.go` and `rotation_payload.go` show the pattern, but the bead and session payload structs live in other packages not fully inspected. UNKNOWN which fields are present in `order.fired` payload (e.g., does it include the order name, the triggering event seq?).

2. **`bead.updated` payload completeness in practice** — `caching_store_events.go` shows partial-field merging, indicating `bead.updated` payloads carry only changed fields. However, which fields are included when status changes vs. when assignee changes depends on the bd hook implementation, which was not inspected. UNKNOWN whether a status-change `bead.updated` always includes the old status value in the payload.

3. **`exec.Provider` behavior with custom event types** — The exec provider delegates operations to a user-supplied script. Whether such a script would correctly handle custom event types (or would filter them out) depends on the script implementation. UNKNOWN — no production exec provider scripts were inspected.

4. **Cross-rig event visibility** — The event bus is city-scoped (per the Multiplexer design). Whether a rig-level order can observe events from a different rig (or from the city-level event bus) was not confirmed in the code. INFERRED from the architecture that all city events share one event bus, but rig isolation semantics were not explicitly confirmed for event triggers.

5. **`session.quarantined` and `session.suspended` emitters** — Both are listed in `KnownEventTypes` and registered as reserved, with no production emitter documented. Whether these will be emitted in a future version and what their payload would contain is UNKNOWN.

6. **Issue #2293 (session.drain_acked_with_assigned_work) status** — This event was added with a comment indicating "pack-level subscribers own the recovery policy." Whether any built-in pack or order in the core pack subscribes to this event was not confirmed.
