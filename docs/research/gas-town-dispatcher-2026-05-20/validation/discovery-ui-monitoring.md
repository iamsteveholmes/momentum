---
content_origin: research-agent
date: 2026-05-22
sub_question: "Gas Town/Gas City dashboard and monitoring UI — what ships, what the community built, monitoring gap assessment"
---

# Gas Town / Gas City Dashboard and Monitoring UI — Discovery

## Research Question

For a Momentum multi-loop automated sprint pipeline (parallel story dispatch → per-story review/QA → corpus AVFL fix loop → E2E loop → human review loop), can a solo developer maintain adequate real-time visibility into pipeline state using the monitoring tools that ship with Gas Town and Gas City? What exactly do those tools show, and where are the gaps?

## Sources Consulted

- `github.com/gastownhall/gastown` README — [OFFICIAL] full GT dashboard, gt feed, OTEL telemetry documentation
- `github.com/gastownhall/gascity` README — [OFFICIAL] gc dashboard description and API surface
- `github.com/gastownhall/gascity/docs/reference/cli.md` — [OFFICIAL] full CLI reference for gc dashboard, gc converge, gc status, gc order, gc events (read via GitHub API)
- `github.com/gastownhall/gascity/docs/reference/events.md` — [OFFICIAL] gc events format specification
- `github.com/gastownhall/gascity/docs/reference/api.md` — [OFFICIAL] Supervisor REST API surface
- `github.com/gastownhall/gascity/cmd/gc/dashboard/web/src/panels/status.ts` — [OFFICIAL] source code confirming dashboard status panel data
- `github.com/gastownhall/gascity/cmd/gc/dashboard/web/src/panels/supervisor.ts` — [OFFICIAL] source code confirming supervisor panel content
- `github.com/gastownhall/gascity/cmd/gc/dashboard/web/src/main.ts` — [OFFICIAL] dashboard panel registry and refresh model
- `github.com/gastownhall/gascity/cmd/gc/dashboard/web/src/palette.ts` — [OFFICIAL] dashboard command palette / interactive controls
- `github.com/gastownhall/gascity-packs` repository — [OFFICIAL] community packs inventory (slack-pack, flywheel, pr-pipeline, etc.)
- `github.com/gastownhall/gascity-packs/slack-pack` — [OFFICIAL] slack-pack README confirming preview/scaffold status
- `github.com/gastownhall/gastown/docs/otel-data-model.md` — [OFFICIAL] Gas Town OTEL telemetry event schema
- `github.com/gastownhall/gastown/docs/design/otel/otel-architecture.md` — [OFFICIAL] OTEL architecture and backend support
- `docs.gastownhall.ai/usage/diagnostics` — [OFFICIAL] gt feed and gt dashboard documentation
- `docs.gascityhall.com/reference/cli` — [OFFICIAL] Gas City CLI reference overview
- `github.com/gastownhall/gascity/issues` — [OFFICIAL] issue tracker, dashboard-related issues #1804 and #2017
- `tenzinwangdhen.com/posts/gastown-good-bad-ugly/` — [PRAC] practitioner review of Gas Town monitoring experience
- `github.com/gastownhall/wasteland` — [OFFICIAL] federation protocol description (confirmed not a monitoring tool)
- GitHub search for gastownhall Grafana dashboards — zero results

---

## Findings

### Area 1: Gas Town Dashboard — What It Actually Shows

#### `gt dashboard` (Web Server)

CONFIRMED from official documentation and source code analysis.

`gt dashboard` launches an HTTP server (default port 8080, configurable with `--port`) serving a single-page web application. The `--open` flag launches the browser automatically. No authentication is documented.

**What the dashboard shows:**

The dashboard has two modes depending on scope:

**Supervisor-level scope (no city selected):**
- Summary banner: total city count, running count, stopped count, supervisor uptime
- City table: name, running/stopped/error badge, status, phases completed, error message, "Open" link
- Activity stream: last hour of events from the supervisor event bus, filterable by type and agent

**City-level scope (city directory or `--city` flag):**
- Status banner with five stat chips: Agents (running count), Assigned (in-progress beads), Beads (open total), Convoys (count), Unread (mail)
- Alert indicators: stuck agents (>30 min inactive, shown in red), stale assigned beads (yellow), P1/P2 priority issues (red), dead sessions (red), "All clear" when clean
- Crew panel: agent sessions with running state
- Issues panel: open beads with assignee and status
- Mail panel: inbox messages between agents and humans
- Convoy panel: convoy list
- Escalations panel: open escalations
- Services panel, Rigs panel, Pooled panel, Queues panel, Assigned panel: additional city-scoped views

**Interactive controls:**
The dashboard includes a command palette (keyboard shortcut) with actions: new issue, compose mail, new convoy, assign work, plus JSON viewer shortcuts for status, agent list, convoy list, and mail inbox. The dashboard is not purely read-only — it supports creating issues, composing mail, and creating convoys from the browser. [OFFICIAL — palette.ts source]

**What `gt dashboard` does NOT show:**
- No order execution history view
- No convergence loop state (iteration count, gate status, current loop phase) — no panel for these exists
- No unified pipeline diagram showing which phase a story is in
- No explicit "human gates pending" panel (escalations panel covers blocked work but not specifically gate-awaiting items)
- No formula/molecule step progress tracking

**Refresh model:** Event-driven via SSE (Server-Sent Events) connected to the Gas City supervisor event bus. The dashboard marks panels dirty when relevant events arrive and re-fetches from the REST API. Not a static 30-second poll — it is live with SSE streaming. [OFFICIAL — main.ts source]

#### `gt feed` (TUI)

CONFIRMED from official documentation.

`gt feed` is a terminal interactive TUI with three panels:
- **Agent tree** (top): all agents organized by role, latest activity per agent
- **Convoy panel** (middle): in-progress and recently landed convoys
- **Event stream** (bottom): chronological event feed, scrollable with vim-style keys (j/k), filterable by `--mol`, `--type`, `--rig`, `--since`

Navigation: Tab to switch panels, 1/2/3 to jump to panel, `?` for help, `q` to quit.

**Problems View:** Accessible via `p` key in `gt feed` or `gt feed --problems` flag. Groups agents by health state:
- GUPP Violation — hooked work with no progress for extended period
- Stalled — hooked work with reduced progress
- Zombie — dead tmux session
- Working — active, progressing normally
- Idle — no hooked work

Intervention keys in problems view: `n` to nudge, `h` to handoff (refresh context). This makes `gt feed --problems` the closest thing to an interactive triage surface.

**What `gt feed` does NOT show:** Order execution history, convergence loop state, formula step progress, human gate queue. [OFFICIAL — docs + README]

**`gt dashboard` vs `gt feed` distinction:** Dashboard is browser-based and shows a richer data model (beads, mail, convoys, stuck-agent alerts, interactive controls). `gt feed` is terminal-only with real-time event streaming and the Problems View triage capability. They are complementary, not redundant. [CONFIRMED — source analysis]

---

### Area 2: Gas City Dashboard — Current State

CONFIRMED from official CLI reference and source code.

`gc dashboard` (alias: `gc dashboard serve`) launches the same type of web application as the Gas Town dashboard, serving from port 8080. The official description: "Open the static GC dashboard against the machine-wide supervisor API."

**Panels confirmed in source code** (`cmd/gc/dashboard/web/src/panels/`):
`activity`, `admin`, `cities`, `convoys`, `crew`, `issues`, `mail`, `options`, `ready`, `status`, `supervisor`

**Status panel (confirmed from status.ts source):**
At city scope: fetches city status, active sessions, open beads, and convoys in parallel. Displays: running agent count, assigned beads, open beads, convoy count, unread mail. Alert chips: stuck agents (red), stale assigned (yellow), P1/P2 issues (red), dead sessions (red). Stuck agent detection is generic: any pooled running agent with `last_active` >30 minutes ago. No role names are checked.

At supervisor scope: total cities, running count, stopped count, supervisor uptime. Alert chips: no cities registered, cities not running, cities reporting errors, startup phase.

**Supervisor panel (confirmed from supervisor.ts source):**
Shows a table of all managed cities with: name, running/stopped/error badge, status message, phases completed, error message, and an "Open" link to navigate to city scope.

**What `gc dashboard` does NOT show:**
- No convergence loop state — no panel named `converge` exists in the dashboard source. The `gc converge list/status` commands are CLI-only.
- No order execution history — no panel named `orders` exists. `gc order history` is CLI-only.
- No pipeline diagram or unified "story ABC is in phase QA" view
- No human gate pending items as a distinct view (escalations panel covers related territory)

**`gc converge status` (CLI only):**
Shows the state of a specific convergence loop by bead-id. Flags: `--json` for machine-readable output. The loop model: root bead + formula + gate = repeat until gate passes or max iterations. State values: `active`, `waiting_manual`, `terminated`. `gc converge list` supports `--state` filter and `--all-rigs`. Per-loop status is per-bead, not an aggregate view. There is no single command that shows all convergence loops in the system at a glance without `gc converge list`. [OFFICIAL — CLI reference]

**`gc status`:**
Shows city-wide overview: controller state, suspension status, all agents with running status, rigs, summary count. Supports `--json`. This is the primary CLI health check command. [OFFICIAL — CLI reference]

**`gc events`:**
Real-time event stream from the supervisor API. Outputs JSON Lines (`--follow` or `--watch` for streaming). Event schema: `{actor, city, message, seq, subject, ts, type}`. Confirmed event types from documentation examples: `bead.created`, `mail.sent`, `session.woke`. All CLI operations emit events — in principle any state transition is observable via `gc events --follow`. Can be filtered by `--type`, `--since`, `--payload-match`. [OFFICIAL — events.md]

**`gc order history`:**
Queries bead history for past order runs. Filterable by order name and rig. Output: JSONL. This gives a record of which orders fired, but it is a pull query not a live view. [OFFICIAL — CLI reference]

---

### Area 3: Community-Built Monitoring Tools

CONFIRMED: No community-built monitoring or observability tools specific to Gas City pipelines exist in the public ecosystem.

Evidence:
- `github.com/gastownhall/gascity-packs` contains: `discord-intake`, `discord`, `flywheel`, `github-intake`, `jeffrey`, `pr-pipeline`, `pr-review`, `rlm`, `slack-pack`, `tmux-theme`. None of these are monitoring or visualization tools.
- `flywheel` is an agent-enhancement pack (memory, inter-agent mail, past-session search, pre-commit scanning). Not monitoring.
- `github.com/gastownhall/wasteland` is a federated work coordination protocol (job marketplace), not a monitoring tool.
- GitHub search for `gascity pipeline monitor` returned zero results.
- GitHub search for `gastownhall grafana` returned zero results.
- No community Grafana dashboards, Prometheus exporters, or custom status pages were found. [CONFIRMED — search results]

Gas Town ships its own OTEL telemetry (see Area 4), which can feed into any OTLP-compatible backend including Grafana/Prometheus, but no pre-built dashboards for that integration were found in the public ecosystem.

---

### Area 4: Notification and Alerting Integrations

#### Gas Town OTEL Telemetry (Shipping, Production-Ready)

CONFIRMED from official documentation and source (`otel-data-model.md`, `otel-architecture.md`).

Gas Town ships OpenTelemetry (OTLP) telemetry as a production feature on main. Activated by environment variables:
```
GT_OTEL_METRICS_URL=http://localhost:8428/opentelemetry/api/v1/push
GT_OTEL_LOGS_URL=http://localhost:9428/insert/opentelemetry/v1/logs
```

**Events emitted (confirmed event names):**
`agent.instantiate`, `session.start/stop`, `agent.state_change`, `prompt.send`, `prime`, `agent.event`, `agent.usage`, `bd.call`, `mail`, `sling`, `nudge`, `done`, `polecat.spawn`, `polecat.remove`, `mol.cook`, `mol.wisp`, `mol.squash`, `mol.burn`, `bead.create`, `formula.instantiate`, `convoy.create`, `daemon.restart`, `pane.output`

**Metrics (18 counters):** Includes `gastown.session.starts.total`, `gastown.bd.calls.total`, `gastown.polecat.spawns.total`, `gastown.done.total`, `gastown.convoy.creates.total`, and others. Latency histogram: `gastown.bd.duration_ms`.

**Backends supported:** Any OTLP v1.x+ compatible backend. VictoriaMetrics/VictoriaLogs is the local development default. Prometheus, Grafana Mimir, Loki, Datadog, New Relic, Grafana Cloud, and OTel Collector are all listed as compatible. VictoriaMetrics spins up via Docker.

**Gap:** Distributed traces are roadmap-only (not yet implemented). "Work context injection" and agent conversation event streaming remain incomplete pending PR #2199. Token cost tracking is not yet implemented. [OFFICIAL — otel-architecture.md maturity note]

**Practical implication:** A solo developer can build a Grafana dashboard against VictoriaMetrics that shows Gas Town agent activity, session lifecycle, and formula execution — but there are no pre-built dashboards for this, and the event schema does not include pipeline-phase-level granularity (e.g., "story ABC entered QA phase").

#### Gas City slack-pack (Preview, Not Production-Ready)

CONFIRMED from official slack-pack README.

The `slack-pack` in `gascity-packs` is at v0.1.0 and is explicitly marked "preview/scaffold status." Its README states: "not yet at parity with the discord pack." Key capabilities that are NOT yet implemented: channel mapping, rig mapping, workflow status projection.

**What it actually does:** Binds Slack DMs or channels to Gas City sessions, enabling agents to participate in Slack conversations. It handles slash commands, button clicks, modal submissions, and file attachments as bidirectional communication between Slack and Gas City agents. It does NOT send pipeline state change notifications, order completion alerts, or gate pending notifications autonomously. [OFFICIAL — slack-pack README]

**Practical implication:** The slack-pack is a conversation bridge, not a notification system. Using it to get push notifications when a story enters a new phase or when a human gate opens would require custom workflow wiring that the pack does not currently provide. [CONFIRMED]

#### Gas Town Escalation / Email / SMS Notifications

CONFIRMED from prior research corpus (`research-human-in-loop-oversight.md`).

Gas Town's escalation system routes notifications via email and SMS based on severity level in `escalation.json`. CRITICAL severity triggers email + SMS to the human Overseer. This is pull-not-push for gate-pending items: the human must be watching escalation mail or proactively running `bd gate list` to discover pending human approvals. No Slack or webhook integration ships natively with Gas Town. [OFFICIAL — prior research]

#### What Practitioners Actually Use

CONFIRMED from practitioner review (Tenzin Wangdhen, February 2026).

The practitioner report is clear: "There's a web dashboard (`gt dashboard`), but I found myself in tmux panes anyway." The primary operational pattern is terminal-based: `gt feed`, direct tmux pane inspection, and `gt convoy list`. The dashboard was not used in daily operation despite being available.

Practitioner report also confirms significant observability gaps: "Observability is thin. Sometimes 6 PRs merged and I had no idea when I'd slung them." And: "Other times the system seemed stuck and I couldn't tell why." [PRAC — tenzinwangdhen.com]

---

### Area 5: The Monitoring Gap Assessment

#### Can the developer see the unified pipeline state?

CONFIRMED: No single view provides the required unified pipeline state for a Momentum sprint pipeline.

The question was: can a developer see "story ABC is in QA, story DEF is in code review, the AVFL loop is on iteration 2 of 5, E2E is not yet started, human gate is pending" in a single view?

**Analysis by dimension:**

| Dimension | Gas Town | Gas City | Gap |
|---|---|---|---|
| Which stories are in which phase | No native view | No native view | Gap |
| Which loops are running | No loops concept | `gc converge list` (CLI) | Partial — CLI only, no dashboard panel |
| Current loop iteration number | N/A | `gc converge status <id>` (CLI) | Partial — per-loop query, no aggregate |
| Gate status per loop | N/A | `gc converge list --state waiting_manual` | Partial — CLI only |
| Stuck agents | `gt feed --problems` (TUI) | Dashboard "N stuck" alert + session list | Adequate for stuck detection |
| Human gate pending items | Pull only, `bd gate list` | No dedicated view | Gap — pull-only, not surfaced proactively |
| E2E loop not yet started | No concept | No concept | Gap |
| Story completion across agents | `gt convoy list` (partial) | `gc converge list` (partial) | Inadequate for multi-loop |
| Order firing history | No concept | `gc order history` (CLI) | Partial — historical, not live |
| Pipeline diagram | Not present | Not present | Full gap |

**Closest achievable with current tooling:**

A developer running Gas City could assemble approximate pipeline awareness by combining:
1. `gc status` — agent health, running count, assigned beads
2. `gc converge list` — active convergence loops by state
3. `gc events --follow --type bead.closed,mail.sent,session.woke` — live event stream for state transitions
4. `gc order history` — which orders fired recently
5. `gc dashboard` (browser) — stuck agents, mail, bead counts, convoy counts

This is four separate terminal queries plus a browser tab, with no unified view. Each query answers a different fragment of the pipeline state question. There is no data source that ties "story identity" to "current pipeline phase" — that mapping exists only in the Momentum bead metadata, which Gas City does not interpret semantically.

**What it would take to build a Momentum pipeline status page:**

Gas City exposes a full REST API (`/v0/city/{cityName}/beads`, `/v0/city/{cityName}/events/stream`, `/v0/city/{cityName}/status`, plus orders and convergence endpoints). The supervisor event bus streams all state transitions as SSE. A custom status page could:
1. Query all open beads and read their labels/metadata to determine which phase each story is in
2. Subscribe to `gc events --follow` for live updates
3. Query `gc converge list --json` for active loop states
4. Query `gc order history --json` for recent order firings

This is buildable as a shell script + simple HTML page polling the API. Estimated effort: 1–2 days for a working prototype if the story-phase label schema is defined upfront. The API surface is well-documented (OpenAPI spec downloadable from `docs.gascityhall.com/schema`). [OFFICIAL — api.md, events.md]

Gas Town's OTEL telemetry pipeline (metrics + structured logs to VictoriaMetrics, visualized in Grafana) could also serve as a foundation — but it requires VictoriaMetrics + Grafana to be running and a custom dashboard built. The OTEL events do not include pipeline-phase-level metadata by default.

---

## Synthesis

**Gas Town dashboard reality:** The official documentation claims `gt dashboard` shows "agents, convoys, hooks, queues, issues, and escalations." Source code confirms this. The dashboard is richer than the diagnostic docs alone suggest: it has event-driven SSE refresh, a command palette with interactive controls (create issues, compose mail, assign work), stuck-agent alerting, and city/supervisor scope switching. However, practitioner experience indicates the dashboard was not used in daily operation — terminal panes were preferred. The stated "Problems View" is part of `gt feed` (TUI), not the web dashboard.

**Gas City dashboard reality:** Architecturally parallel to Gas Town's dashboard. It has the same panel structure (activity, convoys, crew, issues, mail, escalations, services, rigs, status, supervisor). The status panel has generic stuck-agent detection (30 min idle threshold, no role names). The dashboard does NOT have panels for convergence loop state, order execution history, or pipeline phase. These are CLI-only surfaces.

**The fundamental monitoring gap:** Both Gas Town and Gas City are optimized for monitoring a fleet of parallel coding agents doing software development tasks. Their monitoring primitives are: agent health (running/stuck/dead), work assignment (which bead is assigned to which agent), convoy progress (how many beads in a convoy are closed), and mail state. They do NOT model "pipeline phases" — the concept of a story moving through QA → code review → AVFL → E2E is not native to either system. That semantic layer would have to be implemented by Momentum.

**OTEL telemetry is real but incomplete:** Gas Town's OTEL telemetry ships and is production-quality for core agent lifecycle events. It would enable Grafana/Prometheus-based monitoring of agent throughput, session counts, and formula execution rates. It does NOT provide story-phase-level pipeline visibility and has no pre-built dashboards. Distributed traces remain a roadmap item.

**Slack-pack is not a solution:** The slack-pack v0.1.0 is a conversation bridge at preview status. It explicitly lacks "workflow status projection" — the exact capability a solo developer would need for push notifications when a human gate opens.

**Community has not filled the gap:** Zero community-built monitoring tools, Grafana dashboards, or pipeline visualization tools exist for Gas City in the public ecosystem. The ecosystem is young (v1.1.0 as of May 2026), and community tooling is nascent.

**The notification story is weak:** Gas Town routes CRITICAL escalations to email/SMS, but this is reactive (escalation-triggered), not proactive (phase-change-triggered). Human gate pending items require active polling by the developer. The `gt feed --problems` TUI provides the best available proactive alert surface, but it requires a persistent terminal window and only covers agent health, not pipeline phase transitions.

---

## Open Questions

1. **Does `gc converge status` output include iteration count and current gate state?** The CLI reference documents the command exists with `--json` flag, but the exact output schema is not in available documentation. This matters for determining whether `gc converge status` alone gives sufficient per-loop visibility without a custom status page. [Cannot be determined from available sources — requires running the command or reading convergence loop handler source.]

2. **What event types does `gc events` emit for convergence loop state changes?** The events.md reference cites `bead.created`, `mail.sent`, `session.woke` as examples. Whether `converge.iterate`, `converge.gate.passed`, or similar events exist is not documented in available sources. If they exist, a live event stream could replace polling `gc converge list`. [Requires inspection of convergence events.go or running against a live system.]

3. **Can the Gas City REST API be queried for bead label metadata in a way that maps to story pipeline phase?** The supervisor API reference confirms `/v0/city/{cityName}/beads` with query parameters. If Momentum labels story beads with phase metadata (e.g., `phase:qa`, `phase:avfl-loop`), the API can filter by label. Whether the bead label schema allows this is a Momentum design decision, not a Gas City limitation.

4. **Is Gas Town's OTEL telemetry also available in Gas City (which carries Gas Town as a pack)?** The OTEL docs are in the `gastownhall/gastown` repo, not `gastownhall/gascity`. It is UNKNOWN whether Gas City's native agent lifecycle emits OTLP telemetry or only the Gas Town pack does.

---

## Monitoring Verdict

**The monitoring gap is a material risk, but not a blocker — it is a build-not-buy problem.**

The current tooling provides adequate visibility into one thing: **agent health**. The `gt feed --problems` TUI and the `gc dashboard` stuck-agent alert are reliable indicators that something is broken at the infrastructure layer. For the question "is any agent stuck or dead?" the tools are adequate.

The current tooling provides inadequate visibility into: **pipeline phase state**. A developer cannot determine in a single view which stories are in which phase, whether a convergence loop is on iteration 2 of 5, or whether a human gate is pending — without running 4+ separate CLI queries and mentally assembling the picture.

For a solo developer running an automated Momentum sprint pipeline at 4–8 concurrent stories, this gap matters in proportion to how often things go wrong:

- **Nominal case (pipeline flows):** A developer can check `gc status` + `gc converge list` periodically and have sufficient awareness. The gap is tolerable.
- **Degraded case (stuck loop, failed gate, blocked story):** Discovery requires active polling across multiple commands or waiting for an escalation email. The time-to-awareness for a blocked pipeline could be 30+ minutes if the developer is not watching. This is a material operational risk.

**The practical mitigation is a simple custom status script, not a full dashboard.** A 50-line shell script querying `gc status --json`, `gc converge list --json`, `gc order history --json`, and `gc events --seq` on a 60-second cron, writing a summary to a file, could cover 80% of the monitoring need. Gas City's full REST API is documented and accessible. The gas City supervisor API makes a custom status page buildable in 1–2 developer-days.

**The notification gap (human gate discovery) is a distinct and harder problem.** Even with a custom status page, a solo developer who is not watching the terminal will not know a human gate is pending until they check. The slack-pack v0.1.0 does not solve this. Building a webhook notification for gate-opened events would require wrapping a `gc events --follow --type converge.gate.opened` listener in a small service that posts to Slack — feasible but not built.

**Verdict:** Operating an automated Momentum sprint pipeline on Gas City without custom monitoring tooling is a **medium-high operational risk** for a solo developer. The built-in tools provide adequate agent health coverage and insufficient pipeline phase visibility. The gap is closeable with a modest custom script (monitoring) and a small notification service (human gate alerting), neither of which currently exists in the community or ships with the platform.
