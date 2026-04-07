# Sprint Transcript Audit — sprint-2026-04-06-2

**Retro date:** 2026-04-07
**Sprint completed:** 2026-04-07
**Data analyzed:** 684 user messages | 359 subagents | 584 tool errors | 589 inter-agent messages

---

## Executive Summary

Sprint-2026-04-06-2 delivered 9 stories across 2 waves, all reaching done status. The sprint's core deliverables — orchestrator deduplication guard, workflow team composition spec, mandatory task tracking, retro workflow rewrite, and related infrastructure improvements — represent genuine practice improvements addressing recurring pain points. The sprint also produced foundational infrastructure for the retrospective process itself: the DuckDB transcript-query pipeline and audit extract system now powering this document are direct outputs of this sprint.

The dominant finding across all three auditors is massive agent duplication: an estimated 47.8% of compute (12,981KB and 1,662 assistant turns) was wasted spawning identical agents for roles that needed only one instance. The 82% waste in the review layer — 17 QA reviewers and 14 E2E validators with identical prompts when 2-4 were sufficient — is a critical orchestrator bug. The stories this sprint implemented (orchestrator-deduplication-guard, workflow-team-composition-spec) were designed to fix exactly this problem, creating a productive irony: the sprint that implemented deduplication fixes ran with maximal duplication waste.

Human interaction quality was mixed. The user made 10 significant corrections and 6 redirections across 89 purely human-typed messages in 8 sessions. Recurring struggles include: TeamCreate vs. individual Agent spawn confusion (appears 3+ times), missing dev agent in AVFL/review team compositions, task tracking visibility gaps, and sprint planning producing raw data dumps instead of synthesis. Positives are equally clear: the TeamCreate review pipeline worked well when properly configured, the QA/E2E review cycle produced near-zero false positives, the fix cycle converged without thrashing, and the new transcript-audit approach discovered by the user mid-sprint represents a strategic breakthrough for the flywheel.

---

## What Worked Well

### 1. Review Pipeline Quality — Linear, No Thrashing

The QA/E2E review cycle was productive and linear. Timeline shows: QA reviewers spawned, found real issues, E2E validators identified 6 genuine Gherkin spec violations, prompt-engineer fixed them across 3 commits (e9ce1a7, b2c04eb, 05de33e), re-verification confirmed all 6 resolved. All 312 tests passed after changes. No bounce-back loops. False positive rate near zero — all E2E findings were confirmed valid.

**Evidence:** Team-messages show clean "QA concurs — team review complete" followed by E2E re-validation "all 4 feature files pass" in a single linear pass (18:34-19:19).

**Recommendation:** KEEP — the review pipeline itself works. The problem is spawning too many of them, not the pipeline design.

---

### 2. DuckDB Transcript-Query Infrastructure

The sprint produced `transcript-query.py` with real DuckDB integration, enabling the extraction that powers this very document. The 4-extract pipeline (user-messages, agent-summaries, errors, team-messages) provides the data backbone for systematic retrospectives and practice improvement.

**Evidence:** All four extract files populated correctly (684/359/584/589 records). The transcript-query.py script auto-installs duckdb, handles schema variations gracefully, and produces auditable JSONL output.

**Recommendation:** KEEP — this is the foundation of the practice flywheel. Build on it.

---

### 3. Fix Cycle Quality — Prompt-Engineer Did Real Work

When properly configured, the prompt-engineer agents delivered substantive fixes: impetus dispatch fixes, epic-grooming log path corrections, momentum-tools wire-up for ensure_priority(), TDD test suite additions, and 6 Gherkin spec structural fixes. Quality was high — fixes were verified and tests passed.

**Evidence:** Commits e9ce1a7 (CRITICAL+HIGH), b2c04eb (MEDIUM), 05de33e (Gherkin) with 312 tests passing post-fix. No rework needed.

**Recommendation:** KEEP — prompt-engineer role and fix quality are sound. Reduce their count to 1 per batch.

---

### 4. Dev-Allowed-Tools: Gold Standard Execution

The 3 dev-allowed-tools agents (impetus-allowed-tools-restriction story) demonstrated ideal execution: EDD-first approach, clean TDD cycles, 56-60 turns per agent, zero errors. One of the clearest examples of what correct individual Agent spawn execution looks like.

**Evidence:** agent-summaries show 3 instances, 556-567KB each, 0 errors, 56-60 assistant turns. Clean completion messages in all 3.

**Recommendation:** KEEP — use this as the template for dev agent prompting and scoping.

---

### 5. SendMessage/Team Communication Worked When Tools Were Loaded

When agents properly loaded SendMessage via ToolSearch first, inter-agent coordination was clean. The 3-auditor to documenter pipeline in this retro itself demonstrates the pattern works: execution auditor sent 9 findings, human auditor sent 10+6+4+9 categorized findings, review auditor sent 7 findings — all received cleanly by the documenter.

**Evidence:** Team-messages show 3 clean SendMessage → documenter acknowledgement sequences at 23:39, 23:40, 23:42 with specific finding counts confirmed.

**Recommendation:** KEEP the pattern. Fix the gap: E2E validator definition must include ToolSearch-first instruction.

---

### 6. Explore Agents — Efficient Research Pattern

9 Explore agents averaged 14-28 turns, 1-3 errors, unique prompts. They were not duplicated. Each ran a distinct query or discovery task. This is the correct usage pattern.

**Evidence:** All Explore agents in agent-summaries have unique first prompts. Average size 100KB vs. 200-400KB for team agents.

**Recommendation:** KEEP — Explore agents as scoped, unique research probes work well.

---

### 7. TDD Dev-Priority Story Execution

The 2 dev-priority agents (backlog-priority-field story) had 23 errors each — but the errors were legitimate TDD iterations: write test, run, fail, fix, re-run. Final state: 310 tests passing. This is the correct behavior for a TDD implementation cycle.

**Evidence:** High error counts correlate with test-fix cycles, not tool misuse. Final test runs show "310 passed, 0 failed."

**Recommendation:** KEEP — do not penalize high error counts without inspecting their cause. TDD iteration is expected.

---

## What Struggled

### 1. Agent Duplication — 47.8% Compute Waste (Critical)

Nearly every team-based agent type was spawned in bulk with identical prompts. The orchestrator did not check whether a role was already assigned before spawning another. Result: 7 prompt-engineers, 7 dev-refine-skill agents, 17 QA reviewers, 14 E2E validators — when 1 of each per batch was sufficient.

**Evidence:** 7 dev-refine-skill agents all show identical first prompts, sizes spread 359-374KB, errors identical (6 each), 6 of 7 end with "Stale self-message. Task N is already completed. No action needed." Execution auditor estimates 12,981KB and 1,662 turns wasted.

**Root cause:** Orchestrator spawning logic (sprint-dev workflow and AVFL) does not track whether a role has already been assigned. Multiple `Agent` calls with the same prompt are sent simultaneously or in rapid succession.

**Recommendation:** FIX — orchestrator-deduplication-guard story was implemented this sprint specifically to address this. Verify the guard is enforced at the orchestrator level, not just documented.

---

### 2. Missing Dev Agent in AVFL/Review Teams (High)

The user had to correct the agent twice in the same sprint session for omitting a dev/fixer role from AVFL and review team compositions: "Wait where is the dev here?" (04:25) and "Where is the dev agent?" (06:36). A validation team without a fixer is structurally incomplete.

**Evidence:** Human auditor C3 and C4. Two separate corrections about the same structural omission within a single session, demonstrating the agent did not learn from the first correction.

**Root cause:** AVFL and review workflows do not explicitly mandate a fix-capable agent alongside validators. The workflow text is permissive about team composition, leaving it to orchestrator judgment.

**Recommendation:** FIX — AVFL and sprint-dev review phase must explicitly specify: "Include a fixer agent (dev, prompt-engineer, or dev-skills) alongside QA and E2E validator roles. A validation team without a fixer is incomplete." Make this a blocking check.

---

### 3. TeamCreate vs. Individual Agent Spawn Confusion (High)

The user had to correct TeamCreate vs. individual Agent spawn behavior 3 times: sprint planning output as a team (04:25), wave agents spawned as TeamCreate instead of individual (18:55), and story agents as TeamCreate during sprint-planning (01:01 "NOOOOOOOO / Stop the TEAM"). Sprint-dev workflow language is apparently ambiguous enough to trigger this mistake repeatedly.

**Evidence:** Human auditor C5, C7. User messages: "Why are wave agents coming as teams? Absolutely should not be." and "This is meant to be a fan out of subagents NOT a TeamCreate."

**Root cause:** Workflow text uses "spawn" without consistently distinguishing TeamCreate from Agent. The distinction is critical: TeamCreate creates coordinated teams with shared context; Agent spawns are independent subagents. The two are not interchangeable.

**Recommendation:** FIX — Sprint-dev and sprint-planning workflows must use explicit markers: `<spawning-mode>individual-agent</spawning-mode>` or `<spawning-mode>team-create</spawning-mode>` at every delegation step. The workflow-team-composition-spec story implemented this sprint should enforce this.

---

### 4. Task Tracking Visibility Gaps (High)

Three escalating messages about task tracking in a single session: "Where is the task list?" → "But that is not a claude code task list" → "Seriously...WHy can't you create a task list? Is that no longer a capability you have?" This was the peak frustration sequence of the sprint.

**Evidence:** Human auditor C6. Timestamps 18:46, 18:47, 18:55. The mandatory-task-tracking story was implemented this sprint to address this.

**Root cause:** Agents were not consistently using TaskCreate/TaskList tools at workflow start and throughout execution. The sprint-dev workflow previously did not mandate these tools explicitly enough.

**Recommendation:** FIX — Verify that mandatory-task-tracking story implementation actually enforces TaskCreate at workflow start (not just documents it). Test by running sprint-dev and confirming task list appears immediately without prompting.

---

### 5. Sprint Planning Raw Data Dump (High)

First correction of the sprint, within 6 minutes: "Good lord that is a wall of crap. What about making some suggestions from the master plan and backlog? What comes out as high priority?" Sprint planning produced a raw inventory instead of a prioritized synthesis.

**Evidence:** Human auditor C1. Timestamp 2026-04-06T03:04:00. The sprint-planning-synthesis-first story was implemented this sprint to address this.

**Root cause:** Sprint planning workflow's initial step presented all backlog data without a synthesis or prioritization pass first.

**Recommendation:** FIX — Verify sprint-planning-synthesis-first implementation: the skill must lead with "Here are my top N recommendations and why" before presenting any backlog data. Raw data should be available on request, not as the default first output.

---

### 6. SendMessage Without ToolSearch Pre-Load (Medium)

7 of 14 E2E validators attempted to call SendMessage before loading its schema via ToolSearch. All hit InputValidationError, recovered automatically, and completed their work. But each wasted 1 turn.

**Evidence:** Review auditor Finding 6. Review auditor message: "The E2E validator agent definition does not explicitly instruct the agent to discover tools like SendMessage before using them. QA reviewers did not have this issue."

**Root cause:** E2E validator agent definition lacks the ToolSearch-first instruction that QA reviewer definition apparently includes.

**Recommendation:** FIX — Add to e2e-validator agent definition: "Before sending any SendMessage, call ToolSearch with query 'select:SendMessage' to load the schema. Calls without the schema will fail." The e2e-validator-toolsearch-fix story was implemented this sprint.

---

### 7. Self-Message Routing Artifacts (Medium)

Multiple agents received messages addressed from themselves, causing confusion and wasted turns. Agents handled gracefully but it adds 1-2 turns of noise per agent lifecycle.

**Evidence:** Execution auditor Finding 9. Agent transcripts: "This message appears to be a self-addressed task assignment — likely a routing artifact." Found in QA reviewers and E2E validators.

**Root cause:** When multiple agents share the same role name (due to duplication), SendMessage to that role delivers to all instances including the sender. Fixing the duplication problem (Finding 1) will eliminate most self-message artifacts.

**Recommendation:** FIX — Primary fix is eliminating agent duplication. Secondary: consider role-name uniquification per spawn (e.g., qa-reviewer-1, qa-reviewer-2) rather than shared role names.

---

### 8. Concurrent Review Not Default (Medium)

User had to ask: "Does it have to be sequential? Can the E2E happen concurrently?" during the review phase. Parallelism is in the workflow-fidelity rules as "expected" but was not applied.

**Evidence:** Human auditor C8. Timestamp 18:36. Workflow-fidelity rule states "Parallelism Is Expected" explicitly.

**Root cause:** Agent defaulted to sequential execution when no explicit parallelism instruction appeared in the review phase workflow.

**Recommendation:** FIX — Sprint-dev review phase must state: "Spawn QA and E2E agents simultaneously in a single Agent call batch. Do not sequence them."

---

### 9. Agent Logging Gap — Flywheel Risk (Critical, Strategic)

The user's insight at 22:42 is the most strategically important moment of the sprint: "Oh god yes...this is meant to be the crux of our flywheel. If we can't implement good logging we're doomed." The existing milestone log system (momentum-tools log) was never written during sprint execution, leaving the audit data-poor. This sprint's retro itself only succeeded because the user redirected to DuckDB transcript analysis.

**Evidence:** Retro workflow note: "Milestone logs are NOT the critical path — retro proceeds and produces findings even when zero log events exist." Sprint impetus.jsonl shows minimal entries vs. 684 user messages in transcripts.

**Root cause:** Agents do not write momentum-tools log events during sprint execution. The logging calls are in the workflow but skipped in practice. The retro-workflow-rewrite story this sprint shifted to DuckDB as the primary data source.

**Recommendation:** FIX — This was partially addressed by retro-workflow-rewrite. Complete the fix: ensure the DuckDB-based approach is the default path, and remove any workflow language that makes milestone log writing appear optional or secondary.

---

### 10. Staleness Check Missing from Sprint Planning (Medium)

User had to manually request: "Are we certain those ready-for-dev stories have not already been implemented? Can you please run a couple agents to do discovery?" Sprint planning presented stories as candidates without verifying they hadn't already been done.

**Evidence:** Human auditor C9. Timestamp 14:45. Stories presented as backlog candidates that were potentially already implemented.

**Root cause:** Sprint planning workflow has no step to cross-reference backlog stories against git history and existing code.

**Recommendation:** FIX — Add to sprint planning workflow: "Before presenting backlog candidates, run discovery agents to verify each story's code hasn't already been implemented. Check git log for story slug references and verify expected files exist."

---

## User Interventions

The sprint had 89 genuinely human-typed messages across 8 sessions (~20 hours). Key interventions:

| Type | Count | Examples |
|------|-------|---------|
| Corrections | 10 | Missing dev agent (x2), TeamCreate misuse, task tracking, sprint planning data dump |
| Redirections | 6 | Fix in momentum not local, abandon team use tasks, sprint planning redirect, rabbit hole recovery |
| Frustrations | 4 | "Good lord" (x2), "Seriously...WHy can't you", "NOOOOOOOO" |
| Praise | 9 | "There we go", "That looks good", "I love Option 1", "OK I love what you've got here" |
| Strategic decisions | 15+ | DuckDB pivot, epic-grooming vs create-epic, agent guidelines rename, backlog priority field |

**Highest-impact corrections:**
- C3/C4 (dev agent missing, repeated): Practice gap requiring workflow fix
- C5 (wave agents as TeamCreate): Sprint-dev workflow ambiguity
- C6 (task list): Peak frustration sequence, 3 escalating messages

**Most significant user decision:**
At 23:04 the user articulated the transcript-audit approach: "Let's fire up a big TeamCreate of session auditors. They are comparing each session and looking for struggle points." This insight drove the retro-workflow-rewrite story and the DuckDB infrastructure this sprint delivered.

---

## Story-by-Story Analysis

### orchestrator-deduplication-guard
Addresses the most critical execution problem: 47.8% compute waste from duplicate agent spawning. Implementation this sprint means future sprints should not exhibit the same duplication pattern. The guard itself was not active during this sprint's execution (circular dependency — it was being built).

### workflow-team-composition-spec
Addresses TeamCreate vs. individual Agent spawn confusion (repeated human correction C5). Specifies explicit spawning modes at each delegation step.

### mandatory-task-tracking
Addresses the peak frustration sequence (C6: task list visibility). Sprint-dev and sprint-planning must now use TaskCreate at workflow start.

### retro-workflow-rewrite
The most architecturally significant story of the sprint. Rewrites the retro from milestone-log-dependent to DuckDB transcript-based. This document is evidence the rewrite works.

### sprint-planning-synthesis-first
Addresses C1 (raw data dump). Sprint planning now leads with prioritized recommendations.

### review-orchestration-codification
Addresses R5 (user having to specify review orchestration details). Codifies: AVFL (scan mode) + concurrent code-reviews → review team (fixer + QA + E2E).

### agent-observability-system
Foundation for the logging flywheel. Addresses the agent logging gap identified as strategically critical at 22:42.

### e2e-validator-toolsearch-fix
Addresses the InputValidationError from SendMessage before ToolSearch (review auditor Finding 6). Small fix, high correctness value.

### transcript-query-calibration
Calibrates the error detection logic in transcript-query.py to use actual is_error flags rather than string matching. Fixes inflated error counts in extraction (review auditor Finding 7).

---

## Cross-Cutting Patterns

### Pattern 1: Deduplication is the single highest-leverage fix
Human, execution, and review auditors all surface agent duplication as the dominant dysfunction. 47.8% compute waste (execution), 82% review compute waste (review), and 3 user corrections about unexpected team behavior (human). A single orchestrator fix — track spawned roles, skip if already running — eliminates the majority of waste across all audit dimensions.

### Pattern 2: Workflow ambiguity drives repeated corrections
TeamCreate vs. individual spawn confusion appears in human auditor (C5, with "NOOOOOOOO" signal), execution auditor (dev-refine-skill duplication), and review auditor (17 QA reviewers when 2 needed). The fix is the same in all three: explicit `<spawning-mode>` markers in workflow XML.

### Pattern 3: Stories implementing their own fixes created self-referential gaps
Several sprint-2026-04-06-2 stories fixed the exact patterns that hurt sprint-2026-04-06-2 execution. The deduplication guard wasn't active while it was being built. Task tracking wasn't enforced while it was being implemented. This is expected for infrastructure work but explains why execution quality this sprint was lower than the specs would suggest.

### Pattern 4: Quality gate effectiveness vs. quantity
Review auditor confirmed near-zero false positives: all 6 E2E findings were valid, all 4 QA story verifications were accurate. The gates work. The problem is purely in count — 17 QA reviewers doing identical work when 1 would have been adequate. Quality and quantity are orthogonal concerns here.

### Pattern 5: Strategic inflection at end of sprint
The user's recognition that transcript-based analysis (vs. milestone logs) is the right foundation represents a genuine strategic pivot. This pattern — real problems surfacing late in sprints and driving architectural decisions — suggests the retro itself is a critical product-shaping mechanism, not just a post-mortem.

### Pattern 6: The E2E validator's ToolSearch gap is a systematic instruction deficit
7 of 14 E2E validators hit the same InputValidationError because the agent definition lacks ToolSearch-first guidance that QA reviewer has. This is a copy-paste deficit in the agent definition file, not a model-level problem. One-line fix resolves it across all future E2E validator instances.

### Pattern 7: Logging and observability is the flywheel bottleneck
Human auditor F3 and user message at 22:42 converge on the same insight: if agents can't observe themselves, the practice can't improve. The agent-observability-system story addresses this. Until it delivers, every retro is dependent on human insight to identify what to look for, rather than systematic detection.

---

## Metrics

| Metric | Value |
|--------|-------|
| User messages analyzed | 684 |
| Subagents analyzed | 359 |
| Tool errors detected | 584 |
| Sprint-2026-04-06-2 specific errors | 434 |
| Struggles identified | 10 |
| Successes identified | 7 |
| User interventions (corrections) | 10 |
| User interventions (redirections) | 6 |
| User frustration signals | 4 |
| Cross-cutting patterns | 7 |
| Estimated compute waste from duplication | 47.8% |
| Review layer waste (82% of review compute) | 12,981 KB |
| Stories completed | 9/9 |
| Test suite result post-sprint | 312 passed, 0 failed |

---

## Priority Action Items

| # | Item | Priority | Recommended Story Stub Title |
|---|------|----------|------------------------------|
| 1 | Verify orchestrator-deduplication-guard enforcement — confirm it prevents identical role spawns in next sprint execution | Critical | `verify-dedup-guard-enforcement` |
| 2 | Add explicit `<spawning-mode>individual-agent</spawning-mode>` markers to sprint-dev and sprint-planning at every delegation step | Critical | `spawning-mode-markers` |
| 3 | AVFL and review workflows must mandate fixer agent (dev/prompt-engineer) alongside validators — make it a blocking check | High | `avfl-fixer-required-gate` |
| 4 | Verify mandatory-task-tracking implementation produces visible TaskList immediately on workflow start without user prompting | High | `verify-task-tracking-enforcement` |
| 5 | Verify sprint-planning-synthesis-first implementation: planning must lead with recommendations, not raw backlog dump | High | `verify-sprint-planning-synthesis` |
| 6 | Sprint planning staleness check: discover already-implemented stories before presenting candidates | High | `sprint-planning-staleness-check` |
| 7 | E2E validator agent definition: add ToolSearch-first instruction before SendMessage calls | Medium | `e2e-validator-toolsearch-instruction` |
| 8 | Review orchestration must spawn QA and E2E concurrently — add explicit parallel spawn instruction to sprint-dev review phase | Medium | `review-concurrent-spawn` |
| 9 | Agent logging flywheel: deliver agent-observability-system to enable systematic self-improvement rather than relying on human intuition | Medium | `agent-observability-delivery-verification` |
| 10 | Master plan must be read as sprint planning prerequisite — add to workflow step 1 | Low | `sprint-planning-master-plan-prerequisite` |
