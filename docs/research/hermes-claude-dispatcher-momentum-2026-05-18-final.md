---
title: "Hermes-as-Dispatcher vs. Claude-Native: Research Synthesis"
topic: "Can Hermes run as a 24/7 dispatcher/delegate with Claude Code as planner/brains"
date: 2026-05-18
research_profile: heavy
verdict: DONT_ADOPT_HERMES
confidence: high
avfl_score: 68/100
followup_date: 2026-05-18
files_synthesized: 9
---

# Hermes-as-Dispatcher vs. Claude-Native: Research Synthesis

## 1. Verdict

**Do not adopt Hermes as the dispatcher/delegate. Build the Claude-native beads+Channel/SDK background daemon (Option B) that the prior dispatcher research already designed.** Hermes Agent is a genuinely well-engineered, MIT-licensed, local-capable 24/7 runtime whose Kanban resilience kernel (atomic claim, per-run retry rows, circuit breaker, crash recovery) is more mature than anything the Claude-native design ships. But against Momentum's specific constraints — solo dev, local-first, cost-sensitive, and *Claude-Code-skill-centric* — every Hermes advantage either evaporates or inverts: it adds a second authoritative state machine that collides with `index.json`/beads, it requires net-new unpaved integration glue to drive Claude Code, and it changes nothing about the Claude inference bill.

**One-sentence version a stakeholder can repeat:** *Hermes is a strong general-purpose autonomous-agent runtime, but for a Claude-skill practice it buys orchestration we'd have to hand-wire onto Claude Code while introducing a second source of truth — so we build the Claude-native dispatcher instead and borrow Hermes's best design ideas.*

## 2. Triangulation Reconciliation

The corpus contains 8 specialist discovery files (Claude-Code subagents, OFFICIAL-sourced) plus 1 Gemini deep-research file. **The Gemini file is a rejected outlier** and must not be used as decision evidence.

**Why Gemini reached the opposite conclusion.** Gemini recommends *"Adopt Asymmetric Integration: Claude Code (Planner) + Hermes (Delegate)"* — the inverse of the 8 specialist files' DON'T ADOPT. It got there by (a) never surfacing the state-ownership split-brain (the corpus's central disqualifying finding), (b) comparing Option B against the wrong comparand — Claude Code's "Agent View" preview feature rather than the beads+Channel/SDK dispatcher actually under evaluation [H-007], and (c) mis-rating Hermes as "production-ready / enterprise-grade" when it is openly pre-1.0 with biweekly breaking changes [H-001].

**Confirmed fabrications that disqualify Gemini as a reliable source** (AVFL C-002 through C-004, H-002/H-003):

| # | Fabrication | Reality (OFFICIAL) |
|---|---|---|
| 1 | REST endpoint `/task/{id}/approve` | Does not exist in the Hermes API |
| 2 | Product "Flux" (MCP-first tracker) | Appears in no official Hermes documentation |
| 3 | "MCP Server Mode" lets Claude drive Hermes | Hermes is an MCP **client only**; the server-side protocol is ACP |
| 4 | 5 execution backends | Actually **7** (omits Daytona, Vercel Sandbox) |
| 5 | Column name "In Progress" | Actual enum value is `running` (string-match break risk) |
| 6 | "Production Ready / enterprise-grade" | Pre-1.0, breaking changes ~biweekly |
| 7 | Claude-native rated "Poor" on local-only | Actual: **parity** (both are local-loop / networked-inference) |
| 8 | beads attributed to "Steve Yegge"; framed adversarially without DEC-028 context | Unverified attribution; missing project context |

Gemini also has structural defects: all 97 inline citations are orphaned (reference list lost in browser extraction), no provenance tags, no Markdown heading structure.

**Trust the 8-file constellation.** The AVFL report states plainly: *"The discovery corpus (files 1–8) is sound … internally consistent, evidence-tagged, and reaches an unambiguous verdict."* Where Gemini agrees with the specialists (Hermes is local-capable, model-agnostic, git-worktree-based, has a 60s dispatcher), it is corroborated and usable as `[PRAC]`; every Gemini-only claim is `[UNVERIFIED]` and excluded from this synthesis's reasoning.

## 3. Hermes: What It Actually Is

**Disambiguation first:** "Hermes 4" is an open-weight LLM family (a model you run); **"Hermes Agent"** is the self-hosted agent runtime (the product this decision is about). They are model-agnostic — Hermes Agent can run on Claude, GPT, local Llama, or Hermes 4. [OFFICIAL]

**Architecture.** A three-tier design: entry points (`cli.py`, `gateway/run.py`, ACP adapter, batch runner) → a single shared `AIAgent` core (synchronous orchestration loop) → subsystems (70+ tools, SQLite+FTS5 session storage, provider resolution, plugins). The core natively speaks `chat_completions`, `codex_responses`, **and `anthropic_messages`** — so Hermes can call Claude directly. The Kanban board is a per-board SQLite DB (`~/.hermes/kanban.db`) with `tasks`, `task_runs` (one row per attempt), `task_links` (untyped parent→child DAG), `task_events` (append-only, monotonic-id, `since=` cursor), and `task_comments`. Hermes is an **MCP client only** (it consumes tools, does not serve them); it runs as an **ACP server** over stdio for editors. [OFFICIAL]

**The 7 backends.** `local | Docker | SSH | Singularity | Modal | Daytona | Vercel Sandbox`. Local = no isolation; Docker = namespace sandbox; SSH/Modal/Daytona/Vercel = separate-machine isolation. Daytona/Modal hibernate when idle ("costs nearly nothing"). [OFFICIAL]

**Runtime model.** Continuous operation = the **gateway daemon** (`hermes gateway start`), which embeds the Kanban dispatcher by default (`dispatch_in_gateway: true`, **60s tick**). The dispatcher tick, in order: reclaim stale claims → reclaim crashed workers → promote `todo→ready` (all parents `done`) → atomically claim a `ready` task in `BEGIN IMMEDIATE` → spawn the assigned profile. **Claim is dispatcher-centralized and atomic** — there is no "agent picks up its own card" path. Parallelism is keyed to **distinct assignee identities**, not ready-frontier width; within one assignee, execution appears serial (`[UNVERIFIED]` — tutorial-implied, not a documented invariant). "24/7" is an OS-level concern (systemd on Linux; **launchd on macOS is a flagged, less-documented gap**), not managed uptime. [OFFICIAL]

**Maturity reality.** Pre-1.0 (`v0.14.0` / `v2026.5.16`). ~8,757 commits, ~13 releases in ~9 weeks (one every ~8–9 days), 215–295 contributors per cycle — but founder `teknium1` authors roughly half of all commits (bus-factor risk). Multiple practitioner reviews: *"breaking changes every two weeks on the main release branch."* The in-source circuit-breaker contradiction (2 vs 3 vs 5) is direct evidence of doc-vs-code drift under this velocity. Well-funded (Nous: ~$70M raised, ~$1B valuation) so runway risk is low; **stability risk is high**. [OFFICIAL maturity signals; `[PRAC]` stability reviews]

## 4. Why Hermes-as-Delegate Fails for Momentum

Five structural incompatibilities, each independently sufficient to disqualify Hermes as the runtime.

**4.1 State-ownership split-brain (the decisive finding).** Hermes Kanban *insists* on owning lifecycle truth — *"worker lanes execute but never own that truth"* [OFFICIAL]. Momentum already has a designated single source of truth under the sole-writer sprint-manager: today `index.json` is authoritative with beads as best-effort shadow (DEC-028 dual-write spike); post-spike beads becomes authoritative. Putting Hermes *also* in an authoritative position creates a **three-way split-brain** (`index.json` ⇄ beads Dolt DB ⇄ Hermes `kanban.db`), each with its own claim engine and `todo→ready` promotion. There is **no clean reconciliation key** — beads issue IDs and Hermes task IDs are independent namespaces, and Hermes's `task_runs` retry history has no beads analog. The only non-forking topology is "Hermes board = sole truth, beads demoted to a planning input" — which throws away the just-validated dispatcher design's entire state layer. [OFFICIAL + PRAC]

**4.2 Sprint-model mismatch.** A Momentum sprint is a **frozen-scope batch**: sprint-planning locks a story set (`sprints/index.json` `active.locked: true`, per-story approval-SHA gates), and sprint-dev drains that frozen set in dependency-ordered `waves[]`. Hermes Kanban is the **opposite by design**: a continuous board where work is added anytime and the dispatcher promotes the ready frontier *continuously* — no batch boundary, no freeze, no approval gate. There is **no Hermes concept that maps to a sprint or a wave** (the deepest mismatch). A faithful Hermes projection would either erase the freeze invariant or require a synthetic label Hermes's promotion engine would ignore — promoting stories *outside* the current sprint's frozen scope. [OFFICIAL]

**4.3 Worker-lane gap.** A Hermes lane requires (1) an assignee = a **Hermes profile**, (2) a spawn mechanism (`hermes -p <assignee> chat -q <prompt>`), (3) a lifecycle terminator (`kanban_complete`/`kanban_block`/crash). Momentum's workers are **Claude Code subagents running SKILL.md workflows** — not Hermes profiles. The docs are explicit that wiring a non-Hermes CLI (Claude Code/Codex/OpenCode) is **"not yet a paved path"** — wrapping the Claude exit into `kanban_complete`/`kanban_block`, mapping `HERMES_KANBAN_WORKSPACE`, auth, and per-CLI policy are all net-new per-integration work. An official Hermes "Claude Code skill" exists but documents *how to drive Claude Code*, not a turnkey lane. Worse: Momentum's in-process subagent fan-out / `TeamCreate` / AVFL patterns are invisible to Hermes — it sees one PID, one outcome. [OFFICIAL]

**4.4 FSM bypass.** Momentum's FSM is **enforced** — sprint-manager is the sole writer and rejects non-adjacent/backward transitions without `force`. Hermes Kanban's lifecycle is **advisory and openly writable**: *"every handoff is a row anyone (agent or human) can read and write,"* and the dashboard drag-drop does a *direct status write* through `kanban_db`. Hermes is **more permissive than beads** here (it adds a GUI write path), so it is a *larger* enforcement hole. A Hermes-authoritative model voids the sprint-manager sole-writer moat — Momentum's entire stated value. [OFFICIAL]

**4.5 Cost reality — the $0-local phantom.** Hermes's headline advantage is model-agnostic $0-local inference (local Ollama/vLLM). But under Momentum's constraints this is **inaccessible**: the dispatched work *is* Claude Code skills/subagents/hooks, which a non-Claude runtime cannot execute. If Hermes spawns `claude -p` workers, you are back in the exact Claude billing model — *Hermes adds no inference-cost relief, just a different orchestrator on top of the same Claude bill.* The $0-local win is only realized by abandoning the Claude-skill layer (a substantial capability downgrade, not a config flag). Additional cost hazards: the *"$1,800-in-two-days"* stray-`ANTHROPIC_API_KEY` incident applies fully; the Hermes Claude Code skill *confirms* unattended Claude needs `ANTHROPIC_API_KEY` + `--dangerously-skip-permissions` — the exact landmine; and parent-wakeup amplification can wake an Opus-tier planner once per child terminal event. [OFFICIAL + PRAC]

## 5. The One Technically Feasible Design (and Why It's Still Wrong)

**The inverted topology** (file 5). The Claude-plans/Hermes-delegates/Hermes-signals-back contract *is* feasible — but only inverted: Hermes owns operational state, and Claude is a Hermes **orchestrator-profile lane backed by `claude -p`**. Ingress is strong (idempotent `POST /api/plugins/kanban/tasks` with deterministic `--idempotency-key=momentum-<story-id>`, better than a filesystem watcher). 24/7 delegation is strong (literally what Hermes Kanban is built for).

**The parent-task-wakeup callback `[INVESTIGATED — does not exist as described]`.** The "decisive new fact" that would make the contract work: the originating task stays alive as the parent of every leaf, and *"when a watched task transitions to `done` or `blocked`, it injects a synthetic system message back into the orchestrator's ACP session."* This mechanism was investigated in a Gemini follow-up pass (2026-05-18). **ACP is not mentioned anywhere in 35k words of Hermes documentation. No "parent-task-wakeup" or orchestrator-session injection exists.** The actual callback path described is EXTERNAL: Hermes workers post to Claude Code Channels (`fakechat → http://localhost:8787`) after calling `kanban_complete`. This pushes a `<channel source="fakechat">` block into the Claude Code session — a custom integration requirement, not a native wakeup. Per the AVFL report and file 8: **the DON'T ADOPT verdict does not depend on this mechanism being absent** — the split-brain (4.1) and worker-lane gap (4.3) are independently disqualifying. This finding confirms the protocol requires a custom Channels integration rather than a native one.

**Why it's still wrong even if feasible.** Choosing it means (a) surrendering state ownership to Hermes's SQLite DB, (b) re-platforming execution off Claude skills onto Hermes profiles, (c) running two always-on daemons where one Agent-SDK-daemon-over-beads achieves the same loop natively. The valuable artifact is Hermes's *protocol*, not its engine.

**The three borrowed patterns worth adopting into the Claude-native design:**

1. **Per-run-attempt child tasks** — first-class `task_runs`-style attempt rows (strictly richer than Momentum's current re-spawn/quick-fix history).
2. **Structured handoff manifest** — `kanban_complete(summary, metadata={changed_files, verification, dependencies, residual_risk})` as a machine-readable downstream contract.
3. **Parent-wakeup concept** — a "live parent epic task that re-wakes the planner on child terminal events," implementable over beads + the Channel/SDK ingress already specified, with debounce (judge on *frontier* change, not per-leaf) and Haiku-tier triage of "does this require a plan change?".

## 6. What to Build Instead

**Build Option B — the Claude-native beads+Channel/SDK daemon** from `docs/research/claude-code-background-dispatcher-2026-05-17.md` §6 + Beads addendum.

**Recommended architecture in one paragraph.** A long-lived Agent SDK streaming-input daemon (or `claude -p` under launchd `KeepAlive`) blocked on a local queue; beads `.beads/hooks/on_update` as the push wake-source; idempotent claim-by-status (`bd ready --claim`) as the lock with a single sole-claimer + `flock`; hooks closing the loop; a startup reconcile sweep to compensate for lossy fire-and-forget hook delivery; and an OS scheduler (launchd/systemd) as the liveness watchdog. Borrow Hermes's per-run attempt rows, structured handoff metadata, stranded-task detection, and the live-parent-wakeup concept into this design.

**Why it fits Momentum's constraints.** It is *the architecture already designed for this exact codebase* — it slots into the existing `intake-queue.jsonl`/beads ingress without replacing it, every Momentum skill/subagent/hook runs natively because Option B *is* Claude Code, beads stays the single source of truth under the enforcing sprint-manager, and it is trivially reversible (glue over owned primitives, near-zero lock-in). Local-only is source-verified and spike-confirmed; the unattended-permission problem has spike-validated SDK `canUseTool` mitigations. No second daemon, no second state machine, no unpaved CLI-lane bridge.

## 7. Open Questions and Contingencies

Carried forward verbatim from the AVFL report — these gate any future reconsideration:

1. **parent-task-wakeup `[RESOLVED — does NOT exist as described]`** — Gemini follow-up (2026-05-18) found no ACP mechanism in 35k words of Hermes documentation. The actual callback is via Claude Code Channels external integration (`fakechat → localhost:8787`). This is a custom integration requirement, not a native wakeup. The DON'T ADOPT verdict does not depend on its absence; the split-brain (4.1) and worker-lane gap (4.3) remain independently disqualifying.
2. **Serial-vs-parallel per assignee `[RESOLVED — confirmed fan-out]`** — Gemini follow-up (2026-05-18) directly quotes the Hermes documentation: *"Independent, unlinked lanes are processed concurrently by the dispatcher, fanning out across multiple OS worker processes to maximize execution speed."* Multiple same-assignee tasks with no parent-child dependency run concurrently. Serial behavior requires explicit parent→child links. Hermes CAN run multiple same-assignee workers concurrently — this partially addresses one concern but does not change the overall DON'T ADOPT verdict.
3. **Circuit-breaker defaults — unresolved 3-way contradiction (2 vs 3 vs 5)** across official docs. Do not rely on any specific default without verifying against `docs/hermes-kanban-v1-spec.pdf` or current Hermes source. (Operator-overridable via `kanban.failure_limit` regardless.)
4. **beads SoT state** — `index.json` is currently authoritative; beads is the designated post-spike target (DEC-028 dual-write spike). The split-brain analysis and the Hermes-as-delegate verdict **apply in both the current and post-spike states**; beads SoT gates depend on the dual-write spike passing.
5. **Gemini file is an outlier** — all 8 factual fabrications and 4 structural defects are documented. Do not use Gemini-specific claims as decision evidence unless independently corroborated by the 8 specialist files.

## 8. Decision Table

Populated from file 7's head-to-head, corrected for the AVFL H-001 (maturity) and H-004 (local-only parity) fixes. Scoring 1–5, 5 = better for a solo-dev, local-first, Claude-skill-centric Momentum practice.

| Dimension | Hermes-as-Delegate (A) | Claude-Native Daemon (B) | Edge |
|---|---|---|---|
| **Local-only operation** | 4 — local loop, but adds unauth localhost HTTP surface | 5 — source-verified + spike-confirmed local; minimal surface | B (slight) |
| **Cost / $0-local** | 3 — real $0-local capability, unreachable without dropping the Claude-skill layer; with Claude workers = identical bill | 3 — no $0 path, but cost levers (Haiku-tier, cache) fully designed | Tie |
| **Autonomy (24/7, no-human)** | 5 — resilience kernel shipped (retry rows, circuit breaker, crash recovery, stranded detection) | 4 — equivalent achievable but designer-built | A |
| **Agentic-coding capability** | 4 — = Claude Code, but opaque-process control; in-process fan-out invisible | 5 — = Claude Code with direct agent-loop + permission control | B |
| **Operational risk** | 3 — handles more failures, but unauth dashboard + dual-dispatcher claim-race + contradictory defaults | 4 — fewer built-ins, smaller/better-characterized surface, spike-validated mitigations | B |
| **Maturity (real signals, H-001 corrected)** | 3 — pre-1.0, high-velocity (~8,757 commits, 295 contributors, PyPI) but 0.x, **breaking changes ~biweekly**, contradictory docs, unfinished external lane | 3 — mature core (Claude Code) but preview/pinned dispatcher glue (Channels, beads, SDK daemon) | Tie |
| **Local-only comparand (H-004 corrected)** | parity | parity (both local-loop / networked-inference) | Tie |
| **Integration / build effort** | 2 — net-new unpaved Claude lane + dual-state reconciliation | 4 — the prior-art-designed path, no re-platforming | B |
| **Reversibility / lock-in** | 3 — MIT, SQLite-inspectable, but 2nd system of record | 5 — glue over owned primitives, trivially reversible | B |

**Net:** Hermes wins on shipped resilience and time-to-autonomy. Option B wins on integration cost, reversibility, capability control, operational surface, and — decisively — fit with a Claude-skill-centric practice. The two ties (cost, maturity) do not rescue Hermes because its sole strong advantage (autonomy kernel) is recoverable as a *design borrow* at zero integration cost.

## 9. Sources

| File | Sub-question | Key verdict contribution |
|---|---|---|
| `research-what-hermes-is.md` | SQ1: Hermes architecture, backends, runtime model, license, cost | Establishes the 7 backends, gateway/60s-tick model, MIT license, model-agnostic local capability, and the launchd-on-macOS gap; flags $0-local as conditional |
| `research-kanban-board-mechanics.md` | SQ2: Kanban board/column/state model | Pins the 7-state enum, dispatcher-centralized atomic claim, per-run `task_runs` model, append-only `task_events`+cursor; confirms the in-source circuit-breaker contradiction |
| `research-worker-lanes.md` | SQ3: Concurrency, worker lanes, assignee model | Establishes lanes as order-blind dumb executors; the serial-vs-parallel-per-assignee `[UNVERIFIED]` highest-leverage unknown; untyped AND-only edges vs Momentum's typed beads graph |
| `research-external-integration-callback.md` | SQ4: External integration surface (MCP/ACP/API/callback) | Confirms MCP-client-only, ACP-server; Runs API as cleanest local ingress; **no native outbound webhook**; external CLI lane "not a paved path" |
| `research-claude-planner-hermes-delegate.md` | SQ5: Claude-as-planner + Hermes-as-delegate feasibility | The inverted-topology feasibility analysis; surfaces the `[UNVERIFIED]` parent-task-wakeup; concludes feasible-but-wrong-fit; recommends borrowing the protocol |
| `research-kanban-momentum-mapping.md` | SQ6: Hermes Kanban → Momentum concept mapping | The three-way split-brain analysis; frozen-sprint vs continuous-board mismatch; enforced-FSM bypass; safe topology = read-only beads→Hermes projection only |
| `research-hermes-vs-native-dispatcher.md` | SQ7: Head-to-head vs Claude-native dispatcher | The scored decision table; "Momentum-specific catch"; blunt BUILD-OPTION-B recommendation; the steal-the-ideas hedge |
| `research-cost-deployment-maturity.md` | SQ8: Cost, deployment, maturity realities | Real maturity signals (commits/contributors/cadence, bus-factor); pre-1.0 biweekly-breakage as dominant solo-dev risk; OAuth/cost paths |
| `gemini-deep-research-output.md` | Corpus-synthesis (outlier) | **Rejected triangulation source** — opposite conclusion, 8 confirmed fabrications, 4 structural defects; used only as a contrarian cross-check, never as evidence |
| `validation/avfl-report.md` | AVFL validation (8 validators, 1 fix pass) | Pre-fix 24 → post-fix 62/100, ADEQUATE_WITH_CONTINGENCIES; corpus 1–8 sound; carries the 5 synthesis contingencies in §7 |
