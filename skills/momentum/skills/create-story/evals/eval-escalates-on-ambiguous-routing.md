# Eval: Escalates to developer when routing is ambiguous

## Scenario A: Two conflicting non-subsumable methods

Given a Momentum story file at a known path, and the skill `momentum:create-story` has completed
Step 3 (change-type classification) and produced `{{classification_list}}` containing:
- Task 1 → `skill-instruction`
- Task 2 → `script-code`
- Task 3 → `rule-hook`

and `skills/momentum/references/rules/verification-standard.md` exists on disk with the routing table mapping:
- `skill-instruction` → `EDD eval`
- `script-code` → `execution test`
- `rule-hook` → `behavioral trigger test`

The skill should:
1. Load `verification-standard.md` and read the routing table
2. Map each classified change type to its method:
   - `skill-instruction` → `EDD eval`
   - `script-code` → `execution test`
   - `rule-hook` → `behavioral trigger test`
3. Determine that multiple distinct methods exist (none are subsumable)
4. Present the method candidates to the developer, listing each change type and its mapped method
5. Explain why the routing is ambiguous
6. Ask the developer to choose the method governing the story's primary deliverable
7. After the developer selects (e.g., "EDD eval"), set `verification_method = "EDD eval"`
8. Write `verification_method: EDD eval` to the story file's YAML frontmatter
9. Output "**Verification method selected:** `EDD eval`"
10. Continue to Step 5

The skill should NOT silently pick a method. The escalation message must list the candidates clearly.
After developer selection, no further prompting occurs — the frontmatter is updated and execution continues.

---

## Scenario B: All tasks unclassified

Given `{{classification_list}}` where every task is tagged `unclassified`
(e.g., "Task 1 → unclassified, Task 2 → unclassified"),

The skill should:
1. Detect that no classified change types are available
2. Escalate to the developer: ask what verification method should govern the story
3. After the developer selects, write `verification_method: <selected>` to frontmatter
4. Continue to Step 5

The skill should NOT default to any method silently when all tasks are unclassified.
The developer's explicit selection is required.

---

## Scenario C: Two change types that include only specification as the non-agreeing type

Given `{{classification_list}}` containing:
- Task 1 → `script-code`
- Task 2 → `specification`

The skill should:
1. Map `script-code` → `execution test`, `specification` → `document review`
2. Filter out `specification` (subsumed)
3. Determine the remaining entry agrees on `execution test`
4. Set `verification_method = "execution test"` without escalation
5. Write to frontmatter and continue

This is NOT an ambiguous case — the skill should NOT escalate. The `specification` subsumption
rule resolves it silently.
