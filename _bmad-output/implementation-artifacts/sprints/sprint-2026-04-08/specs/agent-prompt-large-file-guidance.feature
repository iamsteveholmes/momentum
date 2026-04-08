Feature: Agent Prompt Large-File Guidance — Standard Instructions for Context-Exceeding Files

  Background:
    Given the Momentum sprint-dev workflow is installed
    And agent definitions exist in skills/momentum/agents/

  Scenario: Agent reads a large file using chunked offset rather than failing
    Given a sprint-dev agent is spawned to implement or review a story
    And the story context references a file known to exceed the Read tool's token limit
    When the agent attempts to read the file
    Then the agent uses offset and limit parameters to read the file in targeted chunks
    And the agent does not emit a file-too-large error

  Scenario: Agent searches before reading when only a specific section is needed
    Given a sprint-dev agent is spawned to implement or review a story
    And the agent needs a specific section from architecture.md, prd.md, or epics.md
    When the agent locates the relevant content
    Then the agent uses Grep to find the section heading and its line number
    And the agent reads only the lines surrounding that result using offset and limit

  Scenario: Agent recovers from a token-limit error without retrying the same read
    Given a sprint-dev agent is spawned and encounters a file-too-large error mid-task
    When the agent handles the error
    Then the agent switches to a Grep-then-targeted-Read strategy
    And the agent does not retry the same full-file read that triggered the error

  Scenario: Agent development guide documents large-file handling as a standard convention
    Given a developer is authoring a new agent definition
    When the developer consults the agent-skill-development-guide
    Then the guide includes a large-file handling section describing the offset/limit pattern
    And the guide identifies which project files commonly exceed the token limit
