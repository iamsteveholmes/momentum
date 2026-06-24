# Eval: Constitution emits wiki-query block with both modes and exact syntax

## Scenario

Given: The constitution-builder skill is invoked to generate the standalone hot constitution for a project that has at least one knowledge base configured.

The skill should emit a `## Wiki-Query Interface` block (or equivalently labeled always-loaded section) that:

1. **Documents NORMAL mode** with the exact invocation string `wiki-query [question]` and states its behavior as tiered retrieval:
   - index scan first
   - then section grep
   - then full page read as needed
   - returns cited answers containing `[[wikilinks]]`

2. **Documents FAST / index-only mode** with the exact invocation string `wiki-query quick answer: [question]` and states its behavior as:
   - answers from page summaries and index only
   - no page bodies opened
   - cheaper than normal mode
   - good for factual lookups

3. **Lists ALL FOUR fast-mode trigger prefixes** that are treated as equivalent to `quick answer:`:
   - `quick answer:`
   - `just scan:`
   - `don't read the pages:`
   - `fast lookup:`

## Expected outcome

The generated constitution text contains a clearly labeled wiki-query interface block near the top-level (always-loaded) content. The block shows both invocation forms verbatim, both mode behavior descriptions, and all four trigger prefixes for fast mode. The block is not placed under a conditional heading or gated on project type.

## Pass criteria

- Block is present and clearly labeled
- Normal-mode invocation is exactly `wiki-query [question]`
- Normal mode describes tiered retrieval (index → grep → page read) with `[[wikilinks]]`
- Fast-mode invocation is exactly `wiki-query quick answer: [question]`
- Fast mode describes index-only behavior (no page bodies, cheaper, factual lookups)
- All four trigger prefixes listed for fast mode

## Fail criteria

- Block is absent
- Either mode is missing
- Either invocation string differs from the specified exact form
- Fast mode describes opening page bodies
- Fewer than four trigger prefixes listed
- Block is conditional or optional
