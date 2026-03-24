# Eval: Hygiene Checks Fire Before Selection Prompt

## Scenario

Given a developer invokes `/momentum` and the session journal contains:
- Thread 1: `last_active` = 20 minutes ago (within 30-minute concurrent threshold)
- Thread 2: `last_active` = 5 days ago (dormant, exceeds 3-day threshold)
- Thread 3: `last_active` = 2 hours ago (normal active thread)

When Impetus displays the session journal,

Then Impetus should:
1. Display all three threads in a numbered list with `context_summary_short`, phase, and elapsed time
2. Emit the concurrent-work warning for Thread 1 (! Thread "..." appears active in another tab) BEFORE any selection prompt
3. Emit the dormant closure offer for Thread 2 (N days inactive. Close this thread?) BEFORE any selection prompt
4. End the response with the selection prompt "Continue (1/2/...) or tell me what you need?"
5. All of this happens in ONE response turn — no user input is requested between the thread list display and the hygiene warnings

## What Would Fail This Eval

- Hygiene warnings appear in a separate response turn (after the user has already been prompted for input)
- The selection prompt appears before any hygiene warning
- The response pauses after displaying the thread list and asks for selection before checking hygiene conditions
- No hygiene warnings appear at all
