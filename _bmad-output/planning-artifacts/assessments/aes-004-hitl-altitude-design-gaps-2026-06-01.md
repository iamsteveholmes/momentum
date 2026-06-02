---
id: AES-004
title: Momentum's HITL-Facing Design vs. the Decision-Altitude Research — Conduct Is Legible but Stakes-Blind
date: '2026-06-01'
status: current
method: 4-agent parallel discovery (conduct end-gate auditor, plan-gate legibility auditor, communication-altitude auditor, gate-placement & calibration auditor) grading actual artifact state against the HITL decision-altitude research at docs/research/hitl-oversight-altitude-2026-05-31
decisions_produced: [DEC-036]
---

# AES-004: Momentum's HITL-Facing Design vs. the Decision-Altitude Research — Conduct Is Legible but Stakes-Blind

## Purpose

This assessment grades Momentum's current human-in-the-loop (HITL) design surface — the Conduct end-gate, the plan/spec approval gates, and the prompt/template layer that talks to the developer — against the principles established in the decision-altitude research (`docs/research/hitl-oversight-altitude-2026-05-31`). It exists to find the concrete gaps between how Momentum gates and communicates with the human today and what the research says good HITL looks like, so those gaps can be resolved by decisions and encoded into the Conduct build and the practice's prompts/templates. It answers: is the human gate at the right altitude/grain? Do our HITL artifacts communicate decision-grade or firehose? Where are the gaps, and which are conduct-build-now vs. the deferred plan-gate epic vs. practice-wide?

## Method

Four discovery agents ran in parallel, each auditing actual artifact state (file paths + line references) and grading **Aligned / Partial / Misaligned / Missing** against the research as rubric:

- **Conduct end-gate auditor** — `sprint-dev-redesign-spec.md` §8–9, `conduct-report-template.html`, `conduct-skill-vs-code-flow-2026-05-31.html`, DEC-035 D5/D6.
- **Plan-gate legibility auditor** — sprint-planning, plan-audit (+ `.claude/rules/plan-audit.md`), canvas, create-story, DEC-031.
- **Communication-altitude auditor** — `.claude/rules/impetus.md`, the HTML report templates, conversational skill workflows, and a skills-tree grep for altitude controls.
- **Gate-placement & calibration auditor** — the full gate/HALT/ask/approval inventory across conduct + sprint-dev + git-discipline + AVFL.

Findings were validated with the developer one pass, who confirmed them and added two refinements now folded in: (1) stakes routing is **two-dimensional — what is raised AND when** (end-gate-expanded by default; a narrow, high-bar mid-flight tier for irreversible-and-imminent or build-invalidating cases); (2) the plan-gate gap (F5) is **knowingly deferred** per DEC-035 D7 — captured via intake for a future sprint, not reprioritized now.

### Headline

Momentum is overcorrecting on the axis the research says matters most. Today's `sprint-dev` is a 17-ask **firehose** (over-review); Conduct swings to a **single undifferentiated gate** (under-review). Conduct gets *legibility* right and *stakes-routing* wrong — neither model lands the calibrated middle the research prescribes.

---

## Finding 1: Conduct's end-gate is genuinely decision-grade on legibility & progressive disclosure — the win to build on

The report's progressive-disclosure and functionality-organization principles are faithfully realized.

| Component | Status | Evidence |
|---|---|---|
| Spine = user-facing functionality + divergences, not story dump | Aligned | DEC-035 D6 (dec-035…md:138-150); spec §9 (sprint-dev-redesign-spec.md:143-146) |
| Clean stories collapse to a line; divergences expand | Aligned | template collapses b2–b4+a4 into one row (conduct-report-template.html:251-260) |
| Decision-grade summary on top + detail-on-demand | Aligned | HERO metrics strip (template:170-198); options/trade-offs behind `<details>` (template:354-358; spec:694) |
| Per-section self-sufficiency mandate (no "see code") | Aligned | spec §9 CORE MANDATE (:685-700); data-layer enforces non-empty `what`/`why`/`evidence` (spec:792) |

Narrative: On the two axes the research calls decision-grade communication — progressive disclosure and organize-by-functionality — Conduct is strong and concrete. The HERO strip is a true decision-grade summary, detail lives behind disclosure, and the self-sufficiency mandate operationalizes "make the autonomous span legible, in full context." This is the foundation; the remaining findings are about what this legible surface fails to *route*.

---

## Finding 2: The end-gate is stakes-blind — the master gap

Security/irreversible findings get the identical treatment as a docstring typo. This hardwires the research's #1 real-world failure (under-review / automation bias) into the architecture.

| Component | Status | Evidence |
|---|---|---|
| Security/auth/irreversible finding **class** | Missing | "security / irreversible / migration / blast-radius" appear 0× in spec; XSS card rendered identically to a sort bug (template:302-313) |
| Auto-fix applied uniformly regardless of stakes | Misaligned | spec D1 "Legitimate issues are *always* fixed automatically" (:13); §03 "Nothing here needs a decision" (:268) |
| Irreversible sprint→main merge given line-by-line review | Misaligned | Conductor auto-resolves conflicts and retries, no human verify (spec §6:470-482) |
| Stakes-routing lever (`review_depth: deep`) | Missing/unwired | exists as a per-story opt-in (spec:215) but open Q5 admits no one sets it and no heuristic flags high-risk (spec:885) |

Narrative: The research's load-bearing claim is that oversight altitude is set by stakes — and that security/irreversible findings warrant line-by-line scrutiny *even when they pass happy-path tests*. Conduct does the opposite: every finding (including XSS) is auto-fixed, marked "no decision needed," and collapsed into a transparency stream sorted only by a generic severity chip. Severity-sorting is altitude-by-apparent-magnitude, not altitude-by-stakes — exactly the conflation the research warns against.

---

## Finding 3: The autonomous auto-fix loop is only half-legible — "dismissed" findings have no home

DEC-035 D5 mandates surfacing what the fixer changed *and dismissed*; only the changed half is built.

| Component | Status | Evidence |
|---|---|---|
| D5 mandate: surface changed AND dismissed, full context | (target) | dec-035…md:126-136 |
| Fixed findings surfaced legibly | Aligned | spec §03 (:728-730); template §03 cards (:273-328) |
| `dismissed` disposition exists in the fixer schema | Aligned | spec:264 |
| Dismissed findings have a section in the report | Missing | spec §03 covers only the fixed path (:717-741); template renders zero dismissed cards |

Narrative: A finding the fixer judged not-legitimate and dismissed — exactly the autonomous judgment D5 says must be surfaced — currently has nowhere to land. The precise failure mode D5 was written to prevent is left half-closed: the changed half is legible, the dismissed half is invisible.

---

## Finding 4: One uncapped gate + a pre-checked "Approve" is a structural rubber-stamp surface

The story-count cap is removed (D4), routing an unbounded feature through one terminal gate that defaults to approve.

| Component | Status | Evidence |
|---|---|---|
| Uncapped surface under one terminal gate | (context) | DEC-035 D4 (:114-124); spec §8 single gate (:587-591) |
| Forcing function on high-stakes items (acknowledge before approve) | Missing | absent from spec §8/§9 |
| Anti-theatre proxy (e.g., review-depth vs. cycle-time signal) | Missing | none adopted |
| Default-approve UI bias | Misaligned | end-gate radio pre-checks **Approve & finish** (template:450); decision cards pre-check the recommendation (template:360,377) — one-click rubber-stamp path |
| Ambiguous input defaults to `question`, never silent approve | Aligned (partial mitigation) | spec:632 |

Narrative: The research is pointed that the dominant real-world failure is rubber-stamping (38–61% of agent PRs merge unreviewed), and that a single gate over a large uncapped surface becomes oversight theatre unless attention is stakes-routed and a forcing function exists. Conduct has the uncapped surface and a pre-checked Approve, and none of the mitigations. Readability (Finding 1) is not a forcing function; the polished 15-second summary is the design that *maximizes* automation bias.

---

## Finding 5: The plan/spec gate is the most porous gate, and its fix is scoped-but-unbuilt — knowingly deferred

Plan/spec approval today forces line-by-line raw-artifact reading or offers a too-thin metadata summary. The legibility layer is fully scoped but unbuilt. **Per developer decision, this is deferred (consistent with DEC-035 D7) and captured via intake for a future sprint — not reprioritized.**

| Component | Status | Evidence |
|---|---|---|
| Per-story approval presents raw `.momentum/stories/{slug}.md` | Misaligned | sprint-planning/workflow.md:280-292 |
| Sprint-plan approval = slugs + counts (too thin to judge intent) | Misaligned | sprint-planning/workflow.md:910-944 |
| create-story UI ACs at implementation altitude | Misaligned | create-story/workflow.md:85-106 |
| `plan-audit` is decision-grade (Spec Impact + Go/No-Go) — but narrow | Aligned (narrow) | plan-audit/workflow.md:185-225; rule covers only ad-hoc plan-mode exits (.claude/rules/plan-audit.md:1-9) |
| DEC-031 D2 canvas Reviewer/attestation layer | Missing (backlog) | no reviewer route in canvas/server.tsx; `canvas-gate-review-surface-epic` = backlog |

Narrative: The practice has correctly diagnosed that its plan gate is porous (DEC-031 D1) and scoped the fix, but DEC-035 D7 deferred it in favor of execution automation. The known inversion tension — shipping more execution throughput while the highest-leverage gate stays illegible — is acknowledged and accepted. The resolution here is not to re-litigate sequencing but to ensure the plan-gate stories are intaken alongside the conduct stories so the work is captured for a future sprint.

---

## Finding 6: Communication altitude is left to the model's default everywhere live

Only the (unwired, cap-less) conduct HTML template demands decision-grade output; every live HITL surface relies on the model defaulting to terse — which the research proves is unsafe.

| Component | Status | Evidence |
|---|---|---|
| Conduct HTML template demands decision-grade shape | Partial | progressive disclosure present (template:154-159) but no measurable caps; self-sufficiency mandate pushes toward expansion (template:13-25); not wired to any skill |
| Live sprint-dev HITL surface | Misaligned | flat severity-grouped fix-queue dump, count placed after the dump, no summary/caps (sprint-dev/workflow.md:438-455) |
| Conversational skills enforce pacing but not altitude | Partial | one-at-a-time pacing (assessment:79; decision:16,94) but no exec-summary-first, no bullet/word caps for prose-to-human |
| Measurable caps / positive-concision / output schemas (live) | Missing | grep: zero "be concise / skip non-essential / word budget" across conversational skills |
| `effort:` used as the verbosity lever the research credits | Misaligned | `effort:` is a thinking-depth dial, set `high` on the very skills that talk to the developer (sprint-dev/SKILL.md:5, assessment:5, decision:5); no OpenAI `verbosity`/Gemini `thinkingLevel` anywhere |
| `retro` has a real word cap | Aligned (misplaced) | 500-word hard cap (retro/workflow.md:711-718) — but on a persisted file, not the live presentation |

Narrative: The capability and the patterns exist in-house (the conduct template's shape; retro's enforced cap; plan-audit's Go/No-Go) but are never applied to the live decision moment. The research's headline lever — measurable caps beat qualitative "be concise" — is absent from every surface the developer actually reads in-session. `effort` is the clearest case of a confirmed lever pointed the wrong way.

---

## Recommended Next Steps

1. **Define Conduct's stakes-and-timing escalation policy** — the escalation classes that raise HITL at all (security/auth-isolation, irreversible/destructive [migration, delete, force-push, prod deploy], high-blast-radius/architecture) × the two timing tiers (end-gate-expanded by default; a narrow, high-bar mid-flight tier for irreversible-and-imminent or build-invalidating cases); everything else stays autonomous and collapsed. This is the centerpiece — it resolves Finding 2 and operationalizes the developer's what-and-when refinement. Build-now.
2. **Add a stakes finding-class to the per-story + AVFL fixer schema, and hold stakes-class findings OUT of silent auto-fix** — security/irreversible findings become expanded end-gate decision cards (or mid-flight escalations if imminent), never "auto-fixed · no decision needed." Resolves Finding 2's auto-fix carve-out and part of Finding 3. Build-now.
3. **Render the `dismissed` disposition in the report** — add a "Dismissed / not-actioned (with rationale)" section so the fixer's waved-off judgments are visible, closing the second half of DEC-035 D5. Resolves Finding 3. Build-now.
4. **Add an anti-rubber-stamp forcing function to the end-gate** — drop the pre-checked Approve; when stakes-class items are present, require explicit per-card acknowledgment before Approve enables. Resolves Finding 4. Build-now (UI) + a standing-practice policy.
5. **Establish a practice-wide "decision-grade presentation" standard** — measurable caps (≤N bullets / word budgets), executive-summary-first, positive-concision phrasing, output schemas; plus a convention that `effort` drives work depth while explicit caps govern output verbosity. Apply to the conduct template and the live conversational skills. Resolves Finding 6. Practice-wide.
6. **Intake the plan-gate-legibility work for a future sprint — do not reprioritize** — capture the plan-gate stories alongside the conduct stories generated by these decisions; the plan-gate epic (DEC-031 D2 / DEC-035 D7) moves in a later sprint. Resolves Finding 5 without re-litigating sequencing.

---

## Raw Data

### Conduct end-gate auditor
TOP GAP: Conduct nails legibility and progressive disclosure but ignores the rubric's master axis — it flattens every finding (including security/irreversible ones) into a uniform "auto-fixed, no decision needed" stream and offers a one-click pre-checked Approve over an uncapped surface, so the single gate is stakes-blind and structurally primed for rubber-stamping. (Findings 1–4.)

### Plan-gate legibility auditor
TOP GAP: The DEC-031 D2 legibility layer (canvas Reviewer tab + attestation strip + sprint-planning plain-language per-story output) is fully scoped but entirely unbuilt (`canvas-gate-review-surface-epic` = backlog); today every plan/spec gate forces either line-by-line raw-artifact reading or a too-thin structural-metadata summary; `plan-audit` is the lone decision-grade surface and covers only ad-hoc plan-mode exits. (Finding 5.)

### Communication-altitude auditor
TOP GAP: The only surface that demands decision-grade output (the conduct HTML template) is unwired and cap-less, while every live HITL surface relies on the model defaulting to terse — which the research proves is unsafe; no live surface applies measurable caps, exec-summary-first, positive-concision, output schemas, or verbosity knobs; `effort:` is set `high` on the human-facing skills. (Finding 6.)

### Gate-placement & calibration auditor
TOP GAP: Conduct routes one review altitude over an uncapped feature with zero stakes axis — security/auth and irreversible-merge changes are auto-fixed and folded into the same approve-the-summary gate as docs, hardwiring the research's documented under-review/automation-bias failure into the architecture; only `git push` (via git-discipline) is correctly gated as irreversible. Current sprint-dev is the opposite failure (17 ask/HALT points = over-review firehose); the redesign should preserve the firehose collapse but add back stakes-escalation. (Findings 2, 4; headline.)
