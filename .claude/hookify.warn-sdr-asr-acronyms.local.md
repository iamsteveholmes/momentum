---
name: warn-sdr-asr-acronyms
enabled: true
event: file
pattern: \b(SDR|ASR)\b
action: warn
---

⚠️ **SDR/ASR acronym detected**

Use the full names instead:
- `SDR` → "decision document"
- `ASR` → "assessment document"

Source: `feedback_sdr_asr_terminology.md`
