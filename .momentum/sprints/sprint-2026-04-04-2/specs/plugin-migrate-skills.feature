Feature: Plugin Migrate Skills — Move Satellite Skills into Plugin Structure

  Background:
    Given the plugin skeleton exists at "skills/momentum/.claude-plugin/plugin.json"
    And 10 satellite skills exist at "skills/momentum-*/" directories

  Scenario: All satellite skills move to plugin structure
    When all 10 satellite skills are migrated
    Then "skills/momentum/skills/avfl/SKILL.md" exists
    And "skills/momentum/skills/dev/SKILL.md" exists
    And "skills/momentum/skills/create-story/SKILL.md" exists
    And "skills/momentum/skills/plan-audit/SKILL.md" exists
    And "skills/momentum/skills/sprint-manager/SKILL.md" exists
    And "skills/momentum/skills/agent-guidelines/SKILL.md" exists
    And "skills/momentum/skills/code-reviewer/SKILL.md" exists
    And "skills/momentum/skills/architecture-guard/SKILL.md" exists
    And "skills/momentum/skills/upstream-fix/SKILL.md" exists
    And "skills/momentum/skills/research/SKILL.md" exists

  Scenario: Name fields are updated to short names
    When all 10 satellite skills are migrated
    Then the SKILL.md at "skills/momentum/skills/avfl/" has name "avfl"
    And the SKILL.md at "skills/momentum/skills/dev/" has name "dev"
    And the SKILL.md at "skills/momentum/skills/create-story/" has name "create-story"

  Scenario: Old directories are removed
    When all 10 satellite skills are migrated
    Then no directories matching "skills/momentum-*/" exist

  Scenario: Complex subdirectories are preserved
    When all 10 satellite skills are migrated
    Then "skills/momentum/skills/avfl/sub-skills/" contains 4 sub-skill directories
    And "skills/momentum/skills/avfl/references/framework.json" exists
    And "skills/momentum/skills/avfl/evals/" is non-empty

  Scenario: SKILL.md content is unchanged beyond name field
    When a satellite skill is migrated
    Then only the "name" field in SKILL.md frontmatter differs from the original
    And the description, model, effort, and body content are identical

  Scenario: Plugin discovers all 11 skills
    When all migrations are complete
    Then the plugin.json skills glob matches 11 SKILL.md files
