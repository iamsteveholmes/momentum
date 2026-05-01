# Sprint Transcript Audit — sprint-2026-04-08

**Retro date:** 2026-04-10
**Sprint completed:** 2026-04-09
**Data analyzed:** 267 user messages | 105 subagents | 214 errors | 93 team messages

## Executive Summary

Sprint-2026-04-08 delivered all 12 stories across 3 waves in ~23 minutes of parallel dev execution — every story completed on its first dev pass without rework. The wave model, AVFL pre-activation checkpoint (14 real defects caught), and dev-skills agent quality represent the practice's strongest execution patterns. Three new skills (intake, assessment, decision) shipped cleanly. QA passed 346/346 tests. Architecture guard confirmed zero drift.

The sprint's central struggle was the E2E validator. It consumed 734 agent turns across 7 spawns, produced a 66% MANUAL rate on its first pass, and triggered the user's most intense frustrations — including a fundamental black-box enforcement failure where the validator inspected source code instead of executing through cmux. The user intervened at least 7 times on E2E alone, with corrections escalating from "is cmux not in our rules?" to "NEVER EVER EVER EVER looks at source code." The root cause was compounding: no cmux knowledge in the agent definition, optional language creating escape hatches, MANUAL used as a fallback instead of ERROR, and the validator being refined while simultaneously serving as a quality gate.

Beyond E2E, the sprint revealed systemic patterns: file-too-large errors accounted for 44% of all tool errors (95/214), workflow fidelity violations occurred in at least 5 places (inline execution instead of subagent spawns, missing parallelism, skipped steps), and the retro pipeline itself required 3 attempts (spawning 17 agents for 4 roles). The user's correction rate was 25-28% of substantive messages — roughly 1 in 4 interactions was a redirection. Priority actions: harden E2E validator contract with mandatory cmux and zero-tolerance MANUAL policy, add file-size guidance for known-large files, enforce workflow delegation rules, and add consumer-audit steps for subtractive stories.

## What Worked Well

### Wave-Based Parallel Dev Execution
**Description:** All 12 stories completed in exactly 1 dev pass each — clean 2-agent pattern (1 create-story + 1 dev-skills per story). 10 Wave 1 stories launched simultaneously via worktree isolation, completing in ~15 minutes. Waves 2 and 3 followed dependency ordering correctly.
**Evidence:** Git log shows 10 feat commits in a 13-minute window. Every story has exactly 1 create-story + 1 dev-skills agent with no rework loops. Dev-skills turns ranged 40-246 across stories.
**Recommendation:** KEEP — The parallel wave model is the sprint's strongest execution pattern. Zero rework on dev passes validates spec quality at the story level.

### AVFL Pre-Activation Checkpoint Caught 14 Real Defects
**Description:** Three validation lenses (structural, accuracy, domain fitness) ran against all 12 stories before dev agents activated. Found contradictory tasks in quality-gate-parity, wrong log counts in remove-agent-journals, non-existent paths in 8-3-gemini, hedged ACs, wrong change_type values, and missing sections.
**Evidence:** AVFL QA reviewer scored 62/100. Commit 081bea9: 13 files changed, 227 insertions, 181 deletions. 4 HIGH findings (task/AC contradiction, wrong log counts, wrong config file, wrong path), 6 MEDIUM, 4 LOW.
**Recommendation:** KEEP — Highest-value quality gate. Without this, dev agents would have implemented against broken specs. The 62/100 score (not inflated) shows the gate has teeth.

### QA Reviewer: Fast, High-Confidence Signal
**Description:** 346 tests, 346 passed, 0 failed, 0 skipped. Executed in ~5 minutes with 87 turns and 78 tool calls.
**Evidence:** QA reviewer verdict: PASS. Test suite correctly reflected remove-agent-journals deletion (16 log tests removed, 346 remaining all pass).
**Recommendation:** KEEP — Clean test pass provides fast feedback. The test suite adapts correctly to subtractive changes.

### Architecture Guard Drift Prevention
**Description:** Validated sprint changes against 6 architectural decisions (1d, 2a, 3a, 3b, 3d, 5a). Verdict: PASS.
**Evidence:** Execution time ~4 minutes. No drift detected.
**Recommendation:** KEEP — Low overhead, high confidence. Valuable even when it finds nothing.

### Post-Merge Fix Cycle Converged in One Iteration
**Description:** AVFL post-merge scan identified findings. Orchestrator spawned 5 parallel fix agents with scoped tasks. Re-scan confirmed all fixes. One iteration to convergence.
**Evidence:** Fix agents for trailing comma, dead log calls in epic-grooming, dead log calls in dev, stale references, sprint-dev refs — each completed correctly on first attempt.
**Recommendation:** KEEP — Fix-then-rescan pattern is well-designed. When scoped correctly, fix agents are efficient.

### Retro Team Collaboration Pattern (TeamCreate)
**Description:** 3 auditors forwarded findings to documenter, documenter asked 3 follow-up questions, auditors responded, document written — all in 7 minutes.
**Evidence:** 21 unique messages (from 70 raw, 3:1 duplication from TeamCreate replication). Documenter caught commit count discrepancy; three auditors converged on 52 commits/15 fixes (28.8%) after reconciliation.
**Recommendation:** KEEP — TeamCreate collaborative pattern worked as designed. Documenter's cross-check caught a data inconsistency before it entered findings.

### Agent Proactive Suggestions During Planning
**Description:** Agent proactively suggested the intake skill concept during planning; user approved immediately ("I like the /momentum:intake idea"). Decision-skill earned "Excellent!" after template review.
**Evidence:** User praise signals: "This looks great!" (story quality), "Excellent! decision-skill approved" (immediate approval), "Will this change go out with the next momentum release?" (downstream thinking).
**Recommendation:** KEEP — Agent adds value by suggesting adjacent improvements. Planning is a collaborative dialogue, not just ticket transcription.

## What Struggled

### E2E Validator: Black-Box Enforcement Failure (CRITICAL)
**Description:** The E2E validator repeatedly fell back to file inspection instead of black-box execution through cmux. Despite extensive specification work across 5 commits over 2 days, the agent found escape hatches — marking scenarios MANUAL instead of executing them, inspecting source code instead of running commands.
**Evidence:** User: "What you're describing he did was a total failure... the E2E NEVER EVER EVER EVER looks at source code. He is ALWAYS supposed to treat it as a black box." User: "Again why 15 manual. Why are we struggling through this. Please hear me that this is NOT NOT NOT NOT acceptable."
**Root cause:** Compounding failures: (1) no cmux knowledge in the agent definition — the validator literally didn't know it could open terminal panes, (2) optional language ("If cmux is unavailable, mark as MANUAL") treated as opt-out by the agent, (3) no explicit failure path — when unsure, agent defaulted to MANUAL instead of ERROR, (4) no global cmux rule existed for any agent to reference.
**Recommendation:** FIX — Mandatory cmux execution in agent definition with zero escape hatches. MANUAL only for scenarios requiring live user interaction. ERROR for infrastructure gaps, never MANUAL.

### E2E Validator: Excessive Cost and Spawn Waste (HIGH)
**Description:** 7 E2E validator instances spawned for one 12-story sprint: 2 full runs, 3 targeted re-checks, 1 abandoned (470KB loaded, 0 turns), 1 revalidation. Combined 734 agent turns. First full pass produced 66% MANUAL rate (31/47 scenarios), yielding a misleading PASS verdict. Contradictory scenario counts across runs (57 vs 47).
**Evidence:** E2E validators averaged 104.9 turns and 88.7 tool calls — 3x the general-purpose agent average. Targeted re-checks (27 turns) massively outperformed broad re-runs (175+ turns). The abandoned validator loaded 470KB of context but never processed a single turn.
**Root cause:** Validation scope not narrowed between passes. No idempotency — each re-run spawned fresh agents. Abandoned validator wasted context budget. MANUAL rate inflated passing results.
**Recommendation:** FIX — One validator per review cycle with scope narrowing on re-checks. Add MANUAL rate threshold (>20% triggers self-check). Prefer targeted re-checks over broad re-runs. Add scenario count reconciliation between passes.

### File-Too-Large Errors: 44% of All Tool Errors (HIGH)
**Description:** 95 of 214 errors (44%) were "File content exceeds maximum allowed tokens." Token counts ranged from 10,387 to 41,982. Errors concentrated in validation/retro phases (T17: 18 errors, T22: 28 errors). Same large files hit repeatedly by different agents.
**Evidence:** Error bursts correlate with validation (49 errors at T17) and retro (60 errors at T22) — 51% of all errors. Development hours had only 30 errors total.
**Root cause:** Agents attempt to Read large files without offset/limit parameters. No guidance specifies known-large files or required chunking strategies. Validation and retro agents inherently need to read large JSONL and transcript files.
**Recommendation:** FIX — Add file-size guidance to agent definitions for validation and retro roles. Known-large files (JSONL logs, transcripts, sprint indexes) should specify recommended offset/limit patterns. Consider a "file manifest" in sprint metadata listing files and approximate sizes.

### Workflow Fidelity Violations: 5 Instances (HIGH)
**Description:** Workflow steps that specify "spawn subagent" were executed inline by the orchestrator in at least 5 cases: E2E validator run inline instead of spawned, research agents run sequentially instead of parallel, dev agent implemented fix without EDD eval first, E2E validator phase in team review never executed at all, and parallelism not used where specified.
**Evidence:** User: "So a few things here, first I don't see a subagent" (E2E not spawned). User: "Do you run the other research in parallel?" (sequential execution). User: "Make sure to follow the dev TDD requirements" (EDD skipped). User: "But the E2E validator never ran. So what happened?" (step silently skipped).
**Root cause:** Orchestrator agents optimize for perceived efficiency — doing work inline feels faster than spawning. No runtime enforcement of delegation requirements. Silent step skipping has no detection mechanism.
**Recommendation:** FIX — Workflow steps marked "spawn" must be enforced, not advisory. Add workflow step completion checklist that orchestrators must acknowledge. Consider a workflow audit hook that detects inline execution of delegation-marked steps.

### Subtractive Story Consumer Cascade: remove-agent-journals (HIGH)
**Description:** Deleted sprint-log write infrastructure but missed consumer references, triggering 5 fix commits over ~3 hours: trailing comma in hooks.json, dead log calls in epic-grooming, dead log calls in dev workflow, residual stale references, sprint-dev refs.
**Evidence:** 5 fix commits (241c13e, fe47d83, b451068, 7eeb32b, 8db4398). Also broke hooks-global-distribution's hooks.json changes via trailing comma from array element removal.
**Root cause:** Story touches list was incomplete. Dev agent grep'd for direct references but missed indirect ones — workflow steps calling log commands, config arrays with trailing comma issues after element removal. Cross-story integration effects (hooks-global-distribution conflict) not covered by any quality gate.
**Recommendation:** FIX — Subtractive stories need a mandatory "consumer audit" step: grep ALL references to deleted artifacts (commands, paths, config keys) and include every consumer file in touches. Add cross-story integration validation to AVFL, especially for stories that delete shared infrastructure.

### Retro Pipeline Required 3 Attempts: 17 Agents for 4 Roles (MEDIUM)
**Description:** The retro workflow spawned a fresh team on each attempt — 4 documenters (identical prompts), 3 auditor-review, 3 auditor-execution, 3 auditor-human. All 9 auditor agents from early runs hit parse errors from malformed DuckDB output.
**Evidence:** 4 documenters share identical first 200 chars of prompt. All 9 early-run auditors produced parse errors — Python dict syntax (NULL, single quotes) instead of JSON (null, double quotes). First retro captured only 1 of ~30+ subagent sessions.
**Root cause:** No idempotency check — each retro run spawns fresh team without cleaning up prior. DuckDB serialization bug (Python repr() instead of json.dumps()) produced malformed output in early runs. Transcript extraction pipeline failed on worktree sessions.
**Recommendation:** FIX — Add idempotency to retro workflow (detect prior attempt, offer resume or clean restart). Fix DuckDB serialization to produce valid JSON. Harden transcript extraction for worktree session paths.

### Concurrent Write Contention on Shared Files (MEDIUM)
**Description:** 11 "File has been modified since read" errors during active dev waves when multiple worktree agents touched shared files (sprint index, hooks.json).
**Evidence:** 11 file-modified-since-read errors during Wave 1 parallel execution.
**Root cause:** Worktree isolation protects source code but not shared config files. Multiple agents reading and writing sprint index and hooks.json simultaneously.
**Recommendation:** FIX — Identify shared mutable files and either serialize access or use append-only patterns. Sprint index and hooks.json are the primary contention points.

### Agent Spawn Waste: 6 Abandoned Agents (MEDIUM)
**Description:** 6 agents loaded up to 470KB of context but had 0 assistant turns, 0 tool results, 0 errors — spawned then immediately superseded or parent session interrupted.
**Evidence:** agent-afcdc522 (e2e-validator, 470KB), agent-a29a477 (auditor-review, 396KB), agent-aa69b90 (documenter, 389KB), plus 3 more.
**Root cause:** Spawned then superseded by retry, or parent session interrupted. No cleanup of orphaned agents.
**Recommendation:** INVESTIGATE — Quantify context budget waste from abandoned agents. Consider timeout or heartbeat mechanism.

### Fan-Out Agents Instructed to Use SendMessage (MEDIUM)
**Description:** Fan-out validators (not in TeamCreate) tried to use SendMessage, wasting 2-4 turns each searching for it before falling back to text response.
**Evidence:** Three validators tried ToolSearch for SendMessage; all failed. One correctly identified "not inside a TeamCreate team."
**Root cause:** Prompt instructed agents to use SendMessage for reporting, but fan-out agents don't have team communication available.
**Recommendation:** FIX — Fan-out agent prompts should specify "return report as final text response." Reserve SendMessage instructions for TeamCreate agents only.

### Story Completeness Gaps: Templates, Draft Markers, Lifecycle Steps (MEDIUM)
**Description:** Multiple stories shipped without complete lifecycle artifacts. decision-skill had no template. Intake stubs lacked DRAFT markers, causing downstream skills to treat stub content as authoritative. Quality gate spec missed worktree cleanup step.
**Evidence:** User: "decision-skill — Is there a template? In every story we should make sure that if a template doesn't exist for a document we create it." User: "AC3 needs to state that each section of the template should clearly state that this is a draft." User: "DELETING the worktree should be part of passing the quality gate."
**Root cause:** Story specs don't include a "completeness checklist" for new artifact types. Template creation and lifecycle steps are assumed, not specified.
**Recommendation:** FIX — Add to story spec template: "If this story introduces a new artifact type, include template creation in tasks. If this story modifies a lifecycle, include all lifecycle steps."

### Main Session Error Noise: 62/214 Errors, Many Informational (LOW)
**Description:** The main orchestrator session produced 29% of all errors (62/214), but many were informational non-zero exits — grep no-match, git status in clean state.
**Evidence:** 35 bash-exit-error (many grep no-match), 15 file-too-large, 10 other, 2 write-before-read.
**Root cause:** Error extraction doesn't distinguish true errors from informational non-zero exits.
**Recommendation:** INVESTIGATE — Filter non-zero exits that are informational (grep no-match = expected behavior) from real errors in extraction pipeline.

## User Interventions

### Intervention 1: E2E Validator Black-Box Violation (CRITICAL)
**Context:** E2E validator inspected source code files instead of treating skills as black boxes via execution.
**User action:** "What you're describing he did was a total failure and I would like to understand why he failed so horribly. It is supposed to be the most crystal clear thing in the world that the E2E NEVER EVER EVER EVER looks at source code."
**Resolution:** Multiple rounds of agent definition hardening — adding cmux knowledge, making cmux mandatory, changing MANUAL to ERROR for missing infrastructure.
**Implication:** Optional language in agent definitions is treated as opt-out. Enforcement requires mandatory language with zero fallback escape hatches. This was the sprint's most frustrating experience for the user.

### Intervention 2: E2E MANUAL Rate Unacceptable
**Context:** After multiple fix rounds, E2E validator still marking 15+ scenarios MANUAL.
**User action:** "Again why 15 manual. Why are we struggling through this. Please hear me that this is NOT NOT NOT NOT acceptable."
**Resolution:** Progressive hardening: MANUAL only for genuine user-interaction requirements, ERROR for infrastructure gaps.
**Implication:** MANUAL as escape hatch undermines the entire quality gate. A 66% MANUAL rate means the validator is not validating.

### Intervention 3: E2E Validator Not Spawned as Subagent
**Context:** Orchestrator ran E2E validation inline instead of spawning as subagent with cmux panes.
**User action:** "So a few things here, first I don't see a subagent, and second, Where is the CMUX pane/surfaces?"
**Resolution:** E2E re-run as proper subagent with cmux integration.
**Implication:** Workflow fidelity violation — delegation requirements are not optional.

### Intervention 4: cmux Knowledge Gap
**Context:** E2E validator had no awareness that cmux existed as infrastructure for execution.
**User action:** "I'm bothered that the E2E tester is still seemingly unaware that he has access to CMUX... Is that not in our rules?"
**Resolution:** Created global cmux rule, updated E2E agent definition to reference cmux as mandatory.
**Implication:** Infrastructure capabilities must be explicitly declared in agent definitions, not assumed.

### Intervention 5: Worktree Cleanup Before Validation
**Context:** Sprint-dev workflow cleaned up worktrees before running post-merge AVFL validation.
**User action:** "Why would we remove the worktrees before validating the merge?"
**Resolution:** Reordered workflow — validation before cleanup.
**Implication:** Logical ordering in workflow steps needs review. Cleanup is final, not mid-process.

### Intervention 6: Epic Assignment Override
**Context:** Agent accepted "Epic: ad-hoc" from user's draft prompt literally.
**User action:** "I don't want the stories to be ad-hoc. They should be properly prioritized in the backlog."
**Resolution:** Re-created stories with proper epic assignment and priority.
**Implication:** Conversational prompts are intent, not specs. Agents should validate against backlog conventions.

### Intervention 7: Sprint Lifecycle Misunderstanding
**Context:** Agent referred to a sprint in "planning" status as "not yet active."
**User action:** "No there is a sprint being planned. But it's part of the plan."
**Resolution:** Agent re-oriented to planning sprint as active context.
**Implication:** "Planning" is an active sprint state. Impetus needs clearer lifecycle semantics.

### Intervention 8: Vague Session Handoff
**Context:** Agent offered "ready to move on?" after ~6.5 hour gap with no concrete next step.
**User action:** "Move on to what?"
**Resolution:** Agent recovered by re-presenting Impetus menu.
**Implication:** Orchestrator must maintain menu-driven context across time gaps. Vague closers are disorienting.

### Intervention 9: cmux Surface Type Miscommunication
**Context:** User asked to "fire up stories in a surface on the right" — meant markdown viewer panes, not terminal.
**User action:** "I meant for you to fire each story up in a CMUX pane/surface on the right, the actual markdown when it's done."
**Resolution:** Agent opened markdown viewers instead of terminals.
**Implication:** cmux surface type (terminal vs markdown vs browser) needs clearer communication patterns.

### Intervention 10: Research Parallelism Not Used
**Context:** Research skill launched agents sequentially instead of in parallel.
**User action:** "Do you run the other research in parallel?"
**Resolution:** Agent parallelized subsequent research queries.
**Implication:** Parallelism is expected when workflow specifies it. Agents default to sequential even when independence is clear.

### Intervention 11: Dev Agent Skipped EDD
**Context:** Dev agent implemented Impetus fix without writing eval first.
**User action:** "Make sure to follow the dev TDD requirements."
**Resolution:** Agent wrote eval before proceeding.
**Implication:** EDD/TDD requirements exist in rules but agents don't consistently follow them without reminders.

### Intervention 12: Agent Asked User to Check Browser
**Context:** Agent asked user to manually check Gemini browser state instead of using cmux browser capture.
**User action:** "Can't you check on the gemini thing? Why am I checking it?"
**Resolution:** Agent used cmux browser tools to verify.
**Implication:** Agents should be self-sufficient with browser automation. Never ask the user to do what cmux can do.

### Intervention 13: Retro Recommendations Rejected (All 8)
**Context:** First retro attempt (with 3% of data) produced 8 recommendations. User rejected all.
**User action:** "1:N, 2:N, 3:N, 4:N, 5:N, 6:N, 7:N, 8:N"
**Resolution:** Retro re-run with full data extraction.
**Implication:** Retro output quality is directly proportional to input data quality. Running with 3% of data produces calibration-grade output at best.

### Intervention 14: Plugin Distribution Gap
**Context:** User's other projects didn't have /momentum:retro available.
**User action:** "Before we start, why do my other projects not have /momentum:retro?"
**Resolution:** Plugin update needed for downstream distribution.
**Implication:** New skills aren't available downstream until plugin is updated and pushed. Distribution is a manual step that's easy to forget.

## Story-by-Story Analysis

### remove-agent-journals (HIGH impact — 5 fix commits)
The sprint's most impactful story from a fix perspective. Deleted sprint-log write infrastructure but missed consumer references in 4 workflow files and introduced a JSON syntax error in hooks.json. Also broke hooks-global-distribution's concurrent changes via trailing comma. The sprint plan correctly flagged this as high-risk, but the dev agent's consumer audit was incomplete. User provided critical scope clarification mid-planning: "I just want to be certain this doesn't remove any other logging or journals for tracking sprint status."

### E2E Validator Refinement (CRITICAL impact — 5 commits, 7 spawns, 734 turns)
The sprint's most-iterated artifact. Required 5 commits across 2 days to stabilize the behavioral contract: initial cmux integration, trim, harden black-box constraint, make cmux mandatory, change MANUAL to ERROR. Simultaneously serving as quality gate while being refined — a moving target. The 66% MANUAL rate on the first full pass meant the validator was approving stories it hadn't actually tested. User frustration escalated across 7+ interventions.

### intake-skill, assessment-skill, decision-skill (Clean — 0 fix commits)
Three new practice capabilities shipped without incident. All completed on first dev pass. decision-skill needed a template addition (caught by user during planning review). Intake needed DRAFT markers (caught by user in AC review). Both were spec-level catches, not dev-level failures.

### quality-gate-parity-across-workflows (1 fix commit)
AVFL checkpoint caught an AC/task contradiction (HIGH finding) that was fixed pre-dev. Post-activation fix (commit 177d170) added missing sprint-dev worktree deferral task and touches entry.

### hooks-global-distribution (Clean dev, broken by cross-story interaction)
Implemented cleanly, but its hooks.json changes were broken by remove-agent-journals' array element deletion (trailing comma). This is a cross-story integration issue — no per-story quality gate covers it.

### refine-reprioritization
User made a key design decision during planning: "reprioritization is not just a presentation and an approval but a back and forth." This shaped the story's conversational interaction model.

### 8-3-gemini-deep-research
AVFL caught non-existent paths in spec. User had to remind agent to verify browser state with cmux tools instead of asking user to check manually.

### impetus-journal-hygiene
Triggered the broader remove-agent-journals story. User realized during review: "What is left in this doc once we've done that? We want to get rid of agent journals because the retro works really well with session journals."

### refine-assessment-decision-review (Wave 3)
Dependency chain (depends on assessment-skill and decision-skill) executed correctly — committed 3 minutes after Wave 2.

### gherkin-acs, remaining stories
Completed cleanly by dev agents. No notable post-merge issues.

## Cross-Cutting Patterns

### Pattern 1: E2E Validator — The Sprint's Central Struggle
**Sources:** Human audit (7 findings, 40% of all corrections), Execution audit (7 spawns, 734 turns, 3x cost of average agent), Review audit (66% MANUAL rate, contradictory scenario counts).
**Analysis:** The E2E validator consumed more user attention, more agent turns, and more fix commits than any other sprint artifact. The failure cascaded across three dimensions: (1) the agent lacked infrastructure knowledge (no cmux), (2) the spec provided escape hatches (optional language, MANUAL as fallback), and (3) the validator was being refined while simultaneously gating other stories. Each fix exposed the next gap — no cmux knowledge led to file inspection, adding cmux with optional language led to MANUAL escape, hardening MANUAL led to realizing ERROR was the right default. The user's frustration escalated from medium ("Is that not in our rules?") to critical ("NEVER EVER EVER EVER") over the course of the sprint.
**Impact:** Critical — consumed disproportionate user and agent resources, undermined confidence in quality gates.

### Pattern 2: Specification Quality Determines Fix-Tail Length
**Sources:** Human audit (4 story completeness gaps), Execution audit (clean dev passes prove agents implement specs faithfully), Review audit (AVFL caught 14 pre-merge spec defects).
**Analysis:** Dev execution was fast and correct — 12/12 first-pass success. Every problem was upstream: incomplete touches lists (remove-agent-journals), underspecified behavioral contracts (E2E validator), missing templates (decision-skill), absent draft markers (intake stubs). The AVFL checkpoint caught 14 spec-level defects, proving the gate works. But post-merge integration effects and behavioral contract edge cases slipped through. When specs are right, agents deliver. When specs are wrong, the fix tail is 8x longer than dev.
**Impact:** High — spec quality is the single largest determinant of sprint efficiency.

### Pattern 3: File-Too-Large Is a Systemic Tax on Validation and Retro
**Sources:** Execution audit (95/214 errors = 44%, concentrated in validation/retro phases).
**Analysis:** Validation and retro agents inherently need to read large files — JSONL logs, transcripts, sprint indexes. Without chunking guidance, every agent attempts full reads and fails. The same large files are hit repeatedly by different agents. Error bursts at T17 (49 errors) and T22 (60 errors) correspond to validation and retro phases. Dev phases had only 30 errors. This is not an agent intelligence problem — it's a missing infrastructure pattern.
**Impact:** High — 44% of all errors are preventable with file-size metadata and chunking guidance.

### Pattern 4: Workflow Fidelity Is Inconsistently Enforced
**Sources:** Human audit (5 workflow violations — inline execution, no parallelism, skipped steps, EDD skipped), Execution audit (retro 3x spawns with no idempotency), Review audit (fan-out agents given TeamCreate instructions).
**Analysis:** Five distinct workflow fidelity failures: (1) E2E validator run inline instead of spawned, (2) research agents run sequentially instead of parallel, (3) E2E validator phase silently skipped in team review, (4) dev agent skipped EDD/TDD eval-first requirement, (5) retro workflow has no idempotency check. The pattern is consistent — agents optimize for perceived efficiency by taking shortcuts. Rules say "spawn" but there's no enforcement mechanism. The user catches these failures through observation, not through automated detection.
**Impact:** High — undermines practice guarantees. Workflow steps exist for separation of concerns and auditability.

### Pattern 5: Agent Spawn Economics Need Attention
**Sources:** Execution audit (6 abandoned agents with 0 turns, 470KB max context loaded; 17 agents for 4 retro roles), Review audit (7 E2E validators for one sprint, 734 combined turns).
**Analysis:** The sprint spawned 105 agents. Of these, 6 were abandoned (0 turns, up to 470KB loaded), 13 were retro duplicates across 3 attempts, and 7 were E2E validators for a single gate. That's 26 agents (25%) that were either wasted or excessive. The targeted re-check pattern (27 turns vs 175+ turns for broad re-run) shows that scope matters more than spawning more agents.
**Impact:** Medium — context budget waste adds up. Targeted, scoped agents outperform broad ones.

### Pattern 6: Quality Gates Are High-Value but Need Integration Coverage
**Sources:** Review audit (AVFL caught 14, QA 346/346, arch guard passed, E2E caught 3 real failures), Human audit (user values gates, pushes for them to work correctly).
**Analysis:** The multi-layer quality gate system caught real defects at every layer. AVFL caught spec-level issues (14 findings). QA caught regression risk (346 tests). E2E caught runtime integration failures (3). Architecture guard prevented drift. However, all gates validate in isolation — no gate checks cross-story integration effects. The hooks-global-distribution/remove-agent-journals trailing comma conflict slipped through all gates because each story was valid in isolation.
**Impact:** Medium — fix cycle converges quickly, but cross-story integration validation would prevent defects rather than detect them post-merge.

### Pattern 7: Conversational Over Autonomous Is a User Design Principle
**Sources:** Human audit (reprioritization must be back-and-forth, not batch-approval; momentum:dev made internal-only; session handoffs must be menu-driven).
**Analysis:** Three distinct decisions share a common theme: the user prefers conversational, interactive workflows over autonomous one-shot decisions. Reprioritization is "a back and forth, not a presentation and an approval." The user-facing path is quick-fix (conversational), not dev (autonomous). Session handoffs must present menus, not vague "ready to move on?" This is a design principle for all user-facing skills: collaborative dialogue, not autonomous execution.
**Impact:** Medium — shapes skill design philosophy. User-facing skills must be conversational.

## Metrics

| Metric | Value |
|--------|-------|
| User messages analyzed | 267 |
| Subagents analyzed | 105 (96 valid, 9 parse errors) |
| Total assistant turns across agents | 4,255 |
| Total tool calls across agents | 3,181 |
| Tool errors detected | 214 |
| - File-too-large | 95 (44%) |
| - Bash exit errors (main session) | 35 (16%) |
| - File-modified-since-read | 11 (5%) |
| - Other | 73 (34%) |
| Team messages (raw / unique) | 93 / ~21 |
| Total commits in sprint | 52 |
| - feat commits | 13 |
| - docs commits | 21 |
| - fix commits | 15 (28.8%) |
| - chore commits | 2 |
| - refactor commits | 1 |
| AVFL pre-merge findings fixed | 14 |
| E2E validator instances spawned | 7 |
| E2E validator total turns | 734 |
| E2E first-pass MANUAL rate | 66% (31/47) |
| QA reviewer tests | 346 (346 pass) |
| Dev execution time (wall-clock) | ~23 minutes |
| Stories completed | 12/12 |
| Stories completed in 1 dev pass | 12/12 |
| Abandoned agents (0 turns) | 6 |
| Retro attempts before success | 3 |
| Successes identified | 7 |
| Struggles identified | 11 |
| User interventions | 14 |
| - Corrections | 7 |
| - Frustration signals | 4 |
| - Redirections | 2 |
| - Rejections | 1 |
| Cross-cutting patterns | 7 |
| User correction rate | ~25-28% of substantive messages |

## Priority Action Items

| # | Action Item | Priority | Source Patterns | Recommended Story |
|---|------------|----------|-----------------|-------------------|
| 1 | Harden E2E validator: mandatory cmux execution, zero escape hatches, MANUAL only for live user interaction, ERROR for infrastructure gaps. Include "there is no acceptable reason to mark a scenario as MANUAL" language | Critical | P1 (E2E central struggle), 7 human interventions | `e2e-validator-black-box-hardening` |
| 2 | Add file-size guidance and chunking patterns for validation/retro agents. Known-large files (JSONL, transcripts, sprint indexes) get offset/limit recommendations | High | P3 (file-too-large systemic tax), 95 preventable errors | `agent-file-size-guidance` |
| 3 | Add mandatory consumer-audit step for subtractive stories: grep all references (commands, paths, config keys) and include every consumer in touches list | High | P2 (spec quality), remove-agent-journals cascade | `subtractive-story-consumer-audit` |
| 4 | Enforce workflow delegation: steps marked "spawn" must spawn. Add workflow step completion tracking or audit hook for delegation-marked steps | High | P4 (workflow fidelity), 5 violations | `workflow-delegation-enforcement` |
| 5 | Add cross-story integration validation to AVFL checkpoint, especially for stories touching shared files or deleting shared infrastructure | High | P2 (spec quality), P6 (integration gaps) | `avfl-cross-story-integration-lens` |
| 6 | Add idempotency to retro workflow: detect prior attempt, offer resume or clean restart. Fix DuckDB serialization (json.dumps not repr) | High | P5 (spawn economics), 17 agents for 4 roles | `retro-pipeline-idempotency` |
| 7 | Prefer targeted re-checks (27 turns) over broad re-runs (175+ turns). Scope validators to changed stories only on re-check | Medium | P1 (E2E cost), P5 (spawn economics) | `validator-targeted-recheck-pattern` |
| 8 | Fix fan-out agent prompts: "return report as final text response," not SendMessage. Reserve SendMessage for TeamCreate only | Medium | P4 (workflow fidelity), RF-05 | `fan-out-agent-prompt-fix` |
| 9 | Story spec template: require template creation for new artifact types, DRAFT markers for stubs, lifecycle completeness for workflow changes | Medium | P2 (spec quality), 4 human findings | `story-spec-completeness-checklist` |
| 10 | Teach Impetus: "planning" = active sprint state; return to menu after ad-hoc tasks; never use vague handoffs | Medium | P7 (conversational design), interventions 7-8 | `impetus-lifecycle-and-handoff-fix` |
| 11 | Serialize access to shared mutable files (sprint index, hooks.json) during parallel dev waves, or use append-only patterns | Medium | P4, 11 file-modified errors | `shared-file-contention-fix` |
| 12 | Track and report abandoned agent count and context waste per sprint as observability metric | Low | P5 (spawn economics), 6 abandoned agents | `agent-spawn-observability-metric` |
| 13 | Deduplicate team messages by tool_use ID before writing audit extracts (3:1 duplication ratio) | Low | RF-07, P5 | `team-message-deduplication` |
| 14 | Filter informational non-zero exits (grep no-match) from real errors in extraction pipeline | Low | main session noise, 35 bash-exit-errors | `error-extraction-filtering` |
