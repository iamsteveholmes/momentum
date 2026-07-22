# Live E2E Transcript — conduct-live-run-against-fixture-sprint

Story: `conduct-live-run-against-fixture-sprint` (sprint-2026-07-13). Run date: 2026-07-22. Invocation:

```
FIXTURE_DIR=~/projects/nornspun COMPOSED_SLUG=dev-kotlin-compose MATCH_PATH="composeApp/src/commonMain/kotlin/App.kt" NONMATCH_PATH="README.md" bash skills/momentum/skills/build-guidelines/e2e/live-compose-resolve.sh
```

Captured stdout (verbatim, complete):

`````
--- build-guidelines E2E: asserting composed fixture state ---
  fixture : /Users/steve/projects/nornspun
  slug    : dev-kotlin-compose
  match   : composeApp/src/commonMain/kotlin/App.kt
  nonmatch: README.md

## AC3 / AC5-guard — fixture agents.json project entry + verbatim patterns

  registered patterns: ["composeApp/**", "shared/**"]
  PASS: agents.json project entry 'dev-kotlin-compose' exists; patterns == manifesto File Ownership verbatim (AC3 / AC5-guard)

## AC2 — resolve --touches on matching path

Path: composeApp/src/commonMain/kotlin/App.kt

```json
{
  "action": "agent_resolve",
  "success": true,
  "results": [
    {
      "slug": "dev-kotlin-compose",
      "agent_path": ".claude/guidelines/agents/dev-kotlin-compose.md",
      "write_permissions": [
        "composeApp/**",
        "shared/**"
      ],
      "file_scope": [
        "composeApp/src/commonMain/kotlin/App.kt"
      ]
    }
  ]
}
```

  PASS: AC2: resolve --touches 'composeApp/src/commonMain/kotlin/App.kt' → 'dev-kotlin-compose' (composed slug, not dev)

## AC4 — composed agent file: /Users/steve/projects/nornspun/.claude/guidelines/agents/dev-kotlin-compose.md

File:                  /Users/steve/projects/nornspun/.claude/guidelines/agents/dev-kotlin-compose.md
Lines:                      325
Diagnostic Table hits: 2
Base-body marker:      present (You are a dev agent)

  PASS: AC4: composed file has base body + '## Diagnostic Table' section

## AC5 — negative control: resolve --touches on non-matching path

Path: README.md

```json
{
  "action": "agent_resolve",
  "success": true,
  "results": [
    {
      "slug": "dev",
      "agent_path": ".claude/guidelines/agents/dev-kotlin-compose.md",
      "write_permissions": [],
      "file_scope": [
        "README.md"
      ]
    }
  ]
}
```

  PASS: AC5: resolve --touches 'README.md' → 'dev' (genuine pattern match, not vacuous)

## Summary

| Assertion | Result |
|---|---|
| AC3 / AC5-guard: agents.json project entry + verbatim patterns | PASS |
| AC2: resolve 'composeApp/src/commonMain/kotlin/App.kt' → dev-kotlin-compose (not dev) | PASS |
| AC4: composed file has base body + Diagnostic Table | PASS |
| AC5 negative: resolve 'README.md' → dev | PASS |

All assertions passed. Driver exited 0.

PASS — all assertions hold.
Evidence artifact: docs/research/live-e2e-compose-resolve-evidence.md
`````

Observed exit code:

```
exit=0
```
