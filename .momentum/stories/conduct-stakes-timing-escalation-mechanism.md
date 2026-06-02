---
title: Conduct stakes-and-timing mid-flight escalation mechanism
story_key: conduct-stakes-timing-escalation-mechanism
status: backlog
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
depends_on: []
touches: []
---

# Conduct stakes-and-timing mid-flight escalation mechanism

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want the Conductor to pause-ask-resume on a narrow, high-bar class of mid-flight findings,
so that irreversible-and-imminent or build-invalidating decisions are surfaced to me before they happen, while all routine work stays autonomous and collapsed.

## Description

The Conductor-side pause-ask-resume ENGINE for DEC-036 D1's mid-flight escalation tier. It is the new intermediate gate DEC-036 amends DEC-035 binding decision #1 to permit. It reads the stakes finding-class off a per-story pipeline or AVFL result, evaluates D1's narrow timing condition (irreversible-and-imminent OR build-invalidating) and fires ONLY on that bar, raises a single developer-facing mid-flight decision card carrying what/why/evidence inline (the D5 self-sufficiency floor), and on resolution resumes the build (proceed / change / abort-that-branch). Everything that does not hit the bar stays autonomous + collapsed (anti-firehose preserved).

This is the shared primitive that `conduct-build-phase-frontier` and `conduct-merge-and-conflict-resolution` both call. It is distinct from the terminal end-gate, from the stakes finding-class schema field (epic 02 / `directed-fix-finding-schema`), and from the anti-rubber-stamp forcing function (D4, report/end-gate). It exists in NONE of the current 52 breakdown stories.

**Pain context:** Every leg of the DEC-036 impact mapping points at this engine; none builds it. Without it, DEC-036 D1 tier (b) is asserted in the schema but never realized in control flow — the amendment to DEC-035 #1 is unrepresentable in code. Suggested deps (set at create-story): conduct-skill-scaffold-and-spine, conduct-build-phase-frontier, directed-fix-finding-schema. Consumed by: conduct-merge-and-conflict-resolution, conduct-preflight-halts (invariant carve-out). Source: DEC-036 D1 / AES-004 Finding 1-2. The mid-flight bar MUST stay narrow (DEC-036 Decision Gate) — bias narrow; D1 tier (a) end-gate-expanded is the safety net.

## Acceptance Criteria

<!-- DRAFT: rough ACs captured from conversation; rewrite via create-story. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Reads the stakes finding-class (DEC-036 D2) off a pipeline/AVFL result.
- Evaluates D1's high bar (irreversible-and-imminent OR build-invalidating) and fires ONLY on that bar; everything else stays autonomous + collapsed.
- Raises one developer-facing mid-flight decision card carrying what / why / evidence inline (D5 floor).
- On resolution, resumes the build: proceed / change / abort-that-branch.
- Is the single shared primitive invoked by the build-phase frontier and the merge/conflict path (they defer to it; they do not implement detection).
- The mid-flight bar stays narrow — over-escalation re-creating a firehose is the explicit failure mode to avoid.

> Note: rough captures only. Create-story will replace with validated, testable ACs.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

No technical analysis has been performed. Source decision: DEC-036 (`_bmad-output/planning-artifacts/decisions/dec-036-conduct-hitl-calibration-2026-06-01.md`); impact brief: `.momentum/handoffs/conduct-dec036-impact-brief-2026-06-01.md` §3.
