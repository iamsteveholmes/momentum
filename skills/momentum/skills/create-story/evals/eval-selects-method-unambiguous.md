# Eval: Selects verification method without escalation when routing is unambiguous

## Scenario A: Single change type

Given a Momentum story file at a known path, and the skill `momentum:create-story` has completed
Step 3 (change-type classification) and produced `{{classification_list}}` containing only
`skill-instruction` tasks (e.g., "Task 1 → skill-instruction, Task 2 → skill-instruction"),
and `skills/momentum/references/rules/verification-standard.md` exists on disk with the standard
routing table mapping `skill-instruction` → `EDD eval`,

The skill should:
1. Load `verification-standard.md` and read the routing table
2. Map each classified change type to its method — producing `skill-instruction → EDD eval`
3. Determine that all entries agree on the same method (`EDD eval`)
4. Set `verification_method = "EDD eval"` **without prompting the developer**
5. Write `verification_method: EDD eval` into the story file's YAML frontmatter
6. Output "**Verification method selected:** `EDD eval`"
7. Continue to Step 5 (Implementation Guide injection) without pausing

The skill should NOT ask the developer to choose a method, and should NOT halt or warn.
The story file's frontmatter after this step includes `verification_method: EDD eval`.

---

## Scenario B: Mixed change types where specification is subsumed

Given the same conditions but `{{classification_list}}` contains:
- Task 1 → `skill-instruction`
- Task 2 → `specification`

The skill should:
1. Map `skill-instruction` → `EDD eval`, `specification` → `document review`
2. Filter out `specification` entries (subsumed by the dominant method for primary deliverable)
3. Determine the remaining entry agrees on `EDD eval`
4. Set `verification_method = "EDD eval"` without prompting
5. Write `verification_method: EDD eval` to frontmatter
6. Continue without escalation

The skill should NOT escalate to the developer because `specification` (document review)
is always subsumed by any other verification method.

---

## Scenario C: Missing verification-standard.md

Given the same story but `skills/momentum/references/rules/verification-standard.md` does NOT
exist on disk,

The skill should:
1. Attempt to load the file
2. Detect that it does not exist
3. Output the exact message: "Cannot select verification method — verification-standard.md not found.
   This story depends on `enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard` being implemented first."
4. HALT — do not proceed to guide injection

The skill should NOT write any `verification_method` to frontmatter and should NOT continue to Step 5.
