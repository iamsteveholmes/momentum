Feature: Analyst Base Body — Universal Agent Role Contract for Analyst

  Background:
    Given the Momentum plugin is installed and the analyst agent is available for spawning

  Scenario: Analyst produces a structured findings report within the mandatory output envelope
    Given an analysis task naming a specific artifact and analysis question
    When the developer spawns the analyst agent with that task
    Then the agent emits an ANALYST_OUTPUT_START / ANALYST_OUTPUT_END block
    And the block contains a Findings Report with Scope, Verdict, Key Findings, and Open Questions sections
    And each finding in Key Findings includes a cited artifact reference and a confidence level

  Scenario: Analyst surfaces unknowns rather than filling gaps with inference
    Given an analysis task where the available artifacts do not fully answer the question
    When the developer spawns the analyst agent with that task
    Then the Open Questions section lists every claim the agent could not substantiate
    And the Verdict is PARTIAL or BLOCKED rather than COMPLETE
    And no finding in Key Findings asserts a HIGH confidence answer for any item listed in Open Questions

  Scenario: Analyst does not produce implementation artifacts or modify non-analysis files
    Given an analysis task scoped to a story or requirements artifact
    When the developer spawns the analyst agent with that task
    Then the agent does not write or commit any code files, story index files, or sprint records
    And any output written to disk is an assessment or findings document
