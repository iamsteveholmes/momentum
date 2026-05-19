---
title: Verification Standard
applies_to: All Momentum stories
status: Active
cascade: global → project → path-scoped
source_decisions: DEC-029 D1, D3, D6, D7
---

# Verification Standard

This rule is authoritative and self-sufficient. Agents loading only this file have
complete enforcement guidance — no other document is required to apply it.

---

## 1. Method Routing Table

Every story's `change_type` maps to exactly one required verification method.
The validator reads this table and applies the mapped method.

| change_type | Required Verification Method |
|---|---|
| `skill-instruction` | EDD eval — adversarial eval scenarios authored by acceptance tester independent of implementation |
| `agent-definition` | Run-once behavioral check — invoke the agent with a representative input; observe that it routes, responds, and halts as specified |
| `rule-hook` | Behavioral trigger test — create the condition that should trigger the rule/hook; observe that expected behavior fires |
| `script-code` | Execution test — run the script with representative inputs; observe that output matches spec |
| `script-cli` | Execution test — run the CLI command; observe that output matches spec |
| `backend` | Execution test — exercise the endpoint or service; observe that response matches spec |
| `app-ui` | Smoke test (build + launch + drive) then human residual — automated smoke confirms launch; human confirms visible correctness |
| `research-spike` | Document review — confirm the research artifact satisfies all ACs by inspection and cross-reference |
| `specification` | Document review — confirm the spec artifact satisfies all ACs by inspection and cross-reference |
| `config-structure` | Direct implementation + validation — verify JSON/YAML parses, required fields present, no existing entries disturbed |

Stories with multiple `change_type` values apply each type's required method to the
task(s) of that type.

---

## 2. Method Override

A story may override its default method **only when**:

1. A written justification appears in the story's frozen contract (the story file's
   Dev Notes or Acceptance Criteria section), explaining why the default method is
   insufficient or inapplicable.
2. The justification is authored by the story creator or product owner — **not** the
   validator. The validator reads the justification; it cannot author it.

If no written justification exists in the frozen contract, the default method applies
and cannot be substituted.

---

## 3. Harness Profile Requirement

Every verified change **must** declare a harness-profile reference before verification
begins. The harness-profile reference names the entry in `momentum/harness.json` that
governs:

- Execution environment (runtime, OS, tool versions)
- Driver binding (which verification driver executes the method)
- Readiness probes (how to confirm the environment is ready before verification runs)

**Non-compliance condition:** A verification that proceeds without a declared
harness-profile is non-compliant. The validator must reject it and request a
harness-profile declaration before continuing.

The harness-profile reference is declared in the story file or in the frozen contract.
It is a name (string key) — `momentum/harness.json` defines the schema and defaults.

---

## 4. Adversarial Anti-Insider-Knowledge Guard

Any frozen contract whose verification steps require insider or application knowledge
is **rejected** at contract-authoring time and at validation time.

**Insider knowledge** is any fact not available to an ordinary user of the system:

- Implementation details not stated in the story spec
- Source code internals (variable names, function names, file paths internal to the
  implementation)
- Test fixture values or internal test setup
- Internal API names not part of the public interface
- Any fact about *how* the code is structured rather than *what it does*

**Ordinary-user knowledge** (permitted) is:

- What the skill/agent does (its stated purpose)
- What inputs it accepts (per its spec or UI)
- What observable outputs it produces
- What the story's Acceptance Criteria state
- What a user sees when they invoke the skill/agent normally

**Enforcement:** The validator applies this guard to every contract step. If a step
cannot be executed using only ordinary-user knowledge, the step is flagged and the
contract is returned for revision. Validation does not proceed on a flagged contract.

---

## 5. Cascade Order

This rule cascades in the following order:

```
global:  ~/.claude/rules/verification-standard.md
project: .claude/rules/verification-standard.md
path:    .claude/rules/<path-scoped>/verification-standard.md
```

**What can be overridden at lower scope:**

- Harness-profile reference (Section 3) — project and path scopes may specify a
  different default harness profile for their context.
- Method override justification (Section 2) — project scope may declare standing
  justifications for recurring override patterns.

**What cannot be overridden at any lower scope:**

- The routing table (Section 1) — global only. Project and path scopes may not
  replace, remove, or redefine routing table entries.
- The adversarial anti-insider-knowledge guard (Section 4) — global only. The guard
  applies uniformly; no project or path exception is valid.

Lower scopes that attempt to override non-overridable sections are ignored.
The global rule takes precedence.
