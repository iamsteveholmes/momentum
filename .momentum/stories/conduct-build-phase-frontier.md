---
title: "Conductor build phase: dependency frontier with a mid-flight escalation consumption hook"
story_key: conduct-build-phase-frontier
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - skill-instruction
verification_method: skill-invoke
depends_on:
  - conduct-skill-scaffold-and-spine
touches:
  - skills/momentum/skills/conductor/workflow.md
---

# Conductor build phase: dependency frontier with a mid-flight escalation consumption hook

## Story

As the Conductor running a sprint's build phase,
I want an event-driven dependency frontier that launches every unblocked story concurrently and reacts to per-story completion signals,
so that the whole feature epic builds in one continuous autonomous flow that never stalls and never silently swallows a stakes-class finding that meets the narrow mid-flight bar.

## Description

This story specifies the **build phase** of the Conductor: the loop that drives the feature-epic stories from "ready" to "merged" without a human in the middle of the flow. The Conductor reads the sprint's story set (its index and each story's `depends_on`), computes the set of stories whose dependencies are all satisfied (a dependency **frontier**), and launches those stories — concurrently, with **no story-count cap** — through the one-story build pipeline. As each story's pipeline reports a terminal signal, the Conductor re-evaluates the frontier and launches whatever just became unblocked. The phase ends when no story can advance further.

**What is being built:** instructions in the Conductor skill's `workflow.md` that define this frontier loop as an event-driven heartbeat — gate stories on `>= review`, launch the frontier, react to `merged` by re-evaluating and launching the newly-unblocked, react to `failed` with a bounded retry that continues rather than halts, and **consume** the escalation mechanism when a per-story pipeline surfaces a stakes-class finding meeting the narrow mid-flight bar.

**Why / pain context:** The legacy `momentum:sprint-dev` builds in discrete waves with a human gate between waves, which fragments long sprints into stop-and-wait segments and forces the developer to babysit the run. DEC-035 adopts the Conductor model: one autonomous build flow with a single human gate at the very end, no story-count cap, and a legible auto-fix loop. The build phase is the engine that makes "single end-gate" possible — without a non-halting frontier, any single story failure would strand the rest of the sprint and re-introduce mid-flow human intervention.

**The DEC-036 amendment (the consumption hook):** A pure "never halt, always auto-fix" frontier is too absolute. DEC-036 narrowly amends DEC-035's first binding decision to permit a high-bar, stakes-gated **mid-flight escalation tier**. The build phase must therefore carry a **consumption hook**: between a per-story pipeline's terminal signal and the frontier's "continue" action, the Conductor checks whether that pipeline surfaced a stakes-class finding that meets the **narrow mid-flight bar** — *irreversible-and-imminent* OR *build-invalidating*, and nothing else. If so, the frontier defers to the escalation mechanism and **pauses that branch** rather than silently continuing or auto-fixing it. The frontier does **not** implement detection or classification; it only consumes the mechanism. Routine findings never trigger the hook, so the anti-firehose intent of DEC-035 is fully preserved.

Source decisions: **DEC-035** (adopt Conductor; one human gate at the end; no story-count cap; legible auto-fix loop) and **DEC-036** (narrow, high-bar, stakes-gated mid-flight escalation tier amending DEC-035 binding decision #1).

## Acceptance Criteria

1. The build phase launches every story whose `depends_on` entries are all at status `>= review`, and launches them concurrently.
2. There is no story-count cap on the build phase: when more than any fixed number of stories are unblocked at once, all of them are launched (none are deferred solely because of how many are ready).
3. When a story reaches `merged`, the build phase re-evaluates the dependency frontier and launches every story that has just become newly unblocked as a result.
4. When a story's pipeline exhausts its bounded retries, the build phase marks that story blocked and **continues** with the rest of the frontier — it never halts the whole phase on a single story's failure.
5. The build phase runs as a continuous event-driven heartbeat: it reacts to each per-story terminal signal (merged or failed) and never requires a human to advance the flow between stories.
6. The build phase carries a **consumption hook** between a per-story pipeline's terminal signal and the "continue" action: before continuing, it checks whether that pipeline surfaced a stakes-class finding meeting the narrow mid-flight bar.
7. When a per-story pipeline surfaces a stakes-class finding that meets the narrow mid-flight bar (**irreversible-and-imminent OR build-invalidating, and nothing wider**), the build phase invokes the escalation mechanism and **pauses that branch** instead of silently continuing or auto-fixing it.
8. The build phase **defers to** the escalation mechanism for detection and classification — it does not itself detect, classify, or decide what constitutes a stakes-class finding; it only consumes the mechanism's outcome.
9. A **routine** finding never triggers the consumption hook: the affected branch continues (the routine finding stays on the always-auto-fix path) and no mid-flight pause occurs (the anti-firehose intent is preserved).
10. The mid-flight bar stays narrow: a stakes-class finding that does **not** meet "irreversible-and-imminent OR build-invalidating" does not pause its branch mid-flight; it is left for the end-gate-expanded tier rather than widening the mid-flight trigger.
11. Pausing one branch via the consumption hook does not halt the rest of the build phase: other unblocked stories continue to launch and advance.

## Tasks / Subtasks

- [ ] Define the build-phase frontier in `skills/momentum/skills/conductor/workflow.md`
  - [ ] Specify reading the sprint's story set (story index + each story's `depends_on`) to compute the dependency frontier
  - [ ] Specify the readiness gate: a story is launchable when all of its `depends_on` are at status `>= review`
  - [ ] Specify concurrent launch of the full frontier with **no story-count cap** (AC 1, AC 2)
- [ ] Define the event-driven heartbeat reactions
  - [ ] On a `merged` terminal signal: re-evaluate the frontier and launch every newly-unblocked story (AC 3)
  - [ ] On a `failed` terminal signal: apply a bounded retry; on exhausted retries, mark the story blocked and continue the phase — never halt (AC 4)
  - [ ] Specify that the heartbeat needs no human input to advance between stories (AC 5)
- [ ] Define the mid-flight escalation **consumption hook**
  - [ ] Insert the hook between a per-story pipeline's terminal signal and the "continue" step (AC 6)
  - [ ] Specify the narrow mid-flight bar that gates the hook: irreversible-and-imminent OR build-invalidating only (AC 7, AC 10)
  - [ ] Specify that the frontier **invokes the escalation mechanism and pauses that branch** when the bar is met, instead of silently continuing or auto-fixing (AC 7)
  - [ ] Specify that detection/classification is **deferred to** the escalation mechanism — the frontier does not implement it (AC 8)
  - [ ] Specify that routine findings bypass the hook and keep the branch on the always-auto-fix path (AC 9)
  - [ ] Specify that a paused branch does not halt the rest of the phase (AC 11)
- [ ] Cross-check the workflow text against DEC-035 (single end-gate, no cap, legible auto-fix) and DEC-036 (narrow mid-flight tier) so no instruction widens the mid-flight bar
- [ ] Self-verify by invoking the Conductor skill against a representative sprint fixture and confirming the observable frontier and hook behaviors

## Dev Notes

This story builds **skill instructions only** — the frontier and its consumption hook live as workflow text in `skills/momentum/skills/conductor/workflow.md`. There is no application, UI, or backend lane; everything is markdown/bash skill authoring. The Conductor scaffold and spine (`conduct-skill-scaffold-and-spine`) must already define the skill shell, the per-story pipeline contract, and the escalation mechanism this hook consumes — hence the `depends_on`.

**Governing spec sections (by number, per the authoring brief):**
- **Section 3** — per-story dependency gating, frontier re-evaluation, and the one-story build pipeline. This is the primary grounding for AC 1–5: the `>= review` readiness gate, concurrent launch, the `merged`-triggers-re-evaluation rule, and the bounded-retry/continue-don't-halt behavior on `failed`.
- **Section 2** — the overall Conductor spine the build phase plugs into (the event-driven session loop, terminal signals, and the boundary between what the Conductor owns versus what subagents own).

**Design constraints to honor:**
- The Conductor writes no code itself; the frontier launches subagent pipelines and reacts to their terminal signals.
- **No story-count cap** is a DEC-035 D4 invariant — do not introduce any concurrency ceiling that defers a ready story purely on count.
- **Never halt** on a single-story failure — a stranded story is marked blocked and the phase proceeds (DEC-035 single-end-gate depends on this).
- The consumption hook **defers to** the escalation mechanism. This story must not author detection or classification logic for stakes findings — that belongs to the mechanism. Keep the frontier's role to: observe the pipeline's terminal signal, consume the mechanism's outcome, and pause-the-branch vs. continue accordingly.
- **Keep the mid-flight bar narrow.** Only *irreversible-and-imminent* OR *build-invalidating* stakes findings may pause a branch mid-flight. Everything else — including stakes-class findings that don't meet the bar — defers to the end-gate-expanded tier. The mid-flight tier is deliberately the exception; the end-gate is the safety net. Do not widen the trigger.
- **Anti-firehose preserved:** routine findings (the default class) never reach the hook; they stay on the always-auto-fix path so the build flow is not flooded with mid-flight pauses.

**Vocabulary used (keep consistent):** stakes classes = security/auth-isolation; irreversible/destructive (migration, delete, force-push, prod deploy); high-blast-radius/architecture; default routine. Dispositions = fixed | dismissed (non-empty rationale required) | triaged-out | escalated (raised, not silently fixed). Timing tiers = end-gate-expanded (default) | mid-flight (narrow). For this story the relevant disposition is **escalated** and the relevant timing tier is **mid-flight**.

### References

- Epic **momentum-sprint-orchestration** — `_bmad-output/planning-artifacts/epics.json`: "The required core of the Momentum cycle (sprint-planning → sprint-dev → retro) and its execution engine: concurrent agent waves, merge sequencing, quality gate integration, and team composition." This story replaces the legacy wave engine with the Conductor's continuous dependency frontier.
- **DEC-035** — adopt the Conductor; one human gate at the end; no story-count cap (D4); report organized by user-facing functionality; legible auto-fix loop.
- **DEC-036** — narrowly amends DEC-035 binding decision #1: permits a narrow, high-bar, stakes-gated mid-flight escalation tier (D1/D2); stakes-class findings meeting the bar leave the silent auto-fix path; routine findings stay always-auto-fixed; the anti-firehose intent is preserved and the mid-flight bar must stay narrow.
