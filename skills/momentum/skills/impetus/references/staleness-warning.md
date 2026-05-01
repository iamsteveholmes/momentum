---
name: Staleness Warning Templates
code: staleness-warning
description: Warning copy templates for plugin cache staleness detection. Used when Impetus detects a version skew between the active plugin cache and the source-tree.
---

# Plugin Cache Staleness Warning Templates

These templates are rendered when `session plugin-cache-check` reports a version skew.
They are the **one explicit exception** to the "never narrate the reads" rule in `orient.md`.

Render the appropriate template **before** the orientation greeting. Do not apologize for the
warning. Do not soften it. The developer needs clear, direct information to act.

---

## Template A — Cache Behind (skew-cache-behind)

> Cache version older than source — workflows will silently run against stale content.

```
⚠ Plugin cache is behind the source tree.

Cache: {cache_version}  |  Source: {source_version}

Any workflow dispatched through /momentum:* is running against the frozen plugin cache —
not your current source tree. Edits to workflow.md files made since the last marketplace
update are invisible to the running session.

Remedy: run /plugin marketplace update momentum, then start a fresh Claude Code session.

This is the primary operator-discipline rule: update the marketplace and start a fresh
session before major Momentum workflows. This warning is the safety net for when that
discipline lapses.
```

---

## Template B — Cache Ahead (skew-cache-ahead)

> Source version older than cache — developer may be on an older branch or hasn't pulled.

```
⚠ Source tree is behind the plugin cache.

Cache: {cache_version}  |  Source: {source_version}

The installed plugin is newer than the source tree you are working in. If you are on a
feature branch or haven't pulled recently, this is expected. If not, pull the latest
source to align the trees.

Operator-discipline reminder: fresh session before major workflows is the primary
mitigation for cache drift in either direction.
```

---

## Rendering Notes

- Replace `{cache_version}` and `{source_version}` with the actual version strings from
  the `session plugin-cache-check` JSON output.
- For `status: "match"`, `"no-cache"`, `"no-source"`, or `"indeterminate"` — **render nothing**.
  Proceed silently to the orientation greeting.
- Voice: Optimus Prime conviction + KITT attentive service. Direct, grounded. No sycophancy,
  no apologies for surfacing the warning. The warning exists to protect the practice.
