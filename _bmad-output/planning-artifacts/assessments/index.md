---
lastEdited: '2026-04-08'
description: Registry of point-in-time assessment records that evaluate current product state against goals, identify gaps, and inform strategic decisions. Each assessment links forward to the decisions it produced.
---

# Assessment Registry

Assessments are **point-in-time snapshots** — they evaluate where the product is, what works, what's broken, and what's missing. They go stale by design. Their value is in the decisions they produce.

Assessments feed into decisions. The pipeline:

```
Research (external findings)
        ↘
         Assessment (where are we now? what's working? what's broken?)
        ↗
Codebase state
        ↘
         Decision (given the assessment, what do we do?)
                ↘
                 Stories (how do we do it?)
```

## Assessments

| ID | Title | Date | Decisions Produced | Status |
|----|-------|------|--------------------|--------|
| AES-001 | [Agent Guidelines Current State — Gen-1 vs. Gen-2 Target](aes-001-agent-guidelines-current-state-2026-04-09.md) | 2026-04-09 | DEC-001 | current |
