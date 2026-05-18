---
title: "Claude Code background dispatcher — can it handle or generate events to fire off agents/skills? — Research Report"
date: 2026-05-17
type: Technical Research — Consolidated Report
status: Complete
content_origin: claude-code-synthesis
human_verified: false
derives_from:
  - path: raw/research-hooks-event-dispatch.md
    relationship: synthesized_from
  - path: raw/research-scheduled-background-execution.md
    relationship: synthesized_from
  - path: raw/research-trigger-event-emission.md
    relationship: synthesized_from
  - path: raw/research-local-dispatcher-patterns.md
    relationship: synthesized_from
  - path: raw/cost-max-coverage-billing.md
    relationship: synthesized_from
  - path: raw/cost-automation-usage-policy.md
    relationship: synthesized_from
  - path: raw/beads-event-surface.md
    relationship: synthesized_from
  - path: spike-channel-push-sufficiency-2026-05-17.md
    relationship: validated_by
---

# Claude Code background dispatcher — can it handle or generate events to fire off agents/skills? — Research Report

## Executive Summary

**Verdict: Yes — a local, autonomous, event-driven background dispatcher that fires Claude Code agents/skills can be built today, with no external network systems beyond Claude's own model inference call. But not from a single built-in primitive.** Claude Code ships no native daemon, no filesystem-watch trigger, and no cross-session event bus — Anthropic explicitly closed the native "watch + wake" request as *not planned* ([anthropics/claude-code #28229](https://github.com/anthropics/claude-code/issues/28229)) (CITED). Every working pattern is **external orchestration wrapping the headless runtime**: a long-lived process hosting the Agent SDK in streaming-input mode (or a loop around `claude -p`), fed by a local event source (your `intake-queue.jsonl`, a SQLite cursor, a FIFO, or a filesystem watcher), with hooks closing the loop by appending follow-up events back into that store. All transport, queue, and state stay on the machine; only LLM inference traverses the network.

The four mechanism families each contribute a layer, not a complete solution. **Hooks** are a strong in-session *trigger surface and side-effect emitter* — they react (block/allow/inject) and emit (append to a file/DB/socket, shell out to `claude -p`), but only fire inside a live session and cannot be an autonomous loop by themselves. **Scheduled/background execution** (`/loop`, `ScheduleWakeup`/Snooze, `run_in_background`, `Monitor`, `/goal`) gives state-reactive autonomy but is session-scoped and not durable across restarts; only headless `claude -p` under an OS scheduler is fully local *and* survives with no open Claude process. **Trigger/event-emission primitives** split cleanly: the Agent SDK streaming-input loop and local Channels are fully local; Routines/RemoteTrigger and PushNotification are Anthropic-cloud-bound and disqualified for the local-only constraint. **Local dispatcher patterns** — file watchers, SQLite/JSONL queues, FIFOs, Unix sockets, OS schedulers — are the proven glue and are all local.

This report is for an engineer deciding whether to build a local autonomous dispatcher around an existing event log. The recommended architecture (Section 5 / Recommendations) is a **single long-lived Agent SDK daemon blocked on the local queue**, with hooks emitting follow-up events back and an OS scheduler as a liveness watchdog. The decisive constraints to design around: amortizing the ~12 s per-process spawn cost, the no-open-session limitation, permission flags for unattended runs, and self-trigger loop guards.

One contradiction across the raw sources is flagged explicitly in Section 6: whether headless `claude -p` can fire `/slash`-style skills (it cannot directly, with `/goal` as the one documented exception).

---

## 1. Hooks — Lifecycle Events, Dispatch, and Event Emission

**The hook surface is large and dispatcher-relevant, but every event requires a live session.** The 2026 lifecycle has expanded to roughly **29 events**, up from the original ~8 ([Hooks reference](https://code.claude.com/docs/en/hooks)) (VERIFIED); community trackers corroborate the growth with `InstructionsLoaded`, `ConfigChange`, `WorktreeCreate/Remove`, `PostCompact`, and `Elicitation` added ([SmartScope, March 2026](https://smartscope.blog/en/generative-ai/claude/claude-code-hooks-guide/)) (CITED). Two events matter most for a dispatcher:

- **`FileChanged`** — fires when a watched file changes on disk. This is the closest native filesystem-event source and the natural inbound trigger for a queue-file-driven dispatcher — *but it only fires while a session is live*.
- **`Notification`** — fires on `idle_prompt`, `permission_prompt`, etc.

Other dispatcher-useful events: `Stop` / `SubagentStop` (turn finished → dispatch next), `PostToolUse` / `PostToolUseFailure`, `TaskCompleted`, `SubagentStart`. Every command hook receives event JSON on **stdin**; HTTP hooks receive it as the POST body ([Hooks reference](https://code.claude.com/docs/en/hooks)) (VERIFIED). Hooks communicate back via exit code and stdout JSON: exit 0 = proceed (stdout parsed for JSON), exit 2 = blocking error (where the event supports blocking), other = non-blocking error. Output is capped at 10,000 characters; longer is spilled to a file ([Hooks reference](https://code.claude.com/docs/en/hooks)) (VERIFIED).

### Can a hook dispatch agents/skills?

**Yes — five handler types, all initiated from inside a live session** ([Hooks reference](https://code.claude.com/docs/en/hooks)) (VERIFIED):

1. **`command`** — runs a shell command with event JSON on stdin. The universal escape hatch: a `Stop`/`PostToolUse` hook can `exec` anything, including `claude -p`, a queue-append script, or a signal to a daemon.
2. **`http`** — POSTs event JSON to a local URL; a 2xx JSON body is parsed as hook output.
3. **`mcp_tool`** — calls a tool on a connected MCP server.
4. **`prompt`** — single-turn prompt to a fast model for a decision.
5. **`agent`** *(experimental)* — spawns a subagent that can `Read`/`Grep`/`Glob` and return a decision. This is the most literal "hook dispatches an agent," but it is scoped to returning a decision for the current event, not launching free-running background agents ([Hooks reference](https://code.claude.com/docs/en/hooks)) (VERIFIED).

The cleanest dispatch pattern is a `command` hook invoking the headless CLI: `claude -p "task" --allowedTools "Read,Edit,Bash"` spawns a fresh independent process. Notably, **`--bare` mode does not load hooks**, which doubles as the recursion firewall — a dispatched headless child won't re-fire the parent's `Stop` hook ([Run Claude Code programmatically](https://code.claude.com/docs/en/headless)) (VERIFIED).

**Dispatch constraints:** Hooks run synchronously and block the main loop by default until exit or timeout (command/HTTP/MCP 600 s; prompt 30 s; agent 60 s) ([Hooks reference](https://code.claude.com/docs/en/hooks)) (VERIFIED). A long synchronous `claude -p` inside a hook stalls the parent session. Command hooks can run detached with `async: true` — Boris Cherny confirmed "Hooks can now run in the background without blocking… Just add `async: true`" ([Threads / @boris_cherny](https://www.threads.com/@boris_cherny/post/DT8obEVkiRI/)) (VERIFIED) — but an async hook **cannot feed its result back**; the SDK doc states async outputs "cannot block, modify, or inject context… the agent has already moved on" ([Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks)) (VERIFIED). The one bridge back into a still-alive session is **`asyncRewake: true`**: the hook runs in the background and, if it exits code 2, wakes Claude with its stderr shown as a system reminder ([Hooks reference](https://code.claude.com/docs/en/hooks)) (VERIFIED). Practitioners report async hooks may be cancelled when a headless session ends ([Claude Code async hooks](https://ai.sulat.com/claude-code-async-hooks-what-they-are-and-when-to-use-them-61b21cd71aad)) (CITED).

### Can a hook emit/generate events?

**Yes, in the "produce a signal another process consumes" sense — not a built-in pub/sub bus.** A `command` hook can append a JSON line to an event log, `INSERT` into local SQLite, write to a Unix socket / named pipe, or send a signal. The official MCP-tool example explicitly demonstrates a `PreToolUse` hook doing `echo 'Memory operation' >> ~/log.log` ([Hooks reference](https://code.claude.com/docs/en/hooks)) (VERIFIED); the official SDK example appends to a local audit file from a `PostToolUse` hook ([Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)) (VERIFIED). The architectural point: a hook is an excellent **event emitter**, and `FileChanged` is a natural **consumer trigger** — but producer and consumer are decoupled only loosely. A hook writing to `queue.jsonl` does **not** automatically wake another Claude session; some live process must watch that queue. Practitioners confirm: "Hooks operate within individual sessions. There's no cross-session event bus or distributed dispatch mechanism" ([disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery)) (CITED).

### The self-triggering loop and its guardrails

The canonical "keep Claude working" pattern is a **`Stop` hook returning `{"decision": "block", "reason": "..."}`**, which prevents the stop and re-injects the reason as the next directive ([claudefa.st](https://claudefa.st/blog/tools/hooks/stop-hook-task-enforcement)) (CITED). The documented guardrail is the **`stop_hook_active`** flag: the hook must check it first and exit 0 when true, because true means Claude is already in forced-continuation ([Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks)) (VERIFIED). A separate documented footgun: returning `{"continue": true}` from a Stop hook triggers another round of stop hooks — a real bug observed in the wild ([claude-mem #1288](https://github.com/thedotmack/claude-mem/issues/1288)) (CITED); the fix is `{"continue": false}` or omitting the field. For SDK dispatchers, a `UserPromptSubmit` hook that spawns subagents can loop infinitely; documented mitigations are checking for `agent_id`/`agent_type` or scoping hooks to the top-level session ([Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks)) (VERIFIED).

**Section verdict:** Hooks form the *trigger and emit* layer — react with control flow, shell out to `claude -p --bare` to dispatch fresh agents, write to local stores. The guardrailed `Stop`-hook loop keeps one agent working. But hooks alone are not an autonomous loop: no session, no event; sync hooks block; async hooks can't return except via `asyncRewake`; no cross-session bus.

---

## 2. Scheduled / Background Execution — Can Any Act as a No-Human Dispatcher?

Claude Code ships **five families** of time-based/background execution. Each can run with no human prompt mid-execution; several can fire skills/agents autonomously. The disqualifying question for a local dispatcher is durability with no open Claude process.

**1. `/loop` + Cron tools (session-scoped).** `/loop` is a bundled skill. `/loop 5m check the deploy` is fixed-interval; `/loop check the deploy` (prompt only) is **dynamic/self-paced** — Claude chooses a 1 min–1 h delay based on observed state and can end the loop itself when the task is provably complete (the only built-in mode reacting to *state* over pure wall-clock) ([scheduled-tasks](https://code.claude.com/docs/en/scheduled-tasks)) (VERIFIED). Crucially `/loop <prompt>` can be another command — `/loop 20m /review-pr 1234` re-fires a packaged workflow with no human in the loop. Backed by `CronCreate`/`CronList`/`CronDelete` (no permission required, ≤50 tasks/session, scheduler checks every second, fires between turns). **Disqualifying constraints:** tasks "only fire while Claude Code is running and idle… Closing the terminal or letting the session exit stops them firing"; no catch-up for missed fires; **7-day expiry** on recurring tasks; `CLAUDE_CODE_DISABLE_CRON=1` kills it (VERIFIED). It is an in-session autopilot, not a standalone daemon.

**2. `ScheduleWakeup` / Snooze.** The self-rescheduling primitive powering `/loop` dynamic mode; accepts `prompt`, `delaySeconds`, `reason`. On fire it **re-feeds the prompt string as a fresh user turn** including slash-command semantics — self-perpetuating by design ([anthropics/claude-code #51304](https://github.com/anthropics/claude-code/issues/51304)) (CITED). Sharp edges practitioners report: no resume-vs-replay distinction — passing a one-shot slash command verbatim re-executes the *entire* command (all sub-agents, $1+/run, no consent gate) ([#54086](https://github.com/anthropics/claude-code/issues/54086)) (CITED); only `/loop`-style skills are safe to re-fire. Lives entirely inside one live session.

**3. `run_in_background` + `Monitor`.** `run_in_background: true` (Bash) starts a detached task that **emits a completion notification back to the orchestrator** when its polled condition is met — a harness-tracked event with no human ([tools-reference](https://code.claude.com/docs/en/tools-reference)) (VERIFIED; completion-notification detail CITED via [#51304](https://github.com/anthropics/claude-code/issues/51304)). Background subagents run with permissions pre-granted and auto-deny anything that would prompt. The **`Monitor`** tool (v2.1.98+) runs a background script and receives each output line as it arrives, interjecting in-session — "your agent reacts when something happens, not every 30 seconds." **Monitor is the closest built-in to true push (not poll) reaction to local state** (files, logs, process output); plugins can declare monitors that **auto-start when the plugin is active** ([plugins-reference](https://code.claude.com/docs/en/plugins-reference#monitors)) (VERIFIED). Not restored on `--resume`; scoped to a running session.

**4. Headless `claude -p` under an OS scheduler — the LOCAL autonomous path.** Each invocation is a fresh process; continuity via `--continue`/`--resume <session_id>` ([headless](https://code.claude.com/docs/en/headless)) (VERIFIED). `--allowedTools` / `--permission-mode acceptEdits|dontAsk` auto-approve for unattended runs; `--max-turns` / `--max-budget-usd` bound runaway; cron does not load the shell profile so env vars must be set in the crontab/plist explicitly. **This is the only fully LOCAL, no-cloud, no-open-session autonomous path:** an OS scheduler fires `claude -p`; the schedule/event detection lives in the OS layer or a long-lived `--continue` chain.

**5. Durable schedulers — `/goal`, Desktop scheduled tasks, Routines.** **`/goal`** (v2.1.139) sets a completion condition; a fast model (Haiku) checks after each turn and continues if unmet — **state-reactive, not wall-clock**, and it **works non-interactively with `-p`**: `claude -p "/goal CHANGELOG.md has an entry for every PR merged this week"` runs to completion in one invocation ([goal](https://code.claude.com/docs/en/goal)) (VERIFIED). This is the cleanest state-driven autonomous loop and composes with headless mode. **Desktop scheduled tasks** run locally with file access and can self-reschedule via `update_scheduled_task`, but require the Desktop GUI app process running and the computer awake — not headless/server-friendly. **Routines** are Anthropic-cloud-hosted with no local file access (fresh clone) — disqualified for local-only.

**Section verdict:** No single built-in is simultaneously local-only, survives with no open Claude process, *and* self-perpetuating with no OS scheduler. Viable LOCAL patterns: (1) OS scheduler firing headless `claude -p` (optionally `/goal` for state-reactivity, `--continue` for memory) — durable, no open session; or (2) one long-lived persistent `claude` process running `/loop` (dynamic) / `/goal` / Channels — self-perpetuating but bounded by the process staying alive (and the 7-day `/loop` cap, which `/goal` avoids).

---

## 3. Trigger & Event-Emission Primitives — The Signaling Layer

Claude Code's trigger/event primitives split cleanly into **local-capable** and **cloud-bound**.

### Local-capable (suitable for a local dispatcher)

**Agent SDK streaming-input mode — the primary local-dispatcher path.** `query({ prompt, options })` accepts `prompt` as an **`AsyncIterable<SDKUserMessage>`**. When you pass an async generator, the agent runs continuously, pulling messages as you yield them — the generator can yield from *any* local source (file watcher, SQLite poll, Unix socket, named pipe). **This is a custom event loop**: the dispatcher decides when to emit a user message into the agent ([agent-sdk/typescript](https://code.claude.com/docs/en/agent-sdk/typescript), [streaming-vs-single-mode](https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode)) (VERIFIED). The Python equivalent is `ClaudeSDKClient` with a message generator (caveat: avoid `break` mid-iteration — causes asyncio cleanup issues; use a flag) ([streaming_mode.py](https://github.com/anthropics/claude-agent-sdk-python/blob/main/examples/streaming_mode.py)) (CITED). The streaming `Query` object exposes `interrupt()`, `setPermissionMode()`, `setModel()`, `stopTask()` for mid-flight retuning; `options.agents` defines subagents and `.claude/skills/*/SKILL.md` is discovered — so the daemon can fire specific agents/skills per event. SDK hooks (`TaskCompleted`/`SubagentStop`/`Stop`) act as event-OUT "agent finished, dispatch next" triggers.

**Channels — the strongest local push-into-session primitive.** A channel is an MCP server running locally, spawned by Claude Code as a stdio subprocess; it pushes events via `mcp.notification({ method: 'notifications/claude/channel', ... })`, arriving wrapped as `<channel source="...">content</channel>` on Claude's next turn — a genuine server-initiated notification, not polling ([channels](https://code.claude.com/docs/en/channels), [channels-reference](https://code.claude.com/docs/en/channels-reference)) (VERIFIED). The official webhook-receiver example binds to `127.0.0.1` — **no external URL, no Anthropic cloud for the event path** (`curl -X POST localhost:8788 -d "build failed"` lands in the session). Two-way via a `reply` tool; events queue and batch while Claude is busy. A custom channel needs only `@modelcontextprotocol/sdk` + a Node-compatible runtime (Bun/Node/Deno) — Bun is not required for your own server, only for the prebuilt plugins ([channels-reference](https://code.claude.com/docs/en/channels-reference)) (VERIFIED, source-read 2026-05-17). Channels add **no separate billing surface** — cost is whatever `claude` session hosts them (interactive Max quota if interactive; headless/SDK metering if `-p` — see Cost & Licensing); and **Pro/Max users without an org skip the `channelsEnabled` admin gate entirely**, so no enablement step on your plan. **Caveats:** research preview — custom/local channels must launch with `--dangerously-load-development-channels server:<name>` (per-entry, even for your own marketplace plugin until it passes Anthropic security review); `--channels` syntax/protocol may change; requires Anthropic auth for inference; not on Bedrock/Vertex/Foundry; events are fire-and-forget (drop silently if the session didn't load the channel).

**Headless `claude -p` + stream-json.** `--output-format stream-json` (with `--verbose`, `--include-partial-messages`) emits newline-delimited typed JSON events — *an event interface* a wrapper parses for turn completion and `session_id`. Combining `--input-format stream-json` with `--output-format stream-json` establishes a persistent bidirectional session: the dispatcher writes user-message JSON to stdin, reads event JSON from stdout — turning one `claude` process into a long-lived scriptable agent ([headless](https://code.claude.com/docs/en/headless)) (VERIFIED; `--input-format stream-json` lightly documented per [#24594](https://github.com/anthropics/claude-code/issues/24594) (CITED)).

**Monitor tool** (in-session reactive watch) and **session-scoped `/loop`** (local timer self-trigger) round out the local set — both bounded to an open session (see Section 2).

### Cloud-bound (document, but disqualified for local-only)

**Routines / RemoteTrigger.** Saved configs executing on **Anthropic-managed cloud infrastructure**, "Access to local files: No (fresh clone)." The API trigger is an HTTP POST to a per-routine endpoint on `api.anthropic.com` behind a dated beta header ([routines](https://code.claude.com/docs/en/routines)) (VERIFIED). Practitioners report reliability issues in the preview: HTTP 200 but agent never executes ([#48888](https://github.com/anthropics/claude-code/issues/48888)), `/run` HTTP 400 ([#53581](https://github.com/anthropics/claude-code/issues/53581)) (CITED). Categorically unsuitable as the core of a network-free dispatcher; accurate to document as the *official remote trigger*.

**PushNotification.** Works only through Remote Control to the Claude mobile app via Anthropic's relay — one-way emit, no local sink to subscribe to. For local event-OUT, use a Channel `reply` tool, an SDK hook callback, or have the agent write to a local file/socket. Practitioners confirm most community "push notifications" use `Notification`/`Stop` hooks firing a local `ntfy`/`terminal-notifier` script, not the `PushNotification` tool ([tonydehnke.com](https://tonydehnke.com/blog/claude-code-notifications-ntfy-hooks/)) (CITED).

**Section verdict:** The strongest local event-IN paths are the **Agent SDK streaming-input loop** (most control, no preview flag) and **a custom local Channel server** (purpose-built push, but research-preview). Both keep transport, queue, and state on the machine; only inference traverses the network.

---

## 4. Wiring Claude Code Into a LOCAL-Only Dispatcher

A LOCAL-only event-driven dispatcher is buildable today from documented primitives plus community-proven glue. Anthropic **closed the native watch+wake request as "not planned"** ([#28229](https://github.com/anthropics/claude-code/issues/28229)) (CITED), so every working pattern is external orchestration wrapping `claude -p` or the Agent SDK.

**Filesystem watchers as triggers.** macOS `launchd` `WatchPaths` + a wrapper script is the canonical local trigger ([mayeu.me](https://mayeu.me/post/how-to-trigger-any-action-when-a-file-or-folder-changes-on-macos-on-the-cheap/)) (CITED). Documented gotchas, all dispatcher-relevant: no recursion (subfolders not watched), watched path must exist (can't watch for creation), no debouncing (implement `flock`/timestamp guard), no context passed (script must re-scan the store), race-prone ("modifications can be missed"). **Treat the watcher as a wake signal, not a reliable event source — always re-scan the authoritative store on wake.** Cross-platform: `fswatch`, `inotifywait`, `entr`, `watchman` ([eradman/entr](https://github.com/eradman/entr)) (CITED).

**Local queue / event log (the strongest fit for the existing `intake-queue.jsonl`).** The generic loop is **poll → claim → invoke → mark done**. A JSONL append-only log + tail loop: a daemon seeks past a stored offset; each new line is an event. Practitioners report the TICK_PROMPT must be imperative and idempotent ("pop one job from queue.jsonl, do it, append a `done` line; empty? exit") so a missed/duplicate wake is safe; fresh-process-per-tick is a feature ("the previous turn is in another universe") ([dev.to/agentdm](https://dev.to/agentdm/running-claude-code-in-a-loop-the-script-that-turns-it-into-a-persistent-agent-4i3f)) (CITED). SQLite-queue alternative: a `status` column *is* the lock (`pending`→`in_progress`→`completed`); atomic claim via `UPDATE ... WHERE status='pending' RETURNING` inside `BEGIN IMMEDIATE`, or WAL + busy-retry — for a solo-dev local dispatcher one writer is usually fine ([dev.to/domoniqueluchin](https://dev.to/domoniqueluchin/how-i-use-claude-code-to-dispatch-agent-tasks-from-a-supabase-queue-table-29jp)) (CITED). Hooks → local SQLite at near-zero latency is an established bridge ([disler/claude-code-hooks-multi-agent-observability](https://github.com/disler/claude-code-hooks-multi-agent-observability), [hoangsonww/Claude-Code-Agent-Monitor](https://github.com/hoangsonww/Claude-Code-Agent-Monitor)) (CITED).

**Named pipes / Unix sockets.** Anthropic's own (closed) daemon-mode request proposed a Unix-socket interface, confirming the pattern is desired but not natively provided ([claude-agent-sdk-typescript #33](https://github.com/anthropics/claude-agent-sdk-typescript/issues/33)) (CITED). FIFO: zero polling latency, no DB, but no persistence/priority/replay and writes above `PIPE_BUF` can interleave (INFERRED — standard Unix behavior, flagged in raw as unverified). Rule of thumb: FIFO/socket for low-latency fire-and-forget; SQLite/JSONL when you need durability, retry, priority, audit, or replay. Robust designs use both: the pipe as wake signal, the durable store as source of truth.

**Long-running local daemon hosting the Agent SDK (most robust).** Streaming-input mode is the documented mechanism for a long-lived, event-fed session: it "allows the agent to operate as a **long lived process**" ([streaming-vs-single-mode](https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode)) (VERIFIED). **Decisive performance constraint:** practitioners report `query()` spawns a fresh process per call with **~12 s overhead** (4-5 s spawn + 3-4 s CLI init + 2-3 s model load) and no documented hot-process reuse; `continue:true` workarounds tested *worse* ([claude-agent-sdk-typescript #34](https://github.com/anthropics/claude-agent-sdk-typescript/issues/34), [#33](https://github.com/anthropics/claude-agent-sdk-typescript/issues/33)) (CITED). Implication: keep **one** streaming-input client alive and feed it events — amortize the 12 s once instead of per-event. Per-event `claude -p` spawning is fine only for low-frequency triggers.

**OS schedulers as the heartbeat.** cron/launchd/systemd repeatedly run a headless Claude to drain a local store; the login shell (`-l`) is required so Node/PATH resolve under cron ([blle.co](https://www.blle.co/blog/automated-claude-code-workers)) (CITED). Existence proofs of pure-shell local daemons: `ClaudeNightsWatch` (adaptive polling 10 min→2 min→30 s) ([aniketkarne/ClaudeNightsWatch](https://github.com/aniketkarne/ClaudeNightsWatch)), `everything-claude-code` autonomous-agent-harness (markdown task queue surviving session boundaries) ([affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code/blob/main/skills/autonomous-agent-harness/SKILL.md)) (CITED).

**Hooks closing the loop.** Full local cycle: event source → dispatcher → `claude -p`/SDK → work → `Stop`/`PostToolUse` hook appends a follow-up event to the same store → dispatcher picks it up next tick. The official SDK example literally appends to a local audit file from a `PostToolUse` hook ([agent-sdk/overview](https://code.claude.com/docs/en/agent-sdk/overview)) (VERIFIED).

---

## 5. Cross-Cutting Themes

- **No session, no event.** Hooks, `/loop`, `ScheduleWakeup`, `Monitor`, and Channels all require a live Claude process. The only way to be durable with *no* open Claude is headless `claude -p` fired by an OS scheduler — or a long-lived daemon that *is* the always-on session.
- **Spawn cost dominates the architecture.** ~12 s per fresh process makes per-event `claude -p` viable only for low event rates. A persistent streaming-input process amortizes it once — the single biggest design driver.
- **The watcher is a wake signal, never the event source.** launchd/`fswatch` miss events, pass no context, and don't debounce. Always re-scan an authoritative durable store (the JSONL queue / SQLite) on wake; make the tick idempotent so spurious or duplicate wakes are no-ops.
- **Self-trigger is a real, recurring hazard at every layer.** Stop-hook loops (`stop_hook_active`, `{"continue":false}`), watcher self-fires (write outputs outside the watched path; `flock`), and `ScheduleWakeup` re-firing expensive one-shot commands. Loop guards are not optional.
- **Local transport, networked inference.** "Local-only" here means no external orchestration network — the model inference call to Anthropic is unavoidable. From 2026-06-15, `claude -p` / Agent SDK usage on subscription plans draws from a separate monthly Agent SDK credit ([agent-sdk/overview](https://code.claude.com/docs/en/agent-sdk/overview)) (VERIFIED) — directly relevant to a 24/7 dispatcher's economics.

## 6. Recommendations — Decision Framework & Recommended Architecture for Momentum

Momentum already has an `intake-queue.jsonl` event log, which makes the choice straightforward.

### Recommended architecture (primary build)

**A single long-lived Python (or TypeScript) daemon hosting `ClaudeSDKClient` in streaming-input mode, blocked on `intake-queue.jsonl`.**

> **Cost revision:** This long-lived Agent SDK daemon must authenticate with a **dedicated Anthropic API key on pay-as-you-go billing** — *not* subscription/Max OAuth. Anthropic explicitly prohibits subscription auth with the Agent SDK libraries, and from 2026-06-15 meters all `claude -p`/SDK subscription use against a small fixed monthly credit at full API rates, so the subscription confers no price advantage for a sustained dispatcher. The primary cost lever is **model-tier routing** (Haiku/Sonnet for event routing and light steps, Opus only for heavy reasoning); the top operational hazard is a stray `ANTHROPIC_API_KEY` in the daemon environment silently diverting billing — see the **Cost & Licensing** section for the full economics and mitigation.

1. **Event source — the existing queue.** The daemon's async generator blocks on the queue: tail-from-stored-offset, or a `watchdog`/`fswatch` wake that triggers an idempotent re-scan. Treat any filesystem wake purely as a signal; the queue file is the source of truth. If beads becomes the system of record (per the dual-write spike), `.beads/hooks/on_update` is a documented storage-layer push wake-source the daemon can ingest instead of a blind filesystem watcher — see **Beads as an Event Source (Design Addendum)** for the wiring.
2. **Claim semantics.** Mark each consumed event with a status (`pending`→`in_progress`→`done`) — either in-line in the JSONL or in a sidecar SQLite cursor table. The status field is the lock; an idempotent re-scan claims only unclaimed rows, so a duplicate/spurious wake finds nothing to do.
3. **Dispatch.** Per event, route to the matching agent/skill via SDK `agents={...}` and `.claude/skills/*/SKILL.md` discovery — *not* `/slash` strings (see contradiction note below).
4. **Close the loop with hooks.** `Stop` / `PostToolUse` hooks append follow-up events back into `intake-queue.jsonl` (or `INSERT` into the sidecar SQLite). The daemon picks them up next iteration. This is the documented hook-to-local-store pattern.
5. **OS scheduler as fallback heartbeat / liveness watchdog only.** A launchd/cron entry restarts the daemon if it dies and (optionally) injects a periodic "drain + maintenance" event so the system makes progress even if no external event arrives. The scheduler is *not* the dispatcher — it's the watchdog.

### Key tradeoffs to design around

- **SDK spawn-cost amortization.** Keep one streaming-input client alive for the daemon's lifetime; do not spawn `claude -p` per event. This converts ~12 s/event into ~12 s once. If the daemon must restart, capture `session_id` from the `system/init` event and respawn with `--resume`.
- **No-open-session limitation.** The daemon *is* the always-on session — it must be supervised (launchd `KeepAlive`, systemd `Restart=always`). If the host can't keep a daemon alive, fall back to OS-scheduler + headless `claude -p` per tick (durable, no open session, but pays spawn cost every tick — acceptable only at low event rates).
- **Permission flags for unattended runs.** Prefer least privilege: `--permission-mode dontAsk` + an explicit `permissions.allow` allowlist, with MCP scope (`--mcp-config .mcp.json --strict-mcp-config`) as the capability boundary. Use `--dangerously-skip-permissions` only if the allowlist proves impractical; every community loop uses it but it removes all gates. **Safer unattended posture if using a Channel:** a two-way channel can declare the `claude/channel/permission` capability (Claude Code v2.1.81+) so `Bash`/`Write`/`Edit` approval prompts are *relayed* (allow/deny by `request_id`) instead of blanket-skipped — keeps a real gate while still running headless. Only declare it if the channel authenticates the sender (anyone who can reply can approve tool use).
- **Self-trigger loop guards (mandatory).** (a) Hooks that append events must not append on every turn unconditionally — gate on a condition or a sentinel. (b) Stop hooks must check `stop_hook_active` and return `{"continue":false}`. (c) Write Claude outputs outside any watched path. (d) `flock`/`fcntl` lockfile so a second wake no-ops while a run is in flight. (e) Idempotent claim-by-status so a self-write wake finds no unclaimed work.
- **Cost telemetry.** Log `total_cost_usd` from `--output-format json` / the SDK result per event; budget against the separate Agent SDK credit effective 2026-06-15.

### Decision rule

> Daemon can be kept alive (supervisor available) **and** event rate is non-trivial → **persistent Agent SDK streaming-input daemon** (primary).
> No supervisor / low event rate / simplest possible → **OS scheduler + headless `claude -p` draining the queue** (fallback; pays spawn cost per tick).
> Want a supported push primitive and can accept research-preview status → add a **local Channel server** wrapping the queue as the event-IN transport into the daemon. Channel notifications are **unacknowledged** (`await mcp.notification()` resolves on transport-write, not on Claude processing it; dropped silently if the session didn't load the channel) — so the channel server, not the notification, must own idempotent claim/ack against the queue, and use a `reply` tool if you need delivery confirmation. The wake mechanism itself is **empirically confirmed** (spike 2026-05-17): an idle session autonomously takes a turn on an inbound channel event. But an unattended Channel-fed session **must** launch with a non-interactive permission posture (skip-permissions / `dontAsk`+allowlist / permission-relay) **and** a system prompt that legitimizes the event source, or it stalls on the first side-effectful tool and refuses injection-shaped events — see `spike-channel-push-sufficiency-2026-05-17.md`.

### Mechanism comparison

| Mechanism | Local-capable | No open session required | Self-perpetuating | State-reactive (vs wall-clock only) | Can fire skills/agents |
|---|---|---|---|---|---|
| Hooks (`Stop`/`PostToolUse`/`FileChanged`) | Yes | No | Via guarded `Stop`-block loop | Yes (`FileChanged`, tool events) | Yes (`command`→`claude -p`, `agent` type) |
| `/loop` + Cron tools | Yes | No (session-scoped, 7-day cap) | Yes (in-session) | Dynamic mode only | Yes (`/loop /cmd`) |
| `ScheduleWakeup` / Snooze | Yes | No (live session) | Yes (verbatim re-fire) | Via `/loop` dynamic | Yes (re-fire) |
| `run_in_background` + `Monitor` | Yes | No (not restored on resume) | Orchestrator chains it | Yes (Monitor = push) | Yes (orchestrator chains) |
| Headless `claude -p` + OS scheduler | **Yes** | **Yes** | Via `--continue` chain / scheduler | Via `/goal` / prompt logic | Skills yes; not raw `/slash` (except `/goal`) |
| `/goal` | Yes | Yes (composes with `-p`) | Yes (until condition holds) | **Yes** (condition-driven) | Yes |
| Agent SDK streaming-input daemon | **Yes** | **Yes** (daemon *is* the session) | **Yes** (you own the loop) | **Yes** (generator yields on state) | Yes (`agents=` / skill discovery) |
| Local Channel server | Yes | No (needs live session) | Reacts; loop is external | **Yes** (push) | Yes (channel `instructions` route to skill) |
| Routines / RemoteTrigger | **No (cloud)** | Yes | Via schedule | Via prompt | Yes (committed skills) |
| PushNotification | No (mobile relay) | — | No | No | No (event-OUT only) |

## 7. Known Limitations & Contradictions

- **Contradiction flagged — can headless `claude -p` fire `/slash` skills?** All four raw files agree user-invoked slash commands (`/commit`, `/review`) are interactive-only and won't fire literally in `-p` mode; you describe the task instead. The scheduled-execution file documents **`/goal` as a tested exception** that *does* work with `-p`. The recommended architecture sidesteps this entirely by routing to skills/agents via SDK `agents=` / SKILL.md discovery (model-mediated), not `/slash` strings. There is no SDK "invoke skill X" API — invocation is model-mediated.
- **Channels are research-preview.** Custom local channels require the `--dangerously-load-development-channels` dev flag and are subject to protocol change; not on Bedrock/Vertex/Foundry. Treat as promising but not yet stable for a production dispatcher. Both `channels` and `channels-reference` docs were **source-read and verified on 2026-05-17**: the local-stdio-subprocess architecture and the webhook example binding `127.0.0.1` (no Anthropic cloud in the event path) are confirmed VERIFIED, not inferred. Two further constraints from the reference: (a) notifications are **unacknowledged and silently dropped** if the channel isn't loaded — at-least-once delivery must be enforced in your server, not assumed; (b) concurrent events delivered while Claude is busy are **batched into one turn and processed as a group, in order** — to process independent event streams concurrently you must run **separate sessions**. Permission relay requires v2.1.81+. **Empirically confirmed 2026-05-17** (spike: `spike-channel-push-sufficiency-2026-05-17.md`; claude 2.1.143 / Max / fakechat / cmux-hosted idle session): an inbound channel event **autonomously drives a turn in an idle session with zero terminal input** (reproduced 2/2) — the wake question is settled **YES**. Two measured operational constraints for unattended use: (a) channel input is treated as **untrusted** — adversarially-shaped content is flagged as prompt injection, refused, and escalated to the human, so legitimate event framing + the channel server's `instructions` are mandatory; (b) side-effectful channel tools (e.g. `reply`) hit an **interactive permission gate that hard-stalls a no-human session** — unattended operation requires one of `--dangerously-skip-permissions`, `--permission-mode dontAsk` + a `permissions.allow` allowlist, a pre-seeded "don't ask again", or the permission-relay capability.
- **The ~12 s spawn-cost figure is community-reported** (CITED, GitHub issues #33/#34), not in official docs. The architectural conclusion (amortize via a persistent process) holds regardless of the exact number, but treat the precise figure as indicative.
- **Async hook cancellation under headless** is practitioner-reported and was partially addressed in v2.1.23; the lifetime risk remains. Don't rely on async hooks for guaranteed delivery — use a durable store.
- **FIFO/Unix-socket framing details** are inference from standard Unix behavior (flagged as unverified in the raw source), not Claude-Code-specific documentation.
- **Out of scope:** No Gemini, AVFL, or practitioner-notes corpus for this topic; cloud Routines/RemoteTrigger documented only as the official remote alternative, not evaluated for the local goal. Long-term durability of session-restore semantics across Claude Code versions was not exhaustively tested.

## Beads as an Event Source (Design Addendum)

**Upgraded verdict: monitoring beads and pushing the result into a running Claude Code session is feasible, and beads is *not* poll-only.** Earlier reasoning in this report assumed an external tracker would be a poll target; the beads-event-surface findings overturn that for beads specifically. Beads ships a first-class **storage-layer exec-on-state-change hook system** — `.beads/hooks/on_create`, `on_update`, `on_close` — that fires automatically after every committed mutation. That is a genuine push surface: a monitor does not have to spin on an interval (VERIFIED — `internal/hooks/hooks.go`, `internal/storage/hook_decorator.go` `HookFiringStore`, source-read 2026-05-17).

**The push mechanism.** Drop an executable at `.beads/hooks/on_update` (and `on_create`/`on_close`). Beads exec's it as `hook_script <issue_id> <event_type>` with the **full issue JSON piped to stdin**, **fire-and-forget, asynchronously, in a process group, with a 10 s timeout** (`BEADS_HOOK_TIMEOUT`-tunable). Wiring lives in the storage decorator, not in individual commands, so *every* mutation fires hooks — including commands not yet written — and only after the transaction commits, never on rollback (VERIFIED — `internal/hooks/hooks_unix.go`, `hook_decorator.go`; CHANGELOG PR #2891). This script *is* the "separate event monitoring system" the user asked about: it is the producer. There is no `bd serve`/`bd daemon`/`bd events`/`bd subscribe`/`bd listen` and no streaming JSON tail — the exec hook is the only push surface beads exposes.

**Push-triggered, pull-resolved.** There is deliberately no `on_ready` hook, because "ready" is a *derived projection* (open + no open blockers), not a stored status — no mutation event named "ready" exists (VERIFIED — no such constant in `hooks.go`; INFERRED that this is intentional). So the hook is a **coarse wake signal**, not a work item. When story A closes and unblocks story B, the monitor receives `on_close`/`on_update` for *A* — it must then run `bd ready --json --claim` to discover that *B* is now actionable. Do not treat the hook's stdin issue payload as the thing to dispatch; treat it strictly as "something changed, re-resolve the ready frontier now." This eliminates blind interval polling — the monitor sits idle and only runs `bd ready` on a hook fire — while keeping `bd ready` as the authority on what is actually claimable.

**Wiring into the dispatcher (a variant, not a replacement).** This slots cleanly into the recommended architecture in §6 without replacing it. The `on_update` hook becomes the **ingress producer** feeding the existing daemon: the hook script appends to the local queue / FIFO / Unix socket that the **local Channel server** reads, which then emits `notifications/claude/channel` into the long-lived session (§3); or it signals the **Agent SDK streaming-input daemon** whose async generator yields a "re-scan beads" message. Either way the hook does *not* push the issue into Claude — it pushes a wake into the same idempotent ingress this report already specifies. Transport stays entirely local (exec hook → local socket/queue → in-process notification); only model inference traverses the network, exactly as in the base architecture. The daemon or Channel server still owns idempotent claim/ack: the hook fans wakes in, the daemon resolves them against `bd ready --claim` and dedupes — the §6 claim-by-status discipline is unchanged, only its trigger source is upgraded from a filesystem watcher to a real storage event.

**What beads does NOT provide.** No `bd daemon`/`serve`/`events`/`subscribe`/`listen` command. `bd list --watch`/`bd show --watch` exist but are **internally poll-then-diff** — fsnotify was explicitly removed because Dolt stores data server-side, not in watchable files (VERIFIED — `cmd/bd/show_watch_test.go` regression test). An internal `events` SQL table with a `GetAllEventsSinceInTx` since-cursor query would be the ideal cheap change feed, but it is an internal Go API with no CLI/MCP surface. The `beads-mcp` MCP server is strictly request/response — a thin wrapper translating MCP calls into `bd` CLI commands, with no notifications, sampling, or subscriptions; the agent always *pulls* `beads_ready` (VERIFIED — `website/docs/integrations/mcp-server.md`). So the exec hook is the *only* push primitive; the MCP path is pull-only and cannot server-push to Claude.

**Risks, sharpened for the push model:**

1. **Self-trigger loop — acute.** The agent's own `bd update` / `bd close` / `discovered-from` create all fire `on_update`/`on_create` → wake → potential re-dispatch of work the agent itself just touched. Beads fires the hook on *every* committed mutation with **no actor filtering**. Mandatory guards: act only when `bd ready --claim` returns claimable work (the idempotent claim-by-status *is* the lock — a self-write wake that yields no new claimable issue is a no-op); debounce coalesced bursts; and where the mutation's actor is distinguishable from the monitor's own session, suppress it. This is the same self-trigger hazard §6 already flags, but the hook makes it more frequent — every field touch is a wake.
2. **Fire-and-forget = lossy.** Beads does not retry or track hook delivery. If the monitor or session is down when the hook fires, that wake is **permanently lost** — there is no replay. Mitigation: on monitor startup, always run a full `bd ready` **reconcile** sweep before trusting the hook stream; never treat the hook stream as the sole source of truth. This mirrors the report's "watcher is a wake signal, never the event source" principle — re-scan the authoritative store on wake and on boot.
3. **Atomic-claim race UNVERIFIED.** The 2026-05-16 dual-write spike recorded `bd ready --claim` as an atomic single-transaction claim, but the spike's own no-go list names "duplicate story assignments" as an abort trigger, and the beads-event-surface findings could not reconcile the duplicate-assignment report against beads issues (GitHub issue search unavailable). Treat built-in claim atomicity under concurrent load as **open**: run a single sole-claimer monitor, wrap claims in the monitor's own `flock`/lockfile, and validate empirically on pinned v1.0.4 before relying on beads' built-in atomicity for multi-claimer fan-out.
4. **Single-session serialization vs beads' parallelism.** Per §3's source-verified finding, Channels and a single session process queued events **batched into one turn, in order, one turn at a time** — but beads' core value is a *parallelizable* ready frontier (the whole point of `bd ready` is concurrent disjoint claims). Exploiting that parallelism requires **multiple monitor+session pairs**, each claiming disjoint ready work; one monitor + one session serializes a graph that beads is built to fan out.
5. **Cost gating.** A hook that wakes Claude on every mutation maximizes token burn under the licensing reality in the next section — and beads moves fast (multiple mutations per agent turn). The gate is the same idempotent-claim discipline: the wake must only escalate to a Claude turn when `bd ready` actually yields **new claimable work**, never on every field touch. A no-op wake must cost zero tokens — resolve it in the monitor process, not in a Claude turn.

**Version pin.** All of the above is verified against beads **v1.0.4** (released 2026-05-09; `main` advanced ~2026-05-18 with in-flight schema changes). The hook invocation contract and `bd ready --claim` semantics move fast and **must be re-verified against the exact pinned version before building**. The findings flagged two points low-confidence: whether built-in atomic `--claim` is genuinely race-free under heavy concurrent load, and whether an `on_ready`-style derived-state hook is planned (none found) — treat both as unproven and pin-and-test accordingly.

**Bottom line:** the user's idea works and is the natural fit — beads is *not* poll-only, and `.beads/hooks/on_*` is exactly the missing push primitive a separate event monitor needs. The hook is a coarse wake; `bd ready --claim` resolves the actual work, feeding the existing local Channel/SDK-daemon ingress this report already recommends. The real engineering is the self-trigger filter, the lossy-delivery startup reconcile, and the unproven atomic-claim race under concurrency — not the plumbing, which is already documented and local. One newly-measured constraint specific to the cmux+Channel variant (spike 2026-05-17): the dispatcher's Claude process must run with a non-interactive permission posture **and** a channel `instructions` system prompt that authorizes beads events — a vanilla interactive session empirically refuses injection-shaped channel input and hard-stalls on the permission gate for side-effectful tools. The Agent SDK-daemon path sidesteps both (programmatic `canUseTool`, no idle-session ambiguity), which is why it remains the primary recommendation over the cmux+Channel variant.

## Cost & Licensing

**Decision up front: for a sustained *local* dispatcher, authenticate with a dedicated Anthropic API key on pay-as-you-go billing — not your Max subscription.** A single-user local dispatcher running Anthropic's first-party Claude Code on your own Max subscription *is within terms*, but the economics and the Agent SDK auth rules make subscription auth the wrong choice for anything beyond low-volume or cloud-tolerant use. Subscription/Routines fits only narrow cases; everything else is API-key territory.

### Is a local unattended dispatcher on the Max subscription within Anthropic's terms?

Yes, conditionally — and the boundary is precise. The Anthropic Consumer Terms (eff. 2025-10-08) prohibit accessing the Services "through automated or non-human means … *except when you are accessing our Services via an Anthropic API Key or where we otherwise explicitly permit it*" ([Consumer Terms](https://www.anthropic.com/legal/consumer-terms)) — VERIFIED. The carve-out is decisive: Anthropic's own Claude Code docs explicitly permit scripted/headless use on subscription auth, shipping `claude setup-token` to mint a one-year `CLAUDE_CODE_OAUTH_TOKEN` "for CI pipelines, scripts, or other environments where interactive browser login isn't available" ([Authentication docs](https://code.claude.com/docs/en/authentication)) — VERIFIED. A long-lived daemon / scheduled `claude -p` / hook loop running *first-party Claude Code* on *your own* Max subscription falls under that carve-out.

What **is** unambiguously prohibited: reusing a subscription-derived OAuth token *inside any other product, tool, or service — including the Agent SDK packages and third-party harnesses*. Anthropic's February 2026 compliance clarification names the Agent SDK directly: subscription OAuth tokens "in any other product, tool, or service — including the Agent SDK — is not permitted" ([The Register, 2026-02-20](https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access/)) — VERIFIED for the prohibition (Anthropic compliance page quoted), CITED for the reporting. Enforcement — active blocking of OAuth tokens in third-party clients — began **January 9, 2026** ([Winbuzzer, 2026-02-19](https://winbuzzer.com/2026/02/19/anthropic-bans-claude-subscription-oauth-in-third-party-apps-xcxwbn/)) — CITED. The two raw sources **agree** here: first-party `claude -p` on subscription is permitted (metered); the Agent SDK *libraries* on subscription OAuth are prohibited. This directly constrains the recommended architecture — the long-lived SDK daemon cannot legitimately run on subscription auth and must use an API key. There are no dated reports of bans for first-party self-scheduling on one's own account; absence of such reports is suggestive, not proof — confidence here is medium (INFERRED on the long-term residual risk, which the raw research flagged explicitly).

### The economics that make subscription auth pointless for sustained automation

**Today (until June 14, 2026):** headless `claude -p` on subscription OAuth draws from the *same* interactive Max meter as claude.ai and Desktop — a rolling 5-hour session window plus weekly caps (Max has an all-model weekly cap and a separate Sonnet-only one) ([How usage and length limits work](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work)) — VERIFIED. An agentic loop consumes 10×–100× the tokens of chat, so it exhausts those caps fast. Behavior at the cap with extra usage disabled is a **hard stop** ("limit reached, resets at *time*"), no throttle, no auto-resume (a requested, unshipped feature) ([The New Stack](https://thenewstack.io/claude-code-usage-limits/)) — CITED; with extra usage enabled it spills to metered API-rate overage ([Manage extra usage](https://support.claude.com/en/articles/12429409-manage-extra-usage-for-paid-claude-plans)) — VERIFIED.

**From June 15, 2026 (official, in-docs):** all Agent SDK and `claude -p` use on a subscription stops drawing from the interactive pool and instead draws from a *separate, fixed, non-rollover monthly Agent SDK credit billed at full API rates* — **Pro $20/mo · Max 5x $100/mo · Max 20x $200/mo**, per-user, non-poolable, no rollover ([Use the Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)) — VERIFIED, corroborated by [InfoWorld](https://www.infoworld.com/article/4171274/anthropic-puts-claude-agents-on-a-meter-across-its-subscriptions.html) and [The Decoder](https://the-decoder.com/claude-subscriptions-get-separate-budgets-for-programmatic-use-billed-at-full-api-prices/) — CITED. On exhaustion: hard-stop, or pay-as-you-go overage only if extra usage is enabled. At standard API token rates a Max 20x's $200 credit buys roughly **300–600 Opus turns/month (~10–20/day)** — a modest fixed ceiling, not the generous interactive allowance. After June 15 the subscription confers **no price advantage** for a background dispatcher over a plain API key: same API rates, just a small prepaid bucket. (This is a post-dated policy — confidence is high because both raw sources cite the official effective-dated Help Center article, but it has not yet taken effect as of this report's 2026-05-17 date.)

### The SDK auth landmine (top operational hazard)

The Agent SDK docs prohibit subscription/claude.ai auth for SDK-built products and direct developers to API keys ([Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)) — VERIFIED. The trap: Anthropic's auth precedence places `ANTHROPIC_API_KEY` *above* `CLAUDE_CODE_OAUTH_TOKEN`, and in non-interactive `-p` mode "the key is always used when present" — so a stray exported API key in the daemon's environment **silently** overrides subscription OAuth and bills pay-as-you-go with no warning ([Authentication docs](https://code.claude.com/docs/en/authentication)) — VERIFIED. This is not theoretical: a Max 20x subscriber scheduled `claude -p` via cron with a stray `ANTHROPIC_API_KEY` set and was charged **$1,800+ in two days**; the issue was closed "not planned" with no maintainer fix ([anthropics/claude-code #43333 / #37686](https://github.com/anthropics/claude-code/issues/43333)) — CITED. **Mitigation (mandatory for any unattended loop):** strict env hygiene — the dispatcher exports exactly one dedicated API key and nothing else; interactive shells `unset ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN` and verify auth source via `/status` before any subscription-billed session; set billing alerts / spend limits on the dedicated key's Console org; and budget against `total_cost_usd` per event. Treat a stray key as the single highest-severity failure mode of the whole design.

### The Cloud Routines exception

Routines / scheduled remote agents are the one programmatic surface that genuinely stays subscription-covered: they draw the *interactive* subscription pool ("Routines draw down subscription usage the same way interactive sessions do"), a **different meter than the post-June-15 Agent SDK credit**, and run on **Anthropic-hosted compute** you don't pay for separately ([Automate work with routines](https://code.claude.com/docs/en/routines)) — VERIFIED. So Routines *are* covered by the Max subscription. The unavoidable tradeoff: Routines run cloud-hosted with **no local file access** (fresh clone), which directly conflicts with this dispatcher's local-only requirement and the verdict's local-only architecture. Routines are subscription-covered but cannot be the local dispatcher; they remain a low-volume / cloud-tolerant alternative only.

### Current API pricing (as of 2026-05)

First-party per-million-token (MTok) rates ([Pricing — Claude API Docs](https://platform.claude.com/docs/en/about-claude/pricing)) — VERIFIED:

| Model | Input | Output | Cache read |
|---|---|---|---|
| **Opus 4.7** | $5 | $25 | $0.50 |
| **Sonnet 4.6** | $3 | $15 | $0.30 |
| **Haiku 4.5** | $1 | $5 | $0.10 |

Opus 4.7 ships a **new tokenizer that can consume up to ~35% more tokens** for the same text — materially worse than the nominal rate. A substantive Opus agent turn with accumulated context (~30–60K in / ~5–15K out) runs ≈ **$0.30–$0.70 per turn** before tool/search costs; a dispatcher firing ~100 such turns/day is **≈ $1,000–2,000/month** on Opus — the order-of-magnitude reality, and exactly consistent with the $1,800-in-two-days incident. Per-turn token figures are illustrative (INFERRED — depend on context size and routing), but the order of magnitude is robust.

### Bottom line

For a sustained **local** dispatcher, the compliant and economically honest path is a **dedicated Anthropic API key on pay-as-you-go billing** — not subscription/Max auth. This is unambiguously within the Commercial Terms (the automated-access ban explicitly exempts API-key access), removes the cap-exhaustion failure mode, is what Anthropic's own docs direct for production automation, and is *required* for the recommended Agent SDK daemon (subscription OAuth with the SDK libraries is prohibited). Keep the Max subscription for *interactive* Claude Code. The primary cost lever is **model-tier routing** — Haiku/Sonnet for event routing and light steps (3×–25× cheaper than Opus), Opus reserved for heavy reasoning — plus aggressive prompt caching (0.1× input on cache hits) and Batch API (−50%) for non-interactive work. Subscription auth fits only **low-volume** use (staying under the post-June-15 fixed credit) or **cloud-tolerant** use (Routines, which forgo local file access). Confidence is high on the compliant path and the post-June-15 economics (official, effective-dated); medium on the residual terms risk of very-high-volume first-party self-scheduling, which the raw research flagged as permitted by the letter of the docs but with no published volume guarantee and a surface Anthropic has been actively tightening through 2026.

## Sources

**Official (VERIFIED):**
- [Hooks reference — Claude Code Docs](https://code.claude.com/docs/en/hooks)
- [Intercept and control agent behavior with hooks — Claude Agent SDK Docs](https://code.claude.com/docs/en/agent-sdk/hooks)
- [Run Claude Code programmatically (headless) — Claude Code Docs](https://code.claude.com/docs/en/headless)
- [Agent SDK reference — TypeScript](https://code.claude.com/docs/en/agent-sdk/typescript)
- [Agent SDK reference — Python](https://code.claude.com/docs/en/agent-sdk/python)
- [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [Streaming Input vs Single Message mode](https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode)
- [Push events into a running session with channels](https://code.claude.com/docs/en/channels)
- [Channels reference (build a custom channel)](https://code.claude.com/docs/en/channels-reference)
- [Run prompts on a schedule (/loop, Cron tools, Monitor)](https://code.claude.com/docs/en/scheduled-tasks)
- [Schedule recurring tasks in Claude Code Desktop](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- [Automate work with routines (RemoteTrigger / API trigger)](https://code.claude.com/docs/en/routines)
- [Tools reference (Monitor tool)](https://code.claude.com/docs/en/tools-reference)
- [Keep Claude working toward a goal (/goal)](https://code.claude.com/docs/en/goal)
- [Plugins reference — monitors](https://code.claude.com/docs/en/plugins-reference#monitors)
- [Boris Cherny on async hooks (Threads)](https://www.threads.com/@boris_cherny/post/DT8obEVkiRI/)
- [Authentication — Claude Code Docs (setup-token, OAuth precedence, June 15 note, bare mode, Remote Control scope)](https://code.claude.com/docs/en/authentication)
- [What is the Max plan? — Claude Help Center](https://support.claude.com/en/articles/11049741-what-is-the-max-plan)
- [Use Claude Code with your Pro or Max plan — Claude Help Center](https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan)
- [Use the Claude Agent SDK with your Claude plan — Claude Help Center (June 15 2026 Agent SDK credit, per-tier amounts)](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)
- [How do usage and length limits work? — Claude Help Center](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work)
- [Usage limit best practices — Claude Help Center](https://support.claude.com/en/articles/9797557-usage-limit-best-practices)
- [Manage extra usage for paid Claude plans — Claude Help Center](https://support.claude.com/en/articles/12429409-manage-extra-usage-for-paid-claude-plans)
- [Models, usage, and limits in Claude Code — Claude Help Center](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code)
- [Pricing — Claude API Docs (Opus/Sonnet/Haiku rates, caching, batch, worked example)](https://platform.claude.com/docs/en/about-claude/pricing)
- [Anthropic Consumer Terms of Service (eff. 2025-10-08)](https://www.anthropic.com/legal/consumer-terms)
- [Anthropic Usage Policy (eff. 2025-09-15)](https://www.anthropic.com/legal/aup)

**Beads source-reads (VERIFIED — repo source/docs, retrieved 2026-05-17):**
- [beads README — github.com/steveyegge/beads](https://github.com/steveyegge/beads/blob/main/README.md)
- [beads `docs/CLI_REFERENCE.md` (bd ready/list/show flags, --watch)](https://github.com/steveyegge/beads/blob/main/docs/CLI_REFERENCE.md)
- [beads `internal/hooks/hooks.go` — exec hook engine, event constants](https://github.com/steveyegge/beads/blob/main/internal/hooks/hooks.go)
- [beads `internal/hooks/hooks_unix.go` — hook invocation contract (args, stdin JSON, timeout, process group)](https://github.com/steveyegge/beads/blob/main/internal/hooks/hooks_unix.go)
- [beads `internal/storage/hook_decorator.go` — `HookFiringStore` storage-layer hook firing](https://github.com/steveyegge/beads/blob/main/internal/storage/hook_decorator.go)
- [beads `internal/storage/schema/migrations/0005_create_events.up.sql` — `events` table schema](https://github.com/steveyegge/beads/blob/main/internal/storage/schema/migrations/0005_create_events.up.sql)
- [beads `internal/storage/issueops/events.go` — `GetAllEventsSinceInTx` since-cursor query](https://github.com/steveyegge/beads/blob/main/internal/storage/issueops/events.go)
- [beads `cmd/bd/show_watch_test.go` + `cmd/bd/show.go` — `--watch` is polling, fsnotify regression](https://github.com/steveyegge/beads/blob/main/cmd/bd/show_watch_test.go)
- [beads `website/docs/integrations/mcp-server.md` — `beads-mcp` package, request/response only](https://github.com/steveyegge/beads/blob/main/website/docs/integrations/mcp-server.md)
- [beads `website/docs/cli-reference/hooks.md` — `bd hooks` = git hooks](https://github.com/steveyegge/beads/blob/main/website/docs/cli-reference/hooks.md)
- [beads `docs/ARCHITECTURE.md` — storage layout (.beads/embeddeddolt, .beads/dolt, issues.jsonl)](https://github.com/steveyegge/beads/blob/main/docs/ARCHITECTURE.md)
- [beads `CHANGELOG.md` — v1.0.0–v1.0.4 + Unreleased; PR #2891 (HookFiringStore), PR #2754, GH#2732](https://github.com/steveyegge/beads/blob/main/CHANGELOG.md)
- [beads docs site — gastownhall.github.io/beads (v1.0.4)](https://gastownhall.github.io/beads/)

**Community / practitioner (CITED):**
- [ccheney/bd-claim — community atomic-claim tool (naïve read-then-write race scenario)](https://github.com/ccheney/bd-claim)
- [Better Stack — Beads issue tracker for AI agents (overview/architecture)](https://betterstack.com/community/guides/ai/beads-issue-tracker-ai-agents/)
- [Steve Yegge — Beads Best Practices](https://steve-yegge.medium.com/beads-best-practices-2db636b9760c)
- [Claude Code async hooks (ai.sulat.com mirror)](https://ai.sulat.com/claude-code-async-hooks-what-they-are-and-when-to-use-them-61b21cd71aad)
- [Claude Code Stop Hook: Force Task Completion (claudefa.st)](https://claudefa.st/blog/tools/hooks/stop-hook-task-enforcement)
- [Stop hook loops infinitely due to {"continue":true} — claude-mem #1288](https://github.com/thedotmack/claude-mem/issues/1288)
- [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery)
- [Claude Code Hooks Complete Guide, March 2026 (SmartScope)](https://smartscope.blog/en/generative-ai/claude/claude-code-hooks-guide/)
- [Issue #51304: ScheduleWakeup re-enters slash command — anthropics/claude-code](https://github.com/anthropics/claude-code/issues/51304)
- [Issue #54086: ScheduleWakeup re-fires slash commands — anthropics/claude-code](https://github.com/anthropics/claude-code/issues/54086)
- [Issue #24594: --input-format stream-json undocumented](https://github.com/anthropics/claude-code/issues/24594)
- [Issue #48888: RemoteTrigger HTTP 200 but agent never executes](https://github.com/anthropics/claude-code/issues/48888)
- [Issue #53581: Routines /run HTTP 400 trigger_id](https://github.com/anthropics/claude-code/issues/53581)
- [Issue #28229: Native agent scheduling / daemon mode — closed not-planned](https://github.com/anthropics/claude-code/issues/28229)
- [claude-agent-sdk-typescript #33 — Daemon Mode for Hot Process Reuse](https://github.com/anthropics/claude-agent-sdk-typescript/issues/33)
- [claude-agent-sdk-typescript #34 — query() ~12s overhead](https://github.com/anthropics/claude-agent-sdk-typescript/issues/34)
- [claude-agent-sdk-python streaming_mode.py](https://github.com/anthropics/claude-agent-sdk-python/blob/main/examples/streaming_mode.py)
- [Running Claude Code in a Loop (dev.to/agentdm)](https://dev.to/agentdm/running-claude-code-in-a-loop-the-script-that-turns-it-into-a-persistent-agent-4i3f)
- [Dispatch agent tasks from a queue table (dev.to/domoniqueluchin)](https://dev.to/domoniqueluchin/how-i-use-claude-code-to-dispatch-agent-tasks-from-a-supabase-queue-table-29jp)
- [Building Automated Claude Code Workers with Cron and MCP (blle.co)](https://www.blle.co/blog/automated-claude-code-workers)
- [everything-claude-code autonomous-agent-harness](https://github.com/affaan-m/everything-claude-code/blob/main/skills/autonomous-agent-harness/SKILL.md)
- [aniketkarne/ClaudeNightsWatch](https://github.com/aniketkarne/ClaudeNightsWatch)
- [How to trigger an action on file/folder change on macOS (mayeu.me)](https://mayeu.me/post/how-to-trigger-any-action-when-a-file-or-folder-changes-on-macos-on-the-cheap/)
- [eradman/entr](https://github.com/eradman/entr)
- [hoangsonww/Claude-Code-Agent-Monitor](https://github.com/hoangsonww/Claude-Code-Agent-Monitor)
- [disler/claude-code-hooks-multi-agent-observability](https://github.com/disler/claude-code-hooks-multi-agent-observability)
- [Push notifications via ntfy + hooks (tonydehnke.com)](https://tonydehnke.com/blog/claude-code-notifications-ntfy-hooks/)
- [anthropics/claude-code #43333 — `claude -p` with OAuth bills as API usage (incl. #37686 $1,800/2-day report)](https://github.com/anthropics/claude-code/issues/43333)
- [anthropics/claude-code #37686 — `claude -p` on Max → $1,800 unintended API billing](https://github.com/anthropics/claude-code/issues/37686)
- [anthropics/claude-code #36320 — Auto-resume after usage limit reset (requested, not shipped)](https://github.com/anthropics/claude-code/issues/36320)
- [The Register — Anthropic clarifies ban on third-party Claude access (2026-02-20)](https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access/)
- [Winbuzzer — Anthropic bans Claude subscription OAuth in third-party apps (2026-02-19, Jan 9 enforcement)](https://winbuzzer.com/2026/02/19/anthropic-bans-claude-subscription-oauth-in-third-party-apps-xcxwbn/)
- [InfoWorld — Anthropic puts Claude agents on a meter across its subscriptions](https://www.infoworld.com/article/4171274/anthropic-puts-claude-agents-on-a-meter-across-its-subscriptions.html)
- [The Decoder — Claude subscriptions get separate budgets for programmatic use, billed at full API prices](https://the-decoder.com/claude-subscriptions-get-separate-budgets-for-programmatic-use-billed-at-full-api-prices/)
- [The New Stack — Claude Code users hitting usage limits faster](https://thenewstack.io/claude-code-usage-limits/)
- [apidog — Claude Code weekly limits +50% through July 13, 2026](https://apidog.com/blog/claude-code-weekly-limits-50-percent-increase-july-2026/)
- [MindStudio — Claude Code Routines scheduled agents (~15 runs/day cap)](https://www.mindstudio.ai/blog/claude-code-routines-scheduled-agents)
- [claudefa.st — Claude Code Remote Control guide (Pro/Max gating)](https://claudefa.st/blog/guide/development/remote-control-guide)
- [amux — Claude Code Headless Mode: Complete Self-Hosting Guide (2026)](https://amux.io/guides/claude-code-headless/)
- [TokenMix — Complete Claude Limits Guide 2026 (5-hour + weekly caps)](https://tokenmix.ai/blog/complete-claude-limits-guide-2026-tokens-uploads-5-hour)
- [Pasquale Pillitteri — Claude Code weekly limits +50% May 13–July 13 2026](https://pasqualepillitteri.it/en/news/2494/claude-code-weekly-limits-50-percent-anti-codex-anthropic-2026)
- [Hypereal — Claude Pro & Max Weekly Rate Limits Guide (2026)](https://hypereal.cloud/a/weekly-rate-limits-claude-pro-max-guide)
- [autonomee.ai — Is This Allowed? Claude Code Terms of Service Explained](https://autonomee.ai/blog/claude-code-terms-of-service-explained/)
- [VentureBeat — Anthropic cracks down on unauthorized Claude usage by third-party harnesses](https://venturebeat.com/technology/anthropic-cracks-down-on-unauthorized-claude-usage-by-third-party-harnesses)
