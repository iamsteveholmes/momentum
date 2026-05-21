---
content_origin: claude-code-subagent
date: 2026-05-20
sub_question: "How does Gas Town dispatch and route work? What are its dispatch primitives (queues, agents, triggers, policies)?"
topic: "Gas Town as dispatcher/coordinator for Momentum agentic engineering"
---

# Gas Town Dispatch and Routing Primitives

## Overview

Gas Town is a multi-agent workspace manager built around a small set of persistent, git-backed dispatch primitives. Its dispatch model inverts the assumption that sessions are durable: instead, **work items are durable and sessions are disposable**. Agents die and restart; their hook-mounted work does not. This section maps the dispatch architecture in depth — from the foundational propulsion principle through queues, routing tables, workflow templates, concurrency controls, and the escalation protocol.

Sources: [Official Gas Town Docs](https://docs.gastownhall.ai/) [OFFICIAL], [Gas Town README](https://github.com/gastownhall/gastown/blob/main/README.md) [OFFICIAL], [Steve Yegge's launch post](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04) [PRAC], [Augusteo Inside Gas Town](https://www.augusteo.com/blog/inside-gas-town) [PRAC].

---

## The Foundational Dispatch Principle: GUPP

Everything in Gas Town flows from a single governing rule:

> **Gas Town Universal Propulsion Principle (GUPP):** "If there is work on your Hook, YOU MUST RUN IT."

[OFFICIAL] This is not advisory. It is the invariant that makes the whole system autonomous. When a session starts, the first thing an agent does is check its Hook. If a bead is pinned there, execution begins immediately — no user prompt, no waiting for confirmation. The principle solves the "stalled system" failure mode where restarted agents sit idle until prodded.

In practice, GUPP breaks down with Claude Code because the model's safety training instills a politeness constraint: it waits for explicit input rather than acting autonomously on startup. Gas Town works around this with the **nudge system** — sending a simulated tmux `send-keys` event approximately 30–60 seconds after session start to activate GUPP behavior. [PRAC - Augusteo] This is not a clean solution; practitioners report that agents still require manual nudges in practice. [PRAC - Tenzin Wangdhen, "The Good, The Bad, The Ugly"]

---

## Core Dispatch Primitives

### The Hook

The Hook is the atomic dispatch primitive. It is a **special pinned Bead** — a persistent attachment point for one unit of work that survives process crashes and session restarts. [OFFICIAL - Glossary]

- One Hook per agent identity
- Survives session termination because it lives in git-backed Beads (Dolt), not in process memory
- When a session starts, the agent reads its Hook and begins executing whatever is pinned there
- Work is "dispatched" to an agent by placing a Bead on its Hook via `gt sling`

The Hook is a pull model dressed as push: the dispatcher places work, the agent pulls it on next wakeup.

### Beads (The Work Unit)

Beads are the atomic work items — git-backed, JSONL-format, stored in a Dolt database embedded in the repository. [OFFICIAL - Architecture]

Key properties:
- **Persistent across sessions** — a crashed session leaves its Bead open; the next session reads it from git history
- **Carry acceptance criteria** — agents evaluate their work against a completion contract, not just a description
- **Support hierarchical decomposition** — Epics are Beads with child Beads
- **Addressed by ID prefix** — the routing layer automatically maps prefixes to the correct database without requiring the caller to know which rig a Bead lives in

The terms "bead" and "issue" are used interchangeably in the codebase. [OFFICIAL]

### Hooks vs. Queues

Gas Town does not use a conventional FIFO queue. Each agent has exactly one Hook. Batch work is managed by **Convoys** (groupings of Beads) and the **Scheduler** (which controls how many Hooks get work in parallel). There is no queue that multiple agents compete to drain — work is explicitly assigned to a named agent identity.

---

## Dispatch Operations

### `gt sling` — Primary Dispatch Command

```bash
gt sling <bead-id> <rig>                    # Assign to default agent
gt sling <bead-id> <rig> --agent <alias>    # Override agent runtime
gt sling <proto> --on <bead> <rig>          # Dispatch with workflow template
```

[OFFICIAL - Reference]

`gt sling` is the universal dispatch verb. It places a Bead on an agent's Hook and optionally activates a protomolecule workflow template for multi-step execution. The `--agent` flag lets the caller override which runtime processes the work (e.g., `claude`, `gemini`, `codex`, `cursor`, `copilot`). This makes routing multi-provider at the sling level, not in a separate routing service.

### `gt convoy` — Batch Dispatch

```bash
gt convoy create "Feature X" gt-abc gt-def --notify
gt convoy list
gt convoy add <convoy-id> <issue-id>
gt convoy show [id]
```

[OFFICIAL - Reference]

Convoys bundle related Beads into a tracked batch — a "work order." They are not agent-level queues; they are coordinating envelopes. A convoy can span multiple rigs and multiple agents. The Mayor typically creates convoys after decomposing a high-level request.

A **swarm** is the set of agents currently working a convoy's Beads. Swarms are ephemeral — they exist as long as polecats are running; they dissolve when work completes.

Convoys tagged "mountain" receive special autonomous handling: stall detection and skip logic activate automatically. [OFFICIAL - README]

### `gt dog call` / `gt dog dispatch` — Infrastructure Dispatch

These commands wake idle Dogs (cross-rig persistent workers) or dispatch plugin execution through the Deacon. Dogs are used for maintenance tasks, not feature work — they return to idle after completion. [OFFICIAL - Agent Management]

### `gt callbacks process` — Inbound Message Routing

Handles agent messages from Witnesses, Refineries, and Polecats flowing back to coordinating agents. This is the return channel that feeds completion events and escalations back up the hierarchy. [OFFICIAL - Agent Management]

---

## Agent Taxonomy and Routing Roles

Gas Town defines seven roles across two organizational levels. Dispatch routing maps work type to the appropriate role.

### Town-Level Agents (Persistent, Cross-Rig)

| Agent | Role | Lifecycle | Dispatch Authority |
|-------|------|-----------|-------------------|
| **Mayor** | Global coordinator | Persistent | Creates convoys, slings to rigs |
| **Deacon** | Background supervisor | Persistent | Dispatches Dogs, monitors all Witnesses |
| **Dogs** | Infrastructure workers | Long-running | Dispatched by Deacon for maintenance |

The Mayor is the entry point for human-originated work. A human tells the Mayor what to build; the Mayor decomposes it and slings Beads across rigs.

### Rig-Level Agents (Per-Project)

| Agent | Role | Lifecycle | Work Source |
|-------|------|-----------|------------|
| **Witness** | Polecat lifecycle manager | Persistent patrol | No direct dispatch; monitors |
| **Refinery** | Merge queue processor | Persistent patrol | Merge requests from polecats |
| **Polecat** | Task executor | Ephemeral, per-task | Receives slung Beads |
| **Crew** | Persistent collaborative worker | Long-lived | Human-directed or self-assigned |

**Polecats** are the primary dispatch targets for feature work. They are spawned per-task, isolated in git worktrees, and decommissioned after submitting a Merge Request. Their names are recycled.

**Crew** are persistent agents — a developer clone running long-lived sessions. Unlike polecats, they can receive mail, route work, and maintain context across tasks.

[OFFICIAL - Glossary, Architecture; PRAC - Yegge launch post]

---

## Routing Rules and Address Resolution

### The `routes.jsonl` File

Gas Town uses a transparent routing table stored at `~/gt/.beads/routes.jsonl`. Each entry maps a Bead ID prefix to a rig's Beads database path. [OFFICIAL - Architecture]

Example:
| Prefix | Routes To | Purpose |
|--------|-----------|---------|
| `hq-*` | `~/gt/.beads/` | Cross-rig coordination (Mayor mail, convoys) |
| `gp-*` | `~/gt/greenplace/mayor/rig/.beads/` | Greenplace project |
| `wyv-*` | `~/gt/wyvern/mayor/rig/.beads/` | Wyvern project |

This means callers never need to know which database a Bead lives in — they use the ID and the routing layer resolves it. Commands like `bd show gt-xyz` automatically resolve to the correct rig's database. [OFFICIAL]

### Worktree vs. Full-Clone Routing

Gas Town uses different workspace strategies depending on agent type:
- **Polecats and Refinery:** Git worktrees (fast spawn, shared object storage from canonical `mayor/rig`)
- **Crew:** Full clones (independence from the canonical clone)

This means ephemeral agents are cheaper to spawn and share disk with the canonical repo, while persistent human-scale agents get isolation. [OFFICIAL - Architecture]

### Cross-Rig Dispatch

When a task must be executed in another rig, two options exist:
1. **Worktrees (Preferred):** Create a worktree in the target rig, preserving the agent's home-rig identity
2. **Dispatch:** Route the Bead to the target rig's local workers when they should own the work long-term

[OFFICIAL - Docs landing page]

---

## Workflow Templates: Formulas, Molecules, Wisps

Gas Town's dispatch goes beyond "run this task" — it supports multi-step, recoverable workflow execution via the MEOW stack (Molecules, Epics, Orders, Wisps). [PRAC - Augusteo]

### Formulas (Workflow Source Templates)

Formulas are TOML-defined workflow blueprints. They define steps, branching logic, and execution parameters. They are not executable directly — they must be instantiated. [OFFICIAL - Glossary]

### Protomolecules (Compiled Workflow Templates)

A formula is "cooked" (`bd cook <formula>`) into a Protomolecule — a frozen, parameterized workflow ready for instantiation. Protomolecules are reusable across tasks. [OFFICIAL - Glossary, Reference]

### Molecules (Live Workflow Instances)

Protomolecules are instantiated into Molecules via `bd mol pour <proto>`. Molecules are durable chained Bead workflows with atomic checkpoints. Key properties:

- **Any worker can continue any molecule** — nondeterministic idempotence means execution does not depend on which specific agent picks it up
- **Survive agent restarts** — completed steps remain closed in the Beads database; the next session resumes from the last open step
- **Two materialization modes:**
  - *Root-only (default):* A single root wisp executes; steps are read inline from the embedded formula. No sub-rows created. Reduces database overhead from thousands to hundreds of rows/day.
  - *Poured (`pour = true`):* Steps materialize as sub-wisps with full checkpoint recovery. Use for expensive, low-frequency workflows like releases.

[OFFICIAL - molecules.md; OFFICIAL - Glossary]

### Wisps (Ephemeral Dispatch Units)

Wisps are ephemeral Beads that exist in the database but are not persisted to git. They are used for high-velocity orchestration operations (patrol cycles, refinery cycles) that should not pollute the repository history. Wisps are destroyed after execution. [OFFICIAL - Glossary]

The `gt sling --on <proto>` form dispatches work with an attached protomolecule, turning a simple Bead assignment into a multi-step workflow dispatch.

---

## Trigger Mechanisms

### How Work Gets Dispatched (Push vs. Pull)

Gas Town is primarily a **pull system with push injection**:

1. **Push:** The human or Mayor calls `gt sling`, placing a Bead on an agent's Hook
2. **Pull:** The agent, on next wakeup, reads its Hook and begins executing (GUPP)

There are no webhooks or event subscriptions for dispatch. Work does not arrive; it is placed.

### Patrol Loops (Polling-Based Triggers)

Rather than pure event-driven architecture, persistent agents (Deacon, Witness, Refinery) use **polling-based patrol loops with exponential backoff**. [PRAC - Augusteo]

- Agents wake periodically, check for state changes (new Beads, stuck workers, merge conflicts)
- Sleep duration increases exponentially when no work is found
- Any mutating `gt` or `bd` command immediately wakes the daemon, interrupting the backoff sleep

This design trades event immediacy for operational simplicity — no message broker, no event bus, no pub/sub infrastructure required.

### The Daemon's Role in Triggering

The Gas Town daemon (a Go process running in the background) is responsible for:
- Receiving heartbeats from agents
- Enforcing the scheduler's concurrency limit (see below)
- Waking patrol agents when mutations occur
- Maintaining the health of the watchdog chain

Without the daemon running, deferred dispatch and scheduled patrol interruption do not work.

### Session Startup Trigger (Nudge Workaround)

Because Claude Code doesn't autonomously follow GUPP, Gas Town fires simulated keyboard input via tmux `send-keys` approximately 30–60 seconds after session startup to force the agent to read its hook. [PRAC - Augusteo] This is described as a "physics over politeness" workaround — bypassing training constraints with mechanical input rather than relying on the model's judgment.

---

## Concurrency and Capacity Management

### The Scheduler

Gas Town has a config-driven capacity governor for polecat dispatch. [OFFICIAL - README]

```bash
gt config set scheduler.max_polecats 5   # Enable deferred dispatch, max 5 concurrent
gt config set scheduler.max_polecats -1  # Immediate dispatch (default)
gt scheduler status                      # View current state
```

- **Default (`-1`):** Every `gt sling` immediately places work on the target agent's Hook. No queuing.
- **With a limit set:** The daemon maintains a count of active polecats. Slings beyond the limit are queued and released incrementally as polecats complete and exit.

This prevents API rate-limit exhaustion when running large swarms. Without a limit, 20+ simultaneous polecats will quickly hit provider rate limits.

### The Refinery's Merge Queue (Serialized Merges)

Concurrent polecats produce concurrent Merge Requests, which creates rebase conflicts on main. The Refinery serializes merges using a **Bors-style bisecting merge queue**:

1. Polecat calls `gt done` → branch pushed, MR created
2. Refinery batches pending MRs
3. Runs: "merge all, test once"
4. If batch passes, all land
5. If batch fails: split in half, retry each half recursively
6. Bad MRs are isolated in O(log N) test cycles rather than O(N) sequential

[PRAC - Augusteo; OFFICIAL - Agent Management]

The Refinery patrols the merge queue continuously via the `mol-refinery-patrol` wisp, not on a fixed schedule.

---

## Model Routing (Tier-Based Dispatch)

An RFC (Discussion #2531) proposes — and the community has partially adopted — a tier-based model routing convention. [OFFICIAL - gastownhall/gastown Discussion #2531]

### Emergent Convention (Community Practice)

| Role | Recommended Tier | Reasoning |
|------|-----------------|-----------|
| Mayor, Crew | Large (e.g., Opus) | Planning, cross-context reasoning, architectural decisions |
| Polecat | Medium (e.g., Sonnet) | Implementation tasks — scoped, frequent, cheaper |
| Witness, Deacon, Dogs | Small/Medium (e.g., Haiku) | Monitoring and patrol cycles are lightweight |

### Proposed RFC Architecture

The RFC formalizes this into three phases:
1. **Phase 1:** Abstract tier config + role defaults (formalize convention)
2. **Phase 2:** Mayor override API — Mayor can force a specific model for a sensitive task
3. **Phase 3:** Optional dedicated LLM router — a local Ollama instance evaluates task complexity and upgrades/downgrades from role defaults dynamically

The `--agent` flag on `gt sling` already allows per-sling runtime override as a manual escape hatch. [OFFICIAL - Reference]

---

## Escalation Protocol

When an agent hits a blocker it cannot resolve, it escalates rather than stalling:

```bash
gt escalate "Blocker description"          # Default: MEDIUM severity
gt escalate -s HIGH "blocker"              # Important blocker
gt escalate -s CRITICAL "urgent"           # Immediate attention needed
```

Severity routing:
- **CRITICAL (P0):** Immediate — routes to Deacon → Mayor → Overseer chain
- **HIGH (P1):** Blocker — routed to Mayor
- **MEDIUM (P2):** Default — tracked in Beads, surfaced at next patrol

[OFFICIAL - Agent Management, Reference]

Escalations create tracked Beads that are routed through the Deacon and Mayor. This means the escalation system uses the same Beads infrastructure as regular work — there's no separate message bus.

---

## Health Monitoring and Watchdog Chain

Dispatch reliability depends on knowing when agents are stuck. Gas Town has a three-tier watchdog:

| Layer | Agent | Frequency | Responsibility |
|-------|-------|-----------|----------------|
| Per-Rig | Witness | Continuous patrol | Detects stalled polecats, triggers recovery |
| Town-Wide | Deacon | Every few minutes | Monitors all Witnesses, manages Dogs |
| Infrastructure | Daemon | Every 10 min heartbeat | Receives mechanical heartbeats, runs plugins |

```bash
gt deacon health-check <agent>    # Ping agent
gt deacon health-state            # All agent health
gt peek <agent>                   # Check agent status
gt feed                           # Interactive TUI dashboard
gt feed --problems                # Focus on stuck agents
```

Agents unresponsive for 30 minutes without progress trigger escalation automatically. [PRAC - comparison with Swarm-Tools]

---

## Gas City: The Next-Generation Dispatch Model

Gas City (`gastownhall/gascity`) is Gas Town's successor, recast as a **composable SDK** rather than a role-taxonomy framework. [OFFICIAL - gascity GitHub; OFFICIAL - coming-from-gastown.md]

Key architectural changes to dispatch:

| Concept | Gas Town | Gas City |
|---------|----------|----------|
| **Primary dispatch** | `gt sling` + convoy + polecat role | Orders (exec or formula) |
| **Routing** | Role taxonomy + filesystem layout | `city.toml` config + controller |
| **Exec dispatch** | Plugin system through Deacon | Exec orders (no LLM session needed) |
| **Workflow dispatch** | Formula → molecule → polecat | Formula orders (agent-driven) |
| **Session types** | Hardcoded (polecat/crew/dog) | Operating conventions, not SDK types |
| **State** | Implicit filesystem state | Explicit metadata in Beads |

The Gas City controller implements a **reconcile loop** — desired state declared in config, controller reconciles to running state. This is closer to a Kubernetes Operator model than Gas Town's patrol-based approach.

**Exec orders** run without spawning an LLM session (pure shell/controller logic). **Formula orders** instantiate agent-driven multi-step workflows. This separation eliminates the need for "helper agents" like the Deacon's Dogs — controller-side logic runs directly.

[OFFICIAL - coming-from-gastown.md; PRAC - gascity GitHub search results]

Note: Gas City 1.0 is active development as of 2026-05-20. Some multi-step execution features are described as "backend-dependent today." [UNVERIFIED - inferred from search results]

---

## Summary Table: Dispatch Primitive Inventory

| Primitive | Type | Durability | Use Case |
|-----------|------|-----------|---------|
| Hook | Pinned Bead | Persistent (git-backed) | Agent's primary work queue |
| Bead | Work unit | Persistent (Dolt/git) | Any atomic task |
| Wisp | Ephemeral Bead | Non-persistent | Patrol/orchestration operations |
| Convoy | Work batch | Persistent | Group related Beads, track progress |
| Swarm | Agent group | Ephemeral | Agents currently working a convoy |
| Molecule | Workflow instance | Persistent (checkpointed) | Multi-step recoverable workflows |
| Protomolecule | Workflow template | Persistent | Reusable workflow definitions |
| Formula | Workflow source | Persistent (TOML) | Workflow authoring |
| Nudge | Message | Fire-and-forget | Real-time agent-to-agent communication |
| Escalation | Tracked Bead | Persistent | Blocker escalation chain |
| Route | Config entry | Persistent | ID-prefix → database mapping |

---

## Sources

- [Gas Town Docs — Landing](https://docs.gastownhall.ai/) [OFFICIAL]
- [Gas Town Docs — Architecture](https://docs.gastownhall.ai/design/architecture/) [OFFICIAL]
- [Gas Town Docs — Agent Management](https://docs.gastownhall.ai/usage/agent-management/) [OFFICIAL]
- [Gas Town Docs — Reference](https://docs.gastownhall.ai/reference/) [OFFICIAL]
- [Gas Town Docs — Glossary](https://docs.gastownhall.ai/glossary/) [OFFICIAL]
- [Gas Town GitHub — gastownhall/gastown](https://github.com/gastownhall/gastown) [OFFICIAL]
- [Gas Town README](https://github.com/gastownhall/gastown/blob/main/README.md) [OFFICIAL]
- [Gas Town — molecules.md](https://github.com/gastownhall/gastown/blob/main/docs/concepts/molecules.md) [OFFICIAL]
- [Gas Town — Intelligent Routing RFC #2531](https://github.com/gastownhall/gastown/discussions/2531) [OFFICIAL]
- [Gas City GitHub — gastownhall/gascity](https://github.com/gastownhall/gascity) [OFFICIAL]
- [Gas City — Coming from Gastown](https://github.com/gastownhall/gascity/blob/main/docs/getting-started/coming-from-gastown.md) [OFFICIAL]
- [Steve Yegge — Welcome to Gas Town (Medium)](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04) [PRAC]
- [Augusteo — Inside Gas Town](https://www.augusteo.com/blog/inside-gas-town) [PRAC]
- [Tenzin Wangdhen — Gas Town: The Good, The Bad, The Ugly](https://tenzinwangdhen.com/posts/gastown-good-bad-ugly/) [PRAC]
- [Gas Town vs Swarm-Tools (GitHub Gist)](https://gist.github.com/johnlindquist/4174127de90e1734d58fce64c6b52b62) [PRAC]
- [Paddo.dev — GasTown and the Two Kinds of Multi-Agent](https://paddo.dev/blog/gastown-two-kinds-of-multi-agent/) [PRAC]
