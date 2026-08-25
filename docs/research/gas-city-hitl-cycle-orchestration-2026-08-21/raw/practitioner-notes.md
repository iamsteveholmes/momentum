---
content_origin: human
date: 2026-08-25
topic: "Gas City HITL gates and cycle orchestration for Momentum"
---

# Practitioner Q&A — Steve's verdicts (2026-08-25, decision gate)

Presented via visual decision gate (.momentum/handoffs/gas-city-decision-gate-2026-08-25.html) after full walkthrough.

## Fork 1 — Out-of-session goal (the DEC-035 revisit)
**Answer: Not yet — deferral stands.**
DEC-035's deferral of Gas City remains in force; this corpus files as the evidentiary baseline for any future revisit.

## Fork 2 — How an unattended cycle ends (push authority)
**Answer: Stop before push.**
Any future out-of-session cycle terminates at "merged locally, ready to push"; push remains a manual, approval-gated session action. No fifth gate, no rule change.

## Fork 3 — Residual empirical unknowns
**Answer: Ship with open items.**
The four unknowns (bd v1.2.2 CAS flags; notify-orders vs typed human gate; barrier failed-close semantics; multi-hour session survival) are recorded as open, becoming mandatory pre-adoption checks if Fork 1 ever flips.

## Developer requirement stated verbatim-in-substance (crucial, elevates a finding)
> "It needs better notifications. It's crucial we have back and forth and visibility with me (the HITL)."

Interpretation, confirmed in context: **rich notification and genuinely bidirectional developer interaction is a HARD requirement for any HITL orchestration Momentum runs** — with or without Gas City. Consequences for synthesis:
1. Gas City's silent-gate gap is not merely one of three gaps — it is **the disqualifying gap** for the out-of-session goal today. A gate that blocks but tells nobody fails the developer's core requirement even where the blocking mechanics are proven.
2. Any future revisit of Gas City (or alternative) must lead with the notification + verdict-return (back-and-forth) layer as the first thing proven, not the last thing built.
3. This requirement also reads onto Momentum's CURRENT in-session practice: the plan gate / results gate surfaces already meet it in-session; an out-of-session design must match that bar, not lower it.
