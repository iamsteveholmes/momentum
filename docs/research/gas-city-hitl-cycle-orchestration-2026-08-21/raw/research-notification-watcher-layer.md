---
content_origin: claude-code-subagent
date: 2026-08-21
sub_question: "Notification and watcher layer: gate-bead bead.created events to human notification — what exists today (dashboard, gc events --follow, mail) and what Momentum would need to build"
topic: "Gas City HITL gates and cycle orchestration for Momentum"
---

## Bottom line

The notification substrate Momentum would need **already exists and is well-specified** — a typed event bus with `bead.created` carrying the full bead record, payload-level filtering that can select gate beads specifically, resumable SSE with cursors, and a writable bead REST surface for closing the gate and recording a verdict. What does **not** exist in any tagged Gas City release is the *reflex* that connects a created human gate to a notified human: as of `v1.4.1` (2026-08-15) creating a `type=human` gate produces zero notification. That reflex was written — two core-pack orders, `notify-on-human-gate-creation` and `renudge-stale-human-gates`, landed on `main` on 2026-07-23 — but it is **not in v1.4.0 or v1.4.1**; it ships only in the `edge` rolling-main pre-release the maintainers label "not for production."

Even with those orders, the last mile terminates at `gc mail send human`, which writes a mail bead into a `human` inbox that nothing surfaces outside the city. Gas City's own code comments say so: humans "have no session to poke." So the honest gap statement for Momentum is not "build a watcher" — the watcher is a 222-line shell script that exists upstream (line count corrected for consistency during AVFL fix pass — MIN-007) — it is **build the last mile and the verdict return path**, which for Momentum's anti-rubber-stamp gate is the harder half.

**Environment note (MIN-005, added during AVFL fix pass):** this file's Confidence section below states `gc events --follow` behavior was not verified because `gc` was not installed during this sub-question's own research session (2026-08-21). A later probe session (2026-08-24) installed `gc` 1.4.1 globally and exercised it live in a throwaway city — see `research-verification-probes.md`. That session did not specifically re-verify `--payload-match bead.issue_type=gate`, so the caveat below about confirming the selector before building on it still stands, but the broader "gc is not installed" framing is now stale as of 2026-08-24.

---

## The event bus contract: what a gate bead looks like on the wire

The authoritative catalog is the published OpenAPI document, not the prose reference page. The city event stream's `TypedEventStreamEnvelope` is a discriminated union with **91 event types** in its `discriminator.mapping` ([openapi.json](https://raw.githubusercontent.com/gastownhall/gascity/main/docs/reference/schema/openapi.json)) **[OFFICIAL]**. Ten are bead events: `bead.created`, `bead.closed`, `bead.updated`, `bead.deleted`, `bead.claim_rejected`, `bead.claim_released`, `bead.dead_assignee_reopened`, `bead.worktree.reaped`, `bead.worktree.reap_skipped`, plus `beads.conditional_writes.degraded`.

**There is no `gate.*` event type.** A gate is not a first-class event citizen — it is a bead whose `issue_type` is `gate`, so it arrives on the wire as an ordinary `bead.created`. **[OFFICIAL]**

The envelope for a city-scope stream line is:

```
{ seq, type, ts, actor, subject, message, payload,
  session_id, step_id, run_id, depends_on_step_ids, workflow }
```
with `seq`, `type`, `ts`, `actor` required, and `payload` additionally required on the `bead.created` variant **[OFFICIAL]**. For `bead.created` the payload is `BeadEventPayload` = `{ bead: Bead }`, and `Bead` carries `id, title, status, issue_type, created_at` (required) plus `assignee, labels, metadata, dependencies, needs, is_blocked, parent, priority, description, defer_until, ephemeral, ref, from, no_history, updated_at` **[OFFICIAL]**.

Two consequences matter for a Momentum watcher:

1. **`metadata` is a flat `string → string` map.** Verdict text, fork identifiers, and a pointer to the rendered decision surface all have to be serialized into string values. There is no nested-object metadata.
2. **The `bead.created` payload does not carry `await_type`.** The gate's human/timer/`gh:*` discriminator lives on the bead record but is not in the event payload — Gas City's own notifier explicitly re-fetches the bead to learn it: *"the bead.created payload omits await_type, so the event alone cannot tell a human gate from a timer/gh gate"* ([notify-on-human-gate-creation.sh](https://raw.githubusercontent.com/gastownhall/gascity/main/internal/bootstrap/packs/core/assets/scripts/notify-on-human-gate-creation.sh)) **[OFFICIAL]**. Any watcher is therefore a two-hop read: event → re-fetch.

The envelope also carries `workflow` (a `WorkflowEventProjection` with `workflow_id`, `root_bead_id`, `logical_node_id`, `step_ref`, `changed_fields`, `watch_generation`) and `step_id`/`run_id`/`depends_on_step_ids` **[OFFICIAL]**. For a gate synthesized by a formula step this is the thread back to *which sprint phase* is blocked — exactly what a companion decision surface needs in its header.

---

## `gc events --follow` as the watcher substrate

`gc events` is documented as "a CLI reflection of the supervisor event APIs" with an explicit output contract **[OFFICIAL]** ([reference/events](https://docs.gascity.com/reference/events)):

- **List mode** (`gc events`) emits JSON Lines, one `TypedEventStreamEnvelope` per line in city scope; empty stdout on no match.
- **Stream mode** (`--watch`, `--follow`) emits one SSE envelope (`EventStreamEnvelope`) per line. Heartbeat frames are consumed internally and never reach stdout — a real convenience versus raw SSE.
- **Cursor mode** (`--seq`) prints a bare `X-GC-Index` integer (city) or a composite cursor like `alpha:4,beta:9,mc-city:21` (supervisor).

Filter flags — `--type`, `--since`, `--payload-match`, `--after`, `--after-cursor` — "only filter which objects are emitted. They do not change the JSON shape" **[OFFICIAL]**. Critically, `--payload-match` "accepts top-level fields and dotted paths into nested payload objects. For example, use `--payload-match bead.issue_type=task` to match bead events by issue type" **[OFFICIAL]**.

That yields the exact selector a Momentum gate watcher wants:

```
gc events --follow --type bead.created --payload-match bead.issue_type=gate
```

`--watch` blocks until a match and exits (default `--timeout 30s`, tunable); `--follow` streams indefinitely. Resumption uses `--after <seq>` (city) or `--after-cursor <composite>` (supervisor); with neither, "API streams … start at the current event head" **[OFFICIAL]** — so a watcher that restarts without persisting a cursor silently misses gates created during the gap.

A caveat worth carrying: `gc events` has a **local fallback path** used when the supervisor API is down, and the payload shape differs there. The upstream notifier normalizes with `(.payload.bead // .payload)` and comments that fallback mode "is exactly when notifications matter most" **[OFFICIAL]**. Any Momentum watcher must handle both shapes.

---

## Two other watcher substrates

**SSE directly.** `GET /v0/city/{cityName}/events/stream` emits `event: event` frames with `EventStreamEnvelope` plus `event: heartbeat`; the supervisor-scope `GET /v0/events/stream` emits `event: tagged_event` with a `city` field added. Resumption is `Last-Event-ID` or `after_seq`/`after_cursor`; the bus stream "replays from the last received index" **[OFFICIAL]** ([reference/api](https://docs.gascity.com/reference/api)). Mutations require an `X-GC-Request` anti-CSRF header (any non-empty value); every response carries `X-GC-Request-Id`. Errors are RFC 9457 Problem Details with a stable `urn:gascity:error:<code>` type — branch on `code`, not prose **[OFFICIAL]**.

**Long-poll on the beads list.** Less advertised but arguably simpler for a single-gate watcher: `GET /v0/city/{cityName}/beads` accepts `type`, `status`, `label`, `assignee`, `rig` filters *and* `index` ("Event sequence number; when provided, blocks until a newer event arrives") with `wait` ("How long to block waiting for changes … Default 30s, max 2m") **[OFFICIAL]**. A poll of `?type=gate&status=open&index=N&wait=30s` gives change-triggered gate discovery with no stream to keep alive and no cursor file to corrupt — at the cost of a 2-minute ceiling per call.

**Writing back.** The bead surface is mutable over HTTP: `POST /bead/{id}/close`, `POST /bead/{id}/reopen`, `POST /bead/{id}/assign`, and `POST /bead/{id}/update` with a `BeadUpdateBody` that includes `metadata` ("Metadata key-value pairs to set"), `labels`, `remove_labels`, `status`, `assignee` **[OFFICIAL]**. So *resolve the gate and record the verdict* is two authenticated POSTs — no CLI shell-out required.

---

## `bd show --watch` and `bd gate` — the local layer

Gas City's orientation page names three human-facing observation surfaces: "Humans watch the stream with `bd show --watch`, the `gc events --follow` CLI, or the dashboard" **[OFFICIAL]** ([how-gas-city-works](https://docs.gascity.com/getting-started/how-gas-city-works)).

I exercised the bd half directly against the `bd` Momentum already has installed (mise github backend, **v1.0.4**) **[EMPIRICAL]**:

- `bd show <id> -w/--watch` = "Watch for changes and auto-refresh display" — a redraw loop over one bead, not an event subscription. `bd --help` lists no `events` command: **bd has no event bus of its own.** Every event in this story is emitted by the Gas City supervisor, not by beads.
- `bd gate` is real and fully implemented: `create`, `list`, `check`, `resolve`, `show`, `add-waiter`, `discover`. Gate types are `human`, `timer`, `gh:run`, `gh:pr`, `bead`.

A gate I created in a throwaway repo **[EMPIRICAL]**:

```
$ bd gate create --type=human --blocks gl-03n --reason="Pre-sprint plan gate: developer must write per-fork verdicts"
✓ Created gate gl-qnc (type: human)

$ bd gate list --json
[{ "id":"gl-qnc", "title":"Gate: human", "status":"open",
   "issue_type":"gate", "await_type":"human",
   "description":"Ad-hoc gate blocking gl-03n\n\nReason: Pre-sprint plan gate: …" }]
```

`bd ready` returned `[]` and `bd blocked` reported `gl-03n` with `blocked_by:["gl-qnc"]`; after `bd gate resolve gl-qnc -r "approved: verdicts written"` the story returned to `bd ready` **[EMPIRICAL]**. The gate primitive works.

Two negative results matter more:

- **`bd gate check` refuses to touch human gates.** On a database containing exactly one open human gate it printed `Checked 0 gates: 0 resolved, 0 escalated, 0 errors` **[EMPIRICAL]**. Its help confirms the design: it evaluates `gh`, `gh:run`, `gh:pr`, `timer`, `bead` — human gates "require manual `bd gate resolve`."
- **`bd gate wake` does not exist as a command in v1.0.4.** `bd gate add-waiter`'s help says "When the gate closes, the waiter will receive a wake notification via `bd gate wake`," but `bd gate wake --help` falls through to the parent gate help **[EMPIRICAL]**. And the waiter mechanism runs the wrong direction for us anyway: it wakes *agents* when a gate *closes*, not humans when a gate *opens*.

The formula v2 spec matches this: `[steps.gate]` "synthesizes a real gate bead that blocks its step until the gate bead is closed (manually or by an external watcher), but the `type` values `gh:run`, `gh:pr`, `timer`, `human`, and `mail` are doc-comment vocabulary … the parser never validates them and no bundled watcher acts on them. **Zero bundled formulas use `gate`**" **[OFFICIAL]** ([formula-spec-v2](https://docs.gascity.com/reference/specs/formula-spec-v2)). The spec files this under a section explicitly headed as parsed-but-no-runtime-consumer surface — authors "should not rely on them."

---

## Mail as human notification — and where the last mile stops

Mail is a bead: "Carrier: a bead in the store," survives a crash, has a subject, "stays unread until processed," and — the load-bearing row — "**Wakes the recipient: No by itself; `--notify` can request a managed wake**" **[OFFICIAL]** ([tutorial 04](https://docs.gascity.com/tutorials/04-communication)). Delivery to an *agent* happens through a hook: on each turn `gc mail check --inject` surfaces unread mail as a system reminder in the agent's context.

There is no equivalent injection for a person. Gas City's core escalation hook is four lines of shell whose terminal action is `gc mail send "${GC_ESCALATION_RECIPIENT:-human}"` ([escalate.sh](https://raw.githubusercontent.com/gastownhall/gascity/main/internal/bootstrap/packs/core/assets/scripts/escalate.sh)) **[OFFICIAL]**. And the notifier comments state the constraint plainly: `gc mail send --notify` "mails the addressee and nudges them when they are a real session — and **deliberately skips the tmux-nudge for the `human` recipient (humans have no session to poke; cmd_mail.go guards `to != "human"`)**" **[OFFICIAL]**.

So "notify the human" in stock Gas City means: a row appears in `gc mail inbox human`, discoverable only by someone who runs that command or opens the dashboard. There is no push, no OS notification, no email/SMS bridge in core.

The escape hatch is the external-messaging fabric. `POST /v0/extmsg/clients` + `GET /v0/extmsg/{provider}/{account_id}/{conversation_id}/subscribe` + `POST /v0/extmsg/inbound` give a registered external LLM client a bidirectional SSE conversation with a city session **[OFFICIAL]**, and `city.toml`'s `[extmsg] default_route` can bind unbound inbound conversations to an agent (the example provider named is `telegram`) **[OFFICIAL]** ([config reference](https://docs.gascity.com/reference/config)). The public registry ships `slack-mini`, `slack-channel`, `slack-full`, and `discord` packs; `slack-mini` documents an outbound verb — `gc slack-mini post-message --channel C0123 --text "…"` — reachable in ~3 minutes of setup with four env vars ([slack-mini README](https://github.com/gastownhall/gascity-packs/tree/main/slack-mini)) **[OFFICIAL]**. That is a genuine last mile, but nothing wires it to gates: it is a verb you must call yourself.

A cleaner seam than patching the notifier: the bus emits `mail.sent` with the recipient in the envelope's `subject` field (the documented example is `{"actor":"human","subject":"mayor","type":"mail.sent",…}`) **[OFFICIAL]**. A single Momentum-side process on `gc events --follow --type mail.sent` filtering `subject == "human"` catches *every* escalation — gate creation, stale-gate re-nudge, and any future core escalation — at one place, and forwards to whatever the developer actually watches.

---

## The dashboard's treatment of blocked/gated work

The supervisor ships a single-page dashboard compiled into the `gc` binary, served at `http://127.0.0.1:8372/`, opened via `gc dashboard` (`--no-open` prints the URL) **[OFFICIAL]** ([dashboard](https://docs.gascity.com/getting-started/dashboard)). It "reads the supervisor's typed API directly (same origin), so it reflects live state: **agents and their sessions, beads, mail, formula runs, and a health view**."

That enumeration has no gate view, no blocked-work queue, and no notification/alerting surface — and the docs describe nothing gate-specific anywhere on the page **[OFFICIAL]**. What it does have: same-origin mutations carrying the `X-GC-Request` CSRF header, so mutating controls exist; and a read-only degradation when bound to a non-localhost address without `allow_mutations`. It binds loopback by default and is "intended for local, single-operator use." `GC_SUPERVISOR_DASHBOARD=0` disables it. I could not enumerate the dashboard's component tree — no `web/`, `ui/`, or `internal/dashboard/` path exists at the repo root and code search requires auth — so "no gate view" rests on the documentation's own enumeration rather than on source **[UNVERIFIED as to source; OFFICIAL as to docs]**.

For Momentum the deeper problem is not the missing view but the *addressing model*: a loopback single-operator dashboard is exactly wrong for the case that motivates Gas City at all — a cycle running out-of-session while the developer is elsewhere.

---

## What already exists upstream (and why you probably can't have it yet)

The strongest finding of this sub-question. Gas City's bundled `core` pack on `main` ships three gate-related orders ([core/orders](https://github.com/gastownhall/gascity/tree/main/internal/bootstrap/packs/core/orders)) **[OFFICIAL]**:

| Order | Trigger | What it does |
|---|---|---|
| `gate-sweep` | cooldown 30s | `gc bd gate check --type=timer --escalate`; `--type=gh --escalate`. Human gates deliberately excluded. `--type=bead` is commented out pending a beads fix. |
| `notify-on-human-gate-creation` | **event, `on = "bead.created"`** | Mails + nudges the addressee the moment a human gate bead is created. |
| `renudge-stale-human-gates` | cooldown 5m | Re-notifies any human gate still open past a staleness threshold (default re-nudge interval 1h via `GC_STALE_GATE_RENUDGE_INTERVAL`). |

The `notify-on-human-gate-creation.toml` header is an unusually candid statement of the gap this sub-question asks about: *"Without it, creating a `type=human` gate produces ZERO notification — the gate bead is built, the blocks edge is added, a line prints to stdout, and the human who must resolve it is never told (proven ABSENT in gascity/beads: gate creation has no post-create notify hook; the only gate watcher skips human gates entirely). Doctrine compensates by hand … this ships that reflex."* **[OFFICIAL]**

Its 222-line implementation is a near-exact template for what Momentum would otherwise write: pull `gc events --type bead.created --since 5m`; `jq` down to beads where `issue_type == "gate"`; re-fetch each via `gc bd show --json` to read `await_type` and `status`; keep only open human gates; resolve the addressee (`assignee` → `gc.deferred_assignee` metadata → `${GC_ESCALATION_RECIPIENT:-human}`); send `gc mail send <addressee> -s "Human gate awaiting you: <id>" -m "…Resolve with: gc bd gate resolve <id>" --notify`; dedup in an atomically-written JSON state file under `$GC_PACK_STATE_DIR`; prune by retention; **exit non-zero on any undeliverable send** because "the controller captures an exec order's combined output but only logs it on a non-zero exit" **[OFFICIAL]**. It also handles cross-rig gates via a prefix→rig lookup from `gc rig list --json`.

**The release gap.** I enumerated `internal/bootstrap/packs/core/orders` at both release tags **[EMPIRICAL]**: `v1.4.1` and `v1.4.0` contain `gate-sweep.toml` but **not** `notify-on-human-gate-creation.toml` or `renudge-stale-human-gates.toml`. Raw fetches of those two files at `v1.4.1`, `v1.4.0`, and `v1.3.5` all return **404**, while `gate-sweep.toml` at `v1.4.1` returns 200 **[EMPIRICAL]**. The commit that added them (`741a2d9d`, PR #4553, "feat(orders): notify the addressee on human-gate creation + re-nudge stale human gates") is dated **2026-07-23**, one day before v1.4.0 was published — so it missed that cut and has not landed in a release since. Latest release is **v1.4.1, 2026-08-15** **[OFFICIAL]**. The only build carrying the reflex is the `edge` rolling-main pre-release, rebuilt from main today (asset timestamp 2026-08-21T23:44Z) and described in its own release notes as "Pre-release for cross-version contract radars; **not for production**" **[OFFICIAL]**.

Repo health context: gascity is public, was pushed to minutes before this research ran, and carries **1,011 open issues** — the `repos/…/open_issues_count` figure, which includes open PRs alongside open issues (query method annotated during AVFL fix pass — MAJ-004; `research-maturity-open-bugs.md` separately reports **575** via the search-API `is:issue is:open` query, which excludes PRs — the two are not in conflict, they count different things) **[EMPIRICAL, GitHub API]**.

---

## What Momentum's human-gate watcher would actually have to do

Momentum's current plan gate is a rendered HTML page — `.momentum/handoffs/{sprint_slug}-plan-gate.html`, 20–43 KB in practice (`sprint-2026-08-03-plan-gate.html` is 35 KB; end-gate reports run to 780 KB) **[EMPIRICAL, local files]**. It is opened as a `file://` URL in a cmux browser surface. Its sign-off block requires a written one-line verdict per genuine fork before the submit button enables, then the button's only action is `navigator.clipboard.writeText(...)` and the page instructs: *"copy and paste the decision text back into the chat"* ([plan-gate-renderer.md](/Users/steve/projects/momentum/skills/momentum/skills/sprint-planning/references/plan-gate-renderer.md)) **[EMPIRICAL, local source]**.

**That clipboard-into-a-live-session hop is the thing Gas City breaks.** Out-of-session there is no chat to paste into. Everything else — notification, blocking, release — Gas City already models; the verdict *return* path does not exist in any form.

### Gap list

1. **Verdict return path — the real work.** Gate closure must become a machine-readable write: `POST /v0/city/{c}/bead/{id}/update` with `metadata` carrying per-fork verdicts (string values only — serialize), then `POST /bead/{id}/close`. The gate page must become a served page (not `file://`) that can issue those two authenticated calls with an `X-GC-Request` header, or must write a verdict file that a small local daemon relays. **Absent entirely.**
2. **Last-mile delivery.** `gc mail send human` is a row in an inbox nobody watches. Needs either a `mail.sent`-where-`subject == "human"` forwarder into a real channel, or `slack-mini post-message` wired into the notify path. **Absent in core; substrate available.**
3. **Release availability.** The upstream notifier is main-only. Adopting it means running `edge` (explicitly not-for-production) or vendoring the two order files plus their scripts into a Momentum-owned pack. Vendoring is the lower-risk call and is a supported pattern — packs override by import order.
4. **Surface addressing.** The gate bead must carry a pointer to the rendered companion decision surface (`metadata` key holding a URL or path) so the notification is actionable, and the surface must be reachable from wherever the developer is. Loopback-only serving defeats out-of-session orchestration.
5. **Cursor durability.** `gc events` streams start at head with no cursor. A restarted watcher misses gates created in the gap. `--seq` + persisted cursor, or long-poll on `GET /beads?type=gate&status=open&index=N&wait=30s`, closes this.
6. **Three-way verdicts.** Momentum's gate offers Approve / Modify / Re-run AVFL. A gate bead has two terminal states (open/closed). Modify and Re-run need a convention — verdict metadata plus a `bd gate reopen`/new-gate cycle, or a labeled close that a downstream formula step branches on. **No upstream convention exists.**
7. **Mid-story tooling gates.** For nornspun/chorgi-class stories the developer must exercise a live tool, which means the gate notification has to carry launch instructions and the city has to hold the worktree open. Not a notification problem per se, but it lands on the same bead.

### Glue scope estimate

- **Watcher + notifier (adapted from upstream):** ~1–2 days. The 222-line reference implementation is directly reusable; the change is swapping the `gc mail send` terminal for a real channel and adding the surface-URL metadata read.
- **Last-mile channel:** ~0.5–1 day for `slack-mini` (four env vars plus a public endpoint via Tailscale Funnel per its README), or ~0.5 day for a local forwarder that fires an OS notification off `mail.sent`.
- **Verdict capture + write-back:** ~3–5 days, and this is where the risk concentrates. It means re-targeting the plan-gate renderer from a `file://` clipboard page to a served page with two authenticated POSTs, deciding the metadata schema for per-fork verdicts, preserving the anti-rubber-stamp enable-gate, and defining Modify / Re-run semantics against a two-state bead.
- **Cursor durability + idempotence + restart tests:** ~1 day.

**Total ≈ 6–9 days** of glue for one gate type, most of it in the verdict path rather than the watcher. **[Reworded during AVFL fix pass — ACCURACY2-A-010; the original "neither is true in Momentum today" framing is stale.]** That estimate assumes `gc` is installed globally and a live Momentum city is running: `gc` 1.4.1 is in fact now installed (via `mise`, per `research-verification-probes.md`), but no live Momentum city exists yet — the running-city half of that assumption still does not hold, and neither the install nor the city-standup effort is costed here.

---

## Confidence and limitations

Event contract, CLI framing, API surface, dashboard scope, mail semantics, and the core-pack order inventory are all read from primary sources dated within the last month (docs site `llms-full.txt` retrieved 2026-08-21; `openapi.json` and pack sources from `main`; release metadata from the GitHub API). The bd gate behaviors are first-hand against bd v1.0.4. The one claim I could not source-verify is the dashboard's lack of a gate/blocked view — no dashboard source path is exposed at the repo root and GitHub code search requires authentication, so that rests on the documentation's own enumeration of dashboard surfaces. I did not install `gc` (that is sub-question 1's job), so nothing here about `gc events --follow` behavior is empirical — the framing contract is documented precisely enough that I treated the reference page as authoritative, but a hands-on pass should confirm `--payload-match bead.issue_type=gate` actually selects gate beads before that selector is built on.

---

## Sources

- [gc events Output Formats — reference/events](https://docs.gascity.com/reference/events)
- [Supervisor REST API — reference/api](https://docs.gascity.com/reference/api)
- [openapi.json (supervisor OpenAPI 3.1 contract)](https://raw.githubusercontent.com/gastownhall/gascity/main/docs/reference/schema/openapi.json)
- [events.json (gc events JSONL line schema)](https://raw.githubusercontent.com/gastownhall/gascity/main/docs/reference/schema/events.json)
- [Web dashboard — getting-started/dashboard](https://docs.gascity.com/getting-started/dashboard)
- [How Gas City Works — the six primitives](https://docs.gascity.com/getting-started/how-gas-city-works)
- [Tutorial 04 — Agent-to-Agent Communication](https://docs.gascity.com/tutorials/04-communication)
- [Tutorial 07 — Orders](https://docs.gascity.com/tutorials/07-orders)
- [Gas City Formula Specification — v2](https://docs.gascity.com/reference/specs/formula-spec-v2)
- [Builtin Packs — reference/system-packs](https://docs.gascity.com/reference/system-packs)
- [Gas City Configuration — reference/config](https://docs.gascity.com/reference/config)
- [Connect an external LLM client — guides/connected-clients](https://docs.gascity.com/guides/connected-clients)
- [Find and Import Public Packs — guides/registry-showcase](https://docs.gascity.com/guides/registry-showcase)
- [core pack orders directory (main)](https://github.com/gastownhall/gascity/tree/main/internal/bootstrap/packs/core/orders)
- [notify-on-human-gate-creation.toml](https://raw.githubusercontent.com/gastownhall/gascity/main/internal/bootstrap/packs/core/orders/notify-on-human-gate-creation.toml)
- [notify-on-human-gate-creation.sh](https://raw.githubusercontent.com/gastownhall/gascity/main/internal/bootstrap/packs/core/assets/scripts/notify-on-human-gate-creation.sh)
- [renudge-stale-human-gates.toml](https://raw.githubusercontent.com/gastownhall/gascity/main/internal/bootstrap/packs/core/orders/renudge-stale-human-gates.toml)
- [gate-sweep.toml](https://raw.githubusercontent.com/gastownhall/gascity/main/internal/bootstrap/packs/core/orders/gate-sweep.toml)
- [gate-sweep.sh](https://raw.githubusercontent.com/gastownhall/gascity/main/internal/bootstrap/packs/core/assets/scripts/gate-sweep.sh)
- [escalate.sh](https://raw.githubusercontent.com/gastownhall/gascity/main/internal/bootstrap/packs/core/assets/scripts/escalate.sh)
- [gascity releases (v1.4.1, 2026-08-15; edge rolling-main)](https://github.com/gastownhall/gascity/releases)
- [gascity issue #4543 — loud-fail guard for drained/terminated session wakes](https://github.com/gastownhall/gascity/issues/4543)
- [gascity-packs — slack-mini](https://github.com/gastownhall/gascity-packs/tree/main/slack-mini)
- Local: `bd version 1.0.4`; `bd gate --help`, `bd gate create/list/check/resolve` transcripts (2026-08-21)
- Local: `/Users/steve/projects/momentum/skills/momentum/skills/sprint-planning/references/plan-gate-renderer.md`
- Local: `/Users/steve/projects/momentum/.momentum/handoffs/sprint-2026-08-03-plan-gate.html`
