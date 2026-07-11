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

## Notes for the planning session

- §4 shortlist unchanged and active: `momentum-knowledge-base-buildout` (M), `manifesto-builder-skill-generate-then-curate` (M, needs re-enrichment vs manifesto-format.md incl. File Ownership), `base-body-collapse-rollback` (high — co-select/link siblings `rename-base-body-files-to-canonical-naming`, `architecture-decision-26-update-for-base-body-collapse`), `conductor-endgate-viewer-hijack-and-silent-gate` (critical), `conduct-adoption-retire-sprint-dev` Phase 0 only, then Wave 2 `conduct-live-run-against-fixture-sprint` (verification must demand observed driver PASS/FAIL output — never structured status; the shipped driver has never passed).
- `repair-phantom-story-file-entries-and-backfill-live-fixture-scope` (high, conductor-core) owns the phantom `story_file:true` repair incl. `conduct-live-run-against-fixture-sprint`'s spec — planning should sequence or fold that backfill before/with Wave 2.
- 4 stale remote branches remain on origin (feat/companion-decision-surface-standard, sprint/sprint-2026-05-03, -05-26, -06-10) — all merged; pruning offered but not yet approved.
