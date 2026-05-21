# Sprint Transcript Audit — sprint-2026-05-17

**Retro date:** 2026-05-20
**Sprint completed:** 2026-05-19
**Data analyzed:** 213 user messages | 115 subagents | 102 errors | 11 team messages

---

## Executive Summary

Sprint-2026-05-17 delivered significant architectural work — the agent taxonomy, routing table, build pipeline, and E2E validation redesign — but the sprint itself was marked by a high volume of developer interventions and agent failures that reveal systemic practice gaps. The developer was effectively co-piloting the sprint rather than verifying it: catching skipped process gates, correcting over-applied validation methods, redesigning architectural concepts mid-flight, and repeatedly prompting for closure steps the practice should have driven autonomously.

Three themes dominate. First, **visibility and human-legibility**: agents ran silently for extended periods, produced gate artifacts written for LLM consumption, and never emitted a clear "done" signal. The developer had to ask "are you still running?" and "are we done?" multiple times. Second, **process gate bypass**: required steps (triage before sprint-planning, dedup/consolidation, hook validation, the agent-builder approval gate) were skipped without any quality gate catching the omission. Third, **infrastructure fragility**: 4 intake agents failed instantly on billing gates, 2 agents were lost to socket aborts and had to retry, the Gemini browser driver spent 119 turns producing zero output, and permission propagation races blocked 5 dev agents simultaneously.

Priority actions center on: making sprint-dev emit real-time heartbeat signals, enforcing human-legibility for all gate/decision artifacts, building triage-before-planning enforcement, fixing the E2E validator's hardcoded service-stack assumptions so it produces actual signal, and addressing the socket-abort retry gap that wasted entire agent sessions. The sprint's successes — fan-out pattern used correctly, clean triage→create-story pipeline when properly sequenced, QA reviewer with explicit path lists producing actionable AC-by-AC findings — point to what the practice looks like when it works.

---

## What Worked Well

### Fan-Out Pattern Applied Correctly
AVFL validators and review agents used independent fan-out spawning with no inter-agent communication, matching the pattern decision rule exactly. Team messages (11 entries) contained zero SendMessage inter-agent communication — all entries were independent outputs returned to orchestrator. No TeamCreate overhead was incurred.
**Evidence:** Execution audit: "Team messages (11 entries) contain no SendMessage inter-agent communication. All entries are independent agent outputs returned to orchestrator."
**Recommendation:** KEEP

### QA Reviewer Prompt Design Produced Actionable Findings
When the QA reviewer prompt provided all 7 story file paths explicitly with canonical paths and clear AC-by-AC verification instruction, the agent produced a complete AC-by-AC table with VERIFIED/PARTIAL/MISSING status and file evidence. Explicit path lists prevented path guessing and produced findings with citation quality.
**Evidence:** Review audit: "Agent produced complete AC-by-AC table with VERIFIED/PARTIAL/MISSING status and file evidence."
**Recommendation:** KEEP

### Triage→Create-Story Pipeline When Properly Sequenced
When the triage→create-story pipeline ran with proper dedup and consolidation, the developer responded with "Perfect, Go!" — immediate unqualified approval. The pipeline itself is sound; the failures occurred when sequencing gates were bypassed.
**Evidence:** Human audit: "Perfect, Go!" after the create-story + triage sequence completed cleanly.
**Recommendation:** KEEP

### AVFL Multi-Lens Independent Re-Reading Is Correct By Design
Two AVFL validators at ~0.98 tool/turn ratio independently re-reading every story file and referenced artifact is expected behavior — each lens must independently verify without sharing state. High churn is intrinsic to the multi-lens design. Consolidator correctly ran single-turn.
**Evidence:** Execution audit: "Expected AVFL behavior — independent validators re-read same files. High churn is intrinsic to multi-lens design."
**Recommendation:** KEEP

### Developer Trusts Direct Discovery Over Spike Scaffolding
For lightweight internal research the developer explicitly streamlined: "Just do it now. We don't need a spike story for internal discovery." Demonstrates appropriate process calibration where overhead is proportional to uncertainty.
**Evidence:** Human audit: developer chose direct discovery over formal spike story for low-stakes internal research.
**Recommendation:** KEEP

---

## What Struggled

### Sprint-Dev Emits No Progress Signals During Long Fan-Out Periods
During extended fan-out periods, sprint-dev runs silently. Developer asked "Are you using beads for the whole thing?" at ~7 minutes and "Are you still running?" at ~18 minutes — unable to distinguish working agents from stalled ones.
**Evidence:** Human audit: two status-check questions within the first 18 minutes of sprint-dev.
**Root cause:** Sprint-dev has no heartbeat output mechanism. Fan-out spawning fires agents and waits; there is no progress event emitted to the orchestrator surface between spawn and collect.
**Recommendation:** FIX — story: "sprint-dev: emit per-agent heartbeat signals during fan-out execution"

### Gate and Decision Artifacts Not Human-Readable
Two separate gate/decision presentations this sprint were flagged as incomprehensible. "Wow your Gate 2 description was not meant for human consumption at all" and "The first two paragraphs of your decision make almost no sense to me." Developer could not parse what they were being asked to decide.
**Evidence:** Human audit: two separate incidents of developer unable to parse gate/decision output.
**Root cause:** No human-legibility requirement in gate artifact templates. Agents default to LLM-optimized structured output rather than plain-language decision framing.
**Recommendation:** FIX — story: "gate/decision artifacts: enforce human-legible presentation format"

### Required Process Gates Bypassed by Agents
Two sequential gates skipped before sprint-planning: dedup/consolidation pass AND the triage gate. Developer had to manually enforce both: "Did you run a careful dedup and consolidation?" and "Have they been triaged? Stories are normally triaged before they go into sprint-planning."
**Evidence:** Human audit: two separate corrections in quick succession before sprint-planning could proceed.
**Root cause:** Sprint-planning skill does not assert preconditions (triage-complete state, dedup pass) before accepting story input. No structural enforcement — relies on developer memory.
**Recommendation:** FIX — story: "sprint-planning: enforce triage-complete and dedup preconditions"

### E2E Validator Hardcodes Service-Stack Assumptions
E2E validator prompt hardcodes "finch + PostgreSQL + FastAPI via cmux" service assumptions. This project is pure agent/skill/markdown changes. The validator blocks every sprint regardless of actual behavioral gaps, producing zero signal sprint-over-sprint. This is the third consecutive sprint it has blocked.
**Evidence:** Review audit: "E2E gate permanently neutralized for this project by service-stack assumptions. Zero E2E signal every sprint."
**Root cause:** E2E validator prompt written for service-oriented projects with no change_type-aware routing or practice-project variant.
**Recommendation:** FIX — story: "e2e-validator: change_type-aware routing — skip service checks for skill/agent/markdown sprints"

### Socket-Abort Retries Waste Full Agent Sessions
Two create-story agents hit network socket aborts mid-run (at 34 turns each) and were retried with identical prompts. The retry agents completed but accumulated secondary errors. No deduplication guard in the spawning layer — 34 turns of work lost per abort, plus retry overhead.
**Evidence:** Execution audit: agents a245ae299a48b1faa and a78c93be851536a09 (identical prompt), agents a7249ed63b10b9616 and acf3beaf08caea0c3 (identical prompt) — both pairs socket-abort + retry.
**Root cause:** Orchestrator has no idempotency layer. Socket abort triggers re-spawn with no awareness of prior partial work.
**Recommendation:** FIX — story: "sprint-dev: idempotent agent spawn — detect in-progress or completed tasks before re-spawning"

### Four Intake Agents Failed Instantly on Billing Gate
All 4 intake-wave agents terminated immediately with "API Error: Extra usage is required for 1M context." Parent session had 1M context enabled; billing gate fires per-subagent on first tool call.
**Evidence:** Execution audit: agents a7198753e80c4b5a7, a95799e93a5f92f9e, a9ceea504aae13077, afe1a671dbee340c5 — all failed on first tool call.
**Root cause:** Subagents inherit context tier from parent session but billing gate re-fires per subagent. No pre-flight context-tier check before spawning intake waves.
**Recommendation:** FIX — story: "sprint-dev: pre-flight context tier validation before spawning subagents"

### Gemini Browser Driver Looped 119 Turns Producing Zero Output
Gemini Deep Research browser driver agent ran 119 assistant turns, 61 tool results, 6 errors — all JS errors or "Unsupported browser subcommand: status" — then self-terminated with "aborted: superseded by chrome driver." Zero useful output.
**Evidence:** Execution audit: agent-aee9f4bc299a32360 — 119 turns, complete failure.
**Root cause:** cmux browser surface had broken JavaScript environment. Agent had no circuit-breaker after repeated identical errors.
**Recommendation:** FIX — story: "browser-driver agents: implement error-count circuit breaker to abort after N consecutive identical failures"

### Permission Propagation Race Blocked 5 Dev Agents Simultaneously
All 5 dev-skills agents hit "Permission to use Skill has been denied" and "Permission to use Edit/Write has been denied" within a 90-second window. All ultimately completed, but had to retry after the race cleared.
**Evidence:** Execution audit: 5 agents in sprint-2026-05-16 wave blocked simultaneously, all recovered.
**Root cause:** Worktree subagents spawn faster than harness propagates permissions from parent session.
**Recommendation:** FIX — story: "worktree agent spawn: add permission propagation readiness check before tool use"

### Architect-Guard Role Missing from agents.json Defaults
"Role architect-guard not found in defaults block" error. The routing-table story was just implemented but architect-guard was not included in the generated agents.json defaults block.
**Evidence:** Execution audit: agent-a7067cec7dda42191 — role lookup error, recovered by reading file directly.
**Root cause:** routing-table-schema-and-implementation story spec did not enumerate architect-guard as a required default role.
**Recommendation:** FIX — addressed by QA CRITICAL finding — include in next agent-related story's AC

### Sprint Closure Checklist Not Driven Autonomously
Developer had to prompt four separate closure steps: "Shouldn't it be merged and deleted?" / "Did you also clean up remote branches?" / "Did you push main?" / "Did you push it?" Sprint closure was not proceeding autonomously through its full checklist.
**Evidence:** Human audit: four follow-up prompts for steps that should have been autonomous.
**Root cause:** Sprint closure in sprint-manager does not drive a complete checklist to completion. Each step waits for human trigger.
**Recommendation:** FIX — story: "sprint-manager: autonomous sprint closure checklist execution"

### Plugin Version Bump Not Firing at Sprint Close
Developer had to ask: "Does momentum have a skill or rules for versioning the plugin?" The version-on-release rule exists in .claude/rules but sprint closure was not consulting it.
**Evidence:** Human audit: developer prompted for version bump that should be automatic.
**Root cause:** Sprint-manager sprint closure does not include a version-on-release rule check as a mandatory closure step.
**Recommendation:** FIX — story: "sprint-manager: enforce version-on-release rule as mandatory sprint closure step"

### Gherkin Over-Applied as Universal Validation Method
Developer caught Gherkin being applied indiscriminately and pushed back: "Should it be a Gherkin spec though? Is that true across all our stories? How about you look through a few dozen stories and make sure they are all easily verified E2E using Gherkin." AVFL and sprint-dev were not surfacing the mismatch between story type and validation method.
**Evidence:** Human audit: developer-initiated correction mid-sprint.
**Root cause:** No story-type-to-validation-method mapping in sprint-dev or AVFL. Default to Gherkin without checking applicability.
**Recommendation:** FIX — story: "sprint-dev/AVFL: story-type-aware validation method selection"

### Process-Document Anti-Pattern Recurred
Developer had to intervene to prevent creation of an inert "process document" artifact: "if it's a process for momentum alone shouldn't it be a rule? And if it's something that's a process for me in general shouldn't it be a rule or skill." Agent defaulted to documentation over enforcement — a documented recurring pattern.
**Evidence:** Human audit: developer manual correction. Memory also has feedback_process_as_enforced_rule.md documenting prior occurrence.
**Root cause:** No quality gate checks whether a proposed artifact is a process doc that should be a rule instead. Recurring despite memory entry.
**Recommendation:** FIX — story: "add process-doc anti-pattern check to AVFL structural lens"

### Context Exhaustion Requiring Mid-Triage Model Switch
Developer hit context limits mid-triage and had to manually orchestrate a model switch + handoff: "Can you change the triage to opus and then give me a handoff and we can run this in a new session." Context-window management is not built into triage or retro workflows.
**Evidence:** Human audit: developer-driven workaround, not workflow-driven.
**Root cause:** Long triage/retro workflows have no context-window monitoring or automatic handoff generation before exhaustion.
**Recommendation:** FIX — story: "triage/retro: context-window monitoring with proactive handoff before exhaustion"

### Hook Deployed With Invalid CLI Flag
"startup hook error — Failed with non-blocking status code: Error: unknown flag: --no-git-ops" — a hook was deployed with an invalid flag. Hook validation is not part of the practice pipeline.
**Evidence:** Human audit: developer discovered the error; execution audit confirms hook spec issue.
**Root cause:** Story completion and AVFL did not include hook smoke-test (run hook with --help or dry-run to verify flag validity).
**Recommendation:** FIX — story: "story DoD: add hook smoke-test to acceptance criteria for any story deploying hooks"

### Sprint Completion State Not Clearly Signaled
Developer asked "Are we done?" twice within ~1 minute near sprint close. Workflow completion state is not definitively communicated.
**Evidence:** Human audit: repeated "are we done?" signals within one minute.
**Root cause:** Sprint closure emits no definitive terminal signal. Developer cannot tell when the orchestrator has finished its final step.
**Recommendation:** FIX — consolidate with sprint-manager autonomous closure checklist story

### Agent-Builder Approval Gate Missing from Workflow
QA reviewer found that AC5 (developer approval gate A/R/X) is entirely absent from agent-builder-skill workflow.md. Phase 4 writes the composed file and routing entry unconditionally — agents can be written and registered without developer review.
**Evidence:** Review audit: CRITICAL finding — sprint execution defect, DoD item not implemented.
**Root cause:** Story spec for agent-builder did not carry AC5 through to workflow implementation. AVFL did not catch the omission.
**Recommendation:** FIX — carry-forward story: "agent-builder: implement developer approval gate before writing composed agent file"

### agents.json Defaults Block Missing 3 Required Roles
QA reviewer found CRITICAL: agents.json defaults block missing 3 of 9 required roles (architect, pm, sm). Any call to agent-resolve for these roles returns an error.
**Evidence:** Review audit: CRITICAL — sprint-blocking runtime failure for downstream workflows.
**Root cause:** Story spec enumerated required roles but implementation did not include all three in the defaults block.
**Recommendation:** FIX — immediate carry-forward story: "agents.json: add missing architect, pm, sm roles to defaults block"

### CREED Blocks and Eval Files Absent for Three Agent Roles
CREED blocks absent from analyst.md and researcher.md. Zero eval files for ux, analyst, or researcher base bodies despite story requirements.
**Evidence:** Review audit: HIGH — behavioral identity mechanism unimplemented, no regression protection.
**Root cause:** Story acceptance criteria included evals but implementation skipped them. No AC-completeness enforcement in AVFL.
**Recommendation:** FIX — carry-forward story: "analyst/researcher/ux agents: add CREED blocks and behavioral eval files"

### Output Envelope Mismatch Between UX Base Body and Story Spec
ux-base-body output format uses UX_OUTPUT_START envelope but story spec requires AGENT_OUTPUT_START envelope. Downstream sprint orchestrators will encounter divergent output parsing.
**Evidence:** Review audit: MEDIUM — cross-story integration failure not caught during story-level AVFL.
**Root cause:** Story spec and base-body template used different envelope constants. No cross-story integration check in AVFL.
**Recommendation:** FIX — carry-forward story: "ux-base-body: correct output envelope to AGENT_OUTPUT_START"

### Analyst Agent Has Write Access Prohibited by Role Contract
analyst.md tools list includes Write and Edit. AC2 requires read-only tools only. Also ToolSearch is absent from the tools list.
**Evidence:** Review audit: MEDIUM — violates principle of least privilege.
**Root cause:** Base-body template populated without checking role-contract tool restrictions.
**Recommendation:** FIX — carry-forward story: "analyst-base-body: enforce read-only tool contract, add ToolSearch"

### Research Session Terminated Without Recovery Path
A heavy research session terminated unexpectedly: "I have no idea why but a prior research session shut down. Can you see where it was in the research of hermes and continue where it left off?" No crash-recovery or session-resume protocol exists.
**Evidence:** Human audit: developer had to manually request resume from unknown state.
**Root cause:** momentum:research has no checkpoint/resume mechanism. Session state is not persisted.
**Recommendation:** FIX — story: "momentum:research: session checkpoint and resume protocol"

### Research Scope Narrower Than Developer Intended
After extensive Hermes research, developer found the conclusion under-explored: "Have you looked at all at Hermes plans? I was talking about replacing our current state and dispatch model, not necessarily integrating hermes into beads." Scope alignment was insufficient at research start.
**Evidence:** Human audit: developer had to re-frame after research completed.
**Root cause:** Research kickoff does not include explicit scope-alignment confirmation before launching parallel research agents.
**Recommendation:** INVESTIGATE — story: "momentum:research: explicit scope and framing confirmation before spawning research wave"

### Dispatcher Architecture Diverged From Developer Mental Model
Developer discovered mid-sprint the proposed dispatcher model contradicted their design intent: "Wait so the agent is doing work? I thought the dispatcher just called a claude session and the claude session did work? This is very different from what I imagined." Extended research and decision work proceeded without validating alignment.
**Evidence:** Human audit: high-severity correction after significant investment.
**Root cause:** No comprehension gate between research/design and developer ratification. Decision artifacts assumed rather than validated the developer's mental model.
**Recommendation:** FIX — story: "momentum:decision: add comprehension-alignment check before presenting ratification"

### Licensing/Cost Implications Not Surfaced by Practice
Developer had to ask proactively: "Do we know for certain all these things are covered by my max license?" Practice proposes integrations (beads, channels, SDK dispatcher) without surfacing licensing/cost implications.
**Evidence:** Human audit: MEDIUM — developer uncertainty discovered late.
**Root cause:** No cost/licensing review step in research or decision workflows.
**Recommendation:** FIX — story: "research/decision workflow: add cost-and-licensing surface step for proposed integrations"

### AVFL Consolidator Dismissed a Valid Structural Finding
AVFL consolidator dismissed STRUCTURAL-002 for beads-dual-write-spike (wrong file path), but the finding was accurate — the story still lives at _bmad-output/implementation-artifacts/ rather than .momentum/stories/.
**Evidence:** Review audit: false-positive dismissal, file path discrepancy remains.
**Root cause:** Consolidator threshold too aggressive; dismissed findings without verifying the underlying file-path claim.
**Recommendation:** FIX — story: "AVFL consolidator: require file-existence check before dismissing structural path findings"

### E2E Validation Strategy Designed Ad Hoc Mid-Sprint
Sprint started without E2E strategy decided. Developer articulated the complete three-tier validation pipeline (story-level code review → post-merge AVFL → sprint-level E2E) in real-time during sprint execution.
**Evidence:** Human audit: "QA/Code Review should happen at the story level PRIOR to merging. an AVFL happens AFTER the merge on the corpus... And lastly we run the E2E."
**Root cause:** Sprint-planning did not require E2E strategy to be defined before sprint start. DEC-029 was decided this sprint as a result.
**Recommendation:** INVESTIGATE — DEC-029 already captured; ensure sprint-planning enforces E2E strategy as a precondition

### AVFL Skip Not Logged When Developer Redirects
Developer said "Don't bother this time" to skip an AVFL post-merge step. The ability to skip silently without logging the skip is a practice gap — no record of what was skipped or why.
**Evidence:** Human audit: developer mid-workflow triage of validation step value.
**Root cause:** No skip-logging mechanism in AVFL. Skips are invisible to future sprint audits.
**Recommendation:** INVESTIGATE — story: "AVFL: log developer-directed skips with reason to sprint audit trail"

---

## User Interventions

All developer corrections, redirections, and frustration signals catalogued in order of severity and theme.

### High-Severity Interventions

| Type | Quote | Implication |
|------|-------|-------------|
| Correction | "Did you run a careful dedup and consolidation?" + "Have they been triaged? Stories are normally triaged before they go into sprint-planning" | Two required preconditions bypassed; developer enforcing process manually |
| Correction | "I want to minimize or even eliminate all human in the loop until verification time. That's largely the point of this exercise." | Agent introducing unnecessary checkpoints; developer restating core design goal |
| Correction | "Should it be a Gherkin spec though? Is that true across all our stories?" | Gherkin over-applied; developer caught assumption before it propagated |
| Correction | "But momentum IS the process...if it's a process for momentum alone shouldn't it be a rule?" | Process-doc anti-pattern recurred; agent defaulting to docs over enforcement |
| Correction | "Wait so the agent is doing work? I thought the dispatcher just called a claude session..." | Architectural mental model misalignment discovered after significant investment |
| Correction | "QA/Code Review should happen at the story level PRIOR to merging. an AVFL happens AFTER..." | Developer designed three-tier validation pipeline ad hoc mid-sprint |
| Frustration | "Uhg this hurts. Can you change the triage to opus and then give me a handoff and we can run this in a new session" | Context exhaustion mid-workflow; manual model switch required |
| Frustration | "I don't see a question for Gate 1? ...Wow your Gate 2 description was not meant for human consumption at all." | Gate artifacts unreadable; developer cannot parse what they are deciding |
| Frustration | "What is intake-queue.jsonl? where does that come from? ...The first two paragraphs of your decision make almost no sense to me." | Second gate/decision artifact flagged as incomprehensible this sprint |
| Frustration | "Are you using beads for the whole thing?" (7 min) / "Are you still running?" (18 min) | No visibility into agent progress during fan-out; silent execution |

### Medium-Severity Interventions

| Type | Quote | Implication |
|------|-------|-------------|
| Frustration | "Are we done?" (twice within ~1 minute) | No definitive sprint-closed signal emitted |
| Correction | "Shouldn't it be merged and deleted?" / "Did you also clean up remote branches?" / "Did you push main?" / "Did you push it?" | Four prompted closure steps that should be autonomous |
| Correction | "Does momentum have a skill or rules for versioning the plugin?" | Version bump not firing automatically at sprint close |
| Correction | "What the heck is this? startup hook error — Failed with non-blocking status code: Error: unknown flag: --no-git-ops" | Hook deployed with invalid flag; no smoke-test in pipeline |
| Correction | "Why do I have multiple panes on the right with one surface each? ...make certain that is a memory and we have a mandatory rule that states this?" | cmux layout rule violated; viewer panes accumulating |
| Redirection | "Don't bother this time." (AVFL post-merge step) | Developer skipping step; value unclear or timing friction; skip not logged |
| Frustration | "I have no idea why but a prior research session shut down." | Session crash with no recovery path |
| Frustration | "Is there nothing else to say about it?" / "I was talking about replacing our current state and dispatch model, not necessarily integrating hermes into beads" | Research scope narrower than intended; framing not aligned at start |
| Frustration | "Do we know for certain all these things are covered by my max license?" | Cost/licensing not surfaced proactively |

### Low-Severity Interventions

| Type | Quote | Implication |
|------|-------|-------------|
| Correction | "harness.json isn't named in such a way that makes me think e2e validation...Shouldn't it be called verification-harness?" | Artifact naming decisions made silently; no naming review gate |

---

## Story-by-Story Analysis

### create-story for method-selection-step
Two agents given identical prompts. First aborted at 34 turns (socket close). Second ran 71 turns to completion. Story produced once — second was a retry. ~34 turns of work wasted per socket abort. No deduplication guard.

### create-story for harness schema + plugin defaults
Same socket-abort retry pattern. First agent: 34 turns, socket abort. Second agent: 93 turns, completed with 5 errors — wrong create-story path (probed 3x), index.json schema mismatch. Path lookup in the agent prompt pointed to wrong plugin version path.

### beads-dual-write-spike
Dev agent: 109 assistant turns, 69 tool results, 7 errors — highest error count in the sprint. Errors include file-not-found, permissions denied, "fatal: pathspec AGENTS.md did not match any files." Git staging errors indicate file created at wrong location. Touched files outside standard patterns requiring pre-authorization.

### routing-table-schema-and-implementation
architect-guard role omitted from generated agents.json defaults block. Agent recovered by reading file directly. QA later surfaced 3 additional missing roles (architect, pm, sm). Carry-forward required.

### agent-builder-skill
AC5 (developer approval gate) entirely absent from workflow.md. Phase 4 writes and registers agent unconditionally. Not caught by story-level AVFL. Carry-forward required.

### analyst / researcher / ux base bodies
CREED blocks absent from analyst.md and researcher.md. Zero eval files for all three despite story requirements. analyst.md tools list includes Write/Edit in violation of read-only role contract. ux-base-body uses wrong output envelope constant. Three carry-forward stories required.

### Intake wave (4 agents)
All 4 terminated immediately on first tool call: "API Error: Extra usage is required for 1M context." Zero useful work. Entire intake wave failed. Context tier inherited from parent session but per-subagent billing gate fired.

### Gemini Deep Research browser driver
119 assistant turns, 61 tool results, 6 errors, zero useful output. Repeated JS environment failures, no circuit breaker. Another agent (chrome driver) superseded it — correct outcome but after massive wasted compute.

### Sprint closure
"No active sprint to complete" error. Adjacent Python AttributeError/KeyError from schema mismatch cascaded into orchestrator confusion. Sprint not in 'active' state when closure ran.

---

## Cross-Cutting Patterns

### Pattern 1: Human-Legibility Gap in All Artifacts Surfaced to Developer
Gate 1 missing from presentation. Gate 2 "not meant for human consumption." Decision document "makes almost no sense." This pattern cuts across human audit (multiple incidents), the gate template design, and the decision workflow. Agents consistently produce LLM-optimized structured output rather than human-optimized decision framing. Every artifact the developer must act on needs a plain-language lead.

### Pattern 2: Process Gate Bypass Without Detection
Dedup/consolidation skipped. Triage before planning skipped. Hook smoke-test absent from DoD. Agent-builder approval gate absent from workflow. Version-on-release not consulted at close. Sprint closure checklist not driven autonomously. No quality gate caught any of these. The practice has many documented gates but no enforcement that they fired.

### Pattern 3: Silent Execution — No Heartbeat, No Terminal Signal
"Are you still running?" (18 min in). "Are we done?" (twice at close). Research session terminated without notice. Sprint-dev, research, and sprint-close all share the same pattern: they begin, they work, and the developer has no signal about state until they ask.

### Pattern 4: Infrastructure Fragility Concentrated in Subagent Lifecycle
Socket aborts (2 retries). Billing gate failures (4 agents). Permission propagation race (5 agents). Browser JS environment failure (119-turn dead agent). Sleep-block stall. Five distinct failure modes all in the subagent spawn/init lifecycle. The orchestration layer is brittle and has no resilience primitives.

### Pattern 5: Architectural Decisions Made Ad Hoc During Sprint Execution
Three-tier validation pipeline designed mid-sprint. Dispatcher model misalignment discovered mid-sprint after extended work. E2E strategy absent from sprint-planning. Fundamental practice architecture being decided in the executor role rather than the planner role.

### Pattern 6: Carry-Forward Debt from Incomplete Story Implementation
Three carry-forward stories (CREED blocks, eval files, tool contract) from analyst/researcher/ux. Two carry-forward fixes from agents.json (3 missing roles, agent-builder approval gate). Output envelope mismatch. All were undetected by story-level AVFL — caught only by post-merge QA pass. AVFL is not catching implementation completeness gaps.

### Pattern 7: Recurring Violations of Documented Rules
process-doc anti-pattern (documented in memory, recurred). cmux multi-pane accumulation (documented in rules, violated). Gherkin over-application (documented in memory, recurred). The memory/rules system exists but agents are not consulting it at the point where it would prevent the violation.

---

## Metrics

| Metric | Value |
|--------|-------|
| User messages analyzed | 213 |
| Subagents analyzed | 115 |
| Tool errors detected | 102 |
| Struggles identified | 26 |
| Successes identified | 5 |
| User interventions | 22 |
| Cross-cutting patterns | 7 |

---

## Priority Action Items

### Critical

1. **agents.json defaults block: add missing architect, pm, sm roles**
   Sprint-blocking runtime failure. Any workflow invoking agent-resolve for these roles errors immediately.
   Story stub: `fix(agents): agents.json defaults block missing 3 required roles — carry-forward`

2. **Agent-builder: implement developer approval gate (AC5)**
   Agents can be written and registered without developer review. DoD item was not implemented.
   Story stub: `fix(skills): agent-builder approval gate absent from workflow — carry-forward`

3. **E2E validator: change_type-aware routing**
   Third consecutive sprint with zero E2E signal. Gate permanently neutralized by hardcoded service-stack assumptions. No behavioral validation running at the sprint level.
   Story stub: `fix(skills): e2e-validator hardcoded service assumptions block all signal for practice projects`

### High

4. **Sprint-dev: emit per-agent heartbeat signals during fan-out execution**
   Developer blind for 18+ minutes. Systemic visibility gap across every sprint.
   Story stub: `feat(skills): sprint-dev fan-out heartbeat output`

5. **Gate/decision artifacts: enforce human-legible presentation format**
   Two incomprehensible artifacts this sprint. Developer cannot exercise judgment on decisions they cannot parse.
   Story stub: `fix(skills): gate and decision artifacts human-legibility requirement`

6. **Sprint-planning: enforce triage-complete and dedup preconditions**
   Two required gates bypassed with no detection. Developer manually enforcing sequence.
   Story stub: `fix(skills): sprint-planning precondition enforcement — triage gate and dedup pass`

7. **Subagent spawn: pre-flight context-tier validation**
   4 agents failed instantly on billing gate. Zero work produced from entire intake wave.
   Story stub: `fix(skills): subagent spawn pre-flight context tier check`

8. **Sprint-manager: autonomous sprint closure checklist**
   Four developer-prompted closure steps. Sprint state not definitively signaled.
   Story stub: `fix(skills): sprint-manager autonomous closure checklist with terminal signal`

9. **momentum:decision: add comprehension-alignment check before ratification**
   Dispatcher architectural model misalignment discovered after significant investment.
   Story stub: `fix(skills): decision ratification comprehension-alignment gate`

### Medium

10. **Sprint-dev: idempotent agent spawn — detect completed tasks before re-spawning**
    34 turns of work lost per socket abort. Two separate incidents this sprint.
    Story stub: `fix(skills): sprint-dev idempotent agent spawn with completion detection`

11. **Story DoD: hook smoke-test for hook-deploying stories**
    Hook deployed with invalid CLI flag. No validation step in pipeline.
    Story stub: `fix(rules): story DoD add hook smoke-test acceptance criterion`

12. **Sprint-manager: enforce version-on-release rule at sprint close**
    Rule exists, not consulted. Developer had to prompt version bump.
    Story stub: `fix(skills): sprint-manager version-on-release enforcement at close`

13. **momentum:research: session checkpoint and resume protocol**
    Session terminated without recovery path. Developer had to manually request resume.
    Story stub: `feat(skills): momentum:research session checkpoint and resume`

14. **AVFL structural lens: process-doc anti-pattern check**
    Recurring violation despite memory entry. No quality gate catches it.
    Story stub: `fix(skills): AVFL structural lens add process-doc anti-pattern detector`

15. **Triage/retro: context-window monitoring with proactive handoff**
    Developer hit context exhaustion mid-workflow, had to manually orchestrate model switch.
    Story stub: `feat(skills): triage and retro context-window monitoring with auto-handoff`

16. **Analyst base body: enforce read-only tool contract, add ToolSearch**
    Write/Edit access violates role contract. Carry-forward.
    Story stub: `fix(agents): analyst-base-body tool contract — read-only enforcement`

17. **ux-base-body: correct output envelope to AGENT_OUTPUT_START**
    Cross-story integration failure. Downstream sprint orchestrators will break.
    Story stub: `fix(agents): ux-base-body output envelope mismatch`

18. **CREED blocks and eval files for analyst, researcher, ux agents**
    Behavioral identity unimplemented, no regression protection for three new roles.
    Story stub: `fix(agents): CREED blocks and eval files for analyst, researcher, ux — carry-forward`

### Low / Investigate

19. **AVFL consolidator: require file-existence check before dismissing structural path findings**
    Valid structural finding dismissed; file path discrepancy remains.
    Story stub: `fix(skills): AVFL consolidator structural path finding verification`

20. **AVFL: log developer-directed skips to sprint audit trail**
    Skips are invisible to future retros. Practice gap in audit trail completeness.
    Story stub: `feat(skills): AVFL skip logging with developer reason capture`

21. **momentum:research: explicit scope and framing confirmation before spawning research wave**
    Research scope narrower than intended; developer had to re-frame after research completed.
    Story stub: `fix(skills): momentum:research scope-alignment confirmation gate`

22. **Browser-driver agents: error-count circuit breaker**
    119 turns of wasted compute. No stopping condition for repeated identical errors.
    Story stub: `fix(skills): browser-driver agent circuit breaker after N consecutive identical failures`

23. **Research/decision workflow: cost-and-licensing surface step**
    Licensing implications not surfaced proactively for proposed integrations.
    Story stub: `feat(skills): research and decision cost-and-licensing review step`
