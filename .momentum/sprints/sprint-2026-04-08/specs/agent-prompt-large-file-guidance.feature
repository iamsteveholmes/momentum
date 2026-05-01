Feature: Agent Prompt Large-File Guidance — Standard Instructions for Context-Exceeding Files

  Background:
    Given the Momentum sprint-dev workflow is installed
    And agent definitions exist in skills/momentum/agents/

  Scenario: Agent reads a large file without triggering a token-limit error
    Given an agent is spawned to implement or review a story
    And the story context references a file too large to read in a single operation
    When the agent processes the file
    Then the agent reads only the relevant portion and completes the task
    And no file-too-large error appears in the output

  Scenario: Agent locates a specific section without reading the entire file
    Given an agent needs a specific section from a large project file
    When the agent locates the relevant content
    Then the task completes successfully with the correct section content
    And the operation uses fewer reads than a full-file approach would require

  Scenario: Agent recovers from a token-limit error without repeating the failure
    Given an agent encounters a file-too-large error mid-task
    When the agent recovers from the error
    Then the agent produces correct output for the task
    And the same error does not recur for the same file

  Scenario: Agent development guide documents large-file handling as a standard convention
    Given a developer is authoring a new agent definition
    When the developer consults the agent-skill-development-guide
    Then the guide includes a large-file handling section describing the chunked-read pattern
    And the guide identifies which project files commonly exceed the single-read limit
