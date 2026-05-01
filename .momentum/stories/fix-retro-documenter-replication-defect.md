---
title: Fix retro documenter replication defect (AC4 regression)
story_key: fix-retro-documenter-replication-defect
status: ready-for-dev
epic_slug: impetus-core
feature_slug:
story_type: defect
priority: critical
depends_on: []
touches:
  - skills/momentum/skills/retro/workflow.md
---

# Fix retro documenter replication defect (AC4 regression)

Status: ready-for-dev

## Story

As the retro orchestrator,
I want to spawn exactly one documenter and N distinct auditors (no duplicate documenter spawns from a single TeamCreate call),
so that retro runs match AC4 of `retro-workflow-rewrite` and produce coherent, non-replicated audit output without burning tokens on idle duplicates.

## Description

**Defect against:** `retro-workflow-rewrite` (AC4 — "Retro spawns an auditor team with 3 specialized roles (human, execution, review) plus 1 documenter, all communicating via SendMessage").

**Observed behavior.** Despite AC4 specifying 3 auditors + 1 documenter, actual runs produce N× duplicate documenters (evidence from `audit-extracts/agent-summaries.jsonl` for each sprint):
- sprint-2026-04-08 retro: 8× documenter, 3× auditor-execution, 3× auditor-review, 3× auditor-human — 17 agents total for an intended 4-agent team.
- sprint-2026-04-10 retro: 10× documenter, 3× auditor-review, 2× auditor-human, 2× auditor-execution — 17 agents total.

**Diagnostic signal.** Identical `tool_use_id` across the 10 documenter transcripts in the sprint-04-10 retro confirms replication from a single API call rather than distinct spawns. The duplication is not the orchestrator looping over TeamCreate; it is TeamCreate (or the way the retro workflow expresses its team) generating N× workers under one tool invocation.

**Root cause hypothesis (to be confirmed by the dev agent during diagnosis).** The current `<team-composition>` block in `skills/momentum/skills/retro/workflow.md` declares all four roles (`auditor-human`, `auditor-execution`, `auditor-review`, `documenter`) with `spawning="team-create"` and `concurrency="parallel"` (workflow.md lines 18–33). The Phase 4 prose then says "Spawn 4 agents via TeamCreate" with one block of system prompts per role. The defect appears to be that the documenter — a singleton coordinator — is being declared inside the same `team-create` group as the auditors, causing TeamCreate to multiplex it. Auditors are conceptually distinct independent workers (fan-out targets that happen to need SendMessage to one shared peer); the documenter is the peer. The fix is to express that topology explicitly so the documenter is a single coordinator, never multiplexed.

**Fix shape.** Replace the "all four roles in one TeamCreate group" topology with: **single orchestrator (the retro skill itself) → 1 documenter (single Agent spawn or sole TeamCreate `documenter` role) → N distinct auditors (fan-out via individual Agent spawns, each carrying the documenter handle for SendMessage)**. The retro skill orchestrator is the only fan-out point; the documenter is never multiplied per-instance.

**Source pain.** Findings E14 and E15 from the nornspun sprint-2026-04-12 retro (`auditor-execution`). Prior retro flagged this as RV-05 in sprint-2026-04-08 retro and it went unactioned. Signal type: workflow defect. Escalating multiplier: 5× → 10× duplicate documenters in a single retro interval.

**Relationship to `retro-team-singleton-guard` (also in this sprint).** This story is the **topology fix**: it changes how the retro workflow expresses agent spawning so duplicate documenters cannot occur. `retro-team-singleton-guard` is the **assertion layer**: it adds a post-spawn Phase 4 guard that the assembled team matches the intended counts (1 documenter + 3 auditors) and halts otherwise. The two stories are complementary:
- This story removes the cause of the duplication.
- `retro-team-singleton-guard` adds belt-and-suspenders verification so any future regression of this kind is caught at runtime, not at retro audit.

This story does not depend on `retro-team-singleton-guard` and is independently mergeable. The singleton-guard story can be developed in parallel; if that story lands first, the assertions it adds will pass once this topology fix lands. If this story lands first, the team count is already correct; the guard story then formalizes the contract.

## Acceptance Criteria

1. **Topology declaration corrected.** The `<team-composition>` block in `skills/momentum/skills/retro/workflow.md` (Phase 4) declares the documenter as a single coordinator role distinct from the auditor fan-out group. Acceptable shapes (dev agent picks the one that prevents documenter multiplication while preserving SendMessage between auditors and documenter, per the spawning-patterns.md decision rule):
   - **Shape A (preferred):** Documenter spawned as a singleton coordinator (1 Agent spawn or 1 TeamCreate role declared with explicit `cardinality="1"` / single-spawn semantics), with auditors fanned out via 3 individual Agent calls in a single message, each given the documenter's team/agent handle so they can SendMessage to it; OR
   - **Shape B:** All 4 roles remain in TeamCreate but with each role declared exactly once and the workflow prose verifying `tool_use_id` uniqueness post-spawn before proceeding. Shape A is preferred because it eliminates the multiplexing-prone path entirely.

2. **Phase 4 prose matches the declared topology.** The "Spawn N agents via TeamCreate" / "Spawn N agents" prose in Phase 4 is rewritten so it cannot be read as "spawn one block per role with N implied" — the spawn instruction is unambiguous about creating exactly 1 documenter and exactly 3 auditors (one per type). The system prompts for each role are unchanged in content (auditor-human reads user-messages.jsonl etc.; documenter waits for SendMessage findings); only the spawn topology changes.

3. **Retro-lead / fan-out-per-instance ruled out.** The workflow contains no path — implicit or explicit — where a "retro-lead" intermediate agent fans out one instance per documenter or per auditor. The retro skill itself is the sole orchestrator. (No retro-lead agent exists today; this AC documents the constraint to prevent reintroduction.)

4. **Fix verified by re-running on prior sprint data.** Dry-running `/momentum:retro` against a prior sprint (developer's choice — sprint-2026-04-08 or sprint-2026-04-10 are the canonical regression cases) produces:
   - Exactly 1 documenter agent in the spawned team.
   - Exactly 3 auditor agents (auditor-human, auditor-execution, auditor-review) — no duplicates of any auditor type.
   - Total Phase 4 agent count = 4.
   - Distinct `tool_use_id` per spawned agent in the session transcript (no two agents share a `tool_use_id`, ruling out single-call replication).
   The verification method (DuckDB query against the new session JSONL, or direct inspection of the retro session transcript) is documented in the Dev Agent Record `Completion Notes` with the exact query used and the resulting agent count.

5. **Regression bounds for prior escalation cases.** When the retro is rerun against the audit extracts of sprint-2026-04-08 (which historically produced 17 agents) and sprint-2026-04-10 (which also produced 17), agent count is exactly 4 in both — not the historical 17. (If a true rerun against archived extracts is impractical because some Phase-1/2 inputs are no longer reproducible, the dev agent runs Phase 4 in isolation against the archived `audit-extracts/` directories of those sprints and reports the agent count from the spawn step.)

6. **AC4 of `retro-workflow-rewrite` restored.** This story explicitly cites and respects AC4 of `retro-workflow-rewrite`: "Retro spawns an auditor team with 3 specialized roles (human, execution, review) plus 1 documenter, all communicating via SendMessage." After the fix, AC4 holds in practice on every retro run.

7. **Functional equivalence preserved.** The findings document (`_bmad-output/implementation-artifacts/sprints/{sprint-slug}/retro-transcript-audit.md`) is still produced by the documenter with the required sections (Executive Summary, What Worked Well, What Struggled, User Interventions, Story-by-Story Analysis, Cross-Cutting Patterns, Metrics, Priority Action Items). Auditors still SendMessage findings to the documenter; the documenter still owns the file exclusively.

8. **Defect citation closed.** This story closes the workflow defect flagged in `auditor-execution` E14/E15 from the nornspun sprint-2026-04-12 retro. The Dev Agent Record references those findings and notes that prior retro RV-05 (sprint-2026-04-08) is also resolved by this fix.

## Tasks / Subtasks

- [ ] **Task 1 — Diagnose the exact replication trigger** (AC: 1, 4) — `skill-instruction`
  - [ ] Subtask 1.1: Re-read `skills/momentum/skills/retro/workflow.md` Phase 4 (lines ~227–434) and the `<team-composition>` block (lines 18–33). Document in Dev Agent Record `Debug Log References` exactly which construct in the workflow generates the duplicate documenter when interpreted by the runtime: the `<team-composition>` declaration, the inline "Spawn 4 agents via TeamCreate" prose, or the way the system prompt block is structured.
  - [ ] Subtask 1.2: If the duplicate-spawn cause is not unambiguous from static reading of the workflow, inspect one archived retro session transcript (e.g., sprint-2026-04-10's retro session JSONL) and trace the Phase-4 `tool_use_id` emission to confirm the call shape that produced 10 documenters under one tool use.
  - [ ] Subtask 1.3: Choose Shape A (preferred) or Shape B per AC1 and record the choice + rationale.

- [ ] **Task 2 — Rewrite the `<team-composition>` block for Phase 4** (AC: 1, 3) — `skill-instruction`
  - [ ] Subtask 2.1: Update the `<phase name="auditor-team" step="4">` block in `skills/momentum/skills/retro/workflow.md` so the documenter role is declared as a singleton coordinator separate from the auditor fan-out group. Use spawning attributes that match the chosen shape:
    - Shape A: auditor roles `spawning="individual" concurrency="parallel"`; documenter `spawning="individual"` (or `team-create` with explicit single-cardinality semantics) — declared as a coordinator role.
    - Shape B: keep `spawning="team-create"` for all four but ensure each role appears exactly once with no implicit cardinality, and add a `<critical>` directive in the workflow prose forbidding any pattern that multiplexes the documenter.
  - [ ] Subtask 2.2: Add a `<critical>` directive at the top of Phase 4 stating: "Exactly 1 documenter and exactly 3 auditors. The documenter is a singleton coordinator and must never be multiplexed within a TeamCreate group." Cite Decision 41 (Workflow Team Composition Declarations) and `~/.claude/rules/spawning-patterns.md` (Fan-Out vs TeamCreate Decision Rule) in the directive's prose so future maintainers can trace the rationale.

- [ ] **Task 3 — Rewrite the Phase 4 spawn prose** (AC: 2, 3, 7) — `skill-instruction`
  - [ ] Subtask 3.1: Replace "Spawn 4 agents via TeamCreate" with prose that matches the chosen topology unambiguously. For Shape A, this is "Create the documenter via TeamCreate (or single Agent spawn) as the sole coordinator. Then in a single message, fan out 3 individual Agent spawns — auditor-human, auditor-execution, auditor-review — each given the documenter's team handle for SendMessage." For Shape B, this is "Create the team via a single TeamCreate call declaring each of the 4 roles exactly once."
  - [ ] Subtask 3.2: Preserve the existing system-prompt content for each role (file paths, finding shape, SendMessage protocol, JSON serialization warnings). Only the spawn instruction changes.
  - [ ] Subtask 3.3: Remove or rewrite any prose that could be misread as "spawn-per-instance" or "fan-out per role." There is no retro-lead intermediate. The retro skill itself is the only orchestrator.

- [ ] **Task 4 — Behavioral evals for the topology fix** (AC: 4, 5) — `skill-instruction`
  - [ ] Subtask 4.1: Create `skills/momentum/skills/retro/evals/` if it does not exist. Add 2 behavioral evals as `.md` files:
    - `eval-phase-4-spawns-exactly-one-documenter.md`: "Given a retro run reaches Phase 4 with prepared audit-extracts, the workflow should spawn exactly 1 documenter and 3 distinct auditor agents (auditor-human, auditor-execution, auditor-review). The agent count for Phase 4 is 4."
    - `eval-phase-4-no-duplicate-tool-use-id.md`: "Given Phase 4 spawns its team, every spawned agent has a distinct tool_use_id in the session transcript. No two agents share a tool_use_id (which would indicate single-call replication)."
  - [ ] Subtask 4.2: Run the evals per the EDD protocol in the Momentum Implementation Guide section below.

- [ ] **Task 5 — Verify against prior regression cases** (AC: 4, 5, 8) — `skill-instruction`
  - [ ] Subtask 5.1: Identify the archived `audit-extracts/` for sprint-2026-04-08 and sprint-2026-04-10 (under `_bmad-output/implementation-artifacts/sprints/{slug}/audit-extracts/`).
  - [ ] Subtask 5.2: Run `/momentum:retro` (or equivalent Phase-4-only invocation) against each archived sprint with the topology fix in place. Capture the spawned agent count for Phase 4 of each run.
  - [ ] Subtask 5.3: Document in Dev Agent Record: agent count for sprint-04-08 retro rerun (expected 4, historically 10); agent count for sprint-04-10 retro rerun (expected 4, historically 17); the DuckDB or jq query used to count agents from the new retro session JSONL; and a one-line confirmation that distinct `tool_use_id` was observed.

- [ ] **Task 6 — Cross-reference and close-out** (AC: 6, 8) — `skill-instruction`
  - [ ] Subtask 6.1: In the Dev Agent Record `Completion Notes`, cite AC4 of `retro-workflow-rewrite` and the two source findings (E14/E15 from nornspun sprint-2026-04-12 retro; RV-05 from sprint-2026-04-08 retro) as closed by this story.
  - [ ] Subtask 6.2: Note the relationship with `retro-team-singleton-guard` — this story is the topology fix; the singleton-guard story will add the runtime assertion. If the singleton-guard story has already merged before this one, run its assertion against the fixed workflow as additional verification.

## Dev Notes

### Architecture Compliance

- **Decision 27 (Transcript Audit Retro)** — preserved. The retro still uses DuckDB preprocessing (Phase 2) and the auditor team (Phase 4) to produce `retro-transcript-audit.md`. Only the team-spawn topology of Phase 4 changes.
  - Source: `_bmad-output/planning-artifacts/architecture.md` Decision 27 section and lines 1933–1941 (Wave 2: Auditor Team).
- **Decision 41 (Workflow Team Composition Declarations, 2026-04-06)** — directly governs this story. Decision 41 requires workflows that spawn agents to declare team composition explicitly via `<team-composition>` XML elements with three fields: `required-roles`, `spawning-mode` (`individual` vs `team`), and `concurrency` (`parallel` vs `sequential`). The current retro `<team-composition>` block declares all four roles with `spawning="team-create" concurrency="parallel"` — the topology that is producing the defect. The fix updates the declaration to express documenter-as-singleton vs auditors-as-fan-out semantics correctly.
  - Source: `_bmad-output/planning-artifacts/architecture.md` Decision 41 section (lines 2139–2168) and the Decision 41 application table (where retro is **not yet listed** — this story may also implicitly expand that table; if the dev agent's reading of architecture.md indicates retro should be added to the application table, that is a separate spec-impact item to flag in the post-merge AVFL, not in this story's scope).
- **`~/.claude/rules/spawning-patterns.md` (Fan-Out vs TeamCreate Decision Rule)** — the rule says "Can each agent complete its work without talking to any other agent? Yes → Fan-out (individual Agent spawns). No → TeamCreate." Auditors **must** SendMessage to the documenter, so on its face TeamCreate is correct. But the rule also applies to **the documenter individually**: the documenter does not collaborate with another documenter. Therefore the documenter is a singleton coordinator and the auditor group is a fan-out that happens to address one shared peer. The cleanest expression of this is Shape A.
- **Decision 30 (Black-box separation)** — N/A in mechanics. Phase 4 reads `audit-extracts/`, not the sprint's `specs/` directory. The dev agent does not read or write `.feature` files for this story. (The Gherkin-spec reminder is included in the Implementation Guide below per workflow standard.)

### Testing Requirements

EDD (Eval-Driven Development) applies because all changes are to a SKILL workflow file (`workflow.md`). No unit tests apply; behavioral evals replace them.

- 2 behavioral evals in `skills/momentum/skills/retro/evals/`:
  1. `eval-phase-4-spawns-exactly-one-documenter.md` — verifies 1 documenter + 3 auditors after the fix.
  2. `eval-phase-4-no-duplicate-tool-use-id.md` — verifies distinct `tool_use_id` per spawn.
- Per-eval execution: Use the Agent tool to spawn a subagent. Give it (1) the eval scenario as its task and (2) load the retro skill by passing the SKILL.md and workflow.md contents as context. Observe whether the subagent's behavior matches the eval's expected outcome.
- All evals must pass before the story is complete; if any fail, diagnose the gap, revise, re-run (max 3 cycles; surface to user if still failing).
- Verification against archived sprint data (Task 5) is functional verification, not a unit test — captured in the Dev Agent Record as evidence of AC4/AC5 satisfaction.

### Implementation Guide

This section is populated by `momentum:create-story` after change-type classification (Step 4 of create-story workflow). See the `## Momentum Implementation Guide` block below.

### Project Structure Notes

- File touched: `skills/momentum/skills/retro/workflow.md` — only this file is modified by code.
- Directory created (if missing): `skills/momentum/skills/retro/evals/` — for the 2 behavioral evals.
- No script changes (`scripts/` not touched), no rule changes (`.claude/rules/` not touched), no settings.json changes, no agent definition changes.
- The retro `SKILL.md` does not need updates — only the `workflow.md` topology declaration and Phase 4 prose change. If during implementation the dev agent finds that `SKILL.md` references the team count or spawn pattern, update accordingly; otherwise leave it.

### References

- `_bmad-output/implementation-artifacts/stories/retro-workflow-rewrite.md` — origin story; AC4 is the regressed acceptance criterion this fix restores.
- `_bmad-output/implementation-artifacts/stories/retro-team-singleton-guard.md` — sibling story (assertion layer) in the same sprint. This story removes the cause; that story adds the runtime check.
- `skills/momentum/skills/retro/workflow.md` — primary file under modification. Specific zones (line numbers approximate as of story creation; dev agent should re-locate by anchor text, not by line number):
  - `<team-composition>` block: anchor `<team-composition>` opening tag (~line 18) through closing `</team-composition>` (~line 33).
  - Phase 4 spawn prose: anchor `<step n="4" goal="Spawn auditor team via TeamCreate` (~line 227) through end of step 4 (~line 434, just before Phase 5 header).
- `_bmad-output/planning-artifacts/architecture.md`:
  - Decision 27 (Transcript Audit Retro) — overall retro architecture.
  - Decision 41 (Workflow Team Composition Declarations) — governs `<team-composition>` declarations.
  - Lines 1933–1947 — Wave 2 auditor team description.
  - Lines 2139–2168 — Decision 41 spec.
- `~/.claude/rules/spawning-patterns.md` — Fan-Out vs TeamCreate decision rule.
- `_bmad-output/implementation-artifacts/sprints/sprint-2026-04-14/retro-transcript-audit.md` — likely contains the auditor-execution finding that elevated this defect (verify during diagnosis).
- nornspun sprint-2026-04-12 retro — original signal source (E14/E15). Cross-project reference; the findings narrative in the stub is the operative summary.

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 5, 6 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/retro/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-phase-4-spawns-exactly-one-documenter.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the SKILL.md, workflow.md, or reference files

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context (or invoke the skill via its Agent Skills name if installed). Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3)
- Skill names use `momentum:` namespace prefix (NFR12 — no naming collision with BMAD skills)

**Note on this story specifically:** The change is to `workflow.md`, not `SKILL.md`. NFR1 (description ≤150 chars) is unchanged because the SKILL.md description is not being modified. Verify during implementation that no incidental SKILL.md edit pushes its description over 150 characters; if so, revert that edit.

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/retro/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed (count the actual characters) — re-verify if SKILL.md was incidentally touched
- [ ] `model:` and `effort:` frontmatter present and correct on retro/SKILL.md (re-verify if SKILL.md was incidentally touched)
- [ ] workflow.md body ≤500 lines / 5000 tokens after the change (overflow in `references/` if needed) — count after the edit; if Phase 4 prose growth pushes total over 500, refactor large system prompts into `skills/momentum/skills/retro/references/auditor-prompts.md` with a load instruction
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the implemented workflow.md against story ACs)

### Gherkin spec separation reminder

Gherkin specs for this sprint live under `_bmad-output/implementation-artifacts/sprints/{sprint-slug}/specs/` and are off-limits to the dev agent — Decision 30 (black-box separation). The dev agent implements against the plain English ACs in this story file only, never against `.feature` files. Verifier agents (E2E Validator, etc.) own the `specs/` directory; dev agents do not read or write to it.

## Dev Agent Record

### Agent Model Used

_Populated by dev agent_

### Debug Log References

_Populated by dev agent_

### Completion Notes List

_Populated by dev agent_

### File List

_Populated by dev agent_
