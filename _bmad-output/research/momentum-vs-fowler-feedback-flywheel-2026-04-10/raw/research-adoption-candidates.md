---
content_origin: claude-code-subagent
date: 2026-04-10
sub_question: "Of the novel Fowler concepts identified, which are highest-value candidates for adoption into Momentum's processes?"
topic: "Momentum Flywheel vs. Fowler's Feedback Flywheel — Conceptual Comparison"
---

# Fowler Feedback Flywheel — Adoption Candidates for Momentum

**Research date:** 2026-04-10
**Primary sources:** Fowler/Garg series on martinfowler.com (fetched directly); Momentum codebase at `/Users/steve/projects/momentum`

---

## Executive Summary

Fowler's Feedback Flywheel series (authored by Rahul Garg, Thoughtworks) articulates five clusters of practice that systematically capture AI-session learnings and feed them back into shared infrastructure. Momentum already has significant architectural overlap with several of these concepts — particularly in its retro workflow, AVFL quality gate, and upstream-fix skill stub. The highest-value gap is **Signal Classification and Routing**: Momentum captures raw sprint-log events but has no typed taxonomy that routes signals to specific artifact destinations. The second-highest gap is **Artifact Distillation** — the retro workflow produces findings documents but does not yet close the loop by updating rules files, CLAUDE.md sections, or skill references. Both are implementable within Momentum's existing skill architecture at low-to-medium effort.

---

## Scoring Framework

Each concept is scored on four dimensions (1–5 scale, 5 = highest):

| Dimension | What it measures |
|---|---|
| **Impact** | How much would adoption improve quality, velocity, or learning compounding? |
| **Fit** | How cleanly does it map to Momentum's existing skill/sprint/agent patterns? |
| **Effort** | Inverse of implementation effort — 5 means very low effort, 1 means very high |
| **Risk** | Inverse of risk — 5 means minimal risk, 1 means high risk of overhead or false positives |

**Priority score** = Impact + Fit + Effort + Risk (max 20).

---

## Candidate 1: Signal Classification and Routing

**Priority score: 18/20** — Highest priority

### What Fowler Describes

Garg's framework classifies learning signals into four typed categories: **Context Signal** (priming document gaps), **Instruction Signal** (effective prompts/phrasings), **Workflow Signal** (successful task decompositions), and **Failure Signal** (root-cause of AI failures). The key mechanism is that each signal type routes to a specific artifact destination — a context signal goes to the priming doc, a failure signal goes to anti-pattern documentation or a guardrail, a workflow signal becomes a team playbook entry. Without this routing, all signals collapse into undifferentiated "notes" that nobody acts on. [OFFICIAL — martinfowler.com/articles/reduce-friction-ai/feedback-flywheel.html]

### What Momentum Has Today

Momentum's sprint logs capture events as JSONL (e.g., `impetus.jsonl`, `hooks-observability.jsonl`), storing `timestamp`, `agent`, `story`, `sprint`, `event`, and `detail` fields. The retro workflow's `auditor-human` agent already identifies patterns categorized as: corrections, redirections, frustration signals, praise/approval, and decision points. However, these categories are **retro-analysis outputs**, not real-time signal types. There is no taxonomy applied at the moment of observation, and no mechanism that routes a classified signal to its correct artifact destination. The `upstream-fix` skill is a stub ("Upstream fix skill — full implementation in Story 4.X"), which is exactly where this routing logic would live. [OFFICIAL — codebase read of `/Users/steve/projects/momentum/skills/momentum/skills/retro/workflow.md` and `.claude/momentum/sprint-logs/sprint-2026-04-08/impetus.jsonl`]

### Scoring

| Dimension | Score | Rationale |
|---|---|---|
| Impact | 5 | Directly unlocks the compounding mechanism — without routing, captured signals evaporate |
| Fit | 5 | Maps perfectly to the upstream-fix skill stub already planned; retro already captures proto-signals |
| Effort | 4 | Medium — requires defining the taxonomy and routing table; upstream-fix is already stubbed |
| Risk | 4 | Low risk — additive to existing retro flow, not replacing it |

### Implementation Sketch

**New element: Signal taxonomy embedded in the retro documenter prompt**

Extend the `auditor-human` prompt in `retro/workflow.md` to classify each finding using the four-type taxonomy at time of capture:

```
type: context_signal | instruction_signal | workflow_signal | failure_signal
destination: rules/{rule-file} | CLAUDE.md#{section} | references/{doc} | skills/{skill}/workflow.md
```

**New element: `momentum:upstream-fix` implementation (Story 4.X)**

The stub already exists. Full implementation routes each classified signal to its artifact:
- `context_signal` → proposes addition to project's `CLAUDE.md` context section
- `instruction_signal` → proposes addition to relevant skill's references or a new rule file
- `workflow_signal` → proposes addition to a skill's `workflow.md` step
- `failure_signal` → proposes addition to a `rules/anti-patterns.md` file or an AVFL dimension

**Minimal starting point:** Add a `signal_type` field to the findings document's "Priority Action Items" table in `retro/workflow.md`. This costs one line per finding and seeds the routing data without requiring the full upstream-fix skill to exist yet.

---

## Candidate 2: Artifact Distillation

**Priority score: 16/20** — Second priority

### What Fowler Describes

Garg describes the practice of reviewing raw AI sessions and converting learnings into curated priming documents, playbooks, and standards. The mechanism is explicit: after a session (or sprint), the developer asks "what should change for the next one?" and updates the relevant artifact immediately while the lesson is fresh. The emphasis is on **human curation** — not auto-extraction, but deliberate selection of what earns permanent encoding. Artifacts under evolution include priming documents, generation/review instructions, team playbooks, and anti-pattern documentation. [OFFICIAL — martinfowler.com/articles/reduce-friction-ai/feedback-flywheel.html]

### What Momentum Has Today

Momentum's retro workflow produces a `retro-transcript-audit.md` findings document with a "Priority Action Items" section and creates story stubs in the backlog. This is powerful — but the loop stops there. The findings become backlog items that require sprint planning, selection, development, and merge before they affect the rules or skill files that future sessions consume. There is no lightweight path from "finding" to "rule update" that can happen in minutes rather than sprints.

The `momentum:intake` skill exists for fast story capture. The `momentum:decision` skill captures strategic decisions. The `momentum:plan-audit` skill adds spec impact sections. None of these close the artifact distillation loop directly. [OFFICIAL — codebase reads of `/Users/steve/projects/momentum/skills/momentum/skills/retro/workflow.md`, `intake/SKILL.md`, `decision/SKILL.md`]

### Scoring

| Dimension | Score | Rationale |
|---|---|---|
| Impact | 5 | This is the core flywheel mechanism — without it, findings accumulate but don't compound |
| Fit | 4 | Maps to retro Phase 5, but needs a new "lightweight distillation path" that bypasses sprint queue |
| Effort | 3 | Medium — requires a new lightweight skill or an extension to retro Phase 5 |
| Risk | 4 | Low risk — can coexist with backlog path; distillation is additive |

### Implementation Sketch

**New skill: `momentum:distill`**

A lightweight skill invocable from retro Phase 5 or directly. Takes the findings document and proposes immediate (non-sprint-queued) updates to rules files and references:

```
Input: retro-transcript-audit.md findings
Output: git diff proposals for:
  - ~/.claude/rules/*.md (global rules affected)
  - skills/momentum/references/*.md (shared references affected)
  - CLAUDE.md additions
```

The distill skill distinguishes two artifact tiers:
- **Tier 1 (immediate):** Small, low-risk updates to rules files — anti-patterns, voice rules, routing notes. These can commit directly without a full story.
- **Tier 2 (sprint-queued):** Structural changes to skill workflows, new sub-skills, AVFL dimension additions. These become backlog stubs.

**Integration point:** Retro Phase 5 presents an additional question after story stub approval: "Would you like me to propose immediate rule/reference updates from these findings?" This invokes `momentum:distill` before sprint closure.

**Minimal starting point:** A single step added to retro Phase 5 that reads the findings document and outputs a `## Proposed Immediate Updates` section — just text proposals, no file writes, for developer review. This establishes the habit without requiring the full skill.

---

## Candidate 3: Structured Feedback Cadences

**Priority score: 14/20** — Third priority

### What Fowler Describes

Garg specifies four nested timeframes for feedback practice: per-session (immediate reflection), daily stand-up (single question surfacing one discovery), sprint retrospective (dedicated agenda item), and quarterly (artifact currency review). The key insight is that **cadence determines whether learnings accumulate or evaporate** — without scheduled moments for reflection, even teams with good intentions let signals fade. The daily stand-up addition is particularly novel: it adds a low-overhead signal capture point between session-level and sprint-level cadences. [OFFICIAL — martinfowler.com/articles/reduce-friction-ai/feedback-flywheel.html]

### What Momentum Has Today

Momentum operates at two cadences: per-story (AVFL runs on every story) and per-sprint (retro closes each sprint). There is no daily or per-session reflection mechanism. The Impetus greeting generates a `planning_context` narrative from sprint state, but this is a status summary, not a learning-capture prompt. The `momentum:intake` skill is the closest analog — it captures ideas fast — but is not positioned as a reflection cadence. [OFFICIAL — practice-overview.md, impetus/SKILL.md]

### Scoring

| Dimension | Score | Rationale |
|---|---|---|
| Impact | 4 | Per-session and daily cadences would capture signals that currently evaporate between sprints |
| Fit | 3 | Fits the Impetus greeting pattern but requires behavioral change from the developer |
| Effort | 4 | Low effort for a minimal implementation; Impetus already has the right interaction surface |
| Risk | 3 | Medium risk of becoming overhead if the prompt feels like a survey |

### Implementation Sketch

**Minimal: Per-session reflection prompt in Impetus greeting**

The Impetus happy-path greeting already has a closer (`greeting.closer`). Extend the preflight logic to occasionally append a reflection prompt: "Last session, did anything make you correct the agent mid-task? If yes, `intake` it now."

This adds zero overhead for sessions with no notable events (developer types "no") and routes notable events to `momentum:intake` in one step.

**Structured: Retro micro-section for daily learnings**

Add a `## Daily Captures` section to the sprint-log schema — a simple append-only file at `.claude/momentum/sprint-logs/{{sprint_slug}}/daily-captures.md`. Impetus session close (or the per-session reflection) appends a timestamped one-liner. Retro Phase 2 includes this file in the DuckDB extraction. This gives retro auditors additional signal without changing the core transcript audit.

**Anti-pattern to avoid:** A formal daily stand-up question that the AI asks unprompted. In a solo-dev context, unsolicited structured check-ins become abandoned overhead quickly. The Fowler pattern assumes a team context; in Momentum's solo model, the reflection must be opt-in and ultra-lightweight.

---

## Candidate 4: Team Standard Encoding

**Priority score: 13/20** — Fourth priority

### What Fowler Describes

Garg's "Encoding Team Standards" article (separate from the Feedback Flywheel article, part of the same series) describes a framework for converting senior engineers' tacit knowledge into versioned, executable instructions stored in the repository. The article specifies a four-element anatomy for each instruction: role definition, context requirements, categorized standards (mandatory/recommended/optional), and output format. The critical distinction from documentation: standards become **executable governance** — embedded in prompts that run automatically, not descriptions that people must remember to apply. [OFFICIAL — martinfowler.com/articles/reduce-friction-ai/encoding-team-standards.html]

### What Momentum Has Today

Momentum's `agent-guidelines` skill does precisely this: it discovers the project stack, researches breaking changes, and generates path-scoped rules and reference docs. The `avfl` skill encodes review standards as adversarial validator and enumerative validator sub-agents. The authority hierarchy (`global → project → session`) is a versioned, cascading standard enforcement mechanism. The `code-reviewer` skill encodes review judgment. [OFFICIAL — codebase reads of `agent-guidelines/SKILL.md`, `avfl/SKILL.md`, `code-reviewer/SKILL.md`, `references/rules/authority-hierarchy.md`]

### Scoring

| Dimension | Score | Rationale |
|---|---|---|
| Impact | 3 | Moderate — Momentum already covers most of this with agent-guidelines + AVFL dimensions |
| Fit | 4 | Very high fit — Momentum's existing skill patterns match Fowler's instruction anatomy exactly |
| Effort | 3 | Medium — value is in filling specific gaps, not a wholesale new capability |
| Risk | 3 | Medium risk of over-prescribing rules that produce false positives in AVFL |

### Gap Analysis and Implementation Sketch

The concept is substantially covered. The gap is in **Fowler's four-element instruction anatomy** not being uniformly applied to all Momentum skill system prompts. Some skills lack explicit categorized standards (mandatory/recommended/optional) and output format specifications.

**Specific gap: AVFL dimension priority encoding**

Fowler's categorized standards hierarchy (mandatory/recommended/optional) maps naturally to AVFL scan dimensions but is not currently formalized in the AVFL sub-skill prompts. Adding a `severity_tier` field to AVFL dimension definitions would encode this hierarchy explicitly.

**Specific gap: Knowledge extraction during agent-guidelines**

The agent-guidelines workflow generates rules, but it doesn't systematically extract and encode the "what causes immediate review rejection" class of knowledge — the implicit rejection criteria that experienced developers apply instinctively. Adding a structured extraction step to `agent-guidelines/workflow.md` that asks these questions before generating rules would strengthen the output.

**Minimal starting point:** Add Fowler's four-element anatomy as a checklist to `skills/momentum/references/agent-skill-development-guide.md` — the authoritative source for skill conventions. New skills get reviewed against it automatically.

---

## Candidate 5: Frustration Loop Tracking

**Priority score: 12/20** — Fifth priority

### What Fowler Describes

Garg introduces the "Frustration Loop" concept to name what happens when AI generates contextually wrong output requiring extensive revision. He recommends measuring where these loops occur by tracking: first-pass acceptance rates, iteration cycles per task, post-merge rework frequency, and principle alignment. The purpose is to identify **which tasks or contexts generate the most friction**, directing priming and standard investments to high-ROI targets. [OFFICIAL — martinfowler.com/articles/reduce-friction-ai/feedback-flywheel.html]

Note on attribution: the 45-minute/5-minute revision example ("code requiring 45 minutes of revision might need only 5 minutes of review with proper priming") appears in the Knowledge Priming article, where it illustrates the benefits of Knowledge Priming — not as part of the Frustration Loop definition itself. The Frustration Loop is defined through its cycle of misaligned output and repeated correction, independent of this specific example. [OFFICIAL — martinfowler.com/articles/reduce-friction-ai/knowledge-priming.html]

### What Momentum Has Today

The retro workflow's `auditor-human` agent already identifies "frustration signals: repeated asks, escalating tone, explicit complaints" in user messages. The `auditor-execution` agent tracks "story iteration: stories with many dev agents (why did story X need N passes?)." The sprint log JSONL schema captures events per-story and per-agent. However, **no metric is computed or tracked over time** — frustration signals are identified in each retro but not accumulated into a trend. There is no "first-pass acceptance rate" metric that persists across sprints to show improvement or degradation. [OFFICIAL — retro/workflow.md Phase 4 auditor prompts]

### Scoring

| Dimension | Score | Rationale |
|---|---|---|
| Impact | 4 | Trend data would identify highest-ROI improvement targets — currently invisible |
| Fit | 3 | The retro already surfaces these signals; the gap is aggregation and persistence |
| Effort | 2 | Requires schema additions, a metrics store, and a trend-query mechanism |
| Risk | 3 | Medium risk of gaming metrics or over-optimizing proxies |

### Implementation Sketch

**New element: Sprint metrics ledger**

Add a `metrics.json` to each sprint directory at close time, computed from the retro findings:

```json
{
  "sprint": "sprint-2026-04-08",
  "frustration_signals": 3,
  "corrections": 7,
  "story_iteration_counts": { "story-slug": 2, "other-story": 1 },
  "first_pass_acceptance_rate": 0.6,
  "tool_errors": 12
}
```

The retro documenter agent populates this as part of Phase 4 synthesis (it already has all the data). The `momentum-tools` script gains a `metrics trend` command that DuckDB-queries the ledger across sprints.

**New element: Trend display in Impetus greeting**

When a frustration signal trend is worsening (e.g., corrections increasing sprint-over-sprint), the Impetus `planning_context` includes a "! Friction trend: corrections up 40% vs. last sprint — consider running distill before starting."

**Minimal starting point:** Add a `## Metrics` section with standard fields to the retro findings document template (it already has a `## Metrics` table). Standardize the field names so they're machine-readable by a future aggregation step. The retro documenter already fills this table — standardizing it costs nothing.

---

## Prioritized Ranking Summary

| Rank | Concept | Score | Primary Recommendation |
|---|---|---|---|
| 1 | Signal Classification and Routing | 18/20 | Implement as `upstream-fix` Story 4.X + signal_type field in retro findings |
| 2 | Artifact Distillation | 16/20 | Implement `momentum:distill` skill; add to retro Phase 5 as optional invoke |
| 3 | Structured Feedback Cadences | 14/20 | Extend Impetus greeting with per-session reflection prompt; add daily-captures.md |
| 4 | Team Standard Encoding | 13/20 | Add Fowler four-element anatomy to agent-skill-development-guide.md |
| 5 | Frustration Loop Tracking | 12/20 | Standardize retro metrics table fields; add Sprint metrics ledger |

---

## Cross-Cutting Observations

**Momentum's structural advantage:** Momentum already operates at the "after foundational infrastructure exists" level that Garg explicitly says is a prerequisite for the Feedback Flywheel. Knowledge priming (`CLAUDE.md`, rules cascade), design-first collaboration (story/epic/spec structure), context anchoring (sprint logs, decision records), and team standard encoding (AVFL, agent-guidelines) are all substantially implemented. Momentum is positioned to adopt the Flywheel layer directly — not from scratch. [PRAC]

**The critical gap:** Fowler's flywheel turns on one mechanism that Momentum currently lacks: a **direct path from session learning to artifact update** that does not require queuing a story, running a sprint, and merging a branch. The retro-to-backlog path is valuable for structural changes. But the Fowler mechanism also requires a lightweight path for small, immediate updates — the kind that take "minutes of effort when warranted." The `momentum:distill` skill (Candidate 2) combined with Signal Routing (Candidate 1) provides this missing path. [PRAC]

**Solo-dev adaptation required:** Fowler's daily stand-up cadence (Candidate 3) assumes a team. In Momentum's primary solo-dev context, this cadence requires adaptation to a per-session reflection prompt in Impetus rather than a team ceremony. The principle survives the adaptation; the ceremony does not. [PRAC]

**What Momentum has that Fowler doesn't:** The `momentum:upstream-fix` stub (once implemented) will trace quality failures upstream to their root cause in specs, rules, or workflows — a more systematic upstream tracing than anything in Fowler's framework. Fowler's Failure Signal is a category; Momentum's upstream-fix is a causal trace. Fowler's framework would benefit from this concept, not the other way around. [OFFICIAL — `/Users/steve/projects/momentum/skills/momentum/skills/upstream-fix/SKILL.md`]

---

## Sources

- [OFFICIAL] Garg, Rahul. "Feedback Flywheel." *martinfowler.com*, 08 April 2026. https://martinfowler.com/articles/reduce-friction-ai/feedback-flywheel.html
- [OFFICIAL] Garg, Rahul. "Encoding Team Standards." *martinfowler.com*, 31 March 2026. https://martinfowler.com/articles/reduce-friction-ai/encoding-team-standards.html
- [OFFICIAL] Garg, Rahul. "Knowledge Priming." *martinfowler.com*, 24 February 2026. https://martinfowler.com/articles/reduce-friction-ai/knowledge-priming.html
- [OFFICIAL] "Patterns for Reducing Friction in AI-Assisted Development." *martinfowler.com* series index. https://martinfowler.com/articles/reduce-friction-ai/
- [OFFICIAL] Momentum codebase: `/Users/steve/projects/momentum/skills/momentum/skills/retro/workflow.md` — retro Phase 4 auditor team prompts
- [OFFICIAL] Momentum codebase: `/Users/steve/projects/momentum/skills/momentum/skills/upstream-fix/SKILL.md` — upstream-fix stub
- [OFFICIAL] Momentum codebase: `/Users/steve/projects/momentum/skills/momentum/skills/impetus/SKILL.md` — Impetus greeting and routing
- [OFFICIAL] Momentum codebase: `/Users/steve/projects/momentum/skills/momentum/references/practice-overview.md` — eight principles
- [OFFICIAL] Momentum codebase: `.claude/momentum/sprint-logs/sprint-2026-04-08/impetus.jsonl` — sprint log schema
