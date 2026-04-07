Feature: Workflow Team Composition Spec

  Background:
    Given a Momentum project with sprint-dev and sprint-planning workflows
    And a sprint with stories assigned to dev agents

  Scenario: Dev wave agents are spawned individually not as a team
    When the sprint-dev workflow executes the dev wave phase
    Then each dev agent is spawned as a separate individual agent
    And no dev agents are spawned via grouped team creation

  Scenario: Review agents are spawned individually in parallel
    Given a sprint-dev workflow has reached the team review phase
    When the review phase executes
    Then a QA agent is spawned as an individual agent
    And an E2E Validator agent is spawned as an individual agent
    And an Architect Guard agent is spawned as an individual agent
    And no review agents are spawned via grouped team creation

  Scenario: Fix agents are spawned individually on the sprint branch
    Given the AVFL phase has identified critical findings requiring fixes
    When fix agents are spawned for the findings
    Then each fix agent is spawned as a separate individual agent
    And fix agents operate on the sprint branch without worktrees

  Scenario: AVFL validators are spawned individually not as a team
    When the AVFL skill executes its validation phase
    Then each validator agent is spawned as a separate individual agent
    And no validators are spawned via grouped team creation

  Scenario: AVFL pipeline runs consolidator after validators complete
    When the AVFL skill executes its full pipeline
    Then all validator agents complete before the consolidator starts
    And the fixer agent does not start until the consolidator completes

  Scenario: Sprint planning surfaces missing required roles before activation
    Given a sprint plan where the team object has no dev agent assigned
    When sprint planning validates the team composition
    Then sprint planning reports the missing required role
    And the sprint is not activated until the gap is resolved

  Scenario: Sprint planning validates all stories have agent assignments
    Given a sprint plan with a story that has no agent assigned
    When sprint planning validates the team composition
    Then sprint planning reports the unassigned story
    And the sprint is not activated until all stories are assigned
