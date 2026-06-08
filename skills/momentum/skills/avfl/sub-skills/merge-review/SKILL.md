---
name: avfl-merge-review
description: "AVFL merge-review sub-skill — invoked by the avfl-merge-review Workflow. Do not invoke directly."
model: sonnet
effort: medium
user-invocable: false
---

# AVFL Merge Review

This sub-skill is the invocation target for the avfl-merge-review Workflow. The Workflow in `../../workflow-merge-review.md` owns orchestration; this skill carries the system prompt for the merge review execution context.

Invoked by the `avfl-merge-review` Workflow only. Not user-invocable.
