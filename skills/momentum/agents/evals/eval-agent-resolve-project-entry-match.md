# Eval: agent-resolve Returns Project Entry When Path Matches Pattern

## Purpose

Verify that `momentum-tools agent resolve --touches` returns the matching project
entry (not the defaults fallback) when an input path matches a pattern in the
`project` array of `momentum/agents.json`.

## Expected Behavior

When a project entry exists with patterns that match at least one input path,
`agent-resolve` must return that project entry's slug, agent path, and
write_permissions in the `results` array — not the defaults `dev` fallback.

## Inputs

### Test routing table (`momentum/agents.json`)

```json
{
  "defaults": {
    "ux": "skills/momentum/agents/ux.md",
    "analyst": "skills/momentum/agents/analyst.md",
    "researcher": "skills/momentum/agents/researcher.md",
    "dev": "skills/momentum/agents/dev.md",
    "qa-reviewer": "skills/momentum/agents/qa-reviewer.md",
    "e2e-validator": "skills/momentum/agents/e2e-validator.md"
  },
  "project": [
    {
      "role": "dev",
      "slug": "dev-cmp",
      "agent": "skills/momentum/agents/dev-build.md",
      "patterns": ["**/src/**/ui/**", "**/*.kt"],
      "write_permissions": ["src/main/kotlin/**/ui/**"]
    }
  ]
}
```

### Command

```
momentum-tools agent resolve --touches "src/main/kotlin/ui/Button.kt,src/api/routes.py"
```

## Expected Output

```json
{
  "action": "agent_resolve",
  "success": true,
  "results": [
    {
      "slug": "dev-cmp",
      "agent_path": "skills/momentum/agents/dev-build.md",
      "write_permissions": ["src/main/kotlin/**/ui/**"],
      "file_scope": ["src/main/kotlin/ui/Button.kt"]
    },
    {
      "slug": "dev",
      "agent_path": "skills/momentum/agents/dev.md",
      "write_permissions": [],
      "file_scope": ["src/api/routes.py"]
    }
  ]
}
```

## Verification Steps

1. Set up a test `momentum/agents.json` with the project entry above.

2. Run: `momentum-tools agent resolve --touches "src/main/kotlin/ui/Button.kt,src/api/routes.py"`

3. Parse the JSON output. Verify:
   - `success` is `true`
   - `results` array has exactly 2 entries
   - First entry has `slug == "dev-cmp"` and `agent_path == "skills/momentum/agents/dev-build.md"`
   - First entry `file_scope` contains `"src/main/kotlin/ui/Button.kt"` and NOT `"src/api/routes.py"`
   - First entry `write_permissions` equals `["src/main/kotlin/**/ui/**"]`
   - Second entry has `slug == "dev"` (defaults fallback for the unmatched path)
   - Second entry `file_scope` contains `"src/api/routes.py"` and NOT `"src/main/kotlin/ui/Button.kt"`

4. Verify the matched path does NOT appear in the defaults fallback `file_scope`.

## Expected Pass Criteria

- The project entry `dev-cmp` appears as a result with correct slug, agent_path, and write_permissions
- The matched path is in `dev-cmp`'s `file_scope`, not in the defaults fallback `file_scope`
- The unmatched path falls through to the defaults `dev` entry
- Both results are present and well-formed

## Expected Fail Criteria

- Both paths fall through to the defaults `dev` entry (pattern matching not working)
- The `dev-cmp` entry appears but contains the wrong `file_scope`
- `write_permissions` is missing or empty for the `dev-cmp` entry
- `results` array has only 1 entry when 2 are expected
