# Eval: Green-field new file is committed

## Scenario

Given a conduct build for story `story-new-ref` whose sole deliverable is one brand-new file (for example, a new reference file at `skills/momentum/skills/example/references/new-thing.md`) that did not exist in the worktree before the dev agent ran, and no existing tracked file is modified, when the Conductor reaches the stage-1 commit step (`feat({slug}): implement …`), the skill should stage and commit that new file rather than silently dropping it.

## Expected behavior

1. Before committing, the Conductor enumerates the worktree's full change set with `git status --porcelain` (bound to `{{porcelain_paths}}`) — NOT `git add -u` and NOT `git diff --name-only --cached` — because both of those are blind to untracked files and would see zero changes for this story.
2. `{{porcelain_paths}}` includes the new file with an untracked (`??`) status line.
3. The WRITE-SCOPE COMMIT GUARD confirms the new file's path is in `{{writable_files}}` for the story (it is — it's the story's declared deliverable) and is not the story's own spec file, so it is classified in-scope, not discarded.
4. The Conductor stages the new file explicitly (`git add -- skills/momentum/skills/example/references/new-thing.md`), preferring the dev agent's returned `file_list` as the staged set.
5. The commit `feat(story-new-ref): implement …` contains the new file with its full expected content — confirmed by inspecting the commit's tree or `git show --stat` on the resulting commit.
6. After the story merges and its worktree is removed, the new file is present at its expected path on the sprint branch — not absent, not reverted, and not destroyed by the worktree cleanup.
7. Contrast (the defect this fixes): had the Conductor used `git add -u` as before, `git status --porcelain --cached` after that add would show nothing staged (the new file is untracked and `add -u` does not see it), the commit would contain no file changes, and the new file would be destroyed when `.worktrees/story-new-ref` is removed at cleanup — this is the failure mode the eval must NOT reproduce.
