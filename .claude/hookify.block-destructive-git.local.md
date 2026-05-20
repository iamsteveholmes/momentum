---
name: block-destructive-git
enabled: true
event: bash
pattern: git\s+(reset\s+--hard|clean\s+-f|push\s+--force)|git\s+checkout\s+--\s+\.
action: block
---

🚫 **Irreversible git operation blocked**

This command discards committed history or unrecoverable work. Never run autonomously — requires an explicit user instruction and should be extremely rare.

Blocked: reset --hard, clean -f, push --force, checkout -- .
