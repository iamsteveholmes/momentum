---
stepsCompleted: [1, 2, 3, 4]
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
    description: "Agent Skills deployment research — plugin vs flat skills, hybrid architecture, BMAD coexistence"
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

1. **Deployment Packaging** — Standard Agent Skills (SKILL.md) as the portable core; Claude Code-specific frontmatter (`context: fork`, `model:`, `effort:`) optimizes for Claude Code while remaining standards-compliant. Hooks and subagents travel via Claude Code Plugin container. One set of SKILL.md files serves all targets.

2. **Provenance Infrastructure** — `derives_from` frontmatter (downstream-only authoring), content hash staleness detection, suspect link flagging (pull-based), auto-generated `referenced_by`, Chain of Evidences prompting, Citations API integration for mechanical grounding.

3. **Hook Infrastructure (Tier 1 Deterministic)** — PostToolUse auto-lint/format, PreToolUse acceptance test directory protection, PreToolUse file protection, PreToolUse git-commit quality gate, Stop conditional quality gate. Complemented by standard git hooks (Husky/pre-commit framework) at the repository level.

4. **Rules Architecture (Tier 3 Advisory)** — Global `~/.claude/rules/` (authority hierarchy, anti-patterns, model routing) + project `.claude/rules/` (architecture conventions, stack-specific standards). Auto-loaded in every session including subagents — the always-present advisory layer.

5. **Subagent Composition** — code-reviewer (read-only tools, pure verifier, never modifies code), architecture-guard (pattern drift detection). Both use `context: fork` for producer-verifier isolation. Hub-and-spoke: Impetus is the sole user-facing voice; subagents return structured output to Impetus for synthesis. Subagents cannot spawn subagents — chains route through main conversation.

6. **Validate-Fix Loop (VFL) Skill** — Three profiles: Gate (1 agent, pass/fail), Checkpoint (2-4 agents, 1 fix attempt), Full (dual-reviewer per lens, up to 4 fix iterations). Four lenses: Structural Integrity, Factual Accuracy, Coherence & Craft, Domain Fitness. Consolidation handles deduplication, cross-check confidence tagging, and scoring. Invocable standalone, inline from workflows, or declared as a rule.

7. **Orchestrating Agent — Impetus** — Session orientation (reads ledger, surfaces active threads), visual progress (✓ Built / → Now / ◦ Next), proactive gap detection, productive waiting during subagent execution, hub-and-spoke voice unification. Impetus is the force that maintains practice velocity — the system keeps compounding because Impetus carries knowledge and context forward across sessions and sprints without requiring repeated external input.

8. **Findings Ledger + Evaluation Flywheel** — Structured findings with provenance_status field; cross-story pattern detection; flywheel workflow (Detection → Review → Upstream Trace → Solution → Verify) with visual status graphics; `/upstream-fix` skill; retrospective integration.

9. **Model Routing** — `model:` and `effort:` frontmatter required on every SKILL.md and agent definition. Cognitive hazard rule: flagship models for outputs without automated validation. Escalation semantics in VFL: mid-tier first, flagship if not converging within 3-4 iterations.

10. **Protocol-Based Integration** — Every integration point (validation, research, review, tools, documents) defines an interface before implementation is wired. Implementations are substitutable: swap the ATDD framework, the research model, the validation profile — the practice layer is unchanged.

---

### Non-Functional Requirements

- **Portability gradient** — Tier 1 (hooks) = Claude Code only; Tier 2 (structured workflows) = partially portable; Tier 3 (rules) = all tools. System degrades gracefully — Cursor gets skills + rules, Claude Code gets full enforcement.
- **Context budget** — Agent Skills three-stage loading (description at startup ~100 tokens, full SKILL.md on invocation, references/ on demand) means startup overhead is manageable with good authoring discipline. Concise descriptions, heavy content in references/. Hygiene note, not a hard constraint.
- **Evolvability (Impermanence Principle)** — Thin packaging layer. Practice portable even if plugin ecosystem changes. Monthly ecosystem review. Interfaces before implementations everywhere.
- **Solo developer efficiency** — One person, limited hours, concurrent with other projects. MVP deploys in days. Real work on real projects is the test harness.
- **Cost as managed dimension** — `model:` + `effort:` frontmatter on every skill. Cognitive hazard rule universal. VFL max 4 iterations (context accumulation makes later iterations progressively more expensive).
- **Terminal-native UX** — No web UI. ASCII/text visual progress. Structured markdown artifacts. Everything works beautifully in a terminal environment.

---

### Scale & Complexity

- **Primary domain:** Developer tooling / practice framework
- **Complexity:** Medium — no regulatory compliance; complexity from multi-tool portability, evolving ecosystem dependencies, and the meta-nature of a practice that governs practices using its own practice
- **Estimated architectural components:** 13 major subsystems
- **Dogfooding as validation:** Momentum is built using its own practice. The system's first test case is itself.

---

### Technical Constraints & Dependencies

- **Claude Code Plugin ecosystem** — pre-1.0 as of March 2026; Impermanence Principle requires thin packaging layer; practice survives packaging changes
- **Agent Skills standard** — SKILL.md format; Claude Code-specific frontmatter silently ignored by other tools; one file, dual behavior by design
- **Subagents cannot spawn subagents** — VFL orchestration chains through main conversation; affects Full-profile parallel execution design
- **context:fork isolation** — Skills/agents using context:fork cannot maintain persona across main-conversation interactions; determines plugin vs. flat skill classification

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
3. **Producer-verifier separation** — context:fork isolation on all review steps. The producing context never reviews its own output.
4. **Model routing** — model: and effort: frontmatter required on every SKILL.md and agent definition. Cognitive hazard rule applies universally.
5. **Visual progress** — ✓ Built / → Now / ◦ Next at every phase transition across all orchestrated workflows.
6. **Protocol interfaces** — Every integration point defines an interface before any implementation is wired.

---

## Deployment Structure

### Classification Rule: Plugin vs. Flat Skills

The defining question for each component: *does this need main-context persona persistence, or does it benefit from isolation?*

| Component | Deployment | Rationale |
|---|---|---|
| Impetus (orchestrating agent) | Flat skill | Must persist persona across interactions |
| upstream-fix, create-story, dev-story | Flat skills | Stateful workflows needing main context |
| code-reviewer | Plugin agent | Pure verifier — isolation is its purpose |
| architecture-guard | Plugin agent | Pattern analysis — isolation prevents drift |
| VFL skill | Plugin skill | Spawns multiple agents, benefits from isolation |
| Hooks | Plugin hooks/hooks.json | Deterministic enforcement requires plugin container |
| Rules | Plugin → ~/.claude/rules/ | Written globally on install, auto-load every session |
| MCP config | Plugin .mcp.json | Bundled alongside enforcement layer |

### Repository Structure

```
momentum/
├── plugin/                          ← Unit 1: Claude Code Plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── agents/
│   │   ├── code-reviewer.agent.md
│   │   └── architecture-guard.agent.md
│   ├── hooks/
│   │   └── hooks.json
│   ├── skills/
│   │   └── vfl/SKILL.md
│   └── .mcp.json
│
├── skills/                          ← Unit 2: Standard Agent Skills (flat)
│   ├── impetus/SKILL.md
│   ├── upstream-fix/SKILL.md
│   ├── create-story/SKILL.md
│   └── dev-story/SKILL.md
│
├── rules/                           ← Unit 3: Always-loaded advisory rules
│   ├── authority-hierarchy.md
│   ├── anti-patterns.md
│   └── model-routing.md
│
└── docs/                            ← Reference content loaded on demand
```

### Install Experience

```bash
# Full Claude Code install
/plugin install momentum/momentum-plugin       # hooks + agents + enforcement skills
npx skills add momentum/momentum-skills -a claude-code  # orchestrating workflows

# Cursor install (skills + rules only)
npx skills add momentum/momentum-skills -a cursor
```

### Version Management

Plugin and flat skills share a single `version.md` at repo root. A pre-commit hook validates they match. Release tags version both units together to prevent drift.

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
- Structured array of findings with fields: `story_ref`, `severity`, `pattern_tags`, `provenance_status`, `phase`, `description`, `evidence`, `upstream_fix_applied`
- Queryable for cross-story pattern detection (same pattern across S-04, S-07, S-11)
- Only flywheel workflow writes findings; read by Impetus at retrospective and upstream trace

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

---

### Agent Communication & Orchestration

**Decision 3a — VFL Parallel Execution: Main Context Orchestration**

The main conversation CAN spawn multiple subagents simultaneously (confirmed: official Claude Code docs explicitly document parallel subagent spawning as a supported pattern). The constraint is only that subagents cannot spawn further subagents.

Architecture:
- **VFL runs as a flat skill** (main context, not context:fork) — orchestration needs main context to spawn agents
- **Impetus invokes VFL** from main conversation
- **VFL spawns all reviewers in parallel** — up to 8 simultaneous subagents (2 per lens × 4 lenses for Full profile)
- **Reviewers are context:fork agents** defined in `plugin/agents/` — isolated, read-only where appropriate
- **VFL consolidates results** in main context after all reviewers complete
- Context window consideration: all reviewer results return to main context; keep reviewer output structured and bounded

Updated deployment: VFL skill moves from `plugin/skills/` to `skills/` (flat skill alongside Impetus).

**Decision 3b — Hub-and-Spoke Voice Contract**
Impetus is the only agent that speaks to the user. All subagents return:
```json
{ "status": "complete | needs_input | blocked", "result": {}, "question": "optional" }
```
Impetus synthesizes into its own voice. Subagent identity never surfaces to user.

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
While a context:fork subagent runs, Impetus maintains dialogue on the same topic.
Default: surface implementation summary ("here's what was built and how it maps to the ACs").
Dead air is a failure mode, not an acceptable pause.

---

### Packaging & Deployment

**Decision 5a — Global Rules Scope: Confirmed Limitation, Accepted**
Claude Code plugins physically cannot write to `~/.claude/rules/` (verified March 17, 2026).
Plugin files go to `~/.claude/plugins/cache/` only; no loose file deployment to any `~/.claude/` subdirectory.

Resolution: Impetus includes a `momentum setup` menu option that interactively copies
`momentum/rules/*` to `~/.claude/rules/` on first run. Project-scoped rules deploy to
`.claude/rules/` automatically. Global rules are a one-time interactive setup, not silent
automation. Promote to automatic if Claude Code plugin capabilities expand.

**Decision 5b — BMAD Enhancement Touch Points (MVP)**
Impetus proactively suggests Momentum enhancements at BMAD workflow boundaries:

| BMAD Event | Momentum Enhancement |
|---|---|
| Any BMAD artifact generated (user selects C) | Impetus proposes `derives_from` frontmatter + git commit |
| BMAD code-review complete | Impetus offers Momentum code-reviewer as additional adversarial pass |
| BMAD dev-story complete | Impetus gates on acceptance tests passing before closing story |
| BMAD retrospective | Impetus adds findings ledger summary to retrospective input |

Long-term: evaluate all BMAD workflows and agents for Momentum enhancement opportunities.
Goal is that running any BMAD workflow inside Momentum automatically inherits provenance,
enforcement, flywheel, and versioning without workflow authors needing to explicitly add it.
