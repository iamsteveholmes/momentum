Feature: UX Base Body — Universal Agent Role Contract for UX Designer

  Background:
    Given the Momentum plugin is installed and the UX agent is available for spawning

  Scenario: UX agent produces a structured deliverable scoped to the given story
    Given a story spec file describing a UX design task
    When the developer spawns the UX agent with that story file
    Then the agent emits a UX_OUTPUT_START / UX_OUTPUT_END block containing a Scope, Verdict, Artifacts, and Open Questions section
    And at least one UX artifact file is listed in the output

  Scenario: UX agent stays within UX artifact scope and does not touch non-UX files
    Given a story spec file that touches both UX and non-UX concerns
    When the developer spawns the UX agent with that story file
    Then any files committed by the agent are UX specification, wireframe, or design document files
    And the agent does not modify story index files, sprint records, or architecture documents

  Scenario: UX agent handles a story with ambiguous requirements without fabricating design decisions
    Given a story spec file with underspecified UX requirements
    When the developer spawns the UX agent with that story file
    Then the Open Questions section of the output lists the unresolved design decisions
    And the Verdict is not marked complete when open questions remain unanswered
