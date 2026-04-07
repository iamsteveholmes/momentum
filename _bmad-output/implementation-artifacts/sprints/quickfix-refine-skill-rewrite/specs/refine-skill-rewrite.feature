Feature: Refine Skill Rewrite — Practical Backlog Hygiene over Gap Analysis

  Background:
    Given a Momentum project with a populated backlog and planning artifacts

  Scenario: Planning artifact discovery skips update when no gaps are found
    Given the PRD and architecture documents are current with the completed stories
    When the developer invokes momentum:refine
    Then planning artifact discovery runs and reports no required updates
    And the workflow proceeds to status hygiene without requesting document changes

  Scenario: Developer approves planning artifact changes before updates are applied
    Given the PRD has requirements that no longer reflect completed work
    When the developer invokes momentum:refine
    Then a summary of proposed PRD changes is presented for review
    And the workflow waits for the developer to approve before applying any updates
    And the PRD is updated only after approval is given

  Scenario: Planning artifact updates run in parallel when both documents have gaps
    Given the PRD has outdated requirements and the architecture has stale decisions
    When the developer invokes momentum:refine and approves the findings
    Then both the PRD and architecture documents are updated before the workflow continues
    And the workflow does not require sequential approval for each document separately

  Scenario: Status hygiene flags completed stories still showing as in-progress
    Given a story file exists where all checklist items are checked
    And the story's status in the backlog index is not done
    When the developer invokes momentum:refine
    Then the story is presented as a status mismatch
    And the developer is offered a transition to mark it done
    And the transition is applied via the momentum-tools CLI

  Scenario: Small finding sets are presented for individual review
    Given the backlog has fewer than five total findings across all categories
    When the developer invokes momentum:refine
    Then each finding is presented individually
    And the developer can accept, modify, or reject each one before the next appears

  Scenario: Large finding sets are presented with batch approval options
    Given the backlog has five or more findings across several categories
    When the developer invokes momentum:refine
    Then findings are grouped by category in the presentation
    And the developer is offered the option to approve or reject an entire category at once
    And the developer can also approve a numbered range within a category
    And individual review of each finding remains available as a fallback

  Scenario: Stale backlog stories receive individual keep-or-drop recommendations
    Given several stories exist with low priority, no story file, and backlog status
    When the developer invokes momentum:refine
    Then each candidate stale story is evaluated with a keep or drop recommendation and rationale
    And no story is dropped without the developer reviewing and confirming the recommendation

  Scenario: Epic analysis is delegated rather than performed inline
    Given the backlog contains epics with overlapping scope
    When the developer invokes momentum:refine
    Then epic-level structural analysis is performed by a separate grooming step
    And the refine workflow does not produce its own epic deduplication output

  Scenario: Epic grooming step is skipped gracefully when the skill does not exist
    Given the momentum:epic-grooming skill is not installed
    When the developer invokes momentum:refine
    Then the workflow notifies the developer that epic grooming is unavailable
    And the workflow continues with remaining steps without failing

  Scenario: No dependency analysis findings appear in the output
    Given the backlog contains stories with declared dependencies
    When the developer invokes momentum:refine
    Then no circular dependency warnings are produced
    And no missing dependency target findings are produced
    And no satisfied dependency findings are produced

  Scenario: Approved changes are applied through CLI commands without direct file edits
    Given the developer has approved a set of status transitions and story drops
    When the workflow applies the changes
    Then status updates are performed via momentum-tools sprint status-transition
    And the workflow does not directly modify the backlog index file
    And a summary of applied changes and rejected findings is presented afterward
