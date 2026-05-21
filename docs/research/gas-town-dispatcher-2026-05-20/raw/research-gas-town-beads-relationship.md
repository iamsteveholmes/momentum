---
content_origin: claude-code-subagent
date: 2026-05-20
sub_question: "What is the Gas Town ↔ Beads relationship? Are they designed to work together? Shared data model, protocols, contracts?"
topic: "Gas Town as dispatcher/coordinator for Momentum agentic engineering"
---

# Gas Town ↔ Beads Relationship

## Overview: A Designed Two-Layer Stack

Gas Town and Beads are not independent tools that happen to be compatible — they are designed as two explicit layers of a single stack, created by the same author (Steve Yegge) and hosted under the same GitHub organization (gastownhall). The relationship is architectural: **Beads is the persistence and task-state layer; Gas Town is the orchestration and dispatch layer built on top of it.**

A key design invariant that Yegge states explicitly: "Beads is completely unaware of Gas Town." [OFFICIAL] This one-directional dependency is intentional. Beads does not import Gas Town code, does not know about mayors, polecats, or convoys. Gas Town, by contrast, depends on Beads as its core memory layer. The coupling flows only downward.

## Authorship and Organization

Both projects live under the `gastownhall` GitHub organization, which has 18 repositories as of May 2026. [OFFICIAL] The organization owner is Chris Sells, who manages the community infrastructure. Steve Yegge created the Gas Town concept and is the primary author of both Beads and Gas Town. A third project, Gas City (GasCity), was also released in April 2026 as a next-generation SDK that supersedes Gas Town while maintaining the same Beads foundation.

The full ecosystem, in ascending architectural order:

| Project | Role | Stars (approx.) |
|---|---|---|
| `gastownhall/beads` | Persistence / task-state layer | 23,900 |
| `gastownhall/gastown` | Orchestration / workspace manager | 15,500 |
| `gastownhall/gascity` | Next-gen SDK orchestration builder | 790 |
| `gastownhall/wasteland` | Federation protocol across Gas Towns | 72 |

[OFFICIAL — GitHub organization, as of 2026-05-20]

## The Beads Data Model

Beads is a distributed issue-tracking system designed for AI agents. Its storage backend is **Dolt** — a version-controlled SQL database with Git-like semantics (branch, merge, diff, push, pull at the database level). [OFFICIAL]

### A Bead's Core Fields

A bead is an atomic work unit stored as a row in Dolt. Core fields:

- `id` — Hash-based identifier (e.g., `bd-a1b2`, `gt-abc12`). Hash-derived to prevent merge collisions in multi-agent, multi-branch environments.
- `desc` / `title` — Task description
- `status` — `open`, `in_progress`, `done`
- `priority` — Numeric priority
- `assignee` — Agent claiming the work
- `blocked_by` — Dependency array linking to other bead IDs
- `discovered_from` — Audit trail link (for bug provenance tracking)

[OFFICIAL — gastownhall/beads ARCHITECTURE.md, gastownhall/beads quickstart docs]

### Storage Architecture

Beads supports two operational modes:

- **Embedded mode** (default): In-process Dolt database stored in `.beads/embeddeddolt/` — no external server, suitable for solo use, CI/CD, and containers.
- **Server mode**: Running `dolt sql-server` for multi-agent concurrent writes, with MySQL protocol on port 3307. Gas Town uses server mode with strict transaction discipline: `BEGIN / DOLT_COMMIT / COMMIT`. [PRAC — augusteo.com/blog/inside-gas-town]

An export format `.beads/issues.jsonl` exists but is explicitly described as "for viewers and interchange, not the source of truth." Dolt is the source of truth; JSONL is a derived artifact. [OFFICIAL — beads docs DOLT.md]

### Synchronization Protocol

Sync happens via native Dolt push/pull to compatible remotes: DoltHub, S3, GCS, filesystem, or custom git-compatible URLs. Hash-based IDs implement a deterministic conflict resolution policy: "same ID + different content = update, same ID + same content = skip." [OFFICIAL]

## The MEOW Stack: How Beads Compose Into Workflows

The most important Gas Town abstraction is the **MEOW stack** (Molecular Expression of Work). This is the formal protocol that bridges Beads (atomic tasks) to Gas Town's dispatch and orchestration layer. [OFFICIAL — docs.gastownhall.ai/glossary]

The hierarchy, bottom to top:

1. **Beads** — Atomic task units in Dolt. Individual issues with acceptance criteria, dependencies, status.
2. **Epics** — Hierarchical parent-child collections of Beads.
3. **Molecules** — Durable chained Bead workflows. A molecule is an instantiated workflow graph: an agent walks the chain one step at a time, claiming and closing each bead sequentially. Molecules survive agent restarts because state persists in Dolt, not in the agent's context window.
4. **Protomolecules** — Reusable workflow templates. Like a function definition vs. a function call.
5. **Formulas** — Declarative TOML-based source definitions that compile into protomolecules. "A formula gets cooked into a protomolecule, instantiated into a molecule, then executed by agents." [PRAC — augusteo.com/blog/inside-gas-town]

**Wisps** are ephemeral beads — generated by orchestration agents but never persisted to avoid repo noise. They represent in-flight decisions that don't need permanent history.

## Gas Town as Orchestration Layer: The Core Mechanisms

### The Hook / GUPP Protocol

Each persistent agent in Gas Town has a **hook** — a pinned bead in the Beads database that functions as that agent's work queue. The **GUPP** (Gas Town Universal Propulsion Principle) is the dispatch contract: "If there is work on your hook, you MUST run it." [OFFICIAL — docs.gastownhall.ai/glossary]

Work is assigned to an agent via the `gt sling` command, which "slings" a molecule onto the agent's hook. This is the fundamental dispatch primitive: sling → hook → GUPP → execution.

### Agent Identity in Beads

A critical design decision: **persistent agent identities are stored as beads**. Each Polecat (worker agent) has a permanent agent bead in the Beads database, along with a CV chain and accumulated work history. [PRAC — codex.danielvaughan.com]

This means the distinction in Gas Town is:
- **Agent** = a persistent row in the Beads database (survives indefinitely)
- **Session** = an ephemeral process that borrows the agent's identity while working

When a session crashes or exhausts its context window, it terminates. When work is slunged back onto the hook, a fresh session spawns — reads the agent's persistent identity from Beads, reads the molecule state from Beads, and resumes. No state lives in the process; all state lives in Dolt. [OFFICIAL — gastown README; PRAC — augusteo.com]

### Agent Integration Protocol

Gas Town integrates with agent providers (Claude Code, GitHub Copilot, etc.) through loose coupling via environment variables, not library imports. [OFFICIAL — gastown/docs/agent-provider-integration.md]

Key environment variables:
- `GT_ROLE` — agent's role in the Gas Town hierarchy
- `GT_RIG` — which repository (rig) the agent is working in
- `GT_ROOT` — town workspace root
- `BD_ACTOR` — the agent's identity in Beads

Agents receive work through three channels: beads (issue tracking), mail, and hook-based dispatching. The `gt prime` command injects context; `gt mail check --inject` delivers messages. [OFFICIAL]

### GasCity: Beads as a Selectable Storage Provider

In the newer Gas City SDK (April 2026), Beads' role is made even more explicit. GasCity treats Beads (`bd`) as its **default store provider** for "work tracking, formulas, molecules, waits, and mail." Users can substitute file-based storage via environment variable, but Beads is the production-grade default. [OFFICIAL — gastownhall/gascity README]

This confirms that the Beads/Gas Town pairing is not accidental — it is the intentional, documented production configuration.

## Beads Standalone Capability

Despite being tightly integrated with Gas Town and Gas City, Beads is designed to be **independently useful**. Key evidence:

1. The Beads FAQ and README do not mention Gas Town. The tool presents itself as a standalone issue tracker with no Gas Town dependency. [OFFICIAL — beads/docs/FAQ.md]
2. Yegge explicitly states: "You can use Beads by itself and get a vastly improved agentic experience, no matter which coding agent you're using." [OFFICIAL — gas-town-from-clown-show-to-v1-0]
3. Practitioners confirm independently adopting Beads after abandoning Gas Town. At least one blogger continued using Beads as their primary task tracker after discontinuing Gas Town use. [PRAC — medium.com/long-context]
4. Beads works with "anything and everything, as long as it's roughly as smart as Claude Sonnet 3.5 was." [OFFICIAL] This is explicitly contrasted with Gas Town, which only supports a handful of specific agent providers.

The standalone path installs Beads system-wide (not as a project dependency), uses embedded Dolt mode, and requires no Gas Town infrastructure at all.

## What Contracts Exist Between Them

The integration between Beads and Gas Town is not a formal API contract in the traditional sense (no OpenAPI spec, no gRPC definition). Instead, the contract is:

1. **Schema contract**: Gas Town reads/writes specific Dolt table schemas in the `.beads/` database — hooks, agents, molecules, wisps, CVs. Gas Town extends the base bead schema with Gas Town-specific bead types (hook beads, agent beads, role beads).
2. **ID contract**: Bead IDs use a prefix + 5-character alphanumeric format (e.g., `gt-abc12`, `hq-x7k2m`). The prefix encodes which rig or context the bead belongs to.
3. **Transaction contract**: All multi-agent writes use `BEGIN / DOLT_COMMIT / COMMIT` with isolation discipline to prevent write conflicts.
4. **GUPP behavioral contract**: Agents are expected to check their hook and execute any work present. This is a behavioral contract enforced by Gas Town agent prompts, not a technical API.
5. **Environment variable contract**: `BD_ACTOR` links an active session to its persistent agent identity in Beads.

[OFFICIAL — gastown README, agent-provider-integration.md; PRAC — augusteo.com]

## Nondeterministic Idempotence (NDI): The Runtime Model

A key philosophical contract between the layers: Gas Town does not attempt deterministic replay of LLM decisions (impossible given non-determinism). Instead it uses **NDI** — each bead defines well-specified acceptance criteria. A session claims a step, attempts to close it, and if it crashes, a future session re-reads the molecule state and retries. "The path is whatever the agent decides. The destination is whatever the bead says." [PRAC — augusteo.com]

This means Beads encodes *what must be true when done*, not *how to do it*. Gas Town provides the execution harness that keeps retrying until the acceptance criterion is met.

## Ecosystem Trajectory

The Gas Town → Gas City evolution (April 2026) preserves the Beads foundation while improving the orchestration layer. Gas City is described as "a drop-in replacement for Gas Town, and can import all your rigs and beads." [OFFICIAL — steve-yegge.medium.com/welcome-to-gas-city] Gas Town will continue to be maintained for existing users, but Gas City is the forward path for new projects.

Both Gas Town and Gas City reached v1.0 in April 2026, signaling production stability. [OFFICIAL — steve-yegge.medium.com/gas-town-from-clown-show-to-v1-0]

## Summary of the Relationship

| Dimension | Beads | Gas Town / Gas City |
|---|---|---|
| Layer | Persistence + task-state | Orchestration + dispatch |
| Awareness | Unaware of Gas Town | Depends on Beads |
| Standalone | Yes, fully | No, requires Beads |
| Storage | Dolt (embedded or server) | Reads/writes Beads' Dolt |
| Work unit | Individual bead | Molecules (chains of beads) |
| Agent identity | Stored as a bead row | Managed via BD_ACTOR env var |
| Dispatch | `bd ready` (what's unblocked) | `gt sling` (assign to hook) |
| Crash recovery | State survives in Dolt | Re-reads molecule from Dolt |
| Designed together | Yes | Yes |
| Same author | Yes (Steve Yegge) | Yes |

## Sources

- [OFFICIAL] gastownhall GitHub Organization — https://github.com/gastownhall
- [OFFICIAL] gastownhall/beads — https://github.com/gastownhall/beads
- [OFFICIAL] gastownhall/gastown — https://github.com/gastownhall/gastown
- [OFFICIAL] gastownhall/gascity — https://github.com/gastownhall/gascity
- [OFFICIAL] Gas Town Glossary — https://docs.gastownhall.ai/glossary/
- [OFFICIAL] Beads Architecture Docs — https://gastownhall.github.io/beads/architecture
- [OFFICIAL] Beads Quickstart — https://gastownhall.github.io/beads/getting-started/quickstart
- [OFFICIAL] gastown/docs/agent-provider-integration.md — https://github.com/gastownhall/gastown/blob/main/docs/agent-provider-integration.md
- [OFFICIAL] Steve Yegge, "Gas Town: from Clown Show to v1.0", Apr 2026 — https://steve-yegge.medium.com/gas-town-from-clown-show-to-v1-0-c239d9a407ec
- [OFFICIAL] Steve Yegge, "Welcome to Gas Town", Jan 2026 — https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04
- [OFFICIAL] Steve Yegge, "Welcome to Gas City", Apr 2026 — https://steve-yegge.medium.com/welcome-to-gas-city-57f564bb3607
- [PRAC] augusteo.com, "Inside Gas Town" — https://www.augusteo.com/blog/inside-gas-town
- [PRAC] paddo.dev, "GasTown and the Two Kinds of Multi-Agent" — https://paddo.dev/blog/gastown-two-kinds-of-multi-agent/
- [PRAC] Maggie Appleton, "Gas Town's Agent Patterns" — https://maggieappleton.com/gastown
- [PRAC] Better Stack, "Building with Gas Town" — https://betterstack.com/community/guides/ai/gas-town-multi-agent/
- [PRAC] Starlog, "Beads: A Version-Controlled Task Graph" — https://starlog.is/articles/ai-dev-tools/gastownhall-beads/
- [PRAC] decisioncrafters.com, "Beads: AI Agent Memory System" — https://www.decisioncrafters.com/beads-ai-agent-memory-system/
- [PRAC] VirtusLab, "Beads - Give AI Memory" — https://virtuslab.com/blog/ai/beads-give-ai-memory
- [PRAC] Medium/Long Context, "Gas Town: The Good, The Bad, The Ugly", Feb 2026 — https://medium.com/long-context/gas-town-the-good-the-bad-the-ugly-ed3643b2bb50
- [PRAC] Justin Abrahms, "Wrapping My Head Around Gas Town", Jan 2026 — https://justin.abrah.ms/blog/2026-01-05-wrapping-my-head-around-gas-town.html
- [PRAC] codex.danielvaughan.com, "Gas Town: Multi-Agent Factory", Apr 2026 — https://codex.danielvaughan.com/2026/04/08/gas-town-multi-agent-factory/
- [PRAC] reading.torqsoftware.com, "Gas Town: Multi-Agent Orchestration Framework", Jan 2026 — https://reading.torqsoftware.com/notes/software/ai-ml/agentic-coding/2026-01-15-gas-town-multi-agent-orchestration-framework/
- [PRAC] embracingenigmas.substack.com, "Exploring Gas Town" — https://embracingenigmas.substack.com/p/exploring-gas-town
- [PRAC] johncodes.com, "A Glimpse into the Future", Jan 2026 — https://johncodes.com/archive/2026/01-16-a-glimpse-into-the-future/
- [PRAC] Software Engineering Daily, "Gas Town, Beads, and the Rise of Agentic Development", Feb 2026 — https://softwareengineeringdaily.com/2026/02/12/gas-town-beads-and-the-rise-of-agentic-development-with-steve-yegge/
