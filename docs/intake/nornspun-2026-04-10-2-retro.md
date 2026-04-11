# Momentum Upstream Intake — nornspun sprint-2026-04-06 (D3) Retrospective
**Source project:** nornspun  
**Retro date:** 2026-04-10  
**Sprint:** sprint-2026-04-06 / D3 (completed 2026-04-06)  
**Intake iteration:** 2  
**Prepared by:** retro skill (automated transcript audit + documenter synthesis)  

---

## How to Use This Document

This document captures 11 upstream improvement opportunities identified during a retrospective transcript audit of the D3 code sprint — nornspun's first major production code sprint. All items were classified as Momentum-owned after review: even project-surfaced symptoms (uniform error counts, stale test fixtures) trace back to gaps in Momentum skill guidance, not project-specific defects.

Each finding includes quantitative evidence, verbatim user quotes, root cause analysis, and recommended fix scope.

**Sprint data summary:**
- 220 user messages across 4 sessions
- 129 subagents spawned (38 with zero turns — 29% spawn waste)
- 595 tool errors (exit_code_nonzero: 424/71%, other: 68, cancelled: 45, file_not_found: 31, file_too_large: 20)
- 451 team messages
- 10,405 total assistant turns · 89,441 KB total transcript
- 12 user interventions that required course-correction
- 8 production bugs found and fixed by E2E validator (BUG-1 through BUG-8)
- Final E2E pass rate: 57/71 scenarios (80%)

**Context:** This was a code sprint (vs. the prior planning sprint). Error profile, team patterns, and agent behaviors shift significantly between sprint types. The planning sprint (sprint-2026-04-08) generated findings about file-size hints and coverage deduplication; this sprint surfaces code-sprint-specific patterns that Momentum must address separately.

**Dedup note:** The 13 findings from the prior intake (`nornspun-2026-04-10-1-retro.md`) are not repeated here. Items below are new.

---

## Issue Index

| # | ID | Priority | Skill/Component Affected |
|---|-----|----------|--------------------------|
| 1 | `sprint-dev-team-composition-rules` | **Critical** | sprint-dev skill |
| 2 | `e2e-black-box-enforcement` | **Critical** | e2e validator skill |
| 3 | `agent-spawn-preflight-check` | **High** | All spawn workflows |
| 4 | `idle-notification-deduplication` | **High** | Team orchestration / platform |
| 5 | `e2e-client-side-coverage` | **High** | E2E skill, Maestro guidance |
| 6 | `backend-dev-systematic-error-guidance` | **High** | sprint-dev, dev agent prompts |
| 7 | `module-upgrade-change-preview` | **Medium** | BMad builder / module upgrade skills |
| 8 | `sprint-dev-workflow-sequencing` | **Medium** | sprint-dev workflow |
| 9 | `user-context-aware-explanations` | **Medium** | Agent prompts, lead behavior |
| 10 | `sprint-scope-tracking` | **Low** | Sprint practice / retro |
| 11 | `maestro-ux-spec-sync-guidance` | **Low** | E2E skill, spec sync guidance |

---

## Issues

---

### Issue 1 — `sprint-dev-team-composition-rules`
**Priority:** Critical  
**Skill/Component:** sprint-dev skill — team creation rules  

#### What happened
The sprint-dev workflow created per-story team agents (dev-d4-1, dev-d4-2, dev-d4-4, wave1-d4-1, wave1-d4-2, wave1-d4-4) instead of using shared role agents. The user discovered a "massive team" and ordered an immediate shutdown.

#### Evidence
User interventions at messages 45–46:
> *"Why does it keep asking me for permission? And why is this a team?"* (message 45)  
> *"Okay now you've got a massive team. I think you messed this up. Shut them all down."* (message 46)

Six+ specialized agent types were created for work that should have used 2–3 shared role agents. The correct pattern (established later in the sprint) was: one backend-dev, one qa, one e2e — shared across all stories in the cycle. The oversized team also contributed to the 38 zero-turn agents (29% of all agents spawned).

#### Root cause
Sprint-dev skill allows per-story agent decomposition without constraining total team size. Wave-based decomposition multiplied the count further. No team-size sanity check exists before spawning.

#### Recommended fix
Sprint-dev skill must encode explicit composition rules for code sprints:
```
Team composition for code sprints:
  - backend-dev: 1 shared agent (handles all backend stories in the cycle)
  - frontend-dev: 1 shared agent (if client changes required)
  - qa: 1 shared agent
  - e2e: 1 shared agent
  Maximum team size: 4 agents (lead excluded)
  
Per-story decomposition → fan-out INDIVIDUAL agents (not team members).
TeamCreate is for collaborative cycles only (dev+qa+e2e iterating on bugs).
```
Add a pre-spawn team composition review step: lead proposes team structure, developer approves, THEN spawn.

---

### Issue 2 — `e2e-black-box-enforcement`
**Priority:** Critical  
**Skill/Component:** E2E validator skill — enforcement of black-box constraints  

#### What happened
The E2E validator analyzed source code instead of running the app. The user discovered this at message 71 and it required 2.5 hours (messages 71–91) to establish proper guidelines.

#### Evidence
User interventions at messages 71–72:
> *"Hey can you tell me how the validation was happening? I didn't see the android emulator."* (message 71)  
> *"I thought we had ABSOLUTE blocking of the E2E validator from reading source code. In the past the E2E opened up cmux panes/surfaces on the right to run postgresql and fastapi and then opened an android emulator using the maestro library."* (message 72)

The validator defaulted to static analysis of Gherkin specs against source code because no project-level E2E guidelines existed yet. The rules from prior interactions had not been persisted as mandatory constraints.

The session spent 2.5 hours on unplanned work: creating cmux usage rules, Android emulator guidelines, and E2E black-box validation rules — then live-testing them (emulator launched at message 86, Maestro tests ran at message 90).

#### Root cause
E2E validator skill has no hard constraint requiring service launch before validation. The skill falls back to static analysis silently when cmux panes and services aren't detected.

#### Recommended fix
The E2E validator skill must:
1. **Fail fast** if it cannot detect running services (FastAPI, PostgreSQL) — do not fall back to source code analysis
2. **Require explicit cmux pane references** before beginning validation
3. **Encode as a hard constraint**, not a guideline:
   ```
   PROHIBITED: Reading source code files to validate behavior.
   REQUIRED: All behavioral validation runs against live services via cmux panes.
   If services are not running, halt and report: "Services not detected. 
   Launch FastAPI and PostgreSQL in cmux panes before running E2E validation."
   ```
4. **Provide a startup checklist** in the skill: services → emulator → Maestro → validate

---

### Issue 3 — `agent-spawn-preflight-check`
**Priority:** High  
**Skill/Component:** All Momentum spawn workflows  

#### What happened
38 of 129 agents (29%) had zero assistant turns — they were created but never produced any work. These wasted resources for spawning, tool loading, and context preparation.

#### Evidence
Agent summary analysis: 38 agents with `assistant_turns=0` out of 129 total. These agents still appear in the subagent manifest with non-zero `size_kb` (JSONL files were created, resources consumed). The oversized team incident (messages 45–46) likely accounts for some, but 29% is too high to attribute to a single incident.

Combined with the planning sprint's 54-agent fan-out, this pattern suggests spawn-before-think is a recurring orchestration failure mode, not an isolated incident.

#### Root cause
Spawn workflows do not validate prompts or team composition before creating agents. Agents are created first, then given work (or not). No gate exists between "decide to spawn" and "actually spawn."

#### Recommended fix
Add a pre-flight validation step to all spawn workflows:
```
Before spawning any agent, verify:
  1. Prompt is non-empty (no blank or placeholder prompts)
  2. Team size is within bounds (for TeamCreate: ≤4 members)
  3. Agent type matches the required tools (read-only task → Explore, not general-purpose)
  4. No duplicate agent is already running the same task
```
For team spawning specifically: propose team composition to the developer first, receive approval, then spawn. This eliminates the oversized-team failure mode entirely.

---

### Issue 4 — `idle-notification-deduplication`
**Priority:** High  
**Skill/Component:** Team orchestration — idle notification system  

#### What happened
The 451 team messages included a large proportion of idle notifications — often 3–5 in rapid succession from the same agent within seconds. Substantive messages (bug reports, fix confirmations, validation results) were buried in notification noise.

#### Evidence
Messages 60–70 show 10+ idle notifications in rapid succession. Pattern: agent completes work, sends substantive message, then sends 2–5 idle notifications before being acknowledged. Estimated 40–50%+ of all 451 team messages were idle notifications rather than substantive communication.

From the current retro session: the same pattern recurred — the retro team's documents were well-structured and the findings were strong, but the team message channel required manual filtering to find substantive content.

#### Root cause
The idle notification system fires on a timer regardless of whether the agent has new information. No deduplication or backoff — each tick generates a new notification.

#### Recommended fix
Idle notifications should be deduplicated at the platform or skill level:
- **One notification per agent per idle period** — suppress subsequent notifications until the agent receives new work or produces new output
- **Backoff strategy**: if an agent has been idle for >60 seconds, suppress further notifications until the lead sends a message
- **Signal filtering**: substantive messages (bug reports, findings, completions) should be visually distinguished from idle pings in the team message display

If platform-level deduplication is not feasible, the Momentum team orchestration skill should add explicit guidance: leads should not acknowledge idle notifications unless they contain new information in the `summary` field.

---

### Issue 5 — `e2e-client-side-coverage`
**Priority:** High  
**Skill/Component:** E2E skill — coverage scope definition  

#### What happened
After automated E2E validation passed 57/71 scenarios (API-level), the user's 30 minutes of manual testing found fundamental interaction bugs: norn switching didn't work, context wasn't isolated between norns, and connection errors occurred. These were invisible to the automated API-level validation.

#### Evidence
User manual testing at messages 147–157:
> *"How do I switch to verdandi? Is it the button on the top right? When I click it nothing happens"* (message 148)  
> *"The problem I see is that Urd repeated herself"* (message 155)  
> *"I switched to Verdandi but it seemed to maintain the same text, output, context as Urd"* (message 156)

The E2E validation checked API-level behavior (POST /sessions, POST /messages, etc.) but not client-side state management. Norn switching is a client-state concern that requires the actual Kotlin app to validate.

The user spent 30+ minutes (19:29–20:07) manually debugging issues that were invisible to the automated validation.

#### Root cause
The E2E skill's definition of "covered" encompasses API scenarios only. Client-integration flows (UI state management, screen transitions, context isolation between agents) are not included in the Gherkin coverage requirement. Momentum's E2E skill guidance does not specify that client-side interaction must be validated.

#### Recommended fix
The E2E skill must define two coverage layers:
```
Layer 1 — API behavioral coverage (current):
  - All Gherkin scenarios validated against live FastAPI endpoints
  - Pass/fail/inconclusive categorization

Layer 2 — Client interaction coverage (required addition):
  - UI state transitions (norn switching, context isolation)
  - End-to-end user flows via Maestro (Android) and desktop UI testing
  - Connection handling and error state display
```
A sprint's E2E validation is not complete until both layers pass. The skill should surface a warning if Layer 2 coverage is absent: "API validation complete. Client interaction coverage not performed. User manual testing required."

---

### Issue 6 — `backend-dev-systematic-error-guidance`
**Priority:** High  
**Skill/Component:** sprint-dev, dev agent prompts  

#### What happened
20 backend-dev agents each produced exactly 19 errors — a suspiciously uniform count that suggests every agent independently rediscovered and re-triggered the same systematic setup issue rather than building on prior agents' knowledge.

#### Evidence
Error analysis: 20 backend-dev agents, 4,500 total turns, 212 errors = **exactly 19 errors per agent** (uniform to the count). The uniformity strongly suggests a systematic pre-work error sequence (possibly test suite setup, import errors, or environment initialization) that every agent hits before reaching its actual task.

Combined cost: if each agent wasted 3–5 turns on the systematic error sequence, that's 60–100 wasted turns across 20 agents for a single fixable issue.

#### Root cause
Momentum's dev agent prompts do not include: (1) known systematic error patterns for the project, (2) a "first run a smoke test before beginning" instruction, or (3) a mechanism for agents to share discoveries about systematic setup issues with subsequent agents.

This is a Momentum guidance gap — the skill has no pattern for "here are the known error types this project's test suite generates before you reach actual work."

#### Recommended fix
Sprint-dev skill should support a **pre-work diagnostic step**:
```
Before beginning implementation:
1. Run the full test suite once: note which tests fail and what errors appear
2. Categorize errors as: (a) pre-existing / known, (b) caused by your changes
3. Report pre-existing errors in your opening summary so the lead can update 
   the spawn prompt for subsequent agents
```
Additionally: when a sprint produces a pattern of identical errors across many dev agents, the retro skill should flag it as a systematic environment issue requiring a one-time fix — not a per-agent debugging task.

---

### Issue 7 — `module-upgrade-change-preview`
**Priority:** Medium  
**Skill/Component:** BMad builder / module setup and upgrade skills  

#### What happened
A BMad builder upgrade from 1.0.0 to 1.5.0 modified files without clearly communicating what would change. The user discovered unexpected git changes after the fact.

#### Evidence
Messages 177–178:
> *"What the heck just happened to my git?"* (message 177)  
> *"Did it change the bmad output location?"* (message 178)

Earlier: *"wait are you manually updating the skill files and such? Shouldn't you have copied those from the bmb github repo?"* (message 174), indicating the upgrade process was unclear throughout.

#### Root cause
Module setup/upgrade skills apply file changes without a preview step. The user has no opportunity to review what will be modified before the skill executes. For upgrades that touch directory structure or file locations, this creates surprise git state.

#### Recommended fix
Any module setup or upgrade skill must include a preview step before applying changes:
```
Step N (before apply): Generate diff preview
  - List files that will be created, modified, or deleted
  - Highlight any directory structure changes
  - Show file moves or renames explicitly
  - Present to developer: "The upgrade will make these changes. Proceed?"
  
Only after explicit developer approval: apply changes.
```
The preview should be diff-style (old path → new path, or +/- for content changes) so the developer can assess risk without reading full file contents.

---

### Issue 8 — `sprint-dev-workflow-sequencing`
**Priority:** Medium  
**Skill/Component:** sprint-dev workflow — step ordering  

#### What happened
The sprint-dev workflow used TeamCreate before AVFL validation and before individual dev agents completed their stories. The user had to specify the correct ordering.

#### Evidence
User intervention at message 54:
> *"Yes the team should happen after avfl, a dev, validator, and possibly qa. But that shouldn't be until ALL are finished."*

And at message 94:
> *"We should have the E2E validator and dev together in a CreateTeams. If we need both devs use a backend and frontend and use a team of three"*

The correct sequence the user specified:
1. Individual dev agents implement stories (fan-out, independent)
2. AVFL validation of implementations
3. Team cycle: backend-dev + qa + e2e (collaborative, bug-fix loop)

The sprint-dev skill had no explicit sequencing constraint, allowing the lead to create the team at the wrong phase.

#### Root cause
Sprint-dev workflow.md does not encode the correct phase ordering for code sprints. The lead made a judgment call that was incorrect.

#### Recommended fix
Sprint-dev workflow must explicitly sequence the phases:
```
Phase 1 — Implementation (fan-out):
  Spawn individual dev agents per story (NOT a team).
  Wait for ALL stories to reach done.

Phase 2 — AVFL validation:
  Run AVFL checkpoint on all implementations.
  Fix agents address findings.

Phase 3 — Team validation cycle (TeamCreate):
  Compose: backend-dev (or frontend-dev if needed) + qa + e2e
  Max 3 agents + lead.
  Iterate until E2E pass rate meets threshold (e.g., ≥80%).
```
TeamCreate is prohibited in Phase 1. Phase 3 only begins after Phase 2 AVFL findings are resolved.

---

### Issue 9 — `user-context-aware-explanations`
**Priority:** Medium  
**Skill/Component:** Lead agent behavior, agent prompts  

#### What happened
When asked about storage architecture, the lead defaulted to technical implementation details (PostgreSQL, Docker, Alembic migration paths) when the user needed a conceptual explanation of where their campaign data lives.

#### Evidence
Messages 12–16:
> *"What is add persistent storage do?"* (message 12)  
> *"Woof I'm getting lost. Currently, the legacy system stores loads of campaign files... You keep talking very technical and I'm getting lost in the details."* (message 14)  
> *"Where does all this get stored? When do we implement it?"* (message 14)

The lead was explaining implementation layers when the user's question was user-level: "where do my campaign files go?"

#### Root cause
Momentum's lead agent prompts do not include instructions to calibrate explanation level to the user's role. When a non-technical user asks an architectural question, agents default to implementation-level answers.

#### Recommended fix
Lead agent prompts should include an explanation calibration rule:
```
When explaining architecture or technical decisions to the user:
1. Start with the user's mental model (what they experience / what they care about)
2. Map to implementation only after the user-level concept is clear
3. Use concrete analogies from their domain (for nornspun: campaign files, GM prep, 
   session notes — not PostgreSQL tables, Alembic migrations, Docker volumes)
4. If the user says "I'm lost" or asks the same question twice: stop, restart 
   from the user's perspective, not the system's perspective
```
This is a general Momentum guidance capability gap: skills should encode explanation-level awareness as a first-class concern, especially for products where the developer is also the primary user.

---

### Issue 10 — `sprint-scope-tracking`
**Priority:** Low  
**Skill/Component:** Sprint practice, retro skill  

#### What happened
The D3 sprint expanded significantly beyond its original scope: actual code implementation was roughly 40% of activity. The rest was unplanned work: E2E guidelines (unplanned), emulator setup (unplanned), cmux rules (unplanned), BMad builder upgrade (unplanned), UX discovery (unplanned), and next-sprint planning.

#### Evidence
Story-by-story analysis: D4 implementation (D4.1, D4.2, D4.4, backend bug cycles) accounts for the largest agent counts, but the sprint also produced three guideline documents, an emulator setup validation, a BMad upgrade, and UX discovery — none of which appeared in the sprint's original story list.

From the retro: *"The sprint started with D4 story implementation but expanded to include E2E guidelines creation, emulator guidelines, cmux rules creation, BMad builder upgrade, UX discovery, and next-sprint planning."*

#### Root cause
Momentum has no mechanism for the lead to track planned vs unplanned work within a sprint. When scope expands (legitimately, as gaps are discovered), there's no record of what was planned vs discovered, making retros less precise and velocity measurements misleading.

#### Recommended fix
Sprint-dev skill should maintain a lightweight scope log:
```
Sprint scope log (updated in real time):
  PLANNED: [list of sprint stories]
  UNPLANNED (discovered): [item | reason | outcome]
```
At sprint close, the scope log feeds into the retro automatically: unplanned items that recur across sprints become upstream candidates (like E2E guidelines, which should be pre-installed by Momentum, not discovered mid-sprint).

The retro skill should also report a **scope expansion ratio**: planned turns / total turns. A ratio below 50% (as in D3) flags a systematic practice gap — sprints should start with adequate guidelines rather than discovering their absence mid-execution.

---

### Issue 11 — `maestro-ux-spec-sync-guidance`
**Priority:** Low  
**Skill/Component:** E2E skill, spec sync guidance  

#### What happened
A Maestro test referenced removed UX copy ("The Nornspun Experience") that had been deleted in a prior UX story. The user had to manually identify and flag the stale reference.

#### Evidence
Message 93:
> *"'The Nornspun Experience' was removed in one of our UX stories. It should be removed from that maestro test."*

The stale fixture was not caught by any automated check during the sprint. The user discovered it incidentally while reviewing test output.

#### Root cause
Momentum's E2E skill provides no guidance on keeping test fixtures in sync with UX spec changes. When UX stories modify or remove UI copy, there is no step that checks downstream test fixtures for stale references.

This is a guidance gap — Momentum should encode the pattern, even though the specific fixtures are project-specific.

#### Recommended fix
E2E skill should include a **spec-sync check** in its pre-validation step:
```
Before running Maestro tests:
1. Check for recent UX story completions (stories in the UX epic closed since 
   the last E2E run)
2. For each completed UX story: scan Maestro test files for references to 
   modified or removed UI copy
3. Flag stale references before running (not after — stale tests produce 
   misleading failures)
```
This prevents the "tests fail because the copy changed, not because the behavior broke" failure mode that wastes debugging time.

---

## Summary for Momentum Triage

| Priority | Count | Issues |
|----------|-------|--------|
| Critical | 2 | sprint-dev team composition, E2E black-box enforcement |
| High | 4 | agent spawn pre-flight, idle notification dedup, E2E client coverage, backend-dev error guidance |
| Medium | 3 | module upgrade preview, sprint-dev sequencing, context-aware explanations |
| Low | 2 | sprint scope tracking, Maestro spec sync guidance |

**Highest-leverage fixes (biggest impact on next sprint):**
1. Sprint-dev team composition rules → prevents oversized team incidents and 29% zero-turn agent waste
2. E2E black-box enforcement → prevents 2.5 hours of unplanned guideline creation mid-sprint
3. Sprint-dev workflow sequencing → prevents TeamCreate at wrong phase

**Common thread:** The D3 sprint was the first code sprint. Many of these issues are "first code sprint" gaps — patterns that planning sprints never expose. Momentum needs a distinct code-sprint track with its own defaults, constraints, and agent compositions separate from planning-sprint patterns.
