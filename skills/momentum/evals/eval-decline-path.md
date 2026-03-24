# Eval: Decline Path — Developer Chooses [N]

## Scenario

Given neither `~/.claude/momentum/global-installed.json` nor `.claude/momentum/installed.json` exists, when the developer invokes `/momentum` and the pre-consent summary is displayed, and the developer responds with [N] (no):

The skill should:
1. NOT write any files (no rules, no hooks config, no state files)
2. Acknowledge the developer's choice without judgment
3. Explain that setup is needed for full enforcement functionality
4. Offer to run setup again later (developer can invoke `/momentum` again any time)
5. Proceed to session orientation in a degraded state

## Expected Behavior

After [N], zero files are written. The skill informs the developer that enforcement hooks and rules won't be active until setup runs, but continues the conversation normally (proceeds to orientation).

Because state files are NOT written, the next `/momentum` invocation will offer setup again.

## NOT Expected

- Writing any config files after [N]
- Writing state files (would suppress future setup prompts)
- Refusing to continue the session after decline
- Showing error messages or warnings beyond a simple explanation
