# Eval: wiki-query resolves the Momentum vault from a declared project_kb

**Eval ID:** wiki-query-resolves-momentum-kb
**Stakes:** correctness — a Momentum agent's diagnostic-table lookup must return Momentum-domain
knowledge, not nornspun's or an empty result (DEC-038 D2, PRD FR142)

## Scenario

**Given:**
- The multi-KB registry in `~/.obsidian-wiki/config` maps `KB_REGISTRY_MOMENTUM_AGENTIC_KB` to
  `/Users/steve/projects/momentum-agentic-kb` (a seeded, existing vault).
- A query term that matches a page seeded in that vault (e.g. "three-tier agent architecture
  manifesto diagnostic table", which resolves to `Momentum Three-Tier Agent Architecture`).

**When** `wiki-query` is invoked declaring `project_kb: momentum-agentic-kb` (via
`wiki-query --kb momentum-agentic-kb <query term>`, or via an invoking manifesto's identity block
carrying `project_kb: momentum-agentic-kb`) with that query term.

**Then:**
1. The skill's "Before You Start" resolution step looks up `KB_REGISTRY_MOMENTUM_AGENTIC_KB` in
   `~/.obsidian-wiki/config` and sets the active vault to `/Users/steve/projects/momentum-agentic-kb`
   for this invocation.
2. The answer is sourced from a page in the Momentum vault (traceable via `[[wikilink]]` citation
   to a page under `momentum-agentic-kb/`).
3. No nornspun-vault page is cited, and the result is not empty.

## Pass criteria

The returned answer cites a page from `momentum-agentic-kb` and the resolution step is observed
reading the `KB_REGISTRY_MOMENTUM_AGENTIC_KB` entry rather than the default `OBSIDIAN_VAULT_PATH`.

## Fail criteria

The answer cites a nornspun-vault page, is empty, or the resolution step ignores the declared
`project_kb` and reads the default `OBSIDIAN_VAULT_PATH` instead.

## Verification approach

Spawn a subagent with the modified `wiki-query` `SKILL.md` (`~/.agents/skills/wiki-query/SKILL.md`)
loaded as its instructions and the scenario above as its task. Observe which vault path it reads
in its resolution step and which page it cites.
