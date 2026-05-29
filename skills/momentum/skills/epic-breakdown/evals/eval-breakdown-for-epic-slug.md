# Eval: Breakdown for an Epic Slug

Given an `epic_slug` argument (e.g., "impetus-core") that exists as a key in `_bmad-output/planning-artifacts/epics.json`, the skill should:

1. Load the target epic's context from epics.json — `acceptance_conditions`, `value_analysis`, `system_context`, and `stories` array
2. Spawn exactly 2 gap-analysis agents (Agent A: acceptance-first; Agent B: value-gap-first) in a single message
3. Synthesize and deduplicate their findings into a structured gap list with IDs, titles, descriptions, sources, and suggested classes
4. Present the gap list to the developer at the review gate before delegating to triage
5. If the epic_slug is not found in epics.json, halt with a clear error listing available slugs and instructing the developer to run `/momentum:epic-grooming` to add missing epics
