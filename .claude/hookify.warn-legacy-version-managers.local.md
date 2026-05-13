---
name: warn-legacy-version-managers
enabled: true
event: all
pattern: \b(nvm|fnm|volta|pyenv|rbenv|asdf)\s+(install|use|exec|shell|local|global)\b
action: warn
---

⚠️ **Legacy version manager detected**

Use `mise` instead — it replaces nvm, fnm, volta, pyenv, rbenv, and asdf.

Source: `~/.claude/rules/mise.md`, `~/.claude/rules/anti-patterns.md`
