# Sprint Transcript Audit — sprint-2026-06-02-conduct-core

## Executive Summary

This sprint built the **Conductor** engine spine — the in-session sprint-build orchestrator that runs per-story pipelines, AVFL-on-merge, and a single human end-gate — across 21 stories, all of which merged with `qa_verdict=PASS` and `freeze=MATCH`, zero blocked. The build's own quality ledger is strong: 105 finding cards (93 fixed, 7 dismissed, 1 escalated, 4 triaged-out) and a build-results stream of 96 findings / 87 fixed with **zero escalation thrash**. The single escalated card — a nested-vs-flat `timing_tier` field-shape mismatch between the fixer and the Conductor that made the mid-flight-vs-end-gate routing branch structurally unreachable — is exactly the cross-file integration defect the AVFL-on-merge pass exists to catch. The gate stack worked.

Two classes of problem dominate the findings, and they are orthogonal to the build's clean convergence:

1. **Practice / process gaps in the planning sessions** — the developer suffered four distinct fresh-session disorientation events over five days ("Specification Fatigue," his words), acted as the manual message bus between three parallel sessions (decision, planning, build) by hand-pasting prompts, and ran every governed skill (research, assessment, sprint-planning, sprint-dev) as an ad-hoc dynamic-workflow variant — bypassing the audited skill paths entirely.

2. **Gate-design and bookkeeping gaps inside the otherwise-healthy build** — the document-review (claim-checklist) verifier returned a false-clean PASS on a self-contradicting spec that only the adversarial reviewer caught; story specs repeatedly under-scoped blast radius and seeded wrong spec-section citations that the dev faithfully propagated; and one high-severity bookkeeping defect where a scope-discipline revert silently undid a correct fix while the scorecard still reported 5/5 fixed.

The headline tension of the whole sprint: **approval clustered when the agent operated at decision-grade altitude (options, plain framing); frustration clustered when it surfaced internal counts and jargon (52 stories, beads, stubs, judgment calls) without a plain-language anchor.** That is the central thesis the conduct architecture exists to validate, and the transcript validates it.

A critical caveat scopes this entire audit: the **audit-extract harvest captured the wrong session set.** `team-messages.jsonl` is empty, and all 7 `agent-summaries.jsonl` records are from the 2026-05-31 AES-004 assessment / HITL-research wave — not the 2026-06-04 conduct build. The build's dev/QA/code-review/AVFL/fix-cycle activity had to be reconstructed from build-results JSONL, finding-cards JSON, and git history rather than from any captured transcript.

## What Worked Well

**The gate stack caught real defects at every layer (KEEP).**
- *What happened:* Per-story review caught internal contradictions and spec drift; the AVFL-on-merge integration pass caught a genuine cross-file contract incompatibility no single-story reviewer could see.
- *Evidence:* 105 finding cards across 21 stories; the lone escalated card — "The fixer and the Conductor built incompatible halves of the same hand-off contract" — a `escalation.timing_tier` (nested) vs `F.timing_tier` (flat) mismatch making the routing branch unreachable, caught only by the cross-file AVFL pass and correctly classed high-blast-radius-architecture. Verified against `.momentum/conduct-core-finding-cards-by-story.json`.
- *Root cause:* Layered review (claim-checklist + adversarial per-story + AVFL-on-merge) provides orthogonal coverage; the integration seam is only visible at merge.
- *Recommendation:* KEEP. This is the gate doing exactly its designed job.

**Fix loop converged cleanly with no oscillation (KEEP).**
- *What happened:* All 21 stories reached `merged=true`, `qa_verdict=PASS`, `freeze=MATCH`, `blocked=0`. The single escalation was a deliberate high-stakes route-up, not a stuck loop.
- *Evidence:* build-results: 96 findings, 87 fixed in-band, escalated sum = 0. The `round` field (dist {1:1, 2:2, 3:7, 4:5, 5:4, 6:2}) tracks the dependency wave/frontier, not fix-cycle iterations — no story shows re-open churn. Verified against `.momentum/conduct-core-build-results.jsonl`.
- *Root cause:* Healthy gate→fix→merge cycle with a bounded recheck loop.
- *Recommendation:* KEEP. (Caveat: assessed from build artifacts, not the absent build transcript.)

**False-positive discrimination is sound — the gate is not rubber-stamping (KEEP).**
- *What happened:* All 7 dismissals are low/minor and each carries an explicit, scoped `resolution` rationale (intentional design endorsed by ACs; out-of-scope pre-existing lines; spec-prose-vs-machine-identifier divergence).
- *Evidence:* `conduct-contract-freeze-check` dismissal ("defensible and arguably better reading... endorsed by AC 6 and Dev Notes"); `code-review-adapter-normalize-triage` (model-pin drift "pre-existing and not touched by this story's diff"); `qa-reviewer-rescope` (slash-vs-hyphen stakes-class names "only in human-prose tables, not in any diff hunk").
- *Root cause:* The finding schema forces evidence-grade output with disposition rationale.
- *Recommendation:* KEEP.

**The bounded recheck loop is load-bearing — it caught two fix-induced regressions (KEEP).**
- *What happened:* Fix passes twice introduced behaviorally significant regressions that QA's PASS and the first adversarial review missed; the recheck/re-fix loop caught both.
- *Evidence:* `dev-strip-merge-cleanup-authority` — fixer invented a Conductor lock duty the spec explicitly deleted (REFIXED, commit aa929a0). `conduct-preflight-halts` — a fix hardcoded a wrong H5 status enum that would false-HALT a normally-statused story (residual finding #5, major; fixed commit 2873b2a, `recheck: REFIXED`).
- *Root cause:* Fixers reason about where authority/behavior moves without re-reading the governing spec section; the recheck step is the net.
- *Recommendation:* KEEP — and note this is direct evidence the recheck loop must stay.

**Decision-grade presentation earned fast, genuine approval (KEEP).**
- *What happened:* Approval clusters at decision-ratification moments when the agent presented a synthesized plan or option set at the right altitude.
- *Evidence:* Msg 54 "Yes that sounds perfect, let's do it!"; Msg 51 "OK that looks good."; Msg 18 "Yes please consolidate... Yes, I agree... Yes, agreed." Sharp contrast with the frustration findings, which all involve surfaced internal detail.
- *Root cause:* The developer's own thesis — decision-grade altitude is the lever — confirmed in his behavior.
- *Recommendation:* KEEP.

**Human-driven architectural decisions landed cleanly (KEEP).**
- *What happened:* DEC-035 (feature-grained HITL, no story cap) and DEC-036 (narrow, stakes-and-timing-gated escalation) were both set by the developer's first-principles reasoning about his own cognitive load as reviewer.
- *Evidence:* Msg 21 "why not make it ALL the stories for a given epic?"; Msg 27 "remove the arbitrary limiting of stories"; Msg 53/56/59 setting the narrow escalation bar. The narrow-bar discipline was then verified by the planning critic (Msg 84: "No widened bar anywhere... no third condition").
- *Root cause:* The practice surfaced the right framing question and let human judgment set the unit of work and risk boundary.
- *Recommendation:* KEEP. This is the central bet the sprint exists to test.

**A one-off agent mistake was converted into a durable rule in-session (KEEP).**
- *What happened:* The agent clobbered an HTML doc the developer was actively reading (cmux pane-accumulation problem); the developer caught it, diagnosed it, and turned it into a codified cmux rule fix.
- *Evidence:* Msg 11 "Why did the other page disappear?... you seemed to kill it" → Msg 12 "Is that worth adding to our cmux rule?" → Msg 13 "Yes please, apply."
- *Root cause:* Strength in the practice's mistake→rule conversion; gap is that close-then-open discipline was not yet enforced.
- *Recommendation:* KEEP the conversion habit (the gap is captured as an action item below).

**Reviewer/auditor prompting enforces evidence-grade output (KEEP); healthy agent lifecycle (KEEP).**
- *What happened:* Finding cards uniformly carry headline/what/where (file:line)/why/evidence/resolution; the escalated card cites exact line spans on both sides of the contract. No abandoned or stalled agents.
- *Evidence:* `finding-schema.md:103-105 (Rule 3) vs :70`; escalated card cites `dev/workflow.md:54 ... conductor/workflow.md:444 ... :447`. All 7 captured agents have `assistant_turns >= 17`, `error_count=0`, non-empty substantive final responses.
- *Root cause:* The finding schema shapes reviewer output toward verifiable claims; reliable spawn-and-complete.
- *Recommendation:* KEEP.

## What Struggled

**Document-review (claim-checklist) verification is structurally blind to cross-section contradictions (FIX).**
- *What happened:* On the same `conduct-spec-revision-dec036` dev-pass diff, the document-review QA verifier returned "PASS, 18/18 claims verified, all 5 required sections present" while the parallel adversarial reviewer returned "3 contradictions (1 critical) + 1 major completeness gap." The checklist only inspects the four sections the story named (§1/§4/§8/§9) and is blind to the contradictions the revision introduced in §2/§3/§6/§10.
- *Evidence:* L377 (QA PASS) vs L378 (3 contradictions) in build session 12af2ca3; QA contract anchors all 18 claims to the named sections.
- *Root cause:* Claim-checklist verification scoped to story-named sections cannot see blast radius outside them. Without the adversarial reviewer, a self-contradicting spec would have shipped.
- *Recommendation:* FIX — adversarial review must remain mandatory (not optional/redundant) for document-review stories, and the claim-checklist should be widened to scan for contradictions against the whole document, not only the named sections.

**A correct fix was silently reverted while the scorecard reported it fixed (FIX).**
- *What happened:* A reviewer correctly raised a §8 spec-citation defect that lived inside the story spec file; the fixer correctly repaired it; the Conductor's scope-discipline revert (build agents must not edit their own story file) silently undid the correct fix. The finding card still reads `disposition: "fixed"` and build-results reports 5/5 fixed.
- *Evidence:* Commit `5ca370f revert(conduct-preflight-halts): drop out-of-scope edit...`; the currently merged `.momentum/stories/conduct-preflight-halts.md:89` still reads "**Section 8**: the git-state handling that the reconcile-on-start procedure draws on..." — the exact error the finding flagged. Verified live in the working tree.
- *Root cause:* Scope-discipline rule and the directed-fix loop collide with no reconciliation step; the scorecard overstates convergence.
- *Recommendation:* FIX — when a fix targets the story spec file itself, the disposition must be re-evaluated post-revert (re-route the correction to create-story/refine, or mark the card unresolved). The scorecard must never report a reverted fix as fixed.

**Story specs repeatedly under-scoped blast radius and seeded wrong citations (INVESTIGATE).**
- *What happened:* `conduct-spec-revision-dec036` scoped the revision to §1/§4/§8/§9 but the absolutism it relaxed was duplicated across §2/§3/§6/§10, guaranteeing cross-section contradictions. `dev-strip-merge-cleanup-authority` Dev Notes told the dev to cite spec section numbers it had not opened, propagating five wrong citations (section 12 = file inventory, not governing section 6). The same story's `touches` list omitted SKILL.md, leaving a stale public description advertising the exact behavior being removed.
- *Evidence:* Finding cards: spec-scoping (high), spec-citation-error-seeded-by-story (high), incomplete-touches-list (high). The "do not open the spec to renumber; cite by number" Dev Note pattern recurs.
- *Root cause:* Story authoring (run as ad-hoc dynamic workflow, not via create-story) under-scoped change blast radius and licensed unverified citation-by-number. These are spec-authoring quality gaps, not dev failures — the dev did what the story said.
- *Recommendation:* INVESTIGATE — create-story should require a blast-radius scan (find all sections/files that duplicate the text being changed) and forbid cite-by-number without verifying the referenced section.

**Per-story document-review gates cannot see multi-file integration seams (INVESTIGATE).**
- *What happened:* `directed-fix-invocation-contract` passed its in-story document-review in isolation, then needed two post-merge AVFL commits to define `finding_id`, add join-back semantics, and resolve the `timing_tier` nesting that would make a consumer silently read undefined.
- *Evidence:* Post-merge commits 8032578 (finding_id, findings 7/10/11) and 36712a6 ("D1 — codify nested fixer↔Conductor seam," 55-line Canonical Fixer Output Shape). This is the same seam as the escalated card.
- *Root cause:* The per-story gate is scoped to a single artifact while the contract is inherently a multi-file seam. Real defects escaped the per-story gate and were caught only by AVFL-on-merge.
- *Recommendation:* INVESTIGATE — contract/seam stories may need an explicit "both sides of the seam" review scope, not just the single produced artifact. (The AVFL net held, so this is calibration, not a hole.)

**Cross-session orientation failures — "Specification Fatigue" (FIX).**
- *What happened:* Four distinct disorientation events over five days, several at the start of a returning session, several mid-flow when an agent surfaced internal artifacts without grounding context.
- *Evidence:* Msg 15 "remind me what we were working on?"; Msg 45 "totally lost... What is the 52 stories?"; Msg 70 "no idea what you're talking about... the per-leg amendments to the existing 18 stories"; Msg 86 "I don't understand the stubs or why we're talking about beads." Work spanned 3+ concurrent session files with thin state continuity.
- *Root cause:* Cross-session handoff is manual, and the agent references internal counts/jargon (52 stories, beads, stubs, judgment calls) without a plain-language anchor. Named by the developer himself as Specification Fatigue (Msg 60).
- *Recommendation:* FIX — agents must lead returning sessions and jargon-bearing turns with a plain-language anchor before any internal count; pair with a durable cross-session handoff artifact (next item).

**The developer was the manual message bus between parallel sessions (INVESTIGATE).**
- *What happened:* State (the 18 stories, DEC-036 amendments, the sprint plan) was carried across session boundaries by hand-pasted prompts rather than a durable shared artifact.
- *Evidence:* "Could you give me a prompt to another session to run a sprint plan" (06-01); "Please provide me the 18 stories... I'm working through some decisions in another session" (06-02); "Here is the prompt from another session for this planning..." (06-02, fbbb18d4); "give me the full prompt to hand off to the sprint-dev session" (06-04).
- *Root cause:* No programmatic handoff contract between decision, planning, and build sessions; the dominant coordination mechanism for the whole sprint was entirely manual.
- *Recommendation:* INVESTIGATE — a durable session-handoff artifact the next session reads (vs. copy-paste) would eliminate the message-bus role and reduce orientation failures.

**Every governed skill was run as an ad-hoc dynamic-workflow variant (INVESTIGATE).**
- *What happened:* research, assessment, sprint-planning, and eventually sprint-dev all ran as hand-driven dynamic-workflow variants rather than via the skill itself.
- *Evidence:* Msg 39 "rather than following /momentum:research exactly... use dynamic workflows"; Msg 46/75/87 same for sprint-planning; Msg 50 reveals a concrete breakage — the assessment skill hard-codes a sonnet agent that no longer resolves ("It's not able to use the sonnet agent it's built for"), forcing manual execution.
- *Root cause:* Intentional R&D prototyping of conduct's dynamic-workflow substrate — but none of this sprint's planning artifacts went through the audited skill paths, a fidelity/auditability gap. At least one skill (assessment) has a stale agent binding.
- *Recommendation:* INVESTIGATE the auditability gap; FIX the stale assessment agent binding (broken out as an action item).

**The audit-extract harvest captured the wrong session set (FIX).**
- *What happened:* `team-messages.jsonl` is empty (0 lines); all 7 `agent-summaries.jsonl` records are from the 2026-05-31 AES-004 assessment / HITL-research wave; none are from the conduct build. The build artifacts are timestamped 2026-06-04, produced by a session whose transcript is absent.
- *Evidence:* `wc -l` confirms team-messages=0, agent-summaries=7; all 7 first_prompts reference "discovery auditor for a Momentum assessment (AES-004)" or "senior research synthesist... HITL sweet spot."
- *Root cause:* The extract window selection (or agent-attribution filter) is keyed to the wrong session set. A reviewer working only from these extracts would have zero visibility into the build and could only hallucinate.
- *Recommendation:* FIX — the retro's audit-extract harvest must key on the build session(s), not the prior planning wave. This undercuts the efficiency and coordination lenses for this sprint.

**Read-before-write discipline lapse (KEEP — micro-pattern, recovered).**
- *What happened:* An agent attempted Write/Edit without a prior Read, twice ~3s apart, before adapting.
- *Evidence:* errors.jsonl entries 5 and 6 (both 2026-06-02T00:25, src fe491b4a): "File has not been read yet. Read it first before writing to it."
- *Root cause:* Minor discipline lapse; harness guard caught it correctly.
- *Recommendation:* KEEP — not a practice gap, but a recurring micro-pattern worth noting.

## User Interventions

- **Reconciliation against the standing decision record (Msg 19–27, medium).** The developer interrupted the agent mid-action ("[Request interrupted by user for tool use]") to force reconciliation between the new conduct plan and prior committed decisions (DEC-028 beads, DEC-032 Gas City) before letting it proceed: "we had plans to integrate beads and gascity. I think this plan is a bit of a replacement." Resolved at Msg 27 "move forward with our plan for conduct." Root cause: the agent built forward without reconciling against standing decisions; the human had to catch it. (Correctly recorded — DEC-035 supersedes DEC-032.) Recommendation: INVESTIGATE — agents should proactively surface decision-record conflicts when a new plan supersedes prior commitments.

- **cmux pane-clobber caught and codified (Msg 11–13, medium).** See "What Worked Well" — the developer caught a clobbered HTML doc and turned it into a durable rule. Recommendation: KEEP (conversion), FIX (the missing close-then-open discipline).

- **HITL calibration set by the developer (Msg 53–59, high).** "rather than removing HITL interactions totally we should limit them to ONLY certain categories. security/irreversible/migration/blast-radius... can it wait until the end?" → DEC-036. The human set the risk boundary the autonomous build must respect. Recommendation: KEEP.

- **Unit-of-work grain set by the developer (Msg 21/27, high).** Feature-grained HITL and no story cap, reasoned from his own cognitive load as reviewer. Recommendation: KEEP.

- **No story-specific build-time interventions.** The full dev-review-fix loop for the build stories ran autonomously — no human steering touched any individual story's build (confirmed by user-messages query returning only sprint-planning context for slug-matching sessions). This is a strength in autonomy but also why the build transcript's absence matters.

## Story-by-Story Analysis

All 21 stories merged with `qa_verdict=PASS`, `freeze=MATCH`, `blocked=0`. Stories with notable findings:

- **conduct-spec-revision-dec036** (round 1) — 1 dev pass + 3 directed-fix + 2 review passes; did NOT converge one-shot. Under-scoped to named sections, leaving cross-section contradictions (§2/§3/§6/§10) the dev faithfully reproduced. **The false-clean document-review PASS vs adversarial-catch divergence originates here** — the single most important gate-design finding in the sprint.

- **conduct-skill-scaffold-and-spine** (round 2) — cleanest possible convergence (1 dev + 1 fix, 3-line correction, 4 min). But review caught a real spec contradiction: the scaffold baked a developer-facing HALT into the live merge loops, violating the Never-HALT git invariant (AC 7). Also a definitional-drift finding: scaffold and spec disagreed on what "the two routine touchpoints" are (run-start+end-gate vs end-gate+push).

- **code-review-adapter-noninteractive-driver** (round 3) — caught a real correctness bug: config resolved CWD-relative (`ls _bmad/bmm/config.yaml`) would spuriously fail inside conduct's worktree; fix resolves via `git rev-parse --git-common-dir` (commit 432d964). Also AC3 (HALT-suppression coverage) and AC4 (dropped dismiss-class findings) reworked — review enforced AC traceability.

- **dev-read-contract-part-a-header** (round 3) — Conductor reverted an out-of-scope story-file edit, keeping the merge confined to deliverables (safety machinery working). Robustness gap: contract-file discovery guessed extension across five possibilities instead of deriving from `verification_method`; agent's Part-A key list dropped `harness_profile`. Both caught at end-gate.

- **dev-strip-merge-cleanup-authority** (round 3) — three high-severity findings: (1) five spec citations pointed to section 12 (file inventory) instead of governing section 6, seeded by the story's own Dev Notes; (2) incomplete `touches` list omitted SKILL.md, which still advertised worktree creation; (3) fixer over-corrected by inventing a Conductor lock duty the spec deleted (caught by recheck). Also a semantic merge-conflict resolution on `dev/workflow.md` (shared with the sibling read-contract story) — both intents preserved by hand-merge, validating this story's own thesis that the Conductor owns conflict resolution.

- **directed-fix-finding-schema** (round 2) — spec-gap caught in review: triaged-out was unreachable for the legitimate-but-out-of-scope case it exists for; review added Rule 4 (commit 708f2c0), protecting the "no finding silently lost" invariant. Doc-precision finding: illustrative enums read as exhaustive and used invented values (verdict 'warning'/'nitpick') not matching spec §4 vocabulary — reconciled and marked open.

- **directed-fix-invocation-contract** (round 3) — converged clean in-story (1 author + 2 fix), but needed two post-merge AVFL commits to define `finding_id`, add join-back semantics, and codify the nested `timing_tier` seam. The per-story document-review could not see the multi-file seam.

- **stakes-classification-rubric** (round 3) — single clean fix cycle. Both review findings low/routine: a genuine internal contradiction (rubric mid-flight bar disagreed with the already-merged conductor workflow) and a clarity defect (redundant restatement, line 84). The bar reconciliation was deliberately deferred to the downstream escalation-mechanism story.

- **conduct-preflight-halts** (round 3) — **two notable findings.** (1) HIGH bookkeeping defect: the §8 citation fix was reverted by the Conductor's scope-discipline rule, yet recorded `fixed` 5/5 — the error persists at line 89 of the merged file. (2) MEDIUM: a fix hardcoded a wrong H5 status enum (omitting 5 valid statuses, inventing 2) that would false-HALT a normally-statused story; caught only by recheck (commit 2873b2a).

- **Remaining stories** (conduct-build-phase-frontier, dev-fix-mode-entry, conduct-contract-freeze-check, conduct-stakes-timing-escalation-mechanism, code-review-adapter-normalize-triage, qa-reviewer-rescope-per-story-contract, stage3-fix-loop-via-directed-dev, conduct-merge-and-conflict-resolution, conduct-coverage-disposition-branch, code-review-adapter-retire-stub, code-review-adapter-repoint-sprint-dev, code-review-adapter-repoint-quick-fix) — converged within their dependency waves with no flagged struggles; dismissals on these were the well-reasoned, scoped false-positive discriminations noted above.

## Cross-Cutting Patterns

1. **Altitude is the lever (recurs across human + praise + frustration lenses).** Approval came when the agent presented options/plain framing; frustration came when it surfaced internal counts/jargon. This is the conduct architecture's central thesis, validated by the transcript itself.

2. **Per-story gates are single-artifact-scoped; integration defects live at the seam (recurs across review + 3 story lenses).** The escalated card, the directed-fix-invocation-contract rework, and the spec-revision cross-section contradictions are all the same shape: a defect spanning files/sections that no single-story, single-artifact review can see. AVFL-on-merge is the net that catches them — and it held every time. The lesson is calibration (give seam stories a two-sided review scope), not a hole.

3. **Story-authoring quality, not dev quality, is the upstream root cause of the high-severity findings (recurs across 4 story lenses).** Wrong section citations, incomplete touches lists, under-scoped blast radius, and unreachable dispositions all originated in specs authored via ad-hoc dynamic workflows rather than create-story. The dev faithfully propagated each one. This points squarely at hardening create-story's blast-radius and citation discipline.

4. **Fix passes introduce factual regressions when fixers don't re-read the spec (recurs across 2 story lenses).** Twice a fixer invented a responsibility the spec had deleted; both caught by recheck. The recheck loop is load-bearing and must stay.

5. **Manual cross-session coordination is the sprint's connective tissue and its biggest fragility (recurs across human + coordination lenses).** The developer-as-message-bus and the four orientation failures are two faces of one gap: no durable session-handoff artifact.

6. **Claim-checklist and adversarial review are not redundant (recurs across review + story lenses).** The checklist alone would have shipped a self-contradicting spec. Both layers are required.

## Metrics

| Metric | Value |
|---|---|
| User messages (extract) | 87 |
| Subagents (agent-summaries) | 7 (all from 2026-05-31 wave — wrong session set) |
| Errors (errors.jsonl) | 8 (incl. 2 read-before-write at 2026-06-02T00:25) |
| Team messages (team-messages.jsonl) | 0 (empty — extract scope mismatch) |
| Stories merged | 21 / 21 (PASS, freeze MATCH, blocked 0) |
| Finding cards | 105 (93 fixed, 7 dismissed, 1 escalated, 4 triaged-out) |
| Build-results findings | 96 total / 87 fixed / 0 escalated-thrash |
| Build rounds (waves) | {1:1, 2:2, 3:7, 4:5, 5:4, 6:2} |
| Struggles (FIX + INVESTIGATE) | 11 |
| Successes (KEEP) | 13 |

## Priority Action Items

1. **Widen document-review verification to scan the whole document for contradictions** — *critical*. Source: review-divergence on conduct-spec-revision-dec036 (QA PASS 18/18 while adversarial found 1 critical + 2 contradictions). The claim-checklist is structurally blind outside story-named sections. Suggested ACs: (a) for document-review stories, adversarial review is mandatory and non-skippable; (b) the claim-checklist scans the full document for contradictions against changed claims, not only named sections; (c) a QA PASS is invalid if a parallel adversarial reviewer returns critical findings on the same diff.

2. **Reconcile fix-disposition with Conductor scope-discipline reverts** — *high*. Source: conduct-preflight-halts §8 citation fix reverted (commit 5ca370f) but recorded fixed 5/5; error persists at line 89. Suggested ACs: (a) when a fix edits a non-deliverable (e.g. the story spec file) and is reverted, its finding card disposition is re-evaluated, not left `fixed`; (b) the correction is re-routed to create-story/refine for the record; (c) the end-gate scorecard cannot report a reverted fix as fixed.

3. **Fix the retro audit-extract harvest to key on the build session(s)** — *high*. Source: team-messages.jsonl empty, all 7 agent-summaries from the 2026-05-31 planning wave, build transcript absent. Suggested ACs: (a) audit-extract selection is keyed to the sprint's build session IDs, not the prior planning wave; (b) the harvest validates that captured agents/team-messages temporally overlap the build artifacts before filing; (c) an empty team-messages.jsonl raises a harvest warning.

4. **Harden create-story blast-radius and citation discipline** — *high*. Source: three high findings on dev-strip-merge-cleanup-authority + conduct-spec-revision-dec036 (wrong section-12 citations, omitted SKILL.md in touches, under-scoped section list). Suggested ACs: (a) create-story runs a blast-radius scan finding all sections/files that duplicate the text being changed and adds them to scope/touches; (b) cite-by-number is forbidden unless the referenced section is opened and verified; (c) the touches list is validated against the actual surfaces the change invalidates (e.g. public SKILL.md descriptions).

5. **Lead returning/jargon-bearing turns with a plain-language anchor + durable session handoff** — *high*. Source: four orientation failures (Msg 15/45/70/86, "Specification Fatigue") + developer-as-message-bus across 4 cross-session handoffs. Suggested ACs: (a) on a returning session or any turn surfacing internal counts/jargon, the agent leads with a plain-language anchor before any number; (b) a durable session-handoff artifact is written that the next session reads, replacing hand-pasted prompts; (c) the handoff carries the live story set, active decisions, and the sprint plan.

6. **Fix the assessment skill's stale sonnet agent binding** — *medium*. Source: Msg 50 "It's not able to use the sonnet agent it's built for," forcing manual execution. Suggested ACs: (a) the assessment skill resolves its agent via the current routing table, not a hard-coded sonnet binding; (b) a smoke check verifies the bound agent resolves before the skill runs.

7. **Give contract/seam stories a two-sided review scope** — *medium*. Source: directed-fix-invocation-contract + the escalated timing_tier card — per-story document-review cannot see multi-file seams. Suggested ACs: (a) stories that define a contract between two agents declare both sides as review scope; (b) the per-story gate checks field-shape compatibility across both sides, not only the produced artifact. (epic_slug: conduct)

8. **Proactively surface decision-record conflicts when a new plan supersedes prior commitments** — *medium*. Source: Msg 19–27 (developer had to interrupt to force beads/Gas City reconciliation). Suggested ACs: (a) when a new plan touches an area covered by a prior DEC, the agent surfaces the conflict and proposed supersession before proceeding; (b) the supersession is recorded as a decision amendment.
