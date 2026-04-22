---
content_origin: claude-code-orchestrator-followup
date: 2026-04-21
topic: "ForgeCode and agentic tooling evaluation for Momentum"
purpose: "Post-synthesis follow-up — scope omission correction (JetBrains Air/Junie), standalone descriptions of Goose and OpenCode, and integration/licensing reality between these tools and Claude Code"
supplements: final/forgecode-agentic-tools-eval-final-2026-04-21.md
---

# Follow-Up Note — JetBrains, Integration, and Licensing

This note supplements the final research report with three items the initial scope missed or under-treated:

1. **JetBrains Air and Junie** — omitted from scope.md sub-questions despite being part of the developer's original framing
2. **Goose and OpenCode described standalone** — the main report framed them mostly against Claude Code; this restates each in its own terms
3. **Integration and licensing** — can Goose or OpenCode use a Claude Pro/Max subscription? Can either integrate *with* Claude Code? The answers materially changed in February–April 2026

---

## 1. Scope Omission — JetBrains Air and Junie

The developer's original framing explicitly mentioned researching JetBrains Air alongside OpenCode, Qwen, and Kilo. The scope.md sub-questions passed to the research subagents did not include JetBrains tooling. Recovering that thread below.

### JetBrains Air — an Agentic Development Environment (ADE)

**Origin.** Public preview launched March 2026. Built on the **abandoned Fleet IDE codebase** — JetBrains recycled the Fleet architecture rather than retire it ([The Register coverage](https://www.theregister.com/2026/03/10/jetbrains_previews_air_proclaims_new/)) [CITED]. Currently macOS-only; Windows/Linux in progress.

**Critical distinction — Air is not itself an agent.** It is an **orchestration shell** that wraps OTHER agents as subordinate workers. Officially supported: **Claude Agent, OpenAI Codex, Gemini CLI, and Junie** ([Supported Agents docs](https://www.jetbrains.com/help/air/supported-agents.html)) [VERIFIED]. The developer BYOKs their Anthropic key and Air drives Claude Code. Notable ToS caveat in the docs: *"Authentication with Claude Pro/Max/Team plans is not permitted by Anthropic Terms of Service"* — API billing only.

**Design philosophy** (quoted from the Air blog): *"IDEs add tools to the code editor, while Air builds tools around the agent."* Task-dispatch UI with code editor as one of several surfaces. Symbol-precise context: mention a specific line, commit, class, method, or other symbol when defining a task — the agent gets structured context rather than pasted blobs.

**Execution model.** Agents run locally by default, or isolated in **Docker containers and Git worktrees for sandboxing and concurrent work** ([Air Launches blog](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/)) [VERIFIED]. Structurally close to Momentum's worktree-per-story pattern.

**ACP — Agent Client Protocol.** Air supports ACP, the same protocol Goose uses for subscription passthrough. An **ACP Agent Registry** is planned to allow any ACP-speaking agent to plug in ([ADTmag coverage](https://adtmag.com/articles/2026/03/19/jetbrains-launches-air-preview-for-developers-managing-multiple-ai-agents.aspx)) [CITED].

**Why this matters for Momentum.** Air is the mainstream IDE vendor's bet that **multi-agent orchestration is the product category**, not AI-assistant-in-editor. Directly the shape Momentum assumed from day one. Air could host Momentum *on top of Claude Agent* — JetBrains-native worktree/Docker isolation, agent parallelism, symbol-precise context, while Momentum's skills and rules continue driving Claude Code underneath. Alternative form factor to terminal-first (BMAD, CMUX), worth experimenting with if the developer is already JetBrains-fluent.

### Junie / Junie CLI

**Origin.** JetBrains' native agentic coding agent, v1 launched 2025. **Junie CLI** went beta March 2026 as a standalone, LLM-agnostic agent that runs in terminals, any IDE, CI/CD, and GitHub/GitLab integrations ([Junie CLI beta announcement](https://blog.jetbrains.com/junie/2026/03/junie-cli-the-llm-agnostic-coding-agent-is-now-in-beta/)) [VERIFIED].

**Model flexibility.** Quoted from the beta announcement: *"all the top-performing models from OpenAI, Anthropic, Google, and Grok"* — BYOK or JetBrains AI subscription.

**Extension surface** (direct quote): *"guidelines, custom agents and agent skills, commands, MCP, and other agent configuration methods."* MCP-native.

**Key detail — `.junie/skills/` directory.** JetBrains formally adopted **Anthropic's Agent Skills open standard**, with Junie loading skills from `.junie/skills/` ([Kotlin AI Stack blog](https://blog.jetbrains.com/kotlin/2025/09/the-kotlin-ai-stack-build-ai-agents-with-koog-code-smarter-with-junie-and-more/)) [VERIFIED]. Same `.xxx/skills/<name>/SKILL.md` convention the rest of the market converged on — Momentum's core authoring format is portable to Junie with zero rework.

**Koog** (separate JetBrains product, context worth knowing). Kotlin/Java SDK for **building** AI agents — structured, observable, fault-tolerant agent workflows. Think "LangGraph for the JVM." Not directly Momentum-relevant unless Momentum ever ships JVM-native agents.

### Verdict for Momentum (JetBrains column)

- **Junie CLI as co-processor:** Viable for teams that want a JetBrains-blessed agent; adopts SKILL.md standard so Momentum skills port with zero rework.
- **Air as host:** Structurally compelling — multi-agent orchestration + worktree isolation match Momentum's conventions. Could run Momentum's Claude Code session *inside* Air to gain JetBrains-native worktree UI and agent parallelism.
- **Risk:** JetBrains' track record with new IDEs (Fleet) is mixed — Air is the Fleet codebase resurrected. Commercial model not fully clear yet.

**Recommendation:** Treat Air as a **form-factor experiment** rather than a peer agent. If testing "can Momentum run on Cursor?", the parallel question is "can Momentum run inside Air, driving Claude Code as its Air-managed agent?" Likely yes, and preserves everything Momentum already does.

---

## 2. Goose and OpenCode — Standalone Descriptions

The main report framed Goose and OpenCode primarily against Claude Code. Restating each in its own terms.

### Goose — the enterprise-governance option from Block

**Origin.** Announced by **Block** (parent of Square and Cash App) in January 2025 as their internal agentic coding framework, then open-sourced ([Block Open Source announcement](https://block.xyz/inside/block-open-source-introduces-codename-goose)) [VERIFIED]. December 2025: Block contributed Goose to the **Linux Foundation Agentic AI Foundation (AAIF)** alongside the MCP specification and the AGENTS.md standard. AAIF now has 170+ member organizations including AWS, Anthropic, Bloomberg, Cloudflare, Google, Microsoft, and OpenAI.

**Surfaces.** Three: a **CLI** (primary), a **desktop app** for non-terminal users, and an **API** for headless / server deployments. Conversational interface; Goose decides what tools to call. The model is interchangeable — Anthropic, OpenAI, Gemini, Bedrock, Ollama, or others, configured per-session or globally. **There is no "Goose model"** — Goose is the loop, the tools, the memory, and the extension system. The underlying AI is BYOK.

**The Recipe system — Goose's defining primitive.** A Recipe is a YAML file capturing a reusable workflow: parameters, steps, which extensions to load, which sub-recipes to compose in. Jinja2-templated, composable:

```yaml
name: database-migration
parameters:
  - schema_version
extensions: [postgres-mcp, github]
sub_recipes:
  - name: generate-migration
    path: ./subrecipes/generate.yaml
    values: {target_version: "{{ schema_version }}"}
  - name: verify-migration
    path: ./subrecipes/verify.yaml
```

Recipes are first-class artifacts: shared across teams, versioned in git, tested, composed. The community maintains a Recipe Marketplace catalog of production recipes for common tasks.

**Extensions and MCP.** Deepest MCP ecosystem in the market: 70+ first-party extensions, 3,000+ community servers via the AAIF extension catalog. Extensions are MCP servers, so writing one is writing a standard MCP server — portable across any MCP host.

**ACP — Agent Client Protocol.** Goose pioneered **subscription passthrough** — instead of paying for API access, Goose can drive a model through a browser-authenticated subscription session. Works for ChatGPT Plus and Gemini Advanced ([ACP Providers docs](https://goose-docs.ai/docs/guides/acp-providers/)) [VERIFIED]. **Claude Pro/Max passthrough is blocked** — see §3 below.

**Local-model-first.** First-class Ollama, Docker Model Runner, Ramalama integration. Many recipes run entirely local, giving Goose a "sovereign operation" lane with no cloud API involved. This is Block's compliance story.

**Security posture.** January 2026 red-team exercise "Operation Pale Fire" successfully compromised Goose via a poisoned Recipe hiding malicious instructions in invisible Unicode. Block patched it, published a post-mortem, and hardened the Recipe loader ([effloow.com post-mortem coverage](https://effloow.com/articles/goose-open-source-ai-agent-review-2026)) [CITED]. Transparency positive; reminder that the recipe/extension ecosystem is a prompt-injection attack surface.

**Who uses Goose.** Block internally (primary user base). Enterprise teams that need the AAIF governance story. Teams that prefer local models or multi-vendor model choice. Desktop-app users who do not want a terminal-first workflow. Recipe-library-oriented teams that codify common ops as executable artifacts.

**In one sentence.** Goose is an AAIF-governed, recipe-driven, BYOK/subscription agent framework with the broadest MCP ecosystem and the strongest multi-corp governance in the space — optimized for teams who want portable, versioned, shareable workflows and do not care whose model sits underneath.

### OpenCode — the developer-velocity option from the SST team

**Origin.** **Anomaly Innovations** (formerly SST — Serverless Stack Toolkit, a well-known TypeScript infrastructure framework). Profitable company, not VC-backed in the conventional sense. First release mid-2025; 147K GitHub stars and ~3 releases per day as of April 2026 — **the highest velocity of any tool in the space**.

**Surfaces.** TUI (terminal user interface) — keyboard-driven, vim-influenced, split panes. Also a beta desktop app and a mobile-drive mode (control OpenCode from your phone). The architectural distinguishing feature: **client/server split** — the OpenCode daemon runs separately from the UI, so it can be driven headlessly from scripts, CI, or mobile. Most peers couple UI and agent; OpenCode deliberately separates them.

**Agents and subagents.** Two built-in agent modes: `build` (execution) and `plan` (read-only analysis), plus a `@general` subagent invoked inline. **Multiple sessions in parallel** — each with its own model, tool allowlist, and context. Useful when one agent refactors while another runs tests.

**Configuration — the portability hack.** `opencode.json` defines providers, models, agents, permissions. The clever bit: **OpenCode reads `.claude/skills/*/SKILL.md` and `CLAUDE.md` as configuration fallbacks**. An existing Claude Code project can be pointed at OpenCode and 80% of the rules and skills just work, unmodified. Intentional — SST's team is explicit that OpenCode is the "escape hatch" from Claude-specific lock-in without demanding a practice rewrite.

**Plugin system.** **25+ lifecycle events** through TypeScript/JavaScript plugins: `session.*` (including `session.compacting` pre-compaction), `tool.execute.before/after`, `file.edited`, `permission.asked`, `message.part.*`, `tui.prompt.append`, `shell.env` ([OpenCode Plugins docs](https://opencode.ai/docs/plugins/)) [VERIFIED]. Richest plugin surface in the set.

**Model flexibility.** 75+ providers via Models.dev integration. Different models per-role: `main` vs `small_model` (cheap fast model for summaries/decisions) vs per-agent configuration.

**Community and vibe.** Fast-moving open-source project — Discord, daily releases, PRs merged in hours. Kelsey Hightower publicly documented migrating 12 agents from Claude Code to OpenCode in a single afternoon ([gist](https://gist.github.com/RichardHightower/827c4b655f894a1dd2d14b15be6a33c0)) [CITED]. Community plugins for hook compatibility (`oh-my-opencode`) bridge Claude Code's hook surface to OpenCode's plugin events.

**Who uses OpenCode.** TypeScript/JavaScript developers. Teams driving agents from scripts/CI/mobile rather than just a terminal. Teams escaping Claude Code lock-in without losing practice investment. Developers who value rapid iteration and rich plugin ecosystems over stability.

**In one sentence.** OpenCode is a TUI-first, client/server-architected agentic coding tool with the richest TS/JS plugin ecosystem in the market and a deliberate backdoor that lets Claude Code projects run on it with minimal porting — optimized for developer velocity and escape-hatch portability.

### Three different bets on the same market

- **JetBrains Air** bets on orchestration-as-product: "developers manage multiple agents; we build the IDE for that." Wraps competitors as subordinate workers. JetBrains-native form factor.
- **Goose** bets on governance and portability: "agents are commodity; workflows are the asset. Make workflows (recipes) a versionable, shareable, composable artifact under a neutral foundation."
- **OpenCode** bets on developer velocity and escape-hatch portability: "Claude Code is fine but you shouldn't be locked in. Here's a richer plugin system, a client/server architecture, and we will read your existing config — move when you want."

---

## 3. Licensing and Integration — Can These Tools Use Claude Pro/Max? Can They Integrate With Claude Code?

### 3.1 Licensing reality (material change February–April 2026)

**Short answer: NO — as of April 2026, neither Goose nor OpenCode can legitimately use a Claude Pro/Max subscription.** Anthropic formally prohibited third-party tool use of subscription OAuth tokens in February 2026 and enforced it in April 2026.

**Timeline:**
- **February 20, 2026:** Anthropic updated the Consumer Terms of Service, adding an explicit *"Authentication and credential use"* section. Using OAuth tokens obtained through Claude Free, Pro, or Max accounts in any other product, tool, or service — **including the Agent SDK** — is not permitted. OAuth authentication is stated to be intended **only for Claude Code and Claude.ai** ([Anthropic news](https://www.anthropic.com/news/updates-to-our-consumer-terms), [The Register coverage](https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access/)) [VERIFIED].
- **April 4, 2026:** Enforcement began. Anthropic provided a one-time credit equal to the monthly subscription value to ease the transition ([VentureBeat coverage](https://venturebeat.com/technology/anthropic-cuts-off-the-ability-to-use-claude-subscriptions-with-openclaw-and)) [CITED].
- **April 17, 2026:** Transition compensation credit expired.
- **Today (2026-04-21):** Third-party tools using Claude OAuth tokens receive an explicit error: *"This credential is only authorized for use with Claude Code and can't be used for other API requests"* ([openclaw issue #53456](https://github.com/openclaw/openclaw/issues/53456)) [CITED].

**Tool-by-tool status:**

| Tool | Claude Pro/Max subscription passthrough | API key (BYOK) | Subscription passthrough for other models |
|---|---|---|---|
| **Goose** | **Blocked** (Feb 2026 ToS). [aaif-goose/goose#3647](https://github.com/block/goose/issues/3647) tracks this as a known limitation. | Supported (ANTHROPIC_API_KEY) | Works for ChatGPT Plus and Gemini Advanced via ACP |
| **OpenCode** | **Blocked** (Feb 2026 ToS). OpenCode's project leads received a formal legal request from Anthropic and removed OAuth support; the OAuth path now redirects users to OpenAI, GitHub, or GitLab as alternatives. | Supported | Works for other providers |
| **JetBrains Air** | Explicitly blocked in the Air documentation: *"Authentication with Claude Pro/Max/Team plans is not permitted by Anthropic Terms of Service"* | Supported | N/A (Air is an orchestration shell) |

**Community workarounds exist but violate ToS.** Within days of the April 2026 enforcement, developers published `opencode-claude-auth`, `opencode-anthropic-oauth`, and routing proxies ([griffinmartin/opencode-claude-auth](https://github.com/griffinmartin/opencode-claude-auth), [ex-machina-co/opencode-anthropic-auth](https://github.com/ex-machina-co/opencode-anthropic-auth), [ianjwhite99/opencode-with-claude](https://github.com/ianjwhite99/opencode-with-claude)) [CITED]. These **explicitly violate Anthropic's ToS** and are a ticking clock: Anthropic's enforcement infrastructure is active and the credentials are scoped/tagged. Do not rely on these for production Momentum usage.

**Practical implication for Momentum.**
- To run Goose, OpenCode, or Air **using Claude models**, pay for API-key-billed access (pay-per-token) in addition to any Claude Pro/Max subscription used with Claude Code directly.
- **OR** run Goose / OpenCode / Air on **non-Anthropic models** (OpenAI, Gemini, DeepSeek, Qwen on OpenRouter, Cerebras, local Ollama) and keep Claude Code on the Claude subscription for the primary driver role.
- The OpenRouter "Anthropic Skin" base URL (`https://openrouter.ai/api/anthropic`) accepts an API key — this works for both Claude Code (via `ANTHROPIC_BASE_URL`) and OpenCode/Goose, but it is **API-key billing, not subscription passthrough**.

### 3.2 Integration with Claude Code — both directions

**Claude Code → OpenCode (Claude Code calls OpenCode as a subagent).** Yes, via MCP.

- **opencode-mcp** ([Traves-Theberge/opencode-mcp](https://github.com/Traves-Theberge/opencode-mcp)) [CITED] — an MCP server that **exposes OpenCode as a tool/subagent for any MCP-compatible client**, including Claude Code. From Claude Code's perspective, OpenCode becomes a callable tool that handles: code implementation and refactoring, file operations and search, code analysis and planning, multi-turn coding sessions, and agent delegation.
- **Mechanism:** Claude Code talks MCP → opencode-mcp server → OpenCode daemon → OpenCode executes with its own model/context/plugins → result returns up the chain.
- **Momentum application:** Wrap `opencode-mcp` in a `momentum:*` skill (e.g., `momentum:bulk-refactor` or `momentum:parallel-review`) so Claude Code can dispatch specific sub-tasks to OpenCode running cheaper models via OpenRouter, while Claude Code stays on Opus for orchestration and review. Sandbox in a sibling git worktree.

**Claude Code → Goose (Claude Code calls Goose as a subagent).** Yes, via MCP or the HTTP API.

- **AgentAPI** ([coder/agentapi](https://github.com/coder/agentapi)) [CITED] — HTTP API wrapper for Claude Code, Goose, Aider, Gemini, Amp, and Codex. Lets any of them be driven programmatically. Can be used as the backend of an MCP server exposing Goose as a callable tool.
- Goose has first-class MCP support, so exposing it or being driven by it is idiomatic. No known pre-built `goose-mcp` server as of this research date, but Goose's HTTP API (`goose serve`) plus AgentAPI as a wrapper provides the functional equivalent.
- **Momentum application:** A `momentum:recipe-run` skill that invokes a specific Goose Recipe via AgentAPI or the HTTP endpoint. Good fit for discrete, repeatable workflows (schema migrations, scaffolds, changelog generation) where Goose's Recipe marketplace already has a battle-tested recipe.

**Goose → Claude Code (Goose calls Claude Code as a tool).** Theoretically yes via MCP, but not a common pattern.

- Goose is MCP-native, so it could in principle call a Claude-Code-exposed MCP endpoint. Claude Code itself does not natively expose its skills/agents as MCP servers, but `@coder/agentapi` wraps Claude Code and turns it into an HTTP service.
- **Less common in practice** because Goose and Claude Code target overlapping orchestration roles. More typical: Goose uses its own model backend (including Claude via API key if billed through a proxy) rather than calling Claude Code as a service.

**OpenCode → Claude Code (OpenCode calls Claude Code as a tool).** Not a mainstream pattern, but mechanically possible.

- OpenCode reads `.claude/skills/` natively, so the typical integration is the *reverse*: migrate the Momentum practice onto OpenCode directly (either as a specialist lane or as a parallel track). No wrapper needed.
- If ever needed: AgentAPI could wrap Claude Code into an HTTP endpoint, and an OpenCode plugin could call it. But this is architecturally awkward — both tools want to be the orchestrator.

**JetBrains Air and Claude Code.** Air's entire design **is** to drive Claude Code (and Codex/Gemini CLI/Junie) as its subordinate agent. The integration is first-class via Air's Claude Agent connector. Constraint: API-key billing only (no Claude Pro/Max passthrough per ToS).

### 3.3 Momentum-specific integration recommendations

**Pathway A: OpenCode as MCP-exposed specialist (lowest risk).** Install `opencode-mcp`. Wrap it in a Momentum skill. Route bulk-edit and refactor sub-tasks to OpenCode running DeepSeek-V3 or Qwen3-Coder via OpenRouter. Claude Code remains primary, Momentum skills and hooks unchanged. Effort: ~3–5 days. Cost lever: substantial for routine coding.

**Pathway B: Goose as MCP-exposed recipe runner.** Install AgentAPI wrapper around Goose. Expose specific curated recipes as Momentum skills (`momentum:migrate-schema`, `momentum:generate-changelog`). Gains access to Goose's 3,000-extension ecosystem and local-model lanes. Effort: ~5–10 days depending on recipe library curation. Governance bonus: AAIF stewardship.

**Pathway C: Air as alternative form factor.** Install Air (macOS). Configure it to drive Claude Code with the developer's Anthropic API key. Retain Momentum's existing `.claude/` directory — Claude Code inside Air still sees it. Gains JetBrains-native worktree/Docker UI and multi-agent parallelism at the host level. Effort: ~1 day to set up; ongoing: form-factor adaptation.

**Not recommended:** Relying on any third-party OAuth workaround for Claude Pro/Max subscription passthrough. ToS violation, enforcement active, credentials tagged. Budget for API billing separately if running Goose/OpenCode on Claude models, or route those tools to non-Anthropic models (DeepSeek, Qwen, Gemini, local Ollama) to avoid the double-pay problem.

## Sources

- [JetBrains Air — Launches announcement](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/) [VERIFIED]
- [JetBrains Air — Supported Agents](https://www.jetbrains.com/help/air/supported-agents.html) [VERIFIED]
- [JetBrains Air — Quick Start](https://www.jetbrains.com/help/air/quick-start-with-air.html) [VERIFIED]
- [The Register — JetBrains Air on Fleet](https://www.theregister.com/2026/03/10/jetbrains_previews_air_proclaims_new/) [CITED]
- [ADTmag — Air multi-agent preview](https://adtmag.com/articles/2026/03/19/jetbrains-launches-air-preview-for-developers-managing-multiple-ai-agents.aspx) [CITED]
- [Junie CLI beta announcement](https://blog.jetbrains.com/junie/2026/03/junie-cli-the-llm-agnostic-coding-agent-is-now-in-beta/) [VERIFIED]
- [JetBrains Junie product page](https://www.jetbrains.com/junie/) [VERIFIED]
- [Kotlin AI Stack — Koog, Junie, Agent Skills](https://blog.jetbrains.com/kotlin/2025/09/the-kotlin-ai-stack-build-ai-agents-with-koog-code-smarter-with-junie-and-more/) [VERIFIED]
- [InfoWorld — JetBrains launches Air and Junie CLI](https://www.infoworld.com/article/4142675/jetbrains-launches-air-and-junie-cli-for-ai-assisted-development/) [CITED]
- [Block — Goose open-source announcement](https://block.xyz/inside/block-open-source-introduces-codename-goose) [VERIFIED]
- [Goose — ACP Providers docs](https://goose-docs.ai/docs/guides/acp-providers/) [VERIFIED]
- [Goose GitHub issue #3647 — Claude OAuth for subscription users](https://github.com/block/goose/issues/3647) [CITED]
- [sst/opencode — canonical repo](https://github.com/sst/opencode) [VERIFIED]
- [OpenCode plugins docs](https://opencode.ai/docs/plugins/) [VERIFIED]
- [Anthropic — Consumer Terms update](https://www.anthropic.com/news/updates-to-our-consumer-terms) [VERIFIED]
- [The Register — Anthropic clarifies third-party Claude ban](https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access/) [CITED]
- [VentureBeat — Anthropic cuts off third-party tool subscription access](https://venturebeat.com/technology/anthropic-cuts-off-the-ability-to-use-claude-subscriptions-with-openclaw-and) [CITED]
- [openclaw issue #53456 — claude-agent-acp error](https://github.com/openclaw/openclaw/issues/53456) [CITED]
- [Traves-Theberge/opencode-mcp — OpenCode as an MCP server](https://github.com/Traves-Theberge/opencode-mcp) [CITED]
- [coder/agentapi — HTTP API wrapper for agents](https://github.com/coder/agentapi) [CITED]
- [RichardHightower gist — Claude Code Agents → OpenCode Agents migration](https://gist.github.com/RichardHightower/827c4b655f894a1dd2d14b15be6a33c0) [CITED]
- [griffinmartin/opencode-claude-auth](https://github.com/griffinmartin/opencode-claude-auth) [CITED — community workaround, ToS-violating]
- [ianjwhite99/opencode-with-claude](https://github.com/ianjwhite99/opencode-with-claude) [CITED — community workaround, ToS-violating]
