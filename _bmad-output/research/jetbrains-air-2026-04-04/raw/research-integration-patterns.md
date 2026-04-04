---
content_origin: claude-code-subagent
date: 2026-04-04
sub_question: "Can Air and Claude Code coexist in a workflow? Concrete integration scenarios."
topic: "JetBrains Air"
---

## Executive Summary

JetBrains Air and Claude Code operate at different layers of the development workflow and can coexist without conflict. Air is a visual, task-oriented orchestration environment for delegating discrete coding tasks to multiple agents in isolated sandboxes. Claude Code is a terminal-native agent with deep filesystem access, custom rules, hooks, memory, and multi-agent orchestration capabilities (subagents, worktrees). The two tools share no runtime state, do not compete for the same filesystem locks, and address different segments of the development lifecycle. The primary integration pattern is **complementary delegation**: Air handles isolated, visually-reviewable coding tasks while Claude Code drives workflow orchestration, practice enforcement, and complex multi-file operations governed by Momentum's rule system.

## Air's Architecture and Operating Model

JetBrains Air launched in public preview in March 2026 as an "Agentic Development Environment" (ADE) — a standalone desktop application (macOS only as of April 2026, with Windows and Linux planned) built around task delegation rather than code editing. ([Air Launch Blog Post](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/)) **[OFFICIAL]**

### Core Concepts

- **Task-centric model**: Work is organized as discrete tasks with clear prompts. Each task is assigned to one agent and one execution environment. You define the task through interactive chat, refine it step by step, and provide precise context by referencing specific files, folders, classes, methods, commits, or lines. ([Quick Start](https://www.jetbrains.com/help/air/quick-start-with-air.html)) **[OFFICIAL]**

- **Agent selection per task**: Air supports four built-in agent providers — Claude Agent (Anthropic), OpenAI Codex, Gemini CLI, and Junie (JetBrains). You select the agent when creating a task; after launch, you can change models within the same provider but cannot switch providers. ([Select Agents and Models](https://www.jetbrains.com/help/air/select-agents-and-models.html)) **[OFFICIAL]**

- **Isolation modes**: Three execution environments provide different isolation guarantees. Local Workspace runs directly in your project folder (fastest, no isolation). Git Worktree creates a separate branch with filesystem isolation. Docker runs in a fully isolated container where all edits, commands, and dependencies stay inside the container. Cloud execution is in tech preview. ([Set Up](https://www.jetbrains.com/help/air/set-up.html)) **[OFFICIAL]**

- **Concurrent execution**: Multiple tasks run asynchronously. The UI shows one task at a time with notifications for others. This enables parallel agent work — one agent adding tests while another fixes a bug — without interference. ([Quick Start](https://www.jetbrains.com/help/air/quick-start-with-air.html)) **[OFFICIAL]**

- **Review and integration**: After task completion, developers inspect changes in a diff view (unified or side-by-side), leave inline comments for follow-up iterations, and accept/commit/push when satisfied. Agent-performed review is also available for structured checks. ([Review and Integrate](https://www.jetbrains.com/help/air/review-and-integrate.html)) **[OFFICIAL]**

### Extensibility

- **MCP support**: Air supports Model Context Protocol servers at three levels — global (all projects), local (`.air/mcp.json` in the project), and workspace (`.mcp.json` in project root). MCP servers extend agents with tools for fetching data and performing actions in external systems. ([Set Up](https://www.jetbrains.com/help/air/set-up.html)) **[OFFICIAL]**

- **ACP (Agent Client Protocol)**: Air adheres to the ACP standard, and the ACP Agent Registry (launched jointly with Zed) provides a curated directory of third-party agents that can be installed with minimal configuration. Custom ACP agents can be added via `acp.json`. ([ACP Agent Registry Blog](https://blog.jetbrains.com/ai/2026/01/acp-agent-registry/)) **[OFFICIAL]**

- **Instruction files**: Air agents automatically detect and use `AGENTS.md` or `CLAUDE.md` files in the repository root. These can specify project context, coding standards, restrictions, and definitions of done. Claude Agent specifically uses `CLAUDE.md` and the `.claude` directory. ([Supported Agents](https://www.jetbrains.com/help/air/supported-agents.html)) **[OFFICIAL]**

## Claude Code's Operating Model (for Contrast)

Claude Code is a terminal-native agentic coding tool that runs in your shell with direct filesystem read/write/edit access across the entire codebase. Key differentiators relevant to coexistence:

- **Rules, hooks, and memory**: Claude Code supports hierarchical rules (global, project, session), pre/post hooks for automated behaviors, and a persistent memory system. These features constitute a **practice layer** — the foundation Momentum builds on. Air has instruction files but no equivalent hook or memory system. **[OFFICIAL]**

- **Subagent orchestration**: Claude Code can spawn subagents that work in isolated worktrees with a hub-and-spoke coordination model. The main agent manages context, delegates tasks, and integrates results — all within the terminal. ([Addy Osmani, Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/)) **[PRAC]**

- **Workflow automation**: Claude Code executes complex, multi-step workflows (sprint planning, story implementation, AVFL validation) that involve sequencing agent actions, enforcing quality gates, and maintaining state across steps. Air's task model is simpler: one task, one agent, one outcome. **[UNVERIFIED]**

- **Git discipline**: Claude Code's hook and rule system can enforce commit conventions, push policies, and branching strategies autonomously. Air provides basic git integration (commit, push, worktree creation) but does not enforce workflow rules. **[UNVERIFIED]**

## Why They Do Not Conflict

Air and Claude Code operate on different planes:

| Dimension | Air | Claude Code |
|---|---|---|
| Interface | Desktop GUI (macOS) | Terminal / CLI |
| Unit of work | Discrete task with visual review | Conversation with full codebase access |
| Agent binding | One agent per task, locked after start | One agent per session, subagent spawning |
| Isolation | Git worktree, Docker, or local | Git worktree or local |
| Practice enforcement | Instruction files only | Rules, hooks, memory, skills |
| Workflow complexity | Single-task, interactive refinement | Multi-step orchestrated workflows |
| State | Per-task, no cross-task memory | Persistent memory, session context |
| Git integration | Basic (commit, push) | Full (conventional commits, push gates, branch discipline) |

They share the filesystem and git repository, but Air's worktree/Docker isolation prevents write conflicts. If Air runs a task in a git worktree, its changes exist on a separate branch until explicitly integrated. Claude Code working on the main branch or its own worktree will not see or be affected by Air's in-progress work.

The `CLAUDE.md` file is shared — Air's Claude Agent reads it, and Claude Code reads it. This means project-level instructions propagate to both tools automatically, providing a shared baseline of coding standards and project context. **[OFFICIAL]**

## Concrete Integration Scenarios

### Scenario 1: Parallel Task Offloading During Sprint Implementation

**Context**: You are running a Momentum sprint-dev workflow in Claude Code, implementing a story that requires focused multi-file changes.

**Pattern**: While Claude Code handles the primary story implementation (which requires Momentum's practice enforcement, AVFL validation, and commit discipline), delegate independent, bounded tasks to Air:

- Generate boilerplate test fixtures in Air (Docker-isolated) while Claude Code implements the feature
- Have Air's Codex agent write API documentation stubs while Claude Code builds the API
- Send a "add error handling to these 5 utility functions" task to Air while Claude Code works on the main feature logic

**Value**: Air's visual diff review makes it easy to verify isolated tasks. Claude Code stays focused on the primary workflow without context dilution. The tasks converge at integration time.

### Scenario 2: Multi-Agent Comparative Evaluation

**Context**: You need to evaluate how different agents handle a specific implementation challenge — for example, a complex data transformation or an algorithm optimization.

**Pattern**: Create the same task in Air targeting different agents (Claude Agent, Codex, Gemini CLI) and review the outputs side by side using Air's diff viewer. Then feed the best approach into Claude Code for integration with full Momentum workflow enforcement.

**Value**: Air's per-task agent selection makes A/B comparison trivial. Claude Code would need separate sessions or subagent configurations to achieve the same effect. Air handles the evaluation; Claude Code handles the integration.

### Scenario 3: Visual Code Review for Agent-Generated Changes

**Context**: Claude Code's AVFL (Adversarial Validate-Fix Loop) identifies issues and applies fixes. You want a human-friendly visual review of the accumulated changes before committing.

**Pattern**: After Claude Code completes a fix pass, open the project in Air and create a review-only task (using Plan permission mode) where an agent summarizes and categorizes the changes. Alternatively, use Air's diff viewer directly to inspect the changes Claude Code made.

**Value**: Air's IDE-grade diff viewer with inline commenting provides a richer review experience than terminal-based `git diff`. This is particularly useful for large changesets spanning many files.

### Scenario 4: Delegating IDE-Aware Refactoring Tasks

**Context**: You need refactoring that benefits from structural code understanding — renaming symbols across a codebase, extracting interfaces, or reorganizing imports.

**Pattern**: Define the refactoring task in Air, which provides structural code context (classes, methods, symbols) to the agent. Air's code intelligence layer gives agents precise context that a terminal-based tool would need to reconstruct from raw file reads.

**Value**: Air inherits JetBrains' 26-year investment in code intelligence. For refactoring tasks that depend on understanding type hierarchies, call graphs, or symbol references, Air's structural context may produce more accurate results than pure file-based context.

### Scenario 5: Onboarding and Exploration Tasks

**Context**: A new team member needs to understand a codebase, or you need to explore an unfamiliar dependency.

**Pattern**: Use Air to create exploration tasks: "Explain the authentication flow in this codebase," "Document the data model relationships," or "Identify all API endpoints and their request/response schemas." Air's visual interface and interactive refinement make exploration more accessible than terminal-based workflows.

**Value**: Air's GUI lowers the barrier for exploratory tasks that do not require Momentum's practice enforcement. Claude Code is overkill for "help me understand this code" tasks that benefit from visual presentation.

### Scenario 6: MCP-Bridged External System Integration

**Context**: Your workflow requires fetching context from external systems — YouTrack issues, Confluence pages, Slack threads, or custom APIs.

**Pattern**: Configure MCP servers in Air's `.air/mcp.json` to connect to these systems. When defining tasks, agents can pull issue details, documentation, or other context through MCP. Claude Code can also use MCP servers, but Air's three-level MCP configuration (global, local, workspace) and its shared `.mcp.json` support make it straightforward to maintain MCP config that both tools consume.

**Value**: Both tools support MCP, so the same servers can serve both. Air's GUI makes it easier to verify that MCP context was correctly ingested. For tasks that are primarily about translating external requirements into code, Air's interactive task refinement with MCP context is effective.

### Scenario 7: Spike Research with Contained Blast Radius

**Context**: During sprint execution, a spike story requires experimental code that should not touch the main working branch.

**Pattern**: Create the spike task in Air using Docker isolation. The agent experiments freely — installing dependencies, writing throwaway code, running tests — without any risk to the local workspace. Review the results in Air's diff viewer. If the spike yields useful patterns, extract them and feed them to Claude Code for proper implementation under Momentum's story workflow.

**Value**: Docker isolation in Air provides a stronger sandbox than git worktrees alone. The experimental code never touches your local environment. This is particularly valuable for spikes involving unfamiliar dependencies or system-level changes.

## Anti-Patterns: When NOT to Use Air

Not every scenario benefits from adding Air to the workflow. Avoid these:

- **Practice-enforced workflows**: Momentum's sprint-dev, AVFL, and story implementation workflows depend on Claude Code's rules, hooks, and memory. Running these through Air would bypass all practice enforcement. Keep orchestrated workflows in Claude Code.

- **Sequential multi-step operations**: Air's task model is one-task-one-outcome. Workflows that require maintaining state across steps (e.g., "implement feature, then write tests, then run AVFL, then commit with conventional format") should stay in Claude Code.

- **Git discipline enforcement**: Air's git integration is basic — commit and push. It does not enforce conventional commits, push approval gates, or commit-at-every-logical-unit rules. Any workflow where git discipline matters should be driven by Claude Code.

- **Cross-task coordination**: Air tasks are independent. If task B depends on task A's output, you must manually bridge them. Claude Code's subagent model handles dependencies natively through the hub-and-spoke pattern.

## Architectural Considerations for Coexistence

### Shared Configuration Surface

Both tools read from the same project configuration:

- `CLAUDE.md` / `.claude/` — Read by both Claude Code and Air's Claude Agent
- `.mcp.json` — Consumable by both tools if Air's "Launch workspace MCP servers" is enabled
- `AGENTS.md` — Read by Air agents (and potentially by Claude Code if configured)

This shared surface means project-level instructions, coding standards, and MCP configurations only need to be maintained once. **[OFFICIAL]**

### Branch Coordination

When both tools are active on the same repository, branch management requires attention:

- If Air uses git worktree isolation, its tasks create separate branches that do not affect Claude Code's working branch
- If Air uses local workspace mode (no isolation), both tools write to the same branch — potential for conflicts
- **Recommendation**: Always use git worktree or Docker isolation in Air when Claude Code is also active on the same project

### JetBrains Central (Future)

JetBrains Central, announced March 2026 with EAP in Q2 2026, aims to provide a unified control plane for agent orchestration across IDEs, CLI tools, and agents with governance, cost tracking, and audit trails. If Central materializes as described, it could provide a coordination layer between Air and Claude Code — routing tasks to the appropriate tool based on complexity, required isolation, or practice enforcement needs. ([JetBrains Central Blog](https://blog.jetbrains.com/blog/2026/03/24/introducing-jetbrains-central-an-open-system-for-agentic-software-development/)) **[OFFICIAL]**

## Integration Maturity Assessment

| Capability | Maturity | Notes |
|---|---|---|
| Side-by-side usage on same repo | Ready | Git worktree isolation prevents conflicts |
| Shared instruction files | Ready | CLAUDE.md read by both tools |
| Shared MCP servers | Ready | .mcp.json consumable by both |
| Task delegation from Claude Code to Air | Manual | No API or automation bridge exists |
| Unified workflow orchestration | Not available | JetBrains Central may address this in future |
| Practice enforcement in Air | Not possible | Air lacks hooks, rules, memory |
| Cross-tool state sharing | Not available | No mechanism for sharing session context |

## Key Findings

1. **Coexistence is architecturally sound** but requires manual coordination. There is no automated bridge between the tools — you manually create Air tasks for work you want to delegate and manually integrate results back.

2. **Air adds the most value for bounded, visually-reviewable tasks** that benefit from IDE-grade code intelligence and diff viewing but do not require Momentum's practice enforcement.

3. **Claude Code remains the correct home for orchestrated workflows**. Sprint planning, story implementation, AVFL, and any workflow requiring rules/hooks/memory must stay in Claude Code.

4. **The shared configuration surface (CLAUDE.md, .mcp.json) reduces maintenance burden** and ensures both tools operate with the same project context and coding standards.

5. **Docker isolation in Air provides a stronger sandbox** than either tool offers alone for worktree-based isolation, making it valuable for experimental and spike work.

6. **JetBrains Central could change this picture significantly** if it delivers on the promise of a unified control plane with task routing between tools. This is speculative — EAP is Q2 2026.

## Sources

- [Air Launch Blog Post — JetBrains](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/) **[OFFICIAL]**
- [Quick Start — JetBrains Air Documentation](https://www.jetbrains.com/help/air/quick-start-with-air.html) **[OFFICIAL]**
- [Set Up — JetBrains Air Documentation](https://www.jetbrains.com/help/air/set-up.html) **[OFFICIAL]**
- [Select Agents and Models — JetBrains Air Documentation](https://www.jetbrains.com/help/air/select-agents-and-models.html) **[OFFICIAL]**
- [Supported Agents — JetBrains Air Documentation](https://www.jetbrains.com/help/air/supported-agents.html) **[OFFICIAL]**
- [Review and Integrate — JetBrains Air Documentation](https://www.jetbrains.com/help/air/review-and-integrate.html) **[OFFICIAL]**
- [ACP Agent Registry Blog — JetBrains](https://blog.jetbrains.com/ai/2026/01/acp-agent-registry/) **[OFFICIAL]**
- [JetBrains Central Blog — JetBrains](https://blog.jetbrains.com/blog/2026/03/24/introducing-jetbrains-central-an-open-system-for-agentic-software-development/) **[OFFICIAL]**
- [Air Homepage](https://air.dev/) **[OFFICIAL]**
- [The Code Agent Orchestra — Addy Osmani](https://addyosmani.com/blog/code-agent-orchestra/) **[PRAC]**
- [JetBrains Air Launches: A New Way to Orchestrate Multiple AI Coding Agents — DEV Community](https://dev.to/ajay_kumar_1daef5fe089885/jetbrains-air-launches-a-new-way-to-orchestrate-multiple-ai-coding-agents-14gk) **[PRAC]**
- [Claude Code JetBrains Integration — Claude Code Docs](https://code.claude.com/docs/en/jetbrains) **[OFFICIAL]**
- [AI Coding Assistants April 2026 Rankings — Digital Applied](https://www.digitalapplied.com/blog/ai-coding-assistants-april-2026-cursor-copilot-claude) **[PRAC]**
- [Configure Agent Behavior — JetBrains AI Assistant Documentation](https://www.jetbrains.com/help/ai-assistant/configure-agent-behavior.html) **[OFFICIAL]**
