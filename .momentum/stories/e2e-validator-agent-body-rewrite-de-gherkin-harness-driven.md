---
title: e2e-validator agent body rewrite — de-Gherkin, harness-driven
story_key: e2e-validator-agent-body-rewrite-de-gherkin-harness-driven
status: ready-for-dev
epic_slug: agent-team-model
feature_slug: momentum-agent-role-contracts
story_type: practice
depends_on:
  - momentum-harnessjson-schema-and-plugin-shipped-defaults
touches:
  - skills/momentum/agents/e2e-validator.md
  - skills/momentum/agents/evals/
---

# e2e-validator agent body rewrite — de-Gherkin, harness-driven

## Story

As a developer,
I want an e2e-validator agent body that reads method-polymorphic contracts and a harness profile instead of assuming Gherkin and a fixed stack,
so that the validator works across projects and stacks without prompt edits and stays consistent with the method-routed pipeline decided in DEC-029.

## Description

The current `e2e-validator.md` agent body has three concrete defects that this story corrects:

1. **Gherkin hardwiring.** The agent's "Load Gherkin Specs" step assumes all contracts are `.feature` files. DEC-029 D1 demotes Gherkin to one of six verification methods, routed by story change-type. The agent must accept any contract format — `.eval.yaml`, `.trigger.md`, `.smoke.sh`, `.review.md`, or `.feature` — and dispatch the right execution strategy per file extension / declared method.

2. **Stack leak.** The "Environment Prerequisites" section names `finch`, `PostgreSQL`, and `FastAPI` directly in the generic agent body. These are a consumer project's stack (Nornspun). They must be removed; environment startup is now declared in `momentum/verification-harness.json` per DEC-029 D3.

3. **Absent harness integration.** The agent has no mechanism for reading per-project env/driver/target declarations. After this story, the agent must load `momentum/verification-harness.json` at startup and use it to determine: environment startup + readiness probes, execution surface per change-type, driver binding (cmux / Skill-invoke / Maestro / Playwright / curl), platform/target matrix, and human-review carve-outs.

**Source decisions:** DEC-029 D1/D3 (primary); DEC-020 D1 (agent taxonomy — e2e role is one of nine universal base bodies; its rewrite must remain consistent with the nine-role ownership model).

**Intra-sprint dependency:** This story consumes `momentum/verification-harness.json`. The schema stub story (`momentum-harnessjson-schema-and-plugin-shipped-defaults`) must land before this story's implementation begins. The dependency is declared in `depends_on`.

**Out of scope:** The full sprint-dev rewrite (four-step flow, three-tier pipeline, PASS-sticky loop) is a downstream epic sequenced in DEC-029 Phase 2. This story is Phase 1 only: rewrite the validator body. Sprint-dev wiring is not touched here.

## Acceptance Criteria

### AC1 — Harness file loaded at startup

When the e2e-validator agent is spawned with a sprint slug and a project root, it reads `momentum/verification-harness.json` from the project root. If the file is absent, the agent reports BLOCKED with the message "momentum/verification-harness.json not found — cannot determine environment startup or execution drivers. Create verification-harness.json per the plugin defaults schema." It does not fall back to hardcoded environment assumptions.

### AC2 — No stack-specific references in the agent body

The rewritten `e2e-validator.md` contains no references to `finch`, `PostgreSQL`, `FastAPI`, or any other consumer-project technology. Environment startup and readiness probes are described generically, as "follow the steps declared in verification-harness.json under `environment.startup` and poll `environment.readiness_probe` until it passes."

### AC3 — Method-polymorphic contract dispatch

The agent's scenario execution loop reads each file in `.momentum/sprints/{sprint-slug}/specs/` and dispatches by contract type:

- `.feature` → existing Gherkin execution strategy (unchanged — Gherkin remains a valid method)
- `.eval.yaml` → EDD eval execution: spawn a subagent with the scenario and skill context, observe behavior, record PASS/FAIL
- `.trigger.md` → behavioral trigger execution: apply the described trigger via cmux and verify the observable outcome
- `.smoke.sh` → shell execution: run the script via Bash and verify exit code + output
- `.review.md` → document review: read the file being reviewed, compare against the criteria in the contract, record PASS/FAIL. _(Maps to DEC-029 D1's `research/spike → document review` method. The contract states what must be true about the reviewed document; the agent reads both the target document and the contract criteria and renders a judgment.)_

Unknown extensions are reported as ERROR with: "Unrecognized contract type: {extension}. No execution strategy available."

### AC4 — Harness-driven execution surface

For each scenario, the execution driver (cmux, Skill-invoke, Maestro, Playwright, or curl) is resolved from `verification-harness.json` under the `change_types.{change_type}.driver` field. If the harness declares `driver: cmux` for a scenario's change-type, the existing cmux procedure is used. If it declares `driver: maestro`, the agent invokes Maestro. If the field is absent for a given change-type, the agent falls back to its own heuristic and notes the fallback in the scenario's evidence field.

### AC5 — Harness-driven environment startup

The agent follows `verification-harness.json`'s `environment.startup` steps (a list of commands or Skill invocations) in sequence before executing any scenario. After each startup command, it polls `environment.readiness_probe` (a command whose exit code 0 means ready) with a configurable timeout. If the readiness probe does not pass within the timeout, the agent reports BLOCKED and halts — it does not proceed to scenario execution with an unverified environment.

### AC6 — Human-review carve-outs from harness

Scenarios whose change-type appears in `verification-harness.json`'s `human_review_carveouts` list are marked MANUAL automatically, without the agent attempting execution. The evidence field records: "Marked MANUAL per verification-harness.json human_review_carveouts for change-type: {change_type}."

### AC7 — Trivial-smoke escape hatch

If `verification-harness.json` declares `trivial_smoke_escape: true` for a change-type, the agent runs only the minimal smoke check declared in the contract (e.g., the first Given/Then of a `.feature` or the first step of a `.smoke.sh`) and marks the scenario PASS-with-smoke. Full execution is not performed. The evidence field records: "Trivial smoke escape applied per verification-harness.json."

### AC8 — DEC-020 taxonomy compliance

The rewritten agent frontmatter declares `name: e2e-validator` (matching DEC-020's nine-role taxonomy). The role statement at the top of the body reads: "You are an E2E Validator in Momentum's three-tier quality pipeline." The description field (≤ 250 characters) accurately reflects the harness-driven, method-polymorphic behavior without mentioning Gherkin as the exclusive format.

### AC9 — Backward compatibility for Gherkin-only harnesses

A project whose `verification-harness.json` does not declare any change-type–specific drivers (uses only plugin defaults) and whose sprint specs contain only `.feature` files must validate identically to the behavior before this story — no regressions for existing Gherkin-only workflows.

### AC10 — Spec quality classification preserved

The spec quality classification logic (untestable-scenario, outsider-test-failure tags) is carried forward unchanged. The rewrite does not remove or alter the `## Spec Quality Classification` section or its output format.

## Tasks / Subtasks

> **EDD ORDER REQUIRED:** This story uses Eval-Driven Development. Write evals (Tasks 1–3) BEFORE beginning implementation (Tasks 4–11). A dev agent that implements first has violated EDD.

- [ ] **Task 1 — Write eval: harness absent reports BLOCKED**
  Create `skills/momentum/agents/evals/eval-e2e-validator-harness-absent-reports-blocked.md` (create `evals/` directory if absent). Format: "Given a sprint with spec files in `.momentum/sprints/{slug}/specs/` but no `momentum/verification-harness.json` in the project root, the e2e-validator agent should report BLOCKED with an explanation about the missing harness file and halt without attempting scenario execution."

- [ ] **Task 2 — Write eval: .eval.yaml contract dispatched correctly**
  Create `skills/momentum/agents/evals/eval-e2e-validator-eval-yaml-contract-dispatched.md`. Format: "Given a sprint spec directory containing a `.eval.yaml` contract file (not a `.feature` file), the e2e-validator agent should dispatch the EDD eval execution strategy — spawning a subagent with the scenario as task — and not attempt Gherkin parsing."

- [ ] **Task 3 — Write eval: no stack-specific references in agent body**
  Create `skills/momentum/agents/evals/eval-e2e-validator-no-stack-references.md`. Format: "Given the rewritten `e2e-validator.md` agent body, a search for 'finch', 'PostgreSQL', and 'FastAPI' should return zero matches. Environment startup instructions should reference `verification-harness.json` fields generically, not name specific technologies."

- [ ] **Task 4 — Audit and annotate current agent body**
  Read `skills/momentum/agents/e2e-validator.md` in full. Annotate (in a scratch note, not in the file) every section that contains: (a) hardcoded stack references (finch, PostgreSQL, FastAPI), (b) Gherkin-only assumptions, (c) places where verification-harness.json integration will slot in. This produces the diff map for the rewrite.

- [ ] **Task 5 — Rewrite Environment Prerequisites section**
  Remove the hardcoded `finch`, `PostgreSQL`, `FastAPI` startup steps. Replace with a generic section: "Before executing any scenario, load `momentum/verification-harness.json`. Follow the steps in `environment.startup` in sequence. Poll `environment.readiness_probe` until exit 0 or timeout. Report BLOCKED if the probe does not pass." Add the BLOCKED-on-absent-harness guard (AC1).

- [ ] **Task 6 — Rewrite Input section to accept harness context**
  Update the `## Input` section to list three inputs: sprint slug, path to sprint specs directory, and (new) path to `momentum/verification-harness.json`. The AVFL findings list remains optional context as before.

- [ ] **Task 7 — Rewrite validation process Step 1: Load Contracts (replaces Load Gherkin Specs)**
  Replace "Load Gherkin Specs" with "Load Contracts." The new step reads all files from the sprint specs directory regardless of extension, classifies each by extension to determine contract type, and maps each to the dispatch table in AC3.

- [ ] **Task 8 — Rewrite validation process Step 2: Determine Execution Strategy (harness-driven)**
  Replace the static execution strategy decision table with harness-driven resolution: resolve driver from `verification-harness.json change_types.{change_type}.driver`; check `human_review_carveouts` for MANUAL classification; check `trivial_smoke_escape` for abbreviated execution. Add the `.eval.yaml`, `.trigger.md`, `.smoke.sh`, `.review.md` execution strategies alongside the preserved Gherkin strategy (AC3, AC4, AC6, AC7). Before implementing, read the harness schema from the dependency story to confirm field names.

- [ ] **Task 9 — Update frontmatter and role statement**
  Confirm frontmatter has `name: e2e-validator`, `model: sonnet`, `effort: medium`. Rewrite the role statement opening line to: "You are an E2E Validator in Momentum's three-tier quality pipeline." Update the description field to reflect method-polymorphic, harness-driven behavior without naming Gherkin as the exclusive format. Verify description ≤ 250 characters.

- [ ] **Task 10 — Verify DEC-020 taxonomy alignment**
  Read DEC-020 D1 (nine universal base bodies). Confirm the rewritten agent's role identity, behavioral constraints, and file ownership scope are consistent with the e2e role's position in the taxonomy. Note any alignment gaps and resolve them in the agent body.

- [ ] **Task 11 — Preserve unchanged sections**
  Verify that the following sections are carried forward without functional change: `## Skill and Workflow Testing via cmux (REQUIRED)`, `## Spec Quality Classification`, `## Large File Handling`, `## Output Format`, `## Returning Results`, `## Verdict Rules`. The `## Critical Constraints` section is updated only to remove the "finch/PostgreSQL/FastAPI" reference in the environment startup constraint; all other constraints remain.

- [ ] **Task 12 — Run evals and confirm**
  Run each eval (spawn a subagent with the eval scenario as its task, pass the rewritten agent body as context). All three evals must confirm expected behavior. Document results in Dev Agent Record.

## Dev Notes

### Architecture Compliance

**DEC-029 D1 — Method-routed verification:** The rewrite makes the agent method-polymorphic by dispatching on contract file extension. `.feature` files continue to use the existing Gherkin strategy unchanged. The new contract types (`.eval.yaml`, `.trigger.md`, `.smoke.sh`, `.review.md`) each get a distinct execution strategy. The dispatch table lives in the agent body's "Determine Execution Strategy" step.

**DEC-029 D3 — Per-project harness profile:** `momentum/verification-harness.json` is the sole source for: environment startup steps, readiness probes, per-change-type driver bindings, human-review carve-outs, and trivial-smoke escapes. The agent body contains no project-specific values. If a field is absent from verification-harness.json, the agent falls back to its own heuristic and notes the fallback — it never hard-errors on a missing optional field.

**DEC-020 D1 — Nine universal base bodies:** The e2e role is one of nine. Its file (`skills/momentum/agents/e2e-validator.md`) is plugin-shipped. The rewrite must not add new files to `skills/momentum/agents/` — the existing single file is the canonical base body. Role identity statement, behavioral constraints, output format contract, and file ownership scope must remain coherent with the nine-role taxonomy.

**Intra-sprint dependency:** This story depends on `momentum-harnessjson-schema-and-plugin-shipped-defaults` — specifically the `verification-harness.json` schema (field names, structure for `environment.startup`, `environment.readiness_probe`, `change_types.*.driver`, `human_review_carveouts`, `trivial_smoke_escape`). The rewrite must use the schema as specified in that story. Do not invent field names; read the produced schema before writing verification-harness.json access code in the agent body.

### Testing Requirements

This is a `skill-instruction` (agent definition) story. Use EDD — not TDD.

**Before writing:** Write 3 behavioral evals in `skills/momentum/agents/evals/` (Task 9). Run them after the rewrite to confirm behavioral correctness (Task 10).

**Backward compatibility check:** After the rewrite, verify that the existing Gherkin path is still intact by tracing the `.feature` dispatch path through the new execution strategy step. No behavioral change for `.feature` contracts is permitted (AC9).

**Format check:** After the rewrite, verify:
- Description field ≤ 250 characters (count precisely)
- `model:` and `effort:` frontmatter fields present
- No mention of `finch`, `PostgreSQL`, or `FastAPI` anywhere in the file (`grep -i "finch\|postgresql\|fastapi" skills/momentum/agents/e2e-validator.md` must return empty)

### Implementation Guide

### Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1–12 → skill-instruction (EDD) — writing evals and rewriting an agent definition file in `skills/momentum/agents/`

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for agent definition files.** Agent definitions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the rewritten agent:**
1. Write 3 behavioral evals in `skills/momentum/agents/evals/` (Tasks 1–3):
   - One `.md` file per eval, named descriptively
   - Format each eval as: "Given [describe the input and context], the agent should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement (Tasks 4–11):**
2. Work through Tasks 4–11 in order: audit → rewrite env section → rewrite input → rewrite load-contracts step → rewrite execution strategy step → update frontmatter → verify taxonomy → preserve unchanged sections

**Then verify (Task 12):**
3. Run evals: for each eval file, spawn a subagent with the eval's scenario as its task and pass the rewritten agent body as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap, revise the agent body, re-run (max 3 cycles; surface to developer if still failing)

**NFR compliance — mandatory:**
- `model:` and `effort:` frontmatter fields must be present (model routing)
- Agent body should stay under 500 lines; if the rewrite pushes past this, move reference content to `skills/momentum/agents/references/` with load instructions
- Description field ≤ 250 characters (agent descriptions use 250 not 150 per `agent-skill-development-guide.md`)
- `name: e2e-validator` in frontmatter — no rename

**Additional DoD items for this story:**
- [ ] 3 behavioral evals written in `skills/momentum/agents/evals/` (Tasks 1–3, done BEFORE implementation)
- [ ] EDD cycle ran — all 3 eval behaviors confirmed (Task 12, or failures documented with explanation)
- [ ] `grep -i "finch\|postgresql\|fastapi" skills/momentum/agents/e2e-validator.md` returns empty
- [ ] Description ≤ 250 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] Gherkin (`.feature`) path traced through new dispatch table — no behavioral regression
- [ ] DEC-020 taxonomy alignment verified and noted in Dev Agent Record (Task 10)
- [ ] Gherkin specs exist for this sprint in `.momentum/sprints/{sprint-slug}/specs/` but are off-limits to the dev agent during implementation — implement against plain English ACs above only, never against `.feature` files (Decision 30 black-box separation)

### Project Structure Notes

**File being rewritten:** `skills/momentum/agents/e2e-validator.md` — this is the only file changed by this story. No new agent files are created.

**Evals directory:** `skills/momentum/agents/evals/` — create if absent. Three eval files go here. This directory is not shipped as part of the plugin; it is local practice tooling.

**verification-harness.json schema source:** `.momentum/stories/momentum-harnessjson-schema-and-plugin-shipped-defaults.md` — read its Task and Dev Notes sections before implementing verification-harness.json field access in the agent body. The field names used in the agent body must exactly match the schema defined there.

**Agent definition conventions:** `skills/momentum/references/agent-skill-development-guide.md` — authoritative source for frontmatter schema, system prompt structure, and the mandatory Large File Handling section. The existing agent body already includes this section; preserve it unchanged.

### References

- DEC-029: `_bmad-output/planning-artifacts/decisions/dec-029-method-routed-acceptance-validation-pipeline-2026-05-17.md` — primary source; decisions D1 and D3 are directly implemented by this story
- DEC-020: `_bmad-output/planning-artifacts/decisions/dec-020-universal-agent-role-taxonomy-2026-05-16.md` — nine-role taxonomy; e2e-validator is one of the nine; rewrite must stay consistent
- Current agent body: `skills/momentum/agents/e2e-validator.md` — audit before rewriting (Task 1)
- Harness schema story: `.momentum/stories/momentum-harnessjson-schema-and-plugin-shipped-defaults.md` — read before Task 5 (harness field access)
- Agent dev guide: `skills/momentum/references/agent-skill-development-guide.md` — conventions for agent definition files

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
