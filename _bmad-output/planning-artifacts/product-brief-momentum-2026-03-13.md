---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments:
  - docs/research/AI-Solo-Dev-Consolidated-Research-2026-03-07-final.md
  - docs/research/AI Solo Dev Workflow Optimization Report.md
  - docs/research/AI Engineering Maturity and Adoption.md
  - docs/research/technical-agentic-architecture-bmad-vs-claude-code-2026-03-07.md
  - docs/research/technical-claude-code-tool-permissions-research-2026-03-07.md
  - docs/research/technical-subagent-permissions-reference-2026-03-07.md
  - docs/research/preliminary-findings-momentum-as-skills-2026-03-13.md
  - docs/research/technical-acp-agent-client-protocol-2026-03-13.md
  - docs/planning-artifacts/AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md
  - docs/process/process-backlog.md
  - docs/implementation-artifacts/tech-spec-global-practice-layer.md
  - docs/analyst-handoff-prompt.md
  - docs/research/handoff-product-brief-2026-03-14.md
date: 2026-03-13
author: Steve
---

# Product Brief: Momentum

## Executive Summary

Momentum is an open-source practice framework for agentic engineering — the discipline of directing AI agents to produce production-quality software while maintaining human accountability for architecture, quality, and correctness.

The core insight: AI code generation tools produce more code, not better outcomes. Industry data shows 67.3% of AI-generated PRs are rejected, AI-generated code produces 1.7x more issues per PR, and experienced developers are measurably slower with AI tools while believing they're faster. The problem isn't the tools — it's the absence of a verification architecture, a quality discipline, and a continuous improvement practice around them.

Momentum provides that missing layer. It defines how specifications govern code generation, how quality is enforced when AI writes the code, and how the practice itself improves over time through a compounding flywheel where every upstream fix prevents a class of errors permanently. The principles are tool-agnostic; the current implementation targets Claude Code and BMAD Method, with cross-tool compatibility (including Cursor) as a design consideration for team adoption.

The framework scales from a solo developer doing everything to teams where roles are distributed across specialists. It is designed for the realistic case — one person wearing every hat — while considering what's best handled by the same person versus split across roles when a team is available.

---

## Core Vision

### Problem Statement

The promise of AI-assisted development is throughput: write code faster, ship features sooner. The reality, documented across multiple independent studies, tells a different story:

- **67.3% of AI-generated PRs are rejected** vs 15.6% for human code (LinearB, 8.1M PRs, 4,800 teams)
- AI-generated code produces **1.7x more issues per PR** — logic errors 1.75x more frequent, security vulnerabilities 1.57x, performance issues 8x (CodeRabbit, Dec 2025)
- AI increases PR volume by **+98%** but review time increases **+91%**, and organizational delivery metrics remain **flat** (DORA 2025)
- Anti-patterns appear in **80-100% of AI-generated projects** (Ox Security, 300+ repositories)
- Experienced developers are **19% slower** with AI tools in controlled trials, while believing they're 20% faster — a **39-point perception gap** (METR, 2025)

The conclusion is not that AI tools are bad. The conclusion is that using AI without a verification architecture produces more code, not better outcomes. Speed without quality assurance is speed toward a wall.

### Problem Impact

AI-augmented development without practice governance creates four formally identified debt types that compound and interact:

- **Verification Debt** — AI output accepted without sufficient review accumulates faster than human-written code because generation is cheap. 96% of developers don't fully trust AI code, yet 48% skip verification. Unverified outputs become inputs to downstream workflows, creating cascading errors.
- **Cognitive Debt** — AI generates code 5-7x faster than developers can understand it. When you can't explain the code, you can't safely change it. For a solo developer, cognitive debt is existential — there is no team to distribute understanding across.
- **Pattern Drift** — AI reproduces and amplifies patterns it finds in context. One suboptimal pattern becomes convention, then proliferates. Self-reinforcing and invisible until correction becomes prohibitively expensive.
- **Technical Debt** — Compounds exponentially with AI: code duplication rises, refactoring collapses, and code churn doubles. The predicted trajectory is Euphoria → Plateau → Decline → The Wall — the inevitable outcome of speed without quality governance.

Left unaddressed, these debts interact: verification debt feeds cognitive debt (unreviewed code you don't understand), cognitive debt enables pattern drift (you can't spot what you don't comprehend), and pattern drift accelerates technical debt (bad patterns replicate at AI speed). The compounding is not linear — it's systemic.

### Why Existing Solutions Fall Short

The agentic engineering space has produced valuable reference implementations, but each addresses only part of the problem:

- **StrongDM's Software Factory** treats specification as the entire product and code as disposable — philosophically aligned, but their "no human review" stance is inappropriate outside a large, mature organization. Their discovery of test gaming is critical but their solution (blind holdout scenarios) is narrow.
- **The Karviha approach** (350k+ LOC solo with Claude Code) demonstrates subagent review, custom skills, and iterative CLAUDE.md refinement — but lacks formal flywheel discipline. Improvements happen organically rather than through structured upstream trace.
- **Kent Beck's TDD-as-superpower** is powerful but insufficient alone — TDD catches behavioral errors but not architectural drift, cognitive debt, or the systemic patterns that emerge across stories.
- **Tool-specific solutions** (Cursor rules, Claude Code CLAUDE.md, Windsurf rules) provide context engineering but no verification architecture, no continuous improvement loop, and no cross-tool portability.

No existing approach combines specification authority, layered verification, producer-verifier separation, a continuous improvement flywheel, cross-tool compatibility, and adaptation from solo to team workflows into a cohesive practice.

### Proposed Solution

Momentum provides the practice layer through a small set of composable principles:

1. **Spec-Driven Development** — Specifications are the primary engineering artifact. Human-written acceptance criteria define correctness. Code is a generated, verified output — disposable and replaceable.

2. **Authority Hierarchy** — Specifications > Tests > Code. Agents never modify specifications or pre-existing tests to make code pass. If a test fails, the code is wrong.

3. **Producer-Verifier Separation** — The agent that writes code does not review it. Verification happens in a separate context with a separate agent whose only job is to find problems.

4. **Evaluation Flywheel** — When output fails quality standards, trace the failure upstream. Don't fix the code — fix the workflow, specification, or rule that caused the defect. Every upstream fix prevents a class of errors permanently.

5. **Three Tiers of Enforcement** — Deterministic (hooks, linters, tests that always execute), Structured (workflow steps that enforce standards during execution), and Advisory (rules loaded into agent context). Push enforcement as high up the tiers as possible.

6. **Cost as a Managed Dimension** — Model selection, effort levels, and retry loop economics are engineering decisions, not afterthoughts. The cognitive hazard rule: for outputs without automated validation, use flagship models because invisible errors cost more than the price premium.

7. **Impermanence Principle** — Processes and tooling that grow and improve are better than those that stay unchanged. Research has a short half-life. The practice itself must evolve.

The system is designed to work for a solo developer doing everything — analyst, architect, PM, dev, QA, reviewer — while structuring roles so they can be distributed across a team when one is available. Momentum considers what must be global to a workstation, what is local to a project, what is configured per individual, and what is shared across a team.

### Key Differentiators

- **Upstream fix discipline** — Most quality approaches fix symptoms. Momentum's flywheel traces every failure to its root cause in the workflow, specification, or rule that produced it. Fix the process, not the defect. Each upstream fix prevents an entire class of errors permanently, creating compounding improvement where the system gets better every sprint.

- **Tool-agnostic principles, tool-optimized implementation** — The philosophy works regardless of AI coding tool. The current implementation targets Claude Code and BMAD Method, with cross-tool compatibility (including Cursor) as a design goal. Open standards enable adoption across environments while each environment gets optimized configuration.

- **Solo-to-team scaling** — Designed for one person wearing every hat, with explicit consideration of what's best handled by the same person versus what benefits from role separation. The practice adapts rather than prescribing a fixed team structure.

- **Eat-your-own-dogfood evolution** — Momentum's MVP is a working install. From there, the system iterates using its own principles — finding what works, discarding what doesn't, adapting as the philosophy demands. The practice is its own first test case.

- **Open source with cross-environment reach** — Available for adoption and adaptation by others, with licensing that supports both individual practitioners and teams using diverse tooling (Claude Code, Cursor, and future agentic environments).

---

## Target Users

### Primary Users

#### The Side-Project Builder (Solo Developer)

A developer passionate enough to build on their own time — working on a labor of love, whether an open-source project or an app they've always wanted to create. They are not the typical developer; they go the extra mile because they care about what they're building. Their defining constraint is time and resources — they have extremely limited hours and need to maximize every one of them.

They've adopted AI coding tools and experienced the initial thrill of speed, but they've also hit the wall: code that looks right but isn't, patterns that drift without anyone noticing, and the creeping sense that they're building faster but not building better. They're looking for a system that lets them move fast *without* creating a codebase they'll regret in six months.

**Motivations:** Maximize production given extremely limited resources. Build something real, not just a prototype that collapses under its own weight. Maintain the joy of building by keeping the codebase comprehensible and the practice sustainable.

**Current Pain:** Speed without quality governance. No peer review safety net. AI output they can't fully verify alone. Growing unease about accumulating debt they can't see yet.

**Success Vision:** A practice that compounds — each session builds on the last, the system gets smarter about their project over time, and they can trust that what's being produced meets a standard they'd be proud of.

#### The New-to-AI Team Member (Team Developer)

A developer on a small team (4-5 people) of varying experience and skill levels, typically very new or brand new to generative AI for development. They're eager to use AI tools but don't know what they don't know — ready to start cowboy coding and creating debt without realizing it. Their immediate pain point isn't quality (they haven't experienced the consequences yet) — it's being lost.

They're trying to follow documentation about how to go about any particular task, struggling with the gap between "here are the docs" and "here's what I actually need to do right now." They need guidance, not just reference material.

**Motivations:** Get productive with AI tools quickly. Stop feeling lost. Have a clear process to follow without needing to internalize an entire methodology first.

**Current Pain:** Overwhelmed by documentation. No clear path from "I have a task" to "I'm doing it correctly." Unaware of the quality risks they're creating. Following whatever patterns the AI suggests without a framework for evaluating them.

**Success Vision:** An orchestrating agent that meets them where they are, understands what they're trying to accomplish, and guides them through the process conversationally — replacing "read this document" with "let's work through this together."

### Secondary Users

#### The Open-Source Adopter

A developer or team lead who discovers Momentum through GitHub, community discussion, or word of mouth. They're already experiencing the problems Momentum addresses — AI-generated quality issues, lack of verification discipline, or process chaos — and are looking for a structured approach they can adapt to their own environment and tooling (Claude Code, Cursor, or other agentic tools).

They may adopt Momentum wholesale or cherry-pick specific principles (the authority hierarchy, the flywheel, the enforcement tiers) to integrate into their existing workflow. Their primary need is that the framework is well-documented, adaptable, and licensed for their use case.

### User Journey

**Discovery:** For the solo builder, discovery is organic — they're already in the agentic engineering space, hitting quality walls, and searching for better patterns. For the team member, discovery is top-down — a team lead or senior developer introduces Momentum as "how we work with AI tools here."

**Onboarding:** The first thing that changes is they have an **orchestrating agent** helping them through the process. Instead of reading documentation to figure out what to do, they talk to the agent. The agent understands where they are, what they're trying to accomplish, and guides them step by step. For the team member especially, this replaces the painful "follow the docs" experience with a conversational partner.

**First Impressions:** Initial skepticism is natural — "this is just another process framework." Skepticism likely persists until code is actually generated. But as they interact with the orchestrating agent through discovery, specification, and planning, they start seeing what the system can figure out on its own, how it incorporates their feedback, and the quality of the documents produced. The gap between "reading docs" and "having a conversation that produces real artifacts" is the first value signal.

**The Aha Moment:** Different for each persona:
- **Solo builder:** The first time the flywheel catches something — a code review finding that traces back to a workflow gap, gets fixed upstream, and prevents a class of errors they would have hit again and again. The system got smarter without them having to think about it.
- **Team member:** The first time they complete a full cycle (spec → implement → review) with agent guidance and realize the output is better than what they would have produced cowboy-coding. The practice didn't slow them down — it gave them confidence.

**Long-term Value:** The practice compounds. Each sprint's learnings improve the next. The rules, workflows, and agent instructions get more refined. The developer stops fighting quality and starts trusting the system — not blindly, but because they can see the improvement trajectory. For teams, Momentum becomes "how we work" rather than "a tool we use."

---

## Success Metrics

### Practice Effectiveness (The System Is Learning)

These metrics measure whether Momentum's core flywheel is turning — the practice should get better over time, not just run consistently:

- **Upstream fixes per sprint** start high and decrease over time — the system is learning and preventing classes of errors permanently
- **Code review Critical findings** decrease across sprints — upstream fixes are preventing recurrence
- **Test coverage** increases without manual effort — TEA integration and layered verification are working
- **Pattern drift incidents** decrease — architecture guard rules and conventions are effective
- **Time spent reviewing** decreases as a proportion of total work — layered verification catches issues before human review
- **The developer can explain every architectural decision** in the codebase — cognitive debt is controlled

**Failure signals (the practice is broken if):**
- The same class of error recurs across stories (flywheel not turning)
- CLAUDE.md and quality rules are not being updated (upstream fix discipline lapsed)
- The developer accepts AI output without understanding it (cognitive debt accumulating)
- "Just fix the code" becomes the default response to quality failures (downstream patching)

### Adoption Success

#### Solo Developer (Steve)

Success is sustained use and continuous iteration. The solo builder keeps working on Momentum and keeps improving it — not because it's perfect, but because it's working and getting better. Given that BMAD is the closest alternative and Momentum builds on it rather than competing with it, the bar is: does the practice produce better outcomes than working without it, and does it keep compounding?

- **Installs and runs** on a fresh workstation — the MVP gate
- **Provenance tracking works from day one** — the system tracks where artifacts, decisions, and generated outputs come from and what depends on them. This is the highest-priority capability at install time.
- **The developer keeps iterating** — sustained engagement is the strongest signal that the system is earning its place in the workflow

#### Team Developer

Success is that team members stop being lost and start being productive. The measure is behavioral, not attitudinal:

- **Team members report positively** about the experience — they feel guided, not confused
- **Team members don't act lost** — they know where they are in the process and what to do next, because the orchestrating agent is doing its job
- **Team members complete entire stories** through the full cycle (spec → implement → review) with agent guidance
- **A complex set of stories is finished to completion** — not just individual tasks, but a cohesive body of work that demonstrates the practice works end-to-end for the team

### Cross-Tool Portability

Momentum must work across environments — currently Claude Code and Cursor — while being optimized for each tool's strengths:

- **The principles and instructions are shared** — 80% or higher commonality across toolsets. The philosophy, authority hierarchy, workflow steps, and quality standards don't change between tools.
- **The implementation layer adapts** — metadata, hooks, deployment model, and tool-specific configuration are optimized per environment. What changes is how enforcement is wired up, not what is enforced.
- **The system can be optimized for a different toolset and deployment model** without forking the core practice. Success is demonstrating this with the Cursor adaptation for the company team.

### Business Objectives

Momentum is not a commercial product — it is a practice system that happens to be open source. Business objectives are measured in terms of adoption, impact, and sustainability rather than revenue:

- **Personal productivity** — the solo developer ships higher-quality output with sustained or increased throughput, without accumulating the four debt types
- **Team enablement** — the company team adopts agentic engineering practices that would have taken months to develop organically, accelerated by Momentum's structured guidance
- **Open-source viability** — the project is documented, licensed, and structured well enough that an external adopter can install, configure, and get value without direct support from the creator

---

## MVP Scope

### Core Features

**Day 1: Standard Skill Installation**

The MVP is the ability to install Momentum as standard Agent Skills — `SKILL.md` files with YAML frontmatter, installed via `npx skills` or whatever the current standard package manager is. No custom shell scripts, no proprietary installers. Following the official Agent Skills specification gets cross-IDE compatibility as a side effect. Even if the initial skills are minimal, the deployment pipeline follows the standard. BMAD is already converting to skills-based architecture; Momentum follows the same direction.

- Skills install via standard mechanism into the Claude Code environment
- Hook infrastructure is wired and functional
- Rules and agents deploy to the right locations
- The install is repeatable — run it again after updates and changes propagate

**After install, iterate by priority:**

**Foundational (the system doesn't work without these):**

1. **Provenance tracking** — Bidirectional reference traceability so every artifact, decision, and generated output tracks where it came from and what depends on it. This is the highest-priority capability. Without it, obsolete decisions keep resurfacing (as demonstrated by `momentum install` appearing in content long after research showed it was superseded). The system must know what depends on what so changes propagate and stale information gets flagged.

2. **Git integration as infrastructure** — Frequent commits must be part of every development effort, not an afterthought. Git is not just version control — it's the system's memory. The ability to review past document changes, trace when decisions were made, and understand what changed between versions is foundational to provenance, the flywheel, and cognitive debt prevention.

3. **Hook infrastructure** — PostToolUse auto-lint/format, PreToolUse acceptance test directory protection, PreToolUse file protection, Stop hook conditional test/lint gate. These are the Tier 1 deterministic enforcement that can't be forgotten or deprioritized.

4. **CLAUDE.md and rules architecture** — Authority hierarchy, @import project-context.md, modular `.claude/rules/` files. The advisory layer that's always present.

5. **Adversarial sub-agents** — Code-reviewer (read-only, pure verifier), architecture-guard (pattern drift detection). The verification layer.

6. **Visual progress tracking** — ASCII art or visual status indicators at agent load, when planning begins, after each step, and at end of each instruction set. One of the biggest problems with AI-assisted work is not knowing where you are. Every phase of work should show a clear visual of current position in the overall process.

**High priority (first sprint, between stories):**
- Quality rules file for review workflows
- Gherkin-based universal ATDD specification format (technology-agnostic acceptance criteria that can be implemented by BMAD TEA, Playwright, Cypress, or any other framework)
- BMAD Code Review enforcement of pure verifier role
- Upstream fix discipline
- Model routing strategy with default frontmatter
- Stop hook quality gate with conditional logic

### BMAD Relationship

BMAD is the development framework used to build Momentum. Use it wherever it works well, but expect to wrap or replace constantly with more Claude Code-optimized skills, or even project-optimized skills. BMAD is changing fast — the skills-based architecture conversion is underway — so the relationship is collaborative, not dependent. Momentum skills can work with or without BMAD installed.

For testing specifically: BMAD TEA is one ATDD implementation, not the only one. Gherkin provides a universal specification format that any testing technology can implement. **Acceptance tests must describe general behavior, not specific implementation — specificity is the killer of Gherkin value.** The Gherkin specs say *what* the system does from the user's perspective; the test implementation decides *how* to verify it technically. This keeps acceptance criteria technology-agnostic and reusable across frameworks. BMAD TEA may work for some cases and not others. The acceptance criteria (Gherkin specs) are the authority; the test implementation is the generated, replaceable artifact — applying the same authority hierarchy to the test layer itself.

### Out of Scope for MVP

Everything is in scope *eventually*. The question is sequencing:

- Pipeline orchestrator (full spec-to-code single-command execution)
- Benchmarking harness (promptfoo, bash benchmarking, golden datasets)
- Property-based testing and mutation testing
- **Cursor adaptation and cross-IDE deployment** — planning for portability is smart (Impermanence Principle), and following Agent Skills standards gets us most of the way there. But actively building Cursor-specific deployment is not the current job. Claude Code optimized.
- Team scaling, role distribution, and multi-developer workflow
- Architectural fitness tests
- Hybrid research workflow automation
- Open-source packaging and licensing for external adopters

### MVP Success Criteria

- **Standard skill installation completes** and the environment is functional
- **Provenance is tracked** — artifacts reference their sources, dependencies are visible, stale information gets flagged
- **Git integration works** — frequent commits are part of the workflow, document history is reviewable
- **Hooks fire correctly** — lint on edit, test protection on acceptance tests, quality gate on stop
- **Visual progress is always visible** — the user always knows where they are in the process
- **First story cycle completes** with the full practice: spec → Gherkin ATDD → implement → review → flywheel

### Future Vision

Momentum's trajectory follows three conceptual phases, each building on the last:

**Phase 1 — Deterministic Foundation:** Standard skill installation, provenance tracking, git integration, hook enforcement, rules architecture, adversarial sub-agents, visual progress tracking. The practice becomes real — deterministic enforcement that can't be forgotten.

**Phase 2 — Integration and Iteration:** Quality rules, Gherkin-based ATDD with pluggable implementations, pure verifier enforcement, automated flywheel with findings ledger, CLAUDE.md generation from architecture docs. The practice becomes self-improving. BMAD workflows are wrapped or replaced as needed with Claude Code-optimized skills.

**Phase 3 — Scale and Portability:** Pipeline orchestration, model routing with benchmarking validation, property-based testing, architectural fitness tests, cross-tool portability (Cursor and beyond), and team workflow support. The practice becomes a platform.

The Impermanence Principle governs all of this: priorities will shift as we learn from using the system. What matters is that each iteration is informed by the last — eating our own dogfood.
