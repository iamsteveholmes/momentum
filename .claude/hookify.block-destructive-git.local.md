---
name: block-destructive-git
enabled: true
event: bash
pattern: git\s+(reset\s+--hard|clean\s+-f|push\s+--force|branch\s+-D|stash\s+drop)|git\s+rebase\b|git\s+checkout\s+--\s+\.
action: block
---

🚫 **Destructive git operation detected**

This command rewrites history or discards work. It requires explicit user request per `git-discipline.md` — never run autonomously.

Allowed only when the user explicitly asks for: reset --hard, clean -f, push --force, branch -D, stash drop, rebase, or checkout -- .
