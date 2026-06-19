---
title: Visual HITL gates + presentation-form standard leg
story_key: visual-hitl-gates-presentation-form-standard-leg
status: backlog
epic_slug: momentum-impetus-experience
feature_slug:
story_type: practice
depends_on: []
touches: []
---

# Visual HITL gates + presentation-form standard leg

<!-- INTAKE STUB: This story was captured by momentum:intake. It is a conversational
     stub, NOT a dev-ready story. All sections below marked DRAFT require full rewrite
     by create-story before any development begins. -->

_This story is a backlog stub. Run `momentum:create-story` on it when ready to make it
dev-ready. Do NOT assign to a developer until create-story has enriched it._

## Story

As a developer (the practice owner),
I want Momentum's two highest-leverage human-in-the-loop gates — the pre-sprint plan review and the post-sprint results review — rendered as **visual, purpose-first decision surfaces** (not text walls), with a **presentation-form leg added to the decision-grade-presentation standard** so this is enforced by rule,
so that I can actually review, understand, and shape a sprint at the two moments where my judgment matters most, instead of rubber-stamping a wall of machine-grade spec.

## Description

This came out of a discovery + research session (run from the `nornspun` project, but the work belongs to the Momentum practice itself).

**The problem.** The two most important HITL intervention points are (1) the **pre-sprint plan review** (approve/redirect the sprint before agents build it) and (2) the **post-sprint review** (assess results + process). Both were failing the human:

- The pre-sprint review surface today is an **ad-hoc concatenation of full story specs** — for one 8-story app-shell sprint that was a **~37,500-word document** (18 H1 / 62 H2 / 96 H3 / 70 checkboxes). One story spec alone is ~2,800 words, of which only ~100 are decision-grade for the human; the rest is the **machine band** for the implementing agent (Tasks/Subtasks with file:line, Dev Notes, 17 sub-dp Design-Fidelity ACs, Implementation Guide, empty Dev Agent Record). That is a "log file, not a decision document."
- **There is no generating skill for the pre-sprint gate at all.** `sprint-planning` selects/specs/activates stories but emits no human go/no-go surface; the human reviews by opening whatever they open — an unmeasured, ad-hoc path.

**The reframe (verified).** Momentum already ships a `decision-grade-presentation.md` standard (v0.29.0) governing all human-facing output: effort-vs-verbosity orthogonality, ≤7-bullet caps, exec-summary-first, and a non-negotiable self-sufficiency floor (every decision-relevant item carries what / why-it-matters / evidence inline). The two HITL gates are **exactly the two surfaces missing a §2.2 per-surface budget row** (the standard itself calls an undeclared surface "a gap in this rule, not a silent exemption"). The post-sprint side is largely already built twice — `conduct` emits `endgate-report.html` (results + ship gate) and `retro`'s findings digest is already ≤7-capped — but results and process live in two separate moments.

**The deeper insight (the durable finding).** A content-trimmed Markdown gate was prototyped first; the developer's reaction was: _"It doesn't look neat or attractive, no visuals or diagrams, I have no idea after reading it for over a minute what it's trying to accomplish."_ This exposed that the standard governs **which information and what order** (caps + floor) but says **nothing about visual form / medium / purpose framing**. A skill can be fully compliant and still emit a correct, well-ordered **text wall**. The post-sprint gate only dodged this by happening to be authored as HTML. **Presentation form is a missing leg of the standard.** A second prototype — a designed HTML surface (purpose-first hero stating what the sprint accomplishes, an SVG dependency/wave diagram showing the critical-path hub, color-coded story + decision cards, sibling to `endgate-report.html`) — landed the point in seconds.

**Decisions already ratified in this conversation (honor them in create-story):**
- Pre-sprint gate is **emitted as the final step of `momentum:sprint-planning`** (it already holds the selected-story set + wave/dep graph — generation is a synthesis step, not a new pipeline).
- Gate fields (per-story stakes / one-line value / ★CALL-vs-✓batch verdict) are produced by **synthesis-now** — read and extract the fork callouts story authors already write — **deferring** a `stakes:`/`value_line:`/`delta:` frontmatter contract on `create-story` until the gate's shape proves out over 2-3 sprints.
- Post-sprint gate is **one fused results-first surface**: extend `conduct`'s `endgate-report.html` with a RESULTS-first lead and fold `retro`'s ≤7 process digest (Keep/Stop/Change) beneath it — not a third surface.
- Both gates **link to (never inline or edit) the canonical story `.md` files** so `momentum:dev` / `bmad-dev-story` keep their source-of-truth machine band intact.

**Provenance / artifacts:**
- Working prototype (validated on a real sprint): `~/projects/nornspun/.momentum/plan-gate-sprint-2026-06-18.html` (designed HTML) and `…/plan-gate-sprint-2026-06-18.md` (the earlier flat-prose version that drew the "text wall" critique).
- Parent it extends: the `decision-grade-presentation-standard` story (done) → `references/rules/decision-grade-presentation.md`.
- Post-sprint surfaces it aligns: `conduct-endgate-decision-card-rendering` (done) + `endgate-report.html`; `retro`'s findings digest (≤7, §2.2 row 6).
- Evidence base: Momentum research `spec-fatigue-research-2026-03-21.md` (+ `spec-fatigue-sections/`), `hitl-oversight-altitude-2026-05-31/`, `LLM Dual-Track Output Research Report.md`; external info-design (BLUF / Amazon-memo / NN-g scannability + progressive disclosure / automation-complacency).

**Pain context:** These two gates recur every sprint (pre and post) and are the highest-leverage points for human steering — so a presentation failure here costs the most. The lived failure: a ~37.5k-word concatenation that drives skim-then-rubber-stamp, and even a content-correct trimmed version that left the reviewer with "no idea what it's trying to accomplish" after a minute. ASR-004/006 separately document validators rubber-stamping real defects when overloaded. Forgetting risk: the durable insight — that **presentation form is a missing leg of the decision-grade standard**, distinct from content caps + the self-sufficiency floor — will be lost if not captured as work.

## Acceptance Criteria

<!-- DRAFT: These are rough acceptance criteria captured from conversation. They have NOT
     been refined, validated against architecture, or verified for completeness. This
     section MUST be fully rewritten by create-story before development. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

The following are rough draft ACs captured from conversation:

**A. Extend the decision-grade-presentation standard**
- [ ] Add two `§2.2` per-surface budget rows: **pre-sprint plan gate** and **post-sprint results gate** (close the two declared gaps).
- [ ] Add a third leg beyond caps + floor — **presentation form** — stating that decision gates render as **visual HTML surfaces**, lead with a **plain-language purpose** (what the work accomplishes), and **diagram the structure** (dependencies / waves / status) rather than describing it in prose. Treat it as non-overridable-at-lower-scope, alongside the caps-vs-floor boundary.
- [ ] Keep the standard self-sufficient (an agent loading only that file can apply the presentation-form leg).

**B. Build the pre-sprint plan gate (new surface)**
- [ ] `momentum:sprint-planning` emits a Layer-0 plan-gate surface as its final step (HTML, visual sibling of `endgate-report.html`).
- [ ] Purpose-first hero (what the sprint accomplishes, in plain language) + a dependency/wave diagram marking any single-point-of-failure story.
- [ ] A scannable story table (stakes · wave · dep · ★CALL/✓batch verdict); as-specified stories collapse to one line.
- [ ] A decision card per genuine fork only (what / why-it-matters / evidence / recommend, fully inlined — no bare handles); sign-off forces a written one-line reason per fork (anti-rubber-stamp).
- [ ] The gate **links to** the canonical story files; it never inlines or edits them; the machine band stays reachable for the dev agent.
- [ ] Generation is synthesis-now (extract existing story fork-callouts); no story-frontmatter contract required for v1.

**C. Align the post-sprint results gate (reconcile existing surfaces)**
- [ ] Extend `conduct`'s `endgate-report.html` with a RESULTS-first lead (per-story ship status; incompletes get a force-close/investigate card).
- [ ] Fold `retro`'s ≤7 process findings (Keep/Stop/Change) beneath results in the same gate; one gate, per-decision checkboxes. No third surface.

**D. Shared visual system**
- [ ] Both gates share one design family (warm parchment palette, pills, cards, SVG diagrams) consistent with `endgate-report.html`.
- [ ] Risk/stakes stratification and delta-framing ("what changed", not restating the unchanged) drive what gets the human's attention.

> Note: The ACs above are rough captures from conversation. They are starting points only.
> Create-story will replace them with validated, testable acceptance criteria. This story is
> sized like an epic-let — create-story should consider whether it splits into: (1) standard
> extension, (2) pre-sprint gate, (3) post-sprint gate alignment.

## Tasks / Subtasks

<!-- DRAFT: No tasks have been analyzed or planned. -->

_DRAFT — requires rewrite via create-story before this story is dev-ready._

- [ ] Tasks not yet defined — run create-story to analyze and plan implementation

## Dev Notes

<!-- DRAFT: Not yet populated. Run create-story to enrich. -->

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

_DRAFT — requires rewrite via create-story before this story is dev-ready._

(Provenance and ratified decisions captured inline in the Description above — create-story should formalize them here.)

## Dev Agent Record

<!-- DRAFT: Populated only during and after development. -->

_DRAFT — this section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
