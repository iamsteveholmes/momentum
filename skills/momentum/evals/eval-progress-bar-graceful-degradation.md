# Eval: Progress Bar Graceful Degradation

## Scenario

Given:
- `sprint-status.yaml` does **not** exist in the project (new project, no sprint planning done yet)
- `session_stats.momentum_completions: 0`
- No open journal threads

When `/momentum` runs

Then Impetus should:
- Produce **zero output** related to the progress bar
- The session menu or journal display appears as if the bar feature does not exist
- No error messages, no "file not found" text, no warnings about missing sprint-status.yaml
- Normal Step 7 flow continues unaffected (orientation + menu render normally)

## What to Test

Behavioral: silent omission when sprint-status.yaml is absent.
- No bar-related text appears in output
- No backstage machinery surfaced to the developer
- Session open proceeds normally
