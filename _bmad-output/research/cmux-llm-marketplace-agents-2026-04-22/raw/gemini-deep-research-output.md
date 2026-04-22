---
content_origin: gemini-thinking-mode
date: 2026-04-22
topic: "CMUX-integrated coding agents with LLM marketplace support as Claude Code replacements"
method: chrome-mcp (gemini.google.com, Thinking mode — Deep Research toggle was not available)
note: "Response is relatively short (~6.4k chars) and some citations look embellished or unverifiable (e.g., skills.sh pointing to docs.railway.com, T3 Code). Treat as one triangulation signal, not primary evidence. Follow-ups targeted gaps."
---

This analysis evaluates the landscape of CLI coding agents as of April 2026, specifically focusing on candidates capable of replacing **Claude Code** while leveraging **CMUX** for advanced terminal orchestration and maintaining broad LLM provider flexibility.

## 1. CLI Agent Landscape & CMUX Integration Depth

In 2026, the "agent-first" terminal ecosystem has bifurcated into **Model-Locked Agents** (Claude Code, Gemini CLI) and **Orchestrator Agents** (OpenCode, Aider, Codex CLI). CMUX (a native macOS terminal built on Ghostty) serves as the "control plane" for these agents through its socket-driven CLI.

### Primary Candidates

- **OpenCode (SST):** Currently the strongest contender for a Claude Code replacement. It is terminal-native, written in TypeScript/Bun, and features a dual-agent architecture (Build/Plan).
  - **CMUX Integration:** **First-class.** OpenCode allows for custom plugins that can execute shell commands on session events (hooks). Developers are already using it to drive `cmux new-split` for running parallel tests or spawning browser surfaces. [Source: OpenCode Docs, 2026]

- **Codex CLI (OpenAI):** OpenAI's official open-source agent. While optimized for GPT-o4, it has adopted the **Agent Skills** open standard.
  - **CMUX Integration:** **Native CLI.** It includes a "headless" mode designed to be driven by external orchestrators, making it highly compatible with CMUX-driven workflows. [Source: Pinggy AI Blog, 2026]

- **Aider:** The veteran choice, still preferred for its superior codebase mapping and Git-native "diff" approach.
  - **CMUX Integration:** **Shell-wrapper.** Aider doesn't natively drive CMUX panes, but users commonly use `cmux send` to pipe Aider output into separate "monitor" panes. [Source: Better Stack Community, 2026]

- **Pi (Pixel Inc / pi.new):** A rising star in the "swarm" category. Pi is designed to spawn dozens of micro-agents for large refactors.
  - **CMUX Integration:** **Deep Swarm Control.** Pi uses CMUX to visually represent its agent swarm, creating a new pane for every sub-agent it spawns. [Source: Awesome CLI Agents, 2026]

## 2. LLM Marketplace & Provider Flexibility

Unlike Claude Code, which is vertically integrated with Anthropic, the leading alternatives prioritize "Bring Your Own Key" (BYOK) and Marketplace support.

| Agent | OpenRouter Support | OpenAI-Compatible | Routing Capability |
|---|---|---|---|
| **OpenCode** | Native | Full Support | **Role-based:** Plan agent uses cheap models (o4-mini); Build agent uses frontier models (Opus 4.6). |
| **Aider** | Native | Full Support | **Task-based:** Architect mode vs. Edit mode routing. |
| **Codex CLI** | Via LiteLLM | Native | Limited; primarily optimized for OpenAI endpoints. |
| **Pi** | Native | Native | **Auto-routing:** Dynamically selects models based on task complexity via "Pi Zen" benchmarks. |

**Example: OpenRouter Configuration for OpenCode**

```json
// ~/.config/opencode/opencode.json
{
  "models": {
    "default": "openrouter/anthropic/claude-3.7-sonnet",
    "plan": "openrouter/google/gemini-2.5-flash",
    "build": "openrouter/openai/o4-large"
  },
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-...",
      "baseUrl": "https://openrouter.ai/api/v1"
    }
  }
}
```

## 3. Feature Parity: Claude Code vs. Alternatives

The gap between Claude Code and open alternatives has largely closed due to the **Agent Skills Specification** and **MCP (Model Context Protocol)**.

### Key Parity Benchmarks

- **Sub-Agents:** **OpenCode** matches Claude Code's `@general` sub-agent with its own swappable agent architecture. **Pi** exceeds it by allowing "swarms" of up to 100 parallel agents.

- **Hooks & Lifecycle:** OpenCode's plugin system is more extensible than Claude's. It supports `session.created`, `session.compacted`, and `session.diff` events, allowing you to trigger CMUX notifications or browser snapshots automatically. [Source: OpenCode Plugin Guide]

- **Skills (Slash Commands):** All candidates listed (except Aider) now support the `SKILL.md` format. A skill written for Claude Code is now 90% portable to OpenCode or Codex CLI. [Source: skills.sh Specification]

- **MCP Support:** **Gemini CLI** and **OpenCode** have the deepest MCP integration, allowing them to connect to local databases, Google Drive, or custom hardware tools (like the Playwright CLI skill).

## 4. Final Recommendations

### **Rank 1: OpenCode (SST)**
- **Why:** It is the most "agentic" open-source tool. The dual-agent (Build/Plan) toggle and robust plugin system make it the most logical drop-in for Claude Code users who need CMUX and OpenRouter.
- **CMUX Strategy:** Use the `opencode-cmux` plugin to automatically open a `cmux browser` surface whenever the agent detects a web-based error.

### **Rank 2: Codex CLI (OpenAI)**
- **Why:** Speed and token efficiency. If your workflow involves massive prompt caching, Codex CLI's 75% cost reduction on cached prompts (via OpenAI) is unbeatable.
- **CMUX Strategy:** Best for "headless" operation where a parent script drives Codex instances in different CMUX panes.

### **Rank 3: Pi (Pixel Inc)**
- **Why:** Specifically for complex, multi-file refactoring. Its ability to decompose a task into 10+ sub-agents, each visible in its own CMUX pane, provides the best "visual debugging" of an agent's thought process.

### **Honest Assessment of Gaps**

The primary limitation in early 2026 remains **CMUX "awareness."** While agents can *execute* `cmux` commands, they do not yet natively "see" the terminal state (e.g., they don't know a pane is already open unless they query the `cmux tree`). Claude Code's advantage is its polished, highly-opinionated TUI; replacing it requires a more "manual" configuration of your CMUX environment to achieve the same level of seamlessness.

**Citations (from Gemini; flagged as potentially questionable):**

- [cmux: Native macOS Terminal for AI Agents](https://betterstack.com/community/guides/ai/cmux-terminal/)
- [OpenCode: Revolutionizing Terminal Agents](https://webkul.com/blog/opencode-terminal-coding-agent/)
- [Agent Skills Specification (skills.sh)](https://docs.railway.com/ai/agent-skills) — *Note: this URL looks suspect; railway.com is an unrelated hosting service*
- [Aider vs OpenCode vs Claude Code: 2026 CLI Showdown](https://sanj.dev/post/comparing-ai-cli-coding-assistants)
- [T3 Code: Managing AI Coding Swarms](https://betterstack.com/community/guides/ai/t3-code/) — *Possibly hallucinated*

---

## Follow-Up 1: Primary sources and whether "pi" is real

*Asked for canonical repo links, config file names, and OpenRouter setup locations for opencode, pi, and Crush; also asked whether pi actually ships.*

### 1. OpenCode (by Anomaly/SST) — *Gemini-reported*

- **Canonical GitHub Repo (Gemini said):** `https://github.com/anomalyco/opencode` — ⚠️ **Subagent research contradicts this; the real repo is `github.com/sst/opencode`. Treat Gemini's attribution as possibly wrong.**
- **Official Landing/Docs:** https://opencode.ai
- **Config File:** `~/.opencode.json` (global) or `.opencode.json` (project-local)
- **Provider/OpenRouter Setup:** Documented in Core Concepts > Configuration; a `providers` block defines an `openrouter` entry with a custom `base_url`.
- **Unique feature:** built-in LSP support.

### 2. Pi (by Pixel Inc / Mario Zechner) — *Gemini-reported, plausible*

- **Status:** Real and shipping. Pi is a modular "agent stack" extendable via NPM.
- **Canonical GitHub Repo:** `https://github.com/badlogic/pi-mono` (specifically `packages/coding-agent`)
- **Official Landing:** https://pi.new (terminal-based landing page) and the Developer README
- **Config File:** `pi.config.ts` or `pi.config.json` in project root
- **Provider/OpenRouter Setup:** Uses `@mariozechner/pi-ai` package for LLM orchestration. OpenRouter is first-class; wiring keys is in the pi-ai Provider Guide.
- **Marketplace:** NPM under `@pi-package` keyword.

### 3. Crush (by Charm)

- **Canonical GitHub Repo:** `https://github.com/charmbracelet/crush`
- **Official Landing/Docs:** https://charm.sh/crush
- **Config File:** `$HOME/.config/crush/crush.json` (global) or `crush.json` (project-local)
- **Provider/OpenRouter Setup:** Crush uses the `land/fantasy` library for provider abstraction. Add OpenRouter by defining a provider with `type: "openai"` and the OpenRouter base URL. Detailed snippets in their `AGENTS.md`.
- **Unique feature:** sophisticated Charm TUI, includes "Yolo Mode" and styling.

### Summary Comparison Table (Gemini)

| Feature | OpenCode | Pi | Crush |
|---|---|---|---|
| Primary Language | TypeScript / Rust | TypeScript / Bun | Go |
| Config Format | JSON | TS / JSON | JSON |
| Provider Support | 75+ (Native) | 2000+ (via pi-ai) | — |
| Strength | Stability & LSP | Extreme Modularity | UI/UX & Speed |

**Gemini's recommendation:** "For a drop-in Claude Code replacement that 'just works' with OpenRouter today, OpenCode is the most viable. For custom multi-agent workflows spanning multiple CMUX panes, Pi is the superior architectural choice."

**⚠️ Verification note:** Gemini's `anomalyco/opencode` repo attribution is incorrect — real repo is `sst/opencode` (see subagent research). Treat Gemini content as low-confidence triangulation; lean on subagent findings for canonical facts.

---

## Follow-Up 2: Marketplace integration depth + per-sub-agent model routing

*Asked (per user concern): can different sub-agents use different models from the same marketplace? Can marketplaces and direct providers mix in one session? Is runtime model escalation supported? Where do the "75+" and "2000+" provider numbers come from? Do agents leverage OpenRouter's native features (auto-routing, provider preferences, fallback chains)?*

The landscape of CLI coding agents in early 2026 has moved toward **extreme provider heterogeneity**. While Claude Code remains vertically integrated with Anthropic, its primary competitors — **OpenCode**, **Pi**, and **Crush** — have optimized for "marketplace first" architectures.

### 1. Multi-Agent Model Routing

All three agents allow you to assign specific models to different "roles" within a single session, typically via sub-agent definitions.

**OpenCode (`opencode.json`):**

```json
{
  "model": "openrouter/anthropic/claude-3.7-sonnet",
  "agents": {
    "planner": {
      "model": "openrouter/openai/o4-preview",
      "description": "High-reasoning architect for complex planning",
      "prompt": "You are a system architect. Create a plan..."
    },
    "editor": {
      "model": "openrouter/qwen/qwen-2.5-72b-coder",
      "description": "Fast, high-context code writer",
      "prompt": "Execute the following edits precisely..."
    },
    "reviewer": {
      "model": "anthropic/claude-3-opus",
      "description": "Critical reviewer using a different reasoning engine",
      "prompt": "Find bugs in the proposed changes..."
    }
  }
}
```

Triggered via `@reviewer` or by the planner spawning them through the `spawn_subagent` tool. *(Source: `opencode-agents` Marketplace — per Gemini)*

**Pi (`pi.config.ts`)** — uniquely, the config is executable TypeScript, enabling logic-based routing:

```ts
import { defineConfig } from '@mariozechner/pi-ai';

export default defineConfig({
  agents: {
    coder: {
      // Use local Ollama for small files, OpenRouter for large ones
      model: (context) => context.fileCount > 5
        ? "openrouter/anthropic/claude-4.5-sonnet"
        : "ollama/qwen3-7b",
      skills: ["@pi-package/git-skill"]
    },
    architect: {
      model: "openrouter/google/gemini-3-pro"
    }
  }
});
```

### 2. Mixing Marketplaces and Direct Providers

All three agents support mixing. Anthropic's occasional OpenRouter restrictions in 2026 make keeping a direct API key as fallback important.

- **OpenCode:** `providers` block defines multiple provider configs; reference by prefix (`openrouter/` vs `anthropic/`).
- **Crush:** Environment variable precedence — `OPENROUTER_API_KEY` and `ANTHROPIC_API_KEY` both set, switch mid-session via `ctrl+p` model switcher.

### 3. Runtime Model Escalation

The concept of **"Auto-Escalation"** is the primary differentiator in 2026:

| Agent | Escalation Strategy | Detail |
|---|---|---|
| **OpenCode** | Task-Based | The Planner (cheap model) can call `@advanced` (a sub-agent on Opus/GPT-5) if it fails to resolve a bug after 3 attempts. |
| **Pi** | Per-Turn Routing | Uses the `pi-model-router` extension. It classifies the "intent" of every prompt. "List files" → Haiku; "Refactor Auth module" → reasoning model. |
| **Crush** | Manual/Explicit | Relies on the user switching models or agent suggesting a switch if response is "inconclusive." |

### 4. Provider Counts: The Matrix

- **OpenCode (75+ Native):** via the `models.dev` SDK. "First-class" drivers that understand provider-specific tool-use formats (XML for Anthropic, JSON for OpenAI) without middleware translation. *(Source: Morph Benchmarks 2026 — per Gemini)*
- **Pi (2000+ Models):** integration with full OpenRouter + Hugging Face Inference catalogs. ~300 are "verified" for coding; the agent can connect to any endpoint with a standard API. *(Source: `pi-mono` Issue #2179 — per Gemini)*

### 5. OpenRouter Feature Leverage

Most agents treat OpenRouter as a standard OpenAI-compatible endpoint. Two features are seeing native support:

- **`openrouter/auto`:** Both Pi and OpenCode support passing "auto" as the model ID — hands routing logic to OpenRouter's internal engine (latency/cost optimization).
- **Provider Preferences:** Crush added a `provider_order` key in `crush.json` passed in OpenRouter headers — ensures the agent uses "DeepInfra" or "Together" for Llama-3 models to save cost.

**Crush header-aware config example:**

```json
{
  "openrouter": {
    "api_key": "sk-or-...",
    "headers": {
      "X-Title": "My-Coding-Agent",
      "HTTP-Referer": "https://github.com/charmbracelet/crush"
    }
  }
}
```

### Final Recommendation (Gemini) for per-agent routing

> If you want the most robust sub-agent isolation, go with OpenCode. Its ability to run a Reviewer and a Coder on two different providers (e.g., one on direct Anthropic for reliability and one on OpenRouter for cost) is the closest thing to a "Production-Grade" agent setup available today.

**Primary Sources (Gemini-cited, verify against subagent research):**
- OpenCode Configuration Docs (opencode.ai/docs/providers/)
- pi-model-router GitHub
- Charm Crush: AGENTS.md

---

## Follow-Up 3: Feature parity gaps — MCP, hooks, plan mode, skills spec, ecosystem

*Asked: MCP client/server roles and transports, hook event lists and blocking behavior, true Plan Mode equivalents, whether SKILL.md is actually standardized, and ecosystem maturity.*

### 1. Model Context Protocol (MCP) Maturity

| Agent | MCP Role | Supported Transports | Maturity & Practical Difference |
|---|---|---|---|
| **Claude Code** | Client | `stdio` (Primary), `sse` | Gold Standard. Highly stable, strictly local. Best-in-class tool discovery. |
| **OpenCode** | Client | `stdio`, `http`, `sse` | Enterprise-Ready. Supports remote HTTP MCP servers out-of-the-box — shared team infrastructure (central DB explorer, etc.). |
| **Crush** | Client | `stdio`, `http`, `sse` | Native & fast. Integrated directly into Go core. Best for cross-platform (WSL/Android) where `stdio` can be flaky. |
| **Pi** | Client | `stdio` | Minimalist. Relies on a wrapper; MCP tools must be manually registered in `pi.config.ts`. |

**None of these CLI agents natively act as MCP servers.** They are MCP Hosts. If you need an agent to expose itself as an MCP server to another tool, use a bridge like `agent-mcp-proxy`.

### 2. Hooks & Lifecycle Events

- **Claude Code:** 26+ events. `PreToolUse` (blocking), `PostToolUse`, `UserPromptSubmit`, `SubagentStart/Stop`, `CwdChanged`, `InstructionsLoaded`, etc.
- **OpenCode:** Mirrors Claude's list almost 1:1. `PreToolUse` is blocking — the hook script can return `{"permissionDecision": "deny"}` to halt destructive ops.
- **Crush:** Streamlined. `PreToolUse` (blocking via exit code 2), `PostToolUse`, `Notification`, `Stop`. Uses shell exit codes for control logic.
- **Pi:** Does NOT use "hooks" in the event-listener sense. Uses **TypeScript Extensions** that wrap the agent's internal methods (AOP style) — more powerful but requires writing TS code.

### 3. Plan Mode: Read-Only vs. Agentic

- **Claude Code:** Dedicated, hard-coded "Plan Mode" where write tools are disabled.
- **OpenCode:** "Best implementation." `Tab` toggles between Build and Plan agents. Plan agent is a distinct sub-agent with `tools.write: false`. Native TUI indicator.
- **Crush:** No hard Plan Mode button yet (GitHub Issue #1734). Relies on "Non-Yolo Mode" — every tool call requires `y/n` confirmation, effectively forcing plan-and-approve.
- **Pi:** Explicitly **omits** Plan Mode. Philosophy: "conversational steering" — you tell the agent "don't write anything, just analyze."

### 4. Agent Skills Specification (`SKILL.md`)

Gemini claims: `SKILL.md` was published by Anthropic in December 2025, now governed at `agentskills.io`.
- **Standardization:** Cross-platform standard. A skill is a folder containing `SKILL.md` (YAML frontmatter + Markdown) and optional `/scripts`.
- **Registry:** `skills.sh` is a Vercel-hosted registry + CLI.
- **Portability:** `npx skills i vercel/react-best-practices` detects installed agent (Claude Code / OpenCode / Crush) and places files in the correct `.agent/skills` directory.

*⚠️ Verify: earlier Gemini citations for skills.sh pointed at docs.railway.com which was clearly wrong. Treat "skills.sh / agentskills.io" claim as needing primary-source verification.*

### 5. Ecosystem & Maturity

| Feature | Claude Code | OpenCode (SST) | Pi (Pixel Inc) | Crush (Charm) |
|---|---|---|---|---|
| Marketplace Size | 2,000+ Skills | 500+ Plugins/Agents | 100+ NPM Packages | 200+ Go-based Tools |
| GitHub Stars | Proprietary | 147,000+ | 12,000+ | 8,000+ |
| Community | Massive (Discord) | High (SST Discord) | Niche/Expert (X/OSS) | High (Charm Discord) |
| Backing | Anthropic ($B) | SST (Venture-backed) | Independent/Pixel Inc | Charm.sh (Venture-backed) |

**Gemini's assessment:** OpenCode is the most viable drop-in replacement today — adopts Claude-style UX while removing the Anthropic-only restriction. Crush is for users who want the most beautiful TUI and Go-native speed. Pi is for power-users who want to build their own agent from scratch on a minimalist base.

**Citations (Gemini-cited; verify):**
- Claude Code Hooks Reference
- OpenCode: Plan Mode vs Build Mode
- Agent Skills Open Standard
- Vercel's skills.sh Registry Launch
- Charm Crush: MCP & Lifecycle Docs
