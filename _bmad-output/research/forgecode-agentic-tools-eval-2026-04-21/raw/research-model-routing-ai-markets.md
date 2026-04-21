---
content_origin: claude-code-subagent
date: 2026-04-21
sub_question: "Which model routers and AI marketplaces are popular in these communities — OpenRouter and its alternatives (Together, Groq, Fireworks, OpenAI-compatible gateways like LiteLLM/Helicone, direct provider APIs, Ollama / Llama.cpp / local)? For each tool, how first-class is the integration, what routing/fallback/cost-control primitives exist, and what does the cost/quality tradeoff look like in practice for routine coding tasks?"
topic: "ForgeCode and agentic tooling evaluation for Momentum"
---

# Model Routers and AI Marketplaces in Agentic Coding Tools (April 2026)

## 1. The Router Landscape

The market for "route a single SDK call to any model" has consolidated around a handful of patterns: (a) a hosted aggregator with one API key and credits (OpenRouter), (b) dedicated high-throughput inference clouds for open-weight models (Groq, Cerebras, Together, Fireworks), (c) self-hosted OpenAI-compatible gateways that unify direct provider keys (LiteLLM, Helicone, Portkey), and (d) local runtimes for offline / privacy workloads (Ollama, LM Studio, llama.cpp). Every tool surveyed below ultimately talks to one of these shapes.

### 1.1 OpenRouter (hosted aggregator)

OpenRouter is the de-facto default "bring one key, talk to 300+ models" service in the indie / open-source agentic coding community. As of April 2026 it advertises 290+ models from Anthropic, OpenAI, Google, DeepSeek, Meta, Mistral, xAI, Qwen and community hosts, and does not mark up per-token provider pricing — revenue comes from a 5.5% surcharge on credit top-ups [OFFICIAL][^or-pricing][^zenmux]. It exposes an OpenAI-compatible `/chat/completions` endpoint, plus a native-dialect "Anthropic Skin" at `https://openrouter.ai/api` that speaks Claude's Messages API well enough for Claude Code to talk to it unmodified [OFFICIAL][^or-cc].

Routing primitives are a major reason OpenRouter dominates:

- **Provider ordering** (`provider: { order: [...], allow_fallbacks: true|false }`) lets a caller pin a preferred backend for a model served by multiple hosts, with automatic failover to the next provider on error [OFFICIAL][^or-provider-routing].
- **Auto Exacto** (default-on for tool-call requests as of 2026) re-scores providers every five minutes across throughput, tool-call telemetry, and benchmark signals [OFFICIAL][^or-pricing].
- **Sort modes** — lowest-price, highest-throughput, lowest-latency — are first-class request params and are reflected one-for-one in Cline/Kilo UIs [OFFICIAL][^kilo-or].
- **BYOK** lets you point a provider slot at your own OpenAI/Anthropic/etc. key; OpenRouter always tries BYOK endpoints first regardless of the declared order, then falls back to shared capacity [OFFICIAL][^or-byok]. A million BYOK requests/month are free; beyond that a thin 5% BYOK fee applies [OFFICIAL][^or-byok].
- **Middle-out prompt compression** is a server-side transform Cline/Kilo expose as a checkbox [OFFICIAL][^kilo-or].

Reputation: latency and reliability vary per-provider, but OpenRouter's provider-aware routing mitigates the worst cases. Practitioners on HN/Reddit generally treat it as "good enough to put in front of real work" as long as you pin providers for quality-sensitive models [PRAC][^hn-arbitrage][^free-guide].

### 1.2 Dedicated inference clouds (open-weight focus)

- **Groq** runs open-weight Llama / Qwen / GPT-OSS models on custom LPU silicon. Reported steady-state throughput ~476 tok/s on Llama 3.1 70B with 0.6–0.9 s TTFT [PRAC][^infra-compared][^arbitrage]. Free tier exists; primary trade-off is that only open-weight models are served.
- **Cerebras** is the outlier on speed: ~3,000 tok/s on GPT-OSS 120B and ~2,000 tok/s on Qwen3-Coder-480B, ~6× Groq on identical models per Artificial Analysis benchmarks [OFFICIAL][^cerebras-cs3][^cerebras-qwen3]. Cerebras Code is a flat-rate subscription plan aimed directly at agentic coding, and the company partners with Cline for first-class VS Code integration [OFFICIAL][^cerebras-qwen3][^cerebras-cline].
- **Together AI** and **Fireworks AI** are the general-purpose open-weight clouds — Llama, Mistral, DeepSeek, Qwen, plus fine-tuning. Reported Fireworks throughput 747 tok/s at 0.17 s TTFT; both advertise 50–90% savings vs. frontier APIs on equivalent workloads [PRAC][^infra-compared][^arbitrage].
- **DeepInfra**, **Hyperbolic**, **SambaNova**, **Novita** round out the pack and show up in ForgeCode / Qwen Code configuration examples [OFFICIAL][^novita-forge].

### 1.3 Self-hosted gateways (the LiteLLM layer)

- **LiteLLM** is the dominant open-source proxy. It speaks OpenAI's Chat Completions and Anthropic's Messages API in front of 100+ providers, with load balancing, ordered fallbacks (`order=1` → `order=2` → `order=3` each with their own retry budget, then a final fallbacks list), cooldowns, timeouts, exponential-backoff retries, tag-based routing, budget routing, and health-check-driven routing [OFFICIAL][^litellm-routing][^litellm-gh]. Per-key / per-team virtual keys, cost tracking, guardrails, logging, and an admin dashboard ship in the proxy mode. It is the component that makes most Claude-Code-on-non-Anthropic-models setups possible [OFFICIAL][^litellm-cc][^litellm-non-anth].
- **Helicone** is primarily an observability proxy (cost/latency dashboards, request-level tracing, user tracking) with a newer Rust-based AI Gateway that competes more directly with LiteLLM on latency [PRAC][^helicone-portkey][^gateway-compare].
- **Portkey** is a commercial gateway ($49/mo+, not self-hostable) that advertises 1,600+ models, conditional routing, circuit breakers, HIPAA/SOC 2, and guardrails [PRAC][^helicone-portkey]. Popular at enterprises, less so in the indie coding-agent community.
- **Cloudflare AI Gateway**, **Tetrate Agent Router**, **RelayPlane** are newer competitors that show up in side-by-side gateway reviews [PRAC][^gateway-compare][^tetrate].

### 1.4 Direct provider APIs

Anthropic, OpenAI, and Google still serve their flagship models directly, and every tool below has a first-class path to them. The pitch for going direct: lowest latency, no aggregator overhead, native feature access (prompt caching headers, interleaved-thinking betas, Files API, etc.). The pitch against: separate billing per provider and no unified fallback.

### 1.5 Local runtimes

- **Ollama** exposes an OpenAI-compatible server on `http://localhost:11434` [OFFICIAL][^ollama-opencode]. It added first-class "Ollama launch" wrappers for claude-code, codex, droid, and opencode in 2026 [PRAC][^ollama-launch].
- **LM Studio** and **llama.cpp** server mode fill the same OpenAI-compatible niche.
- Practitioner consensus: useful for privacy/offline and for routing easy sub-tasks (lint, summarize, grep) to a local model, but context-window tuning (Ollama defaults to 4,096 tokens, painfully low for agent loops) and tool-calling fidelity are the usual blockers [PRAC][^opencode-ollama].

## 2. Tool × Router Integration Matrix

Legend: **First-class** = dedicated UI/config; **Via OpenAI-compat** = works through the OpenAI-compatible provider slot with base URL override; **Via proxy** = requires a LiteLLM-style proxy in front; **Native API** = tool speaks the provider's wire format directly.

| Tool | OpenRouter | Anthropic direct | OpenAI direct | Google / Vertex | Groq | Cerebras | Together / Fireworks | LiteLLM / proxy | Ollama / local | Per-task/subagent model | Fallback chain |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Claude Code** | First-class (Anthropic Skin via `ANTHROPIC_BASE_URL`) [^or-cc] | Native API (default) | Via proxy (LiteLLM) [^litellm-cc] | Via proxy | Via proxy | Via proxy | Via proxy | First-class (documented flow) [^litellm-cc] | Via proxy or Ollama Launch [^ollama-launch] | Built-in (subagent `model:` field, `CLAUDE_CODE_SUBAGENT_MODEL`) [^cc-subagents] | No native chain; relies on proxy |
| **ForgeCode** | First-class [^forge-custom] | First-class | First-class | First-class (Vertex) | First-class | Via `[[providers]]` custom entry | Via `[[providers]]` custom entry [^novita-forge] | Via `[[providers]]` with LiteLLM URL | Via `[[providers]]` pointing at localhost | Per-agent via `.forge/agents/*.md` front-matter; `:provider` command to switch [^forge-custom] | Manual via `[[providers]]` entries; no automatic chain documented |
| **Goose** | First-class (browser auth flow) [^goose-providers] | First-class | First-class | First-class | First-class | Via OpenAI-compat | Via OpenAI-compat | First-class (dedicated LiteLLM provider) [^goose-providers] | First-class (dedicated Ollama/LM Studio/vLLM/Ramalama/KServe providers) [^goose-providers] | Configure per provider via `goose configure`; prompt caching auto-enabled for Claude via Anthropic/Bedrock/Databricks/OpenRouter/LiteLLM [^goose-providers] | Tool-call fidelity gated on "works best with Claude 4" |
| **OpenCode** | First-class (preloaded) [^opencode-providers] | First-class | First-class | First-class | First-class | Via OpenAI-compat | Via OpenAI-compat | Via OpenAI-compat | First-class (Ollama, LM Studio, llama.cpp) [^opencode-providers] | `provider` / `model` / `small_model` keys in `opencode.json`; AI SDK-backed [^opencode-providers] | Not built-in; relies on OpenRouter or proxy |
| **Qwen Code** | Via OpenAI-compat (baseUrl swap) [^qwen-providers] | First-class (`anthropic` auth type) | First-class (`openai` auth type) | First-class (`gemini` auth type) | Via OpenAI-compat | Via OpenAI-compat | First-class (documented) [^qwen-providers] | Via OpenAI-compat | Via OpenAI-compat (Ollama, vLLM) [^qwen-providers] | `modelProviders` in `settings.json` with per-provider `generationConfig` as "impermeable layer"; `/model` picker switches between them [^qwen-providers] | No native; switch providers manually |
| **Kilo Code** | First-class with provider sort (price/throughput/latency), data policy, middle-out compression [^kilo-or] | First-class | First-class | First-class | First-class | First-class (via OpenRouter or direct) | Via OpenAI-compat | Via OpenAI-compat | First-class | Per-mode model selection; no built-in fallback chain | Relies on OpenRouter sort order |
| **Aider** | First-class (`--model openrouter/<provider>/<model>`, `.aider.model.settings.yml`) [^aider-or] | First-class | First-class | First-class | First-class (via LiteLLM under the hood) | First-class (via LiteLLM) | First-class (via LiteLLM) | Uses LiteLLM internally — anything LiteLLM supports, Aider supports [^aider-deepwiki] | First-class | **Three-tier architecture**: main model, `--weak-model` (commit msgs, summarization), `--editor-model` (architect-mode edits) [^aider-config] | Provider-level via OpenRouter or `.aider.model.settings.yml` |
| **Cline** | First-class, with provider-routing UI for sort/order (limited — no `allow_fallbacks` toggle yet) [^cline-or][^cline-issue] | First-class | First-class | First-class | First-class | First-class (partnered) [^cerebras-cline] | Via OpenAI-compat | Via OpenAI-compat | First-class (LM Studio, Ollama) | Per-mode (Plan/Act) model selection | Inherits OpenRouter behaviour; no native multi-provider chain |

### 2.1 Notes on configuration ergonomics

- **Env-var plumbing is universal.** Every tool accepts `OPENROUTER_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` equivalents; ForgeCode, Qwen Code, and OpenCode all use `envKey`/`api_key_vars` indirection so secrets never hit config files [OFFICIAL][^forge-custom][^qwen-providers][^opencode-providers].
- **Config-file primacy** differs sharply: Aider uses `~/.aider.model.settings.yml` + `.env`, OpenCode uses `opencode.json` with `{env:VAR}` interpolation, ForgeCode uses `.forge.toml` with `[[providers]]` arrays, Qwen Code uses `settings.json` `modelProviders`, Claude Code uses `.claude/settings.local.json` + env, Cline/Kilo push most config into a VS Code settings UI.
- **Per-task override** is where tools diverge most. Claude Code's subagent `model:` field, Aider's three-tier (`--model` / `--weak-model` / `--editor-model`), and ForgeCode's per-agent YAML front-matter are the three most mature patterns. OpenCode's `small_model` is a one-dimensional equivalent. Cline/Kilo ship per-mode (Plan vs Act) model selection. Goose/Qwen Code rely on global `/model` switching.

### 2.2 Cost-control primitives by tool

| Tool | Budget/token cap | Cost telemetry | Observability hook |
|---|---|---|---|
| Claude Code | Via proxy (LiteLLM key budgets) | Built-in usage line; richer via proxy | LiteLLM, Helicone via `ANTHROPIC_BASE_URL` |
| ForgeCode | Provider-level only | Per-session; no central aggregation documented | Custom provider URL points anywhere |
| Goose | Per-provider | Cost tracking via LiteLLM or provider | LiteLLM as first-class provider |
| OpenCode | Provider-level | Session-level; usage command | OpenAI-compatible base URL to any proxy |
| Qwen Code | Provider-level | None built-in | OpenAI-compatible base URL |
| Kilo Code | OpenRouter credits / provider | UI-level | OpenRouter |
| Aider | None built-in; LiteLLM below | Per-session `/tokens` command; cache stats | LiteLLM layer |
| Cline | OpenRouter credits | UI-level; per-task cost display | OpenRouter; Helicone possible |

The pattern is unmistakable: **none of these tools implement sophisticated budget/rate-limit logic themselves.** They all offload it to either OpenRouter's credit system or a LiteLLM/Helicone proxy. If a team wants per-project budgets, per-developer caps, or alerting, the operative decision is which gateway sits in front, not which tool sits in the editor.

## 3. Cost / Quality Trade-offs for Routine Coding

The Aider Polyglot leaderboard (last refreshed Nov 2025, 225 Exercism exercises across C++, Go, Java, JS, Python, Rust) remains the most cited apples-to-apples benchmark for "can this model actually edit real code" [OFFICIAL][^aider-leaderboard]. Key rows:

| Model | Polyglot % | Cost to run benchmark | Per-MTok (in/out) | Notes |
|---|---|---|---|---|
| Claude Opus 4.5 | 89.4% (vendor-reported) | n/a | $15/$75 (est.) | Tops multi-language |
| GPT-5 (high) | 88.0% | $29.08 | — | Leaderboard #1 |
| GPT-5 (medium) | 86.7% | $17.69 | — | |
| O3-Pro (high) | 84.9% | $146.32 | — | Expensive outlier |
| Gemini 2.5 Pro Preview | 83.1% | $49.88 | — | |
| O3 (high) | 81.3% | $21.23 | — | |
| Claude Sonnet 4.6 | ~79.6% SWE-bench Verified | — | $3/$15 | ~95% Opus quality at 60% cost per Morph analysis [^morph-coding] |
| DeepSeek V3.2 Reasoner | 74.2% | $1.30 | $0.27/$1.00 | **22× cheaper than GPT-5 at 84% of score** [^aider-leaderboard] |
| Claude Opus 4 | 72.0% | $65.75 | — | |
| DeepSeek V3.2 Chat | 70.2% | $0.88 | — | Non-reasoning |
| Qwen3-Coder-480B | (not on leaderboard; ~73% SWE-bench Verified reported) | — | ~$2/MTok on Cerebras; free tier on OpenRouter [^cerebras-qwen3][^or-qwen] | Dominated OpenRouter's coding leaderboard at launch — #2 within 2 weeks [^cerebras-qwen3] |
| Qwen2.5-Coder-32B | ~73.7 on older Aider / 8% on current polyglot [^qwen-polyglot-gh] | — | $0.07–0.90/MTok on open-weight hosts | Older-benchmark-only; newer polyglot much harder |
| Qwen3-Coder-Next-3B-active | 70.6% SWE-bench Verified | — | local or cheap | 3B active params, runs on 24 GB GPU |

### 3.1 What practitioners actually pick

- **Frontier autonomy (large refactors, architecture, multi-file reasoning):** Claude Sonnet 4.6 or GPT-5 (medium) are the community defaults. Sonnet wins on tool-call fidelity; GPT-5 wins on raw polyglot score [PRAC][^morph-coding].
- **Routine edits, scaffolding, CRUD:** DeepSeek V3.2 Chat at $0.88 for the entire Aider polyglot is the cost-per-quality champion; Qwen3-Coder-480B on the free OpenRouter tier or at ~$2/MTok on Cerebras (at 2,000 tok/s) is the speed-per-quality champion [PRAC][^cerebras-qwen3][^aider-leaderboard].
- **Explore / read-only / search sub-tasks:** Haiku 4 (Claude Code's built-in default for Explore subagent), Gemini 2.5 Flash, or a local Qwen3 via Ollama. The industry rule-of-thumb: "no reason a find-all-files task needs Opus" [PRAC][^cc-subagents].
- **Commit message / summarization weak-model slot:** DeepSeek Chat, Haiku 4, or Gemini Flash are the common picks — Aider's `--weak-model` flag exists specifically for this [OFFICIAL][^aider-config].

### 3.2 The "speed changes the loop" effect

Cerebras' 2,000 tok/s Qwen3-Coder figure — "1,000 lines of JavaScript in 4 seconds vs 80 seconds on Claude 4 Sonnet" — is a practitioner-level UX shift, not just a benchmark win [OFFICIAL][^cerebras-qwen3]. In agentic loops where the model calls tools dozens of times per task, cutting round-trip latency 10–20× compresses the whole session. That's why Cline's official Cerebras integration matters: it's the fastest end-to-end agentic coding setup currently shipping, not just the cheapest [OFFICIAL][^cerebras-cline]. The caveat is latency at small prompt sizes: Cerebras has higher TTFT than Groq, so for chat-style interactions Groq still wins [PRAC][^biggo-cerebras].

### 3.3 Tokens per fix — Aider's overhead advantage

A 2026 morphllm analysis found Aider uses 4.2× fewer tokens than Claude Code on a 3-tool, 47-file diff benchmark, largely because Aider's edit format is compact diff-based rather than full-file rewrites [PRAC][^morph-aider]. When multiplied across a day's work, this is a bigger cost lever than the model choice itself for routine edits — a point that affects model-economics reasoning for Momentum regardless of the router chosen.

## 4. OpenAI-Compatible Gateways as Universal Adapter

The OpenAI `/chat/completions` shape (plus its `tools` / `tool_calls` dialect) has effectively become the lingua franca. The evidence in this survey:

- **Qwen Code** explicitly treats `openai` as its primary auth type that covers OpenAI, Azure, OpenRouter, and local inference servers — "any OpenAI-compatible endpoint" [OFFICIAL][^qwen-providers].
- **OpenCode** is built on Vercel's AI SDK, whose `@ai-sdk/openai-compatible` provider handles anything shaped like OpenAI; Models.dev preloads 75+ providers through this channel [OFFICIAL][^opencode-providers].
- **Ollama, LM Studio, llama.cpp, vLLM** all expose OpenAI-compatible endpoints, which is why every tool can point at `http://localhost:11434` without special-casing [OFFICIAL][^ollama-opencode].
- **LiteLLM's proxy mode** is designed to *produce* an OpenAI-compatible endpoint on top of anything, which is why it's the universal adapter for Claude Code and other tools that can override a base URL [OFFICIAL][^litellm-cc].

Where tools **bypass** OpenAI-compat:

- **Claude Code** speaks Anthropic's Messages API natively. OpenRouter's "Anthropic Skin" and LiteLLM's pass-through endpoint are what make non-Anthropic backends usable — either by translating Messages-API-in to Messages-API-out (OpenRouter) or by translating Messages-API-in to OpenAI/any-out (LiteLLM) [OFFICIAL][^or-cc][^litellm-non-anth].
- **Goose** adds `cache_control` markers for Claude via Anthropic / Bedrock / Databricks / OpenRouter / LiteLLM; this is Anthropic-dialect-specific behavior that sits above the OpenAI-compat layer [OFFICIAL][^goose-providers].
- **OpenCode's provider transformations** inject Anthropic-specific beta headers (`interleaved-thinking`, `fine-grained-tool-streaming`) when talking to Claude, even through OpenRouter — showing that "OpenAI-compatible" alone isn't sufficient when you want feature parity [OFFICIAL][^opencode-transforms].

**Net assessment for Momentum:** if a Claude-Code-centric workflow needs to route sub-tasks to cheaper / open-weight models, there are two viable architectures. (A) Set `ANTHROPIC_BASE_URL` to OpenRouter's Anthropic Skin and use Claude Code's native subagent `model:` field to pick cheaper Claude-family models or to point at OpenRouter's Anthropic-dialect-compatible entries. (B) Stand up LiteLLM as a self-hosted proxy, point Claude Code at it via `ANTHROPIC_BASE_URL`, and use LiteLLM's routing/fallback/budget primitives to fan out to any backend. Architecture (B) is strictly more capable (real fallback chains, real budgets, real per-key telemetry) at the cost of one more service to operate. Architecture (A) is zero-ops and works today [OFFICIAL][^or-cc][^litellm-cc].

Every other tool in the survey is more flexible than Claude Code on this axis — ForgeCode, Goose, OpenCode, Aider, and Qwen Code can all mix models per-agent or per-task natively. This is the single most important delta if cost control via model specialization is a goal: **Claude Code is the most constrained tool in the survey on router/provider choice**, which is a structural consequence of being Anthropic's first-party product.

## Sources

[^or-pricing]: [OpenRouter Pricing](https://openrouter.ai/pricing) — OFFICIAL, 2026. Passthrough rates, 5.5% credit surcharge, Auto Exacto re-evaluation.
[^or-cc]: [Claude Code Integration — OpenRouter Docs](https://openrouter.ai/docs/guides/coding-agents/claude-code-integration) — OFFICIAL, 2026. Anthropic Skin, `ANTHROPIC_BASE_URL` setup.
[^or-provider-routing]: [Provider Routing — OpenRouter Docs](https://openrouter.ai/docs/guides/routing/provider-selection) — OFFICIAL. `provider.order`, `allow_fallbacks`, sort modes.
[^or-byok]: [BYOK — OpenRouter Docs](https://openrouter.ai/docs/guides/overview/auth/byok) and [1M free BYOK requests/month announcement](https://openrouter.ai/announcements/1-million-free-byok-requests-per-month) — OFFICIAL, 2026.
[^or-qwen]: [Qwen3 Coder 480B A35B (free) on OpenRouter](https://openrouter.ai/qwen/qwen3-coder:free) — OFFICIAL, 2026.
[^zenmux]: [OpenRouter API Pricing 2026 — ZenMux](https://zenmux.ai/blog/openrouter-api-pricing-2026-full-breakdown-of-rates-tiers-and-usage-costs) — PRAC, 2026.
[^litellm-gh]: [BerriAI/litellm — GitHub](https://github.com/BerriAI/litellm) — OFFICIAL. Proxy server, 100+ providers, cost tracking.
[^litellm-routing]: [Routing & Load Balancing — liteLLM Docs](https://docs.litellm.ai/docs/routing-load-balancing) — OFFICIAL. Ordered fallbacks, retries, cooldowns, tag-based / budget / health-check routing.
[^litellm-cc]: [Claude Code Quickstart — liteLLM Docs](https://docs.litellm.ai/docs/tutorials/claude_responses_api) — OFFICIAL.
[^litellm-non-anth]: [Use Claude Code with Non-Anthropic Models — liteLLM Docs](https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models) — OFFICIAL.
[^helicone-portkey]: [Helicone vs Portkey — TrueFoundry](https://www.truefoundry.com/blog/helicone-vs-portkey) — PRAC, 2026.
[^gateway-compare]: [LLM Gateway Comparison 2026 — RelayPlane](https://relayplane.com/blog/llm-gateway-comparison-2026) and [Buyer's Guide to Pick the Best LLM Gateway in 2026](https://dev.to/pranay_batta/buyers-guide-to-pick-the-best-llm-gateway-in-2026-1epa) — PRAC, 2026.
[^tetrate]: [Goose with Tetrate Agent Router Service](https://tetrate.io/blog/frictionless-setup-of-goose-with-tetrate-agent-router-service) — PRAC, 2026.
[^infra-compared]: [AI Inference API Providers Compared (2026) — Infrabase](https://infrabase.ai/blog/ai-inference-api-providers-compared) — PRAC, 2026. Throughput / TTFT numbers for Groq, Fireworks, Cerebras, Together.
[^arbitrage]: [The Token Arbitrage: Groq vs DeepInfra vs Cerebras vs Fireworks vs Hyperbolic (2025)](https://blog.gopenai.com/the-token-arbitrage-groq-vs-deepinfra-vs-cerebras-vs-fireworks-vs-hyperbolic-2025-benchmark-ccd3c2720cc8) — PRAC. Slightly older but still cited.
[^cerebras-cs3]: [Cerebras CS-3 vs. Groq LPU](https://www.cerebras.ai/blog/cerebras-cs-3-vs-groq-lpu) — OFFICIAL (vendor-reported) — treat with caution.
[^cerebras-qwen3]: [Qwen3 Coder 480B is Live on Cerebras](https://www.cerebras.ai/blog/qwen3-coder-480b-is-live-on-cerebras) — OFFICIAL. 2,000 tok/s, $2/MTok, #2 on OpenRouter coding leaderboard within 2 weeks.
[^cerebras-cline]: [Cerebras — Cline Docs](https://docs.cline.bot/provider-config/cerebras) — OFFICIAL.
[^biggo-cerebras]: [Qwen3 Coder 480B Speed vs Latency Trade-offs — BigGo](https://biggo.com/news/202508030143_Qwen3_Coder_480B_Speed_vs_Latency_Trade-offs) — PRAC.
[^novita-forge]: [How to Use Novita AI API in ForgeCode — Novita](https://blogs.novita.ai/use-novita-ai-api-in-forgecode/) — PRAC, 2026.
[^forge-custom]: [Custom Providers — ForgeCode Docs](https://forgecode.dev/docs/custom-providers/) — OFFICIAL. `.forge.toml`, `[[providers]]`, `[session]`, per-agent YAML.
[^goose-providers]: [Configure LLM Provider — Goose Docs](https://goose-docs.ai/docs/getting-started/providers/) — OFFICIAL. 40+ providers, OpenRouter browser-auth flow, Ollama/LM Studio/vLLM, prompt caching auto-enable.
[^opencode-providers]: [Providers — OpenCode Docs](https://opencode.ai/docs/providers/) — OFFICIAL. 75+ providers via AI SDK + Models.dev, `small_model`, `{env:VAR}` interpolation.
[^opencode-transforms]: [Provider Transformations — DeepWiki (sst/opencode)](https://deepwiki.com/sst/opencode/4.3-provider-transformations) — OFFICIAL-adjacent. Cache control markers, Anthropic beta headers.
[^opencode-ollama]: [OpenCode — Ollama Docs](https://docs.ollama.com/integrations/opencode) and [Optimizing Local LLM Context for Agentic Coding with Ollama and OpenCode](https://tkamucheka.github.io/blog/2026/02/15/opencode-ollama-integration/) — PRAC, 2026. 4096-token context trap.
[^qwen-providers]: [Model Providers — Qwen Code Docs](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/model-providers/) — OFFICIAL. `modelProviders`, `envKey`, `generationConfig` impermeable layer, `/model` picker.
[^kilo-or]: [Using OpenRouter With Kilo Code](https://kilo.ai/docs/providers/openrouter) — OFFICIAL.
[^cline-or]: [OpenRouter — Cline Docs](https://docs.cline.bot/provider-config/openrouter) — OFFICIAL.
[^cline-issue]: [Cline issue #4371: OpenRouter Provider Selection and Routing](https://github.com/cline/cline/issues/4371) and [Discussion #1076: Provider preference for openrouter](https://github.com/cline/cline/discussions/1076) — OFFICIAL, open gaps.
[^aider-or]: [OpenRouter — Aider Docs](https://aider.chat/docs/llms/openrouter.html) — OFFICIAL. `--model openrouter/...`, `.aider.model.settings.yml`.
[^aider-config]: [Advanced Model Settings — Aider Docs](https://aider.chat/docs/config/adv-model-settings.html) — OFFICIAL. `--weak-model`, `--editor-model`, `extra_params`.
[^aider-deepwiki]: [Model Configuration and Capabilities — DeepWiki (Aider-AI/aider)](https://deepwiki.com/Aider-AI/aider/7-model-configuration-and-capabilities) — OFFICIAL-adjacent. LiteLLM is Aider's model layer.
[^aider-leaderboard]: [Aider Polyglot Leaderboard](https://aider.chat/docs/leaderboards/) — OFFICIAL, last refreshed Nov 20 2025.
[^qwen-polyglot-gh]: [Improve aider polyglot benchmark — QwenLM/Qwen3 Discussion #1139](https://github.com/QwenLM/Qwen3/discussions/1139) — OFFICIAL. Qwen2.5-Coder-32B at 8% on current polyglot (vs 73.7 on older variant).
[^cc-subagents]: [Create custom subagents — Claude Code Docs](https://code.claude.com/docs/en/sub-agents) — OFFICIAL. `model:` field, `CLAUDE_CODE_SUBAGENT_MODEL`, Haiku-default Explore subagent, cost-control framing.
[^morph-coding]: [Best LLM for Coding (2026) — Morph](https://www.morphllm.com/best-llm-for-coding) — PRAC, 2026. Sonnet 4.6 at ~95% Opus quality / 60% cost.
[^morph-aider]: [Aider Uses 4.2x Fewer Tokens Than Claude Code — Morph](https://www.morphllm.com/comparisons/morph-vs-aider-diff) — PRAC, 2026.
[^ollama-opencode]: [OpenCode — Ollama Integration Docs](https://docs.ollama.com/integrations/opencode) — OFFICIAL.
[^ollama-launch]: [Running AI Coding Agents Locally with Ollama Launch (Jan 2026)](https://atalupadhyay.wordpress.com/2026/01/27/running-ai-coding-agents-locally-with-ollama-launch/) — PRAC.
[^hn-arbitrage]: [Cerebras launches Qwen3-235B, achieving 1.5k tokens per second — HN](https://news.ycombinator.com/item?id=44657727) — PRAC community discussion.
[^free-guide]: [Every Free AI API in 2026 — AwesomeAgents](https://awesomeagents.ai/tools/free-ai-inference-providers-2026/) — PRAC, 2026.
