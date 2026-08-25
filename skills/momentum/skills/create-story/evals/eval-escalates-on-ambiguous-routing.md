# Eval: Escalates to developer when routing is ambiguous

## Scenario A: Two conflicting non-subsumable methods (inference fallback — no declared surface)

Given a Momentum story file at a known path with no `surface:` field declared in its
frontmatter, and the skill `momentum:create-story` has completed Step 3 (change-type
classification) and produced `{{classification_list}}` containing:
- Task 1 → `skill-instruction`
- Task 2 → `script-code`
- Task 3 → `rule-hook`

and `skills/momentum/references/rules/verification-standard.md` exists on disk with the
change_type → surface inference table mapping:
- `skill-instruction` → `skill-invocation` → `skill-invoke`
- `script-code` → `cli` → `bash`
- `rule-hook` → `hook-trigger` → `behavioral-trigger`

The skill should:
1. Check the story frontmatter for a declared `surface:` — find none, so change_type
   inference applies
2. Load `verification-standard.md` and read the change_type → surface inference table
3. Map each classified change type to its inferred surface and closed-enum method token:
   - `skill-instruction` → `skill-invocation` → `skill-invoke`
   - `script-code` → `cli` → `bash`
   - `rule-hook` → `hook-trigger` → `behavioral-trigger`
4. Determine that multiple distinct methods exist (none are subsumable)
5. Present the method candidates to the developer, listing each change type and its mapped method token
6. Explain why the routing is ambiguous
7. Ask the developer to choose the method governing the story's primary deliverable
8. After the developer selects (e.g., `skill-invoke`), set `verification_method_advisory = "skill-invoke"`
9. Write `verification_method_advisory: skill-invoke` to the story file's YAML frontmatter
10. Output "**Verification method advisory:** `skill-invoke` (routed by: change_type_inference)"
11. Continue to Step 5

The skill should NOT silently pick a method. The escalation message must list the candidates clearly
using the closed-enum tokens from the routing table.
After developer selection, no further prompting occurs — the frontmatter is updated and execution continues.

---

## Scenario A2: A declared surface bypasses this escalation entirely, even with conflicting change types

Given the same story and the same conflicting `{{classification_list}}` from Scenario A
(`skill-instruction` + `script-code` + `rule-hook` — three non-subsumable inferred methods),
but the story's frontmatter declares `surface: application-ui`,

The skill should:
1. Check the story frontmatter for a declared `surface:` — find `application-ui`, a valid
   token in Section 1's surface enum
2. Look up `application-ui` directly in Section 1's surface-to-method table — producing `smoke`
3. Set `verification_method_advisory = "smoke"` and `routed_by = "surface"` **without ever
   computing `method_candidates` from change_type** — the conflicting change types are never
   examined, because the declared surface resolves the routing before change_type is consulted
4. Write `verification_method_advisory: smoke` to frontmatter and continue

The skill should NOT ask the developer to choose between the change-type-derived candidates.
A declared surface is never ambiguous, regardless of how many conflicting change types are present.

---

## Scenario B: All tasks unclassified and no surface declared

Given `{{classification_list}}` where every task is tagged `unclassified`
(e.g., "Task 1 → unclassified, Task 2 → unclassified"), and no `surface:` is declared in
the story frontmatter,

The skill should:
1. Check the story frontmatter for a declared `surface:` — find none
2. Detect that no classified change types are available either
3. Escalate to the developer: ask what verification method should govern the story,
   presenting the valid closed-enum tokens as options
4. After the developer selects a token, write `verification_method_advisory: <selected-token>` to frontmatter
5. Continue to Step 5

The skill should NOT default to any method silently when all tasks are unclassified and no
surface is declared. The developer's explicit selection is required.

---

## Scenario C: Two change types that include only specification as the non-agreeing type (inference fallback)

Given `{{classification_list}}` containing:
- Task 1 → `script-code`
- Task 2 → `specification`

and no `surface:` declared,

The skill should:
1. Confirm no `surface` is declared, so change_type inference applies
2. Map `script-code` → `cli` → `bash`, `specification` → `artifact` → `document-review`
3. Filter out `specification` (subsumed)
4. Determine the remaining entry agrees on `bash`
5. Set `verification_method_advisory = "bash"` without escalation
6. Write `verification_method_advisory: bash` to frontmatter and continue

This is NOT an ambiguous case — the skill should NOT escalate. The `specification` subsumption
rule resolves it silently.
