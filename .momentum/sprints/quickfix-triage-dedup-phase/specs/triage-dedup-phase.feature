Feature: Triage dedup phase — deterministic prefilter + cluster fan-out + per-theme findings

  Background:
    Given the momentum project has a populated stories backlog with at least 10 active stories
    And at least 5 open items are waiting in the intake queue

  Scenario: Prefilter tool produces ranked candidates and similarity matrix for a batch of items
    Given a batch of 3 incoming items with titles and descriptions covering distinct topics
    When the developer runs the triage prefilter command against the stories index
    Then each incoming item receives a ranked list of up to 10 candidate stories
    And each candidate entry includes a combined score and individual score components
    And an intra-batch similarity matrix is output covering all item pairs

  Scenario: Prefilter excludes terminal-status stories from candidates
    Given the stories index contains stories in done, dropped, and closed-incomplete status
    And those stories share keywords with an incoming item
    When the developer runs the triage prefilter command for that item
    Then none of the terminal-status stories appear in the candidate list
    And only active stories appear as candidates

  Scenario: Developer sees dedup findings and approves actions before classifying survivors
    Given the developer invokes momentum:triage with a batch of items
    And at least one incoming item closely resembles an existing backlog story
    When triage presents its approval output
    Then the output includes a dedup actions section grouping findings by recommended action
    And items with multiple distinct themes appear in a split candidates section
    And any consolidation groups involving multiple items appear in a merge candidates section labeled as deferred
    And the existing classification section follows for items that survive the dedup review

  Scenario: Duplicate items are consumed from the queue after developer approves dedup actions
    Given the developer invokes momentum:triage with a batch that includes a known duplicate item
    When the developer approves the duplicate finding in the dedup actions section
    Then the duplicate item is marked as consumed in the intake queue
    And the remaining non-duplicate items proceed to the five-class classification step

  Scenario: A multi-theme item surfaces as a split candidate with two separate findings
    Given an incoming item whose description covers two clearly distinct concerns
    When the developer invokes momentum:triage with that item in the batch
    Then the dedup output shows two separate findings for that item, one per theme
    And the item appears in the split candidates section of the approval output

  Scenario: A single-item triage batch completes without clustering errors
    Given only one open item is present in the intake queue
    When the developer invokes momentum:triage for that single item
    Then triage completes successfully and presents dedup findings for the item
    And the approval output contains the dedup actions section with at least one finding
    And the item proceeds to classification after the developer reviews findings

  Scenario: Prefilter correctly identifies known near-duplicate items in its top candidates
    Given the stories index contains a story whose title and description closely paraphrase an incoming item
    When the developer runs the triage prefilter command for that incoming item
    Then the closely matching story appears in the top 10 candidates for that item
