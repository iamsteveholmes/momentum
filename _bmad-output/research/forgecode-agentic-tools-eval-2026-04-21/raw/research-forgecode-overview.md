---
content_origin: claude-code-subagent
date: 2026-04-21
sub_question: "What is ForgeCode (forgecode.dev) — its architecture, core capabilities, model support, CLI/IDE integration surface, pricing model, target use cases — and where does it sit relative to Claude Code?"
topic: "ForgeCode and agentic tooling evaluation for Momentum"
---

## TL;DR

ForgeCode (also branded "Forge Code") is an open-source (Apache-2.0), Rust-implemented, terminal-first agentic coding harness developed primarily by the antinomyhq organization (repo: `antinomyhq/forge`, formerly under `tailcallhq/forgecode`). It runs as a native CLI with a ZSH shell plugin and a strong multi-provider model story (Anthropic, OpenAI, Google, Groq, Bedrock, OpenRouter, and "300+ models" via OpenAI-compatible providers), built around three built-in specialized agents (`forge` for execution, `sage` for research, `muse` for planning) plus user-authored custom agents, skills, and MCP servers. It self-promotes as "#1 on TermBench 2.0" and occupies roughly the same niche as Claude Code — a terminal-native coding agent — but trades Claude Code's richer automation layer (hooks, checkpoints, IDE extensions, auto-memory) for model-agnosticism, an Apache-2.0 license, and a lightweight Rust footprint with git-worktree sandboxing baked in ([forgecode.dev](https://forgecode.dev/) [OFFICIAL]; [antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]; [ForgeCode vs Claude Code, dev.to, 2026](https://dev.to/liran_baba/forgecode-vs-claude-code-which-ai-coding-agent-actually-wins-36c) [PRAC]).

## Product Positioning

ForgeCode markets itself as "the world's #1 coding harness" and the leader on TermBench 2.0 with 81.8% accuracy; it foregrounds terminal-native workflow ("type `:` to talk to ForgeCode right inside your terminal") and multi-agent execution with "bounded context" ([forgecode.dev homepage](https://forgecode.dev/) [OFFICIAL]). The project's GitHub description is: *"AI enabled pair programmer for Claude, GPT, O Series, Grok, Deepseek, Gemini and 300+ models"* ([antinomyhq/forgecode GitHub search result](https://github.com/antinomyhq/forgecode) [OFFICIAL]). The active canonical repo today is `antinomyhq/forge` (the older `tailcallhq/forgecode` name and its mirrors still surface in search results and the npm package `@antinomyhq/forge` still publishes releases) ([@antinomyhq/forge on npm](https://www.npmjs.com/package/@antinomyhq/forge) [OFFICIAL]).

Homepage metrics (developer-marketing figures, treat with appropriate skepticism): 38.1B+ tokens processed daily, 24.4M+ lines of code generated daily, 6.8k GitHub stars, 1.4k forks, 2,571 commits, 336 total releases — latest `v2.12.0` on April 21, 2026, matching the research-date cutoff ([antinomyhq/forge GitHub](https://github.com/antinomyhq/forge) [OFFICIAL]; [forgecode.dev](https://forgecode.dev/) [OFFICIAL]).

## Architecture

ForgeCode is a **standalone Rust binary**, distributed primarily via the install script `curl -fsSL https://forgecode.dev/cli | sh`, with alternate distributions via `nix run github:tailcallhq/forgecode` and the npm shim `@antinomyhq/forge` ([antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]). Language breakdown of the repo: Rust 93.6%, Shell 4.0%, HTML 1.1%, TypeScript 0.8%, JS/CSS/Nix trailing ([antinomyhq/forge GitHub](https://github.com/antinomyhq/forge) [OFFICIAL]). Internally the repo is a **Cargo workspace** (`crates/` with multiple crates, plus `commands/`, `templates/`, `shell-plugin/`, `docs/`).

The runtime has **three interaction modes**:

1. **Interactive TUI** — `forge` with no arguments drops into a persistent conversational session.
2. **One-shot CLI** — `forge -p "prompt"` runs a single task and returns to the shell; pipeable.
3. **ZSH shell plugin** — after `forge setup`, the `:` prefix invokes ForgeCode inline at your shell prompt (e.g., `: refactor the auth module`) so you do not leave the shell ([antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]).

The design talking point is a **multi-agent architecture with bounded context**: specialized sub-agents each operate on a minimal, relevant context window rather than dumping the full codebase into one monolithic prompt ([forgecode.dev](https://forgecode.dev/) [OFFICIAL]). Workspace indexing (see below) sends content to `https://api.forgecode.dev` by default, configurable via `FORGE_WORKSPACE_SERVER_URL`, so there is a **hosted component** even though the binary runs locally — this contradicts some third-party claims of "fully local" operation (see [dev.to "Why I Chose ForgeCode"](https://dev.to/forgecode/why-i-chose-forgecode-as-1-ai-coding-assistant-in-2025-325l) [PRAC], which claims local-first; the README's `FORGE_WORKSPACE_SERVER_URL` default makes the picture more nuanced).

## Core Capabilities

### Built-in Agents

Three agents ship in-box ([antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]):

- **`forge`** — default execution agent; writes code, edits files, runs tests.
- **`sage`** (alias `:ask`) — read-only research agent; maps architecture, traces data flow, no file modifications.
- **`muse`** (alias `:plan`) — planning agent; analyzes project structure and writes plan files into a `plans/` directory.

Custom agents are user-authored Markdown files with YAML front-matter placed in `.forge/agents/` (project-local) or `~/forge/agents/` (global). Project-local agents override global ones. Each agent definition carries `id`, `title`, `description`, `system_prompt`, `user_prompt`, and optional `templates` (Handlebars-rendered partials like `repomix-output.xml`) ([antinomyhq/awesome-forge-agents](https://github.com/antinomyhq/awesome-forge-agents) [OFFICIAL]).

### Skills

Skills are reusable workflows invokable as tools. Three built-in skills ship with Forge:

- **`create-skill`** — scaffolds new custom skill templates.
- **`execute-plan`** — executes plan files from the `plans/` directory (links Muse's output to Forge's execution).
- **`github-pr-description`** — generates PR descriptions from diffs.

Custom skills live in `.forge/skills/<name>/SKILL.md` (project) or `~/forge/skills/<name>/SKILL.md` (global); precedence: project > global > built-in ([antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]). The "SKILL.md with YAML front-matter" convention is essentially the same shape Momentum uses today, and is convergent with Claude Code's Agent Skills format.

### MCP Support

ForgeCode implements the Model Context Protocol. MCP servers are declared in `.mcp.json` (project) or `~/forge/.mcp.json` (global) with the standard `mcpServers` shape (`command`, `args`, `env`). Management commands: `forge mcp list | import | show | remove | reload`. Project-local config overrides global ([antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]).

### Git Worktree Sandboxing

`forge --sandbox <name>` creates an isolated git worktree with its own branch, starts an interactive session in it, and keeps the main tree untouched; merge back only what works ([antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]; [ForgeCode vs Claude Code dev.to, 2026](https://dev.to/liran_baba/forgecode-vs-claude-code-which-ai-coding-agent-actually-wins-36c) [PRAC]). This is a first-class built-in, unlike Claude Code where worktree isolation is a community skill pattern rather than a CLI flag ([Worktree Isolation Claude Code Skill](https://mcpmarket.com/tools/skills/worktree-isolation) [PRAC]).

### Semantic Codebase Indexing

`:sync` (alias `:workspace-sync`) indexes the repository for meaning-based search. Additional workspace commands: `:workspace-init`, `:workspace-status`, `:workspace-info`. Indexing ships file content to the workspace server at `https://api.forgecode.dev` by default (overridable). Search tuning via `FORGE_SEM_SEARCH_LIMIT` (default 200) and `FORGE_SEM_SEARCH_TOP_K` (default 20) ([antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]).

### Custom Commands & Config

- `forge.yaml` controls `model`, `temperature`, `max_walker_depth`, `max_tool_failure_per_turn`, `max_requests_per_turn`, `custom_rules`, and `commands`.
- `AGENTS.md` (project root or `~/forge/AGENTS.md`) is the Forge equivalent of `CLAUDE.md` — persistent project-wide agent instructions and coding conventions.
- Custom commands: YAML files in `.forge/commands/` or `~/forge/commands/` expose `:commandname` shortcuts.
- Conversation management: `forge conversation {resume|list|new|dump|compact|retry|clone|rename|delete}`, plus `:new`, `:conversation`, `:clone`, `:rename` in the shell plugin ([antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]).

### Developer UX Commands

From the ZSH plugin reference ([antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]):

- `:agent <name>` (switch agent) — `:model <id>` (one-shot model swap) — `:config-model` (persistent)
- `:reasoning-effort <none|minimal|low|medium|high|xhigh|max>` and `:config-reasoning-effort`
- `:commit` / `:commit-preview` for AI commit messages
- `:suggest <description>` turns natural language into a shell command
- `:edit` opens `$EDITOR` for composing multi-line prompts
- `:copy`, `:dump`, `:info`, `:tools`, `:skill`
- `@filename` + Tab for fzf file attachment in prompts

### Plan Mode and Restricted Shell

ForgeCode supports a plan-first workflow via the `muse` agent that writes into `plans/`, and `:execute-plan` drives Forge to implement the plan. Search results also describe a "restricted shell mode" that limits filesystem access and prevents unintended changes ([antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]).

### Hooks

**Hooks are the most important explicit gap.** A detailed 2026 comparison confirms: *"Claude Code has hooks that fire on file changes… none of that exists in ForgeCode yet"* ([ForgeCode vs Claude Code dev.to, 2026](https://dev.to/liran_baba/forgecode-vs-claude-code-which-ai-coding-agent-actually-wins-36c) [PRAC]). Note that a separate, unaffiliated project at `Forge-NC/Forge` advertises 18 plugin hooks; this is a different tool and should not be confused with antinomyhq's ForgeCode ([Forge-NC/Forge GitHub](https://github.com/Forge-NC/Forge) [PRAC]).

## Model Support

ForgeCode is deliberately **model-agnostic**. Providers named in the README and community coverage:

- **Anthropic** — Claude Sonnet/Opus families (e.g., `claude-sonnet-4@20250514`, `claude-3.7-sonnet`; 2026 coverage references Claude 4 and Opus 4.6)
- **OpenAI** — O-series and GPT (`o3-mini-high`, GPT-5.x referenced in 2026 benchmark tables)
- **Google** — Gemini via Vertex AI (`gemini-2.5-pro`, `gemini-2.0-flash`)
- **Groq** — `deepseek-r1-distill-llama-70b`
- **Amazon Bedrock** — via Bedrock Access Gateway
- **xAI Grok, DeepSeek, z.ai, Cerebras, IO Intelligence, Requesty**
- **OpenRouter** — the primary catch-all for the "300+ models" claim
- **Any OpenAI-compatible API** — generic bring-your-own-endpoint provider ([antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]; [forgecode.dev](https://forgecode.dev/) [OFFICIAL])

Provider credentials are now managed via `forge provider login` (file-based credential store); the legacy `.env` approach is deprecated. Model selection supports mid-session switching — thinking models for planning, fast models for coding, large-context models for file-heavy tasks — and persistent defaults via `:config-model` and `:config-provider` stored in `~/forge/.forge.toml` ([antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]).

Local models are indirectly supported through OpenAI-compatible endpoints (LM Studio, Ollama with OpenAI compat, llama.cpp server, etc.), though no first-class local-model integration is advertised.

## CLI/IDE Integration Surface

- **Terminal (primary)** — Rust binary with interactive TUI, one-shot CLI, and ZSH shell plugin.
- **Platforms** — Linux, macOS, Windows (README references both `SHELL=/bin/zsh` and `COMSPEC=cmd.exe`).
- **IDE plugins** — **None.** No VS Code extension, no JetBrains plugin. The positioning is explicitly: "use VS Code, Vim, IntelliJ or any IDE, and ForgeCode will still listen to your commands" — i.e., ForgeCode stays in the terminal and lets your IDE be your IDE ([dev.to "Why I Chose ForgeCode"](https://dev.to/forgecode/why-i-chose-forgecode-as-1-ai-coding-assistant-in-2025-325l) [PRAC]; [antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]).
- **Web UI** — None published.
- **Shell fit** — ZSH is first-class; the `:` prefix is a ZSH widget. Bash parity is not advertised.

## Pricing Model

ForgeCode left its unlimited free-tier early-access period on **July 27, 2025** and moved to a tiered plan ([ForgeCode blog — Graduating from Early Access](https://forgecode.dev/blog/graduating-from-early-access-new-pricing-tiers-available/) [OFFICIAL]):

| Tier | Price | Quota |
|---|---|---|
| Free | $0/mo | Dynamic daily request limit based on server load, typically **10–50 requests/day**; permanent, not a trial |
| Pro | **$20/mo** | Up to **1,000 AI requests/day** |
| Max | **$100/mo** | Up to **5,000 AI requests/day** |

The ForgeCode subscription is for access to *their* inference gateway / workspace server. Because ForgeCode accepts per-provider API keys (Anthropic, OpenAI, OpenRouter, etc.), **BYOK is effectively supported** for inference cost, though the free-tier/paid-plan caps described above still apply to ForgeCode's hosted semantic workspace and routing layer. Enterprise terms are not published as of the research date.

The **code itself is Apache-2.0**, so self-hosting and forking the binary is permitted; however, disabling telemetry requires `FORGE_TRACKER=false` and the semantic-search workspace pointing at `api.forgecode.dev` is a hosted dependency unless redirected via `FORGE_WORKSPACE_SERVER_URL` ([antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]; [ForgeCode vs Claude Code dev.to](https://dev.to/liran_baba/forgecode-vs-claude-code-which-ai-coding-agent-actually-wins-36c) [PRAC]).

## Target Use Cases

- **Solo developers** who want a terminal-native agent but refuse vendor lock-in on one model family.
- **Teams with mixed LLM budgets** — cost-sensitive tasks on Groq/DeepSeek, hard tasks on Claude Opus/GPT-5.
- **Privacy-leaning shops** — Apache-2.0 license means code inspectability; however, the workspace indexer uploads file content to a hosted server by default and must be self-hosted for true air-gapping.
- **Polyglot codebases** — model-per-task routing and semantic indexing favor big, mixed-language repos.
- **Experimentation-heavy workflows** — `--sandbox` worktree isolation is a primary pitch.

The product is clearly optimized for **CLI-oriented solo/small-team developers**. The absence of hooks, scheduled tasks, auto-memory, and IDE extensions signals weak fit for larger-team governance and "practice layer" needs that Claude Code is explicitly building toward.

## Comparison to Claude Code

A side-by-side synthesis of the dev.to April 2026 comparison ([ForgeCode vs Claude Code](https://dev.to/liran_baba/forgecode-vs-claude-code-which-ai-coding-agent-actually-wins-36c) [PRAC]) with the official READMEs:

| Dimension | ForgeCode | Claude Code |
|---|---|---|
| License | Apache-2.0 open source | Proprietary (Anthropic) |
| Implementation language | Rust | TypeScript |
| Model support | 300+ via multi-provider + OpenRouter | Claude family only (at time of writing) |
| Project config | `AGENTS.md` + `forge.yaml` | `CLAUDE.md` (hierarchical) + settings.json |
| MCP | Yes (`.mcp.json`, import/show/remove/reload) | Yes (extensive, primary extension surface) |
| Hooks | **No** | **Yes** (PreToolUse, PostToolUse, UserPromptSubmit, Stop, etc.) |
| Scheduled tasks | No | Yes (cloud + local) |
| Sub-agents | `forge` / `sage` / `muse` + custom agents | Parallel subagent spawns + Agent Skills |
| Plan mode | Yes (muse agent writes plans; `:execute-plan` skill) | Yes (Shift+Tab plan mode, plan-audit integrations) |
| VS Code extension | No | Yes |
| JetBrains plugin | No | Yes |
| Auto-memory | No | Yes (project memory, session memory) |
| Checkpoints / `/rewind` | No | Yes |
| Git worktree sandbox | **Yes** (`--sandbox` flag, first-class) | Community skill pattern only |
| Terminal integration | ZSH `:` prefix, native TUI | TUI, slash commands |
| Semantic code search | Built-in `:sync` against hosted workspace | None built-in (user-arranged via MCP) |
| Pricing model | $0 / $20 / $100 tiers + BYOK | Anthropic subscription (Pro/Team/Enterprise) + API |

**Where ForgeCode is arguably ahead of Claude Code:**
- Multi-model mid-session switching; no vendor lock.
- Apache-2.0 license — inspectable, forkable, self-hostable.
- Rust implementation — smaller footprint, faster startup (reviewers cite ~30s vs ~90s on comparable Opus 4.6 tasks — a small-sample observation, not a benchmark).
- `--sandbox` worktree isolation as a single CLI flag.
- Native `:commit`, `:suggest`, `:edit`, `@file` ergonomics glued into ZSH.

**Where Claude Code is ahead:**
- **Hooks ecosystem** — the single biggest gap for any tool functioning as a *practice layer*. Claude Code's hooks enable deterministic pre/post-tool enforcement that ForgeCode cannot reproduce without external shell wrappers.
- **IDE extensions** — VS Code and JetBrains surfaces.
- **Auto-memory** — session-to-session persistence without manual file authoring.
- **Checkpoints / `/rewind`** — native rollback semantics.
- **Scheduled agents / cloud execution** — remote trigger surface.
- **Anthropic model-family tuning** — Claude Code is hand-optimized for Claude thinking + caching and arguably pushes the frontier models harder on code tasks than a generic harness does.

**Where they overlap closely:**
- Both are terminal-native, TUI-centric agentic loops.
- Both support MCP as the primary extension surface.
- Both have a Skills/Agents split; Forge's `SKILL.md` layout is conceptually aligned with Claude Code's Agent Skills.
- Both support plan mode as a first-class workflow.

## Benchmarks — With Appropriate Skepticism

- **TermBench 2.0 (ForgeCode's own benchmark):** ForgeCode + GPT-5.4 = 81.8%, ForgeCode + Opus 4.6 = 81.8%, Claude Code + Opus 4.6 = 58.0% ([ForgeCode vs Claude Code dev.to](https://dev.to/liran_baba/forgecode-vs-claude-code-which-ai-coding-agent-actually-wins-36c) [PRAC]). Self-run benchmarks on your own harness should be discounted heavily.
- **SWE-bench Verified (Princeton/UChicago, independent):** ForgeCode + Claude 4 = 72.7%; Claude 3.7 Sonnet = 70.3%; Claude 4.5 Opus = 76.8% ([same source](https://dev.to/liran_baba/forgecode-vs-claude-code-which-ai-coding-agent-actually-wins-36c) [PRAC]). The independent gap between the two tools is materially smaller than ForgeCode's marketing suggests — on the order of single digits.

## Positioning Relative to Momentum

ForgeCode is in the **same product category** as Claude Code — a terminal-native coding agent harness — and offers a set of overlapping primitives (agents, skills, MCP, plan mode, `AGENTS.md`). The conceptual fit with Momentum's "file-authoritative rules, skills/agents as first-class, deterministic workflows" is real:

- Skills: `.forge/skills/<name>/SKILL.md` is almost directly comparable to Momentum's `module/skills/**/SKILL.md`.
- Agents: `.forge/agents/*.md` with YAML front-matter mirrors Momentum's agent artifacts.
- Rules: `AGENTS.md` + `custom_rules:` in `forge.yaml` plays the role of `.claude/rules/**/*.md`.

**But** the load-bearing Momentum primitive — **hooks** — is absent from ForgeCode today. Momentum's architecture assumes deterministic pre/post-tool enforcement (checkpoint commits, plan-audit gates, permission guards) executed by the harness outside the model's loop. Without hooks, ForgeCode can host the skills and rules but cannot enforce the workflow discipline that Momentum's practice layer depends on. Deterministic workflow fidelity, in Momentum's model, is not something you can graft on after the fact via shell wrappers.

Practical positioning options for Momentum (to be evaluated in other sub-questions of this research project):

1. **Parallel track** — support ForgeCode as a secondary harness for model-agnostic work (e.g., DeepSeek/Groq on cost-sensitive tasks) while Claude Code remains the primary practice-layer host.
2. **Partial replacement** — impractical today given the hooks gap; worth revisiting if ForgeCode lands a hooks subsystem.
3. **Integration point** — use ForgeCode's `--sandbox` worktree pattern and semantic-search workspace as a reference model for Momentum's own worktree/AVFL flows.

## Sources

- [forgecode.dev homepage](https://forgecode.dev/) [OFFICIAL]
- [antinomyhq/forge GitHub](https://github.com/antinomyhq/forge) [OFFICIAL]
- [antinomyhq/forge README](https://github.com/antinomyhq/forge/blob/main/README.md) [OFFICIAL]
- [antinomyhq/awesome-forge-agents](https://github.com/antinomyhq/awesome-forge-agents) [OFFICIAL]
- [@antinomyhq/forge on npm](https://www.npmjs.com/package/@antinomyhq/forge) [OFFICIAL]
- [ForgeCode blog — Graduating from Early Access: New Pricing Tiers Now Available](https://forgecode.dev/blog/graduating-from-early-access-new-pricing-tiers-available/) [OFFICIAL]
- [ForgeCode vs Claude Code: which AI coding agent actually wins? (dev.to, Liran Baba, 2026)](https://dev.to/liran_baba/forgecode-vs-claude-code-which-ai-coding-agent-actually-wins-36c) [PRAC]
- [Why I Chose 'ForgeCode' as #1 AI Coding Assistant in 2025 (dev.to)](https://dev.to/forgecode/why-i-chose-forgecode-as-1-ai-coding-assistant-in-2025-325l) [PRAC]
- [I Tested 5 CLI Coding Agents & Here's What Surprised Me (dev.to)](https://dev.to/forgecode/i-tested-5-cli-coding-agents-heres-what-surprised-me-28i) [PRAC]
- [ForgeCode: The Multi-Agent Coding Harness Dominating Terminal-Bench 2.0 (Medium, Rick Hightower, April 2026)](https://medium.com/@richardhightower/forgecode-dominating-terminal-bench-2-0-harness-engineering-beat-claude-code-codex-gemini-etc-eb5df74a3fa4) [PRAC]
- [Benchmarks & Evaluation Framework — antinomyhq/forgecode DeepWiki](https://deepwiki.com/antinomyhq/forgecode/10-benchmarks-and-evaluation-framework) [PRAC]
- [Worktree Isolation Claude Code Skill (mcpmarket)](https://mcpmarket.com/tools/skills/worktree-isolation) [PRAC] — contrastive reference for Claude Code side
- [Forge-NC/Forge GitHub](https://github.com/Forge-NC/Forge) [PRAC] — unaffiliated project; referenced only to disambiguate from antinomyhq's ForgeCode
