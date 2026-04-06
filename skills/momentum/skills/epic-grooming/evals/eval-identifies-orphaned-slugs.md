---
eval: identifies-orphaned-slugs
behavior: Data collection produces accurate orphan/registered split
---

# Eval: Identifies Orphaned Epic Slugs

## Scenario

Given a `stories/index.json` containing stories assigned to 20 distinct `epic_slug` values, and an `epics.md` file whose Epic List section defines only 13 named epics (e.g., "Epic 1: Foundation & Bootstrap", "Epic 2: Stay Oriented with Impetus", etc.), the skill should:

1. Extract all unique `epic_slug` values from `stories/index.json` with their story counts (e.g., `impetus-core: 17`, `agent-team-model: 5`).
2. Cross-reference against the epics registered in `epics.md` to produce two lists:
   - **Registered:** slugs that have a matching named section in epics.md
   - **Orphaned:** slugs that appear in stories but have no definition in epics.md
3. Display the orphaned list clearly (e.g., `agent-team-model (5)`, `greeting-redesign (4)`, `harden-epic-2-foundation (5)`, `impetus-core (17)`, `plugin-migration (6)`, `process-stories (4)`, `research-knowledge-management (3)`) before proceeding to taxonomy analysis.
4. NOT proceed to proposals until the full data picture is assembled and surfaced to the developer.

## Expected behavior

The skill presents a data summary table or list showing:
- Total unique slugs found in stories/index.json
- Registered slugs (with epic title and story count)
- Orphaned slugs (slug, story count, sample story titles for context)

The skill does NOT begin proposing merges or taxonomy changes during Phase 1. It completes data collection, confirms the picture, then transitions to Phase 2.
