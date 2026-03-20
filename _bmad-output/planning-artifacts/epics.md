---
stepsCompleted:
  - step-01-validate-prerequisites
  - step-02-design-epics
  - step-03-epic-1-stories
  - step-03-epic-2-stories-vfl-gate-applied
  - step-03-epic-3-stories-vfl-gate-applied
inputDocuments:
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/ux-design-specification.md
lastEdited: '2026-03-20'
editHistory:
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
FR30: Flywheel can explain detected issues and suggest upstream trace with visual workflow status (detection → review → upstream trace → solution → verify)
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
- Session ledger stored at `.claude/momentum/ledger.json`; auto-generated `.claude/momentum/ledger-view.md` for human readability
- Findings ledger stored at `.claude/momentum/findings-ledger.json` with structured schema: id, story_ref, phase, severity, pattern_tags, description, evidence, provenance_status, upstream_fix_applied, upstream_fix_ref, timestamp
- Only the flywheel workflow writes to findings ledger; Impetus reads at retrospective and upstream trace

**From Architecture — Security & File Protection**
- PreToolUse hook must block writes to: `tests/acceptance/` and `**/*.feature`, `_bmad-output/planning-artifacts/*.md`, `.claude/rules/`, `.claude/momentum/findings-ledger.json`
- Agents may not remove or modify `derives_from` frontmatter in spec files
- Every significant claim classified as SOURCED / DERIVED / ADDED / UNGROUNDED

**From Architecture — MCP Servers**
- MVP: `@modelcontextprotocol/server-git` (file history, blame, diff for provenance) + Momentum findings MCP (custom, lightweight — read/write findings-ledger.json)
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

UX-DR1: Implement Session Ledger Display component — numbered list of open threads with workflow phase + elapsed time; appears at every session start with open threads; absent on first-time user (no ledger exists). States: single thread, multiple threads, empty (first time).

UX-DR2: Implement Progress Indicator component — always exactly 3 lines using ✓/→/◦ symbol vocabulary; completed steps collapse to single ✓ line with value summary; current step stands alone with one-phrase description; upcoming steps collapse to single ◦ line. Appears at workflow entry and every phase transition.

UX-DR3: Implement Hook Announcement component — pass: one-line `[hook-name] ✓ checked [what] — [result]`; fail: hook name + specific issue + file:line + likely cause. Never silent, never verbose. Every hook, every fire.

UX-DR4: Implement Workflow Step component — orientation line (never "step N/M"), substantive content, transition signal, explicit user control [A/P/C or equivalent]. Most frequent pattern in the system.

UX-DR5: Implement Completion Signal component — explicit ownership return ("this is yours to review and adjust"), what was produced (file list), what's next question. Every story cycle and workflow completion must use this.

UX-DR6: Implement Subagent Return component — Impetus's voice synthesizes subagent findings; severity indicators (! critical, · minor); critical findings surface flywheel trigger. User never sees raw subagent output.

UX-DR7: Implement Flywheel Notice component — surfaced after upstream fix applied; shows finding, root cause, fix applied, what it prevents. Makes invisible improvement visible.

UX-DR8: Implement Proactive Orientation component — surfaces knowledge gap or about-to-be-skipped step detection; offers, never blocks; decision always returned to user. Fires only when conversational floor is open.

UX-DR9: Implement consistent Symbol Vocabulary across all agents and hooks: ✓ completed/passing, → current/active, ◦ upcoming/pending, ! warning/attention, ✗ failed/blocked, ? question/decision. Symbols always paired with text — meaning must survive any rendering context.

UX-DR10: Implement Hub-and-Spoke Voice Contract — Impetus is the sole user-facing voice; all subagents return structured JSON `{status, result, question, confidence}`; subagent identity never surfaces to user; Impetus synthesizes before presenting.

UX-DR11: Implement Session Orientation Contract — at every session start, Impetus reads ledger and within two exchanges surfaces: active story/task, current phase, last completed action, suggested next action. Agent speaks first; user never hunts for context.

UX-DR12: Implement Productive Waiting pattern — while a background subagent runs, Impetus maintains dialogue on the same topic (never context-switches). Dead air is a failure mode. Brief acknowledged pauses acceptable for very short tasks only.

UX-DR13: Implement Multi-Thread Ledger Awareness — each Impetus instance (per Claude Code tab) reads/writes the shared ledger; recently-timestamped entries signal intentional concurrent work; conflicting thread starts flagged with user decision required.

UX-DR14: Implement Thread Hygiene — surface dormant threads beyond a threshold; low-friction closure (one confirmation); contextually triggered when dependent work completes or ledger grows unwieldy.

UX-DR15: Implement Response Architecture Pattern — every agent response follows: orientation line → substantive content → transition signal → user control. Orientation line is narrative (never "step N/M"); user control always last and always visible.

UX-DR16: Implement Input Interpretation patterns — number selects ledger item; letter command is case-insensitive; fuzzy match (continue/yes/go ahead = C); natural language extracts intent and confirms; ambiguous input triggers one clarifying question (never two).

UX-DR17: Implement Workflow Resumability — every workflow must be resumable from any step; sufficient context saved in ledger entry to re-orient a fresh agent session without user re-explanation. Step re-entry after interruption always confirms ("continue from here, or restart this step?").

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
**NFRs covered:** NFR1–13 (portability, resilience, compatibility, token budget architecture decision)
**Additional:** Repo structure, skills/rules layout, version.md, cost observability (showTurnDuration, ccusage recommendation)
**Priority:** Day 1

---

### Epic 2: Stay Oriented with Impetus
A developer always knows where they are and what to do next. Session ledger tracks open threads across tabs and sessions. Visual progress answers "what have we built, what are we doing, what's next" at every transition. Impetus's unified voice keeps backstage invisible.
**FRs covered:** FR6, FR7, FR8, FR9, FR10, FR11
**NFRs covered:** NFR1, NFR2, NFR3
**UX-DRs covered:** UX-DR1, UX-DR2, UX-DR4, UX-DR5, UX-DR9, UX-DR10, UX-DR11, UX-DR12, UX-DR13, UX-DR14, UX-DR15, UX-DR16, UX-DR17, UX-DR18
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
**Additional:** code-reviewer (`context:fork` skill, `allowed-tools: Read`), VFL flat skill (momentum-vfl), create-story skill, dev-story skill, ATDD workflow
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
**Additional:** findings-ledger.json (with full schema), upstream-fix skill (momentum-upstream-fix), flywheel workflow, Momentum findings MCP server
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

A developer always knows where they are and what to do next. Session ledger tracks open threads across tabs and sessions. Visual progress answers "what have we built, what are we doing, what's next" at every transition. Impetus's unified voice keeps backstage invisible.

**FRs covered:** FR6, FR7, FR8, FR9, FR10, FR11
**NFRs covered:** NFR1, NFR2, NFR3
**UX-DRs covered:** UX-DR1, UX-DR2, UX-DR4, UX-DR5, UX-DR6, UX-DR9, UX-DR10, UX-DR11, UX-DR12, UX-DR13, UX-DR14, UX-DR15, UX-DR16, UX-DR17, UX-DR18
**Note:** UX-DR3 (Hook Announcement) → Epic 3. UX-DR7 (Flywheel Notice) → Epic 6. UX-DR8 (Proactive Orientation) — the proactive-offer-never-block pattern is established here in Stories 2.2/2.5 and fully exercised once story cycles (Epic 4) provide real workflow steps.

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
**Then** a number selects the corresponding ledger item or menu item
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

**Given** the ledger at `.claude/momentum/ledger.json` contains one or more open thread entries
**When** Impetus starts (UX-DR1)
**Then** Impetus displays the Session Ledger: numbered list of open threads, each showing workflow phase and elapsed time
**And** threads are ordered by most-recently-active
**And** each thread is directly selectable by its number

**Given** no ledger exists or the ledger is empty (user has never started a workflow — `installed.json` exists but no ledger entries)
**When** Impetus starts
**Then** the Session Ledger display is absent
**And** Impetus transitions directly to new-session orientation
**Note:** If `installed.json` does not exist, Story 1.3 (FR2) governs — this AC applies only to post-install sessions with no prior workflow activity.

**Given** a developer is running a workflow in Tab A
**When** they open Tab B and invoke `/momentum` (UX-DR13)
**Then** Impetus in Tab B reads the shared ledger and surfaces Tab A's active thread
**And** if the entry was timestamped within the last 30 minutes, Impetus flags it as likely intentional concurrent work
**And** asks the developer to confirm before starting a competing thread on the same story

**Given** a ledger entry has had no activity beyond the configured dormancy threshold (default: 3 days)
**When** Impetus starts (UX-DR14 — time-based trigger)
**Then** Impetus surfaces the dormant thread with brief context and offers one-action closure ("is this thread complete?")
**And** closure requires exactly one developer confirmation
**And** if the developer confirms, the thread is marked closed in the ledger

**Given** a story or workflow that another ledger thread depended on has just completed
**When** Impetus detects the dependency is satisfied (UX-DR14 — contextual trigger)
**Then** Impetus surfaces the waiting thread at session start: "The work this thread was waiting on is complete — ready to continue?"
**And** the developer decides whether to activate the waiting thread

**Given** the session ledger has grown to more than 5 open threads
**When** Impetus starts (UX-DR14 — unwieldy-ledger trigger)
**Then** Impetus flags the ledger size and offers a triage pass before starting new work
**And** triage surfaces each thread's status and age with a single-action close option

**Given** the developer starts Impetus in a fresh context after an interruption
**When** Impetus reads the ledger entry for the interrupted workflow (UX-DR17)
**Then** Impetus re-orients using saved ledger context — no developer re-explanation required
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
**Then** Impetus identifies the interrupted workflow from the ledger
**And** presents the Progress Indicator showing which steps are complete
**And** asks: "continue from here, or restart this step?"
**And** sufficient context is in the ledger entry to re-orient without developer re-explanation

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
**When** a Claude Code tool attempts to write to any path matching `tests/acceptance/`, `**/*.feature`, `.claude/rules/`, or `.claude/momentum/findings-ledger.json`
**Then** the PreToolUse hook fires and blocks the write before it executes
**And** returns an explanation of what was blocked and why

**Given** a PreToolUse hook blocks a write (UX-DR3)
**When** the hook fires
**Then** it outputs: `[file-protection] ✗ blocked write to [path] — [policy]: [reason]`
**And** the policy name and reason are specific (e.g. "acceptance-test-dir: no modification after ATDD phase begins")

**Given** a PreToolUse hook allows a write (non-protected path)
**When** the hook fires (UX-DR3)
**Then** it outputs: `[file-protection] ✓ [path] — ok`
**Note:** One compact line per write — UX-DR3 requires every hook fire to produce output; pass output must stay minimal to avoid noise on frequent writes

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

**Given** any Momentum workflow definition
**When** reviewed for Claude Code API references (NFR8)
**Then** no workflow definition invokes a Claude Code tool by name (e.g. no `Bash(git ...)`, no `Edit`, no `Read` called from workflow step logic)
**And** all workflow steps invoke protocol types by name (e.g. `code-reviewer:review`, `test-runner:run`) — the protocol implementation is resolved from the project config, not hard-coded
**And** "Claude Code-specific API" is defined as: any tool from the Claude Code tool set invoked by name in workflow SKILL.md instructions rather than via a protocol interface lookup

---

### Story 3.5: Model Routing Configured by Frontmatter

As a developer,
I want every Momentum skill and agent to have its model and effort level set by frontmatter,
So that the right model is used for every task automatically — no manual overrides needed.

**Acceptance Criteria:**

**Given** the model routing guide exists at `module/canonical/resources/model-routing-guide.md` (canonical source; also bundled into `skills/momentum/references/` for runtime access)
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
