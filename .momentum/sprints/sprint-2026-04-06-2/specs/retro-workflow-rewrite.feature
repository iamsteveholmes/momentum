Feature: Retro Workflow Rewrite — Replace Milestone Logs with Transcript Audit

  Background:
    Given a completed sprint with session transcripts available

  Scenario: Preprocessing extracts structured data from session transcripts
    When the retro runs its preprocessing step
    Then user messages are extracted from all sprint sessions
    And agent summaries are extracted with per-agent digests
    And tool errors are extracted from session data
    And inter-agent messages are extracted
    And each extract type is written to the sprint audit-extracts directory

  Scenario: User messages exclude tool results and capture only human prompts
    When the retro extracts user messages
    Then every extracted entry represents a human-typed prompt
    And tool results and system messages are not included
    And entries span all sessions within the sprint date range

  Scenario: Auditor team analyzes extracts with specialized roles
    Given preprocessed extracts exist for the sprint
    When the retro spawns the auditor team
    Then three auditors and one documenter are created
    And auditors communicate findings to the documenter via messaging
    And a findings document is produced for the sprint

  Scenario: Findings document covers both successes and struggles
    Given the auditor team has completed analysis
    When the documenter assembles the findings document
    Then the document includes a section on what worked well
    And the document includes a section on what struggled
    And each finding includes evidence and a recommendation

  Scenario: Retro produces findings without milestone log events
    Given a sprint with no milestone log events recorded
    When the retro runs
    Then transcript audit still produces substantive findings
    And the retro completes without halting or producing empty output

  Scenario: Retro produces actionable story stubs from audit findings
    Given the auditor team has produced findings with recommendations
    When the retro generates improvement stories
    Then each story stub has a description and acceptance criteria
    And story stubs trace back to specific audit findings

  Scenario: Session discovery matches sprint date range automatically
    Given a sprint with defined start and end dates
    When the retro discovers session transcripts
    Then only sessions within the sprint date range are included
    And no manual path specification is required

  Scenario: Ad-hoc queries can be run against session transcripts
    Given preprocessed session data is available
    When an auditor runs a custom SQL query against session transcripts
    Then the query returns results from the session data
    And the query tool supports arbitrary SQL expressions

  Scenario: Extracted errors reflect actual failures not false matches
    Given session transcripts containing both real errors and benign content
    When the retro extracts errors
    Then flagged errors correspond to genuine tool or execution failures
    And benign content is not misidentified as errors
