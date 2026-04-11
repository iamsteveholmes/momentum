---
content_origin: claude-code-subagent
date: 2026-04-10
sub_question: "What concepts in Momentum's flywheel are absent or underdeveloped in Fowler's framework?"
topic: "Momentum Flywheel vs. Fowler's Feedback Flywheel — Conceptual Comparison"
---

# Momentum Concepts Absent or Underdeveloped in Fowler's Framework

## Overview

Fowler's Feedback Flywheel series (authored by Rahul Garg on martinfowler.com) focuses on practice-layer concerns: how individuals and teams harvest signal from AI sessions and route it back into shared artifacts. It addresses the human-in-the-loop dimension of AI-assisted development with sophistication and precision. Böckeler's "Harness Engineering for Coding Agent Users" (a separate standalone article on martinfowler.com, 2026-04-02) provides supplementary context on the technical harness layer.

Momentum operates at a different layer. It is an agentic engineering practice *module* — a deployed, executable harness of skills, agents, hooks, and workflows that automates the development lifecycle rather than advising on it. The gap between the two is not primarily quality vs. speed; it is *advisory* vs. *operational*. Fowler describes what teams should do; Momentum does it automatically.

This document identifies Momentum concepts that Fowler's framework does not address, addresses only at the level of principle without implementation, or explicitly leaves to future work.

**Sources used:**
- Momentum codebase at `/Users/steve/projects/momentum` — skills, workflows, hooks, agents, reference files
- Fowler's Feedback Flywheel: `martinfowler.com/articles/reduce-friction-ai/feedback-flywheel.html` [OFFICIAL]
- Böckeler's Harness Engineering: `martinfowler.com/articles/harness-engineering.html` [OFFICIAL: Böckeler, harness-engineering.html]
- Fowler's Encoding Team Standards: `martinfowler.com/articles/reduce-friction-ai/encoding-team-standards.html` [OFFICIAL]
- Fowler's Context Anchoring: `martinfowler.com/articles/reduce-friction-ai/context-anchoring.html` [OFFICIAL]

---

## 1. Adversarial Validation as a Formal Pipeline (AVFL)

**What Momentum does:** AVFL — the Adversarial Validate-Fix Loop — is a fully operationalized multi-agent validation pipeline [OFFICIAL: `/Users/steve/projects/momentum/skills/momentum/skills/avfl/SKILL.md`]. It runs parallel reviewer subagents with deliberately different reading styles (Enumerator and Adversary), consolidates findings, scores outputs against a threshold (≥95/100 = clean), and iterates fix cycles until the threshold is met or the iteration cap is reached. It applies across four validation lenses: structural integrity, factual accuracy, coherence and craft, and domain fitness.

AVFL is benchmarked: "dual reviewers with different framings improve accuracy ~8 percentage points absolute over single-agent validation (Meta-Judge 2025). Staged validation is 8%+ more accurate and 1.5–5× more compute-efficient than outcome-only evaluation." [OFFICIAL: `avfl/SKILL.md`]

**What Fowler and Böckeler say:** Fowler identifies "Failure Signal" as one of four signal types — "root causes of AI errors mapped to specific artifact gaps." He routes failure signal to "guardrails and documented anti-patterns." [OFFICIAL: feedback-flywheel.html]

Böckeler also introduces the concept of "Sensors" in harness engineering — feedback controls that "observe after the agent acts and enable self-correction," citing linters, type checkers, and code review agents as examples. [OFFICIAL: Böckeler, harness-engineering.html]

**Why Momentum is novel here:** Fowler and Böckeler identify the need for feedback sensors and failure signal routing, but stop at naming the category. Neither describes a formal pipeline with: parallel reviewer diversity, cross-reviewer confidence scoring (HIGH when both find it, MEDIUM when one finds it), iterative fix loops with convergence thresholds, skepticism calibration across iterations, or profile selection based on artifact maturity (gate / checkpoint / full / scan). Böckeler's "code review agents" are mentioned as examples of inferential sensors; Momentum's AVFL is an architecturally specified, benchmarked multi-agent pipeline with provably better recall than single-agent review.

The concept of **dual-reviewer adversarial framing** as a structural mechanism for hallucination filtering — not just quality improvement — is absent from Fowler's framework entirely. [PRAC]

---

## 2. Dependency-Driven Story Spawning with Worktree Isolation

**What Momentum does:** Sprint execution builds an explicit dependency graph from story metadata and spawns dev agents only for stories whose blockers are all `done`. Each story runs in a git worktree (`story/{slug}`), isolated from the sprint branch. Worktrees are retained through quality gate cycles and cleaned up only after all fixes are confirmed [OFFICIAL: `/Users/steve/projects/momentum/skills/momentum/skills/sprint-dev/workflow.md`].

This produces a wave structure: unblocked stories execute in parallel; newly unblocked stories are identified after each merge and dispatched immediately. The spawning model is explicit: one `Agent` tool call per story in a single message turn for maximum parallelism.

**What Fowler says:** Fowler's "Design-First Collaboration" pattern recommends establishing design before implementation, and "Context Anchoring" addresses maintaining context across sessions. Neither addresses multi-story sprint coordination, dependency-ordered execution, or git-branch isolation per story. [OFFICIAL]

Böckeler's "Harness Engineering" discusses "Keep Quality Left" as a principle — distributing checks across the development lifecycle. But this is a principle about where checks live, not about orchestration of parallel story work. [OFFICIAL: Böckeler, harness-engineering.html]

**Why Momentum is novel here:** Fowler's framework is session-scoped: a developer and an AI collaborating in a single context. Momentum's sprint-dev is sprint-scoped: multiple isolated agents executing concurrently with coordinated merge sequencing and quality gating after all stories complete. The concept of a **dependency graph driving agent spawning** — rather than a human deciding what to work on next — is entirely absent from Fowler's framework. [PRAC]

---

## 3. Transcript Audit as Retrospective Data Source

**What Momentum does:** The retro skill extracts raw session transcript data via DuckDB queries and analyzes it with a four-agent collaborative team (three auditors + one documenter using TeamCreate). Auditors read different slices of transcript data — user messages, agent summaries and errors, inter-agent team messages — and send findings to the documenter via SendMessage. The documenter synthesizes cross-cutting patterns and produces a structured findings document that feeds directly into the next sprint's backlog. [OFFICIAL: `/Users/steve/projects/momentum/skills/momentum/skills/retro/workflow.md`]

Specifically tracked: user corrections, redirections, frustration signals, agent duplication patterns, error recovery rates, false-positive review findings, fix cycle thrash, and inter-agent coordination quality.

**What Fowler says:** Fowler's "Feedback Flywheel" includes retrospective cadence as one of four cadences — "Concrete outputs include priming revisions and command refinements." [OFFICIAL: feedback-flywheel.html] He also describes "After each session" reflection and stand-up integration. But the retrospective is described as a team ceremony that happens to produce artifact updates, not as a data pipeline.

**Why Momentum is novel here:** Fowler treats retrospectives as a team practice with qualitative discussion outputs. Momentum treats sprint history as a structured data source. The session transcript is a queryable artifact; auditor agents specialize in different analytical lenses; findings are structured with severity, evidence, and source attribution; and the output directly populates the story backlog.

The concept of **machine-readable sprint history as primary retro input** — rather than team memory and discussion — is not addressed in Fowler's framework. The four-agent collaborative team pattern (TeamCreate with SendMessage for iterative cross-auditor synthesis) is also architecturally novel: it's a workflow that depends on inter-agent communication during analysis, not just parallelism. [PRAC]

---

## 4. Eval-Driven Skill Development (EDD)

**What Momentum does:** Momentum's practice overview lists "Eval-driven development — skills are validated by behavioral evals, not unit tests" as one of its eight principles [OFFICIAL: `/Users/steve/projects/momentum/skills/momentum/references/practice-overview.md`]. Each skill directory contains an `evals/` subdirectory. Skills are created following a workflow that classifies tasks as `skill-instruction`, `script-code`, `rule-hook`, `config-structure`, or `specification` and injects appropriate implementation guidance including EDD steps for skill-instruction tasks [OFFICIAL: `/Users/steve/projects/momentum/skills/momentum/skills/create-story/workflow.md`].

The AVFL skill's benchmarking section is itself a product of EDD: "36 runs across 3 models × 3 effort levels × all roles" produced the Role Configuration table, and specific model-role combinations are prohibited based on measured failure modes. [OFFICIAL: `avfl/SKILL.md`]

**What Fowler and Böckeler say:** Böckeler's "Harness Engineering" describes "Sensors" including "Computational" (deterministic, fast: tests, linters, type checkers) and "Inferential" (semantic, GPU-based: AI code review, custom semantic analysis). [OFFICIAL: Böckeler, harness-engineering.html] She describes a "Maintainability Harness," "Architecture Fitness Harness," and "Behaviour Harness" as regulation dimensions. But these apply to application code, not to the skills and workflows themselves.

Fowler's "Encoding Team Standards" discusses treating AI instructions "as infrastructure: versioned, reviewed, and shared artifacts." [OFFICIAL: encoding-team-standards.html] But this is about sharing and versioning instructions, not about systematically evaluating their behavioral correctness through structured test runs.

**Why Momentum is novel here:** Fowler and Böckeler describe skills/instructions as things to share and version. Momentum adds the discipline of **behavioral evaluation** for the skills themselves: each skill should be verifiable by running it against known inputs and checking outputs. This is not unit testing code; it is testing whether an AI skill produces correct behavior across representative scenarios. The epistemological question — how do you know your AI instructions actually work? — is addressed by Momentum's EDD principle and absent from Fowler's framework. [PRAC]

---

## 5. Orchestrator Purity and Agent Spawning Discipline

**What Momentum does:** Impetus (the session orchestrator) enforces a strict purity rule: it dispatches to skills and agents but never performs dev, validation, or test work directly [OFFICIAL: `architecture-guard/SKILL.md` Decision 3d: "Orchestrator purity — Impetus does not perform dev/eval/test/validation"]. The spawning pattern is architecturally prescribed: fan-out (individual Agent tool calls, all in one message for parallelism) vs. TeamCreate (collaborative agents that communicate via SendMessage during execution) is a design decision documented in `spawning-patterns.md` with explicit guidance on when each applies [OFFICIAL: `/Users/steve/.claude/rules/spawning-patterns.md`].

Sprint-dev's team composition is declared in XML annotations specifying spawning mode, concurrency, agent definition, and rationale for every phase [OFFICIAL: `sprint-dev/workflow.md`].

**What Böckeler says:** Böckeler's "Harness Engineering" describes the harness as "everything in an AI agent except the model itself." She describes guides (feedforward) and sensors (feedback) as the two components. She discusses a "Steering Loop" where humans iterate on harness controls based on recurring issues. [OFFICIAL: Böckeler, harness-engineering.html]

Böckeler does not address multi-agent orchestration, the design decision between parallel independent agents vs. collaborative communicating agents, or the principle that orchestrators should not do domain work directly.

**Why Momentum is novel here:** Böckeler's harness model is a human-and-one-agent model. Momentum's architecture is a multi-agent graph with explicit composition rules. The concepts of **orchestrator purity** (an agent that routes but never implements) and **spawn registry** (deduplication guard preventing re-spawning of already-running agents) have no analogues in Böckeler's or Fowler's framework. The fan-out vs. TeamCreate decision is a novel design pattern for agentic systems that Fowler's single-agent-centric framing does not need to address. [PRAC]

---

## 6. File-System Enforcement via PreToolUse/PostToolUse Hooks

**What Momentum does:** Momentum ships a hooks system with three layers: `PreToolUse` (blocks writes to protected paths before they execute), `PostToolUse` (runs lint/format on modified files), and `Stop` (advisory quality gate — lint, uncommitted change check, test runner — runs before session end). Protected paths include Gherkin specs, planning artifacts, story/sprint index files, and project rules. The hook system is deployed via `hooks.json` and is enforced at the Claude Code runtime level — the agent literally cannot write to protected paths. [OFFICIAL: `/Users/steve/projects/momentum/skills/momentum/hooks/hooks.json`; `references/hooks/file-protection.sh`; `references/hooks/stop-gate.sh`]

This implements what Momentum calls "Consent at every gate — no file writes, no merges, no destructive actions without explicit approval" [OFFICIAL: `practice-overview.md`] and the architectural invariant that dev agents cannot access Gherkin specs (Decision 30: black-box separation).

**What Fowler and Böckeler say:** Fowler's "Failure Signal" routes to "Guardrails and documented anti-patterns." [OFFICIAL: feedback-flywheel.html] Böckeler's "Harness Engineering" describes "Sensors" that observe after the agent acts, and "Guides" that anticipate behavior before action. She mentions "code mods" and "structural tests" as guide examples. [OFFICIAL: Böckeler, harness-engineering.html]

**Why Momentum is novel here:** Fowler and Böckeler identify the *category* (guardrails, guides) but do not describe runtime enforcement mechanisms. Momentum's hook system is a specific technical implementation: hooks fire at the tool-use layer, not at the output-review layer. The distinction matters — a PostToolUse lint hook that fires every time a file is written is qualitatively different from a guardrail a developer might consult. **Real-time path protection via PreToolUse** that blocks writes before they happen (rather than catching them after) is a concept in Böckeler's implied future work but not addressed in the published framework. [PRAC]

---

## 7. Model Routing by Role and Cognitive Hazard

**What Momentum does:** Momentum assigns specific models to specific roles based on measured performance characteristics and cognitive hazard classification. Verifier roles (code-reviewer, architecture-guard) use Opus because of "Cognitive hazard rule — verifier." AVFL's Adversary validators use Opus/high because "Best severity calibration; critical findings correctly classified" — a finding derived from 36 benchmark runs. The Enumerator uses Sonnet/medium because Haiku "produces false-pass scores (92/100 while missing a critical architectural contradiction)." The Consolidator uses Haiku/low because it is "Fully invariant across all model/effort combos." [OFFICIAL: `avfl/SKILL.md`; `references/model-routing-guide.md`]

This is not "use the best model everywhere" — it is principled differentiation based on what each role's failure mode looks like and which model calibrates severity correctly for that role.

**What Fowler and Böckeler say:** Fowler's and Böckeler's frameworks are model-agnostic. Their patterns apply regardless of which model is used. Neither addresses multi-model systems, role-to-model assignment, or how model choice interacts with failure mode risk. [OFFICIAL]

**Why Momentum is novel here:** In a multi-agent system, different agent roles have different failure mode risks. A validator that downgrades critical findings to high severity causes under-reporting; a validator that produces false-pass scores is more dangerous than no validator. **Cognitive hazard classification as a model routing signal** — the idea that verifier roles carry higher failure risk and therefore require stronger models — is a concept specific to orchestrated agentic systems that Fowler's and Böckeler's single-developer-with-AI framing does not require. [PRAC]

---

## 8. Gherkin-Based Black-Box Verification with Developer Separation

**What Momentum does:** Sprint planning generates Gherkin `.feature` files for every story, stored in `sprints/{sprint-slug}/specs/`. Dev agents are architecturally prohibited from reading these files (Decision 30: black-box separation, enforced by the file-protection hook). E2E validator agents read only the Gherkin specs and validate running behavior against scenarios — they do not read the implementation. Sprint-dev's Phase 6 (Verification) presents a developer checklist derived from Gherkin scenarios where the developer manually confirms each behavior. [OFFICIAL: `sprint-dev/workflow.md`; `references/gherkin-template.md`; `architecture-guard/SKILL.md`]

Gherkin quality is governed by specific anti-patterns in Momentum's template: no AC-by-AC translation, no internal mechanism references, no implementation-coupled assertions, no passive voice in When clauses. The template enforces behavioral specification, not structural verification. [OFFICIAL: `references/gherkin-template.md`]

**What Böckeler says:** Böckeler's "Behaviour Harness" (harness engineering) is described as "least developed, most challenging" and is not given substantive treatment. She mentions functional correctness as a harness dimension but provides no mechanism for it. [OFFICIAL: Böckeler, harness-engineering.html]

Fowler's Encoding Team Standards includes "Review-time" application of standards acting "as team quality gate" — but this is instruction-set governance, not behavioral specification. [OFFICIAL: encoding-team-standards.html]

**Why Momentum is novel here:** Böckeler acknowledges behavioral correctness is the hardest harness dimension but does not propose a mechanism. Momentum provides a complete mechanism: ATDD-style Gherkin specs generated before implementation, enforced separation between implementer and verifier via file-system protection, and developer-facing confirmation checklists at sprint close. The concept of **spec-to-verification pipeline with enforced ignorance** (dev agents cannot see specs they are implementing against) is architecturally novel and addresses the "developer teaches AI" problem from a different angle than Fowler's priming-and-standards approach. [PRAC]

---

## 9. Architecture Drift Detection as a Quality Gate

**What Momentum does:** Architecture Guard is a read-only agent spawned at the end of every sprint that checks all sprint changes against a versioned architecture decisions document. It reports CRITICAL / HIGH / MEDIUM / LOW findings per architecture decision violated and produces a PASS/FAIL verdict (FAIL = any CRITICAL or 3+ HIGH findings). It is structurally similar to a linter but operates against semantic architectural invariants, not syntactic rules. [OFFICIAL: `/Users/steve/projects/momentum/skills/momentum/skills/architecture-guard/SKILL.md`]

Architecture Guard is scoped specifically: it checks plugin structure, naming conventions, orchestrator purity, separation of concerns, read/write authority, two-layer agent model compliance, and context isolation — the architectural invariants documented in the project's `architecture.md`.

**What Böckeler says:** Böckeler's "Harness Engineering" describes "Architecture Fitness Harness" as addressing "performance and structural characteristics." She identifies "Continuous Drift Detection" as an emergent concept — "monitoring gradual codebase degradation outside change workflows." [OFFICIAL: Böckeler, harness-engineering.html]

Fowler's Failure Signal routing reaches "Custom Linters or Architectural Guardrails" as a destination. [OFFICIAL: feedback-flywheel.html]

**Why Momentum is novel here:** Böckeler identifies architectural guardrails as a signal destination and drift detection as an emergent concept. Momentum implements both as a concrete skill: an agent role with a defined input (sprint diff + architecture doc), a specific set of decisions to check, a severity taxonomy, and a binary PASS/FAIL verdict that gates sprint completion. The **architecture guard as a sprint completion gate** — not an advisory tool but a blocking check — is more operationalized than Fowler's or Böckeler's framework describes. [PRAC]

---

## 10. Provenance and Staleness Detection

**What Momentum does:** Sprint planning checks all candidate stories against recent git history: "For each story with status `ready-for-dev` or `in-progress`, get the story's touches paths, run `git log --oneline --since='30 days ago' -- touches_paths` to find recent commits, if commits exist mark the story as potentially stale." [OFFICIAL: `sprint-planning/workflow.md`]

Momentum's practice overview lists "Provenance by default — every artifact traces to its source; staleness is detected, not discovered" as a core principle. [OFFICIAL: `practice-overview.md`] Stories carry `touches` arrays explicitly tying them to the files they modify, enabling this automated staleness check.

**What Fowler says:** Fowler's "Knowledge Priming" pattern includes the problem of "outdated versions" as a context signal — "information the AI lacked." [OFFICIAL: feedback-flywheel.html] His Context Anchoring recommends "updating at natural decision points" to prevent priming documents from becoming stale. [OFFICIAL: context-anchoring.html]

**Why Momentum is novel here:** Fowler's staleness concern is about priming documents becoming outdated relative to the codebase. Momentum's staleness concern is different: a story on the backlog might already have been implemented by related commits, making the story itself stale. Git is used as an oracle — not just a history tool — for automated staleness detection at sprint planning time. The concept of **automated story staleness detection via git history** before including a story in a sprint is not addressed in Fowler's framework. [PRAC]

---

## Summary Table

| Momentum Concept | Fowler/Böckeler Coverage | Gap |
|---|---|---|
| AVFL — adversarial dual-reviewer validation pipeline | Identifies "failure signal" and "sensors" as categories | No pipeline specification, no dual-reviewer cross-checking, no convergence thresholds |
| Dependency-driven story spawning with worktree isolation | Design-first at session scope | No sprint-scope orchestration; no dependency graph; no isolation-per-story |
| Transcript audit as retro data source | Retro as team ceremony cadence | No structured data pipeline; no specialized auditor agents; no machine-readable sprint history |
| Eval-driven skill development (EDD) | Standards as shared infrastructure | No behavioral evaluation mechanism for the skills themselves |
| Orchestrator purity + spawning discipline | Harness as guide+sensor | No multi-agent composition rules; no fan-out vs. TeamCreate distinction; no orchestrator purity principle |
| PreToolUse/PostToolUse file-system enforcement | Guardrails and sensors as categories | No runtime enforcement mechanism; no path-level write blocking |
| Model routing by cognitive hazard | Model-agnostic | No role-to-model assignment; no failure-mode-specific model selection |
| Gherkin-based black-box verification | Behaviour harness "least developed" | No concrete mechanism; no enforced implementer/verifier separation |
| Architecture drift detection as sprint gate | Drift detection as "emergent concept" | No concrete agent role; no per-sprint architectural verdict |
| Automated story staleness via git | Priming doc staleness | Different concern entirely; no automated detection against git history |

---

## Sources

### Momentum Codebase [OFFICIAL]
- `/Users/steve/projects/momentum/skills/momentum/skills/avfl/SKILL.md` — AVFL pipeline specification
- `/Users/steve/projects/momentum/skills/momentum/skills/sprint-dev/workflow.md` — Sprint execution workflow
- `/Users/steve/projects/momentum/skills/momentum/skills/retro/workflow.md` — Retrospective workflow
- `/Users/steve/projects/momentum/skills/momentum/skills/sprint-planning/workflow.md` — Sprint planning workflow
- `/Users/steve/projects/momentum/skills/momentum/skills/impetus/SKILL.md` — Impetus orchestrator
- `/Users/steve/projects/momentum/skills/momentum/skills/architecture-guard/SKILL.md` — Architecture Guard
- `/Users/steve/projects/momentum/skills/momentum/skills/create-story/workflow.md` — Story creation
- `/Users/steve/projects/momentum/skills/momentum/hooks/hooks.json` — Hook configuration
- `/Users/steve/projects/momentum/skills/momentum/references/hooks/file-protection.sh` — PreToolUse hook
- `/Users/steve/projects/momentum/skills/momentum/references/hooks/stop-gate.sh` — Stop hook
- `/Users/steve/projects/momentum/skills/momentum/references/practice-overview.md` — Eight core principles
- `/Users/steve/projects/momentum/skills/momentum/references/gherkin-template.md` — Gherkin spec template
- `/Users/steve/projects/momentum/skills/momentum/references/model-routing-guide.md` — Model routing
- `/Users/steve/projects/momentum/skills/momentum/agents/dev.md` — Dev agent definition

### Fowler's Feedback Flywheel Series [OFFICIAL]
- `martinfowler.com/articles/reduce-friction-ai/feedback-flywheel.html` — Four signal types, four cadences
- `martinfowler.com/articles/reduce-friction-ai/encoding-team-standards.html` — Versioned executable instructions
- `martinfowler.com/articles/reduce-friction-ai/context-anchoring.html` — Feature documents, session lifecycle

### Böckeler's Harness Engineering [OFFICIAL]
- Birgitta Böckeler, "Harness Engineering for Coding Agent Users," martinfowler.com, 2026-04-02. https://martinfowler.com/articles/harness-engineering.html — Guides, sensors, harness engineering
