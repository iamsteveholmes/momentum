# Eval: Progress Indicator at Last Step

## Scenario

Given a developer has completed 6 phases (Brief, Research, PRD, UX, Architecture, Epics) and is currently on the final phase (Stories) with no upcoming phases, when Impetus displays the progress indicator, it should show only 2 lines.

## Expected Behavior

The response includes a progress indicator with exactly 2 lines:

```
  ✓  Brief · Research · PRD · UX · Arch · Epics  foundation through planned work
  →  Stories                                      breaking the work into deliverables
```

Specifically:
- The ◦ upcoming line is absent — there are no upcoming phases
- Line 1 uses ✓ symbol with all completed phases collapsed to one line and a value summary
- Line 2 uses → symbol with the current step and a narrative description
- Every symbol has adjacent text conveying the same meaning
- No numeric step counts appear anywhere
- The indicator is exactly 2 lines, not 3

## NOT Expected

- An ◦ line (nothing is upcoming)
- 3 lines in the indicator
- An empty ◦ line or an ◦ line with placeholder text like "none remaining"
- "Step 7/7" or any numeric position format
- A symbol without adjacent descriptive text
