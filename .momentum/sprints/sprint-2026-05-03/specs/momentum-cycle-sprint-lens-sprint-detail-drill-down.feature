Feature: Momentum Cycle — Sprint Lens + Sprint Detail Drill-Down

  Background:
    Given the Momentum Cycle dashboard is running at http://localhost:3456

  Scenario: Sprint lens shows active sprint summary
    Given an active sprint exists in the sprint index
    When the developer views the dashboard
    Then the Sprint lens section displays a card with the sprint identifier and start date
    And the card shows whether the sprint retro has been completed

  Scenario: Sprint lens shows empty state when no sprint is active
    Given no active sprint exists in the sprint index
    When the developer views the dashboard
    Then the Sprint lens section displays a message indicating no active sprint is running

  Scenario: Developer drills into sprint detail and sees stories by outcome
    Given an active sprint exists with stories in various statuses
    When the developer clicks the sprint card
    Then the page navigates to a sprint detail view
    And the URL updates to reflect the sprint being viewed
    And stories are grouped into Blocked, In Progress, and Validated sections

  Scenario: Story navigation from sprint detail leads to story view
    Given the developer is viewing a sprint detail page with at least one story
    When the developer clicks a story row in the sprint detail
    Then the page navigates to a story detail view
    And the URL updates to reflect the story being viewed
