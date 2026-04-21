---
content_origin: claude-code-subagent
date: 2026-04-21
sub_question: "How do ForgeCode, Goose AI (block/goose), OpenCode (sst/opencode), Qwen Code, Kilo Code, Aider, Cline, and any notable peers you surface compare on: model flexibility, orchestration primitives, extension model (agents/skills/hooks/MCP), and overall maturity?"
topic: "ForgeCode and agentic tooling evaluation for Momentum"
---

## Scope and Framing

This note compares the open-source/terminal-native agentic coding ecosystem that has grown up alongside Claude Code through 2025–2026. The comparison centers on the four dimensions Momentum cares about as a practice layer: **model flexibility**, **orchestration primitives**, **extension model** (skills / agents / hooks / MCP), and **overall maturity**. A secondary axis — where the tool lives (CLI vs IDE vs hybrid) — is critical for Momentum because Momentum's primitives (file-authoritative rules, deterministic workflows, hook-driven enforcement) are CLI-native and depend on process-level extensibility.

The tools surveyed:

1. **ForgeCode** (tailcallhq/forgecode) — harness-first terminal agent, Terminal-Bench 2.0 leader
2. **Goose** (block/goose) — Block-incubated, Rust, now at Linux Foundation AAIF
3. **OpenCode** (sst/opencode) — SST-incubated, client/server TUI
4. **Aider** (Aider-AI/aider) — git-native pair programmer, the elder statesman
5. **Cline** (cline/cline) — VS Code autonomous agent
6. **Qwen Code** (QwenLM/qwen-code) — Alibaba's Gemini-CLI fork tuned for Qwen3-Coder
7. **Kilo Code** (Kilo-Org/kilocode) — Cline+Roo fork, "all-in-one platform"
8. **Roo Code** (RooCodeInc/Roo-Code) — Cline fork with custom modes
9. **Codex CLI** (openai/codex) — OpenAI's Rust terminal agent
10. **Crush** (charmbracelet/crush) — Charm's Bubble Tea TUI agent
11. **Continue.dev** (continuedev/continue) — IDE assistant pivoting to CI quality checks

Today is 2026-04-21. Sources older than 2 years will be flagged; most inputs below are 2025–2026.

## Taxonomy: Claude-Code-Like vs Editor-Integrated vs Hybrid

The first cut to make before comparing features is **where the tool runs** and **who extends it**:

- **Claude-Code-like (agentic CLI with extension surface):** ForgeCode, Goose (CLI + desktop), OpenCode, Aider, Qwen Code, Codex CLI, Crush. These are standalone processes with a config/plugin/MCP surface that treats the terminal as the primary UI. They match Momentum's shape.
- **Editor-integrated helpers:** Cline, Roo Code, Continue.dev (primarily). These are VS Code/JetBrains extensions. Extension surfaces are IDE-scoped (commands, settings panes, `.clinerules` etc.) rather than shell-level hooks.
- **Hybrid:** Kilo Code (VS Code + JetBrains + CLI + App Builder), Goose (CLI + desktop + API), OpenCode (TUI + beta desktop + mobile drive via client/server), Continue.dev (IDE + CLI for CI checks).

For Momentum, the Claude-Code-like row is the relevant integration surface. Editor-integrated tools cannot host Momentum's hook/rule/skill primitives in the same way.

## Comparison Matrix

| Tool | Primary UI | License | Stars | Model Flex | Orchestration | Extension Model | Maturity Signal |
|------|------------|---------|-------|------------|---------------|-----------------|-----------------|
| **ForgeCode** | Terminal/ZSH | Apache-2.0 | ~6.8k | 300+ models, OpenAI/Anthropic/Gemini/Groq/Bedrock/OpenRouter ([OFFICIAL](https://github.com/tailcallhq/forgecode)) | Forge/Muse/Sage built-in agents; custom `.forge/agents/*.md` with YAML front-matter; sequential | `forge.yaml` config, MCP (`.mcp.json`), custom agents, skills | v2.12.0 (Apr 2026); claims #1 on Terminal-Bench 2.0 at 81.8% ([PRAC](https://medium.com/@richardhightower/forgecode-dominating-terminal-bench-2-0-harness-engineering-beat-claude-code-codex-gemini-etc-eb5df74a3fa4)) |
| **Goose** | CLI + desktop + API | Apache-2.0 | ~42.9k | 15–25+ providers incl. Anthropic, OpenAI, Gemini, Ollama, Bedrock, Azure; subscription passthrough via ACP ([OFFICIAL](https://github.com/block/goose)) | Recipes, extensions, sub-agent workflows via MCP | MCP-native (70+ extensions), Skills directory conventions (`.agents/skills`), recipes | v1.31.1 (Apr 2026); 110+ releases; contributed to Linux Foundation AAIF Dec 2025 ([OFFICIAL](https://block.xyz/inside/block-open-source-introduces-codename-goose)) |
| **OpenCode** | TUI (+ beta desktop, mobile drive) | MIT | ~147k | Anthropic/OpenAI/Google/Bedrock/Groq/Azure/OpenRouter + local; OpenCode Zen gateway ([OFFICIAL](https://github.com/sst/opencode)) | Built-in `build` + `plan` agents; `@general` subagent; multi-session parallel; client/server | Agents as primary extension; MCP; config via `opencode.json` | v1.14.20 (Apr 2026); highest star count in set; TypeScript-heavy |
| **Aider** | CLI | Apache-2.0 | ~43.7k | OpenAI, Anthropic, Gemini, DeepSeek, local ("almost any LLM") ([OFFICIAL](https://github.com/Aider-AI/aider)) | Architect/Editor mode pairing; watch mode; repo map; git-native auto-commit | MCP Registry (newer), `.aider.conf.yml`, `CONVENTIONS.md` prompt injection | v0.86.0 (Aug 2025 — stalled vs peers); 84.9% polyglot benchmark with o3-pro |
| **Cline** | VS Code extension | Apache-2.0 | ~60.5k | OpenRouter, Anthropic, OpenAI, Gemini, Bedrock, Azure, Vertex, Cerebras, Groq, LM Studio/Ollama ([OFFICIAL](https://github.com/cline/cline)) | Plan/Act modes; human-in-loop approvals | `.clinerules/` directory; MCP server marketplace; browser tool | v3.79.0 (Apr 2026); active monthly cadence |
| **Qwen Code** | CLI (+ VS Code/Zed/JetBrains integration) | Apache-2.0 | ~23.6k | OpenAI-compat, Anthropic, Gemini, ModelStudio, OpenRouter, Fireworks, Vertex, Ollama/vLLM ([OFFICIAL](https://github.com/QwenLM/qwen-code)) | Skills + SubAgents; session compression | Skills-based; TypeScript SDK; `@path` skill refs | v0.14.5 (Apr 2026); Gemini-CLI fork tuned for Qwen3-Coder |
| **Kilo Code** | VS Code + JetBrains + CLI + App Builder | MIT | ~18.4k | 500+ models across 30+ providers (transparent passthrough) ([OFFICIAL](https://github.com/Kilo-Org/kilocode)) | Orchestrator mode delegating to Architect/Coder/Debugger; custom modes | `.kilocode/skills/*`; MCP Server Marketplace; custom modes | v7.2.14 (Apr 2026); $8M seed Jan 2026; 1.5M users claim ([PRAC](https://vibecoding.app/blog/kilo-code-review)) |
| **Roo Code** | VS Code | Apache-2.0 | ~23.3k | Multi-provider BYOK incl. xAI, Poe, MiniMax + standard set | Architect/Code/Ask/Debug + custom modes; "boomerang" task delegation | Modes as extension primitive; MCP | v3.52.1 (Apr 2026); enterprise focus, SOC 2 |
| **Codex CLI** | CLI (Rust) | Apache-2.0 | (large) | OpenAI models only; ChatGPT subscription or API key ([OFFICIAL](https://developers.openai.com/codex/cli)) | To-do tracking; MCP; web search; Agents SDK orchestration | Agent Skills (OpenAI spec), MCP, hooks via OMX layer | GPT-5-Codex tuned model; GitHub-native Feb 2026 release |
| **Crush** | TUI (Go/Bubble Tea) | FSL-1.1-MIT | ~23.3k | Anthropic, OpenAI, Gemini, Groq, OpenRouter, HF, Bedrock, Azure, Vercel AI Gateway, custom ([OFFICIAL](https://github.com/charmbracelet/crush)) | Mid-session model switching; LSP-enhanced context; permission prompts / `--yolo` | MCP (stdio/http/sse); Agent Skills standard; JSON config layered | v0.61.1 (Apr 2026); broadest OS coverage (macOS/Linux/Windows/*BSD/Android) |
| **Continue.dev** | VS Code + JetBrains + CLI | Apache-2.0 | (large) | Any provider via hub agents | Hub agents; agent mode; PR checks in CI | `.continue/checks/*.md` markdown agents; MCP pre-configured via hub | Pivoting to "source-controlled AI checks" for CI ([OFFICIAL](https://github.com/continuedev/continue)) |

## Per-Tool Deep Dive

### ForgeCode — Harness-First Multi-Agent CLI

ForgeCode is the clearest philosophical peer to Claude Code plus a Momentum-style practice layer baked in. Its architecture is **three built-in roles — Forge (implementation), Muse (planning, writes to `plans/`), Sage (research/read-only)** — with custom agents defined as markdown files with YAML front-matter in `.forge/agents/` ([OFFICIAL](https://github.com/tailcallhq/forgecode)). It supports `forge.yaml` for rules/commands/model selection/temperature/failure limits, and MCP via `.mcp.json`. It ships a ZSH `:` prefix for in-shell invocation alongside full TUI and one-shot CLI modes. Model support spans 300+ models via OpenRouter-style passthrough (OpenAI, Anthropic, Gemini, Groq, Bedrock, Vertex, DeepSeek).

Marketing claim: "World's #1 Coding Harness" on TermBench 2.0 at 81.8% beating Claude Code, Codex, and Gemini-CLI ([PRAC](https://medium.com/@richardhightower/forgecode-dominating-terminal-bench-2-0-harness-engineering-beat-claude-code-codex-gemini-etc-eb5df74a3fa4)). Treat the benchmark claim as vendor-aligned; the architectural claim (that a better harness beats a better model) is the interesting thesis for Momentum. ForgeCode is the smallest in this set by stars (~6.8k) but its primitives — YAML-front-matter agents, workflow config, MCP, skills — map almost 1:1 onto Momentum's shape. **This makes it Momentum's closest "parallel track" candidate.**

### Goose — Rust Agent with Deepest MCP Ecosystem

Goose (block/goose) is the most mature in terms of governance and breadth: **42.9k stars, 110+ releases, 350+ contributors, and as of December 2025 contributed to the Linux Foundation's Agentic AI Foundation alongside MCP itself and OpenAI's AGENTS.md standard** ([OFFICIAL](https://block.xyz/inside/block-open-source-introduces-codename-goose), [PRAC](https://effloow.com/articles/goose-open-source-ai-agent-review-2026)). Originally released January 2025 by Block, it ships as CLI + native desktop (macOS/Linux/Windows) + embeddable API. Model flex spans 15–25+ providers (Anthropic, OpenAI, Gemini, Ollama, Docker Model Runner, Ramalama, Azure, Bedrock, xAI, Mistral) plus subscription passthrough via ACP (Agent Client Protocol) so users can use existing Claude/ChatGPT/Gemini subscriptions ([PRAC](https://www.paperclipped.de/en/blog/goose-block-open-source-ai-agent/)).

Extension model is MCP-first with 70+ documented extensions and 3,000+ available via broader MCP ecosystem. The repo structure shows `.agents/skills`, `.claude/skills`, `.codex/skills`, `.cursor/skills` — suggesting an emerging cross-vendor **skills convention**. Recipes provide reusable workflow templates. Written in Rust, which is a relevant operational signal for a practice-layer host.

For Momentum: Goose is the **most likely "integration" target** rather than replacement — its MCP ecosystem could host Momentum skills, but Goose's own skill/recipe model competes with Momentum's primitives.

### OpenCode — Client/Server TUI with Highest Community Velocity

OpenCode (sst/opencode) is by far the highest-star tool in this set at ~147k, reflecting SST's momentum and the "open Claude Code" positioning ([OFFICIAL](https://github.com/sst/opencode)). Its differentiators: **client/server architecture** (you can drive an OpenCode instance from a mobile app, similar to a headless daemon), two built-in agents (`build` full-access, `plan` read-only) plus a `@general` subagent, **multi-session parallel execution**, and a beta desktop app. MIT-licensed, TypeScript-heavy.

Model flex is broad: Anthropic, OpenAI, Google, Bedrock, Groq, Azure, OpenRouter, local, plus OpenCode's own "Zen" gateway. Extension model is agent-centric (agents are the primary first-class abstraction) with MCP and config via `opencode.json`. The built-in plan-vs-build split is essentially a two-agent Architect/Dev orchestration baked in.

The client/server design is interesting for Momentum because it separates UI from the agent process — in principle a Momentum workflow engine could drive OpenCode as a headless worker. That said, OpenCode's agent model is less developer-facing (less file-authoritative) than ForgeCode's YAML-front-matter agents. ([PRAC](https://sanj.dev/post/comparing-ai-cli-coding-assistants), [PRAC](https://www.infralovers.com/blog/2026-01-29-claude-code-vs-opencode/))

### Aider — The Elder Statesman, Now Lagging Cadence

Aider predates the modern agentic wave; Paul Gauthier started it in 2023. It is git-native (auto-commits changes with sensible messages), has a high-quality **repo map** that extracts symbol information from the codebase, supports an Architect/Editor two-model mode, voice input, image/webpage context, and runs in a watch mode that integrates with any editor via file notifications ([OFFICIAL](https://github.com/Aider-AI/aider), [PRAC](https://agentwiki.org/aider)). Achieves 84.9% on its polyglot benchmark with o3-pro.

**Caution flag:** latest GitHub release appears to be v0.86.0 dated August 9, 2025, meaning Aider has not shipped a release in ~8 months as of April 2026. That's a meaningful cadence gap relative to Goose (monthly), OpenCode (daily), Cline (monthly), and Kilo (weekly). Extension model is comparatively thin: `.aider.conf.yml`, `CONVENTIONS.md` for prompt injection, and a more recently added MCP Registry. For Momentum the takeaway is that Aider is a **conceptual reference** (first to popularize repo-map + architect mode) but not a live integration track.

### Cline — VS Code Autonomous Agent with Plan/Act

Cline (cline/cline, 60.5k stars, Apache 2.0) is the strongest VS Code-native agent ([OFFICIAL](https://github.com/cline/cline)). Core primitives: **Plan mode** (analyze/explore, no modification) vs **Act mode** (execute with step-by-step approval), browser automation (headless Chromium for visual debugging), terminal integration, and MCP support. Extension surface is a `.clinerules/` directory (file-authoritative rules) plus MCP servers and a marketplace. Model flex: OpenRouter, Anthropic, OpenAI, Gemini, Bedrock, Azure, Vertex, Cerebras, Groq, LM Studio, Ollama. Latest v3.79.0 Apr 2026, monthly cadence.

Cline is editor-integrated, not CLI, so Momentum cannot host its skills/workflows inside Cline directly — but Cline has inspired the shape of several others (Roo, Kilo) and demonstrates that `.clinerules` is a converged pattern for file-authoritative rules that Momentum already uses. ([PRAC](https://www.devtoolreviews.com/reviews/cline-vs-roo-code-vs-continue))

### Qwen Code — Gemini-CLI Fork, Model-Tuned

Qwen Code (QwenLM/qwen-code, ~23.6k stars, Apache-2.0) is Alibaba's adaptation of Google's Gemini CLI, customized at the parser level for Qwen3-Coder's function-calling format ([OFFICIAL](https://github.com/QwenLM/qwen-code), [OFFICIAL](https://qwenlm.github.io/blog/qwen3-coder/)). It emphasizes Skills + SubAgents as first-class primitives, supports OpenAI/Anthropic/Gemini-compatible APIs plus ModelStudio/OpenRouter/Fireworks/Vertex/Ollama/vLLM, and ships IDE integrations (VS Code, Zed, JetBrains) plus a TypeScript SDK. Qwen3-Coder-480B-A35B offers 256K native context extendable to 1M via YaRN — attractive for repo-scale tasks. Latest v0.14.5 April 2026.

For Momentum: Qwen Code is a **model-access path** more than an orchestration peer. Its Gemini-CLI lineage means similar extension shape to Google's official CLI, but it's not architecturally distinctive relative to ForgeCode/Goose/OpenCode.

### Kilo Code — The Aggregator Fork

Kilo Code (Kilo-Org/kilocode, ~18.4k stars, MIT) took the interesting path: fork both Cline and Roo Code, then add **Orchestrator mode** that delegates subtasks to Architect/Coder/Debugger specialists, ship across VS Code + JetBrains + CLI (`@kilocode/cli`) + App Builder, and offer 500+ models through 30+ providers with transparent pass-through pricing ([OFFICIAL](https://github.com/Kilo-Org/kilocode), [PRAC](https://kilo.ai/)). Raised $8M seed in January 2026. Adds Memory Bank, voice commands, MCP Server Marketplace, `.kilocode/skills/*` directory. 1.5M user claim (vendor).

Kilo's Orchestrator-delegates-to-specialists model is directly analogous to Momentum's Impetus-spawning-subagents pattern. The mode-based architecture (Architect/Coder/Debugger) is also analogous to Momentum's agent specialization. For Momentum, Kilo is an **architectural validation** — multiple teams are converging on the same orchestration shape.

### Roo Code — Cline's Enterprise Fork

Roo Code (RooCodeInc/Roo-Code, 23.3k stars, Apache 2.0) forked Cline to add: custom modes (Architect/Code/Ask/Debug + user-defined), Roo Cloud for hosted agents, SOC 2 compliance, and a "boomerang" pattern for task delegation between modes ([OFFICIAL](https://github.com/RooCodeInc/Roo-Code)). Reputation in 2026 community threads is as the tool developers reach for on large, multi-file changes when others break down ([PRAC](https://www.qodo.ai/blog/roo-code-vs-cline/)). Latest v3.52.1 April 2026.

### Codex CLI — OpenAI's Native Rust Agent

OpenAI's codex CLI (Rust, open-source) is their terminal response to Claude Code ([OFFICIAL](https://developers.openai.com/codex/cli)). GPT-5-Codex is the trained-for-agentic variant of GPT-5. Features: to-do list tracking for complex work, web search, MCP support, Agents SDK integration that exposes the CLI itself as an MCP server. Agent Skills are an explicit OpenAI spec — markdown files describing agent capabilities, now part of the emerging cross-vendor skills convention alongside AGENTS.md ([OFFICIAL](https://developers.openai.com/codex/skills)).

**Notable emergent layer:** "Oh My Codex" (OMX) is an open-source orchestration layer on top of Codex CLI that adds multi-agent coordination, persistent state, hooks, and structured workflows — essentially reinventing the Momentum/ForgeCode harness on top of Codex ([PRAC](https://a2a-mcp.org/blog/what-is-oh-my-codex)). This is a strong market signal that **Momentum's harness concept is real and not Claude-specific** — it's being rebuilt for every base CLI.

Limitation: Codex CLI only works with OpenAI models (via API or ChatGPT subscription). Not model-flexible.

### Crush — Charmbracelet's Bubble Tea TUI

Crush (charmbracelet/crush, ~23.3k stars, FSL-1.1-MIT) is the tool built by the Bubble Tea / Charm team ([OFFICIAL](https://github.com/charmbracelet/crush)). Key features: MCP support via stdio/http/sse transports, **mid-session model switching** (change provider without restarting context), LSP-enhanced context (symbol resolution via language servers), permission model with `--yolo` autonomy flag. Model flex is broad: Anthropic, OpenAI, Gemini, Groq, OpenRouter, HuggingFace, Bedrock, Azure, Vercel AI Gateway, custom compat APIs. Broadest OS coverage in the set (macOS/Linux/Windows/FreeBSD/OpenBSD/NetBSD/Android). Crush also adopts the **Agent Skills open standard** — the same cross-vendor convention Goose and Codex use.

For Momentum: Crush is interesting because it demonstrates that **MCP + Agent Skills + LSP** is becoming the minimum viable terminal-agent stack. If that triple becomes standardized, Momentum's skills could target it as a portable substrate.

### Continue.dev — Pivoting from Copilot to CI

Continue.dev (continuedev/continue) was originally an open VS Code/JetBrains Copilot alternative with Agent mode. In 2025–2026 it pivoted to **source-controlled AI checks enforceable in CI**: agents as markdown files in `.continue/checks/` that run on every PR as GitHub status checks ([OFFICIAL](https://github.com/continuedev/continue), [PRAC](https://blog.continue.dev/beyond-code-generation-how-continue-enables-ai-code-review-at-scale)). The hub provides pre-configured MCP tools for databases, docs, browser automation. This pivot toward "AI as source-controlled review gates" is a strong parallel to Momentum's adversarial validate-fix loop — except executed in CI rather than in-session.

## Cross-Cutting Observations

### Convergence on `.xxx/skills/` + MCP + Agent Markdown Files

By April 2026 the extension-surface conventions have visibly converged. Repo structure evidence: Goose has `.agents/skills`, `.claude/skills`, `.codex/skills`, `.cursor/skills` side-by-side; ForgeCode uses `.forge/agents/*.md`; Kilo uses `.kilocode/skills/*`; Cline uses `.clinerules/`; Continue uses `.continue/checks/*.md`; Codex has Agent Skills as an official OpenAI spec; Crush supports "Agent Skills open standard." **This is directly aligned with Momentum's file-authoritative-skills premise** — the market is telling Momentum its foundational bet is correct.

### MCP Is Table Stakes, Hooks Are Not

Every tool except Aider (which added MCP Registry only recently) has first-class MCP support. Hooks, by contrast, are rare: **Claude Code has hooks, Momentum has hooks, OMX adds hooks to Codex**, but Goose/OpenCode/ForgeCode/Cline/Roo/Kilo do not expose shell-hook lifecycle events in the same way. Hooks remain a Claude-Code-specific differentiator that Momentum leverages.

### Orchestration Primitives Are Re-Converging on "Planner + Specialists"

The Architect/Coder/Debugger triplet (or Plan/Build pair) appears in OpenCode, Kilo, Roo, Cline, ForgeCode (Muse/Forge/Sage), and Claude Code's own plan mode. **Momentum's Impetus-orchestrator + specialist-subagents model is the mainstream pattern in 2026**, not an outlier.

### Maturity Ranking (April 2026)

By a combined signal of stars + release cadence + governance + commercial backing:

1. **OpenCode** — highest stars (147k), daily releases, SST-backed
2. **Cline** — 60.5k stars, monthly cadence, commercial entity (Cline Bot Inc.)
3. **Goose** — 42.9k stars, 110+ releases, Linux Foundation governance
4. **Aider** — 43.7k stars BUT release stalled since Aug 2025 — maturity signal is weakening
5. **Crush** — 23.3k stars, Charm-backed, daily releases
6. **Roo Code** — 23.3k stars, SOC 2 compliant, commercial entity
7. **Qwen Code** — 23.6k stars, Alibaba-backed
8. **Kilo Code** — 18.4k stars, $8M seed, most aggressive feature velocity
9. **ForgeCode** — 6.8k stars, benchmark claims but smallest community

### Model Flexibility Ranking

1. **Kilo Code** — 500+ models / 30+ providers
2. **ForgeCode / OpenRouter-style routers** — 300+ models
3. **Crush / Cline / OpenCode** — broad provider set + OpenAI-compat + local
4. **Goose** — 25+ providers with subscription passthrough via ACP
5. **Aider / Qwen Code / Roo Code** — strong multi-provider
6. **Codex CLI** — OpenAI only (intentional, but a real limitation)

### CLI vs IDE Split

- **Pure CLI/TUI:** ForgeCode, Aider, Codex CLI, Crush
- **CLI + desktop + API:** Goose, OpenCode (client/server)
- **Multi-surface (IDE + CLI):** Kilo Code, Qwen Code, Continue.dev
- **Pure IDE extension:** Cline, Roo Code

## Implications for Momentum

Translating the landscape into Momentum-specific options:

**Parallel track candidates (Claude-Code-like, primitives aligned):** ForgeCode is the closest structural match. Its Forge/Muse/Sage + YAML-front-matter agents + `forge.yaml` + `.mcp.json` shape is functionally isomorphic to Momentum's Impetus + subagent + rules + MCP shape. A Momentum-on-ForgeCode port would be a small exercise compared to a Momentum-on-Goose port.

**Integration-point candidates (host Momentum skills inside their ecosystem):** Goose (MCP-native with 3,000+ extension universe), OpenCode (client/server lets Momentum drive headless), Codex CLI (Agents SDK + MCP exposure). Each would require Momentum to target a specific skill/extension format.

**Partial-replacement candidates:** Kilo Code's Orchestrator mode + Architect/Coder/Debugger triplet overlaps Momentum's sprint-dev Impetus-spawning-subagents workflow — but Kilo is IDE-forward rather than file-authoritative. Continue.dev's `.continue/checks/` in-CI agents overlap Momentum's AVFL loop — but shifted to post-merge CI rather than in-session adversarial pre-merge.

**Non-candidates:** Aider (cadence stalled), Cline/Roo (editor-bound), Qwen Code (model path, not orchestration peer), Codex CLI in isolation (OpenAI-only lock-in).

**Signal to take seriously:** The emergence of "Oh My Codex" (OMX) — an independent project that adds hooks, multi-agent, persistent state, structured workflows on top of Codex — proves that Momentum's harness concept is being reinvented on every base CLI. Momentum's opportunity is to be the **portable practice layer** that targets the converging `.xxx/skills/` + MCP + Agent Skills substrate rather than being Claude-specific.

## Sources

- [ForgeCode GitHub](https://github.com/tailcallhq/forgecode) [OFFICIAL]
- [ForgeCode landing](https://forgecode.dev/) [OFFICIAL]
- [ForgeCode Medium deep dive (Rick Hightower, Apr 2026)](https://medium.com/@richardhightower/forgecode-dominating-terminal-bench-2-0-harness-engineering-beat-claude-code-codex-gemini-etc-eb5df74a3fa4) [PRAC]
- [ForgeCode Review aicoolies](https://aicoolies.com/reviews/forgecode-review) [PRAC]
- [Ralph Wiggum: Agentic Coding Frameworks 2026](https://ralphwiggum.org/blog/agentic-coding-frameworks-guide) [PRAC]
- [Goose GitHub (block/goose)](https://github.com/block/goose) [OFFICIAL]
- [Goose docs](https://goose-docs.ai/) [OFFICIAL]
- [Block Open Source: Introducing Goose](https://block.xyz/inside/block-open-source-introduces-codename-goose) [OFFICIAL]
- [Effloow: Goose by Block Review](https://effloow.com/articles/goose-open-source-ai-agent-review-2026) [PRAC]
- [Paperclipped: Goose vs Claude Code setup guide 2026](https://www.paperclipped.de/en/blog/goose-block-open-source-ai-agent/) [PRAC]
- [Marc Nuri: Goose on-machine AI agent](https://blog.marcnuri.com/goose-on-machine-ai-agent-cli-introduction) [PRAC]
- [OpenCode GitHub (sst/opencode)](https://github.com/sst/opencode) [OFFICIAL]
- [OpenCode docs](https://opencode.ai/docs/) [OFFICIAL]
- [OpenCode CLI docs](https://opencode.ai/docs/cli/) [OFFICIAL]
- [DeepWiki: sst/opencode Tools Reference](https://deepwiki.com/sst/opencode/5.3-built-in-tools-reference) [PRAC]
- [sanj.dev: Aider vs OpenCode vs Claude Code 2026](https://sanj.dev/post/comparing-ai-cli-coding-assistants) [PRAC]
- [Infralovers: Claude Code vs OpenCode](https://www.infralovers.com/blog/2026-01-29-claude-code-vs-opencode/) [PRAC]
- [OpenAIToolsHub: OpenCode vs Claude Code](https://www.openaitoolshub.org/en/blog/opencode-vs-claude-code) [PRAC]
- [Aider GitHub (Aider-AI/aider)](https://github.com/Aider-AI/aider) [OFFICIAL]
- [Aider Releases](https://github.com/Aider-AI/aider/releases) [OFFICIAL]
- [AgentWiki: Aider](https://agentwiki.org/aider) [PRAC]
- [AI for Developers: Aider 2026](https://aifordevelopers.org/tool/github-com-paul-gauthier-aider) [PRAC]
- [Cline GitHub](https://github.com/cline/cline) [OFFICIAL]
- [Cline site](https://cline.bot) [OFFICIAL]
- [Cline VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) [OFFICIAL]
- [DevToolReviews: Cline vs Roo vs Continue](https://www.devtoolreviews.com/reviews/cline-vs-roo-code-vs-continue) [PRAC]
- [VibeCoding: Cline Review 2026](https://vibecoding.app/blog/cline-review-2026) [PRAC]
- [Morph: Cline alternatives 2026](https://www.morphllm.com/comparisons/cline-alternatives) [PRAC]
- [Qwen Code GitHub (QwenLM/qwen-code)](https://github.com/QwenLM/qwen-code) [OFFICIAL]
- [Qwen3-Coder blog (Qwen team)](https://qwenlm.github.io/blog/qwen3-coder/) [OFFICIAL]
- [Qwen3-Coder GitHub](https://github.com/QwenLM/Qwen3-Coder) [OFFICIAL]
- [RITS Shanghai NYU: Introducing Qwen-Code](https://rits.shanghai.nyu.edu/ai/introducing-qwen-code-alibabas-open%E2%80%91source-cli-for-agentic-coding-with-qwen3%E2%80%91coder/) [PRAC]
- [MindStudio: Qwen 3.6 Plus review](https://www.mindstudio.ai/blog/qwen-3-6-plus-review-agentic-coding-model) [PRAC]
- [Kilo Code GitHub](https://github.com/Kilo-Org/kilocode/) [OFFICIAL]
- [Kilo Code site](https://kilo.ai/) [OFFICIAL]
- [Kilo Code VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=kilocode.Kilo-Code) [OFFICIAL]
- [VibeCoding: Kilo Code review](https://vibecoding.app/blog/kilo-code-review) [PRAC]
- [Kilo vs Roo comparison (openalternative.co)](https://openalternative.co/compare/kilocode/vs/roo-code) [PRAC]
- [Ai505: Kilo vs Roo vs Cline 2026](https://ai505.com/kilo-code-vs-roo-code-vs-cline-the-2026-ai-coding-battle-nobody-saw-coming/) [PRAC]
- [Kilo blog: 6 Open-Source Copilot Alternatives](https://kilo.ai/articles/open-source-github-copilot-alternatives) [PRAC]
- [Roo Code GitHub](https://github.com/RooCodeInc/Roo-Code) [OFFICIAL]
- [Qodo: Roo Code vs Cline](https://www.qodo.ai/blog/roo-code-vs-cline/) [PRAC]
- [Codex CLI docs (OpenAI)](https://developers.openai.com/codex/cli) [OFFICIAL]
- [Codex GitHub (openai/codex)](https://github.com/openai/codex) [OFFICIAL]
- [OpenAI: Upgrades to Codex](https://openai.com/index/introducing-upgrades-to-codex/) [OFFICIAL]
- [Codex Agent Skills docs](https://developers.openai.com/codex/skills) [OFFICIAL]
- [Codex MCP docs](https://developers.openai.com/codex/mcp) [OFFICIAL]
- [Codex + Agents SDK guide](https://developers.openai.com/codex/guides/agents-sdk) [OFFICIAL]
- [a2a-mcp: What is Oh My Codex (OMX)](https://a2a-mcp.org/blog/what-is-oh-my-codex) [PRAC]
- [Crush GitHub (charmbracelet/crush)](https://github.com/charmbracelet/crush) [OFFICIAL]
- [Crush README](https://github.com/charmbracelet/crush/blob/main/README.md) [OFFICIAL]
- [Tembo: 2026 Guide to Coding CLI Tools — 15 Agents Compared](https://www.tembo.io/blog/coding-cli-tools-comparison) [PRAC]
- [Silver Umbrella: Crush vs OpenCode](https://ian729.github.io/silver-umbrella/ai/cli/tools/crushcli/opencode/2026/02/23/crush-cli-comparison.html) [PRAC]
- [Continue.dev GitHub (continuedev/continue)](https://github.com/continuedev/continue) [OFFICIAL]
- [Continue docs](https://docs.continue.dev/) [OFFICIAL]
- [Continue: Quality control for your software factory](https://www.continue.dev/) [OFFICIAL]
- [Continue blog: Beyond Code Generation — AI Code Review at Scale](https://blog.continue.dev/beyond-code-generation-how-continue-enables-ai-code-review-at-scale) [OFFICIAL]
- [Visual Studio Magazine: Top Agentic AI Tools for VS Code by Installs](https://visualstudiomagazine.com/articles/2025/10/07/top-agentic-ai-tools-for-vs-code-according-to-installs.aspx) [PRAC]
- [Artificial Analysis: Coding Agents Comparison](https://artificialanalysis.ai/agents/coding) [PRAC]
- [WeTheFlyWheel: Open-Source AI Coding Agents 2026](https://wetheflywheel.com/en/guides/open-source-ai-coding-agents-2026/) [PRAC]
- [Faros AI: Best AI Coding Agents 2026](https://www.faros.ai/blog/best-ai-coding-agents-2026) [PRAC]
- [OpenSourceAIReview: Best Open Source AI Coding Agents 2026](https://www.opensourceaireview.com/blog/best-open-source-ai-coding-agents-in-2026-ranked-by-developers) [PRAC]
- [Morph: 15 AI Coding Agents Tested](https://www.morphllm.com/ai-coding-agent) [PRAC]
