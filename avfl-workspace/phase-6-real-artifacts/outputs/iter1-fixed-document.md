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
  - id: BACKLOG-MOMENTUM-001
    path: docs/process/process-backlog.md
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

Industry data is unambiguous: AI code generation without governance fails. 67.3% of AI-generated PRs are rejected (vs 15.6% for human code). AI-generated code produces 1.7x more issues per PR. Experienced developers are 19% slower with AI tools while believing they're 20% faster. Organizations see PR volume increase 98% but delivery metrics stay flat. *(Source: multi-model-benchmarking-handoff-2026-03-14.md and preliminary-findings-momentum-as-skills-2026-03-13.md — see inputDocuments.)* The problem is not the tools. The problem is the absence of a verification architecture, a quality discipline, and a continuous improvement practice around them.

Momentum provides that missing layer through eight composable principles: spec-driven development, an authority hierarchy (specifications > tests > code — encoded into machine-readable `derives_from` chains enforced by tooling), producer-verifier separation, an evaluation flywheel (a feedback loop that traces quality failures upstream through the specification chain to the workflow or rule that produced them, fixes at that level, and measures whether the fix prevents recurrence — see Evaluation Flywheel section), three tiers of enforcement (deterministic hooks, structured workflows, advisory rules), cost as a managed dimension (the cognitive hazard rule: for outputs without automated validation, use flagship models — invisible errors cost more than the price premium), provenance as infrastructure, and protocol-based integration (each major capability defines an interface so implementations can be substituted across teams, tools, and environments). The system is delivered as standard Agent Skills — installable via `npx skills`, portable across 17+ AI coding tools, with Claude Code-specific enforcement (hooks, subagents, rules) bundled as a plugin for full Tier 1 deterministic governance.

The primary user is a solo developer using AI coding tools who has experienced the initial thrill of speed and hit the wall: code that looks right but isn't, patterns that drift without anyone noticing, and growing unease about accumulating debt they can't see. Momentum is designed for this person first, with team adaptation as a future consideration.

### What Makes This Special

**Upstream fix discipline.** Most quality approaches fix symptoms — the code, the test, the failing PR. Momentum traces every failure to the workflow, specification, or rule that produced it and fixes *that*. Each upstream fix prevents a class of errors permanently. The system gets smarter every sprint — not because the AI improves, but because the practice around it compounds.

**Provenance as infrastructure.** Every specification claim traces to a source. Every artifact tracks what it derives from and what depends on it. Ungrounded claims are marked, not assumed valid. When upstream documents change, downstream documents are flagged as suspect. This is not documentation hygiene — it is load-bearing infrastructure that enables the flywheel, prevents hallucination propagation, and stops obsolete decisions from resurfacing.

**Standard packaging with tool-optimized enforcement.** The principles are tool-agnostic. The skills are portable (Agent Skills standard, 17+ tools). The enforcement is Claude Code-optimized (hooks that always fire, subagents with read-only tools, rules that auto-load every session). One set of SKILL.md files serves both audiences — extra frontmatter fields are silently ignored by tools that don't understand them. This is not a compromise; it is the intended design of the spec.

## Project Classification

- **Project Type:** Developer Tool (practice system delivered as Agent Skills)
- **Domain:** Agentic Engineering
- **Complexity:** Medium — no regulatory compliance, but multi-tool portability, evolving ecosystem dependencies (BMAD, Agent Skills standard, Claude Code plugins), and the meta-nature of a practice that governs practices
- **Project Context:** Greenfield

## Success Criteria

### User Success

**First value signal: Provenance catches stale sources.** The system flags outdated or questionable sources in specification documents — something that currently happens daily without detection. Expected to deliver value immediately upon first use.

**Second value signal: The flywheel turns.** A quality failure traces upstream to a workflow, spec, or rule. The fix prevents a class of errors permanently. The developer sees the system learn.

**Sustained value: Specs improve, work accelerates.** As the developer works through stories, specifications get better instead of fragmenting. Time spent on specs decreases instead of steadily increasing. Code quality improves because the specs driving generation improve. The developer feels more engaged and more confident — not because AI got smarter, but because the practice around it compounded.

**The defining outcome:** The developer completes stories faster with fewer rework cycles, because the specifications driving generation improve with every sprint. The compounding is measurable: fewer upstream fixes needed, fewer critical findings per story, less time revising specs.

### Business Success

Momentum is not a commercial product. Success is measured in practitioner outcomes:

- **Personal productivity:** The solo developer ships higher-quality output with sustained or increased throughput, without accumulating the four debt types — *verification debt* (unvalidated outputs that require costly manual checking), *cognitive debt* (understanding gaps created when AI-generated code or decisions aren't fully comprehended by the developer), *pattern drift debt* (systemic issues introduced when AI follows stale or missing conventions), and *technical debt* (the conventional accumulation of shortcuts and deferred quality work)
- **Compounding improvement:** The amount of rework and spec revision *decreases* over time — a new experience compared to the typical trajectory where complexity compounds and quality degrades
- **Open-source viability:** An external adopter can install, configure, and get value without direct support from the creator. Future success criterion, not an MVP gate.

### Team Adoption Success (Growth-Phase)

These metrics apply when Momentum is used by team members beyond the solo developer. Not an MVP gate — included for traceability against Journey 4.

- **Onboarding completion:** New team member completes a full story cycle (spec → ATDD → implement → review) with agent guidance on their first day
- **Process adherence:** Team members follow the guided workflow without needing to read documentation front-to-back — the orchestrating agent delivers context just-in-time
- **Quality consistency:** Team member story output has <=2 critical findings from code review, comparable to the solo developer baseline
- **Team member sentiment:** Self-reported positive experience with the guided workflow (>=4/5 rating)

### Technical Success

- **Day 1: Deployable skill package installs and runs.** A prototype skill package — with hooks, rules, and at least one functional skill — deploys via `npx skills` (or plugin install for full enforcement). It doesn't need to be feature-complete. It needs to be *installable and usable*. If it can't be installed, nothing else can be verified.
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
| Developer confidence | >=4/5 self-reported rating after each sprint | 1-5 rating recorded manually at sprint retrospective (out of system scope — no automated collection) | Practice is earning trust |
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

**Rising Action:** Steve runs `npx skills add momentum -a claude-code` and installs the plugin. The orchestrating agent greets him, shows a menu of available workflows, and understands what practice artifacts already exist in his project. He picks a current side project as the first test bed. The hooks wire up immediately — auto-lint fires on his first edit, the acceptance test directory gets protected. The rules auto-load in every session.

He starts a story. The orchestrating agent shows him where he is in the process — a clear ASCII status graphic: **[Spec Review] → ATDD → Implement → Review → Flywheel**. He reviews the spec. When implementation completes, the agent prompts him: "Implementation complete. Ready to fire off the code-reviewer for adversarial review? While it runs, here's a summary of what was built..." The code-reviewer launches in a separate context. While it works, Steve reads a concise explanation of what the code does — not the code itself, but what it accomplishes, what architectural decisions it made, and how it maps to the acceptance criteria. He'd half-forgotten the details of the third AC. The summary brings him back in. The status graphic updates: **Spec Review → ATDD → Implement → [Review] → Flywheel**.

**Climax:** Two days in, he's working on a PRD and the provenance system flags a `derives_from` reference where the upstream document has changed since the PRD was written. It's a decision about packaging — the brief still references `momentum install` even though research showed that's obsolete. The system caught it. Without provenance, this stale decision would have silently propagated into the architecture doc, into stories, into code. The first value signal lands exactly as predicted — and it's the kind of thing that has cost him hours of rework before.

**Resolution:** By the end of the first sprint, Steve has completed a full story cycle with the practice: spec → Gherkin ATDD → implement → code review → flywheel. At every step he knew where he was, what the agent was doing, and what came next. The code review surfaces a finding. The flywheel explains the issue and suggests tracing upstream. He agrees. The system learned — and so did he.

**Requirements revealed:** Skill installation, plugin bundling, orchestrating agent with menu, hook infrastructure, provenance/staleness detection, code-reviewer subagent (prompted/automatic, not manual), visual status graphics showing current phase and next phase, human-readable implementation summaries during review, `derives_from` frontmatter, upstream fix workflow.

---

### Journey 2: Steve — The Flywheel Catches Something

**Opening Scene:** Steve is three sprints in. Momentum is part of his daily workflow. He's working on a complex feature across multiple stories. The specs are getting better — he spends less time revising acceptance criteria because the Create Story workflow now loads all the right context automatically (a flywheel fix from sprint 1).

**Rising Action:** The code-reviewer flags a pattern: the AI agent is using direct database queries in the service layer instead of going through the repository abstraction. This is the third time across three different stories. Each time it looked like a one-off — different service, different query, different story. But the findings ledger shows the pattern.

**Climax:** The flywheel explains the issue to Steve: "This is the third occurrence of direct database access bypassing the repository pattern. The findings ledger shows occurrences in stories S-04, S-07, and S-11. This looks systemic. I'd suggest we do a round of **upstream trace** to determine how far up the hierarchy this goes. Want to proceed?"

Steve agrees. The status graphic updates to show the flywheel workflow: **[Detection] → Review → Upstream Trace → Solution → Verify**. The agent walks through each level: Is it a code-level fix? No — three occurrences rules that out. Is it a CLAUDE.md/rules gap? Yes — the architecture doc specifies repository pattern, but `.claude/rules/` doesn't mention it. In ad-hoc sessions and subagent contexts, the AI defaults to direct queries because its training data suggests that's fine. The graphic advances: **Detection → Review → [Upstream Trace] → Solution → Verify**.

The fix: add a rule to `.claude/rules/architecture.md` specifying repository pattern as mandatory for data access. One rule, added once, prevents an entire class of errors permanently. The graphic completes: **Detection → Review → Upstream Trace → [Solution] → Verify**. Steve sees the rule, approves it, and the agent confirms it's active.

**Resolution:** The next two stories have zero data access violations. The time Steve would have spent catching and fixing these in code review is now zero. More importantly, he was *part of every step*. He wasn't wondering what the agent was doing — he saw the detection, understood the trace, approved the fix. The flywheel turned, and he turned it together with the system.

**Requirements revealed:** Findings ledger with cross-story pattern detection, flywheel workflow with visual status (detection → review → upstream trace → solution → verify), agent explains issues and suggests next steps (never proceeds without Steve), `.claude/rules/` as always-loaded enforcement, flywheel integration with retrospective, measurable improvement across sprints.

---

### Journey 3: Steve — Something Doesn't Fit

**Opening Scene:** Steve installs Momentum on a new project — a Kotlin/JVM backend, different from the TypeScript projects he's been using it with. The hooks fire, the rules load, but the ATDD workflow assumes Playwright/Cypress and the test commands are wrong.

**Rising Action:** The Stop hook quality gate tries to run `npm test` — which doesn't exist. It blocks his session. The ATDD workflow generates test scaffolding for a web frontend that doesn't exist. The validation protocol calls Momentum's default validator, which ships with general-purpose assumptions that don't account for JVM conventions.

**Climax:** Steve doesn't have to throw Momentum away. The protocol-based integration means each of these is a substitution, not a rewrite. He configures the test command in his project CLAUDE.md. He swaps the ATDD implementation to use Kotest (satisfying the same Gherkin → failing test interface). He points the validation protocol at a simplified validator that understands JVM conventions. The orchestrating agent still works — the menu, the workflow guidance, the flywheel — because the practice layer is independent of the implementation layer.

**Resolution:** Within an hour, Momentum is functional on the Kotlin project. Not every feature works perfectly — the code-reviewer's anti-pattern catalog is still web-heavy — but the core practice (spec authority, provenance, upstream fix discipline) operates identically. Over the next sprint, Steve adds Kotlin-specific rules to `.claude/rules/` via the flywheel. The system adapts to the new stack because it was designed to.

**Requirements revealed:** Protocol-based integration points, configurable test commands, stack-agnostic ATDD interface, swappable validation implementation, project-level configuration that overrides defaults, graceful degradation when a component doesn't fit.

---

### Journey 4: Future Team Member — Momentum Is Just There

**Opening Scene:** A developer on Steve's work team clones a project repo. They've never heard of Momentum. They're new to AI coding tools and currently follow a loose "read the docs, ask the senior dev" workflow.

**Rising Action:** They open Claude Code. The project-level hooks and rules activate automatically (configured in `.claude/settings.json` committed to the repo). But the orchestrating agent detects that the global Momentum components aren't installed on this developer's machine. It prompts: "This project uses Momentum for quality governance. Some components need a one-time global install. Would you like me to set that up?" The developer says yes. The global rules, agents, and practice infrastructure install to `~/.claude/`. Now everything works.

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
| Skill/plugin installation | ✓ | | | |
| Global install detection + guided setup | | | | ✓ |
| Orchestrating agent with menu | ✓ | | | ✓ |
| Visual status graphics (phase + next) | ✓ | ✓ | | ✓ |
| Hook infrastructure | ✓ | | ✓ | ✓ |
| Provenance/staleness detection | ✓ | | | |
| Code-reviewer subagent (prompted/auto) | ✓ | ✓ | | ✓ |
| Human-readable implementation summaries | ✓ | | | ✓ |
| Findings ledger + pattern detection | | ✓ | | |
| Flywheel workflow with visual status | | ✓ | | |
| Retrospective integration | | ✓ | | |
| Upstream fix workflow | ✓ | ✓ | | |
| `.claude/rules/` enforcement | | ✓ | ✓ | ✓ |
| Protocol-based integration | | | ✓ | |
| Stack-agnostic ATDD interface | | | ✓ | |
| Configurable project overrides | | | ✓ | |
| Just-in-time context delivery | | | | ✓ |
| Developer questions as discovery | | | | ✓ |
| Bidirectional improvement | | | | ✓ |

## Innovation & Novel Patterns

### Detected Innovation Areas

**1. Upstream fix as a formal discipline.** Quality approaches fix outputs. Momentum traces failures through a specification chain to the workflow that produced the defect and fixes that. This isn't incremental improvement on code review — it's a different model of where quality comes from. The flywheel is the mechanism; the insight is that in agentic engineering, the *process artifacts* are the product, not the code.

**2. Provenance as load-bearing infrastructure for AI-generated specifications.** Citation systems exist. Dependency tracking exists. But applying the suspect link pattern (analogous to techniques used in requirements traceability tooling such as IBM DOORS) to an LLM specification chain — where hallucination rates range from 11% to 95% depending on task type and cascading errors reach 79% probability over 6 hops in multi-step pipelines *(source: preliminary-findings-momentum-as-skills-2026-03-13.md)* — is novel. The combination of mechanical citation (Anthropic Citations API), content hash staleness, and one-hop `derives_from` tracing is a new synthesis.

**3. Protocol-based integration for practice systems.** Dependency inversion is established in software architecture. Applying it to the *practice layer* — where validation, research, and review are swappable protocols rather than hardcoded tools — is new. This is what makes Momentum a composable system rather than a collection of skills.

**4. Three-tier enforcement mapped to portability layers.** The insight that deterministic (hooks) = Claude Code only, structured (workflows) = partially portable, advisory (rules) = fully portable — and designing the product so enforcement *degrades gracefully* across that spectrum — is a novel packaging strategy for developer tools in the multi-IDE era.

### What Is NOT Innovative (And Should Not Be Claimed)

- Spec-driven development (established across many methodologies, including BDD and specification-by-example approaches)
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
2. Skill package installs via `npx skills` or plugin install
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

### Growth Features (Post-MVP)

- **Orchestrating agent evolves toward pipeline automation** — menu items gain workflow chaining (spec → ATDD → implement → review → flywheel), human touchpoints only at gates and critical findings
- `/validate` skill — full VFL validate-fix-loop engine (gate/checkpoint/full profiles), implemented behind the validation protocol interface. Includes: `source_material` required at checkpoint/full profiles, claim classification (SOURCED/DERIVED/ADDED/UNSOURCED), and model/effort routing per VFL profile and role (enumerator/adversary/fixer) with escalation semantics — mid-tier first, flagship if not converging within 3-4 iterations
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
| Plugin ecosystem is pre-1.0 — packaging may change | High | Impermanence Principle: thin packaging layer, practice portable even if packaging changes. Monthly ecosystem review. |
| Context budget exhaustion — 68 BMAD + Momentum skills | Medium | Concise descriptions, monitor matching quality, plugin namespacing may help (unverified) |
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

**Source separation by portability layer, merged at distribution time:**

*(Note: diagram below shows source layout only — the distribution input. For the full repository structure including docs/ and module/, see Documentation & Repository Structure below.)*

```
momentum/
├── skills/                  # Portable SKILL.md files (Agent Skills standard)
├── ide/
│   ├── claude-code/         # Hooks, agents, rules, plugin manifest
│   └── cursor/              # Future: Cursor-specific rules and config
└── package.json
```

- Standard skills live in `skills/` — portable across all 17+ Agent Skills-adopting tools
- IDE-specific enforcement lives in `ide/<ide-name>/` — cleanly separated for contribution
- Distribution merges the appropriate layers: Claude Code plugin assembles `skills/` + `ide/claude-code/`; Cursor package assembles `skills/` + `ide/cursor/`
- Contributing a new IDE requires only adding `ide/<new-ide>/` — no changes to base skills or other IDE layers

**Installation methods:**

| Method | Target | What's Installed |
|---|---|---|
| Claude Code plugin install | Claude Code | Full system: skills + hooks + agents + rules |
| `npx skills add momentum -a cursor` | Cursor | Skills only (advisory enforcement) |
| `git clone` (project repo) | Team members | Project-level config via `.claude/settings.json` |
| Global install (prompted by local agent) | New team member's machine | `~/.claude/` rules, agents, global practice |

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

**Configuration level:** Project-level. Each project can override default protocol implementations without affecting the practice layer.

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
├── skills/                  # Portable Agent Skills
├── ide/                     # IDE-specific layers
├── docs/
│   ├── archive/             # Outdated docs, still referenced, not deleted
│   ├── research/            # Active research documents
│   ├── research-final/      # Consolidated, validated research
│   └── specifications/      # Project specifications
└── module/                  # Canonical practice files (rules, agents, templates)
```

**Provenance for all documentation:**
- Every document tracks what it derives from (`derives_from` frontmatter)
- Human-authored vs AI-generated is a provenance distinction worth tracking
- Archive preserves the reference chain — outdated docs moved to `docs/archive/`, not deleted (deletion policy is a future decision; git preserves history regardless)
- The reference tree is navigable: README → principles → research → sources

### Adoption Path

**Solo developer (MVP):** Install via `npx skills` or plugin install. Ships with documented default protocol implementations (built-in validator, Gherkin ATDD, standard code-reviewer). The orchestrating agent detects missing configuration and helps fill gaps conversationally.

**Team member:** `git clone` delivers project-level config. Orchestrating agent detects missing global components and prompts one-time setup. After initial global install, no further configuration is needed — project-level settings propagate via the repo.

**Existing BMAD users:** Momentum skills coexist with BMAD skills in `.claude/skills/`. BMAD is used to build Momentum but is an implementation detail, not a dependency for users.

**Future (Growth):** Project configuration discovery — Momentum detects existing tools and spec structure, auto-configures protocol implementations.

### Implementation Considerations

- **Context budget management:** With 68 BMAD skills installed, keep Momentum skill descriptions extremely concise (~100 tokens each). Monitor for skill matching degradation as total count grows. Plugin-namespaced skills may not count against the flat budget (unverified — see technical-agent-skills-deployment-research-2026-03-15.md for current findings).
- **Version management:** Semantic versioning in `plugin.json`. Always bump version on changes (caching issue with git SHA pinning). Consider stable/latest channels via marketplace refs.
- **Testing strategy:** promptfoo for skill output quality, `run_eval.py` for trigger precision, `claude plugin validate` for manifest integrity, `--plugin-dir` for local development iteration.

## Functional Requirements

*Phase tags: [MVP] = in scope for Day 1 through First Sprint. [Growth] = post-MVP. See Product Scope & Phased Development for detailed phase assignments.*

### Installation & Deployment

- **FR1** [MVP]**:** Developer can install Momentum skills via `npx skills add` into any Agent Skills-adopting IDE
- **FR2** [MVP]**:** Developer can install the full Momentum plugin (skills + hooks + agents + rules) into Claude Code
- **FR3** [MVP]**:** Developer can re-run installation after updates and receive propagated changes
- **FR4** [MVP]**:** Team member can receive project-level Momentum configuration via `git clone` without manual setup
- **FR5** [MVP]**:** Orchestrating agent can detect missing global Momentum components and guide one-time installation

### Orchestrating Agent

- **FR6** [MVP]**:** Developer can interact with an orchestrating agent that presents menu-driven access to all practice workflows
- **FR7** [MVP]**:** Orchestrating agent can show the developer's current position in any workflow via visual status graphics (ASCII)
- **FR8** [MVP]**:** Orchestrating agent can provide human-readable summaries of what was built during implementation, while review runs
- **FR9** [MVP]**:** Orchestrating agent can detect ambiguous or missing project configuration and guide the developer through resolution conversationally
- **FR10** [Growth]**:** Orchestrating agent can contextualize specifications just-in-time — explaining relevant architectural decisions, acceptance criteria, and prior choices at the moment they're needed, rather than requiring document reading
- **FR11** [MVP]**:** Developer can ask follow-up questions during any workflow step; the agent investigates whether the question reveals a specification ambiguity and, if so, proposes a spec update for developer review

### Provenance & Traceability

- **FR12** [MVP]**:** Developer can declare `derives_from` relationships in document frontmatter, tracing each document to its upstream sources
- **FR13a** [MVP]**:** System can detect staleness using hash-based comparison for internal documents: compare `derives_from` content hash to current upstream document hash; flag downstream document as SUSPECT when hash differs
- **FR13b** [MVP]**:** System can detect staleness using time-based comparison for edge documents: compare research document date to domain-specific freshness windows (defined in FR47); flag as SUSPECT when outside the window
- **FR13c** [MVP]**:** System flags stale downstream documents as SUSPECT rather than auto-updating — the SUSPECT status is surfaced to the developer for human review and decision
- **FR13d** [MVP]**:** Staleness propagation is one-hop only: when an upstream document changes, only its direct dependents are flagged SUSPECT; further propagation requires human/verifier decision at each level
- **FR14** [MVP]**:** System can auto-generate backward references (`referenced_by`) from forward `derives_from` declarations — no manual maintenance of backward links
- **FR15** [MVP]**:** Top-level specification documents can self-identify via frontmatter marker, enabling the system to discover the specification tree for any project
- **FR16** [MVP]**:** Developer can track provenance status of claims (VERIFIED, CITED, INFERRED, UNGROUNDED, SUSPECT)
- **FR17** [MVP]**:** System can distinguish human-authored from AI-generated content in provenance metadata

### Enforcement & Quality Governance

*(Implementation notes: FR18, FR19, FR20, FR21 are implemented via Claude Code hooks in the full enforcement tier — the hook type is specified as implementation guidance, not a requirement constraint. These FRs must remain satisfied at the advisory tier without hooks in non-Claude Code environments.)*

- **FR18** [MVP]**:** System can auto-lint and auto-format code on every file edit
- **FR19** [MVP]**:** System can block modifications to acceptance test directories
- **FR20** [MVP]**:** System can run conditional quality gates before session end — tests only when code was modified, lint always
- **FR21** [MVP]**:** System can protect specified files from modification
- **FR22** [MVP]**:** System can ensure authority hierarchy rules auto-load in every Claude Code session including subagents — no manual loading required
- **FR23a** [MVP]**:** Developer can configure model routing defaults per skill and agent via `model:` and `effort:` frontmatter fields
- **FR23b** [MVP]**:** System ships with a documented default model routing strategy: Sonnet-class models at medium effort for general tasks; upgrade to Opus-class for complex reasoning, orchestration, or outputs without automated validation (cognitive hazard rule: invisible errors from cheaper models cost more than the flagship premium); downgrade to Haiku-class for well-constrained tasks with downstream validation

### Verification & Review

- **FR24** [MVP]**:** Code-reviewer subagent can perform adversarial review with read-only tools, producing structured findings reports
- **FR25** [MVP]**:** Code-reviewer can be prompted or triggered automatically at implementation completion, not requiring manual invocation
- **FR26** [MVP]**:** Findings reports can include provenance status for traceability-dimension findings
- **FR27** [MVP]**:** Every finding requires evidence — validators cannot generate findings without supporting evidence from the reviewed artifact (calibration principle)

### Evaluation Flywheel

- **FR28** [MVP]**:** Findings ledger can accumulate findings across stories with category, root cause classification, and upstream level
- **FR29** [MVP]**:** System can detect cross-story patterns in the findings ledger and surface systemic issues — pattern detection triggers when the same finding category appears in 3 or more distinct stories (e.g., findings in stories S-04, S-07, and S-11 as illustrated in Journey 2)
- **FR30** [MVP]**:** Flywheel can explain detected issues to the developer and suggest upstream trace with visual workflow status (detection → review → upstream trace → solution → verify)
- **FR31** [MVP]**:** Developer can approve or reject each flywheel suggestion — the agent never proceeds without explicit consent
- **FR32** [MVP]**:** Upstream fixes can be applied at any level: spec-generating workflow, specification, CLAUDE.md/rules, tooling, or one-off code fix
- **FR33** [MVP]**:** System can track the ratio of upstream fixes to code-level fixes as a practice health metric

### Protocol-Based Integration

- **FR34** [MVP]**:** Developer can configure which agent, skill, tool, MCP provider, or document structure satisfies each protocol — at project level
- **FR35** [MVP]**:** Project configuration file maps protocols to implementations with provenance (who configured, when, why)
- **FR36** [MVP]**:** Orchestrating agent can read the project configuration, detect gaps in protocol mappings, and help fill them conversationally
- **FR37** [MVP]**:** System can resolve workflow step invocations through protocol interfaces — workflow definitions reference protocol types, not specific implementations; the runtime resolves the binding from project configuration
- **FR38** [MVP]**:** Developer can substitute any protocol implementation without modifying the workflows that depend on it

### Specification & Development Workflow

- **FR39** [MVP]**:** Developer can define acceptance criteria in Gherkin format that is behavioral, technology-agnostic, and implementation-independent
- **FR40** [MVP]**:** ATDD workflow can generate failing acceptance tests from Gherkin criteria before implementation begins
- **FR41** [MVP]**:** Developer can complete a full story cycle guided by the orchestrating agent: spec review → ATDD → implement → review → flywheel
- **FR42** [MVP]**:** System can track visual progress through the story cycle, always showing current phase and next phase
- **FR43** [MVP]**:** Developer can invoke the upstream fix skill to analyze a quality failure and propose corrections at the appropriate upstream level

### Research & Knowledge Management

- **FR44** [Growth]**:** Developer can conduct multi-model research using MCP-integrated LLM providers (Gemini, GPT, and additional providers)
- **FR45** [Growth]**:** System can enforce date-anchoring and primary-source directives in research agent prompts — research prompts missing a date anchor constraint or primary-source preference directive are flagged before execution
- **FR46** [MVP]**:** Developer can archive outdated documents to a designated directory while preserving their reference chain
- **FR47** [MVP]**:** System can track document freshness using domain-specific freshness windows (90 days for AI/LLM, 6 months for tooling, 12 months for standards, 24 months for principles)

## Non-Functional Requirements

*Phase tags: [MVP] = required at launch. [Growth] = post-MVP quality bar.*

### Context Window & Token Economics

- **NFR1** [MVP]**:** Each Momentum skill description must be ≤100 tokens to minimize startup context budget impact
- **NFR2** [MVP]**:** Skill matching accuracy must remain >=95% (correct skill invoked on first attempt) when Momentum skills are added to an environment with 68+ existing BMAD skills, as measured by manual spot-checks during dogfooding
- **NFR3** [MVP]**:** Skill instructions should stay under 500 lines / 5000 tokens per the Agent Skills spec recommendation
- **NFR4** [MVP — blocking]**:** Architecture must determine whether plugin-namespaced skills count against the flat skill context budget and design the packaging strategy accordingly — this is a blocking architecture decision that gates plugin vs flat skill deployment choice. *(See Post-PRD Actions — this must be resolved before implementation begins.)*

### Portability & Graceful Degradation

- **NFR5** [MVP]**:** All SKILL.md files must be valid Agent Skills standard — parseable by any of the 17+ adopting tools
- **NFR6** [MVP]**:** Claude Code-specific frontmatter (`context: fork`, `model`, `effort`) must be additive — skills must function correctly when these fields are ignored by non-Claude Code tools
- **NFR7** [MVP]**:** Enforcement must degrade across three defined tiers: Tier 1 full deterministic (Claude Code with plugin — hooks fire, subagents enforce, rules auto-load), Tier 2 advisory (Cursor/other tools with skills only — skill instructions guide but don't enforce), Tier 3 philosophy only (no tooling — principles documented in README). Each tier must be explicitly tested: Tier 1 via plugin install, Tier 2 via `npx skills add` into a non-Claude Code tool, Tier 3 via documentation review.
- **NFR8** [MVP]**:** No Momentum workflow definition may import or reference a Claude Code-specific API directly. Workflows depend on protocol interfaces; protocol implementations resolve to Claude Code features at runtime. Validated by: every workflow SKILL.md must parse and execute (at advisory level) in at least one non-Claude Code tool.

### Ecosystem Resilience

- **NFR9** [MVP]**:** A breaking change in any single ecosystem dependency (BMAD major version, Claude Code plugin API, Agent Skills spec) must be absorbable by modifying only the packaging/distribution layer (plugin manifest, install scripts, frontmatter), not the practice content (skill instructions, rules, agent definitions). Validated by: practice content files have zero imports of ecosystem-specific APIs.
- **NFR10** [MVP]**:** All ecosystem dependencies (BMAD version, Claude Code plugin API, Agent Skills spec version) must be tracked and reviewed at minimum monthly
- **NFR11** [MVP]**:** The packaging/distribution layer must comprise <=5% of total Momentum files (by count). Replacing the entire packaging mechanism (e.g., migrating from plugin to flat skills or vice versa) must not require changes to any skill instruction, rule, or agent definition file.

### Integration Compatibility

- **NFR12** [MVP]**:** Momentum skills must coexist with BMAD skills in `.claude/skills/` without namespace conflicts or matching interference
- **NFR13** [MVP]**:** Momentum hooks must merge cleanly with existing project hooks and BMAD hooks — no silent override. Validated by: install Momentum alongside an existing project hook configuration and verify both hook sets fire without conflict.
- **NFR14** [Growth]**:** MCP provider integrations must respect Cursor's ~40 active tool ceiling when Momentum is used in Cursor environments
- **NFR15** [MVP]**:** Protocol implementations must satisfy documented interface contracts. Validated by: substituting any protocol implementation with a different one that satisfies the same contract must not cause any consuming workflow to fail or produce different structural output.

### Dogfooding Integrity

- **NFR16** [MVP]**:** Every Momentum feature must be validated by real use on at least one active project before being considered stable. Synthetic unit tests are supplementary, not primary validation. Validated by: each feature's release notes reference the project(s) and story cycle(s) where it was dogfooded.
- **NFR17** [MVP]**:** The meta-risk (system amplifying its own blind spots via dogfooding) must be mitigated by external validation: adversarial review by separate context, multi-model research cross-checking, and explicit human checkpoints at critical decisions

## Post-PRD Actions

- Create/update project README to document the eight core principles
- Commit LICENSE as the first artifact in the Momentum repository
- **[Blocking]** Resolve NFR4: architecture document must determine whether plugin-namespaced skills count against the flat skill context budget before implementation begins. This decision gates the plugin vs flat skill deployment choice.
