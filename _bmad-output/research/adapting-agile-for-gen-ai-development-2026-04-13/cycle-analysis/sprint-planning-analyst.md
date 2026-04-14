---
date: 2026-04-13
phase: Sprint Planning
role: Analyst
inputs:
  - _bmad-output/research/adapting-agile-for-gen-ai-development-2026-04-13/synthesis/synthesis.md
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/sprint-manager/workflow.md
  - skills/momentum/skills/sprint-manager/references/state-machine.md
  - skills/momentum/skills/feature-status/SKILL.md
  - skills/momentum/references/practice-overview.md
  - skills/momentum/references/sprint-tracking-schema.md
---

# Sprint Planning Phase — Analyst Findings

## Executive Summary

Sprint Planning as currently practiced is a **story-centric, capacity-style, AC-first** workflow. It is well-engineered as a mechanical pipeline (10 steps, task-tracked, AVFL-gated, sprint-branch-isolated) and it is disciplined about separation of concerns (plain-English ACs for devs, Gherkin for verifiers, team-composition gate, spec-impact analysis into PRD/architecture).

Against the research, it has four structural gaps:

1. **No sprint goal or hypothesis.** The sprint is assembled bottom-up from prioritized stories; there is no value-level "what are we trying to learn/prove this sprint" statement that would make the sprint a governance/learning rhythm rather than a story-batch container. The research says this is the point of the sprint in an AI-native practice.
2. **No walking-skeleton / value-floor concept.** Planning cannot distinguish a pre-floor sprint (establish core capability) from a post-floor sprint (elaborate). Nothing forces Sprint 1 on a new feature to target end-to-end walking-skeleton capability. The "punting failure mode" in the research (5–10 sprints of spec-correct stories with zero user value) is not defended against.
3. **No here-to-there gap analysis at planning time.** The synthesis step (Step 1) reads PRD + product brief + previous sprint summary and derives "what matters most right now" — but it does not ask "what can a user do now / what is the minimum capability they must be able to do / what's the gap, and does this sprint close it?" Selection is priority-weighted, not gap-weighted.
4. **Capacity framing ("3–8 stories"), not appetite framing.** The only sizing constraint is a story-count band. There is no "appetite" (time I'm willing to spend) declared for the sprint or per story, and no check that the committed work fits the sprint's duration claim.

Additionally, the **human judgment unit is missing** — selection happens at the story level, but the research says the feature/pitch is the human's unit and the story is the AI's. There is no "feature in motion" view at planning time that lets the owner see whether the selected stories collectively move any feature toward its value floor.

Finally, the workflow's **ceremony cost is high for a solo practitioner** (10 steps, multiple subagent spawns, two validation gates, approval loop). This is proportionate only if planning produces something more than a sorted story list — and today, it mostly produces a sorted story list plus specs and team assignments.

---

## What Exists and How It Aligns

### Aligned with research

- **Dual-horizon bifurcation is explicit.** The workflow enforces "story files retain ONLY plain English ACs; Gherkin specs are written to `sprints/{sprint-slug}/specs/` exclusively for verifier agents" (Step 4, critical block). This directly matches Kurilyak's machine-actionable vs. human-readable split and the Codecentric isolated-specification-testing pattern.
- **Harness-engineering discipline is real.** The workflow delegates to subagents (create-story, agent-guidelines, AVFL, sprint-manager) with exclusive write authority per file. This matches Fowler's "humans on the loop, not in the loop" framing and the orchestrator-purity memory the owner has explicitly encoded (`feedback_orchestrator_purity_quickfix`, `feedback_impetus_orchestration_model`).
- **Spec impact analysis (Step 4.5) is the right shape.** Reading the selected stories against PRD + architecture and updating both in place is exactly the "harness iteratively corrects the spec" pattern Fowler advocates.
- **Outsider Test on Gherkin (Step 4) is rigorous.** Black-box behavioral language, AC-by-AC translation forbidden, structural validation gate after generation — this meets the research bar for behavioral validation specs.
- **Team-composition gate (Step 5.5) enforces role availability** before activation. This mirrors the research's "separate transcript from outcome" requirement by pre-declaring QA, E2E, and Architect Guard roles that will verify work independently of the implementer.
- **Sprint-branch isolation is clean.** All planning artifacts land on `sprint/{slug}` and merge only on completion. This is the right unit-of-coordination discipline; it's PR-centric in spirit if not in name.
- **Prior-sprint context carry-forward (Step 1, Phase A.5)** reads the previous sprint summary into "what matters now." This is a learning-cadence mechanic, consistent with Lindsay's "AI didn't kill the sprint — it exposed what sprints were really for."
- **Dependency waves (Step 5)** give a real execution plan, not a bag of tickets. This is better than what most team frameworks in the corpus publish.

### Partially aligned

- **Staleness check (Step 1, Phase B)** uses `git log` against `touches` paths to flag stories that may already be implemented. This is a real defect-prevention mechanism — but it is backward-looking (did the code change?), not forward-looking (does this sprint close a gap?).
- **Task tracking across the 10 steps** (Step 0) guards against context drift in a long workflow. This is good practice but is about workflow reliability, not about whether the sprint itself is pointing at value.
- **AVFL as a final gate (Step 6)** validates the sprint plan's coherence. But the profile is `checkpoint` and the stage is `final` — the gate asks "is this plan internally consistent?" not "does this plan move any feature toward its value floor?"

---

## Gaps: What the Research Says Should Exist

### Gap 1 — Sprint goal (hypothesis)

**Research position:** The sprint's purpose is "bounding the time the team will pursue a hypothesis before re-assessing" (Siderova/Lindsay). In AI-native work the sprint is a governance and learning rhythm, not a capacity container. The sprint is defined by *what we are trying to learn or prove*, then stories are chosen that serve that hypothesis.

**What's there today:** No sprint goal. Step 1 produces "what matters most right now" as a synthesis; Step 2 opens with "Select 3–8 stories for this sprint." There is no step between "understand context" and "select stories" where a goal is written down and then used to filter selection.

**Downstream effects:**
- Retro has no target to evaluate against. "Did we ship our stories" is the only question; "did we close the hypothesis we set" is never asked.
- Story selection is implicitly priority-weighted (critical > high > medium > low in Step 1, Phase C), not goal-weighted. A high-priority story unrelated to the sprint's (unstated) goal can crowd out a lower-priority story that would close it.
- The `sprint-summary.md` artifact used by the next sprint's planning (Step 1, Phase A.5) has no goal-rollup section, so the learning signal across sprints is narrative rather than structural.

### Gap 2 — Walking skeleton / value floor / pre-floor vs. post-floor

**Research position:** "The punting failure mode happens specifically when sprints are elaborating on a skeleton that hasn't been built yet." Every feature has a value floor — the minimum capability below which all delivery has zero user value. Sprint 1 on any new feature targets the walking skeleton; subsequent sprints elaborate. Pre-floor and post-floor sprints are categorically different.

**What's there today:** Nothing. There is no concept of "value floor" in any planning artifact (story, feature, epic, sprint record, PRD schema, architecture). There is no question asked during planning of the form "is this feature pre-floor or post-floor, and does this sprint cross the floor?" The feature-status skill exists (see "Feature Layer Integration" below) but is not wired into planning.

**Downstream effects:**
- Three to five high-priority stories that each elaborate different features can be selected into a single sprint, none of which crosses a value floor. Every story passes AC; no feature ships.
- Sprint selection cannot distinguish "this sprint builds the walking skeleton for feature X" from "this sprint polishes three already-walking features." The retro cannot tell them apart either.
- The "here-to-there gap" the owner describes is not a queryable artifact; it only exists as the owner's mental model, which is exactly the single point of failure the research warns about.

### Gap 3 — Here-to-there gap analysis at planning time

**Research position:** "Before sprint planning begins and reviewed at sprint close" there should be a gap artifact answering: (1) what can a user do now, (2) what is the minimum valuable capability, (3) what is the gap, (4) does the sprint close it.

**What's there today:** Planning reads `prd.md`, `product-brief`, and `sprint-summary.md` (previous). None of these answer "what can a user do *right now* with the running system?" The synthesis in Step 1 operates entirely on planning intent (what's prioritized) rather than on system state (what's usable). There is no `status.md`, no user-journey-as-is artifact, no current-capability description referenced.

**Downstream effects:**
- Stories are selected against a prioritization model, not against a capability-gap model.
- The synthesis's "what matters most right now" is a ranking exercise; it cannot answer "are we pointed at the destination."

### Gap 4 — Appetite vs. capacity framing

**Research position:** "Use Shape Up's 'appetite' concept for sizing. Instead of estimating story points or hours, declare an appetite ('I'm willing to spend half a day on this') and fix scope to fit. Appetite is ordinal, not cardinal."

**What's there today:** The only sizing primitive is the story-count band "3–8 stories" (Step 2). There is no time-box declaration on the sprint (no "this sprint runs X days"), no per-story appetite, and no check that selected scope fits the declared duration. The research is explicit that one-week cadence is about right for solo AI-native practice; the workflow is silent on cadence.

**Downstream effects:**
- "Did we fit" has no reference to compare against at retro.
- The sprint-level time commitment is implicit; the owner cannot see at planning time "I'm committing to spend 1 week on this" vs. "3 days" and scope accordingly.
- Story-count is a proxy for effort that loses its meaning as stories vary in size. A 3-story sprint of three walking-skeleton stories is enormous; an 8-story sprint of eight polish stories is small. The workflow treats them the same.

### Gap 5 — Feature-level commit vs. story-level commit

**Research position:** "The story is the AI's unit. The feature — or the 'shaped pitch' — is the human's unit." Human judgment (selection, prioritization, goal-setting) should happen at the feature/pitch level; story-level work is decomposition for AI execution.

**What's there today:** Selection, approval, and activation all happen at the story level (Step 2 prompt, Step 7 approval prompt). Features/epics exist in the data model (`epic_slug` in stories/index.json) and are used for grouping in the backlog display (Step 1's "[Epic: epic-slug-1]" grouping), but they are not the commit unit. There is no "sprint commits to advancing features X and Y" framing, and no feature-level view of "how much of this feature remains" at planning time.

**Downstream effects:**
- Owner reviews a list of story titles at Step 7 and must mentally aggregate them back to features to judge "is this sprint coherent at a feature level." This is the exact review-mode-vs-generative-mode failure the Vibe-Check paper describes: the brain can pattern-match "yes this list looks right" while missing that no feature actually advances meaningfully.
- The `feature-status` skill (which exists and produces HTML feature coverage) is not invoked during planning. Planning has no "features advanced this sprint" view.

### Gap 6 — Cadence and duration

**Research position:** One-week governance rhythm + event-driven execution. Two weeks is the ceiling. Sprint is for inspect-and-adapt, not for throttling.

**What's there today:** No declared cadence. The sprint slug is `sprint-YYYY-MM-DD` (planning date), and `completed` is set at close — so the duration is implicit and variable. There is no "we are committing to a 1-week sprint" statement and no cadence enforcement.

**Downstream effects:**
- Owner cannot say "our sprints run 1 week" and be held to it — because nothing holds them to it.
- Sprints that stretch (a story blocks, a spec revision loops) have no explicit signal to force a cutoff/rescope.

### Gap 7 — Ceremony proportionality for solo practice

**Research position:** For a solo AI-first practice, "weekly governance + PR-centric continuous flow" is the cadence the literature converges on. Ceremony should be lightweight.

**What's there today:** Sprint planning has 10 steps (including 4.5 and 5.5), multiple subagent spawns (create-story, agent-guidelines, AVFL, discovery agents, update agents), two approval gates (story-level in Step 3, sprint-level in Step 7), and a team-composition audit. For a 3-story sprint, this can mean >15 subagent invocations before a single line of code is written.

**Observations:**
- Steps 4.5 (spec impact) and 5.5 (team-composition validation) are defensible gates, but they assume stories are novel and large. For a small-delta sprint, they may be expensive relative to their yield.
- The 3–8 story floor means sprints below 3 stories are not supported by the workflow. Yet the research explicitly argues for shorter cycles, and a one-story walking-skeleton sprint is the most valuable sprint to run early on a new feature. The workflow cannot produce it.
- The guidelines-verification gate (Step 5) is the right idea but is invoked on every sprint even when guidelines haven't changed. A caching/skip heuristic would reduce friction.

---

## Removal Candidates

None of these should be removed without discussion — each is doing something. But each is a candidate to re-scope or make conditional.

1. **The 3-story floor (Step 2).** This forces the sprint into "batch mode" and prevents the most research-aligned sprint shape: a single walking-skeleton story that crosses a feature's value floor. Consider replacing "3–8 stories" with "1 or more stories; provide an appetite in days."

2. **The full team-composition build for every sprint (Step 5).** Role assignment, specialist domain matching, and guidelines verification run every sprint. For a continuing sprint on the same feature-area, the team composition is likely identical to the prior sprint. Consider caching and only running this step when `touches` paths introduce new specialist domains.

3. **The post-generation Gherkin validation pass (Step 4).** Structural validation (indentation, scenario naming, outsider-test compliance) could be a precommit hook or AVFL concern rather than a blocking step in planning. Running it inline in Step 4 means a spec regeneration loop blocks the whole planning flow.

4. **The separate discovery / update subagent pairs in Step 4.5.** Two discoveries (arch + PRD) then two updates (arch + PRD) is four subagent spawns. A single spec-impact agent that does discover + update in one pass against both documents would halve the cost for the common case (no major impact). The split makes sense only when impact is large and concurrent updates collide — which is a rare case.

5. **Step 1 Phase B (staleness check) run unconditionally.** This runs `git log` for every non-terminal story in the backlog. On a large backlog this is slow and usually produces no findings. Consider running it only on the final selected stories (after Step 2), or only when `stories/index.json.last_validated` is older than N days.

6. **The dual approval loop (Step 3 per-story approval + Step 7 sprint approval).** Per-story approval in Step 3 is the right place to catch story-level drift. But the sprint-level approval in Step 7 then makes the owner re-review the same stories in aggregate. If Step 3 produced approved stories, Step 7 could be limited to approving the *wave plan and team composition*, not re-approving the story list.

---

## Feature Layer Integration Opportunities

The data model already treats features/epics as first-class (`epic_slug` in every story; epics are a grooming target; `feature-status` skill generates an HTML feature-coverage view). The planning workflow does not use this.

Opportunities, ranked by research leverage:

1. **Sprint goal as feature movement.** Replace "select 3–8 stories" with "declare 1–3 features this sprint will advance, then select stories that advance them." The sprint goal becomes a list of feature slugs + one-sentence feature-level hypothesis each. Story selection is then filtered/validated against the goal: every selected story must either advance a listed feature or be tagged as "infrastructure for goal feature X."

2. **North Star capability statement per feature, referenced at planning.** Each feature gets a one-sentence value-floor statement (separate from the feature description). Planning's Step 1 synthesis surfaces, for each goal-feature: (a) value floor statement, (b) current status (pre-floor or post-floor), (c) what crossing the floor would look like. This is the here-to-there gap artifact.

3. **Invoke `feature-status` during Step 1.** Before selecting stories, the workflow could generate the feature-status HTML (the skill already exists) and open it in a browser pane. The owner sees at a glance which features are advanced/stalled/untouched, which gives selection a feature-aware context instead of a story-list context.

4. **Feature-level Judgment Frame at Step 7.** Step 7 currently displays stories grouped by wave. A feature-centric rollup — "Feature: X — currently at state S; after this sprint, expected at state S'; stories contributing: a, b, c" — would let the owner verify feature movement rather than story movement. This directly addresses the research's "human's unit is the feature" point.

5. **Pre-floor / post-floor tagging on the sprint record.** Each sprint gets tagged per-feature as `pre-floor` (goal: cross the walking skeleton) or `post-floor` (goal: elaborate existing capability). The sprint record in `sprints/index.json` gains a `feature_goals: [{feature_slug, state, hypothesis}]` section. Retro then has a queryable artifact to evaluate: "did we cross the floor we said we would?"

6. **Feature membership in wave planning.** Currently waves are computed from story dependencies. A secondary view of "waves by feature" — which features are worked in parallel? which are serialized? — would surface cases where one sprint fragments attention across too many features to close any of them.

7. **Feature-level AVFL stage.** AVFL today validates sprint-plan internal consistency. A second AVFL pass (or an extended profile) asking "does this sprint plan move any listed feature past its value floor, or explicitly justify why it's pre-requisite elaboration?" would encode the gap-check discipline directly into the gate.

---

## Questions Raised

These are for the owner — not decisions, not recommendations.

1. **Is the sprint a hypothesis unit or a batch unit?** The workflow today treats it as a batch (3–8 stories, prioritized). The research treats it as a hypothesis-bounding window. If Momentum wants the learning-cadence role the research describes, planning needs a sprint-goal step. Is that worth adding?

2. **Should the commit unit at planning be the feature, not the story?** The current Step 2 prompt ("Select 3–8 stories") puts the human at the AI's granularity. If the feature is the human's unit (per research), Step 2 could become "Select 1–3 features to advance; the workflow will propose stories that advance them." Does that match how the owner actually wants to plan?

3. **Where should the North Star / value floor live?** Architecturally, options: (a) in the feature/epic grooming artifact (extend epic-grooming skill); (b) in the PRD per feature; (c) in a dedicated `value-floor.json` per feature; (d) inline in story files. Each has consequences for who writes it and when.

4. **What is the right response to a pre-floor sprint that doesn't cross the floor?** The research says "do not punt." Concretely: does that mean (a) the sprint is not marked complete until the skeleton is live, (b) the retro flags it and rolls unfinished floor-closing work into the next sprint's top priority, or (c) the feature is explicitly re-scoped / paused? The workflow today has no distinct handling for this case.

5. **Is the 3-story minimum actually helpful?** Is there evidence that the 3-minimum produces better outcomes than allowing a 1- or 2-story sprint? The research argues explicitly for the single-walking-skeleton-story sprint. Is the minimum a historical artifact worth reconsidering?

6. **Should Step 3 (flesh out stories) happen *during* sprint planning at all?** The research says AI-native planning should be fast. Fleshing out a backlog stub into a full story with ACs is substantial work — it is real story-creation, not planning. An alternative: only select stories that are already fleshed out (`story_file: true`); send stubs back to `refine` or `create-story` before they become sprint-eligible. Then sprint planning becomes a pure selection/commit step, much lighter.

7. **What does success look like at retro for a sprint goal?** If sprint goals are introduced, the retro skill needs to be able to evaluate them. Does that mean a goal must be phrased in a way that can be evaluated from shipped artifacts alone (no "did we feel good about it"), or is a narrative goal acceptable?

8. **Appetite vs. story count: does the owner actually want time-boxed sprints?** The research argues for it. But the owner runs event-driven work (sprint closes when stories close; sprints vary in duration). Is a declared appetite ("this sprint is 5 days") useful, or does it add ceremony without yield in a solo context?

9. **How does the `feature-status` skill relate to `feature-grooming` and `epic-grooming`?** Three feature-aware skills exist; none are invoked from sprint planning. Is there an intentional layering the analyst is missing, or is this integration debt?

10. **Is the spec-impact agent pair (Step 4.5) doing work that belongs in `refine` or `create-story`?** If stories are refined to include their spec-impact implications before sprint planning, Step 4.5 collapses. Currently, impact is discovered *during* planning, which means planning is also serving as a late-stage refinement pass.

11. **Does the AVFL validation at Step 6 ask any feature/value-level questions?** Reading the workflow, AVFL validates "sprint plan coherence" using story ACs, Gherkin specs, team composition, and wave assignments. It does not appear to check "does this sprint plan move any feature toward its value floor." If AVFL is going to be the planning gate, is value-floor alignment a lens it should include?
