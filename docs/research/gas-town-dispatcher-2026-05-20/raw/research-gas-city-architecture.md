---
content_origin: claude-code-subagent
date: 2026-05-20
sub_question: "What is Gas Town / Gas City? Architecture, primitives, core abstractions, and the problem it solves."
topic: "Gas Town as dispatcher/coordinator for Momentum agentic engineering"
---

## What Is Gas Town?

Gas Town is a multi-agent workspace manager built on top of AI coding agents (primarily Claude Code) that coordinates colonies of 20–30 parallel agents on shared software projects. It was created by Steve Yegge and released publicly in early January 2026, reaching stable v1.0.0 in April 2026. [OFFICIAL] The core source of truth is the official documentation at https://docs.gastownhall.ai/ and the GitHub organization at https://github.com/gastownhall.

Gas Town is not a framework in the traditional sense—it is an orchestration layer that treats agent work as structured, durable data. Where most multi-agent systems manage conversations or reasoning chains, Gas Town's central innovation is inverting the persistence model: **make the work durable, not the agent**. Sessions are disposable; agents have persistent identities; work survives crashes by living in git. [PRAC: https://www.augusteo.com/blog/inside-gas-town]

The guiding metaphor is a company: the developer is a factory operator, the Mayor agent is the chief-of-staff, Polecats are assembly-line workers, and the Deacon is the facilities manager running continuous system health checks. All coordination happens through externalized state—a git-versioned SQL database (Dolt)—not through inter-agent messaging in memory. [OFFICIAL: https://docs.gastownhall.ai/]

---

## The Problem Gas Town Is Designed to Solve

### Agent Cognitive Degradation

LLM-based coding agents have a fundamental limitation: context windows fill and agents "develop progressive dementia," losing awareness of prior decisions. Gas Town's founder describes this as agents having "zero attention span." [PRAC: https://steve-yegge.medium.com/gas-town-from-clown-show-to-v1-0-c239d9a407ec] Gas Town solves this by externalizing all work state into Beads stored in Dolt/git—agents can be destroyed and recreated at will, picking up exactly where the last session left off.

### Coordination Chaos at Scale

Managing 10+ parallel coding agents manually becomes untenable. Without a coordination layer, agents write conflicting code to the same files, lose track of what's in progress, and create unresolvable merge conflicts. Gas Town provides structured work decomposition, isolated git worktrees per agent, a Bors-style merge queue (the Refinery) that intelligently bisects bad merges, and hierarchical supervisors that detect stuck agents and trigger recovery. [OFFICIAL: https://docs.gastownhall.ai/glossary/]

### Missing Work Attribution and Auditability

In single-agent chat workflows, there is no record of which agent made which decision or why. Git preserves the "What, Where, Who, and How" of code changes, but not the "Why." Gas Town's Beads system adds the missing context: each work item carries acceptance criteria, decision rationale, and a full execution history. [PRAC: https://steve-yegge.medium.com/gas-town-from-clown-show-to-v1-0-c239d9a407ec] This enables objective model comparison, capability mapping, and cost optimization by tracking agent performance data over time.

### Claude Code's "Politeness Problem"

Claude Code's safety training creates a deadlock in autonomous workflows: even when an agent has executable work, it tends to wait for human confirmation rather than proceeding. Gas Town works around this with a mechanical tmux send-keys technique that simulates keystroke input to bypass this alignment artifact and allow fully autonomous agent execution. [PRAC: https://www.augusteo.com/blog/inside-gas-town]

---

## Core Architecture

### The Town / Rig Hierarchy

Gas Town organizes into two scopes:

- **Town** (the `~/gt/` directory): The coordination hub. Hosts cross-project agents (Mayor, Deacon) and serves as the workspace root. One Town can manage many Rigs.
- **Rig**: A Git repository under Gas Town management. Each Rig contains its own workers (Polecats, Crew), its own merge processor (Refinery), and its own health monitor (Witness). [OFFICIAL: https://docs.gastownhall.ai/glossary/]

This separation enables scaling from a single repo to a swarm spanning dozens of parallel initiatives managed by one operator.

### The Data Substrate: Beads and Dolt

The foundational data primitive is the **Bead** — a git-backed atomic work unit stored in JSONL format, representing a single issue, task, or epic. Beads are versioned alongside code: checking out an old commit rewinds work state as well as source state. [OFFICIAL: https://docs.gastownhall.ai/glossary/]

In v1.0, Beads migrated from fragile SQLite + JSONL to **Dolt**: a git-versioned relational database that speaks the MySQL protocol. A single Dolt SQL server per Town serves all databases on port 3307. Agents write to main using explicit transaction discipline (`BEGIN / DOLT_COMMIT / COMMIT` atomically), eliminating the race conditions and merge conflicts that plagued earlier versions. [PRAC: https://steve-yegge.medium.com/gas-town-from-clown-show-to-v1-0-c239d9a407ec]

Dolt provides:
- SQL queryability over version-controlled work data
- Full audit trail with branch coupling to code history
- Multi-session recovery from any checkpoint
- Transactional consistency across concurrent agent writers

---

## Core Primitives and Abstractions

### GUPP — The Dispatch Primitive

**GUPP (Gas Town Universal Propulsion Principle)** is the scheduling rule that drives autonomous execution:

> "If there is work on your Hook, YOU MUST RUN IT."

This is a pull-based dispatch model. There is no central scheduler pushing work to agents. Instead, work is "slung" onto an agent's Hook (its personal queue), and agents check their Hook on startup and begin work immediately. No waiting, no confirmation. [OFFICIAL: https://docs.gastownhall.ai/glossary/]

The `gt sling` command places a Bead on a target agent's Hook. The `gt nudge` command sends real-time messages between agents. These two primitives—sling and nudge—constitute the entire dispatch surface from the operator's perspective.

### The MEOW Stack — Work Composition Hierarchy

Gas Town's workflow abstraction is called **MEOW (Molecular Expression of Work)**. It has five composition levels: [OFFICIAL: https://docs.gastownhall.ai/glossary/] [PRAC: https://reading.torqsoftware.com/notes/software/ai-ml/agentic-coding/2026-01-15-gas-town-multi-agent-orchestration-framework/]

| Layer | Description |
|-------|-------------|
| **Bead** | Atomic unit — a single issue with acceptance criteria, status, and history |
| **Epic** | A Bead with children, used for planning hierarchies |
| **Molecule** | Durable chained Bead workflows — a directed graph of Beads agents walk sequentially |
| **Protomolecule** | Template graph with placeholders, ready for instantiation |
| **Formula** | TOML source definition with macros, gates, and loops — compiles into Protomolecules |
| **Wisp** | Ephemeral Bead, destroyed after the run — used for orchestration-only transient operations |

Formulas are the top-level authoring surface. A developer writes a Formula in TOML to express a reusable workflow pattern (e.g., "patrol all Rigs and triage stuck agents"), and Gas Town instantiates it into a Molecule with tracked execution state. Molecule steps can be crashed and resumed: an agent reads chain state from git, finds the last completed Bead, and continues from there. [PRAC: https://www.augusteo.com/blog/inside-gas-town]

### NDI — Reliability Guarantee

**NDI (Nondeterministic Idempotence)** is Gas Town's correctness model. Unlike deterministic replay systems (like Temporal), LLM execution paths are non-reproducible. Gas Town guarantees outcome-level—not trajectory-level—durability:

1. Workflow (Molecule) persists in git
2. Each Bead has explicit acceptance criteria
3. Agents claim and close Beads one at a time
4. Crashed Beads remain open; the next session completes them
5. Path varies; destination is invariant [PRAC: https://www.augusteo.com/blog/inside-gas-town]

This trades exact replay for practical reliability: the path to the goal can be different each time, but the goal is guaranteed to be reached.

### Hooks — The Work Queue Primitive

Each agent has a **Hook**: a special pinned Bead that acts as their personal work queue. The Hook is a durability primitive—it persists in Dolt/git so work survives process crashes and session restarts. The GUPP principle mandates that agents execute whatever is on their Hook immediately. When no Hook work exists, agents wait in a ready state. [OFFICIAL: https://docs.gastownhall.ai/glossary/]

### Convoys — Work Batching and Visibility

A **Convoy** is the primary work-order object, grouping related Beads for delivery tracking. The Mayor creates Convoys to batch related work, enabling:
- Cross-Rig visibility of "what's in flight"
- Auto-notification on completion
- Historical record of related work grouped together
- `mountain` convoys receive autonomous stall detection and skip logic for large-scale execution [OFFICIAL: https://docs.gastownhall.ai/glossary/]

Convoys are the operator-facing view of work; Beads are the agent-facing atoms.

---

## Agent Role Taxonomy

Gas Town defines a two-level hierarchy of specialized roles: [OFFICIAL: https://docs.gastownhall.ai/glossary/]

### Town-Level Roles (Cross-Rig)

**Mayor** — Chief-of-staff agent and primary human interface. The Mayor decomposes high-level goals into Beads, creates Convoys, slings work to agents, monitors progress, and presents consolidated status to the developer. Users talk to the Mayor, not directly to workers. The Mayor abstraction reduces cognitive load: instead of monitoring raw agent output, the developer manages a team through a Chief of Staff. [PRAC: https://steve-yegge.medium.com/gas-town-from-clown-show-to-v1-0-c239d9a407ec]

**Deacon** — Background supervisor daemon running continuous patrol cycles every ~2 minutes across all Rigs. Checks agent health, dispatches Dogs for maintenance tasks, and escalates issues that individual Witnesses can't resolve. The Deacon is the operational backbone that ensures nothing silently stalls. [PRAC: https://www.augusteo.com/blog/inside-gas-town]

**Dogs** — Maintenance agents dispatched by the Deacon for specific infrastructure tasks (cleanup, triage, health checks). Important distinction: *Dogs are NOT general workers.* They perform only infrastructure utilities. The "Boot the Dog" is a specialized Dog that heartbeats the Deacon every 5 minutes, creating an accountability chain. [OFFICIAL: https://docs.gastownhall.ai/glossary/]

### Rig-Level Roles (Per-Repository)

**Polecats** — The primary ephemeral worker agents. Each Polecat operates in an isolated git worktree (preventing interference with parallel workers), executes Beads, produces Merge Requests, and terminates. Despite being ephemeral sessions, Polecats retain persistent identity (stored in Dolt) so their work history, track record, and completed Convoys accumulate over time. Gas Town can run 20–30 Polecats in parallel. [OFFICIAL: https://docs.gastownhall.ai/]

**Crew** — Long-lived, named agents for persistent collaboration. Where Polecats handle discrete parallelizable tasks, Crew members maintain context across sessions and are managed by the human developer rather than by the Witness supervisor. Crew is for work requiring sustained engagement and human oversight. [OFFICIAL: https://docs.gastownhall.ai/glossary/]

**Witness** — Per-Rig lifecycle manager that supervises all Polecats and the Refinery within one Rig. Detects stuck agents, triggers recovery, manages session cleanup, and escalates to the Deacon. One Witness per Rig runs continuous patrol loops. [OFFICIAL: https://docs.gastownhall.ai/glossary/]

**Refinery** — Per-Rig merge queue processor. Uses Bors-style bisecting: batches all pending Merge Requests, runs tests once, and if the batch fails, recursively splits in half to isolate bad MRs. This requires O(log N) test runs instead of N sequential runs—for 8 MRs with one bad actor, 4 runs vs 8. [PRAC: https://www.augusteo.com/blog/inside-gas-town]

### Watcher Chain — Reliability Through Hierarchy

Reliability emerges from layered patrol loops, not from individual agent perfection:

```
Deterministic daemon (3-min heartbeat)
  ↓ wakes
Boot the Dog (every 5 min)
  ↓ wakes
Deacon (patrols town every 2 min)
  ↓ dispatches
Witnesses (per-Rig patrols)
  ↓ supervises
Polecats / Refinery (workers)
```

Each watcher is simpler and more reliable than what it watches. The deterministic daemon is the single failure point at the root; everything below re-checks state from scratch on each patrol rather than relying on event propagation. [PRAC: https://www.augusteo.com/blog/inside-gas-town]

---

## Supporting Systems

**Seance** — Allows agents to query previous sessions for context by reading `.events.jsonl` logs. An agent can "séance" its predecessor to recover earlier decisions without re-reading the entire codebase. [OFFICIAL: https://docs.gastownhall.ai/glossary/]

**Scheduler / Capacity Governor** — Configuration-driven dispatcher that prevents API rate limit exhaustion. `scheduler.max_polecats` sets the concurrency cap; when set, the daemon defers dispatch rather than spawning agents immediately. Default is direct dispatch (no cap). [OFFICIAL: https://docs.gastownhall.ai/]

**Escalation** — Severity-routed issue escalation (CRITICAL / HIGH / MEDIUM) routing blockers through the Deacon → Mayor → Overseer hierarchy. [OFFICIAL: https://docs.gastownhall.ai/]

**Wasteland** — Federated coordination network linking multiple Gas Towns through DoltHub for distributed work sharing and portable reputation tracking across organizations. [OFFICIAL: https://docs.gastownhall.ai/glossary/]

**Dashboard** — Web interface providing single-page visibility into agents, Convoys, Hooks, queues, issues, and escalations with browser-based command execution. [OFFICIAL: https://docs.gastownhall.ai/]

---

## Gas City: The SDK Layer

Gas City (https://github.com/gastownhall/gascity) was announced April 24, 2026 as the successor and generalization of Gas Town. Where Gas Town is an opinionated, hardwired multi-agent platform for coding, Gas City is an **orchestration-builder SDK** that deconstructs Gas Town's architecture into composable, declarative building blocks called **packs**. [OFFICIAL: https://github.com/gastownhall/gascity]

### What Changed

Gas Town organized around role taxonomy and filesystem layout (named directories encoding architecture). Gas City shifts to a "small primitive set plus configuration" model: [OFFICIAL: https://docs.gascityhall.com/getting-started/coming-from-gastown]

| Gas Town | Gas City |
|----------|----------|
| Role-specific directories | Configured agents from packs |
| Plugins | Orders (exec or formula) |
| Convoy runtime layer | Bead-backed beads + sling/formulas |
| Deacon watchdog logic | Controller and supervisor (infrastructure-owned) |
| Directory tree encoding architecture | `dir` for scope, `work_dir` for isolation |

The **Controller** in Gas City is a reconciliation loop—continuously comparing desired configuration state with actual running state and converging toward desired. It owns: session scaling, order evaluation, health checks, and garbage collection. This consolidates what Gas Town distributed across multiple role agents. [OFFICIAL: https://docs.gascityhall.com/getting-started/coming-from-gastown]

### Configuration Model

Three-file separation: [OFFICIAL: https://docs.gascityhall.com/getting-started/coming-from-gastown]
- `pack.toml` — Reusable shared behavior (agent definitions, prompts, skills, workflow templates)
- `city.toml` — Deployment choices and Rig configuration (which packs, which backends, concurrency settings)
- `.gc/` — Site-local bindings and runtime state

### Runtime Backends

Gas City supports multiple execution backends: tmux, subprocess, exec, ACP, and Kubernetes. This makes it deployable from local development to cloud-scale. [OFFICIAL: https://github.com/gastownhall/gascity]

### Relationship to Gas Town

Gas City ships a "fully functional Gas Town pack" that runs an exact replica of Gas Town. Existing Gas Town users can import their configuration and switch over seamlessly. Gas City extends the model beyond coding: the same orchestration engine can drive image moderation pipelines, compliance review workflows, ticket triage systems, or any arbitrary agent topology. [PRAC: https://steve-yegge.medium.com/welcome-to-gas-city-57f564bb3607]

Technology stack: Go 1.25+ (95.5%), TypeScript (2.8%), shell scripting. Dependencies: tmux, git, jq, Dolt (optional with file-based Beads fallback). [OFFICIAL: https://github.com/gastownhall/gascity]

---

## Design Principles and Critiques

### What Works

- **Identity-based architecture**: Agents have externally visible, persistent identities. Work is attributed to performers across their lifetime, enabling objective model comparison and performance tracking. [OFFICIAL: https://docs.gastownhall.ai/]
- **Git as single source of truth**: All work state, agent identity, and execution history live in version-controlled repositories. Rollback and audit are free. [PRAC: https://www.augusteo.com/blog/inside-gas-town]
- **The Mayor abstraction**: Reduces developer cognitive load from monitoring raw agent chatter to interacting with a Chief of Staff. Non-technical users have independently built tools using it. [PRAC: https://steve-yegge.medium.com/gas-town-from-clown-show-to-v1-0-c239d9a407ec]
- **Patrol-driven coordination**: Periodic health checks with restart capability are more reliable than event-driven wakeups. The watcher chain ensures nothing silently dies. [PRAC: https://www.augusteo.com/blog/inside-gas-town]

### Known Limitations

- **Planning becomes the bottleneck**: As agent velocity increases, design and planning becomes the rate-limiting factor. Agents quickly generate code that doesn't align with unstated intentions. Gas Town can outpace human architectural thinking. [PRAC: https://maggieappleton.com/gastown]
- **Ad hoc conceptual model**: Yegge has acknowledged that Gas Town itself suffers from poor upfront design—"just made stuff up as he went"—resulting in overlapping and ad hoc concepts. Gas City's explicit goal is to clean this up into coherent primitives. [PRAC: https://maggieappleton.com/gastown]
- **Requires significant infrastructure**: Go 1.25+, Dolt, tmux, git. Not a lightweight addition to an existing project. [OFFICIAL: https://github.com/gastownhall/gastown]
- **Claude Code alignment workaround**: The tmux send-keys technique for bypassing Claude's politeness training is a fragile hack, not a principled solution. [PRAC: https://www.augusteo.com/blog/inside-gas-town]
- **Target audience is Stage 7-8 developers**: Gas Town explicitly warns that developers not already managing 10+ parallel agents will find it counterproductive. It is not a beginner tool. [PRAC: https://reading.torqsoftware.com/notes/software/ai-ml/agentic-coding/2026-01-15-gas-town-multi-agent-orchestration-framework/]

---

## Summary: What Gas Town Is and Isn't

Gas Town is:
- A persistent workspace manager and coordination layer for multi-agent AI coding
- A pull-based dispatcher (GUPP) with git-backed durable work queues (Hooks + Beads)
- A hierarchical supervisor system (Mayor → Deacon → Witness → Polecat) with automatic recovery
- A work composition system (MEOW stack: Beads → Molecules → Formulas) for reproducible workflows
- An attribution and audit system tracking agent identity and performance across sessions

Gas Town is not:
- A general-purpose agent communication protocol (no message passing between arbitrary agents)
- An LLM provider or prompt management layer
- A lightweight library — it is a full operational platform requiring Dolt, tmux, and Go
- Optimized for human-in-the-loop workflows — it targets fully autonomous operation with operators in an oversight role

Gas City is Gas Town's SDK generalization: same primitives, declarative configuration via packs and `city.toml`, multiple runtime backends, and no hardcoded role taxonomy. Gas City is designed for building custom orchestrators, including non-coding agent topologies.

---

## Sources

- [OFFICIAL] Gas Town Documentation — https://docs.gastownhall.ai/
- [OFFICIAL] Gas Town Documentation: Glossary — https://docs.gastownhall.ai/glossary/
- [OFFICIAL] GitHub: gastownhall/gastown — https://github.com/gastownhall/gastown
- [OFFICIAL] GitHub: gastownhall/gascity — https://github.com/gastownhall/gascity
- [OFFICIAL] Gas City Documentation: Coming from Gas Town — https://docs.gascityhall.com/getting-started/coming-from-gastown
- [PRAC] Steve Yegge, "Welcome to Gas City" (Medium, April 2026) — https://steve-yegge.medium.com/welcome-to-gas-city-57f564bb3607
- [PRAC] Steve Yegge, "Gas Town: from Clown Show to v1.0" (Medium, April 2026) — https://steve-yegge.medium.com/gas-town-from-clown-show-to-v1-0-c239d9a407ec
- [PRAC] "Inside Gas Town" — https://www.augusteo.com/blog/inside-gas-town
- [PRAC] "Gas Town: Agent Patterns, Design Bottlenecks, and Vibecoding at Scale" (Maggie Appleton) — https://maggieappleton.com/gastown
- [PRAC] "Gas Town: Steve Yegge's Multi-Agent Orchestration Framework" (TorqSoftware Reading List, January 2026) — https://reading.torqsoftware.com/notes/software/ai-ml/agentic-coding/2026-01-15-gas-town-multi-agent-orchestration-framework/
- [PRAC] "Building with Gas Town: Multi-Agent AI Development Guide" (Better Stack) — https://betterstack.com/community/guides/ai/gas-town-multi-agent/
- [PRAC] "Gas Town: Orchestrating Claude Agents" (Nahornyi AI LAB) — https://nahornyi.ai/en/news/gastown-claude-code-multi-agent-workspace-manager
