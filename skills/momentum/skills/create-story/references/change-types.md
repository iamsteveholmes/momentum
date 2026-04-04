# Momentum Change Type Detection and Injection Templates

## Detection Heuristics

Read each task in the story's Tasks/Subtasks section. Apply the signals below to classify each task. A task typically maps to one change type — use the most specific signal. Exception: when a task bundles multiple file types (e.g., creating a full skill package with both instruction files and scripts), classify each file group separately per the rules below.

| Signal in task description or AC | Change Type |
|---|---|
| `SKILL.md`, `workflow.md`, `references/`, `agents/`, skill instructions, agent definition | `skill-instruction` |
| `.sh`, `.py`, `.ts`, `.js`, `scripts/`, `bin/`, executable, Python, bash, TypeScript | `script-code` |
| `.claude/rules/`, `settings.json`, `hooks`, hook configuration, frontmatter config | `rule-hook` |
| JSON config, directory structure, `momentum-versions.json`, `installed.json`, `mcp-config.json`, `hooks-config.json`, `version.md` | `config-structure` |
| `docs/`, `_bmad-output/`, PRD, architecture, epics, stories, UX design, research, README, `*.md` in planning/output directories | `specification` |

When a task mentions creating a new skill package (e.g., "Create `skills/momentum/skills/foo/`"), classify all of the following within that task:
- The SKILL.md and workflow.md files → `skill-instruction`
- Any scripts/ subdir → `script-code`
- Any references/ or assets/ content → `skill-instruction`

**Disambiguation — `.md` files:** Files inside `skills/*/` (SKILL.md, workflow.md, references/) are `skill-instruction`. Files inside `.claude/rules/` are `rule-hook`. Files in `docs/`, `_bmad-output/`, or the project root (README, architecture docs, PRDs) are `specification`.

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
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the SKILL.md and workflow.md contents as context (or invoke the skill via its Agent Skills name if installed). Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3)
- Skill names use `momentum:` namespace prefix (NFR12 — no naming collision with BMAD skills)

**Additional DoD items for skill-instruction tasks (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/{{SKILL_DIR}}/evals/`
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [ ] SKILL.md description ≤150 characters confirmed (count the actual characters)
- [ ] `model:` and `effort:` frontmatter present and correct
- [ ] SKILL.md body ≤500 lines / 5000 tokens confirmed (overflow in `references/` if needed)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the implemented SKILL.md against story ACs)
```

---

### script-code Template

Include when any task involves bash, Python, TypeScript, or other executable scripts.

```markdown
### script-code Tasks: TDD via bmad-dev-story

Script and code changes use standard TDD (red-green-refactor). bmad-dev-story handles TDD natively — the implementation guidance below matches its standard approach:

1. **Red:** Write failing tests for the task's functionality first. Confirm they fail before implementing.
2. **Green:** Implement the minimum code to make tests pass. Run tests to confirm.
3. **Refactor:** Improve code structure while keeping tests green.

**Note:** Scripts in Momentum live under `skills/momentum/skills/[name]/scripts/` or `skills/momentum/scripts/`. Follow the pattern in existing Momentum scripts for language choice and structure.

**DoD items for script-code tasks (bmad-dev-story standard DoD applies — listed here for reference):**
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
   - For Stop hooks: verify the conditional logic matches the functional requirements in the story's acceptance criteria
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
   - JSON files: must parse without error (validate with a JSON linter, `jq`, or IDE — do not rely on manual visual inspection)
   - Required fields: each required field must be present with the correct type
   - Paths: all referenced paths must exist after creation
   - Version consistency: any version fields must be consistent with related version references
3. **Document** what was created in the Dev Agent Record

**No tests required** for pure config/structure changes.

**DoD items for config-structure tasks:**
- [ ] All JSON files parse without error (validated with a tool)
- [ ] All required fields present with correct types
- [ ] All referenced paths exist after creation
- [ ] Changes documented in Dev Agent Record
```

---

### specification Template

Include when any task involves writing or updating documentation, planning artifacts, or specification files.

```markdown
### specification Tasks: Direct Authoring with Cross-Reference Verification

Specification and documentation changes are validated by AVFL against their upstream source (epic, PRD, or parent spec) — not by tests or evals. Write directly and verify by inspection:

1. **Write or update the spec** per the story's acceptance criteria
2. **Verify cross-references:** All references to other documents, files, sections, or identifiers must resolve correctly. Check links, path references, and section names.
3. **Verify format compliance:** If the project has an established template or convention for this document type (e.g., ADR format, story frontmatter schema), confirm the output follows it.
4. **Document** what was written or updated in the Dev Agent Record

**No tests or evals required** for specification changes. AVFL checkpoint (run by momentum:dev) validates the spec against acceptance criteria.

**Additional DoD items for specification tasks:**
- [ ] All cross-references to other documents, files, or sections resolve correctly
- [ ] Document follows project template/format conventions if one exists
- [ ] AVFL checkpoint result documented (momentum:dev runs this automatically)
```

---

## Complete Example (mixed story)

For a story with Tasks:
- Task 1: Create `skills/momentum/skills/create-story/SKILL.md` → skill-instruction
- Task 2: Create `skills/momentum/skills/create-story/scripts/validate.py` → script-code
- Task 3: Create `skills/momentum/skills/create-story/references/` → skill-instruction

Injected header would be:
```
**Change Types in This Story:**
- Tasks 1, 3 → skill-instruction (EDD)
- Task 2 → script-code (TDD)
```

Then the `skill-instruction` and `script-code` sections follow. The `rule-hook` and `config-structure` sections are omitted since those types are not present.
