Feature: Impetus Greeting Rewrite — 9-State Narrative Orientation

  The Impetus greeting orients the user with a narrative prose greeting
  and an adaptive menu based on the current sprint state. Fill bars
  and dashboard formatting are replaced with voice-driven text.

  # -------------------------------------------------------------------
  # Greeting output characteristics
  # -------------------------------------------------------------------

  Scenario: Greeting contains no fill bar block characters
    Given a project with an active sprint in progress
    When the user invokes /momentum:impetus
    Then the greeting output does not contain any of the characters "░", "▒", or "█"

  Scenario: Greeting does not list individual story slugs or counts
    Given a project with an active sprint containing multiple stories
    When the user invokes /momentum:impetus
    Then the greeting output does not include a numbered list of story slugs
    And the greeting output does not include a story count

  Scenario: No file diff or write operation is visible during greeting
    Given a project with an active sprint in progress
    When the user invokes /momentum:impetus
    Then no file write output appears before the menu is presented

  # -------------------------------------------------------------------
  # First session identity declaration
  # -------------------------------------------------------------------

  Scenario: First session ever shows identity declaration
    Given a project with no sprint history and zero prior completions
    When the user invokes /momentum:impetus
    Then the greeting includes an identity declaration stating what Impetus stands for
    And the greeting does not reference any sprint by name

  # -------------------------------------------------------------------
  # Active sprint states
  # -------------------------------------------------------------------

  Scenario: Active sprint not started — menu offers to run the sprint
    Given a project with an active sprint where no stories have started
    When the user invokes /momentum:impetus
    Then the greeting references the active sprint by name
    And the menu includes an option to run the sprint
    And the menu does not include an option to continue the sprint

  Scenario: Active sprint in progress — menu offers to continue the sprint
    Given a project with an active sprint where stories are in progress
    When the user invokes /momentum:impetus
    Then the greeting references the active sprint by name
    And the menu includes an option to continue the sprint
    And the menu does not include an option to run the sprint

  Scenario: Active sprint blocked — greeting acknowledges the obstacle
    Given a project with an active sprint where at least one story is blocked
    When the user invokes /momentum:impetus
    Then the greeting conveys that something is blocking progress
    And the menu includes an option to continue the sprint

  Scenario: Planning sprint needs work — menu offers to finish planning
    Given a project with an active sprint and a planning sprint that is incomplete
    When the user invokes /momentum:impetus
    Then the greeting references the planning sprint
    And the menu includes an option to finish planning

  Scenario: Planning sprint needs work — finish planning option absent without planning sprint
    Given a project with an active sprint and no planning sprint
    When the user invokes /momentum:impetus
    Then the menu does not include an option to finish planning

  # -------------------------------------------------------------------
  # Done states
  # -------------------------------------------------------------------

  Scenario: done-retro-needed state — retro is first menu item
    Given a project with an active sprint where status is "done" and a planning sprint exists
    When the user invokes /momentum:impetus
    Then the greeting conveys that the sprint work is complete
    And the first menu item is an option to run a retrospective

  Scenario: done-no-planned state — retro is first, plan is available
    Given a project with an active sprint where status is "done" and no planning sprint exists
    When the user invokes /momentum:impetus
    Then the first menu item is an option to run a retrospective
    And the menu includes an option to plan a sprint

  # -------------------------------------------------------------------
  # No active sprint states
  # -------------------------------------------------------------------

  Scenario: No active sprint and nothing planned — menu offers to plan
    Given a project with no active sprint and no planned sprint
    When the user invokes /momentum:impetus
    Then the greeting does not reference a current sprint in progress
    And the menu includes an option to plan a sprint

  Scenario: No active sprint but planned sprint ready — menu offers to activate
    Given a project with no active sprint and a planned sprint marked ready
    When the user invokes /momentum:impetus
    Then the greeting references the planned sprint by name
    And the menu includes an option to activate the sprint

  # -------------------------------------------------------------------
  # Voice characteristics
  # -------------------------------------------------------------------

  Scenario: Greeting voice uses narrative prose, not dashboard labels
    Given a project with an active sprint in progress
    When the user invokes /momentum:impetus
    Then the greeting output is written in narrative prose
    And the greeting output does not contain labels like "STATUS:", "PROGRESS:", or "MODE"

  # -------------------------------------------------------------------
  # Menu adapts per state — no expertise-adaptive question
  # -------------------------------------------------------------------

  Scenario: Greeting does not ask about walkthrough vs decision points
    Given a project with an active sprint in progress
    When the user invokes /momentum:impetus
    Then the greeting does not ask whether the user wants a full walkthrough or decision points
