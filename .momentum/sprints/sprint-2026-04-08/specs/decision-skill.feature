Feature: Decision Skill — Capture Strategic Decisions from Assessments

  Background:
    Given the developer has a Momentum project with an existing backlog

  Scenario: Developer captures decisions from an assessment report
    Given an assessment report (ASR) exists with findings and recommendations
    When the developer invokes momentum:decision with the ASR as source
    Then the skill walks through each finding in the ASR
    And for each finding, the developer can choose to adopt, reject, defer, or adapt the recommendation
    And the skill records the developer's decision and rationale for each finding

  Scenario: Developer captures decisions from a research document
    Given a research document exists with recommendations
    When the developer invokes momentum:decision with the research document as source
    Then the skill extracts the recommendations from the research document
    And for each recommendation, the developer can choose to adopt, reject, or defer it
    And the skill records the developer's choice and rationale for each

  Scenario: Developer re-evaluates a prior decision
    Given an existing SDR document is present in the decisions directory
    When the developer invokes momentum:decision to revisit that SDR
    Then the skill checks whether conditions specified in the decision gates have changed
    And walks the developer through re-evaluating each original decision in light of new information

  Scenario: Completed SDR is written and linked to its sources
    Given the developer has walked through decisions from an ASR source
    When the skill finishes capturing all decisions
    Then a new SDR document is written to the decisions directory
    And the SDR includes each decision's recommendation, the developer's choice, and the rationale
    And the SDR frontmatter lists the source documents and any affected backlog stories
    And the source ASR's frontmatter is updated to reference the new SDR
    And the decisions index is updated with the new entry

  Scenario: Developer proceeds to story creation after capturing decisions
    Given a new SDR has been written with decisions that imply new work
    When the skill offers to create stories for those decisions
    And the developer accepts
    Then the skill invokes momentum:create-story for each decision that implies new work
