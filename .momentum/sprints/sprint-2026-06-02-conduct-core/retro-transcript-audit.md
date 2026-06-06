# Sprint Transcript Audit — sprint-2026-06-02-conduct-core

## Executive Summary

This sprint built the **Conductor** engine spine — the in-session sprint-build orchestrator that runs per-story pipelines, AVFL-on-merge, and a single human end-gate — across 21 stories. Every story merged with `qa_verdict=PASS` and `freeze=MATCH`, zero blocked, zero escalation thrash. The build's quality ledger is strong: 105 finding cards (≈93 fixed, 7 dismissed, 1 escalated, 4 triaged-out) over a build-results stream of 96 findings / 87 fixed. The single escalated card — a nested-vs-flat `timing_tier` field-shape mismatch between the fixer and the Conductor that made the mid-flight-vs-end-gate routing branch structurally unreachable — is precisely the cross-file integration defect the AVFL-on-merge pass exists to catch. The gate stack worked, and the central conduct thesis held: the developer approved crisply when the agent operated at decision-grade altitude (options, plain framing) and grew frustrated when it surfaced internal counts and jargon ("52 stories," beads, stubs, judgment calls) without a plain-language anchor.

Three classes of problem dominate the findings, orthogonal to the build's clean convergence:

1. **Human-facing communication-altitude gaps in the planning/decision sessions.** Eight distinct developer confusion messages and three repeated scope-boundary re-assertions ("Planning is out of scope") show the orchestrator presenting its own working vocabulary instead of decision-grade framing. Ironically, the sprint whose purpose was *not* overwhelming the HITL repeatedly overwhelmed the HITL.

2. **Two-sided contract / seam defects that per-story review structurally cannot see.** The fixer↔Conductor hand-off contract was authored in incompatible halves (nested vs flat field shapes, an undefined `finding_id` correlation key, thin disposition objects that starve downstream triage). Per-story gates passed each half in isolation; only the cross-file AVFL pass caught the seam — and it carried two MAJOR state-machine defects out of the sprint unfixed.

3. **Bookkeeping and gate-design gaps inside the otherwise-healthy build.** A scope-discipline revert silently undid a correct fix while the scorecard still reported 5/5 fixed; story specs seeded wrong spec-section citations and under-scoped touch lists that the dev faithfully propagated; the end-gate report collapsed rich finding detail into terse scorecard shorthand that violated its own self-sufficiency mandate; and the finding `type`/`severity` ledger fields are free-text, defeating aggregate queries.

A critical caveat scopes this entire audit: the **audit-extract harvest captured the wrong session set.** `team-messages.jsonl` is empty (0 lines), and all 7 `agent-summaries.jsonl` records are from the 2026-05-31 AES-004 assessment / HITL-research wave — not the 2026-06-04 conduct build. The build's dev/QA/code-review/AVFL/fix-cycle activity had to be reconstructed from build-results JSONL, finding-cards JSON, story-diffs, and git history rather than from any captured transcript. The efficiency and coordination lenses are therefore structurally blind to the population they most need to see.

## What Worked Well

**The layered gate stack caught real defects at every level (KEEP).**
- *What happened:* Per-story adversarial review caught internal contradictions and spec drift; the AVFL-on-merge pass caught a genuine cross-file contract incompatibility no single-story reviewer could see.
- *Evidence:* 17 HIGH-severity findings across the sprint, all real (16 fixed, 1 escalated, 0 dismissed as false positives). The lone escalated card — "The fixer and the Conductor built incompatible halves of the same hand-off contract" — was correctly classed `high-blast-radius-architecture` and caught only by the cross-file AVFL pass.
- *Root cause:* Layered review (claim-checklist QA + adversarial per-story + AVFL-on-merge) provides orthogonal coverage; the integration seam is only visible at merge.
- *Recommendation:* KEEP. This is the gate doing exactly its designed job; near-zero high-stakes false-positive rate this sprint.

**The bounded recheck loop is load-bearing — it caught fix-induced regressions (KEEP).**
- *What happened:* 12 of 18 rechecked stories returned REFIXED — the first fix missed or introduced a defect the recheck caught. Several were new HIGH-severity regressions injected by the first fix.
- *Evidence:* `dev-strip-merge-cleanup-authority` — fixer invented a Conductor lock duty the spec explicitly deleted (REFIXED, commit aa929a0). `conduct-preflight-halts` — a fix hardcoded a wrong H5 status enum that would false-HALT a normally-statused story (major residual, fixed 2873b2a). `stage3-fix-loop-via-directed-dev` and `conduct-build-phase-frontier` — fixes introduced invalid `--target blocked` transitions caught at recheck.
- *Root cause:* Fixers reason about where authority/behavior moved without re-reading the governing spec section; the recheck step is the net. One fix pass is demonstrably insufficient for this class of work.
- *Recommendation:* KEEP. (Caveat: assessed from build artifacts, not the absent build transcript.)

**False-positive discrimination is sound — the gate is not rubber-stamping (KEEP).**
- *What happened:* 9 build-leg dismissals plus 7 dismissed finding cards, each carrying an explicit scoped rationale tied to the finding's own words or to scope boundaries.
- *Evidence:* `conduct-contract-freeze-check` dismissal ("the finding itself states this is a defensible and arguably better reading"); `code-review-adapter-normalize-triage` model-pin ("pre-existing and not touched by this story's diff"); `qa-reviewer-rescope` slash-vs-hyphen names ("only in human-prose tables, not in any diff hunk").
- *Root cause:* The finding schema forces evidence-grade output with a non-empty disposition rationale (DEC-036 D-rule).
- *Recommendation:* KEEP. Correct counter-pressure against over-fixing out-of-scope or pre-existing issues.

**The Conductor's scope-enforcement guardrail fired correctly every time (KEEP, but see struggle).**
- *What happened:* At least 5 stories had a fixer/dev edit to a story-spec file or a sibling workflow reverted by the Conductor before merge.
- *Evidence:* `dev-read-contract-part-a-header`, `conduct-preflight-halts`, `conduct-coverage-disposition-branch`, `code-review-adapter-retire-stub`, `stakes-classification-rubric` all record a Conductor scope-revert.
- *Root cause:* Healthy integration-time scope discipline catches dev agents that "helpfully" edit adjacent files.
- *Recommendation:* KEEP the guardrail. (The recurrence itself is a struggle — see "What Struggled.")

**The fan-out coordination contract held across all 21 stories (KEEP).**
- *What happened:* Every story flowed Conductor → dev → Conductor → code-reviewer → directed fixer with `freeze=MATCH` every time, no blocked waits, no stuck fix loops, no deadlock or starvation across 6 dependency waves.
- *Evidence:* build-results: 21/21 PASS+MATCH, escalated sum 0, no re-open churn; dependency-wave distribution {1:1, 2:2, 3:7, 4:5, 5:4, 6:2}.
- *Root cause:* Contract-driven (finding-card/gate-verdict) coordination rather than message-driven; dependency-frontier sequencing.
- *Recommendation:* KEEP.

**DEC-035/DEC-036 autonomy intent was honored — zero mid-build human gates (KEEP).**
- *What happened:* No per-story HALT fired; the developer was interrupted exactly once, at the single end-gate, plus the one deliberate D1 architecture escalation.
- *Evidence:* `code-review-adapter-noninteractive-driver` auto-fixed a routine/mid-flight critical config-worktree bug without escalating; `directed-fix-invocation-contract` correctly escalated its one architecture seam to the end-gate ("approve with your recommendation").
- *Root cause:* The single-end-gate model worked as specified — the practice's central bet validated live.
- *Recommendation:* KEEP. The clustered "adopt" approvals confirm the model works when framing is decision-grade.

## What Struggled

**Communication altitude — sustained sprint-long jargon/altitude mismatch (FIX).**
- *What happened:* The developer expressed comprehension breakdown in eight separate messages over the sprint window, repeatedly hitting dense internal vocabulary (per-leg amendments, judgment calls, stubs, "52 stories," "Pre-flight HALTs H1-H5," beads).
- *Evidence:* "[13] What are the strange symbols all over the document?"; "[44] I'm sorry I'm totally lost what is happening here? What is the 52 stories?"; "[85] I really don't understand what the judgment calls... beads... is all about."
- *Root cause:* The orchestrator presents its own working vocabulary instead of decision-grade, plain-language framing — and there is no durable altitude guardrail across sessions/handoffs.
- *Recommendation:* FIX. Decision-grade framing rule for HITL-facing prompts; ban internal counts/jargon without a plain anchor.

**Scope-creep — planning kept getting folded into a conduct-scoped effort (FIX).**
- *What happened:* The developer had to re-assert the same scope boundary at least three times across three days.
- *Evidence:* "[27] Planning is out of scope... What am I missing that you continue to bring this up???"; "[52] I feel like I'm going nuts with the LLMs pushing me to handle the planning as part of this."; "[23] Planning is a different epic."
- *Root cause:* No durable scope guardrail survives across sessions/handoffs; each fresh session re-imports planning concerns.
- *Recommendation:* FIX. Persist explicit scope boundaries in handoff state; load and honor them at session start.

**Two-sided contract seam authored incompatibly (FIX — partially actioned).**
- *What happened:* The fixer↔Conductor hand-off contract was built in incompatible halves: the fixer emits `escalation.timing_tier` (nested) while the Conductor reads flat `F.timing_tier`/`F.stakes_class`, making the mid-flight routing branch dead. The correlation key `finding_id` was never defined in the contract doc that exists to define the seam. Triaged-out findings reach triage with only a `finding_id` and no description.
- *Evidence:* Escalated card (high-blast-radius-architecture); cards 6/9/10 of the AVFL pass; `directed-fix-invocation-contract.md` lacked a "Canonical Fixer Output Shape" section until post-merge commit 36712a6.
- *Root cause:* Per-story review cannot see a producer in one story and consumer in another; the seam concentrates exactly where no single-artifact reviewer looks. The 12 ACs specified WHAT fields exist but not their canonical JSON nesting.
- *Recommendation:* FIX. Pin canonical wire shapes in seam contracts; two-sided contract stories need a paired-review scope. (A `contract-seam-stories-two-sided-review-scope` stub was already intaked.)

**Found-but-not-fixed leak — two MAJOR state-machine defects shipped unfixed (FIX).**
- *What happened:* The AVFL residual pass carried 4 findings "identified but not dispositioned in the fix loop," two MAJOR, both triaged-out (deferred, not fixed): an illegal terminal-to-terminal status transition at approve, and approve jumping merged stories review→done while skipping the required verify state (rejected by the state machine at runtime).
- *Evidence:* AVFL "— residual" card set; grep of `.momentum/stories/*.md` for these topics returns no dedicated follow-up story.
- *Root cause:* The fix loop terminated before dispositioning everything it surfaced; the residual sweep chose triaged-out over fixed for MAJOR bugs with no backlog-stub linkage — "deferred" risks meaning "forgotten."
- *Recommendation:* FIX. The two MAJOR runtime-rejected transitions need a follow-up story now.

**Scorecard cannot be trusted as a record of what merged (FIX).**
- *What happened:* `conduct-preflight-halts` reports `fixed: 5/5` and a §8-citation card `disposition: fixed`, yet the Conductor scope-revert (5ca370f) silently restored the bad §8 citation; the merged story file still reads the erroneous text.
- *Evidence:* Revert diff restores the bad line; `.momentum/stories/conduct-preflight-halts.md:89` still wrong. Same pattern in `code-review-adapter-retire-stub` (fix to story-doc reverted at merge; card says "fixed," main still has the dangling pointer).
- *Root cause:* Collision between the Conductor's scope-discipline sweep (build agents must not mutate their own story file) and the directed-fix loop — when a real defect lives in the story spec, the fixer's correct repair gets blanket-reverted, and neither the card nor the scorecard is reconciled.
- *Recommendation:* FIX. Reconcile scope-reverts against finding dispositions; route story-spec defects to a sanctioned owner instead of letting the fixer edit-then-lose them.

**Story-spec quality seeds defects the dev faithfully propagates (FIX / INVESTIGATE).**
- *What happened:* Specs seeded wrong spec-section citations (cite-by-number without opening the section) and under-scoped touch lists, which the dev implemented faithfully.
- *Evidence:* `dev-strip-merge-cleanup-authority` — Dev Notes cited "section 12" for content in "section 6"; five wrong citations propagated (HIGH). Same story's `touches` omitted `SKILL.md`, leaving the public description advertising removed behavior (HIGH). `dev-read-contract-part-a-header` — dangling "section 10" repeated 3×; an AC contradicting the spec's own Part-A/Part-B boundary. `code-review-adapter-repoint-quick-fix` — `touches` omitted the co-located eval that the same edit invalidated.
- *Root cause:* Story-authoring (create-story / contract-authoring) quality gap: cite-by-number, incomplete blast-radius enumeration for multi-file agent surfaces (dev.md + workflow.md + SKILL.md + evals).
- *Recommendation:* FIX. Verify cited section numbers at authoring time; enumerate the full agent/eval surface in `touches`.

**End-gate report under-served the build it summarized (FIX).**
- *What happened:* The orchestrator collapsed each story's rich finding detail/evidence into a one-line scorecard label, violating DEC-036 D5's per-section self-sufficiency mandate the report itself enforces.
- *Evidence:* Developer pushback "[00:03] What's going on here? Why is there not more context?" on `dev-fix-mode-entry` / `stage3-fix-loop-via-directed-dev`; orchestrator conceded "my scorecard rows are exactly the terse shorthand / no see-code the mandate bans," triggering a full report rebuild. An `end-gate-rendering` intake stub already exists.
- *Root cause:* The renderer summarized rather than reconstructed per-finding narratives from the reviewers' real detail.
- *Recommendation:* FIX. End-gate renderer must reconstruct per-finding cards from reviewer evidence, not paraphrase into a label.

**Dev agents repeatedly stray outside their write scope (FIX).**
- *What happened:* 5 of 21 stories (24%) required a Conductor revert of a dev/fixer edit to a file the story didn't own — usually the story's own spec file or a hot sibling workflow.
- *Evidence:* `dev-read-contract-part-a-header`, `conduct-coverage-disposition-branch`, `code-review-adapter-retire-stub`, `stakes-classification-rubric`, `conduct-preflight-halts`.
- *Root cause:* The dev/fixer spawn contract under-constrains write scope; fixers' instinct on a cross-artifact finding is to fix the consumer in-place.
- *Recommendation:* FIX. Tighten the write-scope constraint in the dev spawn prompt; pre-merge story-file revert is a band-aid, not a fix.

**Duplicated diff-range defect across sibling agents (FIX / INVESTIGATE).**
- *What happened:* The same HIGH per-story diff-range bug was independently re-authored in two repoint stories; one took three fix attempts (two empty three-dot diffs) before converging.
- *Evidence:* `code-review-adapter-repoint-sprint-dev` ("tip-relative ~N wrong; fix bounced twice then CONVERGED to pre_merge_sha pattern") and `code-review-adapter-repoint-quick-fix` ("main~1..main only last commit"). `qa-reviewer-rescope` had a third variant (`main...HEAD` over-scoping).
- *Root cause:* No shared, vetted diff-range helper/reference; each call site rediscovered the merge-boundary `pre_merge_sha` pattern. "Pure repoint" stories that synthesize a diff range are not trivial.
- *Recommendation:* FIX. Extract a shared diff-range reference/helper; stop pre-classifying adapter-migration stories as trivial wiring.

**Escalation machinery is essentially unexercised (INVESTIGATE).**
- *What happened:* The sprint's centerpiece stakes-and-timing escalation engine fired exactly once, only in the post-merge AVFL pass; the per-story mid-flight path was never triggered by a real finding.
- *Evidence:* Across 105 cards: `stakes_class` is 104 routine / 1 high-blast-radius-architecture; `timing_tier` is 100% end-gate-expanded; escalated=1. `stage3-fix-loop-via-directed-dev` verification was inspection-only (markdown, no live runner).
- *Root cause:* The machinery was confirmed by reading, not running; its correctness rests on review rather than exercise.
- *Recommendation:* INVESTIGATE. Drive a real stakes-class finding through the mid-flight loop end-to-end before trusting it.

**Free-text ledger fields defeat aggregate queries (FIX).**
- *What happened:* Finding `type` is free-text (20+ distinct strings across 105 cards: "internal-contradiction" vs "internal-contradiction / AC-violation"; "broken-cross-reference" vs "broken cross reference"). build-results schema also drifted mid-build (3 rows structured `gates`, 18 rows prose `key`).
- *Evidence:* near-duplicate type categories; finding-cards keyed by slug but two real stories (`conduct-spec-revision-dec036`, `stakes-classification-rubric`) have no card key while two non-story prose keys exist.
- *Root cause:* `type`/`severity` are not controlled enums; the card ledger and build-results ledger disagree on which work units exist.
- *Recommendation:* FIX. Controlled enums for `type`/`severity`; stable build-results schema; join card/build ledgers on a single key.

**Instrumentation harvest captured the wrong session window (FIX).**
- *What happened:* `team-messages.jsonl` is empty and all 7 `agent-summaries.jsonl` records are from the 2026-05-31 assessment/research wave, not the 2026-06-04 build.
- *Evidence:* 0-line team-messages; agent first-prompts are AES-004 discovery auditors / HITL research synthesists.
- *Root cause:* The audit-extract harvester keyed on the prior planning session, not the build session; fan-out coordination has no SendMessage channel to populate team-messages by design.
- *Recommendation:* FIX. Harvest must key on the build session window; add a build-wave coordination record for fan-out sprints.

## User Interventions

The 87 user messages cluster into four interaction modes:

1. **Confusion / altitude breakdown (8 messages, high signal):** [13] mojibake symbols, [27]/[52]/[23] planning-scope, [32] Pre-flight HALTs, [44] "what is the 52 stories?", [69] per-leg amendments, [85] judgment calls / stubs / beads. These cluster at the planning/decision stage, never during a build. Root cause: internals-grade framing reaching the HITL.

2. **Scope re-assertion (3 messages):** [27], [52], [23] — the developer repeatedly pushing planning back out of conduct's scope. A durable cross-session scope guardrail is missing.

3. **Decision-grade approval (clustered, healthy):** [26] "move forward with our plan for conduct"; [53] "Yes that sounds perfect"; [50] "OK that looks good"; [55]-[58] four consecutive "adopt" confirmations. The contrast with the confusion cluster is the sprint's central evidence: the practice works at decision-grade altitude and fails at internals-grade.

4. **Status chasing / deliverable re-requests:** [76] "Did you finish?", [77] "Where are you now?", [83] "Try again", plus repeated HTML-report asks ([9], [15], [21], [29], [41], [63], [74]). The end-gate HTML render was not a dependable automatic output, so the human carried the burden of remembering and re-requesting it.

**Conceptual load came from the human, not the agent.** The whole epic's framing — "Specification Fatigue" [59], the four escalation categories (security/irreversible/migration/blast-radius) [52], and "surface context with the decision" — was authored by the developer. Preserve [59] as the canonical DEC-036 rationale.

**Healthy HITL contract practiced live.** [61] "I can't confirm it, if it's high risk please do some discovery and confirm yourself" plus [38] "imagine we are working with a Junior developer... I can trust them to make good decisions" — the developer declined to rubber-stamp what they could not verify and directed the agent to self-verify, validating the DEC-036 direction. The single D1 architecture escalation ("approve with your recommendation") is this contract working end-to-end.

**Build-time interventions were near-zero**, exactly as DEC-035 intends. The only build-window messages were a sprint-wide review-design AskUserQuestion (answered after an overnight pause), a "Is it stuck?" latency check, and the end-gate report-quality pushback — none were per-story build corrections.

**One-off corrections hardened into rules.** [10]/[11]/[12] — the agent clobbered a viewer pane the developer was reading; the developer turned it into a durable cmux rule change. Good practice-hardening loop, but the underlying cmux viewer-pane handling keeps reproducing this failure across sessions.

## Story-by-Story Analysis

All 21 stories merged PASS/MATCH. The rollup below groups by outcome; `round` is the dependency wave, not a retry count.

**Clean single-pass convergence (no thrash, low/medium findings only):**
- `conduct-skill-scaffold-and-spine` — 2-pass; code-review caught a HALT-on-conflict that contradicted the "never HALT" invariant (QA missed it).
- `directed-fix-finding-schema` — 1 fix round; code-review caught an unreachable `triaged-out` disposition that QA's presence-checklist passed.
- `directed-fix-invocation-contract` — 1 minor finding in-build; but shipped a latent under-specified seam (canonical wire shape unpinned) that surfaced post-merge as escalation D1.
- `stakes-classification-rubric` — 1 low finding; the rubric immediately exposed a divergent mid-flight bar in an already-merged consumer (its single-source-of-truth value working).
- `conduct-coverage-disposition-branch` — 1 review-fix-recheck loop; merge contention on `conductor/workflow.md` + a story-file scope revert.
- `code-review-adapter-noninteractive-driver` — 3 review rounds; adversarial review caught a CRITICAL fail-closed-on-every-worktree config bug that QA's prose-check passed (P0 purpose would have been defeated).
- `code-review-adapter-normalize-triage` — caught a HIGH AC1 violation (bmad bucket stuffed into the schema `verdict` field); 1 sound dismissal.
- `qa-reviewer-rescope-per-story-contract` — clean in-build, but the AVFL pass caught the story's OWN core invariant violated (`main...HEAD` over-scoping the diff it was rescoped to isolate).
- `code-review-adapter-retire-stub` — pure plumbing; report claims a story-doc fix that was reverted at merge (false "fixed").
- `code-review-adapter-repoint-quick-fix` — 1 fix pass; all 4 findings traced to one faulty diff line; sibling eval left stale.

**Converged but with fix-induced regression caught by recheck (REFIXED):**
- `dev-strip-merge-cleanup-authority` — fixer invented a Conductor lock duty the spec deleted; HIGH spec-citation + HIGH incomplete-touches (`SKILL.md`) both seeded by the story spec; real content merge conflict resolved semantically (validated the story's own thesis).
- `conduct-preflight-halts` — one of the most-reworked stories (2 review rounds + recheck, 8+ defects); fix hardcoded a wrong H5 status enum; scorecard reports 5/5 fixed while a §8 citation persists unfixed on main.
- `conduct-build-phase-frontier` — fix introduced an invalid `--target blocked` transition; bugs clustered on momentum-tools status-transition semantics; a self-referential gap where build-invalidating findings bypassed the escalation hook.
- `stage3-fix-loop-via-directed-dev` — fix introduced invalid `--target blocked`; caught a real BLOCKED-stories-merged-anyway spec contradiction; verification was inspection-only on the escalation channel it builds.
- `dev-fix-mode-entry` — dropped the AC3 legitimacy gate (would flood the end-gate with false-positive escalations); 4/5 findings were schema vocab drift; concrete trigger for the end-gate-report-quality pushback.
- `conduct-stakes-timing-escalation-mechanism` — HIGH: keyed the escalation bar on a non-existent `escalation_reason` field (nearly dead code); 2 low residuals at recheck; the central seam story whose latent defect later escalated.
- `conduct-merge-and-conflict-resolution` — 2 full review→fix cycles (unconditional `--abort` discarding resolution; quarantine falling through into success); hard-coded an absolute line number that went stale post-merge.
- `dev-read-contract-part-a-header` — self-inflicted refix (a fix added a guard contradicting the governing spec); spec-quality defects (dangling "section 10", contradictory AC).
- `conduct-contract-freeze-check` — 2 adversarial cycles (5→1→0); HIGH unwired call-site (freeze check was dead code) caught by review, missed by QA.

**Multi-bounce convergence:**
- `code-review-adapter-repoint-sprint-dev` — highest-iteration leg (round 6, fix bounced twice on empty three-dot diffs before converging to `pre_merge_sha`); "pure repoint" framing masked net-new diff-generation machinery.

**Upstream (pre-build) story:**
- `conduct-spec-revision-dec036` — section-scoped revision of a document-wide policy change kept surfacing stragglers across §2/§3/§6/§10; F5 slash-form tokens marked "resolved" but resurfaced at the integration layer.

## Cross-Cutting Patterns

**Pattern 1 — Per-story review is structurally blind to two-sided contracts and how-it-runs invariants.** Recurs across the coordination, review, execution, and per-story lenses. The fixer↔Conductor seam (nested vs flat), the undefined `finding_id` key, the thin disposition object, the `qa-reviewer` over-scoped diff, the `directed-fix-invocation-contract` unpinned wire shape — all passed every per-story gate and were caught only at AVFL-on-merge (or escaped entirely as residuals). PASS-on-every-story ≠ a working integrated system. This is the single most important structural finding.

**Pattern 2 — Fixers regress while fixing, and one fix pass is insufficient.** 71% REFIXED rate. Fixers reason about where authority/behavior moved without re-reading the governing spec section (invented Conductor lock duty; wrong H5 enum; invalid `--target blocked` ×3; over-corrected scope guards). The recheck loop is load-bearing precisely because of this — but it doubles fix-stage cost on most stories.

**Pattern 3 — Story-spec authoring seeds downstream defects.** Cite-by-number without opening the section, incomplete `touches` enumeration for multi-file agent surfaces, section-scoped revisions of document-wide changes, and "pure wiring / trivial" framing that masked real traps. The dev faithfully implemented internally-inconsistent specs; code-review had to reconcile the spec, not the code. Points upstream to create-story / contract-authoring.

**Pattern 4 — Communication altitude bifurcates outcomes.** Frustration clustered on internals-grade framing (jargon, raw counts); approval clustered on decision-grade framing (options, plain stakes). Same root cause surfaced at the end-gate-report layer (terse scorecard shorthand violating the self-sufficiency mandate).

**Pattern 5 — Bookkeeping diverges from reality.** Scope-reverts silently undo correct fixes while scorecards report them fixed; free-text `type`/`severity` defeat aggregation; card and build-results ledgers disagree on which stories exist; the audit harvest captured the wrong session. The audit trail cannot be trusted as a record of what merged or what ran.

**Pattern 6 — Hot-file contention on `conductor/workflow.md`.** ~6 sibling stories edit one keystone file, producing recurring merge conflicts (resolved cleanly, but at extra spawn cost) and one stale hard-coded line reference. The dominant source of per-story merge overhead and an artifact of slicing one spine into many parallel worktree stories.

## Metrics

| Metric | Value |
|---|---|
| User messages | 87 |
| Subagent summaries (captured) | 7 (all from 2026-05-31 assessment/research wave, NOT the build) |
| Errors logged | 8 (all pre-build 2026-05-29..06-02; none recur in the build) |
| Team messages | 0 (empty file; fan-out has no SendMessage channel by design) |
| Stories | 21 (all merged PASS/MATCH, 0 blocked) |
| Dependency waves (rounds) | 6 (dist {1:1, 2:2, 3:7, 4:5, 5:4, 6:2}) |
| Findings (build-results) | 96 total / 87 fixed / 9 dismissed / 0 escalated in-band |
| Finding cards | 105 (≈93 fixed, 7 dismissed, 1 escalated, 4 triaged-out) |
| HIGH-severity findings | 17 (16 fixed, 1 escalated, 0 false-positive) |
| Recheck distribution | REFIXED 12, CLEAN 5, n/a/blank 4 (71% REFIXED of rechecked) |
| Stakes routing exercised | 104 routine / 1 high-blast-radius-architecture; mid-flight fired 0× per-story |
| Scope-discipline reverts | 5 of 21 stories (24%) |
| Findings (struggles) | 27 (FIX/INVESTIGATE) |
| Findings (successes) | 36 (KEEP) |

## Priority Action Items

1. **Two MAJOR state-machine defects shipped unfixed — create follow-up story now** — priority: **critical**
   - *source_detail:* AVFL "— residual" card set: illegal terminal-to-terminal status transition at approve; approve jumps merged stories review→done skipping the required verify state (rejected by the state machine at runtime). Both triaged-out with no backlog linkage.
   - *suggested ACs:* Identify both runtime-rejected transitions in `conductor/workflow.md`; fix the approve path to route merged stories review→verify→done; add a guard preventing terminal-to-terminal transitions; add an eval scenario per defect; no residual carries a MAJOR severity out of a future sprint without a linked stub.
   - *epic_slug:* conduct-core

2. **End-gate scorecard silently diverges from what merged — reconcile reverts against dispositions** — priority: **high**
   - *source_detail:* `conduct-preflight-halts` reports 5/5 fixed while the §8 citation persists on main (scope-revert 5ca370f undid the correct fix); `code-review-adapter-retire-stub` card says "fixed" but the dangling pointer remains on main.
   - *suggested ACs:* When the Conductor reverts a worktree edit, cross-check it against open finding dispositions; if a reverted edit was a finding's fix, re-classify to "deferred" with a backlog stub rather than "fixed"; story-spec defects route to a sanctioned owner instead of fixer edit-then-lose; scorecard reflects only what reached main.
   - *epic_slug:* conduct-core

3. **Pin canonical wire shapes for two-sided contracts; add paired-review scope** — priority: **high**
   - *source_detail:* Fixer↔Conductor seam authored in incompatible halves (nested `escalation.timing_tier` vs flat `F.timing_tier`); `finding_id` correlation key undefined in the contract doc; thin disposition object starves triage. Caught only at AVFL; one item escalated, one item's producer-side left open.
   - *suggested ACs:* Seam contracts include a "Canonical Output Shape" section with exact JSON nesting; define `finding_id` (assigner, uniqueness scope, lifetime); stories authoring opposite halves of one contract are co-reviewed against both halves before merge; QA gate checks producer-emitted fields against consumer-read fields.
   - *epic_slug:* conduct-core

4. **Tighten dev/fixer write-scope; stop story-spec edit-then-revert** — priority: **high**
   - *source_detail:* 5 of 21 stories (24%) required a Conductor revert of an out-of-scope edit to the story file or a hot sibling workflow; fixers' instinct on cross-artifact findings is to fix the consumer in-place.
   - *suggested ACs:* Dev/fixer spawn prompt enumerates the exact writable file set and forbids editing the story `.md` and sibling stories' files; a cross-artifact finding routes to a reconciliation note for the owning story; revert rate falls below 10% of stories.
   - *epic_slug:* conduct-core

5. **Fix story-spec authoring quality (cite-by-number, incomplete touches)** — priority: **high**
   - *source_detail:* `dev-strip-merge-cleanup-authority` seeded 5 wrong "section 12" citations and omitted `SKILL.md` from `touches`; `dev-read-contract-part-a-header` dangling "section 10" ×3; `code-review-adapter-repoint-quick-fix` omitted the co-located eval; "pure wiring / trivial" framing masked diff-range traps.
   - *suggested ACs:* create-story verifies every cited spec-section number against the live spec before commit; `touches` enumerates the full agent surface (agent.md + workflow.md + SKILL.md + co-located evals); adapter-migration/repoint stories are not pre-classified as trivial; document-wide policy changes are not scoped by section number.
   - *epic_slug:* conduct-core

6. **End-gate report must reconstruct per-finding narratives, not paraphrase** — priority: **high**
   - *source_detail:* Orchestrator collapsed rich finding detail into one-line scorecard labels, violating DEC-036 D5 self-sufficiency; developer pushback forced a full report rebuild. An `end-gate-rendering` stub exists.
   - *suggested ACs:* End-gate renderer emits per-finding cards built from the reviewers' real `detail`/`evidence`; no scorecard row uses terse "see-code" shorthand; each section is self-sufficient (readable without watching the build); HTML report is an automatic, dependable end-of-cycle output (no human re-request).
   - *epic_slug:* conduct-core

7. **Decision-grade altitude guardrail for HITL-facing prompts** — priority: **high**
   - *source_detail:* 8 developer confusion messages on internal jargon ("52 stories," beads, stubs, per-leg amendments, Pre-flight HALTs); approval clustered only at decision-grade framing.
   - *suggested ACs:* HITL prompts lead with the plain-language question + stakes; internal counts/jargon banned without a plain anchor; decision context travels with the decision (no "reference other material"); a lint flags raw internal vocabulary in developer-facing output.
   - *epic_slug:* conduct-core

8. **Persist scope boundaries across sessions** — priority: **medium**
   - *source_detail:* Developer re-asserted "planning is out of scope" at least 3× across 3 days; no guardrail survived handoffs.
   - *suggested ACs:* Explicit scope boundaries are written into handoff state at session end; session start loads and honors them; an agent proposing out-of-scope work against a recorded boundary self-corrects before surfacing it.
   - *epic_slug:* conduct-core

9. **Extract a shared diff-range reference/helper** — priority: **medium**
   - *source_detail:* The same HIGH `pre_merge_sha` merge-boundary diff bug was re-authored in 2 repoint stories + a 3rd `qa-reviewer` variant; one took 3 attempts (2 empty three-dot diffs) to converge.
   - *suggested ACs:* A single vetted diff-range pattern (capture `pre_merge_sha` at the merge point; two-dot `{{pre_merge_sha}}..story/{slug}`) is documented once and cited by every per-story review call site; fixes are validated against the workflow's concrete merge mechanics (rebase-then-ff), not the abstract git model.
   - *epic_slug:* conduct-core

10. **Controlled enums + stable ledger schema for finding cards / build-results** — priority: **medium**
    - *source_detail:* 20+ free-text `type` strings (near-duplicates); build-results schema drifted (3 structured rows vs 18 prose); card ledger and build-results disagree on which stories exist (two stories have no card key).
    - *suggested ACs:* `type` and `severity` are controlled enums; build-results uses one stable schema across all rounds; both ledgers join on a single canonical key (story slug); a consumer joining them loses no stories.
    - *epic_slug:* conduct-core

11. **Exercise the escalation machinery end-to-end before trusting it** — priority: **medium**
    - *source_detail:* The stakes-and-timing engine fired exactly once (post-merge AVFL only); per-story mid-flight never triggered by a real finding; `stage3` verification was inspection-only.
    - *suggested ACs:* A runtime/eval test drives a real stakes-class finding through the mid-flight loop; the end-gate-expanded vs mid-flight branch is exercised with both timing tiers; the bound-exhausted (BLOCKED) and escalated dispositions are each driven through the loop at least once.
    - *epic_slug:* conduct-core

12. **Audit-extract harvest must key on the build session window** — priority: **medium**
    - *source_detail:* `team-messages.jsonl` empty; all 7 `agent-summaries` from the prior assessment wave, none from the build; efficiency/coordination lenses were blind.
    - *suggested ACs:* The retro harvester selects the build session window (not the most recent planning session); fan-out sprints emit a build-wave coordination record (spawn prompts + return signals); the harvest validates that captured agents overlap the sprint's merge timestamps.
    - *epic_slug:* conduct-core
