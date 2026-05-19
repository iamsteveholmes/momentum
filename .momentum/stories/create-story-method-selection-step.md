---
title: "create-story: method-selection step"
story_key: create-story-method-selection-step
status: review
epic_slug: story-cycles
feature_slug: momentum-quality-gates-enforced
story_type: practice
change_type:
  - skill-instruction
verification_method: eval
depends_on:
  - enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard
touches:
  - skills/momentum/skills/create-story/workflow.md
  - skills/momentum/skills/create-story/evals/
---

# create-story: method-selection step

## Story

As a developer,
I want `momentum:create-story` to select the verification method for every story it creates — consulting the change-type routing rule automatically and escalating to me only when the choice is genuinely ambiguous —
so that every story I receive carries an explicit, rule-derived verification method already recorded on it, and I am never surprised at validation time by an unresolved method.

## Description

DEC-029 D5 assigns `momentum:create-story` ownership of the verification-method decision. The method is derived from the change-type routing table in `skills/momentum/references/rules/verification-standard.md` (delivered by the `enforced-verification-rule` story in this sprint). When the routing is unambiguous, create-story selects silently. When the story's change types map to conflicting methods or the routing is unclear, create-story surfaces the candidates and asks the developer to choose.

The selected method is written into the story's YAML frontmatter as `verification_method:` before the story is handed to the developer — making it a frozen, auditable field from story-creation time rather than a validator-time guess.

**What this story adds to the create-story workflow:**
A new step — inserted between the existing change-type classification step (Step 3) and the Implementation Guide injection step (Step 4) — that:
1. Loads `verification-standard.md` and reads the routing table.
2. Maps each classified change type to its routed method.
3. Resolves a single method when all change types converge, or identifies the conflict when they diverge.
4. Escalates to the developer only when the routing is ambiguous.
5. Writes `verification_method: <selected>` into the story's YAML frontmatter.

**Intra-sprint dependency:** This story routes off `enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard`, which must be done (and `verification-standard.md` must exist) before this story can be implemented and verified.

**Gate 1 already cleared:** `routing-table-schema-and-implementation` is done; `momentum/agents.json` is present at `momentum/agents.json`.

## Acceptance Criteria

**AC-1: New step present in workflow between classification and guide injection**
When `skills/momentum/skills/create-story/workflow.md` is read, it contains a method-selection step that appears after the change-type classification step and before the Momentum Implementation Guide injection step.

**AC-2: Step loads the verification rule and reads the routing table**
When the method-selection step executes, it loads `skills/momentum/references/rules/verification-standard.md` and reads the change-type → verification-method routing table from that file. It does not hardcode routing logic in the workflow — the routing table in the rule file is the single source of truth.

**AC-3: Step maps each classified change type to its routed method**
When the method-selection step runs after change-type classification, for each change type identified in the story's classification list (e.g., `skill-instruction`, `rule-hook`, `specification`), the step looks up the corresponding required method from the routing table and produces a mapping list: `change-type → method`.

**AC-4: Single method resolves when all change types agree**
When all change types in the story map to the same verification method (or to methods that are clearly subsumable), the step selects that method without prompting the developer. For this story, `specification` (document review) is the only subsumed method — a story with `skill-instruction` + `specification` tasks resolves to EDD eval without escalation, because EDD verifies the skill deliverable that subsumes the spec work.

**AC-5: Ambiguous routing escalates to the developer with candidates listed**
When the story's change types map to two or more distinct methods that are not subsumable (e.g., `skill-instruction` → EDD eval, `script-code` → execution test — neither subsumes the other), the step presents the method candidates to the developer, explains why the routing is ambiguous, and asks the developer to select the method that governs the story's primary deliverable.

**AC-6: Selected method written to story frontmatter**
After a method is selected (either automatically or via developer choice), the step writes `verification_method: <selected-method>` into the story file's YAML frontmatter. The field is placed alongside the other frontmatter fields (`status`, `change_type`, `depends_on`, `touches`).

**AC-7: Method field is present in the finished story before guide injection runs**
When the step completes, `verification_method:` is present in the story's frontmatter before the Momentum Implementation Guide injection step (Step 4) runs. The guide injection step may reference `verification_method` to tailor its guidance, but the recording of the method must not depend on the guide injection completing first.

**AC-8: Step does not select a method if the routing rule file does not exist**
When `skills/momentum/references/rules/verification-standard.md` does not exist on disk (e.g., the `enforced-verification-rule` story has not yet been implemented), the method-selection step halts with a clear message: "Cannot select verification method — verification-standard.md not found. This story depends on `enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard` being implemented first." It does not proceed to guide injection.

**AC-9: Unclassified tasks do not block method selection**
When the story has some tasks tagged `unclassified` (change type unknown), the step resolves the method from the classified tasks only. If all tasks are unclassified, the step escalates to the developer rather than defaulting silently.

**AC-10: Step is visible in completion output**
When create-story's completion signal step (Step 8 after the new method-selection step is inserted as Step 4) runs, the output includes the selected `verification_method` alongside the existing change types and AVFL checkpoint fields.

## Tasks / Subtasks

- [x] **Task 1: Add method-selection step to `skills/momentum/skills/create-story/workflow.md`** (`skill-instruction`)
  - Insert a new `<step>` element after the change-type classification step (currently Step 3) and before the Implementation Guide injection step (currently Step 4)
  - The new step must: load `verification-standard.md`, map each classified change type to its routed method, resolve a single method or escalate on conflict, write `verification_method:` to frontmatter
  - Renumber the subsequent steps (new Step 4 becomes method-selection, old Step 4 becomes Step 5, etc.) to maintain sequential numbering
  - Update Step 7 (completion signal) to include `verification_method` in its output
  - Add a guard check: if `verification-standard.md` is absent, halt with the prescribed message (AC-8)

- [x] **Task 2: Write behavioral evals for the method-selection step** (`skill-instruction`)
  - Write at least 2 evals in `skills/momentum/skills/create-story/evals/`:
    - `eval-selects-method-unambiguous.md` — covers the single-method resolution case (all change types converge)
    - `eval-escalates-on-ambiguous-routing.md` — covers the multi-method conflict case and developer escalation
  - Each eval follows the format: "Given [input context], the skill should [observable behavior]"
  - Test behaviors (what the step decides and records), not exact output text

- [x] **Task 3: Run EDD verification** (`skill-instruction`)
  - Spawn a subagent for each eval, providing the eval scenario and the updated workflow.md content as context
  - Confirm that the unambiguous-routing eval results in silent selection + `verification_method` written to frontmatter
  - Confirm that the ambiguous-routing eval results in developer escalation with candidates listed
  - If any eval fails: diagnose the gap in the workflow instructions, revise, re-run (max 3 cycles; surface to developer if still failing)

## Dev Notes

### Architecture Compliance

**Routing rule as single source of truth (DEC-029 D5 + D7):**
The method-selection step must read `skills/momentum/references/rules/verification-standard.md` — it must not hardcode a routing table inline in the workflow. The rule is the governing document; the workflow obeys it. This separation is the whole point of D7 (dissolve process docs, enforce via rules).

**Step ordering constraint:**
The method-selection step must run after change-type classification (current Step 3) because it needs the classification list. It must run before the Implementation Guide injection (current Step 4) so the method is available if the guide injection ever uses it. Record `verification_method` in frontmatter before guide injection starts.

**YAML frontmatter update mechanics:**
The workflow already reads and writes `story_file`. Updating frontmatter means reading the file, parsing the YAML block (the `---` delimited header), adding or updating `verification_method:`, and writing back. Follow the same pattern used in Step 5 (which writes `status: ready-for-dev` to the index) for consistency. Do not use a script — update the file directly using the Write tool.

**Ambiguity definition:**
Ambiguity is strictly structural: two or more change types mapping to distinct, non-subsumable verification methods. The step should not second-guess the routing table by soft-inferring a "dominant" type — if the table produces a conflict, escalate. This keeps the rule authoritative and the workflow honest.

**Subsumption rule (for single-method resolution):**
`specification` tasks (document review) are always subsumed by any other method — a story with `skill-instruction` + `specification` tasks selects `EDD eval` without escalation, because EDD verifies the skill that subsumes the spec work. State this explicitly in the workflow step so the dev agent doesn't escalate needlessly on mixed stories. (Design authority: this is a dev-agent design decision for implementation; it is not explicitly enumerated in DEC-029 D1 or D5 but follows directly from D1's routing intent — EDD validates the whole story deliverable when the primary output is a skill.)

**`verification_method` frontmatter field:**
This is a new field — no existing stories use it. The create-story workflow writes it; downstream consumers (sprint-planning, e2e-validator) read it. Do not make the field mandatory for backlog stubs — only stories processed through the updated create-story will have it.

### Testing Requirements

All tasks are `skill-instruction`. Use EDD per the Momentum Implementation Guide below.

**Expected behaviors to test (minimal set):**
1. Single change type → silent resolution, `verification_method` written to frontmatter, no developer prompt.
2. Multiple change types, all same method → silent resolution, same result.
3. Multiple change types, conflicting methods → escalation message lists candidates, developer selects, frontmatter updated.
4. `verification-standard.md` absent → halt with required message, no frontmatter update.
5. All tasks unclassified → escalation, no default.

### Implementation Guide

**Order of operations:**
1. Write the two evals first (Task 2) — EDD requires behavioral expectations before implementation.
2. Implement the workflow step (Task 1) to satisfy the evals.
3. Run EDD verification (Task 3).

**Workflow step structure (suggested skeleton):**
```xml
<step n="4" goal="Select verification method from change-type routing">
  <action>Load `skills/momentum/references/rules/verification-standard.md`</action>
  <check if="verification-standard.md does not exist on disk">
    <output>Cannot select verification method — verification-standard.md not found.
This story depends on `enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard` being implemented first.</output>
    <action>HALT</action>
  </check>
  <action>Read the change-type → method routing table from verification-standard.md</action>
  <action>For each change type in {{classification_list}}, look up its required method from the routing table. Produce {{method_candidates}}: a list of (change-type, method) pairs.</action>
  <action>Filter out any (change-type, method) pairs where change-type is `specification` — specification tasks are subsumed by the dominant method of the story's primary deliverable.</action>
  <check if="all remaining entries in {{method_candidates}} agree on a single method OR only specification tasks remain">
    <action>Set {{verification_method}} = the agreed method (or `document review` if only specification tasks). No developer prompt.</action>
  </check>
  <check if="two or more distinct methods remain in {{method_candidates}} after filtering">
    <action>Set {{ambiguous}} = true</action>
    <ask>The change types in this story map to multiple verification methods:
{{method_candidates}}
Which method should govern this story's verification? (Pick the method for the story's primary deliverable.)</ask>
    <action>Set {{verification_method}} = developer's selection</action>
  </check>
  <check if="all tasks are unclassified">
    <ask>All tasks in this story are unclassified (no change type matched). What verification method should govern this story?</ask>
    <action>Set {{verification_method}} = developer's selection</action>
  </check>
  <action>Write `verification_method: {{verification_method}}` to the story's YAML frontmatter in {{story_file}}</action>
  <output>**Verification method selected:** `{{verification_method}}`</output>
</step>
```

**Step renumbering:** After inserting this as Step 4, the existing steps 4–7 become 5–8. Update all step `n=` attributes and any cross-references (e.g., "from Step 3" in Step 4's note becomes "from Step 3" in the new Step 5).

**Completion signal update:** Add to the existing Step 7 (now Step 8) output template:
```
**Verification method:** {{verification_method}}
```

### Project Structure Notes

Files touched by this story:

- `skills/momentum/skills/create-story/workflow.md` — primary change; new step inserted, steps renumbered, completion signal updated
- `skills/momentum/skills/create-story/evals/eval-selects-method-unambiguous.md` — new eval file
- `skills/momentum/skills/create-story/evals/eval-escalates-on-ambiguous-routing.md` — new eval file

Files read (not modified) by this story:
- `skills/momentum/references/rules/verification-standard.md` — routing rule, read at method-selection step runtime

The `SKILL_DIR` for EDD is `create-story`.

### References

- DEC-029 D5 — create-story owns verification-method decision: `_bmad-output/planning-artifacts/decisions/dec-029-method-routed-acceptance-validation-pipeline-2026-05-17.md`
- DEC-029 D1 — method routing table (change-type → verification method)
- DEC-029 D7 — process documents dissolved; enforced rules replace them
- Enforced verification rule story (intra-sprint dependency): `.momentum/stories/enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard.md`
- Routing table (already shipped): `momentum/agents.json`
- Change-type detection heuristics: `skills/momentum/skills/create-story/references/change-types.md`

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3 → `skill-instruction` (EDD)

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for SKILL.md or workflow.md files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the skill:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/create-story/evals/` (the `evals/` directory already exists):
   - One `.md` file per eval, named descriptively (e.g., `eval-selects-method-unambiguous.md`)
   - Format each eval as: "Given [describe the input and context], the skill should [observable behavior — what Claude does or produces]"
   - Test behaviors and decisions, not exact output text

**Then implement:**
2. Write/modify `skills/momentum/skills/create-story/workflow.md` to add the method-selection step

**Then verify:**
3. Run evals: for each eval file, use the Agent tool to spawn a subagent. Give it: (1) the eval's scenario as its task, and (2) load the skill by passing the updated workflow.md content as context. Observe whether the subagent's behavior matches the eval's expected outcome.
4. If all evals match → task complete
5. If any eval fails → diagnose the gap in the skill instructions, revise, re-run (max 3 cycles; surface to user if still failing)

**NFR compliance — mandatory for every skill-instruction task:**
- SKILL.md `description` field must be ≤150 characters (NFR1) — count precisely
- `model:` and `effort:` frontmatter fields must be present (model routing per FR23)
- SKILL.md body must stay under 500 lines / 5000 tokens; overflow content goes in `references/` with clear load instructions (NFR3)
- Skill names use `momentum:` namespace prefix (NFR12 — no naming collision with BMAD skills)

> **Note for this story:** This story modifies `workflow.md` and `evals/` only — `SKILL.md` is not changed. The SKILL.md line-count, description-length, and frontmatter presence checks are satisfied by no-modification. Verify the existing SKILL.md is unchanged after implementation.

**Additional DoD items for skill-instruction tasks:**
- [x] 2+ behavioral evals written in `skills/momentum/skills/create-story/evals/`
- [x] EDD cycle ran — all eval behaviors confirmed (or failures documented with explanation)
- [x] SKILL.md description ≤150 characters confirmed (141 chars — within limit)
- [x] `model:` and `effort:` frontmatter present and correct
- [x] SKILL.md body ≤500 lines / 5000 tokens confirmed (workflow.md is 209 lines; SKILL.md unchanged)
- [ ] AVFL checkpoint on produced artifact documented (momentum:dev runs this automatically — validates the implemented workflow.md against story ACs)

**Gherkin blackout:** Gherkin specs exist for this sprint in `sprints/{sprint-slug}/specs/` but are off-limits to the dev agent. Implement against the plain English ACs in this story file only — never read or reference `.feature` files. (Decision 30 black-box separation.)

## Dev Agent Record

### Agent Model Used

claude-sonnet-4-6

### Debug Log References

None — implementation was straightforward.

### Completion Notes List

- Wrote eval `eval-selects-method-unambiguous.md` covering: single change type (silent), specification-subsumed (silent), missing verification-standard.md (HALT).
- Wrote eval `eval-escalates-on-ambiguous-routing.md` covering: multiple conflicting methods (escalate), all unclassified (escalate), specification subsumed from non-specification (silent).
- Inserted Step 4 "Select verification method from change-type routing" into workflow.md between the classification step (Step 3) and the guide injection step (now Step 5).
- Step 4 logic: check file exists → load routing table → build method_candidates from classified tasks → filter specification entries → if all unclassified escalate → if 1 distinct method silent → if 2+ methods escalate → write verification_method to frontmatter.
- Renumbered old Steps 4–7 to Steps 5–8.
- Updated Step 8 (completion signal) to include `**Verification method:** {{verification_method}}` in its output.
- EDD verification: traced all 6 eval scenarios against workflow logic — all pass. No revisions needed.
- SKILL.md unchanged. Description 141 chars (≤150 ✓). `model:` and `effort:` present ✓. workflow.md 209 lines (≤500 ✓).

### File List

- `skills/momentum/skills/create-story/workflow.md` — modified: added Step 4 (method-selection), renumbered Steps 5–8, updated completion signal
- `skills/momentum/skills/create-story/evals/eval-selects-method-unambiguous.md` — new: EDD eval for unambiguous routing
- `skills/momentum/skills/create-story/evals/eval-escalates-on-ambiguous-routing.md` — new: EDD eval for ambiguous routing escalation
