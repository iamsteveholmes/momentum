---
eval: staleness-warning-on-cache-behind
description: Cache version is older than source-tree version — Impetus surfaces a warning naming both versions, the remedy, and the operator-discipline reinforcement.
---

# Eval: Staleness Warning When Cache Is Behind

## Given

The developer invokes `/momentum:impetus` in a momentum source-tree checkout. Before any orientation
output, Impetus invokes `python3 .../scripts/momentum-tools.py session plugin-cache-check` and
receives this JSON:

```json
{
  "cache_version": "0.17.0",
  "source_version": "0.18.0",
  "active_cache_dir": "~/.claude/plugins/cache/momentum/momentum/0.17.0",
  "status": "skew-cache-behind"
}
```

## Expected Behavior

Before the orientation greeting, Impetus outputs a visible warning block. The warning MUST:

1. Name both versions explicitly — cache 0.17.0 vs source 0.18.0
2. Explain in one sentence that workflows dispatched through the cache will silently run against
   stale `workflow.md` content
3. Give the remedy: run `/plugin marketplace update momentum` and start a fresh Claude Code session
4. Explicitly name the operator-discipline rule (fresh session before major workflows) as the
   primary mitigation, framing this warning as a safety net
5. Use Impetus's voice — direct, grounded, no apologies, no sycophancy

## What Is NOT Acceptable

- Warning that omits either version number
- Warning that does not mention the remedy command `/plugin marketplace update momentum`
- Warning that does not acknowledge the operator-discipline rule
- Warning that uses apologetic language ("I'm sorry to inform you…")
- Warning appearing AFTER the orientation greeting
- No warning surfaced at all
