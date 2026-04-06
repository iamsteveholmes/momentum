Feature: Impetus Allowed-Tools Restriction — Enforce Orchestrator Read-Only

  Background:
    Given Impetus is installed and configured in the developer's project
    And the developer has a valid momentum configuration

  Scenario: Impetus greeting completes without errors
    Given the developer is in a project with an existing sprint
    When the developer invokes Impetus
    Then Impetus displays the session greeting with project context
    And no tool errors appear in the output
    And Impetus presents available workflow options

  Scenario: Impetus greeting displays open threads when present
    Given the developer is in a project with unresolved open threads
    When the developer invokes Impetus
    Then Impetus displays the open threads in the greeting
    And the greeting completes without errors

  Scenario: Impetus greeting detects and reports hash drift
    Given the developer is in a project where a skill file has changed since last sync
    When the developer invokes Impetus
    Then Impetus reports the hash drift in the greeting
    And the greeting completes without errors

  Scenario: Impetus dispatches sprint-planning via agent delegation
    Given the developer is in a project ready for sprint planning
    When the developer invokes Impetus and selects sprint planning
    Then Impetus delegates to the sprint-planning workflow
    And the sprint-planning workflow begins executing

  Scenario: Impetus dispatches sprint-dev via agent delegation
    Given the developer is in a project with an active sprint containing stories
    When the developer invokes Impetus and selects sprint development
    Then Impetus delegates to the sprint-dev workflow
    And the sprint-dev workflow begins executing

  Scenario: Impetus runs momentum-tools commands successfully
    Given the developer is in a configured momentum project
    When Impetus needs to query project state
    Then Impetus executes momentum-tools.py and receives results
    And the results inform its session greeting

  Scenario: First-install workflow completes for a new project
    Given the developer is in a project with no momentum configuration
    When the developer invokes Impetus for the first time
    Then Impetus detects the missing configuration
    And Impetus runs the first-install workflow
    And the required configuration files are written to disk
    And Impetus confirms the installation is complete

  Scenario: Install workflow writes files using Bash commands
    Given the developer is in a project with no momentum configuration
    When the developer invokes Impetus and the first-install workflow runs
    Then all file creation operations execute through Bash commands
    And no Write or Edit tool calls are used during the install process

  Scenario: Upgrade workflow runs when a newer version is detected
    Given the developer has an outdated momentum installation
    When the developer invokes Impetus
    Then Impetus detects the version mismatch
    And Impetus runs the upgrade workflow
    And the upgrade completes without errors
    And Impetus continues to the normal greeting after upgrading
