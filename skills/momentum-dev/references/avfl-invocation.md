# AVFL Invocation Guide for momentum-dev

Reference this file in Step 2 to determine the correct AVFL parameters for each story's primary artifact.

## When to Run AVFL vs. Skip

| Primary artifact type | Run AVFL? | Profile | Stage |
|---|---|---|---|
| skill-instruction (SKILL.md, workflow.md) | Yes | `checkpoint` | `final` |
| rule-hook (.claude/rules/, hooks config) | Yes | `checkpoint` | `final` |
| config-structure only (JSON, version files) | Yes | `gate` | `final` |
| script-code only (.sh, .py, .ts) | **No** — tests are the quality gate | — | — |
| mixed (skill + script) | Yes — validate the skill artifact only | `checkpoint` | `final` |

## Parameter Reference

### skill-instruction primary artifact

```
domain_expert: "skill author"
task_context: "Momentum skill — [skill name, e.g., momentum-create-story]"
output_to_validate: [full content of the primary SKILL.md file]
source_material: [the Acceptance Criteria section from the story file]
profile: checkpoint
stage: final
```

**Why `checkpoint` not `full`?**
The skill will be dogfooded on real stories (NFR16) — real use is the ultimate validation. `checkpoint` (2–3 lenses, one fix attempt) gives structural and coherence quality signal without the 8-agent cost of `full`. Use `full` only when a skill is a final production deliverable being published to a release.

**Why acceptance criteria as source_material?**
AVFL's Factual Accuracy lens checks whether the produced artifact delivers what it was supposed to deliver. The ACs define what "supposed to deliver" means.

### rule-hook primary artifact

```
domain_expert: "practice engineer"
task_context: "Momentum rule — [rule/hook name, e.g., model-routing.md]"
output_to_validate: [full content of the produced rule file or hook config section]
source_material: [the Acceptance Criteria section from the story file]
profile: checkpoint
stage: final
```

### config-structure primary artifact

```
domain_expert: "project engineer"
task_context: "Momentum config — [what was created, e.g., momentum-versions.json]"
output_to_validate: [full content of the produced config file(s)]
source_material: [the Acceptance Criteria section from the story file]
profile: gate
stage: final
```

**Why `gate` not `checkpoint`?**
Config files are structural — they either have the required fields or they don't. A gate (single pass, no fix loop) is the right check. If the gate fails, the config has a structural defect that needs manual attention.

## Identifying the Primary Artifact

From the story's File List section, identify the primary artifact as follows:

1. If the list contains any `SKILL.md` files → the primary artifact is the SKILL.md for the new/modified skill. If multiple SKILL.md files were modified, validate the one most central to the story's acceptance criteria.

2. If the list contains `.claude/rules/` files and no SKILL.md → the primary artifact is the rule file.

3. If the list contains only JSON configs and directories → the primary artifact is the most important config file (usually `momentum-versions.json` or the entry-point config).

4. If the list contains only script files → skip AVFL (tests are the gate).

## Presenting AVFL Findings

Always synthesize AVFL output before presenting to the user. Never dump raw JSON.

**Format:**
```
AVFL checkpoint — [CLEAN | CHECKPOINT_WARNING]
[If CHECKPOINT_WARNING:]
  ! [critical finding summary — one line]
  · [medium finding summary — one line]
  [etc.]
```

**Severity key:** `!` = critical or high, `·` = medium or low
