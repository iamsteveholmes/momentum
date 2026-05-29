# Eval: Halts on missing epic_slug or missing epic record

## Scenario

Two sub-scenarios tested independently. In both cases the skill `momentum:create-story`
is executing Step 7 (Write story metadata to stories/index.json). `stories/index.json`
exists with pre-existing entries.

### Sub-scenario A: Story has no epic_slug in frontmatter

Story file frontmatter:

```yaml
---
title: "Orphan story"
story_key: orphan-story
status: ready-for-dev
# epic_slug field is absent
---
```

`_bmad-output/planning-artifacts/epics.json` exists and is valid JSON.

### Sub-scenario B: Story has an epic_slug that does not match any record

Story file frontmatter:

```yaml
---
title: "Lost story"
story_key: lost-story
epic_slug: nonexistent-epic-that-does-not-exist
status: ready-for-dev
---
```

`_bmad-output/planning-artifacts/epics.json` exists but contains no key matching
`"nonexistent-epic-that-does-not-exist"`.

## Expected behavior

### Sub-scenario A: missing epic_slug

The skill should:
1. Detect that the story frontmatter has no `epic_slug` field (or the field is blank/null)
2. Emit a clear, actionable error message that:
   - Names the problem: missing `epic_slug` frontmatter
   - Instructs the developer to set `epic_slug` in the story frontmatter
   - Mentions `ad-hoc` as the catch-all value for stories not belonging to a named epic
3. HALT — stop execution before writing anything to `stories/index.json`

The skill should NOT silently continue with empty `depends_on`/`touches`. The
`stories/index.json` file must remain unmodified after the halt.

### Sub-scenario B: epic_slug present but record not found in epics.json

The skill should:
1. Load `_bmad-output/planning-artifacts/epics.json` as JSON
2. Attempt to look up the key `"nonexistent-epic-that-does-not-exist"`
3. Detect that no matching record exists
4. Emit a clear error message that:
   - Names the missing slug: `"nonexistent-epic-that-does-not-exist"`
   - States it was not found in `epics.json`
   - Instructs the developer to add the epic to `epics.json` or correct the `epic_slug`
     in the story frontmatter
5. HALT — stop execution before writing anything to `stories/index.json`

The skill should NOT silently create an index entry with empty fields. The
`stories/index.json` file must remain unmodified after the halt.
