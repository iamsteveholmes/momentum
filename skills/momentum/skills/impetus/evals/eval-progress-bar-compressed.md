# Eval: Progress Bar Compressed Variant

## Scenario

Given:
- `sprint-status.yaml` exists with:
  - `epic-1: done`
  - `epic-2: done`
  - `epic-2a: in-progress`
  - `epic-3: backlog`
- `session_stats.momentum_completions: 5` (experienced user, `>= 3` threshold met)
- No open journal threads

When `/momentum` runs

Then Impetus should:
- Render the **compressed single-line** bar (not the verbose multi-line bar)
- Format: `  ✓ 2 done  ·  → Epic 2a  ·  ◦ next: Epic 3`
- No logo or preamble appears before the bar
- No blank line before the compressed bar (verbose rules don't apply)
- After the bar, continue to normal Step 7 flow (menu or journal display)

## What to Test

Behavioral: compressed format used when `momentum_completions >= 3`.
- Single-line output (not multi-line verbose format)
- Done count shown as number, not per-epic lines
- In-progress epic labels shown
- Next backlog epic labeled
- No logo, no preamble
