# Eval: Corpus Mode Activates Cross-Document Dimensions

## Scenario

Given: Two markdown files with a cross-document contradiction.

- `file-a.md` states: "The compaction threshold is 150,000 tokens."
- `file-b.md` states: "Compaction triggers at approximately 83.5% of the context window."

These are contradictory descriptions of the same mechanism. Additionally, both files
discuss context management but neither addresses the subagent context window ceiling,
which is a required topic for a complete context management corpus.

AVFL is invoked with:
```
corpus: true
profile: checkpoint
output_to_validate: [file-a.md, file-b.md]
domain_expert: "technical writer"
task_context: "two-document context management corpus"
```

## Expected Behavior

The skill should:

1. Pass both files to each validator — validators receive all corpus files, not just one
2. Produce at least one finding with `dimension: cross_document_consistency` describing
   the compaction threshold contradiction between the two files
3. Produce at least one finding with `dimension: corpus_completeness` noting that the
   subagent context ceiling topic is absent from both files
4. All findings include a `location` value in `{filename}:{section}` format
   (e.g., `file-a.md:Context Management` or `file-b.md:Compaction`)
5. The `cross_document_consistency` and `corpus_completeness` dimensions appear in
   the findings — not just generic consistency/completeness findings

## What Failure Looks Like

- Validators only process one file at a time (context isolation failure)
- Findings use plain section names without filename prefix
- No finding mentions `cross_document_consistency` or `corpus_completeness`
- Only `consistency` or `completeness` dimensions appear (single-doc dimensions)
- The contradiction is not detected
