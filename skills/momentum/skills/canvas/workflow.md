# canvas Workflow

Launch the Momentum Cycle live dashboard. If the Hono+Bun server is already
listening on port 3456, skip the start step and open the browser directly.

---

## Step 1 — Locate the server entry point

Resolve the server path relative to the project root:

```
SERVER_FILE="skills/momentum/skills/canvas/server.tsx"
```

Verify the file exists:

```bash
test -f "$SERVER_FILE" && echo "ok" || echo "missing"
```

If missing, output:

```
Dashboard server not found at skills/momentum/skills/canvas/server.tsx
Run: bun install hono    (first-time setup)
Expected server entry: skills/momentum/skills/canvas/server.tsx
```

Then stop.

---

## Step 2 — Check if port 3456 is already listening

```bash
lsof -iTCP:3456 -sTCP:LISTEN 2>/dev/null | grep -q LISTEN && echo "running" || echo "stopped"
```

Store result as `PORT_STATUS`.

---

## Step 3 — Start server if not running

**Only run this step when `PORT_STATUS` == "stopped".**

Identify the cmux services pane:

```bash
cmux list-panes 2>/dev/null
```

Find the surface ref for the "services" tab (bottom-left pane). If multiple
surfaces exist, pick the one labelled "services". Store as `SERVICES_SURFACE`.

If cmux is unavailable or no services pane exists, fall back to starting the
server in the background:

```bash
bun --hot skills/momentum/skills/canvas/server.tsx &
```

Otherwise, launch via respawn-pane so the developer can see it:

```bash
cmux respawn-pane --surface "$SERVICES_SURFACE" \
  --command "bun --hot skills/momentum/skills/canvas/server.tsx"
```

Wait up to 10 seconds for the port to become available:

```bash
for i in $(seq 1 10); do
  lsof -iTCP:3456 -sTCP:LISTEN 2>/dev/null | grep -q LISTEN && break
  sleep 1
done
```

If still not up after 10 seconds:

```
Dashboard server failed to start on port 3456.
Check the services pane for error output.
```

Then stop.

---

## Step 4 — Open dashboard in viewer pane

Find the existing viewer pane surface ref:

```bash
VIEWER=$(cmux list-panes 2>/dev/null | grep -i "viewer\|browser" | grep -o "surface:[0-9]*" | head -1)
```

Open `http://localhost:3456` in the viewer pane using cmux. If `VIEWER` is found, open into that surface; otherwise open without a surface flag (cmux will create a new browser surface):

```bash
# If VIEWER is set:
cmux browser open --surface "$VIEWER" "http://localhost:3456"

# If VIEWER is empty (fallback):
cmux browser open "http://localhost:3456"
```

If cmux is unavailable:

```
Dashboard running at: http://localhost:3456
Open it manually in your browser.
```

---

## Step 5 — Output status

Print a one-line status:

```
Momentum Cycle dashboard → http://localhost:3456  [started|already running]
```

Use "started" if the server was launched in Step 3, "already running" if
`PORT_STATUS` was already "running".
