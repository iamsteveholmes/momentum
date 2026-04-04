---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
status: complete
inputDocuments:
  - _bmad-output/planning-artifacts/product-brief-momentum-2026-03-13.md
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/ux-design-specification.md
  - _bmad-output/planning-artifacts/research/technical-agent-skills-deployment-research-2026-03-15.md
  - docs/research/handoff-product-brief-2026-03-14.md
  - docs/research/validate-fix-loop-handoff.md
  - docs/planning-artifacts/AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md
  - README.md
derives_from:
  - id: PRD-MOMENTUM-001
    path: _bmad-output/planning-artifacts/prd.md
    relationship: derives_from
    description: "Momentum PRD with validated FRs, NFRs, and epics structure"
  - id: UX-MOMENTUM-001
    path: _bmad-output/planning-artifacts/ux-design-specification.md
    relationship: derives_from
    description: "Momentum UX design specification — conversational agent interface, knowledge gap UX, visual progress tracking"
  - id: BRIEF-MOMENTUM-001
    path: _bmad-output/planning-artifacts/product-brief-momentum-2026-03-13.md
    relationship: derives_from
    description: "Momentum product brief — philosophy, target users, MVP scope"
  - id: RESEARCH-SKILLS-DEPLOY-001
    path: _bmad-output/planning-artifacts/research/technical-agent-skills-deployment-research-2026-03-15.md
    relationship: derives_from
    description: "Agent Skills deployment research — skills-only model, hooks/rules/MCP deployment constraints, context:fork behavior"
  - id: HANDOFF-BRIEF-001
    path: docs/research/handoff-product-brief-2026-03-14.md
    relationship: derives_from
    description: "Research handoff — provenance system design, VFL validation framework, model routing, skills strategy"
  - id: VFL-HANDOFF-001
    path: docs/research/validate-fix-loop-handoff.md
    relationship: derives_from
    description: "Validate-fix-loop architecture — dual-reviewer system, 15-dimension taxonomy, staged validation"
workflowType: 'architecture'
project_name: 'momentum'
user_name: 'Steve'
date: '2026-03-17'
lastEdited: '2026-04-03'
editHistory:
  - date: '2026-04-03'
    changes: 'Plugin model adoption: Momentum becomes a Claude Code plugin with .claude-plugin/plugin.json. Replaced skills-only flat deployment (npx skills add) with plugin packaging. Namespaced skills under momentum: prefix (momentum-avfl → momentum:avfl, momentum-dev → momentum:dev, etc.). Workflow modules (sprint-planning.md, sprint-dev.md) converted to proper skills invoked as /momentum:sprint-planning and /momentum:sprint-dev. Always-on hooks delivered via plugin hooks/hooks.json (not Impetus-written to settings.json). Rules bundled in plugin references/rules/ (Impetus still writes to ~/.claude/rules/ and .claude/rules/ on first run). Repository structure replaced with plugin root layout. Agent Teams for sprint execution: teammates load skills from project/user settings, sequential execution with commit-as-sync-point. Updated Decisions 5a, 5c, 25, 26, 29 and all deployment, naming, structural, and integration sections.'
  - date: '2026-04-02'
    changes: 'Phase 3 sprint execution architecture: replaced Epic Orchestration Architecture with Sprint Orchestration Architecture (dependency-driven teams over waves, Decision 25); added Sprint Planning Workflow (Decision 29), Sprint Execution Flow (6 phases), Two-Layer Agent Model (Decision 26); replaced momentum-sprint-manager subagent with momentum-tools.py sprint CLI throughout; added Agent Logging Infrastructure section (Decision 24); added Gherkin Specification Separation section (Decision 30); added Phase 3 Architecture Decisions (24-31); replaced Next-Story Selection Rule with Story Assignment Model; updated Read/Write Authority table (new rows for momentum-tools log, sprint-planning, sprint-dev; updated Impetus, momentum-dev, momentum-create-story rows); added sprint-logs to installed structure; added workflows/ directory to repository structure; added specs protection boundary; moved AVFL from per-story to per-sprint (Decision 31); simplified momentum-dev to pure executor (subsuming momentum-dev-auto); removed dag-executor integration section; updated session open sequence and subsystem descriptions.'
  - date: '2026-03-26'
    changes: 'Epic orchestration model: added Epic Orchestration Architecture section (lifecycle, immutability rule, DAG topology, tier-sequential execution); added Agent Pool Governance section (pool cap, AVFL embedding, merge gate, pre-flight checks); added momentum-dev-auto Design section (background-safe variant, behavioral constraints, autonomous-or-fail principle); added dag-executor Integration section (optional sub-skill, tradeoffs, decision criteria); added Retro → Triage Handoff Format section (triage-inbox.md, entry format); added done-incomplete and closed-incomplete statuses to Story State Machine; updated Decision 4c with rolling pool feasibility note (Agent tool available in skill execution context); updated Impetus session open per session-stats deferral and epic progress bar.'
  - date: '2026-03-23'
    changes: 'AVFL integration: renamed momentum-vfl to momentum-avfl throughout; renamed vfl-validator protocol type to avfl-validator; reconciled sub-skill model (AVFL uses own nested sub-skills, not momentum-code-reviewer); updated repo structure with framework.json and sub-skills directory; added AVFL deployment note distinguishing production skill from research benchmarking variants.'
  - date: '2026-03-22'
    changes: 'Added terminal-multiplexer to subsystem 10 Protocol-Based Integration; added Terminal Multiplexer ↔ Workflows integration point with detect-and-adapt pattern. Derives from CMUX research document.'
---

# Architecture Decision Document: Momentum

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements (10 subsystems):**

Momentum's FRs organize into 10 architectural subsystems:

1. **Deployment Packaging** — Claude Code plugin with `.claude-plugin/plugin.json` manifest (`name: "momentum"`). Skills are namespaced under `momentum:` (e.g., `/momentum:impetus`, `/momentum:avfl`, `/momentum:dev`). Plugin root contains `skills/` (all SKILL.md files), `hooks/hooks.json` (always-on hooks delivered by the plugin), `scripts/` (CLI tools), and `references/` (rules, practice docs, version manifest). Flat skills run in main context; `context: fork` skills run in isolated subagent contexts for pure verifiers. Rules are bundled in `references/rules/` and written by Impetus to `~/.claude/rules/` and `.claude/rules/` on first `/momentum:impetus` invocation (the plugin cannot write there directly). Momentum is a Claude Code plugin — hooks, `context:fork`, Agent Teams, and model routing are all Claude Code features.

2. **Provenance Infrastructure** — `derives_from` frontmatter (downstream-only authoring), content hash staleness detection, suspect link flagging (pull-based), auto-generated `referenced_by`, Chain of Evidences prompting, Citations API integration for mechanical grounding.

3. **Hook Infrastructure (Tier 1 Deterministic)** — PostToolUse auto-lint/format, PreToolUse acceptance test directory protection, PreToolUse file protection, PreToolUse git-commit quality gate, PreToolUse plan audit gate (ExitPlanMode), Stop conditional quality gate. Two hook deployment mechanisms: (1) **Always-on hooks** — defined in `hooks/hooks.json` at the plugin root; delivered automatically by the plugin install mechanism; these fire on every matching tool event in every session regardless of which skill is active. (2) **Skill-lifecycle hooks** — defined in SKILL.md `hooks:` frontmatter; scoped to the skill's lifetime; only fire while that skill is active; automatically cleaned up when the skill completes. Complemented by standard git hooks (Husky/pre-commit framework) at the repository level.

4. **Rules Architecture (Tier 3 Advisory)** — Global `~/.claude/rules/` (authority hierarchy, anti-patterns, model routing) + project `.claude/rules/` (architecture conventions, stack-specific standards). Project-scoped rules auto-load in every session including subagents. Rules are bundled in `references/rules/` at the plugin root. The plugin install mechanism does not write to `~/.claude/rules/` or `.claude/rules/` directly — Impetus writes rules to both targets on first `/momentum:impetus` invocation using the Write tool. No separate setup step.

5. **Subagent Composition** — code-reviewer (read-only tools, pure verifier, never modifies code), architecture-guard (pattern drift detection), momentum-dev (story executor, spawned by sprint-dev skill). code-reviewer and architecture-guard use `context: fork` for producer-verifier isolation. momentum-dev runs as a flat subagent (main context) for story execution. Two-layer agent model (Decision 26): Momentum provides generic roles (Dev, QA, E2E Validator, Architect Guard); projects provide role-specific stack guidelines wired together during sprint planning. Agent Teams share a working directory with commit-as-sync-point. Hub-and-spoke: Impetus is the sole user-facing voice; subagents return structured output to Impetus for synthesis. Subagents cannot spawn subagents — chains route through main conversation.

6. **Validate-Fix Loop (VFL) Skill** — Three profiles: Gate (1 agent, pass/fail), Checkpoint (2-4 agents, 1 fix attempt), Full (dual-reviewer per lens, up to 4 fix iterations). Four lenses: Structural Integrity, Factual Accuracy, Coherence & Craft, Domain Fitness. Consolidation handles deduplication, cross-check confidence tagging, and scoring. Invocable standalone, inline from workflows, or declared as a rule.

7. **Orchestrating Agent — Impetus** — Session orientation (reads journal, surfaces active threads), visual progress (✓ Built / → Now / ◦ Next), proactive gap detection, productive waiting during subagent execution, hub-and-spoke voice unification. Impetus is the primary entry-point skill (`/momentum:impetus`) and the recommended path for all Momentum operations. Users can invoke other namespaced skills directly (e.g., `/momentum:sprint-planning`), but Impetus provides session orientation and context that direct invocation skips. For sprint-scoped operations, Impetus dispatches to dedicated skills: `/momentum:sprint-planning` for story selection and team composition, `/momentum:sprint-dev` for dependency-driven execution. Sub-command dispatch: developer selects "Plan a sprint" or "Continue sprint" from the session menu, and Impetus invokes the corresponding skill. Impetus is the force that maintains practice velocity — the system keeps compounding because Impetus carries knowledge and context forward across sessions and sprints without requiring repeated external input.

8. **Findings Ledger + Evaluation Flywheel** — Structured findings with provenance_status field; cross-story pattern detection; flywheel workflow (Detection → Review → Upstream Trace → Solution → Verify → Log) with visual status graphics; `/upstream-fix` skill; retrospective integration.

9. **Model Routing** — `model:` and `effort:` frontmatter required on every SKILL.md and agent definition. Cognitive hazard rule: flagship models for outputs without automated validation. Escalation semantics in VFL: mid-tier first, flagship if not converging within 3-4 iterations.

10. **Protocol-Based Integration** — Every integration point (validation, research, review, tools, documents, terminal multiplexers) defines an interface before implementation is wired. Implementations are substitutable: swap the ATDD framework, the research model, the terminal multiplexer, the validation profile — the practice layer is unchanged.

---

### Non-Functional Requirements

- **Claude Code plugin** — Momentum is a Claude Code plugin. Hooks, `context:fork`, Agent Teams, and model routing are Claude Code features. The plugin model makes explicit what was already true: Momentum is Claude Code-specific.
- **Context budget** — Agent Skills three-stage loading (description at startup ~100 tokens, full SKILL.md on invocation, references/ on demand) means startup overhead is manageable with good authoring discipline. Concise descriptions, heavy content in references/. Hygiene note, not a hard constraint.
- **Evolvability (Impermanence Principle)** — Thin plugin packaging layer. Practice content portable even if the plugin ecosystem changes. Monthly ecosystem review. Interfaces before implementations everywhere.
- **Solo developer efficiency** — One person, limited hours, concurrent with other projects. MVP deploys in days. Real work on real projects is the test harness.
- **Cost as managed dimension** — `model:` + `effort:` frontmatter on every skill. Cognitive hazard rule universal. VFL max 4 iterations (context accumulation makes later iterations progressively more expensive).
- **Terminal-native UX** — No web UI. ASCII/text visual progress. Structured markdown artifacts. Everything works beautifully in a terminal environment.

---

### Scale & Complexity

- **Primary domain:** Developer tooling / practice framework
- **Complexity:** Medium — no regulatory compliance; complexity from multi-tool portability, evolving ecosystem dependencies, and the meta-nature of a practice that governs practices using its own practice
- **Estimated architectural components:** 10 subsystems + 3 cross-cutting concerns = 13 total components
- **Dogfooding as validation:** Momentum is built using its own practice. The system's first test case is itself.

---

### Technical Constraints & Dependencies
<!-- REVISED 2026-04-03: Plugin model adopted. Momentum is a Claude Code plugin with .claude-plugin/plugin.json. -->

- **Claude Code plugin model** — Momentum is packaged as a Claude Code plugin with `.claude-plugin/plugin.json` manifest. Plugin install delivers all skills, hooks, scripts, and references. Skills are namespaced under `momentum:` (e.g., `/momentum:impetus`, `/momentum:avfl`).
- **Subagents cannot spawn subagents** — VFL orchestration chains through main conversation; affects Full-profile parallel execution design
- **context:fork isolation** — `context: fork` is a SKILL.md frontmatter field, Claude Code-exclusive. Skills with `context: fork` run in isolated subagent contexts without access to conversation history. code-reviewer and architecture-guard are implemented as `context: fork` SKILL.md files. The `allowed-tools` frontmatter field restricts tool access (e.g., `Read` only for pure verifiers).
- **Plugin-delivered vs. Impetus-written** — The plugin install delivers SKILL.md files, `hooks/hooks.json` (always-on hooks), `scripts/`, and `references/`. It cannot write to `~/.claude/rules/` or `.claude/rules/`. Rules are bundled in `references/rules/` and written by Impetus on first `/momentum:impetus` invocation. Install/upgrade logic is governed by `references/momentum-versions.json` and `installed.json` (Decision 5c). The UX interaction for install/upgrade is defined in the UX specification.
- **Hooks: two deployment paths** — Always-on hooks (fire every session regardless of skill) are defined in `hooks/hooks.json` at the plugin root, delivered automatically by plugin install. Skill-lifecycle hooks (fire only while a specific skill is active) are defined in SKILL.md `hooks:` frontmatter and require no separate deployment — they travel with the skill. Both are Claude Code features.

---

### BMAD as Practice Substrate

BMAD is not a coexistence challenge — it is Momentum's practice substrate. BMAD provides proven workflow scaffolding (analyst, PM, architect, dev-story, code-review workflows). Momentum is the quality governance layer that makes BMAD workflows momentous:

- **Provenance wrapping** — `derives_from` frontmatter auto-populated on BMAD-generated artifacts; staleness detection fires when upstream docs change
- **VFL validation at BMAD completion gates** — BMAD workflow completes → Impetus fires a checkpoint or full validate-fix loop before the artifact is accepted
- **Commit hooks at workflow boundaries** — BMAD step completes → git commit proposed per git-discipline rules
- **Model routing inheritance** — Momentum's `model:` + `effort:` rules apply to BMAD-invoked skills via rules auto-loading
- **Knowledge dispensation** — Momentum's rules auto-load context BMAD skills don't carry natively (authority hierarchy, anti-patterns, architecture decisions)
- **Optimized subagent replacement** — Momentum's code-reviewer and architecture-guard can supersede or augment BMAD's built-in review steps

The vision: a developer running BMAD workflows gets Momentum's quality layer for free — provenance, enforcement, flywheel — without needing to change how they work.

---

### Cross-Cutting Concerns

1. **Provenance** — Every artifact, every agent output, every specification claim carries derives_from and provenance_status. Affects all 10 subsystems.
2. **Enforcement tier assignment** — Every mechanism has a tier designation. Nothing floats undefined.
3. **Producer-verifier separation** — `context: fork` isolation on all review steps. The producing context never reviews its own output. Each reviewer invocation = one isolated subagent; VFL spawns N reviewers via N Agent tool calls.
4. **Model routing** — model: and effort: frontmatter required on every SKILL.md and agent definition. Cognitive hazard rule applies universally.
5. **Visual progress** — ✓ Built / → Now / ◦ Next at every phase transition across all orchestrated workflows.
6. **Protocol interfaces** — Every integration point defines an interface before any implementation is wired.

---

## Deployment Structure
<!-- REVISED 2026-04-03: Momentum adopts the Claude Code plugin model. .claude-plugin/plugin.json manifest, namespaced skills, hooks/hooks.json for always-on hooks. -->

> _[Changed 2026-03-18: Removed two-unit plugin + skills model. Adopted skills-only deployment via `npx skills add`.]_
> _[Changed 2026-04-03: Adopted Claude Code plugin model. Momentum is packaged as a plugin with `.claude-plugin/plugin.json`. Skills namespaced under `momentum:`. Always-on hooks delivered via `hooks/hooks.json` at plugin root. Workflow modules (sprint-planning, sprint-dev) converted to proper skills. Reason: Momentum already depends entirely on Claude Code features (hooks, context:fork, Agent Teams, model routing) — the plugin model makes this explicit.]_

### Skills Deployment Classification

The defining question for each component: *does this need main-context persona persistence, or does it benefit from isolation?*

| Component | Deployment | Rationale |
|---|---|---|
| Impetus (orchestrating agent) | Flat skill (`/momentum:impetus`) | Must persist persona across interactions; primary entry point |
| Sprint planning | Flat skill (`/momentum:sprint-planning`) | Multi-step workflow needing main context; invoked by Impetus or directly |
| Sprint dev | Flat skill (`/momentum:sprint-dev`) | Dependency-driven execution needing main context; invoked by Impetus or directly |
| AVFL | Flat skill (`/momentum:avfl`) | Must orchestrate parallel spawning from main context |
| upstream-fix, create-story, dev, status, retro, plan-audit | Flat skills | Stateful workflows needing main context |
| code-reviewer | `context: fork` skill | Pure verifier — `context: fork` provides isolation; `allowed-tools: Read` enforces read-only |
| architecture-guard | `context: fork` skill | Pattern analysis — isolation prevents drift; `allowed-tools: Read` enforces read-only |
| Always-on hooks | `hooks/hooks.json` (plugin root) | Delivered by plugin install; fire every session regardless of active skill |
| Global rules | `~/.claude/rules/` | Bundled in `references/rules/` at plugin root; Impetus writes on first run |
| Project rules | `.claude/rules/` | Bundled in `references/rules/` at plugin root; Impetus writes on first run |
| MCP config | `.mcp.json` | Deferred to Epic 6 — no MCP servers configured at 1.0.0. When available, Impetus writes on run. |

### Repository Structure (preview — full structure in Project Structure section)

```
momentum/                              ← Plugin root
├── .claude-plugin/
│   └── plugin.json                   ← { "name": "momentum" }
├── skills/                           ← All skills: flat + context:fork
│   ├── impetus/SKILL.md             ← Orchestrator (/momentum:impetus)
│   ├── sprint-planning/SKILL.md     ← /momentum:sprint-planning
│   ├── sprint-dev/SKILL.md          ← /momentum:sprint-dev
│   ├── dev/SKILL.md                 ← /momentum:dev
│   ├── avfl/SKILL.md               ← + sub-skills/ and references/
│   ├── code-reviewer/SKILL.md      ← context: fork, allowed-tools: Read
│   ├── architecture-guard/SKILL.md  ← context: fork, allowed-tools: Read
│   ├── upstream-fix/SKILL.md
│   ├── create-story/SKILL.md
│   ├── plan-audit/SKILL.md
│   ├── status/SKILL.md
│   └── retro/SKILL.md
├── hooks/
│   └── hooks.json                    ← Always-on hooks (Tier 1 enforcement)
├── scripts/
│   └── momentum-tools.py
└── references/
    ├── rules/                        ← Bundled rules (written to ~/.claude/rules/ by Impetus)
    ├── practice-overview.md
    ├── phase-guide.md
    └── momentum-versions.json
```

### Install Experience
<!-- REVISED 2026-04-03: Plugin install replaces npx skills add. -->

> _[Changed 2026-04-03: Install via Claude Code plugin mechanism. Plugin install delivers all skills, hooks, scripts, and references. Impetus handles first-run setup for runtime state (journal, installed.json) and writes rules to ~/.claude/rules/ and .claude/rules/.]_

```bash
# Install Momentum plugin into Claude Code
claude plugin add momentum

# Primary entry point — session orientation, menu dispatch, first-run setup:
/momentum:impetus
```

Plugin install delivers all SKILL.md files (namespaced under `momentum:`), `hooks/hooks.json` (always-on hooks active immediately), `scripts/`, and `references/`. Rules cannot be written directly by the plugin install — Impetus writes rules to `~/.claude/rules/` and `.claude/rules/` on first `/momentum:impetus` invocation. No `momentum setup` command. No `momentum bootstrap` command.

Impetus handles install and upgrade via the manifest mechanism (Decision 5c). What triggers install vs. upgrade checks, and how the user experience unfolds, is defined in the UX specification — not here. The architectural guarantee: `/momentum:impetus` is the recommended interface; all setup and upgrade paths flow through it. Users can invoke individual skills directly (e.g., `/momentum:sprint-planning`) but skip session orientation when doing so.

### Plugin Manifest

Momentum is a Claude Code plugin. The plugin manifest lives at `.claude-plugin/plugin.json` in the plugin root:

```json
{
  "name": "momentum"
}
```

The `name` field determines the namespace prefix for all skills. With `"name": "momentum"`, a skill directory `skills/impetus/` becomes invocable as `/momentum:impetus`. Claude Code discovers the plugin through the `.claude-plugin/` directory and registers all skills, hooks, and scripts.

**Plugin root layout:**

| Directory | Purpose | Delivered by |
|---|---|---|
| `.claude-plugin/` | Plugin manifest | Plugin install |
| `skills/` | All SKILL.md files (flat + context:fork) | Plugin install |
| `hooks/` | Always-on hook definitions (`hooks.json`) | Plugin install |
| `scripts/` | CLI tools (`momentum-tools.py`) | Plugin install |
| `references/` | Rules, practice docs, version manifest | Plugin install |
| `agents/` | Custom agent definitions for teams | Plugin install |
| `mcp/` | Custom MCP server source (Epic 6) | Plugin install |

Hooks in `hooks/hooks.json` are active immediately after plugin install — no Impetus invocation required. Rules in `references/rules/` require Impetus to write them to `~/.claude/rules/` and `.claude/rules/` because the plugin cannot write outside its own directory.

### Agent Teams and Skill Loading

Sprint execution uses Claude Code Agent Teams. Teams share a working directory and execute stories sequentially with commit-as-sync-point — no worktree needed within a team.

**Skill loading model:** Teammates do NOT load skills from `.agent.md` `skills` frontmatter. Instead, teammates load skills from project and user settings (the standard Claude Code skill loading path). The dev agent receives workflow instructions through its spawn prompt, which includes the story file path and role-specific guidelines from the sprint record's team composition.

**Commit-as-sync-point:** Within a team, stories execute sequentially. Each story completes with a git commit before the next begins. The commit is the synchronization boundary — the next story sees the previous story's changes via the committed state of the working directory. This eliminates the need for worktrees within team execution while maintaining isolation between story implementations.

**Team composition:** Defined during sprint planning (`/momentum:sprint-planning`) and stored in the sprint record. Each story maps to one or more roles (Dev, QA, E2E Validator, Architect Guard). Each role carries project-specific guidelines. The sprint-dev skill (`/momentum:sprint-dev`) reads the team composition and spawns agents with the appropriate role, guidelines, and story assignment.

### Version Management

> _[Changed 2026-03-18: Removed plugin-skills sync requirement. Single version source covers all skills.]_

All skills share a single `version.md` at repo root. A standard git pre-commit hook (Husky/pre-commit framework — not a Claude Code hook) validates SKILL.md frontmatter consistency. Release tags version all skills together.

---

## Core Architectural Decisions

### Storage & State Architecture

**Decision 1a — Provenance Graph: Pure YAML Frontmatter**
- Each document carries its own `derives_from` in frontmatter (downstream-only authoring)
- `referenced_by` is computed on demand by a provenance scanner — never manually maintained
- Content hashes use git blob SHAs (`git hash-object <file>`) — zero extra tooling
- Staleness detection: compare stored hash in `derives_from` against current `git hash-object`
- One-hop propagation only; human/Impetus-gated at each level

**Decision 1b — Session Journal: JSONL with Markdown View**
- Location: `.claude/momentum/journal.jsonl`
- Format: JSONL — one JSON object per line, append-only. Each write appends a new state entry for a thread.
- Current state of a thread = last entry in the file with that `thread_id`
- Auto-generated `.claude/momentum/journal-view.md` for human readability (regenerated after every append)
- Tracks: active story, current phase, last completed action, open threads
- Rationale (concurrency safety): same argument as Decision 1c — multiple Claude Code sessions can safely append concurrently without file locking. POSIX atomic append for lines under pipe buffer size. JSON read-modify-write is racy under multi-tab access (lost writes, corruption on crash, torn reads).
- Rationale (query patterns): current-state reconstruction (read all lines, group by `thread_id`, take last entry) is a one-time cost at session start — not a hot path. `journal-view.md` provides the pre-built snapshot for human consumption.
- Rationale (implementation complexity): append-only is simpler than read-parse-modify-serialize-write. No file locking logic required in instruction-based workflows.
- Rationale (human readability): raw JSONL is less readable than JSON, but `journal-view.md` auto-generation already provides the human-readable layer.
- Evaluated in Story 1.9.

**Decision 1c — Findings Ledger: JSONL (Global)**
- Location: `~/.claude/momentum/findings-ledger.jsonl` (global, not per-project)
- Format: JSONL — one JSON object per line, append-only. No wrapping array.
- Structured findings with fields: `id` (globally unique, format `F-{unix_ms}-{random_4hex}`), `project` (string, project identifier), `story_ref`, `phase`, `severity`, `pattern_tags`, `description`, `evidence`, `provenance_status`, `upstream_fix_applied`, `upstream_fix_level`, `upstream_fix_ref` (reference to the fix artifact), `timestamp` (ISO 8601 when finding was recorded)
- `upstream_fix_level` — null until a fix is applied; then one of: `spec-generating-workflow | specification | rules-or-CLAUDE.md | tooling | one-off-code-fix`
- Queryable for cross-project and cross-story pattern detection
- JSONL enables concurrent append from multiple Claude Code sessions without file locking (POSIX atomic append for lines under pipe buffer size)
- Only flywheel workflow writes findings; read by Impetus at retrospective and upstream trace
- Rationale: Global scope enables cross-project pattern detection — the same anti-pattern appearing in projects A and B becomes visible. Per-project scope would miss these systemic patterns.

**Decision 1d — Installed State: JSON**
- Location: `.claude/momentum/installed.json`
- Written by Impetus on first install; updated on each upgrade
- Tracks: `momentum_version` at last install/upgrade, per-component version + hash
- Impetus reads this at session start to detect version drift (see Decision 5c for full schema)

---

### Security & Integrity

**Decision 2a — File Protection Targets (PreToolUse hook blocks)**

| Protected Path | Rationale |
|---|---|
| `tests/acceptance/` and `**/*.feature` | Acceptance tests are immutable — agents never modify to make code pass |
| `_bmad-output/planning-artifacts/*.md` | Spec authority — coding agents read, never write |
| `.claude/rules/` | Global enforcement rules — protected from coding agent modification |
| `~/.claude/momentum/findings-ledger.jsonl` | Ledger integrity — only flywheel workflow writes. Note: global path is outside project PreToolUse scope; protection enforced by authority rule. |

**Decision 2b — Provenance Integrity Rules (Tier 3, promotable to Tier 1)**
- Agents may not remove or modify `derives_from` frontmatter in spec files
- Every significant claim classified as SOURCED / DERIVED / ADDED / UNGROUNDED
- Violations tracked in findings ledger; repeated violations trigger hook promotion
- **Note:** `UNGROUNDED` here refers to content origin (no source was provided). This is distinct from FR16's epistemic trust vocabulary, which also uses `UNGROUNDED` to mean "based on training data with no grounding in provided sources." In implementation, use `content_origin` for Decision 2b values and `provenance_status` for FR16 values to avoid field-name collision.

---

### Agent Communication & Orchestration

**Decision 3a — VFL Parallel Execution: Main Context Orchestration**

The main conversation CAN spawn multiple subagents simultaneously (confirmed: official Claude Code docs explicitly document parallel subagent spawning as a supported pattern). The constraint is only that subagents cannot spawn further subagents.

Architecture:
- **AVFL runs as a flat skill** (main context, not context:fork) — orchestration needs main context to spawn agents
- **Impetus invokes AVFL** from main conversation
- **AVFL uses its own nested sub-skills** for multi-lens artifact validation — these are DISTINCT from `/momentum:code-reviewer`. Sub-skills are nested inside `skills/avfl/sub-skills/` and deploy automatically with the parent skill. The sub-skill pipeline was developed through 6-phase research (36 runs across 3 models x 3 effort levels) with benchmarked optimal model/effort configurations per role:
  - **validator-enum** (Enumerator) — sonnet/medium: systematic dimension-by-dimension enumeration
  - **validator-adv** (Adversary) — opus/high: failure-focused adversarial validation
  - **consolidator** — haiku/low: deduplication, cross-check confidence tagging, scoring (fully invariant across models — cheapest sufficient)
  - **fixer** — sonnet/medium: targeted artifact repair based on consolidated findings
- **Consolidation and fixing run as sub-skill agents** (not in AVFL main context) because they need specific model routing: haiku for consolidator, sonnet for fixer
- **`/momentum:code-reviewer`** (Epic 4 Story 4.1) is a separate skill for adversarial code review of implementation artifacts — it is NOT used by AVFL. AVFL sub-skills are for multi-lens artifact validation with specific model routing per role.
- **AVFL spawns validators in parallel** — up to 8 simultaneous subagents for Full profile (2 per lens x 4 lenses)
- **AVFL consolidates results** via the consolidator sub-skill after all validators complete
- Context window consideration: all validator results return to main context; keep validator output structured and bounded
- **Execution mode:** validator subagents run as **background agents** (non-blocking — main conversation continues); automated hook-triggered passes may use foreground (blocking) where dead air is acceptable. Background execution is what enables productive waiting (Decision 4c).
- **Validator output bound:** Validators return structured JSON (not free-form prose). AVFL framework (framework.json) specifies per-validator output schema. Impetus enforces this to keep context accumulation bounded across all validator results.
- **Implementation note:** Background agent execution model is validated in Story 2.Spike (Epic 2) before Stories 2.4 and 4.3 begin. Do not implement productive waiting or background AVFL execution until spike result is documented. The execution mode is adopted as the architectural intent; the spike validates the specific implementation mechanism (inter-agent communication + checkpoint/resume). If the spike reveals the mechanism is unavailable, Decision 3a/4c will be revised before Stories 2.4 and 4.3 begin.

**context:fork agent count — explicit model:**

> _[Added 2026-03-18: Clarifying how multiple agents are actually created. `context: fork` = one agent per invocation.]_

`context: fork` creates **exactly one** isolated subagent per invocation. Multiple parallel agents = multiple Agent tool calls. AVFL's parallel execution works as follows:

- AVFL (flat skill, main context) issues **N separate Agent tool calls**, each with `run_in_background: true`
- Each call spawns one isolated subagent running an AVFL sub-skill (validator-enum or validator-adv) with lens criteria passed via `$ARGUMENTS`
- **Full profile agent count:** 8 Agent tool calls = 8 concurrent validator agents (2 per lens x 4 lenses: Structural Integrity, Factual Accuracy, Coherence & Craft, Domain Fitness) — one enumerator + one adversary per lens
- **Checkpoint profile:** 2–4 Agent tool calls (1–2 lenses, 1 validator each)
- **Gate profile:** 1 Agent tool call
- After validators complete: 1 consolidator sub-skill call (haiku/low), then 0–4 fixer sub-skill calls (sonnet/medium) depending on findings

architecture-guard is a **separate** skill, invoked independently by Impetus (not inside AVFL). It is one additional Agent tool call when pattern drift checking is needed — not part of the AVFL validator count.

`/momentum:code-reviewer` is also a **separate** skill (Epic 4 Story 4.1), invoked independently for adversarial code review of implementation artifacts — not part of the AVFL pipeline.

Invocation flow for Full AVFL:
```
AVFL (flat, main context)
├── Agent tool call 1 → validator-enum [structural] (background)
├── Agent tool call 2 → validator-adv [structural] (background)
├── Agent tool call 3 → validator-enum [factual] (background)
├── Agent tool call 4 → validator-adv [factual] (background)
├── Agent tool call 5 → validator-enum [coherence] (background)
├── Agent tool call 6 → validator-adv [coherence] (background)
├── Agent tool call 7 → validator-enum [domain] (background)
└── Agent tool call 8 → validator-adv [domain] (background)
     ↓ (all complete)
├── Agent tool call 9 → consolidator (deduplicate, cross-check, score)
     ↓ (consolidated findings)
└── Agent tool call 10..N → fixer (targeted repairs, up to 4 iterations)
     ↓ (all complete)
AVFL returns validated artifact + findings report → Impetus
```

**AVFL Deployment Note:**

The benchmarked AVFL pipeline (developed via 6-phase research in `avfl-workspace/`) is deployed as `/momentum:avfl` with 4 production sub-skills at their benchmarked optimal model/effort configurations. The `avfl-*` skills that remain in `.claude/skills/` are research/benchmarking tools (gitignored, not deployed with Momentum). The 13 benchmark variants (2lens, 3lens, declining, composition variants, effort variants) are not deployed — only the 4 production sub-skills: validator-enum (sonnet/medium), validator-adv (opus/high), consolidator (haiku/low), and fixer (sonnet/medium).

**Decision 3b — Hub-and-Spoke Voice Contract**
Impetus is the only agent that speaks to the user. All subagents return:
```json
{ "status": "complete | needs_input | blocked", "result": {}, "question": "optional" }
```
Impetus synthesizes into its own voice. Subagent identity never surfaces to user.

Confidence weighting: low-confidence results surface as questions to the user rather than assertions; medium-confidence results are flagged explicitly; high-confidence results are synthesized directly. Exact weighting logic is an implementation-time decision for Impetus.

**Decision 3c — MCP Servers**

| Server | Phase | Purpose |
|---|---|---|
| ~~`@modelcontextprotocol/server-git`~~ | ~~MVP~~ | ~~File history, blame, diff for provenance tracking~~ — **Removed (p1.1):** Zero value over git CLI; provenance design (Decision 1a) already uses `git hash-object` via Bash with "zero extra tooling." Consumed a tool-ceiling slot and added an npx dependency for no functional benefit. |
| Momentum findings MCP (lightweight, custom) | Deferred (Epic 6) | Optional query/filter interface over `~/.claude/momentum/findings-ledger.jsonl`. Not a concurrency solution — MCP is per-session (each Claude Code instance launches its own), so multiple instances cannot serialize writes. Primary write path is direct JSONL append by the flywheel. MCP provides structured query (filter by project, pattern_tag, severity, date range) for pattern detection. |
| `@rlabs-inc/gemini-mcp` | Growth | Multi-model deep research |
| GPT deep research MCP | Growth | Cross-model verification |

**Decision 3d — Orchestrator Purity Principle**

> _[Added 2026-03-22: Formalizes what Decisions 3a, 3b, and Subsystem 5 (Subagent Composition) imply but never explicitly constrain.]_

Impetus (`/momentum:impetus`) is a **pure orchestrator** and the recommended entry point for all Momentum operations. Users can invoke other namespaced skills directly (e.g., `/momentum:sprint-planning`, `/momentum:avfl`) but skip session orientation when doing so. Impetus MUST NOT perform development, evaluation, testing, or validation itself.

**Prohibited roles for Impetus — explicitly:**
- Code writing (any file creation or modification that constitutes implementation)
- Test execution (running test suites, evaluating test outcomes)
- Eval running (executing or judging evals for any skill)
- Code review (adversarial inspection of implementation artifacts)
- Findings generation (producing quality findings about implementation output)

**Delegation rule:**
All non-orchestration work is dispatched to purpose-specific subagents:
- Implementation → `bmad-dev-story` (dispatched per story, returns structured completion signal)
- Quality validation → `/momentum:avfl` (dispatched with artifact + source material, returns pass/fail signal)
- Code review → `/momentum:code-reviewer` (context:fork subagent, returns findings JSON)
- Architecture drift → `/momentum:architecture-guard` (context:fork subagent, returns drift report JSON)

Impetus's role is to **dispatch, synthesize, and advance** — never to produce.

**Rationale:** Purity is what makes the orchestrator trustworthy as a synthesis layer. If Impetus both produces and synthesizes output, the producer-verifier isolation (established in subagent composition) breaks down. Impetus must remain a clean conduit: it routes work to producers, receives structured results, and presents synthesized output in its own voice (Decision 3b).

**Traceability:** Formalization of the producer-verifier separation implicit in Decision 3a (VFL orchestration), Decision 3b (hub-and-spoke voice contract), and Subsystem 5 (Subagent Composition). Triggered by Epic 1 retrospective Action Item #7 (`_bmad-output/implementation-artifacts/epic-1-retro-2026-03-22.md`).

---

**context:fork evaluation for `bmad-dev-story` invocation:**

_The question:_ Should Impetus invoke `bmad-dev-story` using `context:fork` isolation?

**Arguments for context:fork:**
- Isolation prevents dev agent's implementation details from accumulating in orchestrator context
- Consistent with code-reviewer / architecture-guard pattern (both use context:fork for producer-verifier separation)
- Long dev-story sessions produce many file changes — isolation limits context contamination risk

**Arguments against context:fork:**
- While context:fork and productive waiting are orthogonal (resolved in A-1), the specific checkpoint/resume communication mechanism needed for mid-story progress updates during long dev sessions has not been confirmed as available in a forked context — the productive waiting spike (Decision 3a implementation note) must validate this before relying on it
- Context handoff requires file-based parameter passing (story file path) — already the convention, so no additional overhead
- Orchestrator purity does not require context isolation — it requires role separation. Impetus maintaining purity while in the same context is a behavioral commitment, not a structural one; Impetus achieves purity by dispatching and doing nothing else during the dev session

**Recommendation: flat skill invocation (no context:fork) for `bmad-dev-story`**

Rationale: productive waiting (Decision 4c) is a first-class UX requirement that depends on Impetus maintaining an active dialogue channel. Context:fork would make Impetus go silent during the longest and most attention-demanding phase of the practice cycle. The orchestrator purity constraint is satisfied behaviorally: Impetus dispatches the story file path, receives the structured completion signal, and takes no other action — it does not write code, run tests, or generate findings during the session. Purity via behavioral discipline, not structural isolation.

If the productive waiting spike (Decision 3a implementation note) reveals that background agent communication requires context:fork, this recommendation will be revised before Stories 2.4 and 4.3 begin.

---

**Verification artifact exclusion convention:**

Acceptance test and eval files must be excluded from the dev agent's implementation context. The convention:

- **Storage locations:**
  - Skill evals: `skills/[skill-name]/evals/` (each skill carries its own eval suite)
  - Project-level acceptance tests: `tests/acceptance/` (top-level, cross-skill behavioral tests)

- **Exclusion mechanism:** Explicit instruction in the `bmad-dev-story` workflow — the dev agent MUST NOT read or modify files in `evals/` directories or `tests/acceptance/` during implementation. This is a workflow directive, not a file protection hook (file protection hooks are Story 3.2, FR19/FR21). The workflow directive establishes the convention now; hooks will provide deterministic enforcement once Story 3.2 is implemented.

- **Consistency with existing pattern:** PreToolUse file protection (Decision 2a, FR19/FR21) will block dev agent writes to acceptance test directories once Story 3.2 is implemented. This convention predates that enforcement and establishes the same boundary as intent.

---

### Workflow & UX Architecture

**Decision 4a — Visual Progress Format (non-negotiable)**
```
✓ Built: [accumulated value]
→ Now:   [this step and why it matters]
◦ Next:  [what follows]
```
Never `Step N/M`. Always narrative. Every phase transition in every Impetus-orchestrated workflow.

**Decision 4b — Session Orientation Contract**
At every session start via `/momentum:impetus`, Impetus reads the session journal and within two exchanges surfaces:
active story/task, current phase, last completed action, suggested next action.
User never hunts for context. Direct skill invocation (e.g., `/momentum:sprint-planning`) skips session orientation — the user's choice.

**Session open sequence (updated 2026-04-03):** At session start, Impetus reads `stories/index.json` and `sprints/index.json` and renders sprint progress (done/current/next) before presenting the primary menu. The primary menu offers sprint-oriented actions: "Plan a sprint" (invokes `/momentum:sprint-planning`), "Continue sprint" (invokes `/momentum:sprint-dev`), and standalone story operations. Session-stats write is deferred until after the menu is displayed — startup rendering does not block on writes.

**Decision 4c — Productive Waiting**
While a context:fork subagent runs, Impetus maintains engagement through pre-launch briefing and post-completion synthesis.
`context:fork` subagents run to completion in a foreground operation — the main conversation is blocked during execution. Background execution via `run_in_background: true` on the Bash tool is available for mechanical tasks (test runs, builds) but not for agent reasoning.
Default: surface implementation summary ("here's what was built and how it maps to the ACs").
Dead air is a failure mode, not an acceptable pause.
**Implementation note (updated 2026-03-24, Story 2.10 spike result):** The spike is complete. Results documented in `docs/research/background-agent-coordination.md`. Key findings: (1) No `SendMessage` or inter-agent messaging API exists in Claude Code — checkpoint/resume mid-task is not possible. (2) No `Agent` tool exists as a general-purpose callable tool — subagent execution is declared via `context:fork` in SKILL.md, not dispatched dynamically. (3) `run_in_background: true` on the Bash tool runs shell commands (not agents) in the background — fire-and-forget only. (4) Productive waiting is behavioral, not mechanical: Impetus briefs the user before subagent launch and synthesizes results after completion. Story 4.3 should decompose work into discrete `context:fork` invocations (each runs to completion) and use background Bash for test/build tasks only.

**Rolling pool feasibility note (2026-03-26):** Story 2.10's spike was conducted in a bare Claude Code CLI session where the Agent tool was not available. In a skill execution context (where /develop-epic runs), the Agent tool with `run_in_background: true` and the notification model are available. Rolling pool dispatch (dispatch when a slot frees, not wait-for-all) is therefore architecturally feasible. Tier-sequential batching is the MVP implementation choice for simplicity and correctness — not an architectural constraint. Rolling dispatch is a valid follow-on enhancement.

---

### Packaging & Deployment

**Decision 5a — Global Rules Deployment: Bundled in Plugin, Written by Impetus**
<!-- REVISED 2026-04-03: Plugin bundles rules in references/rules/. Impetus writes them to target locations. -->

> _[Changed 2026-04-03: Rules bundled at plugin root in `references/rules/`. Plugin install cannot write to `~/.claude/rules/` or `.claude/rules/` directly — Impetus writes them on first run.]_

The plugin install mechanism delivers rules to `references/rules/` at the plugin root but cannot write to `~/.claude/rules/` or `.claude/rules/` directly. Resolution: Impetus writes rules to the appropriate targets using the Write tool on first invocation:

- `~/.claude/rules/` — global rules (all projects for this user)
- `.claude/rules/` — project-scoped rules (this project only)

This happens on first invocation and on upgrade — governed by the manifest/installed state mechanism defined in Decision 5c. No separate CLI, no separate command. The UX interaction pattern (when to prompt, what to show) is defined in the UX specification.

Update mechanism: Impetus compares the hash of installed global rules against the bundled rules in `references/rules/` using git blob SHA — zero extra tooling. See Decision 5c for the full version tracking schema.

**Decision 5b — BMAD Enhancement Touch Points (MVP)**
Impetus proactively enhances BMAD workflow boundaries. Each touchpoint is classified: **Gate** (blocks progress) or **Proposal** (user-discretionary).

| BMAD Event | Momentum Enhancement | Type |
|---|---|---|
| Any BMAD artifact generated (user selects C) | Impetus proposes `derives_from` frontmatter + git commit | Proposal |
| BMAD code-review complete | Impetus offers Momentum code-reviewer as additional adversarial pass | Proposal |
| BMAD dev-story complete | Impetus gates on acceptance tests passing before closing story | **Gate** |
| BMAD retrospective | Impetus adds findings ledger summary to retrospective input | Proposal |

The dev-story acceptance test gate is the only hard gate at MVP — quality guarantee without friction. All other touchpoints are proposals; the developer retains discretion. This boundary may shift based on flywheel findings.

Long-term: evaluate all BMAD workflows and agents for Momentum enhancement opportunities.
Goal is that running any BMAD workflow inside Momentum automatically inherits provenance,
enforcement, flywheel, and versioning without workflow authors needing to explicitly add it.

**Decision 5c — Installation & Upgrade Manifest**

> _[Added 2026-03-18: Defines the data structures that drive install, upgrade, and version drift detection. The UX interaction for these operations (when to prompt, how to present, what to show) is defined in the UX specification — not here.]_
>
> _[Revised 2026-03-23: Split version tracking into global (per-machine) and project (per-repo) state files. Replaced monolithic action types with `add`/`replace`/`delete`/`migration`. Added per-component-group versioning to support partial upgrades.]_

Three files govern Momentum's install and upgrade lifecycle:

**File 1: `references/momentum-versions.json`** (at plugin root) — bundled with the plugin; the authoritative per-version action list. Each version entry contains instructions that tell Impetus exactly what to do. Each action declares a `group` (component group name) and `scope` (`global` or `project`):

```json
{
  "current_version": "1.0.0",
  "versions": {
    "1.0.0": {
      "description": "Initial release — repository structure established",
      "actions": [
        { "action": "add", "group": "rules", "scope": "global",
          "source": "rules/authority-hierarchy.md",
          "target": "~/.claude/rules/authority-hierarchy.md" },
        { "action": "add", "group": "rules", "scope": "global",
          "source": "rules/anti-patterns.md",
          "target": "~/.claude/rules/anti-patterns.md" },
        { "action": "add", "group": "rules", "scope": "global",
          "source": "rules/model-routing.md",
          "target": "~/.claude/rules/model-routing.md" },
        { "action": "migration", "group": "hooks", "scope": "project",
          "source": "migrations/1.0.0-hooks-install.md",
          "description": "Merge enforcement hooks into .claude/settings.json",
          "requires_restart": true }
      ]
    },
    "1.1.0": {
      "description": "Revised authority rules, new git-discipline rule",
      "from": "1.0.0",
      "actions": [
        { "action": "replace", "group": "rules", "scope": "global",
          "source": "rules/authority-hierarchy.md",
          "target": "~/.claude/rules/authority-hierarchy.md" },
        { "action": "add", "group": "rules", "scope": "global",
          "source": "rules/git-discipline.md",
          "target": "~/.claude/rules/git-discipline.md" },
        { "action": "migration", "group": "hooks", "scope": "project",
          "source": "migrations/1.1.0-hooks-update.md",
          "description": "Add new PostToolUse hook",
          "requires_restart": true }
      ]
    }
  }
}
```

**Action types:**

| Type | Behavior | Use when |
|---|---|---|
| `add` | Write source file to target path. Create parent dirs if needed. Warn if target exists. | New file — a new rule, config, template |
| `replace` | Overwrite target path with source file content. | Updated content for an existing file |
| `delete` | Remove file at target path. | Deprecated file — consolidated rule, removed config |
| `migration` | Read the instruction file at `source` (relative to plugin root `references/`), follow its natural language instructions. May reference bundled data files. | Config merging, multi-file restructuring, template migrations — anything beyond single-file ops |

Migration instruction files live in `references/migrations/` (at plugin root) and contain natural language instructions Impetus follows. They can express arbitrarily complex operations while keeping the manifest itself simple.

**File 2: `~/.claude/momentum/global-installed.json`** — per-machine state file; tracks what version of global-scoped components (e.g., rules in `~/.claude/rules/`) have been applied on this machine. Never shipped in the package, never committed to any project. Created silently on first install; updated when user consents to upgrade:

```json
{
  "installed_at": "2026-03-22T14:30:00Z",
  "components": {
    "rules": { "version": "1.0.0", "hash": "<git-blob-sha>" }
  }
}
```

**File 3: `.claude/momentum/installed.json`** — per-project state file; tracks what version of project-scoped components (e.g., project rules in `.claude/rules/`) have been applied to THIS project. Committed to git so team members can detect that project-level setup is done:

```json
{
  "installed_at": "2026-03-22T14:30:00Z",
  "components": {
    "hooks": { "version": "1.0.0" }
  }
}
```

Both state files use per-component-group versioning — no top-level `momentum_version`. Each group tracks its own version independently, enabling partial upgrades when a developer requests them.

**Mechanisms:**
- **First install** — neither state file exists; Impetus reads `versions["1.0.0"].actions`, executes all, writes both state files
- **New project on existing machine** — `global-installed.json` exists and is current; project `installed.json` absent. Impetus skips global actions, runs only project-scoped actions, writes project state file
- **Session-start check** — Impetus reads `current_version` from `momentum-versions.json`; for each component group, compares group's installed version (from the appropriate state file) against `current_version`; only stale groups are offered for upgrade
- **Upgrade** — Impetus reads the action list for each version between installed and current; presents to user with description + action per step; executes on confirmation; updates the appropriate state file per group
- **Partial upgrade** — If the developer requests specific groups only (via natural language), Impetus applies only those groups and records per-group versions accordingly. The default UX offers all-or-nothing; partial is developer-initiated.
- **Multi-version gaps** — actions applied sequentially (1.0.0 → 1.1.0 → 1.2.0); each version's changes presented and confirmed as a group
- **Hash comparison** — per-component git blob SHA in `global-installed.json` detects manual drift (user edited an installed file); surfaced as a warning, not a blocker
- **Team member joining** — `global-installed.json` absent on new machine but project `installed.json` committed in repo → Impetus runs only global setup

The UX interaction for install and upgrade — when to prompt, how to present each action, how to handle restarts and partial failures — is defined in the UX specification (Journeys 0 and 4).

---

## Implementation Patterns & Consistency Rules

### Potential Conflict Points

10 areas where different AI agents could make incompatible choices when implementing Momentum:

1. SKILL.md frontmatter fields (required vs. optional, values)
2. Agent definition structure and tool restriction format
3. `derives_from` frontmatter format and relationship vocabulary
4. Findings JSON schema field names and value enumerations
5. Visual progress format (the ✓/→/◦ pattern)
6. Subagent structured output contract
7. Hook announcement output format
8. Skill naming conventions
9. Commit message format and trigger timing
10. VFL profile selection criteria

---

### Naming Patterns

**Plugin-namespaced skills:**
```
momentum:impetus            ← Primary entry point (/momentum:impetus)
momentum:[concept]          e.g. momentum:avfl, momentum:upstream-fix, momentum:status
momentum:[verb]-[noun]      e.g. momentum:create-story, momentum:sprint-planning
```
Skills use short names (impetus, avfl, dev, sprint-planning) under the `momentum:` namespace. Directory names under `skills/` match the short name. BMAD skills retain their existing names — no renaming.

**context:fork skills (verifier/enforcer subagents):**
```
momentum:[role]             e.g. momentum:code-reviewer, momentum:architecture-guard
```
Same namespace as flat skills — distinguished by `context: fork` in SKILL.md frontmatter, not by naming convention.

> _[Changed 2026-04-03: Plugin namespace convention replaces `momentum-` prefix convention. Skills use short names under `momentum:` namespace.]_

**Rules files:**
```
[concept].md                e.g. authority-hierarchy.md, anti-patterns.md, model-routing.md
```

**Hook event names:** Use standard Claude Code lifecycle events verbatim:
`PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `UserPromptSubmit`

**Findings pattern tags:** kebab-case noun phrases:
`direct-db-access`, `missing-provenance`, `test-modification`, `pattern-drift`, `cognitive-debt`

---

### Structural Patterns

**Every SKILL.md MUST have this frontmatter (no exceptions):**
```yaml
---
name: [short-name]
description: "[One sentence. Action verb. What it does and when to use it.]"
model: claude-sonnet-4-6        # or claude-opus-4-6 for high-stakes outputs
effort: normal                  # normal | high | low
---
```
The `name` field uses the short name (e.g., `impetus`, `avfl`, `sprint-planning`). The plugin namespace `momentum:` is applied automatically by the plugin manifest — it does not appear in the SKILL.md `name` field.

**Enforcement skills (context:fork) add:**
```yaml
context: fork
disable-model-invocation: true  # prevent accidental auto-trigger of heavy skills
```

**Skills with heavy reference content use `references/` subdirectory:**
```
skills/impetus/
├── SKILL.md              ← Instructions + frontmatter (under 500 lines)
└── references/           ← Skill-specific references (loaded on demand)
```
Plugin-level references (rules, practice docs, version manifest) live in `references/` at the plugin root, not inside individual skill directories.

**context:fork skills (verifier/enforcer subagents) MUST include:**

> _[Changed 2026-04-03: Updated to plugin namespace model. Short names in frontmatter; plugin applies `momentum:` prefix.]_

```yaml
---
name: [role]
description: "[What this skill does and when Impetus invokes it — under 150 chars]"
model: claude-opus-4-6          # verifiers get flagship — cognitive hazard rule
context: fork                   # isolated subagent context — no conversation history
allowed-tools: Read             # code-reviewer and architecture-guard: Read only — never Edit, Write, Bash
disable-model-invocation: true  # prevents nested model calls from context:fork peer skills
---
```

**Workflow step files (micro-file architecture for multi-step skills):**
```
skills/[workflow]/
├── SKILL.md
└── steps/
    ├── step-01-[name].md       ← Each step self-contained with embedded rules
    ├── step-02-[name].md
    └── step-N-complete.md      ← Always a completion step
```

---

### Format Patterns

**derives_from frontmatter (ALL spec-generating artifacts):**
```yaml
derives_from:
  - id: UNIQUE-DOC-ID-001       # SCREAMING-KEBAB-CASE, unique across project
    path: relative/path/to/source.md
    relationship: derives_from  # or: depends_on, satisfies
    description: "One sentence: what this source contributed"
    hash: ""                    # filled by provenance scanner on first check
```

**Provenance status vocabulary (5 values, no others):**

| Status | Meaning | When to use |
|---|---|---|
| `VERIFIED` | Source exists, claim is accurate | High trust — cite without caveat |
| `CITED` | Source URL provided, accessible on research date | Moderate trust |
| `INFERRED` | Derived through reasoning from verified sources | Lower trust — note the inference |
| `UNGROUNDED` | No source; based on training data | Low trust — must verify before spec |
| `SUSPECT` | Was VERIFIED/CITED but upstream source has since changed | Re-verify required |

**Visual progress (every phase transition, no exceptions):**
```
✓ Built: [what exists now — value accumulated, not tasks completed]
→ Now:   [this step and why it matters to the work]
◦ Next:  [what follows after this step]
```
Never: "Step 3/8", "Continuing...", "Moving on to...", "Great work!"

**Hook announcement output (every hook, every fire):**
```
[hook-name] ✓ checked [what was checked] — [one-line result]
```
On failure:
```
[hook-name] ✗ [specific issue] — [exact file/line if applicable]
```
Silent hooks build no trust. Verbose hooks create noise. One line, always. (Exception: high-frequency guard hooks — e.g., PreToolUse file-protection — suppress pass-through output for non-blocked events. The 'never silent' principle applies to meaningful events such as blocks, not to routine allow decisions.)

**Subagent structured output contract (all agents returning to Impetus):**
```json
{
  "status": "complete",          // complete | needs_input | blocked
  "result": { ... },             // domain-specific structured result
  "question": null,              // non-null if status=needs_input; Impetus decides whether to ask user
  "confidence": "high"           // high | medium | low — Impetus weights synthesis accordingly
}
```
Agents NEVER address the user directly. All output goes through Impetus.

**Findings schema (findings-ledger.jsonl entries — one per line):**
```json
{
  "id": "F-1711929600000-a3f2",   // F-{unix_ms}-{random_4hex}
  "project": "momentum",          // project identifier
  "story_ref": "S-04",
  "phase": "code-review",         // spec | atdd | implement | code-review | flywheel
  "severity": "critical",         // critical | high | medium | low
  "pattern_tags": ["direct-db-access"],
  "description": "One sentence describing the finding",
  "evidence": "Exact quote or file:line reference",
  "provenance_status": "VERIFIED",
  "upstream_fix_applied": false,
  "upstream_fix_level": null,     // null until fix applied; then: spec-generating-workflow | specification | rules-or-CLAUDE.md | tooling | one-off-code-fix
  "upstream_fix_ref": null,       // ID of the fix story/rule if applied
  "timestamp": "2026-03-17T00:00:00Z"
}
```

---

### Communication Patterns

**Impetus voice register:** Guide's voice. Oriented, substantive, forward-moving.
- Synthesizes before delivering: reads subagent output, forms a view, delivers as Impetus
- Acknowledges uncertainty honestly: "I'm not certain — here's what I know and where the gap is"
- Returns agency explicitly at completion: "That's done — here's what was produced. What's next?"
- Never: generic praise ("Great!"), numeric progress ("Step 3/8"), visible agent machinery

**Error and blocker communication:**
```
⚠ [what was attempted] — [what went wrong in one sentence]
  Action: [what to do next]
```

**Proactive gap detection (only when conversational floor is open):**
```
I notice [observation]. Before [next action], do you want [suggested step]?
```
Never interrupt mid-task. Surface gaps at natural handoffs.

---

### Process Patterns

**Commit trigger points (per git-discipline.md — every logical unit of work):**
- Any SKILL.md created or substantially modified
- Any agent definition created or modified
- Any rule file created or modified
- Any workflow step file created
- Any spec artifact (PRD, architecture, story) created or substantially modified
- VFL validation complete (commit the validated artifact)
- Flywheel fix applied (commit the rule/workflow change)

**VFL profile selection criteria:**

| Situation | Profile |
|---|---|
| Input validation (is source material present and complete?) | Gate |
| After first interpretation step | Checkpoint |
| Before irreversible decisions | Checkpoint |
| Final deliverable artifacts (PRD, architecture, stories) | Full |
| Penultimate step in any workflow | Checkpoint |
| Ad-hoc quality check on any artifact | Full |

**Upstream fix process (always this order, never skip steps):**
`Detection → Review → Upstream Trace → Solution → Verify → Log`
Finding logged to findings ledger at Detection. Fix logged at Log (sixth phase). Never patch code without tracing first.

**SKILL.md description budget rule:**
Descriptions are loaded at startup for ALL installed skills. Keep under 150 characters.
Heavy content goes in `references/` — loaded only on invocation.
Bad: `"A comprehensive workflow that orchestrates the full validate-fix-loop process including dual-reviewer patterns across four validation lenses with configurable profiles"`
Good: `"Run validate-fix-loop validation on an artifact. Profiles: gate/checkpoint/full."`

---

### Enforcement Guidelines

**All AI agents implementing Momentum MUST:**
- Include `model:` and `effort:` frontmatter on every SKILL.md and agent definition
- Use `derives_from` frontmatter on every spec-generating artifact
- Follow the visual progress format exactly (✓/→/◦) — no numeric steps
- Return structured JSON from all subagents (never free-form text to Impetus)
- Use the findings schema exactly — no ad-hoc fields
- Follow the commit trigger points — no end-of-session batching
- Keep SKILL.md descriptions under 150 characters

**Pattern enforcement levels** (distinct from NFR7's portability Tier 1/2/3 taxonomy):
- Enforcement Level A: SKILL.md frontmatter validated by pre-commit hook (Husky/pre-commit framework)
- Enforcement Level B: VFL Structural Integrity lens checks format compliance on generated artifacts
- Enforcement Level C: These patterns loaded as rules in every agent session via `.claude/rules/`

---

## Project Structure & Boundaries

### Repository Structure
<!-- REVISED 2026-04-03: Plugin root layout with .claude-plugin/plugin.json, namespaced skills, hooks/hooks.json. -->

> _[Changed 2026-04-03: Adopted Claude Code plugin structure. `.claude-plugin/plugin.json` manifest. Skills use short names under `momentum:` namespace. Hooks delivered via `hooks/hooks.json`. References (rules, practice docs, version manifest) at plugin root.]_

```
momentum/                                    ← Plugin root
├── .claude-plugin/
│   └── plugin.json                          ← { "name": "momentum" }
├── README.md
├── LICENSE
├── CLAUDE.md
├── version.md                               ← Single version source for all skills
│
├── skills/                                  ← All skills: flat + context:fork
│   ├── impetus/                             ← Orchestrator (/momentum:impetus)
│   │   ├── SKILL.md
│   │   └── workflow.md                      ← Session workflow (menu, dispatch)
│   ├── sprint-planning/                     ← /momentum:sprint-planning (was workflows/sprint-planning.md)
│   │   └── SKILL.md                         ← Inline skill (no context:fork), creates team
│   ├── dev/                                 ← /momentum:dev (was skills/momentum-dev/)
│   │   └── SKILL.md                         ← Referenced in team spawn prompts
│   ├── sprint-dev/                          ← /momentum:sprint-dev (was workflows/sprint-dev.md)
│   │   └── SKILL.md
│   ├── avfl/                                ← /momentum:avfl
│   │   ├── SKILL.md                         ← Validate-fix-loop orchestrator (flat skill)
│   │   ├── references/
│   │   │   └── framework.json               ← 15-dimension taxonomy, prompt templates, scoring
│   │   └── sub-skills/                      ← Nested internal sub-skills (deploy with parent)
│   │       ├── validator-enum/SKILL.md      ← Enumerator (sonnet/medium)
│   │       ├── validator-adv/SKILL.md       ← Adversary (opus/high)
│   │       ├── consolidator/SKILL.md        ← Consolidator (haiku/low)
│   │       └── fixer/SKILL.md               ← Fixer (sonnet/medium)
│   ├── code-reviewer/                       ← /momentum:code-reviewer
│   │   └── SKILL.md                         ← context:fork, allowed-tools: Read — pure verifier
│   ├── architecture-guard/                  ← /momentum:architecture-guard
│   │   └── SKILL.md                         ← context:fork, allowed-tools: Read — pattern drift detector
│   ├── upstream-fix/                        ← /momentum:upstream-fix
│   │   ├── SKILL.md
│   │   └── steps/
│   │       ├── step-01-detect.md
│   │       ├── step-02-trace.md
│   │       ├── step-03-solution.md
│   │       └── step-04-verify.md
│   ├── create-story/                        ← /momentum:create-story
│   │   └── SKILL.md
│   ├── plan-audit/                          ← /momentum:plan-audit
│   │   └── SKILL.md
│   ├── status/                              ← /momentum:status
│   │   └── SKILL.md
│   └── retro/                               ← /momentum:retro
│       └── SKILL.md
│
├── agents/                                  ← Custom agent definitions for teams
│
├── hooks/
│   └── hooks.json                           ← Always-on hooks (Tier 1 enforcement; delivered by plugin)
│
├── scripts/
│   └── momentum-tools.py                    ← CLI tool: sprint, version, log subcommands
│
├── references/                              ← Plugin-level references
│   ├── rules/                               ← Bundled rules (written to ~/.claude/rules/ by Impetus)
│   │   ├── authority-hierarchy.md
│   │   ├── anti-patterns.md
│   │   └── model-routing.md
│   ├── practice-overview.md
│   ├── phase-guide.md
│   └── momentum-versions.json               ← Per-version action list (install + upgrade instructions)
│
├── mcp/                                     ← Custom MCP server source
│   └── findings-server/                     ← Lightweight findings-ledger MCP server
│
├── docs/                                    ← Project documentation
│   ├── research/                            ← Research documents
│   ├── planning-artifacts/                  ← Older plan (superseded by _bmad-output)
│   ├── process/                             ← Process backlog
│   └── implementation-artifacts/            ← Tech specs, handoffs
│
├── _bmad-output/                            ← BMAD workflow output
│   └── planning-artifacts/
│       ├── prd.md
│       ├── ux-design-specification.md
│       └── architecture.md                  ← This document
│
├── _bmad/                                   ← BMAD framework (managed by BMAD)
│
└── .claude/                                 ← Claude Code project config (committed to repo)
    ├── rules/                               ← Project-scoped rules (committed; written by Impetus)
    └── skills/                              ← BMAD skills (managed by BMAD installer)
```

---

### Installed Structure (after plugin install + first `/momentum:impetus` invocation)
<!-- REVISED 2026-04-03: Plugin install delivers skills, hooks, scripts, references. Impetus writes rules and creates runtime state. -->

> _[Changed 2026-04-03: Plugin install replaces `npx skills add`. Skills delivered as namespaced plugin skills. Always-on hooks delivered via `hooks/hooks.json` at plugin root (not Impetus-written to settings.json). Rules still written by Impetus on first run.]_

**Delivered by plugin install:**
- All `skills/*/SKILL.md` files — available as `/momentum:*` commands
- `hooks/hooks.json` — always-on hooks active immediately
- `scripts/momentum-tools.py` — CLI tool
- `references/` — rules, practice docs, version manifest

**Written by Impetus on first `/momentum:impetus` invocation:**

```
~/.claude/                                   ← Global Claude Code config
├── rules/
│   ├── authority-hierarchy.md               ← Written by Impetus (from plugin references/rules/)
│   ├── anti-patterns.md
│   └── model-routing.md
└── momentum/
    ├── findings-ledger.jsonl               ← Quality findings (global, flywheel writes, JSONL append-only)
    └── global-installed.json               ← Per-machine install state

[project-root]/
└── .claude/
    ├── rules/                               ← Written by Impetus (from plugin references/rules/)
    └── momentum/                            ← Per-project Momentum state
        ├── journal.jsonl                     ← Session journal (JSONL append-only, Impetus reads/writes)
        ├── journal-view.md                   ← Human-readable view (auto-generated)
        ├── installed.json                   ← Install/upgrade state (version + per-component hashes)
        └── sprint-logs/                     ← Agent logging (Decision 24, runtime, gitignored)
            └── {sprint-slug}/
                ├── impetus.jsonl            ← Impetus orchestration log
                └── dev-{story-slug}.jsonl   ← Per-story agent logs
```

---

### Architectural Boundaries

**Read/Write Authority:**

<!-- REVISED Phase 3: Updated Impetus, momentum-dev, momentum-create-story rows; replaced momentum-sprint-manager subagent with momentum-tools CLI; added momentum-tools log, sprint-planning workflow, sprint-dev workflow rows. sprint-status.yaml references replaced with stories/index.json and sprints/index.json. -->

| Component | Reads | Writes |
|---|---|---|
| Impetus | stories/index.json, sprints/index.json, journal.jsonl, specs, findings-ledger.jsonl, sprint-logs/{sprint-slug}/ | journal.jsonl, journal-view.md, sprint-logs (via momentum-tools log) |
| momentum-tools sprint | stories/index.json, sprints/index.json | stories/index.json (status fields), sprints/index.json, sprints/{slug}.json (sole writer) |
| momentum:dev | Story files, code | Code in worktree only; sprint-logs (via momentum-tools log, best-effort); structured JSON completion output |
| momentum:create-story | stories/index.json, epics.md | Story files in _bmad-output/implementation-artifacts/ |
| momentum-tools log | (none — write-only append) | .claude/momentum/sprint-logs/{sprint-slug}/*.jsonl (sole writer per agent file) |
| momentum:sprint-planning | stories/index.json, sprints/index.json, story files | sprints/{sprint-slug}/specs/*.feature (Gherkin specs); sprint record team composition (via momentum-tools sprint) |
| momentum:sprint-dev | sprints/index.json (active sprint, team, deps), stories/index.json, sprints/{sprint-slug}/specs/*.feature | Task state (via TaskCreate/TaskUpdate); status transitions (via momentum-tools sprint); sprint completion (via momentum-tools sprint complete) |
| code-reviewer | Source code, specs, acceptance tests | findings (via structured output → flywheel) |
| architecture-guard | Source code, rules, architecture doc | pattern drift report (via structured output) |
| VFL / AVFL | Any artifact being validated, source material | consolidated findings / validation report |
| Flywheel workflow (Epic 6) | findings-ledger.jsonl, rules, specs | findings-ledger.jsonl, rules/, specs |
| Upstream-fix skill (Epic 4, standalone) | session journal, specs, rules | session journal only (not findings-ledger.jsonl) |
| Hooks | Filesystem (reads), git status | Terminal output only (never modifies files) |
| ATDD workflow | Gherkin spec | `tests/acceptance/` only |
| Coding agents (dev-story) | Specs, rules, existing code | Source code, unit tests |

**Protection boundaries (PreToolUse blocks writes to):**
- `tests/acceptance/` — acceptance test immutability
- `_bmad-output/planning-artifacts/` — spec authority
- `.claude/rules/` — enforcement rule integrity
- `~/.claude/momentum/findings-ledger.jsonl` — Ledger integrity (authority-enforced; global path is outside project PreToolUse scope)
- `sprints/{sprint-slug}/specs/` — Gherkin spec integrity (Decision 30: dev agents must never write to this path; only sprint-planning writes, only verifiers read)

---

### Requirements to Structure Mapping
<!-- REVISED 2026-04-03: Plugin model. Source paths at plugin root; installed via plugin mechanism. -->

> _[Changed 2026-04-03: Updated for plugin model. Source paths reference plugin root layout. Installed locations reflect plugin delivery (skills, hooks) vs. Impetus-written (rules, runtime state).]_

| Subsystem | Source File(s) | Installed Location |
|---|---|---|
| Impetus | `skills/impetus/` | Plugin skill: `/momentum:impetus` |
| Sprint planning | `skills/sprint-planning/` | Plugin skill: `/momentum:sprint-planning` |
| Sprint dev | `skills/sprint-dev/` | Plugin skill: `/momentum:sprint-dev` |
| Dev | `skills/dev/` | Plugin skill: `/momentum:dev` |
| AVFL | `skills/avfl/` | Plugin skill: `/momentum:avfl` |
| Upstream Fix / Flywheel | `skills/upstream-fix/` | Plugin skill: `/momentum:upstream-fix` |
| code-reviewer | `skills/code-reviewer/SKILL.md` | Plugin skill: `/momentum:code-reviewer` (context:fork) |
| architecture-guard | `skills/architecture-guard/SKILL.md` | Plugin skill: `/momentum:architecture-guard` (context:fork) |
| Hook infrastructure (always-on) | `hooks/hooks.json` | Delivered by plugin install (active immediately) |
| Plan audit gate hook | `skills/plan-audit/` | Plugin skill: `/momentum:plan-audit` |
| Global rules | `references/rules/*.md` | `~/.claude/rules/` (written by Impetus on first run) |
| Project rules | `references/rules/*.md` | `.claude/rules/` (written by Impetus on first run) |
| MCP servers | `mcp/` source (Epic 6) | `.mcp.json` (written by Impetus when MCP servers are available — Epic 6) |
| Session journal | (runtime) | `.claude/momentum/journal.jsonl` |
| Findings ledger | (runtime) | `~/.claude/momentum/findings-ledger.jsonl` (global) |
| Install state | (runtime) | `.claude/momentum/installed.json` |

---

### Integration Points

**Impetus ↔ Subagents:** Structured JSON output contract (`status`, `result`, `question`, `confidence`)

**Impetus ↔ BMAD:** Enhancement at BMAD workflow completion boundaries — one hard gate (acceptance tests before story close) plus user-discretionary proposals at other boundaries

**Skills ↔ Claude Code:** Plugin discovery via `.claude-plugin/plugin.json`. All skills under `skills/` are registered under the `momentum:` namespace. SKILL.md description loaded at startup; full skill loaded on invocation; `references/` loaded on demand.

**Hooks ↔ Claude Code:** Always-on hooks defined in `hooks/hooks.json` at plugin root; delivered by plugin install and active immediately. Merge with any existing project hook config automatically on session start.

**MCP Servers ↔ Agents:** Findings MCP (Epic 6, optional) provides structured query over `~/.claude/momentum/findings-ledger.jsonl`. Primary write path is direct JSONL append by the flywheel — MCP is a read-only query layer, not the write mechanism. Git file history, blame, and diff for provenance are accessed via the git CLI (Bash tool) — no dedicated MCP server required (see Decision 3c).

**Provenance Scanner ↔ Spec Files:** Reads all `derives_from` frontmatter across the project; computes `referenced_by` graph; compares stored hashes to current `git hash-object`; outputs suspect list to Impetus at session start. Placement: implemented as `references/provenance-scan.md` at the plugin root — runs as part of session orientation, not a separate skill.

**Terminal Multiplexer ↔ Workflows:** Optional protocol binding for terminal pane management (create, read, send, notify, cleanup). Uses the detect-and-adapt pattern: skills check for environment indicators (`CMUX_WORKSPACE_ID`, `CMUX_SURFACE_ID`, `CMUX_SOCKET_PATH` for CMUX; `TMUX` env var for tmux) and adapt behavior when present. Null binding is the default — workflows function identically without a multiplexer. Primary use cases: worktree-to-tab automation (link story sessions to terminal tabs), external process monitoring (simulators, dev servers), and multi-session visual awareness. Reference implementations: CMUX (macOS), tmux (cross-platform). See Epic 7, Story 7.1.

---

## Validation Summary (Steps 7–8)

### Dual-Reviewer Pass Results

Adversarial validation conducted per the dual-reviewer pattern from VFL framework (HANDOFF-BRIEF-001 §Provenance). Enumerator (systematic) + Adversary (failure-focused) passes run against the full document.

**10 findings triaged. All resolved:**

| Finding | Severity | Resolution |
|---|---|---|
| A-1: context:fork + productive waiting contradiction | Revised to Low | Resolved: foreground/background is orthogonal to context:fork isolation. Background subagents confirmed in Claude Code docs. Decision 4c updated. |
| A-2: Global rules auto-load stated as unconditional | High | Fixed: subsystem 4 now states conditional on first `/momentum:impetus` invocation — Impetus writes rules to `~/.claude/rules/` on first run; no separate `momentum setup` CLI (eliminated 2026-03-18) |
| A-3: Copied global rules go stale | High | Fixed: update mechanism added to Decision 5a; Impetus surfaces version-drift warning |
| A-4: Plugin-agent invocation assumed, not verified | High | Resolved (2026-03-18): `context: fork` is a SKILL.md frontmatter field, not a plugin-only feature. code-reviewer and architecture-guard are `context: fork` SKILL.md files. Plugin model adopted (2026-04-03) for deployment packaging — `context: fork` remains a SKILL.md feature within the plugin. |
| A-5: VFL reviewer output unbounded | Medium | Fixed: reviewer output bound added to Decision 3a |
| A-6: Gate vs. proposal distinction undefined | Medium | Fixed: Decision 5b table now includes Type column; one hard gate identified |
| E-1: Provenance scanner has no home | Low | Fixed: placed in momentum/references/provenance-scan.md |
| E-2: Custom MCP server has no source location | Low | Fixed: mcp/findings-server/ added to repository structure |
| E-4: Version pre-commit hook type ambiguous | Low | Fixed: clarified as standard git pre-commit hook (Husky/pre-commit framework) |
| A-7: Confidence weighting unresolved | Low | Fixed: implementation-time decision noted in Decision 3b |

### Architecture Status

**Complete.** All 10 subsystems covered, all 6 NFRs addressed, all 10 potential conflict points specified, all adversarial findings resolved. Momentum is a Claude Code plugin (adopted 2026-04-03). `context: fork` is a SKILL.md feature within the plugin. Skills namespaced under `momentum:`. Workflow modules converted to proper skills.

---

## Sprint Story Lifecycle

> _Added 2026-03-21: Parallel story execution model. Revised 2026-03-21: Unified tracking — Momentum metadata lives in sprint-status.yaml alongside BMAD's development_status. No separate story spec files._

### Story State Machine

> _Revised 2026-04-01: New story stages (verify, closed-incomplete). Story IDs changed to kebab-case slugs. All status writes go through momentum-sprint-manager._
> _Revised 2026-04-02: momentum-sprint-manager subagent replaced by momentum-tools.py sprint CLI. AVFL per-story replaced by AVFL per-sprint (Decision 31). verify stage updated for Phase 3 developer-confirmation model._

```
backlog → ready-for-dev → in-progress → review → verify → done
```

- **`backlog`** — story exists in epics.md/sprint-status.yaml, no story file yet
- **`ready-for-dev`** — story file created, waiting to be picked into a sprint
- **`in-progress`** — sprint-dev agent actively working it (worktree active)
- **`review`** — worktree merged to main, awaiting sprint-level AVFL (automated batch after all sprint stories merge, per Decision 31)
- **`verify`** — AVFL passed, behavioral verification running (developer-confirmation checklist in Phase 3; automated via momentum-verify in future phases)
- **`done`** — verified, complete
- **`dropped`** — removed, obsolete or duplicate (pre-development cancellation)
- **`closed-incomplete`** — story was in a sprint that was force-closed before completion; migrated to next sprint or dropped. Worktree preserved for reference.

**Epic-level statuses:**

- **`done-incomplete`** — Epic closed mid-execution. Some stories completed; others incomplete or dropped. Counts as "done" in accounting.

**Story ID format:** Globally unique kebab-case slugs. No epic encoding.

```
Good:  posttooluse-lint-hook
Good:  impetus-identity-redesign
Bad:   3-1-posttooluse-lint-hook   ← encodes epic, breaks on re-categorization
```

Collision resolution: add short qualifier suffix (`auth-refresh-api` vs `auth-refresh-ui`).

**Status update authority:** All writes to `stories/index.json` (status fields) and `sprints/index.json` go through `momentum-tools.py sprint` — a CLI tool with exclusive write authority over these files. No other agent or script writes to these files directly. Story file content (ACs, dev notes) is written by `momentum:create-story`. The sprint-manager executor subagent described in earlier architecture versions has been superseded by this CLI tool (Phase 2 decision).

### Sprint Tracking Schema — Folder-Based Model

> _Revised 2026-04-01: sprint-status.yaml is deprecated. Story and sprint state is now decomposed into a `stories/` folder and a `sprints/` folder. All status writes via momentum-tools.py sprint CLI (formerly momentum-sprint-manager subagent)._

**`stories/` folder** — one file per story (`stories/{slug}.md`). Created early at backlog stage as a stub (slug, title, epic, status). Fleshed out with full ACs, dev notes, and tasks during sprint planning via `momentum:create-story`. Story file content (ACs, dev notes) is written by `momentum:create-story`.

**`stories/index.json`** — lightweight lookup index. Each entry: slug, status, title, epic slug, story_file (boolean — whether fleshed out), depends_on, touches. Epic membership lives here, not in epics.md.

```json
{
  "posttooluse-lint-hook": {
    "status": "in-progress",
    "title": "PostToolUse lint and format hook",
    "epic": "quality-enforcement",
    "story_file": true,
    "depends_on": [],
    "touches": ["hooks/hooks.json"]
  },
  "impetus-identity-redesign": {
    "status": "ready-for-dev",
    "title": "Impetus Identity & Persona Section",
    "epic": "impetus-ux",
    "story_file": true,
    "depends_on": [],
    "touches": ["skills/impetus/workflow.md"]
  },
  "model-routing-frontmatter": {
    "status": "backlog",
    "title": "Model routing configured by frontmatter",
    "epic": "quality-enforcement",
    "story_file": false,
    "depends_on": [],
    "touches": []
  }
}
```

<!-- REVISED Phase 3: Added team composition, dependencies, and specs directory to sprint record schema per Decisions 25, 26, 29, 30. -->

**`sprints/` folder** — one file per sprint (`sprints/{slug}.json`). Contains: name, slug, stories list, locked flag, started/completed dates, team composition, dependency graph, and wave plan. One specs directory per sprint (`sprints/{slug}/specs/`) for Gherkin feature files.

**`sprints/index.json`** — which sprint is active, which is planning, list of completed sprint slugs.

**`sprints/{sprint-slug}/specs/`** — Gherkin feature files written during sprint planning (Decision 30). One file per story: `{story-slug}.feature`. These specs encode detailed behavioral expectations that only verifier agents access. Dev agents NEVER read this directory — verification is black-box by design. Story markdown files retain plain English ACs only; Gherkin is never written back to story files.

```json
// sprints/index.json
{
  "active": "quality-hooks-sprint",
  "planning": "impetus-ux-sprint",
  "completed": []
}

// sprints/quality-hooks-sprint.json
{
  "name": "Quality Hooks Sprint",
  "slug": "quality-hooks-sprint",
  "stories": ["posttooluse-lint-hook", "pretooluse-file-protection", "stop-gate-quality-checks"],
  "locked": true,
  "started": "2026-03-30",
  "completed": null,
  "team": {
    "roles": [
      {"role": "dev", "guidelines": "path/to/project-dev-guidelines.md"},
      {"role": "qa", "guidelines": "path/to/project-qa-guidelines.md"}
    ],
    "story_assignments": {
      "posttooluse-lint-hook": {"role": "dev"},
      "pretooluse-file-protection": {"role": "dev"},
      "stop-gate-quality-checks": {"role": "dev"}
    }
  },
  "dependencies": {
    "stop-gate-quality-checks": ["posttooluse-lint-hook"]
  },
  "waves": [
    { "wave": 1, "stories": ["posttooluse-lint-hook", "pretooluse-file-protection"] },
    { "wave": 2, "stories": ["stop-gate-quality-checks"] }
  ]
}
```

**`epics.md`** — names, slugs, and descriptions only. No story lists. Pure documentation. Epic membership is tracked in `stories/index.json`.

**`sprint-status.yaml` is deprecated** — replaced by the folder-based model above. The `sprint-status-schema-decomposition` migration story handles the transition from sprint-status.yaml to the new structure.

**Write authority:** `momentum-tools.py sprint` is the sole writer of the `sprints/` folder and the `status` fields in `stories/index.json`. Story file content (ACs, dev notes, tasks) is written by `momentum:create-story`. Sprint-scoped Gherkin specs (`sprints/{sprint-slug}/specs/`) are written by the sprint-planning skill (`/momentum:sprint-planning`). No other agent or script writes to these files directly.

### Story Assignment Model

<!-- REVISED Phase 3: Replaced Next-Story Selection Rule. momentum-dev no longer selects stories autonomously. Story assignment is managed by the sprint-dev workflow (Impetus). -->

momentum-dev does NOT select its own stories. Story assignment is managed by the sprint-dev skill (`/momentum:sprint-dev`):

1. sprint-dev reads the active sprint record from `sprints/index.json`
2. sprint-dev resolves the dependency graph from story `depends_on` fields
3. sprint-dev identifies unblocked stories (all dependencies merged)
4. sprint-dev spawns one momentum-dev agent per unblocked story, passing the story file path and role-specific guidelines
5. When a story completes and merges, sprint-dev re-evaluates the dependency graph and spawns agents for newly unblocked stories

momentum-dev receives its story assignment as input — it never reads `stories/index.json` to choose what to work on. If momentum-dev is invoked standalone (outside a sprint context), the developer provides the story path directly.

### Session Journal Extension: `active_stories`

The session journal `active_story` field (singular) extends to `active_stories` (array) to support concurrent sessions:

```json
{
  "active_stories": [
    {
      "story_id": "posttooluse-lint-hook",
      "worktree_path": ".worktrees/story-posttooluse-lint-hook",
      "target_branch": "main",
      "phase": "Implement"
    },
    {
      "story_id": "sprint-status-schema",
      "worktree_path": null,
      "target_branch": "main",
      "phase": "ATDD"
    }
  ]
}
```

Impetus's session orientation must handle the multi-story case: when multiple stories are active, summarize all active sessions and their current phases.

### Parallel Story Execution Model (Always-Worktree)

Every `momentum-dev` session runs in its own git worktree from the start — even if it appears to be the only session. This eliminates the mid-session file-change race (if Story A ran in main and Story B merged first, A would find changed files under it).

**Worktree naming convention:** `.worktrees/story-{story_id}` on branch `story/{story_id}`

**Target branch:** Captured at invocation via `git branch --show-current` (Bash tool). The worktree merges back to this branch on completion — not hardcoded to `main`.

**Worktree environment:** Git worktrees share the same `.git` directory — all project files, skills, config, and `.claude/` structure are available inside every worktree.

**`.worktrees/` directory:** Must be in `.gitignore` — worktrees are local execution environments, not committed artifacts.

**Concurrency limitation (single-developer):** Two sessions started within ~30 seconds of each other may both read the same story as `ready` before either writes `in_progress`. Mitigation: start sessions with a brief (~30s) offset. A lock file (`.worktrees/story-{story_id}.lock`) provides additional protection and should be checked before status write.

**Ready for:** Epic and story creation.

---

## Sprint Orchestration Architecture

<!-- REVISED Phase 3: Replaced Epic Orchestration Architecture with Sprint Orchestration Architecture. Waves replaced by dependency-driven team concurrency (Decision 25). AVFL moved from per-story to per-sprint (Decision 31). Epic commands replaced by sprint workflow modules. momentum-dev-auto section removed — momentum-dev simplified to pure executor, subsuming momentum-dev-auto's scope. dag-executor section removed — dependency-driven model replaces wave-based scheduler. -->

> _Added 2026-03-26: Epic orchestration model. Revised 2026-04-02: Replaced with sprint-centric, dependency-driven model per Phase 3 Decisions 24-31._

The sprint is the primary unit of planned work. The lifecycle is:

```
backlog (mutable) → /momentum:sprint-planning (story selection + team composition + Gherkin specs + AVFL)
  → /momentum:sprint-dev (dependency-driven execution + post-merge AVFL + verification)
  → /momentum:retro (structured handoff from agent logs)
  → backlog (next cycle)
```

**Sprint immutability rule:** Once `momentum-tools sprint activate` is called, the sprint is locked. No patching in-place. Recovery path: close sprint (set status `closed-incomplete`), migrate incomplete stories to next sprint backlog.

### Sprint Planning Workflow (Decision 29)

Sprint planning is a dedicated skill (`/momentum:sprint-planning`) with 8 steps. Invoked by Impetus when the developer selects "Plan a sprint" from the session menu, or directly by the user:

1. **Backlog presentation** — read stories/index.json, group by epic, exclude terminal states
2. **Story selection** — developer selects 3-8 stories, register via momentum-tools sprint plan
3. **Story fleshing-out** — spawn `/momentum:create-story` for each stub; developer approves each
4. **Gherkin spec generation** — write detailed `.feature` files to `sprints/{sprint-slug}/specs/`; story files retain plain English ACs only (Decision 30)
5. **Execution plan and team composition** — analyze stories to determine agent roles, project guidelines, dependency graph, and execution waves (Decision 26: two-layer agent model)
6. **AVFL validation** — single AVFL pass on the complete sprint plan (all stories together, not per-story — Decision 31)
7. **Developer review** — present full plan for approval; developer can request adjustments
8. **Sprint activation** — call `momentum-tools sprint activate`; log the decision

### Dependency-Driven Execution (Decision 25: Teams Over Waves)

The DAG topology is derived from `depends_on` fields in `stories/index.json`. Execution is dependency-driven, not wave-sequential:

1. Identify unblocked stories (no dependencies, or all dependencies already `done`)
2. Spawn one momentum-dev agent per unblocked story (each in its own worktree)
3. When a story completes and merges, re-evaluate the dependency graph
4. Spawn agents for newly unblocked stories
5. Repeat until all sprint stories have merged

Wave assignments in the sprint record are informational (planning visualization) — execution order is determined by dependency resolution at runtime. Multiple stories can run concurrently if they share no dependencies. A story with dependencies waits until ALL its blockers have merged.

### Two-Layer Agent Model (Decision 26)

Momentum provides generic agent roles with orchestration patterns:
- **Dev** — implements stories in worktrees, logs decisions via momentum-tools log
- **QA** — reviews code against acceptance criteria
- **E2E Validator** — validates end-to-end behavior against Gherkin specs
- **Architect Guard** — checks pattern drift against architecture decisions

Projects provide stack-specific guidelines per role (e.g., "Frontend Dev uses Kotlin Multiplatform + Compose, TDD required"). Sprint planning wires the layers together: for each story, determine which roles apply based on `change_type` and `touches`, then attach the project's guidelines for those roles. The team composition is stored in the sprint record.

### Agent Guidelines Generation (FR61a)

The `agent-guidelines` skill (`/momentum:agent-guidelines`) creates the project-specific guidelines that the two-layer model requires. It operationalizes the research findings from the Agent Guidelines Authoring research (see `_bmad-output/planning-artifacts/research/technical-agent-guidelines-authoring-research-2026-04-03.md`).

**Design principles (evidence-based):**
- Instruction budget is ~100-150 slots; every rule competes with every other rule
- Path-scoped rules (`.claude/rules/*.md` with `paths:` frontmatter) load only when matching files are touched — zero cost when irrelevant
- Three-layer architecture: Layer 1 (path-scoped rules, 30-80 lines) → Layer 2 (reference docs, 100-300 lines, on-demand) → Layer 3 (skills, unlimited, invoked)
- Correct stale training data, don't teach basics — prohibitions over aspirations
- Pin versions, date-stamp, put critical prohibitions first

**Workflow phases:**

1. **Discover** — Parallel subagents (Sonnet/medium) scan build files, existing `.claude/rules/`, test configs, and source patterns to produce a structured technology profile with versions
2. **Research** — Parallel subagents (Sonnet/medium) with web search perform 2-3 focused queries per detected technology for breaking changes, deprecated APIs, and current best practices. Outputs prohibition-format corrections. Does not invoke the full research skill — stays light; user can escalate if needed
3. **Consult** — Interactive back-and-forth with the developer across decision points: technology inventory confirmation, existing guidelines audit, testing framework recommendations, validation approach (which roles need guidelines), path scope design (glob patterns), and content depth (Layer 1/2/3 decisions)
4. **Generate** — Parallel subagents (Sonnet/high) produce artifacts from templates: path-scoped `.claude/rules/*.md` files, reference docs in `docs/references/`, and CLAUDE.md pointer updates
5. **Validate** — AVFL checkpoint profile on all generated artifacts

**Key architectural choices:**
- Opus for orchestration (consultation needs nuance), Sonnet for all subagents (scoped tasks)
- Detection heuristics live in a reference file (`references/detection-heuristics.md`), not code — extensible, AVFL-validatable, human-editable
- Consultation happens before generation — don't waste compute on artifacts the user doesn't want
- Generic agents in Momentum carry practice/workflow; generated project rules carry technology corrections — they compose automatically through the file system at runtime via path-scoped loading

### Sprint Execution Flow (sprint-dev skill)

sprint-dev is a dedicated skill (`/momentum:sprint-dev`) with 6 phases. Invoked by Impetus when the developer selects "Continue sprint" from the session menu, or directly by the user:

**Phase 1: Initialization**
- Read active sprint from `sprints/index.json`; validate locked state
- Build dependency graph from story `depends_on` fields
- Create a task per story via TaskCreate for progress tracking
- Log sprint start via momentum-tools log

**Phase 2: Team Spawn**
- Identify unblocked stories
- Transition each to `in-progress` via `momentum-tools sprint status-transition`
- Within the team, execute the first unblocked story sequentially; subsequent unblocked stories execute one at a time after each commit-as-sync-point (see Agent Teams model). Parallel execution of independent stories requires separate terminal sessions, not within a single team session.
- Each agent logs all activity via momentum-tools log

**Phase 3: Progress Tracking Loop**
- Monitor spawned agents via task status
- On story completion: propose merge to developer (merge gate — never auto-execute)
- After merge: transition to `review`, re-evaluate dependency graph, spawn newly unblocked stories
- Repeat until all stories have merged

**Phase 4: Post-Merge Quality Gate (Decision 31: AVFL at Sprint Level)**
- Run single AVFL pass on the full codebase (all sprint changes together)
- AVFL no longer runs per-story — it runs once after ALL stories merge
- If findings: present to developer, iterate fixes
- This catches cross-story integration issues that per-story AVFL would miss

**Phase 5: Verification (Decision 30: Black-Box)**
- Read Gherkin specs from `sprints/{sprint-slug}/specs/`
- Dev agents never access this directory — verification is black-box
- Phase 3 implementation: developer-confirmation checklist derived from Gherkin scenarios
- Future: automated verification via momentum-verify skill
- On full confirmation: transition all stories to `done`

**Phase 6: Sprint Completion**
- Run `momentum-tools sprint complete` to archive the sprint
- Surface summary: stories completed, merge order, AVFL findings, verification results
- Suggest retrospective as next step

### Agent Pool Governance

**Pool cap:** Configurable, default 12 concurrent agents. Applied at spawn time.

**AVFL at sprint level (Decision 31):** AVFL does NOT run per-story. momentum-dev has no AVFL. A single AVFL pass runs after ALL sprint stories merge (Phase 4 of sprint-dev). This is a deliberate architectural change from the pre-Phase-3 model where AVFL was embedded in each story agent.

**Merge gate:** Every merge requires explicit developer confirmation. sprint-dev proposes the merge and waits — never auto-executes. momentum-dev signals "ready to merge" in its structured completion output.

**Pre-flight checks before sprint execution:**
1. Active sprint exists and is locked
2. Topological sort validity / cycle detection
3. Dangling reference detection — every `depends_on` key must exist in sprint story list
4. Story file existence for all sprint stories
5. Correct story status — unblocked stories must be `ready-for-dev`

### momentum-dev — Simplified Pure Executor

<!-- REVISED Phase 3: momentum-dev simplified to pure executor. momentum-dev-auto is subsumed — the simplified momentum-dev has no AVFL, no status writes, no DoD supplement, no code review offer, making it functionally equivalent to what momentum-dev-auto was designed to be. -->

momentum-dev is a pure executor: worktree setup, bmad-dev-story invocation, agent logging, and structured completion output. It does NOT:
- Run AVFL (moved to sprint-dev Phase 4)
- Write status transitions (handled by sprint-dev after merge)
- Apply DoD supplement (moved to sprint-level verification)
- Offer code review (orthogonal concern managed by caller)

momentum-dev emits structured JSON completion output that sprint-dev parses: status, files modified, test results. All decisions are logged via `momentum-tools log` with best-effort execution (logging failures do not block development).

**Note:** The pre-Phase-3 `momentum-dev-auto` variant (background-safe, no ask gates) is subsumed by this simplified momentum-dev. With AVFL, status transitions, DoD, and code review removed, momentum-dev itself is now a pure executor suitable for both interactive and background execution.

---

### Retro → Triage Handoff Format

After each epic, the retro skill writes structured entries to `triage-inbox.md`. The developer reviews before triage runs — retro does not auto-launch triage.

**triage-inbox.md location:** `_bmad-output/implementation-artifacts/triage-inbox.md` (per-project, not global)

**triage-inbox.md is append-only per epic.** Triage reads the full inbox and classifies each item before marking it consumed.

**Entry format per action item:**
```yaml
- source: "epic-N-retro"
  type: "action-item"        # action-item | incomplete-story | blocker-resolution
  priority: "high"           # high | medium | low
  description: "..."
  references:
    - story_key: "..."
    - file: "..."
  proposed_resolution: "..."
```

**Type vocabulary:**
- `action-item` — a practice improvement, process fix, or architectural change surfaced by the retro
- `incomplete-story` — a story that was `closed-incomplete` during the epic; needs re-triage before it can re-enter the backlog
- `blocker-resolution` — a dependency or external blocker that was worked around; resolution should be tracked

**Triage consumption:** After triage processes an item, it appends a `consumed_at` timestamp and `triage_outcome` field to the entry. The inbox is never truncated — full history is preserved.

---

### Agent Logging Infrastructure (Decision 24)

<!-- Added Phase 3: Agent logging as foundational infrastructure for retrospectives and observability. -->

Every agent in the system records structured JSONL logs via the `momentum-tools log` CLI. Agent logs are the primary input for retrospective workflows — they provide the evidence trail of decisions, errors, and assumptions made during sprint execution.

**Storage location:** `.claude/momentum/sprint-logs/{sprint-slug}/`

**File naming:**
- `{agent-role}.jsonl` — orchestration-level logs (e.g., `impetus.jsonl`)
- `{agent-role}-{story-slug}.jsonl` — per-story agent logs (e.g., `dev-agent-logging-tool.jsonl`)

**JSONL entry schema:**
```json
{"timestamp": "2026-04-02T14:30:00.123456", "agent": "momentum-dev", "story": "agent-logging-tool", "event": "decision", "detail": "Chose worktree-based isolation for concurrent story execution"}
```

**Event type vocabulary (6 types, no others):**

| Event | When to use |
|---|---|
| `decision` | Agent chose between alternatives — record the choice and why |
| `error` | Something failed — record what and context |
| `retry` | Agent is retrying an operation — record attempt number and reason |
| `assumption` | Agent assumed something not explicitly stated — record what |
| `finding` | Agent discovered something noteworthy — record observation |
| `ambiguity` | Agent encountered unclear input — record what was unclear |

**Write authority model:** Each agent file has exclusive write authority by the agent that created it. Append-only — no reads or modifications by any agent. The `momentum-tools log` CLI is the sole write interface.

**CLI interface:**
```
momentum-tools log --agent <role> --story <slug> --sprint <slug> --event <type> --detail "..."
```

**Runtime characteristics:**
- Sprint-logs are runtime artifacts, not committed to version control (gitignored)
- Directory structure is created automatically on first write
- Log calls are best-effort from momentum-dev — logging failures do not block development
- Sprint-logs are the primary input for the retro workflow (Decision 27: two-output retro)

### Gherkin Specification Separation (Decision 30)

<!-- Added Phase 3: Black-box behavioral validation via separated Gherkin specs. -->

Story files and Gherkin specs are deliberately separated to enforce black-box validation:

- **Story files** (`stories/{slug}.md`) — contain plain English acceptance criteria. Dev agents read these to understand intent.
- **Gherkin specs** (`sprints/{sprint-slug}/specs/{story-slug}.feature`) — contain detailed behavioral expectations. Only verifier agents read these.

**Key constraints:**
- Gherkin specs are written during sprint planning (Step 4), before any code exists
- Dev agents NEVER access `sprints/{sprint-slug}/specs/` — this is a protection boundary
- Gherkin is NEVER written back to story files
- Specs are validated post-implementation by different agents than those who wrote the code
- This separation enables true black-box behavioral validation

---

## Phase 3 Architecture Decisions (24-31)

<!-- Added Phase 3: Decisions from the Phase 3 plan that govern sprint execution, agent logging, and team model. -->

**Decision 24 — Agent Logging as Foundational Infrastructure**
Every agent writes JSONL logs via `momentum-tools log`. Logs are the primary input for retrospectives. Per-agent exclusive write authority. Storage: `.claude/momentum/sprint-logs/{sprint-slug}/`. See Agent Logging Infrastructure section for full specification.

**Decision 25 — Teams Over Waves**
Dependency-driven concurrency replaces rigid wave tiers. The sprint-dev skill (`/momentum:sprint-dev`) spawns agents for unblocked stories and spawns more as dependencies complete. Wave assignments in sprint records are informational for planning visualization — execution order is determined by dependency resolution at runtime. See Dependency-Driven Execution section.

**Decision 26 — Two-Layer Agent Model**
Momentum provides generic roles (Dev, QA, E2E Validator, Architect Guard). Projects provide role-specific stack guidelines. Sprint planning (`/momentum:sprint-planning`) wires the layers together — for each story, determine which roles apply based on `change_type` and `touches`, then attach the project's guidelines. Team composition is stored in the sprint record. Agent Teams share a working directory; sequential story execution with commit-as-sync-point means no worktree needed within a team. Teammates load skills from project/user settings, not from `.agent.md` `skills` frontmatter — dev agents get workflow instructions through their spawn prompt. See Two-Layer Agent Model section.

**Decision 27 — Two-Output Retro**
Retro produces two triage outputs from agent logs: Momentum triage (practice improvements) and Project triage (project-specific findings). Agent logs (Decision 24) are designed to support this dual-output pattern. Full retro implementation is deferred to Phase 5.

**Decision 28 — Triage vs Refinement Distinction**
Triage is intake-focused: analyze documents/ideas, create story stubs, initial prioritization, assign to an epic. Refinement is organization-focused: classify, prioritize, gap-analyze the whole backlog. Different purposes, complementary workflows. Both deferred to Phase 5.

**Decision 29 — Sprint Planning Builds the Team**
Sprint planning (`/momentum:sprint-planning`) encompasses story selection, create-story invocation, team composition, dependency graph construction, and execution plan generation. Sprint planning is a proper skill (not an inline workflow module) — invoked by Impetus or directly by the user. The sprint record stores team + dependencies (not just story lists and wave assignments). See Sprint Planning Workflow section.

**Decision 30 — Gherkin Separation**
Story files retain plain English ACs (dev sees intent). Sprint-scoped specs directory holds detailed Gherkin `.feature` files (verifiers only). Black-box behavioral validation: specs written pre-implementation, validated post-implementation, by different agents. See Gherkin Specification Separation section.

**Decision 31 — AVFL at Sprint Level**
AVFL validates the complete sprint plan during planning (all stories together). AVFL runs once after ALL stories merge during sprint execution (not per-story). Per-story AVFL is removed from `momentum:create-story` and `momentum:dev`. This catches cross-story integration issues that per-story AVFL would miss. See Agent Pool Governance section.
