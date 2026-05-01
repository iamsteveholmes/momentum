Feature: Plugin Scripts, Hooks, and References — Consolidate at Plugin Root

  Background:
    Given the plugin structure exists with all 11 skills under "skills/momentum/skills/"
    And "skills/momentum/scripts/" contains momentum-tools.py
    And "skills/momentum/references/" contains shared reference files

  Scenario: Scripts remain at plugin root
    When the consolidation story is implemented
    Then "skills/momentum/scripts/momentum-tools.py" exists
    And the script content is unchanged

  Scenario: Shared references remain at plugin root
    When the consolidation story is implemented
    Then "skills/momentum/references/" exists with all original files
    And skill-specific references remain inside their skill directories

  Scenario: Hooks directory is created with valid hooks.json
    When the consolidation story is implemented
    Then "skills/momentum/hooks/hooks.json" exists
    And the hooks.json parses as valid JSON
    And the hooks.json follows Claude Code hooks schema

  Scenario: Always-on hooks are defined
    When the consolidation story is implemented
    Then hooks.json contains at least one hook definition
    And each hook has a valid event type and handler

  Scenario: Workflows directory is resolved
    When the consolidation story is implemented
    Then workflow files are either moved to consuming skill directories or documented as shared at plugin root
    And no workflow file is orphaned without a consumer

  Scenario: Skill-specific references stay in skill directories
    When the consolidation story is implemented
    Then "skills/momentum/skills/avfl/references/framework.json" still exists inside the avfl skill
    And it has not been moved to the plugin root references directory
