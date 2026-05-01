Feature: Plugin Skeleton — Create Plugin Root and Manifest

  Background:
    Given the Momentum project has skills in flat "skills/momentum/" directory
    And no ".claude-plugin/" directory exists

  Scenario: Plugin manifest is created with correct schema
    When the plugin skeleton story is implemented
    Then "skills/momentum/.claude-plugin/plugin.json" exists
    And the manifest contains "name" field with value "momentum"
    And the manifest contains "version" field
    And the manifest contains "description" field
    And the manifest contains "skills" glob pattern
    And the manifest parses as valid JSON

  Scenario: Impetus moves to nested skills directory
    When the plugin skeleton story is implemented
    Then "skills/momentum/skills/impetus/SKILL.md" exists
    And "skills/momentum/skills/impetus/workflow.md" exists
    And the SKILL.md "name" field is "impetus"

  Scenario: Old Impetus location is cleaned up
    When the plugin skeleton story is implemented
    Then "skills/momentum/SKILL.md" does not exist
    And "skills/momentum/workflow.md" does not exist

  Scenario: Impetus evals are preserved
    When the plugin skeleton story is implemented
    Then "skills/momentum/skills/impetus/evals/" contains the same number of files as the original evals directory

  Scenario: Non-Impetus files remain untouched
    When the plugin skeleton story is implemented
    Then "skills/momentum/references/" exists with all original files
    And "skills/momentum/scripts/" exists with all original files
    And "skills/momentum/workflows/" exists with all original files

  Scenario: Plugin skill discovery works
    When the plugin skeleton story is implemented
    Then the skills glob in plugin.json matches "skills/momentum/skills/impetus/SKILL.md"
