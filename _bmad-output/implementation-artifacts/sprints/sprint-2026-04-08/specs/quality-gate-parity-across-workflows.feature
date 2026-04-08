Feature: Quality Gate Parity Across Workflows

  Background:
    Given a Momentum project with stories ready for development

  Scenario: quick-fix surfaces code review findings before team validation
    Given a story has been merged by the quick-fix workflow
    When the quick-fix Phase 4 quality gates run
    Then a code review via momentum:code-reviewer runs after the AVFL scan
    And the code review findings are presented to the developer before team validation begins

  Scenario: quick-fix passes code review findings into the collaborative fix loop
    Given momentum:code-reviewer has produced findings during a quick-fix run
    When the collaborative fix team is created
    Then the code review findings appear in the team's task list alongside AVFL findings
    And the Dev agent addresses both sets of findings in the same fix loop

  Scenario: the developer cannot invoke momentum:dev directly from Impetus
    Given the developer opens the Impetus menu
    When the developer reviews the available commands
    Then no develop or dev command appears in the menu
    And the developer is directed to momentum:quick-fix for single-story development

  Scenario: a story developed via quick-fix receives all four quality gates
    Given a story is run through the quick-fix workflow end to end
    When each phase completes
    Then a pre-implementation AVFL checkpoint runs before implementation begins
    And a post-merge AVFL scan runs after the worktree is merged
    And code review runs after the AVFL scan
    And team validation runs with the appropriate validators for the story's change_type

  Scenario: the worktree remains available throughout all quality gate phases
    Given a story has been merged and quality gates are running in quick-fix
    When AVFL, code review, or team validation produces findings requiring fixes
    Then the worktree is still accessible for fix iterations
    And the worktree is only deleted after all gates pass or the developer explicitly accepts remaining findings
