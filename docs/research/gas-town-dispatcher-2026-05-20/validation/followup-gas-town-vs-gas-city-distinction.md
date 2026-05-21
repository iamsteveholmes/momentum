---
content_origin: research-agent
date: 2026-05-20
sub_question: "Can Gas Town 'poor fit' and Gas City 'right tool' verdicts both be correct? What is the product-level distinction?"
---

# Gas Town vs. Gas City: Can Both Verdicts Be Correct?

## Research Question

Two prior research files produced directly contradictory adoption verdicts for the same ecosystem:

- **Verdict A** (`research-maturity-production-readiness.md:169`): "Gas Town's architectural model is a poor fit. Momentum's orchestration needs are fundamentally different from Git-worktree-parallel software development."
- **Verdict B** (`research-adoption-path-risks.md:254`): "Gas City is architecturally the right tool for Momentum's dispatcher gap. The Orders system maps directly to what Momentum needs: event-triggered dispatch of skill formulas without human intervention."

The AVFL report (CON-001) flagged this as a CRITICAL consistency finding. This document resolves the contradiction by establishing whether Gas Town and Gas City are sufficiently different products that different verdicts legitimately apply.

## Sources Consulted

- `gastownhall/gascity` README — [OFFICIAL] product definition, prerequisites, quickstart
- `gastownhall/gascity` `docs/getting-started/coming-from-gastown.md` — [OFFICIAL] explicit Gas Town → Gas City migration guide
- `gastownhall/gascity` `engdocs/architecture/orders.md` — [OFFICIAL] authoritative Orders system specification
- `gastownhall/gascity` `engdocs/architecture/nine-concepts.md` — [OFFICIAL] five primitives + four derived mechanisms taxonomy
- `docs.gastownhall.ai/design/architecture` — [OFFICIAL] Gas Town role taxonomy (Mayor, Deacon, Witness, Polecat, Refinery, Dogs)
- `docs.gastownhall.ai/concepts/polecat-lifecycle` — [OFFICIAL] Polecat session model
- `steve-yegge.medium.com/welcome-to-gas-city-57f564bb3607` — [PRAC] Yegge's framing of Gas City as a reimagining of Gas Town
- `steve-yegge.medium.com/gas-town-from-clown-show-to-v1-0-c239d9a407ec` — [PRAC] Gas Town v1.0 announcement; Gas City successor framing
- Prior corpus files: `research-maturity-production-readiness.md`, `research-adoption-path-risks.md`

---

## Findings

### Finding 1: Gas Town and Gas City Are Architecturally Distinct Products

CONFIRMED. The official Gas City migration guide is unambiguous on this point:

> "Gas City is not 'Gas Town with renamed commands'. It is the lower-level orchestration toolkit that Gas Town can be expressed in." [OFFICIAL — coming-from-gastown.md]

The distinction is structural, not cosmetic:

| Dimension | Gas Town | Gas City |
|---|---|---|
| Architecture | Fixed role taxonomy baked into Go SDK | Primitives + composable packs; no role names in Go code |
| Topology | Mayor → Deacon → Witness → Polecat/Refinery (hardwired) | Any topology; defined in `city.toml` + `pack.toml` |
| Dolt dependency | Hard requirement (all state in Beads/Dolt) | Optional — `GC_BEADS=file` skips Dolt/bd/flock entirely |
| Colony model | Implied by role structure (persistent colony of agents) | Explicit config; colony is one pack option, not the model |
| Development status | Maintenance mode as of April 2026 | Active; 40 releases, v1.1.0 May 6 2026 |
| Author recommendation | "Should you switch from Gas Town to Gas City? Yes!" | Active investment target |

Yegge describes Gas City as "Gas Town, but torn apart and rewritten from the ground up as an SDK for building your own dark factories." [PRAC — welcome-to-gas-city] Gas Town ships as a pack inside Gas City — it is one configuration of Gas City, not the other way around. [OFFICIAL — coming-from-gastown.md: "Gas City comes with a fully functional 'Gas Town' pack, which runs an exact replica of Gas Town"]

**Both verdicts are evaluating different products.** Verdict A correctly evaluates Gas Town's fixed architecture. Verdict B correctly evaluates Gas City's composable SDK.

---

### Finding 2: The Specific Gas Town Characteristics That Cause Poor Fit for Momentum

CONFIRMED. Gas Town's architectural choices map poorly to Momentum's actual needs on four specific axes:

**2a. Fixed role taxonomy assumes a coding colony topology.**

Gas Town bakes Mayor, Deacon, Witness, Polecat, Refinery, and Dogs as SDK-level primitives in Go. The Polecat lifecycle document confirms: each Polecat is spawned in a dedicated git worktree, runs a Claude Code session, and self-destructs after pushing a branch for the Refinery's merge queue. [OFFICIAL — polecat-lifecycle] This is a purpose-built pipeline for software development via parallel coding agents. Momentum's orchestration does not produce PRs or merge requests — it dispatches skill invocations and manages story state machines. There is no Refinery-equivalent in Momentum's model.

**2b. Scale mismatch: Gas Town's value proposition requires 20–30 parallel agents.**

Gas Town's economic value comes from parallelizing multiple coding agents simultaneously across isolated worktrees. Independent practitioner reports confirm: at 4–8 agents the overhead of the colony infrastructure rivals the throughput gains. [PRAC — DoltHub blogs] Momentum's sprint model uses 4–8 session-scoped agents sequentially through a workflow, not persistent parallel workers. Gas Town's entire supervisory stack (Witness health monitoring, Refinery merge queue, Deacon watchdog) exists to manage persistent parallel workers at scale. At Momentum's operating scale, this is pure overhead.

**2c. Directory-as-identity model is antithetical to Momentum's design.**

Gas Town derives agent identity from filesystem directory structure (`~/gt/...`). The migration guide is explicit that this is a known design flaw: "Stop encoding architecture into paths. Keep identity in config and metadata." [OFFICIAL — coming-from-gastown.md] Momentum's skills-based orchestration uses explicit agent composition, not path-inferred identity. Adopting Gas Town would require porting a design anti-pattern.

**2d. No general-purpose event dispatch — work model is hardwired to PRs.**

Gas Town's work model assumes tasks are issues that become PRs via the merge queue. The Refinery manages a queue specifically for serializing parallel coding results. Momentum's story lifecycle (backlog → ready → in-progress → done → validated) is a general state machine. There is no native Gas Town primitive for story-state transitions that don't produce commits. [INFERRED — from role taxonomy and polecat lifecycle docs; no Gas Town doc describes non-coding workflows]

---

### Finding 3: Gas City Characteristics That Do Not Have These Problems

CONFIRMED. Gas City's design addresses each of the four Gas Town fit problems:

**3a. No hardcoded roles.** The nine-concepts architecture doc states explicitly: "The SDK contains zero hardcoded role names." [OFFICIAL — nine-concepts.md] Mayor, Deacon, Witness, Polecat are pack conventions, not SDK primitives. A Momentum pack would express Momentum's topology (orchestrator → dev subagent → AVFL validator) without fighting against a fixed role structure.

**3b. Scale is configurable, not assumed.** Gas City's session configuration uses pool sizing in `city.toml`. The default Gas City quickstart deploys a single `mayor` agent — not a 20–30 agent colony. The Gastown pack can be configured with `max = 1` polecats. Solo-scale deployment is a first-class configuration, not a degenerate case. [OFFICIAL — coming-from-gastown.md: `[[rigs.patches]] agent = "gastown.polecat" [rigs.patches.pool] max = 10`]

**3c. Explicit identity, not path-derived.** Gas City uses `dir` for scope and bead metadata for durable state. The migration guide explicitly lists "cwd-derived identity" in the "What NOT to port literally" section. [OFFICIAL — coming-from-gastown.md] Momentum's explicit agent composition model aligns with Gas City's design philosophy.

**3d. Orders system is genuinely general-purpose.** The Orders architecture document confirms five trigger types: cooldown, cron, condition, event, and manual. [OFFICIAL — orders.md] The event trigger responds to any bead event (`bead.closed`, `bead.created`, or arbitrary named events), not specifically to PRs or code commits. An exec order runs a shell script with no LLM involvement at all. A formula order dispatches any formula to any agent pool. Nothing in the Orders system is hardwired to coding tasks. [OFFICIAL — orders.md: "No line of Go references a specific role name"]

**3e. Dolt is optional for minimal deployments.** Gas City's file-based Beads store (`GC_BEADS=file`) removes the Dolt/bd/flock prerequisite entirely. [OFFICIAL — README, quickstart] This is material for Momentum adoption risk: the highest-risk Gas Town dependency (Dolt, with its documented deadlock bugs at Issue #1930) can be bypassed for initial adoption.

---

### Finding 4: Official Acknowledgment That Gas City Is Independently Adoptable Without Gas Town

CONFIRMED. Multiple official sources frame Gas City as standalone:

**Yegge's explicit recommendation:** "Should you switch from Gas Town to Gas City? Yes!" The welcome-to-gas-city article positions Gas City as the platform that Gas Town users should migrate to — not a dependency that requires Gas Town to already be running. [PRAC — welcome-to-gas-city]

**The migration guide is written for migration away from Gas Town, not toward it:** The coming-from-gastown.md document exists to help Gas Town users stop thinking in Gas Town terms. Its "What NOT to port literally" section explicitly tells Gas Town users to abandon Gas Town's architectural habits when adopting Gas City. [OFFICIAL]

**The Gas Town pack ships inside Gas City.** Gas City includes a Gastown pack that "runs an exact replica of Gas Town" — but this is one optional configuration. The quickstart (`gc init` → `gc rig add` → `gc sling`) does not reference the Gastown pack at all. [OFFICIAL — README quickstart, coming-from-gastown.md]

**The quickstart deploys zero Gas Town infrastructure.** The official four-step quickstart (`gc init`, `gc rig add`, `gc sling`, `bd show`) makes no reference to Mayor/Deacon/Polecat/Colony roles. It boots a city and dispatches work without the Gas Town topology. [OFFICIAL — quickstart.md]

---

### Finding 5: Is Gas City a Meaningful Step Up for Solo-Scale Momentum?

INFERRED (no direct source; synthesized from architecture analysis).

For a solo developer at 4–8 concurrent Claude Code sessions with a sprint-driven cadence, Gas City's Orders system provides one genuine capability Momentum currently lacks: **persistent event-triggered dispatch without human intervention**. Specifically:

- An event-triggered formula order responds to bead events (story-bead created → dispatch sprint-dev) within one controller tick (~30 seconds), with no human keystroke required [OFFICIAL — orders.md]
- Exec orders handle mechanical operations (branch pruning, queue inspection, AVFL triggering) without burning an LLM session [OFFICIAL — orders.md]
- The controller runs as a supervised background daemon (`gc supervisor`) that restarts after crashes [OFFICIAL — nine-concepts.md]

These capabilities are not replicated by Momentum's current orchestrator-subagent fan-out pattern, which requires a human to initiate each sprint-dev cycle.

However, Gas City is still overbuilt relative to Momentum's core needs in several ways:
- The full Gastown pack (Mayor, Deacon, Polecat, Refinery) is unnecessary for Momentum — Momentum's fan-out model with 4–8 session-scoped agents does not need persistent colony management
- The convergence loops, health patrol, wisp garbage collection, and federation features address problems Momentum does not currently have
- The PackV2 migration (Issue #2120) leaves the pack/config schema in active redesign — schema stability is lower than the v1.0 label implies [OFFICIAL — maturity file]

**The step up is real but narrow:** Gas City's value for Momentum is specifically the Orders + formula dispatch loop. The rest of Gas City's feature surface is infrastructure for problems Momentum doesn't yet face.

---

## Synthesis

The contradiction between Verdict A and Verdict B resolves cleanly once the product-level distinction is established. Both verdicts are correct — they evaluate different products:

**Gas Town** is a finished, fixed orchestration platform for parallel AI-driven software development at 20–30 agent colony scale. Its architecture (fixed role taxonomy, directory-as-identity, PR-producing work model, Witness health management, Refinery merge queue) is purpose-built for this use case and is not composable into other topologies without substantial re-engineering. The maturity file's verdict — "poor fit" — is accurate.

**Gas City** is a composable orchestration SDK whose primitives (session, beads, event bus, config, prompt templates) and derived mechanisms (messaging, formulas/molecules, dispatch, orders, health patrol) are explicitly designed to have no hardcoded role names, no assumed topology, and no dependency on coding-task work models. The Orders system is a general-purpose event-triggered dispatcher that is independent of the Gastown topology. The adoption file's verdict — "architecturally right tool for Momentum's dispatcher gap" — is accurate for the specific, narrow use case of event-triggered formula dispatch.

The prior research corpus conflated these two products under the label "Gas Town / Gas City" — correct when evaluating maturity (they share a release history) but incorrect when evaluating architectural fit (they have fundamentally different design philosophies).

**The hypothesis is confirmed:** both verdicts can be simultaneously correct because Gas Town and Gas City are sufficiently different products.

---

## Open Questions

1. **Does Gas City's file-based Beads store (`GC_BEADS=file`) support the event trigger type?** The Orders architecture doc describes event triggers as depending on the Event Bus primitive and bead labels for cursor tracking. If the file store's `MolCook` or `ListByLabel` has reduced fidelity compared to the `bd` store, event-triggered orders may not work cleanly in minimal deployments without Dolt. [Cannot be determined from available documentation.]

2. **Does Momentum's existing Beads adoption (from the dual-write spike) share a Dolt database with Gas City?** If both use `bd` against the same project directory, there may be write contention. If they use separate Dolt databases, there is a data model duplication problem (story state in both places). The beads-dual-write-spike-findings file would need cross-referencing. [Requires design session, not additional research.]

3. **What is the correct mapping from Momentum skills to Gas City formulas?** The adoption file sketches a mapping (`momentum:sprint-dev` → formula → order) but the translation is UNVERIFIED. Gas City formulas invoke shell commands or agent prompts — it's not obvious how a Claude Code slash-command invocation (`/momentum:sprint-dev`) maps to a Gas City formula without a shim layer. This is the highest-value open question for any PoC design.

---

## Recommendation

The synthesis should endorse Gas City's Orders system as a legitimate target for Momentum's dispatcher gap while explicitly ruling out Gas Town's Gastown topology as the deployment model. Gas City is independently adoptable without the Gas Town Colony infrastructure — this is confirmed by official documentation and the product's own migration guide. The specific value proposition for Momentum is narrow: the event-triggered formula dispatch loop (Orders) and its five trigger types, not Gas City's broader surface area. Any PoC should validate Gas City in isolation from the Gastown pack, using the file-based Beads store initially to de-risk Dolt dependency, and treat the Orders-to-formula-to-agent path as the single hypothesis under test. The adoption file's full migration mapping (current state → Gas City equivalent table) should be retained but marked as UNVERIFIED pending PoC execution — the architectural intent is sound but the implementation path has not been walked.
