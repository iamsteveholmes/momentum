---
content_origin: claude-code-subagent
date: 2026-05-20
sub_question: "How does Gas Town's coordination model compare to Momentum's orchestrator-subagent pattern? Tradeoffs?"
topic: "Gas Town as dispatcher/coordinator for Momentum agentic engineering"
---

# Gas Town Coordination Model vs. Momentum's Orchestrator-Subagent Pattern

## Overview

Gas Town (released January 2026 by Steve Yegge) and Momentum occupy very different positions in the agent orchestration design space. Gas Town is a **persistent, infrastructure-heavy, process-model** orchestrator designed to coordinate 20–30 parallel AI agents on production codebases. Momentum is a **session-scoped, file-backed, fan-out** orchestrator where one human-triggered Claude Code session spawns subagents and dissolves. Understanding the tradeoffs requires examining each system's persistence model, coordination mechanism, infrastructure requirements, failure recovery posture, and scaling ceiling.

## Gas Town's Coordination Model

### Persistent, Daemon-Based Architecture

Gas Town is fundamentally a **persistent system**. It runs as a daemon ensemble across sessions rather than as an ephemeral per-invocation process. The core components that remain running between agent sessions include:

- **Deacon**: A background health-monitoring daemon that runs continuous patrol loops
- **Witness**: A per-rig (per-repository) supervisor that monitors ephemeral worker health
- **Boot**: A watchdog that checks Deacon every five minutes, anchoring the whole accountability chain

[OFFICIAL] The Mayor (global coordinator), Deacon (daemon supervisor), Witness (per-rig monitor), and Refinery (merge queue processor) together form a "control plane" that persists across any individual agent session. Polecats — the ephemeral workers — come and go, but the coordination infrastructure does not. [[Gas Town docs](https://docs.gastownhall.ai/)]

This is categorically different from Momentum. When a Momentum sprint-dev session ends, the orchestrator ceases to exist. There is no daemon watching for newly completed stories or unblocking dependent work. The next sprint requires a human to manually re-invoke the workflow.

### The GUPP Principle: Pull-Based Execution

Gas Town's key scheduling innovation is GUPP — the **Gas Town Universal Propulsion Principle**: *"If there is work on your hook, YOU MUST RUN IT."* [[torqsoftware reading notes](https://reading.torqsoftware.com/notes/software/ai-ml/agentic-coding/2026-01-15-gas-town-multi-agent-orchestration-framework/)]

This is a **pull-based** execution model. Agents do not wait for a central orchestrator to dispatch them — they check their own hook (a Bead-backed work queue), find assigned work, and execute immediately. This eliminates the failure mode where a restarted agent sits idle because no orchestrator is alive to give it new instructions.

Momentum uses a **push-based** fan-out model: the orchestrator session spawns subagents via the `Agent` tool, each subagent runs its story, and returns a result to the parent. If the orchestrator session crashes mid-sprint, all in-flight work context is lost. There is no mechanism for surviving agents to continue autonomously or for a restarted session to pick up where subagents left off.

### State Persistence: Git-Backed Beads vs. File-Backed Stories

Gas Town's persistence layer is **Beads** — atomic work units stored in Dolt (a Git-native SQL database with column-level merge semantics). The MEOW stack layers persistence primitives:

- **Beads**: Atomic issues with identity, history, CV chain
- **Molecules**: Multi-step workflow graphs compiled from Formula TOML definitions, frozen in Git
- **Gates**: Async coordination primitives (GitHub run status, PR state, timer, human approval, mail)
- **Wisps**: Ephemeral Beads destroyed after a single use

[OFFICIAL] "Work backed by Git; auditable history, resumable state" — when an agent crashes mid-molecule, its successor session reads the last committed Bead state and resumes from the checkpoint. The path of execution may vary (it is nondeterministic), but convergence on the goal is guaranteed by persistent workflow definitions and explicit acceptance criteria. [[Gas City SDK docs](https://github.com/gastownhall/gascity)]

Momentum's persistence is entirely **file-based**: story markdown files in `.momentum/stories/`, sprint indexes, and epic files. This is sufficient for session-to-session continuity but carries no intra-session crash recovery. If a subagent's worktree is lost or a session context limit is reached, the orchestrator must re-read file state from scratch on the next human invocation. Unmerged worktree work can be recovered (git branches persist), but the orchestrator has no automatic mechanism to resume from mid-story state.

### Coordination Mechanism: Process Model vs. Conversational Fan-Out

The deepest architectural difference is in how coordination decisions are made.

**Gas Town** uses a **deterministic process model**: hooks and state machines route work. The Mayor analyzes goals, creates Beads, and "slings" them to Polecats via `gt sling`. Polecats pull work from their hooks autonomously. The Refinery manages the merge queue with sequential rebase semantics to prevent parallel write collisions. Agents coordinate through Dolt Beads and async mail — not through LLM routing decisions in a conversation. [[w-gc-004 framework survey](https://gist.github.com/tmchow/f539adef1d11974eb51478a32a72ff68)]

**Momentum** uses **LLM-mediated fan-out**: the orchestrator skill (e.g., sprint-dev) makes in-context decisions about which stories to activate, spawns `Agent` tool calls in parallel, interprets results, and decides next steps. All routing intelligence lives in the orchestrator's context window during that session.

The implication: Gas Town's coordination survives orchestrator crashes because hooks and Beads encode the routing state externally. Momentum's coordination dissolves with the session.

### Role Taxonomy and Agent Lifecycle

Gas Town defines eight operational roles with distinct lifecycles:

| Role | Lifecycle | Function |
|---|---|---|
| Mayor | Persistent (daemon) | Global work dispatcher |
| Deacon | Persistent (daemon) | Health monitor, patrol loops |
| Boot | Persistent (watchdog) | Checks Deacon every 5 min |
| Witness | Persistent (per rig) | Monitors Polecats |
| Refinery | Persistent (per rig) | Merge queue management |
| Crew | Persistent (human-managed) | Named long-term agents |
| Polecats | Ephemeral | Worker agents per task |
| Dogs | Ephemeral | Infrastructure maintenance |

[PRAC] Each Polecat maintains a permanent Agent Bead — persistent identity with CV chain and capability history — even though its session is ephemeral. This separates *agent identity* (durable) from *agent session* (transient). [[Codex blog, Daniel Vaughan, April 2026](https://codex.danielvaughan.com/2026/04/08/gas-town-multi-agent-factory/)]

Momentum has no equivalent concept. Subagents spawned by `Agent` tool calls are fully anonymous and stateless. Each sprint-dev session spawns fresh subagents with no memory of prior executions. The "identity" of a story's implementer is implicit in git blame, not in any persistent agent record.

## Momentum's Current Pattern: Strengths and Limits

### What Makes Momentum's Pattern Work

Momentum's single-session orchestrator with fan-out subagents is effective precisely because of what it *doesn't* require:

- **Zero infrastructure**: No daemons, no Dolt database, no tmux session management, no Go toolchain
- **No operational cost at rest**: Nothing runs between sprints — no daemon consuming resources or API credits
- **Simple mental model**: One session, one sprint, one orchestrator reading from files
- **Human-paced execution**: The human controls when work starts; context can be re-established intentionally

These advantages compound at Momentum's scale. A solo developer running 4–8 stories per sprint with 2–4 subagents per story does not need 20-30 parallel agents with health monitoring infrastructure.

### Where Momentum's Pattern Breaks Down

**Context limit pressure**: Long sprints with many stories exhaust the orchestrator's context window. The orchestrator must re-read file state to continue, but that re-read consumes context that could be used for coordination decisions. Gas Town externalizes all task state into Beads precisely to avoid this.

**Human availability gating**: Every sprint requires a human invocation. Overnight unattended execution — a capability Gas Town explicitly targets — is impossible without a persistent orchestrator.

**No crash recovery**: If the sprint-dev session crashes mid-sprint (context limit, network error, process kill), stories that were in-flight in subagent worktrees must be manually recovered. The orchestrator has no way to resume from mid-story state without human intervention.

**No event-driven triggers**: Momentum cannot react to external events (PR merged, CI passed, test failed) without human polling. Gas Town's Gate primitives explicitly handle `gh:run`, `gh:pr`, timer, human, and mail signals — agents can park on a Gate and resume when the condition clears.

**Sequential sprint activation**: Stories are activated in dependency order, but the orchestrator must track this. Gas Town's Molecule graphs encode dependency order in the workflow definition itself; Polecats self-sequence based on Bead dependencies without orchestrator intervention.

## Infrastructure and Operational Cost Comparison

### Gas Town's Infrastructure Requirements

[OFFICIAL] Running Gas Town requires: tmux 3.0+, Git 2.25+, Go ≥1.25 (corrected from 1.23 — see research-gas-city-architecture.md for authoritative version floor), Beads 0.44.0+ (or Dolt for full cell-level merge semantics), and optionally additional AI provider CLIs. [[Gas City SDK docs](https://github.com/gastownhall/gascity)]

Beyond toolchain, the operational costs are substantial:

- **API credits**: $100/hour at full capacity (12–30 parallel Claude Code instances). Yegge reportedly exhausted three Claude Code accounts during Gas Town's launch week. [[Cloud Native Now](https://cloudnativenow.com/features/gas-town-what-kubernetes-for-ai-coding-agents-actually-looks-like/)]
- **Human oversight**: "Constant steering" rather than fully autonomous operation — DoltHub reported "auto-merging failing tests into main" and a "murderous rampaging Deacon" deleting code unpredictably during early use. [[paddo.dev analysis](https://paddo.dev/blog/gastown-two-kinds-of-multi-agent/)]
- **Oversight fatigue**: Reviewing dozens of parallel Polecat pull requests creates significant cognitive load
- **Setup complexity**: Named agents, Role Beads, Formulas, Molecules — significant configuration surface

Gas Town explicitly targets Stage 7–8 developers already comfortable with 10+ parallel agents daily. Yegge notes: "You won't like Gas Town if you ever have to think about where money comes from." [[torqsoftware reading notes](https://reading.torqsoftware.com/notes/software/ai-ml/agentic-coding/2026-01-15-gas-town-multi-agent-orchestration-framework/)]

### Momentum's Infrastructure Requirements

Momentum runs entirely within a Claude Code session with no additional infrastructure:

- Claude Code (already required for Momentum)
- Git (already required)
- Filesystem for story/sprint files
- No daemons, no database, no additional CLI tools

At rest, Momentum costs nothing. During a sprint, it runs 2–8 subagents concurrently — orders of magnitude below Gas Town's operational cost.

## Failure Recovery Model Comparison

| Scenario | Gas Town | Momentum |
|---|---|---|
| Agent session crash | GUPP + Beads: next session resumes from last Bead checkpoint | Context lost; orchestrator must re-read files from scratch on next human invocation |
| Orchestrator crash | Daemon ensemble (Deacon/Witness/Boot) detects and escalates; GUPP ensures workers self-continue | Sprint halted; human must restart sprint-dev |
| Mid-task failure | Molecule gates park on failure condition; Witness detects stuck Polecats | Subagent returns failure to orchestrator; orchestrator decides whether to retry in-session |
| Context window exhaustion | `/handoff` command transfers Bead state to fresh session; work resumes | Orchestrator session ends; human must restart; partially-completed worktrees survive in git |
| Merge conflict | Refinery manages sequential merge queue with Dolt cell-level conflict resolution | Subagents merge sequentially in dependency order; conflicts surface as git errors to orchestrator |

[PRAC] Gas Town's failure recovery is described as "nondeterministic idempotence" — the execution path varies on retry but convergence is guaranteed by persistent workflow definitions. This is contrasted with Temporal's deterministic replay model. [[Cloud Native Now](https://cloudnativenow.com/features/gas-town-what-kubernetes-for-ai-coding-agents-actually-looks-like/)]

## Scaling Ceiling Comparison

Gas Town is designed to scale to 20–30 parallel agents and explicitly targets multi-repository, multi-team ("Wasteland") federation where thousands of Gas Towns can link for distributed multi-agent coordination. [[Codex blog, Daniel Vaughan, April 2026](https://codex.danielvaughan.com/2026/04/08/gas-town-multi-agent-factory/)]

The framework survey notes: "Gas Town scales to 20-30 parallel agents while conversation-based frameworks struggle beyond 3-5 — every additional agent in a conversation multiplies token cost and routing complexity, while every additional agent in Gas Town is just another independent process with its own worktree." [[w-gc-004 framework survey](https://gist.github.com/tmchow/f539adef1d11974eb51478a32a72ff68)]

Momentum's practical ceiling is lower — determined by the orchestrator's context window. A session running 8 parallel subagents with rich story context is near the practical limit before routing decisions degrade. Gas Town externalizes all routing state, so adding a 25th Polecat has zero impact on coordination overhead.

## Where Gas Town Sits in the Broader Landscape

The framework survey contrasts Gas Town against all major orchestration approaches along one fundamental axis: **conversation as control plane vs. process as control plane**. [[w-gc-004 framework survey](https://gist.github.com/tmchow/f539adef1d11974eb51478a32a72ff68)]

| Framework | Control Plane | Persistence | Parallelism Ceiling |
|---|---|---|---|
| CrewAI | Conversational (LLM routing) | Session-ephemeral | 3–5 agents |
| LangGraph | Conversational (typed state graph) | Checkpoint-based | 3–5 agents |
| AutoGen / MS Agent Framework | Conversational (actor-based) | Session or checkpoint | 3–5 agents |
| OpenAI Agents SDK | Conversational (handoff-based) | Session-scoped | 3–5 agents |
| Google ADK | Conversational (tree hierarchy) | Session state | 3–5 agents |
| **Gas Town** | **Process model (hooks, GUPP, state machines)** | **Git + Dolt; crash-surviving** | **20–30+ agents** |
| **Momentum** | **Conversational (LLM fan-out)** | **File-backed, session-scoped** | **~4–8 agents** |

Momentum sits in the same category as CrewAI and LangGraph — conversational fan-out — but with a lighter coordination model (no typed state graph, no built-in checkpointing, pure file persistence). Its simplicity is an advantage at its target scale; it becomes a liability at Gas Town's target scale.

Gas Town is described as "Kubernetes mated with Temporal" — borrowing container scheduling concepts for agent management and workflow durability patterns for crash resilience. [[torqsoftware reading notes](https://reading.torqsoftware.com/notes/software/ai-ml/agentic-coding/2026-01-15-gas-town-multi-agent-orchestration-framework/)]

## Concrete Tradeoff Summary

### What Gas Town Offers That Momentum Lacks

1. **Session-independent execution**: Agents run and continue without a human present
2. **Crash recovery**: GUPP + Beads allow mid-molecule resumption after any failure
3. **Event-driven gates**: Agents can park on CI status, PR merge, timer, or human approval
4. **Scaling beyond context limits**: Process model decouples coordination overhead from agent count
5. **Persistent agent identity**: Polecats accumulate capability history across sprints

### What Momentum Offers That Gas Town Lacks

1. **Zero infrastructure**: Works with only Claude Code and git — no daemons, no Dolt, no Go toolchain
2. **No operational cost at rest**: Nothing runs or bills between sprints
3. **Simple mental model**: One human, one session, one sprint
4. **Lower cognitive overhead**: No fleet management, no Bead taxonomy, no Formula TOML authoring
5. **Appropriate scale**: At 4–8 parallel subagents, infrastructure complexity of Gas Town adds no value

### The Fundamental Design Mismatch

Adopting Gas Town as a Momentum dispatcher is not a drop-in upgrade — it would require accepting Gas Town's entire infrastructure stack (Dolt, tmux, Go toolchain, daemon management, Bead authoring conventions) in exchange for capabilities that only matter at 15+ parallel agents running unattended. At Momentum's current solo-developer scale, this infrastructure cost exceeds the benefit.

The more tractable question is whether **specific Gas Town patterns** — GUPP-style pull-based story hooks, Molecule-style dependency graphs in external state, or Gate-style async CI coordination — could be borrowed and implemented at Momentum's lower infrastructure floor. Gas City (the SDK extracting Gas Town's primitives) is the project attempting exactly this decomposition. [OFFICIAL] [[Gas City SDK docs](https://github.com/gastownhall/gascity)]

## Sources

- [Gas Town Official Documentation — docs.gastownhall.ai](https://docs.gastownhall.ai/)
- [Gas City SDK — github.com/gastownhall/gascity](https://github.com/gastownhall/gascity)
- [Gas Town: Steve Yegge's Multi-Agent Orchestration Framework — torqsoftware reading list](https://reading.torqsoftware.com/notes/software/ai-ml/agentic-coding/2026-01-15-gas-town-multi-agent-orchestration-framework/)
- [GasTown and the Two Kinds of Multi-Agent — paddo.dev](https://paddo.dev/blog/gastown-two-kinds-of-multi-agent/)
- [Gas Town: What Kubernetes for AI Coding Agents Actually Looks Like — Cloud Native Now](https://cloudnativenow.com/features/gas-town-what-kubernetes-for-ai-coding-agents-actually-looks-like/)
- [Gas Town vs Swarm-Tools: Multi-Agent AI Orchestration Compared — GitHub Gist, John Lindquist](https://gist.github.com/johnlindquist/4174127de90e1734d58fce64c6b52b62)
- [w-gc-004: Survey of Existing Agent Orchestration Frameworks — GitHub Gist, tmchow](https://gist.github.com/tmchow/f539adef1d11974eb51478a32a72ff68)
- [Building with Gas Town: Multi-Agent AI Development Guide — Better Stack Community](https://betterstack.com/community/guides/ai/gas-town-multi-agent/)
- [Gas Town: Steve Yegge's Multi-Agent Factory and What It Means for Codex CLI — Codex Blog, Daniel Vaughan, April 2026](https://codex.danielvaughan.com/2026/04/08/gas-town-multi-agent-factory/)
- [GitHub — gastownhall/gastown: Gas Town multi-agent workspace manager](https://github.com/gastownhall/gastown)
