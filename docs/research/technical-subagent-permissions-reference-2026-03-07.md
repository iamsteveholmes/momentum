# Claude Code Subagent Permissions & Configuration Reference

**Date:** 2026-03-07
**Researcher:** Mary (Business Analyst Agent)
**Status:** Complete
**Related:** [Agentic Architecture: BMAD vs Claude Code](./technical-agentic-architecture-bmad-vs-claude-code-2026-03-07.md)

---

## Subagent Resolution: How Names Map to Agents

When Claude calls `Agent(subagent_type="something")`, resolution follows this priority:

| Priority | Source | Location |
|----------|--------|----------|
| 1 (highest) | CLI flag | `claude --agents '{"name":"x","description":"...","prompt":"..."}'` |
| 2 | Project agents | `.claude/agents/**/*.md` |
| 3 | User agents | `~/.claude/agents/**/*.md` |
| 4 | Plugin agents | Plugin's `agents/` directory |

Resolution matches the **`name` field in YAML frontmatter**, not the filename. A file named `code-reviewer.md` with `name: my-reviewer` is invoked as `Agent(subagent_type="my-reviewer")`.

When duplicates exist across scopes, the higher-priority location wins.

---

## Agent Definition File Schema

Claude Code native agents are Markdown files with YAML frontmatter:

```yaml
---
name: my-agent                    # Required. Unique ID (lowercase, hyphens, max 64 chars)
description: What this agent does # Required. Claude reads this to decide when to delegate
tools: Read, Grep, Glob          # Optional. Tool allowlist (empty = inherit all)
disallowedTools: Write, Edit     # Optional. Tool denylist
model: sonnet                    # Optional. sonnet | opus | haiku | inherit (default: inherit)
permissionMode: plan             # Optional. default | acceptEdits | dontAsk | bypassPermissions | plan
maxTurns: 10                     # Optional. Max agentic turns before stopping
skills:                          # Optional. Skills to preload into agent context
  - skill-name
mcpServers:                      # Optional. MCP servers available to this agent
  - server-name
hooks:                           # Optional. Lifecycle hooks
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./validate.sh"
memory: project                  # Optional. Persistent memory scope: user | project | local
background: false                # Optional. Always run in background
isolation: worktree              # Optional. Run in isolated git worktree
---

System prompt for the agent goes here in markdown.
This is the ONLY context the agent gets (plus CLAUDE.md auto-load).
```

---

## Per-Agent Tool Permissions

### How Tool Inheritance Works

```
Session permissions (settings.local.json)
  └── Agent's tools: field (subtractive allowlist)
       └── Agent's disallowedTools: field (additional denials)
            └── Session deny rules still apply
```

**Key principle:** Agents can only **restrict** capabilities, never **grant** ones the parent session doesn't have.

### Examples

**Unrestricted agent (inherits everything):**
```yaml
---
name: general-worker
description: General-purpose task handler
tools:
---
```

**Read-only research agent:**
```yaml
---
name: researcher
description: Conducts research without modifying files
tools: Read, Grep, Glob, WebFetch, WebSearch
---
```
This agent CANNOT use Edit, Write, or Bash even though your session allows them.

**Agent that can edit but not delete:**
```yaml
---
name: safe-editor
description: Makes code changes safely
tools: Read, Grep, Glob, Edit, Write, Bash
disallowedTools: Bash(rm:*), Bash(git push:*)
---
```

**Agent with restricted subagent spawning:**
```yaml
---
name: coordinator
description: Coordinates specialized workers
tools: Agent(researcher, analyzer), Read, Bash
---
```
Can only spawn agents named `researcher` and `analyzer`.

---

## Subagent Context & Isolation

### What Subagents Receive

| Context | Received? | Notes |
|---------|-----------|-------|
| Parent conversation history | No | Completely isolated |
| Project CLAUDE.md files | Yes | Auto-discovered from working directory |
| Parent's BMAD persona | No | Only their own markdown body |
| Parent's MCP servers | Only if configured | Via `mcpServers:` field |
| Preloaded skills | Only if configured | Via `skills:` field |
| Tool permissions | Inherited + restricted | Cannot exceed parent |
| Working directory | Yes | Same as parent |

### What Subagents Cannot Do

- Spawn other subagents (no nesting — hard constraint)
- Execute slash commands (/bmad-*, /help, etc.)
- Access parent conversation state
- Modify session configuration
- Show interactive menus or prompts to the user

---

## Subagent Nesting: The Hard Constraint

**Subagents cannot spawn other subagents.** This is a hard limitation in Claude Code.

Only agents running as the **main thread** (via `claude --agent <name>`) can spawn subagents. All subagents spawned by the Agent tool are terminal — they do work and return results, period.

**If you need nested delegation:**
- Chain subagents sequentially from the main conversation
- Use Skills to inject reusable prompts into a single context
- Have the BMAD agent (running in your main session) orchestrate multiple workers

---

## How Claude Decides Which Subagent to Use

Claude uses **semantic matching** against the `description` field:

1. A task is described (either by you or by a BMAD workflow)
2. Claude reads all available agent descriptions
3. Claude matches the task semantically to the best-fit agent
4. If no match, falls back to built-in agents (Explore for read-only, general-purpose for complex tasks)

**Tips for better matching:**
- Make descriptions specific: "Conducts market research and competitive analysis" beats "Does research"
- Include trigger phrases: "use PROACTIVELY when gathering market insights"
- The description is the primary signal — make it count

---

## Built-in Agent Types

| Type | Model | Tools | Purpose |
|------|-------|-------|---------|
| `Explore` | Haiku | Read-only (no Write/Edit) | Fast codebase search and analysis |
| `Plan` | Inherits | Read-only (no Write/Edit) | Architecture planning |
| `general-purpose` | Inherits | All tools | Complex multi-step tasks |
| `claude-code-guide` | Haiku | Read, WebFetch, WebSearch | Claude Code feature questions |
| `statusline-setup` | Sonnet | Read, Edit | Status line configuration |

---

## Your Current Native Agents (Installed by BMAD)

### Analysis Agents (`.claude/agents/bmad-analysis/`)

| Agent | Name | Purpose |
|-------|------|---------|
| data-analyst.md | `bmm-data-analyst` | Quantitative analysis, market sizing, metrics |
| api-documenter.md | `bmm-api-documenter` | API and interface documentation |
| codebase-analyzer.md | `bmm-codebase-analyzer` | Project structure and architecture analysis |
| pattern-detector.md | `bmm-pattern-detector` | Architectural and design pattern identification |

### Research Agents (`.claude/agents/bmad-research/`)

| Agent | Name | Purpose |
|-------|------|---------|
| tech-debt-auditor.md | `bmm-tech-debt-auditor` | Technical debt identification and assessment |
| market-researcher.md | `bmm-market-researcher` | Market research and competitive analysis |

### Review Agents (`.claude/agents/bmad-review/`)

| Agent | Name | Purpose |
|-------|------|---------|
| test-coverage-analyzer.md | `bmm-test-coverage-analyzer` | Test suite and coverage analysis |
| technical-evaluator.md | `bmm-technical-evaluator` | Technology choice evaluation |
| document-reviewer.md | `bmm-document-reviewer` | Document quality validation |

### Planning Agents (`.claude/agents/bmad-planning/`)

| Agent | Name | Purpose |
|-------|------|---------|
| user-journey-mapper.md | `bmm-user-journey-mapper` | User journey and touchpoint mapping |
| requirements-analyst.md | `bmm-requirements-analyst` | Requirements analysis and refinement |
| user-researcher.md | `bmm-user-researcher` | User research and persona development |
| epic-optimizer.md | `bmm-epic-optimizer` | Epic boundary and scope optimization |
| technical-decisions-curator.md | `bmm-technical-decisions-curator` | Technical decision documentation |
| dependency-mapper.md | `bmm-dependency-mapper` | Module and package dependency analysis |
| trend-spotter.md | `bmm-trend-spotter` | Emerging trend identification |

**Current state:** All have `tools:` empty (no restrictions). They inherit all permissions from your session.

---

## Agent Resumption

Each subagent invocation gets a unique **agent ID**. You can resume a completed agent to continue its work:

```
Agent(resume="a23c62df961beff05", prompt="Now also analyze the auth module")
```

Resumed agents retain:
- Full conversation history (messages, tool calls, results)
- Previous reasoning and state
- Same system prompt and configuration
- Same persona (if one was in the markdown body)

Transcripts are stored at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl` and cleaned up after 30 days.

---

## Practical Configuration Recommendations

### For Read-Only Research Agents

```yaml
---
name: bmm-market-researcher
description: Conducts comprehensive market research...
tools: Read, Grep, Glob, WebFetch, WebSearch
---
```
Prevents accidental file modifications during research.

### For Code Analysis Agents

```yaml
---
name: bmm-codebase-analyzer
description: Performs comprehensive codebase analysis...
tools: Read, Grep, Glob, Bash
disallowedTools: Bash(rm:*), Bash(git:*)
---
```
Can run commands for analysis but can't delete files or touch git.

### For Document Writers

```yaml
---
name: bmm-document-reviewer
description: Reviews and validates product documentation...
tools: Read, Grep, Glob, Edit, Write
disallowedTools: Bash
---
```
Can read and write docs but can't execute commands.
