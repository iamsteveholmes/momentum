Feature: Build the /momentum:feature-breakdown Skill — Feature → Gap List → Triage

  Background:
    Given the developer has a Momentum project with a populated features.json

  Scenario: Developer receives a triaged set of outcomes after invoking feature-breakdown with a valid slug
    Given a feature slug exists in features.json with defined acceptance conditions and stories
    And the momentum:triage skill is available
    When the developer invokes /momentum:feature-breakdown with that slug
    And the developer approves the synthesized gap list at the review gate
    Then triage runs against the approved items and returns classified outcomes
    And the developer sees a final report naming the feature slug, total gap count, classification breakdown, and pointers to any new artifacts

  Scenario: Skill fails fast when the feature slug is not found
    Given the developer provides a slug that does not exist in features.json
    When the developer invokes /momentum:feature-breakdown with that slug
    Then the skill exits immediately with an error naming the missing slug
    And the error suggests running /momentum:feature-grooming to view available slugs

  Scenario: Developer removes items at the review gate before delegation
    Given a feature slug exists in features.json
    And the momentum:triage skill is available
    When the developer invokes /momentum:feature-breakdown with that slug
    And the developer removes one or more items from the gap list at the review gate
    Then triage runs only against the remaining approved items
    And the final report reflects the reduced item count

  Scenario: Workflow exits cleanly when developer removes every gap item
    Given a feature slug exists in features.json
    And the momentum:triage skill is available
    When the developer invokes /momentum:feature-breakdown with that slug
    And the developer removes every item from the gap list at the review gate
    Then the skill exits without invoking triage
    And the output states that no gaps were submitted for triage

  Scenario: Optional focus hint narrows the gap list the developer sees
    Given a feature slug exists in features.json
    And the momentum:triage skill is available
    When the developer invokes /momentum:feature-breakdown with that slug and a focus hint
    Then the gap list presented at the review gate is narrowed toward items relevant to the focus hint
    And the developer can proceed to approval or removal as normal

  Scenario: Skill fails fast when triage is unavailable
    Given a feature slug exists in features.json
    And the momentum:triage skill is unavailable
    When the developer invokes /momentum:feature-breakdown with that slug
    And the developer approves the gap list at the review gate
    Then the skill exits with a clear error naming momentum:triage as the missing dependency
