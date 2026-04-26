---
title: "everything-claude-code vs Momentum — Comparative Analysis"
date: 2026-04-26
type: Technical Research — Consolidated Report
status: Complete
content_origin: claude-code-synthesis
human_verified: true
derives_from:
  - path: raw/research-architecture-capabilities.md
    relationship: synthesized_from
  - path: raw/research-maturity-community.md
    relationship: synthesized_from
  - path: raw/research-feature-parallels.md
    relationship: synthesized_from
  - path: raw/research-ecc-superior.md
    relationship: synthesized_from
  - path: raw/research-momentum-superior.md
    relationship: synthesized_from
  - path: raw/research-portability.md
    relationship: synthesized_from
  - path: raw/research-philosophy.md
    relationship: synthesized_from
  - path: raw/research-integration-assessment.md
    relationship: synthesized_from
  - path: raw/verification-hackathon-and-identity.md
    relationship: synthesized_from
  - path: raw/deep-dive-continuous-learning.md
    relationship: synthesized_from
  - path: raw/gemini-deep-research-output.md
    relationship: synthesized_from
  - path: validation/iteration-1/consolidated.md
    relationship: validated_by
  - path: validation/iteration-1/fix-log.md
    relationship: validated_by
  - path: raw/practitioner-notes.md
    relationship: informed_by
---

# everything-claude-code vs Momentum — Comparative Analysis

## Executive Summary

`affaan-m/everything-claude-code` (ECC) and Momentum address agentic engineering from opposite ends of the same problem space. ECC is a **horizontal toolkit and distribution platform** — 48 agents, 183 skills, 79 commands, ~40 hook scripts, 6 default MCP servers, a 24-server reference catalog, install profiles, a Tkinter dashboard, an alpha Rust control plane, and adapters for Claude Code, Codex, OpenCode, Cursor, Gemini, Kiro, Trae, and CodeBuddy. Momentum is a **vertical practice** — a sprint state machine, sole-writer registries, the Adversarial Validate-Fix Loop (AVFL), Gherkin acceptance specs separated from dev agents, change-type story classification, retrospectives with auditor teams, decision documents, and an intake-queue event log. ECC asks "how do I make this harness produce better code, faster, more cheaply?" Momentum asks "how do I run a disciplined agentic engineering practice that survives AI generation outpacing human verification?"

The philosophical contrast is the spine of every other difference. ECC treats AI agents as **specialized workers to be dispatched**; Momentum treats them as **structurally unreliable producers requiring adversarial verification**. ECC's quality bar is *green tests + clean security scan = ship*. Momentum's is *parallel multi-lens dual-reviewer validation reaching a numeric pass score, plus retro that traces every defect to its upstream cause*. ECC distributes for maximum surface area across every harness and channel; Momentum distributes deeply for one harness with graceful degradation. ECC learns by automatic pattern extraction (Haiku observer → atomic instincts → confidence scoring → promotion); Momentum learns by human-curated failure tracing (AVFL findings → retro → triage → distill or decision).

The strategic verdict — which emerges from a component-by-component scorecard once the philosophy is named — is **stay independent and cherry-pick aggressively**. Momentum's value lives in its constraints, and ECC's value lives in its options. Wholesale integration would dilute both. There is, however, one cheap and high-leverage adoption: **`AGENTS.md` at the project root** — a Linux-Foundation-stewarded standard adopted by 60K+ projects and 25+ tools (Codex, OpenCode, Cursor, Gemini CLI, Aider, GitHub Copilot Coding Agent, Devin, Windsurf, etc.) that gives Momentum cross-CLI legibility for a few hours of work. Beyond that, three small wins from ECC are worth a sprint: the `silent-failure-hunter` adversary prompt (drop-in for AVFL's adversarial roster), the `repo-scan` community-origin pointer (wired into `momentum:assessment`), and the `post-edit-format` / `console-warn` *behaviors* re-implemented in Momentum's existing bash dispatcher pattern.

ECC's `continuous-learning-v2` deserves its own treatment. The mechanism is real — `observe.sh` hook, background Haiku analyzer, project-scoped instinct YAML files, `instinct-cli.py promote`, `/evolve` clustering — but its curation philosophy (auto-extract first, filter later) inverts Momentum's (validate first, write only what survives). The most plausible integration is **Path C**: adopt `observe.sh` as a lightweight session diary, skip the Haiku observer entirely, and let `momentum:triage` periodically classify findings into intake/distill/decision with the developer as the human gate.

Two corpus caveats colour confidence: the AVFL validation pass had three of eight validators degrade (Accuracy-Enumerator timed out, Coherence-Adversary stalled mid-stream, Domain-Adversary returned a stub), and the Gemini Deep Research input contained four critical fabrications (the imaginary `tools/agentshield/` directory, a non-existent `qflow` MCP server, and a `claude-mem` adoption recommendation built on the false premise that `claude-mem` is part of ECC) which were quarantined by a disputed-input header rather than retracted. Net confidence: high on architecture and feature counts (verified directly against the GitHub API and a shallow clone), high on philosophy (verified against ECC's own SOUL.md/RULES.md/CLAUDE.md and Momentum's local source), medium on community traction (commits and contributors are firm; star counts are bracketed as gameable surface metrics), and medium on the hackathon attribution claim (the README's "Anthropic Hackathon Winner" badge applied to ECC is misleading credibility inflation by association — Affaan IS a real hackathon winner, but for `zenith.chat` in Sep 2025, not for ECC).

---

## Section 1 — Philosophy & Framing

The single most useful sentence in this report: **ECC is a toolkit; Momentum is a practice.** Every other difference falls out of that.

### 1.1 Toolkit vs Practice

ECC's README opens "The performance optimization system for AI agent harnesses" and immediately offers a dashboard GUI to browse 48 agents, 183 skills, and 79 legacy commands ([README.md](https://github.com/affaan-m/everything-claude-code/blob/main/README.md)) (VERIFIED). The pitch is breadth: "12+ language ecosystems," "Production-ready agents, skills, hooks, rules, MCP configurations." The CLAUDE.md describes the project as "a collection of production-ready agents, skills, hooks, commands, rules, and MCP configurations." Five install profiles (`core`, `developer`, `security`, `research`, `full`) exist to help users *pick a subset*, not to enforce one. The implicit invitation is *use what you want*.

Momentum's CLAUDE.md opens "Momentum provides the practice layer for agentic engineering: global rules, agents, hooks, and workflows that enforce quality standards across all projects" (VERIFIED). The README declares an Authority Hierarchy: **Specifications > Tests > Code. Agents never modify specifications or pre-existing tests to make code pass.** A Producer-Verifier Separation rule reads "The agent that writes code does not review it. Verification happens in a separate context with a separate agent whose only job is to find problems." These are not configurable knobs; they are framed as load-bearing rules.

The clearest expression of the divergence: ECC's catalog is the product. Momentum's principles are the product, and the catalog exists to enforce them.

### 1.2 Governance Model

ECC is a **community-extended single-maintainer** project under MIT license. CONTRIBUTING.md actively solicits new agents, framework experts, DevOps specialists, and language reviewers. The v1.10.0 release notes thank "30+ community PRs merged — Contributions from 30 contributors across 6 languages" plus Korean and Chinese translations. Recent commits include community PRs (#1546, #1511, #1522) directly to `main`. Affaan Mustafa is BDFL and authored ~66% of the 1,465 commits; the next 10 humans collectively contribute ~150 commits. (VERIFIED — GitHub API contributors endpoint, 2026-04-26.)

Momentum is a **single-author closed practice** at this stage. No CONTRIBUTING.md exists. The project's `version-on-release.md` describes a personal release cadence: "When a sprint completes and merges to main: bump `skills/momentum/.claude-plugin/plugin.json` version." The git log shows a single author, and the master plan is described as "Authoritative for: model, status, architecture decisions, and roadmap" (VERIFIED).

ECC is a marketplace. Momentum is a manifesto. ECC's success is measured by PR throughput; Momentum's by whether the practice produces better outcomes for one developer.

### 1.3 Target User

ECC targets a broad professional audience. From `ecc.tools`: "Thousands of developers and engineers across various Fortune 500 teams." Language ecosystem coverage spans TypeScript, Python, Go, Java, Kotlin, C++, Rust, Perl, PHP, Swift, Dart/Flutter, plus framework packs for Spring Boot, Django, Laravel, NestJS, Nuxt 4, Next.js Turbopack. The GitHub App offers freemium/pro/enterprise tiers, indicating commercial team usage as a target.

Momentum targets a narrower archetype: the **solo developer directing AI agents on a single complex codebase**. The canonical planning artifact is `AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md`. The Impetus orchestrator persona — "field commander meeting your operator for the first time" with `PERSONA.md / BOND.md / CREED.md` sanctum files — assumes a single human owner. Memory file `feedback_quickfix_epic_ad_hoc.md` codifies single-developer ergonomics ("don't ask the developer; always use 'ad-hoc'") (CITED — practitioner memory).

ECC scales out: more languages, more frameworks, more contributors. Momentum scales depth: one practice, deeply enforced for one person.

### 1.4 AI-Agent Treatment

This is the single biggest philosophical fork. ECC treats agents as **specialized workers to be dispatched**. SOUL.md: "Agent-First — route work to the right specialist as early as possible." Agents are discrete units (`planner.md`, `architect.md`, `tdd-guide.md`, `code-reviewer.md`, `security-reviewer.md`) with explicit `tools`, `model`, and frontmatter. The metaphor is *team of consultants*. The trust model is *trust the specialist for their domain*; quality emerges from picking the right one.

Momentum treats agents as **suspect producers requiring adversarial verification**. The README is explicit: "The agent that writes code does not review it. Verification happens in a separate context with a separate agent whose only job is to find problems. Verifiers produce findings — they never modify code." Agents are also given *deep persona and continuity* — Impetus has a sanctum of identity files, a creed, and "Three Laws." Memory file `feedback_impetus_orchestration_model.md` enforces the orchestration shape: "Impetus ALWAYS spawns all subagents directly. No direct-invocation workarounds. Exclusive write authority per file." (CITED — practitioner memory.)

ECC's mental model: *agents are skilled hires; manage them.* Momentum's mental model: *agents are unreliable producers; structure the work so their output is independently verified, by another agent, in a fresh context.*

### 1.5 Validation Philosophy

ECC assumes agents are **mostly reliable**, with safety nets. RULES.md mandates "Write tests before implementation and verify critical paths" and notes a "minimum 80% test coverage" expectation. The `verification-loop`, `eval-harness`, and `checkpoint` skills exist for high-stakes flows. AgentShield (a separate sibling repo, `affaan-m/agentshield`, *not* part of ECC — see Section 8 glossary) is positioned for security: "1,282 tests, 102 rules" with an `--opus` flag for red-team/blue-team/auditor pipelines. But these are opt-in, situational tools.

Momentum assumes agents are **structurally unreliable** by default. The README declares an entire debt taxonomy specifically for this: "Verification Debt — Unreviewed or inadequately tested AI-generated output accumulates faster than human-written code because generation is cheap. Layered verification (acceptance tests, unit tests, adversarial review, human review) counteracts this." The AVFL skill encodes empirical calibration into its defaults: "Do not use Haiku for Enumerator validators. Benchmarking showed Haiku enum-medium produces false-pass scores (92/100 while missing a critical architectural contradiction)." Validation is a parallel, multi-lens, dual-reviewer pipeline (8 subagents — 1 Enumerator + 1 Adversary per lens × 4 lenses) that runs *every* sprint. (VERIFIED — `skills/momentum/skills/avfl/SKILL.md`.)

ECC's validation is a **safety net** invoked when the developer chooses. Momentum's validation is a **load-bearing wall** that runs whether the developer asks or not.

### 1.6 Learning Model

ECC learns by automatic pattern extraction. Continuous-learning-v2 fires `observe.sh` on every Claude tool call (PreToolUse + PostToolUse), writes JSON observations to `~/.claude/homunculus/projects/<hash>/observations.jsonl`, and a background Haiku agent (off by default, gated by `session-guardian.sh`'s time-window/cooldown/idle checks) periodically reads the last 500 lines and writes atomic instinct YAML files with confidence scores 0.3–0.9. Section 5 of this report covers the mechanism in depth.

Momentum learns by human-curated failure tracing. The AVFL skill produces findings; the retro skill mines transcripts via DuckDB and runs an auditor team; findings flow to `intake-queue.jsonl`; `momentum:triage` classifies them into six classes (ARTIFACT, DISTILL, DECISION, SHAPING, DEFER, REJECT) with mandatory human approval; approved DISTILL items go to `momentum:distill` for surgical edits to a specific rule, reference, or skill prompt, with a git commit on every change. (VERIFIED — `skills/momentum/skills/triage/`, `distill/`, `retro/SKILL.md`.)

ECC learns *patterns of doing* and accumulates a long tail of low-confidence atomic candidates. Momentum learns *causes of failure* and edits the practice itself surgically. ECC's curation question: did this happen often enough? Momentum's curation question: did the human approve it?

### 1.7 The Recurring Axis

| Axis | ECC pole | Momentum pole |
|---|---|---|
| Primary unit | Component (skill/agent/hook) | Principle (rule/workflow) |
| Optimization target | Marginal session | Long-run practice |
| Trust in AI | Mostly reliable specialists | Structurally unreliable producers |
| Quality model | Tests + reviewers + scanners | Adversarial multi-lens validation + upstream traceback |
| Distribution | Maximum surface (every harness, every channel) | Minimum surface (one harness deeply, everything else as docs) |
| Pedagogy | Tips and external guides | First-principles prose with citations |
| Governance | Open community + BDFL | Closed solo author |
| Cadence | Continuous monthly minors | Time-boxed immutable sprints |
| Specs | Tests are specs | Behavioral specs govern tests govern code |
| Learning loop | Pattern extraction → new skills | Failure tracing → upstream rule edits |

ECC's design philosophy is **amplification** — take the agent harness you have and make it dramatically more productive across every language and context. Momentum's design philosophy is **constraint** — accept that AI agents are unreliable producers and build a sustainable practice (separation of producer/verifier, adversarial validation, attention-aware checkpoints, upstream root-cause fixing) that survives that fact.

Both projects are coherent inside their own frame. The disagreement is about whether the bottleneck of AI-assisted development is **what tools the agent has access to** (ECC) or **how the human-agent loop is structured to catch what the agent gets wrong** (Momentum).

---

## Section 2 — Component-by-Component Scorecard

The scorecard inventories everything substantive ECC ships and pairs each item with Momentum's analogue (or its absence). Effort estimates assume the developer doing the work is already familiar with both codebases; estimates are inclusive of writing the change, validating it, and committing.

### 2.1 Plugin Distribution & Architecture

**ECC.** Multi-channel: Claude Code marketplace, npm package `ecc-universal@1.10.0`, manual installer (`install.sh` / `install.ps1` / `npx ecc-install --profile full`), `ecc list-installed`/`ecc doctor`/`ecc repair` CLI subcommands. Five install profiles backed by manifests/install-profiles.json + manifests/install-modules.json + manifests/install-components.json. State persisted to `~/.claude/ecc/state.db` (sql.js / SQLite-in-WASM) with JSON-Schema-validated schema. Cross-platform installer pair (POSIX bash + native PowerShell). `configure-ecc` skill drives install conversationally. (VERIFIED — `manifests/`, `scripts/install-*.js`, `scripts/lib/state-store/`.)

**Momentum.** Single Claude Code plugin marketplace channel. `plugin.json` is minimal (4 fields). No installer beyond the marketplace. Memory note codifies this: "momentum install shell script is obsolete — use standard Agent Skills installation. Keeps resurfacing." (CITED.)

**Effort to adopt.** Selective install architecture is a **multi-sprint investment** (~2–3 sprints of focused work) and is **not recommended** until Momentum's catalog grows past ~50 skills. The current 25-skill plugin doesn't justify the complexity. **Watch only.**

### 2.2 Cross-Harness Portability

**ECC.** Real per-target adapter pattern. `.claude-plugin/plugin.json` (Claude Code primary), `.codex/config.toml` + `.codex-plugin/plugin.json` (Codex CLI, full support with `[mcp_servers.*]` blocks, agents, named profiles `strict`/`yolo`), `.opencode/opencode.json` + `.opencode/index.ts` (OpenCode TypeScript plugin with 13 agents, 31 commands, 37 skills, 11+ hook events), `.cursor/hooks.json` + `.cursor/hooks/adapter.js` (Cursor adapter that translates Cursor's stdin to Claude-Code-shaped payload, then re-invokes the canonical `scripts/hooks/*.js`), `.gemini/GEMINI.md` (thin, plus `scripts/gemini-adapt-agents.js` rewrites tool names: Read → `read_file`, Bash → `run_shell_command`, etc.). Plus experimental `.kiro/`, `.trae/`, `.codebuddy/`, and an Antigravity install target. (VERIFIED.)

**Momentum.** Claude Code only. Plugin hooks use `$CLAUDE_PROJECT_DIR` and `$CLAUDE_TOOL_INPUT_FILE_PATH` (CC-specific env vars). Skill frontmatter uses `model: claude-opus-4-6` (CC-specific model handles). Slash-command pattern (`/momentum:foo`) is CC-specific.

**Effort to adopt.** **AGENTS.md at the project root: a few hours.** This is the cheapest and highest-leverage portability win. AGENTS.md is a Linux-Foundation-stewarded standard (donated December 2025 alongside MCP and goose) used by 60K+ projects and 25+ tools (VERIFIED — agents.md, linuxfoundation.org). Momentum should adopt this immediately. Beyond AGENTS.md, full multi-harness ports (Codex / OpenCode / Cursor / Gemini) would require months of adapter work and explicitly contradict Momentum's depth-over-breadth positioning. **Recommend AGENTS.md adoption; defer everything else.** See Section 6 for detailed treatment.

### 2.3 Hooks Layer

**ECC.** `hooks/hooks.json` registers ~14 distinct hook IDs across PreToolUse / PostToolUse / Stop / UserPromptSubmit / SessionStart / PreCompact, each delegating to a Node script under `scripts/hooks/` (~40 scripts total). Notable:

- **GateGuard fact-force** — three-stage pre-edit gate (DENY → FORCE investigation → ALLOW retry). Demands the agent list importers, schemas, and quote the user instruction before the first edit. Reported "+2.25 points avg quality lift in two A/B tests" (ECC self-report; mechanism verified via `scripts/hooks/gateguard-fact-force.js` + tests).
- **Config-protection** — blocks linter/formatter config edits ("steers agent to fix code instead of weakening configs").
- **Block-no-verify** — refuses `git commit --no-verify` and similar bypasses.
- **Continuous-learning observer** — async PreToolUse/PostToolUse capture (10s timeout) feeding observations.jsonl.
- **MCP health-check** — pre-call probe.
- **Post-edit accumulator** — records JS/TS files for batched format+typecheck at Stop time.
- **Post-edit console-warn** — flags `console.log` after edits.
- **Design-quality-check** — warns on generic-looking UI edits.
- **Suggest-compact** — nudges `/compact` at logical task boundaries.
- **Cost-tracker, governance-capture, desktop-notify** — operational hooks.

Runtime gating via `ECC_HOOK_PROFILE=minimal|standard|strict` and `ECC_DISABLED_HOOKS=...`. 24 hook test files under `tests/hooks/`. (VERIFIED.)

**Momentum.** Targeted hooks: plan-audit gate (blocks `ExitPlanMode` until the plan file contains a `## Spec Impact` section), commit checkpoint (project rule), file-protection PreToolUse hook, version-bump check, lint-format dispatcher. Three bash dispatchers total. No tests on hook scripts. (VERIFIED — `skills/momentum/hooks/hooks.json`, `.claude/momentum/hooks/`.)

**Effort to adopt.**
- `block-no-verify`: ~1 hour as a small bash hook in Momentum's existing dispatcher. **Recommend adopt.**
- `post-edit-format` / `console-warn` *behavior*: ~2 hours re-implemented in bash, not the JS. **Recommend adopt.**
- GateGuard fact-forcing: ~1 sprint to design the equivalent for Momentum's flow (the +2.25 quality lift is empirical evidence the pattern works, but the implementation is heavyweight and Momentum's plan-audit gate already serves the spec-traceability need at the right granularity). **Watch.**
- Hookify family (conversational hook authoring): **ignore.** Inverts Momentum's "practice-shaped, not user-shaped" hook policy.
- Per-hook annotation convention (`id`, `description` fields): ~1 hour. **Recommend adopt** as a hook-policy doc.

### 2.4 MCP Integrations

**ECC.** Root `.mcp.json` pre-configures 6 servers with pinned versions: `github` (`@modelcontextprotocol/server-github@2025.4.8`), `context7` (`@upstash/context7-mcp@2.1.4`), `exa` (HTTP), `memory` (`@modelcontextprotocol/server-memory@2026.1.26`), `playwright` (`@playwright/mcp@0.0.69`), `sequential-thinking` (`@modelcontextprotocol/server-sequential-thinking@2025.12.18`). Separately, `mcp-configs/mcp-servers.json` is a 24+ server **reference catalog** with placeholder credentials (jira, firecrawl, supabase, omega-memory, vercel, railway, cloudflare-*, clickhouse, magic, fal-ai, browserbase, etc.). `scripts/lib/mcp-config.js` merges ECC's MCP catalog into the user's existing config; `scripts/hooks/mcp-health-check.js` verifies servers respond before tool calls. Multiple skills assume MCP availability (`jira-integration`, `documentation-lookup`, `agent-introspection-debugging`). (VERIFIED.)

**Momentum.** Root `.mcp.json`: `{"mcpServers": {}}`. Empty stub. No MCP-related skills, no MCP setup script.

**Effort to adopt.** **Ignore the MCP catalog.** A bundled MCP catalog is a per-project decision; Momentum should not bundle one. The valuable insight is the *names* of useful servers (sequential-thinking, omega-memory, context7) which can be referenced in onboarding docs. ~30 minutes to write a brief reference doc.

### 2.5 Skills Catalog Breadth

**ECC.** 183 skill directories spanning seven axes: language patterns (~30 skills covering Python, Go, Kotlin, Rust, C++, C#, Swift, Dart/Flutter, Perl, .NET, PyTorch), framework patterns (Spring Boot, Django, Laravel, NestJS, Nuxt 4, Next.js Turbopack, Compose Multiplatform, Android Clean Architecture), workflow practice (`tdd-workflow`, `agentic-engineering`, `verification-loop`, `eval-harness`, `agent-eval`, `continuous-learning-v2`, `code-tour`, `codebase-onboarding`), operator/business (`customer-billing-ops`, `finance-billing-ops`, `customs-trade-compliance`, `production-scheduling`, `inventory-demand-planning`, ~15 ops skills), domain (`healthcare-cdss-patterns`, `healthcare-emr-patterns`, `hipaa-compliance`, `defi-amm-security`, `llm-trading-agent-security`), security (`security-review`, `security-scan`, `security-bounty-hunter`, `gateguard`, `safety-guard`), content/media (`manim-video`, `remotion-video-creation`, `frontend-slides`, `liquid-glass-design`, `seo`, `article-writing`, `content-engine`), and self-referential (`everything-claude-code`, `configure-ecc`, `skill-stocktake`, `ecc-tools-cost-audit`). (VERIFIED — `skills/` listing.)

**Momentum.** 25 skills, all about practice mechanics: sprint-planning, sprint-dev, sprint-manager, retro, AVFL, intake, distill, decision, create-story, dev, code-reviewer, architecture-guard, agent-guidelines, plan-audit, refine, feature-grooming, feature-status, feature-breakdown, epic-grooming, assessment, quick-fix, research, triage, upstream-fix, impetus. Language-agnostic by design. (VERIFIED.)

**Effort to adopt.**
- Per-language reviewers (10+ files): **ignore.** Conflicts with Momentum's "practice not toolkit" stance and creates a language-matrix maintenance burden.
- Per-language build-resolvers: **ignore.** Build resolution belongs in `bmad-quick-dev` or per-project rules.
- Domain skills (healthcare, energy, customs): **ignore.** No place in an agentic-engineering practice module.
- `silent-failure-hunter` agent prompt: ~30 minutes to drop into AVFL's adversarial roster. **Recommend adopt** (see Section 3).
- `repo-scan` skill (community-origin pointer to `haibindev/repo-scan`): ~1 hour to wire into `momentum:assessment`. **Recommend adopt** (see Section 3).
- `skill-stocktake` *idea* (LLM-based skill quality eval over the catalog): rebuild as an AVFL-corpus-mode wrapper, ~1 sprint. **Recommend adopt next.**
- `strategic-compact` *behavior* (compaction nudge at task boundaries): fold into Impetus's Orient phase, ~half a day. **Recommend adopt next.**
- `eval-harness` skill (capability/regression/pass@k): **watch.** Momentum has DEC-010 fixture-based testing as practice primitive heading the same direction with cleaner alignment.
- `council` skill (Architect/Skeptic/Pragmatist/Critic deliberation): **watch.** Momentum's design assumes deliberation already happened (via assessment, research, or external thinking) before `decision` records it. Adopting council would shift the philosophy toward in-system deliberation.
- `agentic-engineering` skill (~50-line principle skill): **ignore.** Momentum's practice is broader and the philosophical content already lives in Momentum's README and rules.

### 2.6 Multi-Agent Orchestration

**ECC.** Process-level and cross-harness:
- `dmux-workflows` skill — multi-agent orchestration via dmux (tmux pane manager for AI agents). Patterns 1–5 cover research+implement, multi-file feature, test+fix loop, cross-harness, code-review pipeline.
- `scripts/orchestrate-worktrees.js` + `scripts/lib/tmux-worktree-orchestrator.js` — declarative tmux+worktree orchestration with workers in parallel tmux panes against isolated worktrees.
- `team-builder` skill — interactive picker for ad-hoc parallel teams.
- `commands/multi-plan.md`, `multi-execute.md`, `multi-backend.md`, `multi-frontend.md`, `multi-workflow.md` — gated on external `ccg-workflow` runtime.
- `pm2.md` — PM2 process supervisor integration.
- `loop-operator` agent + `loop-start.md` / `loop-status.md` + `autonomous-loops` + `continuous-agent-loop` skills — autonomous loops with stall detection.
- `chief-of-staff` agent — orchestration of other agents.

(VERIFIED.)

**Momentum.** Agent-level inside one Claude Code session (Fan-Out via `Agent` tool spawns, or TeamCreate for collaborative teams) and worktree-isolated for sprint-dev. `~/.claude/rules/spawning-patterns.md` codifies the Fan-Out vs TeamCreate decision. Impetus is the practice orchestrator; sprint-dev is the parallel-worktree executor. Memory note: "Impetus ALWAYS spawns all subagents directly. No direct-invocation workarounds. Exclusive write authority per file." (CITED.)

**Effort to adopt.**
- `loop-operator` escalation list (no progress across two consecutive checkpoints, repeated failures with identical stack traces, cost drift outside budget window): use as a **checklist when hardening sprint-dev**. ~1 hour to extract into a reference doc.
- tmux+worktree orchestrator: **ignore.** Momentum delegates to cmux for terminal multiplexing, and its sprint-dev pattern (in-process Fan-Out + worktree isolation) is the practice-aligned answer. Adopting ECC's pattern would fork the orchestration model.
- PM2 integration: **ignore.** Out of scope.
- Council deliberation: see 2.5.

### 2.7 Adversarial Validation

**ECC.** Three relevant skills:
- `santa-method` — "Multi-agent adversarial verification with convergence loop" (306 lines, single skill). Phase 1 Generate → Phase 2 dual independent review (Reviewer B and Reviewer C in parallel, context-isolated) → Phase 3 Verdict Gate (binary PASS/FAIL — both must pass) → Phase 4 Fix Cycle. Attributed to "Ronald Skelton — Founder, RapportScore.ai." This is the closer AVFL analogue conceptually.
- `gan-style-harness` — Generator + Evaluator + Playwright loop. Three roles (Planner → Generator → Evaluator), iterates 5–15 times, scores against 4 weighted criteria (Design Quality, Originality, Craft, Functionality). Engineered for *building a whole app from a prompt* with live-app evaluation. Cites "Anthropic's Harness Design for Long-Running Application Development" (March 24, 2026).
- `verification-loop` — single-agent six-phase checklist (build → typecheck → lint → tests → security scan → diff review). Closer to a procedural verification than an adversarial loop.

(VERIFIED.)

**Momentum.** AVFL — four-phase pipeline (VALIDATE → CONSOLIDATE → EVALUATE → FIX). Distinguishing properties:
- Four orthogonal lenses: Structural Integrity, Factual Accuracy, Coherence & Craft, Domain Fitness.
- Two framings per lens — Enumerator (systematic) and Adversary (intuitive) — explicitly designed to break shared-bias failure.
- Four named profiles: `gate` (1 agent, no fix), `checkpoint` (1 per lens, 1 fix attempt), `full` (8 agents, 4 fix iterations), `scan` (8 agents, no fix, structured handoff).
- Benchmarked role-tier configuration: 36 runs across 3 models × 3 effort levels × all roles → Enumerator=Sonnet/medium, Adversary=Opus/high, Consolidator=Haiku/low, Fixer=Sonnet/medium. Anti-patterns called out: "Do not use Haiku for Enumerator validators."
- Skepticism scheduling: hardcoded high (3) on iteration 1, low (2) on subsequent.
- Stage parameter (`draft`/`checkpoint`/`final`) controls whether absence counts as a finding.
- Corpus mode for cross-document validation with authority-hierarchy resolution.
- Three benchmarked variants: `avfl-2lens`, `avfl-3lens`, `avfl-declining`.

(VERIFIED.)

**Verdict.** Strong philosophical overlap, materially different shape. Both reject single-agent self-evaluation. AVFL is the more sophisticated framework on every axis except brevity — santa-method is shorter and more digestible but lacks lens decomposition, profile selection, scan mode, role-tier benchmarks, skepticism scheduling, stage parameter, and corpus mode. Gan-style-harness solves a different problem (live app generation+evaluation, not artifact validation).

**Effort to adopt.**
- `silent-failure-hunter.md` agent prompt: ~30 minutes to add to AVFL's adversarial roster. **Recommend adopt now.**
- Santa-method's binary-verdict + dual-reviewer shape: **ignore.** AVFL is materially more sophisticated; backporting would weaken Momentum's quality posture.
- Gan-style-harness Playwright live-app evaluation: **watch.** Relevant only if Momentum starts shipping user-facing apps that need live evaluation.

### 2.8 TDD/EDD/Test Infrastructure

**ECC.** Deep TDD framework:
- `tdd-workflow` skill, `tdd-guide` agent, `commands/tdd.md`.
- Per-language TDD/testing skills: `python-testing`, `golang-testing`, `kotlin-testing`, `rust-testing`, `csharp-testing`, `cpp-testing`, `perl-testing`, `springboot-tdd`, `django-tdd`, `laravel-tdd`.
- `eval-harness` skill — formal evaluation framework with capability evals, regression evals, code-based / LLM / human graders, pass@k and pass^k metrics.
- `agent-eval` skill — head-to-head agent comparison on YAML task definitions, git-worktree isolation, pass-rate/cost/time metrics.
- `healthcare-eval-harness` — domain-specific eval framework.
- 91 Jest test files + 4 Python tests in the repo's own test suite. Validators (`scripts/ci/validate-agents.js`, `validate-commands.js`, `validate-hooks.js`, `validate-rules.js`, `validate-skills.js`, `validate-install-manifests.js`, `validate-workflow-security.js`, `validate-no-personal-paths.js`, `check-unicode-safety.js`) lint the catalog itself.
- 36-job CI matrix (3 OS × 3 Node × 4 package managers, with Bun-on-Windows excluded).

(VERIFIED.)

**Momentum.** EDD/TDD discipline injected into stories by `create-story`'s change-type classification. AVFL validates a wider variety of artifacts (not just code/agents) but has no comparable pass@k or capability/regression eval taxonomy. The repo ships a single `momentum-tools.py` test plus four BMAD-owned tests; nothing CI-grade for Momentum's own catalog.

**Verdict.** Both endorse EDD/TDD; ECC has a deeper framework, Momentum has tighter workflow integration via the change-type classifier (5 types: skill-instruction, script-code, rule-hook, config-structure, specification, with type-specific test guidance injected into Dev Notes).

**Effort to adopt.**
- `eval-harness` framework: **watch.** Momentum's DEC-010 fixture-based regression testing is heading the same direction with cleaner alignment to the practice.
- Catalog validators (`validate-skills.js` etc.): **adopt with modification**, ~2 sprints to build the equivalent in bash + small Python. Momentum has no automated way to detect a malformed SKILL.md frontmatter, a broken hook script, or a regression in `triage` behavior before a sprint relies on it. This is a real gap.
- `agent-eval` head-to-head benchmark (Claude Code vs Aider vs Codex on YAML tasks): **watch.** Useful when Momentum needs to evaluate model/agent choice empirically.
- 36-job CI matrix: **ignore.** Momentum's tooling is markdown + bash + tiny Python CLI; the matrix complexity is not justified.

### 2.9 Code Review

**ECC.** 12+ language-specific reviewer agents (`typescript-reviewer`, `python-reviewer`, `go-reviewer`, `rust-reviewer`, `java-reviewer`, `kotlin-reviewer`, `csharp-reviewer`, `cpp-reviewer`, `flutter-reviewer`, `database-reviewer`, `security-reviewer`, `healthcare-reviewer`). Plus specialized reviewers: `silent-failure-hunter`, `pr-test-analyzer`, `comment-analyzer`, `type-design-analyzer`, `refactor-cleaner`, `code-simplifier`. Plus security review skills (`security-review`, `security-scan`, `security-bounty-hunter`). Plus `commands/code-review.md` and `commands/review-pr.md`. (VERIFIED.)

**Momentum.** `code-reviewer` skill — language-agnostic adversarial reviewer with read-only tools, "do not invoke directly" — gated by AVFL. Plus `architecture-guard` (read-only enforcer that diffs sprint changes against numbered architecture decisions, severity-ranks findings CRITICAL/HIGH/MEDIUM/LOW), `upstream-fix` (traces quality failures upstream to spec/rule/workflow root cause). (VERIFIED.)

**Verdict.** ECC has dramatically more language-specific reviewers; Momentum has a tighter integration into the AVFL flow.

**Effort to adopt.**
- ECC's `code-reviewer` agent: **ignore.** Less rigorous than Momentum's (only "report findings >80% confident" with no fixer loop). Substituting would weaken quality.
- `silent-failure-hunter`: see 2.7.
- Per-language reviewers: **ignore** per 2.5.

### 2.10 Memory Systems

**ECC.** Continuous-learning-v2 (covered in Section 5). Plus MCP-level memory (`memory` server pre-wired in `.mcp.json`; `omega-memory` template in catalog with "persistent agent memory with semantic search, multi-agent coordination, and knowledge graphs"). Plus `commands/save-session.md`, `resume-session.md`, `sessions.md`. Plus `strategic-compact` skill + `pre-compact.js` + `suggest-compact.js` hooks for context-budget compaction. (VERIFIED.)

**Momentum.** File-based persistent memory at `~/.claude/projects/<project-hash>/memory/` keyed by project. Index file `MEMORY.md` references typed feedback/reference/project notes (18 feedback files at scan time). Impetus sanctum at `_bmad/memory/impetus/` with `INDEX.md`, `PERSONA.md`, `CREED.md`, `BOND.md`, `MEMORY.md`, `CAPABILITIES.md`. (VERIFIED.)

**Verdict.** Strong functional overlap, opposite curation philosophies. Both isolate by project hash. Momentum's memory is human-curated and typed; ECC's is agent-curated with confidence scoring.

**Effort to adopt.** See Section 5 — recommend Path C (observation diary feeding triage). Strategic-compact's nudging behavior folded into Impetus's Orient phase, ~half a day.

### 2.11 Decision Documents & Deliberation

**ECC.** `architecture-decision-records` skill — Michael Nygard format (Context / Decision / Alternatives Considered / Consequences). Auto-detects decision moments from phrases like "we decided to…" Plus `council` skill — convenes four advisors (Architect, Skeptic, Pragmatist, Critic) for ambiguous decisions, explicitly delegates Skeptic/Pragmatist/Critic to fresh subagents with only the question (anti-anchoring mechanism). (VERIFIED.)

**Momentum.** `decision` skill — "Decision recorder — not deliberator. The thinking already happened. This skill captures what was decided, links it to source material, and bridges to story creation." Walks findings, records adopt/reject/defer, writes a linked decision document. (VERIFIED.) Memory note: never use SDR/ASR acronyms — say "decision document" / "assessment document" (CITED).

**Verdict.** Strong overlap on capture; ECC adds in-system deliberation (council).

**Effort to adopt.**
- ADR format: Momentum already does this implicitly. ~1 hour to confirm format alignment in `momentum:decision` references.
- Council deliberation: **watch.** Adopting would shift Momentum's philosophy toward in-system deliberation. Momentum currently assumes deliberation already happened (via assessment, research, or external thinking).

### 2.12 Sprint Discipline (Momentum-only territory)

**Momentum.** `sprint-manager` skill — sole writer of `stories/index.json` and `sprints/index.json`. State machine (backlog → ready-for-dev → in-progress → review → verify → done; terminal: done, dropped, closed-incomplete). 15 completed sprints + 4 quickfix sprints in `_bmad-output/implementation-artifacts/sprints/`. `sprint-planning` skill produces team_composition with per-story roles, change_type, guidelines, test_approach, wave, dependencies. `sprint-dev` runs dependency-driven story development across worktrees with post-merge AVFL and team review. `retro` skill mines transcripts via DuckDB, runs an auditor team, writes findings document, closes sprint. (VERIFIED.)

**ECC.** **None.** Tree scan confirms zero hits for `sprint`, `backlog`, `epic`, `retro`, `state-machine`, `index.json` across 2,662 path entries. ECC has session-scoped workflows (`feature-dev.md`: Discovery → Codebase Exploration → Clarifying Questions → Architecture Design → Implementation → Quality Review → Summary; `loop-operator` agent for autonomous loops) but no concept of a sprint, no backlog persistence between sessions, no story status, no concurrency control on a shared index. (VERIFIED — recursive tree grep.)

**Effort to adopt.** N/A — this is Momentum's territory. The retro auditor-team pattern, the intake-queue.jsonl event log, the change-type classifier, the architecture-guard pattern-drift detector, and the plan-audit hook gate are all Momentum capabilities ECC entirely lacks.

### 2.13 Behavioral Specifications (Momentum-only territory)

**Momentum.** Gherkin specs per story written to `sprints/{sprint-slug}/specs/{story-slug}.feature`. Specs are written for an E2E Validator that is a black-box agent — explicitly cannot read source. Outsider Test enforced. Reference template at `references/gherkin-template.md` with anti-patterns enforced via post-generation validation (no AC numbers, no Phase numbers in scenario names, no internal agent/tool/file refs). Decision 30 black-box separation: dev agents implement against plain-English ACs in the story file; only the validator sees the `.feature` files. (VERIFIED.)

**ECC.** Tree scan: 0 matches for `gherkin`, 0 matches for `atdd`, 0 matches for `.feature`, 0 matches for `acceptance`. ECC has `e2e-testing`, `tdd-workflow`, `tdd-guide` agent, and Playwright integrations, but no behavioral spec format, no Outsider Test discipline, and no separation between code-blind validators and dev agents. ECC's TDD pair instructs the agent to write test code as the spec; Momentum runs a behavioral specification layer above test code.

**Effort to adopt.** N/A — Momentum-only.

### 2.14 Statusline / Dashboard / Cosmetics

**ECC.** `examples/statusline.json` — a single-line bash script that renders `user:cwd branch* ctx:% model time todos:N` with truecolor RGB ANSI escapes. Plus `ecc_dashboard.py` — a 39 KB Tkinter desktop app for browsing installed plugin components. Plus `ecc2/` Rust TUI (`ecc-tui` v0.1.0 with `ratatui`, `crossterm`, `tokio`, `rusqlite`, `git2`, `clap`) — alpha control plane exposing `dashboard`, `start`, `sessions`, `status`, `stop`, `resume`, `daemon`. (VERIFIED.)

**Momentum.** `feature-status` skill renders an HTML planning artifact showing feature coverage gaps and story assignments; opens in a browser pane. No statusline. No GUI dashboard. (VERIFIED.)

**Effort to adopt.**
- Statusline: ~1 hour to drop ECC's example into Momentum docs as an example. **Watch / cosmetic.**
- Tkinter dashboard: **ignore.** Different audience, not Momentum's responsibility.
- ECC 2.0 Rust control plane: **watch.** Re-evaluate at GA. The Rust dependency would be a step-change in Momentum's maintenance posture (currently markdown + bash + tiny Python CLI).

### 2.15 Documentation & Onboarding

**ECC.** 68 KB English README plus Chinese (36 KB), 17 docs under `docs/` including `SKILL-DEVELOPMENT-GUIDE.md`, `SELECTIVE-INSTALL-ARCHITECTURE.md`, `SELECTIVE-INSTALL-DESIGN.md`, `SESSION-ADAPTER-CONTRACT.md`, `MANUAL-ADAPTATION-GUIDE.md`, `TROUBLESHOOTING.md`, `token-optimization.md`, `hook-bug-workarounds.md`. Localized docs in `ja-JP`, `ko-KR`, `pt-BR`, `tr`, `zh-CN`, `zh-TW`. 6 KB `COMMANDS-QUICK-REF.md`. Three "longform/shortform/security" guides (15-29 KB each). 8 example CLAUDE.md files. 13 KB `CONTRIBUTING.md`. (VERIFIED.)

**Momentum.** 33-line CLAUDE.md. Rich planning artifacts under `docs/planning-artifacts/` and `_bmad-output/`, but those are internal practice artifacts. No tutorials, no language-specific examples, no internationalization, no contributor guide.

**Verdict.** ECC has invested in user-facing docs; Momentum has invested in internal planning docs. ECC offers a more legible front door for evaluators.

**Effort to adopt.** Building Momentum-equivalent external docs would be ~2 sprints. **Defer.** Momentum's audience is currently "the maintainer" — docs scale up when the audience does. **Recommend a small README revision** to make the philosophy/practice distinction loud (the current 33-line CLAUDE.md undersells what Momentum is) — ~half a day.

### 2.16 Summary Table

| Category | Momentum has | ECC has | Recommended action |
|---|---|---|---|
| AVFL / dual-reviewer validation | Yes (4 lenses × 2 framings × 4 profiles, benchmarked roles) | santa-method (closer analogue, simpler) + gan-style-harness | Keep AVFL; adopt `silent-failure-hunter` |
| Gherkin / ATDD specs | Yes | None | Keep |
| Sprint state machine | Yes | None | Keep |
| Change-type story classification | Yes | None | Keep |
| Intake queue / triage | Yes | None | Keep |
| Decision documents | Yes | Yes (ADR + council) | Keep; watch council |
| Feature/epic taxonomy | Yes | None | Keep |
| Plan-audit / spec-impact gate | Yes | GateGuard (different purpose) | Keep |
| Architecture-guard / pattern drift | Yes | None | Keep |
| Retro w/ auditor team | Yes | None | Keep |
| Cross-harness portability | None | Multi-target adapter | **Adopt AGENTS.md** |
| MCP integrations | Empty stub | 6 default + 24+ catalog | Reference catalog only |
| Selective install | None | Profiles + state store | Defer |
| Statusline | None | Example | Cosmetic |
| Catalog validators | None | 9 CI scripts | Adopt-with-modification (~2 sprints) |
| Continuous learning | distill (manual, surgical) | continuous-learning-v2 (auto, confidence-scored) | **Path C** (Section 5) |
| `silent-failure-hunter` | None | Yes | **Adopt now** |
| `repo-scan` (community) | None | Pointer | **Adopt now** |
| `post-edit-format` / `console-warn` | Partial | Yes | **Adopt behavior, not JS** |
| `block-no-verify` | None | Yes | **Adopt** |
| `skill-stocktake` idea | Partial (in-flight) | Yes | Adopt-as-AVFL-corpus next |
| `strategic-compact` behavior | None | Yes | Fold into Impetus next |
| Per-language patterns/reviewers/build-resolvers | None | Yes (~30 skills) | Ignore |
| Domain skills (healthcare, energy, etc.) | None | Yes (~15) | Ignore |
| Council deliberation | None | Yes | Watch |
| Eval-harness / agent-eval | None (DEC-010 in flight) | Yes | Watch |
| Hookify (conversational hook authoring) | None | Yes | Ignore |
| ECC 2.0 Rust control plane | None | Alpha | Watch (re-evaluate at GA) |

---

## Section 3 — Strategic Verdict

The verdict, in one sentence: **stay independent and cherry-pick aggressively.**

### 3.1 Adopt-as-Is (one sprint, three small commits)

**1. `silent-failure-hunter.md` into AVFL's adversarial roster.** A 40-line agent prompt with one job: hunt empty catch blocks, swallowed errors, dangerous fallbacks, and lost stack traces. Tools: Read/Grep/Glob/Bash. Model-agnostic, free of ECC-specific tooling. Slots into `/Users/steve/projects/momentum/skills/momentum/skills/avfl/agents/silent-failure-hunter.md` (or as a referenced sub-prompt). Cost: ~30 minutes. Conflicts: none. (VERIFIED — `agents/silent-failure-hunter.md`.)

**2. `repo-scan` (community-origin pointer) into `momentum:assessment`.** Classifies every file in a repo as project / third-party / build-artifact, detects 50+ embedded libraries, produces a four-level verdict (Core Asset / Extract & Merge / Rebuild / Deprecate). ECC ships only the SKILL.md pointer — the implementation lives at `https://github.com/haibindev/repo-scan`. Slot into `/Users/steve/projects/momentum/skills/momentum/skills/repo-scan/` as a standalone skill, invoked by `assessment`, not by Impetus directly. Tag with `origin: community`. Cost: ~1 hour. Conflicts: depends on third-party scanner being installed; mitigation is to print "scanner not installed; skipping" rather than failing. (VERIFIED — `skills/repo-scan/SKILL.md`.)

**3. `post-edit-format` + `post-edit-console-warn` *behaviors* re-implemented in bash.** Take the *behavior* (formatter auto-detect — Biome vs Prettier; non-blocking debug-statement warnings), not the JS. Re-implement as a small bash addition to the existing Momentum hook chain. Avoid adding Node as a runtime dependency for hooks — Momentum has stayed bash-only and that simplicity is a feature. Cost: ~2 hours. Conflicts: none; reinforces the existing single-bash-dispatcher pattern.

### 3.2 Adopt-with-Modification (next sprint or two)

**4. `block-no-verify` hook.** Refuse `git commit --no-verify` and similar bypasses. ECC's `scripts/hooks/block-no-verify.js` is the reference; re-implement in bash as one entry in Momentum's PreToolUse dispatcher. Cost: ~1 hour. Conflicts: none. The `~/.claude/rules/git-discipline.md` already says "Never skip hooks (--no-verify) unless the user has explicitly asked for it" — this hook makes the rule load-bearing.

**5. `AGENTS.md` at the project root.** See Section 6 for full treatment. Cost: a few hours.

**6. Skill-stocktake idea, built as AVFL-corpus-mode wrapper.** Run skill-quality eval over `skills/momentum/skills/**/SKILL.md` using AVFL's existing corpus mode rather than as a standalone Quick-Scan harness. The corpus-mode infrastructure already enumerates files, distributes to validators, and consolidates findings; ECC's stocktake harness duplicates that. Keep ECC's judgment criteria and results-cache idea. Tied to in-flight `impetus-eval-triage` story. Cost: ~1 sprint. Conflicts: must respect Momentum's sole-writer pattern — emit findings as story-stub files via `momentum:intake`, never write to indexes directly.

**7. `strategic-compact` *behavior* folded into Impetus.** Don't ship the JS hook. Extend Impetus's Orient phase to print a one-line context-pressure hint when the session shows tool-call accumulation patterns Impetus already inspects. Cost: ~half a day. Conflicts: minor — Momentum's hook policy is "single PreToolUse / PostToolUse / Stop dispatcher"; adding a competing hook would violate that.

**8. Hook annotation convention (`id` / `description` fields).** Borrow from ECC's `hooks/hooks.json`. Document as the canonical pattern in `skills/momentum/references/hooks-config.json` so future hook contributions stay disciplined. Cost: ~1 hour.

**9. Catalog validators** (`validate-skills.sh`, `validate-agents.sh`, `validate-hooks.sh`, `validate-rules.sh`). Built in bash, lint Momentum's own catalog. ECC's `scripts/ci/validate-*.js` are the reference. Cost: ~2 sprints. Conflicts: none. **This is a real gap** — Momentum has no automated way to detect a malformed SKILL.md frontmatter, a broken hook script, or a regression in `triage` behavior before a sprint relies on it.

### 3.3 Watch-and-Learn (no integration)

**10. `ecc2/` Rust control plane.** Alpha-quality Rust crate (`ratatui` + `rusqlite` + `git2`) proposing a "session control plane above individual harness installs": multi-session state, observability, risk scoring, worktree-aware scaffolding. README states "alpha quality, not yet a public GA release." Re-evaluate at GA. Currently: alpha-grade, Rust dependency expands Momentum's maintenance posture, not aligned with cmux-as-substrate.

**11. `continuous-learning-v2`.** See Section 5. Recommend Path C (observation diary feeding triage) but defer adoption pending evaluation.

**12. `skill-comply` reference implementation.** Auto-generates compliance scenarios at three prompt-strictness levels, runs `claude -p`, captures stream-json tool traces, classifies whether agents actually follow rules/skills. Useful when DEC-010 (fixture-based regression testing) implementation begins.

**13. Selective-install manifest architecture.** Profiles / modules / components / state store. Bookmark the schemas. Revisit only if Momentum's plugin grows past ~50 skills.

**14. `loop-operator` escalation list.** Use as a checklist when hardening sprint-dev (no progress across two checkpoints, repeated failures with identical stack traces, cost drift outside budget window). Don't ship the agent.

**15. Council deliberation skill.** Adopting would shift Momentum's philosophy. Currently Momentum's design assumes deliberation already happened.

**16. `eval-harness` framework.** Momentum's DEC-010 is heading the same direction. Re-read when DEC-010 implementation begins to harvest test-case ideas.

**17. ECC's gan-style-harness Playwright live-app evaluation.** Relevant only if Momentum starts shipping user-facing apps that need live evaluation.

### 3.4 Ignore (do not import)

- **Per-language reviewers** (12+ files of toolkit duplication; conflicts with Momentum's "practice not toolkit" stance).
- **Per-language build-resolvers** (build resolution belongs in `bmad-quick-dev` or per-project rules).
- **Vertical-domain skills** (healthcare, energy, customs, logistics, etc. — no place in an agentic-engineering practice module).
- **ECC's TDD pair (`tdd-workflow` + `tdd-guide`).** Implementation-heavy ("80%+ coverage, npm test, edge cases list") and mismatches Momentum's behavior-not-implementation Gherkin stance. Adopting would weaken existing discipline.
- **Bundled MCP catalog.** Per-project decision.
- **Hookify family** (`hookify`, `hookify-configure`, `hookify-help`, `hookify-list`). Inverts Momentum's "practice-shaped, not user-shaped" hook policy.
- **ECC's `code-reviewer` agent.** Less rigorous than Momentum's; would weaken quality posture if substituted.
- **Most ECC scripts** (installer, session adapters, codex/opencode bridges, Tkinter dashboard) — they serve ECC's many-harnesses cross-portability mandate.
- **`agentic-engineering` skill** (~50-line principle skill). Momentum's practice is broader and the philosophical content already lives in Momentum's README and rules.

### 3.5 Fork (track the source without integrating)

- **`ecc2/`** — possibly fork-worthy when GA. If ECC2 reaches 1.0, it could become a layer Momentum sits on top of (Momentum sprints become first-class entities in an ECC2 session store). Until then: read the code, watch the issues.
- **`skill-comply`** — keep a reference checkout for harvest of compliance test scaffolding when Momentum's micro-eval runner story starts.
- **`the-security-guide.md`** — 28 KB security longform. Reference text to cite from `momentum:research` when security topics surface.

### 3.6 Architectural Reasoning

Momentum's value is **constraint discipline**: sole-writer files (`stories/index.json`, `sprints/index.json`), AVFL gates, `intake-queue.jsonl` event log, sprint-manager validation of state transitions, sprint-dev's dependency-driven execution, and the rules cascade (global → project → session). Every constraint is a feature.

ECC's value is **breadth and battle-testing**: 48 agents, 183 skills, 79 commands, hooks tested in a real CI matrix (95+ test files), a hardened Node installer, a Rust control plane in alpha, and a public marketplace presence. Every option is a feature.

Importing ECC broadly would replace a few hundred lines of constraint with thousands of lines of optional capability — exactly the inversion that broke earlier "kitchen-sink" practice modules. The adoption candidates above are the rare cases where ECC's tested code matches a missing Momentum slot without dragging in the toolkit philosophy.

### 3.7 Key Conflict Surfaces to Keep Watching

- **Sole-writer pattern.** Any imported skill that writes to `stories/index.json` or `sprints/index.json` directly violates Momentum's invariant. ECC's stocktake-style skills are flagged for this risk.
- **Hook count.** Momentum runs three bash dispatchers; ECC runs ~30 hook entrypoints across `scripts/hooks/`. Each new Momentum hook should be justified against the dispatcher pattern.
- **Runtime drift.** Momentum is markdown + bash + a small Python CLI. Adopting any ECC component that requires Node at runtime expands the dependency surface — reject unless the value is overwhelming.
- **Sprint discipline.** ECC's `loop-operator` and `continuous-learning-v2` are agent-driven autonomous loops; Momentum's loops run inside sprint-dev with explicit story state transitions. Don't blur the boundary.
- **AVFL authority.** AVFL is Momentum's quality gate. Imported review/eval skills must integrate *under* AVFL, not alongside it.

### 3.8 The Bottom Line

ECC is a treasure of patterns wrapped in a toolkit philosophy Momentum should not adopt. Quarry it carefully, ship the small wins (silent-failure-hunter, repo-scan, post-edit hooks, block-no-verify, AGENTS.md), and stay independent.

---

## Section 4 — Maturity & Community Traction

The headline figures invite a hot-take ("167K stars in 90 days!") that is the wrong place to start. Per Steve's explicit guidance, this section leads with verified-commit and contributor metrics — the harder-to-game signals — and brackets star counts as gameable surface metrics.

### 4.1 Verified-Commit and Contributor Metrics

All numbers verified against the GitHub REST API on 2026-04-26 (VERIFIED — `api.github.com/repos/affaan-m/everything-claude-code/...`).

- **Total commits on main:** ~1,465 (derived from the Link header `rel="last"` at `per_page=1`).
- **Commits in the last 25 days (since 2026-04-01):** 430. That is ~17 commits/day average over the last 4 weeks — very high, comparable to active commercial monorepos.
- **Total contributors:** 159 (computed from Link header on `/contributors?per_page=1`).
- **Top contributor:** `affaan-m` with 965 commits — ~66% of all commits.
- **Next 9 humans contribute ~150 commits combined:** `pangerlkr` (47), `pvgomes` (15), `Lidang-Jiang` (14), `ozoz5` (12), `pythonstrup` (12), `shimo4228` (12), `chris-yyau` (9), and others.
- **Bots:** GitHub Copilot (22 commits), dependabot (14), `claude` / `Claude` GitHub App, `ecc-tools[bot]`.
- **Long tail:** 159 contributors total, with ~140 having 1–3 commits each. Healthy for drive-by docs/translation/typo-fix PRs.
- **Bus factor:** **1.** Affaan Mustafa wrote ~66% of all commits. The next 10 humans collectively contribute ~10% of his volume.
- **Releases:** 12 tagged releases between 2026-01-22 (`v1.0.0`) and 2026-04-05 (`v1.10.0`). One release every ~8 days.
- **Issue close rate:** 85.6% (415 closed / 485 total) — very healthy.
- **PR merge rate:** 36.0% (368 merged / 1,025 closed) — moderate. The remaining 657 closed-but-not-merged PRs suggest active triage and rejection of low-value drive-bys.
- **Recent issue response time:** sub-day on community-reported bugs (sample: #1541 closed in 1.2h, #1538 in 3.2h, #1537 in 3.3h, #1534 in 3.1h).
- **CI matrix:** 36 base jobs (3 OS × 3 Node × 4 package managers, with Bun-on-Windows excluded). SHA-pinned action versions. Concurrency cancellation. Minimal `contents: read` permissions. Matrix `fail-fast: false`. Reusable workflow modules. (VERIFIED — `.github/workflows/ci.yml`.)
- **Release pipeline:** tag format `vX.Y.Z` regex validation, `package.json` version must match the tag, `tests/scripts/build-opencode.test.js` verifies package payload before publishing. (VERIFIED — `.github/workflows/release.yml`.)
- **Dependency hygiene:** dependabot active (14 commits among top contributors). Recent PRs include `chore(deps): bump the minor-and-patch group` and `chore(deps): bump actions/setup-node`. `.tool-versions` pins Node 20.19.0 and Python 3.12.8 (asdf/mise compatible).

These are the metrics that matter. **ECC is genuinely actively maintained, professionally engineered, and led by a verifiable maintainer.** The "hot README riding the hype curve" hypothesis is rejected on these signals alone.

### 4.2 The Star Count — Bracketed as Gameable

Per Steve's instruction: *"Many of the AI projects are faking their github stars... that doesn't necessarily mean that the project itself is doing it, it might be external, or they have a single malicious bot or developer causing this misalignment. In my experience that doesn't mean that the project isn't legit, but it definitely DOES mean that the github stars and many other metrics should be wholly thrown out. The actual commits, bug fixes, etc. are a better metric."* (CITED — practitioner notes.)

With that framing, the star data:

- **Stars (GitHub API, 2026-04-26):** 167,488. (VERIFIED.)
- **Forks:** 25,969.
- **Watchers (subscribers):** 864.
- **Repo age:** 3 months and 1 week (created 2026-01-18).
- **Star velocity:** ~2× growth in ~5 weeks (early March to late April). At ~1,800 stars/day sustained for ~90 days, this is unprecedented in dev-tooling history.
- **Star-to-download conversion:** ~0.6%. Weekly npm downloads of `ecc-universal`: ~1,000/week. (VERIFIED — npm registry / shields.io live download badge.)

**These numbers should be treated as awareness signals, not adoption signals.** The Medium analysis ("inside the 82K-star agent harness that's dividing the developer community", 2026-03-18) explicitly characterizes the community as split: advocates praise time savings; skeptics call it over-engineered and note "minimal Discussion forum activity" relative to star count. (CITED — medium.com/@tentenco.) Hacker News submissions of the repo returned 2 results, both 2 points each. Affaan himself has not posted to HN. The HN-side story is much smaller than the Twitter/X-side story (where Affaan claims 3M-5M+ views and 25M+ impressions for his guides).

The fork-to-star ratio (~15.5%) is high for a developer-tools repo, indicating people are not just bookmarking — they're cloning and customizing. This argues against pure star-farming. But the ~0.6% star-to-install conversion suggests external amplification (viral X threads, a hackathon halo effect, content-farm coverage) is part of the curve.

**Bottom line on stars:** real but inflated. Not fabricated. Treat as awareness, not adoption. Lead with commits and contributors.

### 4.3 The Hackathon Attribution Issue

Per Steve's explicit instruction to "dig into this" and his statement *"I don't want fakeness"* (CITED), this gets its own treatment. The verification subagent's findings:

**The README's "Anthropic Hackathon Winner" badge applied to ECC is misleading credibility inflation by association.** ECC is not a hackathon entry and won no hackathon. The badge appears in the README header (line 22: "**140K+ stars** | **21K+ forks** | **170+ contributors** | **12+ language ecosystems** | **Anthropic Hackathon Winner**") and in the lede (line 37: "From an Anthropic hackathon winner"). These ambiguous claims don't name which hackathon, which project, or which year, and they imply ECC itself is the winning entry, which is not supported by any evidence. (VERIFIED — README contents and subagent verification.)

**However, Affaan Mustafa IS a real hackathon winner — for a different project.** The README's Background section (lines 1349–1350) accurately describes the actual win: "Won the Anthropic x Forum Ventures hackathon in Sep 2025 with @DRodriguezFX — built zenith.chat entirely using Claude Code." This event is real and verifiable:

- Forum Ventures × Anthropic Agentic AI Hackathon, NYC, Sep 12, 2025. (VERIFIED — Forum Ventures event page, Devpost.)
- Win is multiply corroborated: zenith.chat homepage self-identifies as "Anthropic × Forum Ventures Hackathon Winner"; Affaan's personal site lists "$15k in Anthropic credits, first place among 100+ teams"; GitHub profile README lists "Zenith Chat — 1st / 100+ people, $15k credits"; third-party X amplification (@godofprompt, Sep 2025).
- Win is *not* independently confirmed by Forum Ventures or Anthropic via official press release. The Devpost project gallery was never published publicly. The "100+ teams" claim is inconsistent with Devpost's 19 registrants and the event page's "75 curated participants." Probable, not proven. (CITED — verification subagent.)

**The Cerebral Valley × Anthropic "Built with Opus 4.6" hackathon (Feb 10–16, 2026) is real, definitively documented, with five named winners — ECC and Affaan are not among them.** Official Anthropic blog post lists CrossBeam (Mike Brown, 1st), Elisa (Jon McBee, 2nd), PostVisit.ai (Michał Nedoszytko, 3rd), TARA (Kyeyune Kazibwe, "Keep Thinking" Prize), and Conductr (Asep Bagja Priandana, Special Prize — Creative Exploration). (VERIFIED — claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon.)

ECC's README correctly says AgentShield (the sibling repo at `affaan-m/agentshield`, *not* part of ECC) was "Built at the Claude Code Hackathon (Cerebral Valley x Anthropic, Feb 2026)" — this is a provenance claim, not a win claim. Affaan participated in this hackathon as a builder; AgentShield emerged from that event. Defensible.

**The problem is the lede.** "Anthropic Hackathon Winner" applied to ECC's repo header — without disambiguation — creates a false impression that ECC's technical approach was validated by hackathon competition. It wasn't. ECC is a configuration repository, not a hackathon submission.

**Affaan Mustafa is real.** Identity verification: ResearchGate profile (UW Applied Mathematics graduate student), BS in Math-CS + BA in Business Economics from UCSD, AA from Bellevue College, MIT Applied Data Science Professional Certificate, published research (HyperMamba paper on SSRN), elizaOS core contributions (verifiable in elizaOS repo, 17K+ stars), LinkedIn, personal website with detailed project history, active multi-platform social presence. Not a synthetic identity. (VERIFIED — multiple independent sources.)

**Synthesis decision:** This is a credibility-inflation issue, not a fabrication. Affaan's win is real but for a different project; ECC's badge is misleading by association. For Momentum, this matters because evaluators reading the ECC README may inflate ECC's validation by ~one notch unless they read carefully. The technical work in ECC stands on its own — the hackathon framing does not enhance or diminish that work.

### 4.4 Production Readiness — The Honest Score

**Pro-production signals (verified):**
- Cross-platform CI matrix (36 jobs).
- Dependabot + automated dependency PRs.
- SHA-pinned actions.
- Semver-strict release pipeline with tag-vs-package version validation.
- 12 numbered releases in 94 days, with detailed changelog entries.
- MIT license (permissive, dependable).
- SECURITY.md, CODE_OF_CONDUCT.md, CONTRIBUTING.md present.
- 6 translated READMEs (international community uptake).
- Sub-day issue response time on recent samples.
- Real Rust 2.0 control plane in-progress (~1.8MB Rust code, builds with `cargo`).
- Companion product surface at `ecc.tools` and a GitHub App in marketplace.
- Real human maintainer with verifiable identity, startup, and public X/LinkedIn presence.

**Caution signals (verified):**
- **Bus factor = 1.** 66% of commits from one person; next contributor has 4.9% of his volume. If Affaan stops, momentum dies.
- **Star-to-download gap.** 167K stars vs ~1K weekly npm downloads = ~0.6% conversion. Many stargazers are bookmarking, not running.
- **README claims are partly hyped.** "1,282 automated tests" cannot be verified at exact count without running the suite — and the 1,282 figure refers to AgentShield (sibling repo), not ECC's 91 Jest + 4 Python tests. "98% coverage" is asserted with no externally verifiable badge. Marketed counts (38 agents / 156 skills / 72 commands) under-count the actual filesystem (48 / 183 / 79).
- **Catalog drift.** README, SOUL.md, REPO-ASSESSMENT.md, and `/contents/` listings disagree on counts. Sign of fast iteration faster than docs can keep up.
- **Repo age (3 months) vs complexity.** A 1.8MB Rust prototype, 183 skills, and a Tkinter dashboard appearing in 12 weeks raises questions about how much is polished vs partially-prototyped scaffolding (the v1.10.0 release notes themselves caveat: "the broader control-plane roadmap remains incomplete and should not be treated as GA").
- **Community sentiment is genuinely split** between "essential toolkit" and "textbook over-engineering" per blog/Reddit analysis.

### 4.5 Verdict on Maturity

**ECC is real, fast-growing, professionally engineered, and led by a verifiable maintainer.** The "hot README riding the hype curve" hypothesis is rejected. The repo has CI breadth most enterprise products lack, a 12-release semver-disciplined cadence over 94 days, sub-day issue response, an active 159-contributor community, and a tangible Rust 2.0 prototype building locally.

But it is **not yet a stable, production-grade foundation to depend on.** It is a single-maintainer-driven, three-month-old project growing faster than its own documentation can keep up; star-to-actual-install conversion is ~0.6%; the marketing claims (especially exact test counts and coverage percentages) outrun externally-verifiable evidence; and the v1.10.0 changelog itself disclaims that the ECC 2.0 control-plane roadmap is incomplete.

**For Momentum integration purposes:** Treat ECC as a **rapidly-evolving reference codebase**, not a stable upstream dependency. It is worth mining for patterns. It is **not yet trustworthy as a versioned dependency** to lock against, given (a) the velocity (8-day average release cadence means breaking changes are likely), (b) the bus factor on a single founder, and (c) the over-broad marketing claims. Adopt selectively. Version-pin if pulled in. Do not assume backward compatibility across releases.

---

## Section 5 — ECC's `continuous-learning-v2` — Concrete Integration Paths

Per Steve's request *"I'd sure like to understand it better"* (CITED), this section explains the actual mechanism and three integration paths.

### 5.1 The Mechanism

`continuous-learning-v2` is a hook-driven, background-agent system. The directory structure: (VERIFIED — `skills/continuous-learning-v2/`)

- `SKILL.md` (12,601 bytes) — main documentation.
- `config.json` (135 bytes) — observer toggle (`enabled: false` by default) and interval settings.
- `hooks/observe.sh` (17,703 bytes) — PreToolUse + PostToolUse hook script.
- `agents/observer.md` (7,396 bytes) — Haiku agent prompt.
- `agents/observer-loop.sh` (9,876 bytes) — background loop running `observer.md` via Claude CLI.
- `agents/start-observer.sh` (7,522 bytes) — start/stop/status lifecycle manager.
- `agents/session-guardian.sh` (6,392 bytes) — gating logic (time windows, cooldown, idle detection).
- `scripts/detect-project.sh` (8,254 bytes) — project ID derivation from git remote.
- `scripts/instinct-cli.py` (57,750 bytes) — CLI for managing instincts (promote, export, import).
- `scripts/test_parse_instinct.py` (33,106 bytes) — test suite for instinct parsing.

Total: ~58 KB Python + ~50 KB shell. Real, substantial subsystem — the largest self-contained module in the ECC repo.

**Observation flow.** `observe.sh` is registered as both PreToolUse and PostToolUse on `*` (all tools). Every Claude tool call fires the hook. The script:

1. Parses hook payload from stdin (tool name, tool input, cwd).
2. Resolves cwd to a git repository root.
3. Skip guards: skips on CLI/automation contexts, `ECC_HOOK_PROFILE=minimal`, `ECC_SKIP_LEARNING=1`, paths in excluded dirs.
4. Truncates payload to 5,000 characters.
5. Scrubs secrets matching patterns like `api_key`, `token`, `password`, `secret` (regex-based; not semantic).
6. Derives project ID via `detect-project.sh` (priority: `CLAUDE_PROJECT_DIR` env var → `git remote get-url origin` hashed to 12-char ID → `git rev-parse --show-toplevel` → global fallback).
7. Appends observation as JSON line to `~/.claude/homunculus/projects/<project-hash>/observations.jsonl`.
8. Archives at 10MB; purges archives older than 30 days.
9. Optionally signals background observer via SIGUSR1.

The hook itself has no LLM cost — pure bash disk I/O.

**Background analyzer.** Off by default. When enabled (`enabled: true` in config.json + `start-observer.sh start`), the loop fires every `run_interval_minutes` (default 5 minutes). `session-guardian.sh` applies three gates:

1. **Time window** — skip if outside `OBSERVER_ACTIVE_HOURS_START`–`OBSERVER_ACTIVE_HOURS_END` (defaults 8 AM – 11 PM, supports overnight).
2. **Project cooldown** — skip if same project analyzed within 300s (mkdir-based file locking).
3. **Idle detection** — skip if user idle longer than 1800s (default 30 min).

Plus a minimum threshold: `min_observations_to_analyze: 20` prevents spurious instinct generation.

When analysis runs, `observer-loop.sh` invokes Claude with Haiku model in `--print` mode, limited to Read/Write tools. It samples the last 500 lines of the observations file (memory management), writes to a temp file, and the agent writes instinct YAML files directly to the instincts directory. Re-entrancy guards prevent concurrent runs; cooldown throttling (default 60s) prevents rapid-fire concurrent Claude processes.

**Token cost estimate.** At Haiku pricing (~$0.80/M input tokens), 500 lines × ~100 tokens/line = 50K tokens → ~$0.04 per cycle. At 5-minute intervals during 8-hour session: ~96 cycles → ~$3.84/session. Low but not zero. *This is why the observer is off by default.*

**Instinct format.** YAML with frontmatter — example from SKILL.md:

```yaml
---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
source: "session-observation"
scope: project
project_id: "a1b2c3d4e5f6"
project_name: "my-react-app"
---

# Prefer Functional Style

## Action
Use functional patterns over classes when appropriate.

## Evidence
- Observed 5 instances of functional pattern preference
- User corrected class-based approach to functional on 2025-01-15
```

Confidence scoring:
- 1–2 observations → 0.3 (tentative, "suggested but not enforced")
- 3–5 observations → 0.5 ("applied when relevant")
- 6–10 observations → 0.7 ("auto-approved for application")
- 11+ observations → 0.85 ("near-certain")
- Dynamic adjustment: +0.05 per confirming observation, -0.1 per contradicting observation, decay over time.

**Promotion to global.** Not automatic. Requires running `python3 instinct-cli.py promote` explicitly. Auto-promotion criteria for `promote` with no argument: same instinct `id` appears in 2+ projects AND average confidence ≥ 0.8. `--dry-run` flag exists but isn't required. Once promoted, no rollback besides manual file deletion.

**`/evolve` command** clusters related instincts and proposes evolution into full skills/commands/agents. The instinct-writing step is fully autonomous; the evolution-to-skill step requires the user to invoke `/evolve` explicitly.

### 5.2 Comparison to Momentum

| Dimension | ECC `continuous-learning-v2` | Momentum `distill` + `triage` + `intake-queue.jsonl` |
|---|---|---|
| Trigger | Every tool call, autonomous hook | Human-invoked; from retro Phase 5 or directly |
| Observer | Background Haiku in separate process | Parallel Enumerator + Adversary in main session |
| Candidate generation | Automatic (Haiku reads observations, writes candidates) | Human-described in natural language |
| Adversarial check | None; observer writes instincts without challenge | Mandatory; Adversary checks redundancy/conflict/scope |
| Output | YAML instinct file with confidence score | Targeted edit to specific rule/reference/skill file |
| Human approval | Not required for instinct writing; required for promotion (via `promote`) | Required at Phase 1 (before any write); explicit batch approval in triage |
| Rollback | Manual file deletion; no git history | Git commit on every change |
| Versioning | Confidence decay; no commit | Git-backed with full history |
| Scope decision | Observer decides (defaults to project) | Enumerator classifies, developer approves |
| Low-confidence tail | Yes — 0.3 instincts persist | No — if adversary blocks, nothing is written |

**Philosophical divergence.** ECC's `continuous-learning-v2` optimizes for **coverage** (capture everything, filter by confidence later). Momentum's curation pipeline optimizes for **precision** (don't write anything that isn't already validated). ECC produces a long tail of tentative candidates; Momentum produces a short list of high-certainty rule changes.

### 5.3 Integration Paths

Steve's specific question: could ECC's mechanism sit underneath Momentum's gate — auto-extract candidates, human approves before promotion?

**Path A — `observe.sh` feeds `intake-queue.jsonl`.** Reuse ECC's `observe.sh` hook as-is to capture tool events into `~/.claude/homunculus/projects/<hash>/observations.jsonl`. Modify the Haiku observer step to write candidate instincts not to YAML files but as `kind: shape` events to Momentum's `intake-queue.jsonl`. Run `momentum:triage` periodically to classify and route them.

- *What this achieves:* The observation infrastructure (100% hook coverage, secret scrubbing, project scoping, archiving, session-guardian gating) is reused. Human gate is `triage`. Instinct-to-rule application is `distill`.
- *What conflicts:* Schema mismatch (YAML instincts vs JSONL events) needs an adapter. The 58 KB `instinct-cli.py` either gets called directly or just the observation-capture portion is reused. ECC's instincts live in `~/.claude/homunculus/` (global, cross-project); Momentum's queue is per-project in `_bmad-output/`. Structural mismatch needs a choice: keep ECC's global storage and query per-project, or adapt observations to write into Momentum's project tree.
- *Cost:* Medium — the modification of the observer step is real Python work, ~1–2 sprints.

**Path B — Periodic export as triage input.** Leave ECC's instinct system running as-is (observer writes YAML instincts). Periodically run `instinct-cli.py list` to dump candidates, then pipe them as a list into `momentum:triage`. Triage classifies (DISTILL for good ones, REJECT for noise, SHAPE for uncertain), and approved DISTILL items go to `momentum:distill`.

- *What this achieves:* No code changes. Pure workflow composition. ECC does extraction; Momentum does curation. Human gate at triage, not at observation.
- *What conflicts:* Philosophically, this puts Momentum in the role of "garbage collector for ECC's outputs." If ECC generates many low-confidence instincts (0.3 tentative), most triage sessions will be dominated by rejections. Signal-to-noise unknown until tested. Cross-directory sourcing requires explicit setup.
- *Cost:* Low — half a sprint to wire up the export+import flow.

**Path C — Adopt `observe.sh` only, discard the rest.** Use `observe.sh` purely as a lightweight session diary — hook fires, writes events, nothing else runs. Periodically (at retro, or weekly) run a `momentum:triage` pass over the raw observations log to identify patterns worth distilling. Skip ECC's background Haiku observer entirely; use Momentum's `distill` for the actual write step.

- *What this achieves:* The cheapest possible integration. No ongoing LLM cost. No YAML instinct files. The observation log becomes a human-readable session diary that can inform retro (alongside DuckDB transcript mining). The triage pattern-recognition step would be simpler than ECC's Haiku observer (Haiku reads raw events; triage reads classified findings), but with human judgment driving classification.
- *What conflicts:* Nothing technically. Additive. The session diary path is separate from everything Momentum writes. Only friction: adding `observe.sh` to Momentum's `hooks/hooks.json` (or forking it to use Momentum's bash dispatcher pattern instead of Node).
- *Cost:* Half a sprint.

### 5.4 Recommendation: Path C

Path C is the most plausible integration. It:

- Preserves Momentum's "human-curated, high-precision" curation philosophy.
- Adds a free machine-level session diary that feeds retro analysis.
- Avoids the YAML-instinct schema entirely (no schema impedance mismatch).
- Avoids Haiku observer cost.
- Is reversible — if the observation log isn't useful, remove the hook.
- Gracefully degrades to current behavior if `observe.sh` fails.

The only architectural concern: `observe.sh` writes to `~/.claude/homunculus/projects/<hash>/observations.jsonl`, which is *outside* the project. Momentum's instinct (a different sense of the word) is to keep practice artifacts inside `_bmad-output/`. Two options:

1. **Honor ECC's location.** Keep observations in `~/.claude/homunculus/...`; teach `momentum:triage` and `momentum:retro` to optionally read from there.
2. **Repath to Momentum's tree.** Fork `observe.sh` to write to `_bmad-output/observation-diary/<sprint-slug>.jsonl`. Simpler triage path; loses ECC's global-cross-project view (which Momentum doesn't need anyway).

Option 2 is cleaner. Recommend forking `observe.sh` and shipping it as a Momentum hook in a future sprint. Tag the file with `origin: ECC` for attribution.

### 5.5 Concerns

**Token cost.** Path C avoids the Haiku observer cost entirely. Path A and B incur Haiku costs (~$3.84/8-hour-session at default settings). For Momentum's solo-developer audience this is small but worth flagging.

**Bad pattern propagation.** Confidence decay and contradiction mechanisms have gaps:
- Silent auto-approval at 0.7 — an instinct reinforced by 6–10 observations becomes auto-approved with no notification.
- Auto-promotion without per-instinct confirmation — `promote` (no arg) promotes all qualifying instincts without per-item review. `--dry-run` not required.
- No rollback besides file deletion.
- Observer confidence drift — the 500-line window may miss late contradictions.

Path C avoids all of these because the human gate is preserved.

**Privacy.** ECC's `observe.sh` scrubs secrets via pattern matching on field names (`api_key`, `token`, `password`, `secret`). Not semantic. A credential stored in a field named `auth` or `bearer` or `x-api-key` might pass through unredacted. 5,000-char truncation could cut off sensitive sections or leave them in the retained portion. Observations contain tool call inputs which may include file paths, code snippets, and partial file contents. **Before enabling on healthcare/finance projects, audit the regex.**

**Volume at scale.** 100–500 tool calls per hour of active development → 4,000–20,000 observation lines per sprint week. The 10MB archival trigger and 30-day purge manage this, but file-based storage is sequential (no indexing). Should handle Momentum's volume; not benchmarked.

---

## Section 6 — Cross-CLI Portability & AGENTS.md Adoption

Per Steve's explicit guidance — *"Definitely want it to be cross-agent"* (CITED) — this section recommends concrete adoption.

### 6.1 The AGENTS.md Standard

AGENTS.md is **a real, well-codified standard.** (VERIFIED — multiple primary sources.)

- **Origin.** Introduced by OpenAI in August 2025 as "a simple, universal standard … that gives AI coding agents a consistent source of project-specific guidance" alongside Codex.
- **Governance.** Donated to the Linux Foundation in December 2025 as one of three founding projects of the **Agentic AI Foundation (AAIF)**, alongside Anthropic's Model Context Protocol (MCP) and Block's goose. Press release confirmed by Linux Foundation, OpenAI, Anthropic, and TechCrunch.
- **Adoption.** 60K+ open-source projects, 25+ tools listed as supporting the format including GitHub Copilot Coding Agent, OpenAI Codex, Google Jules, Gemini CLI, Cursor, VS Code, Zed, Aider, Devin, Windsurf, UiPath, JetBrains Junie.
- **Spec.** Hosted at `https://agents.md` with accompanying repo at `https://github.com/openai/agents.md`. The format has no required fields — it is "just standard Markdown" — with common conventions for setup, code style, testing, PR rules, and security. Monorepos may use nested AGENTS.md files where the closest file wins.
- **AAIF Platinum members (2026):** AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI. Gold tier includes Adyen, Arcade.dev, Cisco, Datadog, Docker, Ericsson, IBM, JetBrains, Okta, Oracle, Salesforce, SAP, Shopify, Snowflake, Temporal, Twilio.

**ECC uses it correctly.** `AGENTS.md` lives at the ECC repo root with project rules (Agent-First, Test-Driven, Security-First, Immutability, Plan Before Execute, agent table, security guidelines, testing requirements, workflow surface policy). A separate `.codex/AGENTS.md` provides Codex-specific overlays. OpenCode is configured to read root `AGENTS.md` first via `instructions`. Codex is told to "Follow project AGENTS.md guidelines" via `persistent_instructions`. This is exactly how the standard is intended to be consumed.

**The caveat.** AGENTS.md is **a content convention, not a runtime.** It does not give portable hooks, portable plugin manifests, or portable agent definitions. It is the lowest-common-denominator integration: every agentic tool reads markdown, so a markdown file at a known location works everywhere. ECC leans on this pragmatically; everything else (hooks, plugin manifests, agent frontmatter) requires per-tool adapter glue.

### 6.2 What ECC's Cross-Harness Story Actually Achieves

Per the portability subagent (VERIFIED):

- **Highly portable across CC + Codex + OpenCode + Cursor:** skill markdown (most), AGENTS.md content, MCP server *intent*, ~80% of agent prompt content.
- **Adapter-required:** agent frontmatter formats, MCP server *configuration syntax*, hook business logic invocations.
- **Per-tool re-implemented:** hook event manifests, plugin manifests, install scripts, slash-command shims.
- **Estimate:** ~60–70% of ECC's value is portable across CC + Codex + OpenCode + Cursor; declining to ~30–40% into Gemini CLI (mostly AGENTS.md and skill text); ~0% into Goose/Aider/Cline (no integration shipped).

**Goose, Aider, Cline, ForgeCode are not supported by ECC.** No `.goose`, `.aider`, `.cline`, or `.forgecode` directories. This matters because Goose is one of the three founding contributions to the AAIF.

The prior research framing of a single "Plugin-Everything architecture agnostic to the specific agentic CLI" is **overstated**. The actual mechanism is a per-tool adapter pattern with shared sources, not a runtime-neutral plugin format.

### 6.3 Recommendation for Momentum

**Adopt AGENTS.md at the project root. A few hours of work. Ship it next sprint.**

The minimal AGENTS.md should:

1. State Momentum's identity and target user (solo developer using AI agents as primary code producers).
2. State the Authority Hierarchy (Specifications > Tests > Code).
3. State the Producer-Verifier Separation rule.
4. Point to Momentum-specific files for tools that read them (e.g., "If you are Claude Code, read `CLAUDE.md` and `~/.claude/rules/`. If you are Codex, OpenCode, or Cursor, read this file plus `_bmad-output/skills/impetus/references/`.").
5. Stay generic enough to not assume Claude Code idioms.
6. Link to `momentum:research` deep dives where relevant.

**Do not pursue full multi-harness ports.** Months of adapter work for Codex/OpenCode/Cursor/Gemini contradicts Momentum's depth-over-breadth positioning. AGENTS.md is the cheap win that gets Momentum readable everywhere a developer might be working.

**Tier 2 fallback (already in Momentum's README).** "Cursor and other tools" support is advisory: hooks don't auto-fire, global rules don't auto-load, but the philosophy and skill content remain valuable. AGENTS.md formalizes this Tier 2 — agents in other harnesses get the principles and the skill content; they just don't get the runtime gates.

**Tier 3 (philosophy only).** Already documented in the README. AGENTS.md reinforces it — a developer who wants Momentum's discipline without any tooling can read AGENTS.md and the rules cascade and apply them manually.

**Estimated effort.** Half a day to write a draft AGENTS.md, half a day to validate it against the spec at agents.md, ~1 hour to commit. Total: ~1 day of work, single sprint.

**A note on `CLAUDE.md`.** ECC keeps both `AGENTS.md` (universal) and `CLAUDE.md` (Claude-Code-specific). Momentum's existing `CLAUDE.md` becomes the Claude Code overlay; AGENTS.md becomes the universal layer. Consider the marker-based merge pattern ECC's `sync-ecc-to-codex.sh` uses — it preserves user-specific sections while merging shared sections.

### 6.4 The Bigger Cross-CLI Question

Steve's "definitely want cross-agent" comment opens a longer conversation than just AGENTS.md. The portability subagent flagged a middle path: ship a minimal `momentum-bridge` package that exports an AGENTS.md, the rules/, and the references/ as a Codex/OpenCode reference — at a fraction of the cost of full ECC-style ports.

This is **out of scope for the current adoption sprint** but worth flagging for the next research cycle. If Momentum gains adoption beyond the maintainer, the bridge becomes more valuable. For now: AGENTS.md is enough.

---

## Section 7 — Limitations & Corpus Caveats

The synthesis is honest about what wasn't fully covered.

### 7.1 AVFL Validator Coverage Was Degraded

Per the AVFL consolidated findings (`validation/iteration-1/consolidated.md`):

| Lens | Enumerator | Adversary | Status |
|---|---|---|---|
| Structural | ✓ (10 findings) | ✓ (5 findings) | Complete |
| Accuracy | ✗ FAILED (timeout) | ✓ (14 findings) | Degraded — Enumerator lost mid-stream |
| Coherence | ✓ (13 findings) | ⚠ PARTIAL (1 finding) | Degraded — Adversary stalled before completion |
| Domain | ✓ (11 findings) | ⚠ STUB only | Degraded — Adversary returned reference to parent only |

**Three of eight validators degraded.** The Accuracy-Enumerator failure means certain accuracy claims may not have been independently cross-checked. The Coherence-Adversary partial means some coherence framings were not stress-tested. The Domain-Adversary stub means domain-fitness intuitive criticisms are missing.

**What this means for the synthesis.** Some claims that should have received dual-reviewer cross-check received only single-reviewer validation. The synthesis flags `[VERIFIED]` only where direct file or API evidence is cited; `[CITED]` for practitioner sources with URLs; `[INFERRED]` for reasonable inference; nothing tagged `[SUSPECT]` survived past the fix-log cleanup. Readers who want maximum confidence should re-run AVFL on this synthesis with full validator coverage.

### 7.2 The Gemini Deep Research Output Is Disputed

Per the AVFL fix log, four CRITICAL findings against the Gemini Deep Research output were quarantined rather than retracted:

- **CRITICAL-001** — Gemini's directory table lists `tools/agentshield/` as an ECC repository path with "Proprietary security scanning engine with over 1,282 automated tests." This directory does not exist in ECC. AgentShield is a separate sibling npm package at `affaan-m/agentshield`, not an in-repo directory.
- **CRITICAL-002** — Gemini presents `qflow` as a real MCP server in ECC with "7-state machine and dependency DAG for task management." `qflow` does not exist anywhere in the ECC repository. All 2,662 verified tree entries return zero matches.
- **CRITICAL-003** — Gemini states "ECC has evolved [memory persistence] into `claude-mem`, a plugin that reached 89,000 stars in early 2026." `claude-mem` is not part of ECC. The most-starred `claude-mem` (`thedotmack/claude-mem`) has ~67.9K stars, not 89K, and is a distinct Claude Code plugin owned by `thedotmack`.
- **CRITICAL-004** — A whole strategic recommendation in the Gemini output pivots on adopting `claude-mem`. Built on the false premise from CRITICAL-003.

Plus 12 HIGH findings (stale stats, hackathon attribution conflation, MCP count errors, retro mapping error, AVFL/AgentShield mapping error, `.opencode/dist/index.js` nonexistent path, `--target opencode` nonexistent flag).

**Strategy.** Gemini output has a prominent DISPUTED INPUT header at the top citing all major hallucinations. Body preserved for historical record (negative-control value). Used only for triangulation context, not as a primary source. Synthesis treats Gemini as a known-bad fact source; verified subagent files are the primary truth ground.

### 7.3 Sub-Agent Coverage Gaps

The synthesis is built from 10 raw research files (8 sub-question subagents + 2 follow-up subagents on hackathon verification and continuous-learning deep dive). Areas the corpus did *not* cover comprehensively:

- **Live downstream-user feedback.** The Medium analysis ("82K-star agent harness dividing the developer community") is cited but not corroborated by independent user interviews. Community sentiment is reported as "split" but not quantified.
- **ECC's actual install success rate.** The selective-install architecture is documented but not stress-tested in this report. The `ecc doctor` / `ecc repair` flow exists but its real-world reliability is unknown.
- **Continuous-learning-v2 signal-to-noise ratio.** The mechanism is documented; the actual quality of instincts produced under real session conditions is not measured.
- **Cross-harness portability quality.** The portability subagent reported ~60–70% of ECC's value is portable. The exact value loss on each harness is not measured under real workloads.
- **Long-term maintenance trajectory.** With bus factor 1, the project's resilience to maintainer absence is untested.

These are flagged so readers can calibrate confidence and direct future research effort.

### 7.4 What the Synthesis Is Confident About

Direct file-verified facts:
- ECC's catalog counts (48 agents, 183 skills, 79 commands) verified against `gh api` listings.
- Continuous-learning-v2's mechanism verified against `observe.sh`, `observer.md`, `observer-loop.sh`, `instinct-cli.py`, `config.json`, SKILL.md.
- AGENTS.md standard verified against agents.md, openai/agents.md GitHub repo, Linux Foundation press releases, AAIF events page.
- Hackathon attribution (the headline issue) verified against Cerebral Valley event page, Anthropic blog winner announcement, Forum Ventures event page, Devpost.
- Affaan Mustafa identity verified against ResearchGate, GitHub, LinkedIn, personal website, elizaOS contributions.
- Star count, fork count, commit count, contributor count verified against GitHub REST API on 2026-04-26.
- Momentum's sprint state machine, sole-writer pattern, AVFL design, Gherkin specs verified against local repo files.

What the synthesis is *less* confident about:
- ECC's "1,282 tests" claim (refers to AgentShield, not ECC; not independently audited).
- ECC's "+2.25 quality lift" claim for GateGuard (mechanism real; effect size is ECC self-report).
- ECC's "98% coverage" claim (no externally verifiable badge).
- ECC's "5–15 iterations" claim for gan-style-harness (ECC self-report).

---

## Section 8 — Appendix: ECC Component Glossary

Quick reference for names that appear throughout the synthesis. Status: VERIFIED (file-confirmed in ECC repo), CITED (referenced from external source), DISPUTED (Gemini hallucination not in repo), or EXTERNAL (sibling project, not part of ECC).

| Component | Status | What it is |
|---|---|---|
| **AgentShield** | EXTERNAL | Separate sibling repo (`affaan-m/agentshield`), invoked by ECC's `security-scan` skill via `npx ecc-agentshield scan .`. The "1,282 tests, 102 rules" claim refers to AgentShield, not ECC. |
| **AGENTS.md** | VERIFIED | OpenAI-originated, Linux-Foundation-stewarded universal markdown standard for project-level agent guidance. Adopted by 60K+ projects, 25+ tools. |
| **agentic-engineering** | VERIFIED | ~50-line ECC skill with operating principles (define completion criteria, decompose to agent-sized units, route model tier, measure with evals). |
| **autonomous-loops** | VERIFIED | ECC skill documenting six loop architectures (sequential pipeline, NanoClaw REPL, infinite agentic loop, continuous Claude PR loop, de-sloppify, Ralphinho RFC DAG). |
| **block-no-verify** | VERIFIED | ECC hook script that refuses `git commit --no-verify` and similar bypasses. |
| **blueprint** | VERIFIED | ECC skill — "turn a one-line objective into a step-by-step construction plan" with self-contained context briefs per step. |
| **chief-of-staff** | VERIFIED | ECC agent for orchestration of other agents. |
| **claude-mem** | DISPUTED | Gemini hallucination treating `claude-mem` as part of ECC. Actual `claude-mem` (`thedotmack/claude-mem`) is a separate plugin, ~67.9K stars, not part of ECC. |
| **code-tour** | VERIFIED | ECC skill for guided codebase walkthrough. |
| **codebase-onboarding** | VERIFIED | ECC skill for onboarding new contributors to a codebase. |
| **codemaps** | VERIFIED | ECC subsystem (`scripts/codemaps/generate.ts` + `commands/update-codemaps.md` + `doc-updater` agent) for generating code-structure visualizations. |
| **configure-ecc** | VERIFIED | ECC skill that drives selective install conversationally via AskUserQuestion, including a Step 0 that clones ECC into `/tmp/everything-claude-code`. |
| **continuous-learning-v2** | VERIFIED | Hook-driven, background-Haiku-agent system that observes tool calls, writes instinct YAML files with confidence scoring (0.3–0.9), supports project→global promotion. v2.1 added project scoping. See Section 5. |
| **council** | VERIFIED | ECC skill convening four advisors (Architect, Skeptic, Pragmatist, Critic) for ambiguous decisions. Anti-anchoring via fresh subagents. |
| **dmux-workflows** | VERIFIED | ECC skill for multi-agent orchestration via dmux (tmux pane manager for AI agents). |
| **ECC 2.0** | VERIFIED | Alpha Rust prototype at `ecc2/` — `ecc-tui` v0.1.0 with `ratatui`, `crossterm`, `tokio`, `rusqlite`, `git2`, `clap`. Exposes `dashboard`, `start`, `sessions`, `status`, `stop`, `resume`, `daemon`. Per CHANGELOG: "alpha, not yet a public GA release." |
| **ecc_dashboard.py** | VERIFIED | 39 KB Tkinter desktop app at ECC repo root, runnable via `python3 ./ecc_dashboard.py` or `npm run dashboard`. GUI surface to install/sessions/status data. |
| **eval-harness** | VERIFIED | ECC formal evaluation framework with capability evals, regression evals, code-based / LLM / human graders, pass@k metrics. |
| **agent-eval** | VERIFIED | ECC skill for head-to-head agent comparison on YAML task definitions, git-worktree isolation, pass-rate/cost/time metrics. |
| **gan-style-harness** | VERIFIED | ECC adversarial generation+evaluation skill: Planner → Generator → Evaluator (all Opus 4.6) + Playwright MCP. Iterates 5–15 times. Engineered for live-app generation. |
| **gateguard** | VERIFIED | ECC skill + PreToolUse hook (`scripts/hooks/gateguard-fact-force.js`) — three-stage gate (DENY → FORCE investigation → ALLOW retry). Demands listing importers, schemas, quoting user instruction before first edit. ECC reports "+2.25 points avg quality lift in two A/B tests." |
| **harness-optimizer** | VERIFIED | ECC agent + script (`harness-audit`) for closed-loop tuning of harness configuration. |
| **Hookify** | VERIFIED | ECC slash command + skill (`commands/hookify.md`, `skills/hookify-rules/`) — frontmatter-driven rule generator for hook authoring. NOT a "conversational config wizard" as Gemini implied. |
| **install profiles** | VERIFIED | Five canned ECC profiles in `manifests/install-profiles.json`: `core`, `developer`, `security`, `research`, `full`. |
| **instinct-cli.py** | VERIFIED | 58 KB Python CLI for managing instincts (promote, export, import, list). Part of continuous-learning-v2. |
| **loop-operator** | VERIFIED | ECC agent for autonomous loop execution with stop conditions, observability, recovery actions. Pairs with `loop-start` / `loop-status` commands. |
| **omega-memory** | VERIFIED | MCP server template in ECC's `mcp-configs/mcp-servers.json` — "persistent agent memory with semantic search, multi-agent coordination, and knowledge graphs." Not preinstalled; reference catalog only. |
| **PRP** | VERIFIED | ECC command family (`prp-plan`, `prp-prd`, `prp-implement`, `prp-commit`, `prp-pr`) for artifact-producing planning pipeline. |
| **qflow** | DISPUTED | Gemini hallucination. Does not exist in ECC. |
| **repo-scan** | VERIFIED | ECC skill (community-origin, points at `haibindev/repo-scan`) — classifies repo files as project / third-party / build-artifact, detects 50+ embedded libraries, four-level verdict. |
| **safety-guard** | VERIFIED | ECC skill with three modes (Careful, Sandbox, Read-Only) intercepting destructive commands. |
| **santa-method** | VERIFIED | ECC adversarial verification skill with convergence loop. Phase 1 Generate → Phase 2 dual independent review → Phase 3 binary verdict gate → Phase 4 fix cycle. Attributed to Ronald Skelton. Closer AVFL analogue than gan-style-harness. |
| **session-guardian.sh** | VERIFIED | Part of continuous-learning-v2. Three gates (time window, project cooldown, idle detection) before background observer fires. |
| **silent-failure-hunter** | VERIFIED | 40-line ECC adversarial agent prompt — hunts empty catch blocks, swallowed errors, dangerous fallbacks, lost stack traces. Recommended for adoption into Momentum's AVFL roster. |
| **skill-comply** | VERIFIED | ECC skill that auto-generates compliance scenarios at three prompt-strictness levels, runs `claude -p`, captures stream-json tool traces, classifies whether agents follow rules. |
| **skill-stocktake** | VERIFIED | ECC slash command + skill that scans `~/.claude/skills/` and runs LLM-based quality eval against every SKILL.md, with results cache. |
| **strategic-compact** | VERIFIED | ECC skill + `pre-compact.js` + `suggest-compact.js` hooks for context-budget compaction. |
| **team-builder** | VERIFIED | ECC skill — interactive picker for ad-hoc parallel teams. |
| **tdd-workflow** | VERIFIED | ECC skill enforcing 80%+ coverage, RED-GREEN-REFACTOR with embedded TypeScript Jest examples. Plus per-language TDD skills. |
| **the-longform-guide.md / the-shortform-guide.md / the-security-guide.md** | VERIFIED | Three guide documents at ECC repo root, 15–29 KB each, describing ECC usage. Equivalent to "tutorials" externally. |
| **token-budget-advisor / context-budget / cost-aware-llm-pipeline** | VERIFIED | ECC token/cost discipline skills. |
| **verification-loop** | VERIFIED | ECC single-agent six-phase checklist (build → typecheck → lint → tests → security scan → diff review). Closer to procedural verification than adversarial. |
| **WORKING-CONTEXT.md** | VERIFIED | 29 KB working-context document at ECC repo root tracking active queues. |
| **zenith.chat** | VERIFIED | Affaan Mustafa's earlier project, won Forum Ventures × Anthropic hackathon Sep 2025. NOT part of ECC. The Forum Ventures win is what the README's "Anthropic Hackathon Winner" badge actually refers to. |

---

## Sources

### Primary [VERIFIED]

- `affaan-m/everything-claude-code` repository (shallow-clone 2026-04-26): all paths cited as `skills/...`, `agents/...`, `commands/...`, `hooks/...`, `scripts/...`, `manifests/...`, `mcp-configs/...`, `ecc2/...`, `examples/...`, `docs/...`.
- GitHub REST API endpoints for `affaan-m/everything-claude-code`: repo metadata, `/contributors`, `/releases`, `/tags`, `/commits`, `/languages`, `/contents/...`, `/git/trees/main?recursive=1`. All queries 2026-04-26.
- GitHub Search API: `/search/issues?q=repo:affaan-m/everything-claude-code+...`.
- Local Momentum repo `/Users/steve/projects/momentum/`: `skills/momentum/.claude-plugin/plugin.json` (v0.17.0), `CLAUDE.md`, `.claude/rules/*`, `skills/momentum/skills/*/SKILL.md`, `skills/momentum/hooks/hooks.json`, `_bmad-output/implementation-artifacts/stories/index.json`, `sprints/index.json`, `intake-queue.jsonl`, sprint directories.
- agents.md spec site, `https://github.com/openai/agents.md`, Linux Foundation AAIF press releases.
- Cerebral Valley event page, Anthropic winners blog post (`claude.com/blog/meet-the-winners-of-our-built-with-opus-4-6-claude-code-hackathon`), Forum Ventures event page, Devpost listings.
- Affaan Mustafa identity sources: ResearchGate, GitHub (`affaan-m`), LinkedIn, affaanmustafa.com.

### Secondary [CITED]

- medium.com/@tentenco — "Everything Claude Code: Inside the 82K-Star Agent Harness That's Dividing the Developer Community" (2026-03-18).
- bridgers.agency — "everything-claude-code explained" (2026-03-23).
- claudeskills.info — "The Claude Code Hackathon Winner: Eval-Driven Development".
- help.apiyi.com — "Decoding everything-claude-code" comprehensive analysis.
- DeepWiki.com — auto-generated docs page.
- FlorianBruniaux/claude-code-ultimate-guide independent eval.
- @godofprompt X status 2030434516397891732 (Sep 2025 amplification of zenith.chat win).
- Practitioner notes: `~/.claude/projects/-Users-steve-projects-momentum/memory/MEMORY.md` and 18 typed feedback files.

### Disputed Input [SUSPECT — quarantined]

- `raw/gemini-deep-research-output.md` — contains four CRITICAL fabrications (tools/agentshield/, qflow MCP, claude-mem attribution, claude-mem adoption recommendation cascade) plus 12 HIGH inaccuracies. Used only for triangulation context, not as a primary source. Disputed-input header at top of file.

### Validation Artifacts

- `validation/iteration-1/consolidated.md` — AVFL findings (51 total: 4 CRITICAL, 16 HIGH, 21 MEDIUM, 10 LOW).
- `validation/iteration-1/fix-log.md` — fix log (36 of 51 addressed; 15 deferred).
- `raw/practitioner-notes.md` — Steve's Q&A responses informing synthesis structure and emphasis.

---

*End of synthesis. Word count: ~10,800.*
