# Eval: Produces a conformant, KB-grounded manifesto draft

**Eval ID:** manifesto-builder-produces-conformant-grounded-draft
**Stakes:** correctness — a manifesto with invented entries or missing sections is a dead pipeline input; `build-guidelines` cannot compose an agent from it and the composed agent's routing table would be fiction.

**Given** a role (e.g. `dev`) and a domain (e.g. `kotlin-compose`) whose technology areas are represented in a reachable project knowledge base (KB),

**When** `momentum:manifesto-builder` is invoked and completes its full generate→curate→write flow,

**Then**:
1. A file exists at `.claude/manifests/{role}-{domain}.md`.
2. The file contains, in order: a YAML identity block (`role`, `domain`, `project_kb`); a `## Project Stack` section; a `## File Ownership` section with a non-empty `file_ownership` glob list in standard glob syntax; a `## Diagnostic Table` section.
3. The Diagnostic Table's entries are grouped under `###` technology-area headings, with multiple entries under at least one heading.
4. Every entry's `wiki-query` terms trace to concepts that actually exist in the project KB — running the same `wiki-query` against the KB returns non-empty, on-topic results. No entry's terms are invented placeholders unconnected to the KB's index.
5. Every entry's symptom reads as an observable, specific, diagnostic situation (per `manifesto-format.md`'s normative symptom-phrasing rules) — never a yes/no question, never vague language like "issues with X."
6. Every entry's `wiki-query` invocation is exact and backtick-rendered — never "search for X" or "consult the KB if needed."

## Verification approach

Read `skills/momentum/skills/manifesto-builder/SKILL.md` and `workflow.md`. Confirm:

1. The GENERATE phase instructs locating the vault (`cat ~/.obsidian-wiki/config`), reading the KB `index.md`, and running `wiki-query [concept]` (or `wiki-query --kb [project] [concept]` in multi-KB mode) per technology area of the role×domain — mirroring `constitution-builder`'s Phase 3 loop, not inventing an independent generation method.
2. The GENERATE phase instructs rendering each result as a grouped `- **<symptom>** → \`wiki-query <exact terms>\`` bullet under `###` area headings.
3. The GENERATE phase instructs drafting `## Project Stack` facts and a first-pass `## File Ownership` glob list from the role×domain's owned paths.
4. The FINALIZE phase instructs writing sections in the template order (identity block → Project Stack → File Ownership → Diagnostic Table) and self-checking against the four-section Phase-1-Discover checklist before writing.
5. The workflow never instructs fabricating a `wiki-query` term that wasn't sourced from a KB lookup, and never permits a placeholder like "search for X if needed."

Then spawn a subagent (or directly invoke the skill in an environment with a reachable KB — e.g. the nornspun-agentic-kb fixture at `~/.obsidian-wiki/config` OBSIDIAN_VAULT_PATH) with the skill loaded, task it to run `momentum:manifesto-builder` for `role=dev, domain=kotlin-compose`, and inspect the produced draft against points 1–6 above.

## Pass criteria

The produced (or, pre-write, the drafted) manifesto has all four sections in order, a non-empty concrete `file_ownership` list, grouped diagnostic-table entries with observable/specific/diagnostic symptoms, and every `wiki-query` invocation is exact, backticked, and traceable to real KB content (verifiable by running the same query).

## Fail criteria

Any of: a missing or reordered required section; a flat (non-grouped) diagnostic table; entries whose `wiki-query` terms return nothing when run against the KB (signaling invented content); a symptom phrased as a question or as vague "issue with X" language; a `wiki-query` invocation rendered as a vague placeholder instead of an exact backticked command.
