---
name: retro
description: "Sprint retrospective — transcript audit engine (dynamic Workflow), story verification, findings document, and sprint closure."
model: claude-sonnet-4-6
effort: high
---

Follow the instructions in ./workflow.md

Phase 4 (the transcript audit) runs as a single dynamic-Workflow call — the orchestrator invokes the Workflow tool once with `audit-workflow.js` (Discover → Verify → Synthesize), only after the Phase 2 zero-session guard passes. The Workflow runs in the background and returns once; it performs no human-in-the-loop, so all developer gates stay in `workflow.md`.

## Presentation Standard

All developer-facing output produced by this skill is governed by the
**Decision-Grade Presentation Standard** (`skills/momentum/references/rules/decision-grade-presentation.md`).

**Named surface caps that apply here:**

| Surface | Cap |
|---|---|
| Findings digest (Phase 4-5 — surfaced to developer for stub approval) | ≤ 7 actionable findings surfaced; routine findings collapsed to a count |

**Floor (non-negotiable):** Every finding the developer must approve as a story stub carries **what / why-it-matters / evidence inline** on the approval surface. A finding presented without its what/why/evidence is a defect.

**Caps-vs-floor:** Routine findings are collapsed to a count. Actionable findings (requiring developer approval) keep their full what/why/evidence. When the findings list is long, collapse more routine items — do not thin the actionable ones.

`effort: high` means more thorough transcript analysis. It does not earn a longer findings digest.
