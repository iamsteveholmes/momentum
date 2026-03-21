# Momentum Change Type Detection and Injection Templates

## Detection Heuristics

Read each task in the story's Tasks/Subtasks section. Apply the signals below to classify each task. A task may match multiple types — use the most specific match.

| Signal in task description or AC | Change Type |
|---|---|
| `SKILL.md`, `workflow.md`, `references/`, `agents/`, skill instructions, agent definition | `skill-instruction` |
| `.sh`, `.py`, `.ts`, `.js`, `scripts/`, `bin/`, executable, Python, bash, TypeScript | `script-code` |
| `.claude/rules/`, `settings.json`, `hooks`, hook configuration, frontmatter config | `rule-hook` |
| JSON config, directory structure, `momentum-versions.json`, `installed.json`, `mcp-config.json`, `hooks-config.json`, `version.md` | `config-structure` |

When a task mentions creating a new skill package (e.g., "Create `skills/momentum-foo/`"), classify all of the following within that task:
- The SKILL.md and workflow.md files → `skill-instruction`
- Any scripts/ subdir → `script-code`
- Any references/ or assets/ content → `skill-instruction`

---

## Injection Templates

Compose the `## Momentum Implementation Guide` section by including ONLY the templates for change types present in this story. If a type is not present, omit its section entirely.

The section header and change type summary ALWAYS appear. Per-type sections follow.

---

### Header Template (always include)

```markdown
## Momentum Implementation Guide

**Change Types in This Story:**
{{CHANGE_TYPE_LIST}}
  *(e.g., "- Tasks 1, 3 → skill-instruction (EDD)", "- Task 2 → config-structure (direct)")*

---
```

---

### skill-instruction Template

Include when any task involves SKILL.md, workflow.md, or other skill instruction files.

```markdown
### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/{{SKILL_DIR}}/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-creates-story-from-backlog.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify the SKILL.md, workflow.md, or reference files

**Then verify:**
3. Run evals: for each eval file, spawn a subagent with the eval's input context and the skill loaded; observe whether the behavior matches what the eval describes
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per NFR3)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3)
- Skill names prefixed `momentum-` (NFR12 — no naming collision with BMAD skills)

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/{{SKILL_DIR}}/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] AVFL checkpoint result documented (run automatically by momentum-dev after implementation)
```

---

### script-code Template

Include when any task involves bash, Python, TypeScript, or other executable scripts.

```markdown
### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). bmad-dev-story's Step 5 handles this correctly — the implementation guidance below is the standard approach:

1. **Red:** Write failing tests for the task's functionality first. Confirm they fail before implementing.
2. **Green:** Implement the minimum code to make tests pass. Run tests to confirm.
3. **Refactor:** Improve code structure while keeping tests green.

**Note:** Scripts in Momentum live under `skills/momentum-[name]/scripts/`. Follow the pattern in existing Momentum scripts for language choice and structure.

**DoD items for script-code tasks (standard — no additions needed):**
- Tests written and passing
- No regressions in existing test suite
- Code quality checks pass if configured
```

---

### rule-hook Template

Include when any task involves `.claude/rules/` files or `settings.json` hook configuration.

```markdown
### rule-hook Tasks: Functional Verification

Rules and hook configurations are declarative — they don't have unit tests. Use functional verification:

1. **Write the rule or hook entry** per the established format in existing `.claude/rules/` files or `.claude/settings.json`
2. **State the expected behavior** as a testable condition: "Given [event or trigger], this rule/hook should [observable result]"
3. **Verify functionally:**
   - For PreToolUse hooks: confirm the hook entry matches the required format and the blocked paths/tools are correct
   - For PostToolUse hooks: trigger a test edit and confirm the hook fires (if testable in current environment)
   - For Stop hooks: verify the conditional logic matches the FR specification
   - For rules files: confirm all required sections are present and the rule is internally consistent
4. **Document** the verification result and expected behavior in the Dev Agent Record

**Format requirements:**
- Rules files in `.claude/rules/` must follow the established markdown format
- Hook entries in `.claude/settings.json` must follow the Agent Skills hooks schema
- No duplicate hook entries (merge, don't append)

**Additional DoD items for rule-hook tasks:**
- [ ] Expected behavior stated as testable condition (in Dev Agent Record)
- [ ] Functional verification performed and result documented
- [ ] Format matches established patterns
```

---

### config-structure Template

Include when any task involves JSON config files, version files, or directory structure.

```markdown
### config-structure Tasks: Direct Implementation

Config and structure changes need no tests or evals. Implement directly and verify by inspection:

1. **Write the config or create the directory structure** per the story's acceptance criteria
2. **Verify by inspection:**
   - JSON files: must parse without error (mentally parse or use a tool)
   - Required fields: each required field must be present with the correct type
   - Paths: all referenced paths must exist after creation
   - Version consistency: any version fields must be consistent with related version references
3. **Document** what was created in the Dev Agent Record

**No tests required** for pure config/structure changes.
```

---

## Complete Example (mixed story)

For a story with Tasks:
- Task 1: Create `skills/momentum-create-story/SKILL.md` → skill-instruction
- Task 2: Create `skills/momentum-create-story/scripts/validate.py` → script-code
- Task 3: Create `skills/momentum-create-story/references/` → skill-instruction

Injected header would be:
```
**Change Types in This Story:**
- Tasks 1, 3 → skill-instruction (EDD)
- Task 2 → script-code (TDD)
```

Then the `skill-instruction` and `script-code` sections follow. The `rule-hook` and `config-structure` sections are omitted since those types are not present.
