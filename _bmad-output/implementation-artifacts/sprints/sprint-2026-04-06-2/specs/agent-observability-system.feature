Feature: Agent Observability System — Hook-Based Logging for Retro Flywheel

  Background:
    Given the Momentum plugin is installed with observability hooks enabled

  Scenario: Subagent start produces a structured log entry
    Given an active sprint is configured
    When a subagent is spawned during a session
    Then a log entry with event type "subagent-start" appears in the sprint log directory
    And the entry contains the subagent name and a timestamp

  Scenario: Subagent stop produces a structured log entry with summary
    Given an active sprint is configured
    When a subagent completes its work
    Then a log entry with event type "subagent-stop" appears in the sprint log directory
    And the entry contains the subagent name, timestamp, and a message summary

  Scenario: Stop event message summary is truncated for manageability
    Given a subagent that produces a final message longer than 500 characters
    When the subagent completes its work
    Then the message summary in the log entry is at most 500 characters

  Scenario: Events fall back to unsorted when no active sprint exists
    Given no active sprint is configured
    When a subagent is spawned and completes its work
    Then log entries appear in the unsorted log directory instead of a sprint directory

  Scenario: Hook failure does not block agent work
    Given the sprint log directory is not writable
    When a subagent is spawned
    Then the agent session continues without interruption
    And no error is surfaced to the user

  Scenario: Momentum log command accepts observability event types
    Given the momentum-tools log command is available
    When a user logs an event with type "subagent-start"
    Then the command accepts the event and writes it successfully
    When a user logs an event with type "subagent-stop"
    Then the command accepts the event and writes it successfully

  Scenario: Retro reads observability events without modification
    Given a sprint log directory containing subagent-start and subagent-stop entries
    When the retro skill collects log data for analysis
    Then the observability entries are included alongside existing log entries
