# Plan Audit Gate

Before calling `ExitPlanMode`, always check whether the active plan file contains a `## Spec Impact` section.

- Find the active plan: most recently modified `.md` in `~/.claude/plans/`
- If `## Spec Impact` is present: proceed to `ExitPlanMode`
- If `## Spec Impact` is absent: invoke `momentum:plan-audit` first, wait for it to complete and write the section, then call `ExitPlanMode`

Do not call `ExitPlanMode` until `## Spec Impact` is present in the active plan file.
