---
title: Stakes-classification rubric (shared, single source)
story_key: stakes-classification-rubric
status: backlog
epic_slug: momentum-sprint-orchestration
feature_slug:
story_type: feature
depends_on: []
touches: []
---

# Stakes-classification rubric (shared, single source)

<!-- INTAKE STUB: captured by momentum:intake. NOT dev-ready. DRAFT sections require
     full rewrite by create-story before development. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer,
I want one shared rubric that classifies findings into DEC-036's stakes classes and timing tiers,
so that every producer (the code-review adapter, qa-reviewer, AVFL) tags stakes consistently from a single source of truth rather than three divergent classifiers.

## Description

`directed-fix-finding-schema` adds the stakes finding-class FIELD; this story authors the LOGIC that populates it. Define the shared, referenceable rubric: the concrete signals/patterns that mark a finding as each of D1's three stakes classes (security/auth-isolation; irreversible/destructive — migration, delete, force-push, prod deploy; high-blast-radius/architecture), the timing-tier decision (mid-flight only for irreversible-and-imminent / build-invalidating; else end-gate-expanded), and the `routine` fall-through. Authored ONCE; consumed by every producer via small emission-wiring touches (the adapter sets it from bmad prose; qa-reviewer from AC/diff signal — folded into its rescope; AVFL on integration findings).

**Pain context:** Three legs (adapter, fixer, qa) independently proposed near-identical classifiers — this is ONE shared rubric consumed by N producers, NOT three units of work. AES-004 Finding 2 grades the heuristic itself "missing/unwired — no heuristic flags high-risk." Suggested dep (set at create-story): directed-fix-finding-schema. Source: DEC-036 D1+D2 / AES-004. Note: DEC-036's stakes classes ARE the long-missing `review_depth: deep` heuristic (spec open-Q5) — deep-review opt-in should become an OUTPUT of this rubric, not a hand-set flag.

## Acceptance Criteria

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- Defines concrete signals for each of the three stakes classes (security/auth-isolation; irreversible/destructive; high-blast-radius/architecture).
- Defines the timing-tier decision (mid-flight only for irreversible-and-imminent / build-invalidating; else end-gate-expanded) and the `routine` fall-through.
- Is authored once and referenced by every producer; producers get only small emission-wiring touches, not their own classifiers.
- Stays narrow on the mid-flight bar (consistent with the escalation mechanism).

> Note: rough captures only. Create-story will replace with validated, testable ACs.

## Tasks / Subtasks

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

_DRAFT — requires rewrite via create-story before this story is dev-ready._

Source decision: DEC-036 D1/D2; impact brief `.momentum/handoffs/conduct-dec036-impact-brief-2026-06-01.md` §3 (the de-dup note).
