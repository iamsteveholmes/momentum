# Eval: Silent Pre-Flight — Zero Output Before Menu

Story: 2a.1 — Silent Pre-Flight and Deferred Stats Write
AC: AC1, AC2

Note: AC1 references "the progress bar" as the first visible output — that artifact is Story 2a.2's deliverable. For 2a.1 validation, the session menu is the first visible output. Once 2a.2 is implemented, the progress bar will precede the menu and this eval's pass condition still holds (zero output before the first visible element).

## Scenario

Momentum is fully installed. All component groups are at current version. global-installed.json and installed.json both report the current version for all groups. Hash checks pass (no drift). No journal open threads.

**Given** all components are current and no actionable condition exists
**When** Impetus runs (developer invokes `/momentum`)
**Then** zero lines of output appear before the session menu

## Context to Load

Load `skills/momentum/skills/impetus/SKILL.md` as the implementation under test (happy path startup is inline in SKILL.md; workflow.md is only loaded for non-happy paths).

Simulate the following state:
- `installed.json` has all component versions == current_version
- `global-installed.json` exists and all stored hashes match (no drift)
- `journal.jsonl` does not exist
- `startup-preflight` returns `route: "greeting"`, `has_open_threads: false`

## Expected Behavior

1. `startup-preflight` runs silently (1 Bash call, zero output)
2. SKILL.md routes to the inline greeting path — this produces the **first visible output** (session menu)

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
