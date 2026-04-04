# Eval: Symbol-Text Pairing Accessibility

## Scenario

Given any Impetus response that contains symbols from the Momentum vocabulary (✓, →, ◦, !, ✗, ?), every symbol must have adjacent text that conveys the same meaning. This ensures the response is accessible when Unicode symbols don't render correctly in a terminal.

## Expected Behavior

For each symbol in any Impetus response:
- ✓ is paired with text like "completed", "built", "done", "confirmed", "passing", or a value summary phrase
- → is paired with text like "now", "current", "active", or a description of the current activity
- ◦ is paired with text like "next", "upcoming", "pending", "ahead", or a description of what follows
- ! is paired with text describing the warning condition
- ✗ is paired with text describing the failure or blockage
- ? is paired with text describing the question or decision needed

Examples of correct pairing:
- `✓  Brief · Research · PRD · UX      vision through interaction patterns done` — ✓ paired with value summary
- `→  Architecture                     making implementation decisions` — → paired with activity description
- `◦  Epics · Stories                  2 phases to implementation` — ◦ paired with upcoming description
- `!  Restart Claude Code when ready` — ! paired with warning text
- `✗  lint check failed — missing semicolon` — ✗ paired with failure description

Examples of violations:
- `✓` appearing alone on a line with no text
- `→` as a bullet point without descriptive text
- `◦ ◦ ◦` used decoratively without meaning
- Any symbol used as pure decoration without carrying semantic meaning

## NOT Expected

- A symbol appearing without adjacent text on the same line
- Symbols used as decorative separators or borders
- Meaning conveyed solely through the symbol with no text fallback
