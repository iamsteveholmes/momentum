# Eval: Produces and Registers ≥1 Composed Agent (DEC-038 G1)

**Eval ID:** build-guidelines-g1-registration
**Stakes:** load-bearing — G1 is the story's pass/fail gate

## Scenario

**Given:**
- A project has a conformant manifesto at `.claude/manifests/dev-kotlin-compose.md` containing:
  - Identity block: `role: dev`, `domain: kotlin-compose`, `project_kb: momentum-agentic-kb`
  - `## Project Stack` section with tech facts (including owned paths like `composeApp/`)
  - `## Diagnostic Table` with ≥1 symptom → `wiki-query` entry
- The plugin base body `skills/momentum/agents/dev.md` exists on disk
- `momentum/agents.json` does not yet exist
- `constitution-builder` write-mode parameterization is available (dependency honored)

**When** the developer invokes `/momentum:build-guidelines` and lets it complete a full run for the `dev × kotlin-compose` pair.

**Then** (observable behavior — all must hold):

1. A composed agent file exists on disk at `.claude/guidelines/agents/dev-kotlin-compose.md`
2. The composed file has YAML frontmatter with `name`, `model`, and `tools` fields
3. The composed file has a project-guidelines block containing the diagnostic table **above** a `---` separator
4. The full unmodified base role body appears **below** the `---` separator
5. No sprint identifier and no story identifier appears anywhere in the composed file
6. `momentum/agents.json` exists, parses as valid JSON with structure `{"defaults": {}, "project": [...]}`
7. `momentum/agents.json` contains a `project[]` entry keyed by `"slug": "dev-kotlin-compose"` with:
   - An `"agent"` field pointing to the composed file path
   - A `"patterns"` array that is **non-empty** (e.g., `["composeApp/**", "shared/**"]`)
8. Running `momentum-tools agent resolve --touches "composeApp/src/main/MyScreen.kt"` returns the
   **composed** slug `dev-kotlin-compose` — NOT the generic fallback slug `dev`.
   This is the critical production-path assertion: sprint-dev uses `--touches` to resolve agents at
   spawn time. If `--touches` returns the generic fallback, the composed agent is functionally dead
   regardless of whether the file exists on disk (root cause: `patterns: []` in agents.json).

## Outcome Criteria

**Pass:** All 8 observables confirmed, including that `--touches` returns the composed slug (observable 8).

**Fail — hard failure (G1 not met):**
- No file at `.claude/guidelines/agents/dev-kotlin-compose.md` after a successful run
- `momentum/agents.json` absent or missing the `project[]` entry after a successful run
- `momentum/agents.json` entry has `patterns: []` — `--touches` will fall through to the generic agent
- `momentum-tools agent resolve --touches "composeApp/src/main/MyScreen.kt"` returns the generic slug
  `dev` instead of the composed slug `dev-kotlin-compose`
- Composed file shape does not match: frontmatter + guidelines-block + `---` + base body

**Acceptable diagnostic behavior if dependency missing:**
- If `constitution-builder`'s `composed_agent_file` write mode is unavailable, the skill halts with a clear message naming the dependency gap — this is not a G1 failure but a dependency-gap failure.
