Feature: PreToolUse File Protection Hooks Active

  Background:
    Given the Momentum plugin is installed with hooks active

  Scenario: Write to a protected planning artifact is blocked
    When the developer attempts to edit a file in the planning artifacts directory
    Then the write is blocked before it executes
    And a message explains the file is protected and which workflow should modify it

  Scenario: Write to a Gherkin spec file is blocked
    When the developer attempts to edit a .feature file
    Then the write is blocked before it executes
    And a message explains that Gherkin specs are modified via sprint-planning only

  Scenario: Write to the stories index is blocked
    When the developer attempts to edit stories/index.json directly
    Then the write is blocked before it executes
    And a message explains that the story index is modified via momentum-tools only

  Scenario: Write to a non-protected file proceeds silently
    When the developer edits a regular source file
    Then the write proceeds without any hook output

  Scenario: Protected paths list is configurable
    Given a new path pattern is added to the protected paths configuration
    When the developer attempts to edit a file matching the new pattern
    Then the write is blocked with the configured reason message
