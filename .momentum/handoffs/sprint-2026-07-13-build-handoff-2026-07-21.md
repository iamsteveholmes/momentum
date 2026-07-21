# Build Handoff — sprint-2026-07-13

> **Use-then-discard build bridge** for the next `/momentum:conduct` session. Delete after
> consumption (handoffs are ephemeral). Written manually by planning — the automated emission
> is this sprint's own `sprint-planning-handoff-artifact` story.

## Sprint goal (DEC-039 D1 — approved at the plan gate 2026-07-21)

The agent cohort goes live: the composition stack — Momentum's own KB, the manifesto producer,
and routing-table resolution — lands and is proven by the shipped E2E driver passing live
against the nornspun fixture with observed PASS output, exercising the exact resolve seam a
/momentum:conduct build uses to spawn composed gen-2 subagents. The ride-along fixes harden the
conduct engine and planning rails that this sprint's own conducted build runs on.

**End-gate renders a dual verdict (DEC-039 D3, applied manually — machinery not yet built):
stories delivered AND goal delivered.** Goal delivered = the live-run driver's observed
`PASS — all assertions hold.` + exit 0. Mid-build discovered work routes through the DEC-039 D2
matrix (punt / auto-pull-with-citation / pause-ask / recommend-new-sprint) — recorded in
architecture.md (Sprint Orchestration) and prd.md FR139.

## Stories by wave

**Wave 1 (12, parallel):** momentum-knowledge-base-buildout · manifesto-builder-skill-generate-then-curate ·
base-body-collapse-rollback · conductor-endgate-viewer-hijack-and-silent-gate ·
conduct-adoption-retire-sprint-dev · repair-phantom-story-file-entries-and-backfill-live-fixture-scope ·
sprint-planning-cross-story-coherence-gate · conduct-qa-execute-verification-method (2 out-of-sprint
deps, both done) · sprint-planning-continuous-execution-and-cli-fixes · sprint-planning-handoff-artifact ·
conduct-resume-and-rehydration-idempotency-hardening · conduct-conductor-staging-and-ledger-append-safety

**Wave 2 (3):** rename-base-body-files-to-canonical-naming (after rollback) ·
architecture-decision-26-update-for-base-body-collapse (after rollback) ·
conduct-live-run-against-fixture-sprint (after KB + manifesto + repair — THE proof story)

## Contract / spec locations

Per-story frozen contracts (SHA-pinned in `planning.team.story_assignments`):
`.momentum/sprints/sprint-2026-07-13/specs/{slug}.{eval.yaml|smoke.sh|review.md}`
Coverage plan: `.momentum/sprints/sprint-2026-07-13/coverage-plan.md` — the integration scenario
"Conducted fixture build — interrupted, resumed, approved" discharges 5 conductor stories
(endgate, retire-P0, resume, staging, qa-execute); 10 stories are dedicated runs.

## Planning-time cautions (build MUST honor)

1. **Merge sequencing:** six Wave-1 stories touch `skills/momentum/skills/conductor/workflow.md`
   (endgate, retire-P0, resume, staging, qa-execute, rollback ref-sweep) — merge these serially
   with a conflict review each; also overlaps on sprint-planning/workflow.md ×4,
   momentum-tools.py ×3, build-ledger.md ×2. (Plan-gate Fork 3, accepted with this caution.)
2. **Land the end-gate and staging fixes early in Wave 1** — this sprint's own end-gate runs on
   the pre-fix code until they merge.
3. **Live-run hard rule:** acceptance is ONLY the driver's observed stdout PASS + exit 0.
   Structured status, prior done, self-reports, harness "skip" = FAILURE. The contract
   (conduct-live-run-against-fixture-sprint.smoke.sh) executes the driver itself.
4. **Frozen invocation shapes:** continuous-cli's contract froze `sprint plan --slug` (AC-stated
   shape); live-run's contract froze the driver env-var interface. If the implementer ships a
   different shape, escalate a contract update loudly — never adjust silently.
5. **Rename story runs Option A** (verify + annotate DEC-020, zero renames) — ruled at both
   gates; the PRE-REQ gate task in that story is discharged by this record.
6. **Cross-repo surfaces:** the KB vault (~/projects/momentum-agentic-kb), the shared wiki-query
   skill (~/.obsidian-wiki config), and the nornspun fixture (~/projects/nornspun) are outside
   this repo — pin exact paths, prefer config-driven resolution, never fork the shared skill.

## Plan-gate decision record (2026-07-21, Decision: A)

Fork 1 goal: Approve as worded · Fork 2 proof chain: Accept as sequenced · Fork 3 overlap:
Accept with sequencing caution · Fork 4 narrowed proof scope: Confirmed · Fork 5 rename:
Option A · Fork 6 KB: both legs · Fork 7 harness override: Confirmed.
(Also stored at `.momentum/sprints/index.json` → active sprint `plan_gate`.)

## Where state lives

Sprint record: `.momentum/sprints/index.json` (active) · Stories: `.momentum/stories/{slug}.md` ·
Contracts+coverage: `.momentum/sprints/sprint-2026-07-13/` · Branch: `sprint/sprint-2026-07-13`
(9 planning commits, unpushed).
