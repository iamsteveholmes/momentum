Feature: Review Orchestration Codification — Automate AVFL + Code Review Flow

  Background:
    Given a sprint execution with multiple stories that have completed development

  Scenario: AVFL findings are presented before any fix agents are spawned
    When the orchestrator begins the AVFL review phase
    Then AVFL findings are presented to the developer as a report
    And no fix agents are spawned until the developer acknowledges the findings

  Scenario: Each story receives an independent code review after AVFL
    Given the developer has acknowledged the AVFL findings
    When the orchestrator begins the per-story code review phase
    Then a code review is invoked for each completed story independently
    And each review is scoped to that story's changeset

  Scenario: AVFL and code review findings are merged into a single fix queue
    Given AVFL has produced findings for two stories
    And code review has produced findings for one of those stories
    When the orchestrator builds the consolidated fix queue
    Then findings from both sources appear in a single prioritized queue
    And the developer is asked to confirm which items to fix and which to defer

  Scenario: Fix agents are spawned only after the developer confirms the fix queue
    Given the consolidated fix queue has been presented to the developer
    When the developer has not yet confirmed the queue
    Then no fix agents are spawned
    When the developer confirms items to fix
    Then fix agents are spawned only for the confirmed items

  Scenario: Only affected reviewers re-run after fixes are applied
    Given fix agents have completed changes addressing AVFL findings
    And no code review findings were fixed in this pass
    When the orchestrator triggers selective re-review
    Then only the AVFL reviewer re-runs on the changed files
    And the code reviewer is not re-invoked

  Scenario: Substantial fixes trigger a lightweight AVFL re-scan
    Given fix agents have applied substantial changes to the codebase
    When the fix pass completes
    Then a lightweight AVFL re-scan is triggered automatically
    And any new findings enter the fix queue for developer review

  Scenario: Developer only makes acknowledge-confirm-accept decisions
    When the orchestrator drives the full review-fix cycle
    Then the developer is prompted to acknowledge AVFL findings
    And the developer is prompted to confirm which items to fix
    And the developer is prompted to accept the final state
    And no other manual orchestration of review sequence is required
