> Ephemeral bridge document — consume in the `/momentum:retro` session for sprint-2026-07-13, then delete once consumed.

# Retro Handoff — sprint-2026-07-13

**Written:** 2026-07-30 · **By:** the Conductor session that ran the resumed build through approval and push
**Sprint state:** COMPLETE — approved at end-gate 2026-07-30, merged to main (fast-forward), pushed (`origin/main` at `a5fc3e1`), plugin bumped to **0.32.0**. `sprints/index.json` `completed[]` carries `{sprint-2026-07-13, status: done, retro_run_at: null}` — the shape retro Step 1 keys on.

## The build in one paragraph

15/15 stories merged (no blocked, no quarantined). The sprint's proof — the compose→register→resolve driver against the populated nornspun fixture — was observed passing three separate times (dev run, QA independent re-execution, E2E re-run; console `PASS — all assertions hold.` + exit 0 each time). The build itself was interrupted (session death after stage-3 of 6 stories, 2026-07-21→22) and resumed from the build ledger; the six live worktrees were preserved against the reconcile heuristic per the resume handoff's override, and merged per its conflict-aware order (one semantic conflict resolved via directed fixer + two deterministic self-supersession hunks; everything else rebased clean). A second idle gap (07-24→30) held at the gate with zero drift.

## Durable record (read these, in this order)

1. **`.momentum/sprints/sprint-2026-07-13/build-ledger.jsonl`** (~155 rows) — the authoritative event record: 15 launched/terminal pairs, 35+ finding dispositions, 8 stage3-escalations (the 7 gate cards + 1 routine merge-stitch record), 22 avfl-finding rows, AVFL/coverage/E2E/end-gate phase-complete rows, and the post-approve discharge rows. Supersession rule: latest row wins per (story_slug, event, finding_id). NOTE: per-story finding_ids collide across stories (`bmad-code-review-0` exists per story) — always key on (story_slug, finding_id).
2. **`.momentum/handoffs/sprint-2026-07-13-endgate-report.html`** — the single human-facing decision surface. **Retro Phase 4.5 EXTENDS this file** (fused re-render): insert §08 before the gate div; the gate `<script>` carries the literal parse-stable lines `var STAKES_DECISION_COUNT = 7;` / `var FC_SLUGS = [];` / `var PROCESS_COUNT = 0;` — preserve the first, rewrite only `PROCESS_COUNT`. §04 card state is ALREADY pre-populated in the HTML (all 7 checkboxes `checked`, Option-A radios `checked`) — developer verdicts were recorded at the gate; do not reset them.
3. **`.momentum/sprints/sprint-2026-07-13/`** — coverage-plan.md, specs/ (15 frozen contracts), build-cross-artifact-notes.json (11), deferred-triaged-out.json (4), writable-files.json.

## Gate outcome (all recorded in the ledger)

All 7 decision cards: **Option A**, four upgraded to fix-now and applied in the change pass (commits `4964ff7` D1 staging-union + D3 runtime-state-exclusion, `798a0c5` D2 --kb unconditional, `d0046be` D6 eval mechanism, `e68c34f` D4a debugprobe1 removal — regression contract re-ran exit 0). D4b queued as follow-up story; D5 acknowledged (fix queued, must land before the coherence gate's first live firing); D7 acknowledged (agent-stitched approve flow — it then executed correctly at this very approval).

## Open observation legs the RETRO ITSELF discharges

- **conduct-adoption-retire-sprint-dev** final leg: "retro finds the freshly completed sprint." If your Step 1 discovers sprint-2026-07-13 without HALTing, that observation closes the leg — append a note to its `coverage-deferral-discharged` evidence chain (ledger row exists from the approve; the retro-discovery leg was explicitly deferred to you).
- Still unobserved anywhere: re-approval no-op; the five crafted-probe legs (truncated ledger line, smoke-routed story, missing-declaration BLOCKED, unevidenced-pass rejection, env-unavailable BLOCKED) — queued as a fixture-sprint candidate; the coherence gate and handoff-automation first live firings (next planning run).

## Raw material for the process digest (Keep / Stop / Change candidates)

1. **Subagent signal delivery is chronically unreliable** — nearly every dev/fixer/simplify/QA agent idled without delivering; the SendMessage nudge recovered 100% of them. Candidate: bake the nudge into the Conductor workflow, or fix the agent return convention.
2. **The proof-story dev stalled ~3h** wedged between "run the real pipeline" and "do not spawn agents" (build-guidelines is an orchestrator), compounded by the plugin-cache-vs-sprint-branch seam. The retry with corrected routing (invoke agent-builder skill directly; follow worktree files, not stale cache) succeeded immediately — and revealed attempt 1 had finished composition before being killed. Candidate: spawn-prompt doctrine for stories that must exercise orchestrator skills; cache-vs-branch diff check before spawning registry agents (now in auto-memory).
3. **The E2E validator breached its no-spawn constraint** by fanning out 4 children — whose results routed to the Conductor, not to it (parent stood down). The breach produced the best coverage of the phase (72 scenarios, honest SKIP accounting). Candidate: sanction a Conductor-driven Phase-4 fan-out instead of a single validator agent.
4. **AVFL merge-review scores never converged (51→46→77→71, NON_CONVERGENT)** because deliberately gate-held stakes cards re-count every iteration. Candidate: exclude escalated-and-carded findings from the convergence score, or short-circuit when the finding set ⊆ known-escalated.
5. **Verify-then-fix earned its keep twice**: the haiku consolidator asserted false premises (dual-table "inconsistency"; the word "safe" that never existed; the model-pin "accident" that was the developer's own deliberate commit 50b8b12) and the fixer/Conductor dismissals were all evidence-grounded. Candidate: keep adversarial-verify before any fix; consider a stronger consolidator model.
6. **Test-probe hygiene**: `debugprobe1` leaked from the prior session's registration-guard sandbox probe into the committed index, then had to be removed via a sole-writer exception because **no index-entry removal CLI exists** (queued follow-up includes it).
7. **Environment friction now memorized** (auto-memory `project-conduct-operational-gotchas`): hookify false-positive on `git checkout -- <path>` (developer narrowed the regex mid-run), large-inline-payload hook denials → script-file appends, `momentum-tools` shim resolves to main repo, Workflow-tool `args` arrives as a string on scriptPath re-invocation, session scratchpad does not survive long idle gaps.

## Queue + loose ends (do not resolve in retro; just be aware)

- **19 practice-ledger entities** queued under source `conduct-sprint-2026-07-13` (11 cross-artifact notes + 4 triaged-out findings + model-routing reconciliation + 2 coverage observations + create-story write-path follow-up) → the developer's next `/momentum:triage` batch session.
- **Unpushed local commits on main**: `9e8fd7e` (consumed-handoff cleanup) + this handoff's own commit — ride the next push.
- The developer's own rules/skills reorg sits **uncommitted in the working tree** (`.claude/rules/` + `.claude/skills/momentum-*` deletions, `CLAUDE.md` edit) — theirs; do not stage, commit, or clean it.
- Retro audit subagents run on **Sonnet** (standing feedback memory).
