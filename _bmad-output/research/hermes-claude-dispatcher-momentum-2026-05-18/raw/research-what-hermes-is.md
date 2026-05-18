---
content_origin: claude-code-subagent
date: 2026-05-18
sub_question: "What is Hermes (Nous Research's agent) — runtime architecture, models, local-vs-hosted deployment, 24/7 autonomy model, license, and cost?"
topic: "Can Hermes run as a 24/7 dispatcher/delegate with Claude Code as planner/brains, and can Hermes Kanban + worker lanes map onto Momentum?"
---

# What Hermes Is — Runtime, Models, Deployment, Autonomy, License, Cost

> **Scope note:** This document extends the prior-art Kanban discovery (`docs/research/hermes-kanban-discovery-2026-05-17.md`), which covers the Kanban coordination primitive in depth. This file deliberately does *not* re-derive Kanban; it answers the orthogonal question — what the Hermes *runtime* is, how it executes models, where it can run, how it stays alive 24/7, its safety/autonomy model, license, and cost — so the larger Hermes-as-delegate-vs-Claude-native decision can be made on grounded facts.

## 1. Two Different Things Named "Hermes" (the critical disambiguation)

There are two distinct Nous Research products that share the "Hermes" name, and conflating them is the single biggest source of confusion in the downstream decision:

- **Hermes 4** — an **open-weight LLM family** released **August 2025**: Llama-3.1-based fine-tunes in 14B / 70B / 405B sizes, with hybrid `<think>` reasoning (the model decides whether to emit an explicit chain-of-thought trace based on query complexity) and neutrally-aligned (low-refusal) post-training ([Ertas AI](https://www.ertas.ai/blog/hermes-agent-vs-hermes-4); [Hermes 4 site](https://hermes4.nousresearch.com/)) [UNVERIFIED — secondary; model-card not fetched]. This is a *model you run*, not a runtime.
- **Hermes Agent** — a **self-hosted agent runtime** released **2026**: a long-lived process with persistent memory, autonomous skill creation, scheduled automations, cross-channel messaging, and a learning loop ([hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/)) [OFFICIAL]. This is the *product* the Momentum decision is about.

The relationship: Hermes Agent is **model-agnostic** and can run on top of Hermes 4 *or* any other model (Claude, GPT, Qwen, local Llama, etc.). "You use Hermes Agent when you want self-improving agent behavior — typically with Hermes 4 or another base model underneath" ([Ertas AI](https://www.ertas.ai/blog/hermes-agent-vs-hermes-4)) [UNVERIFIED — secondary]. **Everything below refers to Hermes Agent (the product) unless explicitly stated otherwise.**

## 2. Runtime Architecture

Hermes Agent uses a deliberate **three-tier architecture** with a single shared agent core ([Architecture docs](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)) [OFFICIAL]:

1. **Entry points** — `cli.py` (interactive/headless CLI), `gateway/run.py` (the long-running messaging daemon), an ACP adapter, and a batch runner. Platform differences live here, not in the core.
2. **Agent core** — a single `AIAgent` class (`run_agent.py`) implementing a **synchronous orchestration loop**: prompt construction → provider resolution → API call → tool dispatch → retries/fallbacks → callbacks → context compression → persistence. The documented path is: `User input → HermesCLI.process_input() → AIAgent.run_conversation() → prompt_builder.build_system_prompt() → runtime_provider.resolve_runtime_provider() → API call → tool_calls? → model_tools.handle_function_call() → loop → final response` ([Architecture docs](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)) [OFFICIAL].
3. **Subsystems** — a centralized tool registry (`tools/registry.py`, **70+ tools across 28 toolsets**, self-registering at import), session storage (SQLite + FTS5), provider resolution, and a plugin system ([Architecture docs](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)) [OFFICIAL].

**Stated design principle:** "One AIAgent class serves CLI, gateway, ACP, batch, and API server. Platform differences live in the entry point, not the agent." ([Architecture docs](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)) [OFFICIAL]

**Model invocation modes:** the core supports three API shapes — `chat_completions`, `codex_responses`, and `anthropic_messages` — so it speaks OpenAI-style, Codex-style, *and* native Anthropic Messages API. Provider resolution maps a `(provider, model)` tuple to credentials/endpoint; a failed call retries or falls back to alternate providers **without rewriting the prompt** ([Architecture docs](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)) [OFFICIAL]. This is directly relevant to the larger question: Hermes can natively call Claude via `anthropic_messages`.

**Memory & skills:** skills are bundled context injected into the system prompt; memory providers are pluggable single-select subsystems set in `config.yaml`. The system prompt assembles personality data, memory files, skills, tool guidance, and model-specific instructions ([Architecture docs](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)) [OFFICIAL]. The headline differentiator is a **built-in learning loop**: Hermes converts a solved workflow into a reusable skill, then loads/applies/refines it next time a similar task appears ([i-scoop](https://www.i-scoop.eu/hermes-agent-from-nous-research/); [Architecture docs](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)) [UNVERIFIED — behavior described in secondary + official overview, not independently exercised].

**Terminal/execution backends:** terminal tools support **7 backends — local, Docker, SSH, Singularity, Modal, Daytona, Vercel Sandbox** ([GitHub README](https://github.com/nousresearch/hermes-agent); [Architecture docs](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)) [OFFICIAL]. Daytona and Modal offer **serverless persistence** — the environment hibernates when idle and "costs nearly nothing" ([Docs index](https://hermes-agent.nousresearch.com/docs/)) [OFFICIAL].

## 3. Which Models It Runs — Swappable and Local-Capable

Hermes Agent is **model-agnostic by design**. The official providers page lists **100+ AI providers**: OpenAI, Anthropic, Google Gemini, OpenRouter, GitHub Copilot, xAI/Grok, DeepSeek, Hugging Face, AWS Bedrock, Azure OpenAI, plus a large set of Chinese-lab models (Qwen, Kimi/Moonshot, MiniMax, DashScope, z.ai/GLM, Xiaomi MiMo, Tencent), and multi-provider routers (LiteLLM, OpenRouter) ([Providers docs](https://hermes-agent.nousresearch.com/docs/integrations/providers)) [OFFICIAL].

**No hard default model.** "You need at least one provider configured to use Hermes." There is no built-in default model; the user picks one via the `hermes model` wizard. OpenRouter is the *recommended* starting point for a no-local-infra multi-model experience ([Providers docs](https://hermes-agent.nousresearch.com/docs/integrations/providers)) [OFFICIAL]. Models are swapped at runtime via `hermes model` with no code changes ([GitHub README](https://github.com/nousresearch/hermes-agent)) [OFFICIAL].

**Fully local / offline models are a first-class, supported path.** Documented self-hosted options, all OpenAI-compatible: **Ollama, vLLM, SGLang, llama.cpp / llama-server, LM Studio, LocalAI, Jan** ([Providers docs](https://hermes-agent.nousresearch.com/docs/integrations/providers); [providers.md source](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md)) [OFFICIAL]. The docs are explicit: "At the agent layer, Hermes does not care whether tokens come from OpenRouter, Ollama, LM Studio, vLLM, llama.cpp, Kobold, or another OpenAI-compatible server" ([Local LLM search synthesis](https://hermes-agent.nousresearch.com/docs/integrations/providers)) [OFFICIAL]. Configuration is via `hermes model` → "Custom endpoint (self-hosted / VLLM / etc.)" → enter base URL (e.g. `http://localhost:11434/v1` for Ollama, `:8000/v1` for vLLM), or `config.yaml` with `provider: custom`, `base_url`, optional `api_key`; multiple named endpoints via `custom_providers:` ([Providers docs](https://hermes-agent.nousresearch.com/docs/integrations/providers)) [OFFICIAL].

**Hard model-capability requirements** (load-bearing for any local-only Momentum plan):

- **Native tool/function calling is mandatory.** A model that emits tool calls as JSON in response text won't be recognized — e.g., llama.cpp requires `--jinja`, vLLM requires `--enable-auto-tool-choice`, SGLang requires `--tool-call-parser` ([providers.md source](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md)) [OFFICIAL]. Models with documented native support include Qwen 2.5, Llama 3.x, Mistral, Hermes 2/3/4.
- **Context window minimum ~16k–32k tokens**, because the system prompt + tool schemas alone consume ~4k–8k. Ollama's 4k default is explicitly called out as too small for agent use ([Providers docs](https://hermes-agent.nousresearch.com/docs/integrations/providers)) [OFFICIAL].

**Conclusion for the larger decision:** Hermes Agent *can* run with zero external API (local Ollama/vLLM), satisfying the local-only preference — but only with a sufficiently capable local model that does real tool calling at ≥16–32k context. The runtime also speaks the native Anthropic Messages API, so a hybrid (Claude as the model behind Hermes) is architecturally trivial.

## 4. Deployment Modes — Hosted vs. Self-Host vs. Local

Hermes Agent is **self-hosted software, not a SaaS** — there is no hosted Hermes Agent product; Nous sells *inference* (Nous Portal), not a managed agent runtime. Deployment topology choices ([GitHub README](https://github.com/nousresearch/hermes-agent); [Installation docs](https://hermes-agent.nousresearch.com/docs/getting-started/installation); [GlobeNewswire FlyHermes](https://www.globenewswire.com/news-release/2026/05/06/3289272/0/en/flyhermes-and-hermes-agent-five-ways-to-run-the-self-improving-ai-agent-from-60-second-cloud-to-fully-local-hardware.html)) [OFFICIAL for first two]:

- **Local machine** — Linux, macOS, WSL2, Termux (Android); native Windows PowerShell in early beta. One-line bash/`irm` installer; only hard prerequisite is Git (installer pulls Python 3.11, Node.js, ripgrep, ffmpeg) ([Installation docs](https://hermes-agent.nousresearch.com/docs/getting-started/installation)) [OFFICIAL].
- **Remote / VPS** — runs on a $5 VPS up to GPU clusters; numerous third-party guides for systemd-managed VPS deployment ([dplooy](https://www.dplooy.com/blog/hermes-agent-nous-researchs-self-learning-ai-runtime); [Bluehost VPS guide](https://www.bluehost.com/blog/run-hermes-agent-vps/)) [UNVERIFIED — secondary, but consistent].
- **Serverless** — Daytona / Modal backends hibernate when idle ([Docs index](https://hermes-agent.nousresearch.com/docs/)) [OFFICIAL].
- **"Five ways to run"** — Nous's own positioning spans 60-second cloud deploy to fully local hardware (incl. NVIDIA RTX / DGX Spark partnership) ([GlobeNewswire](https://www.globenewswire.com/news-release/2026/05/06/3289272/0/en/flyhermes-and-hermes-agent-five-ways-to-run-the-self-improving-ai-agent-from-60-second-cloud-to-fully-local-hardware.html); [NVIDIA blog](https://blogs.nvidia.com/blog/rtx-ai-garage-hermes-agent-dgx-spark/)) [UNVERIFIED — press release / vendor blog].

**Data locality:** marketed as "all data stays on your machine — no telemetry, no tracking, no cloud lock-in" ([Bluehost self-hosted guide](https://www.bluehost.com/blog/hermes-agent-self-hosted/)) [UNVERIFIED — secondary]. The state stores (sessions SQLite+FTS5, Kanban SQLite, memory files) are all local to the host (consistent with prior-art §12 single-host scope) [OFFICIAL — cross-referenced].

## 5. How It Runs Continuously / 24-7

Continuous operation is the **gateway daemon** (`hermes gateway start`), a long-running process that ([Architecture docs](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture); [DeepWiki messaging gateway](https://deepwiki.com/NousResearch/hermes-agent/7-messaging-gateway)) [OFFICIAL for first; UNVERIFIED for DeepWiki]:

- Holds **20+ platform adapters** open (Telegram polling, Discord WebSocket, Slack, etc.), routes messages to per-chat/per-profile `AIAgent` instances, persists conversations to SQLite, and maintains **per-profile process locks** for safe concurrency ([Architecture docs](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)) [OFFICIAL].
- **Ticks a built-in cron scheduler**: cron jobs stored in JSON, can attach skills/scripts, delivered to any platform. Each job spins up a *fresh* `AIAgent`, injects context, and atomically updates job state ([Architecture docs](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)) [OFFICIAL]. Cron jobs "fire from inside the running gateway process" ([Bluehost VPS guide](https://www.bluehost.com/blog/run-hermes-agent-vps/)) [UNVERIFIED — secondary].
- **Embeds the Kanban dispatcher by default** (`kanban.dispatch_in_gateway: true`, 60s tick) — cross-referenced from prior-art §3, §8.1 [OFFICIAL]. So the same daemon that handles chat also drives the durable task board.

**Staying alive across logout/reboot is an OS-level concern, not built in.** Running `hermes gateway start` in a terminal stops when the session disconnects; the recommended pattern is a **systemd user service** that survives logout and auto-restarts on crash/reboot ([LumaDock systemd tutorial](https://lumadock.com/tutorials/run-hermes-agent-with-systemd); [Bluehost VPS guide](https://www.bluehost.com/blog/run-hermes-agent-vps/)) [UNVERIFIED — secondary, but multiple independent sources agree]. **Implication for Momentum:** "24/7" = a self-managed systemd/launchd service on a host you own; there is no managed uptime. On macOS (the developer's platform per the practice context) this means a `launchd` agent, which the docs/community guides cover less than the Linux/systemd path — a flagged integration gap.

## 6. Autonomy & Control Model

Hermes ships a **graduated command-approval system** plus sandboxing tiers ([Configuration docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)) [OFFICIAL]:

- **Manual mode (default)** — prompts before any flagged command (file modification, package install, network). CLI shows an interactive dialog; messaging platforms queue the request and accept `/approve` / `/deny` ([Configuration docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration); [systemd/approval search synthesis](https://www.bluehost.com/blog/run-hermes-agent-vps/)) [OFFICIAL + UNVERIFIED].
- **Smart mode** — an auxiliary LLM scores risk; auto-approves low-risk, escalates dangerous ops to a human ([Configuration docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)) [OFFICIAL].
- **Off mode** — all terminal safety checks disabled; docs explicitly warn "Only use this in trusted, sandboxed environments" ([Configuration docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)) [OFFICIAL].

**Sandboxing is the real autonomy boundary**: local backend = no isolation; Docker backend = namespace sandbox with dropped capabilities and PID limits; SSH/Modal/Daytona/Vercel = isolation to a separate machine/container ([Configuration docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)) [OFFICIAL]. For a **24/7 unattended agent**, the documented recommended posture is: `approvals.mode: smart`, Docker or remote sandbox, `agent.disabled_toolsets` to drop high-risk tools, credential-pool limits, and a website blocklist to block internal infra ([Configuration docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)) [OFFICIAL]. This pairs with the Kanban dispatcher's failure controls (circuit breaker, crash recovery, stale-claim TTL — prior-art §7) for unattended resilience [OFFICIAL — cross-referenced].

## 7. Licensing

**MIT License.** Stated consistently across the GitHub repo, the docs footer ("MIT License · 2026"), the homepage, and multiple secondary sources ([GitHub README](https://github.com/nousresearch/hermes-agent); [Docs index](https://hermes-agent.nousresearch.com/docs/)) [OFFICIAL]. Permissive, free forever, no copyleft, commercial use allowed, no per-seat or feature-gated tier — "Every Hermes Agent feature — including the learning loop, persistent memory, and multi-platform gateway — is available in the free open-source version" ([OpenClaw cost guide](https://www.getopenclaw.ai/blog/hermes-agent-cost)) [UNVERIFIED — secondary, but consistent with the MIT claim]. Note: the **Hermes 4 model weights** are governed by their own (separate) model license — out of scope here, flag if model self-hosting becomes load-bearing.

## 8. Pricing / Cost Model

**The runtime is free (MIT).** Real cost has exactly two components ([OpenClaw cost guide](https://www.getopenclaw.ai/blog/hermes-agent-cost); [Hermify cost blog](https://www.hermify.io/en/blog/how-much-does-hermes-agent-cost)) [UNVERIFIED — secondary, consistent]:

1. **Infrastructure** — where it runs. $0 if on existing local hardware; ~$5/mo small VPS; more for GPU. Total commonly cited range **$5–$80/mo** depending on VPS + model + volume [UNVERIFIED — secondary].
2. **Inference** — LLM API tokens (or $0 if a local model on your own GPU).

**Nous Portal** is Nous's optional first-party inference + bundled-tools subscription (not required to use Hermes Agent), launched ~April 27, 2026 ([KuCoin](https://www.kucoin.com/news/flash/nous-research-launches-nous-portal-subscription-platform-to-integrate-hermes-agent-workflows)) [UNVERIFIED — secondary]. Tiers: **Free ($0.10/mo credits), Plus $20, Super $100, Ultra $200**, with bonus credits on signup/upgrade (+$2/+$10/+$20). All paid tiers bundle monthly credits, 300+ models, and tools (web search, scraping, image gen, browser, code exec, voice) ([Teknium/X](https://x.com/Teknium/status/2047442402303226174); [Nous portal info](https://portal.nousresearch.com/info)) [UNVERIFIED — secondary/social, treat tier numbers as approximate]. Example model price: Hermes-4-70B on Nous Portal at **$0.05/M input, $0.20/M output**, 128k context ([pricepertoken](https://pricepertoken.com/pricing-page/model/nousresearch-hermes-4-70b)) [UNVERIFIED — secondary].

**Cost conclusion for the decision:** A local-only, cost-sensitive deployment can run Hermes Agent at **effectively $0 marginal cost** (existing Mac + local Ollama/vLLM model), or pennies-per-month inference if pointed at Claude/cheap APIs. The cost objection to Hermes-as-delegate is therefore weak; the real constraints are (a) local model tool-calling quality, (b) macOS `launchd` 24/7 self-management, and (c) the non-paved external-CLI lane integration (prior-art §5.3) — not licensing or runtime cost.

## 9. Source Freshness & Caveats

- Official docs, GitHub README, Architecture, Providers, Configuration pages: current (repo at **v0.14.0, 2026-05-16**; docs footer "2026") — **<1 month old, fresh** [OFFICIAL].
- Nous Portal tier numbers come from X/social + aggregator sites (April–May 2026) — recent but **secondary; verify exact prices in-app before relying on them**.
- "Five ways to run" and NVIDIA/DGX claims are vendor press (May 2026) — recent, promotional, **directionally reliable not spec-grade**.
- The Hermes 4 *model* details (sizes, `<think>`, license) are from secondary comparisons; the model card itself was not fetched — flagged if model self-hosting becomes the deciding factor.
- Several official doc subpaths returned 404 (`/user-guide/configuration/models`, `/features/gateway`); detail was recovered from the architecture page, the providers page, and the GitHub `website/docs` source — primary-equivalent, but exact current page URLs may have moved.

## Sources

- [Hermes Agent — Architecture (official docs)](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)
- [Hermes Agent — Documentation index (official)](https://hermes-agent.nousresearch.com/docs/)
- [Hermes Agent — Installation (official docs)](https://hermes-agent.nousresearch.com/docs/getting-started/installation)
- [Hermes Agent — AI Providers (official docs)](https://hermes-agent.nousresearch.com/docs/integrations/providers)
- [Hermes Agent — Configuration (official docs)](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
- [Hermes Agent — Homepage (official)](https://hermes-agent.nousresearch.com/)
- [NousResearch/hermes-agent — GitHub repo (official)](https://github.com/nousresearch/hermes-agent)
- [providers.md — GitHub source (official)](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md)
- [Hermes 4 — Nous Research (official)](https://hermes4.nousresearch.com/)
- [Nous Portal — info (official)](https://portal.nousresearch.com/info)
- [Hermes Agent vs Hermes 4 — Ertas AI](https://www.ertas.ai/blog/hermes-agent-vs-hermes-4)
- [Hermes Agent: Nous Research's Self-Learning AI Runtime — dplooy](https://www.dplooy.com/blog/hermes-agent-nous-researchs-self-learning-ai-runtime)
- [Hermes Agent from Nous Research — i-scoop](https://www.i-scoop.eu/hermes-agent-from-nous-research/)
- [FlyHermes — Five Ways to Run (GlobeNewswire press release)](https://www.globenewswire.com/news-release/2026/05/06/3289272/0/en/flyhermes-and-hermes-agent-five-ways-to-run-the-self-improving-ai-agent-from-60-second-cloud-to-fully-local-hardware.html)
- [Hermes Unlocks Self-Improving AI Agents (NVIDIA blog)](https://blogs.nvidia.com/blog/rtx-ai-garage-hermes-agent-dgx-spark/)
- [What is Hermes Agent: self-hosted guide — Bluehost](https://www.bluehost.com/blog/hermes-agent-self-hosted/)
- [How to Run Hermes Agent 24/7 on a VPS — Bluehost](https://www.bluehost.com/blog/run-hermes-agent-vps/)
- [Run Hermes Agent 24/7 with systemd — LumaDock](https://lumadock.com/tutorials/run-hermes-agent-with-systemd)
- [Messaging Gateway — DeepWiki](https://deepwiki.com/NousResearch/hermes-agent/7-messaging-gateway)
- [Hermes Agent Cost: Real Pricing 2026 — OpenClaw](https://www.getopenclaw.ai/blog/hermes-agent-cost)
- [How Much Does Hermes Agent Cost — Hermify](https://www.hermify.io/en/blog/how-much-does-hermes-agent-cost)
- [Nous Portal subscription tiers — Teknium/X](https://x.com/Teknium/status/2047442402303226174)
- [Nous Research launches Nous Portal — KuCoin](https://www.kucoin.com/news/flash/nous-research-launches-nous-portal-subscription-platform-to-integrate-hermes-agent-workflows)
- [Hermes-4-70B API pricing — pricepertoken](https://pricepertoken.com/pricing-page/model/nousresearch-hermes-4-70b)
