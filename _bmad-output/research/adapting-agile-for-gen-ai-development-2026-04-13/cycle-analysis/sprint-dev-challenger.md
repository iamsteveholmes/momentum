# Sprint Dev Phase — Challenger Findings

## Executive Summary

Sprint Dev is the most elaborated phase in Momentum — and that is exactly where the research cuts deepest. The phase has built a ceremonially rich multi-stage quality pipeline (worktrees, AVFL, per-story code review, consolidated fix queue, team review with QA + E2E + Architect Guard, verification checklist, sprint completion) that reads, from the outside, as thorough defense in depth. Read against the synthesis, it looks like a **correlated-agent echo chamber with a behavioral-validation-shaped hole in the middle**.

The core structural problems:

1. **AVFL is not independent validation.** The implementer and the validators share model family, share training distribution, share the same story-as-ground-truth, and often share the raw context of the change. The synthesis (CAISI, arxiv 2603.25773) is explicit that AI-review-of-AI-work "checks code against itself, not against intent." AVFL's dual-reviewer enumerator/adversary architecture reduces variance within a single failure mode; it does not produce the independence the research demands. Sprint Dev treats AVFL CLEAN as a quality signal. It is a coherence signal at best.

2. **The DoD checklist is almost entirely structural.** Read `references/dod-checklist.md`: it verifies tests run, frontmatter is present, line counts, JSON validity, file format compliance, "AVFL result noted." There is not one item that asks whether a user can do something they could not do before, whether the feature is observably closer to its value floor, or whether the change delivers the intent described in the story. The DoD can be 100% green on a story whose implementation misses the point entirely.

3. **The running app is absent from the entire pipeline.** The E2E Validator role exists in team review and quick-fix Phase 4, and the workflow speaks of "black-box verification." But neither `dev` nor `sprint-dev` requires the application to be built and running. The diff and the AC are the only ground truths consulted. Phase 6's "verification checklist" asks the developer to confirm behaviors manually — there is no enforcement that the system can actually exercise those behaviors.

4. **The owner's review moment is recognition mode by construction.** Phase 4 AVFL presents findings for acknowledgement. Phase 4c presents a fix/defer list. Phase 5 presents a findings summary. Phase 6 presents a Given/When/Then checklist. At every single review gate the owner is handed pre-digested AI output to react to — the exact "recognition mode" failure the Vibe-Check Protocol paper warns about. There is no point in the workflow where the owner is forced into generative mode against the running artifact.

5. **Literalness amplification is unchecked.** The story file — an AI execution artifact, inherited from `create-story` which is itself AI-generated — is the source of truth for AC. The synthesis says AI implements specs literally and fills gaps plausibly-but-wrong. Sprint Dev's only cross-check on the story's gaps is AVFL, whose `source_material` is the AC from the same story file. The feedback loop is closed before it ever touches the world.

6. **Velocity-adjacent metrics are what the pipeline outputs.** The sprint completion summary reports stories done, AVFL findings count, code review findings count, fix queue stats, team findings. There is no "are we closer to user value than we were a week ago" signal anywhere in the artifact.

If the owner takes the research at face value, **Sprint Dev is not a quality pipeline; it is a consistency pipeline.** It guarantees that what the AI produced is internally coherent with what the AI specified. It does not guarantee value, and it actively masks the absence of value with the appearance of rigor.

---

## Assumed Truths That The Research Questions

### "AVFL is a quality gate."

The SKILL.md is explicit: "Dual reviewers with different framings improve accuracy ~8 percentage points absolute over single-agent validation (Meta-Judge 2025). Staged validation is 8%+ more accurate and 1.5–5× more compute-efficient than outcome-only evaluation."

Read that carefully. It says dual-reviewer is better than single-agent. It says staged is better than outcome-only. It does **not** say dual-reviewer is independent of the implementer. It does **not** say staged validation catches failures that the implementer's context contains.

The research cited by the synthesis (CAISI, arxiv 2603.25773, CodeRabbit, Vibe-Check Protocol) establishes a categorical finding: agents reviewing agent output produce correlated failures. The 8-point improvement from Meta-Judge is a within-family improvement. It reduces noise in AVFL's own output; it does not bridge the gap to ground-truth user behavior.

**What the research actually implies about AVFL:** it is a sophisticated drafting step. It catches some classes of error (structural gaps, hallucinated references, internal inconsistencies, spec/artifact contradictions). It is not a substitute for the thing it is named to do — adversarial validation. The name creates false security.

### "The DoD defines story completion."

The research's formulation is sharper: "done means live in production with observed user benefit" (synthesis Problem 3). Sprint Dev's DoD means "file list matches, tests pass, frontmatter parses, AVFL was run." These are different definitions of done. The practice calls both "done" and the ambiguity is not incidental — it is structural cover for the value-floor problem.

A story can pass every DoD item and:
- implement the wrong thing correctly
- implement the right thing in a way the app does not actually expose to users
- implement a thing that works in isolation but breaks an integration seam (the Speedscale/Testkube finding)
- implement the right thing but fail to build, run, or boot (nothing in the DoD requires the app to run)

The DoD gives completion a shape that feels objective. It is not measuring what the research says matters.

### "Orchestrator purity ensures separation."

Orchestrator purity is valuable — the synthesis supports role separation (Codecentric isolation, Anthropic transcript/outcome, CAISI cheating findings). But the current orchestrator-purity rule addresses **write authority**, not **information access**. The orchestrator doesn't write files directly; it spawns subagents that do. This is not the isolation the research demands.

The research demands technical isolation: the implementer **cannot read** the test files; the tester **cannot read** the source. `.claudeignore`, symmetric `settings.json` permissions, process-level enforcement. Momentum's orchestrator purity is a coordination pattern, not an epistemic firewall. The dev agent has full read access to the story, the AC, the Gherkin spec (explicitly barred by one critical rule, but enforced only by prose, not permissions), the architecture docs, the rules files. The agent chain that produces the code shares context with the agent chain that reviews it.

### "Black-box verification is happening."

The workflow's critical rule says: "Dev agents never access sprints/{sprint-slug}/specs/ — verification is black-box." This is prose enforcement. It says the dev agent must not read the Gherkin. It does not say the dev agent cannot. It is not a `.claudeignore` rule, not a permission, not enforced by the harness.

More importantly: the black-box separation is between dev and spec. The E2E Validator, when it runs in team review, does receive the Gherkin. But:
- The E2E Validator is a Claude agent receiving text. Its "observation" of running behavior depends on tools the workflow does not mandate (no Playwright MCP, no running-app requirement in sprint-dev's workflow).
- The workflow text in team review says the validator "validates running behavior against Gherkin scenarios" — passively. There is no action step that says `npm start && wait for ready && invoke validator with app URL`.
- The developer is then asked to confirm scenarios (Phase 6). This is the developer's eyes, not the validator's executed behavior.

**The research's isolated specification testing pattern is structurally absent.** What exists is a Gherkin spec + a reviewer agent + a checklist for the developer. This is BDD documentation practice, not behavioral validation.

### "More reviewers = more coverage."

Sprint Dev's defense has roughly this structure:
- AVFL: up to 8 agents × 4 iterations = up to 32 agent runs
- Per-story code reviewer: 1 per merged story
- Team review: QA + E2E Validator + Architect Guard
- Fix agents: 1 per confirmed finding, sequential
- Re-review on fixes

The research pattern is the opposite: two agents with enforced technical separation and a running app as ground truth. Quality comes from *non-correlation*, not from *volume*. Twenty correlated reviewers can all agree on the wrong answer. The pipeline's cost scaling is in the direction of more correlation (more agents in the same family, more artifact-based review, more findings consolidation), not more independence.

---

## The Value Floor Risk

Synthesis Problem 4 — the owner's own framing — is the single most damning lens on Sprint Dev.

Sprint Dev takes a pre-written sprint record, executes the stories, runs quality gates, and emits a completion summary. Nowhere in the 7-phase pipeline does any step ask:

- Is the core capability of this feature now reachable that wasn't before?
- Did this sprint move us from pre-floor to post-floor, or elaborate on something not yet reaching floor?
- Is there an observable user behavior — one a stranger could see — that confirms value delivery?

The sprint completion output template:

```
**Stories done:** {{done_count}} / {{total_count}}
**Merge order:** {{merge_sequence}}
**AVFL:** {{avfl_findings_count}} findings
**Per-Story Code Review:** {{code_review_findings_count}} findings
**Fix Queue:** {{fix_items_count}} fixed, {{defer_items_count}} deferred
**Team Review:** {{team_findings_count}} findings, {{team_resolved}} resolved
**Verification:** {{confirmed_scenarios}} / {{total_scenarios}} scenarios confirmed
**Follow-up items:** {{followup_count}} stories added to backlog
```

Every metric in this summary can be green while the feature's value floor is uncrossed. A developer running this workflow for 5–10 sprints, as the owner describes, could watch every sprint close "successful" and still be below the value floor — with nothing in the pipeline signalling that fact. The verification checklist in Phase 6 asks for scenario confirmation, but Gherkin scenarios for a pre-floor feature will themselves be pre-floor scenarios. Confirming them does not cross the threshold.

**The punting failure mode the owner described is not merely unaddressed by Sprint Dev — it is actively enabled.** The pipeline generates confident completion signals for work that may not reduce the gap to the destination. The volume of green checkmarks creates the illusion of progress. This is the failure mode in its purest institutional form.

### What's missing at the sprint boundary

The research prescribes:
- North Star capability statement per feature (pre-sprint artifact).
- Walking skeleton discipline: Sprint 1 on any new feature targets end-to-end capability, however ugly.
- Gap check at sprint close: are we closer to the North Star than before?
- Pre-floor / post-floor state tracking in the sprint log.

Sprint Dev has none of these. There is no feature-level North Star concept. There is no walking-skeleton discipline in sprint planning (out of scope for this analysis, but the absence cascades here). There is no gap check between "all stories done" and "sprint complete." Phase 7 runs `momentum-tools sprint complete` without asking a single question about whether the sprint delivered value.

---

## Overbuilt vs. Underbuilt

### Overbuilt

**1. The multi-stage AVFL + code review + team review pipeline.**
Three separate review passes with overlapping scope (AVFL has a domain lens that overlaps with code review; code review overlaps with QA; QA overlaps with E2E validator on AC adherence; architect guard overlaps with AVFL's structural lens). The research says quality comes from non-correlation. Three more correlated passes is not three times the coverage; it is three times the ceremony producing three findings lists that must be consolidated, triaged, fixed, and re-reviewed. The `Phase 4 → 4b → 4c → 4d → 5 → re-review` structure is the most elaborate part of Sprint Dev and it validates nothing the research recognizes as validation.

**2. The consolidation/deduplication machinery.**
The `spawn_registry`, `pending_worktree_cleanup`, selective re-review routing, source tagging by reviewer, fix/defer list reconciliation. This is sophisticated state management for a problem the research says shouldn't exist in this shape: if you had one independent behavioral check running against a running app, you wouldn't need to consolidate findings from 5+ correlated reviewers.

**3. Per-role specialist dev agents (dev-skills / dev-build / dev-frontend / dev).**
The synthesis is explicit: "Do not chase a 'perfect spec' — build the harness that makes the spec iteratively correctable" (Fowler context engineering). Specialist agents per change type is the opposite pattern — it pre-specifies role boundaries before the harness has revealed which boundaries matter. None of the research supports this specialization model. Kurilyak, Agentsway, Playwright's three-agent architecture all separate by *function* (planner / implementer / tester), not by *file type touched*. The specialist routing adds configuration surface without research backing.

**4. The 7-phase task tracking structure.**
The workflow itself has a Phase 0 whose only purpose is to create tasks for the other phases. This is TaskWrite-as-ritual. The research on context engineering and harness design suggests the harness should encode what matters; the task list here encodes the workflow's own existence.

### Underbuilt

**1. Application running.**
Nowhere does the workflow require the application to build or run. Not before the dev agent starts. Not after merge. Not at AVFL. Not at code review. Not at team review. Not at verification. The `E2E Validator` role names running behavior but the workflow does not enforce it. This is the single most important gap. The synthesis names Codecentric's isolated-agent pattern as "the single highest-leverage addition." Sprint Dev has zero of it.

**2. Red-phase discipline.**
The synthesis: "Before the dev agent implements, require: the tester agent produces failing scenarios against the un-built feature. If all scenarios pass before implementation, the specs are wrong." Sprint Dev runs dev first, verification last. The red phase never exists. Beck's finding — that AI deletes tests to make them pass — is structurally possible here because the tests (Gherkin scenarios) exist before implementation but are never executed against a pre-implementation build.

**3. Technical isolation between implementer and verifier.**
Prose rules ("dev agent never reads specs/") are not isolation. There is no `.claudeignore`. There is no permission config. There is no harness enforcement. The research is unambiguous that isolation is the mechanism, not the intent.

**4. Outcome vs. transcript separation at the environment level.**
Anthropic's principle: separate what the agent said it did from what actually happened in the environment's state. Sprint Dev's DoD consults the story's Dev Agent Record — agent narration. It does not consult the filesystem, the running app's state, a database, logs, or any environmental artifact as independent confirmation. The story is the ground truth for whether the story is done.

**5. Behavioral regression eval set.**
The synthesis recommends a 20–50 task curated eval set drawn from past Momentum failures, run before closing a sprint. This doesn't exist. Retros surface findings; those findings are not codified as runnable checks that gate the next sprint.

**6. Value-validation gate at sprint close.**
No step in Phase 7 asks: "Is there a user behavior observable in the running app, in telemetry, in your own use, that confirms this sprint's features delivered value?" Without this, the owner's punting failure mode has no circuit breaker.

**7. The Judgment Frame.**
Synthesis Problem 2's central recommendation: a 5–10 line human-readable block per story (Intent / Done-state-for-a-stranger / Anti-goals / Review focus). Sprint Dev receives stories from `create-story`; the dev agent consumes AC technically; the human reviewer gets a findings list at the end. The Judgment Frame is the artifact that would force generative-mode review. Its absence means every owner review gate is recognition-mode by default.

### Appropriately built

- **Worktree isolation per story.** This is correct. It prevents cross-story contamination, enables parallel execution, supports recovery. The research supports role/session separation.
- **Autonomous merges, approved pushes.** The authority gradient is right — local commits are recoverable; pushes are not. This is defensible discipline.
- **Dependency-driven spawning.** Parallelizing unblocked stories matches Kurilyak's math on small verifiable units. This is the right shape.
- **Sprint record as single source of truth read by execution.** Planning-vs-execution separation is Kurilyak's dual-horizon model. Right primitive.

---

## Structural Misalignments

### 1. The review point is after the point of maximum damage.

Synthesis: "Move the review forward, not back. The review you want is *before the spec goes to the AI* (the Judgment Frame, the anti-goals, the review focus). This is the highest-leverage change."

Sprint Dev does the opposite. Every owner checkpoint is post-implementation:
- Phase 4: review AVFL findings (post-merge)
- Phase 4c: fix/defer decisions (post-findings)
- Phase 5: review team findings (post-team-review)
- Phase 6: scenario confirmation (post-everything)

The owner has zero review moments before implementation begins. By the time findings exist, the owner is pattern-matching on a pre-processed list — recognition mode, by the workflow's own design.

### 2. The validators share context with the implementer by default.

The dev agent reads: story file (AC, Dev Notes, Momentum Implementation Guide), architecture docs, rules files, specialist guidelines.

AVFL validators read: the diff, the AC (same source), the artifact.

Code reviewer reads: the touched files (same artifact), the story file (same source).

QA reads: story AC sections (same source), sprint stories.

Architect guard reads: architecture doc (possibly read by dev), touched files.

The only role with genuinely different context is E2E Validator — receives Gherkin, not AC — but it is a text agent, not an isolated-process agent with a running-app handle. The "different framing" is descriptive, not epistemic.

Correlated context produces correlated errors. This is the research's central warning and Sprint Dev's default state.

### 3. AC is the source of truth for both production and verification.

This is the circularity problem at its most concrete. `avfl-invocation.md` says the source_material for AVFL is the story's AC. The dev agent implements to the same AC. AVFL's Factual Accuracy lens asks "does the output match the source?" When the source is the spec and the output implements the spec, the lens is tautological by construction.

The research's resolution: the source of truth for verification is the running app's observable behavior, mediated by an isolated tester. The AC is the dev's input; the app is the verifier's input. Sprint Dev collapses these.

### 4. AVFL's findings consume developer attention that should be spent on the Judgment Frame.

Phase 4 through Phase 4d is, in wall-clock terms, the heaviest developer-interaction portion of the sprint (developer must review AVFL, acknowledge, review code review, make fix/defer decisions on potentially dozens of findings). This is the owner's scarcest resource spent on the pipeline's least independent signal. The Osmani/Vibe-Check research is explicit: this is where recognition mode collapses review quality. The workflow spends the owner's attention precisely where it has the least marginal value.

### 5. Quick-fix has some behavioral seams sprint-dev lacks — and still falls short.

`quick-fix/workflow.md` has:
- Two developer blocking gates in Phase 1 and Phase 2 (before implementation) — this is the research's "move the review forward" partial win.
- A collaborative fix loop with validators and a resident fixer (Phase 4) — closer to Codecentric pattern in spirit.
- AVFL checkpoint **on the plan** (Phase 2f) — validating the plan before implementation.

Sprint Dev has none of these. Quick-fix is doing better work on a smaller scope. This is backwards from a risk-weighting perspective: the sprint is higher stakes and has fewer pre-implementation review gates.

Even quick-fix still lacks the running-app gate, the Judgment Frame, and technical isolation. But its plan-first AVFL and blocking developer gates before implementation are patterns sprint-dev should inherit.

### 6. Autonomy asymmetry between merge and value judgment.

The workflow declares: "Worktree-to-sprint merges are autonomous — only pushes require developer confirmation." The owner's stated feedback is that this is correct.

But consider what the autonomous merge implies: the workflow trusts the dev agent's output sufficient to merge to the sprint branch without developer review. It then produces a findings pipeline post-merge that presupposes the merge was wrong (AVFL, code review, team review all exist to find defects in the merged state). The workflow is simultaneously confident enough to merge autonomously and suspicious enough to triple-review the merge.

This is not inherently incoherent — a staged pipeline with trust-and-verify can be rational. But the verification must be *independent*. When the verification is correlated (as argued above), the autonomous merge + correlated review pattern produces a structural false positive: the system keeps telling itself the work is good because the implementer and the reviewer agree, and the owner's only input is ratification of their agreement.

---

## The Feature Layer Question

The research's strongest meta-claim about granularity (Problem 2): *the story is the AI's unit; the feature or shaped pitch is the human's unit.*

Sprint Dev operates exclusively at story granularity. Every phase iterates over stories: spawn per story, merge per story, code review per story, fix per story, re-review per story. The only feature-level artifact is the epic assignment in the sprint record, used for prioritization at spawn time.

The sprint closes with a story-count summary. The summary does not roll stories up to features. It does not report "Feature X is now usable end-to-end" or "Feature Y's value floor is now crossed." A sprint can complete all stories for two different features, fully resolving one and fractionally progressing the other, and the completion report treats both the same way.

**This is the missing artifact the owner has named.** The human review gate that should exist at sprint close is a feature-level judgment question, not a story-level findings list. The research supports this from multiple angles:

- Kurilyak's dual-horizon: human reviews at feature/sprint scale; AI executes at story scale.
- Torres / Forbes outcome-based roadmaps: value judged at outcome, not at output.
- JTBD: job done is the unit, not task completed.
- Shape Up: shaped pitch (coarser than story) is the human artifact.

Sprint Dev's structure encourages story-level reasoning for the owner because that's the granularity the pipeline surfaces. The feature-level question — *did we cross the floor? did we move closer? is this feature usable?* — has nowhere to land. It is not in the DoD (too coarse for a per-story check). It is not in sprint completion (Phase 7 does not have a feature-level gate). It is not in any cross-cutting artifact.

The practical consequence: the owner gets excellent information about whether story 1-3-2's frontmatter is valid and no information about whether the sprint delivered a thing a user can see.

**If you were to remove exactly one thing from Sprint Dev and add exactly one thing, based on the research:** remove the AVFL Phase 4 + 4b + 4c + 4d apparatus (it is doing consistency work, not validation work, at high developer-attention cost) and add a feature-level value-floor gate at sprint close with a running-app demonstration requirement. The first recovers owner attention; the second spends it where the research says it matters.

---

## Hard Questions for the Owner

1. **What specifically has AVFL caught in Sprint Dev that a code linter, type checker, and "does the app build and boot" check would have missed?** If the answer is mostly cross-file coherence issues and AC-implementation mismatches, those are drafting-stage issues, not validation. If the answer includes class-of-failure categories the research identifies (integration seams, infrastructure failures, user-facing behavior divergence), AVFL would be earning its keep. Audit the last 3 sprints' AVFL findings against that split. What shape is the distribution?

2. **Has the Momentum app it was used to build crossed its own value floor?** Or, asked sharpest: over the last N sprints, has any sprint close produced a thing an outside user could pick up and get value from that they couldn't before? If yes, which sprint and what was the mechanism? If no, Sprint Dev is currently optimizing for a thing that is not the thing.

3. **Where does the dev agent verify its work against the running application?** If the answer is "nowhere — it runs tests and trusts the AC," the entire pipeline downstream is reviewing text. The research says this cannot catch the failure modes that matter. Is this gap acknowledged?

4. **When the owner reviews AVFL findings at Phase 4, is the review in recognition mode or generative mode?** Specifically: does the owner reason from first principles about whether each finding is correct and important, or does the owner agree/disagree with AVFL's assessment as presented? The Vibe-Check Protocol says the brain takes the easy path. Be honest about which path you take at that gate.

5. **What is the failure cost of accepting an AVFL CLEAN signal on a story that is spec-correct and value-zero?** If the answer is "we catch it in a later sprint," the system is working. If the answer is "we've been punting for 5–10 sprints on the same feature" (the owner's stated failure mode), the AVFL CLEAN signal is actively harmful — it provides false confirmation that the sprint delivered what it was supposed to.

6. **The workflow critical rule says the dev agent must not read Gherkin specs. What enforces that rule?** Not "should." Not "per the workflow." What file system, permission, or harness configuration would prevent a dev agent from reading `sprints/{slug}/specs/` if it chose to? If the answer is "the prose rule," the CAISI research says to expect circumvention. Is there a test that confirms the isolation holds?

7. **What would Sprint Dev stop doing if the owner built the Codecentric isolated-agent behavioral harness?** If the answer is "nothing, they'd be additive," then the current pipeline's overhead is being justified on "why not both." If the answer is "we'd drop AVFL's accuracy lens and the E2E validator role and trust the behavioral harness," that's a defensible simplification and worth acknowledging as the correct path.

8. **Does the sprint completion message's Follow-up items count ever decrease sprint over sprint?** If deferred items accumulate (they become backlog follow-up stories that themselves get deferred), the pipeline is producing debt faster than it resolves it. That is the literal signature of pre-floor punting.

9. **If the owner were handed a Sprint Dev output with all 7 phases green and was asked "is this feature deliverable to a user right now" — what would the answer depend on?** The synthesis says a correct pipeline should make this answer obvious and positive. What currently makes it uncertain?

10. **The specialist dev variants (dev-skills / dev-build / dev-frontend) represent a structural commitment that role boundaries follow file-type boundaries.** The research's role boundaries follow function boundaries (plan / implement / test / fix). Why was file-type chosen? What would break if the specialist system were collapsed to a single dev + isolated tester pair, as Codecentric recommends?

11. **What's the sprint-dev equivalent of the quick-fix Phase 1/Phase 2 blocking gates?** Quick-fix forces developer approval of the story and the Gherkin spec before implementation begins. Sprint-dev starts implementation as soon as the sprint record is unlocked, with no pre-implementation developer review gate. If the research is right that review-before-implementation is the highest-leverage change, sprint-dev is missing the thing quick-fix got right.

12. **The Phase 6 verification checklist asks the developer to tick off Gherkin scenarios. In practice, does the developer actually run the application and exercise each scenario, or does the developer read the Gherkin and affirm plausibility?** If the latter, Phase 6 is the Vibe-Check Protocol's recognition-mode failure mode in its purest form — it has the shape of verification without the substance. The workflow should either enforce execution (screenshot evidence, tool output, something) or stop calling this verification.
