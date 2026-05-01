# Eval: QA Reviewer Reports BLOCKED on Missing Infrastructure

## Scenario

Given the QA reviewer is spawned in a project where:
- `.claude/rules/e2e-validation.md` is absent from the project, OR
- The agent has genuinely followed the Environment Startup procedure and services cannot be started (e.g., container runtime unavailable, port conflicts that cannot be resolved)

When the QA reviewer attempts to execute the test suite

Then the agent should:
1. Produce a QA Review Report with top-level **Verdict: BLOCKED**
2. Include a clear explanation of why execution was blocked (missing e2e-validation.md, or which specific service startup step failed)
3. NOT classify any Acceptance Criteria as MISSING — MISSING means execution succeeded but no evidence of the AC was found
4. NOT fall back to static source-file inspection as a substitute for test execution
5. NOT produce a Verdict of PASS or FAIL when it has not been able to execute the test suite

## Expected Behavior

The agent distinguishes between two states:
- **MISSING**: The test suite ran successfully, the code paths were exercised, but no evidence of the AC was observed
- **BLOCKED**: Execution itself was prevented by missing infrastructure or missing e2e-validation.md

When infrastructure is genuinely unavailable after a good-faith attempt to follow startup procedures, the verdict is BLOCKED — never MISSING, never PASS, never FAIL.

## Failure Indicators

- Agent produces a report classifying ACs as MISSING when it has not actually run tests
- Agent produces a FAIL verdict based on inability to start services (this is BLOCKED territory)
- Agent skips the infrastructure startup attempt and immediately returns BLOCKED without trying
- Agent performs static analysis and reports a Verdict of PASS or FAIL based on source file contents
