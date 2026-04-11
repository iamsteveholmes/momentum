---
title: "Momentum Flywheel vs. Fowler's Feedback Flywheel — Research Report"
date: 2026-04-10
type: Technical Research — Consolidated Report
status: Complete
content_origin: claude-code-synthesis
human_verified: true
gemini_note: "Gemini output quarantined — analyzed Steve Yegge's Momentum, not this project. Fowler analysis from Gemini usable; Momentum analysis discarded."
derives_from:
  - path: raw/research-momentum-flywheel-definition.md
    relationship: synthesized_from
  - path: raw/research-fowler-feedback-flywheel.md
    relationship: synthesized_from
  - path: raw/research-fowler-concepts-absent-from-momentum.md
    relationship: synthesized_from
  - path: raw/research-momentum-concepts-absent-from-fowler.md
    relationship: synthesized_from
  - path: raw/research-feedback-loop-framing.md
    relationship: synthesized_from
  - path: raw/research-adoption-candidates.md
    relationship: synthesized_from
  - path: validation/avfl-report.md
    relationship: validated_by
  - path: raw/practitioner-notes.md
    relationship: informed_by
---

# Momentum Flywheel vs. Fowler's Feedback Flywheel — Research Report

## Executive Summary

Momentum and Fowler's Feedback Flywheel both use the flywheel metaphor to describe self-reinforcing improvement cycles in AI-assisted software development, but they operate at fundamentally different layers. Momentum is an agentic engineering practice module — a deployed, executable harness of skills, agents, hooks, and workflows that automates the development lifecycle. Its flywheel, formally named "Practice compounds" (principle #7 of 8 in the practice overview), traces quality failures upstream through a structured hierarchy to fix the process that produced the defect, not just the defect itself. Fowler's Feedback Flywheel, authored by Rahul Garg as the fifth article in a five-part series on martinfowler.com, describes the social and procedural practice of harvesting signals from AI sessions and routing them back into shared team artifacts.

The core philosophical difference: Fowler treats feedback loops as human social processes that happen to involve AI tools. Momentum treats them as engineered quality pipelines that happen to involve human checkpoints. Fowler's signals are epistemological — what did we learn about working with AI? Momentum's signals are forensic — what defects exist in the work product?

This comparison identified eight Fowler concepts absent or underdeveloped in Momentum and ten Momentum concepts absent from Fowler. The gap is not symmetric: Fowler's missing concepts represent lightweight practice improvements that Momentum could adopt incrementally, while Momentum's missing concepts represent architectural capabilities that Fowler's advisory framing does not attempt to provide. The three highest-value adoption candidates are: (1) signal classification and routing — adding a typed taxonomy to retro findings so they route to specific artifact destinations (score 18/20), (2) artifact distillation — a lightweight path from session learning to immediate artifact update that bypasses the sprint queue (16/20), and (3) structured feedback cadences — a per-session reflection prompt in the Impetus greeting to capture signals before they decay (14/20).

## 1. Momentum's Flywheel: How It Is Defined and Implemented

Momentum's flywheel concept appears in two source documents with different framings. The product brief (committed 2026-03-16) names it the "Evaluation Flywheel" — principle #4 of 7 — with a narrower defect-tracing focus: "When output fails quality standards, trace the failure upstream. Don't fix the code — fix the workflow, specification, or rule that caused the defect." [VERIFIED — `_bmad-output/planning-artifacts/product-brief-momentum-2026-03-13.md`]

The practice overview (last updated 2026-04-04) evolves this into principle #7 of 8: "Practice compounds — findings accumulate across stories into a flywheel of systemic improvement." [VERIFIED — `skills/momentum/references/practice-overview.md`] This is the authoritative current framing: it broadens the concept from defect tracing to systemic cross-story improvement. The practice overview is the live installed reference in the plugin, while the product brief is a historical planning artifact.

### The Upstream Trace Hierarchy

The flywheel operates through a five-level upstream trace. When a quality failure is detected, the fix is sought at the highest applicable level [VERIFIED — `docs/planning-artifacts/AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md`, Section 4.3]:

1. **Spec-generating workflow gap** — the workflow that produces stories failed to generate sufficient context. Fix the workflow; every future story improves. Highest-value fix.
2. **Specification gap** — the PRD, architecture doc, or story ACs were incomplete for this case. Fix the spec.
3. **CLAUDE.md / .claude/rules/ gap** — the AI deviated from a universal standard. Add the rule.
4. **Tooling gap** — something advisory should be deterministic. Add a hook, lint rule, or architectural test.
5. **One-off error** — fix the code. Least valuable fix.

This hierarchy is explicitly traced to Deming's "fix the process, not the defect." The planning document cites three independent prior implementations as intellectual precursors: OpenAI's Evaluation Flywheel, NVIDIA's Data Flywheel, and Stanford's DSPy. [VERIFIED]

### Three Operating Cadences

The flywheel operates at three cadences [VERIFIED — planning document Section 5.5]:

- **Per-session (immediate):** failures trigger explicit dialogue — the agent surfaces the failure and asks whether it is a CLAUDE.md gap, a missing rule, or a one-off.
- **Per-story (sprint cadence):** code review findings trigger the full upstream trace. The findings ledger activates here.
- **Per-sprint (retrospective):** the retro asks whether stories arrived at implementation with missing context. Workflow modifications, rule amendments, and process tasks flow from here.

### The Findings Ledger

The findings ledger is a global JSONL append-only store (`~/.claude/momentum/findings-ledger.jsonl`) designed to make the flywheel function across sessions. It captures findings with fields for pattern tags, upstream fix level, and provenance status. The retrospective reads it and groups findings by category to surface cross-story patterns. [VERIFIED — PRD functional requirements FR28-FR33]

### Implementation Status (2026-04-10)

The sprint lifecycle, AVFL, code review, architecture guard, and retro are implemented. The `upstream-fix` skill is a stub ("full implementation in Story 4.X"). The findings ledger infrastructure and cross-story pattern detection are defined in Epic 6 ("Practice Compounds") with backlog stubs but no story files. In the absence of `upstream-fix`, Impetus includes a deferral note: "flywheel processing deferred — Epic 6." [VERIFIED]

### What Makes It Self-Reinforcing

The reinforcing loop: governing artifacts guide AI generation; multi-layer verification surfaces findings; upstream trace attributes findings to the workflow, spec, or rule that produced the defect; fixes improve governing artifacts; improved artifacts guide the next generation cycle. The PRD states: "The system gets smarter every sprint — not because the AI improves, but because the practice around it compounds." [VERIFIED]

Provenance is called "load-bearing infrastructure that enables the flywheel" — `derives_from` frontmatter, content hashes via `git hash-object`, and one-hop propagation ensure that flywheel fixes propagate through the document chain rather than silently consuming stale versions. [VERIFIED]

## 2. Fowler's Feedback Flywheel: Core Components and Framing

The "Feedback Flywheel" is the fifth and culminating article in a five-part series titled "Patterns for Reducing Friction in AI-Assisted Development" published on martinfowler.com between February and April 2026. [VERIFIED — https://martinfowler.com/articles/reduce-friction-ai/]

**Author:** Rahul Garg, Principal Engineer at Thoughtworks. Martin Fowler hosts the series; Garg is the sole credited author of all five articles. The articles are: Knowledge Priming (24 Feb), Design-First Collaboration (3 Mar), Context Anchoring (17 Mar), Encoding Team Standards (31 Mar), and Feedback Flywheel (8 Apr).

**Supplementary source (not part of the series):** Birgitta Bockeler's "Harness Engineering for Coding Agent Users" (martinfowler.com, 2 Apr 2026) is a separate standalone article that provides complementary technical context on guides and sensors for coding agents. It is referenced in this report where it adds relevant context but is not counted as part of Garg's series for gap analysis. It is a candidate for follow-on research focused on harness engineering specifically.

### The Frustration Loop

The series opens with a central failure mode: the AI produces syntactically correct code that follows generic internet patterns rather than project-specific conventions. The developer corrects it. The cycle repeats. "The time saved by AI-generated code is often consumed by the effort required to correct it." [VERIFIED] The five patterns collectively aim to transform this into a state where shared context infrastructure produces aligned output and fewer correction passes — what the series frames as the desired end state. [INFERRED — "Collaboration Loop" is an analytical synthesis of the series framing; the exact term is not formally defined in the articles]

### The Five Patterns

1. **Knowledge Priming** — share curated project context (tech stack, conventions, anti-patterns) before generation begins. "Manual RAG" that overrides training-data defaults. Priming documents are versioned repository artifacts, not personal habits.
2. **Design-First Collaboration** — walk AI through progressive design levels (capabilities, components, interactions, contracts, implementation) before any code generation. "No code until Level 5 is approved."
3. **Context Anchoring** — maintain a two-layer context strategy: stable priming documents for project context, living feature documents for per-feature decisions. The litmus test: "If you can close a chat session and start fresh without anxiety, context is properly anchored."
4. **Encoding Team Standards** — convert senior engineers' tacit knowledge into versioned, executable instruction sets in repositories. Two moves: tacit to explicit, documentation to execution. "The governance is the workflow."
5. **Feedback Flywheel** — the meta-pattern that maintains all others. Harvest learnings from AI sessions, classify them by signal type, route them to the correct artifact, and iterate.

### Signal Taxonomy

Garg defines four signal types with explicit routing [VERIFIED]:

| Signal Type | Definition | Improvement Target |
|---|---|---|
| Context Signal | Gaps in project knowledge the AI needed but lacked | Priming documents |
| Instruction Signal | Prompts/phrasings that produced better or worse results | Shared commands / prompt templates |
| Workflow Signal | Interaction sequences that reliably succeed | Design-first playbooks |
| Failure Signal | Errors with identified root causes | Guardrails and anti-pattern docs |

The critical contribution is that different signal types require different artifact targets. A failure caused by missing context is a different problem — with a different fix — than a failure caused by a poor instruction.

### Four Cadences

The feedback practice operates at four timeframes [VERIFIED]:

- **After each session** — "Did anything happen that should change a shared artifact?" Seconds to reflect, minutes to act.
- **Daily standup** — "Did anyone learn something with the AI yesterday that the rest of us should know?"
- **Sprint retrospective** — dedicated agenda item producing concrete artifact revisions.
- **Periodic review (quarterly)** — audit artifact currency and usage.

Design principle: "If the practice requires its own meeting, it will be the first thing cut when the team is busy."

### Metrics

Garg distinguishes misleading speed metrics (lines generated, time to first output) from informative quality metrics: first-pass acceptance rate, iteration cycles per task, post-merge rework, and principle alignment. He acknowledges "these metrics are difficult to track rigorously" and suggests a qualitative proxy: "the absence of frustration — the declining frequency of 'why did the AI do that?'" [VERIFIED]

## 3. What Fowler Has That Momentum Lacks

Eight concepts from Garg's series are absent or underdeveloped in Momentum. These are ordered by adoption priority (highest first).

### 3.1 Signal Classification and Routing

**Fowler's concept:** Four typed signal categories with explicit routing rules that map each signal to a specific artifact destination. Without routing, all feedback collapses into undifferentiated notes. [VERIFIED]

**Momentum's state:** The retro workflow classifies human-turn signals (corrections, redirections, frustration, praise, decisions), but these categories map to human behavior types, not root cause types. A priming gap and a command gap feed the same story stub queue without classification that would route them to the appropriate artifact. [VERIFIED — `retro/workflow.md` Phase 5]

**Assessment:** Partially present in mechanism (retro audits exist), fully absent in framing (no signal taxonomy, no routing logic).

### 3.2 Artifact Distillation as an Explicit Practice

**Fowler's concept:** Distillation is the act of reviewing a session and updating a shared artifact immediately — while the lesson is fresh. The output is smaller and higher-concentration than the input. "Intuition remains personal. It does not transfer." [VERIFIED]

**Momentum's state:** When a retro identifies a finding, it creates a story stub that goes through the full sprint pipeline before landing in a rules file. This is distillation via sprint cycle, not distillation as a lightweight session-adjacent practice. The `upstream-fix` skill is the intended fast path but is not yet implemented. [VERIFIED]

**Assessment:** Structurally absent as a named, practiced session-level step. The sprint pipeline is a coarser, slower approximation.

### 3.3 Structured Feedback Cadences (Three of Four)

**Fowler's concept:** Four nested cadences — after-session, daily standup, sprint retro, quarterly review. [VERIFIED]

**Momentum's state:** Only the sprint retrospective cadence is present. There is no after-session reflection, no standup integration, and no periodic artifact health audit. The gap is most significant at the after-session level, where most signal decay occurs. [VERIFIED]

**Assessment:** One of four cadences present.

### 3.4 First-Pass Acceptance Rate and Quality Metrics

**Fowler's concept:** Leading indicators — first-pass acceptance rate, iteration cycles, post-merge rework, principle alignment — replacing vanity speed metrics. [VERIFIED]

**Momentum's state:** No equivalent metrics are tracked. The retro aggregates counts (interventions, errors, struggles) but does not normalize them to rates or trend them over sprints. [VERIFIED]

**Assessment:** Fully absent.

### 3.5 The Frustration Loop / Collaboration Loop Framing

**Fowler's concept:** Named distinction between two system states — frustration (generate-correct-repeat without learning) vs. collaboration (shared infrastructure produces aligned output). The first-pass acceptance rate is the measurable signal for loop health. [VERIFIED]

**Momentum's state:** The directional intent matches. The explicit framing, measurement framework, and named distinction are absent. [VERIFIED]

### 3.6 Human-in-the-Loop Learning Ceremonies

**Fowler's concept:** Ceremonies where humans reflect on what they learned — not safety gates, but learning moments. The after-session ceremony asks "what should change in our shared artifacts?" [VERIFIED]

**Momentum's state:** Human consent at gates is fully present. Human learning ceremonies — reflection, sharing, artifact update decisions — are absent. Impetus's session greeting presents sprint state; it does not prompt reflection on the previous session. [VERIFIED]

### 3.7 Living Artifact Maintenance Discipline

**Fowler's concept:** Shared artifacts as "surfaces that can absorb learning" requiring the same maintenance discipline as test suites. Staleness tracking, periodic review, pruning. [VERIFIED]

**Momentum's state:** Architecturally implicit (rules files are intended to evolve), operationally absent (no staleness detection for rules files, no periodic review cadence for artifact health). [VERIFIED]

### 3.8 Design-First Collaboration as Pre-Generation Practice

**Fowler's concept:** Progressive design walkthrough (capabilities, components, interactions, contracts) before any code generation. The AI participates in elaborating the design. [VERIFIED]

**Momentum's state:** Partially addressed by Gherkin generation (design artifact exists pre-dev), but Gherkin specs are created for verifier agents, not as a collaborative design session with the dev agent. The progressive design conversation pattern is absent. [VERIFIED]

## 4. What Momentum Has That Fowler Lacks

Ten Momentum concepts have no substantive treatment in Garg's series. Bockeler's "Harness Engineering" article is referenced where it identifies the category without providing the mechanism.

### 4.1 Adversarial Multi-Agent Validation Pipeline (AVFL)

Momentum's AVFL runs parallel reviewer subagents with different reading styles (Enumerator: systematic; Adversary: pattern-aware holistic), consolidates findings with cross-reviewer confidence scoring (HIGH when both find it), iterates fix cycles to convergence (score >= 95/100), and selects profiles by artifact maturity. Benchmarked across 36 runs. [VERIFIED — `avfl/SKILL.md`]

Garg identifies "Failure Signal" as a category routed to guardrails. Bockeler identifies "sensors" including code review agents. Neither describes a formal pipeline with reviewer diversity, convergence thresholds, or skepticism calibration. [CITED]

### 4.2 Dependency-Driven Story Spawning with Worktree Isolation

Sprint execution builds a dependency graph from story metadata, spawns dev agents only for unblocked stories, runs each in an isolated git worktree, and coordinates wave-structured parallel merge sequencing. [VERIFIED — `sprint-dev/workflow.md`]

Garg's framework is session-scoped (one developer, one AI). Sprint-scope orchestration with dependency graphs is absent. [CITED]

### 4.3 Transcript Audit as Retrospective Data Source

The retro spawns a four-agent collaborative team (3 auditors + 1 documenter via TeamCreate) against DuckDB transcript extracts. Auditors specialize in different analytical lenses (human behavior, execution patterns, review quality). Findings are structured with severity, evidence, and source attribution. [VERIFIED — `retro/workflow.md`]

Garg describes retrospectives as team ceremonies with qualitative discussion outputs. Machine-readable sprint history as primary retro input is not addressed. [CITED]

### 4.4 Eval-Driven Skill Development (EDD)

Skills are validated by behavioral evals, not unit tests. Each skill directory contains an `evals/` subdirectory. AVFL's role configuration was derived from 36 benchmark runs with specific model-role combinations prohibited based on measured failure modes. [VERIFIED — `practice-overview.md`, `avfl/SKILL.md`]

Garg and Bockeler describe standards as things to share and version. Behavioral evaluation for the skills themselves — how do you know your AI instructions actually work? — is absent. [CITED]

### 4.5 Orchestrator Purity and Spawning Discipline

Impetus dispatches to skills and agents but never performs dev, validation, or test work directly. The spawning pattern (fan-out vs. TeamCreate) is a documented design decision with explicit guidance on when each applies. [VERIFIED — `architecture-guard/SKILL.md`, `~/.claude/rules/spawning-patterns.md`]

Bockeler's harness model is human-and-one-agent. Multi-agent composition rules, orchestrator purity, and spawn registry deduplication have no analogues. [CITED]

### 4.6 File-System Enforcement via PreToolUse/PostToolUse Hooks

PreToolUse hooks block writes to protected paths before they execute. PostToolUse hooks run lint/format on modified files. The agent literally cannot write to protected paths at the Claude Code runtime level. [VERIFIED — `hooks/hooks.json`, `references/hooks/file-protection.sh`]

Garg routes to "guardrails." Bockeler identifies "guides" that anticipate behavior before action. Neither describes runtime enforcement at the tool-use layer. [CITED]

### 4.7 Model Routing by Cognitive Hazard

Momentum assigns models to roles based on measured failure mode risk. Verifier roles use Opus ("cognitive hazard rule — verifier"). AVFL's Adversary uses Opus/high for severity calibration. Enumerator uses Sonnet/medium because Haiku produces false-pass scores. [VERIFIED — `avfl/SKILL.md`, `references/model-routing-guide.md`]

Garg's and Bockeler's frameworks are model-agnostic. Role-to-model assignment based on failure mode risk is absent. [CITED]

### 4.8 Gherkin-Based Black-Box Verification

Sprint planning generates Gherkin `.feature` files. Dev agents are architecturally prohibited from reading them (Decision 30: black-box separation, enforced by file-protection hooks). E2E validators test running behavior against Gherkin scenarios without source code access. [VERIFIED — `sprint-dev/workflow.md`, `references/gherkin-template.md`]

Bockeler acknowledges behavioral correctness as the hardest harness dimension but provides no mechanism. Spec-to-verification pipeline with enforced implementer/verifier ignorance is novel. [CITED]

### 4.9 Architecture Drift Detection as Sprint Gate

Architecture Guard is a read-only agent that checks sprint changes against documented architecture decisions, produces a severity-tagged verdict, and gates sprint completion (FAIL = any CRITICAL or 3+ HIGH findings). [VERIFIED — `architecture-guard/SKILL.md`]

Bockeler identifies "continuous drift detection" as emergent. Garg routes failure signal to "architectural guardrails." Neither provides a concrete blocking gate. [CITED]

### 4.10 Automated Story Staleness Detection via Git

Sprint planning checks candidate stories against recent git history (`git log --since='30 days ago' -- touches_paths`). Stories with recent commits to their touch paths are flagged as potentially stale before inclusion. [VERIFIED — `sprint-planning/workflow.md`]

Garg addresses priming document staleness relative to the codebase. Automated story staleness detection before sprint inclusion is absent. [CITED]

## 5. How the Two Frameworks Frame Feedback Loops Differently

### Structural Comparison

| Dimension | Fowler's Feedback Flywheel | Momentum |
|---|---|---|
| **Cadence model** | Social/ceremonial: session, daily, sprint, quarterly | Event-driven: story completion, sprint merge, post-sprint retro |
| **Fastest loop** | After-session reflection (seconds, human-initiated) | Hook-based pre/post-tool invocations (milliseconds, automated) |
| **Slowest loop** | Quarterly artifact review | Retrospective (post-sprint) |
| **Signal types** | Context, Instruction, Workflow, Failure (AI interaction quality) | AVFL findings, code review, E2E results, architecture drift, transcript analysis (work product quality) |
| **Signal structure** | Informal, human-classified | Mandatory schema with evidence requirement |
| **Signal orientation** | Epistemological: what did we learn about working with AI? | Forensic: what defects exist in the work product? |
| **Primary actor** | Human developer (continuous observer) | Agent pipeline (automated executor) |
| **Human role** | Observer, classifier, artifact updater | Decision authority at consent gates |
| **Direction of flow** | Individual experience -> shared artifact (forward accumulation) | Multi-directional: inward (fix), upward (backlog), backward (upstream trace) |
| **Closure mechanism** | Human judgment with optional agent drafting | Automated pipeline with human gates at decision points |
| **Self-correcting capability** | Not present | AVFL iterates to convergence autonomously |
| **Upstream causal tracing** | Human reflects manually | `upstream-fix` traces to root cause in spec/rule/workflow |

### Signal Type Comparison

| | Fowler Captures | Momentum Captures |
|---|---|---|
| **What worked well** | Instruction Signal, Workflow Signal | Not captured |
| **What the AI lacked** | Context Signal | Architecture drift (against documented decisions) |
| **What the code got wrong** | Failure Signal (human-classified) | AVFL findings, code review, E2E pass/fail (agent-classified, evidence-mandatory) |
| **What the human experienced** | After-session reflection | Transcript audit (retro auditor-human agent) |
| **Cross-story patterns** | Sprint retro discussion | Findings ledger + pattern detection (planned, Epic 6) |

### The Philosophical Divide

Fowler's theory: quality emerges from shared tacit knowledge made explicit. The human is irreplaceable because only humans can judge whether an observation constitutes team learning vs. a one-off anomaly. The flywheel compounds by producing better shared artifacts.

Momentum's theory: quality emerges from automated verification at every gate. Agent pipelines are irreplaceable because no human can consistently apply 4-lens adversarial review across parallel story implementations. The flywheel compounds by producing better practice infrastructure.

What each framework is missing: Fowler has no automated quality gate for work product. A team could follow all four cadences and still ship code that violates architecture decisions — because no structured verification runs automatically. Momentum accumulates no knowledge about how to work better with AI. A team could run Momentum for a year and never capture that a particular prompt structure produces dramatically better output — because no mechanism captures Instruction or Workflow signals.

A complete framework would run Momentum's automated quality gates continuously and Fowler's social learning cadences at their natural frequencies, treating them as orthogonal concerns.

## 6. Adoption Candidates: Highest-Value Fowler Concepts for Momentum

### Scoring Framework

Each concept scored on four dimensions (1-5, 5 = highest): Impact (how much it improves quality/velocity/learning), Fit (how cleanly it maps to existing patterns), Effort (inverse of implementation cost), Risk (inverse of overhead risk). Priority score = sum (max 20).

### Candidate 1: Signal Classification and Routing — Score 18/20

**What to adopt:** Add Fowler's four-type signal taxonomy (Context / Instruction / Workflow / Failure) as a classification layer on retro findings, with routing logic that maps each type to a specific artifact destination.

**Why it matters:** Without routing, captured signals evaporate into undifferentiated story stubs. This is the mechanism that transforms raw findings into directed artifact improvement. It directly enables the "Practice compounds" principle by telling the system which artifact needs the fix.

**Implementation sketch:**
- Extend the `auditor-human` prompt in `retro/workflow.md` to classify each finding with `signal_type` and `destination` fields
- Complete `upstream-fix` (Story 4.X) to route classified signals: context signals to CLAUDE.md, instruction signals to skill references, workflow signals to workflow steps, failure signals to anti-pattern rules
- Minimal starting point: add a `signal_type` column to the retro findings "Priority Action Items" table — one field per finding, seeding the routing data without requiring the full upstream-fix skill

**Scores:** Impact 5, Fit 5, Effort 4, Risk 4.

### Candidate 2: Artifact Distillation — Score 16/20

**What to adopt:** A lightweight path from session learning to immediate artifact update that bypasses the sprint queue for small, low-risk changes.

**Why it matters:** The retro-to-backlog path requires findings to survive sprint planning, story selection, and development before they reach the rules or skill files that future sessions consume. This can take weeks. Fowler's model allows distillation in minutes. The critical gap: Momentum has no mechanism for small, immediate updates — the kind that take minutes of effort.

**Implementation sketch:**
- New skill `momentum:distill`: takes retro findings and proposes immediate updates to rules files and references as git diff proposals
- Two tiers: Tier 1 (immediate) for small rule additions and anti-patterns that commit directly; Tier 2 (sprint-queued) for structural workflow changes
- Integration: retro Phase 5 presents an additional question after story stub approval: "Propose immediate rule/reference updates from these findings?"
- Minimal starting point: add a `## Proposed Immediate Updates` text section to retro Phase 5 output — proposals only, no file writes, for developer review

**Scores:** Impact 5, Fit 4, Effort 3, Risk 4.

### Candidate 3: Structured Feedback Cadences — Score 14/20

**What to adopt:** A per-session reflection prompt in the Impetus greeting to capture signals before they decay between sprints.

**Why it matters:** The after-session cadence is where most signal decay occurs. Between retros, individual session learnings evaporate. A single reflection prompt at session start closes this gap.

**Implementation sketch:**
- Extend Impetus preflight to occasionally append: "Last session, did anything make you correct the agent mid-task? If yes, `intake` it now."
- Zero overhead for uneventful sessions (developer says "no"). Routes notable events to `momentum:intake` in one step.
- Optional: add a `daily-captures.md` append-only file to sprint logs that retro Phase 2 includes in DuckDB extraction
- Important adaptation: Fowler's daily standup assumes a team. In Momentum's solo-dev context, the reflection must be opt-in and lightweight. Unsolicited structured check-ins become abandoned overhead quickly.

**Scores:** Impact 4, Fit 3, Effort 4, Risk 3.

### Candidate 4: Team Standard Encoding Anatomy — Score 13/20

**What to adopt:** Fowler's four-element instruction anatomy (role definition, context requirements, categorized standards, output format) as a uniform checklist for Momentum skill system prompts.

**Why it matters:** Momentum already covers most of this territory with `agent-guidelines` and AVFL dimensions. The gap is in uniform application — some skills lack explicit mandatory/recommended/optional categorization and output format specifications.

**Minimal starting point:** Add the four-element anatomy as a checklist to `references/agent-skill-development-guide.md`. New skills get reviewed against it automatically.

**Scores:** Impact 3, Fit 4, Effort 3, Risk 3.

### Candidate 5: Frustration Loop Tracking — Score 12/20

**What to adopt:** Sprint-over-sprint quality trend metrics — first-pass acceptance rate, correction count, iteration cycles — computed at retro and trended across sprints.

**Why it matters:** Trend data identifies highest-ROI improvement targets. Currently invisible: no metric persists across sprints to show quality trajectory.

**Implementation sketch:**
- Add a `metrics.json` to each sprint directory at close time, populated by the retro documenter
- Fields: `frustration_signals`, `corrections`, `first_pass_acceptance_rate` (stories with zero AVFL findings / total stories), `tool_errors`
- Impetus greeting displays worsening trends as friction alerts
- Minimal starting point: standardize field names in the existing retro metrics table so they are machine-readable by a future aggregation step

**Scores:** Impact 4, Fit 3, Effort 2, Risk 3.

## Cross-Cutting Themes

### Advisory vs. Operational

The deepest structural difference is not what each framework addresses but how. Garg describes what teams should practice. Momentum implements it as executable workflow. This is why Fowler's gaps in Momentum tend to be practice-layer concerns (reflection, distillation, cadences) while Momentum's gaps in Fowler tend to be infrastructure concerns (AVFL, worktree isolation, hooks, model routing). The two are complementary, not competing.

### The Missing Middle: Instruction and Workflow Signals

Momentum's signal capture is entirely output-oriented — what did the code get wrong? Fowler's Instruction Signal and Workflow Signal capture what went right: which prompts produced excellent results, which task decompositions succeeded. Momentum has no mechanism for this positive-signal capture. This is the single most structurally important gap because the flywheel's compounding mechanism depends not just on fixing failures but on amplifying successes.

### Solo-Dev Adaptation

Garg's framework assumes a team (5-15+ developers). Momentum operates primarily as a solo-developer practice. Three of Garg's four cadences assume social ceremonies (standup, retro discussion, periodic team review). Adapting these to solo context requires replacing social mechanisms with automated prompts — the principle survives the adaptation, but the ceremony does not.

### Foundational Infrastructure Already in Place

Momentum has already built Garg's first four patterns in substance: Knowledge Priming (CLAUDE.md, rules cascade), Design-First Collaboration (story/epic/spec structure), Context Anchoring (sprint logs, decision records), and Encoding Team Standards (AVFL, agent-guidelines). Momentum is positioned to adopt the Feedback Flywheel layer directly rather than building prerequisites. This makes the adoption candidates actionable in the near term.

### The Speed of the Loop Matters

Fowler argues that the after-session cadence prevents the most signal decay. Momentum's fastest learning loop is the sprint retro — which can lag days or weeks behind the session where the signal originated. Closing this temporal gap (via Candidate 3: per-session reflection) may deliver disproportionate value relative to its low implementation cost.

## Recommendations

1. **Implement signal classification in the next retro workflow update.** Add a `signal_type` field to retro findings. This requires no new skills and immediately improves the actionability of retro output.

2. **Prioritize `upstream-fix` completion (Story 4.X).** This is the architectural linchpin for both signal routing (Candidate 1) and the broader "Practice compounds" principle. Without it, the flywheel cannot mechanically close.

3. **Add per-session reflection to Impetus greeting.** A single optional prompt — "Last session, anything worth an intake?" — costs one workflow step and catches signals before they decay.

4. **Design `momentum:distill` for retro Phase 5.** A lightweight skill that proposes immediate rule/reference updates from retro findings, distinguishing small changes (commit now) from structural changes (queue as stories).

5. **Standardize retro metrics fields.** Make existing retro metrics machine-readable so that sprint-over-sprint trending becomes possible when the aggregation infrastructure arrives.

6. **Flag Bockeler's "Harness Engineering" for follow-on research.** Her guides-and-sensors taxonomy, the Steering Loop concept, and the computational/inferential sensor distinction are directly relevant to Momentum's hook and AVFL architecture but fall outside the scope of this flywheel-specific comparison.

## Known Limitations

### Research Gaps

- **No direct web fetch of Fowler articles during synthesis.** All Fowler claims derive from subagent research files that fetched the articles. Claims tagged VERIFIED were confirmed against primary sources by research subagents; claims tagged CITED were reported by subagents without independent re-verification during synthesis.

- **Gemini analyzed the wrong project.** The Gemini deep research output analyzed Steve Yegge's tool-intensive "Momentum" (NTM, Beads, CASS, PageRank, Thompson sampling), not this project. The Gemini output's Fowler analysis was accurate and usable as corroboration. The Momentum-side analysis was quarantined entirely. No Yegge concepts appear in this report.

- **Bockeler's article is adjacent, not central.** Per practitioner decision, "Harness Engineering for Coding Agent Users" is referenced as supplementary context but not treated as part of the core Fowler series comparison. A dedicated research pass on harness engineering concepts would yield additional adoption candidates.

### Open Questions from AVFL Validation

Three questions surfaced during AVFL checkpoint validation and resolved in practitioner Q&A:

1. **Bockeler scope** — resolved: in-scope for mention as supplementary, not as part of Fowler series. (Applied throughout this report.)
2. **Flywheel numbering** — resolved: practice-overview framing (principle #7 of 8, "Practice compounds") is authoritative. Product brief's "Evaluation Flywheel" (#4 of 7) is the historical precursor. (Applied in Section 1.)
3. **Gemini/Yegge** — resolved: discarded entirely. (Applied; no Yegge references in this report.)

### Evidence Strength

The strongest evidence in this report is Momentum's own codebase (all claims verifiable against files on disk) and direct Fowler article content (fetched by research subagents). The weakest evidence is the gap analysis in Sections 3 and 4, which requires negative claims ("X is absent from Y") — inherently harder to verify than positive claims. The AVFL validation pass caught and corrected 13 findings before synthesis, including one fabricated quote and several misattributions.

## Sources

### Fowler's Feedback Flywheel Series (Rahul Garg, martinfowler.com)

- [Series index](https://martinfowler.com/articles/reduce-friction-ai/) — "Patterns for Reducing Friction in AI-Assisted Development"
- [Knowledge Priming](https://martinfowler.com/articles/reduce-friction-ai/knowledge-priming.html) — 24 February 2026
- [Design-First Collaboration](https://martinfowler.com/articles/reduce-friction-ai/design-first-collaboration.html) — 03 March 2026
- [Context Anchoring](https://martinfowler.com/articles/reduce-friction-ai/context-anchoring.html) — 17 March 2026
- [Encoding Team Standards](https://martinfowler.com/articles/reduce-friction-ai/encoding-team-standards.html) — 31 March 2026
- [Feedback Flywheel](https://martinfowler.com/articles/reduce-friction-ai/feedback-flywheel.html) — 08 April 2026

### Supplementary (not part of the Fowler series)

- Birgitta Bockeler, ["Harness Engineering for Coding Agent Users"](https://martinfowler.com/articles/harness-engineering.html) — martinfowler.com, 02 April 2026

### Momentum Codebase (primary sources, all VERIFIED)

- `skills/momentum/references/practice-overview.md` — Eight principles, including #7 "Practice compounds"
- `docs/planning-artifacts/AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md` — Planning document, Sections 3.5, 4.3, 5.5
- `_bmad-output/planning-artifacts/product-brief-momentum-2026-03-13.md` — Product brief, seven principles
- `_bmad-output/planning-artifacts/prd.md` — PRD, FR28-FR33 (Evaluation Flywheel requirements)
- `skills/momentum/skills/avfl/SKILL.md` — AVFL pipeline specification
- `skills/momentum/skills/sprint-dev/workflow.md` — Sprint execution workflow
- `skills/momentum/skills/retro/workflow.md` — Retrospective workflow
- `skills/momentum/skills/sprint-planning/workflow.md` — Sprint planning workflow
- `skills/momentum/skills/impetus/SKILL.md` — Impetus orchestrator
- `skills/momentum/skills/upstream-fix/SKILL.md` — Upstream fix stub
- `skills/momentum/skills/architecture-guard/SKILL.md` — Architecture Guard
- `skills/momentum/skills/code-reviewer/SKILL.md` — Code reviewer
- `skills/momentum/references/completion-signals.md` — Flywheel integration triggers
- `skills/momentum/hooks/hooks.json` — Hook configuration
- `skills/momentum/references/hooks/file-protection.sh` — PreToolUse hook
- `skills/momentum/references/model-routing-guide.md` — Model routing
- `skills/momentum/references/gherkin-template.md` — Gherkin spec template
