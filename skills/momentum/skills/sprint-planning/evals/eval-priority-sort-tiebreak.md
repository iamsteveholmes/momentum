# Eval: Priority Sort Tiebreak by Dependency Depth then Alphabetical

**Given:** A stories/index.json with one epic containing 3 stories with the same priority (medium):
- story-alpha: priority=medium, no dependencies (leaf)
- story-beta: priority=medium, depends_on: [story-alpha] (blocked by alpha)
- story-gamma: priority=medium, no dependencies (leaf)

The sprint-planning workflow reaches Step 1.

**The skill should:**
- Sort within the medium priority group by dependency depth first: story-alpha and story-gamma (leaves, depth 0) appear before story-beta (depth 1, has pending dep)
- Within the same depth, sort alphabetically: story-alpha appears before story-gamma

**Observable outcome:** The medium stories appear in order: story-alpha, story-gamma, story-beta — demonstrating depth tiebreak then alphabetical tiebreak.
