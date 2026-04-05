Feature: Sprint Lifecycle Tools — Status Fields, New Commands, and Unit Tests

  Background:
    Given a project directory with a valid momentum configuration
    And the momentum-tools.py script is available at skills/momentum/scripts/momentum-tools.py

  # --- sprint plan: status field ---

  Scenario: sprint plan creates a new sprint with status planning
    When I run "python3 skills/momentum/scripts/momentum-tools.py sprint plan" with valid sprint arguments
    Then the command output is JSON with "success" set to true
    And the planning entry in sprints/index.json contains "status" set to "planning"

  # --- sprint activate: status field ---

  Scenario: sprint activate sets status to active
    Given a planning sprint exists in sprints/index.json with "status" set to "planning"
    When I run "python3 skills/momentum/scripts/momentum-tools.py sprint activate"
    Then the command output is JSON with "success" set to true
    And the active sprint in sprints/index.json contains "status" set to "active"

  # --- sprint complete: status and retro_run_at fields ---

  Scenario: sprint complete sets status to done and retro_run_at to null
    Given an active sprint exists in sprints/index.json with "status" set to "active"
    When I run "python3 skills/momentum/scripts/momentum-tools.py sprint complete"
    Then the command output is JSON with "success" set to true
    And the most recent completed entry in sprints/index.json contains "status" set to "done"
    And the most recent completed entry in sprints/index.json contains "retro_run_at" set to null

  # --- sprint ready: new command ---

  Scenario: sprint ready sets status to ready
    Given a planning sprint exists in sprints/index.json with "status" set to "planning"
    When I run "python3 skills/momentum/scripts/momentum-tools.py sprint ready"
    Then the command output is JSON with "success" set to true
    And the planning entry in sprints/index.json contains "status" set to "ready"

  Scenario: sprint ready fails when no planning sprint exists
    Given no planning sprint exists in sprints/index.json
    When I run "python3 skills/momentum/scripts/momentum-tools.py sprint ready"
    Then the command exits with a non-zero exit code
    And the command output is JSON with "success" set to false

  # --- sprint retro-complete: new command ---

  Scenario: sprint retro-complete sets retro_run_at on most recent eligible completed sprint
    Given a completed sprint exists in sprints/index.json with "retro_run_at" set to null
    When I run "python3 skills/momentum/scripts/momentum-tools.py sprint retro-complete"
    Then the command output is JSON with "success" set to true
    And the most recent completed entry in sprints/index.json contains "retro_run_at" set to today's date

  Scenario: sprint retro-complete auto-activates a ready planning sprint
    Given a completed sprint exists in sprints/index.json with "retro_run_at" set to null
    And a planning sprint exists in sprints/index.json with "status" set to "ready"
    When I run "python3 skills/momentum/scripts/momentum-tools.py sprint retro-complete"
    Then the command output is JSON with "success" set to true
    And the most recent completed entry in sprints/index.json contains "retro_run_at" set to today's date
    And no planning sprint exists in sprints/index.json
    And an active sprint exists in sprints/index.json with "status" set to "active"

  Scenario: sprint retro-complete does not auto-activate a planning-status sprint
    Given a completed sprint exists in sprints/index.json with "retro_run_at" set to null
    And a planning sprint exists in sprints/index.json with "status" set to "planning"
    When I run "python3 skills/momentum/scripts/momentum-tools.py sprint retro-complete"
    Then the command output is JSON with "success" set to true
    And the most recent completed entry in sprints/index.json contains "retro_run_at" set to today's date
    And the planning entry in sprints/index.json still contains "status" set to "planning"

  Scenario: sprint retro-complete fails when no completed sprint has retro_run_at unset
    Given all completed sprints in sprints/index.json have "retro_run_at" set to a date
    When I run "python3 skills/momentum/scripts/momentum-tools.py sprint retro-complete"
    Then the command exits with a non-zero exit code
    And the command output is JSON with "success" set to false

  # --- session stats-update: new command ---

  Scenario: session stats-update creates session_stats when absent
    Given installed.json exists with no "session_stats" section
    When I run "python3 skills/momentum/scripts/momentum-tools.py session stats-update"
    Then the command output is JSON with "success" set to true
    And installed.json contains a "session_stats" section
    And "session_stats.momentum_completions" is set to 1
    And "session_stats.last_invocation" is set to today's date

  Scenario: session stats-update increments existing momentum_completions
    Given installed.json contains "session_stats" with "momentum_completions" set to 5
    When I run "python3 skills/momentum/scripts/momentum-tools.py session stats-update"
    Then the command output is JSON with "success" set to true
    And "session_stats.momentum_completions" is set to 6
    And "session_stats.last_invocation" is set to today's date

  Scenario: session stats-update preserves other data in installed.json
    Given installed.json contains "session_stats" and other top-level keys with values
    When I run "python3 skills/momentum/scripts/momentum-tools.py session stats-update"
    Then the command output is JSON with "success" set to true
    And all other top-level keys in installed.json retain their original values
