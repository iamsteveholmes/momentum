---
name: warn-cmux-send-key-uses-return
enabled: true
event: bash
pattern: cmux\s+send-key[^"']*["']Enter["']
action: warn
---

⚠️ **`cmux send-key` needs `"Return"`, not `"Enter"`**

The Enter key is spelled `"Return"` in cmux/iTerm/macOS keysym conventions. `"Enter"` silently fails — looks correct, does nothing.

Correct: `cmux send-key --surface <ref> "Return"`
