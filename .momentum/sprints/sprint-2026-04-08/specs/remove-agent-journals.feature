Feature: Remove Agent Journals — Delete Sprint-Log Write Infrastructure

  Background:
    Given the Momentum plugin is installed in the project

  Scenario: Workflows complete without writing sprint-log entries
    Given a sprint is active with stories ready for development
    When the developer invokes sprint-dev and stories are executed
    Then no entries are written to any .claude/momentum/sprint-logs/ directory
    And the workflow completes and produces its normal outputs

  Scenario: momentum-tools rejects the log subcommand
    Given the momentum-tools script is available on the path
    When the developer runs momentum-tools log with any arguments
    Then the command exits with an error indicating log is not a recognized subcommand
    And no JSONL file is created

  Scenario: Retro produces findings without any sprint-log data present
    Given a completed sprint with DuckDB transcripts available
    And no sprint-log entries exist for the sprint
    When the developer invokes retro
    Then the retro completes all phases and produces an findings report
    And the report contains findings derived from transcript analysis

  Scenario: Subagent lifecycle events produce no observability log entries
    Given a workflow spawns subagents during execution
    When the subagents start and stop
    Then no observability JSONL entries are written to sprint-logs
    And the workflow completes normally
