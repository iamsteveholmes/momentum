---
content_origin: claude-code-subagent
date: 2026-04-22
sub_question: "How do top CLI coding agents support LLM marketplaces (OpenRouter, OpenAI-compatible, custom providers)?"
topic: "CMUX-integrated coding agents with LLM marketplace support as Claude Code replacements"
---

# LLM Marketplace & Provider Flexibility Across CLI Coding Agents

A provider-flexibility audit of the top CLI coding agents under evaluation as Claude Code replacements. Each agent is scored on five dimensions: **OpenRouter first-class support**, **OpenAI-compatible endpoints**, **native multi-provider SDKs**, **per-task / per-agent routing**, and **custom bring-your-own-provider** extension points. Concrete config snippets are quoted from official docs whenever available.

## At-a-Glance Comparison

| Agent | OpenRouter | OpenAI-Compat | Native Multi-Provider | Per-Agent Model Routing | Custom BYO Provider | Config Surface |
|---|---|---|---|---|---|---|
| **opencode (SST)** | First-class (via models.dev registry + provider routing options) | Yes (`@ai-sdk/openai-compatible`) | 75+ via Vercel AI SDK | Yes — per-agent `model` field | Yes — add `provider.*` block pointing at any npm AI SDK package | `opencode.json` + agent markdown frontmatter |
| **OpenAI Codex CLI** | Documented recipe (set `model_provider`, `base_url`) | Yes (chat + responses wire APIs) | OpenAI-native primary; others via `[model_providers.*]` | Limited (global `model` + `model_reasoning_effort`) | Yes — `[model_providers.<id>]` with auth command, headers, retries | `~/.codex/config.toml` |
| **Charm Crush** | Env var `OPENROUTER_API_KEY` (first-class in provider list) | Yes (`"type": "openai-compat"`) | Anthropic/OpenAI/OpenAI-compat typed providers | No documented per-agent routing | Yes — any `providers.*` entry | `crush.json` / `.crush.json` |
| **OpenHands** | First-class UI option + custom-model fallback | Yes (via LiteLLM) | 100+ via LiteLLM | Agent-role split (main/condenser) | Yes via LiteLLM config | UI settings + LiteLLM env vars |
| **Aider** | First-class (`--model openrouter/...`) | Yes (via LiteLLM) | 100+ via LiteLLM | Weak/editor split (`--editor-model`, `--weak-model`) | Yes (LiteLLM env vars, YAML settings) | CLI flags, `.env`, `.aider.model.settings.yml` |
| **Cline** | First-class UI dropdown | Yes (OpenAI Compatible option) | Anthropic/OpenAI/Gemini/Bedrock/Vertex/Cerebras/Groq etc. | Plan/Act mode split (separate models per mode) | Yes (OpenAI-Compatible with base URL) | VS Code extension UI settings |
| **Roo Code** | First-class | Yes | Same as Cline + more | Yes — "Configuration Profiles" per mode | Yes | VS Code extension UI + profiles |
| **Continue** | First-class (provider: `openrouter`) | Yes (provider: `openai` with `apiBase`) | Native Anthropic/OpenAI/Google/Mistral/Azure/Ollama/LM Studio | Yes — `roles:` array per model | Yes | `config.yaml` |
| **Gemini CLI (Google)** | Not supported officially (community forks only) | Limited (LiteRT-LM only) | Google-only | No | No (requires source fork or LiteLLM proxy) | `~/.gemini/settings.json` |
| **Amp (Sourcegraph)** | No | No | Controlled centrally | No (automatic mode selection) | No | N/A — Amp picks model per mode |
| **pi (pi-mono)** | First-class (`OPENROUTER_API_KEY` + `/model`) | Yes via `~/.pi/agent/models.json` | Anthropic/OpenAI/Google/Azure/Bedrock/Mistral/Groq/Cerebras/xAI/HF/Kimi/MiniMax/OpenRouter/Ollama | Subagent support with its own context/LLM | Yes via `models.json` + custom extension | `~/.pi/agent/models.json` + CLI flags |

---

## opencode (SST)

opencode has the most developed marketplace story of any agent in this survey. It integrates the **Vercel AI SDK** plus the **models.dev registry** to expose 75+ providers out of the box and allows any NPM AI SDK package as a pluggable provider backend [OFFICIAL].

### OpenRouter

OpenRouter is preloaded. Users invoke `/connect` inside opencode and search for OpenRouter, with most OpenRouter models preloaded by default [OFFICIAL]. Routing hints are supported directly in config, using OpenRouter's provider-ordering semantics [OFFICIAL]:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "openrouter": {
      "models": {
        "moonshotai/kimi-k2": {
          "options": {
            "provider": {
              "order": ["baseten"],
              "allow_fallbacks": false
            }
          }
        }
      }
    }
  }
}
```

### OpenAI-Compatible / Custom Provider

Any OpenAI-style endpoint — LiteLLM proxy, Ollama, vLLM, Together, Groq, Fireworks, Anyscale, Cerebras, DeepInfra, llama.cpp — fits this shape [OFFICIAL]:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "myprovider": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "My AI Provider",
      "options": {
        "baseURL": "https://api.myprovider.com/v1",
        "apiKey": "{env:API_KEY}",
        "headers": {
          "Authorization": "Bearer custom-token"
        }
      },
      "models": {
        "model-id": {
          "name": "Display Name",
          "limit": { "context": 200000, "output": 65536 }
        }
      }
    }
  }
}
```

The `npm:` field is the killer extensibility point: any package conforming to the Vercel AI SDK provider interface can be slotted in without a source-tree modification [OFFICIAL].

### Per-Agent Model Routing

Per-agent model override is a first-class concept, either in `opencode.json` or in agent markdown frontmatter [OFFICIAL]:

```json
{
  "agent": {
    "build": { "model": "anthropic/claude-sonnet-4-20250514", "mode": "primary" },
    "plan":  { "model": "anthropic/claude-haiku-4-20250514",  "mode": "primary" },
    "code-reviewer": { "model": "anthropic/claude-sonnet-4-20250514", "mode": "subagent" }
  }
}
```

```markdown
---
description: Reviews code for quality and best practices
mode: subagent
model: anthropic/claude-sonnet-4-20250514
---
You are a code reviewer focused on identifying potential issues.
```

Defaults: if a subagent has no explicit model, it inherits from the invoking primary agent [OFFICIAL]. Dynamic per-invocation override from the Task tool is still an open feature request [UNVERIFIED — GH #6651, #11215].

### Verdict

opencode's provider layer is arguably the most flexible in the ecosystem. First-class OpenRouter, NPM-pluggable custom providers, per-agent models, and a public models.dev registry.

---

## OpenAI Codex CLI

Codex CLI ships with a generic `[model_providers.*]` table in `~/.codex/config.toml`, usable to point at OpenRouter, Azure OpenAI, LiteLLM, or any OpenAI-compatible gateway [OFFICIAL].

### OpenRouter

OpenRouter publishes an official Codex CLI integration recipe [OFFICIAL]:

```toml
model_provider = "openrouter"
model_reasoning_effort = "high"
model = "openai/gpt-5.3-codex"

[model_providers.openrouter]
name = "openrouter"
base_url = "https://openrouter.ai/api/v1"
env_key = "OPENROUTER_API_KEY"
```

### Generic Custom Provider

Arbitrary OpenAI-compatible gateways slot in via [OFFICIAL]:

```toml
model = "gpt-5.4"
model_provider = "proxy"

[model_providers.proxy]
name = "OpenAI using LLM proxy"
base_url = "https://proxy.example.com/v1"
wire_api = "responses"          # or "chat"
env_key = "OPENAI_API_KEY"
http_headers = { "X-Example-Header" = "example-value" }
env_http_headers = { "X-Example-Features" = "EXAMPLE_FEATURES" }
request_max_retries = 4
stream_max_retries = 10
```

Auth can be sourced from an external command (useful for short-lived tokens) [OFFICIAL]:

```toml
[model_providers.proxy.auth]
command = "/usr/local/bin/fetch-codex-token"
args = ["--audience", "codex"]
timeout_ms = 5000
refresh_interval_ms = 300000
```

Azure is a standard worked example including `query_params` for `api-version` and Responses API wire mode [OFFICIAL].

### Wire API Selection

`wire_api = "chat"` for Chat Completions endpoints (most third-party providers); `wire_api = "responses"` for OpenAI's newer Responses API [OFFICIAL]. Most third-party providers use `"chat"` [OFFICIAL].

### Per-Agent / Per-Task Routing

Codex CLI lacks a true per-agent sub-model concept. Routing levers are global: `model`, `model_provider`, `model_reasoning_effort` (`low`/`medium`/`high`/`xhigh`), `model_verbosity`, `model_context_window` [OFFICIAL]. No documented subagent-with-different-model primitive exists.

### Verdict

Strong custom-provider story, good enough for single-model Claude Code replacement, but weaker than opencode for multi-model orchestration.

---

## Charm Crush

Crush uses a typed provider model — `"openai"`, `"openai-compat"`, or `"anthropic"` — in `crush.json` [OFFICIAL].

### OpenRouter

Lightweight recipe [PRAC — Apiyi / Medium walkthroughs]:

```json
{
  "providers": {
    "openrouter": {
      "api_key": "$OPENROUTER_API_KEY",
      "base_url": "https://openrouter.ai/api/v1"
    }
  }
}
```

Env-only setup is also documented: `export OPENROUTER_API_KEY="..."` [OFFICIAL].

### Custom OpenAI-Compatible

The Deepseek worked example is the canonical template [OFFICIAL]:

```json
{
  "$schema": "https://charm.land/crush.json",
  "providers": {
    "deepseek": {
      "type": "openai-compat",
      "base_url": "https://api.deepseek.com/v1",
      "api_key": "$DEEPSEEK_API_KEY",
      "models": [{
        "id": "deepseek-chat",
        "name": "Deepseek V3",
        "cost_per_1m_in": 0.27,
        "cost_per_1m_out": 1.1,
        "context_window": 64000,
        "default_max_tokens": 5000
      }]
    }
  }
}
```

Local OpenAI-compatible endpoints (Ollama at `http://localhost:11434/v1`, LocalAI at `http://localai.lan:8081/v1`) are documented with the same pattern [OFFICIAL]. Anthropic-typed providers additionally accept `extra_headers` for custom routing [OFFICIAL].

### Per-Agent Routing

**Not supported.** Crush's documented config has no per-agent model field; model selection happens at session level via `/model` picker [OFFICIAL]. This is the main gap vs opencode.

### Verdict

Excellent for a polished single-model workflow with free provider choice. Weak for multi-model orchestration.

---

## OpenHands

OpenHands is a **LiteLLM-based** agent, which inherits LiteLLM's full provider catalog (100+ including OpenRouter, Anthropic, OpenAI, Azure, Bedrock, Vertex, Together, Groq, Cerebras, Fireworks, DeepInfra, Ollama, vLLM) [OFFICIAL].

### OpenRouter

Configured in the UI under Settings → LLM, with `LLM Provider: OpenRouter` and `LLM Model` either from the list or custom-formatted as `openrouter/<model-name>` e.g. `openrouter/anthropic/claude-3.5-sonnet` [OFFICIAL].

### Custom OpenAI-Compatible

Configuration flows through LiteLLM's base-URL mechanism. Env vars include `OPENROUTER_API_KEY` and `OPENROUTER_API_BASE` (defaults to `https://openrouter.ai/api/v1`) [OFFICIAL]. Arbitrary endpoints use LiteLLM's `openai/` prefix with `api_base` and `api_key` [OFFICIAL].

### Per-Agent / Per-Role Routing

OpenHands has a **condenser** and **main LLM** split — distinct model configs for the primary agent vs. the context-condensation step [OFFICIAL — OpenHands settings]. This is a real per-role routing point, though narrower than opencode's per-agent design.

### Verdict

Any provider LiteLLM knows, OpenHands knows. Configuration lives in a UI rather than a text config, which is awkward for CLI-only workflows — though the `config.toml` backend config is editable.

---

## Aider

Aider is **LiteLLM-based** and therefore speaks every provider LiteLLM does [OFFICIAL].

### OpenRouter

```bash
export OPENROUTER_API_KEY=<key>
aider --model openrouter/anthropic/claude-3.7-sonnet
```

Provider routing pins and fallbacks are configured in `.aider.model.settings.yml` [OFFICIAL]:

```yaml
- name: openrouter/anthropic/claude-3.7-sonnet
  extra_params:
    extra_body:
      provider:
        order: ["Anthropic", "Together"]
        allow_fallbacks: false
        data_collection: "deny"
        require_parameters: true
```

### OpenAI-Compatible

```bash
export OPENAI_API_BASE=<endpoint>
export OPENAI_API_KEY=<key>
aider --model openai/<model-name>
```

The `openai/` prefix with a custom base URL unlocks any OpenAI-compatible endpoint including vLLM, Together AI, Groq, and LiteLLM proxy [OFFICIAL].

### Per-Role Model Routing

Aider has the oldest documented role-split in this survey: `--model` for the main "architect", `--editor-model` for the edit stage, and `--weak-model` for lightweight commit-message generation [OFFICIAL]. This is a genuine per-task router built before the concept was standard.

### Verdict

Mature, LiteLLM-backed, architect/editor/weak model split. Weaker sub-agent/delegation story than opencode but stronger than Crush.

---

## Cline & Roo Code (VS Code)

Both are VS Code extensions, not pure CLIs, but frequently considered as Claude Code alternatives.

### OpenRouter (both)

Settings → API Provider → OpenRouter, paste API key, pick model. Custom base URL is optional [OFFICIAL].

### OpenAI-Compatible (both)

Settings → API Provider → "OpenAI Compatible", supply `base_url`, `api_key`, and `model_id`. Model ID must include the provider prefix (e.g., `anthropic/`, `openai/`) when the base URL points at a gateway [OFFICIAL]. Tool-calling support on the endpoint is required — Cline uses native tool calling exclusively [OFFICIAL].

### Per-Agent / Per-Mode Routing

- **Cline** has a Plan/Act mode split: separate model selection for each mode [OFFICIAL].
- **Roo Code** extends this with **Configuration Profiles** — multiple named API configs (e.g., "Gemini 2.0 Flash for docs, low temperature") assignable to interaction modes (Code/Architect/Ask/Debug/Orchestrator) [OFFICIAL].

Roo Code is effectively the richest per-mode routing in this survey apart from opencode.

### Verdict

Both are strong marketplace consumers. Roo Code's configuration profiles are the closest match to opencode's per-agent model field. Neither is a CMUX-native CLI — that's a disqualifier for the broader research goal.

---

## Continue

Continue (`continue.dev`) is a `config.yaml`-driven multi-provider assistant with explicit **model roles** [OFFICIAL].

### OpenRouter

```yaml
name: My Config
version: 0.0.1
schema: v1

models:
  - name: <MODEL_NAME>
    provider: openrouter
    model: <MODEL_ID>
    apiBase: https://openrouter.ai/api/v1
    apiKey: <YOUR_OPEN_ROUTER_API_KEY>
    capabilities:
      - tool_use
    requestOptions:
      extraBodyProperties:
        transforms: []
```

### Roles

The `roles:` array on each model assigns it to one or more of: `chat`, `autocomplete`, `edit`, `apply`, `embed`, `rerank`, `summarize` [OFFICIAL]. Default: `[chat, edit, apply, summarize]`. This is explicit per-task model routing at the config level — different from opencode's agent-based slicing but functionally similar.

### Verdict

Strong per-role routing baked into the config schema. Native multi-provider SDKs including Anthropic, OpenAI, Google, Mistral, Azure, Ollama, LM Studio [OFFICIAL].

---

## Gemini CLI (Google)

**Official Gemini CLI supports only Google Gemini models** and a narrow local inference path via LiteRT-LM [OFFICIAL — GH Discussion #24166, Issue #1605]. No official OpenRouter, no arbitrary OpenAI-compatible backend, no provider override field.

Workarounds are community-only:

- `@chameleon-nexus-tech/gemini-cli-openrouter` — a third-party npm fork translating Gemini API format to OpenRouter's API surface, 200+ models [UNVERIFIED — npm package].
- LiteLLM Proxy in front of Gemini CLI — route through LiteLLM pretending to be Google, gaining access to any LiteLLM-supported model [OFFICIAL — LiteLLM docs].

### Verdict

**Does not qualify** as an LLM-marketplace CLI. Eliminate unless you're specifically committing to Google-only and accept community forks.

---

## Amp (Sourcegraph)

Amp is **deliberately** not a BYOM product. Its manual states the core principle: "always uses the best models" — Amp picks Claude Opus 4.6, GPT-5.4, and Claude Haiku 4.5 per-mode (smart/rush/deep) and the user cannot override [OFFICIAL]. Configuration knobs are `AMP_API_KEY`, `AMP_LOG_LEVEL`, `AMP_SETTINGS_FILE`, and MCP server registration — all tool-level, not model-level [OFFICIAL].

### Verdict

**Does not qualify** on the marketplace criterion. Eliminate if BYO-LLM is a hard requirement.

---

## pi (pi-mono / @mariozechner/pi-coding-agent)

pi is a TypeScript-based agent toolkit. Provider list: Anthropic, OpenAI, Google, Azure, Bedrock, Mistral, Groq, Cerebras, xAI, Hugging Face, Kimi For Coding, MiniMax, OpenRouter, Ollama [OFFICIAL — pi-mono docs].

### OpenRouter

```bash
export OPENROUTER_API_KEY=your-key
pi
```

Model selection is then interactive via `/model` or Ctrl+L [OFFICIAL].

### Custom Providers

Per the official provider docs: "Custom providers and models can be added via `~/.pi/agent/models.json` if they speak a supported API (OpenAI Completions, OpenAI Responses, Anthropic Messages, Google Generative AI)" [OFFICIAL]. For stranger auth flows or OAuth, a pi **extension** is the pluggable path [OFFICIAL — examples/extensions/custom-provider-gitlab-duo].

Credential resolution order is explicit: CLI `--api-key` → `auth.json` → env var → custom provider key in `models.json` [OFFICIAL].

### Subagents & Per-Task

pi supports **subagents that run in their own context window, possibly with a different LLM** [OFFICIAL]. CLI example: `pi --provider openai --model gpt-4o "Help me refactor"` — explicit per-invocation routing [OFFICIAL].

### Verdict

Strong marketplace story for a TypeScript-native agent, with four built-in tools (read, write, edit, bash) and a first-class subagent-with-own-LLM concept. Custom providers are JSON-extensible; oddball providers require an extension.

---

## Answering the Targeted Questions

**Q: Which agents have first-class OpenRouter support?**
opencode, Codex CLI, Crush, OpenHands, Aider, Cline, Roo Code, Continue, and pi all have documented OpenRouter recipes. Only Gemini CLI and Amp do not. [OFFICIAL across all docs.]

**Q: Which agents generically accept OpenAI-compatible endpoints (LiteLLM, Ollama, vLLM, etc.)?**
All of the above except Amp. opencode, Codex, and Crush use explicit typed provider blocks; OpenHands and Aider use LiteLLM internally; Cline/Roo Code use a UI "OpenAI Compatible" picker; Continue uses provider: openai with apiBase override; pi uses models.json.

**Q: Which agents have native multi-provider SDKs (not just OpenAI-style)?**
opencode (Vercel AI SDK, 75+), OpenHands (LiteLLM, 100+), Aider (LiteLLM, 100+), Cline, Roo Code, Continue, and pi. Codex CLI and Crush support Anthropic natively but are thinner elsewhere. Amp is single-vendor-controlled.

**Q: Per-task / per-agent model routing (use model X for plan, Y for edit, Z for review)?**

- **Best**: opencode (per-agent config + subagent mode + markdown frontmatter) and Roo Code (Configuration Profiles per mode).
- **Good**: Continue (explicit `roles:` array), Aider (`--model`/`--editor-model`/`--weak-model`), pi (subagents with own LLM), OpenHands (main + condenser split), Cline (Plan/Act mode split).
- **Weak/none**: Crush, Codex CLI (global knobs only), Gemini CLI, Amp.

**Q: Custom bring-your-own-provider without modifying source?**
opencode wins on generality (any npm AI SDK package). Codex CLI and Crush are strong via `[model_providers.*]` / `providers.*`. pi supports it via `models.json`. Everything routing through LiteLLM (OpenHands, Aider) inherits LiteLLM's custom-endpoint handling. Gemini CLI and Amp do not support BYO.

**Q: Configuration surface?**

- JSON: opencode (`opencode.json`), Crush (`crush.json`), pi (`models.json`), Cline/Roo Code (VS Code settings JSON)
- TOML: Codex CLI (`~/.codex/config.toml`)
- YAML: Continue (`config.yaml`), Aider (`.aider.model.settings.yml`)
- UI-only: OpenHands (settings panel + LiteLLM env behind it)
- Env-only at minimum: all agents support env-var API keys

---

## Ranking by Marketplace Flexibility (Claude Code Replacement Lens)

1. **opencode** — Most flexible; per-agent models, 75+ providers, npm-pluggable backends, explicit OpenRouter provider-routing fields.
2. **pi** — Strong multi-provider story with models.json + subagents-with-own-LLM + extensions.
3. **OpenHands** — LiteLLM gives it everything; per-role split (main/condenser); weaker as a pure CLI.
4. **Aider** — LiteLLM + oldest-but-still-best architect/editor/weak split; config via YAML.
5. **Roo Code** — Configuration Profiles per mode; VS-Code-native so non-CLI.
6. **Continue** — Clean `roles:` array in config.yaml; native multi-provider SDKs.
7. **Codex CLI** — Solid custom-provider support; weak per-agent routing.
8. **Charm Crush** — Polished UX, typed providers, but no per-agent routing.
9. **Cline** — Plan/Act split is narrower than Roo Code's profiles; VS-Code-native.
10. **Gemini CLI** — Disqualified without community forks.
11. **Amp** — Disqualified by design.

For a **CMUX-integrated Claude Code replacement**, the top three contenders on provider flexibility alone are **opencode**, **pi**, and **OpenHands** (with Codex CLI as a viable single-model fallback and Roo Code as the best VS-Code alternative if a non-CLI surface is acceptable).

---

## Sources

- [OpenCode Providers docs](https://opencode.ai/docs/providers/) [OFFICIAL]
- [OpenCode Models docs](https://opencode.ai/docs/models/) [OFFICIAL]
- [OpenCode Agents docs](https://opencode.ai/docs/agents/) [OFFICIAL]
- [sst/opencode provider-and-model-configuration (DeepWiki)](https://deepwiki.com/sst/opencode/3.3-provider-and-model-configuration) [OFFICIAL mirror]
- [Kickstart OpenCode with OpenRouter](https://dev.to/mozes721/kickstart-opencode-with-openrouter-32o7) [PRAC]
- [OpenAI Codex CLI config-advanced](https://developers.openai.com/codex/config-advanced) [OFFICIAL]
- [OpenAI Codex CLI config-reference](https://developers.openai.com/codex/config-reference) [OFFICIAL]
- [OpenRouter Integration with Codex CLI](https://openrouter.ai/docs/guides/coding-agents/codex-cli) [OFFICIAL]
- [Charm Crush GitHub README](https://github.com/charmbracelet/crush) [OFFICIAL]
- [Crush Model Configuration (DeepWiki)](https://deepwiki.com/charmbracelet/crush/4.3-model-configuration) [OFFICIAL mirror]
- [Setting up Crush-AI Coding Agent with OpenRouter (Medium)](https://medium.com/@ankushjain358/setting-up-crush-ai-coding-agent-with-open-router-a9bcd1a2a00c) [PRAC]
- [How to use Open WebUI (Ollama) with Crush](https://jrdsgl.com/how-to-use-open-webui-backed-by-ollama-with-charms-crush/) [PRAC]
- [OpenHands OpenRouter docs](https://docs.openhands.dev/openhands/usage/llms/openrouter) [OFFICIAL]
- [LiteLLM OpenRouter provider docs](https://docs.litellm.ai/docs/providers/openrouter) [OFFICIAL]
- [LiteLLM OpenAI-Compatible Endpoints](https://docs.litellm.ai/docs/providers/openai_compatible) [OFFICIAL]
- [Aider OpenRouter docs](https://aider.chat/docs/llms/openrouter.html) [OFFICIAL]
- [Aider OpenAI-compatible docs](https://aider.chat/docs/llms/openai-compat.html) [OFFICIAL]
- [Cline OpenRouter docs](https://docs.cline.bot/provider-config/openrouter) [OFFICIAL]
- [Roo Code OpenRouter docs](https://docs.roocode.com/providers/openrouter) [OFFICIAL]
- [Roo Code OpenAI-Compatible docs](https://docs.roocode.com/providers/openai-compatible) [OFFICIAL]
- [Continue OpenRouter docs](https://docs.continue.dev/customize/model-providers/top-level/openrouter) [OFFICIAL]
- [Continue Model Roles](https://docs.continue.dev/customize/model-roles/intro) [OFFICIAL]
- [Continue config.yaml Reference](https://docs.continue.dev/reference) [OFFICIAL]
- [Gemini CLI Universal Local Model Support discussion (#24166)](https://github.com/google-gemini/gemini-cli/discussions/24166) [OFFICIAL — issue tracker]
- [Gemini CLI Add OpenAI backend request (#1605)](https://github.com/google-gemini/gemini-cli/issues/1605) [OFFICIAL — issue tracker]
- [@chameleon-nexus-tech/gemini-cli-openrouter (npm)](https://www.npmjs.com/package/@chameleon-nexus-tech/gemini-cli-openrouter) [UNVERIFIED — community fork]
- [Amp Owner's Manual](https://ampcode.com/manual) [OFFICIAL]
- [pi-mono coding-agent README](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/README.md) [OFFICIAL]
- [pi-mono providers.md](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/providers.md) [OFFICIAL]
- [@mariozechner/pi-coding-agent npm](https://www.npmjs.com/package/@mariozechner/pi-coding-agent) [OFFICIAL]
