Feature: Momentum Cycle — Story L3 Drill-Down (Reading Mode)

  Background:
    Given the Momentum Cycle dashboard is running at http://localhost:3456
    And at least one story file exists in the stories directory

  Scenario: Developer reads a story in the polished reading view
    Given the developer navigates to a story via the Features lens drill-down path
    When the developer navigates to the story detail view
    Then the page displays the story title, acceptance criteria, and available metadata
    And the page uses a warm light reading surface
    And the URL reflects the story being viewed

  Scenario: Long dev notes are collapsible
    Given a story has a dev notes section with more than three items or more than one paragraph
    When the developer views that story's detail page
    Then the dev notes section is initially collapsed behind an expand affordance
    And the developer can expand the section to read the full content

  Scenario: Breadcrumb reflects entry point when arriving from a feature
    Given the developer navigated to the story through a feature detail page
    When the developer arrives at the story detail view from a feature page
    Then the breadcrumb shows Feature and Dashboard as ancestor segments
    And Dashboard and Feature segments are clickable links

  Scenario: Breadcrumb reflects entry point when arriving from sprint detail
    Given the developer navigated to the story through a sprint detail page
    When the developer arrives at the story detail view from a sprint detail page
    Then the breadcrumb shows Sprint and Dashboard as ancestor segments
    And Dashboard and Sprint segments are clickable links

  Scenario: Unknown story slug shows a not-found message
    Given no story file exists for a given slug
    When the developer navigates to that story's URL
    Then a not-found message appears in the content area
    And the dashboard remains functional with no server error
