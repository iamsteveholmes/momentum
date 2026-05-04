Feature: Momentum Cycle — Dashboard Shell (Hono+Bun Server)

  Background:
    Given the developer has the Momentum plugin installed
    And the canvas skill is registered as /momentum:canvas

  Scenario: Developer opens the Momentum Cycle dashboard and sees the live UI
    Given port 3456 is not currently listening
    When the developer invokes /momentum:canvas
    Then a browser pane opens showing the Momentum Cycle dashboard at http://localhost:3456
    And the dashboard displays a dark background with three visible lens sections labeled Features, Sprint, and Cycle

  Scenario: Dashboard shows brand header and design elements
    Given the Momentum Cycle dashboard is running at http://localhost:3456
    When the developer views the dashboard root page
    Then the page displays a "Momentum Cycle" brand heading
    And a meta line appears in monospace font showing a git hash and date

  Scenario: Canvas skill skips server start when dashboard is already running
    Given port 3456 is already listening with the Momentum Cycle dashboard running
    When the developer invokes /momentum:canvas
    Then a browser pane opens at http://localhost:3456 without attempting to restart the server

  Scenario: Deprecated feature-status skill redirects to canvas
    When the developer invokes /momentum:feature-status
    Then the skill outputs a message indicating it is deprecated and instructs the developer to use /momentum:canvas instead
    And no HTML artifact is generated
