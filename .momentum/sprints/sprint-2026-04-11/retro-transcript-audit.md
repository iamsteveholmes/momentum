# Sprint Transcript Audit — sprint-2026-04-11

**Retro date:** 2026-04-12
**Sprint completed:** 2026-04-12
**Data analyzed:** 169 user messages | 74 subagents | 156 errors | 56 team messages

## Data Scope Advisory (read before interpreting findings)

The audit extracts for sprint-2026-04-11 **do not contain execution transcripts for the five named stories** (feature-artifact-schema, feature-status-skill, sprint-boundary-compression, impetus-feature-status-cache, feature-status-practice-path). Independent verification against all three extract files returns zero mentions of any of those story names in agent `first_prompt` values or user messages, and the project has no `.claude/momentum/sprint-logs/sprint-2026-04-11/` directory (the log tree stops at sprint-2026-04-08).

What the extracts *do* contain, by date:

| Date | User msgs | Team msgs | Errors | Dominant activity |
|------|-----------|-----------|--------|-------------------|
| 2026-04-09 | 51 | 9 | 58 | Sprint-2026-04-08 post-merge AVFL, E2E validator iterations |
| 2026-04-10 | 23 | 46 | 60 | Sprint-2026-04-08 retrospective team session |
| 2026-04-11 | 95 | 1 | 38 | Pre-sprint discovery: ultraplan research, BMad 6.3.0 evaluation, feature-status ideation |

This audit therefore evaluates two real things:

1. **The pre-sprint discovery work** that produced sprint-2026-04-11's five stories (conceived 2026-04-11 evening via `/momentum:decision` on feature-status).
2. **Practice spillover from sprint-2026-04-08** (E2E validator, retro pipeline) that consumed sprint-2026-04-11's working window.

The audit **cannot speak** to the correctness, iteration count, or agent behavior of the five named stories' implementations. That data is either outside the captured window or was never captured (no sprint-log directory exists).

The extract-date-filter itself is the top finding — the retro tooling must not silently mis-window transcripts, and a missing sprint-log directory should be a hard error in retro preflight.

## Executive Summary

Sprint-2026-04-11's most valuable signal is its absence: the retro's transcript-extract pipeline produced a dataset that does not contain execution of the sprint's five named stories. The sprint's genesis *is* visible (the 2026-04-11 evening `/momentum:decision` session where feature-status was conceived, scoped, and converted to story stubs), and it reveals strong practice patterns — conversational decision-capture, early-returns for adopt/adapt/reject, caching-as-design-constraint — but the dev/review/validate cycle itself is missing. This is not a sprint failure; it is a retro-tooling failure.

Within the captured window, the two most-cited struggles are re-discoveries of sprint-2026-04-08 retro findings: the E2E validator's black-box violations (7 human-audit findings on 2026-04-09, all with explicit quotes like "NEVER EVER EVER EVER looks at source code") and the retro pipeline itself (5 documenter instances, 3 duplicated auditor roles, no `documenter` alias in the team config forcing auditors to re-resolve addressing). Both have dedicated action items in the sprint-2026-04-08 retro; their re-appearance here confirms the fixes were either not yet merged when the 04-11 extracts were captured, or are still pending.

Genuine sprint-2026-04-11 findings are clustered on 04-11 evening: a strong conversational-design signal ("Impetus is already too slow" → feature-status must ship cached-first), user explicit rejection of agent over-asking ("You're not supposed to ask me that! You should check it yourself."), and a context-drift complaint ("Often times you get lost in between workflows"). These three are the real sprint-2026-04-11 signals worth acting on. Priority actions: (1) fix retro extract-date-filter to hard-fail on missing sprint-log, (2) preserve the cached-first/async-refresh design pattern for Impetus sub-features, (3) add a "don't ask, verify" rule for agents with tool access to the thing they'd otherwise ask about.

## What Worked Well

### Decision Skill as Conversational Design Vehicle (04-11 evening)
**Description:** The `/momentum:decision` session on 2026-04-11 evening (23:08–23:56) successfully carried feature-status from concept to stub stories in a single conversational pass. Eight user messages in the session used explicit adopt/adapt/reject vocabulary, producing scoped acceptance conditions and sequencing decisions inline.
**Evidence:** User messages: "adopt but I think it needs to do a bit more" (23:23), "adapt I think Impetus is already too slow" (23:27), "adapt There is no reason that some of these stories couldn't be run concurrently" (23:43), "Maybe that was a reject" (23:43:50). The session ended with: "Prepare a prompt for me, I'll use it in another session, for sprint planning" (23:56).
**Recommendation:** KEEP — The decision-skill's adopt/adapt/reject vocabulary produces fast, scoped design conversations. Carry this pattern into feature-grooming and epic-grooming.

### User Exercises "Maybe That Was a Reject" as First-Class Signal
**Description:** User reframed their own prior input mid-conversation ("Maybe that was a reject. Because this is something sprint planning determines") — treating their own decisions as revisable. The agent correctly captured this without defensiveness.
**Evidence:** 23:43:50 on 04-11, in the feature-status decision session.
**Recommendation:** KEEP — Design conversations must permit the user to reverse themselves without friction. The decision-skill did this correctly.

### Retro Team Collaboration (TeamCreate) Produces Structured Findings
**Description:** The retro team (this team) converged cleanly: 21 unique messages in a short window, three auditors producing structured JSON findings, documenter synthesizing cross-cuts. Auditor-review's RF-00 scope-warning was detected and escalated *before* synthesis, preventing a mis-framed report.
**Evidence:** auditor-review identified the data-scope mismatch (RF-00) and routed it through team-lead when `documenter` name resolution failed; documenter verified independently before writing.
**Recommendation:** KEEP — TeamCreate is the right shape for retro synthesis. The addressing issue (RF-04) is a prompt-quality fix, not a pattern fix.

### Quality Gate Calibration Held (from captured window)
**Description:** From the captured window, auditor-review observed: all AVFL findings led to fixes, all E2E failures converged to PASS, no false positives from quality gates.
**Evidence:** RF-01: QA reviewer (sprint-2026-04-08) — 87 turns, 1 error, 14 genuine findings, 13 files changed as remediation. RF-08: zero false positives in captured window.
**Recommendation:** KEEP — The AVFL checkpoint remains the sprint's highest-value quality gate. Do not loosen its calibration.

### Research Fan-Out Pattern: 7 Parallel Queries, 0 Errors
**Description:** Seven parallel technical-research agents launched on 2026-04-11 23:01 (AI workflow metrics project) completed cleanly with zero errors across any agent. Turn counts: 3, 23, 26, 27, 36, 45 + 16-turn synth agent. The 3-turn outlier is worth a lightweight follow-up but doesn't invalidate the pattern.
**Evidence:** auditor-execution: "7 research agents, 0 errors across any of them... Research fan-out is the healthiest pattern in this sprint." User messages at 23:01:41–23:02:11 launched 5 of the 7 queries within 30 seconds.
**Recommendation:** KEEP — Research fan-out is the model pattern for parallel discovery. Zero-error rate across 7 agents indicates the prompt template + tool budget is right-sized.

### Targeted Fix Agents: 15-Turn Mean for Bounded Scope
**Description:** Eight general-purpose "targeted fix" agents averaged 15.4 turns (median 12.5) with 1 error across all 8 combined. Compare to dev-skills full flow at 79-turn mean. Targeted-fix is ~5× more efficient for scope ≤2 files.
**Evidence:** auditor-execution: turn counts 7, 10, 11, 12, 13, 16, 22, 37; each fix agent produced its own commit.
**Recommendation:** KEEP and PROMOTE — Encode as an explicit pattern: when fix scope is ≤2 files and well-scoped, prefer a targeted-fix template (file + bug + expected behavior + commit) over full dev-skills. This is already implicitly used in `/momentum:quick-fix`; worth documenting the turn-budget evidence.

## What Struggled

### Retro Extract Pipeline: Wrong Sprint Window, Silent Mis-Scope (CRITICAL)
**Description:** The retro extract pipeline produced `audit-extracts/` for sprint-2026-04-11 that contain no execution transcripts for any of the sprint's five named stories. Instead, the extracts captured the sprint-2026-04-08 retro team session (04-10) and pre-sprint discovery work (04-11 daytime).
**Evidence:** Zero matches for feature-artifact-schema, feature-status-skill, sprint-boundary-compression, impetus-feature-status-cache, feature-status-practice-path in any agent first_prompt or user message. No `.claude/momentum/sprint-logs/sprint-2026-04-11/` directory exists. 46 of 56 team-messages are from 04-10 (sprint-2026-04-08 retro team).
**Root cause:** Either (a) the stories executed in a window outside the filter, or (b) sprint-2026-04-11 has no sprint-log directory because one was never created. The retro workflow did not preflight-check either.
**Recommendation:** FIX — Retro preflight must hard-fail when sprint-log directory is missing. Extract pipeline must verify at least one agent first_prompt references a sprint-named story before writing extracts.

### E2E Validator Re-appears as a Sprint Tax Before 04-10 Retro Fixes Shipped (HIGH)
**Description:** Seven human-audit findings on 2026-04-09 all circle the same issue: E2E validator violates the black-box principle by inspecting source code, does not use cmux, and treats MANUAL as an escape hatch. These are re-discoveries of the sprint-2026-04-08 retro's Priority 1 action item.
**Evidence:** User: "It is supposed to be the most crystal clear thing in the world that the E2E NEVER EVER EVER EVER looks at source code" (17:30 04-09). User: "why is the validator still ignorant of the fact that he can run a CMUX pane/surface" (17:52 04-09). User: "I'm bothered that the E2E tester is still seamingly unaware" (14:45 04-09).
**Root cause:** The sprint-2026-04-08 retro (written 04-10) produced a dedicated action item (e2e-validator-black-box-hardening) but the fix was not yet shipped by the time 04-09 work was captured. The re-run on 04-09 17:52 still found the validator ignorant of cmux — proving that in-sprint agent-definition edits do not retroactively improve already-instantiated agents.
**Recommendation:** FIX (already queued as sprint-2026-04-08 P1; confirm shipped before next validator spawn). Retro should cross-reference prior-sprint action items and flag recurrences.

### File-Too-Large: 68/156 Errors (HIGH)
**Description:** 68 of 156 errors (44%) are "File content exceeds maximum allowed tokens." Concentrated in two populations: (a) retro auditor agents re-reading large audit extracts, (b) parallel BMad 6.3.0 evaluation fan-out where 6 of 7 evaluator agents hit exactly 2 file-too-large errors each on the same BMad docs.
**Evidence:** auditor-human (19+19), auditor-execution (4+4), auditor-review (4), general-purpose (4). Separately, the BMad 6.3.0 eval fan-out (bmad-advanced-elicitation, bmad-checkpoint-preview, bmad-party-mode, bmad-quick-dev, bmad-prfaq, Amelia-consolidation) had exactly 2 errors each — all from reading the same full BMad docs/llms.txt. That's ~12 redundant file-too-large errors in a single fan-out pattern.
**Root cause:** Two distinct sub-causes: (1) retro auditor prompts lack file-size guidance; (2) parallel evaluation fan-outs give every agent the same docs to read whole instead of pre-fetching and sharding.
**Recommendation:** FIX — Two changes: (a) update retro auditor prompts: "audit-extracts can be >10K tokens; use offset/limit or stream via python3/jq. Do not Read whole." (b) for parallel-evaluation fan-outs where every agent reads the same docs, pre-fetch + shard once centrally and pass the relevant shard to each agent. Eliminates the systematic 2-error-per-agent pattern. This overlaps with sprint-2026-04-08 retro P2 (which covered validation agents) but extends to retro-auditors and eval fan-outs.

### Retro Team Config: `documenter` Not Resolvable (HIGH)
**Description:** Three auditors generated their findings but could not send them to `documenter` because no member with that name existed in the team-config at send time (or the name resolver did not match the actual documenter's agent ID). auditor-review routed findings through `team-lead` as a fallback; auditor-human sent successfully (suggesting name-resolution is intermittent or was fixed mid-run).
**Evidence:** RF-04: `"documenter" role not in team config`. auditor-review's full findings arrived via team-lead with explicit note: "they sent these to me (team-lead) because 'documenter' wasn't resolvable in the team config."
**Root cause:** Either the team config joined `documenter` after auditors started, or the name resolver does not resolve `documenter` when addressed by name instead of agent ID. Team config snapshot shows `documenter@retro-sprint-2026-04-11` exists with `name: documenter`, so the resolver is the likely culprit.
**Recommendation:** FIX — Audit SendMessage name resolution. Test coverage should include: send to name that joined after sender. If this is a timing issue (auditor spawned before documenter joined), either (a) pre-populate all team members in config before any agent spawns, or (b) retry name resolution on miss.

### Dev-Skill File-Modified-Since-Read Races (MEDIUM)
**Description:** 10 "File has been modified since read" errors inside sprint-2026-04-08 dev-skills agents, concentrated: `quality-gate-parity-across-workflows` (4), `impetus-journal-hygiene-script` (3), `remove-agent-journals` (2), `gherkin-acs-and-atdd-workflow-active` (1). One agent hit 4 in 55 seconds (05:26:02 → 05:26:57).
**Evidence:** 10 errors of form "File has been modified since read, either by the user or by a linter. Read it again before attempting to write it."
**Root cause:** A PostToolUse lint/format hook rewrites the file after Write; the dev agent's cached read is stale; agent retries Write without re-reading.
**Recommendation:** INVESTIGATE — Either (a) make the lint hook silent about rewrites it triggers itself, or (b) add dev-skills guidance: "after any Write/Edit, re-Read before next Write to account for lint rewrites." Not blocking, but wastes turns.

### Context Drift Between Workflows (MEDIUM)
**Description:** User explicitly complained about agent losing context between workflows: "We need to stay on topic. Often times you get lost in between workflows and this tells us exactly what we need."
**Evidence:** 04-11 23:31.
**Root cause:** Long `/momentum:impetus` sessions spanning multiple sub-skills (research, decision, sprint planning) accumulate context without structural anchors; agent loses the thread when returning from a sub-skill.
**Recommendation:** FIX — Use TaskCreate/TaskList as structural state anchors during multi-skill orchestrator sessions (note: this matches the existing `project_task_tracking_for_drift` memory). Consider a re-orient step after every sub-skill return.

### Agent Over-Asking When Tool Access Is Available (MEDIUM)
**Description:** User rebuke on 04-11 23:48: "Are you kidding me? What skill is this? You're not supposed to ask me that! You should check it yourself."
**Evidence:** Single high-intensity user message at 23:48 on 04-11.
**Root cause:** Agent asked the user for information the agent had tool access to retrieve. Specific skill context is cut off in the extract, but the pattern is clear: agent defaulted to asking instead of verifying.
**Recommendation:** FIX — Add a global or per-skill rule: "Before asking the user to confirm a fact, verify whether the tools available to you can confirm it directly. Ask only if no tool can." This is a complement to the anti-pattern rule for "agents should be self-sufficient with browser automation" (sprint-2026-04-08 intervention 12).

### Abandoned Agents: 5 with 0 Assistant Turns (MEDIUM)
**Description:** Five agents loaded context (26kb–886kb) but produced 0 assistant turns. Three are this retro's in-flight agents (filter artifact). One is `agent-afcdc522dbc392e33` — a `momentum:e2e-validator` that loaded 470kb of context and produced no turns. Tagged in sprint-2026-04-08 retro's P12 (`agent-spawn-observability-metric`) but re-appears here.
**Evidence:** 5 zero-turn agents; the e2e-validator one is not from this retro.
**Root cause:** Agent spawned then superseded by retry, or parent interrupted. 470kb of context loaded but never processed.
**Recommendation:** INVESTIGATE — Already queued as P12 in sprint-2026-04-08 retro. Confirm whether observability metric has shipped; if not, promote to action item.

### Ultraplan Experiment: 90-Minute Approval Timeout (LOW / data point)
**Description:** On 04-11 early morning (00:21–02:08) the user experimented with remote `/ultraplan` cloud sessions. After ~90 minutes the session terminated: "Ultraplan terminated: no approval after 90 minutes."
**Evidence:** User messages 00:21 through 02:08 walking through the feature, followed by timeout message.
**Root cause:** Ultraplan cloud session requires user approval checkpoints; user was not available to approve within the window.
**Recommendation:** KEEP as data point — This experiment informed whether Ultraplan could be wrapped in a skill. The user concluded "it can be ran separately from momentum" (20:58 04-11). No action needed; informational.

## User Interventions

Within the captured window, the user exercised corrective authority 14+ times. Grouped by sprint boundary:

### Pre-Sprint Discovery (04-11 evening feature-status decision session)

**Intervention A: "You're not supposed to ask me that!" (23:48)**
**Context:** Agent (skill unclear from extract) asked user for information the agent had tool access to verify itself.
**User action:** "Are you kidding me? What skill is this? You're not supposed to ask me that! You should check it yourself."
**Implication:** Agent over-asking is a direct practice violation. Asking when verification is available is a signal the skill lacks a "verify first" rule.

**Intervention B: "We need to stay on topic" (23:31)**
**Context:** Agent drifted between workflow steps in the feature-status decision session.
**User action:** "We need to stay on topic. Often times you get lost in between workflows and this tells us exactly what we need."
**Implication:** Confirms `project_task_tracking_for_drift` memory: orchestrator needs structural state anchors between sub-skills.

**Intervention C: Caching-as-design-constraint (23:27–23:28)**
**Context:** User objected to a proposed Impetus enhancement on performance grounds.
**User action:** "adapt I think Impetus is already too slow. As a result, we should probably have him use a cached version of the feature, and let the user know when it's out of date."
**Implication:** User treats latency as a design constraint, not a post-hoc optimization. Story `impetus-feature-status-cache` originated here.

**Intervention D: Parallelism by sprint planning, not story spec (23:43)**
**Context:** Proposed stories had sequential ordering baked in.
**User action:** "adapt There is no reason that some of these stories couldn't be run concurrently... We should, for the most part, allow sprint planning to determine this."
**Implication:** Sequencing is sprint-planning's responsibility, not story-spec's. Story specs should not over-constrain execution order.

**Intervention E: Feature scope self-definition (19:57)**
**Context:** Discussion of what counts as a "feature" for feature-status tracking.
**User action:** "This model works, but I would say an E2E is also a feature despite being fairly broad. It's still a finite feature with a finite set of duties. So campain init is a feature for example."
**Implication:** User retains authority over feature-granularity decisions; the skill must not over-prescribe what constitutes a "feature."

### Spillover from Sprint-2026-04-08 (04-09 E2E validator cluster)

**Intervention F–L: E2E validator, seven findings from auditor-human (04-09)**
All seven intensities/quotes (summarized — full quotes in auditor-human batch 1):
- "How have we failed to do that?" (17:30) — escalation, medium severity
- "NEVER EVER EVER EVER looks at source code" (17:30) — direct invariant correction, high severity
- "I'm bothered that the E2E tester is still seamingly unaware" of cmux (14:45) — capability gap, high severity
- "why is the validator still ignorant of the fact that he can run a CMUX pane/surface" (17:52) — re-failure after fix, high severity
- "I'm glad it was honest, that's good" (17:52) — praise for honest failure over fake pass, low severity
- "re-run the E2E validator and dev at least. It seems like we don't need the other agents" (17:41) — scoped re-run, medium severity
- "Are we certain the E2E verifier verified actual black box behavior and NOT code?" (14:43) — trust in PASS verdict, medium severity

All seven are documented in the sprint-2026-04-08 retro. Their re-appearance here is a timing artifact (fix not yet merged by 04-09 capture) and is resolved by the sprint-2026-04-08 P1 action item.

### Pre-Sprint Research (04-11 daytime)

**Intervention M: "I like the idea but it can be ran separately from momentum." (20:58)**
**Context:** After evaluating BMad 6.3.0 (incl. bmad-prfaq) for Momentum integration.
**User action:** User accepted that bmad-prfaq is good, but does not need to be pulled into Momentum.
**Implication:** Scoping decision preserves Momentum's footprint. Not every good idea needs to ship with the practice.

## Story-by-Story Analysis

The five sprint-2026-04-11 stories — **feature-artifact-schema, feature-status-skill, sprint-boundary-compression, impetus-feature-status-cache, feature-status-practice-path** — have no execution data in the captured extracts. Their spec files are on disk (`_bmad-output/implementation-artifacts/sprints/sprint-2026-04-11/specs/*.feature`), and the sprint is marked complete per recent commits (`372f272 chore(plugin): bump version to 0.14.0`), but this audit cannot evaluate iteration count, review cycles, or dev-agent behavior for any of them.

What *is* visible in the captured window is their **genesis**:

- **feature-status-skill** conceived 04-11 23:08 via `/momentum:decision` after the user described the need: "items are getting completed and themes(epics) are being completed and yet no user facing capabilities are being completed. I believe this is a solution for that."
- **impetus-feature-status-cache** scoped 04-11 23:27 in direct response to user's latency concern.
- **sprint-boundary-compression** — no clear genesis visible in window; likely derived from retro-pipeline pain observed during sprint-2026-04-08 retro.
- **feature-artifact-schema** — schema-first design flagged 04-11 23:34: "different types of projects need different feature tracking and acceptance conditions."
- **feature-status-practice-path** — no clear genesis visible in window.

**Recommendation:** The retro workflow must resolve the extract-scope issue (see CRITICAL struggle above) before story-by-story analysis is possible. As-is, four of five stories have no captured execution trace.

## Cross-Cutting Patterns

### Pattern 1: Retro Infrastructure Is the Sprint's Central Risk
**Sources:** Data-scope mismatch (my verification + RF-00), retro team config name-resolution (RF-04), retro file-too-large errors (68 occurrences from auditor agents including this retro's own), retro agent duplication (RF-05: 5 documenter instances visible in prior session data).
**Analysis:** Three independent retro-pipeline issues converge: (1) extract pipeline silently mis-windowed the sprint, (2) team config name resolution drops auditor→documenter routing, (3) auditor prompts lack file-size guidance causing them to thrash on their own inputs. Each is individually fixable; together they render the retro output-quality-at-risk unless fixed.
**Impact:** Critical — the retro's output (this document) is itself a load-bearing artifact for practice improvement. A mis-scoped retro propagates errors forward.

### Pattern 2: Sprint-2026-04-08 Fix-Tail Still Visible
**Sources:** E2E validator findings (auditor-human 7 findings, auditor-review RF-02), file-too-large errors (auditor-execution), abandoned e2e-validator (auditor-execution). All re-discover sprint-2026-04-08 retro findings.
**Analysis:** The captured window (04-09 to 04-11) overlaps sprint-2026-04-08's post-merge fix work. Seven action items from that retro have not been verified shipped. Re-discovering them here is a signal that the retro-to-story pipeline has latency: findings produced 04-10 have not fully landed by 04-11.
**Impact:** High — if retro fixes don't land before the next sprint, retros re-find the same issues. Closes the loop only when pipeline is ship-fast.

### Pattern 3: Conversational Decision-Capture Works (Keep)
**Sources:** 04-11 23:08–23:56 decision session (my 04-11 content analysis), existing `/momentum:decision` design. User-auditor findings: adopt/adapt/reject pattern used 4+ times, "Maybe that was a reject" self-correction.
**Analysis:** The decision skill's adopt/adapt/reject vocabulary let the user make 5+ consequential design decisions in one session without agent re-prompting or summarization loops. The skill anchored each decision to a concrete story stub. This is an existence proof that conversational design skills can be fast, structured, and low-drift.
**Impact:** Medium — validates the design-skill pattern. Preserve it; propagate the vocabulary to feature-grooming and epic-grooming.

### Pattern 4: User Rejects Agent Over-Asking
**Sources:** Intervention A ("You're not supposed to ask me that!"), human-audit decision-points pattern.
**Analysis:** The user's tolerance for "agent asks user to verify X" is very low when tools can verify X directly. This pattern already exists as a sprint-2026-04-08 memory (agent must use cmux-browser not ask user to check browser) and as a feedback memory (`feedback_follow_workflow_exactly`). A global rule could consolidate: "Verify before asking."
**Impact:** Medium — small user-experience-eroding pattern, but recurrent across sprints.

### Pattern 5: Sprint Data Provenance Has No Enforcement
**Sources:** Data-scope mismatch, missing sprint-log directory.
**Analysis:** Sprint-2026-04-11 has no `sprint-logs/sprint-2026-04-11/` directory. Whatever execution happened did not log to the expected location. The retro workflow did not preflight this. Multiple sprints (2026-04-04 variants, 2026-04-05 variants, 2026-04-06 variants) show naming inconsistencies (`sprint-2026-04-04`, `sprint-2026-04-04-2`, `sprint-2026-04-04-3`) that suggest the sprint-logging pattern itself is not enforced.
**Impact:** High — retro quality depends on sprint-log provenance. Without it, retros audit the wrong window.

## Metrics

| Metric | Value |
|--------|-------|
| User messages analyzed | 169 |
| Subagents analyzed | 74 |
| Tool errors detected | 156 |
| - file-too-large | 68 (44%) |
| - file-modified-since-read | 10 (6%) |
| - tool-validation | 5 (3%) |
| - git (pathspec / worktree / conflict) | 3 |
| - file-not-found | 2 |
| - other | 68 (44%) |
| Errors on 2026-04-09 (prior-sprint spillover) | 58 |
| Errors on 2026-04-10 (prior-sprint retro) | 60 |
| Errors on 2026-04-11 (this sprint's visible window) | 38 |
| Team messages | 56 |
| - on 2026-04-09 | 9 |
| - on 2026-04-10 (prior-sprint retro team) | 46 |
| - on 2026-04-11 | 1 |
| Agent types seen | 10 |
| - general-purpose | 37 |
| - momentum:dev-skills | 12 |
| - momentum:e2e-validator | 7 |
| - documenter (retros) | 5 |
| - claude-code-guide | 5 |
| - auditor-execution | 2 |
| - auditor-review | 2 |
| - auditor-human | 2 |
| - momentum:qa-reviewer | 1 |
| - momentum:dev | 1 |
| Sprint-named stories visible in extracts | 0 / 5 |
| Abandoned agents (0 assistant turns) | 5 |
| Struggles identified | 9 |
| Successes identified | 6 |
| User interventions (documented) | 13 (A–M) |
| Cross-cutting patterns | 5 |
| Prior-sprint findings re-surfaced | 5+ (all match sprint-2026-04-08 retro items) |
| Total assistant turns across all agents | 2,982 |
| Total tool results across all agents | 2,202 |
| Sprint-wide tool-error rate | 4.18% (156 / 3,728 tool uses) |
| E2E validator combined turns (sprint-04-08) | 734 across 6 productive spawns |
| Dev-skills turn budget (sprint-04-08, 12 stories) | 1,033 total, mean 79, median 58, range 14–246 |
| Research fan-out (04-11): 7 agents / 0 errors | clean |
| Targeted fix agents: mean turns | 15.4 (vs dev-skills 79) |

## Priority Action Items

| # | Action Item | Priority | Source Patterns | Recommended Story |
|---|------------|----------|-----------------|-------------------|
| 1 | Fix retro extract pipeline: preflight-check sprint-log directory existence, verify at least one sprint-named story appears in agent prompts, hard-fail on mismatch instead of writing silent wrong-scope extracts | Critical | P1 (retro infrastructure), P5 (data provenance) | `retro-extract-preflight-validation` |
| 2 | Enforce sprint-log directory creation as part of sprint-planning or sprint-dev preflight; make missing sprint-log a hard error in retro workflow | Critical | P5 (data provenance) | `sprint-log-directory-enforcement` |
| 3 | Audit and fix SendMessage name resolution — test: send to name that joined team after sender; either pre-populate full team config before any agent spawns, or retry name resolution on miss | High | P1 (retro infrastructure), RF-04 | `team-config-name-resolution-fix` |
| 4 | Add file-size guidance to retro auditor prompts (audit-extracts can be >10K tokens; stream via offset/limit or python); complements sprint-2026-04-08 P2 which covered validation agents | High | P1 (retro infrastructure), file-too-large 68 errors | `retro-auditor-file-size-guidance` |
| 5 | Add "verify before asking" rule — before asking user to confirm a fact, agents must check whether available tools can confirm it directly | Medium | P4 (over-asking), Intervention A | `verify-before-asking-rule` |
| 6 | Add structural-state anchor (TaskCreate/TaskList) to `/momentum:impetus` orchestrator to prevent cross-workflow context drift | Medium | P4 (context drift), Intervention B | `impetus-workflow-state-anchor` |
| 7 | Add retro cross-reference step: before writing findings, cross-reference against prior retros' priority action items and flag recurrences (tells user "this was action-item N from sprint X, still not landed") | Medium | P2 (fix-tail latency) | `retro-prior-action-item-cross-ref` |
| 8 | Address file-modified-since-read races: either silent linter (PostToolUse) or dev-skills guidance "re-Read after Write" | Medium | dev-skills races, 10 errors | `dev-skills-lint-rewrite-awareness` |
| 9 | Ship the pending sprint-2026-04-08 P1 (e2e-validator-black-box-hardening), P2 (agent-file-size-guidance), and P12 (agent-spawn-observability) — re-appearance in this retro confirms they are not yet landed | High | P2 (fix-tail latency) | (already-queued stories) |
| 10 | Preserve the `/momentum:decision` adopt/adapt/reject conversational pattern; consider lifting to `feature-grooming` and `epic-grooming` | Medium | P3 (decision skill works) | `propagate-decision-skill-vocabulary` |
| 11 | For parallel-evaluation fan-outs where every agent reads the same docs, pre-fetch + shard once centrally and pass the relevant shard to each evaluator — the BMad 6.3.0 eval fan-out showed exactly 2 file-too-large errors per agent on the same docs (~12 redundant errors) | Medium | file-too-large BMad sub-pattern | `fan-out-pre-shard-pattern` |
| 12 | Document the "targeted-fix template" explicitly (file + bug + expected behavior + commit) as the preferred pattern for scope ≤2 files — turn-budget evidence shows 15-turn mean vs 79 for dev-skills | Low | Targeted Fix success pattern | `targeted-fix-pattern-doc` |

## Appendix: Known Limitations of This Audit

1. **Story execution data absent.** The five sprint-2026-04-11 stories' implementation transcripts are not in the captured window. Iteration counts, dev-pass success rate, review cycle counts, E2E validator behavior specific to this sprint — all unknown.
2. **04-09/04-10 spillover dominates.** 118 of 156 errors (76%) are dated before 04-11. Many findings trace to sprint-2026-04-08's post-merge and retro work, not sprint-2026-04-11 execution.
3. **Retro-self-referential errors.** Three of the four auditors in this retro (auditor-human, auditor-execution, auditor-review) hit file-too-large on the very extracts they were reading. Their own error counts are represented in the 68 file-too-large total, slightly inflating the sprint's error signal.
4. **No sprint-log for sprint-2026-04-11.** The `.claude/momentum/sprint-logs/` tree stops at sprint-2026-04-08. If dev/review/E2E for this sprint ran, they did not log there.

Findings that are grounded in 04-11 substantive content (post-19:00 feature-status decision session, morning ultraplan research) are tagged as such; all other findings should be read as "observations from the captured window" rather than "sprint-2026-04-11 execution findings."
