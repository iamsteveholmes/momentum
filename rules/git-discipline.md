# Git Discipline

## Commit Philosophy: Early and Often

Commit after every completed task — not at the end of a session, after every logical unit of work. A task is: a fix applied, a file created, a section written, a validation completed, a refactor done. When in doubt, commit.

## Workflow Sessions

Multi-step agentic workflows (BMAD, skill workflows, UX design, PRD creation, etc.) are long-running sessions that produce many logical units of work. The commit rule does not get suspended during these sessions.

**Explicit commit triggers during workflows:**
- A workflow completes (final step reached) — always propose a commit
- A major artifact is created or substantially modified mid-workflow — propose a commit at that step's C (Continue)
- A workflow is paused or abandoned mid-session — propose a commit before stopping

Do not wait until the end of a conversation to surface the commit. If a workflow step saves meaningful changes to a file, surface the commit at that step's natural pause point — immediately after the user selects C to continue.

## Commit Message Format: Conventional Commits

Single-line format:
```
type(scope): concise description
```

Multi-line format (when a commit covers multiple changes):
```
type(scope): summary of primary change

- type(scope): detail 1
- type(scope): detail 2
- type(scope): detail 3
```

**Every bullet point in a multi-line commit MUST also use `type(scope):` format.** Generic bullets like `- extracted 47 FRs` are not allowed. Each bullet is its own conventional commit entry.

### Code vs. Docs — The Critical Distinction

**`feat`, `fix`, `refactor`, `perf`, `test`, `style` are for CODE changes only.**
Code means: anything that executes, enforces, or runs — skill SKILL.md files, agent definitions, hook scripts, rules files, shell scripts, source code, tests.

**`docs` is for specification and planning artifacts** — things that describe what to build, not what runs.
Docs means: PRD, architecture, epics, stories, UX design, research, README, product brief, validation reports.

**The rule:** If you're writing a spec for a feature, that's `docs(story)` or `docs(epics)` — not `feat`. `feat` is only when the feature is actually implemented in code/skills. A story saying "implement X" is `docs(story)`. The skill that implements X is `feat(skills)`.

**Markdown skill files ARE code.** Creating a new SKILL.md is `feat(skills)`. Fixing a broken step in a skill is `fix(skills)`. Restructuring a skill without behavior change is `refactor(skills)`.

### Types

| Type | When to Use | Code or Docs? |
|---|---|---|
| `feat` | New capability implemented — skill created, agent built, hook added, feature coded | Code only |
| `fix` | Bug or error corrected in something that runs | Code only |
| `refactor` | Restructuring with no behavior change | Code only |
| `perf` | Performance improvement | Code only |
| `test` | Adding or updating tests | Code only |
| `style` | Formatting, whitespace, linting — no logic change | Code only |
| `docs` | Specification, planning artifacts, research, README — things that describe, not run | Docs only |
| `chore` | Maintenance — config files, dependencies, CI, version bumps | Either |
| `ci` | CI/CD pipeline changes | Code only |
| `revert` | Reverting a previous commit | Either |

### Common Scopes for Momentum

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

For non-Momentum projects, use domain-appropriate scopes (e.g., `api`, `ui`, `db`, `auth`).

## Push Policy

Push after:
- Completing a story or equivalent body of work
- End of a session
- Before switching branches

Do NOT push after every commit — batch commits and push at logical milestones.

### Before Every Push: Show What Will Be Pushed

Before running `git push`, always run `git log @{u}..HEAD --oneline` and show the output to the user. This lets the user see exactly which commits will be pushed before the Claude Code confirmation dialog appears.

Format it clearly:

```
Ready to push 3 commits to origin/main:

  a1b2c3d docs(ux): add complete UX design specification
  e4f5g6h chore(hooks): add PostToolUse commit checkpoint hook
  i7j8k9l chore(rules): add workflow sessions section to git-discipline

Push?
```

Wait for the user to confirm before attempting `git push`.

## Permission Gates — CRITICAL

**ALWAYS ask the user before:**
- `git add` (show what will be staged)
- `git commit` (show the full commit message)
- `git push` (show what will be pushed and to where)

The user can say no or request changes. Wait for explicit approval.

**NEVER run these without explicit user request:**
- `git reset --hard`
- `git checkout -- .`
- `git clean -f`
- `git push --force`
- `git branch -D`
- `git rebase` (interactive or otherwise)
- `git stash drop`
- Any command that discards uncommitted work or rewrites published history

**Free to run without asking:**
- `git status`, `git log`, `git diff`, `git branch`, `git show`
- `git stash` (preserves work, doesn't destroy it)
- Any read-only git query

## Worktree Conventions

These conventions apply to `momentum-dev` story sessions, which always use git worktrees.

**Naming:** `.worktrees/story-{story_id}` (directory) on branch `story/{story_id}`

**Always-worktree rule:** Every `momentum-dev` story session creates a git worktree — even if it appears to be the only active session. This prevents mid-session file-change races when concurrent stories merge at different times.

**Crash recovery:** Before running `git worktree add`, check whether branch `story/{story_id}` already exists. If branch + worktree both exist, offer to resume or clean up. If branch exists but no worktree, delete the stale branch before proceeding.

**Status writes go to the main working tree:** Story status updates (`ready-for-dev` → `in-progress`, `in-progress` → `done`) are written to `sprint-status.yaml` in the main working tree, not inside the worktree. This ensures all concurrent sessions see status changes immediately.

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

## Session End Protocol

Before ending a session:
1. Check for uncommitted changes (`git status`)
2. If changes exist, propose a commit with conventional message
3. If commits exist that haven't been pushed, ask if the user wants to push
4. Never end a session with uncommitted work without explicitly flagging it
