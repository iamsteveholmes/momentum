---
content_origin: claude-code-subagent
date: 2026-05-18
sub_question: "Hermes-based dispatcher vs Claude-native beads+Channel/SDK dispatcher — local, cost, autonomy, capability, risk, maturity?"
topic: "Can Hermes run as a 24/7 dispatcher/delegate with Claude Code as planner/brains, and can Hermes Kanban + worker lanes map onto Momentum?"
---

# Hermes-as-Delegate vs the Claude-Native beads+Channel/SDK Dispatcher

## Scope and Framing

This compares two concrete architectures for a 24/7, no-human, local-first work dispatcher feeding a Claude-Code-skill practice (Momentum):

- **Option A — Hermes-as-delegate.** Hermes Kanban (SQLite board + gateway-embedded dispatcher) owns the task lifecycle. Claude Code is the "brains": each card spawns a worker that runs `claude -p` (or interactive tmux) to do the actual coding/skill work. Hermes provides the durable queue, dependency promotion, run/retry rows, circuit breaker, crash recovery, and human-in-loop block/unblock. Per `hermes-kanban-discovery-2026-05-17.md`.
- **Option B — Claude-native dispatcher.** The fully-designed architecture in `claude-code-background-dispatcher-2026-05-17.md`: a long-lived Agent SDK streaming-input daemon (or `claude -p` under launchd) blocked on a local queue, with beads `.beads/hooks/on_*` as the push wake-source, hooks closing the loop, and an OS scheduler as liveness watchdog.

Both keep transport/queue/state local; only model inference traverses the network in either design. The decision turns on what each *adds* on top of that shared baseline. Tags: [OFFICIAL] = vendor docs/source, [PRAC] = practitioner/third-party report, [UNVERIFIED] = inferred or unresolved.

## Local-Only Operation (No External Network)

Both options satisfy the hard constraint that no external orchestration network is required — only LLM inference egresses.

**Option B** is the stricter local citizen because the native research report establishes its entire transport surface as local-by-construction: beads exec hooks fire in-process, the local Channel server binds `127.0.0.1` with "no Anthropic cloud in the event path" [OFFICIAL, source-read 2026-05-17 per `claude-code-background-dispatcher-2026-05-17.md`], and the Agent SDK streaming loop yields from local sources. The one cloud-bound alternative (Routines/RemoteTrigger) is explicitly disqualified in the prior art.

**Option A's** dispatcher loop is equally local: the Hermes gateway-embedded dispatcher "scans for eligible cards, claims one atomically, and starts the assigned profile" on the same host, with `~/.hermes/kanban.db` a local SQLite file and "single-host only" an explicit non-goal boundary [OFFICIAL, Hermes Kanban docs §12; corroborated [PRAC] glukhov.org 2026-05]. Hermes "itself does not do GPU inference — it is a gateway and orchestration layer" [PRAC], so the loop is network-free; only the worker's LLM call egresses. **Net: parity.** Both are local-loop / networked-inference. Option B's locality has been source-verified and spike-confirmed in the prior art; Option A's is documented but not independently spike-tested here ([UNVERIFIED] at the same evidentiary bar).

## Cost Model — Who Pays Inference; $0-Local Feasibility

This is where the two architectures diverge most sharply, and it cuts *in Hermes's favor on flexibility but not on the Momentum-specific reality*.

**Option B inherits the full Claude licensing reality** documented at length in `claude-code-background-dispatcher-2026-05-17.md`'s Cost & Licensing section: a sustained Agent SDK daemon **must** use a dedicated Anthropic API key on pay-as-you-go (subscription OAuth with the SDK libraries is prohibited; enforcement began 2026-01-09) [OFFICIAL]. From 2026-06-15 even first-party `claude -p` on a subscription draws a small fixed monthly Agent SDK credit at full API rates [OFFICIAL]. The "$1,800 in two days" stray-`ANTHROPIC_API_KEY` incident [PRAC, #43333/#37686] is the headline hazard. There is **no $0-local path** for Option B that preserves the Momentum skill layer — the prior art's Lever-1 conclusion is Haiku-tiered + cache-stable all-Anthropic, ~order-of-magnitude cheaper than all-Opus but never free.

**Option A's cost story is structurally more flexible** because Hermes is model-agnostic: it "supports any model… or your own endpoint" and "auto-detects models installed through Ollama" with per-model tool-call parsers tuned for local models [OFFICIAL Hermes docs; [PRAC] remoteopenclaw 2026]. Hermes itself is MIT-licensed and free [OFFICIAL]; reported run cost is "$5–$80/month" and a genuine "$0 API cost using local Ollama models" path exists [PRAC]. **But this flexibility only helps Momentum if Momentum's work runs on the local model** — and per the prior art's decisive "Momentum-specific catch," the dispatched work *is* Claude Code skills/subagents/hooks (AVFL, sprint-dev, fan-out/TeamCreate), which "a non-Claude runtime cannot execute." If Hermes spawns `claude -p` workers, you are back in Option B's exact cost model — Hermes adds no inference-cost relief, just a different orchestrator on top of the same Claude bill. Hermes's $0-local advantage is *only* realized by abandoning the Claude-skill execution layer (Lever-3 re-platforming), which the prior art prices as a substantial capability downgrade, not a config flag.

**Net:** Option A has a real $0-local *capability* that Option B lacks — but it is inaccessible without giving up the very skill layer Momentum's value resides in. For a Claude-skill-centric practice, both options pay the same Claude inference bill; Hermes does not reduce it.

## Autonomy — 24/7, No-Human

Both can run unattended; the maturity of the autonomy machinery differs.

**Option A is purpose-built for this.** Hermes Kanban's entire reason for existing over `delegate_task` is durable, resumable, fire-and-forget multi-agent work: dependency promotion (todo→ready when parents done), first-class `task_runs` retry rows, a circuit breaker on consecutive spawn failures, crash recovery via `kill(pid,0)` PID polling, stale-claim TTL (15 min default, extends live workers), stranded-task detection with escalating severity, and a gateway that can run as a user service for 24/7 operation (`hermes gateway install`) [OFFICIAL Hermes docs §3,§4,§7; [PRAC] open-techstack 2026]. Story 2 ("create all, `hermes gateway start`, walk away") and Story 4 (circuit breaker + crash recovery) are exactly the no-human loop. This is autonomy infrastructure shipped and documented, not assembled.

**Option B achieves equivalent autonomy but you build the resilience yourself.** The prior art is explicit that "no single built-in is simultaneously local-only, survives with no open Claude process, *and* self-perpetuating." The recommended architecture is a supervised long-lived SDK daemon (launchd `KeepAlive`/systemd `Restart=always`) with hand-rolled idempotent claim-by-status, self-trigger loop guards, lossy-delivery startup reconcile, and an OS-scheduler watchdog. Every resilience property Hermes ships (retry rows, circuit breaker, stranded detection) is something Option B's designer must specify and implement. The prior art names these as the "real engineering… not the plumbing."

**Net:** Both reach 24/7 no-human. Option A delivers the resilience layer as documented product; Option B requires the developer to build the equivalent of Hermes's dispatcher kernel. Advantage Hermes on *time-to-resilient-autonomy*.

## Agentic-Coding Capability

**Both ultimately run Claude Code for the actual coding**, so raw capability is governed by Claude, not the orchestrator — *if* Hermes drives Claude Code.

Critically, Hermes ships an **official, documented Claude Code integration skill** (`skills/autonomous-ai-agents/claude-code/SKILL.md`) describing print-mode (`claude -p`, preferred) and interactive-tmux orchestration, auth handling, and the JSON output contract [OFFICIAL, NousResearch repo]. This materially upgrades the prior `hermes-kanban-discovery-2026-05-17.md` finding (§5.3) that external CLI lanes are "NOT a paved path." There is now a real skill — but it is a *worker skill describing how Hermes drives Claude Code*, **not** a turnkey kanban *worker lane*: the lane plumbing (wrapping `claude -p` exit codes into `kanban_complete`/`kanban_block`, mapping `HERMES_KANBAN_WORKSPACE`, per-CLI auth/policy) is still per-integration design work [OFFICIAL worker-lanes doc §5.3, re-confirmed 2026-05-18]. So Hermes-as-delegate driving Claude Code is *more supported than the discovery doc implied* but still requires the spawn_fn → terminator glue.

Whether Hermes-spawned Claude Code can run Momentum's full skill stack (AVFL, sprint-dev fan-out, plan-audit hooks) depends entirely on Claude Code itself once spawned — Hermes is out of the loop after spawn. The risk: Hermes's worker model is "spawn process → it terminates via a tool call." Momentum's subagent fan-out / `TeamCreate` patterns run *inside* one Claude Code process and are invisible to Hermes; Hermes sees one PID, one outcome. Option B's Agent SDK daemon, by contrast, owns the agent loop directly (`options.agents`, SKILL.md discovery, programmatic `canUseTool`) and the prior art recommends it precisely because it "sidesteps" the idle-session permission ambiguity Hermes-spawned workers would also face. **Net:** capability ceiling is identical (both = Claude Code); Option B has tighter, lower-impedance control of the Claude agent loop and permission posture; Option A treats the Claude worker as an opaque process, which is simpler but coarser.

## Operational Risk — Split-Brain, Lost Callbacks, Trust/Permission, Runaway

| Risk | Option A (Hermes) | Option B (native) |
|---|---|---|
| **Split-brain / claim race** | Documented and *handled* by atomic claim + run/`current_run_id` invariant — **but** gateway-embedded dispatch + `hermes kanban daemon --force` on one DB causes claim races [OFFICIAL]; beads atomic-`--claim` race under load is [UNVERIFIED] in the prior art and Hermes inherits the same risk if beads-backed | Prior art flags atomic `bd ready --claim` under concurrent load as **open/[UNVERIFIED]**; mitigation = single sole-claimer + `flock`. Same hazard, designer-owned |
| **Lost callbacks / events** | Gateway downtime → "`ready` tasks do not dispatch and can burst later" [PRAC]; but state is durable SQLite, no event is *lost* (it's deferred) — strong | beads exec hooks are **fire-and-forget, lossy** [OFFICIAL source-read]; native design *requires* a startup reconcile sweep to compensate. Lossier primitive, mitigated by discipline |
| **Trust / permission** | Worker spawned as `hermes -p <profile> chat`; the *Claude Code child's* unattended permission posture is still the prior art's hard problem (idle-session refuses injection-shaped input, hard-stalls on side-effectful tool gate — spike-confirmed) | Same Claude permission problem, but prior art recommends Agent SDK `canUseTool` / permission-relay as cleaner than skip-permissions; Option B has the better-characterized mitigation |
| **Runaway / cost** | Circuit breaker (consecutive spawn failures → `gave_up`), `max_runtime_seconds` hard cap, stale-claim TTL — runaway *spawn* loops are bounded by design [OFFICIAL]. Token runaway inside a Claude worker is **not** bounded by Hermes | `--max-turns`/`--max-budget-usd`, `total_cost_usd` telemetry, stray-API-key env hygiene (highest-severity failure mode per prior art). Token runaway is designer-bounded |
| **Extra surface** | Hermes dashboard `/api/plugins/` is **unauthenticated by design** (localhost-bound; `--host 0.0.0.0` exposes the whole board) — a net-new attack surface Option B does not introduce [OFFICIAL Hermes §8.3] | No added HTTP surface beyond an optional local Channel on 127.0.0.1 |
| **Circuit-breaker default** | Source docs **internally contradict** (2 vs 3 vs 5) — must verify against Hermes source before relying [OFFICIAL, flagged in discovery §7.1] | N/A (no equivalent built-in; designer sets it) |

**Net:** Hermes *handles* more failure modes out of the box (its kernel is the resilience layer), but introduces two risks Option B does not: an unauthenticated localhost HTTP surface, and a documented dual-dispatcher claim-race footgun. Option B has fewer built-in safeguards but a smaller, better-understood surface and the prior art's spike-validated permission mitigations. The Claude-worker token-runaway and unattended-permission problems are **identical in both** — neither architecture solves them; the prior art's mitigations apply to both.

## Maturity — Real Signals (Not Stars)

Per the instruction to discard stars, the substantive signals for **Hermes** [PRAC, NousResearch release notes 2026-04/05; stars explicitly discarded per `feedback_github_stars_unreliable`]:

- **Velocity:** v0.14.0 (2026-05-16): 808 commits / 633 merged PRs since v0.13.0 (2026-05-07). v0.12.0→v0.13.0: 864 commits/588 PRs. v0.11.0: 1,556 commits. This is extremely high throughput — multiple thousand commits/month.
- **Contributor distribution:** 215 community contributors in the v0.14.0 cycle, 295 in v0.13.0 — broad, not single-author.
- **Cadence:** weekly minor releases (v0.10→v0.14 across ~Apr–May 2026); date-stamped builds (v2026.5.7).
- **Caveat:** still **0.x** — pre-1.0. The Kanban discovery flags run-state/reclaim edge cases "patched over time" and the source docs are internally contradictory on the circuit-breaker default. High velocity cuts both ways: rapid iteration *and* unstable contracts. The Claude Code worker-lane glue is explicitly still per-integration design work.

For **Option B's** building blocks, the prior art's maturity picture: Claude Code itself is mature and first-party; **but** the load-bearing primitives are *research-preview* — Channels require the `--dangerously-load-development-channels` dev flag and "protocol may change" [OFFICIAL]; native daemon mode was closed "not planned" (#28229) [PRAC]; beads is pinned at v1.0.4 with the discovery flagging atomic-claim under load and hook contract as fast-moving and "must be re-verified before building." So Option B is *assembled from* a mature CLI plus several preview/pre-1.0 parts.

**Net:** Neither is a stable-1.0 foundation. Hermes has the stronger raw activity/contributor signal but is monolithically 0.x with contradictory docs and an unfinished external-lane path. Option B's core (Claude Code) is mature but its dispatcher-critical glue (Channels, beads, SDK daemon-reuse) is preview/community-pinned. Maturity is a wash — both demand pin-and-verify-before-build.

## Integration / Build Effort Into a Claude-Code-Skill Practice

This is the most decision-relevant axis for a solo dev.

**Option B is the *designed* path for Momentum.** The prior art's §6 recommended architecture is built *around Momentum's existing `intake-queue.jsonl`* and the beads-as-event-source addendum slots in "without replacing it." The skill/agent/hook layer — Momentum's actual value — runs natively because Option B *is* Claude Code. Build effort = the daemon + claim discipline + loop guards the prior art already specifies in detail. No re-platforming.

**Option A requires bridging two ecosystems.** To use Hermes-as-delegate while keeping Momentum's Claude skills: implement a `spawn_fn` that launches `claude -p` in the task's pinned workspace, translate Claude Code's exit/JSON outcome into `kanban_complete`/`kanban_block`, map `HERMES_KANBAN_WORKSPACE` onto Claude Code's workspace/worktree conventions, handle Claude auth inside the spawned process, and reconcile Momentum's `stories/index.json`/`sprints/index.json` state model against Hermes's task/run rows (two sources of truth — the prior art and Momentum's "exclusive write authority per file" principle both warn against this). The official Claude Code skill reduces but does not eliminate this — it documents *how to drive Claude Code*, not a finished kanban lane. Momentum's subagent fan-out and AVFL post-merge have no Hermes equivalent and remain Claude-internal. **This is net-new integration plus a dual-state-model reconciliation — a substantial build, not a config.**

**Net:** Option B's integration cost is "build the dispatcher the prior art already designed." Option A's is "build the Claude-Code worker lane Hermes explicitly hasn't paved, *plus* reconcile two task-state systems." Decisively in Option B's favor for a Claude-skill-centric practice.

## Reversibility / Lock-In

**Option B** has near-zero lock-in: it is glue code around primitives Momentum already owns (`intake-queue.jsonl`, beads optional, Claude Code first-party). Ripping it out leaves Momentum's skills/stories untouched. The prior art's design is intentionally a "variant, not a replacement" of existing structure.

**Option A** introduces a second system of record (Hermes Kanban SQLite + gateway + profiles + dashboard plugin). State lives in `~/.hermes/kanban.db` with "no migration or export documentation" surfaced [PRAC, fetch 2026-05-18]; the dependency graph, run history, and comments become Hermes-shaped. Reversibility is moderate (SQLite is inspectable; MIT license means no legal lock-in) but you would re-home the task-lifecycle truth into Hermes and then have to extract it back out. The two-source-of-truth problem against Momentum's JSON indexes is the real lock-in cost, not the license.

**Net:** Option B is markedly more reversible. Option A's lock-in is architectural (dual state of record), not licensing.

## Head-to-Head Scored Comparison

Scoring 1–5 (5 = better for a solo-dev, local-first, Claude-skill-centric Momentum practice). Even-handed; ties called where evidence is genuinely balanced.

| Criterion | Hermes-as-delegate (A) | Claude-native beads+Channel/SDK (B) | Edge |
|---|---|---|---|
| **Local-only operation** | 4 — local loop, but adds unauth localhost HTTP surface | 5 — source-verified + spike-confirmed local; minimal surface | B (slight) |
| **Cost model / $0-local** | 3 — real $0-local capability, but unreachable without dropping the Claude-skill layer; with Claude workers = identical bill | 3 — no $0 path, but cost levers (Haiku-tier, cache) fully designed | Tie |
| **Autonomy (24/7, no-human)** | 5 — resilience kernel shipped (retry rows, circuit breaker, crash recovery, stranded detection) | 4 — equivalent achievable but designer-built | A |
| **Agentic-coding capability** | 4 — = Claude Code, but opaque-process control, fan-out invisible | 5 — = Claude Code with direct agent-loop + permission control | B |
| **Operational risk** | 3 — handles more failures, but unauth dashboard + dual-dispatcher race + contradictory defaults | 4 — fewer built-ins, smaller/better-characterized surface, spike-validated mitigations | B |
| **Maturity (real signals)** | 3 — Pre-1.0, high-velocity: Over 8,722 commits and 295 contributors; packaged on PyPI — but 0.x, explicitly unstable, breaking changes ~biweekly; contradictory docs, unfinished lane | 3 — mature core, preview/pinned dispatcher glue | Tie |
| **Integration/build effort** | 2 — net-new Claude lane + dual-state reconciliation | 4 — the prior-art-designed path, no re-platforming | B |
| **Reversibility / lock-in** | 3 — MIT, SQLite-inspectable, but 2nd system of record | 5 — glue over owned primitives, trivially reversible | B |

## When Is Hermes the Better Choice?

Hermes-as-delegate genuinely wins when:

1. **The work is *not* Claude-skill-centric.** If the dispatched work can run on local Ollama/vLLM models (generic coding, research triage, fleet ops, scheduled briefs), Hermes's model-agnosticism + $0-local + shipped resilience kernel is decisively better — this is exactly Hermes's designed sweet spot (Kanban Stories 2–4).
2. **You want a resilient multi-profile fleet *now* without building a dispatcher kernel.** Hermes's retry rows, circuit breaker, crash recovery, stranded detection, and human-in-loop block/unblock are production-shaped and free. Replicating them in Option B is the prior art's "real engineering."
3. **Multi-channel human-in-loop matters.** `/kanban` over Telegram/Discord/Slack to unblock a peer from your phone mid-run is a capability Option B has no equivalent for.
4. **You value a durable audit trail of every attempt as the primary representation** — Hermes's two-table task/run model is more formalized than Momentum's current re-spawn history (the discovery doc's idea #1).

Hermes is the *worse* choice precisely when the workload is Claude-Code skills/subagents/hooks under tight cost control — because then Hermes contributes orchestration you must bridge while changing nothing about the Claude bill or the skill execution model, and adds a second system of record.

## Blunt Overall Recommendation

**For a solo-dev, local-first, Claude-Code-skill-centric Momentum practice: build Option B — the Claude-native beads+Channel/SDK daemon — and do not adopt Hermes as the delegate.**

> **Note on parent-task-wakeup:** The single finding that would have made Hermes feasible — the native parent-task-wakeup callback mechanism described in `research-claude-planner-hermes-delegate.md` — was tagged `[UNVERIFIED]` by that document. The DON'T ADOPT verdict does not depend on this mechanism being absent (the split-brain and worker-lane issues are independently disqualifying), but consumers should note: if the parent-task-wakeup is real and verifiable, the Hermes-as-delegate pattern becomes technically feasible while remaining the wrong fit for Momentum's specific constraints.

The reasoning is not that Hermes is weak — its resilience kernel is genuinely better-engineered than anything Option B ships, and its $0-local model-agnosticism is real. The reasoning is that **Momentum's value is the Claude skill/subagent/hook layer**, and against that constraint every Hermes advantage either evaporates or inverts:

- Hermes's headline $0-local cost win is *unreachable* without abandoning the Claude-skill layer; with Claude workers the inference bill is identical to Option B.
- Hermes's resilience kernel is real, but it manages the *spawn* lifecycle of an opaque Claude process — it cannot see or help Momentum's in-process fan-out/AVFL, and the hard unattended-permission problem is identical in both designs (the prior art solves it better on the SDK side).
- Hermes adds a *second system of record* against Momentum's JSON indexes and "exclusive write authority per file" principle, plus net-new Claude-lane glue Hermes explicitly hasn't paved — a substantial build that buys orchestration you mostly don't need.
- Option B is *the architecture the prior art already designed for this exact codebase*, slots into the existing `intake-queue.jsonl`/beads ingress, keeps every skill working, and is trivially reversible.

**Caveat / where I am uncertain (be honest):** This recommendation is conditional on the work staying Claude-skill-centric. If Momentum's roadmap shifts toward heterogeneous local-model work or a multi-profile fleet, the calculus flips toward Hermes. Two factual uncertainties remain unresolved: (1) Hermes's exact Claude-Code-worker-lane maturity is documented-but-unbuilt — the spawn_fn→terminator glue cost is [UNVERIFIED] and could be smaller than estimated if the official skill matures into a real lane; (2) atomic-claim-under-concurrency is [UNVERIFIED] for *both* beads and Hermes and must be empirically pin-tested before relying on either for multi-claimer fan-out. **Pragmatic hedge:** steal Hermes's *ideas* (first-class per-run attempt rows, structured handoff metadata, stranded-task detection, the model-tools/human-CLI two-surface invariant) into Option B's design — the discovery doc already flagged these — without adopting Hermes as the runtime. That captures Hermes's best engineering at zero integration and zero lock-in.

## Sources

**Prior art (cited by name, read in full 2026-05-18):**
- `/Users/steve/projects/momentum/docs/research/claude-code-background-dispatcher-2026-05-17.md` — native dispatcher design incl. Cost & Licensing, Cost-Reduction & Alternative Runtimes, Beads addendum, Channel spike
- `/Users/steve/projects/momentum/docs/research/hermes-kanban-discovery-2026-05-17.md` — Hermes Kanban comprehensive discovery (data model, worker lanes, failure modes, §13 Momentum relevance)

**Hermes — Official [OFFICIAL]:**
- [Kanban worker lanes — Hermes Agent docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-worker-lanes)
- [Hermes + Claude Code integration skill — NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent/blob/main/skills/autonomous-ai-agents/claude-code/SKILL.md)
- [Hermes Agent releases (v0.10–v0.14, commit/PR/contributor counts)](https://github.com/NousResearch/hermes-agent/releases)
- [Hermes Agent docs — AI providers / local models](https://hermes-agent.nousresearch.com/docs/integrations/providers)
- [Hermes Agent repository (MIT license)](https://github.com/nousresearch/hermes-agent)

**Hermes — Practitioner [PRAC]:**
- [Kanban in Hermes Agent for self-hosted LLM workflows — glukhov.org (2026-05)](https://www.glukhov.org/ai-systems/hermes/kanban-in-hermes/)
- [How to set up Hermes Agent for local automation — open-techstack.com (2026)](https://open-techstack.com/blog/how-to-set-up-hermes-agent-local-automation-2026/)
- [How much does Hermes Agent cost to run in 2026 — remoteopenclaw.com](https://www.remoteopenclaw.com/blog/hermes-agent-cost-breakdown)
- [Best free AI models for Hermes Agent — remoteopenclaw.com](https://www.remoteopenclaw.com/blog/best-free-models-for-hermes)

**Native-design primitives:** all underlying Claude Code / beads / Channel / Agent SDK sources are enumerated in the Sources section of `claude-code-background-dispatcher-2026-05-17.md` and are not duplicated here; this report cites that document as the synthesized authority for Option B.
