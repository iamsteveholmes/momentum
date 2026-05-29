# Eval: Reads epic context from epics.json for touches and depends_on

## Scenario

Given a Momentum story file with frontmatter:

```yaml
---
title: "Some story"
story_key: some-story
epic_slug: momentum-backlog-refinement
status: ready-for-dev
---
```

And `_bmad-output/planning-artifacts/epics.json` contains a record keyed by
`"momentum-backlog-refinement"` with the following shape:

```json
{
  "momentum-backlog-refinement": {
    "epic_slug": "momentum-backlog-refinement",
    "name": "Backlog Refinement and Epic Taxonomy",
    "system_context": "Feeds sprint-planning with ready stories. Touches skills/momentum/skills/epic-grooming/ and skills/momentum/skills/refine/ for implementation. Without backlog hygiene, sprint-planning is selecting from a noisy, partially-valid input.",
    "acceptance_conditions": ["..."],
    "stories": [
      { "slug": "prev-story", "depends_on": [] }
    ]
  }
}
```

The skill `momentum:create-story` is executing Step 7 (Write story metadata to
stories/index.json). `stories/index.json` exists and contains existing entries.

## Expected behavior

The skill should:

1. Load `_bmad-output/planning-artifacts/epics.json` as JSON (NOT read `epics.md`)
2. Look up the record keyed by the story's `epic_slug` value (`"momentum-backlog-refinement"`)
3. Extract `touches` from the epic record's `system_context` field — identifying skill
   directories or paths mentioned in the text:
   - `skills/momentum/skills/epic-grooming/`
   - `skills/momentum/skills/refine/`
4. Write the new story entry in `stories/index.json` with:
   - `touches` array containing both directories extracted above
   - `depends_on` array (empty `[]` if no explicit cross-references found)
   - `status: "ready-for-dev"`
   - `epic_slug: "momentum-backlog-refinement"`
5. Output confirmation: "Story metadata written to stories/index.json — depends_on: [],
   touches: [skills/momentum/skills/epic-grooming/, skills/momentum/skills/refine/]"

The skill should NOT:
- Read `epics.md` at any point in this step
- Read or reference `features.json`
- Prompt the user during this step
- Silently omit the extracted paths from `touches`
