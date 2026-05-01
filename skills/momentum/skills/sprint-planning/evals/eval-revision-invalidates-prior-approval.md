# Eval: Revision Invalidates Prior Approval

**Behavior:** When a story file is modified after approval (revise loop), the prior approval entry is superseded. The developer must re-approve, and the new approval records the current SHA.

## Input

A planning sprint has 1 story: `story-x`.

1. The developer opens `story-x` in the cmux viewer and selects **A (Approve)**.
2. `momentum-tools sprint story-approve --slug story-x --decision approved` runs and records the SHA of `story-x.md` at that moment.
3. The developer then selects **R (Revise)** — `momentum:create-story` is re-spawned and rewrites `story-x.md`, changing its contents (and therefore its SHA).
4. The revised story is opened in the cmux viewer.
5. The developer selects **A (Approve)** again on the revised version.

## Expected Behavior

1. After step 2: `planning.approvals` contains one entry for `story-x` with `decision = "approved"` and SHA₁.
2. After step 5: `planning-tools sprint story-approve --slug story-x --decision approved` runs again and **replaces** the prior entry with a new entry containing SHA₂ (the SHA of the revised file).
3. The final `planning.approvals` entry for `story-x` contains SHA₂, not SHA₁.
4. There is only one approval entry for `story-x` (the replace, not an additional append).
5. When `momentum-tools sprint activate` runs, it computes the current SHA of `story-x.md` and matches it against SHA₂ — activation succeeds.

## Anti-Patterns (Must Not Occur)

- Keeping the original SHA₁ approval after revisions (stale approval)
- Appending a second approval entry instead of replacing the existing one
- Skipping `story-approve` on the revised story because the developer already approved once
- Allowing `sprint activate` to succeed with SHA₁ when the file now has SHA₂

## Verification

The eval passes if:
- After the second approval, `planning.approvals` contains exactly one entry for `story-x`
- That entry has SHA₂ (the SHA of the revised story file)
- Sprint activation succeeds when the story file matches SHA₂
