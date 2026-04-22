---
content_origin: claude-code-subagent
date: 2026-04-22
sub_question: "Beyond opencode, pi, Goose, and ForgeCode, what other CLI coding agents exist and how deeply do they integrate with CMUX?"
topic: "CMUX-integrated coding agents with LLM marketplace support as Claude Code replacements"
---

# CLI Coding Agent Candidate Enumeration — CMUX Integration Depth

## Context and Framing

This document enumerates viable CLI coding agents that could replace Claude Code as of 2026-04-22, with a focus on CMUX integration depth. "First-class CMUX integration" specifically means the agent can programmatically invoke cmux CLI commands (`cmux new-split`, `cmux send`, `cmux capture-pane`, `cmux browser open`, etc.) to orchestrate panes, browser surfaces, and markdown viewers — not merely running inside a cmux pane.

### A Preliminary Finding About CMUX

Per the cmux project page and comparison guides, **cmux is explicitly agent-agnostic**: "cmux works with any agent that runs in a terminal, including Claude Code, Codex, OpenCode, Gemini CLI, Kiro, Aider, Goose, Amp, Cline, Cursor Agent, and anything else you can launch from the command line" ([cmux — terminal built for multitasking](https://cmux.com/)) [OFFICIAL]. As a consequence, **no CLI coding agent in this enumeration ships with native cmux-CLI orchestration baked in.** CMUX integration depth for every candidate reduces to: (a) does the agent have a bash/shell tool reliable enough to invoke `cmux` commands, and (b) does the agent expose hooks, custom tools, skills, or subagents such that cmux orchestration can be cleanly wired in?

Using that framing, the real differentiators are extensibility primitives: **hooks, custom tools, skills, subagents, plan mode, and MCP**. Agents with richer extensibility are easier to wire up as cmux orchestrators; agents with only a raw bash tool can still drive cmux but with less reusability.

---

## Tier 1 — Strong Candidates (Extensibility + Shell + Marketplace LLM Access)

### opencode (SST)

- **What**: Open-source (MIT) AI coding agent, Go + TUI, by SST and the terminal.shop creators. Primary URL: <https://opencode.ai>, repo: <https://github.com/sst/opencode>.
- **Maturity**: Very active — April 2026 releases added NVIDIA as a built-in provider, an "LLM Gateway" provider, and concurrent-edit safety. Supports 75+ LLMs including Anthropic, OpenAI, Google, OpenRouter, Ollama, and now LLM Gateway ([OpenCode docs](https://opencode.ai/docs/)) [OFFICIAL]. GitHub officially partnered with opencode in January 2026 ([Every AI Coding CLI in 2026 — DEV](https://dev.to/soulentheo/every-ai-coding-cli-in-2026-the-complete-map-30-tools-compared-4gob)) [PRAC].
- **CMUX integration depth**:
  - (a) Programmatic pane control: **No native cmux integration** [UNVERIFIED for any claim otherwise].
  - (b) Shell-wiring sufficiency: **Very high.** opencode has a `bash` tool, **plugin system with 25+ lifecycle hooks**, **custom tools defined in config**, **subagents invokable via `@mention` and manually**, **task tool for multi-step tracking**, and **MCP support** ([OpenCode Plugin Development — Lushbinary](https://lushbinary.com/blog/opencode-plugin-development-custom-tools-hooks-guide/), [opencode docs — Tools](https://opencode.ai/docs/tools), [OpenCode Agents](https://opencode.ai/docs/agents/)) [OFFICIAL]. The plugin hooks (`tool.execute.before`, `tool.execute.after`) make it straightforward to wire `cmux new-split`/`cmux send` invocations around tool use.
  - (c) Assessment: opencode is the single best candidate for cmux-integrated workflows outside Claude Code. Its plugin system maps cleanly onto Claude Code's hook + skill + subagent model. A Skills-equivalent ("Superpowers for OpenCode" community project) exists ([Superpowers for OpenCode — fsck.com blog](https://blog.fsck.com/2025/11/24/Superpowers-for-OpenCode/)) [PRAC].
- **LLM flexibility**: Full OpenRouter + 75+ providers including Anthropic, OpenAI, Google, Ollama, NVIDIA, LLM Gateway.

### OpenAI Codex CLI

- **What**: Open-source (Apache-2.0 per repo) terminal-native coding agent from OpenAI. Primary URL: <https://developers.openai.com/codex/cli>, repo: <https://github.com/openai/codex>.
- **Maturity**: Very active. Now exposes itself as an MCP server; integrates with OpenAI Agents SDK; supports subagents explicitly ([Codex Features](https://developers.openai.com/codex/cli/features), [Codex Changelog](https://developers.openai.com/codex/changelog)) [OFFICIAL].
- **CMUX integration depth**:
  - (a) Programmatic pane control: **None native.**
  - (b) Shell-wiring sufficiency: **High.** Codex CLI supports **subagents configurable via `config.toml`**, **MCP servers over stdio and streamable HTTP**, **tool discovery**, and an **AGENTS.md project-context file** ([openai/codex AGENTS.md](https://github.com/openai/codex/blob/main/AGENTS.md)) [OFFICIAL]. Shell commands are first-class. The subagent system specifically supports parallelizing larger tasks — a natural fit for "spawn each subagent in its own cmux pane" patterns.
  - (c) Assessment: Close second to opencode. Lacks the richer lifecycle-hook model but subagent + MCP gives plenty of surface area to wire cmux.
- **LLM flexibility**: OpenAI-native; limited to OpenAI models via ChatGPT subscription or API key. Not a full marketplace play.

### Charm Crush

- **What**: Open-source (FSL-1.1-MIT) Go/BubbleTea TUI agent by Charm. Repo: <https://github.com/charmbracelet/crush>.
- **Maturity**: Active; 2026 release line. The original "OpenCode AI" project pre-fork/rename; now sibling to SST's opencode ([The New Stack review of Crush ex-OpenCode AI](https://thenewstack.io/terminal-user-interfaces-review-of-crush-ex-opencode-al/)) [PRAC].
- **CMUX integration depth**:
  - (a) Programmatic pane control: **None native.**
  - (b) Shell-wiring sufficiency: **Moderate.** Crush has a bash tool with `allowed_tools` allow/deny/ask configuration, **LSP integration**, and **MCP server support (stdio, SSE, HTTP)** ([charmbracelet/crush GitHub](https://github.com/charmbracelet/crush), [DeepWiki — Crush MCP Tool Integration](https://deepwiki.com/charmbracelet/crush/6.3-mcp-tool-integration)) [OFFICIAL]. However, **custom slash commands are still an open feature request** ([Issue #2219](https://github.com/charmbracelet/crush/issues/2219)) [OFFICIAL]; no lifecycle hooks or plugin system documented.
  - (c) Assessment: Usable for ad-hoc cmux-from-shell workflows, weaker than opencode for reusable orchestration patterns until slash-commands/hooks land.
- **LLM flexibility**: Multi-provider (Anthropic, OpenAI, Gemini, Bedrock, Copilot, Hyper, MiniMax, Vercel, etc.) with mid-session model switching.

### GitHub Copilot CLI

- **What**: Proprietary terminal-native agent, GA February 2026. Primary URL: <https://github.com/features/copilot/cli/>, repo: <https://github.com/github/copilot-cli>.
- **Maturity**: GA. Multiple specialized agents (Explore, Task, Code Review, Plan), Autopilot mode, `/resume` for local-cloud handoff, cross-session memory, claudette-like `&`-prefix delegation to cloud coding agent ([GitHub Copilot CLI GA announcement](https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available/), [Visual Studio Magazine](https://visualstudiomagazine.com/articles/2026/03/02/github-copilot-cli-reaches-general-availability-bringing-agentic-coding-to-the-terminal.aspx)) [OFFICIAL/PRAC].
- **CMUX integration depth**:
  - (a) Programmatic pane control: **None native.**
  - (b) Shell-wiring sufficiency: **Unclear.** Claude Sonnet 4.5 default with `/model` switching, but documentation emphasizes GitHub-platform integration; custom tools and plugin/hook APIs are not foregrounded in public docs.
  - (c) Assessment: Functional for running inside a cmux pane; weak for orchestrating cmux programmatically without reverse-engineering.
- **LLM flexibility**: Claude Sonnet 4.5, Claude Sonnet 4, GPT-5; curated, not a full marketplace.

### Cursor Agent CLI

- **What**: Proprietary CLI from Cursor, shipped January 16, 2026. Primary URL: <https://cursor.com/blog/cli>.
- **Maturity**: Shipping. Plan/Ask modes via `/plan`, `--mode=plan`; `/debug`, `/config`, `/statusline`, `/btw`; Cloud Agent handoff. Feb 2026 v2.5 added a Plugin Marketplace and 8-parallel-subagent worktree orchestration ([CLI Agent Modes and Cloud Handoff — Cursor](https://cursor.com/changelog/cli-jan-16-2026)) [OFFICIAL].
- **CMUX integration depth**:
  - (a) Programmatic pane control: **None native.**
  - (b) Shell-wiring sufficiency: **Moderate.** Shell command execution exists; a **Plugin Marketplace** landed in Feb 2026 and is the most plausible wiring surface. Subagent worktrees hint at a model where cmux-pane-per-subagent is natural but undocumented.
  - (c) Assessment: Cursor Agent CLI is promising but heavily tied to the Cursor IDE ecosystem. Plugin Marketplace maturity determines whether cmux can be wired cleanly.
- **LLM flexibility**: Multi-model through Cursor's backend (Claude Opus 4.6, GPT-5.4, etc.). Usage tied to Cursor subscription.

### Amp (Sourcegraph)

- **What**: Proprietary agentic coding tool from Sourcegraph (formerly Cody). CLI + VS Code/JetBrains/Neovim. Primary URL: <https://ampcode.com/>.
- **Maturity**: Enterprise-focused since 2025; self-serve plans discontinued. First-class CLI with multi-model per-task routing and parallel subagents ([Amp by Sourcegraph](https://sourcegraph.com/amp), [npm @sourcegraph/amp](https://www.npmjs.com/package/@sourcegraph/amp)) [OFFICIAL].
- **CMUX integration depth**:
  - (a) Programmatic pane control: **None native.** Explicitly listed as a cmux-compatible agent ([cmux.com](https://cmux.com/)) [OFFICIAL] but only at the "runs in a pane" level.
  - (b) Shell-wiring sufficiency: **Unclear.** Bash tool likely exists; plugin/hook surface not publicly documented at the level needed to compare to opencode.
  - (c) Assessment: Strong engine, restricted access model. For solo-dev replacement of Claude Code, enterprise pricing is a blocker.
- **LLM flexibility**: Claude Opus 4.6, GPT-5.4, internal fast models — routed automatically per task.

### Gemini CLI (Google)

- **What**: Open-source (Apache-2.0) terminal-native agent. Primary URL: <https://github.com/google-gemini/gemini-cli>.
- **Maturity**: Very active. 1,000 free requests/day with Gemini 2.5 Pro and 1M context. Custom slash commands (TOML + MCP prompts), subagents (local execution + tool isolation), remote subagents, MCP integration ([Gemini CLI — Google Cloud Blog](https://cloud.google.com/blog/topics/developers-practitioners/gemini-cli-custom-slash-commands), [MCP servers with Gemini CLI](https://geminicli.com/docs/tools/mcp-server/)) [OFFICIAL].
- **CMUX integration depth**:
  - (a) Programmatic pane control: **None native.**
  - (b) Shell-wiring sufficiency: **High.** Custom slash commands in `~/.gemini/commands/*.toml` plus MCP subagents and remote subagents give three separate extensibility points to wire cmux. Shell tool is first-class.
  - (c) Assessment: Second only to opencode for extensibility. Biggest constraint is LLM lock-in — works best with Gemini models.
- **LLM flexibility**: Google-first. Extensible but not a marketplace play.

---

## Tier 2 — Viable But Weaker Fits

### Cline (with CLI Mode)

- **What**: Open-source (Apache-2.0) VS Code extension that shipped a CLI in 2026. Primary URL: <https://docs.cline.bot/cline-cli/getting-started>.
- **Maturity**: Mature VS Code extension (100k+ stars category, formerly Claude Dev); CLI supports macOS/Linux/Windows with both interactive TTY and automated modes ([Cline Docs — CLI Getting Started](https://docs.cline.bot/cline-cli/getting-started)) [OFFICIAL].
- **CMUX integration depth**:
  - (a) Programmatic pane control: **None native.**
  - (b) Shell-wiring sufficiency: **Moderate.** Shell access is central to Cline's design. MCP + OpenRouter + custom model support. Plugin/hook primitives are less mature than opencode's.
  - (c) Assessment: Feasible but less ergonomic than opencode for cmux orchestration.
- **LLM flexibility**: Very broad — same providers as VS Code extension (OpenRouter, Anthropic, OpenAI, Bedrock, Ollama, LM Studio, etc.).

### Roo Code

- **What**: Cline fork, open-source, VS Code extension — CLI mode exists but is secondary. Custom modes, Roo Cloud, SOC-2 compliance. Primary URL (marketplace): <https://marketplace.visualstudio.com/items?itemName=RooVeterinaryInc.roo-cline>.
- **Maturity**: Active 2026 development as a Cline fork ([Roo Code vs Cline — Qodo blog](https://www.qodo.ai/blog/roo-code-vs-cline/)) [PRAC].
- **CMUX integration depth**: Similar to Cline. Custom modes are the most compelling wiring surface (define a "cmux-orchestrator" mode).
- **LLM flexibility**: Same broad provider list as Cline.

### Kiro / Kiro CLI (AWS)

- **What**: AWS agentic IDE + CLI. Primary URL: <https://kiro.dev/cli/>, repo: <https://github.com/kirodotdev/Kiro>.
- **Maturity**: Active. 2026 added Code Intelligence (LSP), multi-session support, MCP registry for governance, **subagents with live progress tracking**, enterprise auth ([Kiro CLI Changelog](https://kiro.dev/changelog/cli/), [Kiro CLI MCP docs](https://kiro.dev/docs/cli/mcp/)) [OFFICIAL].
- **CMUX integration depth**:
  - (a) Programmatic pane control: **None native.** Listed as a cmux-compatible agent ([cmux.com](https://cmux.com/)) [OFFICIAL].
  - (b) Shell-wiring sufficiency: **High.** Subagents + MCP registry + LSP + enterprise auth — good extensibility surface. ACP-compatible.
  - (c) Assessment: Strong open-weight model support (DeepSeek, MiniMax, Qwen added as built-in options) [OFFICIAL via Kiro changelog]. Viable cmux host.
- **LLM flexibility**: Strong — Bedrock, multiple open-weight models, OpenRouter-adjacent ecosystem.

### Kilo Code

- **What**: Open-source VS Code extension (Cline lineage) that expanded to JetBrains, CLI, Slack. Primary URL: <https://kilo.ai>.
- **Maturity**: Early 2026 Kilo CLI 1.0. Supports 500+ models across 60+ providers. Orchestrator mode coordinates multiple tasks; Memory Bank stores architectural decisions ([Kilo Code vs Cline — Morph](https://www.morphllm.com/comparisons/kilo-code-vs-cline)) [PRAC].
- **CMUX integration depth**: Shell-wiring viable; Orchestrator mode is the closest analog to cmux-pane-per-task patterns but doesn't invoke cmux natively.
- **LLM flexibility**: Best-in-class — 500+ models, 60+ providers, free access to GLM-4.7 and MiniMax M2.1 ([Kilo open-source models](https://kilo.ai/open-source-models)) [OFFICIAL].

### Aider

- **What**: Open-source (Apache-2.0) pioneering pair-programmer CLI. Primary URL: <https://aider.chat/>, repo: <https://github.com/Aider-AI/aider>.
- **Maturity**: Mature (multi-year). 100+ languages, automatic git commits, connects to almost any LLM. Claude 3.7 Sonnet, DeepSeek R1/V3, OpenAI o1/o3-mini/GPT-4o, local models ([Aider Docs](https://aider.chat/docs/)) [OFFICIAL].
- **CMUX integration depth**:
  - (a) None native. Listed as cmux-compatible agent.
  - (b) Shell-wiring sufficiency: **Low to moderate.** Aider's model is focused on file-editing loops, not general agentic orchestration. No skills/subagents/hooks primitives comparable to Claude Code.
  - (c) Assessment: Excellent at what it does; a weak fit for a cmux-driving orchestrator.
- **LLM flexibility**: Very broad — any OpenAI-compatible API + direct Anthropic.

### Continue CLI (`cn`)

- **What**: Open-source (Apache-2.0). Primary URL: <https://docs.continue.dev/cli/overview>, repo: <https://github.com/continuedev/continue>.
- **Maturity**: Active; 2026 pivot toward "source-controlled AI checks enforceable in CI". Both TUI interactive mode and headless mode; async-first architecture; tool permission system at `~/.continue/permissions.yaml` ([Continue CLI Overview](https://docs.continue.dev/cli/overview), [Building Cloud Agents with Continue CLI](https://blog.continue.dev/building-async-agents-with-continue-cli)) [OFFICIAL].
- **CMUX integration depth**: Shell tool exists; agent mode autonomous. Plugin/hook surface exists via Continue's extension model. Moderate fit for cmux orchestration — stronger for CI/automation than interactive cmux-driven workflows.
- **LLM flexibility**: Broad — any provider, local models via Ollama/LM Studio.

### pi / pi-coding-agent (Mario Zechner)

- **What**: Deliberately minimal terminal coding harness by Mario Zechner. Primary URL: <https://github.com/badlogic/pi-mono>, npm: `@mariozechner/pi-coding-agent`.
- **Maturity**: Very active — 0.68.1 as of April 2026, nearly daily releases. Philosophy: minimal core (read, write, edit, bash), extensibility via packages/skills. **Explicitly skips subagents and plan mode** in favor of extensions ([Pi Coding Agent — DEV](https://dev.to/theoklitosbam7/pi-coding-agent-a-self-documenting-extensible-ai-partner-dn), [Pi: The Minimal Agent — Armin Ronacher](https://lucumr.pocoo.org/2026/1/31/pi/)) [PRAC].
- **CMUX integration depth**:
  - (a) None native.
  - (b) Shell-wiring sufficiency: **High for custom extension builders**, low out-of-the-box. pi's whole pitch is "build what you need as pi packages" — a cmux-orchestration package is the canonical pi-shaped solution.
  - (c) Assessment: Best fit for a developer willing to write their own cmux-orchestrator as a pi extension. Worse than opencode if the goal is to adopt existing extensions.
- **LLM flexibility**: Multi-provider (subscription or API key).

### `oh-my-pi`

- **What**: A more opinionated pi fork with **hash-anchored edits, LSP, Python, browser, subagents**. Repo: <https://github.com/can1357/oh-my-pi>.
- **Maturity**: Niche community fork; notable for adding subagents and browser tool that pi explicitly omits.
- **CMUX integration depth**: Same as pi — shell-wireable. Browser tool overlaps with `cmux browser` but doesn't invoke cmux.
- **LLM flexibility**: Same as pi.

---

## Tier 3 — Lower-Fit but Worth Naming

### OpenHands (ex-OpenDevin)

- **What**: Open-source (MIT), MIT-licensed core, 70k+ GitHub stars, 490+ contributors. Primary URL: <https://docs.openhands.dev/>, repo: <https://github.com/All-Hands-AI/OpenHands>.
- **Maturity**: v1.6.0 March 2026; Kubernetes support, Planning Mode beta. Docker-sandboxed full agentic loop (code, terminal, browser, GitHub PRs) ([OpenHands Review 2026 — Vibe Coding](https://vibecoding.app/blog/openhands-review), [OpenHands SDK docs](https://docs.openhands.dev/sdk)) [OFFICIAL/PRAC].
- **CMUX integration depth**:
  - (a) None native.
  - (b) Shell-wiring sufficiency: **Sandboxed.** OpenHands runs in Docker by default, which **breaks host cmux invocation** unless the container is configured to expose the host cmux socket or the agent runs outside the sandbox. Lightweight `OpenHands-CLI` binary exists but same host/container boundary issue.
  - (c) Assessment: Architecturally awkward fit for cmux. Strong OpenRouter + MCP support; if the sandbox can be punched through, extensibility surface is excellent.
- **LLM flexibility**: Broad — OpenRouter, direct API keys, local via Ollama.

### SWE-agent / mini-SWE-agent (Princeton + Stanford)

- **What**: Research tool. Primary URL: <https://swe-agent.com/>, repos: <https://github.com/SWE-agent/SWE-agent>, <https://github.com/SWE-agent/mini-swe-agent>.
- **Maturity**: NeurIPS 2024 paper; continued 2026 development. mini-swe-agent is a 100-line CLI that scores >74% on SWE-bench Verified ([SWE-agent GitHub](https://github.com/SWE-agent/SWE-agent)) [OFFICIAL].
- **CMUX integration depth**:
  - (a) None. Architecture is "bash commands only, `subprocess.run` per action, strictly linear message history" — intentionally minimal.
  - (b) Shell-wiring sufficiency: Trivially possible (the agent only emits bash) but there is no hooks/skills/subagents surface.
- **Assessment**: Research tool, not a Claude Code replacement for day-to-day work.
- **LLM flexibility**: LiteLLM-based; direct Anthropic adapter.

### Zed Agent Panel / Zed External Agents (ACP)

- **What**: Open-source editor with the **Agent Client Protocol (ACP)** — an open standard letting any editor host any ACP-speaking agent. Primary URL: <https://zed.dev/acp>.
- **Maturity**: ACP is Zed's 2025-2026 bet; hosts Claude Agent, Gemini CLI, Codex, Copilot natively ([Zed External Agents](https://zed.dev/docs/ai/external-agents), [Zed ACP](https://zed.dev/acp)) [OFFICIAL].
- **CMUX integration depth**: Zed-as-orchestrator is an *alternative* to cmux-as-orchestrator; they overlap in role. Zed can't drive cmux because it is its own surface.
- **Assessment**: Out of scope for "cmux-driven orchestrator" framing.

### Warp (Agentic Development Environment)

- **What**: Proprietary terminal replacement with embedded agents. Primary URL: <https://www.warp.dev/>.
- **Maturity**: 700K+ developers. Runs multi-step plans in-shell; natively embeds Claude Code, Codex, Gemini CLI alongside its own agent ([Warp — Universal Agent Support blog](https://www.warp.dev/blog/universal-agent-support-level-up-coding-agent-warp)) [OFFICIAL].
- **CMUX integration depth**: **Warp and cmux are direct competitors** — both replace your terminal with agent-aware multiplexers. Adopting Warp means abandoning cmux.
- **Assessment**: Not applicable.

### Augment Code / Auggie CLI

- **What**: Enterprise-focused CLI from Augment Code, emphasizing 400K+ file Context Engine. Primary URL: <https://www.augmentcode.com/>.
- **Maturity**: Claims SWE-Bench Pro #1 for the Auggie agent ([Warp vs Intent — Augment Code](https://www.augmentcode.com/tools/intent-vs-warp)) [OFFICIAL/promotional].
- **CMUX integration depth**: Shell-wireable; enterprise positioning and closed architecture make extensibility unclear.
- **LLM flexibility**: Proprietary routing.

### Qwen Code

- **What**: Open-source terminal agent optimized for Qwen models. Repo: <https://github.com/QwenLM/qwen-code>.
- **Maturity**: OAuth free tier discontinued 2026-04-15; API key or coding plan required going forward ([Qwen Code GitHub](https://github.com/QwenLM/qwen-code)) [OFFICIAL].
- **CMUX integration depth**: Shell-wireable; limited extensibility primitives documented.
- **LLM flexibility**: Qwen-first.

### DeepSeek CLI

- **What**: Community wrapper around DeepSeek Coder models. Repo: <https://github.com/holasoymalva/deepseek-cli>.
- **Maturity**: Small project.
- **CMUX integration**: Shell-wireable only.

---

## Summary Table: CMUX Integration Depth

| Agent | Native cmux? | Shell-wire fit | Extensibility primitives | Tier |
|---|---|---|---|---|
| **opencode (SST)** | No | Excellent | Plugin hooks (25+), custom tools, subagents, task tool, MCP | 1 |
| **OpenAI Codex CLI** | No | High | Subagents (config.toml), MCP server role, AGENTS.md | 1 |
| **Gemini CLI** | No | High | Custom slash commands (TOML), subagents, remote subagents, MCP | 1 |
| **Crush (Charm)** | No | Moderate | MCP, LSP, allowed_tools; no hooks/custom-commands yet | 1 |
| **Copilot CLI** | No | Unclear | Specialized agents (Explore/Task/Plan), cross-session memory | 1 |
| **Cursor Agent CLI** | No | Moderate | Plugin Marketplace (Feb 2026), subagent worktrees | 1 |
| **Amp (Sourcegraph)** | No | Unclear | Parallel subagents, multi-model routing | 1 |
| **Cline** | No | Moderate | VS Code-first; CLI exists; MCP | 2 |
| **Roo Code** | No | Moderate | Custom modes, Roo Cloud | 2 |
| **Kiro CLI (AWS)** | No | High | Subagents, MCP registry, LSP, enterprise auth | 2 |
| **Kilo Code** | No | Moderate | Orchestrator mode, Memory Bank, 500+ models | 2 |
| **Aider** | No | Low-moderate | Minimal — file-edit loop focused | 2 |
| **Continue CLI (cn)** | No | Moderate | Permission system, async, headless mode | 2 |
| **pi / oh-my-pi** | No | High (DIY) | Extensions/packages/skills; pi skips subagents | 2 |
| **OpenHands** | No | Sandbox-constrained | MCP, OAuth, tool filtering — but Docker-sandboxed | 3 |
| **SWE-agent / mini** | No | Trivial bash | Research tool; no extensibility model | 3 |
| **Zed Agent Panel** | N/A | — | ACP-based alternative orchestrator | 3 (out of scope) |
| **Warp** | N/A | — | Direct cmux competitor | 3 (out of scope) |

**Critical cross-cutting finding**: Per the cmux.com product page, cmux is **explicitly agent-agnostic by design** — "cmux works with any agent that runs in a terminal" ([cmux.com](https://cmux.com/)) [OFFICIAL]. None of the above agents ship native cmux orchestration. The differentiator for "wire cmux in easily" is therefore the richness of hooks, custom tools, skills, and subagent primitives — where **opencode, Gemini CLI, and OpenAI Codex CLI lead the open-source field**, with Copilot CLI and Cursor Agent CLI being promising proprietary options.

---

## Sources

Primary official sources:

- [opencode.ai docs](https://opencode.ai/docs/) — [OFFICIAL]
- [opencode Tools docs](https://opencode.ai/docs/tools) — [OFFICIAL]
- [opencode Agents docs](https://opencode.ai/docs/agents/) — [OFFICIAL]
- [opencode Custom Tools docs](https://opencode.ai/docs/custom-tools/) — [OFFICIAL]
- [OpenAI Codex CLI docs](https://developers.openai.com/codex/cli) — [OFFICIAL]
- [OpenAI Codex CLI Features](https://developers.openai.com/codex/cli/features) — [OFFICIAL]
- [OpenAI Codex Changelog](https://developers.openai.com/codex/changelog) — [OFFICIAL]
- [openai/codex AGENTS.md](https://github.com/openai/codex/blob/main/AGENTS.md) — [OFFICIAL]
- [charmbracelet/crush GitHub](https://github.com/charmbracelet/crush) — [OFFICIAL]
- [Crush Feature Request — Slash Commands Issue #2219](https://github.com/charmbracelet/crush/issues/2219) — [OFFICIAL]
- [GitHub Copilot CLI repo](https://github.com/github/copilot-cli) — [OFFICIAL]
- [GitHub Copilot CLI GA blog 2026-02-25](https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available/) — [OFFICIAL]
- [GitHub Copilot CLI Jan 2026 Enhancements](https://github.blog/changelog/2026-01-14-github-copilot-cli-enhanced-agents-context-management-and-new-ways-to-install/) — [OFFICIAL]
- [Cursor CLI changelog Jan 16, 2026](https://cursor.com/changelog/cli-jan-16-2026) — [OFFICIAL]
- [Cursor Agent CLI blog](https://cursor.com/blog/cli) — [OFFICIAL]
- [ampcode.com](https://ampcode.com/) — [OFFICIAL]
- [Sourcegraph Amp](https://sourcegraph.com/amp) — [OFFICIAL]
- [npm @sourcegraph/amp](https://www.npmjs.com/package/@sourcegraph/amp) — [OFFICIAL]
- [Gemini CLI repo](https://github.com/google-gemini/gemini-cli) — [OFFICIAL]
- [Gemini CLI Custom Slash Commands — Google Cloud Blog](https://cloud.google.com/blog/topics/developers-practitioners/gemini-cli-custom-slash-commands) — [OFFICIAL]
- [Gemini CLI MCP docs](https://geminicli.com/docs/tools/mcp-server/) — [OFFICIAL]
- [Cline CLI Getting Started](https://docs.cline.bot/cline-cli/getting-started) — [OFFICIAL]
- [Kiro CLI docs](https://kiro.dev/cli/) — [OFFICIAL]
- [Kiro CLI MCP docs](https://kiro.dev/docs/cli/mcp/) — [OFFICIAL]
- [Kiro CLI Changelog](https://kiro.dev/changelog/cli/) — [OFFICIAL]
- [Kiro open-source models — DeepSeek/MiniMax/Qwen](https://kiro.dev/changelog/models/deepseek-minimax-and-qwen-now-available-as-open-weight-model-options/) — [OFFICIAL]
- [Kilo Code open-source models](https://kilo.ai/open-source-models) — [OFFICIAL]
- [Aider Docs](https://aider.chat/docs/) — [OFFICIAL]
- [Aider-AI/aider GitHub](https://github.com/Aider-AI/aider) — [OFFICIAL]
- [Continue CLI Overview](https://docs.continue.dev/cli/overview) — [OFFICIAL]
- [Continue CLI How-To](https://docs.continue.dev/guides/cli) — [OFFICIAL]
- [Continue Building Cloud Agents with CLI](https://blog.continue.dev/building-async-agents-with-continue-cli) — [OFFICIAL]
- [pi-mono GitHub (badlogic)](https://github.com/badlogic/pi-mono/) — [OFFICIAL]
- [pi-coding-agent README](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/README.md) — [OFFICIAL]
- [oh-my-pi (can1357)](https://github.com/can1357/oh-my-pi) — [OFFICIAL]
- [OpenHands docs](https://docs.openhands.dev/) — [OFFICIAL]
- [OpenHands SDK docs](https://docs.openhands.dev/sdk) — [OFFICIAL]
- [OpenHands-CLI GitHub](https://github.com/OpenHands/OpenHands-CLI) — [OFFICIAL]
- [SWE-agent docs](https://swe-agent.com/) — [OFFICIAL]
- [SWE-agent GitHub](https://github.com/SWE-agent/SWE-agent) — [OFFICIAL]
- [mini-swe-agent GitHub](https://github.com/SWE-agent/mini-swe-agent) — [OFFICIAL]
- [Zed External Agents docs](https://zed.dev/docs/ai/external-agents) — [OFFICIAL]
- [Zed Agent Client Protocol](https://zed.dev/acp) — [OFFICIAL]
- [Warp](https://www.warp.dev/) — [OFFICIAL]
- [Warp Universal Agent Support blog](https://www.warp.dev/blog/universal-agent-support-level-up-coding-agent-warp) — [OFFICIAL]
- [cmux.com](https://cmux.com/) — [OFFICIAL]
- [manaflow-ai/cmux GitHub](https://github.com/manaflow-ai/cmux) — [OFFICIAL]
- [Qwen Code GitHub](https://github.com/QwenLM/qwen-code) — [OFFICIAL]

Practitioner sources:

- [OpenCode Plugin Development Guide — Lushbinary](https://lushbinary.com/blog/opencode-plugin-development-custom-tools-hooks-guide/) — [PRAC]
- [Superpowers for OpenCode — fsck.com](https://blog.fsck.com/2025/11/24/Superpowers-for-OpenCode/) — [PRAC]
- [OpenCode Review — OpenAIToolsHub](https://www.openaitoolshub.org/en/blog/opencode-review-terminal-ai-coding) — [PRAC]
- [The New Stack — Crush review](https://thenewstack.io/terminal-user-interfaces-review-of-crush-ex-opencode-al/) — [PRAC]
- [Crush Review 2026 — Vibe Coding Hub](https://vibecodinghub.org/tools/crush) — [PRAC]
- [Every AI Coding CLI in 2026 — DEV Community](https://dev.to/soulentheo/every-ai-coding-cli-in-2026-the-complete-map-30-tools-compared-4gob) — [PRAC]
- [Pi: The Minimal Agent — Armin Ronacher](https://lucumr.pocoo.org/2026/1/31/pi/) — [PRAC]
- [Pi Coding Agent — DEV Community](https://dev.to/theoklitosbam7/pi-coding-agent-a-self-documenting-extensible-ai-partner-dn) — [PRAC]
- [Claude Code vs Codex CLI 2026 — NxCode](https://www.nxcode.io/resources/news/claude-code-vs-codex-cli-terminal-coding-comparison-2026) — [PRAC]
- [10 Claude Code Alternatives — DigitalOcean](https://www.digitalocean.com/resources/articles/claude-code-alternatives) — [PRAC]
- [The 2026 Guide to Coding CLI Tools — Tembo](https://www.tembo.io/blog/coding-cli-tools-comparison) — [PRAC]
- [8 Best AI CLI Tools for Coding in 2026 — Morph](https://www.morphllm.com/best-ai-cli-tools-2026) — [PRAC]
- [Kilo Code vs Cline — Morph](https://www.morphllm.com/comparisons/kilo-code-vs-cline) — [PRAC]
- [Roo Code vs Cline — Qodo](https://www.qodo.ai/blog/roo-code-vs-cline/) — [PRAC]
- [OpenHands Review 2026 — Vibe Coding App](https://vibecoding.app/blog/openhands-review) — [PRAC]
- [cmux vs tmux — Soloterm](https://soloterm.com/cmux-vs-tmux) — [PRAC]
- [cmux Guide — Better Stack](https://betterstack.com/community/guides/ai/cmux-terminal/) — [PRAC]
- [Warp vs Intent — Augment Code](https://www.augmentcode.com/tools/intent-vs-warp) — [OFFICIAL (vendor)]
- [Visual Studio Magazine — Copilot CLI GA](https://visualstudiomagazine.com/articles/2026/03/02/github-copilot-cli-reaches-general-availability-bringing-agentic-coding-to-the-terminal.aspx) — [PRAC]
