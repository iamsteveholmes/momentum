# Eval: Fixer Resolves Cross-Document Contradictions via Authority Hierarchy

## Scenario A — Authority Hierarchy Provided

Two files contradict each other on a factual claim:
- `official-docs.md` states: "The 1M context window is GA since March 13, 2026."
- `draft-guide.md` states: "The 1M context window is currently in beta."

AVFL is invoked with:
```
corpus: true
profile: full
output_to_validate: [official-docs.md, draft-guide.md]
authority_hierarchy: [official-docs.md, draft-guide.md]
domain_expert: "technical writer"
task_context: "two-document corpus with a known contradiction"
```

After validation surfaces a `cross_document_consistency` finding, the fixer runs.

### Expected Fixer Behavior (Scenario A)

1. The fixer produces **two output blocks**, one per file — not a single merged document
2. Block format: `### File: {path}` followed by the corrected content for that file
3. `official-docs.md` output block is **unchanged** (it is the higher-authority source)
4. `draft-guide.md` output block **corrects the beta claim** to match official-docs.md
   (e.g., changes "currently in beta" to "GA since March 13, 2026")
5. The fix log contains an entry annotated `resolved_by: authority_hierarchy` explaining
   which file was trusted and why

## Scenario B — No Authority Hierarchy

Same two contradicting files, but AVFL is invoked WITHOUT `authority_hierarchy`:
```
corpus: true
profile: full
output_to_validate: [official-docs.md, draft-guide.md]
domain_expert: "technical writer"
task_context: "two-document corpus with a known contradiction"
```

### Expected Fixer Behavior (Scenario B)

1. The fixer does NOT guess a resolution — it does not pick one file over the other
2. The fix log contains an entry for the contradiction annotated `unresolved_contradiction`
3. The entry names both conflicting claims and both source files
4. The output blocks for both files are returned **unchanged** for this contradiction
   (the fixer may fix other non-contradictory findings normally)
5. The final score remains below 95 because the contradiction finding is not resolved

## What Failure Looks Like

- Scenario A: Single output block instead of two per-file blocks
- Scenario A: `resolved_by` annotation missing from fix log
- Scenario A: Higher-authority file is modified instead of lower-authority file
- Scenario B: Fixer guesses a resolution without `authority_hierarchy`
- Scenario B: `unresolved_contradiction` annotation absent from fix log
- Either scenario: Fixer produces narrative text instead of structured per-file blocks
