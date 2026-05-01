---
eval: staleness-tolerant-of-missing-cache
description: Plugin cache directory does not exist — Impetus does not surface a warning and does not crash. Orientation proceeds normally.
---

# Eval: Tolerant of Missing Cache Directory

## Given

The developer invokes `/momentum:impetus`. The plugin cache directory
`~/.claude/plugins/cache/momentum/momentum/` does not exist on their machine (e.g., they are
running from source without a marketplace install). Impetus invokes
`python3 .../scripts/momentum-tools.py session plugin-cache-check` and receives this JSON:

```json
{
  "cache_version": null,
  "source_version": "0.17.4",
  "active_cache_dir": null,
  "status": "no-cache"
}
```

## Expected Behavior

Impetus treats `status: "no-cache"` as a silent pass. The output should:

1. Contain NO mention of plugin cache versions
2. Contain NO staleness warning
3. Contain NO error or crash output related to the check
4. Proceed to the normal orientation output (First Breath or Rebirth path as applicable)

## What Is NOT Acceptable

- A false-positive staleness warning when there is nothing to compare against
- An error surfaced to the developer about the missing cache directory
- A crash or exception propagating to the developer
- Any friction introduced by the absent cache
