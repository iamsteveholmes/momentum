# Contract Format Guide

Per-change-type authoring rules for frozen verification contracts written during Step 3.5 of sprint planning.

---

## File Extension by Change-Type

| change_type | Extension | Harness driver |
|---|---|---|
| `skill-instruction` | `.eval.yaml` | `skill-invoke` |
| `rule-hook` | `.trigger.md` | `behavioral-trigger` |
| `script-code` | `.smoke.sh` | `bash` |
| `script-cli` | `.smoke.sh` | `bash` |
| `specification` | `.review.md` | `document-review` |
| `research-spike` | `.review.md` | `document-review` |
| `app-ui` | `.feature` | `smoke` |
| `agent-definition` | `.eval.yaml` | `skill-invoke` |
| `backend` | `.smoke.sh` | `bash` |
| `config-structure` | `.review.md` | `document-review` |

### Multi-Change-Type Precedence

When a story declares multiple change-types, use the extension of the highest-weight type:

```
app-ui > script-code > script-cli > backend > agent-definition
> skill-instruction > rule-hook > config-structure
> specification > research-spike
```

Rationale: verification weight scales with change-type (DEC-029 D1). The highest-weight type's method subsumes lighter-weight methods.

---

## Universal Contract Rules (All Types)

1. **Black-box only** — the contract describes observable behavior. A person with no source code access must be able to execute every clause using only skill invocations, shell commands, or document inspection.

2. **Outsider Test** — before writing any clause, ask: "Could someone who has never seen the source code verify this clause?" If not, rewrite.

3. **No insider references** — never name internal delegation chains, which skill calls another, which tool is invoked, which file is read internally, or which function processes input.

4. **Harness reference** — every contract must declare `harness_profile: <name>` (for YAML/sh formats) or include a `## Harness Profile: <name>` section (for markdown formats). The name must match an entry in `momentum/verification-harness.json`.

5. **Observable scope** — state what must be true about outputs, files, terminal state, or observable system behavior — not what must happen inside the implementation.

---

## Mandatory Verification Header (Part A)

Every contract file must open with a Part-A header block before its body content. The header
fields are listed below in required order. All fields are mandatory unless marked optional.

**For YAML contracts** (`.eval.yaml`), the header is a YAML comment block followed by the
`story_slug` key at the top of the document:

```yaml
# === VERIFICATION HEADER (Part A) ===
story_slug: <story-slug>
verification_method: <driver-token>
harness_profile: <driver-token>
contract_path: .momentum/sprints/<sprint-slug>/specs/<story-slug>.<ext>
how_dev_self_checks: |
  <plain-language description of what to do and observe to confirm this story is done>
coverage_disposition: dedicated-run | covered-by-composition
covered_by_scenario: null | "<scenario name from coverage-plan.md>"
acceptance_criteria_ref: .momentum/stories/<story-slug>.md#acceptance-criteria
platforms: [host]
```

**For Markdown contracts** (`.trigger.md`, `.review.md`), the header is a YAML front-matter block:

```markdown
---
story_slug: <story-slug>
verification_method: <driver-token>
harness_profile: <driver-token>
contract_path: .momentum/sprints/<sprint-slug>/specs/<story-slug>.<ext>
how_dev_self_checks: |
  <plain-language description of what to do and observe to confirm this story is done>
coverage_disposition: dedicated-run | covered-by-composition
covered_by_scenario: null | "<scenario name from coverage-plan.md>"
acceptance_criteria_ref: .momentum/stories/<story-slug>.md#acceptance-criteria
platforms: [host]
---
```

**For Shell contracts** (`.smoke.sh`), the header is a structured comment block at the top:

```bash
#!/usr/bin/env bash
# === VERIFICATION HEADER (Part A) ===
# story_slug: <story-slug>
# verification_method: <driver-token>
# harness_profile: <driver-token>
# contract_path: .momentum/sprints/<sprint-slug>/specs/<story-slug>.smoke.sh
# how_dev_self_checks: Run this script; observe exit 0 and PASS output.
# coverage_disposition: dedicated-run | covered-by-composition
# covered_by_scenario: null | "<scenario name from coverage-plan.md>"
# acceptance_criteria_ref: .momentum/stories/<story-slug>.md#acceptance-criteria
# platforms: [host]
```

### Header Field Definitions

| Field | Required order | Description |
|---|---|---|
| `story_slug` | 1 | Kebab-case identifier matching the story file name |
| `verification_method` | 2 | Driver token from the closed enum: `skill-invoke`, `behavioral-trigger`, `bash`, `smoke`, `curl`, `document-review` |
| `harness_profile` | 3 | Same driver token as `verification_method` (or the profile name if project overrides exist in `momentum/verification-harness.json`) |
| `contract_path` | 4 | Relative path to this contract file from the project root |
| `how_dev_self_checks` | 5 | Plain-language instructions the developer follows to confirm the story is done — no insider knowledge, Outsider Test applies |
| `coverage_disposition` | 6 | `dedicated-run` if this story is verified standalone; `covered-by-composition` if an integration scenario discharges it |
| `covered_by_scenario` | 7 | `null` for dedicated-run; name of the integration scenario from `coverage-plan.md` for covered-by-composition |
| `acceptance_criteria_ref` | 8 | Path and anchor to the story's ACs in its markdown file |
| `platforms` | 9 | List of platforms where verification runs (typically `[host]`; may include `android`, `ios`, `web`) |

---

## skill-instruction → `.eval.yaml`

```yaml
# {story-slug}.eval.yaml
harness_profile: skill-invoke

scenarios:
  - name: "Descriptive scenario name"
    invocation: "momentum:skill-name with [input description]"
    given: "[observable precondition — what is set up or present before invocation]"
    when: "[what the user does — expressed as a skill invocation or command]"
    then:
      - "[observable output or state that must be true]"
      - "[additional observable outcome]"
    pass_criteria: "[how a black-box evaluator confirms the outcome]"
    fail_criteria: "[what observable absence or wrong output signals failure]"
```

**Do NOT include:**
- References to SKILL.md contents or frontmatter values
- Which sub-skill is delegated to
- Internal tool calls
- Which agent handles the invocation internally

**Include:**
- Concrete invocation strings
- Observable output content (not file paths to internal code)
- Pass/fail criteria expressible from the terminal

---

## rule-hook → `.trigger.md`

```markdown
# {story-slug} — Hook Trigger Contract

**Harness Profile:** behavioral-trigger

## Trigger Condition

[Observable: what the user does or what system state exists that should fire the hook]

## Observable Outcome

[What must be measurably different after the trigger fires]
[What the user sees, what files change, what command outputs change]

## Pass Criteria

[How a black-box tester confirms the hook fired — only using observable evidence]

## Fail Criteria

[What observable absence indicates the hook did not fire]
```

**Do NOT include:**
- The settings.json key path for the hook
- The hook body implementation
- Which internal script or command the hook runs
- The hook's `matcher` pattern verbatim (describe the triggering condition behaviorally)

---

## script-code / script-cli / backend → `.smoke.sh`

```bash
#!/usr/bin/env bash
# {story-slug} smoke contract
# Harness profile: bash
#
# Invocation:
#   [full command the black-box tester runs]
#
# Expected: [brief description of expected behavior]

set -euo pipefail

# Run
OUTPUT=$([command with sample inputs])

# Assert: [observable outcome]
echo "$OUTPUT" | grep -q "[expected output pattern]" || {
  echo "FAIL: expected [what] but got: $OUTPUT"
  exit 1
}

echo "PASS"
```

**Do NOT include:**
- Internal function names
- Internal data structures
- File paths that are not public interface paths
- Internal implementation choices

---

## specification / research-spike / config-structure → `.review.md`

```markdown
# {story-slug} — Document Review Contract

**Harness Profile:** document-review

## Document Under Review

[Path or description of the document to be reviewed — must be an observable path,
not an internal reference]

## Required Claims

- [ ] [Observable claim that must be verifiable by reading the document]
- [ ] [Another verifiable claim]

## Required Sections

- [ ] [Section heading or content that must be present]
- [ ] [Cross-reference that must resolve]

## Pass Criteria

[How a black-box reviewer confirms each required claim by reading the document]

## Fail Criteria

[What is missing or incorrect that would indicate the document fails review]
```

**Do NOT include:**
- File line numbers or internal schema keys
- Implementation details referenced in the document
- Assertions about file structure that require source code access

---

## app-ui → `.feature`

This is a Gherkin feature file. It follows all the rules in `skills/momentum/references/gherkin-template.md`.

The Step 3.5 contract for app-ui stories is the canonical `.feature` — Step 4 (Gherkin spec generation) must NOT overwrite it. Step 4 treats an existing `.feature` in `specs/` as already authored and skips that story.

---

## Anti-Insider Checklist

Before saving any contract, verify each clause passes:

- [ ] Does not name a specific skill called internally (e.g., "delegates to momentum:create-story")
- [ ] Does not name a specific tool used internally (e.g., "uses the Write tool to create")
- [ ] Does not name an internal file read (e.g., "reads stories/index.json")
- [ ] Does not name an internal function or variable
- [ ] Does not describe what the agent "decides" internally
- [ ] Could be verified by a tester who can only invoke skills and run commands
- [ ] `harness_profile` declares a valid entry from `momentum/verification-harness.json`
