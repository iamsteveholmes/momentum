# Eval: Invalid status transition is rejected with error

## Scenario

Given `stories/index.json` contains a story entry:

```json
{
  "stories": [
    {
      "slug": "sprint-manager-skill",
      "title": "Sprint Manager Skill",
      "epic_slug": "epic-0",
      "status": "backlog",
      "depends_on": [],
      "touches": ["skills/momentum-sprint-manager/"]
    }
  ]
}
```

When the sprint-manager receives:

```
Action: status_transition
Story: sprint-manager-skill
To: done
```

## Expected behavior

The skill should:
1. Read `stories/index.json`
2. Find the story with slug `sprint-manager-skill`
3. Determine that `backlog -> done` skips intermediate states and is NOT a legal transition
4. NOT modify `stories/index.json`
5. Return structured JSON: `{ "action": "status_transition", "story": "sprint-manager-skill", "from": "backlog", "to": "done", "success": false, "error": "..." }` where the error explains the illegal transition
