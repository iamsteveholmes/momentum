---
stepsCompleted:
  - step-01-validate-prerequisites
  - step-02-design-epics
  - step-03-epic-1-stories
  - step-03-epic-2-stories-vfl-gate-applied
  - step-03-epic-3-stories-vfl-gate-applied
  - step-03-epic-4-stories-vfl-gate-applied
  - step-03-epic-5-stories-vfl-gate-applied
  - step-03-epic-6-stories-vfl-gate-applied
  - step-03-epic-7-stories-vfl-gate-applied
  - step-03-epic-8-stories-vfl-gate-applied
  - step-03-epic-9-stories-vfl-gate-applied
inputDocuments:
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/ux-design-specification.md
derives_from:
  - id: PRD-MOMENTUM-001
    path: _bmad-output/planning-artifacts/prd.md
    relationship: derives_from
  - id: ARCH-MOMENTUM-001
    path: _bmad-output/planning-artifacts/architecture.md
    relationship: derives_from
  - id: UX-MOMENTUM-001
    path: _bmad-output/planning-artifacts/ux-design-specification.md
    relationship: derives_from
lastEdited: '2026-03-22'
editHistory:
  - date: '2026-03-22'
    changes: 'Added mise as standard tool/runtime manager in Additional Requirements (From PRD — Tool/Runtime Management section); updated Story 7.2 project inspection file list to include mise.toml alongside package.json, build.gradle, pyproject.toml.'
  - date: '2026-03-20'
    changes: 'Synced FR numbering with PRD edits: FR2 updated to solo first-install path; FR2b/FR2c added for Nth-run routing; FR3 decomposed to FR3a/FR3b/FR3c; FR5 updated to team member joining path; NFR1 corrected to ≤150 characters; NFR4 updated to remove plugin reference; Epic 1 FRs covered list updated; FR Coverage Map updated with new FR entries.'
  - date: '2026-03-20'
    changes: 'Validation fix pass: C-01 purged plugin model throughout (Deployment & Packaging block replaced, Spike Required block replaced with Architecture Decision Closed, Epic 1 Additional field updated, Epic 4 Additional field updated, NFR7 updated, NFR10 updated); C-02 renamed configured_for_version → momentum_version in FR2/FR2b/FR2c/FR3b/FR3c; C-05 fixed Story 1.2 AC ≤100 tokens → ≤150 characters; C-06 replaced all Tony references with Impetus throughout (UX-DR6/10/13/18, Epic 2 description, Story 2.1/2.4 ACs); C-16 updated NFR4 label in NFR mapping comment.'
  - date: '2026-03-20'
    changes: 'Propagation fix pass (6 findings): I2-01 FR20 requirements inventory updated with PostToolUse Write/Edit event tracking detail; I2-01 FR20 Coverage Map description updated to include source file change detection via PostToolUse; I2-02 FR37 requirements inventory appended with Impetus dispatch mechanism (reads config at invocation time, looks up protocol binding, invokes implementation); I2-03 NFR7 requirements inventory appended with Tier 3 validation method (README documents all three tiers; principles actionable without tooling); I2-04 FR9 requirements inventory appended with minimum example list (protocol mapping table gaps, missing MCP provider, undefined ATDD tool binding); I2-04 Story 2.5 AC examples updated to include third example (ATDD tool binding undefined) with FR9 pointer; I2-05 Story 1.3 showTurnDuration AC annotated with cost observability trace note; I2-06 Story 1.3 new AC added for installed.json git tracking and gitignore policy.'
  - date: '2026-03-20'
    changes: 'Story 3.3 AC clarification: added And line after conditional test execution AC specifying that the Stop hook detects code modification via session state from PostToolUse Write/Edit events — not git diff or any external check — aligning Story 3.3 with FR20 specified detection mechanism.'
---

# Momentum - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Momentum, decomposing the requirements from the PRD, UX Design, and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

**Installation & Deployment**
FR1: Developer can install Momentum skills via `npx skills add` into any Agent Skills-adopting IDE
FR2: Developer (solo, first install) runs `npx skills add momentum/momentum -a claude-code` then `/momentum`; Impetus detects no `installed.json`, presents pre-consent summary of what will be configured, and with explicit confirmation completes setup and writes `installed.json` recording `momentum_version` (set to the value of `current_version` from `momentum-versions.json`), `installed_at`, and per-component hashes
FR2b: When Impetus starts and `installed.json` exists with `momentum_version` matching `momentum-versions.json` `current_version`, Impetus skips install/upgrade flows and proceeds directly to session orientation
FR2c: When Impetus starts and `installed.json` exists but `momentum_version` does not match `current_version`, Impetus triggers the upgrade flow (FR3b)
FR3a: Developer can run `npx skills update` to pull the latest Momentum package to disk; the updated package contains a revised `momentum-versions.json` with per-version action lists
FR3b: When Impetus starts and detects `momentum-versions.json` `current_version` differs from `installed.json` `momentum_version`, Impetus presents a structured upgrade summary and requires explicit user confirmation before proceeding
FR3c: Impetus executes upgrade actions sequentially across all intermediate versions between `momentum_version` and `current_version`, updating `installed.json` on successful completion; partial failures are reported with the step that failed
FR4: Team member can receive project-level Momentum configuration via `git clone` without manual setup
FR5: Developer joining a project that has `.claude/momentum/installed.json` committed but lacks global Momentum components on their machine runs `/momentum`; Impetus detects missing global components and guides one-time global setup without re-running the full install sequence

**Orchestrating Agent**
FR6: Developer can interact with an orchestrating agent that presents menu-driven access to all practice workflows
FR7: Orchestrating agent can show the developer's current position in any workflow via visual status graphics (ASCII)
FR8: Orchestrating agent can provide human-readable summaries of what was built during implementation, while review runs
FR9: Orchestrating agent can detect ambiguous or missing project configuration and guide the developer through resolution conversationally, including at minimum: gaps in the protocol mapping table (FR35), missing MCP provider configuration, and undefined ATDD tool binding
FR10: Orchestrating agent can contextualize specifications just-in-time — explaining relevant architectural decisions, acceptance criteria, and prior choices at the moment they're needed
FR11: Developer can ask follow-up questions during any workflow step, and the agent treats questions as discovery opportunities

**Provenance & Traceability**
FR12: Developer can declare `derives_from` relationships in document frontmatter, tracing each document to its upstream sources
FR13: System can detect staleness via hash-based (internal docs) and time-based (edge docs) modes; stale downstream documents flagged as SUSPECT, one-hop propagation only, human/verifier-gated at each level
FR14: System can auto-generate backward references (`referenced_by`) from forward `derives_from` declarations — no manual maintenance
FR15: Top-level specification documents can self-identify via frontmatter marker, enabling specification tree discovery
FR16: Developer can track provenance status of claims (VERIFIED, CITED, INFERRED, UNGROUNDED, SUSPECT)
FR17: System can distinguish human-authored from AI-generated content in provenance metadata

**Enforcement & Quality Governance**
FR18: System can auto-lint and auto-format code on every file edit (PostToolUse hook)
FR19: System can block modifications to acceptance test directories (PreToolUse hook)
FR20: System can run conditional quality gates before session end — tests only when any source file outside `tests/acceptance/` was written or edited during the current session (detectable via PostToolUse Write/Edit event tracking in session state), lint always (Stop hook)
FR21: System can protect specified files from modification (PreToolUse hook)
FR22: System can ensure authority hierarchy rules auto-load in every Claude Code session including subagents via `.claude/rules/`
FR23: Developer can configure model routing defaults per skill and agent via `model:` and `effort:` frontmatter, with documented default strategy (Sonnet 4.6 general, Opus for complex/cognitive-hazard, Haiku for constrained tasks with downstream validation)

**Verification & Review**
FR24: Code-reviewer subagent can perform adversarial review with read-only tools, producing structured findings reports
FR25: Code-reviewer can be prompted or triggered automatically at implementation completion, not requiring manual invocation
FR26: Findings reports can include provenance status for traceability-dimension findings
FR27: Every finding requires evidence — validators cannot generate findings without supporting evidence from the reviewed artifact

**Evaluation Flywheel**
FR28: Findings ledger can accumulate findings across stories with category, root cause classification, and upstream level
FR29: System can detect cross-story patterns in the findings ledger and surface systemic issues
FR30: Flywheel can explain detected issues and suggest upstream trace with visual workflow status (detection → review → upstream trace → solution → verify → log)
FR31: Developer can approve or reject each flywheel suggestion — the agent never proceeds without explicit consent
FR32: Upstream fixes can be applied at any level: spec-generating workflow, specification, CLAUDE.md/rules, tooling, or one-off code fix
FR33: System can track the ratio of upstream fixes to code-level fixes as a practice health metric

**Protocol-Based Integration**
FR34: Developer can configure which agent, skill, tool, MCP provider, or document structure satisfies each protocol — at project level
FR35: Project configuration file maps protocols to implementations with provenance (who configured, when, why)
FR36: Orchestrating agent can read the project configuration, detect gaps in protocol mappings, and help fill them conversationally
FR37: System can resolve workflow step invocations through protocol interfaces — workflow definitions reference protocol types, not specific implementations; Impetus reads the project configuration at invocation time, looks up which implementation satisfies the protocol type for the current step, and invokes that implementation
FR38: Developer can substitute any protocol implementation without modifying the workflows that depend on it

**Specification & Development Workflow**
FR39: Developer can define acceptance criteria in Gherkin format that is behavioral, technology-agnostic, and implementation-independent
FR40: ATDD workflow can generate failing acceptance tests from Gherkin criteria before implementation begins
FR41: Developer can complete a full story cycle guided by the orchestrating agent: spec review → ATDD → implement → review → flywheel
FR42: System can track visual progress through the story cycle, always showing current phase and next phase
FR43: Developer can invoke the upstream fix skill to analyze a quality failure and propose corrections at the appropriate upstream level

**Research & Knowledge Management**
FR44: Developer can conduct multi-model research using MCP-integrated LLM providers (Gemini, GPT, and additional providers)
FR45: System can enforce date-anchoring and primary-source directives in research agent prompts
FR46: Developer can archive outdated documents to a designated directory while preserving their reference chain
FR47: System can track document freshness using domain-specific freshness windows (90 days AI/LLM, 6 months tooling, 12 months standards, 24 months principles)

### NonFunctional Requirements

**Context Window & Token Economics**
NFR1: Each Momentum skill description must be ≤150 characters to minimize startup context budget impact
NFR2: Skill matching accuracy must remain ≥95% when Momentum skills coexist with 68+ BMAD skills
NFR3: Skill instructions should stay under 500 lines / 5000 tokens per Agent Skills spec recommendation
NFR4: All Momentum skills are flat skills deployed via Agent Skills standard; no plugin namespacing is used or required

**Portability & Graceful Degradation**
NFR5: All SKILL.md files must be valid Agent Skills standard — parseable by any of the 17+ adopting tools
NFR6: Claude Code-specific frontmatter must be additive — skills must function correctly when ignored by non-Claude Code tools
NFR7: Enforcement must degrade across three defined tiers: Tier 1 full deterministic (Claude Code — hooks fire via `.claude/settings.json` written by Impetus, subagents enforce via `context:fork` skills, rules auto-load via `.claude/rules/` written by Impetus), Tier 2 advisory (Cursor/other tools with skills only), Tier 3 philosophy only (no tooling). Each tier explicitly tested. Tier 3 validated by: verifying the README documents all three enforcement tiers and their respective capabilities and limitations; confirming that the practice principles are documented in a form that is actionable without any tooling installation.
NFR8: No Momentum workflow definition may import or reference a Claude Code-specific API directly — workflows depend on protocol interfaces

**Ecosystem Resilience**
NFR9: A breaking change in any single ecosystem dependency must be absorbable by modifying only the packaging/distribution layer, not practice content
NFR10: All ecosystem dependencies (BMAD version, Agent Skills spec version) must be tracked and reviewed monthly
NFR11: Packaging/distribution layer must comprise ≤5% of total Momentum files (by count); replacing the entire packaging mechanism must not require changes to any skill instruction, rule, or agent definition file

**Integration Compatibility**
NFR12: Momentum skills must coexist with BMAD skills in `.claude/skills/` without namespace conflicts or matching interference
NFR13: Momentum hooks must merge cleanly with existing project and BMAD hooks — no silent override
NFR14: MCP provider integrations must respect Cursor's ~40 active tool ceiling in Cursor environments
NFR15: Protocol implementations must satisfy documented interface contracts — substituting any implementation with a contract-satisfying alternative must not cause any consuming workflow to fail

**Dogfooding Integrity**
NFR16: Every Momentum feature must be validated by real use on at least one active project before considered stable; each feature's release notes reference the project(s) and story cycle(s) where it was dogfooded
NFR17: Meta-risk (system amplifying its own blind spots via dogfooding) must be mitigated by external validation: adversarial review by separate context, multi-model research cross-checking, and explicit human checkpoints at critical decisions

### Additional Requirements

**From Architecture — Deployment & Packaging**
- Starter template: No starter template specified. Momentum is greenfield — Epic 1 Story 1 establishes the repository structure per the architecture's documented layout (skills/, rules/, mcp/, docs/)
- All skills are flat skills deployed via `npx skills add momentum/momentum -a claude-code`; no plugin directory
- `context:fork` is a SKILL.md frontmatter feature; code-reviewer and architecture-guard are `context:fork` SKILL.md files, not plugin agents
- Rules, hooks config, and MCP config are bundled in `skills/momentum/references/` and written by Impetus on first `/momentum` invocation
- Version tracking: `momentum-versions.json` (per-version action list, bundled in package) + `.claude/momentum/installed.json` (project state, committed to repo)
- Single entry point: `/momentum` command
- Impetus must surface a version-drift warning at session start when installed global rules hash differs from current version's rules hash

**From Architecture — Storage & State**
- Session journal stored at `.claude/momentum/journal.json`; auto-generated `.claude/momentum/journal-view.md` for human readability
- Findings ledger stored at `~/.claude/momentum/findings-ledger.jsonl` (global, JSONL append-only) with structured schema: id, project, story_ref, phase, severity, pattern_tags, description, evidence, provenance_status, upstream_fix_applied, upstream_fix_level, upstream_fix_ref, timestamp
- Only the flywheel workflow writes to findings ledger; Impetus reads at retrospective and upstream trace

**From PRD — Tool/Runtime Management**
- mise is the standard polyglot tool/runtime manager for developer environments using Momentum. When Momentum skills, workflows, or rules reference installing runtimes (node, python, ruby, go, java) or CLI tools, they must prefer `mise use` over legacy single-purpose managers (nvm, pyenv, rbenv, asdf, volta, fnm) or global package installs (`npm install -g`, `pip install --user`). Enforced by global Claude Code rules (`~/.claude/rules/mise.md`) and the anti-patterns rule. Momentum does not bundle or install mise itself — it is a prerequisite of the developer environment.

**From Architecture — Security & File Protection**
- PreToolUse hook must block writes to: `tests/acceptance/` and `**/*.feature`, `_bmad-output/planning-artifacts/*.md`, `.claude/rules/`. Findings ledger (`~/.claude/momentum/findings-ledger.jsonl`) is authority-enforced (global path, outside PreToolUse scope).
- Agents may not remove or modify `derives_from` frontmatter in spec files
- Every significant claim classified as SOURCED / DERIVED / ADDED / UNGROUNDED

**From Architecture — MCP Servers**
- Deferred (Epic 6): Momentum findings MCP (custom, lightweight — optional read-only query layer over `~/.claude/momentum/findings-ledger.jsonl`). ~~`@modelcontextprotocol/server-git`~~ removed (p1.1) — git CLI provides file history, blame, and diff via Bash tool
- Growth: `@rlabs-inc/gemini-mcp` and GPT deep research MCP for multi-model research

**From Architecture — VFL Skill**
- VFL deployed as flat skill (`momentum-vfl/SKILL.md`) alongside Impetus
- VFL orchestrates parallel reviewer spawning from main context (confirmed pattern per Claude Code docs)
- Reviewers are context:fork agents; return structured JSON (not free-form prose) per vfl-framework-v3.json output schema
- VFL consolidates findings in main context; context accumulation bounded by structured output contract
- Execution mode: background (non-blocking) during interactive workflows; foreground acceptable for hook-triggered passes

**From Architecture — Architecture Decision Closed**
- The plugin-agent invocation spike (previously open) is resolved: `context: fork` is a SKILL.md frontmatter feature requiring no plugin. code-reviewer and architecture-guard are implemented as `context:fork` SKILL.md files with `allowed-tools: Read`.

**From Architecture — BMAD Integration**
- BMAD enhancement touchpoints at MVP: (1) Any BMAD artifact generated → Impetus proposes derives_from frontmatter + git commit [Proposal]; (2) BMAD code-review complete → Impetus offers Momentum code-reviewer as additional adversarial pass [Proposal]; (3) BMAD dev-story complete → Impetus gates on acceptance tests passing before closing story [Gate — the only hard gate at MVP]; (4) BMAD retrospective → Impetus adds findings ledger summary [Proposal]

### UX Design Requirements

UX-DR1: Implement Session Journal Display component — numbered list of open threads with workflow phase + elapsed time; appears at every session start with open threads; absent on first-time user (no journal exists). States: single thread, multiple threads, empty (first time).

UX-DR2: Implement Progress Indicator component — always exactly 3 lines using ✓/→/◦ symbol vocabulary; completed steps collapse to single ✓ line with value summary; current step stands alone with one-phrase description; upcoming steps collapse to single ◦ line. Appears at workflow entry and every phase transition.

UX-DR3: Implement Hook Announcement component — pass: one-line `[hook-name] ✓ checked [what] — [result]`; fail: hook name + specific issue + file:line + likely cause. Never silent, never verbose. Every hook, every fire.

UX-DR4: Implement Workflow Step component — orientation line (never "step N/M"), substantive content, transition signal, explicit user control [A/P/C or equivalent]. Most frequent pattern in the system.

UX-DR5: Implement Completion Signal component — explicit ownership return ("this is yours to review and adjust"), what was produced (file list), what's next question. Every story cycle and workflow completion must use this.

UX-DR6: Implement Subagent Return component — Impetus's voice synthesizes subagent findings; severity indicators (! critical, · minor); critical findings surface flywheel trigger. User never sees raw subagent output.

UX-DR7: Implement Flywheel Notice component — surfaced after upstream fix applied; shows finding, root cause, fix applied, what it prevents. Makes invisible improvement visible.

UX-DR8: Implement Proactive Orientation component — surfaces knowledge gap or about-to-be-skipped step detection; offers, never blocks; decision always returned to user. Fires only when conversational floor is open.

UX-DR9: Implement consistent Symbol Vocabulary across all agents and hooks: ✓ completed/passing, → current/active, ◦ upcoming/pending, ! warning/attention, ✗ failed/blocked, ? question/decision. Symbols always paired with text — meaning must survive any rendering context.

UX-DR10: Implement Hub-and-Spoke Voice Contract — Impetus is the sole user-facing voice; all subagents return structured JSON `{status, result, question, confidence}`; subagent identity never surfaces to user; Impetus synthesizes before presenting.

UX-DR11: Implement Session Orientation Contract — at every session start, Impetus reads journal and within two exchanges surfaces: active story/task, current phase, last completed action, suggested next action. Agent speaks first; user never hunts for context.

UX-DR12: Implement Productive Waiting pattern — while a background subagent runs, Impetus maintains dialogue on the same topic (never context-switches). Dead air is a failure mode. Brief acknowledged pauses acceptable for very short tasks only.

UX-DR13: Implement Multi-Thread Journal Awareness — each Impetus instance (per Claude Code tab) reads/writes the shared journal; recently-timestamped entries signal intentional concurrent work; conflicting thread starts flagged with user decision required.

UX-DR14: Implement Thread Hygiene — surface dormant threads beyond a threshold; low-friction closure (one confirmation); contextually triggered when dependent work completes or journal grows unwieldy.

UX-DR15: Implement Response Architecture Pattern — every agent response follows: orientation line → substantive content → transition signal → user control. Orientation line is narrative (never "step N/M"); user control always last and always visible.

UX-DR16: Implement Input Interpretation patterns — number selects journal item; letter command is case-insensitive; fuzzy match (continue/yes/go ahead = C); natural language extracts intent and confirms; ambiguous input triggers one clarifying question (never two).

UX-DR17: Implement Workflow Resumability — every workflow must be resumable from any step; sufficient context saved in journal entry to re-orient a fresh agent session without user re-explanation. Step re-entry after interruption always confirms ("continue from here, or restart this step?").

UX-DR18: Impetus agent persona voice — "guide's voice": oriented, substantive, forward-moving. Synthesizes before delivering. Returns agency explicitly at completion. Acknowledges uncertainty honestly. Never: generic praise ("Great!"), numeric progress ("Step 3/8"), visible agent machinery. Surface name and implementation name: Impetus.

### FR Coverage Map

| FR | Epic | Description |
|---|---|---|
| FR1 | Epic 1 | Install skills via npx skills add |
| FR2 | Epic 1 | Solo developer first-install path: detect no installed.json, present pre-consent summary, complete setup on confirmation |
| FR2b | Epic 1 | Current version match → skip install/upgrade, proceed to session orientation |
| FR2c | Epic 1 | Version mismatch → trigger upgrade flow (FR3b) |
| FR3a | Epic 1 | npx skills update pulls latest package with revised momentum-versions.json |
| FR3b | Epic 1 | Detect version drift, present structured upgrade summary, require explicit confirmation |
| FR3c | Epic 1 | Execute upgrade actions sequentially across intermediate versions; report partial failures |
| FR4 | Epic 1 | Project config received via git clone |
| FR5 | Epic 1 | Team member joining path: detect missing global components on machine, guide one-time global setup |
| FR6 | Epic 2 | Orchestrating agent with menu-driven workflow access |
| FR7 | Epic 2 | Visual status graphics (ASCII) for workflow position |
| FR8 | Epic 2 | Human-readable implementation summaries during review |
| FR9 | Epic 2 | Detect and resolve ambiguous project configuration conversationally |
| FR10 | Epic 2 | Just-in-time spec contextualization |
| FR11 | Epic 2 | Follow-up questions treated as discovery opportunities |
| FR12 | Epic 5 | derives_from frontmatter declarations |
| FR13 | Epic 5 | Staleness detection (hash-based + time-based) |
| FR14 | Epic 5 | Auto-generated referenced_by from derives_from |
| FR15 | Epic 5 | Top-level spec self-identification via frontmatter |
| FR16 | Epic 5 | Provenance status tracking (VERIFIED/CITED/INFERRED/UNGROUNDED/SUSPECT) |
| FR17 | Epic 5 | Human vs AI-generated content distinction in provenance |
| FR18 | Epic 3 | Auto-lint and auto-format on every file edit (PostToolUse hook) |
| FR19 | Epic 3 | Block modifications to acceptance test directories (PreToolUse hook) |
| FR20 | Epic 3 | Conditional quality gates before session end — source file change detection via PostToolUse event tracking (Stop hook) |
| FR21 | Epic 3 | File protection via PreToolUse hook |
| FR22 | Epic 3 | Authority hierarchy rules auto-load via .claude/rules/ |
| FR23 | Epic 3 | Model routing via model: and effort: frontmatter |
| FR24 | Epic 4 | Code-reviewer adversarial review with read-only tools |
| FR25 | Epic 4 | Code-reviewer triggered automatically at implementation completion |
| FR26 | Epic 4 | Findings reports include provenance status |
| FR27 | Epic 4 | Every finding requires evidence from the reviewed artifact |
| FR28 | Epic 6 | Findings ledger accumulates across stories |
| FR29 | Epic 6 | Cross-story pattern detection |
| FR30 | Epic 6 | Flywheel explains issues and suggests upstream trace with visual status |
| FR31 | Epic 6 | Developer approves/rejects each flywheel suggestion |
| FR32 | Epic 6 | Upstream fixes applied at any level |
| FR33 | Epic 6 | Ratio of upstream to code-level fixes as practice health metric |
| FR34 | Epic 7 | Developer configures protocol implementations at project level |
| FR35 | Epic 7 | Project config maps protocols to implementations with provenance |
| FR36 | Epic 7 | Impetus reads config, detects gaps, helps fill them conversationally |
| FR37 | Epic 7 | Workflow steps resolve through protocol interfaces, not specific implementations |
| FR38 | Epic 7 | Substitute any protocol implementation without modifying consuming workflows |
| FR39 | Epic 4 | Gherkin acceptance criteria — behavioral, technology-agnostic |
| FR40 | Epic 4 | ATDD workflow generates failing acceptance tests from Gherkin |
| FR41 | Epic 4 | Full story cycle guided by orchestrating agent |
| FR42 | Epic 4 | Visual progress through story cycle (current phase + next phase) |
| FR43 | Epic 4 | Upstream fix skill analyzes quality failure and proposes correction |
| FR44 | Epic 8 | Multi-model research via MCP-integrated providers |
| FR45 | Epic 8 | Enforce date-anchoring and primary-source directives in research prompts |
| FR46 | Epic 8 | Archive outdated documents while preserving reference chain |
| FR47 | Epic 8 | Track document freshness using domain-specific freshness windows |

**NFR mapping:** NFR1–3 (context/token budget) → Epic 1 & 2. NFR4 (flat skills deployment — no plugin namespacing required) → Epic 1. NFR5–8 (portability/degradation) → Epic 1. NFR9–11 (ecosystem resilience) → Epic 1. NFR12–15 (integration compatibility) → Epic 1. NFR16–17 (dogfooding integrity) → cross-cutting, applied across all epics.

## Epic List

### Epic 1: Foundation & Bootstrap
A developer installs Momentum from scratch — global practice files in place, project bootstrapped, all structure scaffolded by the module. Epic 2 onwards can start.
**FRs covered:** FR1, FR2, FR2b, FR2c, FR3a, FR3b, FR3c, FR4, FR5
**NFRs covered:** NFR1–15 (NFR14–15 co-covered with Epic 7) (portability, resilience, compatibility, token budget architecture decision)
**Additional:** Repo structure, skills/rules layout, version.md, cost observability (showTurnDuration, ccusage recommendation)
**Priority:** Day 1

---

### Epic 2: Stay Oriented with Impetus
A developer always knows where they are and what to do next. Session journal tracks open threads across tabs and sessions. Visual progress answers "what have we built, what are we doing, what's next" at every transition. Impetus's unified voice keeps backstage invisible.
**FRs covered:** FR6, FR7, FR8, FR9, FR10, FR11
**NFRs covered:** NFR1, NFR2, NFR3
**UX-DRs covered:** UX-DR1, UX-DR2, UX-DR4, UX-DR5, UX-DR6 (partial), UX-DR8 (partial), UX-DR9, UX-DR10, UX-DR11, UX-DR12, UX-DR13, UX-DR14, UX-DR15, UX-DR16, UX-DR17, UX-DR18
**Priority:** Day 1

---

### Epic 3: Automatic Quality Enforcement
Quality gates fire without developer intervention. Lint and format run on save. Acceptance tests are protected from modification. Model routing is configured by frontmatter so every skill and agent uses the right model by default. Authority hierarchy rules auto-load every session.
**FRs covered:** FR18, FR19, FR20, FR21, FR22, FR23
**NFRs covered:** NFR7, NFR8
**UX-DRs covered:** UX-DR3
**Additional:** Model routing strategy (PT-016): model-routing-guide.md, model/effort frontmatter on all skills/agents, model-routing.md rule
**Priority:** Sprint 1

---

### Epic 4: Complete Story Cycles
A developer completes a full story cycle guided by Impetus — spec → ATDD → implement → code review → VFL validation — with every handoff driven by the agent. The developer never needs to know the next command; the agent tells them.
**FRs covered:** FR24, FR25, FR26, FR27, FR39, FR40, FR41, FR42, FR43
**UX-DRs covered:** UX-DR6, UX-DR8
**Additional:** code-reviewer (`context:fork` skill, `allowed-tools: Read`), VFL flat skill (momentum-vfl), create-story skill, dev-story skill (includes ATDD workflow capability — ATDD is not a separate deployed skill)
**Priority:** Sprint 1

---

### Epic 5: Trust Artifact Provenance
A developer can trace every artifact to its origins, detect stale references, and know the confidence level of every significant claim. The provenance graph is maintained in frontmatter — no external tooling required.
**FRs covered:** FR12, FR13, FR14, FR15, FR16, FR17
**Additional:** derives_from frontmatter format, content hash staleness (git hash-object), referenced_by auto-generation, provenance scanner (in Impetus references/)
**Priority:** Sprint 1–2

---

### Epic 6: The Practice Compounds
Findings accumulate across stories. Systemic patterns surface. Upstream fixes are applied at the right level — spec, rule, workflow, or one-off patch. Each sprint the practice gets measurably smarter. The flywheel makes invisible improvement visible.
**FRs covered:** FR28, FR29, FR30, FR31, FR32, FR33
**UX-DRs covered:** UX-DR7
**Additional:** findings-ledger.jsonl (global, with full schema), upstream-fix skill (momentum-upstream-fix), flywheel workflow, Momentum findings MCP server (optional query layer)
**Priority:** Sprint 2

---

### Epic 7: Bring Your Own Tools
A developer configures which agent, model, test framework, or MCP provider satisfies each protocol. Swapping any component doesn't touch workflow definitions. The practice layer is unchanged even when the tooling changes underneath it.
**FRs covered:** FR34, FR35, FR36, FR37, FR38
**NFRs covered:** NFR14, NFR15
**Priority:** Sprint 2

---

### Epic 8: Research & Knowledge Management
A developer runs multi-model research with freshness guarantees. Research prompts are date-anchored. Documents have domain-specific freshness windows. Outdated docs are archived with their reference chain intact.
**FRs covered:** FR44, FR45, FR46, FR47
**Additional:** Gemini MCP + GPT MCP integration (growth), hybrid research workflow (PT-020), freshness windows per domain
**Priority:** Growth

---

### Epic 9: Performance Validation
The model routing decisions made in earlier epics are validated empirically. The benchmarking harness measures real task performance across models so routing rules are grounded in evidence, not just judgment.
**Scope:** PT-022 — promptfoo config, bash benchmarking script, golden dataset starter, Pydantic AI harness with agent.override(), updated model/effort frontmatter based on results
**Priority:** Growth (requires Epics 2–4 to have real skills to benchmark)

---

## Epic 1: Foundation & Bootstrap

A developer installs Momentum from scratch — global practice files in place, project bootstrapped, all structure scaffolded through Impetus. Everything subsequent depends on this.

### Story 1.1: Repository Structure Established

As a Momentum contributor,
I want the repository to have the correct directory structure,
So that all components can be developed, tested, and packaged from the right locations.

**Acceptance Criteria:**

**Given** the Momentum repository is cloned
**When** the developer inspects the root directory
**Then** the following directories exist: `skills/`, `rules/`, `mcp/`, `docs/`
**And** `version.md` exists at repo root as the single version source of truth
**And** no `plugin/` directory exists — all deployment is via `skills/`
**And** `skills/momentum/references/momentum-versions.json` exists and contains valid JSON with `current_version` string and `versions` object where each version entry has a non-empty `actions` array
**And** each action in `momentum-versions.json` contains at minimum: `action` (string), `source` (string), `target` (string)
**And** `skills/momentum/references/hooks-config.json` exists and contains valid JSON with at least one hook entry
**And** `skills/momentum/references/mcp-config.json` exists and contains valid JSON

**Given** the repository structure
**When** a contributor adds a new Momentum skill
**Then** it is placed under `skills/momentum-[concept]/SKILL.md`
**And** any content exceeding 500 lines or 5000 tokens goes in `skills/momentum-[concept]/references/`

---

### Story 1.2: Skills Installable via `npx skills add`

As a developer,
I want to install all Momentum skills with a single command,
So that Impetus and all supporting skills are available in my Claude Code environment immediately.

**Acceptance Criteria:**

**Given** a developer has Claude Code installed
**When** they run `npx skills add momentum/momentum -a claude-code`
**Then** all Momentum SKILL.md files are installed to `.claude/skills/`
**And** each skill's `references/` content is bundled and accessible at runtime
**And** Momentum skill names are prefixed `momentum-` (except the entry point `momentum`) so no naming collision with BMAD skills is possible

**Given** the installed skills
**When** Claude Code starts
**Then** each Momentum skill description is ≤150 characters
**And** the correct Momentum skill is invoked on first attempt when tested manually alongside BMAD skills (validated by spot-check during dogfooding per NFR16)

**Given** the installed skills in a non-Claude Code tool (e.g. Cursor)
**When** the tool parses the SKILL.md files
**Then** all SKILL.md files parse without error as valid Agent Skills standard files
**And** Claude Code-specific frontmatter (`context: fork`, `model:`, `effort:`) is silently ignored and does not cause parse failure

---

### Story 1.3: First `/momentum` Invocation Completes Setup

As a developer,
I want invoking `/momentum` for the first time to automatically configure my environment,
So that I never have to run a separate setup command or manually edit config files.

**Acceptance Criteria:**

**Given** a developer has run `npx skills add` but `.claude/momentum/installed.json` does not exist in the project
**When** they invoke `/momentum` for the first time
**Then** Impetus reads `momentum-versions.json` from its own bundled `references/` directory
**And** detects the absence of `installed.json` — identifies this as a first install
**And** presents the developer with a summary of all files that will be written before taking any action
**And** waits for explicit developer approval before proceeding
**And** if the developer declines, Impetus explains that setup is required for full functionality, offers to run it again later, and proceeds to session orientation in a degraded state

**Given** the developer approves the setup summary
**When** Impetus executes the first-install actions
**Then** rules files are written to `~/.claude/rules/` from bundled `references/rules/`
**And** hooks config is **merged** into `.claude/settings.json` — existing keys are preserved, only Momentum-specific hook entries are added, no existing hooks are overwritten or removed
**And** `.mcp.json` is written from bundled `references/mcp-config.json`
**And** `showTurnDuration: true` is set in `.claude/settings.json` (cost observability — Epic 1 Additional requirement)
**Note:** This is an Epic 1 Additional Requirement — no PRD FR; implementation authority is Epic 1 Additional section.
**And** `.claude/momentum/installed.json` is written recording `momentum_version`, `installed_at`, and a hash for each written component
**And** Impetus confirms to the developer exactly which files were written

**Given** setup is run again (e.g. developer deleted `installed.json` to force re-setup)
**When** Impetus executes the first-install actions a second time
**Then** the result is identical to the first run — no duplicate hook entries, no file corruption

**Given** setup completes
**When** the developer starts a new Claude Code session
**Then** rules in `~/.claude/rules/` auto-load in every session including subagents
**And** always-on hooks (PostToolUse lint, PreToolUse file protection, Stop gate) are active in `.claude/settings.json`

**Given** `.claude/momentum/installed.json` already exists and its version matches `current_version` in `momentum-versions.json`
**When** `/momentum` is invoked
**Then** Impetus skips setup entirely and proceeds directly to session orientation

**Given** a second team member clones a project where Impetus has already run setup
**When** they run `npx skills add` and invoke `/momentum`
**Then** Impetus reads the existing `installed.json` committed to the repo
**And** detects that project-level config is already present
**And** only runs global setup steps (rules to `~/.claude/rules/`) if those are missing from the new machine
**And** does not re-write project-level config already committed to the repo

**Given** setup has completed and `.claude/momentum/installed.json` has been written
**When** the developer inspects the project's version control state
**Then** `.claude/momentum/installed.json` is tracked in git (not gitignored)
**And** `.gitignore` does not contain an entry excluding `.claude/momentum/installed.json`

---

### Story 1.4: Momentum Detects and Applies Upgrades

As a developer,
I want Impetus to detect when my Momentum installation is out of date and guide me through upgrading,
So that I always have the latest rules, hooks, and config without manual intervention.

**Acceptance Criteria:**

**Given** a developer runs `npx skills update` and the package `current_version` in `momentum-versions.json` advances
**When** they next invoke `/momentum`
**Then** Impetus compares `installed.json` `momentum_version` against `momentum-versions.json` `current_version`
**And** detects a version mismatch
**And** presents a summary of what changed in each intermediate version before applying anything
**And** on approval, applies version actions sequentially through each intermediate version (e.g. 1.0.0 → 1.1.0 → 1.2.0 — not a direct diff from installed to current)
**And** each intermediate version's actions are presented and confirmed as a group
**And** hook updates are merged into `.claude/settings.json` — existing non-Momentum hooks are never removed
**And** updates `installed.json` with the new version and updated component hashes

**Given** the hash of installed rules in `installed.json` differs from the hash of the bundled rules
**When** `/momentum` is invoked
**Then** Impetus surfaces a version-drift warning at session start
**And** offers to re-apply the rules — developer decides whether to proceed

---

### Story 1.5: Enforcement Degrades Gracefully Across Tool Tiers

As a developer,
I want Momentum's enforcement tiers to be explicitly defined and behave as documented at each tier,
So that teams using any tool can adopt Momentum at the level their environment supports.

**Acceptance Criteria:**

**Given** Momentum skills installed in Cursor via `npx skills add`
**When** a developer invokes a Momentum skill
**Then** skill instructions execute at advisory level — guidance is provided but not enforced
**And** `context: fork` frontmatter is silently ignored (Claude Code-exclusive per skills compatibility table)
**And** the developer is not required to take any additional action for skills to function

**Given** Momentum installed in Claude Code (Tier 1)
**When** a developer uses any Momentum workflow
**Then** Tier 1 full deterministic enforcement is active: hooks fire automatically, rules auto-load, subagents enforce quality
**And** this is explicitly documented in the README as Tier 1

**Given** no tooling at all (Tier 3)
**When** a developer reads the Momentum README
**Then** all three enforcement tiers are defined: Tier 1 (Claude Code — full deterministic), Tier 2 (Cursor/other tools with skills — advisory), Tier 3 (no tooling — philosophy/documentation only)
**And** each tier lists what works and what does not
**And** instructions for adopting at each tier are present

---

## Epic 2: Stay Oriented with Impetus

A developer always knows where they are and what to do next. Session journal tracks open threads across tabs and sessions. Visual progress answers "what have we built, what are we doing, what's next" at every transition. Impetus's unified voice keeps backstage invisible.

**FRs covered:** FR6, FR7, FR8, FR9, FR10, FR11
**NFRs covered:** NFR1, NFR2, NFR3
**UX-DRs covered:** UX-DR1, UX-DR2, UX-DR4, UX-DR5, UX-DR6, UX-DR8 (partial — proactive-offer pattern introduced; fully exercised in Epic 4), UX-DR9, UX-DR10, UX-DR11, UX-DR12, UX-DR13, UX-DR14, UX-DR15, UX-DR16, UX-DR17, UX-DR18
**Note:** UX-DR3 (Hook Announcement) → Epic 3. UX-DR7 (Flywheel Notice) → Epic 6. UX-DR8 (Proactive Orientation) — the proactive-offer-never-block pattern is established here in Stories 2.2/2.5 and fully exercised once story cycles (Epic 4) provide real workflow steps.

### Story 2.Spike: Validate Background Agent Coordination Mechanism

**Type:** Technical Spike
**FR Trace:** Architecture prerequisite for Stories 2.4, 4.3
**Description:** Validate that the SendMessage API reliably supports background agent checkpoint/resume for multi-step story cycles. Stories 2.4 (productive waiting) and 4.3 (full story cycle) depend on background agents that can be resumed mid-task via SendMessage. This spike must be documented before those stories are implemented.

**Acceptance Criteria:**

**Given** a background agent launched with `run_in_background: true`
**When** the spike investigates what inter-agent communication mechanisms Claude Code supports (TaskOutput, SendMessage if it exists, structured return values, or other)
**Then** the spike documents what API(s) support background agent coordination and whether checkpoint/resume is possible

**And** the spike documents whether background agents simply run to completion and return structured output, or whether mid-task communication is possible

**And** if no mid-task communication mechanism exists, the spike proposes an alternative to the productive waiting pattern before Stories 2.4 and 4.3 begin

**And** the spike result is documented in `docs/research/` before Story 2.4 is implemented

**And** if SendMessage + background does not support reliable checkpoint/resume, Architecture Decision 4c is updated and an alternative approach is proposed before Stories 2.4 and 4.3 begin implementation

---

### Story 2.1: Impetus Skill Created with Correct Persona and Input Handling

As a developer,
I want Impetus available as a skill with Impetus's consistent voice and clear menu,
So that I have a single, reliable orchestrating agent for every Momentum workflow.

**Acceptance Criteria:**

**Given** the Momentum skills are installed
**When** Claude Code starts
**Then** `momentum/SKILL.md` exists with a description ≤150 characters (NFR1)
**And** the skill name is `momentum` (entry-point, no prefix) — all other Momentum skills are prefixed `momentum-` to prevent naming collision with BMAD skills (NFR12)
**And** the skill's `model:` is set to a current Sonnet-tier model and `effort:` is `high` per the model routing guide (FR23); the specific model string is read from `references/model-routing-guide.md`, not hard-coded
**Note:** Impetus is classified as an orchestrator producing outputs without automated validation — per FR23/model routing guide, this qualifies for elevated effort. The routing guide (Story 3.5) will formally document this exception.
**And** skill instructions stay under 500 lines / 5000 tokens; overflow content is in `references/` (NFR3)
**And** when tested by invoking `/momentum` manually alongside 68+ BMAD skills, the correct Momentum skill matches on first attempt — spot-checked during dogfooding per NFR16 (NFR2)

**Given** a developer invokes `/momentum`
**When** Impetus presents its first response
**Then** a numbered menu lists all available practice workflows and entry points
**And** the response follows the Response Architecture Pattern (UX-DR15): orientation line → substantive content → transition signal → user control
**And** the orientation line is narrative (never "step N/M")
**And** user control is always the final element and always visible

**Given** Impetus is responding to any user action
**When** formulating the response
**Then** Impetus's voice is used: oriented, substantive, forward-moving (UX-DR18)
**And** no generic praise appears ("Great!", "Excellent!", "Sure!")
**And** no step counts appear ("Step 3/8")
**And** no agent machinery is visible — no internal names, no model references
**And** subagent findings are synthesized by Impetus before presenting (never raw output)
**And** when Impetus is uncertain, it acknowledges uncertainty explicitly rather than fabricating confidence

**Given** a developer enters a number, letter, or natural language phrase
**When** Impetus interprets input (UX-DR16)
**Then** a number selects the corresponding journal item or menu item
**And** a letter command is case-insensitive
**And** "continue" / "yes" / "go ahead" / "proceed" all map to C
**And** natural language intent is extracted and confirmed before acting ("Starting the story cycle for Story 4.2 — correct?")
**And** ambiguous input triggers exactly one clarifying question (never two)

---

### Story 2.2: Session Orientation and Thread Management

As a developer,
I want Impetus to tell me where I am at every session start and track open threads across sessions and tabs,
So that I can pick up any thread without hunting for context.

**Acceptance Criteria:**

**Given** a developer invokes `/momentum`
**When** Impetus starts (UX-DR11)
**Then** within two exchanges, Impetus surfaces: active story/task, current phase, last completed action, and suggested next action
**And** Impetus speaks first — the developer is never required to ask "where were we?"

**Given** the journal at `.claude/momentum/journal.json` contains one or more open thread entries
**When** Impetus starts (UX-DR1)
**Then** Impetus displays the Session Journal: numbered list of open threads, each showing workflow phase and elapsed time
**And** threads are ordered by most-recently-active
**And** each thread is directly selectable by its number

**Given** no journal exists or the journal is empty (user has never started a workflow — `installed.json` exists but no journal entries)
**When** Impetus starts
**Then** the Session Journal display is absent
**And** Impetus transitions directly to new-session orientation
**Note:** If `installed.json` does not exist, Story 1.3 (FR2) governs — this AC applies only to post-install sessions with no prior workflow activity.

**Given** a developer is running a workflow in Tab A
**When** they open Tab B and invoke `/momentum` (UX-DR13)
**Then** Impetus in Tab B reads the shared journal and surfaces Tab A's active thread
**And** if the entry was timestamped within the last 30 minutes, Impetus flags it as likely intentional concurrent work
**And** asks the developer to confirm before starting a competing thread on the same story

**Given** a journal entry has had no activity beyond the configured dormancy threshold (default: 3 days)
**When** Impetus starts (UX-DR14 — time-based trigger)
**Then** Impetus surfaces the dormant thread with brief context and offers one-action closure ("is this thread complete?")
**And** closure requires exactly one developer confirmation
**And** if the developer confirms, the thread is marked closed in the journal

**Given** a story or workflow that another journal thread depended on has just completed
**When** Impetus detects the dependency is satisfied (UX-DR14 — contextual trigger)
**Then** Impetus surfaces the waiting thread at session start: "The work this thread was waiting on is complete — ready to continue?"
**And** the developer decides whether to activate the waiting thread

**Given** the session journal has grown to more than 5 open threads
**When** Impetus starts (UX-DR14 — unwieldy-journal trigger)
**Then** Impetus flags the journal size and offers a triage pass before starting new work
**And** triage surfaces each thread's status and age with a single-action close option

**Given** the developer starts Impetus in a fresh context after an interruption
**When** Impetus reads the journal entry for the interrupted workflow (UX-DR17)
**Then** Impetus re-orients using saved journal context — no developer re-explanation required
**And** offers: "continue from here, or restart this step?" before proceeding

---

### Story 2.3: Visual Progress Tracks Workflow Position

As a developer,
I want Impetus to show me exactly where I am in any workflow with a consistent 3-line indicator,
So that I'm never lost and always know what's completed and what's next.

**Acceptance Criteria:**

**Given** a developer enters any Momentum workflow via Impetus
**When** a workflow is entered or a phase transitions (UX-DR2)
**Then** Impetus displays the Progress Indicator using ✓/→/◦ symbols
**And** completed steps collapse to a single ✓ line with a value summary phrase
**And** the current step stands alone with a one-phrase description
**And** upcoming steps collapse to a single ◦ line

**Given** a developer is at the very first step of a workflow (no completed steps yet)
**When** the Progress Indicator is displayed
**Then** the ✓ completed line is absent (there is nothing to collapse)
**And** the indicator shows → current step and ◦ upcoming steps only — the indicator is 2 lines at workflow start

**Given** a developer is at the very last step of a workflow (no upcoming steps)
**When** the Progress Indicator is displayed
**Then** the ◦ upcoming line is absent
**And** the indicator shows ✓ completed and → current step only — the indicator is 2 lines at workflow end

**Given** any symbol appears in any Impetus, hook, or subagent response
**When** rendered in any terminal or text context (UX-DR9)
**Then** each symbol is paired with text — meaning is recoverable without symbol rendering
**And** the symbol vocabulary is consistent across all Momentum components: ✓ completed/passing, → current/active, ◦ upcoming/pending, ! warning/attention, ✗ failed/blocked, ? question/decision

**Given** a developer is at a Workflow Step
**When** Impetus renders it (UX-DR4)
**Then** the step contains: narrative orientation line, substantive content, transition signal, explicit user control [A/P/C or equivalent]
**And** the orientation line is narrative — it never contains a step count in "Step N/M" format
**And** user control is always the final element

**Given** a workflow is interrupted mid-step
**When** the developer re-invokes `/momentum` in a new session (UX-DR17)
**Then** Impetus identifies the interrupted workflow from the journal
**And** presents the Progress Indicator showing which steps are complete
**And** asks: "continue from here, or restart this step?"
**And** sufficient context is in the journal entry to re-orient without developer re-explanation

**Given** a developer asks for their current position in any workflow (FR7)
**When** Impetus responds
**Then** a visual ASCII status graphic shows completed / current / upcoming phases
**And** the representation uses only characters available in any terminal

---

### Story 2.4: Completion Signals and Productive Waiting

As a developer,
I want Impetus to surface clear completion signals and maintain dialogue during background tasks,
So that I always know when something is mine to act on and I'm never left in silence.

**Acceptance Criteria:**

**Given** a story cycle, workflow, or major workflow step completes
**When** Impetus delivers the Completion Signal (UX-DR5)
**Then** the signal contains: explicit ownership return ("this is yours to review and adjust"), a file list of what was produced with paths, and a "what's next?" question
**And** the developer is never left unsure whether Impetus is still working

**Given** Impetus dispatches a background subagent (e.g. code-reviewer, VFL)
**When** the subagent is running (UX-DR12)
**Then** Impetus maintains dialogue on the same topic — does not context-switch to unrelated subjects
**And** for tasks taking more than a few seconds, Impetus offers substantive discussion or an acknowledged pause
**And** silence (dead air) is never the response to a running background task

**Given** a subagent returns findings
**When** Impetus synthesizes the result (UX-DR10)
**Then** Impetus's voice synthesizes the findings — raw subagent JSON or output is never presented to the developer
**And** severity indicators are used: ! for critical findings, · for minor findings
**And** critical findings trigger an explicit flywheel offer when the flywheel skill is available; if Epic 6 is not yet implemented, Impetus notes the finding and logs it for later flywheel processing

**Given** Impetus is orchestrating any subagent
**When** results arrive (UX-DR6)
**Then** subagent identity is never surfaced to the developer (hub-and-spoke contract maintained)
**And** the developer interacts only with Impetus — no awareness of which subagent ran is required
**And** subagents return structured JSON with at minimum `{status, result, question, confidence}` — Impetus synthesizes from this contract, not from free-form prose

**Given** implementation of a story cycle or workflow step has completed and a review process is being dispatched (FR8)
**When** the review runs
**Then** Impetus provides a human-readable summary of what was built or produced during the implementation phase
**And** this summary is delivered at the moment review is dispatched — the developer reads it while review runs, not after

---

### Story 2.5: Spec Contextualization and Configuration Gap Detection

As a developer,
I want Impetus to surface relevant spec context at the moment I need it and guide me through configuration gaps,
So that I never need to manually hunt for specs or figure out how to fix missing configuration.

**Acceptance Criteria:**

**Given** a developer is in a workflow step that references an architectural decision, acceptance criterion, or prior choice
**When** Impetus presents that step (FR10)
**Then** it surfaces the relevant spec context inline — file reference and key decision, not the full document
**And** the developer can act on the step without opening another file

**Given** a developer asks a follow-up question during any workflow step
**When** Impetus receives the question (FR11)
**Then** Impetus treats it as a discovery opportunity — gathers artifact context before answering
**And** returns an answer grounded in the current artifact (not generic)
**And** if the question reveals an ambiguity or gap in the current spec, Impetus flags it explicitly ("This question reveals an ambiguity in the acceptance criteria — worth clarifying before we continue")
**And** after answering, re-presents the user control so the workflow continues

**Given** the developer's project is missing required Momentum configuration (e.g. protocol mapping undefined, MCP provider unconfigured, ATDD tool binding undefined — full example list in FR9)
**When** Impetus detects the gap at session start or when a workflow step encounters it (FR9)
**Then** Impetus surfaces the gap with a clear description of what's missing and why it matters
**And** guides the developer through resolution conversationally — never dumps a raw config file
**And** does not block other workflows while resolution is pending unless the missing config would cause data loss or irreversible action in that workflow
**And** blocking gaps are defined as: missing MCP server required for the next workflow step, missing write target that would silently skip a required output

**Given** Impetus detects an information gap or a step the developer is about to skip
**When** the conversational floor is open (no subagent running, no pending decision) (UX-DR8)
**Then** Impetus uses proactive-offer framing — offers options without blocking on a response; the developer retains the decision

**Given** a developer has explicitly declined a proactive offer
**When** the same or similar gap recurs (UX-DR8)
**Then** Impetus does not re-surface the same offer unless context changes materially

---

## Epic 3: Automatic Quality Enforcement

Quality gates fire without developer intervention. Lint and format run on save. Acceptance tests are protected from modification. Model routing is configured by frontmatter so every skill and agent uses the right model by default. Authority hierarchy rules auto-load every session.

**FRs covered:** FR18, FR19, FR20, FR21, FR22, FR23
**NFRs covered:** NFR7, NFR8
**UX-DRs covered:** UX-DR3

### Story 3.1: PostToolUse Lint and Format Hook Active

As a developer,
I want code to be automatically linted and formatted every time I edit a file,
So that formatting violations never accumulate and I never have to run a separate format step.

**Acceptance Criteria:**

**Given** Momentum hooks are installed in `.claude/settings.json` (via Story 1.3)
**When** a developer edits any code file using a Claude Code tool
**Then** the PostToolUse hook fires automatically
**And** it runs the project's configured lint/format command (e.g. `prettier --write`, `eslint --fix`, `black`)
**And** the hook executes within the same tool response cycle — before the developer sees the final result

**Given** the PostToolUse hook runs and finds no issues
**When** the hook completes (UX-DR3)
**Then** it outputs exactly one line: `[lint] ✓ checked [file path] — clean`
**And** no additional output appears

**Given** the PostToolUse hook runs and finds auto-fixable issues
**When** the hook auto-fixes them (UX-DR3)
**Then** it outputs exactly one line: `[lint] ✓ auto-fixed [N issue(s)] in [file path]`

**Given** the PostToolUse hook runs and finds issues that cannot be auto-fixed
**When** the hook completes (UX-DR3)
**Then** it outputs: `[lint] ✗ [N issues] — [file:line of first] — [likely cause]`
**And** the output is specific enough for the developer to act without opening a separate tool

**Given** the project has no lint/format tool configured
**When** the PostToolUse hook fires
**Then** it outputs: `[lint] ◦ skipped — no lint tool configured`
**And** exits successfully — no false failure

---

### Story 3.2: PreToolUse File Protection Hooks Active

As a developer,
I want Momentum to block writes to acceptance tests and protected configuration files,
So that test integrity and critical config are preserved automatically — no accidental overwrites.

**Acceptance Criteria:**

**Given** Momentum hooks are installed
**When** a Claude Code tool attempts to write to any path matching `tests/acceptance/`, `**/*.feature`, or `.claude/rules/`
**Then** the PreToolUse hook fires and blocks the write before it executes
**And** returns an explanation of what was blocked and why

**Given** a PreToolUse hook blocks a write (UX-DR3)
**When** the hook fires
**Then** it outputs: `[file-protection] ✗ blocked write to [path] — [policy]: [reason]`
**And** the policy name and reason are specific (e.g. "acceptance-test-dir: no modification after ATDD phase begins")

**Given** a PreToolUse hook blocks a write (protected path)
**When** the hook fires (UX-DR3)
**Then** it outputs: `[file-protection] ✗ blocked write to [path] — momentum-state: protected Momentum state file`
**And** the developer receives a clear explanation of why the write was blocked and what they should do instead.
**Note:** Pass output is suppressed for allowed writes — UX-DR3's "never silent" principle applies when the hook has something meaningful to report (a block). Routine pass-through on non-protected paths is silent.

**Given** `.claude/momentum/installed.json` contains a project-customized protected path list
**When** the PreToolUse hook evaluates a write
**Then** it enforces the project-specific paths in addition to Momentum defaults
**And** project overrides are additive — they cannot remove Momentum default protected paths

**Given** a write to `_bmad-output/planning-artifacts/*.md` is attempted
**When** the PreToolUse hook fires
**Then** the write is blocked with: `[file-protection] ✗ blocked write to [path] — planning-artifacts: spec files are read-only during implementation`

---

### Story 3.3: Stop Gate Runs Conditional Quality Checks

As a developer,
I want quality gates to run automatically before my session ends,
So that I never close a session with failing tests or unresolved lint errors.

**Acceptance Criteria:**

**Given** a developer ends a Claude Code session
**When** the Stop hook fires (FR20)
**Then** lint runs unconditionally — regardless of whether code was modified this session
**And** tests run only if at least one code file was modified during the session
**And** the Stop hook determines whether code was modified by reading session state accumulated by PostToolUse Write/Edit hook events — not by running git diff or any external check
**And** if no code was modified, tests are skipped and the session ends cleanly

**Given** the Stop hook runs lint and finds no issues (UX-DR3)
**When** the hook completes
**Then** it outputs: `[stop-gate] ✓ checked lint — clean`
**And** the session proceeds to close

**Given** the Stop hook runs and finds lint failures (UX-DR3)
**When** the hook completes
**Then** it outputs: `[stop-gate] ✗ lint: [N issues] — [file:line of first] — fix before closing`
**And** the hook exits with a non-zero exit code to signal Claude Code that session termination should not proceed

**Given** the Stop hook runs tests and they pass (UX-DR3)
**When** the hook completes
**Then** it outputs: `[stop-gate] ✓ checked tests — [N] passed`

**Given** the Stop hook runs tests and they fail (UX-DR3)
**When** the hook completes
**Then** it outputs: `[stop-gate] ✗ tests: [N failed] — [failing test name] — [failure summary]`
**And** the hook exits with a non-zero exit code to signal Claude Code that session termination should not proceed

**Given** the Stop hook runs and the project has no test runner configured
**When** the test step would run
**Then** it outputs: `[stop-gate] ◦ tests — no test runner configured`
**And** lint still runs regardless

---

### Story 3.4: Authority Hierarchy Rules Auto-Load Every Session

As a developer,
I want Momentum rules to auto-load in every Claude Code session without any manual step,
So that practice standards are enforced consistently in primary sessions and all subagents.

**Acceptance Criteria:**

**Given** a developer starts any Claude Code session (primary or subagent)
**When** the session initializes (FR22)
**Then** all files in `~/.claude/rules/` auto-load as authority rules
**And** Momentum rules written there by Story 1.3 are active from the first message

**Given** Momentum rules are loaded in the primary session
**When** a Claude Code subagent is spawned (context:fork)
**Then** the subagent also loads rules from `~/.claude/rules/`
**And** enforcement applies equally to primary sessions and all subagents (NFR7 Tier 1)

**Given** a developer is using Cursor or another Agent Skills-compatible tool (Tier 2)
**When** they invoke a Momentum skill (NFR7)
**Then** the skill's advisory guidance is surfaced — hooks do not fire (no `.claude/settings.json` in Cursor)
**And** the developer is not required to take any additional action for skills to function in advisory mode
**And** the Momentum README documents Tier 1 vs. Tier 2 capabilities explicitly

**Given** a developer has no tooling at all (Tier 3)
**When** they read the Momentum README (NFR7)
**Then** all three tiers are defined with explicit lists of what works and what does not at each tier
**And** adoption instructions for each tier are present

**Cross-cutting:** The following ACs verify NFR8 portability compliance — they appear here as an integration check for the workflows implemented across Epics 2–4, with this Epic 3 story as the enforcement point.

**Given** any Momentum workflow SKILL.md file
**When** any integration-point step invoking an external tool is inspected (NFR8)
**Then** the step references a registered protocol type by name (e.g. `code-reviewer:review`, `test-runner:run`, `atdd-tool:run`) rather than a specific implementation or tool name (e.g. `playwright`, `jest`, `npm test`, `npx`)
**And** no workflow definition invokes a Claude Code tool by name in workflow step logic
**Note:** Formal protocol type registry (`references/protocol-contracts.md`) created in Story 7.1. At Story 3.4 implementation time, registered protocol type names are the names listed in the Protocol-Based Integration subsystem (subsystem 10) in the Architecture Requirements Overview and FR34–FR37 in the PRD. Native Claude Code tool calls (Read, Edit, Bash, Agent) are permitted — they are not protocol implementations.

---

### Story 3.5: Model Routing Configured by Frontmatter

As a developer,
I want every Momentum skill and agent to have its model and effort level set by frontmatter,
So that the right model is used for every task automatically — no manual overrides needed.

**Acceptance Criteria:**

**Given** the model routing guide exists at `skills/momentum/references/model-routing-guide.md`
**When** a contributor creates a new Momentum skill or agent (FR23)
**Then** they set `model:` and `effort:` frontmatter according to the routing guide
**And** the routing guide documents the default strategy: Sonnet 4.6 at medium effort for general skills; Opus for complex reasoning or outputs without automated validation (cognitive-hazard tasks); Haiku for constrained tasks with downstream automated validation

**Given** a Momentum skill's `model:` and `effort:` frontmatter is set
**When** Claude Code invokes the skill
**Then** the `model:` frontmatter value is used as the default model for that skill's execution
**And** higher-priority settings (e.g. `CLAUDE_CODE_SUBAGENT_MODEL` env var, `availableModels` project configuration) take precedence if set — frontmatter is the default, not an absolute guarantee
**And** no developer override is required in the normal case to get correct model behavior

**Given** the model routing guide is updated (e.g. a new model tier releases)
**When** the guide is applied to existing skills
**Then** all Momentum SKILL.md files have their `model:` frontmatter updated to reflect the new guidance
**And** the guide is reviewed as the source of truth — changes to model names happen first in the guide, then propagate to frontmatter

**Given** a Momentum skill is deployed in a non-Claude Code tool (NFR6)
**When** the tool parses `model:` and `effort:` frontmatter
**Then** it either respects them (if supported) or silently ignores them
**And** the skill functions correctly in both cases

**Given** a model routing rule file is written to `~/.claude/rules/model-routing.md` by Impetus (Story 1.3)
**When** a developer starts a Claude Code session
**Then** the model routing rule auto-loads and is active for all unspecified routing decisions

---

## Epic 4: Complete Story Cycles

A developer completes a full story cycle guided by Impetus — spec → ATDD → implement → code review → VFL validation — with every handoff driven by the agent. The developer never needs to know the next command; the agent tells them.

**FRs covered:** FR24, FR25, FR26, FR27, FR39, FR40, FR41, FR42, FR43
**UX-DRs covered:** UX-DR6, UX-DR8

### Story 4.1: Code-Reviewer Skill Performs Adversarial Review

As a developer,
I want a code-reviewer skill to perform adversarial, evidence-grounded review with read-only access,
So that every implementation is checked by an independent context before it is considered done.

**Acceptance Criteria:**

**Given** the code-reviewer skill is installed
**When** Claude Code parses `momentum-code-reviewer/SKILL.md`
**Then** the skill has `context: fork` frontmatter — it runs in a forked context isolated from the primary session
**And** the skill has `allowed-tools: Read` — it cannot write files, run commands, or call external services
**And** the skill has `disable-model-invocation: true` frontmatter — it cannot spawn nested model calls
**And** the skill description is ≤150 characters (NFR1)

**Given** the code-reviewer skill is invoked (FR24)
**When** it reviews an implementation artifact
**Then** it produces a structured findings report as JSON matching the subagent output contract (Architecture Decision 3b): `{status, result: {findings: [{id, severity, location, description, evidence, provenance_status}], summary}, question, confidence}`
**And** every finding includes a `evidence` field quoting the specific artifact content that supports the finding (FR27)
**And** findings without direct evidence from the reviewed artifact are not emitted — fabricated findings are a critical defect

**Given** the findings report includes traceability-dimension findings (FR26)
**When** a finding relates to a derives_from reference, a staleness concern, or an ungrounded claim
**Then** the finding's `provenance_status` field is populated (VERIFIED/CITED/INFERRED/UNGROUNDED/SUSPECT)
**And** findings without a provenance dimension leave `provenance_status` null — not defaulted to any value

**Given** a story cycle implementation step completes in Impetus (FR25)
**When** Impetus transitions to the review phase
**Then** the code-reviewer is invoked automatically — the developer is not required to run a separate command
**And** Impetus announces the review has started and maintains productive dialogue while it runs (UX-DR12)

**Given** the code-reviewer returns its structured JSON findings (UX-DR6)
**When** Impetus synthesizes the result
**Then** Impetus presents a summary in Impetus's voice — severity grouped, most critical first
**And** raw JSON is never shown to the developer
**And** the `! critical` and `· minor` severity indicators are used in the synthesis
**And** any critical finding triggers an explicit flywheel offer

---

### Story 4.2: Gherkin ACs and ATDD Workflow Active

As a developer,
I want to define acceptance criteria in Gherkin that generates failing tests before I write code,
So that the test suite captures intent from the spec, not from the implementation.

**Acceptance Criteria:**

**Given** a developer writes acceptance criteria for a story (FR39)
**When** the criteria are reviewed
**Then** each AC is expressed as a Given/When/Then scenario
**And** each scenario is behavioral — it describes what the system does, not how
**And** each scenario is technology-agnostic — no specific library, framework, or tool name appears
**And** each scenario is implementation-independent — passing or failing is determinable without reading the implementation

**Given** the ATDD workflow capability is part of the dev-story skill
**When** Claude Code parses `momentum-dev-story/SKILL.md`
**Then** the skill file exists at that path and its description is ≤150 characters (NFR1)
**Note:** ATDD is not a separate deployed skill — it is part of the `momentum-dev-story` workflow. There is no `momentum-atdd/SKILL.md`.

**Given** the ATDD workflow is invoked with a story's Gherkin ACs (FR40)
**When** the workflow runs
**Then** it generates failing acceptance tests before any implementation code is written
**And** each generated test maps 1:1 to a Given/When/Then scenario
**And** the tests fail initially because the implementation does not yet exist — not because the test is malformed
**And** the tests are written to `tests/acceptance/` and are protected from modification (Story 3.2) once written

**Given** the developer inspects the generated failing tests
**When** they run the test suite
**Then** the failure messages reference the scenario name and the specific assertion that failed
**And** the developer can determine what code to write from the failure message alone — no spec re-reading required

**Given** a Gherkin scenario references a specific implementation detail (e.g. a function name, a database column, a URL path)
**When** the ATDD workflow validates the scenario
**Then** it flags the scenario as implementation-coupled and requests a behavioral rewrite
**And** the test is not generated until the scenario is corrected

---

### Story 4.3: Full Story Cycle Guided by Impetus

As a developer,
I want Impetus to guide me through the complete story cycle from spec to flywheel,
So that I always know the next step and every handoff happens without me having to ask.

**Acceptance Criteria:**

**Given** a developer begins a story cycle with Impetus (FR41)
**When** the cycle starts
**Then** Impetus presents the five phases in order: Spec Review → ATDD → Implement → Code Review → Flywheel
**And** Impetus drives each phase transition automatically when the prior phase completes — the developer is prompted to confirm before proceeding to the next phase (FR25: transitions are automatic when unambiguous, or prompted when the developer's intent is needed)
**And** the developer may also invoke any phase explicitly at any time — Impetus never blocks manual phase invocation (UX-DR15: user control always last)

**Given** the story cycle is in progress (FR42)
**When** any phase begins or completes
**Then** Impetus displays the visual story-cycle progress: completed phases with ✓ summary, current phase with → description, remaining phases collapsed to ◦ one-liner
**And** the current phase and next phase are always visible — no phase is invisible to the developer

**Given** Impetus detects the developer is about to skip a required phase (e.g. moving to Implement without completing ATDD) (UX-DR8)
**When** the conversational floor is open (no subagent running, no pending decision)
**Then** Impetus proactively surfaces the skip: "The ATDD step hasn't run yet — tests should come before implementation. Want to run it now?"
**And** Impetus offers, never blocks — if the developer explicitly declines, the cycle continues
**And** the developer's decision is respected and not re-asked unless context changes

**Given** Impetus detects a knowledge gap relevant to the current phase (e.g. an architectural decision the developer may be unaware of) (UX-DR8)
**When** the conversational floor is open
**Then** Impetus surfaces the knowledge gap with a one-sentence summary and a question: "There's an architecture decision here that might affect this step — want a quick summary?"
**And** the developer controls whether to hear it — Impetus never dumps context unsolicited

**Given** the story cycle's code review phase completes with critical findings
**When** Impetus synthesizes results (UX-DR6)
**Then** Impetus presents the findings summary and asks whether to trigger the flywheel
**And** the flywheel offer is explicit — the developer must approve before it runs
**And** if the developer declines, Impetus notes the open findings and closes the cycle

---

### Story 4.4: Create-Story and Dev-Story Skills Active

As a developer,
I want dedicated skills for creating story files and executing story implementations,
So that Impetus can delegate each phase to a focused, context-rich agent.

**Acceptance Criteria:**

**Given** the create-story skill is installed
**When** Impetus delegates story creation
**Then** `momentum-create-story/SKILL.md` exists and runs in the main context (not forked)
**And** it produces a story file that contains: story title, user story statement, Gherkin ACs, architecture context relevant to the story, derives_from pointers to the spec documents it was created from
**And** sprint metadata is written to `sprint-status.yaml` in the `momentum_metadata` section (keyed by story_key, with `depends_on`, `touches`, `story_file`) and Impetus tells the developer the path before writing (completion signal per UX-DR5)
**And** `depends_on` is a list of story_keys extracted from the epics dependency notes for this story, `touches` is a list of paths inferred from the story's implementation scope (skill dirs, shared config files)

**Given** the dev-story skill is installed
**When** invoked without an explicit story path
**Then** `momentum-dev` reads `sprint-status.yaml`, selects the highest-priority story where `development_status == "ready-for-dev"` and all `depends_on` story_keys have `development_status == "done"`
**And** priority order is: epic sprint assignment (Day 1 first, then Sprint 1, Sprint 2, Growth), then story order within that epic
**And** if no story qualifies (all remaining are blocked or in_progress), `momentum-dev` surfaces "All remaining stories are blocked on: [list]" and halts

**When** invoked with an explicit story file path
**Then** `momentum-dev` uses that story directly, skipping selection

**Given** `momentum-dev` has selected or been given a story to develop
**When** the story session begins
**Then** `momentum-dev` captures the current branch via `git branch --show-current` (Bash tool) and stores it as `target_branch`
**And** checks for crash recovery: if branch `story/{story_id}` already exists AND worktree `.worktrees/story-{story_id}` exists, offers to resume or clean up; if branch exists but no worktree, deletes the stale branch and proceeds fresh
**And** creates a git worktree: `git worktree add .worktrees/story-{story_id} -b story/{story_id}`
**And** writes a lock file `.worktrees/story-{story_id}.lock`, then writes `status: in_progress` to the story spec frontmatter in the main working tree (not inside the worktree, so all concurrent sessions see the update immediately)
**And** it reads the story file and implements to the Gherkin ACs — not to implementation details it infers independently
**And** it does not modify acceptance test files in `tests/acceptance/` (enforced by Story 3.2 hooks)

**Given** a dev-story run completes
**When** the story implementation is done
**Then** `momentum-dev` writes `status: complete` to the story spec frontmatter (in the main working tree) and removes the lock file
**And** presents to the user: "Ready to merge story/{story_id} into {target_branch}. touches overlap: [list or none]. Run: git merge story/{story_id}" — and waits for explicit user confirmation before executing the merge
**And** after confirmed merge: runs `git worktree remove .worktrees/story-{story_id}` and `git branch -d story/{story_id}`
**And** signals completion with a structured output matching the subagent output contract (Architecture Decision 3b): `{status, result: {files_modified: [], tests_run: bool, test_result: pass|fail|not_run}, question, confidence}`

**Given** a dev-story run completes
**When** Impetus receives the structured output
**Then** Impetus synthesizes the completion signal per UX-DR5: files produced, test results, what's next
**And** transitions the story cycle to the Code Review phase automatically (FR41 handoff)

**And** if `test_result` is `not_run` (ATDD generated tests but no test runner protocol binding is configured)
**Then** Impetus surfaces the gap: "Tests generated but no test runner is configured — Story 4.4 requires Story 7.2 (protocol gap resolution) or manual test runner setup before automated verification."
**And** the story does not advance to Code Review automatically

---

### Story 4.5: Upstream Fix Skill Analyzes Quality Failures

As a developer,
I want an upstream fix skill that traces quality failures back to their root cause and proposes the right fix at the right level,
So that defects get fixed in specs and rules — not just patched in the code.

**Acceptance Criteria:**

**Given** the upstream-fix skill is installed
**When** invoked with a quality failure (a findings report, a test failure, a VFL finding) (FR43)
**Then** `momentum-upstream-fix/SKILL.md` exists and reads the failure description plus the relevant artifacts
**And** it proposes the fix level: spec-generating workflow, specification (story/epic/PRD), CLAUDE.md/rules, tooling, or one-off code fix
**And** it outputs a structured proposal matching the subagent output contract (Architecture Decision 3b): `{status, result: {failure_summary, root_cause, proposed_fix_level, proposed_fix_description}, question, confidence}`

**Given** the upstream-fix skill proposes a fix
**When** Impetus presents the proposal to the developer
**Then** Impetus presents it in Impetus's voice — not the raw JSON
**And** the developer must explicitly approve before any fix is applied
**And** if the fix modifies a spec or rule, Impetus identifies which file will change and shows the change before applying

**Given** a fix is applied at the spec or rule level
**When** the fix is complete
**Then** the story cycle continues from the phase where the failure was detected — not from the beginning

**Given** an upstream fix is approved and applied
**When** Impetus records the fix
**Then** the upstream fix outcome is recorded in the session journal by Impetus (field: `upstream_fix_applied`, `upstream_fix_level`) — the findings ledger (`~/.claude/momentum/findings-ledger.jsonl`) is written only by the flywheel workflow (Epic 6)
**And** Impetus records the upstream fix application in the session journal with fix level and artifact modified

---

## Epic 5: Trust Artifact Provenance

A developer can trace every artifact to its origins, detect stale references, and know the confidence level of every significant claim. The provenance graph is maintained in frontmatter — no external tooling required.

**FRs covered:** FR12, FR13, FR14, FR15, FR16, FR17
**UX-DRs covered:** UX-DR5 (scanner completion signal at session orientation)
**Additional:** derives_from frontmatter format, content hash staleness (git hash-object), referenced_by auto-generation, provenance scanner (in Impetus references/)

### Story 5.1: derives_from Frontmatter Establishes Traceability

As a developer,
I want every specification artifact to carry derives_from frontmatter linking it to its upstream sources,
So that any artifact can be traced to the documents that produced it — without consulting anyone.

**Acceptance Criteria:**

**Given** a spec-generating artifact is created (PRD, architecture, epics, stories, UX design, research summary) (FR12)
**When** the artifact is first authored
**Then** its frontmatter includes a `derives_from` block with one entry per upstream source
**And** each entry contains: `id` (SCREAMING-KEBAB-CASE, unique across project), `path` (repo-relative), `relationship` (`derives_from`, `depends_on`, or `satisfies`), `description` (one sentence: what the source contributed), and `hash` (empty string on initial authoring — set by the author or a provisioning workflow on first use; the provenance scanner reads this field but never writes it)

**Given** a top-level specification document is authored (PRD, architecture, UX design, product brief, or any document that is a root of the specification tree) (FR15)
**When** the document is created
**Then** its frontmatter includes `is_specification: true`
**And** this marker enables the provenance scanner to discover the root of the specification tree without traversal from every leaf

**Given** any content block in a spec artifact was written or substantially revised (FR17)
**When** the content is committed
**Then** the document frontmatter includes `authored_by: human` for human-written content or `authored_by: ai` for AI-generated content
**And** artifacts with mixed authorship carry `authored_by: mixed` at the document level
**And** the `authored_by` field is document-level frontmatter (not inside the `derives_from` block) — it is set by the author and is never auto-inferred
**And** AI agents setting `authored_by` are updating a document-level frontmatter field, which is permitted — Decision 2b's write restriction applies specifically to the `derives_from` block, not to all frontmatter

**Given** an AI agent (Impetus, code-reviewer, or any Momentum subagent) modifies a spec artifact
**When** the modification is applied (Architecture Decision 2b)
**Then** the agent does not remove or modify the `derives_from` frontmatter block or any entry within it
**And** the agent may add new `derives_from` entries if a new dependency is introduced — but never silently remove or alter existing ones
**And** a single violation is reported to Impetus, which surfaces it at session end and records it in the findings ledger as a `missing-provenance` finding
**And** if the same agent produces repeated violations across multiple sessions, Impetus proposes promoting the constraint to a PreToolUse hook rule — the hook-promotion path is the escalation for systemic failures

---

### Story 5.2: Provenance Scanner Builds referenced_by Graph

As a developer,
I want to know what depends on a document I'm about to change,
So that I can anticipate downstream impact without manually tracking reverse references.

**Acceptance Criteria:**

**Given** the provenance scanner is implemented at `references/provenance-scan.md` within the `momentum/` skill (FR14)
**When** the scanner runs
**Then** it reads all `derives_from` entries across every file in the project
**And** it constructs a reverse-reference index: for each source document, a list of all downstream documents that declare it in `derives_from`
**And** this index is the `referenced_by` graph — no file in the project manually maintains `referenced_by` entries

**Given** the provenance scanner runs as part of Impetus session orientation (Story 2.2 — "Session Orientation and Thread Management")
**When** Impetus initializes a session
**Then** the scanner executes before Impetus presents the session summary
**And** the scanner is not a separate `context: fork` skill invocation — it runs as inline reference logic within the `momentum/` skill's session orientation step
**And** the scanner produces a structured result using the same field names as the subagent output contract (`{status, result: {suspect_list: [], referenced_by_graph: {}, ungrounded_count: N}, question, confidence}`) for consistency, but it is not invoked via the Agent tool — it runs inline within the session orientation step
**And** this output is available to Impetus for surfacing impact warnings and SUSPECT flags throughout the session

**Given** a developer asks Impetus "what depends on [document]?"
**When** the question is processed
**Then** Impetus queries the referenced_by graph and reports all downstream dependents
**And** if no dependents exist, Impetus says so — it never implies a document is depended on when it is not

**Given** a new document is added to the project with `derives_from` entries
**When** the scanner next runs
**Then** the new document's upstream sources appear in their respective `referenced_by` sets automatically — no manual step required

---

### Story 5.3: Hash-Based Staleness Detection for Internal Documents

As a developer,
I want Impetus to flag documents that depend on source files I've changed,
So that I know which downstream artifacts may need to be updated before I close a session.

**Acceptance Criteria:**

**Given** a `derives_from` entry has a non-empty `hash` field (FR13 — hash mode)
**When** the provenance scanner runs
**Then** it computes `git hash-object <path>` for each referenced internal document
**And** it compares the computed hash against the stored `hash` value in the `derives_from` entry
**And** if the hashes differ, the dependent document's provenance status for that entry is flagged as SUSPECT

**Given** a `derives_from` entry has an empty `hash` field
**When** the provenance scanner encounters it
**Then** it skips hash comparison for that entry and includes it in the scanner output as `hash_unchecked: true`
**And** the provenance scanner never writes to spec files — hash values are populated by the author or a provisioning step, not the scanner
**And** Impetus surfaces unchecked entries at session start: `◦ [N] derives_from entries have no stored hash — run hash provisioning to enable staleness detection`

**Given** the provenance scanner detects one or more SUSPECT downstream documents
**When** Impetus presents the session summary
**Then** Impetus surfaces the suspect list: `⚠ [N] dependent(s) may be stale — [downstream-doc] depends on [source-doc] which has changed / Action: review [downstream-doc] and confirm or update`
**And** Impetus does not automatically update any downstream document — it surfaces and asks, never acts without consent

**Given** a SUSPECT document is flagged
**When** Impetus propagates the staleness signal (FR13 — one-hop only)
**Then** only direct one-hop dependents are flagged — second-hop dependents are not automatically flagged
**And** Impetus asks the developer for each flagged dependent: "Does [downstream-doc] still hold given the change to [source-doc]?" — the developer must explicitly confirm or indicate an update is needed (this is the human gate)
**And** if the developer confirms the dependent is still valid, the SUSPECT flag is cleared for this session and Impetus does not propagate the signal further
**And** if the developer updates the dependent document to reflect the source change, the author or provisioning step updates the `hash` field in that entry's `derives_from` block and the SUSPECT flag clears on the next scan

---

### Story 5.4: Time-Based Staleness for Edge Documents

As a developer,
I want external sources (research docs, web references) to carry freshness windows,
So that Impetus warns me when an external source may have aged out before I rely on it.

**Acceptance Criteria:**

**Given** a `derives_from` entry references an external or edge document (FR13 — time-based mode)
**When** the entry is authored
**Then** it carries two additional fields that extend the canonical derives_from schema for edge references: `sourced_date` (ISO 8601 date: the date the content was retrieved or verified) and optionally `freshness_window` (integer days: overrides the document-level default for this entry)
**And** the parent document's frontmatter may carry a `freshness_window` field (in days) as the domain-level default for all edge derives_from entries in that document
**And** entry-level `freshness_window` takes precedence over document-level `freshness_window`

**Given** the provenance scanner runs and encounters a time-based derives_from entry
**When** it evaluates staleness
**Then** it obtains `current_date` from the `currentDate` context variable injected at session start — if unavailable, it reports the entry as `freshness_unchecked: true` and does not attempt time-based comparison
**And** it computes: `current_date - sourced_date > freshness_window`
**And** if true, the entry is included in the scanner's SUSPECT output list — the scanner never writes SUSPECT status to spec file frontmatter (scanner is read-only)
**And** if false, the entry remains in CITED status

**Given** Impetus surfaces a time-based SUSPECT at session start
**When** the developer sees the warning
**Then** Impetus states: `⚠ [document] cites [source] — sourced [N] days ago, past the [domain] window of [W] days / Action: re-verify [source] or extend freshness_window if still current`
**And** Impetus offers to help re-verify the source — but does not block work if the developer declines
**And** one-hop propagation applies: only documents that directly cite the stale edge source are flagged — second-hop dependents are not automatically flagged (same gate as Story 5.3)

**Given** a domain-specific freshness window is needed
**When** the provenance guide (`references/provenance-scan.md`) documents default windows
**Then** the defaults follow the authoritative domain taxonomy defined in FR47 (Epic 8) — Story 5.4 does not define competing defaults
**And** document authors may override the default by setting `freshness_window` in the document's frontmatter or the entry — entry-level override takes precedence

---

### Story 5.5: Claim-Level Provenance Status and Integrity Enforcement

As a developer,
I want every significant claim in a spec to carry a provenance status,
So that I know which claims are verified facts, which are inferences, and which have no grounding at all.

**Acceptance Criteria:**

**Given** a specification artifact contains claims (FR16)
**When** claims are classified
**Then** a "significant claim" is defined as: any assertion of fact, capability, constraint, or design decision — as opposed to meta-commentary, headings, or transitional language
**And** each significant claim carries one of five provenance status values (FR16 — canonical epistemic status vocabulary):
- `VERIFIED`: source exists and the claim is accurate against it — high trust, cite without caveat
- `CITED`: source URL provided and accessible on the research date — moderate trust
- `INFERRED`: derived through reasoning from verified sources — lower trust, note the inference
- `UNGROUNDED`: no source; based on training knowledge — low trust, must verify before acting
- `SUSPECT`: was VERIFIED or CITED but the upstream source has since changed — re-verify required
**And** this five-value vocabulary (FR16) covers epistemic confidence in a claim — it is distinct from Architecture Decision 2b's content-origin classification (SOURCED / DERIVED / ADDED / UNGROUNDED), which categorizes how content was produced, not how trustworthy it is; both systems coexist and serve different purposes

**Given** a Momentum agent (Impetus, code-reviewer, upstream-fix) produces a significant claim in a spec context
**When** the claim is emitted
**Then** the claim is accompanied by its provenance_status field value — never left implicit
**And** UNGROUNDED claims are flagged explicitly: "This claim has no external source — treat as a starting point for verification, not a decision basis"

**Given** a spec artifact contains UNGROUNDED claims
**When** Impetus reviews the artifact at the start of a story cycle
**Then** Impetus surfaces a count: `[N] ungrounded claims found in [document] — review before implementing`
**And** Impetus does not block implementation — it surfaces and asks whether to address before proceeding

**Given** an AI agent generates or modifies a spec artifact and sets provenance statuses
**When** the statuses are evaluated (FR17 — human vs. AI attribution)
**Then** the `authored_by` field on the document distinguishes whether the provenance classification was done by a human or AI
**And** AI-classified provenance statuses are treated as provisional — a human reviewer must confirm VERIFIED status before it is treated as authoritative

**Given** a provenance integrity violation occurs
**When** the provenance scanner detects a structural violation (missing `derives_from` block in a spec that should have one; empty `id` or `path` fields in an entry)
**Then** the scanner includes the violation in its session-start output — it does not write to any file
**And** Impetus receives the scanner output and surfaces the violation: `⚠ provenance integrity — [document]: [violation description] / Action: add missing derives_from or correct the entry`
**And** Impetus triggers the flywheel workflow to record a finding in the findings ledger (Decision 1c: only the flywheel workflow writes findings)
**And** the finding includes the required schema fields: `id` (generated), `story_ref`, `phase: "session-orientation"`, `severity: "HIGH"`, `pattern_tags: ["missing-provenance"]`, `description`, `evidence` (file and field reference), `provenance_status: null`, `upstream_fix_applied: false`, `upstream_fix_ref: null`, `timestamp`

**Given** a semantic violation is suspected (AI agent claims VERIFIED status without providing a source)
**When** Impetus encounters this in an artifact review
**Then** Impetus (not the scanner) evaluates the claim: if the claim has a provenance_status of VERIFIED but the derives_from block has no entry that could substantiate it, Impetus surfaces the discrepancy and asks the developer to confirm or reclassify
**And** the scanner never evaluates claim semantics — it only checks structural completeness of derives_from blocks and entry fields

---

## Epic 6: The Practice Compounds

Findings accumulate across stories. Systemic patterns surface. Upstream fixes are applied at the right level — spec, rule, workflow, or one-off patch. Each sprint the practice gets measurably smarter. The flywheel makes invisible improvement visible.

**FRs covered:** FR28, FR29, FR30, FR31, FR32, FR33
**UX-DRs covered:** UX-DR7
**Additional:** findings-ledger.jsonl (global, with full schema), upstream-fix skill (momentum-upstream-fix), flywheel workflow, Momentum findings MCP server (optional query layer)

### Story 6.1: Findings Ledger Accumulates Quality Findings Across Stories

As a developer,
I want all quality findings — from code reviews, VFL runs, and flywheel traces — to accumulate in a structured ledger,
So that nothing is lost between sessions and every defect has a traceable record.

**Acceptance Criteria:**

**Given** the findings ledger is initialized (FR28)
**When** Momentum is first installed on a workstation
**Then** `~/.claude/momentum/findings-ledger.jsonl` is created as an empty file (directory created if absent)
**And** only the flywheel workflow (momentum-upstream-fix) is authorized to write to this file — all other agents submit findings via structured output to Impetus, which triggers the flywheel to write (Architecture Decision 1c / Decision 2a)
**And** the flywheel writes findings by appending a single JSON line to `~/.claude/momentum/findings-ledger.jsonl` — this is the primary write mechanism; no MCP server is required for writes

**Given** a quality finding is produced (from code-reviewer, VFL, or architecture-guard)
**When** the flywheel records the finding
**Then** the journal entry contains all required schema fields: `id` (`F-{unix_ms}-{random_4hex}`, e.g. `F-1711929600000-a3f2`), `project` (string, project identifier), `story_ref`, `phase` (one of: `spec` | `atdd` | `implement` | `code-review` | `flywheel`), `severity` (`critical` | `high` | `medium` | `low`), `pattern_tags` (kebab-case noun phrases), `description` (one sentence), `evidence` (exact quote or `file:line` reference), `provenance_status` (one of the five FR16 values, or `null` if not applicable), `upstream_fix_applied` (boolean, initially `false`), `upstream_fix_ref` (`null` until a fix is applied), `upstream_fix_level` (`null` until a fix is applied; then one of: `spec-generating-workflow` | `specification` | `rules-or-CLAUDE.md` | `tooling` | `one-off-code-fix`), `timestamp` (ISO 8601)
**And** subagent findings submitted to Impetus must use the structured output contract (Architecture Decision 3b): `{status, result: {findings: [...]}, question, confidence}` — Impetus extracts finding objects and passes them to the flywheel for ledger ingestion
**And** an entry with any missing required field is rejected — the flywheel does not write partial entries

**Given** the Momentum findings MCP server is installed (`mcp/findings-server/` — Epic 6 scope)
**When** Impetus or the flywheel queries the journal
**Then** the MCP server provides structured read-only query access over `~/.claude/momentum/findings-ledger.jsonl` (filter by project, pattern_tag, severity, date range)
**And** Impetus reads the journal at retrospective and upstream trace phases to build pattern context
**And** when the MCP server is unavailable, direct JSONL file reading is the fallback — developer can always inspect the file directly

**Given** the journal has grown across multiple sprints
**When** Impetus generates a session summary
**Then** it includes a one-line ledger summary: `[N] findings across [S] stories — [C] critical open, [H] high open` (where "open" means `upstream_fix_applied: false` for that severity level)
**And** if no findings exist, the summary is omitted — no placeholder text

---

### Story 6.2: Cross-Story Pattern Detection Surfaces Systemic Issues

As a developer,
I want Impetus to detect when the same type of defect keeps appearing across different stories,
So that I know when a problem is systemic and needs a root-level fix rather than another patch.

**Acceptance Criteria:**

**Given** the findings ledger contains entries from two or more stories or projects (FR29)
**When** Impetus runs pattern detection (at session start, retrospective, or explicit query)
**Then** it groups findings by `pattern_tags` across all stories and projects
**And** a pattern is considered systemic when the same `pattern_tag` appears in findings from 2 or more distinct `story_ref` values OR 2 or more distinct `project` values
**And** Impetus surfaces each systemic pattern: `⚠ systemic pattern: [tag] — appeared in [N] stories across [P] projects ([story-refs]) / Action: run flywheel to trace root cause`

**Given** a systemic pattern is detected
**When** Impetus presents the pattern to the developer
**Then** it shows: the tag name, the count of affected stories, the severity distribution (how many critical/high/medium/low), and the most recent evidence quote
**And** Impetus does not automatically trigger the flywheel — it offers: "Want to run the flywheel to trace root cause for [tag]?"
**And** the developer must explicitly approve before the flywheel starts (FR31)

**Given** a pattern was surfaced and the developer declined to act on it
**When** the pattern appears in a subsequent session
**Then** Impetus surfaces it again with an updated count — it does not remember that the developer declined unless the developer explicitly says "suppress this pattern"
**And** if the developer suppresses a pattern, Impetus records the suppression in the findings ledger as a special entry: `{id, project, story_ref: null, phase: "pattern-suppression", pattern_tags: [tag], description: "Developer suppressed pattern", upstream_fix_applied: false, upstream_fix_level: null, timestamp}` — this persists the suppression across sessions
**And** Impetus does not surface the same tag again until the findings-journal entry count for that tag increases beyond the count at suppression time

**Given** no systemic patterns exist in the journal
**When** pattern detection runs
**Then** the result is omitted from the session summary — no "no patterns found" message is shown

---

### Story 6.3: Flywheel Workflow Explains Issues and Guides Upstream Trace

As a developer,
I want the flywheel to walk me through a structured trace from finding to root cause to fix,
So that I fix defects at the right level instead of patching symptoms.

**Acceptance Criteria:**

**Given** the flywheel is triggered for a finding or systemic pattern (FR30)
**When** the workflow begins
**Then** it executes the six phases in order: Detection → Review → Upstream Trace → Solution → Verify → Log (per the upstream fix process defined in architecture.md; the Log phase is the sixth phase — confirmed in Architecture Process Patterns section)
**And** at each phase transition, Impetus displays the Workflow Step component (UX-DR4): an orientation line (never "phase N/6"), substantive content for the current phase, a transition signal, and explicit user control (A/P/C or Approve/Reject as context requires)
**And** no phase may be skipped — the Log phase is required even if the solution is a "no-fix" decision
**And** the finding is appended to `~/.claude/momentum/findings-ledger.jsonl` during the Detection phase, not at the end of the workflow — the finding exists in the journal before any trace or fix is applied

**Given** the Detection phase runs
**When** Impetus presents the detected finding
**Then** it displays: finding id, description, evidence, severity, and whether a prior upstream fix was applied to this pattern
**And** if this is a systemic pattern, it shows the full list of affected stories
**And** the finding is appended to the findings ledger at this phase (if not already present from the originating review)

**Given** the Review phase runs (second phase — examination before root-cause tracing)
**When** Impetus presents the review
**Then** it examines the finding in context: reads the artifact where the finding was detected, reads the relevant spec/rule that governs that area, and summarizes: "This finding is in [artifact], governed by [rule/spec], and appears to be caused by [preliminary hypothesis]"
**And** Impetus asks the developer: "Does this match your understanding, or should I adjust the scope before tracing?" (explicit developer checkpoint before Upstream Trace proceeds)
**And** the developer must confirm or redirect before the workflow advances to Upstream Trace
**Note:** If the developer redirects (adjusts scope), Impetus re-analyzes with the revised scope and re-presents for confirmation. This loops within the Review phase until confirmed. Maximum 3 adjustment iterations before Impetus offers to defer the trace to a later session.

**Given** the Upstream Trace phase runs
**When** Impetus presents the trace result
**Then** it identifies the root level: one of `spec-generating-workflow` | `specification` | `rules-or-CLAUDE.md` | `tooling` | `one-off-code-fix`
**And** it explains why this level was chosen: "The root cause is in [artifact] because [one sentence]"
**And** the explanation is Impetus's synthesis — never raw subagent output (UX-DR10)
**And** Impetus asks the developer: "Does this root level look correct before proposing a fix?" — developer must explicitly confirm before Solution phase begins

**Given** the Log phase runs (final phase)
**When** all prior phases are complete
**Then** Impetus records the complete flywheel run: finding id, phases completed, fix level applied (or "no-fix"), fix ref, outcome (resolved | unresolved | deferred), and timestamp
**And** the findings journal entry is updated by appending a new JSONL line with the same `id` and updated `upstream_fix_applied`, `upstream_fix_level`, and `upstream_fix_ref` values (JSONL is append-only; the latest line with a given `id` supersedes prior entries)
**And** if the developer rejected the fix, the outcome is recorded as "deferred" — not "resolved"

**Given** the Solution phase completes and a fix is applied
**When** Impetus presents the outcome (UX-DR7)
**Then** it displays the Flywheel Notice component:
- `Finding:` [description of the original defect]
- `Root cause:` [one sentence]
- `Fix applied:` [what changed and where]
- `What it prevents:` [the class of future defects this fix eliminates]
**And** this notice makes the improvement visible — the developer can see that practice quality increased, not just that a bug was fixed

---

### Story 6.4: Developer Consent Required at Every Flywheel Step

As a developer,
I want to control every step of the flywheel — approve, modify, or reject — before anything changes,
So that the system never applies a fix I haven't reviewed.

**Acceptance Criteria:**

**Given** the flywheel reaches the Solution phase (FR31)
**When** a fix is proposed
**Then** Impetus presents the full proposed fix: what file changes, what the change is, and which finding it addresses
**And** the developer must explicitly approve (`A`) or reject (`R`) before any change is applied
**And** if the developer rejects, the flywheel records the rejection in the Log phase and closes — no changes are made

**Given** the flywheel proposes a fix to a specification or rule file
**When** the proposal is shown
**Then** Impetus displays the exact diff of the proposed change before asking for approval
**And** the developer may request modifications: "change X to Y before applying"
**And** Impetus applies modifications and shows the revised diff before re-asking for approval — the cycle repeats until the developer approves or rejects

**Given** the flywheel reaches a consent gate (after Review, after Upstream Trace, or at Solution)
**When** Impetus is about to ask for developer approval
**Then** the flywheel writes the pending consent state to the session journal immediately before presenting the consent prompt: `{flywheel_ref, finding_id, phase: "[current-phase]", status: "awaiting_consent", timestamp}`
**And** the phase value is the actual current phase name — not hardcoded to "solution"
**And** at the next session start, Impetus reads the session journal, detects any `status: "awaiting_consent"` entries, and surfaces them: "A flywheel trace is awaiting your decision — [finding description] at [phase]. Want to resume?"

**Given** the flywheel's Verify phase runs after a fix is applied
**When** verification executes
**Then** Impetus re-reads the artifact where the finding was originally detected and checks whether the condition described in the finding's `evidence` field is still present
**And** if the evidence condition is no longer present, verification passes: Impetus confirms "The fix has been applied and the finding is resolved"
**And** if the evidence condition is still present or a new related finding is produced, verification fails and Impetus surfaces: "The fix didn't fully resolve the issue — want to re-trace or apply a different fix level?"
**And** the developer controls whether to re-trace — the flywheel never automatically restarts

---

### Story 6.5: Practice Health Metric and Fix Level Tracking

As a developer,
I want to see the ratio of upstream fixes to code-level patches,
So that I know whether my practice is improving or just accumulating code debt.

**Acceptance Criteria:**

**Given** findings have been resolved over time (FR33)
**When** Impetus computes the practice health metric
**Then** it calculates: `upstream_fix_ratio = upstream_fixes / total_fixes` where `upstream_fixes` = entries where `upstream_fix_applied: true` AND `upstream_fix_level != "one-off-code-fix"`, and `total_fixes` = all entries where `upstream_fix_applied: true` — computed across ALL projects in the global ledger
**And** this ratio represents: of all fixes applied so far, what fraction reached a root level (spec, rule, tooling, or workflow) vs. staying in code — a value of 0% means every fix was a patch; 100% means every fix reached root cause
**And** a ratio ≥ 0.5 is reported as healthy: `✓ practice health: [N]% upstream fixes — the practice is compounding`
**And** a ratio < 0.5 is reported as degraded: `! practice health: [N]% upstream fixes — most fixes are patches, not root fixes`
**And** if fewer than 5 fixes exist, the metric is reported as `◦ practice health: insufficient data ([N] fixes recorded)`
**And** per-project breakdown is available on request: Impetus can compute and display the metric grouped by `project` field

**Given** the practice health metric is degraded
**When** Impetus surfaces it at session start or retrospective
**Then** Impetus offers context: "Most recent code-level patches: [top 3 by severity]" and asks if the developer wants to run the flywheel on any of them
**And** Impetus does not force a flywheel run — it offers, never blocks (FR31)

**Given** an upstream fix is applied (FR32)
**When** the flywheel records the fix in the Log phase
**Then** the findings journal entry is updated: `upstream_fix_applied: true`, `upstream_fix_ref` set to the id of the fix artifact (rule file modified, spec corrected, workflow updated)
**And** the `upstream_fix_level` field in the journal entry is set to one of: `spec-generating-workflow` | `specification` | `rules-or-CLAUDE.md` | `tooling` | `one-off-code-fix`
**And** all five fix levels are valid — the flywheel accepts `one-off-code-fix` as a legitimate choice when the root cause is genuinely isolated to a single code location

**Given** a retrospective runs (via BMAD retrospective or explicit request)
**When** Impetus contributes to the retrospective input
**Then** it includes a findings summary using the following structure:
- Total findings: [N] ([C] critical, [H] high, [M] medium, [L] low)
- Systemic patterns: [tag-1] ([N] stories), [tag-2] ([N] stories) — or "none detected"
- Practice health: [upstream_fix_ratio]% upstream fixes ([N] of [total] resolved)
- Top fixed patterns: [top 3 tags by fix count]
**And** this summary is included in the developer's response at the retrospective step — it is not passed directly to a BMAD agent; Impetus presents it and the developer decides how to incorporate it

---

## Epic 7: Bring Your Own Tools

A developer configures which agent, model, test framework, or MCP provider satisfies each protocol. Swapping any component doesn't touch workflow definitions. The practice layer is unchanged even when the tooling changes underneath it.

**FRs covered:** FR34, FR35, FR36, FR37, FR38
**NFRs covered:** NFR14, NFR15

### Story 7.1: Project Configuration File Defines Protocol Bindings

As a developer,
I want a single project configuration file that maps each integration protocol to its implementation,
So that Momentum knows which tools to use for this project and every workflow step uses the right one.

**Acceptance Criteria:**

**Given** Momentum is installed on a project (FR34)
**When** the project configuration file is initialized
**Then** `.claude/momentum/project-config.json` is created with a `protocol_bindings` object mapping protocol types to implementations
**And** each binding entry includes: `implementation` (the tool, skill, or command that satisfies the protocol), `configured_by` (who created the entry — `"impetus"` for agent-configured, `"developer"` for manually set), `configured_at` (ISO 8601 timestamp), `configured_why` (one sentence: the reason this implementation was chosen)
**And** the recognized protocol types at MVP are: `atdd-tool`, `test-runner`, `lint-tool`, `code-reviewer`, `vfl-validator`, `research-provider` — additional types may be added; unrecognized types are ignored without error
**And** the protocol type registry and each type's interface contract are formally documented in `references/protocol-contracts.md` within the `momentum/` skill — this is the canonical authority for what each type means and what its implementation must produce
**And** the config file also includes a `host_environment` field: `"claude-code"` | `"cursor"` | `"cline"` | `"other"` — set by the developer during setup; used by Impetus to determine which environment-specific behaviors apply (e.g. Cursor tool ceiling check in NFR14)

**Given** a protocol binding is defined for `atdd-tool` (FR35)
**When** a developer reviews the project config
**Then** it contains: the test framework name, the command to run it, and a provenance record (configured_by, configured_at, configured_why) for the binding
**And** the full config file is committed to the project repository — it is part of the project's practice infrastructure, not a developer-local setting

**Given** a binding is updated (implementation changed or command modified)
**When** the update is written
**Then** the previous binding is replaced and the new configured_at and configured_why are set — the config does not maintain history (history is in git)
**And** Impetus surfaces the change summary: "`atdd-tool` binding updated: [old] → [new] — reason: [why]"

---

### Story 7.2: Protocol Gap Resolution Creates Valid Config Entries

As a developer,
I want Impetus to guide me through configuring missing protocol bindings conversationally,
So that when a tool is undefined I come out of the conversation with a working config entry, not just an error message.

**Acceptance Criteria:**

**Given** Impetus detects a gap in the protocol mapping (FR36)
**When** it surfaces the gap (gap detected when: `project-config.json` is absent, a required `protocol_bindings` key is missing, or a workflow step invokes a protocol type with no binding)
**Then** Impetus does not stop at "X is missing" — it enters a guided configuration conversation:
  1. Names the protocol and explains what it does: "The `atdd-tool` protocol is the tool Momentum uses to generate acceptance tests. Which test framework does this project use?"
  2. Accepts the developer's answer, asks for the run command: "What command runs your ATDD test generation? (e.g. `cucumber`, `behave`, `npx jest --testPathPattern=acceptance`)"
  3. Asks for the reason: "One sentence: why this framework for this project?"
  4. Shows the would-be config entry and asks for confirmation before writing
**And** the conversation ends with a valid `project-config.json` entry written — not just guidance
**And** if the gap is detected during an automated execution (no active user session — e.g. a hook fires and encounters a missing binding), Impetus logs the gap to the session journal as an open thread and surfaces it at the next session start: "A protocol gap was detected during [workflow step] — want to configure it now?"

**Given** the developer cannot answer a configuration question (e.g. "I don't know which test framework is configured")
**When** Impetus receives "I don't know"
**Then** Impetus offers to inspect the project: "Let me check your project files for clues" — reads `mise.toml`, `package.json`, `build.gradle`, `pyproject.toml`, or equivalent
**And** when inferring the `atdd-tool` binding, Impetus looks for ATDD-specific frameworks (Cucumber, Behave, Gherkin processors, JBehave, SpecFlow) — not general test runners; if only a general test runner is found, Impetus says "I found [test-runner], but `atdd-tool` needs a Gherkin/ATDD framework — do you have one installed?"
**And** proposes a candidate for the correct protocol type: "Looks like you're using [framework] — want me to configure `atdd-tool` to use it?"
**And** still asks for confirmation before writing — inferred entries are never silently committed

**Given** a configured implementation is later found to be wrong (wrong command, tool not installed)
**When** a workflow step fails because the implementation is unavailable
**Then** Impetus surfaces the failure with the protocol binding context: "`atdd-tool` is configured as [command] — this command returned an error. Want to update the binding?"
**And** re-enters the configuration conversation to resolve it

---

### Story 7.3: Workflow Steps Resolve Through Protocol Interfaces at Invocation Time

As a developer,
I want workflow definitions to name what kind of tool they need — not which specific tool — so that the right tool for this project is always used automatically,
So that a workflow written for Playwright still works when I switch to Cypress, without editing the workflow.

**Acceptance Criteria:**

**Given** a Momentum workflow SKILL.md references an integration point (FR37, NFR8)
**When** the workflow is authored
**Then** it references a protocol type (e.g. `atdd-tool:run`, `test-runner:run`, `vfl-validator:validate`), not a specific implementation name or command
**And** no Momentum workflow SKILL.md hard-codes project-specific tool names (e.g. `playwright`, `jest`, `npm test`) in its integration-point instruction steps — this prohibition applies to integration-point invocations only; native Claude Code tool calls (Read, Edit, Bash, Agent) are permitted and are not "protocol implementations" under NFR8's definition
**And** compliance is verified by workflow authoring review against `references/protocol-contracts.md` — the reviewer confirms that each integration-point step references a registered protocol type, not a named implementation

**Given** Impetus executes a workflow step that invokes a protocol type
**When** the step fires
**Then** Impetus reads `project-config.json` at invocation time and looks up the implementation bound to that protocol type
**And** it invokes the bound implementation — the workflow step has no direct knowledge of which tool runs
**And** if the protocol type has no binding in the config (or project-config.json is absent entirely), Impetus triggers the gap resolution flow (Story 7.2) before continuing — it does not silently skip or substitute a default

**Given** a project-config.json binding is changed from implementation A to implementation B
**When** any workflow step next invokes that protocol type
**Then** the new implementation B is used — no changes to any SKILL.md file are needed
**And** this swap is the complete required change (FR38): one config file update, zero workflow file changes

---

### Story 7.4: Protocol Substitution Satisfies Interface Contract

As a developer,
I want Momentum to validate that a substitute implementation satisfies the protocol contract before accepting the binding,
So that swapping a tool doesn't silently break every workflow that depends on it.

**Acceptance Criteria:**

**Given** a developer configures a new implementation for a protocol (FR38, NFR15)
**When** the binding is proposed during the configuration conversation (Story 7.2)
**Then** Impetus validates the interface contract: it checks that the proposed command exists and is executable in the project environment
**And** if the implementation is a Momentum skill (e.g. substituting `momentum-code-reviewer` with a custom `my-code-reviewer` skill), Impetus checks two things: (1) the skill's SKILL.md frontmatter contract (context, allowed-tools) AND (2) the skill's expected output format (does it return structured JSON matching the subagent output contract `{status, result, question, confidence}`?)
**And** if validation fails, the binding is not written and Impetus explains what the contract requires: "`vfl-validator` requires a skill with `context: fork`, `allowed-tools: Read`, and JSON output matching `{status, result: {findings: [...]}, question, confidence}` — the proposed skill does not match"

**Given** a binding is validated and accepted
**When** any consuming workflow invokes the protocol
**Then** the consuming workflow receives the implementation's output in the format it expects — defined by the protocol's interface contract
**And** the protocol's interface contract is documented in `references/protocol-contracts.md` within the `momentum/` skill — this file defines for each protocol type: the invocation contract (frontmatter requirements if a skill), the output contract (exit codes or structured JSON schema), and a human-readable description of what the protocol does

**Given** a consuming workflow fails after a substitution
**When** the failure is diagnosed
**Then** Impetus identifies whether the failure is a contract violation (implementation output does not match expected schema) or a configuration error (wrong command, wrong path)
**And** contract violation failures are surfaced with the protocol name and the expected vs. actual output format: "`atdd-tool` expected exit-code 0 for success and exit-code 1 for failure — received [exit code]"
**And** Impetus offers to re-enter the binding configuration conversation to resolve the violation

---

### Story 7.5: MCP Provider Registration and Cursor Tool Ceiling Compliance

As a developer,
I want Momentum to track MCP providers and warn me when I'm approaching the Cursor tool limit,
So that I don't accidentally make my Cursor environment non-functional by enabling too many tools.

**Acceptance Criteria:**

**Given** an MCP provider is added to the project's Momentum configuration (NFR14)
**When** Impetus registers the provider
**Then** it determines the host environment from `project-config.json`'s `host_environment` field — if `"cursor"`, the ceiling check applies; otherwise it is skipped
**And** it counts active MCP tools using the tool-count registry in `references/mcp-tool-counts.md` (a curated lookup of known MCP servers → tool count); for MCP servers not in the registry, Impetus asks the developer: "How many tools does [provider] expose?" and adds the declared count
**And** if total count ≥ 35 tools (approaching the ~40 ceiling), Impetus warns: `! Cursor tool ceiling — adding [provider] brings total to [N]/~40 tools; approaching Cursor limit. Proceed?`
**And** if total count > 40, Impetus warns more urgently: `! Cursor tool ceiling — adding [provider] brings total to [N] tools — exceeds Cursor's ~40 limit. Proceed anyway?`
**And** if the developer proceeds past 40, Impetus notes which providers may need to be selectively disabled

**Given** Momentum's own MCP servers are configured (findings MCP)
**When** tool count is computed
**Then** Momentum's own MCP servers count toward the ceiling — they are not exempt
**And** the count includes both Momentum-registered providers and any pre-existing MCP servers in the project's `.mcp.json`

**Given** a project's `host_environment` is not `"cursor"`
**When** MCP provider configuration runs
**Then** the tool ceiling check is skipped — no warning is shown
**And** all MCP providers that were configured function identically regardless of the host tool (protocol-level behavior, not tool-specific behavior)

---

## Epic 8: Research & Knowledge Management

A developer runs multi-model research with freshness guarantees. Research prompts are date-anchored. Documents have domain-specific freshness windows. Outdated docs are archived with their reference chain intact.

**FRs covered:** FR44, FR45, FR46, FR47
**Additional:** Gemini MCP + GPT MCP integration (growth), hybrid research workflow (PT-020), freshness windows per domain
**Priority:** Growth
**UX-DRs covered:** UX-DR5 (research findings surfaced in Impetus's voice), UX-DR8 (warnings are advisory — do not block flow), UX-DR15 (response follows orientation → substantive content → transition signal → user control)

### Story 8.1: Multi-Model Research Workflow Active

As a developer,
I want to run research across multiple AI models using MCP-integrated providers,
So that I can cross-validate findings and reduce the risk of single-model hallucination in research artifacts.

**Acceptance Criteria:**

**Given** the multi-model research workflow is configured (FR44)
**When** a developer runs a research task via Impetus
**Then** Impetus dispatches the research query to multiple providers in parallel — at minimum two distinct providers from: `@rlabs-inc/gemini-mcp`, GPT deep research MCP, or any provider bound to the `research-provider` protocol (Story 7.1)
**And** each provider runs independently — providers do not see each other's output during generation
**And** Impetus synthesizes the results from all providers and presents a cross-validated summary in Impetus's voice (UX-DR10) — raw provider output is never shown directly

**Given** the research providers return results
**When** Impetus synthesizes the cross-model output
**Then** it identifies claims where providers agree (high confidence), claims where they differ (flagged for manual verification), and claims present in only one provider's output (flagged as single-source)
**And** each synthesized claim carries a `research_confidence` field — `CORROBORATED` (all providers agree), `DIVERGENT` (providers disagree — flagged for manual review), or `SINGLE_SOURCE` (only one provider cited this claim) — this vocabulary is orthogonal to FR16's epistemic vocabulary and does not redefine any FR16 terms
**And** the research output carries `authored_by: ai` and `sourced_date` frontmatter reflecting the date of the research run

**Given** a research provider is unavailable at research time
**When** Impetus dispatches the research query
**Then** it proceeds with the remaining available providers — single-provider results are flagged as `single_source: true` in the output
**And** Impetus surfaces: `! research ran on [N] of [M] providers — [provider] was unavailable. Results are single-source for this run.`

**Given** a research provider returns a result (FR44, Architecture Decision 3b)
**When** Impetus processes the provider's output
**Then** the provider's response conforms to the structured output contract `{status, result, question, confidence}` before synthesis proceeds
**And** if a provider returns malformed output (missing required fields), Impetus treats that provider as unavailable for this run and surfaces: `! [provider] returned malformed output — excluded from synthesis`
**And** Impetus never exposes raw provider JSON to the developer — only the synthesized narrative in Impetus's voice (UX-DR10)

---

### Story 8.2: Research Prompts Are Date-Anchored with Primary-Source Directives

As a developer,
I want every research prompt to include the current date and a directive to cite primary sources,
So that research agents can't silently use outdated knowledge and research outputs are traceable.

**Acceptance Criteria:**

**Given** Impetus constructs a research prompt (FR45)
**When** the prompt is sent to any research provider
**Then** it includes a date-anchor directive: "Today's date is [ISO 8601 date]. Only consider information that was accurate as of this date. If your training data predates this date, say so."
**And** it includes a primary-source directive: "Cite primary sources for every significant claim. Do not cite secondary summaries or blog posts as the primary reference. If the primary source is unavailable, say the claim is unverified."
**And** these directives are injected automatically — the developer does not need to manually include them in their research query

**Given** Impetus constructs a research prompt but `currentDate` is not available in context
**When** the prompt is sent to a research provider
**Then** Impetus omits the date-anchor directive and sets `date_unchecked: true` in the artifact's frontmatter
**And** Impetus surfaces: `! currentDate unavailable — research prompt was sent without a date anchor. Results may use outdated training data.`
**And** the research run still proceeds — missing currentDate is a degraded-mode warning, not a blocking error

**Given** a research result is produced with these directives
**When** Impetus records the output as a research artifact
**Then** the artifact's frontmatter records: `sourced_date` (the date of the research run), `research_providers` (the list of providers used), and `authored_by: ai`
**And** the artifact's derives_from block includes one entry per provider used, with `sourced_date` set to the research date and `relationship: derives_from`
**And** derives_from entries for MCP provider invocations are point-in-time snapshots — they are not subject to time-based staleness scanning (Story 5.4); only persistent document paths are scanned for staleness

**Given** a research prompt covers a time-sensitive domain (AI/LLM, tooling)
**When** the date-anchor is applied
**Then** Impetus additionally warns the developer: "This research covers [domain] — results may be outdated within [freshness_window] days (FR47 domain window). Plan to re-verify on [sourced_date + freshness_window]."
**And** this warning is advisory — it does not block the research run

---

### Story 8.3: Domain-Specific Freshness Windows Define Document Currency

As a developer,
I want documents to carry domain-specific freshness windows so I know when to re-verify,
So that I'm not relying on a research doc that was current 18 months ago in a field that moves every 90 days.

**Acceptance Criteria:**

**Given** a document is classified by domain (FR47)
**When** the provenance scanner evaluates its currency
**Then** it applies the canonical freshness window for that domain:
- AI/LLM domain: 90 days
- Tooling/frameworks domain: 180 days (6 months)
- Standards/specifications domain: 365 days (12 months)
- Principles/fundamentals domain: 730 days (24 months)
**And** this taxonomy is the authoritative source referenced by Story 5.4 — freshness windows in Story 5.4 defer to this list

**Given** a document has no explicit domain classification
**When** the freshness window is applied
**Then** Impetus uses the document's title and `derives_from` relationship types to infer the most likely domain from the FR47 taxonomy
**And** if domain cannot be inferred, the Tooling/frameworks window (180 days) is applied as the conservative default — this matches the FR47 tier, not a separate general-research category — and Impetus prompts the developer to set an explicit domain classification

**Given** a developer sets an explicit `freshness_window` in document frontmatter or a `derives_from` entry
**When** the scanner evaluates staleness
**Then** the explicit value takes precedence over the domain taxonomy default
**And** the scanner records which rule was applied: `domain_default` | `explicit_override` — so reviewers can see why a particular window was used

**Given** the freshness window taxonomy is updated (e.g. a new domain tier is added)
**When** the update is applied to `references/provenance-scan.md`
**Then** documents with `explicit_override` are not affected — their override remains authoritative
**And** all other documents will pick up the new taxonomy on their next scanner evaluation — no batch re-evaluation trigger is needed since the scanner reads the taxonomy at evaluation time

---

### Story 8.4: Outdated Documents Archived with Reference Chain Intact

As a developer,
I want to archive outdated documents rather than delete them,
So that reference chains remain valid and I can trace what changed and why.

**Acceptance Criteria:**

**Given** a document is identified as outdated (SUSPECT status confirmed by developer, or freshness window exceeded and developer elects to archive) (FR46)
**When** Impetus archives the document
**Then** it moves the file to `docs/archive/[original-relative-path]` (preserving directory structure within the archive)
**And** the document's frontmatter is updated with: `archived_at` (ISO 8601 timestamp), `archived_by` (`"impetus"` or `"developer"`), `archived_reason` (one sentence)
**And** if the archive was triggered by a confirmed-SUSPECT finding, `archived_reason` includes the findings-journal entry ID: `"confirmed-suspect: [finding-id]"` — linking the archive decision to its audit trail
**And** the document retains its full `derives_from` block — the reference chain is preserved in the archive

**Given** the archive target path matches the protected spec pattern (`_bmad-output/planning-artifacts/*.md`)
**When** Impetus attempts the archive operation
**Then** the operation is rejected — Impetus surfaces: `! [path] is a protected spec file and cannot be archived. Protected spec files must be managed by their authoring workflow.`
**And** the rejection is non-negotiable — no confirmation prompt is offered for protected paths

**Given** other documents reference the archived document via `derives_from`
**When** the archive operation completes
**Then** Impetus scans the `referenced_by` graph (Story 5.2) for all documents that cited the now-archived document
**And** it offers to update each referencing document's `derives_from` entry `path` to the new archive path: "3 documents reference [doc] — update their derives_from paths to the archive location?"
**And** if the developer confirms, the paths are updated — if they decline, the stale paths remain and Impetus flags them as SUSPECT for the next scan
**And** after any path updates are applied (or declined), the `referenced_by` graph is rebuilt to reflect the new archive path — referencing documents that were updated now point to the archive location in the graph

**Given** a developer wants to un-archive a document
**When** they request restoration
**Then** Impetus moves the file back to its original path, removes the `archived_at`, `archived_by`, and `archived_reason` fields, and offers to restore the derives_from paths in referencing documents
**And** the git history preserves the archive/restore cycle — no data is ever deleted, only moved

---

## Epic 9: Performance Validation

A developer benchmarks BMAD skills and sub-agents across model tiers to validate that the default model/effort routing decisions (FR23) are grounded in measured performance, not assumption. Benchmarking results feed back into skill frontmatter updates.

**FRs covered:** FR23
**Scope:** PT-022 — promptfoo config, bash benchmarking script, golden dataset starter, Pydantic AI harness with `agent.override()`, updated `model:`/`effort:` frontmatter based on results
**Priority:** Growth (requires Epics 2–4 to have real skills to benchmark)
**UX-DRs covered:** UX-DR8 (benchmark warnings advisory), UX-DR16 (benchmark results surfaced in Impetus's voice before developer acts on them)

### Story 9.1: Promptfoo Configuration Benchmarks Skills Across Model Tiers

As a developer,
I want a promptfoo configuration that runs BMAD skills across Opus, Sonnet, and Haiku,
So that I have empirical quality, cost, and latency measurements to validate default model routing decisions.

**Acceptance Criteria:**

**Given** a `promptfooconfig.yaml` is present in `docs/benchmarking/` (PT-022) (FR23)
**When** a developer runs `promptfoo eval`
**Then** it tests at minimum two Momentum skills (one complex — e.g. `/momentum-vfl` — and one constrained — e.g. `/momentum-create-story`) across at minimum three model variants: `claude-opus-4-6`, `claude-sonnet-4-6`, and `claude-haiku-4-5-20251001`
**And** skill execution uses the Claude Agent SDK provider (`anthropic:claude-agent`) so that full skill workflows run rather than raw model completions
**And** `temperature: 0` is set for all model variants to minimize variance between runs
**And** cost and latency metrics are captured per run — `cost` and `latency` threshold assertions may optionally be added as budget gates but the metrics are recorded regardless

**Given** the promptfoo eval runs
**When** a skill execution produces output
**Then** quality is evaluated using `llm-rubric` with `claude-opus-4-6` as the grader model, applying a multi-dimensional rubric: accuracy, completeness, coherence, domain fitness, and usability — each scored on a 3-point scale (0 = fail, 1 = partial, 2 = pass) to minimize middle-clustering bias
**And** the rubric is defined in `docs/benchmarking/rubrics/general.yaml` and referenced by path in `promptfooconfig.yaml` — YAML anchors cannot be shared cross-file; the reference mechanism is a file path string, not a YAML alias

**Given** the eval runs multiple iterations for statistical consistency
**When** `evaluateOptions.repeat` is set
**Then** it is set to at minimum 5 (quick-check minimum per benchmarking guide statistical rigor standard) — single-run scores are not sufficient to route model decisions
**And** the eval output includes per-run scores, mean, and standard deviation so variance is visible alongside the mean

---

### Story 9.2: Bash Benchmarking Script Captures Time, Cost, and Tokens

As a developer,
I want a bash script that benchmarks `claude -p` invocations across models,
So that I can measure wall time, API time, cost, and token counts without a full promptfoo setup.

**Acceptance Criteria:**

**Given** `docs/benchmarking/run_bench.sh` exists (PT-022)
**When** a developer runs it for a given prompt and target skill
**Then** it invokes `claude -p --model [model] --output-format json` for each model in the benchmark set (`claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`) sequentially
**And** it captures available timing and cost fields from the JSON output: wall time (derived from shell timing), cost (`cost_usd` field), total tokens, input tokens, output tokens — field names map to the actual `claude -p --output-format json` schema; if a field is absent, the column shows `N/A` rather than failing
**And** it writes a comparison table to stdout formatted as: `model | wall_time | cost | input_tokens | output_tokens | total_tokens`

**Given** the script runs all model variants
**When** the run completes
**Then** it optionally invokes an LLM judge using `claude-opus-4-6` as grader (`--judge` flag) to score the output of each variant using the rubric in `docs/benchmarking/rubrics/general.yaml`
**And** the judge output appends a `quality_score` column to the comparison table — the score is the mean across rubric dimensions (0–2 scale per Story 9.1); judge invocation cost is captured separately and printed after the table as `judge_cost_usd: [X]`
**And** if `--judge` is not passed, the table is printed without quality scores — the script is useful without judge invocation

**Given** a model invocation fails (timeout, API error, rate limit)
**When** the script encounters the error
**Then** it logs the failure, marks that row in the table as `FAILED`, and continues with remaining models — a single failure does not abort the benchmark run

---

### Story 9.3: Golden Dataset Provides Canonical Benchmark Inputs and Reference Outputs

As a developer,
I want a starter golden dataset with reference inputs and Opus-reviewed outputs per skill type,
So that quality regressions are detectable when model defaults are changed.

**Acceptance Criteria:**

**Given** `docs/benchmarking/golden/` exists (PT-022)
**When** a developer inspects it
**Then** it contains at minimum one golden case per benchmarked skill type (e.g. `momentum-vfl.yaml`, `momentum-create-story.yaml`) — each golden case is structured as a promptfoo-native test fixture with `vars:` (the prompt/input), `assert:` (rubric assertions), and a `description:` label; a separate `_metadata.yaml` sidecar records human-review provenance: `reference_model`, `reference_effort`, `reviewed_by`, `reviewed_date`

**Given** a golden case is created
**When** a new reference output is generated
**Then** it is generated by `claude-opus-4-6` at `high` effort and reviewed by a human before being committed as canonical — automated outputs alone are not sufficient for golden cases
**And** the `_metadata.yaml` sidecar records `reference_model: claude-opus-4-6` and `reference_effort: high` — both are required so future re-benchmarks run under comparable conditions
**And** "≥90% of the Opus reference" means a cheaper model's mean rubric dimension score is ≥90% of the Opus reference mean score (e.g., if Opus mean = 1.8/2.0, ≥90% threshold = 1.62/2.0) — this definition is canonical for Stories 9.3, 9.4, and 9.5

**Given** a promptfoo eval or bash benchmark run uses the golden dataset
**When** outputs are compared against reference
**Then** promptfoo consumes the golden cases as test fixtures via `tests:` in `promptfooconfig.yaml` — the cases use promptfoo-native format (no transform step required)
**And** any output scoring below 80% of the Opus reference mean score on any rubric dimension is flagged as a quality regression; scores in the 80–89% range are advisory ("below routing threshold but not a regression") — no action is required in this band, but it is surfaced for awareness

---

### Story 9.4: Pydantic AI Harness Benchmarks Agent Workflows with agent.override()

As a developer,
I want a Pydantic AI benchmarking harness that switches models via `agent.override()`,
So that I can benchmark full agent workflows in Python with precise token and cost tracking.

**Acceptance Criteria:**

**Given** `docs/benchmarking/pydantic_bench.py` exists (PT-022)
**When** a developer runs it with a target agent module path as argument (e.g. `python pydantic_bench.py agents.validate`)
**Then** it imports the specified agent, runs it against a benchmark prompt using `with agent.override(model='anthropic:[model]'):` (context manager pattern) for each model in the benchmark set (`claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`)
**And** it captures `result.usage()` for each run and produces a comparison table: model, cost (USD), input tokens, output tokens, run time

**Given** the Pydantic AI harness runs a benchmark
**When** `result.usage()` is captured
**Then** it records the available usage fields from the Pydantic AI usage object — field names should match the installed version's API; the script includes a comment noting the version it was validated against
**And** cost is computed as `(input_tokens / 1M) * input_price + (output_tokens / 1M) * output_price` — the script includes a `PRICING` constants dict with a `last_updated` date; if `last_updated` is more than 90 days old, the script prints: `! pricing constants may be stale — update PRICING dict before trusting cost estimates`

**Given** the harness runs the same agent across 3+ models
**When** all runs complete
**Then** the script prints: "Routing note: if Story 9.1 or 9.3 rubric scoring shows [model] ≥90% of opus-4-6 reference AND cost is lower, consider setting model: [model] in this agent's frontmatter."
**And** this recommendation is advisory and references the rubric scoring threshold defined in Story 9.3 — the harness captures cost and tokens only; quality scoring requires a separate promptfoo eval run; the developer combines both before making routing decisions
**And** the script never modifies skill or agent files

---

### Story 9.5: Benchmark Results Drive model:/effort: Frontmatter Updates in Skill Files

As a developer,
I want a workflow to update `model:` and `effort:` frontmatter in skill files based on benchmark findings,
So that routing decisions are grounded in measured evidence and documented with the evidence that justified the change.

**Acceptance Criteria:**

**Given** a benchmark run (Story 9.1, 9.2, or 9.4) produces results showing a cheaper model achieves ≥90% of the Opus reference mean rubric score (per the threshold defined in Story 9.3) at lower cost (FR23)
**When** a developer elects to update a skill's routing
**Then** the skill's `model:` and `effort:` frontmatter is updated to the benchmarked model
**And** a `benchmark_basis` frontmatter field is added as a human-readable string recording: date, score achieved vs. reference, and path to the benchmark results file — e.g. `benchmark_basis: "2026-03-20: sonnet-4-6 scored 92% of opus-4-6 reference (Story 9.3 threshold); see docs/benchmarking/results/2026-03-20-validate.json"` — this field is documentation; it is not machine-parsed by any workflow

**Given** a skill uses the cognitive hazard rule (Opus required for outputs without automated downstream validation) (FR23)
**When** a benchmark shows a cheaper model achieves high quality scores
**Then** the cognitive hazard rule overrides the benchmark recommendation — the developer must not route to a cheaper model unless they have added automated validation that will catch invisible errors in that skill's output
**And** the developer is responsible for checking this before committing the routing change — no automated enforcement is provided in this story; the rule is documented in FR23 and must be applied manually

**Given** benchmark results are committed to the repository
**When** the developer commits updated frontmatter
**Then** the benchmark results file is committed under `docs/benchmarking/results/[date]-[skill].json` so the routing decision is auditable
**And** both commits — the skill frontmatter update and the results file — are made together or in immediate succession so the audit trail is never split



---

## P{n} — Process Sprint-{n} (placeholder)

Each sprint has a corresponding process epic `P{n} — Process Sprint-{n}`. Process stories capture dev-environment and practice improvement work (skills, rules, hooks, tooling) that doesn't belong in product epics. Process story keys follow the format `p{sprint}-{n}-{title}` (e.g., `p1-1-momentum-plan-audit-skill`). Process stories are tracked in `sprint-status.yaml` (`development_status` + `momentum_metadata`) — this epic is a convention anchor, not a story registry.
