# Eval: Valid status transition updates story and returns confirmation

## Scenario

Given `stories/index.json` contains a story entry:

```json
{
  "stories": [
    {
      "slug": "posttooluse-lint-hook",
      "title": "PostToolUse Lint Hook",
      "epic_slug": "epic-0",
      "status": "in-progress",
      "depends_on": [],
      "touches": ["skills/momentum/hooks/"]
    }
  ]
}
```

When the sprint-manager receives:

```
Action: status_transition
Story: posttooluse-lint-hook
To: review
```

## Expected behavior

The skill should:
1. Read `stories/index.json`
2. Find the story with slug `posttooluse-lint-hook`
3. Validate that `in-progress -> review` is a legal forward transition
4. Update the story's `status` field to `review`
5. Write the updated JSON back, preserving all other fields
6. Return structured JSON: `{ "action": "status_transition", "story": "posttooluse-lint-hook", "from": "in-progress", "to": "review", "success": true }`
