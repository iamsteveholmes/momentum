# Eval: Ownership field flows verbatim into agents.json patterns

**Given** a manifesto whose `## File Ownership` section declares:

```yaml
file_ownership:
  - "skills/**/*.md"
  - "skills/**/*.sh"
```

**When** build-guidelines runs the agent-composition process for that manifesto (Phase 1 validates the field is present, Phase 3 passes it to agent-builder as `permissions_scope`),

**Then** the produced `momentum/agents.json` project entry for the composed agent has:

```json
"patterns": ["skills/**/*.md", "skills/**/*.sh"]
```

exactly — no glob added, dropped, reordered, or reworded relative to the manifesto's `file_ownership` list. The patterns value is the verbatim field value, not an LLM-inferred approximation from `## Project Stack` prose.

## Verification approach

Read the manifesto format spec (`skills/momentum/references/manifesto-format.md`) and build-guidelines `workflow.md` Phase 3 `permissions_scope` action. Confirm:

1. Phase 3 instructs the orchestrator to read the `## File Ownership` field verbatim and pass it unchanged as `permissions_scope`.
2. There is no "derive from `## Project Stack` prose" or "default to broad-match" path for resolver-critical globs when the ownership field is present.
3. agent-builder writes `patterns = permissions_scope` without modification (this is the existing agent-builder contract; no agent-builder change is needed).

## Pass criteria

The workflow instruction for `permissions_scope` reads the File Ownership field verbatim with no inference fallback when the field is populated.

## Fail criteria

The workflow instruction for `permissions_scope` still says "derive from ## Project Stack paths" or "default to broad-match patterns" — meaning an LLM inference path remains for resolver-critical globs when the ownership field is populated.
