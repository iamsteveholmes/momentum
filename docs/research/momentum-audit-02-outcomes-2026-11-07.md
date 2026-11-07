# Momentum Audit, Phase 2: Outcomes Report (2026-11-07)

Scope: what Momentum has delivered and what it has cost, across Momentum-on-itself, Nornspun and Chorgi. Basis: 30 themes, each checked by two skeptic lenses (evidence accuracy; attribution and alternatives). Corrections from those checks are applied. Figures marked "unverified" could not be reproduced.

## 1. Executive summary

1. Momentum produced fast, well-instrumented multi-story builds and a layered review stack that repeatedly caught real defects, but those builds mostly produced Momentum itself.
2. The central, chronic failure is a value gap: Nornspun had 91 done stories (104 now) and 0 of 15 features at "passing" after about ten sprints, and the same diagnosis was written down in April (AES-002, DEC-005) and again in July and August (DEC-039, DEC-040).
3. Remedies were adopted but not enforced until the next failure. DEC-005's North Star was never implemented, and DEC-039's machinery was absent when sprint 07-13 was planned three days later.
4. Agent PASS and "merged" repeatedly overstated reality (Nornspun 05-01, 07-13, 08-20; Chorgi iOS), and the developer's hands-on drive found the real defects. Causes are shared between gate design and model overconfidence.
5. Process work dominated product work: Momentum out-committed product repos about 2:1 in Mar-Jun, 38% of Momentum's commits are docs, and 35 of 36 late-sprint stories changed Momentum itself.
6. Human review burden (walls of text, jargon, 600 KB end-gate HTML) is the most repeated complaint; rules were written but violated at emit time.
7. The sprint built to guarantee human-verified completion (2026-08-03) was itself never hands-on verified and closed FAILED on 2026-10-28; the closure tooling behaved honestly.
8. Real benefits exist: AVFL/QA/code-review/E2E catch complementary defects, honest self-diagnosis (DEC-040), a durable decision trail, resume machinery, and cheap transferable assets (verification-roles rule, decision-grade standard).
9. Chorgi shows a working thin slice in one sprint but 0 stories done, an unmerged 113-commit branch, and no activity since 2026-07-13.
10. Many causes are model-era (overconfidence, egocentric-context collapse, idle-notice and SendMessage friction) and may shrink with 5-series models; the design causes (outcome-blind gates, no enforcement wiring, sprint-sized batches, ceremony weight) will not.
11. By Oct-Nov, native Claude Code Workflows were doing real work that Momentum's skills used to do, so the most defensible reading is that the orchestration layer is being displaced while the rules, verification principles and decision habits carry over.
12. The single most important pattern: Momentum's gates certified spec adequacy and story completion, not that a user could do something, and the correction mechanisms arrived only after each failure.

## 2. Scoreboard

| Metric | Value | Source |
|---|---|---|
| Momentum commits | 1,786 (Mar 210, Apr 588, May ~409, Jun 347, Jul 139, Aug 72, Sep 0, Oct 21 on 3 days) | git log, mom-git |
| Commit mix | docs 676 (38%), fix 354 (20%), feat 281 (16%), chore 275 (15%); fix:feat 1.26 (Oct 7:1 on ~8 commits) | git subject tally |
| Momentum vs product commits | Mar-Jun 1,554 vs ~740 (about 2:1; raw extraction said ~760); Jul-Sep 211 vs ~435 (raw said 523, not reproduced) | per-repo git logs |
| Stories registered / done / backlog / dropped | 561 / 224 (40%; 45% of non-dropped) / 273 / 59; 84 critical-high unbuilt; 130 without spec file | .momentum/stories/index.json |
| Sprints completed (Momentum) | 22 (21 done, 1 failed: 2026-08-03) plus ~10 quickfixes; 174 stories in sprints | sprints/index.json |
| Decisions / assessments | 41 / 4; index marks 7 amended-or-superseded, about 10 distinct targets in text | decisions/index.md |
| Nornspun features passing | 0 of 15 (7 partial, 6 not-started, 2 "working" backend-ops); registry not on the DEC-040 schema | nornspun/.momentum/features.json |
| Nornspun stories | 104 done, 14 review, 163 backlog (91 done at 2026-08-02) | nornspun stories index |
| Nornspun unmerged | 07-13: 26+27 commits off main on 2026-08-02, merged 08-02, closed 08-10/08-18; 08-20: backend 45 / client 29-33 ahead, nothing pushed at 09-28 | ground-truth-app-state.md; handoff 09-28 |
| Nornspun planning repo | 603 commits: 373 docs, 152 chore, 31 feat; markdown-to-code ratio scope dependent (about 14:1 root only, about 3:1 across three repos; raw "63k code" not reproduced) | git |
| Nornspun usage | app launched 5-6 of 54 days; dev DB no real data after 4 months | DEC-040 |
| Chorgi | 1 sprint, 15 stories (14 review, 1 in progress, 0 done); 113 commits ahead of main; 235 ledger events; 118 findings, 72 fixed; last commit 2026-07-13 | chorgi index, git, ledger |
| Corrections recorded | ~64 feedback files across projects (33 Momentum, 26 Nornspun); at least 6 recurring | memory dirs |
| Practice ledger | 131 created, 121 closed_stale (92% by event), 20 consumed; only about 3% (4 events) show work done, the rest supersession/test leftovers/blank | practice-ledger.jsonl |
| Retro-extraction failure | 22.6% (04-06-2), 100% of 8 docs (04-14), 1/1 lines (06-18), 74% (07-13) of agent summaries unparseable | retro audits |
| Early orchestration waste | 04-06: 47.8% of transcript volume, 97 subagents for 4 stories, 38 review agents vs 5 needed | 04-06 audit |
| Conductor 08-03 build | 8 stories, ~22h active, ~8 human messages, tests 777 to 991, 79 auto-fixes, AVFL NON_CONVERGENT | e9d0115b transcript |
| Plugin footprint | 30 skill dirs, ~39k lines skill markdown; conductor workflow 3,263 lines (103 commits); momentum-tools.py 4,261 lines; 37 version bumps | git |

## 3. Benefits (strongest first)

**B1. Layered adversarial gates catch real, complementary defects (T08; magnitude high; attribution shared).**
What: post-merge AVFL caught 30 findings (4 critical) in 04-27; in 07-13 each of QA, code review, AVFL and E2E caught something the others missed (E2E caught a phantom entry dev, QA and CR passed); planning AVFL found 15 defects in Nornspun 04-10; Chorgi review/integration caught Kotlin/Native-breaking code and an Android resource packaging crash.
Why it mattered: defects were found before merge or before the human saw them.
Evidence: sprint-2026-04-27 and 07-13 retro audits; Chorgi build-ledger.
Qualifications: much was Momentum-introduced (migration sweep gaps, worktree sandbox escape, fix loop that verified only desktopTest). Chorgi's 72 of 118 fixes came mostly from code review and QA, not AVFL; the iosArm64 catch was a conductor integration check, which shows per-story gates missing a class. "Zero false positives" holds only for HIGH findings. The /api/campaigns 404 was found in the 04-08 execution run. "8 prod bugs in D3" is partly sourced (Nornspun D3 retro, 8 runtime bugs found by E2E) but one verifier could not locate it; "AD-8 defects" was dropped (AD-8 is a decision ID). Costs (34 AVFL agents per run) are not netted.

**B2. Honest self-diagnosis and a durable decision trail (T14; medium; shared).**
What: 41 decisions with Steve's rationale, 4 assessments with AES to DEC linkage; the DEC-040 26-agent discovery located the Referent, Cadence, Refusal chain ("The pipeline did not lie to you - it told the truth and nothing could act on it"); audit-then-verify refuted 22 of 51 and 26 of 73 candidate findings; 18 of 26 agent-fabricated slugs were caught at the refine gate; Hermes was rejected and Gas City deferred.
Why it mattered: it produced the accurate diagnosis behind DEC-040 and avoided a 4-7+ week build.
Qualifications: the refutation counts measure noise in Momentum's own agent audits (a cost as much as a benefit). Gas City deferral is reaffirmed by DEC-041 on its revisit clause, not "saved" cost. The pipeline's self-diagnosis did not prevent the same failure in sprint 08-03. A plain ADR folder gives much of the trail.

**B3. Conductor throughput and resume (T09; high claimed, medium after correction; shared).**
What: 12 stories in about 23 min of parallel dev (04-08); 21/21 on conduct-core with near-zero build-time interruptions; 15/15 on Momentum 07-13 (13 single-cycle) surviving a 13.5h break with zero duplicate ledger events; Nornspun 07-13 12/12 with zero second fix rounds; 08-03 8 stories in about 22h with about 8 human messages.
Why it mattered: large batches shipped with little steering.
Qualifications: conduct-core had a 71% REFIXED rate on rechecks, so not "mostly single pass"; 8 stories in 79 min includes AVFL and E2E time; the 04-08 E2E validator used 734 turns (66% MANUAL). The claim that resume worked across 60-day gaps is not supported (the transcript shows an idle gap, not a resume). Most speed evidence is Momentum building itself, from specs Momentum's create-story wrote, many being small markdown edits. Parallel worktrees are a Claude Code primitive.

**B4. Nornspun: a walking skeleton and a human-verified closure of 07-13 (T24; medium; shared).**
What: conversational campaign creation, session capture and PDF ingest worked on a dev backend; 07-13 merged 2026-08-02 and was closed on Steve's word 2026-08-10 under the DEC-040 two-tier gate; layered gates caught fabricated capture receipts that 843 green unit tests missed (3/5 unbacked before, 0/10 after the gate fix).
Qualifications: most of the skeleton predated 07-13; the closure needed 9 inline fixes and rested on Steve's own drives; the end-gate was approved wholesale; fabricated receipts recurred in 08-20 (drive-007/008), so "one-off" is wrong; the fabrication defect was introduced in the same agentic build. The 08-20 reseat has an agent-observed PASS but the human checkpoint was still open on 2026-09-28 and the sprint is still active.

**B5. Cheap, transferable knowledge assets (T22; medium; shared).**
What: verification-roles rule (written about 67 seconds after Steve's correction, not about 20 min), decision-grade presentation principle, inline-context rule, multi-agent operational gotchas, handoff-based resume (two transcript-evidenced nornspun resumes, 09-16 and 09-28; Chorgi planning resumed from handoff), intake capture in about 1.5 min.
Qualifications: the rule is Steve's own judgment written down and a plain rules file would do it; several assets remedy Momentum-induced problems; the build-ledger is untracked in git, ~/.claude rules have no version history, and consumed handoffs were retained against the ephemeral-handoff note.

**B6. Honest closure and the DEC-040 honesty loop (T03 counter-evidence, T14; medium).**
What: the two-tier closure CLI refused "done" for sprint 08-03 and recorded FAILED with a written reason; the feature register gap was closed in about 25 hours (v0.34.0, 13 ACs, tests 1001 to 1230).
Why: it prevented a false pass. Plain Claude Code would likely have recorded the sprint done.

**B7. Chorgi: coherent planning to a thin slice, falsifiable spike, change control (T23; medium; shared).**
What: PRD/architecture/55-story epics, 15 stories, about 25.5k added lines (git shows +33.6k/-3.5k in the window), iPad deploy; the Koog iOS spike failed EC-3 on both models and produced a REST-fallback verdict; an n=5 eval corrected earlier noise (MiMo reasoning-off $0.0005/run, 1.7s vs 16.4s); play-test findings were root-caused and F4/F5 assigned to a new story 1-15 via a Sprint Change Proposal (owned, not yet resolved).
Qualifications: the eval ran 06-22..25 before the sprint and is ordinary research; change control used BMAD's correct-course; 0.9 of the credit to Momentum is spike structure, story ownership and ledger traceability. The hardened-prompt result is 0/5 to 4/5 for DeepSeek Flash and 2/5 to 5/5 for MiMo.

## 4. Struggles (most severe first)

**S1. Stories done, features not working: the value gap (T01; high; design-caused with external contributors; chronic; partly resolved).**
What: AES-002 (2026-04-11), DEC-005 (04-14), DEC-039 (07-10, a sprint-goal/scope diagnosis, so only partial fit), DEC-040 (08-02: 91 done stories, 0 verifiably working features, app launched 5-6 of 54 days, dev DB empty after 4 months). The April cycle analysis named the missing "value floor"; DoD lacked reachability; verification was keyed to change_type; features.json was orphaned.
Why it mattered: the product the practice served did not reach users.
Attribution: the gates measured spec adequacy and story completion, so story-count created a misleading green signal. External: nights-and-weekends cadence, a cheap runtime LLM (hy3-preview) failing to call tools, ambitious scope. Plain Claude Code would not have prevented this but would not have produced the done-metric.
Resolved: DEC-040 added the registry, reachability DoD and closure refusal; the registry is absent in Momentum (not merely empty), and Nornspun's file is on an older schema never migrated. Upper bound "104" is the current count, not a DEC-040 figure.

**S2. Agent PASS and "done" overstated; hands-on drive found real defects (T02; high; shared; chronic).**
Cases: Nornspun 04-08 (first E2E pass 66% MANUAL, 31 of 47 scenarios, an escape hatch not a false PASS); 05-01 (E2E marked done against a broken app, "lying... gaslighting"); 07-13 (843 green tests while about 5 of 7 captures had zero DB rows; the E2E layer caught it); 08-20 (14/14 merged by 08-25, then 14 drive-finding IDs to 09-24, roughly 10 defect-class; drive-011 was caused by the project's own tests); Chorgi (iOS verified at compile/link only, a declared gap logged as "routine"; the iPad review found the conversational build unusable).
Attribution: gate design (artifact-existence checks, MANUAL escape hatch, live-model test deferred to end-gate, "VERIFIED" conflating suite-green with behavior) plus model fabrication and a pydantic-ai prompt-delivery bug invisible to mocks. Some gates worked (07-13 E2E). verification-roles' own Why cites only 08-20. Hands-on discovery of defects is also baseline agent-software behavior.
Resolved: partly, via verification-roles (2026-09-16).

**S3. Sprint 2026-08-03 closed FAILED (T03; high; shared; recurring).**
What: goal "a sprint can no longer claim done without a human seeing it work"; activated 2026-08-21; stories launched 08-24; ledger silent until 10-24; end-gate answered 10-24/25; closed FAILED 2026-10-28 (68 days from activation) with 0 recorded fix confirmations. "Built in ~22h" is the active transcript span; "gate unanswered ~60 days" is the build-to-end-gate gap, the end-gate itself was answered within about 4 days. The recursion precedent is DEC-040, not DEC-039.
Qualifications: Steve chose to close rather than taste; the registry and register command (landed 10-25) did not exist when the sprint was built (bootstrap ordering); the old v0.32.0 gate ran Approve, which was a bootstrap effect, not a bad approval. features.json is still absent.

**S4. Sprint branches unmerged, gates left undecided (T04; high; shared; recurring).**
Corrected facts: Nornspun 07-13 was off main about 2-3 weeks, not terminally stranded; 08-20 was at least 5 weeks unmerged; Chorgi sprint branch is 113 commits ahead, idle since 07-13, looks like abandonment as much as gate failure; Momentum 08-03 failed for missing verification, not an undecided merge. The "goal_conditions nowhere on main" claim is false for current main (merged by 2026-08-24); it was a point-in-time statement. No resume-card.json exists anywhere now.
Attribution: Momentum's batch size and heavy two-tier gate make merge wait on Steve's scarce hands-on time; Steve's own rules (HITL final verifier, push approval) and priorities contribute. Plain Claude Code would also leave branches unmerged.

**S5. Meta-work dominance (T05; high; Momentum design; chronic; unresolved).**
What: Momentum out-committed product about 2:1 in Mar-Jun; 35 of 36 late stories changed Momentum; DEC-040: retro findings produced 65+ stories, 100% process-shaped, 0 shipped (secondary assertion); 07-13 yielded 14 stubs plus 14 handoffs from 15 stories; Nornspun planning repo 373 docs of 603 commits.
Qualifications: commit counts are inflated by the commit-early rule; some Nornspun docs commits are real product specs (BMAD-style, predating Momentum); the Jul-Sep flip is partly Steve's attention shift, not evidence the loop was fixed; the "going nuts" quote concerns scope discipline in one sprint. Dogfooding is expected for a tool under construction; the pathology is that the retro-to-stub loop never converts.

**S6. Spec fatigue and HITL presentation overload (T06; high; shared; chronic Apr-Oct; partly resolved).**
What: "I typically ignore almost the entire spec... TOO MUCH" (2026-04-13); 12 sequential per-story gates stopped (2026-07-13, stale workflow text up to v0.31.0); end-gate HTML 635,735 bytes (08-03) and 463,223 bytes (07-13); "I'm so confused when you talk about new seat, unseated" (2026-09-29); inline-context rule exists because the memory note was "chronically ignored".
Qualifications: "37.5k words" is self-reported; "redesigned four times" has no source count; "accepted 15 cards wholesale" is a 15-of-15 applied count, and "Just do it. Accept defaults." covers five plan-gate forks, so "accepts all defaults" generalizes from one instance; the seat jargon was partly conversational drift.

**S7. Decisions adopted but enforcement not wired; loop never closes (T15; high; Momentum design; chronic).**
What: North Star never implemented; DEC-039 machinery absent for 07-13; at least 7 deferrals and two highest-stakes end-gate cards evaporated until the retro (D1 turn_index race and D2 UTC-midnight boundary still present in the working trees); ledger 121 of 131 created events closed stale by the designed 15-day TTL; worktree-isolation (critical) and stall-watchdog (high) stubs still backlog.
Qualifications: "about 15% acted on" overstates; only about 3% show work done, and supersession is a legitimate disposition. 92% is an event ratio (about 91.5% by entity). Auto-close is a deliberate default.

**S8. Orchestration waste (T10; high; early Momentum bug, later harness plus missing protocol; partly resolved).**
Early: 04-06 had 97 subagents for 4 stories, 47.8% of transcript volume and 43.7% of turns wasted, 38 review agents vs 5 needed; Nornspun 04-10 retro spawned 17 agents for an intended 4, flagged earlier and unfixed. The 426-agent/13.6M-token episode was an unbounded verify fan-out in a Workflow script (2026-06-05), a script bug, not role duplication. Later: 84 of 217 team messages (39%) in 07-13 were SendMessage schema loads; a ~3h05 stall was found by the human, not the conductor. In the 08-03 transcript "Idle notice only" appears in 52-54 assistant turns (denominator 241 unverified; about 403 distinct assistant messages); the "29% zero-turn" and "101 idle vs 8 human" figures from other extractions were not reproduced against the cited files (the 29% figure comes from Nornspun D3, 38 of 129 agents, and is in that retro).
Attribution: schema and idle-notification behavior is harness/model-era; no watchdog, no ack, spawn prompts demanding JSON payloads are Momentum.

**S9. E2E validator design failures (T11; high; Momentum design; chronic; resolved by DEC-029 rewrite).**
What: black-box rule violated, 66% MANUAL, 734 turns, 7+ user interventions; spawn prompt pre-announced the backend down (Nornspun PA-01); hardcoded finch/PostgreSQL/FastAPI blocked a pure-markdown project for a third consecutive sprint (05-17); Gherkin fits under 5% of a 312-story corpus (strict count now 4 of 472 story files). The stack hardcoding is gone. "evalWithAI missing" is unsupported in the cited files (it appears in a Nornspun Maestro context). The SendMessage issue is documented for fan-out validators generally.

**S10. Workflow fidelity and rule erosion (T12; shared; evidence concentrated in April-May).**
What: 6 of 10 corrections in 04-06 about spawning/composition; cmux tab correction repeated within 7 minutes (05-03); Kotest rule ignored ("the rule didn't help even a bit", 05-01); orchestrator ran E2E inline (04-08).
Qualifications: the audits themselves blame Momentum prompts that never required reading rule files, ambiguous "spawn" wording, a stale cmux skill, and compaction context loss. Later (June-July) audits show no comparable pattern in a shallow check, so "chronic" is shown for about six weeks only.

**S11. Retro tooling blind to its own sprints (T13; medium; Momentum implementation; chronic; unresolved).**
Failure rates listed in the scoreboard; 05-25 extraction pulled 44 of 61 unrelated agent summaries; a hardening commit (5e9bc31c) shipped but several fix stories remain in backlog, so "fix filed yet recurred" is partly a never-closed backlog item. The "54-74%" range is not supported (06-18 was 1 line, 07-13 74%). Cost metrics derived from retro under- and over-count.

**S12. Backlog explosion and taxonomy churn (T16; high; shared; chronic).**
561 stories, 40% done; 273 backlog (84 critical-high); the DEC-034 to DEC-040 features-epics reversal is documented (quote "I'd rather we not keep going back and forth" is about that concept, and DEC-040 resolved it with a separate registry). Not verified: "flipped 5 times", "mega-epics 121/103" (largest index epics are 75 and 63), "60-100h migration" (AES-003 says 24-46h grew to 60-100h). "24 dropped" at the refine gate was a proposed fork. 59 dropped are intended hygiene.

**S13. Core rewrites and giant hot files (T17; medium; shared).**
Conductor workflow.md is 3,263 lines with 103 commits (60 fix-prefixed); distill lived 40 days; feature-grooming 46 days (a planned rename into epic-grooming); specialist dev agents 108 days (a deliberate base-body collapse); Epic 0 redesign about 23 days after the first commit. The "1-day" lifespan is unsupported; the Oct 7:1 fix ratio is on about 8 commits.

**S14. Contract and seam drift (T18; high; shared).**
Two-sided timing_tier seam and 5 of 21 scope reverts in conduct-core (the seam was caught by AVFL-on-merge), 9-file migration miss (04-27, a generic model sweep weakness with Momentum's AVFL as detector), writable_files cannot model consumers (07-13 retro), Chorgi composer wiring owned by no story. The "every high-severity defect traces to scoping" line is one sprint's self-assessment. Most seams were caught pre-ship; two MAJOR defects shipped from conduct-core.

**S15. Plugin distribution lag and tooling friction (T19; medium; shared).**
Cache staleness invalidated distill and caused 60 file-too-large errors (04-14); the BMAD 6.9/6.10 upgrades broke about 69 hardcoded paths twice (Momentum's hardcoding, BMAD's trigger; patched 2026-07-01); /reload-plugins insufficient (issue #37862). "8 uses" is unverified (one invocation found). File-too-large shares (56% Nornspun, 44% Momentum) are within-project, April-era. Magnitude low to medium.

**S16. Agent invention and unobserved claims (T25; medium; shared).**
Silence toggle (FR55/Decision 22), BYOK settings, speculative affordances; two of two audit headline findings false (2026-06-14); Urd self-correction. Persistence of inventions in PRD/decision docs is the Momentum-attributable part. "22/51" refutation counts came from the audit handoffs (not the memory files).

**S17. Environment collisions and bug-fix loops (T26; medium; shared).**
Fixer compiled in the live app's worktree (NoClassDefFoundError, lost message, conductor_fault); a fixer killed Steve's MainKt PID 4412; tests hit the live backend (493 leaked plists); drive-013 regression from the drive-012 fix; cmux close-surface footgun (2026-07-22). "Two-repo hand-assembled builds, no CI" is unsupported (nornspun-backend has .github); the PID 4412 kill is not drive-env-001/002.

**S18. Agent-composition cohort late and incomplete (T27; medium; Momentum design).**
06-14 audit: 47 confirmed (4 critical, 17 high), pipeline non-functional, routing empty, 3 of 9 base bodies missing; 67 backlog stories in one epic (now 54). The 05-16 sprint did ship the builder, three bodies and resolve code the same day. The manifesto concept came from a pre-Momentum Nornspun prototype. Live compose-register-resolve first observed passing 2026-07-22 after a June attempt merged with AC1/AC6 unmet for missing fixture. "108 days" is correct for the specialist agents; "only 1 of 36 late stories touched a product repo" is supported by the late-sprint summaries (nornspun-agent-constitution).

**S19. Execution-engine research churn (T28; low; shared).**
Decisions DEC-028, 030, 031 (Hermes rejected, D7), 032 (Gas City adopted 05-22), 035 (superseded 05-30), 041 (deferral reaffirmed 08-25). The supersession was a documented discipline; the answer was a platform feature. "Six decisions" is roughly five. Benchmark fragility (answer leak; AVFL gate scores 33-51, not 13-51) is only loosely related.

**S20. Usage decay and long human latencies (T29; medium; shared).**
Monthly commits as above (gradual May-Jun slope, then July cliff; Aug concentrated on 5 days, real gap 08-25 to 10-24). Documented latencies: 3.5-day plan-to-activation (06-18), 11-day gate hang (07-13), "nights and weekends" quote. Chorgi ended at its peak month, 07-13; Nornspun's last commit 09-29. "About 100% of recent Momentum transcript time is maintenance" is unmeasured (Momentum-repo sessions are a biased sample) and should be dropped.

## 5. Mixed themes

**M1. Decision-grade presentation standard and companion gates (T07).** Benefit: seven written fork verdicts at the 07-13 plan gate (2026-07-21 21:08, held 2.6 days), compact Gas City gate (three forks, 12 KB, uncommitted), 06-18 end-gate approved in one turn (the retro called it appropriate). Cost: violations persisted (Steve twice "I don't see a question"), added ceremony, global rule is long. The game-prep transcript shows the rule auto-loaded, not demonstrably applied. Much of the benefit is reproducible with a short brief; Momentum's contribution is per-fork written-verdict forcing, visual HTML gate and codification.

**M2. Model tiering (T20).** Sonnet carries execution (Momentum 08-03 transcript: 6,691 Sonnet subagent turns vs 133 Fable and 48 Opus, from the transcript extraction). Policy lives in memory; model-routing.md is a stub; leaks by inheritance; [1m] entitlement breaks spawns (external). Pins are about 16 lines in 11 files now (23 was the 05-16 count); routing guide stale (dated 2026-03-14); the AVFL benchmark is 4.x-era (Haiku-low suffices only for consolidator/fixers; Haiku enum-medium false-passed 92/100). The "14 audit agents on Fable" and "even code should be sonnet" quote are in the Chorgi memory note, not the repo. No Haiku 5.x or Sonnet 5.x benchmarks exist.

**M3. Native Workflows displacing skills (T21).** Verified: three Workflow runs (44, 33, 3 agents = 80); the 44-agent run took 14.9 min; the 33-agent run took about 18.8h wall-clock. Steve praised the Fix/Verify/Integrate UI (2026-10-24) and said he does not "care much for the quick-fix" (2026-10-25). Corrected: the flagship run reused Momentum concepts (conductor constraints, momentum:dev fix-mode, dual-lens verify), so it is hybrid; the fix-pass record shows 12 fixed plus 3 stubbed with fixer 7 unaccounted, not "14 of 15"; "quick fix is not really quick" is from 2026-07-09 and concerns per-item overhead; "makes momentum obsolete?" is a 2026-09-19 release-notes question. Skill adoption (6 skills invoked) is in a window starting 08-24 and is not a full adoption measure.

**M4. Impetus (T30; low).** First load took 3+ minutes ("horrible and embarrassing"), persisted after a fix sprint, then pre-rendered in preflight; later an always-on rule with N-of-M headline. Epic momentum-impetus-session-orientation has 75 stories (45 done, 19 backlog, 11 dropped). "Minimal measured user value" is an inference, not a measurement.

## 6. By project

**Momentum on itself (Mar-Oct 2026).** Redesign (Epic 0) three weeks in; April peak (588 commits) with AVFL, TeamCreate-era sprint-dev, E2E validator thrash and duplicate spawns; May: decision documents, canvas, state-model migration, cohort DECs; June: conductor core (21/21), first live run on its own seams, companion gate surfaces; July: 07-13 cohort/conductor proof; August: DEC-040 honesty loop built in about one active day; Sep: no commits; Oct: end-gate fix burst, feature register, sprint closed FAILED, Workflows displacing skills.

**Nornspun.** 603 planning commits; ten-ish sprints. April: first code sprint, 57 of 71 E2E scenarios passed, 8 production bugs found; May: "lying and gaslighting" E2E; June-July: campaign-init iteration (the 05-30 sprint's 15 stories merged while the headline conversation was client-local hardcoded copy, per the campaign-init incident handoff); 07-13 12/12 merged but off main, 53 commits stranded in early August; DEC-040 discovery 08-02 (0 of 15 features); 07-13 merged 08-02, closed 08-10 after nine fixes; 08-20 sprint 14/14 merged to sprint branches, then 14 drive findings and a 5-6 week gate through 09-30; idle since. Benefits real (skeleton, forensic E2E, honest disclosure); outcome thin (dev-only, runtime LLM unreliable).

**Chorgi.** About two weeks planning (06-22 to 07-06), then one sprint 07-06..13: 15 stories, 118 findings, play-test on 07-09 found 11 findings, SCP added story 1-15, iPad review 07-13 found the iOS build unusable. 0 stories done, 113 commits unmerged, no retro or close, no activity since. No Chorgi build transcripts survive.

## 7. By component

| Component | Net observed value | Themes |
|---|---|---|
| Impetus (greeting/persona) | Mixed | T30; slow start, vocabulary overhead; N-of-M headline adopted late |
| sprint-planning / plan gate | Mixed | T01, T06, T07; planning AVFL catches defects, but 3.5- to 18-day gaps, huge artifacts, no goal enforcement until DEC-040 |
| create-story / Gherkin specs | Mixed to negative | T06, T11, T18; AVFL-validated specs prevent bad builds, but fatigue, spec drift, Gherkin fit under 5% |
| conductor (build) | Positive on throughput, mixed on outcomes | T09, T03, T04, T10 |
| conductor end-gate / merge gate | Mixed | T04, T07, T03; honest but heavy, wholesale approvals |
| sprint-dev (legacy) | Negative (retired 2026-07-21) | T10, T12; 17-ask firehose, duplication |
| dev / qa-reviewer / code-reviewer | Positive | T08, T09 |
| e2e-validator | Negative early, positive after DEC-029 | T11, T02, T08 |
| AVFL | Positive with caveats (non-convergence, cost, 4/20 overlap with human fixes) | T08, T10 |
| quick-fix | Negative to unobserved | T21 (Steve: "not really quick"; replaced by Workflow) |
| retro (DuckDB audit) | Mixed | T14 positive, T13 negative; stubs 0 shipped |
| assessment / decision / research | Positive | T14, T28 |
| refine / triage / intake | Mixed | T16, T14; intake capture cheap (1.5 min), backlog never drained |
| practice-ledger | Negative to mixed | T15 (92% closed stale), T05 |
| feature registry / tasting / closure | Unobserved (too new) with an honest-refusal signal | T03, T14 |
| agent composition (builder, constitutions, manifestos) | Negative to mixed | T27 |
| momentum-tools CLI | Positive (tests kept), but hot file | T17 |
| canvas dashboard | Unobserved or low | 05-03 delivery with design gaps; not seen in later transcripts |
| rules / memory | Positive for rules, negative for memory | T12, T22 |
| hooks | Unobserved (4 non-blocking errors, 0 denials in transcript window) | transcripts |
| plugin distribution | Negative | T19 |
| cmux integration | Negative | T26, memory notes |

## 8. Attribution analysis

**Momentum design (persists regardless of model).** Outcome-blind gates and the missing enforcement wiring (T01, T15); orphaned or later-arriving registry; sprint-sized batches that make verification a single scarce human event (T04, T03); decision/spec artifact volume built for LLM consumption (T06); self-feeding retro/triage loop (T05, T16); hardcoded paths and plugin-cache distribution (T19); tools without cross-skill contract tests (T18); the E2E validator's early design (T11, fixed).

**Implementation (fixable, mostly already addressed or cheap).** Retro extractor casts and window selection (T13), unbounded Workflow fan-out (T10), missing spawn-prompt constraints leading to environment collisions (T17), stale workflow text (T06), unfinished composition pipeline (T27).

**Model limitation of the era (may not apply to 5-series).** Fabricated receipts and overconfident "done" claims (T02, T25); egocentric-context collapse producing jargon and handles (T06); ignoring prose rules after compaction (T12); idle/SendMessage friction and AVFL seats going silent (T10); migration-sweep misses (T18); unbounded-sweep and invention behaviors. Evidence: the 08-03 build ran on Sonnet 5 and Fable 5 and still showed idle notices, non-reporting seats and NON_CONVERGENT AVFL, so some of this persists in the 5-series. The AVFL role/model benchmarks (4.x-era) have not been rerun on Sonnet 5.5 or Haiku 5.5.

**External or human factors.** Nights-and-weekends cadence, Steve's choice to close without tasting, Claude Code plugin resolution (#37862), [1m] entitlement, the Nornspun runtime LLM, BMAD upstream breaks, platform Workflows arriving.

**Counterfactual caution.** Plain Claude Code would have no story-count metric, no backlog, no retro, and none of Momentum's overhead, but also no closure refusal, no ledger-backed resume and no layered gates. Nobody has run the counterfactual; the game-prep and khaoss-io controls (different task types) show plain work being smooth (about 3 corrections across 40 messages in game-prep).

## 9. Data limitations

1. Raw transcripts exist only from 2026-08-24 (Momentum) and 2026-09-05/09-16 (others), earlier than the 09-26 estimate; only nine Momentum main sessions, two of which carry most substance. Earlier history rests on retro audits written by Momentum's own retro skill, which has a bias to find faults and whose extraction was 54-74% blind for later sprints.
2. Chorgi has no build transcripts, no retro or sprint summary, and the reason activity stopped is inferred.
3. Counts such as 91-104 done, 113 commits, ~740 vs ~760 product commits and "523" differ by date or scope; "523", "63k code lines", "98 touches" (103 actual), "83 agents" (80), "14 of 15" (12 plus 3 stubs), "54 of 241 idle turns" (52-54 of about 403 messages), "8 uses of /reload-plugins" (1 found), "22 + 21 fix confirmations" are unreproduced or corrected.
4. Several figures are secondary (DEC-040's discovery receipts, the "65+ stories, 0 shipped" claim, 0 of 29 retro stories) and were not re-derived.
5. Sprint name collision: Nornspun sprint-2026-07-13 and Momentum sprint-2026-07-13 are different sprints.
6. Costs in dollars or tokens are largely absent; cache-read volumes are not value-normalized. Commit counts are a weak activity proxy.
7. Verifiers did not check Nornspun's retros fully (self-correction claims) or Chorgi beyond one sprint.

## Appendix A: Claims that did not survive verification (or were weakened)

No theme was refuted by both lenses; all were confirmed or weakened. Specific claims dropped or corrected:
- T01: "91-104 done stories" as a DEC-040 figure (91 is DEC-040; 104 is current); "fix landed Aug" (value-floor adopted April, enforcement August); DEC-039 as a direct instance.
- T02: "led to verification-roles rule" is only evidenced for 08-20; "14/14 shipped then 14 findings" includes about 4 non-defect items.
- T03: "gate unanswered ~60 days" (about 4 days from end-gate; 60 days is build-to-end-gate); "registry empty" (absent); DEC-039 citation (should be DEC-040).
- T04: "goal_conditions nowhere on main" (false now); "11+ days stranded" as terminal; "features stranded so downstream plugin lacked them" (no evidence beyond the point-in-time quote); "no expiry/resume" partly stale.
- T05: "523" Jul-Sep product commits and "63k code lines" not reproduced; "going nuts" quote is about scope.
- T06: "accepts all defaults" generalization; "redesigned four times"; 15 cards wholesale.
- T08: "AD-8 defects"; "8 prod bugs in D3" partly verified only; "0 FP on HIGH in conduct-core" unverified; "27 divergences" is code review mostly.
- T09: "60-day gap resume"; "mostly single-pass" (71% REFIXED on conduct-core).
- T10: "29% zero-turn" and "101 idle" not reproduced; 426-agent episode is a Workflow fan-out.
- T11: "evalWithAI missing"; current validator no longer hardcodes the stack.
- T12: breadth of "chronic".
- T13: "54-74%".
- T14: "retros self-corrected" unverified; "kills" partially research verdicts.
- T16: "flipped 5 times", "121/103 mega-epics", "24 dropped" (proposed).
- T17: "1-day" lifespan; "98 touches".
- T19: "8 uses of /reload-plugins"; "chronic" file-too-large.
- T20: "6,691 of ~6,870 turns" appears in the transcript extraction but not the repo; "14 Fable audit agents" in a Chorgi note; pins count 23 (now about 16).
- T21: "14 of 15 fixes", "83 agents/34 findings in 15 min"; the two dated quotes are mis-timed.
- T22: "within ~20 min" (about 67 seconds); "3 session resets" (2 evidenced).
- T23: "F4 resolved by 1-15" (owned, not resolved); "47 fix vs 14 feat" cited to the wrong source (git).
- T24: "one-off" fabricated receipts; e2e-validator credit doubtful.
- T26: "no CI, hand-assembled builds"; "environments down between sessions" wording.
- T27: "hollow" overstated; "108 days" confirmed for specialists, not for 05-16 decisions.
- T28: "13-51" (33-51); "six decisions" (about five).
- T29: "100% maintenance" claim; "Aug 72" real gap is 08-25 to 10-24.

## Appendix B: Notable quotes

- "Sprints are completing. Stories are being done. Yet users cannot use Nornspun for anything useful today." (AES-002, 2026-04-11)
- "The pipeline did not lie to you - it told the truth and nothing could act on it." (nornspun-delivery-discovery synthesis)
- "I typically ignore almost the entire spec... it's just TOO MUCH." (Steve, 2026-04-13)
- "I'm fairly sure you're lying to me... you the sales person are lying and gaslighting me." (Steve, Nornspun 05-01)
- "E2E NEVER EVER EVER EVER looks at source code." (Steve, 2026-04-08)
- "We should absolutely check our skills and rules... They are NOT the final verifier. It is the HITL that does the final verification." (Steve, 2026-09-16)
- "Sadly this is not an 8 hour/day job for me. It's nights and weekends." (DEC-040)
- "If you always punt problems to the next sprint then you never have a functional sprint, right?" (Steve, DEC-040)
- "I'd rather we not keep going back and forth on this." (Steve, DEC-040 D1, on features vs epics)
- "I'm so confused when you talk about new seat, unseated, first seat second seat." (Steve, 2026-09-29)
- "closed without hands-on tasting verification of the 7 fixes - developer has not exercised them and the sprint had been open too long to hold." (sprints/index.json)
- "Let's please close it. This sprint has been open for too long to do much more." (Steve, 2026-10-28)
- "I don't actually care much for the quick-fix but you could read the quick fix and build out a similar workflow." (Steve, 2026-10-25)
- "Every high-severity defect that shipped or nearly shipped traces to a scoping/modeling gap, not an execution error." (07-13 retro audit)
- "The sprint looked done and didn't work." (campaign-init incident write-up)
- "Agent PASS is evidence, not acceptance." (verification-roles rule)
