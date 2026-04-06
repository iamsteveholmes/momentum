Feature: Refine Skill — Backlog Grooming with PM and Architect

  Background:
    Given the momentum plugin is installed and available
    And the project has an active backlog with stories across multiple epics

  Scenario: Invoking the refine skill displays a prioritized backlog
    When the developer invokes the refine skill
    Then the output displays a list of backlog stories
    And each story shows a priority indicator of [C], [H], [M], or [L]
    And stories are grouped by epic
    And within each group stories are sorted from highest to lowest priority
    And each story shows whether its dependencies are met or blocked

  Scenario: Discovery agents identify coverage gaps from PRD and architecture
    When the developer invokes the refine skill
    Then the skill launches PRD coverage discovery and architecture coverage discovery
    And both discovery processes complete before findings are presented
    And the output presents a consolidated findings section

  Scenario: Developer can approve or reject each finding individually
    When the developer invokes the refine skill
    And findings are presented after discovery completes
    Then each finding is presented as a discrete item requiring a decision
    And the developer can approve a finding to apply the suggested change
    And the developer can reject a finding to leave the story unchanged
    And the skill does not apply any change that was not explicitly approved

  Scenario: Approved priority change is reflected in the backlog
    Given a finding suggests changing a story's priority from low to high
    When the developer approves the priority change for that story
    Then the story's priority indicator shows [H] when the backlog is displayed again

  Scenario: Approved epic reassignment moves the story to the correct epic
    Given a finding suggests a story belongs in a different epic
    When the developer approves the epic reassignment for that story
    Then the story appears under the newly assigned epic in subsequent backlog views

  Scenario: Dependency issues are flagged for manual resolution
    Given a finding identifies a dependency ordering conflict between two stories
    When the developer invokes the refine skill
    Then the dependency conflict is presented as a finding
    And the output indicates that dependency resolution requires manual action
    And no automatic dependency change is applied

  Scenario: New stories identified during grooming are created via delegation
    Given a finding identifies a gap requiring a new story
    When the developer approves the creation of the new story
    Then a new story entry appears in the backlog on the next invocation
    And the new story has a priority and epic assignment consistent with the suggestion

  Scenario: All decisions are logged and a summary is presented at session end
    When the developer invokes the refine skill
    And the developer makes approval and rejection decisions across multiple findings
    Then after all decisions are processed the skill presents a session summary
    And the summary lists the changes applied and findings rejected

  Scenario: Refine skill is independently invocable without prior setup
    When the developer invokes the refine skill in a project with an existing backlog
    Then the skill starts, runs discovery, and presents findings without errors
