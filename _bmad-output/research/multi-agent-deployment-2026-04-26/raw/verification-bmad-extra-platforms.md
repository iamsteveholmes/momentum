---
content_origin: claude-code-subagent-verification
date: 2026-04-26
sub_question: "BMAD-supported platforms not in original scope — capability survey for Momentum interest"
topic: "Multi-agent deployment strategies for agentic engineering practice modules"
verification_targets: ["22 untouched BMAD platforms", "4 lightly-touched platforms"]
---

# BMAD-Supported Platforms Beyond Primary Scope — Capability Survey

**Scope check.** BMAD v6.5.0 (released 2026-04-26 per release notes) supports 42 platforms via [`tools/installer/ide/platform-codes.yaml`](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/tools/installer/ide/platform-codes.yaml). The v6.5.0 changeset added 18 platforms in a single drop and standardised the cross-tool `.agents/skills/` install path. [OFFICIAL]

The primary research stream covered Claude Code, OpenCode, Codex CLI, Gemini CLI, Goose, ForgeCode, Cursor, Continue, Cline, Roo Code, Aider, Cody/Amp (light), GitHub Copilot, Windsurf, Junie (light), OpenHands (light), Antigravity (light), KiloCoder (light), and Trae (light). This document examines the remaining 22 untouched platforms plus a fresh pass on Junie, Antigravity, Crush, and Sourcegraph Amp.

**Bottom line up front.** Most of the 22 are commodity forks, vendor-locked reskins, or vapor. **Five are genuinely interesting** for Momentum: Factory Droid, Kiro, Antigravity, Sourcegraph Amp, and Neovate. Two more (Mux, Pochi) demonstrate worktree-based parallel agents that mirror Momentum's own model, so they're useful for cross-checking — but offer little novel. The rest can be filed and forgotten.

---

## Tier 1 — High Interest for Momentum

These platforms expose capabilities Momentum's existing target set (Claude Code, Codex, OpenCode, Goose, ForgeCode) does not currently teach us.

### 1. Factory Droid — Hook + Sub-Droid Architecture, Enterprise Routing

- **Repo / URL:** [factory.ai](https://factory.ai) · docs at [docs.factory.ai](https://docs.factory.ai/cli/configuration/hooks-guide) · GitHub action [Factory-AI/droid-action](https://github.com/factory-ai/droid-action) [OFFICIAL]
- **Parent:** Factory AI (Khosla Ventures, $150M Series C, $1.5B valuation as of April 2026 per [tech-insider.org](https://tech-insider.org/factory-ai-150-million-series-c-khosla-coding-droids-2026/)) [PRAC]
- **OSS:** Proprietary CLI; runtime closed-source. Customer base includes Nvidia, Adobe, MongoDB, Bayer, EY, Zapier per [SiliconANGLE](https://siliconangle.com/2025/09/25/factory-unleashes-droids-software-agents-50m-fresh-funding/) [PRAC]
- **Surface:** CLI (`droid`), VS Code, JetBrains, Vim, Slack, Teams, web — multi-surface from day one
- **Hook surface:** **10 events** matching/surpassing Claude Code's core: `PreToolUse`, `PostToolUse`, `Notification`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `PreCompact`, `SessionStart`, `SessionEnd`, MCP tool ops. `SessionStart` accepts matchers `startup|resume|clear|compact` to differentiate origin — this is **richer than Claude Code's stock SessionStart** which is a single event. `PreCompact` distinguishes `manual` vs `auto` triggers, also an advance over Claude Code's coarse hook. [OFFICIAL — [Factory hooks reference](https://docs.factory.ai/reference/hooks-reference)]
- **Sub-agents:** `.factory/droids/` (project) and `~/.factory/droids/` (personal). The CLI scans these folders, validates them, and exposes them as `subagent_type` targets for the Task tool. **Identical pattern to Claude Code's sub-agents** — but with Custom Droids supported across all surfaces, not just CLI. [OFFICIAL — [Custom Droids docs](https://docs.factory.ai/cli/configuration/custom-droids)]
- **Workflow primitives:** `.droid.yaml` at repo root for project-level config; "Droid Computers" for persistent remote orchestration; integrates with Jira/Linear so an issue assignment can trigger a droid run. [OFFICIAL]
- **Model routing:** Multi-model with **on-prem routing for sensitive data**. Claude Sonnet 4.5 for quality tasks, on-prem for regulated. SOC2/GDPR, HIPAA and FedRAMP on roadmap. [PRAC — [Idlen news](https://www.idlen.io/news/factory-ai-150-million-1-5-billion-droids-coding-agents-enterprise-april-2026/)]
- **Wire protocol:** MCP supported; bespoke runtime; no public ACP claim
- **What Momentum could borrow:**
  - **Matcher specialisation on `SessionStart` and `PreCompact`** — Momentum's Impetus does different work on cold start vs resume; first-class matchers would replace ad-hoc detection.
  - **Subagent-as-folder convention** at `.factory/droids/` mirrors `.claude/agents/` exactly — confirms this is the converging industry pattern.
  - **Multi-surface deployment (CLI + IDE + chatops + ticket triggers)** — Momentum runs only in Claude Code today; Factory's surface multiplexer is worth studying for how a single skill manifest reaches all surfaces.

### 2. Kiro — Spec-Driven Mode as a First-Class Workflow Primitive

- **Repo / URL:** [kiro.dev](https://kiro.dev) · public preview · GitHub stub at [kirodotdev/Kiro](https://github.com/kirodotdev/Kiro) [OFFICIAL]
- **Parent:** AWS (built on Code OSS, runs on Amazon Bedrock) [OFFICIAL]
- **OSS:** Closed source; free during public preview; Bedrock pricing post-GA [PRAC]
- **Surface:** Forked VS Code IDE + companion CLI
- **Hook surface:** **10 distinct hook events** per [Kiro hooks/types docs](https://kiro.dev/docs/hooks/types): Prompt Submit, Agent Stop, Pre Tool Use, Post Tool Use, **File Create / File Save / File Delete (filesystem-pattern matchers built in)**, **Pre Task Execution / Post Task Execution (spec-task scoped)**, Manual Trigger. The Task-execution hooks are scoped to *spec tasks* rather than tool calls, which is **a level of workflow-awareness Claude Code's hooks don't expose**. [OFFICIAL]
- **Spec-driven dev:** Three-phase pipeline — (1) requirements in EARS notation, (2) technical design auto-generated from codebase analysis, (3) sequenced implementation tasks with dependency tracking. The IDE writes `requirements.md`, `design.md`, `tasks.md` into a `.kiro/specs/<feature>/` folder. **This is essentially the BMAD model implemented natively in an IDE.** [OFFICIAL — [DEV314 talk](https://dev.to/aws/dev-track-spotlight-spec-driven-development-with-kiro-dev314-45e8)]
- **Steering rules:** `.kiro/steering/` for path-scoped AI behaviour rules — directly comparable to Momentum's `momentum:agent-guidelines` output.
- **Model:** Claude Sonnet 4.0 / 3.7 selectable
- **Wire protocol:** MCP support; no ACP
- **What Momentum could borrow:**
  - **Pre/Post Task Execution hooks** — these fire around *spec tasks* rather than tool calls. Momentum's sprint-dev runs many implicit "task boundaries" (story start, AVFL gate, merge); a spec-task-scoped hook surface would let practice rules fire at workflow junctures rather than tool junctures.
  - **EARS-notation requirement generation** — Kiro converts NL → EARS (Easy Approach to Requirements Syntax) deterministically. Momentum's create-story injects EDD/TDD guidance but doesn't enforce a structured requirement form. EARS may be worth evaluating against Gherkin for non-test specs.
  - **`tasks.md` with dependency sequencing** — Kiro's `tasks.md` is a structured ordered task list with deps; Momentum represents this loosely in story bodies. A structural format would feed into TaskCreate/TaskList tracking better.

### 3. Google Antigravity — Verification Artifacts as a Trust Primitive

- **Repo / URL:** [antigravity.google](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/) · launched 18 Nov 2025 alongside Gemini 3 [OFFICIAL]
- **Parent:** Google
- **OSS:** Closed source; free public preview [PRAC]
- **Surface:** Standalone IDE (forked from VS Code) + Manager surface (multi-agent orchestration view)
- **Differentiator:** **Artifacts.** Agents generate verifiable deliverables — task lists, implementation plans, **screenshots and browser recordings** — alongside their code changes. The browser is a first-class tool: agent writes feature, launches app, drives browser, captures recording, attaches as proof-of-work. Walkthroughs explicitly support video clips of agent actions. [PRAC — [Index.dev review](https://www.index.dev/blog/google-antigravity-agentic-ide), [AmplifiLabs](https://www.amplifilabs.com/post/google-antigravity-review-everything-you-need-to-know-about-googles-ai-first-ide)]
- **Manager view:** Spawn, orchestrate, and observe N agents working asynchronously across workspaces — explicitly designed for **the parallel-worktree pattern Momentum uses** but elevated into a UI rather than CLI scripts.
- **Plan vs Fast modes:** Plan generates a Plan Artifact before acting; Fast executes immediately. **The Plan Artifact is editable Google-Docs-style and the agent updates the run live as you comment on it** — much closer to a true human-in-the-loop pattern than Claude Code's plan mode (which is one-shot).
- **Learning:** Agents save useful context/snippets to a knowledge base across runs.
- **Models:** Gemini 3 Pro primary; Anthropic Claude Sonnet 4.5 and OpenAI GPT-OSS supported.
- **What Momentum could borrow:**
  - **Verification artifacts as standard output of dev work.** Momentum's AVFL is rigorous on text artifacts (specs, code) but weak on UI verification. An "artifact" type for browser-recorded UI verification would close that gap. The cmux browser surface is already in play — Antigravity proves this is viable as a standard practice.
  - **Live-editable plan artifacts** rather than one-shot plan mode. Momentum's plan-audit gate runs once at ExitPlanMode; treating the plan as a living doc the developer can comment on mid-run is a richer interaction.
  - **Manager view for parallel agents** — Momentum's sprint-dev runs N stories in worktrees but visibility is split across panes. A unified Manager-style surface would make this legible.

### 4. Sourcegraph Amp — Persistent Threads as Project Memory

- **Repo / URL:** [ampcode.com](https://ampcode.com) · [Owner's Manual](https://ampcode.com/manual) · examples repo at [sourcegraph/amp-examples-and-guides](https://github.com/sourcegraph/amp-examples-and-guides) [OFFICIAL]
- **Parent:** Sourcegraph
- **OSS:** Closed-source agent runtime; AGENT.md spec is open
- **Surface:** VS Code extension + CLI
- **Differentiator:** **Persistent threads as living project memory.** Threads track coding conventions, library usage, architectural decisions, testing patterns — distinct from session memory. The `AGENT.md` file at repo root acts as a foundational context document with sections for Project Overview, Coding Standards, Tech Stack, Workflow Preferences, Context Priorities. **This is structurally what Momentum tries to achieve via `.claude/rules/` + `momentum:agent-guidelines` but Amp implements it as a single canonical artifact with first-class persistence semantics.** [PRAC — [Brendan Bohan's Top Five](https://medium.com/@brendan.bohan/hunting-for-my-next-agent-my-top-five-favorite-features-of-sourcegraph-amp-32b571f53f6f)]
- **Subagents:** Mini-Amps spawned by main agent with their own context window; results consolidated back. Standard Task-tool pattern.
- **Context engineering:** Documented at [Context Engineering - Amp.md](https://github.com/sourcegraph/amp-examples-and-guides/blob/main/guides/context-management/Context%20Engineering%20-%20Amp.md) — includes intentional context management primitives, not just defaults. [OFFICIAL]
- **What Momentum could borrow:**
  - **Persistent thread = project memory artifact** — distinct from session-scoped memory. Momentum's `.claude/projects/.../memory/MEMORY.md` is per-project but session-derived; a persistent thread that tracks decisions across sessions and is queryable by skills could replace several decision documents.
  - **AGENT.md canonical structure** — Momentum has CLAUDE.md, several rules files, several reference docs. Amp's single-document approach with named sections is more hygienic. Worth evaluating against Momentum's current sprawl.
  - **Documented context-engineering practice** — Amp publishes their context strategy as a spec. Momentum has implicit conventions; making them explicit is a win.

### 5. Neovate — Most Hookable Open-Source Agent

- **Repo / URL:** [github.com/neovateai/neovate-code](https://github.com/neovateai/neovate-code) · 1.5K stars, 152 forks, 111 releases · npm package `@neovate/code` [OFFICIAL]
- **Parent:** Neovate AI (independent OSS team) [PRAC]
- **OSS:** **Yes, fully OSS** — explicitly positions itself against Claude Code on this axis [PRAC — [neovateai.dev/overview](https://neovateai.dev/en/docs/overview)]
- **Surface:** Terminal (Ink-based React TUI) + headless quiet mode for CI/CD + desktop variant
- **Hook surface:** **23 named hooks** — counted from [neovateai.dev/plugins](https://neovateai.dev/en/docs/plugins): `agent`, `config`, `context`, `conversation`, `destroy`, `env`, `initialized`, `modelAlias`, `nodeBridgeHandler`, `outputStyle`, `provider`, `query`, `skill`, `slashCommand`, `status`, `stop`, `subagentStop`, `systemPrompt`, `telemetry`, `tool`, `toolResult`, `toolUse`, `userPrompt`. **This is the broadest extensibility surface I found across all 26 platforms surveyed.** It exceeds Claude Code's hook count and crucially exposes hooks Claude Code does not have: `provider` (modify provider map), `modelAlias` (rewrite model selection), `outputStyle` (register output styles), `systemPrompt` (modify system prompt), `nodeBridgeHandler` (extend Node bridge). [OFFICIAL]
- **Subagents:** Yes, registered via `agent` hook
- **Model support:** 15+ providers including OpenAI, Anthropic, Google, DeepSeek, xAI; auto-resolution and fallback strategies
- **What Momentum could borrow:**
  - **`systemPrompt` and `provider` hooks** are the killer features. Momentum currently cannot intercept the system prompt at runtime — rules are concatenated into context via reads. A `systemPrompt` hook would let `momentum:agent-guidelines` inject path-scoped rules dynamically rather than via static file reads.
  - **`outputStyle` hook** — Momentum has implicit output conventions (no emojis, no co-author trailer, etc.). A registered output style would make these mechanical instead of memorised.
  - **Prove out a richer hook taxonomy by example.** If Momentum ever proposes hook additions to Claude Code or builds its own harness, Neovate's 23-hook list is a reference.

---

## Tier 2 — Worth Watching

Niche relevance — capabilities partially overlap with what Momentum already has, or relevant only in specific domains.

### 6. Mux — Worktree-Per-Agent as a Product

- **Repo:** [github.com/coder/mux](https://github.com/coder/mux) · AGPL-3.0 · BYO-LLM [OFFICIAL]
- **Parent:** Coder (the Coder.com cloud-IDE company)
- **Differentiator:** Each agent runs in its own isolated workspace. **Confirms the worktree-per-agent pattern Momentum already implements is the converging industry approach** rather than an outlier choice. UX heavily inspired by Claude Code (Plan/Exec, vim inputs, /compact). Adds **opportunistic compaction and mode prompts** as novelties.
- **Borrow:** Opportunistic compaction (compact when convenient, not when forced) is a small but real UX win.

### 7. Pochi — Parallel Agents in Worktrees + ACP-First

- **URL:** [getpochi.com](https://getpochi.com) · CLI docs at [docs.getpochi.com/cli](https://docs.getpochi.com/cli/) [OFFICIAL]
- **Parent:** TabbyML (formerly Tabby autocomplete) [PRAC]
- **Differentiator:** **Parallel Agents** explicitly run each agent inside its own Git worktree per [docs.getpochi.com/parallel-agents/](https://docs.getpochi.com/parallel-agents/). Browser automation built into CLI. Skills loaded from symlinked directories — same in CLI and VS Code extension.
- **Borrow:** The skills-as-symlinked-directories pattern — single source of truth, multiple surfaces consume.

### 8. Auggie (Augment Code) — Auto Discovery of Claude Code Configs

- **Docs:** [docs.augmentcode.com/cli](https://docs.augmentcode.com/cli/overview) [OFFICIAL]
- **Differentiator:** **Auto-discovers and imports commands from Claude Code's `.claude/commands/` directory with no migration step.** This validates the "Claude Code is the de facto config standard" hypothesis Momentum has been pursuing. Hook surface is 5 events (`PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`) — narrower than Factory's 10.
- Subagents support tool allowlists/blocklists and VCS sharing.
- Context Engine claims to maintain a "live" codebase understanding (closed-source proprietary tech).
- **Borrow:** The auto-import-from-Claude-Code precedent matters strategically. Momentum should confirm its on-disk layout works for Auggie ingestion.

### 9. Replit Agent 4 — Multi-Agent Architecture with Visible Roles

- **URL:** [replit.com/products/agent](https://replit.com/products/agent) · case study at [langchain.com/breakoutagents/replit](https://www.langchain.com/breakoutagents/replit) [OFFICIAL]
- **Differentiator:** Architecture is explicitly multi-agent: **Manager agent** (orchestrates), **Editor agents** (file ops), **Verifier agent** (tests). Auth/DB/backend/frontend handled in parallel. Replit reports ~90% tool invocation success rate at production scale. [PRAC]
- **Caveat:** Locked to Replit's cloud platform. Not a self-host option.
- **Borrow:** The named-role pattern (Manager/Editor/Verifier) is similar to Momentum's lens system in AVFL but applied to dev rather than validation. Worth comparing structurally.

### 10. Qoder — Quest Mode Async Spec Execution

- **URL:** [qoderide.net](https://qoderide.net/en/features) [OFFICIAL]
- **Parent:** Alibaba [PRAC]
- **Differentiator:** **Quest Mode** runs spec-driven tasks fully async — agent works in background, only pings the user for decisions or completion. Spec auto-generated from project analysis. Repository wiki auto-built. [PRAC — [Jimmy Song review](https://jimmysong.io/blog/qoder-alibaba-ai-ide-personal-review/)]
- **Borrow:** Async-by-default Quest Mode is conceptually similar to Momentum's sprint-dev (run worktrees, return when done) but with a much more polished UX layer — agent posts progress notifications.

### 11. Junie (JetBrains) — Three-Tier Reasoning Architecture

- **URL:** [jetbrains.com/junie](https://www.jetbrains.com/junie/) [OFFICIAL]
- **Differentiator:** Three-tier architecture: (1) Contextual Indexing using JetBrains Static Analysis, (2) Plan Generation as a "Task Blueprint", (3) Execution Loop with self-correction. Brave / Think / Auto modes for different autonomy levels. Junie CLI is now standalone (LLM-agnostic) per [DevOps.com](https://devops.com/jetbrains-launches-air-and-junie-cli-to-blend-traditional-ide-with-ai-agents/). [PRAC]
- **Borrow:** **Static-analysis-driven contextual indexing** is something Momentum lacks — its context comes from grep/read/MCP. Tighter LSP/static-analysis integration is a long-term direction worth noting.

### 12. Ona (formerly Gitpod) — Sandboxed Per-Agent Cloud Environments

- **URL:** [ona.com](https://ona.com) [OFFICIAL]
- **Differentiator:** Each agent gets its own ephemeral sandboxed cloud environment defined via `devcontainer.json` and `automations.yml`. Agents run on phones via VS Code Browser. Sells AWS VPC deployment for regulated industries. [PRAC — [InfoQ rebrand coverage](https://www.infoq.com/news/2025/09/gitpod_ona/)]
- **Borrow:** **`devcontainer.json` + `automations.yml` as the agent-environment spec** — Momentum runs in local worktrees today. If Momentum ever needs to scale to ephemeral cloud environments, Ona's spec is the model.

### 13. OpenHands — OSS Reference Implementation with Plugins

- **Repo:** [github.com/OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) · MIT license · 65K+ stars · [paper](https://arxiv.org/abs/2511.03690) [OFFICIAL]
- **Differentiator:** Plugins bundle skills + hooks + MCP servers + agents + commands as **single reusable packages**. Plugin structure includes `hooks/pre-task.sh`, `hooks/post-task.sh`, `scripts/`. Sub-agents as file-based markdown (no Python required). [OFFICIAL — [docs.openhands.dev/sdk/guides/plugins](https://docs.openhands.dev/sdk/guides/plugins)]
- **Borrow:** **Plugin = bundle of skills + hooks + agents + MCP** is a useful packaging model. Momentum currently has its plugin distribution but the bundle isn't quite this clean — distinct skills, distinct rules, distinct hooks.

---

## Tier 3 — Routine Catalog

One-line entries; no novel capability for Momentum.

| Platform | Parent | One-line verdict |
|---|---|---|
| **AdaL** | SylphAI | "Self-evolving" auto-prompting that learns from commits — neat in theory, no public details on the mechanism. [SylphAI-Inc/adal-cli](https://github.com/SylphAI-Inc/adal-cli) [UNVERIFIED] |
| **IBM Bob** | IBM watsonx | RPG/COBOL/IBM-Z modernisation focus. Mainframe-only relevance. Multiple modes (Ask/Plan/Code/Advanced/Orchestrator) but nothing structurally novel for Momentum. [PRAC] |
| **Command Code** | Independent (no Cohere link despite the name) | "Continuously learns your coding taste" — vague, single-page marketing site. Skip until they ship docs. [UNVERIFIED — [commandcode.ai](https://commandcode.ai)] |
| **Crush** | Charm | Bubble Tea TUI, MIT-licensed, MCP/LSP support, multi-model. Beautifully terminal-aesthetic but functionally a Claude Code clone. Worth installing for the polish, not the architecture. [github.com/charmbracelet/crush](https://github.com/charmbracelet/crush) |
| **Snowflake Cortex Code** | Snowflake | Tied to Snowflake data stack; uses ACP for editor integration (Zed, JetBrains, Emacs). Domain-locked. [PRAC] |
| **Firebender** | YC startup | Android Studio + JetBrains. Niche to mobile dev. Has Plan mode and "Heavy Mode" multi-agent — names without distinguishing tech. |
| **iFlow** | Independent | Yet another Qwen3-Coder/Kimi/DeepSeek wrapper. SubAgent + MCP "Open Market" — a registry, not a capability. |
| **Kimi Code** | Moonshot | **Notable detail: claims Agent Swarm of up to 100 parallel sub-agents**. Supports ACP out of the box. [github.com/MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli) — borderline Tier 2 but the claim is unverified at scale. |
| **Kode** | shareAI-lab | `@`-mention-driven model+subagent invocation. Open-source. Niche aesthetic. |
| **Mistral Vibe** | Mistral | Devstral 2-powered. Now paid (Le Chat plans). Standard CLI agent. |
| **Mux (Coder)** | Coder.com | See Tier 2 — included for completeness. |
| **OpenClaw** | Open source | Multi-channel "personal AI assistant" — claims 50+ inbound channels (Slack, email, etc.). Not coding-focused; included by BMAD curiously. |
| **Pi** | badlogic/pi-mono | Minimal 4-tool agent (read/write/edit/bash); skills/extensions add capability. Open source. Trivially small surface — a teaching tool more than a production target. [BMAD support is community-proposed, not yet merged per [Issue #1853](https://github.com/bmad-code-org/BMAD-METHOD/issues/1853)] |
| **QwenCoder (Qwen Code)** | Alibaba/QwenLM | Open-source CLI optimised for Qwen3-Coder. SubAgents + Skills. **Documents itself as "Claude Code-like"** — a literal port of the Claude Code experience to Qwen models. [github.com/QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) |
| **Replit Agent** | See Tier 2 |
| **Rovo Dev** | Atlassian | Powered by Atlassian's Teamwork Graph (Jira/Confluence/Bitbucket). Generates Jira sub-tasks from user stories. **Interesting only if Momentum integrates with Atlassian** — not currently in scope. [PRAC] |
| **Trae** | ByteDance | Full IDE fork. Builder Mode does pre-change preview. Concerning [data-collection report](https://blog.unit221b.com/dont-read-this-blog/unveiling-trae-bytedances-ai-ide-and-its-extensive-data-collection-system) — ByteDance privacy posture is a red flag. Skip. |
| **Warp** | Warp.dev | Increasingly an agent-orchestration platform. Runs Claude Code, Codex, Gemini CLI **under itself** as a meta-terminal. Worth tracking as a host for Momentum, not a target. |
| **Zencoder** | Independent | "Repo Grokking" indexes codebase for context-aware retrieval. 80+ languages, monorepo support. Closed-source. |
| **CodeBuddy** | Tencent | The first Chinese tool to ship as plugin + IDE + CLI. `.codebuddy/rules/`, Skills, MCP. Tencent reports 85% internal adoption — relevant signal but capability is standard. |
| **Auggie** | See Tier 2 |
| **Pochi** | See Tier 2 |
| **Junie** | See Tier 2 |
| **Antigravity** | See Tier 1 |
| **Sourcegraph Amp** | See Tier 1 |
| **Kiro** | See Tier 1 |
| **Factory Droid** | See Tier 1 |
| **Neovate** | See Tier 1 |

---

## Capability Gap Analysis

What Momentum's current research base (Claude Code + OpenCode + Codex + Goose + ForgeCode + Gemini CLI) does **not** teach us — and which of the 22 surveyed platforms could fill the gap:

### Gap 1: System-prompt-modifying hooks
Claude Code does not expose `systemPrompt` as a hook event. Skill content is concatenated via reads at session start. **Neovate exposes `systemPrompt`, `provider`, `modelAlias`, `outputStyle` hooks** — none of which Claude Code has. If Momentum ever wants dynamic, path-scoped rule injection without static reads, Neovate is the reference implementation.

### Gap 2: Workflow-task-scoped (not tool-call-scoped) hooks
Claude Code's hooks fire around tool calls. **Kiro fires `Pre Task Execution` / `Post Task Execution` around spec-task lifecycle events.** Momentum's sprint-dev has many implicit "task boundaries" (story start, AVFL gate, merge) where practice rules should fire. Today these require ad-hoc detection. Kiro's spec-task hook is the missing layer.

### Gap 3: Verification artifacts as standard practice output
None of Claude Code, Codex, OpenCode, Goose, ForgeCode treat verification artifacts (screenshots, recordings, walkthroughs) as standard outputs. **Antigravity makes them mandatory.** Momentum's AVFL is text-rigorous but UI-blind — closing this requires the cmux browser surface to produce attached artifacts on dev-story completion, not just on demand.

### Gap 4: Persistent thread / project memory as a first-class artifact
Claude Code's MEMORY.md is auto-managed but ad-hoc. **Sourcegraph Amp's persistent threads** model project memory as a structured, queryable artifact distinct from session context. Momentum scatters this across `.claude/rules/`, `momentum:decision` documents, retrospective findings, and MEMORY.md — Amp consolidates.

### Gap 5: Multi-surface deployment from one source
Momentum runs in Claude Code only. **Factory Droid deploys the same droid across CLI + VS Code + JetBrains + Slack + Teams + ticket triggers.** Pochi's "skills-as-symlinked-directories" is the simpler version. If Momentum ever wants to ship one practice across multiple surfaces, both are precedents — Factory for the polish, Pochi for the OSS minimum.

### Gap 6: Async, notification-driven workflow execution
Claude Code's sprint-dev pattern requires the developer to monitor cmux panes. **Qoder's Quest Mode** and **Antigravity's Manager surface** both run agents fully async with progress notifications. The cmux-as-multiplexer approach in Momentum is functional but agent-aware UI surfaces are the next step.

### Gap 7: Static-analysis-grounded context
Claude Code grounds context in grep/read. **Junie's three-tier architecture starts with JetBrains static analysis indexing.** This is closer to how a senior engineer reasons. Momentum has no equivalent today — long-term direction.

---

## Recommendations

Two-three platforms warrant a **deeper individual research project** to extract patterns Momentum should consider adopting:

### Recommendation 1 — Deep Research: Factory Droid (HIGH PRIORITY)

Factory is the closest functional analog to Momentum's ambitions: hook-rich, sub-agent-rich, multi-surface, enterprise-routed, used at named-brand companies. A focused research pass should extract:

- **Hook event taxonomy** — full reference, not just the 10-event summary I captured
- **`.droid.yaml` schema** — the project-config YAML format
- **Custom Droid validation pipeline** — how does the CLI validate a droid before exposing it as a `subagent_type`?
- **On-prem model routing** — the rules engine that picks Claude Sonnet 4.5 vs on-prem for sensitive data
- **Project Manager integration** — Jira/Linear-triggered droid runs are a pattern Momentum doesn't have

Output target: 1500-word deep-dive at `verification-factory-droid-deep.md`.

### Recommendation 2 — Deep Research: Kiro Spec-Driven Workflow (HIGH PRIORITY)

Kiro's three-phase pipeline (`requirements.md` EARS → `design.md` → `tasks.md`) is structurally identical to BMAD/Momentum but **implemented as a native IDE workflow with first-class file artifacts and lifecycle hooks**. A focused pass should extract:

- **EARS notation** — does Momentum's create-story output meet EARS, and should it?
- **`tasks.md` dependency-sequenced format** — comparable to Momentum's stories/index.json
- **Pre/Post Task Execution hooks** — exact event payload, what's available to a hook script
- **`.kiro/steering/` rules** vs Momentum's `.claude/rules/` — are there structural lessons?
- Risks: Kiro is AWS-locked and closed-source. The patterns are extractable; the implementation is not.

Output target: 1500-word deep-dive at `verification-kiro-spec-driven-deep.md`.

### Recommendation 3 — Deep Research: Neovate Plugin/Hook System (MEDIUM PRIORITY)

If Momentum ever wants to argue for hook surface expansion in Claude Code (or build a harness layer of its own), Neovate's 23-hook implementation is the open-source proof-of-concept. A focused pass should extract:

- **Full plugin manifest schema** — how a plugin registers across the 23 hooks
- **`systemPrompt` hook semantics** — when does it fire, what's mutable?
- **`provider` and `modelAlias` hooks** — how dynamic model routing actually works in OSS
- **Comparison with Claude Code's documented 28 hooks** — net new surface

Output target: 1000-word focused note at `verification-neovate-hooks-deep.md`. Lower priority because the value is comparative rather than directly applicable.

---

## Confidence and Limits

- **Verified [OFFICIAL]:** Platform-codes.yaml (BMAD), Factory hooks reference, Kiro hooks/types, Neovate plugin docs, OpenHands SDK plugin docs, Auggie hooks, Sourcegraph Amp examples repo. Primary sources fetched directly.
- **Verified [PRAC]:** Reviews, blog write-ups, news coverage. Useful for differentiator claims but model-summarised; treat numbers (productivity %, customer counts, valuations) with normal skepticism.
- **[UNVERIFIED]:** AdaL's "self-evolving" auto-prompting; Command Code's claims; Kimi Code's 100-parallel-subagent claim; Replit's 90% tool success at scale. Marketing material, no engineering data.
- **Did not directly verify:** Pricing for any platform; SOC2/HIPAA actual certification (vs roadmap); enterprise audit-log surfaces. Claims here come from vendor-side material and should not be load-bearing.

The 42-platform support claim in BMAD v6.5.0 is straightforwardly verifiable from `platform-codes.yaml`. What "support" *means* per platform is highly variable — some entries are full installer integrations, others are just an output directory and a marker file. BMAD's support is a delivery mechanism, not a quality assertion.
