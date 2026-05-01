Feature: Orchestrator Deduplication Guard — Track Spawned Agents by (Story, Role)

  Scenario: Duplicate agent spawn is suppressed for same story and role
    Given a sprint execution with story "refine-skill" assigned to a dev agent
    When the orchestrator re-enters the dev wave for unblocked stories
    Then no second dev agent is spawned for "refine-skill"
    And the sprint event log contains a decision entry noting the suppressed spawn

  Scenario: Newly unblocked stories receive agents after re-entry
    Given a sprint execution where "auth-module" was blocked and has no agent
    And "auth-module" becomes unblocked after a dependency completes
    When the orchestrator re-enters the dev wave for unblocked stories
    Then a dev agent is spawned for "auth-module"

  Scenario: Failed agent can be retried without being blocked by dedup
    Given a sprint execution where the dev agent for "refine-skill" has failed
    When the orchestrator retries the dev agent for "refine-skill"
    Then a new dev agent is spawned for "refine-skill"
    And no duplicate suppression is logged for "refine-skill"

  Scenario: Team review agents are spawned at most once per sprint
    Given a sprint execution that has already spawned a QA reviewer
    When the orchestrator attempts to spawn a second QA reviewer
    Then no second QA reviewer is spawned
    And the sprint event log contains a decision entry noting the suppressed spawn
