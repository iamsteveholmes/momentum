# Handoff: Run the Retro for sprint-2026-06-28

**Date:** 2026-07-06
**From:** end-gate pickup session (f9aa0ebe-39e4-470d-a386-9889bbc9245c)
**Next action:** In a fresh session, invoke `/momentum:retro` for `sprint-2026-06-28`. Plugin is already at 0.31.0 (marketplace update confirmed) — no update needed before starting.

---

## Sprint state (all closure mechanics DONE — retro is the only remaining step)

- **Sprint:** `sprint-2026-06-28` — companion surfaces + agent-cohort. 5 stories, 2 waves.
- **Outcome:** all 5 stories merged → transitioned review→verify→done. Sprint marked `completed` 2026-07-06 via `momentum-tools sprint complete`.
- **Merge:** sprint branch merged to main (no conflicts), branch deleted, **pushed** — main is at `cf4033f` (0f00342..cf4033f, 34 commits).
- **Version:** plugin bumped 0.30.0 → **0.31.0** (`f1f68a0`).
- **End-gate:** developer approved at the gate (report: `.momentum/handoffs/sprint-2026-06-28-endgate-report.html`, committed `9b2aff3`, 3 decision cards).
- After retro completes, mark it: `momentum-tools sprint retro-complete`.

## Stories (all done)

| Story | Notes for retro |
|---|---|
| companion-surface-pre-sprint-plan-gate | QA BLOCKED all 9 ACs on runtime-unverifiability (no harness) → deferred to E2E; 1 critical finding dismissed, 11 fixed |
| companion-surface-post-sprint-results-gate | 2 critical code-review findings FIXED during build, escalated to end-gate for visibility only (paint() constant; §13 dual-section gate) |
| companion-surface-rule-sync-and-bulk-derivation | clean |
| manifesto-format-normative-file-pattern-ownership-field | 5 findings fixed |
| live-e2e-compose-register-resolve-gen-2-agent | **genuine residual**: live composition run against nornspun NOT performed (fixtures unset); merged with escalation; backlog stub exists: `conduct-live-run-against-fixture-sprint` |

## Build-phase signals (from `.momentum/sprints/sprint-2026-06-28/build-ledger.jsonl`)

- AVFL-on-merge: CLEAN, score 100, 2 iterations, 2 fixes, 0 leftovers.
- E2E: 27 scenarios — 10 passed, 1 low FAIL, **16 BLOCKED**, all traced to unset fixtures (no live sprint-planning / completed-sprint / composed-nornspun). Implementations confirmed present in source.
- Finding dispositions: 32 total, all fixed/dismissed; 0 blocked.
- Cross-artifact batch: 2 notes routed to backlog (retro audit-workflow process_findings; endgate format spec §3 alignment) — the first is directly about the retro skill itself.

## PRIME RETRO MATERIAL — process incident during this sprint's end-gate

The conduct session (transcript `83ea46d8-000b-487f-9455-8073a512dc23.jsonl`, 15:59–18:01Z) ended with three verified defects that caused the developer to lose their session view and the sprint to park silently:

1. **Focus-steal against spec:** end-gate open ran `cmux browser new … --focus true`; conductor workflow.md:2337/:2610 mandate `--focus false`.
2. **False placement assumption:** workflow.md:2336 + endgate-report-renderer.md assume `cmux browser new` reuses the viewer pane (placement=reuse). Verified false by live test: it ALWAYS returns `placement=split` and creates a new structural pane, even when a browser pane exists and is focused. Correct pattern: reuse existing viewer surface via `cmux browser <surface> goto <url>` when its content is superseded; `browser new --focus false` only when none exists. (Memory saved: `reference_cmux_browser_new_always_splits`.)
3. **Silent gate:** the conductor's turn ENDED immediately after opening the report — the workflow.md:2341 end-gate ask was never presented. The approval was recovered in a follow-up session ~18 min later.

**Already captured as a critical backlog stub:** `.momentum/stories/conductor-endgate-viewer-hijack-and-silent-gate.md` (epic `momentum-sprint-orchestration`, story_type defect, priority critical). The retro should treat this incident as a finding with an existing remediation stub — do not duplicate the stub; do audit the transcript for root cause of defect 3 (why the turn ended between render and ask).

## Transcripts for the retro audit engine

- Build/conduct session: `~/.claude/projects/-Users-steve-projects-momentum/83ea46d8-000b-487f-9455-8073a512dc23.jsonl` (4.5 MB)
- End-gate pickup session (intake + approve + merge + push): `f9aa0ebe-39e4-470d-a386-9889bbc9245c.jsonl`
- Earlier same-day sessions if needed: `5fab6aaf-…` (10:31), `321745ff-…` (08:44)

## Housekeeping observed (optional retro/refine fodder)

Untracked clutter in the working tree predating this session: `undefined/`, `raw/`, `skills/momentum/skills/retro/err.log`, `.momentum/close-stale.log`, stale `conduct-core-*` artifacts from sprint-2026-06-02. Harmless but worth a sweep.
