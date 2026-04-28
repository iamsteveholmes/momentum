---
title: Harden sprint-dev Phase 5 spawn prompts (systemic)
story_key: harden-sprint-dev-phase5-spawn-prompts
status: ready-for-dev
epic_slug: sprint-dev-workflow
feature_slug:
story_type: practice
depends_on: []
touches:
  - skills/momentum/skills/sprint-dev/workflow.md
  - skills/momentum/agents/e2e-validator.md
  - skills/momentum/agents/qa-reviewer.md
---

# Harden sprint-dev Phase 5 spawn prompts (systemic)

## Story

As a Momentum practice operator,
I want sprint-dev's Phase 5 reviewer spawn pathway and the validator/QA agent definitions hardened so that service state is never pre-announced and live testing is never bypassed,
so that E2E and QA gates reliably exercise HTTP/SSE and other live-service scenarios instead of misclassifying them as MANUAL when the spawn prompt happens to mention "the backend is not running."

## Description

The nornspun sprint-2026-04-12 retrospective surfaced two systemic findings (auditor-review RQ-003 and RQ-004): the sprint-dev Phase 5 spawn block pre-announced service state ("the backend is NOT currently running") and offered pytest as a fallback path, which the spawned E2E validator interpreted as explicit permission to skip live testing. As a result, 8 HTTP/SSE scenarios were classified as MANUAL when they should have been executed end-to-end. The QA Reviewer spawn pattern carried the same shape and is at risk of the same regression.

Two prior commits (`65b7bca`, `c83ed4b`) already hardened `skills/momentum/agents/e2e-validator.md` with an Environment Prerequisites section and a MANUAL-only-for-human-UI Critical Constraint, and added the verbatim spawn-prompt constraints in `skills/momentum/skills/sprint-dev/workflow.md` Phase 5 (lines 531–540). The `qa-reviewer.md` agent definition has not yet been hardened — it still has no service-startup guidance and no MANUAL-classification constraint. If a future spawn-prompt edit drifts (paraphrases, omits, or weakens the verbatim block) the e2e-validator definition holds the line, but the QA reviewer has nothing in its definition that prevents the same regression.

This story closes the remaining gap with **defense in depth**: confirm and minimally tighten layer (a) — the workflow Phase 5 spawn block — and layer (b) — `e2e-validator.md`; and add the symmetric protection at layer (c) — `qa-reviewer.md`. The agent-definition layer must be self-sufficient: even if the workflow spawn prompt regresses, the agent's own constraints prevent service-state-driven test skipping and MANUAL misclassification.

**Pain context (verbatim from retro handoff):** auditor-review RQ-003, RQ-004 from nornspun sprint-2026-04-12. Phase 5 E2E-validator spawn prompt pre-announced "the backend is NOT currently running" and offered pytest as a fallback, giving the agent explicit permission to skip live testing. 8 HTTP/SSE scenarios misclassified as MANUAL. QA Reviewer prompt showed the same pre-declaration pattern.

**Architecture alignment:** Decision 34 (AVFL Scan Profile and Hybrid Resolution Team) defines QA Reviewer and E2E Validator as concurrent Phase 5 reviewers. Decision 35 (Agent Definition Files vs SKILL.md Boundary) places both as agent definition files (`agents/qa-reviewer.md`, `agents/e2e-validator.md`) — pure spawned workers, never user-invoked. The hardening lives at the agent-definition layer because that is the durable artifact the team has chosen for this role.

## Acceptance Criteria

1. **No pre-announcement of service state in workflow.md Phase 5 spawn block.** `skills/momentum/skills/sprint-dev/workflow.md` Phase 5 (the QA Agent and E2E Validator spawn block) contains no statement that asserts services are or are not currently running. Phrases like "the backend is not currently running," "services are already up," or any equivalent service-state assertion are absent. Service-state observation is delegated to the agent at execution time.

2. **No pytest-as-fallback offer in workflow.md Phase 5 spawn block.** The Phase 5 E2E Validator spawn block contains no language presenting pytest (or any unit-test runner) as a substitute path for live behavioral validation. The existing constraint that pytest is QA's domain and must not be used as a substitute is preserved verbatim.

3. **MANUAL classification is constrained in the workflow.md Phase 5 spawn block.** The Phase 5 E2E Validator spawn block continues to specify (verbatim, do-not-paraphrase) that MANUAL applies only to scenarios requiring a human to physically observe a visual UI, and that missing infrastructure is ERROR (or BLOCKED if cmux itself is absent), never MANUAL. The verbatim-do-not-paraphrase directive is preserved.

4. **`e2e-validator.md` retains its Environment Prerequisites and MANUAL-classification constraints.** `skills/momentum/agents/e2e-validator.md` still contains an Environment Prerequisites section (or equivalent) directing the agent to follow the project's `.claude/rules/e2e-validation.md` Environment Startup before executing scenarios, and Critical Constraints stating that MANUAL is only for genuine human-interaction scenarios and missing infrastructure is ERROR. No regression from the current state.

5. **`qa-reviewer.md` gains an Environment Prerequisites section.** `skills/momentum/agents/qa-reviewer.md` gains a section (named "Environment Prerequisites" for parity with `e2e-validator.md`) that directs the QA reviewer to start required services per the project's `.claude/rules/e2e-validation.md` Environment Startup procedure before running tests that depend on live services, and explicitly states that contextual claims in the spawn prompt about service state ("the backend is not running") are context, not permission to skip live test execution. If `e2e-validation.md` is absent from the project, the section directs the reviewer to report BLOCKED rather than fall back to static inspection.

6. **`qa-reviewer.md` gains a Critical Constraints section covering live-test execution and AC-verification semantics.** `skills/momentum/agents/qa-reviewer.md` gains a Critical Constraints section that codifies: (i) reading source files alone is never a substitute for executing the test suite (a source file containing the right words proves nothing about runtime behavior); (ii) every AC must be checked against actual evidence (tests run, code paths executed, observable outputs) — not against the presence of a string in a file; (iii) AC status MISSING is never an acceptable shortcut when the reviewer has not attempted execution; missing infrastructure is reported as BLOCKED, not as MISSING.

7. **Defense-in-depth holds against a regressed spawn prompt.** The constraints in `e2e-validator.md` (AC4) and `qa-reviewer.md` (AC5, AC6) are written to be self-sufficient: each agent's behavior is correctly bounded even if the Phase 5 spawn prompt is later edited to remove or weaken its verbatim constraints. Each agent definition's Environment Prerequisites and Critical Constraints sections explicitly state that any spawn-prompt context about service state is context-only and does not override these constraints.

8. **Story-cycle EDD evidence committed.** At least 2 behavioral evals are present under `skills/momentum/agents/evals/` (existing `evals/` directory) covering the new qa-reviewer behavior: one eval verifying that a QA reviewer given a "backend is not running" spawn prompt still attempts to start services and execute tests (does not skip to MISSING), and one eval verifying that a QA reviewer encountering missing infrastructure reports BLOCKED rather than MISSING. Eval format follows the project EDD pattern: one `.md` file per eval, named descriptively, content stating Given/When/Then in plain English.

9. **NFR compliance for modified agent definitions.** Each modified agent definition (`e2e-validator.md`, `qa-reviewer.md`) keeps its `description` field ≤150 characters, retains required frontmatter (`name`, `description`, `model`, `effort`, `tools`), and keeps body length ≤500 lines / ~5000 tokens (overflow content goes in `references/` with clear load instructions if needed).

10. **Regression closure documented.** The story's Dev Agent Record cross-references retro auditor-review RQ-003 and RQ-004 (nornspun sprint-2026-04-12) and states that the implemented changes close these findings at the agent-definition layer.

## Tasks / Subtasks

- [ ] **Task 1: Audit and minimally tighten `skills/momentum/skills/sprint-dev/workflow.md` Phase 5 spawn block** (AC1, AC2, AC3) — `skill-instruction`
  - [ ] 1.1 Read the current Phase 5 step (`<step n="5">`, approximately lines 503–594) end-to-end. Re-verify exact line ranges by opening the file — line numbers shift over time.
  - [ ] 1.2 Verify no service-state pre-announcement is present in the QA Agent spawn block (around lines 522–525) or the E2E Validator spawn block (around lines 527–540). If any such statement is found, remove it.
  - [ ] 1.3 Verify the E2E Validator's verbatim-do-not-paraphrase block (currently around lines 531–540) is intact: (1) follow `.claude/rules/e2e-validation.md` Environment Startup before any scenario; (2) no pytest as substitute, BLOCKED on inability to start services; (3) MANUAL only for visual-UI human-interaction scenarios. If any item is weakened or paraphrased, restore the strict wording.
  - [ ] 1.4 Add a parallel verbatim-do-not-paraphrase block to the QA Agent spawn description (around lines 522–525) with these constraints: (1) follow `.claude/rules/e2e-validation.md` Environment Startup before running any test that depends on live services; (2) no static-inspection-as-AC-verification; (3) missing infrastructure is BLOCKED, not MISSING. The block must contain the same directive as the E2E block: "Spawn prompt MUST include these constraints verbatim — do not paraphrase or omit. The agent definition does not make these redundant; they override any contextual claims in the spawn prompt about service state."
  - [ ] 1.5 Confirm no other Phase 5-adjacent step (Phase 4d, Phase 6, Phase 7) re-introduces a service-state pre-announcement.

- [ ] **Task 2: Audit `skills/momentum/agents/e2e-validator.md` and confirm no regression** (AC4, AC7, AC9) — `skill-instruction`
  - [ ] 2.1 Confirm the Environment Prerequisites section (currently lines 30–36) is present and directs the agent to follow the project's `.claude/rules/e2e-validation.md` Environment Startup before any scenario.
  - [ ] 2.2 Confirm the Critical Constraints section (currently lines 16–28) still includes: (i) test behavior not code; (ii) reading source files is never a substitute for execution; (iii) MANUAL only for human-interaction; (iv) missing infrastructure is ERROR not MANUAL; (v) every scenario must be attempted.
  - [ ] 2.3 Confirm the explicit defense-in-depth wording: "If a spawn prompt says 'the backend is not running' — that is context, not permission to skip. Start the services." If wording has drifted, restore.
  - [ ] 2.4 Confirm `description` field is ≤150 characters; confirm `name`, `model`, `effort`, `tools` frontmatter keys are present.
  - [ ] 2.5 Confirm body length ≤500 lines / 5000 tokens. (Currently ~197 lines — well within budget.)

- [ ] **Task 3: Add Environment Prerequisites and Critical Constraints sections to `skills/momentum/agents/qa-reviewer.md`** (AC5, AC6, AC7, AC9) — `skill-instruction`
  - [ ] 3.1 Add a new "Environment Prerequisites" section directly after the existing "Critical Constraints" section. Wording: direct the QA reviewer to follow the project's `.claude/rules/e2e-validation.md` Environment Startup before running any test that depends on live services. State explicitly: "If a spawn prompt says 'the backend is not running' — that is context, not permission to skip. Start the services per `.claude/rules/e2e-validation.md` and execute the test suite. If `.claude/rules/e2e-validation.md` is absent, report BLOCKED — do not fall back to static inspection."
  - [ ] 3.2 Extend the existing "Critical Constraints" section (or add an additional bullet block) with: (i) "Reading source files is NEVER a substitute for executing the test suite or exercising the AC's behavior. A source file containing the right strings proves nothing about runtime behavior." (ii) "Every AC must be checked against actual evidence — tests run, code paths executed, observable outputs — not against grep hits in a source file." (iii) "MISSING is never used as a shortcut when execution has not been attempted. Missing infrastructure is reported as BLOCKED."
  - [ ] 3.3 Confirm the new wording does not contradict the existing AC-classification triple (VERIFIED / PARTIAL / MISSING). MISSING remains valid when execution succeeded but no evidence of the AC was found; BLOCKED is the verdict when execution itself was prevented by missing infrastructure.
  - [ ] 3.4 Confirm `description` field is ≤150 characters; confirm `name`, `model`, `effort`, `tools` frontmatter keys are present and unchanged.
  - [ ] 3.5 Confirm body length ≤500 lines / 5000 tokens. (Currently ~131 lines — well within budget.)

- [ ] **Task 4: Add EDD evals for the new qa-reviewer behavior** (AC8) — `skill-instruction`
  - [ ] 4.1 Confirm the `skills/momentum/agents/evals/` directory exists; create it if absent.
  - [ ] 4.2 Write `eval-qa-reviewer-starts-services-when-spawn-prompt-claims-backend-not-running.md`. Format: "Given the QA reviewer is spawned with a sprint slug, list of stories with HTTP-touching ACs, and a spawn-prompt note saying 'the backend is not currently running,' the agent should follow `.claude/rules/e2e-validation.md` Environment Startup, bring up services, run the test suite, and verify ACs against actual test execution — not skip to MISSING based on the spawn-prompt claim."
  - [ ] 4.3 Write `eval-qa-reviewer-reports-blocked-on-missing-infrastructure.md`. Format: "Given the QA reviewer is spawned in a project where `.claude/rules/e2e-validation.md` is absent or services genuinely cannot be started, the agent should produce a QA Review Report with top-level Verdict: BLOCKED and an explanation — never produce a report classifying ACs as MISSING based on inability to execute."
  - [ ] 4.4 Run the EDD cycle: for each eval, spawn a subagent with the eval scenario as its task and the (modified) `qa-reviewer.md` content as context. Observe whether behavior matches expectations. Document results in Dev Agent Record. If any eval fails, diagnose the gap and revise the agent definition (max 3 cycles; surface to user if still failing).

- [ ] **Task 5: Final cross-document verification and Dev Agent Record summary** (AC7, AC10) — `skill-instruction`
  - [ ] 5.1 Re-read all three modified files (`workflow.md` Phase 5, `e2e-validator.md`, `qa-reviewer.md`) and confirm the constraints in each are self-sufficient — that is, each file's wording stands alone such that even if the spawn-prompt verbatim block is later weakened, the agent definition still bounds behavior correctly.
  - [ ] 5.2 Write Dev Agent Record completion notes that include: (a) summary of changes per file; (b) cross-reference to retro auditor-review RQ-003 and RQ-004 (nornspun sprint-2026-04-12); (c) statement that the agent-definition layer now closes these findings independently of spawn-prompt drift; (d) EDD eval results.

## Dev Notes

### Architecture Compliance

- **Decision 34 (AVFL Scan Profile and Hybrid Resolution Team):** QA Reviewer and E2E Validator are concurrent Phase 5 reviewers. The hardening preserves their distinct roles — E2E Validator owns black-box behavioral validation against Gherkin specs; QA Reviewer owns AC verification against merged code with test execution. Neither can substitute for the other.
- **Decision 35 (Agent Definition Files vs SKILL.md Boundary):** Both agents are pure spawned workers, never user-invoked. Their authority surface is the agent definition file at `skills/momentum/agents/{name}.md`. This story modifies those files in place.
- **Decision 30 (Black-Box Separation):** Phase 5 reviewers operate on the merged sprint branch / main. The dev agent never sees `.feature` files; the reviewer agents do. This story's constraints are about how reviewers run, not about what dev sees.
- **Decision 38 (Narrative Voice Contract):** Does not apply — agent definition files are spawned worker prompts, not Impetus dialog output.

### Testing Requirements

This is a `skill-instruction` story across all five tasks (workflow.md and two agent definition .md files are skill-instruction artifacts, not code). Standard TDD does not apply — use **EDD (Eval-Driven Development)** per `skills/momentum/skills/create-story/references/change-types.md`.

- **Tasks 1, 2:** No new evals required for audit-only confirmation, but if changes are made, update or add evals under `skills/momentum/skills/sprint-dev/evals/` (existing directory) covering the changed behavior.
- **Task 3:** Two new evals required (AC8) — see Task 4 subtasks. Place under `skills/momentum/agents/evals/`.
- **Task 4:** EDD cycle runs evals via subagent spawn — observe behavior match, max 3 cycles before surfacing failure.
- **Task 5:** Final manual verification by re-reading all modified files for self-sufficiency.

There is no test runner involved — these are LLM-prompt evals, not unit tests. The acceptance evidence is documented eval results in the Dev Agent Record.

### Implementation Guide

#### Files modified (UPDATE) — current state and what this story changes

**`skills/momentum/skills/sprint-dev/workflow.md`** (UPDATE; ~700 lines)
- *Current state:* Phase 5 (`<step n="5">`) spans approximately lines 503–594. The E2E Validator spawn block (around lines 527–540) already contains the verbatim-do-not-paraphrase constraints (around lines 531–540) added in commit `65b7bca`. The QA Agent spawn block (around lines 522–525) is currently bare — only describes the agent's input and output. The dev agent should re-verify these line ranges by opening the file (line numbers shift over time).
- *What this story changes:* Add a parallel verbatim-do-not-paraphrase constraint block to the QA Agent spawn description; verify no service-state pre-announcement leaked back in elsewhere.
- *What must be preserved:* The verbatim-do-not-paraphrase E2E block; the parallel-spawn structure for QA Agent / E2E Validator / Architect Guard; spawn registry deduplication (`{{spawn_registry}}` keys `sprint::qa-reviewer`, `sprint::e2e-validator`, `sprint::architecture-guard`); the parallel-execution structure ("Spawn eligible reviewers in parallel using individual Agent tool calls in a single message. NEVER use TeamCreate"); the consolidation flow into a unified fix queue.

**`skills/momentum/agents/e2e-validator.md`** (UPDATE; ~197 lines)
- *Current state:* Frontmatter with `name`, `description`, `model: sonnet`, `effort: medium`, `tools` (Read, Glob, Grep, Bash, ToolSearch). Critical Constraints section codifies: test behavior not code; reading source files is never a substitute for execution; cmux is mandatory for skill scenarios; MANUAL only for visual-UI human-interaction; missing infrastructure is ERROR not MANUAL; every scenario must be attempted. Environment Prerequisites section directs the agent to follow `.claude/rules/e2e-validation.md` Environment Startup. Subsequent sections cover Skill and Workflow Testing via cmux, Large File Handling, Output Format, Returning Results (SendMessage via ToolSearch), Verdict Rules.
- *What this story changes:* Audit only — no expected modifications unless drift is found.
- *What must be preserved:* Every constraint listed above. The defense-in-depth wording on line 34 ("If a spawn prompt says 'the backend is not running' — that is context, not permission to skip. Start the services."). Every Critical Constraints bullet. The cmux-mandatory directive. The SendMessage / ToolSearch sequence.

**`skills/momentum/agents/qa-reviewer.md`** (UPDATE; ~131 lines)
- *Current state:* Frontmatter with `name`, `description`, `model: sonnet`, `effort: medium`, `tools` (Read, Glob, Grep, Bash, ToolSearch). Critical Constraints section is minimal: only "READ-ONLY" and "review the integrated codebase" bullets. No Environment Prerequisites section. Review Process section covers: load sprint context, run tests, verify ACs per story (VERIFIED / PARTIAL / MISSING), cross-story integration check. Subsequent sections cover Large File Handling, Output Format, Returning Results, Verdict Rules.
- *What this story changes:* Add Environment Prerequisites section after Critical Constraints; extend Critical Constraints with three additional bullets (source-files-not-substitute, AC-evidence-against-execution, MISSING-not-shortcut).
- *What must be preserved:* All existing structure. Frontmatter unchanged. Tool list unchanged. Output Format / Verdict Rules unchanged. The VERIFIED / PARTIAL / MISSING / BLOCKED classification semantics — extended only insofar as MISSING vs BLOCKED is now disambiguated explicitly.

#### Defense-in-depth wording template (use verbatim or near-verbatim)

The phrase that ties the agent-definition layer to the spawn-prompt layer is:

> "If a spawn prompt says 'the backend is not running' — that is context, not permission to skip. Start the services per `.claude/rules/e2e-validation.md`."

This phrase already appears in `e2e-validator.md` (line 34). Replicate it in `qa-reviewer.md` Environment Prerequisites with the equivalent execution path ("run the test suite" instead of "execute scenarios").

#### Black-box separation reminder

This is a `skill-instruction` story and Decision 30 black-box separation applies generally. Gherkin specs for the active sprint (`sprint/sprint-2026-04-27`) live at `_bmad-output/implementation-artifacts/sprints/sprint-2026-04-27/specs/` but are off-limits to the dev agent — implement against this story file's plain-English ACs only, never against `.feature` files.

### Project Structure Notes

- All three modified files live under `skills/momentum/`. No new top-level directories are created.
- New evals (Task 4) live under `skills/momentum/agents/evals/`. The directory may need to be created — confirm at Task 4.1.
- No changes to `.claude-plugin/plugin.json`, `_bmad-output/planning-artifacts/architecture.md`, or any other planning artifact. This story is implementation-only at the practice layer; the architecture decisions (34, 35, 30) already cover the structural model.
- No changes to `stories/index.json` or `sprints/index.json` from the dev agent — those are sole-write authorities (`momentum:sprint-manager`).

### References

- `_bmad-output/planning-artifacts/epics.md` — Epic 12: Sprint Execution Workflow (lines 682–697)
- `_bmad-output/planning-artifacts/architecture.md` — Decision 34 (Hybrid Resolution Team, ~line 1968), Decision 35 (Agent Definition Files vs SKILL.md Boundary), Decision 30 (Black-Box Separation), Sprint Execution Flow Phase 5 (~line 1648)
- `skills/momentum/skills/sprint-dev/workflow.md` — Phase 5 spawn block (`<step n="5">`, approximately lines 503–594); existing verbatim-do-not-paraphrase block (around lines 531–540)
- `skills/momentum/agents/e2e-validator.md` — Critical Constraints (lines 16–28); Environment Prerequisites (lines 30–36)
- `skills/momentum/agents/qa-reviewer.md` — Critical Constraints (lines 16–22) [target of Task 3 extension]
- `skills/momentum/skills/create-story/references/change-types.md` — EDD instructions for skill-instruction tasks
- `skills/momentum/references/agent-skill-development-guide.md` — Authoritative source for agent definition frontmatter, structure, and NFR compliance
- Recent commits hardening this area: `65b7bca` (e2e-validator spawn prompt constraints), `c83ed4b` (e2e-validator environment prerequisites), `3521935` (missing infrastructure is ERROR not MANUAL)
- Retro source: nornspun sprint-2026-04-12 retrospective handoff — auditor-review findings RQ-003 and RQ-004 (8 HTTP/SSE scenarios misclassified as MANUAL)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 5 → skill-instruction (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md, workflow.md, or agent definition .md files.** Skill instructions and agent definitions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the change:**
1. Write 2–3 behavioral evals in `skills/momentum/agents/evals/` (this story's primary eval target — create the directory if it does not exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-qa-reviewer-starts-services-when-spawn-prompt-claims-backend-not-running.md`).
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]."
   - Test behaviors and decisions, not exact output text.

**Then implement:**
2. Modify `skills/momentum/skills/sprint-dev/workflow.md` Phase 5 (Tasks 1, 2 — audit-and-tighten).
3. Modify `skills/momentum/agents/e2e-validator.md` (Task 2 — audit-only, no expected change unless drift found).
4. Modify `skills/momentum/agents/qa-reviewer.md` (Task 3 — add Environment Prerequisites and extend Critical Constraints).

**Then verify:**
5. Run evals: for each eval file under `skills/momentum/agents/evals/`, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the modified `qa-reviewer.md` (or `e2e-validator.md` for cross-checks) by passing the file contents as context. Observe whether the subagent's behavior matches the eval's expected outcome.
6. If all evals match → task complete.
7. If any eval fails → diagnose the gap in the agent definition or workflow constraints, revise, re-run (max 3 cycles; surface to user if still failing).

**NFR compliance — mandatory for every skill-instruction task:**
- Each modified `.md` file's `description` field (frontmatter) must be ≤150 characters (NFR1) — count precisely. Confirm `e2e-validator.md` description (current: 209 chars, over by 59 — check with developer whether to tighten or treat as exempt-as-existing) and `qa-reviewer.md` description (current: 158 chars, over by 8 — same situation, marginal).
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23). Both agent definitions already comply; preserve.
- Modified file body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3). `e2e-validator.md` is currently ~197 lines, `qa-reviewer.md` is ~131 lines — significant headroom.
- Skill names use `momentum:` namespace prefix (NFR12 — applies to skills, not agent definitions). Agent definitions use bare names (`qa-reviewer`, `e2e-validator`) per Decision 35.

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/agents/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] Each modified file's `description` ≤150 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] Each modified file body ≤500 lines / 5000 tokens confirmed (overflow in `references/` if needed)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the implemented changes against story ACs)

### Black-Box Separation Reminder (Decision 30)

Gherkin specs for the active sprint exist at `_bmad-output/implementation-artifacts/sprints/sprint-2026-04-27/specs/` but are **off-limits to the dev agent.** Implement against this story file's plain-English Acceptance Criteria only — never open or read `.feature` files. The black-box separation is a binding architectural decision: the dev agent's input is this story; the QA Reviewer's and E2E Validator's input is the Gherkin specs; they must not converge on the dev side.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
