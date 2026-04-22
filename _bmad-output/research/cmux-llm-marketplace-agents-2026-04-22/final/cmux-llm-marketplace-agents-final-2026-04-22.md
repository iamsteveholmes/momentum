---
title: "CMUX-integrated coding agents with LLM marketplace support as Claude Code replacements — Research Report"
date: 2026-04-22
type: Technical Research — Consolidated Report
status: Complete
profile: light
content_origin: claude-code-synthesis
human_verified: false
derives_from:
  - path: raw/research-candidate-enumeration.md
    relationship: synthesized_from
  - path: raw/research-llm-marketplace-support.md
    relationship: synthesized_from
  - path: raw/research-feature-parity.md
    relationship: synthesized_from
  - path: raw/gemini-deep-research-output.md
    relationship: synthesized_from
---

# CMUX-integrated coding agents with LLM marketplace support as Claude Code replacements

## TL;DR

**opencode (SST) is the strongest Claude Code replacement for a CMUX + OpenRouter practice**, with OpenAI Codex CLI and pi as the most credible runners-up. The key insight is that **cmux is explicitly agent-agnostic** — no CLI coding agent ships native pane orchestration, so "CMUX integration" reduces to how cleanly each agent's hook / custom-tool / subagent surface can invoke the `cmux` CLI. On per-sub-agent marketplace routing — the user's primary concern — **only opencode, Roo Code, pi, and Continue treat per-agent/per-role model selection as a first-class config field**, and opencode is the sole agent that combines that with 75+ providers, blocking lifecycle hooks, and SKILL.md portability. Gemini's triangulation broadly agrees but mis-attributes the opencode repository (it is `sst/opencode`, not `anomalyco/opencode`) and over-claims on several specific features — favor the subagent evidence when the two disagree.

## 1. What "CMUX integration" actually means

Per the cmux product page, cmux is explicitly agent-agnostic: "cmux works with any agent that runs in a terminal, including Claude Code, Codex, OpenCode, Gemini CLI, Kiro, Aider, Goose, Amp, Cline, Cursor Agent, and anything else you can launch from the command line" ([cmux.com](https://cmux.com/)) [OFFICIAL].

The practical consequence: **no CLI coding agent in this enumeration ships native cmux-CLI orchestration**. Every agent can drive cmux the same basic way — by shelling out to `cmux new-split`, `cmux send`, `cmux browser open`, `cmux capture-pane`. The real differentiator is the agent's extensibility surface — how cleanly that shell-out can be wrapped into reusable, declarative primitives. That narrows to five axes:

- **Hooks** — can lifecycle events (PreToolUse, PostToolUse, session.created) fire cmux commands automatically?
- **Custom tools** — can we expose `cmux_browser_open` as a first-class tool to the model rather than asking it to author bash every time?
- **Sub-agents** — is there a native "spawn specialist in a new context" primitive we can wire to "spawn specialist in a new cmux pane"?
- **SKILL.md / slash commands** — portable, versioned practice knowledge attached to invocation points.
- **MCP** — standardized external-tool exposure.

On these axes, the field is not flat.

## 2. The shortlist (ranked)

### 1. opencode (SST) — top pick

- **What**: Open-source (MIT) TypeScript/Bun TUI agent. Repo: `github.com/sst/opencode`. Docs: `opencode.ai/docs`.
- **Why shortlisted**: Widest provider coverage (75+ via Vercel AI SDK + models.dev), broadest hooks surface in the ecosystem (28 lifecycle events vs. Codex's 6 vs. Claude Code's ~5), first-class per-agent model field, built-in Plan vs Build modes, and SKILL.md portability that reads both `.opencode/skills/` and Anthropic-compatible `.claude/skills/` paths ([opencode docs — Agents](https://opencode.ai/docs/agents/), [opencode docs — Hooks via plugins](https://opencode.ai/docs/plugins/)) [OFFICIAL]. An `awesome-opencode` index and "Superpowers for OpenCode" community project exist ([Superpowers for OpenCode — fsck.com blog](https://blog.fsck.com/2025/11/24/Superpowers-for-OpenCode/)) [PRAC].

### 2. OpenAI Codex CLI — strong runner-up

- **What**: Open-source (Apache-2.0). Repo: `github.com/openai/codex`.
- **Why shortlisted**: Near-full Claude Code parity on subagents (`[agents]` in `config.toml`), SKILL.md-based Agent Skills (replacing deprecated custom prompts), `/plan` mode, MCP client **and server** (unusual — Codex can expose itself as an MCP server), and blocking PreToolUse hooks ([Codex CLI Features](https://developers.openai.com/codex/cli/features), [Codex Hooks docs](https://developers.openai.com/codex/hooks)) [OFFICIAL]. Weaker marketplace story than opencode: OpenAI-first, with OpenRouter supported via the generic `[model_providers.*]` table rather than first-class ([OpenRouter Codex CLI integration](https://openrouter.ai/docs/guides/coding-agents/codex-cli)) [OFFICIAL]. Hooks currently only fire on Bash tools.

### 3. pi / pi-coding-agent (Mario Zechner)

- **What**: Open-source TypeScript "minimal core + extensions" harness. Repo: `github.com/badlogic/pi-mono`, npm: `@mariozechner/pi-coding-agent`.
- **Why shortlisted**: Subagents-with-own-LLM as a first-class primitive; provider list covers Anthropic, OpenAI, Google, Azure, Bedrock, Mistral, Groq, Cerebras, xAI, Hugging Face, Kimi, MiniMax, OpenRouter, Ollama via `~/.pi/agent/models.json` ([pi-mono providers.md](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/providers.md)) [OFFICIAL]. Philosophy is "build what you need as pi packages" — perfect shape for a custom cmux-orchestrator package. pi **explicitly omits plan mode** in favor of conversational steering ([Pi: The Minimal Agent — Armin Ronacher](https://lucumr.pocoo.org/2026/1/31/pi/)) [PRAC].

### Runners-up (not top-3 but worth naming)

- **Gemini CLI** — Cleanest extension-packaging model (skills + agents + hooks + MCP + commands in one installable), but Gemini-only on the provider side; community OpenRouter forks exist but are unverified ([Gemini CLI Extensions](https://geminicli.com/docs/extensions/)) [OFFICIAL].
- **Charm Crush** — Polished TUI, typed providers (`openai` / `openai-compat` / `anthropic`), MCP — but no documented sub-agents, custom slash commands, hooks, or plan mode as of April 2026 ([charmbracelet/crush](https://github.com/charmbracelet/crush), [Crush Issue #2219 — slash commands](https://github.com/charmbracelet/crush/issues/2219)) [OFFICIAL].
- **Continue CLI (`cn`)** — Good role-based routing via `roles:` array and native multi-provider SDKs; weaker agent/hook story ([Continue CLI Overview](https://docs.continue.dev/cli/overview)) [OFFICIAL].

**Excluded**: Amp (enterprise-gated in 2026; model selection is not user-configurable), Gemini CLI from the top-3 (single-vendor lock-in), Cline/Roo Code (VS Code–first, not CLI-native enough), Aider (no sub-agents, no hooks, no MCP), OpenHands (Docker sandbox breaks host-level cmux invocation by default).

## 3. Dimension 1 — LLM marketplace support and per-sub-agent routing

This is the user's primary concern: **can I run planner on Claude Sonnet via OpenRouter, editor on Qwen-Coder via OpenRouter, and reviewer on GPT-5 via OpenRouter — in the same session?**

### The landscape

| Agent | OpenRouter | OpenAI-Compat | Per-Sub-Agent Model | Mix Marketplace + Direct | Runtime Escalation |
|---|---|---|---|---|---|
| **opencode** | First-class via models.dev registry | Yes (`@ai-sdk/openai-compatible`, any npm AI SDK pkg) | **Yes — `model` field per agent in opencode.json or agent markdown frontmatter** | Yes (prefix-based: `openrouter/...` vs `anthropic/...`) | Task-based delegation to higher-capability subagent |
| **Codex CLI** | Via `[model_providers.*]` recipe | Yes | Limited — global `model` + `model_reasoning_effort`; no true sub-agent model split | Yes via multiple `[model_providers.*]` blocks | No built-in; manual via `/model` |
| **Crush** | Env var + `providers.openrouter` block | Yes (`"type": "openai-compat"`) | **No** — session-level `/model` picker only | Yes | Manual |
| **pi** | `OPENROUTER_API_KEY` + `/model` picker | Yes via `~/.pi/agent/models.json` | **Yes — subagents run in own context, optionally with own LLM** | Yes (credential resolution: CLI → auth.json → env → models.json) | Extension-mediated (`pi-model-router` is community) |
| **Continue** | First-class `provider: openrouter` | Yes (`provider: openai` + `apiBase`) | **Yes — `roles:` array assigns models to chat/edit/apply/summarize/embed/rerank** | Yes | No |
| **Aider** | `--model openrouter/...` | Yes via LiteLLM | Role-split: `--model` / `--editor-model` / `--weak-model` | Yes | No |
| **Roo Code** (VS Code) | First-class UI | Yes | **Yes — Configuration Profiles per mode (Code/Architect/Ask/Debug/Orchestrator)** | Yes | Per-mode switch |
| **Cline** (VS Code) | First-class UI | Yes | Plan/Act mode split only | Yes | Mode-switch |
| **Gemini CLI** | ❌ (community forks only) | Limited | No | No | No |
| **Amp** | ❌ | ❌ | Amp picks per-mode, user cannot override | No | Automatic |

### Concrete per-sub-agent routing — opencode

The canonical pattern. One `opencode.json` wires three agents to three different OpenRouter models plus a direct Anthropic fallback for the reviewer ([opencode Providers docs](https://opencode.ai/docs/providers/), [opencode Agents docs](https://opencode.ai/docs/agents/)) [OFFICIAL]:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "openrouter": {
      "models": {
        "moonshotai/kimi-k2": {
          "options": {
            "provider": { "order": ["baseten"], "allow_fallbacks": false }
          }
        }
      }
    }
  },
  "agent": {
    "plan": {
      "mode": "primary",
      "model": "openrouter/anthropic/claude-sonnet-4"
    },
    "build": {
      "mode": "primary",
      "model": "openrouter/qwen/qwen-2.5-coder-32b-instruct"
    },
    "code-reviewer": {
      "mode": "subagent",
      "model": "anthropic/claude-opus-4-20250514"
    }
  }
}
```

Per-agent markdown is equivalent and version-controllable:

```markdown
---
description: Reviews code for quality and best practices
mode: subagent
model: openrouter/openai/gpt-5
---
You are a code reviewer focused on identifying potential issues.
```

Subagents without an explicit `model` inherit from the invoking primary ([opencode Agents docs](https://opencode.ai/docs/agents/)) [OFFICIAL]. This inheritance-with-override shape is exactly what a Momentum-style practice wants: defaults at the agent definition, overrides per invocation when needed.

### Concrete per-sub-agent routing — pi

pi's differentiator is that `pi.config.ts` is **executable TypeScript**, enabling conditional routing ([Gemini FU2 — illustrative example](https://lucumr.pocoo.org/2026/1/31/pi/)) [UNVERIFIED — exact schema per Gemini; treat as pattern sketch]:

```ts
import { defineConfig } from '@mariozechner/pi-ai';

export default defineConfig({
  agents: {
    coder: {
      // Local Ollama for small changes, OpenRouter for large refactors
      model: (context) => context.fileCount > 5
        ? "openrouter/anthropic/claude-sonnet-4"
        : "ollama/qwen2.5-coder-7b",
      skills: ["@pi-package/git-skill"]
    },
    architect: { model: "openrouter/google/gemini-2.5-pro" }
  }
});
```

The subagent research confirms pi supports "subagents that run in their own context window, possibly with a different LLM" and that explicit per-invocation routing works via `pi --provider openai --model gpt-4o "Help me refactor"` ([pi-mono coding-agent README](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/README.md)) [OFFICIAL]. Gemini's `pi.config.ts` conditional-model-function syntax is illustrative and should be checked against the current pi API before relying on it.

### OpenRouter-native feature leverage

- **`openrouter/auto`** — Gemini claims both opencode and pi support passing `"auto"` to hand routing to OpenRouter's internal engine [UNVERIFIED — Gemini claim, not in subagent evidence]. Opencode documentation does confirm OpenRouter provider-routing options (`order`, `allow_fallbacks`) are passed through ([opencode Providers docs](https://opencode.ai/docs/providers/)) [OFFICIAL], which is the verified case.
- **`provider_order` pinning** — opencode's config supports this directly via the `options.provider.order` block shown above. Aider supports the same via `.aider.model.settings.yml` `extra_body.provider.order` ([Aider OpenRouter docs](https://aider.chat/docs/llms/openrouter.html)) [OFFICIAL].
- **HTTP-Referer / X-Title headers** — Crush's `headers` object lets you tag requests for OpenRouter attribution/quota separation [PRAC].

### Mixing marketplaces and direct providers

All three top picks handle this cleanly. opencode distinguishes by model prefix (`openrouter/...` vs `anthropic/...`), each resolved by a separate `provider.*` block. Codex CLI selects via `model_provider = "openrouter"` vs `model_provider = "anthropic"`. pi uses credential-resolution order: CLI `--api-key` → `auth.json` → env var → `models.json` entry ([pi-mono providers.md](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/providers.md)) [OFFICIAL].

This matters because **Anthropic blocked third-party Claude auth in January 2026** ([Every AI Coding CLI in 2026 — DEV](https://dev.to/soulentheo/every-ai-coding-cli-in-2026-the-complete-map-30-tools-compared-4gob)) [PRAC]. Direct Anthropic API keys still work, but OAuth-via-Claude-subscription into opencode is blocked. Keeping a direct Anthropic key as a fallback provider alongside OpenRouter is the pragmatic pattern.

### Runtime escalation

- **opencode** — Task-based: a cheap planner agent can invoke a more expensive subagent when it hits complexity; subagent definitions gate this with `allow` / `ask` / `deny` glob patterns in the Task tool permission list ([opencode Agents docs](https://opencode.ai/docs/agents/)) [OFFICIAL].
- **pi** — Per-turn routing via the community `pi-model-router` extension [UNVERIFIED — Gemini claim; verify against the pi extensions index before building on this].
- **Codex CLI / Crush** — Manual only; user issues `/model` mid-session.

### Ranking on marketplace flexibility

1. **opencode** — per-agent models, 75+ providers, npm-pluggable backends, explicit OpenRouter provider routing.
2. **pi** — multi-provider `models.json` + subagents-with-own-LLM + extensions for custom auth flows (example: `custom-provider-gitlab-duo`).
3. **Continue** — clean `roles:` array, native multi-provider SDKs.
4. **Aider** — architect/editor/weak split, LiteLLM-backed.
5. **Codex CLI** — solid custom-provider recipe, weak per-agent.
6. **Crush** — typed providers, no per-agent.
7+. Gemini CLI, Amp — disqualified.

## 4. Dimension 2 — CMUX integration depth

All three shortlist candidates score "None native, shell-wireable" on cmux orchestration. The differentiator is how they wrap that shell-out.

### opencode

- **Hook surface**: 28 lifecycle events. Most relevant for cmux: `tool.execute.before` (blocking — can intercept and swap in a cmux-aware version of the tool), `tool.execute.after`, `session.created` (set up pane layout), `session.compacted`, `message.part.updated`, `permission.asked` ([opencode Plugin Development Guide — Lushbinary](https://lushbinary.com/blog/opencode-plugin-development-custom-tools-hooks-guide/)) [PRAC]. A plugin is a TypeScript file in a plugin dir or an npm package referenced in config.
- **Custom tools**: First-class. A plugin can register a `cmux_browser_open` tool the model invokes directly, rather than asking it to author `bash("cmux browser open ...")`.
- **Subagents**: Native primary + subagent model. Each subagent runs in its own context window — natural fit for "primary in pane A, subagent in pane B".
- **Wiring pattern**: Register a plugin with `session.created` → `cmux new-split right` + `cmux rename-tab`, and `tool.execute.after` (on `task` tool) → spawn new pane for the subagent context. All in a single TS plugin.

### Codex CLI

- **Hook surface**: 6 events — SessionStart, PreToolUse (blocking; Bash-only scope currently), PermissionRequest, PostToolUse, UserPromptSubmit, Stop ([Codex Hooks docs](https://developers.openai.com/codex/hooks)) [OFFICIAL]. JSON-over-stdin schema with `session_id`, `cwd`, `hook_event_name`, `model`.
- **Custom tools**: Via MCP only; Codex can also run **as** an MCP server, enabling orchestrator-of-orchestrators patterns.
- **Subagents**: Configured in `[agents]` in `~/.codex/config.toml`. Must be explicitly invoked — no auto-delegation by default.
- **Wiring pattern**: `SessionStart` hook invokes `cmux identify` + `cmux new-split`. `PreToolUse` Bash hook can prepend `cmux send` redirection to log streams to a visible pane. Narrower surface than opencode; still workable.

### pi

- **Hook surface**: pi uses **TypeScript extensions** that wrap internal methods (AOP style) rather than an event-listener hook model ([Gemini FU3](https://lucumr.pocoo.org/2026/1/31/pi/)) [PRAC]. More powerful for arbitrary wiring, but requires writing TS.
- **Custom tools**: A pi package is the canonical extensibility primitive. A `@steve/pi-cmux` package could expose cmux primitives as tools.
- **Subagents**: Native, with own LLM. Conceptually clean fit for "pane-per-subagent".
- **Wiring pattern**: Write a pi extension that exposes `cmux_new_split`, `cmux_send`, etc. as pi tools; optionally wrap the subagent-spawn method to automatically allocate a cmux pane. Higher up-front cost than opencode's config-driven plugin, lower than writing this from scratch.

### The overall CMUX verdict

| Agent | Hook surface | Custom tools | Subagents | Wiring cost |
|---|---|---|---|---|
| **opencode** | 28 events | Plugin-registered | Native, per-model | **Low** — one TS plugin |
| **Codex CLI** | 6 events (Bash PreToolUse only) | MCP only | Config-declared | Medium — MCP server or hook scripts |
| **pi** | TS-extension AOP | Package-defined | Native, per-LLM | Medium-high — write a pi package |

**opencode's 28-event hook surface is the single clearest practical win** for Momentum-style CMUX orchestration: you can wire `cmux new-split` into `session.created`, pipe `cmux send` echoes into `message.part.updated` for visibility, intercept destructive bash at `tool.execute.before`, and spawn subagent panes from `todo.updated`.

## 5. Dimension 3 — Feature parity vs Claude Code

| Axis | Claude Code | opencode | Codex CLI | pi | Gemini CLI | Crush | Continue |
|---|---|---|---|---|---|---|---|
| Sub-agents | ✅ `.claude/agents/*.md` | ✅ per-agent model | ✅ `[agents]` config | ✅ own-LLM subagents | ✅ via extensions | ❌ | ↗ agents in config |
| Slash cmds / Skills | ✅ SKILL.md + slash | ✅ SKILL.md (reads `.claude/skills/` too) | ✅ SKILL.md replacing /prompts | ↗ extension-driven | ✅ bundled in extensions | ↗ SKILL.md | ✅ slash + MCP prompts |
| Hooks | ✅ ~5 events, blocking | ✅ 28 events, blocking | ✅ 6 events, blocking (Bash-only) | ↗ TS AOP extensions | ✅ via extensions | ❌ | ❌ |
| MCP | ✅ stdio/http/sse | ✅ stdio/http/sse | ✅ stdio/http + can run as server | ✅ stdio | ✅ stdio/http | ✅ stdio/http/sse + Docker | ✅ stdio/http |
| Plan mode | ✅ read-only filter | ✅ Plan vs Build (own model) | ✅ `/plan` | ❌ (philosophy: conversational) | 🟡 not first-class | ❌ | ❌ |
| Tool use | ✅ built-ins + MCP | ✅ built-ins + MCP + plugin tools | ✅ built-ins + MCP + namespacing | ✅ 4 built-ins (read/write/edit/bash) | ✅ built-ins + MCP | ✅ built-ins + MCP + LSP | ✅ built-ins + MCP |
| Ecosystem | ✅ `/plugin` marketplaces, closed harness | ✅ npm plugins, awesome-opencode, 116k+ stars | 🟡 OpenAI-first, growing | 🟡 NPM @pi-package keyword | ✅ Extension Gallery | 🟡 newer TUI polish | ✅ config.yaml |

Legend: ✅ full parity · 🟡 partial · ❌ none · ↗ different model

**Key cross-cutting observations**:

1. **SKILL.md is becoming a de facto standard** — Claude Code, opencode, Codex CLI, Crush, Cursor, Gemini CLI, OpenHands, and Amp all support some variant ([Claude Code Extensions guide — Morph](https://www.morphllm.com/claude-code-extensions)) [PRAC]. Gemini claims Vercel runs a `skills.sh` / `agentskills.io` registry that cross-installs skills — this is **unverified** and Gemini's earlier citation pointed at an unrelated `docs.railway.com` URL. Treat as a claim needing primary-source verification.
2. **AGENTS.md has replaced CLAUDE.md** for most agents — Codex, Cursor, Amp, OpenHands, opencode all read `AGENTS.md`; some (Cursor, opencode) read both.
3. **Plan mode is inconsistent**. Claude Code and opencode treat it as a first-class mode with enforced tool filtering. Codex and Amp treat it as a slash command / deep-mode toggle. Gemini, Cursor, Continue, Crush, pi, OpenHands, Aider don't have a read-only-enforced-by-harness equivalent.

## 6. Current limitations and gaps

- **CMUX awareness is still one-way**. Agents can *execute* `cmux` commands but cannot natively *read* pane state (e.g., "is pane 3 busy?") unless they query it via `cmux capture-pane` / `cmux list-panels`. This is a general limitation of cmux-as-control-plane, not an agent deficiency. Claude Code's polished, highly-opinionated TUI mitigates it; any replacement requires more explicit cmux querying in hooks/prompts.
- **Anthropic's January 2026 third-party auth block** means opencode cannot use a Claude subscription OAuth; direct Anthropic API keys still work, and OpenRouter remains a viable path ([Every AI Coding CLI in 2026](https://dev.to/soulentheo/every-ai-coding-cli-in-2026-the-complete-map-30-tools-compared-4gob)) [PRAC]. This drove an 18k-star surge for opencode in early 2026 as users migrated.
- **SKILL.md portability** is strong in practice for the format itself (YAML frontmatter + markdown body), but **tool-dependent behaviors embedded in skills may not transfer** — a skill that assumes `PreToolUse` hook semantics from Claude Code will behave differently on Codex's Bash-only hook scope.
- **Gemini's claims to verify before relying on**: `openrouter/auto` native support in opencode/pi; `pi-model-router` extension existence and API; the `skills.sh` / `agentskills.io` registry; the "T3 Code" project (subagent research does not find this; likely hallucinated). Gemini's `anomalyco/opencode` repo attribution is confirmed wrong — real repo is `sst/opencode`.

## 7. Recommendation

For a solo-dev practice that wants Claude Code replacement, OpenRouter access, per-sub-agent model routing, and CMUX orchestration, the decision is:

### Primary: **opencode (SST)**

The only agent that combines all three requirements natively. One `opencode.json` gives you `planner: claude-sonnet via openrouter`, `builder: qwen-coder via openrouter`, `reviewer: gpt-5 via openrouter`, and an `anthropic` fallback block — plus SKILL.md portability from `.claude/skills/`, 28 lifecycle hooks for wiring `cmux new-split` on session start, and a Plan vs Build mode with separate models. The Momentum ruleset ports largely intact because opencode reads Anthropic-compatible paths.

**Primary risk**: Anthropic's January 2026 third-party auth block — keep a direct Anthropic API key, or route Claude via OpenRouter instead of OAuth.

### Secondary: **OpenAI Codex CLI**

Pick this if OpenAI is your primary model provider and you value the MCP-server-role Codex uniquely offers. Per-agent routing is weaker (global `model` + reasoning effort), but subagents exist, SKILL.md is supported, and the 6-event hook surface is sufficient for most cmux wiring (SessionStart for layout, PreToolUse-Bash for destructive guards). Weaker marketplace story means less value for a multi-provider practice.

### Tertiary: **pi / pi-coding-agent**

Pick this if you want to build the practice from first principles as pi packages. Higher upfront cost (write a `@steve/pi-cmux` package) but pure — a pi extension is the canonical extensibility primitive, subagents support own-LLM natively, and the provider list is broad. No plan mode by design. Best fit if the Momentum practice evolves toward "assemble from small, sharp tools".

**Do not pick**: Gemini CLI (no OpenRouter without community forks), Amp (no BYO LLM by design, enterprise-gated), Cline or Roo Code (VS Code–first; weaker as CLI-native replacements), Aider (no sub-agents, no hooks, no MCP — feature gap is too large), OpenHands (Docker sandbox breaks host cmux invocation by default).

## 8. Sources

### Official primary sources

- [cmux.com](https://cmux.com/) [OFFICIAL]
- [opencode.ai docs — index](https://opencode.ai/docs/) [OFFICIAL]
- [opencode — Providers](https://opencode.ai/docs/providers/) [OFFICIAL]
- [opencode — Agents](https://opencode.ai/docs/agents/) [OFFICIAL]
- [opencode — Plugins / Hooks](https://opencode.ai/docs/plugins/) [OFFICIAL]
- [opencode — Modes](https://opencode.ai/docs/modes/) [OFFICIAL]
- [opencode — Agent Skills](https://opencode.ai/docs/skills/) [OFFICIAL]
- [opencode — MCP servers](https://opencode.ai/docs/mcp-servers/) [OFFICIAL]
- [OpenAI Codex CLI — Features](https://developers.openai.com/codex/cli/features) [OFFICIAL]
- [OpenAI Codex CLI — Hooks](https://developers.openai.com/codex/hooks) [OFFICIAL]
- [OpenAI Codex CLI — config-advanced](https://developers.openai.com/codex/config-advanced) [OFFICIAL]
- [OpenAI Codex CLI — MCP](https://developers.openai.com/codex/mcp) [OFFICIAL]
- [OpenRouter — Codex CLI integration](https://openrouter.ai/docs/guides/coding-agents/codex-cli) [OFFICIAL]
- [pi-mono coding-agent README](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/README.md) [OFFICIAL]
- [pi-mono providers.md](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/providers.md) [OFFICIAL]
- [charmbracelet/crush](https://github.com/charmbracelet/crush) [OFFICIAL]
- [Crush Issue #2219 — slash commands](https://github.com/charmbracelet/crush/issues/2219) [OFFICIAL]
- [Gemini CLI — Extensions](https://geminicli.com/docs/extensions/) [OFFICIAL]
- [Gemini CLI Add-OpenAI-backend Issue #1605](https://github.com/google-gemini/gemini-cli/issues/1605) [OFFICIAL]
- [Continue CLI Overview](https://docs.continue.dev/cli/overview) [OFFICIAL]
- [Continue — Model Roles](https://docs.continue.dev/customize/model-roles/intro) [OFFICIAL]
- [Aider OpenRouter docs](https://aider.chat/docs/llms/openrouter.html) [OFFICIAL]
- [Cline CLI Getting Started](https://docs.cline.bot/cline-cli/getting-started) [OFFICIAL]
- [Roo Code OpenRouter docs](https://docs.roocode.com/providers/openrouter) [OFFICIAL]
- [Amp Owner's Manual](https://ampcode.com/manual) [OFFICIAL]
- [LiteLLM OpenRouter provider docs](https://docs.litellm.ai/docs/providers/openrouter) [OFFICIAL]

### Practitioner / secondary sources

- [OpenCode Plugin Development — Lushbinary](https://lushbinary.com/blog/opencode-plugin-development-custom-tools-hooks-guide/) [PRAC]
- [Superpowers for OpenCode — fsck.com](https://blog.fsck.com/2025/11/24/Superpowers-for-OpenCode/) [PRAC]
- [Pi: The Minimal Agent — Armin Ronacher](https://lucumr.pocoo.org/2026/1/31/pi/) [PRAC]
- [Every AI Coding CLI in 2026 — DEV Community](https://dev.to/soulentheo/every-ai-coding-cli-in-2026-the-complete-map-30-tools-compared-4gob) [PRAC]
- [Claude Code Extensions Guide 2026 — Morph](https://www.morphllm.com/claude-code-extensions) [PRAC]
- [OpenCode's January surge — 18,000 new stars](https://medium.com/@milesk_33/opencodes-january-surge-what-sparked-18-000-new-github-stars-in-two-weeks-7d904cd26844) [PRAC]
- [2026 Guide to Coding CLI Tools — Tembo](https://www.tembo.io/blog/coding-cli-tools-comparison) [PRAC]
- [cmux Guide — Better Stack](https://betterstack.com/community/guides/ai/cmux-terminal/) [PRAC]

### Gemini-cited (flagged as [UNVERIFIED] unless also in subagent evidence)

- `anomalyco/opencode` repo attribution — **confirmed wrong**, real repo is `sst/opencode`.
- `skills.sh` / `agentskills.io` / Vercel skills registry — earlier Gemini citation pointed at `docs.railway.com` (unrelated). Treat as unverified.
- "T3 Code" project — not found in subagent research; likely hallucinated.
- `pi-model-router` extension — plausible but unverified; check pi extensions index.
- `openrouter/auto` native support in opencode/pi — pattern plausible, specific native-support claim unverified.
- Specific GitHub star counts (opencode "147k+", "2000+ providers for pi") — approximate; subagent evidence cites opencode at 116k–146k depending on source and notes the count is contested.
