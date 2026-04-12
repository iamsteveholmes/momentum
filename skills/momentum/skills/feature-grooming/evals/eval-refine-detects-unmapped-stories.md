# Eval: Refine Detects Unmapped Stories

Given a `_bmad-output/planning-artifacts/features.json` with at least 3 feature entries, and a `_bmad-output/implementation-artifacts/stories/index.json` that contains at least one story that is neither dropped nor done and is not assigned to any feature slug present in features.json, the skill should:

1. Announce "refine" mode before any analysis output
2. In its final post-write output, include the count of unmapped stories (non-dropped, non-done stories not assigned to any feature)
3. In its final post-write output, list the slug of each unmapped story individually
