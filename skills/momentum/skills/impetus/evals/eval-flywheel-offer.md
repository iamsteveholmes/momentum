# Eval: Flywheel Offer on Critical Findings

## Scenario

Given a subagent returns a critical finding (one that would be rendered with `!` severity indicator), Impetus must handle flywheel integration based on skill availability:

1. **When `momentum:upstream-fix` skill is available:** Impetus offers flywheel processing — "This looks like it could be traced upstream. Want me to run a flywheel trace?"
2. **When `momentum:upstream-fix` is NOT available:** Impetus notes the finding and logs it with "flywheel processing deferred — Epic 6"

## Expected Behavior

- Every `!`-severity finding is evaluated for flywheel processing
- When flywheel skill is installed, an explicit offer is made to trace the finding upstream
- When flywheel skill is not installed, the deferral note is included naturally in the synthesis
- The flywheel offer or deferral does not disrupt the flow of findings presentation
- Minor findings (`·` severity) do not trigger flywheel offers

## NOT Expected

- Critical findings presented with no mention of flywheel processing
- Flywheel offer made for minor/informational findings
- Raw technical language about skill availability shown to the developer
- Silent omission of flywheel integration
