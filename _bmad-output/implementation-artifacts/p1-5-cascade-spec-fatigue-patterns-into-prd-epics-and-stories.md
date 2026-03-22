---
story_id: p1.5
status: in-progress
type: process
epic: P1 — Process Sprint-1
title: Cascade Spec Fatigue Patterns into PRD, Epics, and Stories
sprint: 1
touches:
  - _bmad-output/planning-artifacts/ux-design-specification.md
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/epics.md
  - _bmad-output/implementation-artifacts/2-1-impetus-skill-created-with-correct-persona-and-input-handling.md
  - _bmad-output/implementation-artifacts/2-2-session-orientation-and-thread-management.md
  - _bmad-output/implementation-artifacts/2-4-completion-signals-and-productive-waiting.md
depends_on: []
---

# Process Story p1.5: Cascade Spec Fatigue Patterns into PRD, Epics, and Stories

Status: ready-for-dev

## Story

As a Momentum developer,
I want spec fatigue mitigation patterns formally cascaded from the UX spec into PRD requirements, epic acceptance criteria, and ready-for-dev stories,
so that developers implementing Impetus stories have specification-level guidance on when and how to apply attention-aware checkpoints, expertise-adaptive orientation, motivated disclosure, and confidence-directed review.

## Background

The spec fatigue research (2026-03-21) produced 4 empirically-grounded mitigation patterns that were integrated into the UX design specification's "Spec Fatigue Mitigation Patterns" section. However, the cascade stopped there — the PRD has no FRs/NFRs referencing these patterns, the epics have no ACs requiring them, and the ready-for-dev stories (2.1–2.4) don't implement them. Without downstream traceability, developers have no specification mandate to apply these patterns.

## Acceptance Criteria

**AC1 — UX-DRs formalized:**
Given the UX design specification contains 4 spec fatigue mitigation patterns as prose guidelines,
When the UX Designer pass completes,
Then each pattern has a numbered UX-DR entry (UX-DR19–22 or next available) that downstream documents can reference.

**AC2 — PRD requirements updated:**
Given the UX-DRs are formalized,
When the PM pass updates the PRD,
Then FR8 references attention-aware checkpoints (UX-DR19) and confidence-directed review (UX-DR22),
And FR10 references expertise-adaptive orientation (UX-DR20) and motivated disclosure (UX-DR21),
And FR11 references motivated disclosure (UX-DR21),
And a new NFR18 (Review Sustainability) requires all workflow checkpoints to implement spec fatigue mitigation patterns.

**AC3 — Epic ACs added:**
Given the PRD requirements are updated,
When the PM pass updates the epics,
Then Stories 2.4, 2.5, 4.1, 4.3, and 6.3 each have new acceptance criteria referencing applicable UX-DRs.

**AC4 — Ready-for-dev stories updated:**
Given the epic ACs are added,
When the SM pass audits ready-for-dev stories,
Then Story 2.4 has new ACs, tasks, and evals for tiered review depth and confidence-directed findings,
And Stories 2.1 and 2.2 have dev notes explaining that spec fatigue patterns are established here and exercised downstream,
And Story 2.3 is audited but requires no changes (visual display, not a review checkpoint).

**AC5 — Verification:**
Given all three passes complete,
When grepping for UX-DR19 across planning and implementation artifacts,
Then matches appear in the UX spec, epics, and story 2.4,
And grepping for NFR18 in the PRD returns one match in a Review Sustainability section.

## Definition of Done

- [ ] `_bmad-output/planning-artifacts/ux-design-specification.md` — UX-DR19–22 added to requirements list
- [ ] `_bmad-output/planning-artifacts/prd.md` — FR8, FR10, FR11 updated; NFR18 added
- [ ] `_bmad-output/planning-artifacts/epics.md` — New ACs on Stories 2.4, 2.5, 4.1, 4.3, 6.3
- [ ] `_bmad-output/implementation-artifacts/2-1-impetus-skill-created-with-correct-persona-and-input-handling.md` — Dev note added re: spec fatigue foundation
- [ ] `_bmad-output/implementation-artifacts/2-2-session-orientation-and-thread-management.md` — Dev note added re: spec fatigue foundation
- [ ] `_bmad-output/implementation-artifacts/2-4-completion-signals-and-productive-waiting.md` — New ACs, tasks, evals for UX-DR19/22

## Dev Notes

**Change type:** docs-spec (specification cascade — all changes are additive to existing planning/implementation artifacts)

**Execution model:** Three sequential BMAD agent passes (UX Designer → PM → SM), each building on the prior's output. Commit after each pass.

**Scope constraint:** Only 4 patterns (Attention-Aware Checkpoints, Expertise-Adaptive Orientation, Motivated Disclosure, Confidence-Directed Review). Pattern 5 (Multi-Session Dashboard) is explicitly parked — do not formalize.

**Story scope constraint:** SM pass only touches ready-for-dev stories (2.1, 2.2, 2.3, 2.4). Backlog stories (4.1, 4.3, 6.3) receive epic-level ACs only — full story files created when promoted.
