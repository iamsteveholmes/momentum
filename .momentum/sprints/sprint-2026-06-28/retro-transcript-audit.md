# Sprint Transcript Audit — sprint-2026-06-28

## Executive Summary

Five stories shipped (companion-surface-pre-sprint-plan-gate, companion-surface-post-sprint-results-gate, companion-surface-rule-sync-and-bulk-derivation, manifesto-format-normative-file-pattern-ownership-field, live-e2e-compose-register-resolve-gen-2-agent) across 67 subagents, 96 user messages, and 24 tool errors, all self-recovered with zero permanent data loss. The sprint's core theme: process discipline and layered review (code-review, QA, AVFL, E2E) repeatedly caught real defects before merge, but the sprint's central goal — proving these companion-surface / live-e2e features actually run — was undercut everywhere by the same missing piece: **no live test fixture** (no `nornspun` `agents.json`, `.claude/manifests/`, or completed-sprint sample), which pushed verification for 3+ stories from "run and observe" down to "read and reason," and one 51-turn E2E agent's net-new yield was zero because it rediscovered a gap already known twice over. The sprint's one true incident — the Conductor's end-gate silently swapping out the developer's cmux tab with no presented sign-off ask — is already captured as its own critical-priority story (`conductor-endgate-viewer-hijack-and-silent-gate`) and is **not duplicated** in this audit's action items.

## What Worked Well

- **Layered review caught real, load-bearing bugs before merge.** code-review on companion-surface-post-sprint-results-gate found `paint()` referencing an undefined `STAKES_DECISION_COUNT` constant — a bug that would have silently defeated the anti-rubber-stamp gate protecting the practice's single highest-stakes human decision point — and escalated it for visibility even after fixing it, rather than absorbing it silently.
- **Dual-lens AVFL convergence on real defects, with working noise filters.** Independent reviewers on live-e2e-compose-register-resolve-gen-2-agent (qa-reviewer + code-reviewer) converged on the identical template-not-real-run defect from different evidence paths; code-reviewer's own `bmad-dismiss` layer separately caught and dropped a false positive before it cost a fix cycle.
- **Efficient validators when given inline context.** Three AVFL checkpoint validators for companion-surface-post-sprint-results-gate completed in 2 turns / 0 tool calls each (vs. 51-105 turns elsewhere) by working from injected story text — and still caught a real critical finding (epic_slug mismatch). Worth deliberately preserving as a pattern.
- **Case-sensitive grep trap caught pre-dev by two independent lenses.** A story's own AC verification observable (`companion-surface-rule-sync-and-bulk-derivation`) would have permanently failed self-checks on a correct implementation; Structural and Domain lenses independently caught the identical case-mismatch before dev started.
- **Autonomous stall detection and clean recovery.** The Conductor detected a 32-minute zero-diff stall on the rule-sync dev agent by comparing sibling completion signals (not by reading the stalled transcript), killed it via TaskStop, and re-spawned with a tighter prompt — no lost work, no human needed.
- **Transient infra failures self-healed.** A connection-drop mid-enrichment for the manifesto-format story was cleanly re-run from scratch with zero lasting sprint impact.
- **2 collapsed routine items:** clean two-pass review convergence on the driver-robustness bugs (live-e2e-compose story); 24 of 24 tool errors self-corrected within seconds via the harness's built-in read-before-write safety check.

## What Struggled

- **No live fixture/test harness exists for the companion-surface / live-e2e story family.** This is the sprint's dominant, recurring root cause — see Cross-Cutting Patterns below for the full chain (3 stories, 3+ pipeline stages, one 51-turn E2E agent with zero net-new yield).
- **The pre-sprint plan gate's "CLEAN/95" verdict was a single agent's self-graded read-through, not a true 3-lens adversarial pass.** AVFL's async Agent-tool "mailbox" spawn path did not deliver structured findings from the 3 independent checkpoint validators back to the orchestrator; the consolidator disclosed this honestly as a caveat, but nothing in the pipeline would have caught a differently-behaved orchestrator hiding the gap.
- **Two subagent lifecycles were fully discarded and restarted from zero** (manifesto-format enrichment on a dropped connection; rule-sync on a 32-min stall) — the Conductor's subagent execution path has no checkpoint/resume mechanism, so any interruption re-pays every prior turn.
- **A one-line skill-name typo (`avfl` vs `momentum:avfl`) in create-story/workflow.md:349 guarantees a tool-use error on every run** that reaches the AVFL checkpoint step — confirmed still present in the repo.
- **AVFL pre-build findings against story/spec/contract files have no owner to close them.** STRUCTURAL-001/002 were raised correctly before the build started and are still unresolved in the repo — dev-fixers are scoped to code, and AVFL-on-merge is explicitly forbidden from touching spec/contract files.
- **A dual-lens, HIGH-confidence epic-fit flag from story creation went unactioned through sprint-planning and merge** — companion-surface-pre-sprint-plan-gate shipped under an epic (`momentum-impetus-experience`) that does not list it in `stories[]`.
- **The retro pipeline's own transcript-parsing lost 75% of its per-agent metrics** to a parser that can't handle Python-dict-repr content, forcing this audit to reconstruct tool-efficiency evidence by hand via raw session-file queries.
- **9 additional routine/lower-severity struggles collapsed to a count:** documentation drift between `index.json` and per-story `.md` files on completion (3 stories); a misleading structured-JSON "pass" status contradicted by the dev agent's own trailing prose; a story marked `done` with its headline AC empirically failing in committed evidence; severity miscalibration tagging an AC-defeating bug "minor"; an under-specified WWE contract in a frozen eval.yaml that happens to match the shipped renderer today but isn't pinned; a foreseen risk closed by spec rewording rather than a real mechanism; a backlog stub (`conduct-live-run-against-fixture-sprint`) registered `story_file: true` with no backing file; a 100%-incidence (6/6 agents) read-before-write tool-efficiency miss; and team-messages.jsonl being structurally uninformative for this sprint's fan-out coordination model (not a bug — a signal for future retro auditors).

## User Interventions

Two developer interventions this sprint, both handled cleanly:

1. **End-gate viewer hijack (critical, already actioned).** The developer's cmux session tab was silently replaced by the End-Gate document with no presented sign-off ask — the conductor violated its own `--focus false` spec (used `true` instead), wrongly assumed `cmux browser new` reuses the existing viewer pane (it always splits), and ended its turn without presenting the mandatory approve/request-changes ask. The developer diagnosed the cause themselves, requested a critical intake (`conductor-endgate-viewer-hijack-and-silent-gate` — already filed, do not duplicate), and manually supplied the approval the skill should have solicited.
2. **Next-sprint priority signal.** The developer flagged an explicit standing priority for the next sprint-planning pass: using the subagents feature paired with manifesto/hot-constitution and KB work. Carried forward as a handoff candidate (see below) so it isn't lost to the developer having to restate it.

## Story-by-Story Analysis

**companion-surface-pre-sprint-plan-gate** — Merged, but its entire behavioral contract (SVG diagram render, anti-rubber-stamp JS gate, link-not-inline) shipped on document/structural review alone: QA blocked all 9 ACs on missing-fixture runtime-unverifiability, deferred to Phase-4 E2E, which hit the identical missing-fixture wall and also never ran it. A one-line `avfl` skill-name bug (workflow.md:349) caused a live tool error during its create-story pass. Its AVFL checkpoint's "CLEAN/95" verdict came from a single self-read agent after the 3-lens mailbox spawn failed to deliver findings — disclosed honestly as a caveat. A dual-lens HIGH-confidence epic-fit flag (wrong epic_slug) was never actioned.

**companion-surface-post-sprint-results-gate** — The strongest quality-gate story this sprint: code review caught a critical undefined-constant bug defeating its own anti-rubber-stamp gate, and 3 lightweight inline-context AVFL validators (2 turns each) still caught a real epic_slug mismatch. But it needed 3 review passes to converge, and one "critical" fix (the STAKES_DECISION_COUNT contract) was incomplete on the first attempt, resurfacing at sprint-wide AVFL-on-merge. It also shipped a one-sided contract: retro's Phase 4.5 fused re-render depends on `audit-workflow.js` emitting `process_findings`/`routine_process_count`, which was never implemented — this retro's own Phase 4.5 will silently skip until that follow-up lands. Its eval.yaml under-specifies the WWE+Recommendation card contract relative to what actually shipped. Runtime verification of the whole feature was deferred to E2E and never actually exercised (all 5 ACs BLOCKED) — the one live run that did happen was the viewer-hijack incident above.

**companion-surface-rule-sync-and-bulk-derivation** — On paper the simplest story of the wave; in practice the long pole. Stage-1 dev dispatch used a broad "implement it fully" framing for what was really a small mechanical section-port, and the agent stalled 32 minutes with zero writes before the Conductor's zero-diff heuristic caught it, killed it, and re-spawned with a tighter prompt that finished cleanly in 33 minutes. Pre-dev AVFL caught a case-sensitive grep observable that would have permanently failed self-checks on a correct sync — two independent lenses, same defect, closed before dev.

**manifesto-format-normative-file-pattern-ownership-field** — The story's "determinism over inference" premise rested on 3 of 4 behavioral ACs (verbatim ownership patterns, missing-field signaling, `--touches` resolution) being verified by document reasoning rather than an actual `agents.json`/resolver run, because no fixture existed. A defect where a manifesto flagged invalid at Discover would still complete composition — silently defeating AC5 — was tagged "minor" by code review, though the endgate report itself later called it "was MAJOR." Completion metadata was never written back to the story's own `.md` (still `status: ready-for-dev`, blank Dev Agent Record) despite `index.json` correctly showing `done`. One clean infra self-heal (dropped connection, re-run) had zero lasting impact.

**live-e2e-compose-register-resolve-gen-2-agent** — This story's headline purpose — proving a real running-app composition, not a hand-walked trace — never succeeded: both driver runs failed at the first check (`agents.json not found`), and `.momentum/stories/index.json` still marked it `done`. The stage-1 dev agent's own structured output claimed `"outcome": "pass"` while its own trailing prose admitted the composition step was never executed — a signal any downstream consumer reading only the JSON would miss. A risk flagging exactly this gap was raised at story-creation time (a week prior) and closed only by rewording the spec, not by a mechanism — so it recurred three more times downstream. The driver-robustness bug fixes themselves (7 findings, 6 applied) converged cleanly in one review→fix pass, which is legitimate, working rework rather than thrash.

## Cross-Cutting Patterns

1. **Missing live fixture is the sprint's dominant root cause, spanning 3 stories and 3 pipeline stages.** QA on companion-surface-pre-sprint-plan-gate blocked all 9 ACs on it; the sprint-wide E2E validator (51 turns, the most expensive validator in the sprint) independently rediscovered it and still returned BLOCKED with zero net-new yield; the manifesto-format and live-e2e-compose stories both hit the identical `agents.json`-not-found wall. One fixture story (`conduct-live-run-against-fixture-sprint`) is meant to track this but its backing `.md` file doesn't exist despite `index.json` claiming it does.
2. **Verification deferred rather than resolved, repeatedly.** The QA→E2E deferral chain failed at both ends for the identical reason on two separate stories, and neither stage escalated the repeat — a pattern of quietly re-discovering the same gap rather than closing it or short-circuiting the redundant check once known.
3. **Structured "pass" signals can mask deferred/failed reality.** Both the live-e2e-compose dev agent's self-report and the story's shipped `index.json` status show "done"/"pass" over acknowledged, evidenced failures in the same artifact's prose or in committed evidence files — a generalizable trust risk for any automation reading structured fields without the accompanying narrative.
4. **Story-completion metadata drift between `index.json` and per-story `.md` recurs across at least 3 stories** (manifesto-format, live-e2e-compose, and implicitly others) — the conduct pipeline updates the authoritative index but doesn't write back Dev Agent Record / status / checkbox state to the story file of record.
5. **Read-before-write tool errors hit 100% (6/6) of independent story-authoring/file-sync agents** — self-corrected every time via the harness's safety net, but a shared, foreseeable prompt gap rather than randomness.
6. **The Conductor's stall/interruption recovery is robust in effect but has no cheaper recovery path** — 2 of ~68 agents this sprint were fully discarded and restarted from zero (connection drop; 32-min stall), each re-paying all prior context-gathering turns.

## Metrics

| Metric | Count | Source |
|---|---|---|
| User messages | 96 | `audit-extracts/user-messages.jsonl` |
| Subagents (summarized) | 67 | `audit-extracts/agent-summaries.jsonl` |
| Tool/skill errors | 24 | `audit-extracts/errors.jsonl` |
| Inter-agent team messages | 1 | `audit-extracts/team-messages.jsonl` |
| Stories shipped | 5 | build-ledger.jsonl / stories/index.json |
| Findings surviving verification | 33 | this audit |
| — recommended `keep` (successes) | 8 | this audit |
| — recommended `fix`/`investigate` (struggles) | 25 | this audit |
| User interventions | 2 | User Interventions section above |

## Priority Action Items

1. **[HIGH] Backfill the missing story-stub file for `conduct-live-run-against-fixture-sprint`.** `stories/index.json` (lines 5628-5637) claims `story_file: true` and `priority: high` for this slug, but no `.md` file backs it — the next sprint-planning pass that selects this item will hit a missing-file error instead of context.
   - AC1: `.momentum/stories/conduct-live-run-against-fixture-sprint.md` exists with frontmatter matching the index entry.
   - AC2: Story content specifies the actual live-fixture scope (`agents.json`, `.claude/manifests/`, composed-sprint sample) needed by the 3 blocked stories below.
   - AC3: A bookkeeping check (sprint-manager or create-story) verifies `story_file: true` entries have a backing file before the flag is set.

2. **[HIGH] Harden AVFL's async Agent-tool checkpoint-validator mailbox delivery.** The pre-sprint plan gate's "CLEAN/95" verdict was a single orchestrator's self-graded read-through after the 3 independent lens spawns failed to deliver structured findings back — disclosed honestly this time, but nothing in the pipeline enforces that disclosure.
   - AC1: Structural/Coherence/Domain checkpoint validators deliver findings back to the orchestrator via the mailbox path without a "read the artifacts yourself" fallback.
   - AC2: If mailbox delivery fails, the consolidator surfaces an explicit degraded/BLOCKED state rather than a scored CLEAN/N verdict.
   - AC3: A dry run confirms end-to-end 3-lens finding delivery before the next sprint's plan gate ships.

3. **[HIGH] Stand up a live fixture/test harness for the companion-surface / live-e2e story family.** The same missing-fixture root cause (no `agents.json`, `.claude/manifests/`, or completed-sprint sample) blocked QA on companion-surface-pre-sprint-plan-gate (9/9 ACs), E2E sprint-wide (16/27 scenarios, zero net-new yield on the most expensive validator this sprint), and both live-e2e-compose and manifesto-format story ACs.
   - AC1: A committed `nornspun` fixture provides a real `momentum/agents.json`, `.claude/manifests/`, and a composed sprint sample sufficient to drive sprint-planning → build-guidelines → agent-builder to completion.
   - AC2: Story-level QA/E2E for the 3 affected stories can report PASS/FAIL against the fixture instead of BLOCKED-on-missing-fixture.

4. **[HIGH] Fix retro's `audit-workflow.js` to emit `process_findings`/`routine_process_count`.** retro/workflow.md:304-305 documents the contract, but the producer script was never updated — this sprint's own retro Phase 4.5 fused re-render will silently skip and fall back to "review separately" until it's wired up.
   - AC1: `skills/momentum/skills/retro/audit-workflow.js` emits both fields per the documented contract.
   - AC2: A retro run against a real sprint produces the fused re-render instead of the fallback path.

5. **[MEDIUM] Fix the `avfl` → `momentum:avfl` skill-name typo at `create-story/workflow.md:349`.** Confirmed still present; causes a guaranteed `Unknown skill` tool-use error on every create-story run that reaches the AVFL checkpoint.
   - AC1: The line invokes `momentum:avfl`.
   - AC2: A create-story run reaching the AVFL checkpoint produces zero `Unknown skill` errors.

6. **[MEDIUM] Assign an owner for closing AVFL pre-build findings against story/spec/contract files.** STRUCTURAL-001 (duplicate `harness_profile` key, 3 eval.yaml files) and STRUCTURAL-002 (change_type/Dev-Notes mismatch) were raised correctly pre-build and remain unresolved — no pipeline stage currently has both the authority and the mandate to close them.
   - AC1: A named stage (sprint-planning, epic-grooming, or a new remediation step) is documented as accountable for spec/contract-file AVFL findings.
   - AC2: The 2 outstanding findings above are resolved in the repo.

7. **[MEDIUM] Reassign `companion-surface-pre-sprint-plan-gate`'s epic_slug.** A dual-lens HIGH-confidence flag at story creation ("this slug isn't in `momentum-impetus-experience`'s stories[]") went unactioned through sprint-planning and merge.
   - AC1: The story's epic_slug is corrected to an epic that lists it in `stories[]` (or the epic's `stories[]` is updated to include it).
   - AC2: epic-grooming or sprint-planning gains a check for unresolved "flagged, not changed" epic-fit findings before a story is selected into a sprint.
