---
content_origin: claude-code-subagent
date: 2026-05-18
sub_question: "What are Hermes worker lanes — definition, parallelism, lane assignment, and dependency/ordering semantics?"
topic: "Can Hermes run as a 24/7 dispatcher/delegate with Claude Code as planner/brains, and can Hermes Kanban + worker lanes map onto Momentum?"
---

# Hermes Worker Lanes — Definition, Parallelism, Assignment, and Ordering Semantics

## Scope and Method

This extends the prior-art discovery (`docs/research/hermes-kanban-discovery-2026-05-17.md`, §5 "Worker Lanes"), which established the lane *contract* (assignee string + spawn mechanism + lifecycle terminator) and the failure-handling envelope. It does **not** repeat that material. The focus here is the crux question for a Momentum mapping: **do lanes express a dependency DAG / ready-frontier, or are they simple independent parallel executors — and what bounds their concurrency?**

Sources: the three official Hermes docs pages (worker-lanes, kanban reference, kanban-tutorial), fetched 2026-05-18. The docs carry no published date; the prior discovery (2026-05-17) treated them as current. Treat behavioral specifics as "documented, not independently verified" — no source code or config schema was inspected. Tags: `[OFFICIAL]` = stated in Hermes docs; `[PRAC]` = practitioner/operational inference grounded in doc text; `[UNVERIFIED]` = the docs are silent or contradictory and the claim cannot be grounded. Untagged sentences are framing only.

## What a "Lane" Actually Is

A worker lane is **"a class of process that the kanban dispatcher can route tasks to"** `[OFFICIAL]`. It is not a queue, not a thread pool, not a scheduling slot, and not a column on the board. It is an *executor archetype* defined by exactly three things `[OFFICIAL]` (unchanged from prior art §5.1):

1. **An assignee string** — the routing key. The dispatcher matches `task.assignee` against a Hermes profile name (spawnable lane) or a registered non-spawnable id (plugin lane).
2. **A spawn mechanism** — for profile lanes, `_default_spawn` runs `hermes -p <assignee> chat -q <prompt>` in the task's pinned workspace with the `HERMES_KANBAN_*` env block.
3. **A lifecycle terminator** — every claim ends in `kanban_complete` (→done), `kanban_block` (→blocked), or a process exit without a tool call (→crashed) `[OFFICIAL]`.

The single most load-bearing sentence for the Momentum question is the explicit ownership statement: **lanes "execute but never own [lifecycle] truth — everything flows back through `kanban_*` tools"** `[OFFICIAL]`. A lane is a *dumb executor of one card at a time*. All dependency logic, ordering, promotion, and retry accounting live in the kanban kernel (the SQLite state machine + dispatcher loop), **not in the lane**. This is the decisive architectural fact: **lanes carry zero ordering semantics**. Any DAG behavior is a property of `task_links` + the dispatcher, executed *through* lanes that are themselves order-blind.

The word "lane" is overloaded across the docs and this distinction matters for Momentum:

- **Scheduling lane** (the worker-lanes page): an executor class keyed by assignee. Real coordination primitive.
- **Dashboard "Lanes by profile"** (kanban reference): a *UI-only* toggle that sub-groups the Running column by assignee — **"This is UI-only grouping, not a scheduling primitive"** `[OFFICIAL]`. It changes nothing about scheduling; toggling it off yields "a single flat list ordered by claim time" `[OFFICIAL]`.

These are not the same thing. A Momentum mapping must not conflate the dashboard's per-profile swimlanes with a scheduling construct — they are purely a viewing convenience.

## How Work Is Assigned to a Lane

Assignment is **by the `task.assignee` field, set at task-creation time** `[OFFICIAL]`. There is **no tag-based, type-based, or content-based auto-router in the kernel** `[OFFICIAL]`: "Tasks are assigned by manual assignee field only. The dispatcher matches `task.assignee` against either a Hermes profile name or a registered non-spawnable identifier." Story 1 and Story 2 both set assignee explicitly at `hermes kanban create` time (`--assignee backend-dev`, `--assignee translator`, etc.) `[OFFICIAL]`.

Two configured fallbacks soften the "manual only" rule, surfaced on the kanban reference page `[OFFICIAL]`:

- `default_assignee` (default `""`) — **"Where a child task lands when the LLM picks an unknown profile. Empty = fall back to active default."** This only fires inside auto-decomposition (below), not for human-created tasks.
- An unresolvable assignee is **not** silently dropped or run by a fallback lane: the task stays in `ready` and emits a `skipped_nonspawnable` event `[OFFICIAL]` (prior art §5.1; reconfirmed). Stranded-task detection (default 30 min, `kanban.stranded_threshold_seconds`) escalates it to a diagnostic.

Priority exists as a creation flag (`--priority N`, Story 1 uses `--priority 2`) but **the docs do not state whether the dispatcher honors priority when choosing which ready task to claim** `[UNVERIFIED]`. This is a real gap for any Momentum mapping that wants a priority-ordered ready frontier — it cannot be assumed from the docs.

### The one real auto-routing path: `auto_decompose`

This is new relative to the prior discovery and is the most important finding for the DAG question. The kanban reference page documents a decomposition subsystem `[OFFICIAL]`:

- `auto_decompose: true` (default) — **"Dispatcher auto-runs the decomposer on each tick, capped by `kanban.auto_decompose_per_tick` (default 3 tasks per tick)."**
- `orchestrator_profile: ""` — **"Profile that owns decomposition. Empty = fall back to active default profile."**
- The decomposer **"reads your rough idea, examines installed profiles, then ask[s] the LLM to produce a JSON task graph: which tasks to spawn, who they go to, and which depend on which"** `[OFFICIAL]`.

This is the actual mechanism by which a goal becomes a typed dependency graph: an LLM (the orchestrator profile) emits a JSON task graph — nodes (tasks), assignees (which lane each goes to), and edges (`depend on which`). The decomposer materializes that graph as `tasks` rows + `task_links` rows. **The DAG is authored by an LLM call, persisted as `task_links`, and then executed by order-blind lanes.** Lanes never see the graph; they only ever see one claimed card.

## Concurrency and What Bounds It — The Central Open Question

This is the area where the official docs are weakest, and it is exactly the area Momentum cares about most.

**What the dispatcher does per tick** `[OFFICIAL]`: "every N seconds (default 60): reclaims stale claims, reclaims crashed workers, promotes ready tasks, atomically claims, spawns assigned profiles." Config: `dispatch_interval_seconds: 60`, `dispatch_in_gateway: true` (defaults).

**What is NOT documented anywhere across all three pages** `[OFFICIAL — by explicit absence]`:

- No `max_parallel_workers`, `dispatch_max`, `max_concurrent`, semaphore, or spawn-budget config key.
- No per-profile concurrency cap (e.g., "at most 1 `backend-dev` at a time").
- No statement of whether one tick claims **one** ready task or **all** ready tasks.

Three repeated WebFetch probes specifically hunting for a concurrency cap each returned "No information found" / "does not specify" `[OFFICIAL]`. The only one-shot control is `hermes kanban dispatch --max N` `[OFFICIAL]`, which **"controls one-shot pass behavior — limiting how many tasks the dispatcher processes in a single invocation"** `[PRAC]`. Critically, `--max` is a flag on the *manual one-shot* `dispatch` command, **not** a config for the embedded gateway dispatcher's continuous loop — "the reference does not detail a default concurrency cap for the embedded gateway dispatcher's ongoing operation" `[OFFICIAL]`.

### Inferring the concurrency model from tutorial behavior

The tutorial gives the strongest behavioral evidence, and it points to a specific (unstated) model:

- **Cross-lane parallelism is real and unbounded by config.** Story 2: three specialist profiles (translator, transcriber, copywriter), each with a pile of independent tasks. **"With three daemons working on three assignee pools in parallel, the whole content queue drains without further human input"** `[OFFICIAL]`. So *different assignees run concurrently* — N lanes ⇒ up to N concurrent OS processes.
- **Within a single assignee pool, execution appears serial.** Story 2's operative sentence: **"The dispatcher will promote the next ready task to running as soon as the current one completes"** `[OFFICIAL]`. Story 2's board state is described as **"two transcribes done, one running, two ready waiting"** `[OFFICIAL]` — i.e., one transcriber task running, others queued in `ready`, not five transcriber processes in flight. This strongly implies **one in-flight run per assignee at a time** `[PRAC]`, with the claim acting as a de-facto per-assignee mutex (the claim lock `<host>:<pid>:<uuid>` is per task, but the observed pattern is one active claim per profile).
- **This is an inference, not a documented invariant** `[UNVERIFIED]`. The docs never state "one worker per assignee." It is possible the dispatcher would spawn multiple `transcriber` processes if multiple `transcriber` tasks were `ready` simultaneously; the tutorial just happens to show them draining one at a time. The phrase "as soon as the current one completes" is the only anchor, and it reads as serial-per-lane. **For a Momentum design decision this must be verified against Hermes source — it is the single highest-leverage unknown.**

### Practical concurrency ceiling

Effective parallelism ≈ **number of distinct assignees with ready work**, not a tunable worker count `[PRAC]`. To get K-way parallelism in Hermes you create K *distinct profiles/assignees*; you do not raise a concurrency knob. This is a structurally different model from Momentum's "sprint wave of N parallelizable stories spawned at once," where parallelism is a property of the *ready frontier width*, not the number of distinct worker identities.

## Do Lanes Encode Dependencies / Ordering?

**No — categorically, at the lane level** `[OFFICIAL]`. The worker-lanes page states lanes are independent executors and "no inter-lane ordering or dependency encoding is mentioned." Ordering lives entirely in two kernel mechanisms, *outside* lanes:

1. **`task_links` (parent→child edges).** **"The dispatcher promotes todo → ready when all parents are done"** `[OFFICIAL]`. This is an AND-join on parents. Story 1 is the canonical demonstration: schema → API → tests, created with `--parent`. **"Because `API` has `SCHEMA` as its parent, and `tests` has `API` as its parent, only `SCHEMA` starts in `ready`. The other two sit in `todo` until their parents complete"** `[OFFICIAL]`. On parent completion, "the dependency engine promotes `API` to `ready` automatically" `[OFFICIAL]`.
2. **Claim time** for the within-lane ordering of already-`ready` tasks (the dashboard's flat list is "ordered by claim time" `[OFFICIAL]`; priority influence is `[UNVERIFIED]`).

So the dependency model is: **a `task_links` DAG + AND-join promotion (`all parents done` ⇒ `todo→ready`)**, executed by lanes that are themselves graph-blind. The set of `ready` tasks at any moment **is** the ready frontier of the DAG. Lanes drain that frontier; the kernel re-computes it on every promotion.

### Can lane semantics express a dependency DAG / ready frontier?

**Yes — but the expressive power is in `task_links` + the dispatcher promotion rule, NOT in lanes.** Concretely `[PRAC, grounded in OFFICIAL mechanics]`:

- **DAG nodes** = tasks (`tasks` rows, each with one assignee). ✅ expressible.
- **DAG edges** = `task_links` parent→child rows; cross-board links disallowed (single-board DAGs only) `[OFFICIAL]`.
- **Ready frontier** = exactly the set of tasks in status `ready` (parents all `done`, not yet claimed). The dispatcher recomputes it every tick via the `all parents done ⇒ promote` rule. ✅ This is a genuine ready-frontier engine, equivalent in shape to Momentum's "wave of parallelizable stories."
- **Join semantics** = AND-only (`all parents done`). **No documented OR-join, no conditional/typed edges, no edge labels** `[OFFICIAL — by absence]`. This is a meaningful gap vs. Momentum's *typed-edge* beads graph: Hermes edges are untyped "blocks-until-done" only. A typed dependency (e.g., "informs" vs. "blocks" vs. "discovered-by") cannot be expressed natively — all edges are hard AND-blocking.
- **Frontier *width* (parallelism)** = bounded by distinct ready assignees, not by frontier size, given the `[PRAC]` serial-per-lane behavior. A Momentum "wave" of 5 parallel stories all assigned to one `dev` profile would (on the inferred model) execute **serially**, not in 5-way parallel — unless split across 5 distinct assignees. **This is the sharpest mismatch between the two models** `[PRAC]`.

So: Hermes *can* represent a dependency DAG and *does* maintain a true ready frontier — but (a) edges are untyped AND-blocking only, and (b) frontier-width parallelism is keyed to distinct worker identities, not to the number of independent ready nodes. Momentum's model (typed-edge beads graph + wide same-role waves) is *richer on both axes*.

## Lane Lifecycle and Failure Handling (delta only)

Prior art §5.1, §7 covered the full lifecycle (spawn env block, the three terminators, stale-claim TTL `DEFAULT_CLAIM_TTL_SECONDS` 15 min, crash reap, stranded detection 30 min, per-task `max_runtime_seconds`). Not repeated. The relevant deltas for parallelism/cost:

- **Respawn is a fresh OS process and a new `task_runs` row.** After `kanban_unblock`, "the dispatcher promotes `$IMPL` back to `ready` and, on the next tick, respawns the `backend-dev` worker. This second spawn is a **new run** on the same task" `[OFFICIAL]`. The retry worker's `worker_context` includes the prior run's block reason `[OFFICIAL]` — structured retry, no re-derivation.
- **Circuit breaker default is internally contradictory in the source** — the kanban reference says `failure_limit: 2`; the tutorial prose says "three consecutive failures (the default `failure_limit`)"; prior art §7.1 also found a "5" instance. **Unresolved `[UNVERIFIED]`** — must be checked against Hermes config source before any Momentum decision depends on the number.
- **Promotion latency floor = `dispatch_interval_seconds` (60s default)**, bypassable via the dashboard **"Nudge dispatcher"** action ("60s by default, or immediately if you hit Nudge dispatcher") `[OFFICIAL]`. Any Momentum-on-Hermes pipeline inherits a ~60s inter-stage latency unless every handoff is manually nudged — a non-trivial throughput tax for fine-grained story graphs.

## Resource and Cost Implications of Multiple Lanes

- **One full OS process per active run** `[OFFICIAL]` (`hermes -p <assignee> chat -q ...`). Not a thread, not a coroutine — a complete Hermes agent process with its own model context. N concurrent lanes ⇒ N concurrent agent processes ⇒ N concurrent model-inference streams.
- **The docs do not quantify model-call cost, memory, or token overhead** `[OFFICIAL — by absence]`. The worker-lanes page: "The document does not quantify model call costs, memory overhead, or concurrency impact on costs."
- **Cost is governed by lane count + retry count, with no kernel-level budget cap** `[PRAC]`. There is no documented spend ceiling, token budget, or "max N model calls" governor in the kernel; the prior discovery noted budgets/governance are explicitly *user-space* (a router profile or `tools/approval.py`), not core. For a **cost-sensitive, local-only** project this is a material risk: an auto-decomposed graph that fans out into many tasks across many assignees, each retrying up to the (ambiguous) failure limit, has **no built-in brake** — backpressure is the operator's responsibility.
- **`auto_decompose_per_tick: 3`** caps how fast the graph *grows* (3 decompositions/tick), which indirectly throttles fan-out rate but not total fan-out or total spend `[PRAC]`.
- The serial-per-assignee `[PRAC]` behavior is, perversely, a *cost containment* property: if one `dev` lane drains its queue serially, you pay for one inference stream at a time for that role, not the whole frontier at once. Momentum's wide-wave model is faster but more cost-spiky. This is a genuine tradeoff to surface in the dispatcher decision.

## Bottom Line for the Momentum Mapping

`[PRAC]` synthesis, grounded in the `[OFFICIAL]` mechanics above:

1. **Lanes are order-blind dumb executors.** All DAG/ordering intelligence is in `task_links` + the dispatcher's `all-parents-done ⇒ promote` rule. A Momentum mapping would map: beads-graph edge → `task_links` row; Momentum story → kanban task; Momentum role/agent → assignee/profile; ready frontier → set of `ready` tasks. The shapes align.
2. **Two structural mismatches block a clean 1:1 mapping.** (a) Hermes edges are **untyped AND-blocking only** — Momentum's typed-edge beads graph loses information on the way in. (b) Hermes parallelism is keyed to **distinct assignee identities**, not frontier width — Momentum's "N parallel same-role stories per wave" does **not** parallelize on Hermes unless artificially split into N distinct profiles (the inferred serial-per-lane behavior).
3. **The single highest-leverage unknown** is whether the dispatcher truly serializes per assignee or will spawn multiple same-assignee workers when multiple are `ready`. The docs never state it; the tutorial implies serial. **This must be verified against Hermes source before deciding Hermes-as-delegate.** If it serializes per assignee, Hermes cannot natively reproduce Momentum's wide same-role dev waves.
4. **No kernel cost governor** + ~60s promotion latency floor are concrete frictions against the local-only, cost-sensitive, Claude-Code-skill-centric constraints. A Claude-native dispatcher would have full control over both; Hermes pushes both into user-space.

## Sources

- [OFFICIAL] Hermes docs — *Kanban Worker Lanes*: `https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-worker-lanes` (fetched 2026-05-18; no publish date on page). Lane definition, three-part contract, env block, lifecycle terminators, "lanes execute but never own lifecycle truth," review-required convention, explicit absence of concurrency-cap documentation.
- [OFFICIAL] Hermes docs — *Kanban* (reference): `https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban` (fetched 2026-05-18). Dispatcher tick (`dispatch_interval_seconds: 60`, `dispatch_in_gateway: true`), `failure_limit: 2`, `auto_decompose: true`, `auto_decompose_per_tick: 3`, `orchestrator_profile`, `default_assignee`, `task_links` AND-join promotion, status state machine, "Lanes by profile" = UI-only, `--max`/`--dry-run` on `dispatch`, decomposer "JSON task graph" description.
- [OFFICIAL] Hermes docs — *Kanban Tutorial*: `https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-tutorial` (fetched 2026-05-18). Story 1 (schema→API→tests `--parent` chain, "only SCHEMA starts in ready"), Story 2 (three specialists "in parallel," "promote the next ready task to running as soon as the current one completes," "two transcribes done, one running, two ready waiting"), Nudge dispatcher, new-run respawn after unblock.
- [OFFICIAL] Prior art — *Hermes Kanban Comprehensive Discovery* (2026-05-17): `/Users/steve/projects/momentum/docs/research/hermes-kanban-discovery-2026-05-17.md`. §5 lane contract, §7 failure modes, §7.1 circuit-breaker contradiction (2 vs 3 vs 5), §12 single-host scope, §13 Momentum parallels. Extended, not repeated, here.
- [UNVERIFIED] Hermes v1 design spec PDF (`docs/hermes-kanban-v1-spec.pdf`, in the Hermes repo) — not fetched; would contain concurrency-correctness proofs that could resolve the serial-per-assignee question and the circuit-breaker default. Flagged as the source to consult before a final dispatcher decision.
