---
title: Conductor stakes-and-timing mid-flight escalation mechanism
story_key: conduct-stakes-timing-escalation-mechanism
status: ready-for-dev
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
change_type:
  - skill-instruction
verification_method: skill-invoke
depends_on:
  - conduct-skill-scaffold-and-spine
  - conduct-build-phase-frontier
  - directed-fix-finding-schema
touches:
  - skills/momentum/skills/conductor/workflow.md
  - skills/momentum/skills/conductor/references/escalation.md
---

# Conductor stakes-and-timing mid-flight escalation mechanism

## Story

As a developer running a conduct build,
I want the Conductor to pause-ask-resume on only a narrow, high-bar class of mid-flight findings,
so that irreversible-and-imminent or build-invalidating decisions are surfaced to me before they happen, while all routine work stays autonomous and collapsed for the single end-gate.

## Description

This story builds the Conductor-side **pause-ask-resume escalation engine** — the mid-flight escalation tier that DEC-036 D1 introduces. It is the new intermediate gate that DEC-036 amends DEC-035 binding decision #1 to permit: a single, narrow, high-bar interruption between the start of the build and the terminal end-gate.

The engine does four things in sequence:

1. **Reads** the stakes finding-class and timing tier off a per-story pipeline / validation result (the stakes-class field is produced upstream by `directed-fix-finding-schema`).
2. **Evaluates** the DEC-036 D1 narrow, high-bar timing condition — **irreversible-and-imminent OR build-invalidating** — and **fires only on that bar**. Everything that does not hit the bar stays autonomous and collapsed (the anti-firehose intent of DEC-035 #1, preserved).
3. **Raises** exactly one developer-facing mid-flight surface — a single decision card / pause-ask — carrying **what changed, why it matters, and the supporting evidence inline** (the D5 self-sufficiency floor: the developer can decide without going to fetch context).
4. **Resolves** the developer's answer into one of three outcomes — **proceed / change / abort-that-branch** — and resumes the build accordingly.

This is the **shared primitive**. Both `conduct-build-phase-frontier` (the in-flight build leg) and `conduct-merge-and-conflict-resolution` (the merge leg) call into this engine for mid-flight escalation. The engine owns detection-of-the-bar and the pause primitive; the callers do **not** re-implement detection — they defer to it.

It is distinct from three neighbors it must not be confused with:
- the **terminal end-gate** (the single human gate at the close of the run — a different surface);
- the **stakes finding-class schema field** itself (built by `directed-fix-finding-schema` — this engine consumes that field, it does not define it);
- the **anti-rubber-stamp forcing function** (DEC-036 D4, which lives in the report and end-gate, not here).

**Pain context:** Every leg of the DEC-036 impact mapping points at this engine, yet none of the other breakdown stories builds it. Without it, DEC-036 D1 tier (b) is asserted in the schema but never realized in control flow — the amendment to DEC-035 #1 would be unrepresentable in the Conductor's behavior. The new `escalated` disposition (raised, not silently fixed) would have nothing that produces it.

**Source decisions:** DEC-035 (adopt conduct; one human end-gate; auto-fix loop must be legible) and DEC-036 (narrow, high-bar, stakes-gated mid-flight escalation tier amending DEC-035 #1). The mid-flight bar **must stay narrow** (DEC-036 Decision Gate) — bias narrow; the end-gate-expanded tier (DEC-036 D1 tier a) is the safety net for everything that does not clear the bar.

## Acceptance Criteria

1. When a per-story pipeline / validation result is presented to the Conductor, the escalation engine reads both the stakes finding-class (one of: security/auth-isolation; irreversible/destructive; high-blast-radius/architecture; routine) and the timing tier (end-gate-expanded or mid-flight) off that result before deciding whether to escalate.
2. The engine raises a mid-flight pause-ask **only** when a finding's timing condition is **irreversible-and-imminent OR build-invalidating**. No other condition triggers a mid-flight pause.
3. Any finding that does NOT meet the irreversible-and-imminent-or-build-invalidating bar — including stakes-class findings whose timing is not imminent — stays on the autonomous path: it is handled silently and collapsed into the end-gate report, with no mid-flight interruption.
4. Routine-class findings are never escalated mid-flight; they remain always-auto-fixed and produce no developer-facing pause.
5. When the engine does fire, it raises exactly **one** developer-facing surface for that finding (a single decision card / pause-ask), not a stream of prompts — a single mid-flight interruption per qualifying finding.
6. The pause-ask surface carries, inline and self-sufficient: **what** the finding is (the change at stake), **why** it matters (the stakes class and the reason it is irreversible-and-imminent or build-invalidating), and the supporting **evidence** — such that the developer can decide without leaving the surface to fetch context.
7. The developer can resolve the pause-ask with one of exactly three outcomes: **proceed** (continue as planned), **change** (alter the planned action), or **abort-that-branch** (stop that line of work).
8. After the developer resolves the pause-ask, the build resumes according to the chosen outcome (proceeds, applies the change, or abandons that branch) — the run is not left hung, and no further mid-flight prompt is raised for that resolved finding.
9. A finding raised mid-flight is recorded with the **escalated** disposition (raised, not silently fixed), distinct from fixed, dismissed, and triaged-out.
10. The escalation engine is the single shared detection-and-pause primitive: the build-phase frontier leg and the merge/conflict-resolution leg both route mid-flight escalation decisions through it; neither leg independently decides the bar or owns its own pause primitive.
11. Over-escalation that re-creates a firehose is the explicit failure mode: across a representative build with many routine and non-imminent findings and only a small number of true irreversible-and-imminent-or-build-invalidating findings, the number of mid-flight pauses equals the number of bar-clearing findings and no more — the engine biases narrow, and end-gate-expanded handling absorbs the rest.

## Tasks / Subtasks

- [ ] Author `skills/momentum/skills/conductor/references/escalation.md` defining the escalation engine: its inputs (stakes finding-class, timing tier from a per-story result), the narrow bar (irreversible-and-imminent OR build-invalidating), the single-surface pause-ask, the three resolution outcomes, and the `escalated` disposition.
- [ ] In the reference, specify the **bar evaluation** rule explicitly: enumerate that ONLY irreversible-and-imminent OR build-invalidating fires; specify that all other findings (including non-imminent stakes-class findings) stay autonomous + collapsed; specify that routine never escalates mid-flight.
- [ ] In the reference, specify the **pause-ask surface contract** (D5 floor): the single decision card must carry what / why / evidence inline so the developer can decide without fetching context. Define the three resolution outcomes (proceed / change / abort-that-branch) and the resume behavior for each.
- [ ] In the reference, mark this engine as the **shared primitive**: document that build-phase-frontier and merge-and-conflict-resolution defer detection-of-the-bar and the pause primitive to this engine and do not re-implement them.
- [ ] In `skills/momentum/skills/conductor/workflow.md`, wire the escalation engine into the build loop: at the point where a per-story result is evaluated, invoke the bar check; on a bar-clearing finding, raise the single pause-ask and block until resolved; on resolution, apply proceed / change / abort-that-branch and continue.
- [ ] In `workflow.md`, ensure the merge/conflict leg routes its mid-flight escalation decisions through the same engine rather than prompting independently.
- [ ] In `workflow.md` and the reference, record the `escalated` disposition for any finding raised mid-flight, distinct from fixed / dismissed / triaged-out, so it is legible in the end-gate report.
- [ ] Add an explicit anti-firehose guard note in both files: bias narrow; everything that does not clear the bar flows to the end-gate-expanded tier (the safety net); the bar must never be widened beyond irreversible-and-imminent OR build-invalidating.
- [ ] Self-check the wiring against the ACs: confirm a routine-heavy / non-imminent-heavy run produces zero mid-flight pauses, and that only bar-clearing findings produce exactly one pause each.

## Dev Notes

This story implements the control-flow realization of DEC-036 D1 tier (b). The stakes finding-class field this engine reads is produced upstream by `directed-fix-finding-schema` (a dependency) — this engine **consumes** that field and the timing tier; it does not define the schema. The dependency on `conduct-skill-scaffold-and-spine` provides the Conductor skill structure (`skills/momentum/skills/conductor/`), and the dependency on `conduct-build-phase-frontier` provides the in-flight build leg that calls this engine.

Governing behaviors to fold in (from the conduct spec, cited by section number per the brief):
- DEC-036 **D1** — the two-tier timing model: tier (a) end-gate-expanded (default, the safety net) and tier (b) mid-flight (narrow). This engine is tier (b). The bar for tier (b) is **irreversible-and-imminent OR build-invalidating** and nothing else.
- DEC-036 **D2** — the stakes finding-classes the engine reads: security/auth-isolation; irreversible/destructive (migration, delete, force-push, prod deploy); high-blast-radius/architecture; and default routine.
- DEC-036 **D4** — the anti-rubber-stamp forcing function lives in the report/end-gate, NOT in this engine. This engine only contributes the `escalated` disposition into that downstream legibility; it does not implement the end-gate forcing function.
- DEC-036 **D5** — the self-sufficiency floor: every escalation surface carries what / why / evidence inline so the developer can decide in place.
- DEC-036 **Decision Gate** — the explicit failure mode is over-escalation re-creating the firehose that DEC-035 #1 was written to prevent. Bias narrow. Never widen the bar.

Disposition vocabulary the engine participates in: **fixed | dismissed (requires non-empty rationale) | triaged-out | escalated**. This engine is the sole producer of `escalated` (raised, not silently fixed). The `dismissed` and `triaged-out` dispositions are produced elsewhere on the autonomous path; `fixed` is the routine auto-fix outcome.

Boundary discipline (what this engine is NOT):
- Not the terminal end-gate (the single human gate at run close — a separate surface and separate story).
- Not the stakes finding-class schema field (built by `directed-fix-finding-schema`).
- Not the anti-rubber-stamp forcing function (DEC-036 D4, in the report/end-gate).

Shared-primitive contract: `conduct-build-phase-frontier` and `conduct-merge-and-conflict-resolution` both call this engine for mid-flight escalation. Detection-of-the-bar and the pause primitive live here once; callers defer. Do not let either caller grow its own parallel bar logic or its own pause prompt — that would fragment the narrow bar and risk widening it.

Touches:
- `skills/momentum/skills/conductor/workflow.md` — wire the bar check, the single pause-ask, the block-until-resolved, and the three resolution branches into the build loop; route the merge leg through the same engine.
- `skills/momentum/skills/conductor/references/escalation.md` — the engine's behavioral specification (inputs, bar, single-surface pause-ask, resolution outcomes, escalated disposition, anti-firehose guard).

### References

- Epic: **momentum-sprint-orchestration** (`_bmad-output/planning-artifacts/epics.json`) — conduct is the in-session, per-story, autonomous-build, single-end-gate rewrite of sprint-dev; the Conductor owns the build phase, all git mutation, and the single human end-gate.
- Decision: **DEC-035** (`_bmad-output/planning-artifacts/decisions/`) — adopt conduct; ONE human gate at the end; no story-count cap; report organized by user-facing functionality; auto-fix loop must be legible (what it changed AND dismissed).
- Decision: **DEC-036** (`_bmad-output/planning-artifacts/decisions/dec-036-conduct-hitl-calibration-2026-06-01.md`) — narrowly amends DEC-035 #1 to permit a narrow, high-bar, stakes-gated mid-flight escalation tier; D1 (timing tiers), D2 (stakes classes), D4 (anti-rubber-stamp end-gate), D5 (self-sufficiency floor), Decision Gate (anti-firehose / never widen the bar).
- Source: AES-004 Finding 1-2; impact brief `.momentum/handoffs/conduct-dec036-impact-brief-2026-06-01.md` §3.
