---
eval_id: eval-impetus-handles-empty-signals
skill: momentum:impetus
reference: orient.md
tags: [state-migration, .momentum, signals, graceful-degradation]
---

# Eval: Impetus handles empty .momentum/signals/ gracefully

## Scenario

Given `.momentum/sprints/index.json` and `.momentum/stories/index.json` exist with valid content, and `.momentum/signals/` directory exists but contains only the `README.md` file and no JSON signal files:

When Impetus opens a session and orients:

## Expected Behavior

1. Impetus completes the orientation without error.
2. No signal-related warnings, errors, or mentions appear in the output.
3. The situational report focuses on sprint and story state only.
4. "No pending signals" is NOT narrated — silence on empty signals is the correct behavior.
5. The orientation is delivered in the normal grounded-situation-statement format.

## Anti-Patterns (Must NOT Occur)

- Any error or warning about a missing or empty `.momentum/signals/` directory.
- Any mention of "no signals found" or equivalent that would confuse the user.
- A crash or exception due to the signals directory being empty.
- Blocking orientation because signals are absent.
