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
lastEdited: '2026-04-11'
editHistory:
  - date: '2026-04-11'
    changes: 'Removed /momentum:create-epic and /momentum:develop-epic — superseded by momentum:create-story + momentum:epic-grooming + sprint model (developer decision 2026-04-11): replaced FR50 and FR51 rows in FR Coverage Map with removal notices; rewrote FR52 row to reflect current lifecycle (triage → sprint-planning → sprint-dev → retro → triage); renamed Epic 2b from "Impetus as Epic Orchestrator" to "Impetus as Sprint Orchestrator" in both the Epic List and the full epic body; rewrote Epic 2b description to replace create-epic/develop-epic workflow with create-story + epic-grooming + sprint model; updated Epic 2b FRs covered to remove FR50 and FR51; updated Epic 2a Additional field to remove /create and /develop references and reflect sprint-aware narrative greeting.'
  - date: '2026-04-01'
    changes: 'Added Epic 0 (Redesign Foundation — 3 stories): story-id-migration, sprint-status-schema-redesign, momentum-sprint-manager-skill. Added Epic 0 to epic list. These are the foundation for the full Momentum orchestration redesign.'
  - date: '2026-03-26'
    changes: 'Added Epic 2a (Impetus UX Redesign — 4 stories) and Epic 2b (Impetus as Epic Orchestrator — 6 stories) with high priority before Epic 3. Added FR49–FR54 to FR Coverage Map. Inserted epic list entries and full epic body sections. Epic 2a covers silent pre-flight, progress bar, menu redesign, hash-drift plain language. Epic 2b covers triage skill, /create-epic, momentum-dev-auto, /develop-epic (tier-sequential DAG), retro handoff, epic close-out model.'
  - date: '2026-03-23'
    changes: 'AVFL Epic 3 validation: Dropped Story 3.4 (duplicates Stories 1.3/1.5, NFR8 unverifiable at Epic 3). Reassigned NFR8 compliance audit to Story 7.3, CMUX anti-patterns to Story 7.1. Added session state contract between Stories 3.1/3.3 (session-modified-files.txt). Fixed Story 3.2 path scope ambiguity and installed.json schema gap. Fixed Story 3.3 missing no-lint-tool AC. Fixed Story 3.5 effort vocabulary and orchestration omission. Updated Epic 3 FR/NFR coverage.'
  - date: '2026-03-23'
    changes: 'AVFL integration: renamed momentum-vfl to momentum-avfl throughout; renamed vfl-validator protocol type to avfl-validator; added FR48 for AVFL skill to Requirements Inventory and FR Coverage Map; added Story 4.6 (AVFL Skill Orchestrates Multi-Lens Validation) to Epic 4; updated Story 4.3 ACs with AVFL phase in story cycle (Code Review → AVFL → Flywheel); updated Epic 4 description and Additional fields.'
  - date: '2026-03-22'
    changes: 'Retro Action Item #4 resolution: FR39 (Gherkin format convention) split between Story 1.7 (process/convention) and Story 4.2 (automated enforcement). Story 4.2 first AC block (FR39 format requirements) removed — now covered by Story 1.7. Story 4.2 narrowed to FR40 only, depends_on updated. FR Coverage Map updated to show FR39 split across Epic 1b and Epic 4.'
  - date: '2026-03-22'
    changes: 'Added Epic 1b — Foundation Fixes (Stories 1.6–1.9) between Epic 1 and Epic 2. Retro-driven mini-epic addressing action items #1, #2, #3, #5, #7 and team agreements 1–3 from the Epic 1 retrospective. Must complete before Epic 2 development begins.'
  - date: '2026-03-22'
    changes: 'Added terminal-multiplexer protocol type to Story 7.1 recognized types; added AC for terminal-multiplexer protocol contract with detect-and-adapt pattern; forward-referenced CMUX anti-patterns for Story 3.4. Derives from CMUX research document.'
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
FR48: AVFL skill deployed as flat skill at `momentum-avfl/` supporting gate/checkpoint/full profiles; spawns parallel reviewers across structural integrity, factual accuracy, coherence & craft, and domain fitness lenses; cross-checks findings between independently-framed reviewers; returns consolidated scored findings with evidence

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
- Session journal stored at `.claude/momentum/journal.jsonl`; auto-generated `.claude/momentum/journal-view.md` for human readability
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

**From Architecture — AVFL Skill**
- AVFL deployed as flat skill (`momentum-avfl/SKILL.md`) alongside Impetus
- AVFL orchestrates parallel reviewer spawning from main context (confirmed pattern per Claude Code docs)
- Reviewers are context:fork agents; return structured JSON (not free-form prose) per vfl-framework-v3.json output schema
- AVFL consolidates findings in main context; context accumulation bounded by structured output contract
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

UX-DR19: Implement Attention-Aware Checkpoints — every workflow checkpoint that pauses for human review leads with a micro-summary of what was generated and key decisions made; offers tiered review depth (quick scan / full review / trust & continue); never dumps a full artifact unprompted. Grounded in spec fatigue research: vigilance decrement onset at 10–15 minutes; reviewers who scan a summary and drill into one section exercise more scrutiny than those who scroll past a wall of text.

UX-DR20: Implement Expertise-Adaptive Orientation — agents and workflows adapt guidance depth to demonstrated competence: first encounter = full walkthrough with context; subsequent encounters = abbreviated decision points; expert mode = minimal cue. Grounded in expertise reversal effect (Kalyuga et al., 2003): instructional techniques effective for novices become actively harmful for experts. Even crude detection is effective ("Full walkthrough or just the decision points?" at workflow start).

UX-DR21: Implement Motivated Disclosure — every drill-down, detail expansion, or "see more" must be framed with *why it matters* to the current task, not just what it contains. Transforms review from passive chore into motivated retrieval. Grounded in coherence cascade principle (Thomas, 2026): progressive disclosure only works when each layer explains why the hidden information is valuable.

UX-DR22: Implement Confidence-Directed Review — when generating or presenting specifications, flag sections by confidence level (high = derived from upstream spec, medium = inferred from patterns, low = needs developer input) to direct review attention where it matters most. Aligns with provenance infrastructure (`derives_from` chain strength as confidence proxy). Grounded in IJHCS 2025: medium verbalized uncertainty produces highest trust, satisfaction, and task performance.

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
| FR39 | Epic 1b (convention, Story 1.7) + Epic 4 (automated enforcement, Story 4.2) | Gherkin acceptance criteria — behavioral, technology-agnostic |
| FR40 | Epic 4 | ATDD workflow generates failing acceptance tests from Gherkin |
| FR41 | Epic 4 | Full story cycle guided by orchestrating agent |
| FR42 | Epic 4 | Visual progress through story cycle (current phase + next phase) |
| FR43 | Epic 4 | Upstream fix skill analyzes quality failure and proposes correction |
| FR44 | Epic 8 | Multi-model research via MCP-integrated providers |
| FR45 | Epic 8 | Enforce date-anchoring and primary-source directives in research prompts |
| FR46 | Epic 8 | Archive outdated documents while preserving reference chain |
| FR47 | Epic 8 | Track document freshness using domain-specific freshness windows |
| FR48 | Epic 4 | AVFL skill deployed with multi-lens validation pipeline |
| FR49 | Epic 2b | triage workflow — raw input → epics.md mutations; only unlocked epics mutable |
| FR50 | — | Removed — /momentum:create-epic superseded by momentum:create-story + momentum:epic-grooming + sprint model |
| FR51 | — | Removed — /momentum:develop-epic superseded by momentum:sprint-dev |
| FR52 | Epic 2b | Epic lifecycle: triage → sprint-planning → sprint-dev → retro → triage |
| FR53 | Epic 2b | momentum-dev-auto — background-safe story implementation: no ask gates, merge deferred, AVFL GATE_FAILED = clean structured fail |
| FR54 | Epic 2a | Session-open epic progress bar: read sprint-status.yaml, render done/current/next bar, 2-item primary menu |

**NFR mapping:** NFR1–3 (context/token budget) → Epic 1 & 2. NFR4 (flat skills deployment — no plugin namespacing required) → Epic 1. NFR5–8 (portability/degradation) → Epic 1. NFR9–11 (ecosystem resilience) → Epic 1. NFR12–15 (integration compatibility) → Epic 1. NFR16–17 (dogfooding integrity) → cross-cutting, applied across all epics.

## Epic List

### Epic 1: Foundation & Bootstrap
A developer installs Momentum from scratch — global practice files in place, project bootstrapped, all structure scaffolded by the module. Epic 2 onwards can start.
**FRs covered:** FR1, FR2, FR2b, FR2c, FR3a, FR3b, FR3c, FR4, FR5
**NFRs covered:** NFR1–15 (NFR14–15 co-covered with Epic 7) (portability, resilience, compatibility, token budget architecture decision)
**Additional:** Repo structure, skills/rules layout, version.md, cost observability (showTurnDuration, ccusage recommendation)
**Priority:** Day 1

---

### Epic 1b: Foundation Fixes
Retro-driven fix epic. The Epic 1 retrospective surfaced gaps in the install experience, acceptance testing process, orchestrator purity, and storage format. These must be resolved before Epic 2 development begins — they affect architecture decisions, story structure, and process constraints that Epic 2 stories depend on.
**Retro source:** `_bmad-output/implementation-artifacts/epic-1-retro-2026-03-22.md` — Action Items #1, #2, #3, #5, #7; Team Agreements 1, 2, 3
**Touches:** epics.md, architecture.md, acceptance-testing-standard.md (new), Epic 2 story files, README
**Priority:** Day 1 (must complete before Epic 2 development)

---

### Epic 2: Stay Oriented with Impetus
A developer always knows where they are and what to do next. Session journal tracks open threads across tabs and sessions. Visual progress answers "what have we built, what are we doing, what's next" at every transition. Impetus's unified voice keeps backstage invisible.
**FRs covered:** FR6, FR7, FR8, FR9, FR10, FR11
**NFRs covered:** NFR1, NFR2, NFR3
**UX-DRs covered:** UX-DR1, UX-DR2, UX-DR4, UX-DR5, UX-DR6 (partial), UX-DR8 (partial), UX-DR9, UX-DR10, UX-DR11, UX-DR12, UX-DR13, UX-DR14, UX-DR15, UX-DR16, UX-DR17, UX-DR18
**Priority:** Day 1

---

### Epic 0: Redesign Foundation
Migrate sprint-status.yaml to the new 3-section schema (stories/epics/sprints), rename all story keys from `N-N-slug` to plain kebab-case slugs, and introduce momentum-sprint-manager as the sole writer of sprint-status.yaml. Everything in the Momentum redesign depends on this.
**FRs covered:** FR55
**Priority:** Immediate (blocks all redesign work)

---

### Epic 2a: Impetus UX Redesign
The session-open experience communicates what Impetus is and shows real project state. Startup is silent on happy path. Menu is minimal and outcome-focused. Sprint-aware narrative greeting replaces the static menu as the primary orientation surface.
**FRs covered:** FR54
**UX-DRs covered:** UX-DR1, UX-DR2, UX-DR6 (extended)
**Additional:** Sprint-aware narrative greeting with 9 greeting states; adaptive 3-4 item menus; silent pre-flight voice rules; hash-drift plain language.
**Priority:** High (before Epic 3)

---

### Epic 2b: Impetus as Sprint Orchestrator
Impetus orchestrates work at the sprint level. The developer uses triage to plan, momentum:create-story to add individual stories, momentum:epic-grooming to manage epic taxonomy, and sprint-planning + sprint-dev to execute. The sprint is the primary unit of execution; the epic is the primary unit for grouping and scoping work.
**FRs covered:** FR49, FR52, FR53
**Note:** FR50 (/momentum:create-epic) and FR51 (/momentum:develop-epic) removed — superseded by this model (developer decision 2026-04-11).
**Additional:** triage skill (epics.md mutations), momentum:epic-grooming (taxonomy management), retro handoff (triage-inbox.md), sprint close-out (done-incomplete/closed-incomplete statuses).
**Priority:** High (before Epic 3)

---

### Epic 3: Automatic Quality Enforcement
Quality gates fire without developer intervention. Lint and format run on save. Acceptance tests are protected from modification. Model routing is configured by frontmatter so every skill and agent uses the right model by default.
**FRs covered:** FR18, FR19, FR20, FR21, FR23 (FR22 delivered by Story 1.3)
**NFRs covered:** NFR7 (NFR8 verified in Story 7.3)
**UX-DRs covered:** UX-DR3
**Additional:** Model routing strategy (PT-016): model-routing-guide.md, model/effort frontmatter on all skills/agents, model-routing.md rule. Story 3.4 dropped — see Epic 3 body.
**Priority:** Sprint 1 (deferred; Epic 2a and 2b take priority)

---

### Epic 4: Complete Story Cycles
A developer completes a full story cycle guided by Impetus — spec → ATDD → implement → code review → AVFL validation — with every handoff driven by the agent. The developer never needs to know the next command; the agent tells them.
**FRs covered:** FR24, FR25, FR26, FR27, FR39 (automated enforcement — convention in Epic 1b), FR40, FR41, FR42, FR43, FR48
**UX-DRs covered:** UX-DR6, UX-DR8, UX-DR19 (Story 4.1), UX-DR20 (Story 4.3), UX-DR22 (Story 4.1)
**Additional:** code-reviewer (`context:fork` skill, `allowed-tools: Read`), AVFL flat skill (momentum-avfl, Story 4.6), create-story skill, dev-story skill (includes ATDD workflow capability — ATDD is not a separate deployed skill)
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
**UX-DRs covered:** UX-DR7, UX-DR19 (Story 6.3), UX-DR22 (Story 6.3)
**Additional:** findings-ledger.jsonl (global, with full schema), upstream-fix skill (momentum-upstream-fix), flywheel workflow, Momentum findings MCP server (optional query layer)
**Priority:** Sprint 2

---

### Epic 7: Bring Your Own Tools
A developer configures which agent, model, test framework, terminal multiplexer, or MCP provider satisfies each protocol. Swapping any component doesn't touch workflow definitions. The practice layer is unchanged even when the tooling changes underneath it.
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

### Epic 10: Impetus Core Infrastructure
The engine room — Impetus orchestrator workflow modules, Python tooling scripts, agent observability, and cross-cutting improvements that enable the practice to run reliably and efficiently. Retro-driven and sprint-driven improvements that don't belong to a specific capability epic land here.
**FRs covered:** FR6, FR7, FR8 (orchestrating agent capabilities — shared with Epic 2)
**NFRs covered:** NFR3 (token economics)
**Additional:** momentum-tools.py CLI, sprint workflow modules, quick-fix and retro skills, agent logging/observability, journal tooling, orchestrator guards
**Priority:** Ongoing (continuous improvement)

---

### Epic 11: Agent Team Model
Sprint-dev assembles the right execution team — agent roles, spawning modes (fan-out vs TeamCreate), communication patterns, deduplication guards, and quality gate coordination. Ensures the right agents are spawned with the right tools for each development and review phase.
**FRs covered:** FR84, FR85 (spawn registry, duplicate logging), FR88 (per-story code review), FR91 (E2E validator accuracy)
**Additional:** Agent role definitions, specialist vs generalist agent decisions, turn budgets, self-routing filters, collaboration pattern research
**Priority:** High (sprint execution quality depends on correct team composition)

---

## Epic 1: Foundation & Bootstrap

A developer installs Momentum from scratch — global practice files in place, project bootstrapped, all structure scaffolded through Impetus. Everything subsequent depends on this.


> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## Epic 1b: Foundation Fixes

The Epic 1 retrospective surfaced four categories of gap that must be closed before Epic 2 development begins: a broken install experience (90 skills shown instead of 8), no acceptance testing process or standards, no architectural enforcement of orchestrator purity, and a concurrency-unsafe storage format decision. This mini-epic resolves each gap as a proper story with acceptance criteria, ensuring Epic 2 stories start on solid ground.

**Retro source:** `_bmad-output/implementation-artifacts/epic-1-retro-2026-03-22.md`
**Action Items addressed:** #1 (install fix), #2 (acceptance test role separation), #3 (acceptance test standard by story type), #5 (JSONL migration evaluation), #7 (orchestrator purity principle)
**Team Agreements addressed:** 1 (E2E deployment testing mandatory), 2 (acceptance testing role separation starts now), 3 (stories include Acceptance Test Plan section)
**Sequencing:** Story 1.7 has no dependencies and unblocks Story 1.6. Stories 1.8 and 1.9 are independent. All four must complete before Epic 2 stories begin.


> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## Epic 2: Stay Oriented with Impetus

A developer always knows where they are and what to do next. Session journal tracks open threads across tabs and sessions. Visual progress answers "what have we built, what are we doing, what's next" at every transition. Impetus's unified voice keeps backstage invisible.

**FRs covered:** FR6, FR7, FR8, FR9, FR10, FR11
**NFRs covered:** NFR1, NFR2, NFR3
**UX-DRs covered:** UX-DR1, UX-DR2, UX-DR4, UX-DR5, UX-DR6, UX-DR8 (partial — proactive-offer pattern introduced; fully exercised in Epic 4), UX-DR9, UX-DR10, UX-DR11, UX-DR12, UX-DR13, UX-DR14, UX-DR15, UX-DR16, UX-DR17, UX-DR18, UX-DR19 (Story 2.4), UX-DR20 (Story 2.5), UX-DR21 (Story 2.5), UX-DR22 (Story 2.4)
**Note:** UX-DR3 (Hook Announcement) → Epic 3. UX-DR7 (Flywheel Notice) → Epic 6. UX-DR8 (Proactive Orientation) — the proactive-offer-never-block pattern is established here in Stories 2.2/2.5 and fully exercised once story cycles (Epic 4) provide real workflow steps. UX-DR19–22 (Spec Fatigue Mitigation) — introduced in Stories 2.4/2.5 and fully exercised once code review (Epic 4) and flywheel (Epic 6) provide real review content.


> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## Epic 0: Redesign Foundation

The Momentum orchestration redesign requires a new sprint-status.yaml schema, a new story ID format, and a dedicated sprint-manager subagent. This epic provides the foundation that all other redesign work depends on. It migrates existing data to the new format while preserving all current tracking information.

**FRs covered:** FR55 (sprint-manager exclusive write authority)
**Sequencing:** All three stories must complete before any other redesign stories begin. `story-id-migration` is independent. `sprint-status-schema-redesign` depends on `story-id-migration`. `momentum-sprint-manager-skill` depends on `sprint-status-schema-redesign`.


> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## Epic 2a: Impetus UX Redesign

The session-open experience communicates what Impetus is and shows real project state. Startup is silent on happy path. Menu is minimal and outcome-focused.

**FRs covered:** FR54
**UX-DRs covered:** UX-DR1, UX-DR2, UX-DR6 (extended)


> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## Epic 2b: Impetus as Sprint Orchestrator

Impetus orchestrates work at the sprint level. The developer uses triage to plan, momentum:create-story to add individual stories, momentum:epic-grooming to manage epic taxonomy, and sprint-planning + sprint-dev to execute. The sprint is the primary unit of execution; the epic is the primary unit for grouping and scoping work.

**FRs covered:** FR49, FR52, FR53
**Note:** FR50 (/momentum:create-epic) and FR51 (/momentum:develop-epic) removed — superseded by this model (developer decision 2026-04-11).


> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## Epic 3: Automatic Quality Enforcement

Quality gates fire without developer intervention. Lint and format run on save. Acceptance tests are protected from modification. Model routing is configured by frontmatter so every skill and agent uses the right model by default.

**FRs covered:** FR18, FR19, FR20, FR21, FR23
**NFRs covered:** NFR7
**UX-DRs covered:** UX-DR3
**Note:** FR22 (rules auto-load) delivered by Story 1.3 (native Claude Code behavior). NFR8 (protocol portability) verified in Story 7.3 where the protocol registry exists.


> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## Epic 4: Complete Story Cycles

A developer completes a full story cycle guided by Impetus — spec → ATDD → implement → code review → AVFL validation — with every handoff driven by the agent. The developer never needs to know the next command; the agent tells them.

**FRs covered:** FR24, FR25, FR26, FR27, FR39 (automated enforcement — convention in Epic 1b Story 1.7), FR40, FR41, FR42, FR43, FR48
**UX-DRs covered:** UX-DR6, UX-DR8, UX-DR19 (Story 4.1), UX-DR20 (Story 4.3), UX-DR22 (Story 4.1)


> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## Epic 5: Trust Artifact Provenance

A developer can trace every artifact to its origins, detect stale references, and know the confidence level of every significant claim. The provenance graph is maintained in frontmatter — no external tooling required.

**FRs covered:** FR12, FR13, FR14, FR15, FR16, FR17
**UX-DRs covered:** UX-DR5 (scanner completion signal at session orientation)
**Additional:** derives_from frontmatter format, content hash staleness (git hash-object), referenced_by auto-generation, provenance scanner (in Impetus references/)


> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## Epic 6: The Practice Compounds

Findings accumulate across stories. Systemic patterns surface. Upstream fixes are applied at the right level — spec, rule, workflow, or one-off patch. Each sprint the practice gets measurably smarter. The flywheel makes invisible improvement visible.

**FRs covered:** FR28, FR29, FR30, FR31, FR32, FR33
**UX-DRs covered:** UX-DR7, UX-DR19 (Story 6.3), UX-DR22 (Story 6.3)
**Additional:** findings-ledger.jsonl (global, with full schema), upstream-fix skill (momentum-upstream-fix), flywheel workflow, Momentum findings MCP server (optional query layer)


> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## Epic 7: Bring Your Own Tools

A developer configures which agent, model, test framework, or MCP provider satisfies each protocol. Swapping any component doesn't touch workflow definitions. The practice layer is unchanged even when the tooling changes underneath it.

**FRs covered:** FR34, FR35, FR36, FR37, FR38
**NFRs covered:** NFR14, NFR15


> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## Epic 8: Research & Knowledge Management

A developer runs multi-model research with freshness guarantees. Research prompts are date-anchored. Documents have domain-specific freshness windows. Outdated docs are archived with their reference chain intact.

**FRs covered:** FR44, FR45, FR46, FR47
**Additional:** Gemini MCP + GPT MCP integration (growth), hybrid research workflow (PT-020), freshness windows per domain
**Priority:** Growth
**UX-DRs covered:** UX-DR5 (research findings surfaced in Impetus's voice), UX-DR8 (warnings are advisory — do not block flow), UX-DR15 (response follows orientation → substantive content → transition signal → user control)


> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## Epic 9: Performance Validation

A developer benchmarks BMAD skills and sub-agents across model tiers to validate that the default model/effort routing decisions (FR23) are grounded in measured performance, not assumption. Benchmarking results feed back into skill frontmatter updates.

**FRs covered:** FR23
**Scope:** PT-022 — promptfoo config, bash benchmarking script, golden dataset starter, Pydantic AI harness with `agent.override()`, updated `model:`/`effort:` frontmatter based on results
**Priority:** Growth (requires Epics 2–4 to have real skills to benchmark)
**UX-DRs covered:** UX-DR8 (benchmark warnings advisory), UX-DR16 (benchmark results surfaced in Impetus's voice before developer acts on them)


> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## Epic 10: Impetus Core Infrastructure

The engine room — continuous improvement of the Impetus orchestrator itself: workflow modules, Python CLI scripts, agent observability, sprint execution improvements, and cross-cutting quality work that enables the practice but doesn't belong to a specific capability epic.

**Category:** Core orchestration and tooling

**Strategic intent:** Momentum's orchestrator accumulates improvements from every sprint retrospective and quality audit. These improvements — deduplication guards, task tracking enforcement, synthesis-first patterns, observability hooks — are too heterogeneous for any single capability epic but collectively determine whether the practice runs reliably. This epic is their home.

**Boundaries:** Includes Impetus workflow changes, momentum-tools.py script additions, agent observability/logging, sprint workflow modules (planning, dev, retro, quick-fix), journal/DuckDB tooling, and orchestrator behavioral guards. Excludes capability-specific work (provenance → Epic 5, research → Epic 8, protocol integration → Epic 7) and agent team composition decisions (→ Epic 11).

**FRs covered:** FR6, FR7, FR8 (shared with Epic 2)

**NFRs covered:** NFR3

**Current state:** 23 done, 13 remaining

> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## Epic 11: Agent Team Model

Sprint-dev assembles the right execution team for each development and review phase — agent roles, spawning modes, communication patterns, deduplication guards, and quality gate coordination.

**Category:** Sprint execution team composition

**Strategic intent:** The quality and efficiency of sprint execution depends on correct team composition. Duplicate agent spawns wasted 47.8% of compute in one sprint. Agent role confusion led to 6 of 10 user corrections in another. This epic formalizes the team model so sprint-dev consistently spawns the right agents with the right tools, and review teams coordinate without waste.

**Boundaries:** Includes agent role definitions (dev, dev-skills, dev-build, dev-frontend), spawning mode decisions (fan-out vs TeamCreate), deduplication guards, collaboration pattern research, turn budgets, and self-routing filters. Excludes individual skill implementations (→ Epic 10), quality gate definitions (→ Epic 3), and story cycle tooling (→ Epic 4).

**FRs covered:** FR84, FR85, FR88, FR91

**NFRs covered:** none

**Current state:** 4 done, 6 remaining

> Story details are tracked in `stories/index.json`. Epic membership is authoritative there.

---

## P{n} — Process Sprint-{n} (placeholder)

Each sprint has a corresponding process epic `P{n} — Process Sprint-{n}`. Process stories capture dev-environment and practice improvement work (skills, rules, hooks, tooling) that doesn't belong in product epics. Process story keys follow the format `p{sprint}-{n}-{title}` (e.g., `p1-1-momentum-plan-audit-skill`). Process stories are tracked in `sprint-status.yaml` (`development_status` + `momentum_metadata`) — this epic is a convention anchor, not a story registry.
