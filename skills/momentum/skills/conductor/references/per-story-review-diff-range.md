# Per-Story Review Diff Range — Canonical Pattern

**This document is the single named source-of-record for the per-story review diff range.**  
Every per-story review call site (QA reviewer + code-review adapter, and Phase D re-check) in `workflow.md` cites this document and uses this pattern — no call site re-derives its own diff range expression.

---

## Scenario A — Pre-Merge Review (Conduct's primary case)

Conduct's per-story review runs at **stage 2**, which occurs BEFORE the story branch is rebased or merged (pipeline order: stage 1 dev → stage 2 QA + code-review → stage 3 fix-loop → stage 4 merge 2.2.M). The reviewers receive the diff while the sprint branch may have advanced as other stories merged concurrently.

### The Canonical Pre-Merge Pattern

Use the merge-base form to isolate exactly the story's own commits regardless of sprint branch advancement:

```bash
git -C .worktrees/story-{S.slug} diff \
  $(git -C .worktrees/story-{S.slug} merge-base sprint/{{sprint_slug}} story/{{S.slug}}) \
  ..story/{{S.slug}}
```

Equivalently, the three-dot shorthand:

```
sprint/{{sprint_slug}}...story/{{S.slug}}
```

No SHA needs to be captured ahead of time. The merge-base is computed at review time from the two branch tips.

### Why the Merge-Base Form is Correct Pre-Merge

- **Isolates the story's changes exactly:** the merge-base form diffs from the point where `story/{slug}` diverged from `sprint/{{sprint_slug}}` to the story tip. Even if the sprint branch has advanced (other stories merged in), the merge-base shifts accordingly, and only this story's commits appear in the diff.
- **Does NOT produce an empty diff pre-merge:** an empty three-dot diff occurs only when B is already an ancestor of A — i.e. AFTER the story is merged. Pre-merge, the story branch is NOT an ancestor of the sprint branch, so `sprint...story` diffs correctly and non-emptily.
- **Two-dot sprint..story over-scopes:** `sprint/{{sprint_slug}}..story/{{S.slug}}` (two-dot, current sprint tip to story tip) would include the story's commits MINUS any commits the sprint tip is already ahead of the story — producing spurious deletions for files changed by other stories that have since merged.

### Validation Against Conduct's Stage Ordering

The Conductor's per-story pipeline stage ordering is:

1. **Stage 1** — dev agent produces output
2. **Stage 2** — QA reviewer + code-review adapter run concurrently (pre-merge; this is where the diff is computed)
3. **Stage 3** — directed fix-loop (Phases B–D), using the same diff range for re-checks
4. **Stage 4** — merge (step 2.2.M): rebase onto sprint branch, then fast-forward merge

Because the diff is computed at stage 2, before the merge, no "capture at merge time" step is needed or possible — the merge has not happened yet.

---

## Scenario B — Post-Merge Review (The Different Case)

When a review runs AFTER the story has already been merged into an integration branch (e.g., `quick-fix` reviewing a merged commit, or sprint-dev repoint reviews that ran `pre_merge_main..main`), the situation is reversed:

- `sprint/{{sprint_slug}}...story/{{S.slug}}` produces an **empty diff** — the story branch is now an ancestor of the sprint branch, so there is no divergence from which to diff.
- **Correct post-merge pattern:** capture the integration target's pre-merge SHA before the merge occurs, then use a two-dot range after the merge:

```bash
# Captured before merge:
pre_merge_sha=$(git rev-parse {{merge_target}})

# Used after merge to recover the story's contribution:
git diff {{pre_merge_sha}}..{{merge_target}}
```

**This is a distinct scenario.** The capture-at-merge / two-dot pattern only applies here. Never apply it to conduct's stage-2 review, where the merge has not yet occurred.

---

## Summary: Which Pattern for Which Case

| Review timing | Sprint branch state | Pattern | Notes |
|---|---|---|---|
| Stage 2 (pre-merge) — **conduct's case** | May have advanced (other stories merged) | `git diff $(git merge-base sprint/{{sprint_slug}} story/{{S.slug}})..story/{{S.slug}}` | No capture step needed; computed at review time |
| Post-merge review | Story is now an ancestor of merge target | `git diff {{pre_merge_sha}}..{{merge_target}}` | `pre_merge_sha` captured before the merge |

---

## What Callers Must Do (Conduct Stage 2 + Phase D Re-Check)

Callers (QA reviewer dispatch, code-review adapter dispatch at step 2.1.3 stage 2, and Phase D RE-CHECK at step 2.S3) must:

1. Compute the diff at review time using the merge-base form:
   `git -C .worktrees/story-{S.slug} diff $(git -C .worktrees/story-{S.slug} merge-base sprint/{{sprint_slug}} story/{{S.slug}})..story/{{S.slug}}`
2. Pass the materialized diff (not the range expression) as the `story_diff` input to the reviewer.
3. Do **not** re-derive a diff range inline — use the merge-base expression from this document.
4. Do **not** wait for the merge to happen before computing the diff — stage 2 runs pre-merge.

---

## Anti-Patterns to Reject

| Pattern | Why it fails |
|---|---|
| `main...HEAD` | Over-scopes: includes all commits since the story branched from main, not just this story's changes |
| `main~1..main` | Under-scopes: only the last commit on main — misses multi-commit stories entirely |
| `sprint/{{sprint_slug}}..story/{{S.slug}}` (two-dot, current sprint tip) | Over-scopes pre-merge: includes story commits minus any sprint-tip-ahead commits; surfaces spurious deletions for files already merged by other stories |
| Capturing `pre_merge_sha` then using `pre_merge_sha..story/{slug}` pre-merge | Wrong model for stage 2 — the merge has not happened at review time; this pattern belongs only in post-merge reviews (Scenario B) |
| `sprint/{{sprint_slug}}...story/{{S.slug}}` post-merge | Empty diff — story is now an ancestor of sprint; use Scenario B's two-dot capture pattern instead |
