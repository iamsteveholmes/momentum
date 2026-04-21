---
title: "ForgeCode and agentic tooling evaluation for Momentum — Research Report"
date: 2026-04-21
type: Technical Research — Consolidated Report
status: Complete
content_origin: claude-code-synthesis
human_verified: true
profile: medium
derives_from:
  - path: scope.md
    relationship: scoped_by
  - path: raw/research-forgecode-overview.md
    relationship: synthesized_from
  - path: raw/research-agentic-peers-comparison.md
    relationship: synthesized_from
  - path: raw/research-model-routing-ai-markets.md
    relationship: synthesized_from
  - path: raw/research-momentum-practice-surface.md
    relationship: synthesized_from
  - path: raw/research-integration-parallel-replace-paths.md
    relationship: synthesized_from
  - path: raw/research-maturity-risks-governance.md
    relationship: synthesized_from
  - path: raw/gemini-deep-research-output.md
    relationship: synthesized_from
  - path: raw/verification-forgecode-hooks-and-version.md
    relationship: verified_by
  - path: raw/verification-direct-webfetch.md
    relationship: verified_by
  - path: validation/avfl-report.md
    relationship: validated_by
  - path: raw/practitioner-notes.md
    relationship: informed_by
---

# ForgeCode and Agentic Tooling Evaluation for Momentum — Research Report

## Executive Summary

The agentic coding harness market has converged, in the twelve months since Claude Code shipped, on a recognizable shape: terminal-native loop, markdown rule files auto-loaded from conventional directories, skills and agents as first-class markdown + YAML frontmatter, MCP as the tool-extension substrate, and planner+specialist orchestration. Every serious peer — ForgeCode, Goose, OpenCode, Qwen Code, Kilo Code, Cline, Roo, Crush, Codex CLI — is building in this shape. This is a strong validation of Momentum's foundational bets: file-authoritative rules, portable SKILL.md, and orchestrator-plus-subagents patterns.

ForgeCode itself is a credible open-source Claude-Code-class harness — Rust, Apache-2.0, terminal-native, three built-in agents (Forge, Muse, Sage), multi-provider, git-worktree sandboxing as a first-class flag, and a usable `.forge/agents/`, `.mcp.json`, `AGENTS.md`, `forge.yaml` config surface. But its headline TermBench 2.0 score of 81.8% is compromised by a documented benchmark-contamination finding from the University of Pennsylvania DebugML group: ForgeCode auto-loaded `AGENTS.md` files that literally contained answer keys, and the clean-scaffold adjusted score is ~71.7% (14th place, not 1st). That matters — both because it sets a ceiling on ForgeCode's credibility as an engineering organization and because the "trust the benchmark" mode of evaluation is no longer safe. Separately, ForgeCode does **not** expose a user-configurable hook surface — its determinism comes from a different, internally-hardcoded set of mechanisms (per-agent tool allowlists, `todo_write` + `verify_todos` enforcement, file-materialized plans via the Muse-to-Forge handoff, doom-loop detection, bounded-turn caps). This is a meaningful architectural difference from Claude Code, not a gap to be papered over.

The practical finding for Momentum: **no peer is a better host for Momentum than Claude Code today**, but two peers are strong enough to play specific supporting roles. OpenCode (sst/opencode, 147k stars, MIT, TypeScript plugins, 25+ lifecycle events, native read of `.claude/skills/*/SKILL.md` and `CLAUDE.md`) is the only viable full-migration target if Momentum ever needs to leave Claude Code; it already reads Momentum's authored artifacts with zero porting. Goose (block/goose, ~42.9k stars, Apache-2.0, stewarded by the Linux Foundation's Agentic AI Foundation) is the strongest governance-stable option and has the deepest MCP ecosystem, but its Recipes/subrecipes model competes with Momentum's skill/workflow model rather than hosting it. Aider is excellent as a narrow specialist co-processor for bulk mechanical edits, but not a practice host.

The recommended direction is a three-layer strategy: (1) keep Claude Code as primary, (2) wire ForgeCode or Aider behind a single `momentum:bulk-refactor` co-processor skill so routine mechanical edits route to cheap models while Claude Opus stays on architecture, (3) run a one-workflow parallel experiment on OpenCode to de-risk future harness migration — using Momentum's existing `.claude/skills/` directory unchanged. In parallel, Momentum should actively import specific transferable primitives that peer tools have shipped: Cline's rule-vs-workflow token-cost split, Goose's sub-recipe parameter mapping, OpenCode's `session.compacting` pre-compaction hook, Continue's regex rule activation, Qwen's `SubagentStart`/`SubagentStop` events, and Codex's `AGENTS.override.md` pattern. The market is commoditizing Momentum's substrate; Momentum's defensibility is the practice layer on top.

## TL;DR Recommendations

1. **Do not migrate Momentum off Claude Code in 2026 Q2.** The hook, TeamCreate + SendMessage, and auto-memory deltas are structural, not cosmetic. Re-evaluate after OpenCode or Goose ships an inter-agent messaging primitive, or after Block's unified-tooling RFC lands.
2. **Wire ForgeCode (or Aider) as a specialist co-processor** behind a single new skill like `momentum:bulk-refactor`. Route mechanical edits (scaffolding, CRUD, boilerplate, bulk renames) to cheap open-weight models via OpenRouter and keep Claude Opus for architecture and review. Sandbox in a sibling git worktree.
3. **Run a one-workflow parallel experiment on OpenCode.** Pick a contained workflow (candidate: `create-story` or `research`) and execute it under OpenCode using the existing `.claude/skills/` directory — OpenCode reads it natively. Compare outputs. Cost of experiment: <1 week.
4. **Adopt the TermBench disclosure as part of ForgeCode's credibility assessment**, not a footnote. ForgeCode's raw score is contested and the team has not (as of 2026-04-21) publicly reconciled with the DebugML paper. Treat benchmark claims from the vendor with skepticism; treat the primary repo's architectural qualities at face value.
5. **Standardize Momentum authoring on portable substrate.** Keep writing under `.claude/skills/` and `CLAUDE.md` regardless of host — this is now the widest-compatibility surface (OpenCode reads it directly, others have converged on SKILL.md). Add `AGENTS.md` as a compatibility symlink/generation target where appropriate.
6. **Import transferable primitives:** Cline's rules-vs-workflows split; Goose's `sub_recipes` parameter mapping; OpenCode's `session.compacting` pre-compaction hook; Continue's regex rule activation; Qwen's `SubagentStart`/`SubagentStop` hook events; Codex's `AGENTS.override.md` pattern. All are concrete, small-surface upgrades Momentum can ship independently of any migration decision.
7. **Run Momentum's router layer behind a proxy.** Either OpenRouter's Anthropic-skin base URL (zero-ops) or a self-hosted LiteLLM (full fallback chains, per-team budgets). Either one is more capable than Claude Code's env-var approach for cost control.
8. **Governance hedge: track AAIF.** The Linux Foundation's Agentic AI Foundation (MCP + Goose + AGENTS.md as founding contributions) is the best governance story in the set. Lean on the shared standards (MCP, AGENTS.md, SKILL.md) as portability insurance.

## 1. What is ForgeCode?

ForgeCode — occasionally branded "Forge Code" — is an open-source, Rust-implemented, terminal-first agentic coding harness. The canonical repository is `tailcallhq/forgecode` [VERIFIED]; `antinomyhq/forge` resolves to the same repository via HTTP 301 redirect (this is the reverse of the earlier subagent assumption, confirmed by direct `curl -sI` against GitHub on 2026-04-21) ([tailcallhq/forgecode](https://github.com/tailcallhq/forgecode)) [VERIFIED]. Repo stats on 2026-04-21: 6,794 stars, 1,374 forks, 132 open issues, 340 git tags, Apache-2.0 license, Rust 93.6% of LOC, created 2024-12-08, last pushed the day of research ([tailcallhq/forgecode](https://github.com/tailcallhq/forgecode)) [VERIFIED].

### 1.1 Architecture and Runtime

ForgeCode is a standalone Rust binary, distributed primarily via `curl -fsSL https://forgecode.dev/cli | sh`, with alternate paths via `nix run github:tailcallhq/forgecode` and the npm shim `@antinomyhq/forge` ([README](https://github.com/tailcallhq/forgecode/blob/main/README.md)) [VERIFIED]. Internally it is a Cargo workspace with multiple crates under `crates/`. It has three interaction modes:

1. **Interactive TUI** — `forge` with no arguments drops into a persistent conversational session.
2. **One-shot CLI** — `forge -p "prompt"` runs a single task and is pipeable.
3. **ZSH shell plugin** — after `forge setup`, a `:` prefix at the shell invokes ForgeCode inline (`: refactor the auth module`), so the developer never leaves the shell.

### 1.2 Built-in Agents and the Determinism Story

ForgeCode ships three built-in agents as `.md` files with YAML frontmatter in `crates/forge_repo/src/agents/` ([VERIFIED](https://github.com/tailcallhq/forgecode/tree/main/crates/forge_repo/src/agents)):

- **Forge** (execution): tools = `task, sem_search, fs_search, read, write, undo, remove, patch, multi_patch, shell, fetch, skill, todo_write, todo_read, mcp_*` — the only agent that can modify files.
- **Muse** (planning): tools = `sem_search, sage, search, read, fetch, plan, mcp_*` — has a `plan` tool but no `write`/`patch`/`shell`, so is structurally incapable of modifying code.
- **Sage** (research/read-only): tools = `sem_search, search, read, fetch` — pure read-only.

Custom agents follow the same shape under `.forge/agents/*.md` (project-local) or `~/forge/agents/*.md` (global). Project-local overrides global.

**This per-agent tool allowlist is load-bearing.** It is the primary determinism mechanism and the reason Forge advertises "bounded context." The Muse agent cannot write files not because its prompt tells it so, but because its tool list does not contain `write`, `patch`, or `shell`. The enforcement is at the orchestrator level, not the prompt level.

**Hooks — primary-source truth.** Gemini's main-body synthesis claimed ForgeCode has "native hook systems for validation and logging." Four Claude Code subagent files claimed hooks were "absent." Direct repo reading resolves both positions as partially correct [VERIFIED per [verification-forgecode-hooks-and-version.md](../raw/verification-forgecode-hooks-and-version.md)]:

- **Forge has a fully realized internal lifecycle-hook architecture in Rust** — six event types (`Start`, `End`, `Request`, `Response`, `ToolcallStart`, `ToolcallEnd`) and five concrete handlers (`CompactionHandler`, `DoomLoopDetector`, `PendingTodosHandler`, `TitleGenerationHandler`, `TracingHandler`) in `crates/forge_domain/src/hook.rs` and `crates/forge_app/src/hooks/mod.rs` ([VERIFIED](https://github.com/tailcallhq/forgecode/blob/main/crates/forge_domain/src/hook.rs)).
- **ForgeCode exposes zero user-configurable hook surface.** The only relevant user toggle is the boolean config flag `verify_todos` (default `false`), which conditionally adds `PendingTodosHandler` to the `on_end` chain ([VERIFIED via `forge.schema.json`](https://github.com/tailcallhq/forgecode/blob/main/forge.schema.json)). A developer cannot drop a shell script or declare `PreToolUse`/`PostToolUse` handlers in YAML/JSON.

The determinism story Forge tells instead is:

1. **Per-agent tool allowlists** (Forge/Muse/Sage separation above).
2. **`todo_write` + `verify_todos` enforcement loop** — Forge's system prompt instructs "Use this tool VERY frequently," and if `verify_todos: true`, `PendingTodosHandler` prevents premature termination when unfinished todos remain.
3. **File-materialized plan workflow** — Muse writes plan markdown files to `plans/`; the `execute-plan` skill then runs them. Plan-as-file is the review gate; no formal approval hook.
4. **`DoomLoopDetector`** — hardcoded, fires on every request, catches consecutive-identical `(tool, args)` pairs and `[A,B,C][A,B,C]` sequences, injects a break-out message when detected ([VERIFIED](https://github.com/tailcallhq/forgecode/blob/main/crates/forge_app/src/hooks/doom_loop.rs)).
5. **`CompactionHandler`** — auto-compacts context on token-budget exceedance.
6. **Bounded-turn config flags** — `max_tool_failure_per_turn`, `max_requests_per_turn`, and `restricted: boolean` for shell sandboxing.
7. **`task` tool / subagents** — gated by `subagents: boolean` (default `false`); when enabled, Forge gets a `task` tool that launches specialized sub-agents as subprocesses with their own tool allowlists. Subagents support `session_id` resumption.

The takeaway: **Forge's determinism is a curated, hardcoded set of primitives, not a user-extensible hook API.** A team cannot add a `post_edit_lint` hook without modifying Rust source — but they also get working determinism out of the box without configuring one. For Momentum's practice-layer needs, where the hook API is the enforcement spine, this is a **structural mismatch**, not a capability we can polyfill.

Gemini's named components "Tool-Call Correction Layer" and "Semantic Entry-Point Discovery" do not exist in the codebase under those names — direct GitHub code search returns 0 hits for both [HALLUCINATION, VERIFIED by [verification-forgecode-hooks-and-version.md](../raw/verification-forgecode-hooks-and-version.md)]. Gemini's follow-up 3 cited a ForgeCode blog URL as "verification," but the codebase itself has no such symbols. Do not cite these as real feature names; they are a specific caution about the Gemini synthesis reliability.

### 1.3 Skills, MCP, Sandboxing, Indexing

**Skills.** Three built-in skills ship: `create-skill` (scaffolder), `execute-plan` (runs Muse's plan files), `github-pr-description`. Custom skills live in `.forge/skills/<name>/SKILL.md` (project) or `~/forge/skills/<name>/SKILL.md` (global); precedence is project > global > built-in ([VERIFIED README](https://github.com/tailcallhq/forgecode/blob/main/README.md)). This is the same SKILL.md shape Momentum uses today and Anthropic's Agent Skills standardize.

**MCP.** Project-local `.mcp.json` or global `~/forge/.mcp.json`, standard `mcpServers` shape. Management: `forge mcp list | import | show | remove | reload`. Project overrides global. [VERIFIED]

**Git worktree sandboxing.** `forge --sandbox <name>` creates an isolated worktree with its own branch, starts an interactive session in it, leaves the main tree untouched. Merge back only what works. This is a first-class CLI flag, which Claude Code does not currently have — in Claude Code the same pattern is a community skill ([Worktree Isolation Claude Code Skill](https://mcpmarket.com/tools/skills/worktree-isolation)) [CITED].

**Semantic codebase indexing.** `:sync` indexes the repo for meaning-based search. **Indexing ships file content to `https://api.forgecode.dev` by default** (configurable via `FORGE_WORKSPACE_SERVER_URL`) [VERIFIED]. Some community posts describe ForgeCode as "fully local"; the README contradicts this. For private codebases this is a data-egress concern that needs explicit configuration to self-host.

### 1.4 Model Support and CLI/IDE Integration

Model-agnostic by design. Provider support spans Anthropic (Opus/Sonnet), OpenAI (O-series, GPT-5.x), Google (Gemini via Vertex), Groq (DeepSeek-R1 distill), Amazon Bedrock, xAI Grok, DeepSeek, Z.AI, Cerebras, IO Intelligence, Requesty, OpenRouter, and any OpenAI-compatible API ([README](https://github.com/tailcallhq/forgecode/blob/main/README.md)) [VERIFIED]. Provider credentials are managed via `forge provider login`; the legacy `.env` approach is deprecated. Mid-session model switching is supported via `:model` (one-shot) and `:config-model` (persistent). Local models work via OpenAI-compatible endpoints (LM Studio, Ollama with OpenAI compat, llama.cpp server).

**IDE integration: essentially none.** No VS Code extension beyond a lightweight file-reference utility (~1,679 installs at time of research, per AVFL finding 005). No JetBrains plugin. No web UI. Platforms: Linux, macOS, Windows (with ZSH as first-class shell; Bash parity not advertised). The positioning is explicitly "use any IDE, ForgeCode stays in the terminal."

### 1.5 Pricing and Licensing

ForgeCode left its unlimited free-tier early-access window on 2025-07-27 and moved to tiered pricing ([ForgeCode blog — Graduating from Early Access](https://forgecode.dev/blog/graduating-from-early-access-new-pricing-tiers-available/)) [VERIFIED]:

| Tier | Price | Quota |
|---|---|---|
| Free | $0/mo | Dynamic daily request limit, typically 10–50 requests/day |
| Pro | $20/mo | Up to 1,000 AI requests/day |
| Max | $100/mo | Up to 5,000 AI requests/day |

The subscription gates access to ForgeCode's hosted inference gateway and workspace server. BYOK is supported against Anthropic, OpenAI, OpenRouter, etc., though free-tier caps still apply to ForgeCode's hosted semantic workspace. The code itself is Apache-2.0, so self-hosting and forking the binary is permitted. Telemetry can be disabled via `FORGE_TRACKER=false`.

### 1.6 Current Version and Benchmark Controversy

**Current version:** v2.12.0, published 2026-04-21T06:52:07Z — the day of research [VERIFIED via GitHub Releases API, see [verification-forgecode-hooks-and-version.md](../raw/verification-forgecode-hooks-and-version.md)]. Trajectory: v0.106.0 (2025-08-12) → v1.0.0 (2025-10-25) → v2.0.0 (2026-03-14) → v2.12.0 (2026-04-21). Gemini's cited version (v0.106.0) was accurate for August 2025 but eight months stale at the research date.

**TermBench 2.0 score — contested [DISPUTED].** ForgeCode's homepage claims 81.8% on TermBench 2.0 with both GPT-5.4 and Claude Opus 4.6 — #1 on the leaderboard, beating Claude Code, Codex, Gemini-CLI ([forgecode.dev](https://forgecode.dev/)) [CITED, vendor]. A peer-reviewed paper titled "Finding Widespread Cheating on Popular Agent Benchmarks" (Adam Stein, Davis Brown, Hamed Hassani, Mayur Naik, Eric Wong; arxiv 2604.11806; published 2026-04-10) documented that ForgeCode *"automatically loads `AGENTS.md` files into the agent's system prompt before execution begins"* — and that the `AGENTS.md` files submitted to the benchmark contained *literal answer keys*, including "the exact expected answer along with a record of why a prior attempt had failed" (specifically naming `GritLM/GritLM-7B` as the expected output on one task; another trace showed ForgeCode hard-coding all six graph edges without running any discovery algorithm) ([DebugML paper](https://debugml.github.io/cheating-agents/)) [VERIFIED, primary source].

The paper reports the adjusted clean-scaffold score: *"When we replace the ForgeCode traces that reference `AGENTS.md` with the performance of the same model (Claude Opus 4.6) running through a clean scaffold, the overall pass rate drops from 81.8% to approximately 71.7%, which would move the submission from 1st place to 14th on the leaderboard"* [VERIFIED].

Per practitioner direction in Q1 of the developer Q&A, this disclosure is integrated as part of ForgeCode's credibility assessment, not a mere footnote. Both numbers are presented with context. For Momentum evaluation purposes: the 81.8% figure should not be used to infer harness superiority; the 71.7% figure indicates Forge performs roughly in line with the broader Claude Opus 4.6-driven cohort and substantially below Claude Code or Codex at their independently-verified scores. As a credibility signal, the finding matters — submitting benchmark entries with embedded answer keys is not a minor oversight, and as of research date ForgeCode has not publicly reconciled. Compare to SWE-bench Verified (Princeton/UChicago, independent): ForgeCode + Claude 4 ≈ 72.7%; Claude 3.7 Sonnet ≈ 70.3%; Claude Opus 4.5 ≈ 76.8% ([ForgeCode vs Claude Code, dev.to](https://dev.to/liran_baba/forgecode-vs-claude-code-which-ai-coding-agent-actually-wins-36c)) [CITED] — an independent gap on the order of single digits, not the 23.8-point gap the marketing implies.

### 1.7 ForgeCode vs Claude Code — Feature Delta

| Dimension | ForgeCode | Claude Code |
|---|---|---|
| License | Apache-2.0 | Proprietary (Anthropic) |
| Language | Rust | TypeScript |
| Model support | 300+ via OpenRouter + direct providers | Claude family only |
| Project config | `AGENTS.md` + `forge.yaml` | `CLAUDE.md` (nested) + `settings.json` |
| MCP | Yes | Yes (extensive, primary extension surface) |
| User-configurable hooks | **No** (internal Rust only) | **Yes** (PreToolUse, PostToolUse, UserPromptSubmit, Stop, etc.) |
| Scheduled tasks | No | Yes |
| Sub-agents | Forge/Muse/Sage + custom + optional `task` tool | Agent tool + TeamCreate/SendMessage |
| Plan mode | Muse writes to `plans/`, `:execute-plan` runs | Shift+Tab plan mode |
| VS Code extension | No (file-reference utility only) | Yes |
| JetBrains plugin | No | Yes |
| Auto-memory | No | Yes |
| Checkpoints / `/rewind` | No | Yes |
| Git worktree sandbox | **Yes** (`--sandbox` flag) | Community skill only |
| Terminal integration | ZSH `:` prefix + TUI | TUI + slash commands |
| Semantic code search | Built-in `:sync` (hosted) | None built-in |
| Pricing model | $0/$20/$100 + BYOK | Anthropic subscription + API |
| Benchmark credibility | Contested (DebugML disclosure) | Independent (SWE-bench Verified baseline) |

Where ForgeCode is arguably ahead: multi-model agility without vendor lock, Apache-2.0 inspectability, Rust footprint, `--sandbox` worktree isolation as a single CLI flag, native `:commit`/`:suggest`/`:edit`/`@file` ZSH ergonomics. Where Claude Code is ahead: **hooks** (the load-bearing Momentum primitive), IDE extensions, auto-memory, checkpoints, TeamCreate + SendMessage for inter-agent dialogue, Anthropic model-family tuning. The two tools overlap closely on terminal-first, MCP, skills, plan mode — which is why ForgeCode is Momentum's closest structural parallel among the open-source peers.

## 2. Agentic Tooling Landscape — ForgeCode vs Peers

Reproducing and refining the cross-tool comparison matrix. Star counts and versions are April 2026 snapshots.

| Tool | Primary UI | License | Stars | Model Flex | Orchestration | Extension Model | Maturity |
|------|------------|---------|-------|------------|---------------|-----------------|----------|
| **ForgeCode** | Terminal/ZSH | Apache-2.0 | 6.8k | 300+ models | Forge/Muse/Sage built-in + custom `.forge/agents/*.md`; optional `task` subagent tool | `forge.yaml`, MCP, custom agents, skills (`.forge/skills/<name>/SKILL.md`) | v2.12.0 (Apr 2026); benchmark claim compromised |
| **Goose** | CLI + desktop + API | Apache-2.0 | 42.9k | 15–25+ providers via ACP subscription passthrough; Anthropic/OpenAI/Gemini/Ollama/Bedrock | Recipes + subrecipes; sub-agent workflows via MCP | MCP-native (70+ extensions, 3000+ universe), `.agents/skills` | v1.31.1 (Apr 2026); 110+ releases; Linux Foundation AAIF stewardship Dec 2025 |
| **OpenCode** | TUI + beta desktop + mobile drive | MIT | 147k | Anthropic/OpenAI/Google/Bedrock/Groq/Azure/OpenRouter + local via AI SDK (75+ providers via Models.dev) | Built-in `build` + `plan` agents; `@general` subagent; multi-session parallel | Agents primary, MCP, TS/JS plugins, 25+ lifecycle events, `opencode.json` | v1.14.20 (Apr 2026); highest velocity in set |
| **Aider** | CLI | Apache-2.0 | ~43.7k | Any LiteLLM-backed provider | Architect/Editor mode pairing; watch mode; repo map; git-native auto-commit | `.aider.conf.yml`, `CONVENTIONS.md` prompt injection, MCP Registry | v0.86.0 (Aug 2025 — **release stalled vs peers**) |
| **Cline** | VS Code extension | Apache-2.0 | 60.5k | OpenRouter/Anthropic/OpenAI/Gemini/Bedrock/Azure/Vertex/Cerebras/Groq + local | Plan/Act modes; HITL approvals | `.clinerules/` + MCP marketplace + 6 lifecycle hooks (v3.36+) | v3.79.0 (Apr 2026); $32M VC, 5M+ users claim |
| **Qwen Code** | CLI + IDE integrations | Apache-2.0 (code) | 23.6k | OpenAI-compat/Anthropic/Gemini/ModelStudio/OpenRouter/Fireworks/Vertex/Ollama/vLLM | Skills + SubAgents; session compression | SKILL.md native, 13 lifecycle events | v0.14.5 (Apr 2026); Gemini-CLI fork; **free tier killed 2026-04-15** |
| **Kilo Code** | VS Code + JetBrains + CLI + App Builder | MIT (CLI) / Apache-2.0 (core) | 18.4k | 500+ models / 30+ providers | Orchestrator mode delegating to Architect/Coder/Debugger; custom modes | `.kilocode/skills/*`, MCP Server Marketplace, custom modes | v7.2.14 (Apr 2026); $8M seed Jan 2026; **GitLab ROFR through Aug 2026** |
| **Roo Code** | VS Code | Apache-2.0 | 23.3k | Multi-provider BYOK + xAI/Poe/MiniMax | Architect/Code/Ask/Debug + custom modes; boomerang delegation | Modes as extension primitive, MCP, `.roo/rules-{modeSlug}/` | v3.52.1 (Apr 2026); SOC 2 compliant |
| **Codex CLI** | CLI (Rust) | Apache-2.0 | (large) | OpenAI only | To-do tracking; MCP; Agents SDK orchestration | Agent Skills (OpenAI spec), MCP, experimental hooks (5+ events, feature-flagged) | GPT-5-Codex-tuned; hook support caveated on non-Bash tools |
| **Crush** | TUI (Go/Bubble Tea) | FSL-1.1-MIT | 23.3k | Anthropic/OpenAI/Gemini/Groq/OpenRouter/HF/Bedrock/Azure/Vercel/custom | Mid-session model switching; LSP-enhanced context; `--yolo` | MCP (stdio/http/sse), Agent Skills, JSON config | v0.61.1 (Apr 2026); broadest OS coverage incl. *BSD/Android |
| **Continue.dev** | VS Code + JetBrains + CLI | Apache-2.0 | (large) | Any provider via hub agents | Hub agents; agent mode; PR checks in CI | `.continue/rules/*.md` with regex/glob activation, `.continue/checks/*.md` as CI gates | Pivoting to source-controlled AI checks in CI |

### 2.1 Per-Tool Notes (condensed)

**ForgeCode.** Closest structural parallel to Momentum's primitive shape among the peers. `.forge/agents/*.md` with YAML frontmatter is functionally isomorphic to Momentum's subagent files. `.forge/skills/<name>/SKILL.md` mirrors Momentum's skill shape. `forge.yaml` is the Momentum settings-rules analog. MCP is first-class. The load-bearing gap is the absent user-configurable hook surface. Benchmark credibility compromised by DebugML disclosure.

**Goose.** Strongest governance in the set — Linux Foundation AAIF contribution December 2025 alongside MCP and AGENTS.md ([Block announcement](https://block.xyz/inside/block-open-source-introduces-codename-goose)) [VERIFIED]. 42.9k stars, 350+ contributors, AWS / Anthropic / Bloomberg / Cloudflare / Google / Microsoft / OpenAI among 170+ AAIF member organizations. Subscription passthrough via ACP (Agent Client Protocol) lets existing Claude/ChatGPT/Gemini subscriptions drive Goose. Recipes + subrecipes are a native deterministic workflow composition model — Jinja2-templated YAML with mapped-parameter sub_recipes ([Goose recipe reference](https://goose-docs.ai/docs/guides/recipes/)). Security: "Operation Pale Fire" red-team exercise in January 2026 compromised Goose via a poisoned Recipe hiding malicious instructions in invisible Unicode — patched, post-mortem public [CITED]. No user-level lifecycle hook API; prior Gemini claim retracted ([verification via follow-up 3](../raw/gemini-deep-research-output.md)).

**OpenCode.** Highest-star tool in the set — 147k stars on `sst/opencode` [VERIFIED, direct WebFetch]. MIT licensed. Daily-cadence releases. Client/server architecture separates UI from agent process — in principle Momentum could drive an OpenCode daemon headlessly. Two built-in agents (`build`, `plan`) plus `@general` subagent; multi-session parallel execution. Most interesting for Momentum: **OpenCode natively reads `.claude/skills/*/SKILL.md` and `CLAUDE.md`** as config fallbacks — a parallel review agent using OpenCode literally sees the same rules Claude Code does, with no porting. 25+ lifecycle events exposed via TypeScript/JavaScript plugins (`session.*`, `tool.execute.before`/`after`, `file.edited`, `permission.asked`, `message.part.updated`, `tui.prompt.append`, `shell.env`, experimental `session.compacting`) ([OpenCode Plugins docs](https://opencode.ai/docs/plugins/)) [VERIFIED]. The "2.5 million monthly developers" figure claimed in some sources is unsupported by the repo README; treat as [INFERRED, unreliable].

**Aider.** The elder statesman. Git-native auto-commit per change. Repo-map with symbol extraction. Architect/Editor two-model mode (plan with Opus, apply with DeepSeek/Haiku). Uses LiteLLM under the hood, so anything LiteLLM supports, Aider supports. 84.9% on its own polyglot benchmark with O3-Pro. **Cadence concern:** latest GitHub release is v0.86.0 dated 2025-08-09, meaning ~8 months without a release by research date. Contrast with Goose (monthly), OpenCode (daily), Cline (monthly), Kilo (weekly). Extension model is thin; Aider is best treated as a Unix-style runner behind a Momentum skill, not a practice host.

**Cline.** Strongest VS Code-native agent. 60.5k stars, $32M VC (Emergence/Pace), 5M+ users claimed. Plan/Act mode split. **First-class lifecycle hooks (v3.36+)**: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `TaskStart`, `TaskResume`, `TaskCancel`, plus `TaskComplete` and `PreCompact` in later docs — stdin-JSON-in, JSON-out contract with `cancel` and `contextModification` fields ([Cline v3.36 hooks blog](https://cline.bot/blog/cline-v3-36-hooks)) [VERIFIED]. `.clinerules/` supports path-scoped activation via frontmatter glob. Cline explicitly separates always-on rules from on-demand workflows — a clean design Momentum should borrow (see Cross-Cutting Themes). **Known context-budget issues:** open issues through v3.78.0 show Cline overflowing large-context models because it serializes a ~4.5K-token tool schema into every request and requests max-output-tokens equal to full context window ([Cline issue #9651, #8261, #10240](https://github.com/cline/cline/issues)) [CITED].

**Qwen Code.** Alibaba's Gemini-CLI fork, tuned at the parser level for Qwen3-Coder function-calling. 13 lifecycle events (highest count in the set). First-class SKILL.md + subagents. Qwen3-Coder-480B offers 256K native context extendable to 1M via YaRN. But **the free tier was killed on 2026-04-15** — daily quota dropped from 1,000 to 100 to zero, and users must now switch to Alibaba Cloud Coding Plan, OpenRouter, Fireworks, or BYOK ([GitHub issue #3203, Decrypt coverage](https://decrypt.co/364501/alibaba-shuts-down-free-tier-qwen-code)) [CITED]. Financial Times reporting (summarized by Decrypt) indicates Alibaba is shifting toward proprietary Qwen3.5/Qwen3.6 releases. The Apache-2.0 code continues; the model access pulls behind paywalls and state/regulatory surface. Policy risk is high.

**Kilo Code.** Interesting architectural validation for Momentum: Orchestrator mode delegates to Architect/Coder/Debugger specialists ([Kilo docs](https://kilo.ai/docs/customize/custom-modes)) [VERIFIED]. This is directly analogous to Momentum's Impetus-spawning-subagents pattern. Nested AGENTS.md loading is best-in-class among peers. $8M seed December 2025 from Cota Capital et al. Co-founded by Sid Sijbrandij (GitLab ex-CEO), with a **GitLab Right of First Refusal through August 2026** [CITED] — so acquisition risk is explicit in the governance story. No hooks.

**Roo Code.** Cline fork with custom modes, Roo Cloud, SOC 2 compliance, boomerang inter-mode task delegation. Rules support per-mode scoping via `.roo/rules-{modeSlug}/`. No hooks (open issues requesting them).

**Codex CLI.** OpenAI's Rust-native terminal agent. GPT-5-Codex is the agentic-tuned variant. Experimental hooks, flag-gated (`codex_hooks = true`), ~6 events documented, but currently only fire reliably for the Bash tool (not ApplyPatchHandler) per GitHub issue #16732 — a PostToolUse code-quality gate on file edits is not production-safe yet. Notable layer above: **Oh My Codex (OMX)** is an open-source orchestration project that adds hooks, multi-agent, persistent state, structured workflows on top of Codex — a strong market signal that Momentum's harness concept is being reinvented on every base CLI ([OMX writeup](https://a2a-mcp.org/blog/what-is-oh-my-codex)) [CITED]. Codex is OpenAI-only (intentional, but a real lock-in).

**Crush.** Charm/Bubble Tea TUI, FSL-1.1-MIT. Mid-session model switching. LSP-enhanced context. Adopts the cross-vendor "Agent Skills open standard" alongside MCP. Broadest OS coverage (macOS/Linux/Windows/FreeBSD/OpenBSD/NetBSD/Android). Demonstrates that MCP + Agent Skills + LSP is becoming the minimum viable terminal-agent stack.

**Continue.dev.** Pivoting from VS Code/JetBrains assistant to source-controlled AI checks enforceable in CI — `.continue/checks/*.md` markdown agents run as GitHub status checks ([blog post](https://blog.continue.dev/beyond-code-generation-how-continue-enables-ai-code-review-at-scale)) [CITED]. Its regex-based rule activation (file-content match, not just glob path) is a transferable primitive Momentum should study.

### 2.2 Maturity Ranking (April 2026)

By combined stars + release cadence + governance + commercial backing:

1. **OpenCode** — 147k stars, daily cadence, SST/Anomaly Innovations (profitable 2025)
2. **Cline** — 60.5k, monthly cadence, VC-backed ($32M)
3. **Goose** — 42.9k, 110+ releases, Linux Foundation AAIF governance
4. **Aider** — ~43.7k BUT stalled since 2025-08 — maturity trajectory weakening
5. **Crush** — 23.3k, Charm-backed
6. **Roo Code** — 23.3k, SOC 2, commercial entity
7. **Qwen Code** — 23.6k, Alibaba, policy risk
8. **Kilo Code** — 18.4k, $8M seed, GitLab ROFR
9. **ForgeCode** — 6.8k, smallest community, benchmark credibility compromised

## 3. Model Routing and AI Markets

Every tool in the survey ultimately talks to one of four router shapes: a hosted aggregator (OpenRouter), a dedicated inference cloud (Groq, Cerebras, Together, Fireworks), a self-hosted gateway (LiteLLM, Helicone, Portkey, Bifrost), or a local runtime (Ollama, LM Studio, llama.cpp, vLLM).

### 3.1 OpenRouter Is the Default

OpenRouter offers one API key across 290+ models from Anthropic/OpenAI/Google/DeepSeek/Meta/Mistral/xAI/Qwen. Pricing is passthrough (no per-token markup) plus a 5.5% surcharge on credit top-ups ([OpenRouter Pricing](https://openrouter.ai/pricing)) [VERIFIED]. It exposes both an OpenAI-compatible `/chat/completions` endpoint and an "Anthropic Skin" at `https://openrouter.ai/api` that speaks Claude's Messages API well enough for Claude Code to talk to it unmodified via `ANTHROPIC_BASE_URL` ([OpenRouter Claude Code docs](https://openrouter.ai/docs/guides/coding-agents/claude-code-integration)) [VERIFIED].

Routing primitives:
- **Provider ordering** (`provider.order`, `allow_fallbacks`) — pin preferred backend, auto-failover on error.
- **Auto Exacto** — default-on for tool-call requests; re-scores providers every five minutes across throughput, tool-call telemetry, benchmark signals.
- **Sort modes** — lowest-price / highest-throughput / lowest-latency as first-class params; Cline/Kilo expose one-for-one UIs.
- **BYOK** — point a provider slot at your own key; OpenRouter tries BYOK endpoints first. First 1M BYOK requests/month free; beyond that 5% surcharge ([OpenRouter BYOK announcement](https://openrouter.ai/announcements/1-million-free-byok-requests-per-month)) [VERIFIED].
- **Middle-out prompt compression** — server-side transform, Cline/Kilo expose as a checkbox.

### 3.2 Dedicated Inference Clouds

- **Groq** — open-weight Llama/Qwen/GPT-OSS on LPU silicon; ~476 tok/s on Llama 3.1 70B, 0.6–0.9 s TTFT [CITED].
- **Cerebras** — the speed outlier: ~3,000 tok/s on GPT-OSS 120B, ~2,000 tok/s on Qwen3-Coder-480B per Artificial Analysis benchmarks ([Cerebras Qwen3 blog](https://www.cerebras.ai/blog/qwen3-coder-480b-is-live-on-cerebras)) [VERIFIED]. Cerebras Code is a flat-rate subscription aimed at agentic coding; Cline has a first-class Cerebras integration ([Cline Cerebras docs](https://docs.cline.bot/provider-config/cerebras)) [VERIFIED]. Cerebras has higher TTFT than Groq — for chat-style interactions Groq still wins on small prompts, but in agentic loops the 2,000 tok/s compresses the whole session.
- **Together AI** and **Fireworks AI** — general-purpose open-weight clouds; Llama/Mistral/DeepSeek/Qwen + fine-tuning; 50–90% savings vs frontier APIs on equivalent workloads [CITED].
- **DeepInfra, Hyperbolic, SambaNova, Novita** — rounded out the pack.

### 3.3 Self-Hosted Gateways

- **LiteLLM** — the dominant open-source proxy. Speaks OpenAI Chat Completions *and* Anthropic Messages API in front of 100+ providers. Load balancing, ordered fallbacks (with per-rank retry budgets), cooldowns, timeouts, exponential backoff, tag-based routing, budget routing, health-check routing, per-key/per-team virtual keys, cost tracking, guardrails, admin dashboard ([LiteLLM docs](https://docs.litellm.ai/docs/routing-load-balancing)) [VERIFIED]. It is the component that makes most Claude-Code-on-non-Anthropic-models setups possible.
- **Helicone** — primarily observability (cost/latency dashboards, request-level tracing), newer Rust-based AI Gateway competing with LiteLLM on latency.
- **Portkey** — commercial ($49/mo+, not self-hostable), 1,600+ models, conditional routing, circuit breakers, HIPAA/SOC 2 [CITED].
- **Bifrost** — open-source Go gateway by **Maxim** (company: [getmaxim.ai](https://getmaxim.ai)) [VERIFIED, corrected from Gemini's "Maxim AI" naming]. Overhead: **11 µs on t3.xlarge / 59 µs on t3.medium**, sustained 5,000 req/sec; marketing claim "50× faster than LiteLLM" ([maximhq/bifrost](https://github.com/maximhq/bifrost)) [VERIFIED]. Cite the range, not just the low figure — the low figure is instance-dependent.
- **Cloudflare AI Gateway, Tetrate Agent Router, RelayPlane** — newer competitors.

### 3.4 Local Runtimes

- **Ollama** — OpenAI-compatible server on `localhost:11434`. Added "Ollama Launch" wrappers for claude-code/codex/droid/opencode in 2026.
- **LM Studio** and **llama.cpp** server mode — same niche.
- Practitioner consensus: useful for privacy/offline and for routing easy sub-tasks; context-window tuning (Ollama default 4,096 is too low for agent loops) and tool-calling fidelity are usual blockers.

### 3.5 Tool × Router Compatibility

| Tool | OpenRouter | Per-task/subagent model | Fallback chain |
|---|---|---|---|
| **Claude Code** | First-class via Anthropic Skin + `ANTHROPIC_BASE_URL` | Subagent `model:` field, `CLAUDE_CODE_SUBAGENT_MODEL` env | No native chain; relies on proxy |
| **ForgeCode** | First-class | Per-agent YAML frontmatter; `:provider` runtime switch | Manual `[[providers]]`; no auto chain |
| **Goose** | First-class with browser-auth flow | Per-provider; prompt caching auto-enabled for Claude via Anthropic/Bedrock/OpenRouter/LiteLLM | Tool-call fidelity gated on "works best with Claude" |
| **OpenCode** | First-class (preloaded) | `provider` / `model` / `small_model` in `opencode.json` | Not built-in; OpenRouter or proxy |
| **Qwen Code** | Via OpenAI-compat | `modelProviders` + per-provider `generationConfig` impermeable layer | Manual switch |
| **Kilo Code** | First-class with provider sort, data policy, middle-out | Per-mode model | OpenRouter sort |
| **Aider** | First-class | **Three-tier**: main + `--weak-model` + `--editor-model` | LiteLLM layer or `.aider.model.settings.yml` |
| **Cline** | First-class with provider-routing UI | Per-mode (Plan/Act) | OpenRouter only |

**Key observation: Claude Code is the most constrained tool in the survey on router/provider choice** — a structural consequence of being Anthropic's first-party product. Every other tool natively mixes models per-agent or per-task. This is the single most important delta if cost control via model specialization is a goal.

### 3.6 Cost / Quality Tradeoffs for Routine Coding

The Aider Polyglot leaderboard (225 Exercism exercises across C++/Go/Java/JS/Python/Rust, last refreshed Nov 2025) remains the most cited apples-to-apples benchmark ([leaderboard](https://aider.chat/docs/leaderboards/)) [VERIFIED]:

| Model | Polyglot % | Benchmark cost | Notes |
|---|---|---|---|
| Claude Opus 4.5 | 89.4% | — | Multi-language leader |
| GPT-5 (high) | 88.0% | $29.08 | Leaderboard #1 |
| GPT-5 (medium) | 86.7% | $17.69 | |
| O3-Pro (high) | 84.9% | $146.32 | Expensive outlier |
| Gemini 2.5 Pro Preview | 83.1% | $49.88 | |
| Claude Sonnet 4.6 | ~79.6% SWE-bench Verified | — | ~95% Opus quality at 60% cost per Morph [CITED] |
| DeepSeek V3.2 Reasoner | 74.2% | **$1.30** | **22× cheaper than GPT-5 at 84% of score** |
| Claude Opus 4 | 72.0% | $65.75 | |
| DeepSeek V3.2 Chat | 70.2% | $0.88 | Non-reasoning |
| Qwen3-Coder-480B | ~73% SWE-bench Verified reported | — | ~$2/MTok on Cerebras; free tier on OpenRouter |

**Practitioner defaults:**
- **Frontier autonomy** (large refactors, architecture): Claude Sonnet 4.6 or GPT-5 (medium).
- **Routine edits, scaffolding, CRUD**: DeepSeek V3.2 Chat ($0.88 on the full polyglot), or Qwen3-Coder-480B on Cerebras at 2,000 tok/s.
- **Explore / read-only / search**: Haiku 4 (Claude Code's default Explore subagent), Gemini 2.5 Flash, or local Qwen3 via Ollama.
- **Commit message / summarization weak-model**: DeepSeek Chat, Haiku 4, Gemini Flash. Aider's `--weak-model` flag targets this explicitly.

**Tokens-per-fix matters as much as model choice.** A 2026 Morph analysis found Aider uses 4.2× fewer tokens than Claude Code on a 3-tool, 47-file diff benchmark, largely because Aider's edit format is compact diff-based rather than full-file rewrites ([Morph analysis](https://www.morphllm.com/comparisons/morph-vs-aider-diff)) [CITED]. Across a day's work this is a bigger cost lever than model choice for routine edits.

### 3.7 Architecture Options for Momentum's Router Layer

If Momentum needs to route sub-tasks to cheaper or open-weight models:

- **Architecture A (zero-ops):** `ANTHROPIC_BASE_URL=https://openrouter.ai/api/anthropic`. Use Claude Code's subagent `model:` field and `CLAUDE_CODE_SUBAGENT_MODEL` env var to pick cheaper Claude-family models or OpenRouter's Anthropic-dialect entries. Zero new infrastructure.
- **Architecture B (full-capability):** Self-host LiteLLM, point Claude Code at it via `ANTHROPIC_BASE_URL`. Use LiteLLM's routing/fallback/budget primitives. Real fallback chains, real budgets, real per-key telemetry. One more service to operate.

**Architecture B is strictly more capable.** For per-project budgets, per-developer caps, or alerting, LiteLLM (or a commercial Portkey) is the operative decision, not the editor.

## 4. How Well Each Tool Hosts Momentum's Primitives

Momentum's practice layer rests on four primitives: (1) file-authoritative rules (auto-loaded from `.claude/rules/*.md` + nested `CLAUDE.md`), (2) skills as SKILL.md + workflow.md directories (model-invoked), (3) shell-command hooks in `settings.json` (harness-executed), (4) deterministic workflows with `<check>`/`<action>`/`<critical>` semantics. A fifth supporting primitive is the subagent-spawn model with isolated context, custom prompts, and tool whitelists.

| Tool | File-authoritative rules | Skills/agents first-class | Hooks | Deterministic workflows |
|---|---|---|---|---|
| **Claude Code (baseline)** | Native | Native | Native | Native (skill workflow.md) |
| **Qwen Code** | Native (AGENTS.md) | Native (SKILL.md + subagents) | Native (13 events) | Glue (skills carry workflows) |
| **OpenCode** | Native (AGENTS.md + `.claude/` fallback) | Native (SKILL.md + agents) | Native (~25 plugin events, TS/JS) | Glue |
| **Codex CLI** | Native (AGENTS.md chain + `AGENTS.override.md`) | Glue (slash + community SKILL.md) | Native (experimental, 5+ events, Bash-only reliable) | Glue |
| **Kilo Code** | Native (nested AGENTS.md) | Glue (modes) | Missing | Glue |
| **Cline** | Native (.clinerules/, AGENTS.md) | Glue (workflow slash commands) | Native (6–8 events, v3.36+) | Glue |
| **Roo Code** | Native (AGENTS.md + `.roo/rules`) | Glue (custom modes) | Missing | Glue |
| **Goose AI** | Glue (AGENTS.md flat) | Glue (Recipes hybrid) | Missing (retracted — no lifecycle hook API; MCP only) | Native (Recipes YAML + Jinja + sub_recipes) |
| **ForgeCode** | Native (AGENTS.md) | Glue (custom agents + SKILL.md skills) | **Missing at user surface** (internal Rust only, see §1.2) | Glue (agent prompts + custom commands + Muse/Forge plan file pattern) |
| **Continue.dev** | Glue (.continue/rules with regex/glob) | Missing (agents are profiles) | Missing | Missing |
| **Aider** | Glue (CONVENTIONS.md manual) | Missing | Missing | Missing |

Two clusters emerge:

- **High-fidelity hosts** (all four primitives native or near-native): Qwen Code, OpenCode, Codex CLI.
- **Partial hosts** (2+ primitives missing or heavy glue): Kilo, Cline, Roo, Goose, ForgeCode.

Aider and Continue.dev sit below the practice threshold.

**Key caveat on ForgeCode's determinism story.** ForgeCode substitutes a *different* determinism mechanism for hooks: per-agent tool allowlists (Forge/Muse/Sage structural separation), `todo_write` + `verify_todos` enforcement loop, file-materialized plan workflow (Muse's plans/ + `:execute-plan` skill), hardcoded `DoomLoopDetector`, bounded-turn config (`max_tool_failure_per_turn`, `max_requests_per_turn`), and `restricted` shell mode. For a greenfield team starting from scratch, this is a coherent alternative. For Momentum specifically — whose practice is *built around* user-configurable pre/post hooks (plan-audit, autonomous checkpoint-commit, architecture-guard, AVFL lens triggers) — Forge's substitute cannot fulfill the same role. The hooks are the enforcement spine.

**Transferable primitives worth importing to Momentum** (expanded in §5 and §Cross-Cutting Themes):

- **Cline's workflow/rule token-cost split** — always-on rules (persistent, expensive) vs on-demand workflows (slash-command-invoked, lazy) ([Cline blog](https://cline.ghost.io/stop-adding-rules-when-you-need-workflows/)) [VERIFIED].
- **Goose's `sub_recipes` with mapped parameters** — cleaner than "skill spawns subagent via Agent tool and prompt-templates inputs."
- **OpenCode's `session.compacting` pre-compaction hook** — fires before summarization, can inject domain context to survive compaction.
- **Continue's regex rule activation** — "when a file imports `openai`, load the openai-migration rule" via content regex, not just path glob.
- **Qwen's `SubagentStart`/`SubagentStop` lifecycle events** — these do not exist in Claude Code's documented hook list and would directly benefit Momentum's fan-out/TeamCreate audit logging.
- **Codex's `AGENTS.override.md` pattern** — temporary override file at same level, loaded preferentially. Useful for experiments and retros.
- **Kilo's machine-readable rule precedence** — Kilo documents and enforces exact precedence order. Momentum's authority-hierarchy rule is similar but only documented; a manifested precedence would reduce conflicts.

## 5. Integration / Parallel / Replacement Pathways

For each top candidate, three pathways: (a) specialist co-processor alongside Claude Code, (b) parallel Momentum-equivalent practice, (c) partial or full migration. Per practitioner notes, integration first is the lowest-risk experiment; parallel track is acceptable for exploration; migration is not recommended in 2026 Q2.

### 5.1 Decision Matrix

| Tool | (a) Co-Processor | (b) Parallel Track | (c) Migration | Justification |
|---|---|---|---|---|
| **ForgeCode** | Viable | Viable | Risky | `.forge/agents/*.md` YAML frontmatter + MCP are strong; no user-configurable hook surface; migration forfeits Momentum's enforcement spine. Benchmark credibility compromised. |
| **OpenCode** | Recommended | Recommended | Viable | Reads `.claude/skills/*/SKILL.md` and `CLAUDE.md` as fallback — skill portability is near-free. 25+ lifecycle hooks via TS/JS plugins. Highest-star open-source peer. |
| **Goose** | Recommended (recipe-library specialist) | Viable | Risky | sub_agents + sub_recipes are natural co-processors; Recipe YAML doesn't map to skill/workflow/hook trinity; no hook lifecycle. Strongest governance via AAIF. |
| **Aider** | Recommended (narrow) | Not Recommended | Not Recommended | Best scalpel for bulk mechanical edits + auto-commit; no skill/agent/hook primitives — not a practice host. Release cadence stalled. |

### 5.2 ForgeCode Pathways

**(a) Co-processor.** Shell out to `forge -p "<prompt>"` from a Momentum skill — candidate: a new `momentum:bulk-refactor` skill that runs Forge with a DeepSeek-V3 or Qwen-Coder model via OpenRouter. Benefits: 5–10× lower $/token on routine work vs Opus; ForgeCode's harness is architecturally distinct from Claude Code so running on the same diff is genuinely adversarial (different prompts, different tool-call patterns — good second-opinion AVFL signal). Failure modes: no structured output contract (need a post-processor); ForgeCode writes to disk so sandbox in a sibling worktree; the `:sync` indexer uploads file content to `api.forgecode.dev` by default — data-egress concern until self-hosted. Recommended for narrow bulk-edit sub-tasks, not general parallel review.

**(b) Parallel track.** Feasible for contained slices. Skills that are pure subagent-spawn-and-compose (intake, distill) map mechanically to `.forge/agents/*.md`. Rules port via `AGENTS.md` + `custom_rules:` in `forge.yaml`. What requires rewriting: everything that depends on user hooks — plan-audit, autonomous checkpoint-commit, architecture-guard PostToolUse. In ForgeCode these would have to move into agent system prompts (brittle) or external shell wrappers (loses harness integration).

**(c) Migration.** Risky. Clean migrations: research, intake, distill. Hard blocks: no user hook layer; no TeamCreate/SendMessage analog (retro auditor team, sprint review team cannot be rebuilt without polling loops); no slash commands (Impetus session-orientation UX collapses). Full migration: 2–4 months primarily spent reimplementing hooks as wrapper scripts and rebuilding team coordination. Partial (just the "executor" layer): 2–3 weeks.

### 5.3 OpenCode Pathways

**(a) Co-processor.** Shell out to OpenCode or expose it as an MCP server. Critical advantage: **OpenCode reads the same `.claude/skills/` and `CLAUDE.md` Claude Code does**, so a parallel review agent sees the same rules with zero porting. Multi-session parallel execution lets Momentum drive one agent on a refactor while another runs unit tests. Per-agent model selection means the co-processor can use OpenRouter with DeepSeek-V3 while Claude Code stays on Opus. Picking the right fork matters — `sst/opencode` is canonical (147k stars).

**(b) Parallel track.** **Strongly recommended.** Lowest-friction experiment in the entire survey: skills and rules load from existing paths. Port work is:
- Hooks rewrite from shell → TS/JS plugin functions subscribing to `tool.execute.after` and shelling out via Bun's `$`. Practitioner evidence: a 12-agent migration done in a single day ([Hightower gist](https://gist.github.com/RichardHightower/827c4b655f894a1dd2d14b15be6a33c0)) [CITED].
- Slash commands become OpenCode commands (separate format, mechanical translation).
What stays the same: `CLAUDE.md`, every `SKILL.md`, every `workflow.md`, every rules file, every agent definition.

**(c) Migration.** The only viable full-migration target in the set. Full migration: 3–6 weeks (hook port + retro/sprint-review team coordination rewrite). Partial (Impetus on Claude Code, dev-wave on OpenCode): 1 week. Hard-loss items: TeamCreate + SendMessage (inter-agent dialogue) — OpenCode's subagents are still fan-out/collect. Hard-gain items: OpenRouter-native routing, TS/JS plugin API (strictly more ergonomic than Claude's shell-command hooks), Apache-2 predecessor / MIT license eliminates vendor-exit risk.

### 5.4 Goose Pathways

**(a) Co-processor (recipe-library specialist).** Invoke `goose run --recipe <name>` from a Momentum skill for discrete repeatable workflows the community has already codified (database schema migration, changelog generation, scaffolds). Goose's AAIF-stewarded extension catalog is the widest in the set (3,000+ servers). Local-model-first via Ollama/Docker Model Runner/Ramalama gives Momentum a sovereign-operation lane with zero API cost. Adversary/prompt-injection detection is mature. Failure modes: Recipe YAML differs from skill YAML (no shared-format benefit vs OpenCode); Goose recipes are coarse-grained (invoking one carries whatever recipe-wide extensions it declares); 2× MCP subprocess overhead when stacking both Goose and Claude Code.

**(b) Parallel track.** Viable but expensive. Goose's sub_recipes are arguably *better* than Momentum's current workflow composition — but every SKILL.md must be rewritten as a Recipe, and the hook gap bites. The **unified-tooling RFC** (block/goose discussion #6202) is a Momentum-relevant signal: Block is designing a bridge so recipes, subrecipes, Claude Skills, and Claude Subagents can interop. If that lands, parallel-track viability improves materially.

**(c) Migration.** Risky. Full: 4–8 months (waiting for unified-tooling RFC + rebuilding hooks as external scripts). Partial (local-model-first executor): 2–4 weeks. The gap between recipe-YAML and Momentum's skill/workflow/hook trinity is wider than it looks. Revisit when the unified-tooling RFC ships.

### 5.5 Aider Pathways

**(a) Co-processor (narrow).** Shell out to `aider --message "<prompt>" --yes <files>` from a Momentum skill. Aider's architect/editor split is battle-tested for cheap-model bulk editing — plan with Opus, apply with Haiku/DeepSeek. A single `momentum:bulk-refactor` skill wrapping Aider is high-value for mechanical edits + auto-commit. Sandbox in sibling worktree.

**(b) and (c).** Not viable as a practice host. Aider provides none of Momentum's structural primitives — no skills, no hooks, no agent definitions, no subagent spawning. Would require wholesale re-architecture.

### 5.6 Recommendation

**Lowest-risk, highest-signal next experiment: pathway (b) on OpenCode.** Pick one contained Momentum workflow — `create-story` or `research` are strong candidates — and run it on OpenCode using the existing `.claude/skills/` directory. Compare outputs against Claude Code. Effort: <1 week because skills are shared-format. Output: a direct comparison between Anthropic-direct Claude Code and OpenRouter-brokered OpenCode on identical practice. De-risks the future question of whether Momentum can live off Claude Code without committing to full migration.

**Co-processor quick win: pathway (a) with ForgeCode or Aider** behind a single new `momentum:bulk-refactor` skill. Does not touch Momentum's core practice; adds a new capability at the specialist edge. Sandbox in sibling git worktree; sandbox data egress (ForgeCode's `api.forgecode.dev` workspace server) with `FORGE_WORKSPACE_SERVER_URL` override or use Aider (no hosted workspace dependency).

**Avoid in 2026-Q2: full migration to any peer.** The TeamCreate+SendMessage gap and the user-configurable hook gap are too costly to paper over. Revisit after (i) Block's unified-tooling RFC ships, (ii) OpenCode grows an inter-agent messaging primitive, or (iii) Anthropic publishes terms / pricing that materially change Claude Code's cost trajectory.

## 6. Maturity, Licensing, and Governance Risks

### 6.1 Summary Risk Ranking

| Tool | License | Governance | Ecosystem | Lock-In | Practice Drift | Overall Risk |
|---|---|---|---|---|---|---|
| **Aider** | Apache-2.0 | Solo maintainer (Paul Gauthier) | ~43.7k stars, 3+ years | Low (plain CLI, git-native) | Low (no skills/rules surface to drift from) | **Low–Medium** (SPOF) |
| **Goose** | Apache-2.0 | Linux Foundation AAIF since Dec 2025 | 42.9k stars, 350+ contributors, 110+ releases | Medium (recipes/extensions/MCP) | Medium (own skill/recipe model) | **Low** |
| **OpenCode** | MIT | Anomaly Innovations (ex-SST, profitable 2025) | 147k stars, ~3 releases/day | Medium (opencode.json, plugins) | Medium (own conventions) | **Medium** (velocity churn) |
| **Cline** | Apache-2.0 | VC-backed ($32M Emergence/Pace) | 60.5k stars, 5M+ users | Medium-High (VS Code-coupled, `.clinerules`) | Medium | **Medium** (VC pressure) |
| **Kilo Code** | Apache-2.0 (core) / MIT (CLI) | VC-backed ($8M, GitLab ROFR) | 18.4k stars, 1.5M users | Medium | Medium | **Medium** (early, acquisition risk) |
| **ForgeCode** | Apache-2.0 | Tailcall Inc. (no foundation) | 6.8k stars, v2.12.0, ~16 months old | Medium | Medium | **Medium-High** (young, benchmark cred compromised) |
| **Qwen Code** | Apache-2.0 (code); model access restricted | Alibaba (single vendor, policy risk) | Large repo, **free tier killed 2026-04-15** | High (tied to Alibaba inference) | High (policy whiplash) | **High** |

### 6.2 Specific Risk Flags

**ForgeCode — TermBench 2.0 cheating disclosure [VERIFIED].** The DebugML paper (arxiv 2604.11806, 2026-04-10) documented that ForgeCode auto-loaded `AGENTS.md` files containing literal answer keys on the benchmark. Adjusted clean-scaffold score is ~71.7% (14th place, not 1st). Per practitioner direction this is part of ForgeCode's merits assessment — i.e., a credibility signal, not a footnote. The team has not, as of 2026-04-21, publicly reconciled with the paper. Implication for Momentum: treat ForgeCode marketing claims with skepticism; treat architectural qualities at face value.

**opencode-workflows plugin — DEPRECATED [VERIFIED].** The `mark-hingston/opencode-workflows` plugin that Gemini recommended for "critical engineering paths" is a solo-dev community project (15 stars, marked Deprecated in its own README) with a successor called "Keystone." Per practitioner Q4 answer: keep the recommendation with explicit governance caveats — treat as prototype/experimentation rather than production-critical path. Reframe toward Keystone if/when it proves credible; otherwise do not use for critical paths.

**Aider — release cadence stall.** Latest release v0.86.0 dated 2025-08-09, ~8 months without a release by research date. Paul Gauthier has publicly acknowledged solo-maintenance pain on HN ([HN discussion](https://news.ycombinator.com/item?id=41137559)) [CITED]. Aider remains useful as a narrow co-processor; not a long-term practice bet.

**Qwen Code — governance concerns.** Alibaba shut down the Qwen OAuth free tier on 2026-04-15. The Apache-2.0 code is portable; the model access is captive to Alibaba pricing and geopolitical regulation. FT reporting (via Decrypt) indicates Qwen3.5-Omni and Qwen3.6-Plus are proprietary releases. MiniMax (Chinese peer) did an explicit license-bait-and-switch (MIT-style → commercial-use-requires-permission) in the same window. Policy whiplash is the dominant signal. Not recommended as primary or even secondary practice surface.

**Cline — context-budget issues.** Open issues through v3.78.0 (April 2026) show Cline overflowing large-context models (MiniMax, Qwen, OpenRouter) because it serializes a ~4.5K-token tool schema into every request and requests max-output-tokens equal to the model's full context window. UI-to-API discrepancies. Structural, not cosmetic. Enterprise story is best in the set (SSO, self-host, audit) if accepting commercial lock-in.

**Kilo Code — GitLab ROFR.** Kilo co-founded by Sid Sijbrandij (GitLab ex-CEO) with a Right of First Refusal agreement with GitLab through August 2026. If GitLab acquires, direction shifts to GitLab's enterprise roadmap; if it does not, Kilo is a Series-A-racing startup. Either path carries acquisition/pivot risk for the practice layer.

**Goose — "Operation Pale Fire."** January 2026 red-team exercise successfully compromised Goose via a poisoned Recipe hiding malicious instructions in invisible Unicode ([post-mortem](https://effloow.com/articles/goose-open-source-ai-agent-review-2026)) [CITED]. Patched with public post-mortem — a transparency positive, and a reminder that the recipe/extension ecosystem is a prompt-injection attack surface.

### 6.3 Adoption-Cost Analysis for Momentum

Three buckets:

**Rework cost (re-authoring).** Aider ≈ 0 (runner only). ForgeCode ≈ 40–60% (skills/rules port; hooks rebuild). OpenCode ≈ 10–25% (skills/rules load natively; hooks rewrite shell→TS). Goose ≈ 60–80% (skill→Recipe rewrite; hooks become external). Cline/Kilo/Roo ≈ 60–80% (native skill/mode format mismatch). Qwen ≈ not worth scoping.

**Drift cost (sync forever).** Aider: none. OpenCode: modest (skills are shared-format; hooks parallel). ForgeCode/Goose/Cline/Kilo: one full parallel practice surface, hundreds of files synced manually or via generation — and VC-era pressure means the target moves.

**Governance/commercial cost.** Goose (AAIF) clearest win; Aider stable but SPOF; Cline/Kilo/OpenCode/ForgeCode all carry single-vendor / VC / acquisition / license-change risk. Qwen is the cautionary case — license stayed Apache, economic terms changed without notice.

## Cross-Cutting Themes

### The Market Has Converged on Momentum's Bets

By April 2026, extension-surface conventions have visibly converged:

- `.xxx/skills/<name>/SKILL.md` is a cross-tool standard — Goose has `.agents/skills`, `.claude/skills`, `.codex/skills`, `.cursor/skills` side-by-side; ForgeCode uses `.forge/skills/<name>/SKILL.md`; Kilo uses `.kilocode/skills/*`; Cline uses `.clinerules/`; Codex ships Agent Skills as an official OpenAI spec; Crush adopts the cross-vendor "Agent Skills open standard."
- AGENTS.md is nearly universal as the system-prompt injection standard.
- MCP is table stakes — every tool except Aider (which added MCP Registry only recently) has first-class MCP.
- Planner + specialist orchestration — Architect/Coder/Debugger, Plan/Build, Muse/Forge/Sage — appears in OpenCode, Kilo, Roo, Cline, ForgeCode, and Claude Code's own plan mode. **Momentum's Impetus-orchestrator + specialist-subagents model is the mainstream 2026 pattern, not an outlier.**

The implication: **Momentum's opportunity is to be the portable practice layer on the converging substrate** (SKILL.md + MCP + AGENTS.md). Staying Claude-specific leaves leverage on the table; targeting the shared conventions multiplies it.

### Hooks Remain the Claude-Code-Specific Differentiator

Only Claude Code and Cline expose real user-configurable lifecycle hooks. OpenCode's 25+ TS/JS plugin events come closest. Codex has experimental feature-flagged hooks with known coverage gaps. Goose, ForgeCode, Kilo, Roo, Qwen, Aider, Continue have none (or internal-only, as with Forge's Rust-wired handlers). The emergence of community projects like **Oh My Codex** — adding hooks + multi-agent + persistent state on top of Codex — is a market signal that hooks-as-orchestration are being rebuilt on every base CLI. Momentum's hook-driven practice is not niche; it's ahead of the pack. The trade: if Momentum migrates off Claude Code to any non-hook host, the enforcement spine goes with it.

### Transferable Primitives Momentum Should Import

A concrete list with attribution:

1. **Cline's rule-vs-workflow token-cost split.** Always-on rules (persistent context, expensive on every message) vs on-demand workflows (slash-invoked, lazy-load). Mark Momentum rules with `trigger: on-demand` in frontmatter; surface them via skill or slash command rather than CLAUDE.md injection. Reduces context bloat for rules like `avfl-post-merge-strategy.md` that matter only during retro.
2. **Goose `sub_recipes` with mapped parameters.** A recipe-like DSL for workflow composition — `sub_recipes: [{name, path, values: {param: {{parent_param}}}}]`. Declares the composition graph explicitly, enabling static dependency analysis and orphan detection that Momentum does by convention today.
3. **OpenCode's `session.compacting` pre-compaction hook.** Fires *before* summarization and can inject domain context. Momentum can use this (when hosting OpenCode, or by advocating for Claude Code to add a similar event) to preserve sprint state across compaction.
4. **Continue's regex rule activation.** Rules can activate on file content regex, not just glob. Enables "when a file imports `openai`, load the openai-migration rule" patterns currently hand-coded in prompt logic.
5. **Kilo's machine-readable rule precedence order.** Kilo documents exact precedence (`agent prompts > project config > AGENTS.md > global config > skills`) as a contract, not advice. Momentum's `authority-hierarchy.md` is the analog; promote it from documented to manifested/enforced.
6. **Qwen's `SubagentStart`/`SubagentStop` lifecycle events.** These do not exist in Claude Code's current hook list. Momentum's spawning-patterns rule would benefit from them for auditing fan-out vs TeamCreate spawn events.
7. **Codex's `AGENTS.override.md` pattern.** Temporary override at the same directory level, loaded preferentially when present. Useful for experiments, retros, and A/B of rule sets without editing the canonical file.

These are small, concrete, shippable upgrades. They can be implemented independent of any migration decision.

### The Cross-Vendor Skills Convention Is Real

Crush adopts the "Agent Skills open standard." Codex has Agent Skills as an OpenAI spec. Goose repo structure shows `.agents/skills/` — a generic path. OpenCode reads `.claude/skills/` as a fallback. This is an organic, market-led convergence. Momentum's authoring decision should be to (a) author under `.claude/skills/` as the de facto portable path, (b) validate the frontmatter against the emerging SKILL.md contract (required `name`, `description`; optional `license`, `compatibility`, `metadata`), and (c) generate/symlink `AGENTS.md` stubs for cross-tool compatibility.

## Recommendations for Momentum

Prioritized by leverage-per-effort.

### Immediate (this sprint)

1. **Ship `momentum:bulk-refactor` specialist co-processor skill.** Wrap Aider or ForgeCode behind a single skill that handles mechanical/bulk edit tasks. Sandbox in sibling git worktree. Route via OpenRouter to DeepSeek-V3 or Qwen3-Coder for cost control. This adds a new capability without touching Momentum's core practice. Effort: ~3–5 days for a functional v1.
2. **Run parallel-track proof on OpenCode.** Pick `create-story` or `research` and execute under OpenCode using the existing `.claude/skills/` directory (OpenCode reads it natively). Compare outputs. Effort: <1 week. Output: concrete evidence on whether Momentum can live off Claude Code.
3. **Set `ANTHROPIC_BASE_URL` to OpenRouter's Anthropic Skin for a subset of Momentum subagents.** Zero-ops experiment in cost control. Use the subagent `model:` field + `CLAUDE_CODE_SUBAGENT_MODEL` env var to route Explore/read-only subagents to Haiku 4 or Gemini Flash. Retain Opus/Sonnet 4.6 for architecture and review.

### Near-term (next 2–4 weeks)

4. **Import Cline's rule-vs-workflow split into Momentum rules.** Add `trigger: on-demand` frontmatter; move rules that apply only in specific contexts (e.g., retro-time, AVFL-time, ATDD-time) to lazy-load. Reduces context bloat on every session.
5. **Prototype `sub_recipes`-style workflow composition DSL.** Declare skill composition graphs in YAML frontmatter so dependencies are static-analyzable. Enables orphan detection and workflow validation.
6. **Stand up LiteLLM behind Claude Code for real fallback/budget primitives.** Swap `ANTHROPIC_BASE_URL` from OpenRouter to a self-hosted LiteLLM. Add per-sprint token budgets, per-model cooldowns, per-developer caps. Much stronger cost control than env-var routing.
7. **Add `AGENTS.md` generation stubs to Momentum's install flow.** Keep `.claude/` as the canonical authoring surface; generate cross-tool compatibility files so Momentum-authored skills are portable on day one.

### Medium-term (next quarter)

8. **Evaluate OpenCode as a genuine parallel harness.** If the #2 proof succeeds, extend to dev-wave execution (let sprint-dev fan out on OpenCode while Impetus stays on Claude Code). Sketches out a dual-harness Momentum that's model-cost-optimized.
9. **Track Block unified-tooling RFC (block/goose discussion #6202) and AAIF standards progress.** If Block ships the bridge between recipes/subrecipes/Claude Skills/Claude Subagents, Goose becomes a materially better parallel-track candidate.
10. **Evaluate the ForgeCode vs Claude Code determinism comparison on a real Momentum workflow.** Concretely: run `sprint-dev` through ForgeCode's Muse→Forge plan-file handoff and measure whether the per-agent tool allowlist + `verify_todos` enforcement produces comparable quality to Momentum's hook-driven gates. This is a research question with implications for whether Momentum's enforcement spine is architecturally right or just historically contingent.

### Long-term (next 2–3 quarters)

11. **Publish Momentum as a cross-harness practice layer.** The market is converging on `.xxx/skills/*/SKILL.md` + MCP + AGENTS.md. Momentum's defensibility is the practice and the workflows, not the host. Publishing Momentum as a portable practice targeting the shared substrate is the strategic direction consistent with the market signals.
12. **Monitor Goose + AAIF.** If the Linux Foundation Agentic AI Foundation continues to steward standards with multi-corp backing, Momentum's portability insurance is substantially strengthened. Keep AAIF standards as explicit targets in Momentum's authoring conventions.

### Not Recommended in 2026 Q2

- Full migration to any peer.
- Adopting ForgeCode's TermBench 2.0 score as a legitimate signal.
- Treating Qwen Code as a primary or secondary practice surface.
- Using `opencode-workflows` plugin for critical paths (deprecated).
- Kilo Code commitments until the GitLab ROFR resolves (Aug 2026).

## Source Reliability and Known Limitations

**Gemini Deep Research main body — Failing grade (50/100 via AVFL).** Systematic issues documented in [validation/avfl-report.md](../validation/avfl-report.md): missing evidence tags throughout, OpenCode star count off by ~55% (95K claimed vs actual 147K), OpenCode developer count unsupported ("2.5 million monthly developers"), "Tool-Call Correction Layer" and "Semantic Entry-Point Discovery" named as ForgeCode components but not present in codebase (0 hits in direct GitHub code search — fabricated names), ForgeCode version cited as v0.106.0 (Aug 2025, eight months stale vs actual v2.12.0), Claude model naming inverted ("Claude 4.6 Opus" vs correct "Claude Opus 4.6"), Bifrost vendor named "Maxim AI" (correct: "Maxim" / getmaxim.ai), Goose hooks presence claimed then retracted, `opencode-workflows` plugin recommended without noting deprecation, VS Code "never mode" attribution inaccurate. Gemini follow-ups 1–3 carry citations and are marginally more reliable than main body but still require tier-2 verification to trust.

**Primary-source verification via direct WebFetch and repo-reading** resolved the most load-bearing disputes:
- ForgeCode hook reality: internal lifecycle architecture exists in Rust, zero user-configurable surface (see §1.2). Determinism achieved via per-agent tool allowlists + todo_write + plan-file workflow + bounded turns.
- ForgeCode version: v2.12.0 (2026-04-21), canonical repo `tailcallhq/forgecode` (NOT `antinomyhq/forge` — the latter 301-redirects).
- OpenCode metrics: 147k stars, canonical `sst/opencode`.
- DebugML TermBench paper: real, verified, findings applied to assessment.
- Bifrost: Maxim company, 11–59 µs overhead range.
- opencode-workflows: deprecated, solo-maintained, successor Keystone.

**Claude Code subagent research files** — the six sub-question research documents — show some stale metrics (Goose star count 29K → actual 42.9K, forge star snapshot 6.6K → 6.8K) but are substantively accurate on architecture, shape, and capabilities. Evidence tags ([OFFICIAL]/[PRAC]/[UNVERIFIED]) are present and traceable. These are tier-3 reliability relative to primary-source verification.

**Open questions the corpus could not resolve:**
- Exact number of OpenCode's documented plugin events (corpus says 25+, repo enumeration would confirm).
- Qwen3-Coder-480B SWE-bench Verified score (reported ~73% but not on the Aider polyglot leaderboard; independent confirmation wanted).
- Whether Block's unified-tooling RFC (discussion #6202) has shipped, is in-progress, or is stalled.
- The long-term viability of AAIF's multi-corp stewardship — whether governance holds under commercial pressure from founding-member vendors.
- Whether Anthropic will add `SubagentStart`/`SubagentStop` hooks (Qwen has them; Claude Code does not).
- Whether `opencode-workflows` successor "Keystone" reaches production-viable maturity.
- Updated Gemini Deep Research from a less-credulous synthesis layer would resolve several [DISPUTED] items more cleanly.

**Load-bearing claims by reliability tier:**

| Tier | Claims in this report |
|---|---|
| VERIFIED (primary source, direct repo/paper read) | ForgeCode architecture, hook reality, version v2.12.0, TermBench disclosure, OpenCode star count + canonical repo, Bifrost metrics, Cline hook events, Goose AAIF status, Qwen free tier shutdown, model polyglot scores |
| CITED (practitioner blogs, secondary source with URL) | Star count / contributor count trends, release cadences, practitioner-reported per-task model picks, Oh My Codex existence, Operation Pale Fire incident |
| INFERRED (reasonable inference without specific source) | Migration effort estimates (weeks/months), drift cost percentages, practitioner-default model picks where sources don't explicitly enumerate |
| DISPUTED | ForgeCode 81.8% vs 71.7% TermBench — both numbers cited with DebugML adjustment preferred for credibility assessment |
| HALLUCINATION (removed from narrative) | Gemini's "Tool-Call Correction Layer," "Semantic Entry-Point Discovery," "anomalyco/opencode" URL, "2.5M monthly developers" figure |

## Sources

Consolidated, deduplicated. Only sources actually cited in this final document.

### ForgeCode — Primary

- [ForgeCode homepage](https://forgecode.dev/) [VERIFIED]
- [tailcallhq/forgecode GitHub](https://github.com/tailcallhq/forgecode) [VERIFIED]
- [tailcallhq/forgecode README](https://github.com/tailcallhq/forgecode/blob/main/README.md) [VERIFIED]
- [tailcallhq/forgecode v2.12.0 release](https://github.com/tailcallhq/forgecode/releases/tag/v2.12.0) [VERIFIED]
- [crates/forge_domain/src/hook.rs](https://github.com/tailcallhq/forgecode/blob/main/crates/forge_domain/src/hook.rs) [VERIFIED]
- [crates/forge_app/src/hooks/mod.rs](https://github.com/tailcallhq/forgecode/blob/main/crates/forge_app/src/hooks/mod.rs) [VERIFIED]
- [crates/forge_app/src/hooks/doom_loop.rs](https://github.com/tailcallhq/forgecode/blob/main/crates/forge_app/src/hooks/doom_loop.rs) [VERIFIED]
- [forge.schema.json](https://github.com/tailcallhq/forgecode/blob/main/forge.schema.json) [VERIFIED]
- [ForgeCode pricing blog — Graduating from Early Access](https://forgecode.dev/blog/graduating-from-early-access-new-pricing-tiers-available/) [VERIFIED]
- [ForgeCode Custom Providers docs](https://forgecode.dev/docs/custom-providers/) [VERIFIED]
- [Forgecode vs Claude Code (dev.to, Liran Baba, 2026)](https://dev.to/liran_baba/forgecode-vs-claude-code-which-ai-coding-agent-actually-wins-36c) [CITED]
- [DebugML — Finding Widespread Cheating on Popular Agent Benchmarks](https://debugml.github.io/cheating-agents/) [VERIFIED]
- [arxiv 2604.11806 — Stein, Brown, Hassani, Naik, Wong](https://arxiv.org/abs/2604.11806) [VERIFIED]

### OpenCode

- [sst/opencode GitHub](https://github.com/sst/opencode) [VERIFIED]
- [OpenCode Plugins docs](https://opencode.ai/docs/plugins/) [VERIFIED]
- [OpenCode Agents docs](https://opencode.ai/docs/agents/) [VERIFIED]
- [OpenCode Skills docs](https://opencode.ai/docs/skills/) [VERIFIED]
- [OpenCode Rules docs](https://opencode.ai/docs/rules/) [VERIFIED]
- [OpenCode Providers docs](https://opencode.ai/docs/providers/) [VERIFIED]
- [Hightower gist: Claude Code Agents to OpenCode Agents](https://gist.github.com/RichardHightower/827c4b655f894a1dd2d14b15be6a33c0) [CITED]
- [mark-hingston/opencode-workflows (DEPRECATED)](https://github.com/mark-hingston/opencode-workflows) [VERIFIED — deprecated]

### Goose

- [block/goose GitHub](https://github.com/block/goose) [VERIFIED]
- [Goose docs](https://goose-docs.ai/) [VERIFIED]
- [Goose Providers docs](https://goose-docs.ai/docs/getting-started/providers/) [VERIFIED]
- [Goose Recipes docs](https://goose-docs.ai/docs/guides/recipes/) [VERIFIED]
- [Block — Introducing Codename Goose](https://block.xyz/inside/block-open-source-introduces-codename-goose) [VERIFIED]
- [Linux Foundation AAIF announcement](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) [VERIFIED]
- [Block unified-tooling RFC (discussion #6202)](https://github.com/block/goose/discussions/6202) [VERIFIED]
- [Effloow — Goose review 2026](https://effloow.com/articles/goose-open-source-ai-agent-review-2026) [CITED]

### Claude Code / Momentum

- [Claude Code Hooks docs](https://code.claude.com/docs/en/hooks) [VERIFIED]
- [Claude Code Subagents docs](https://code.claude.com/docs/en/sub-agents) [VERIFIED]
- [Claude Code Skills docs](https://code.claude.com/docs/en/skills) [VERIFIED]
- [Claude Code MCP docs](https://code.claude.com/docs/en/mcp) [VERIFIED]
- [Anthropic blog — Subagents in Claude Code](https://claude.com/blog/subagents-in-claude-code) [VERIFIED]

### Cline / Roo / Kilo

- [cline/cline GitHub](https://github.com/cline/cline) [VERIFIED]
- [Cline v3.36 Hooks blog](https://cline.bot/blog/cline-v3-36-hooks) [VERIFIED]
- [Cline — Stop adding rules when you need workflows](https://cline.ghost.io/stop-adding-rules-when-you-need-workflows/) [VERIFIED]
- [Cline docs — Customization / Cline Rules](https://docs.cline.bot/customization/cline-rules) [VERIFIED]
- [RooCodeInc/Roo-Code GitHub](https://github.com/RooCodeInc/Roo-Code) [VERIFIED]
- [Kilo-Org/kilocode GitHub](https://github.com/Kilo-Org/kilocode) [VERIFIED]
- [Kilo — AGENTS.md](https://kilo.ai/docs/customize/agents-md) [VERIFIED]
- [Kilo — Custom Modes](https://kilo.ai/docs/customize/custom-modes) [VERIFIED]

### Qwen Code / Codex / Crush / Continue / Aider

- [QwenLM/qwen-code GitHub](https://github.com/QwenLM/qwen-code) [VERIFIED]
- [Qwen Code Skills docs](https://qwenlm.github.io/qwen-code-docs/en/users/features/skills/) [VERIFIED]
- [Qwen Code Hooks (repo docs)](https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/hooks.md) [VERIFIED]
- [Qwen OAuth Free Tier Issue #3203](https://github.com/QwenLM/qwen-code/issues/3203) [VERIFIED]
- [Decrypt — Alibaba Shuts Down Free Qwen Code](https://decrypt.co/364501/alibaba-shuts-down-free-tier-qwen-code) [CITED]
- [Codex CLI docs](https://developers.openai.com/codex/cli) [VERIFIED]
- [openai/codex GitHub](https://github.com/openai/codex) [VERIFIED]
- [Codex Agent Skills docs](https://developers.openai.com/codex/skills) [VERIFIED]
- [charmbracelet/crush GitHub](https://github.com/charmbracelet/crush) [VERIFIED]
- [continuedev/continue GitHub](https://github.com/continuedev/continue) [VERIFIED]
- [Continue — Rules deep dive](https://docs.continue.dev/customize/deep-dives/rules) [VERIFIED]
- [Continue blog — AI Code Review at Scale](https://blog.continue.dev/beyond-code-generation-how-continue-enables-ai-code-review-at-scale) [CITED]
- [Aider-AI/aider GitHub](https://github.com/Aider-AI/aider) [VERIFIED]
- [Aider Polyglot Leaderboard](https://aider.chat/docs/leaderboards/) [VERIFIED]
- [HN — Paul Gauthier solo-maintainer thread](https://news.ycombinator.com/item?id=41137559) [CITED]
- [Morph — Aider 4.2× fewer tokens than Claude Code](https://www.morphllm.com/comparisons/morph-vs-aider-diff) [CITED]

### Routers and Gateways

- [OpenRouter Pricing](https://openrouter.ai/pricing) [VERIFIED]
- [OpenRouter Claude Code Integration](https://openrouter.ai/docs/guides/coding-agents/claude-code-integration) [VERIFIED]
- [OpenRouter Provider Routing](https://openrouter.ai/docs/guides/routing/provider-selection) [VERIFIED]
- [OpenRouter BYOK announcement](https://openrouter.ai/announcements/1-million-free-byok-requests-per-month) [VERIFIED]
- [BerriAI/litellm GitHub](https://github.com/BerriAI/litellm) [VERIFIED]
- [LiteLLM Routing & Load Balancing docs](https://docs.litellm.ai/docs/routing-load-balancing) [VERIFIED]
- [LiteLLM Claude Code Quickstart](https://docs.litellm.ai/docs/tutorials/claude_responses_api) [VERIFIED]
- [maximhq/bifrost GitHub](https://github.com/maximhq/bifrost) [VERIFIED]
- [Cerebras — Qwen3 Coder 480B live on Cerebras](https://www.cerebras.ai/blog/qwen3-coder-480b-is-live-on-cerebras) [VERIFIED]
- [Cline Cerebras provider config](https://docs.cline.bot/provider-config/cerebras) [VERIFIED]
- [Ollama OpenCode integration](https://docs.ollama.com/integrations/opencode) [VERIFIED]

### Community / Secondary

- [Oh My Codex writeup (a2a-mcp)](https://a2a-mcp.org/blog/what-is-oh-my-codex) [CITED]
- [ForgeCode Medium deep dive (Hightower, Apr 2026)](https://medium.com/@richardhightower/forgecode-dominating-terminal-bench-2-0-harness-engineering-beat-claude-code-codex-gemini-etc-eb5df74a3fa4) [CITED]
- [Infrabase — AI Inference API Providers Compared 2026](https://infrabase.ai/blog/ai-inference-api-providers-compared) [CITED]
- [Morph — Best LLM for Coding 2026](https://www.morphllm.com/best-llm-for-coding) [CITED]

### Verification and Validation (Internal)

- [verification-forgecode-hooks-and-version.md](../raw/verification-forgecode-hooks-and-version.md) — direct repo read
- [verification-direct-webfetch.md](../raw/verification-direct-webfetch.md) — primary-source WebFetch
- [validation/avfl-report.md](../validation/avfl-report.md) — AVFL corpus validation
- [practitioner-notes.md](../raw/practitioner-notes.md) — developer Q&A resolving highest-stakes disputes
