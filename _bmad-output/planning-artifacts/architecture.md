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
---

# Architecture Decision Document: Momentum

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements (10 subsystems):**

Momentum's FRs organize into 10 architectural subsystems:

1. **Deployment Packaging** — Standard Agent Skills (SKILL.md) as the sole deployment mechanism; no plugin required. Claude Code-specific frontmatter (`context: fork`, `model:`, `effort:`) optimizes for Claude Code while remaining standards-compliant. Flat skills run in main context; `context: fork` skills run in isolated subagent contexts for pure verifiers. Rules, hooks config, and MCP config are bundled in `skills/momentum/references/` and written by Impetus on first `/momentum` invocation — `npx skills add` deploys SKILL.md files only; Impetus handles all non-skills config. One set of SKILL.md files serves all targets.

2. **Provenance Infrastructure** — `derives_from` frontmatter (downstream-only authoring), content hash staleness detection, suspect link flagging (pull-based), auto-generated `referenced_by`, Chain of Evidences prompting, Citations API integration for mechanical grounding.

3. **Hook Infrastructure (Tier 1 Deterministic)** — PostToolUse auto-lint/format, PreToolUse acceptance test directory protection, PreToolUse file protection, PreToolUse git-commit quality gate, PreToolUse plan audit gate (ExitPlanMode), Stop conditional quality gate. Two hook deployment mechanisms: (1) **Always-on hooks** — configuration template bundled in `skills/momentum/references/hooks-config.json`; Impetus writes it to `.claude/settings.json` on first `/momentum` invocation using the Write tool; these fire on every matching tool event in every session regardless of which skill is active. (2) **Skill-lifecycle hooks** — defined in SKILL.md `hooks:` frontmatter; scoped to the skill's lifetime; only fire while that skill is active; automatically cleaned up when the skill completes. Research confirmation (2026-03-19): hooks in SKILL.md frontmatter are a Claude Code-exclusive feature; `npx skills add` does not deploy hooks independently — they are embedded in the SKILL.md file itself or written to `.claude/settings.json` by Impetus. Complemented by standard git hooks (Husky/pre-commit framework) at the repository level.

4. **Rules Architecture (Tier 3 Advisory)** — Global `~/.claude/rules/` (authority hierarchy, anti-patterns, model routing) + project `.claude/rules/` (architecture conventions, stack-specific standards). Project-scoped rules auto-load in every session including subagents. Rules are bundled in `skills/momentum/references/rules/` and written to both targets by Impetus on first `/momentum` invocation — no separate setup step. Research confirmation (2026-03-19): `npx skills add` cannot write to `~/.claude/rules/` or `.claude/rules/`; it deploys SKILL.md files only. Rules deployment via Impetus's Write tool is the correct and only mechanism.

5. **Subagent Composition** — code-reviewer (read-only tools, pure verifier, never modifies code), architecture-guard (pattern drift detection). Both use `context: fork` for producer-verifier isolation. Hub-and-spoke: Impetus is the sole user-facing voice; subagents return structured output to Impetus for synthesis. Subagents cannot spawn subagents — chains route through main conversation.

6. **Validate-Fix Loop (VFL) Skill** — Three profiles: Gate (1 agent, pass/fail), Checkpoint (2-4 agents, 1 fix attempt), Full (dual-reviewer per lens, up to 4 fix iterations). Four lenses: Structural Integrity, Factual Accuracy, Coherence & Craft, Domain Fitness. Consolidation handles deduplication, cross-check confidence tagging, and scoring. Invocable standalone, inline from workflows, or declared as a rule.

7. **Orchestrating Agent — Impetus** — Session orientation (reads ledger, surfaces active threads), visual progress (✓ Built / → Now / ◦ Next), proactive gap detection, productive waiting during subagent execution, hub-and-spoke voice unification. Impetus is the force that maintains practice velocity — the system keeps compounding because Impetus carries knowledge and context forward across sessions and sprints without requiring repeated external input.

8. **Findings Ledger + Evaluation Flywheel** — Structured findings with provenance_status field; cross-story pattern detection; flywheel workflow (Detection → Review → Upstream Trace → Solution → Verify → Log) with visual status graphics; `/upstream-fix` skill; retrospective integration.

9. **Model Routing** — `model:` and `effort:` frontmatter required on every SKILL.md and agent definition. Cognitive hazard rule: flagship models for outputs without automated validation. Escalation semantics in VFL: mid-tier first, flagship if not converging within 3-4 iterations.

10. **Protocol-Based Integration** — Every integration point (validation, research, review, tools, documents) defines an interface before implementation is wired. Implementations are substitutable: swap the ATDD framework, the research model, the validation profile — the practice layer is unchanged.

---

### Non-Functional Requirements

- **Portability gradient** — Tier 1 (hooks) = Claude Code only; Tier 2 (structured workflows) = partially portable; Tier 3 (rules) = all tools. System degrades gracefully — Cursor gets skills + rules, Claude Code gets full enforcement.
- **Context budget** — Agent Skills three-stage loading (description at startup ~100 tokens, full SKILL.md on invocation, references/ on demand) means startup overhead is manageable with good authoring discipline. Concise descriptions, heavy content in references/. Hygiene note, not a hard constraint.
- **Evolvability (Impermanence Principle)** — Thin packaging layer. Practice portable even if skills ecosystem changes. Monthly ecosystem review. Interfaces before implementations everywhere.
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
<!-- REVISED: Verified deployment constraints against github.com/vercel-labs/skills README and agentskills.io/specification (2026-03-19). Confirmed: npx skills add deploys SKILL.md files only — no hooks, rules, agents, or MCP config. Hooks in SKILL.md frontmatter are skill-lifecycle-scoped (Claude Code + Cline only). context:fork is Claude Code-exclusive. Plugin-agent spike confirmed eliminated. -->

- **Agent Skills standard** — SKILL.md format; Claude Code-specific frontmatter silently ignored by other tools; one file, dual behavior by design
- **Subagents cannot spawn subagents** — VFL orchestration chains through main conversation; affects Full-profile parallel execution design
- **context:fork isolation** — `context: fork` is a SKILL.md frontmatter field, Claude Code-exclusive (confirmed: compatibility table in vercel-labs/skills README — only Claude Code = Yes; all other agents = No). Skills with `context: fork` run in isolated subagent contexts without access to conversation history. code-reviewer and architecture-guard are implemented as `context: fork` SKILL.md files — no plugin required. The `allowed-tools` frontmatter field restricts tool access (e.g., `Read` only for pure verifiers). Plugin-agent invocation spike is eliminated — `context: fork` is a SKILL.md frontmatter feature.
- **Non-skills deployment: bundled and agent-written** — `npx skills add` deploys SKILL.md files and their bundled supporting files (scripts/, references/, assets/) only. It cannot write to `~/.claude/rules/`, `.claude/settings.json`, `.mcp.json`, or any config target outside the skills directory. Rules, hook config templates, MCP config templates, and the install/upgrade manifest are bundled inside `skills/momentum/references/`. Impetus uses `${CLAUDE_SKILL_DIR}` to locate its own skill directory and writes these files directly to their targets. Install/upgrade logic is governed by `momentum-versions.json` and `installed.json` (Decision 5c). The UX interaction for install/upgrade is defined in the UX specification.
- **Hooks: two deployment paths** — Always-on hooks (fire every session regardless of skill) are written to `.claude/settings.json` by Impetus. Skill-lifecycle hooks (fire only while a specific skill is active) are defined in SKILL.md `hooks:` frontmatter and require no separate deployment — they travel with the skill. Both are Claude Code-exclusive features confirmed by the hooks row in the vercel-labs/skills compatibility table (Claude Code = Yes; all other agents except Cline = No).

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
<!-- REVISED: Plugin/Unit 1/Unit 2 model removed; skills-only deployment confirmed against live research sources (2026-03-19). npx skills add deploys SKILL.md files only — hooks, rules, and MCP config deploy via Impetus. -->

> _[Changed 2026-03-18: Removed two-unit plugin + skills model. All deployment is now via standard Agent Skills only (`npx skills add`). Plugin/Unit 1 concept eliminated. code-reviewer and architecture-guard are `context: fork` SKILL.md files, not plugin agents. Reason: product owner direction; plugin model rejected. Research source: agentskills.io/specification + github.com/vercel-labs/skills README, verified March 18, 2026.]_
> _[Verified 2026-03-19: Research pass against live sources confirms npx skills add deploys SKILL.md + bundled files only; no hooks/rules/MCP deployment via skills CLI. Deployment table and descriptions are accurate.]_

### Skills Deployment Classification

The defining question for each component: *does this need main-context persona persistence, or does it benefit from isolation?*

| Component | Deployment | Rationale |
|---|---|---|
| Impetus (orchestrating agent) | Flat skill | Must persist persona across interactions |
| VFL skill | Flat skill | Must orchestrate parallel spawning from main context |
| upstream-fix, create-story, dev-story | Flat skills | Stateful workflows needing main context |
| code-reviewer | `context: fork` skill | Pure verifier — `context: fork` provides isolation; `allowed-tools: Read` enforces read-only |
| architecture-guard | `context: fork` skill | Pattern analysis — isolation prevents drift; `allowed-tools: Read` enforces read-only |
| Always-on hooks | `.claude/settings.json` | Template bundled in `skills/momentum/references/hooks-config.json`; Impetus writes on first `/momentum` run |
| Global rules | `~/.claude/rules/` | Bundled in `skills/momentum/references/rules/`; Impetus writes on first `/momentum` run |
| Project rules | `.claude/rules/` | Bundled in `skills/momentum/references/rules/`; Impetus writes on first `/momentum` run |
| MCP config | `.mcp.json` | Template bundled in `skills/momentum/references/mcp-config.json`; Impetus writes on first `/momentum` run |

### Repository Structure (preview — full structure in Project Structure section)

```
momentum/
├── skills/                          ← All skills: flat + context:fork
│   ├── momentum/SKILL.md
│   ├── momentum-vfl/SKILL.md
│   ├── momentum-code-reviewer/SKILL.md    ← context: fork, allowed-tools: Read
│   ├── momentum-architecture-guard/SKILL.md ← context: fork, allowed-tools: Read
│   ├── momentum-upstream-fix/SKILL.md
│   ├── momentum-create-story/SKILL.md
│   └── momentum-dev-story/SKILL.md
│
├── rules/                           ← Advisory rules source
│   ├── authority-hierarchy.md
│   ├── anti-patterns.md
│   └── model-routing.md
│
└── .claude/                         ← Project config (committed to repo)
    ├── rules/                       ← Project-scoped rules (committed)
    └── settings.json                ← Always-on hook definitions (Tier 1 enforcement; committed)
```

### Install Experience
<!-- REVISED: Plugin+setup command replaced with single npx skills add; momentum setup and momentum bootstrap CLIs eliminated. Install command format verified against vercel-labs/skills README (2026-03-19). -->

> _[Changed 2026-03-18: Two-command plugin + skills install replaced with single `npx skills add`. Changed again (2026-03-18): removed separate `momentum setup` step — Impetus handles all first-run configuration automatically. Reason: single entry point; no separate installer.]_
> _[Verified 2026-03-19: Install command format confirmed against vercel-labs/skills README. No momentum setup CLI, no momentum bootstrap CLI. Impetus is the sole post-install entry point.]_

```bash
# Install Momentum into any Claude Code project
npx skills add momentum/momentum -a claude-code

# Single entry point — all setup, config, and upgrades flow through here:
/momentum
```

`npx skills add` installs the SKILL.md files and their bundled `references/` content to `.claude/skills/`. It does not install hooks, rules, or MCP config — those are written by Impetus on first `/momentum` invocation. No `momentum setup` command. No `momentum bootstrap` command. No separate plugin install.

Impetus handles install and upgrade via the manifest mechanism (Decision 5c). What triggers install vs. upgrade checks, and how the user experience unfolds, is defined in the UX specification — not here. The architectural guarantee: `/momentum` is the only interface; all setup and upgrade paths flow through it.

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

**Decision 1b — Session Ledger: JSON with Markdown View**
- Location: `.claude/momentum/ledger.json`
- Impetus reads/writes JSON for reliable structured updates
- Auto-generated `.claude/momentum/ledger-view.md` for human readability
- Tracks: active story, current phase, last completed action, open threads

**Decision 1c — Findings Ledger: JSON**
- Location: `.claude/momentum/findings-ledger.json`
- Structured array of findings with fields: `id` (unique finding identifier), `story_ref`, `phase`, `severity`, `pattern_tags`, `description`, `evidence`, `provenance_status`, `upstream_fix_applied`, `upstream_fix_level`, `upstream_fix_ref` (reference to the fix artifact), `timestamp` (ISO 8601 when finding was recorded)
- `upstream_fix_level` — null until a fix is applied; then one of: `spec-generating-workflow | specification | rules-or-CLAUDE.md | tooling | one-off-code-fix`
- Queryable for cross-story pattern detection (same pattern across S-04, S-07, S-11)
- Only flywheel workflow writes findings; read by Impetus at retrospective and upstream trace

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
| `.claude/momentum/findings-ledger.json` | Ledger integrity — only flywheel workflow writes |

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
- **VFL runs as a flat skill** (main context, not context:fork) — orchestration needs main context to spawn agents
- **Impetus invokes VFL** from main conversation
- **VFL spawns all reviewers in parallel** — up to 8 simultaneous subagents for Full profile (2 per lens × 4 lenses)
- **Reviewers are context:fork skills** defined in `skills/momentum-code-reviewer/` — isolated via `context: fork`, read-only via `allowed-tools: Read` in their SKILL.md frontmatter
- **VFL consolidates results** in main context after all reviewers complete
- Context window consideration: all reviewer results return to main context; keep reviewer output structured and bounded
- **Execution mode:** reviewer subagents run as **background agents** (non-blocking — main conversation continues); automated hook-triggered passes may use foreground (blocking) where dead air is acceptable. Background execution is what enables productive waiting (Decision 4c).
- **Reviewer output bound:** Reviewers return structured JSON (not free-form prose). VFL framework (vfl-framework-v3.json) specifies per-reviewer output schema. Impetus enforces this to keep context accumulation bounded across all reviewer results.
- **Implementation note:** Background agent execution model is validated in Story 2.Spike (Epic 2) before Stories 2.4 and 4.3 begin. Do not implement productive waiting or background VFL execution until spike result is documented. The execution mode is adopted as the architectural intent; the spike validates the specific implementation mechanism (inter-agent communication + checkpoint/resume). If the spike reveals the mechanism is unavailable, Decision 3a/4c will be revised before Stories 2.4 and 4.3 begin.

**context:fork agent count — explicit model:**

> _[Added 2026-03-18: Clarifying how multiple agents are actually created. `context: fork` = one agent per invocation.]_

`context: fork` creates **exactly one** isolated subagent per invocation. Multiple parallel agents = multiple Agent tool calls. VFL's parallel execution works as follows:

- VFL (flat skill, main context) issues **N separate Agent tool calls**, each with `run_in_background: true`
- Each call spawns one isolated subagent running momentum-code-reviewer with different lens criteria passed via `$ARGUMENTS`
- The same skill is invoked N times with different parameters — NOT N different skill types
- **Full profile agent count:** 8 Agent tool calls = 8 concurrent reviewer agents (2 per lens × 4 lenses: Structural Integrity, Factual Accuracy, Coherence & Craft, Domain Fitness)
- **Checkpoint profile:** 2–4 Agent tool calls (1–2 lenses, 1 reviewer each)
- **Gate profile:** 1 Agent tool call

architecture-guard is a **separate** skill, invoked independently by Impetus (not inside VFL). It is one additional Agent tool call when pattern drift checking is needed — not part of the VFL reviewer count.

Invocation flow for Full VFL:
```
VFL (flat, main context)
├── Agent tool call 1 → momentum-code-reviewer [structural, reviewer-A] (background)
├── Agent tool call 2 → momentum-code-reviewer [structural, reviewer-B] (background)
├── Agent tool call 3 → momentum-code-reviewer [factual, reviewer-A] (background)
├── Agent tool call 4 → momentum-code-reviewer [factual, reviewer-B] (background)
├── Agent tool call 5 → momentum-code-reviewer [coherence, reviewer-A] (background)
├── Agent tool call 6 → momentum-code-reviewer [coherence, reviewer-B] (background)
├── Agent tool call 7 → momentum-code-reviewer [domain, reviewer-A] (background)
└── Agent tool call 8 → momentum-code-reviewer [domain, reviewer-B] (background)
     ↓ (all complete)
VFL consolidates 8 structured JSON results → sends to Impetus
```


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
| `@modelcontextprotocol/server-git` | MVP | File history, blame, diff for provenance tracking |
| Momentum findings MCP (lightweight, custom) | MVP | Read/write findings-ledger.json as a structured resource |
| `@rlabs-inc/gemini-mcp` | Growth | Multi-model deep research |
| GPT deep research MCP | Growth | Cross-model verification |

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
At every session start, Impetus reads the session ledger and within two exchanges surfaces:
active story/task, current phase, last completed action, suggested next action.
User never hunts for context.

**Decision 4c — Productive Waiting**
While a context:fork subagent runs in background, Impetus maintains dialogue on the same topic.
Background execution (confirmed: Claude Code subagents explicitly support foreground/background modes) means the main conversation is not blocked — Impetus can continue responding to the user while isolated agents run concurrently.
Default: surface implementation summary ("here's what was built and how it maps to the ACs").
Dead air is a failure mode, not an acceptable pause.
**Implementation note:** Background agent execution model is validated in Story 2.Spike (Epic 2) before Stories 2.4 and 4.3 begin. Do not implement productive waiting or background VFL execution until spike result is documented. The execution mode is adopted as the architectural intent; the spike validates the specific implementation mechanism (inter-agent communication + checkpoint/resume). If the spike reveals the mechanism is unavailable, Decision 3a/4c will be revised before Stories 2.4 and 4.3 begin.

---

### Packaging & Deployment

**Decision 5a — Global Rules Deployment: Bundled in Skills, Written by Impetus**
<!-- REVISED: Rules cannot be deployed via npx skills add — confirmed against vercel-labs/skills README compatibility table (2026-03-19). No "Rules" row exists in the table; only Basic skills, allowed-tools, context:fork, and Hooks are listed. Rules deployment via Impetus Write tool is the correct and only mechanism. -->

> _[Changed 2026-03-18 (twice): First from "plugin limitation" to "skills CLI limitation"; then rewritten — rules are bundled inside the skills package and Impetus writes them directly. No separate setup step. Reason: single /momentum entry point; rules travel with the skill.]_
> _[Verified 2026-03-19: Confirmed against live research — npx skills add deploys SKILL.md files only. The vercel-labs/skills compatibility table contains no rules deployment feature. Bundled-and-agent-written is the definitive model.]_

`npx skills add` deploys SKILL.md files only — it cannot write to `~/.claude/rules/` directly. Resolution: rules are bundled inside the momentum skill at `skills/momentum/references/rules/`. Impetus uses `${CLAUDE_SKILL_DIR}` to locate its own skill directory and writes rules to the appropriate targets using the Write tool:

- `~/.claude/rules/` — global rules (all projects for this user)
- `.claude/rules/` — project-scoped rules (this project only)

This happens on first invocation and on upgrade — governed by the manifest/installed state mechanism defined in Decision 5c. No separate CLI, no separate command. The UX interaction pattern (when to prompt, what to show) is defined in the UX specification.

Update mechanism: Impetus compares the hash of installed global rules against the bundled rules in `${CLAUDE_SKILL_DIR}/references/rules/` using git blob SHA — zero extra tooling. See Decision 5c for the full version tracking schema.

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

Two files govern Momentum's install and upgrade lifecycle:

**`skills/momentum/references/momentum-versions.json`** — bundled with the skills package; the authoritative per-version action list. Each version entry contains machine-readable instructions that tell Impetus exactly what to do — not a summary, but executable steps:

```json
{
  "current_version": "1.1.0",
  "versions": {
    "1.0.0": {
      "description": "Initial release",
      "actions": [
        { "action": "write_file", "source": "rules/authority-hierarchy.md",
          "target": "~/.claude/rules/authority-hierarchy.md" },
        { "action": "write_file", "source": "rules/anti-patterns.md",
          "target": "~/.claude/rules/anti-patterns.md" },
        { "action": "write_file", "source": "rules/model-routing.md",
          "target": "~/.claude/rules/model-routing.md" },
        { "action": "write_config", "source": "hooks-config.json",
          "target": ".claude/settings.json", "requires_restart": true },
        { "action": "write_config", "source": "mcp-config.json",
          "target": ".mcp.json", "requires_restart": false }
      ]
    },
    "1.1.0": {
      "description": "Revised authority hierarchy; Findings MCP v2",
      "from": "1.0.0",
      "actions": [
        { "action": "update_file", "source": "rules/authority-hierarchy.md",
          "target": "~/.claude/rules/authority-hierarchy.md",
          "description": "Revised authority precedence rules" },
        { "action": "update_config", "source": "mcp-config.json",
          "target": ".mcp.json",
          "description": "Findings MCP updated to v2",
          "requires_restart": false }
      ]
    }
  }
}
```

**`.claude/momentum/installed.json`** — written to the target project on install; records what version was last applied to THIS project. `npx skills update` updates the package on disk; `installed.json` records what the project has actually been configured for:

```json
{
  "momentum_version": "1.0.0",
  "installed_at": "2026-03-18T00:00:00Z",
  "components": {
    "rules-global":  { "version": "1.0.0", "hash": "<git-blob-sha>" },
    "hooks":         { "version": "1.0.0" },
    "mcp":           { "version": "1.0.0" }
  }
}
```

**Mechanisms:**
- **First install** — no `installed.json` exists; Impetus reads `versions["1.0.0"].actions`, executes each, writes `installed.json`
- **Session-start check** — Impetus reads `current_version` from `momentum-versions.json`; compares against `installed.json.momentum_version`; if they differ, the project needs upgrading
- **Upgrade** — Impetus reads the action list for each version between installed and current; presents to user with description + action per step; executes on confirmation; updates `installed.json`
- **Multi-version gaps** — actions applied sequentially (1.0.0 → 1.1.0 → 1.2.0); each version's changes presented and confirmed as a group
- **Hash comparison** — per-component git blob SHA detects manual drift (user edited an installed file); surfaced as a warning, not a blocker

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

**Skills (flat):**
```
momentum                    ← Entry point only (exception: bare name for /momentum UX)
momentum-[concept]          e.g. momentum-vfl, momentum-upstream-fix
momentum-[verb]-[noun]      e.g. momentum-create-story, momentum-dev-story
```
Lowercase, hyphen-separated, `momentum-` prefix for all skills except the entry point (`momentum`).
BMAD skills retain their existing names — no renaming.

**context:fork skills (verifier/enforcer subagents):**
```
momentum-[role]             e.g. momentum-code-reviewer, momentum-architecture-guard
```
Same `momentum-` prefix as flat skills — distinguished by `context: fork` in SKILL.md frontmatter, not by naming convention.

> _[Changed 2026-03-18: Removed "Plugin skills" and "Agents (.agent.md)" naming sections. code-reviewer and architecture-guard are now `context: fork` SKILL.md files following flat skill naming. Reason: skills-only deployment model.]_

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
name: momentum-[concept]
description: "[One sentence. Action verb. What it does and when to use it.]"
model: claude-sonnet-4-6        # or claude-opus-4-6 for high-stakes outputs
effort: normal                  # normal | high | low
---
```

**Enforcement skills (context:fork) add:**
```yaml
context: fork
disable-model-invocation: true  # prevent accidental auto-trigger of heavy skills
```

**Workflow skills with heavy reference content use `references/` subdirectory:**
```
skills/momentum/
├── SKILL.md              ← Instructions + frontmatter (under 500 lines)
└── references/
    ├── practice-overview.md
    └── phase-guide.md    ← Loaded on demand, not at startup
```

**context:fork skills (verifier/enforcer subagents) MUST include:**

> _[Changed 2026-03-18: Replaced `.agent.md` pattern with `context: fork` SKILL.md pattern. code-reviewer and architecture-guard are now skills, not plugin agents. Reason: skills-only deployment model.]_

```yaml
---
name: momentum-[role]
description: "[What this skill does and when Impetus invokes it — under 150 chars]"
model: claude-opus-4-6          # verifiers get flagship — cognitive hazard rule
context: fork                   # isolated subagent context — no conversation history
allowed-tools: Read             # code-reviewer and architecture-guard: Read only — never Edit, Write, Bash
disable-model-invocation: true  # prevents nested model calls from context:fork peer skills
---
```

**Workflow step files (micro-file architecture for multi-step skills):**
```
skills/momentum-[workflow]/
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

**Findings schema (findings-ledger.json entries):**
```json
{
  "id": "F-[story]-[seq]",        // e.g. F-S04-003
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
<!-- REVISED: plugin/ directory removed; no Unit 1/Unit 2 split. All deployment via skills/. Hooks in settings.json (always-on) and SKILL.md frontmatter (skill-lifecycle). Verified against research (2026-03-19). -->

> _[Changed 2026-03-18: Removed `plugin/` directory entirely. code-reviewer and architecture-guard moved to `skills/` as `context: fork` SKILL.md files. `.claude/settings.json` now carries committed always-on hook definitions. Reason: skills-only deployment model.]_
> _[Verified 2026-03-19: Structure confirmed correct for skills-only deployment. npx skills add installs to .claude/skills/. Non-skills config (rules, hooks-config, mcp-config) bundled in skills/momentum/references/ for Impetus to deploy.]_

```
momentum/                                    ← Root
├── README.md
├── LICENSE
├── CLAUDE.md
├── version.md                               ← Single version source for all skills
│
├── skills/                                  ← All skills: flat + context:fork
│   ├── momentum/
│   │   ├── SKILL.md                         ← Orchestrating agent (flat skill)
│   │   └── references/
│   │       ├── practice-overview.md
│   │       ├── phase-guide.md
│   │       ├── momentum-versions.json       ← Per-version action list (install + upgrade instructions)
│   │       ├── rules/                       ← Bundled rules (written to ~/.claude/rules/ on install)
│   │       │   ├── authority-hierarchy.md
│   │       │   ├── anti-patterns.md
│   │       │   └── model-routing.md
│   │       ├── hooks-config.json            ← Hook config template (written to .claude/settings.json)
│   │       └── mcp-config.json             ← MCP config template (written to .mcp.json)
│   ├── momentum-vfl/
│   │   ├── SKILL.md                         ← Validate-fix-loop orchestrator (flat skill)
│   │   └── references/
│   │       └── vfl-framework-v3.json        ← Dimension taxonomy + profiles
│   ├── momentum-code-reviewer/
│   │   └── SKILL.md                         ← context:fork, allowed-tools: Read — pure verifier
│   ├── momentum-architecture-guard/
│   │   └── SKILL.md                         ← context:fork, allowed-tools: Read — pattern drift detector
│   ├── momentum-upstream-fix/
│   │   ├── SKILL.md
│   │   └── steps/
│   │       ├── step-01-detect.md
│   │       ├── step-02-trace.md
│   │       ├── step-03-solution.md
│   │       └── step-04-verify.md
│   ├── momentum-create-story/
│   │   └── SKILL.md
│   └── momentum-dev-story/
│       └── SKILL.md
│
├── rules/                                   ← Advisory rules source
│   ├── authority-hierarchy.md
│   ├── anti-patterns.md
│   └── model-routing.md
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
    ├── rules/                               ← Project-scoped rules (committed; symlinked from rules/)
    ├── skills/                              ← BMAD skills (managed by BMAD installer)
    └── settings.json                        ← Always-on hook definitions (Tier 1 enforcement; committed)
```

---

### Installed Structure (after `npx skills add` + first `/momentum` invocation)
<!-- REVISED: Removed plugin cache and momentum setup step. npx skills add installs SKILL.md files to .claude/skills/; Impetus writes all config on first /momentum invocation. Verified (2026-03-19). -->

> _[Changed 2026-03-18 (twice): Removed plugin cache; then removed `momentum setup` step — Impetus writes all config files on first run from bundled references/. Reason: single entry point model.]_
> _[Verified 2026-03-19: No momentum setup CLI, no momentum bootstrap CLI. Structure reflects what npx skills add actually installs (.claude/skills/ only) plus what Impetus writes on first invocation.]_

```
~/.claude/                                   ← Global Claude Code config
├── rules/
│   ├── authority-hierarchy.md               ← Written by Impetus on first run (from bundled references/)
│   ├── anti-patterns.md
│   └── model-routing.md
└── skills/
    └── (optional: if installed with -g flag)

[project-root]/
└── .claude/
    ├── skills/
    │   ├── momentum/                ← Installed via npx skills add
    │   ├── momentum-vfl/
    │   ├── momentum-code-reviewer/          ← context:fork skill (pure verifier)
    │   ├── momentum-architecture-guard/     ← context:fork skill (pattern drift)
    │   ├── momentum-upstream-fix/
    │   ├── momentum-create-story/
    │   └── momentum-dev-story/
    ├── settings.json                        ← Always-on hooks (written by Impetus on first run)
    └── momentum/                            ← Per-project Momentum state
        ├── ledger.json                      ← Session ledger (Impetus reads/writes)
        ├── ledger-view.md                   ← Human-readable view (auto-generated)
        ├── findings-ledger.json             ← Quality findings (flywheel writes)
        └── installed.json                   ← Install/upgrade state (version + per-component hashes)
```

---

### Architectural Boundaries

**Read/Write Authority:**

| Component | Reads | Writes |
|---|---|---|
| Impetus | ledger.json, specs (read-only), findings-ledger.json | ledger.json, ledger-view.md |
| code-reviewer | Source code, specs, acceptance tests | findings (via structured output → flywheel) |
| architecture-guard | Source code, rules, architecture doc | pattern drift report (via structured output) |
| VFL | Any artifact being validated, source material | consolidated findings report |
| Flywheel workflow (Epic 6) | findings-ledger.json, rules, specs | findings-ledger.json, rules/, specs |
| Upstream-fix skill (Epic 4, standalone) | session ledger, specs, rules | session ledger only (not findings-ledger.json) |
| Hooks | Filesystem (reads), git status | Terminal output only (never modifies files) |
| ATDD workflow | Gherkin spec | `tests/acceptance/` only |
| Coding agents (dev-story) | Specs, rules, existing code | Source code, unit tests |

**Protection boundaries (PreToolUse blocks writes to):**
- `tests/acceptance/` — acceptance test immutability
- `_bmad-output/planning-artifacts/` — spec authority
- `.claude/rules/` — enforcement rule integrity
- `.claude/momentum/findings-ledger.json` — ledger integrity

---

### Requirements to Structure Mapping
<!-- REVISED: Plugin rows removed. Classification Rule (Plugin vs Flat Skills) eliminated — all deployment is via skills. Hooks/rules/MCP config deployed by Impetus from bundled references/, not by npx skills add. Verified (2026-03-19). -->

> _[Changed 2026-03-18: Removed plugin rows. code-reviewer and architecture-guard now install as `context:fork` skills to `.claude/skills/`. Hooks, rules, and MCP config are bundled in `skills/momentum/references/` and written by Impetus on first run. Reason: skills-only, single-entry-point model.]_
> _[Verified 2026-03-19: Table confirmed correct. No plugin classification — flat skills and context:fork skills are the only two deployment types. Hooks row correctly shows settings.json as target (Impetus-written), not a skills-installed path.]_

| Subsystem | Source File(s) | Installed Location |
|---|---|---|
| Impetus | `skills/momentum/` | `.claude/skills/momentum/` |
| VFL | `skills/momentum-vfl/` | `.claude/skills/momentum-vfl/` |
| Upstream Fix / Flywheel | `skills/momentum-upstream-fix/` | `.claude/skills/momentum-upstream-fix/` |
| code-reviewer | `skills/momentum-code-reviewer/SKILL.md` | `.claude/skills/momentum-code-reviewer/` |
| architecture-guard | `skills/momentum-architecture-guard/SKILL.md` | `.claude/skills/momentum-architecture-guard/` |
| Hook infrastructure (always-on) | `skills/momentum/references/hooks-config.json` | `.claude/settings.json` (written by Impetus on first run) |
| Plan audit gate hook (dev env) | `skills/momentum-plan-audit/scripts/check-plan-audited.sh` | `.claude/settings.json` PreToolUse on ExitPlanMode (project-scoped; deploy story installs globally) |
| Global rules | `skills/momentum/references/rules/*.md` | `~/.claude/rules/` (written by Impetus on first run) |
| Project rules | `skills/momentum/references/rules/*.md` | `.claude/rules/` (written by Impetus on first run) |
| MCP servers | `skills/momentum/references/mcp-config.json` + `mcp/` source | `.mcp.json` (written by Impetus on first run) |
| Session ledger | (runtime) | `.claude/momentum/ledger.json` |
| Findings ledger | (runtime) | `.claude/momentum/findings-ledger.json` |
| Install state | (runtime) | `.claude/momentum/installed.json` |

---

### Integration Points

**Impetus ↔ Subagents:** Structured JSON output contract (`status`, `result`, `question`, `confidence`)

**Impetus ↔ BMAD:** Enhancement at BMAD workflow completion boundaries — one hard gate (acceptance tests before story close) plus user-discretionary proposals at other boundaries

**Skills ↔ Claude Code:** SKILL.md frontmatter matching at startup; full skill loaded on invocation; `references/` loaded on demand

**Hooks ↔ Claude Code:** Defined in `.claude/settings.json` (committed to repo); merge with any existing project hook config automatically on session start

**MCP Servers ↔ Agents:** Git MCP provides file history and blame for provenance; Findings MCP provides structured read/write of findings-ledger.json

**Provenance Scanner ↔ Spec Files:** Reads all `derives_from` frontmatter across the project; computes `referenced_by` graph; compares stored hashes to current `git hash-object`; outputs suspect list to Impetus at session start. Placement: implemented as `references/provenance-scan.md` within `momentum/` — runs as part of session orientation, not a separate skill.

---

## Validation Summary (Steps 7–8)

### Dual-Reviewer Pass Results

Adversarial validation conducted per the dual-reviewer pattern from VFL framework (HANDOFF-BRIEF-001 §Provenance). Enumerator (systematic) + Adversary (failure-focused) passes run against the full document.

**10 findings triaged. All resolved:**

| Finding | Severity | Resolution |
|---|---|---|
| A-1: context:fork + productive waiting contradiction | Revised to Low | Resolved: foreground/background is orthogonal to context:fork isolation. Background subagents confirmed in Claude Code docs. Decision 4c updated. |
| A-2: Global rules auto-load stated as unconditional | High | Fixed: subsystem 4 now states conditional on first `/momentum` invocation — Impetus writes rules to `~/.claude/rules/` on first run; no separate `momentum setup` CLI (eliminated 2026-03-18) |
| A-3: Copied global rules go stale | High | Fixed: update mechanism added to Decision 5a; Impetus surfaces version-drift warning |
| A-4: Plugin-agent invocation assumed, not verified | High | Resolved (2026-03-18): `context: fork` is a SKILL.md frontmatter field, not a plugin-only feature. code-reviewer and architecture-guard are `context: fork` SKILL.md files — no plugin required. Spike eliminated. Plugin model dropped entirely. |
| A-5: VFL reviewer output unbounded | Medium | Fixed: reviewer output bound added to Decision 3a |
| A-6: Gate vs. proposal distinction undefined | Medium | Fixed: Decision 5b table now includes Type column; one hard gate identified |
| E-1: Provenance scanner has no home | Low | Fixed: placed in momentum/references/provenance-scan.md |
| E-2: Custom MCP server has no source location | Low | Fixed: mcp/findings-server/ added to repository structure |
| E-4: Version pre-commit hook type ambiguous | Low | Fixed: clarified as standard git pre-commit hook (Husky/pre-commit framework) |
| A-7: Confidence weighting unresolved | Low | Fixed: implementation-time decision noted in Decision 3b |

### Architecture Status

**Complete.** All 10 subsystems covered, all 6 NFRs addressed, all 10 potential conflict points specified, all adversarial findings resolved. Plugin model eliminated; all deployment via standard Agent Skills only (revised 2026-03-18). Previously-noted plugin-agent invocation spike is resolved — `context: fork` is a SKILL.md feature requiring no plugin.

---

## Sprint Story Lifecycle

> _Added 2026-03-21: Parallel story execution model. Revised 2026-03-21: Unified tracking — Momentum metadata lives in sprint-status.yaml alongside BMAD's development_status. No separate story spec files._

### Story State Machine

Momentum uses BMAD's state machine directly — no parallel states, no translation layer:

```
backlog → ready-for-dev → in-progress → review → done
```

- **`backlog`** — story exists in epics.md but no implementation story file has been created yet
- **`ready-for-dev`** — story file created by `momentum-create-story`, metadata written to `momentum_metadata` section, all `depends_on` stories are `done` (or there are none)
- **`in-progress`** — a `momentum-dev` session has claimed this story and is executing in an isolated git worktree
- **`review`** — implementation complete, ready for code review (set by `bmad-dev-story` inside the worktree)
- **`done`** — story's worktree has been merged to the target branch and cleaned up

This is the **sprint-level lifecycle** — distinct from the implementation phase lifecycle (Spec Review → ATDD → Implement → Code Review → Flywheel) tracked in the session ledger. The two are complementary:
- `development_status` in sprint-status.yaml: where the story is in the sprint cycle
- Session ledger `active_stories` + `phase`: what is being actively worked on in each concurrent session

### Unified Sprint Tracking in sprint-status.yaml

All story tracking lives in `sprint-status.yaml`. Momentum adds a `momentum_metadata` section alongside BMAD's `development_status` — additive, not breaking. BMAD skills only read `development_status` and ignore unknown sections.

```yaml
development_status:
  epic-1: in-progress
  1-1-repository-structure-established: ready-for-dev
  1-2-skills-installable-via-npx-skills-add: backlog
  # ... (BMAD reads only this section)

# Momentum parallel execution metadata — invisible to BMAD skills
momentum_metadata:
  1-1-repository-structure-established:
    depends_on: []                    # story_keys whose development_status must be "done"
    touches:                          # paths likely to need merge conflict review
      - "skills/momentum/"
      - "version.md"
    story_file: "_bmad-output/implementation-artifacts/1-1-repository-structure-established.md"
```

**Schema for each `momentum_metadata` entry:**

| Field | Type | Description |
|---|---|---|
| `depends_on` | list of strings | Story keys (matching `development_status` keys) that must have status `done` before this story can be selected. Empty list `[]` if no dependencies. |
| `touches` | list of strings | Paths this story will create or modify. Used for merge conflict risk assessment — not a blocker. |
| `story_file` | string or null | Path to the full implementation story file (in `_bmad-output/implementation-artifacts/`). Null for process stories that are self-contained. |

`depends_on` is populated at story creation time from the dependency notes in the epics section. `touches` is inferred from the story's implementation scope (skill dirs, shared config files, paths mentioned in tasks).

### Next-Story Selection Rule

When `momentum-dev` is invoked without an explicit story path, it reads `sprint-status.yaml` and selects:
> The highest-priority story where `development_status[key] == "ready-for-dev"` AND all keys in `momentum_metadata[key].depends_on` have `development_status == "done"`

Priority order: epic sprint assignment (Day 1 > Sprint 1 > Sprint 2 > Growth), then story order within that epic (parsed from the key: `1-2-...` → epic 1, story 2).

If no story qualifies (all remaining stories are blocked), `momentum-dev` surfaces the blocked-on list and halts.

### Session Ledger Extension: `active_stories`

The session ledger `active_story` field (singular) extends to `active_stories` (array) to support concurrent sessions:

```json
{
  "active_stories": [
    {
      "story_id": "3.1",
      "worktree_path": ".worktrees/story-3.1",
      "target_branch": "main",
      "phase": "Implement"
    },
    {
      "story_id": "3.2",
      "worktree_path": ".worktrees/story-3.2",
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
