# Sprint Transcript Audit — sprint-2026-04-27

**Retro date:** 2026-05-01
**Sprint completed:** 2026-05-01
**Data analyzed:** 266 user messages | 151 subagents | 249 errors | 30 team messages

**Auditor follow-up corrections incorporated (post-initial-draft):**
- Auto-compaction CONFIRMED on the 307-turn dev agent (record 484 of 539); the 199/149/143/138/128-turn agents did NOT compact. Compaction is rare (1/151 = 0.7%) but adds ~30 turns when triggered. Recovery worked correctly. (Updates S-14)
- The "AVFL Cluster A duplicate passes" finding is **WITHDRAWN** — same parent UUID (261d0611...), 11-minute spawn window. Cluster A is the legitimate avfl-3lens 6-agent topology (3 lenses × 2 framings = 6 validators), not duplicate runs. No recommendation needed.
- e2e-validator CLI errors are **NOT signature drift** (the `--priority` flag has been required since the command was added). The agent prompt invokes commands the way it "remembers" them — hardcoded-assumption error in the prompt. (Updates plugin-cache story analysis)
- AVFL fixer with 11 DuckDB errors **completed successfully** with structured fix log; errors were exploration tax, not failure. S-6 downgraded from HIGH to MEDIUM (DX improvement, not correctness).

## Executive Summary

The sprint shipped 8 stories, all merged to main with version 0.18.0 released. The post-merge AVFL gate was the load-bearing quality control: it caught 30 real findings (4 critical, 10 high), every one of which became a labeled fix commit (AVFL-001..AVFL-030 across commits 0ded486..3838e0d). Without that gate, the sprint would have shipped with `_compute_story_sha` reading a deleted legacy path and the next sprint-dev invocation HALTing on its own approval gate. The retrospective practice — corpus AVFL with mixed Enumerator+Adversary framing across 4 lenses — is doing exactly what it was designed to do.

The recurring failure mode is **state-file/contract drift**. A single planning-vs-execution mismatch (sprint-planning never wrote the per-sprint JSON file that sprint-dev expected to read) cascaded into multiple high-severity human interventions and triggered the largest story of the sprint (impetus-momentum-state-migration, 307 dev turns). The sibling pattern — vestigial sprint-log artifacts that the user had already decided to retire — required a separate cleanup story (retire-sprint-log-final-cleanup) and surfaced repeatedly as user corrections asking "are you sure we still need this?". The same theme appears in C-01 (architecture.md cross-section drift) and T-01 (singleton-guard ↔ TeamCreate side-channel coupling). The sprint's own state-migration story acknowledged this problem; the retro confirms it is the highest-leverage upstream fix.

Beyond state contracts, the audit surfaces three actionable themes: (a) the **research skill** needs a digest-presentation Q/A rebuild — the user gave 5+ separate corrections about being quizzed on material they had not read, gameable metrics like GitHub stars being trusted, and primary-source verification being skipped; (b) **specialist agents are missing** for AVFL (24 lens validators) and quick-fix Phase 2a (Architecture/PRD Discovery), all currently spawned as general-purpose with embedded role prompts; (c) **release UX is a gap** — the user asked "did you push 0.17.3?" and "what is our momentum skill for these releases?" — a deterministic release skill exists only as a rule. These three are the priority fix candidates for next sprint.

## What Worked Well

### W-1. Post-merge AVFL gate caught what per-story dev cycles missed (R-01, R-02, T-02)
**Description:** The post-merge AVFL run on the integrated sprint changeset caught 30 real findings (4 critical, 10 high), including AVFL-001 (`_compute_story_sha` reading deleted legacy path) confirmed by 8 separate validator findings across 4 lenses. Every finding became a labeled fix commit; convergence was complete.
**Evidence:** `/tmp/sprint-2026-04-27-avfl-findings.md` — 8 validators (Enumerator+Adversary on structural/accuracy/coherence/domain). Score 0/100 Failing pre-fix, all 30 findings remediated in commits 0ded486..3838e0d. AVFL-003 specifically caught the migration sweep gap: 9 files still referenced deleted legacy paths after Wave 1 dev claimed AC6 ("all 15 skill workflows updated") complete.
**Recommendation:** KEEP. Mixed Enumerator+Adversary framing across 4 lenses is load-bearing — only the Domain Adversary lens caught AVFL-001 (a runtime contradiction). Cross-lens consensus is what makes the gate trustworthy.

### W-2. QA reviewer caught cross-story integration regression (R-02)
**Description:** QA reviewer (105 turns, 444 live tests) caught a cross-story regression: `test_sprints_path_resolves_to_momentum` (added by impetus-momentum-state-migration) created a fixture without an `approvals` key, broken by the approval gate added in sprint-planning-adds-per-story-approval-gate — same sprint, two stories touching `cmd_sprint_activate`, neither dev agent updating the other's tests.
**Evidence:** `agent-summaries.jsonl` line 45. Verdict FAIL with file:line attribution. Per-story dev cycles could not have detected this in isolation.
**Recommendation:** KEEP. Running QA gate on the merged sprint changeset (not per-story) catches wave-vs-wave regressions that the EDD/TDD story cycle structurally cannot.

### W-3. E2E validator separated implementation defects from spec-quality defects (R-03)
**Description:** E2E validator (126 turns) returned PASS (31 of 41 scenarios passing, 10 MANUAL legitimately requiring live retro runtime) but surfaced 4 spec-quality defects: missing `momentum-tools sprint show` command, unmeasurable latency budget, asserts-on-silent-workflow, and 6 outsider-test scenarios that verify agent-definition wording rather than observable behavior.
**Evidence:** `agent-summaries.jsonl` line 39. Did not rubber-stamp; did not over-call FAIL.
**Recommendation:** KEEP. The spec-quality channel feeds back into create-story / Gherkin generation. The "outsider test" finding (harden-sprint-dev-phase5) needs follow-up: Gherkin generation for agent-definition-only changes needs different scenario shapes.

### W-4. Multi-turn human-in-the-loop sprint shaping converged on the right plan
**Description:** After back-and-forth on sprint composition the user explicitly approved the agent's recommendation: "I agree with your recommendation" and confirmed reliability-first ordering. Terse approval menu UX ("A1", "B+ and add the state migration story", "Fix all legit and move on", "wave 2") allowed extremely fast iteration in long workflows.
**Evidence:** Repeated terse approvals across the sprint (auditor-human finding, severity low). User has internalized the menu/option-letter convention.
**Recommendation:** KEEP. Continue menu-driven prompts; they are the highest-throughput interaction pattern in this practice.

### W-5. Research-then-verify pattern (intentional duplication)
**Description:** The multi-agent-deployment research session deliberately spawned a verification agent (113 turns, 10 errors) to fact-check an earlier research agent's corpus claims for Goose/ForgeCode/Gemini.
**Evidence:** `agent-summaries.jsonl` agents `a109a095...` (research) + `a06befcf...` (verification).
**Recommendation:** KEEP. This is intentional — and the pattern caught real corpus errors. Refinement: the verification agent could be informed by which sources the research agent found dead (high WebFetch 404 rate suggested filterable signal was already on the table).

### W-6. AVFL validator prompts produce attributable structured findings (P-01, P-02)
**Description:** Eight AVFL validators produced structured JSON output with stable IDs (e.g., STRUCTURAL-ENUM-001), severity, dimension, location, description, suggestion. Cross-lens deduplication produced clean "Confirmations: 8" counts. QA reviewer prompt produced per-story AC matrices with Status + Evidence columns — every VERIFIED entry cited file:line, grep result, or live test execution. PARTIAL classification protected the reviewer from over-claiming verification.
**Evidence:** All 8 AVFL agents (lines 4,5,6,10,12,14,16,18). QA reviewer line 45.
**Recommendation:** KEEP. Current AVFL and QA reviewer prompt structures are working — no changes recommended.

### W-7. Re-validation after fix application caught fix-introduced regressions (C-02)
**Description:** Mid-fix AVFL re-run caught a defect the singleton-guard fix introduced: the fix prose said "Do NOT use TeamCreate" but the guard reads `~/.claude/teams/<slug>/config.json`, which is written only by TeamCreate. Required a third pass to revert to `TeamCreate(cardinality=1)` for the documenter so the guard's contract holds.
**Evidence:** Team-messages timestamps 2026-05-01T18:15-18:20 (AVFL adversary/enumerator on singleton-guard fix) followed by 19:05 reconcile pass.
**Recommendation:** KEEP. Re-validation after fix is necessary and was load-bearing.

## What Struggled

### S-1. State-file/contract drift between sprint-planning and sprint-dev (HIGH)
**Description:** Sprint-planning and sprint-dev had a contract break that shipped to the user: branches deleted before activation, per-sprint JSON record never written, dependencies field missing. The user discovered this and asked the agent to consult prior architectural decisions — agent had not done so.
**Evidence:** Direct user quotes: "I ran into this issue and I can't figure out why: 3 gaps between sprint-planning and sprint-dev — branch deleted before activation, per-sprint JSON record never written, dependencies field missing"; "Do we need a per-sprint file? I thought we were moving away from that. Can you read up on our decisions and such...". Same theme: "I'm fairly certain our plan was to get rid of the sprint log totally. If we have no need for it outside of retros then it is pointless."
**Root cause:** No enforced consultation of `decisions/` before proposing fixes. No integration test across skill boundaries (sprint-planning output → sprint-dev input contract). Vestigial state files (sprint-log) coexist with the new direction without explicit retirement signal in workflows.
**Recommendation:** FIX. (a) Make the impetus-momentum-state-migration story critical, not high — it is the upstream root cause. (b) Add a workflow rule that before proposing fixes touching state files, the agent must cite the most recent decision document for that artifact. (c) Add cross-skill contract tests (output of skill A consumed by skill B should be schema-validated end to end).

### S-2. Same-defect-class sweep is not automatic after a fix (HIGH)
**Description:** After the sprint-planning/sprint-dev fix landed, the user had to ask: "What about the rest of our momentum skills, do any of them reference state files that don't exist?" The agent did not naturally trigger an upstream/sibling-skill audit.
**Evidence:** Direct user quote above. Reinforced by AVFL-003 (Wave 1 migration claimed AC6 "all 15 skill workflows updated" but missed 9 files — same defect class, only AVFL caught the sweep gap).
**Root cause:** Quick-fix completion does not include a sibling-skill audit phase. Migration-class story ACs do not require a sweep-verification artifact (e.g., grep proving zero residual references).
**Recommendation:** FIX. (a) Add to quick-fix or upstream-fix completion: "scan for analogous broken-contract patterns elsewhere". (b) For migration-class stories, add to create-story expectations: sweep-verification AC must include the exact grep/search that proves zero residual references.

### S-3. Research skill Q/A has the wrong shape (HIGH)
**Description:** momentum:research Phase 4 quizzes the user on raw research material the user has not read. Multiple high-severity user corrections on this single failure mode.
**Evidence:** Direct user quotes:
- "How could I possibly know if I agree with something I haven't myself researched? I would think the Q/A would be perhaps a presentation to me about what various researchers found and an open question about what questions I have rather than the agent asking me my own opinion on research I haven't looked at at all."
- "Tell me what else we haven't talked much about with this research?"
- "What else did we miss in my questions here about ECC?"
**Root cause:** Phase 4 collapses synthesis too aggressively, hiding sub-topics the user would interrogate. Asks for opinions instead of presenting findings.
**Recommendation:** FIX. Phase 4 must (a) present a structured findings digest first, (b) include a "topics-not-yet-discussed" section, (c) ask open redirect questions ("what should we dig into?") rather than opinion-extraction questions.

### S-4. Research subagents accept claims at face value (HIGH)
**Description:** Research subagents leave [UNVERIFIED] tags where a single repo search would resolve. Trust gameable metrics (GitHub stars) over commit cadence / contributor distribution / downloads.
**Evidence:** Direct user quotes:
- "I'm concerned that there wasn't enough verification of any of these claims. It seems like simple searches of repos could have confirmed or falsified claims... No bmad 6.4.0 has been released and a simple search of the repo would have validated that..."
- "I'm seeing over and over that many of the AI projects are faking their github stars... github stars and many other metrics should be wholly thrown out. The actual commits, bug fixes, etc. are a better metric. Not really gamed as easily."
- 20 WebFetch 404s in `agent-a109a095...` from training-data hallucinated docs paths.
**Root cause:** Research workflow lacks an enforced "verify against primary source" step. No source-quality heuristic for AI/OSS maturity claims. No retry/backoff/fallback when WebFetch hits 404s.
**Recommendation:** FIX. (a) Add a verify-via-primary-source step before any [UNVERIFIED] is allowed to ship. (b) Encode the "discard gameable metrics" rule directly in the research subagent prompt with concrete substitutes (commits, contributor distribution, downloads). (c) Build a deadlink filter so the verification agent doesn't re-walk the research agent's 404 trail.

### S-5. Specialist-agent gap (general-purpose with embedded roles) (HIGH)
**Description:** AVFL spawned 24 lens-validator agents + 6 fixers + 4 consolidators (34 total AVFL agents). Only 4 use specialist agent_types; 30 are general-purpose with embedded role definitions. Quick-fix Phase 2a similarly spawns 4+ general-purpose agents per fix (Architecture Discovery, PRD Discovery, Architecture Update, Story Revision).
**Evidence:** 8 AVFL validators, 6 fixers (turns 9–138), 4 consolidators. Quick-fix examples: `agent-a358baf...` (Architecture Update, 30 turns), `agent-a6d3a650...` (Architecture Discovery, 13 turns).
**Root cause:** Every general-purpose spawn pays the tool-discovery cost and re-loads framework references (validator-adv/SKILL.md, validator-enum/SKILL.md, framework.json) inside the prompt body.
**Recommendation:** FIX. Promote AVFL Adversary, AVFL Enumerator, AVFL Fixer, AVFL Consolidator, Architecture Discovery, PRD Discovery, Architecture Update, and Story Revision to specialist agent types. Saves tokens per spawn and reduces per-agent setup error.

### S-6. DuckDB schema brittleness — recurring trap (MEDIUM, downgraded from HIGH)
**Description:** AVFL fixer agent `agent-a53b5da3682d02c4b` had 11 DuckDB query errors against transcript JSONL: 'Conversion Error: Expected ARRAY, but got VARCHAR' on `json_extract` of `message.content`, 'Binder Error: Referenced column ts not found' (column is `timestamp`), 'Referenced table message not found'. Multiple parallel duckdb calls cancelled. **Agent COMPLETED successfully despite errors** — final assistant message contains a full structured fix log [F-001]..[F-004]. Errors were exploration-phase trial-and-error SQL refinement, not failure indicators.
**Evidence:** `agent-a53b5da3...` 11 errors, 171 transcript records, structured fix log in final message. Pattern: agents hand-craft SQL without a stable schema reference; the content-can-be-string-or-array problem is recurring.
**Root cause:** No query helper or stable schema reference for transcript JSONL. Agents re-derive the schema each time, hit the same gotchas. ~11 wasted tool calls per encounter.
**Recommendation:** FIX (DX improvement, not correctness). Build a `transcript-query` helper (skill or library) that exposes typed accessors and handles content-string-vs-array. Encode in the AVFL fixer / retro skills as the canonical way to query transcripts. Lower priority than originally classified — does not affect deliverable quality, only iteration cost.

### S-7. Wave 1 migration claimed all consumers updated, missed 9 files (HIGH)
**Description:** AVFL-003 caught migration sweep gap: `_compute_story_sha` was patched at cd286f3 BEFORE AVFL ran, but AVFL caught the same path migration in 8+ other call sites. Files missed: `sprint-dev/workflow.md` (3 sites), `intake/workflow.md`, `quick-fix/workflow.md` (3 sites), `distill/workflow.md`, `dev/workflow.md` (2 sites), `plan-audit/workflow.md`, `feature-breakdown/workflow.md`, `e2e-validator.md`, `sprint-planning/workflow.md` (2 sites + undefined template var).
**Evidence:** Sprint commits 0ded486..3838e0d are 8 fix commits applying AVFL-001..AVFL-027 (17 distinct AVFL IDs).
**Root cause:** AC6 ("all 15 skill workflows updated") had no verification artifact requirement.
**Recommendation:** INVESTIGATE → FIX. See S-2 recommendation (sweep-verification AC for migration stories). This is the same defect class.

### S-8. Co-touch story collisions on shared workflow files (MEDIUM)
**Description:** retro-team-singleton-guard and fix-retro-documenter-replication-defect both mutated the same Phase 4 block in retro/workflow.md. Each fix was unaware of the other's structural assumption. AVFL caught 10 cross-lens contradictions (workflow.md edited 7 times in 5 minutes flipping between three topologies). Required a third pass post-AVFL to reconcile.
**Evidence:** Commits d2b7e38, b38d75c, 7ed927a; team-messages 2026-05-01 entries 11–20; AVFL-002 quote: "Under any reading: the team config will have at most 3 members and the guard's exactly-4 assertion will HALT every retro run."
**Root cause:** Sprint-planning does not detect overlapping `touches` on the same file across stories. The singleton-guard's contract (reads team-config side-channel) is coupled to its declared topology by an implicit channel.
**Recommendation:** FIX. (a) Add sprint-planning lint: if two stories' `touches` arrays overlap on a SKILL.md file AND both are skill-instruction change-types, emit a "co-touch reconciliation needed" warning. (b) Co-locate side-channel contracts (singleton guard's team-config dependency) with the topology they assert about, or surface the contract explicitly in the spec.

### S-9. Architecture.md cross-section drift (MEDIUM)
**Description:** Two same-day editHistory entries asserted contradictory final states for per-story .md location (AVFL-007). Wave 2 retro topology section in architecture.md still said "Spawn 4 agents in parallel via TeamCreate" — exactly the pattern fix-retro-documenter-replication-defect rejected (AVFL-008). Caught only by the cross-document AVFL coherence lens.
**Evidence:** AVFL-007, AVFL-008. Required reading multiple sections of the same file plus comparing against workflow.md.
**Root cause:** No cross-section consistency check on architecture.md writes. Per-story reviewer doesn't cover coherence dimension.
**Recommendation:** FIX. Add to architecture-guard skill: list all editHistory entries within last 7 days; flag contradictory claims about the same artifact. Alternatively, gate architecture.md writes through a sole-writer agent (sprint-manager pattern).

### S-10. Eval coverage gaps — declared but not written (MEDIUM)
**Description:** AVFL-013 and AVFL-014 caught 4 missing eval files across 2 stories. Both stories declared eval files in `touches` but dev agents did not write them. QA reviewer did NOT catch this — verified evals existed AFTER fix commits added them, not before.
**Evidence:** AVFL-013 (retro-team-singleton-guard, 2 evals), AVFL-014 (qa-reviewer, 2 evals).
**Root cause:** No structural pre-merge check that `touches` entries actually exist as non-stub files. QA reviewer's per-AC matrix can be satisfied by the AVFL fix commits, masking the original gap.
**Recommendation:** FIX. Add `momentum-tools sprint verify-evals --slug <slug>` (or similar) that confirms every `touches` entry exists and is non-stub before allowing a status transition to review. Cheaper than relying on AVFL.

### S-11. Lost parallelism across general-purpose subagents (MEDIUM)
**Description:** Tool-results-to-assistant-turns ratio for 131 general-purpose agents — min 0.50, p25 0.62, median 0.72, p75 0.81, max 0.97. No agent had a ratio > 1, meaning no single assistant turn produced multiple tool calls in parallel on average.
**Evidence:** Aggregate from agent-summaries.jsonl across 131 general-purpose agents.
**Root cause:** Despite the project rule "parallelism is expected", agent spawn-time prompts don't reinforce it with examples. Agents default to sequential tool calling.
**Recommendation:** FIX. Add example-driven parallelism guidance to the highest-volume spawn prompts (research subagents, AVFL validators, dev-story).

### S-12. Permission denials show pattern of attempted git reset --hard (MEDIUM)
**Description:** 13 permission-denied errors total (9 Bash, 1 Edit, 4 generic). 4 were `git reset --hard afc097c` — agents trying to recover from earlier failures or roll back exploratory changes.
**Evidence:** `errors.jsonl` aggregated.
**Root cause:** Pre-merge git reset is correctly blocked by safety policy. But 4 agents independently tried it — suggests dev/fixer prompts don't tell agents to use `git revert` (new commit), or agents are overusing exploratory commits and trying to clean up.
**Recommendation:** INVESTIGATE. Add to dev-story / fixer prompts: "if you need to undo a commit, use `git revert <sha>` (creates a new commit). `git reset --hard` is blocked and will fail." Plus encourage smaller, more deliberate commits to reduce the urge to roll back.

### S-13. "File has not been read" before Edit — recurring across 7 agents (LOW)
**Description:** 7 distinct agents tried to Edit a file before Read'ing it. Recoverable but recurring efficiency loss.
**Evidence:** Affects both root sessions and subagents (`agent-af3d3114...`, `agent-a1af8296...`, `agent-ae6c88ec...`, `agent-a55f10fa...`).
**Root cause:** Common LLM mistake — when given an "edit X" instruction, jumping to Edit before Read.
**Recommendation:** INVESTIGATE. Could be addressed in a session-level pre-flight rule: "always Read before Edit, even if you wrote the file in a prior turn — your scratch state isn't shared with the tool".

### S-14. Largest dev agent (307 turns, 1094 KB) on the most complex story (MEDIUM)
**Description:** impetus-momentum-state-migration required 2 dev-skill agents: `agent-a1af82966...` (307 turns, 6 errors, 1094 KB — largest in sprint) and `agent-ae8cc7d8d...` (97 turns, 6 errors). Second agent's last message: "I need to stop and explain. Task 2.8 requires deleting `_bmad-output/implementation-artifacts/stories/` to enforce the single-source-of-truth invariant (AC #11). The deletion is being blocked by permissions."
**Evidence:** Dev agent transcript sizes. 3.5x the next-largest dev agent (199 turns). **Auto-compaction CONFIRMED**: transcript record 484 of 539 is the explicit "session is being continued from a previous conversation that ran out of context" marker. Split: 276 assistant messages BEFORE compaction, 31 AFTER. Compaction summary preserved primary intent; agent terminated normally with structured `AGENT_OUTPUT_START` block. Only 1 of 151 agents (0.7%) experienced compaction this sprint — the other 5 high-turn agents (199/149/143/138/128) completed within original context.
**Root cause:** Story scope exceeded a single agent's effective context. Cost decomposes into: (a) intrinsic story complexity (~270 turns), (b) auto-compaction overhead (~30 turns of context re-derivation), (c) blocked-on-permission re-spawn (~97 turns for the second agent). Permission/policy mismatch with story requirements (AC required a `rm -rf` not authorized in the policy).
**Recommendation:** FIX. For migration-class stories that touch >10 files or require destructive ops, sprint-planning should split into ≤2 stories with a checkpoint, or annotate the story with required-permission additions for sprint-dev to surface upfront. Compaction worked correctly when triggered — no compaction-resilience gap; the fix is at planning time, not runtime.

### S-15. Release UX gap — no discoverable release skill (MEDIUM)
**Description:** User had to ask "Did you push the latest 0.17.3?" and "What is our momentum skill for these releases?" Version bump on merge-to-main exists as a rule (`.claude/rules/version-on-release.md`) but the user expected a discoverable skill ("the semver skill concept").
**Evidence:** Direct user quotes above.
**Root cause:** No `momentum:release` skill. The version-bump rule is hidden in rules/, not surfaced as a callable workflow.
**Recommendation:** FIX. Create a `momentum:release` skill that: (a) computes correct semver bump from changeset, (b) updates `plugin.json`, (c) commits the bump, (d) reports what will be pushed and asks for confirmation, (e) pushes after approval.

### S-16. Audit-extract truncates first_prompt at 400 chars (META, MEDIUM)
**Description:** All `first_prompt` fields in `agent-summaries.jsonl` are exactly 400 chars (max). The truncation hides lens/role/specialist suffixes that distinguish otherwise-near-identical AVFL prompts. Auditor's own duplication analysis was overstated as a result.
**Evidence:** Auditor-execution batch 2 finding (self-report).
**Root cause:** Audit extraction script truncates at 400 chars without hashing or capturing a stable identity field.
**Recommendation:** FIX. Either (a) capture full prompts (compressed), or (b) capture a stable prompt-hash + role-tag pair for reliable deduplication analysis.

### S-17. Two zero-turn subagents — investigate or extraction bug (LOW, INVESTIGATE)
**Description:** 2 subagents recorded `assistant_turns=0`, `error_count=0`, empty `first_prompt`, but non-trivial size_kb (439 and 520 KB). Either silently killed/interrupted, or extraction tooling missed extracting them.
**Evidence:** `agent-ae1eb8558...`, `agent-af974e6d3...`.
**Root cause:** Unknown — either spawn-side or extraction-side.
**Recommendation:** INVESTIGATE. Pull the full transcripts; if extraction bug, fix the extractor; if real abandons, capture the trigger pattern.

## User Interventions

The following user interventions are the highest-signal redirections — each indicates a gap the agent should have caught.

### Strategic / Decision-Level
1. **Multi-agent-host portability decision**: "I need to expand my agents beyond merely claude-code for momentum, even for my own development. I want to target no less than Claude Code, OpenCode, Codex, Gemini, Goose and ForgeCode... my primary push for this research is less about the recommendation and MORE about how it is being done." → Project-level pivot. Multi-host portability is now a goal; agents had not surfaced this independently.
2. **State-migration as gate, not just high**: "My thinking was that it may be high but it's necessary before we can do canvas because canvas reads from it. It also holds up impetus updates." → Planner did not reason about transitive blocking dependencies.
3. **GAN ↔ AVFL connection**: "I'm actually extremely interested in the GAN piece. It seems very similar to what we're trying to do in our verification phase. I'm not sure what to do here but maybe you could add this entire thing to an analysis paper showing the gaps in our decisions." → User connecting research to practice; agents didn't proactively flag adversarial-ML literature.

### Practice-Level Corrections
4. **Sprint-log retire**: "I'm fairly certain our plan was to get rid of the sprint log totally. If we have no need for it outside of retros then it is pointless."
5. **Per-sprint file retire**: "Do we need a per-sprint file? I thought we were moving away from that. Can you read up on our decisions and such and see if we were moving away from that?"
6. **Sibling-skill audit**: "Yes but before you do, does this permanently fix the mismatch? What about the rest of our momentum skills do any of them reference state files that don't exist?"
7. **Branch lifecycle confusion**: "Wait are you saying branches are not created by planning?" → User's mental model contradicted by agent's account; spec drift between sprint-planning behavior and what the user/skills assume.
8. **Orphan story handling**: "I think the state migration is a HUGE gap but it seems like it might be a single story. Not all stories are part of a feature. Why not just /momentum:intake it as a story and have the rest of these stories depends_on that one?"

### Research / Workflow Shape Corrections
9. **Q/A digest, not opinion-extraction**: see S-3 quote.
10. **Discard gameable metrics**: see S-4 quote.
11. **Verify primary sources**: see S-4 quote.
12. **Surface latent topics**: "Tell me what else we haven't talked much about with this research?", "What else did we miss in my questions here about ECC?"
13. **Subagent fan-out + AVFL by default**: "Please use subagents and have each produce a document of appropriate sort. Please save the documents to the base momentum directory and please run avfl on both completed documents." → User had to explicitly request this; should be the default for analysis above some threshold.

### Tool / UX Friction
14. **Release ask**: "Did you push the latest 0.17.3?" / "What is our momentum skill for these releases?"
15. **Worktree/branch hygiene**: "Make sure we don't have any branches locally or remotely or worktrees that should be deleted hanging around" → recurring manual ask.
16. **Completion acknowledgement gap**: "Did you do that already?" → User unsure whether action completed.
17. **Benchmark capture**: "Can you please use DuckDB to review two previous Sprint Planning sessions, please capture everything required during that session including the original state, even the git hash along with inputs and outputs. I'd like to use these for benchmarks." → No skill captures pre/post state + inputs/outputs as a benchmark recipe.
18. **Session-handoff prompts**: "let's prepare a prompt for the next session to begin sprint planning, make it easily copy/pasteable" → Cross-session continuity is a recurring need.
19. **Low-info session filtering**: "6d6ec9b2 seems fairly worthless. Is there an older one that can be used?" → Need richness/length heuristic when sampling sessions.

### Successful Patterns (Preserve)
20. **Terse menu-driven approval**: "A1", "B+ and add the state migration story", "Fix all legit and move on", "wave 2", "bundled", "go", "yes" — consistently fast-iteration UX. Confirmed working.
21. **Multi-turn shaping**: "I agree with your recommendation" after back-and-forth on sprint composition — confirms iterative human-in-the-loop produces good plans.
22. **Amend in place**: "Amend in place" — user explicitly directed an amend rather than a new commit; solo-dev local-commit context warrants exception. Agents should ask rather than refuse silently.

## Story-by-Story Analysis

### impetus-momentum-state-migration (LARGEST, MOST COMPLEX)
- 2 dev agents required: 307 turns + 97 turns (largest in sprint, 3.5x next biggest)
- Permission block on `rm -rf _bmad-output/implementation-artifacts/stories/` (AC #11 requires it)
- Likely auto-compaction mid-execution
- Consensus across audits: scope was too large for a single dev agent; should have been split or had checkpoint
- Connected to S-1, S-2, S-7 (state-file/contract drift theme)

### sprint-planning-adds-per-story-approval-gate
- Caused R-02 cross-story regression: added approvals key to fixture, broke a test added by impetus-momentum-state-migration
- Co-touched `cmd_sprint_activate` with the migration story; neither dev updated the other's tests
- Caught only by post-merge QA gate — per-story dev cycles structurally cannot catch this

### retro-team-singleton-guard + fix-retro-documenter-replication-defect (CO-TOUCH COLLISION)
- Both mutated the same Phase 4 block in retro/workflow.md
- 7 edits in 5 minutes flipping between three topologies (T-01)
- Singleton guard reads `~/.claude/teams/<slug>/config.json` (written only by TeamCreate); the fix prose said "Do NOT use TeamCreate" — fix-introduced regression
- Required a third reconciliation pass after AVFL caught it
- Connected to S-8 (sprint-planning lint for co-touch detection)

### harden-sprint-dev-phase5-spawn-prompts
- E2E validator surfaced "outsider test" finding: all 6 scenarios verify agent-definition wording, not observable behavior (R-03)
- Indicates Gherkin generation needs different scenario shapes for agent-definition-only changes
- Two declared eval files missing on first pass (AVFL-014); fixed in remediation commits

### retire-sprint-log-final-cleanup
- Connected to S-1 (state-file/contract drift): the user had already decided the sprint log was vestigial; this story was the cleanup
- E2E validator flagged spec asserting active provenance reporting workflow that only does silently — spec quality issue
- Successful execution; no thrash

### plugin-cache-staleness-detection
- E2E validator flagged unmeasurable latency budget in spec (R-03)
- e2e-validator agent (`agent-abf21938...`, 7 errors) hit `momentum-tools sprint stories: error: the following arguments are required: --priority` — **NOT stale signature drift** (`--priority` has been required since the command was added). The agent prompt invokes commands the way it "remembers" them. Hardcoded-assumption error in the validator prompt.
- Plugin-cache version lookup stale (0.16.0..0.17.3) — single-source-of-truth gap (e2e-validator does "find newest cached plugin" instead of reading the active version from `plugin.json`)

### retro-transcript-extraction-hardening
- Successful execution; the 400-char first_prompt truncation finding (S-16) is a related but separate gap

## Cross-Cutting Patterns

These are the themes that appear across multiple auditor reports and warrant the highest-priority next-sprint focus.

### CC-1. State-file/contract drift is the dominant root cause
**Appears in:** Human findings (5+ high-severity quotes), Execution findings (impetus-state-migration as largest, e2e CLI drift, plugin-cache version drift), Review findings (R-02 cross-story regression, T-02 sweep gap, C-01 architecture cross-section drift, C-03 missing evals).
**Synthesis:** The same root cause shows up in spec text, in workflow.md text, in CLI signatures, in test fixtures, in plugin cache version, in eval `touches` declarations, in editHistory entries — every place where two artifacts must agree about the same fact, they drift. The impetus-momentum-state-migration story is the right strategic response; the retro confirms it is the highest-leverage upstream fix.
**Action:** Promote state-migration to **critical**, not high. Follow with consolidated state-model architecture work.

### CC-2. Per-story dev cycles structurally miss cross-cutting issues
**Appears in:** R-02 (QA cross-story regression), T-02 (migration sweep gap), C-01 (cross-section drift), C-03 (missing evals), S-7 (Wave 1 sweep claim).
**Synthesis:** EDD/TDD per-story works for in-story behavior; it does not catch (a) wave-vs-wave regressions, (b) cross-section drift in long files, (c) missing-file gaps the AC implies but doesn't enforce, (d) sweep claims like "all N consumers updated". Post-merge AVFL is the load-bearing safety net. Without it, the sprint would not have shipped clean.
**Action:** Continue post-merge AVFL. Add structural pre-merge checks (eval-presence, sweep-grep) that are cheaper than AVFL but catch the most common gap patterns.

### CC-3. Specialist agents are systematically missing where role is well-scoped
**Appears in:** Execution findings (S-5 AVFL + quick-fix Phase 2a both general-purpose with embedded role), prompt-quality findings (P-01, P-02 confirm the role definitions ARE high quality — they just live in the prompt body instead of agent type).
**Synthesis:** The existing role prompts work — that's confirmed. The gap is they live in spawn-time prompt bodies rather than as specialist agent types. Token cost, cold-start cost, and per-agent setup error are all paid unnecessarily.
**Action:** Promote AVFL Adversary, Enumerator, Fixer, Consolidator, Architecture Discovery, PRD Discovery, Architecture Update, Story Revision to specialist agent types.

### CC-4. The research skill is the lowest-coherence skill in the practice
**Appears in:** Human findings (5+ corrections — Q/A shape, gameable metrics, primary-source verification, sub-topic surfacing, missing-topics digest), Execution findings (20 WebFetch 404s on a single research agent), no positive review findings.
**Synthesis:** Every other skill in the practice has at least one "kept" finding from the auditors; momentum:research has none. This is the most concentrated quality gap.
**Action:** Treat as a single skill rebuild. Phases need: structured digest first, sub-topics surfaced, primary-source verification step, gameable-metrics filter, deadlink filter, redirect-questions instead of opinion-extraction.

### CC-5. Practice operations (release, hygiene, completion ack) are under-automated
**Appears in:** Human findings (release ask, worktree/branch cleanup ask, completion confusion ask).
**Synthesis:** Three separate user asks point to the same gap: deterministic operational workflows that don't exist as discoverable skills. The user expected each one.
**Action:** Build `momentum:release`. Add a sprint-close hygiene routine (worktree/branch cleanup). Add explicit completion acknowledgements after multi-step ops in dev/quick-fix flows.

### CC-6. AVFL false-positive rate on Low severity is non-trivial (~50/50)
**Appears in:** Review finding F-01 (AVFL-027, AVFL-028, AVFL-030 are stylistic or past-tense-claim findings).
**Synthesis:** Low-severity AVFL findings are roughly 50/50 actionable vs stylistic. Cost is low (batched into fix commits) but signal degrades.
**Action:** Tighten validator prompt to skip purely tonal findings unless part of a cluster. Or empower the consolidator to filter style-only / past-tense-claim findings.

## Metrics

| Metric | Value |
|--------|-------|
| User messages analyzed | 266 |
| Subagents analyzed | 151 |
| Tool errors detected | 249 |
| Struggles identified | 17 |
| Successes identified | 7 |
| User interventions | 22 |
| Cross-cutting patterns | 6 |
| Stories shipped | 8 |
| AVFL findings remediated | 30 (4 critical, 10 high) |
| AVFL fix commits | 8 (0ded486..3838e0d) |

## Priority Action Items

Ranked by impact × actionability. Each item names a concrete next-sprint story stub.

### CRITICAL
1. **Consolidate state-model contract** — story stub: "consolidate-state-model-and-cross-skill-contract-tests" — Bundles CC-1 root cause: per-sprint JSON, sprint-log retirement, branch lifecycle, plugin-cache version source, all under one architectural decision. Add cross-skill contract tests (output of skill A consumed by skill B is schema-validated end-to-end). **The impetus-momentum-state-migration story should have been critical, not high.**
2. **Sweep-verification AC for migration stories** — story stub: "create-story-sweep-verification-ac-for-migration-class" — Encode in create-story expectations: any "all N consumers updated" AC must include the exact grep/search proving zero residual references. Address S-2, S-7, T-02 as a class.

### HIGH
3. **Rebuild momentum:research Q/A as digest-first** — story stub: "research-q-a-digest-first-rebuild" — Phase 4 presents structured findings + sub-topics + open redirect questions. Bundles S-3.
4. **Add primary-source verification + gameable-metrics filter to research subagents** — story stub: "research-subagent-primary-source-verification" — Bundles S-4. Includes deadlink filter, encoded substitute-metrics rule (commits / contributor distribution / downloads instead of stars).
5. **Promote AVFL + quick-fix roles to specialist agents** — story stub: "specialist-agents-avfl-and-quickfix-phase2a" — Address S-5. Eight specialist agent types: AVFL Adversary, Enumerator, Fixer, Consolidator + Quick-fix Architecture Discovery, PRD Discovery, Architecture Update, Story Revision.
6. **Build momentum:release skill** — story stub: "momentum-release-skill" — Address S-15 + CC-5. Computes semver bump, updates plugin.json, commits, asks before push.
7. **Build transcript-query helper / encode DuckDB schema** — story stub: "transcript-query-helper-stable-schema" — Address S-6. Typed accessors that handle content-string-vs-array; canonical query interface for retro/AVFL.

### MEDIUM
8. **Sprint-planning co-touch lint** — story stub: "sprint-planning-co-touch-detection" — Detect overlapping `touches` on shared files; emit reconciliation warning. Address S-8.
9. **Architecture-guard cross-section coherence check** — story stub: "architecture-guard-cross-section-check" — Add editHistory contradiction check; or sole-writer agent for architecture.md. Address S-9, C-01.
10. **Eval-presence pre-merge check** — story stub: "momentum-tools-sprint-verify-evals" — `momentum-tools sprint verify-evals --slug <slug>`. Address S-10, C-03.
11. **Story-too-large detection in sprint-planning** — story stub: "sprint-planning-story-size-heuristic" — For migration-class stories touching >10 files or requiring destructive ops, force split or annotate required-permission additions upfront. Address S-14.
12. **Sprint-close hygiene routine** — story stub: "sprint-close-worktree-branch-hygiene" — Periodic cleanup of stale worktrees/branches; runs at sprint complete. Address user-intervention #15 + CC-5.
13. **Audit-extract first_prompt full-capture or hash** — story stub: "audit-extract-first-prompt-full-capture" — Address S-16 (meta finding from auditor itself).
14. **Parallelism-by-example in spawn prompts** — story stub: "spawn-prompts-parallelism-examples" — Add example-driven parallelism guidance to highest-volume spawn prompts. Address S-11.

### LOW / INVESTIGATE
15. **AVFL Low-severity filter** — story stub: "avfl-consolidator-stylistic-filter" — Tighten validator prompt or empower consolidator to drop style-only / past-tense-claim findings. Address F-01, CC-6.
16. **Read-before-Edit pre-flight rule** — story stub: "session-rule-read-before-edit" — Address S-13.
17. **git revert guidance in dev/fixer prompts** — story stub: "dev-prompt-git-revert-guidance" — Address S-12.
18. **Two zero-turn agents — investigate** — story stub: "investigate-zero-turn-subagents" — Address S-17.
19. **Session-handoff prompt artifact** — story stub: "session-handoff-prompt-as-artifact" — Address user-intervention #18. First-class "next-session prompt" capture.
20. **Benchmark-capture-from-transcripts skill** — story stub: "benchmark-capture-from-session-transcripts" — Address user-intervention #17. Capture pre/post state + inputs/outputs as a benchmark recipe.
