# Sprint Transcript Audit — sprint-2026-05-03

**Retro date:** 2026-05-09
**Sprint completed:** 2026-05-09
**Data analyzed:** 456 user messages | 189 subagents | 238 errors | 83 team messages

## Executive Summary

This sprint produced solid foundational architecture decisions — the canonical Momentum cycle (triage → intake → feature-grooming → epic-grooming → refine → sprint-planning → sprint-dev → retro), the state-in-.momentum vs knowledge-in-KB separation, orchestrator-as-sole-state-writer, and shop-before-build for external skills (Ar9av/obsidian-wiki, kepano/obsidian-skills) — all of which should be preserved and propagated. The AVFL post-merge fix loop converged cleanly in one iteration (~6 minutes wallclock from initial findings to all-green), demonstrating that the post-merge model works when reviewer feedback is structured.

The dominant struggle this sprint is a known but unfixed protocol mismatch: review-quality fan-out agents (e2e-validator, qa-reviewer, dev-fixer) are prompted to use SendMessage but spawned without team membership, causing them to spend hundreds of turns and ~1MB-per-agent transcripts reasoning about a tool they cannot actually call. This single defect dominates sprint token spend and is documented in project memory as a backlog item — fixing it is the highest-leverage action available. Adjacent to this, the cmux skill is stale (tab-vs-pane discipline violated within 7 minutes of correction; --title flag still referenced after removal), and discovery-first behavior is not internalized: developer corrected agents 8+ times for not consulting existing stories, decisions, or skill catalogs before proposing new work.

The third major theme is "done" not being verified. Three independent failure modes confirm this: UI implementations diverged from designs (dashboard end-of-line text missing, colors wrong) and were marked complete; migration work left artifacts behind in _bmad-output; the markdown-formatting-skill story required two dev-fixer follow-on agents (each ~1MB) to clean up after a 222-turn dev-skills pass. Completion verification needs to become a first-class step, not a self-report. Benchmark and bulk-ingest workloads (~25-30% of sprint agent-effort) are also commingled with sprint-story work in the audit corpus, obscuring real throughput metrics.

## What Worked Well

### Canonical Momentum cycle codified
- **Description:** Developer named the cycle (triage → intake → feature-grooming → epic-grooming → refine → sprint-planning → sprint-dev → retro) as a foundational concept this sprint.
- **Evidence:** "OK that looks like a decision. This is a cycle: triage → intake → feature-grooming → epic-grooming → refine → sprint-planning → sprint-dev → retro" (developer)
- **Recommendation:** KEEP — reference in Impetus orientation, dashboard, and skill cross-links.

### State/knowledge separation adopted as architectural constraint
- **Description:** Three paired decisions established the rule: state lives in `.momentum/`; KB is read-shared across all agents; orchestrator is the sole state writer, subagents are pure executors with no state access.
- **Evidence:** "adopt. We've isolated state documents into .momentum and the story is passed in the prompt"; "adopt the owners of state is basically the orchestrator, the agents should have no direct access to the state"; "adopt knowledge is open to all agents and optimized for quick access"
- **Recommendation:** KEEP — promote to a global rule; should drive future skill design and audits of any skill that writes state from a subagent.

### Shop-before-build validated for KB capabilities
- **Description:** Adopting external skills (Ar9av/obsidian-wiki, kepano/obsidian-skills) avoided rebuilding capabilities that already had provenance support built in.
- **Evidence:** "I think they did a great job, better even then my plans even having the concept of provenance already built in. And this means we don't need to build it ourselves."
- **Recommendation:** KEEP — apply this lens proactively in feature-grooming and epic-grooming.

### AVFL post-merge fix loop converged in one iteration
- **Description:** Initial E2E verification (4 PASS / 1 FAIL / 1 CANNOT_VERIFY) → two parallel-ish dev-fixer commits (5591d49, 3ba4979) → final E2E PASS. Total wallclock: ~6 minutes. No thrash, no rework.
- **Evidence:** team-messages timestamped sequence 02:10:07 → 02:16:23. CR-001 (3 EDD eval files), M-001 (SDR acronyms), M-002 (terminal headers), and the missing GATE_FAILED blockquote all closed in one round.
- **Recommendation:** KEEP — this is the success case for the AVFL post-merge model. Document as canonical.

### TeamCreate research with parallel WebSearch + post-hoc synthesis
- **Description:** May 3 06:54-07:18 TeamCreate research used 5 parallel research agents writing distinct files to `_bmad-output/research/teamcreate-real-world-usage-2026-05-02/raw/`, then a final synthesizer consolidated to `final/`. No agent-to-agent SendMessage during research.
- **Evidence:** team-messages L5-L52; research output itself validated the fan-out (not TeamCreate) decision rule.
- **Recommendation:** KEEP — pure parallel write to shared dir + post-hoc consolidation is the canonical research shape.

### Single-turn consolidator pattern is correct
- **Description:** Three AVFL/team-review consolidator agents executed in exactly 1 turn each, receiving structured findings from N validators and emitting a single consolidated structured response.
- **Evidence:** agent-a65c72591b (1 turn, quality-consolidator for quick-fix story plan); agent-aee46e1319f (1 turn, story spec); agent-a163cbe7f6 (1 turn, sprint implementation).
- **Recommendation:** KEEP — single-turn consolidators are the goal shape for aggregator nodes. Document explicitly so future audits don't mistake them for abandoned agents.

### Feature-grooming produced high-precision classification
- **Description:** Feature-grooming agent (composable-specialist-agents feature) analyzed 27/30 stories, correctly distinguished strong duplicates (none) from thematic overlap (named pair: build-guidelines-skill ↔ constitutionmd-generation-acceptance-criteria), enumerated 24 unmapped backlog stories with affinity reasoning.
- **Evidence:** agent-a1d5db4dbb42ecfc4, agent-aaffe81e7fc6ceb23 in team-messages L1-L4.
- **Recommendation:** KEEP — grooming workflow precision is high; reuse the prompt structure.

### Dev-fixer correctly identified pre-existing-correct findings
- **Description:** Dev-fixer explicitly verified that 3 H-tier findings (H-001 blockquote overuse across 10 files, H-002 plan-audit parenthetical, H-003 distill/intake multi-H2) were already correct in the source and did not over-edit.
- **Evidence:** team-messages L62 dev-fixer summary.
- **Recommendation:** KEEP — verification step in dev-fixer prevents speculative edits. Bake into dev-fixer prompt as a required step.

## What Struggled

### Fan-out reviewers prompted to use SendMessage they cannot call
- **Description:** e2e-validator, qa-reviewer, and dev-fixer agents are prompted to deliver findings via SendMessage to documenter/team-lead, but spawned in fan-out mode without team membership. Agents repeatedly run `ToolSearch select:SendMessage` (sometimes per-turn), eventually reason that SendMessage is unavailable, then fall back to text response.
- **Evidence:** L168 e2e-validator (529KB, 200 turns) last_response: "I need to use ToolSearch to load SendMessage before calling it. However, I do not have ToolSearch available as a tool in this session." L185 qa-reviewer cites project memory "Fan-Out Agent Prompt Fix — Return Report as Final Response, Not SendMessage (backlog)". 6 identical ToolSearch(select:SendMessage) calls within 90 seconds across 5 agents (team-messages L53,L59-L74).
- **Root cause:** Known protocol mismatch documented in project memory but not yet fixed. Reviewer prompts assume team-spawned context; spawn reality is fan-out.
- **Recommendation:** FIX — highest-leverage. Two acceptable resolutions: (a) spawn reviewers via TeamCreate so SendMessage works, OR (b) rewrite reviewer prompts to drop SendMessage and require structured-text final response. Option (b) aligns with the existing "Fan-Out Agent Prompt Fix" memory.

### e2e-validator JSONL writer produces unparseable transcripts
- **Description:** 3 e2e-validator agents (combined ~1.4MB) and 1 dev-fixer (1.2MB) recorded as 0 assistant turns / 0 tools because their transcripts are written using Python `repr()` (single-quoted dicts) instead of `json.dumps()`. Audit cannot recover content.
- **Evidence:** parse_error "Malformed JSON at byte 1: unexpected character. Input: {matches: NULL, query: NULL, total_deferre..." across agents a27bde18d8061defb (503KB), aa258e57d41079019 (427KB), ae6f0f50bd131e836 (546KB), ae176c85cb161c40e (1218KB).
- **Root cause:** JSONL writer for e2e-validator uses Python dict repr, not json.dumps with `default=str`.
- **Recommendation:** FIX — patch the writer to use `json.dumps(obj, default=str)`. Investigate the 1.2MB dev-fixer separately (may be a distinct empty-prompt failure).

### cmux discipline violated repeatedly within minutes of correction
- **Description:** Agent created new splits/panes for markdown viewers despite a documented memory rule and global rule mandating tabs in the existing viewer pane. Same correction issued twice in ~7 minutes.
- **Evidence:** "A and PLEASE open them in new tabs NOT in new surface/pane"; 7 minutes later: "You're still not opening them in tabs but in new surfaces or panes. Please open them in tabs in the future."
- **Root cause:** Rules are written but not consulted at the decision point (before issuing cmux markdown/browser commands). Compounds with auditor-execution's finding that cmux skill docs still reference the removed `--title` flag.
- **Recommendation:** FIX — (a) update cmux skill docs to remove `--title`; (b) add a pre-flight check or skill-side reminder before any cmux markdown/browser open command verifies the existing viewer surface ref is reused; (c) consider a hook that intercepts `cmux markdown open` / `cmux browser open` without `--surface` and prompts.

### Wiki ingest fanned out one-agent-per-URL
- **Description:** 11 separate wiki-ingest agents ran against Kotlin/CMP doc URLs (3.4MB of transcript, 796 turns, 585 tools, 5-6 errors per agent). Each reloaded SKILL.md and per-agent context. Highest error concentration of any cluster in the sprint.
- **Evidence:** 9 agents share identical first prompt prefix; agents a123dd7a/a20925119c/a386409c8/a61b806d4/a70c0b505 with 73-94 turns each.
- **Root cause:** Operator manually fanned out a long URL list across separate invocations rather than using a batch mode.
- **Recommendation:** FIX — wiki-ingest needs a batch mode: one agent processes a URL list with bounded concurrency, sharing index/raw-state writes. Update practice guidance: never spawn one agent per URL for ingestion.

### momentum:intake invoked via three different prompt templates
- **Description:** 12 intake agents fragmented into 3 distinct prompt phrasings ("You are running momentum:intake. Base skill directory:..." / "Run momentum:intake for the following story idea..." / "Run momentum:intake to capture a backlog stub..."). All 12 had errors=1 — uniform failure.
- **Evidence:** auditor-execution finding #3.
- **Root cause:** Three different callers (orchestrator skills or impetus contexts) invoke intake via three different templates. Uniform errors=1 suggests an intake-internal step that always fails (likely a duckdb query against intake-queue.jsonl or stories/index.json).
- **Recommendation:** FIX — (a) consolidate intake invocation into a single template, (b) investigate and fix the uniform errors=1 in the intake skill itself.

### UI implementations diverged from designs and were marked done
- **Description:** Dashboard implementation missed end-of-line text from the design, colors were wrong, layout off. Same dashboard quality issue resurfaced after a fix attempt.
- **Evidence:** "None of the end of line text that is in the design show up. Why wasn't the css followed strictly?" "Dashboard and stories still not working. Also the look of the actual features is not right."
- **Root cause:** Implementing agent did not validate against the design source before reporting done. Confirms the CLAUDE.md mandate "if you can't test the UI, say so explicitly" is not being followed.
- **Recommendation:** FIX — UI stories must include a design-comparison step in their dev workflow that produces a side-by-side or design-diff artifact before marking complete.

### Migration and ingest "completion" not verified against source list
- **Description:** Two parallel cases: BMAD migration declared complete with artifacts left behind in `_bmad-output/`; KB ingest reported success but coverage was incomplete (compose, compose-multiplatform docs missing).
- **Evidence:** "I thought we had already migrated them. please /intake a story for migrating decisions. Is there ANYTHING ELSE in _bmad-output?" "How could the KB possibly be missing so much? I thought we imported everything based on our libraries."
- **Root cause:** "Done" criteria is a self-report, not a coverage check.
- **Recommendation:** FIX — migration and ingest skills must produce a coverage report (source list vs ingested list, residual file count) as part of the completion artifact.

### Story decomposition signal: 222-turn ceiling needs follow-on fixers
- **Description:** markdown-formatting-skill-output-templates story spawned one dev-skills agent at 222 turns / 940KB / 4 errors, then required TWO separate dev-fixer follow-on agents (140 turns / 1175KB and 133 turns / 1051KB) to finish the work.
- **Evidence:** auditor-execution finding #5 (agents adf8714, ace0b67, ab9ee53). Last response: "Files modified (18)" — touching 18 skill workflow.md files in one agent.
- **Root cause:** Story scope (touch 18 skill files) exceeded what a single dev-skills agent could complete in one pass. No checkpoint or split mechanism kicked in.
- **Recommendation:** UPSTREAM-FIX — refine should flag stories that cross-cut N skills/files as candidates for decomposition or scripted transformation. Investigate a turn-count circuit breaker (~100 turns) that forces an explicit checkpoint or split.

### TeamCreate misused in retro skill itself
- **Description:** Developer flagged that the retro skill uses TeamCreate where simple fan-out would have worked, violating the spawning-patterns.md decision rule.
- **Evidence:** "It does but this is a horrible use of TeamCreate. Can you just make sure we have a story to remove that team create?" "I thought we already had a story for removing TeamCreate from the retro. Please look into that before creating a new one."
- **Root cause:** spawning-patterns.md rule not consulted during skill design.
- **Recommendation:** FIX — story already exists per developer note; ensure it's prioritized. Audit other skills for TeamCreate misuse.

### Benchmark agents inflate sprint metrics
- **Description:** ~25-30% of sprint agent-effort went to non-sprint-story work (campaign-init benchmark + wiki KB ingestion). 13 agents touched campaign-init-screen-integration as a controlled benchmark experiment, but they share the audit corpus with real story work and obscure throughput metrics.
- **Evidence:** auditor-execution finding #4. campaign-init story has explicit "fresh implementation, ignore status:done" prompts indicating benchmark intent. Untracked `.momentum/handoffs/multi-model-skill-benchmark-2026-05-09.md` confirms benchmark workflow.
- **Recommendation:** INVESTIGATE — does Momentum need a way to tag agent runs by purpose (sprint-story / benchmark / ingest / exploratory) so retro metrics reflect actual sprint throughput?

### Per-turn ToolSearch ritual loading inflates cost
- **Description:** Reviewer agents repeat `ToolSearch select:SendMessage` at every turn boundary instead of caching the loaded schema. 5 agents × ~3 turns each = 15+ redundant tool round-trips in 90 seconds.
- **Evidence:** team-messages L53,L59,L60,L61,L65,L66,L67,L68,L73,L74.
- **Root cause:** Agent prompts don't instruct "load once at session start, not before every send"; schema persistence in-session not communicated.
- **Recommendation:** FIX — once SendMessage protocol mismatch is resolved, this disappears. If it persists, add explicit "load once at session start" guidance to agent prompts.

### Token-limit / large-file Read errors persist
- **Description:** 27 token-limit-exceeded errors from agents attempting full Read of stories/index.json, prd.md, transcripts (25k token cap exceeded).
- **Evidence:** auditor-execution finding #6. Large-file protocol exists (wc -l + chunked Read) but not enforced in agent prompts.
- **Recommendation:** FIX — propagate large-file protocol to all dev/Explore agent prompts via the agent constitution or shared rules.

### Worktree git path errors
- **Description:** 14 git-fatal errors from agents operating on absolute paths that escape worktree boundaries ("main is already checked out at...", "is outside repository").
- **Evidence:** auditor-execution finding #6.
- **Recommendation:** FIX — audit worktree-aware paths in dev/dev-skills agent prompts; use repo-relative paths inside worktrees.

### Skill discoverability/routing
- **Description:** Developer redirected agent to use the right skill name ("Actually I think this would make more sense as /momentum:feature-grooming, right?"). Agent picked the wrong skill for a grooming task.
- **Recommendation:** INVESTIGATE — is this a skill description trigger problem, or an Impetus routing problem? Quick analysis: are skill descriptions distinct enough that an agent picks the right one without developer intervention?

### Decision-to-implementation gap
- **Description:** Decisions captured in prior sessions ("move all our project knowledge into the KB with a different sub-directory") were not implemented or surfaced as backlog work.
- **Evidence:** "we had a plan, which I'm not sure we implemented... Do you see it there in the KB? Are we using it at all?"
- **Recommendation:** INVESTIGATE — decision skill should produce backlog stubs automatically when a decision implies implementation work.

### Retro skill ran but didn't produce expected artifact
- **Description:** Developer noted the prior retro ran but no findings document was written.
- **Evidence:** "I thought I just did the retro... Why didn't it write it? Do we need to fix that?"
- **Recommendation:** INVESTIGATE — confirm retro completion-output gap; this audit may already be resolving it via the documenter pattern.

### Bulk-approve flow risks over-approving
- **Description:** Developer reversed an A&A&A bulk approval to insist on splitting before approval.
- **Evidence:** "Actually I'd like you to split it and then confirm"
- **Recommendation:** INVESTIGATE — bulk-approve UX may need a "split first?" prompt for batches above N items.

### Handoff file placement inconsistent
- **Description:** Handoff written to wrong directory; developer had to reason from first principles ("Why wouldn't momentum handoffs be in the same place as nornspun handoffs? And wouldn't it make sense for them to be in .session?").
- **Recommendation:** FIX — codify handoff location convention (`.momentum/handoffs/` per recent commit e787182) and propagate the pattern to other projects' rules.

### Agent reports work without surfacing git persistence state
- **Description:** Developer had to ask whether commit/push actually happened.
- **Evidence:** "Did you commit and push?"
- **Recommendation:** FIX — completion reports must include git state (commit SHA, push status, branch).

## User Interventions

| # | Quote (excerpt) | Type | Implication |
|---|---|---|---|
| 1 | "open them in new tabs NOT in new surface/pane" | correction | cmux discipline violation; rule not consulted before action |
| 2 | "You're still not opening them in tabs but in new surfaces" | correction | Same rule violated again ~7 min later |
| 3 | "NOOOOO....we already have those results" | frustration | Re-ran existing benchmark; no artifact inventory |
| 4 | "Wait... showing me the OPPOSITE of what I thought I saw before" | frustration | Inconsistent benchmark summaries; trust collapse |
| 5 | "It's silly you ask me. Do your own discovery" | frustration | Agent asking for discoverable facts |
| 6 | "None of the end of line text that is in the design show up" | correction | Dashboard diverged from design; not verified before "done" |
| 7 | "Dashboard and stories still not working" | correction | Same UI quality issue after fix attempt |
| 8 | "I thought we already had a story for removing TeamCreate" | correction | No backlog search before story create |
| 9 | "take a comprehensive look at the feature(s)/stories we already have" | correction | Discovery-first not internalized |
| 10 | "horrible use of TeamCreate" | correction | spawning-patterns.md violated in skill |
| 11 | "I don't see the roles that would cover every single subagent call" | correction | Coverage analysis incomplete |
| 12 | "Did you commit and push?" | correction | Git state not surfaced in reports |
| 13 | "Why didn't it write it? Do we need to fix that?" | correction | Retro skill output gap |
| 14 | "Do you see it there in the KB? Are we using it at all?" | correction | Decision-to-implementation gap |
| 15 | "Actually I think this would make more sense as /momentum:feature-grooming" | redirection | Skill routing issue |
| 16 | "Actually I'd like you to split it and then confirm" | redirection | Bulk-approve UX risk |
| 17 | "I thought we had already migrated them" | frustration | Migration "done" not verified |
| 18 | "How could the KB possibly be missing so much?" | frustration | Ingest "done" not verified |
| 19 | "Why wouldn't momentum handoffs be in the same place as nornspun handoffs?" | correction | Handoff convention not enforced |

## Story-by-Story Analysis

### markdown-formatting-skill-output-templates (quick-fix)
- **Agents:** 1 dev-skills (222 turns / 940KB / 4 errors) + 2 dev-fixers (140 turns / 1175KB; 133 turns / 1051KB)
- **Iteration count:** 3 large agents totaling ~3.2MB
- **Pattern:** Story scope (18 skill workflow.md files) exceeded single-agent capacity; required two follow-on cleanup passes.
- **Issue:** No turn-count circuit breaker; refine didn't flag this as a decomposition candidate.

### Quick-fix workflow E2E verification
- **Agents:** Initial e2e-validator (PASS 4/FAIL 1/CANNOT_VERIFY 1) → 2 dev-fixer commits (5591d49, 3ba4979) → final e2e-validator (PASS all)
- **Iteration count:** 1 fix iteration, ~6 min wallclock
- **Pattern:** Clean AVFL post-merge convergence — model works.

### campaign-init-screen-integration (benchmark)
- **Agents:** 13 (9 implementation × 5 prompt phrasings + 4 avfl-3lens validators)
- **Iteration count:** N/A — controlled benchmark, not real iteration
- **Pattern:** Benchmark fixture for multi-model/multi-skill comparison (bmad-dev-story / compose-expert / frontend-dev / no-skill). Not a story problem; a metrics/tagging problem.

### Wiki ingest cluster (Kotlin/CMP docs)
- **Agents:** 11 wiki-ingest agents
- **Iteration count:** 1 per URL; should have been 1 batch
- **Pattern:** One-agent-per-URL fan-out anti-pattern. Highest error concentration in the sprint.

### momentum:intake cluster
- **Agents:** 12 intake invocations across 3 prompt templates
- **Iteration count:** 1 each, all errors=1
- **Pattern:** Fragmented invocation; uniform internal failure.

### Canvas SKILL.md (qa-reviewed)
- **Agents:** qa-reviewer (435KB / 79 turns / 4 errors) → fix → re-validation (16KB / 8 turns)
- **Iteration count:** 1 fix
- **Pattern:** Real catches (model frontmatter violation, description length, status bookkeeping) cleanly closed.

## Cross-Cutting Patterns

### 1. Discovery-first behavior is not internalized (HIGH)
Appears in: human (8+ corrections about consulting existing stories/decisions/skills), execution (intake invocation fragmentation), review (false-positive H-tier findings flagging non-existent issues). Agents do not reliably verify against current state before acting — whether the state is the backlog, the source files, or prior decisions.

### 2. "Done" is self-reported, not verified (HIGH)
Appears in: human (UI fidelity gap × 2, migration leftovers, KB ingest gaps), execution (markdown-formatting story needs 2 dev-fixer follow-ons after 222-turn pass), review (e2e-validator catches missed blockquote). System-wide pattern: completion lacks a verification artifact.

### 3. Reviewer agent protocol breakdown (HIGH)
Appears in: review (#1 finding — fan-out reviewers prompted to use SendMessage they cannot call), execution (127 "other" errors include the bash exit-1 ToolSearch retries; ritual per-turn ToolSearch loading). Single highest-leverage fix in the sprint — cascades into token waste, transcript bloat, audit difficulty.

### 4. Long-running agents accumulate errors and need decomposition (MEDIUM)
Appears in: execution (top-error agents are top-turn agents; 222-turn dev-skills + 200-turn e2e-validator), review (200-turn e2e-validator inflated by SendMessage protocol overhead). No turn-count circuit breaker; no errors-per-turn ratio metric.

### 5. cmux skill staleness (MEDIUM)
Appears in: human (tab-vs-pane violations), execution (cmux --title flag drift). Skill instructions don't match current cmux behavior; rules don't get consulted at decision points.

### 6. Benchmark/ingest workloads commingled with sprint work (MEDIUM)
Appears in: human (benchmark frustration), execution (campaign-init + wiki ingest = ~25-30% of sprint agent-effort, no purpose tagging). Real sprint capacity obscured.

### 7. Architectural decisions strong, propagation weak (LOW)
Appears in: human (multiple high-quality "adopt" decisions captured), human (decision-to-implementation gap noted by developer). Decisions are being made well but not consistently turned into backlog work.

## Metrics

| Metric | Value |
|--------|-------|
| User messages analyzed | 456 |
| Subagents analyzed | 189 |
| Tool errors detected | 238 |
| Struggles identified | 19 |
| Successes identified | 8 |
| User interventions | 19 |
| Cross-cutting patterns | 7 |

## Priority Action Items

| Rank | Item | Priority | Recommended Story Stub Title |
|---|---|---|---|
| 1 | Fix fan-out reviewer SendMessage protocol mismatch (rewrite prompts to return structured-text final response, OR spawn via TeamCreate) | critical | fix-fan-out-reviewer-sendmessage-protocol |
| 2 | Patch e2e-validator JSONL writer to use json.dumps(default=str) | critical | fix-e2e-validator-jsonl-serialization |
| 3 | Add design-comparison step to UI story dev workflow before "done" | high | enforce-ui-design-verification-before-done |
| 4 | Migration/ingest skills must produce coverage report (source vs ingested) before "done" | high | enforce-migration-ingest-coverage-reports |
| 5 | wiki-ingest needs batch mode; deprecate one-agent-per-URL pattern | high | wiki-ingest-batch-mode |
| 6 | Update cmux skill docs (remove --title flag) and add pre-flight tab-vs-pane check | high | refresh-cmux-skill-docs-and-preflight |
| 7 | Consolidate momentum:intake invocation prompts into single template; investigate uniform errors=1 | high | consolidate-intake-invocation-and-fix-error |
| 8 | Remove TeamCreate misuse from retro skill (story already exists per developer) | high | remove-teamcreate-from-retro-skill |
| 9 | Enforce large-file Read protocol (wc -l + chunked) in dev/Explore agent prompts | high | enforce-large-file-read-protocol |
| 10 | Audit worktree path handling in dev/dev-skills agent prompts | medium | fix-worktree-absolute-path-errors |
| 11 | Add agent-run purpose tagging (sprint-story / benchmark / ingest / exploratory) for audit filtering | medium | tag-agent-runs-by-purpose |
| 12 | Add turn-count circuit breaker (~100 turns) requiring explicit checkpoint or split | medium | turn-count-circuit-breaker |
| 13 | Track errors-per-10-turns ratio as a decomposition signal in audits | medium | errors-per-turn-ratio-metric |
| 14 | Completion reports must surface git state (commit SHA, push status, branch) | medium | require-git-state-in-completion-reports |
| 15 | Decision skill should auto-create backlog stubs for decisions implying implementation | medium | decision-to-backlog-auto-stub |
| 16 | Codify handoff location convention (.momentum/handoffs/) and propagate cross-project | medium | handoff-location-convention |
| 17 | Investigate skill discoverability/routing — are descriptions distinct enough? | medium | audit-skill-description-routing |
| 18 | Investigate retro completion-output gap (artifact not written) | medium | retro-completion-artifact-verification |
| 19 | Investigate bulk-approve UX — prompt to split for batches above N items | low | bulk-approve-split-prompt |
| 20 | Investigate L98 dev-fixer 1218KB / 0-turn anomaly (parse vs genuine zero-output) | low | investigate-zero-turn-fixer-anomaly |
| 21 | Document single-turn consolidator pattern as canonical in AVFL/team-review skills | low | document-single-turn-consolidator-pattern |
| 22 | Document AVFL post-merge one-iteration convergence as canonical success case | low | document-avfl-post-merge-convergence |
| 23 | Reviewer prompt fix: verify finding exists in source before flagging (reduce H-tier false-positive rate ~50%) | medium | reviewer-verify-before-flag |
| 24 | Audit other skills for TeamCreate misuse (use spawning-patterns.md decision rule) | medium | audit-skills-for-teamcreate-misuse |
