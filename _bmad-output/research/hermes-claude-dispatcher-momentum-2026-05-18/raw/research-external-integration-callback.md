---
content_origin: claude-code-subagent
date: 2026-05-18
sub_question: "What is Hermes's external integration and callback surface, and is it local-capable?"
topic: "Can Hermes run as a 24/7 dispatcher/delegate with Claude Code as planner/brains, and can Hermes Kanban + worker lanes map onto Momentum?"
---

# Hermes External Integration & Callback Surface — Is It Local-Capable?

## Scope and Bottom Line

This investigates whether an external system (Claude Code) can (a) hand work *into* Hermes programmatically and (b) receive callbacks *out* of Hermes on significant state change or completion, and whether any of it works with **no external network beyond model inference**. Documentation reviewed on 2026-05-18 from the Hermes docs site; all pages are current (the docs are "generated fresh on every deploy" [OFFICIAL — docs index]).

**Headline finding:** Hermes exposes a rich, mostly-local integration surface. The single strongest *event-IN* primitive for Claude Code is the **API Server's Runs API** (`POST /v1/runs` + `GET /v1/runs/{id}/events` SSE) — it binds to `127.0.0.1` by default and the entire transport is local; only model inference traverses the network [OFFICIAL]. For *event-OUT* (Hermes calling back to Claude Code), there is **no built-in outbound webhook/event-bus to an arbitrary local consumer** — but **gateway hooks and plugin/shell hooks** can run arbitrary local code on lifecycle events (including `agent:end`, `subagent_stop`, completion), which is a fully-local, code-level callback that can append to a queue, write a FIFO, or hit a local socket [OFFICIAL]. The webhook adapter is *inbound-only* by design (it receives, it does not emit) [OFFICIAL]. Kanban's external-worker lane for a non-Hermes CLI like Claude Code is explicitly **not a paved path** [OFFICIAL].

## Event-IN: Getting Work Into Hermes Programmatically

Hermes has four distinct programmatic ingress mechanisms. All four are local-capable.

### 1. API Server — Runs API and Jobs API (the primary candidate)

The API Server exposes Hermes as an OpenAI-compatible HTTP endpoint, but it also has two non-OpenAI surfaces purpose-built for orchestrators [OFFICIAL — API Server].

**Runs API (streaming-friendly async run submission):**
- `POST /v1/runs` — create an agent run; accepts a simple `input` string plus optional `session_id`, `instructions`, `conversation_history`, or `previous_response_id`. Returns `{"run_id": "run_abc123", "status": "started"}` [OFFICIAL].
- `GET /v1/runs/{run_id}` — poll run state; returns `{"object": "hermes.run", "run_id": ..., "status": "completed", "session_id": ..., "output": "Done.", "usage": {...}}`. Terminal statuses (`completed`, `failed`, `cancelled`) are retained briefly for polling/reconciliation [OFFICIAL].
- `GET /v1/runs/{run_id}/events` — **Server-Sent Events stream** of tool-call progress, token deltas, and lifecycle events. "Designed for dashboards and thick clients that want to attach/detach without losing state" [OFFICIAL].
- `POST /v1/runs/{run_id}/stop` — interrupt a running turn; returns `{"status": "stopping"}` [OFFICIAL].
- `GET /v1/capabilities` — machine-readable feature discovery returning `run_submission`, `run_status`, `run_events_sse`, `run_stop` booleans, "so they can discover whether the running Hermes version supports runs, streaming, cancellation, and session continuity without depending on private Python internals" [OFFICIAL].

This is the cleanest event-IN/event-OUT pair Hermes offers: Claude Code POSTs a run (event-IN), then either polls `GET /v1/runs/{id}` or subscribes to the SSE event stream (event-OUT for *that run*). The SSE stream is request-scoped — it is a callback channel for a run Claude Code itself started, not an unsolicited push for arbitrary state changes.

**Jobs API (background scheduled work CRUD):**
- `GET/POST /api/jobs`, `GET/PATCH/DELETE /api/jobs/{job_id}`, `POST /api/jobs/{job_id}/pause|resume|run`. "Body accepts the same shape as `hermes cron` — prompt, schedule, skills, provider override, delivery target." `POST /api/jobs/{job_id}/run` triggers an immediate out-of-schedule run [OFFICIAL]. This lets Claude Code register/trigger recurring or one-shot Hermes work over HTTP.

**Locality and auth:** `API_SERVER_HOST` defaults to `127.0.0.1` ("localhost only by default") [OFFICIAL]. Auth is a bearer token via `API_SERVER_KEY` (env var only; "config.yaml support coming in a future release") [OFFICIAL]. When bound to a non-loopback address, the key is *required*; CORS is off by default [OFFICIAL]. Enable with `API_SERVER_ENABLED=true`, `API_SERVER_PORT` (default `8642`) [OFFICIAL]. **Verdict: fully local-capable, no external network in the transport path.** Server-to-server callers (Claude Code on the same host) need no CORS [OFFICIAL]. An `Idempotency-Key` request header is supported (responses cached by key for 5 minutes) [OFFICIAL] — relevant for safe retry from a dispatcher.

One caveat flagged: the docs note stored responses (for `previous_response_id`) cap at 100 with LRU eviction [OFFICIAL]; the Runs API is the better surface for a sustained dispatcher because it does not depend on that store.

### 2. Webhook Adapter — Inbound HTTP Events

The webhook adapter "runs an HTTP server that accepts POST requests, validates HMAC signatures, transforms payloads into agent prompts, and routes responses" [OFFICIAL — Webhooks]. This is *event-IN only* — it accepts external events and turns them into agent runs.

- Enable: `WEBHOOK_ENABLED=true`, `WEBHOOK_PORT` (default `8644`), `WEBHOOK_SECRET` [OFFICIAL].
- Routes are defined in `config.yaml` under `platforms.webhook.extra.routes` **or** created dynamically via `hermes webhook subscribe <name> --events ... --prompt ... --deliver ...` (stored in `~/.hermes/webhook_subscriptions.json`, hot-reloaded on each request, no gateway restart) [OFFICIAL].
- A route has `events`, `secret` (HMAC, required), `prompt` (dot-notation template like `{pull_request.title}`, or `{__raw__}` to dump the whole payload), optional `skills`, and `deliver` [OFFICIAL].
- Auth: HMAC-SHA256 (`X-Hub-Signature-256` GitHub-style, `X-Webhook-Signature` generic, or GitLab plain-token `X-Gitlab-Token`). A secret is mandatory; `INSECURE_NO_AUTH` is accepted **only when bound to loopback** (`127.0.0.1`/`localhost`/`::1`) — it refuses to start if combined with `0.0.0.0` [OFFICIAL]. Rate-limited 30 req/min/route default; 1 MB body cap; idempotency by `X-GitHub-Delivery`/`X-Request-ID` cached 1 hour [OFFICIAL].

**`deliver_only: true` (Direct Delivery Mode):** the rendered template becomes the literal delivered message, **the agent is never invoked, zero LLM tokens, sub-second, synchronous `200 OK`** on delivery success or `502` on target rejection [OFFICIAL]. Relevant because it makes the webhook adapter usable as a pure local message relay between processes without burning inference — explicitly cited use case: "Inter-agent pings — Agent A notifies Agent B's user that a long-running task finished" [OFFICIAL].

**Locality:** the webhook server is a local HTTP listener; binding to `127.0.0.1` keeps it fully local. Claude Code could `curl -X POST localhost:8644/webhooks/<route>` with an HMAC signature to inject work. **Verdict: local-capable event-IN.** Prompt-injection warning applies — webhook payloads are attacker-controlled when exposed [OFFICIAL]; for a local Claude→Hermes bridge this is a trusted-local channel.

### 3. CLI — One-Shot and Gateway Invocation

`hermes -z "<prompt>"` is "the purest one-shot entry point: single prompt in, final response text out, nothing else on stdout or stderr" — no banner, spinner, or `Session:` line [OFFICIAL — CLI commands]. `-Q/--quiet` is the programmatic-mode flag. `--source tool` tags the session so third-party-integration runs don't pollute user session lists [OFFICIAL]. `--ignore-user-config` + `--ignore-rules` give a fully isolated run for "third-party integrations" [OFFICIAL]. Other relevant CLI surfaces: `hermes cron create ...`, `hermes kanban create ...`, `hermes webhook subscribe ...`. **Verdict: fully local event-IN** — Claude Code shells out to `hermes -z` exactly as it would `claude -p`. Each invocation is a fresh process (spawn-cost applies, analogous to the ~12 s Claude Code figure from the prior dispatcher research [PRAC — cross-report]).

### 4. Python Library — Embedded `AIAgent`

`pip install git+...hermes-agent`; `from run_agent import AIAgent; agent.chat(...)` or `agent.run_conversation(user_message=..., conversation_history=...)` returns `{"final_response": ..., "messages": [...]}` [OFFICIAL — Python Library]. In-process, no network in the orchestration path (only provider inference). Not directly relevant to a Claude-Code-as-planner topology (Claude Code is not a Python host for Hermes), but it confirms the agent core is library-embeddable and fully local. **Verdict: local, but topology-mismatched for this use case.**

## Event-OUT: Hermes Calling Back on Significant Change

This is the weaker half of the surface. Hermes has **no built-in outbound webhook emitter to an arbitrary local URL**, no event bus, no pub/sub, and no `hermes events`/`subscribe`/`listen` command. What it does have is **hooks** — local code that runs on lifecycle events and can do *anything*, including calling back to Claude Code's local ingress.

### Hooks — Three Systems, All Local Code

Hermes has three hook systems [OFFICIAL — Hooks]:

1. **Gateway hooks** (`~/.hermes/hooks/<name>/HOOK.yaml` + `handler.py`) — fire during gateway operation only. Subscribable events: `gateway:startup`, `session:start`, `session:end`, `session:reset`, `agent:start`, `agent:step` (each tool-loop iteration, with `iteration` and `tool_names`), **`agent:end`** (with `message` and `response`), `command:*` [OFFICIAL]. The `agent:end` event is the natural "Hermes finished, notify Claude Code" callback point. The docs literally show a "Session Start Webhook" example that `httpx.post(WEBHOOK_URL, json={...})` to an external service [OFFICIAL] — the same pattern works to POST into Claude Code's local Channel server / queue.
2. **Plugin hooks** (`ctx.register_hook(...)`) — fire in **both CLI and gateway**. Includes **`subagent_stop`** (fires once per `delegate_task` child with `child_status` ∈ `completed|failed|interrupted|error`, `child_summary`, `duration_ms`) [OFFICIAL], `post_llm_call` (per successful turn, with `assistant_response`), `on_session_end` (`completed`/`interrupted` flags), `post_tool_call`, plus transform hooks. `post_llm_call`'s documented use case is explicitly "triggering follow-up actions" [OFFICIAL].
3. **Shell hooks** (`hooks:` block in `config.yaml` pointing at any executable) — fire in CLI + gateway, JSON payload on **stdin**, optional JSON on **stdout**. Worked example #4 logs every `subagent_stop` to a file [OFFICIAL]. A shell hook on `agent:end`/`subagent_stop`/`post_llm_call` that appends to a JSONL queue or writes a FIFO **is the local event-OUT bridge** — directly analogous to the beads `.beads/hooks/on_update` exec-hook pattern the prior dispatcher research recommends [PRAC — cross-report, beads addendum].

**Critical limitation:** gateway hooks "only fire in the gateway (Telegram, Discord, Slack, WhatsApp, Teams). The CLI does not load gateway hooks" [OFFICIAL]. So `agent:end` callback requires Hermes running as a **gateway** (long-lived), not per-`hermes -z` invocation. Plugin/shell hooks fire in CLI too, so for a `hermes -z`-per-task topology the callback must use a *plugin or shell* hook on `on_session_end`/`post_llm_call`, not a gateway hook. All hooks are non-blocking and best-effort — "errors in any hook are caught and logged, never crashing the agent" [OFFICIAL] — meaning **callback delivery is lossy and unacknowledged**; the consumer must reconcile, mirroring the lossy-delivery caveat in the prior research [PRAC — cross-report].

### Webhook `deliver` Targets — Not a Claude-Code Callback

The webhook adapter's `deliver` field routes the agent's *response* to a target, but the enumerated targets are messaging platforms (`telegram`, `discord`, `slack`, ...), `github_comment`, or `log` [OFFICIAL]. **There is no `deliver: http`/`deliver: webhook`/`deliver: command` target** — so a webhook-triggered run cannot natively POST its result back to Claude Code's local endpoint. The callback path *must* be a hook (or the agent itself calling a tool that writes locally). This is the sharpest gap for the Claude-Code-as-planner topology: Hermes accepts work cleanly but does not natively *push* completion to an arbitrary local consumer; you must instrument it with a hook.

### Cron — Scheduled, Delivers to Chat/Files/Platforms

Cron jobs "deliver results back to the origin chat, local files, or configured platform targets" [OFFICIAL — Cron]. "Local files" delivery is a usable local event-OUT sink — a cron job could write results to a file Claude Code's watcher consumes. No-agent mode runs "a script on a schedule, its stdout delivered verbatim, zero LLM involvement" [OFFICIAL]. Cron is event-IN (scheduled trigger) with a file/platform event-OUT. Local-capable. Not a *reactive* callback (it's wall-clock, not state-change), so secondary to hooks for "signal on significant change."

## MCP and ACP

**MCP:** Hermes is an MCP *client/consumer*, not an MCP server. It connects *out* to MCP servers (stdio local subprocess or remote HTTP) to gain tools [OFFICIAL — MCP]. There is **no documented "Hermes as MCP server" mode** that would let Claude Code drive Hermes via MCP, and the agent always *pulls* MCP tools — no server-push/notifications/subscriptions surface for MCP. Direction is inverted from what this topic needs. Local-capable (stdio servers run as local subprocesses) but not an ingress/callback channel for Claude Code. *(This mirrors the beads-MCP finding in the prior research: MCP here is pull-only request/response [PRAC — cross-report].)*

**ACP (Agent Context Protocol):** Hermes runs as an **ACP server over stdio** for editors (VS Code, Zed, JetBrains) — `hermes acp` / `hermes-acp` [OFFICIAL — ACP]. ACP is bidirectional over stdio (chat, tool activity, diffs, approval prompts, streamed chunks) and fully local (stdio, no network). In principle an ACP client could drive Hermes as an editor-native agent, but ACP is editor-UX-shaped (it excludes messaging/cron) and is not a task-queue/callback API. For a Claude-Code-as-planner topology it is a theoretically-local but awkward fit versus the Runs API. Local-capable: yes.

## Is the Dispatcher / Kanban Local? Yes — Aggressively So

The Kanban board is "a durable, single-host task board" — every task is a row in a local SQLite DB (`~/.hermes/kanban.db`), the dispatcher spawns workers on the same machine, and crash detection assumes host-local PIDs [OFFICIAL — Kanban, corroborated by prior discovery]. The dispatcher runs **inside the gateway** by default (`kanban.dispatch_in_gateway: true`, 60 s tick) [OFFICIAL — prior discovery §8.1]. Worker env (`HERMES_KANBAN_DB`, `HERMES_KANBAN_BOARD`, `HERMES_KANBAN_WORKSPACE`, etc.) points at local paths [OFFICIAL]. Logs go to `<board-root>/logs/<task_id>.log` [OFFICIAL — worker-lanes]. **No external network is involved in the board, dispatcher, or worker spawn — only model inference.** This is the strongest locality story in the entire surface.

**External-worker lane for Claude Code: not a paved path.** "Wiring a non-Hermes CLI tool (Codex CLI, Claude Code CLI, OpenCode CLI, a local coding-model runner, etc.) as a kanban worker lane is *not yet a paved path*" [OFFICIAL — worker-lanes]. The dispatcher's `spawn_fn` is a pluggable parameter and a plugin "could register its own `spawn_fn` for a non-Hermes assignee," but "wrapping the CLI's exit code into `kanban_complete` / `kanban_block` calls, mapping the CLI's workspace/sandbox conventions onto `HERMES_KANBAN_WORKSPACE`, handling auth and per-CLI policy — is still per-integration design work" [OFFICIAL]. There is a *mention* of "non-Hermes external workers, via the API" but **no REST endpoints/paths/payloads for kanban are documented** — the kanban tool surface (`kanban_complete`, `kanban_block`, etc.) is an in-process Python toolset for Hermes-spawned workers, not an HTTP API [OFFICIAL — worker-lanes, corroborated by prior discovery §2/§5.3]. Kanban state changes emit `task_events` rows (`promoted`, `claimed`, `completed`, `blocked`, `gave_up`, `crashed`, `timed_out`, `reclaimed`) **queryable from SQLite** — but there are **no kanban webhooks/queues/push notifications**; `hermes kanban tail`/`watch` are local CLI streams reading the events table [OFFICIAL — worker-lanes, prior discovery §10]. Gateway notifications (Telegram/Discord/Slack) fire on terminal events *if a messaging platform is wired in* [OFFICIAL — prior discovery §2.2/§7], but that is a messaging-platform callback, not a local-process callback to Claude Code.

## Mechanism Map: IN / OUT / Local

| Mechanism | Direction | Protocol | Local-capable | Auth |
|---|---|---|---|---|
| API Server `POST /v1/runs` | event-IN | HTTP (`127.0.0.1:8642`) | **Yes** | Bearer (`API_SERVER_KEY`) |
| API Server `GET /v1/runs/{id}/events` (SSE) | event-OUT (run-scoped) | HTTP SSE | **Yes** | Bearer |
| API Server `GET /v1/runs/{id}` (poll) | event-OUT (run-scoped) | HTTP | **Yes** | Bearer |
| API Server `POST /v1/runs/{id}/stop` | control-IN | HTTP | **Yes** | Bearer |
| API Server Jobs API (`/api/jobs*`) | event-IN (schedule/trigger) | HTTP | **Yes** | Bearer |
| Webhook adapter (`POST /webhooks/<route>`) | event-IN | HTTP (`8644`) | **Yes** | HMAC-SHA256 |
| Webhook `deliver_only` | event-OUT (to messaging targets only) | HTTP→platform | Yes (to local platforms) | HMAC (inbound) |
| CLI `hermes -z` | event-IN | process spawn | **Yes** | OS/process |
| Python `AIAgent` | event-IN (in-proc) | Python import | **Yes** | env keys |
| Gateway hooks (`agent:end` etc.) | event-OUT (code) | local code (gateway only) | **Yes** | filesystem trust |
| Plugin/shell hooks (`subagent_stop`, `post_llm_call`, `on_session_end`) | event-OUT (code) | local code (CLI+gateway) | **Yes** | consent allowlist |
| Cron (deliver to local file) | both | scheduler + file | **Yes** | OS/process |
| MCP (Hermes as client) | neither (inverted) | stdio/HTTP | Yes | per-server |
| ACP (Hermes as server) | both (editor-shaped) | stdio | **Yes** | stdio/process |
| Kanban board/dispatcher | internal | SQLite + local spawn | **Yes** | local FS |
| Kanban external worker lane (Claude Code) | — | **not a paved path** | (would be local) | per-integration |

## Implications for the Claude-Code-as-Planner Topology

Concretely, the lowest-friction local bridge is: **Claude Code (planner) → `POST http://127.0.0.1:8642/v1/runs` with a bearer token → Hermes runs the task → Claude Code subscribes to `GET /v1/runs/{id}/events` (SSE) or polls `GET /v1/runs/{id}`.** This is a request/response-with-progress pattern, entirely local, with idempotency-key retry safety. It does *not* require Hermes to be a gateway and does not need the Kanban layer at all.

If the requirement is *unsolicited* callback on significant change (not tied to a run Claude Code started — e.g., a Hermes cron job or kanban worker finished autonomously), the only local mechanism is a **hook that writes into Claude Code's local ingress** (the Channel server / `intake-queue.jsonl` / FIFO from the prior dispatcher research [PRAC — cross-report §3/§4]). A gateway hook on `agent:end` or a shell hook on `subagent_stop`/`on_session_end` POSTs/appends locally. This is symmetric with the recommended beads `on_update` exec-hook ingress and shares its hazards: lossy fire-and-forget delivery (reconcile on startup), self-trigger risk if Hermes acts on Claude Code's writes, and the gateway-only constraint on `agent:*` events. There is **no native Hermes outbound webhook** to spare you writing that hook.

The Kanban-as-Momentum-mapping question is constrained by the explicit "external CLI worker lane is not a paved path" finding: routing Momentum stories to Claude Code *through Hermes Kanban* is net-new `spawn_fn`-plugin integration work, not configuration — consistent with the prior discovery's §5.3 and §13 observations. The locality is excellent (SQLite, local spawn, no network) but the Claude-Code worker bridge does not exist off the shelf.

## Confidence and Caveats

- API Server Runs/Jobs API, webhook adapter, hooks, MCP/ACP direction, and Kanban locality are all **[OFFICIAL]** — sourced directly from current Hermes docs (2026-05-18, generated per-deploy).
- The absence of a native outbound-webhook-to-arbitrary-URL is inferred from the *enumerated* `deliver` targets and the absence of any documented emitter — strong but negative-evidence; flagged as a documentation-scope conclusion, not a source-read of code.
- "config.yaml support coming in a future release" for API Server keys means current config is env-var-only [OFFICIAL] — pin behavior to the installed version before building.
- The Runs API SSE event vocabulary is described generically ("tool-call progress, token deltas, and lifecycle events") without an enumerated event-type list [OFFICIAL]; exact terminal-event payload shape should be verified empirically against the installed Hermes version before a dispatcher depends on a specific field.
- Kanban "via the API" for non-Hermes workers is mentioned but undocumented [OFFICIAL — worker-lanes]; treat as nonexistent until proven against source.

## Sources

- [API Server — Hermes Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server) (Runs API, Jobs API, `/v1/capabilities`, auth, locality) — retrieved 2026-05-18
- [Webhooks — Hermes Docs](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks) (routes, HMAC, `deliver`, `deliver_only`, dynamic subscriptions, env vars) — retrieved 2026-05-18
- [Hooks — Hermes Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) (gateway/plugin/shell hooks, event list, `subagent_stop`, `agent:end`, JSON wire protocol) — retrieved 2026-05-18
- [MCP — Hermes Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) (Hermes-as-client, stdio/HTTP servers) — retrieved 2026-05-18
- [ACP — Hermes Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/acp) (Hermes-as-ACP-server over stdio) — retrieved 2026-05-18
- [Cron Jobs — Hermes Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) (delivery targets, no-agent mode) — retrieved 2026-05-18
- [Delegation — Hermes Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation) (`delegate_task` in-process RPC) — retrieved 2026-05-18
- [Use Hermes as a Python Library — Hermes Docs](https://hermes-agent.nousresearch.com/docs/guides/python-library) (`AIAgent`, `run_conversation`) — retrieved 2026-05-18
- [CLI Commands Reference — Hermes Docs](https://hermes-agent.nousresearch.com/docs/reference/cli-commands) (`hermes -z`, `hermes gateway`, `hermes webhook`, `hermes kanban`, `hermes cron`) — retrieved 2026-05-18
- [Kanban Worker Lanes — Hermes Docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-worker-lanes) (non-Hermes lane "not a paved path", `spawn_fn`, `task_events`, locality) — retrieved 2026-05-18
- [Gateway Internals — Hermes Docs](https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-internals) (adapter list incl. `api_server.py`, `webhook.py`; SQLite session store) — retrieved 2026-05-18
- [Hermes Docs index + llms.txt](https://hermes-agent.nousresearch.com/docs) (doc freshness, integration inventory) — retrieved 2026-05-18
- Prior art (cross-report, tagged [PRAC]): `/Users/steve/projects/momentum/docs/research/hermes-kanban-discovery-2026-05-17.md`; `/Users/steve/projects/momentum/docs/research/claude-code-background-dispatcher-2026-05-17.md` (§3 Channels, §4 local patterns, beads exec-hook addendum)
