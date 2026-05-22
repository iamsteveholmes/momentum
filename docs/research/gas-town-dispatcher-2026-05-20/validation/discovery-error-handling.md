---
content_origin: research-agent
date: 2026-05-22
sub_question: "Gas City error handling — exec order failures, formula failures, Controller surfacing, retry config, barrier failure detection"
---

# Gas City Error Handling — Discovery Report

## Research Question

For a 3-loop automated sprint pipeline running on Gas City v1.1.0 (Loop 1:
per-story parallel sprint-dev + code review + QA; Loop 2: corpus AVFL; Loop
3: E2E), what happens at every failure mode? Specifically: exec order failure
behavior, formula order failure behavior, controller surfacing without the Gas
Town pack, retry and circuit breaker configuration, and barrier/condition
failure detection.

## Sources Consulted

- `engdocs/architecture/orders.md` (gastownhall/gascity, v1.1.0) — authoritative orders
  architecture doc, last verified 2026-03-01. [OFFICIAL]
- `engdocs/architecture/controller.md` (gastownhall/gascity, v1.1.0) — controller
  architecture doc, last verified 2026-04-25. [OFFICIAL]
- `engdocs/architecture/health-patrol.md` (gastownhall/gascity, v1.1.0) — health patrol
  subsystem doc, last verified 2026-04-25. [OFFICIAL]
- `engdocs/architecture/formulas.md` (gastownhall/gascity, v1.1.0) — formulas and
  molecules architecture, last verified 2026-03-17. [OFFICIAL]
- `engdocs/architecture/life-of-a-molecule.md` (gastownhall/gascity, v1.1.0) — molecule
  lifecycle phases. [OFFICIAL]
- `engdocs/architecture/event-bus.md` (gastownhall/gascity, v1.1.0) — event bus
  architecture. [OFFICIAL]
- `docs/reference/config.md` (gastownhall/gascity, v1.1.0) — auto-generated schema
  reference for city.toml. [OFFICIAL]
- `docs/reference/cli.md` (gastownhall/gascity, v1.1.0) — auto-generated CLI
  reference. [OFFICIAL]
- `docs/reference/formula.md` (gastownhall/gascity, v1.1.0) — formula file format
  reference. [OFFICIAL]
- `docs/tutorials/07-orders.md` (gastownhall/gascity, v1.1.0) — orders tutorial. [OFFICIAL]
- v1.1.0 release notes (GitHub releases API) — "session lifecycle recovery,"
  "resilience" themes. [OFFICIAL]
- GitHub issues feed (gastownhall/gascity, open+closed) — active bug and known
  limitation signal. [OFFICIAL]

---

## Area 1: Exec Order Failure Behavior

### What happens on non-zero exit

When an exec order's shell script exits non-zero, the controller:

1. Labels the tracking bead `exec-failed` (vs `exec` for success).
2. Emits an `order.failed` event to the JSONL event bus at `.gc/events.jsonl`.
3. Does **not** retry. The architecture doc states explicitly: "Failed orders
   emit `order.failed` events but do not retry; the tracking bead prevents
   re-fire within the same cooldown window." [OFFICIAL]

The tracking bead (labeled `order-run:<scopedName>`) is created **before** the
dispatch goroutine launches. Its presence blocks the cooldown trigger from
re-firing on the next tick. The failed order therefore sits out a full cooldown
cycle before it can fire again — it is not immediately retried. [OFFICIAL]

There is no automatic escalation to a human. No alert, no mail, no upstream
notification. The failure is recorded as an event; a human must query it
actively. [OFFICIAL, with gap implication noted below]

### stdout/stderr capture and queryability

The `ExecRunner` type signature is `func(ctx, command, dir string, env []string) ([]byte, error)`.
The `[]byte` return is stdout/stderr captured from the subprocess. The
architecture doc states that `dispatchExec()` runs the shell command via
`ExecRunner` and labels the tracking bead with `exec` or `exec-failed`.
However, the doc does not state that the captured output is written into
the tracking bead's body or metadata. [OFFICIAL source for capture;
UNKNOWN whether captured output is surfaced in `gc order history` output]

The `gc order history` command queries tracking beads by label and shows
bead ID and execution timestamp. Whether it also surfaces exit code or
stderr output is not documented in the available CLI reference. [UNKNOWN]

### Timeout behavior (300s default for exec orders)

The tutorial doc clarifies the exec order default: "Default timeouts differ:
30 seconds for formula orders, **300 seconds for exec orders**." (Note: the
architecture doc says "Default timeout: 60 seconds" for exec orders — this
is a discrepancy between the two docs.) [OFFICIAL, with internal discrepancy
flagged]

When a timeout fires, the dispatch goroutine context is cancelled. The
tutorial states: "if the script is still running when time is up, the process
is killed." The tracking bead outcome in timeout cases follows the same
`exec-failed` path as non-zero exit. The same no-retry rule applies. [OFFICIAL]

Per-order timeout is configurable via `timeout = "90s"` in `order.toml`. A
global `max_timeout` cap in `city.toml` overrides any per-order value that
exceeds it. The effective timeout is `min(per-order timeout, max_timeout)`.
[OFFICIAL]

### Retry and backoff configuration

There is **no retry count, backoff, or retry configuration for exec orders
in Gas City v1.1.0.** The Known Limitations section of the orders
architecture doc explicitly lists: "No retry on dispatch failure: Failed orders
emit events but are not retried." [OFFICIAL]

The only "retry" mechanism is the natural re-fire when the trigger next
opens — which for a cooldown trigger means waiting for the full interval to
elapse after the failed tracking bead was created. For a condition trigger,
the order fires again the next tick that the condition command exits 0. [OFFICIAL]

---

## Area 2: Formula Order Failure Behavior

### What "failure" means for a formula order

Formula order dispatch is fundamentally different from exec order dispatch.
The formula order's timeout (default 30 seconds) covers only the **dispatch
phase**: calling `MolCook`, creating the wisp root bead, and routing it to
the pool via label. Once the wisp is created and the pool label is stamped,
the dispatch is considered complete from the order's perspective. [OFFICIAL]

The tutorial states this explicitly: "For formula orders, the timeout covers
the initial dispatch — compiling the formula, creating the wisp, and routing
it to the pool. Once the wisp is created and handed off, the agent works on
it at its own pace; the timeout doesn't kill an agent mid-work." [OFFICIAL]

This means:

- An `order.failed` event for a formula order indicates the wisp could not
  be created (e.g., MolCook failed, formula not found, store error) — not
  that the agent failed to complete the work. [OFFICIAL]
- If the agent crashes mid-formula, or never picks up the work, or the step
  work fails — that is **not** surfaced as an `order.failed` event. The wisp
  remains open (or partially open) in the bead store. [CONFIRMED]

### When an agent session crashes mid-molecule

If an agent session dies while working on a formula step, the GUPP (Get Up,
Pick Up) pattern applies. The health patrol's "let it crash" model means:

- The controller detects the dead session within one patrol tick (default 30s).
- It restarts the session (subject to crash loop quarantine limits).
- On restart, `gc hook` follows the three-tier work_query: first, it checks
  for `in_progress` work assigned to that session or alias (crash recovery
  tier). If the molecule step bead is still assigned and `in_progress`, the
  restarted session picks it up and continues. [OFFICIAL — controller.md and
  health-patrol.md]

Whether the molecule step was checkpointed before the crash determines
whether the agent re-does work. Gas City does not provide a built-in
checkpoint mechanism; idempotency is the agent's responsibility. [INFERRED
from "let it crash" + GUPP model; CONFIRMED by absence of checkpoint docs]

### Automatic session restart — is it configurable?

Session restart after crash is automatic and on by default. It is bounded
by the crash loop quarantine:

- `max_restarts = 5` (default) within `restart_window = "1h"` (default)
- After 5 restarts within 1 hour, the agent is quarantined and the controller
  stops attempting to restart it until the window expires. [OFFICIAL — config.md
  DaemonConfig schema]
- The named-session respawn circuit breaker (`session_circuit_breaker = true`
  in `[daemon]`) adds an additional layer: it suppresses no-progress
  named-session respawns after the configured threshold, with configurable
  `session_circuit_breaker_max_restarts`, `session_circuit_breaker_window`,
  and `session_circuit_breaker_reset_after`. This was added in v1.1.0 as part
  of the "session lifecycle recovery" hardening. [OFFICIAL]

### When the agent pool is exhausted

There is no "pool exhausted" error returned to the caller at formula dispatch
time. The formula order dispatch creates the wisp, labels it
`pool:<qualifiedPool>`, and returns success. The work sits in the bead store
labeled for the pool. The controller's reconciler sees labeled demand on the
next tick and scales up pool sessions (subject to `max_active_sessions` caps).
[OFFICIAL — dispatch.md, config.md Agent schema]

If the pool cap prevents new sessions, new work simply queues in the bead
store. There is no blocking, no failure, no dead-letter fallback — it is
a passive queue backed by the bead store. [CONFIRMED from dispatch.md's
scale_check / work_query correspondence section; INFERRED for cap-bounded
non-start behavior]

Formula orders with open (non-closed) work already in flight are **skipped**
on the next trigger evaluation: "Before dispatching, the controller checks
whether the order already has open (non-closed) work. If it does, the order
is skipped even if the trigger says it's due." [OFFICIAL — tutorial 07-orders]

### Formula step retry (check field)

At the step level within a formula (distinct from order-level retry), the
`check` field on a `[[steps]]` entry provides runtime retry: `max_attempts`
with a `check` script after each attempt. The `mol-review-quorum` formula
uses `on_exhausted = "soft_fail"` on reviewer lanes so synthesis can continue
with degraded coverage when one lane exhausts its retry budget. [OFFICIAL]

This is step-level retry within a single formula execution, not order-level
retry of the entire dispatch. It is managed by the `bd` beads backend and
is not the same as re-dispatching a failed formula order. [OFFICIAL]

---

## Area 3: Controller-Level Error Handling Without the Gas Town Pack

### How the Controller surfaces pipeline failures to humans

In the Orders-only model (no Mayor/Deacon/Witness), the Controller surfaces
failures through:

1. **`gc order history`** — queries tracking beads labeled `order-run:<name>`,
   shows executed timestamp and bead ID. A bead labeled `exec-failed` vs `exec`
   distinguishes failed from succeeded exec orders. [OFFICIAL]

2. **`gc events`** — reads `.gc/events.jsonl`. Supports `--type order.failed`
   filtering, `--since` time filtering, and `--watch` streaming. The event bus
   records `order.fired`, `order.completed`, and `order.failed` for every
   dispatch. [OFFICIAL]

3. **`gc status`** — shows city-wide overview: controller state, suspension,
   all agents with running status, rigs, and a summary count. Does **not**
   directly surface order failures — it shows agent/session state, not order
   execution state. [OFFICIAL]

4. **`gc analyze reliability`** — correlates session-lifecycle events with
   model/version/rig. This is a post-hoc analysis tool, not a real-time
   failure alert. [OFFICIAL]

5. **`gc order check`** — evaluates trigger conditions for all orders and shows
   which are due. This is a point-in-time snapshot; it does not distinguish
   "never ran" from "ran and failed." [OFFICIAL]

There is **no proactive escalation, alert, or notification mechanism** in Gas
City's controller when an order fails without the Gas Town pack. The human
must actively query `gc events`, `gc order history`, or watch the event log.
[CONFIRMED — absence of alert/notify/escalate in all source docs reviewed]

### What `gc supervisor` watches

`gc supervisor` is the machine-wide supervisor process that manages all
registered cities. Its watch scope is **process-level**: it watches whether
the per-city controller runtime is alive, manages startup/shutdown of city
runtimes, and hosts the shared API server. It does **not** watch individual
order execution outcomes. [OFFICIAL — controller.md, cli.md gc supervisor
section]

`gc supervisor status` reports whether the supervisor process is running.
`gc supervisor logs` tails the supervisor log file. Neither command surfaces
order failure details. [OFFICIAL]

The supervisor's health scope is city runtimes, not order-level work items.

### Controller's own escalation mechanism

The controller has no escalation mechanism independent of the Gas Town
supervisor chain in v1.1.0. The event bus records failures; the human queries
them. The controller does apply crash loop quarantine for agent sessions
(`max_restarts = 5` within `restart_window = "1h"`), which is a form of
circuit breaking, but this applies to agent sessions, not to order dispatch
failures. [OFFICIAL]

### `gc status` does not show failed/stuck orders

`gc status` shows controller state and agent running status. It does not show
a list of failed orders, stuck orders, or orders that have exhausted retries.
That information lives in the event log and the tracking beads. [OFFICIAL]

---

## Area 4: Order-Level Retry and Circuit Breaker Configuration

### Max retries and retry backoff

**There is no retry, backoff, or circuit breaker configuration for orders in
Gas City v1.1.0.** The Known Limitations section of the orders architecture
doc is unambiguous: "No retry on dispatch failure." [OFFICIAL]

The config schema (`OrdersConfig`) offers:
- `skip` — exclude orders from scanning entirely
- `max_timeout` — hard cap on per-order timeout
- `overrides` — per-order overrides of trigger type, interval, schedule,
  check, on, pool, and timeout

None of these fields configure retry behavior, backoff, or a circuit breaker
for order-level failures. [OFFICIAL — config.md OrdersConfig and OrderOverride
schemas]

### Dead-letter queue

There is no dead-letter queue for orders that have exhausted retries. There
are no retries, and therefore no exhaustion concept at the order level. Failed
orders are recorded as `order.failed` events and left in the event log.
[CONFIRMED]

The `gc order sweep-tracking` command can close stale open tracking beads
manually (for maintenance/recovery purposes). It does not constitute a
dead-letter queue — it is an operator cleanup tool. [OFFICIAL]

### Can a failed order create a human gate?

There is no built-in mechanism for a failed order to automatically create a
human gate (a bead requiring human input or approval). The event trigger type
can be used in a secondary order that fires on `order.failed` events — which
would dispatch a formula to an agent that could then send mail or create a
human-gate bead. But this is a user-defined pattern, not a built-in feature.
[INFERRED — composable from event trigger + formula dispatch; no direct
documentation of this pattern]

---

## Area 5: The Barrier Failure Case

### How Gas City handles "barrier condition never becomes true"

The sprint pipeline's barrier case is: a condition-trigger order watching for
"all stories merged" that never becomes true because one story's Loop 1
failed. Understanding this requires examining the condition trigger.

A condition trigger runs `sh -c <check>` on each patrol tick (default every
30 seconds). If the command exits 0, the order fires. If it exits non-zero,
nothing happens — the order simply does not fire this tick. There is no state
accumulation, no aging, no timeout on how long a condition trigger can be
"active but never firing." [OFFICIAL — orders.md, tutorial 07-orders]

Specifically:

- There is **no maximum time a condition trigger can be "active but never
  firing" before escalating.** The condition trigger will wait indefinitely
  for the check script to exit 0. [CONFIRMED]
- There is **no watchdog** on condition triggers. The controller does not
  notice or alert that a condition trigger has been checking for 6 hours
  without firing. [CONFIRMED — absence of any watchdog mechanism in all
  docs reviewed]
- The condition trigger check runs **synchronously** during trigger evaluation.
  The architecture doc flags this as a known limitation: "Condition trigger
  blocks the dispatch loop: `checkCondition()` runs `sh -c <check>`
  synchronously during trigger evaluation. A slow check command blocks
  evaluation of subsequent orders on that tick." [OFFICIAL]
- The check has a **10-second timeout** (per the tutorial). [OFFICIAL]

### How the developer detects a stuck barrier

In the Orders-only model, the developer has no proactive notification. The
detection paths are:

1. **`gc order check`** — will perpetually show the barrier order as `no` with
   a reason like "condition check exited non-zero." The developer must poll
   this manually. [OFFICIAL]
2. **`gc events --type order.fired --watch`** — absence of `order.fired`
   events for the barrier order is the signal. Not a notification — requires
   active watching. [OFFICIAL]
3. **`gc order history`** — shows no new tracking beads for the barrier order.
   [OFFICIAL]

There is no timeout on how long a barrier can be unsatisfied before Gas City
escalates or kills it. The pipeline would wait indefinitely. [CONFIRMED]

### Relationship between story failure and barrier

In the sprint pipeline design, if a story's Loop 1 work (code review or QA)
fails and the worktree merge never happens, the condition trigger checking
"all stories merged" will never evaluate to true. Gas City has no internal
linkage between that story's failure and the barrier condition — the condition
script is whatever the operator writes. The operator must write the condition
script to handle partial failure (e.g., checking for a failure marker bead in
addition to merge completion). [INFERRED — from composition of condition
trigger behavior and absent linkage mechanism]

---

## Synthesis

### Cross-cutting conclusions

**1. The no-retry guarantee is load-bearing and must be designed around.**
Gas City's exec order dispatch is fire-once per trigger window: fail once,
wait for the next trigger opening. For the sprint pipeline's per-story orders
(Loop 1), this means a flaky CI check that fails the first time forces a full
cooldown wait before the order re-fires, and there is no automatic escalation.
The pipeline must encode retry logic inside the exec script itself (exit 0
after N internal attempts, or use a condition trigger that only fires when
truly ready rather than a cooldown trigger).

**2. Formula order dispatch and formula execution are decoupled in error space.**
An `order.completed` event for a formula order means the wisp was created, not
that the agent completed the work. The pipeline's Loop 2 and Loop 3 formula
orders will show "completed" dispatch even if the AVFL or E2E agent work later
fails. The pipeline's barrier logic (waiting for all work to succeed) cannot
rely on `order.failed` events for formula orders — it must check the bead
store state of the formula molecules directly.

**3. The event log is the only failure surface without the Gas Town pack.**
`gc events --type order.failed --watch` is the closest thing to a failure
alert. The pipeline's human gate design must include an explicit event-watch
or polling step; there is no passive push notification.

**4. The condition trigger has no built-in timeout or watchdog.**
A barrier implemented as a condition trigger will wait indefinitely if the
condition is never satisfied. The sprint pipeline must either (a) implement a
timeout in the condition script itself (e.g., check both the condition and a
deadline timestamp), or (b) run a companion monitoring order that fires on a
cron schedule and alerts if the barrier condition has been checked without
firing for longer than a defined window.

**5. Session circuit breaker (new in v1.1.0) is a meaningful resilience gain.**
The named-session respawn circuit breaker prevents restart loops from producing
noisy goroutine buildup (the P1 bug already known). It is opt-in via
`[daemon] session_circuit_breaker = true`. For a production sprint pipeline,
enabling this with a conservative `session_circuit_breaker_max_restarts` is
recommended. Without it, a wedged agent will be restarted up to `max_restarts`
(default 5) times before quarantine.

**6. Pool exhaustion is not an error — it is a passive queue.**
Formula orders dispatched to a capped pool will simply queue in the bead store.
The pipeline does not need to handle "pool full" as a failure case. It does
need to handle "work queued but never picked up" as an indefinite-wait case,
with the same watchdog gap noted above.

**7. gc status does not show failed orders.**
Any monitoring or loop-control logic that reads `gc status` to detect "did
all stories pass?" will not find the answer there. Order failure state lives
in the event log and tracking beads. The pipeline's barrier and monitoring
scripts must query `gc events` or `gc order history`, not `gc status`.

**8. Exec order stderr/stdout surfaceability is UNKNOWN.**
Whether the output of a failed exec script is queryable via `gc order history`
or stored in the tracking bead is not documented in any reviewed source. This
is a practical gap for debugging pipeline failures.

---

## Open Questions

1. **Does `gc order history` surface exec order exit codes and stderr?**
   The architecture doc confirms output is captured (`[]byte` return from
   ExecRunner) but does not state whether it is stored in the tracking bead.
   This directly affects how quickly failures can be debugged in a production
   pipeline.

2. **What is the actual exec order default timeout — 60 seconds (architecture
   doc) or 300 seconds (tutorial)?** The two official documents disagree. The
   architecture doc was last verified 2026-03-01; the tutorial may reflect a
   later change. This must be resolved before setting per-order timeouts.

3. **Is there an `order.failed` event for a formula order whose wisp was
   created but whose agent work later fails?** Based on the architecture, the
   answer is no — but confirming via `gc events` in a live test would validate
   this assumption before the pipeline relies on it.

4. **Can the `condition` trigger's 10-second check timeout be overridden?**
   The tutorial states the condition check has a 10-second timeout but the
   per-order `timeout` field description says it covers the condition trigger's
   check command. The exact scope needs clarification for slow barrier checks.

5. **What does `gc events --type order.failed` show — both exec and formula
   dispatch failures?** Based on the architecture, yes — but does the payload
   distinguish exec vs formula failures? This affects monitoring script design.

---

## Verdict

**Gas City's error handling is functional but operationally thin for a
production sprint pipeline without the Gas Town pack.**

The core mechanisms are sound: events are durably recorded, tracking beads
provide history, crash quarantine prevents restart storms, and the session
circuit breaker (v1.1.0) closes the goroutine-buildup P1. The underlying
reliability improved substantially in v1.1.0.

However, three gaps represent real operational risk for the 3-loop pipeline:

**Risk 1 (HIGH): No order-level retry.** A single exec order failure — whether
from a flaky CI check, transient network issue, or timing problem — forces a
full cooldown wait. The pipeline's Loop 1 exec orders must implement internal
retry logic. External retry via a separate retry-wrapper order is possible but
adds cooldown windows between attempts.

**Risk 2 (HIGH): No barrier timeout or watchdog.** A condition-trigger barrier
that is never satisfied waits indefinitely with no notification. Loop 1's
barrier (all stories merged) can stall silently if one story fails. The
pipeline must implement its own timeout logic inside condition scripts, or
run a separate monitoring order on a cron schedule.

**Risk 3 (MEDIUM): Formula dispatch success != formula work success.** `gc
events --type order.completed` for formula orders means the wisp was created,
not the work is done. Loop 2 (AVFL) and Loop 3 (E2E) formula orders require
the pipeline to check molecule bead state directly to determine pass/fail,
not the order event log.

These are not disqualifying — they are design constraints that require
compensating patterns in the pipeline's condition scripts and monitoring orders.
Gas City's composability (event triggers, condition triggers, manual orders,
`gc event emit`) makes all three compensating patterns buildable. But they must
be built explicitly. The platform does not provide them by default.
