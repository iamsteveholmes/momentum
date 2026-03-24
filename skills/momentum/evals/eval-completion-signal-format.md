# Eval: Completion Signal Format

## Scenario

Given a story cycle, workflow, or major workflow step completes, when Impetus delivers a completion signal, it must contain all three required components:

1. **Explicit ownership return** — a phrase making clear the developer now owns the output (e.g., "This is yours to review and adjust")
2. **File list with paths** — every file produced or modified, with its path, each on its own line with `·` prefix
3. **"What's next?" prompt** — an explicit forward-looking question returning control to the developer

The signal must follow the canonical format:
```
✓  [what completed] — [one-line summary]

What was produced:
  · path/to/file1.ext — brief description
  · path/to/file2.ext — brief description

This is yours to review and adjust. What's next?
```

## Expected Behavior

- All three components present in every completion signal
- The developer is never left uncertain whether Impetus is still working or waiting for input
- File paths are real paths relative to project root, not placeholders
- No generic praise ("Great work!", "Excellent!")
- No step-count format ("Step 5/8 complete")
- Progress indicator transitions correctly: `✓ Built: [all steps]` with no `◦ Next:` line at final completion

## NOT Expected

- Omitting any of the three required components
- Using "Step N/M complete" instead of narrative completion
- Generic praise in the completion signal
- Leaving the developer uncertain about whether Impetus is done or still working
- File list with placeholder paths instead of real paths
- Completion signal without a forward-looking question
