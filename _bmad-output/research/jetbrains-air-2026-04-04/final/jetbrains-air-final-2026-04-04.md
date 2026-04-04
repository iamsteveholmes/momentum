---
title: "JetBrains Air — Research Report"
date: 2026-04-04
type: Technical Research — Consolidated Report
status: Complete
content_origin: claude-code-synthesis
human_verified: false
derives_from:
  - path: raw/research-agent-orchestration.md
    relationship: synthesized_from
  - path: raw/research-ide-capabilities.md
    relationship: synthesized_from
  - path: raw/research-integration-patterns.md
    relationship: synthesized_from
  - path: raw/gemini-output.md
    relationship: synthesized_from
---

# JetBrains Air — Research Report

## Executive Summary

JetBrains Air is an Agentic Development Environment (ADE) that launched in public preview in March 2026. It dispatches discrete coding tasks to heterogeneous agent backends (Claude Agent, OpenAI Codex, Gemini CLI, Junie, and any ACP-compliant agent) running in isolated environments (local workspace, git worktree, or Docker container). Air is not an AI agent itself. It is an orchestration surface that manages agent lifecycles, provides IDE-grade code intelligence as context, and presents agent-generated changes through a visual diff review interface. ([Air Launch Blog](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/)) [VERIFIED]

Air and Claude Code occupy different layers of the development stack. Air is a task dispatcher: it routes independent units of work to agents and manages their sandboxed execution. Claude Code is a composition framework: it orchestrates hierarchical multi-agent workflows through skills, subagents, and agent teams within the Claude model family. Air handles *what* gets done and *who* does it. Claude Code handles *how* complex work is decomposed, quality-gated, and practiced. The two tools share configuration surfaces (CLAUDE.md, .mcp.json) and can operate on the same repository without conflict when Air uses worktree or Docker isolation.

The practical integration pattern is complementary delegation. Momentum's practice-enforced workflows (sprint-dev, AVFL, story implementation) stay in Claude Code, which provides the rules, hooks, memory, and compositional orchestration they require. Bounded, visually-reviewable tasks that benefit from IDE-aware context, multi-agent comparison, or Docker sandboxing are delegated to Air. This layering adds value without disrupting existing workflows.

Air's most distinctive capabilities are structural code context (symbol resolution, cross-file usage graphs, semantic refactoring via the IntelliJ MCP Server), Docker-isolated execution, visual diff review with inline commenting, and heterogeneous agent selection. These are capabilities that terminal-based agents fundamentally lack. However, Air provides no inter-agent coordination, no practice enforcement, no workflow composition, and no persistent memory — all areas where Claude Code is strong.

## 1. Multi-Agent Task Dispatch vs. Skill Composition

### Air's Orchestration Model

Air's core abstraction is the **task** — a user-defined unit of work assigned to a single agent in a single execution environment. Tasks have a lifecycle (Running, Input Required, Done, Canceled) and run concurrently but independently. There is no inter-agent communication, shared state, or dependency tracking between tasks. ([Quick Start](https://www.jetbrains.com/help/air/quick-start-with-air.html)) [VERIFIED]

The user selects the agent backend per task from four built-in providers plus any ACP-registered agent. ([Supported Agents](https://www.jetbrains.com/help/air/supported-agents.html)) [VERIFIED]

| Agent | Provider | Key Strength |
|---|---|---|
| Claude Agent | Anthropic | Complex reasoning, CLAUDE.md awareness |
| OpenAI Codex | OpenAI | Code generation patterns |
| Gemini CLI | Google | Multimodal reasoning, large context |
| Junie | JetBrains | Aggregated multi-model access |

Execution isolation options — local workspace, git worktree, or Docker container — prevent concurrent agents from conflicting on the filesystem. ([Air Launch Blog](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/)) [VERIFIED]

### Claude Code's Composition Model

Claude Code provides three composition primitives operating at different coordination levels:

- **Skills** — filesystem-based capability extensions (`.claude/skills/`) that encode domain knowledge and workflow procedures. Auto-discovered, model-invoked, composable. ([Agent Skills — Claude API Docs](https://platform.claude.com/docs/en/agent-sdk/skills)) [VERIFIED]
- **Subagents** — context-isolated child agents with tool restrictions, model routing, and parallel execution. Parent-child hierarchy only; no nesting. ([Subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents)) [VERIFIED]
- **Agent Teams** (experimental) — multi-session coordination with shared task lists, dependency tracking, peer-to-peer messaging, and git worktree isolation per teammate. Demonstrated at scale: a 16-agent team produced a 100K-line Rust C compiler. ([Agent Teams — Claude Code Docs](https://code.claude.com/docs/en/agent-teams), [Building a C compiler](https://www.anthropic.com/engineering/building-c-compiler)) [VERIFIED]

### Comparative Analysis

| Dimension | Air | Claude Code |
|---|---|---|
| Unit of dispatch | Task (1 agent, 1 session) | Subagent / teammate / skill invocation |
| Agent heterogeneity | Yes — multiple providers | No — Claude models only (multiple tiers) |
| Inter-agent communication | None | Subagents: parent-child. Teams: peer-to-peer |
| Shared state | None between tasks | Teams: shared task list with dependencies |
| Coordination model | Flat, independent | Hierarchical, composable |
| Execution isolation | Local / worktree / Docker | Same process (subagents) / worktree (teams) |
| Workflow automation | Manual task assignment via UI | Programmatic via SDK, skills, hooks |

### What Each Tool Uniquely Offers

**Air can do what Claude Code cannot:**
- Run heterogeneous agent backends concurrently on the same codebase [VERIFIED]
- Provide Docker-based full-system isolation for agent execution [VERIFIED]
- Route tasks to the best-fit model (e.g., Codex for bulk generation, Gemini for multimodal) [VERIFIED]
- Extend the agent ecosystem via the open ACP protocol ([Agent Client Protocol](https://agentclientprotocol.com/)) [VERIFIED]

**Claude Code can do what Air cannot:**
- Compose hierarchical multi-step workflows (skill invokes subagent invokes validation loop)
- Enable inter-agent debate and collaborative convergence
- Maintain shared task lists with dependency tracking
- Enforce quality gates via hooks (PostToolUse, TaskCompleted, TeammateIdle)
- Preserve accumulated context across delegated tasks
- Automate workflow composition programmatically via the Agent SDK

### Protocol Relationship: ACP and MCP

ACP (Agent Client Protocol) and MCP (Model Context Protocol) are complementary, not competing. ACP standardizes IDE-to-agent communication; MCP standardizes agent-to-tool communication. ACP can transport MCP ("MCP-over-ACP"), making it a superset. Claude Code uses MCP directly for external tool access. Air uses ACP to dispatch work to agents, which may internally use MCP. ([Agent Client Protocol](https://agentclientprotocol.com/)) [VERIFIED]

## 2. IDE-Level Capabilities

### Air's Code Intelligence Layer

Air uses Language Server Protocol implementations to provide structural code intelligence for 9 languages with full support (Kotlin, Go, Rust, Python, C/C++/CUDA, TypeScript/JavaScript, HTML, CSS, Svelte) and 50+ with syntax highlighting only. Notably, Java has syntax highlighting only — full LSP support is not yet available. ([Air Language Support](https://www.jetbrains.com/help/air/supported-languages.html)) [VERIFIED]

For supported languages, Air exposes:
- Go to Definition, Find Usages, Go to Implementations, Go to Type Definition
- Code completion (single-line and block)
- Semantic highlighting and language-aware formatting
- Quick-fixes and rename refactoring

([Air Explore Code](https://www.jetbrains.com/help/air/explore-projects.html)) [VERIFIED]

### The IntelliJ MCP Server

Starting with IDE version 2025.2, all JetBrains IDEs include a built-in MCP server exposing ~25 tools to any MCP-compatible agent. Air can pass these tools to installed agents via ACP. ([IntelliJ IDEA MCP Server](https://www.jetbrains.com/help/idea/mcp-server.html)) [VERIFIED]

Key tool categories:

| Category | Tools | What They Provide |
|---|---|---|
| Symbol resolution | `get_symbol_info` | Semantic type, signature, docs for symbol at position |
| Code analysis | `get_file_problems` | IDE inspection results (errors, warnings, severity) |
| Refactoring | `rename_refactoring`, `reformat_file` | Scope-aware structural rename, formatting |
| Project model | `get_project_modules`, `get_project_dependencies` | Module structure, library dependencies |
| Execution | `execute_run_configuration`, `execute_terminal_command` | Named run configs, shell commands |
| Database | 9 tools (list connections, schemas, execute SQL) | Full SQL access for configured data sources |
| Navigation | `find_files_by_glob`, `search_in_files_by_text/regex` | IDE-indexed search |

### Debugger Integration (Community Plugin)

The built-in MCP server does not include debugger tools. A community-maintained plugin (Debugger MCP Server) adds 22 tools covering breakpoint management, execution control, state inspection, and session management. Tested across IntelliJ IDEA, PyCharm, WebStorm, GoLand, RustRover, Android Studio, and PhpStorm. ([jetbrains-debugger-mcp-plugin — GitHub](https://github.com/hechtcarmel/jetbrains-debugger-mcp-plugin)) [CITED]

### Capability Comparison: Air+IDE vs. Claude Code CLI

| Capability | Air / JetBrains IDE | Claude Code CLI |
|---|---|---|
| Symbol resolution | `get_symbol_info` — typed, semantic | LLM inference from file content |
| Find usages | IDE-indexed cross-project graph | ripgrep text search + disambiguation |
| Rename refactoring | `rename_refactoring` — scope-aware | LLM-guided text replacement |
| Code inspections | `get_file_problems` — hundreds of inspections | Linters via shell (if configured) |
| Debugger control | 22-tool MCP plugin (breakpoints, stepping, eval) | Shell-based debugger; unstructured output |
| Project model | `get_project_modules`, `get_project_dependencies` | Parse package.json/build.gradle manually |
| Database access | 9 SQL tools | Shell-based psql/mysql if available |
| Task context | @-mentions resolve to symbols, commits, lines | User describes locations in text |
| Diff review | Integrated editor with gutter comments | `git diff` in terminal |
| Language coverage | 9 languages full; 50+ syntax only | Language-agnostic (no intelligence layer) |

### The CLI Workaround

Claude Code can connect to the IntelliJ MCP server when a JetBrains IDE is running, gaining access to the same ~25 tools. This requires external setup and an active IDE instance, but it narrows the capability gap for teams willing to maintain that configuration. ([JetBrains ACP docs](https://www.jetbrains.com/help/ai-assistant/acp.html)) [VERIFIED]

## 3. Coexistence and Integration Patterns

### Why They Do Not Conflict

Air and Claude Code share the filesystem and git repository but operate on different planes. Air is a desktop GUI for visual task management; Claude Code is a terminal agent with practice enforcement. When Air uses worktree or Docker isolation, its in-progress changes exist on separate branches invisible to Claude Code's working branch. Both tools read CLAUDE.md and .mcp.json, so project-level instructions propagate automatically. ([Supported Agents](https://www.jetbrains.com/help/air/supported-agents.html)) [VERIFIED]

### Integration Maturity

| Capability | Status |
|---|---|
| Side-by-side usage on same repo | Ready (worktree isolation) |
| Shared instruction files (CLAUDE.md) | Ready |
| Shared MCP servers (.mcp.json) | Ready |
| Task delegation from Claude Code to Air | Manual only |
| Unified workflow orchestration | Not available |
| Practice enforcement in Air | Not possible (no hooks/rules/memory) |
| Cross-tool state sharing | Not available |

### Concrete Integration Scenarios

**Parallel task offloading during sprint work.** While Claude Code handles primary story implementation with Momentum practice enforcement, delegate bounded independent tasks to Air: test fixture generation (Docker-isolated), API documentation stubs via Codex, or error handling additions across utility functions. Air's visual diff review makes verification fast. Claude Code stays focused without context dilution.

**Multi-agent comparative evaluation.** Create the same implementation task in Air targeting different agents (Claude, Codex, Gemini) and review outputs side by side. Feed the best approach into Claude Code for integration under full workflow enforcement. Air makes A/B comparison trivial.

**IDE-aware refactoring delegation.** Define refactoring tasks in Air where structural code context (classes, methods, symbols via @-mentions) gives agents precise context that terminal-based tools must reconstruct from raw file reads.

**Spike research with contained blast radius.** Create spike tasks in Air using Docker isolation. Agents experiment freely — installing dependencies, writing throwaway code — without touching the local workspace. Extract useful patterns for proper implementation in Claude Code under Momentum's story workflow.

**Visual review of agent-generated changes.** After Claude Code completes a fix pass, use Air's diff viewer with inline commenting for human-friendly review of large changesets spanning many files.

### Anti-Patterns

- **Do not run Momentum workflows through Air.** Sprint-dev, AVFL, and story implementation depend on Claude Code's rules, hooks, and memory. Air bypasses all practice enforcement.
- **Do not use Air for sequential multi-step operations.** Air's one-task-one-outcome model cannot maintain state across workflow steps.
- **Do not use Air's local workspace mode when Claude Code is active.** Both tools writing to the same branch creates conflict risk. Always use worktree or Docker isolation.
- **Do not expect cross-task coordination in Air.** If task B depends on task A's output, you must manually bridge them.

## Decision Framework: When to Use What

| Scenario | Use Air | Use Claude Code | Use Both |
|---|---|---|---|
| Practice-enforced workflow (sprint, story, AVFL) | | X | |
| Bounded, isolated coding task | X | | |
| Complex multi-step implementation | | X | |
| Multi-agent comparison (A/B testing agents) | X | | |
| Spike with Docker sandbox | X | | |
| Story implementation + parallel test generation | | | X |
| Structural refactoring needing symbol resolution | X | | |
| Git discipline (conventional commits, push gates) | | X | |
| Visual review of large changesets | X | | |
| Workflow requiring hooks and quality gates | | X | |

**Rule of thumb:** If the task requires practice enforcement, workflow composition, or persistent state, use Claude Code. If the task is bounded, benefits from visual review or IDE context, or needs agent heterogeneity or Docker isolation, use Air.

## Cross-Cutting Themes

**Complementary by architecture, not by accident.** Air dispatches; Claude Code composes. Air manages the outer loop of independent tasks; Claude Code manages the inner loop of coordinated workflow steps. This is not a workaround — the tools genuinely address different coordination problems.

**CLAUDE.md as shared contract.** Both tools read CLAUDE.md and the `.claude/` directory, creating a natural shared baseline for project context and coding standards. This means adopting Air does not require maintaining separate instruction sets.

**ACP as ecosystem play.** The Agent Client Protocol is JetBrains' bet on becoming the hub for heterogeneous agents. Zed and Cursor have already joined the ACP Registry. If ACP achieves broad adoption, Air becomes the universal agent orchestration surface regardless of which models or agents emerge. ([ACP Agent Registry](https://blog.jetbrains.com/ai/2026/01/acp-agent-registry/), [Cursor joins ACP](https://blog.jetbrains.com/ai/2026/03/cursor-joined-the-acp-registry-and-is-now-live-in-your-jetbrains-ide/)) [VERIFIED]

**JetBrains Central as inflection point.** JetBrains Central (EAP Q2 2026) promises a unified control plane with governance, cost attribution, cloud runtimes, and a semantic layer aggregating code, architecture, and organizational knowledge. If delivered, Central could provide the missing coordination layer between Air and Claude Code — routing tasks to the appropriate tool based on complexity and practice requirements. This is speculative but worth monitoring. ([JetBrains Central](https://blog.jetbrains.com/blog/2026/03/24/introducing-jetbrains-central-an-open-system-for-agentic-software-development/)) [VERIFIED]

## Recommendations

1. **Adopt Air for bounded task offloading.** Use it alongside Claude Code for isolated tasks that benefit from visual review, Docker sandboxing, or multi-agent comparison. Do not migrate Momentum workflows to Air.

2. **Use worktree or Docker isolation exclusively.** Never run Air tasks in local workspace mode when Claude Code is also active on the same repository.

3. **Leverage the shared CLAUDE.md surface.** Maintain a single set of project instructions that both tools consume. No duplication needed.

4. **Evaluate the IntelliJ MCP Server connection from Claude Code.** For teams running JetBrains IDEs, connecting Claude Code to the IntelliJ MCP server provides IDE-grade tools (symbol resolution, inspections, structural rename) without switching to Air for every task.

5. **Monitor JetBrains Central.** The Q2 2026 EAP could change the integration calculus significantly. If Central delivers unified task routing with governance, the Air + Claude Code combination becomes a managed platform rather than a manual pairing.

6. **Do not invest in ACP agent development yet.** The protocol is young and adoption is limited. Wait for the ecosystem to stabilize before building custom ACP agents.

## Known Limitations

- **Air is macOS only** as of the March 2026 public preview. Windows and Linux support is planned but unavailable. ([Air Launch Blog](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/)) [VERIFIED]
- **Air's language intelligence covers only 9 languages fully.** Java, C#, PHP, Ruby, and others receive syntax highlighting only. Claude Code's LLM-based approach is language-agnostic, which is an advantage for polyglot projects. [VERIFIED]
- **No inter-agent coordination in Air.** Tasks are independent. Merge conflicts and inconsistent patterns can emerge when multiple agents touch related files. Practitioners report this as a friction point. ([ADTmag](https://adtmag.com/articles/2026/03/19/jetbrains-launches-air-preview-for-developers-managing-multiple-ai-agents.aspx)) [CITED]
- **Air's single-task UI creates context-switching overhead.** Despite concurrent execution, the developer sees one task at a time and receives notifications for others. [VERIFIED]
- **Agent teams in Claude Code are experimental.** Known issues with session resumption, task status lag, slow shutdown, and no nested teams. [VERIFIED]
- **The Debugger MCP plugin is community-maintained.** Not an official JetBrains product. Maintenance and compatibility are not guaranteed. [CITED]
- **No automated delegation bridge exists.** Moving work between Air and Claude Code is entirely manual. There is no API, webhook, or protocol for automated task handoff.
- **JetBrains Central is vaporware until EAP ships.** All governance and coordination capabilities attributed to Central are roadmap promises, not delivered features. [INFERRED]

## Sources

1. [Air Launch Blog Post — JetBrains (March 2026)](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/) [VERIFIED]
2. [Quick Start — JetBrains Air Documentation](https://www.jetbrains.com/help/air/quick-start-with-air.html) [VERIFIED]
3. [Supported Agents — JetBrains Air Documentation](https://www.jetbrains.com/help/air/supported-agents.html) [VERIFIED]
4. [Select Agents and Models — JetBrains Air Documentation](https://www.jetbrains.com/help/air/select-agents-and-models.html) [VERIFIED]
5. [Air Language Support — JetBrains Air Documentation](https://www.jetbrains.com/help/air/supported-languages.html) [VERIFIED]
6. [Air Explore Code — JetBrains Air Documentation](https://www.jetbrains.com/help/air/explore-projects.html) [VERIFIED]
7. [Review and Integrate — JetBrains Air Documentation](https://www.jetbrains.com/help/air/review-and-integrate.html) [VERIFIED]
8. [Set Up — JetBrains Air Documentation](https://www.jetbrains.com/help/air/set-up.html) [VERIFIED]
9. [Agent Client Protocol — Specification](https://agentclientprotocol.com/) [VERIFIED]
10. [ACP Agent Registry — JetBrains (January 2026)](https://blog.jetbrains.com/ai/2026/01/acp-agent-registry/) [VERIFIED]
11. [Cursor Joins ACP Registry — JetBrains (March 2026)](https://blog.jetbrains.com/ai/2026/03/cursor-joined-the-acp-registry-and-is-now-live-in-your-jetbrains-ide/) [VERIFIED]
12. [IntelliJ IDEA MCP Server — JetBrains Documentation](https://www.jetbrains.com/help/idea/mcp-server.html) [VERIFIED]
13. [ACP Documentation for AI Assistant — JetBrains](https://www.jetbrains.com/help/ai-assistant/acp.html) [VERIFIED]
14. [JetBrains Central Announcement — JetBrains (March 2026)](https://blog.jetbrains.com/blog/2026/03/24/introducing-jetbrains-central-an-open-system-for-agentic-software-development/) [VERIFIED]
15. [Agent Skills — Claude API Docs](https://platform.claude.com/docs/en/agent-sdk/skills) [VERIFIED]
16. [Subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents) [VERIFIED]
17. [Agent Teams — Claude Code Docs](https://code.claude.com/docs/en/agent-teams) [VERIFIED]
18. [Building a C Compiler with Parallel Claudes — Anthropic Engineering](https://www.anthropic.com/engineering/building-c-compiler) [VERIFIED]
19. [Debugger MCP Server Plugin — GitHub](https://github.com/hechtcarmel/jetbrains-debugger-mcp-plugin) [CITED]
20. [JetBrains Air: Multi-Agent Coding Analysis — Medium](https://medium.com/vibecodingpub/jetbrains-air-the-future-of-multi-agent-coding-or-just-more-ai-noise-5450e648a962) [CITED]
21. [JetBrains Launches Air Preview — ADTmag](https://adtmag.com/articles/2026/03/19/jetbrains-launches-air-preview-for-developers-managing-multiple-ai-agents.aspx) [CITED]
22. [The Code Agent Orchestra — Addy Osmani](https://addyosmani.com/blog/code-agent-orchestra/) [CITED]
