# Handoff: Sprint Planning — Conductor Seam-Fix Sprint (First Live Conduct Run)

**Date:** 2026-06-10
**From:** Story-creation session (five conductor seam-fix stories)
**To:** Next session — run `/momentum:sprint-planning`
**Commit anchor:** `c5da23b` — `docs(story): five conductor seam-fix stories for first live conduct run`

## Mission

Compose a sprint from the five conductor seam-fix stories below, then run that sprint as the **first live `/momentum:conduct` run**. The developer explicitly accepted the chicken-and-egg risk: the Conductor will be fixing its own seams on its maiden run ("2 do it, and that can be our first run").

## Pre-flight (do this BEFORE invoking sprint-planning)

Per standing practice (`feedback_fresh_session_before_major_workflows`):

1. `/plugin marketplace update momentum`
2. Restart the session (a `/reload-plugins` is NOT sufficient)
3. Then invoke `/momentum:sprint-planning`

## The Five Stories

All are `ready-for-dev` in `.momentum/stories/index.json`, epic `momentum-sprint-orchestration`, committed in `c5da23b`. Each was produced via `momentum:create-story` with full AVFL checkpoint validation.

| Story slug | What it fixes | AVFL | Priority |
|---|---|---|---|
| `conduct-build-state-persistence-and-resume` | Conductor has zero persistence; mandates append-only `.momentum/sprints/{sprint_slug}/build-ledger.jsonl` + resume path | CLEAN 97/100 | **critical** |
| `conduct-worktree-and-branch-creation` | workflow.md passes `worktree_path` to dev spawn but never creates the worktree/branch | 94, 2 minors fixed | high |
| `conduct-dev-commit-authority-reconciliation` | dev.md instructs dev agents to commit; Conductor invariant 1 claims sole git mutation — dev commits silently neutralize the WRITE-SCOPE COMMIT GUARD (`git add -u` stages nothing on a clean tree). Resolution: Conductor is sole committer; strip commit duties from all 7 dev-side artifacts | accuracy fully clean; 2 minors + 4 lows fixed | — |
| `conduct-qa-reviewer-normalization-adapter` | Conductor consumes canonical qa findings that qa-reviewer never emits (qa-reviewer.md:173 disclaims the shape; promised adapter never built). Binding design decision in story: Conductor-side stage-2 normalization (Option A), verdict-only severity mapping BLOCKED→critical, MISSING→major, PARTIAL→minor | 80 → fixed | — |
| `conduct-coverage-deferral-preserve-code-review` | covered-by-composition disposition skips ALL of stage 2 including code review (workflow.md:376-377); must preserve the code-review lens | CLEAN 95/100 | — |

### Dependency / sequencing notes for planning

- These stories all touch `skills/momentum/skills/conductor/workflow.md` — expect merge adjacency. The commit-authority story also touches `agents/dev.md`, `agents/dev-{build,frontend,skills}.md`, `skills/dev/workflow.md`, `references/directed-fix-invocation-contract.md`, and `sprint-dev-redesign-spec.md`.
- `conduct-dev-commit-authority-reconciliation` declares predecessor `dev-strip-merge-cleanup-authority` (status: done — satisfied).
- No formal `depends_on` edges between the five; treat overlap on conductor/workflow.md as a merge-ordering concern, not a blocker.
- Persistence story is priority **critical** — it is the recovery net if the live run stalls (and stalls are the proven failure mode: three create-story agents stalled on orphaned background validators during this very batch).

## Known Residuals (out of story scope)

1. **epics.json is stale** — `momentum-sprint-orchestration` epic record's `stories` array (last_verified 2026-05-03) lists none of the five slugs. Index entries are correct and authoritative. Either let sprint-planning/sprint-manager enroll them at activation, or run `momentum:epic-grooming` first.
2. **Nothing pushed** — `c5da23b` (and any subsequent commits) are local-only. Push requires explicit developer approval.

## Context: Why These Five

A six-lens adversarially-verified review (30 agents) of `momentum:conductor` concluded: the architecture/process is empirically proven (two hand-run rehearsal sprints, 46/46 stories merged, 17/17 HIGH findings real), but the skill artifact has **zero live runs** and exactly these five confirmed seam defects. Full decision record in memory: `project_conduct_first_live_run.md`.

## Operational Warnings for the Live Conduct Run (after planning)

- **Background-validator orphaning is real.** During story creation, headless `claude -p` validators spawned via background Bash died/orphaned when the spawning agent's turn ended (0-byte output files, no processes). Proven recovery: run the lens inline, or SendMessage the stalled agent with a precise diagnosis. The Conductor has no watchdog — this exact failure class is what the persistence story exists to mitigate.
- **Index writes survived 5-way parallelism this time** (483 entries verified intact), but last-writer-wins clobbering on `stories/index.json` remains a live risk — sole-writer discipline (sprint-manager) matters.
- Git discipline: commits autonomous with `type(scope):` format; story specs are `docs(story)` not `feat`; **never push without explicit approval**; no Co-Authored-By trailers.
