Feature: Refine Workflow — Assessment & Decision Review Step

  Background:
    Given the developer has run backlog refinement at least once before

  Scenario: Stale and unacted-on assessments surface in consolidated findings
    Given assessments exist in the planning artifacts directory
    And at least one assessment is older than 30 days with status "current"
    And at least one assessment has an empty decisions_produced list
    When the developer runs the refine workflow
    Then consolidated findings include an "Assessment & decision review" category
    And each stale assessment appears with its age in days
    And each assessment with no decisions produced is flagged as having unacted-on findings

  Scenario: Unresolved assessment next steps surface when no decision or story exists
    Given an assessment with status "current" has recommended next steps
    And no decision document references that assessment
    And no backlog story corresponds to those next steps
    When the developer runs the refine workflow
    Then the unresolved next steps appear in consolidated findings
    And the developer can approve creation of a story to address them

  Scenario: Decisions referencing missing stories surface in consolidated findings
    Given a decision document lists stories in its stories_affected field
    And one or more of those stories do not exist in the backlog
    When the developer runs the refine workflow
    Then consolidated findings include entries for each missing story
    And each entry identifies the decision and describes the missing story

  Scenario: Decision gates that appear ready for review surface to the developer
    Given a decision document has gates with timing conditions
    And the stories referenced by a gate's condition are all in "done" status
    When the developer runs the refine workflow
    Then that gate appears in consolidated findings as ready for review
    And the gate's criteria are displayed so the developer can evaluate

  Scenario: Assessment and decision findings participate in batch approval
    Given consolidated findings include assessment and decision entries
    When the developer reviews findings and approves an entry for story creation
    Then the refine workflow delegates new story creation to the create-story skill
    And the approved finding is resolved without the developer manually invoking any secondary command
