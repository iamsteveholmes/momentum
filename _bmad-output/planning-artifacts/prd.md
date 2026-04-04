---
stepsCompleted:
  - step-01-init
  - step-02-discovery
  - step-02b-vision
  - step-02c-executive-summary
  - step-03-success
  - step-04-journeys
  - step-05-domain
  - step-06-innovation
  - step-07-project-type
  - step-08-scoping
  - step-09-functional
  - step-10-nonfunctional
  - step-11-polish
  - step-e-01-discovery
  - step-e-02-review
  - step-e-03-edit
lastEdited: '2026-04-03'
editHistory:
  - date: '2026-04-03'
    changes: 'Plugin model conversion: Momentum becomes a Claude Code plugin with plugin.json manifest and momentum: namespace. Rewrote FR1 (plugin install replaces npx skills add), FR2/FR2b/FR2c (plugin install trigger), FR3a/FR3b/FR3c (plugin update mechanism), FR4 (team member plugin install), FR5 (plugin delivers skills, Impetus writes global rules), FR6 (namespaced menu invocations), FR37 (namespaced protocol resolution), FR48 (momentum:avfl plugin skill), FR50/FR51/FR53 (namespaced skill invocations). Added FR71 (plugin manifest) and FR72 (namespaced skill invocation). Removed NFR4 (no plugin namespacing — replaced with plugin namespace requirement). Rewrote NFR1 (rationale update), NFR2 (namespacing simplifies matching), NFR5 (plugin bundle replaces cross-tool parseability), NFR6 (removed — Claude Code native), NFR7 (single-tier full enforcement), NFR8 (protocol abstraction retained, cross-tool validation dropped), NFR9/NFR11 (packaging layer includes plugin.json), NFR12 (plugin namespacing eliminates conflicts). Updated Executive Summary, Journey 1, Journey 4, Journey Requirements Summary, Installation Architecture, Adoption Path, Implementation Considerations, Day 1 Success Criteria, Innovation section 4, Risk table, Epic 1 story 1.6 note.'
  - date: '2026-04-02'
    changes: 'Phase 3 sprint model integration: added FR56-FR70 (agent logging, Gherkin separation, sprint planning/execution/retro, two-layer agent model, dependency-driven concurrency, task tracking, sprint record schema, error handling, sprint slug convention); added Sprint Lifecycle and Sprint Planning & Execution sections; updated FR6 (sprint-level menu items), FR39 (plain English ACs, Gherkin separation), FR41 (dual orchestration models), FR48 (sprint-level AVFL scope), FR51 (dependency-driven concurrency replaces waves), FR53 (momentum-dev as pure executor subsumes momentum-dev-auto), FR54 (index.json replaces sprint-status.yaml), FR55 (momentum-tools CLI replaces subagent, index.json replaces sprint-status.yaml); updated Sprint Status Definitions data source references; updated review status definition (sprint AVFL replaces wave AVFL); added sprint capabilities to Journey Requirements Summary; added epic-sprint coexistence reconciliation.'
  - date: '2026-03-26'
    changes: 'Epic orchestrator model: added FR49 (triage workflow), FR50 (/create-epic command), FR51 (/develop-epic command), FR52 (epic lifecycle), FR53 (momentum-dev-auto), FR54 (session-open epic progress bar); updated FR6 (Impetus as pure orchestrator, epic-level dispatch), FR41 (epic as primary unit of work, stories created in bulk); added sprint-status.yaml status definitions section with done-incomplete and closed-incomplete; added Epic Orchestrator Model section clarifying epic-first workflow model.'
  - date: '2026-03-23'
    changes: 'AVFL integration: renamed momentum-avfl to momentum-avfl throughout; moved AVFL validation from Growth to First Sprint scope (gate/checkpoint profiles in story cycles); added FR48 for AVFL skill deployment; kept standalone /validate command as Growth; updated repo structure tree with framework.json and sub-skills.'
  - date: '2026-03-22'
    changes: 'Added terminal-multiplexer row to Protocol-Based Integration Architecture table; added terminal multiplexer integration note with detect-and-adapt pattern and anti-pattern forward reference for Story 3.4. Derives from CMUX research document.'
  - date: '2026-03-22'
    changes: 'Added mise as standard tool/runtime manager in Implementation Considerations — Momentum skills and workflows must prefer mise over legacy version managers (nvm, pyenv, rbenv, asdf, volta, fnm) when referencing tool installation.'
  - date: '2026-03-20'
    changes: 'Removed plugin deployment model; replaced with skills-only architecture (npx skills add momentum/momentum -a claude-code + Impetus interactive setup). Updated FR2, NFR4, NFR7, NFR9, NFR10, NFR11, Journey 1 narrative, deployment table, repository structure, installation architecture, implementation considerations.'
  - date: '2026-03-20'
    changes: 'Disambiguated FR2 (solo first-install) and FR5 (team member joining); added FR2b (current version → orientation) and FR2c (version mismatch → upgrade); decomposed FR3 into FR3a/FR3b/FR3c (upgrade mechanism); corrected NFR1 to ≤150 characters; removed duplicate token constraint from NFR4; updated NFR7 Tier 3 validation method; marked J1 ✓ for global install detection in Journey Requirements Summary; corrected all npx skills add momentum occurrences to full org/package -a adapter form throughout.'
  - date: '2026-03-20'
    changes: 'Fixed repo tree in Installation Architecture — context:fork skills now shown as peer directories (momentum-code-reviewer/, momentum-architecture-guard/), not nested under skills/momentum/; replaced package.json with version.md; added .claude/settings.json entry. Added -g global install row to deployment table. Added installed.json commit policy to Implementation Considerations. Removed stale README update item from Post-PRD Actions.'
  - date: '2026-03-20'
    changes: 'Validation fix pass: C-02 renamed current_version → momentum_version in FR2 (full field description) and configured_for_version → momentum_version in FR2b/FR2c/FR3b/FR3c; C-03 replaced Documentation & Repository Structure repo tree with correct peer layout (version.md, all context:fork skills as peer dirs, .claude/rules/, .claude/skills/, _bmad-output/); C-04 fixed NFR7 Tier 3 validation method (was a Tier 1 test; now: README documents all three tiers and principles are actionable without tooling); C-04 appended README documentation note to Tier 1 test; C-07 clarified FR20 (tests conditional on PostToolUse Write/Edit event tracking, not just "code was modified"); C-08 clarified FR37 (Impetus reads config, looks up protocol binding, invokes implementation); C-09 added deployment constraint note to NFR4; C-11 added abbreviated tree note to Installation Architecture; C-12 added FR9 qualification (protocol mapping table gaps, MCP provider, ATDD tool binding); C-13 added BMAD v6 parenthetical to 68 BMAD skills (risk table + implementation considerations); C-14 covered by C-04 (README Tier 1 note); C-15 added FR3a post-condition (installed SKILL.md files and bundled references replaced).'
classification:
  projectType: developer_tool
  domain: agentic-engineering
  complexity: medium
  projectContext: greenfield
inputDocuments:
  - _bmad-output/planning-artifacts/product-brief-momentum-2026-03-13.md
  - _bmad-output/planning-artifacts/research/technical-agent-skills-deployment-research-2026-03-15.md
  - docs/planning-artifacts/AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md
  - docs/research/handoff-product-brief-2026-03-14.md
  - docs/research/multi-model-benchmarking-handoff-2026-03-14.md
  - docs/research/preliminary-findings-momentum-as-skills-2026-03-13.md
  - docs/process/process-backlog.md
documentCounts:
  briefs: 1
  research: 4
  projectDocs: 1
  processBacklog: 1
workflowType: 'prd'
derives_from:
  - id: BRIEF-MOMENTUM-001
    path: _bmad-output/planning-artifacts/product-brief-momentum-2026-03-13.md
    relationship: derives_from
  - id: PLAN-SOLO-DEV-001
    path: docs/planning-artifacts/AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md
    relationship: derives_from
  - id: HANDOFF-BRIEF-001
    path: docs/research/handoff-product-brief-2026-03-14.md
    relationship: derives_from
  - id: RESEARCH-BENCHMARK-HANDOFF-001
    path: docs/research/multi-model-benchmarking-handoff-2026-03-14.md
    relationship: derives_from
  - id: RESEARCH-SKILLS-PRELIM-001
    path: docs/research/preliminary-findings-momentum-as-skills-2026-03-13.md
    relationship: derives_from
  - id: RESEARCH-SKILLS-DEPLOY-001
    path: _bmad-output/planning-artifacts/research/technical-agent-skills-deployment-research-2026-03-15.md
    relationship: derives_from
referenced_by: []
provenance:
  generated_by: pm-agent (John) + Steve
  model: claude-opus-4-6
  timestamp: 2026-03-16
---

# Product Requirements Document — Momentum

**Author:** Steve
**Date:** 2026-03-16

## Executive Summary

Momentum is a practice system for agentic engineering — the discipline of directing AI agents to produce production-quality software while maintaining human accountability for architecture, quality, and correctness.

Industry data is unambiguous: AI code generation without governance fails. 67.3% of AI-generated PRs are rejected (vs 15.6% for human code). AI-generated code produces 1.7x more issues per PR. Experienced developers are 19% slower with AI tools while believing they're 20% faster. Organizations see PR volume increase 98% but delivery metrics stay flat. The problem is not the tools. The problem is the absence of a verification architecture, a quality discipline, and a continuous improvement practice around them.

Momentum provides that missing layer through eight composable principles: spec-driven development, an authority hierarchy (specifications > tests > code — encoded into machine-readable `derives_from` chains enforced by tooling), producer-verifier separation, an evaluation flywheel that traces failures upstream via navigable `derives_from` chains, three tiers of enforcement (deterministic hooks, structured workflows, advisory rules), cost as a managed dimension (the cognitive hazard rule: for outputs without automated validation, use flagship models — invisible errors cost more than the price premium), provenance as infrastructure, and protocol-based integration (each major capability defines an interface so implementations can be substituted across teams, tools, and environments). The system is delivered as a Claude Code plugin — installable via the Claude Code plugin mechanism, with full enforcement (hooks, subagents, rules) configured by Impetus on first run.

The primary user is a solo developer using AI coding tools who has experienced the initial thrill of speed and hit the wall: code that looks right but isn't, patterns that drift without anyone noticing, and growing unease about accumulating debt they can't see. Momentum is designed for this person first, with team adaptation as a future consideration.

### What Makes This Special

**Upstream fix discipline.** Most quality approaches fix symptoms — the code, the test, the failing PR. Momentum traces every failure to the workflow, specification, or rule that produced it and fixes *that*. Each upstream fix prevents a class of errors permanently. The system gets smarter every sprint — not because the AI improves, but because the practice around it compounds.

**Provenance as infrastructure.** Every specification claim traces to a source. Every artifact tracks what it derives from and what depends on it. Ungrounded claims are marked, not assumed valid. When upstream documents change, downstream documents are flagged as suspect. This is not documentation hygiene — it is load-bearing infrastructure that enables the flywheel, prevents hallucination propagation, and stops obsolete decisions from resurfacing.

**Native Claude Code plugin with full enforcement.** Momentum is a Claude Code plugin — hooks that always fire, subagents with read-only tools, rules that auto-load every session, and namespaced skills that eliminate collision with other installed plugins. The plugin model makes explicit what was always true: Momentum depends on Claude Code's enforcement infrastructure (hooks, context:fork, Agent Teams) and is designed for that environment.

## Project Classification

- **Project Type:** Developer Tool (practice system delivered as a Claude Code plugin)
- **Domain:** Agentic Engineering
- **Complexity:** Medium — no regulatory compliance, but evolving ecosystem dependencies (BMAD, Claude Code plugin model), and the meta-nature of a practice that governs practices
- **Project Context:** Greenfield

## Success Criteria

### User Success

**First value signal: Provenance catches stale sources.** The system flags outdated or questionable sources in specification documents — something that currently happens daily without detection. Expected to deliver value immediately upon first use.

**Second value signal: The flywheel turns.** A quality failure traces upstream to a workflow, spec, or rule. The fix prevents a class of errors permanently. The developer sees the system learn.

**Sustained value: Specs improve, work accelerates.** As the developer works through stories, specifications get better instead of fragmenting. Time spent on specs decreases instead of steadily increasing. Code quality improves because the specs driving generation improve. The developer feels more engaged and more confident — not because AI got smarter, but because the practice around it compounded.

**The defining outcome:** The developer completes stories faster with fewer rework cycles, because the specifications driving generation improve with every sprint. The compounding is measurable: fewer upstream fixes needed, fewer critical findings per story, less time revising specs.

### Business Success

Momentum is not a commercial product. Success is measured in practitioner outcomes:

- **Personal productivity:** The solo developer ships higher-quality output with sustained or increased throughput, without accumulating the four debt types (verification, cognitive, pattern drift, technical)
- **Compounding improvement:** The amount of rework and spec revision *decreases* over time — a new experience compared to the typical trajectory where complexity compounds and quality degrades
- **Open-source viability:** An external adopter can install, configure, and get value without direct support from the creator. Future success criterion, not an MVP gate.

### Team Adoption Success (Growth-Phase)

These metrics apply when Momentum is used by team members beyond the solo developer. Not an MVP gate — included for traceability against Journey 4.

- **Onboarding completion:** New team member completes a full story cycle (spec → ATDD → implement → review) with agent guidance on their first day
- **Process adherence:** Team members follow the guided workflow without needing to read documentation front-to-back — the orchestrating agent delivers context just-in-time
- **Quality consistency:** Team member story output has <=2 critical findings from code review, comparable to the solo developer baseline
- **Team member sentiment:** Self-reported positive experience with the guided workflow (>=4/5 rating)

### Technical Success

- **Day 1: Deployable plugin installs and runs.** A prototype plugin — with hooks, rules, and at least one functional skill — deploys via Claude Code plugin install; Impetus handles global configuration interactively on first run. It doesn't need to be feature-complete. It needs to be *installable and usable*. If it can't be installed, nothing else can be verified.
- **Day 2+: Iterate on functionality in real use.** The developer uses Momentum with other active projects concurrently. Real work is the test harness. Every feature is validated by using it, not by synthetic testing.
- **Hooks fire correctly** — lint on edit, test protection on acceptance tests, quality gate on stop
- **Provenance tracking works** — artifacts reference sources, dependencies are visible, staleness gets flagged
- **Interfaces defined before implementations** — each integration point (validation, research, review) has a protocol specification even if only one implementation exists
- **Visual progress is always visible** — the user knows where they are in any workflow at all times

### Measurable Outcomes

| Metric | Target | Measurement Method | Signal |
|--------|--------|-------------------|--------|
| Upstream fixes per sprint | >=30% decrease sprint 1→3; approaches zero by sprint 5 | Count fixes classified as upstream in findings ledger | The system is learning |
| Code review Critical findings | <=1 critical finding per story by sprint 3 | Count from code-reviewer findings reports | Upstream fixes preventing recurrence |
| Time spent on spec revision | Decreases >=20% per story cycle from baseline | Track time from story start to spec-approved (self-reported) | Specs are compounding, not fragmenting |
| Developer confidence | >=4/5 self-reported rating after each sprint | 1-5 rating recorded at sprint retrospective | Practice is earning trust |
| Stale source detections | >=3 detections in first sprint; decreasing thereafter | Count from provenance staleness checker | Provenance infrastructure working |

**Failure signals:**
- Same class of error recurs across stories (flywheel not turning)
- CLAUDE.md and quality rules stop being updated (upstream fix discipline lapsed)
- Developer accepts AI output without understanding it (cognitive debt accumulating)
- Time spent on specs increases instead of decreasing (system adding friction, not reducing it)
- A component substitution breaks the workflow (protocol not properly defined)

## User Journeys

### Journey 1: Steve — First Install and First Sprint

**Opening Scene:** Steve has been using BMAD V6 with Claude Code for months. The initial creation of any project goes great — specs are sharp, code generation is fast, the first few stories feel like magic. But it gets worse every day after that. He constantly fights outdated docs — decisions made in the brief that were superseded by research, but nobody flagged the brief. Specs get updated in ways that don't match his expectations. Code does things he wasn't aware of because the AI followed a pattern from three stories ago that was never corrected. He can *see* the debt accumulating. It's not invisible — it's visible and exhausting, and the effort to keep everything aligned grows instead of shrinking.

**Rising Action:** Steve installs the Momentum plugin and then runs `/momentum:impetus`. Impetus greets him, explains what it needs to configure — global rules, enforcement hooks, MCP servers — and with his confirmation sets everything up. Impetus then shows a menu of available workflows and understands what practice artifacts already exist in his project. He picks a current side project as the first test bed. The hooks wire up immediately — auto-lint fires on his first edit, the acceptance test directory gets protected. The rules auto-load in every session.

He starts a story. The orchestrating agent shows him where he is in the process — a clear ASCII status graphic: **[Spec Review] → ATDD → Implement → Review → Flywheel**. He reviews the spec. When implementation completes, the agent prompts him: "Implementation complete. Ready to fire off the code-reviewer for adversarial review? While it runs, here's a summary of what was built..." The code-reviewer launches in a separate context. While it works, Steve reads a concise explanation of what the code does — not the code itself, but what it accomplishes, what architectural decisions it made, and how it maps to the acceptance criteria. He'd half-forgotten the details of the third AC. The summary brings him back in. The status graphic updates: **Spec Review → ATDD → Implement → [Review] → Flywheel**.

**Climax:** Two days in, he's working on a PRD and the provenance system flags a `derives_from` reference where the upstream document has changed since the PRD was written. It's a decision about packaging — the brief still references `momentum install` even though research showed that's obsolete. The system caught it. Without provenance, this stale decision would have silently propagated into the architecture doc, into stories, into code. The first value signal lands exactly as predicted — and it's the kind of thing that has cost him hours of rework before.

**Resolution:** By the end of the first sprint, Steve has completed a full story cycle with the practice: spec → Gherkin ATDD → implement → code review → flywheel. At every step he knew where he was, what the agent was doing, and what came next. The code review surfaces a finding. The flywheel explains the issue and suggests tracing upstream. He agrees. The system learned — and so did he.

**Requirements revealed:** Plugin installation, Impetus-guided interactive setup, orchestrating agent with menu, hook infrastructure, provenance/staleness detection, code-reviewer subagent (prompted/automatic, not manual), visual status graphics showing current phase and next phase, human-readable implementation summaries during review, `derives_from` frontmatter, upstream fix workflow.

---

### Journey 2: Steve — The Flywheel Catches Something

**Opening Scene:** Steve is three sprints in. Momentum is part of his daily workflow. He's working on a complex feature across multiple stories. The specs are getting better — he spends less time revising acceptance criteria because the Create Story workflow now loads all the right context automatically (a flywheel fix from sprint 1).

**Rising Action:** The code-reviewer flags a pattern: the AI agent is using direct database queries in the service layer instead of going through the repository abstraction. This is the third time across three different stories. Each time it looked like a one-off — different service, different query, different story. But the findings ledger shows the pattern.

**Climax:** The flywheel explains the issue to Steve: "This is the third occurrence of direct database access bypassing the repository pattern. The findings ledger shows occurrences in stories S-04, S-07, and S-11. This looks systemic. I'd suggest we do a round of **upstream trace** to determine how far up the hierarchy this goes. Want to proceed?"

Steve agrees. The status graphic updates to show the flywheel workflow: **[Detection] → Review → Upstream Trace → Solution → Verify → Log**. The agent walks through each level: Is it a code-level fix? No — three occurrences rules that out. Is it a CLAUDE.md/rules gap? Yes — the architecture doc specifies repository pattern, but `.claude/rules/` doesn't mention it. In ad-hoc sessions and subagent contexts, the AI defaults to direct queries because its training data suggests that's fine. The graphic advances: **Detection → Review → [Upstream Trace] → Solution → Verify → Log**.

The fix: add a rule to `.claude/rules/architecture.md` specifying repository pattern as mandatory for data access. One rule, added once, prevents an entire class of errors permanently. The graphic completes: **Detection → Review → Upstream Trace → [Solution] → Verify → Log**. Steve sees the rule, approves it, and the agent confirms it's active.

**Resolution:** The next two stories have zero data access violations. The time Steve would have spent catching and fixing these in code review is now zero. More importantly, he was *part of every step*. He wasn't wondering what the agent was doing — he saw the detection, understood the trace, approved the fix. The flywheel turned, and he turned it together with the system.

**Requirements revealed:** Findings ledger with cross-story pattern detection, flywheel workflow with visual status (detection → review → upstream trace → solution → verify → log), agent explains issues and suggests next steps (never proceeds without Steve), `.claude/rules/` as always-loaded enforcement, flywheel integration with retrospective, measurable improvement across sprints.

---

### Journey 3: Steve — Something Doesn't Fit

**Opening Scene:** Steve installs Momentum on a new project — a Kotlin/JVM backend, different from the TypeScript projects he's been using it with. The hooks fire, the rules load, but the ATDD workflow assumes Playwright/Cypress and the test commands are wrong.

**Rising Action:** The Stop hook quality gate tries to run `npm test` — which doesn't exist. It blocks his session. The ATDD workflow generates test scaffolding for a web frontend that doesn't exist. The validation protocol calls Momentum's default validator, which uses lenses optimized for web fullstack.

**Climax:** Steve doesn't have to throw Momentum away. The protocol-based integration means each of these is a substitution, not a rewrite. He configures the test command in his project CLAUDE.md. He swaps the ATDD implementation to use Kotest (satisfying the same Gherkin → failing test interface). He points the validation protocol at a simplified validator that understands JVM conventions. The orchestrating agent still works — the menu, the workflow guidance, the flywheel — because the practice layer is independent of the implementation layer.

**Resolution:** Within an hour, Momentum is functional on the Kotlin project. Not every feature works perfectly — the code-reviewer's anti-pattern catalog is still web-heavy — but the core practice (spec authority, provenance, upstream fix discipline) operates identically. Over the next sprint, Steve adds Kotlin-specific rules to `.claude/rules/` via the flywheel. The system adapts to the new stack because it was designed to.

**Requirements revealed:** Protocol-based integration points, configurable test commands, stack-agnostic ATDD interface, swappable validation implementation, project-level configuration that overrides defaults, graceful degradation when a component doesn't fit.

---

### Journey 4: Future Team Member — Momentum Is Just There

**Opening Scene:** A developer on Steve's work team clones a project repo. They've never heard of Momentum. They're new to AI coding tools and currently follow a loose "read the docs, ask the senior dev" workflow.

**Rising Action:** They open Claude Code. The project-level hooks and rules activate automatically (configured in `.claude/settings.json` committed to the repo). But the orchestrating agent detects that the global Momentum components aren't installed on this developer's machine. It prompts: "This project uses Momentum for quality governance. The Momentum plugin needs to be installed and some global components need a one-time setup. Would you like me to guide you through that?" The developer says yes. They install the Momentum plugin, then Impetus writes the global rules and practice infrastructure to `~/.claude/`. Now everything works.

They start working on an assigned story. The orchestrating agent asks: "Would you like me to guide you through this story? I can help with spec review, test generation, implementation, and code review." They say yes.

**Climax:** The agent doesn't just walk them through steps — it actively reduces their cognitive debt. Instead of telling them to "read the PRD, architecture doc, epic, and story" (four documents they'd skim at best), the agent *contextualizes* as they go. During spec review: "This story implements the caching layer specified in the architecture doc. The key decision was to use write-through caching because the data access patterns favor consistency over speed — that was decided in ADR-003. The acceptance criteria require cache invalidation on every write." The developer understands *why* before they write a single line.

During implementation, they ask: "Why doesn't this use Redis? That's what I used at my last job." The agent doesn't treat this as an obstacle to bypass — it's an opportunity. "Good question. The architecture specifies an in-memory cache for the MVP because the dataset is small enough. Redis is in the Growth scope for when the dataset exceeds single-node memory. But if you think the dataset is already approaching that threshold, we should flag this for the architect." The developer's question might reveal a problem in the spec. The agent encourages that.

At each step, the developer sees the visual status. They understand where they are, what just happened, and what's next. When the code-reviewer runs, the agent shows them a summary of what was built while they wait. When a finding comes back, the agent explains it in the context of the project's specific architectural decisions.

**Resolution:** The developer completes the story. The code review comes back clean. They didn't need to read a single documentation page front-to-back — but they *understand* the project better than if they had, because the context was delivered exactly when it was relevant. They report to their team lead: "I completed a full story with AI and I actually understand what I built and why it's built that way."

More than that: during the process, they asked two questions that revealed an ambiguity in the acceptance criteria. The agent flagged it, the spec was clarified, and every future developer working on related stories benefits. The new developer didn't just consume the system — they made it better. Every moment of the process that they work through improves the system for everyone.

**Requirements revealed:** Global install detection and guided setup from project-level agent, zero-config onboarding after initial setup, orchestrating agent as conversational guide that contextualizes rather than lectures, cognitive debt reduction through just-in-time context delivery, developer questions treated as discovery opportunities not obstacles, visual status throughout, full workflow cycle accessible to newcomers, bidirectional value — the developer learns from the system AND the system learns from the developer.

---

### Journey Requirements Summary

| Capability | J1 | J2 | J3 | J4 |
|---|---|---|---|---|
| Skill installation (npx skills add momentum/momentum -a claude-code) | ✓ | | | |
| Global install detection + guided setup | ✓ | | | ✓ |
| Orchestrating agent with menu | ✓ | | | ✓ |
| Visual status graphics (phase + next) | ✓ | ✓ | | ✓ |
| Hook infrastructure | ✓ | | ✓ | ✓ |
| Provenance/staleness detection | ✓ | | | |
| Code-reviewer subagent (prompted/auto) | ✓ | ✓ | | ✓ |
| Human-readable implementation summaries | ✓ | | | ✓ |
| Findings ledger + pattern detection | | ✓ | | |
| Flywheel workflow with visual status | | ✓ | | |
| Upstream fix workflow | ✓ | ✓ | | |
| `.claude/rules/` enforcement | | ✓ | ✓ | ✓ |
| Protocol-based integration | | | ✓ | |
| Stack-agnostic ATDD interface | | | ✓ | |
| Configurable project overrides | | | ✓ | |
| Just-in-time context delivery | | | | ✓ |
| Developer questions as discovery | | | | ✓ |
| Bidirectional improvement | | | | ✓ |
| Agent logging / observability | ✓ | | | |
| Sprint planning workflow (selection, Gherkin, team) | ✓ | | | |
| Sprint execution workflow (dependency concurrency, AVFL) | ✓ | | | |
| Two-output retrospective (Momentum + project) | | ✓ | | |
| Black-box verification (Gherkin separation) | ✓ | | | |

## Innovation & Novel Patterns

### Detected Innovation Areas

**1. Upstream fix as a formal discipline.** Quality approaches fix outputs. Momentum traces failures through a specification chain to the workflow that produced the defect and fixes that. This isn't incremental improvement on code review — it's a different model of where quality comes from. The flywheel is the mechanism; the insight is that in agentic engineering, the *process artifacts* are the product, not the code.

**2. Provenance as load-bearing infrastructure for AI-generated specifications.** Citation systems exist. Dependency tracking exists. But applying the suspect link pattern (from IBM DOORS requirements engineering) to an LLM specification chain — where hallucination rates are 11-95% and cascading errors hit 79% probability over 6 hops — is novel. The combination of mechanical citation (Anthropic Citations API), content hash staleness, and one-hop `derives_from` tracing is a new synthesis.

**3. Protocol-based integration for practice systems.** Dependency inversion is established in software architecture. Applying it to the *practice layer* — where validation, research, and review are swappable protocols rather than hardcoded tools — is new. This is what makes Momentum a composable system rather than a collection of skills.

**4. Three-tier enforcement mapped to portability layers.** The insight that deterministic (hooks) = Claude Code only, structured (workflows) = partially portable, advisory (rules) = fully portable — and designing the product so enforcement *degrades gracefully* across that spectrum — is a novel packaging strategy for developer tools in the multi-IDE era.

### What Is NOT Innovative (And Should Not Be Claimed)

- Spec-driven development (Kent Beck, StrongDM, others)
- Producer-verifier separation (established pattern)
- Agent Skills packaging (following the standard, not inventing it)
- TDD/ATDD (decades of established practice)
- Code review (standard software engineering)

The innovation is in the *composition* of established patterns and the *upstream trace model*, not in any individual component.

### Validation Approach

Each innovation area validates through dogfooding — Momentum is built using its own practice:
- **Upstream fix discipline:** Validated when the flywheel catches systemic issues across sprints and the fix prevents recurrence (Journey 2)
- **Provenance infrastructure:** Validated when stale sources are caught that would otherwise propagate (Journey 1 — expected immediately)
- **Protocol-based integration:** Validated when Momentum deploys on a different stack without breaking the practice layer (Journey 3)
- **Three-tier enforcement:** Validated when the same skills work in Claude Code (full enforcement) and other tools (advisory only)

## Product Scope & Phased Development

### MVP Strategy

**Approach:** Deployment-first, iterate-in-production. Prove the pipeline on Day 1, iterate functionality from Day 2. Real work on real projects is the test harness — no synthetic validation. One developer, limited hours, concurrent with other projects.

### Day 1 (Proves the Pipeline)

1. LICENSE committed (open source, first task, non-negotiable)
2. Skill package installs via `npx skills add momentum/momentum -a claude-code`
3. At least one hook fires (auto-lint on edit — simplest to verify)
4. Orchestrating agent loads and shows a menu
5. The install is repeatable

### Day 2-3 (Before First Sprint)

- Full hook suite (test protection, quality gate, file protection)
- Code-reviewer subagent operational
- Provenance/staleness detection (`derives_from` + content hash)
- Protocol interface definitions (validation, research, review, agents, tools, MCP, documents)
- README.md and CONTRIBUTING.md

### First Sprint

- Authority hierarchy rule in `.claude/rules/`
- Git integration as workflow infrastructure (frequent commits, reviewable history)
- Gherkin-based ATDD specification format (behavioral, technology-agnostic)
- Quality rules file for review workflows
- Upstream fix discipline (`/upstream-fix` skill)
- Model routing defaults with `model:` and `effort:` frontmatter
- Findings ledger scaffolded (with `provenance_status` field)
- Calibration principle operationalized: every finding requires evidence; false positives waste more time than missed issues
- AVFL validation (gate/checkpoint profiles) integrated into story cycles via momentum-dev — multi-lens validation pipeline with parallel reviewers across structural integrity, factual accuracy, coherence & craft, and domain fitness lenses; benchmarked model routing per role (Enumerator=sonnet, Adversary=opus, Consolidator=haiku, Fixer=sonnet)

### Growth Features (Post-MVP)

- **Impetus as Epic Orchestrator** — Impetus evolves from story-level guidance to epic-level and sprint-level orchestration: `triage` workflow for backlog shaping, `/create-epic` for bulk parallel story creation with AVFL validation, `/develop-epic` for dependency-driven DAG execution within a single epic, sprint planning for cross-epic story selection and team composition, sprint-dev for dependency-driven execution of sprint stories. The epic remains the primary unit for grouping and scoping work; the sprint is the primary unit for execution. Impetus dispatches agents, never implements. Human touchpoints at merge gates and critical AVFL findings only (see FR49–FR54, FR59–FR70)
- Standalone `/validate` command — user-invocable AVFL validation outside story cycles (full profile with iterative fix loop, up to 8 parallel reviewers); extends the story-cycle-integrated AVFL to ad-hoc artifact validation
- **Findings template** — standard + open sections format for validation reports, consumed by findings ledger and Evaluation Flywheel
- **Citations API + CoE integration** (PT-026) — wire Anthropic Citations API into spec generation workflows for mechanically grounded provenance; add Chain of Evidences prompting pattern
- BMAD Code Review enforcement of pure verifier role
- Automated flywheel with retrospective integration
- CLAUDE.md generation from architecture docs
- Benchmarking harness (promptfoo, bash scripts, golden datasets)
- Traceability infrastructure (reference scanner, link validator, suspect resolution)
- Stop hook quality gate with full conditional logic
- **Gemini MCP server** (PT-028) — automated multi-model research via `@rlabs-inc/gemini-mcp`
- **GPT deep research integration** — MCP-based access to GPT deep research capabilities for cross-model verification
- **Research prompt templates** (PT-029) — canonical templates with date-anchoring, primary-source directives, freshness scout role. Includes 3-tier depth presets (Light: 15-30min single-model quick scan; Medium: 1-2hr multi-model with cross-check; Heavy: half-day multi-model with Gemini/GPT deep research and full VFL validation)
- **Two-pass research verification** — Pass 1: fact-check before consolidation (catch errors early); Pass 2: full VFL validation after consolidation (verify synthesis quality)
- Alternative protocol implementations for validation, research, and review — enabling substitution across teams and tools

### Vision (Future)

- Near-autonomous spec-to-code pipeline with human only at gates
- Property-based testing and mutation testing
- Architectural fitness tests
- Cursor adaptation and cross-IDE deployment
- Team scaling, role distribution, multi-developer workflow
- Full protocol ecosystem — teams and organizations plug in their own implementations for each integration point
- Open-source packaging for external adopters

### Risk Mitigation

| Risk | Severity | Mitigation |
|---|---|---|
| Agent Skills ecosystem is pre-1.0 — packaging may change | High | Impermanence Principle: thin packaging layer, practice portable even if packaging changes. Monthly ecosystem review. |
| Context budget exhaustion — 68 BMAD (count as of BMAD v6; actual count varies by BMAD version) + Momentum skills | Medium | Concise descriptions (≤150 characters each), monitor matching quality |
| BMAD coexistence friction — two systems in `.claude/skills/` | Medium | BMAD is an implementation detail. As BMAD migrates to skills, friction decreases. Momentum works with or without BMAD. |
| Solo developer bottleneck — no peer review safety net | High | Momentum's own practice (code-reviewer, adversarial review) provides the safety net. Dogfooding is both the risk and the mitigation. |
| Protocol abstraction over-engineering | Medium | Define with one implementation. Refine when second implementation reveals what the first got wrong. |
| Provenance authoring friction — `derives_from` gets skipped | Medium | Downstream-only authoring, auto-generated backward references, agent assists with discovery |
| Ecosystem volatility invalidates packaging decisions | Medium | Accepted per Impermanence Principle. Practice is portable even if packaging changes. |
| Upstream fix too expensive for small projects | Low | Upstream fixes *reduce* total effort over time. Cost is front-loaded; savings compound. |

### Resource Reality

One developer, limited hours, concurrent with other projects. The MVP must be lean enough to ship in days, not weeks. Everything after Day 1 is iterative — each feature validated by real use before the next one starts.

## Developer Tool Specific Requirements

### Installation Architecture

**Single entry point via Agent Skills standard:**

```
momentum/                        # repo root
├── skills/
│   ├── momentum/                # Impetus — main entry point SKILL.md
│   │   ├── SKILL.md
│   │   └── references/          # bundled rules, hooks-config.json, mcp-config.json, momentum-versions.json
│   ├── momentum-code-reviewer/  # context:fork skill — peer, not child
│   │   └── SKILL.md
│   └── momentum-architecture-guard/  # context:fork skill — peer, not child
│       └── SKILL.md
├── .claude/
│   └── settings.json            # committed; always-on hooks written by Impetus
└── version.md
```

(Abbreviated — shows primary packaging structure. See Repository Structure section for complete directory layout.)

- All Momentum capabilities deploy via `npx skills add momentum/momentum -a claude-code` (Agent Skills standard)
- No plugin manifest, no plugin install — single distribution method
- Impetus writes rules, hooks, and MCP config to their target locations on first run (`momentum-versions.json` tracks what to write per version; `.claude/momentum/installed.json` records project configuration state)
- `context:fork` skills (code-reviewer, architecture-guard) are SKILL.md files with `context:fork` frontmatter — not plugin agents
- `showTurnDuration: true` is set in `.claude/settings.json` during installation as a cost observability default (implementation requirement, see Epic 1 Additional)

**Installation methods:**

| Method | Target | What's Installed |
|---|---|---|
| `npx skills add momentum/momentum -a claude-code` | Claude Code | Full system: skills + Impetus-managed global configuration (rules, hooks, MCP) |
| `npx skills add momentum/momentum -a claude-code -g` | Claude Code (global) | Skills available in all projects; Impetus-managed global configuration still required on first `/momentum` run per project |
| `npx skills add momentum/momentum -a claude-code` | Cursor | Skills only (advisory enforcement) |
| `git clone` (project repo) | Team members | Project-level config via `.claude/settings.json` |
| Global setup (prompted by Impetus) | New team member's machine | `~/.claude/` rules, hooks, MCP — written by Impetus on first `/momentum` run |

### Protocol-Based Integration Architecture

Every integration point in Momentum is a configurable protocol. The project configures which implementation satisfies each protocol.

**Identified protocol types:**

| Protocol Type | What It Governs | Example Substitutions |
|---|---|---|
| **Agent protocols** | Which agent performs a role | BMAD Dev ↔ Workflow Builder ↔ custom agent |
| **Skill protocols** | Which skill implements a capability | Momentum /validate ↔ team's existing review process |
| **Tool protocols** | Which tool executes a function | Playwright ↔ Kotest ↔ custom test runner |
| **MCP provider protocols** | Which LLM/service provides capability | Gemini ↔ GPT ↔ add 3rd/4th provider |
| **Document specification protocols** | What constitutes the spec tree | Story ↔ Task ↔ Spec ↔ custom top-level doc |
| **Terminal multiplexer protocols** | Which terminal manager provides pane/session management | CMUX (macOS) ↔ tmux (cross-platform) ↔ null (no multiplexer) |

**Configuration level:** Project-level. Each project can override default protocol implementations without affecting the practice layer.

**Terminal multiplexer integration:** Optional and protocol-bound (Epic 7). Skills must use the detect-and-adapt pattern — check for environment indicators and adapt behavior when present; never require a specific multiplexer. Three anti-patterns (cross-session orchestration instead of subagents, multiplexer as primary orchestrator, over-coupling to multiplexer environment) are documented in CMUX research and queued for anti-patterns rules (Story 3.4).

**Document specification protocol:** The specification tree varies team to team. Momentum does not prescribe a shape (Brief → PRD → Architecture → Epic → Story). Instead:
- Top-level specification documents self-identify (frontmatter marker)
- Each document declares `derives_from` — its upstream dependencies
- The full `derives_from` chain IS the specification — Momentum navigates the chain, it doesn't prescribe it
- Provenance infrastructure works regardless of what the documents are called or how they're organized

### Progressive Configuration Discovery

When the orchestrating agent encounters ambiguous or missing configuration — unclear test runner, no ATDD tool specified, missing MCP provider — it does not guess. It asks the user, sets the choice into the project configuration, and records the decision with provenance (who decided, when, why). Over time, the configuration file becomes a complete picture of how this project implements each protocol.

**The configuration file is itself a specification document:**
- Has `derives_from` (what informed the decisions)
- Tracks authorship and decision rationale
- Participates in the provenance chain
- Whether it's a standalone `momentum.config.yaml`, part of `project-context.md`, or another form is an architecture decision
- Committed to the repo so team members inherit the decisions via `git clone`

**Requirements:**
- Exists at project level
- Maps protocols to implementations (which test runner, which validator, which agents, which LLM providers)
- Each entry carries provenance (when configured, by whom, why)
- The orchestrating agent reads it, detects gaps, and helps fill them conversationally
- Gaps are resolved through dialogue, not defaults that silently assume

### Documentation & Repository Structure

**Required Day 1 (before any other work):**
- **LICENSE** — open source license. First task, non-negotiable.

**Required for MVP:**
- **README.md** — philosophy and practices (or links to canonical docs), getting started/installation for Claude Code
- **CONTRIBUTING.md** — how to contribute, IDE directory structure for new IDE support, protocol implementation guidelines

**Repository structure:**
```
momentum/
├── LICENSE
├── README.md
├── CONTRIBUTING.md
├── version.md              ← single version source for all skills
├── skills/
│   ├── momentum/           ← Impetus — main entry point
│   │   ├── SKILL.md
│   │   └── references/    ← bundled rules, hooks-config.json, mcp-config.json, momentum-versions.json
│   ├── momentum-avfl/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   └── framework.json
│   │   └── sub-skills/          ← nested internal sub-skills (deploy with parent)
│   ├── momentum-code-reviewer/    ← context:fork skill (peer, not nested)
│   │   └── SKILL.md
│   ├── momentum-architecture-guard/   ← context:fork skill (peer, not nested)
│   │   └── SKILL.md
│   ├── momentum-upstream-fix/
│   │   └── SKILL.md
│   ├── momentum-create-story/
│   │   └── SKILL.md
│   └── momentum-dev-story/
│       └── SKILL.md
├── rules/                  ← source for bundled rules (advisory)
├── mcp/                    ← custom MCP server source
├── docs/
├── .claude/
│   ├── rules/              ← authority hierarchy rules (auto-load)
│   ├── skills/             ← installed skills
│   └── settings.json       ← always-on hooks (committed)
└── _bmad-output/           ← planning artifacts
```

**Provenance for all documentation:**
- Every document tracks what it derives from (`derives_from` frontmatter)
- Human-authored vs AI-generated is a provenance distinction worth tracking
- Archive preserves the reference chain — outdated docs moved to `docs/archive/`, not deleted (deletion policy is a future decision; git preserves history regardless)
- The reference tree is navigable: README → principles → research → sources

### Adoption Path

**Solo developer (MVP):** Install via `npx skills add momentum/momentum -a claude-code`, then run `/momentum`. Impetus handles global configuration interactively on first run. Ships with documented default protocol implementations (built-in validator, Gherkin ATDD, standard code-reviewer). The orchestrating agent detects missing configuration and helps fill gaps conversationally.

**Team member:** `git clone` delivers project-level config. Orchestrating agent detects missing global components and prompts one-time setup. After initial global install, no further configuration is needed — project-level settings propagate via the repo.

**Existing BMAD users:** Momentum skills coexist with BMAD skills in `.claude/skills/`. BMAD is used to build Momentum but is an implementation detail, not a dependency for users.

**Future (Growth):** Project configuration discovery — Momentum detects existing tools and spec structure, auto-configures protocol implementations.

### Implementation Considerations

- **Context budget management:** With 68 BMAD skills installed (count as of BMAD v6; actual count varies by BMAD version), keep Momentum skill descriptions ≤150 characters each. All Momentum skills are flat skills (no plugin namespacing). Monitor for skill matching degradation as total count grows.
- **Version management:** `momentum-versions.json` bundled in the package — machine-readable per-version action list (what files to write, where, for each version). `.claude/momentum/installed.json` written by Impetus at project level — records what version the project is currently configured for. Always bump version on changes.
- **`installed.json` commit policy:** `.claude/momentum/installed.json` must be committed to the project repository. It records the Momentum version the project is configured for — without it, team members joining via `git clone` cannot receive correct incremental upgrade instructions and will be prompted for a full install instead. `.gitignore` must NOT exclude `.claude/momentum/installed.json`; it is intentionally tracked, unlike most `.claude/` contents which may be gitignored.
- **Testing strategy:** promptfoo for skill output quality, `run_eval.py` for trigger precision, local `npx skills` development iteration.
- **Tool/runtime management:** mise is the standard polyglot tool manager for developer environments using Momentum. When Momentum skills, workflows, or rules reference installing runtimes (node, python, ruby, go, java) or CLI tools, they must prefer `mise use` over legacy single-purpose managers (nvm, pyenv, rbenv, asdf, volta, fnm) or global package installs (`npm install -g`, `pip install --user`). This is enforced by global Claude Code rules (`~/.claude/rules/mise.md`) and the anti-patterns rule. Momentum does not bundle or install mise itself — it is a prerequisite of the developer environment.

## Functional Requirements

### Installation & Deployment

- **FR1:** Developer can install Momentum skills via `npx skills add` into any Agent Skills-adopting IDE
- **FR2:** Developer (solo, first install) runs `npx skills add momentum/momentum -a claude-code` then `/momentum`; Impetus detects no `installed.json` exists, presents a pre-consent summary of what will be configured (global rules, hooks, MCP), and with explicit developer confirmation completes setup and writes `installed.json` recording `momentum_version` (set to the value of `current_version` from `momentum-versions.json`), `installed_at`, and per-component hashes
- **FR2b:** When Impetus starts and `installed.json` exists with `momentum_version` matching `momentum-versions.json` `current_version`, Impetus skips install and upgrade flows and proceeds directly to session orientation
- **FR2c:** When Impetus starts and `installed.json` exists but `momentum_version` does not match `current_version`, Impetus triggers the upgrade flow (FR3b)
- **FR3a:** Developer can run `npx skills update` to pull the latest Momentum package to disk; the updated package contains a revised `momentum-versions.json` with per-version action lists, such that the installed SKILL.md files and bundled references in `.claude/skills/momentum*/` are replaced with the new version's content
- **FR3b:** When Impetus starts and detects `momentum-versions.json` `current_version` differs from `installed.json` `momentum_version`, Impetus presents a structured upgrade summary — which files change, what each change does, which steps require restart — and requires explicit user confirmation before proceeding
- **FR3c:** Impetus executes upgrade actions sequentially across all intermediate versions between `momentum_version` and `current_version`, updating `installed.json` on successful completion; partial failures are reported with the step that failed and project state left unchanged from that step onward
- **FR4:** Team member can receive project-level Momentum configuration via `git clone` without manual setup
- **FR5:** Developer joining a project that has `.claude/momentum/installed.json` committed but lacks global Momentum components on their machine (rules, hooks) runs `/momentum`; Impetus detects missing global components and guides them through one-time global setup without re-running the full install sequence

### Orchestrating Agent

- **FR6:** Developer can interact with an orchestrating agent (Impetus) that presents menu-driven access to all practice workflows. Impetus is a pure orchestrator — it dispatches workflows and agents, never implements. At the epic orchestration level, the primary menu items are `/create-epic` and `/develop-epic`. At the sprint orchestration level, menu items include "Plan a sprint" and "Continue sprint". Impetus dispatches story creation agents, DAG execution agents, and sprint workflow modules from parent context rather than performing implementation work itself
- **FR7:** Orchestrating agent can show the developer's current position in any workflow via visual status graphics (ASCII)
- **FR8:** Orchestrating agent can provide human-readable summaries of what was built during implementation, while review runs. Summaries follow attention-aware checkpoint patterns (UX-DR19) — lead with micro-summary, offer tiered review depth — and indicate confidence levels on presented content (UX-DR22)
- **FR9:** Orchestrating agent can detect ambiguous or missing project configuration and guide the developer through resolution conversationally, including at minimum: gaps in the protocol mapping table (FR35), missing MCP provider configuration, and undefined ATDD tool binding
- **FR10:** Orchestrating agent can contextualize specifications just-in-time — explaining relevant architectural decisions, acceptance criteria, and prior choices at the moment they're needed, rather than requiring document reading. Guidance depth adapts to expertise level (UX-DR20); every drill-down is framed with why it matters (UX-DR21)
- **FR11:** Developer can ask follow-up questions during any workflow step, and the agent treats questions as discovery opportunities that may improve the specification. Answers are framed with motivated context — why the information matters to the current task (UX-DR21)

### Provenance & Traceability

- **FR12:** Developer can declare `derives_from` relationships in document frontmatter, tracing each document to its upstream sources
- **FR13:** System can detect staleness using two modes: hash-based for internal documents (compare `derives_from` content hash to current upstream hash) and time-based for edge documents (compare research date to domain-specific freshness windows). Stale downstream documents are flagged as SUSPECT, not auto-updated — one-hop propagation only, human/verifier-gated at each level.
- **FR14:** System can auto-generate backward references (`referenced_by`) from forward `derives_from` declarations — no manual maintenance of backward links
- **FR15:** Top-level specification documents can self-identify via frontmatter marker, enabling the system to discover the specification tree for any project
- **FR16:** Developer can track provenance status of claims (VERIFIED, CITED, INFERRED, UNGROUNDED, SUSPECT)
- **FR17:** System can distinguish human-authored from AI-generated content in provenance metadata

### Enforcement & Quality Governance

- **FR18:** System can auto-lint and auto-format code on every file edit (PostToolUse hook)
- **FR19:** System can block modifications to acceptance test directories (PreToolUse hook)
- **FR20:** System can run conditional quality gates before session end — tests only when any source file outside `tests/acceptance/` was written or edited during the current session (detectable via PostToolUse Write/Edit event tracking in session state), lint always (Stop hook)
- **FR21:** System can protect specified files from modification (PreToolUse hook)
- **FR22:** System can ensure authority hierarchy rules auto-load in every Claude Code session including subagents via `.claude/rules/` — no manual loading required
- **FR23:** Developer can configure model routing defaults per skill and agent via `model:` and `effort:` frontmatter, with a documented default strategy: Sonnet 4.6 at medium effort for general tasks; upgrade to Opus for complex reasoning, orchestration, or outputs without automated validation (cognitive hazard rule: invisible errors from cheaper models cost more than the flagship premium); downgrade to Haiku for well-constrained tasks with downstream validation

### Verification & Review

- **FR24:** Code-reviewer subagent can perform adversarial review with read-only tools, producing structured findings reports
- **FR25:** Code-reviewer can be prompted or triggered automatically at implementation completion, not requiring manual invocation
- **FR26:** Findings reports can include provenance status for traceability-dimension findings
- **FR27:** Every finding requires evidence — validators cannot generate findings without supporting evidence from the reviewed artifact (calibration principle)
- **FR48:** AVFL skill deployed as flat skill at `momentum-avfl/` supporting gate/checkpoint/full profiles; spawns parallel reviewers across structural integrity, factual accuracy, coherence & craft, and domain fitness lenses; cross-checks findings between independently-framed reviewers; returns consolidated scored findings with evidence; sub-skills nested inside the skill directory deploy automatically with the parent skill. AVFL runs at sprint level: during planning it validates the complete sprint plan (all stories together as one pass), and during execution a single AVFL pass runs after all sprint stories have merged — not per-story, not per-wave. The profiles (gate/checkpoint/full) remain valid within the sprint-level invocation context

### Epic Orchestration

*These requirements belong to Epic Y (Impetus as Epic Orchestrator).*

- **FR49:** `triage` workflow accepts raw input — conversational or file-based (`triage-inbox.md`) — and produces mutations to `epics.md`: story titles, one-line scope, epic assignments, priority ordering. Only unlocked epics (those without story files already created) are mutable. Cross-epic dependency violations are surfaced before committing changes. Triage is repeatable — it may be run any number of times before `/create-epic` is called on an epic. **Priority: High**
- **FR50:** `/create-epic` command locks the target epic at invocation time, dispatches parallel story creation agents (one per story, batch of 4–8), runs an AVFL pass on all created stories from the parent context, and marks the epic locked on all-CLEAN result. Lock point is when `/create-epic` is called — not after AVFL, not after developer approval. Epic is immutable after this point. **Priority: High**
- **FR51:** `/develop-epic` command executes a dependency-driven DAG across the epic's stories. Pre-flight validation includes: topological sort, cycle detection, key normalization, dangling reference check, and file-overlap warning between concurrently runnable stories. Stories with satisfied dependencies execute in parallel (dependency-driven concurrency — not rigid wave tiers); when a story completes and merges, previously blocked stories are checked and spawned if unblocked. AVFL validation runs once after all stories have merged — not per-story, not per-wave. Orchestrator handles merge gate — never background agents. Agent concurrency cap is configurable (default 12). Integration with a dag-executor skill (e.g., by Erich Owens) is supported as a swappable scheduler via the skill protocol. **Priority: High**
- **FR52:** Epic lifecycle is the primary unit of planned work, progressing through five phases: (1) **Triage** — mutable, repeatable, any number of times before `/create-epic`; (2) **Create-epic** — locks epic, creates story files in parallel, AVFL validates; (3) **Develop-epic** — DAG execution, tier-sequential, merge at each tier; (4) **Retro** — structured retrospective, writes `triage-inbox.md` entries for next cycle; (5) **Triage** — next cycle begins. Epic is immutable after create-epic. If a blocker or scope change occurs mid-epic, the epic is closed with status `done-incomplete` and incomplete stories are re-triaged into the next cycle. **Priority: High**
- **FR53:** `momentum-dev` is a pure executor: worktree setup, bmad-dev-story invocation, agent logging, and structured completion signal — no AVFL invocation, no status transitions, no DoD supplement, no code review offer. AVFL and status transitions are handled by the orchestration layer (Impetus / sprint-dev). The completion output emits a structured JSON signal (status, files modified, test results) that the caller can parse. momentum-dev can still be invoked standalone; logging calls degrade gracefully when no sprint context exists. The merge gate still requires developer confirmation. This subsumes the original `momentum-dev-auto` intent — the base momentum-dev is itself the stripped-down executor. **Priority: High**
- **FR54:** At session open, Impetus reads `stories/index.json` and `sprints/index.json` and renders a 3-line epic progress bar as the first visible output — before any menu or preamble. Format: done epic(s), current in-progress epic(s) with story counts, next backlog epic. A two-sentence synthesis follows. For experienced users (`momentum_completions >= 3`), the progress bar is compressed to a single line. No preamble text precedes the progress bar. **Priority: High** *(Epic X — Impetus UX Redesign)*

### Evaluation Flywheel

- **FR28:** Findings ledger can accumulate findings across stories with category, root cause classification, and upstream level
- **FR29:** System can detect cross-story patterns in the findings ledger and surface systemic issues
- **FR30:** Flywheel can explain detected issues to the developer and suggest upstream trace with visual workflow status (detection → review → upstream trace → solution → verify → log)
- **FR31:** Developer can approve or reject each flywheel suggestion — the agent never proceeds without explicit consent
- **FR32:** Upstream fixes can be applied at any level: spec-generating workflow, specification, CLAUDE.md/rules, tooling, or one-off code fix
- **FR33:** System can track the ratio of upstream fixes to code-level fixes as a practice health metric

### Protocol-Based Integration

- **FR34:** Developer can configure which agent, skill, tool, MCP provider, or document structure satisfies each protocol — at project level
- **FR35:** Project configuration file maps protocols to implementations with provenance (who configured, when, why)
- **FR36:** Orchestrating agent can read the project configuration, detect gaps in protocol mappings, and help fill them conversationally
- **FR37:** System can resolve workflow step invocations through protocol interfaces — workflow definitions reference protocol types, not specific implementations; Impetus reads the project configuration at invocation time, looks up which implementation satisfies the protocol type for the current step, and invokes that implementation
- **FR38:** Developer can substitute any protocol implementation without modifying the workflows that depend on it

### Specification & Development Workflow

- **FR39:** Developer can define acceptance criteria in plain English in story markdown files. Acceptance criteria are behavioral, technology-agnostic, and implementation-independent. Story files never contain Gherkin — detailed Gherkin specs are generated separately during sprint planning and stored in the sprint-scoped specs directory
- **FR40:** ATDD workflow can generate failing acceptance tests from Gherkin criteria before implementation begins
- **FR41:** Developer can complete a full story cycle guided by the orchestrating agent: spec review → ATDD → implement → review → flywheel. Two orchestration models coexist: (1) Epic orchestration — stories created in bulk by `/create-epic` and executed as a DAG by `/develop-epic`; (2) Sprint orchestration — stories pulled from across epics during sprint planning, executed via dependency-driven concurrency by sprint-dev. In both models, individual story cycles are invoked by Impetus; the developer interacts at the orchestration unit's granularity (epic or sprint)
- **FR42:** System can track visual progress through the story cycle, always showing current phase and next phase
- **FR43:** Developer can invoke the upstream fix skill to analyze a quality failure and propose corrections at the appropriate upstream level

### Research & Knowledge Management

- **FR44:** Developer can conduct multi-model research using MCP-integrated LLM providers (Gemini, GPT, and additional providers)
- **FR45:** System can enforce date-anchoring and primary-source directives in research agent prompts — research prompts missing a date anchor constraint or primary-source preference directive are flagged before execution
- **FR46:** Developer can archive outdated documents to a designated directory while preserving their reference chain
- **FR47:** System can track document freshness using domain-specific freshness windows (90 days for AI/LLM, 6 months for tooling, 12 months for standards, 24 months for principles)

## Non-Functional Requirements

### Context Window & Token Economics

- **NFR1:** Each Momentum skill description must be ≤150 characters to minimize startup context budget impact
- **NFR2:** Skill matching accuracy must remain >=95% (correct skill invoked on first attempt) when Momentum skills are added to an environment with 68+ existing BMAD skills, as measured by manual spot-checks during dogfooding
- **NFR3:** Skill instructions should stay under 500 lines / 5000 tokens per the Agent Skills spec recommendation
- **NFR4:** All Momentum skills are flat skills deployed via Agent Skills standard; no plugin namespacing is used or required. (Deployment architecture constraint — grouped here because flat skill deployment eliminates plugin overhead from the context budget.)

### Portability & Graceful Degradation

- **NFR5:** All SKILL.md files must be valid Agent Skills standard — parseable by any of the 17+ adopting tools
- **NFR6:** Claude Code-specific frontmatter (`context: fork`, `model`, `effort`) must be additive — skills must function correctly when these fields are ignored by non-Claude Code tools
- **NFR7:** Enforcement must degrade across three defined tiers: Tier 1 full deterministic (Claude Code — hooks fire via `.claude/settings.json` written by Impetus, subagents enforce via `context:fork` skills, rules auto-load via `.claude/rules/` written by Impetus), Tier 2 advisory (Cursor/other tools with skills only — skill instructions guide but don't enforce), Tier 3 philosophy only (no tooling — principles documented in README). Each tier must be explicitly tested: Tier 1 via `npx skills add momentum/momentum -a claude-code` + `/momentum` first-run setup; README explicitly documents this configuration as Tier 1. Tier 2 via `npx skills add` into a non-Claude Code tool. Tier 3 validated by: verifying the README documents all three enforcement tiers and their respective capabilities and limitations; confirming that the practice principles are documented in a form that is actionable without any tooling installation.
- **NFR8:** No Momentum workflow definition may import or reference a Claude Code-specific API directly. Workflows depend on protocol interfaces; protocol implementations resolve to Claude Code features at runtime. Validated by: every workflow SKILL.md must parse and execute (at advisory level) in at least one non-Claude Code tool.

### Ecosystem Resilience

- **NFR9:** A breaking change in any single ecosystem dependency (BMAD major version, Agent Skills spec) must be absorbable by modifying only the packaging/distribution layer (install scripts, frontmatter, momentum-versions.json), not the practice content (skill instructions, rules, agent definitions). Validated by: practice content files have zero imports of ecosystem-specific APIs.
- **NFR10:** All ecosystem dependencies (BMAD version, Agent Skills spec version) must be tracked and reviewed at minimum monthly
- **NFR11:** The packaging/distribution layer must comprise <=5% of total Momentum files (by count). Replacing the entire packaging mechanism must not require changes to any skill instruction, rule, or agent definition file.

### Integration Compatibility

- **NFR12:** Momentum skills must coexist with BMAD skills in `.claude/skills/` without namespace conflicts or matching interference
- **NFR13:** Momentum hooks must merge cleanly with existing project hooks and BMAD hooks — no silent override
- **NFR14:** MCP provider integrations must respect Cursor's ~40 active tool ceiling when Momentum is used in Cursor environments
- **NFR15:** Protocol implementations must satisfy documented interface contracts. Validated by: substituting any protocol implementation with a different one that satisfies the same contract must not cause any consuming workflow to fail or produce different structural output.

### Dogfooding Integrity

- **NFR16:** Every Momentum feature must be validated by real use on at least one active project before being considered stable. Synthetic unit tests are supplementary, not primary validation. Validated by: each feature's release notes reference the project(s) and story cycle(s) where it was dogfooded.
- **NFR17:** The meta-risk (system amplifying its own blind spots via dogfooding) must be mitigated by external validation: adversarial review by separate context, multi-model research cross-checking, and explicit human checkpoints at critical decisions

### Review Sustainability

- **NFR18:** All Momentum workflow checkpoints that pause for human review must implement spec fatigue mitigation patterns (UX-DR19 through UX-DR22): lead with micro-summary and tiered review depth (UX-DR19), adapt guidance to expertise level (UX-DR20), frame drill-downs with motivated context (UX-DR21), and indicate confidence levels on generated content (UX-DR22). Validated by: behavioral evals confirm each checkpoint offers tiered review depth (not full-artifact dump) and flags confidence levels on generated content.

## Sprint Status Definitions

> _Revised 2026-04-02: Data model decomposed to `stories/index.json` and `sprints/index.json`; `momentum-tools.py` CLI replaces sprint-manager subagent as sole writer; sprint AVFL replaces wave AVFL; sprint lifecycle definition added._

`stories/index.json` and `sprints/index.json` are the authoritative state files for story and sprint tracking. All writes go through `momentum-tools.py` (exclusive write authority via CLI tool, not subagent). `stories/index.json` contains the flat story registry with status, epic membership, and dependencies. `sprints/index.json` contains active, planning, and completed sprint records including team composition and dependency graphs. See architecture doc for full schema.

### Story Statuses

| Status | Meaning |
|---|---|
| `backlog` | Story exists in epics.md/sprint-status.yaml; no story file yet. |
| `ready-for-dev` | Story file created; waiting to be picked into a sprint. |
| `in-progress` | Sprint-dev agent actively working it (worktree active). |
| `review` | Worktree merged to main; awaiting post-merge sprint AVFL. |
| `verify` | AVFL passed; behavioral verification running (momentum-verify). |
| `done` | Verified, complete. |
| `dropped` | Removed — obsolete or duplicate (pre-development cancellation). |
| `closed-incomplete` | Story in a force-closed sprint; migrated to next sprint or dropped. Worktree preserved. |

### Epic Statuses

| Status | Meaning |
|---|---|
| `backlog` | Epic defined in `epics.md`; stories may be added/removed freely. |
| `in-progress` | At least one story in this epic is in-progress or later. |
| `done` | All stories completed successfully. |
| `done-incomplete` | Epic force-closed mid-execution. Some stories completed; others incomplete or dropped. |

### Story ID Format

Story IDs are globally unique kebab-case slugs with no epic encoding. This allows stories to be re-categorized across epics without renaming. Examples: `posttooluse-lint-hook`, `impetus-identity-redesign`. Collisions resolved by adding a qualifier suffix.

### FR55: Sprint-Manager Exclusive Write Authority

- **FR55:** All writes to `stories/index.json` and `sprints/index.json` go through `momentum-tools.py`, a Python CLI tool invoked via Bash. No other agent, skill, or script writes to these files directly. This ensures atomic status transitions and prevents concurrent write conflicts. **Priority: High** *(Redesign Foundation)*

### Agent Observability

- **FR56:** Every agent (Impetus, dev, QA, E2E Validator, verifiers) must write structured JSONL logs via `momentum-tools log` throughout execution. The tool accepts `--agent`, `--event`, `--detail`, `--story` (optional), and `--sprint` (required) arguments. Valid event types: `decision`, `error`, `retry`, `assumption`, `finding`, `ambiguity`. Logs are append-only, stored at `.claude/momentum/sprint-logs/{sprint-slug}/`. Per-agent exclusive write authority on log files. Log entries contain ISO 8601 timestamp, agent, story (or null), event type, and detail text. **Priority: High** *(Phase 3)*
- **FR57:** Agent logging must be non-blocking and fault-tolerant — log calls degrade gracefully when no sprint context exists, when the sprint-logs directory has not been created, or when momentum-tools is not available. Logging failures never block agent execution. **Priority: High** *(Phase 3)*

### Gherkin Separation

- **FR58:** Story markdown files contain plain English acceptance criteria only. Detailed Gherkin `.feature` specs are generated during sprint planning and written to `sprints/{sprint-slug}/specs/{story-slug}.feature`. Dev agents never access the specs directory. Verifier agents read Gherkin specs exclusively from this path. This enforces black-box behavioral validation — developers implement against intent (plain English ACs), while verifiers validate against precise behavioral specifications (Gherkin). **Priority: High** *(Phase 3)*

### Sprint Planning & Execution

- **FR59:** Sprint planning workflow includes: backlog presentation (grouped by epic, excluding terminal states), story selection (3-8 stories with dependency warnings), story fleshing-out (spawn momentum-create-story for stubs), Gherkin spec generation, team composition, AVFL validation of the complete plan, developer review, and sprint activation. Planning decisions are logged throughout via the agent logging tool. **Priority: High** *(Phase 3)*
- **FR60:** Sprint planning determines team composition: which agent roles the sprint needs (based on story `change_type` and `touches`), what project-specific guidelines each role receives, and which stories can run concurrently based on the dependency graph. Team composition is stored in the sprint record and read by sprint-dev for execution. **Priority: High** *(Phase 3)*
- **FR61:** Agent guidance uses a two-layer model. Momentum provides generic agent roles (Dev, QA, E2E Validator, Architect Guard) with orchestration patterns, logging requirements, and quality gates. Projects provide role-specific guidelines per role (e.g., stack conventions, TDD requirements). Sprint planning wires the two layers together for each story based on `change_type` and `touches`. **Priority: High** *(Phase 3)*
- **FR61a:** Developer can invoke an agent-guidelines workflow that discovers the project's technology stack, researches current state and breaking changes, interactively recommends testing tools and validation approaches, and generates path-scoped rules (`.claude/rules/*.md`), reference docs (`docs/references/*.md`), and CLAUDE.md updates. The workflow uses parallel subagents for discovery and research, and validates generated artifacts via AVFL checkpoint. **Priority: High** *(Phase 3)*
- **FR62:** Sprint execution reads the activated sprint record, creates a task list for progress tracking, spawns momentum-dev agents for unblocked stories (each in its own worktree), tracks completion via tasks, handles dependency-driven sequencing, runs post-merge AVFL, executes black-box verification against Gherkin specs, and surfaces a sprint summary. Every merge requires explicit developer confirmation. **Priority: High** *(Phase 3)*
- **FR63:** Sprint execution spawns one agent per unblocked story (stories with no unmet dependencies). When a story completes and merges, sprint-dev checks whether previously blocked stories are now unblocked and spawns agents for those. Dependency ordering is strict — stories never start before all blockers have merged. This replaces rigid wave-tier scheduling with dependency-driven concurrency. **Priority: High** *(Phase 3)*
- **FR64:** AVFL validates the complete sprint plan during sprint planning (all stories together as one validation pass). During sprint execution, a single AVFL pass runs after all stories have merged — not per-story, not per-wave. This catches cross-story integration issues. **Priority: High** *(Phase 3)*
- **FR65:** In Phase 3, verification takes the form of a developer-confirmation checklist derived from Gherkin scenarios — each scenario becomes a checkbox item the developer confirms. Full automated verification is deferred. Unconfirmed items become findings to address or follow-up stories. **Priority: High** *(Phase 3)*

### Sprint Retrospective

- **FR66:** The retrospective workflow analyzes all agent logs from the sprint and produces two triage outputs: (1) Momentum triage — practice-level issues feeding back into Momentum's own refinement cycle, (2) Project triage — project-level issues feeding back into the project's refinement cycle. Both outputs derive from the same evidence base (agent JSONL logs stored in `.claude/momentum/sprint-logs/{sprint-slug}/`). **Priority: High** *(Phase 5)*

### Sprint Lifecycle

The sprint is the primary execution unit for Phase 3 and beyond. Stories are pulled from across epics during sprint planning (not bound to a single epic). The sprint lifecycle progresses through five phases:

1. **Plan** — story selection from backlog (cross-epic), story fleshing-out, Gherkin spec generation, team composition, AVFL validation of complete plan, developer approval, sprint activation
2. **Execute** — dependency-driven agent spawning (one momentum-dev per unblocked story), implementation in worktrees, progress tracking via tasks, merge gates with developer confirmation
3. **Verify** — post-merge AVFL (single pass on full codebase), black-box verification against Gherkin specs (Phase 3: developer-confirmation checklist)
4. **Complete** — sprint archival via `momentum-tools sprint complete`, sprint summary (stories completed, merge order, AVFL findings, verification results)
5. **Retro** — agent log analysis, two-output triage (Momentum practice issues + project issues), findings feed back into respective refinement cycles

The sprint model coexists with the epic orchestration model (FR49-FR53). Epics remain the primary unit for grouping related stories and managing scope. Sprints are the primary unit for execution — stories selected into a sprint may come from multiple epics. `/create-epic` produces stories; sprint planning selects stories for execution. `/develop-epic` remains valid for executing all stories within a single epic as a batch; sprint-dev provides the cross-epic execution model.

### Operational Requirements

- **FR67:** Multi-step workflows use task-based tracking for position and progress that survives context compression. Sprint-dev creates a task per story with dependency metadata, updating task status as stories progress through the execution loop. **Priority: High** *(Phase 3)*
- **FR68:** The sprint record in `sprints/index.json` stores team composition (roles, guidelines, story assignments) and the dependency graph. Sprint planning writes this record; sprint-dev reads it. The schema is defined by the architecture document. **Priority: High** *(Phase 3)*
- **FR69:** Sprint slugs follow the convention `sprint-YYYY-MM-DD` (date of planning). Same-day multiples append a sequence suffix: `sprint-2026-04-03-2`. **Priority: Medium** *(Phase 3)*
- **FR70:** Sprint execution handles errors gracefully: no active sprint surfaces an error and returns to session menu; unlocked sprint surfaces an activation error; agent failure offers retry or skip (no auto-retry); merge conflicts surface with diff context for developer resolution; AVFL critical issues block verification until resolved; declined verification items log as findings with option to create follow-up stories. **Priority: High** *(Phase 3)*

## Post-PRD Actions

- Commit LICENSE as the first artifact in the Momentum repository
