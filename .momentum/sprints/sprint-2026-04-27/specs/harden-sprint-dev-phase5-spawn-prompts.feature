Feature: Harden sprint-dev Phase 5 spawn prompts (systemic)

  Background:
    Given a sprint contains stories with HTTP or SSE acceptance criteria

  Scenario: E2E Validator runs live tests on HTTP scenarios when services are running
    Given the project's live services are up and reachable
    And the developer runs sprint-dev Phase 5 against the sprint
    When the E2E Validator evaluates an HTTP or SSE scenario
    Then the validator exercises the scenario against the live service
    And the scenario verdict reflects the observed runtime behavior
    And no HTTP or SSE scenario is recorded as MANUAL

  Scenario: E2E Validator starts services rather than skipping when they are not yet running
    Given the project's live services are not currently running
    And the project provides an environment startup procedure
    When the developer runs sprint-dev Phase 5 against the sprint
    Then the E2E Validator brings up the required services before evaluating scenarios
    And HTTP and SSE scenarios are exercised against the running services
    And no HTTP or SSE scenario is recorded as MANUAL

  Scenario: E2E Validator reports BLOCKED when required services genuinely cannot be started
    Given the project has no environment startup procedure available
    When the developer runs sprint-dev Phase 5 against the sprint
    Then the E2E Validator reports the affected scenarios as BLOCKED
    And no scenario depending on missing infrastructure is recorded as MANUAL

  Scenario: E2E Validator reserves MANUAL for scenarios that require a human to observe a visual UI
    Given the sprint contains a scenario that can only be confirmed by a human watching a visual UI
    When the developer runs sprint-dev Phase 5 against the sprint
    Then the E2E Validator records that scenario as MANUAL
    And every other scenario is recorded as VERIFIED, FAILED, or BLOCKED based on live execution

  Scenario: QA Reviewer executes the test suite against live services rather than inspecting source files
    Given the project's live services can be started
    When the developer runs sprint-dev Phase 5 against the sprint
    Then the QA Reviewer runs the test suite against the running services
    And each acceptance criterion is verified against actual test execution evidence
    And no acceptance criterion is recorded as MISSING based solely on source-file inspection

  Scenario: QA Reviewer reports BLOCKED when execution itself cannot be attempted
    Given the project has no way to start the services the tests depend on
    When the developer runs sprint-dev Phase 5 against the sprint
    Then the QA Reviewer reports the affected acceptance criteria as BLOCKED
    And no acceptance criterion is recorded as MISSING because execution was prevented
