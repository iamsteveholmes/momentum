Feature: Specialist Dev Agents — Domain-Specific Agent Definitions

  Background:
    Given a sprint is being planned with stories that have a touches array
    And the base dev agent definition exists

  Scenario: Sprint planning classifies a story to a domain specialist by path patterns
    Given a story whose touches paths match a known domain pattern
    When sprint planning Step 5 runs domain classification
    Then the story is assigned the matching specialist type
    And the specialist assignment is stored in the team composition output

  Scenario: Most-specific pattern wins when multiple specialists match
    Given a story whose touches paths match more than one specialist pattern
    When sprint planning classifies the domain
    Then the specialist with the most matching paths is assigned
    And ties resolve to the most specific pattern in table order

  Scenario: Stories with no matching paths fall back to the base dev agent
    Given a story whose touches paths match no specialist pattern
    When sprint planning classifies the domain
    Then the story is assigned the base dev agent
    And no warning or error is produced

  Scenario: Each specialist agent definition carries domain-specific expertise
    Given a specialist agent definition file exists for a domain
    When its content is inspected
    Then it contains a focused domain expertise section relevant to that domain
    And it does not contain full workflow orchestration logic

  Scenario: Each specialist agent definition follows the established agent schema
    Given any specialist agent definition file
    When its frontmatter is inspected
    Then it has name, description, model, effort, and tools fields
    And its body is a focused system prompt rather than a step-by-step workflow

  Scenario: Sprint-dev spawns the correct specialist agent for a story
    Given a story in the sprint record has a specialist assignment
    When Phase 2 of sprint-dev launches an agent for that story
    Then it spawns the agent definition file matching the assigned specialist
    And it passes the same guidelines it would pass to the base dev agent

  Scenario: Sprint-dev falls back gracefully when a specialist file is missing
    Given a story's sprint record references a specialist that has no definition file
    When Phase 2 of sprint-dev attempts to spawn the agent
    Then it logs a warning about the missing specialist
    And it falls back to spawning the base dev agent instead

  Scenario: Specialist assignment is persisted in the sprint record
    Given sprint planning has completed domain classification
    When the sprint record is written
    Then each story entry contains a specialist field with the assigned specialist name
    And stories assigned to the base dev agent record that assignment explicitly

  Scenario: Specialist agents accept project guidelines that override built-in defaults
    Given a specialist agent is spawned with project guidelines provided
    When the agent performs implementation
    Then it applies the project guidelines in preference to its built-in domain defaults
