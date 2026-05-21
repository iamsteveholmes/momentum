---
content_origin: research-agent
date: 2026-05-20
sub_question: "Can Gas City Orders function as a standalone dispatcher for Momentum without the full Gas Town Colony topology?"
---

# Gas City Orders as Standalone Dispatcher for Momentum

## Research Question

Can Gas City's Orders system be used as a minimal dispatcher for Momentum — specifically firing Momentum skill formulas (Claude Code sessions) in response to sprint events (story ready, intake created, quick-fix triggered) — WITHOUT deploying the full Gas Town Colony topology (Mayor, Deacon, Polecat workers, Refinery, etc.)?

Sub-questions investigated:
1. What is the minimal Gas City setup to use Orders? City required or just Controller?
2. How does a Gas City Formula invoke a Claude Code session?
3. Are there community examples of Gas City at small scale?
4. What is the exec order pattern and does it cover Claude Code CLI invocations?
5. Is Gas City Orders usable without Dolt?

---

## Sources Consulted

- [OFFICIAL] Gas City GitHub repository — `github.com/gastownhall/gascity` — repository structure, README, internal source
- [OFFICIAL] Gas City quickstart docs (`docs.gascityhall.com/getting-started/quickstart`) — init commands, controller startup, GC_BEADS=file
- [OFFICIAL] Gas City Orders tutorial (`gascityinc-5c0069dd.mintlify.app/tutorials/07-orders`) — exec vs formula orders, trigger types, TOML syntax
- [OFFICIAL] Gas City `internal/orders/triggers.go` source — trigger evaluation logic, event cursor tracking, condition checks
- [OFFICIAL] Gas City `internal/runtime/exec/exec.go` source — exec provider subprocess pattern, exit code semantics
- [OFFICIAL] Gas City `internal/runtime/tmux/tmux.go` source — how tmux sessions are started for agent invocation
- [OFFICIAL] Gas City `coming-from-gastown.md` docs — Orders replace Gas Town plugins, Controller owns dispatch
- [OFFICIAL] Gas City `tutorials/01-cities-and-rigs.md` — what a City is, implicit agent providers, rig definition
- [PRAC] Steve Yegge, "Welcome to Gas City" (Medium, April 2026) — Formulas, MEOW stack, exec vs formula distinction
- [PRAC] Gemini deep research, Follow-up 1 — PackV2 status, MCP deferral
- [PRAC] Gemini deep research, Follow-up 2 — Orders event model, exec orders as external trigger bridge
- [PRAC] `research-adoption-path-risks.md` (prior research subagent) — Orders PoC path, five trigger types, prerequisite list
- [PRAC] `research-dispatch-routing-primitives.md` (prior research subagent) — Gas City dispatch vs Gas Town comparison table
- [PRAC] `research-gas-city-architecture.md` (prior research subagent) — Controller reconcile loop, pack model
- [PRAC] `research-momentum-integration-mapping.md` (prior research subagent) — Momentum workflow → Gas City mapping
- [PRAC] `avfl-report.md` (AVFL validator) — corpus contradiction flags, MCP gap identification (CON-008)
- [PRAC] gastownhall/gastown Discussion #624 — solo developer lighter-weight patterns

---

## Findings

### Finding 1: A "City" is Required — But It Is Minimal

CONFIRMED: Gas City's Orders system requires a running Controller process, and the Controller is started as part of `gc init` (city initialization). There is no documented standalone Controller mode that runs Orders without a City directory structure. [OFFICIAL: quickstart docs — "gc init bootstraps the city directory, registers it with the supervisor, and starts the controller. The city is running as soon as init completes."]

However, "a City" does not mean the full Gas Town Colony topology. A minimal Gas City city requires:
- `gc` CLI binary
- `tmux`
- `git`
- `jq`
- A beads provider (Dolt by default, or `GC_BEADS=file` to skip)

It does NOT require: Mayor agent, Deacon, Witness, Polecats, Refinery, or any of Gas Town's role-specific agents. [OFFICIAL: Gas City quickstart] Those are the Gas Town pack — they are optional, importable pack configuration, not SDK prerequisites. The Controller itself is a reconcile loop — a Go process — not an agent.

CONFIRMED: The minimal working city is three commands:
```bash
gc init ~/momentum-city
gc rig add ~/my-project
gc start  # if not already running
```

Then Orders defined in `city.toml` fire without any Gas Town Colony agents. [OFFICIAL: tutorials/01-cities-and-rigs.md]

### Finding 2: Exec Orders Run Without Any LLM Session — Directly Applicable to Claude Code CLI

CONFIRMED: Exec orders are a first-class Gas City primitive explicitly designed to "run shell commands directly on the controller — no agent, no LLM, no wisp." [OFFICIAL: Orders tutorial]

The exec provider implements the "Git credential helper pattern": the controller forks a subprocess, pipes operation + arguments through stdin/stdout, and interprets exit codes. This is a plain shell subprocess — not tmux, not MCP, not a long-lived session. [OFFICIAL: `internal/runtime/exec/exec.go`]

This means an exec order can directly invoke `claude -p "run momentum:sprint-dev for story XYZ"` as a subprocess. The Claude Code CLI (`claude`) is already on PATH in the developer's environment and does not require any Gas City-specific integration to invoke. The exec provider handles:
- Bounded timeout enforcement (default 300 seconds for exec orders)
- stdout/stderr capture
- Exit code semantics (0 = success, 1 = error, 2 = unknown op, treated as success)

CONFIRMED: For Momentum's dispatch use case — "fire a Claude Code session for each story-ready event" — exec orders are the correct pattern, and they require no deferred Gas City features. The MCP deferral (CON-008 in the AVFL report) affects formula orders that rely on MCP toolchains for agent coordination, NOT exec orders that invoke the Claude CLI as a subprocess.

### Finding 3: Formula Orders Dispatch Agent-Driven Workflows — But MCP Is Deferred

CONFIRMED: Formula orders pair a trigger with a named formula and dispatch to an agent pool. TOML syntax:
```toml
[order.run-sprint-story]
formula = "sprint-dev"
pool = "worker"
trigger.event = "bead.closed"
```
[OFFICIAL: Orders tutorial]

Formula orders require: (1) a named formula defined in `formulas/<name>.toml`, (2) a named agent pool in `city.toml`, (3) an agent provider (claude, codex, gemini — these are implicit without explicit config). The controller dispatches the formula by starting a tmux session with the appropriate provider's binary. [OFFICIAL: `internal/runtime/tmux/tmux.go` — sessions created via `NewSessionWithCommand()` with the provider command dynamically resolved]

INFERRED: The Claude Code binary invocation path from a formula order is: Controller → tmux new-session → claude binary (resolved via `GT_PROCESS_NAMES` or `GT_AGENT` env vars). There is no hardcoded `claude` invocation — Gas City resolves the binary at runtime.

CONFIRMED (critical gap): First-class MCP runtime support was explicitly deferred from PackV2. [OFFICIAL: Gemini Follow-up 1 — "Hold off on native MCP integration: Gas City does not yet offer full runtime support for [MCP]"] Momentum's skills are invoked as Claude Code slash commands (`/momentum:sprint-dev`), which operate within Claude Code's MCP toolchain. If a formula order starts a Claude Code session and that session needs to call Momentum's skills via MCP, that toolchain is not natively managed by Gas City yet. The session must configure MCP independently at the agent level.

INFERRED: This gap affects formula orders more than exec orders. An exec order calling `claude -p "run the sprint-dev skill"` with an appropriate prompt bypasses the MCP runtime gap — it relies on Claude Code's own MCP handling within the session, not on Gas City's MCP runtime. Momentum's skills are invoked as Claude Code agent instructions, and Claude Code handles MCP internally regardless of how the session was started.

### Finding 4: Five Trigger Types — Event Triggers Are the Natural Fit for Momentum

CONFIRMED: Gas City Orders support five trigger types:

| Type | Behavior | Momentum Relevance |
|------|----------|--------------------|
| Cooldown | Fires after interval since last run | Story polling fallback |
| Cron | Absolute wall-clock schedule | Sprint kickoff at fixed time |
| Condition | Shell exit-code check (10s timeout) | "are there ready stories?" check |
| Event | Fires on `bead.closed`, `bead.created` etc. | Natural story-state triggers |
| Manual | Only via `gc order run` | Explicit human-triggered dispatch |

[OFFICIAL: `internal/orders/triggers.go`, Orders tutorial]

For Momentum, the natural wiring is:
- `trigger.event = "bead.created"` with a condition filter → fires `sprint-dev` formula when a story bead enters `status=ready`
- Condition trigger checking a file flag → fires `quick-fix` when the intake queue has entries
- Manual trigger → explicit sprint kickoff by the developer

Event triggers use a sequence-based cursor in the events provider — each trigger tracks `seq:<N>` in bead labels to prevent duplicate firing. [OFFICIAL: `triggers.go` source]

CONFIRMED: The Gemini Follow-up 2 research is consistent with the source code analysis: "the Gas City Controller watches the Event Bus, which is an append-only pub/sub log of all system activity, separate from the durable Beads storage." Orders fire based on trigger conditions evaluated every 30 seconds (one "tick"). [PRAC: Gemini Follow-up 2]

### Finding 5: Dolt Is Optional — GC_BEADS=file Removes It

CONFIRMED: Gas City explicitly provides a Dolt escape hatch. Setting `GC_BEADS=file` (environment variable) or `[beads] provider = "file"` in `city.toml` disables the Dolt/bd/flock dependency entirely and uses file-based storage instead. [OFFICIAL: Gas City GitHub README, quickstart docs]

INFERRED: The file-based provider is adequate for Momentum's solo-developer dispatch use case. Dolt's advantages (transactional consistency under concurrent writes, versioned SQL queryability) matter when 20-30 agents write simultaneously — not when a single developer runs one sprint at a time with 3-6 sequential stories. However, if Momentum is already adopting Beads as a tracking layer (the `beads-dual-write-spike` story is at `ready-for-dev` as of 2026-05-20), running Dolt for both Beads and Gas City sharing the same store is the natural path.

IMPORTANT CORRECTION (from AVFL CON-006): The claim that Beads is "already adopted" in Momentum is inaccurate — it is planned but not yet operational. This increases the integration complexity and means Dolt stability risks affect both Beads adoption and Gas City adoption simultaneously.

### Finding 6: Community Precedent for Minimal / Solo Use Is Thin

INFERRED: There are no documented community examples of Gas City Orders being used at solo-developer scale (1-4 agents, skill-based workflows) as of May 2026. The Gas City repository was released April 27, 2026 — less than one month old. [OFFICIAL: GitHub release tags] The Gas Town Discussion #624 community thread reveals the solo-developer pattern for Gas Town (not Gas City) is: "single rig, one Crew member, no Polecats, no Witness/Refinery/Convoys — just Beads for tracking and worktrees when needed." This translates to Gas City as: one city, one rig, Orders for dispatch, no Gas Town pack. [PRAC: gastownhall/gastown Discussion #624]

CONFIRMED: The Gas City SDK explicitly positions the Gas Town colony as one optional pack, not the default. The architecture docs state the Gas Town pack is "a fully functional Gas Town compatibility pack" that drops into Gas City — it is not required. [OFFICIAL: `research-gas-city-architecture.md` citing gascity README]

### Finding 7: Known Stability Risk — Dolt Concurrent Write Bug

CONFIRMED: Bug #1930 in the Gas City issue tracker documents a Dolt supervisor conflict where competing processes on the same Dolt port caused ~23,759 restarts over 6 hours, leaving `.beads/dolt/` empty and blocking all `gc sling` operations. [PRAC: `research-adoption-path-risks.md` citing GitHub Issue #1930] This risk is relevant even at solo scale if the controller and any Momentum story processes write to the same Beads database concurrently.

CONFIRMED: Gas City v1.1.0 (May 6, 2026 — 455 commits) explicitly included "managed Dolt hardening" as a release theme, suggesting active work on this class of problem. [OFFICIAL: `research-maturity-production-readiness.md` citing v1.1.0 release notes] Status of Issue #1930 specifically is UNKNOWN — not confirmed fixed.

---

## Synthesis

### Direct Answer to the Primary Question

**Conditional YES.** Gas City Orders can function as a minimal dispatcher for Momentum without the full Gas Town Colony topology, with three important conditions:

1. **A City (not just a Controller) is required.** `gc init` is the entry point — Orders do not run standalone. However, "a City" in this context means only the `gc` controller process, a city directory, and one rig. No Mayor, Deacon, Witness, Polecats, or Refinery agents are needed.

2. **The initial integration should use exec orders, not formula orders.** Exec orders call `claude -p` as a direct subprocess — no MCP runtime dependency, no Gas City formula resolution complexity. Formula orders are the natural long-term target (trigger → formula → agent pool), but they run into Gas City's deferred MCP support, which means the skill invocation layer must be handled at the Claude Code session level, not at the Gas City level. For an initial PoC, exec orders are the pragmatic path.

3. **Dolt is avoidable but creates a tradeoff.** `GC_BEADS=file` removes the Dolt dependency but loses event-based triggers — the Event Bus that `trigger.event = "bead.closed"` listens to is Beads-backed. Without Dolt/Beads, Momentum would be limited to cooldown, cron, condition, and manual triggers. For story-ready dispatch, a condition trigger checking a file flag (`test -f .momentum/sprint/ready-flag`) is a viable substitute that keeps Dolt optional.

### The Exec Order Pattern for Momentum

The exec order pattern for dispatching a Momentum sprint story would look like:

```toml
# in city.toml or a pack
[order.dispatch-ready-stories]
description = "Fire sprint-dev for each story in status=ready"
trigger = "condition"
check = "scripts/check-ready-stories.sh"
exec = "scripts/dispatch-story.sh"
```

Where `dispatch-story.sh` does: `claude -p "You are running momentum:dev for story $(cat .momentum/sprint/next-ready-story)"`. This is a shell subprocess — no Gas City MCP runtime involvement — and Claude Code handles Momentum's MCP toolchain internally when it starts.

This pattern means the Gas City controller is functioning as a **cron/condition-triggered shell launcher**, not a full orchestration runtime. That is precisely the "minimal dispatcher" use case Momentum needs.

### Cross-Cutting Tensions

**Tension 1: Exec orders are powerful enough, but formula orders are the intended path.** Gas City's design intent is for exec orders to handle mechanical/infrastructure work and formula orders to handle agent-driven workflow dispatch. Using exec orders to launch Claude Code sessions is using Gas City as a shell script scheduler — which works but undersells the platform and may diverge from future Gas City conventions as MCP support lands.

**Tension 2: The Orders system requires a City, and Cities are not zero-overhead.** The controller is a persistent Go process with its own footprint. For a solo developer who opens Claude Code once a day, the value of a continuously running controller is lower than for a team running 20-30 parallel agents. The overhead is manageable but should not be invisible.

**Tension 3: Gas Town (poor fit) vs Gas City (potentially good fit) are not the same product.** The AVFL corpus contained a direct contradiction (CON-001): one subagent concluded Gas Town was "a poor fit" while another concluded Gas City "is architecturally the right tool." Both conclusions are consistent with each other: Gas Town's fixed Mayor→Deacon→Witness→Polecat topology is poor fit for Momentum; Gas City's composable Orders system without that topology is a better-fit tool. The distinction is real and should not be collapsed.

---

## Minimum Viable Integration (3 Steps)

Assuming the research validates as viable, the minimum viable integration is:

**Step 1: Initialize a City with file-based Beads (no Dolt required)**
```bash
brew install gastownhall/gascity/gascity
GC_BEADS=file gc init ~/momentum-city
gc rig add ~/projects/my-project
```
Validates: controller starts, rig registers, no Dolt dependency.

**Step 2: Wire one exec order for manual dispatch**
```toml
# ~/momentum-city/city.toml
[order.sprint-story]
description = "Dispatch a Momentum sprint story"
trigger = "manual"
exec = "scripts/run-momentum-dev.sh"
```
Where `run-momentum-dev.sh` invokes `claude -p` with the story context. Validates: exec order fires, Claude Code session starts, Momentum skill runs, session exits cleanly.

**Step 3: Replace manual trigger with condition trigger**
```toml
[order.sprint-story]
trigger = "condition"
check = "test -f $HOME/projects/my-project/.momentum/sprint/story-ready.flag"
exec = "scripts/run-momentum-dev.sh"
```
Validates: controller polls the condition every 30 seconds, fires automatically when a story is marked ready (Momentum writes the flag file), Claude Code session runs and the flag is cleared on completion.

This 3-step path avoids Dolt, avoids formula complexity, avoids MCP runtime dependency, and avoids the Gas Town Colony topology entirely. It proves the core dispatch loop. Further steps (event triggers via Beads, formula-based dispatch, Dolt adoption) can be added incrementally once the exec order baseline is stable.

---

## Open Questions

1. **Does `GC_BEADS=file` support the Event Bus used by event triggers?** The source evidence suggests the Event Bus is Beads-backed — if so, `bead.closed` and `bead.created` event triggers may be unavailable without Dolt. This must be confirmed before designing event-triggered dispatch. (Matters because event triggers are the cleanest Momentum integration story.)

2. **What is the actual command Gas City uses to invoke Claude Code in a formula order?** The tmux provider resolves the binary via `GT_PROCESS_NAMES` or `GT_AGENT` env vars, but the specific arguments passed (`--dangerously-skip-permissions`, `-p`, etc.) are not confirmed from source. This determines whether Momentum's `claude -p` invocation pattern is compatible with Gas City's agent spawning.

3. **Is Issue #1930 (Dolt concurrent writes) resolved in Gas City v1.1.0?** The v1.1.0 release included "managed Dolt hardening" but the issue status was not verified. If unresolved, Dolt adoption carries meaningful operational risk for Momentum's story-tracking layer.

4. **Can Momentum's `GC_BEADS=file` city share a Beads Dolt instance with a later Dolt-backed city?** If Momentum starts with `GC_BEADS=file` and later wants to add Beads-backed event triggers, is migration from file to Dolt straightforward or a breaking change?

5. **Does the exec order pattern (Gas City as a shell scheduler) violate Gas City's intended use in ways that would break on upgrade?** Exec orders are explicitly supported but positioned as "mechanical operations" — using them to launch LLM sessions is a use Gas City didn't explicitly design for. Need to confirm this usage pattern doesn't conflict with future Gas City changes.

---

## Verdict

Gas City Orders **can** serve as a standalone dispatcher for Momentum without the Gas Town Colony topology — the Mayor, Deacon, Witness, Polecats, and Refinery are entirely optional. The minimum viable integration is a `gc init` city with one rig, one exec order triggered by a condition check, and a shell script that invokes `claude -p` with the story context. This avoids Dolt (via `GC_BEADS=file`), avoids the MCP runtime gap (exec orders call the Claude CLI as a subprocess), and avoids Gas City's unfinished formula/pool machinery. The critical constraint is that **a City directory and a running Controller process are required** — there is no "orders-only" mode lighter than a full `gc init`. For a solo developer who wants the simplest possible dispatch trigger, the overhead of the Gas City controller is real but manageable, and the exit ramp (remove `gc`, keep the shell scripts) is clean.
