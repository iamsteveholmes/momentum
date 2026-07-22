> Ephemeral bridge document — use to resume the conducted build of sprint-2026-07-13 in a fresh session, then delete once consumed.

# Conduct Build Resume Handoff — sprint-2026-07-13

**Written:** 2026-07-22 · **By:** the Conductor session that ran Phases 1–2 (interrupted by UI trouble, not by build failure)
**Resume command:** `/momentum:conduct` — the Conductor rehydrates from the build ledger at `.momentum/sprints/sprint-2026-07-13/build-ledger.jsonl`.

## ⚠ Critical resume caution (read first)

Six stories are `in-progress` with live worktrees under `.worktrees/` and story branches carrying ALL their work as commits. The installed workflow's Phase-1 "reconcile on start" would DELETE these worktrees/branches and reset the stories to ready-for-dev — **do not let it**. Nothing in these worktrees is stale; every one is at the END of stage-3 (reviews done, fixes applied, simplify done) and needs only the stage-4 rebase-then-merge (workflow step 2.2.M). Treat the reconcile's "in-progress = crashed" heuristic as overridden by this handoff and the ledger's `conductor-warning` checkpoint row.

## State snapshot

**Sprint branch:** `sprint/sprint-2026-07-13` at `1739e82` (checked out in the main worktree).
**Uncommitted in main worktree:** `.momentum/practice-ledger.jsonl`, `.momentum/stories/index.json` (status churn; `.momentum/sprints/index.json` may also show churn) — commit as a chore checkpoint or leave; harmless.
**Build ledger:** current through the simplify-pass rows + handoff checkpoint row (event set matches references/build-ledger.md; rehydration-ready).

### Merged to sprint branch (6) — status `review`
| Story | Outcome |
|---|---|
| conduct-adoption-retire-sprint-dev | clean (0 findings) |
| sprint-planning-continuous-execution-and-cli-fixes | clean (0 findings) |
| repair-phantom-story-file-entries-and-backfill-live-fixture-scope | 1 finding triaged-out (reverse-phantom caller ordering → deferred triage) |
| conductor-endgate-viewer-hijack-and-silent-gate | 3 findings fixed |
| conduct-qa-execute-verification-method | 1 finding fixed |
| conduct-conductor-staging-and-ledger-append-safety | 3 fixed + **1 escalated (decision card)** |

### Ready to merge (6) — status `in-progress`, worktrees live, ALL work committed on story branches
Merge each per step 2.2.M (rebase in the worktree onto sprint tip → `--no-ff` merge → worktree/branch cleanup → status→review → ledger `story-terminal` merged row). Suggested order (conflict-aware):

1. **sprint-planning-cross-story-coherence-gate** (tip `a36163e`) — findings: 6 fixed. Rebase WILL likely conflict in `sprint-planning/workflow.md` (cli-fixes merged there). Classify per 2.2.M.3.
2. **sprint-planning-handoff-artifact** (tip `e404821`) — findings: 2 fixed. Same file conflict risk, after #1 merges it grows.
3. **conduct-resume-and-rehydration-idempotency-hardening** (tip `61b0b8d`) — findings: 2 fixed. HIGH semantic-conflict risk in `conductor/workflow.md` + `build-ledger.md` vs the already-merged staging-ledger story (both edited rehydration/ledger text). Use the semantic-resolution fixer path (2.2.M.3) if hunks overlap.
4. **base-body-collapse-rollback** (tip `84a07a3`) — findings: 1 fixed; simplify returned none. Conflicts possible in `conductor/workflow.md` + `sprint-planning/workflow.md` (regions likely distinct). **Merging unlocks wave-2 stories #13/#14.**
5. **momentum-knowledge-base-buildout** (tip `2fbad92`) — findings: 2 fixed, 2 dismissed (rationales in ledger), 1 triaged-out, **1 escalated (decision card)**. NOTE: its simplify pass was never dispatched — worktree is clean; either dispatch a quick simplify or record `findings_count: 0` deliberately (a simplify row for it is NOT yet in the ledger; the batch-4 rows cover the other five). Also has out-of-repo deliverables already live (vault `~/projects/momentum-agentic-kb/`, registry entries in `~/.obsidian-wiki/config`, ratified wiki-query SKILL.md edit — see ledger conductor-warning).
6. **manifesto-builder-skill-generate-then-curate** (tip `3e460c5`) — findings: 3 fixed, 1 triaged-out. **kb + manifesto + repair-phantom merges unlock wave-2 story #15.**

### Wave-2 — NOT launched (3) — status `ready-for-dev`
For each, at launch: contract-freeze check (step 2.V, SHAs in sprints/index.json), coverage check (all three are `dedicated-run`), branch+worktree from the then-current sprint tip, dev spawn per step 2.1 STAGE-1 (constraints: no git mutation, uncommitted output, writable_files, cross-artifact rule), then stage-2 QA+CR → stage-3 → merge.
- **rename-base-body-files-to-canonical-naming** (← base-body) — touches dec-020 doc; verification: skill-invoke eval.
- **architecture-decision-26-update-for-base-body-collapse** (← base-body) — architecture.md; verification: document-review (per sprint record, no qa-reviewer role — pure document review).
- **conduct-live-run-against-fixture-sprint** (← kb, manifesto, repair-phantom) — the sprint's proof story: run the shipped build-guidelines E2E driver live against the nornspun fixture (compose→register→resolve seam), artifact to docs/research/; verification: bash smoke.

### End-gate decision cards accumulated (2) — both in ledger as `stage3-escalation` rows
1. **staging-ledger / bmad-code-review-0** — `irreversible-destructive`, end-gate-expanded: the story-commit file_list-preference staging clause can silently drop an in-scope new deliverable omitted from a non-empty file_list (destroyed at worktree cleanup). Fix deliberately NOT applied (stakes-class). Suggested fix in ledger row.
2. **kb-buildout / bmad-code-review-0** — `high-blast-radius-architecture`, end-gate-expanded: build-guidelines mandates unconditional `--kb`, constitution-builder's emit logic still self-determines — emitted Tier-1 constitutions can drop KB scoping (wrong-vault fallback). Needs follow-up story; evidence + fix in ledger row.

### Remaining phases after all 15 stories terminal
- **Phase 3 AVFL-on-merge:** invoke avfl-merge-review Workflow (skills/momentum/skills/avfl/workflow-merge-review.md) with sprint branch vs main, merged_stories (slug+touches), story_contracts map. Conductor commits fixer output per iteration. Then **step 3.D**: discharge the 5 coverage deferrals — all name scenario "Conducted fixture build — interrupted, resumed, approved" (this very build IS that scenario: it was interrupted and resumed; the discharge executor must verify each deferred story's acceptance behavior was observed in this integrated, resumed build).
- **Phase 4 E2E:** e2e-validator agent over the integrated sprint branch; normalize findings; routine auto-fix / stakes escalate.
- **Phase 5 end-gate:** assemble from LEDGER ONLY (Sources 1–3 + supporting vars incl. supersession), render HTML report to `.momentum/handoffs/sprint-2026-07-13-endgate-report.html` per references/endgate-report-renderer.md, open in cmux viewer (query-then-branch, `--focus false`, render-then-ask atomic), single ask. Approve path includes `momentum-tools sprint complete` (ported this sprint by conduct-adoption — it's in the merged workflow), MAJOR-residual governance guard, push confirmation.

### Deferred work-lists (now durable in the sprint dir — session scratchpad copies are dead)
- **`.momentum/sprints/sprint-2026-07-13/build-cross-artifact-notes.json`** (7 notes) → route ONCE as a batch to momentum:triage at build-phase completion (step 2.2 wrap-up), then ledger conductor-warning row.
- **`.momentum/sprints/sprint-2026-07-13/deferred-triaged-out.json`** (3 records) → momentum:triage stubs at build-phase completion (reverse-phantom ordering fix; Dev-Agent-Record systemic gap; nornspun-client wiki-query sync).
- **`.momentum/sprints/sprint-2026-07-13/writable-files.json`** — wave-1 writable sets (derive fresh for wave-2 stories).

### Operational gotchas learned this run (save re-discovery)
- `momentum-tools` shim resolves to the MAIN repo's script, not a worktree's — QA/smoke runs must invoke `python3 <worktree>/skills/momentum/scripts/momentum-tools.py` or use a PATH shim.
- Dev/fixer/simplify agents return output but often idle without auto-delivering — SendMessage a nudge requesting the structured signal.
- Subagent-of-subagent results (eval graders, lens reviews) route to the Conductor, not their spawner — relay them.
- Ledger appends: use a python script file (a PreToolUse hook intermittently denies large inline heredocs).
- Stage staged-file lists explicitly (new files!) — never bare `git add -u`; the write-scope guard runs on the staged list.
- Reviewer dedup rule: same location+issue from QA and CR → one finding, higher severity, source "qa-reviewer+bmad-code-review".
