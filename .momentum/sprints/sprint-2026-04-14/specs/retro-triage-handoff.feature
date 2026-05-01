Feature: Retro findings feed next-sprint planning via the intake queue

  Background:
    Given a completed sprint has just had its retro run

  Scenario: Un-actioned retro findings become handoff entries in the intake queue
    Given the retro produced action items that the developer did not immediately distill or stub
    When the developer closes out the retro
    Then each un-actioned item is captured as a handoff entry in the intake queue
    And each entry records which sprint it originated from

  Scenario: Feature-state transitions observed in retro are recorded in the handoff
    Given the retro observed a feature regressing from a Done state back to Partial
    When the developer closes out the retro
    Then the handoff entry for the regression carries the prior state, the observed state, and supporting evidence

  Scenario: Diagnosed failures from retro are recorded in the handoff
    Given the retro named a failure with what was attempted, what did not work, and what was learned
    When the developer closes out the retro
    Then the handoff entry for the failure carries all three pieces of context

  Scenario: Sprint planning surfaces open handoff entries without manual injection
    Given open handoff entries exist from a prior retro
    When the developer starts a new sprint planning session
    Then the planning session presents those handoff entries as candidate context before asking for story selection
    And the developer does not need to re-describe those findings verbally

  Scenario: Retro does not gate handoff items on value or priority
    Given the retro identified findings of varying apparent importance
    When the developer closes out the retro
    Then every un-actioned finding is written to the queue without a pre-filter on value or priority

  Scenario: Handoff entries that have been acted on stop re-surfacing
    Given a handoff entry is currently open in the intake queue
    When the developer acts on that handoff entry in a subsequent session — by promoting it to a story, distilling it, capturing a decision, or explicitly rejecting it
    Then that handoff entry is marked consumed or rejected
    And subsequent triage and planning sessions do not surface it as an open item again
