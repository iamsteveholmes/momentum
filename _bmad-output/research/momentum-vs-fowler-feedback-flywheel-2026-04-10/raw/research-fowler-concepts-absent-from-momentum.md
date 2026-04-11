---
content_origin: claude-code-subagent
date: 2026-04-10
sub_question: "What concepts in Fowler's Feedback Flywheel are absent or underdeveloped in Momentum's model?"
topic: "Momentum Flywheel vs. Fowler's Feedback Flywheel — Conceptual Comparison"
---

# Fowler Feedback Flywheel Concepts Absent or Underdeveloped in Momentum

## Overview

Fowler's Feedback Flywheel series (specifically Rahul Garg's concluding article published 2026-04-08 at `martinfowler.com/articles/reduce-friction-ai/feedback-flywheel.html`) proposes a structured practice for converting individual AI session learnings into shared team artifacts. This document compares that framework against the actual Momentum codebase — skills, workflows, references, and planning artifacts — to identify gaps.

**Key framing note:** The Gemini-generated research in `gemini-deep-research-output.md` (also in this `raw/` directory) analyzed Steve Yegge's tool-centric "Momentum" (NTM/Beads/CASS) rather than this project. The analysis below is grounded entirely in the actual Momentum codebase at `/Users/steve/projects/momentum`. [OFFICIAL]

---

## Fowler's Core Framework: The Signal-Artifact Loop

The Fowler article identifies a root cause: "Every AI interaction generates signal" that most teams discard. Its proposed remedy is a closed loop: classify the signal, route it to the correct artifact, update that artifact, and fold the update back into future sessions. [OFFICIAL — martinfowler.com/articles/reduce-friction-ai/feedback-flywheel.html]

The framework rests on four interlocking constructs:

1. **Four signal types** — Context, Instruction, Workflow, Failure — each routed to a specific artifact type
2. **Living artifacts** — priming documents, shared commands, team playbooks, guardrails — described as "surfaces that can absorb learning"
3. **Four cadences** — after each session, daily standup, sprint retrospective, periodic review — for structured practice
4. **Outcome metrics** — first-pass acceptance rate, iteration cycles, post-merge rework, principle alignment — replacing vanity speed metrics

What follows is a gap-by-gap analysis of how each Fowler construct maps (or fails to map) onto Momentum.

---

## Gap 1: Signal Classification and Routing

**Fowler's concept:** Fowler defines four distinct signal types with explicit routing rules. Context Signal (missing AI knowledge → priming documents). Instruction Signal (effective phrasings → shared commands). Workflow Signal (task sequencing insights → team playbooks). Failure Signal (root-cause categorized by type: priming gap, command gap, or model boundary → guardrails and documented anti-patterns). [OFFICIAL]

The critical contribution is the routing logic: not all feedback is the same, and different feedback requires different artifact targets. A failure caused by missing context is a different problem — with a different fix — than a failure caused by a poor instruction.

**Momentum's current state — fully absent.**

Momentum's retrospective skill (`skills/momentum/skills/retro/workflow.md`) does classify human-turn signals at sprint close. The auditor-human agent categorizes user messages as corrections, redirections, frustration signals, praise, or decision points. [OFFICIAL] This is the closest analogue to Fowler's signal classification.

However, the mapping is incomplete in two ways. First, Momentum's categories map to *human behavior types* (how the user responded), not to *root cause types* (why the AI generated the wrong output). Fowler's signal taxonomy answers "what needs to change in the artifact ecosystem"; Momentum's taxonomy answers "where did the sprint go poorly for the human." Second, there is no routing step. Retro findings generate story stubs for the backlog — a correct practice — but those stubs are undifferentiated. A priming gap (missing context in a rules file) and a command gap (a poorly crafted agent system prompt) and a model boundary (a capability the AI doesn't have) all feed into the same story stub queue without any classification that would route them to the appropriate artifact type. [OFFICIAL — retro/workflow.md Phase 5]

**Assessment:** Partially present in mechanism (retro audits exist), fully absent in framing (no signal taxonomy, no routing logic).

---

## Gap 2: Artifact Distillation as an Explicit Practice

**Fowler's concept:** Fowler distinguishes between *raw session history* and *distilled knowledge*. Distillation is the act of a human reviewing a session — while the lesson is still fresh — and manually updating a shared artifact: adding a line to a priming document, adding a check to a shared review command, extending an anti-patterns list. The article gives a concrete example: a developer encounters a missing authorization check, fixes it, and adds one line to a learning log that then becomes part of priming context for the next session. [OFFICIAL]

The word "distillation" is deliberate: the output is smaller and higher-concentration than the input. Raw history is noisy; distilled artifacts are actionable. Fowler explicitly warns that without distillation, "intuition remains personal. It does not transfer." [OFFICIAL]

**Momentum's current state — structurally absent as a named practice, partially addressed by incident.**

Momentum has no concept of artifact distillation as a named, practiced step. When a sprint retro identifies a finding — say, "dev agents repeatedly added authorization checks because the rule wasn't in the project's rules file" — the retro creates a story stub to fix it. [OFFICIAL — retro/workflow.md Phase 5] That story then goes through the full create-story → sprint-planning → sprint-dev pipeline before the fix lands in a rules file.

This is distillation via sprint cycle, not distillation as a lightweight, session-adjacent practice. Fowler's model allows distillation to happen *within minutes* of the session ending, before context decays. Momentum's model requires the finding to survive the backlog, sprint planning, and story execution pipeline — a cycle that could take days to weeks.

The `upstream-fix` skill (`skills/momentum/skills/upstream-fix/SKILL.md`) is the closest conceptual match — it traces quality failures upstream to spec, rule, or workflow root cause and proposes fixes at the right level. [OFFICIAL] However, this skill is currently a stub ("Upstream fix skill — full implementation in Story 4.X") and is not yet operational.

The `agent-guidelines` skill (`skills/momentum/skills/agent-guidelines/SKILL.md`) produces rules files and reference docs from stack discovery. [OFFICIAL] This is artifact creation, not artifact distillation from session signals.

**Assessment:** Fully absent as a named, practiced session-level step. The sprint-retro-to-story-stub pipeline is a coarser, slower approximation. `upstream-fix` is the intended placeholder but is not implemented.

---

## Gap 3: Structured Feedback Cadences

**Fowler's concept:** Fowler defines four distinct cadences, matched to different learning timescales: [OFFICIAL]

- **After each session** — a single reflective question: "Did anything happen in this session that should change a shared artifact?" Updates happen immediately, while memory is fresh. Designed to be anchored to existing checkpoints (PR templates, end-of-day closure, standup).
- **Daily standup** — a single query surfaced at standup: "Did anyone learn something with AI yesterday that the rest of us should know?" Rapid spread without new ceremonies.
- **Sprint retrospective** — a dedicated agenda item: what worked, what friction emerged, what will we update? Produces concrete artifact revisions with a designated owner.
- **Periodic review (quarterly minimum)** — audit which artifacts are actually used, which are stale, where gaps remain. The "lightest cadence" — explicitly designed to avoid burdening teams.

These cadences are deliberately nested: the after-session cadence catches individual signals before they decay; the standup cadence spreads individual signals to the team; the retro cadence produces structural artifact revisions; the periodic cadence audits artifact health. Each layer builds on the previous.

**Momentum's current state — only the sprint-retrospective cadence is present; the others are absent.**

Momentum has a sprint retrospective workflow that produces findings and story stubs. [OFFICIAL — retro/workflow.md] This maps to Fowler's third cadence. It is more automated and data-rich than Fowler envisions (DuckDB transcript audit, multi-agent analysis team), but it serves the same function at the sprint boundary.

The other three cadences are absent:

- There is no after-session reflection step in any Momentum workflow. The closest mechanism is the `gate-findings.txt` produced by the PostToolUse lint hook, but this is a quality gate (checking committed code against rules), not a reflection prompt for updating shared artifacts. [OFFICIAL]
- There is no standup integration. Momentum has no concept of a daily ceremony or inter-session knowledge sharing.
- There is no periodic artifact health audit. Momentum's `refine` skill (`skills/momentum/skills/refine/workflow.md`) does planning artifact discovery — comparing the PRD and stories for coverage gaps — but this is a backlog hygiene operation triggered on demand, not a cadenced audit of whether rules files and agent definitions are stale or unused. [OFFICIAL]

**Assessment:** One of four cadences present (sprint retro). Three are fully absent. The gap is most significant at the after-session level, where Fowler argues most signal decay occurs.

---

## Gap 4: The Frustration Loop vs. Collaboration Loop Distinction

**Fowler's concept:** Fowler frames the flywheel's purpose as a transition from a "Frustration Loop" to a "Collaboration Loop." In the Frustration Loop, the AI's first-pass output is frequently wrong, requiring repeated correction cycles. The Frustration Loop is self-reinforcing negatively: each correction session produces no persistent learning, so the same mistakes recur. In the Collaboration Loop, priming documents and shared commands are rich enough that the AI's first-pass acceptance rate is high — developers spend their time directing rather than correcting. [OFFICIAL]

The measurable signal for loop health is the *first-pass acceptance rate* — what fraction of AI-generated output is usable without major revision. Fowler contrasts this against the "speed trap" of measuring lines generated or time to first output. [OFFICIAL]

**Momentum's current state — the concept is present implicitly, absent explicitly.**

Momentum's design philosophy embeds the Collaboration Loop intuition. The practice overview states: "Practice compounds — findings accumulate across stories into a flywheel of systemic improvement." [OFFICIAL — `skills/momentum/references/practice-overview.md`] The AVFL (Adversarial Validate-Fix Loop) runs post-merge to catch quality gaps, and retro findings feed story stubs back into the backlog. The direction of travel — toward fewer corrections per story — is intended.

However, Momentum does not name or measure the Frustration Loop / Collaboration Loop distinction. There is no metric tracked for first-pass acceptance rate, iteration cycles, post-merge rework, or principle alignment. The retro produces findings with qualitative labels (correction, redirection, frustration, praise) but does not aggregate these into a leading indicator of loop health. The AVFL produces findings counts, but these are not trended over time as a sprint-over-sprint indicator. [OFFICIAL]

The retro metrics table captures: user messages analyzed, subagents analyzed, tool errors detected, struggles identified, successes identified, user interventions, cross-cutting patterns. [OFFICIAL — retro/workflow.md Phase 4] None of these map to Fowler's four outcome metrics.

**Assessment:** The directional intent matches Fowler's Collaboration Loop goal. The explicit framing, the measurement framework, and the named distinction between the two loop states are absent.

---

## Gap 5: Human-in-the-Loop Learning Ceremonies

**Fowler's concept:** Fowler's model is fundamentally human-driven at the distillation step. While AI generates code, humans make the judgment call about which session signals represent individual preferences versus team standards. The article frames this as "the team's practices for working with AI mirror how good teams work with each other: share context early, think before coding, make standards explicit, externalize decisions, and learn from each session." [OFFICIAL]

Specific human ceremonies in Fowler's model: the individual developer reflects after each session; the team shares at standup; a designated owner makes final calls on what commits to shared infrastructure at retrospectives; a periodic reviewer audits artifact health. These are human judgment moments, not automated.

**Momentum's current state — human consent is present at gates, human learning ceremonies are absent.**

Momentum enforces human consent at every destructive action gate: merges, pushes, story stub approval in retros, sprint activation. [OFFICIAL — practice-overview.md principle 5: "Consent at every gate"] This is human-in-the-loop in the safety sense.

But Fowler's ceremonies are not safety gates — they are *learning moments*. The distinction matters. Momentum asks the developer "approve these story stubs?" at retro Phase 5. This is consent, not reflection. Fowler's session-end ceremony asks "what should change in our shared artifacts?" — which requires the developer to have been paying attention to friction throughout the session, not just reviewing a list at the end.

There is no after-session learning ceremony in any Momentum workflow. Impetus's session greeting reads sprint state and presents a menu; it does not prompt the developer to reflect on the previous session before beginning the new one. [OFFICIAL — impetus/SKILL.md]

**Assessment:** Human consent at gates is fully present. Human learning ceremonies — reflection, standup sharing, artifact update decisions — are fully absent.

---

## Gap 6: The "Living Artifact" Infrastructure Concept

**Fowler's concept:** Fowler introduces a specific framing for shared artifacts: they are not documentation, they are "surfaces that can absorb learning." This reframes the maintenance obligation. A priming document is not a static reference — it is "living infrastructure" with the same maintenance discipline as a test suite. Artifacts that are not kept current "become liabilities, not assets." The articles emphasize that priming documents and team standards require the same active maintenance discipline as a dependency manifest — they must be kept current as the ecosystem evolves, or they drift into teaching outdated patterns. [OFFICIAL]

This framing produces specific operational commitments: artifacts are reviewed periodically, staleness is tracked, unused artifacts are pruned.

**Momentum's current state — the concept is architecturally implicit, operationally absent.**

Momentum's rules files, agent definitions, and skill SKILL.md files are intended to be updated as the practice evolves. The PRD's edit history tracks spec changes over time. The `refine` skill checks PRD and architecture coverage against the current story backlog. [OFFICIAL — refine/workflow.md]

However, none of this constitutes a living-artifact discipline in Fowler's sense. There is no staleness detection for rules files (only for stories). There is no periodic review cadence that asks "which rules files are actually loaded and used?" or "which agent definitions are stale relative to the stack they serve?" The `agent-guidelines` skill creates guidelines from stack discovery but has no mechanism to detect when they need refreshing. [OFFICIAL]

The `architecture-guard` skill checks sprint changes against architecture decisions [OFFICIAL — architecture-guard/SKILL.md], but this is drift detection (is the code consistent with the spec?), not artifact health monitoring (is the spec itself still accurate?).

**Assessment:** Living artifacts exist as an implicit design intent. The operational discipline — staleness tracking, periodic review, pruning — is absent.

---

## Gap 7: Measurement Framework — First-Pass Acceptance Rate

**Fowler's concept:** Fowler proposes specific leading indicators to measure flywheel effectiveness: first-pass acceptance rate (usable output without major revision), iteration cycles (back-and-forth rounds per task), post-merge rework (fixing after code ships), and principle alignment (output follows team's architectural standards). He explicitly rejects "speed" (lines generated, time to first output) as capturing only volume, not quality. [OFFICIAL]

For teams without formal tracking, Fowler suggests proxy indicators: frequency of "the AI knew exactly what to do" and declining "why did the AI do _that_?" frustrations. He notes "the absence of frustration...is often the most reliable indicator." [OFFICIAL]

**Momentum's current state — fully absent as a tracked metric.**

Momentum tracks no equivalent metrics. The retro aggregates counts (user interventions, errors, struggles, successes) but does not normalize these to a rate or trend them over sprints. There is no "first-pass acceptance rate" equivalent — no measurement of how often a story's dev agent produced merge-ready output versus requiring rework. The AVFL finding count is a proxy for post-merge quality but is not tracked as a sprint-over-sprint trend. [OFFICIAL]

The momentum-tools CLI provides sprint state (stories by status, retro_run_at timestamps) but no quality trend data. [PRAC — inferred from skills/momentum/scripts/ usage in workflow files]

**Assessment:** Fully absent. Momentum measures throughput (stories done per sprint) but not quality trajectory (first-pass rate, rework rate, iteration cycles).

---

## Gap 8: The "Design-First Collaboration" Pattern

**Fowler's concept:** One of the five patterns in the Fowler series is Design-First Collaboration — the practice of walking the AI through progressive design levels (capabilities, interactions, contracts) before generation begins. The pattern mirrors "whiteboarding" before coding: ensure the AI understands the "why" before generating the "how." This produces output more aligned with architectural intent, reducing the need for post-generation correction. [OFFICIAL — documented in research-fowler-feedback-flywheel.md, Pattern 2, from the primary Garg article at martinfowler.com/articles/reduce-friction-ai/design-first-collaboration.html]

**Momentum's current state — partially present via Gherkin specs, absent as a pre-generation practice.**

Momentum's sprint-planning skill generates Gherkin specs before dev agents begin implementation. Dev agents implement against plain English ACs and are explicitly barred from reading Gherkin specs (black-box separation). [OFFICIAL — sprint-planning/workflow.md, sprint-dev/workflow.md critical directives] The Gherkin generation step is a design artifact, but it is created for verifier agents, not as a collaborative design session with the dev agent.

The create-story skill produces Momentum Implementation Guides injected into story files — pre-generation context for dev agents. [OFFICIAL — dev/workflow.md] This is closer to Knowledge Priming (another Fowler pattern) than Design-First Collaboration.

There is no step in any Momentum workflow that mirrors the progressive design walkthrough: capability level → interaction level → contract level → implementation. Story ACs are written in plain English but not structured as a progressive design conversation between the developer and an AI agent.

**Assessment:** Partially addressed by Gherkin generation (design artifact exists pre-dev), but the collaborative design conversation pattern — where the AI participates in progressively elaborating the design before coding — is absent.

---

## Synthesis: Priority Ranking of Gaps for Adoption

Based on evidence quality and structural fit with Momentum's existing model, the gaps rank as follows for adoption priority:

**Highest priority — low implementation cost, high leverage:**

1. **After-session reflection trigger** — A single question surfaced at Impetus session open ("In the last session, did any AI output require repeated correction on the same issue? If so, which rules file or agent definition should change?") would operationalize Fowler's highest-frequency cadence. Implementation cost: one Impetus workflow step. [PRAC]

2. **Signal classification in retro stubs** — Tagging retro-generated story stubs with Fowler's four signal types (Context / Instruction / Workflow / Failure) and the corresponding artifact type to update would add routing logic to an existing mechanism without redesigning it. [PRAC]

**Medium priority — requires new infrastructure:**

3. **Artifact staleness tracking** — A periodic `refine` check that reviews rules files for evidence of actual loading and use (e.g., checking `.claude/rules/` file mtime against session dates) would operationalize the living-artifact discipline. [PRAC]

4. **Sprint-over-sprint quality metrics** — Adding first-pass acceptance rate (stories needing zero AVFL findings) and user-intervention rate (retro user_msg_count normalized to story count) to the retro output would enable trend detection. [PRAC]

**Lower priority — requires significant design work:**

5. **Standup integration** — Momentum is a solo-developer tool in its current form. Daily standup integration requires a multi-developer model not yet in the architecture. [OFFICIAL — practice-overview.md framing as solo-dev practice]

6. **Design-First Collaboration pattern** — Restructuring story ACs as progressive design conversations would require rethinking the create-story and sprint-planning workflows substantially.

---

## Sources

**Primary sources — direct inspection:**

- [OFFICIAL] `martinfowler.com/articles/reduce-friction-ai/feedback-flywheel.html` — Rahul Garg, 2026-04-08. Fetched directly via WebFetch during this research session.
- [OFFICIAL] `/Users/steve/projects/momentum/skills/momentum/skills/retro/workflow.md` — Retro workflow, Phase 4 (auditor team) and Phase 5 (story stubs)
- [OFFICIAL] `/Users/steve/projects/momentum/skills/momentum/skills/impetus/SKILL.md` — Impetus orchestrator, session greeting logic
- [OFFICIAL] `/Users/steve/projects/momentum/skills/momentum/skills/refine/workflow.md` — Refine backlog hygiene workflow
- [OFFICIAL] `/Users/steve/projects/momentum/skills/momentum/skills/sprint-planning/workflow.md` — Sprint planning, Gherkin spec generation
- [OFFICIAL] `/Users/steve/projects/momentum/skills/momentum/skills/sprint-dev/workflow.md` — Sprint execution, AVFL stop gate
- [OFFICIAL] `/Users/steve/projects/momentum/skills/momentum/skills/upstream-fix/SKILL.md` — Upstream fix stub
- [OFFICIAL] `/Users/steve/projects/momentum/skills/momentum/skills/architecture-guard/SKILL.md` — Architecture drift detection
- [OFFICIAL] `/Users/steve/projects/momentum/skills/momentum/references/practice-overview.md` — Eight principles, flywheel principle 7

**Secondary sources — prior research:**

- [PRAC] `/Users/steve/projects/momentum/_bmad-output/research/momentum-vs-fowler-feedback-flywheel-2026-04-10/raw/gemini-deep-research-output.md` — Gemini deep research output. Note: Gemini analyzed Steve Yegge's tool-centric "Momentum" (NTM/Beads/CASS), not this project. The Fowler analysis sections are accurate and were used as corroborating context; the Momentum-side analysis was not used as it describes a different product.
