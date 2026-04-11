---
content_origin: claude-code-subagent
date: 2026-04-10
sub_question: "How does Momentum define and implement its flywheel concept? (our own docs/code as source of truth)"
topic: "Momentum Flywheel vs. Fowler's Feedback Flywheel — Conceptual Comparison"
---

# How Momentum Defines and Implements Its Flywheel Concept

## Overview

Momentum's flywheel is formally called the **Evaluation Flywheel** — a named principle that sits at the center of its practice model. It is not incidental; it is explicitly numbered as one of the framework's seven core composable principles and encoded as a discrete set of functional requirements (FR28–FR33). The flywheel's defining claim is that every quality failure in AI-generated output is a signal about the *input system* (workflow, specification, rule) that produced it. Fixing the output is a one-time patch. Fixing the process prevents an entire class of errors permanently.

The flywheel is currently in a partially implemented state: the sprint cycle infrastructure (planning → dev → AVFL → retro) is live, the `upstream-fix` skill exists as a stub, and the findings ledger and cross-story pattern detection belong to Epic 6 ("Practice Compounds"), which has backlog stubs but no story files yet.

---

## How the Flywheel Is Defined

**[OFFICIAL]** The product brief (`_bmad-output/planning-artifacts/product-brief-momentum-2026-03-13.md`) articulates the Evaluation Flywheel as the fourth of seven foundational principles:

> "**Evaluation Flywheel** — When output fails quality standards, trace the failure upstream. Don't fix the code — fix the workflow, specification, or rule that caused the defect. Every upstream fix prevents a class of errors permanently."

Note on numbering: the two source documents present different counts. The product brief defines **7 principles**, with the Evaluation Flywheel at position **#4**. The practice overview defines **8 principles**, with the flywheel concept at position **#7** ("Practice compounds"). Both counts are correct — they reference different source documents with different principle sets. The discrepancy does not indicate an error in either source.

**[OFFICIAL]** The planning document (`docs/planning-artifacts/AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md`) traces the concept to three independent prior implementations: OpenAI's Evaluation Flywheel (analyze failures, categorize, refine prompts, iterate), NVIDIA's Data Flywheel (self-improving loop from interaction data), and Stanford's DSPy (programmatic prompt optimization). The common principle stated is: "every output failure is a signal about the input system." Fixing the input (specification, template, CLAUDE.md rule, workflow step) prevents a class of errors permanently.

**[OFFICIAL]** The practice overview (`skills/momentum/references/practice-overview.md`) encodes the flywheel as principle #7 of eight: "Practice compounds — findings accumulate across stories into a flywheel of systemic improvement."

**[OFFICIAL]** The PRD's innovation section states: "Upstream fix as a formal discipline. Quality approaches fix outputs. Momentum traces failures through a specification chain to the workflow that produced the defect and fixes that. This isn't incremental improvement on code review — it's a different model of where quality comes from. The flywheel is the mechanism; the insight is that in agentic engineering, the *process artifacts* are the product, not the code."

---

## The Upstream Trace Hierarchy

**[OFFICIAL]** The flywheel operates through a structured upstream trace. When a quality failure is detected, the responsible fix is sought at the highest applicable level in the following chain (from `AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md`, Section 4.3):

1. **Spec-generating workflow gap** — The story creation workflow, its template, or the agent running it failed to produce sufficient context. Fix the workflow that produces stories; every future story improves. This is the highest-value fix — upstream of upstream. Uses BMB (self-modification capability) to modify the workflow or agent.
2. **Specification gap in this particular story** — The PRD, architecture doc, or story ACs were incomplete or incorrect for this specific case. Fix the spec. Valuable but only fixes this instance.
3. **CLAUDE.md / .claude/rules/ gap** — The AI deviated from a standard that should apply universally. Add the rule so it applies in every future session.
4. **Tooling gap** — Something that should be enforced deterministically was left advisory. Add a hook, lint rule, or architectural test.
5. **One-off error** — Fix the code. This is the least valuable fix.

**[OFFICIAL]** The hierarchy is explicitly deliberate: "Fixing code prevents one error, once. Fixing a CLAUDE.md rule prevents a class of errors across all future sessions. Fixing a workflow prevents a class of errors across all future executions of that workflow. Fixing a spec-generating workflow prevents a class of errors across all future specifications and everything downstream of them."

**[OFFICIAL]** The document explicitly names this as "Deming's 'fix the process, not the defect' applied to AI-augmented development."

---

## The Three Flywheel Cadences

**[OFFICIAL]** The planning document (Section 5.5) specifies that the flywheel operates at three distinct cadences:

**1. Per-session (immediate):** When Claude output fails quality standards during a session, the failure should trigger explicit dialogue between agent and developer — not silent correction. The agent surfaces the failure: "This output didn't meet [standard]. Is this a gap in CLAUDE.md, a missing rule, or a one-off?" If the answer is a CLAUDE.md or rules gap, the rule is added immediately in-session.

**2. Per-story (sprint cadence):** Code review findings trigger the full upstream trace. The critical question is not just "what went wrong in this story?" but "what went wrong in the process that produced this story?" This is where the findings ledger activates.

**3. Per-sprint (retrospective):** The retrospective explicitly asks whether any stories arrived at implementation with missing context, unclear ACs, or absent ATDD tests. If yes, the Create Story, TEA ATDD, or related workflows are the fix targets — not the individual stories. Retrospective outputs include: workflow modifications, CLAUDE.md amendments, quality rules updates, Definition of Done additions, hook/tooling additions, and process tasks added to the process backlog.

**[OFFICIAL]** The measurability principle: "The flywheel's output is measurable: the number of upstream fixes per sprint, categorized by level. A healthy flywheel shows frequent upstream fixes early (the system is learning) that decrease over time (the system has learned). The most valuable metric is the ratio of workflow-level fixes to code-level fixes — a mature system fixes almost nothing at the code level because the workflows that generate and verify code have been refined to prevent errors before they occur."

---

## The Findings Ledger — The Flywheel's Memory

**[OFFICIAL]** The findings ledger is the structural mechanism that makes the flywheel function across sessions. It is a global JSONL append-only store at `~/.claude/momentum/findings-ledger.jsonl` with fields: `id`, `project`, `story_ref`, `phase`, `severity`, `pattern_tags`, `description`, `evidence`, `provenance_status`, `upstream_fix_applied`, `upstream_fix_level`, `upstream_fix_ref`, `timestamp`.

**[OFFICIAL]** The ledger serves two purposes: immediate (each finding is communicated to the developer with the agent's best assessment of whether it's one-off or systemic, and the developer confirms or reclassifies) and cumulative over time (patterns become visible even when each individual occurrence looked like a one-off — "three 'one-off' auth validation misses across different stories is a systemic issue that no single code review could detect").

**[OFFICIAL]** The retrospective workflow reads the ledger and groups findings by category to surface these patterns. The PRD specifies FR28–FR33 as the Evaluation Flywheel functional requirements:
- FR28: Findings ledger accumulates findings across stories with category, root cause classification, and upstream level
- FR29: System detects cross-story patterns and surfaces systemic issues
- FR30: Flywheel explains detected issues and suggests upstream trace with visual workflow status: detection → review → upstream trace → solution → verify → log
- FR31: Developer can approve or reject each flywheel suggestion — the agent never proceeds without explicit consent
- FR32: Upstream fixes can be applied at any level: spec-generating workflow, specification, CLAUDE.md/rules, tooling, or one-off code fix
- FR33: System tracks the ratio of upstream fixes to code-level fixes as a practice health metric

**[OFFICIAL]** Implementation status: the findings ledger and cross-story pattern detection are in Epic 6 ("Practice Compounds"), currently at backlog stub stage with no story files. The flywheel infrastructure is described as planned but not yet built as of 2026-04-10.

---

## What Makes It Self-Reinforcing

**[OFFICIAL]** The self-reinforcing mechanism operates through compounding improvement of the artifacts that govern AI generation. From the PRD: "The system gets smarter every sprint — not because the AI improves, but because the practice around it compounds."

The reinforcing loop is:

1. **AI generates code** guided by specifications, CLAUDE.md rules, and workflow templates
2. **Multi-layer verification** (AVFL + code review + architecture guard + E2E validation) surfaces findings
3. **Upstream trace** attributes findings to the workflow, spec, or rule that produced the defect
4. **Fixes applied at the right level** improve the governing artifacts
5. **Improved artifacts guide the next AI generation cycle** — preventing the same class of errors

**[OFFICIAL]** The PRD explicitly describes what constitutes compounding: "As the developer works through stories, specifications get better instead of fragmenting. Time spent on specs decreases instead of steadily increasing. Code quality improves because the specs driving generation improve. The developer feels more engaged and more confident."

**[OFFICIAL]** Provenance is explicitly called "load-bearing infrastructure that enables the flywheel" — when upstream documents change, downstream documents are flagged as suspect. This prevents obsolete decisions from resurfacing and ensures that flywheel fixes propagate correctly through the document chain.

**[OFFICIAL]** The failure signal for a non-turning flywheel is stated explicitly in both the PRD and the practice overview: "Same class of error recurs across stories (flywheel not turning)" — confirming that the flywheel's defining success criterion is the *absence* of recurrence for previously traced issues.

---

## Role of Each Skill in the Flywheel

### `momentum:sprint-planning`
**[OFFICIAL]** Sprint planning is the intake gate for quality. It generates Gherkin specs from plain English ACs (stored separately so dev agents never see them), runs AVFL on the complete sprint plan before activation, and creates the team composition record. Poor sprint planning is upstream of every quality failure in execution.

### `momentum:sprint-dev`
**[OFFICIAL]** Sprint execution is where findings are generated. After all stories merge, a single AVFL scan pass (discovery only, no fixes) runs on the full sprint codebase. Per-story code review agents run in parallel. Findings are consolidated into a fix queue; fix agents address confirmed findings in severity order. The Team Review phase (QA reviewer + E2E validator + architecture guard) validates behavioral compliance with Gherkin specs.

### `momentum:avfl`
**[OFFICIAL]** The Adversarial Validate-Fix Loop is the primary finding-generation engine. It runs with up to 8 parallel validators across 4 lenses (structural integrity, factual accuracy, coherence and craft, domain fitness), each with dual-reviewer framings (Enumerator: systematic; Adversary: intuitive). The scan profile runs in sprint context — discovery only, structured handoff to a resolution team. The full profile runs iterative fix loops until score ≥ 95/100. Every AVFL finding is a potential flywheel input.

### `momentum:retro`
**[OFFICIAL]** The retrospective is the primary flywheel activation point. It runs a 4-agent auditor team (3 auditors + 1 documenter via TeamCreate, collaborative pattern) against DuckDB transcript extracts from all sprint sessions. The retro explicitly closes the cycle by: verifying story completion, producing a findings document, creating story stubs from triage findings (including process improvement items), and calling sprint closure commands. The retro output contains both Momentum triage (practice improvements) and project triage (project findings).

### `momentum:upstream-fix`
**[OFFICIAL]** Defined in the SKILL.md as: "Traces quality failures upstream to spec, rule, or workflow root cause. Proposes fixes at the right level." Currently a stub — "full implementation in Story 4.X." The skill's role in the runtime is as a triggered offer from Impetus when critical findings are detected.

### `momentum:code-reviewer`
**[OFFICIAL]** An adversarial, read-only verifier that runs per-story after each merge. It cannot modify files. Its findings populate the consolidated fix queue that feeds the upstream trace process.

### `momentum:architecture-guard`
**[OFFICIAL]** A read-only pattern drift detector. It compares new code against established patterns in CLAUDE.md and architecture documents. Drift findings are inputs to the flywheel — persistent pattern drift signals that a .claude/rules/ file needs updating.

### `momentum:intake`
**[OFFICIAL]** Appends to the `intake-queue.jsonl` event log — an append-only JSONL that accumulates observations and issues. Events escalate to stories when patterns emerge. This is the mechanism for per-session flywheel activation outside of formal sprint cycles.

---

## The Flywheel in Terms of Agents, Artifacts, and Feedback Loops

### Agents Involved

**[OFFICIAL]** The production side: the `dev` agent (implementing stories in isolated worktrees), the `sprint-dev` orchestrator (managing the sprint lifecycle).

**[OFFICIAL]** The verification side (all read-only, structurally separated): code-reviewer, architecture-guard, AVFL validators (Enumerator + Adversary per lens), AVFL consolidator, QA reviewer, E2E validator.

**[OFFICIAL]** The flywheel side: retro auditor team (3 auditors + 1 documenter), upstream-fix (planned), Impetus (synthesizes findings in its own voice, offers flywheel traces on critical findings).

### Artifacts in the Loop

**[OFFICIAL]** The governing artifacts that get improved by the flywheel:
- `_bmad-output/planning-artifacts/prd.md` — product requirements
- `_bmad-output/planning-artifacts/architecture.md` — architectural decisions
- `.claude/rules/` — project-scoped rules loaded every session
- `~/.claude/rules/` — global rules loaded every session
- Skill SKILL.md files — workflow instructions
- Sprint Gherkin specs (`sprints/{slug}/specs/*.feature`) — behavioral specs for verifiers
- Story files — acceptance criteria

**[OFFICIAL]** The evidence artifacts that the flywheel reads:
- `~/.claude/momentum/findings-ledger.jsonl` — global cross-story findings accumulator
- `.claude/momentum/sprint-logs/` — agent JSONL logs
- Claude Code session transcripts (DuckDB via transcript-query.py) — full session evidence

### The Feedback Loop Structure

**[UNVERIFIED]** Synthesizing from the architecture, the full loop is:

```
Governing Artifacts
       ↓ (guide)
AI Code Generation (momentum:dev)
       ↓ (produces)
Merged Sprint Codebase
       ↓ (evaluated by)
Verification Layer (AVFL scan + code-reviewer + architecture-guard + Team Review)
       ↓ (produces)
Findings → Findings Ledger
       ↓ (pattern detected at retro)
Upstream Trace (momentum:upstream-fix)
       ↓ (fix applied at right level)
Governing Artifacts (improved)
       ↑ (restart loop)
```

The loop is bounded by human consent at every gate — the developer approves fixes before they are applied (FR31). No auto-apply. This makes the flywheel a human-in-the-loop compounding system, not an autonomous one.

---

## Provenance as Flywheel Infrastructure

**[OFFICIAL]** The PRD calls provenance "load-bearing infrastructure" for the flywheel specifically: "This is not documentation hygiene — it is load-bearing infrastructure that enables the flywheel, prevents hallucination propagation, and stops obsolete decisions from resurfacing."

**[OFFICIAL]** The provenance mechanism uses `derives_from` frontmatter in every artifact, content hashes (via `git hash-object`), and one-hop propagation. When an upstream document changes, dependent documents are flagged as suspect. This ensures that when a flywheel fix updates a specification, its downstream artifacts (stories, Gherkin specs) are flagged for review rather than silently consuming the old version.

**[OFFICIAL]** The architecture decision (1a) encodes this as: "Provenance graph — Pure YAML frontmatter. `derives_from` in each doc, `referenced_by` computed on demand. Content hashes via `git hash-object`. One-hop propagation, human-gated."

---

## The Flywheel's Relationship to the Enforcement Tier Model

**[OFFICIAL]** The flywheel does not operate in isolation — it interacts with a three-tier enforcement model:
- **Tier 1: Deterministic** (hooks, linters, tests) — cannot be forgotten or deprioritized. The flywheel can promote advisory standards to Tier 1 by adding hooks.
- **Tier 2: Structured** (SKILL.md workflow steps) — procedurally enforced during workflow execution. The flywheel can improve Tier 2 by modifying workflow step files.
- **Tier 3: Advisory** (CLAUDE.md, .claude/rules/) — always-loaded but advisory. The flywheel most frequently acts here by adding or updating rules.

**[OFFICIAL]** An explicit flywheel action is "advisory standards promoted to deterministic enforcement" — taking something from Tier 3 to Tier 1 when recurrence patterns confirm it needs mechanical enforcement.

---

## Impetus's Flywheel Integration

**[OFFICIAL]** Impetus (the orchestrating agent) integrates the flywheel at the subagent result synthesis stage. From the workflow-runtime.md:

> When any finding has `!` severity (critical):
> - If `momentum:upstream-fix` skill is available: offer flywheel trace — "This looks like it could be traced upstream. Want me to run a flywheel trace?"
> - If `momentum:upstream-fix` is NOT available: include deferral note naturally — "(flywheel processing deferred — Epic 6)"

**[OFFICIAL]** Minor findings never trigger flywheel offers. This is a deliberate calibration — the flywheel is reserved for systemic signals, not noise.

**[OFFICIAL]** The eval `eval-flywheel-offer.md` specifies: "Critical findings presented with no mention of flywheel processing" is explicitly a NOT EXPECTED behavior — confirming that the flywheel offer is a required behavior, not optional.

---

## What the Flywheel Is Not

**[OFFICIAL]** The PRD explicitly contrasts the flywheel against the Karviha approach: "[Karviha] demonstrates subagent review, custom skills, and iterative CLAUDE.md refinement — but lacks formal flywheel discipline. Improvements happen organically rather than through structured upstream trace." This establishes that the flywheel's defining characteristic is *formal structure* — the upstream trace hierarchy, the findings ledger, the consent gates, and the measurable health metrics — not merely the general practice of improving context over time.

**[UNVERIFIED]** The distinction implies that many practitioners informally improve their CLAUDE.md or rules files after noticing problems. Momentum's flywheel formalizes this as: an explicit trace through a hierarchy of fix levels, a structured ledger for accumulation and pattern detection, a consent gate before any fix is applied, and a health metric (ratio of upstream to code-level fixes) that makes the flywheel's operation visible and measurable.

---

## Current Implementation Status (as of 2026-04-10)

**[OFFICIAL]** From the master plan (`docs/planning-artifacts/momentum-master-plan.md`):
- Sprint lifecycle (planning → dev → AVFL → retro): **implemented**
- AVFL multi-lens validation: **implemented**
- Per-story code review (momentum:code-reviewer): **implemented**
- Architecture guard: **implemented**
- Retro with DuckDB transcript audit: **implemented**
- `momentum:upstream-fix` skill: **stub only** — "full implementation in Story 4.X"
- Findings ledger (`~/.claude/momentum/findings-ledger.jsonl`): **infrastructure defined but Epic 6 stories not started**
- Cross-story pattern detection (FR29): **not started**
- Automated flywheel with retrospective integration: **planned for growth phase**
- MCP server for findings query: **deferred to Epic 6**

**[OFFICIAL]** The master plan (Part 3, Future Epics) shows: "Practice Compounds (Epic 6) — Findings ledger, cross-story patterns, flywheel, health metrics — 5 backlog stubs, no story files."

**[OFFICIAL]** In the absence of the upstream-fix skill, Impetus acknowledges this explicitly: critical findings include a deferral note "flywheel processing deferred — Epic 6" rather than offering an active trace.

---

## Sources

Files read during this research:

- `/Users/steve/projects/momentum/CLAUDE.md`
- `/Users/steve/projects/momentum/README.md`
- `/Users/steve/projects/momentum/docs/planning-artifacts/momentum-master-plan.md`
- `/Users/steve/projects/momentum/docs/planning-artifacts/AI-Solo-Dev-Workflow-Plan-2026-03-07-final.md` (primary source — Sections 3.5, 4.3, 5.5, 6.x)
- `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/product-brief-momentum-2026-03-13.md`
- `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/prd.md`
- `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/epics.md`
- `/Users/steve/projects/momentum/skills/momentum/references/practice-overview.md`
- `/Users/steve/projects/momentum/skills/momentum/references/completion-signals.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/impetus/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/impetus/workflow-runtime.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/impetus/evals/eval-flywheel-offer.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/impetus/evals/eval-subagent-synthesis.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/upstream-fix/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/avfl/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/retro/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/retro/workflow.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/sprint-planning/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/sprint-dev/SKILL.md`
- `/Users/steve/projects/momentum/skills/momentum/skills/sprint-dev/workflow.md` (partial)
