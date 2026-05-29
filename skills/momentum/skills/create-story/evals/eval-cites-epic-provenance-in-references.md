# Eval: Cites epic provenance in the story body's References subsection

## Scenario

Given a Momentum story file `{{story_file}}` with frontmatter:

```yaml
---
title: "Some story"
story_key: some-story
epic_slug: momentum-backlog-refinement
status: ready-for-dev
---
```

And `_bmad-output/planning-artifacts/epics.json` contains a record keyed by
`"momentum-backlog-refinement"`.

The skill `momentum:create-story` is executing the step that reads epic context from epics.json
(DEC-034 D6) and writes epic provenance into the story body.

## Expected behavior

The skill should write the epic provenance into the story file BODY — not only into
`stories/index.json` or the frontmatter — so the generated story cites the epic it was routed under:

1. Locate the `### References` subsection within the Dev Notes section.
2. If no `### References` subsection exists, create one at the end of the Dev Notes section.
3. Append a citation bullet that names the source `epic_slug`:

   ```
   - Epic context: `momentum-backlog-refinement` (from _bmad-output/planning-artifacts/epics.json)
   ```

4. Do not duplicate the bullet if an identical citation already exists in `### References`.
5. Output confirmation:
   `Epic provenance cited in {{story_file}} body — References → momentum-backlog-refinement`

After the step completes, the rendered story body's `### References` subsection names the source
epic_slug verbatim.

## What This Tests

- Epic provenance lands in the story body's `### References` subsection, not just in index.json/frontmatter
- The cited value is the story's actual `epic_slug` (`momentum-backlog-refinement`), not a placeholder
- A `### References` subsection is created under Dev Notes when absent
- The citation is idempotent — re-running does not append a duplicate bullet

## Notes

This eval realizes the contract the create-story workflow references in-line ("Eval contract b2
Scenario 5 requires the story body's References subsection to name the source epic"). The workflow
comment and this eval are kept in sync — if the citation format or location changes in the workflow,
update this eval.
