---
title: "Companion surface — post-sprint results gate (conduct end-gate + retro digest, fused)"
story_key: companion-surface-post-sprint-results-gate
status: ready-for-dev
epic_slug: momentum-impetus-experience
feature_slug:
story_type: practice
priority: high
change_type:
  - skill-instruction
verification_method_advisory: skill-invoke
depends_on: []
touches:
  - skills/momentum/skills/conductor/
  - skills/momentum/skills/retro/
---

# Companion surface — post-sprint results gate (conduct end-gate + retro digest, fused)

## Story

As the developer (the practice owner),
I want the post-sprint review delivered as **one fused, results-first companion decision surface**
— `conduct`'s end-gate report extended with a RESULTS-first lead and `retro`'s ≤7 process digest
(Keep / Stop / Change) folded in beneath it —
so that results and process review live in a single moment instead of two disconnected surfaces.

## Description

The post-sprint results gate is the second of Momentum's two highest-leverage HITL gates, and the
decision-grade-presentation standard names it as a Companion-decision-surface instance
(§6 surface schema: "post-sprint results gate (`conduct` end-gate + `retro` digest, fused)").
The pieces largely exist but live in two separate moments: `conduct` emits
`{{sprint_slug}}-endgate-report.html` (results + ship gate) at the end of the build (Phase 5),
and `retro` later produces a flat-prose findings document (`retro-transcript-audit.md`) plus
interactive story-stub proposals. This story **reconciles them into one gate** — it is **not** a
third surface.

**The reframe.** The standard governs *which* information and *how much* (caps + self-sufficiency
floor) and — since the presentation-form leg (§5.1) — *what form* (visual HTML, purpose-first hero,
diagrammed/scannable structure, anti-rubber-stamp sign-off). The post-sprint side already dodged the
"text wall" failure by being authored as HTML, but it splits the human's post-sprint judgment across
two artifacts at two times. The fix is to fold `retro`'s process findings into the same HTML artifact
that already carries results, leading with ship status.

**Decisions already ratified (honored in these ACs):**
- Extend `conduct`'s `endgate-report.html` with a **RESULTS-first lead** — per-story ship status
  leads the surface; each incomplete / blocked / quarantined story surfaces a force-close-or-investigate
  decision card.
- **Fold `retro`'s ≤7 process findings** (Keep / Stop / Change) **beneath results in the same gate**;
  one HTML file, per-decision sign-off on both sections. No third surface.
- The presentation-form leg (§5.1) applies: visual HTML (sibling of `endgate-report.html`, shared
  design family + the `companion-decision-surface.html` skeleton), plain-language results-first hero,
  scannable per-story status, anti-rubber-stamp sign-off per genuine fork.
- Both halves **link to** (never inline or edit) their source artifacts — the build ledger, the
  canonical story `.md` files, and `retro-transcript-audit.md` — so `momentum:dev` / `bmad-dev-story`
  keep their machine band intact.

**Scope note.** This story is the post-sprint (Part C) decomposition of
`visual-hitl-gates-presentation-form-standard-leg`. The standard extension (Part A) is already
delivered; the pre-sprint plan gate (Part B) is a sibling story, not a dependency. This story does
**not** introduce a new file format — it extends the existing end-gate report and re-points `retro`'s
process output into it.

## Acceptance Criteria

1. **Results-first lead.** The fused gate's first content section (after the hero metrics strip)
   is a per-story **ship status** block: every sprint story is listed with an explicit outcome
   (`shipped-merged` / `blocked` / `closed-incomplete` / `quarantined`), and this block leads the
   surface ahead of the "What shipped" prose. (Renderer spec §3 section spine updated so the
   ship-status lead precedes §01.)
2. **Incomplete-story decision cards.** Every story that did not reach a shipped/merged outcome
   surfaces a **force-close-or-investigate** decision card in the decision section, each carrying
   what / why-it-matters / evidence inline and the two options (Force-close as `closed-incomplete`
   / Investigate) per the Pause-Ask template. A clean sprint (all stories merged) renders no such
   card.
3. **Retro process digest folded beneath, same artifact.** `retro`'s ≤7 process findings, organized
   as **Keep / Stop / Change**, render as a dedicated "Process review" section **beneath** the
   results sections in the **same** `{{sprint_slug}}-endgate-report.html` file — not a separate
   document.
4. **≤7 cap + self-sufficiency floor on process findings.** The Process review section surfaces at
   most 7 findings; routine findings collapse to a single count line ("N routine items …"); each
   surfaced finding carries **what / why-it-matters / evidence** inline.
5. **Anti-rubber-stamp sign-off across both sections.** The gate's approve control stays disabled
   until (a) each results decision card from AC2 is acknowledged and an option is picked, and
   (b) each surfaced process finding is answered with a per-decision response and a written one-line
   reason. A blanket "approve all" does not satisfy the gate. (Extends the existing §GATE / `paint()`
   forcing function to cover the process section.)
6. **Presentation-form leg (§5.1).** The fused gate is visual HTML — a sibling of
   `endgate-report.html` using the shared warm-parchment design family and the
   `companion-decision-surface.html` skeleton — leading with a plain-language **results-first purpose
   hero** and presenting per-story status scannably (status pills / strip), not as flat prose.
7. **Links, never inline or edit, source artifacts.** The gate references the build ledger, the
   canonical story `.md` files, and `retro-transcript-audit.md` as depth-on-demand links; it does
   not inline their full content and does not modify the story `.md` files during render.
8. **Single-surface invariant.** For a completed sprint, the post-sprint review emits **exactly one**
   human-facing decision surface (the extended `endgate-report.html`); `retro` no longer emits a
   separate parallel review surface for the same sprint — its process findings appear inside the
   fused gate.

## Tasks / Subtasks

- [ ] **Task 1 — Results-first lead + force-close cards in the renderer spec** (AC1, AC2, AC5a) → *skill-instruction*
  - [ ] Edit `skills/momentum/skills/conductor/references/endgate-report-renderer.md` §3 section spine:
        add a per-story **ship status** lead that precedes §01 (outcome per story:
        shipped-merged / blocked / closed-incomplete / quarantined), sourced from `{{build_log}}`,
        `{{blocked_stories}}`, `{{quarantined_stories}}`.
  - [ ] Specify the **force-close-or-investigate** decision card (§04) for every non-shipped story,
        following the §5 decision-card data contract (what / stakes / options A=Force-close,
        B=Investigate) and the Pause-Ask template; assert the clean-sprint (zero cards) path.
  - [ ] These force-close/investigate cards are standard §04 decision cards, so they inherit the
        **existing** §GATE `paint()` anti-rubber-stamp enforcement (approve blocked until each card is
        acknowledged and an option is picked) — this satisfies the results-card half of AC5 (AC5a).
        Task 2 extends `paint()` to additionally cover the process section (AC5b).
- [ ] **Task 2 — Folded process section + retro→gate data contract** (AC3, AC4, AC5) → *skill-instruction*
  - [ ] Add a "Process review (Keep / Stop / Change)" section to the renderer spec §3 spine,
        positioned **beneath** the results sections; define its data contract (a `{{process_findings}}`
        binding: ≤7 entries, each `{ disposition: keep|stop|change, what, why, evidence }`).
  - [ ] Wire `{{process_findings}}` assembly into `skills/momentum/skills/conductor/workflow.md`
        Phase 5 (or document the retro-owned render path per the Dev Notes design decision), and
        extend the §GATE `paint()` forcing function so approve is blocked until each process finding
        carries a per-decision response + written reason.
- [ ] **Task 3 — Retro emits the structured digest into the fused gate** (AC3, AC4, AC8) → *skill-instruction*
  - [ ] Update `skills/momentum/skills/retro/workflow.md` so its findings are emitted as a structured
        ≤7 **Keep / Stop / Change** digest, each item carrying what / why-it-matters / evidence
        (not only flat prose in `retro-transcript-audit.md`).
  - [ ] Fold that digest into the same `{{sprint_slug}}-endgate-report.html` artifact (the fused gate)
        rather than a separate review surface; establish the single-surface ownership/timing per the
        Dev Notes design decision.
- [ ] **Task 4 — Presentation-form leg + links + single-surface invariant** (AC5, AC6, AC7, AC8) → *skill-instruction*
  - [ ] In the renderer spec, require the fused surface to use the shared design family +
        `skills/momentum/references/templates/companion-decision-surface.html` skeleton, lead with a
        results-first purpose hero, and render per-story status as scannable pills/strip.
  - [ ] Require the gate to **link** (never inline/edit) the build ledger, story `.md` files, and
        `retro-transcript-audit.md`; assert the single-surface invariant (one HTML file per completed
        sprint).
- [ ] **Task 5 — EDD evals for the fused gate** (AC1–AC8) → *skill-instruction*
  - [ ] Write/extend behavioral evals under `skills/momentum/skills/conductor/evals/` and
        `skills/momentum/skills/retro/evals/` asserting: results-first lead present; force-close/
        investigate card for an incomplete story; retro ≤7 folded beneath in one file; anti-rubber-stamp
        across both sections; exactly one post-sprint surface emitted.

## Dev Notes

### Decision Authority

This story implements ratified decisions captured in the parent story
`visual-hitl-gates-presentation-form-standard-leg` (Part C) and is governed by the
**decision-grade-presentation standard** at
`skills/momentum/references/rules/decision-grade-presentation.md`:
- **§2.2 row 9** — Companion decision surface budget (lead with purpose; one ✓ line for verified
  mechanics; ≤7 genuine forks as What/Why/Evidence/Recommendation/Options cards; large doc linked
  as depth-on-demand; rendered as visual HTML).
- **§5** — Companion-Surface Obligation (the large record is depth-on-demand backing; the companion
  surface is what the human is handed).
- **§5.1** — Presentation-form leg (visual HTML, plain-language purpose hero, diagrammed/scannable
  structure, link-not-inline source artifacts, anti-rubber-stamp sign-off). Non-overridable at lower
  scope (§8).
- **§6** — names this exact surface: "post-sprint results gate (`conduct` end-gate + `retro` digest,
  fused)".

The what/why/evidence floor (§3) and the caps-vs-floor boundary (§4) are non-negotiable: the ≤7 cap
on process findings never trims a surfaced finding's what/why/evidence — collapse routine items to a
count line instead.

### Design decision to confirm at the approval gate (genuine fork)

**What.** `conduct` renders the end-gate at build-end (Phase 5); `retro` runs later as a separate
invocation. "One fused gate" requires choosing **who owns the fused render and when**.
**Why it matters.** It determines whether the two skills stay decoupled (each invoked on its own) or
become coupled at one moment, and which skill writes the final HTML.
**Evidence.** `conductor/workflow.md` Phase 5 builds `{{sprint_slug}}-endgate-report.html` from the
build ledger; `retro/workflow.md` Phase 1 independently discovers a completed sprint awaiting retro
and Phase 4 produces `retro-transcript-audit.md`.
**Recommendation (defaulted — confirm or override):** **`retro` owns the fused re-render.** `conduct`
continues to emit the results-first end-gate at build-end (the ship gate, unchanged ownership);
`retro` — which already has both the build outcomes and the ≤7 process findings — folds its
Keep/Stop/Change digest into the **same** `{{sprint_slug}}-endgate-report.html` file (one artifact,
progressively completed), preserving the single-surface invariant without coupling the two skills'
invocation. **Options:** A = retro owns the fused re-render (recommended); B = conduct holds the gate
open and invokes retro inline before render (couples invocation); C = shared template/path that retro
appends to. The ACs are written to be observable under any option (the outcome is one HTML surface,
results-first, retro ≤7 folded beneath).

### Current state of affected files

- `skills/momentum/skills/conductor/references/endgate-report-renderer.md` — defines the end-gate
  HTML data contract and §3 section spine (hero · §01 What shipped · §02 per-piece · §03 divergences ·
  §04 decisions · §05 waved-off · §06 honesty · §07 merge · §GATE). No results-first ship-status lead
  and no process-findings section today. The §5 decision-card contract and §GATE `paint()`
  anti-rubber-stamp forcing function already exist and are the extension points.
- `skills/momentum/skills/conductor/workflow.md` — Phase 5 assembles the report variables and renders
  the HTML; it already tracks blocked/quarantined stories and `closed-incomplete` terminal transitions
  at "Phase 5 approve."
- `skills/momentum/skills/retro/workflow.md` — Phase 3 verifies story completion (already offers
  per-incomplete-story Force-close / Investigate), Phase 4 produces `retro-transcript-audit.md` (flat
  prose), Phase 5 proposes story stubs interactively. There is no structured ≤7 Keep/Stop/Change
  digest and no HTML surface today — this is the principal new work.
- `skills/momentum/references/templates/companion-decision-surface.html` — the reusable skeleton
  (exists); the fused gate should build on it + the `endgate-report.html` design family.

### Architecture Compliance

- **No third surface.** This is an extension of `endgate-report.html` + a re-point of `retro`'s
  process output, never a new parallel artifact (AC8). The renderer spec defers format authority to
  `_bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md`; if the §3 spine of
  that canonical doc needs a matching results-first/process-section update for consistency, flag it as
  a follow-up — this story's edits stay within the two declared skill directories.
- **Sprint-state ownership unchanged.** Terminal `closed-incomplete` transitions remain owned by the
  existing Phase 5 approve / retro Phase 3 paths via `momentum-tools` — the fused gate surfaces the
  force-close decision; it does not bypass the state machine.
- **Self-contained HTML** (inline `<style>`/`<script>`, zero external deps), opened in the cmux viewer
  pane as a browser tab, per the renderer spec §8.

### Testing Requirements

- **Method:** `skill-invoke` (advisory; routing is derived from `change_type: skill-instruction` at
  sprint-planning time per `skills/momentum/references/rules/verification-standard.md` §1).
- **EDD, not TDD** — these are skill-instruction (SKILL.md/workflow.md/references) changes; verify by
  behavioral evals (Task 5), not unit tests. Confirm the observable gate behaviors (results-first lead,
  fused process section, ≤7 + floor, anti-rubber-stamp across both, single surface) by invoking the
  affected skills' instructions against a representative completed-sprint fixture.
- A frozen verification contract for this story will live at
  `sprints/{sprint-slug}/specs/companion-surface-post-sprint-results-gate.{ext}` once sprint-planning
  freezes it; the dev reads only the Part-A self-check header before signaling done.

### Project Context Reference

- Parent / provenance: `.momentum/stories/visual-hitl-gates-presentation-form-standard-leg.md` (Part C).
- Standard: `skills/momentum/references/rules/decision-grade-presentation.md` §2.2 row 9, §5, §5.1, §6.
- Existing surfaces: `endgate-report.html` (`conduct-endgate-decision-card-rendering`, done);
  `retro`'s findings digest (≤7, §2.2 row 6).

### References

- Renderer spec: `skills/momentum/skills/conductor/references/endgate-report-renderer.md`
- Format & voice authority: `_bmad-output/planning-artifacts/conduct-endgate-report-format-and-voice.md` (§9 decision-grade presentation; §3/§5 risk narrative)
- Companion-surface skeleton: `skills/momentum/references/templates/companion-decision-surface.html`
- Conductor end-gate render: `skills/momentum/skills/conductor/workflow.md` (Phase 5)
- Retro findings/closure: `skills/momentum/skills/retro/workflow.md` (Phases 3–6)
- Verification routing: `skills/momentum/references/rules/verification-standard.md` §1
- Epic context: `momentum-impetus-experience` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 5 → skill-instruction (EDD)

All work edits skill instruction files (`SKILL.md` / `workflow.md` / `references/`) under
`skills/momentum/skills/conductor/` and `skills/momentum/skills/retro/`. No deterministic
script/code, rule-hook, config, or app-UI tasks are present.

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md, workflow.md, or reference specs.** Skill instructions are
non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing changes:**
1. Write 2–3 behavioral evals (Task 5):
   - Renderer/end-gate behaviors → `skills/momentum/skills/conductor/evals/`
   - Retro-side digest behaviors → `skills/momentum/skills/retro/evals/`
   - One `.md` per eval, named descriptively (e.g.
     `eval-endgate-leads-with-per-story-ship-status.md`,
     `eval-retro-process-digest-folded-into-single-surface.md`).
   - Format: "Given [a completed sprint with N stories, M incomplete, plus retro process
     findings], the surface should [observable behavior]." Test behaviors and decisions, not
     exact output text.

**Then implement:** edit the renderer spec, conductor Phase 5, and retro workflow per Tasks 1–4.

**Then verify:** for each eval, spawn a subagent (Agent tool), give it the eval scenario and the
affected skill instructions as context (or invoke the skill via its Agent Skills name), and observe
whether behavior matches. Max 3 revise/re-run cycles; surface to the developer if still failing.

**NFR compliance — mandatory for every skill-instruction edit:**
- Any SKILL.md `description` touched must stay ≤150 characters (NFR1).
- `model:` and `effort:` frontmatter must remain present on touched SKILL.md files.
- Each touched SKILL.md body stays under 500 lines / 5000 tokens; overflow goes to `references/`
  with clear load instructions (NFR3). The conductor `workflow.md` is already large — prefer adding
  the data contract to `references/endgate-report-renderer.md` and keeping `workflow.md` edits to the
  binding/wiring, not prose expansion.
- Skill names keep the `momentum:` namespace prefix (NFR12).

**Additional DoD items (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written across `conductor/evals/` and `retro/evals/`.
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented).
- [ ] Touched SKILL.md descriptions ≤150 characters confirmed; `model:`/`effort:` present.
- [ ] Touched SKILL.md bodies ≤500 lines / 5000 tokens confirmed (overflow in `references/`).
- [ ] AVFL checkpoint on produced artifacts documented (momentum:dev runs this automatically).
- [ ] Single-surface invariant (AC8) asserted by at least one eval.

**Frozen verification contract reminder:** a frozen contract for this sprint will live at
`sprints/{sprint-slug}/specs/companion-surface-post-sprint-results-gate.{ext}`. Before signaling
done, the dev reads only the Part-A header (`how_dev_self_checks`, `verification_method`,
`harness_profile`) as a self-check — never the verifier body (Part B: scenarios, assertion scripts)
beyond sections `how_dev_self_checks` explicitly references.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
