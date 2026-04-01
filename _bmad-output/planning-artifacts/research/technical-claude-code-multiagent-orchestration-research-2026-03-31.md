# Claude Code Multi-Agent Orchestration — Technical Research Report
**Date:** 2026-03-31
**Researcher:** Claude Sonnet 4.6 (automated research agent)
**Sources:** Official Anthropic documentation (code.claude.com, platform.claude.com), GitHub issues, practitioner blog posts

---

## 1. Native Orchestration Features in Claude Code

Claude Code (as of v2.1.32+) supports three distinct multi-agent primitives natively:

### 1a. Subagents (Stable)
Subagents are the primary parallelization primitive. Each runs in its own isolated context window with a custom system prompt, restricted tool set, and independent permissions. Defined as Markdown files with YAML frontmatter in:
- `.claude/agents/` (project scope, checked into git)
- `~/.claude/agents/` (user scope, all projects)
- Plugin's `agents/` directory (lowest priority)
- `--agents` CLI flag (session scope, highest priority)

Key frontmatter fields:
- `tools` / `disallowedTools` — allowlist or denylist
- `model` — `sonnet`, `opus`, `haiku`, full model ID, or `inherit`
- `permissionMode` — `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`
- `maxTurns` — max agentic turns before subagent stops
- `isolation: worktree` — spawn subagent in its own git worktree (clean isolation)
- `memory` — `user`, `project`, or `local` for persistent cross-session memory
- `hooks` — `PreToolUse`, `PostToolUse`, `Stop` lifecycle hooks scoped to the subagent
- `mcpServers` — MCP servers scoped to the subagent (not exposed to main conversation)
- `skills` — inject full skill content at startup (not inherited from parent)
- `effort` — override effort level for this subagent
- `background: true` — always run as background task

**Critical constraint:** Subagents cannot spawn other subagents. Nesting is not supported.

Built-in subagents Claude Code ships with:
- **Explore** — Haiku, read-only tools, codebase search
- **Plan** — inherits model, read-only, used in plan mode
- **General-purpose** — all tools, complex multi-step tasks
- **Bash** — terminal commands in separate context
- **statusline-setup**, **Claude Code Guide** — internal tooling

### 1b. Agent Teams (Experimental — v2.1.32+)
Enabled via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `settings.json` or environment. This is a distinct, higher-coordination architecture vs. subagents.

Architecture:
- **Team lead** — main session, creates team, spawns teammates, coordinates
- **Teammates** — independent Claude Code sessions, each with own context window
- **Shared task list** — `~/.claude/tasks/{team-name}/`, with file-locking for claim races
- **Mailbox** — async messaging between agents; point-to-point `message` or `broadcast`

Display modes:
- **in-process** — all teammates in main terminal, Shift+Down to cycle
- **split panes** — tmux or iTerm2 required; each teammate in own pane

Teammate coordination features:
- Self-claim tasks from shared list (no lead required for every assignment)
- Task dependencies: blocked tasks auto-unblock when dependencies complete
- Peer messaging without going through lead
- `TeammateIdle`, `TaskCreated`, `TaskCompleted` hooks in `settings.json`

Context passing: Teammates load the same project context as a new session (CLAUDE.md, MCP servers, skills) plus the spawn prompt from the lead. Lead's conversation history does NOT carry over.

Team config stored at: `~/.claude/teams/{team-name}/config.json` — do not edit manually.

**Resumption limitation:** `/resume` and `/rewind` do not restore in-process teammates.

### 1c. Git Worktree Isolation (Stable)
Two mechanisms:

1. `claude --worktree <name>` — creates `.claude/worktrees/<name>/` with branch `worktree-<name>`, branching from `origin/HEAD`
2. `isolation: worktree` in subagent frontmatter — each invocation gets a fresh worktree, auto-cleaned if no changes

`.worktreeinclude` file at project root: copies gitignored files (`.env`, etc.) into fresh worktrees.

The `/batch` skill (announced Feb 27, 2026 by Boris Cherny) uses this pattern for large-scale parallel code migrations with worktree-isolated agents.

### 1d. Hooks (Stable)
Hooks are shell commands or SDK callbacks that fire at lifecycle events. Key events for multi-agent:
- `PreToolUse` / `PostToolUse` — before/after any tool call
- `SubagentStart` / `SubagentStop` — in `settings.json`, fires in main session
- `TeammateIdle`, `TaskCreated`, `TaskCompleted` — for agent teams
- `WorktreeCreate` / `WorktreeRemove` — replace default git worktree logic
- `Notification` — when Claude needs attention (idle, permission prompt, auth)

Exit code 2 from a hook sends feedback and blocks the action (for `PreToolUse`, `TaskCreated`, `TaskCompleted`).

### 1e. Skills / SKILL.md (Stable)
Skills are Markdown files in `.claude/skills/*/SKILL.md` with YAML frontmatter. Not subagents — they inject content into the main conversation context or a specified subagent's context. Key frontmatter:
- `context: fork` — runs the skill in a specified subagent's context (not main)
- `disable-model-invocation: true` — for side-effecting workflows invoked manually
- `skills` in subagent frontmatter — inject skill content into subagent at startup

**Context rot risk:** Skill files should be kept under ~2,000–3,000 tokens. Bloated skill files degrade attention, create instruction conflicts, and compress the token budget before actual work begins.

### 1f. Claude Agent SDK (Python and TypeScript)
Renamed from "Claude Code SDK." Available via:
- `pip install claude-agent-sdk`
- `npm install @anthropic-ai/claude-agent-sdk`

The SDK exposes the same primitives programmatically:
- `query()` — streaming agent loop with `allowedTools`, `agents`, `hooks`, `mcpServers`, `permissionMode`, `resume`, `settingSources`
- `AgentDefinition` — define subagents inline with `description`, `prompt`, `tools`, `model`
- `HookMatcher` — programmatic hooks with callback functions
- Session resume via `session_id` from `init` message
- Supports Bedrock, Vertex AI, and Azure AI Foundry backends

**SDK constraint:** Must include `"Agent"` in `allowedTools` for the agent to be able to spawn subagents. Can restrict which subagent types with `Agent(worker, researcher)` syntax.

---

## 2. Concurrency Limits

### Official Documentation Position
The official docs do NOT specify a hard numeric cap. The subagent docs note a "parallelism cap of 10 concurrent subagents" in one source, with queuing behavior for additional tasks. The agent teams docs state: "There's no hard limit on the number of teammates."

### Practitioner-Reported Limits

**GitHub Issue #15487 (opened Dec 27, 2025 — auto-closed Mar 4, 2026, locked Mar 19, 2026):**
The most authoritative practitioner data point. Key findings:
- On a 2vCPU/4GB RAM VPS, 24 parallel subagent processes spawned within 2 minutes
- Caused **17.3x disk I/O spike** (8.83 → 152.80 blocks/s) and **5.6x CPU increase** (7.59% → 42.77%)
- System required hard reboot
- Evidence: 24 `.jsonl` session files with overlapping timestamps
- Doc says "Subagents operate sequentially, not in parallel" but evidence contradicts this — multiple Agent tool calls in a single response launch simultaneously

**Community data point from the same issue (audiovideoron, Feb 3, 2026 — Mac mini M4 Pro, 24GB RAM):**
- Complete system freeze from memory exhaustion / macOS compressor saturation
- WindowServer watchdog killed display server after 40+ seconds unresponsiveness
- Practical observed limits:
  - ~5–6 agents: light tasks (file ops, git)
  - ~3–4 agents: medium tasks (builds, linting)
  - ~2 agents: heavy tasks (Whisper, large file processing)

**Proposed feature `maxParallelAgents`:** Suggested default of 5, configurable down to 1 (sequential) or up to `-1` (unlimited). Anthropic auto-closed without response.

**Practitioner reports (claudefa.st, 2025):**
- "Over-parallelizing: Launching 10 parallel agents for a simple feature wastes tokens and creates coordination overhead." — No hard cap stated, but 10+ is explicitly called out as problematic.

**Official recommendation (agent teams docs):**
- "Start with 3–5 teammates for most workflows"
- "5–6 tasks per teammate keeps everyone productive"
- "Scale up only when work genuinely benefits from simultaneous teammates. Three focused teammates often outperform five scattered ones."

**Summary on concurrency:** There is no enforced cap. The "~10-12 before degradation" user report aligns with practitioner experience but is not officially documented. The practical safe range from all evidence is:
- **3–5 concurrent subagents/teammates** for routine work
- **Up to ~10** before coordination and token overhead creates diminishing returns
- **20+** causes system stability risk on most hardware (GitHub issue data)

---

## 3. Orchestration Patterns That Work Best

### 3a. Parallel Research / Independent Domains
Most effective documented pattern. Each agent explores a non-overlapping area, reports findings, lead synthesizes.
```
Create an agent team: one on security, one on performance, one on test coverage. Have them each review PR #142.
```
Works because: agents don't write shared files, conflict probability is near zero, synthesis is the only coordination point.

### 3b. Worktree-Isolated Parallel Implementation
Each subagent (or teammate) works in its own git worktree. No file-write conflicts possible. Used by incident.io (4–5 parallel agents routinely).

Implementation: `isolation: worktree` in subagent frontmatter, or `claude --worktree <name>` for manual sessions.

### 3c. Sequential Chaining (Pipeline Pattern)
Planning → Implementation → Review loops where each stage's output is the next stage's input. Reduces coordination complexity vs. fully parallel architectures.
```
Use the code-reviewer subagent to find issues, then use the optimizer subagent to fix them.
```

### 3d. Context Isolation for High-Volume Operations
Delegate operations that produce massive output (test runs, log processing, large codebase scans) to subagents. The verbose output stays in the subagent's 200K context; only a summary returns to the main conversation.

### 3e. Writer/Reviewer Separation
Session A writes code; Session B reviews from a clean context (no bias from implementation). This is explicitly recommended in best practices docs.

### 3f. Competitive Hypothesis Testing
Multiple agents assigned to investigate competing explanations for a bug, with explicit instructions to challenge each other's theories. The surviving theory is more likely to be correct (Anthropic's stated rationale for this pattern).

### 3g. Fan-Out via CLI Loop
For large migrations (1,000+ files), bash loop calling `claude -p` per file with `--allowedTools` scoped for safety:
```bash
for file in $(cat files.txt); do
  claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)"
done
```

### 3h. Subagent-as-Context-Fence
Subagents for investigation that preserves main context:
```
Use subagents to investigate how our authentication system handles token refresh, and whether we have existing OAuth utilities I should reuse.
```
Subagent explores, reads files, reports summary. Main context stays clean for implementation.

---

## 4. Patterns That Fail or Degrade

### 4a. Same-File Concurrent Edits
Two agents editing the same file causes overwrites. Agent teams have no file-level locking — it's design-level responsibility to partition files. Worktree isolation sidesteps this but requires manual merge.

### 4b. Sequential Tasks Forced into Parallel
Tasks with dependencies (B needs output from A) break when parallelized. The system has no dependency graph at the task content level — only at the task list level in agent teams.

### 4c. Context Window Saturation
Degradation begins at roughly 60% context utilization (practitioner reports). The "lost in the middle" effect (Liu et al., 2023) is observable: models favor tokens at context start and end; middle tokens are recalled less reliably. For multi-agent workflows, this means:
- Main agent context accumulates every subagent result — runs out faster with many agents
- Each subagent starting with a bloated CLAUDE.md or skill files consumes its budget before useful work

### 4d. Spawning Too Many Agents Without Resource Awareness
No built-in throttling. 20+ agents on resource-constrained hardware (VPS, small servers) causes system-level failures. No `maxParallelAgents` setting exists (feature request closed without response).

### 4e. Nested Delegation
Subagents cannot spawn other subagents. Attempting nested delegation silently fails or produces unexpected behavior. The docs state this explicitly.

### 4f. Resumption After Team Session Interruption
`/resume` and `/rewind` do not restore in-process teammates. The lead may attempt to message non-existent teammates. Known limitation — requires manually spawning replacement teammates.

### 4g. Agent Teams on Non-tmux Terminals
Split-pane mode requires tmux or iTerm2. VS Code integrated terminal, Windows Terminal, and Ghostty are not supported. In-process mode works everywhere but is harder to monitor.

### 4h. Task Status Lag
In agent teams, teammates sometimes fail to mark tasks completed, blocking dependent tasks. Requires manual intervention or nudging via lead.

### 4i. One Team Per Session
A lead can only manage one team at a time. No parallel multi-team architectures from a single lead.

### 4j. Prompt Drift / Non-Determinism
Changing one subagent's prompt causes ripple effects across the workflow. Agent definitions should be version-controlled and treated like code.

---

## 5. Claude Agent SDK — Capabilities and Constraints

### Capabilities
- Same agent loop and tools that power Claude Code, accessible programmatically
- Python: `claude_agent_sdk`; TypeScript: `@anthropic-ai/claude-agent-sdk`
- Available cloud backends: Anthropic API, Amazon Bedrock (`CLAUDE_CODE_USE_BEDROCK=1`), Google Vertex AI (`CLAUDE_CODE_USE_VERTEX=1`), Microsoft Azure (`CLAUDE_CODE_USE_FOUNDRY=1`)
- Built-in tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, AskUserQuestion
- Session persistence and resume: capture `session_id` from `init` message, pass as `resume`
- Programmatic hooks: `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, etc.
- Inline subagent definitions via `AgentDefinition` / `agents` dict
- MCP server configuration
- Filesystem-based config via `settingSources: ['project']` (loads CLAUDE.md, skills, slash commands)
- Skills (`context: fork` for subagent injection), plugins

### Constraints
- The SDK is Claude Code running as a library — it has the same concurrency limitations as the CLI
- No built-in rate limiting or `maxParallelAgents` configuration
- Third-party API providers cannot offer `claude.ai` login or rate limits for SDK-built products — API key auth only
- `Agent` must be in `allowedTools` for subagent spawning; omitting it prevents any delegation
- Subagents spawned via SDK also cannot spawn subagents (same nesting constraint)
- Session transcripts stored at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`, cleaned up after `cleanupPeriodDays` (default: 30)
- Cannot brand SDK-built products as "Claude Code" — must maintain own branding

---

## 6. Context Window and Concurrency Issues

### Context Window Size
Claude 3.x and 4.x models have 200K token context windows. Each subagent and teammate gets its own 200K window — this is one of the primary advantages of the multi-agent architecture.

### Auto-Compaction
Triggers at approximately 95% context capacity by default. Override with `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (e.g., `50` for earlier triggering). Compaction events logged in subagent transcripts with `preTokens` metadata.

### Practical Context Issues Reported

**Context rot in CLAUDE.md / skills:**
- Performance degrades significantly when CLAUDE.md or skill files are too long
- Recommended max: ~2,000–3,000 tokens per skill file
- Bloated files cause: attention dilution, instruction conflicts, token budget compression before work starts

**Main context accumulation:**
- Each subagent result returned to main context — running many subagents that return detailed results consumes main context fast
- Mitigation: instruct subagents to return summaries, not full outputs; use `background: true` for fire-and-forget tasks

**"Lost in the Middle" degradation:**
- At <50% context fill: information in middle of context is recalled less reliably
- At >50% fill: earliest tokens begin getting lost
- Practical threshold for noticeable quality degradation: ~60% utilization

**Token burn rate:**
- 3 active subagents = 3–4x more tokens than single-threaded session
- Agent teams: token usage scales linearly with active teammate count; each has its own 200K window
- Practitioners report "hitting API rate limits" at aggressive parallel execution (Zach Wills, 2025)
- Running 3 concurrent Claude Max accounts was reported as necessary for intensive multi-agent work by one practitioner (Shipyard.build, 2026)

---

## 7. Third-Party Plugins, Extensions, and Frameworks

### Official Plugin System
Claude Code has a native plugin system distributing skills, subagents, hooks, and MCP servers as installable units. Plugin subagents do NOT support `hooks`, `mcpServers`, or `permissionMode` frontmatter (security restriction). Browse via `/plugin` in Claude Code.

### VoltAgent Awesome Collections
- [`awesome-claude-code-subagents`](https://github.com/VoltAgent/awesome-claude-code-subagents) — 100+ specialized subagents
- [`awesome-agent-skills`](https://github.com/VoltAgent/awesome-agent-skills) — 1000+ skills compatible with Claude Code and other agents

### ccswarm (nwiizo)
Rust-native multi-agent coordination system with Git worktree isolation and specialized agent pools (Frontend, Backend, DevOps, QA). Task delegation infrastructure with template-based scaffolding.
- GitHub: https://github.com/nwiizo/ccswarm

### Multiclaude (Dan Lorenc)
Supervisor agent assigns tasks to subagents. Two modes: "singleplayer" (auto-merge) and "multiplayer" (team review). Better for long-running tasks with less real-time oversight.

### Ruflo (ruvnet)
Enterprise-grade orchestration platform. Distributed swarm intelligence, RAG integration, native Claude Code/Codex integration.
- GitHub: https://github.com/ruvnet/ruflo

### Claude Squad
Terminal application managing multiple AI coding agents (Claude Code, Aider, Codex, OpenCode, Amp) in separate workspaces with Git worktree isolation. 5.8k GitHub stars as of early 2026.

### oh-my-claudecode
Zero-config orchestration layer, trending on GitHub. Claimed 3–5x speedup and 30–50% token cost reduction on large projects.

### barkain/claude-code-workflow-orchestration
Plugin for multi-step workflow orchestration — automatic task decomposition, parallel agent execution, specialized agent delegation with native plan mode integration.
- GitHub: https://github.com/barkain/claude-code-workflow-orchestration

### mbruhler/claude-orchestration
Multi-agent workflow orchestration plugin for Claude Code.
- GitHub: https://github.com/mbruhler/claude-orchestration

### hesreallyhim/awesome-claude-code
Curated list of skills, hooks, slash commands, agent orchestrators, applications, and plugins.
- GitHub: https://github.com/hesreallyhim/awesome-claude-code

### Parallel Worktrees Skill
- GitHub: https://github.com/spillwavesolutions/parallel-worktrees

### /batch Built-In Skill
Announced Feb 27, 2026 (Boris Cherny). Ships with Claude Code. Spins up worktree-isolated agents for large-scale parallel code migrations.

---

## 8. Practitioner Reports (2025–2026)

### Incident.io
Routinely runs 4–5 parallel Claude agents; worktree isolation is the enabling pattern.
Source: Upsun Developer Center / Shipyard.build, 2026.

### Zach Wills (2025)
Parallelized development workflow with a "core trio" of specialist agents (product-manager, ux-designer, senior-software-engineer) dispatched simultaneously. Key findings:
- Agents hit API rate limits — confirming genuinely concurrent execution
- Token consumption accelerates dramatically with parallel agents
- Synthesis ("reduce") step is the hardest part — mitigation: each agent writes distinct output files for audit trail

### Shipyard.build Practitioner Survey (2026)
- Practitioners "hit usage limits really quickly" with multi-agent work
- One expert ran 3 concurrent Claude Max accounts to maintain needed pace
- Patterns catalogued: Agent Teams (official), Gas Town (Steve Yegge — hierarchical mayor model), Multiclaude (Dan Lorenc — supervisor/subagent)
- "Don't make sense for 95% of agent-assisted development tasks" — reserved for complex, genuinely parallel work

### GitHub Issue #15487 Community (Dec 2025 – Mar 2026)
- Primary data source for concurrency limits (see Section 2)
- Frustration with Anthropic's non-response to stability issue
- Issue auto-closed, locked, no official engagement

### Blake Crosley (2025 — 50 sessions analysis)
- Quality degradation at ~60% context window utilization
- Solutions that help across multi-hour sessions: proactive compaction after each subtask, filesystem-based memory across context boundaries, subagent delegation to keep main context lean

### Addy Osmani (2025 — "The Code Agent Orchestra")
- "Coordination overhead increases with team size"
- "Diminishing returns: beyond a certain point, additional teammates don't speed up work proportionally"
- Recommends starting with research/review tasks before parallel implementation

---

## Key Conclusions

1. **No enforced concurrency cap exists.** The safe practical range is 3–5 concurrent agents. 10+ introduces coordination overhead and token burn that often negates the benefit. 20+ risks system stability.

2. **Context isolation is the primary value proposition** of multi-agent architectures — not raw speed. Each subagent/teammate gets a fresh 200K window, preventing context rot from accumulating in a single long session.

3. **File-write conflicts are the primary coordination hazard.** The `isolation: worktree` frontmatter field is the most important mitigation for any agent that writes files.

4. **Subagents cannot spawn subagents.** Agent teams allow peer-to-peer coordination but are still experimental with known limitations.

5. **Context rot is real and measurable.** CLAUDE.md and skill file bloat, plus accumulated subagent results in the main context, are the primary causes. Keep skill files under 2,000–3,000 tokens.

6. **The Agent SDK enables programmatic orchestration** with the same primitives as the CLI, but has no built-in throttling. Production SDK usage requires explicit resource management.

7. **Third-party frameworks exist** (ccswarm, Multiclaude, Ruflo, Claude Squad) but the native primitives (worktree isolation, agent teams, subagents with `isolation: worktree`) cover most patterns without external dependencies.

---

## Sources

- [Claude Code: Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams)
- [Claude Code: Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code: Common workflows (worktrees, /batch)](https://code.claude.com/docs/en/common-workflows)
- [Claude Code: Best Practices](https://code.claude.com/docs/en/best-practices)
- [Claude Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview)
- [GitHub Issue #15487: Add maxParallelAgents Configuration Setting](https://github.com/anthropics/claude-code/issues/15487)
- [Shipyard.build: Multi-agent orchestration for Claude Code in 2026](https://shipyard.build/blog/claude-code-multi-agent/)
- [Shipyard.build: Claude Code Subagents Quickstart](https://shipyard.build/blog/claude-code-subagents-guide/)
- [Zach Wills: How to Use Claude Code Subagents to Parallelize Development](https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/)
- [claudefa.st: Claude Code Sub-Agents Parallel vs Sequential Patterns](https://claudefa.st/blog/guide/agents/sub-agent-best-practices)
- [MindStudio: Context Rot in Claude Code Skills](https://www.mindstudio.ai/blog/context-rot-claude-code-skills-bloated-files)
- [Towards AI: Git Worktree Isolation in Claude Code](https://pub.towardsai.net/git-worktree-isolation-in-claude-code-parallel-development-without-the-chaos-262e12b85cc5)
- [Upsun Developer Center: Git worktrees for parallel AI coding agents](https://devcenter.upsun.com/posts/git-worktrees-for-parallel-ai-coding-agents/)
- [GitHub: nwiizo/ccswarm](https://github.com/nwiizo/ccswarm)
- [GitHub: ruvnet/ruflo](https://github.com/ruvnet/ruflo)
- [GitHub: hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [GitHub: VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [GitHub: barkain/claude-code-workflow-orchestration](https://github.com/barkain/claude-code-workflow-orchestration)
- [Blake Crosley: Context Window Management — 50 Sessions](https://blakecrosley.com/blog/context-window-management)
- [Addy Osmani: The Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/)
