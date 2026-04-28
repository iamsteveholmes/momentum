Feature: Sprint-planning adds per-story approval gate

  Background:
    Given the developer is running sprint-planning with a selection of fleshed-out stories

  Scenario: Developer reviews and approves each story spec individually before activation
    Given a planning sprint contains multiple stories ready for review
    When the developer steps through sprint-planning
    Then each story spec opens in a markdown viewer for review
    And the developer is prompted to approve, revise, or reject each story before continuing
    And the sprint activates only after every story has been approved

  Scenario: Rejecting a story removes it from the sprint and halts when too few remain
    Given a planning sprint contains the minimum acceptable number of stories
    When the developer rejects one of the story specs at its approval prompt
    Then the rejected story is removed from the sprint selection
    And sprint-planning halts with a message that the remaining selection is below the minimum

  Scenario: Sprint-dev refuses to start when story approvals are missing or stale
    Given an active sprint where at least one story lacks a current approval
    When the developer invokes sprint-dev
    Then sprint-dev halts before any story moves to in-progress
    And the developer is told which stories are missing approval and directed back to sprint-planning
