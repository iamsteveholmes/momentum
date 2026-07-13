# Handoff: 2026-07-06 refine complete — next step is sprint-planning

**Date:** 2026-07-10
**From:** refine execution session (2aaa5e94) — full apply of the consolidated gate approved by the developer.
**Next step:** `momentum:sprint-planning` with the §4 "cohort goes live" shortlist in
`.momentum/handoffs/next-sprint-cohort-review-2026-07-06.md` (still the live brief — read it first; §4 verified intact post-refine on 2026-07-10). Plugin marketplace already updated; run planning in a fresh session.

## What this refine changed (all committed AND pushed — origin/main at `8876afd`)

- **Backlog 288 → 266 active** (the two new stubs included). POST priorities: critical 13, high 80, medium 107, low 66.
- **24 drops** (7 handoff-superseded + 12 stale-eval + 5 dedup merges), **7 priority changes**, `researcher-base-body` closed done. Full list in commit `70ad807`.
- **Two epic splits adopted** (developer's Fork 2 call, overriding the defer recommendation):
  - NEW epic `momentum-conductor-core` (type flow) — whole conduct-*/conductor-* family moved wholesale incl. done stories; 47 stories, 14 remaining. All three §4 conductor stories live here now.
  - `momentum-impetus-session-orientation` narrowed to session/install surface; retro/planning/agent-infra stories rehomed to owning epics. 104 rehomes total, zero orphan epic refs left. Mapping in commit `70ad807`; epics.json recompute in `6b31abc`.
- **Two new developer-approved stubs** (Fork 3): `avfl-spec-contract-finding-owner-assignment` (high, quality-gates) and `story-file-completion-metadata-write-back-sweep` (medium, conductor-core).
- **4 practice-ledger consumes** for entries closed by shipped work; 12 auto close_stale events also landed 2026-07-10.
- Repo hygiene: 6 stale local branches deleted (all verified merged), leftover worktree removed, stray research run consolidated into `docs/research/`, session byproducts gitignored. Working tree clean.

## Developer-directed additions to the shortlist (2026-07-13)

The developer asked that the sprint-planning and conduct process fixes ride along this sprint —
pull these into selection alongside the §4 six (planning may wave/sequence them; the criticals are
non-negotiable, the mediums may be trimmed if sizing balks):

**Sprint-planning fixes (land during the build; improve future planning sessions):**
- `sprint-planning-cross-story-coherence-gate` (critical)
- `sprint-planning-continuous-execution-and-cli-fixes` (high) — **co-select/merge check** with `sprint-planning-enforce-continuous-sequential-execution` (high): overlapping scope, likely one story
- `sprint-planning-handoff-artifact` (high)
- `sprint-planning-pre-sprint-class-1-render-gate`, `sprint-planning-story-size-heuristic`, `retro-and-planning-ux-defaults` (medium — trim candidates)

**Conduct hardening (beyond the §4 endgate fix + Phase 0 port):**
- `conduct-qa-execute-verification-method` (critical)
- `conduct-resume-and-rehydration-idempotency-hardening` (high)
- `conduct-conductor-staging-and-ledger-append-safety` (high)

## DEC-039 governs this planning session (2026-07-13)

`_bmad-output/planning-artifacts/decisions/dec-039-sprint-goal-mutable-scope-2026-07-10.md`
landed after this handoff was written and the skill updates are **amendment-pending** — apply it manually:

- **D1:** capture a one-to-few-sentence **sprint goal** during planning, store it in the sprint record
  (`.momentum/sprints/index.json` entry), and approve it at the plan gate. Stories are the decomposition,
  not the definition of done. For this sprint the goal derives from the "cohort goes live" intent — the
  epic acceptance_conditions in epics.json are the citation source (DEC-035 composes).
- DEC-030 D3's never-add freeze is amended: goal-critical discovered work is admissible via the D2
  routing matrix (loud absorption — `discovered-from` linked, cited, end-gate-reported). The end-gate
  verdict is dual: stories delivered AND goal delivered.

## Notes for the planning session

- §4 shortlist unchanged and active: `momentum-knowledge-base-buildout` (M), `manifesto-builder-skill-generate-then-curate` (M, needs re-enrichment vs manifesto-format.md incl. File Ownership), `base-body-collapse-rollback` (high — co-select/link siblings `rename-base-body-files-to-canonical-naming`, `architecture-decision-26-update-for-base-body-collapse`), `conductor-endgate-viewer-hijack-and-silent-gate` (critical), `conduct-adoption-retire-sprint-dev` Phase 0 only, then Wave 2 `conduct-live-run-against-fixture-sprint` (verification must demand observed driver PASS/FAIL output — never structured status; the shipped driver has never passed).
- `repair-phantom-story-file-entries-and-backfill-live-fixture-scope` (high, conductor-core) owns the phantom `story_file:true` repair incl. `conduct-live-run-against-fixture-sprint`'s spec — planning should sequence or fold that backfill before/with Wave 2.
- 4 stale remote branches remain on origin (feat/companion-decision-surface-standard, sprint/sprint-2026-05-03, -05-26, -06-10) — all merged; pruning offered but not yet approved.
