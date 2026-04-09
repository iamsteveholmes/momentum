# Eval: Gherkin ATDD Workflow — Active and Enforced

## Purpose

Verify that the full ATDD workflow is active: spec generation quality is enforced,
the black-box boundary is explicit in dev agent instructions, the feedback loop
exists for spec-quality findings, and generated scenarios remain behavioral and general.

---

## Eval 1: Outsider Test Self-Check in Spec Generation

### Setup
Sprint-planning workflow, Step 4 (Generate Gherkin specs).

### Expected Behavior
After generating each `.feature` file, the workflow performs a self-check:
- Iterates every Given/When/Then clause
- Applies the Outsider Test (can someone verify this by invoking skills and reading outputs?)
- Flags and rewrites any clause that references internal mechanisms (skill names, tool names, file reads, agent internals)
- Does NOT save a spec that fails the Outsider Test

### Verification
The sprint-planning workflow Step 4 contains an explicit self-check action that:
1. Iterates every Given/When/Then clause after generating the spec
2. States the Outsider Test criterion
3. Requires flagging and rewriting failing clauses before saving

---

## Eval 2: Spec Quality Pre-Check Gate

### Setup
Sprint-planning workflow, Step 4, after all specs are generated.

### Expected Behavior
A validation sub-step runs before proceeding to team composition:
- Every scenario has at least one Given, one When, and one Then
- No scenario name contains AC numbers (e.g., "AC 1", "AC-2", "AC3") or phase numbers
- No Given/When/Then clause references internal agent names, tool names, or file paths that would fail the Outsider Test
- The feature file follows gherkin-template.md structure rules (indentation, no tags, no Scenario Outline, no comments)
- Failures surface the specific clause that failed with a reason, and the spec is regenerated before planning proceeds

### Verification
Sprint-planning Step 4 has a post-generation validation action that checks all four criteria and halts to regenerate on failure.

---

## Eval 3: Anti-Patterns Section in Gherkin Template

### Setup
`skills/momentum/references/gherkin-template.md`

### Expected Behavior
The file contains an "Anti-Patterns" section that:
- Lists the AC-by-AC translation pattern as an anti-pattern (one scenario per AC, AC numbers in names)
- Lists internal mechanism references (agent names, tool names, file reads) as an anti-pattern
- Lists implementation-coupled assertions (specific file paths, function names, class names, internal data structures) as an anti-pattern
- Lists passive voice in When clauses as an anti-pattern
- Each anti-pattern includes a concrete "Bad" example and a "Good" example pair

### Verification
Read `skills/momentum/references/gherkin-template.md`. Confirm the Anti-Patterns section exists with all four listed anti-patterns and at least one Bad/Good pair per anti-pattern.

---

## Eval 4: Dev Agent Black-Box Boundary — Critical Directive

### Setup
`skills/momentum/skills/dev/workflow.md`

### Expected Behavior
The dev workflow contains a `<critical>` directive that explicitly:
- Forbids dev agents from reading files under `sprints/{sprint-slug}/specs/`
- Forbids reading any `.feature` file
- States the reason (black-box separation — Gherkin specs are for verifiers only)

This is an explicit prohibition, not just a side-effect of protected-paths.json write protection.

### Verification
Read `skills/momentum/skills/dev/workflow.md`. Confirm a `<critical>` element is present that mentions both `specs/` (or `sprints/{sprint-slug}/specs/`) and `.feature` files as forbidden reads.

---

## Eval 5: Create-Story Workflow Reminder About Gherkin Boundary

### Setup
`skills/momentum/skills/create-story/workflow.md`, Step 4 (Momentum Implementation Guide injection).

### Expected Behavior
The create-story workflow's Step 4 includes a note reminding that:
- Gherkin specs exist for the sprint but are off-limits to the dev agent
- The dev agent must not access `sprints/{sprint-slug}/specs/` or any `.feature` file

### Verification
Read `skills/momentum/skills/create-story/workflow.md`. Confirm Step 4 contains a note or action about the Gherkin boundary for dev agents.

---

## Eval 6: E2E Validator Tags Spec-Quality Findings

### Setup
`skills/momentum/agents/e2e-validator.md`

### Expected Behavior
When the E2E Validator produces findings, it can tag them with `spec-quality` metadata when findings indicate:
- An untestable scenario (cannot be verified by external observation)
- A scenario that fails the Outsider Test (references internal mechanisms)

The tag appears in the structured output so downstream tools can filter on it.

### Verification
Read `skills/momentum/agents/e2e-validator.md`. Confirm the output format or finding classification section includes `spec-quality` as a tag or metadata field for untestable/outsider-test-failing scenarios, with documentation of the tag format.

---

## Eval 7: Sprint-Planning References Anti-Patterns Section

### Setup
Sprint-planning workflow, Step 4 (Generate Gherkin specs).

### Expected Behavior
The Gherkin spec generation step explicitly references the anti-patterns section in `gherkin-template.md`, directing the generating agent to consult it before writing scenarios.

### Verification
Sprint-planning Step 4 contains a reference to `gherkin-template.md`'s anti-patterns (or Anti-Patterns section) in its generation instructions.

---

## Eval 8: Protected Paths — Feature File Write Protection Confirmed

### Setup
`skills/momentum/references/protected-paths.json`

### Expected Behavior
The `*.feature` pattern exists in the protected paths with policy `acceptance-test-dir`, providing write protection for all feature files.

### Verification
Read `skills/momentum/references/protected-paths.json`. Confirm `*.feature` entry exists with `acceptance-test-dir` policy. (This is a verification-only eval — no change expected here unless the entry is missing.)

---

## Eval 9: Behavioral Generality — No Internal References in Scenarios

### Setup
Any generated `.feature` file in `sprints/*/specs/`.

### Expected Behavior
No scenario in any generated Gherkin spec:
- References specific file paths (e.g., `skills/momentum/skills/...`)
- References function or method names
- References internal agent names as mechanism (e.g., "When bmad-dev-story is invoked internally")
- References class names or data structure internals
- Uses passive voice in When clauses ("When quick-fix is invoked")

### Verification
Inspect generated feature files. All scenarios describe observable behavior: what the user does, what the system produces, what the developer can see. The sprint-planning Step 4 instructions enforce this standard during generation.
