# Eval: Repeat Invocation Gets Abbreviated Orientation

## Scenario

**Given** an `installed.json` file containing:
```json
{
  "installed_at": "2026-03-20T10:00:00Z",
  "components": { "hooks": { "version": "1.0.0" } },
  "session_stats": {
    "momentum_completions": 3,
    "first_invocation": "2026-03-20T10:00:00Z",
    "last_invocation": "2026-03-23T14:00:00Z"
  }
}
```

**When** Impetus reaches Step 7 (session orientation) and reads `session_stats.momentum_completions`,

**Then** Impetus should:
1. Detect `momentum_completions >= 1` (value is 3) and treat this as a repeat encounter
2. Deliver abbreviated orientation — current state and decision points only, without full explanatory walkthrough
3. Optionally ask once: "Full walkthrough or just the decision points?"
4. After the expertise-adaptive check, increment `momentum_completions` to 4, update `last_invocation`, and write `installed.json`

## What to Observe

- Orientation does NOT include the full "what the workflow does, what each phase covers" walkthrough.
- Orientation IS concise: current state summary + decision points or menu.
- The `session_stats.momentum_completions` counter is incremented before the menu/journal display.
- If `session_stats` were absent, it would be initialized with `momentum_completions: 1`.
