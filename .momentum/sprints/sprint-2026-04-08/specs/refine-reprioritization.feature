Feature: Refine Reprioritization — Add Priority Change Phase to Backlog Refinement

  Background:
    Given a Momentum project with a populated backlog and at least one completed sprint retro

  Scenario: Refine surfaces heuristic-grounded priority recommendations before consolidated findings
    Given the developer invokes the refine skill
    And stale-story evaluation has completed
    When the re-prioritization step runs
    Then the skill presents priority change recommendations grounded in recurrence, workaround burden, forgetting risk, and dependency chain analysis
    And each recommendation includes a rationale citing the specific evidence that drove it

  Scenario: Developer shapes final priority changes through back-and-forth conversation
    Given the refine skill has presented its initial priority recommendations
    When the developer redirects or refines the recommendations during the conversation
    Then the skill adapts its recommendations to reflect the developer's stated goals
    And the conversation continues until the developer signals satisfaction with the proposed changes

  Scenario: Agreed priority changes flow into consolidated findings and are applied via CLI
    Given the developer has approved a set of priority changes through the re-prioritization conversation
    When the refine skill reaches the apply approved changes step
    Then each agreed priority change is applied using the momentum-tools set-priority command
    And the final summary reflects the before-and-after priority distribution including the changes
