---
content_origin: claude-code-subagent
date: 2026-05-22
sub_question: "Gas City roadmap: orchestration v3, HITL, dispatcher primitives, and trajectory vs. Temporal/Prefect"
topic: "Gas Town as dispatcher/coordinator for Momentum agentic engineering"
---

# Gas City Roadmap — Orchestration, HITL, and Dispatcher Primitives

## Sources Consulted

- GitHub issues #1709, #2311, #2131, #2168, #2120, #1690 in gastownhall/gascity [OFFICIAL]
- GitHub milestone API (open milestones and issue counts) [OFFICIAL]
- Issue search across open issues by keyword [OFFICIAL]

---

## 1. Orchestration v3 (Issue #1709) — Scope and Status

**Status:** OPEN, P2 / `kind/feature`. Last updated 2026-05-20. No milestone assigned. No PR linked. [OFFICIAL]

The proposal is large, fully written, and active (comments from core contributors csells, donbox, quad341, and an external tool author seanmartinsmith through May 7–20, 2026). It is a design document, not an implementation in progress. Implementation has not started as of assessment date. [CONFIRMED]

**Core architectural shift:** Today a convoy of N beads produces N independent Runs, one per bead, so post-implementation verification phases (review, arch check, coverage) each see only their own fragment. The O3 proposal makes one Run per convoy invocation. Implementation phases can still parallelize via a drain loop; verification phases see the complete convoy as a unit. This is exactly the pattern Momentum's corpus-AVFL and E2E loops require (all stories merged → single corpus check). [CONFIRMED from issue body]

**HITL implementation design (R4, R12–R14, TC6):** HITL is specified as a typed disposition variant (`HITL{assigned_human, request, auth_policy, deadline}`) within a broader Disposition ADT (`Pass`, `HardFail`, `Transient`, `Degraded`, `HITL`, `Skipped`). Individual steps can enter HITL-paused state while other independent steps in the same Run continue. The orchestrator pauses the step, notifies the assigned human (dashboard-only for v1), and resumes on approval. Rejection routes through the hard-fail path. Multi-channel notification (email, Slack), presence detection, and escalation chains are explicitly deferred out of scope. [CONFIRMED]

**Scatter/gather design (S3, R15, TC5):** Scatter/gather is a first-class sub-formula. The author declares the gather policy in TOML using predicate expressions over typed children's dispositions (e.g., `pass_when = "count(d.kind == 'pass') >= 4"`), or as an agent step for judgment-based policies. Current behavior — any-fail immediately skips remaining children and closes as failed — is explicitly called out as wrong and targeted for replacement. A "degraded" disposition (R16) is a first-class outcome for partial success, distinct from pass, hard-fail, and transient-fail. [CONFIRMED]

**Run as execution primitive:** Sessions become Runs of a single-step "execute" formula. Sub-formulas expand inline into the parent Run's step graph (no separate child Run). Runs are persisted as typed beads (`Type="run"`), so crash recovery falls out of existing bead-store infrastructure. Dashboard renders Runs as the central object. [CONFIRMED]

**Timeline:** No milestone, no assignee, no draft PR. The proposal has ten open design questions (molecule→Run relationship, data-flow scoping, formula schema location). This is early-to-mid design phase. Realistic estimate: no implementation in 2026 H1. [INFERRED]

---

## 2. Convergence Loop Evolution and Barrier Improvements

**`convergence.terminated` subscription:** No issue or PR found addressing whether orders can subscribe to `convergence.terminated`. The O3 open questions section does not mention it. No evidence this is planned or blocked. [UNKNOWN — not found in available sources]

**Native barrier/join primitives:** The `waits_for = "children-of(X)"` mechanism is the current barrier approach. Issue #2311 (P2, OPEN, filed 2026-05-17) documents a race condition: the tracking dep edge is created at plan time when no children exist yet, so `bd ready` gates only on step A closing, not on A's bond-fanout children finishing. The reporter provides a concrete proposed fix: at bond-expansion time, walk sibling/successor steps and insert real `blocks` edges against each newly-spawned child. No PR linked. [CONFIRMED bug; fix approach specified but unimplemented]

O3's drain loop (P1, P2 requirements) is the planned replacement for ad-hoc barrier patterns: drain completes at quiescence (no ready beads, no in-flight polecats), and downstream steps wait via existing step-dependency mechanism. This is O3-level, not a near-term fix. [CONFIRMED as future design]

**Retry-on-failure in exec orders:** The typed dispatch metadata issue (#1690, P3 backlog) describes `gc.max_attempts`, `gc.attempt`, and `gc.on_exhausted` as existing but stringly-typed metadata fields — retry logic exists today at the bead metadata level but is untyped and fragile. O3's Disposition ADT (`Transient{retries_remaining, last_error}`) would make retry first-class. No standalone near-term retry improvement tracked. [INFERRED: retry exists implicitly, O3 formalizes it, no near-term hardening planned]

---

## 3. Roadmap Beyond v1.1

**Open milestones:** `1.0+` (87 open, 45 closed, overdue from April 22), `1.1.0` (4 open, 24 closed), `1.1.1` (0 open, 13 closed), `1.2` (4 open, 1 closed, due May 11). [CONFIRMED]

The `1.2` milestone contains: typed claim/lifecycle primitive bundle (#1249, P2 chore), ghost session leak fix (#2073, P2 bug), Dolt/beads layering architecture review (#1248, P3). Active v1.2 work is infrastructure hardening, not orchestration features. [CONFIRMED]

The `1.0+` backlog includes: supervisor health/crash detection/startup probes, Docker/K8s container support, multi-account quota rotation, provider failover, webhook triggers for orders, pack registry, headless Docker session provider. Infrastructure and scaling concerns — not HITL or orchestration semantics. [CONFIRMED]

No v2.0 milestone exists. O3 (#1709) is the only issue describing a major orchestration redesign, and it is unscheduled. [CONFIRMED]

---

## 4. Error Handling Trajectory

**Proactive failure alerts / watchdog timers:** A 1.0+ backlog feature: "Supervisor health: crash history, heartbeat restarts, stuck detection, startup probes." This addresses supervisor-level stuck detection at infra layer, not formula/order-level hung conditions. [CONFIRMED feature exists in backlog; no milestone, not in-progress]

**Design philosophy — user builds compensation:** The current system and O3 both lean toward "runtime routes typed values, never makes data-flow judgment calls; authors declare." The gather policy escape hatch ("if the declarative language doesn't suffice, the gather policy is an agent step") makes this explicit. Gas City's design explicitly avoids the runtime making workflow-level decisions. [CONFIRMED from O3 TC4, TC5]

---

## 5. Dispatcher Wedge Bugs — Status

**Issue #2131 (order-tracking-sweep self-wedge → full dispatcher wedge):** Root cause identified and resolved upstream in Beads HEAD. The Beads v1.0.4 bug — stale JSONL imported over live Dolt state on every `bd` write — caused close operations not to persist, creating ghost tracking beads that gate dispatcher re-fire. Beads fix commit: `1cf83373`. Gas City guardrail PR (#2215) adds `TestDoltPersistence*` integration tests. Issue remains OPEN with `status/accepted` and `status/in-progress` labels; dispatcher stale-order cleanup hardening (widening scope to all rig target stores) is ongoing. [CONFIRMED]

**Issue #2168 (watchdog scope too narrow — cannot recover from multi-order tracking-bead jam):** Root cause overlaps #2131 (Beads persistence gap). Additionally: the watchdog's `onlyOrders` filter sweeps only `order-tracking-sweep`'s own beads, creating a self-wedge when that order's own tracking bead ghosts. Three improvements proposed: widen watchdog scope to all orders, add cold-start unconditional sweep, surface `hasOpenWork` gate skips in logs. No `status/in-progress` label. No PR linked. The Beads fix resolves accumulation root cause, but the watchdog design gap (single-point-of-failure by design) remains unaddressed structurally. [CONFIRMED root cause partially resolved; structural watchdog redesign not yet scheduled]

---

## 6. Community Signal on Roadmap

The O3 issue (#1709) received 18 comments from contributors (donbox, philcunliffe, quad341) and one external tool author (seanmartinsmith/beadstui). The conversation is substantive, with no "this is missing and I'm blocked" urgency from external users. [CONFIRMED]

GitHub search for "Temporal," "Prefect," "Durable," or "join primitive" returns zero results — the community is not framing requests in those terms. [CONFIRMED]

The 1.0+ backlog shows community interest in infrastructure (Docker, K8s, multi-account quota, webhook triggers) over orchestration semantics. [INFERRED from relative issue density]

---

## Synthesis: Is Gas City Converging on Temporal-Parity or Diverging?

**Divergent, not convergent. Deliberately so.**

Three structural differences define the trajectory:

**Beads as universal substrate, not a workflow engine.** Where Temporal builds durable execution as a specialized runtime concern (histories, event replay, deterministic workers), Gas City encodes all coordination state into beads. Crash recovery, observability, and operator intervention all flow through the same bead-query infrastructure. The O3 "Run as a bead" decision doubles down on this. [CONFIRMED]

**Author-declared policy, not runtime compensation.** Temporal's durable workflow engine automatically retries, replays, and compensates. Gas City's design, as expressed in O3's TC4 and TC5, explicitly routes that responsibility to the formula author or an agent step. The runtime "routes typed values, never makes data-flow judgment calls." More transparent but more demanding authoring model. [CONFIRMED]

**HITL as a disposition, not an interrupt.** Gas City's HITL design (TC6) models human approval as a typed disposition variant returned by the agent, not as an external interrupt to a running execution. The orchestrator acts on that disposition through normal scheduling machinery. No out-of-band "pause everything" escape valve yet. [CONFIRMED from TC6]

**Where Gas City is going:** Toward a composable SDK where typed primitives (dispositions, convoy operations, HITL, gather policies) let sophisticated users build workflows that look like Temporal from the outside but are implemented as bead-coordination patterns from the inside. O3 is the decisive test of that bet.

Near-term trajectory: stabilization (dispatcher reliability, Beads persistence fix, typed dispatch metadata). O3 is research-phase with no implementation schedule. Users needing Temporal-style durable execution with automatic retry, event replay, or cross-workflow barriers today should treat those as gaps, not planned near-term features.
