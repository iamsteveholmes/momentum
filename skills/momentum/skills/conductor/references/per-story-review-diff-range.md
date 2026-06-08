# Per-Story Review Diff Range — Canonical Pattern

**This document is the single named source-of-record for the per-story review diff range.**  
Every per-story review call site (QA reviewer + code-review adapter) in `workflow.md` cites this document and uses this pattern — no call site re-derives its own diff range expression.

---

## The Canonical Pattern

### Step 1 — Capture the pre-merge SHA at the merge point

Immediately **before** the story branch is merged into the sprint integration branch (step 2.2.M.2), capture the HEAD of the sprint branch:

```bash
pre_merge_sha=$(git -C .worktrees/story-{S.slug} rev-parse sprint/{{sprint_slug}})
```

This records the exact commit that was the tip of the sprint branch before the story's commits were added. It is the merge boundary for this story.

### Step 2 — Compute the diff as a two-dot range

The per-story review diff is:

```
{{pre_merge_sha}}..story/{{S.slug}}
```

Expressed as a git command against the story worktree:

```bash
git -C .worktrees/story-{S.slug} diff {{pre_merge_sha}}..story/{{S.slug}}
```

---

## Why Two-Dot, Not Three-Dot

Three-dot (`A...B`) computes the diff from the **merge base** of A and B to B. After a rebase (step 2.2.M.1), the story branch's merge base with the sprint branch IS the current sprint tip — so `pre_merge_sha...story/{slug}` produces an **empty diff** (merge base equals the left side). This is the known failure mode that generated three failed attempts in the prior sprint.

Two-dot (`A..B`) computes the diff from A to B directly. After rebase, `pre_merge_sha..story/{slug}` returns exactly the story's commits rebased onto the sprint branch — the correct, non-empty, story-scoped diff.

| Range form | After rebase | Result |
|---|---|---|
| `pre_merge_sha...story/{slug}` | merge-base == pre_merge_sha | **empty diff** (bug) |
| `pre_merge_sha..story/{slug}` | N/A | **story-scoped diff** (correct) |

---

## Validation Against Concrete Merge Mechanics

The Conductor's per-story integration sequence (step 2.2.M) is:

1. **Rebase** `story/{slug}` onto `sprint/{{sprint_slug}}` (`git rebase sprint/{{sprint_slug}} story/{slug}`)
2. **Fast-forward merge** into the sprint branch (`git merge --no-ff story/{slug}`)

The pre-merge SHA capture must happen **between steps 1 and 2** — after the rebase completes cleanly, before the merge. At that moment:

- `story/{slug}` is rebased and its commits are clean relative to the sprint branch
- `sprint/{{sprint_slug}}` HEAD is unchanged (the rebase rewrote the story branch, not the sprint branch)
- `pre_merge_sha` correctly identifies the merge boundary

Capturing before the rebase (against the pre-rebase sprint tip) also works and produces the same result — but capturing between rebase and merge is the authoritative placement aligned with step 2.2.M.

After the merge completes (step 2.2.M.6), the story branch and worktree are removed. The diff range must be materialized (passed to the QA reviewer and code-review adapter as content) **before** that cleanup — not reconstructed post-merge.

---

## What Callers Must Do

Callers (QA reviewer dispatch and code-review adapter dispatch in the per-story pipeline, step 2.1.3 stage 2) must:

1. Bind `{{pre_merge_sha}}` using the capture step above at the start of stage 2.
2. Materialize the diff: `git -C .worktrees/story-{S.slug} diff {{pre_merge_sha}}..story/{{S.slug}}`
3. Pass the materialized diff (not the range expression) as the `story_diff` input to both the QA reviewer and the code-review adapter.
4. Do **not** re-derive a diff range inline — use the two-dot expression from this document.

---

## Anti-Patterns to Reject

| Pattern | Why it fails |
|---|---|
| `main...HEAD` | Over-scopes: includes all commits since the story branched from main, not just this story's changes |
| `main~1..main` | Under-scopes: only the last commit on main — misses multi-commit stories entirely |
| `pre_merge_sha...story/{slug}` | Empty diff after rebase (merge-base == pre_merge_sha) |
| Capturing pre_merge_sha after the merge | Post-merge, the sprint tip has advanced — the captured SHA is the story's own merge commit, not the boundary |
