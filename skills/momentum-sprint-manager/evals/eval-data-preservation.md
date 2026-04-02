# Eval: Data preservation during status update

## Scenario

Given `stories/index.json` contains multiple stories:

```json
{
  "stories": [
    {
      "slug": "story-alpha",
      "title": "Story Alpha",
      "epic_slug": "epic-0",
      "status": "done",
      "depends_on": [],
      "touches": ["skills/alpha/"]
    },
    {
      "slug": "story-beta",
      "title": "Story Beta",
      "epic_slug": "epic-1",
      "status": "in-progress",
      "depends_on": ["story-alpha"],
      "touches": ["skills/beta/", "docs/beta.md"]
    },
    {
      "slug": "story-gamma",
      "title": "Story Gamma",
      "epic_slug": "epic-1",
      "status": "ready-for-dev",
      "depends_on": ["story-beta"],
      "touches": ["skills/gamma/"]
    }
  ]
}
```

When the sprint-manager receives:

```
Action: status_transition
Story: story-gamma
To: in-progress
```

## Expected behavior

The skill should:
1. Update only `story-gamma`'s status to `in-progress`
2. Preserve `story-alpha` and `story-beta` completely unchanged (status, epic_slug, depends_on, touches, title -- all fields identical)
3. Preserve the overall JSON structure
4. Return success confirmation
5. The written JSON must be valid and parseable
