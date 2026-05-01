Feature: Sprint-Boundary Context Compression — Structured Sprint Summary at Retro Close

  Background:
    Given a sprint is underway with at least one completed story
    And the feature-status skill has been implemented

  Scenario: Sprint summary is written when retro reaches sprint closure
    When the developer runs the retro through to sprint closure
    Then a sprint-summary.md file appears in the sprint's artifact directory
    And the file contains a narrative section summarising the sprint
    And the file contains a stories completed vs planned section
    And the developer sees a confirmation line in the retro output pointing to the summary file

  Scenario: Sprint summary stays within the orientation length limit
    Given a sprint with multiple completed stories and several recorded decisions
    When the developer runs the retro through to sprint closure
    Then the sprint-summary.md that is written contains fewer than 500 words

  Scenario: Next sprint planning incorporates the previous sprint summary
    Given a completed sprint with a sprint-summary.md on file
    When the developer starts a new sprint planning session
    Then the planning session proceeds with context from the previous sprint
    And no warning about a missing sprint summary appears

  Scenario: Sprint planning continues gracefully when no prior summary exists
    Given no sprint has been completed yet
    When the developer starts a sprint planning session
    Then planning proceeds without error
    And a notice appears indicating that context from the previous sprint is unavailable
