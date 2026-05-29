# Eval: Refine Detects Unmapped Stories

Given a `_bmad-output/planning-artifacts/epics.json` with at least 3 epic entries, and a `.momentum/stories/index.json` that contains at least one story that is neither dropped nor done and whose `epic_slug` does not match any epic slug defined in epics.json, the skill should:

1. Announce "refine" mode before any analysis output
2. In its signal-detection phase, include a NEW signal count for capability clusters from story themes not represented in epics.json
3. In its final post-write output, include the count of unmapped stories (non-dropped, non-done stories whose epic_slug has no entry in epics.json)
4. In its final post-write output, list the slug of each unmapped story individually
5. Prompt the developer to run epic-grooming again (refine) or add the epic_slug to epics.json to resolve any remaining unmapped items
