# Momentum-Specific DoD Checklist

This checklist supplements the standard `bmad-dev-story` DoD. Items in the standard DoD (all tasks [x], File List complete, Dev Agent Record updated, Change Log updated, tests passing, no regressions) are NOT repeated here — `bmad-dev-story` already verifies them.

Check ONLY the items that apply to the story's change types. Skip sections for types not present.

**Note:** AVFL always runs on the full story changeset regardless of story type. The AVFL result documentation item appears in every section below because every story type goes through AVFL.

---

## code Stories

- [ ] **AVFL result noted:** AVFL checkpoint result (CLEAN or CHECKPOINT_WARNING with summary) is recorded in Dev Agent Record

*(Tests, regressions, and code quality are already covered by the standard bmad-dev-story DoD.)*

---

## specification Stories

- [ ] **Cross-references valid:** Any references to other documents, files, or sections resolve correctly
- [ ] **Format compliance:** Document follows the project's established template or format conventions if one exists
- [ ] **AVFL result noted:** AVFL checkpoint result (CLEAN or CHECKPOINT_WARNING with summary) is recorded in Dev Agent Record

---

## skill-instruction Stories

- [ ] **Evals exist:** `skills/[name]/evals/` directory contains 2 or more `.md` eval files
- [ ] **EDD cycle completed:** Dev Agent Record documents that evals were run and results (pass/partial/fail with notes)
- [ ] **Description length:** SKILL.md `description` field is ≤150 characters — count the actual characters in the frontmatter value
- [ ] **Model routing frontmatter:** `model:` and `effort:` fields present in SKILL.md frontmatter
- [ ] **Size compliance:** SKILL.md body is under 500 lines; if longer, overflow is in `references/` with load instructions
- [ ] **Skill name prefix:** Skill name starts with `momentum-` (prevents BMAD naming collision per NFR12)
- [ ] **AVFL result noted:** AVFL checkpoint result (CLEAN or CHECKPOINT_WARNING with summary) is recorded in Dev Agent Record

---

## rule-hook Stories

- [ ] **Behavior stated:** Dev Agent Record contains a "Given [trigger] → [result]" statement for each hook/rule written
- [ ] **Verification performed:** Dev Agent Record documents how the rule/hook was verified (format inspection, functional trigger, schema check)
- [ ] **No duplicate hooks:** If modifying `settings.json`, existing hooks were preserved and new entries were merged not appended
- [ ] **Format compliance:** Rule files follow the established `.claude/rules/` markdown format; hook entries follow the Agent Skills hooks schema

---

## config-structure Stories

- [ ] **JSON validity:** Any JSON files created or modified parse without error
- [ ] **Required fields present:** Each required field documented in ACs is present with correct type
- [ ] **Path existence:** Any referenced paths exist after the changes

---

## How to Report DoD Supplement Results

If all items pass:
```
Momentum DoD — all passed
```

If an item fails, halt immediately and surface the specific failure:
```
⚠ Momentum DoD — FAILED
  Item: [exact checklist item]
  Issue: [what specifically is wrong]
  Fix: [what needs to be done]
```

Do NOT mark the story complete until all applicable items pass.
