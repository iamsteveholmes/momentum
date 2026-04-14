---
role: Challenger
phase: Sprint Planning
cycle: Momentum (Triage → Refinement → **Sprint Planning** → Sprint Dev → Retro)
research_anchor: _bmad-output/research/adapting-agile-for-gen-ai-development-2026-04-13/synthesis/synthesis.md
artifacts_evaluated:
  - skills/momentum/skills/sprint-planning/workflow.md
  - skills/momentum/skills/sprint-manager/workflow.md
  - skills/momentum/skills/sprint-manager/references/state-machine.md
  - skills/momentum/skills/feature-status/workflow.md
  - skills/momentum/references/practice-overview.md
  - skills/momentum/references/sprint-tracking-schema.md
date: 2026-04-13
---

# Sprint Planning Phase — Challenger Findings

## Executive Summary

Momentum's `sprint-planning` workflow is **a nine-step Agile planning ceremony running inside a solo AI-first practice**. It reproduces — almost one-for-one — the artifacts of a team-scale sprint planning meeting: a capacity-shaped backlog view, developer selection (with a 3–8 story range enforced as a business rule), per-story elaboration, spec generation, team composition with role guardrails, a dependency wave graph, an adversarial validation gate, a developer review loop, and an activation handoff.

The research the practice commissioned argues that most of this ceremony is **solving a problem that has moved**. Fowler, Beck, Siderova, Lindsay, Kurilyak, and Thoughtworks converge on one point: the bottleneck is no longer coding throughput — it is human judgment about *what to build, what counts as correct, and what constitutes value*. The sprint-planning workflow as written still concentrates its ceremony on coordinating the AI's work for the sprint, not on bounding a hypothesis and checking the value floor.

Four structural problems stand out:

1. **No value-floor check.** There is no "North Star capability" statement, no walking skeleton discipline, and no "here-to-there gap" analysis before stories are locked. Step 1 ("synthesize recommendations") reads the PRD and the previous sprint summary — but nothing in the workflow forces the question *are we still pointed at the minimum capability a user can feel?*
2. **Pre-sprint commitment contradicts the "last responsible moment" principle.** The workflow writes Gherkin specs, does spec impact analysis, assigns specialists, computes waves, and runs AVFL on the complete plan — **all before any code runs**. For AI-native work where gaps become visible only when the system runs, this front-loads cost at exactly the moment knowledge is lowest.
3. **Planning produces artifacts the AI doesn't need and humans can't review.** The synthesis says stories are AI execution artifacts and human judgment belongs at a coarser grain (feature / pitch / outcome). The workflow produces nine artifact types at story grain and zero at the grain the research says humans actually operate at.
4. **The sprint commitment is uncoupled from feature completion.** Stories commit in sprints; features span sprints; there is no sprint-planning step that asks "is sprint 2 of feature X building on a working skeleton from sprint 1, or on specs that never hit the running system?"

The planning phase looks rigorous, but the rigor is aimed at the wrong failure modes. It hardens selection, specification, and team composition — none of which is the documented failure mode in AI-native work. The documented failure mode is value-floor drift and spec-correct-value-zero punting, and the workflow has nothing that catches either.

---

## Assumed Truths That The Research Questions

The workflow encodes a set of assumptions that read as self-evident inside Agile but are precisely what the research corpus disputes.

### Assumption 1: "Sprint planning is a ceremony that produces a locked plan."

Workflow evidence: step 2 generates a sprint slug and creates a sprint branch; step 8 sets `locked: true` in `sprints/index.json`; state-machine.md forbids modifying a locked sprint. The artifact of planning is a committed-to list.

Research counter: Siderova, Lindsay, and Futurice converge on the sprint as a **governance and learning cadence**, not a capacity container. Shape Up explicitly rejects backlog grooming as a planning input. OpenAI, AWS AI-DLC, and Brgr.one describe continuous flow with PR-centric coordination — no sprint ceremony at all. The research does not say "keep the sprint planning ceremony but do it better." It says *"the purpose of the sprint is to bound time on a hypothesis"* — and bounding a hypothesis does not require a 9-step planning ritual.

### Assumption 2: "3–8 stories per sprint is a meaningful selection range."

Workflow evidence: step 2 validates `selection count must be between 3 and 8 (inclusive)` and loops back on violation.

Research counter: the entire corpus treats story count as the wrong primitive. Kurilyak's math argues for **small verifiable units sized by agent reliability**, not story count. Shape Up uses **appetite** (ordinal time commitment), not count. DORA 2025 emphasizes flow metrics (cycle time, lead time) — not sprint capacity. The 3–8 rule is a cargo-culted team sizing from two-week Scrum planning; in solo AI-first work it has no theoretical basis. Why not 1 story? Why not 12 tiny ones? The workflow can't answer from its own principles.

### Assumption 3: "Gherkin specs must be generated at planning time."

Workflow evidence: step 4 writes `.feature` files to `sprints/{slug}/specs/` for every selected story, with a full validation pass for format, naming, and "Outsider Test" compliance. This is substantial work — probably the most expensive single step in planning.

Research counter: Fowler/Böckeler warn that **SDD over-specifies small tasks**. Kiro's documented failure mode is generating "4 user stories with 16 acceptance criteria for a single bug fix." The "curse of instructions" — model performance degrading past a threshold of simultaneous requirements — is empirical. The workflow generates specs *ahead of implementation* at the exact moment knowledge is lowest, then re-runs AVFL over them, then asks the developer to approve, **then** dev agents implement against them. Every layer of pre-specification is a chance for the spec to diverge from reality once code runs.

Beck's red-phase TDD discipline (corpus, Section: Problem 3) is an alternative: write specs *against a running walking skeleton*, not against an imagined system. The workflow has no mechanism for this — specs are a planning artifact, not an execution artifact.

### Assumption 4: "AVFL on a sprint plan catches defects before they matter."

Workflow evidence: step 6 concatenates "all story ACs + team composition + wave assignments" and sends them to AVFL. GATE_FAILED halts planning.

Research counter: CAISI, arxiv 2603.25773, and the Codecentric pattern all argue that **AI-reviewing-AI on the same artifact produces correlated failures**. AVFL on a plan document (paper artifact, no running system) is exactly the failure mode the research flags: "checks code against itself, not against intent." Planning-time AVFL can catch internal contradictions in the plan — but not whether the plan, once executed, will cross the value floor. The costly step gates the cheap failure mode.

### Assumption 5: "Specialist domain assignment and guidelines verification are planning concerns."

Workflow evidence: step 5 runs a domain classification table (dev-skills / dev-build / dev-frontend / dev), a guidelines verification gate (`.claude/rules/*.md` file existence), and asks the developer per-domain whether to Generate / Proceed / Downgrade. Step 5.5 re-validates that required role agents exist.

Research counter: the harness-engineering framing (Fowler, Kief Morris' "on the loop") says rules and guidelines are **accretive harness**, added when a class of failure recurs — not pre-verified at planning time per sprint. The workflow treats missing guidelines as a planning blocker for the developer to resolve. The research says the right response is to *let the failure surface, then add the rule*. Pre-verifying guidelines for every sprint is the "perfect spec upfront" failure mode at the agent-configuration layer.

### Assumption 6: "Planning must produce a dependency wave graph."

Workflow evidence: step 5 computes Wave 1 / Wave 2 / ... from `depends_on` fields; step 2 flags dependency warnings if a story depends on something not in the sprint.

Research counter: OpenAI runs ~3.5 PRs/engineer/day with no sprint structure. Continuous flow uses **just-in-time dependency resolution at the PR level**. A pre-computed wave graph assumes the dependencies are correctly declared in the story stub, before implementation has revealed what's actually needed. The workflow has no step for "re-plan waves when implementation exposes a new dependency" — waves are a planning artifact, not a running artifact.

---

## The Value Floor Risk

This is the single most damaging gap in the sprint-planning workflow.

The research's Problem 4 (added from the owner's direct observation) describes a failure mode with a specific shape:

> You can deliver correct stories and still be below the value floor. After 5-10 sprints we're still NOT there. You keep punting to the next sprint and the next sprint, delivering versions with no value.

The fix the research names is explicit:

- A **North Star capability statement** per feature before work begins.
- **Walking skeleton first** — Sprint 1 on any new feature targets end-to-end capability, not elaboration.
- A **gap check at sprint close** asking *are we closer to the North Star than before?*
- **Pre-floor / post-floor sprint states** so retrospective questions match the state the sprint is operating in.

Now inspect the sprint-planning workflow. Where does the North Star show up?

**Step 1** ("Synthesize recommendations from master plan and backlog") reads `prd.md`, the product brief, and the previous sprint summary. It extracts "current priorities and recent edit history." It produces 3–5 top story recommendations with rationales tied to "master plan priorities and readiness." **It does not check for a North Star capability statement per active feature.** It does not ask "is the walking skeleton up yet?" It does not distinguish pre-floor from post-floor work.

**Step 4.5** ("Spec impact analysis — update architecture and PRD") updates PRD and architecture when stories introduce new requirements. This is downstream drift management — it keeps the specs honest about what was planned. It does not ask whether the plan moves toward or away from the value floor.

**Step 6** (AVFL on the complete plan) validates internal coherence. It does not ask "does this sprint deliver observable user value?"

**Step 7** (developer review) displays stories, team composition, dependency graph, AVFL result. **There is no "gap to North Star" display.** The developer cannot see from the plan whether sprint 3 of a feature is elaborating on a walking skeleton or inventing elaboration around a gap.

This is not a minor omission. The research explicitly calls this out as the fix that has no ceremony: *"No published framework in this corpus explicitly defines a 'value floor' concept or a 'pre-floor / post-floor' distinction. The owner's framing is new and deserves to be developed as a Momentum-specific practice."*

The sprint-planning workflow is the correct place for that ceremony. It currently isn't there.

### What this specifically costs

The workflow as written **can plan, validate, AVFL-clear, and activate a sprint that elaborates around a gap**. Every gate it runs is internal-coherence-checking. Not one is value-floor-checking. A sprint can be perfectly planned, fully team-composed, spec-complete, and still be the fourth consecutive sprint that fails to cross the floor.

The `feature-status` skill exists and does produce a gap indicator ("acceptance_condition requires X; assigned stories only cover Y"). But `sprint-planning` **does not invoke `feature-status` at any point**. The gap check is a separate HTML artifact the developer can open — not a gate in sprint planning. That's a designed-in disconnect between the signal and the decision.

---

## Overbuilt vs. Underbuilt

### Overbuilt

**Gherkin spec generation (step 4).** This is a large, high-ceremony step with a two-phase validation pass, an "Outsider Test" rubric, and a halting regeneration loop. For a solo practitioner, against research that says spec-completeness-non-monotonically-degrades-model-performance and that specs should follow the walking skeleton rather than precede it, this reads as expensive ritual for marginal defect catch. The research (Codecentric, Beck) puts the cost-effective behavioral validation at the **running system** boundary with isolated tester agents. Pre-generated Gherkin is planning-time ceremony aimed at runtime problems.

**Team composition with specialist domain tallying (step 5).** A pattern table with a majority-rule tally across touches paths, a file-existence check for project-specific guidelines per specialist domain, a three-choice prompt per missing domain (G/P/D), and a downstream reassignment pass. For stories where the AI is going to implement in minutes, the planning-time specialist selection is low-impact — specialists mostly differ in which rules files they consult, and those rules files are harness the agent reads at runtime anyway. The work to pick the right specialist at planning time is probably wasted vs. letting the `sprint-dev` runtime pick based on actually-touched paths.

**Wave graph computation (step 5).** Pre-computing execution waves from declared `depends_on` fields assumes those fields are correct at planning time. Implementation often reveals undeclared dependencies. Continuous-flow practice lets dependencies resolve at PR boundary. The wave graph is overfitting to a declaration that isn't reliably true.

**AVFL on the plan (step 6).** Running the adversarial loop over a paper artifact catches internal contradictions but not value-floor issues. The research says AI-review-of-AI produces correlated failures; AVFL on a plan is this pattern at planning scale. The cost (an entire subagent spawn on a concatenated plan) is high for what it catches.

**The 3–8 story selection rule (step 2).** No theoretical basis in the research. A cargo-culted team-scale rule.

### Underbuilt

**Value-floor ceremony. Missing entirely.** No North Star statement check, no walking-skeleton selection rule, no pre-floor/post-floor state, no here-to-there gap artifact. This is the most important missing step.

**Appetite declaration. Missing.** Shape Up's appetite (ordinal time commitment — "I'm willing to spend half a day on this") is the research-recommended sizing primitive for solo AI-first work. The workflow has no appetite input; it has a count constraint (3–8).

**Judgment Frame per story. Missing.** The research's central recommendation for the human-AI specification interface is a 5–10 line block (Intent / Done-state-for-a-stranger / Anti-goals / Review focus) that lives above the AC. The workflow generates ACs and Gherkin specs — both AI-facing artifacts. It produces nothing at the "glanceable-correctness" layer the owner specifically identified as missing.

**Feature-level Judgment Frame. Missing.** The research says the human-judgment grain is feature, not story. Sprint planning commits at story grain but never rolls up to feature grain for developer review. Step 7's review table lists stories by wave — not features by capability-delivered.

**"Walking skeleton in place" check. Missing.** The workflow does not ask, for any feature that has stories in the sprint, whether a minimal end-to-end version of the feature's core capability exists yet. Sprints 2..N on a feature proceed the same way as Sprint 1.

**Re-planning trigger at runtime. Missing.** The state machine forbids modifying a locked sprint. Sprint-dev runtime discoveries (a wave invalidated, a new dependency, a story that can't complete) do not route back to sprint-planning. The plan is immutable; only re-opening a sprint can change it.

**Pre-floor / post-floor sprint classification. Missing.** Retrospective asks the same questions regardless of whether the sprint crossed the value floor or elaborated on one already crossed. The research says these should be different questions.

---

## Structural Misalignments

### 1. The ceremony is calibrated to team-scale Agile, not solo AI-first practice

The workflow's phase count, artifact count, and gate count are team-scale. Nine steps with sub-steps, multiple approvals, role composition, specialist assignment, per-domain guideline verification, and AVFL: this is the shape of a planning meeting that needs to coordinate ten people's work for two weeks. For a solo developer whose AI can implement a story in minutes, the ratio of planning ceremony to execution cost is badly inverted.

DORA 2025: "AI as amplifier, not fixer." The amplifier-of-planning-ceremony is planning-ceremony. Inverting the planning-to-execution ratio is the research's most consistent refrain.

### 2. The ceremony front-loads decisions that should defer to running-system evidence

The "last responsible moment" principle says: defer decisions until you have maximum knowledge. At sprint planning, the running system doesn't yet exist for the work you're planning. Yet the workflow commits to: which stories (step 2), their full acceptance criteria (step 3), their behavioral Gherkin specs (step 4), architecture and PRD updates (step 4.5), specialist assignment per story (step 5), and a dependency wave order (step 5). These are all decisions that would be better made *against a running walking skeleton*.

Beck's red-phase TDD discipline says the right move is: build the walking skeleton first, watch the specs fail against it, *then* implement. The workflow's specs are written before the walking skeleton exists. This is the pattern Fowler calls out as replaying MDD's failure mode.

### 3. The sprint-planning skill writes files directly despite orchestrator-purity rules

The project's orchestrator-purity rule (from memory: `feedback_orchestrator_purity_quickfix`) states that orchestrator skills must not write files directly — only tools and subagent spawns. Sprint-planning writes:
- Gherkin `.feature` files (step 4 — "Write the spec to: `sprints/{slug}/specs/{slug}.feature`")
- Architecture and PRD updates (step 4.5 — via spawned subagents, which is compliant)
- Sprint-branch creation via git (step 2)

The spec writes are orchestrator-level file writes. They are compliant only because a different rule (the sprint-planning workflow itself) directs them. This is internally inconsistent: `quick-fix` cannot write files, but `sprint-planning` can. The research principle (role separation by construction) favors extracting spec generation to a subagent with write authority, leaving sprint-planning as pure orchestrator.

### 4. The workflow assumes stories are the primary planning unit, but the research says features are

The workflow takes stories as input (from backlog), selects stories, generates per-story artifacts, and outputs a story-wave plan. Features appear nowhere in sprint-planning's execution logic. Epics appear only as grouping in the backlog display.

The research: *"The story is the AI's unit. The feature — or the shaped pitch — is the human's unit."* Sprint planning is where the human most needs to operate at feature grain. The workflow keeps them at story grain throughout — then asks the developer to approve the assembled story list.

### 5. AVFL as a planning gate conflates two different validation surfaces

AVFL runs at:
- Sprint planning (step 6, on the paper plan)
- Sprint dev (post-merge, on running code)

These gate different failure modes. The planning AVFL can catch plan-internal-contradictions. It cannot catch runtime behavior. Running AVFL at planning creates the appearance of rigor without the substance. The research is explicit: *"Do not rely on AI-review-of-AI-work as a quality gate."* Planning AVFL is AI-review-of-AI on a paper artifact.

### 6. The sprint branch is created before planning is approved

Step 2 runs `git checkout -b sprint/{slug}` immediately after story selection, **before** specs, team composition, AVFL, or developer review. If the developer rejects the plan at step 7, the branch exists with nothing useful on it. This is a minor operational issue, but it reflects the broader pattern: the workflow commits to structure before the decisions that justify the structure have been made.

---

## The Feature Layer Question

The hardest question the research raises for sprint planning is not about sprint planning at all — it is about what sprint planning is planning.

The practice has three layers: epic → feature → story. The workflow operates at the story layer. Features are where users experience capability. Stories are where the AI executes. These are different grains; **the research says the planning layer should match the judgment layer, which is the feature**.

The workflow has no feature-aware planning logic. Consider a concrete scenario:

- Feature F has 7 stories in the backlog.
- Sprint N selects 3 of them; Sprint N+1 selects 2; Sprint N+2 selects the last 2.
- After Sprint N, the feature is 3/7 stories done. After Sprint N+1, 5/7. After Sprint N+2, 7/7.

**At no point in the sprint-planning workflow is the question asked: "after this sprint, what will a user be able to do with Feature F that they couldn't before?"**

This is the failure mode Problem 4 describes. Individual sprints close stories correctly. The feature's value floor may never cross. The developer may "keep punting to the next sprint and the next sprint, delivering versions with no value."

### The sprint-planning workflow cannot catch this because:

1. Stories are the input primitive. Features appear only implicitly via `epic_slug` and `feature` assignment in feature-status.
2. The synthesis step (step 1) reads the PRD and previous sprint summary but does not compute per-feature progress toward capability.
3. The AVFL gate (step 6) receives story ACs and team composition but not feature capability statements.
4. The developer review display (step 7) groups by wave, not by feature.

The `feature-status` skill *does* produce a gap analysis — but sprint-planning does not integrate it. `feature-status` is an HTML artifact the developer opens separately. There is no workflow step that says "read `features.json`, list all features touched by selected stories, show per-feature delta: before-sprint capability → after-sprint capability, flag features that are still below their North Star after this sprint."

**The feature layer exists in the data model. It does not exist in the planning ceremony.**

### What this means for sprint-2-of-a-feature

The research's walking skeleton principle says: sprint 1 of a feature targets end-to-end capability (however minimal); sprints 2..N accumulate incremental value. The workflow treats all sprints identically. A sprint planner has no signal about whether they are doing sprint 1 (skeleton discipline required) or sprint 2+ (elaboration is safe). The retrospective (a different phase) is where this would show up; by then, two sprints of wrong-mode work have already shipped.

This is a structural hole where a piece of ceremony was never built.

---

## Hard Questions for the Owner

These are the questions the research forces that the workflow does not currently address.

1. **Why do you need a planning ceremony at all?** OpenAI Codex runs 3.5 PRs/engineer/day with no sprint ceremonies. AWS AI-DLC talks about "Bolts" as units of work with no planning meeting. For a solo practitioner, what does sprint planning buy that a "pick the next unblocked story and start" loop does not? The research does not answer this question — you have to.

2. **What decision does sprint planning defer?** Per the "last responsible moment" principle, every commit made at planning time is a commit that might be wrong because the running system didn't exist yet. Name one decision that is *genuinely better made at planning time* than at the moment the AI picks up the story. The Gherkin spec? The specialist choice? The wave order? If the answer is "nothing critical is better made at planning time," the ceremony is theater.

3. **Where in sprint-planning do you assert you're still pointed at value?** Not "the story matches the PRD" — that is internal coherence. "A user will be able to do something after this sprint that they couldn't before." If this is not the top-level question the workflow asks, the workflow is not doing the job the research says sprint planning should do.

4. **What is the North Star capability for each active feature?** Walk through the last 3 sprints. For each feature that had stories in those sprints, state the North Star in one sentence. If you can't do it in one sentence without reading the PRD, the North Star does not exist. If it does not exist, the workflow cannot check it. If it is not checked, value-floor punting is the default.

5. **Is sprint 1 of a new feature structurally different from sprint 3 of an existing feature?** In the workflow, no — they go through identical steps. In the research, they are categorically different (pre-floor vs. post-floor). Which is true for your practice?

6. **Why do you still estimate by story count?** The 3–8 rule is the only scope primitive the workflow recognizes. Shape Up's appetite, DORA's cycle time, Kurilyak's agent-step count — all research-backed alternatives. The 3–8 rule is the Scrum-team-sized residue in an otherwise AI-native practice. What is it doing?

7. **What is the cost-to-catch ratio on AVFL at planning time?** AVFL on the plan costs a subagent spawn and a synthesis pass. What class of defects has it actually caught in the last 5 sprints? If the answer is "internal-contradiction defects only," the cost is aimed at the wrong failure mode — and the research warns this explicitly.

8. **Should Gherkin specs be generated at planning or at red-phase-of-TDD?** The workflow puts them in planning. Beck's discipline says they belong after the walking skeleton is up. Which is the right place in your practice — and what specifically breaks if you move them?

9. **Should sprint-planning invoke `feature-status`?** The gap analysis exists. The sprint-planning ceremony does not use it. If you had to defend the separation, what would the argument be? If you can't defend it, they should be joined.

10. **Is the planning sprint branch a premature commitment?** Step 2 creates the branch. Step 7 is where the plan is approved. What happens to the branch on rejection at step 7? What does the state of `sprints/index.json` `planning` entry look like across a failed approval loop? This is the smallest of the gaps identified, but it is symptomatic of a workflow that writes before it thinks.

11. **What would the workflow look like if you believed the research?** A one-week governance cadence. Appetite instead of count. A North Star gate at step 1. A walking-skeleton check for new features. Judgment Frames at story grain, feature-level frames above. Specs generated in red-phase during dev, not in planning. AVFL at running-system boundary, not paper-plan boundary. Re-planning allowed mid-sprint on material discovery. **Write the alternative workflow and compare.** The comparison is the argument — either the current ceremony survives the comparison or the alternative wins. The research gives you the material; the ceremony currently does not.

---

## Summary of Disputes

| Dispute | Workflow Says | Research Says |
|---|---|---|
| Purpose of sprint planning | Produce a locked, validated plan | Bound a hypothesis, govern and learn |
| Sizing primitive | 3–8 story count | Appetite (ordinal time) or flow metrics |
| Spec generation | Planning-time Gherkin | Red-phase against walking skeleton |
| Validation gate | AVFL on paper plan | Isolated agent vs. running system |
| Human judgment grain | Story (ACs, waves) | Feature (North Star, Judgment Frame) |
| Primary failure mode to catch | Plan incoherence | Value-floor punting |
| Re-plan triggers | None (plan is locked) | Discovery at runtime |
| Skeleton discipline | Not enforced | Sprint 1 of feature = skeleton |
| Pre-floor/post-floor distinction | None | Required for retrospective validity |
| Feature-layer integration | Data-only (epic_slug) | Planning should operate at feature grain |

The current workflow is internally consistent and careful. Its problem is not execution — it is aim. Nearly every step is well-designed for a question the research says is no longer the load-bearing question.
