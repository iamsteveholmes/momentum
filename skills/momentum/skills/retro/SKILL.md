---
name: retro
description: "Sprint retrospective — transcript audit engine (dynamic Workflow), story verification, findings document, and sprint closure."
model: claude-sonnet-4-6
effort: high
---

Follow the instructions in ./workflow.md

Phase 4 (the transcript audit) runs as a single dynamic-Workflow call — the orchestrator invokes the Workflow tool once with `audit-workflow.js` (Discover → Verify → Synthesize), only after the Phase 2 zero-session guard passes. The Workflow runs in the background and returns once; it performs no human-in-the-loop, so all developer gates stay in `workflow.md`.
