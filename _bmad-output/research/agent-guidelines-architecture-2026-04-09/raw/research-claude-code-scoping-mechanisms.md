---
content_origin: claude-code-subagent
date: 2026-04-09
sub_question: "What Claude Code mechanisms most effectively scope guidelines to specific agent roles — CLAUDE.md hierarchy, paths: frontmatter rules, subagent system prompts, worktree isolation — and what are their tradeoffs across all role types?"
topic: "Agent-specific guidelines architecture in Claude Code"
---

# Claude Code Scoping Mechanisms for Agent-Specific Guidelines

## Executive Summary

Claude Code offers four distinct mechanisms for scoping behavioral guidelines to specific agent roles: the CLAUDE.md file hierarchy, path-scoped `.claude/rules/` files, subagent system prompts (via `.claude/agents/` markdown files), and worktree isolation. These mechanisms differ sharply in what they actually deliver to a subagent's context window. The critical finding for any agent-guidelines redesign: **subagents do NOT automatically inherit CLAUDE.md or rules files from the parent session**. The only reliable channel from parent to subagent is the Agent tool's prompt string, the subagent's own markdown body (its system prompt), and any `skills` explicitly listed in subagent frontmatter.

---

## 1. CLAUDE.md File Hierarchy: Load Order and Cascade Behavior

### How the cascade works

Claude Code reads CLAUDE.md files by walking up the directory tree from the current working directory, concatenating all discovered files into context. If you run Claude Code in `foo/bar/`, it loads `foo/bar/CLAUDE.md`, `foo/CLAUDE.md`, and any CLAUDE.local.md files alongside them. All discovered files are concatenated rather than overriding each other ([Official docs: memory.md](https://code.claude.com/docs/en/memory.md)) [OFFICIAL].

The full resolution order, from broadest to most specific:

| Scope | Location | Notes |
|---|---|---|
| Managed policy | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | Cannot be excluded; always loads |
| User | `~/.claude/CLAUDE.md` | All projects on the machine |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared via version control |
| Local | `./CLAUDE.local.md` | Personal, gitignored |
| Subdirectory | `./subdir/CLAUDE.md` | Loaded **on demand**, not at launch |

The key distinction for agentic workflows: files at or above the working directory are loaded at session launch. Files in subdirectories are loaded **lazily**, triggered only when Claude reads files in those subdirectories.

### What subdirectory CLAUDE.md files actually do

Subdirectory CLAUDE.md files are NOT loaded at startup. They are included when Claude reads files in those subdirectories during a session. This means a `src/api/CLAUDE.md` file will load only if Claude opens a file under `src/api/` — not proactively, and not based on the task description alone ([Official docs: memory.md](https://code.claude.com/docs/en/memory.md)) [OFFICIAL].

The `InstructionsLoaded` hook (added in v2.1.69) fires when CLAUDE.md or rules files are loaded, enabling debug logging of exactly which files load and when ([Hooks reference](https://code.claude.com/docs/en/hooks)) [OFFICIAL].

### Do subagents inherit the parent's CLAUDE.md?

This is the critical question. **The answer is context-dependent and partially conditional.** According to the official SDK subagents documentation, a subagent receives:

- Its own system prompt (the markdown body of its agent file)
- The Agent tool's prompt string (what the parent passes to it)
- Project CLAUDE.md — **only when loaded via `settingSources`**
- Tool definitions

A subagent does NOT receive the parent's conversation history, prior tool results, or the parent's system prompt ([Official SDK subagents docs](https://platform.claude.com/docs/en/agent-sdk/subagents)) [OFFICIAL].

The important nuance: in the interactive CLI, project CLAUDE.md **does load for subagents** because the working directory is set and the session sources are inherited. In the SDK, CLAUDE.md requires explicit `settingSources: ['project']` to load, and the `claude_code` system prompt preset alone is insufficient. This is a documented gotcha that trips SDK users ([SDK modifying-system-prompts docs](https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts.md)) [OFFICIAL].

A community-filed feature request (GitHub issue #8395, closed January 2026 as "not planned") confirmed that automatic rule propagation from parent agents to subagents is **not supported** and not on the roadmap. The issue documented that subagents "operate in isolation with their own system prompts" and that there is "no mechanism for user-level instruction files" that propagate to subagents ([GitHub issue #8395](https://github.com/anthropics/claude-code/issues/8395)) [PRAC].

### Tradeoffs

| Strength | Weakness |
|---|---|
| Zero configuration — loads automatically for main sessions | Subagents in the SDK require explicit `settingSources` opt-in |
| Hierarchical: global → project → subdirectory | Subdirectory files load lazily, not predictably for role-scoping |
| Supports `@import` for modular content | Over 200 lines degrades adherence |
| Team-shareable via version control | No role-targeting — same content loads for all agent types |

---

## 2. Path-Scoped `.claude/rules/` Files

### How `paths:` frontmatter works

Rules files in `.claude/rules/` support YAML frontmatter with a `paths` field. A rule with `paths` frontmatter activates only when Claude is working with files matching the specified glob pattern(s):

```yaml
---
paths:
  - "src/api/**/*.ts"
---
# API Development Rules
- All endpoints must include input validation
```

Rules without a `paths` field are loaded unconditionally at session launch with the same priority as `.claude/CLAUDE.md`. Path-scoped rules trigger when Claude reads a matching file, not on every tool use ([Official docs: memory.md](https://code.claude.com/docs/en/memory.md)) [OFFICIAL].

Support for this feature was introduced in Claude Code 2.0.64. Multiple path patterns and brace expansion are supported:

```yaml
---
paths:
  - "src/**/*.{ts,tsx}"
  - "tests/**/*.test.ts"
---
```

User-level rules at `~/.claude/rules/` are loaded before project rules, giving project rules higher priority for overrides. Symlinks in `.claude/rules/` are supported for sharing rules across projects ([claudefa.st rules directory guide](https://claudefa.st/blog/guide/mechanics/rules-directory)) [PRAC].

### What `paths:` scoping does NOT do

Path-scoped rules are triggered by file access patterns, not by agent role or task type. They are designed for **domain/language scoping** (TypeScript files, API directories, test files), not for **agent role scoping** (dev agent vs QA agent vs PM agent). There is no mechanism to say "load this rule only when the dev subagent is running" ([paddo.dev path-specific rules](https://paddo.dev/blog/claude-rules-path-specific-native/)) [PRAC].

Additional limitations documented by the community:
- No explicit invocation: you cannot force a rule to load when file patterns don't match
- No disable flags: cannot skip a rule during a session
- No invocation logging without the `InstructionsLoaded` hook

### Do subagents inherit rules files?

Based on official documentation and community investigation: when a subagent runs in the interactive CLI with the same working directory, global (no-paths) rules files **do load** alongside CLAUDE.md. Path-scoped rules **would load** if the subagent reads matching files. However, in the SDK context, explicit `settingSources` configuration is required. The community GitHub issue #8395 found that whether CLAUDE.md (and by extension rules files) is even available to subagents was "undocumented" at the time of investigation (September 2025) [PRAC].

### Tradeoffs

| Strength | Weakness |
|---|---|
| Reduces context bloat — domain rules only load when relevant | Scopes by file type, not by agent role |
| Modular — one topic per file, easy team maintenance | Cannot target a specific subagent type |
| Symlink support for cross-project sharing | No invocation control within a session |
| User-level rules for personal preferences across projects | Path matching triggers on file access, may not fire for planning-only agents |

---

## 3. Subagent System Prompts — The Primary Role-Scoping Mechanism

### How subagent system prompts work

Subagents defined in `.claude/agents/` (project scope) or `~/.claude/agents/` (user scope) receive their markdown body as a custom system prompt. This is a complete replacement of the default Claude Code system prompt, not a supplement to it:

> "Subagents receive only this system prompt (plus basic environment details like working directory), not the full Claude Code system prompt." — ([Custom subagents docs](https://code.claude.com/docs/en/sub-agents.md)) [OFFICIAL]

This is the most reliable and powerful mechanism for scoping role-specific guidelines. The system prompt body is completely under the author's control and is always delivered — no cascade, no lazy loading, no path matching required.

Key frontmatter fields for role scoping:

| Field | Role-scoping use |
|---|---|
| `name` | Unique identifier; determines which subagent Claude delegates to |
| `description` | Primary routing signal — Claude reads this to decide when to delegate |
| `tools` | Allowlist constrains what the agent can do (e.g., read-only for QA review) |
| `disallowedTools` | Denylist blocks specific tools while inheriting the rest |
| `model` | Route cheap/fast tasks to Haiku, complex reasoning to Opus |
| `skills` | Pre-load skill content into the subagent's context at startup |
| `permissionMode` | Control whether the subagent auto-accepts edits, prompts, or bypasses |
| `isolation` | Set to `worktree` for file-system isolation during parallel execution |
| `memory` | Enable persistent cross-session memory for the agent role |
| `hooks` | Lifecycle hooks scoped to this subagent only |

([Custom subagents docs](https://code.claude.com/docs/en/sub-agents.md)) [OFFICIAL]

### The `skills` field — best mechanism for injecting guidelines

The `skills` frontmatter field is the cleanest mechanism for the **generic-agent + injected-guidelines = specialized-agent** pattern. When listed in a subagent's frontmatter:

> "The full content of each skill is injected into the subagent's context, not just made available for invocation. Subagents don't inherit skills from the parent conversation; you must list them explicitly." — ([Custom subagents docs](https://code.claude.com/docs/en/sub-agents.md)) [OFFICIAL]

This means a skill file can serve as a reusable guidelines payload — maintained once, injected into any subagent that needs it. Example:

```yaml
---
name: dev-agent
description: Implements story tasks following project coding standards
skills:
  - typescript-conventions
  - testing-standards
  - git-workflow
---

You are a senior software engineer. Implement the assigned story following the conventions in your preloaded skills.
```

The skill content is injected as part of the subagent's startup context, giving it domain-specific guidelines without duplicating them in the agent file itself. This is bidirectionally documented: `skills` in a subagent definition loads skill content; `context: fork` in a skill file injects the skill into an agent you specify ([Sub-agents docs: preload skills](https://code.claude.com/docs/en/sub-agents.md)) [OFFICIAL].

### Subagent scope priority

When multiple subagents share the same name, the higher-priority source wins:

1. Managed settings (highest)
2. `--agents` CLI flag (session only)
3. `.claude/agents/` (project)
4. `~/.claude/agents/` (user)
5. Plugin's `agents/` directory (lowest)

Project subagents are discovered by walking up from the current working directory. Directories added with `--add-dir` grant file access only — they are not scanned for subagents ([Custom subagents docs](https://code.claude.com/docs/en/sub-agents.md)) [OFFICIAL].

### Propagating guidelines via the Agent tool prompt

Since the Agent tool's prompt string is the only guaranteed channel from orchestrator to subagent, it can be used to inject dynamic, per-invocation guidelines alongside the task description:

```
Implement the authentication story. Follow these constraints for this task:
- Use existing middleware patterns in src/middleware/
- Do not modify database schema
- Test coverage must include the happy path and auth-failure cases
```

This pattern keeps the subagent definition generic while the orchestrator injects context-specific guidance at call time. The tradeoff: this content is ephemeral — it lives only in that invocation, not in the subagent's persistent definition ([SDK subagents docs](https://platform.claude.com/docs/en/agent-sdk/subagents)) [OFFICIAL].

### Tradeoffs

| Strength | Weakness |
|---|---|
| Most reliable delivery — always in context, no loading conditions | Subagent does NOT inherit parent CLAUDE.md by default in SDK |
| Complete control over system prompt content | CLAUDE.md from interactive CLI does load alongside the subagent system prompt |
| `skills` field enables reusable guidelines payload | Subagent system prompts are opaque — no /memory visibility into them |
| Tool restrictions enforce role boundaries structurally | Updating role guidelines requires editing each subagent file |
| Per-role model routing (haiku for cheap tasks, opus for complex) | No automatic propagation — must list all skills explicitly |

---

## 4. Worktree Isolation — File System Scoping, Not Guidelines Scoping

### What worktree isolation actually does

The `isolation: worktree` frontmatter field and the `--worktree` CLI flag create a separate git working directory for the agent. Each worktree has its own files and branch while sharing the same repository history. Subagents with `isolation: worktree` run in complete isolation and their worktrees are automatically cleaned up if no changes are made ([Common workflows docs](https://code.claude.com/docs/en/common-workflows)) [OFFICIAL].

### Does worktree isolation change which guidelines load?

Worktrees are created at `<repo>/.claude/worktrees/<name>`. Since they are still within the same git repository, they inherit the same `.claude/` directory structure (CLAUDE.md, rules, agents files). The working directory **is different** (the worktree path vs the main repo path), but since `.claude/` is part of the committed repository structure, the same project CLAUDE.md and rules files are present in the worktree.

Implication: changing the worktree directory does not meaningfully change which project-level guidelines load. The project CLAUDE.md and rules files are the same content. However, if you construct worktrees with different `.claude/` content (e.g., a specialized subproject with its own agents), the worktree directory change would result in different configuration loading.

Subdirectory CLAUDE.md files would differ if the worktree's working directory is set to a subdirectory — those files would then be in the ancestor path and load at launch rather than lazily. This is a niche mechanism, not a general-purpose role-scoping tool.

### Practical role for worktrees

Worktree isolation's value is **parallel execution without file conflicts**, not guidelines differentiation. The official recommendation is to split work so each subagent owns different files; worktrees prevent merge conflicts at execution time ([Worktree guide](https://claudefa.st/blog/guide/development/worktree-guide)) [PRAC].

For Momentum's use case (dev, QA, E2E, PM, SM, skill-dev agents running in parallel), worktree isolation is valuable for dev agents writing code in parallel, but it does not serve as a guidelines differentiation mechanism.

### Tradeoffs

| Strength | Weakness |
|---|---|
| Prevents file conflicts in parallel multi-agent workflows | Does not change which guidelines load |
| Automatic cleanup when no changes made | Adds git complexity; requires clean branch hygiene |
| `.worktreeinclude` allows copying .env and local config files | Not designed for role-scoping; designed for isolation |
| Built into subagent frontmatter as `isolation: worktree` | CLAUDE.md and rules content is identical to main repo |

---

## 5. Prompt Injection vs. File-Based Guidelines — Reliability Comparison

A core question for the agent-guidelines redesign: **when a generic agent is given role-specific instructions via prompt vs. via file, which is more reliable?**

### The delivery hierarchy

Based on official documentation, instructions are delivered through different channels with different priority characteristics:

1. **System prompt (subagent markdown body)**: highest reliability — always in context, delivered before any user message
2. **Skills injected via `skills` frontmatter**: high reliability — injected at startup as part of system context
3. **CLAUDE.md content**: medium-high reliability — delivered as a user message after the system prompt, not part of the system prompt itself
4. **Agent tool prompt string**: medium reliability — ephemeral, per-invocation, can be long and compete with task description
5. **Path-scoped rules**: conditional reliability — only loads if matching files are accessed

The official documentation states explicitly:

> "CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself. Claude reads it and tries to follow it, but there's no guarantee of strict compliance, especially for vague or conflicting instructions." — ([memory.md troubleshooting section](https://code.claude.com/docs/en/memory.md)) [OFFICIAL]

This is a critical finding: CLAUDE.md is **context**, not **enforcement**. The same is true for rules files. The subagent system prompt body, being part of the actual system prompt, has stronger adherence characteristics.

### File-based vs. prompt injection

For persistent, role-defining guidelines (the agent's identity, core constraints, domain expertise), **file-based delivery via the subagent markdown body or preloaded skills** is more reliable than prompt injection via the Agent tool call. The reasons:

- System prompt content is structurally prior to user messages — it establishes baseline behavior
- Skill content is injected as a cohesive, pre-structured block
- Prompt injection competes with the task description for attention in the same turn
- Prompt-injected guidelines are invisible to the subagent file — they cannot be audited via `/memory` or `/agents`

For **dynamic, per-task** guidance (this specific story's constraints, current sprint context), prompt injection via the Agent tool is the right mechanism — it is the only channel that can carry runtime-specific information.

The recommended architecture: **static role guidelines in the subagent file body + reusable domain knowledge in skills + dynamic task context in the Agent prompt**.

---

## 6. Patterns for All Momentum Role Types

Based on the research above, here is a role-by-role recommendation:

### Dev agent (story implementation)
- **Primary mechanism**: Subagent file body defines the engineering persona and coding standards
- **Skills injection**: Tech stack conventions, testing standards, git workflow — maintained as reusable skills
- **Worktree**: `isolation: worktree` for parallel story execution
- **Tool scope**: Full tools or Write/Edit/Bash; no restriction on read

### QA agent (test generation, review)
- **Primary mechanism**: Subagent file body defines QA persona and quality standards
- **Skills injection**: ATDD conventions, framework-specific patterns, coverage thresholds
- **Tool scope**: Read-only tools for review; Bash + Write for test generation
- **CLAUDE.md role**: CLAUDE.md project context loads alongside (in CLI) but subagent body takes precedence

### E2E agent (end-to-end testing)
- **Primary mechanism**: Subagent file body defines E2E persona (Playwright, behavior-first, etc.)
- **Skills injection**: Playwright conventions, test patterns, selector strategies
- **MCP scope**: `mcpServers` field can scope browser/Playwright MCP tools to this agent only
- **Tool scope**: Bash + Read for execution; restrict Write to test files only

### PM agent (story creation, PRD)
- **Primary mechanism**: Subagent file body defines PM persona; no code tools
- **Tool scope**: Read, Grep, Glob only — no Write/Edit/Bash
- **Skills injection**: Story template, acceptance criteria standards
- **Memory**: `memory: project` to accumulate product decisions across sessions

### SM agent (sprint planning, coordination)
- **Primary mechanism**: Subagent file body defines orchestration rules
- **Tool scope**: Read + Bash (for git/sprint tooling) + Agent (to spawn subagents)
- **Agent spawning**: `Agent(dev-agent, qa-agent)` in tools field to restrict which agents SM can spawn

### Skill-dev agent (creates new skills)
- **Primary mechanism**: Subagent file body defines skill authoring conventions
- **Skills injection**: Skill structure standards, frontmatter conventions
- **Tool scope**: Write + Edit + Read; no Bash unless testing skills

---

## 7. Key Limitations and Open Issues

**No automatic rule propagation from parent to subagents**: GitHub issue #8395, filed September 2025 and closed January 2026 as "not planned," confirmed that rules do not automatically cascade from CLAUDE.md or user-level rules files to subagents. Each subagent must be independently configured with its needed guidelines [PRAC].

**CLAUDE.md adherence is probabilistic**: The official documentation explicitly states CLAUDE.md instructions are "context, not enforced configuration" — Claude reads and tries to follow them without strict compliance guarantees, especially for vague or conflicting instructions [OFFICIAL].

**Subagents cannot spawn subagents**: Subagents cannot use the Agent tool to spawn further subagents. Hierarchical delegation requires the orchestrator to remain the top-level spawner [OFFICIAL].

**`paths:` scoping is file-type based, not role-based**: There is no path-based mechanism to route guidelines to a specific agent type by name. Path scoping serves language/domain separation, not agent-role separation [OFFICIAL].

**SDK requires explicit `settingSources` for CLAUDE.md**: In programmatic SDK usage, CLAUDE.md does not load unless `settingSources: ['project']` is explicitly set. This is a footgun for SDK-based agent orchestration systems like Momentum's Impetus [OFFICIAL].

---

## Sources

- [How Claude remembers your project (memory.md)](https://code.claude.com/docs/en/memory.md) — Official documentation, CLAUDE.md hierarchy, rules, path-scoped rules [OFFICIAL]
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents.md) — Official documentation, subagent configuration, skills injection, worktree isolation, system prompt behavior [OFFICIAL]
- [Subagents in the SDK](https://platform.claude.com/docs/en/agent-sdk/subagents) — Official SDK documentation, what subagents inherit, programmatic definition [OFFICIAL]
- [Modifying system prompts](https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts.md) — Official SDK documentation, system prompt methods, settingSources requirement for CLAUDE.md [OFFICIAL]
- [Common workflows — worktrees](https://code.claude.com/docs/en/common-workflows) — Official documentation, worktree isolation for subagents [OFFICIAL]
- [Hooks reference](https://code.claude.com/docs/en/hooks) — Official documentation, InstructionsLoaded hook for debugging rules loading [OFFICIAL]
- [Claude Code settings](https://code.claude.com/docs/en/settings) — Official documentation, scope system [OFFICIAL]
- [Claude Code Rules Directory: Modular Instructions That Scale](https://claudefa.st/blog/guide/mechanics/rules-directory) — Practitioner guide, paths: frontmatter mechanics [PRAC]
- [Claude Code Gets Path-Specific Rules](https://paddo.dev/blog/claude-rules-path-specific-native/) — Practitioner analysis, limitations of paths: scoping [PRAC]
- [GitHub issue #8395: User-Level Agent Rules and Rule Propagation](https://github.com/anthropics/claude-code/issues/8395) — Community feature request, confirmed no automatic rule propagation to subagents, closed not-planned January 2026 [PRAC]
- [Best practices for Claude Code subagents](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/) — Practitioner guide, role-specific tool scoping patterns [PRAC]
- [How and when to use subagents in Claude Code](https://claude.com/blog/subagents-in-claude-code) — Official Anthropic blog, context isolation architecture [OFFICIAL]
- [Claude Code Subagents: What They Are and How They Work](https://www.morphllm.com/claude-subagents) — Practitioner analysis, inheritance model, role-scoping patterns [PRAC]
- [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) — Community reverse-engineering of Claude Code system prompt structure; subagent prompt isolation analysis [PRAC]
- [GitHub issue #12790: Subagents should inherit parent agent context](https://github.com/anthropics/claude-code/issues/12790) — Community feature request documenting current inheritance limitations [PRAC]
- [Claude Code worktrees: Run Parallel Sessions Without Conflicts](https://claudefa.st/blog/guide/development/worktree-guide) — Practitioner guide, worktree isolation use cases [PRAC]
