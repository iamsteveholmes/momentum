# Sprint Transcript Audit — sprint-2026-04-06

## Executive Summary

Sprint 2026-04-06 completed all 4 stories (backlog-priority-field, impetus-allowed-tools-restriction, epic-grooming, refine-skill) across 8 sessions spanning ~20 hours. 97 subagents were spawned in the primary session, with 246 user-facing messages and 89 genuinely human-typed messages.

The sprint delivered successfully, but at roughly **twice the necessary compute cost**. The dominant problem was massive agent duplication: the orchestrator spawned multiple identical agents for the same role, resulting in 47.8% wasted transcript volume (12,981KB of 27,132KB) and 43.7% wasted turns (1,662 of 3,799). In the review layer specifically, 82% of compute was redundant. When agents were not duplicated, execution was clean — dev agents completed stories with zero errors, the review pipeline was linear and productive, and QA/E2E validators caught real issues with zero false positives.

The human experience was mixed. The user made 10 corrections and experienced 4 distinct frustration moments, primarily around team composition errors and lost task tracking. But the user also gave 9 explicit approval signals and engaged in high-quality design discussions. The most common failure mode was orchestration — how agents were spawned, composed, and coordinated — not the quality of individual agent work.

The sprint surfaced a critical strategic insight: agent logging/observability is the bottleneck for the practice improvement flywheel. Without better logging, retrospectives cannot generate the insights needed to drive improvement.

**Health assessment:** The practice model works. Individual agents perform well. The orchestration layer is the weak link — fix agent deduplication, team composition defaults, and task tracking, and the next sprint should be dramatically more efficient.

---

## What Worked Well

### W1. Parallel Worktree Dev Execution
- **What:** All wave-1 dev agents completed successfully in parallel using the worktree model. Clean separation, tests passing, no merge conflicts.
- **Evidence:** Dev agents completed between 04:40-04:50 (session 27af). All reported status:complete. The 3 dev-allowed-tools agents achieved zero errors in 56-60 turns each.
- **Recommendation:** KEEP. The worktree model for parallel dev execution is the strongest pattern in the practice.

### W2. Review Pipeline Was Linear and Productive
- **What:** The review cycle followed a clean sequence: QA review -> findings -> prompt-engineer fix -> E2E re-verify -> done. No bounce-back loops or thrashing.
- **Evidence:** Timeline: QA concurred at 18:40, prompt-engineer committed fixes at 19:11 (e9ce1a7), 19:16 (b2c04eb), and 19:18 (05de33e). E2E re-verified. All shutdown clean by 19:19. 312 tests passed.
- **Recommendation:** KEEP. The review pipeline architecture is sound. The problem was duplication, not the pipeline design.

### W3. QA/E2E Quality Gates Caught Real Issues
- **What:** QA reviewers correctly verified all 4 stories against acceptance criteria. E2E validators identified 6 genuine Gherkin spec violations. Zero false positives across all findings.
- **Evidence:** All 6 E2E findings were confirmed valid and subsequently fixed. QA correctly identified that F-TOOLS-1 and F-TOOLS-2 should be withdrawn (static artifact checks belong in DoD, not Gherkin). All 4 stories received PASS verdicts.
- **Recommendation:** KEEP. The quality gates are effective and produce high signal-to-noise output.

### W4. Prompt-Engineer Fixes Were Substantive
- **What:** The prompt-engineer agent made real, verified code-level fixes across 3 commits — not cosmetic changes.
- **Evidence:** Commit e9ce1a7 (CRITICAL+HIGH): impetus dispatch fix, eval fix, epic-grooming log paths, refine-skill Dev Agent Record. Commit b2c04eb (MEDIUM): ensure_priority() wire-up, new test (test_sprint_stories_invalid_priority). Commit 05de33e: 6 Gherkin fixes across 4 feature files. All 312 tests passed.
- **Recommendation:** KEEP. The prompt-engineer role is effective at translating review findings into verified fixes.

### W5. Design Discussion as Thinking Partner
- **What:** Agent served as an effective collaborative design partner during architecture discussions about agent guidelines, role simplification, and skill naming.
- **Evidence:** 17:38-17:57 (session fe5b): Multi-turn design exchange. User engaged deeply ("I love Option 1. I have follow up questions..."), agent asked good questions, concrete decisions emerged (unified dev agent, skill rename to "agent guidelines", "backlog add" command naming).
- **Recommendation:** KEEP. The agent's ability to facilitate design discussions is a genuine strength.

### W6. Single-Letter Menu UX
- **What:** Users navigated Impetus/skill menus efficiently via single-letter responses ("G", "A", "C", "Y", "1").
- **Evidence:** 9 single-letter menu selections across sessions. No confusion or mis-selection observed.
- **Recommendation:** KEEP. Fast, efficient decision-making UX.

### W7. Efficient Explore Agents
- **What:** Explore agents were consistently efficient — unique prompts (not duplicated), scoped research tasks, clean completion.
- **Evidence:** 9 parsed explore agents: 14-28 turns, 1-3 errors, average 100KB. Each had a distinct query. Best single-agent performance: momentum:dev (agent-af93dbc9ee60f40a7) completed a targeted finding review in 8 turns, 39KB, 1 error.
- **Recommendation:** KEEP. Explore agents are well-scoped and efficient.

---

## What Struggled

### S1. Massive Agent Duplication — 47.8% Compute Waste
- **What:** The orchestrator spawned multiple identical agents for the same role. Every team-based agent type was duplicated, with identical first prompts. Each duplicate performed the full work independently, then discovered the work was already done.
- **Why:** The orchestrator (sprint-dev workflow) does not track which subagents have already been assigned to a story. It spawns by role name without checking for existing agents in that role.
- **Evidence:** 7 identical dev-refine-skill agents (only 1 needed), 7 identical prompt-engineers (only 1 needed), 17 QA reviewers (only 2 needed), 14 E2E validators (only 2 needed). 12,981KB and 1,662 turns wasted. 6 of 7 dev-refine-skill agents ended with "Stale self-message. Task N is already completed."
- **Recommendation:** FIX (Critical). The orchestrator must track spawned agents by (story, role) tuple and not re-spawn duplicates. This single fix would cut compute nearly in half.

### S2. Review Layer Redundancy — 82% Waste
- **What:** Within the review layer specifically, 11.4MB of 13.9MB total review transcript was redundant identical agents.
- **Why:** Same root cause as S1 — the orchestrator spawned N copies per role per batch instead of 1.
- **Evidence:** 17 QA reviewers spawned when 2 were needed. 14 E2E validators when 2 were needed. 7 prompt-engineers when 1 was needed. 30+ duplicate status messages flooded the team-lead's context window.
- **Recommendation:** FIX (Critical). Spawn exactly 1 agent per role per batch.

### S3. Team Composition Errors — Missing Dev Agent
- **What:** AVFL validation team was set up without a dev agent to fix findings. Same mistake repeated twice in the same session.
- **Why:** The AVFL workflow does not mandate required team roles. The agent composed a review-only team (QA, E2E Validator, Architecture Guard) without a fixer.
- **Evidence:** User corrected at 04:25 ("Wait where is the dev here?") and again at 06:36 ("Where is the dev agent?"). Agent failed to learn from the first correction within the session.
- **Recommendation:** FIX. AVFL and review workflows must explicitly document required team roles: validator(s) + fixer. A validation team without a dev agent is architecturally incomplete.

### S4. Sprint Planning Data Dump
- **What:** Sprint planning skill dumped the full backlog/status as raw data without synthesis or recommendations.
- **Why:** The sprint planning workflow does not mandate a "synthesis first" step. It presents inventory before analysis.
- **Evidence:** User reaction at 03:04: "Good lord that is a wall of crap. What about making some suggestions from the master plan and backlog?" First frustration, within 6 minutes of starting.
- **Recommendation:** FIX. Sprint planning must lead with prioritized recommendations, not raw inventory. Add a mandatory synthesis step before presenting backlog state.

### S5. Task Tracking Abandoned During Long Sessions
- **What:** Agent failed to maintain Claude Code task tracking during complex multi-step workflows. User lost track of progress and had to ask repeatedly.
- **Why:** No workflow enforcement of TaskCreate/TaskList usage. The agent reverted to ad-hoc summaries instead of structured task state.
- **Evidence:** Escalating frustration sequence at 18:46-18:55: "Where is the task list?" -> "But that is not a claude code task list" -> "Seriously...WHy can't you create a task list?" (ALL-CAPS "WHy" = peak frustration).
- **Recommendation:** FIX. Sprint-dev and sprint-planning workflows MUST use TaskCreate at session start and maintain task state throughout. Proactive task progress display, not reactive.

### S6. Wrong Agent Spawning Mode (TeamCreate vs Individual)
- **What:** Agent spawned wave dev agents as TeamCreate instead of individual Agent spawns, and ran review agents sequentially when they could run concurrently.
- **Why:** Sprint-dev workflow ambiguity. The workflow said "Spawn the resolved agents" which the agent interpreted as TeamCreate. The agent also defaulted to sequential when concurrent was possible.
- **Evidence:** User at 18:55: "Why are wave agents coming as teams? Absolutely should not be." User at 18:36: "Does it have to be sequential? Can the E2E happen concurrently?"
- **Recommendation:** FIX. Sprint-dev workflow must clarify that "spawn agents" means individual Agent spawns, not TeamCreate. Workflow fidelity rule already says "Parallelism Is Expected" — enforce it.

### S7. Story Staleness Not Checked
- **What:** Agent presented stories as ready-for-dev without checking if they had already been implemented.
- **Why:** Sprint planning workflow does not include a staleness check step.
- **Evidence:** User at 14:45: "Are we certain those ready for dev stories have not already been implemented? Can you please run a couple agents to do discovery?"
- **Recommendation:** FIX. Sprint planning must compare backlog stories against git log and existing code to detect already-implemented work before presenting sprint candidates.

### S8. Agent Logging/Observability Gap
- **What:** Agent analysis of its own sprint produced thin results because logging is insufficient to support meaningful self-analysis.
- **Why:** No structured agent logging system exists. Sprint analysis relies on raw transcript extraction with fragile heuristics.
- **Evidence:** User at 22:23: "Good lord was that all you found?" Leading to the strategic insight at 22:42: "Oh god yes...this is meant to be the crux of our flywheel. If we can't implement good logging we're doomed."
- **Recommendation:** FIX (Strategic). Agent logging is a critical blocker for the practice improvement flywheel. Without it, retrospectives are blind.

### S9. E2E Validator ToolSearch Gap
- **What:** 7 of 14 E2E validators hit an InputValidationError trying to use SendMessage before loading its schema via ToolSearch.
- **Why:** The E2E validator agent definition does not include tool discovery guidance. QA reviewers did not have this issue, suggesting their prompt includes it.
- **Evidence:** All 7 errors were identical: "This tool's schema was not sent to the API." Self-recovering (agent retried after loading), but added 1 wasted turn per agent.
- **Recommendation:** FIX. Add explicit ToolSearch guidance to the E2E validator agent definition, or pre-load SendMessage in spawn config.

### S10. Error Extraction False Positives
- **What:** 65% of the 806 flagged "errors" in the extraction pipeline were false positives — file content that happened to contain error-like strings.
- **Why:** The extraction heuristic matches on string patterns rather than actual error indicators (is_error flags, tool_use_error responses).
- **Evidence:** ~529 false positives out of 806 flagged items. True errors were ~277. The error rate reported per agent type was inflated (e.g., 30% for prompt-engineer vs. ~1% actual).
- **Recommendation:** FIX. Extraction script should filter by actual error indicators, not string matches in content.

---

## User Interventions

### I1. Sprint Planning Redirect — Synthesis Over Data
- **What:** "Good lord that is a wall of crap. What about making some suggestions?"
- **Why:** Agent dumped raw backlog without analysis. User needed prioritized recommendations.
- **Impact:** Agent recalibrated and provided good recommendations that the user immediately approved ("Agreed, go!").
- **Recommendation:** Sprint planning workflow should mandate synthesis-first output. This intervention should never be needed.

### I2. CMUX Pane Misunderstanding
- **What:** "No...new pane, man. Not this pane"
- **Why:** Agent rendered content in the current pane instead of creating a new CMUX surface.
- **Impact:** Minor delay. Agent corrected.
- **Recommendation:** Default to creating NEW splits when user says "show X in a pane/surface."

### I3. Missing Dev Agent (First Occurrence)
- **What:** "Wait where is the dev here? QA, E2E Validator, Architect Guard - ? Who is meant to fix things?"
- **Why:** AVFL team composed without a fixer. Reviewers without a dev are useless.
- **Impact:** Team had to be recomposed. Delayed the review cycle.
- **Recommendation:** AVFL workflow must mandate dev agent inclusion.

### I4. Missing Dev Agent (Repeated)
- **What:** "Where is the dev agent?" + "The team is meant to be a TeamCreate, can you set them up again in that mode?"
- **Why:** Same mistake as I3, recurring in the same session. Agent failed to retain the correction.
- **Impact:** Further delay. User had to re-explain the team composition requirement.
- **Recommendation:** Practice-level fix. AVFL workflow must codify required roles. Within-session learning must improve.

### I5. Fix Scope — Momentum Not Local
- **What:** "But that doesn't fix it for other projects does it? Can it be fixed in momentum?"
- **Why:** Agent proposed a project-local fix when the user wanted a practice-level fix in the momentum plugin.
- **Impact:** Healthy architectural redirection. Agent should default to practice-level fixes in momentum.
- **Recommendation:** When fixing practice-related issues, default to fixing at the momentum level, not project-locally.

### I6. Story Staleness Verification
- **What:** "Are we certain those ready for dev stories have not already been implemented?"
- **Why:** Agent presented stale stories without checking implementation status.
- **Impact:** Discovery agents were spawned to verify. Some stories were already implemented.
- **Recommendation:** Staleness check must be built into sprint planning workflow.

### I7. Master Plan Not Consulted
- **What:** "I don't feel like you've looked over the master plan document."
- **Why:** Sprint planning agent worked without reading the master plan.
- **Impact:** Agent had to go back and read the plan, then revise recommendations.
- **Recommendation:** Sprint planning step 1 should mandate reading the master plan.

### I8. Task List Escalation (3-message sequence)
- **What:** "Where is the task list?" -> "But that is not a claude code task list" -> "Seriously...WHy can't you create a task list?"
- **Why:** Agent presented ad-hoc summaries instead of using TaskCreate/TaskList tools.
- **Impact:** Peak frustration moment. User lost confidence in workflow tracking.
- **Recommendation:** Mandatory TaskCreate at session start for any multi-step workflow. Proactive task display.

### I9. Wrong Spawning Mode
- **What:** "Why are wave agents coming as teams? Absolutely should not be."
- **Why:** Agent used TeamCreate where individual Agent spawns were specified by the workflow.
- **Impact:** Agents had to be re-spawned in the correct mode.
- **Recommendation:** Clarify sprint-dev workflow language: "spawn agents" = individual spawns, not TeamCreate.

### I10. Sequential When Concurrent Was Possible
- **What:** "Does it have to be sequential? Can the E2E happen concurrently?"
- **Why:** Agent defaulted to sequential execution of independent review agents.
- **Impact:** Unnecessary delay in review cycle.
- **Recommendation:** Workflow fidelity rule already mandates parallelism. Enforce it.

### I11. Team Communication Breakdown
- **What:** "Who are you talking to? Did you send this to the team?"
- **Why:** Agent output text about team work instead of routing via SendMessage.
- **Impact:** Messages not delivered to team agents. Communication breakdown.
- **Recommendation:** When a team is active, work-related messages must always route via SendMessage.

### I12. Rabbit Hole Recovery
- **What:** "Sorry where were we. I'm a bit confused how we went down this rabbit hole"
- **Why:** Design discussion about agent guidelines derailed from sprint planning.
- **Impact:** Lost time and context. User had to re-orient.
- **Recommendation:** Long planning sessions need periodic checkpoint messages: "We've been on this tangent for N minutes. Return to [original task]?"

### I13. Complex Review Orchestration Micromanagement
- **What:** "Proceed but remember that the AVFL should STOP before fix... followed by feeding into the team to make fixes. There should ALSO be independent /bmad-code-review on each story..."
- **Why:** Agent wasn't following the expected review flow. User had to specify exact orchestration.
- **Impact:** User micromanaged what should be an automated workflow.
- **Recommendation:** Sprint-dev workflow's review phase should codify this exact flow: AVFL (no-fix mode) + concurrent code-reviews -> results fed to review team.

---

## Story-by-Story Analysis

### backlog-priority-field
- **Dev iterations:** 2 duplicate agents (only 1 needed)
- **Turns per agent:** 90-91
- **Errors per agent:** 23 (legitimate TDD iteration — test-fix cycles, final result: 310 tests passed)
- **Outcome:** Completed successfully. TDD approach was sound despite high error count.
- **Notable:** Highest per-agent error count in the sprint, but all from productive test iteration, not dysfunction.

### impetus-allowed-tools-restriction
- **Dev iterations:** 3 duplicate agents (only 1 needed)
- **Turns per agent:** 56-60
- **Errors per agent:** 0
- **Outcome:** Completed successfully. Gold standard execution — EDD-first, clean TDD, zero conflicts.
- **Notable:** Best execution quality of any story. Zero errors across all 3 duplicate agents.

### epic-grooming
- **Dev iterations:** 2 duplicate agents (only 1 needed)
- **Turns per agent:** ~83
- **Errors per agent:** Moderate
- **Outcome:** Completed successfully.
- **Notable:** Straightforward implementation.

### refine-skill
- **Dev iterations:** 7 duplicate agents (only 1 needed)
- **Turns per agent:** 70-76
- **Errors per agent:** 6 each (identical across all 7)
- **Outcome:** Completed successfully by 1 agent; 6 discovered work was done.
- **Notable:** Worst duplication case — 7x the needed compute. All 7 agents had identical prompts, near-identical sizes (359-374KB), identical error counts. 6 of 7 ended with "Stale self-message. Task already completed."

---

## Cross-Cutting Patterns

### Pattern 1: Orchestration Is the Bottleneck, Not Agent Quality
Every major problem in this sprint traces to orchestration, not individual agent performance. Agent duplication (S1, S2), team composition errors (S3), wrong spawning modes (S6), sequential-when-concurrent (S6), lost task tracking (S5) — all orchestrator failures. When agents were properly spawned and scoped, they performed well (W1, W2, W3, W4, W7).

**Implication:** Investment should focus on orchestrator reliability (sprint-dev, AVFL workflows), not on improving individual agent performance.

### Pattern 2: Corrections Cluster Around Team Composition and Spawning
6 of 10 user corrections (C3, C4, C5, C7, C8, R6) were about HOW agents were spawned, composed, or coordinated. This is a single failure mode appearing in multiple forms: the orchestrator does not have reliable conventions for team formation.

**Implication:** Team composition needs to be declarative and codified in workflows, not left to runtime decisions. Required roles, spawning mode (individual vs. TeamCreate), and concurrency expectations should be explicit workflow parameters.

### Pattern 3: Duplication Cascades Through Layers
Agent duplication in the dev layer (7 dev-refine-skill agents) cascaded into the review layer (7 prompt-engineers fixing the same findings). The review layer then generated duplicate status messages (30+ to team-lead), consuming context window. Duplication is not a point problem — it propagates.

**Implication:** Fixing duplication at the source (the orchestrator spawning logic) eliminates cascading waste across all downstream layers.

### Pattern 4: The Review Pipeline Design Is Sound
Despite massive redundancy in agent count, the review pipeline architecture worked correctly. QA caught real issues, E2E validators found genuine Gherkin violations, prompt-engineers made substantive fixes, and re-verification confirmed the fixes. Zero false positives. No thrashing. Linear flow from finding to fix to verification.

**Implication:** The review pipeline does not need architectural redesign. It needs deduplication (spawn 1 per role, not N) and the review orchestration flow codified in the workflow to prevent user micromanagement (I13).

### Pattern 5: User Frustration Follows Lost State
The 4 frustration moments (F1-F4) all share a common trigger: the user could not see or trust the agent's understanding of state. The data dump (F1) showed the agent hadn't synthesized state. The task list failures (F2) showed the agent wasn't tracking state. The thin analysis (F3, F4) showed the agent couldn't observe its own state.

**Implication:** State visibility is a UX priority. Every long-running workflow needs persistent, visible state tracking (TaskCreate/TaskList) and synthesis-first output.

### Pattern 6: Self-Messaging and Routing Artifacts
Multiple agents received messages from themselves due to role-based routing delivering to all agents with that role. Agents handled it gracefully (recognized and ignored), but each added 1-2 unnecessary turns.

**Implication:** Message routing should be instance-based (specific agent ID), not role-based, when multiple agents share a role name. This is a secondary consequence of the duplication problem — with 1 agent per role, self-messaging doesn't occur.

### Pattern 7: Audit Tooling Needs Calibration
The extraction pipeline had two significant accuracy issues: 65% false-positive rate on error detection (S10), and 18 agents unparseable due to JSONL schema variations. The audit partially blind and its error metrics unreliable.

**Implication:** Before the next sprint, the extraction script needs calibration: filter errors by actual error indicators (not string matching), and handle multiple JSONL schema variants. Reliable audit tooling is a prerequisite for the observability flywheel.

---

## Metrics

| Metric | Value |
|---|---|
| **Sprint duration** | ~20 hours (03:00-23:00 UTC) |
| **Sessions** | 8 |
| **Stories completed** | 4/4 |
| **Total subagents spawned** | 97 |
| **Parseable agents** | 79 |
| **Unparseable agents (schema mismatch)** | 18 |
| **Total transcript size** | 27,132 KB |
| **Total assistant turns** | 3,799 |
| **Wasted by duplication (KB)** | 12,981 (47.8%) |
| **Wasted by duplication (turns)** | 1,662 (43.7%) |
| **Unique work turns** | ~2,137 |
| **Human messages (total)** | 246 |
| **Human messages (genuinely typed)** | 89 |
| **Inter-agent messages** | 231 |
| **Tool errors (flagged)** | 806 |
| **Tool errors (true)** | ~277 |
| **Tool errors (false positive)** | ~529 (65.6%) |
| **User corrections** | 10 |
| **User frustration moments** | 4 |
| **User praise/approval signals** | 9 |
| **Correction-to-praise ratio** | 10:9 |

### Dev Iterations Per Story

| Story | Agents Spawned | Agents Needed | Turns (per agent) | Errors (per agent) |
|---|---|---|---|---|
| backlog-priority-field | 2 | 1 | 90-91 | 23 (TDD) |
| impetus-allowed-tools-restriction | 3 | 1 | 56-60 | 0 |
| epic-grooming | 2 | 1 | ~83 | Moderate |
| refine-skill | 7 | 1 | 70-76 | 6 |

### Review Layer

| Role | Spawned | Needed | Waste % |
|---|---|---|---|
| QA Reviewer | 17 | 2 | 88% |
| E2E Validator | 14 | 2 | 86% |
| Prompt Engineer | 7 | 1 | 86% |
| **Total review** | **38** | **5** | **87%** |

### Error Distribution (True Errors Only)

| Category | Count | Notes |
|---|---|---|
| file-not-found | 166 | Mix of path typos and exploration |
| already-exists | 53 | Write conflicts from duplicate agents |
| file-too-large | 43 | Token limits; agents recovered with offset/limit |
| InputValidationError | 11 | Wrong parameter types/names |
| Permission | 3 | Minor |
| Timeout | 1 | Minor |

---

## Priority Action Items

### Critical (Fix Before Next Sprint)
1. **Fix orchestrator agent deduplication** — Track spawned agents by (story, role). Never re-spawn duplicates. Eliminates ~48% compute waste.
2. **Codify team composition in workflows** — Required roles (including dev/fixer), spawning mode (individual vs. TeamCreate), and concurrency expectations must be explicit workflow parameters.
3. **Mandatory task tracking in long sessions** — TaskCreate at session start, maintained throughout. Non-negotiable for sprint-dev and sprint-planning.

### High (Fix Soon)
4. **Sprint planning synthesis-first** — Lead with prioritized recommendations, not raw data dumps. Include staleness check against git history.
5. **Codify review orchestration flow** — AVFL (no-fix mode) + concurrent code-reviews -> results to review team. Should not require user specification.
6. **Fix message routing** — Instance-based routing when multiple agents share a role, not broadcast to all.

### Medium (Improve)
7. **Agent logging/observability** — Strategic priority. The practice improvement flywheel depends on this.
8. **E2E validator ToolSearch guidance** — Add tool discovery instructions or pre-load SendMessage in spawn config.
9. **Calibrate extraction tooling** — Filter errors by actual indicators, handle JSONL schema variants.

### Preserve (Do Not Change)
10. Parallel worktree dev execution model
11. Review pipeline architecture (QA -> fix -> E2E verify)
12. Single-letter menu UX
13. Explore agent scoping pattern
14. Design discussion / thinking partner capability
