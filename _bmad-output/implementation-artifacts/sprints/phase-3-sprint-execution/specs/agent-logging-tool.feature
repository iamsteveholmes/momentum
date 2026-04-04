Feature: Agent Logging Tool
  The `log` subcommand of momentum-tools.py provides structured JSONL event
  logging for all agents during sprint execution. Append-only, deterministic,
  and self-provisioning.

  Background:
    Given a project directory with CLAUDE_PROJECT_DIR set
    And no sprint-log directory exists yet

  # --- Happy Path ---

  Scenario: First log entry creates directory structure and file
    When I run momentum-tools log --agent "dev" --sprint "phase-3" --event "decision" --detail "Starting implementation"
    Then the exit code is 0
    And the directory ".claude/momentum/sprint-logs/phase-3/" exists
    And the file ".claude/momentum/sprint-logs/phase-3/dev.jsonl" exists
    And stdout contains valid JSON with "success": true

  Scenario: Log entry with story creates story-scoped file
    When I run momentum-tools log --agent "dev" --story "agent-logging-tool" --sprint "phase-3" --event "finding" --detail "Tests pass"
    Then the exit code is 0
    And the file ".claude/momentum/sprint-logs/phase-3/dev-agent-logging-tool.jsonl" exists
    And the file ".claude/momentum/sprint-logs/phase-3/dev.jsonl" does not exist

  Scenario: Log entry without story creates agent-only file
    When I run momentum-tools log --agent "impetus" --sprint "phase-3" --event "decision" --detail "Spawning dev agent"
    Then the exit code is 0
    And the file ".claude/momentum/sprint-logs/phase-3/impetus.jsonl" exists

  Scenario: Log entry contains all required fields with correct types
    When I run momentum-tools log --agent "dev" --sprint "phase-3" --event "decision" --detail "Chose approach A"
    Then the exit code is 0
    And the JSONL line in "dev.jsonl" contains key "timestamp" with an ISO 8601 value
    And the JSONL line contains key "agent" with value "dev"
    And the JSONL line contains key "story" with value null
    And the JSONL line contains key "event" with value "decision"
    And the JSONL line contains key "detail" with value "Chose approach A"

  Scenario: Log entry with story populates story field
    When I run momentum-tools log --agent "dev" --story "my-story" --sprint "phase-3" --event "assumption" --detail "API returns JSON"
    Then the JSONL line contains key "story" with value "my-story"

  Scenario: Multiple appends accumulate in the same file
    Given I run momentum-tools log --agent "dev" --sprint "s1" --event "decision" --detail "First"
    And I run momentum-tools log --agent "dev" --sprint "s1" --event "finding" --detail "Second"
    And I run momentum-tools log --agent "dev" --sprint "s1" --event "error" --detail "Third"
    Then the file ".claude/momentum/sprint-logs/s1/dev.jsonl" contains exactly 3 lines
    And each line is valid JSON
    And the lines have distinct timestamps

  Scenario: All six event types are accepted
    When I run momentum-tools log with event type "decision"
    Then the exit code is 0
    When I run momentum-tools log with event type "error"
    Then the exit code is 0
    When I run momentum-tools log with event type "retry"
    Then the exit code is 0
    When I run momentum-tools log with event type "assumption"
    Then the exit code is 0
    When I run momentum-tools log with event type "finding"
    Then the exit code is 0
    When I run momentum-tools log with event type "ambiguity"
    Then the exit code is 0

  Scenario: Stdout confirmation includes log metadata
    When I run momentum-tools log --agent "dev" --sprint "s1" --event "decision" --detail "test"
    Then stdout JSON contains "action": "log"
    And stdout JSON contains "success": true
    And stdout JSON contains "file" with the path to the written JSONL file

  # --- Error Handling ---

  Scenario: Invalid event type is rejected
    When I run momentum-tools log --agent "dev" --sprint "s1" --event "warning" --detail "test"
    Then the exit code is 1
    And stdout JSON contains "success": false
    And stdout JSON contains an error message mentioning valid event types

  Scenario: Missing --agent argument is rejected
    When I run momentum-tools log --sprint "s1" --event "decision" --detail "test"
    Then the exit code is not 0
    And stderr contains an error about the missing required argument

  Scenario: Missing --event argument is rejected
    When I run momentum-tools log --agent "dev" --sprint "s1" --detail "test"
    Then the exit code is not 0
    And stderr contains an error about the missing required argument

  Scenario: Missing --detail argument is rejected
    When I run momentum-tools log --agent "dev" --sprint "s1" --event "decision"
    Then the exit code is not 0
    And stderr contains an error about the missing required argument

  Scenario: Missing --sprint argument falls back to _unsorted directory
    When I run momentum-tools log --agent "dev" --event "decision" --detail "test"
    Then the exit code is 0
    And the file ".claude/momentum/sprint-logs/_unsorted/dev.jsonl" exists
    And the log entry has "sprint" field set to null

  # --- Append-Only Guarantee ---

  Scenario: Logging never modifies existing entries
    Given the file ".claude/momentum/sprint-logs/s1/dev.jsonl" contains a pre-existing entry
    When I run momentum-tools log --agent "dev" --sprint "s1" --event "finding" --detail "New entry"
    Then the pre-existing entry is unchanged (byte-identical first line)
    And the new entry is appended as the last line

  # --- Concurrent Safety ---

  Scenario: Concurrent agents write to separate files
    Given agent "frontend-dev" logs to story "ui-story" in sprint "s1"
    And agent "backend-dev" logs to story "api-story" in sprint "s1"
    Then "frontend-dev-ui-story.jsonl" and "backend-dev-api-story.jsonl" are separate files
    And neither file contains entries from the other agent

  # --- Edge Cases ---

  Scenario: Detail text with special characters is preserved
    When I run momentum-tools log --agent "dev" --sprint "s1" --event "error" --detail "Failed: \"Connection refused\" on port 5432\nnested newline"
    Then the JSONL entry's detail field contains the exact input string including quotes

  Scenario: Agent role with hyphens works correctly
    When I run momentum-tools log --agent "momentum-sprint-manager" --sprint "s1" --event "decision" --detail "test"
    Then the file is named "momentum-sprint-manager.jsonl"
    And the agent field in the entry is "momentum-sprint-manager"

  Scenario: Sprint slug with hyphens works correctly
    When I run momentum-tools log --agent "dev" --sprint "phase-3-sprint-execution" --event "decision" --detail "test"
    Then the directory is ".claude/momentum/sprint-logs/phase-3-sprint-execution/"
