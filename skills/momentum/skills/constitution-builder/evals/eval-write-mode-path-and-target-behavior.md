# Eval: write_mode path elicitation and target-path behavior

## Scenario A — standalone_constitution targets canonical path without asking

Given: The constitution-builder skill is invoked with `write_mode=standalone_constitution`
and no target path supplied.

Expected: The skill writes to `.claude/guidelines/constitution.md` (the canonical path)
without asking the developer for a path. Phase 1 does not prompt "where should this
constitution be written?"

Pass criteria:
- No path-prompt is issued to the developer
- The skill proceeds directly to content generation
- The completion message confirms the file was written at `.claude/guidelines/constitution.md`

Fail criteria:
- Skill asks for a target path despite being in `standalone_constitution` mode
- Skill writes to any path other than `.claude/guidelines/constitution.md`

---

## Scenario B — in_place_skill without path triggers path elicitation

Given: The constitution-builder skill is invoked with `write_mode=in_place_skill` and
NO target path supplied.

Expected: The skill asks the developer "where should this constitution be written?"
(or equivalent phrasing requesting the target SKILL.md path) before generating any content.
The skill does not proceed past Phase 1 until a path is provided.

Pass criteria:
- Skill pauses and asks the developer for the target path
- No constitution content is generated before the path is supplied
- Once a path is provided, the skill proceeds with content generation

Fail criteria:
- Skill generates content without first asking for the path
- Skill invents or guesses a path without eliciting from the developer

---

## Scenario C — in_place_skill with supplied path skips path prompt

Given: The constitution-builder skill is invoked with `write_mode=in_place_skill` AND
an explicit target path supplied (e.g., `target_path=skills/momentum/skills/myskill/SKILL.md`).

Expected: The skill does NOT ask "where should this constitution be written?" — it already
has the path. The skill proceeds directly to domain discovery and content generation.

Pass criteria:
- No path-prompt is issued to the developer
- The skill proceeds to content generation with the supplied path as the write target
- The completion message confirms the supplied path was used

Fail criteria:
- Skill re-asks for the path despite it being supplied
- Skill uses a different path than the one supplied

---

## Scenario D — composed_agent_file without path triggers path elicitation

Given: The constitution-builder skill is invoked with `write_mode=composed_agent_file` and
NO target path supplied.

Expected: Same elicitation behavior as Scenario B — the skill asks for a path before
generating content.

Pass criteria:
- Skill pauses and asks the developer for the target file path
- No constitution content is generated before the path is supplied

Fail criteria:
- Skill generates content without first asking for the path
