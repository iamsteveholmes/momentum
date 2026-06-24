# Eval: Wiki-query block makes KB selection explicit for multi-KB projects

## Scenario

Given: The constitution-builder skill is invoked in two configurations:
- **Configuration A:** A project with more than one knowledge base configured (e.g., a Momentum project KB + a nornspun project KB)
- **Configuration B:** A project with exactly ONE knowledge base configured

The wiki-query interface block should handle both configurations correctly.

## Expected behavior — Configuration A (multi-KB)

The generated wiki-query block makes **knowledge-base selection explicit** when more than one KB is configured:
- States that when multiple KBs are available, the agent must specify which KB to query (project-scoped selection)
- Provides syntax for selecting a specific KB (e.g., `wiki-query --kb [kb-name] [question]` or equivalent explicit selection form)
- Makes clear that selecting the right KB (by project scope) is part of the invocation, not inferred

## Expected behavior — Configuration B (single-KB)

The generated wiki-query block **degrades cleanly** to single-KB form:
- Does not require explicit KB selection ceremony when only one KB is configured
- Single-KB syntax matches the canonical forms: `wiki-query [question]` and `wiki-query quick answer: [question]`
- No mandatory KB specifier in the invocation

## Expected outcome

The skill produces a wiki-query block that branches on KB count:
- Multi-KB: the block documents explicit KB selection as part of the invocation
- Single-KB: the block uses the canonical plain syntax without an explicit selection step

The block does NOT silently assume a single global vault when the project has multiple KBs.

## Pass criteria (Configuration A — multi-KB)

- Block explicitly mentions that multiple KBs require specifying which KB to query
- Syntax for multi-KB invocation is shown (project-scoped selection)
- The guidance is part of always-loaded constitution content (not conditional)

## Pass criteria (Configuration B — single-KB)

- Block uses simple canonical syntax (`wiki-query [question]`, `wiki-query quick answer: [question]`)
- No mandatory KB specifier required in single-KB mode
- Block is structurally identical to multi-KB block except for the KB-selection guidance

## Fail criteria

- Multi-KB block silently assumes one global vault (no mention of KB selection)
- Single-KB block requires unnecessary explicit selection ceremony
- Block omits multi-KB guidance entirely for multi-KB projects
