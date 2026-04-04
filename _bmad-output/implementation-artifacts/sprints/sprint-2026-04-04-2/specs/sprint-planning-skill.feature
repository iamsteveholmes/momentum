Feature: Sprint Planning Skill — SKILL.md for Sprint Planning Workflow

  Scenario: SKILL.md exists with valid frontmatter
    When the sprint-planning skill story is implemented
    Then "skills/momentum/skills/sprint-planning/SKILL.md" exists
    And the SKILL.md has "name" field set to "sprint-planning"
    And the SKILL.md has "model" field present
    And the SKILL.md has "effort" field present
    And the SKILL.md description is 150 characters or fewer

  Scenario: Workflow content is accessible from SKILL.md
    When the sprint-planning skill story is implemented
    Then the SKILL.md references a workflow file
    And the referenced workflow file exists and contains the 9-step sprint planning workflow

  Scenario: Skill is independently invocable
    Given no other Momentum skill is running
    When a user invokes "/momentum:sprint-planning"
    Then the skill loads and begins the backlog presentation step

  Scenario: All 9 workflow steps are reachable
    When the sprint-planning skill is invoked with an active backlog
    Then step 1 presents the prioritized backlog
    And step 2 accepts story selection
    And step 3 fleshes out story stubs
    And step 4 generates Gherkin specs
    And step 4.5 analyzes spec impact
    And step 5 builds team composition
    And step 6 runs AVFL validation
    And step 7 presents for developer review
    And step 8 activates the sprint

  Scenario: Workflow file is moved from shared location
    When the sprint-planning skill story is implemented
    Then "skills/momentum/workflows/sprint-planning.md" no longer exists at the old location
    And the content is available under the sprint-planning skill directory
