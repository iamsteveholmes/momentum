# Solo Agentic Engineering: Process, Philosophy, and Implementation Plan

**Date:** 2026-03-07
**Based on:** AI-Solo-Dev-Consolidated-Research-2026-03-07-final.md
**Context:** Expanding an existing BMAD V6 development process into a complete Agentic Engineering practice for a solo developer.

---

## 1. What This Document Is

### 1.1 The Practice in One Paragraph

I practice **Agentic Engineering** using **Spec-Driven Development** governed by the **BMAD Method V6**. Specifications are the primary engineering artifact — human-written acceptance criteria define correctness, and code is a generated, verified output. Quality is enforced through **three tiers** — deterministic hooks, structured BMAD workflows, and advisory CLAUDE.md rules — and **layered verification**: immutable ATDD acceptance tests, dev-authored TDD tests, adversarial sub-agent review implementing the **Producer-Verifier** pattern, formal BMAD code review, and strategic human review. The system is governed by the **Authority Hierarchy** (specifications > tests > code) — agents may never modify existing tests or specifications to make code pass. When AI output fails standards, the agent surfaces the failure to the developer and I apply the **Evaluation Flywheel** — tracing upstream to fix the workflow, specification, or rule rather than patching the code, creating compounding improvement where each upstream fix prevents a class of errors permanently. **Cost is a managed dimension, not an afterthought** — effort level selection is part of every skill and agent definition, the bootstrap workflow sets up cost observability (`/cost`, `ccusage`, OTel), and retry loops are capped at 4-5 iterations because context accumulation makes later iterations progressively more expensive (the validate-fix-loop pattern codifies this). Quality failures are recorded in a **findings ledger** so patterns become visible across stories. The entire system is designed for **adaptability over permanence** — processes and tooling that grow and improve are better than those that stay unchanged, and research is actively managed on a monthly-or-faster cadence to prevent decisions from resting on stale foundations. This actively prevents the four AI-induced debt types: **verification debt** through layered automated verification, **cognitive debt** through spec-first development and the "explain it or reject it" rule, **pattern drift** through persistent architectural guard agents and deterministic lint rules, and **technical debt** through adversarial review and enforced refactoring discipline.

### 1.2 What This Document Adds

This is a development process definition for a solo developer practicing Agentic Engineering — the discipline of orchestrating AI agents to produce production-quality software while maintaining absolute human accountability for architecture, quality, and correctness.

The process builds on an existing BMAD V6 foundation. BMAD already provides the spec-driven pipeline (Brief -> PRD -> Architecture -> Epics -> Stories -> Dev -> Review). What BMAD does not yet provide — and what this document defines — is:

- A **philosophy for managing AI-generated output quality** that goes beyond "review the code"
- A **continuous improvement practice** where every quality failure improves the system permanently
- A **verification architecture** informed by documented successes at StrongDM, Anthropic, and in academic research
- **Specific protections** against the four formally identified types of AI-induced debt
- **Integration with Claude Code's native capabilities** to enforce standards deterministically, not just advisorily
- A **research lifecycle** that keeps the entire practice grounded in current knowledge, not stale training data
- A **cost management discipline** where model selection, effort levels, and retry loop caps are codified in agent definitions and validated through benchmarking — treating cost as an engineering dimension alongside quality and speed
- An **adaptability philosophy** for managing framework evolution, customization persistence, and cross-project knowledge sharing

The goal is not Level 4 autonomy for its own sake. The goal is: **high throughput with near-zero tolerance for accumulating technical debt, achieved by treating specifications as the product and code as a verified, generated artifact.**

---

## 2. The Problem: Why "Use AI to Code Faster" Fails

### 2.1 The Quality Data Is Unambiguous

The research paints a consistent picture across multiple independent studies:

- **67.3% of AI-generated PRs are rejected** vs 15.6% for human code (LinearB, 8.1M PRs, 4,800 teams)
- AI-generated code produces **1.7x more issues per PR**, with logic errors 1.75x more frequent, security vulnerabilities 1.57x, and performance issues 8x (CodeRabbit, Dec 2025)
- AI increases PR volume by **+98%** but review time increases **+91%**, and organizational delivery metrics remain **flat** (DORA 2025)
- Anti-patterns appear in **80-100% of AI-generated projects** (Ox Security, 300+ repositories)
- Experienced developers are **19% slower** with AI tools in controlled trials, while believing they're 20% faster — a 39-point perception gap (METR, 2025)
- ThoughtWorks calculates a realistic net cycle time improvement of **8-13%**, not the 50% that headlines suggest

The conclusion is not that AI tools are bad. The conclusion is that **using AI without a verification architecture produces more code, not better outcomes.** Speed without quality assurance is speed toward a wall.

### 2.2 Four Formally Named Debt Types

The research has identified four distinct categories of debt that AI-augmented development creates. Each has different visibility, compounding rates, and mitigation strategies. A development process must address all four explicitly.

**Verification Debt** (Werner Vogels, AWS re:Invent, Dec 2025)
When you write code yourself, comprehension comes with the act of creation. When the machine writes it, you must rebuild that comprehension during review. Verification debt accumulates when AI-generated output is accepted without sufficient review. 96% of developers don't fully trust AI code, yet 48% skip verification. The debt compounds because unverified outputs become inputs to downstream workflows, creating cascading errors. For a solo developer with no peer review safety net, this is the most immediate threat.

**Cognitive Debt** (Margaret-Anne Storey, University of Victoria, Feb 2026)
AI generates code 5-7x faster than developers can understand it. Anthropic's own research quantifies a 17% reduction in skill mastery when developers delegate to AI versus using AI for conceptual inquiry. Cognitive debt manifests as: inability to explain design decisions in AI-generated code, systems perceived as "black boxes" by their own developer, and fear of making changes due to unknown consequences. For a solo developer, cognitive debt is existential — there is no team to distribute understanding across. If you lose comprehension of your own codebase, there is no fallback.

**Pattern Drift** (Multiple sources, 2025-2026)
AI reproduces and amplifies patterns it finds in context. When a suboptimal pattern enters the codebase, the AI treats it as a convention and proliferates it. Each instance makes the next more likely. Ox Security documented this as "Bugs Deja-Vu" — AI regenerating identical problematic code repeatedly. Google's DORA report confirmed the amplification: "AI doesn't fix a team; it amplifies what's already there." Pattern drift is self-reinforcing and invisible until correction becomes prohibitively expensive.

**Technical Debt** (Traditional, compounded by AI)
AI-generated technical debt compounds exponentially, not linearly. GitClear's analysis of 153M lines found code duplication rose from 8.3% to 12.3%, refactoring activity collapsed from 25% to under 10%, and code churn nearly doubled. The "Velocity Paradox" predicts a four-phase trajectory: Euphoria (months 1-3), Plateau (4-9), Decline (10-15), and The Wall (16-18) where delivery stalls entirely. This trajectory is the inevitable outcome of speed without quality governance.

### 2.3 The Anti-Patterns AI Produces

Ox Security's analysis of 300+ repositories cataloged the specific anti-patterns that appear in the vast majority of AI-generated code:

- **Comments Everywhere** (90-100%) — Excessive inline comments that increase cognitive load rather than reducing it
- **By-the-Book Fixation** (80-90%) — Textbook patterns applied without context adaptation, ignoring project conventions
- **Avoidance of Refactors** (80-90%) — AI implements what was asked without improving surrounding structure, actively preventing the cleanup that prevents debt
- **Over-Specification** (80-90%) — Extreme edge case handling unlikely to occur, adding complexity without value
- **Bugs Deja-Vu** (80-90%) — Regenerating code instead of creating reusable abstractions; pattern drift in action
- **Return of Monoliths** — Tightly coupled components without refactoring suggestions
- **Vanilla-Style Code** — Ignoring battle-tested libraries in favor of from-scratch implementations

The headline finding: AI-generated code is "highly functional but systematically lacking in architectural judgment." A development process must actively counteract these tendencies.

---

## 3. Reference Implementations: What Success Looks Like

### 3.1 StrongDM and the Attractor Agent: Specification as the Entire Product

StrongDM's "Software Factory" represents the most radical implementation of spec-driven development. Their engineering charter is governed by two absolute rules: **code must not be written by humans, and code must not be reviewed by humans.**

The Attractor Agent — StrongDM's open-source, non-interactive coding agent — perfectly encapsulates this paradigm. The Attractor repository **contains zero lines of traditional code.** It consists solely of three highly detailed Markdown files outlining exact specifications, alongside instructions to feed those specifications into an LLM of choice to generate the functional system. The specification IS the product. Code is a disposable artifact regenerated on demand.

StrongDM discovered two critical lessons through this process:

1. **AI agents "reward hack" traditional unit tests.** They write tautological assertions or modify tests to pass broken implementations. StrongDM's solution: replace unit tests with "scenarios" — end-to-end user stories stored as blind holdout sets entirely outside the agent's view. The coding agent cannot see the validation criteria and therefore cannot game them.

2. **Probabilistic satisfaction over boolean pass/fail.** StrongDM abandoned binary test results in favor of measuring "what percentage of observed execution trajectories across all scenarios likely satisfy users." This acknowledges that AI output quality is a spectrum, not a binary.

**What we take from StrongDM:** The Attractor Agent's approach — specifications as the complete product, with code generated from them — is philosophically identical to what BMAD V6 already does with its Brief -> PRD -> Architecture -> Story pipeline. The lesson is not to adopt StrongDM's "no human review" stance (inappropriate for a solo developer who IS the human), but to treat the upstream specification artifacts as the primary engineering investment and code as their verified output. Additionally, their discovery of test gaming directly informs our Authority Hierarchy principle.

### 3.2 Anthropic Internal: The Self-Sufficient Loop

Anthropic's internal engineering teams demonstrate mature Level 4 practices with Claude Code. Their key patterns:

- **Parallel headless instances:** 5-10 Claude Code sessions running simultaneously across different branches, each with isolated context. The solo developer equivalent of a synthetic engineering team.
- **Self-sufficient loops:** Claude Code generates code, executes tests, analyzes linter output, and patches its own errors before presenting to the human. The agent iterates until tests pass, dramatically reducing human cognitive load.
- **End-of-session documentation:** Upon completing a task, Claude automatically appends learnings, friction points, and required commands to CLAUDE.md. The context evolves with the codebase.
- **Explore-Plan-Code-Commit workflow:** Agents read files, develop explicit plans in markdown, then implement. Never jumping straight to coding.

**What we take from Anthropic:** The self-sufficient loop pattern — where the agent verifies its own work through tests and linters before presenting to the human — maps directly to BMAD's Dev Story workflow with TDD enforcement. The end-of-session documentation update maps to our Evaluation Flywheel. The parallel execution pattern informs how we'll handle concurrent story development.

### 3.3 The Karviha Case Study: Solo Developer at Scale

Dzianis Karviha maintains a 350k+ LOC codebase solo with Claude Code, achieving 2.3x LOC throughput increase and 4.7x test code increase. Key practices:

- **Subagent code review:** After the primary agent implements, independent review sub-agents (backend, frontend, mobile) evaluate in separate context windows to avoid implementation bias. This is a solo developer's substitute for peer review.
- **25+ custom skills** encoding atomic operations (controllers, entities, migrations) that enforce architectural consistency across sessions.
- **CLAUDE.md hierarchies** — project-level, directory-level, and feature-level instruction files creating nested context.
- **Context discipline:** Each task stays within a single context window. Context is cleared between tasks. Never exceeds 60% context window usage.
- **"Regular iteration on CLAUDE.md and skills based on observed failures"** — the Evaluation Flywheel in practice.

**What we take from Karviha:** The subagent review pattern is directly implementable as Claude Code custom agents. The CLAUDE.md iteration practice IS the continuous improvement flywheel applied to context engineering. The 25+ custom skills approach validates BMAD's workflow-driven methodology.

### 3.4 Kent Beck's Augmented Coding: TDD as Superpower

Beck, the creator of Extreme Programming, positions TDD as the "superpower" for AI-assisted development. His framework:

- **Tests function as "executable prompts"** — they specify what the AI should produce in a machine-verifiable format.
- **TCR (Test && Commit || Revert):** After each change, tests run automatically. Pass = auto-commit. Fail = full revert. Forces atomic, provably correct steps. Prevents the "doom loop" of cascading error fixes.
- **Warning signs of AI deviation:** Unnecessary loops, implementing unrequested functionality, and critically — **deleting or disabling tests** ("cheating").
- **Separation of structural vs behavioral changes:** Never mix renaming/extracting (structural) with new functionality (behavioral) in a single commit.

**What we take from Beck:** The TDD enforcement is already built into BMAD's Dev Story workflow. The TCR concept informs our hook-based quality gates. The "cheating" detection (AI modifying tests) informs our Authority Hierarchy rule that pre-existing tests are read-only to the coding agent.

### 3.5 The Evaluation Flywheel: OpenAI, NVIDIA, DSPy

The concept of systematically improving upstream artifacts rather than patching downstream output has been independently documented by multiple organizations:

- **OpenAI's Evaluation Flywheel:** Analyze ~50 failing examples, categorize failure modes, create automated graders, make targeted prompt refinements, measure impact, iterate.
- **NVIDIA's Data Flywheel:** Self-improving loop where data collected from AI interactions continuously refines the system.
- **Stanford's DSPy:** Programmatic prompt optimization using Bayesian and genetic approaches — automatic upstream improvement.

The common principle: **every output failure is a signal about the input system.** Fixing the output is a one-time patch. Fixing the input (specification, template, CLAUDE.md rule, workflow step) prevents an entire class of errors permanently.

---

## 4. Core Principles of the Process

These principles govern every decision in the development workflow. They are derived from the research findings and reference implementations above.

### 4.1 The Authority Hierarchy: Specs > Tests > Code

This is the master principle. Every other principle serves it.

**Specifications** are the law — human-written intent that agents may not modify. **Tests** are verification — pre-existing tests are read-only to coding agents, new tests may be written. **Code** is the mutable reality — generated, verified, and potentially disposable.

This hierarchy was discovered through failure. StrongDM found that coding agents "reward hack" unit tests. PactKit documented Claude Code silently changing test assertions to make failing code pass. When a test breaks, the agent must **stop and report why** — never modify the test.

In the BMAD context: the PRD, Architecture document, and Story acceptance criteria are the specifications. The test suite verifies compliance. The code implements. If there's a conflict, specs win, then tests, then code is regenerated.

**How the test tier gets populated:** The Authority Hierarchy only works if the test tier exists *before* the coding agent runs — otherwise the coding agent writes both the tests and the code, and the "immutable test" concept is meaningless. This is the role of the **TEA ATDD workflow**: it reads the story's acceptance criteria (which are human-written or human-reviewed specifications) and generates failing acceptance tests — API tests and E2E tests — as the TDD red phase. These ATDD-generated tests are the concrete, executable expression of the specification layer.

**Directory separation enforces the boundary.** Acceptance tests (ATDD-generated, immutable) and implementation tests (dev-authored, mutable) live in separate directories — e.g., `tests/acceptance/` vs `tests/unit/` and `tests/integration/`. This separation provides three enforcement mechanisms:

1. **Hook enforcement is trivial.** A PreToolUse hook on Edit/Write checks if the target path is inside the acceptance test directory. If so, the edit is blocked. No naming conventions or file-tracking logic needed — just a path check.
2. **The dev agent gets a dedicated run command.** The acceptance test suite has its own run command (e.g., `npm run test:acceptance`, `./gradlew acceptanceTest`) that the dev agent executes for pass/fail feedback. The natural workflow becomes "run the command, see what fails, write code to fix it" — the agent gets the red-green signal without needing to browse the test source files.
3. **The test runner configuration itself is a boundary.** Different directories, different run commands, different authority levels. The Architecture workflow or project setup decides the directory structure; the TEA ATDD workflow writes into the acceptance directory; the dev agent writes into the implementation test directories.

**The dev agent can run and read acceptance tests, but cannot modify them.** This is a deliberate design choice. Preventing the agent from *reading* acceptance tests would be impractical (the Read tool would need path-based blocking) and counterproductive (understanding what a test expects is normal TDD behavior). The gaming risk is not that the agent reads the test — it's that the agent *modifies* the test to make broken code pass. That's what the hook blocks deterministically. If an ATDD test fails and the dev agent cannot make it pass, the correct action is to halt and report, not to weaken the test.

**Gaming prevention is layered, not single-point:**
- **Structural (Tier 1):** PreToolUse hook blocks Edit/Write on the acceptance test directory
- **Advisory (Tier 3):** CLAUDE.md Authority Hierarchy rule says "never modify pre-existing tests"
- **Detective (Layer 3):** The code-reviewer sub-agent checks git history to confirm no acceptance test files were modified
- **Detective (Layer 4):** BMAD Code Review validates AC implementation against the natural language ACs, not just test passage — catching "letter of the test, not spirit" implementations

The dev agent may write *additional* unit and integration tests in the implementation test directories during its own TDD cycle. These are lower-authority tests — they verify internal design choices, not spec compliance.

### 4.2 The Producer-Verifier Separation

Creation and verification must be structurally isolated. If the verifier shares the same context as the producer, it succumbs to the same automation bias — rubber-stamping flawed logic it helped create.

In practice, this means:
- **The agent that writes code does not review code.** Review happens in a separate context window via sub-agents, a separate Claude Code session, or a competing model.
- **The agent that writes tests does not write the code those tests verify.** Acceptance criteria come from the specification (human-written or BMAD-generated from the PRD). Implementation tests can be AI-generated but must not share context with the implementation.
- **Verification agents cannot modify code.** They are granted read-only tools and produce findings. A separate process (the coding agent or the human) remediates.

Research shows that uncoordinated multi-agent verification can amplify errors by 17x, and gains saturate beyond ~4 agents. The goal is not "more reviewers" but "structurally separated reviewers."

### 4.3 The Evaluation Flywheel: Fix the Workflow, Not the Code

When AI output fails quality standards, the correct response is to trace the failure upstream. But "upstream" goes further than most people think. Specifications are not the top of the chain — they are themselves *outputs* of BMAD workflows. A poorly constructed story is not a one-off spec problem; it's a Create Story workflow problem that will produce poor stories every time it runs. The flywheel must trace failures all the way up to the workflows and agents that generate specifications, not just to the specifications themselves.

The full upstream trace:

1. **Is this a spec-generating workflow gap?** → The story was missing ATDD prerequisites, the acceptance criteria were vague, or the Dev Notes lacked architectural context. This means the Create Story workflow, its template, or the agent running it needs modification. Fix the workflow that produces stories, and every future story improves. This is the most valuable fix — it's upstream of upstream. *(Use BMB to modify the workflow or agent.)*
2. **Is this a specification gap in this particular story?** → The PRD, architecture doc, or story acceptance criteria were incomplete or incorrect for this specific case. Fix the spec. This is valuable but only fixes this instance — ask whether the spec-generating workflow should have caught it (see #1).
3. **Is this a CLAUDE.md / .claude/rules/ gap?** → The AI deviated from a standard that should apply universally. Add the rule so it applies in every future session.
4. **Is this a tooling gap?** → Something that should be enforced deterministically was left advisory. Add a hook, lint rule, or architectural test (Tier 1 enforcement).
5. **Is this a one-off error?** → Fix the code. This is the least valuable fix.

The hierarchy is deliberate. The higher up the chain you fix, the more future errors you prevent:

- Fixing **code** prevents one error, once.
- Fixing a **CLAUDE.md rule** prevents a class of errors across all future sessions.
- Fixing a **workflow** prevents a class of errors across all future executions of that workflow.
- Fixing a **spec-generating workflow** prevents a class of errors across all future specifications and everything downstream of them.

Every upstream fix prevents a class of errors permanently. Every downstream fix is a one-time patch. Over time, the upstream artifacts (workflow templates, agent instructions, CLAUDE.md rules, specifications) become increasingly robust, and the quality of AI output improves automatically — not because the AI got smarter, but because the system it operates in got better.

This is Deming's "fix the process, not the defect" applied to AI-augmented development. The key realization for a BMAD practitioner is that BMAD itself — its workflows, agents, templates, and checklists — is part of the process. When a story arrives at implementation with insufficient context or missing prerequisites, the correct flywheel response is to use BMB (BMAD's self-modification capability) to improve the workflow that generated that story, not just to fix the story.

### 4.4 Three Tiers of Enforcement

Standards are not binary (enforced vs advisory). There are three tiers, each with different reliability characteristics:

**Tier 1: Deterministic (Hooks, Linters, Automated Tests)**
Always execute, regardless of context pressure, session length, or what the AI decides. The agent cannot skip, forget, or deprioritize them. Code formatting, file protection, test passage before commit, security scanning — anything that must *always* be true belongs here. Factory.ai articulates this as: **"Agents write the code; linters write the law."**

**Tier 2: Structured (BMAD Workflow Step Files)**
When a BMAD workflow is running, its step files are not background context — they are the agent's *active task*. The XML/markdown structure (`<step>`, `<action>`, `<check>`, `<critical>`) creates a procedural flow the agent follows because the steps are the work itself, not guidance about the work. This is far more reliable than advisory text. The dev-story's TDD cycle, the code review's adversarial checklist, the PRD's 13 validation dimensions — these are structurally enforced during workflow execution. The limitation: this tier only applies *when a BMAD workflow is running*. Ad-hoc Claude Code sessions, sub-agents, and quick fixes operate without it.

**Tier 3: Advisory-Ambient (CLAUDE.md, .claude/rules/)**
Loaded automatically at every Claude Code session start, including sub-agent contexts. This is the baseline that's always present — but it is advisory. Research shows frontier LLMs can follow ~150-200 instructions with reasonable consistency, with uniform degradation across all instructions as the count increases (not just newer ones). Under context pressure or in long sessions, the AI may deprioritize these instructions. CLAUDE.md should contain only things that would cause mistakes if removed. If Claude already does something correctly without the rule, the rule is wasting tokens and degrading adherence to the rules that matter.

The principle: **push enforcement as high up the tiers as possible.** If something can be a hook, don't make it a CLAUDE.md rule. If something only matters during a specific workflow, keep it in the workflow step files rather than cluttering the always-loaded CLAUDE.md. Reserve CLAUDE.md for the standards that must apply in *every* context — including ad-hoc sessions and sub-agents that will never see a BMAD workflow.

### 4.5 Layered Verification

No single verification mechanism is sufficient. The research converges on a stack. Each layer below specifies not just *what* it does, but *where* it is defined and configured so that nothing is left as an abstract aspiration.

**Layer 1: Deterministic Gates**
Linters, formatters, type checkers, compilation. Fastest, cheapest, most reliable. Catches syntactic and structural violations.

- **What tools:** Project-specific — ESLint, Prettier, Biome, tsc, rustc, pylint, etc. Determined by the tech stack chosen during the BMAD Architecture workflow.
- **Where configured:** The linter/formatter config files live in the project root (e.g., `.eslintrc`, `biome.json`, `tsconfig.json`). These are created during initial project setup or scaffolded by the TEA Framework workflow (`_bmad/tea/workflows/testarch/framework/`).
- **How enforced:** Claude Code hooks in `.claude/settings.json` — specifically `PostToolUse` hooks on Edit/Write that auto-run the formatter and linter after every file change. Also a `Stop` hook that runs the full lint/typecheck before any session can end (see Section 6.1.1). These are Tier 1 enforcement — deterministic, not advisory.
- **Where decided:** The Architecture workflow (`_bmad/bmm/workflows/3-solutioning/create-architecture/`) decides the tech stack and tooling. The `generate-project-context` workflow captures those choices. The hooks are created once as part of Phase 1 implementation (Section 6.1.1).

**Layer 2: Automated Tests**
Unit, integration, property-based, and ATDD acceptance tests. Catches behavioral violations. Human-written acceptance criteria anchor the test suite.

- **ATDD acceptance tests (immutable, spec-derived):** Generated by the TEA ATDD workflow (`_bmad/tea/workflows/testarch/atdd/`) from story acceptance criteria *before* implementation begins. These are the Authority Hierarchy's test tier — read-only to the dev agent, protected by `PreToolUse` hooks (Section 6.1.1).
- **TDD unit/integration tests (dev-authored):** Written by the dev agent during the BMAD Dev Story workflow (`_bmad/bmm/workflows/4-implementation/dev-story/`) as part of the red-green-refactor cycle (step 5). Lower authority than ATDD tests.
- **Post-implementation coverage expansion:** Generated by the TEA Automate workflow (`_bmad/tea/workflows/testarch/automate/`) after Dev Story completes to fill coverage gaps.
- **Property-based tests (Phase 3):** A planned TEA extension (Section 6.3.3) that derives invariants from specifications. Not yet implemented.
- **How enforced:** Tests run as part of the Dev Story workflow (step 7), the Stop hook quality gate (Section 6.2.6), and during both quick and formal review. The BMAD Dev Story step files enforce that tests must pass before tasks can be marked complete (step 8, validation gates).
- **Where decided:** Test framework selection happens during the TEA Framework workflow or the Architecture workflow. Test strategy for a specific story comes from the TEA ATDD workflow's test strategy step (step 3). The Architecture document may specify testing patterns (e.g., "use integration tests for API routes, unit tests for business logic"). The acceptance test directory structure (`tests/acceptance/` separate from `tests/unit/` and `tests/integration/`) is an architectural decision captured in project-context.md and enforced by hooks (see Section 4.1).

**Layer 3: Quick Adversarial Verification**
A Claude Code native sub-agent with read-only tools, invoked at the end of dev-story or on demand. Produces a pass/fail findings summary. Fast and cheap enough to run on every story.

- **Where defined:** `.claude/agents/bmad-review/code-reviewer.md` — already created. Restricted to Read, Glob, Grep, and Bash tools. Cannot modify files (pure verifier).
- **How invoked:** Manually by the developer ("use the code-reviewer agent to review this story"), or potentially automated via a Stop hook or as an added step in the Dev Story workflow. The invocation method is a Phase 2 decision — whether to make it automatic (hook-based) or manual but strongly encouraged (added to the Dev Story completion checklist).
- **What it checks:** Reads the story file for ACs and Dev Notes context, runs the test suite, verifies each AC has implementation evidence, checks ATDD test integrity, scans for Ox Security anti-patterns. Reports findings with file:line references.
- **Standards source:** Inherits CLAUDE.md and `.claude/rules/` automatically (Tier 3). Gets story-specific standards from the story file's Dev Notes section. Does not need BMAD workflow infrastructure.

**Layer 4: Formal Adversarial Review**
The BMAD Code Review workflow, run in a separate terminal/session. Full story lifecycle management with sprint tracking.

- **Where defined:** `_bmad/bmm/workflows/4-implementation/code-review/` — exists today. The workflow's step files (`instructions.xml`) provide Tier 2 structural enforcement of the adversarial review process.
- **How invoked:** Developer opens a new terminal tab, starts a new Claude Code session, and runs the BMAD code-review skill. This gives clean context separation — the reviewer has no implementation bias from the coding session.
- **Required modification:** Remove step 4 option 1 ("Fix them automatically") to enforce pure verifier role. The reviewer produces findings and action items only. Remediation happens in a subsequent Dev Story session (see Section 6.2.5).
- **Standards source:** Loads `project-context.md` explicitly (workflow.yaml reference). Also loads the complete story file including Dev Notes. Gets CLAUDE.md and `.claude/rules/` automatically. Will additionally load quality rules file once created (Section 6.2.1).
- **Where decided:** The code review workflow already exists in BMAD V6. The modifications (pure verifier enforcement, quality rules loading) are Phase 2 tasks.

**Layer 5: Strategic Human Review**
Risk-based, focused on architecture, security, and complex business logic. Not every change needs the same scrutiny — boilerplate gets less, critical paths get more.

- **Where defined:** Not a workflow — this is the developer's own judgment applied after Layers 1-4 have filtered out mechanical issues.
- **When applied:** After the formal adversarial review produces its findings. The developer reads the review, examines the code, and focuses human attention on areas the automated layers cannot assess: "Is this the right architectural approach? Does this business logic match the domain? Are there security implications the AI wouldn't recognize?"
- **How scoped:** The BMAD Architecture document defines which areas are "critical path" (warrant full human review) vs "boilerplate" (Layers 1-4 are sufficient). This scoping decision should be captured during the Architecture workflow and referenced in story Dev Notes so the developer knows which stories demand deep human review.
- **Flywheel connection:** If human review consistently catches the same class of issue, that's a signal to push the check down to a cheaper layer — add a rule to `.claude/rules/`, add an architectural test, or modify a workflow checklist.

Each layer catches what the layers below it miss. The layers are ordered by cost: deterministic gates are nearly free; human review is expensive. The goal is to push as many catches as possible to the cheaper layers.

### 4.6 Where Standards Live: CLAUDE.md, BMAD, and Hooks

A solo developer using BMAD V6 with Claude Code has multiple places to put standards and instructions. Without a clear boundary, the same rules end up duplicated across CLAUDE.md, project-context.md, BMAD workflow steps, and .claude/rules/ — creating maintenance burden and wasting context tokens. This section defines which standards belong where.

**The guiding principle:** Each standard lives in exactly one place, chosen by two criteria: (1) does it need to apply in every Claude Code session, or only during BMAD workflow execution? and (2) can it be enforced mechanically, or does it require advisory guidance?

| Standard | Where It Lives | Why |
|----------|---------------|-----|
| Build, test, lint command *references* | CLAUDE.md | Claude needs to know *what* the commands are for on-demand use (e.g., "run tests for this file"). Hooks handle *automatic* execution. |
| Build, test, lint command *enforcement* | Hooks (Tier 1) | PostToolUse runs linter after edits; Stop hook runs tests before session ends. Deterministic — not reliant on Claude remembering. |
| Authority hierarchy rule (specs > tests > code) | CLAUDE.md | Must apply always, including sub-agents |
| Anti-pattern blacklist (Ox Security catalog) | .claude/rules/ | Must apply always; modular, one file per category |
| Project coding conventions the AI would get wrong | .claude/rules/ | Must apply always; modular |
| Code formatting enforcement | Hooks + linters (Tier 1) | Deterministic, not advisory |
| ATDD test file protection | Hooks (Tier 1) | Deterministic, not advisory |
| Tech stack, versions, framework patterns | project-context.md, @imported by CLAUDE.md | Single source of truth, available everywhere |
| TDD red-green-refactor cycle | BMAD Dev Story step files (Tier 2) | Structural enforcement during workflow execution |
| Adversarial review checklist | BMAD Code Review step files (Tier 2) | Structural enforcement during workflow execution |
| PRD validation dimensions | BMAD PRD Validate step files (Tier 2) | Only relevant during PRD creation/validation |
| Story-specific architecture constraints | Story Dev Notes | Only relevant during that story's implementation |
| ATDD acceptance tests for a story | TEA-generated test files | Only relevant during that story's implementation |

**The project-context.md bridge:** BMAD's `generate-project-context` workflow creates a file containing tech stack, versions, and implementation rules — information that BMAD workflows load explicitly. To avoid duplication, CLAUDE.md should **@import** project-context.md rather than restating its contents. This gives every Claude Code session (including sub-agents and ad-hoc work) access to the same standards, with project-context.md as the single source of truth maintained through the BMAD workflow.

```markdown
# CLAUDE.md (root)
# ... build commands, authority hierarchy, etc.

# Project standards (maintained via BMAD generate-project-context)
@docs/project-context.md
```

**What does NOT go in CLAUDE.md:**
- Code style rules that linters already enforce (use hooks instead — Tier 1)
- Workflow-specific instructions that only matter during BMAD execution (keep in step files — Tier 2)
- Things Claude would do correctly without being told (wasting tokens degrades all other rules)
- Task-specific context (use story Dev Notes or pass directly in the prompt)

**The 150-instruction ceiling:** Research on LLM instruction-following shows that frontier models can attend to ~150-200 instructions with reasonable consistency. Beyond that, adherence degrades *uniformly across all instructions* — not just the new ones. This means bloating CLAUDE.md with rules that belong in hooks or BMAD workflows doesn't just waste tokens; it actively weakens the rules that need to be there.

**Coding standard specificity: reference, correct, or specify.** Not all coding standards need the same level of detail. The LLM's training data is itself a form of standards knowledge — for well-established conventions, restating them wastes instruction budget. Three tiers:

1. **Reference by name** — for well-established standards the LLM already knows. One line in the architecture doc or project CLAUDE.md: "Follow PEP 8," "Use standard Go conventions," "Follow Kotlin coding conventions." Cost: 1 instruction. Training data handles the details.

2. **Correct with examples** — for cases where the LLM has a strong default but it's the *wrong* default for the project. The LLM knows JUnit well, so it gravitates there even when told to use Kotest. These need explicit rules with code examples in project-scoped `.claude/rules/`. Without the example, you correct the same mistake every session. Cost: 5-10 instructions per correction, but necessary.

3. **Specify in architecture** — for project-specific architectural patterns that have no well-known standard. Which layers exist, dependency direction, where business logic lives, error propagation strategy. These belong in the architecture document and are project-specific by definition. Not an exhaustive textbook — just enough that an agent makes the right structural choices.

**This is inherently iterative and flywheel-driven.** You cannot predict in advance which standards need Tier 2 treatment. Start with Tier 1 references. When the code review catches the LLM ignoring or misapplying a standard, promote to Tier 2 with examples. The findings ledger tracks these — three occurrences of "used JUnit instead of Kotest" across stories is a clear signal. Don't pre-load dozens of pages of standards "just in case" — let failures tell you where to be explicit.

**The project boundary is the coding standard boundary.** When two parts of a system need fundamentally different LLM guidance — different languages, different frameworks, different test strategies, different architectural patterns — they should be separate projects. Each project gets lean, focused project-level config: only the rules for *this* stack, *this* framework, *this* test runner. Cramming Python conventions, Kotlin/Compose patterns, and campaign content rules into one project CLAUDE.md burns instruction budget on rules irrelevant to the current task, creates contradiction risk, and makes the flywheel noisy. The global practice layer (`~/.claude/`) carries the universal standards; the project carries only what's specific to its stack. This principle also guides the Momentum bootstrap workflow (Section 8.2) — it asks "what stack is this project?" and scaffolds the right project-level rules accordingly.

### 4.7 The Impermanence Principle: Adaptability Over Permanence

**Processes and tooling that grow, adapt, and improve are better than those that stay unchanged — if you can manage, mitigate, and adapt to the change.** This is the central tension: stability has value, but stagnation is a cost. The goal is not to maximize durability but to put each piece of the system in the right change category.

The evaluation question is not "will this survive an update?" but **"should this change?"**

Two categories:

1. **Things that should rarely change.** A hook that runs a linter. A hook that runs unit tests. The Authority Hierarchy rule. File protection on acceptance tests. These encode fundamental invariants — the *what* doesn't change even when the *how* (underlying tools, frameworks, test runners) changes frequently. Put these in the most stable layer available (Claude Code native infrastructure: hooks, `.claude/rules/`, CLAUDE.md).

2. **Things that should grow and improve.** BMAD agents, workflows, the dev story process, code review steps, research workflows, the Momentum module. These *should* change — they should get better as BMAD evolves, as we learn from experience, and as the AI tooling landscape matures. Freezing them in Claude Code native infrastructure would make them durable but stagnant. Instead, keep them in layers that participate in BMAD's evolution (custom modules, customize files, wrapper workflows) and accept the maintenance cost of adaptation.

The anti-pattern is not change itself — it's **unmanaged change**. Specifically: editing framework files that get silently overwritten on reinstall or update. BMAD provides customize files and the custom module pattern precisely to avoid this. The implementation details — which customization layers to use, how to track framework evolution, how to manage cross-project portability — are in Section 8.

This principle also applies to the research that grounds this plan. Research in fast-moving domains (LLMs, AI tooling, agentic patterns) has a short half-life. The research lifecycle (Section 7.1) and the temporal focus rules (Section 7.1.3) exist because the Impermanence Principle demands it: knowledge that doesn't get refreshed becomes stale context that actively misleads decisions.

---

## 5. The Solo Developer Agentic Engineering Process

This section describes the complete development process, building on the existing BMAD V6 pipeline. BMAD provides the structured workflow; the principles above govern how that workflow operates.

### 5.1 How the Existing BMAD Pipeline Maps to These Principles

| BMAD Phase | Principle Applied | Role in the Process |
|------------|------------------|---------------------|
| Product Brief | Specification as Product | Human defines the problem space and constraints |
| PRD (13 validation dimensions) | Authority Hierarchy | Specification becomes the law; validated against standards |
| Architecture | Authority Hierarchy | Structural constraints that agents must obey |
| Implementation Readiness | Layered Verification | Gate: specs must be complete before code begins |
| Create Story | Context Engineering | Loads all artifacts to prevent context gaps; the "upstream" |
| Dev Story (TDD) | Producer role; Beck's Augmented Coding | Agent produces code within TDD constraints |
| Code Review | Verifier role; Adversarial | Separate adversarial agent evaluates in clean context |
| TEA (Testing) | Layered Verification | Automated test infrastructure across the verification stack |
| Retrospective | Evaluation Flywheel | Learning extraction feeds back into upstream artifacts |
| BMB (Self-modification) | Fix the Workflow | BMAD can modify its own agents, workflows, and modules |

BMAD V6 already implements most of the Producer-Verifier pattern structurally. The human writes specs (Brief, PRD, Architecture), the Dev agent produces code, and the Code Review agent verifies independently. What's missing is the **deterministic enforcement layer** (hooks, linters), the **automated flywheel** (retrospective findings auto-applied), and the **pipeline orchestration** (single-command spec-to-code execution).

### 5.2 The Development Cycle

**For planned work (features, epics, significant changes):**

```
Define Intent (Human)
  |-> Specify (BMAD: Brief -> PRD -> Architecture -> Epics -> Stories)
  |     [Gate: Implementation Readiness Check]
  |-> Verify Acceptance Criteria (Human writes or reviews)
  |-> Generate Acceptance Tests (TEA ATDD: failing tests from criteria)
  |     [Separate agent/session — produces read-only test files]
  |     [Gate: ATDD tests exist and fail before implementation begins]
  |-> Implement (BMAD Dev Story: TDD red-green-refactor against ATDD tests)
  |     [Continuous: deterministic hooks enforce formatting, linting, file protection]
  |     [Constraint: ATDD-generated test files are protected — dev agent cannot modify]
  |-> Verify (Layered: tests pass -> sub-agent review -> human review if critical)
  |     [Gate: all tests pass, no Critical findings in review]
  |-> Learn (BMAD Retrospective -> Flywheel: update CLAUDE.md, quality rules, workflow)
  |-> Deploy
```

The ATDD step is a **Producer-Verifier boundary**: the TEA agent (producer of tests) operates in a separate context from the Dev agent (producer of code). The TEA agent reads specifications and produces tests; the Dev agent reads tests and produces code. Neither modifies the other's primary output. This structural separation is what prevents the test gaming documented at StrongDM and PactKit — the coding agent cannot see or alter the verification criteria.

**For quick fixes (bugs, small changes, ad-hoc work):**

```
Define Intent (Human: describe the fix)
  |-> Implement (Claude Code with CLAUDE.md context, skills, rules)
  |     [Continuous: deterministic hooks enforce standards]
  |-> Verify (tests pass -> sub-agent review)
  |-> Learn (if failure revealed a gap: upstream fix to CLAUDE.md or skill)
```

Both paths use the same enforcement infrastructure (hooks, CLAUDE.md, sub-agents). The difference is ceremony — planned work gets the full BMAD specification pipeline; quick fixes rely on accumulated context engineering.

### 5.3 How This Process Addresses Each Debt Type

**Verification Debt** (unreviewed AI output)
- Every implementation passes through layered verification before acceptance
- Deterministic hooks guarantee that tests run and linters execute — the agent cannot skip them
- Sub-agent review in clean context catches logic gaps without implementation bias
- The human only reviews what survives automated checks, making human review focused and sustainable

**Cognitive Debt** (understanding gap)
- Specifications are human-written or human-reviewed; the developer understands the intent before code exists
- BMAD's story files encode the full context (PRD references, architectural constraints, acceptance criteria) — the "why" is always available alongside the "what"
- The authority hierarchy rule ("if the human cannot explain how the code works, the code must be rejected") makes cognitive debt a gate, not a latent risk
- The model routing guide codifies the cognitive hazard rule: for outputs without automated validation, use flagship models because invisible errors (embedded hallucinations, subtle logic flaws) cost more in human review burden than the model price premium. Derived from cognitive load research in the benchmarking guide (Section 3) — see `module/canonical/resources/model-routing-guide.md` and `module/canonical/rules/model-routing.md`
- ADRs document significant structural choices for future sessions

**Pattern Drift** (AI reproducing/amplifying bad patterns)
- CLAUDE.md and .claude/rules/ encode project conventions that the AI reads at session start
- The architecture-guard sub-agent has persistent memory of discovered patterns and flags deviations
- Architectural tests encode structural rules (dependency direction, module boundaries) as automated checks
- The evaluation flywheel ensures that every discovered drift pattern becomes a permanent rule

**Technical Debt** (compounds exponentially)
- BMAD's code review workflow is explicitly adversarial — it hunts for debt, not just bugs
- The "Avoidance of Refactors" anti-pattern (80-90% of AI code) is counteracted by explicit CLAUDE.md rules encouraging refactoring
- Spec-first development prevents the root cause: building without understanding
- The flywheel converts individual debt discoveries into systemic prevention

### 5.4 How This Process Implements Producer-Verifier

The Producer-Verifier separation is not a single mechanism but a pattern applied at every level:

| Level | Producer | Verifier | Separation Mechanism |
|-------|----------|----------|---------------------|
| **Specification** | Human + BMAD Analyst | BMAD PRD Validate (13 dimensions) | Validation workflow is structurally separate from creation |
| **Architecture** | BMAD Architect agent | Implementation Readiness Check | Gate between solutioning and implementation |
| **Implementation (quick)** | BMAD Dev agent | Claude Code native `code-reviewer` agent | Read-only tools, clean sub-agent context, fast pass/fail gate |
| **Implementation (formal)** | BMAD Dev agent | BMAD Code Review workflow (separate session) | Full adversarial review, story lifecycle, sprint tracking — pure verifier (no code fixes) |
| **Testing** | TEA ATDD (from specs) | Dev agent implements against tests | Tests written from specs, not from implementation |
| **Standards** | Any agent (writes code) | Hooks + linters (verify mechanically) | Deterministic, non-negotiable, no context dependency |
| **Cross-session** | Current session agent | Architecture-guard sub-agent | Persistent memory compares new code against established patterns |

### 5.5 How This Process Implements the Evaluation Flywheel

The flywheel operates at three cadences:

**Per-session (immediate):** When Claude output fails quality standards during a session, the failure should trigger a back-and-forth between the agent and the developer — not silent correction. The agent should surface the failure explicitly: "This output didn't meet [standard]. Is this a gap in CLAUDE.md, a missing rule, or a one-off?" This dialogue prevents knowledge gaps — without it, the developer may not realize a systemic issue occurred, and the same failure recurs in the next session. If the answer is a CLAUDE.md or rules gap, the rule is added immediately in-session. The Karviha case study documents this practice as "regular iteration on CLAUDE.md and skills based on observed failures." The key behavior: the agent communicates the failure to the developer rather than quietly working around it.

**Per-story (sprint cadence):** BMAD code review findings trigger the full upstream trace from Section 4.3. The critical question is not just "what went wrong in this story?" but "what went wrong in the process that produced this story?"

**The findings ledger.** The agent cannot reliably distinguish a one-off bug from a systemic issue in isolation — it lacks cross-story memory. The solution: every code review finding gets appended to a structured findings ledger (`docs/quality/findings-ledger.json` or similar) with fields for: story ID, finding category, description, root cause classification (one-off / unclear / systemic), upstream level, and resolution. Nothing is silently dismissed. The ledger serves two purposes:

1. **Immediate:** Each finding is communicated to the developer with the agent's best assessment of whether it's one-off or systemic, and the developer confirms or reclassifies. This is the same back-and-forth pattern as per-session — the agent surfaces, the developer decides.
2. **Over time:** Patterns become visible even when each individual occurrence looked like a one-off. Three "one-off" auth validation misses across different stories is a systemic issue that no single code review could detect. The retrospective workflow (per-sprint cadence) reads the ledger and groups findings by category to surface these patterns.

Findings are categorized by upstream level:
- **Spec-generating workflow fixes** (highest value) — The Create Story workflow failed to include ATDD prerequisites, the story template is missing a section, or the agent instructions don't enforce loading the architecture doc. Fix via BMB.
- **CLAUDE.md / .claude/rules/ amendments** — A universal standard was missing. Add the rule.
- **Quality rules updates** — Project-specific patterns need codifying.
- **Tooling fixes** — Something advisory should have been deterministic. Add a hook or lint rule.
- **One-off story/code fixes** (lowest value) — Fix this instance only if the ledger confirms no recurrence pattern.

**Per-sprint (retrospective):** BMAD retrospective workflow extracts learnings across all stories in the sprint. The retrospective should explicitly ask: "Did any stories arrive at implementation with missing context, unclear ACs, or absent ATDD tests?" If yes, the Create Story, TEA ATDD, or related workflows are the fix targets — not the individual stories. Retrospective outputs:
- Workflow modifications via BMB (spec-generating workflows, dev workflows, review workflows)
- CLAUDE.md amendments (new rules discovered)
- Quality rules updates (project-specific patterns)
- Definition of Done additions (new checklist items)
- Hook/tooling additions (advisory standards promoted to deterministic enforcement)
- Process tasks added to the process backlog (Section 6.4) with appropriate priority

The flywheel's output is measurable: the number of upstream fixes per sprint, categorized by level. A healthy flywheel shows frequent upstream fixes early (the system is learning) that decrease over time (the system has learned). The most valuable metric is the ratio of workflow-level fixes to code-level fixes — a mature system fixes almost nothing at the code level because the workflows that generate and verify code have been refined to prevent errors before they occur.

---

## 6. Implementation Roadmap

The process above requires specific technical infrastructure. This section defines what to build, organized by conceptual phase (foundation → integration → orchestration). Each item is also assigned a process task priority in the process backlog (`docs/process/process-backlog.json`) based on when it's actually needed relative to product work: **Critical** (4 items — must exist before first product story), **High** (6 items — resolve during first sprint), **Low** (10 items — batch at sprint boundaries or future sprints). The phases describe conceptual dependencies; the backlog priorities drive execution order.

### Phase 1: Deterministic Foundation (Week 1-2)

*Goal: Establish the enforcement layer that operates in every Claude Code session, whether BMAD or ad-hoc.*

**6.1.1 Hook Infrastructure**

| Hook | Purpose | Addresses |
|------|---------|-----------|
| PostToolUse (Edit\|Write) → auto-lint/format | Mechanical enforcement of code style | Pattern Drift, Tech Debt |
| PreToolUse (Edit\|Write) → acceptance test directory protection | Block modifications to any file in the acceptance test directory (path-based check — simple and reliable) | Verification Debt, Authority Hierarchy |
| PreToolUse (Bash) → file protection | Prevent modification of protected files | Verification Debt |
| Stop → conditional test/lint gate | Run tests and lint check before session ends — but only when code was modified | Verification Debt |

**Hook Scoping: Not All Agents Need All Hooks**

BMAD sessions span multiple agent roles — analyst, architect, PM, dev, reviewer — but only the dev agent modifies code. Hooks must not impose code-centric overhead (test runs, lint checks) on sessions that only produce specifications and documents.

Claude Code provides three scoping mechanisms:

1. **Trigger-based scoping (most hooks are naturally scoped).** `PostToolUse` hooks on Edit/Write only fire when files are edited. If the analyst is writing a PRD, the linter hook only fires on the markdown file being edited — which is harmless. No special configuration needed for these hooks; they are inert in non-code sessions.

2. **Conditional Stop hooks (the one that needs logic).** The Stop hook that runs the full test suite before session end would fire for *every* session, including the architect writing an architecture doc. The Stop hook script must check context before executing:
   - Check `git diff --name-only` — if only markdown/docs files were modified, skip test execution
   - Optionally check the `agent_type` field in the hook's JSON input (available when running as a sub-agent via `--agent`, but not in main-thread BMAD sessions)
   - Always run lint/format (fast, harmless on any file type); conditionally run tests (slow, only meaningful for code changes)

3. **Native sub-agent frontmatter hooks (for `.claude/agents/`).** Claude Code sub-agents support hooks defined directly in their YAML frontmatter. These hooks are scoped to the agent's lifecycle — they activate when the agent starts and are cleaned up when it finishes. Use this for agent-specific enforcement:
   - The `code-reviewer` agent could have a hook that prevents any Write/Edit tool calls (defense in depth on top of tool restrictions)
   - The `architecture-guard` agent could have hooks specific to its pattern detection workflow
   - BMAD planning agents (analyst, architect, PM) get no code-enforcement hooks because they don't have frontmatter hooks defined

**6.1.2 CLAUDE.md and Rules Architecture** (see Section 4.6 for the complete standards placement guide)

Root CLAUDE.md: build/test/lint command *references* (so Claude knows what to run on demand — automatic execution is handled by hooks, not CLAUDE.md), authority hierarchy rule, @import of project-context.md (maintained via BMAD's `generate-project-context` workflow). Keep under 50-100 lines plus imports.

`.claude/rules/` directory: modular rule files — one per concern (e.g., `anti-patterns.md`, `testing-philosophy.md`, `security.md`, `architecture.md`). Each addresses specific debt types. These are auto-loaded by Claude Code in every session, so they must contain only standards that apply universally. Workflow-specific instructions stay in BMAD step files (Tier 2), not here.

**6.1.3 Adversarial Sub-Agents** (defined in `.claude/agents/`)

- `code-reviewer`: Read-only tools (Read, Glob, Grep, Bash for test execution only), adversarial persona. Accepts a story file path, reads the story's acceptance criteria, reads all implementation files, verifies each AC has evidence in code, checks that all tests pass, and produces a structured findings report. Cannot modify any files — pure verifier implementing the quick verification layer. This is the Claude Code native complement to the BMAD Code Review workflow; it runs fast and can be invoked from within an active session or automated via hooks.
- `architecture-guard`: Read-only tools, persistent memory. Detects pattern drift across sessions by comparing new code against established conventions in CLAUDE.md and architecture documents.

**6.1.4 Discord MCP Integration** (pending admin approval — externally gated)

Read-only Discord bot + MCP server (`barryyip0625/mcp-discord`) enabling Claude Code to query BMAD Discord channels directly during research workflows. Requires BMAD server admin to authorize the bot — request submitted March 8, 2026, awaiting response. If approved: create bot application, enable Message Content intent, configure MCP server in Claude Code settings. This is foundational infrastructure for BMAD change tracking (Section 8.3) — without it, Discord monitoring is manual-only. Note: this item is externally gated on admin approval and may not complete within the Phase 1 timeline. If not approved, fallback is manual Discord scanning with structured paste-and-process through the analyst.

**6.1.5 Upstream Fix Discipline**

Create the `/upstream-fix` skill that analyzes quality failures and proposes upstream corrections. Begin maintaining a lightweight decision log.

### Phase 2: BMAD Integration (Week 3-4)

*Goal: Bridge BMAD workflows with Claude Code native infrastructure. Close the flywheel loop.*

**6.2.1 Quality Rules File** — Project-specific standards loaded by BMAD review workflows alongside generic analysis.

**6.2.2 CLAUDE.md Generation** — Skill or workflow step that auto-generates `.claude/rules/` content from BMAD Architecture documents and PRD constraints. Ensures planning decisions become enforcement rules. Additionally, ensure CLAUDE.md @imports project-context.md so that tech stack, versions, and implementation conventions maintained through the BMAD `generate-project-context` workflow are automatically available in every Claude Code session — including sub-agents and ad-hoc work — without duplication (see Section 4.6).

**6.2.3 TEA Integration** — This is the mechanical implementation of the Authority Hierarchy's test tier. Two changes:

1. **ATDD as prerequisite gate for Dev Story:** Modify Dev Story workflow so that it checks for the existence of ATDD-generated test files before beginning implementation. If no ATDD tests exist for the story, Dev Story halts and directs the user to run TEA ATDD first. This ensures the immutable test layer is always in place before code generation begins.
2. **TEA Test Automation after implementation:** After Dev Story completes, run TEA Automate to expand coverage (integration tests, edge cases, regression guards). These post-implementation tests are lower-authority — they verify implementation quality, not spec compliance.

The result is a test sandwich: ATDD tests (spec-derived, immutable) bracket the implementation, with the dev agent's own TDD tests and TEA Automate's expansion tests filling in the middle. The ATDD tests are the ones protected by hooks; the rest are mutable.

**Stack coverage note:** TEA is optimized for web fullstack (Playwright/Cypress + API) with backend stack detection. For non-web projects (Kotlin/JVM, Go, etc.), TEA may need extension or the project may use a different test framework entirely — the ATDD *principle* (spec-derived immutable tests before implementation) applies regardless of tooling. For LLM-powered applications, traditional ATDD is insufficient — non-deterministic model output requires fundamentally different verification strategies (eval frameworks, output pattern assertions, statistical pass criteria). LLM testing is a future-phase research topic, not a current deliverable. Process infrastructure tasks (configuration files, agent definitions, workflow specs) are verified through review and mechanical checks, not automated test suites.

**6.2.4 Automated Flywheel** — Wrap the Retrospective workflow (via custom module wrapper, per Section 8.1 Layer C) to integrate the findings ledger, add upstream trace categorization of action items, and produce CLAUDE.md amendments, quality rule updates, and DoD additions as structured outputs. Create `/apply-retro-learnings` skill to apply them.

**6.2.5 BMAD Code Review: Enforce Pure Verifier Role** — The current BMAD Code Review workflow (step 4, option 1) allows the reviewer to "fix them automatically" — modifying code and tests directly. This violates the Producer-Verifier separation: a verifier that also produces code is no longer structurally independent. The fix: remove option 1 ("Fix them automatically") from the code review workflow. The reviewer's only outputs should be findings and action items (current option 2). Remediation happens in a subsequent Dev Story session where the dev agent addresses the review follow-ups — maintaining the structural separation. The reviewer reads; the developer writes. If a finding is trivial enough that "just fix it" feels appropriate, the developer can fix it themselves — but the *review agent* should never be the one making the change.

**6.2.6 Stop Hook Quality Gate** — Enhance the Phase 1 Stop hook (Section 6.1.1) with the conditional logic described in the Hook Scoping subsection: check `git diff` to determine if code was modified, skip test execution for docs-only sessions, and optionally check agent_type for sub-agent invocations. Phase 1 creates the basic hook; Phase 2 makes it context-aware.

### Phase 3: Pipeline Orchestration (Week 5-8)

*Goal: Build the pipeline orchestrator — the "Level 4 unlock" — and advanced verification patterns.*

**6.3.1 Pipeline Orchestrator** — New BMAD workflow (built via BMB) that chains the full pipeline: PRD Validate → Architecture → Implementation Readiness → Sprint Plan → (for each story: ATDD → Dev → Code Review → Test Automation) → Retrospective → Apply Learnings. Human touchpoints only at gates and critical findings.

**6.3.2 Model Routing Strategy** (elevated from Phase 3 to High priority based on benchmarking research, March 2026) — Comprehensive model selection infrastructure producing three artifacts: (1) a model routing guide as canonical module resource (`module/canonical/resources/model-routing-guide.md`) condensing the benchmarking research's task-type mapping and decision matrix, (2) default `model:` and `effort` frontmatter for all momentum agents and skills, and (3) a rule in `.claude/rules/` (`module/canonical/rules/model-routing.md`) about when to override model defaults. Incorporates the cognitive hazard argument: for outputs without automated validation, use flagship models because invisible errors cost more than the price premium. The companion Benchmarking Harness (PT-022) provides the tooling to validate these routing decisions empirically.

**6.3.7 Benchmarking Harness** (new, March 2026) — Build the runnable testing infrastructure for empirical model routing decisions. Five deliverables: (1) promptfoo configuration for BMAD skills using the Claude Agent SDK provider for full agentic workflow testing, (2) bash benchmarking script using `claude -p --model X --output-format json` to capture time/cost/tokens across models, (3) golden dataset starter with 5-10 reference outputs per skill type for promptfoo test cases, (4) Pydantic AI benchmarking harness using `agent.override()` and Pydantic Evals for multi-model comparison, (5) model configuration (`model:`/`effort` frontmatter) for existing skills and agents. Research and methodology are implementation-ready from the multi-model benchmarking guide; this task produces the executable tooling. See `docs/research/multi-model-benchmarking-handoff-2026-03-14.md` for detailed specifications.

**6.3.3 Property-Based Testing** — TEA extension that derives properties and invariants from specifications (not implementation) and generates Hypothesis/fast-check tests. Properties resist gaming because they express what should always be true.

**6.3.4 Architectural Fitness Tests** — Automated tests encoding structural rules (dependency direction, module boundaries, import policies) that catch drift deterministically.

**6.3.5 Mutation Testing (Optional)** — Mutation testing answers "are these tests actually verifying behavior, or are they tautological?" by introducing small code changes (mutations) and checking whether the test suite catches them. This directly addresses the test gaming concern: if the dev agent writes tests that pass but don't assert anything meaningful, mutation testing exposes the gap. The specific tool is project-dependent (PIT for JVM, Stryker for JS/TS, mutmut for Python) and decided during the Architecture workflow. Mutation testing is most valuable when run against the dev agent's implementation tests (not the ATDD acceptance tests, which are spec-derived and structurally independent). It can be integrated into the TEA Automate workflow or run as a periodic quality check rather than on every story.

**6.3.6 Hybrid Research Workflow** — A custom BMAD workflow (built via BMB) that codifies the three-step hybrid research process described in Section 7.1.4. The workflow wraps the existing Analyst research workflows with two additional steps: (1) prompt preparation for external deep-research tools (Gemini Deep Research), and (2) synthesis of external results with internal multi-agent research. Phase 3 implementation covers the manual version (user submits the external prompt and pastes results back). Future iteration adds async API integration with Gemini to eliminate the manual step entirely.

### 6.4 Process Task Backlog

Process improvement work — new hooks, agent refinements, workflow wrappers, rule additions, research refreshes — does not follow the product story lifecycle. It has different validation criteria, operates on a different cadence, and the specs direct the dev agent to orchestrate BMB agents rather than write product code. But it still needs tracking and accountability.

**The model: a concurrent backlog of process tasks that lives outside the sprint but is prioritized relative to it.**

Process tasks are not stories. They don't go through ATDD or sprint planning. They are lightweight work items that specify: what needs to change, which BMB agent(s) are needed, and how urgent it is.

**Priority levels:**

| Priority | Meaning | When to execute | Example |
|----------|---------|-----------------|---------|
| **Critical** | Blocking. Cannot continue product work without this fix. | Immediately — drop current work. | Hook rejecting valid commits; broken ATDD workflow; code reviewer hallucinating findings |
| **High** | Should be resolved this sprint; can wait until the current story is done. | Between stories within the current sprint. | Findings ledger showing a recurring pattern that needs a new rule; noisy code reviewer prompt |
| **Low** | No urgency. Plan for a future sprint. | Batched at sprint boundaries. | Wrapping a retrospective workflow; building hybrid research workflow; nice-to-have hook refinements |

**Where process tasks come from:**

- **Retrospectives** — the primary source. The retrospective evaluates the entire process against the sprint's product stories and generates process tasks for anything that didn't work well.
- **Per-session flywheel** — when an agent surfaces a quality failure mid-session and the developer confirms it's systemic, a process task is created immediately.
- **Findings ledger patterns** — when the retrospective's cross-story analysis reveals recurring findings, those become process tasks.
- **BMAD change tracking** — when monthly BMAD reviews (Section 8.3) reveal framework changes that require customization updates.

**Task format:** JSON as canonical source (`docs/process/process-backlog.json`), markdown as derived human-readable view (`docs/process/process-backlog.md`). Fields: task description, priority, status (`open` / `in-progress` / `done`), executing agent(s) (e.g., `workflow-builder`, `agent-builder`, `module-builder`, `direct-edit`), source (retrospective, flywheel, findings ledger, BMAD tracking), plan reference, and date created. Not the full story format — just enough to track and prioritize. The add/resolve workflows regenerate the markdown view whenever the JSON changes. The backlog is seeded with all implementation roadmap items from Sections 6.1-6.3, each assigned a process task priority based on whether product work can proceed without it.

**Specification and execution:** Process tasks follow the same spec-first discipline as product work, just lighter weight. The Analyst creates a Quick Spec for the task. The dev agent executes it — same as product stories. The difference is what the spec contains: instead of "write this service with TDD," a process task spec says "invoke module-builder to create this module, then invoke workflow-builder to create these workflows." The dev agent is the **universal spec executor** — the spec determines whether it writes code directly or orchestrates BMB agents.

Each process task's spec identifies which BMB agents are needed:
- **Workflow modifications** → BMB workflow-builder or module-builder
- **Agent prompt changes** → BMB agent-builder
- **New hooks or hook refinements** → direct edit or module-builder
- **CLAUDE.md / .claude/rules/ updates** → direct edit
- **Research refreshes** → Analyst (with hybrid research workflow when applicable)

**Sub-agent workflows for backlog management:** Two simple Momentum operational workflows to keep backlog management low-friction:
- **Add task** — accepts a description, priority, source, and executing agent(s); appends to the backlog JSON and regenerates the markdown view. Invocable from any session (retrospective, mid-story, research review).
- **Resolve task** — marks a task done, records what was changed, regenerates the markdown view. Invocable after completing a process task.

The key is that adding or resolving a task is a single command, not a multi-step process that creates friction.

**Relationship to product sprints:** Process tasks are not *in* the sprint, but they are evaluated *by* the sprint. The retrospective reviews both the product stories and the process that supported them. This is where new process tasks are generated and where prior process changes are assessed for effectiveness. The process backlog is a standing agenda item in every retrospective.

### What to Use As-Is, Modify, and Create

**Use As-Is:** All existing BMAD planning workflows (Brief, PRD, Architecture, Epics, Stories, Sprint Planning), all TEA workflows, BMB self-modification, all BMAD review tasks.

**Modify (via wrapper workflows or customize files — not direct edits, per Section 8.1):** Dev Story (add TEA prerequisite gate), Code Review (remove auto-fix option to enforce pure verifier role; load quality rules), Retrospective (add findings ledger integration, upstream trace categorization, and process backlog review as standing agenda item), review tasks (load quality rules).

**Create:** Hook infrastructure, CLAUDE.md architecture, sub-agents, upstream-fix skill, quality rules file, CLAUDE.md generator, flywheel automation, pipeline orchestrator, cross-model verification skill, PBT integration, architectural fitness tests, hybrid research workflow, research index, findings ledger, process task backlog (file + add/resolve workflows), Discord MCP integration (pending admin approval).

**Don't Build (Claude Code native handles it):** CI/CD enforcement (use GitHub Action + TEA CI), formatting enforcement (use PostToolUse hooks), commit message enforcement (use PreToolUse hooks), secret scanning (use hooks with existing tools).

---

## 7. Measuring Success

The process is working when:

- **Upstream fixes per sprint** start high and decrease over time (the system is learning)
- **Code review Critical findings** decrease over sprints (upstream fixes are preventing recurrence)
- **Test coverage** increases without manual effort (TEA integration is working)
- **Pattern drift incidents** decrease (architecture-guard and rules are effective)
- **Time spent reviewing** decreases as a proportion of total work (layered verification is catching issues before human review)
- **The developer can explain every architectural decision** in the codebase (cognitive debt is controlled)

The process is failing when:
- The same class of error recurs across stories (the flywheel is not turning)
- CLAUDE.md and quality rules are not being updated (upstream fix discipline has lapsed)
- The developer accepts AI output without understanding it (cognitive debt is accumulating)
- "Just fix the code" becomes the default response to quality failures (downstream patching)

### 7.1 Research Lifecycle Management

Research is a first-class project artifact, not a one-time activity. Every research document used to inform decisions — this plan's consolidated research, domain research, technical research, market research — has a lifecycle: it is created, it informs decisions, and eventually it either remains actively relevant or becomes stale. Managing that lifecycle prevents two failure modes: making future decisions on outdated research, and wasting effort re-evaluating research that has already served its purpose.

**7.1.1 Research Index**

Maintain a research index (`docs/research/research-index.md` or `.json`) that tracks every research artifact used in the project:

| Field | Purpose |
|-------|---------|
| Title | What was researched |
| File path | Where the research lives |
| Date created | When the research was conducted |
| Last refreshed | When it was last reviewed or updated |
| Status | `active` (still informing decisions), `monitor` (relevant but not actively used), `archived` (decision made, no ongoing value) |
| Usage | How this research is used — which plan sections, architecture decisions, workflow designs, or product features depend on it |
| Refresh trigger | What would make this research need updating (e.g., "new DORA report," "Anthropic changelog," "competitor launch") |

The index makes the quarterly review tractable. Without it, the reviewer has to rediscover what research exists and why it matters — exactly the kind of context reconstruction that wastes LLM sessions.

**7.1.2 Quarterly Research Review**

Every quarter, review the research index with these questions:

- **Active research — still current?** Has the field moved? Are there new studies, tools, frameworks, or reference implementations that update or invalidate the findings? If so, flag for refresh. Key areas for this plan: DORA/LinearB metrics, Claude Code capabilities (hooks, agents, MCP), Ox Security anti-pattern catalogs, competing spec-driven development approaches. Note: BMAD framework evolution is on a **monthly** review cadence, not quarterly — see Section 8.3.
- **Active research — new topics needed?** Has the project or product evolved in ways that need research coverage? New technology choices, new compliance requirements, new market segments, new workflow patterns? If so, commission new research.
- **Monitor research — promote or archive?** Research in `monitor` status should be promoted to `active` if it's becoming relevant again, or archived if the window has closed.
- **Archived research — still archived?** Briefly confirm. Archived research that's been superseded can be deleted entirely to reduce future iteration overhead.
- **Terminology drift:** "Agentic Engineering" and "Context Engineering" are recent terms. The vocabulary may shift — staying current prevents the plan from becoming an island of outdated language.

After the review, update the research index, refresh any flagged documents (using the hybrid research workflow — see 7.1.4), and assess whether findings warrant changes to this plan (see 7.2) or to any BMAD workflows, architecture documents, or product decisions that depend on the research.

**7.1.3 Temporal Focus: The Recency Imperative**

Most research in this domain is extremely time-sensitive. LLM capabilities, agentic tooling, AI development patterns, and even the frameworks we build on (BMAD, Claude Code, TEA) evolve on a weeks-to-months cadence. A research refresh that treats all time periods equally will produce stale output that recapitulates what the LLM already knows from training data — which is precisely the information most likely to be outdated.

**The 80/20 rule for research refreshes:** When refreshing existing research, ~80% of the effort should focus on the window from the last research date to now. The prior research is already captured and serves as baseline context — it does not need to be re-discovered, only checked for invalidation. The refresh question is "what's new since we last looked?" not "what do we know about this topic?"

**New topic research is also temporally weighted.** Even when researching a topic for the first time, if it involves LLMs, AI tooling, agentic patterns, or fast-moving technology, the research should be heavily weighted toward the last 2-3 months. Older material provides foundation but the actionable insights — what actually works today, what's been deprecated, what patterns have emerged — live in the recent window.

**The training data anti-pattern.** This is the single most dangerous failure mode in LLM-conducted research: the model defaults to its training data instead of actively searching for current information. Training data for any model is months to a year old at the time of use. For stable domains (mathematics, established engineering principles) this is fine. For LLM capabilities, AI development workflows, agentic frameworks, and tooling — training data is an anti-pattern. It represents the state of the art *as it was*, not as it is.

Concrete mitigations:

- **Research prompts must specify temporal scope explicitly.** "Research developments in X from [last research date] to [today]" — never just "research X." The hybrid research workflow (7.1.4) must encode this in its prompt preparation step.
- **Research prompts must instruct web search, not recall.** Explicitly direct the LLM to use web search, documentation sites, changelogs, and release notes rather than answering from memory. Phrases like "search for," "find recent," and "check the latest" are not optional niceties — they are control flow.
- **Research outputs must cite sources with dates.** Any finding without a dated source is suspect. If the LLM cannot point to a specific URL, release note, or publication with a date, the finding may be training-data recall masquerading as current research.
- **The existing research baseline prevents redundancy.** By providing prior research as input context, we give the LLM the foundation it needs without asking it to re-derive it from (stale) training data. The model's job is delta, not total recall.

These temporal focus rules apply to all three research methods: the quarterly review (7.1.2), the hybrid research workflow (7.1.4), and any ad-hoc research conducted during the project lifecycle.

**7.1.4 Hybrid Research Workflow**

Experience has shown that combining two independent research processes produces results vastly superior to either alone:

1. **Prepare external research prompt.** The BMAD Analyst agent (`/bmad-agent-bmm-analyst`) prepares a research prompt optimized for Gemini Deep Research (or equivalent external deep-research tool). This prompt is crafted with the project's context, the specific research questions, and the existing research baseline — information the external tool wouldn't have on its own. The prompt must encode the temporal focus rules from 7.1.3: explicit date range (last research date to today), instruction to search rather than recall, and requirement for dated source citations.

2. **Launch parallel research.** Two research tracks run concurrently:
   - **External track:** The user submits the prepared prompt to Gemini Deep Research (currently manual; see future automation below). This leverages Gemini's broad crawl-based synthesis.
   - **Internal track:** The Analyst runs the BMAD research workflow (`/bmad-bmm-technical-research`, `/bmad-bmm-domain-research`, or `/bmad-bmm-market-research` as appropriate), typically spinning up multiple sub-agents to cover different angles and consolidating their results.

3. **Synthesize.** The Analyst combines the external research results with the internal research, cross-referencing findings, resolving conflicts, and producing a consolidated output that has both breadth (Gemini's web-scale coverage) and depth (the Analyst's project-aware analysis).

This three-step process should be captured as a custom BMAD workflow (built via BMB — see Section 6.3.6) so that it can be invoked without re-explaining the process each time. The workflow wraps the existing Analyst research workflows with the external prompt generation step and the synthesis step.

**Future automation:** The manual step (submitting the prompt to Gemini and retrieving results) is a candidate for API integration. Once Gemini's Deep Research API supports async calls, the workflow could launch the external research programmatically — submit the prompt, continue with internal research, and pull Gemini's results when ready. This would make the entire hybrid process a single workflow invocation with no manual intervention.

### 7.2 Plan Evolution (Continuous, Gated)

This plan has two layers with different change velocities:

**Philosophy and principles (Sections 1-4) — change infrequently.** The Authority Hierarchy, Producer-Verifier separation, Evaluation Flywheel, Impermanence Principle, three enforcement tiers, and layered verification are grounded in structural reasoning that doesn't expire when a tool updates. These should change only when research (Section 7.1) reveals a fundamental shift — e.g., if a new verification pattern demonstrably outperforms Producer-Verifier, or if a new debt type is formally identified.

**Process and implementation (Sections 5-8) — change early and often.** The specific workflows, hook configurations, sub-agent definitions, and tooling choices are practical decisions that should evolve with experience. Especially during the first 2-3 months of implementation (Phases 1-2), expect rapid iteration:

- A hook that fires too aggressively gets tuned or conditionally scoped
- A sub-agent's review process proves too superficial or too noisy — its instructions get refined
- The ATDD-before-Dev-Story gate turns out to need exceptions for certain story types
- A CLAUDE.md rule is ignored under context pressure — promote it to a hook
- The Stop hook's conditional logic needs adjustment based on real session patterns

**How to update:** Treat this plan document itself as an upstream artifact subject to the Evaluation Flywheel. When a process or implementation detail is found wanting:

1. Identify whether the issue is philosophy (Sections 1-4) or implementation (Sections 5-8)
2. For implementation: update this plan, then implement the change. The plan stays current as the source of truth for how the process works.
3. For philosophy: flag for the next quarterly research refresh. Philosophy changes should be deliberate, not reactive.
4. For both: note the change in a lightweight decision log (see Section 6.1.5) so the reasoning is preserved.

**The mechanics of a plan update.** The first major update to this plan (March 8, 2026) revealed that updating a plan of this size is itself a non-trivial process that benefits from discipline. When updating:

- **Content changes propagate.** A new concept (e.g., the findings ledger) may need to be added in its primary section, referenced from several other sections, and reflected in the elevator pitch (Section 1.1). Changes are rarely confined to one section.
- **Cross-references break.** Adding, removing, or renumbering sections invalidates references throughout the document. After any structural change, search for all `Section X.Y` references and update them. This is tedious but critical — a broken cross-reference sends the reader (or the LLM loading this as context) to the wrong place.
- **The elevator pitch (Section 1.1) must stay current.** It's the first thing read and sets the frame. After any significant update, re-read it and check whether it still accurately describes the practice. If a concept was important enough to add to the plan, it's probably important enough to mention in the elevator pitch.
- **Philosophy may need extraction from implementation.** New ideas often arrive as implementation details (Section 6-8) and only later reveal themselves as core principles (Section 4). Be willing to promote — the Impermanence Principle started as Section 8 implementation detail and was promoted to Section 4.7 when its philosophical nature became clear.
- **Section 1.2 ("What This Document Adds") should be updated** when the plan's scope expands beyond what BMAD provides. New bullet points here signal that the plan has grown.

The goal is that this document always reflects how the process *actually works today*, not how it was originally designed. A plan that diverges from practice is worse than no plan — it becomes misleading context.

---

## 8. BMAD Customization and Adaptability

This section implements the Impermanence Principle (Section 4.7) for our primary framework dependency: BMAD. BMAD is not static — V6 was a major rewrite, and another major evolution (skills-based architecture) is imminent. The principle tells us *what* to ask ("should this change?"); this section tells us *how* to manage the answer.

### 8.1 Customization Strategy

Given the "should this change?" frame, the strategy matches each type of customization to the right layer:

**Layer A: Invariants → Claude Code native infrastructure.** Things that encode fundamental rules regardless of framework version: file protection hooks, lint/test execution hooks, the Authority Hierarchy rule in `.claude/rules/`, sub-agents with fixed mandates (like the read-only code-reviewer). These should rarely change. When they do, it's because the invariant itself has been reconsidered, not because a framework updated.

**Layer B: BMAD behavioral customizations → Customize files and custom modules.** Things that should evolve with BMAD: agent persona tweaks, added menu items, injected memories, wrapper workflows that orchestrate built-in workflows with added pre/post steps. The `_bmad/_config/agents/*.customize.yaml` files handle lightweight agent adjustments (persona, menu items, memories, action handlers). Custom modules handle deeper changes — new workflows, new agents, templates, data files. Both participate in BMAD's evolution: when BMAD improves an underlying workflow, your wrapper automatically benefits. When BMAD changes its agent model, customize files adapt at the new customization surface.

**Layer C: Wrapper workflows → Thin orchestration in custom modules.** When you need to change *how* a built-in workflow runs (add pre-steps, post-steps, combine with external tools), create a wrapper workflow in a custom module. The wrapper calls the underlying workflow but adds orchestration. Key discipline: wrappers should be **thin** — orchestration, not reimplementation. When the underlying workflow changes, a thin wrapper is easy to adapt. A thick wrapper that duplicates logic becomes a parallel implementation that diverges. The hybrid research workflow (Section 7.1.4) is a good example: it wraps the analyst research workflow with prompt preparation and synthesis steps.

**Layer D: Documented fragile changes → Migration manifest.** When you must modify a built-in workflow step file (e.g., removing the auto-fix option from code review, Section 6.2.5), document the change in a migration manifest and create a post-update script that can re-apply it. Accept that this is a workaround — track it, and migrate to a proper customize mechanism when BMAD provides one. Minimize Layer D changes; each one is maintenance burden.

**Important:** Layer B and C customizations are not inferior to Layer A — they're *appropriate* for things that should grow. A Claude Code native sub-agent is more durable than a BMAD agent, but it also won't benefit from a year of BMAD agent improvements. Choose the layer that matches the change profile, not the one that maximizes permanence.

### 8.2 The Momentum Module

> **⚠️ OBSOLESCENCE NOTE (2026-03-15):** The `momentum install` shell script approach and custom BMAD module packaging described in this section are **superseded** by the Agent Skills standard. Momentum's deliverables should be standard Agent Skills (`SKILL.md` with YAML frontmatter) installable via `npx skills` or equivalent standard package manager, not a proprietary install script. BMAD is already converting to skills-based architecture (see [BMAD CHANGELOG](https://github.com/bmad-code-org/BMAD-METHOD/blob/main/CHANGELOG.md)). The closer Momentum follows the official skills standard, the closer it gets to cross-IDE support (Cursor, Windsurf, Codex, Copilot). See `docs/research/preliminary-findings-momentum-as-skills-2026-03-13.md` for full analysis. The operational workflows and bootstrap concepts below may still apply but the delivery mechanism has changed.

A cross-project custom BMAD module named **Momentum** serves as the home for the agentic engineering practice layer — wrapper workflows, quality infrastructure, and customizations that apply across projects. The name reflects the core design: each sprint's learnings compound into the next, building continuous improvement momentum.

**Momentum is both the source of truth and the installer for the practice.** Global practice files (`~/.claude/CLAUDE.md`, `~/.claude/rules/`, `~/.claude/agents/`) are *deployed* state — the canonical versions live inside Momentum. This means the global layer is reproducible: new machine, run `momentum install`, practice restored. The module itself travels across projects via BMAD installation, so any project with BMAD can restore the global layer.

**Three roles:**

1. ~~**`momentum install`** — deploy global practice to this machine.~~ **OBSOLETE: Use standard Agent Skills installation (`npx skills` or equivalent).** ~~Copies canonical rule files, agent definitions, and global CLAUDE.md from Momentum to `~/.claude/`. Idempotent: detects existing files, backs up if different, reports what changed. Re-runnable after Momentum updates to propagate rule changes to the global layer. This solves the "new machine" problem.~~

2. **`momentum bootstrap`** — interactively generate initial project config for a new project. Walks the developer through decisions (stack, test framework, test commands, acceptance test directory) and scaffolds: project CLAUDE.md, `.claude/settings.json` (hooks), process backlog, findings ledger, quality rules file, cost observability config (`showTurnDuration` in settings.json, `ccusage` recommendation, optional OTel setup). The output is committed to the project repo like any other project file. Run once per project — after that, the project's `.claude/` files live in git and evolve through the flywheel. A second person cloning the project gets everything via `git clone`; they don't need to run bootstrap.

3. **Operational workflows** — ongoing workflows that support the practice for the life of the project: backlog add/resolve, retrospective wrapper with findings ledger integration, hybrid research workflow (Section 7.1.4), and future workflows as the practice evolves. Bootstrap is the one you outgrow; these keep running.

**Module structure:**

- ~~Lives in `_bmad/_config/custom/momentum/` (or as a standalone module in `_bmad/momentum/`)~~ **Delivered as standard Agent Skills packages**
- Contains canonical source files for global practice (rules, agents, CLAUDE.md templates)
- Contains the bootstrap workflow and operational workflows
- Contains shared templates and data files used across projects
- ~~Is copied or symlinked across project directories (the cross-project portability question — see Section 8.4)~~ **Installed via standard skill package manager**
- ~~Has `version: null` and `source: custom` in the manifest — not touched by npm updates~~

**What lives where:**

| What | Source of truth | Deployed to | How it travels |
|------|----------------|-------------|----------------|
| Practice rules, global agents, global CLAUDE.md | Momentum skills package | `~/.claude/` | Standard skill installation (`npx skills` or equivalent) |
| Project config, hooks, project rules | The project repo (`./.claude/`, root `CLAUDE.md`) | Already in repo | `git clone` |
| Momentum skills | Published package / repo | `.claude/skills/` in any project | Standard skill installation |

Note: The Momentum module pattern itself may be a temporary workaround. As BMAD evolves — particularly with the BMB overhaul toward skills-based architecture — native mechanisms for cross-cutting customization may emerge that make a separate module unnecessary. This is exactly the kind of thing that should be re-evaluated during BMAD change tracking (Section 8.3). The thin wrapper discipline makes migration easier when better patterns arrive.

### 8.3 BMAD Change Tracking

BMAD changes and updates require **at minimum monthly** research, potentially biweekly or weekly during periods of active development (like the current BMB overhaul). The field moves too fast for quarterly cadence on framework evolution specifically.

**Lightweight continuous monitoring:** Subscribe to and periodically scan the BMAD Discord discussion groups. Discord conversations surface upcoming changes, community workarounds, and design intent weeks before they land in releases. A quick scan of recent Discord activity is far cheaper than a full research cycle and provides early warning of changes that affect our customizations.

**Discord MCP integration (pending).** The ideal monitoring approach is a read-only Discord bot paired with an MCP server (e.g., `barryyip0625/mcp-discord`) so Claude Code can query BMAD Discord channels directly during research workflows. This requires the BMAD server admin to authorize the bot (View Channels + Read Message History permissions only). A request has been submitted to the BMAD Discord community (March 8, 2026) — awaiting response. If approved, setup is straightforward: create a bot application in the Discord Developer Portal, enable Message Content intent, install the MCP server via `npx mcp-discord`, and configure it in Claude Code's MCP settings. If not approved, fallback is manual Discord scanning with structured paste-and-process through the analyst.

**Structured periodic review:** At minimum monthly, run a focused research check (not a full hybrid research cycle — just a targeted scan of release notes, Discord highlights, and changelog). The research index entry:

| Field | Value |
|-------|-------|
| Title | BMAD Framework Evolution |
| Status | `active` |
| Refresh trigger | At minimum monthly; weekly during major transitions (e.g., BMB overhaul) |
| Usage | Informs all BMAD-dependent customizations (Sections 6.2.x, 8.1, 8.2), migration planning, and the Momentum module design |

**Why Discord matters here:** Web search and GitHub issues lag behind Discord by weeks. The research agents could not access Discord content — it requires authentication. The most actionable intelligence about BMAD's direction comes from the maintainer's Discord posts, not from shipped releases. Human monitoring of the BMAD Discord (`#bmad-method-help`, `#suggestions-feedback`, and general channels) is a critical input that cannot be automated away.

**Current intelligence (as of March 4, 2026 — from BMAD Discord):**

The BMAD maintainer (BMadCode) has outlined the following changes, most expected by end of March 2026:

1. **Universal skills architecture:** Agents become skills. Workflows become skills. Modules become collections of skills with manifests. All artifacts get metadata manifests linking them into the BMAD help system. This is the fundamental shift — not a V7, but a deep V6 evolution.

2. **Custom workflow registration as replacement or customization:** Custom workflows will be able to register as either a *replacement* for a built-in workflow or as a *customization* of one. Multiple approaches are being prototyped. This directly obsoletes our Section 8.1 Layer D (fragile changes with migration scripts) — once this ships, the code review auto-fix removal (Section 6.2.5) can be done properly through workflow customization rather than direct file editing.

3. **Improved agent customizability and a leaner agent model:** Less bloated, more effective, better integrated into the ecosystem. Each agent will have project or global memory (eventually with global install support and choice of memory). This may change how our customize.yaml tweaks work.

4. **Personal vs. project configuration split:** Name, language, skill level = personal config. Installed modules and project-focused settings = project config. This is directly relevant to cross-project portability (Section 8.4) — personal config travels with the developer, project config stays with the project.

5. **New BMBuilder (drastically different):** Conversion tools will help migrate existing artifacts to the new format. Our current custom modules will need migration, but tooling support is planned.

6. **New installer and post-install tooling:** `bmad-init`, `bmad-update`, `agent-customize`, `skill-customize` — all in development. Headless install tools for CI/CD.

7. **Workflows already available as slash commands** (shipped): Workflows no longer require loading an agent first. They have baked-in personas that get overridden when invoked through an agent.

**What this means for our plan:**

- **Section 8.1 Layer C (wrapper workflows)** remains the right interim pattern, but will likely be superseded by native workflow customization/replacement within weeks. Keep wrappers thin so migration is trivial.
- **Section 8.1 Layer D (fragile changes)** has a shelf life of weeks, not months. Once workflow customization ships, migrate all Layer D changes to proper customizations.
- **Section 8.2 (Momentum module)** may evolve from a module into a collection of skills with a manifest. The concept persists; the packaging changes.
- **The personal/project config split** resolves part of our cross-project portability question (Section 8.4) natively. Wait for this before building custom solutions.
- **Do not over-invest in workarounds.** The next 4-6 weeks will bring native solutions to problems we're currently working around. Invest in understanding the new architecture, not in perfecting the old workarounds.

Specific signals to continue watching:
- **Skills architecture release:** When agents/workflows/modules become skills with manifests. Track the exact migration path and conversion tooling.
- **Workflow customization/replacement:** When custom workflows can register as replacements. Immediately migrate all Layer D changes.
- **Personal vs. project config:** When the config split ships. Evaluate how it interacts with Claude Code's `~/.claude/` hierarchy.
- **Global install and memory:** When `bmad-init`, `bmad-link`, or equivalent ships. Evaluate whether it obsoletes our symlink/dotfiles approach.
- **New BMBuilder:** When it ships, evaluate the conversion tools and migrate custom modules.

### 8.4 Cross-Project Portability (Future — See Also Topic 2)

The Momentum module, Claude Code native infrastructure (hooks, agents, rules), and this plan itself all need to travel across projects. This is the cross-project knowledge sharing problem flagged as Topic 2. The full treatment is deferred, but the customization strategy above is designed with portability in mind:

- Layer A (invariants in Claude Code native) can be copied via `.claude/` directory replication or a setup script
- Layer B/C (custom modules and wrappers) can be copied, symlinked, or potentially published as npm packages if BMAD's module system supports it
- Layer D (fragile changes) are documented in a migration manifest that can be re-applied per project

The unresolved questions — shared vs. duplicated, monorepo vs. multi-repo, symlinks vs. npm packages, per-project CLAUDE.md vs. shared — are Topic 2.

---
