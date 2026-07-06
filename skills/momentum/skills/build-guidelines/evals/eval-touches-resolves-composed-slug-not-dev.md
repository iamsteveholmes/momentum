# Eval: Composed agent resolves deterministically to its own slug, not the dev fallback

**Given** an agent composed from a manifesto whose `## File Ownership` section declares:

```yaml
file_ownership:
  - "skills/**/*.md"
  - "skills/**/*.sh"
```

**And** that agent is registered in `momentum/agents.json` with `patterns` equal to the ownership field verbatim (as verified by `eval-reads-ownership-field-verbatim-into-patterns`),

**When** `momentum-tools agent resolve --touches "skills/momentum/skills/build-guidelines/SKILL.md"` is invoked (a path matching the first declared glob),

**Then** the resolver returns the composed `{role}-{domain}` slug (e.g., `dev-skills`), NOT the generic `dev` fallback.

The match is driven by the declared `file_ownership` patterns in `agents.json`, not by any LLM inference.

## Verification approach

1. Confirm Phase 5 of build-guidelines `workflow.md` runs `momentum-tools agent resolve --touches` against a representative path for each composed agent and asserts the returned slug is the composed slug (not the generic fallback).
2. Confirm Phase 6 (G1 gate) also runs this resolver check: `momentum-tools agent resolve --touches "{{representative_path}}"` returns the composed slug, not the generic `dev`, as a prerequisite for `G1 Gate: PASSED`.
3. The representative path used must match one of the declared ownership globs — not an arbitrary path.

## Pass criteria

`momentum-tools agent resolve --touches <path matching a declared ownership glob>` returns the composed `{role}-{domain}` slug. G1 gate passes.

## Fail criteria

The resolver returns the generic `dev` fallback for a path that matches a declared ownership glob. This indicates `patterns[]` in the agents.json entry is empty, mismatched, or was populated from a guessed inference rather than the declared field.
