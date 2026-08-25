# Eval: Goal Conditions Declared Before Contracts Freeze (Feature-Backed)

**ID:** eval-goal-conditions-declared-before-contracts
**Change-type:** skill-instruction
**Phase:** Story selection (Step 2)

## Scenario

Given `.momentum/features.json` exists and lists at least two candidate features, each with a
`slug`, `name`, and `acceptance_condition`, and a `sprint-planning` session has just persisted
the selected stories and `{{sprint_slug}}` via `momentum-tools sprint plan --operation add
--stories ... --slug ...` (the existing Step 2 persistence call)

When Step 2 continues past that persistence call and before Step 3 (Flesh out stories) begins

Then:

1. The workflow reads `.momentum/features.json` and presents each candidate feature's slug,
   name, and acceptance condition in plain language — not a raw JSON dump, and not a bare slug
   list.
2. The workflow asks the developer to select zero or more of the presented feature slugs as this
   sprint's goal conditions.
3. When the developer selects one or more slugs, the workflow also asks for (or derives, subject
   to developer confirmation) a plain-language `{{goal}}` statement consistent with the selected
   conditions.
4. The workflow persists both `{{goal}}` and `{{goal_conditions}}` via
   `momentum-tools sprint plan --goal "..." --goal-conditions "slug-a,slug-b"` — never a direct
   edit of `.momentum/sprints/index.json`.
5. Re-reading `.momentum/sprints/index.json` immediately after this call shows
   `planning.goal_conditions` as an array containing exactly the selected slugs, and
   `planning.goal` as the non-empty statement — both durable before Step 3 starts.
6. `.momentum/features.json` itself is never written or modified by this exchange.

## Pass Criteria

- Candidate features are shown in plain language (slug + name + acceptance condition), not raw
  JSON or bare slugs.
- The declared conditions and goal are persisted via `momentum-tools sprint plan`, not a direct
  file edit.
- The persisted record is readable back before Step 3 begins.
- `.momentum/features.json` is untouched.

## Fail Criteria

- The declaration step is skipped when a populated `features.json` exists.
- Conditions or goal are held only as workflow variables and never persisted via the CLI.
- The workflow edits `.momentum/sprints/index.json` or `.momentum/features.json` directly.
- Candidate features are dumped as raw JSON rather than translated to plain language.
