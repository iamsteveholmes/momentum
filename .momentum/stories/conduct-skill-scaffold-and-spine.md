---
title: Conductor orchestrator skill scaffold and workflow spine
story_key: conduct-skill-scaffold-and-spine
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - skill-instruction
verification_method: skill-invoke
depends_on:
  - conduct-spec-revision-dec036
touches:
  - skills/momentum/skills/conductor/SKILL.md
  - skills/momentum/skills/conductor/workflow.md
---

# Conductor orchestrator skill scaffold and workflow spine

## Story

As a solo developer running the Momentum practice,
I want a Conductor orchestrator skill that owns the in-session build phase as a single, well-sequenced workflow spine,
so that an entire sprint's worth of stories is built autonomously with all git mutation and agent spawning concentrated in one accountable place, and I am asked to engage only at a small, well-defined set of touchpoints rather than being interrupted story by story.

## Description

This story creates the keystone of the conduct leg: the Conductor orchestrator skill and its workflow spine. `conduct` is the in-session, per-story, autonomous-build, single-end-gate rewrite of the legacy `momentum:sprint-dev`. The Conductor is the top-level session orchestrator that owns the build phase end to end — it is the sole authority for git mutation and for spawning subagents, and it writes no code, spec, or fix itself. Every other piece of the conduct leg (per-story pipelines, the auto-fix loop, the escalation mechanism, the report, the end-gate) hangs off this scaffold and its spine.

**What it delivers:** a new `skills/momentum/skills/conductor/SKILL.md` plus a `workflow.md` that sequences the whole build: a Phase-1 pre-flight, the build phase made of per-story pipelines, AVFL-on-merge, an end-to-end (E2E) validation pass, and a single human end-gate at the very end.

**Why:** Today the practice asks the developer a question at many points during a multi-story build, which fragments attention and makes long sprints exhausting to supervise. DEC-035 adopts conduct precisely to collapse that to ONE human gate at the end, with no story-count cap, so the developer can let a sprint run and review the whole thing once at the finish line. Concentrating all git mutation and all agent spawning in the Conductor makes the build auditable and prevents subagents from racing each other on the working tree.

**Pain context:** Story-by-story human gates are the dominant supervision cost in long sprints. The build either nags the developer constantly or, if it goes silent, hides everything until the end. DEC-036 resolves this tension by keeping the build silent for routine work while permitting a narrow, high-bar exception: a small set of genuinely stakes-class findings may pause the build and ask, mid-flight. This story must lay the structural groundwork for that exception in the spine — a pause-ask-resume control-flow branch — without building the decision engine (which is a separate story).

**Source decisions:** DEC-035 (adopt conduct; one human end-gate; no story-count cap), and DEC-036 (narrow, stakes-gated mid-flight escalation tier amending DEC-035 decision #1). Governing spec sections: section 3 (Conductor + per-story pipeline), section 2 (end-to-end flow), section 8 (single end-gate).

## Acceptance Criteria

1. Invoking the Conductor skill produces a runnable orchestrator: it loads cleanly with no missing-file or malformed-frontmatter errors, presents itself as the top-level build orchestrator for a sprint, and its scaffold conforms to skill conventions — a one-line description of at most 150 characters, declared model/effort frontmatter, and a skill body of at most 500 lines.

2. The Conductor exposes a single, ordered workflow spine that sequences these phases in this order: (a) a Phase-1 pre-flight, (b) the build phase composed of per-story pipelines, (c) AVFL-on-merge, (d) an end-to-end (E2E) validation pass, and (e) a single human end-gate. The ordering is observable from the workflow: no later phase runs before its predecessor, and the end-gate is unambiguously last.

3. The Conductor is the sole git-mutation authority during the build: any creation of branches, commits, merges, or other changes to repository history that occur during a build run are attributable to the Conductor's orchestration, and the spine instructs subagents not to mutate git themselves.

4. The Conductor is the sole agent-spawning authority during the build: the spine spawns every subagent the build needs, and no spawned subagent spawns further build agents on its own.

5. The Conductor writes no code, spec, or fix itself: across the whole spine, the act of producing build output (code, spec text, fixes) is always delegated to a spawned subagent, never performed inline by the Conductor.

6. The build phase imposes no story-count cap: the spine processes however many stories the sprint contains, in sequence of per-story pipelines, without a hardcoded limit and without inserting a human gate between stories.

7. The default supervision contract holds: during a normal build with only routine work, the Conductor asks the developer nothing between the start of the build and the single end-gate. The only two developer-facing touchpoints on the routine path are the start of the run and the end-gate.

8. The spine includes an explicit escalation control-flow branch: a pause-ask-resume path the build can enter, in which the build halts, surfaces a developer-facing prompt, and resumes from where it paused once the developer responds. This branch is present as structural acknowledgment only — the spine references it as a defined path but does not implement the decision logic that selects findings for it (that logic is delivered by a separate story).

9. The spine's stated supervision invariant is the softened DEC-036 form: "the Conductor never asks the developer during build, EXCEPT the narrow stakes-and-timing mid-flight escalation tier." The invariant text explicitly carves out this single exception and frames it as narrow, rather than asserting an absolute no-questions-during-build rule.

10. The mid-flight escalation exception is documented as narrow and high-bar: the spine describes the escalation branch as reserved for a small, stakes-gated set of findings and does not present it as a general-purpose way to ask the developer questions during the build. Routine findings are never routed to this branch.

11. The single end-gate is the only place the build hands off to the developer for final acceptance: after E2E completes, the spine reaches exactly one human end-gate, and no second mandatory human acceptance gate exists elsewhere in the spine.

## Tasks / Subtasks

- [ ] Create the skill directory `skills/momentum/skills/conductor/`.
- [ ] Author `skills/momentum/skills/conductor/SKILL.md`:
  - [ ] Frontmatter with a description of at most 150 characters, plus model and effort fields.
  - [ ] Body of at most 500 lines establishing the Conductor as the top-level, in-session build orchestrator for a sprint.
  - [ ] State the four authority/restraint invariants: sole git-mutation authority, sole agent-spawning authority, writes no code/spec/fix itself, no story-count cap.
  - [ ] State the supervision invariant in the softened DEC-036 form (never asks during build EXCEPT the narrow stakes-and-timing mid-flight escalation tier).
  - [ ] Point to `workflow.md` as the executable spine.
- [ ] Author `skills/momentum/skills/conductor/workflow.md`:
  - [ ] Sequence the spine: Phase-1 pre-flight → build phase (per-story pipelines) → AVFL-on-merge → E2E → single end-gate.
  - [ ] Define the per-story pipeline shell inside the build phase as the repeated unit (no count cap, no inter-story human gate).
  - [ ] Instruct that all git mutation flows through the Conductor and that spawned subagents do not mutate git or spawn further build agents.
  - [ ] Instruct that all build output is delegated to spawned subagents; the Conductor performs no inline authoring.
  - [ ] Add the escalation control-flow branch as a defined pause-ask-resume path: halt → surface developer prompt → resume from the pause point. Mark it as structural acknowledgment; defer the selection/decision engine to the stakes-timing escalation mechanism story.
  - [ ] Document the two routine developer touchpoints (run start, end-gate) and the third narrow escalation surface inside the build phase.
  - [ ] Place the single human end-gate unambiguously last, after E2E.
- [ ] Cross-check that the touchpoint count and ordering match DEC-035 and the DEC-036 amendment before marking the story done.

## Dev Notes

This is the keystone scaffold for the conduct leg. Build it so the rest of the leg can hang off it cleanly: later stories supply the per-story pipeline internals, the auto-fix loop, the escalation decision engine, the functionality-organized report, and the anti-rubber-stamp end-gate. Keep this story to the skeleton — the spine's phase ordering, the four authority invariants, and the two-plus-one touchpoint contract — and leave the engines hollow where the brief says they belong elsewhere.

Governing spec sections (cite by number; do not open the spec): section 3 (Conductor role and the per-story pipeline) defines the Conductor's authority surface and the repeated build unit; section 2 (end-to-end flow) defines the phase sequence the spine must mirror; section 8 (single end-gate) defines the final human acceptance point.

The DEC-036 amendment is narrow on purpose. The mid-flight escalation tier is for irreversible-and-imminent OR build-invalidating findings only — bias narrow; the end-gate-expanded tier is the safety net for everything else, and routine findings are always auto-fixed silently. In this story you only acknowledge the pause-ask-resume branch structurally and soften the invariant text; do NOT widen the bar or implement which findings qualify. The selection logic lives in the separate stakes-timing escalation mechanism story (this story's `depends_on` is the spec revision that defines the amendment; the mechanism that consumes it is downstream).

Supervision-invariant wording matters: the spine must read "never asks during build EXCEPT the narrow stakes-and-timing mid-flight escalation tier" rather than an absolute no-questions claim, because an absolute claim would contradict DEC-036 and leave no defined home for the escalation branch.

This is a markdown/bash repo: the deliverables are skill-instruction artifacts (SKILL.md + workflow.md), verified by invoking the skill (skill-invoke), not by running application code. There is no app/UI/backend lane.

### References

- Epic: `momentum-sprint-orchestration` — "The required core of the Momentum cycle (sprint-planning → sprint-dev → retro) and its execution engine: concurrent agent waves, merge sequencing, quality gate integration, and team composition." (`_bmad-output/planning-artifacts/epics.json`). conduct is the per-story, single-end-gate rewrite of the sprint-dev execution engine within this epic.
- Decision: DEC-035 — adopt conduct; one human gate at the end; no story-count cap; report organized by user-facing functionality; legible auto-fix loop.
- Decision: DEC-036 — narrow, high-bar, stakes-gated mid-flight escalation tier amending DEC-035 decision #1; routine findings stay always auto-fixed; anti-firehose intent preserved.
