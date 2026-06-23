# Eval: Wiki-query triggers in constitution are prescriptive, not permissive

## Scenario

Given: The constitution-builder skill generates the standalone hot constitution (single or multi-KB project).

The wiki-query interface block should contain a **prescriptive trigger section** where:

1. Each trigger is written as an **imperative naming the exact moment** when a wiki-query is required before proceeding.
2. Each trigger pairs the moment with an **exact query string** (e.g., `wiki-query [specific question]`).
3. Example of correct prescriptive phrasing: "Before selecting a test pattern for a new library, run `wiki-query what test patterns apply to [library]`."
4. The block contains **NONE** of the following permissive phrases:
   - "if you need"
   - "consult the KB if needed"
   - "you may want to"
   - "consider consulting"
   - "feel free to"
   - "when helpful"
   - "as needed"

5. The triggers cover **cross-cutting scenarios** (moments that apply across agents and projects) — not per-agent symptom-to-query diagnostic table rows.

6. The block contains **NO per-agent symptom→query routing rows** — no table mapping a specific agent's observed symptom to a lookup. Per-agent routing belongs at the manifesto layer, not in the shared constitution.

## Expected outcome

The wiki-query interface block's trigger section uses imperative "before [moment], run `wiki-query [exact question]`" phrasing throughout. Every trigger names a concrete situation and an exact query string. No permissive language appears anywhere in the block.

## Pass criteria

- At least 2 prescriptive triggers present (imperative + exact query string pair)
- Zero permissive phrases ("if you need", "consult if needed", "you may want to", "consider consulting", "as needed")
- No per-agent symptom→query diagnostic table rows in the block
- Every trigger has both: (a) a named moment and (b) an exact wiki-query invocation string

## Fail criteria

- Triggers use permissive phrasing ("consult the KB if needed", "if you need domain knowledge")
- Triggers omit the exact query string (just say "run wiki-query" without the question)
- Block contains per-agent symptom→query routing entries (a table keyed on agent role or symptom type)
- Zero triggers present
