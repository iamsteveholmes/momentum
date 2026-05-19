---
title: "Enforced verification rule — change-type method-routing, harness-profile requirement, adversarial guard"
story_key: enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard
status: review
epic_slug: quality-enforcement
feature_slug: momentum-quality-gates-enforced
story_type: practice
change_type: [rule-hook, specification, config-structure]
depends_on: []
touches:
  - skills/momentum/references/rules/verification-standard.md
  - docs/process/acceptance-testing-standard.md
  - skills/momentum/references/momentum-versions.json
---

# Enforced verification rule — change-type method-routing, harness-profile requirement, adversarial guard

## Story

As a Momentum developer,
I want a single enforced verification rule that routes verification method by change-type, requires every verified change to declare a harness profile, and blocks insider-knowledge shortcuts,
so that the retired acceptance-testing-standard.md is replaced by an actively enforced constraint that the validator and sprint-dev cannot ignore.

## Description

DEC-029 Decision D7 dissolves the "process document" artifact class. `acceptance-testing-standard.md` is the evidence: it specified a five-method routing matrix that the `e2e-validator` agent entirely ignored, because the standard had no enforcement teeth. A document that governs agents without being loaded by those agents is dead documentation.

This story delivers the replacement: a **concise, enforced rule** at `skills/momentum/references/rules/verification-standard.md` that gets written by Impetus to `~/.claude/rules/` (global) and `.claude/rules/` (project) on first run. Four decisions compile into this rule:

- **D1** — Method routing: every story's change-type maps to a required verification method. The validator reads the table and applies the method; it cannot substitute a different method without a written justification in the frozen contract.
- **D3** — Harness profile location: D3 establishes that the per-project harness lives at `momentum/verification-harness.json`. Derived from D3's intent: every verified change must declare a harness-profile reference — naming the entry in `momentum/verification-harness.json` that governs execution environment and driver binding. A verification that runs without a declared harness profile is non-compliant.
- **D6** — Adversarial anti-insider-knowledge guard: any frozen contract whose verification requires insider/application knowledge is rejected. Contracts must be verifiable with no more knowledge than an ordinary user of the system has.
- **D7** — Cascade: the rule cascades global → project → path-scoped, per the established authority hierarchy. `acceptance-testing-standard.md` is retired: its rationale now lives in DEC-029; its enforceable content lives in this rule.

The retired `acceptance-testing-standard.md` is not deleted — it is marked retired with a forwarding pointer to DEC-029 and the new rule.

Gate 1 is already cleared: `routing-table-schema-and-implementation` is done and `momentum/agents.json` exists.

## Acceptance Criteria

**AC-1: Rule file exists at the correct plugin-bundled path**
The file `skills/momentum/references/rules/verification-standard.md` exists in the Momentum plugin source tree and is non-empty.

**AC-2: Rule defines the change-type → verification-method routing table**
When `verification-standard.md` is read, it contains a routing table mapping each of the following change types to its required verification method: `skill-instruction` → EDD eval; `agent-definition` → run-once behavioral check; `rule-hook` → behavioral trigger test; `script-code`, `script-cli`, and `backend` → execution test; `app-ui` → smoke (build + launch + drive) then human residual; `research-spike` → document review. The table is complete — no change type is listed without a required method.

**AC-3: Rule prohibits method substitution without written justification**
When `verification-standard.md` is read, it contains an explicit statement that a story may override its default method only when a written justification appears in the story's frozen contract, and that the validator reads the justification but cannot author it.

**AC-4: Rule mandates harness-profile declaration**
When `verification-standard.md` is read, it contains an explicit requirement that every verified change must declare a harness-profile reference — naming the entry in `momentum/verification-harness.json` that governs execution environment, driver binding, and readiness probes. A verification that proceeds without a declared harness profile is non-compliant.

**AC-5: Rule defines the adversarial anti-insider-knowledge guard**
When `verification-standard.md` is read, it contains a guard clause stating that any frozen contract whose verification steps require insider or application knowledge is rejected. The rule defines "insider knowledge" as any fact not available to an ordinary user of the system — implementation details, source code internals, test fixture values, internal API names. The guard applies at contract-authoring time and at validation time.

**AC-6: Rule states the cascade order**
When `verification-standard.md` is read, it explicitly states the cascade order: global (`~/.claude/rules/verification-standard.md`) → project (`.claude/rules/verification-standard.md`) → path-scoped (per `.claude/rules/` path-scoped overrides). Lower-scope overrides are permitted only for the harness-profile reference and method justification fields — not for the routing table or the adversarial guard. (Note: the non-overridability of the routing table and adversarial guard is a design decision made at story creation; DEC-029 D7 specifies the cascade mechanism but does not enumerate override scope — the dev agent has authority to implement this as specified.)

**AC-7: `acceptance-testing-standard.md` is retired with a forwarding pointer**
When `docs/process/acceptance-testing-standard.md` is read, its Status field reads `Retired` (previously `Active`), and it contains a forwarding note directing readers to DEC-029 for rationale and to `skills/momentum/references/rules/verification-standard.md` for the enforceable content. No substantive content is deleted from the file — the forwarding note is prepended.

**AC-8: Impetus rule-write path includes the new rule**
When `skills/momentum/references/momentum-versions.json` is read, it includes `verification-standard.md` in the list of rules that Impetus writes on first invocation. Specifically: an entry with `"source": "references/rules/verification-standard.md"` and `"target": "~/.claude/rules/verification-standard.md"` exists in the versions manifest, following the same schema as the existing `authority-hierarchy.md` and `anti-patterns.md` entries.

**AC-9: Rule is self-sufficient — no cross-file lookup required to apply it**
When `verification-standard.md` is read in isolation (without loading DEC-029, `acceptance-testing-standard.md`, or `momentum/verification-harness.json`), the routing table, harness-profile requirement, adversarial guard, and cascade order are all fully stated. Agents loading only this rule file have complete enforcement guidance.

**AC-10: Rule is concise — under 150 lines**
The body of `verification-standard.md` (excluding YAML frontmatter) is 150 lines or fewer. If the full routing rationale and historical context cannot fit, deep-rationale content is extracted to a `references/verification-rationale.md` companion and `verification-standard.md` references it with a load instruction.

## Tasks / Subtasks

- [x] **Task 1: Author `skills/momentum/references/rules/verification-standard.md`** (`rule-hook`)
  - Write the complete, self-sufficient rule file
  - Include: routing table (D1), method-override prohibition with written-justification escape, harness-profile mandate (D3), adversarial anti-insider-knowledge guard (D6), cascade order statement (D7)
  - Verify conciseness: body ≤150 lines; extract to companion reference if needed
  - Verify self-sufficiency: rule is complete without loading sibling documents

- [x] **Task 2: Retire `docs/process/acceptance-testing-standard.md`** (`specification`)
  - Prepend retirement notice and forwarding pointer to DEC-029 + new rule
  - Update Status field from `Active` to `Retired`
  - Do not delete existing content

- [x] **Task 3: Register rule in Impetus rule-write manifest** (`config-structure`)
  - File: `skills/momentum/references/momentum-versions.json` (confirmed location)
  - Add a new entry in the rules group following the existing pattern (see `authority-hierarchy.md` and `anti-patterns.md` entries for schema reference):
    - `"source": "references/rules/verification-standard.md"`
    - `"target": "~/.claude/rules/verification-standard.md"` (global target)
  - Verify the JSON parses without error after modification
  - Verify no duplicate entries exist for `verification-standard.md`
  - Verify the `defaults` block and other existing entries are unchanged

## Dev Notes

### Architecture Compliance

**Rules architecture (from architecture.md Decision 5 + plugin model):**
Rules live at `skills/momentum/references/rules/` in the plugin source. The plugin install cannot write to `~/.claude/rules/` or `.claude/rules/` directly — Impetus writes those targets using the Write tool on first `/momentum:impetus` invocation. The existing rule-write manifest is the canonical list of what Impetus writes. This story adds one entry to that list.

The authority hierarchy cascade (global → project → path-scoped) is already established by `skills/momentum/references/rules/authority-hierarchy.md`. The new rule must explicitly state that it follows this cascade — it doesn't invent a new mechanism.

**No new enforcement hook is required.** The rule enforces through the authority hierarchy: agents that load `~/.claude/rules/verification-standard.md` are bound by its content. The downstream stories (`e2e-validator-agent-body-rewrite`, `create-story-method-selection-step`) will wire their workflows to read and obey this rule. This story only writes the authoritative rule text.

**Harness profile reference vs. verification-harness.json schema:** This story's rule mandates that verified changes declare a harness profile name. The `momentum/verification-harness.json` schema and defaults are defined by the `momentum-harnessjson-schema-and-plugin-shipped-defaults` story (sibling in this sprint). The rule references harness profiles by name only — it does not define the schema. This story does not depend on the harness story; both can proceed in parallel.

**Cascade override scope:** Per D7, the rule cascades global → project → path-scoped. Only harness-profile references and method justifications are overridable at lower scope. The routing table and adversarial guard are global-only and cannot be overridden at project or path scope. State this explicitly in the rule.

### Testing Requirements

This story has three change types: `rule-hook` (Task 1, the rule file itself), `specification` (Task 2, the retirement notice), and `config-structure` (Task 3, the JSON manifest update). Each requires its own verification approach:

**Task 1 (rule-hook): Functional Verification**
State the expected behavior as a testable condition before writing:
- "Given an agent loads `~/.claude/rules/verification-standard.md`, when it evaluates a `skill-instruction` story, it must apply EDD eval as the verification method."
- "Given a frozen contract requires reading source code internals to verify, when the adversarial guard is applied, the contract is rejected."
Verify by inspection: confirm all required sections are present, the routing table is complete, and the rule is internally consistent. Confirm body ≤150 lines.

**Task 2 (specification): Direct Authoring with Cross-Reference Verification**
After writing, verify:
- `acceptance-testing-standard.md` Status field is `Retired`
- Forwarding pointer references both DEC-029 path and the new rule path — both paths must exist on disk after Task 1 completes

**Task 3 (config-structure): Direct Implementation + JSON Validation**
After modifying `skills/momentum/references/momentum-versions.json`:
- Parse the JSON to confirm it is valid (run `python3 -c "import json; json.load(open('skills/momentum/references/momentum-versions.json'))"`)
- Confirm the new entry exists with the correct source and target fields
- Confirm no existing entries were disturbed

### Implementation Guide

**Order of operations:**
1. Write `verification-standard.md` (Task 1) first — Tasks 2 and 3 reference its path.
2. Retire `acceptance-testing-standard.md` (Task 2) after Task 1 exists so the forwarding pointer resolves.
3. Register in manifest (Task 3) last.

**Rule file structure (suggested skeleton):**
```
---
title: Verification Standard
applies_to: All Momentum stories
status: Active
cascade: global → project → path-scoped
---

# Verification Standard

## 1. Method Routing Table
[routing table by change-type]

## 2. Method Override
[written justification requirement]

## 3. Harness Profile Requirement
[mandatory declaration]

## 4. Adversarial Anti-Insider-Knowledge Guard
[guard definition + what counts as insider knowledge]

## 5. Cascade Order
[global → project → path-scoped; what can/cannot be overridden]
```

**Rule-write manifest (confirmed location):** `skills/momentum/references/momentum-versions.json`. Existing rule entries follow this schema pattern (see `authority-hierarchy.md` entry as reference):
```json
{
  "group": "rules",
  "source": "references/rules/authority-hierarchy.md",
  "target": "~/.claude/rules/authority-hierarchy.md"
}
```
Add a new entry with `source: "references/rules/verification-standard.md"` and `target: "~/.claude/rules/verification-standard.md"` following this exact schema.

**What counts as insider knowledge (for the rule text):** implementation details not in the story spec, source code internals, test fixture values, internal API names, any fact about how the code is structured rather than what it does. Ordinary-user knowledge is: what the skill/agent does, what inputs it accepts, what observable outputs it produces, what the story's Acceptance Criteria state.

### Project Structure Notes

Files touched by this story:
- `skills/momentum/references/rules/verification-standard.md` — **new file** (Task 1)
- `docs/process/acceptance-testing-standard.md` — **modified** (Task 2; prepend retirement notice, update Status)
- `skills/momentum/references/momentum-versions.json` — **modified** (Task 3; add one rule entry to the rules group)
- `skills/momentum/references/verification-rationale.md` — **conditionally new** (Task 1 only, if rule body exceeds 150 lines; rationale extracted here and referenced from main rule with a load instruction)

Files **not** touched by this story:
- `momentum/verification-harness.json` — owned by `momentum-harnessjson-schema-and-plugin-shipped-defaults`
- `skills/momentum/agents/e2e-validator.md` — owned by `e2e-validator-agent-body-rewrite-de-gherkin-harness-driven`
- `skills/momentum/skills/create-story/workflow.md` — owned by `create-story-method-selection-step`
- `skills/momentum/skills/sprint-planning/workflow.md` — owned by `sprint-planning-frozen-per-story-contract-holistic-coverage`

No new directories. No new JSON config files. No new scripts.

### References

- `_bmad-output/planning-artifacts/decisions/dec-029-method-routed-acceptance-validation-pipeline-2026-05-17.md` — D1 (method routing), D3 (harness profile), D6 (adversarial guard), D7 (dissolve process-doc class, retire acceptance-testing-standard.md)
- `docs/process/acceptance-testing-standard.md` — retired predecessor; its five-method matrix and role-separation content are the foundation for the new routing table
- `skills/momentum/references/rules/authority-hierarchy.md` — establishes the cascade mechanism this rule follows
- `_bmad-output/planning-artifacts/architecture.md` — Rules Architecture section (Decision 5 / plugin model); rule-write manifest location and Impetus write sequence
- `.momentum/stories/index.json` — confirm `routing-table-schema-and-implementation` status is `done` (Gate 1 cleared) before starting

---

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → rule-hook (functional verification)
- Task 2 → specification (direct authoring with cross-reference verification)
- Task 3 → config-structure (direct implementation with JSON validation)

---

### rule-hook Tasks: Functional Verification

Rules and hook configurations are declarative — they don't have unit tests. Use functional verification:

1. **Write the rule** per the established format in existing `.claude/rules/` files. Use the skeleton structure from the Implementation Guide above.
2. **State the expected behavior** as testable conditions before writing:
   - "Given an agent loads `verification-standard.md`, when evaluating a `skill-instruction` story, it applies EDD eval — not Gherkin, not execution test."
   - "Given a frozen contract requires reading source code to verify, when the adversarial guard is applied, the contract is rejected as insider-knowledge."
   - "Given a story proceeds to validation without a declared harness-profile, the rule marks the verification non-compliant."
3. **Verify by inspection after writing:**
   - All five required sections present (routing table, override prohibition, harness mandate, adversarial guard, cascade order)
   - Routing table covers all change types listed in AC-2 — no gaps
   - Body ≤150 lines (count precisely)
   - Rule is internally consistent — no section contradicts another
4. **Document** the verification result and expected behaviors in the Dev Agent Record

**Format requirements:**
- Rules files in `.claude/rules/` must follow the established markdown format (see `authority-hierarchy.md` for style reference)
- No duplicate rule files — confirm no existing `verification-standard.md` at any level before creating

**Additional DoD items for rule-hook tasks:**
- [ ] Expected behaviors stated as testable conditions (documented in Dev Agent Record before writing)
- [ ] Functional verification performed and result documented (all AC checks passed by inspection)
- [ ] Format matches established rule file patterns
- [ ] Body ≤150 lines confirmed (count the actual lines)

---

### specification Tasks: Direct Authoring with Cross-Reference Verification

Specification and documentation changes are validated by AVFL against their upstream source — not by tests or evals. Write directly and verify by inspection:

1. **Write or update the spec** per the story's acceptance criteria (Task 2 only)
2. **Verify cross-references after writing:**
   - `acceptance-testing-standard.md`: forwarding pointer references DEC-029 path — confirm file exists; references `verification-standard.md` path — confirm Task 1 completed first
3. **Verify format compliance:**
   - Retirement notice follows the established Momentum documentation convention (Status field update + forwarding section)
4. **Document** what was written or updated in the Dev Agent Record

**Additional DoD items for specification tasks:**
- [ ] All cross-references resolve correctly (both paths in forwarding pointer)
- [ ] Document follows project template/format conventions
- [ ] AVFL checkpoint result documented (momentum-dev runs this automatically)

---

### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by inspection:

1. **Write the config entry** in `skills/momentum/references/momentum-versions.json` per Task 3's schema (see Implementation Guide for the exact entry format)
2. **Verify by inspection:**
   - JSON parses without error: `python3 -c "import json; json.load(open('skills/momentum/references/momentum-versions.json'))"`
   - New entry present with correct `group`, `source`, and `target` fields
   - All existing entries unchanged
3. **Document** what was added in the Dev Agent Record

**No tests required** for pure config changes.

**DoD items for config-structure tasks:**
- [ ] JSON file parses without error (validated with python3)
- [ ] Required fields present with correct values (`group: "rules"`, correct source and target paths)
- [ ] No existing entries disturbed
- [ ] Changes documented in Dev Agent Record

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

N/A — all three tasks completed without errors.

### Completion Notes List

- Task 1 (rule-hook): Authored `skills/momentum/references/rules/verification-standard.md`. Body is 119 lines (under 150 limit). Rule is self-sufficient — all five required sections present (routing table, method override, harness profile requirement, adversarial guard, cascade order). Routing table covers all 10 change types from AC-2. Behavioral conditions verified by inspection: skill-instruction maps to EDD eval, insider-knowledge contracts are rejected, harness-profile-less verification is non-compliant.
- Task 2 (specification): Retired `docs/process/acceptance-testing-standard.md`. Status field updated from Active to Retired. Forwarding notice prepended referencing DEC-029 path and new rule path. No substantive content deleted.
- Task 3 (config-structure): Added verification-standard.md entry to `skills/momentum/references/momentum-versions.json` in version 1.0.0 rules group. JSON validates without error. Existing entries unchanged. New entry: source=references/rules/verification-standard.md, target=~/.claude/rules/verification-standard.md.

### File List

- `skills/momentum/references/rules/verification-standard.md` — new file (Task 1)
- `docs/process/acceptance-testing-standard.md` — modified: Status=Retired, forwarding notice prepended (Task 2)
- `skills/momentum/references/momentum-versions.json` — modified: new rules entry added to 1.0.0 block (Task 3)
