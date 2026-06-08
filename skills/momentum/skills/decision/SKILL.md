---
name: decision
description: "Capture strategic decisions from assessments or research. Walk findings, record adopt/reject/defer, write a linked SDR document."
model: claude-opus-4-7
effort: high
---

# momentum:decision

Decision recorder — not deliberator. The thinking already happened. This skill captures
what was decided, links it to source material, and bridges to story creation.

Follow the instructions in ./workflow.md.

## Presentation Standard

All developer-facing output produced by this skill is governed by the
**Decision-Grade Presentation Standard** (`skills/momentum/references/rules/decision-grade-presentation.md`).

**Named surface caps that apply here:**

| Surface | Cap |
|---|---|
| Decision card (Step 2 — each adopt/reject/defer presentation) | ≤ 5 lines of prose + ≤ 3 supporting bullets; headline + verdict first |

**Floor (non-negotiable):** Every decision item carries **what / why-it-matters / evidence inline** on the presentation surface. The developer must be able to decide without opening the source document. A missing field is a defect.

**Ordering:** The headline (what is being decided) leads. Verdict and rationale follow. Background context is last.

**Caps-vs-floor:** Caps trim routine context and background. They never trim what/why/evidence for the decision item.

`effort: high` means more thorough capture. It does not earn longer per-decision presentation.
