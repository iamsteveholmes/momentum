# Sprint Transcript Audit — sprint-2026-04-14

**Retro date:** 2026-04-16
**Sprint completed:** 2026-04-15
**Data analyzed:** 146 user messages | 106 subagents | 165 errors | 200 team messages

## Executive Summary

This sprint delivered its two shipped stories (triage-skill, retro-triage-handoff) but the transcript reveals a sprint that was, in practice, a *strategic redesign window*. Roughly 81 real user prompts across 4 sessions spanned 2026-04-13 → 2026-04-14, with the bulk of user attention spent on research, decisions, and reframing the Momentum practice model (features as the primary value unit, epics as DDD domain boundaries, Judgment Frame for human-in-loop review, HTML-directory dashboard, E2E-behavior-only verification). Sprint output versus transcript output are two different stories: merged code was small; practice-layer learning was the sprint's real deliverable.

The **headline finding** is a systemic bug that reframes every prior retro's distill work: distill edits to plugin-installed `workflow.md` template blocks do **not reach runtime** when a Claude Code session has cached a pre-distill plugin version. We proved this directly — the streaming-read guidance distilled from the last retro (commit `4306c27`, 2026-04-12 20:07) was on disk 6 hours before this retro ran, yet the retro orchestrator spawned all 5 auditor-human, 3 auditor-execution, and 4 auditor-review agents from a stale 0.14.0 plugin cache that pre-dated the distill. The fix landed; the runtime kept using yesterday's prompt. Every distill targeting a workflow.md template block is subject to this silent-miss pattern. This is the single most important action item from the sprint.

Supporting themes: **spec fatigue is real and acknowledged by the user** ("I typically ignore almost the entire spec" — H6), driving concrete decisions for a Judgment Frame human-review section and an HTML-directory feature dashboard. **Orchestrator framing subverts correct agent definitions** — the user personally traced the e2e-validator bug through two levels, proving a correctly-written agent can still fail if its spawn prompt gives it an escape hatch. **Distill skill has calibration problems** — jargon-without-definition, heavyweight ceremony, path-classification bugs that conflate cwd with plugin scope. **Quality gates work when structured** — AVFL iter1→iter2 convergence (61→85), adversary passes catching cross-artifact conflicts enumerators missed, parallel lens reviewers catching portability bugs, and orchestrator→precision-writer separation producing clean auditable diffs. **Priority actions:** fix plugin-cache staleness (critical), overhaul story template with Judgment Frame section (high), harden E2E validator spawn block against orchestrator framing (high), fix distill path-classification logic (high), fix documenter transcript extractor (medium).

## What Worked Well

### W1. AVFL iter→iter convergence on the research corpus

**Description:** The adapting-agile research corpus moved from 61/100 POOR (iter1) to 85/100 NEEDS_FIX (iter2) after a real fix pass, with ~120 findings reduced to ~55 — a 54% convergence rate. Real defects caught before the corpus was used as input to a 14-decision restructuring pass: Harness Engineering attribution collision across three sources, Casey West dating correction to 2025, "clean break" vs "ADLC wrapper" accuracy fix, Kinetic Enterprise [UNVERIFIED] tagging, METR direction-of-effect correction, AI-DLC vs 3-3-3 contradiction resolution.

**Evidence:** Consolidator agents `agent-ab78275b`, `agent-a0da9737`, `agent-ab0e71512` (REV-01). Iter1 vs iter2 finding-count delta: ~120→~55.

**Recommendation:** KEEP — this is the reference point for what healthy AVFL execution looks like.

### W2. Enumerator→adversary two-pass caught cross-artifact conflicts

**Description:** Distill learning cycles used enumerators (short, 3-turn) that proposed changes, then adversaries (9–25 turn) that checked for conflicts with other artifacts. The Tier 1/Tier 2 classification adversary flagged "FOUR artifacts beyond distill/workflow.md" including PRD FR97 that the enumerator had not checked. The Path-A classification adversary caught an attempt to restrict Path A to project-local artifacts by verifying line 60 of `distill/workflow.md`: `.claude/rules/` (project-local, correct) vs `~/.claude/rules/` (installed-output, wrong).

**Evidence:** REV-03, REV-08. Adversary `ad0c47abb` (25 turns, 3 errors), adversary `a9605c42` (15 turns).

**Recommendation:** KEEP — resist collapsing to single-pass. The adversary pass is earning its keep.

### W3. Parallel lens reviewers caught real portability bugs

**Description:** Two structural reviewers in parallel on the sprint-dev Phase 7 worktree-cleanup shell command both independently flagged macOS `xargs` portability (different framing, same defect). Consolidator tagged CRITICAL / HIGH confidence. Portable shell shipped instead of a Linux-only pipeline that would have failed silently on this developer's macOS.

**Evidence:** REV-04. Reviewers `a1a553f` (19 turns, 1 error) and `ac987e2a` (33 turns). Consolidator `ad56cf536`.

**Recommendation:** KEEP — parallel per-lens reviewers are catching issues a single reviewer would miss.

### W4. Orchestrator→precision-writer separation produced clean auditable diffs

**Description:** Six precision-writer agents ran with a narrow-scope prompt: "apply exactly ONE change to exactly ONE file. Do not explore, do not make adjacent improvements, do not modify anything not specified." Every one produced before/after diffs. Zero scope creep. Only two hit errors (lint-format hook race), both still closed with diff-confirmed changes.

**Evidence:** REV-10. Agents `a3c2dac0`, `ac3898682`, `a0c3a267c`, `a207af08e`, `a928112c`, `a80c0fac`.

**Recommendation:** KEEP — the orchestrator-purity pattern is paying off.

### W5. Iter-N prompt explicitly listed iter-(N-1) fixes for validators to verify

**Description:** Iter2 AVFL validator prompts contained explicit "Context — iteration 1 fixes:" blocks listing each fix, with `skepticism=2` (down from iter1 `skepticism=3`) also declared. Example (Coherence Enum): "AI-DLC vs. 3-3-3 contradiction — resolved, the Gemini section now...". Prevents duplicate findings across iterations, makes fix loop auditable.

**Evidence:** REV-09. Validators `a5a08e`, `a7223c1`, `ab62f08b33`, `abe441b5`, `ae4f0662`, `aed6f35`.

**Recommendation:** KEEP — codify "iter-N prompt lists iter-(N-1) fixes" as a requirement for any multi-iteration AVFL run.

### W6. Challenger/analyst role pairing produced substantive critique, not generic validation

**Description:** Cycle-analysis agents named their theses, e.g., Sprint Dev Challenger `a0a6cf8e`: "Sprint Dev is a consistency pipeline masquerading as a quality pipeline." Challenger prompts framed "evaluate Momentum practice against recent research" and demanded a thesis. Structured analyst+challenger pairing per phase, artifacts committed under cycle-analysis/.

**Evidence:** REV-11. Agents `a0a6cf8e`, `a62436ff`, `a585366`, `a932790e`, `a81a2e77`.

**Recommendation:** KEEP — reusable for future practice audits.

### W7. Team-based documenter ↔ auditor iterative collaboration outperformed fan-out

**Description:** During the prior retro run, the documenter pre-emptively pinged "ready to receive findings" to all three auditors. After batch 1 from auditor-human, the documenter asked a targeted dig-deeper ("E2E re-run pattern across rounds?") and auditor-human delivered a spec-vs-behavior correlation the first batch lacked. auditor-review then delivered a scope correction reframing both auditor-human and documenter analysis.

**Evidence:** REV-05, REV-12. A scope-clarification cross-message ("Critical context update from auditor-review...") forced mid-audit re-scoping — the kind of lateral catch that fan-out cannot produce.

**Recommendation:** KEEP — codify "pre-emptive ready ping + targeted dig-deeper" as the documenter playbook. Preserve TeamCreate (not fan-out) for retro auditing.

### W8. Gemini Deep Research via cmux browser produced high-quality output fast

**Description:** User reaction: "Wow it's already done in gemini. You can always send it follow up questions until you are satisfied." Validates the gemini-integration direction.

**Evidence:** H18 (user praise 2026-04-13T19:57:45Z).

**Recommendation:** KEEP — Gemini Deep Research integration worth productizing further.

### W9. User-driven continuous distill works when lightweight

**Description:** User himself submitted fully-formed distill prompts for e2e-validator observations (H20, H21), one finding spanning two levels of the same bug (agent definition AND spawn prompt). When distill is invoked in lightweight mode from direct observation, it flows cleanly.

**Evidence:** H20, H21 (2026-04-14T21:59Z and 23:17Z, session 657a20ca).

**Recommendation:** KEEP — the "continuous distill" direction is validated. See Struggle S3 for the calibration side.

### W10. High-rate frictionless approvals when proposals landed

**Description:** Many single-word affirmations across the sprint ("Proceed, Kind Agent!", "That looks right", 19+ "Yes"). Healthy collaboration signal — when agent proposals land, they land cleanly.

**Evidence:** H19 (sprint-wide).

**Recommendation:** KEEP — baseline flow is functional.

## What Struggled

### S1. [CRITICAL] Plugin-cache staleness silently invalidated distills

**Description:** Distill edits to `skills/momentum/skills/retro/workflow.md` (commit `4306c27`, 2026-04-12 20:07) added the streaming-read guidance to all three retro-auditor system-prompt template blocks. Six hours later (2026-04-13 02:43), the retro orchestrator read `~/.claude/plugins/cache/momentum/momentum/0.14.0/skills/retro/workflow.md` — a pre-distill cached version — and composed all 12 retro-auditor system prompts from it. Guidance absent in every delivered prompt. 60 file-too-large errors followed.

**Evidence:** Orchestrator session `23555e71-274d-4288-bd70-a91ed9b49e5e.jsonl` Read event at 2026-04-13T02:42:06.769Z. Cached file has 0 hits for streaming markers; source-tree file has 3 hits; 0.14.5 cached file has 3 hits. Six auditor prompts individually verified (1670, 1783×3, 1599×2 chars) — zero streaming markers in any. Execution auditor finding #1 (revised). REV-06 (amended).

**Root cause:** Claude Code resolves skill templates from the plugin-cache version locked at session start. Distills that modify on-disk source are not visible to any already-running session. There is no cache-invalidation step in the distill flow. This is a latent failure mode for **every distill touching a plugin-installed skill** — the distill's effectiveness is bounded by cache freshness, not commit recency.

**Blast radius:** Every skill with a TeamCreate-spawned system-prompt template in its workflow.md: `retro`, `sprint-dev`, `avfl`, `decision`, `research`.

**Recommendation:** FIX (critical). Pick one or both levers: (1) Impetus preflight check that compares source-tree `plugin.json` version to active plugin-cache version and prompts `/plugin marketplace update momentum` if skewed; (2) orchestrators `Read` workflow.md from source tree (`skills/momentum/skills/.../workflow.md`) rather than from the plugin cache when operating inside the momentum project. Distill flow must either bump and republish, or explicitly document that the fix will not apply until next session start.

### S2. [HIGH] Spec fatigue — user explicitly skips spec review

**Description:** User's own words: "I typically ignore almost the entire spec, glancing through the acceptance criteria, but as I switch from one context to another it's just TOO MUCH." The story template is optimized for LLM context, not human review — acceptance criteria too low-level-technical, description too high-level to be useful, possible to agree with summary and miss AC failures.

**Evidence:** H6 (2026-04-13T21:53:13Z).

**Root cause:** Story template serves LLM-implementation needs, not human-review needs. Human-in-loop gate is theatrical when the artifact is unreviewable.

**Recommendation:** FIX (high). Story template redesign per user decision H26: add a Judgment Frame section for human review as a first-class element (feature concept, not story concept — holds full context for reviewing the story), plus LLM-optimized section, single file with clear demarcation of which parts are meant for whom.

### S3. [HIGH] Orchestrator framing subverts correct agent definitions

**Description:** The e2e-validator agent definition was behaviorally correct, but in sprint-2026-04-12 the orchestrator pre-announced "the backend was down" and suggested pytest as a primary validation method — handing the agent an exit from live testing. A correctly-written agent can still fail if its spawn prompt provides an escape hatch from the behavior the agent was defined to enforce.

**Evidence:** H20 + H21 (2026-04-14T21:59Z and 23:17Z). User traced the bug through both levels.

**Root cause:** Separation of concerns between agent definition and agent spawn prompt is not enforced. Spawn prompts can override or weaken agent invariants without guardrail.

**Recommendation:** FIX (high). (1) `e2e-validator.md` gets its own "Environment Prerequisites" section that makes it resilient to orchestrator framing (user-provided text, H20). (2) `sprint-dev/workflow.md` Phase 5 E2E Validator spawn block gets explicit constraints preventing orchestrator from offering test-method escape hatches (H21). General principle: agent invariants must be unweakenable by spawn prompts.

### S4. [HIGH] Distill skill path-classification conflates cwd with plugin scope

**Description:** Distill told the user "Both changes correctly targeted Momentum plugin files (Path B), which is right since we are in the Momentum project." User response: "What does this mean? Whether or not it's in the momentum project doesn't determine whether or not it's part of the momentum plugin. That's nonsense." Classification currently keys on cwd heuristics; correct criterion is scope/portability (all-user vs momentum-only).

**Evidence:** H1 (2026-04-13T03:17:25Z). Followed by H3 enumeration of missing cases (local-vs-global plugin install).

**Root cause:** Distill path-classification logic is under-specified and keys on the wrong signal (cwd, not intended scope).

**Recommendation:** FIX (high). `skills/momentum/skills/distill/` path-classification decision tree rewritten to key on scope/portability. Handle local-vs-global plugin install modes. Remove cwd-based heuristics.

### S5. [HIGH] Distill output used internal vocabulary without defining it

**Description:** Distill presented "Path A/B/C/D", "Write Subagents", sandbox constraints without defining any of them. User had to ask five variants of "what does this mean" in 15 minutes: "What is 'Write Subagents'?... What is the use case for writing to ~/.claude?... Path C means you write a prompt, right?... Can you show me what path A, B and C do when they are determined to be one of those paths?"

**Evidence:** H2 (2026-04-13T03:22–03:37Z, 5 messages in 15 min).

**Root cause:** Skill output presupposes reader has internal vocabulary. Human-facing text fell into jargon-without-definition.

**Recommendation:** FIX (high). Distill output must define its own terms before using them. Every human-facing path classification message should inline what the path *does*, not just name it.

### S6. [MEDIUM] Distill ceremony mis-calibrated — heavyweight when user wants lightweight

**Description:** User: "I agree wholly with distill being continuous, but a distillation still requires user understanding and approving... It's not clear to me that our current level of ceremony around distillations is appropriate, sometimes it feels heavyweight, and other times, I'm thinking of the retros specifically, the workflow automates it too much." And: "I'm a little concerned with two things, A. that our distillations aren't being used enough, and B. that we're forcing too much rigor into our distallations." Distillations may be simultaneously underused AND over-ceremonial.

**Evidence:** H13 (2026-04-14T17:06:53Z), H17 (2026-04-14T19:24:01Z).

**Root cause:** No clear tiering between lightweight-continuous distill (user-observed, fast, gated) and heavyweight retro-Tier-1 distill. Retro auto-applies without user gate; direct invocation over-ceremonial.

**Recommendation:** FIX (medium). Tier distill ceremony: lightweight-by-default for user-observed learnings, heavier ceremony only for retro Tier 1 findings. Retro should NOT auto-apply distills — user approval gate.

### S7. [MEDIUM] Research skill ran subagents sequentially, framed question too narrowly

**Description:** User: "In the meantime should you not run the rest of your agents in parallel?" — research orchestrator defaulted to sequential despite workflow-fidelity "Parallelism Is Expected" rule. Separately: "I wouldn't necessarily call it adapting agile for ai, I would happily get rid of agile totally if that was appropriate" — skill locked a narrow title before checking the user's open-endedness.

**Evidence:** H4, H5 (2026-04-13T19:55:39Z).

**Root cause:** (1) research workflow does not explicitly spawn Phase-2 subagents in parallel; (2) research skill crystallizes question framing before user confirmation.

**Recommendation:** FIX (medium). research workflow launches Phase-2 subagents in parallel by default; adds a framing-confirmation step before locking the research question.

### S8. [MEDIUM] Sprint close does not enforce worktree/branch cleanup

**Description:** User repeatedly had to prompt: "can you please review all our git branches local and remote and delete any that have been merged into main / How is it possible that we have these that haven't been merged? / Can you make sure all the branches have been cleaned up too and worktrees both local and remote?" This drove the sprint-dev -D distill prompt.

**Evidence:** H24 (2026-04-13T06:37–19:46Z, session 4bf01be2).

**Root cause:** Sprint close flow has no mandatory worktree+branch cleanup verification. Depends on orchestrator discretion.

**Recommendation:** FIX (medium). Sprint close must verify worktree+branch cleanup as a required gate, both local and remote. Include the macOS-portable xargs fix from W3.

### S9. [MEDIUM] Documenter transcript extractor fails to parse 100% of documenter records

**Description:** Every documenter agent record in `agent-summaries.jsonl` shows `parse_error: "Invalid Input Error: Malformed JSON at byte 1 of input"` with input starting `{'stdout': NULL, ...}`. Eight of eight documenter agents: 100% failure. Zero documenters have parseable turn/tool counts. Agent size ranged 65kb–591kb. Retro has a blind spot for its own most important role.

**Evidence:** Execution auditor finding #4. DuckDB `read_json_auto` rejects Python-repr style dicts ( `{'stdout': NULL}` — lowercase `NULL` and single quotes are Python repr, not JSON).

**Root cause:** Either (a) transcript writer is serializing with Python repr instead of `json.dumps`, or (b) extractor SQL misinterprets a valid JSON shape. Since documenter agents drive retro findings, this is a structural observability gap.

**Recommendation:** FIX (medium). Audit `scripts/transcript-query.py` and the transcript writer. Make parsing robust to both JSON and Python repr inputs, or normalize the writer.

### S10. [MEDIUM] SendMessage schema ↔ auditor prompt mismatch

**Description:** All 5 auditor-human agents hit 2 InputValidationErrors each (10 of 12 total) — "expected string, received object" — agent passed a JSON object as the `message` body instead of a string. Prompts told agents to format findings "as a JSON array under key execution_findings" which agents interpreted as passing a JSON object (not JSON-formatted string) to SendMessage.

**Evidence:** Execution finding #2. Same error on all 5 agents — systematic, not random.

**Root cause:** Prompt-schema ambiguity. Prompt says "JSON array", schema requires string.

**Recommendation:** FIX (medium). Retro auditor prompts explicitly state "send as a string containing JSON" with an example, OR extend SendMessage schema to accept objects.

### S11. [MEDIUM] API stream idle timeouts on corpus-mode AVFL validators produced partial signal

**Description:** Four AVFL validators (`a12ddb668`, `a8fb2f6c6b`, `ad3f87d7d`, `abc82c740`) terminated with "API Error: Stream idle timeout - partial response received" after 14–67 turns on the 9-file research corpus. Partial results produced, not re-run. Fix-pass validator timed out at 22 turns meaning iter2 fixes applied on partial signal. Likely explains REV-02 final-score regression (85→81): scores on missing validator findings are not comparable across iterations.

**Evidence:** REV-07, REV-02.

**Root cause:** Corpus-mode AVFL on 9-file research corpora pushes validators past API stream idle timeout. Consolidator not aware of missing-signal.

**Recommendation:** FIX (medium). Reduce corpus size per validator, add per-validator retry logic, or cap per-turn context. Surface timeouts to consolidator as explicit missing-signal so it can weight accordingly. Anchor final-consolidator scoring to validator-finding delta (or have same agent re-score iter2 and final) so convergence is comparable.

### S12. [MEDIUM] Session identity drift across multi-day work

**Description:** User: "But not the retro, right? / Oh wait this was the retro, right?" (H25). And earlier: "What happened?" after context compaction (H22). User genuinely uncertain what purpose a session served.

**Evidence:** H22, H25 (2026-04-14T02:45:41Z and 2026-04-13T19:45–19:46Z).

**Root cause:** No structured session-identity surface. After compaction or multi-day gaps, the session's purpose isn't re-projected.

**Recommendation:** INVESTIGATE. Impetus session greeting unambiguously state session purpose. Session resume (post-compact) should have a structured "where are we" summary.

### S13. [LOW] Two mid-tool interruptions suggest premature action

**Description:** Two `[Request interrupted by user]` events in the sprint. First during distill path classification (2026-04-13T03:09:39Z), second immediately after H14 ("How did you come to this conclusion? This is a huge change...", 2026-04-14T18:06:31Z). Pattern: agent committing to action before user alignment on a large-surface change.

**Evidence:** H15.

**Root cause:** Unclear — need correlation across the two contexts.

**Recommendation:** INVESTIGATE. Check if the two interruption contexts share a pattern of premature action on high-blast-radius changes.

## User Interventions

Substantive user corrections, redirections, and frustration signals — these are the highest-signal guidance for practice evolution.

| # | Timestamp | Type | Context / Implication |
|---|-----------|------|----------------------|
| 1 | 2026-04-13T03:09Z | Interrupt | Mid-tool during distill path classification — premature commitment |
| 2 | 2026-04-13T03:17Z | Correction (H1) | Distill path classification conflates cwd with plugin scope |
| 3 | 2026-04-13T03:22–03:37Z | Frustration (H2) | "What does this mean?" ×5 in 15 min — distill jargon-without-definition |
| 4 | 2026-04-13T03:46Z | Correction (H3) | User forced to do design thinking for distill's path logic |
| 5 | 2026-04-13T19:45–19:46Z | Redirection (H25) | "Oh wait this was the retro, right?" — session identity drift |
| 6 | 2026-04-13T19:55Z | Redirection (H4) | "Should you not run the rest of your agents in parallel?" — research skill sequential by default |
| 7 | 2026-04-13T19:55Z | Correction (H5) | Research framed too narrowly ("adapting agile"); user's intent broader |
| 8 | 2026-04-13T21:53Z | Correction (H23) | "You could look into the bmad files yourself" — agent offloaded discoverable lookup |
| 9 | 2026-04-13T21:53Z | Frustration (H6) | Spec fatigue — "I typically ignore almost the entire spec... too much" |
| 10 | 2026-04-14T02:45Z | Frustration (H22) | "What happened?" — post-compact context loss |
| 11 | 2026-04-14T03:53Z | Correction (H9) | "A rewrite is... failure is a good thing to recognize" — agent tried to euphemize failure |
| 12 | 2026-04-14T04:10–04:37Z | Decision (H8) | Features as first class, epics as DDD domain boundary, four terminal states |
| 13 | 2026-04-14T04:22Z | Correction (H10) | "Four sprints delivered every speced story and still did not reach the floor" — biggest evidence for redesign |
| 14 | 2026-04-14T04:51Z | Correction (H11) | "I don't want to think at the level of stories delivering value" — rejects agile framing |
| 15 | 2026-04-14T16:26Z | Correction (H12) | App-only behavior verification; "we have struggled to get the LLM not to cheat" |
| 16 | 2026-04-14T17:06Z | Correction (H13) | Distill ceremony mis-calibrated — retro auto-applies without review |
| 17 | 2026-04-14T18:05Z | Correction (H14) | "How did you come to this conclusion?" — demands multi-agent validation for large conclusions (healthy) |
| 18 | 2026-04-14T18:06Z | Interrupt | Second mid-tool interrupt, paired with H14 |
| 19 | 2026-04-14T18:47Z | Decision (H16) | Feature dashboard and story template insufficient; project-level feature dependency graph is worthless |
| 20 | 2026-04-14T18:54Z | Decision (H26) | Judgment Frame as feature concept; human-review section in story template |
| 21 | 2026-04-14T18:59–19:04Z | Decision (H27) | HTML-directory dashboard, drill-down per feature; kill project-level graph |
| 22 | 2026-04-14T19:12Z | Decision (H28) | Spikes as intake stubs with wireframes as committed artifacts |
| 23 | 2026-04-14T19:24Z | Correction (H17) | Distillations underused AND over-ceremonial simultaneously |
| 24 | 2026-04-14T21:59Z | Decision (H20) | Fully-formed distill prompt: e2e-validator Environment Prerequisites section |
| 25 | 2026-04-14T23:17Z | Decision (H21) | Second-level distill: sprint-dev Phase 5 E2E Validator spawn block |

**Pattern across interventions:** Early in the sprint (day 1) the user was reactive — correcting distill jargon, path classification, missing parallelism. Mid-sprint (day 2 early hours) the user pivoted to strategic redesign — features-first, epics-as-DDD, judgment-frame — driving large decisions. Day 2 afternoon/evening the user drove concrete downstream artifacts — dashboard redesign, story template overhaul, E2E validator fixes. The sprint's real output was this decision ladder, not the two merged code stories.

## Story-by-Story Analysis

Note: The sprint's merged code stories were `triage-skill` and `retro-triage-handoff`. Neither produced notable transcript patterns in the audit window — the audit data primarily reflects the retro-for-prior-sprint (2026-04-11) that ran during this window, plus research/decision/distill activity that will seed the next sprint.

### triage-skill

- **Outcome:** Merged. Sprint 2026-04-14 closed 2026-04-15.
- **Transcript patterns:** Not directly observable in this audit window — merge activity predates the bulk of captured messages.
- **Notable:** None.

### retro-triage-handoff

- **Outcome:** Merged. Sprint 2026-04-14 closed 2026-04-15.
- **Transcript patterns:** Not directly observable in this audit window.
- **Notable:** None.

### Retro-for-sprint-2026-04-11 (ran during this window)

- **Outcome:** Produced findings, seeded this sprint's distill work.
- **Iteration count:** Two AVFL iterations on the adapting-agile research corpus (iter1=61/100 POOR, iter2=85/100 NEEDS_FIX, final=81). Slight regression on final score from scoring inconsistency (see S11).
- **Issues:** 60 file-too-large errors on 5 auditor-human agents (see S1 for root cause). 10 SendMessage InputValidationErrors across auditor-human agents (see S10). 4 API stream idle timeouts on corpus-mode validators (see S11). 8 documenter agents 100% parse-failure in extractor (see S9).
- **Net assessment:** Retro produced the findings that drove this sprint's substantial distill work, but the retro itself surfaced three observability gaps (S1, S9, S11) and a schema bug (S10) that would have been invisible without this audit.

### Strategic-redesign activity (session bfac60be)

- **Outcome:** Drove a practice-level redesign: features as first-class value units, epics as DDD domain boundaries, 4 terminal states, Judgment Frame, HTML dashboard.
- **Iteration count:** N/A — conversational decision flow.
- **Issues:** H4 (sequential default), H5 (narrow framing), H9 (failure euphemized), H14 (premature conclusion). All caught by user; none shipped downstream.
- **Notable:** Sprint's highest-value output but invisible in commit log. Decisions feed the next sprint's planning directly.

## Cross-Cutting Patterns

### C1. Agent invariants can be unweakenable — or silently weakened by their caller

Two findings, two levels, same failure mode:
- **S3 (E2E validator):** A correct agent definition gets an escape hatch from its spawn prompt.
- **S1 (retro auditors):** A correctly-distilled agent prompt gets silently replaced by a stale cached version at runtime.

Both are "the agent is not running what you think it's running." Both surface only through behavior audits (this retro). Both argue for a principle: **agent system prompts must be verifiable at spawn time against their source of truth.** Spawn prompts must not weaken agent invariants (S3); runtime prompts must match on-disk prompts (S1).

### C2. Distill skill has multiple simultaneous calibration problems

S1 (runtime invisibility), S4 (path-classification bugs), S5 (jargon), S6 (ceremony mis-calibration). Distill is a high-leverage skill — when it's off, every downstream learning is degraded. Argues for a dedicated distill-skill-hardening epic separate from normal backlog.

### C3. The human-in-loop gate is theatrical when the artifact is unreviewable

S2 (spec fatigue — user self-reports skipping) + H16 (dashboard insufficient) + H27 (project-level graph worthless) all point to the same mechanic: **the human's review surface has not been designed for human reading**. Review gates that present LLM-optimized artifacts are not real gates. User decisions H26/H27/H28 are the direct response: Judgment Frame, HTML dashboard, spike wireframes.

### C4. Quality gates work when structured adversarially and iteratively

W1–W6 all share the pattern: **two or more agents in structured disagreement, with an explicit iteration protocol**. AVFL iter→iter convergence (W1), enumerator→adversary two-pass (W2), parallel lens reviewers (W3), orchestrator→precision-writer separation (W4), iter-N-lists-iter-(N-1)-fixes (W5), challenger/analyst pairing (W6). These are working. Direction: generalize the pattern beyond AVFL (see H7: possible `momentum:analyze` skill).

### C5. Observability of the practice itself has gaps

S9 (documenter extractor 100% fail), S11 (timeout invisibility), plus the fact that this retro had to actively reconstruct a cache-staleness bug from transcript forensics — all indicate the retro's tools are incomplete. Retro quality is bottlenecked on extractor robustness.

### C6. Sprint code output ≠ sprint value output for practice-layer sprints

Two merged code stories. The sprint's real output: a 14-decision strategic redesign, multiple high-signal distill prompts (H20, H21), the cache-staleness root-cause chain, and a feature/epic redesign that sets direction for the next N sprints. This is appropriate for a practice-module project, but it means sprint-health metrics based on code velocity undersell the actual work. Consider practice-output reporting alongside code-output reporting.

## Metrics

| Metric | Value |
|--------|-------|
| User messages analyzed | 146 |
| Subagents analyzed | 106 |
| Tool errors detected | 165 |
| Struggles identified | 13 |
| Successes identified | 10 |
| User interventions | 25 |
| Cross-cutting patterns | 6 |

Additional metrics:
- File-too-large errors (retro auditors) due to stale cache: 60
- SendMessage InputValidationErrors (retro auditors): 10
- API stream idle timeouts (AVFL validators): 4
- Documenter agent parse-failures: 8 of 8 (100%)
- AVFL iter1→iter2 finding reduction: ~120 → ~55 (54% convergence)
- AVFL iter1 score → iter2 score → final: 61 → 85 → 81
- Mid-tool interrupts: 2
- User decisions captured: 8

## Priority Action Items

Ranked by impact and actionability. Each item includes priority and a recommended story stub title.

| # | Priority | Title | Story Stub |
|---|----------|-------|------------|
| 1 | **CRITICAL** | Plugin-cache staleness silently invalidates distills | `fix(impetus): detect plugin-cache version skew and prompt marketplace update before workflow invocation` |
| 2 | **HIGH** | Story template spec fatigue — add Judgment Frame for human review | `feat(skills): story template — Judgment Frame human-review section + LLM-optimized section split` |
| 3 | **HIGH** | E2E validator resilient to orchestrator framing | `fix(skills): e2e-validator Environment Prerequisites + sprint-dev Phase 5 spawn block hardening` |
| 4 | **HIGH** | Distill path-classification keys on scope, not cwd | `fix(skills): distill path-classification decision tree — scope/portability not cwd` |
| 5 | **HIGH** | Distill jargon-without-definition in human-facing output | `fix(skills): distill output defines its own terms before using them; path classification messages inline behavior` |
| 6 | **HIGH** | Feature dashboard redesign — HTML directory with drill-down | `feat(skills): feature-status HTML-directory dashboard with per-feature drill-down; kill project-level dep graph` |
| 7 | **MEDIUM** | Sprint close enforces worktree+branch cleanup (portable shell) | `fix(skills): sprint-dev Phase 7 — mandatory worktree+branch cleanup, macOS-portable commands` |
| 8 | **MEDIUM** | Distill ceremony tiering — lightweight default, retro user-gate | `fix(skills): distill — tier ceremony by origin; retro Tier 1 requires user approval gate` |
| 9 | **MEDIUM** | Research skill parallel Phase-2 + framing confirmation | `fix(skills): research — parallel Phase-2 subagents by default; framing confirmation before question lock` |
| 10 | **MEDIUM** | Documenter transcript extractor robust to Python-repr inputs | `fix(scripts): transcript-query.py parses Python-repr dicts; documenter agents become auditable` |
| 11 | **MEDIUM** | SendMessage ↔ auditor prompt schema alignment | `fix(skills): retro auditor prompts explicitly specify string-containing-JSON format for SendMessage` |
| 12 | **MEDIUM** | AVFL corpus-mode timeout handling + scoring stability | `fix(skills): avfl — surface validator timeouts to consolidator; anchor final scoring to finding delta` |
| 13 | **MEDIUM** | Session identity surface for multi-day work | `feat(skills): impetus — session purpose statement; post-compact "where are we" summary` |
| 14 | **MEDIUM** | Agent avoids offloading discoverable lookups onto user | `fix(rules): skill authoring — local discovery before asking user` |
| 15 | **LOW** | Investigate premature-action pattern on two mid-tool interrupts | `investigate: correlate the two mid-tool interrupt contexts for premature-action pattern on high-blast-radius changes` |
| 16 | **LOW** | Generalize enumerator/adversary beyond AVFL to practice analysis | `spike: momentum:analyze skill — enumerator/adversary multi-lens for non-AVFL practice audits` |

**Recommended sprint-2026-04-17 focus:** Items 1 (critical, unblocks all future distills), 2+3 (high, directly tied to user's decisions), 4+5 (high, distill skill hardening). Items 6/7/8 as stretch. Remaining items as backlog stubs.
