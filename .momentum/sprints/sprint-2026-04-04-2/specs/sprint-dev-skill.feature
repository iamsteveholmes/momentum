Feature: Sprint Dev Skill — SKILL.md for Sprint Execution Workflow

  Scenario: SKILL.md exists with valid frontmatter
    When the sprint-dev skill story is implemented
    Then "skills/momentum/skills/sprint-dev/SKILL.md" exists
    And the SKILL.md has "name" field set to "sprint-dev"
    And the SKILL.md has "model" field present
    And the SKILL.md has "effort" field present
    And the SKILL.md description is 150 characters or fewer

  Scenario: Workflow content is accessible from SKILL.md
    When the sprint-dev skill story is implemented
    Then the SKILL.md references a workflow file
    And the referenced workflow file exists and contains the 7-phase sprint execution workflow

  Scenario: Skill is independently invocable
    Given no other Momentum skill is running
    When a user invokes "/momentum:sprint-dev"
    Then the skill loads and begins the initialization phase

  Scenario: All 7 execution phases are reachable
    When the sprint-dev skill is invoked with an active locked sprint
    Then phase 0 creates phase-level task tracking
    And phase 1 reads the sprint record and builds the dependency graph
    And phase 2 spawns dev agents for unblocked stories
    And phase 3 monitors progress and proposes merges
    And phase 4 runs post-merge AVFL scan
    And phase 5 runs team review with QA, E2E Validator, and Architect Guard
    And phase 6 presents the verification checklist
    And phase 7 completes the sprint

  Scenario: Workflow file is moved from shared location
    When the sprint-dev skill story is implemented
    Then "skills/momentum/workflows/sprint-dev.md" no longer exists at the old location
    And the content is available under the sprint-dev skill directory
