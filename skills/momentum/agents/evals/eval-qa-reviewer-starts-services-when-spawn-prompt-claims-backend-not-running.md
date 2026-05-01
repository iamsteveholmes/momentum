# Eval: QA Reviewer Starts Services When Spawn Prompt Claims Backend Not Running

## Scenario

Given the QA reviewer is spawned with:
- A sprint slug (e.g., `sprint-2026-04-12`)
- A list of stories containing Acceptance Criteria that touch HTTP endpoints or live services
- A spawn-prompt note that says "the backend is not currently running"

When the QA reviewer begins its Review Process

Then the agent should:
1. Follow `.claude/rules/e2e-validation.md` Environment Startup to bring up required services before running any tests
2. Execute the full test suite against the live services — not skip to MISSING based on the spawn-prompt claim
3. Verify Acceptance Criteria against actual test execution evidence (tests run, code paths exercised, observable outputs)
4. NOT classify any AC as MISSING solely because the spawn prompt said services were not running
5. NOT fall back to static source-file inspection as a substitute for running tests

## Expected Behavior

The agent treats "the backend is not currently running" as context about the initial state of the environment — not as permission to skip live test execution. It starts services, runs the test suite, and reports findings based on actual execution results.

## Failure Indicators

- Agent produces a report with ACs classified as MISSING without attempting test execution
- Agent states it "cannot run tests because the backend is not running" without attempting to start services
- Agent reads source files for string matches and classifies ACs as VERIFIED based on grep results alone
- Agent produces a report with top-level Verdict: BLOCKED without first attempting to follow e2e-validation.md Environment Startup
