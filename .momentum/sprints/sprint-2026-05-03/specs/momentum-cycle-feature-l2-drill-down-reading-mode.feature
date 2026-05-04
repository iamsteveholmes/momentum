Feature: Momentum Cycle — Feature L2 Drill-Down (Reading Mode)

  Background:
    Given the Momentum Cycle dashboard is running at http://localhost:3456
    And features.json contains at least one feature with a title, status, and stories

  Scenario: Developer navigates to feature detail and sees reading mode layout
    Given the developer is viewing the Features lens on the dashboard
    When the developer clicks a feature row
    Then the page navigates to the feature detail view
    And the URL updates to reflect the feature being viewed
    And the page background switches to a warm light reading surface
    And the breadcrumb shows the current feature name as the active segment

  Scenario: Feature detail shows all populated sections
    Given a feature exists with value narrative, acceptance condition, system context, and assigned stories
    When the developer views that feature's detail page
    Then the feature name and status appear at the top of the view
    And the value narrative, acceptance condition, and system context sections are all visible
    And a list of stories assigned to the feature appears

  Scenario: Optional sections are absent when feature data is empty
    Given a feature exists with only a name and status and no optional fields populated
    When the developer views that feature's detail page
    Then no empty placeholder sections appear for the missing fields

  Scenario: Developer navigates from feature detail to a story view
    Given the developer is viewing a feature detail page with at least one story listed
    When the developer clicks a story row
    Then the page navigates to the story detail view
    And the URL updates to reflect the story being viewed

  Scenario: Developer returns to dashboard from feature detail
    Given the developer is viewing a feature detail page
    When the developer clicks the Dashboard segment in the breadcrumb
    Then the page returns to the main dashboard view
    And the breadcrumb resets to show only the dashboard as the active segment
