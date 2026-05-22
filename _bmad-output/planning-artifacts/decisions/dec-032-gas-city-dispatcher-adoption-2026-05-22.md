---
id: DEC-032
title: Gas City as Momentum's Dispatcher — Adoption Decision
date: '2026-05-22'
status: decided
source_research:
  - path: docs/research/gas-town-dispatcher-2026-05-20/final/gas-town-dispatcher-final-2026-05-20.md
    type: research-synthesis
    date: '2026-05-20'
  - path: docs/research/gas-town-dispatcher-2026-05-20/validation/discovery-rationale-why-not-temporal.md
    type: discovery-agent
    date: '2026-05-22'
  - path: docs/research/gas-town-dispatcher-2026-05-20/validation/discovery-roadmap-orchestration-v3.md
    type: discovery-agent
    date: '2026-05-22'
  - path: docs/research/gas-town-dispatcher-2026-05-20/validation/alt-temporal.md
    type: alternative-evaluation
    date: '2026-05-20'
  - path: docs/research/gas-town-dispatcher-2026-05-20/validation/alt-langgraph.md
    type: alternative-evaluation
    date: '2026-05-20'
  - path: docs/research/gas-town-dispatcher-2026-05-20/validation/alt-survey.md
    type: alternative-evaluation
    date: '2026-05-20'
prior_decisions_reviewed:
  - DEC-028 (Beads as Tracker/Dependency/Memory Substrate — Adoption Under Momentum via Dual-Write Spike)
  - DEC-030 (Dependency-Driven Execution Model — DAG Dispatch, Closeable Value-Groupings, Frozen-Scope Sprints, and the Dual-Format Integrity Split)
architecture_decisions_affected:
  - DEC-028 D3 — EXTENDED: Gas City is the event-driven trigger layer that makes Beads-driven DAG dispatch reactive; Beads remains standalone-capable as lifecycle state
  - DEC-030 D1 — EXTENDED: continuous DAG-driven dispatch now has an explicit runtime substrate (Gas City exec orders + Event Bus); bd ready --json --claim remains the atomic claim mechanism
---

# DEC-032: Gas City as Momentum's Dispatcher — Adoption Decision

## Summary

After a two-day heavy-profile research engagement covering Gas City architecture, dispatch
primitives, HITL patterns, production maturity, community health, error handling, convergence
loops, and four alternative dispatchers (Temporal, LangGraph, GitHub Actions, broader survey),
the decision is to adopt Gas City as Momentum's dispatcher. The Gas Town Colony topology
(Mayor/Deacon/Witness/Polecat/Refinery hardwired roles) is explicitly ruled out — Gas City
(the composable SDK) is the target.

The adoption decision rests on three reinforcing findings: (1) Gas City's design philosophy
(Zero Framework Cognition, the Bitter Lesson filter) is the same bet Momentum makes — skill
prompts drive decisions, the dispatcher routes state; (2) Beads and Gas City are co-designed,
making the integration coherent rather than bridged; (3) alternatives with better raw
capability (Temporal, Prefect) require adopting infrastructure designed for deterministic
human-written workflows, which is the wrong abstraction for Momentum's model-driven agent
chains. The adoption proceeds via a scoped PoC that defers Dolt and the MCP runtime gap,
proving the exec-order dispatch pattern before committing.

---

## Decisions

### D1: Adopt Gas City (not Gas Town Colony) as Momentum's dispatcher — ADOPTED

**Developer framing:** Gas Town is mentioned as a dispatcher for Beads. Is it the right choice, and which product — Gas Town Colony or Gas City SDK?

**Decision:** Gas City (gastownhall/gascity) is adopted. Gas Town Colony (gastownhall/gastown) is explicitly ruled out. Gas Town is one optional pack inside Gas City; Gas City's quickstart deploys zero Gas Town infrastructure.

**Rationale:** Four hardwired architectural mismatches make Gas Town Colony a poor fit for Momentum: fixed Mayor/Polecat/Refinery role taxonomy in the Go SDK (not configurable), 20–30 agent colony scale assumption (Momentum runs 4–8), work model hardwired to PRs and merge queues (Momentum works on story state transitions, not code changes), and directory-as-identity model (Gas City's own docs list this as a mistake to abandon). Gas City resolves all four mismatches: no hardcoded role names in Go, configurable pool sizing, explicit identity from config/metadata, general-purpose Orders system.

---

### D2: Beads remains the story lifecycle state layer — ADOPTED

**Developer framing:** If Gas City is the dispatcher, does Beads become redundant, or does it still serve a distinct role?

**Decision:** Beads is the story lifecycle state layer (status, deps, readiness, gates, metadata). Gas City is the execution state layer (which loop, which iteration, which agent is assigned). The two layers are distinct and co-designed — Beads is explicitly designed to be standalone-capable independent of Gas City. Only event-driven triggers and the convergence loop primitive require Gas City.

**Rationale:** Three state layers govern Momentum's pipeline:
1. **Story spec** — `.momentum/stories/{slug}.md` — unchanged regardless of dispatcher
2. **Story lifecycle state** — Beads: status, deps, readiness gates, metadata, `bd ready --json --claim` for atomic work acquisition
3. **Execution state** — Gas City: which loop is active, which iteration, which agent is running

Conflating layers 2 and 3 into Gas City alone would mean rebuilding Beads' dependency graph and atomic claim semantics inside Gas City. Beads already has this and is designed to pair with Gas City.

---

### D3: PoC via GC_BEADS=file + exec orders, no Dolt initially — ADOPTED

**Developer framing:** Gas City has a Dolt dependency and a deferred MCP runtime. How do we validate without committing to the full infrastructure stack?

**Decision:** The adoption PoC uses `GC_BEADS=file` (removes Dolt entirely) and exec orders (invoke `claude -p` as a shell subprocess, bypassing Gas City's deferred MCP runtime support). Three-step minimum viable integration:
1. `GC_BEADS=file gc init ~/momentum-city && gc rig add ~/projects/<target-project>`
2. Wire one manual exec order calling `claude -p` with a story-slug argument
3. Replace the manual trigger with a condition trigger on a ready-flag file written by `bd ready --json --claim`

If the PoC validates exec-order dispatch and condition triggers, Dolt becomes optional hardening (column-level merge semantics, audit history) rather than a required dependency.

**Rationale:** The two largest adoption risks are the Dolt infrastructure dependency (Beads v1.0.4 stale-JSONL bug, now fixed upstream, shows the persistence layer is still stabilizing) and the MCP deferred runtime (Gas City's MCP integration is not production-ready). `GC_BEADS=file` eliminates the first; exec orders eliminate the second. The PoC proves the dispatch pattern on Gas City's most stable surface before committing to either dependency.

---

### D4: Gas City's architectural philosophy aligns with Momentum's model-driven agent chain — INFORMING

**Developer framing:** Temporal and Prefect have better raw capability for fan-out, convergence loops, and HITL. Why not adopt one of them?

**Decision:** Temporal and Prefect are technically superior on raw dispatcher capability (native fan-in, durable mid-loop checkpoint, human signals with typed payloads). They are not adopted because they are the wrong abstraction layer for Momentum's design.

**Rationale:** Gas City's four laws are the deciding factor:

- **Zero Framework Cognition (ZFC):** Any Go code containing a judgment call is a design violation. Temporal's retry policies, LangGraph's conditional edges, CrewAI's process selection — all fail this test. These frameworks make decisions that, under Momentum's thesis, only the skill prompt should make.
- **The Bitter Lesson filter:** Every primitive must become more useful as models improve, not less. Skills systems, capability flags, decision trees, and hardcoded roles become dead weight as models improve. Temporal's durable execution encodes deterministic workflow logic — the antithesis of model-driven orchestration.
- **Nondeterministic Idempotence (NDI):** Beads survive sessions; agents rehook on restart. Convergence is guaranteed by persistent workflow definitions and explicit acceptance criteria, not by Temporal's event replay. This matches Momentum's convergence loop design.

The Gas City team arrived at these laws not from a build-or-buy analysis of Temporal, but by extracting the principles from a working system (Gas Town). The principles fit the system Momentum is building: skill prompts drive decisions, the dispatcher routes typed state, the model is the skills system. Adopting Temporal would mean fighting the framework's assumptions at every integration point.

---

### D5: Orchestration v3 (Issue #1709) is not a prerequisite — ADOPTED

**Developer framing:** Gas City's O3 proposal adds native HITL, scatter/gather, convoy-level barriers. Momentum needs all three. Does adoption wait for O3?

**Decision:** O3 is not a prerequisite. Adoption proceeds with current Gas City primitives; O3 improvements are adoption hardening when they ship.

**Rationale:** O3 is a design document, not an implementation. No milestone, no PR, no assignee as of 2026-05-22. Realistic estimate: not in 2026 H1. Momentum's 3-loop pipeline can be implemented with current Gas City primitives:
- Fan-out: exec orders in parallel (current capability)
- Corpus AVFL loop: `gc converge create --gate condition` (current capability, `convergence.terminated` subscription TBD)
- E2E loop: same pattern
- Human review loop: `gc converge create --gate manual` + `gc converge iterate` (current capability; no feedback payload — artifact directory workaround)
- Scatter/gather fan-in: bead-count condition workaround until O3 ships

When O3 ships, the typed HITL disposition and author-declared gather policies replace the workarounds without architectural change. O3 is additive, not required.

---

### D6: Custom pipeline monitoring via Gas City REST API — DEFERRED

**Developer framing:** The `gt dashboard` and `gc dashboard` have no pipeline-phase panels or convergence loop visibility. How do we monitor the Momentum-specific pipeline?

**Decision:** Custom pipeline status page deferred to post-PoC. Gas City exposes a full OpenAPI REST API; a pipeline status script is buildable in approximately 1–2 developer-days. The PoC uses `gc events` and `gc order history` CLI tooling for monitoring. The custom dashboard becomes a story after the PoC validates the dispatch pattern.

**Rationale:** Building monitoring infrastructure before proving the dispatch pattern is premature. `gc events` and `gc order history` are sufficient for PoC-level visibility. The Gas City REST API is the foundation for a custom dashboard when needed.

---

## Open Questions Carried Forward

1. **`convergence.terminated` as order trigger**: Can orders subscribe to `convergence.terminated`? This determines whether loop chaining (AVFL loop → E2E loop → human review) is native event-driven or requires shell calls inside formulas. Not confirmed possible or impossible from available research. Answer via PoC or Gas City Discord.

2. **Dispatcher wedge bug status**: Issues #2131 and #2168 are partially fixed (Beads root cause resolved) but Gas City-side watchdog hardening is `status/in-progress`, not shipped. Monitor for completion before production use.

3. **Barrier race condition** (Issue #2311): `waits_for = "children-of(X)"` has a race condition where the tracking dep edge is created before children exist. Fix approach is specified but no PR exists. Use explicit `blocks` edges rather than `children-of` in Momentum's PoC formulas.

4. **`convergence.terminated` subscription**: Same as #1 — the most critical unknown for loop chaining.
