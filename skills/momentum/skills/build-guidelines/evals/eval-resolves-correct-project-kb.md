# Eval: Resolves the Correct Project KB (DEC-038 D2 Multi-KB)

**Eval ID:** build-guidelines-multi-kb-resolution
**Stakes:** correctness — wrong KB produces agent with citations for a different project

## Scenario

**Given:**
- Two projects coexist with separate KBs:
  - Project A: Momentum (`project_kb: momentum-agentic-kb`)
  - Project B: nornspun (`project_kb: nornspun-agentic-kb`)
- The developer is running `/momentum:build-guidelines` in the Momentum project directory
- A manifesto at `.claude/manifests/dev-kotlin-compose.md` declares `project_kb: momentum-agentic-kb`
- The manifesto's diagnostic table contains `wiki-query` terms written against the Momentum KB

**When** the skill runs the Discover phase and resolves the project + KB for this run.

**Then** (observable behavior — all must hold):

1. The skill reads `project_kb` from the manifesto identity block to determine which KB to resolve against
2. Every `wiki-query` invocation downstream targets the Momentum KB, not the nornspun KB
3. The composed agent file's diagnostic table citations reference Momentum KB page slugs only
4. No nornspun KB page names appear in the composed output's wiki-query entries
5. If the manifesto declares `project_kb: nornspun-agentic-kb` instead, the skill drives queries against the nornspun KB — KB targeting follows the manifesto declaration, not the working directory

## Outcome Criteria

**Pass:** KB resolution follows `project_kb` in the manifesto identity block. Citations in the composed file match the declared KB.

**Fail:**
- Skill drives queries against a KB other than the one declared in `project_kb`
- Composed file contains `wiki-query` terms that would only resolve in a different project's KB
- Skill ignores `project_kb` and uses a hardcoded or environment-derived KB name

## Notes

The multi-KB extension to `wiki-query` (FR142) is not yet implemented — current `wiki-query` resolves against the active vault. However, the skill must still read and preserve the `project_kb` field from the manifesto and pass it as context to `constitution-builder` invocations, so the pipeline is ready when FR142 lands. The observable for this eval is that the skill reads and surfaces `project_kb` during the Discover phase, not that it mechanically routes to separate vaults.
