# Story State Machine

## Valid Forward Transitions

```
backlog -> ready-for-dev -> in-progress -> review -> verify -> done
```

The ordered states are:
1. `backlog`
2. `ready-for-dev`
3. `in-progress`
4. `review`
5. `verify`
6. `done`

A forward transition moves from a lower-numbered state to the next state in sequence. Only adjacent forward transitions are legal by default.

## Terminal States

- `dropped` — reachable from any non-terminal state
- `closed-incomplete` — reachable from any non-terminal state
- `done` — the normal completion terminal state

Once a story is in a terminal state (`done`, `dropped`, `closed-incomplete`), no further transitions are allowed unless `force: true` is specified.

## Force Override

When `force: true` is provided:
- Backward transitions are allowed (e.g., `review -> in-progress`)
- Transitions from terminal states are allowed (e.g., `done -> in-progress`)
- The state machine validation is bypassed entirely

## Validation Rules

1. Target state must be a recognized state (one of the 6 ordered states or a terminal state)
2. Source state must not be terminal (unless `force: true`)
3. Transition must be to the next adjacent state, to `dropped`, or to `closed-incomplete` (unless `force: true`)
4. Story slug must exist in `stories/index.json`
