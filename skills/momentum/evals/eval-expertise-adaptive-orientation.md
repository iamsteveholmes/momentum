# Eval: Expertise-Adaptive Orientation

## Scenario

Given a developer enters a workflow for the second or subsequent time — e.g., they ran `/momentum-dev` yesterday and are running it again today — when Impetus delivers orientation:

The skill should:
1. Detect whether this is a first encounter or repeat encounter for this developer+workflow combination (via journal thread history)
2. **First encounter:** deliver full walkthrough with context — explain what the workflow does, what each phase covers, what to expect
3. **Repeat encounter:** deliver abbreviated orientation — decision points only, skip explanatory context the developer has already seen
4. **Expert mode:** minimal cue — just the essential state and the first decision point
5. Optionally ask at workflow start: "Full walkthrough or just the decision points?" — one question, one time, not repeated within the session

## Expected Behavior

**Detection mechanism:**
- Impetus checks journal thread history for prior completions of this workflow type
- Zero prior completions → first encounter → full walkthrough
- One or more prior completions → repeat encounter → abbreviated or ask preference

**Abbreviated orientation:**
- Skips explanatory context ("This workflow implements stories by...")
- Presents current state directly ("3 stories ready for dev. Story 2.5 is next — it covers spec contextualization.")
- Moves to the first decision point faster

**Expert mode (repeat encounter, developer chooses "just the decision points"):**
- State + first decision only
- Narrative progress format maintained (no "Step N/M")
- All symbol vocabulary still applies (✓ → ◦ ! ✗ ? ·)

**The ask:**
At repeat-encounter workflow start, Impetus may ask:
```
Full walkthrough or just the decision points?
```
This is asked once at workflow start, not repeated at each step.

## NOT Expected

- Delivering full walkthrough every time regardless of history
- Using "Step N/M" framing in any orientation mode (first, abbreviated, or expert)
- Asking "Full walkthrough or just the decision points?" on first encounter (there's no abbreviated version to offer yet)
- Asking the preference question more than once per session
- Skipping orientation entirely in expert mode — minimal cue still includes current state and first decision
- Detecting expertise based on anything other than journal thread history (no guessing based on developer's language or speed)
