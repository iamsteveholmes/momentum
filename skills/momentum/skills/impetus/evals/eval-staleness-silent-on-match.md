---
eval: staleness-silent-on-match
description: Cache version matches source-tree version — Impetus proceeds silently with no staleness warning.
---

# Eval: Silent Pass When Versions Match

## Given

The developer invokes `/momentum:impetus` in a momentum source-tree checkout. Before any orientation
output, Impetus invokes `python3 .../scripts/momentum-tools.py session plugin-cache-check` and
receives this JSON:

```json
{
  "cache_version": "0.17.4",
  "source_version": "0.17.4",
  "active_cache_dir": "~/.claude/plugins/cache/momentum/momentum/0.17.4",
  "status": "match"
}
```

## Expected Behavior

Impetus proceeds directly to the orientation greeting with NO staleness warning surfaced. The
output should:

1. Contain NO mention of plugin cache versions
2. Contain NO mention of staleness or skew
3. Contain NO mention of `/plugin marketplace update momentum`
4. Proceed to the normal orientation output (First Breath or Rebirth path as applicable)

## What Is NOT Acceptable

- Any staleness-related text in the orientation output
- Any version comparison text surfaced to the developer
- Delay or friction caused by the staleness check
- An error or crash during the check
