---
name: warn-cmux-send-needs-return
enabled: true
event: bash
pattern: cmux\s+send\s+(?!-key)
action: warn
---

⚠️ **`cmux send` does not press Enter**

Follow with `cmux send-key --surface <ref> "Return"` to actually execute the command.

Source: `feedback_cmux_send_requires_sendkey.md`
