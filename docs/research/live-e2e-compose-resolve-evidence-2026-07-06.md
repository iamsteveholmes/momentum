# Live E2E Evidence — build-guidelines compose + register + resolve

**Status: PRE-COMPOSITION TEMPLATE**

The composition phase (momentum:build-guidelines → momentum:agent-builder) has not yet been run
against the nornspun fixture. This file satisfies the AC6 committed-artifact requirement and
documents the expected evidence shape; it must be replaced by real output once the composition
phase runs.

To regenerate with real evidence:
1. Complete the composition phase per `skills/momentum/skills/build-guidelines/e2e/README.md`
2. Run the assertion driver from the Momentum repo root:
   ```bash
   FIXTURE_DIR=~/projects/nornspun \
   COMPOSED_SLUG=dev-kotlin-compose \
   MATCH_PATH="composeApp/src/commonMain/kotlin/App.kt" \
   NONMATCH_PATH="README.md" \
   OWNERSHIP_GLOBS='["composeApp/**","shared/**"]' \
   bash skills/momentum/skills/build-guidelines/e2e/live-compose-resolve.sh
   ```
3. The driver overwrites this file with the dated real-run artifact.

---

Supersedes: sprint-2026-06-18 integration-TRACE (a hand-walked instruction trace, not live
execution). The real-run artifact that replaces this template is the running-app proof.

---

## Expected shape when populated by the driver

```
Generated: <ISO timestamp>
Driver:    skills/momentum/skills/build-guidelines/e2e/live-compose-resolve.sh
Fixture:   /Users/steve/projects/nornspun
Slug:      dev-kotlin-compose
Ownership: ["composeApp/**","shared/**"]

## AC3 / AC5-guard — fixture agents.json project entry + verbatim patterns

  registered patterns: ["composeApp/**","shared/**"]
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
      ...
    }
  ]
}
```

  PASS: AC2: resolve --touches 'composeApp/src/commonMain/kotlin/App.kt' → 'dev-kotlin-compose' (composed slug, not dev)

## AC4 — composed file checks

File:                  /Users/steve/projects/nornspun/.claude/guidelines/agents/dev-kotlin-compose.md
Lines:                 <N>
Diagnostic Table hits: <N>
Base-body marker:      present

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
      ...
    }
  ]
}
```

  PASS: AC5: resolve --touches 'README.md' → 'dev' (genuine pattern match, not vacuous)

## Summary

| Assertion | Result |
|---|---|
| AC3 / AC5-guard: agents.json project entry + verbatim patterns | PASS |
| AC2: resolve 'composeApp/...' → dev-kotlin-compose (not dev) | PASS |
| AC4: composed file has base body + Diagnostic Table | PASS |
| AC5 negative: resolve 'README.md' → dev | PASS |

All assertions passed. Driver exited 0.
```

---

## Why this template exists

Story `live-e2e-compose-register-resolve-gen-2-agent` requires a committed evidence artifact
under `docs/research/live-e2e-compose-*.md` as AC6. The composition phase is an LLM skill
invocation (momentum:build-guidelines + momentum:agent-builder) that cannot be run headlessly
in the automated build environment. The executable assertion driver is complete and ready;
the composition phase must be run as a developer/agent step to produce real evidence.

Driver location: `skills/momentum/skills/build-guidelines/e2e/live-compose-resolve.sh`
Run procedure:   `skills/momentum/skills/build-guidelines/e2e/README.md`
