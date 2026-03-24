# Eval: Progress Indicator at First Step

## Scenario

Given a developer has just invoked `/momentum` and entered the BMAD workflow, and they are at the very first phase (Brief) with no completed phases, when Impetus displays the progress indicator, it should show only 2 lines.

## Expected Behavior

The response includes a progress indicator with exactly 2 lines:

```
  →  Brief                                         capturing the core product idea
  ◦  Research · PRD · UX · Arch · Epics · Stories  6 phases ahead
```

Specifically:
- The ✓ completed line is absent — there are no completed phases to show
- Line 1 uses → symbol with the current step and a narrative description
- Line 2 uses ◦ symbol with all upcoming phases collapsed to one line
- Every symbol has adjacent text conveying the same meaning
- No numeric step counts appear anywhere
- The indicator is exactly 2 lines, not 3

## NOT Expected

- A ✓ line (nothing is completed yet)
- 3 lines in the indicator
- An empty ✓ line or a ✓ line with placeholder text like "nothing yet"
- "Step 1/7" or any numeric position format
- A symbol without adjacent descriptive text
