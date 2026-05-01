Feature: Plugin Cross-References — Update All Internal References

  Background:
    Given the full plugin structure is in place
    And all skills, scripts, hooks, and references are at their final locations

  Scenario: No references to old skill paths remain
    When all cross-references are updated
    Then searching the repository for "skills/momentum-" returns zero results in skill files
    And searching for "momentum-avfl" in spawn or invoke contexts returns zero results
    And searching for "momentum-dev" in spawn or invoke contexts returns zero results

  Scenario: Impetus workflow uses correct spawn names
    When all cross-references are updated
    Then Impetus workflow.md spawns skills using "momentum:<name>" format
    And all skill names in spawn prompts match the plugin namespace convention

  Scenario: AVFL sub-skill references are correct
    When all cross-references are updated
    Then AVFL SKILL.md references sub-skills at paths relative to its new location
    And each referenced sub-skill path resolves to an existing file

  Scenario: momentum-tools.py path references are correct
    When all cross-references are updated
    Then every file that invokes momentum-tools.py uses a valid path to the script

  Scenario: Architecture document reflects actual structure
    When all cross-references are updated
    Then the plugin model section in architecture.md matches the actual directory layout
    And no path in the architecture document references a non-existent file

  Scenario: PRD plugin references are consistent
    When all cross-references are updated
    Then FR71 and FR72 in prd.md are consistent with the actual plugin implementation
    And skill names listed in the PRD match actual SKILL.md name fields

  Scenario: Zero dead references across the repository
    When all cross-references are updated
    Then every file path mentioned in any SKILL.md resolves to an existing file
    And every file path mentioned in any workflow resolves to an existing file
