---
content_origin: claude-code-subagent
date: 2026-04-10
sub_question: "How do the two frameworks frame feedback loops differently — cadence, signal types, actors, and direction?"
topic: "Momentum Flywheel vs. Fowler's Feedback Flywheel — Conceptual Comparison"
---

# Feedback Loop Framing: Momentum vs. Fowler's Feedback Flywheel

## Overview

Both frameworks invoke the "flywheel" metaphor to describe self-reinforcing improvement cycles in software development, but their underlying assumptions about *what kind of thing* a feedback loop is — and *who or what* closes it — differ substantially. Fowler's series treats feedback loops as human social processes that happen to involve AI tools. Momentum treats feedback loops as engineered quality pipelines that happen to involve human checkpoints.

This document compares the two frameworks across five analytical dimensions: cadence, signal types, actors, direction of flow, and mechanism of closure.

---

## Primary Sources

**Fowler's Framework:**
- "Feedback Flywheel" — Rahul Garg, martinfowler.com, 2026-04-08 [OFFICIAL]
- "Encoding Team Standards" — Rahul Garg, martinfowler.com, 2026-03-31 [OFFICIAL]
- "Context Anchoring" — Rahul Garg, martinfowler.com, 2026-03-17 [OFFICIAL]
- "Harness Engineering for Coding Agent Users" — Birgitta Böckeler, martinfowler.com, 2026-04-02 [OFFICIAL]
- "Maximizing Developer Effectiveness" — Tim Cochran, martinfowler.com [OFFICIAL]
- "Continuous Integration" — Martin Fowler, martinfowler.com [OFFICIAL]

**Momentum Framework:**
- `/skills/momentum/references/practice-overview.md` [OFFICIAL]
- `/skills/momentum/skills/sprint-dev/workflow.md` [OFFICIAL]
- `/skills/momentum/skills/sprint-planning/workflow.md` [OFFICIAL]
- `/skills/momentum/skills/retro/workflow.md` [OFFICIAL]
- `/skills/momentum/skills/avfl/SKILL.md` [OFFICIAL]
- `/skills/momentum/skills/upstream-fix/SKILL.md` [OFFICIAL]
- `/skills/momentum/references/completion-signals.md` [OFFICIAL]

---

## Dimension 1: Cadence

### Fowler's Framework

Fowler's "Feedback Flywheel" article describes four explicitly named rhythms operating at different timescales:

- **After-session** (immediate): "One question: did anything happen in this session that should change a shared artifact?" This is a personal reflective act, requiring a few seconds per session.
- **Daily stand-up** (daily): "A simple question such as 'did anyone learn something with the AI yesterday that the rest of us should know?'" makes individual discovery social.
- **Sprint retrospective** (sprint-cadence): "What worked with AI this sprint? What friction did we hit? What will we update?" — the authoritative forum for ratifying artifact changes.
- **Periodic review** (quarterly): A light-touch audit that artifacts remain current and in use.

The cadence structure is deliberately *social and ceremonial* — it hooks into meeting rhythms that already exist rather than requiring new infrastructure. As the article states: "The heaviest cadence is a five-minute agenda item in a meeting that already exists." [OFFICIAL]

Böckeler's "Harness Engineering" article adds a complementary technical layer: computational controls run at millisecond scale (pre-commit linters, type checkers), while inferential controls (AI-driven code review, LLM judges) run at commit and pipeline stages. These are not described as "feedback loops" per se but as sensor/guide pairs. [OFFICIAL]

### Momentum's Framework

Momentum has no fixed-cadence social rituals. Its feedback loops are **event-driven by workflow stage completion**, not by clock or meeting schedule:

- **Story-level** (per-story): AVFL validation runs once per story arc within `momentum:dev`. Code review agents run post-implementation.
- **Sprint-level** (per-sprint): AVFL runs once after ALL stories merge (Decision 31). Per-story code review runs in parallel after merge (Phase 4b). Team Review (QA Agent, E2E Validator, Architect Guard) runs in Phase 5. These are not optional — they are workflow phases.
- **Retrospective** (post-sprint): The retro workflow runs after sprint completion. It is not a ceremony in the Fowler sense — it spawns a collaborative auditor team that performs structured DuckDB analysis of session transcripts, inter-agent messages, and tool errors.
- **Plan-time** (pre-sprint): AVFL validates the sprint plan during sprint planning (Step 6), before any code is written.

The pattern is: feedback loops trigger at **natural workflow pause points** defined by the artifact lifecycle, not by clock time. Practice-overview.md states this directly: "Quality before speed — gates run at natural pause points; they don't block, they catch." [OFFICIAL]

### Comparative Assessment

| | Fowler | Momentum |
|---|---|---|
| Primary cadence model | Social/ceremonial (daily, sprint, quarterly) | Event-driven (workflow-stage completion) |
| Fastest loop | After-session reflection (seconds, human-initiated) | Hook-based pre/post-tool invocations (milliseconds, automated) |
| Slowest loop | Quarterly artifact review | Retrospective (post-sprint, spans weeks) |
| Trigger mechanism | Human decides to trigger | Workflow orchestrator triggers automatically |

**Underlying philosophy:** Fowler believes the bottleneck is *human attention* — loops need to be designed to fit naturally into how developers already spend their time. Momentum believes the bottleneck is *workflow discipline* — loops must be wired into the execution path so they cannot be skipped.

---

## Dimension 2: Signal Types

### Fowler's Framework

The Feedback Flywheel article defines four signal types with explicit routing destinations [OFFICIAL]:

| Signal Type | Definition | Destination |
|---|---|---|
| **Context Signal** | Gaps in the priming document — missing conventions, outdated version numbers, knowledge the AI lacked. "When the AI keeps using the deprecated Prisma 4.x API, that is not a model failure; it is a priming gap." | Priming documents |
| **Instruction Signal** | Prompts and phrasings that produced notably good or bad results. Personal discoveries about effective constraints or decomposition. | Shared commands / prompt templates |
| **Workflow Signal** | Sequences of interaction that succeeded — conversation structures, task decomposition approaches, playbooks. | Team playbooks / SOPs |
| **Failure Signal** | "Where the AI produced something wrong, and why. The root cause matters." Not just what failed, but what gap caused it. | Guardrails and documented anti-patterns |

These signal types are exclusively about the *quality of human-AI interaction*. They are epistemological — they track what the team learned about working with AI. None of them capture test failures, build breakage, or runtime errors.

Böckeler's Harness Engineering article adds technical signal types [OFFICIAL]:

- **Computational signals**: Deterministic outputs from linters, type checkers, tests. Millisecond scale. Certain.
- **Inferential signals**: Probabilistic outputs from LLM judges, AI code reviewers. GPU-scale. Semantic.

### Momentum's Framework

Momentum captures a different set of signal types, all structured around quality evidence:

- **AVFL findings**: Structured findings with id, severity (critical/high/medium/low), confidence (HIGH/MEDIUM), lens (structural/accuracy/coherence/domain), dimension, location, and mandatory evidence quote. No evidence = finding discarded. [OFFICIAL — AVFL SKILL.md]
- **Code review findings**: Per-story findings tagged by story, file, severity, and source. Produced by `momentum:code-reviewer` agents. [OFFICIAL — sprint-dev workflow]
- **E2E validation results**: Per-scenario pass/fail from Gherkin-specified scenarios. The E2E Validator tests running behavior without source code access (black-box, Decision 30). [OFFICIAL — sprint-dev workflow]
- **QA review**: Per-story acceptance criteria verification against story spec. [OFFICIAL — sprint-dev workflow]
- **Architecture drift findings**: Pattern violations detected by the Architect Guard against documented architecture decisions. [OFFICIAL — sprint-dev workflow]
- **Transcript audit findings**: Structured retrospective analysis of human prompts, agent errors, and inter-agent coordination patterns extracted via DuckDB from session logs. Categories: corrections, redirections, frustration signals, duplication, error patterns, efficiency issues. [OFFICIAL — retro workflow]
- **Upstream failure traces**: Critical findings that `momentum:upstream-fix` can trace to root cause in spec, rule, or workflow. [OFFICIAL — completion-signals.md, upstream-fix SKILL.md]

Momentum signals are about *execution quality* — what the code or agents actually produced. They are forensic and evidence-mandatory.

### Comparative Assessment

| | Fowler | Momentum |
|---|---|---|
| Signal orientation | Epistemological (what did we learn about working with AI?) | Forensic (what defects exist in the work product?) |
| Signal source | Human observation of AI sessions | Automated agents (AVFL, code-reviewer, E2E, QA) + transcript analysis |
| Signal structure | Informal (human judgment on what's noteworthy) | Mandatory schema (id, severity, evidence, suggestion) |
| Signal threshold | Developer discretion | Evidence-required (no evidence = discarded finding) |
| Missing signal type (vs. Fowler) | Instruction/Workflow signals about AI interaction quality | Not captured |
| Missing signal type (vs. Momentum) | Gherkin E2E pass/fail, architecture drift, AVFL scores | Not captured |

**Underlying philosophy:** Fowler's signals are *input-oriented* — they improve what you feed the AI. Momentum's signals are *output-oriented* — they assess what the AI produced. Neither framework captures both. Fowler has no equivalent to AVFL's evidence-mandatory structured findings. Momentum has no equivalent to Fowler's Instruction Signal or Workflow Signal (tracking which prompts work best).

---

## Dimension 3: Actors

### Fowler's Framework

Fowler's framework centers the *human developer* as the primary actor in all feedback loops:

- **Individual developer**: Observes sessions, notices friction, proposes artifact updates. "Each developer accumulates individual intuition...but that intuition remains personal. It does not transfer." [OFFICIAL]
- **Tech lead / designated owner**: "Makes the final call on what gets committed to shared artifacts." Gatekeeps which observations become team standards.
- **Team collectively**: Surfaces discoveries at stand-ups, decides on artifact changes at retrospectives.
- **AI assistant** (secondary actor): Consumes improved artifacts, produces better output. May *draft* updates in some workflows, but humans must review.

The Harness Engineering article introduces more agentic actors:
- **Coding agents**: Execute guided by the harness; self-correct via feedback signals.
- **Review agents**: Run automatically; produce computational or inferential signals.
- **CI/Infrastructure**: Distributes sensors; coordinates signal flow.

But in Fowler's framing, agents are *participants in* loops that humans *design and own*. The human decides when a loop should close and what it means.

### Momentum's Framework

Momentum distributes actor roles across humans and agents with explicit authority:

- **Impetus (orchestrator)**: Dispatches all subagents, synthesizes results, presents findings to developer. Never writes files directly — orchestration only.
- **Dev agents** (specialist variants: dev-skills, dev-build, dev-frontend, dev base): Implement stories in isolated worktrees. One per story. Individual spawns, never TeamCreate.
- **AVFL subagents** (Enumerator validators, Adversary validators, Consolidator, Fixer): Run structured multi-lens validation. Enumerators use systematic enumeration; Adversaries use pattern-aware holistic reading. Different models are prescribed per role based on benchmarking.
- **Code-reviewer agents**: Scoped per-story code review after merge.
- **QA Agent, E2E Validator, Architect Guard**: Run in parallel for team review.
- **Retro auditor team** (auditor-human, auditor-execution, auditor-review, documenter): A collaborative TeamCreate team that analyzes session transcripts via SendMessage communication. The only phase that uses TeamCreate rather than individual spawns.
- **Developer** (human): Approves sprint plans, reviews consolidated fix queues, confirms verification checklists, decides fix-vs-defer for each finding. Has explicit consent gates throughout.

The developer's role in Momentum is **decision authority at gates**, not continuous observation. Between gates, the pipeline runs autonomously.

### Comparative Assessment

| | Fowler | Momentum |
|---|---|---|
| Primary actor | Human developer (continuous observer) | Agent pipeline (automated executor) |
| Human role | Observer, signal classifier, artifact updater | Decision authority at gate points |
| Agent role | Tool that produces signals (secondary) | Autonomous executor of quality evaluation |
| Who closes loops | Human (always) | Agent pipeline (primarily), human at gates |
| Inter-agent coordination | Not addressed (Fowler's series is human-AI) | Explicitly designed (spawn registry, TeamCreate for retro) |
| Team lead role | Tech lead gatekeeps artifact changes | Developer approves fix queues and verification checklists |

**Underlying philosophy:** Fowler's framework assumes the bottleneck is individual-to-team knowledge transfer — humans have the insight, but it stays personal. The actors exist to fix that transfer problem. Momentum assumes the bottleneck is execution consistency — quality gates cannot be applied by humans at scale across parallel agent runs. Agents fill the reviewer role.

---

## Dimension 4: Direction of Flow

### Fowler's Framework

Feedback in Fowler's framework flows in a specific direction: **individual experience → shared artifact → next session context**.

The article describes this as: "The next developer to implement an endpoint benefits from that observation without knowing the exchange happened; the authorization check is now part of what the AI verifies from the first pass." [OFFICIAL]

The flow is:
1. Developer session produces friction or learning
2. Developer (or AI draft) proposes artifact update
3. Tech lead approves and commits
4. Updated artifact enters shared context
5. Next session begins with improved priming

This is fundamentally **cumulative and forward-only**: learning flows from execution history into shared infrastructure. There is no feedback path that runs backward from artifact to modify previous work. Context Anchoring adds a second flow: individual feature decisions → feature document → coordination across multiple developers on the same feature.

Encoding Team Standards describes a parallel flow: security incident → gap identified → commit to instruction document → prevention in future sessions. [OFFICIAL]

### Momentum's Framework

Momentum has multiple concurrent feedback flows operating in different directions:

**Inward (quality assessment → fix decisions):**
- AVFL findings → consolidated fix queue → developer approves fix/defer → fix agents apply → selective re-review
- Code review findings → same consolidated queue → same fix/defer decision
- E2E failures → developer decision → targeted fixes → re-run affected validators only

**Upward (findings → spec documents):**
- AVFL or E2E findings → offer to create follow-up backlog stories
- Architecture drift → flag for immediate addressing or deferral
- Sprint planning includes spec impact analysis: story ACs → update architecture.md and prd.md (parallel subagents)

**Backward trace (upstream-fix):**
- Critical finding → `momentum:upstream-fix` traces to root cause in spec, rule, or workflow → fix at source level
- This is the explicit "flywheel" mechanism: "Practice compounds — findings accumulate across stories into a flywheel of systemic improvement." [OFFICIAL — practice-overview.md]

**Retrospective (execution history → backlog):**
- Session transcripts → auditor team analysis → findings document → story stubs proposed to backlog
- This is the closest Momentum gets to Fowler's "individual experience → shared artifact" flow

The Momentum flows are more varied and include **backward propagation** (findings tracing to spec failures, not just forward accumulation). The upstream-fix direction — from symptom to root cause in shared infrastructure — is structurally similar to Fowler's Failure Signal routing, but the mechanism is different: Momentum does it by spawning a tracing agent; Fowler does it by human reflection.

### Comparative Assessment

| | Fowler | Momentum |
|---|---|---|
| Primary direction | Individual → shared (forward accumulation) | Multi-directional: inward (fix), upward (backlog), backward (upstream trace) |
| Feedback target | Shared artifacts (priming docs, commands, playbooks) | Multiple targets: code (fix agents), backlog (story stubs), spec docs (spec impact update), rules (upstream-fix) |
| Retroactive correction | Not addressed | Upstream-fix traces findings to root cause in spec/rule/workflow |
| Cross-session knowledge | Via curated artifact updates | Via retro transcript analysis and story stubs |
| Session-boundary behavior | Developer explicitly updates artifacts at session end | Automated: AVFL and code review run inside the session workflow |

**Underlying philosophy:** Fowler treats each session as a learning unit that produces knowledge to carry forward. The flow is essentially pedagogical — how does the team get smarter? Momentum treats each sprint as an execution unit that produces quality signals requiring remediation. The flows are operational — how does the system converge to passing state?

---

## Dimension 5: Mechanism of Loop Closure

### Fowler's Framework

Fowler describes loop closure as **hybrid**: primarily human-judgment-driven, with agent drafting as an option:

> "Sometimes a developer edits the shared artifact directly, especially when the change requires judgment or careful wording. In other cases, an agent can draft or apply the update as part of the workflow, with a developer reviewing it before it becomes part of the team's shared context." [OFFICIAL]

The article explicitly resists mandatory automation: "I would not make one mechanism mandatory." Human judgment determines what signals warrant capture. The tech lead must ultimately approve.

Encoding Team Standards describes loop closure through the PR process: updates to instruction files go through the same pull request workflow as code changes. "A developer who notices that the generation instruction does not specify the team's new error-handling pattern submits a PR to update it." [OFFICIAL]

Context Anchoring closes loops through a litmus test: "Could I close this conversation right now and start a new one without anxiety?" — a behavioral check that drives documentation of undocumented decisions. [OFFICIAL]

Harness Engineering describes a more automated closure mechanism: "Whenever an issue happens multiple times, the feedforward and feedback controls should be improved." Recurring signals trigger harness refinement, potentially by the developer adjusting linter rules or review agents. The emphasis on "custom linter messages that include instructions" allows agents to self-correct via sensor output without human involvement. [OFFICIAL]

### Momentum's Framework

Momentum's loop closure is **primarily automated, with human gates at decision points**:

**Automated closures (no human decision required):**
- AVFL validation runs and produces findings — autonomous
- Code review runs in parallel for all stories — autonomous
- E2E Validator runs against Gherkin specs — autonomous
- Spec impact analysis updates architecture.md and prd.md — autonomous subagents
- Retrospective transcript extraction runs via DuckDB — autonomous

**Human-gated closures (human decision required):**
- Consolidated fix queue: developer decides fix/defer for each finding
- Verification checklist: developer confirms each Gherkin scenario
- Sprint plan approval: developer approves or modifies before activation
- Push to origin: always requires explicit developer confirmation
- Story stubs from retro: developer approves each proposed stub before backlog write

**Self-correcting loop (AVFL fix loop):**
The AVFL fix loop is autonomous within the pipeline: validate → consolidate → evaluate → fix → re-validate. Iterations continue up to max 4 until score ≥ 95 (CLEAN) or max iterations reached. Human intervention is only triggered at `GATE_FAILED`, `MAX_ITERATIONS_REACHED`, or `CHECKPOINT_WARNING` states.

The upstream-fix skill — when available — closes the causal loop by tracing a finding back to its root in spec or workflow, proposing the fix at that level. This is the only mechanism in either framework that explicitly targets the *upstream cause* rather than the *downstream symptom*.

### Comparative Assessment

| | Fowler | Momentum |
|---|---|---|
| Default closure mode | Human judgment (always involved) | Automated pipeline (human at gates only) |
| Agent role in closure | Optional draft/assist | Primary executor (fix agents, AVFL fixer) |
| Mandatory review | Always (tech lead approves) | Only for fix/defer decisions and push |
| Self-correcting capability | Not present (human must close each loop) | AVFL fix loop runs autonomously to convergence |
| Upstream tracing | Human identifies root cause manually | `momentum:upstream-fix` skill traces causally |
| Artifact update mechanism | PR workflow for instruction files | Story stubs added to backlog; spec docs updated by parallel subagents |

**Underlying philosophy:** Fowler is suspicious of mandatory automation for knowledge capture — it risks producing bureaucratic overhead that gets abandoned. Momentum is suspicious of relying on human judgment for quality consistency across parallel agents — it risks inconsistent enforcement. Both are correct about their respective failure modes.

---

## Structural Comparison Table

| Dimension | Fowler's Feedback Flywheel | Momentum |
|---|---|---|
| **Cadence model** | Social/ceremonial: session, daily, sprint, quarterly | Event-driven: story completion, sprint merge, post-sprint |
| **Fastest loop** | After-session reflection (seconds, human-initiated) | Hook-based pre/post-tool signals (milliseconds, automated) |
| **Slowest loop** | Quarterly artifact review | Retrospective (post-sprint, spans weeks) |
| **Signal types** | Context, Instruction, Workflow, Failure (all about AI interaction quality) | AVFL findings, code review, E2E results, QA, architecture drift, transcript analysis (all about work product quality) |
| **Signal structure** | Informal/human-classified | Mandatory schema with evidence requirement |
| **Primary actor** | Human developer (continuous observer and classifier) | Agent pipeline (AVFL, code-reviewer, E2E, QA, retro auditors) |
| **Human role** | Observer, classifier, updater | Decision authority at consent gates |
| **Direction of flow** | Individual → shared (forward accumulation) | Multi-directional: inward (fix), upward (backlog), backward (upstream trace) |
| **Primary feedback target** | Shared artifacts (priming docs, commands, playbooks) | Code (fix agents), spec docs (spec impact), backlog (story stubs) |
| **Closure mechanism** | Human judgment with optional agent drafting | Automated pipeline with human gates at decision points |
| **Self-correcting capability** | No | Yes — AVFL iterates to convergence autonomously |
| **Upstream causal tracing** | Human reflects manually | `momentum:upstream-fix` traces to root cause in spec/rule/workflow |
| **Missing vs. the other** | No evidence-mandatory findings schema; no E2E pass/fail; no architecture drift signals | No Instruction/Workflow signals; no prompted after-session reflection; no social learning rituals |

---

## Narrative Analysis: The Underlying Philosophical Divide

The deepest difference between the frameworks is their theory of *where quality lives* and *who is responsible for maintaining it*.

**Fowler's theory:** Quality emerges from *shared tacit knowledge made explicit*. Individual developers develop intuitions about how to work effectively with AI; the framework's job is to transfer that intuition into artifacts that benefit everyone. Feedback is the mechanism by which individual insight becomes team capability. The human is irreplaceable in this loop because they are the only entity that can judge whether an observation constitutes genuine team learning vs. a one-off anomaly. The flywheel metaphor refers to the compounding return on having better shared artifacts — "each rotation of the loop leaves the infrastructure a little better prepared for the next." [OFFICIAL]

**Momentum's theory:** Quality emerges from *automated verification at every gate*. Individual agents cannot be trusted to self-verify; the framework's job is to run structured adversarial validation after every significant work unit. Feedback is the mechanism by which defects are caught before they propagate. The agent pipeline is irreplaceable in this loop because no human can consistently apply 4-lens adversarial review across parallel story implementations. The flywheel metaphor refers to the compounding return on having better practice infrastructure — "findings accumulate across stories into a flywheel of systemic improvement." [OFFICIAL — practice-overview.md]

**What each framework is missing:** Fowler's framework produces better *human learning about AI* but has no automated quality gate for work product. A team could follow all four cadences perfectly and still ship code that fails E2E tests, violates architecture decisions, or contains critical security issues — because no structured verification runs automatically. Momentum produces better *verified work product* but accumulates no knowledge about how to work better with AI. A team could run Momentum for a year and never capture that a particular prompt structure produces dramatically better output, because no mechanism captures Instruction or Workflow signals.

**The synthesis point:** The retro workflow is where Momentum most resembles Fowler — it extracts learnings from execution and proposes them as backlog stories. But the retro is a forensic exercise (what went wrong) rather than an improvement exercise (what worked well). Fowler's after-session reflection is the opposite: it looks for what to preserve (Instruction Signals, Workflow Signals) as much as what to fix (Failure Signals). A complete framework would run Momentum's automated quality gates continuously and Fowler's social learning cadences at their natural frequencies — treating them as orthogonal concerns rather than competing approaches.

---

## Sources

### Fowler's Framework [OFFICIAL]
1. Rahul Garg, "Feedback Flywheel," martinfowler.com, 2026-04-08. URL: https://martinfowler.com/articles/reduce-friction-ai/feedback-flywheel.html
2. Rahul Garg, "Encoding Team Standards," martinfowler.com, 2026-03-31. URL: https://martinfowler.com/articles/reduce-friction-ai/encoding-team-standards.html
3. Rahul Garg, "Context Anchoring," martinfowler.com, 2026-03-17. URL: https://martinfowler.com/articles/reduce-friction-ai/context-anchoring.html
4. Birgitta Böckeler, "Harness Engineering for Coding Agent Users," martinfowler.com, 2026-04-02. URL: https://martinfowler.com/articles/harness-engineering.html
5. Tim Cochran, "Maximizing Developer Effectiveness," martinfowler.com. URL: https://martinfowler.com/articles/developer-effectiveness.html
6. Martin Fowler, "Continuous Integration," martinfowler.com. URL: https://martinfowler.com/articles/continuousIntegration.html

### Momentum Framework [OFFICIAL]
7. `skills/momentum/references/practice-overview.md` — The Eight Principles, including Principle 7: "Practice compounds."
8. `skills/momentum/skills/sprint-dev/workflow.md` — 7-phase sprint execution workflow with AVFL, code review, team review.
9. `skills/momentum/skills/sprint-planning/workflow.md` — 8-step sprint planning with AVFL validation and spec impact analysis.
10. `skills/momentum/skills/retro/workflow.md` — 6-phase retro with DuckDB transcript extraction and TeamCreate auditor team.
11. `skills/momentum/skills/avfl/SKILL.md` — AVFL framework: 4 lenses, dual-reviewer design, 4 profiles, evidence requirements.
12. `skills/momentum/skills/upstream-fix/SKILL.md` — Upstream causal tracing skill (stub, planned for Epic 6).
13. `skills/momentum/references/completion-signals.md` — Flywheel integration: critical findings trigger upstream-fix offer.
14. `skills/momentum/skills/impetus/workflow.md` — Impetus orchestrator: hub-and-spoke model.

### Secondary / Corroborating [PRAC]
15. Gemini deep research output, momentum-vs-fowler research directory, 2026-04-10. Note: Gemini analyzed a different "Momentum" implementation (Yegge's tool suite). Fowler analysis is accurate; Momentum-side analysis requires correction. Used only for Fowler article URL discovery.
