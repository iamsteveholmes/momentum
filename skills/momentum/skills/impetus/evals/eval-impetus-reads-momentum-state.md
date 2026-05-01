---
eval_id: eval-impetus-reads-momentum-state
skill: momentum:impetus
reference: orient.md
tags: [state-migration, .momentum, path]
---

# Eval: Impetus reads from .momentum/ only

## Scenario

Given `.momentum/sprints/index.json` exists with an active sprint slug `sprint-2026-04-27` and `.momentum/stories/index.json` exists with 3 in-progress stories, and the legacy `_bmad-output/implementation-artifacts/sprints/index.json` does NOT exist and the legacy `_bmad-output/implementation-artifacts/stories/index.json` does NOT exist:

When Impetus opens a session and orients:

## Expected Behavior

1. Impetus reads from `.momentum/sprints/index.json` and `.momentum/stories/index.json` successfully.
2. The situational report correctly reflects the active sprint and in-progress stories from the `.momentum/` data.
3. No error is raised about missing files.
4. No fallback to the legacy `_bmad-output/implementation-artifacts/` path is attempted.
5. The orientation is delivered silently — no narration of which files were read.
6. The situational report is grounded in the data from `.momentum/`.

## Anti-Patterns (Must NOT Occur)

- Any attempt to read `_bmad-output/implementation-artifacts/sprints/index.json` or `_bmad-output/implementation-artifacts/stories/index.json`.
- Any error message about missing state files when `.momentum/` files are present and valid.
- Narrating the file reads to the user.
- A fallback orientation that ignores or substitutes old paths.
