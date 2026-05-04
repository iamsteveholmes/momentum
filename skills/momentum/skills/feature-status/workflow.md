# feature-status Workflow

> **This skill now delegates to `cycle-dashboard`.**
>
> The old static-HTML generation flow has been replaced by the Momentum Cycle
> live dashboard — a persistent Hono+Bun server on port 3456.

---

## Step 1 — Delegate to cycle-dashboard

Invoke the `cycle-dashboard` skill directly. It handles all steps:
port detection, server start, and opening the browser pane.

Do not run any HTML generation steps. Do not write feature-status.html.
The live dashboard is the canonical replacement.
