# Sprint Transcript Audit — sprint-2026-06-18

---

## Executive Summary

Sprint-2026-06-18 was a skill/spec sprint (8 stories: 7 in-repo, 1 out-of-repo) delivering the agent-cohort foundation: manifesto format, constitution-builder write modes, build-guidelines skill, and conduct tooling fixes. The build completed in 79 minutes across 3 dependency waves. All 7 in-repo code-deliverable stories converged in a single fix pass — a strong-efficiency data point that isolates shared-file contention and spec ambiguity as the dominant cost drivers (contrast: conduct-core sprint at 86% multi-round). The post-merge AVFL caught 5 cross-story integration issues, confirming it is non-redundant with per-story review.

Three systemic struggles dominate: (1) HITL presentation — developer experienced decision fatigue from wall-of-text output, the Decision-Grade Presentation Standard exists but is not enforced at skill-output time; (2) cross-session continuity — two handoff gaps in the same sprint required manual context reconstruction; (3) inter-skill ownership contracts — the build-guidelines keystone story shipped a functionally-dead mechanism on the first implementation pass because no explicit inter-skill contract existed between it and constitution-builder. The end-gate passed in a single developer turn; the companion decision surface worked as designed.

---

## What Worked Well

### Parallel wave execution — clean and fast
Wave 1 launched 5 stories simultaneously at 18:47:33; all completed by 19:11:48 (24.2 min). Wave 2 followed with a 1.1-min gap, Wave 3 with 0.7 min. The conductor correctly sequenced build-guidelines-skill as a Wave 3 keystone after all constitution artifacts were available. Total wall time: 79 minutes for 8 stories, AVFL, and E2E.

### Single-pass fix convergence for all 7 in-repo stories
No story required a re-dev pass. All transitioned stage-1 → stage-2 exactly once. 24 per-story findings (all routine stakes_class), fixed in a single directed-fix loop per story. No thrash.

### AVFL-on-merge is non-redundant
Post-merge AVFL caught 5 cross-story integration issues (avfl-diagnostic-table-dropped, avfl-constitution-builder-interactivity, avfl-eval-registry-stale, avfl-conductor-supersession, avfl-trigger-format) that per-story review missed. Single-iteration convergence; result CLEAN with 0 leftovers. Both high-consequence catches (corrupted scorecard on resume; stripped auto-invocation triggers) were real defects that would have shipped.

### End-gate companion surface approved in one developer turn
Single-turn approval with proactive gap identification. The developer also requested 3 follow-on stories with priority recommendations in the same turn, which were produced and approved in one more turn. The companion decision surface model held.

### Seam contracts prevented an entire class of handoff bugs
Stories with explicit producer/consumer seam contracts in eval.yaml (conduct-assign-finding-id, conduct-ledger-append-site-dedup-guards) showed clean resolution vs. the build-guidelines↔constitution-builder gap which lacked one. The seam-contract pattern is a load-bearing reviewer prompt mechanism.

### Out-of-repo story path exercised successfully
nornspun-agent-constitution wrote to a different project's repo, ran 8 ACs against a clear source-traceability requirement, required zero human intervention, and completed in 19 minutes. The out-of-repo path worked as designed on first live exercise.

### Pre-build spec verification saved a silent partial implementation
The conduct-ledger-append-site-dedup-guards story spec omitted 2 of 9 targeted append sites. The pre-build verification workflow caught this before dev started, triggering a surgical amendment subagent. Prevented a "ships with 'every site' in AC text but only 7 of 9 guarded" outcome.

### Quality-gate layering caught the two highest-risk divergences
Per-story review caught both critical divergences before merge: (1) empty file patterns → resolver can match nothing; (2) diagnostic table in a gap between two tools. These were the highest-consequence bugs of the sprint. The fail_criteria in the review contracts were load-bearing.

### In-session practice fix — wall-of-text → immediate standard update
Developer's complaint about HITL verbosity led directly to adding the Conversational Reply surface budget to decision-grade-presentation.md and deploying globally within the same session. Practice responsiveness demonstrated.

---

## What Struggled

### HITL presentation: wall-of-text violations still shipping
**What:** Developer experienced 3–4 pages of text with no sense of priority during HITL surfaces. The Decision-Grade Presentation Standard exists and is written into rules, but HITL surfaces during this sprint still produced text walls.
**Why it matters:** The developer's review budget is finite. A longer report from a deeper run still costs the same to read. Repeated violation erodes trust in the practice.
**Evidence:** "Sometimes I get 3 or 4 solid pages of text with no sense of what's important. That's over a thousand words to read and often most of it is not important." (2026-06-23 19:02:58)
**Root cause:** The Decision-Grade Presentation Standard is a written rule but has no enforcement mechanism at skill-output time. Skills emit what they produce; no post-output validator checks compliance before surfacing to the developer.
**Recommendation:** Fix — add a presentation linting step (or AVFL lens) that checks per-surface budget compliance before the developer sees output. Start with the most frequent violators: conductor HITL escalations and end-gate report sections.

### Cross-session continuity: two handoff gaps in one sprint
**What:** Sprint planning completed 6/18 overnight; user returned 6/19 with no context and issued "Please use DuckDB to figure out what our last few sessions were working on." User then returned again 6/23 with only "Continue from where you left off" before conducting the build.
**Why it matters:** Each gap required manual context reconstruction, burning developer attention before any productive work could begin. Two failures in one sprint indicates a systemic gap, not a one-off.
**Evidence:** Redirections at 2026-06-19 23:46:02 and 2026-06-23 18:39:20; handoff convention exists in .claude/rules/handoff-conventions.md but was not triggered after sprint-planning workflow completion.
**Root cause:** The sprint-planning workflow has no terminal handoff step. The handoff convention rule exists but is not wired into the workflow as a required closing action.
**Recommendation:** Fix — add a mandatory handoff artifact step as the final action in the sprint-planning workflow. The artifact should carry: sprint slug, activation status, story list with wave assignment, and the single sentence needed to re-enter context.

### Sprint activation not automatic after planning
**What:** Sprint planning completed 6/18 but the sprint was not activated until 6/22 when the developer explicitly asked "Are all the stories flushed out, fully written? If so please set it to activated."
**Why it matters:** 3.5-day gap between planning completion and activation. The sprint was ready but sitting idle. The developer had to re-verify story readiness to answer a question the workflow should have answered at planning time.
**Evidence:** User message at 2026-06-22 00:35:45; agent ran a verification workflow confirming all 8 stories dev-ready before activation.
**Root cause:** Sprint-planning workflow does not offer a final activation prompt or deliver a clear "all stories ready — activate now?" gate to the developer when planning concludes.
**Recommendation:** Fix — sprint-planning workflow final step should present an explicit activation gate: list the stories, confirm dev-readiness count, and ask approve/defer rather than leaving the sprint in an implicitly-ready-but-not-activated state.

### Inter-skill ownership gap: build-guidelines shipped a functionally-dead mechanism
**What:** The initial build-guidelines implementation registered composed agents with empty file patterns and never assembled the agent body, producing zero functional effect. The failure looked like success (registrations present) until adversarial review verified resolver behavior.
**Why it matters:** A silent-success bug in an orchestrator skill is especially dangerous because its entire job is to wire tools. A wrong wire that looks like a wire can propagate without any visible error signal.
**Evidence:** End-gate §03 divergence #1: "empty file patterns and never assembled the agent body at all." Fixed in commit bf059b6 (168 workflow.md lines reworked).
**Root cause:** The spec did not define the G1 mechanism precisely enough — specifically, who assembles the agent body vs. who registers the agent. The build-guidelines↔constitution-builder interface had no seam contract, so each assumed the other carried the diagnostic table.
**Recommendation:** Fix — require an inter-skill interface contract (mirroring the producer/consumer seam contract pattern from conduct-assign-finding-id) for any story where two skills share a handoff boundary. The contract should specify: who produces the artifact, what shape it takes, who carries it downstream.

### Diagnostic-table ownership fell into a gap between two tools
**What:** build-guidelines assumed constitution-builder would emit the diagnostic table; constitution-builder's write-mode story had deliberately removed that ownership. Neither tool had the table. The sprint's headline deliverable (the symptom→wiki-query map) was absent from composed agents.
**Why it matters:** The diagnostic table is the entire purpose of the manifesto format. A composed agent without it has no routing capability.
**Evidence:** End-gate §03 divergence #2. Fixed in bf059b6 by having build-guidelines carry the manifesto table verbatim.
**Root cause:** When constitution-builder write-mode story removed Quick-Routing ownership, build-guidelines was not updated to know that it now owned the diagnostic table. The inter-skill interface was updated in one direction only.
**Recommendation:** Fix — inter-skill contract updates must be bidirectional. When a downstream skill removes ownership of an artifact, the upstream caller must be explicitly notified and updated in the same sprint. See recommended seam-contract pattern above.

### Audit extract pipeline failure: no agent telemetry for the sprint
**What:** agent-summaries.jsonl has 1 line — a parse error. team-messages.jsonl is empty. The retro auditor for this sprint has no inter-agent message-level evidence; only the build ledger and end-gate report are available.
**Why it matters:** The retro audit engine is blind to agent tool-efficiency, turn counts, and inter-agent coordination patterns for this sprint. Repeated failures make trend analysis impossible.
**Evidence:** "Invalid Input Error: Malformed JSON at byte 1 — Input: {'bytes': 59680, 'code': 200, ...}" — the preprocessor received a Python dict literal (single-quoted) instead of JSON.
**Root cause:** Transcript-preprocessing step serialized a raw HTTP response object rather than a structured summary. The serialization format is agent-dependent and has no schema validation at write time.
**Recommendation:** Fix — add schema validation at transcript-preprocessing output time. The agent summary serializer should reject non-JSON-serializable types before writing and emit a structured error record instead of a malformed line.

### Cross-artifact notes have no structured queue
**What:** Dev agents returning cross-artifact notes ("this is out of my scope but needs attention") deposit them into the Conductor's working context with no structured artifact. If the Conductor session is interrupted or restarted, these notes are lost.
**Why it matters:** Cross-artifact notes carry real risks (the FR136/prd.md amendment note, the nornspun sibling block cross-reference). A lost note is a silently-dropped finding.
**Evidence:** Session 76bc765c 18:54:18: "Both also returned cross-artifact notes — I'm accumulating those for the deferred triage batch." No ledger entry type for "cross-artifact note pending triage" exists.
**Root cause:** The ledger event schema has no entry type for in-flight cross-artifact observations. The Conductor holds them in-context only.
**Recommendation:** Fix — add a `cross-artifact-note` event type to the build ledger. Dev agents should emit this event when they surface an out-of-scope finding, making it queryable and durable across Conductor session boundaries.

### stakes_class label mismatch: false escalation trigger
**What:** Code-reviewer subagents produced non-canonical stakes_class labels (e.g., "cross-reference-integrity", "correctness-of-spec"). The Conductor initially treated these as genuine escalations. Self-corrected, but the mismatch is a latent false-positive path for every future sprint.
**Why it matters:** Every sprint with non-canonical reviewer labels risks the same mis-trigger, burning an unnecessary human pause-ask turn.
**Evidence:** Session 76bc765c 19:03:10: "Every code-review finding used non-canonical stakes_class labels... My workflow's 'escalate' recommendation was a false trigger from treating any non-routine label as stakes-class; correcting that."
**Root cause:** No shared enum or schema validation at the reviewer→Conductor boundary. The code-reviewer skill emits free-text stakes_class values; the Conductor's escalation logic only recognizes a canonical set.
**Recommendation:** Fix — add a stakes_class validation step between code-review output and the Conductor's escalation decision. Reject non-canonical labels with a normalization pass (map known synonyms to canonical values; treat unknown labels as routine).

### Dev agent description-length NFR vs trigger-phrase conflict
**What:** wiki-query story's dev agent shortened the constitution-builder description from 624 chars to 143 chars to satisfy the ≤150-char NFR, but stripped all auto-invocation trigger phrases in the process. The skill became undiscoverable.
**Why it matters:** A skill with no trigger phrases cannot be routed to by Impetus or any agent that uses description-matching for dispatch.
**Evidence:** CR finding: "The diff strips ALL trigger/invocation phrases from the description. The authoritative dev-skills guide states the description is the trigger mechanism."
**Root cause:** The story's DoD listed the length NFR but did not flag the trigger-phrase convention as a conflicting constraint. The dev agent resolved one constraint by violating the other.
**Recommendation:** Fix — add a DoD item to every story that touches a skill SKILL.md: "description length ≤150 chars AND retains at least 3 trigger phrases per agent-skill-development-guide." The two constraints must be co-stated to prevent the dev agent from resolving one by breaking the other.

### Manifesto patterns field gap: G1 is best-effort, not deterministic
**What:** The manifesto format spec has no normative machine-readable file-ownership/patterns field. build-guidelines derives permissions_scope from Project-Stack prose (best-effort), which means G1 agent registration is LLM-inference-dependent, not schema-guaranteed.
**Why it matters:** G1 is the sprint's headline guarantee — composed agents registered resolvably. Without a normative patterns field, the resolver cannot deterministically match composed agents for any project whose stack is ambiguous in prose.
**Evidence:** build-ledger stage3-finding-blocked event: "manifesto-format.md needs a normative machine-readable file-ownership/patterns field for fully-deterministic G1 resolution." Triaged out; follow-up stub filed.
**Root cause:** The manifesto format spec was complete for its stated ACs but left one integration seam undefined: the field that build-guidelines needs to populate agents.json patterns deterministically. The spec's own verification (document-review) had no consumer-integration check.
**Recommendation:** Investigate — the follow-up stub (manifesto-format-normative-file-pattern-ownership-field) is correctly filed. Prioritize it above the headless bypass stub; it is the remaining blocker to deterministic G1.

### Sprint branch upstream not set: recurring push failure
**What:** git push failed with exit 128 "fatal: no upstream configured for branch 'sprint/sprint-2026-06-18'" because the sprint branch was never configured to track a remote. Recovered, but consumed a corrective turn and produced a confusing failure mid-build. Pattern seen in prior sprints.
**Why it matters:** The git-discipline rule requires showing log @{u}..HEAD before push, but the command fails when there is no upstream — making the pre-push preview impossible and the push error confusing.
**Evidence:** errors.jsonl 2026-06-23 19:15:48. Session 6c3463ed 19:16:26: "sprint/sprint-2026-06-18 has no upstream and doesn't exist on origin."
**Root cause:** The Conductor's sprint-branch creation step does not set upstream (--set-upstream / -u). This is the same bug every sprint.
**Recommendation:** Fix — add `git push --set-upstream origin <sprint-branch>` as the first push action when a sprint branch is first created, before any subsequent push attempts. Alternatively, create the remote branch at sprint activation time so upstream is always set.

---

## User Interventions

Five developer interventions occurred in this sprint. Classified by type:

### Required interventions (pipeline failures)

1. **Context reconstruction after sprint planning** (2026-06-19 23:46:02): "Please use DuckDB to figure out what our last few sessions were working on." No handoff artifact; user bore the cost of re-orientation.

2. **Context re-entry after sprint activation gap** (2026-06-23 18:39:20): "Continue from where you left off." 5-day gap between activation and build with no handoff artifact.

3. **Sprint activation not prompted** (2026-06-22 00:35:45): "Are all the stories flushed out, fully written? If so please set it to activated." Sprint had been ready for 3.5 days; user had to recheck and request activation explicitly.

### Appropriate interventions (genuine judgment)

4. **Story scope amendment authorization** (via AskUserQuestion before wave-2): "Fix the story, then activate." Conductor correctly escalated — the spec contradicted its own stated goal. The decision required human authorization, not agent defaulting.

5. **End-gate approval and gap identification** (2026-06-24 04:13:47): "I approve. Merge and push and please also add the three gaps as future stories and recommend priority for the three." Single-turn, proactive gap identification. Appropriate and efficient.

### Developer-initiated practice improvements

6. **Wall-of-text complaint → in-session standard update** (2026-06-23 19:02:58 → 19:13:16): Developer identified the HITL verbosity problem, agent initially hallucinated a non-existent /output-style skill, correction was issued, and the Conversational Reply surface budget was added to decision-grade-presentation.md and deployed globally within the session.

---

## Story-by-Story Analysis

### agent-manifesto-format-specification
**Outcome:** Merged. Clean single-cycle convergence in 22 minutes.
**Findings:** 2 routine findings (count precision, attribution wording). Both fixed in 4-line commit.
**What worked:** Rich Dev Notes + decision reference (DEC-038) + worked exemplar (35-entry prototype) drove fully autonomous convergence. Zero human intervention.
**Struggle:** Manifesto-patterns-field gap emerged only when build-guidelines consumed the format. Document-review verification for spec stories is blind to integration-seam gaps. The cross-story dependency gap requires a consumer-integration check in the review contract template for spec stories with a named downstream consumer.

### constitutionmd-generation-acceptance-criteria
**Outcome:** Merged. 21-minute convergence, single dev+fix pass.
**Findings:** 4 routine findings (wrong skill reference, architecture-option alignment, stale prd.md amendment claim). All minor wording precision fixes.
**What worked:** Cross-reference integrity section in the review contract surfaced false provenance (hallucinated FR136 amendment). Mechanical reference-resolution checks outperform prose-based review for citation accuracy.
**Struggle:** Slug-based session filtering produced a false positive — the session attributed to this story was actually an Impetus conversational session about decision-grade-presentation rule deployment. Retro analysts should not rely solely on slug matching for session attribution.

### constitution-builder-write-mode-parameterization
**Outcome:** Merged. Single dev+fix pass. 18 of 18 ACs pass.
**Findings:** 1 routine finding (Phase 7 section order inverted vs AC-1). Single-line fix.
**What worked:** EDD pre-implementation evals followed correctly (3 new evals, additive to prior corpus). Description lands at 149/150 chars — compliant. Body reduced 559→456 lines, clearing the 500-line NFR.
**Struggle:** Description is at the boundary (149/150). One word added in a future edit breaches NFR1. Flag for next story touching this skill.

### wiki-query-interface-block-for-hot-constitution
**Outcome:** Merged. 24-minute convergence, single fix loop (5 findings fixed, 1 dismissed).
**Findings:** cr-0 (stale "three" → "four" internal reference count); cr-1 (description truncation stripped all trigger phrases); cr-2 (evals not registered in evals.json); qa-0 (DoD checkbox unchecked — dismissed, out of writable scope).
**What worked:** Code review caught two conflicting-constraint bugs the dev missed. QA correctly handled the out-of-scope DoD checkbox with a clean dismissal rationale.
**Struggle:** cr-1 is the description-NFR vs trigger-phrase conflict pattern — the dev resolved one constraint by violating the other. zsh case-glob bug caused scope guard to drop EDD evals, requiring re-commit; same pattern as feedback_zsh_no_word_split_in_bash_tool memory note.

### build-guidelines-skill
**Outcome:** Merged. Wave-3 keystone. 2 architectural fix passes, 26-minute total, 4 agents (~1.7MB).
**Findings:** 7 findings: F1–F5 (routine, fixed), orchestration-guide-stale (routine, fixed), manifesto-patterns-field-gap (high-blast-radius-architecture, triaged-out).
**What worked:** The adversarial re-review (REVIEWER-B) caught both architectural bugs after the initial fix pass. Convergence was clean at merge despite the rework cost. The triaged-out finding was correctly escalated with a follow-up stub.
**Struggle:** Initial implementation shipped a functionally-dead mechanism (empty file patterns, no agent body assembly). Root cause: G1 contract was under-specified; no seam contract between build-guidelines and constitution-builder. This is the sprint's single highest-rework story.

### nornspun-agent-constitution
**Outcome:** Merged (out-of-repo to /Users/steve/projects/nornspun). 19-minute clean pass. 8 ACs verified.
**Findings:** 0 code-review findings. 0 stage transitions. Document-review PASS.
**What worked:** Out-of-repo deliverable path exercised correctly for the first time. Dev agent caught stale Decision 22 reference (silence toggle permanently rejected 2026-06-09) and self-corrected without intervention.
**Struggle:** Ledger has only start/end events with no intermediate verification record for this story type. A retrospective reader cannot distinguish "stage-2 was skipped intentionally" from "silently missed." The out-of-repo story type needs a normative ledger event variant.

### conduct-assign-finding-id-before-directed-fix-invocation
**Outcome:** Merged. 22-minute convergence, 2 passes (feat + fix). All 8 ACs verified.
**Findings:** cr-0 (eval line anchors cited wrong lines); cr-1 (uniqueness invariant overstated vs algorithm guarantees). Both fixed in 9903961.
**What worked:** Seam contract (producer/consumer field-shape invariants) gave reviewer exact failure-mode language. QA verified 8 ACs; code review caught the 2 issues QA missed. Clean signals from two complementary mechanisms.
**Struggle:** QA does not audit internal accuracy of eval pass conditions against the workflow source. An eval citing wrong line numbers passes QA if the AC text is satisfied. Code review caught what QA missed — this is a QA scope gap.

### conduct-ledger-append-site-dedup-guards
**Outcome:** Merged. 14.5-minute convergence after pre-build scope amendment. 2 high-severity code-review findings, both fixed.
**Findings:** cr-0 (dedup guard over-broad for re-run stories — latent bug); cr-1 (eval fabricated a non-existent clearing mechanism); scope gap (2 of 9 append sites omitted from spec, caught pre-build).
**What worked:** Pre-build verification caught the scope gap before dev started. Adversarial code review caught a multi-story interaction bug and an eval fabrication that dev's own EDD evals missed. Surgical implementation (workflow.md grew by 1 net line).
**Struggle:** The latent re-run bug required understanding the contract between two dependent stories (finding_id determinism from conduct-assign-finding-id interacting with the new dedup guard). Neither the dev agent nor its EDD evals caught it — only adversarial review found it.

---

## Cross-Cutting Patterns

### Pattern 1: Seam contracts are load-bearing — missing ones are the highest-cost bugs
Stories with explicit producer/consumer seam contracts (conduct-assign-finding-id, conduct-ledger) showed clean review resolution. The build-guidelines↔constitution-builder gap — with no seam contract — produced two architectural bugs requiring two fix passes, 1.1MB of rework agents, and the sprint's only high-blast-radius finding. The correlation is clean across all 8 stories.

### Pattern 2: Document-review spec stories need consumer-integration checks
Two spec stories (agent-manifesto-format-specification, constitutionmd-generation-acceptance-criteria) both had review contracts that checked the document against its own ACs but not against the downstream consumer's behavior. Both had integration gaps that only emerged when a consumer ran against them. Document-review verification for spec stories is systematically blind to this class of defect.

### Pattern 3: Handoff gaps recur within the same sprint
Two cross-session continuity failures in one sprint, both traceable to the same root cause: the sprint-planning workflow has no terminal handoff step. The handoff convention is documented as a rule but not wired into any workflow as a required closing action. Rules without workflow enforcement do not fire.

### Pattern 4: Conflicting constraints require co-stating in DoD
The description-NFR vs trigger-phrase conflict (wiki-query story) is a predictable collision when two constraints exist on the same field but appear in different documents. The dev agent resolved one by violating the other because neither document referenced the other. Any two constraints that can conflict need a co-stated DoD item that names both and requires satisfying both.

### Pattern 5: zsh glob behavior recurs in conductor scope guards
The scope guard bug (wiki-query story) is the same pattern documented in feedback_zsh_no_word_split_in_bash_tool. The conductor's guard logic was not updated after the original memory note was written. Memory notes that document behavioral gotchas need a corresponding code fix, not just documentation.

### Pattern 6: The audit extract pipeline is a single point of fragility
With 0 usable agent summary records and 0 team messages, the retro engine for this sprint operated at reduced fidelity — relying entirely on the build ledger and end-gate report. The parse error (Python dict literal vs JSON) indicates the preprocessing step has no output schema validation. A retro is only as good as its extracts.

### Pattern 7: Quality gate layering works — no single gate is sufficient
Per-story review caught 24 findings and the 2 highest-consequence divergences. AVFL-on-merge caught 5 integration issues per-story review missed. Pre-build verification caught a spec scope gap before dev started. Adversarial code review caught bugs that QA and EDD evals both missed. The pipeline's quality is the product of all gates combined; removing any one gate would have let bugs through.

---

## Metrics

| Metric | Value | Notes |
|---|---|---|
| user_msgs | 5 | user-messages.jsonl line count |
| subagents | 1 | agent-summaries.jsonl line count (1 line = 1 parse error; 0 usable records) |
| errors | 1 | errors.jsonl line count — sprint branch no-upstream push failure |
| team_msgs | 0 | team-messages.jsonl empty |
| findings_total | 80 | verified findings entering synthesis |
| findings_keep | 30 | recommend: keep (strengths, expected behavior) |
| findings_fix | 22 | recommend: fix (actionable defects) |
| findings_investigate | 28 | recommend: investigate (patterns needing deeper analysis) |
| stories_total | 8 | 7 in-repo + 1 out-of-repo |
| stories_single_pass | 7 | all in-repo stories converged in one fix pass |
| per_story_findings | 24 | routine stakes only |
| avfl_merge_findings | 5 | cross-story integration issues caught post-merge |
| sprint_wall_time_min | 79 | wave-1 launch to E2E complete |
| support_agent_context_pct | 42 | eval-runners + E2E + code-reviewer + HTML renderer as % of 6.9MB sprint total |
| human_interventions_required | 3 | pipeline failures requiring user action (excludes appropriate judgment gates) |
| human_interventions_appropriate | 2 | genuine judgment calls correctly escalated |
| high_blast_radius_findings | 1 | manifesto-patterns-field-gap (triaged-out with follow-up stub) |
| false_positive_rate | 3.4% | 1 dismissed finding out of 29 total per-story findings |

---

## Priority Action Items

### 1. Add mandatory handoff artifact to sprint-planning workflow terminal step
**Priority:** critical
**Source detail:** Two cross-session continuity failures in one sprint (redirections at 2026-06-19 23:46:02 and 2026-06-23 18:39:20). The handoff convention rule (.claude/rules/handoff-conventions.md) exists but is not wired into the sprint-planning workflow as a required closing action.
**Suggested ACs:**
- sprint-planning workflow's final step emits a handoff artifact to `.momentum/handoffs/sprint-{slug}-planning-{date}.md`
- artifact carries: sprint slug, activation status, story list with wave assignment, open questions/decisions, and a one-sentence re-entry context line
- artifact is committed before the workflow exits
- the developer is shown the artifact path as the last output of the planning workflow
- validated: a new session can re-orient to sprint state by reading only the handoff artifact (no other files required)

### 2. Add explicit activation gate to sprint-planning workflow final step
**Priority:** critical
**Source detail:** Sprint planning completed 6/18; sprint remained unactivated until developer explicitly re-verified and requested activation on 6/22 (3.5-day gap). User message at 2026-06-22 00:35:45.
**Suggested ACs:**
- sprint-planning workflow's final step performs a dev-readiness count (stories with all ACs written and spec frozen)
- if count equals total story count: presents an explicit activate now/defer gate to the developer
- gate displays story list, wave dependency summary, and readiness verdict before asking
- if developer approves: calls sprint-manager to activate immediately
- if developer defers: records deferral reason in the handoff artifact

### 3. Require inter-skill seam contracts for stories where two skills share a handoff boundary
**Priority:** high
**Source detail:** build-guidelines↔constitution-builder lacked a seam contract; both bugs (empty file patterns, diagnostic-table ownership gap) resulted directly from this. Conduct-assign-finding-id and conduct-ledger stories had seam contracts and showed clean review resolution. End-gate §03 divergences #1 and #2.
**Suggested ACs:**
- sprint-planning checklist includes: "for each story that calls a sibling skill's output as input, a seam contract (producer/consumer/artifact shape) is written into the story spec before freeze"
- the seam contract specifies: who produces the artifact, what schema/shape it has, who carries it downstream, and what the failure mode is if the shape is wrong
- stories with seam contracts have a DoD item: "reviewer verified artifact shape matches seam contract"
- when a story removes ownership of an artifact from a skill, the affected upstream callers are identified and their stories are updated in the same sprint

### 4. Add stakes_class validation between code-reviewer output and Conductor escalation logic
**Priority:** high
**Source detail:** Code-reviewer emitted non-canonical labels (cross-reference-integrity, correctness-of-spec); Conductor initially mis-triggered an escalation path. Session 76bc765c 19:03:10. No shared enum exists at the reviewer→Conductor boundary.
**Suggested ACs:**
- define a canonical stakes_class enum (security-auth-isolation, irreversible-destructive, high-blast-radius-architecture, routine) in the conductor's references
- code-reviewer SKILL.md requires emitting only canonical stakes_class values
- conductor workflow includes a normalization pass after code-review output: map known synonyms to canonical values; treat unrecognized values as routine with a logged note
- validated: a code-review finding with stakes_class "cross-reference-integrity" is normalized to "routine" before the escalation decision

### 5. Fix transcript-preprocessing to reject non-JSON-serializable agent summary output
**Priority:** high
**Source detail:** agent-summaries.jsonl has 1 line — a parse error. The preprocessor received a Python dict literal (single-quoted) instead of JSON. The retro engine operated at reduced fidelity for the entire sprint. audit-extracts/agent-summaries.jsonl line 1.
**Suggested ACs:**
- transcript preprocessor validates agent summary output is valid JSON before writing to agent-summaries.jsonl
- on validation failure: emits a structured error record (agent_id, error_type, raw_preview) instead of a malformed line
- on validation failure: logs the error and continues processing remaining summaries rather than silently dropping them
- validated: running the preprocessor against a Python-dict-literal input produces a parseable error record, not a malformed line

### 6. Add cross-artifact-note event type to build ledger
**Priority:** high
**Source detail:** Dev agents returning out-of-scope observations deposited them into the Conductor's working context only. If the Conductor session is interrupted, these notes are lost. Session 76bc765c 18:54:18: "I'm accumulating those for the deferred triage batch."
**Suggested ACs:**
- add event type `cross-artifact-note` to the build ledger schema (story_slug, note, target_artifact, triage_status: pending|resolved)
- conductor workflow: when a dev agent returns a cross-artifact note in its AGENT_OUTPUT, append a cross-artifact-note ledger event before continuing to the next story
- cross-artifact-note events with triage_status=pending are surfaced in the end-gate report as a deferred-items section
- validated: a resumed Conductor session can query the ledger and find all pending cross-artifact notes without relying on prior session context

### 7. Add consumer-integration check to review contract template for specification stories
**Priority:** medium
**Source detail:** agent-manifesto-format-specification and constitutionmd-generation-acceptance-criteria both had document-review contracts that checked the document against its own ACs but not against the downstream consumer. The manifesto-patterns-field gap (high-blast-radius-architecture) was only surfaced when build-guidelines consumed the format.
**Suggested ACs:**
- spec story template includes a "Consumer Integration" section in the review contract (review.md)
- the section requires: "for each named downstream consumer in the story spec, list the observable the consumer requires and the check the reviewer will perform to verify it"
- for spec stories with a named downstream consumer: the review contract is not frozen until the Consumer Integration section is populated
- validated: a manifesto-format spec story would require a review check that build-guidelines can parse the format and derive a non-empty patterns value

### 8. Co-state conflicting DoD constraints on skill SKILL.md edits
**Priority:** medium
**Source detail:** wiki-query dev agent resolved description-length NFR by stripping all trigger phrases. The two constraints (≤150 chars AND trigger phrases) appear in different documents. CR finding: "The diff strips ALL trigger/invocation phrases." Fix commit ec7f3f8.
**Suggested ACs:**
- story template for any story touching a skill's SKILL.md includes a DoD item: "description length ≤150 chars AND retains ≥3 trigger phrases per agent-skill-development-guide"
- the DoD item cites both constraint sources explicitly
- code-reviewer check for SKILL.md edits verifies: (a) description length ≤150 chars, (b) at least 3 recognizable trigger phrases present, (c) neither constraint was satisfied by violating the other
- validated: a description with 148 chars but no trigger phrases fails the co-stated check

### 9. Fix Conductor sprint-branch upstream at branch creation time
**Priority:** medium
**Source detail:** errors.jsonl 2026-06-23 19:15:48: exit 128 "no upstream configured for branch 'sprint/sprint-2026-06-18'". Pattern seen in prior sprints. git-discipline rule requires log @{u}..HEAD before push, which fails when no upstream is set.
**Suggested ACs:**
- conductor workflow creates the sprint branch with `git push --set-upstream origin <sprint-branch>` at branch creation time (before any story commits)
- alternatively: conductor workflow creates the remote tracking branch at sprint activation time using `git push -u origin HEAD`
- validated: `git log @{u}..HEAD` succeeds without error immediately after sprint branch creation
- validated: no subsequent push to the sprint branch requires `--set-upstream` or `-u`

### 10. Add QA scope item: validate eval pass conditions against source file
**Priority:** low
**Source detail:** conduct-assign-finding-id story — QA returned all-verified across 8 ACs while code review simultaneously found a factual error in an eval's pass condition (wrong line anchors for the mechanism described). QA scope gap confirmed.
**Suggested ACs:**
- QA reviewer SKILL.md adds a check: for each eval file cited in the story's DoD, verify that concrete file references (line numbers, mechanism names) in the pass conditions resolve against the current state of the source file
- if an eval cites a line number: QA verifies that line exists and contains the expected content
- if an eval describes a mechanism: QA verifies that mechanism exists in the source at the cited location
- validated: an eval citing "line ~759" for a bind site that is actually at line 763 fails the QA check
