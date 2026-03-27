# Eval: No Routing Narration — GOTO Transitions Are Silent

Story: 2a.1 — Silent Pre-Flight and Deferred Stats Write
AC: AC4

## Scenario

Impetus routes between steps (e.g., GOTO step 10 from Step 1, GOTO step 7 from Step 10). The routing transitions must produce zero output.

**Given** Impetus is routing between workflow steps
**When** an LLM implements the workflow
**Then** no output matching routing narration patterns appears

## Context to Load

Load `skills/momentum/workflow.md` as the implementation under test.

Test the following routing scenarios:
1. Step 1 → GOTO step 10 (fully installed, no drift)
2. Step 10 → GOTO step 7 (hash check passes)

## Forbidden Patterns

Any output containing:
- "Proceeding to step" or "proceeding to" + any word
- "GOTO" or "going to step"
- "Routing to" or "routing"
- "Checking version", "Running version check", "Version check complete"
- "Running hash verification", "Checking hashes", "Hash check passed"
- "Step N" where N is a number (e.g., "Step 7", "Step 10")
- "Step N of M" or "N/M" step counts
- Any narration of internal machinery between steps

## Expected Behavior

Between steps, Impetus produces **zero output**. The only output visible to the developer is at phase boundaries:
- First-install consent prompt (Step 2)
- Install action confirmations: `✓ <target>` (Step 3)
- Decline message (Step 6)
- Session menu (Step 7)
- Upgrade offer (Step 9)
- Hash drift warning (Step 10, only when drift detected)

## Pass Condition

No routing narration appears in any output. The transition from Step 1 → Step 10 → Step 7 is completely silent on the happy path (all current, no drift). The developer's first visible output is the session menu.
