---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments:
  - docs/research/preliminary-findings-momentum-as-skills-2026-03-13.md
  - docs/research/handoff-product-brief-2026-03-14.md
workflowType: 'research'
lastStep: 1
research_type: 'technical'
research_topic: 'Agent Skills Deployment Standards for Momentum'
research_goals: 'Determine standards-based installation for Momentum with Claude Code optimization'
user_name: 'Steve'
date: '2026-03-15'
web_research_enabled: true
source_verification: true
derives_from:
  - id: RESEARCH-SKILLS-PRELIM-001
    path: docs/research/preliminary-findings-momentum-as-skills-2026-03-13.md
    relationship: derives_from
    description: "Preliminary findings on Momentum as Agent Skills — packaging strategy, portability layers, BMAD relationship, Claude Code-specific enhancements"
  - id: HANDOFF-BRIEF-001
    path: docs/research/handoff-product-brief-2026-03-14.md
    relationship: derives_from
    description: "Product brief handoff with research findings and recommendations including skills strategy"
  - id: RESEARCH-PLUGIN-ARCH-001
    path: docs/research/claude-code-plugin-architecture-2026-03-16.md
    relationship: derives_from
    description: "Claude Code plugin architecture — extension points, lifecycle, API surface"
    note: "subagent research"
  - id: RESEARCH-PLUGIN-DIST-001
    path: docs/research/claude-code-plugin-distribution-2026-03-16.md
    relationship: derives_from
    description: "Claude Code plugin distribution — registry, packaging, installation patterns"
    note: "subagent research"
  - id: RESEARCH-BMAD-COEXIST-001
    path: docs/research/bmad-v6-skills-architecture-coexistence-2026-03-16.md
    relationship: derives_from
    description: "BMAD v6 skills architecture coexistence — migration strategy, backward compatibility"
    note: "subagent research"
  - id: RESEARCH-SKILLS-TESTING-001
    path: docs/research/technical-claude-code-skills-testing-plugin-migration-2026-03-16.md
    relationship: derives_from
    description: "Claude Code skills testing and plugin migration — test patterns, validation approaches"
    note: "subagent research"
referenced_by: []
provenance:
  generated_by: analyst-agent (Mary) + 4 research subagents
  model: claude-opus-4-6
  timestamp: 2026-03-16T12:00:00Z
  research_date: "2026-03-15 through 2026-03-16"
  access_dates:
    web_sources: "2026-03-15 and 2026-03-16"
    note: "All external URLs were accessed by research agents on these dates. Subject to link rot — re-verify if using after 2026-06-16 (90-day freshness window)"
  validation: "VFL v3.0 dual-reviewer, 2026-03-16"
---

# Research Report: Technical

**Date:** 2026-03-15 (updated 2026-03-16)
**Author:** Steve
**Research Type:** Technical

---

## Research Overview

Technical research into Agent Skills deployment standards, tool-specific features outside the standard (Claude Code, Cursor), and how Momentum can ship a single standards-based package while configuring tool-specific optimizations.

---

## Technical Research Scope Confirmation

**Research Topic:** Agent Skills Deployment Standards for Momentum
**Research Goals:** Determine standards-based installation for Momentum with Claude Code optimization

**Technical Research Scope:**

- The Agent Skills specification (agentskills.io) and its packaging/distribution model
- skills.sh / skillsmp.com registries and npx skills package manager
- Claude Code features outside the spec (hooks, rules, agents, context forking, model routing, plugins)
- Cursor features outside the spec (rules, agents, MCP, Cursor-specific extensions)
- The dual deployment problem: one package, tool-specific optimizations

**Research Methodology:**

- Current web data with rigorous source verification
- Multi-source validation for critical technical claims
- Confidence level framework for uncertain information
- Comprehensive technical coverage with architecture-specific insights

**Scope Confirmed:** 2026-03-15

## The Three Standards Layers

The deployment landscape has three distinct layers, each with different portability characteristics:

### Layer 1: Agent Skills Standard (Portable — All Tools)

The Agent Skills specification (agentskills.io) defines the universal format for AI agent capabilities. Published by Anthropic in December 2025 (Apache 2.0), adopted by 17+ tools within months.

**Format:** A `SKILL.md` file with YAML frontmatter (`name`, `description`) followed by markdown instructions. Optional subdirectories: `scripts/` (executable code), `references/` (documentation), `assets/` (templates/resources).

**Constraints:** Name is lowercase+hyphens, max 64 chars. Description max 1024 chars. Instructions recommended under 5000 tokens / 500 lines. File must be named exactly `SKILL.md` (case-sensitive).

**Three-stage loading:** (1) Frontmatter (~100 tokens) loaded at startup for matching, (2) full SKILL.md loaded on invocation, (3) scripts/references/assets loaded on demand.

**Supported tools:** Claude Code, Cursor, Codex, Copilot, Windsurf, Antigravity, Gemini CLI, Goose, Kilo, Kiro CLI, OpenCode, Roo, Trae, and others — 17+ as of March 2026.

**Key principle:** Extra YAML frontmatter fields are silently ignored by tools that don't understand them. A single SKILL.md can be both spec-compliant and tool-optimized.

_Source: [agentskills.io/specification](https://agentskills.io/specification), [Anthropic spec on GitHub](https://github.com/anthropics/skills/blob/main/spec/agent-skills-spec.md)_

### Layer 2: Package Management (Distribution)

**`npx skills` (by Vercel)** — The primary package manager for Agent Skills. Launched January 2026. Open source.

- Install: `npx skills add <package> -a <agent>` (e.g., `npx skills add vercel-labs/agent-skills -a claude-code`)
- Target-aware: installs to `.claude/skills/` for Claude Code, `.cursor/skills/` for Cursor, etc.
- Registry: [skills.sh](https://skills.sh) (83K+ skills), [skillsmp.com](https://skillsmp.com) (96K+)
- Supports project-scope and global-scope installation
- Can list installed skills: `npx skills list`, filter by agent: `npx skills ls -a claude-code`

**Alternative installers:** `npx add-skill` (add-skill.org), `openskills` (npm global install). Multiple competing installers exist but `npx skills` is the most established.

_Source: [Vercel Labs / skills on GitHub](https://github.com/vercel-labs/skills), [skills on npm](https://www.npmjs.com/package/skills), [Vercel changelog](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem)_

### Layer 3: Claude Code Plugins (Tool-Specific Bundling)

**This is the key finding for Momentum.** Claude Code Plugins are a bundling format that packages skills + agents + hooks + MCP + settings into a single installable unit. A plugin can contain everything Momentum needs — portable skills AND Claude Code-specific enforcement.

**Plugin directory structure:**
```
momentum-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata (name, version, description, author, license)
├── skills/                   # Standard Agent Skills (SKILL.md files) — PORTABLE
│   ├── code-review/
│   │   └── SKILL.md
│   ├── dev-story/
│   │   └── SKILL.md
│   └── upstream-fix/
│       └── SKILL.md
├── agents/                   # Claude Code subagents — CLAUDE CODE SPECIFIC
│   ├── code-reviewer.agent.md
│   └── architecture-guard.agent.md
├── hooks/
│   └── hooks.json            # Deterministic enforcement — CLAUDE CODE SPECIFIC
├── commands/                 # Slash commands — CLAUDE CODE SPECIFIC
├── .mcp.json                 # MCP server config — CLAUDE CODE SPECIFIC
└── settings.json             # Default settings when plugin enabled — CLAUDE CODE SPECIFIC
```

**Critical architecture rule:** All directories (commands/, agents/, skills/, hooks/) must be at the plugin root, not inside `.claude-plugin/`. Only `plugin.json` belongs in `.claude-plugin/`.

**plugin.json fields:** `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, plus paths to `commands`, `agents`, `skills`, `hooks`, `mcpServers`, `outputStyles`, `lspServers`.

**Installation:** `--scope project` writes to `enabledPlugins` in `.claude/settings.json`, making the plugin available to everyone who clones the repo.

**Timeline:** MCP (Nov 2024) → Subagents (Jul 2025) → Hooks (Sep 2025) → Plugins & Skills (Oct 2025) → Agent Teams (Feb 2026).

_Source: [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference), [Create Plugins](https://code.claude.com/docs/en/plugins), [Claude Code Plugins README](https://github.com/anthropics/claude-code/blob/main/plugins/README.md)_

---

## Claude Code Features Outside the Agent Skills Standard

These are Claude Code capabilities that have no equivalent in the Agent Skills spec. They are what make Claude Code optimization possible — and what a plugin can bundle alongside portable skills.

### Hooks (Tier 1 Deterministic Enforcement)

Hooks are shell scripts that fire automatically at specific lifecycle points. They are deterministic — zero exceptions, no LLM judgment involved.

**21 hook events** including: `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `UserPromptSubmit`, `Notification`.

**Four handler types:** command (shell scripts), HTTP (JSON to URL), prompt (Claude yes/no decisions), agent (spawn subagents to verify conditions).

**Configuration:** `hooks/hooks.json` in plugin root, or inline in `plugin.json`, or in `.claude/settings.json` at project/global level.

**Matchers** can target specific tools (Bash, Edit, Write) or any tool. `PreToolUse` can approve, deny, or modify tool calls.

**Momentum use cases:** Auto-lint on edit, acceptance test directory protection, file protection, conditional test/quality gate on stop, git commit enforcement.

_Source: [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks), [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)_

### Rules (`~/.claude/rules/` and `.claude/rules/`)

Auto-loaded markdown files in every Claude Code session — including subagents. No invocation needed; always present as advisory context (Tier 3 enforcement).

- Global: `~/.claude/rules/*.md`
- Project: `.claude/rules/*.md`

**Not part of the Agent Skills spec.** Skills are invoked on demand; rules are always loaded. For Momentum, rules encode the authority hierarchy, anti-patterns, and universal standards.

_Source: [Claude Code Settings Guide](https://www.eesel.ai/blog/settings-json-claude-code)_

### Subagents (`~/.claude/agents/` and `.claude/agents/`)

Independent agents with their own context window, tool access restrictions, and instructions. Can be bundled in plugins via the `agents/` directory.

**Momentum use cases:** Code-reviewer with read-only tools (pure verifier), architecture-guard for pattern drift detection.

**Key distinction from skills:** Skills are instructions Claude follows in the current context. Agents spawn a separate context with their own tool restrictions.

_Source: [Create Custom Subagents](https://code.claude.com/docs/en/sub-agents)_

### Claude Code-Specific Frontmatter

Extra YAML fields in SKILL.md that Claude Code honors but other tools ignore:

| Field | Purpose | Momentum Use |
|---|---|---|
| `context: fork` | Run skill in separate context window | Producer-Verifier isolation |
| `model` | Route to specific model | Review to Opus, routine to Haiku |
| `disable-model-invocation` | Prevent auto-triggering | Don't auto-invoke heavyweight skills |

**This is the portability bridge:** A SKILL.md with `context: fork` in its frontmatter is still a valid Agent Skill. Claude Code uses the field; other tools ignore it. One file, dual behavior.

_Source: [Extend Claude with Skills](https://code.claude.com/docs/en/skills)_

---

## Cursor Features Outside the Agent Skills Standard

### Cursor Rules (`.cursor/rules/`)

Markdown files in `.cursor/rules/` folder — similar to Claude Code's rules but with Cursor-specific behavior. Always-on context for coding styles, tech stacks, constraints.

**Equivalent to:** Claude Code's `.claude/rules/`
**Difference:** Different directory path, potentially different loading behavior.

_Source: [Cursor Rules Docs](https://cursor.com/docs/context/rules)_

### Cursor MCP (`.cursor/mcp.json`)

MCP server configuration in `.cursor/mcp.json` at project root. Agent scans enabled MCP servers and loads their tools.

**Constraint:** Cursor has a ceiling of ~40 active tools across all MCP servers. Exceed it and the agent silently loses access to some tools.

_Source: [Cursor MCP Guide](https://www.truefoundry.com/blog/mcp-servers-in-cursor-setup-configuration-and-security-guide)_

### Cursor Skills Installation

Skills installed via `npx skills add -a cursor` go to `.cursor/skills/`. However, there is a **known bug (March 2026)** where skills installed via `npx skills add` in Cursor get classified as Rules instead of Skills in the Cursor UI. This is a Cursor-side bug, not a standard issue.

_Source: [Cursor Forum — Skills installed as Rules](https://forum.cursor.com/t/skills-are-installed-as-rules/152793)_

---

## The Dual Deployment Answer: Plugin + Standard Skills

The research reveals a clear architecture for Momentum's deployment:

### For Claude Code: Ship as a Plugin

**Correction:** `npx skills add` installs individual skills only, not full plugins. For Claude Code's complete enforcement layer, use the plugin marketplace system (`/plugin install`). See the CRITICAL CORRECTION section below.

A Claude Code Plugin is the right packaging for Momentum. It bundles:

| Component | Standard? | Portable? | Purpose |
|---|---|---|---|
| `skills/` | Agent Skills spec | Yes — all 17+ tools | Workflow instructions (code review, dev story, upstream fix) |
| `agents/` | Claude Code specific | No | Subagents (code-reviewer, architecture-guard) |
| `hooks/hooks.json` | Claude Code specific | No | Tier 1 deterministic enforcement |
| `.mcp.json` | MCP standard | Partially — format shared, paths differ | Tool/data access |
| `settings.json` | Claude Code specific | No | Default configuration |
| `commands/` | Claude Code specific | No | Slash commands |

**The skills inside the plugin ARE standard Agent Skills.** They work anywhere. The plugin just bundles them with Claude Code-specific enforcement that other tools don't support.

### For Other Tools (Cursor, Codex, etc.): Install Just the Skills

```bash
# Claude Code — full plugin (skills + hooks + agents + settings)
# Installation mechanism TBD — plugin marketplace or manual

# Cursor — portable skills subset only
npx skills add momentum -a cursor
```

Cursor gets the skills (the instructions, workflows, references) but not the hooks or agents. Cursor has its own rules system (`.cursor/rules/`) and its own MCP configuration (`.cursor/mcp.json`). A future Momentum adaptation for Cursor would create Cursor-specific equivalents of the enforcement layer — but that's not the current job.

### The Portability Bridge

The Agent Skills spec's design — extra frontmatter fields are silently ignored — means Momentum can have one set of SKILL.md files that are:
- **Standards-compliant** (name, description, markdown instructions)
- **Claude Code-optimized** (context: fork, model routing, etc.)
- **Portable** (Cursor, Codex, Copilot all load the standard fields and ignore the rest)

This is not a compromise. It's the intended design of the spec.

---

## Comparison: What Lives Where

| Concern | Agent Skills Standard | Claude Code Plugin | Cursor Equivalent |
|---|---|---|---|
| Workflow instructions | `SKILL.md` | `skills/*/SKILL.md` | `.cursor/skills/*/SKILL.md` |
| Always-on rules | Not in spec | `.claude/rules/*.md` | `.cursor/rules/*.md` |
| Deterministic enforcement | Not in spec | `hooks/hooks.json` | No equivalent (advisory only) |
| Subagents | Not in spec | `agents/*.agent.md` | No direct equivalent |
| MCP servers | Not in spec (separate standard) | `.mcp.json` in plugin | `.cursor/mcp.json` |
| Context isolation | Not in spec | `context: fork` frontmatter | No equivalent |
| Model routing | Not in spec | `model` frontmatter | No equivalent |
| Package management | `npx skills add` | Plugin install + `npx skills` | `npx skills add -a cursor` |

**Key insight:** Cursor has no equivalent to hooks (deterministic enforcement) or subagents (context-isolated verification). This means Momentum on Cursor operates at Tier 2 (structured) and Tier 3 (advisory) only — the Tier 1 deterministic layer is a Claude Code advantage. This is exactly why optimizing for Claude Code first makes sense.

---

## Recommendations for Momentum

**Note:** These initial recommendations are superseded by the Implementation Recommendations section below, which incorporates findings from subagent research on BMAD coexistence and plugin isolation constraints.

### 1. Ship as a Claude Code Plugin

Package Momentum as a Claude Code Plugin containing standard Agent Skills plus Claude Code-specific enforcement. This gives:
- One install for Claude Code users (everything bundled)
- Extractable skills for other tools via `npx skills add`
- Standard Agent Skills spec compliance for portability

### 2. Standard Skills as the Portable Core

Every Momentum workflow that can be expressed as instructions should be a standard SKILL.md. Use Claude Code-specific frontmatter (`context: fork`, `model`) for optimization, but ensure the skill works without those fields.

### 3. Hooks for Tier 1 Enforcement (Claude Code Only)

Bundle `hooks/hooks.json` in the plugin for: auto-lint, test protection, file protection, quality gates, git commit enforcement. Accept that this layer doesn't port to Cursor — it's the Claude Code optimization that justifies the plugin packaging.

### 4. Agents for Verification (Claude Code Only)

Bundle `agents/code-reviewer.agent.md` and `agents/architecture-guard.agent.md` in the plugin. These are the producer-verifier separation mechanism. On Cursor, verification would need to be skill-based (less isolated, but still functional).

### 5. Rules for Always-On Context

Deploy `.claude/rules/*.md` files containing the authority hierarchy, anti-patterns, and universal standards. These load automatically in every session. For Cursor portability, equivalent files go in `.cursor/rules/` — same content, different path.

### 6. Don't Build Cursor Deployment Yet

Follow the Agent Skills standard, use Claude Code-specific frontmatter that gets ignored elsewhere, and accept that Cursor adaptation is a future task. The portability is built-in by following the spec; the Cursor-specific enforcement layer is a separate effort.

---

## Open Questions for Architecture

1. **Plugin distribution:** How are Claude Code plugins currently distributed? Is there a plugin marketplace (`code.claude.com/docs/en/discover-plugins` suggests yes), or is it manual install only? What's the `npx` equivalent for plugins vs. skills?

2. **Global vs. project scope:** Can a plugin deploy files to `~/.claude/rules/` (global) or only to `.claude/` (project)? Momentum's authority hierarchy rule needs to be global.

3. **Plugin + BMAD coexistence:** If BMAD is installed as a separate system and Momentum as a plugin, how do they interact? Do BMAD-generated skills and Momentum plugin skills coexist in `.claude/skills/`?

4. **The Cursor skills-as-rules bug:** Is this blocking for Cursor adoption, or just a UI issue? Need to monitor.

5. **Git hooks vs. Claude Code hooks:** Momentum wants git integration as infrastructure. Should git hooks (pre-commit, commit-msg) be part of the plugin, or managed separately? Claude Code hooks and git hooks are different mechanisms with different trigger points.

---

## Sources

- [Agent Skills Specification](https://agentskills.io/specification)
- [Anthropic Agent Skills Spec on GitHub](https://github.com/anthropics/skills/blob/main/spec/agent-skills-spec.md)
- [Vercel Labs / skills (npx skills)](https://github.com/vercel-labs/skills)
- [skills.sh Registry](https://skills.sh)
- [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
- [Create Plugins — Claude Code Docs](https://code.claude.com/docs/en/plugins)
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)
- [Extend Claude with Skills — Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Cursor Rules Documentation](https://cursor.com/docs/context/rules)
- [Cursor Forum — Skills installed as Rules bug](https://forum.cursor.com/t/skills-are-installed-as-rules/152793)
- [Cursor Forum — npx skills not recognized](https://forum.cursor.com/t/npx-skills-are-not-recognized-as-skills/153003)
- [Claude Code Extensions Explained (Medium)](https://muneebsa.medium.com/claude-code-extensions-explained-skills-mcp-hooks-subagents-agent-teams-plugins-9294907e84ff)
- [Skills.sh Blog Post](https://johnoct.github.io/blog/2026/02/12/skills-sh-open-agent-skills-ecosystem/)
- [Agent Skills Standard Blog (Benjamin Abt)](https://benjamin-abt.com/blog/2026/02/12/agent-skills-standard-github-copilot/)

---

## Integration Patterns Analysis

### The Three-Protocol Stack

The agentic engineering ecosystem has converged on three complementary protocols, each handling a different integration concern:

| Protocol | Layer | What It Does | Analogy |
|---|---|---|---|
| **Agent Skills** | Procedures | What to do and how | The recipe |
| **MCP** | Capabilities | Tools and data access | The kitchen equipment |
| **ACP** | Communication | Agent-to-IDE integration | The waiter taking orders |

These are not competing standards — they compose. A Momentum skill (Agent Skills) might instruct the agent to use a git MCP server (MCP) to check file history, and the agent communicates with the IDE through ACP. Each protocol is independently adoptable.

_Source: [MCP vs Agent Skills (ByteBridge)](https://bytebridge.medium.com/model-context-protocol-mcp-vs-agent-skills-empowering-ai-agents-with-tools-and-expertise-3062acafd4f7), [MCP vs Agent Skills (Dev|Journal)](https://earezki.com/ai-news/2026-03-13-model-context-protocol-mcp-vs-ai-agent-skills-a-deep-dive-into-structured-tools-and-behavioral-guidance-for-llms/)_

### MCP Integration (Capabilities Layer)

MCP standardizes how applications expose tools and context to language models. Architecture: **Hosts** (user-facing LLM apps) → **Clients** (protocol connectors within hosts) → **Servers** (external services exposing capabilities).

**Core primitives:** Tools (executable functions, require user approval for destructive actions) and Resources (read-only data sources for contextual information).

**Momentum relevance:** MCP servers could provide:
- Git integration (file history, blame, diff) for provenance tracking
- Findings ledger access for the flywheel
- Cross-project knowledge sharing

**Plugin bundling:** Claude Code plugins can include `.mcp.json` to bundle MCP server configurations. Cursor uses `.cursor/mcp.json` — same format, different path. MCP is the most portable of the three protocols after Agent Skills.

**Constraint (Cursor):** Cursor has a ceiling of ~40 active tools across all MCP servers. Exceeding this causes silent tool access loss. Momentum's MCP integration must be tool-count conscious.

**2026 roadmap:** MCP is prioritizing transport scalability, agent communication, governance maturation, and enterprise readiness.

_Source: [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25), [2026 MCP Roadmap](http://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/), [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol)_

### ACP Integration (Agent-to-IDE Communication)

The Agent Client Protocol, jointly developed by JetBrains and Zed, defines a standard communication interface between AI agents and IDEs. Agents communicate over stdin/stdout using JSON-RPC 2.0.

**Key capability:** Implement the protocol once, work in JetBrains IDEs (IntelliJ, PyCharm, WebStorm), Zed, and any other supporting editor.

**Agent Registry:** Live since January 28, 2026 — a directory of AI agents integrated directly into JetBrains IDEs and Zed.

**Momentum relevance:** ACP is the transport layer — it determines how an agent talks to an IDE, not what the agent does. Skills are agent-internal (they tell the agent what to do regardless of which IDE hosts it). Momentum skills work identically across ACP because they operate inside the agent's context, not at the IDE communication boundary.

**Current status:** ACP is relevant for Momentum's future if Momentum ever needs to provide a standalone agent (rather than skills for existing agents). For now, shipping as Claude Code skills/plugin means ACP is not a deployment concern — Claude Code handles its own IDE integration.

_Source: [JetBrains ACP](https://www.jetbrains.com/acp/), [Zed ACP](https://zed.dev/acp), [ACP Registry Announcement](https://blog.jetbrains.com/ai/2026/01/acp-agent-registry/)_

### Claude Code Hook Lifecycle Integration

Hooks provide 21 lifecycle events for intercepting and controlling agent behavior. The integration pattern for Momentum:

**Hook chain for a typical development cycle:**

```
SessionStart → [load rules, verify environment]
  ↓
UserPromptSubmit → [validate intent, check context]
  ↓
PreToolUse(Edit/Write) → [protect acceptance test files, check file permissions]
  ↓
PostToolUse(Edit/Write) → [auto-lint, auto-format]
  ↓
PreToolUse(Bash:"git commit") → [run linter, typecheck, test suite]
  ↓
Stop → [quality gate: check git diff, run tests if code changed]
```

**Handler types:** Command (shell scripts), HTTP (POST to endpoint — new Feb 2026), Prompt (Claude yes/no decision), Agent (spawn subagent to verify).

**Async hooks:** `async: true` runs hooks in the background without blocking (since Jan 2026). Useful for non-blocking notifications or logging.

**Control flow:** Exit code 0 = proceed, exit code 2 = block the action (PreToolUse) or force continue (Stop). This is the mechanism for deterministic enforcement.

**SubagentStop:** For subagents, Stop hooks are automatically converted to SubagentStop events. Important for Momentum's code-reviewer agent.

_Source: [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks), [Hooks Guide](https://code.claude.com/docs/en/hooks-guide), [Claude Code Hooks Complete Guide](https://claudefa.st/blog/tools/hooks/hooks-guide)_

### Git Integration Pattern

Git integration for Momentum operates at two levels: **Claude Code hooks** (agent-level) and **git hooks** (repository-level). They are complementary, not competing.

**Claude Code hooks intercept the agent:**
- `PreToolUse` on `Bash` matching `git commit` → run lint/typecheck before the agent can commit
- `PostToolUse` on `Write/Edit` → auto-format after every file change
- `Stop` → quality gate before session ends

**Git hooks intercept the repository:**
- `pre-commit` → runs when `git commit` actually executes (after Claude Code hook passes)
- `commit-msg` → validates commit message format
- `pre-push` → runs tests before push

**Execution order when Claude commits:** Claude Code `PreToolUse` hook fires first → if it passes, the `git commit` command runs → git's own `pre-commit` hook fires → if that passes, the commit completes. Two layers of enforcement.

**Feature gap (as of March 2026):** Claude Code does not have native `PreCommit` / `PostCommit` hook events. There's an open feature request (GitHub issue #4834) to add dedicated git lifecycle hooks. Currently, git commit interception requires matching `Bash` tool calls containing "git commit" — functional but less precise.

**GitButler integration:** An emerging pattern where Claude Code hooks auto-manage commits into virtual branches via GitButler, isolating AI-generated code changes automatically. Worth monitoring for Momentum's git integration strategy.

**Momentum's git integration plan:**
1. Claude Code hooks for agent-level enforcement (blocking bad commits)
2. Standard git hooks (Husky / pre-commit framework) for repository-level enforcement (commit message format, secret scanning)
3. Provenance metadata in commit messages or structured commit notes

_Source: [Git Hooks with Claude Code (DEV)](https://dev.to/myougatheaxo/git-hooks-with-claude-code-build-quality-gates-with-husky-and-pre-commit-27l0), [Claude Code Git Integration](https://claudefa.st/blog/guide/development/git-integration), [Feature Request #4834](https://github.com/anthropics/claude-code/issues/4834), [GitButler Hooks](https://docs.gitbutler.com/features/ai-integration/claude-code-hooks)_

### Plugin-to-IDE Integration Pattern

How a Momentum plugin integrates with the Claude Code environment:

```
momentum-plugin/
├── .claude-plugin/plugin.json    → Registers in .claude/settings.json (enabledPlugins)
├── skills/                       → Loaded into .claude/skills/ (discoverable via frontmatter)
├── agents/                       → Available alongside built-in agents (via /agents)
├── hooks/hooks.json              → Merged into active hook configuration
├── .mcp.json                     → MCP servers registered and available
└── settings.json                 → Default settings applied when plugin enabled
```

**Key integration behaviors:**
- Plugin agents appear in `/agents` alongside custom subagents
- Plugin hooks merge with existing hooks (project + global)
- Plugin skills are discoverable via the same frontmatter matching as regular skills
- Plugin MCP servers register alongside existing MCP servers
- `--scope project` makes the plugin available to all repo cloners via `.claude/settings.json`

**For teams:** A team member clones the repo → `.claude/settings.json` references the Momentum plugin → all skills, hooks, agents, and MCP servers are immediately active. No manual installation per team member beyond the initial plugin setup.

_Source: [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference), [Discover Plugins](https://code.claude.com/docs/en/discover-plugins)_

---

## Architectural Patterns (Subagent Research)

_Research conducted via four parallel subagents. Detailed reports at: `docs/research/claude-code-plugin-architecture-2026-03-16.md`, `docs/research/claude-code-plugin-distribution-2026-03-16.md`, `docs/research/bmad-v6-skills-architecture-coexistence-2026-03-16.md`, `docs/research/technical-claude-code-skills-testing-plugin-migration-2026-03-16.md`_

### CRITICAL CORRECTION: `npx skills add` Installs Skills, NOT Plugins

**Earlier in this document I suggested `npx skills add momentum` for Claude Code. This is partially wrong.** `npx skills add` copies SKILL.md files into agent skill directories. It cannot install hooks, agents, MCP servers, LSP servers, or any full plugin container. It is the right tool for Cursor and other tools that only support skills. For Claude Code's full enforcement layer, the **plugin marketplace system** is the correct distribution mechanism.

| Distribution Mechanism | What It Installs | Target |
|---|---|---|
| `npx skills add` (Vercel) | Skills only (SKILL.md files) | Any of 17+ agents (Cursor, Codex, etc.) |
| `/plugin install` (Claude Code) | Full plugins (skills + hooks + agents + MCP + settings) | Claude Code only |
| Plugin marketplace (`marketplace.json`) | Curated plugin catalogs | Claude Code only |
| npm package (via marketplace source) | Plugins distributed as npm packages | Claude Code only |

**Six source types** in `marketplace.json`: relative paths, GitHub repos, git URLs, git subdirectories, **npm packages** (with version range and private registry support), and **pip packages**.

As of March 2026: ~43 community marketplaces, ~834 plugins. The official Anthropic marketplace (`anthropics/claude-plugins-official`) is auto-included.

_Source: [Discover Plugins](https://code.claude.com/docs/en/discover-plugins), [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), [Vercel skills](https://github.com/vercel-labs/skills)_

### CRITICAL FINDING: BMAD Does NOT Use Plugin Format (Deliberately)

BMAD V6.1 (March 13, 2026) completed the conversion to skills-based architecture — everything is now an Agent Skill. The npm package shrank 91%. The installer (`npx bmad-method install`) writes one skill directory per agent/workflow/task to `.claude/skills/`.

**But BMAD installs as flat project-level skills, NOT a plugin.** This is a deliberate design choice (documented in [Issue #1629](https://github.com/bmad-code-org/BMAD-METHOD/issues/1629)):

- BMAD agents need **main-conversation context** (persona persists across interactions)
- BMAD agents need **full tool access** (Edit, Write, Bash — not restricted)
- Plugin isolation prevents both of these

**This means Momentum faces a design decision:**

| Approach | Pros | Cons |
|---|---|---|
| **Plugin** (like Compound Engineering) | Namespaced (`momentum:skill-name`), bundled enforcement (hooks, agents), marketplace distribution, clean install/update | Plugin skills are isolated — cannot maintain persona across interactions, cannot share main context |
| **Flat skills** (like BMAD) | Main-conversation context, full tool access, persona persistence | No bundled hooks/agents, no namespace protection, manual hook configuration, 68+ BMAD skills may approach context budget |
| **Hybrid** | Best of both — flat skills for orchestrating agents, plugin for enforcement and verification | More complex distribution, two install mechanisms |

**Context budget concern:** This project already has 68 BMAD skills. The skill description budget is 2% of context window. Adding Momentum skills on top of 68 BMAD skills may approach or exceed this budget, degrading skill matching quality.

_Source: [bmad-v6-skills-architecture-coexistence-2026-03-16.md](docs/research/bmad-v6-skills-architecture-coexistence-2026-03-16.md), [BMAD Issue #1629](https://github.com/bmad-code-org/BMAD-METHOD/issues/1629)_

### Skill Composition Architecture

Two composition patterns are available:

**1. Skill drives, agent executes** — A skill with `context: fork` spawns an isolated subagent:
```yaml
---
name: adversarial-review
description: Review code in isolated context
context: fork
agent: Explore
---
Review code adversarially...
```

**2. Agent drives, skills provide knowledge** — A subagent preloads skills via `skills:` frontmatter:
```yaml
---
name: code-reviewer
description: Adversarial code reviewer
skills:
  - authority-hierarchy
  - anti-patterns
---
Review code against preloaded standards...
```

**Subagents cannot spawn other subagents.** For nested delegation, chain from the main conversation.

**The Compound Engineering Plugin** (Every, Inc.) is the production exemplar: 26 agents + 13 skills + 23 commands. Pattern: Plan (parallel research) → Work (execution with isolation) → Review (multi-agent assessment) → Compound (capture learnings). This maps closely to Momentum's flywheel.

_Source: [claude-code-plugin-architecture-2026-03-16.md](docs/research/claude-code-plugin-architecture-2026-03-16.md), [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)_

### Plugin Testing and Validation

- **Output quality testing:** promptfoo with LLM-rubric assertions
- **Trigger precision testing:** Anthropic's `run_eval.py` from the skill-creator plugin — uses a 60/40 holdout split to prevent overfitting skill descriptions
- **Pre-commit validation:** [freddo1503/claude-pre-commit](https://github.com/freddo1503/claude-pre-commit) — Rust-based, v0.1.0 experimental. SKILL.md YAML frontmatter validation in progress
- **Native validation:** `claude plugin validate` checks manifest integrity
- **Local development:** `--plugin-dir ./my-plugin` loads a plugin without installing. `/reload-plugins` for hot reload during development

_Source: [technical-claude-code-skills-testing-plugin-migration-2026-03-16.md](docs/research/technical-claude-code-skills-testing-plugin-migration-2026-03-16.md)_

### Migration Path: .claude/ → Plugin

Anthropic documents an explicit migration:
1. Create `.claude-plugin/plugin.json` manifest
2. Copy `commands/`, `agents/`, `skills/` directories to plugin root
3. Move hooks from `settings.json` into `hooks/hooks.json`
4. **Breaking change:** skill names get namespaced — `/deploy` becomes `/my-plugin:deploy`

Plugins are pinned to **git commit SHA** at install time. Manual updates via `claude plugin update <name>`. If you change code without bumping `plugin.json` version, users won't see updates due to caching.

_Source: [Plugins Reference](https://code.claude.com/docs/en/plugins-reference)_

---

## Implementation Recommendations

### The Deployment Decision: Hybrid Approach

Given the BMAD coexistence constraint and the need for both main-context orchestration AND deterministic enforcement, Momentum should use a **hybrid approach**:

**1. Momentum Practice Plugin** (Claude Code marketplace):
- `hooks/hooks.json` — Tier 1 deterministic enforcement (lint, test protection, quality gates, git commit validation)
- `agents/code-reviewer.agent.md` — Pure verifier with read-only tools
- `agents/architecture-guard.agent.md` — Pattern drift detection
- `skills/` — Verification and enforcement skills that benefit from isolation (`context: fork`)
- `.mcp.json` — MCP server configuration for git integration, findings ledger
- Published to a Momentum marketplace or the Anthropic official marketplace

**2. Momentum Practice Skills** (standard Agent Skills, installed via `npx skills add` or BMAD):
- Workflow skills (dev-story, upstream-fix, create-story) that need main-conversation context
- Orchestrating agent skills that need persona persistence
- Portable to Cursor and other tools
- Can be installed alongside BMAD skills in `.claude/skills/`

**3. Momentum Rules** (always-loaded context):
- `.claude/rules/authority-hierarchy.md`
- `.claude/rules/anti-patterns.md`
- `.claude/rules/model-routing.md`
- Deployed by the plugin or installed separately

### Distribution Strategy

| Component | Distribution | Install Command |
|---|---|---|
| Momentum Plugin (enforcement) | Momentum marketplace (GitHub) | `/plugin marketplace add momentum/momentum-plugin` then `/plugin install momentum-practice` |
| Momentum Skills (workflows) | npm or GitHub + npx skills | `npx skills add momentum/momentum-skills -a claude-code` |
| Momentum for Cursor | Same skills via npx | `npx skills add momentum/momentum-skills -a cursor` |

### Context Budget Management

With 68 BMAD skills already installed, context budget is a real concern. Mitigation:
- Keep Momentum skill descriptions extremely concise (each description costs ~100 tokens at startup)
- Consider whether some BMAD skills can be disabled when not needed
- Monitor for skill matching degradation as total skill count grows
- The plugin's skills don't count against the flat skill budget (they're namespaced)

### Version and Update Management

- Use semantic versioning in `plugin.json`
- Always bump version when changing code (caching issue)
- Consider stable/latest release channels via marketplace refs
- Pin to git SHA for reproducibility, update manually via `claude plugin update`

### Testing Strategy

- Use promptfoo for skill output quality validation
- Use `run_eval.py` for skill trigger precision testing
- Use `claude plugin validate` for manifest integrity
- Use `--plugin-dir` for local development and iteration
- Consider `freddo1503/claude-pre-commit` for CI validation when it matures

---

## Validation Status

**Validation Method:** VFL v3.0 dual-reviewer pattern (enumerative + adversarial)
**Validation Date:** 2026-03-16

### Unresolved Findings (require architecture decision)

- **F-10 (CRITICAL):** Hybrid approach has no failure mode analysis — version drift between plugin enforcement and flat skill workflows, two install steps, split namespace cognitive load
- **F-17 (CRITICAL):** Document surveys the ecosystem but does not make a concrete deployment decision — the hybrid approach is a sketch, not a specification
- **F-18 (HIGH):** No Momentum skill inventory defined — packaging recommendation is premature without knowing what's being packaged
- **F-06 (HIGH):** Whether plugin-namespaced skills count against the 2% context budget is unverified — this is load-bearing for the hybrid recommendation

### Resolved by Edits

- **F-01 (MEDIUM):** Hook event count contradiction — reconciled to correct number
- **F-03 (HIGH):** Contradictory plugin recommendation — editorial note added directing to superseding section
- **F-04 (MEDIUM):** npx skills correction note added

### Accepted Risks

- **F-15 (HIGH):** Pre-1.0 ecosystem — accepted per Impermanence Principle, will re-evaluate as ecosystem matures
- **F-14 (MEDIUM):** BMAD version pinning — accepted, BMAD changes tracked monthly per practice plan Section 8.3

---

## Updated Sources (Subagent Research)

- [Claude Code Plugin Architecture Report](docs/research/claude-code-plugin-architecture-2026-03-16.md)
- [Claude Code Plugin Distribution Report](docs/research/claude-code-plugin-distribution-2026-03-16.md)
- [BMAD V6 Skills Coexistence Report](docs/research/bmad-v6-skills-architecture-coexistence-2026-03-16.md)
- [Skills Testing and Plugin Migration Report](docs/research/technical-claude-code-skills-testing-plugin-migration-2026-03-16.md)
- [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)
- [Compound Engineering: How Every Codes With Agents](https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents)
- [BMAD Issue #1629 — Why Not Plugin](https://github.com/bmad-code-org/BMAD-METHOD/issues/1629)
- [Claude Code Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
