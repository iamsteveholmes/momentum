# Git Discipline — Momentum Extensions

Extends the global git-discipline rule with Momentum-specific conventions for sprint branches, worktrees, and commit scopes.

## Common Scopes for Momentum

| Scope | What It Covers |
|---|---|
| `prd` | Product requirements document |
| `brief` | Product brief |
| `arch` | Architecture document |
| `epics` | Epics and stories |
| `ux` | UX design document |
| `rules` | Practice rules (`.claude/rules/`, `module/canonical/rules/`) |
| `agents` | Agent definitions |
| `skills` | SKILL.md files and skill workflows |
| `hooks` | Hook definitions and configuration |
| `provenance` | derives_from, staleness, reference infrastructure |
| `flywheel` | Evaluation flywheel, findings ledger, upstream fix |
| `research` | Research documents and findings |
| `backlog` | Process backlog updates |
| `readme` | README and top-level project docs |
| `license` | License file |
| `config` | Configuration files (settings, manifests, CLAUDE.md) |
| `validation` | Validation reports and validation tooling |
| `module` | Canonical module files |

## Push Policy — Sprint Work

Sprint work (sprint-plan, sprint-dev, momentum-dev) stays on a sprint branch and is NOT pushed until the sprint is complete and verified. All story commits, merges, and AVFL fixes stay local until the sprint reaches its done state. This keeps the full commit history rewritable/rollback-friendly throughout the sprint.

## Sprint Branch Convention

All sprint work — planning and dev — happens on a dedicated `sprint/{sprint_slug}` branch. This branch is created during sprint planning and merges to main only when the sprint is complete and verified.

**Branch lifecycle:**
1. Sprint planning creates `sprint/{sprint_slug}` from main
2. Planning artifacts (stories, specs, team composition) are committed to the sprint branch
3. Story worktrees branch off the sprint branch, merge back to the sprint branch
4. AVFL, team review, and verification all happen on the sprint branch
5. On sprint completion: merge sprint branch to main, delete the sprint branch, push (with approval)

**Why:** Local commits are easy to roll back; pushed commits are not. Keeping the entire sprint local until verified means the team can rewrite, squash, or discard freely. The sprint branch also cleanly separates concurrent sprint-plan and sprint-dev work, since each sprint gets its own branch.

**Concurrent sprints:** If sprint-dev is running on `sprint/sprint-2026-04-01` while sprint-planning creates `sprint/sprint-2026-04-08`, each has an isolated branch. No intermixed commits on main.

## Worktree Conventions

These conventions apply to `momentum-dev` story sessions, which always use git worktrees.

**Naming:** `.worktrees/story-{story_id}` (directory) on branch `story/{story_id}`

**Always-worktree rule:** Every `momentum-dev` story session creates a git worktree — even if it appears to be the only active session. This prevents mid-session file-change races when concurrent stories merge at different times.

**Crash recovery:** Before running `git worktree add`, check whether branch `story/{story_id}` already exists. If branch + worktree both exist, offer to resume or clean up. If branch exists but no worktree, delete the stale branch before proceeding.

**Status writes go to the main working tree:** Story status updates (`ready-for-dev` → `in-progress`, `in-progress` → `done`) are written to `sprint-status.yaml` in the main working tree, not inside the worktree. This ensures all concurrent sessions see status changes immediately.

**Merge target:** Story branches merge to the sprint branch (`sprint/{sprint_slug}`), not main. Main only receives the final sprint merge at completion.

**Merge gate:** Always propose the merge command and wait for explicit user confirmation before running `git merge`. Never auto-execute a merge.

**Merge order:** For stories with no dependency relationship, any merge order is valid. Merge dependency leaves first (a story whose dependents are waiting). Conflicts are expected when `touches` paths overlap — review diffs carefully.

**Cleanup:** After a confirmed merge:
```
git worktree remove .worktrees/story-{story_id}
git branch -d story/{story_id}
```
Run `git worktree prune` periodically to remove stale worktree metadata.

**Concurrency limitation:** Start concurrent sessions with a ~30s offset to avoid same-story selection race (two sessions both reading the same story as `ready` before either writes `in_progress`). A lock file `.worktrees/story-{story_id}.lock` provides additional protection.

**`.worktrees/` is gitignored:** Worktrees are local execution environments, not committed artifacts.

## Session End Protocol — Sprint Override

The global session end protocol applies, with one override:
- If work is part of an active sprint, note unpushed commits but do NOT propose a push — sprint work stays local until sprint completion.
