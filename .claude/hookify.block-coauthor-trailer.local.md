---
name: block-coauthor-trailer
enabled: true
event: bash
pattern: Co-Authored-By:\s*Claude
action: block
---

🚫 **Co-Authored-By trailer detected**

Do not include `Co-Authored-By: Claude` trailers in commit messages.

Source: `feedback_no_coauthor_trailer.md`
