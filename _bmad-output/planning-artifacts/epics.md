---
stepsCompleted:
  - step-01-validate-prerequisites
  - step-02-design-epics
  - step-03-epic-1-stories
inputDocuments:
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/ux-design-specification.md
lastEdited: '2026-03-20'
editHistory:
  - date: '2026-03-20'
    changes: 'Synced FR numbering with PRD edits: FR2 updated to solo first-install path; FR2b/FR2c added for Nth-run routing; FR3 decomposed to FR3a/FR3b/FR3c; FR5 updated to team member joining path; NFR1 corrected to ≤150 characters; NFR4 updated to remove plugin reference; Epic 1 FRs covered list updated; FR Coverage Map updated with new FR entries.'
---

# Momentum - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Momentum, decomposing the requirements from the PRD, UX Design, and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

**Installation & Deployment**
FR1: Developer can install Momentum skills via `npx skills add` into any Agent Skills-adopting IDE
FR2: Developer (solo, first install) runs `npx skills add momentum/momentum -a claude-code` then `/momentum`; Impetus detects no `installed.json`, presents pre-consent summary of what will be configured, and with explicit confirmation completes setup and writes `installed.json` with `current_version`
FR2b: When Impetus starts and `installed.json` exists with `configured_for_version` matching `momentum-versions.json` `current_version`, Impetus skips install/upgrade flows and proceeds directly to session orientation
FR2c: When Impetus starts and `installed.json` exists but `configured_for_version` does not match `current_version`, Impetus triggers the upgrade flow (FR3b)
FR3a: Developer can run `npx skills update` to pull the latest Momentum package to disk; the updated package contains a revised `momentum-versions.json` with per-version action lists
FR3b: When Impetus starts and detects `momentum-versions.json` `current_version` differs from `installed.json` `configured_for_version`, Impetus presents a structured upgrade summary and requires explicit user confirmation before proceeding
FR3c: Impetus executes upgrade actions sequentially across all intermediate versions between `configured_for_version` and `current_version`, updating `installed.json` on successful completion; partial failures are reported with the step that failed
FR4: Team member can receive project-level Momentum configuration via `git clone` without manual setup
FR5: Developer joining a project that has `.claude/momentum/installed.json` committed but lacks global Momentum components on their machine runs `/momentum`; Impetus detects missing global components and guides one-time global setup without re-running the full install sequence

**Orchestrating Agent**
FR6: Developer can interact with an orchestrating agent that presents menu-driven access to all practice workflows
FR7: Orchestrating agent can show the developer's current position in any workflow via visual status graphics (ASCII)
FR8: Orchestrating agent can provide human-readable summaries of what was built during implementation, while review runs
FR9: Orchestrating agent can detect ambiguous or missing project configuration and guide the developer through resolution conversationally
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
FR20: System can run conditional quality gates before session end — tests only when code was modified, lint always (Stop hook)
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
FR37: System can resolve workflow step invocations through protocol interfaces — workflow definitions reference protocol types, not specific implementations
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
NFR7: Enforcement must degrade across three defined tiers: Tier 1 full deterministic (Claude Code + plugin), Tier 2 advisory (Cursor/other tools with skills only), Tier 3 philosophy only (no tooling). Each tier explicitly tested.
NFR8: No Momentum workflow definition may import or reference a Claude Code-specific API directly — workflows depend on protocol interfaces

**Ecosystem Resilience**
NFR9: A breaking change in any single ecosystem dependency must be absorbable by modifying only the packaging/distribution layer, not practice content
NFR10: All ecosystem dependencies (BMAD version, Claude Code plugin API, Agent Skills spec) must be tracked and reviewed monthly
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
- Starter template: No starter template specified. Momentum is greenfield — Epic 1 Story 1 establishes the repository structure per the architecture's documented layout (plugin/, skills/, rules/, mcp/, docs/)
- Plugin vs. flat skill classification rule must be implemented: context:fork = plugin agent (code-reviewer, architecture-guard); main context = flat skill (Impetus, VFL, upstream-fix, create-story, dev-story)
- Plugin and flat skills must share a single `version.md` at repo root; standard git pre-commit hook (Husky/pre-commit framework) validates they match
- Release tags must version both plugin and skills units together to prevent drift
- Global rules cannot be deployed silently by the plugin (verified March 17, 2026 limitation); `momentum setup` menu option in Impetus handles one-time interactive copy to `~/.claude/rules/`
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

**From Architecture — Spike Required**
- Spike: plugin-agent invocation mechanism must be verified before build. If plugin agents cannot be programmatically invoked by flat skills, code-reviewer and architecture-guard implemented as flat skills with Read-only tool restrictions instead of context:fork plugin agents. Producer-verifier separation preserved either way.

**From Architecture — BMAD Integration**
- BMAD enhancement touchpoints at MVP: (1) Any BMAD artifact generated → Impetus proposes derives_from frontmatter + git commit [Proposal]; (2) BMAD code-review complete → Impetus offers Momentum code-reviewer as additional adversarial pass [Proposal]; (3) BMAD dev-story complete → Impetus gates on acceptance tests passing before closing story [Gate — the only hard gate at MVP]; (4) BMAD retrospective → Impetus adds findings ledger summary [Proposal]

### UX Design Requirements

UX-DR1: Implement Session Ledger Display component — numbered list of open threads with workflow phase + elapsed time; appears at every session start with open threads; absent on first-time user (no ledger exists). States: single thread, multiple threads, empty (first time).

UX-DR2: Implement Progress Indicator component — always exactly 3 lines using ✓/→/◦ symbol vocabulary; completed steps collapse to single ✓ line with value summary; current step stands alone with one-phrase description; upcoming steps collapse to single ◦ line. Appears at workflow entry and every phase transition.

UX-DR3: Implement Hook Announcement component — pass: one-line `[hook-name] ✓ checked [what] — [result]`; fail: hook name + specific issue + file:line + likely cause. Never silent, never verbose. Every hook, every fire.

UX-DR4: Implement Workflow Step component — orientation line (never "step N/M"), substantive content, transition signal, explicit user control [A/P/C or equivalent]. Most frequent pattern in the system.

UX-DR5: Implement Completion Signal component — explicit ownership return ("this is yours to review and adjust"), what was produced (file list), what's next question. Every story cycle and workflow completion must use this.

UX-DR6: Implement Subagent Return component — Tony's voice synthesizes subagent findings; severity indicators (! critical, · minor); critical findings surface flywheel trigger. User never sees raw subagent output.

UX-DR7: Implement Flywheel Notice component — surfaced after upstream fix applied; shows finding, root cause, fix applied, what it prevents. Makes invisible improvement visible.

UX-DR8: Implement Proactive Orientation component — surfaces knowledge gap or about-to-be-skipped step detection; offers, never blocks; decision always returned to user. Fires only when conversational floor is open.

UX-DR9: Implement consistent Symbol Vocabulary across all agents and hooks: ✓ completed/passing, → current/active, ◦ upcoming/pending, ! warning/attention, ✗ failed/blocked, ? question/decision. Symbols always paired with text — meaning must survive any rendering context.

UX-DR10: Implement Hub-and-Spoke Voice Contract — Impetus (Tony) is the sole user-facing voice; all subagents return structured JSON `{status, result, question, confidence}`; subagent identity never surfaces to user; Tony synthesizes before presenting.

UX-DR11: Implement Session Orientation Contract — at every session start, Impetus reads ledger and within two exchanges surfaces: active story/task, current phase, last completed action, suggested next action. Agent speaks first; user never hunts for context.

UX-DR12: Implement Productive Waiting pattern — while a background subagent runs, Impetus maintains dialogue on the same topic (never context-switches). Dead air is a failure mode. Brief acknowledged pauses acceptable for very short tasks only.

UX-DR13: Implement Multi-Thread Ledger Awareness — each Tony instance (per Claude Code tab) reads/writes the shared ledger; recently-timestamped entries signal intentional concurrent work; conflicting thread starts flagged with user decision required.

UX-DR14: Implement Thread Hygiene — surface dormant threads beyond a threshold; low-friction closure (one confirmation); contextually triggered when dependent work completes or ledger grows unwieldy.

UX-DR15: Implement Response Architecture Pattern — every agent response follows: orientation line → substantive content → transition signal → user control. Orientation line is narrative (never "step N/M"); user control always last and always visible.

UX-DR16: Implement Input Interpretation patterns — number selects ledger item; letter command is case-insensitive; fuzzy match (continue/yes/go ahead = C); natural language extracts intent and confirms; ambiguous input triggers one clarifying question (never two).

UX-DR17: Implement Workflow Resumability — every workflow must be resumable from any step; sufficient context saved in ledger entry to re-orient a fresh agent session without user re-explanation. Step re-entry after interruption always confirms ("continue from here, or restart this step?").

UX-DR18: Impetus agent persona voice — "guide's voice": oriented, substantive, forward-moving. Synthesizes before delivering. Returns agency explicitly at completion. Acknowledges uncertainty honestly. Never: generic praise ("Great!"), numeric progress ("Step 3/8"), visible agent machinery. Named Tony internally; surface name is Impetus/Momentum.

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
| FR20 | Epic 3 | Conditional quality gates before session end (Stop hook) |
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

**NFR mapping:** NFR1–3 (context/token budget) → Epic 1 & 2. NFR4 (context budget architecture decision, blocking) → Epic 1. NFR5–8 (portability/degradation) → Epic 1. NFR9–11 (ecosystem resilience) → Epic 1. NFR12–15 (integration compatibility) → Epic 1. NFR16–17 (dogfooding integrity) → cross-cutting, applied across all epics.

## Epic List

### Epic 1: Foundation & Bootstrap
A developer installs Momentum from scratch — global practice files in place, project bootstrapped, all structure scaffolded by the module. Epic 2 onwards can start.
**FRs covered:** FR1, FR2, FR2b, FR2c, FR3a, FR3b, FR3c, FR4, FR5
**NFRs covered:** NFR1–13 (portability, resilience, compatibility, token budget architecture decision)
**Additional:** Repo structure, plugin/skills/rules layout, version.md, `momentum setup` global rules copy, cost observability (showTurnDuration, ccusage recommendation)
**Priority:** Day 1

---

### Epic 2: Stay Oriented with Impetus
A developer always knows where they are and what to do next. Session ledger tracks open threads across tabs and sessions. Visual progress answers "what have we built, what are we doing, what's next" at every transition. Tony's unified voice keeps backstage invisible.
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
**Additional:** code-reviewer agent (plugin, read-only), VFL flat skill (momentum-vfl), create-story skill, dev-story skill, ATDD workflow, plugin-agent invocation spike
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
**Then** each Momentum skill description is ≤100 tokens
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
**And** `showTurnDuration: true` is set in `.claude/settings.json`
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
