# Eval: Priority Display in Backlog

**Given:** A stories/index.json with 4 stories across 2 epics, each with different priority values (critical, high, medium, low). The sprint-planning workflow is invoked and reaches Step 1 (backlog presentation).

**The skill should:**
- Display a compact priority badge — `[C]` for critical, `[H]` for high, `[M]` for medium, `[L]` for low — next to each story title in the backlog listing
- Stories missing a priority field are treated as `[L]`
- The badge appears consistently for every story in the listing, not just some

**Observable outcome:** The Step 1 output contains `[C]`, `[H]`, `[M]`, or `[L]` labels next to story entries.
