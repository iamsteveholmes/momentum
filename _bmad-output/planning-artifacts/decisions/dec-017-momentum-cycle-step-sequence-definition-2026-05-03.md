---
id: DEC-017
title: Momentum Practice Cycle — Formal Step Sequence Definition
date: '2026-05-03'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-03'
---

# DEC-017: Momentum Practice Cycle — Formal Step Sequence Definition

## Summary

The Momentum practice lacked a formally named end-to-end unit of work. This decision establishes "cycle" as the canonical term for the full flow from after one retro to the end of the next, and defines its ordered steps. The motivation is dashboard design: when the developer or an agent says "cycle," all parties need a shared, unambiguous referent. The definition is expected to inform Impetus orientation and any future dashboard artifacts that surface cycle state.

---

## Decisions

### D1: Momentum Cycle Definition — ADOPTED

**Developer framing:** Designing a dashboard requires consistent terminology. When Steve says "cycle," agents — particularly Impetus — must know exactly what that means: which steps are in scope, their order, and which are required vs. optional.

**Decision:** A Momentum **cycle** is defined as the full ordered sequence from after a retro to the end of the next retro:

```
triage → intake → feature-grooming → epic-grooming → refine → sprint-planning → sprint-dev → retro
```

Constraints:
- **Required steps:** sprint-planning, sprint-dev, retro
- **Optional steps:** triage, intake, feature-grooming, epic-grooming, refine
- **Distill** runs inside the retro (Phase 5) — it is not a standalone cycle step
- **upstream-fix** is a stub/planned capability — not a live cycle step and not part of the current cycle definition

**Rationale:**
Dashboard design requires that when Steve says "cycle" the agent understands the referent without ambiguity. Naming the unit and its steps makes it possible to surface cycle state, track progress through a cycle, and reason about where in the flow the practice currently sits. This definition is also expected to modify how Impetus orients the developer at session start — the greeting should map to cycle position, not just sprint state.
