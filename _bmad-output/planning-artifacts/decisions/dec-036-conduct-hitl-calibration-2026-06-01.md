---
id: DEC-036
title: Conduct HITL Calibration — Stakes-and-Timing Escalation, Legible Auto-Fix, Anti-Rubber-Stamp, and Decision-Grade Presentation
date: '2026-06-01'
status: decided
source_research:
  - path: _bmad-output/planning-artifacts/assessments/aes-004-hitl-altitude-design-gaps-2026-06-01.md
    type: assessment
    date: '2026-06-01'
  - path: docs/research/hitl-oversight-altitude-2026-05-31/final/hitl-oversight-altitude-2026-05-31.md
    type: prior-research
    date: '2026-05-31'
prior_decisions_reviewed:
  - DEC-035 (Conduct Execution Engine — its single-end-gate model is amended here)
  - DEC-031 (Legibility-Before-Automation — D2 plan-gate legibility reaffirmed as deferred)
  - DEC-030 (Dependency-Driven Execution — HITL-unit framing unchanged)
  - DEC-034 (Epic-Layer Consolidation — finite-lived epic remains the HITL unit)
architecture_decisions_affected:
  - DEC-035 — AMENDED — binding decision #1 ("No in-between HITL; every intermediate gate removed; legitimate issues always auto-fixed, no per-finding prompt") is relaxed for a narrow, high-bar, stakes-gated exception (D1+D2). DEC-035 D5 (auto-fix legibility) is extended to render dismissals (D3). DEC-035 D6 (functionality-spined report) is unchanged. The amendment preserves DEC-035's anti-firehose intent and amends only its absolutism — the conduct spec must be revised to design to the new exception.
  - DEC-031 D2 / DEC-035 D7 — REAFFIRMED — plan-gate legibility stays deferred (D6).
stories_affected:
  - canvas-gate-review-surface-epic
  - sprint-planning-pre-sprint-class-1-render-gate
  - epic-feature-collapse-closeable-grouping
---

# DEC-036: Conduct HITL Calibration — Stakes-and-Timing Escalation, Legible Auto-Fix, Anti-Rubber-Stamp, and Decision-Grade Presentation

## Summary

AES-004 graded Momentum's HITL-facing design against the decision-altitude research (`docs/research/hitl-oversight-altitude-2026-05-31`) and found Conduct **legible but stakes-blind**: its single end-gate gets progressive disclosure and functionality-organization right, but routes one undifferentiated altitude over an uncapped feature, auto-fixes security/irreversible findings identically to typos, renders only the "fixed" half of its auto-fix loop, and offers a one-click pre-checked approve. The net judgment: Momentum is overcorrecting from `sprint-dev`'s 17-ask **firehose** (over-review) to Conduct's **single undifferentiated gate** (under-review), missing the calibrated middle the research prescribes.

Six decisions were captured. Five are adopted and one adapted; none rejected; the plan-gate gap is knowingly deferred. The through-line: **don't remove HITL — remove the safely-handled decisions so the human isn't overwhelmed, while raising safety and review ability.** Conduct gates the human only for stakes classes (security/auth-isolation, irreversible/destructive, high-blast-radius/architecture), routed by *timing* (end-gate-expanded by default; a narrow, high-bar mid-flight tier for irreversible-and-imminent or build-invalidating cases); stakes-class findings leave the silent auto-fix path and become decision cards; the report renders dismissals; the approve control loses its default check and requires per-card acknowledgment of stakes items; and a practice-wide decision-grade presentation standard caps the irrelevant while guaranteeing decision context stays inline.

**This decision amends a binding decision of DEC-035** (see D1) — the single most consequential linkage, confirmed by discovery rather than asserted.

---

## Decisions

### D1: Define Conduct's stakes-and-timing escalation policy — ADOPTED

**Research recommended (AES-004 Rec 1):** Gate HITL only for stakes classes — security/auth-isolation, irreversible/destructive (migration, delete, force-push, prod deploy), high-blast-radius/architecture — across two timing tiers: end-gate-expanded by default, with a narrow, high-bar mid-flight tier reserved for irreversible-and-imminent or build-invalidating cases. Everything else stays autonomous and collapsed.

**Decision:** Adopted. This is the centerpiece. **Note: this amends DEC-035's binding decision #1** ("No in-between HITL; every intermediate approval gate is removed"). The mid-flight escalation tier is an intermediate gate — narrow and stakes-gated, but intermediate. The amendment is intent-preserving: DEC-035 decision #1 existed to kill the firehose (5 asks + 2 fix-loop asks + 8 HALTs + per-finding fix/defer prompts); a high-bar, stakes-only escalation does not reintroduce the firehose. DEC-035's *intent* (no routine asks) is preserved; its *absolutism* (literally zero intermediate gates) is relaxed. The conduct spec (§1 binding decisions, §8 gate model) must be revised to design to this exception.

**Rationale:** "We mustn't remove the HITL decision-making totally. The goal is to remove the safely-handled decisions so the HITL is not overwhelmed, while at the same time increasing our safety and review ability."

### D2: Add a stakes finding-class to the per-story + AVFL fixer schema; hold stakes-class findings OUT of silent auto-fix — ADOPTED

**Research recommended (AES-004 Rec 2):** Today every `legitimate: true` finding is auto-fixed and stamped "no decision needed," including security/XSS findings. Give security/irreversible findings a distinct class in the fixer schema and route them away from silent auto-fix — into expanded end-gate decision cards, or mid-flight escalations if they hit D1's bar.

**Decision:** Adopted. This also touches DEC-035 binding decision #1 ("legitimate issues are *always* fixed automatically — no per-finding fix/defer prompt"): stakes-class legitimate findings are now *raised* rather than silently fixed. The amendment is narrow — routine findings remain always-auto-fixed; only the stakes class is elevated.

**Rationale:** "This is an implementation of the higher-risk issues becoming elevated."

### D3: Render the `dismissed` disposition in the report — ADOPTED

**Research recommended (AES-004 Rec 3):** DEC-035 D5 mandates surfacing what the fixer changed *and dismissed*, but only the "changed" half is built. The fixer schema carries a `dismissed (with rationale)` disposition that the report never renders. Add a "Dismissed / not-actioned (with rationale)" section.

**Decision:** Adopted. Purely additive — it builds the unbuilt half of DEC-035 D5; no amendment.

**Rationale:** "This closes the loop for that sort of review" — seeing what the autonomous fixer waved off, not only what it changed.

### D4: Add an anti-rubber-stamp forcing function to the end-gate — ADOPTED

**Research recommended (AES-004 Rec 4):** The end-gate UI pre-checks Approve & finish and every recommendation — a one-click rubber-stamp over an uncapped surface. Drop the pre-checked Approve; when stakes-class items are present, require explicit per-card acknowledgment before Approve enables. Routine items still collapse and need nothing.

**Decision:** Adopted. Depends on D1/D2 — the forcing function is only as good as the stakes-classification feeding it.

**Rationale:** "For this to work we MUST surface the highest risks." The forcing function is meaningless unless the items it forces attention onto are correctly identified.

### D5: Establish a practice-wide "decision-grade presentation" standard — ADAPTED

**Research recommended (AES-004 Rec 5):** A standard for all human-facing output: measurable caps (≤N bullets / word budgets), executive-summary-first, positive-concision phrasing, output schemas; plus a convention that `effort` drives work depth while explicit caps govern output verbosity. Apply to the conduct template and the live conversational skills.

**Decision:** Adopted **with a self-sufficiency floor**. The caps cut *irrelevant* material (the Specification-Fatigue source) but never decision-relevant context. Every decision must carry its `what / why / evidence` **inline** — the human must never be sent to reference other material to make a call. This reconciles the conflict AES-004 Finding 6 flagged (Conduct's self-sufficiency mandate is good; its lack of a concision counterweight is the gap): the standard is **"tight on the irrelevant, complete on the decision-relevant."**

**Rationale:** "My rationale is all about what I've called 'Specification Fatigue' — spending your cognitive budget on irrelevant parts. But I'd also like to be sure we INCLUDE context for decisions, so we aren't expecting the user to reference other material." (Connects to the prior `spec-fatigue-research-2026-03-21` work.)

### D6: Intake the conduct-build stories now; keep plan-gate legibility deferred — ADOPTED

**Research recommended (AES-004 Rec 6):** The plan/spec gate is the most porous gate, but do not reprioritize planning ahead of Conduct (per DEC-035 D7). Capture the plan-gate-legibility work for a future sprint; prioritize the conduct-build stories now.

**Decision:** Adopted. Discovery confirmed the plan-gate work already exists as backlog stories (`canvas-gate-review-surface-epic`, `sprint-planning-pre-sprint-class-1-render-gate`, `epic-feature-collapse-closeable-grouping`) — so no new plan-gate intake is required; they stay deferred. The conduct-build stories (D1–D5) are new and will be intaken now.

**Rationale:** "We need both, but we have to start somewhere and don't want to lose our momentum on conduct."

---

## Reconciliation with DEC-035

DEC-035's binding decisions were declared "not up for relitigation." D1 and D2 amend binding decision #1, narrowly and intent-preservingly:

| DEC-035 binding decision #1 (as written) | DEC-036 amendment |
|---|---|
| "Every intermediate approval gate is removed." | Removed **except** a narrow, high-bar, stakes-gated mid-flight escalation tier (irreversible-and-imminent / build-invalidating only). |
| "Legitimate issues are *always* fixed automatically — no per-finding fix/defer prompt." | True for routine findings; **stakes-class** legitimate findings are raised as decision cards, not silently fixed. |
| Single end-gate, no in-between HITL. | Single end-gate remains the default surface; the mid-flight tier fires only on the stakes-and-timing bar. |

The anti-firehose intent (no routine asks, no per-finding prompts for ordinary work) is fully preserved. What changes is that *safety-critical, irreversible, or build-invalidating* judgments are no longer forced through a single terminal gate that the research shows trains rubber-stamping.

---

## Phased Implementation Plan

| Phase | Focus | Notes |
|---|---|---|
| 1 — Capture | Intake the five conduct-build stories (D1–D5) | New stories; plan-gate stories already in backlog and stay deferred (D6) |
| 2 — Spec revision | Revise the conduct spec (§1 binding decisions, §4 fixer schema, §8 gate model, §9 report) to design to D1–D5 | The spec currently designs to "zero intermediate gates"; it must absorb the stakes-and-timing exception |
| 3 — Build | Build the revised conduct with the stakes-and-timing policy, stakes finding-class, dismissed rendering, and anti-rubber-stamp gate | Per the conduct build order (DEC-035 Phase 2) |
| 4 — Practice-wide | Apply the decision-grade presentation standard (D5) to the conduct template and live skills | Separable from the conduct build; can proceed in parallel |

---

## Decision Gates

- **The stakes-and-timing bar (D1) is the load-bearing definition.** If the mid-flight tier's bar drifts wide in practice (re-introducing firehose), revisit — the bar must stay narrow (irreversible-and-imminent / build-invalidating only).
- **D4's forcing function depends on D1/D2 classification accuracy.** If stakes-classification has high false-negative rate, the forcing function gives false assurance — monitor in the first real conduct run.
