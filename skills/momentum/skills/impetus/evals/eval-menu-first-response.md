# Eval: Menu First Response

## Setup

Invoke `/momentum` with no prior context in a project where Momentum is fully installed (versions match, setup complete).

## Expected Behavior

Impetus immediately presents a numbered menu without waiting for user input. The response follows:
1. Orientation line (narrative, e.g., "You're set up and ready.")
2. Numbered menu of available workflows
3. Transition/prompt ("What would you like to work on?")
4. User control is the final element

## Fail Conditions

- Response contains "Step N/M" or any numeric step indicator
- Response contains "Great!", "Excellent!", "Sure!", "Of course!", or "Absolutely!"
- Response surfaces an agent name (e.g., "Claude", "Sonnet", "AVFL", "VFL")
- Impetus waits for user to speak first instead of presenting menu immediately
- User control is not the final element of the response
- Menu items are not numbered
