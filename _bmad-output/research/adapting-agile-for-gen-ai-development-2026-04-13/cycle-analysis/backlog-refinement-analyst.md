---
date: 2026-04-13
phase: Backlog Refinement
role: Analyst
source_synthesis: ../synthesis/synthesis.md
---

# Backlog Refinement Phase — Analyst Findings

## Executive Summary

The Backlog Refinement phase is operationally thorough but conceptually misaligned with what the research says this phase should do in an AI-native practice. It is organized around **backlog hygiene** — artifact drift, status mismatches, priority reshuffling, epic taxonomy cleanliness, feature catalog maintenance — and it produces a sprint-ready queue of technically dense story files.

What it does not do, and what the research says matters most:

- It never produces a **Judgment Frame** per story (Intent / Done-state-for-a-stranger / Anti-goals / Review focus). The story that rolls out of `create-story` is a pure AI execution artifact with AC, Dev Notes, and a Momentum Implementation Guide — no sibling artifact optimized for human judgment.
- It never establishes a **North Star capability statement** or **value floor** for a feature before stories are elaborated. Elaboration happens directly from epic/PRD/architecture context against the requirements inventory, not against a minimum-viable-capability statement.
- `feature-grooming` **does** carry real value-mapping language (the multi-paragraph `value_analysis`, the `system_context`, the `acceptance_condition` in outcome form), but that language lives in a catalog (`features.json`) consumed by `feature-status`. It does not propagate into the stories that inherit from the feature. A story does not know its parent feature's value_analysis or acceptance_condition when it is being written.
- The three orchestration skills (`refine`, `epic-grooming`, `feature-grooming`) plus `create-story` together comprise roughly ~25 distinct workflow steps. Several of those steps are scope-cleaning (epic taxonomy, stale-story triage, priority reshuffling) and would still be needed regardless of AI; what's missing is the *AI-native* step that produces the human-judgment artifact the research identifies as the central gap.

The phase is doing too much of one thing (hygiene) and none of another (judgment-artifact production). It is not overbuilt in ceremony count — it is underbuilt in what the AI-native literature says this phase exists to do.

---

## What Exists and How It Aligns

### refine (orchestrator — 11 steps)

| Step | Produces | Research alignment |
|---|---|---|
| 1. Present backlog | Grouped by epic, priority distribution snapshot | Neutral — standard housekeeping |
| 2–3. PRD/architecture drift (2-wave) | Updated prd.md, architecture.md | Aligned with Fowler's "harness" framing — planning artifacts kept current so context-engineering works. But these are *artifacts written for humans* and the research is silent on whether PRD drift detection is the right AI-native mechanism |
| 4. Status hygiene scan | Status-mismatch findings | Operational hygiene — no research bearing |
| 5. Delegate to epic-grooming | Invokes epic-grooming | Structural delegation — see epic-grooming row below |
| 6. Stale-story individual evaluation | Keep/drop recommendations for low-priority, backlog, no-file stories | Loosely aligned with Shape Up's "no unshipped" / no backlog grooming principle — but applied as triage rather than as a structural constraint |
| 7. Re-prioritization conversation | Priority changes grounded in four heuristics (recurrence, workaround burden, forgetting risk, dependency) | Aligned with the spirit of ordinal value (no story points, no numeric velocity). The heuristics are thoughtful. But they do not ask "does this move us toward the value floor?" — the highest-signal heuristic per the research |
| 8. Assessment & decision review | Staleness, coverage gaps, ready gates | Aligned with provenance-by-default principle (internal). No direct research mapping |
| 9. Consolidated findings + batch approval | Approval gate | Aligned with "consent at every gate" — appropriate friction |
| 10. Apply approved changes | CLI-driven mutations, `create-story` invocations for missing stories | Appropriate delegation — refine stays orchestrator-pure |
| 11. Summary | Before/after priority distribution | Operational |

### epic-grooming (4 phases)

Operates on the `epic_slug` taxonomy: merges orphan slugs, creates new epic definitions, splits oversized epics. Every proposal requires explicit per-change approval.

This is a **taxonomy-cleanliness** skill. It has no research parallel in the AI-native literature — epics are a project-management concept, not an AI-native concept. The research's interest in this layer is whether the layer above stories (features, pitches, epics) is carrying the **value-mapping load**. `epic-grooming` does not do value mapping. It enforces categorical cleanliness (every slug resolved) but says nothing about what a user can do once the epic is complete.

Epics here are explicitly **categories** ("long-lived, never-closing groupings of related work" — workflow.md line 12). They are not the human-judgment unit the research identifies. That unit, in this codebase, is the feature.

### feature-grooming (6 steps)

This is the skill closest to what the research says the Backlog Refinement phase should be producing.

The feature schema includes:
- `type` in {flow, connection, quality} — a useful typology
- `value_analysis` — a **three-paragraph** structured block (current value / full vision including new capabilities / known gaps)
- `system_context` — how this feature fits the product
- `acceptance_condition` — in outcome form: "A developer can [action] and [observe outcome]"

This is real value-mapping. The three-paragraph value_analysis explicitly counters AI's "add nearby plausible features" failure mode (the research's Osmani citation) by naming what's *deferred* and what the *full vision* is. The "A developer can X and observe Y" form is directly what the research's Judgment Frame "Done-state-for-a-stranger" component asks for.

But it has two structural problems against the research:

1. **It's catalog-oriented, not story-oriented.** The output is `features.json` consumed by `feature-status` (an HTML dashboard generator). The rich value content does not propagate to stories. A story created under feature X does not inherit feature X's `value_analysis` or `acceptance_condition` into its spec.
2. **It treats the feature as a classification layer, not a commitment layer.** There is no "walking skeleton first" constraint, no North Star statement per feature, no pre-floor/post-floor state tracking. The feature carries a `status` field (`working|partial|not-started`) but that is a catalog status, not a commitment to "this sprint will cross the value floor for feature X."

### create-story (7 steps)

`create-story` delegates context-extraction to `bmad-create-story`, then does Momentum-specific work:
- Change-type classification (5 types)
- Injection of a "Momentum Implementation Guide" section with per-type implementation approach (EDD for skill-instruction, TDD for code, functional verification for rule-hook, direct implementation for config-structure, direct authoring for specification)
- Writes stories/index.json metadata
- Runs AVFL checkpoint on the story against the epic section as ground truth

This produces a dense, technically precise artifact for the AI. It is correctly optimized for AI execution.

What it does not produce: the Judgment Frame. There is no "Intent" block, no "Done-state-for-a-stranger", no "Anti-goals", no "Review focus". The ACs *are* the spec — which the research identifies explicitly as the failure mode (AC is too technical to be a glanceable human review anchor).

### create-story/references/change-types.md

This is a strong internal artifact — disambiguating skill-instruction vs. rule-hook vs. specification changes so the right implementation discipline is injected. Nothing the research directly requires, but it's sound context-engineering (Fowler) and probably reduces AI over-specification on small tasks (the Kiro "4 stories 16 ACs for one bug fix" failure mode).

### practice-overview and sprint-tracking-schema

Practice-overview lists eight principles. None of them is "value floor first" or "human-judgment artifact separate from AI execution artifact." The principles around "quality before speed" and "consent at every gate" approach the cognitive-load problem the research describes but from a gating-ceremony angle, not a judgment-artifact angle.

The sprint tracking schema carries `status`, `priority`, `epic_slug`, `depends_on`, `touches`, `change_type`. No field anchors a story to a feature's acceptance_condition or value_analysis. No field tracks pre-floor/post-floor sprint state. No field captures a Judgment Frame.

---

## Gaps: What the Research Says Should Exist

Mapped one-for-one against the synthesis's "Add these" recommendations.

### Gap 1 — Judgment Frame per story (synthesis §Problem 2, recommendation 2)

**Research prescribes:** a five-to-ten line block above the AC with Intent / Done-state-for-a-stranger / Anti-goals / Review focus. Produced during `create-story`.

**Current state:** Absent. `create-story` writes the story, injects the Momentum Implementation Guide, runs AVFL against epic intent — but produces no human-judgment artifact. The AC is the only spec a human can look at, and the research is explicit that the AC is not glanceable.

**Where it would go:** Inside `create-story` workflow.md, a new Step (between Step 2 and Step 3) that generates a Judgment Frame block and injects it at the top of the story file — above AC, above Dev Notes. Source material: the parent feature's `value_analysis` + `acceptance_condition` from features.json (if present) plus the epic section. Generated once at story creation; re-validated via AVFL against the feature's acceptance_condition as ground truth.

### Gap 2 — Feature-level Judgment Frame / North Star statement (synthesis §Problem 4, recommendation 1; §Problem 2, recommendation 3)

**Research prescribes:** Every feature must have a North Star capability statement before work begins — one sentence describing the minimum user-observable thing that makes the feature valuable at all. Plus a feature-level Judgment Frame answering "what job does this feature get done that it couldn't before?"

**Current state:** Partial. `feature-grooming` produces `value_analysis` (three paragraphs) and an `acceptance_condition` ("A developer can X and observe Y"). The `acceptance_condition` is close to a North Star in form. The three-paragraph value_analysis is close to a JTBD statement.

**What's missing:**
- The acceptance_condition is not explicitly a *minimum-viable* statement. A feature could have ACs that describe the full vision, not the floor. There is no field that says "this is the floor; everything else is additive."
- No pre-floor/post-floor state on features. No signal to the sprint-planning skill "this feature has not yet crossed its value floor, so sprint 1 must target walking skeleton."
- The `value_analysis` is rich, but it lives in `features.json` and is consumed by a dashboard. It does not drive sprint planning gates.

**Where it would go:** Extend `feature-grooming` feature schema with a `north_star: "Minimum user-observable thing that makes this feature valuable"` field (separate from `acceptance_condition` which can describe the full vision) and a `floor_status: pre-floor|post-floor` field.

### Gap 3 — Here-to-there gap artifact (synthesis §Problem 4, recommendations 3–5)

**Research prescribes:** At sprint close, ask: is the core capability reachable from where we are now? Track pre-floor/post-floor explicitly. No silent punts.

**Current state:** `refine` does many things at the boundary between sprints, but it does not produce a gap analysis. Its four re-prioritization heuristics are all **intra-backlog** heuristics (recurrence, burden, forgetting risk, dependency). None of them ask "are we closer to the value floor than last sprint?"

**Where it would go:** A new step in `refine` (or a new skill `gap-check` invoked by `refine`): for each active feature, diff today's running-app capability against the North Star statement. If no progress across two consecutive sprints on the same feature, surface a stop-and-reassess signal.

This is technically a sprint-close concern, but `refine` is the only phase where backlog-and-sprint boundaries are examined holistically, so it belongs here.

### Gap 4 — Feature → story value propagation

**Research prescribes:** Story-level Judgment Frame rolls up to feature-level Judgment Frame. The research treats feature and story as two audiences — human and AI — and expects the human layer to cascade into the AI layer.

**Current state:** `features.json` exists. Stories reference feature membership only transitively (through `epic_slug`). A story has no `feature_slug` field. `create-story` does not read `features.json`.

**Where it would go:** Two edits —
1. Add `feature_slug` to the stories/index.json schema (sprint-tracking-schema.md).
2. `create-story` Step 1 should resolve the story's feature from the epic taxonomy, read `features.json`, pull the parent feature's `value_analysis` and `acceptance_condition`, and use them as inputs to the Judgment Frame generation (Gap 1).

### Gap 5 — Walking skeleton discipline (synthesis §Problem 4, recommendation 2)

**Research prescribes:** Sprint 1 on any new feature must target end-to-end capability (however minimal), not elaboration.

**Current state:** Nothing in `refine`, `epic-grooming`, `feature-grooming`, or `create-story` enforces walking-skeleton ordering. The re-prioritization conversation in `refine` Step 7 is the place where this would bite, but the four heuristics do not include "is this a walking-skeleton story for a pre-floor feature?"

**Where it would go:** Either:
- Add a fifth heuristic to `refine` Step 7: "walking-skeleton promotion — if a feature is pre-floor, the smallest end-to-end story for it promotes to critical regardless of other heuristics."
- Or defer this to the sprint-planning phase and treat it as an out-of-scope concern for refinement. The research's structural argument is that walking-skeleton is a *sprint-planning* constraint; refinement just needs to make sure the feature's floor_status is known and the skeleton story exists in the backlog.

### Gap 6 — Anti-goals / "shall not" constraints (synthesis §Problem 2, recommendation 2c)

**Research prescribes:** Every story's Judgment Frame includes anti-goals: what this story is *not* doing. Directly counters AI's "add nearby plausible features" failure mode.

**Current state:** Absent. Stories have AC (positive constraints) and Dev Notes (context). No "shall not" block anywhere.

**Where it would go:** Part of the Judgment Frame in `create-story`. Source material: explicit negative boundaries from the feature's `system_context` ("this feature does X, adjacent feature Y is out of scope") + epic boundaries.

### Gap 7 — Risk tier / review focus metadata (synthesis §Problem 2, recommendation 7a; §Add these, recommendation 6)

**Research prescribes:** Risk-tiered review — reserve deep human read for security, auth, payments, business-logic boundaries. Osmani PR Contract.

**Current state:** Not present. All stories are reviewed uniformly; the only story-level metadata that affects review depth is `change_type` (which drives implementation discipline, not review discipline).

**Where it would go:** A `risk_tier` field on the story (values like `core`, `standard`, `cosmetic`) plus a `review_focus` free-text field. Part of the Judgment Frame. Generated during `create-story`.

---

## Removal Candidates

The research's "stop or re-task" list identifies things to drop. Mapping to this phase:

### RC-1 — The four re-prioritization heuristics, unchanged

The four heuristics in `refine` Step 7 (recurrence, workaround burden, forgetting risk, dependency) are all backward-looking or infrastructure-looking. None is forward-looking toward the value floor. They solve a genuine problem (backlog priority drift) but they solve it as if the AI-native shift did not happen.

**Proposed:** Keep the heuristics, but demote them below a new top-tier heuristic: *gap-to-floor priority*. A story that closes the value floor on a pre-floor feature promotes past all four existing heuristics. The four existing heuristics operate only among post-floor stories.

This is re-task, not removal.

### RC-2 — Stale-story individual evaluation (refine Step 6)

`refine` Step 6 evaluates low-priority backlog stories without files for keep/drop. This is genuine backlog hygiene.

The research's Shape Up citation is relevant: "no backlog grooming" is a deliberate Shape Up stance. Shape Up treats unshaped work as noise, not backlog. The Momentum position — keep low-priority stubs around and periodically triage them — is a middle ground.

**Proposed:** Keep, but tighten. Adopt Shape Up's "no unshipped" discipline: if a story has been in `backlog/low/no-file` state for more than N (say 3) sprints, the default recommendation flips from "evaluate" to "drop unless rescued." The present workflow's default is 50/50, which is too generous given the cost of carrying unshaped work.

### RC-3 — Epic-grooming as a standalone skill

`epic-grooming` is a taxonomy-cleanliness skill. Its existence is justified by the data model (every story has an `epic_slug`; orphan slugs accumulate). It does not do value mapping.

The research's implicit position: the value-mapping layer is the *feature*, not the epic. If epics are pure categorical bookkeeping — and the skill's own workflow.md line 12 says they are — then `epic-grooming` could be reduced from a separate invoked skill to a step inside `refine`. The 4-phase workflow (collect → analyze → review → apply) is the same shape as most of `refine`'s other steps.

**Proposed:** Do not remove, but consider folding into `refine` as Step 5a/5b if the orchestration overhead (separate task tracking, separate agent spawn) is not paying for itself. Evidence: `refine` already delegates to `epic-grooming` conditionally based on existence-check. If `epic-grooming` is always present in practice, the conditional and the delegation cost buy nothing.

### RC-4 — Separate `feature-status` HTML generator as the consumer of `features.json`

Outside the refinement phase strictly, but relevant: `features.json` is produced by `feature-grooming` and consumed by `feature-status` (an HTML dashboard). That consumption pattern is catalog-oriented. The research says features should drive sprint planning, story creation, and gap analysis — not primarily a dashboard.

**Proposed:** Do not remove the dashboard; it's useful. But stop treating `features.json` as a terminal artifact. The features need to flow into `create-story` (Gap 4) and into a sprint-close gap check (Gap 3).

### Net removal candidates

There is no single skill or step that is genuinely removable against the research's recommendations. The phase is lean in orchestration. Its problem is not excess steps — it is the absence of the judgment-artifact step the research identifies as central.

---

## Feature Layer Integration Opportunities

This is where the highest-leverage changes live. `feature-grooming` already has the right *shape* for the research's human-judgment layer. The integration problem is that the feature layer is disconnected from story production.

### Opportunity 1 — Make features drive create-story

Currently `create-story`'s Step 1 delegates all context extraction to `bmad-create-story`, which reads epics.md, architecture.md, previous stories, git, and the web. It does not read `features.json`.

If the story being created is known to belong to feature F (via a `feature_slug` added to the story stub before create-story runs, or resolvable from `epic_slug` via `features.json` stories[] membership), then `bmad-create-story` or the Momentum wrapper should pull:
- The feature's `value_analysis` — direct input to the Judgment Frame's Intent block
- The feature's `acceptance_condition` — direct input to the Judgment Frame's Done-state-for-a-stranger block
- The feature's `system_context` — direct input to anti-goals (bounds of this feature vs. adjacent features)

This is the closest thing to a ready-to-implement change in the entire analysis. The data exists. The consumer doesn't yet read it.

### Opportunity 2 — Make features carry floor state

Add two fields to the feature schema:
- `north_star`: one sentence — minimum user-observable thing
- `floor_status`: `pre-floor` | `post-floor`

`feature-grooming` Step 4 extends the value_analysis generation to include North Star extraction (the first paragraph of value_analysis is "current value delivered" — in pre-floor features this is empty or minimal; the first-delivery version is the North Star). `floor_status` is computed initially as `pre-floor` if `stories_done == 0`, flipped to `post-floor` only when a story with a specific `crosses_floor: true` metadata bit is merged.

### Opportunity 3 — Promote the feature to be the primary human-judgment unit (synthesis §Problem 2, recommendation 3)

The research's position: the story is the AI's unit; the feature is the human's unit. Ceremony that presumes per-story human judgment is ceremony that will fail under AI velocity.

The concrete shift: sprint review and retrospective (downstream of this phase) stop walking through stories and start walking through features. Did feature X progress this sprint? Is it post-floor yet? What's the next story that will close the gap?

Refinement's role in that shift: ensure the feature taxonomy is accurate enough to support feature-level review. Today's `feature-grooming` is capable of this but it is invoked as a bootstrap/refine cycle, not as a per-sprint ritual. If features become the review unit, `feature-grooming` needs to run *every* refinement cycle (at least the refine-mode path), not only when signals detect drift.

### Opportunity 4 — Features.json is already "ordinal" — exploit that

The research's §Q5 note on ordinal value is partially honored by features.json already: `value_analysis` is qualitative, `stories_done` / `stories_remaining` are counts but not aggregated into a single score. No story-point sum. No velocity number. This aligns with the research.

The opportunity is to make `feature-status` (the dashboard downstream) visualize this correctly — ordinal progress per feature, pre-floor/post-floor state — rather than count-based progress bars. Not a refinement-phase task per se, but a reminder that the current feature artifact is already closer to what the research wants than its consumers exploit.

### Opportunity 5 — Acceptance condition as AVFL ground truth for stories

Currently `create-story`'s AVFL step uses the epic section as `source_material` (create-story/workflow.md Step 6 note). If the story's feature is known, the feature's `acceptance_condition` is a tighter, more behavioral ground truth than the epic section. The epic section is category-level; the feature acceptance condition is outcome-level.

This is a small change (swap the source_material argument when feature is resolvable) with a real quality benefit.

---

## Questions Raised

These are for the owner to consider, not for the analyst to answer.

### Q1 — What is the primary output of Backlog Refinement?

The current workflow's answer: a cleaned backlog — hygiene done, priorities correct, epics tidy, features cataloged, stories ready for dev.

The research's answer: a set of features, each with a North Star, each with a Judgment Frame cascading into story Judgment Frames, each with a known floor status, ready for the sprint-planning skill to consume.

These are different outputs. The current workflow is rigorous about the first and silent about the second. Is the first output the one that matters? Or is the research right that the second is where the leverage lives?

### Q2 — Is the feature the primary unit of human judgment, or is the epic?

`epic-grooming` treats epics as categories. `feature-grooming` treats features as value units. Both exist. Stories reference `epic_slug` directly and `feature_slug` transitively (through features.json membership).

If the owner commits to "feature is the human-judgment unit," the data model should reflect that: stories carry `feature_slug` as first-class, epics become lighter (categorization only, as they already claim to be), and `feature-grooming` runs every refinement cycle rather than on signal.

If the owner commits to "epic is the unit," then `feature-grooming` is redundant with `epic-grooming` and should be absorbed.

The current state has both, with overlapping scope. The research is clear the unit should be one thing with judgment content.

### Q3 — Does the Judgment Frame live in the story file, the feature file, or both?

The research proposes per-story Judgment Frames rolling up to per-feature Judgment Frames. That is two artifacts per story-feature pair.

The alternative: Judgment Frame lives only at the feature level. Stories inherit and do not re-state. This is closer to Shape Up's pitch-driven model.

Single-source-of-truth argues for feature-only. But the research also warns that feature-level judgment is too coarse to catch AC-level failures inside the output. Story-level Judgment Frames exist precisely because feature-level is not enough.

This is a design decision the owner has to make. The current artifact has neither.

### Q4 — How does the value floor get named?

The research treats the value floor as a property of a feature. `feature-grooming`'s `value_analysis` already has a "Paragraph 1 — Current value delivered" structure, which is adjacent to this. But it's not the same question.

Concretely: for the nornspun example in the synthesis, the floor is "user types something, LLM answer appears." If that were a feature in `features.json`, `value_analysis` Paragraph 1 today would describe that capability *once it is built*. Before it is built, Paragraph 1 would be empty — and nothing in the current schema signals "this feature has no current value yet; this is a pre-floor feature."

Does the schema need a separate `north_star` field, or does Paragraph 1 of `value_analysis` absorb that duty with a schema rule ("Paragraph 1 must contain a minimum-viable statement even if not yet delivered")? The latter is cheaper. The former is clearer.

### Q5 — What is `refine`'s job when there are no hygiene findings?

If the backlog is clean — no drift, no status mismatches, no stale stories, no epic orphans, no feature drift — `refine` produces "✓ Backlog is healthy — no issues detected requiring action" and exits.

Under the research's framing, "no hygiene findings" does not mean "nothing to do." It means the hygiene work is done and the judgment-artifact work can begin — generate Judgment Frames for new stories, check floor status of active features, produce the here-to-there gap report.

Should `refine` be reframed so that hygiene is the *precondition* for its real work (judgment artifacts and gap check), not the entire work?

### Q6 — Can `create-story` be AVFL-validated against the Judgment Frame itself?

Currently AVFL uses the epic section as ground truth for whether the story captures epic intent correctly. If a Judgment Frame is added, AVFL could use the Judgment Frame as ground truth for whether the AC and Dev Notes actually implement the intent/done-state the human has approved. This is a cleaner ground-truth chain:

Feature acceptance_condition → Story Judgment Frame (human-approved) → Story AC + Dev Notes (AVFL-validated against Judgment Frame) → implementation (AVFL-validated against AC)

This would tie the two artifacts (judgment and execution) together formally, rather than leaving them as parallel documents.

### Q7 — Is `bmad-create-story` the right upstream?

`create-story` delegates all context extraction to `bmad-create-story`. `bmad-create-story` reads epics, architecture, previous stories, git, and the web. It does not read `features.json`. It has no concept of a Judgment Frame.

If the owner commits to feature-as-judgment-unit and Judgment-Frame-in-story, `bmad-create-story` either needs to be extended (push work upstream into BMAD) or wrapped more thickly by `create-story` (Momentum does the feature resolution + Judgment Frame generation; BMAD does the rest).

The wrapping option preserves BMAD as-is and concentrates the AI-native additions in Momentum. This seems cheaper but makes `create-story` larger. The extending option is invasive but cleaner.

### Q8 — Does the phase-name "Backlog Refinement" still fit?

The research reframes the phase that precedes sprint planning as spec-production, shaping, or pitch-preparation — not "backlog refinement." The Momentum name is inherited from classical Agile.

If the output is changing (judgment artifacts, not hygiene), the name probably should too. Candidates: "Shaping," "Feature Prep," "Spec-Ready," "Pre-Sprint Prep." Naming is trivial relative to the work, but it signals the intent.
