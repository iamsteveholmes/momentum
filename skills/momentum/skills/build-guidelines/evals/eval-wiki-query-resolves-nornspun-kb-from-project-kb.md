# Eval: wiki-query resolves the nornspun vault from a declared project_kb, and default fallback is unchanged

**Eval ID:** wiki-query-resolves-nornspun-kb-and-default-fallback
**Stakes:** correctness — the multi-KB extension must not regress the existing single-vault
behavior for nornspun callers or for callers that declare no `project_kb` (AC5 no-regression
clause)

## Scenario

**Given:**
- The multi-KB registry maps `KB_REGISTRY_NORNSPUN_AGENTIC_KB` to
  `/Users/steve/projects/nornspun-agentic-kb` (the pre-existing, populated nornspun vault).
- `OBSIDIAN_VAULT_PATH` (the default/fallback) is unchanged and still points at
  `/Users/steve/projects/nornspun-agentic-kb`.
- A query term known to resolve in the nornspun vault (e.g. a concept page title already present
  there, such as "Acceptance Test-Driven Development").

**When** `wiki-query` is invoked twice with the same query term:
1. Once declaring `project_kb: nornspun-agentic-kb` explicitly.
2. Once with **no** `project_kb` declared at all.

**Then:**
1. Invocation 1 resolves `KB_REGISTRY_NORNSPUN_AGENTIC_KB` and reads the nornspun vault.
2. Invocation 2 (no context) falls back to reading `OBSIDIAN_VAULT_PATH` directly, exactly as
   `wiki-query` behaved before this story's change.
3. Both invocations return the same nornspun-vault page and cite it — the no-context path is not
   observably different from the pre-change single-vault behavior.

## Pass criteria

Both invocations return content traceable to the nornspun vault; the no-`project_kb` invocation's
resolution step reads `OBSIDIAN_VAULT_PATH` directly (no registry lookup attempted), matching
prior behavior exactly.

## Fail criteria

Either invocation fails to resolve, resolves to a different vault than expected, or the
no-`project_kb` invocation behaves differently than the pre-change default (e.g. it now requires
a `project_kb` to succeed, or it silently reads a registry entry when none was declared).

## Verification approach

Spawn a subagent with the modified `wiki-query` `SKILL.md` loaded and run both invocations from
the scenario. Confirm the vault path read in each case and that the no-context case does not
consult the `KB_REGISTRY_*` entries at all.
