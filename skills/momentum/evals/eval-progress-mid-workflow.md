# Eval: Progress Indicator at Mid-Workflow

## Scenario

Given a developer is running the Momentum BMAD workflow via Impetus and has completed 4 phases (Brief, Research, PRD, UX), is currently on Architecture, with 2 phases remaining (Epics, Stories), when a phase transition occurs (e.g., completing UX and entering Architecture), Impetus should display a 3-line progress indicator.

## Expected Behavior

The response includes a progress indicator with exactly 3 lines:

```
  ✓  Brief · Research · PRD · UX      vision through interaction patterns done
  →  Architecture                     making implementation decisions
  ◦  Epics · Stories                  2 phases to implementation
```

Specifically:
- Line 1 uses ✓ symbol with text summarizing accumulated value (not listing tasks completed)
- Line 2 uses → symbol with text describing the current step and why it matters
- Line 3 uses ◦ symbol with text describing what follows
- Completed phases collapse to a single ✓ line — never one line per completed phase
- Upcoming phases collapse to a single ◦ line — never one line per upcoming phase
- Every symbol has adjacent text conveying the same meaning (accessibility)
- No numeric step counts ("Step 5/7" or similar) appear anywhere

## NOT Expected

- "Step 5/7", "Step 3 of 8", or any numeric position format
- More than 3 lines in the indicator
- A ✓ line for each completed phase individually
- An ◦ line for each upcoming phase individually
- Any symbol without adjacent descriptive text
- Generic praise ("Great work!", "Well done!")
- "Continuing...", "Moving on to...", or ellipsis-based transitions
