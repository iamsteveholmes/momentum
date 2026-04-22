---
content_origin: claude-code-subagent
date: 2026-04-22
sub_question: "How do CLI coding agents compare to Claude Code on feature parity (sub-agents, slash commands/skills, hooks, MCP, tool use, plan mode, ecosystem)?"
topic: "CMUX-integrated coding agents with LLM marketplace support as Claude Code replacements"
---

# Feature Parity: CLI Coding Agents vs. Claude Code

This report compares the current (2026-03/04) state of the major CLI coding agents against the Claude Code baseline on seven axes: sub-agents, slash commands / skills, hooks, MCP, tool use, plan mode, and ecosystem maturity. Priority deep-dive on **opencode** (SST) and **OpenAI Codex CLI** as the most Claude-Code-like options that also intersect the "multi-provider LLM" and "CMUX-friendly terminal-native" constraints.

## TL;DR

- **opencode** and **Codex CLI** both ship near-full parity with Claude Code on every axis that matters: markdown-defined sub-agents with per-agent models, markdown/YAML custom slash commands, `SKILL.md` Agent Skills, lifecycle hooks (including blocking `PreToolUse`), MCP client (stdio + HTTP), plan mode, and a plugin/extension marketplace. [OFFICIAL]
- **opencode** has the widest provider coverage (75+ via AI SDK + Models.dev) and the deepest hooks surface (28 lifecycle events vs. Codex's 6). [OFFICIAL]
- **Codex CLI** is narrower (OpenAI-centric) and its hooks currently only fire on Bash tools, but it has Agent Skills governance and MCP namespacing that Claude Code doesn't. [OFFICIAL]
- **Gemini CLI** shipped a Claude-Code-shaped extension system (sub-agents + skills + hooks + MCP + commands bundled as installable extensions) but is Gemini-tied. [OFFICIAL]
- **Cursor CLI**, **Amp**, **Cline**, **Crush**, **OpenHands**, **Continue**, **Aider** each occupy partial-parity niches — documented below.

## Claude Code baseline (reference, 2026-04)

Sub-agents via Task tool with markdown definitions in `.claude/agents/`; Agent Skills as `SKILL.md` with YAML frontmatter; hooks for `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `Stop` configured in `settings.json`; MCP as client over stdio/http/SSE; plan mode (read-only, enforced via tool filtering); built-in Read/Write/Edit/Bash/Glob/Grep/WebSearch/WebFetch plus custom MCP tools; plugin marketplaces via `/plugin`. [OFFICIAL]

## Comparison Matrix

| Agent | Sub-agents | Slash cmds / Skills | Hooks | MCP | Plan mode | Tool use | Ecosystem |
|---|---|---|---|---|---|---|---|
| **Claude Code** (baseline) | ✅ `.claude/agents/*.md` | ✅ slash cmds + SKILL.md | ✅ 5+ events, blocking | ✅ client (stdio/http/SSE) | ✅ read-only filter | ✅ built-ins + MCP | ✅ `/plugin` marketplaces |
| **opencode** (SST) | ✅ primary + subagents, per-agent model | ✅ slash cmds + SKILL.md | ✅ 28 events, blocking | ✅ client (local+remote) | ✅ Plan vs Build modes | ✅ built-ins + MCP + custom tools | ✅ plugins npm + awesome-opencode, 116–146k stars |
| **Codex CLI** (OpenAI) | ✅ `[agents]` in config.toml | ✅ /prompts + SKILL.md (skills replacing prompts) | ✅ 6 events, blocking (Bash-only scope) | ✅ client + can run AS server | ✅ `/plan` slash | ✅ built-ins + MCP Apps + namespacing | 🟡 growing, OpenAI-first |
| **Gemini CLI** | ✅ via extensions `agents/` | ✅ extensions bundle cmds + skills | ✅ via extensions | ✅ client | 🟡 not a first-class mode | ✅ built-ins + MCP | ✅ Extension gallery |
| **Cursor CLI** | ✅ `.cursor/agents/*.md` (reads `.claude/agents/` too) | ✅ skills + commands | ✅ hooks | ✅ client, JSON in `.cursor` | 🟡 IDE-primary | ✅ built-ins + MCP | ✅ Cursor Marketplace, plugins |
| **Amp** (Sourcegraph) | ✅ parallel subagents (Oracle, Librarian) | ↗ skills via markdown | ✅ `amp.hooks` array | ✅ client + Sourcegraph MCP | ✅ Deep mode | ✅ built-ins + MCP | 🟡 enterprise-gated 2026 |
| **Cline** | 🟡 Roo-fork has modes; Cline invests in MCP+CLI | ↗ via MCP Rules (keyword triggers) | ✅ hooks (macOS/Linux) | ✅ MCP Marketplace, one-click | 🟡 plan/act in VSCode, not CLI-first | ✅ built-ins + MCP | ✅ MCP Marketplace |
| **Crush** (Charm) | ❌ not documented | ↗ SKILL.md Agent Skills open standard | ❌ not documented | ✅ stdio/http/sse + Docker MCP | ❌ not documented | ✅ built-ins + MCP + LSP | 🟡 TUI polish, newer |
| **OpenHands** | ✅ delegation tool, hierarchical | ✅ markdown skills, `.openhands/skills/` | ✅ `HookExecutionEvent` | ✅ client | 🟡 not first-class | ✅ typed tool system | ✅ plugins package everything |
| **Continue** | ↗ agents via config | ✅ slash cmds, MCP prompts → slash | ❌ not documented | ✅ client, MCP prompts auto-bind | ❌ not documented | ✅ built-ins + MCP | ✅ config.yaml, context providers |
| **Aider** | ❌ single-agent | ↗ `/add /drop /model` (different model) | ❌ not documented | ❌ not native (experimental bridge) | ↗ `/ask` mode is read-only-ish | ✅ built-ins only | 🟡 mature but narrower |

Legend: ✅ full parity · 🟡 partial · ❌ none · ↗ different model

---

## opencode (SST) — deep dive

**Verdict: Claude Code parity or better across every axis, plus 75+ providers.**

### Sub-agents [OFFICIAL]
Two-tier model: **primary agents** (Build, Plan ship built-in; switch with Tab) and **subagents** (invoked by `@mention` or auto-invoked by primary via Task). Defined either in `opencode.json` (`agent: { review: { mode: "subagent", ... } }`) or as markdown with YAML frontmatter in `~/.config/opencode/agents/` (global) or `.opencode/agents/` (project). Frontmatter supports `description`, `mode`, `model`, `temperature`, `tools`. Filename becomes agent name. Each agent can pin its own model; subagents inherit parent's model if unset. Task-tool permissions gate which subagents a primary can invoke, with glob patterns per sub-agent (`allow` / `ask` / `deny`).

### Slash commands + Agent Skills [OFFICIAL]
`SKILL.md` files with YAML frontmatter (`name`, `description`, optional `license`, `compatibility`, `metadata`). Discovered in `.opencode/skills/<name>/SKILL.md`, `~/.config/opencode/skills/<name>/SKILL.md`, **and** Anthropic-compatible `.claude/skills/` and `.agents/skills/` paths — meaning skills portability is built in. Agents load them on-demand via a native `skill` tool, not always-on injection. Built-in slash commands: `/connect`, `/init`, `/undo`, `/redo`, `/share`.

### Hooks [OFFICIAL]
**28 lifecycle events** — the broadest surface of any agent in this survey:
- Tool: `tool.execute.before` (blocking pre-interception), `tool.execute.after`
- Session: `session.created`, `session.compacted`, `session.deleted`, `session.diff`, `session.error`, `session.idle`, `session.status`, `session.updated`
- Message: `message.part.removed`, `message.part.updated`, `message.removed`, `message.updated`
- Permission: `permission.asked`, `permission.replied`
- File: `file.edited`, `file.watcher.updated`
- LSP: `lsp.client.diagnostics`, `lsp.updated`
- TUI: `tui.prompt.append`, `tui.command.execute`, `tui.toast.show`
- Plus: `command.executed`, `installation.updated`, `server.connected`, `todo.updated`, `shell.env`

Plugins are JS/TS files in a plugin dir or referenced via npm packages in config. [OFFICIAL]

### MCP [OFFICIAL]
Both local (stdio) and remote (HTTP) MCP servers via `mcp` key in config. Tools auto-exposed to LLM alongside built-ins. No mention of opencode acting as MCP server.

### Plan mode [OFFICIAL]
First-class **Plan vs Build** modes, Tab to switch. Plan is read-only. Each mode can pin its own model — e.g. Haiku for planning, Sonnet for build. Configurable via permissions field (tools property is deprecated).

### Tool use [OFFICIAL]
Built-ins + MCP + plugin-defined custom tools. Per-agent and per-tool permissions with glob patterns (e.g. `"bash": { "git *": "ask", "grep *": "allow" }`).

### Ecosystem [OFFICIAL] [UNVERIFIED stars count]
116k–146k GitHub stars (sources vary); 864 contributors; 11.6k+ commits; releases hourly. `awesome-opencode` curated list; npm-based plugin distribution; 75+ providers via AI SDK and Models.dev including Anthropic, OpenAI, Gemini, Bedrock, Groq, Azure, OpenRouter, Vercel AI Gateway, Ollama, LM Studio, any OpenAI-compatible endpoint. **Note**: Anthropic blocked third-party Claude auth in Jan 2026, which drove an 18k-star surge for opencode as developers sought alternatives — but this means direct Anthropic Claude access via opencode is now restricted (GPT and Copilot-provided models still work). [PRAC]

---

## OpenAI Codex CLI — deep dive

**Verdict: Substantial parity, OpenAI-centric, narrower hooks scope than opencode but adds MCP namespacing + sandbox metadata Claude Code lacks.**

### Sub-agents [OFFICIAL]
Configured under `[agents]` in `~/.codex/config.toml`. "Codex only spawns subagents when you explicitly ask it to" — no auto-delegation by default. Each subagent does its own model and tool work (higher token cost than single-agent). `/review` ships as a built-in specialist agent for diff analysis.

### Slash commands + Skills [OFFICIAL]
Built-ins include `/model`, `/fast`, `/plan`, `/personality`, `/clear`, `/new`, `/resume`, `/fork`, `/diff`, `/status`, `/review`, `/permissions`, `/experimental`, `/statusline`, `/copy`, `/compact`, `/mention`. Custom prompts were originally markdown files in `~/.codex/prompts/` with YAML frontmatter (`description`, `argument-hint`) invoked as `/prompts:<name>` — **but custom prompts are now deprecated in favor of Agent Skills** (`SKILL.md`). The 0.114 release positioned this as "Skill governance". [OFFICIAL]

### Hooks [OFFICIAL]
**6 events**, configured in `~/.codex/hooks.json` or `<repo>/.codex/hooks.json`:
- `SessionStart` (observing, can add context)
- `PreToolUse` (blocking; **Bash only** currently)
- `PermissionRequest` (blocking)
- `PostToolUse` (Bash only; can return `continue: false` though command already ran)
- `UserPromptSubmit` (blocking)
- `Stop` (blocking)

JSON-over-stdin schema with `session_id`, `cwd`, `hook_event_name`, `model`; output supports `continue`, `stopReason`, `systemMessage`. Explicit design intent to match Claude Code's blocking-PreToolUse / observing-PostToolUse split.

### MCP [OFFICIAL]
Stdio **and** streamable HTTP; OAuth + Bearer auth. Servers defined in `~/.codex/config.toml` or managed via `codex mcp` CLI. Codex **can also run as an MCP server** ("when you need it inside another agent") — Claude Code does not advertise this. Recent additions: MCP Apps tool calls, namespaced MCP registration, parallel-call opt-in, sandbox-state metadata.

### Plan mode [OFFICIAL]
Dedicated `/plan` slash command that enters plan mode to propose execution strategies before changes. Permissions have three tiers: Auto, Read-only, Full Access, controllable via `/permissions`.

### Tool use [OFFICIAL]
Built-ins for shell, file ops, web search (cached or live), image input + generation; MCP for the rest. Non-interactive `codex exec` for CI/automation. Remote TUI via WebSocket with capability tokens.

### Ecosystem [OFFICIAL] [UNVERIFIED size]
OpenAI developer docs well-maintained; `AGENTS.md` convention is cross-agent (Cursor, Amp, etc. also read it); `codex-settings` community repos growing. OpenAI-first — other providers via MCP adapters is non-native. Codex 0.114.0 shipped Code Mode + Hooks + Skill Governance as the "operations release." [PRAC]

---

## Charm Crush

**Verdict: Partial — strong TUI + MCP + multi-provider, but missing hooks/sub-agents/plan-mode docs.**

Multi-model (switch mid-session via `/model groq-llama3-70b`), LSP context, MCP over stdio/http/sse, Agent Skills support via `SKILL.md` open standard loading from `.agents/skills` and similar paths. Configuration in JSON (`.crush.json`, `crush.json`, or `$HOME/.config/crush/crush.json`). Docker MCP Catalog integration. **Not documented**: sub-agents, custom slash commands, hooks, plan mode, plugins beyond MCP. Fine-grained tool permissions. [OFFICIAL]

---

## OpenHands

**Verdict: Parity on most axes via SDK/plugin system; plan mode not first-class.**

"Plugins bundle skills, hooks, MCP servers, agents, and commands into reusable packages." Skills as markdown files in `.openhands/skills/` or compatible formats (`.cursorrules`, `agents.md`), either always-active (trigger=None) or keyword-triggered. Skills can include MCP tools. Hierarchical agent coordination via a delegation tool — sub-agents as independent conversations inheriting parent's model + workspace. Hooks gained observability via `HookExecutionEvent`. Marketplace paths configurable; enable/disable for installed skills/plugins since v1.12+. [OFFICIAL]

---

## Aider

**Verdict: Narrowest parity. Commands like `/add`, `/drop`, `/model` are workflow shortcuts, not extensible skills.**

No native MCP support as of 2026 (experimental `mcpm-aider` bridge). No sub-agents. No hooks. No plan mode in the Claude Code sense (though `/ask` is an observing-only mode). Built-in toolset only. Mature, but the feature surface has not followed the Claude Code / opencode convergence. [OFFICIAL] [PRAC]

---

## Cline

**Verdict: Strong MCP story, hooks shipped, but CLI is secondary — VSCode-first.**

MCP Marketplace with one-click install is the headline feature. Hooks "inject custom scripts at key workflow moments to validate operations, monitor usage, and shape AI decisions" — macOS/Linux only. MCP Rules group connected servers into functional categories with keyword triggers. Custom modes are Roo Code fork territory, not Cline proper. Plan/Act modes exist in VSCode UI. CLI 2.0 for terminal-first workflows is newer. [OFFICIAL]

---

## Continue

**Verdict: Partial. Strong slash commands + MCP, weaker on agents/hooks.**

CLI (`cn`) supports `/model`, `@` for file context, `/` for slash commands. Custom slash commands are named prompt templates with optional model routing. MCP prompts auto-convert to slash commands; MCP resources/templates expose as context providers via `MCPContextProvider`. Tool permission system with `~/.continue/permissions.yaml`. Context providers are first-class (open files, git diff, terminal output, doc URLs). Agents defined in `config.yaml` as composition of models + rules + tools. **No documented hooks system, no explicit plan mode, sub-agents are weaker.** [OFFICIAL]

---

## Gemini CLI

**Verdict: Surprisingly close to Claude Code — extensions package everything.**

> "Gemini CLI extensions package prompts, MCP servers, custom commands, themes, hooks, sub-agents, and agent skills into a familiar and user-friendly format." [OFFICIAL]

Skill definitions in `skills/<name>/SKILL.md`. Sub-agents via `.md` files in an `agents/` directory within the extension root. MCP via standard config. `GEMINI.md` as context file. Extension Gallery ranks by GitHub stars. Plan mode is not advertised as a first-class mode (same interaction model as /plan prompts). Gemini-tied on the model side. [OFFICIAL]

---

## Cursor CLI / Cursor Agent

**Verdict: Parity on paper, cross-ecosystem skills/agents loading is the differentiator.**

Sub-agents as markdown + YAML in `.cursor/agents/` **or** `.claude/agents/` (reads Claude Code definitions directly). Foreground / background execution modes. `readonly` flag for safety. MCP servers as JSON in `.cursor/`. Plugin Marketplace bundles skills + subagents + MCP + hooks + rules. Hooks for processing/saving subagent results. Subagents work "in editor, CLI, and Cloud Agents" — same definitions reused across surfaces. Plan mode is not a first-class CLI concept; IDE-first. [OFFICIAL]

---

## Amp (Sourcegraph)

**Verdict: Enterprise parity with Deep mode + parallel subagents; consumer plans discontinued.**

Runs multi-step tasks, spins up parallel subagents (Oracle for code, Librarian for external libs), ships as VS Code extension + CLI. **Hooks** via `amp.hooks` array in editor settings (`.vscode/settings.json`) — event + action pairs that "deterministically override Amp's behavior when AGENTS.md is not sufficient." Sourcegraph MCP for semantic code search across indexed repos. Deep mode = extended-reasoning autonomous research. **Public Free/Pro self-serve discontinued in late 2025; enterprise-only in 2026.** [OFFICIAL]

---

## Cross-cutting observations

1. **Agent Skills (`SKILL.md`) is becoming a de-facto standard.** Claude Code, opencode, Codex CLI, Crush, Cursor, Gemini CLI, OpenHands, and Amp all support some variant. Portability across agents is plausible in practice. [PRAC]

2. **AGENTS.md is the new CLAUDE.md.** Codex, Cursor, Amp, OpenHands all read `AGENTS.md`; opencode reads `AGENTS.md` alongside `opencode.md`; Claude Code reads `CLAUDE.md`. Some agents (Cursor, opencode) read both. [PRAC]

3. **Hook surface is a real differentiator.** opencode's 28 events >> Codex's 6 >> Claude Code's ~5 >> Cline's handful >> Amp's event+action pairs. For CMUX integration (where you want `PostToolUse` → pane creation, `SessionStart` → layout setup), opencode has the most material to work with. [OFFICIAL]

4. **MCP is table stakes.** Every major agent except Aider has it. Client support is universal; namespacing, sandbox metadata, parallel calls are current frontier (Codex leads here).

5. **Plan mode is inconsistent.** Claude Code and opencode treat it as a first-class mode with enforced tool filtering. Codex and Amp treat it as a slash command/deep-mode toggle. Gemini, Cursor, Continue, Crush, OpenHands, Cline (CLI), Aider don't have a directly equivalent read-only-enforced-by-harness mode.

6. **Multi-provider is opencode's and Crush's signature.** Codex (OpenAI), Gemini CLI (Google), and Amp are effectively single-provider on the model side. opencode (75+), Crush (any OpenAI-compatible), Cline, Continue are multi-provider-first. For the "multi-provider LLM marketplace" constraint of the parent research, this narrows to opencode / Crush / Cline / Continue as top candidates. [OFFICIAL]

7. **Ecosystem momentum favors opencode.** 116k+ stars, hourly releases, curated plugin index, and surge-driven contributor growth in early 2026. Claude Code has bigger install base via Anthropic distribution but is a closed-source harness. Codex has OpenAI's brand but tighter provider lock-in. [UNVERIFIED exact stars] [PRAC]

## Implications for the parent question (CMUX + multi-provider as Claude Code replacement)

- **opencode** is the strongest single candidate: full Claude Code feature parity, superset of hooks, 75+ providers, reads `.claude/` skill + agent paths, plugin system in TS/JS maps naturally to CMUX subprocess orchestration. Primary risk: Anthropic blocked third-party Claude auth in Jan 2026, so if the Momentum practice depends on Claude Opus/Sonnet, opencode cannot serve as a drop-in — GPT/Gemini/local only. [PRAC]
- **Codex CLI** is second-strongest on feature surface but model-locked to OpenAI for native use. MCP-as-server mode opens interesting composition patterns for CMUX + Momentum. Hooks are narrower (Bash-scope PreToolUse, 6 events).
- **Gemini CLI** has the cleanest extension model for packaging an entire practice (skills + agents + hooks + MCP + commands in one installable), but Gemini-tied.
- **Crush** + **Cline** + **Continue** are viable multi-provider options but with partial feature parity — each would require more custom CMUX glue because hooks, sub-agents, or plan mode surfaces are narrower.

## Sources

- [Config | OpenCode](https://opencode.ai/docs/config/)
- [Agents | OpenCode](https://opencode.ai/docs/agents/)
- [Agent Skills | OpenCode](https://opencode.ai/docs/skills/)
- [Plugins | OpenCode](https://opencode.ai/docs/plugins/)
- [MCP servers | OpenCode](https://opencode.ai/docs/mcp-servers/)
- [Modes | OpenCode](https://opencode.ai/docs/modes/)
- [Providers | OpenCode](https://opencode.ai/docs/providers/)
- [OpenCode Plugin Development: Custom Tools & Event Hooks Guide | Lushbinary](https://lushbinary.com/blog/opencode-plugin-development-custom-tools-hooks-guide/)
- [awesome-opencode](https://github.com/awesome-opencode/awesome-opencode)
- [OpenCode: Open Source AI Coding Agent with 146k+ Stars](https://www.decisioncrafters.com/opencode-the-open-source-ai-coding-agent-transforming-terminal-development-with-146k-github-stars/)
- [OpenCode's January surge — 18,000 new GitHub stars](https://medium.com/@milesk_33/opencodes-january-surge-what-sparked-18-000-new-github-stars-in-two-weeks-7d904cd26844)
- [Features – Codex CLI | OpenAI Developers](https://developers.openai.com/codex/cli/features)
- [Slash commands in Codex CLI | OpenAI Developers](https://developers.openai.com/codex/cli/slash-commands)
- [Custom Prompts – Codex | OpenAI Developers](https://developers.openai.com/codex/custom-prompts)
- [Custom instructions with AGENTS.md – Codex | OpenAI Developers](https://developers.openai.com/codex/guides/agents-md)
- [Model Context Protocol – Codex | OpenAI Developers](https://developers.openai.com/codex/mcp)
- [Hooks – Codex | OpenAI Developers](https://developers.openai.com/codex/hooks)
- [Changelog – Codex | OpenAI Developers](https://developers.openai.com/codex/changelog)
- [Codex 0.114 — Operations Release (Code Mode, Hooks, Skill Governance)](https://codex.infinitegateways.com/2026/03/codex-0-114-operations-release-march-2026/)
- [Crush — charmbracelet/crush](https://github.com/charmbracelet/crush)
- [Crush + Docker MCP — Charm](https://charm.land/blog/crush-and-docker-mcp/)
- [Crush Review 2026 — VibeCoding Hub](https://vibecodinghub.org/tools/crush)
- [Plugins — OpenHands Docs](https://docs.openhands.dev/sdk/guides/plugins)
- [OpenHands SDK — GitHub](https://github.com/OpenHands/software-agent-sdk)
- [OpenHands v1.12+ releases](https://github.com/OpenHands/software-agent-sdk/releases)
- [Aider Documentation](https://aider.chat/docs/)
- [mcpm-aider — GitHub](https://github.com/lutzleonhardt/mcpm-aider)
- [Cline MCP Marketplace](https://cline.bot/mcp-marketplace)
- [Cline releases](https://github.com/cline/cline/releases)
- [Continue — Slash commands](https://docs.continue.dev/customize/slash-commands)
- [Continue CLI Quick Start](https://docs.continue.dev/cli/quick-start)
- [Continue — How to Set Up MCP](https://docs.continue.dev/customize/deep-dives/mcp)
- [Gemini CLI — Extensions](https://geminicli.com/docs/extensions/)
- [Gemini CLI — Extension Reference](https://geminicli.com/docs/extensions/reference/)
- [Gemini CLI — MCP Servers](https://geminicli.com/docs/tools/mcp-server/)
- [Gemini CLI Extensions Gallery](https://geminicli.com/extensions/)
- [Cursor Subagents](https://cursor.com/docs/subagents)
- [Cursor Changelog 2.4 — Subagents, Skills, Image Generation](https://cursor.com/changelog/2-4)
- [Cursor Changelog 2.5 — Plugins, Sandbox Access, Async Subagents](https://cursor.com/changelog/2-5)
- [Using Agent in CLI — Cursor Docs](https://cursor.com/docs/cli/using)
- [Amp Owner's Manual — ampcode.com](https://ampcode.com/manual)
- [Amp — Sourcegraph](https://sourcegraph.com/amp)
- [Amp Code AI Review 2026](https://www.secondtalent.com/resources/amp-ai-review/)
- [Teaching AI to Navigate Your Codebase: Agent Skills + Sourcegraph MCP](https://medium.com/@ajaynz/teaching-ai-to-navigate-your-codebase-agent-skills-sourcegraph-mcp-710b75ab2943)
- [The 2026 Guide to Coding CLI Tools — Tembo](https://www.tembo.io/blog/coding-cli-tools-comparison)
- [Claude Code Extensions: MCP, Skills, Agents & Hooks Guide 2026 — Morph](https://www.morphllm.com/claude-code-extensions)
