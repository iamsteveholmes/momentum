# Eval: Empty Journal Skip

## Scenario

Given NO file exists at `.claude/momentum/journal.jsonl` (or the file exists but contains zero entries), when the developer invokes `/momentum` and startup routing reaches session orientation (installed.json exists, version matches):

## Expected Behavior

1. Impetus checks for `.claude/momentum/journal.jsonl`
2. Finds it absent or empty
3. Skips the Session Journal display entirely — no numbered thread list appears
4. Transitions directly to the Story 2.1 normal session menu (practice overview, "What are you working on?")

## NOT Expected

- Any mention of "Session Journal" or "threads" or "no threads found"
- An error message about missing journal file
- Prompting the developer to create a journal
- A blank journal section or placeholder
