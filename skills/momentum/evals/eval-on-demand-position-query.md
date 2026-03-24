# Eval: On-Demand Position Query

## Scenario

Given a developer is mid-workflow (e.g., at the Architecture phase of the BMAD workflow with Brief, Research, PRD, and UX completed and Epics and Stories upcoming), and they type "where am I?" or "what's my current position?" or "show me my progress", Impetus should respond with the progress indicator showing their current position.

## Expected Behavior

1. Impetus responds with the correct progress indicator for the current workflow position:

```
  ✓  Brief · Research · PRD · UX      vision through interaction patterns done
  →  Architecture                     making implementation decisions
  ◦  Epics · Stories                  2 phases to implementation
```

2. The indicator follows all standard rules:
   - 3 lines at mid-workflow (✓/→/◦)
   - 2 lines at workflow start (→/◦ only) or workflow end (✓/→ only)
   - Every symbol has adjacent text pairing
   - No numeric step counts ("Step 5/7")
   - Uses only terminal-safe characters — no color codes, no box-drawing characters that require specific font support
   - Renders cleanly within 80-character terminal width

3. The response answers the developer's question directly — it shows position, not a re-explanation of the entire workflow

## Boundary Cases

At first step (Brief):
```
  →  Brief                                         capturing the core product idea
  ◦  Research · PRD · UX · Arch · Epics · Stories  6 phases ahead
```

At last step (Stories):
```
  ✓  Brief · Research · PRD · UX · Arch · Epics  foundation through planned work
  →  Stories                                      breaking the work into deliverables
```

## NOT Expected

- Requiring the developer to specify which workflow they mean (if only one is active)
- Responding with a paragraph description instead of the visual indicator
- "Step 5/7" or any numeric position format
- Color-dependent output or characters that require specific terminal fonts
- Output exceeding 80 characters per line (horizontal scrolling)
- A symbol without adjacent descriptive text
