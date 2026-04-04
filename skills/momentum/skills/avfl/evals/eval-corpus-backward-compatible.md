# Eval: Corpus Mode Off by Default — Single-Document Behavior Unchanged

## Scenario

AVFL is invoked WITHOUT the `corpus` parameter (omitted entirely), on a single document:

```
profile: checkpoint
output_to_validate: "/path/to/single-doc.md"
domain_expert: "technical writer"
task_context: "single research document"
stage: checkpoint
```

The document contains a minor factual error (a model version number that doesn't match
the cited source) and a structural gap (missing a Sources section that other documents
in the project have).

## Expected Behavior

The skill should:

1. Run exactly as it does today — no corpus-specific behavior
2. Pass the single document to validators using the standard prompt templates
   (`validator_system`, `validator_task`) — NOT the corpus variants
   (`validator_system_corpus`, `validator_task_corpus`)
3. Findings use plain section/line location format — NOT `{filename}:{section}` format
4. The `cross_document_consistency` and `corpus_completeness` dimensions do NOT appear
   in any findings — they are corpus-only and must not activate in single-doc mode
5. The factual error and structural gap are detected using existing dimensions
   (correctness, completeness)
6. Score and grade are computed using the standard scoring weights

## What Failure Looks Like

- Corpus prompt templates are used instead of standard templates
- `{filename}:` prefix appears in finding locations
- `cross_document_consistency` or `corpus_completeness` findings are produced
- Existing behavior is altered in any way (different finding counts, score changes,
  template changes) compared to pre-corpus-mode AVFL
