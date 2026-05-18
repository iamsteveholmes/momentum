---
content_origin: claude-code-subagent
date: 2026-05-18
sub_question: "How does the Hermes Kanban board work — board/column/card model, task lifecycle, creation/claim/progress, and persistence?"
topic: "Can Hermes run as a 24/7 dispatcher/delegate with Claude Code as planner/brains, and can Hermes Kanban + worker lanes map onto Momentum?"
---

# Hermes Kanban Board Mechanics — Verification & Extension

## Scope and Method

This document **verifies and extends** the prior discovery at
`/Users/steve/projects/momentum/docs/research/hermes-kanban-discovery-2026-05-17.md`.
It does not repeat that document's framing. It re-fetches the two assigned official
sources plus the sibling worker-lanes page on 2026-05-18, confirms or corrects the
prior art's concrete claims, and pins down field names, status values, transition
triggers, and storage details at the resolution a Momentum-mapping analysis needs.

Tagging: `[OFFICIAL]` = stated directly in the Hermes docs fetched today;
`[PRAC]` = behavioral/operational detail drawn from the tutorial walkthroughs (still
official docs, but narrative/example-derived rather than reference-spec text);
`[UNVERIFIED]` = inferred or unresolved. Untagged sentences are framing only.

No external triangulation (Gemini) or AVFL was run for this sub-question; behavioral
specifics are "as documented." The Hermes docs carry **no version stamp or date**;
they reference `docs/hermes-kanban-v1-spec.pdf` as the authoritative design artifact,
which was not fetched. Treat the docs as the current public v1 surface; flag the
absence of a version date as a staleness risk for any number relied upon below.

## Board / Column / State Model

The board is a single fixed pipeline. The status enum — verbatim from the docs —
is `triage | todo | ready | running | blocked | done | archived`, seven values,
one column per status [OFFICIAL]. There are **no user-defined columns and no
swimlanes in the data model**: the only sub-grouping is a dashboard-only toggle
that lanes the `running` column by `assignee` profile, controlled by the
`dashboard.kanban.lane_by_profile` config key (default `true`) [OFFICIAL]. This
confirms the prior art's enum and the "lanes are a view, not a model concept"
reading. `triage` is explicitly "the parking column for rough ideas"; `archived`
hides a task from the default board view but does not delete it [OFFICIAL].

The board is profile-agnostic by design — it is a coordination primitive, so
opening it as any one profile still shows every profile's tasks [OFFICIAL]. This
matters for the Momentum mapping: there is no per-worker board partition; isolation
is achieved only via separate boards or soft `tenant` filtering.

## Task / Card Schema

The `tasks` row carries these fields, confirmed by today's fetch [OFFICIAL]:

- `id` / `task_id` — unique id; tutorial examples show a `t_<alphanum>` shape [PRAC]
- `title` — required string
- `body` — optional markdown description
- `assignee` — a Hermes profile name, or unassigned/`None`
- `status` — one of the seven enum values
- `priority` — numeric, set via `--priority N`
- `tenant` — optional soft namespace string
- `idempotency_key` — optional dedupe key for automation/webhook callers
- `max_runtime_seconds` — per-task wall-clock ceiling; CLI accepts `30m|2h|1d|<seconds>`
- `workspace` — one of `scratch` (default fresh tmp dir), `dir:<absolute_path>`
  (shared dir; **must be absolute** — relative rejected at dispatch as a
  confused-deputy guard), or `worktree` (git worktree under `.worktrees/<id>/`)
- `current_run_id` — pointer to the active `task_runs` row, or `NULL`
- `workflow_template_id`, `current_step_key` — reserved nullable columns for v2
  workflow routing; **ignored by v1 routing** but writable by clients [OFFICIAL]

Dependencies are **not** a task field — they are separate `task_links` rows
(`parent_id → child_id`), settable at create time via `--parent`/`parents=[...]`
or after the fact via `kanban_link` [OFFICIAL]. Skills can be pinned at creation
(`--skill`/`skills=[...]`) so the spawned worker auto-loads them [OFFICIAL]. The
docs state **no explicit max body length, metadata size limit, or comment-thread
pagination** [OFFICIAL] — a real constraint for a Momentum bridge that would push
large story specs or AVFL findings through `body`/`metadata`.

## Task Lifecycle — States and Exact Transition Triggers

The prior art's transition table is confirmed and tightened. Creation state is
**context-dependent**, and the docs are slightly soft here: `triage` is the
parking state for rough ideas (and `/kanban create --triage` lands there);
the default base case and orchestrator `kanban_create` fan-out land children in
`todo` [OFFICIAL]. This is a documented ambiguity, not a contradiction — the doc
itself does not crisply state the no-flag default, so treat "default = `todo`,
`--triage` = `triage`" as the safe reading [UNVERIFIED on the exact no-flag default].

| From → To | Trigger | Actor |
|---|---|---|
| (none) → `triage` or `todo` | `kanban create` / `kanban_create` / REST `POST` / dashboard inline-create | human or orchestrator agent [OFFICIAL] |
| `triage → todo` | `hermes kanban specify <id>` / `/kanban specify` / dashboard ✨ / `POST .../specify`; or auto-decompose fan-out | triage specifier LLM / decomposer [OFFICIAL] |
| `todo → ready` | all parent tasks reach `done` | dispatcher (link-driven promotion; `promoted` event) [OFFICIAL] |
| `ready → running` | atomic claim + worker spawn | dispatcher (`claimed` then `spawned` events) [OFFICIAL] |
| `running → done` | `kanban_complete(summary, metadata)` | worker agent [OFFICIAL] |
| `running → blocked` | `kanban_block(reason)` | worker agent [OFFICIAL] |
| `blocked → ready` | `hermes kanban unblock` / `/kanban unblock` / `kanban_unblock` / dashboard | human or orchestrator [OFFICIAL] |
| `running → ready` | stale-claim TTL expiry (only if PID actually dead) | dispatcher (`reclaimed`) [OFFICIAL] |
| `running → ready` | crash detection — `kill(pid,0)` shows dead PID | dispatcher (`crashed`) [OFFICIAL/PRAC] |
| `running → ready` | `max_runtime_seconds` exceeded — SIGTERM then SIGKILL after 5s grace | dispatcher (`timed_out`) [OFFICIAL] |
| `ready → blocked` | N consecutive spawn failures (circuit breaker) | dispatcher (`gave_up`) [OFFICIAL] |
| any → `archived` | `kanban archive` / dashboard; reclaims an in-flight run | human [OFFICIAL] |
| any ↔ any | dashboard drag-drop direct status write | human (`status` event; destructive moves confirm) [OFFICIAL] |

The single most load-bearing fact for the Momentum question: **only the dispatcher
moves a card from `ready` into `running`, and it does so by claiming and spawning a
process.** There is no "agent picks up its own card" path — claim is centralized,
atomic, and dispatcher-owned. A worker's only forward levers are `kanban_complete`
(→`done`) and `kanban_block` (→`blocked`); everything else (promotion, claim,
reclaim, timeout, circuit-break) is the dispatcher's.

## How Tasks Are Created

Four creation surfaces, all routed through the same `kanban_db` layer [OFFICIAL]:

1. **CLI** — `hermes kanban create "<title>" [--body --assignee --parent --tenant
   --workspace --priority --triage --idempotency-key --max-runtime --skill --json]`
2. **Orchestrator agent tool** — `kanban_create(title=..., assignee=...,
   body=..., parents=[...], skills=[...])` — the only documented agent-side
   create path, and it is gated to orchestrator-class profiles
3. **REST** — `POST /api/plugins/kanban/tasks` with JSON including `triage: bool`
   and `parents: [id,…]`
4. **Dashboard** — inline `+` per column header → form (title, assignee,
   priority, optional parent dropdown)

**Idempotent create is first-class**: "First call creates the task. Any subsequent
call with the same key returns the existing task id" — the dedupe key prevents
webhook/automation double-creation [OFFICIAL]. This is directly relevant if
Momentum were to push the same sprint repeatedly into a Hermes board.

## Claim / Assignment Mechanism

`assignee` is set independently of claiming. `hermes kanban assign <id> <profile>`
(or dashboard reassign) only writes the `assignee` field and emits an `assigned`
event — it does **not** spawn a worker; the dispatcher spawns on its next claim
cycle [OFFICIAL]. The dispatcher tick (default 60s, `dispatch_interval_seconds`)
runs this ordered sequence [OFFICIAL]:

1. Reclaim stale claims (TTL expired, PID dead)
2. Reclaim crashed workers (PID gone, TTL not yet expired)
3. Promote `todo → ready` where all parents are `done`
4. **Atomically claim** a `ready` task inside a `BEGIN IMMEDIATE` transaction
5. Spawn the assigned profile as a worker process

The atomic claim creates a `task_runs` row, sets `tasks.current_run_id` to it, and
records a `claimed` event whose payload is `{lock, expires, run_id}` [OFFICIAL].
The **claim lock string format is `<host>:<pid>:<uuid>`** [OFFICIAL] — confirmed
verbatim today, resolving the prior art's `[UNVERIFIED]` on lock format. WAL mode
is explicitly enabled so "the read loop never blocks the dispatcher's
`BEGIN IMMEDIATE` claim transactions" [OFFICIAL] — i.e., observers (dashboard, CLI
`watch`) never serialize against the claim path.

An unresolvable `assignee` (typo, deleted profile, down external pool) does **not**
get silently dropped or run by a fallback — the task stays in `ready` and surfaces
in diagnostics; the prior art's "`skipped_nonspawnable`/stranded detection" framing
is consistent with today's fetch though the specific `stranded_threshold_seconds`
default did not re-appear in the fetched pages [UNVERIFIED on the exact number].

The default spawn command for a Hermes-profile lane is verbatim
`hermes -p <assignee> chat -q <prompt>` (or the module form when the `hermes`
shim is off `$PATH`) [OFFICIAL]. Non-Hermes lanes must supply their own
`spawn_fn` callable; **external CLI workers (Codex CLI, Claude Code CLI, OpenCode,
local model runners) are explicitly "not yet a paved path"** — `spawn_fn` is a
pluggable parameter but the exit-code→`kanban_complete`/`kanban_block` mapping,
workspace/sandbox bridging, and auth are unbuilt per-integration work [OFFICIAL].
This is the central constraint for "Hermes as delegate with Claude Code as the
brains": the Claude Code worker lane does not exist as a turnkey path and would be
net-new bridging code.

## Worker Lifecycle Terminator Contract

Every claim must end in exactly one of three ways [OFFICIAL]:

- `kanban_complete(summary=..., metadata=...)` → `done`
- `kanban_block(reason=...)` → `blocked` (respawns on `kanban_unblock`)
- process exits with **no** terminating tool call → kernel classifies as
  `crashed` (PID died), `gave_up` (consecutive-failure breaker tripped), or
  `timed_out` (`max_runtime` exceeded)

A worker that calls neither and exits "normally" is still treated as crashed —
there is no implicit success. The env handed to a spawned worker is confirmed
verbatim today: `HERMES_KANBAN_TASK`, `HERMES_KANBAN_DB` (absolute per-board
SQLite path), `HERMES_KANBAN_BOARD`, `HERMES_KANBAN_WORKSPACES_ROOT`,
`HERMES_KANBAN_WORKSPACE` (absolute path for this task), `HERMES_KANBAN_RUN_ID`
(lifecycle gate), `HERMES_KANBAN_CLAIM_LOCK`, `HERMES_PROFILE`, `HERMES_TENANT`
[OFFICIAL]. This is the exact integration contract a Momentum/Claude-Code bridge
would have to satisfy: read `HERMES_KANBAN_TASK`, operate in
`HERMES_KANBAN_WORKSPACE`, and terminate by writing to the DB at
`HERMES_KANBAN_DB` via the `kanban_*` tools (or the REST API for non-Hermes
workers).

## Runs — Attempt History as Primary Representation

A **task** is the logical unit; a **run** is one attempt. Confirmed today [OFFICIAL/PRAC]:
each claim opens a `task_runs` row; `tasks.current_run_id` points at the live run
or is `NULL`. Run `outcome` values observed in the docs:
`active/completed/blocked/crashed/spawn_failed/gave_up/timed_out` (the prior art's
list, consistent with today's fetch). Per-run fields:
`id, task_id, started_at, ended_at, outcome, summary, metadata, error, pid,
claimer/profile`. Three attempts = three rows; the dashboard "drawer" shows the
full Run History with each attempt's outcome, worker, duration, summary, and
metadata blob [PRAC]. Synthetic zero-duration runs are inserted when a human
completes/blocks a never-claimed task so attempt history stays complete [OFFICIAL,
per prior art; not re-contradicted today].

## Structured Handoff

`kanban_complete(summary, metadata)` is the primary inter-stage handoff channel,
not decoration [OFFICIAL]. When the next worker calls `kanban_show()`, the returned
`worker_context` includes (a) this task's prior attempts (outcome, summary, error,
metadata) and (b) for each parent, that parent's most-recent **completed** run's
summary + metadata [OFFICIAL/PRAC]. Recommended metadata convention (not an
enforced schema): `changed_files`, `verification`, `dependencies`,
`blocked_reason`, `retry_notes`, `residual_risk` [OFFICIAL]. Tutorial Story 3
makes the payoff concrete: a PM task writes acceptance criteria into `metadata`;
the engineer's worker reads it structurally from the parent handoff rather than
re-parsing a design doc [PRAC]. `kanban_complete` is always single-task — there is
no bulk variant in the tool surface; bulk close via CLI is refused when handoff
flags are present [OFFICIAL].

## Persistence / Storage Backend

Single-host SQLite, WAL mode. Paths confirmed today [OFFICIAL]:

- Default board DB: `~/.hermes/kanban.db`
- Non-default board DB: `~/.hermes/kanban/boards/<slug>/kanban.db`
- Default workspaces: `~/.hermes/kanban/workspaces/<id>/`
- Non-default workspaces: `~/.hermes/kanban/boards/<slug>/workspaces/<id>/`
- Logs: `~/.hermes/kanban/logs/` (or `boards/<slug>/logs/`)

Tables [OFFICIAL]: `tasks` (metadata + `current_run_id`), `task_runs` (one row
per attempt — the **primary** retry representation, not an afterthought),
`task_links` (`parent_id`/`child_id` edges), `task_events` (append-only,
monotonic `id`, `task_id`, nullable `run_id`, `kind`, JSON `payload`,
`created_at`), `task_comments` (`task_id`, `author`, `body`, `created_at` — the
durable inter-agent thread, read into `worker_context` on every spawn). There is
no server process owning the data — it is a file any host-local process can open,
which is exactly why the dashboard plugin routes are unauthenticated by design
(localhost bind) and why `--host 0.0.0.0` is explicitly warned against.

This is the hard scope boundary for the larger project: **single-host only.** The
DB is a local file; the dispatcher spawns workers on the same machine; crash
detection assumes host-local PIDs (`kill(pid,0)`). There is no multi-host
coordination primitive. For Momentum's local-only, cost-sensitive constraint this
is actually aligned — but it also means Hermes Kanban cannot itself be the
distributed substrate; it is a local queue.

## Multi-Board Support

One install = many boards; new install has exactly one board `default` (at
`~/.hermes/kanban.db` for back-compat). Per-board isolation is **absolute**:
separate DB, `workspaces/`, `logs/`; workers see only their board's tasks via the
pinned `HERMES_KANBAN_BOARD` env var; **cross-board links are disallowed**
[OFFICIAL]. Slug rules: lowercase alnum + hyphen + underscore, 1–64 chars, must
start alphanumeric, uppercase auto-downcased, path-traversal chars rejected
[OFFICIAL]. Resolution precedence (highest first): `--board` flag >
`HERMES_KANBAN_BOARD` env > `~/.hermes/kanban/current` (set by `boards switch`) >
`default` [OFFICIAL]. Board CLI: `boards list/create/switch/show/rename/rm`
(`rm` archives or hard-deletes with `--delete`) [OFFICIAL]. `tenant` is a **soft**
filter within one board (workspace-path + memory-key prefix isolation); boards are
the hard boundary [OFFICIAL]. For a Momentum mapping, "one board per repo/project"
is the natural unit; `tenant` maps loosely to a sprint or feature namespace.

## External Observability of State

State is observable without touching agent memory because the board lives entirely
in SQLite [OFFICIAL]:

- **Events table** — every transition appends a `task_events` row. ~19 kinds in
  three clusters: lifecycle (`created, promoted, claimed, completed, blocked,
  unblocked, archived`), edits (`assigned, edited, reprioritized, status`),
  telemetry (`spawned, heartbeat, reclaimed, crashed, timed_out, spawn_failed,
  gave_up`). Payloads are concrete, e.g. `claimed → {lock, expires, run_id}`,
  `completed → {result_len, summary?}` (first line, 400-char cap),
  `timed_out → {pid, elapsed_seconds, limit_seconds, sigkill}`,
  `gave_up → {failures, error}` [OFFICIAL].
- **CLI** — `hermes kanban tail <id>` (single-task stream), `watch [--assignee
  --tenant --kinds --interval]` (board-wide stream), `show`, `list`, `stats`,
  `runs <id>` (attempt history), `context <id>` (exactly what a worker sees)
  [OFFICIAL].
- **REST** — `GET /api/plugins/kanban/board`, `GET .../tasks/:id`,
  `PATCH .../tasks/:id`, bulk, comments, specify, decompose, profiles,
  orchestration endpoints [OFFICIAL].
- **WebSocket** — `WS /api/plugins/kanban/events?since=<event_id>&token=<...>`
  tails `task_events` with a last-seen cursor; requires the ephemeral session
  token [OFFICIAL].
- **Slash command** — `/kanban <verb>` from interactive chat and every gateway
  platform; **explicitly exempted from the running-agent guard** so reads/writes
  go through mid-turn (unblock a peer from your phone without interrupting the
  blocked worker) [OFFICIAL]. Gateway `/kanban create` auto-subscribes the chat
  to terminal events [OFFICIAL].

For Momentum, the append-only `task_events` table with a monotonic id and a
`since=` cursor is the clean external-observability primitive — a Claude-native
dispatcher could poll or tail it without coupling to agent state. This is
architecturally close to Momentum's `intake-queue.jsonl` event-log pattern and the
"index files as shared state" principle.

## Resolved Contradiction: Circuit-Breaker Default

The prior art flagged an unresolved 2-vs-3-vs-5 contradiction. Today's targeted
re-fetch **confirms it is a real, in-source inconsistency**, quoted verbatim:

- **Core concepts section:** "After `kanban.failure_limit` consecutive spawn
  failures on the same task (default: **2**) the dispatcher auto-blocks it"
  [OFFICIAL]
- **Event reference, `gave_up` row:** "Circuit breaker fired after N consecutive
  `spawn_failed`. Task auto-blocks with the last error. Default N = **5**"
  [OFFICIAL]
- **Tutorial Story 4 prose:** "After three consecutive failures (the default
  `failure_limit`)" — i.e., **3** [PRAC]
- The worker-lanes page mentions `consecutive_failures` and auto-block but states
  **no number** [OFFICIAL]

Three different defaults (2, 3, 5) appear across the official docs. The CLI exposes
`--failure-limit N` and the config key is `kanban.failure_limit`, so the value is
operator-overridable regardless. **Recommendation for the Momentum design
decision: do not rely on any specific default; treat the circuit-breaker threshold
as a configurable knob and verify against the actual Hermes source/config if a
precise value ever gates a design choice.** This is the one place the docs cannot
be trusted on a number.

Other defaults confirmed today: `dispatch_interval_seconds: 60`,
`dispatch_in_gateway: true`, `auto_decompose: true`, `auto_decompose_per_tick: 3`.
The stale-claim TTL (`DEFAULT_CLAIM_TTL_SECONDS`, prior art said 15 min) and
`stranded_threshold_seconds` (prior art said 30 min) **did not re-appear** in the
pages fetched today — treat those specific numbers as prior-art-only and
[UNVERIFIED] pending the v1 spec PDF.

## Implications for the Momentum Mapping (observations, not recommendations)

1. **Claim is dispatcher-centralized and atomic.** Any Hermes-as-delegate model
   inherits a single 60s-tick local loop as the only thing that moves cards into
   `running`. A Claude-native dispatcher would have to reimplement this loop or
   drive Hermes's loop from outside via CLI/REST.
2. **No turnkey Claude Code worker lane.** `spawn_fn` is pluggable but the
   exit-code→terminator, workspace, and auth bridging is net-new. "Hermes
   dispatches, Claude Code is the brain" is not a configuration — it is an
   integration project.
3. **The event table is the cleanest seam.** Append-only `task_events` + monotonic
   cursor maps directly onto Momentum's event-log instincts; this is the lowest-
   friction interop surface, far cheaper than a worker-lane bridge.
4. **Single-host SQLite aligns with local-only/cost-sensitive constraints** but
   confirms Hermes Kanban is a local queue, not a distributed substrate.
5. **Per-run attempt history + structured `metadata` handoff** remain the two
   ideas with the highest carry-over value into Momentum's story/retry model.

## Sources

- [OFFICIAL] Hermes Kanban reference — `https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban` (fetched 2026-05-18; no version date in page)
- [PRAC] Hermes Kanban tutorial — `https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-tutorial` (fetched 2026-05-18)
- [OFFICIAL] Hermes Kanban worker lanes — `https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-worker-lanes` (fetched 2026-05-18)
- Sibling page `.../features/kanban-architecture` — HTTP 404 on 2026-05-18 (does not exist)
- Prior art (verified/extended, not repeated) — `/Users/steve/projects/momentum/docs/research/hermes-kanban-discovery-2026-05-17.md`
- Referenced but not fetched — `docs/hermes-kanban-v1-spec.pdf` in the Hermes repo (authoritative design doc; concurrency proofs, exact TTL/stranded defaults, circuit-breaker resolution live here)
