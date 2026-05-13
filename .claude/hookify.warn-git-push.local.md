---
name: warn-git-push
enabled: true
event: bash
pattern: ^\s*git\s+push(\s|$)
action: warn
---

⚠️ **git push detected**

Per `git-discipline.md`, before pushing you must:
1. Run `git log @{u}..HEAD --oneline` and show the commits to the user
2. Wait for explicit confirmation

Push is never autonomous — the preview ritual is required.
