---
name: warn-destructive-git
enabled: true
event: bash
pattern: git\s+(branch\s+-D|stash\s+drop)|git\s+rebase\b
action: warn
---

⚠️ **Destructive git operation — confirm before proceeding**

`branch -D`, `stash drop`, and `rebase` are legitimate in workflow contexts but require explicit user confirmation per `git-discipline.md`. If the user has already confirmed, proceed. If not, ask first.
