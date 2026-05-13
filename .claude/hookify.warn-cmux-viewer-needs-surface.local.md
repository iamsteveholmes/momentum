---
name: warn-cmux-viewer-needs-surface
enabled: true
event: bash
pattern: cmux\s+(markdown|browser)\s+open\b(?!.*--surface)
action: warn
---

⚠️ **Viewer opened without `--surface`**

Markdown and browser viewers must open as tabs in the existing viewer pane — pass `--surface <existing-ref>`, never create a new split.

Source: `feedback_cmux_open_in_tabs.md`, `~/.claude/rules/cmux.md`
