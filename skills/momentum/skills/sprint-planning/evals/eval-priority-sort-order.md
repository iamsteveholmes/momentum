# Eval: Priority Sort Order Within Epic Groups

**Given:** A stories/index.json with one epic containing 4 stories with these properties:
- story-a: priority=low, no dependencies
- story-b: priority=critical, no dependencies
- story-c: priority=medium, no dependencies
- story-d: priority=high, no dependencies

The sprint-planning workflow reaches Step 1 (backlog presentation).

**The skill should:**
- Sort stories within the epic group as: story-b [C] first, story-d [H] second, story-c [M] third, story-a [L] last
- Priority is the primary sort key: critical before high before medium before low
- Dependency depth is the secondary key (within same priority level, leaves appear before stories with pending deps)
- Alphabetical is the tertiary key (within same priority and depth)

**Observable outcome:** The listing order within the epic block shows critical stories first, then high, then medium, then low — not alphabetical or arbitrary order.
