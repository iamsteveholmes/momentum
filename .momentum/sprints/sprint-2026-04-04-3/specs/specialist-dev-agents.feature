Feature: Specialist Dev Agents — Domain-Specific Agent Definitions

  Background:
    Given a sprint is being planned with stories that have a touches array
    And the base dev agent definition exists

  Scenario: Sprint planning classifies a story to a domain specialist by path patterns
    Given a story whose touches paths match a known domain pattern
    When sprint planning Step 5 runs
    Then the team composition output lists the matched specialist type for that story
    And the specialist assignment is visible in the planning output alongside the role

  Scenario: Most-specific pattern wins when multiple specialists match
    Given a story whose touches paths match more than one specialist pattern
    When sprint planning produces the team composition
    Then the specialist with the most matching paths is shown in the output for that story
    And when path counts tie, the first specialist in table order is selected

  Scenario: Stories with no matching paths fall back to the base dev agent
    Given a story whose touches paths match no specialist pattern
    When sprint planning produces the team composition
    Then the story shows the base dev agent in the team composition output
    And no warning or error is produced

  Scenario: Sprint-dev processes a story using its assigned specialist and the story gets implemented
    Given a story in the sprint record has a specialist assignment
    When Phase 2 of sprint-dev runs for that story
    Then an agent runs and produces a completion report for the story
    And the completion report shows domain-appropriate implementation choices
    And the same guidelines available for that story are applied during implementation

  Scenario: Sprint-dev falls back gracefully when a specialist file is missing
    Given a story's sprint record references a specialist that has no definition file
    When Phase 2 of sprint-dev attempts to launch an agent for that story
    Then a warning about the missing specialist appears in the sprint-dev output
    And an agent still runs and produces a completion report using the base dev agent

  Scenario: Specialist assignment is persisted in the sprint record
    Given sprint planning has completed domain classification
    When the sprint record is written
    Then each story entry contains a specialist field with the assigned specialist name
    And stories assigned to the base dev agent record that assignment explicitly
