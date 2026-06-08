# Eval: Escalates to developer when routing is ambiguous

## Scenario A: Two conflicting non-subsumable methods

Given a Momentum story file at a known path, and the skill `momentum:create-story` has completed
Step 3 (change-type classification) and produced `{{classification_list}}` containing:
- Task 1 → `skill-instruction`
- Task 2 → `script-code`
- Task 3 → `rule-hook`

and `skills/momentum/references/rules/verification-standard.md` exists on disk with the routing table mapping:
- `skill-instruction` → `skill-invoke`
- `script-code` → `bash`
- `rule-hook` → `behavioral-trigger`

The skill should:
1. Load `verification-standard.md` and read the routing table
2. Map each classified change type to its closed-enum method token:
   - `skill-instruction` → `skill-invoke`
   - `script-code` → `bash`
   - `rule-hook` → `behavioral-trigger`
3. Determine that multiple distinct methods exist (none are subsumable)
4. Present the method candidates to the developer, listing each change type and its mapped method token
5. Explain why the routing is ambiguous
6. Ask the developer to choose the method governing the story's primary deliverable
7. After the developer selects (e.g., `skill-invoke`), set `verification_method_advisory = "skill-invoke"`
8. Write `verification_method_advisory: skill-invoke` to the story file's YAML frontmatter
9. Output "**Verification method advisory:** `skill-invoke`"
10. Continue to Step 5

The skill should NOT silently pick a method. The escalation message must list the candidates clearly
using the closed-enum tokens from the routing table.
After developer selection, no further prompting occurs — the frontmatter is updated and execution continues.

---

## Scenario B: All tasks unclassified

Given `{{classification_list}}` where every task is tagged `unclassified`
(e.g., "Task 1 → unclassified, Task 2 → unclassified"),

The skill should:
1. Detect that no classified change types are available
2. Escalate to the developer: ask what verification method should govern the story,
   presenting the valid closed-enum tokens as options
3. After the developer selects a token, write `verification_method_advisory: <selected-token>` to frontmatter
4. Continue to Step 5

The skill should NOT default to any method silently when all tasks are unclassified.
The developer's explicit selection is required.

---

## Scenario C: Two change types that include only specification as the non-agreeing type

Given `{{classification_list}}` containing:
- Task 1 → `script-code`
- Task 2 → `specification`

The skill should:
1. Map `script-code` → `bash`, `specification` → `document-review`
2. Filter out `specification` (subsumed)
3. Determine the remaining entry agrees on `bash`
4. Set `verification_method_advisory = "bash"` without escalation
5. Write `verification_method_advisory: bash` to frontmatter and continue

This is NOT an ambiguous case — the skill should NOT escalate. The `specification` subsumption
rule resolves it silently.
