---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "Architecture & capabilities — what does affaan-m/everything-claude-code actually ship at the code level"
topic: "everything-claude-code vs Momentum — comparative analysis"
---

# Architecture & Capabilities of `affaan-m/everything-claude-code`

This document enumerates, with verified counts, what the `affaan-m/everything-claude-code` (hereafter "ECC") repository actually ships at the code level. Every numeric claim was verified directly against the GitHub REST API and the recursive git tree of the `main` branch as of 2026-04-26. Where ECC's own README, CHANGELOG, or plugin manifests disagree with the live repo state, both numbers are reported and the discrepancy is flagged.

## Verification of Suspect Numeric Claims

A separate Gemini Deep Research report on this same topic surfaced a list of figures that were treated as suspect and required independent verification. Results:

| Gemini claim                                              | Verified value                                                       | Status                       |
| --------------------------------------------------------- | -------------------------------------------------------------------- | ---------------------------- |
| 140,000+ stars                                            | **167,488 stars**                                                    | DISPUTED (actual is higher)  |
| 21,000+ forks                                             | **25,969 forks**                                                     | DISPUTED (actual is higher)  |
| 113 contributors                                          | **159 contributors**                                                 | DISPUTED (actual is higher)  |
| 768 commits                                               | **~1,465 commits on main** (Link header `page=1465` at per_page=1)   | DISPUTED (actual ~2x higher) |
| 1,282 automated tests                                     | **102 test-like files / 91 `*.test.js` files indexed by GitHub**     | DISPUTED (no evidence for 1,282) |
| 48 agents                                                 | **48 `agents/*.md` files**                                           | VERIFIED                     |
| 183 skills                                                | **183 skill directories under `skills/`**                            | VERIFIED                     |
| 14 MCP integrations                                       | **6 in root `.mcp.json`; ~24 in `mcp-configs/mcp-servers.json`**     | DISPUTED (depends on file)   |
| 12 supported language ecosystems                          | **README claim; ~12 language-named `rules/` subdirs**                | PARTIAL (matches README marketing) |
| Anthropic x Forum Ventures hackathon win in late 2025     | **Repo created 2026-01-18; README says "Anthropic Hackathon Winner"** | UNVERIFIED (no primary source for "Forum Ventures" or "late 2025") |

Source for all GitHub-side numbers: GitHub REST API queries (`gh api repos/affaan-m/everything-claude-code/...`) executed 2026-04-26 ([GitHub API](https://api.github.com/repos/affaan-m/everything-claude-code)) **[OFFICIAL]**.

## Repo Overview

- **Full name:** `affaan-m/everything-claude-code`
- **Description (GitHub):** "The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond." ([GitHub repo metadata](https://api.github.com/repos/affaan-m/everything-claude-code)) **[OFFICIAL]**
- **License:** MIT
- **Homepage:** `https://ecc.tools`
- **Default branch:** `main`
- **Created:** 2026-01-18 ([repo metadata](https://api.github.com/repos/affaan-m/everything-claude-code)) **[OFFICIAL]**
- **Last push:** 2026-04-26 (same day as this research) **[OFFICIAL]**
- **Repo size:** ~31 MB (`size: 31138` KB)
- **Stars / forks / watchers / issues:** 167,488 / 25,969 / 864 / 166 open issues **[OFFICIAL]**
- **Topics:** `ai-agents`, `anthropic`, `claude`, `claude-code`, `developer-tools`, `llm`, `mcp`, `productivity`
- **Current published version:** `1.10.0` (in `VERSION`, `package.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, and `agent.yaml`) **[OFFICIAL]**
- **Latest release:** `v1.10.0`, published 2026-04-05, titled "ECC v1.10.0 — Surface Refresh, Operator Workflows, and ECC 2.0 Alpha" ([GitHub releases](https://github.com/affaan-m/everything-claude-code/releases)) **[OFFICIAL]**
- **Total releases / tags:** 12 GitHub releases, 13 tags (v0.6.0 through v1.10.0) **[OFFICIAL]**

The README brands the project as "The performance optimization system for AI agent harnesses. From an Anthropic hackathon winner." and claims it works across "Claude Code, Codex, Cursor, OpenCode, Gemini, and other AI agent harnesses." ([README.md](https://github.com/affaan-m/everything-claude-code/blob/main/README.md)) **[OFFICIAL]**.

The README also asserts a banner of "**140K+ stars** | **21K+ forks** | **170+ contributors** | **12+ language ecosystems** | **Anthropic Hackathon Winner**". The GitHub-API-verified live numbers (167K/26K/159) are higher than the README on stars and forks but lower on contributors. The README is not synced to live repo state.

## Directory Layout (Top Level)

The repository root contains a deliberately wide set of vendor-prefix directories (one per agent harness it claims to support) plus a flat set of canonical resource folders.

Verified via `gh api repos/affaan-m/everything-claude-code/contents/`:

```
.agents/             # external agent surfaces
.claude/             # Claude Code surface (skills/, rules/, hooks/, commands/, team/, research/, ...)
.claude-plugin/      # plugin.json + marketplace.json (canonical Claude plugin manifest)
.codebuddy/          # CodeBuddy harness surface
.codex/              # Codex surface (agents/, AGENTS.md, config.toml)
.codex-plugin/       # Codex plugin manifest
.cursor/             # Cursor surface (hooks.json, hooks/, rules/, skills/)
.gemini/             # Gemini surface (GEMINI.md only)
.kiro/               # Kiro surface
.opencode/           # OpenCode surface (commands/, prompts/, plugins/, tools/, instructions/)
.trae/               # Trae surface
agents/              # 48 canonical agent .md files
assets/              # images / hero / logos
commands/            # 79 slash-command .md files
contexts/            # context packs
docs/                # localized READMEs and detailed docs
ecc2/                # ECC 2.0 Rust prototype (Cargo.toml, src/)
examples/            # examples
hooks/               # canonical hooks.json + README.md (ONLY 2 files)
manifests/           # install profile manifests (3 .json files)
mcp-configs/         # 1 file: mcp-servers.json
plugins/             # README.md only (legacy directory)
research/            # research bundles
rules/               # 89 .md rules across 15 sub-directories
schemas/             # JSON schemas
scripts/             # 30 entries (Node.js + sub-dirs ci/, codemaps/, codex/, codex-git-hooks/, hooks/, lib/)
skills/              # 183 skill directories (each with at least SKILL.md)
src/                 # src/llm/ only (small)
tests/               # 16 entries (test files + ci/, docs/, hooks/, integration/, lib/, scripts/)
```

Plus root-level files: `AGENTS.md` (8 KB), `CLAUDE.md` (2.8 KB), `SOUL.md`, `RULES.md`, `WORKING-CONTEXT.md` (29 KB), `the-longform-guide.md`, `the-shortform-guide.md`, `the-security-guide.md` (28 KB), `ecc_dashboard.py` (39 KB Tkinter desktop app), `install.sh`, `install.ps1`, `agent.yaml` (gitagent manifest), `package.json`, `pyproject.toml`, `commitlint.config.js`, `eslint.config.js`, plus standard hygiene files (CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, CHANGELOG, EVALUATION, REPO-ASSESSMENT, TROUBLESHOOTING, COMMANDS-QUICK-REF, SPONSORS, SPONSORING) **[OFFICIAL]**.

The README is large: 68,693 bytes (~69 KB) of marketing, install instructions, and component listings. The Chinese translation `README.zh-CN.md` is 36 KB. There are localized READMEs under `docs/` for `pt-BR`, `zh-TW`, `ja-JP`, `ko-KR`, and `tr` ([README.md head](https://github.com/affaan-m/everything-claude-code/blob/main/README.md)) **[OFFICIAL]**.

### Recursive Tree Counts

From `gh api repos/.../git/trees/main?recursive=1` (2,662 tree entries, not truncated) **[OFFICIAL]**:

- Markdown files (`.md`): **1,437**
- JavaScript files (`.js`): **233**
- JSON files (`.json`): **53**
- Python files (`.py`): **42**
- YAML (`.yaml`): **31**
- Shell (`.sh`): **29**
- TypeScript (`.ts`): **17**
- Rust (`.rs`): **16**
- TOML (`.toml`): **7**
- `SKILL.md` files anywhere in tree: **459** (of which 183 are at `skills/<name>/SKILL.md`; the rest live under harness-prefix dirs like `.claude/skills/`, `.opencode/`, etc.)
- `agents/*.md`: **48**
- `commands/*.md`: **79**
- `rules/**/*.md`: **89**
- `scripts/hooks/*`: **40 files**
- Test-like files (containing "test" in path with `.js`/`.ts`/`.py` extension): **102**

## Programming Languages

Per the GitHub `/languages` endpoint (bytes by language) **[OFFICIAL]**:

| Language     | Bytes     | Share approx. |
| ------------ | --------- | ------------- |
| JavaScript   | 2,396,741 | 51%           |
| Rust         | 1,818,298 | 38%           |
| Python       | 234,967   | 5%            |
| Shell        | 162,725   | 3%            |
| TypeScript   | 57,674    | 1%            |
| PowerShell   | 1,547     | <1%           |

The Rust share comes almost entirely from the `ecc2/` "ECC 2.0 alpha" Rust control-plane prototype (Cargo.toml + Cargo.lock + src/), not from anything that hooks into Claude Code today. JavaScript is the dominant *active* language: it powers all hooks, install scripts, validation, and harness adapters. Python is concentrated in `ecc_dashboard.py` (a 39 KB Tkinter desktop dashboard) plus a small `tests/test_*.py` suite. There is no Java, Go, Kotlin, or Swift *source* in the repo despite the marketing claim of "12+ language ecosystems" — those languages appear only as **rules/** subdirectories and skill names targeting projects written *in* those languages.

## Plugin Manifest

The canonical Claude Code plugin manifest is `.claude-plugin/plugin.json` ([plugin.json](https://github.com/affaan-m/everything-claude-code/blob/main/.claude-plugin/plugin.json)) **[OFFICIAL]**:

```json
{
  "name": "everything-claude-code",
  "version": "1.10.0",
  "description": "Battle-tested Claude Code plugin for engineering teams — 38 agents, 156 skills, 72 legacy command shims, production-ready hooks, and selective install workflows evolved through continuous real-world use",
  "author": { "name": "Affaan Mustafa", "url": "https://x.com/affaanmustafa" },
  "homepage": "https://ecc.tools",
  "repository": "https://github.com/affaan-m/everything-claude-code",
  "license": "MIT",
  "skills": ["./skills/"],
  "commands": ["./commands/"]
}
```

The marketplace manifest at `.claude-plugin/marketplace.json` claims a single plugin entry, also versioned `1.10.0`, with description "The most comprehensive Claude Code plugin — 38 agents, 156 skills, 72 legacy command shims, selective install profiles, and production-ready hooks for TDD, security scanning, code review, and continuous learning" **[OFFICIAL]**.

**Notable mismatch:** the manifest description says "38 agents, 156 skills, 72 legacy command shims," yet the live repo ships 48 agent files, 183 skill directories, and 79 command files. The CHANGELOG for v1.10.0 explicitly says "Synced published counts to the live OSS surface: 38 agents, 156 skills, 72 commands" — but that sync was already stale on the day the report was written. Either the manifest under-counts deliberately (perhaps "38 agents" excludes some new ones from the canonical install) or simply lags drift.

For other harnesses ECC ships parallel manifests:

- `.codex-plugin/plugin.json` (Codex) — version 1.10.0, declares `skills: "./skills/"` and `mcpServers: "./.mcp.json"`, plus a Codex-specific `interface` block describing it as "156 battle-tested ECC skills plus MCP configs" **[OFFICIAL]**.
- `agent.yaml` — a gitagent spec (`spec_version: "0.1.0"`) listing ~135 skills and ~80 commands explicitly, with `model.preferred: claude-opus-4-6` and `fallback: [claude-sonnet-4-6]` **[OFFICIAL]**.
- `package.json` — npm package `ecc-universal@1.10.0`, exposes binaries `ecc` (`scripts/ecc.js`) and `ecc-install` (`scripts/install-apply.js`), declares `engines.node: >=18`, and has dependencies on `@iarna/toml`, `ajv`, `sql.js` **[OFFICIAL]**.

The `package.json` `test` script chains 7 validation scripts under `scripts/ci/` plus `tests/run-all.js`. The repo also publishes a sibling npm package `ecc-agentshield`, referenced by README badges (npm download counters). Coverage is configured at 80% line/function/branch thresholds via `c8`.

## Agents (48 verified)

`agents/` is a flat directory of 48 markdown agent definitions, each with YAML frontmatter (`name`, `description`, `tools`, `model`). Verified file list ([agents/](https://github.com/affaan-m/everything-claude-code/tree/main/agents)):

`a11y-architect`, `architect`, `build-error-resolver`, `chief-of-staff`, `code-architect`, `code-explorer`, `code-reviewer`, `code-simplifier`, `comment-analyzer`, `conversation-analyzer`, `cpp-build-resolver`, `cpp-reviewer`, `csharp-reviewer`, `dart-build-resolver`, `database-reviewer`, `doc-updater`, `docs-lookup`, `e2e-runner`, `flutter-reviewer`, `gan-evaluator`, `gan-generator`, `gan-planner`, `go-build-resolver`, `go-reviewer`, `harness-optimizer`, `healthcare-reviewer`, `java-build-resolver`, `java-reviewer`, `kotlin-build-resolver`, `kotlin-reviewer`, `loop-operator`, `opensource-forker`, `opensource-packager`, `opensource-sanitizer`, `performance-optimizer`, `planner`, `pr-test-analyzer`, `python-reviewer`, `pytorch-build-resolver`, `refactor-cleaner`, `rust-build-resolver`, `rust-reviewer`, `security-reviewer`, `seo-specialist`, `silent-failure-hunter`, `tdd-guide`, `type-design-analyzer`, `typescript-reviewer`.

The canonical agent shape, from `agents/code-reviewer.md` **[OFFICIAL]**:

```yaml
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code. MUST BE USED for all code changes.
tools: ["Read", "Grep", "Glob", "Bash"]
model: sonnet
---
```

The body is a long-form English prompt (sections like "Review Process", "Confidence-Based Filtering", "Review Checklist" with CRITICAL/HIGH/MEDIUM/LOW gradations and embedded code examples for SQL injection, XSS, etc.).

`agents/planner.md` declares `tools: ["Read", "Grep", "Glob"]` and `model: opus`, with a body covering Requirements Analysis → Architecture Review → Step Breakdown → Implementation Order, and a literal "Plan Format" markdown template the agent is supposed to produce.

The taxonomic shape: agents are clustered by language (`*-build-resolver`, `*-reviewer`), by lifecycle (`planner`, `architect`, `code-reviewer`, `tdd-guide`, `e2e-runner`, `refactor-cleaner`, `silent-failure-hunter`), by harness/operator concerns (`chief-of-staff`, `harness-optimizer`, `loop-operator`, `conversation-analyzer`), by domain (`healthcare-reviewer`, `database-reviewer`, `seo-specialist`), and by GAN-style synthesis (`gan-evaluator`, `gan-generator`, `gan-planner`).

## Skills (183 verified)

`skills/` contains 183 sub-directories. Each holds at minimum a `SKILL.md` (frontmatter: `name`, `description`, `origin: ECC`). Verified from listing.

The catalog is broad and overlaps several axes:

- **Language patterns:** `python-patterns`, `python-testing`, `golang-patterns`, `golang-testing`, `kotlin-patterns`, `kotlin-testing`, `kotlin-coroutines-flows`, `kotlin-exposed-patterns`, `kotlin-ktor-patterns`, `rust-patterns`, `rust-testing`, `cpp-coding-standards`, `cpp-testing`, `csharp-testing`, `java-coding-standards`, `jpa-patterns`, `dart-flutter-patterns`, `swift-actor-persistence`, `swift-concurrency-6-2`, `swift-protocol-di-testing`, `swiftui-patterns`, `perl-patterns`, `perl-testing`, `perl-security`, `dotnet-patterns`, `pytorch-patterns`.
- **Frameworks:** `springboot-patterns/security/tdd/verification`, `django-patterns/security/tdd/verification`, `laravel-patterns/security/tdd/verification`, `nestjs-patterns`, `nuxt4-patterns`, `nextjs-turbopack`, `compose-multiplatform-patterns`, `android-clean-architecture`.
- **Workflow / engineering practice:** `tdd-workflow`, `agentic-engineering`, `ai-first-engineering`, `ai-regression-testing`, `verification-loop`, `eval-harness`, `agent-eval`, `continuous-learning`, `continuous-learning-v2`, `code-tour`, `codebase-onboarding`, `coding-standards`, `architecture-decision-records`, `git-workflow`.
- **Operator / business:** `customer-billing-ops`, `finance-billing-ops`, `customs-trade-compliance`, `healthcare-cdss-patterns`, `healthcare-emr-patterns`, `healthcare-eval-harness`, `healthcare-phi-compliance`, `hipaa-compliance`, `production-scheduling`, `inventory-demand-planning`, `logistics-exception-management`, `returns-reverse-logistics`, `quality-nonconformance`, `energy-procurement`, `carrier-relationship-management`, `lead-intelligence`, `investor-materials`, `investor-outreach`, `email-ops`, `messages-ops`, `unified-notifications-ops`, `google-workspace-ops`, `project-flow-ops`.
- **Security:** `security-review`, `security-scan`, `security-bounty-hunter`, `defi-amm-security`, `llm-trading-agent-security`, `gateguard`, `safety-guard`, `evm-token-decimals`, `nodejs-keccak256`.
- **Infra / harness:** `agent-harness-construction`, `agent-introspection-debugging`, `autonomous-agent-harness`, `autonomous-loops`, `continuous-agent-loop`, `claude-devfleet`, `dmux-workflows`, `enterprise-agent-ops`, `team-builder`, `council`, `nanoclaw-repl`, `terminal-ops`, `workspace-surface-audit`, `repo-scan`, `mcp-server-patterns`, `claude-api`.
- **Content / media:** `manim-video`, `remotion-video-creation`, `video-editing`, `videodb`, `frontend-slides`, `liquid-glass-design`, `frontend-design`, `design-system`, `seo`, `article-writing`, `crosspost`, `brand-voice`, `content-engine`, `social-graph-ranker`.
- **Self-referential:** `everything-claude-code` (a skill describing ECC itself), `configure-ecc`, `ecc-tools-cost-audit`.

Sample skill (`skills/tdd-workflow/SKILL.md`) **[OFFICIAL]**:

```yaml
---
name: tdd-workflow
description: Use this skill when writing new features, fixing bugs, or refactoring code. Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests.
origin: ECC
---
```

Body includes a "Git Checkpoints" section that asserts that under-Git work must produce checkpoint commits per TDD stage, that compile-time RED is acceptable as proxy for runtime RED, and a "Step 1 / Step 2 / Step 3" RED-GREEN-REFACTOR template with embedded TypeScript Jest examples.

Sample `skills/agentic-engineering/SKILL.md` declares "Operating Principles" (define completion criteria, decompose to agent-sized units, route model tier, measure with evals), an "Eval-First Loop", a "15-minute unit rule", explicit Haiku/Sonnet/Opus routing recommendations, session-strategy guidance, and a "Cost Discipline" tracking schema (model, token estimate, retries, wall-clock, success/failure).

Skills come in two granularities: thin "principle" skills like `agentic-engineering` (~50 lines), and very thick playbook skills (`tdd-workflow`, `verification-loop`, `continuous-learning-v2`) with embedded code, gates, and step-counted procedures.

## Commands (79 verified)

`commands/*.md` holds 79 slash-command definitions ([commands/](https://github.com/affaan-m/everything-claude-code/tree/main/commands)) **[OFFICIAL]**. The set is dominated by language-coupled trios (`{language}-build`, `{language}-review`, `{language}-test`) — present for `cpp`, `flutter`, `go`, `kotlin`, `python` (review only), `rust`, plus `gradle-build`. Cross-cutting commands include `/tdd`, `/plan`, `/code-review`, `/build-fix`, `/e2e`, `/eval`, `/learn`, `/learn-eval`, `/skill-create`, `/skill-health`, `/checkpoint`, `/refactor-clean`, `/test-coverage`, `/quality-gate`, `/verify`, `/promote`, `/prune`, `/aside`, `/orchestrate`, `/multi-{plan,workflow,backend,frontend,execute}`, `/loop-start`, `/loop-status`, `/santa-loop`, `/santa-method`, `/projects`, `/sessions`, `/save-session`, `/resume-session`, `/setup-pm`, `/pm2`, `/jira`, `/devfleet`, `/instinct-{export,import,status}`, `/hookify` (+ help/list/configure), `/harness-audit`, `/model-route`, `/prompt-optimize`, `/prp-{plan,prd,implement,commit,pr}`, `/rules-distill`, `/update-codemaps`, `/update-docs`, `/agent-sort`, `/context-budget`, `/claw`, `/review-pr`, `/feature-dev`, `/evolve`, `/gan-{build,design}`.

The CLAUDE.md describes the "Key Commands" as `/tdd`, `/plan`, `/e2e`, `/code-review`, `/build-fix`, `/learn`, `/skill-create` ([CLAUDE.md](https://github.com/affaan-m/everything-claude-code/blob/main/CLAUDE.md)) **[OFFICIAL]**. Most of the other 70+ commands are best understood as legacy or harness-specific shims, which the manifest description openly calls "72 legacy command shims."

## Hooks

Two surfaces exist for hooks. Both must be considered together:

1. **`hooks/`** — only contains `hooks.json` (~5 KB) and a README.md. The hooks.json file is the canonical Claude Code hooks settings, with `PreToolUse`, `PostToolUse`, `Stop`, `PreCompact`, and `SessionStart` matchers ([hooks/hooks.json](https://github.com/affaan-m/everything-claude-code/blob/main/hooks/hooks.json)) **[OFFICIAL]**. Each hook entry is a `node -e "..."` bootstrap that resolves `CLAUDE_PLUGIN_ROOT` (probing `.claude/plugins/<name>`, marketplace cache, etc.), then `require()`s `scripts/hooks/plugin-hook-bootstrap.js`, which delegates to a specific hook script under `scripts/hooks/`.

2. **`scripts/hooks/`** — 40 hook implementation files. Verified list:

   - **Pre-bash dispatchers / gates:** `pre-bash-dispatcher.js`, `pre-bash-commit-quality.js`, `pre-bash-dev-server-block.js`, `pre-bash-git-push-reminder.js`, `pre-bash-tmux-reminder.js`, `block-no-verify.js`, `gateguard-fact-force.js`.
   - **Post-bash:** `post-bash-dispatcher.js`, `post-bash-build-complete.js`, `post-bash-command-log.js`, `post-bash-pr-created.js`, `bash-hook-dispatcher.js`.
   - **Edit/Write:** `pre-write-doc-warn.js`, `doc-file-warning.js`, `post-edit-accumulator.js`, `post-edit-console-warn.js`, `post-edit-format.js`, `post-edit-typecheck.js`, `check-console-log.js`, `design-quality-check.js`.
   - **Session lifecycle:** `session-start.js`, `session-start-bootstrap.js`, `session-end.js`, `session-end-marker.js`, `session-activity-tracker.js`, `pre-compact.js`, `suggest-compact.js`, `stop-format-typecheck.js`, `evaluate-session.js`.
   - **Cross-cutting:** `auto-tmux-dev.js`, `check-hook-enabled.js`, `config-protection.js`, `cost-tracker.js`, `desktop-notify.js`, `mcp-health-check.js`, `quality-gate.js`, `governance-capture.js`, `run-with-flags.js`, `run-with-flags-shell.sh`, `plugin-hook-bootstrap.js`.

The hooks.json bootstrap pattern is unusually defensive: it inlines a ~30-line `node -e` JavaScript expression that probes six possible plugin install paths plus a `cache/<name>/<version>` glob before settling on a CLAUDE_PLUGIN_ROOT. This strongly implies the team has been bitten by Claude plugin path resolution drift in the wild **[OFFICIAL]**.

## MCP Configurations

ECC ships **two** MCP server config files, with very different shapes:

1. **Root `.mcp.json`** — 6 servers, pinned versions, intended to be the "default" project-level MCP configuration ([.mcp.json](https://github.com/affaan-m/everything-claude-code/blob/main/.mcp.json)) **[OFFICIAL]**:
   - `github` (`@modelcontextprotocol/server-github@2025.4.8`)
   - `context7` (`@upstash/context7-mcp@2.1.4`)
   - `exa` (HTTP, `https://mcp.exa.ai/mcp`)
   - `memory` (`@modelcontextprotocol/server-memory@2026.1.26`)
   - `playwright` (`@playwright/mcp@0.0.69 --extension`)
   - `sequential-thinking` (`@modelcontextprotocol/server-sequential-thinking@2025.12.18`)

2. **`mcp-configs/mcp-servers.json`** — a "kitchen-sink" reference catalog (truncated at ~5 KB read) listing **at least 24** MCP integrations as templates with `YOUR_*_HERE` placeholders for credentials. Verified entries include: `jira` (mcp-atlassian), `github`, `firecrawl`, `supabase`, `memory`, `omega-memory`, `sequential-thinking`, `vercel`, `railway`, `cloudflare-docs`, `cloudflare-workers-builds`, `cloudflare-workers-bindings`, `cloudflare-observability`, `clickhouse`, `exa-web-search`, `context7`, `magic` (Magic UI), `filesystem`, `playwright`, `fal-ai`, `browserbase`, `browser-use`, `devfleet` (local), `token-optimizer`, … (continued past read limit) **[OFFICIAL]**.

So the "14 MCP integrations" Gemini number is wrong in both directions: the *actually-shipped* `.mcp.json` is 6 servers, but the reference catalog at `mcp-configs/mcp-servers.json` is much larger than 14 (24+).

## Scripts

`scripts/` contains 30 entries — a Node-heavy ops layer ([scripts/](https://github.com/affaan-m/everything-claude-code/tree/main/scripts)) **[OFFICIAL]**:

- **Install/uninstall pipeline:** `install-plan.js`, `install-apply.js`, `uninstall.js`, `setup-package-manager.js`, `repair.js`, `list-installed.js`, `doctor.js` (a "diagnose your install" CLI).
- **CLI entry points:** `ecc.js` (the `ecc` binary published as `npx ecc <lang>`), `claw.js` (the `npm run claw` orchestrator).
- **Catalog & health:** `catalog.js`, `harness-audit.js`, `skills-health.js`, `skill-create-output.js`, `status.js`, `session-inspect.js`, `sessions-cli.js`.
- **Cross-harness adapters:** `gemini-adapt-agents.js`, `build-opencode.js`, `sync-ecc-to-codex.sh`.
- **Orchestration (multi-worktree):** `orchestrate-codex-worker.sh`, `orchestrate-worktrees.js`, `orchestration-status.js`.
- **GAN harness (research / experimental):** `gan-harness.sh`.
- **Release plumbing:** `release.sh`.
- **Subdirectories:** `ci/` (validation: `validate-agents.js`, `validate-commands.js`, `validate-rules.js`, `validate-skills.js`, `validate-hooks.js`, `validate-install-manifests.js`, `validate-no-personal-paths.js`, `check-unicode-safety.js`, `catalog.js`), `codemaps/`, `codex/` (4 files: `check-codex-global-state.sh`, `install-global-git-hooks.sh`, `merge-codex-config.js`, `merge-mcp-config.js`), `codex-git-hooks/`, `hooks/` (the 40-file dispatcher/handler set above), `lib/` (shared utilities — `utils.js` is the file the hooks.json bootstrap probes to identify CLAUDE_PLUGIN_ROOT).

## Cross-Harness Surfaces

ECC's headline pitch is "works across Claude Code, Codex, Cursor, OpenCode, Gemini, and other AI agent harnesses." Verified state on disk:

| Harness directory  | What's actually in it                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------- |
| `.claude/`         | Real surface: `commands/`, `enterprise/`, `homunculus/`, `research/`, `rules/`, `skills/`, `team/`, plus `ecc-tools.json`, `identity.json`, `package-manager.json`. **[OFFICIAL]** |
| `.codex/`          | `agents/` (3 TOML files: `docs-researcher.toml`, `explorer.toml`, `reviewer.toml`), `AGENTS.md`, `config.toml`. Real but small. |
| `.cursor/`         | `hooks.json`, `hooks/`, `rules/`, `skills/`. Real surface.                                  |
| `.opencode/`       | `commands/` (34 .md files), `prompts/`, `plugins/` (TypeScript: `index.ts`, `ecc-hooks.ts`, `lib/`), `tools/`, `instructions/`, `index.ts`, `opencode.json`, `package.json`, `tsconfig.json`. Real, sizable. |
| `.gemini/`         | One file: `GEMINI.md`. Token surface only.                                                  |
| `.codebuddy/`, `.kiro/`, `.trae/`, `.agents/` | Present at root but not deeply inspected; sized as zero-byte index entries by the contents endpoint. |

`.opencode/` is the second-most-developed harness surface after `.claude/` (TypeScript plugins, 34 commands, build via `scripts/build-opencode.js`). Codex is supported via parallel manifest (`.codex-plugin/plugin.json`), parallel npm package idea (`ecc` Codex name), and config-merge scripts (`scripts/codex/merge-codex-config.js`, `merge-mcp-config.js`). Gemini support is essentially a single instructions file plus an adapter script (`scripts/gemini-adapt-agents.js`).

## Rules and Other Resources

- **`rules/`** — 89 markdown files spread across 15 sub-directories: `common/`, `cpp/`, `csharp/`, `dart/`, `golang/`, `java/`, `kotlin/`, `perl/`, `php/`, `python/`, `rust/`, `swift/`, `typescript/`, `web/`, `zh/` (a Chinese-language rules variant) **[OFFICIAL]**. This is what backs the "12+ language ecosystems" marketing claim — there are 13 language buckets here (excluding `common/` and `zh/`), so "12+" rounds down generously.
- **`manifests/`** — 3 install profile manifests: `install-components.json`, `install-modules.json`, `install-profiles.json`. These drive the "selective install" flow announced in v1.9.0.
- **`schemas/`** — JSON schemas for validation (used by the `tests/` validators).
- **`tests/`** — 16 top-level entries: 5 JS test files (`codex-config.test.js`, `opencode-config.test.js`, `plugin-manifest.test.js`, `run-all.js` orchestrator) plus Python test files (`test_builder.py`, `test_executor.py`, `test_resolver.py`, `test_types.py`, `conftest.py`, `__init__.py`) and sub-dirs `ci/`, `docs/`, `hooks/`, `integration/`, `lib/`, `scripts/`. **There is no evidence of "1,282 automated tests"**: GitHub code search returns 91 `*.test.js` files; the recursive tree returns 102 test-named files total.
- **`ecc2/`** — a Rust prototype labeled "ECC 2.0 alpha". Contains `Cargo.toml`, `Cargo.lock`, `README.md`, `src/`. Per CHANGELOG v1.10.0: "ECC 2.0 alpha is in-tree — the Rust control-plane prototype in `ecc2/` now builds locally and exposes `dashboard`, `start`, `sessions`, `status`, `stop`, `resume`, and `daemon` commands. It is usable as an alpha, not yet a general release." **[OFFICIAL]**
- **`ecc_dashboard.py`** — a 39 KB single-file Tkinter desktop application, runnable via `python3 ./ecc_dashboard.py` or `npm run dashboard`, providing a GUI surface to the install/sessions/status data.
- **Long-form prose:** `the-shortform-guide.md` (16 KB), `the-longform-guide.md` (15 KB), `the-security-guide.md` (28 KB), `WORKING-CONTEXT.md` (29 KB), `README.md` (69 KB) — together >150 KB of guide content, much of it duplicated as marketing in the README.

## Project Identity

`SOUL.md` is a small (1.1 KB) declaration of project identity. Notably, it states **"Everything Claude Code (ECC) is a production-ready AI coding plugin with 30 specialized agents, 135 skills, 60 commands, and automated hook workflows for software development."** ([SOUL.md](https://github.com/affaan-m/everything-claude-code/blob/main/SOUL.md)) **[OFFICIAL]**. So SOUL.md (30/135/60), the plugin manifest description (38/156/72), and the live repo (48/183/79) all disagree with each other. SOUL.md hasn't been updated to match the v1.10.0 surface refresh.

`agent.yaml` (the gitagent manifest) lists ~135 skill names and ~80 command names explicitly — closer to the SOUL/manifest counts than to the actual `skills/` directory.

`SOUL.md` declares 5 Core Principles: Agent-First, Test-Driven, Security-First, Immutability, Plan Before Execute. It also names the harness portability story: "This gitagent surface is an initial portability layer for ECC's shared identity, governance, and skill catalog."

## Release & Activity Cadence

12 GitHub Releases between 2026-01-22 (`v1.0.0` "Official Plugin Release") and 2026-04-05 (`v1.10.0`). That is 10 minor releases in ~75 days — roughly one every week. Major release themes per CHANGELOG **[OFFICIAL]**:

- v1.1: Cross-Platform Support
- v1.2: Unified Commands & Skills
- v1.3: Complete OpenCode Plugin Support
- v1.4: Multi-Language Rules, Installation Wizard & PM2 Orchestration
- v1.5: Universal Edition
- v1.6: Codex Edition + GitHub App
- v1.7: Cross-Platform Expansion & Presentation Builder
- v1.8: Harness Performance & Cross-Platform Reliability
- v1.9: Selective Install, ECC Tools Pro, 12 Language Ecosystems
- v1.10: Surface Refresh, Operator Workflows, ECC 2.0 Alpha

Total commits on main: ~1,465 (derived from Link header `rel="last"` at `per_page=1`) **[OFFICIAL]**. README.md alone has been touched by ~197 distinct commits — heavy README churn is part of the project's signature.

Top contributors (verified) **[OFFICIAL]**:

- `affaan-m` — 965 commits (~66% of total commits)
- `pangerlkr` — 47
- `Copilot` — 22 (GitHub Copilot bot)
- `pvgomes` — 15
- `Lidang-Jiang` — 14
- `dependabot[bot]` — 14
- `ozoz5`, `pythonstrup`, `shimo4228` — 12 each
- 150 more long-tail contributors

Two-thirds of all commits are by the original author. The bulk of "157+ contributors" are long-tail one- to three-commit drive-bys — typical for any project with very high star-to-code ratio.

## Summary of Hard Counts (verified 2026-04-26)

| Component                         | Live count               | Plugin manifest claim    | SOUL.md claim |
| --------------------------------- | ------------------------ | ------------------------ | ------------- |
| Agents (`agents/*.md`)            | **48**                   | 38                       | 30            |
| Skills (`skills/<name>/`)         | **183**                  | 156                      | 135           |
| Commands (`commands/*.md`)        | **79**                   | 72                       | 60            |
| Rules (`rules/**/*.md`)           | **89** in 15 sub-dirs    | —                        | —             |
| Hook scripts (`scripts/hooks/*`)  | **40**                   | "production-ready hooks" | "automated hook workflows" |
| MCP servers (root `.mcp.json`)    | **6**                    | —                        | —             |
| MCP servers (catalog)             | **24+**                  | —                        | —             |
| GitHub stars                      | **167,488**              | (badge "140K+")          | —             |
| GitHub forks                      | **25,969**               | (badge "21K+")           | —             |
| Contributors                      | **159**                  | (badge "170+")           | —             |
| Releases                          | **12**                   | —                        | —             |
| Total commits on main             | **~1,465**               | —                        | —             |
| Test-like files                   | **102**                  | "1,282 tests" (Gemini)   | —             |

## Sources

- [GitHub repo metadata API](https://api.github.com/repos/affaan-m/everything-claude-code) — stars, forks, watchers, license, created/pushed dates, topics
- [Repo root listing](https://github.com/affaan-m/everything-claude-code) — top-level dirs/files
- [README.md](https://github.com/affaan-m/everything-claude-code/blob/main/README.md) — marketing claims, cross-harness pitch, release headline
- [README.md (raw size)](https://api.github.com/repos/affaan-m/everything-claude-code/contents/README.md) — 68,693 bytes
- [CHANGELOG.md](https://github.com/affaan-m/everything-claude-code/blob/main/CHANGELOG.md) — v1.10.0 surface refresh, "38 agents, 156 skills, 72 commands" sync claim
- [.claude-plugin/plugin.json](https://github.com/affaan-m/everything-claude-code/blob/main/.claude-plugin/plugin.json) — canonical plugin manifest
- [.claude-plugin/marketplace.json](https://github.com/affaan-m/everything-claude-code/blob/main/.claude-plugin/marketplace.json) — marketplace entry
- [.codex-plugin/plugin.json](https://github.com/affaan-m/everything-claude-code/blob/main/.codex-plugin/plugin.json) — Codex plugin manifest
- [package.json](https://github.com/affaan-m/everything-claude-code/blob/main/package.json) — `ecc-universal` npm package
- [agent.yaml](https://github.com/affaan-m/everything-claude-code/blob/main/agent.yaml) — gitagent manifest
- [CLAUDE.md](https://github.com/affaan-m/everything-claude-code/blob/main/CLAUDE.md) — architecture overview
- [SOUL.md](https://github.com/affaan-m/everything-claude-code/blob/main/SOUL.md) — project identity (30/135/60)
- [agents/ directory listing](https://github.com/affaan-m/everything-claude-code/tree/main/agents) — 48 markdown agent files
- [agents/code-reviewer.md](https://github.com/affaan-m/everything-claude-code/blob/main/agents/code-reviewer.md) — sample agent
- [agents/planner.md](https://github.com/affaan-m/everything-claude-code/blob/main/agents/planner.md) — sample agent
- [skills/ directory listing](https://github.com/affaan-m/everything-claude-code/tree/main/skills) — 183 skill directories
- [skills/tdd-workflow/SKILL.md](https://github.com/affaan-m/everything-claude-code/blob/main/skills/tdd-workflow/SKILL.md) — sample skill
- [skills/agentic-engineering/SKILL.md](https://github.com/affaan-m/everything-claude-code/blob/main/skills/agentic-engineering/SKILL.md) — sample skill
- [commands/ directory listing](https://github.com/affaan-m/everything-claude-code/tree/main/commands) — 79 command files
- [hooks/hooks.json](https://github.com/affaan-m/everything-claude-code/blob/main/hooks/hooks.json) — canonical hook settings
- [scripts/hooks/ listing](https://github.com/affaan-m/everything-claude-code/tree/main/scripts/hooks) — 40 hook scripts
- [.mcp.json](https://github.com/affaan-m/everything-claude-code/blob/main/.mcp.json) — 6 default MCP servers
- [mcp-configs/mcp-servers.json](https://github.com/affaan-m/everything-claude-code/blob/main/mcp-configs/mcp-servers.json) — 24+ MCP server templates
- [GitHub releases](https://github.com/affaan-m/everything-claude-code/releases) — 12 releases (v1.0.0 to v1.10.0)
- [Languages API](https://api.github.com/repos/affaan-m/everything-claude-code/languages) — JS 51%, Rust 38%, Python 5%, Shell 3%, TS 1%, PowerShell <1%
- [Contributors API](https://api.github.com/repos/affaan-m/everything-claude-code/contributors) — 159 total, top contributor `affaan-m` 965 commits
- [Recursive git tree main](https://api.github.com/repos/affaan-m/everything-claude-code/git/trees/main?recursive=1) — 2,662 entries, full extension and path counts
