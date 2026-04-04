# Eval: Classifies change types from story tasks

## Scenario

Given a Momentum story file at a known path with the following Tasks section:

```
## Tasks / Subtasks

- [ ] Task 1: Create `skills/momentum-validate/SKILL.md` and `workflow.md`
- [ ] Task 2: Create `skills/momentum-validate/scripts/validate.sh`
- [ ] Task 3: Update `.claude/rules/momentum-quality.md`
- [ ] Task 4: Add entry to `momentum-versions.json`
```

The skill `momentum-create-story` has just completed Step 1 (bmad-create-story ran and produced the story file) and is now in Step 3.

## Expected behavior

The skill should:
1. Read the Tasks/Subtasks section of the story file
2. Classify each task using the detection heuristics from `./references/change-types.md`:
   - Task 1: `skill-instruction` (SKILL.md and workflow.md)
   - Task 2: `script-code` (`.sh` executable)
   - Task 3: `rule-hook` (`.claude/rules/` file)
   - Task 4: `config-structure` (`momentum-versions.json`)
3. Output a classification list showing each task with its change type
4. Store `{{change_types_summary}}` as something like "1 skill-instruction task, 1 script-code task, 1 rule-hook task, 1 config-structure task"

The skill should NOT ask the user for guidance on classification — it should apply the detection signals from change-types.md autonomously.
