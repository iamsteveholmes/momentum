# Eval: an unregistered project_kb surfaces the mismatch rather than masking it (seam clause)

**Eval ID:** wiki-query-unregistered-project-kb-surfaces-mismatch
**Stakes:** correctness / safety — silently substituting an unrelated project's vault content for
an unregistered `project_kb` would mask a real producer/consumer mismatch as a false positive
result

## Scenario

**Given:** the multi-KB registry (`~/.obsidian-wiki/config`) contains only
`KB_REGISTRY_MOMENTUM_AGENTIC_KB` and `KB_REGISTRY_NORNSPUN_AGENTIC_KB`.

**When** `wiki-query` is invoked declaring a `project_kb` value that has no corresponding registry
entry (e.g. `project_kb: some-other-project-kb`).

**Then:**
1. The resolver does not silently fall back to the default `OBSIDIAN_VAULT_PATH` or to either
   registered vault as though it matched.
2. The absence of a matching registry entry is surfaced explicitly in the outcome (e.g. an
   explicit "no KB registered for project_kb: `some-other-project-kb`" message) rather than
   masked by returning content from an unrelated vault.
3. No page content from `momentum-agentic-kb` or `nornspun-agentic-kb` is presented as if it
   answered the query under the unregistered `project_kb`.

## Pass criteria

The resolver's outcome makes the mismatch observable — an explicit unresolved/no-match signal —
and never returns an unrelated project's vault content as though it matched the declared,
unregistered `project_kb`.

## Fail criteria

The resolver silently returns content from `momentum-agentic-kb` or `nornspun-agentic-kb` (or any
other vault) for the unregistered `project_kb` declaration, masking the mismatch between what was
declared and what the registry recognizes.

## Verification approach

Spawn a subagent with the modified `wiki-query` `SKILL.md` loaded and the scenario above as its
task. Confirm it reports the missing-registry-entry condition explicitly and does not proceed to
read any vault's `index.md`/`hot.md` as though resolution had succeeded.
