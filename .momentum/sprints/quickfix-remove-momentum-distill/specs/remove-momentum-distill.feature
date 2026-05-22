Feature: Remove momentum:distill Skill

  Background:
    Given the momentum plugin repository is at skills/momentum/
    And the story has been implemented

  Scenario: Plugin version advances after removal
    When the developer reads skills/momentum/.claude-plugin/plugin.json
    Then the version field reads "0.23.0"
    And the file parses as valid JSON

  Scenario: No skill or workflow in the plugin invokes momentum:distill
    When the developer runs grep -rn "momentum:distill" skills/momentum/
    Then grep returns zero matches

  Scenario: The distill skill directory no longer exists
    When the developer runs ls skills/momentum/skills/distill/
    Then the command exits with a non-zero status code

  Scenario: momentum:distill is not available as an invocable skill
    Given the distill skill directory has been removed
    When the developer looks for momentum:distill in the skills/momentum/skills/ directory
    Then no distill/ directory exists under skills/momentum/skills/
