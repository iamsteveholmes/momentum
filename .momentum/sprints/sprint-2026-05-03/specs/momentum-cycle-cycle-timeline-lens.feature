Feature: Momentum Cycle — Cycle Timeline Lens

  Background:
    Given the Momentum Cycle dashboard is running at http://localhost:3456

  Scenario: Cycle timeline shows seven phases with current progression
    When the developer views the dashboard
    Then the Cycle lens displays exactly seven phase nodes in left-to-right order
    And each node shows a distinct visual state indicating whether the phase is done, upcoming, or not yet reached

  Scenario: Next-required indicator appears only on a required phase
    Given the sprint index shows sprint-planning is complete but sprint-dev has not started
    When the developer views the Cycle timeline
    Then the sprint-dev node shows the next-required visual indicator
    And optional phase nodes do not show the next-required indicator

  Scenario: Status line summarizes current cycle position
    Given the sprint index contains at least one completed sprint
    When the developer views the Cycle timeline
    Then a status line below the nodes displays the next required phase name and the most recent sprint identifier

  Scenario: Cycle timeline reflects updated sprint state within the polling interval
    Given the Cycle lens is visible on the dashboard
    When the developer completes a sprint retro and the sprint data is updated accordingly
    Then the Cycle lens updates to show the retro phase as done within the polling interval without a page reload
