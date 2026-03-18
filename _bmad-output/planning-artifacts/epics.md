---
stepsCompleted:
  - step-01-validate-prerequisites
inputDocuments:
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/ux-design-specification.md
---

# Momentum - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Momentum, decomposing the requirements from the PRD, UX Design, and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

**Installation & Deployment**
FR1: Developer can install Momentum skills via `npx skills add` into any Agent Skills-adopting IDE
FR2: Developer can install the full Momentum plugin (skills + hooks + agents + rules) into Claude Code
FR3: Developer can re-run installation after updates and receive propagated changes
FR4: Team member can receive project-level Momentum configuration via `git clone` without manual setup
FR5: Orchestrating agent can detect missing global Momentum components and guide one-time installation

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
NFR1: Each Momentum skill description must be ≤100 tokens to minimize startup context budget impact
NFR2: Skill matching accuracy must remain ≥95% when Momentum skills coexist with 68+ BMAD skills
NFR3: Skill instructions should stay under 500 lines / 5000 tokens per Agent Skills spec recommendation
NFR4: Architecture must determine whether plugin-namespaced skills count against the flat skill context budget (blocking architecture decision)

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

{{requirements_coverage_map}}

## Epic List

{{epics_list}}
