# Sprint Transcript Audit — sprint-2026-04-06-2 (TeamCreate version)

**Retro date:** 2026-04-07
**Sprint completed:** 2026-04-07
**Data analyzed:** 684 user messages | 359 subagents | 584 tool errors | 589 team messages
**Audit method:** Collaborative TeamCreate (auditors send findings via SendMessage, documenter iterates)

## Executive Summary

Sprint-2026-04-06-2 delivered 9 stories across 2 waves but exposed systemic issues in three areas: plugin installation reliability, agent population management, and UX quality of the Impetus orchestrator. The single most painful episode was a multi-hour plugin installation saga where the agent repeatedly claimed success while the user faced clear errors — revealing the absence of end-to-end validation after plugin changes. The Impetus orchestrator's first invocation was a UX disaster (3+ minute startup, ugly rendering, exposed implementation details, no personality), requiring an entire sub-sprint to remediate — and performance still was not fully resolved.

On the positive side, the quality gates matured significantly this sprint. E2E validation achieved zero false positives with every FAIL leading to a genuine fix. The review-fix-verify cycle converged in single iterations consistently. The AVFL pre-dev checkpoint caught a critical concurrent-write conflict that story-level review would have missed. Prompt quality for review agents improved dramatically, cutting turn counts by 3-6x compared to prior sprints. The user validated several architectural wins: the 9-state greeting architecture, CMUX passive review surfaces, and the simplified agent model (single dev agent + scoped guidelines).

The sprint's compute efficiency was poor. Redundant agent spawning wasted an estimated 10MB+ of context across 18 idle QA reviewers, 7 duplicate prompt-engineers, and 23 ghost agents that never activated. Combined with 196 file-too-large errors (agents not taught to handle the Read tool's token limit), the sprint burned significant resources on avoidable overhead. The extraction pipeline itself had reliability issues, with 22.6% of agent transcripts unparseable due to malformed JSONL.

## What Worked Well

### E2E validation is the most productive quality gate
E2E validators achieved 43/52 scenario PASS with 2 genuine FAILs and 7 correctly-identified MANUAL items. Zero false positives across all sprints examined. Every FAIL led to a committed fix. The BLACK-BOX constraint ("MUST NOT read source code") prevents validators from cheating by reading implementation.
**Evidence:** agent-af7c8448581b0e695 (98 turns, 460KB) produced structured report; prior sprint validator caught issues fixed in commits e9ce1a7 and b2c04eb.
**Recommendation:** KEEP — this is the highest-ROI quality gate in the practice.

### Review-fix-verify cycle converges in one iteration
Across all sprints examined, the pattern is consistent: E2E validators find issues, prompt-engineer fixes all in a single commit, validator re-verifies and confirms resolution. No back-and-forth, no reverts, no disagreements.
**Evidence:** Sprint-2026-04-06 E2E found 6 findings across 4 features; prompt-engineer fixed all in commit 05de33e; re-validation confirmed all 6 resolved.
**Recommendation:** KEEP — single-iteration convergence indicates findings are clear, actionable, and correctly scoped.

### QA reviewers catch AC gaps and partial implementations
QA review correctly identified partial implementations (e.g., transcript-query-calibration AC1 flagged as PARTIAL for string-matching vs. structural JSON check). The AC-level granularity catches what passes casual inspection.
**Evidence:** agent-ae81cd29eee14cd23 (67 turns) identified specific AC gaps; prior sprint QA produced "FAIL — 26/39 ACs (67%)" with story-level breakdown.
**Recommendation:** KEEP — QA review is effective. Sprint-2026-04-06-2 achieved 67-turn efficiency vs. 311 turns in prior sprint.

### AVFL pre-dev checkpoint catches cross-story conflicts
The AVFL enumerator running before dev execution caught a critical concurrent-write conflict: four stories writing to sprint-dev/workflow.md simultaneously in Wave 1. This systemic risk is invisible to individual story reviewers.
**Evidence:** agent-a0196a2758a17409d (33 turns) rated finding as CHECKPOINT_WARNING, appropriately escalating without blocking.
**Recommendation:** KEEP — sprint-level pre-dev validation catches interaction bugs that story-level review misses.

### Review agent prompt quality improved dramatically
Prompts evolved from generic ("Sprint sprint-2026-04-04-3. 4 stories.") to structured (story lists, branch names, spec paths, explicit role constraints). This directly correlates with 3-6x efficiency improvement in turn counts.
**Evidence:** Sprint-2026-04-06-2 reviewers completed in 67/98 turns vs. 311/582 turns in sprint-2026-04-05-2.
**Recommendation:** KEEP — the structured prompt format with explicit constraints is a validated efficiency lever.

### CMUX passive review surfaces keep users engaged
When CMUX markdown surfaces were adopted for story review during sprint planning, the user could review artifacts as they were created rather than after-the-fact. Passive review (show it, user speaks up if concerned) outperformed approval-gated review (block until approved).
**Evidence:** User: "Instead of me sitting here doing nothing, would it be possible for me to be involved in the fleshing out of the stories?" After adoption: "No let's not go through an approval cycle, just put them there."
**Recommendation:** KEEP — passive CMUX review is a validated engagement pattern. Use informational surfaces, not blocking gates.

### Simplified agent model validated (dev + scoped guidelines)
Instead of N specialist agent files (frontend-dev, backend-dev, build-dev), use 1 dev agent with directory-scoped guidelines in CLAUDE.md. Methodology (TDD/EDD) is the agent's concern; domain knowledge (kotlin/python/gradle) is the project's concern.
**Evidence:** User: "So nornspun would still have frontend and backend developers but they are both 'dev' agents configured in Claude.md to use different guidelines."
**Recommendation:** KEEP — this architectural insight reduces agent complexity while preserving specialization.

## What Struggled

### S1. Plugin installation was a multi-hour nightmare
The Momentum plugin installation required 6+ attempts spanning ~40 minutes. The agent repeatedly claimed "installed and working" while the user was seeing clear ENAMETOOLONG and "Invalid input" errors. `/momentum:dev` returned "Unknown skill" after the agent declared success.
**Evidence:** User: "This can't be this hard can it?" / "I don't see it at all. What the heck, man!" / "No you didn't make any changes. You just said you need to change the format."
**Root cause:** Plugin manifest format (plugin.json skills array) was wrong. Agent had no way to validate the manifest schema against what Claude Code expects. Agent described fixes without executing them.
**Recommendation:** FIX — Add mandatory E2E smoke test after plugin changes: install plugin, invoke a skill, verify response. Consider CMUX terminal testing as standard plugin dev step.

### S2. Impetus first impression was terrible — slow, ugly, confusing
First invocation: 3+ minute load time, gray fill bars rendering incorrectly, diff output visible to user, wave/story implementation details exposed, no personality. User: "Wow that was shockingly bad. It took over 3 minutes...it's horrible and embarrassing."
**Evidence:** User: "800 line workflow?!?!?!?!?!" / "Why are they talking about waves?" / "sounds more like I'm buying a sandwich at a cafe."
**Root cause:** No performance budget existed. The 800-line monolithic workflow.md was read on every startup. UX was designed without visual testing. Voice/personality was missing from the spec.
**Recommendation:** FIX — Establish measurable performance targets (e.g., startup < 15s). Modularize workflow files. Include voice/personality as first-class architecture requirements. Visually test greeting output before shipping.

### S3. Performance not resolved despite dedicated sprint
After the greeting-redesign sub-sprint shipped, Impetus was STILL slow on next invocation. The content was fixed but the root cause (workflow file size, tool call count) persisted. User: "Wow...that took a freakin' year to load this. We just had an entire sprint to fix this."
**Evidence:** Performance story was in scope but the fix was incomplete — cosmetic changes without addressing the fundamental bottleneck.
**Root cause:** No measurable performance AC was defined. "Make it faster" is not testable. No before/after measurement, no regression test.
**Recommendation:** FIX — Performance stories must have numeric targets: "Reduce workflow.md below 400 lines, startup under 15 seconds, max 10 tool calls during greeting." Measure before and after.

### S4. Massive redundant agent spawning — 82% compute waste
18 idle QA reviewers, 7 duplicate prompt-engineers (only 1 needed), 23 ghost agents (0 turns), and 12+ duplicate E2E validators. Total wasted context estimated at 10MB+. The review workflow spawned fresh agent teams on every run rather than reusing existing agents.
**Evidence:** 7 prompt-engineers with identical prompts; 6 ran to completion (~106-140 turns each) doing the same work on the same commits. If consolidated to 1 agent, would save ~624 redundant turns and ~7,272KB of context.
**Root cause:** Orchestrators have no spawn registry. Each review pass creates a fresh team. No check for existing agents with the same role/sprint.
**Recommendation:** FIX — Implement agent spawn deduplication in sprint-dev and review orchestrators. Story orchestrator-deduplication-guard was created this sprint but needs verification that it covers review team spawning.

### S5. file_too_large errors dominate the error population (33.6%)
196 of 584 errors were agents hitting the Read tool's token limit on large files without using offset/limit parameters. This is the single most common error type and is entirely preventable.
**Evidence:** 33.6% of all tool errors. Agents attempt to read entire architecture docs, PRDs, and JSONL extracts, fail, then retry or work around — adding 1-3 wasted turns per occurrence.
**Root cause:** Agent prompts and definitions do not include guidance on handling large files with offset/limit parameters.
**Recommendation:** FIX — Add standard instruction to agent definitions: "When reading files that may be large (architecture.md, prd.md, JSONL extracts), use offset/limit parameters or search for specific content."

### S6. TeamCreate in sprint-dev was never implemented
The core agent team creation step (Dev + QA + E2E Validator) was missing from sprint-dev execution. User: "I saw NO TeamCreate." Despite being planned and discussed across multiple sprints, the feature was never actually implemented in code.
**Evidence:** User: "Whoa...I was certain we had fixed that. Can you do an exhaustive search of git and also the master plan?"
**Root cause:** A story being marked "complete" doesn't mean the feature works. No verification step checks that planned features actually landed and function.
**Recommendation:** FIX — Sprint completion verification must include feature-level smoke tests, not just story-level AC checks. "Is TeamCreate actually invoked during sprint-dev?" is a yes/no question that was never asked.

### S7. Gherkin ATDD outsider principle repeatedly violated
Quick-fix workflow generated Gherkin specs from acceptance criteria (implementation-coupled) rather than from behavioral intent (outsider perspective). Specs referenced internal code details rather than observable behavior.
**Evidence:** User: "WHOA! Why is it basing the specs on the ACs? That is a HUGE NO NO!" / "Was it your intention to create E2E behavior specs? Or to have a QA look at code."
**Root cause:** The Gherkin generation step in quick-fix did not include the outsider test guardrail that sprint-planning enforces. Not all spec-generation paths share the same quality constraints.
**Recommendation:** FIX — Add explicit instruction to ALL Gherkin generation paths: "Write specs as if you have ZERO access to the code repository. Derive scenarios from the story description and user intent, NEVER from acceptance criteria or implementation details."

### S8. Agent defaulted to guessing instead of empirical testing
During plugin debugging, the agent made repeated guesses about manifest format rather than testing empirically. The user had to suggest CMUX terminal testing, which was the breakthrough.
**Evidence:** User: "Instead of guessing, why don't you fire up a CMUX surface terminal where you can start claude code and test it."
**Root cause:** Agent lacked a debugging strategy for plugin development. No workflow step mandated empirical testing.
**Recommendation:** FIX — Plugin development workflow should include "test in CMUX terminal" as a mandatory step. More broadly, agent debugging heuristics should prefer empirical testing over inference.

### S9. 22.6% of agent transcripts unparseable in extraction pipeline
81 of 359 agents had malformed JSONL (Python dict syntax with NULL instead of JSON null, single quotes). These agents' data is completely missing from analysis.
**Evidence:** Consistent error: "Malformed JSON at byte 1" with Python repr output in JSONL files. Affected qa-reviewer (17), documenter (7), dev-refine-skill (7), and many specialist types.
**Root cause:** Transcript extraction encounters tool_result entries containing Python repr output rather than JSON. DuckDB's read_json rejects the entire file on encountering these entries.
**Recommendation:** FIX — Pre-process JSONL to normalize Python-style entries before DuckDB ingestion, or parse line-by-line and skip unparseable entries rather than losing entire agent transcripts.

### S10. Write-before-read errors and tool-availability confusion
40 write-before-read errors (agents skipping Read to save a turn) + 12 file-modified-since-read errors (concurrent agents editing shared files) + 6 no-such-tool errors (Explore agents asked to write).
**Evidence:** 52 file-write errors (8.9% of all errors). Write-before-read always fails and requires retry.
**Root cause:** Agents skip Read to save turns. Orchestrators route write tasks to read-only agents. Concurrent worktree agents lack coordination on shared files.
**Recommendation:** FIX — Emphasize "always Read before Write/Edit" in agent definitions. Ensure orchestrators only route write tasks to agents with write tools.

### S11. dev-fix role is vestigial — prompt-engineers do all fixing
5 dev-fix agents spawned across all sprints, 0 had any active turns. Meanwhile, 6 prompt-engineer agents did all actual fixing work (106-140 turns each).
**Evidence:** dev-fix role is spawned by review orchestration but never receives work. The prompt-engineer role has absorbed the dev-fix responsibility entirely.
**Root cause:** Review team composition spec includes dev-fix but the workflow routes all fix work to prompt-engineers.
**Recommendation:** FIX — Remove dev-fix from review team composition or clarify when dev-fix vs. prompt-engineer should be used.

### S12. E2E validator blocked by sequential dependency chains
Review agents sat idle waiting for upstream tasks to complete. Multiple agents burned context just to poll task status.
**Evidence:** agent-a0b4eafc712a2d83b (10 turns) and agent-a3c9a6eea726a9493 (9 turns) spent entire lifecycle waiting. Team message: "I'm ready to start task 4, but tasks 1, 2, and 3 are still showing as pending."
**Root cause:** Review workflow creates sequential dependencies (tasks 1-3 block task 4 block task 5) when E2E validation against Gherkin specs doesn't actually depend on QA findings.
**Recommendation:** FIX — Allow E2E validators to start in parallel with QA review. E2E tests against Gherkin specs are independent of QA review findings.

## User Interventions

| # | Type | Severity | Summary | Quote |
|---|------|----------|---------|-------|
| 1 | Frustration | High | Plugin install claimed success when failing | "This can't be this hard can it?" |
| 2 | Frustration | High | Plugin skill not visible after install | "I don't see it at all. What the heck, man!" |
| 3 | Correction | High | Agent described fix without executing it | "No you didn't make any changes. You just said you need to change the format." |
| 4 | Redirection | High | User taught CMUX debugging strategy | "Instead of guessing, why don't you fire up a CMUX surface terminal" |
| 5 | Frustration | High | Impetus first impression terrible | "Wow that was shockingly bad...it's horrible and embarrassing." |
| 6 | Frustration | High | 800-line workflow discovery | "800 line workflow?!?!?!?!?! WHAAT?!?!" |
| 7 | Correction | High | Greeting exposed implementation details | "Why are they talking about waves?" |
| 8 | Correction | Medium | Too much story-level detail in greeting | "still too much detail. If it's not blocked I don't care." |
| 9 | Correction | Medium | Impetus lacked personality/voice | "He sounds more like I'm buying a sandwich at a cafe." |
| 10 | Frustration | High | Performance still bad after optimization sprint | "Wow...that took a freakin' year to load this." |
| 11 | Correction | High | Gherkin specs derived from ACs not behavior | "WHOA! Why is it basing the specs on the ACs? That is a HUGE NO NO!" |
| 12 | Correction | Medium | Gherkin specs referenced code internals | "Was it your intention to create E2E behavior specs? Or to have a QA look at code." |
| 13 | Redirection | Medium | User wanted CMUX review during sprint planning | "would it be possible for me to be involved in the fleshing out?" |
| 14 | Correction | Medium | Rejected approval-gated review | "No let's not go through an approval cycle, just put them there" |
| 15 | Correction | High | TeamCreate missing from sprint-dev | "I saw NO TeamCreate" |
| 16 | Correction | High | TeamCreate thought to be fixed but wasn't | "Whoa...I was certain we had fixed that." |
| 17 | Correction | Medium | Hook for version bumping not active | "I thought we had a hook and yet you asked me to push without checking the plugin." |
| 18 | Correction | Medium | Agent confused project-specific vs practice-level scope | "No this isn't part of the backlog at all. That's wrong." |
| 19 | Frustration | Medium | Sprint planning presented wall of text | "Good lord that is a wall of crap." |
| 20 | Correction | Medium | Workflow optimization not addressing root cause | "didn't you tell me the reason was that the workflow was very long?" |
| 21 | Correction | Low | Agent asked for merge confirmation against rules | "Why are you asking for confirmation to merge?" |
| 22 | Correction | Low | Quick-fix skipped developer review gate | "Is there something wrong with our workflow that you didn't show it to me?" |

**Total user interventions: 22** (10 high severity, 9 medium, 3 low)

## Story-by-Story Analysis

### Plugin Installation & Manifest (plugin-cross-references, sprint-2026-04-04-2)
The most painful episode of the sprint. Required 3 dev agents totaling 372 turns and 23 errors across 46-file cross-reference updates. The manifest format was wrong, agent couldn't self-test, and the user spent ~40 minutes in a frustrating cycle of install/fail/retry. The breakthrough came when the user suggested CMUX terminal testing. This story alone accounts for a disproportionate share of user frustration.

### Impetus Greeting Redesign (sprint-2026-04-06-2 stories)
Required an entire sub-sprint to fix. The content problems (information hierarchy, personality, adaptive menus) were resolved successfully — user reaction was ecstatic ("YES, YES, YES!!!!!"). But performance (startup time) remained unresolved despite being in scope. The 9-state greeting architecture is a validated win; the implementation path was unnecessarily painful.

### Gherkin Spec Generation (quick-fix workflow)
Violated the outsider test principle in two distinct ways: (1) deriving specs from ACs rather than behavioral intent, (2) referencing code internals in spec scenarios. Both were caught by the user, not by any quality gate. The sprint-planning workflow handles this correctly; the quick-fix workflow does not share the same guardrails.

### Agent Team Model (sprint-2026-04-06-2)
Successfully validated the simplified model (dev + scoped guidelines). User drove the key architectural insight that methodology is the agent's concern while domain knowledge is the project's concern. This will simplify the agent definition structure going forward.

### Orchestrator Deduplication Guard (sprint-2026-04-06-2)
Created this sprint to address the redundant spawning problem. Needs verification that it covers review team spawning (not just dev agents) — the audit shows the review workflow is actually the worst offender for duplication.

## Cross-Cutting Patterns

### Pattern 1: Agents claim success without verification
Appears in: plugin installation (S1), TeamCreate implementation (S6), performance optimization (S3).
The common thread is agents declaring work "done" without empirical verification. The plugin agent said "installed and working" without invoking the plugin. TeamCreate was marked "complete" without testing that it fired during sprint-dev. Performance was "optimized" without measuring startup time.
**Systemic fix:** Every story completion must include a verification step that exercises the feature, not just confirms the code was written.

### Pattern 2: Compute waste from uncontrolled agent spawning
Appears in: redundant reviewers (S4), ghost agents (EF-3), duplicate prompt-engineers (EF-1), duplicate validators (EF-2), blocked waiting agents (S12).
The orchestrator spawns agents aggressively but has no mechanism to reuse, deduplicate, or cancel them. The sprint burned an estimated 10MB+ of context and 600+ redundant turns on agents that either duplicated work, never activated, or sat idle.
**Systemic fix:** Agent spawn registry with deduplication, reuse across review passes, and idle-agent cleanup.

### Pattern 3: Error patterns that could be eliminated by better prompts
Appears in: file_too_large (S5), write-before-read (S10), tool-not-available (S10).
These three error types account for 43.7% of all tool errors (255/584). All are preventable with better agent prompt engineering — teaching agents about file size limits, enforcing read-before-write, and ensuring orchestrators route to correctly-tooled agents.
**Systemic fix:** Add standard operational instructions to all agent definitions covering file handling, tool prerequisites, and large file strategies.

### Pattern 4: Quality gates work but are unevenly applied
Appears in: E2E validation success (RF-2) vs. Gherkin outsider violations (S7), QA catching AC gaps (RF-3) vs. TeamCreate never verified (S6).
The quality gates that exist (E2E validation, QA review, AVFL checkpoint) are highly effective — zero false positives, single-iteration convergence. But these gates are not applied uniformly. Quick-fix bypasses the outsider test. Sprint completion lacks feature verification. The gates work; they just don't cover everything yet.
**Systemic fix:** Audit all workflow paths (sprint-dev, quick-fix, etc.) to ensure they share the same quality constraints. Create a quality gate checklist that every workflow path must satisfy.

### Pattern 5: User drives architectural decisions and debugging strategies
Appears in: CMUX testing suggestion (S8), simplified agent model design, sprint-vs-backlog judgment, multi-dev team composition proposal.
The user consistently contributes strategic judgment that the agent cannot replicate: when to sprint vs. backlog, how to debug plugin issues empirically, when work parallelization makes sense within a story, and architectural simplification insights. The agent contributes research and execution; the user contributes judgment and direction.
**Systemic fix:** This is expected and healthy in an agentic workflow. Impetus should present clear decision points that invite user judgment rather than defaulting to either option.

### Pattern 6: Extraction pipeline reliability limits retro quality
Appears in: 22.6% of agent transcripts unparseable (S9).
With nearly a quarter of agent data missing from analysis, the audit findings are necessarily incomplete. Any patterns involving qa-reviewer, documenter, or dev-refine-skill agents are underrepresented.
**Systemic fix:** Fix the JSONL extraction pipeline to handle Python repr output and non-standard JSON before the next retro.

## Metrics

| Metric | Value |
|--------|-------|
| User messages analyzed | 684 |
| Subagents analyzed | 359 |
| Tool errors detected | 584 |
| Struggles identified | 12 |
| Successes identified | 7 |
| User interventions | 22 |
| Cross-cutting patterns | 6 |
| Agents with 0 turns (ghost/idle) | 23 |
| Redundant reviewer agents | 18+ |
| file_too_large errors (preventable) | 196 (33.6%) |
| Agent transcripts unparseable | 81 (22.6%) |
| E2E validation pass rate | 43/52 (82.7%) |
| E2E false positive rate | 0% |
| Review-fix convergence iterations | 1 (consistent) |

## Priority Action Items

| Priority | Item | Recommended Story Title |
|----------|------|------------------------|
| P0 | Agent spawn deduplication — verify dedup guard covers review teams, not just dev agents | `verify-orchestrator-dedup-guard-review-coverage` |
| P0 | Add standard large-file handling instructions to all agent definitions | `agent-prompt-large-file-guidance` |
| P1 | Plugin development workflow with mandatory CMUX smoke test | `plugin-dev-e2e-validation-workflow` |
| P1 | Measurable performance budget for Impetus startup (target: < 15s, < 10 tool calls) | `impetus-startup-performance-budget` |
| P1 | Unify quality gates across all workflow paths (sprint-dev, quick-fix) | `quality-gate-parity-across-workflows` |
| P1 | Gherkin outsider-test guardrail enforced in all spec-generation paths | `gherkin-outsider-guardrail-all-paths` |
| P2 | Sprint completion verification: feature-level smoke tests, not just AC checks | `sprint-completion-feature-verification` |
| P2 | Fix JSONL extraction pipeline for Python repr / non-standard JSON entries | `transcript-extraction-pipeline-robustness` |
| P2 | Remove vestigial dev-fix role from review team composition | `review-team-composition-cleanup` |
| P2 | E2E validators run in parallel with QA review (remove sequential dependency) | `review-pipeline-parallel-e2e` |
| P2 | Workflow file size budget / modularization strategy | `workflow-modularization-strategy` |
| P3 | Self-addressed message filtering in SendMessage routing | `sendmessage-self-routing-filter` |
| P3 | E2E validator turn budget (guard at 150 turns for standard sprint) | `e2e-validator-turn-budget` |
