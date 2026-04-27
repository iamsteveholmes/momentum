---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "Skill/extension contracts per agent — For each of Claude Code, OpenCode, Codex CLI, Gemini CLI, Goose, ForgeCode: extension points, manifests, invocation, permissions, file paths, marketplace mechanics."
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
---

# Skill / Extension Contracts per Agent (Technical, 2026-04-26)

This document is a side-by-side technical comparison of how the six leading
terminal-native agentic coding tools accept user-authored extensions: Skills,
sub-agents, slash commands, hooks, MCP servers, and packaged plugins. The goal
is to inform Momentum's multi-agent deployment refactor.

A surprising amount of convergence happened in 2025-2026: SKILL.md files,
frontmatter-driven discovery, and MCP have become near-universal. The remaining
divergence sits in (a) plugin/marketplace mechanics, (b) hook event surfaces,
(c) sandbox/permission models, and (d) where agents look for files.

---

## 1. Claude Code (Anthropic)

### Extension points available
- **Skills** (`SKILL.md` with YAML frontmatter, body markdown). The "Custom commands have been merged into skills" — `.claude/commands/*.md` still works, but the Skills directory format with supporting files is the recommended path. [OFFICIAL]
- **Sub-agents** (`.claude/agents/*.md`) — separate context windows, custom system prompts, scoped tool access. [OFFICIAL]
- **Slash commands** (legacy / now subsumed under skills). [OFFICIAL]
- **Hooks** (8 events: SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, PostToolUseFailure, Stop, StopFailure). Configured in `settings.json`. [OFFICIAL]
- **MCP servers** (`.mcp.json`, `~/.claude.json`, settings files). [OFFICIAL]
- **Plugins** (`.claude-plugin/plugin.json` manifests bundle skills + agents + hooks + MCP + LSP + monitors + bin + settings). [OFFICIAL]
- **Output styles** and **status lines** [OFFICIAL]
- **LSP servers** (`.lsp.json` inside plugins) — code intelligence for languages [OFFICIAL]
- **Background monitors** (`monitors/monitors.json`) — stream stdout lines as in-session notifications [OFFICIAL]

### Manifest format

**Skill frontmatter** ([OFFICIAL] code.claude.com/docs/en/skills):
```yaml
---
name: my-skill                       # optional, defaults to dir name
description: When/what               # recommended; truncated to 1,536 chars
when_to_use: extra triggers          # appended to description
disable-model-invocation: false      # block Claude auto-invoke
user-invocable: true                 # show in / menu
allowed-tools: Bash(git *) Read      # pre-approved tools
model: claude-sonnet-4-6 | inherit
effort: low|medium|high|xhigh|max
context: fork                        # run in subagent
agent: Explore                       # subagent type
hooks: { ... }                       # skill-scoped hooks
paths: ["src/**/*.ts"]               # auto-activate by file glob
arguments: [issue, branch]           # named positional args
shell: bash | powershell
---
```

**Plugin manifest** (`.claude-plugin/plugin.json`):
```json
{
  "name": "my-plugin",
  "description": "...",
  "version": "1.0.0",
  "author": { "name": "..." },
  "homepage": "...", "repository": "...", "license": "..."
}
```

**Hook config** (`settings.json`):
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "if": "Bash(rm *)",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/block-rm.sh",
        "timeout": 600
      }]
    }]
  }
}
```
Hook handler types: `command`, `http`, `mcp_tool`, `prompt`, `agent`. [OFFICIAL]

### Invocation lifecycle
- **Skills**: name + description go into Claude's tool list at session start. Claude decides automatically when description matches; or user types `/skill-name`. Full body loads only on invocation, then stays in context for the rest of the session (with auto-compaction re-attaching first 5,000 tokens / shared 25K budget). [OFFICIAL]
- **Sub-agents**: Claude delegates based on description match; spawned via the `Agent` tool. Returns only summary to parent. [OFFICIAL]
- **Hooks**: fire on event matchers. PreToolUse can `allow|deny|ask|defer`. [OFFICIAL]

### Permissioning / sandboxing
- Permission rule syntax: `Bash(git *)`, `Skill(commit)`, `Skill(deploy *)`, `Read`, `Edit`. [OFFICIAL]
- Modes: `default | plan | acceptEdits | auto | dontAsk | bypassPermissions`. [OFFICIAL]
- Skills can pre-approve tools via `allowed-tools` while active. [OFFICIAL]
- Default-ask for anything not in allow list; deny rules win. [OFFICIAL]

### File load paths (precedence high→low)
| Scope | Path |
|---|---|
| Enterprise | managed settings (per OS) |
| Personal | `~/.claude/skills/<name>/SKILL.md`, `~/.claude/agents/`, `~/.claude/commands/` |
| Project | `.claude/skills/<name>/SKILL.md`, `.claude/agents/`, `.claude/commands/` |
| Plugin | `<plugin>/skills/<name>/SKILL.md` (namespaced as `plugin:skill`) |
| Nested (monorepo) | `packages/foo/.claude/skills/` auto-discovered when working in subtree |
| `--add-dir` directories | only `.claude/skills/` is loaded; subagents/commands not |

Live change detection watches all skill dirs within session. [OFFICIAL]

### Plugin / marketplace mechanics
- Marketplaces are git repos containing `.claude-plugin/marketplace.json`. [OFFICIAL]
- Install: `/plugin marketplace add <git-url>`, `/plugin install <name>`. [OFFICIAL]
- Versioning: explicit `version` field; if omitted, git commit SHA used (every commit = new version). [OFFICIAL]
- Distribution: git, npm, official Anthropic marketplace (claude.ai/settings/plugins/submit). [OFFICIAL]
- Local dev: `claude --plugin-dir ./my-plugin` overrides installed copies in that session. [OFFICIAL]
- Plugin namespacing: skills become `/plugin-name:skill-name`, preventing conflicts. [OFFICIAL]

### Recency
Skills shipped general availability for Claude Code in late 2025; the merging of custom commands into skills, plus LSP/monitor support in plugins, are 2026 additions visible in current docs as of 2026-04-26. [OFFICIAL]

---

## 2. OpenCode (sst/opencode)

### Extension points available
- **Agents** (custom and built-in: `build`, `plan`, `general`) [OFFICIAL]
- **Custom commands** [OFFICIAL]
- **Custom tools** [OFFICIAL]
- **Plugins** (TypeScript/JavaScript modules with rich hook surface) [OFFICIAL]
- **MCP servers** (local + remote, with OAuth Dynamic Client Registration) [OFFICIAL]
- **ACP support** (Agent Context Protocol) [OFFICIAL]
- **Agent Skills** (per docs nav, but page returned 404 on 2026-04-26 fetch — likely beta / recently introduced) [UNVERIFIED]
- **LSP** (out of the box) [OFFICIAL]
- **AGENTS.md** project context file generated by `/init` [OFFICIAL]

### Manifest format

**Agent (`.opencode/agents/<name>.md` or `~/.config/opencode/agents/<name>.md`)** [OFFICIAL]:
```yaml
---
description: Required brief
mode: primary | subagent | all
model: anthropic/claude-3-5-sonnet-20241022
temperature: 0.7
top_p: 0.9
steps: 50
color: "#ff8800"
permission:
  edit: ask | allow | deny
  bash: ask | allow | deny     # or specific commands
  webfetch: ask | allow | deny
  task: ["docs/**"]            # globs for subagent access
hidden: false
---
System prompt body...
```

**Command (`.opencode/commands/<name>.md`)** [OFFICIAL]:
```yaml
---
description: Run tests with coverage
agent: build
model: anthropic/claude-3-5-sonnet-20241022
subtask: true
---
Template body with $ARGUMENTS, $1, $2, !`shell-cmd` for output, and @file/path inclusions.
```

**MCP (`opencode.json` under `mcp` key)** [OFFICIAL]:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "my-server": {
      "type": "local", 
      "command": ["node", "server.js"],
      "environment": { "API_KEY": "$KEY" },
      "enabled": true,
      "timeout": 5000
    },
    "remote-svc": {
      "type": "remote",
      "url": "https://example.com/mcp",
      "headers": { "Authorization": "Bearer $TOKEN" },
      "oauth": false
    }
  }
}
```

**Plugin** (TypeScript module):
```ts
import type { Plugin } from "@opencode-ai/plugin";
export default ((ctx) => ({
  "tool.execute.before": async ({ tool, input }) => { /* ... */ },
  "tool.execute.after":  async ({ tool, output }) => { /* ... */ },
  "session.compacting":  async (...) => { /* experimental */ },
})) satisfies Plugin;
```
Plugin context exposes `project, directory, worktree, client, $` (Bun shell). Hook categories: Command, File, Installation, LSP, Message, Permission, Server, Session, Todo, Shell, Tool, TUI events. [OFFICIAL]

### Invocation lifecycle
- **Primary agents**: cycled via Tab key, or `switch_agent` keybind. [OFFICIAL]
- **Subagents**: `@agent-name` syntax or auto-invoked by parent agent. [OFFICIAL]
- **Commands**: typed as `/command-name [args]`. [OFFICIAL]
- **Plugin hooks**: fire on declared events; `tool.execute.before` can intercept and modify tool calls. [OFFICIAL]

### Permissioning / sandboxing
- Per-agent `permission` block in frontmatter (`edit | bash | webfetch | task`). [OFFICIAL]
- Tri-state per category: `ask | allow | deny`. [OFFICIAL]
- Bash can take specific command patterns instead of a single value. [OFFICIAL]
- Default behavior: ask. [UNVERIFIED]

### File load paths
| Scope | Agents | Commands | Plugins | MCP |
|---|---|---|---|---|
| Global | `~/.config/opencode/agents/` | `~/.config/opencode/commands/` | `~/.config/opencode/plugins/` | global `opencode.json` |
| Project | `.opencode/agents/` | `.opencode/commands/` | `.opencode/plugins/` | project `opencode.json` |
| npm | — | — | listed in `opencode.json` `plugin` array, cached at `~/.cache/opencode/node_modules/` | — |

Load order: global config → project config → global plugin dir → project plugin dir. [OFFICIAL]

### Plugin / marketplace mechanics
- No formal marketplace; plugins distributed as **npm packages** or **local directories**. [OFFICIAL]
- Plugin install: add npm name to `opencode.json` `plugin` array — Bun installs automatically on next launch. [OFFICIAL]
- Versioning: standard npm semver. [OFFICIAL]
- TypeScript types via `@opencode-ai/plugin`. [OFFICIAL]

### Recency
Latest stable: **v1.14.27** released 2026-04-27 (one day after this report; 778 total releases — extremely high cadence). Plugin API and rich hook surface are 2025-2026 additions. [OFFICIAL]

---

## 3. Codex CLI (OpenAI)

### Extension points available
- **AGENTS.md** instruction files (project + global) [OFFICIAL]
- **Custom prompts** at `~/.codex/prompts/*.md` (deprecated in favor of skills as of late-2025/early-2026) [OFFICIAL]
- **Skills** — `SKILL.md` directories scanned across multiple scopes, **interoperable with Claude/Anthropic-style skills** [OFFICIAL]
- **MCP servers** in `~/.codex/config.toml` [OFFICIAL]
- **Slash commands** (built-ins; user-defined ones now route through prompts and skills) [OFFICIAL]
- **Notifications hook** — config triggers shell command on agent turn completion [OFFICIAL]
- **No first-class hook system** comparable to Claude Code — sandbox + notifications + MCP are the integration points. [UNVERIFIED]

### Manifest format

**SKILL.md** (matches Claude Code / Anthropic Agent Skills standard):
```yaml
---
name: skill-name
description: When this skill should and should not trigger
---
Skill body...
```
Optional: `scripts/`, `references/`, `assets/`, `agents/openai.yaml` (for Codex-specific UI/policy/tool deps). [OFFICIAL]

**AGENTS.md**: plain markdown, no required frontmatter. Concatenated broadest→narrowest scope, max 32 KiB combined by default. Override with `AGENTS.override.md`. [OFFICIAL]

**Custom prompt frontmatter** (deprecated path):
```yaml
---
description: Brief shown in command menu
argument-hint: TICKET_ID=<id> FILE=<path>
---
Body with $1..$9, $ARGUMENTS, $FILE (named), $$ for literal $.
```

**`~/.codex/config.toml` (TOML)**:
```toml
[mcp_servers.docs]
command = "docs-server"
supports_parallel_tool_calls = true
default_tools_approval_mode = "approve"

[mcp_servers.docs.tools.search]
approval_mode = "prompt"

[[skills.config]]
path = "/abs/path/skill/SKILL.md"
enabled = false
```

### Invocation lifecycle
- **AGENTS.md**: read once per run, before any tool work, concatenated for instruction chain. [OFFICIAL]
- **Prompts**: `/prompts:name` in REPL, or `/` to open menu. [OFFICIAL]
- **Skills**: `/skills` to list, `$` to mention; Codex can auto-select based on description match. Activated via `codex --enable skills`. [OFFICIAL]
- **MCP**: per-server and per-tool approval modes; `supports_parallel_tool_calls` enables concurrent execution for safe servers. [OFFICIAL]

### Permissioning / sandboxing
- Codex sandbox modes (CLI flag `--sandbox`):
  - `read-only` — default, no writes
  - `workspace-write` — writes inside workspace
  - `danger-full-access` — anything goes
  [OFFICIAL — referenced in cli docs and changelog, exact section page returned 404 on fetch]
- Per-tool approval modes via `mcp_servers.<server>.tools.<tool>.approval_mode = "approve|prompt|never"`. [OFFICIAL]
- Custom CA via `CODEX_CA_CERTIFICATE` env. [OFFICIAL]

### File load paths
| Scope | AGENTS.md | Prompts | Skills | MCP / Config |
|---|---|---|---|---|
| Global | `~/.codex/AGENTS.md` (+ `.override.md`) | `~/.codex/prompts/*.md` | `~/.agents/skills/<name>/SKILL.md`, `~/.codex/skills/<name>/SKILL.md` | `~/.codex/config.toml` |
| Admin | — | — | `/etc/codex/skills/` | — |
| Project | walked from git root down | (not directory-scoped) | `.agents/skills/`, also discovered in working tree | — |

The use of `.agents/skills/` as a project-local skills dir is a **deliberate cross-tool convention** — Goose also reads it. [OFFICIAL — Codex docs]; [PRAC — community report].

### Plugin / marketplace mechanics
- **Skills Catalog**: `github.com/openai/skills` is the official Codex skills catalog. [OFFICIAL]
- **No formal plugin format.** Skills + AGENTS.md + MCP are the units of distribution; sharing is by `cp -r` or git clone. [OFFICIAL — implicit from docs]
- Versioning: per-skill via git, no manifest version field. [UNVERIFIED]

### Recency
- v0.125.0 as of April 2026 (Rust 96.3%). [OFFICIAL — repo header]
- Skills landed in Codex Dec 2025; expanded Jan-April 2026. Custom prompts marked deprecated in favor of skills in 2026. [OFFICIAL — developers.openai.com/codex/custom-prompts and changelog]

---

## 4. Gemini CLI (google-gemini/gemini-cli)

### Extension points available
- **Extensions** — installable bundles via `gemini-extension.json` manifest [OFFICIAL]
- **Custom commands** (TOML files in extension's `commands/` dir) [OFFICIAL]
- **Hooks** (`hooks/hooks.json` inside an extension) [OFFICIAL]
- **Agent Skills** (`skills/` dir inside extension) [OFFICIAL]
- **Sub-agents** (`agents/` dir inside extension) [OFFICIAL]
- **Policies** (`policies/` dir inside extension) [OFFICIAL]
- **Themes** (custom UI themes) [OFFICIAL]
- **Context files** — `GEMINI.md` (analogous to AGENTS.md) [OFFICIAL]
- **MCP servers** in `~/.gemini/settings.json` or via extension manifest [OFFICIAL]

### Manifest format

**`gemini-extension.json`** [OFFICIAL]:
```json
{
  "name": "my-extension",
  "version": "1.2.0",
  "description": "...",
  "contextFileName": "GEMINI.md",
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "$GITHUB_TOKEN" },
      "cwd": "."
    }
  },
  "excludeTools": ["WebFetch"],
  "migratedTo": "https://github.com/owner/new-repo",
  "settings": { /* user-provided values stored in .env */ },
  "themes": [ /* ... */ ]
}
```
Required: `name` (lowercase, dashes, must match dir name) and `version`. [OFFICIAL]

**Extension directory layout**:
```
my-extension/
├── gemini-extension.json
├── GEMINI.md
├── commands/        # TOML custom commands
├── hooks/hooks.json
├── skills/
├── agents/
└── policies/
```

**Settings (`~/.gemini/settings.json`)** holds top-level `mcpServers`, `mcp.serverCommand`, `mcp.allowed[]`, `mcp.excluded[]`. [OFFICIAL]

### Invocation lifecycle
- Extensions load at startup. [OFFICIAL]
- Workspace configurations take precedence over extension settings during merge. [OFFICIAL]
- Custom commands invoked as `/command-name`. [OFFICIAL]
- Skills auto-invoked by description; sub-agents delegated. [OFFICIAL]
- Hooks fire on declared events (event surface less documented than Claude Code's). [UNVERIFIED]

### Permissioning / sandboxing
- Sandbox via Docker/Podman or macOS Seatbelt (`--sandbox` flag). [OFFICIAL — geminicli.com docs]
- `policies/` in extensions can declare safety rules. [OFFICIAL]
- `mcp.allowed`/`mcp.excluded` allow-listing of MCP server names. [OFFICIAL]

### File load paths
| Scope | Path |
|---|---|
| User extensions | `~/.gemini/extensions/<name>/` |
| Settings | `~/.gemini/settings.json` |
| Project context | `./GEMINI.md` |
| Workspace settings | `.gemini/settings.json` (project-local) |

### Plugin / marketplace mechanics
- **Extensions Gallery** at geminicli.com/extensions/. [OFFICIAL]
- Install: `gemini extensions install https://github.com/<owner>/<repo>` [OFFICIAL]
- Update: `gemini extensions update <name>` (extensions are *copies*, not symlinks; explicit update required). [OFFICIAL]
- Link for dev: `gemini extensions link <local-path>`. [OFFICIAL]
- Migration: `migratedTo` field redirects users automatically. [OFFICIAL]
- Versioning: manifest `version` field. [OFFICIAL]

### Recency
- v0.39.1 (2026-04-24). 468 releases tracked. Weekly stable cadence. [OFFICIAL]
- Extension system substantially expanded 2025-2026 with skills/sub-agents/policies. [OFFICIAL]

---

## 5. Goose (block/goose)

### Extension points available
- **Extensions** — multiple types (`stdio`, `builtin`, `platform`, `streamable_http`, `frontend`, `inline_python`) [OFFICIAL]
- **Recipes** — declarative reusable workflows (YAML) [OFFICIAL]
- **MCP servers** (70+ via MCP protocol) [OFFICIAL]
- **ACP support** [OFFICIAL]
- **Skills** — reads `.agents/skills`, `.claude/skills`, `.codex/skills`, `.cursor/skills` directories — explicit cross-agent skill compatibility [OFFICIAL]
- **Custom distros** — preconfigured Goose builds with branding [OFFICIAL]
- **Sub-recipes** for nested specialized tasks [OFFICIAL]
- **Toolkits** (legacy term; now subsumed under Extensions) [PRAC]

### Manifest format

**Recipe (YAML)** [OFFICIAL — referenced in repo `recipe.yaml` and docs]:
```yaml
version: "1.0"
title: Migrate API endpoints
description: Refactor legacy API
instructions: |
  You are working on...
prompt: "Start with $endpoint"
parameters:
  - key: endpoint
    input_type: string
    requirement: required
extensions:
  - type: stdio
    name: filesystem
    cmd: npx
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    env_keys: ["NODE_ENV"]
    timeout: 30000
    description: ...
  - type: builtin
    name: developer
  - type: streamable_http
    name: remote-svc
    uri: https://example.com/mcp
  - type: inline_python
    name: helper
    code: |
      def hello(): print("hi")
response:
  json_schema: { ... }       # optional structured output
retry:
  max_retries: 3
```

**Goose config (`~/.config/goose/config.yaml`)** holds provider keys, default extensions, model selection. [OFFICIAL]

### Invocation lifecycle
- Recipes execute via `goose run --recipe path/to/recipe.yaml` or interactive selection. [OFFICIAL]
- Extensions enabled per-session or globally; tools surface through standard MCP-style tool catalog. [OFFICIAL]
- Skills auto-discovered from cross-agent paths and applied based on description match. [OFFICIAL]

### Permissioning / sandboxing
- Per-extension enable/disable; no granular tool-level allow/deny in core (per docs). [OFFICIAL]
- Recipes can declare required extensions; missing ones either prompt install or fail. [OFFICIAL]
- Sandboxing relies on each MCP server's own behavior. [UNVERIFIED]

### File load paths
| Scope | Path |
|---|---|
| User config | `~/.config/goose/config.yaml` |
| Recipes | repo-local YAML, or `~/.config/goose/recipes/` |
| Skills | `.agents/skills/`, `.claude/skills/`, `.codex/skills/`, `.cursor/skills/` (cross-tool) |
| Workflow recipes | `workflow_recipes/` in repo root |

### Plugin / marketplace mechanics
- No central app-style marketplace; recipes shared via git/gist. [OFFICIAL]
- Custom Distributions allow shipping a Goose binary with bundled extensions and provider configs. [OFFICIAL]
- Versioning: recipe `version` field; extensions follow their MCP server versioning. [OFFICIAL]

### Recency
- v1.32.0 (2026-04-23). 130 total releases. 4,285 commits, very active. [OFFICIAL]
- Cross-tool skill directory reading (`.claude/skills`, `.codex/skills`) is a 2025-2026 deliberate compatibility play. [OFFICIAL — repo evidence]

---

## 6. ForgeCode (tailcallhq/forgecode)

### Extension points available
- **Skills** (`SKILL.md` — Claude Code-compatible) [OFFICIAL]
- **Custom Agents** (markdown + YAML frontmatter, `.forge/agents/`) [OFFICIAL]
- **Custom Commands** (YAML in `.forge/commands/` or inline in `forge.yaml`) [OFFICIAL]
- **MCP servers** (`.mcp.json` — same shape as Claude Code's) [OFFICIAL]
- **AGENTS.md** project rules file [OFFICIAL]
- **Permissions policies** (`permissions.yaml`) [OFFICIAL]
- **Three built-in agents**: `forge` (build), `sage`/`:ask` (research, read-only), `muse`/`:plan` (planning, read-only) [OFFICIAL]
- **Semantic codebase index** via `:sync` (built-in command for vector search) [OFFICIAL]

### Manifest format

**Custom agent** (`.forge/agents/<name>.md`) [OFFICIAL]:
```yaml
---
name: reviewer
description: Reviews PRs adversarially
model: claude-3.7-sonnet
tools: [read, search]
system_prompt: ...
---
Body...
```

**Custom command** (YAML) [OFFICIAL]:
```yaml
name: tests
description: Run the project test suite
prompt: |
  Run `npm test` and summarize failures.
```
Or inline in `forge.yaml`:
```yaml
model: "claude-3.7-sonnet"
temperature: 0.7
max_walker_depth: 3
max_tool_failure_per_turn: 3
max_requests_per_turn: 50
custom_rules: |
  Team guidelines and conventions
commands:
  - name: tests
    description: ...
    prompt: ...
```

**`.mcp.json`** (Claude Code-compatible) [OFFICIAL]:
```json
{
  "mcpServers": {
    "server_name": {
      "command": "command_to_execute",
      "args": ["arg1"],
      "env": { "VAR": "value" }
    }
  }
}
```

**`permissions.yaml`** [OFFICIAL]:
```yaml
policies:
  - permission: allow      # allow | deny | confirm
    rule:
      read: "**/*"
  - permission: confirm
    rule:
      command: "rm *"
  - permission: deny
    rule:
      url: "*"
```
Operation types: `read`, `write`, `command`, `url`. [OFFICIAL]

**SKILL.md**: identical to Anthropic Agent Skills standard. ForgeCode docs explicitly state `cp -r .claude/skills .forge/skills` works without conversion. [OFFICIAL]

### Invocation lifecycle
- AGENTS.md loaded at session start (analogous to Codex). [OFFICIAL]
- Skills auto-applied by relevance to description, or via `:skill` to list. [OFFICIAL]
- Three-agent harness: `:plan` (Muse) → `:ask` (Sage) → default Forge for execution. [OFFICIAL]
- Commands invoked as `:commandname`. [OFFICIAL]

### Permissioning / sandboxing
- "Restricted mode" gates all tool execution through `permissions.yaml`. [OFFICIAL]
- **Hybrid default** — when restricted mode is on but no rule matches, fallback is `confirm` (user prompt), not deny. [OFFICIAL]
- Default policy as auto-generated: allow everything (so enabling restricted mode alone does **not** make it stricter — must write deny rules). [OFFICIAL]
- This is a **default-ask** model, not default-deny. [OFFICIAL]

### File load paths
| Scope | Skills | Agents | Commands | MCP | Config |
|---|---|---|---|---|---|
| Global | `~/forge/skills/<name>/SKILL.md` | `~/forge/agents/` | `~/forge/commands/` | `~/forge/.mcp.json` | `~/forge/.forge.toml`, `~/forge/AGENTS.md` |
| Project | `.forge/skills/<name>/SKILL.md` | `.forge/agents/` | `.forge/commands/` | `.mcp.json` | `forge.yaml`, `AGENTS.md` |
| Cross-tool | also reads `~/.agents/skills/` | — | — | — | — |

Project-level overrides global. [OFFICIAL]

### Plugin / marketplace mechanics
- No formal plugin/marketplace. Distribution is via git: clone a repo's `.forge/` into your own. [OFFICIAL]
- Versioning: per-component, follow the host repo's git history. [UNVERIFIED]
- `forge.yaml` supports `custom_rules` for inline team conventions. [OFFICIAL]

### Recency
- v2.12.9 (2026-04-26 — same day as this report). 345+ releases. [OFFICIAL]
- Top of TermBench 2.0 leaderboard as of April 2026 (per Medium article and forgecode.dev). [PRAC]
- Harness-first architecture (3 specialized agents) is the core 2026 differentiator. [PRAC]

---

## Comparison Matrix

### Extension surface

| Feature | Claude Code | OpenCode | Codex CLI | Gemini CLI | Goose | ForgeCode |
|---|---|---|---|---|---|---|
| SKILL.md (Anthropic standard) | ✅ native | partial (Agent Skills) | ✅ explicit | ✅ in extensions | ✅ reads cross-tool | ✅ explicit Claude-compat |
| Sub-agents | ✅ `.claude/agents/` | ✅ `.opencode/agents/` | partial (via skills `agents/openai.yaml`) | ✅ in extensions | via recipes/sub-recipes | ✅ `.forge/agents/` |
| Slash commands | ✅ (merged into skills) | ✅ `.opencode/commands/` | ✅ legacy prompts (deprecated) | ✅ TOML in extensions | ✅ via recipes | ✅ `:command` syntax |
| Hooks | ✅ 8 events | ✅ rich (Tool/Session/TUI/etc) | notifications only | ✅ `hooks/hooks.json` | extension-mediated | ❌ no native hooks |
| MCP servers | ✅ | ✅ local + remote + OAuth | ✅ TOML | ✅ in extensions | ✅ first-class | ✅ Claude-compat |
| Plugins | ✅ `.claude-plugin/plugin.json` | TS modules + npm | ❌ skills are unit | ✅ `gemini-extension.json` | recipes + custom distros | ❌ no plugin format |
| Marketplace | ✅ official + git | npm | github.com/openai/skills catalog | ✅ extensions gallery | informal | ❌ |
| LSP | ✅ in plugins | ✅ built-in | ❌ | ❌ | ❌ | ❌ |

### Manifest formats at a glance

| Agent | Plugin/Extension | Skill | Agent | Command | Hooks |
|---|---|---|---|---|---|
| Claude Code | `plugin.json` (JSON) | `SKILL.md` YAML frontmatter | `<name>.md` YAML frontmatter | `<name>.md` YAML frontmatter (legacy) | `settings.json` `hooks` key |
| OpenCode | TS module | `SKILL.md`-like | `<name>.md` YAML frontmatter | `<name>.md` YAML frontmatter | TS plugin event handlers |
| Codex CLI | n/a | `SKILL.md` (Anthropic spec) + optional `agents/openai.yaml` | (via skill) | `~/.codex/prompts/<name>.md` (deprecated) | TOML notifications |
| Gemini CLI | `gemini-extension.json` | inside extension `skills/` | inside extension `agents/` | TOML in `commands/` | `hooks/hooks.json` |
| Goose | `recipe.yaml` (also custom-distros) | cross-tool skill dirs | (via recipe) | (via recipe) | n/a |
| ForgeCode | `forge.yaml` (config) | `SKILL.md` (Anthropic-compat) | `<name>.md` YAML frontmatter | YAML | n/a (`permissions.yaml` is policy not hook) |

### Sandbox / permission models

| Agent | Default | Granularity | Override mechanism |
|---|---|---|---|
| Claude Code | default-ask | tool patterns: `Bash(git *)`, `Skill(name)` | settings.json `permissions`, skill `allowed-tools` |
| OpenCode | per-agent ask | `edit / bash / webfetch / task` tri-state | agent frontmatter `permission` block |
| Codex CLI | default-deny via sandbox modes | `read-only` / `workspace-write` / `danger-full-access` | CLI `--sandbox` flag, per-MCP-tool approval modes |
| Gemini CLI | sandbox via Docker/Podman/Seatbelt | `mcp.allowed`/`mcp.excluded`, `policies/` dir in extensions | `--sandbox` flag |
| Goose | per-extension enable | extension-level only (no per-tool) | `config.yaml` |
| ForgeCode | default-ask (via "restricted mode") | `read / write / command / url` ops with glob rules | `permissions.yaml` policies |

### File-path conventions (project scope)

| Agent | Project root | Global root |
|---|---|---|
| Claude Code | `.claude/` | `~/.claude/` |
| OpenCode | `.opencode/` | `~/.config/opencode/` |
| Codex CLI | `AGENTS.md`, `.agents/skills/` | `~/.codex/`, `~/.agents/skills/` |
| Gemini CLI | `.gemini/` (workspace settings), `GEMINI.md` | `~/.gemini/extensions/` |
| Goose | `.agents/skills/` (cross-tool), `recipe.yaml` files | `~/.config/goose/` |
| ForgeCode | `.forge/`, `forge.yaml`, `AGENTS.md`, `.mcp.json`, `permissions.yaml` | `~/forge/` |

### Convergence points (2026-04-26)
1. **`SKILL.md` with YAML frontmatter is now the de facto cross-tool skill format.** Claude Code, Codex, ForgeCode use it natively; Gemini CLI and Goose can host or read it. OpenCode has Agent Skills referenced in nav.
2. **MCP is universal.** All six agents speak Model Context Protocol; configuration shapes are nearly identical (command/args/env).
3. **AGENTS.md / GEMINI.md / CLAUDE.md project-context files** are converging into a parallel pattern — markdown, no required frontmatter, hierarchical concatenation.
4. **Cross-tool skill directory awareness**: Goose explicitly reads `.claude/skills`, `.codex/skills`, `.cursor/skills`. ForgeCode reads `~/.agents/skills/`. This is *the* lowest-friction multi-agent deployment path.

### Divergence points
1. **Plugin packaging** is fractured: JSON (Claude/Gemini), TypeScript module (OpenCode), git-clone (Codex/ForgeCode), YAML recipes (Goose).
2. **Hook surfaces** differ enormously — Claude Code (8 events), OpenCode (12+ event categories), others minimal-to-none.
3. **Permission models** range from default-deny sandbox modes (Codex) to default-ask glob policies (ForgeCode) to per-agent tri-state blocks (OpenCode).
4. **Marketplaces**: Claude Code and Gemini CLI have official galleries; the rest rely on git or npm.
5. **Sub-agent semantics**: Claude Code has rich preload-skills + delegation; Gemini bundles agents in extensions; Goose uses sub-recipes; ForgeCode has a fixed three-agent harness as primary architecture.

### Implications for Momentum's multi-agent deployment

- **Single-source-of-truth path: SKILL.md.** Authoring all practice modules as Anthropic-spec SKILL.md files gives free coverage in Claude Code, Codex, ForgeCode, and (via cross-tool dir reads) Goose.
- **Adapter shim for Gemini CLI** would package skills inside a `gemini-extension.json` bundle — minimal boilerplate over the same SKILL.md content.
- **OpenCode adapter** would emit `<name>.md` agent + command files rather than skills (the Skills page being 404 on 2026-04-26 suggests Skills support is in flux).
- **Hook portability is hopeless** — Claude Code hook config does not translate; deploy hooks only on Claude Code and rely on skill-internal logic elsewhere.
- **MCP servers are a portability win** — author MCP servers once, install via each agent's MCP config block.
- **Permission policies do not portably map.** Per-target permission scaffolding is required.
- **Distribution: git-first beats marketplace-first.** Every agent except OpenCode handles git URLs; an `install.sh` that drops files into the right per-agent paths reaches all six.

---

## Sources

### Claude Code [OFFICIAL]
- Skills: https://code.claude.com/docs/en/skills
- Sub-agents: https://code.claude.com/docs/en/sub-agents
- Slash commands: https://code.claude.com/docs/en/slash-commands
- Hooks: https://code.claude.com/docs/en/hooks
- Plugins: https://code.claude.com/docs/en/plugins
- MCP: https://code.claude.com/docs/en/mcp

### OpenCode [OFFICIAL]
- Agents: https://opencode.ai/docs/agents
- Plugins: https://opencode.ai/docs/plugins
- Commands: https://opencode.ai/docs/commands
- MCP servers: https://opencode.ai/docs/mcp-servers
- Repo: https://github.com/sst/opencode (v1.14.27, 2026-04-27)

### Codex CLI [OFFICIAL]
- Repo: https://github.com/openai/codex
- AGENTS.md guide: https://developers.openai.com/codex/guides/agents-md
- Custom prompts: https://developers.openai.com/codex/custom-prompts
- Skills: https://developers.openai.com/codex/skills
- Skills catalog: https://github.com/openai/skills
- Config (TOML): https://github.com/openai/codex/blob/main/docs/config.md
- CLI: https://developers.openai.com/codex/cli

### Gemini CLI [OFFICIAL]
- Repo: https://github.com/google-gemini/gemini-cli
- Extensions intro: https://geminicli.com/docs/extensions/
- MCP setup: https://geminicli.com/docs/cli/tutorials/mcp-setup/
- MCP server doc: https://geminicli.com/docs/tools/mcp-server/
- Extensions reference (in-repo): https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md

### Goose [OFFICIAL]
- Repo: https://github.com/block/goose (v1.32.0, 2026-04-23)
- Recipe reference: https://block.github.io/goose/docs/guides/recipes/recipe-reference/
- Sub-recipes: https://block.github.io/goose/docs/guides/recipes/sub-recipes/
- Recipe.yaml example: https://github.com/block/goose/blob/main/recipe.yaml

### ForgeCode [OFFICIAL]
- Repo: https://github.com/tailcallhq/forgecode (v2.12.9, 2026-04-26)
- Site: https://forgecode.dev/
- Skills: https://forgecode.dev/docs/skills/
- Permissions: https://forgecode.dev/docs/permissions/
- Docs root: https://forgecode.dev/docs

### Practitioner / context [PRAC]
- ForgeCode TermBench 2.0 deep-dive (Hightower, Medium, April 2026): https://medium.com/@richardhightower/forgecode-dominating-terminal-bench-2-0-harness-engineering-beat-claude-code-codex-gemini-etc-eb5df74a3fa4
- 2026 Coding CLI Tools Comparison (Tembo): https://www.tembo.io/blog/coding-cli-tools-comparison
- Awesome Claude plugins (adoption metrics): https://github.com/quemsah/awesome-claude-plugins
- Awesome CLI coding agents (directory): https://github.com/bradAGI/awesome-cli-coding-agents
- "OpenAI are quietly adopting skills" (Simon Willison, Dec 2025): https://simonwillison.net/2025/Dec/12/openai-skills/
- "Skills in OpenAI Codex" (fsck.com, Dec 2025): https://blog.fsck.com/2025/12/19/codex-skills/
- Building Gemini CLI Extensions guide (Tanaike): https://gist.github.com/tanaikech/0a1426535ab3af0c68cf8d79bca770a0
- Goose Recipes guide (Shreyanshrewa, Medium): https://medium.com/@shreyanshrewa/creating-and-sharing-effective-goose-recipes-abf9767d5128
- Goose Extension Types (DeepWiki): https://deepwiki.com/block/goose/5.3-extension-types-and-configuration

### Standards
- Agent Skills open standard: https://agentskills.io
