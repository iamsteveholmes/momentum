# Eval: Canvas opens server when not running

## Scenario
Port 3456 is NOT listening when the developer runs `/momentum:canvas`.

## Expected Behavior
1. The skill performs a port check (lsof -i :3456 or equivalent)
2. Determines port is not in use
3. Starts the server in the cmux services pane via `cmux respawn-pane --command "bun --hot server.tsx"`
4. Opens `http://localhost:3456` in the cmux viewer pane via `cmux browser open`

## Pass Condition
The skill attempts respawn-pane AND browser open in that order.
