# Momentum Upstream Intake — nornspun sprint-2026-04-10 Retrospective
**Source project:** nornspun  
**Retro date:** 2026-04-12  
**Sprint:** sprint-2026-04-10 (completed 2026-04-11) + quick-fix consolidate-shared-ui-viewmodels  
**Intake iteration:** 1  
**Prepared by:** retro skill (automated transcript audit + documenter synthesis)  

---

## How to Use This Document

This document captures 10 upstream improvement opportunities identified during a retrospective transcript audit of nornspun sprint-2026-04-10. All items were classified as Momentum-owned: every symptom traces to a gap in a Momentum skill, workflow, or orchestration behavior — not a nornspun project defect.

Each finding includes quantitative evidence, verbatim user quotes, root cause analysis, and a recommended fix scope. The Momentum team can triage and action these without accessing nornspun session logs directly.

**Sprint data summary:**
- 131 user messages across 3 sessions
- 57 subagents spawned
- 238 tool errors (file-too-large: 106, exit-code-nonzero: ~80, other: ~52)
- 123 inter-agent team messages
- Sprint stories: fix-api-connection, desktop-m3-migration, shared-ui-consolidation
- Quick-fix: consolidate-shared-ui-viewmodels (InMemoryAppPrefs classpath + HTTP/2 ktor engine swap)

**Scope note:** The audit corpus spans sprint-2026-04-08 execution + sprint-2026-04-10 planning. Sprint-2026-04-10 dev execution (the three story dev waves, AVFL, QA/E2E review) ran outside the extract window. Items #1–#5 are confirmed from corpus evidence; #6–#10 supplement with retro-session observation and prior-retro context. This window misalignment is itself item #8.

**Dedup note:** Items from `nornspun-2026-04-10-1-retro.md` (sprint-04-08) and `nornspun-2026-04-10-2-retro.md` (sprint-04-06/D3) are not repeated. Items below are new to this retro, except #1 (`retro-team-singleton-guard`) which was raised as RV-05 in the sprint-04-08 retro and was **not actioned** — it escalated from 5× to 10× duplicate documenters between retros.

---

## Issue Index

| # | ID | Priority | Skill/Component Affected |
|---|-----|----------|--------------------------|
| 1 | `retro-team-singleton-guard` | **Critical** | momentum:retro — team-assemble step |
| 2 | `agent-state-verification-hook` | **Critical** | All dev/E2E skills, cmux enforcement |
| 3 | `retro-to-planning-pipeline` | **High** | momentum:retro + momentum:sprint-planning |
| 4 | `retro-upstream-classifier` | **High** | momentum:retro — findings routing |
| 5 | `sprint-planning-investigate-first` | **High** | momentum:sprint-planning — diagnostic behavior |
| 6 | `retro-and-planning-UX-defaults` | **Medium** | momentum:retro + momentum:sprint-planning |
| 7 | `retro-transcript-discovery` | **Medium** | momentum:retro — preprocessing step |
| 8 | `retro-window-alignment` | **Medium** | momentum:retro — transcript-query date range |
| 9 | `qa-reviewer-prompt-conditionalize` | **Low** | momentum:qa-reviewer skill prompt |
| 10 | `large-file-read-strategy` | **Low** | Documenter/auditor/spec-impact agent prompts |

---

## Issues

---

### Issue 1 — `retro-team-singleton-guard`
**Priority:** Critical  
**Skill/Component:** momentum:retro — team-assemble step  
**First raised:** sprint-04-08 retro as RV-05 (not actioned — escalated)

#### What happened
The retro skill's TeamCreate step spawns duplicate singleton roles: one documenter and one auditor-review was intended; multiple were spawned. This has occurred in every retro and is escalating:

- sprint-04-08 retro (2026-04-10): 5× documenter spawned, 1 productive, 4 consuming tokens waiting for SendMessage findings that never arrived. Also 2× auditor-review.
- sprint-04-10 retro (2026-04-12, **currently running**): 10× documenter spawned, 1 productive (agent `a152e61f7b2d96295`), 9 idle. Also 3× auditor-review, 2× auditor-human, 2× auditor-execution — 17 total agents for an intended team of 4.

The sprint-04-08 retro flagged this pattern explicitly (RV-05) and produced a story stub. The fix never landed. The multiplier grew from 5× to 10× in one retro interval.

#### Evidence
From the sprint-04-08 retro's auditor-execution, on the current run:
> *"The prior sprint retro (sprint-2026-04-08) spawned exactly 10 agents (5 documenters + 2 auditor-reviews + 3 unique auditors). 6 of the 10 were surplus... The same bug is occurring in the current retro: 17 agents spawned for a 4-agent team."*

One surplus documenter from the sprint-04-08 retro noted in its own thinking:
> *"duplication is an orchestration bug where the lead spawned the same..."* (agent a26c7b310f8072c64)

RV-05 from the sprint-04-08 retro intake went unactioned.

#### Root cause hypothesis
The retro skill's team-assemble step may be accumulating prior teammate records into a new spawn count, or a misconfigured loop is duplicating singleton roles (documenter + auditor-review are the most duplicated, while the three distinct auditor types are duplicated less). The multiplier escalating between retros suggests a state-accumulation or loop-count bug rather than a fixed off-by-one.

#### Recommended fix
1. Add singleton guard to retro team-assemble step: assert exactly 1 documenter and exactly 3 auditors before proceeding. If count > expected, halt and report the count before spawning.
2. Add a test asserting the retro produces exactly 4 agents (3 auditors + 1 documenter) for any sprint input.
3. Audit why RV-05 from the prior retro went unactioned — the retro→action-item handoff may itself be broken (see issue #3).
4. **Same-day priority**: this is burning tokens in every retro run.

---

### Issue 2 — `agent-state-verification-hook`
**Priority:** Critical  
**Skill/Component:** All dev/E2E skills — post-action state verification  

#### What happened
Agents repeatedly claimed app, process, or build state without verifying that the running system had actually picked up the change. UI changes were declared "live" without relaunching. Desktop launch failures went unnoticed. E2E validation was claimed complete without a visible cmux pane. Android was declared "showing the new UI" without reinstalling the APK.

#### Evidence
From the sprint-04-08 execution corpus (motivating sprint-04-10's stories):

> *"Where is the E2E? I didn't see the cmux pane/surface"* (HF-04, 2026-04-09T19:47) — E2E claimed success without running in a visible pane.

> *"IT LOOKS LIKE DESktop failed? Can you look into it?"* (HF-06, 2026-04-09T21:37) — caps-lock frustration. Desktop launch failed silently; agent didn't notice.

> *"I think you need to shut it off and restart"* / *"I didn't see the android re-launch"* (HF-07, 2026-04-09T22:14–22:40) — user had to say this three times before the agent acted.

> *"I'm seeing Verdandi coming soon when I click. Is that the latest? / The build is done. Are you not seeing this?"* (HF-19, 2026-04-09T21:27–21:29) — agent's model of the running app diverged from the user's live observation.

From sprint-04-10 verification (outside corpus, from session context): after the desktop connection fix was merged, I initially checked backend logs rather than killing and relaunching the app — same pattern.

The `cmux.md` "Visible to the Developer" principle and GUI-launch checklist already encode the correct behavior. This is a compliance gap, not a knowledge gap.

#### Root cause
Post-action verification is optional in current dev/E2E skill prompts. Agents assert claimed state based on their execution trace, not on observed process output. The cmux rules exist but carry no enforcement weight in skill prompts.

#### Recommended fix
1. **E2E**: Require `surface:N` reference in E2E output — if absent, the step did not run. Make this a hard validation in the sprint-dev review phase.
2. **Dev / desktop launch**: After a build or UI change, require explicit kill + relaunch + process verification sequence (pgrep, cmux capture-pane, version marker or visible indicator in output) before declaring the change live.
3. **Android**: After APK build, `installDebug` is required before claiming "Android has the new UI." Explicitly call this out in the dev-frontend skill for any Android-affecting story.
4. Optionally: encode a post-action verification checklist as a hook that fires after dev agent completion — checks for surface refs if E2E was claimed, and process refs if a GUI was launched.

---

### Issue 3 — `retro-to-planning-pipeline`
**Priority:** High  
**Skill/Component:** momentum:retro + momentum:sprint-planning — inter-skill handoff  

#### What happened
The sprint-04-10 planning session started without consuming the sprint-04-08 retro findings. The user had to manually inject the three largest known gaps — Material 3 inconsistency, API stub status, and iOS coverage — before planning could proceed. Retro outputs do not automatically feed the next sprint's backlog-synthesis step.

#### Evidence
> *"Was the M3 migration captured in stories?"* (HF-01, 2026-04-11T05:31) — user checking whether the prior retro's top visual-bug finding was in the backlog.

> *"Nooo...don't we need to add M3 stories? Also, what about ios? And last I checked we're STILL not hooked into the API, it's just stubbed"* (HF-03, 2026-04-11T05:36) — user had to halt planning to inject all three.

The sprint-04-06 (D3) retro explicitly surfaced M3 inconsistency as a major user-visible problem. The sprint-04-08 retro ran on 2026-04-10. Sprint-04-10 planning also ran on 2026-04-10, the same day — the retro findings were not available to planning.

#### Root cause
The retro and sprint-planning skills have no shared state. Planning's backlog-synthesis step reads `stories/index.json` and accepts user prompts; it does not read prior retro findings, cross-platform coverage gaps, or recent user-stated complaints. The handoff is entirely manual.

#### Recommended fix
1. **Sprint-planning skill**: Add a "prior retro check" step at the start of backlog-synthesis. Read `_bmad-output/implementation-artifacts/sprints/*/retro-transcript-audit.md` for the most recent un-actioned retro. Surface its priority action items as candidate stories before generating new ones.
2. **Planning must enumerate before selecting**: before proposing story candidates, planning should enumerate: (a) unaddressed prior-retro findings, (b) cross-platform coverage gaps (Android/Desktop/iOS parity), (c) any issue the user raised in recent sessions that has no story. Only then generate from the backlog.
3. **Retro skill**: At sprint closure (Phase 6), write a machine-readable `retro-summary.json` alongside the audit markdown. Planning can read this without parsing the full narrative. Fields: `priority_action_items[]`, `unaddressed_platform_gaps[]`, `user_stated_complaints[]`.

---

### Issue 4 — `retro-upstream-classifier`
**Priority:** High  
**Skill/Component:** momentum:retro — findings routing and Phase 5 output  

#### What happened
The retro skill has no explicit step to classify findings as upstream-Momentum vs project-specific before producing output. During the sprint-04-06 retro, the agent was about to file a Momentum workflow finding as a nornspun story stub until the user corrected it. The same manual correction was needed in this retro.

#### Evidence
> *"But this isn't a nornspun issue either. The retro is a momentum skill"* (HF-10, 2026-04-11T02:32)

> *"Add them to Momentum, nothing here for Nornspun I think unless it's specific to guidance."* (HF-11, 2026-04-11T04:44)

> *"Please have this document be very detailed so that momentum doesn't have to go search the logs itself, so for example, the document could include user comments, or say that out of X number of calls in the logs Y number of errors were thrown."* (HF-12, 2026-04-10T15:48)

The user has a clear and consistent heuristic: workflow/agent/skill findings default to Momentum upstream. The retro skill does not encode this heuristic, so the classification is manual every retro.

#### Root cause
Retro Phase 5 (story stub creation) has no upstream/downstream classifier step. All findings feed the same stub-creation path, and the agent must infer routing from context.

#### Recommended fix
Add an explicit Phase 4.5 (or sub-step in Phase 5) to the retro skill:

```
For each priority action item, classify before routing:
  - Upstream-Momentum: any finding where the root cause is in a Momentum skill 
    prompt, workflow step, agent behavior, or orchestration mechanism.
    Route → write to ~/projects/momentum/docs/intake/ with full evidence.
    
  - Project-specific: findings where the root cause is in project code, 
    project-specific rules, or content unique to the project.
    Route → story stub in stories/index.json.
    
Default when ambiguous: upstream-Momentum.
```

The intake document should be self-contained with full evidence (user quotes, error counts, turn counts) so Momentum doesn't need to search the session logs. See HF-12.

---

### Issue 5 — `sprint-planning-investigate-first`
**Priority:** High  
**Skill/Component:** momentum:sprint-planning — diagnostic behavior before user asks  

#### What happened
During sprint-04-10 planning, the agent asked the user to triage API stub status among multiple-choice options the agent could have answered by reading the client code. This is the "ask-before-looking" anti-pattern.

#### Evidence
> *"I hate when you ask me this without doing a bit of research: 2. API stub — what specifically is still stubbed? Is it: - The SSE streaming connection? ... I don't know, but it just returns a scripted speech every time I send a message."* (HF-02, 2026-04-11T05:41)

The user's "I don't know, but it just returns a scripted speech" is itself diagnostic — the answer was observable behavior, not architectural knowledge. A grep of `NornApiClient.kt` for `TODO` or `stub` would have answered the question directly.

#### Root cause
Sprint-planning skill doesn't encode a "look before asking" rule for diagnostic questions. When the agent encounters a question it could answer by searching the codebase, it defaults to presenting options to the user.

#### Recommended fix
Add to the `momentum:sprint-planning` skill prompt:

```
Before presenting a diagnostic question to the user about code state or 
existing implementation:
1. grep/read the relevant files to answer it yourself
2. Only escalate to the user if the answer is genuinely ambiguous after reading
3. NEVER present a multiple-choice "is it A or B or C?" without first searching 
   for A, B, and C in the code

The user's time is for decisions, not for answering questions you can answer yourself.
```

---

### Issue 6 — `retro-and-planning-UX-defaults`
**Priority:** Medium  
**Skill/Component:** momentum:retro + momentum:sprint-planning — skill defaults  

#### What happened
Several skill interactions required the user to explicitly request behavior that should be the default given their workflow: opening story files in cmux panes for review, batching multiple un-retro'd sprints, deduplicating findings across retros.

#### Evidence
> *"Please fire them up in CMUX pane/surface on the right so I can review them"* (HF-14, 2026-04-11T05:43) — cmux markdown review mode not offered by default after story generation.

> *"Can we do both?"* (HF-18, 2026-04-10T07:21) — retro presented either/or when user wanted both sprints retro'd.

> *"Oof...sure. Make sure we dedup against the current one."* (HF-16, 2026-04-11T04:18) — dedup across retros not automatic.

#### Root cause
Skill defaults were designed for general-purpose use, not calibrated to this user's workflow. The user prefers: auto-open review artifacts, batch operations over sequential, automatic deduplication.

#### Recommended fix
1. **momentum:retro**: When multiple sprints have `retro_run_at == null`, batch-retro them by default rather than asking which one. Deduplicate findings against prior intake docs automatically before outputting.
2. **momentum:sprint-planning**: After generating story files, auto-open them in cmux markdown panes for review without requiring the user to ask.
3. Both skills should check the user's established patterns and apply them rather than asking for explicit instruction each time.

---

### Issue 7 — `retro-transcript-discovery`
**Priority:** Medium  
**Skill/Component:** momentum:retro — transcript preprocessing step  

#### What happened
During the sprint-04-08 retro, the auditor team could not find subagent logs. The user had to direct the discovery strategy, including pointing to the `@claude-code-guide` agent and specifying which global directories to check.

#### Evidence
> *"Can you look around? Use @claude-code-guide (agent) to figure out where all the subagent logs are? Send out a few agents to see if we can find things here and global directories."* (HF-20, 2026-04-11T04:22)

The transcript-query.py script was located at the correct path when given explicitly, but the retro skill's Phase 2 step referenced a relative path (`skills/momentum/scripts/`) that didn't exist in the working directory.

#### Root cause
The retro skill assumes transcript-query.py is at a relative path that may not be valid in all invocation contexts. Session files live in project-local and global locations that the skill doesn't encode.

#### Recommended fix
1. Encode known transcript locations in the retro skill's Phase 2 step:
   - Session files: `~/.claude/projects/<project-slug>/*.jsonl`
   - Global session files: `~/.claude/projects/` (all subdirectories)
   - transcript-query.py canonical path: `~/.claude/plugins/cache/momentum/momentum/<version>/scripts/transcript-query.py`
2. Phase 2 should resolve the script path dynamically (glob for the latest version) rather than hardcoding a relative path.
3. If no session files are found with the sprint's date range, expand the window by ±1 day before declaring "no sessions found" — same-day sprints (started and completed on the same date) require `--after <date-1> --before <date+1>` to capture sessions.

---

### Issue 8 — `retro-window-alignment`
**Priority:** Medium  
**Skill/Component:** momentum:retro — transcript-query preprocessing step  

#### What happened
The retro extract window for sprint-2026-04-10 captured sprint-04-08 execution and sprint-04-10 planning, but not sprint-04-10 dev execution. The HTTP/2 ktor fix, InMemoryAppPrefs AVFL catch, and consolidate-shared-ui-viewmodels quick-fix — the sprint's actual substantive development events — were entirely absent from the corpus.

#### Evidence
Documenter scope note:
> *"What the corpus does NOT contain: sprint-04-10 dev execution — no dev-wave agents, no post-wave QA/E2E/Architecture Guard, no post-sprint AVFL. InMemoryAppPrefs production-classpath catch — grep returns zero hits. HTTP/2 ktor-client-java → ktor-client-cio swap — grep returns zero hits."*

The sprint `started: 2026-04-11` and `completed: 2026-04-11` — a single-day sprint. The preprocessing used `--after 2026-04-10 --before 2026-04-12` (a window that includes the correct day) but the corpus was dominated by prior-day sessions.

#### Root cause
The retro skill uses sprint `started`/`completed` dates as preprocessing bounds. When a sprint's dev execution runs in the same session window as prior-sprint retro activity, the corpus includes more of the prior sprint than the current one. There is no mechanism to scope the extraction to the specific sessions that belong to the current sprint.

#### Recommended fix
1. The retro preprocessing step should use sprint `started` as a lower bound but also check which sessions contain content related to the sprint's story slugs. A DuckDB query filtering for messages mentioning the story slugs would identify the relevant sessions.
2. Alternatively: sprint-dev Phase 7 (sprint completion) should write the list of session file IDs to the sprint index at close time, giving the retro an explicit session manifest to extract from.
3. Consider separating planning-phase and execution-phase retros when a sprint's planning and execution run in different calendar windows.

---

### Issue 9 — `qa-reviewer-prompt-conditionalize`
**Priority:** Low  
**Skill/Component:** momentum:qa-reviewer skill prompt  

#### What happened
The `momentum:qa-reviewer` agent opened its session with an explicit disclaimer that it lacked access to SendMessage and ToolSearch, then adapted by returning findings as a final assistant message. The skill prompt referenced team-communication pathways the agent couldn't use.

#### Evidence
From sprint-04-08 execution (agent summary corpus):
> *"I do not have access to `ToolSearch` or `SendMessage` as callable tools in this environment. Per my instructions, I will return the findings report directly as my final assistant message."*

The agent recovered gracefully, but the mismatch created friction and the disclaimer consumed context before any actual work.

#### Root cause
The `momentum:qa-reviewer` prompt includes SendMessage/ToolSearch references for team-context spawning (where it would message a team lead) but is also spawned standalone (fan-out pattern for sprint review). The prompt is not conditionalized on whether the agent is inside a team.

#### Recommended fix
Conditionalize the qa-reviewer prompt:
```
If spawned as a team member (team_name is set): 
  Use SendMessage to report findings to the team lead.
  
If spawned standalone (no team_name):
  Return findings as final assistant message.
  Do not attempt ToolSearch for SendMessage schema.
```
Or: always spawn qa-reviewer inside a review team so the team-context path is always valid. The standalone path is the edge case that creates the mismatch.

---

### Issue 10 — `large-file-read-strategy`
**Priority:** Low  
**Skill/Component:** Documenter/auditor/spec-impact-discovery agent prompts  

#### What happened
96 of 238 tool errors (40%) were `File content exceeds maximum allowed tokens (10000)`, plus 10 more of the 256KB byte-size variant. Long-lived agents (documenter, auditors, spec-impact-discovery) read large files without offset/limit, hit the error, and retried — sometimes multiple times. Recovery worked but consumed turns unnecessarily.

#### Evidence
Error analysis: 96/238 errors are `file_too_large` token variant; 10 more are byte-size variant. Total: 106/238 = 44% of all errors are large-file reads. Files affected: `agent-summaries.jsonl`, `errors.jsonl`, `prd.md`, `architecture.md`, `stories/index.json`.

Auditor-human had 12 errors but completed successfully — recovery works but wastes 12+ turns.

#### Root cause
Long-lived agents (documenter, auditor, spec-impact-discovery) don't check file size before using Read. The 10k-token ceiling is frequently hit by audit-extract files and spec documents that are routinely large.

#### Recommended fix
Two options (pick one or both):
1. **Encode peek-first convention in long-lived agent prompts**: "Before reading any `.jsonl` or `.md` file over 50KB, use `wc -l` to count lines and read in chunks of 500 lines using offset/limit."
2. **Raise the Read tool ceiling for known large-file contexts**: audit-extract files (`agent-summaries.jsonl`, `errors.jsonl`) and spec files (`prd.md`, `architecture.md`) are routinely large by design. A higher ceiling (e.g., 25k tokens) for these paths would eliminate the error class without requiring every agent to learn offset-first reads.

The 44% large-file error rate is high enough to be a consistent source of wasted turns, but agents recover well, so this is low-urgency.

---

## Summary for Momentum Triage

| Priority | Count | Issues |
|----------|-------|--------|
| Critical | 2 | retro singleton guard (escalating, same-day), agent state verification |
| High | 3 | retro→planning pipeline, upstream classifier, look-before-ask |
| Medium | 3 | retro UX defaults, transcript discovery, extract window alignment |
| Low | 2 | qa-reviewer prompt conditionalize, large-file read strategy |

**Highest-leverage same-day fixes:**
1. `retro-team-singleton-guard` — burning tokens in every retro, escalating, was flagged in the prior retro and not fixed
2. `agent-state-verification-hook` — causes user frustration (caps-lock signals, repeated requests) in every code sprint

**Common thread:** This sprint's findings cluster around retro-skill quality and agent–world visibility. The planning-quality gate (multi-lens AVFL with severity-ordered fixer) is working well and should be the template for other phases. The retro-skill orchestration and the gap between agent claimed-state and real observed state are the two areas requiring immediate attention.
