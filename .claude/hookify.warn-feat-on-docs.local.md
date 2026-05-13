---
name: warn-feat-on-docs
enabled: true
event: bash
pattern: git\s+commit[^"']*["'](feat|fix|refactor|perf|test|style)\([^)]*\):[^"']*\b(PRD|epic|story|architecture|UX|research|brief|spec)\b
action: warn
---

⚠️ **Possible misuse of code commit type on docs/spec change**

`feat`, `fix`, `refactor`, `perf`, `test`, `style` are for CODE changes only. Spec and planning artifacts (PRD, epic, story, architecture, UX, research, brief) should use `docs(scope)`.

Source: `feedback_conventional_commits_code_vs_docs.md`, `~/.claude/rules/git-discipline.md`

Note: This rule has higher false-positive potential — review the commit subject before treating as binding.
