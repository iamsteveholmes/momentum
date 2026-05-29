# Handoff — `conduct` (sprint-dev rework)

**Date:** 2026-05-29
**From:** session 71575940 (sprint-2026-05-26 close-out + conduct design)
**To:** the session doing the sprint-dev rework
**Status:** **DESIGN DRAFT — nothing implemented.** Spec + report template exist; naming recommended; 10 open questions UNRATIFIED. This is forward-planning; implementation is a future sprint.

---

## TL;DR

`conduct` is the proposed replacement for `momentum:sprint-dev`: an autonomous, **per-story** execution engine with **exactly one** human gate at the end. A **Conductor** runs each story as its own independent pipeline (dev → concurrent QA + code-review → fix → merge-its-own-worktree), fully autonomously (dev always retries, AVFL never asks, legit issues always auto-fixed), then reviews the integrated merge (AVFL-as-Workflow), runs E2E, and surfaces **one** context-rich HTML report whose only outcomes are **request changes** (loop) or **approve** (triage leftovers → merge to main → ask-before-push). No Reject. Coexists with `sprint-dev` until that's deprecated.

## Artifacts produced (all committed to `main`)

| Artifact | Path | What it is |
|---|---|---|
| **Redesign spec** | `_bmad-output/planning-artifacts/sprint-dev-redesign-spec.md` | 13-section design (commit `56f8b4d`). The authoritative design doc. Still titled "sprint-dev redesign" — **needs `conduct` naming threaded through** (see below). |
| **HTML report template** | `.momentum/handoffs/conduct-report-template.html` | Self-contained report template enforcing the CORE MANDATE (every section carries full context). Worked example uses sprint-2026-05-26. Open in a browser. |
| **This handoff** | `.momentum/handoffs/conduct-redesign-2026-05-29.md` | Pins the naming (not in the spec) + the open-question state. |

The spec's section map: (1) design intent + 10 binding decisions, (2) end-to-end flow, (3) per-story pipeline + Conductor, (4) quality gate (QA + `bmad-code-review` + code-fixer), (5) AVFL-as-Workflow reviewer-of-the-merge, (6) git lifecycle (Conductor owns all mutation), (7) planning→dev verification-contract handoff, (8) single HITL gate + the one change-workflow + approve sequence, (9) the HTML report spec, (10) **agent gap map + build order**, (11) removed-vs-kept, (12) files touched, (13) **10 open questions**.

---

## Naming decision (NOT yet in the spec — thread it through)

Recommended via a brainstorm (66 candidates / 6 families) + 4-lens judge panel:

- **Skill name: `conduct`** → `momentum:conduct` / `/conduct`. Top-ranked (avg 8.0, no veto). Names the architecture (orchestrate independent players → one resolved end), reads as a natural command, doesn't collide with the **Impetus** persona (Impetus *dispatches* conduct; the Conductor *runs* it), shares no stem with `sprint-dev`.
- **Conductor** — the orchestrator role (lowercase functional label, NOT a named persona).
- **movement** — one story's independent pipeline unit.
- **encore** — the single unified change/fix loop when the developer requests changes at the gate.
- Mental model: *Impetus dispatches `conduct`; the Conductor runs each story as a movement; on requested changes it plays an encore; then it converges at the gate.*

**Runner-up shortlist** (if `conduct` is rejected): `cruise` (7.3, great autonomy but single-vehicle feel), `sprint-run` (7.3, safest/most-native but conceptually flat), `autopilot` (7.0), `sprint-ship` (7.0). Honorable mentions that nail the model but lose on ergonomics: `sprint-converge`, `sprint-dispatch`, `convoy`.

**Coexistence → deprecation:** (1) ship `conduct` beside `sprint-dev`, trial it; (2) soft-deprecate `sprint-dev` (notice + make `conduct` Impetus's default dispatch); (3) stub `sprint-dev` (mirror `feature-status`→`canvas` pattern), drop after a release cycle.

> ⚠️ **Naming not finally confirmed by the developer.** They engaged with it positively but didn't explicitly lock it. The HTML template already uses `conduct`/Conductor/movement/encore; the spec does NOT. If confirmed, do a naming pass over the spec.

---

## The 10 open questions — recommendations (ALL UNRATIFIED)

These are the convergence points. The developer has NOT ratified any (the decisions they resolved this session were the *current sprint's* DuckDB + archive, unrelated). My recommendations, for the other session to ratify or redirect:

1. **`/simplify` placement** → **end-gate opt-in only** (not per-story; keeps build cost/latency reasonable). *[flagged for developer]*
2. **Retry bounds** → standardize **dev=2, merge=3, fix-loop=3**, overridable per-sprint.
3. **`bmad-code-review` config** → **RESOLVED** — `_bmad/bmm/config.yaml` exists; no extra work.
4. **AVFL on disjoint merge** → short-circuit to CLEAN when `integration_surface` empty, full loop otherwise; log the skip.
5. **`review_depth: deep` authority** → sprint-planning sets it; heuristic = high-blast-radius change types.
6. **Conductor = skill or top-level session?** → **the top-level session embodies the Conductor** (the `conduct` workflow runs in main context like sprint-dev/Impetus today) — it spawns subagents for all writes and legitimately owns git + push. A separately-spawned skill can't hold the long end-gate conversation or push. ***Most important architectural call.***
7. **Where `code-fixer` lives** → a **fix-mode of `momentum:dev`** (reuse dev.md) rather than a second body that drifts.
8. **E2E ↔ verification-contract overlap** → the contract is the **single source of truth**; the harness JSON derives from contracts.
9. **`closed-incomplete` vs `dropped`** → blocked/never-completed → `closed-incomplete` (+ stub); `dropped` only by explicit developer descope, never autonomous.
10. **Pre-flight HALTs (H1–H5)** → keep all 5 (they're "cannot-start" guards, not in-between gates — don't violate decision 1).

Most worth the developer's eyes: **#6** (Conductor as top-level session) and **#1** (`/simplify` opt-in vs always-on).

---

## Implementation roadmap (from the spec's agent gap map — build order, most-blocking first)

1. **code-reviewer adapter → `bmad-code-review`** (P0) — `momentum:code-reviewer` is a STUB; wire the existing real BMAD bug-hunter as the per-story reviewer, normalize its triage into the finding schema.
2. **`code-fixer` body** (P0) — new write-capable fixer (or dev fix-mode per Q7); used by the per-story fix step, the change-workflow loop, AND merge-conflict resolution.
3. **`conduct` skill + HTML report template wiring** (P0) — the Conductor, the end-gate-as-conversation, triage/merge/push. Largest new build.
4. **Rescope `qa-reviewer`** to per-story worktree + **teach `dev` to read the verification contract's Part-A header** (P1).
5. **AVFL prose → Workflow**, retargeted at the 3-dot merged git result (P1); reuse the sub-skills; integration findings → code-fixer.
6. **merge-resolver wiring** (P1) — Conductor inline for trivial, escalate to code-fixer for semantic; no new base body.
7. **Cleanup `agents.json`** dead `architect`/`pm`/`sm` paths (P2).

Per `version-on-release`: shipping `conduct` = **minor** bump; stubbing `sprint-dev` later = another **minor**.

---

## What's NOT done / next steps for the other session

- **Ratify the 10 open questions** (or accept the recommendations above), especially #6 and #1.
- **Confirm the name** `conduct` (+ vocabulary). If yes, do a naming pass over the spec (currently "sprint-dev redesign").
- **Turn the spec into stories** — the gap-map build order is the natural epic breakdown. This is a future sprint, not done here.
- The HTML template is a *mockup with sample data* — when implementing, the Conductor generates the report data-driven (template/data separation is specified in spec §9).

## Cross-references

- Spec: `_bmad-output/planning-artifacts/sprint-dev-redesign-spec.md`
- Template: `.momentum/handoffs/conduct-report-template.html`
- Decisions behind the current sprint that motivated this: `DEC-033` (practice-ledger), `DEC-034` (epic migration) in `_bmad-output/planning-artifacts/`
- Current `sprint-2026-05-26` is closed/merged to main (version 0.24.0); **47 commits await push** (developer's call) — unrelated to conduct.
