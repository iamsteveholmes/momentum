Feature: Hooks Global Distribution — Move Hook Scripts to Global Path

  Background:
    Given Momentum is installed as a global plugin

  Scenario: Hook scripts fire without errors in a non-Momentum project
    Given the developer is working in a project that has no local Momentum hook scripts
    When a session ends, a file is edited, or a file is written in that project
    Then no "No such file or directory" error appears for any hook script
    And each hook exits silently without disrupting the developer's workflow

  Scenario: Hooks fire correctly in a Momentum project after global distribution
    Given the developer is working in a project with Momentum configured
    When a session ends, a file is edited, or a file is written in that project
    Then the stop-gate, lint-format, and file-protection hooks execute as expected
    And hook behavior is identical to before the global path change

  Scenario: Project-local hook script takes precedence over the global one
    Given the developer is working in a project that has a local stop-gate.sh override
    When a session ends in that project
    Then the local hook script runs instead of the global one
