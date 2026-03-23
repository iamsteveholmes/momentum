# Acceptance Testing Standard

**Applies to:** All Momentum stories
**Status:** Active
**Source:** Epic 1 Retrospective — Action Items #2 and #3, Team Agreements 1–3

---

## 1. Purpose

This document defines the acceptance testing process for Momentum stories. It establishes:

- How each story type maps to a required verification method
- The role separation constraint that keeps verification structurally independent from implementation
- The enforcement mechanism that prevents accidental contamination of implementation with verification assumptions
- Team Agreements codified as binding process constraints

Acceptance testing is distinct from the developer's own verification. A developer running their own tests to confirm implementation is part of development. Acceptance testing is conducted by a separate role — the acceptance tester — after development is complete, using independently-authored criteria.

---

## 2. Story Type Classification

Every story is classified by its change type. The classification determines the required verification method.

| Story Type | Description | Required Verification Method | Examples |
|---|---|---|---|
| **skill-instruction** | Creates or modifies a SKILL.md / workflow.md file | EDD — adversarial eval authoring by an independent acceptance tester | Stories 1.3, 1.4, 2.1, 2.2, 2.3, 2.4 |
| **config-structure** | Creates or modifies JSON configs, YAML, directory structure, or version files | Execution test — run the config, verify observed behavior matches spec | Story 1.1 (JSON parsing + path verification) |
| **install/deploy** | Affects how the module is installed, published, or distributed | End-to-end test — run the actual install from outside the repo, verify the install succeeds and produces the expected result | Stories 1.2, 1.6 |
| **rule/hook** | Creates or modifies a `.claude/rules/` file or a settings.json hook entry | Behavioral trigger test — trigger the rule or hook condition and observe that the expected behavior fires | Stories 3.1–3.4 |
| **process-doc** | Creates or modifies process documentation, standards, or planning artifacts | Document review — confirm document satisfies all ACs by inspection and cross-reference | Story 1.7 |

### Verification Method Definitions

**EDD (Example-Driven Development) — adversarial eval authoring:**
The acceptance tester authors eval scenarios that attempt to demonstrate failure in the skill. Evals are written before the acceptance tester reviews the implementation. The skill passes acceptance when it handles adversarial inputs correctly.

**Execution test:**
The acceptance tester runs the config, command, or process described in the story and observes behavior. Verification is outcome-based, not structure-based. "The JSON parses" is not an execution test. "Running the command produces the expected output" is.

**End-to-end test:**
The acceptance tester performs the install or deploy sequence from outside the repository (a clean environment or fresh directory) and verifies that the observable result matches the story's acceptance criteria.

**Behavioral trigger test:**
The acceptance tester creates the condition that should trigger the rule or hook, then observes whether the expected behavior fires. Verification is trigger → response, not "the file exists".

**Document review:**
The acceptance tester reads the document and verifies each AC is satisfied by content present in the document. Cross-references to sources are checked.

---

## 3. Role Separation

### 3.1 The Constraint

The acceptance tester role is **structurally separate** from the developer role.

- The developer implements the story.
- The acceptance tester authors and executes verification for that story.
- These are different agents or persons operating in separate contexts.

**The developer does not:**
- Author acceptance tests or EDD evals for their own work
- Read acceptance test artifacts or EDD evals during implementation
- Execute acceptance tests on their own implementation

**The acceptance tester does not:**
- Modify the implementation
- Author the developer's unit tests or inline tests

### 3.2 Why This Matters

When a developer authors their own verification criteria, the evals unconsciously mirror implementation assumptions. An eval written after implementation cannot challenge those assumptions — it describes what the implementation does, not what it should do. The result is tests that pass trivially because they were written to pass.

This is not a theoretical risk. The Epic 1 retrospective identified developer-authored verification as a gap that allowed a broken install experience to ship: JSON parsing tests passed, path existence checks passed, but actual npx invocation produced 90 skills instead of 8.

### 3.3 Enforcement Mechanism

Enforcement is structural, not conventional.

**Write protection (existing):**
The PreToolUse hook blocks writes to `tests/acceptance/` and `**/*.feature`. The dev agent cannot create or modify acceptance tests during implementation. This boundary is enforced by the hook, not by developer discipline.

**Read protection (process layer):**
EDD evals live under `skills/[name]/evals/`. The dev agent must not load files from `evals/` or `tests/acceptance/` during implementation. This is enforced by convention at MVP (the story file explicitly lists what the dev agent reads in Dev Notes), with a path to PreToolUse read-blocking when hook infrastructure supports it (Epic 3).

**Session isolation:**
Acceptance testing occurs in a separate Claude Code session from implementation. The acceptance tester session does not load the dev agent's story file or implementation notes. The acceptance tester receives only: the story's Acceptance Criteria, the Acceptance Test Plan, and the produced artifacts.

**File organization:**
- Developer implementation: `skills/[name]/SKILL.md`, `skills/[name]/workflow.md`
- EDD evals (acceptance tester): `skills/[name]/evals/`
- Acceptance tests: `tests/acceptance/`
- Story + ACs: `_bmad-output/implementation-artifacts/[story].md`

The dev agent reads `skills/`, `docs/`, `module/`, story files. It does not read `tests/acceptance/` or `evals/`.

---

## 4. Team Agreements

The following constraints are codified from the Epic 1 Retrospective Team Agreements. They are binding process constraints, not guidelines.

### Agreement 1: E2E deployment testing is mandatory for install/deploy stories

Any story with an install path, deploy path, publish step, or externally-observable distribution change requires an end-to-end test conducted in a clean environment. "JSON parses" and "fields present" do not constitute acceptance for these stories.

**Scope:** Any story classified as `install/deploy` in the story type classification table.
**Test environment:** Outside the repository — a clean directory or environment that does not have the package pre-installed.
**Verification:** The acceptance tester runs the actual install command and verifies the observable result. The story is not done until this test passes.

### Agreement 2: Acceptance testing role separation is active immediately

Role separation is in effect for all stories from this story forward. It is not deferred to Epic 4 tooling.

The process layer (dev agent convention + story file structure) enforces role separation now. Epic 4 tooling (ATDD workflow, automated acceptance test gates) will strengthen enforcement — but the constraint is active today.

**Immediate effect:**
- Every story file includes an Acceptance Test Plan section (see Section 5)
- The acceptance tester is not the same agent/session that implemented the story
- Story 4.2 implements tooling on top of a process that already works

### Agreement 3: Every story file includes an Acceptance Test Plan section

Beginning with stories in Epic 2 and all subsequent stories, the story file contains an explicit Acceptance Test Plan section. The section is authored alongside the story (during story creation or during this audit), not after implementation.

The Acceptance Test Plan is owned by the acceptance tester role. If it is authored during story creation (before a dedicated tester is assigned), it is a draft that the acceptance tester reviews and may update before executing.

---

## 5. Acceptance Test Plan Section — Standard Template

### 5.1 Template

The following section template is added to every story file. It appears after the **Dev Notes** section and before the **Dev Agent Record** section.

```markdown
## Acceptance Test Plan

**Story type:** [skill-instruction | config-structure | install/deploy | rule/hook | process-doc]
**Verification method:** [EDD | execution test | end-to-end test | behavioral trigger test | document review]
**Test artifacts location:** [path — e.g., `skills/[name]/evals/` or `tests/acceptance/`]
**Acceptance tester:** [unassigned | name/role]

### Test Scenarios

[For skill-instruction: adversarial eval scenarios that attempt to demonstrate failure]
[For config-structure: execution steps and expected observations]
[For install/deploy: clean environment install procedure and expected observable result]
[For rule/hook: trigger condition and expected behavior to observe]
[For process-doc: AC-by-AC verification checklist]

### Acceptance Gate

This story passes acceptance when:
[Specific, measurable conditions — one per AC]
```

### 5.2 Section Placement

The Acceptance Test Plan section is placed:
- **After** the Dev Notes section
- **Before** the Dev Agent Record section

This placement ensures:
- The acceptance tester can read story context (Dev Notes) before the test plan
- The dev agent reads Dev Notes and Acceptance Test Plan during implementation (for awareness of what will be tested)
- The dev agent does NOT read the actual test artifacts in `evals/` or `tests/acceptance/` — only the plan

### 5.3 Authoring Responsibility

| When | Who authors |
|---|---|
| Story created via `momentum-create-story` | Story creator (draft) |
| Epic 2 audit (this story) | Developer authoring this story (draft) |
| Before acceptance testing begins | Acceptance tester reviews and may revise |
| After revision | Acceptance tester owns the plan |

---

## 6. Application to Existing Stories

### Stories Needing Acceptance Test Plan sections added retroactively

| Story | Status | Action Required |
|---|---|---|
| 1-6-fix-npx-skills-add-experience | ready-for-dev | Add ATP section before dev starts (depends on 1-7) |
| 2-1 through 2-4 | ready-for-dev | Added in Story 1.7, Task 3 (this story) |
| 1-8, 1-9 | ready-for-dev | Add ATP before dev starts |

Stories 1-1 through 1-5 are `done` — retroactive addition is optional and not required.

### Epic 2 classification

All four Epic 2 stories (2.1–2.4) create Impetus skill files. They classify as `skill-instruction`.

---

## 7. References

- `_bmad-output/implementation-artifacts/epic-1-retro-2026-03-22.md` — Source of Team Agreements and Action Items
- `_bmad-output/planning-artifacts/architecture.md` — Decision 2a (File Protection), Decision 5b (Acceptance Gate), Data Access Matrix
- `_bmad-output/planning-artifacts/epics.md` — Story 1.7 definition, Epic 1b context
