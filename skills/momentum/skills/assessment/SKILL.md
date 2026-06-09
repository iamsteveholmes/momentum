---
name: assessment
description: "Guided product state evaluation. Spawns parallel discovery agents, validates findings with the developer, and produces a structured ASR document."
model: claude-sonnet-4-6
effort: high
---

# momentum:assessment

Collaborative product assessment — discover actual state, validate with the developer,
produce a durable ASR snapshot.

Follow the instructions in ./workflow.md.

## Presentation Standard

All developer-facing output produced by this skill is governed by the
**Decision-Grade Presentation Standard** (`skills/momentum/references/rules/decision-grade-presentation.md`).

**Named surface caps that apply here:**

| Surface | Cap |
|---|---|
| Finding card (Step 3 — each confirmed finding) | Lead-in ≤ 1 sentence; supporting detail follows; what/why/evidence inline (floor) |
| Recommendations / next steps (Step 4) | ≤ 5 items, each ≤ 2 sentences; specific and actionable |

**Floor (non-negotiable):** Every confirmed finding the developer must act on carries **what / why-it-matters / evidence inline** on the validation surface. A missing field is a defect.

**Caps-vs-floor:** Caps trim routine and clean material (collapse to a count). They never trim a decision-relevant what/why/evidence field. When budget pressure arises, trim the irrelevant; preserve the floor.

`effort: high` means deeper analysis. It does not earn a longer findings list or expanded presentation.
