---
description: General cmux usage rules for all agents — pane management, browser automation, markdown viewing, and tested command reference.
---

# cmux Usage

cmux manages terminal panes, browser surfaces, and markdown viewers in a visual multiplexer. Use it to stand up services, open documentation, and automate browser interactions — all in visible panes the developer can watch.

## Query State First

Before creating or modifying panes, always query current state:

```bash
cmux identify          # your workspace/surface context
cmux list-panels       # all surfaces in current workspace
cmux list-workspaces   # all workspaces
```

## Terminal Panes

```bash
# Create panes
cmux new-split right                             # right-side pane (returns "OK surface:N workspace:N")
cmux new-split down                              # below current pane
cmux new-split down --surface surface:N          # split a specific pane

# Interact
cmux send --surface surface:N "command here"     # send command to pane
cmux capture-pane --surface surface:N            # read full pane output
cmux capture-pane --surface surface:N --lines 5  # last N lines only
cmux rename-tab --surface surface:N "Label"      # label the pane for developer visibility

# Close
cmux close-surface --surface surface:N           # close a specific pane
```

## Browser Surfaces

```bash
cmux browser open "https://example.com"          # open browser pane (returns surface ref)
cmux browser open --surface surface:N "url"      # navigate existing browser
cmux browser navigate "url"                      # navigate current browser
cmux browser snapshot                            # capture DOM snapshot
cmux browser screenshot --out /tmp/shot.png      # visual screenshot
cmux browser wait --text "Ready"                 # wait for text to appear
cmux browser click "selector"                    # click an element
cmux browser type "selector" "text"              # type into input
cmux browser eval "document.title"               # run JS
```

## Markdown Viewer

```bash
cmux markdown open /path/to/file.md              # formatted viewer with live reload
```

Returns `surface=surface:N pane=pane:N`. The viewer auto-refreshes when the file changes on disk.

## Launching Long-Running Processes

**Use `respawn-pane` for services and GUI apps** — NOT `send`. `send` has timing/concatenation issues when the shell isn't fully ready.

```bash
# CORRECT — respawn-pane replaces the shell with the command directly
cmux new-split right                              # create the pane
cmux rename-tab --surface surface:N "Label"       # label it BEFORE respawn (respawn kills the shell)
cmux respawn-pane --surface surface:N --command "/full/path/to/binary args"

# WRONG — send can concatenate with prior output or race the shell prompt
cmux send --surface surface:N "long-running-command"
```

`respawn-pane` kills the shell and runs the command as the pane's process. When the process exits, the pane shows its exit status. For GUI apps (emulator, desktop app) the pane may show "closed unexpectedly" — this is normal, the GUI runs as a separate macOS window.

**Chaining commands with respawn-pane:** Use `&&` to run multiple commands sequentially:
```bash
cmux respawn-pane --surface surface:N --command "cd /path && command1 && command2"
```

**Use `send` only for short interactive commands** where the shell is already at a prompt and you need the shell to interpret the command (env vars, pipes, etc.).

### send Timing Rules (when you must use send)

1. **Always wait for the shell prompt before sending.** Poll with `capture-pane` until you see the prompt character.
2. **Never send two commands in rapid succession.** They will concatenate into one line.
3. **Use absolute paths.** `$ANDROID_HOME` and other env vars may not be set in cmux shells.
4. **Keep commands short.** Narrow panes cause line wrapping that breaks command parsing.

```bash
# Wait for prompt before send
for i in $(seq 1 10); do
  OUTPUT=$(cmux capture-pane --surface $SURFACE --lines 3 2>&1)
  if echo "$OUTPUT" | grep -q "❯\|\\$"; then break; fi
  sleep 1
done
cmux send --surface $SURFACE "short command here"
```

## Gotchas (tested, verified)

- `close-panel` does NOT exist — use `close-surface`
- `new-split` takes direction as POSITIONAL arg: `cmux new-split right` not `--direction right`
- Parse surface refs from output: `OK surface:48 workspace:2` — extract `surface:48`
- Always `rename-tab` after creating a pane so the developer can identify it
- `capture-pane` is tmux-compat; `read-screen` also works
- Surface refs are workspace-scoped — store and reuse them within a session
- **GUI apps (emulator, desktop app) open their own macOS windows** — the cmux pane hosts the process but the GUI is a separate window
- **`send-key` uses `ctrl+c` syntax** — NOT `C-c`

## Service Readiness Polling

```bash
for i in $(seq 1 15); do
  OUTPUT=$(cmux capture-pane --surface $SURFACE --lines 5 2>&1)
  if echo "$OUTPUT" | grep -q "READY_STRING"; then
    break
  fi
  sleep 2
done
```

## Principle: Visible to the Developer

All services, logs, and outputs run in cmux panes — never in the agent's own process. The developer should be able to see every running service, every log stream, and every test execution in real time.
