# Eval: Selects verification method without escalation when routing is unambiguous

## Scenario A: Single change type (inference fallback — no declared surface)

Given a Momentum story file at a known path with no `surface:` field declared in its
frontmatter, and the skill `momentum:create-story` has completed Step 3 (change-type
classification) and produced `{{classification_list}}` containing only `skill-instruction`
tasks (e.g., "Task 1 → skill-instruction, Task 2 → skill-instruction"), and
`skills/momentum/references/rules/verification-standard.md` exists on disk with the change_type
→ surface inference table mapping `skill-instruction` → `skill-invocation` → `skill-invoke`,

The skill should:
1. Check the story frontmatter for a declared `surface:` — find none
2. Load `verification-standard.md` and read the change_type → surface inference table
3. Map each classified change type to its inferred surface, then to its method — producing
   `skill-instruction → skill-invocation → skill-invoke`
4. Determine that all entries agree on the same method (`skill-invoke`)
5. Set `verification_method_advisory = "skill-invoke"` and `routed_by = "change_type_inference"`
   **without prompting the developer**
6. Write `verification_method_advisory: skill-invoke` into the story file's YAML frontmatter
7. Output "**Verification method advisory:** `skill-invoke` (routed by: change_type_inference)"
8. Continue to Step 5 (Implementation Guide injection) without pausing

The skill should NOT ask the developer to choose a method, and should NOT halt or warn.
The story file's frontmatter after this step includes `verification_method_advisory: skill-invoke`.

---

## Scenario A2: Declared surface resolves directly, bypassing change_type entirely

Given the same story file, but its frontmatter declares `surface: chat-ui`, and
`{{classification_list}}` contains only `backend` tasks (a change type that, if consulted,
would infer `application-ui`, not `chat-ui`),

The skill should:
1. Check the story frontmatter for a declared `surface:` — find `chat-ui`, a valid token in
   Section 1's surface enum
2. Look up `chat-ui` directly in Section 1's surface-to-method table — producing `smoke`
3. Set `verification_method_advisory = "smoke"` and `routed_by = "surface"` **without ever
   consulting `change_type`** — the declared surface resolves unambiguously on its own,
   regardless of how many distinct change types are present or what they would infer
4. Write `verification_method_advisory: smoke` to frontmatter and continue without escalation

The skill should NOT map `backend` to any method, should NOT filter or dedupe `method_candidates`
(that machinery is inference-path only), and should NOT ask the developer to choose — a declared
surface always wins and is never ambiguous.

---

## Scenario B: Mixed change types where specification is subsumed (inference fallback)

Given the same conditions as Scenario A (no declared surface) but `{{classification_list}}`
contains:
- Task 1 → `skill-instruction`
- Task 2 → `specification`

The skill should:
1. Confirm no `surface` is declared, so change_type inference applies
2. Map `skill-instruction` → `skill-invocation` → `skill-invoke`, `specification` → `artifact` →
   `document-review`
3. Filter out `specification` entries (subsumed by the dominant method for primary deliverable)
4. Determine the remaining entry agrees on `skill-invoke`
5. Set `verification_method_advisory = "skill-invoke"` without prompting
6. Write `verification_method_advisory: skill-invoke` to frontmatter
7. Continue without escalation

The skill should NOT escalate to the developer because `specification` (document-review)
is always subsumed by any other verification method.

---

## Scenario C: Missing verification-standard.md

Given the same story but `skills/momentum/references/rules/verification-standard.md` does NOT
exist on disk,

The skill should:
1. Attempt to load the file
2. Detect that it does not exist
3. Output a message indicating the verification method advisory cannot be computed because
   verification-standard.md is not found, and name the dependency story or rule that must
   be in place first
4. HALT — do not proceed to guide injection

The skill should NOT write any `verification_method_advisory` to frontmatter and should NOT continue to Step 5.
