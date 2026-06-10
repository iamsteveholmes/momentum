---
title: Conduct QA leg executes the story's verification method (smoke), not diff-only review
story_key: conduct-qa-execute-verification-method
status: backlog
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: defect
depends_on: []
touches: []
---

# Conduct QA leg executes the story's verification method (smoke), not diff-only review

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the conduct build phase's QA leg to actually execute each story's routed verification method — for `smoke` that means build + launch + drive on the live targets — instead of degrading to diff-only inspection,
so that "looks done in the diff but doesn't work live" defects are caught per-story during the build, not at the end-gate.

## Description

Root-caused from the nornspun campaign-init sprint (sprint-2026-05-30, conducted by hand
from the conduct RUNBOOK). All 15 stories passed per-story QA, yet the Phase-4 live
walkthrough found the headline feature functionally broken: the campaign-init conversation
was 100% client-local hardcoded copy that never called the backend. Per-story QA was
diff-inspection only — the app-ui code was never compiled or launched until Phase 4.

The decisive detail: the affected story specs **declared** `verification_method: smoke`
and even cited ASR-004 verbatim ("the acceptance signal is live on-device/desktop
observation, not scenario pass counts" — 57/71 scenarios "passed" while the live flow did
nothing). The routing existed; the conduct build phase did not honor it. The QA reviewer
verified the diff against the verification contract textually instead of executing the
contract's method.

Scope: the conductor skill's build-phase QA stage (and the qa-reviewer agent contract it
spawns) must route on the frozen contract's `verification_method` / `harness_profile` and
EXECUTE it — smoke stories get a real build+launch+drive pass (or a BLOCKED verdict if the
environment can't support one), never a silent downgrade to document/diff review.

**Pain context:** An entire 15-story sprint reached the end-gate "green" while its core
feature didn't work end-to-end; the failure class was already documented in ASR-004 and
named in the story specs, and the engine still skipped the antidote. Every conduct run
inherits this until fixed. Discovered during sprint-2026-05-30 root-cause analysis
(2026-06-10).

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

- The conduct build-phase QA stage reads the story's frozen contract Part-A header
  (`verification_method`, `harness_profile`) and routes execution on it — it never
  substitutes diff/document review for an executable method.
- For `smoke` stories, QA builds the app, launches it on the story's declared target(s),
  and drives the story's scenarios live; AC verdicts come from observed behavior.
- If the environment cannot support the routed method (no emulator, no backend), the QA
  verdict is BLOCKED with the missing prerequisite named — never PASSED-by-diff.
- A silent-downgrade guard: any QA result whose evidence is diff-only for an
  executable-method story is rejected by the conductor and the leg re-runs or escalates.
- The qa-reviewer agent contract states this explicitly (it already reads
  verification-harness routing — the gap is execution, not routing).

> Note: The ACs above are rough captures from conversation. They are starting points
> only. Create-story will replace them with validated, testable acceptance criteria.

## Tasks / Subtasks

<!-- DRAFT: No tasks have been analyzed or planned. This section MUST be populated by
     create-story, which will break down the work based on architecture analysis and
     implementation guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

<!-- DRAFT: Not yet populated. Run create-story to enrich with architecture analysis,
     implementation guide, technical requirements, and Momentum-specific guidance. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed. The following sub-sections are all stubs.

### Architecture Compliance

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Testing Requirements

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Implementation Guide

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### Project Structure Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

### References

- Origin: nornspun sprint-2026-05-30 root-cause analysis (build ledger
  `phase4_live.wiring_6_conclusive`; held finding #6) — campaign-init conversation
  client-faked, undetected by diff-only per-story QA.
- ASR-004 (nornspun): fixture-drift / scenario-pass-count failure class the story specs
  cited and the engine did not act on.

## Dev Agent Record

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
