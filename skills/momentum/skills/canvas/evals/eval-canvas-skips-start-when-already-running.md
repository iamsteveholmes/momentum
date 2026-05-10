# Eval: Canvas skips server start when already running

## Scenario
Port 3456 IS already listening when the developer runs `/momentum:canvas`.

## Expected Behavior
1. The skill performs a port check (lsof -i :3456 or equivalent)
2. Determines port is already in use
3. Skips the respawn-pane step entirely
4. Opens `http://localhost:3456` in the cmux viewer pane via `cmux browser open`

## Pass Condition
The skill does NOT attempt respawn-pane and goes directly to browser open.
