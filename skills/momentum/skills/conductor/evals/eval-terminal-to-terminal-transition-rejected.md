# Eval: Terminal-to-terminal status transition is rejected (regression)

**Surface under test:** `momentum-tools sprint status-transition` state machine guard.

**Regression guard for:** illegal terminal-to-terminal transition defect (conduct-core retro,
critical finding). The defect caused the state machine to accept a transition from a terminal
state (e.g., `done`) to another terminal state (e.g., `closed-incomplete`) without error. The
fix (`skills/momentum/scripts/momentum-tools.py` ~L55–58, `validate_transition()`) rejects any
transition from a terminal state unless `--force` is supplied.

## Scenario

**Given:** A story whose current status is a terminal state — one of `done`, `dropped`, or
`closed-incomplete`.

**When:** `momentum-tools sprint status-transition --story {slug} --target {other-terminal}` is
invoked without `--force`.

**Then:**

1. The tool rejects the transition with a non-zero exit code.
2. The tool emits an error message containing `Cannot transition from terminal state` (or
   equivalent wording identifying the terminal-state guard).
3. The story's status in `stories/index.json` is unchanged.

## Pass Criteria

- Every combination of terminal-to-terminal attempted without `--force` exits with code 1.
- The rejection message is observable (non-empty stderr or a JSON `error` field).
- The story's on-disk status is identical before and after the rejected attempt.
- With `--force`, the transition is accepted (bypass guard confirmed).

## Fail Criteria

- A terminal-to-terminal transition is accepted without `--force` (the guard is absent or
  bypassed).
- The story's status changes after a rejected attempt.
- The tool exits 0 for an illegal terminal-to-terminal transition.

## Terminal States Under Test

All three terminal states must be covered:

| From | To (sample) | Expect |
|---|---|---|
| `done` | `closed-incomplete` | reject (exit 1) |
| `done` | `dropped` | reject (exit 1) |
| `dropped` | `done` | reject (exit 1) |
| `closed-incomplete` | `done` | reject (exit 1) |

`--force` bypass must be verified for at least one combination to confirm the guard is
gated on the flag, not removed entirely.

## Verification Method

**Direct CLI exercise against `test-momentum-tools.py`.**

The existing `test_terminal_state_blocked()` test in
`skills/momentum/scripts/test-momentum-tools.py` covers `done`, `dropped`, and
`closed-incomplete` → `backlog` (a non-terminal target). This eval extends coverage to
**terminal → terminal** specifically:

```python
# From done -> closed-incomplete (without --force)
proj = setup_project({"s": {"status": "done", ...}})
code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", "closed-incomplete")
assert code == 1   # rejected

# From done -> dropped (without --force)
proj = setup_project({"s": {"status": "done", ...}})
code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", "dropped")
assert code == 1   # rejected

# With --force: accepted
proj = setup_project({"s": {"status": "done", ...}})
code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", "closed-incomplete", "--force")
assert code == 0   # allowed with --force
```

Inspect `validate_transition()` in `momentum-tools.py` to confirm the terminal-state guard
(`if current in TERMINAL_STATES: return f"Cannot transition from terminal state..."`) is
present and covers all three terminal states.
