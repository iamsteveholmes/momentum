# Eval: Silent Pre-Flight — Zero Output Before Menu

**Story:** 2a.1 — Silent Pre-Flight and Deferred Stats Write
**AC:** AC1, AC2

## Scenario

Momentum is fully installed. All component groups are at current version. global-installed.json and installed.json both report the current version for all groups. Hash checks pass (no drift). No journal open threads.

**Given** all components are current and no actionable condition exists
**When** Impetus runs (developer invokes `/momentum`)
**Then** zero lines of output appear before the progress bar / session menu

## Context to Load

Load `skills/momentum/workflow.md` as the implementation under test.

Simulate the following state:
- `installed.json` has all component versions == current_version
- `global-installed.json` has all component hashes matching stored hashes
- `journal.jsonl` does not exist

## Expected Behavior

1. Step 1 produces **zero output** — it reads files, checks versions, and dispatches to Step 10 silently
2. Step 10 produces **zero output** — hash check passes, dispatches to Step 7 silently
3. Step 7 produces the session menu — this is the **first visible output**

The developer should see ONLY the session menu:
```
Everything's in place — let's build something.

Here's what I can help with:

  1. Create a story
  2. Develop a story
  3. Review a plan
  4. Run quality validation
  5. Audit spec provenance
  6. Show session threads

What would you like to work on?
```

## Failure Conditions

- ANY output before the session menu = FAIL
- "Checking version...", "Running hash verification...", "All checks passed..." = FAIL
- "Proceeding to step 7", "GOTO step 10", or any step number narration = FAIL
- "Step 1 of N" or any step count = FAIL

## Pass Condition

The ONLY output in the session start sequence is the session menu from Step 7.
