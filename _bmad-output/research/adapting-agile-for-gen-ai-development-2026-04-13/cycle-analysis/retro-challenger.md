# Retrospective Phase — Challenger Findings

## Executive Summary

The Momentum `retro` skill is an impressively-engineered artifact producing the wrong-shaped output. It is a six-phase ceremony that spawns a four-agent TeamCreate, preprocesses transcripts through DuckDB, synthesizes findings across three audit lenses, and writes a structured markdown report — then hands that report to a human to decide which items become backlog stubs. The research is blunt on what this optimizes for: **coding throughput is no longer the bottleneck; human judgment about value is.** The retro spends most of its token budget on *coding-throughput diagnostics* (which agents thrashed, which tools failed, which prompts caused rework) while the research's central gap — *did this sprint deliver user value, and are we closer to the value floor?* — is entirely absent from the workflow.

The retro has the correct instinct about harness engineering (Tier 1 → distill routing) but buries it inside Phase 5 of a skill whose primary output is a narrative audit document. The audit document itself reproduces the traditional "what worked well / what struggled" retrospective frame — an artifact the research explicitly says is being replaced by continuous quality monitoring in AI-native teams. And the retro does nothing to enforce that findings actually change the system: stubs get added to a backlog, findings get written to a file, and the system continues as before unless a *future* sprint picks up the stub.

Three specific failures deserve attention: (1) no value-validation gate at sprint close, (2) no feature-level "did we cross the value floor / gap close?" check, and (3) the Tier 1 → distill router is the right primitive but the rest of the workflow drowns it. A lighter sprint-close gate with the distill router and a value check would deliver more practice improvement per retro-hour than the current ceremony.

---

## Assumed Truths That The Research Questions

The retro skill embeds five assumptions that the synthesis directly challenges.

**Assumption 1: A sprint retrospective is a ceremony worth running.**
Research position: *"Continuous quality monitoring replaces retrospectives"* is explicit in the synthesis (Problem 3, and implicit in the DORA "AI as amplifier" position). The retro's function — pattern detection across agent behavior — is the kind of work AI can do continuously, not on a weekly cadence. A per-story hook-based analyzer that flags "this subagent had >5 tool errors" at the moment of failure is more actionable than finding it in a retro seven days later, after the memory of context has decayed.

**Assumption 2: The primary output of a retro is observations.**
The retro's Phase 4 produces `retro-transcript-audit.md` — an elaborate document with sections like "What Worked Well," "What Struggled," "User Interventions," "Cross-Cutting Patterns." This is a traditional *team* retrospective shape. For a solo practitioner, the research says the relevant output is *harness change* (Fowler / Böckeler: "humans on the loop, redesigning the harness"), not a narrative. An audit document that doesn't force harness mutation is vestigial ceremony.

**Assumption 3: The right time to catch problems is at sprint close.**
Problem 4 of the synthesis — the value floor — is explicit that punting failures happen *during* the sprint, not at its end. *"Pre-floor, shipping stories that don't reduce the gap is waste, even if the stories are correct."* Retro-at-the-end catches the punt after the fact. A pre-sprint gap artifact and a mid-sprint gap check would catch the punt before it compounds. The retro runs when the damage is already cemented.

**Assumption 4: The sprint is the right unit for a retrospective.**
The synthesis leans hard toward PR-centric continuous flow (OpenAI Codex data) and event-driven reflection over sprint-boundary ceremonies. A retro skill that only fires at sprint close encodes the sprint as the primary learning boundary — but for a solo practitioner doing weekly governance, meaningful signal arrives at story-merge and feature-close, not at arbitrary calendar boundaries.

**Assumption 5: A structured auditor team produces better findings than a single synthesis pass.**
This is the most expensive assumption. The Phase 4 TeamCreate spawns four agents (human, execution, review, documenter) with SendMessage collaboration. For a solo practitioner with weekly sprints containing ~5–10 stories, this is probably over-engineered instrumentation. The research on AI review (CAISI, arxiv 2603.25773) says AI-review-of-AI-work produces correlated failure — spawning more reviewing agents doesn't escape the correlation; it just generates more tokens of correlated output. A single synthesis pass plus a human with the transcript extract open would likely produce equivalent signal.

---

## The Value Floor Risk

**This is the most serious gap.** The retro skill has no concept of "did the sprint deliver user value" or "are we closer to the North Star capability than we were before." It asks a completely different set of questions.

Evidence from `workflow.md`:

- Phase 3 (Story Verification) checks *"did every sprint story reach done status?"* — this is a spec-completion question, not a value question. The research's exact critique: *"these are different questions, and in AI-native development the second question gets answered automatically while the first goes unasked."*
- Phase 4 (Auditor Team) categorizes findings as `correction | redirection | frustration | praise | decision`, `duplication | error-pattern | efficiency | iteration | abandon`, and `real-catch | false-positive | thrash | coordination | prompt-quality`. Every category is about *agent execution quality*. None are about *delivered user value*.
- Phase 6 (Sprint Closure) produces a sprint-summary.md with sections `Features Advanced`, `Stories Completed vs. Planned`, `Key Decisions`, `Unresolved Issues`, `Narrative`. "Features Advanced" is close — it at least names features — but the section draws from `feature-status.md` which tracks story-to-feature coverage, not user-observable behavior change.

**What's missing, specifically:**

1. **No gap-check question at sprint close.** The research's prescribed question — *"are we closer to the North Star capability than before this sprint?"* — is not asked anywhere in the workflow. The closest surface is `sprint-summary.md`'s Narrative paragraph, which is a free-text field with no required answer to this question.

2. **No pre-floor / post-floor awareness.** The retro treats every sprint identically. A pre-floor sprint (core capability not yet reachable) and a post-floor sprint (incremental elaboration) should have different success criteria. The retro has one shape.

3. **No value-validation gate.** The synthesis is explicit: *"Add a value-validation gate to the sprint close, not to the story close."* The retro is *the* sprint-close moment and it does not contain this gate. For each feature touched by the sprint, the retro should force: "observable user behavior that confirms value delivery" — either checked, queued, or flagged. This is absent.

4. **Punt detection is impossible.** The retro has no mechanism to detect that a feature has been "punted" sprint-after-sprint without closing its gap. The feature-status artifact tracks story coverage (story X → feature Y) but not gap-closure direction. A feature can accumulate completed stories indefinitely while its user-value floor remains uncrossed, and nothing in the retro surfaces this.

**Impact:** The retro is the *last* opportunity to catch a pre-floor punt before the team re-plans the next sprint. Missing this turns every sprint into another round of elaboration on bones that don't walk yet.

---

## Overbuilt vs. Underbuilt

### Overbuilt

**The auditor team (Phase 4).** Four agents, TeamCreate, SendMessage collaboration, three separate JSONL extracts, ad-hoc DuckDB queries, a synthesis documenter. For a solo practitioner's weekly sprint of 5–10 stories with maybe 20–30 subagent sessions, this is a freight train hauling a sandwich. The token cost of four agents collaborating iteratively to produce a retrospective document likely exceeds the token cost of the sprint itself for small sprints.

**The transcript preprocessing pipeline (Phase 2).** Four DuckDB extractions (user-messages, agent-summaries, errors, team-messages). Auto-install duckdb. Date-range discovery. Session file resolution. The infrastructure is elegant; it's also answering yesterday's question. The research says continuous monitoring replaces retrospectives — every one of these queries could be a hook that writes to a rolling log during the sprint, and the retro consumes the pre-aggregated result rather than kicking off fresh extraction at the end.

**The findings document structure.** Seven required sections (Executive Summary, What Worked Well, What Struggled, User Interventions, Story-by-Story Analysis, Cross-Cutting Patterns, Metrics, Priority Action Items). This is the shape of a team retrospective document, and it's aspirational — the document exists to be *read later* as part of a continuity story. For a solo practitioner, the probability of re-reading retro-transcript-audit.md six weeks later is roughly zero. The document's value is in its generation moment only.

**Phase 6 sprint summary production.** A word-count-limited narrative with Features Advanced, Stories Completed, Key Decisions, Unresolved Issues, Narrative sections. This is stakeholder-communication ceremony — the artifact presumes an audience that doesn't exist in a solo practice. The practitioner was present for the entire sprint; they don't need a summary for themselves.

### Underbuilt

**Harness change enforcement.** The Phase 5 Tier 1 → distill routing is the single most important mechanic in the workflow — it's the only part that actually changes the practice atomically. But it applies only to findings *already flagged with `signal_type`* during Phase 4. The workflow gives no detail on how Phase 4 agents decide whether to set `signal_type`. If they don't set it, the finding becomes a stub (best case) or fades (worst case). The retro does not enforce that *every critical finding must be either distilled or stubbed* — it allows findings to be merely documented.

**Value validation.** Covered above — entirely absent.

**Gap analysis.** No "Here / There / Gap / Path check" artifact, no feature-level "is the North Star reachable" question, no pre-floor/post-floor tracking.

**Harness staleness detection.** The retro is the natural moment to ask "which rules files were added/modified during this sprint, and did they actually change behavior?" No step does this. A rule added three sprints ago and never triggered is either dead code or defensive wallpaper; the retro should surface it.

**Continuous signal replacement.** The research predicts continuous quality monitoring displaces retrospectives. The retro makes no gesture toward emitting the kind of signals (per-story events, per-subagent anomalies, per-tool-failure spikes) that would populate a continuous dashboard. It treats retro as the terminal synthesis, not a backfill for gaps in continuous observation.

**Post-commit reflection cadence.** In a solo practice, the higher-value reflection moments are *per-story merge* (while the context is fresh) and *per-feature close* (when value is observable). The retro skill doesn't subdivide these — everything collapses into the weekly retro. A per-merge "lessons captured" hook that feeds distill would catch signal while the context exists; the weekly retro could then operate on the accumulated flow rather than cold-starting analysis from raw JSONL.

---

## Structural Misalignments

**Misalignment 1: The ceremony inherits team-retrospective shape in a solo context.**
The four-agent auditor team is a simulation of the three-roles-plus-facilitator pattern from Scrum retrospectives (what worked / what didn't / how to improve). For a single-practitioner practice, this is cargo. The practitioner was both the "human" being audited and the engineer reviewing the auditors — the separation of concerns that makes team retros work (people have different perspectives) doesn't obtain. The same cognitive process (practitioner + transcript extracts + a single synthesis pass) would produce equivalent findings at a fraction of the cost.

**Misalignment 2: Sprint closure and retrospective are coupled.**
`retro` owns sprint closure (Decision 34 is referenced in the workflow header). This couples two functions that have different frequencies:
- **Sprint close** is a transactional state transition — move the sprint record to completed, clear the active slot. Cheap, must happen every sprint.
- **Retrospective** is a reflective learning ritual — expensive, should happen when there's enough accumulated signal to warrant reflection.

Coupling forces a retro every sprint whether or not there's signal. For a solo practitioner doing weekly governance sprints with small story counts, most sprints produce insufficient signal for a full retro to pay back its cost. The coupling also means if you skip the retro for time reasons, the sprint never closes — so retro becomes load-bearing for sprint-state hygiene, which is the opposite of what should be true.

**Misalignment 3: Distill is a sub-step of retro, but distill is the valuable primitive.**
Phase 5's Tier 1 distill routing is where harness actually changes. But distill is gated behind (a) a sprint completing, (b) retro running, (c) Phase 4 agents tagging findings with `signal_type`, (d) the Tier 1 heuristics matching, (e) the practitioner approving. Five gates on the thing that matters. Meanwhile the findings document (which doesn't change the harness) has zero gates — it is written unconditionally.

A better shape: *distill runs continuously* (per-merge, per-failure, per-intervention), and retro becomes a thin gate that audits "did we distill everything we should have?" rather than the primary distillation surface.

**Misalignment 4: The workflow fidelity rule binds without a cost-benefit check.**
Project rules (`workflow-fidelity.md`) require every step to be executed as written. For `retro`, this means the four-agent TeamCreate fires every time — even when the sprint produced trivial output. The rule is correct in spirit (don't silently skip delegations) but doesn't provide an escape hatch for "this sprint was one story; full retro is overkill." A one-story sprint should trigger a lightweight gate, not a full ceremony. Without a size-aware dispatch in the workflow, fidelity cost dominates small sprints.

**Misalignment 5: Story stubs as the primary feedback path.**
Phase 5 converts findings to backlog stubs. The implicit theory: findings become stories become sprints become fixes. This works for large changes but has three failure modes:
- **Latency.** A finding about "dev agent kept asking for clarification on X" becomes a stub that might be sprint-planned in two weeks. The fix arrives three sprints after the failure pattern started.
- **Dilution.** Stubs accumulate in the backlog; backlog refinement prioritizes by practitioner judgment, not by finding frequency; stubs that never reach the top die quietly.
- **Mismatch.** Many findings are Tier 1 (single rule addition, one-line prompt clarification) — they don't need a story. Phase 5 routes these correctly *if* the auditor set `signal_type` *and* heuristics match. Two conditional gates on the fastest feedback path.

The feedback flywheel the research describes is *immediate application of micro-learnings*. The retro's architecture inverts this — immediate is the exception, delayed is the default.

---

## The Feature Layer Question

The owner's research framing (Problem 4) places the North Star capability at the *feature* level, not the story level. The retro operates almost entirely at the story level.

Evidence:
- Phase 3 verifies every story reached `done`.
- Phase 4 produces per-story analysis.
- Phase 5 creates story stubs.
- Phase 6's sprint summary has a `Features Advanced` section — but it draws from `feature-status.md` which reports story-coverage, not value-floor crossing.

The feature layer is the correct grain for the value question. The synthesis is explicit: *"The story is the AI's unit. The feature — or the 'shaped pitch' — is the human's unit."*

**Concrete absences at the feature layer:**

1. **No feature-level North Star check.** The retro doesn't ask, per feature touched: "what is the minimum user-observable capability we promised this feature delivers, and did this sprint get us closer?"

2. **No feature-level judgment frame review.** The synthesis prescribes a Judgment Frame per feature (Intent / Done-state-for-a-stranger / Anti-goals / Review focus). The retro doesn't check whether the sprint's completed stories honored the feature's judgment frame or drifted from it.

3. **No feature-level walking-skeleton enforcement.** If a feature is pre-floor, Sprint 1 on that feature must target end-to-end capability. The retro has no concept of pre-floor / post-floor and therefore cannot flag "this sprint was supposed to be walking-skeleton and instead elaborated on a non-existent core."

4. **feature-status is read, not mutated.** The retro calls `momentum:feature-status` to refresh the HTML view, but the feature-status workflow reports story → feature coverage; it doesn't ask value-floor questions. Feeding feature-status into the sprint summary preserves the story-coverage framing without surfacing value.

**The structural problem:** the retro has been designed to close a sprint by verifying stories completed and distilling agent-behavior lessons. It has not been designed to close a sprint by verifying *the product moved*. Those are different ceremonies. The current retro does the first well and the second not at all.

---

## Hard Questions for the Owner

1. **If the retro only produces an audit document and some backlog stubs, and neither the document nor most stubs get read/actioned within two weeks, what is the retro actually paying for?** The token and time cost of the four-agent auditor team is substantial. Is there evidence that past `retro-transcript-audit.md` files have been re-consulted when planning subsequent sprints, or are they write-only artifacts?

2. **Why is distill a Phase 5 sub-step instead of a continuous primitive?** The distill skill already exists and is routable. Distill called from a post-story hook (triggered at merge) would apply micro-learnings at the moment of freshest context. Retro would then become a gate that audits "did distill fire enough?" rather than the primary distillation surface. What prevents this inversion?

3. **The sprint summary in Phase 6 is written to `sprint-summary.md` with strict word count rules and structured sections. Who is the audience for this document in a solo practice?** If the practitioner was present for the sprint, they don't need a summary. If the audience is "my future self six months from now," that's a different use case than the sprint-summary format serves well (project history would want a running log, not a series of sprint-scoped summaries).

4. **Decision 27 (Findings Document) and Decision 34 (Retro Owns Sprint Closure) are referenced as architecture commitments. Are these decisions revisitable?** Specifically: Decision 34 couples sprint closure to retro completion. In the research's framing, sprint closure is transactional and frequent; retrospection is reflective and size-dependent. The coupling forces the full ceremony even on trivial sprints. Is this a load-bearing invariant, or is it revisitable?

5. **Where in the Momentum cycle does "did this sprint deliver user value" get asked?** If the answer is "nowhere," then the research's value-validation gap exists in Momentum. If the answer is "at the feature or product level, not the sprint level," then which skill owns that question, and how often does it actually fire?

6. **What happens to a feature that's been "punted" three sprints in a row?** Is there any surface in the current Momentum system that flags this? feature-status tracks story coverage; the backlog tracks stories; sprints/index.json tracks sprint completion. None of these surface "this feature has been open for 30 days and its North Star is not closer." Who or what should catch this, and when?

7. **Is the traditional "what worked / what struggled" retrospective frame still useful in an AI-first practice, or is it ceremonial debt?** The research says continuous quality monitoring replaces retrospectives. If the retro's primary job is converting agent-behavior patterns into harness changes, a continuous hook-based analyzer targeting those specific patterns would do the job better, more immediately, and with less token cost. What's the actual case for the ceremony shape the retro currently has?

8. **The workflow-fidelity rule forbids skipping delegations. For a single-story sprint, does the full four-agent auditor team still fire?** If yes, fidelity is costing more than it saves on small sprints. If no, the workflow has undocumented escape hatches and needs a size-aware dispatch. Which is it?

9. **The Tier 1 → distill routing is the retro's most valuable primitive. Why is it gated behind `signal_type` being set by a Phase 4 agent?** If Phase 4 agents forget to set `signal_type`, a Tier 1 finding silently degrades to a Tier 2 stub — a fifth-wheel finding that won't be applied until it survives backlog refinement. Should the Tier classification run independently of `signal_type`, with `signal_type` being an auditor hint rather than a gate?

10. **If the retro were deleted tomorrow and replaced with a 10-minute sprint-close gate (verify stories, run distill on any queued learnings, answer the three gap questions, transition sprint state), what would be lost?** Name the specific findings or harness changes that the current retro produces that the lightweight gate would miss. If the answer is "mostly the audit document," that's a telling answer.
