---
title: Retro Team Singleton Guard — Enforce Exactly-One Spawning for Documenter and Auditor Roles
story_key: retro-team-singleton-guard
story_type: practice
status: ready-for-dev
epic_slug: impetus-core
priority: critical
depends_on: []
touches:
  - skills/momentum/skills/retro/workflow.md
  - skills/momentum/skills/retro/evals/
derives_from:
  - path: _bmad-output/planning-artifacts/epics.md
    relationship: derives_from
    section: "Epic 10: Impetus Core Infrastructure — orchestrator behavioral guards, deduplication guards"
  - path: _bmad-output/implementation-artifacts/sprints/sprint-2026-04-08/retro-transcript-audit.md
    relationship: evidence
    section: "Retro Pipeline Required 3 Attempts: 17 Agents for 4 Roles (RV-05 / unactioned)"
  - path: _bmad-output/implementation-artifacts/stories/fix-retro-documenter-replication-defect.md
    relationship: related
    section: "Topology fix (TeamCreate replication root cause); this story is the prophylactic count guard"
---

# Retro Team Singleton Guard — Enforce Exactly-One Spawning for Documenter and Auditor Roles

## Story

As the retro skill orchestrator,
I want a singleton-count guard that runs immediately after the Phase 4 TeamCreate spawn and asserts the assembled team contains exactly 1 documenter and exactly 3 auditors (one each of `auditor-human`, `auditor-execution`, `auditor-review`),
so that every retro is guaranteed to run with the intended team — not the silently-replicated team that has been observed in every recent retro — and the workflow halts loudly the next time the underlying topology bug recurs instead of burning tokens on idle duplicate agents.

## Description

The retro skill's Phase 4 TeamCreate step in `skills/momentum/skills/retro/workflow.md` is supposed to spawn exactly **1 documenter + 3 auditors** (`auditor-human` + `auditor-execution` + `auditor-review`). In the retros analyzed so far, it has consistently spawned **N× duplicate documenters** plus extra auditor copies, and the multiplier is **growing**:

| Retro target sprint | Intended team | Actual spawned (from `audit-extracts/agent-summaries.jsonl`) | Surplus |
|---|---|---|---|
| `sprint-2026-04-08` | 4 (1 doc + 3 aud) | 8 documenters, 3 auditor-execution, 3 auditor-review, 3 auditor-human → **17** | +13 |
| `sprint-2026-04-10` retro (per stub) | 4 | 10 documenters, 3 auditor-review, 2 auditor-human, 2 auditor-execution → **17** | +13 |

This was logged in the sprint-2026-04-08 retro audit as *"Retro Pipeline Required 3 Attempts: 17 Agents for 4 Roles"* (item RV-05) and went unactioned. The multiplier going from 5× to 8× to 10× duplicate documenters across consecutive retros — plus the appearance of 2× and 3× auditor copies that were not present at first — is the diagnostic signature of an accumulating topology defect, not a fixed off-by-one. The duplicate documenters share identical first-200-character prompts, indicating a single `TeamCreate` API call replicating rather than four distinct spawns.

### Why this story exists separately from `fix-retro-documenter-replication-defect`

`fix-retro-documenter-replication-defect` (also in this sprint) is the **topology fix** — it replaces the current TeamCreate-with-retro-lead spawn shape with a single-orchestrator + 1 documenter + N distinct auditors topology so the documenter API call no longer fans out per-instance. The two stories share root cause but address different layers:

| Story | Layer | What it changes | If it breaks |
|---|---|---|---|
| `fix-retro-documenter-replication-defect` | **Topology** (root cause) | Replaces the spawn shape so replication cannot occur in the first place | The fix could regress in a future workflow refactor — replication returns silently |
| `retro-team-singleton-guard` (THIS STORY) | **Invariant guard** (defense in depth) | Asserts the post-spawn team count matches the intended composition; HALTs Phase 4 and produces a diagnostic log if it does not | The replication-defect fix never lands or regresses, but the retro now fails *loudly* in <10 seconds instead of after spawning 17 agents and writing a corrupted audit |

The two stories are intentionally redundant. The topology fix is the prophylactic; the singleton guard is the safety net. Either one alone would close the immediate symptom, but only both together prevent silent regression in a future retro workflow rewrite. **This story does not depend on the topology fix being merged first** — it is independent and remains valuable on its own. (See Dev Notes → Sequencing for guidance on what changes if both stories merge in the same wave.)

### Pain context

Every retro currently burns ~9 wasted documenter agents and several wasted auditor copies. At ~389 KB context per documenter (per the sprint-2026-04-08 audit's abandoned-agent observation), that is ~3.5 MB of context loaded for nothing per retro, every retro. The waste was flagged once, went unactioned, and then escalated. This story closes the loop with a guard that cannot itself be silently ignored — if it fires, the retro halts and the developer sees the failure.

## Acceptance Criteria (Plain English)

### AC1: Singleton Guard Runs Immediately After Phase 4 TeamCreate Spawn

- A guard step exists in `skills/momentum/skills/retro/workflow.md` Phase 4 (Step n=4), inserted **immediately after** the `<action>Spawn 4 agents via TeamCreate: ...</action>` block and **before** the `<action>Wait for the team to complete ...</action>` line.
- The guard reads the team configuration file at `~/.claude/teams/{{team_name}}/config.json` (the file written by `TeamCreate` — see Dev Notes → TeamCreate Config Format) and inspects the `members` array.
- The guard runs **before any team work begins** — it must catch a wrong-shape team before the documenter prompt or any auditor prompt produces output.

### AC2: Guard Asserts Exact Composition: 1 Documenter + 3 Distinct Auditors

The guard asserts all four of the following conditions:

1. **Total member count.** The `members` array contains exactly 4 entries (1 documenter + 3 auditors). Not "at least 4" — exactly 4.
2. **Exactly 1 documenter.** Exactly one member has `name == "documenter"` (or `agentType == "documenter"` if the team config uses agent type to identify role — match the field used by TeamCreate, see Dev Notes).
3. **Exactly 3 auditors with distinct roles.** The other three members are exactly the three auditor roles `auditor-human`, `auditor-execution`, `auditor-review` — each appearing exactly once. No role may be missing; no role may appear twice.
4. **No surplus members.** No member has any name or agentType outside the four-role set above.

### AC3: Guard Halts Phase 4 with a Diagnostic Output on Failure

When any of the four conditions in AC2 fails, the guard:

- Emits a diagnostic block naming the failure mode. The block must include:
  - Sprint slug under retro (`{{sprint_slug}}`)
  - Expected composition: `1 documenter + 1 auditor-human + 1 auditor-execution + 1 auditor-review (4 total)`
  - Actual composition: a per-role count tally derived from `members` (e.g., *"actual: 5 documenter, 2 auditor-review, 1 auditor-execution, 1 auditor-human (9 total)"*)
  - The path to the team config file the guard read (`~/.claude/teams/{{team_name}}/config.json`)
  - A reference to this story slug and to `fix-retro-documenter-replication-defect` so the developer immediately sees the correct context for diagnosis
- HALTs the retro workflow. The auditor team does not proceed, the documenter is not awaited, and the findings document is not written. (Reusing the existing Phase 4 "investigate auditor team failure" halt path is acceptable — see Dev Notes for integration approach.)
- Does **not** prompt the developer to "continue anyway." There is no continue-with-known-bad-team path. (This matches the philosophy of the recent Phase 2 hard-fail change in `retire-sprint-log-final-cleanup` — strictness is the point.)

### AC4: Guard Passes Silently on Correct Composition (No Workflow Friction)

When the team composition matches the AC2 assertion exactly:

- The guard emits no developer-visible output (or at most a single confirmation line such as *"Team composition verified: 1 documenter + 3 auditors"* — no multi-line block, no developer prompt).
- Phase 4 continues to the existing `<action>Wait for the team to complete ...</action>` line with no behavioral change.
- The wait loop, the existing findings-document presence check (`<check if="findings document written ...">`), and the existing auditor-team-failure halt path all remain intact and unmodified.

### AC5: Guard Tolerates the TeamCreate Config Field Naming Without Hard-Coding It

- The guard tolerates the documented TeamCreate config schema (`members` array with `name` and `agentType` fields per `~/.claude/teams/{team-name}/config.json`) but does not hard-fail on minor schema variation (e.g., a `role` field in addition to `agentType`). If the four roles can be identified by either `name` or `agentType` (or both), the guard accepts the team as correctly composed.
- Field-naming detection is done in plain prose in the workflow step — not via a brittle exact-match — so a TeamCreate schema clarification in a future Claude Code release does not break the guard.
- If the config file does not exist, is unreadable, or does not contain a `members` array, the guard treats this as a guard-failure with diagnostic output (per AC3) — *"unable to verify team composition: members array not found in {{config_path}}"* — and halts. (This is intentional: an unverifiable team is not a passing team.)

### AC6: No Other Retro Phase Is Modified

- Phases 0, 1, 2, 3, 5, 5.5, and 6 are byte-identical to before this story.
- Within Phase 4 itself, the only changes are:
  1. Insertion of the new guard step between the spawn block and the wait block.
  2. (Optional, if the implementer prefers) a one-line note at the top of Phase 4's existing `<action>Spawn 4 agents via TeamCreate:</action>` block referencing the guard's existence — but this is non-load-bearing prose and not required.
- The four existing system prompts inside the spawn block (`auditor-human`, `auditor-execution`, `auditor-review`, `documenter`) are unchanged — including their SendMessage instructions, their JSON-string-format guidance, and their tool references.
- No SKILL.md frontmatter (`description`, `model`, `effort`) is changed.

### AC7: Behavioral Evals Confirm Both the Pass and Fail Paths

Two behavioral evals are written under `skills/momentum/skills/retro/evals/` (the directory already exists per the existing retro evals):

- `eval-team-singleton-guard-halts-on-duplicate-documenter.md` — *Given a retro Phase 4 where the team config at `~/.claude/teams/{{team_name}}/config.json` contains 5 documenters + 3 auditors (one of each role), the guard should HALT Phase 4 with a diagnostic block naming the actual composition (5 documenter, 1 auditor-human, 1 auditor-execution, 1 auditor-review) and the expected composition (1 + 1 + 1 + 1). The auditor team should not be awaited and the findings document should not be written.*
- `eval-team-singleton-guard-passes-on-correct-composition.md` — *Given a retro Phase 4 where the team config contains exactly 1 documenter + 1 auditor-human + 1 auditor-execution + 1 auditor-review, the guard should pass silently (or emit at most a single confirmation line) and Phase 4 should advance to the existing wait loop without prompting. The four existing system prompts and the wait loop must remain unmodified.*

Both evals must pass when the implementer runs them. If either fails after up to 3 EDD revision cycles, the issue is surfaced to the developer rather than silently dropped.

## Tasks / Subtasks

- [ ] Task 1 — Read existing Phase 4 and confirm the integration point (AC: 1) — `skill-instruction`
  - [ ] Read `skills/momentum/skills/retro/workflow.md` from `<step n="4" ...>` through the closing `</step>` (currently lines ~227–435)
  - [ ] Identify the exact insertion point: between the closing `</action>` of the `<action>Spawn 4 agents via TeamCreate: ...</action>` block (around line 417) and the start of `<action>Wait for the team to complete ...</action>` (around line 419)
  - [ ] Confirm no other phase reads the team config file in a way that the new guard could collide with
  - [ ] Note for the dev: do NOT modify the existing four system prompts inside the spawn block — they are out of scope per AC6

- [ ] Task 2 — Write the two behavioral evals before the workflow change (AC: 7) — `skill-instruction` (EDD)
  - [ ] Create `skills/momentum/skills/retro/evals/eval-team-singleton-guard-halts-on-duplicate-documenter.md` per AC7 wording
  - [ ] Create `skills/momentum/skills/retro/evals/eval-team-singleton-guard-passes-on-correct-composition.md` per AC7 wording
  - [ ] Each eval is a single `.md` file describing scenario + expected behavior in the format used by sibling evals in the same directory (see `eval-sprint-summary-word-count-enforcement.md`, `eval-produces-sprint-summary-at-retro-close.md`, `eval-sprint-summary-omits-features-section-when-no-feature-status.md` for format)
  - [ ] Confirm both eval files render as plain markdown and include enough scenario context for a subagent to evaluate the behavior

- [ ] Task 3 — Insert the singleton guard step in Phase 4 (AC: 1, 2, 3, 4, 5) — `skill-instruction`
  - [ ] Insert a new `<action>` block (or a small `<step>`-internal sub-block — match the local style of Phase 4) between the spawn block and the wait block
  - [ ] The guard step's prose instructs the orchestrator to:
    1. Read `~/.claude/teams/{{team_name}}/config.json` (using the team name passed to TeamCreate in the spawn block — capture this as `{{team_name}}` if not already a workflow variable)
    2. Parse the `members` array
    3. Tally per-role counts using either the `name` field or `agentType` field — accept either as the role identifier per AC5
    4. Assert: 4 total members, exactly 1 with role `documenter`, exactly 1 each with roles `auditor-human`, `auditor-execution`, `auditor-review`, and zero members outside that set
    5. On pass — emit at most a single confirmation line and continue (AC4)
    6. On fail (or if the config file/members array is unreadable per AC5) — emit the diagnostic block per AC3 and HALT (re-using or paralleling the existing Phase 4 `auditor team failure` halt path)
  - [ ] Capture `{{team_name}}` from the spawn step. If the existing spawn block doesn't already name the team explicitly, name it (e.g., `retro-{{sprint_slug}}`) and reference that name in both the spawn instruction and the guard
  - [ ] Confirm the guard runs **before** the `<action>Wait for the team to complete ...</action>` line — not after

- [ ] Task 4 — Run the EDD cycle on both evals (AC: 7) — `skill-instruction`
  - [ ] For each eval file, spawn a subagent via the Agent tool. Provide it: (a) the eval scenario as its task, and (b) the modified `workflow.md` Phase 4 contents (with the new guard step) as context.
  - [ ] Observe whether the subagent's behavior matches the eval's expected outcome — the duplicate-documenter scenario must result in a HALT with a diagnostic output; the correct-composition scenario must result in silent pass-through to the wait loop
  - [ ] If both evals pass → mark Task 4 complete
  - [ ] If either eval fails → diagnose the gap in the guard wording, revise, re-run (max 3 cycles)
  - [ ] If still failing after 3 cycles → surface to developer with the failure detail; do not silently mark complete

- [ ] Task 5 — Verify AC6 (no other phase modified) (AC: 6) — `skill-instruction`
  - [ ] Run a `git diff skills/momentum/skills/retro/workflow.md` and confirm:
    - All changes are inside the Phase 4 `<step n="4" ...>` block
    - The four existing system prompt strings (auditor-human, auditor-execution, auditor-review, documenter) are byte-identical to before
    - No edits in Phases 0, 1, 2, 3, 5, 5.5, 6
    - No edits to `skills/momentum/skills/retro/SKILL.md`
  - [ ] Document the verification result in the Dev Agent Record

## Dev Notes

### TeamCreate Config Format (load-bearing for the guard)

Per the TeamCreate tool documentation surfaced via ToolSearch:

> Teammates can read the team config file to discover other team members:
> - **Team config location**: `~/.claude/teams/{team-name}/config.json`
>
> The config file contains a `members` array with each teammate's:
> - `name`: Human-readable name (always use this for messaging and task assignment)
> - `agentId`: Unique identifier (for reference only - do not use for communication)
> - `agentType`: Role/type of the agent

The retro workflow's existing Phase 4 spawn block calls `TeamCreate` followed by per-member Agent spawns with `team_name` and `name` parameters. After all four spawns complete, `~/.claude/teams/{{team_name}}/config.json` contains the four members. The guard reads this file as plain JSON.

**Field naming caveat (AC5):** The schema documents `name` and `agentType`. In practice each spawn assigns the role through the Agent tool's `name` parameter (the value the workflow asks the orchestrator to pass), and `agentType` is set by the agent definition. The guard should tally by either field — whichever matches the role identifier set in the spawn block. The four role identifiers are `documenter`, `auditor-human`, `auditor-execution`, `auditor-review`.

### Why Inserting the Guard Inside Phase 4 (Not as a Separate Phase)

Phase 4 is the smallest unit of work that owns the team. A separate phase would either:

- Run before `TeamCreate` returns (too early — there is no team to verify yet)
- Run after the documenter writes the findings file (too late — the wasted spawns already happened and the audit is already corrupted)

Inserting between the spawn block and the wait block is the only correct integration point. It uses Phase 4's existing failure path (`<check if="findings document not found after documenter exits">`) as a reference shape — the new guard should HALT in the same loud way.

### Sequencing With `fix-retro-documenter-replication-defect`

Both stories live in the same sprint. Two orderings are acceptable:

1. **Topology fix first, then guard.** Implement `fix-retro-documenter-replication-defect` first; the singleton guard then validates the topology fix on its first real run. Preferred if both ship in the same wave.
2. **Guard first, then topology fix.** Implement this story first; on the next retro the guard fires loudly on the still-broken topology, the developer ships the topology fix, the guard then passes silently from then on.

Either ordering is functional. The guard's value is **independent** of the topology fix — it is the safety net that ensures regression of the topology fix (now or in any future retro workflow rewrite) cannot recur silently. **Do not gate this story's merge on the topology fix.**

If both stories merge in the same wave: confirm post-merge that on a real retro, the team config contains exactly 4 members and the guard emits its single confirmation line. If the topology fix landed correctly, the guard will be a no-op. If the topology fix regressed, the guard will halt with a diagnostic — exactly the behavior the safety net is designed to provide.

**Insertion point after `fix-retro-documenter-replication-defect` lands:** AC1 anchors the guard insertion to the prose "Spawn 4 agents via TeamCreate". If `fix-retro-documenter-replication-defect` lands first, that prose will have been rewritten to describe Shape A (individual Agent spawns). Locate the insertion point semantically: between the spawn block (whatever the current spawn prose says after the topology fix) and the `<action>Wait for the team to complete</action>` line — regardless of the spawn block's surface text. The insertion point is the gap between "spawning is done" and "waiting begins", not a specific string match.

### Files to Modify

| File | Change |
|---|---|
| `skills/momentum/skills/retro/workflow.md` | Insert one new singleton-guard step inside Phase 4, between the spawn block and the wait block |
| `skills/momentum/skills/retro/evals/eval-team-singleton-guard-halts-on-duplicate-documenter.md` | New eval (Task 2) |
| `skills/momentum/skills/retro/evals/eval-team-singleton-guard-passes-on-correct-composition.md` | New eval (Task 2) |

### What NOT to Change

- Phases 0, 1, 2, 3, 5, 5.5, 6 of `skills/momentum/skills/retro/workflow.md`
- The four system prompts inside the existing Phase 4 spawn block (auditor-human, auditor-execution, auditor-review, documenter) — including their SendMessage examples and JSON-string-format guidance
- `skills/momentum/skills/retro/SKILL.md` (no frontmatter or invocation changes)
- The existing Phase 4 wait-loop and findings-document presence check
- Any sibling skill (e.g., `momentum:distill`, `momentum:dev`, `momentum:sprint-dev`)
- The TeamCreate spawning approach itself — that is the topology fix's domain (`fix-retro-documenter-replication-defect`)

### Risk

Low. The guard is a pure additive read of a JSON file plus a count assertion. The failure mode is *not* introducing the guard — it is the guard producing false positives if the TeamCreate schema changes. AC5 mitigates this by tolerating both `name` and `agentType` field naming. The guard fires in <10 seconds (a single file read + count compare), so even if it produces a spurious halt, the loss is one halted retro and a clear diagnostic — vastly better than the status quo of 17 wasted agents and a corrupted audit document.

The only meaningful regression risk is if the guard prose is ambiguous enough that the orchestrator skips it entirely. Task 4 (EDD cycle) is the load-bearing mitigation: both behavioral evals must pass before the story is marked done.

### Architecture Compliance

- **Epic 10 (Impetus Core Infrastructure) — orchestrator behavioral guards.** This story directly implements the epic's stated scope: *"Includes Impetus workflow changes, momentum-tools.py script additions, agent observability/logging, sprint workflow modules (planning, dev, retro, quick-fix), journal/DuckDB tooling, and orchestrator behavioral guards."* The singleton guard is an orchestrator behavioral guard for the retro workflow.
- **Epic 11 (Agent Team Model) — deduplication guards.** Epic 11's strategic intent calls out *"Duplicate agent spawns wasted 47.8% of compute in one sprint."* The singleton guard is a deduplication guard for the retro workflow specifically — Epic 11 owns sprint-dev team composition; this story owns retro team composition.
- **Decision 27 (Findings Document) integrity.** The retro findings document (`retro-transcript-audit.md`) is only trustworthy if the team that produced it had the intended composition. A 17-agent run produces a corrupted audit because the documenter prompt replicated; the singleton guard prevents this corruption at the spawn boundary.

### Testing Requirements

EDD per the Momentum Implementation Guide below. The two behavioral evals in `skills/momentum/skills/retro/evals/` are the test layer for this story; there are no unit tests because skill instructions are non-deterministic LLM prompts. The AVFL checkpoint that `momentum:dev` runs at the end of the dev story validates the produced artifact against the ACs in this file.

### References

- [Source: _bmad-output/planning-artifacts/epics.md:642–660] — Epic 10: Impetus Core Infrastructure (orchestrator behavioral guards in scope)
- [Source: _bmad-output/planning-artifacts/epics.md:662–678] — Epic 11: Agent Team Model (duplicate agent spawn waste — 47.8% of compute in one sprint)
- [Source: skills/momentum/skills/retro/workflow.md:227–435] — Phase 4 (Step n=4) — the current Spawn auditor team via TeamCreate step where the guard is inserted
- [Source: skills/momentum/skills/retro/workflow.md:16] — Phase 4 critical note: *"auditors and documenter collaborate via SendMessage during analysis. This is the collaborative team pattern, not independent fan-out."*
- [Source: skills/momentum/skills/retro/workflow.md:18–33] — Phase 4 team-composition declaration (1 documenter + 3 distinct auditor roles — the canonical intended composition)
- [Source: _bmad-output/implementation-artifacts/sprints/sprint-2026-04-08/retro-transcript-audit.md:84–88] — *"Retro Pipeline Required 3 Attempts: 17 Agents for 4 Roles"* (RV-05; the previously-flagged-and-unactioned signal that justifies this story)
- [Source: _bmad-output/implementation-artifacts/sprints/sprint-2026-04-08/audit-extracts/agent-summaries.jsonl] — direct evidence: `{'documenter': 8, 'auditor-execution': 3, 'auditor-review': 3, 'auditor-human': 3}` for sprint-2026-04-08's retro
- [Source: _bmad-output/implementation-artifacts/stories/fix-retro-documenter-replication-defect.md] — sibling story: topology fix at the TeamCreate spawn shape (root cause); this story is the prophylactic count guard
- [Source: TeamCreate tool documentation] — *"Team config location: `~/.claude/teams/{team-name}/config.json`. The config file contains a `members` array with each teammate's name, agentId, agentType."*

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 3, 4, 5 → skill-instruction (EDD — workflow.md changes)
- Task 2 → skill-instruction (EDD — eval files in `skills/momentum/skills/retro/evals/`)

A reminder for this sprint: Gherkin specs exist for sprint-2026-04-27 (in `_bmad-output/implementation-artifacts/sprints/sprint-2026-04-27/specs/`) but are off-limits to the dev agent — implement against the plain English ACs in this story file only, never against `.feature` files (Decision 30 black-box separation).

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing the workflow change:**
1. Write the 2 behavioral evals in `skills/momentum/skills/retro/evals/` per AC7:
   - `eval-team-singleton-guard-halts-on-duplicate-documenter.md` — describes the duplicate-documenter scenario and the expected HALT + diagnostic behavior
   - `eval-team-singleton-guard-passes-on-correct-composition.md` — describes the correct-composition scenario and the expected silent pass-through
   - Format each eval as: *"Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"*
   - Test behaviors and decisions, not exact output text
   - Match the format used by the three existing retro evals in the same directory

**Then implement:**
2. Insert the singleton guard step into `skills/momentum/skills/retro/workflow.md` Phase 4 per AC1–AC6

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Provide it: (a) the eval's scenario as its task, and (b) the modified workflow.md Phase 4 contents as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If both evals match → tasks complete
5. If any eval fails → diagnose the gap in the guard prose, revise the workflow.md, re-run (max 3 cycles; surface to developer if still failing)

**NFR compliance — applies because this story modifies skill files:**
- This story does NOT modify `skills/momentum/skills/retro/SKILL.md` frontmatter — the description-length / model / effort frontmatter checks (NFR1, FR23) are not triggered.
- The workflow.md file should remain coherent and within reasonable token budget. The singleton guard step is small (a few lines of prose) and will not push the file over the 5000-token threshold; no overflow into `references/` is required (NFR3).
- No new `momentum:` namespace prefix is introduced — this story does not create a new skill (NFR12).

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2 behavioral evals written in `skills/momentum/skills/retro/evals/` per AC7
- [ ] EDD cycle ran — both eval behaviors confirmed (or failures documented with explanation)
- [ ] Phase 4 modifications confined to the new guard step + the spawn block's `team_name` capture if needed (verified by `git diff` per Task 5)
- [ ] No edits to `skills/momentum/skills/retro/SKILL.md` (verified by `git diff`)
- [ ] No edits to other retro phases (verified by `git diff` per AC6)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the modified workflow.md against this story's ACs)

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

### Completion Notes List

### File List
