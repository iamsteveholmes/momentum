# Retrospective Phase — Analyst Findings

**Role:** Analyst (mapping-only, no decisions). Sources: `skills/momentum/skills/retro/workflow.md`, `skills/momentum/skills/sprint-manager/`, `skills/momentum/skills/feature-status/`, `skills/momentum/references/practice-overview.md`, `skills/momentum/references/sprint-tracking-schema.md`, and the research synthesis at `_bmad-output/research/adapting-agile-for-gen-ai-development-2026-04-13/synthesis/synthesis.md`.

---

## Executive Summary

The Momentum retro is, by the literature's standard, one of the most advanced retrospective mechanisms surveyed — it already does three things the research treats as aspirational:

1. **Harness-failure focus over velocity.** The auditor team (human / execution / review) is organized around *where the loop broke*, not *how much got shipped*. No velocity metric is computed. This aligns cleanly with Siderova's "Agile optimizing a moved constraint" and Lindsay's "learning-cadence, not delivery-throttle" framing.
2. **AI at agent cadence for practice improvement.** The Phase 5 Tier 1 → `momentum:distill` routing auto-applies single-sentence rule deltas without human story overhead. This is a direct operationalization of Fowler's "harness engineering" / Morris' "on the loop" principle. The literature describes this pattern; Momentum implements it.
3. **Transcript/outcome separation.** The audit pulls four distinct extracts (user-messages, agent-summaries, errors, team-messages) and the auditors correlate across them. Anthropic's transcript-vs-outcome principle is partially honoured at the *session* level.

However, the retro has four material gaps against the research, all of which concern **the close-of-loop back to value, not the audit of the loop itself**:

- **No value-floor check.** Story verification asks "did stories reach `done`?" (Phase 3). It does not ask "is the core user capability closer than before?" — the question the research identifies as the single most important addition to AI-native sprint close.
- **No feature-level closure ritual.** The retro closes a sprint; it does not close a feature. `feature-status` is invoked once in Phase 6 as a data-source for the summary, not as a judgment artifact. The "did this feature deliver what I wanted?" question is structurally absent.
- **No persistent eval-set extraction.** Failures become *story stubs* (Tier 2) or *rule deltas* (Tier 1). Neither produces a reproducible behavioral regression test. The 20–50-task eval set the research explicitly recommends has no home in the current workflow.
- **Transcript-only ground truth.** The auditor team reads JSONL. Anthropic's principle says transcripts are necessary but not sufficient — what matters is environmental state, not agent narration. The retro never asks "is there a DB record / file / visual state that proves this happened?"

Three additional observations worth raising:

- Phase 5 has two routing paths (distill vs. stub). The research points at a **third** path that doesn't exist yet: **eval-set entry**. A failure that is neither a rule delta nor a new story is potentially a behavioral regression — and there's nowhere to put it.
- The retro's own sprint summary (Phase 6) produces "Stories Completed vs. Planned" as its primary metric. This is the velocity-adjacent framing the research warns against. Cycle time and lead time are the corpus-converged replacements.
- The distinction between **pre-floor** and **post-floor** sprints is the research's most actionable structural idea that Momentum has no concept of. Every sprint is treated as interchangeable.

---

## What Exists and How It Aligns

### Auditor team design (Phase 4) — aligned with research

Three auditor lenses map to three research-backed failure categories:

| Auditor | Reads | Research backing |
|---|---|---|
| auditor-human | user-messages.jsonl | Osmani's "corrections and redirections as signal"; Vibe-Check recognition-vs-generative-mode |
| auditor-execution | agent-summaries + errors | Kurilyak's reliability math (5% × 10 steps = 59.9% success) — find high-error chains |
| auditor-review | team-messages + reviewer agents | arxiv 2603.25773 on AI-review-of-AI correlation failure |

The `documenter` as exclusive writer of `retro-transcript-audit.md` with SendMessage collaboration is exactly the Agentsway "role boundary by construction" pattern the research highlights.

**Verdict:** This is a strength the research would endorse as-is.

### Tier 1 / Tier 2 routing (Phase 5) — partially aligned

The `signal_type` classifier + Tier 1 → `momentum:distill` path is the research's "harness improvement at agent cadence" pattern in action:

- Tier 1 (rule delta, reference entry, prompt clarification): immediate application — skips the human story queue.
- Tier 2 (multi-file, new skill, workflow redesign): generates a story stub for developer approval.

This is aligned with Fowler's context-engineering (accretive rules) and Morris' "humans on the loop."

**Gap:** The routing is binary. There is no third category for "this is a reproducible behavioral failure that should become a regression test." Every such failure currently collapses into either (a) a rule to prevent recurrence (Tier 1) or (b) a story to fix it (Tier 2). Neither path captures the failure as a persistent, runnable eval.

### Sprint summary production (Phase 6) — structurally partial

Phase 6 produces a sprint summary with five sections: Features Advanced / Stories Completed vs. Planned / Key Decisions / Unresolved Issues / Narrative. The `Features Advanced` section is conditional on `feature-status` running and is documented as the only delegation in Phase 6.

**What aligns:** Including Features Advanced at all is a step toward feature-level closure.

**What doesn't:** The section is *descriptive* ("which features advanced"), not *evaluative* ("did the features that advanced actually move closer to their acceptance condition?"). features.json has an `acceptance_condition` field per feature that reads exactly like the North Star capability statement the research recommends — but the retro doesn't compare observed state against it.

### Story verification (Phase 3) — aligned with narrow version of the question

Phase 3 asks "did every story reach `done`?" If not, the developer chooses Force-close or Investigate.

**What aligns:** Incomplete stories are surfaced explicitly, not silently carried. This addresses the "silent punt" anti-pattern the research calls out.

**What doesn't:** "Story `done`" is AC-correctness, not value-delivery. A force-close to `closed-incomplete` goes into the "Unresolved Issues" list but never into a structured gap-tracking artifact. The research's "don't punt gaps" principle is partially honoured (gaps are surfaced) but partially broken (there's no destination for the gap besides a backlog stub).

### Transcript preprocessing (Phase 2) — strong against Anthropic's principle, partial against the corpus

The DuckDB extraction of four JSONL views is the richest session-data pipeline described anywhere in the corpus. No other framework surveyed extracts team-messages as a distinct audit dimension.

**What aligns:** Using "actual error indicators (is_error flag, success=false)" rather than string matching is the kind of detail Anthropic's evals guidance treats as non-negotiable.

**What doesn't:** Sessions are transcripts — they record what agents said, not what happened in the environment. The research's transcript/outcome split is honoured only on the transcript side. There is no extract of "what changed on disk / in the DB / in the built app" during the sprint.

### Sprint closure (Phase 6 tail) — aligned with state-machine discipline

`momentum-tools sprint complete` + `sprint retro-complete` is a clean state machine transition. `retro_run_at` makes "has this sprint been retro'd?" queryable. This aligns with the research's "deliberate re-evaluation checkpoints" recommendation.

---

## Gaps: What the Research Says Should Exist

### Gap 1 — Value-floor / gap check at sprint close

**Research says (Problem 4):** At sprint close, ask for each active feature: "are we closer to the North Star capability than before this sprint?" Track pre-floor vs. post-floor state explicitly. Do not punt gaps.

**Retro currently:** No phase asks this. Phase 3 asks story-level completion; Phase 6 asks "which features advanced" (descriptive, not gap-oriented).

**Evidence of gap:** features.json carries `acceptance_condition` per feature. The retro never loads this field. The retro never computes "distance to acceptance_condition" before vs. after the sprint.

### Gap 2 — Feature-level closure and Judgment Frame

**Research says (Problem 2, rec 3):** The feature is the primary human-judgment unit. Per closed feature: what will a user experience that they could not before? Observable behavior change.

**Retro currently:** No per-feature closure step. Features are mentioned only in the Features Advanced section, which is conditional and descriptive.

**Evidence of gap:** features.json has a `status` field (`not-started`, `partial`, `working`, etc.) but no step in the retro transitions features between these states based on sprint outcome. Features drift between statuses via `feature-status` recalculation, not via retro judgment.

### Gap 3 — Eval-set construction from failures

**Research says (Problem 3, rec 3):** Build a 20–50 task behavioral regression eval set seeded from real Momentum failures. Run before closing a sprint.

**Retro currently:** Failures become rules (Tier 1) or stories (Tier 2). There is no `eval/` directory, no persistent "if we regress this, we'd want to know" artifact, no "run eval set before sprint closure" step.

**Evidence of gap:** Phase 5 explicitly classifies findings and routes them to distill or to a stub. No third route exists for "capture this as a reproducible behavioral test."

### Gap 4 — Transcript vs. outcome separation

**Research says (Problem 3, principle from Anthropic):** Validation evidence must include what happened in the environment, not what the agent narrated.

**Retro currently:** All four extraction sources are transcript-derived. There is no extraction of filesystem diffs, DB state changes, built-app behavior, or running-app verification.

**Evidence of gap:** The `agent-summaries.jsonl` extract reports `tool_results` counts but not *what the tools actually produced in the environment*. A story could be reported as complete by the agent and by the summary while the underlying artifact is missing or wrong — the retro would not detect this.

### Gap 5 — Pre-floor / post-floor state tracking

**Research says (Problem 4, rec 4):** Track pre-floor and post-floor explicitly. The retro question in each state is different.

**Retro currently:** No concept. Every sprint is treated identically.

**Evidence of gap:** sprints/index.json records `started`, `completed`, `retro_run_at`, and a `status` (planning/active/done). No field records whether the sprint was pre-floor infrastructure, a walking-skeleton attempt, or a post-floor elaboration. The retro asks the same questions regardless.

### Gap 6 — Flow metrics over completion metrics

**Research says (Problem 1, rec; Stop-list):** Cycle time per story, lead time from intake → production. Do not measure velocity (including stories-per-sprint).

**Retro currently:** Phase 6 sprint summary leads with "Stories Completed vs. Planned."

**Evidence of gap:** No cycle-time or lead-time computation anywhere in the retro. The one metric produced is the one the research says to stop producing.

### Gap 7 — Red-phase verification loop-back

**Research says (Problem 3, rec 2):** If the dev agent's first run of tester scenarios passes without implementation changes, something is being bypassed. This is a retro-worthy signal.

**Retro currently:** The auditor-review reads reviewer agents, but there is no specific detection for "tests passed suspiciously early" / "zero-diff green." This is a CAISI-cheating failure mode the retro is structurally positioned to catch but doesn't.

### Gap 8 — Judgment Frame outcomes review

**Research says (Problem 2, rec 2):** Each story has a Judgment Frame (Intent / Done-state-for-a-stranger / Anti-goals / Review focus). At sprint close, review whether the done-state-for-a-stranger condition is actually observable.

**Retro currently:** Momentum does not yet have Judgment Frames on stories, so the retro cannot review them. If they are added upstream, the retro will need a step to check them.

---

## Removal Candidates

Candidates are "things currently in the retro that the research suggests should not be there, or should be re-targeted." Analyst raises questions, does not decide.

### Candidate 1 — "Stories Completed vs. Planned" as a summary headline

**Research position:** Stop measuring velocity. Flow metrics (cycle time, lead time) are the corpus-converged alternatives.

**Question for deciders:** Should the sprint summary lead with a different metric — or should this section be kept for developer orientation but demoted below a flow-metric section?

### Candidate 2 — The 500-word cap on sprint summary

**Research position:** At AI-agent cadence, the retro's findings *are* the practice improvement — the cap may trim exactly the content that matters for "on-the-loop" harness updates.

**Question for deciders:** Is the 500-word cap a human-attention budget (keep) or a historical artifact from a time when the summary was a human-written narrative (remove)?

### Candidate 3 — The conditional on Features Advanced

**Research position:** The feature is the primary human-judgment unit. A feature-level closure check should be a required step, not a conditional "if feature-status succeeded."

**Question for deciders:** If `feature-status` fails, should the retro *halt* (features are the primary unit) or *continue without the section* (current behavior)?

### Candidate 4 — Force-close as a terminal disposition for incomplete stories

**Research position:** "Don't punt gaps." A force-close to `closed-incomplete` surfaces the gap but doesn't close it. The gap should either be rescoped into the next sprint explicitly or become an eval-set entry (regression signal), not sit as an "Unresolved Issues" bullet.

**Question for deciders:** Should Force-close require an artifact commitment (gap-closing story next sprint, or eval-set entry) before the retro can proceed?

---

## Feature Layer Integration Opportunities

The retro currently treats features as peripheral. Five places where the feature layer could become more central, with the research principle each is grounded in:

### Opportunity 1 — Load features.json at Phase 1

When the retro identifies the sprint, also load `_bmad-output/planning-artifacts/features.json` and build a feature-to-stories map for the sprint. This is a 5-line change that unlocks everything downstream.

*Research backing: Problem 4 rec 1 (North Star per feature); features.json already carries `acceptance_condition` which reads as the North Star.*

### Opportunity 2 — Add a Phase 3.5 gap check

After story verification, add a per-feature gap check: for each feature touched by sprint stories, ask "is the feature's `acceptance_condition` closer to observable?" Developer answers Y/N/Partial. "No for two consecutive sprints" triggers a re-plan recommendation.

*Research backing: Problem 4 rec 3 (gap question at sprint close); Problem 4 rec 5 (no silent punts).*

### Opportunity 3 — Feature status transitions in Phase 6

When a feature's `acceptance_condition` is judged observable, transition `features.json` status. When it's not, explicitly record "did not close this sprint" — produces a tracking signal the research says is missing.

*Research backing: Problem 4 rec 4 (pre-floor / post-floor state tracking).*

### Opportunity 4 — Feature-level Judgment Frame synthesis

When a feature transitions to `working` (acceptance_condition observable), the retro writes a paragraph: "What can a user do now that they could not before this sprint?" This is the feature-level Judgment Frame the research calls for.

*Research backing: Problem 2 rec 3 (feature as primary human-judgment unit).*

### Opportunity 5 — Features-at-risk surfacing

If a feature has had N sprints touch it without the acceptance_condition becoming observable, flag it as "at risk of punt" in the retro output. This is the mechanical detection of the "5-10 sprints and still not there" failure mode the research calls out by name.

*Research backing: Problem 4 (the owner-observed value floor failure); the failure mode the research treats as the most important addition.*

---

## Questions Raised

Open questions the analyst surfaces for deciders (synthesis, not instruction).

**On value-floor / gap checks:**
1. Is `acceptance_condition` in features.json the right source for the North Star capability, or should a new `north_star` field be introduced that is stricter (one sentence, observable)?
2. Where should the "was the gap closed this sprint?" judgment live — inline in Phase 6, or in a new dedicated phase (e.g., Phase 3.5 or Phase 7)?
3. Should a "no-gap-closed" finding be a hard block on sprint closure (research recommends this) or a soft warning (current workflow tone)?

**On eval-set construction:**
4. Should the Phase 5 routing grow from binary (distill | stub) to ternary (distill | eval | stub)? If so, what is the heuristic that routes a finding to the eval set — "reproducible failure with observable symptom"?
5. Where does the eval set live? Per the research, a project-local `eval/` directory. Does Momentum-the-practice have its own eval set for its own agents, distinct from the eval set of a downstream project?
6. Is the tester-agent pattern (Codecentric isolated specification testing) a prerequisite for the eval set to work, or can the eval set be text-only scenarios run manually?

**On transcript vs. outcome:**
7. Should Phase 2 gain a fifth extract — environmental state diffs (filesystem, git, DB) — alongside the four transcript extracts?
8. If running-app state is the ground truth, does the retro need to invoke a tester agent (Playwright, MCP) against the sprint's deliverables before the audit? This is a structural shift: audit becomes both retrospective analysis *and* post-hoc behavioral verification.

**On flow metrics:**
9. Is the Momentum orchestration already capturing enough timestamps to compute cycle time (per-story intake-to-done) and lead time (per-feature-touch intake-to-value-observed)? If not, what's the minimum schema addition to make those computable retroactively?

**On pre-floor / post-floor:**
10. Should sprints grow a `phase` field (pre-floor-infrastructure | walking-skeleton | post-floor-elaboration) to make the research's distinction tractable? If so, when is it set — at sprint-planning time, or inferred at retro time from outcomes?
11. The research says "Sprint 1 on a new feature targets the walking skeleton." Does that obligation belong to sprint-planning, and does the retro enforce it backwards (penalizing a sprint-1 that didn't attempt the skeleton)?

**On audit scope:**
12. The auditor team currently reads transcripts. Should it also read the sprint's **specs** (story files, Judgment Frames once they exist, feature acceptance_conditions) to compare stated intent against session behavior? This would operationalize the "judgment frame outcomes review" the research implies.
13. Is `auditor-review` the right lens to detect the CAISI-cheating pattern (tests passed without implementation, deleted tests), or does it need its own auditor role (`auditor-integrity`)?

**On tier routing:**
14. A Tier 1 distill applies the rule immediately — but the *next* sprint's retro cannot detect whether that rule worked. Is the missing feedback loop "did last sprint's distilled rules actually prevent the recurrence we expected?"?

**On summary production:**
15. The sprint summary is 500 words. Is its audience the developer (who read the findings doc already) or a future retrospective-of-retrospectives agent (which would benefit from structured data, not prose)? The answer changes the form factor.

---

## Relevant File Paths

- `/Users/steve/projects/momentum/skills/momentum/skills/retro/workflow.md` — retro workflow definition
- `/Users/steve/projects/momentum/skills/momentum/skills/retro/SKILL.md` — retro skill manifest
- `/Users/steve/projects/momentum/skills/momentum/skills/sprint-manager/references/state-machine.md` — story state transitions (retro's Force-close path)
- `/Users/steve/projects/momentum/skills/momentum/references/sprint-tracking-schema.md` — sprints/index.json and stories/index.json schemas
- `/Users/steve/projects/momentum/_bmad-output/planning-artifacts/features.json` — carries `acceptance_condition` per feature (candidate North Star source)
- `/Users/steve/projects/momentum/skills/momentum/skills/feature-status/workflow.md` — current feature status pipeline (read-only in retro Phase 6)
- `/Users/steve/projects/momentum/_bmad-output/research/adapting-agile-for-gen-ai-development-2026-04-13/synthesis/synthesis.md` — source research (Problems 1–4 and Recommended Adaptation Path)
