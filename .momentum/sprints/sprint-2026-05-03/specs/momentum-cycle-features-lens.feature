Feature: Momentum Cycle — Features Lens

  Background:
    Given the Momentum Cycle dashboard is running at http://localhost:3456
    And features.json exists with at least one feature entry

  Scenario: Features lens shows current feature status
    When the developer views the dashboard
    Then the Features lens section renders a table with one row per feature
    And each row shows the feature name, a status indicator, and a story progress fraction

  Scenario: Features with gaps appear at the top of the table
    Given features.json contains features with and without gaps
    When the developer views the Features lens
    Then features flagged as having a gap appear above features without gaps
    And gap rows are visually distinct from non-gap rows

  Scenario: Features lens reflects updated data within two seconds
    Given the Features lens is visible on the dashboard
    When the developer updates a feature entry in features.json
    Then the Features lens table updates to reflect the change within two seconds without a page reload

  Scenario: Features lens shows an empty state when no features exist
    Given features.json is absent or contains no feature entries
    When the developer views the Features lens
    Then the Features lens section displays a message indicating no features were found
    And no table rows appear
