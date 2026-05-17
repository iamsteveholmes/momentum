# Hermes Kanban — Comprehensive Discovery

**Date:** 2026-05-17
**Type:** Lightweight discovery (no Gemini triangulation, no AVFL validation)
**Sources:**

- `https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban` (reference / data model)
- `https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-tutorial` (four narrative user stories)
- `https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-worker-lanes` (lane contract)

> **Provenance note:** All claims below are sourced directly from the three Hermes docs pages above. No external triangulation was performed (per the lightweight-research request). Treat behavioral specifics (default intervals, retry counts) as "documented" not "independently verified" — note the docs themselves contain one internal contradiction on the circuit-breaker default (see §7.1).

---

## 1. What Hermes Kanban Is

Hermes Kanban is a **durable, single-host task board** that lets multiple *named* agents (Hermes profiles) collaborate on work without fragile in-process subagent swarms. It is the coordination primitive for workloads that exceed a simple RPC-style delegation.

Core premises:

- **Every task is a row** in a SQLite DB (`~/.hermes/kanban.db` for the default board).
- **Every handoff is a row** anyone (agent or human) can read and write.
- **Every worker is a full OS process** with its own identity (a Hermes profile), not an anonymous subagent.

It explicitly targets the workloads `delegate_task` (Hermes's fork→join RPC primitive) *cannot* serve:

- Research triage (parallel researchers + analyst + writer, human-in-the-loop)
- Scheduled ops (recurring daily briefs that accumulate over weeks)
- Digital twins (persistent named assistants with growing memory)
- Engineering pipelines (decompose → parallel worktree implement → review → iterate → PR)
- Fleet work (one specialist managing N subjects — 50 social accounts, 12 services)

### 1.1 Kanban vs. `delegate_task` (the key conceptual distinction)

| Dimension | `delegate_task` | Kanban |
|---|---|---|
| Shape | RPC call (fork → join) | Durable message queue + state machine |
| Parent | Blocks until child returns | Fire-and-forget after `create` |
| Child identity | Anonymous subagent | Named profile w/ persistent memory |
| Resumability | None — failed = failed | Block→unblock→re-run; crash→reclaim |
| Human-in-loop | Not supported | Comment / unblock at any point |
| Agents per task | One call = one subagent | N agents over task's life |
| Audit trail | Lost on context compression | Durable SQLite rows forever |
| Coordination | Hierarchical (caller→callee) | Peer — any profile reads/writes any task |

**One-sentence distinction (their words):** `delegate_task` is a function call; Kanban is a work queue where every handoff is a row any profile (or human) can see and edit. They coexist — a kanban worker may call `delegate_task` internally.

---

## 2. The Two-Surface Architecture (the central design idea)

The board has **two front doors, one backend**. Both route through the same `kanban_db` Python layer so reads are consistent and writes can't drift.

1. **Agents drive the board through a dedicated `kanban_*` toolset** — they call tools directly, *never* shell out to `hermes kanban`. The dispatcher spawns each worker with these tools already in its schema.
2. **Humans / scripts / cron drive the board through `hermes kanban …` CLI**, the `/kanban` slash command, or the dashboard GUI.

This is a deliberate, repeatedly-emphasized separation: **the model talks through tools; the human talks through the CLI.** Workers spawned by the dispatcher never see the dashboard or the CLI.

### 2.1 The `kanban_*` worker toolset

| Tool | Purpose | Required params |
|---|---|---|
| `kanban_show` | Read current task (title, body, prior attempts, parent handoffs, comments, pre-formatted `worker_context`). Defaults to `$HERMES_KANBAN_TASK`. | — |
| `kanban_list` | List task summaries w/ filters (assignee, status, tenant, archived, limit). For orchestrators. | — |
| `kanban_complete` | Finish w/ `summary` + `metadata` structured handoff. | ≥1 of `summary`/`result` |
| `kanban_block` | Escalate for human input. | `reason` |
| `kanban_heartbeat` | Signal liveness during long ops (pure side-effect). | — |
| `kanban_comment` | Append durable note to task thread. | `task_id`, `body` |
| `kanban_create` | (Orchestrators) fan out child tasks. | `title`, `assignee` |
| `kanban_link` | (Orchestrators) add parent→child edge after the fact. | `parent_id`, `child_id` |
| `kanban_unblock` | (Orchestrators) move blocked task back to `ready`. | `task_id` |

**Why tools instead of shelling out (their three reasons):**

1. **Backend portability** — workers with a remote terminal backend (Docker/Modal/SSH) would run `hermes kanban` *inside* the container where it isn't installed; tools run in the agent's own Python process and always reach the DB.
2. **No shell-quoting fragility** — passing `--metadata '{json}'` through shlex+argparse is a footgun; structured tool args skip it.
3. **Better errors** — tool results are structured JSON the model can reason about, not stderr strings.

**Zero schema footprint:** a normal `hermes chat` has *zero* `kanban_*` tools. Each tool's `check_fn` only returns true when `HERMES_KANBAN_TASK` is set (i.e., only in dispatcher-spawned processes). No tool bloat for non-kanban users.

---

## 3. Core Data Model

- **Board** — a standalone queue: its own SQLite DB, workspaces dir, dispatcher loop. One install = many boards (per project/repo/domain). Default board = `default` (DB at `~/.hermes/kanban.db`; non-default at `~/.hermes/kanban/boards/<slug>/kanban.db`).
- **Task** — row with title, optional body, one assignee (profile name), status, optional tenant, optional idempotency key. Status enum: `triage | todo | ready | running | blocked | done | archived`.
- **Link** — `task_links` row recording a parent→child dependency. Dispatcher promotes `todo → ready` when **all** parents are `done`.
- **Comment** — the inter-agent protocol; appended by agents/humans; full thread is read into a worker's context on (re-)spawn.
- **Workspace** — directory the worker operates in. Three kinds:
  - `scratch` (default) — fresh tmp dir per task.
  - `dir:<path>` — existing shared dir (Obsidian vault, mail ops). **Must be absolute** — relative paths rejected at dispatch (confused-deputy escape vector). Trusted-local-user threat model.
  - `worktree` — git worktree under `.worktrees/<id>/` for coding tasks.
- **Dispatcher** — long-lived loop (default 60s tick): reclaims stale claims, reclaims crashed workers, promotes ready tasks, atomically claims, spawns assigned profiles. Runs **inside the gateway** by default.
- **Tenant** — soft string namespace *within* a board. Boards = hard isolation; tenants = soft filter.

### 3.1 Runs — one row per attempt (critical concept)

A **task** is a logical unit of work; a **run** is one attempt. When the dispatcher claims a ready task it creates a `task_runs` row and points `tasks.current_run_id` at it. When the attempt ends (completed/blocked/crashed/timed_out/spawn_failed/reclaimed) the run closes with an `outcome` and the pointer clears. Three attempts = three `task_runs` rows.

**Why two tables:** you need full attempt history for postmortems, and a clean place to hang per-attempt metadata (changed files, tests run, reviewer findings) — those are *run* facts, not *task* facts. Retry history is the *primary* representation, not an afterthought layered on "latest state."

Invariant: a `task_runs` row is always terminal when `tasks.current_run_id` is NULL, and vice versa — holds across CLI, dashboard, dispatcher, notifier.

**Synthetic runs:** completing/blocking a never-claimed task (human closes a `ready` task with a summary) inserts a zero-duration run (`started_at == ended_at`) so attempt history stays complete.

**Forward-compat:** two reserved nullable `tasks` columns for v2 workflow routing — `workflow_template_id`, `current_step_key`. v1 ignores them for routing but lets clients write them (no future schema migration needed).

---

## 4. Structured Handoff (the payoff mechanic)

When a worker on task B is spawned and calls `kanban_show()`, the returned `worker_context` includes:

- **B's prior attempts** (previous runs: outcome, summary, error, metadata) so a retrying worker doesn't repeat a failed path.
- **Parent task results** — for each parent, the most-recent *completed* run's summary + metadata — so downstream workers see why/how upstream work was done.

This replaces the "dig through comments and work output" dance of flat kanban systems. `kanban_complete(summary=..., metadata=...)` is the primary handoff channel between workflow stages, not decoration.

Recommended (convention, not enforced schema) metadata shape for engineering/review tasks:

```json
{
  "changed_files": ["path/to/file.py"],
  "verification": ["pytest tests/... -q"],
  "dependencies": ["parent task id or external issue"],
  "blocked_reason": null,
  "retry_notes": "what failed before, if this was a retry",
  "residual_risk": ["what was not tested / still needs human review"]
}
```

The useful property: every worker leaves enough evidence for the next reader to answer — (1) what changed? (2) how verified? (3) what unblocks/retries it? (4) what risk is deliberately left open? Keep secrets/tokens/raw logs *out* of metadata — store pointers/summaries.

**Bulk-close guard:** `hermes kanban complete a b c --summary X` is **refused** — structured handoff is per-run, so copy-pasting one summary to N tasks is almost always wrong. Bulk close *without* handoff flags still works for "I finished a pile of admin tasks." The tool surface doesn't expose a bulk variant at all — `kanban_complete` is always single-task.

---

## 5. Worker Lanes (the integration contract)

A **worker lane** is a class of process the dispatcher can route tasks to. Hierarchy:

```
Hermes Kanban  =  canonical task lifecycle + audit trail
Worker lane    =  implementation executor for one assigned card
Reviewer       =  human or human-proxy that gates "done"
GitHub PR      =  upstreamable artifact (optional, for code lanes)
```

Kanban owns lifecycle truth. Lanes execute but never own that truth — everything flows back through `kanban_*` tools (or the API for non-Hermes external workers). Reviewers gate "code written" → "task done."

### 5.1 What a lane must provide (three things)

1. **An assignee string** — dispatcher matches `task.assignee` against a Hermes profile name (default lane) or a registered non-spawnable id (plugin lane). Unresolvable assignees stay on `ready` with a `skipped_nonspawnable` event — *not* silently dropped or run by a fallback.
2. **A spawn mechanism** — for Hermes profile lanes, `_default_spawn` runs `hermes -p <assignee> chat -q <prompt>` in the task's pinned workspace with these env vars:

   | Variable | Carries |
   |---|---|
   | `HERMES_KANBAN_TASK` | task id |
   | `HERMES_KANBAN_DB` | absolute path to per-board SQLite file |
   | `HERMES_KANBAN_BOARD` | board slug |
   | `HERMES_KANBAN_WORKSPACES_ROOT` | root of board's workspace tree |
   | `HERMES_KANBAN_WORKSPACE` | absolute path to this task's workspace |
   | `HERMES_KANBAN_RUN_ID` | current run id (lifecycle gate) |
   | `HERMES_KANBAN_CLAIM_LOCK` | claim lock string (`<host>:<pid>:<uuid>`) |
   | `HERMES_PROFILE` | worker's own profile name (comment attribution) |
   | `HERMES_TENANT` | tenant namespace if any |

   Non-Hermes lanes supply their own `spawn_fn` callable (gets `task`, `workspace`, `board`; returns optional pid for crash detection).
3. **A lifecycle terminator** — every claim ends in exactly one of: `kanban_complete` (→done), `kanban_block` (→blocked, respawns on `kanban_unblock`), or process exits without a tool call (kernel reaps → `crashed`/`gave_up`/`timed_out`). A worker that calls neither and exits normally is treated as **crashed**.

### 5.2 Existing lane shapes

- **Hermes profile lane (default)** — assignee is a profile name; dispatcher spawns `hermes -p <profile>`; worker auto-loads the `kanban-worker` skill + `KANBAN_GUIDANCE` system-prompt block. No setup beyond defining the profile. Profile names should match the *role* the orchestrator routes to (discovered via `hermes profile list` — no fixed roster assumed).
- **Orchestrator profile lane** — a profile whose toolset includes `kanban` but *excludes* `terminal`/`file`/`code`/`web`. Its job: decompose a goal into child tasks via `kanban_create` + `kanban_link`, then step back. The `kanban-orchestrator` skill encodes anti-temptation rules.

### 5.3 External CLI worker lanes — NOT a paved path

Wiring a non-Hermes CLI (Codex CLI, Claude Code CLI, OpenCode, local model runner) is **not yet supported as a turnkey path**. `spawn_fn` is a pluggable parameter on `dispatch_once`, and a plugin *could* register its own `spawn_fn` for a non-Hermes assignee — but the surrounding integration work (wrapping CLI exit code into `kanban_complete`/`kanban_block`, mapping workspace/sandbox conventions onto `HERMES_KANBAN_WORKSPACE`, auth, per-CLI policy) is still per-integration design work. Historical refs: issue #19931, closed-not-merged Codex PR #19924.

### 5.4 Review-required convention (layered, not enforced)

The kernel does *not* force code tasks to await review (too fuzzy to define "code-changing task"). Convention layered on top:

- **Block instead of complete**, `reason` prefixed `review-required: ` so the dashboard surfaces it as awaiting review.
- **Drop structured metadata into a `kanban_comment` first** (since `kanban_block` only carries human-readable `reason`). Comments are the durable annotation channel.
- **Reviewer approves & unblocks** (respawns worker w/ comment thread) **or** asks for changes via comment (next run sees it in `kanban_show`).

---

## 6. The Four Tutorial Stories (concrete behavior)

**Story 1 — Solo dev shipping a feature.** Three tasks with parent→child deps (schema → API → tests). Only the root starts `ready`; the rest sit in `todo` until parents complete — the dependency promotion engine. Worker loop: `kanban_show()` → do work via terminal/file tools → `kanban_heartbeat(note=...)` → `kanban_complete(summary=..., metadata={changed_files, decisions})`. When schema hits `done`, API auto-promotes; API worker reads parent's summary+metadata via `kanban_show()` — knows schema decisions without re-reading a design doc. Drawer shows Run History (one attempt, outcome, worker, duration, handoff summary + metadata blob).

**Story 2 — Fleet farming.** Three specialist workers (translator/transcriber/copywriter) + a pile of independent tasks. Create all, `hermes gateway start`, walk away. Filter board to a tenant; In Progress column groups by profile ("Lanes by profile" default). Dispatcher promotes next ready task as each completes; queue drains with no further human input. The simplest use-case and the one the original design optimized for.

**Story 3 — Role pipeline with retry (where Kanban earns its keep).** PM writes spec → engineer implements → reviewer rejects attempt 1 → engineer retries → reviewer approves. PM's `kanban_complete` writes acceptance criteria into metadata; engineer's worker reads it structurally in the parent handoff. Engineer hits review feedback, calls `kanban_block(reason=...)` → run 1 closes `outcome='blocked'`. Human/reviewer reads the block reason, `hermes kanban unblock $IMPL`. Dispatcher respawns backend-dev as a **new run** on the same task; `kanban_show()` now includes run 1's block reason so attempt 2 fixes the *specific* findings instead of re-reading the whole spec. Drawer shows two attempts: Run 1 `blocked`, Run 2 `completed`, each its own `task_runs` row w/ own outcome/summary/metadata.

**Story 4 — Circuit breaker & crash recovery.** Two defense lines:
- **Circuit breaker (permanent-looking failure):** deploy task missing `AWS_ACCESS_KEY_ID`. Dispatcher tries spawn → fails → releases claim → increments failure counter → retries next tick. After N consecutive failures the circuit trips: task → `blocked` with outcome `gave_up`, no more retries until a human unblocks. Run history: `spawn_failed` (retryable) ×2 then `gave_up` (terminal). Event sequence: `created → claimed → spawn_failed → claimed → spawn_failed → claimed → gave_up`. Gateway notification fires on `gave_up` if Telegram/Discord/Slack wired in.
- **Crash recovery (mid-flight death):** spawn succeeds but worker dies (segfault/OOM/`systemctl stop`). Dispatcher polls `kill(pid, 0)`, detects dead pid, releases claim, task → `ready`, next tick gives it to a fresh worker. The retrying worker sees the crash of run 1 in context and picks a safer strategy (e.g., chunked migration); metadata records what changed.

---

## 7. Failure Modes the Dispatcher Handles (so lane authors don't reimplement)

- **Stale claim TTL** — claim-but-never-heartbeat/complete/block gets reclaimed after `DEFAULT_CLAIM_TTL_SECONDS` (15 min default) — **but only if the worker process actually died.** A live worker (slow model spending 20+ min in one tool-free LLM call) gets its claim *extended* instead of killed; only a dead PID is reclaimed.
- **Crashed worker** — vanished host-local PID detected by `detect_crashed_workers`, reaped; `consecutive_failures` increments, may auto-block when breaker trips.
- **Run-level retry** — on retry (post-block/crash/reclaim) a worker can use `expected_run_id` on terminating tools to fail fast if its run was superseded.
- **Per-task max runtime** — `task.max_runtime_seconds` hard-caps wall-clock per run regardless of PID liveness; catches genuinely deadlocked workers the live-PID extension would otherwise keep alive.
- **Stranded-task detection** — a ready task whose assignee never produces a claim within `kanban.stranded_threshold_seconds` (default 30 min) shows in `hermes kanban diagnostics` as `stranded_in_ready`. Severity escalates: error at 2× threshold, critical at 6×. Catches typo'd assignees, deleted profiles, down external pools — identity-agnostic, no per-board allowlist.

### 7.1 ⚠️ Internal contradiction in the source docs

The **overview "Core concepts" section** states the dispatcher auto-blocks after `kanban.failure_limit` consecutive spawn failures with **default: 2**. The **Event reference** `gave_up` row and **Story 4 tutorial** both state the circuit breaker fires after **N = 5** consecutive `spawn_failed` ("Default N = 5; override via `--failure-limit`"), while Story 4 prose also says "After three consecutive failures (the default `failure_limit`)". The docs are internally inconsistent on the circuit-breaker default (2 vs 3 vs 5). **If this matters for a Momentum design decision, verify against the actual Hermes source/config before relying on a specific number.**

---

## 8. Surfaces in Detail

### 8.1 CLI (`hermes kanban …`)

Full verb surface (the human/scripts/cron side; every verb has a `kanban_*` tool equivalent):

`init`, `create` (w/ `--body --assignee --parent --tenant --workspace --priority --triage --idempotency-key --max-runtime --skill --json`), `list`, `show`, `assign`, `link`/`unlink`, `claim`, `comment`, `complete`/`block`/`unblock`/`archive` (bulk — accept multiple ids), `tail` (single task stream), `watch` (board-wide stream, `--kinds` filter), `heartbeat`, `runs` (attempt history), `assignees`, `dispatch` (one-shot pass, `--dry-run --max`), `daemon --force` (**DEPRECATED** — use gateway), `stats`, `log`, `notify-subscribe`/`notify-list`/`notify-unsubscribe`, `context` (what a worker sees), `specify` (flesh out a triage idea, `--all`), `gc` (workspaces + old events + logs), `boards` (`list/create/switch/show/rename/rm`).

- **Idempotent create** — `--idempotency-key` makes repeat calls return the existing id instead of duplicating (for automation/webhooks).
- **Gateway-embedded dispatcher (default)** — runs inside the gateway; `kanban.dispatch_in_gateway: true`, `dispatch_interval_seconds: 60`. Standalone `hermes kanban daemon` is deprecated; running both against one DB causes claim races (unsupported).

### 8.2 `/kanban` slash command

Every `hermes kanban <action>` is reachable as `/kanban <action>` from interactive `hermes chat` **and** any gateway platform (Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost, email, SMS). Same `run_slash()` entry point reusing the same argparse tree → identical surface across all three.

**Mid-run exemption:** the gateway normally queues slash commands while an agent is thinking. `/kanban` is *explicitly exempted* — the board lives in SQLite, not agent state, so reads and writes go through immediately even mid-turn. This enables: unblock a peer from your phone while the blocked worker isn't interrupted; drop human context into a task thread the next run will read; inspect the fleet without stopping the orchestrator.

**Auto-subscribe:** `/kanban create` from a gateway auto-subscribes the originating chat to that task's terminal events (`completed/blocked/gave_up/crashed/timed_out`) — one message per terminal event incl. first line of result summary. Auto-removes on `done`/`archived`. Skipped if `--json` (scripted callers manage subscriptions explicitly).

**Output truncation:** gateway messaging caps ~3800 chars with a truncation footer; CLI has no cap.

### 8.3 Dashboard GUI (bundled plugin, not core)

Shipped as bundled dashboard plugin at `plugins/kanban/` (~700 lines Python, thin wrapper, no new business logic). `hermes dashboard` → "Kanban" tab.

- One column per status; `triage` is the parking column for rough ideas.
- Cards: id, title, priority badge, tenant tag, assigned profile, comment/link counts, progress pill (N/M children done), age, multi-select checkbox.
- Per-profile lanes inside Running (toolbar toggle).
- **Live updates via WebSocket** tailing the append-only `task_events` table; debounced burst reload.
- **Drag-drop** between columns → `PATCH /api/plugins/kanban/tasks/:id` through the same `kanban_db` code as CLI; destructive moves confirm.
- **Inline create**, **multi-select bulk actions** (status/archive/reassign, per-id partial failures reported), **side drawer** (editable title/assignee/priority/description, dependency editor w/ cycle rejection, status action row, **✨ Specify** button for triage cards, result section, comment thread, last 20 events).
- **Triage Specifier:** auxiliary LLM (`auxiliary.triage_specifier` in config.yaml) turns a one-liner into a full spec (goal, approach, acceptance criteria) and promotes `triage → todo`. Reachable from CLI (`hermes kanban specify <id>` / `--all`), `/kanban specify`, and `POST /api/plugins/kanban/tasks/:id/specify`.

**Architecture:** strictly read-through-the-DB + write-through-`kanban_db` (React SPA → FastAPI router → shared WAL SQLite, WebSocket tails `task_events`).

**Security model (important):** the dashboard auth middleware *explicitly skips `/api/plugins/`* — plugin routes are **unauthenticated by design** (dashboard binds localhost). The kanban REST surface is reachable from **any process on the host**. The WebSocket additionally requires the ephemeral session token as `?token=`. `hermes dashboard --host 0.0.0.0` exposes the entire collaboration surface (task bodies, comments, workspace paths, create/reassign/archive) to the network — **explicitly warned against on shared hosts**. The board is profile-agnostic on purpose (the coordination primitive) — opening as one profile still shows all profiles' tasks.

---

## 9. Boards (multi-project) & Tenancy

- New install = exactly one board `default` (DB at `~/.hermes/kanban.db` for back-compat); boards are opt-in, hidden until they matter.
- **Per-board isolation is absolute:** separate SQLite DB, `workspaces/`, `logs/`; workers see *only* their board's tasks (`HERMES_KANBAN_BOARD` pinned in child env); cross-board links disallowed.
- Board resolution precedence: explicit `--board` > `HERMES_KANBAN_BOARD` env > `~/.hermes/kanban/current` (persisted by `boards switch`) > `default`.
- Slugs validated: lowercase alnum + hyphen + underscore, 1–64 chars, must start alphanumeric; slashes/spaces/dots/`..` rejected (path-traversal defense).
- Dashboard board switcher persists selection in browser `localStorage` (doesn't shift the CLI `current` pointer).
- **Tenants** = soft filter *within* a board for one fleet serving multiple businesses; isolation by workspace path + memory key prefix. Boards = hard boundary, tenants = soft.

---

## 10. Event Vocabulary

Every transition appends a `task_events` row (optional `run_id` for grouping). Three clusters:

**Lifecycle:** `created`, `promoted` (todo→ready, all parents done), `claimed`, `completed`, `blocked`, `unblocked`, `archived`.

**Edits:** `assigned`, `edited`, `reprioritized`, `status` (dashboard drag-drop direct write).

**Worker telemetry:** `spawned` (pid), `heartbeat`, `reclaimed` (TTL expired), `crashed` (pid gone, TTL not yet expired), `timed_out` (max_runtime exceeded — SIGTERM then SIGKILL after 5s grace), `spawn_failed` (one attempt failed, counter increments), `gave_up` (circuit breaker fired — see §7.1 re: default N).

`hermes kanban tail <id>` = single-task stream; `hermes kanban watch` = board-wide stream with `--kinds` filter.

---

## 11. Collaboration Patterns (no new primitives needed)

| Pattern | Shape | Example |
|---|---|---|
| P1 Fan-out | N siblings, same role | research 5 angles in parallel |
| P2 Pipeline | role chain scout→editor→writer | daily brief assembly |
| P3 Voting/quorum | N siblings + 1 aggregator | 3 researchers → 1 reviewer picks |
| P4 Long-running journal | same profile + shared dir + cron | Obsidian vault |
| P5 Human-in-loop | worker blocks → user comments → unblock | ambiguous decisions |
| P6 @mention | inline routing from prose | `@reviewer look at this` |
| P7 Thread-scoped workspace | `/kanban here` in a thread | per-project gateway threads |
| P8 Fleet farming | one profile, N subjects | 50 social accounts |
| P9 Triage specifier | rough idea → triage → `specify` → todo | one-liner → spec'd task |

---

## 12. Scope Boundaries (explicit non-goals)

- **Single-host only.** `~/.hermes/kanban.db` is a local SQLite file; dispatcher spawns workers on the same machine. No multi-host coordination primitive; crash detection assumes host-local PIDs. For multi-host: independent board per host + `delegate_task`/a message queue to bridge.
- **GUI is deliberately thin** — everything the plugin does is reachable from CLI. Auto-assignment, budgets, governance gates, org-chart views remain user-space (a router profile, another plugin, `tools/approval.py`).
- Full design rationale, concurrency-correctness proofs, comparative analysis (vs Cline Kanban / Paperclip / NanoClaw / Google Gemini Enterprise), eight canonical patterns: `docs/hermes-kanban-v1-spec.pdf` in the Hermes repo (not fetched here).

---

## 13. Relevance to Momentum (observations, not recommendations)

This is filed alongside `beads-vs-momentum-tracker-evaluation` and `background-agent-coordination` because Hermes Kanban is a close analog to Momentum's sprint-dev / dispatch / worktree model. Salient parallels and contrasts:

| Concern | Hermes Kanban | Momentum (current model) |
|---|---|---|
| Task store | SQLite `kanban.db`, per-board | JSON indexes (`stories/index.json`, `sprints/index.json`) |
| Worker identity | Named Hermes profile, full OS process | Spawned `momentum:dev*` agents per story |
| Dependency engine | `task_links`, auto-promote todo→ready when parents done | Sprint-dev dependency-driven story ordering |
| Handoff channel | Per-run `summary` + `metadata` in `kanban_show` context | Story spec + AVFL findings + commit history |
| Retry representation | First-class `task_runs` rows; prior attempts in worker context | Re-spawn / quick-fix; less structured attempt history |
| Human-in-loop | `kanban_block` → human comment → `unblock` | Team review phase, e2e-validator, qa-reviewer |
| Two-surface split | Model=tools, human=CLI, one DB layer | Skills/agents vs human commands; index files as shared state |
| Failure handling | Circuit breaker, crash detection, stale-claim TTL, stranded detection | Less formalized; AVFL post-merge catches content issues |

**Ideas worth a closer look** (flagged for the developer — not adopted):

1. **Per-run attempt history as the primary representation** (not "latest state + afterthought"). Momentum's story model could benefit from first-class run rows so a retrying dev agent sees *why* the prior attempt failed without re-deriving it. Cf. `feedback_spikes_as_stories` and the AVFL post-merge strategy.
2. **Structured handoff metadata** (`changed_files`, `verification`, `residual_risk`) as a machine-readable downstream-worker contract — analogous to but more formalized than Momentum's spec-driven handoff.
3. **The two-surface invariant** (model talks tools, human talks CLI, both through one consistency layer) — directly relevant to Momentum's "exclusive write authority per file" principle (`feedback_impetus_orchestration_model`).
4. **Stranded-task detection with escalating severity** — a drift signal Momentum's refine/sprint-manager could borrow for stale-story triage.
5. **The "review-required" block convention** — a lightweight, non-enforced pattern that maps onto Momentum's team-review phase without rigid kernel rules.

---

## 14. Open Questions / Limits of This Discovery

- The circuit-breaker default is **internally contradictory in the source** (2 vs 3 vs 5 — §7.1). Unresolved without the Hermes source/config.
- No external triangulation (Gemini) or AVFL validation was run per the lightweight-research request — behavioral specifics are "as documented," not independently verified.
- The v1 design spec PDF (`docs/hermes-kanban-v1-spec.pdf`) was not fetched — concurrency-correctness reasoning, the full comparative analysis, and worked examples of all 8 patterns are not covered here.
- External CLI worker lanes (Codex/Claude Code/OpenCode) are documented as *not a paved path*; any Momentum-Hermes bridge would be net-new integration work.
