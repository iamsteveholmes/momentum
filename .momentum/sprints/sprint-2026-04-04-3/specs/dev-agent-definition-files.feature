Feature: Dev Agent Definition Files — Lightweight Agent for Sprint-Dev Spawning

  Background:
    Given a sprint with unblocked stories ready for implementation
    And the sprint-dev workflow is executing Phase 2

  Scenario: Dev agent accepts a story and sprint context and proceeds without requesting input
    Given a story file path and sprint slug are provided to the dev agent
    When the dev agent is launched for that story
    Then it proceeds to implement the story without asking for additional information
    And implementation begins without any prompts or clarification requests

  Scenario: Dev agent produces committed changes and structured completion output
    Given the dev agent has been launched with a story file path and sprint context
    When implementation completes
    Then the story changes are committed to the working branch
    And the agent returns output containing status, files changed, story key, and test results
    And the output format is compatible with what sprint-dev Phase 3 expects

  Scenario: Dev agent produces no worktree artifacts and handles no merge operations
    Given the dev agent has finished implementing a story
    When it returns completion output
    Then no worktree creation or teardown has occurred
    And no merge proposal or user confirmation was presented during implementation

  Scenario: Sprint-dev Phase 2 launches a dev agent per unblocked story and receives completion output
    Given Phase 2 of sprint-dev is processing an unblocked story
    When sprint-dev runs Phase 2 for that story
    Then an agent runs and produces a completion report for the story
    And the report contains status, files changed, and test results
    And sprint-dev Phase 3 receives the report and continues without manual intervention

  Scenario: Direct invocation of momentum:dev skill continues to work
    Given a developer invokes the momentum:dev skill directly
    When the skill is executed
    Then it completes its full workflow without errors
    And no behavior change is observed compared to before this story
