# Eval: agent-resolve Returns Defaults dev Entry When No Project Entry Matches

## Purpose

Verify that `momentum-tools agent resolve --touches` returns the `defaults.dev`
entry when no project entry pattern matches any of the input paths, and verify
the `--role` flag returns the correct defaults entry for a named role.

## Expected Behavior

When no project entry's patterns match the input paths, `agent-resolve` must
fall back to the `defaults.dev` entry with all input paths in `file_scope`.
When `--role` is used, the named role's defaults entry is returned directly
without pattern matching.

## Inputs

### Test routing table (`momentum/agents.json`)

```json
{
  "defaults": {
    "architect": "skills/momentum/agents/architect.md",
    "pm": "skills/momentum/agents/pm.md",
    "ux": "skills/momentum/agents/ux.md",
    "analyst": "skills/momentum/agents/analyst.md",
    "researcher": "skills/momentum/agents/researcher.md",
    "dev": "skills/momentum/agents/dev.md",
    "sm": "skills/momentum/agents/sm.md",
    "qa-reviewer": "skills/momentum/agents/qa-reviewer.md",
    "e2e-validator": "skills/momentum/agents/e2e-validator.md"
  },
  "project": [
    {
      "role": "dev",
      "slug": "dev-cmp",
      "agent": ".claude/guidelines/agents/dev-cmp.md",
      "patterns": ["**/src/**/ui/**", "**/*.kt"],
      "write_permissions": ["src/main/kotlin/**/ui/**"]
    }
  ]
}
```

### Commands

**Test A — unmatched paths fall back to defaults:**
```
momentum-tools agent resolve --touches "src/api/routes.py,tests/unit/test_routes.py"
```

**Test B — role flag returns named defaults entry:**
```
momentum-tools agent resolve --role qa-reviewer
```

**Test C — empty touches returns base dev default:**
```
momentum-tools agent resolve
```

## Expected Output

### Test A

```json
{
  "action": "agent_resolve",
  "success": true,
  "results": [
    {
      "slug": "dev",
      "agent_path": "skills/momentum/agents/dev.md",
      "write_permissions": [],
      "file_scope": ["src/api/routes.py", "tests/unit/test_routes.py"]
    }
  ]
}
```

### Test B

```json
{
  "action": "agent_resolve",
  "success": true,
  "results": [
    {
      "slug": "qa-reviewer",
      "agent_path": "skills/momentum/agents/qa-reviewer.md",
      "write_permissions": [],
      "file_scope": []
    }
  ]
}
```

### Test C

```json
{
  "action": "agent_resolve",
  "success": true,
  "results": [
    {
      "slug": "dev",
      "agent_path": "skills/momentum/agents/dev.md",
      "write_permissions": [],
      "file_scope": []
    }
  ]
}
```

## Verification Steps

### Test A

1. Run: `momentum-tools agent resolve --touches "src/api/routes.py,tests/unit/test_routes.py"`
2. Parse the JSON output. Verify:
   - `success` is `true`
   - `results` array has exactly 1 entry
   - Entry has `slug == "dev"` (defaults fallback)
   - Entry has `agent_path == "skills/momentum/agents/dev.md"`
   - Entry `file_scope` contains both input paths
   - Entry `write_permissions` is an empty array

### Test B

1. Run: `momentum-tools agent resolve --role qa-reviewer`
2. Parse the JSON output. Verify:
   - `success` is `true`
   - `results` array has exactly 1 entry
   - Entry has `slug == "qa-reviewer"`
   - Entry has `agent_path == "skills/momentum/agents/qa-reviewer.md"`
   - Entry `file_scope` is an empty array (role lookup, no paths)
   - Entry `write_permissions` is an empty array

### Test C

1. Run: `momentum-tools agent resolve` (no flags)
2. Parse the JSON output. Verify:
   - `success` is `true`
   - `results` array has exactly 1 entry with `slug == "dev"`

## Expected Pass Criteria

- Unmatched paths produce a single results entry pointing to defaults.dev
- All input paths appear in the single result's `file_scope`
- `--role` flag bypasses pattern matching and returns the named role's defaults entry
- Empty touches returns the base `dev` default with empty `file_scope`

## Expected Fail Criteria

- Paths that don't match any project entry are silently dropped (not in any `file_scope`)
- `--role qa-reviewer` returns the `dev` entry instead of `qa-reviewer`
- `--role unknown-role` returns success instead of an error
- `results` is empty when fallback should apply
