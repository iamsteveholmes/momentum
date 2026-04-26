---
content_origin: claude-code-subagent
date: 2026-04-26
sub_question: "Direct feature parallels between everything-claude-code and Momentum"
topic: "everything-claude-code vs Momentum — comparative analysis"
---

# Feature Parallels — `everything-claude-code` (ECC) vs Momentum

## Inline Summary

ECC and Momentum overlap on roughly a dozen primitives — agents/skills/hooks plugin shape, an adversarial generator-evaluator validation idea, project-scoped persistent memory/instincts, ADR/decision capture, code review, harness orchestration, model routing, and a session-start hook — but the **divergence is largest where Momentum is most opinionated**: Momentum is built around an end-to-end *delivery practice* (sprints → epics → stories → AVFL gating → retros → distillation → version-on-release), while ECC is built around a *performance/optimization toolbox* for AI agent harnesses (token budgeting, instinct extraction, security scanning, multi-harness portability). The two systems answer different questions: ECC asks "how do I make this agent harness produce better code, faster, more cheaply?", and Momentum asks "how do I run a disciplined agentic engineering practice across many projects?"

## Sides at a Glance [OFFICIAL]

| Dimension | Momentum (this repo) | ECC (`affaan-m/everything-claude-code`) |
|---|---|---|
| Plugin name / version | `momentum` v0.17.0 [OFFICIAL] | `everything-claude-code` v1.10.0 [OFFICIAL] |
| Author | Steve Holmes (single dev) [OFFICIAL] | Affaan Mustafa, ~170 contributors per README [OFFICIAL] |
| Distribution | Claude Code plugin marketplace [OFFICIAL] | Claude Code plugin marketplace + `npm: ecc-universal` + manual installer (`install.sh` / `install.ps1` / `npx ecc-install`) [OFFICIAL] |
| Cross-harness | Claude Code only [OFFICIAL] | Claude Code, Codex, Cursor, OpenCode, Gemini, plus `.kiro/`, `.trae/`, `.codebuddy/` adapter dirs [OFFICIAL] |
| Skill count | 25 skills [OFFICIAL] | 183 skills [OFFICIAL] |
| Agent count | 7 agent .md files (`agents/dev*.md`, `e2e-validator.md`, `qa-reviewer.md`) + `agents/evals/` [OFFICIAL] | 48 agent .md files [OFFICIAL] |
| Command count | 16 slash commands in `commands/` [OFFICIAL] | 79 legacy command shims [OFFICIAL] |
| Hooks | settings.json hooks (commit-checkpoint, plan-audit gate) [PRAC] | `hooks/hooks.json` with ~8 PreToolUse + ~6 PostToolUse + SessionStart + PreCompact hooks, all dispatched through Node bootstrap scripts [OFFICIAL] |
| MCP configs | None shipped in plugin [OFFICIAL] | Root `.mcp.json` pre-configures **6 MCP servers** (github, context7, exa, memory, playwright, sequential-thinking); `mcp-configs/mcp-servers.json` catalog lists **24+ MCP server templates** (jira, github, firecrawl, supabase, memory, omega-memory, sequential-thinking, vercel, railway, cloudflare-*, clickhouse, exa-web-search, context7, magic, …) [OFFICIAL] |
| Source files (top-level) | Lean: `module/`, `docs/`, `skills/`, `_bmad-output/` [OFFICIAL] | Heavy: 11 IDE-adapter directories (`.cursor/`, `.codex/`, `.kiro/`, `.opencode/`, `.gemini/`, `.trae/`, `.codebuddy/`, …), `ecc2/` Rust prototype, `ecc_dashboard.py` Tkinter GUI, `tests/`, `manifests/`, `schemas/`, `plugins/`, `package.json` with TS/Node toolchain [OFFICIAL] |

Counts are repository-as-of-2026-04-26 readings; ECC's README claims "48 agents, 183 skills, 79 legacy command shims" and the plugin.json states "38 agents, 156 skills, 72 legacy command shims" — the README and plugin.json disagree. Filesystem listings via the GitHub contents API match the README's higher count [OFFICIAL].

The earlier upstream report's claim of "1,282 automated tests, 14 MCP integrations, 102 AgentShield rules" is partially supported: the **README** boasts those numbers in the v1.6.0 release notes, but the actual `mcp-configs/mcp-servers.json` declares ~17 servers and the test suite count cannot be verified from the filesystem listing alone. Treat README marketing numbers as **[UNVERIFIED]** unless cross-checked against the manifest [PRAC].

---

## Mapping Exercise — Capability by Capability

The order below mirrors the sub-question's checklist. For each capability, ECC analogue and Momentum analogue are placed side by side with file paths.

### 1. Sprint planning, stories, and the delivery loop

**Momentum [OFFICIAL]:**
- `skills/momentum/skills/sprint-planning/` — sprint-planning skill (story selection, team composition, Gherkin specs, activation).
- `skills/momentum/skills/sprint-manager/` — sole writer of `stories/index.json` and `sprints/index.json`; validates state transitions.
- `skills/momentum/skills/sprint-dev/` — sprint execution: dependency-driven story development, post-merge AVFL, team review.
- `skills/momentum/skills/create-story/` — produces a Momentum story with change-type classification, EDD/TDD guidance, AVFL validation.
- `skills/momentum/skills/intake/` — captures a story idea as a backlog stub (fast context preservation).
- `_bmad-output/implementation-artifacts/intake-queue.jsonl` — append-only event log for backlog intake.
- `_bmad-output/implementation-artifacts/stories/index.json` — single source of truth for story status.

**ECC [OFFICIAL]:**
- `skills/blueprint/SKILL.md` — "turn a one-line objective into a step-by-step construction plan" with self-contained context briefs for each step. Closest ECC analogue to story creation.
- `commands/plan.md` — invokes the `planner` agent to produce phases, dependencies, complexity estimates, and waits for confirmation.
- `commands/feature-dev.md` — 7-phase guided feature workflow: Discovery → Codebase Exploration → Clarifying Questions → Architecture Design → Implementation → Quality Review → Summary.
- `agents/planner.md`, `agents/code-architect.md` — the agents `/plan` and `/feature-dev` orchestrate.
- `commands/prp-plan.md`, `prp-implement.md`, `prp-pr.md`, `prp-prd.md`, `prp-commit.md` — "PRP" pipeline for artifact-producing planning.

**Verdict:** Partial overlap on *the act of planning before coding*. ECC has no concept of a sprint, no `index.json` story registry, no state machine for story lifecycle, no change-type taxonomy, and no separate skill that is the "sole writer" of any registry. [Scan method: recursive tree grep for `sprint`, `backlog`, `state-machine`, `index.json`, `epic` across 2,662 ECC path entries — all return 0 matches; confirmed independently by `research-momentum-superior.md`.] ECC's planning is per-task; Momentum's is portfolio-level. The closest ECC analogue is `blueprint` + `prp-*` commands, which produce a *plan file* but not a tracked, status-managed story.

### 2. Multi-agent orchestration and parallel waves

**Momentum [OFFICIAL]:**
- `skills/momentum/skills/impetus/SKILL.md` — practice orchestrator. Reads sprint state, dispatches workflows, never acts without consent.
- `skills/momentum/skills/sprint-dev/` — parallel waves of `momentum:dev` invocations across worktrees, dependency-driven.
- `skills/momentum/skills/dev/` — pure executor: resolves a story, creates a worktree, delegates to `bmad-dev-story`, emits a completion signal.
- Memory: `~/.claude/projects/-Users-steve-projects-momentum/memory/MEMORY.md` notes that "Impetus ALWAYS spawns all subagents directly. No direct-invocation workarounds. Exclusive write authority per file." [PRAC]
- `~/.claude/rules/spawning-patterns.md` — Fan-Out vs TeamCreate decision rule [PRAC].

**ECC [OFFICIAL]:**
- `skills/dmux-workflows/SKILL.md` — multi-agent orchestration via `dmux` (a tmux pane manager for AI agents). Patterns 1–5 cover research+implement, multi-file feature, test+fix loop, cross-harness, code-review pipeline.
- `skills/autonomous-agent-harness/`, `skills/continuous-agent-loop/`, `skills/autonomous-loops/` — long-running loop skills.
- `commands/orchestrate.md` (legacy shim) → delegates to `dmux-workflows` and `autonomous-agent-harness`. Mentions `node scripts/orchestrate-worktrees.js plan.json --execute` and `seedPaths` for overlay of dirty files into worker worktrees.
- `skills/team-builder/SKILL.md` — interactive picker for composing ad-hoc parallel teams from a directory of agent persona files.
- `commands/multi-plan.md`, `multi-execute.md`, `multi-backend.md`, `multi-frontend.md`, `multi-workflow.md` — multi-agent commands gated on the external `ccg-workflow` runtime.
- `commands/pm2.md` — PM2 process supervisor integration for managing multi-service workflows.

**Verdict:** Both have parallel multi-agent. ECC's parallelism is **process-level (tmux panes, PM2)** and **cross-harness** (Claude Code + Codex + OpenCode in different panes). Momentum's parallelism is **agent-level inside one Claude Code session** (Fan-Out via `Agent` tool spawns, or TeamCreate for collaborative teams) and **worktree-isolated** for sprint-dev. Different mechanisms; same underlying goal.

### 3. Validation loops (Momentum's AVFL)

**Momentum [OFFICIAL]:**
- `skills/momentum/skills/avfl/SKILL.md` — Adversarial Validate-Fix Loop. Multi-phase pipeline with dual reviewers (Enumerator + Adversary) per lens, profile-based scoring (gate/checkpoint/full/scan), corpus mode for cross-document validation, authority-hierarchy resolution. Cites Meta-Judge 2025 (~8 pp accuracy gain from dual reviewers with different framings) and ASCoT 2025 (late-stage errors 3.5× more damaging).
- Three benchmarked variants visible in available-skills list: `avfl-2lens`, `avfl-3lens`, `avfl-declining`.

**ECC [OFFICIAL]:**
- `skills/gan-style-harness/SKILL.md` — explicitly cites "Anthropic's Harness Design for Long-Running Application Development" (March 24, 2026). Three roles: **Planner** (Opus 4.6) → **Generator** (Opus 4.6) → **Evaluator** (Opus 4.6 + Playwright MCP). Iterates 5–15 times. Scores against 4 weighted criteria (Design Quality, Originality, Craft, Functionality).
- `agents/gan-planner.md`, `gan-generator.md`, `gan-evaluator.md` — the three roles as standalone agent files.
- `commands/gan-build.md`, `gan-design.md` — slash entry points.
- `skills/verification-loop/SKILL.md` — six-phase verification (build → typecheck → lint → tests → security scan → diff review) producing a structured PASS/FAIL report. More like a checklist than an adversarial loop.

**Verdict:** **Strong philosophical overlap, different shape.** Both systems explicitly endorse "the generator should not grade itself; use a separate ruthless evaluator." ECC has two skills in this neighborhood: `gan-style-harness` (Generator + Evaluator + Playwright — engineered for *building a whole app from a prompt* with live-app evaluation) and `santa-method` (dual independent reviewers, binary verdict, fix loop — closer in spirit to AVFL). Neither matches AVFL's lens-decomposed multi-profile design. AVFL has corpus mode and authority-hierarchy resolution; neither ECC skill has that. `santa-method` is the closer AVFL analogue (adversarial dual-review + fix loop) but is binary and undecomposed; `gan-style-harness` adds live-app Playwright testing which AVFL lacks. ECC's `verification-loop` is a thinner peer to AVFL's `gate` profile.

### 4. Retrospectives

**Momentum [OFFICIAL]:**
- `skills/momentum/skills/retro/SKILL.md` — sprint retrospective: transcript audit via DuckDB, story verification, auditor team analysis, findings document, sprint closure.
- `skills/momentum/skills/distill/SKILL.md` — practice artifact distillation: applies a session learning or retro Tier-1 finding to the appropriate rule, reference, or skill prompt.

**ECC:** **No analogue [OFFICIAL].** Searched `commands/`, `skills/`, and README for "retro" / "retrospective" / "post-mortem" — nothing. Closest is `commands/save-session.md` and `commands/sessions.md` (session capture/replay) and `skills/continuous-learning-v2` (instinct extraction from sessions), but those are continuous, not punctuated by sprint boundaries, and they don't run an auditor team or close a sprint.

### 5. Plugin distribution

**Momentum [OFFICIAL]:** Claude Code plugin marketplace only. `plugin.json` is minimal (4 fields: name, version, description, author). `marketplace.json` not in the visible plugin dir.

**ECC [OFFICIAL]:** Multi-channel:
- Claude Code plugin marketplace at `everything-claude-code@everything-claude-code`.
- npm package `ecc-universal`.
- Direct manual installer (`install.sh` / `install.ps1` / `npx ecc-install --profile full`).
- `ecc list-installed`, `ecc doctor`, `ecc repair` CLI subcommands per README.
- Selective-install architecture v1.9.0 with `install-plan.js` / `install-apply.js` and a SQLite state store.
- Per-IDE adapter directories (`.cursor/`, `.codex/`, `.opencode/`, etc.) generated as part of install.

**Verdict:** ECC has a far more elaborate distribution story. Momentum is single-channel.

### 6. Memory systems

**Momentum [OFFICIAL]:**
- File-based persistent memory at `~/.claude/projects/<project-hash>/memory/` keyed by project. Index file `MEMORY.md` references named feedback/reference/project notes.
- Impetus sanctum at `{project-root}/_bmad/memory/impetus/` containing `INDEX.md`, `PERSONA.md`, `CREED.md`, `BOND.md`, `MEMORY.md`, `CAPABILITIES.md`. Loaded at session start via the impetus skill (`skills/momentum/skills/impetus/SKILL.md` lines 31–41).

**ECC [OFFICIAL]:**
- `skills/continuous-learning-v2/SKILL.md` — instinct-based learning. Hooks (`PreToolUse`/`PostToolUse`) capture observations into `projects/<project-hash>/observations.jsonl`. A background Haiku agent analyses observations and writes atomic "instincts" with confidence scoring (0.3–0.9), domain tagging (code-style/testing/git/etc.), and project-vs-global scope. v2.1 added project-scoped instincts to prevent cross-project contamination, plus promote-to-global when an instinct is seen in 2+ projects.
- MCP-level memory: `mcp-configs/mcp-servers.json` declares both the Anthropic-flavored `memory` server and the third-party `omega-memory` server ("persistent agent memory with semantic search, multi-agent coordination, and knowledge graphs").
- `commands/save-session.md`, `resume-session.md`, `sessions.md` — session capture and resume.

**Verdict:** **Strong functional overlap, different mechanism.** Both systems have project-scoped persistent memory and both use a project hash to isolate. Momentum's memory is **human-curated**: feedback notes are written explicitly when the user gives feedback. ECC's continuous-learning-v2 is **agent-curated**: a background Haiku analyzer extracts patterns automatically. ECC also has MCP-server-backed memory for semantic search; Momentum's is grep-and-read. Convergent design, opposite philosophies on who curates.

### 7. Hooks-driven enforcement

**Momentum [OFFICIAL]:**
- `~/.claude/rules/plan-audit.md` (project rule) — gate before `ExitPlanMode`: requires a `## Spec Impact` section, invokes `momentum:plan-audit` to write it.
- `.claude/settings.json` hooks for commit checkpoints (per repo rules referencing PostToolUse). [PRAC] — referenced in `~/.claude/rules/git-discipline.md` but the actual hook config wasn't read.

**ECC [OFFICIAL]:** Heavy hook investment in `hooks/hooks.json`:
- **PreToolUse** matchers: Bash dispatcher (quality/tmux/push/GateGuard checks); Write doc-file warning; Edit|Write compaction suggester; `*` continuous-learning observer (async, 10s timeout); Bash|Write|Edit|MultiEdit governance-capture; Write|Edit|MultiEdit config-protection (blocks linter/formatter config edits — "steers agent to fix code instead of weakening configs"); `*` MCP health-check; Edit|Write|MultiEdit GateGuard fact-force gate.
- **PreCompact** `*` save-state hook.
- **SessionStart** `*` bootstrap loading previous context and detecting package manager.
- **PostToolUse** Bash dispatcher; Edit|Write|MultiEdit quality-gate; design-quality-check (warns on generic-looking UI edits); post-edit accumulator (records JS/TS files for batch format+typecheck at Stop time); Edit console-warn (flags `console.log`); governance-capture.
- All hooks are dispatched through `scripts/hooks/plugin-hook-bootstrap.js` with a `CLAUDE_PLUGIN_ROOT` resolver that searches multiple plugin install paths.
- Runtime gating via `ECC_HOOK_PROFILE=minimal|standard|strict` and `ECC_DISABLED_HOOKS=...` per v1.8.0 release notes.

**Verdict:** **ECC's hook system is far more elaborate than Momentum's.** ECC has a layered, profile-gated, dispatcher-pattern hook framework with at least 14 distinct hook IDs. Momentum has targeted hooks (commit checkpoint, plan-audit gate) but isn't built around hooks the way ECC is. The `gateguard` skill alone (`+2.25 points` reported quality lift in two A/B tests) is an ECC-specific design pattern with no Momentum analogue.

### 8. Decision documents

**Momentum [OFFICIAL]:**
- `skills/momentum/skills/decision/SKILL.md` — "Decision recorder — not deliberator. The thinking already happened. This skill captures what was decided, links it to source material, and bridges to story creation." Walks findings, records adopt/reject/defer, writes a linked SDR document.
- Memory note: never use SDR/ASR acronyms in conversation — say "decision document" / "assessment document" [PRAC].

**ECC [OFFICIAL]:**
- `skills/architecture-decision-records/SKILL.md` — "Capture architectural decisions made during Claude Code sessions as structured ADRs." Uses Michael Nygard's lightweight ADR format (Context / Decision / Alternatives Considered / Consequences). Auto-detects decision moments from phrases like "we decided to…" or "the reason we're doing X instead of Y is…".
- `skills/council/SKILL.md` — convenes four advisors (Architect, Skeptic, Pragmatist, Critic) for ambiguous decisions under multiple credible paths. Explicitly delegates `Skeptic`, `Pragmatist`, `Critic` to fresh subagents with only the question (anti-anchoring mechanism).

**Verdict:** **Strong overlap on capture; ECC adds deliberation.** Both systems write a structured decision document. Momentum's `decision` skill is post-decision (records what already happened); ECC's `architecture-decision-records` is similar. ECC's `council` skill is a *decision-making* skill, which Momentum lacks — Momentum's design philosophy assumes the user has already deliberated (often via assessment, research, or external thinking).

### 9. Intake / backlog capture

**Momentum [OFFICIAL]:**
- `skills/momentum/skills/intake/SKILL.md` — capture an idea as a backlog stub.
- `_bmad-output/implementation-artifacts/intake-queue.jsonl` — append-only event log.
- `skills/momentum/skills/triage/SKILL.md` — batch-classify observations into six classes, enrich ARTIFACTs, batch-approve, then delegate to intake/distill/decision or queue.

**ECC [OFFICIAL]:** **No direct analogue.** Closest:
- `commands/promote.md` — promote a session learning or instinct (continuous-learning-v2's promote-to-global flow).
- Jira MCP integration in `mcp-configs/mcp-servers.json` and `skills/jira-integration/` — relies on external Jira as the backlog system.
- `skills/continuous-learning-v2/SKILL.md` — observation log at `projects/<hash>/observations.jsonl` is structurally similar to `intake-queue.jsonl` but captures *agent behaviour observations* not *story ideas*.

**Verdict:** ECC outsources backlog management to Jira (or assumes the user does). Momentum has its own native intake queue and triage skill.

### 10. Feature/epic/story taxonomy

**Momentum [OFFICIAL]:**
- `skills/momentum/skills/feature-grooming/SKILL.md` — feature taxonomy discovery, value analysis, `features.json` maintenance.
- `skills/momentum/skills/epic-grooming/SKILL.md` — orphan resolution, story reclassification.
- `skills/momentum/skills/feature-status/SKILL.md` — generates an HTML planning artifact showing feature coverage, story assignments, status. Opens in a browser pane.
- `skills/momentum/skills/feature-breakdown/SKILL.md` — enumerate missing stories for a feature end-to-end.
- `skills/momentum/skills/refine/SKILL.md` — backlog hygiene: planning artifact drift, status mismatches, stale-story triage.
- `.claude/momentum/feature-status.html` and `.claude/momentum/feature-status.md` (modified per current git status) — feature dashboard outputs.

**ECC [OFFICIAL]:** **No analogue.** ECC has no concept of "feature" as a tracked taxonomy item, no `features.json`, no epic/feature/story hierarchy, no status visualization. Closest is `skills/product-capability/` and `skills/product-lens/` (skill names visible in the skills/ listing) — content not read but the names suggest product-oriented framing rather than taxonomy management. The README's `ecc_dashboard.py` Tkinter GUI displays installed plugin components (agents, skills, commands, rules) — *not* product features.

### 11. Change-type classification on stories

**Momentum [OFFICIAL]:**
- `skills/momentum/skills/create-story/SKILL.md` — "Creates a Momentum story with **change-type classification**, injected EDD/TDD guidance, and AVFL validation." Implies the story creation flow tags each story with a change-type.

**ECC [OFFICIAL]:** **No analogue.** No story concept → no story-level metadata. ECC's commands `feature-dev.md`, `tdd.md`, `build-fix.md`, `refactor-clean.md` are themselves *change-type-shaped commands*, but the change-type is a routing decision the user makes, not metadata on a tracked artifact.

### 12. Code review and adversarial review

**Momentum [OFFICIAL]:**
- `skills/momentum/skills/code-reviewer/SKILL.md` — "Adversarial code reviewer with read-only tools. Produces structured findings reports. Invoked by VFL — do not invoke directly."
- `skills/momentum/skills/qa-reviewer.md` (in `agents/`) — agent persona invoked during sprint-dev review.
- `skills/momentum/skills/architecture-guard/SKILL.md` — pattern-drift detection against architecture decisions; read-only.
- `skills/momentum/skills/upstream-fix/SKILL.md` — traces quality failures upstream to spec/rule/workflow root cause.

**ECC [OFFICIAL]:**
- `agents/code-reviewer.md`, `code-architect.md`, `architect.md`, plus language-specific reviewers: `typescript-reviewer.md`, `python-reviewer.md`, `go-reviewer.md`, `rust-reviewer.md`, `java-reviewer.md`, `kotlin-reviewer.md`, `csharp-reviewer.md`, `cpp-reviewer.md`, `flutter-reviewer.md`, `database-reviewer.md`, `security-reviewer.md`, `healthcare-reviewer.md`.
- `agents/silent-failure-hunter.md`, `pr-test-analyzer.md`, `comment-analyzer.md`, `type-design-analyzer.md` — specialized reviewer agents.
- `skills/security-bounty-hunter/`, `skills/security-review/`, `skills/security-scan/` — security reviewers.
- `commands/code-review.md`, `commands/review-pr.md`.
- `agents/refactor-cleaner.md`, `code-simplifier.md`.

**Verdict:** **ECC has dramatically more language-specific reviewers; Momentum has a tighter integration into the AVFL flow.** ECC's reviewers are independently invocable agents (e.g., `/code-review` runs `code-reviewer`); Momentum's `code-reviewer` is gated by AVFL (the SKILL.md notes "do not invoke directly"). Different invocation models.

### 13. Test/eval frameworks

**Momentum [OFFICIAL]:**
- `agents/evals/` directory exists in plugin (contents not enumerated above; only the dir was listed).
- AVFL can validate test artifacts; create-story injects EDD/TDD guidance.

**ECC [OFFICIAL]:**
- `skills/eval-harness/SKILL.md` — formal evaluation framework implementing eval-driven development (EDD): capability evals, regression evals, code-based / LLM / human graders, pass@k metrics.
- `skills/agent-eval/SKILL.md` — eval-driven for agents specifically.
- `skills/ai-regression-testing/SKILL.md`.
- `skills/healthcare-eval-harness/SKILL.md` — domain-specific eval framework.
- `skills/tdd-workflow/SKILL.md`, `agents/tdd-guide.md`, `commands/tdd.md` — TDD pipeline.
- Per-language testing skills: `python-testing`, `golang-testing`, `kotlin-testing`, `rust-testing`, `csharp-testing`, `cpp-testing`, `perl-testing`, `springboot-tdd`, `django-tdd`, `laravel-tdd`.

**Verdict:** **Both endorse EDD/TDD; ECC has a deeper, more formal eval-harness.** ECC's `eval-harness` is the most concrete EDD implementation in either repo. Momentum has the AVFL framework which validates a wider variety of artifacts (not just code/agents) but has no comparable pass@k or capability/regression eval taxonomy.

### 14. Session orientation / first-impression

**Momentum [OFFICIAL]:**
- `skills/momentum/skills/impetus/SKILL.md` — fully personality-loaded session orchestrator with three laws, a "sanctum" of memory files, and an awakening conversation on first install. Memory note flags impetus first-impression as needing personality (ASCII art, nerdfont icons, identity) [PRAC].

**ECC [OFFICIAL]:**
- `hooks/hooks.json` `SessionStart` matcher `*` runs `scripts/hooks/session-start-bootstrap.js` to "load previous context and detect package manager."
- `commands/resume-session.md`, `commands/sessions.md` — session resume.
- No persona-shaped orchestrator; bootstrap is mechanical.

**Verdict:** Both systems do *something* on session start. Momentum's is character-driven (Impetus as orchestrator). ECC's is utilitarian (load context, detect package manager).

### 15. Token / cost / model-routing discipline

**Momentum [OFFICIAL]:**
- `~/.claude/rules/model-routing.md` — "Route tasks to models based on cognitive requirements declared in skill frontmatter." [PRAC]
- Skill frontmatter: `model: claude-opus-4-6` / `claude-sonnet-4-6` and `effort: low|medium|high` declared in each SKILL.md (e.g., `impetus` is `sonnet-4-6 / low`; `sprint-dev` is `opus-4-6 / high`; `avfl` is `opus-4-6 / high`).

**ECC [OFFICIAL]:**
- `skills/agentic-engineering/SKILL.md` — "Model Routing: Haiku for classification/boilerplate, Sonnet for implementation, Opus for architecture / root-cause / multi-file invariants."
- `skills/token-budget-advisor/`, `skills/context-budget/`, `skills/cost-aware-llm-pipeline/` — token/cost budget skills.
- `skills/strategic-compact/` — context compaction strategy.
- `commands/model-route.md`, `commands/context-budget.md`, `commands/quality-gate.md`.
- `skills/harness-optimizer/` and `agents/harness-optimizer.md` — harness performance optimization.
- README v1.8.0 release notes: ECC reframed as "harness-first" performance system.

**Verdict:** Both systems share the *philosophy* of cost-aware tier routing (Haiku/Sonnet/Opus). Momentum encodes this in skill frontmatter and a global rule. ECC encodes it in dedicated skills, commands, and a "harness-first" framing that makes it the centerpiece. ECC has a richer toolkit; Momentum has a tighter coupling between routing decisions and skill metadata.

### 16. Continuous learning / instinct distillation

**Momentum [OFFICIAL]:**
- `skills/momentum/skills/distill/SKILL.md` — applies a session learning or retro Tier-1 finding to the appropriate rule, reference, or skill prompt. Invoked manually or from retro Phase 5.

**ECC [OFFICIAL]:**
- `skills/continuous-learning-v2/SKILL.md` (v2.1) — automated, hook-driven, project-scoped instinct extraction with confidence scoring and evolution path (instincts → cluster → skill/command/agent). `commands/learn.md`, `learn-eval.md`, `evolve.md`, `instinct-import.md`, `instinct-export.md`, `instinct-status.md`, `promote.md`.
- `skills/skill-stocktake/`, `commands/skill-create.md`, `commands/skill-health.md` — meta-skills on skill quality.

**Verdict:** **Same idea, opposite curation model.** Momentum's `distill` is human-triggered, applied immediately, surgically. ECC's `continuous-learning-v2` is hook-driven, automatic, with confidence-weighted aggregation and a formal evolution path. ECC's mechanism produces a long tail of low-confidence atomic learnings; Momentum's produces a small set of high-confidence rule changes.

### 17. Quick-fix / single-story flow

**Momentum [OFFICIAL]:**
- `skills/momentum/skills/quick-fix/SKILL.md` — single-story fix: define, specify, implement, validate, merge in one streamlined flow.
- `~/.claude/projects/-Users-steve-projects-momentum/memory/feedback_quickfix_epic_ad_hoc.md` — convention: always use epic_slug "ad-hoc" [PRAC].

**ECC [OFFICIAL]:**
- `commands/build-fix.md` — bug fix workflow.
- `commands/refactor-clean.md` — refactoring workflow.
- `commands/feature-dev.md` (covered above) — guided feature workflow.
- No single skill that bundles "specify + implement + validate + merge" the way Momentum's quick-fix does. ECC's pieces are separately invocable.

**Verdict:** Momentum's quick-fix is a *bundled* workflow; ECC's equivalent is *composable*. Both reach the same outcome.

### 18. Plan audit / spec-impact gate

**Momentum [OFFICIAL]:**
- `skills/momentum/skills/plan-audit/SKILL.md` — audits the active plan for spec impact, classifies trivial vs substantive, writes a Spec Impact section before plan mode exits.
- Project rule `.claude/rules/plan-audit.md` enforces: "Do not call `ExitPlanMode` until `## Spec Impact` is present in the active plan file."

**ECC [OFFICIAL]:** **No direct analogue.** Closest is `commands/plan.md`'s WAIT-FOR-CONFIRMATION pattern and the GateGuard fact-forcing pre-edit gate. Neither requires a *spec-impact* section in a plan file.

### 19. Specialized engineering "guardrails" (configs, secrets, console.log, design quality, …)

**Momentum [OFFICIAL]:**
- `skills/momentum/skills/architecture-guard/SKILL.md` — pattern-drift detection.
- `skills/momentum/skills/agent-guidelines/SKILL.md` — discovers project stack, researches breaking changes, generates path-scoped rules.
- Project rules in `.claude/rules/` (workflow-fidelity, plan-audit, version-on-release).

**ECC [OFFICIAL]:** Many guardrails embedded as PreToolUse / PostToolUse hooks (per §7 above):
- `pre:edit-write:gateguard-fact-force` — fact-forcing gate.
- `pre:config-protection` — block linter/formatter config edits.
- `pre:write:doc-file-warning` — warn about non-standard documentation files.
- `pre:edit-write:suggest-compact` — compaction suggestion.
- `post:quality-gate` — run quality gate after edits.
- `post:edit:design-quality-check` — warn when frontend edits drift toward generic UI.
- `post:edit:console-warn` — flag `console.log` after edits.
- `post:governance-capture`, `pre:governance-capture` — governance event capture.
- `pre:mcp-health-check` — block unhealthy MCP calls.
- `pre:observe:continuous-learning` — capture observations for the learning loop.

**Verdict:** **Largest single divergence in the system.** ECC has a deep, mature, runtime-enforced guardrail layer driven by hooks. Momentum has rules and skills that *describe* guardrails but enforces fewer of them at runtime. This is consistent with ECC's "harness performance system" framing and Momentum's "practice" framing.

### 20. MCP integrations

**Momentum [OFFICIAL]:** None shipped in plugin. Memory-based (file system).

**ECC [OFFICIAL]:** Root `.mcp.json` pre-configures **6 MCP servers** with pinned versions: `github`, `context7`, `exa`, `memory`, `playwright`, `sequential-thinking`. `mcp-configs/mcp-servers.json` contains a larger **catalog of 24+ MCP server templates** including `jira`, `github`, `firecrawl`, `supabase`, `memory`, `omega-memory`, `sequential-thinking`, `vercel`, `railway`, `cloudflare-docs`, `cloudflare-workers-builds`, `cloudflare-workers-bindings`, `cloudflare-observability`, `clickhouse`, `exa-web-search`, `context7`, `magic`, and more. Most catalog entries expect API keys via env vars. Several MCP integrations have matching ECC skills (`skills/jira-integration/`, `skills/clickhouse-io/`, `skills/exa-search/`, `skills/videodb/`, `skills/fal-ai-media/`).

**Verdict:** ECC ships an MCP integration story; Momentum doesn't.

### 21. Cross-language patterns and reviewers

**Momentum [OFFICIAL]:** Language-agnostic. No language-specific skills shipped. `agent-guidelines` discovers project stack at runtime.

**ECC [OFFICIAL]:** Language-specific skills ship in volume:
- Patterns: `python-patterns`, `golang-patterns`, `rust-patterns`, `kotlin-patterns`, `dart-flutter-patterns`, `dotnet-patterns`, `swift-actor-persistence`, `swiftui-patterns`, `springboot-patterns`, `django-patterns`, `laravel-patterns`, `nestjs-patterns`, `nuxt4-patterns`, `nextjs-turbopack`, `bun-runtime`, `compose-multiplatform-patterns`, `pytorch-patterns`, `kotlin-coroutines-flows`, `kotlin-exposed-patterns`, `kotlin-ktor-patterns`, `jpa-patterns`, `postgres-patterns`, `docker-patterns`, `mcp-server-patterns`, `cpp-coding-standards`, `java-coding-standards`, `perl-patterns`, `perl-security`, `perl-testing`, `swift-concurrency-6-2`, `swift-protocol-di-testing`.
- Build resolvers (per language): `go-build-resolver`, `rust-build-resolver`, `java-build-resolver`, `kotlin-build-resolver`, `dart-build-resolver`, `cpp-build-resolver`, `pytorch-build-resolver`.
- README claims "12+ language ecosystems."

**Verdict:** ECC is a battery-included multi-language assistant; Momentum is a stack-agnostic process framework.

### 22. Operator / business / domain skills (out of scope for "engineering" per se)

**Momentum [OFFICIAL]:** None.

**ECC [OFFICIAL]:** Substantial set of operator-lane and business-lane skills:
- `brand-voice`, `social-graph-ranker`, `connections-optimizer`, `customer-billing-ops`, `ecc-tools-cost-audit`, `google-workspace-ops`, `project-flow-ops`, `workspace-surface-audit`, `email-ops`, `messages-ops`, `unified-notifications-ops`, `enterprise-agent-ops`, `automation-audit-ops`.
- Domain skills: `healthcare-cdss-patterns`, `healthcare-emr-patterns`, `healthcare-phi-compliance`, `hipaa-compliance`, `customs-trade-compliance`, `inventory-demand-planning`, `production-scheduling`, `returns-reverse-logistics`, `quality-nonconformance`, `carrier-relationship-management`, `logistics-exception-management`, `energy-procurement`.
- Content / outbound: `article-writing`, `content-engine`, `crosspost`, `seo`, `seo-specialist` (agent), `manim-video`, `remotion-video-creation`, `frontend-slides`, `investor-materials`, `investor-outreach`, `market-research`, `lead-intelligence`.

**Verdict:** ECC has reached far beyond engineering. Momentum is engineering-only.

---

## Side-by-Side Summary Table

| Capability | Momentum | ECC | Overlap rating |
|---|---|---|---|
| Planning (general) | `sprint-planning`, `create-story`, `feature-breakdown` | `blueprint`, `planner` agent, `prp-*` commands, `commands/plan.md` | High |
| Sprint state machine | `sprint-manager`, `stories/index.json`, `sprints/index.json` | none | None |
| Story lifecycle / change-type classification | `create-story` w/ change-type | none | None |
| Multi-agent parallel execution | `sprint-dev` (worktrees), Fan-Out vs TeamCreate | `dmux-workflows`, `team-builder`, `multi-*` commands, PM2 | High |
| Adversarial validation | `avfl` (Enumerator + Adversary per lens) | `gan-style-harness` (Generator + Evaluator + Playwright) | High (different shape) |
| Procedural verification | AVFL `gate` profile | `verification-loop` (6 phases) | Medium |
| Retrospectives | `retro` skill (auditor team, DuckDB transcript audit) | none | None |
| Distribution | Claude Code marketplace only | Marketplace + npm + manual installer + selective install | Low (ECC much broader) |
| Cross-harness | none | Claude Code, Codex, Cursor, OpenCode, Gemini, Kiro, Trae, CodeBuddy | None |
| Persistent memory | File-based, human-curated, per-project | Hook-driven `continuous-learning-v2` (auto, confidence-scored), MCP `memory` + `omega-memory` | High (different curation) |
| Decision capture | `decision` skill | `architecture-decision-records` skill | High |
| Decision deliberation | none | `council` skill | None |
| Backlog intake | `intake` skill, `intake-queue.jsonl`, `triage` | none (uses Jira MCP) | Low |
| Feature taxonomy | `feature-grooming`, `epic-grooming`, `feature-status`, `feature-breakdown`, `refine` | none (engineering side); `product-capability`, `product-lens` (different framing) | Low |
| Hooks layer | Plan-audit gate, commit checkpoint | ~14 hook IDs across PreToolUse / PostToolUse / PreCompact / SessionStart | Low (ECC much deeper) |
| Hook profiles | none | `ECC_HOOK_PROFILE=minimal/standard/strict`, `ECC_DISABLED_HOOKS` | None |
| GateGuard / fact-forcing | none | `gateguard` skill + `pre:edit-write:gateguard-fact-force` hook | None |
| Eval framework | AVFL (artifact-shaped) | `eval-harness` (capability/regression/pass@k) | Medium |
| TDD pipeline | EDD/TDD guidance injected into stories by `create-story` | `tdd-workflow` skill + `tdd-guide` agent + `tdd.md` command + per-language TDD skills | Medium |
| Code review | `code-reviewer` (gated by AVFL) | `code-reviewer` agent + 12+ language-specific reviewers, `code-review.md` command | High (different invocation) |
| Architecture enforcement | `architecture-guard`, `agent-guidelines` | `architect` agent, `code-architect` agent | Medium |
| Upstream root-cause | `upstream-fix` | `silent-failure-hunter` (closest analogue) | Low |
| Quick fix / single-story flow | `quick-fix` (bundled) | `build-fix` + `refactor-clean` (composable) | Medium |
| Plan-audit / spec-impact gate | `plan-audit` skill + project rule | `commands/plan.md` confirmation pattern + GateGuard | Low |
| Session orchestrator | `impetus` (persona-shaped) | `session:start` hook + `resume-session` (mechanical) | Low |
| Model routing | Skill frontmatter (`model:`, `effort:`) + global rule | `agentic-engineering` skill + `token-budget-advisor` + `model-route` command + `harness-optimizer` agent | High (philosophy) |
| Continuous learning | `distill` (manual, surgical) | `continuous-learning-v2` (hook-driven, automatic) | High (opposite curation) |
| MCP integrations | none | 6 servers in `.mcp.json` (defaults) + 24+ in `mcp-servers.json` catalog + matching skills | None |
| Multi-language patterns | none | 30+ language/framework pattern skills | None |
| Operator / business skills | none | ~15 operator-lane skills | None |
| Security scanning | none built-in | `security-scan` skill + `security-bounty-hunter` + `security-review` skills + AgentShield (per README) | None |
| Dashboard / GUI | `feature-status.html` (HTML artifact) | `ecc_dashboard.py` (Tkinter desktop app, dark/light theme) | Low (different audiences) |
| Continuous loop runners | none | `loop-operator` agent, `loop-start.md`, `loop-status.md`, `autonomous-agent-harness`, `continuous-agent-loop`, `autonomous-loops` | None |

---

## Where the Two Systems Are Most Aligned

1. **Adversarial validation as a design pattern.** AVFL's "Enumerator + Adversary per lens" and `gan-style-harness`'s "Generator + Evaluator" both adopt the same anti-pattern of single-agent self-evaluation. Both cite recent research; both treat the evaluator as engineered to be ruthless.
2. **Project-scoped persistent memory.** Both projects keep memory keyed by project hash, both surface a memory index, both are aware of cross-project contamination risk. The user's MEMORY.md notes the same project hashing pattern that ECC's `continuous-learning-v2` v2.1 implements.
3. **Decision document capture.** Both systems write structured decisions tied to source material, both use a recognizable Nygard-style template (Context/Decision/Alternatives/Consequences), both prefer markdown.
4. **Cost-aware model routing.** Both adopt the Haiku/Sonnet/Opus tiering. Both treat model choice as part of the work definition, not an ambient setting.
5. **Multi-agent parallel work as a first-class concept.** Both make parallelism explicit. The mechanisms differ (Momentum's in-process Fan-Out vs ECC's tmux/PM2 panes), but both reject "single-agent serial" as the only legitimate execution mode.
6. **Skill-centric primitives.** Both projects build their core capability surface as skills (markdown files with frontmatter), both use Claude Code's plugin marketplace, both ship slash commands as thin orchestration shims into skills.

## Where the Divergence Is Largest

1. **End-to-end delivery practice (Momentum) vs harness performance toolbox (ECC).** Momentum implements a full agile-derived loop: intake → triage → grooming → sprint planning → sprint dev → AVFL → retro → distill. ECC has *none* of: sprint, story registry, retro, change-type classification, feature taxonomy, intake queue, story-state machine. ECC instead has: hook-driven enforcement, instinct extraction, cross-harness packaging, language-specific scaffolding, cost/token discipline, security scanning.
2. **Hook-driven runtime enforcement.** ECC ships ~14 hooks; Momentum ships a handful. ECC's `gateguard` (fact-forcing pre-edit gate, claimed +2.25 pp quality lift) and `config-protection` (block linter/formatter config edits) have no Momentum analogues.
3. **Cross-harness portability.** ECC explicitly targets Claude Code, Codex, Cursor, OpenCode, Gemini, Kiro, Trae, CodeBuddy, Antigravity. Momentum is Claude Code only.
4. **Language and domain coverage.** ECC ships per-language patterns, build resolvers, reviewers, testing skills, plus operator/healthcare/logistics/energy domain skills. Momentum is stack-agnostic and engineering-only.
5. **MCP server surface.** ECC ships ~17 MCP server configs; Momentum ships none.
6. **Distribution maturity.** ECC has marketplace + npm + manual installer + selective install + state-store + `ecc doctor`/`ecc repair` CLI subcommands. Momentum is single-channel marketplace.
7. **Curation philosophy.** Momentum's memory and rule changes are human-curated; ECC's `continuous-learning-v2` is agent-curated by a background Haiku analyzer with confidence weighting. Different bets on who decides what's worth keeping.

---

## Verifying the Earlier Report's Claims

The previous summary attributed to ECC "48 agents, 183 skills, 14 MCP integrations, 1,282 automated tests, Plugin-Everything architecture, codemaps, Hookify, AgentShield." Filesystem-checked status:

| Claim | Verification |
|---|---|
| "48 agents" | **Confirmed [OFFICIAL]** — `agents/` listing returns 48 entries. The plugin.json says 38; the README lists 48. README appears authoritative. |
| "183 skills" | **Confirmed [OFFICIAL]** — `skills/` listing returns 183 directories. plugin.json says 156; README and filesystem agree on 183. |
| "14 MCP integrations" | **Partially [OFFICIAL]** — `mcp-configs/mcp-servers.json` declares ~17 servers. Number is in the right ballpark; specifics matter. |
| "1,282 automated tests" | **[UNVERIFIED]** — README v1.6.0 release notes claim "1282 tests" and v1.8.0 claims "997 internal tests passing"; v1.7.0 says "992". The number changes per release. The actual `tests/` directory was not enumerated for this report. Treat as marketing-grade. |
| "Plugin-Everything architecture" | **Reasonable framing [OFFICIAL]** — README claims cross-harness support and the repo has 11 IDE-adapter directories. Description matches. |
| "Codemaps" | **Partial [OFFICIAL]** — `commands/update-codemaps.md` exists. Capability is present. |
| "Hookify" | **Confirmed [OFFICIAL]** — `skills/hookify-rules/SKILL.md`, `commands/hookify.md`, `hookify-configure.md`, `hookify-help.md`, `hookify-list.md` all exist. It's a real subsystem. |
| "AgentShield" | **Referenced [OFFICIAL]** — README v1.6.0 release notes say `/security-scan` runs AgentShield, "1282 tests, 102 rules", and the repo has `npm: ecc-agentshield` per the badge. Skill `skills/security-scan/` exists. The 102-rules and 1282-tests numbers are not verified from this filesystem reading. |

Net: the earlier report's high-level claims about ECC are largely accurate. The specific numeric claims (test counts, rule counts) are **marketing-grade** and should be cited as "ECC self-reports X" rather than as ground truth.

---

## Sources

- ECC repository contents API: `https://api.github.com/repos/affaan-m/everything-claude-code/contents` and subdirectories `agents/`, `skills/`, `commands/`, `hooks/`, `mcp-configs/`, fetched 2026-04-26 [OFFICIAL].
- ECC `README.md` (English): `https://raw.githubusercontent.com/affaan-m/everything-claude-code/main/README.md` [OFFICIAL].
- ECC `.claude-plugin/plugin.json` v1.10.0 [OFFICIAL].
- ECC `hooks/hooks.json` (PreToolUse/PostToolUse/PreCompact/SessionStart blocks) [OFFICIAL].
- ECC `mcp-configs/mcp-servers.json` [OFFICIAL].
- ECC SKILL.md files read for: `verification-loop`, `gan-style-harness`, `continuous-learning-v2`, `council`, `dmux-workflows`, `blueprint`, `architecture-decision-records`, `eval-harness`, `agentic-engineering`, `safety-guard`, `gateguard`, `team-builder` [OFFICIAL].
- ECC commands read: `orchestrate.md`, `plan.md`, `feature-dev.md`, `checkpoint.md` [OFFICIAL].
- Momentum local repo at `/Users/steve/projects/momentum/` (skills, plugin.json, project rules, memory index) [OFFICIAL].
- Momentum SKILL.md files read for: `impetus`, `sprint-dev`, `avfl`, `intake`, `decision`, `retro`, `feature-grooming`, `create-story` [OFFICIAL].
- User's project memory index at `~/.claude/projects/-Users-steve-projects-momentum/memory/MEMORY.md` for practice conventions [PRAC].
- User's global rules at `~/.claude/rules/` (cmux, mise, authority-hierarchy, model-routing, anti-patterns, spawning-patterns, workflow-fidelity, git-discipline) [PRAC].
- Project rules at `/Users/steve/projects/momentum/.claude/rules/` (plan-audit, workflow-fidelity, version-on-release) [OFFICIAL].

All ECC counts and quoted claims (e.g., "+2.25 quality lift", "5–15 iterations", "Meta-Judge 2025 ~8 pp") originate from the listed README/SKILL.md files; they are reproduced as ECC self-reports unless otherwise tagged.
