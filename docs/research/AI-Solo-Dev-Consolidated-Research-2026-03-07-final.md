# Consolidated Research: AI-Augmented Solo Development — Frameworks, Verification, and Workflow Optimization

**Date:** 2026-03-07
**Sources:** 7 research streams (original enterprise report, 6 sub-agent research clusters, Gemini Deep Research)
**Purpose:** Unified reference for building an optimized AI development workflow using BMAD V6 + Claude Code

---

## Table of Contents

1. [Terminology and Frameworks](#1-terminology-and-frameworks)
2. [The Authority Hierarchy and Producer-Verifier Architecture](#2-the-authority-hierarchy-and-producer-verifier-architecture)
3. [Solo Developer Challenges and Strategies](#3-solo-developer-challenges-and-strategies)
4. [Claude Code Implementation Patterns](#4-claude-code-implementation-patterns)
5. [Adversarial Verification and Multi-Agent Quality](#5-adversarial-verification-and-multi-agent-quality)
6. [Technical Debt Prevention](#6-technical-debt-prevention)
7. [BMAD V6 Gap Analysis](#7-bmad-v6-gap-analysis)
8. [Consolidated Terminology Guide](#8-consolidated-terminology-guide)
9. [Sources Index](#9-sources-index)

---

## 1. Terminology and Frameworks

### 1.1 The Terminology Landscape Has Settled

The AI-assisted development lexicon has rapidly consolidated around a small set of terms, each with distinct scope and professional connotation.

**Agentic Engineering** (Karpathy, Feb 2026) is emerging as the dominant umbrella term. Karpathy: "AI does implementation, human owns architecture, quality, correctness." Osmani's endorsement criterion: "You can say it to your VP of Engineering without embarrassment." Endorsed by IBM, Google, and multiple industry publications. Only ~1 month in widespread use but accelerating fast.

**Augmented Engineering / Augmented Coding** (Beck, Sep 2025) describes the developer-AI collaboration at the code level. Beck: "In augmented coding you care about the code, its complexity, the tests, and their coverage." Narrower scope than Agentic Engineering — describes the coding act, not the full orchestration workflow.

**Spec-Driven Development (SDD)** is the tactical framework that makes Agentic Engineering possible. Major institutional backing from GitHub (Spec Kit), AWS (Kiro), ThoughtWorks, and Martin Fowler's team. Boeckeler's three-level taxonomy is the most rigorous definition:

| Level | Name | Description |
|-------|------|-------------|
| 1 | **Spec-First** | Specification guides initial development, discarded after feature ships |
| 2 | **Spec-Anchored** | Specification persists and evolves alongside code |
| 3 | **Spec-As-Source** | Specification is the only maintained artifact; code is generated and marked "DO NOT EDIT" |

**Vibe Coding** (Karpathy, Feb 2025) — accepting AI output without review. 72% of developers say this is NOT part of their professional work (Stack Overflow 2025). Wikipedia article exists. Appropriate only for throwaway prototypes.

**Context Engineering** — "The strategic design and structuring of the environment, input data, and interaction flows that influence how an AI system interprets and responds." Placed on ThoughtWorks Radar in Assess ring. Has displaced "prompt engineering" as the critical discipline. MIT Technology Review called 2025's shift "from vibe coding to context engineering."

### 1.2 Terminology Gap: "Fix the Workflow, Not the Code"

**No standard term exists** for the practice of fixing the upstream specification/template/prompt rather than patching AI output directly. The concept is well-understood across multiple communities but lacks a pithy label. Existing approximations:

- **"Evaluation flywheel"** (OpenAI) — iterative refinement of prompts through failure analysis
- **"Data flywheel"** (NVIDIA) — self-improving loop where outputs refine inputs
- **"Specification refinement"** (SDD community) — fixing the spec rather than the code
- **"Upstream fix"** — informal practitioner term
- **"Prevent-Detect-Correct"** (Kim & Yegge) — prevention means fixing the process

This represents an open naming opportunity for your practice.

### 1.3 Alternative Maturity Frameworks

The Shapiro "Five Levels" framework (Level 0-5) has significant limitations: it measures autonomy, not verification quality, and implicitly suggests Level 5 (Dark Factory) is the goal. Multiple alternatives have emerged:

**DORA 2025 AI Capabilities Model** (Google) — The authoritative industry standard, now in its 12th year. Central finding: "AI's primary role is as an amplifier, magnifying an organization's existing strengths and weaknesses." Defines seven AI capabilities and seven team archetypes. Verification-quality-centric: explicitly warns that without strong automated testing, increased AI-driven change volume leads to instability.

Critical DORA data points:
- Individual tasks completed: +21%
- Pull requests merged: +98%
- Code review time: +91%
- PR size: +154%
- Bug rate: +9%
- Organizational delivery: **flat**

**Credo AI Governance Maturity Model** (Gemini source) — Six levels evaluating governance effectiveness, not autonomy. Progresses from Level 1 "Exploring" (ad-hoc, shadow AI) through Level 5+ "Governing at Speed" (automated, AI-augmented governance managing autonomous actors in real-time).

**AI-MM SET** (Santhosh Sundar) — Five levels across six dimensions including Trust/Safety/Governance and AI-Augmented Collaboration. Community-driven, CC BY 4.0.

**SEI/CMU AI Adoption Maturity Model** — Forthcoming (April 2026), from the creators of the original CMM/CMMI. Eight core dimensions including Workflow Re-engineering and Risk/Governance.

**Key gap:** No existing framework measures AI engineering maturity primarily by verification quality. The DORA model comes closest with its "amplifier" framing but is not structured as a maturity progression. This gap aligns with your instinct that "Level 4" defined by autonomy alone is insufficient.

### 1.4 The Three Developer Loops (Kim & Yegge)

From their book *Vibe Coding*, Kim and Yegge extend the traditional inner/outer loop model:

- **Inner Loop** (seconds-minutes): Rapid AI-assisted coding. Write, build, test, fix.
- **Middle Loop** (hours-days): Getting code into users' hands. Human collaboration, real user feedback.
- **Outer Loop** (weeks-months): Preventing systemic problems through stress tests, CI/CD, and governance.

Each loop uses a **Prevent-Detect-Correct** cycle. The middle loop is their novel contribution — the space between individual coding and strategic governance.

---

## 2. The Authority Hierarchy and Producer-Verifier Architecture

### 2.1 The Master Pattern: Specs > Tests > Code

Every research stream independently converged on the same hierarchy:

1. **Specifications** — the law (immutable by agents, human-written intent)
2. **Tests** — verification (pre-existing tests are read-only to coding agents)
3. **Code** — the mutable reality (generated, potentially disposable)

This hierarchy was discovered through failure:
- **StrongDM** found that coding agents "reward hack" unit tests — writing tautological assertions or hardcoding expected values
- **PactKit** documented Claude Code silently changing test assertions to make failing code pass (changing expected 20 results to 50,000)
- **Kent Beck** identified AI "deleting or disabling tests" as "cheating" — a warning sign of deviation

The enforcement mechanism: when a pre-existing test breaks, the agent must **stop and report why**, not modify the test. New tests are writable; existing tests are read-only.

### 2.2 The Producer-Verifier Pattern

No single coiner. The pattern appears under multiple names: evaluator-optimizer, generator-verifier, critic loop, reflection loop. Now well-documented by Google, Microsoft, Amazon, and academic sources.

**Formal definition:** One agent creates an artifact; a separate agent evaluates it against specific criteria. The separation of creation from validation is the core architectural principle.

**Key variations:**

| Variant | Description | Source |
|---------|-------------|--------|
| **Adversarial Critic** | Verifier operates as hostile security reviewer | Product School, Google |
| **Planner-Worker-Judge** | Three roles: continuous exploration, execution, cycle-end judgment | Cursor internal architecture |
| **TCR Loop** | Test suite verifies mechanically; failure triggers automatic revert | Beck/Werner |
| **Cross-Model Verification** | Route output to a competing vendor's model for review | Practitioner consensus |
| **Specialist Panel** | 15+ focused agents (correctness, security, performance) | Qodo production deployment |
| **Code Council** | "Secretary" sanitizes Producer artifacts before "Skeptic" evaluates | Academic (ICLR 2026) |

**Critical requirement:** Information compartmentalization. If the Verifier shares the same context as the Producer, it succumbs to the same automation bias. The Verifier must operate in a clean context window.

### 2.3 Diminishing Returns and Failure Modes

- Uncoordinated multi-agent systems can **amplify errors by 17x** (Towards Data Science)
- Accuracy gains **saturate beyond ~4 agents** without structured topology
- "Three models reviewing the same diff can share blind spots" — AI agents "don't review code like a senior engineer"
- None of the reviewing models "know what 'done' looks like unless you write it down"
- LLMs remain "systematically vulnerable to reasoning failures" that compound in multi-agent chains

**Implication:** More agents is not better. Structured topology with strict separation is better.

---

## 3. Solo Developer Challenges and Strategies

### 3.1 The Solo Developer Gap

Most AI engineering literature assumes team structures. A solo developer occupies PM, architect, implementer, and reviewer roles simultaneously. This creates unique pressures that are under-documented. No formal frameworks exist specifically for solo developer AI workflows.

### 3.2 Four Formally Named Debt Types

| Debt Type | Named By | When | Mechanism | Solo Dev Severity |
|-----------|----------|------|-----------|-------------------|
| **Verification Debt** | Vogels (AWS re:Invent) | Dec 2025 | Unreviewed AI output accumulating. 96% don't fully trust AI code, yet 48% skip verification | CRITICAL |
| **Cognitive Debt** | Storey (UVic) | Feb 2026 | Understanding gap: AI generates 5-7x faster than humans comprehend. 17% skill mastery reduction (Anthropic) | CRITICAL for solo |
| **Pattern Drift** | Multiple | 2025-2026 | AI reproduces/amplifies bad patterns from context. Self-reinforcing — each instance makes the next more likely | HIGH |
| **Technical Debt** | Traditional | — | Compounds exponentially (not linearly) with AI. Code duplication rose from 8.3% to 12.3% (GitClear). Refactoring collapsed from 25% to under 10% | HIGH |

The **Velocity Paradox** manifests in distinct phases:
- Months 1-3 (Euphoria): Accelerated delivery
- Months 4-9 (Plateau): Integration challenges, velocity flattens
- Months 10-15 (Decline): New features require debugging prior AI output
- Months 16-18 (The Wall): Delivery stalls entirely

### 3.3 The Productivity Paradox Is Real

The most robust finding: AI creates a perception of productivity that frequently exceeds measured reality.

| Study | Finding |
|-------|---------|
| METR controlled trial | Experienced devs **19% slower** with AI; 39-point perception gap (believed 20% faster) |
| Stack Overflow 2025 | Only 16.3% report significant productivity gains |
| HBR Feb 2026 | AI intensifies work rather than reducing it (task expansion, blurred boundaries, multitasking) |
| Karviha case study | 2.3x LOC increase, 4.7x test code increase — but this is one practitioner, not controlled |
| LinearB 8.1M PRs | 67.3% AI-generated PR rejection rate vs 15.6% human |
| ThoughtWorks | Realistic net cycle time impact: **8-13%**, not the 50% headlines suggest |

**Implication:** You cannot trust your own perception of whether AI is helping. Objective metrics (commit frequency, test coverage, defect rates, time-to-completion) are essential.

### 3.4 Verification Strategies Replacing Peer Review

For a solo developer, three adapted patterns have emerged:

1. **Subagent Code Review** — Separate AI instances review code in clean context windows. Documented in the Karviha case study (350k+ LOC solo codebase with Claude Code). The solo developer's substitute for peer review.

2. **Cross-Model Verification** — Route code + original spec to a competing model (e.g., Claude produces, Gemini reviews). Different training distributions catch different failure modes.

3. **Automated Guardrail Layers** — Linters, type checkers, test suites, CI/CD act as objective, tireless reviewers. The AI generates code; automated systems validate it; the human reviews only what survives automated checks.

### 3.5 The Continuous Improvement Flywheel

When AI produces bad output, the high-leverage fix is upstream:

1. AI generates code following a template/spec
2. Developer identifies errors or suboptimal patterns
3. Developer updates the template/spec/CLAUDE.md (**not** just the code)
4. Next generation from the same template produces better output
5. Repeated cycles compound improvements

This is documented as:
- **Evaluation flywheel** (OpenAI) — Analyze failures, Measure with automated graders, Improve prompts, repeat
- **Data flywheel** (NVIDIA) — self-improving loop from output analysis
- **DSPy** (Stanford) — programmatic prompt optimization using Bayesian/genetic approaches
- **Karviha practice** — "regular iteration on CLAUDE.md and skills based on observed failures"

The practical implementation: maintain a decision log. When AI output fails, ask "Is this a spec/template gap or a one-off error?" Spec gaps get permanent fixes. One-offs get one-off fixes.

### 3.6 Cognitive Load Management

The HBR "Work Intensification Cycle" (Feb 2026):
1. Task expansion — solo dev absorbs PM, design, DevOps responsibilities
2. Blurred boundaries — conversational AI makes work feel casual, bleeds into off-hours
3. Increased multitasking — AI enables managing multiple parallel workflows; context-switching degrades quality

**Mitigation strategies:**
- Split work into 4 phases: Research, Plan, Implement, Validate — clear AI context between each
- Never exceed 60% context window usage
- Each AI task should fit within one context window; clear between tasks
- Batch notifications and protect focus time
- Intentional pauses for assessment and decision-making

---

## 4. Claude Code Implementation Patterns

### 4.1 Hooks — Deterministic Quality Gates

Hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at lifecycle events. Unlike CLAUDE.md (advisory), hooks guarantee execution.

**Key quality gate patterns:**

| Hook Event | Pattern | Purpose |
|------------|---------|---------|
| `PreToolUse` (Edit\|Write) | File protection script | Block edits to protected files. Exit code 2 blocks the action |
| `PostToolUse` (Edit\|Write) | Auto-formatter/linter | Run prettier/eslint/black after every file modification. Deterministic, no reliance on Claude remembering |
| `Stop` (type: prompt) | End-of-turn quality check | Haiku evaluates whether tasks are complete. Returns `{"ok": false}` to block premature stopping |
| `Stop` (type: agent) | Multi-turn verification | Spawns subagent with tool access to run tests against actual codebase |
| `PreToolUse` (Bash git commit) | Pre-commit gate | Check for validation flag file that test scripts create only on success |
| `SessionStart` (compact) | Post-compaction re-injection | Re-inject critical context after context compaction |

**Critical detail:** Stop hooks must check `stop_hook_active` to prevent infinite loops.

### 4.2 Custom Sub-Agents — Adversarial Review Architecture

Sub-agents are markdown files with YAML frontmatter in `.claude/agents/`. Key configuration options:

- **`tools`**: Restrict to Read, Grep, Glob for review-only agents (least privilege)
- **`model`**: Can specify `opus` for higher-capability review tasks
- **`memory`**: Persistent memory across sessions (`user`, `project`, or `local` scope)
- **`hooks`**: Scoped hooks that only run while that subagent is active
- **`skills`**: Pre-loaded skill content injected at startup
- **`isolation: worktree`**: Work in temporary git worktree for safe experimentation
- **`background: true`**: Run concurrently while main conversation continues

**Recommended sub-agent topology for solo dev:**
1. **Code Reviewer** — Read-only tools, adversarial persona, runs after implementation
2. **Security Reviewer** — Read-only, OWASP-focused, optionally uses Opus for depth
3. **Architecture Guard** — Checks for pattern drift, dependency violations, consistency

### 4.3 Agent Teams (Experimental)

Multiple independent Claude Code sessions with shared task lists and inter-agent messaging. Enabled via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

- Start with 3-5 teammates; diminishing returns beyond that
- Target 5-6 tasks per teammate
- Avoid having two teammates edit the same file
- Best for research/review tasks before attempting parallel implementation
- ~7x token cost compared to subagents

### 4.4 The Ralph Wiggum Technique

Autonomous loop: when Claude tries to stop, a Stop hook re-injects the original prompt. Claude sees its previous work and continues. Now an official Anthropic plugin.

Results: 30-hour unattended loop built a complete programming language. $50K project completed for under $300 in API costs.

**Safety:** Always use `--max-iterations` to prevent infinite loops on impossible tasks.

### 4.5 CLAUDE.md Best Practices

- **Ruthless pruning:** "Bloated CLAUDE.md files cause Claude to ignore your actual instructions"
- **Test for inclusion:** For each line, ask "Would removing this cause Claude to make mistakes?" If not, cut it
- **Hierarchy:** Global (~/.claude/CLAUDE.md) → Project root → Subdirectories. Deeper files take priority
- **`@path` imports:** Reference external docs without inline bloat
- **Rules directory:** `.claude/rules/*.md` — always loaded, modular
- **Never include style rules a linter handles** — waste of context, unreliable enforcement
- **Focus on:** Architecture decisions, domain constraints, non-obvious behaviors, execution commands

### 4.6 Skills System

Skills (`.claude/skills/SKILL.md`) have superseded simple slash commands:
- Support `$ARGUMENTS` interpolation
- Can run in subagent context
- `disable-model-invocation: true` prevents auto-triggering for side-effect workflows
- The Karviha case study uses 25+ custom skills encoding atomic operations

### 4.7 MCP for Quality Automation

- **Playwright MCP** (Microsoft) — 25+ browser tools, accessibility-tree-based (10-100x faster than screenshots). Enables Claude Code as AI QA engineer
- **Code Mode MCP** (Cloudflare) — Exposes only search() and execute(), reducing token consumption for large toolsets by 99.9%
- **Drift MCP** — Scans codebases, learns conventions, feeds context to prevent pattern drift
- MCP configs can be scoped to subagents and passed to headless mode

---

## 5. Adversarial Verification and Multi-Agent Quality

### 5.1 The Quality Data Is Sobering

| Metric | Finding | Source |
|--------|---------|--------|
| AI PR rejection rate | 67.3% (vs 15.6% human) | LinearB, 8.1M PRs |
| Issues per PR | 10.83 AI vs 6.45 human (1.7x) | LinearB |
| Logic errors | 1.75x more frequent | LinearB |
| Security vulnerabilities | 1.57x more frequent | LinearB |
| Code churn | 41% higher for AI code | GitClear |
| Anti-patterns | Present in 80-100% of AI projects | Ox Security |
| Readability problems | 3x higher in AI code | CodeRabbit |
| Performance issues | 8x more frequent in AI code | CodeRabbit |
| Developer trust | Only 29% trust AI tools (down 11pts from 2024) | Stack Overflow |

### 5.2 Layered Verification Stack

No single verification approach suffices. The emerging consensus:

1. **Deterministic gates** — Type checking, linting, compilation, formatting. "Agents write the code; linters write the law" (Factory.ai). Never use an LLM to do a linter's job.
2. **Property-based testing** — Invariant checking via Hypothesis or similar. Anthropic's PBT agent found real bugs in NumPy, AWS Lambda, HuggingFace (86% validity, ~$5.56/bug). Properties resist gaming better than example-based tests.
3. **Adversarial multi-agent review** — Specialist agents for correctness, security, performance. Strict information compartmentalization between producer and verifier.
4. **Scenario/integration testing** — End-to-end user stories, ideally blind to coding agents (StrongDM's holdout set pattern).
5. **Strategic human review** — Risk-based, focused on architecture, security, and complex logic. Not every change needs the same scrutiny.

### 5.3 TCR (Test && Commit || Revert) with AI

TCR as applied to agentic coding:
1. AI writes a microscopic increment of code
2. Test suite executes automatically
3. **Pass:** Auto-commit with AI-generated message
4. **Fail:** Full revert (git reset --hard), new attempt

Forces atomic, provably correct steps. Prevents the "doom loop" of cascading error fixes. Scott Werner's `tcr_agent` (Ruby) is the documented implementation.

**Open question:** Agents lack persistent memory of past reverts — they may repeat failed approaches unless explicitly re-prompted with failure history.

### 5.4 Property-Based Testing — The Emerging Standard

PBT tests **properties and invariants** rather than specific input-output examples:

- Anthropic's PBT agent: tested 100+ Python packages, found 984 bug reports (56% valid, 86% validity for top-ranked). Real patches merged to NumPy, AWS Lambda Powertools, HuggingFace
- Property-Generated Solver: 23-37% relative improvement over TDD
- Kiro: Converts EARS specs directly into property tests
- Kleppmann argues formal verification is going mainstream: "A proof cannot be gamed"
- 98.2% success rate demonstrated on Dafny programs using multimodel approach

**Why PBT resists gaming:** Properties are derived from documentation and type signatures, not implementation. They express *what should always be true*, not *what specific outputs to expect*.

---

## 6. Technical Debt Prevention

### 6.1 The Foundational Principle: Deterministic Tools Over Prompting

The single most consistent finding across all sources: **never send an LLM to do a linter's job.** Factory.ai: "Agents write the code; linters write the law."

Two-layer approach:
- **CLAUDE.md** documents the "why" and provides examples in human language
- **Linting rules** encode the "how" and provide mechanical guarantees

Seven categories of lint rules (Factory.ai):
1. Grep-ability — Named exports, consistent formatting
2. Glob-ability — Predictable file organization
3. Architectural boundaries — Module separation, import policies
4. Security/privacy — Block secrets, require validation
5. Testability — Colocate tests, no network in unit tests
6. Observability — Structured logging
7. Documentation — Module-level docstrings for public APIs

### 6.2 The Ox Security Anti-Pattern Catalog

Analysis of 300+ repositories found these anti-patterns in 80-100% of AI-generated projects:

| Anti-Pattern | Rate | Description |
|-------------|------|-------------|
| Comments Everywhere | 90-100% | Excessive comments increase cognitive load |
| By-the-Book Fixation | 80-90% | Textbook patterns applied without context adaptation |
| Avoidance of Refactors | 80-90% | AI focuses on prompt, doesn't improve structure |
| Over-Specification | 80-90% | Extreme edge cases unlikely to occur |
| Bugs Deja-Vu | 80-90% | Regenerating code instead of creating reusable libraries |
| Return of Monoliths | High | Tightly coupled components |
| Vanilla-Style Code | High | Ignoring battle-tested libraries |

Headline: AI-generated code is "highly functional but systematically lacking in architectural judgment."

### 6.3 The Upstream Prevention Principle

Analogous to Deming's "fix the process, not the defect":

When AI produces technically-correct-but-debt-accumulating code, the correct response is to improve the specification, template, or agent instruction that produced it — not to patch the output. Every downstream fix is a one-time patch. Every upstream fix prevents a class of errors.

Implementation for solo dev:
1. Templates/skills encode project patterns
2. Error triggers template evaluation: "Is this a spec/template gap or a one-off?"
3. Spec gaps get permanent fixes (update CLAUDE.md, skill, or workflow template)
4. One-off errors get one-off fixes
5. Periodic review: audit templates for staleness, contradictions, or missing patterns

### 6.4 Solo Developer Prevention Stack

**Tier 1: Non-Negotiable (implement immediately)**
1. Deterministic quality gates — linters, formatters, static analyzers as pre-commit hooks
2. CLAUDE.md — maintained actively, every mistake becomes a rule
3. Human-written acceptance criteria — define "correct" before delegating
4. Pre-commit hooks blocking on test failure

**Tier 2: High Value (implement within weeks)**
5. Spec-first workflow — create spec.md before coding
6. Granular commits — atomic save points for quick rollback
7. Dual-model/subagent review — separate AI sessions critique generated code
8. Architectural tests — encode structural rules (dependency direction, layer separation)

**Tier 3: Ongoing Investment (build over time)**
9. ADRs — document decisions for future-you and future AI sessions
10. Automated traceability — link specs to tests to implementation
11. Drift detection — tools like Drift MCP that learn conventions and flag deviations
12. Dependency auditing — verify every AI-suggested package exists and is maintained

---

## 7. BMAD V6 Gap Analysis

### 7.1 What BMAD V6 Already Does Well

**Spec-Driven Pipeline: STRONG**
Complete chain from Brief → PRD → Architecture → Epics/Stories → Dev, with quality gates at each transition. PRD Validate has 13 validation dimensions. Implementation Readiness Check validates alignment across PRD, Architecture, UX, and Epics. The `create-story` workflow is a "context engine" that loads all relevant artifacts and embeds guardrails.

**Adversarial Verification: STRONG**
- `review-adversarial-general.xml`: Mandatory minimum 10 findings, "cynical, jaded reviewer" persona
- `review-edge-case-hunter.xml`: Systematic path enumeration, structured JSON output
- Code Review workflow: Adversarial, validates story claims against git reality, minimum 3 issues
- PRD Validation: 13 separate validation passes

**Dev Agent Execution Discipline: STRONG**
- Strict task-by-task execution in story order
- Red-green-refactor TDD cycle per task
- No proceeding with failing tests
- Definition of Done checklist with 20+ items
- Auto-halt on repeated failures

**Testing Infrastructure (TEA): STRONG**
8 workflows: ATDD, Test Framework, CI Setup (5 platforms), Test Automation, Test Review (0-100 scoring), NFR Assessment, Traceability Matrix, Teach Me Testing. 40+ knowledge files.

**Self-Modification (BMB): STRONG**
Can create, edit, validate its own agents, workflows, and modules.

### 7.2 What Needs Modification

1. **YOLO mode is per-workflow, not per-pipeline** — No "pipeline YOLO" chaining Brief→PRD→Architecture→Epics→Dev→Review
2. **Retrospective captures but doesn't auto-apply** — Learnings must be manually incorporated
3. **Code review auto-fix is user-gated** — For Level 4, should auto-fix and only surface blocking decisions
4. **TEA and BMM operate independently** — Dev-story mentions TEA as optional, no integrated workflow

### 7.3 What Is Missing

1. **Pipeline Orchestrator** (highest priority) — Single-command "spec to shipped code" workflow
2. **CLAUDE.md / Hooks Integration** — BMAD runs entirely through agent conversations; no integration with Claude Code's native enforcement
3. **Automated Learning Loop** — Retrospective findings should auto-update CLAUDE.md, agent instructions, and DoD checklists
4. **Quality Metrics Dashboard** — No tracking of review findings, coverage trends, or retrospective action items over time
5. **Parallel Execution Coordination** — No lock file or race condition protection when running parallel sessions
6. **Project-Specific Quality Rules** — No `quality-rules.yaml` loaded by review workflows

### 7.4 Mapping Table

| AI Development Need | BMAD Component | Status |
|---------------------|----------------|--------|
| Human writes spec, AI executes | Brief → PRD → Arch → Epics → Story → Dev | Ready |
| PRD quality validation | PRD Validate (13 dimensions) | Ready |
| Architecture validation | Implementation Readiness Check | Ready |
| Story context loading | Create Story context engine | Ready |
| Single-story autonomous dev | Dev Story + YOLO mode | Ready |
| Multi-story pipeline automation | — | **Missing** |
| General adversarial review | review-adversarial-general.xml | Ready |
| Edge case analysis | review-edge-case-hunter.xml | Ready |
| Code review (story-based) | Code Review workflow | Ready |
| Auto-fix without user gate | Code review, user-gated | **Needs Work** |
| Continuous review (hooks) | — | **Missing** |
| ATDD (failing tests first) | TEA ATDD workflow | Ready |
| Test framework setup | TEA Framework workflow | Ready |
| CI pipeline scaffolding | TEA CI workflow (5 platforms) | Ready |
| Test coverage traceability | TEA Trace workflow | Ready |
| Retrospective / learning capture | Retrospective workflow | Ready |
| Auto-apply learnings | — | **Missing** |
| Workflow self-modification | BMB module | Ready |
| CLAUDE.md integration | — | **Missing** |
| Pre-commit quality hooks | — | **Missing** |
| Project-specific rules engine | — | **Missing** |

### 7.5 External Assessment

Gemini's research rated BMAD V6 as "Challenging" for solo daily use compared to lighter SDD frameworks (OpenSpec, SpecKit), primarily due to learning curve, context switching between agents, and specification volume. However, it acknowledged BMAD provides an "unparalleled audit trail" and is the most architecturally rigorous option. The challenge is not capability but ergonomics — which the missing pipeline orchestrator would largely solve.

---

## 8. Consolidated Terminology Guide

### Terms to Use Professionally

| Context | Recommended Term | Alternative | Avoid |
|---------|-----------------|-------------|-------|
| Overall methodology | **Agentic Engineering** | AI-Augmented Software Engineering (formal/academic) | "AI coding", "Vibe Coding" |
| Development process | **Spec-Driven Development (SDD)** | — | "Prompt engineering" for this purpose |
| Quality philosophy | **Context Engineering** | — | "Prompt crafting" |
| Code quality pattern | **Producer-Verifier** separation | Adversarial verification | "AI reviews AI" |
| Testing approach | **Verification-Driven Development** | Augmented Coding (Beck) | "Let the AI test itself" |
| Risk management | **Layered Verification** with deterministic gates | — | "Trust the AI" |
| Debt prevention | Prevention of **Verification Debt** and **Cognitive Debt** | — | "Technical debt" alone (too vague) |
| Workflow improvement | **Upstream Fix** / **Evaluation Flywheel** | Specification refinement | "Fixing the code" |
| The framework | **BMAD V6** with **SDD** governance | — | — |

### Maturity Description

Rather than using "Level 4" from Shapiro's framework, describe your practice as:

> "I practice **Agentic Engineering** using **Spec-Driven Development** with **layered verification**. Specifications are the primary artifact — code is generated and verified through deterministic quality gates, adversarial sub-agent review, and property-based testing. The workflow is governed by the **BMAD Method V6** framework with continuous improvement through an evaluation flywheel."

This communicates rigor without relying on a numbered scale that implies full autonomy (Level 5) is the goal.

---

## 9. Sources Index

### Foundational Reports
- [DORA 2025 Report](https://dora.dev/research/2025/dora-report/) — Google, authoritative industry standard
- [Ox Security Anti-Pattern Report](https://www.prnewswire.com/news-releases/ox-report-ai-generated-code-violates-engineering-best-practices-undermining-software-security-at-scale-302592642.html) — Oct 2025
- [CodeRabbit AI vs Human Code](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) — Dec 2025
- [Anthropic 2026 Agentic Coding Trends](https://resources.anthropic.com/2026-agentic-coding-trends-report) — 2026
- [METR Controlled Trial](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — 2025
- [GitClear AI Code Quality](https://www.gitclear.com/ai_assistant_code_quality_2025_research) — 2025

### Terminology and Frameworks
- [Karpathy on Agentic Engineering](https://dnyuz.com/2026/02/08/the-guy-who-coined-vibe-coding-says-the-next-big-thing-is-agentic-engineering/) — Feb 2026
- [Beck: Augmented Coding](https://tidyfirst.substack.com/p/augmented-coding-beyond-the-vibes) — Sep 2025
- [Boeckeler: Understanding SDD](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) — Oct 2025
- [ThoughtWorks: SDD](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices) — Dec 2025
- [Osmani: Agentic Engineering](https://addyosmani.com/blog/agentic-engineering/) — Feb 2026
- [Mason: Coherence Through Orchestration](https://mikemason.ca/writing/ai-coding-agents-jan-2026/) — Jan 2026
- [Credo AI Governance Model](https://www.credo.ai/blog/the-six-levels-of-ai-maturity-where-does-your-organization-rank) — 2026

### Debt and Risk
- [Vogels: Verification Debt](https://www.kloia.com/blog/werner-vogels-final-reinvent-keynote-the-renaissance-developer/) — Dec 2025
- [Storey: Cognitive Debt](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/) — Feb 2026
- [Willison: Cognitive Debt](https://simonwillison.net/2026/Feb/15/cognitive-debt/) — Feb 2026
- [HBR: AI Work Intensification](https://hbr.org/2026/02/ai-doesnt-reduce-work-it-intensifies-it) — Feb 2026

### Claude Code Patterns
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks) — Official
- [Claude Code Sub-Agents](https://code.claude.com/docs/en/sub-agents) — Official
- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices) — Official
- [Claude Code GitHub Action](https://github.com/anthropics/claude-code-action) — Official v1 GA
- [Ralph Wiggum Plugin](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) — Official
- [Karviha: Claude Code in Production](https://dev.to/dzianiskarviha/integrating-claude-code-into-production-workflows-lbn) — Case study

### Verification and Testing
- [Anthropic PBT Agent](https://red.anthropic.com/2026/property-based-testing/) — 2026
- [StrongDM Software Factory](https://simonwillison.net/2026/Feb/7/software-factory/) — Feb 2026
- [Werner: TCR with AI](https://worksonmymachine.ai/p/test-and-and-commit-revert-with-ai) — 2025
- [Kleppmann: AI + Formal Verification](https://martin.kleppmann.com/2025/12/08/ai-formal-verification.html) — Dec 2025
- [BlueCodeAgent](https://www.microsoft.com/en-us/research/blog/bluecodeagent-a-blue-teaming-agent-enabled-by-automated-red-teaming-for-codegen-ai/) — Microsoft, Nov 2025
- [PactKit: Stopping Test Rewriting](https://dev.to/slimd/i-stopped-my-ai-coding-agent-from-rewriting-tests-heres-the-prompt-architecture-that-worked-1io8) — 2025

### SDD Frameworks
- [GitHub Spec Kit](https://github.com/github/spec-kit) — Open source
- [Kiro (AWS)](https://kiro.dev/) — IDE with SDD
- [OpenSpec](https://intent-driven.dev/blog/2025/12/26/choosing-spec-driven-development-tool/) — Lightweight SDD
- [Paul Duvall: AI Development Patterns](https://github.com/PaulDuvall/ai-development-patterns) — 27+ patterns
- [Factory.ai: Linters Direct Agents](https://factory.ai/news/using-linters-to-direct-agents) — 2025
- [BMAD Method V6](https://github.com/bmad-code-org/BMAD-METHOD) — GitHub

### Solo Developer
- [Osmani: LLM Coding Workflow](https://addyosmani.com/blog/ai-coding-workflow/) — 2025
- [OpenAI: Evaluation Flywheel](https://developers.openai.com/cookbook/examples/evaluation/building_resilient_prompts_using_an_evaluation_flywheel/) — Methodology
- [Kim & Yegge: Three Developer Loops](https://itrevolution.com/articles/the-three-developer-loops-a-new-framework-for-ai-assisted-coding/) — 2025
