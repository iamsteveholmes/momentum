# Sprint Transcript Audit — sprint-2026-05-16

**Retro date:** 2026-05-17
**Sprint completed:** 2026-05-17
**Data analyzed:** 98 user messages | 70 subagents | 41 errors | 4 team messages

---

## Executive Summary

Sprint-2026-05-16 was a high-complexity architecture sprint that produced DEC-020 through DEC-027 — a full agent taxonomy redesign — alongside seven stories covering agent base bodies, a beads dual-write spike, and routing table implementation. The sprint produced genuine value: two sprint-blocking AVFL catches (status mismatch across 6 stories, malformed dependency graph) saved the sprint from null execution before it started. The architecture discussion itself was developer-led and high-quality, with the user driving key design decisions that agents could not have reached autonomously.

The dominant struggle theme was **model routing and billing opacity**: the Sonnet 4.6 model pin hardcoded across 23+ skills caused two separate billing gate incidents in two sessions. The user hit the same wall twice because the fix was not applied systemically after the first incident. A second major theme was **autonomous execution gaps**: the sprint-planning orchestrator repeatedly announced intent to proceed but then halted, requiring user re-prompting, and four distill subagents stalled on approval gates that should have been suppressed by upstream batch approval. Both themes represent workflow fidelity failures where the practice says "proceed" but the agent pauses.

Execution data revealed three actionable patterns: parallel distill agents colliding on shared target files (SKILL.md), parallel intake agents causing git lock contention, and sprint-planning skill workflow referencing stale CLI subcommands. AVFL review performance was asymmetric — Coherence & Craft executed in 1 turn with 0 tool calls using pre-injected story content, while Structural Integrity spent 57 turns re-reading files independently. The efficiency gap is an actionable design win that should be extended to all holistic validators while correctness validators retain direct file reads.

---

## What Worked Well

### AVFL Sprint-Plan Review: Sprint-Blocking Catches
The sprint-plan AVFL review caught two findings that would have caused the entire sprint to produce zero execution: stories/index.json showed `status: backlog` for 6 of 7 stories while story files declared `status: ready-for-dev` (sprint-dev reads status exclusively from index), and the depends_on graph had a missing edge for routing-table-schema that would have caused wave ordering failure. Both were caught and fixed pre-activation.

**Evidence:** HIGH-001 (6 stories silently skipped) and CRIT-001 (sprint wave ordering failure); fixes confirmed via commits be082cd and 3e78dec.
**Recommendation:** KEEP — sprint-plan AVFL review is performing its primary function. Mandatory gate.

### AVFL Story-Level Review: High-Fidelity Story Catches
The story-level AVFL for beads-dual-write-spike caught five real issues: STRUCTURAL-005 (missing `--claim` flag in AC 4 and Task 3 — a runtime-critical beads CLI step), STRUCTURAL-004 (AC 10 regression validation had no owning task), wrong file path, missing frontmatter, and incorrect commit type. These are precision catches that would have surfaced as implementation failures mid-story.

**Evidence:** Story-level AVFL findings, all fixed pre-sprint; final story score 74/100 (CHECKPOINT_WARNING).
**Recommendation:** KEEP — story-level AVFL is catching implementation-critical spec gaps.

### Coherence & Craft Validator: Zero-Tool Efficiency Design
The Coherence & Craft AVFL validator produced a complete 9-finding coherence validation in 1 turn with 0 tool calls by consuming pre-serialized story content injected into its prompt. Structural Integrity required 57 turns and 55 tool calls reading the same files independently. The efficiency gap is ~150 unnecessary tool calls per sprint-plan AVFL run.

**Evidence:** Execution findings — agent aaf924023c281045e (Coherence) vs ad0471b7a3cdc54e4 (Structural Integrity).
**Recommendation:** KEEP and EXTEND — pre-inject story content into all holistic validators; correctness validators should retain direct file reads for evidentiary grounding.

### Sprint Story Recommendations: Well-Calibrated Selection
The sprint-planning story recommendation capability presented 1-5 prioritized candidate stories, all of which were approved by the developer in full without modification.

**Evidence:** Human finding — "I liked your 1-5 recommendations. I think we should do them all."
**Recommendation:** KEEP — recommendation quality and calibration were high.

### Architecture Synthesis: DEC-020 through DEC-027
After the developer commissioned a full agent taxonomy audit, the sprint-planning session successfully synthesized a complex architecture discussion into 8 decision documents (DEC-020 through DEC-027). The agent identified the correct framing, proposed the write-up, and executed it correctly.

**Evidence:** Human findings — three high-severity decisions captured; developer approval was enthusiastic ("I like it! Let's write up all the decisions we've captured here.").
**Recommendation:** KEEP — complex synthesis under developer direction was executed correctly.

### AVFL Consolidator: Correct Fan-Out Spawning
The AVFL consolidator correctly used fan-out (independent Agent spawns) rather than TeamCreate for the review phase. Deduplication of 5 findings into a consolidated table was accurate, and severity inheritance was correct with no inter-agent coordination overhead.

**Evidence:** Review finding — agent ad66a4b6560cdd525; 1 turn, 0 tool_results, correct deduplication.
**Recommendation:** KEEP — spawning pattern selection was correct.

---

## What Struggled

### Model Pins Cause Repeated Billing Gate Incidents (Critical)
23+ skills hardcode `model: claude-sonnet-4-6` in frontmatter. When the session runs under Opus 4.7 1M context, the harness routes subagent invocations to Sonnet 4.6 and inherits the 1M context tier, triggering an extra-usage billing gate. The user hit this problem in two separate sessions — the fix was not applied systemically after the first incident.

**Evidence:** "Once again you invoked sonnet [after switching to Opus and requesting momentum:decision]" and "Is this a bug? I'm on opus: [Skill loaded claude-sonnet-4-6] API Error: Extra usage is required for 1M context." Two separate sessions, same root cause.
**Root cause:** Skills with hardcoded model pins inherit the context tier of the session, creating billing landmines when sessions run at 1M context. The agent also gave an incorrect diagnosis on first occurrence (claiming mid-session cache edits would fix it per-invocation), which delayed resolution and undermined trust.
**Recommendation:** FIX — remove `model:` pins from all 23+ skill frontmatter entries, or replace with a tier-relative reference that does not inherit the 1M context tier.

### Sprint-Planning Orchestrator Halts Between Steps (High)
The sprint-planning workflow repeatedly announced intent to proceed to the next step and then stopped, requiring user re-prompting. This happened at least twice and was compounded by a model-switch event causing an additional halt.

**Evidence:** "Why do you keep saying you're going to proceed but you stop" and "Are you continuing?" (after /model switch).
**Root cause:** Sprint-planning skill workflow lacks explicit continuous-execution directive. Step boundaries are treated as implicit confirmation gates. Model switches additionally reset execution state.
**Recommendation:** FIX — sprint-planning skill should declare explicit sequential execution intent in its workflow preamble. Add "proceed without user confirmation between steps" directive. Treat model switches as transparent and resume current workflow position.

### Distill Batch-Approval Not Propagated to Subagents (High)
During the triage phase, four distill subagents paused waiting for A/R/C approval that should have been autonomously granted. The triage batch-approval gate does not suppress downstream distill invocation approval gates.

**Evidence:** "Why are you asking permission for the most innane commands?" — four distill subagents paused post-batch-approval.
**Root cause:** The distill skill has a built-in approval gate that operates independently of upstream batch authorization. No mechanism exists to propagate batch approval from orchestrator to spawned subagents.
**Recommendation:** FIX — distill skill invoked from triage should inherit batch-approval context. Add `orchestrator_approved: true` flag propagation or remove the distill approval gate when invoked from a batch-approved orchestrator context.

### Parallel Distill Agents Colliding on Shared Files (High)
With ~17 distill agents running in parallel, agents targeting the same practice file (SKILL.md) encountered sequential write failures: Write without prior Read, stale read after concurrent modification, file not found. The affected agent required 46 assistant turns and 3 error recovery loops.

**Evidence:** Execution finding — agent a6cf4f4618f1b8bb3 hit three sequential file-edit errors on constitution-builder/SKILL.md.
**Root cause:** The distill orchestrator does not detect file-target collisions before spawning. Multiple agents targeting the same file path will race on reads and writes.
**Recommendation:** FIX — retro/distill orchestrator must detect file-target collisions and serialize agents targeting the same file path before spawning.

### Parallel Intake Agents Causing Git Lock Contention (High)
Multiple intake agents spawned in parallel all attempted to commit at approximately the same time, producing `fatal: Unable to create .git/index.lock: File exists` errors. Three error turns per agent were spent on lock contention recovery.

**Evidence:** Execution finding — agents a5602e2eaa3e50ec4 and ae885110d5143b628 both hit git index.lock at 2026-05-16T16:01:50.
**Root cause:** momentum-tools intake performs a git commit on each stub creation with no coordination between parallel callers.
**Recommendation:** FIX — momentum-tools intake should use a git commit retry loop or file-level lock around the commit step. Alternatively, serialize the intake wave.

### Sprint-Planning CLI: Stale Subcommand Surface (High)
The sprint-planning orchestrator emitted six distinct CLI errors: `zsh: read-only variable: status` (2x), `momentum-tools not found`, `sprint current` invalid choice, `sprint stories` missing `--priority` flag, cmux pane not found, sprint activate blocked.

**Evidence:** Execution finding — 6 distinct errors in sprint-planning orchestrator session.
**Root cause:** Sprint-planning skill workflow references stale momentum-tools subcommand names, uses `status` as a shell variable name (zsh read-only keyword collision), and assumes momentum-tools is on PATH without sourcing.
**Recommendation:** FIX — update sprint-planning skill workflow: remove `sprint current`, correct `sprint stories --priority` form, rename `status` shell variable to avoid zsh collision, add PATH sourcing before CLI calls.

### Wrong create-story Skill Invoked (Medium)
The sprint orchestrator invoked `bmad-create-story` instead of `momentum:create-story` for the beads spike story, writing output to `_bmad-output/implementation-artifacts/` instead of `.momentum/stories/`. The user caught this through inspection and manually redirected.

**Evidence:** "Can you look into this, and also figure out why we're still using _bmad? _bmad-output/implementation-artifacts/beads-dual-write-spike.md."
**Root cause:** Sprint orchestrator does not enforce skill namespace qualification. Unqualified skill names resolve to BMAD defaults in a project where both BMAD and Momentum are installed.
**Recommendation:** FIX — sprint orchestrator must use fully-qualified `momentum:create-story` — never `bmad-create-story`. Apply namespace enforcement to all Momentum skill invocations in sprint workflow files.

### AVFL Validator Receiving Truncated Story Content (Medium)
The Domain Fitness validator for story-level AVFL caught DOMAIN-002 — EDD section truncated in prompt but complete in on-disk file. The consolidator correctly identified this as a prompt artifact, but it produced a false positive that required consolidator reasoning to dismiss.

**Evidence:** Review finding — prompt-quality observation on Domain Fitness validator.
**Root cause:** Story content passed as inline prompt text can be truncated at token limits. Structural Integrity avoids this by reading files directly.
**Recommendation:** FIX — for correctness-critical validators (Domain Fitness, Structural Integrity), require validators to read story files directly rather than consume injected summaries. Reserve summary injection for holistic validators only (Coherence & Craft).

### AVFL Consolidator False Positive on File Path (Low)
The story-level AVFL consolidator dismissed STRUCTURAL-002 (wrong file path for beads spike) on grounds that "template doesn't require frontmatter for implementation artifacts." The finding was valid — stories/index.json declared `story_file: true` implying `.momentum/stories/` canonical path. The latent inconsistency was only caught at the sprint-plan AVFL level.

**Evidence:** Review finding — false-positive observation; file remained at `_bmad-output/implementation-artifacts/` post story-level AVFL.
**Root cause:** Consolidator prompt does not cross-reference stories/index.json path declarations when evaluating path-related findings.
**Recommendation:** FIX — consolidator prompt should instruct the agent to verify findings against stories/index.json before dismissing path-related findings.

### Distill Agents Lacking Write Permission for New Rule Files (Medium)
A distill agent attempting to create `.claude/rules/handoff-conventions.md` received `Permission to use Write has been denied`. The agent correctly halted and reported, but the file was not created until a subsequent session.

**Evidence:** Execution finding — agent a7857a121e5611e07 on handoff-conventions distill.
**Root cause:** Distill agents spawned for rule file creation do not have Write permission for new file creation in `.claude/rules/`.
**Recommendation:** FIX — add `.claude/rules/` to distill skill's required Write permissions documentation when the target artifact is a rules file.

### stories/index.json and architecture.md Exceeding Read Limits (Medium)
Six file-too-large errors occurred across the sprint: stories/index.json exceeded 46292 tokens (4 occurrences), architecture.md exceeded 256KB (1 occurrence), stories/index.json exceeded 49125 tokens (1 occurrence). Pattern will worsen with each sprint.

**Evidence:** Execution finding — six file-too-large errors across the sprint.
**Root cause:** stories/index.json and architecture.md have grown beyond single-read limits. No chunked read protocol exists in intake/distill agent prompts.
**Recommendation:** INVESTIGATE — evaluate whether agents need to read stories/index.json directly vs. delegating to the CLI. Add large-file read protocol to intake and distill prompts.

### Agent Self-Knowledge Gap: Subagent Context Tier Propagation (Medium)
When the user asked about subagent context tier, the agent initially mischaracterized the root cause of the extra-usage error and claimed mid-session cache edits would fix it per-invocation. User had to correct the agent's understanding.

**Evidence:** "No it was when you spawned a subagent. Can't you spawn a subagent with the standard context?"
**Root cause:** No documentation in practice rules about how the Claude Code harness propagates context tier to subagents spawned via the Agent tool. Context tier is inherited from session; model pins in skill frontmatter override model but not context tier.
**Recommendation:** FIX — add harness behavior documentation to practice rules covering subagent context-tier propagation.

### Context Length: No Proactive Handoff Offer (Low)
The agent architecture discussion grew long enough that the user requested a handoff to a new session manually. The agent did not proactively offer a handoff or signal that context was getting long.

**Evidence:** "Provide me a handoff for the triage, I'll give it to a new session."
**Root cause:** No mechanism in long-running workflow skills for the agent to monitor its own context consumption and proactively offer a handoff before the user notices degraded behavior.
**Recommendation:** FIX — add proactive handoff signal to long-running workflow skills: offer a handoff document when context approaches threshold.

---

## User Interventions

### Frustration Signals

**Approval gates in distill subagents**
User: "Why are you asking permission for the most innane commands?"
Context: Four distill subagents paused waiting for approval after the user had already given batch approval at triage. The approval was not propagated downstream. User had to manually approve four separate subagent actions.
Implication: Batch approval mechanisms must suppress downstream gates. This is a trust failure — the practice told the user approval would be batch-applied, then broke that promise four times in a row.

**Sprint-planning inter-step halts**
User: "Why do you keep saying you're going to proceed but you stop"
Context: Sprint-planning orchestrator repeatedly announced intent and halted. Happened at least twice, requiring explicit user re-prompting each time.
Implication: Workflow execution cannot be advisory. Each step boundary that requires re-prompting is a tax on developer attention and erodes confidence in autonomous execution.

**Model switch post-halt**
User: "Are you continuing?"
Context: After issuing `/model` to switch models, the agent stopped executing mid-workflow. User had to re-prompt to resume.
Implication: Model switches should be transparent — the agent should resume its workflow position without requiring user re-confirmation.

### Corrections

**Sonnet billing gate — first occurrence**
User: "Is this a bug? I'm on opus: [Skill loaded claude-sonnet-4-6] API Error: Extra usage is required for 1M context"
Context: User was under Opus 4.7 1M context. momentum:decision hardcodes Sonnet 4.6, inheriting the 1M context tier. The agent gave an incorrect explanation (claiming mid-session cache edits would fix it). User had to manually switch session model.
Implication: Incorrect diagnosis delayed resolution. The systemic fix (all 23 skills) was not applied — only the immediate session was worked around.

**Sonnet billing gate — second occurrence**
User: "So I'm running into the problem now where sonnet 4.6 has an upper and lower context version, and the 1m context I cannot use. Can you set that in the agent file?"
Context: Same issue resurfaced in sprint-planning in a separate session. The first-session workaround had not addressed the systemic problem.
Implication: Treating symptoms without fixing the system causes the same user frustration on a second occurrence, with compounded trust damage.

**Wrong create-story skill**
User: "Can you look into this, and also figure out why we're still using _bmad? _bmad-output/implementation-artifacts/beads-dual-write-spike.md"
Context: Sprint orchestrator invoked bmad-create-story instead of momentum:create-story, writing to the wrong path. User caught this through inspection.
Implication: Skill namespace enforcement must be explicit in the orchestrator. Silent fallback to BMAD defaults is unacceptable in Momentum project context.

**Wrong session context (nornspun vs momentum)**
User: "Wait what is all this? That's not momentum it's nornspun. Wait are we not in the momentum project? Ah crap that was an accident."
Context: User was running 3-4 parallel sessions and queried sprint state in the wrong session. The agent began answering about nornspun sprint state rather than asking for clarification.
Implication: Agents should orient more explicitly about their project context when answering sprint-state queries, especially in multi-session environments.

**Fixer role architecture**
User: "And fixer isn't a dev necessarily. It might be fixing documents or anything else. Couldn't we use standard agents, dev or otherwise, and lobotomize it?"
Context: The agent proposed a "fixer" as a distinct agent role. User corrected that fixer is a mode applied to the role that owns the document.
Implication: Agent taxonomy design should avoid proliferating roles when mode variations (lobotomized base agent) suffice.

**Subagent context tier understanding**
User: "No it was when you spawned a subagent. Can't you spawn a subagent with the standard context?"
Context: Agent mischaracterized root cause of extra-usage error. User had to correct the agent's model of how the harness propagates context tier.
Implication: Gap in agent self-knowledge about harness behavior. The agent should know that context tier is inherited from session and not overrideable per-spawn.

### Redirections

**BMAD intent engineering injection mid-sprint-planning**
User: "Before we go too far, I'd like you to read up on the bmad agents and see how their Intent Engineering works for those agents"
Context: User paused sprint-planning to inject a research task before story approval. Led to the full agent taxonomy audit (DEC-020 through DEC-027).
Implication: Sprint-planning does not have a natural hook for exploratory refinement before story commitment. User had to manually pause and redirect. Consider adding an explicit "architecture review" gate before story approval.

### High-Value Developer Decisions (Not Fixable — Require Developer Judgment)

**Skill-creator integration architecture**
User: "So imagine we use skill-creator for BOTH skills and agents... momentum:create-story knows how to build out an agent or skill spec to use the skill-creator. But one question is still how do we get skill-creator to use our constitution?"
Context: User exercised high-level architectural judgment about how skill-creator and momentum:create-story should interface. Led to DEC-027.
Implication: This category of decision required developer domain knowledge about the constitution-builder tier model. Agents could not have reached this conclusion autonomously.

**Agent taxonomy audit commission**
User: "I need a complete review... Do all our Decision documents reflect this? And B -> Do all our Agent stories... And C -> Do we need all these stories?... I need this Audit to be EXHAUSTIVE"
Context: User identified on their own that the agent taxonomy had become incoherent and commissioned a full audit. Produced DEC-020 through DEC-027.
Implication: The agent ecosystem had grown without sufficient cross-cutting coherence review. This had to be caught by the developer, not surfaced by a practice mechanism.

---

## Story-by-Story Analysis

### beads-dual-write-spike
Most scrutinized story of the sprint. Wrong skill invoked (bmad-create-story), written to wrong path (_bmad-output/implementation-artifacts/), then moved post-correction. Story-level AVFL produced five real catches: STRUCTURAL-001 (missing frontmatter), STRUCTURAL-002 (wrong path — partially dismissed by consolidator as false positive, caught at sprint-plan AVFL), STRUCTURAL-005 (missing `--claim` flag in AC 4 and Task 3), STRUCTURAL-004 (AC 10 without owning task), DOMAIN-003 (incorrect commit type). Final AVFL score: 74/100 (CHECKPOINT_WARNING). All catches fixed pre-sprint.

**Iteration count:** 3 passes (intake → flesh-out → move correction + wrong-skill correction)
**Notable:** The consolidator false-positive on STRUCTURAL-002 left the path inconsistency unresolved until sprint-plan AVFL — illustrating the value of layered review.

### analyst-base-body and researcher-base-body
Both stories required a 3-pass pattern: intake → flesh-out → revision pass to apply constitution.md fix (replacing project-context.md references throughout Dev Notes and ACs). The correction was real and necessary (DEC-026 D4 update), but the flesh-out story prompt was unaware of the current constitution.md path at time of spawning.

**Iteration count:** 3 passes each
**Root cause:** create-story/flesh-out prompts did not inject the latest constitution.md path. A cross-cutting correction was discovered post-flesh-out, requiring a downstream revision wave across both stories.
**Fix needed:** flesh-out prompts should explicitly inject constitution.md path to prevent downstream revision waves.

### routing-table-schema-and-implementation
Dependency graph error caught by AVFL: declared `depends_on: []` in stories/index.json but story file declared `depends_on: [agent-builder-skill]`. Would have caused wave ordering failure. Fixed pre-activation (commit be082cd).

**Iteration count:** 1 pass + AVFL fix
**Notable:** Sprint-blocking catch. AVFL was directly responsible for preventing wave ordering failure.

### agent-builder-skill
Placed in Wave 2 despite `depends_on: []`. Both Domain Fitness and Coherence & Craft independently caught this. Fixed: moved to Wave 1, routing-table moved to Wave 2, Wave 3 eliminated (commit 0762d65).

**Iteration count:** 1 pass + AVFL wave reorganization
**Notable:** Removing Wave 3 was an efficiency gain — one unnecessary serial boundary eliminated.

### missing-base-bodies-audit
`change_type` absent from story file. Caught by AVFL, fixed pre-activation. Role routing for this story was incorrect until the fix was applied.

**Iteration count:** 1 pass + AVFL fix

### ux-base-body
Blocked sprint activation: sprint activate was blocked pending ux-base-body approval. Reveals a sequencing issue in the sprint-planning workflow — activation should not proceed until all stories have explicit approval status.

**Iteration count:** 1 pass + activation unblock

---

## Cross-Cutting Patterns

### Pattern 1: Systemic Fix Not Applied After First Incident
The Sonnet model-pin billing issue appeared in two separate sessions. After the first incident, only the immediate manifestation was addressed (one session workaround), not the systemic root cause (23 skills with hardcoded model pins). The user hit the same wall a second time with compounded frustration.

**Affected auditors:** Human (2 high-severity findings).
**Principle:** When a finding reveals a systemic issue, the fix story must enumerate and address the full population of affected artifacts, not just the instance that surfaced.

### Pattern 2: Approval Gate Propagation Failure
Upstream batch approval (triage) does not suppress downstream subagent approval gates (distill). The user granted permission once and expected it to hold. Four subagents asked again independently. This is the same structural gap at two levels: orchestrator authorization does not propagate to spawned subagents.

**Affected auditors:** Human (frustration finding — high severity).
**Principle:** Authorization granted at the orchestrator level must propagate explicitly to all spawned subagents in the same workflow.

### Pattern 3: Parallel Agent File Collisions
Two distinct collision types occurred: parallel intake agents colliding on git index.lock, and parallel distill agents colliding on the same target file (SKILL.md). Both are consequences of fan-out spawning without collision detection. The pattern will recur and worsen with scale.

**Affected auditors:** Execution (2 error-pattern findings).
**Principle:** Fan-out spawning orchestrators must detect shared-resource collisions (same file path, git commit) and serialize conflicting agents before spawning.

### Pattern 4: Stale CLI Surface in Workflow Skills
Sprint-planning skill workflow references stale momentum-tools subcommands, uses a zsh read-only keyword as a shell variable name, and assumes momentum-tools on PATH without sourcing. Six distinct errors from this single root cause. This is a maintenance discipline failure: skill workflows must be updated and tested against the actual CLI surface after any momentum-tools change.

**Affected auditors:** Execution (1 finding with 6 sub-errors).
**Principle:** Any skill that shells out to a CLI tool owns the obligation to keep its subcommand references current with that CLI.

### Pattern 5: AVFL Efficiency Asymmetry — Pre-Injected vs. Direct File Reads
Coherence & Craft (pre-injected content): 1 turn, 0 tool calls. Structural Integrity (file reads): 57 turns, 55 tool calls. Domain Fitness: 64 turns, 62 tool calls. ~176 tool calls across two validators reading the same files. However, pre-injected content can be truncated, producing false positives (DOMAIN-002 on beads spike). The right design: pre-inject for holistic validators, direct reads for correctness validators.

**Affected auditors:** Execution (efficiency finding), Review (prompt-quality finding).
**Principle:** Validator prompt strategy should be matched to validator type — holistic validators benefit from pre-injection efficiency; correctness validators require file-read evidentiary grounding.

### Pattern 6: Skill Namespace Enforcement Failures
The sprint orchestrator invoked `bmad-create-story` instead of `momentum:create-story`, and invoked bare `avfl` instead of `momentum:avfl`. Both are namespace enforcement failures in a project where BMAD and Momentum coexist. Unqualified skill names resolve to BMAD defaults.

**Affected auditors:** Human (wrong-skill finding), Execution (avfl namespace error).
**Principle:** In Momentum project context, all skill invocations in orchestrator workflow files must use fully-qualified `momentum:` namespace. No bare skill names.

### Pattern 7: Agent Taxonomy Coherence as Developer Responsibility
The agent taxonomy audit (DEC-020 through DEC-027) was commissioned by the developer after they noticed incoherence independently. Eight decisions emerged from a single developer-initiated audit. The practice had no mechanism to surface this need proactively. The developer caught systemic drift that no practice gate flagged.

**Affected auditors:** Human (investigation finding).
**Principle:** The practice should include a periodic coherence check for the agent taxonomy — either at Impetus session-start orientation or as part of epic grooming.

---

## Metrics

| Metric | Value |
|--------|-------|
| User messages analyzed | 98 |
| Subagents analyzed | 70 |
| Tool errors detected | 41 |
| Struggles identified | 13 |
| Successes identified | 6 |
| User interventions | 22 |
| Cross-cutting patterns | 7 |
| Sprint-blocking AVFL catches | 2 |
| Distinct error types in execution | 6 |
| Stories requiring revision passes | 3 |
| Decisions produced (DEC-020–027) | 8 |

---

## Priority Action Items

### Critical

**1. Remove hardcoded model pins from 23+ skill frontmatter**
Two billing gate incidents in two separate sessions. Systemic issue. Every skill with `model: claude-sonnet-4-6` is a billing landmine for 1M Opus sessions. Fix must enumerate and address all affected skills, not just the instance that surfaced.
Priority: Critical
Story stub: "Remove hardcoded Sonnet model pins from all skill frontmatter — replace with session-relative routing"

**2. Serialize distill agents targeting the same file path**
Parallel distill agents on shared files cause 3-error recovery loops and 46-turn remediation. Pattern recurs at scale every sprint with more distill agents.
Priority: Critical
Story stub: "Detect and serialize distill agent file-path collisions in retro/triage orchestrator before spawning"

### High

**3. Propagate batch-approval context from triage to distill subagents**
Four distill subagents paused on approval after batch approval was granted upstream. Trust model broken. The practice promised batch approval; four subagents broke that promise.
Priority: High
Story stub: "Propagate batch-approval context from triage orchestrator to distill subagents"

**4. Eliminate sprint-planning inter-step pause gates**
Orchestrator announced intent and halted at least twice. Workflow execution fidelity failure. Model switches additionally reset execution state.
Priority: High
Story stub: "Sprint-planning: enforce continuous sequential execution without inter-step confirmation gates"

**5. Fix sprint-planning CLI subcommand surface**
Six distinct CLI errors from stale subcommands, zsh read-only variable collision, missing PATH sourcing.
Priority: High
Story stub: "Update sprint-planning workflow: correct momentum-tools CLI surface, fix zsh variable collision, add PATH sourcing"

**6. Add git commit retry/lock to momentum-tools intake**
Parallel intake agents cause git index.lock contention. Three error turns per agent.
Priority: High
Story stub: "Add git commit retry loop to momentum-tools intake for parallel-safe stub creation"

**7. Enforce fully-qualified Momentum skill namespaces in sprint orchestrator**
Sprint orchestrator silently used bmad-create-story and bare avfl instead of momentum-namespaced equivalents. User caught the wrong-skill issue through inspection.
Priority: High
Story stub: "Enforce fully-qualified momentum: skill namespaces in sprint-planning orchestrator workflow"

### Medium

**8. Standardize AVFL validator prompt strategy by validator type**
~176 unnecessary tool calls per sprint-plan AVFL run from symmetric file-read approach. Pre-inject for holistic validators; direct reads for correctness validators.
Priority: Medium
Story stub: "Standardize AVFL validator prompt strategy: pre-inject for holistic, direct file reads for correctness validators"

**9. Fix AVFL consolidator to cross-reference path findings against stories/index.json**
Consolidator dismissed a valid path finding without checking stories/index.json declaration. Latent inconsistency persisted until sprint-plan AVFL caught it.
Priority: Medium
Story stub: "AVFL consolidator: cross-reference path findings against stories/index.json before dismissal"

**10. Inject constitution.md path into create-story flesh-out prompts**
Two stories required a third revision pass to apply constitution.md terminology fix. Flesh-out prompt lacked the current constitution.md path at spawn time.
Priority: Medium
Story stub: "Inject current constitution.md path into create-story flesh-out prompts to eliminate downstream revision waves"

**11. Add .claude/rules/ write permission to distill agents for rule file creation**
Distill agent blocked on new rule file creation. File not created until subsequent session.
Priority: Medium
Story stub: "Add .claude/rules/ write permission to distill skill invocation for rule file targets"

**12. Document subagent context-tier propagation in practice rules**
Agent gave incorrect explanation of context-tier propagation. User had to correct. Gap in agent self-knowledge about harness behavior.
Priority: Medium
Story stub: "Add subagent context-tier propagation behavior to practice rules documentation"

**13. Investigate large-file read protocol for stories/index.json and architecture.md**
Six file-too-large errors across the sprint. Pattern will worsen with each sprint as both files grow.
Priority: Medium
Story stub: "Investigate large-file read protocol for stories/index.json and architecture.md — evaluate CLI delegation vs chunked read"

### Low

**14. Add proactive handoff offer to long-running workflow skills**
Developer requested handoff manually after context grew long. Agent had no proactive signal.
Priority: Low
Story stub: "Add proactive handoff offer to long-running workflow skills at context consumption threshold"

**15. Add agent taxonomy coherence check to Impetus or epic grooming**
Developer discovered incoherent agent taxonomy independently. Practice had no proactive surface for this need.
Priority: Low
Story stub: "Add periodic agent taxonomy coherence check to Impetus session orientation or epic grooming"
