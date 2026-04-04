---
content_origin: claude-code-subagent
date: 2026-04-04
sub_question: "How does Air's multi-agent task dispatch compare to Claude Code's subagent/skill composition model?"
topic: "JetBrains Air"
---

## Executive Summary

JetBrains Air and Claude Code take fundamentally different approaches to multi-agent orchestration. Air is an **agent-agnostic task dispatcher** — a workbench that routes independent tasks to heterogeneous agent backends (Codex, Claude Agent, Gemini CLI, Junie) and manages their execution environments. Claude Code is a **single-model agent framework** with deep composition primitives (subagents, skills, agent teams) that enable coordinated multi-agent workflows within the Claude ecosystem. Air orchestrates *between* agents; Claude Code orchestrates *within* an agent hierarchy. The two systems are complementary rather than competitive: Air can host Claude Agent as one of its backends, while Claude Code's internal composition model has no equivalent in Air.

## Air's Task Dispatch Architecture

### The Task as Atomic Unit

Air's core abstraction is the **task** — a user-defined unit of work described in natural language and assigned to a single agent. Each task has a lifecycle: Running, Input Required, Done, or Canceled. Tasks completed before the current day are archived automatically. **[OFFICIAL]** ([Quick start | JetBrains Air Documentation](https://www.jetbrains.com/help/air/quick-start-with-air.html))

The user selects which agent backend executes each task — this is a per-task choice, not a global setting. Air currently ships with four built-in backends: **[OFFICIAL]** ([Supported agents | JetBrains Air Documentation](https://www.jetbrains.com/help/air/supported-agents.html))

| Agent | Provider | Model Access |
|:------|:---------|:-------------|
| Claude Agent | Anthropic | Claude models via Anthropic Console billing |
| OpenAI Codex | OpenAI | GPT 5.1-5.3 Codex variants |
| Gemini CLI | Google | Gemini 2.5-3.1 Pro/Flash variants |
| Junie | JetBrains | Aggregated access to Gemini, GPT, Grok, and Claude |

### Execution Environments

Air provides three isolation modes for task execution: **[OFFICIAL]** ([Air launch blog](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/))

1. **Local workspace** — Agent runs directly in the project directory. Fastest startup, no isolation. Changes apply immediately to the working tree.
2. **Git worktree** — Agent operates on a separate branch via `git worktree`. Provides branch-level isolation while sharing the local environment. Dependencies may need reinstallation.
3. **Docker container** — Complete isolation. All edits, commands, and dependencies stay inside the container. Nothing touches the local workspace or system environment.

A future cloud execution mode is planned but not yet available.

### Concurrency Model

Air supports running **multiple tasks asynchronously** — e.g., one agent adds tests while another fixes a bug while the developer works on a feature manually. However, the UI is single-task-at-a-time: you see one agent session at a time and receive notifications when another needs attention. **[OFFICIAL]** ([Air launch blog](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/))

This is **concurrent but not coordinated** — agents do not communicate with each other, share context, or know about each other's tasks. Each task is an independent session. There is no inter-agent messaging, shared task list, or orchestration layer within Air itself.

### Review and Merge Workflow

When an agent completes a task, Air presents changes in a diff panel (unified or side-by-side). The developer can add inline comments "directly in the diff panel, similar to a regular code review," and these comments feed back into the agent's chat for iterative refinement. After approval, the developer commits selected files and pushes to a remote. **[OFFICIAL]** ([Quick start | JetBrains Air Documentation](https://www.jetbrains.com/help/air/quick-start-with-air.html))

### Agent Client Protocol (ACP)

Air's extensibility comes from ACP, a vendor-neutral protocol co-sponsored by JetBrains and Zed. ACP standardizes communication between code editors/IDEs and coding agents: **[OFFICIAL]** ([Agent Client Protocol](https://agentclientprotocol.com/))

- **Local transport**: Agents run as sub-processes, communicating via JSON-RPC over stdio
- **Remote transport**: HTTP/WebSocket (work in progress)
- **MCP relationship**: ACP reuses MCP's JSON representations where possible and can transport MCP over ACP channels ("MCP-over-ACP"), meaning ACP is a superset rather than a competitor
- **Protocol features**: Prompt turns, tool calls, slash commands, session management (create, resume, fork, close), filesystem access, terminal execution, content blocks, agent planning communication, and extension points

ACP enables any compliant agent to plug into Air. The ACP Agent Registry (live since January 2026, co-launched with Zed) provides a directory of verified compatible agents. **[OFFICIAL]** ([ACP Agent Registry blog](https://blog.jetbrains.com/ai/2026/01/acp-agent-registry/))

## Claude Code's Composition Model

Claude Code provides three distinct composition primitives, each operating at a different level of coordination.

### Skills: Declarative Capability Extension

Skills are `SKILL.md` files that extend Claude with specialized capabilities. They are: **[OFFICIAL]** ([Agent Skills in the SDK](https://platform.claude.com/docs/en/agent-sdk/skills))

- **Filesystem artifacts** in `.claude/skills/` directories (project or user scope)
- **Auto-discovered** at startup; full content loaded when triggered
- **Model-invoked** — Claude autonomously chooses when to use them based on context matching against the skill's `description` field
- **Composable** — skills can restrict tools, inject context, override the model, and hook into lifecycle events

Skills are the primary mechanism for encoding domain knowledge and workflow procedures. In the Momentum practice, for example, skills encode sprint workflows, story creation procedures, validation loops, and editorial review processes — each as a self-contained capability Claude can invoke. Skills cannot be defined programmatically in the SDK; they must exist as filesystem artifacts.

### Subagents: Context-Isolated Delegation

Subagents are separate agent instances spawned by the main agent to handle focused subtasks. Key characteristics: **[OFFICIAL]** ([Create custom subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents), [Subagents in the SDK](https://platform.claude.com/docs/en/agent-sdk/subagents))

- **Context isolation** — each subagent runs in its own fresh conversation. Only the final message returns to the parent. Intermediate tool calls and file reads do not pollute the parent's context window.
- **Tool restrictions** — subagents can be limited to specific tool subsets (e.g., read-only analysis with `Read, Grep, Glob` only)
- **Model routing** — each subagent can target a different model (`opus`, `sonnet`, `haiku`, `inherit`)
- **Parallel execution** — multiple subagents run concurrently (e.g., style-checker + security-scanner + test-coverage simultaneously)
- **Resumable** — subagent transcripts persist independently and can be resumed via session ID and agent ID
- **No nesting** — subagents cannot spawn their own subagents (no recursive delegation)
- **Defined via filesystem or SDK** — `.claude/agents/` markdown files or programmatic `AgentDefinition` objects

Subagents are the unit of parallelism within a single session. The parent-child relationship is strictly hierarchical: subagents report results back to the parent and cannot communicate laterally.

### Agent Teams: Multi-Session Coordination

Agent teams (experimental, requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`) coordinate multiple independent Claude Code instances: **[OFFICIAL]** ([Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams))

- **Architecture**: One lead session + N teammate sessions, each with its own 1M-token context window
- **Shared task list**: Tasks have states (pending, in-progress, completed) with dependency tracking. Teammates self-claim unblocked tasks via file-locking to prevent race conditions.
- **Peer-to-peer messaging**: Teammates communicate directly via a mailbox system — not just with the lead, but with each other. This enables debate, hypothesis testing, and collaborative convergence.
- **Git worktree isolation**: Each teammate operates in its own worktree, preventing file conflicts
- **Plan approval gates**: Teammates can be required to plan before implementing; the lead reviews and approves/rejects plans
- **Quality hooks**: `TeammateIdle`, `TaskCreated`, and `TaskCompleted` hooks enforce quality gates
- **Display modes**: In-process (single terminal, cycle with Shift+Down) or split-pane (tmux/iTerm2)
- **Subagent definitions as roles**: Teammates can be spawned using subagent type definitions, inheriting tool restrictions and model settings

Agent teams have been demonstrated at significant scale — a 16-agent team produced a 100,000-line Rust C compiler across ~2,000 sessions. **[OFFICIAL]** ([Building a C compiler with parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler))

## Comparative Analysis

### Orchestration Topology

| Dimension | Air | Claude Code |
|:----------|:----|:------------|
| **Unit of dispatch** | Task (1 agent, 1 session) | Subagent call / teammate spawn / skill invocation |
| **Agent heterogeneity** | Yes — Codex, Claude, Gemini, Junie, any ACP agent | No — Claude models only (but multiple tiers: Opus, Sonnet, Haiku) |
| **Inter-agent communication** | None — tasks are fully independent | Subagents: parent-child only. Teams: peer-to-peer mailbox |
| **Shared state** | None between tasks | Teams: shared task list with dependencies. Subagents: none |
| **Coordination overhead** | Zero (no coordination exists) | Teams: significant token cost. Subagents: minimal |
| **Nesting depth** | Flat (1 level) | Skills > subagents (2 levels). Teams cannot nest. |
| **Execution isolation** | Local / worktree / Docker | Subagents: same process. Teams: worktree per teammate |

### What Air Can Orchestrate That Claude Code Cannot

1. **Heterogeneous agent backends in a single workspace.** Air can run a Codex task, a Gemini task, and a Claude task concurrently on the same codebase. Claude Code is locked to Claude models. If a particular task benefits from a specific model's strengths (e.g., Codex for certain code generation patterns, Gemini for multimodal reasoning), Air can route accordingly. **[OFFICIAL]** ([Supported agents | JetBrains Air Documentation](https://www.jetbrains.com/help/air/supported-agents.html))

2. **Docker-based full-system isolation.** Air's Docker execution mode provides complete sandboxing — the agent cannot affect the host system at all. Claude Code's worktree isolation prevents file conflicts but does not sandbox system-level side effects (installed packages, running services, environment variables). **[OFFICIAL]** ([Quick start | JetBrains Air Documentation](https://www.jetbrains.com/help/air/quick-start-with-air.html))

3. **IDE-grade code review workflow.** Air provides a visual diff panel with inline commenting that feeds back into the agent loop, similar to a GitHub PR review experience. Claude Code's review happens in the terminal conversation. **[OFFICIAL]** ([Quick start | JetBrains Air Documentation](https://www.jetbrains.com/help/air/quick-start-with-air.html))

4. **Structural code context injection.** Air lets users reference specific lines, commits, classes, methods, or symbols when defining tasks, leveraging JetBrains' decades of code intelligence. Claude Code relies on file-path-based context (`@file`, `@dir`) or the agent's own exploration via Read/Grep/Glob tools. **[OFFICIAL]** ([Air launch blog](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/))

5. **ACP protocol extensibility.** Any agent that implements ACP can be added to Air without custom integration. Claude Code's extension model is MCP servers and skills — powerful, but limited to extending Claude, not substituting it. **[OFFICIAL]** ([Agent Client Protocol](https://agentclientprotocol.com/))

6. **Enterprise governance (roadmap).** JetBrains Central (EAP Q2 2026) will add centralized policy enforcement, cost attribution, identity management, and auditability across agent-driven workflows. Claude Code has no equivalent enterprise governance layer. **[OFFICIAL]** ([Introducing JetBrains Central](https://blog.jetbrains.com/blog/2026/03/24/introducing-jetbrains-central-an-open-system-for-agentic-software-development/))

### What Claude Code Can Orchestrate That Air Cannot

1. **Hierarchical agent composition.** Claude Code's skill-invokes-subagent pattern enables multi-level workflows: a sprint-dev skill invokes a story implementation subagent, which completes and returns results to a validation loop (AVFL), which spawns parallel reviewer subagents. Air has no concept of agent hierarchy — every task is flat and independent.

2. **Inter-agent communication and debate.** Agent teams enable peer-to-peer messaging, competing hypothesis investigation, and collaborative convergence. Air agents never talk to each other.

3. **Shared task coordination with dependencies.** Agent teams maintain a shared task list with dependency tracking and file-lock-based claiming. Air tasks have no awareness of each other.

4. **Context-preserving delegation.** Subagents receive project CLAUDE.md and the parent's prompt context, then return results that the parent can synthesize. Air tasks start from scratch each time — there is no mechanism to pass accumulated context from one task to another.

5. **Programmatic workflow composition.** The Claude Agent SDK enables programmatic orchestration — dynamic agent creation, streaming message processing, session resumption, and custom permission callbacks. Air's orchestration is entirely manual (user assigns tasks via UI).

6. **Quality gate enforcement via hooks.** Claude Code hooks (`TeammateIdle`, `TaskCreated`, `TaskCompleted`, `PostToolUse`, etc.) enable automated quality enforcement within workflows. Air has no hook system.

### Complementarity Pattern

Air and Claude Code are not competing for the same orchestration niche. A practical integration pattern:

- **Air as the outer loop**: The developer uses Air to manage concurrent independent tasks across the codebase. One task might be assigned to Codex for bulk test generation, another to Gemini for documentation, and a third to Claude Agent for a complex refactoring.
- **Claude Code as the inner loop**: The Claude Agent task within Air runs Claude Code, which internally uses its own skill/subagent/team composition for complex multi-step workflows. The sprint-dev skill orchestrates story implementation, AVFL validation, and iterative fix loops — all invisible to Air, which just sees "one Claude Agent task."

This layered model means Air handles *what* gets done and *who* does it, while Claude Code handles *how* the Claude-specific work is decomposed and quality-gated.

## Protocol Comparison: ACP vs. MCP

ACP and MCP serve different purposes and are not alternatives:

| Aspect | ACP | MCP |
|:-------|:----|:----|
| **Purpose** | Standardize IDE-to-agent communication | Standardize agent-to-tool communication |
| **Direction** | IDE dispatches work to agents | Agent consumes capabilities from servers |
| **Transport** | JSON-RPC over stdio (local); HTTP/WS (remote, WIP) | JSON-RPC over stdio or SSE |
| **Relationship** | ACP can transport MCP ("MCP-over-ACP") | MCP is unaware of ACP |
| **Session model** | Full session lifecycle (create, resume, fork, close) | Stateless tool invocations |
| **Supports** | Planning, diffs, slash commands, file access, terminal | Tool definitions, resource access, sampling |

Claude Code uses MCP extensively — MCP servers provide external capabilities (databases, APIs, browser automation). Air uses ACP to communicate with agents, and those agents may internally use MCP. The two protocols compose naturally. **[OFFICIAL]** ([Agent Client Protocol](https://agentclientprotocol.com/))

## Practical Limitations

### Air Limitations (as of March 2026 public preview)

- **macOS only** — no Windows or Linux support at launch **[PRAC]** ([Medium analysis](https://medium.com/vibecodingpub/jetbrains-air-the-future-of-multi-agent-coding-or-just-more-ai-noise-5450e648a962))
- **No inter-agent coordination** — when multiple agents touch related files, merge conflicts and inconsistent patterns emerge. Air handles this better than manual tool-switching but is not friction-free **[PRAC]** ([ADTmag](https://adtmag.com/articles/2026/03/19/jetbrains-launches-air-preview-for-developers-managing-multiple-ai-agents.aspx))
- **No automated orchestration** — all task assignment is manual; there is no "planner" agent that decomposes work and dispatches subtasks
- **Single-task UI** — despite concurrent execution, the developer sees one task at a time, creating context-switching overhead **[OFFICIAL]** ([Air launch blog](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/))
- **No cloud execution yet** — Docker and worktree isolation are available but cloud sandboxes are roadmap only

### Claude Code Limitations

- **Single-vendor model lock-in** — only Claude models (though multiple tiers available) **[OFFICIAL]** ([Claude Code Docs](https://code.claude.com/docs/en/sub-agents))
- **Agent teams are experimental** — known issues with session resumption, task status lag, slow shutdown, and no nested teams **[OFFICIAL]** ([Agent teams docs](https://code.claude.com/docs/en/agent-teams))
- **No Docker isolation** — worktrees provide file isolation but not system-level sandboxing
- **No visual diff review** — all interaction is terminal-based (unless wrapped in an IDE extension like the VS Code Claude Code extension)
- **No structural code intelligence** — relies on text-based search (Grep/Glob) rather than AST-aware symbol resolution

## Key Findings

1. **Air is a task dispatcher, not an agent orchestrator.** It excels at running heterogeneous agents concurrently in isolated environments, but provides no inter-agent coordination, shared state, or compositional workflow primitives.

2. **Claude Code is a deep composition framework.** Skills, subagents, and agent teams provide hierarchical delegation, peer-to-peer coordination, and programmatic workflow composition — but only within the Claude model family.

3. **The two systems are complementary.** Air can host Claude Agent as a backend, while Claude Code's internal composition handles complex multi-step workflows. This layered model is the natural integration pattern.

4. **Air's unique advantages are IDE-aware**: Docker isolation, structural code context, visual diff review, ACP protocol extensibility, and enterprise governance (roadmap). These are capabilities that terminal-based agents fundamentally lack.

5. **Claude Code's unique advantages are compositional**: hierarchical agent spawning, inter-agent messaging, shared task lists with dependencies, quality gate hooks, and programmatic SDK orchestration. These are capabilities Air's flat task model cannot express.

## Sources

- [Air launch blog post](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/) — **[OFFICIAL]**
- [Quick start | JetBrains Air Documentation](https://www.jetbrains.com/help/air/quick-start-with-air.html) — **[OFFICIAL]**
- [Supported agents | JetBrains Air Documentation](https://www.jetbrains.com/help/air/supported-agents.html) — **[OFFICIAL]**
- [Agent Client Protocol specification](https://agentclientprotocol.com/) — **[OFFICIAL]**
- [ACP landing page](https://www.jetbrains.com/acp/) — **[OFFICIAL]**
- [ACP Agent Registry announcement](https://blog.jetbrains.com/ai/2026/01/acp-agent-registry/) — **[OFFICIAL]**
- [Introducing JetBrains Central](https://blog.jetbrains.com/blog/2026/03/24/introducing-jetbrains-central-an-open-system-for-agentic-software-development/) — **[OFFICIAL]**
- [Create custom subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents) — **[OFFICIAL]**
- [Subagents in the SDK - Claude API Docs](https://platform.claude.com/docs/en/agent-sdk/subagents) — **[OFFICIAL]**
- [Agent Skills in the SDK - Claude API Docs](https://platform.claude.com/docs/en/agent-sdk/skills) — **[OFFICIAL]**
- [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams) — **[OFFICIAL]**
- [Building a C compiler with parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) — **[OFFICIAL]**
- [JetBrains Air: The Future of Multi-Agent Coding](https://medium.com/vibecodingpub/jetbrains-air-the-future-of-multi-agent-coding-or-just-more-ai-noise-5450e648a962) — **[PRAC]**
- [JetBrains Launches Air Preview - ADTmag](https://adtmag.com/articles/2026/03/19/jetbrains-launches-air-preview-for-developers-managing-multiple-ai-agents.aspx) — **[PRAC]**
- [JetBrains Air: agentic IDE - The Register](https://www.theregister.com/2026/03/10/jetbrains_previews_air_proclaims_new) — **[PRAC]**
