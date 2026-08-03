---
title: Conduct resume card + Impetus pending-gate agenda — session-start re-surfacing, never expiry-FAIL
story_key: conduct-resume-card-impetus-pending-gate-agenda-session
status: ready-for-dev
epic_slug: momentum-conductor-core
feature_slug:
story_type: practice
priority: high
depends_on: []
touches:
  - skills/momentum/skills/conductor/workflow.md
  - skills/momentum/skills/conductor/references/resume-card.md
  - skills/momentum/skills/conductor/evals/
  - .claude/rules/impetus.md
  - skills/momentum/skills/impetus/SKILL.md
  - skills/momentum/skills/impetus/evals/
change_type:
  - skill-instruction
  - rule-hook
verification_method_advisory: skill-invoke
---

# Conduct resume card + Impetus pending-gate agenda — session-start re-surfacing, never expiry-FAIL

## Story

As a developer,
I want the Conductor to emit a compact resume card when a build finishes or is interrupted, and Impetus to lead the next session with the pending gate as the agenda — re-surfacing with rising prominence until decided, never expiring to a FAIL state,
so that a nights-and-weekends practice never leaves me facing a wall of text or a decision that silently expired while I was away.

## Description

A conduct build currently ends by rendering a large end-gate HTML report and asking for approval in the same turn. If the developer walks away at that moment — which this practice's work pattern makes routine — nothing durable says a decision is waiting. The next session starts cold, and the only way back in is re-reading the whole report.

This story closes that loop with two halves of one seam:

**Producer (Conductor).** At every phase checkpoint the run already records, and again when the end-gate is presented, the Conductor writes a small durable **resume card** next to the build ledger: where the run got to, what merged, what is blocked, and the single question that is pending. The card survives session death because it is a file, not context.

**Consumer (Impetus).** At session start — whenever that happens, minutes or weeks later — Impetus reads pending cards as part of the single cheap-state call it already makes, and leads the greeting with the pending question. Every re-surfacing raises prominence by one line stating how long the decision has waited; the card itself never grows longer, and nothing ever marks it failed or expired.

The card's shape is an explicit **seam contract** with a Canonical Output Shape, so producer and consumer cannot drift into incompatible halves of the same handoff — the failure mode already observed on `directed-fix-invocation-contract` (nested `escalation.timing_tier` vs flat `F.timing_tier` made a routing branch unreachable).

**Pain context:** Steve, verbatim: "Sadly this is not an 8 hour/day job for me. It's nights and weekends… when I finally get back I need to be reminded where we were… We must do better than massive walls of text that lead to complete demoralization and procrastination." The sprint-2026-07-13 gate hung undecided 11 days; the corpus's unexplained 7–18-day calendar gaps were demoralized withdrawal, which makes gate ergonomics a delivery mechanism, not a nicety.

**Rejected alternative (do not reintroduce):** DEC-040 D5 explicitly rejected the researched 48-hour gate expiry that escalates to FAIL. A gate here may legitimately wait days. Escalation is re-surfacing, never automatic failure.

## Acceptance Criteria

1. When a conduct run presents its end-gate, a resume card exists on disk at `.momentum/sprints/{sprint_slug}/resume-card.json` with status `pending`, written before or at the moment the gate is shown — so the card is already durable if the session dies with the gate on screen.

2. The card states where the run got to (the phase it reached), what merged (a count plus the story slugs), what is blocked (a count plus slugs), and exactly one pending question — never two — stating what the question gates, with the answers available for it and a path to the end-gate report for depth. A card carrying more than one pending question, or a question that does not say what it gates, is a defect.

3. The card is refreshed at each phase checkpoint the run already records and at each story-terminal merge inside the build phase, so a run interrupted anywhere — including mid-build between stories — leaves a card describing the last completed story or phase whose one pending question is to resume the build, not a gate decision.

4. The resume-card schema is written as a seam contract at `skills/momentum/skills/conductor/references/resume-card.md` containing a Canonical Output Shape section that shows the exact JSON nesting, and defining every field with who writes it, who reads it, and when it is set.

5. Both sides cite that contract as their source of shape: the Conductor's emit sites and the Impetus consumer surfaces reference it rather than restating the schema, so a field can only change in one place.

6. Impetus finds a pending card by looking across the sprint state directories in one pass and keeping the cards whose status is pending — folded into the single cheap-state call it already makes at session start, so startup gains no additional round trip. The lookup does not depend on a sprint being marked active, because a gate can be pending on a sprint that never closed.

7. When a pending card exists, Impetus leads the session with it: the pending question is the first thing in the situational report, ahead of sprint summary, ledger counts, and handoffs. If more than one card is pending, the most recently emitted one leads and the others are named in a single count line rather than expanded.

8. The surfaced card stays within its presentation budget: a lead of at most two sentences, merged and blocked work given as count lines rather than enumerated, exactly one question with its options, and the end-gate report linked rather than inlined. A wall-of-text resume card is a defect, not a long-but-acceptable surface.

9. Each time Impetus surfaces the same still-pending card, the card's re-surface counter increases and the surface gains one line stating how long the decision has waited and across how many sessions. Prominence rises through that line alone — the card's total length does not grow with repetition.

10. No elapsed time, re-surface count, or session count ever changes a card's status to failed, expired, or auto-resolved: a card surfaced across repeated sessions is observed still `pending` until a developer decision resolves it. (Review note, not a behavioral criterion: the implementation must also contain no code path that produces a failed/expired/auto-resolved status — verified by source review at QA, since instruction text is this change type's product.)

11. When the developer resolves the gate, the Conductor marks the card resolved with the timestamp and the resolution recorded, and Impetus stops surfacing it from the next session onward.

12. When no pending card exists, the session greeting behaves exactly as it does today — the pending-gate agenda adds nothing to a clean start.

## Tasks / Subtasks

- [ ] **Task 1 — Write the EDD evals before any skill edit** (AC 1, 2, 7, 9, 10)
  - Eval A: a conduct run reaching the end-gate leaves a `pending` card with one question.
  - Eval B: a session start with a pending card present leads with that question.
  - Eval C: a card surfaced three times never leaves `pending` and never gains a failed/expired status.

- [ ] **Task 2 — Author the resume-card seam contract** (AC 2, 4, 10)
  - Create `skills/momentum/skills/conductor/references/resume-card.md`.
  - Include a **Canonical Output Shape** block with exact JSON nesting for the whole card.
  - Define each field with writer, reader, and set-time. Define the correlation key (`sprint_slug`) with its assigner, uniqueness scope, and lifetime.
  - State the anti-expiry invariant as a contract-level rule, not an implementation note: `status` has exactly two values — pending and resolved — and no time-based transition between them exists.
  - Declare the re-surface counter and the waited-since timestamp as the contract's only shared-write fields — emitted by the Conductor, incremented/updated by Impetus on each surfacing, never touched by the Conductor after emit — with explicit write semantics. No other field may be writable by both sides.
  - Declare the presentation budget the rendered card must satisfy (AC 8) so both sides share one definition of "compact".

- [ ] **Task 3 — Conductor emits and refreshes the card** (AC 1, 3, 5)
  - In `skills/momentum/skills/conductor/workflow.md`, write the card at the phase checkpoints that already append phase-complete ledger rows AND on each `story-terminal` ledger row with outcome merged inside the Phase 2 build loop (the longest wall-clock window, and the most likely to be interrupted), and again in step 5 immediately before the end-gate report is opened — inside the RENDER-THEN-ASK atomic block, so no turn boundary can fall between gate render and card durability.
  - Source the card's contents from the build ledger (the authoritative Phase 5 source), not from in-context accumulators, so an interrupted-then-resumed run produces the same card.
  - Cite `references/resume-card.md` at each emit site instead of restating field names.

- [ ] **Task 4 — Conductor resolves the card** (AC 11)
  - On end-gate approval and on a completed request-changes cycle, set the card to resolved with timestamp and resolution.
  - Make the write idempotent: resolving an already-resolved card is a no-op, so a resumed session cannot double-write or regress the card to `pending`.

- [ ] **Task 5 — Impetus reads and leads with the pending card** (AC 6, 7, 8, 9, 12)
  - In `.claude/rules/impetus.md`, fold the pending-card lookup into the existing single session-start Bash call.
  - Make the pending question the first element of the situational report when a card is pending; leave the greeting untouched when none is.
  - On each surfacing, increment the re-surface counter and add the single waited-for line.
  - State the card's budget inline so the rule enforces it without opening another document.

- [ ] **Task 6 — Impetus skill surface declares the agenda item** (AC 7, 8)
  - In `skills/momentum/skills/impetus/SKILL.md`, add the pending-gate agenda to the Presentation Standard table as a named surface with its cap, and record that its floor (the one question, its options, the report link) survives the cap.

- [ ] **Task 7 — Two-sided seam check** (AC 5)
  - Verify every field the Conductor writes is a field Impetus reads, and every field Impetus reads is one the Conductor writes. Any orphan on either side is a finding, not a tolerated extra.
  - For the contract's declared shared-write fields (re-surface counter, waited-since), verify both sides' write semantics match the contract's declaration. Any field written by both sides without a shared-write declaration is a finding.

## Dev Notes

### Decision Authority

**DEC-040 D5** (`_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`) is the governing decision and **amends DEC-036** — implement the amendment, not the original. Its binding content:

- A gate never silently hangs and never greets the developer with a wall of text.
- When a conduct finishes it emits a resume card: where we were, what merged, the one question pending.
- Impetus leads the next session, whenever it happens, with that card as the agenda.
- Escalation is re-surfacing at every session start with rising prominence, **never automatic failure**.
- The researched 48h expiry-to-FAIL was **rejected as shaped**. Do not implement any expiry.
- Massive walls of text on any gate surface are a defect under the Decision-Grade Presentation Standard.

The sprint goal — "A sprint can no longer claim done without a human seeing it work" — makes this story the ergonomics half: the human has to be able to *get back to* the gate cheaply, or the gate is theatre.

### Current State of Affected Files

**`skills/momentum/skills/conductor/workflow.md`** (2924 lines — large-file protocol applies; never full-read, navigate by step anchors):
- Step 5 (end-gate) begins at line 2481. It assembles report variables from the build ledger, writes `.momentum/handoffs/{sprint_slug}-endgate-report.html`, opens it in the cmux viewer, then asks for approval.
- Line 2591 carries a `RENDER-THEN-ASK IS ATOMIC` critical: the turn must not end between opening the report and asking for approval. The card write belongs inside this atomic block — that is precisely the window where a developer walks away.
- Step 2.0 (~line 484) defines the PHASE CHECKPOINT RULE and the phase-complete ledger events (`avfl-on-merge-complete`, `e2e-phase-complete`, `end-gate-phase-complete`). Task 3 hooks these plus the per-story `story-terminal` (outcome: merged) rows inside Phase 2 — no new checkpoint mechanism is needed, but the refresh cadence is per-story during the build, not only at phase boundaries, because Phase 2 is the longest phase and the most likely interruption window.
- Line 2486 establishes the ledger as authoritative for end-gate assembly because in-context accumulators do not survive session death. The card must follow the same rule for the same reason.

**`skills/momentum/skills/conductor/references/build-ledger.md`**: the durable per-sprint state lives at `.momentum/sprints/{sprint_slug}/build-ledger.jsonl`. The resume card is a sibling of that file by design — same directory, same survival guarantee, and the sprint slug is already the correlation key there.

**`.claude/rules/impetus.md`**: the always-on Impetus persona. Its "Session-start behavior" section mandates **one** Bash call gathering cheap state (sprint summary, ledger counts, stale-close, three most recent handoffs), then a 1–2 sentence situational report, then yield. The card lookup folds into that one call; adding a second call would violate the rule and regress startup latency.

**`skills/momentum/skills/impetus/SKILL.md`** (80 lines): lines 61–76 hold the Presentation Standard section, with a named-surface cap table and an explicit caps-vs-floor paragraph. The pending-gate agenda is a new row in that table, written in the same shape.

### Architecture Compliance

- **Decision-Grade Presentation Standard** (`skills/momentum/references/rules/decision-grade-presentation.md`) governs both surfaces. The caps are: exec-summary-first (the question leads), ≤7 bullets, routine collapsed to count lines. The floor is what/why/evidence inline on the decision — here: the question (what), what it gates (why), and the merged/blocked state plus report link (evidence). Caps never trim the floor; if the two collide, the floor wins and the card runs long rather than incomplete.
- **Seam-contract convention** (`contract-seam-stories-two-sided-review-scope`): a contract between two agents declares both sides as review scope, carries a Canonical Output Shape with exact nesting, and defines correlation keys with assigner, uniqueness scope, and lifetime. Task 7 is the two-sided check that convention requires.
- **Single end-gate invariant** (DEC-035 D1, conductor workflow line 2481): the resume card is not a new gate and adds no new human touchpoint. It is a durable pointer *back to* the one gate that already exists. Do not let it grow into a second acceptance surface.
- **One-Bash-call rule** (`.claude/rules/impetus.md`): the consumer read is additive to the existing call, never a new one.

### Coordination — sibling story in this same sprint

`impetus-session-greeting-leads-with-n-of-m-feature` edits the same greeting surface in the same sprint, adding the N-of-M feature-conditions headline. The boundary: **this story owns the pending-gate agenda item and the card read**; that story owns the headline number. Both land in the same section of `.claude/rules/impetus.md` and `skills/momentum/skills/impetus/SKILL.md`. Whichever merges second must preserve the other's addition rather than overwrite the section — when a pending card exists it leads, and the N-of-M headline follows it. No `depends_on` edge is declared; this is a merge-sequencing note for the Conductor, not a build-order constraint.

### Testing Requirements

Verification method: **`skill-invoke`** (routed from `skill-instruction` per `skills/momentum/references/rules/verification-standard.md` §1). This story classifies as `skill-instruction` + `rule-hook`, which route to `skill-invoke` and `behavioral-trigger` respectively; `skill-invoke` is selected as the governing method because the story's primary deliverable is the Conductor's emit behavior and its seam contract. The Impetus consumer half is still exercised behaviorally — a session start with a pending card present must be observed leading with it, not merely inspected in the rule text.

Per the skill-instruction change type, EDD applies: the three evals in Task 1 are written and failing before any skill file is edited. Verification is by invocation and observation, never by reading the diff and concluding the instruction "looks right". The anti-expiry AC (10) is verified by absence — confirm no code path produces a failed/expired status, and that a thrice-surfaced card is still `pending`.

### Project Context Reference

This is skill-instruction and rule work inside the Momentum practice repo itself. No application code, no UI, no database. The deliverables are: one new reference document, edits to one large skill workflow, edits to one always-on rule, and one small skill surface addition.

### References

- Source decision: DEC-040 D5 — `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md` (amending DEC-036)
- Triage source: `decision:DEC-040`
- Producer surface: `skills/momentum/skills/conductor/workflow.md` step 5 (line 2481) and the phase-checkpoint rule (step 2.0)
- Durable state convention: `skills/momentum/skills/conductor/references/build-ledger.md`
- Consumer surfaces: `.claude/rules/impetus.md` (session-start behavior), `skills/momentum/skills/impetus/SKILL.md` (Presentation Standard)
- Presentation governance: `skills/momentum/references/rules/decision-grade-presentation.md`
- Verification routing: `skills/momentum/references/rules/verification-standard.md` §1
- Seam-contract convention: `.momentum/stories/contract-seam-stories-two-sided-review-scope.md`
- Sibling surface owner: `.momentum/stories/impetus-session-greeting-leads-with-n-of-m-feature.md`
- Epic context: `momentum-conductor-core` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 6 → `skill-instruction` (EDD)
- Task 5 → `rule-hook` (functional verification)
- Task 7 → `skill-instruction` (EDD — two-sided seam check)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md, workflow.md, or references/ files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply.

**Before writing a single line of skill instruction:**

1. Write the three evals named in Task 1 as behavioral scenarios: an input condition, an invocation, and an observable outcome.
2. Run them against the current skills and watch them fail. A failing eval that fails for the wrong reason is not a baseline.
3. Only then edit `skills/momentum/skills/conductor/workflow.md`, `references/resume-card.md`, and `skills/momentum/skills/impetus/SKILL.md`.
4. Re-run the evals. Green by invocation, not by inspection.

**Large-file protocol for `workflow.md` (2924 lines):** navigate by step anchors and grep; never full-read the file and never rewrite it wholesale. Edits are surgical insertions at step 2.0's checkpoint rule and inside step 5's atomic render-then-ask block.

**NFR compliance for skill-instruction work:**
- `SKILL.md` description stays ≤150 characters; frontmatter keeps its `model`/`effort` fields.
- New reference documents are self-sufficient — `resume-card.md` must be usable by an agent that has loaded only that file.
- Do not restate the schema in `workflow.md` or the Impetus surfaces; cite the contract. Duplicated schema is the drift this story exists to prevent.

### rule-hook Tasks: Functional Verification

`.claude/rules/impetus.md` is an always-on rule, not a script. Verify it by creating the trigger condition and observing the behavior:

1. Place a `pending` resume card in a sprint directory.
2. Start a fresh session and observe that the greeting leads with the pending question.
3. Repeat twice more and observe the waited-for line appear and its counts rise, while the card's status stays `pending` and the surface does not lengthen.
4. Remove the card, start a fresh session, and observe the greeting is unchanged from baseline (AC 12).

The rule change must not add a second Bash call at session start — check the session-start behavior section still mandates one, and that the card lookup lives inside it.

### Definition of Done additions for this story

- All three EDD evals pass by invocation.
- The seam contract exists and both sides cite it; no field is defined twice.
- Task 7's two-sided check reports zero orphan fields on either side.
- No expiry, timeout, or auto-fail path exists anywhere in the card lifecycle (AC 10 verified by absence).
- The rendered card was observed within its budget on a real surface, not just asserted in prose.

### Frozen verification contract

A frozen verification contract exists for this sprint at `.momentum/sprints/{sprint_slug}/specs/{story_slug}.{ext}`. Read the **Part-A header only** (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signaling done. Do not read the verifier body (Part B: scenarios, assertion scripts) beyond sections `how_dev_self_checks` explicitly names.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
