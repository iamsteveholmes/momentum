Feature: Retro Skill — Sprint Retrospective with Cross-Log Discovery and Sprint Closure

  Background:
    Given a completed sprint exists with agent log files in the sprint-logs directory

  Scenario: Retro identifies the most recent completed sprint for review
    Given two sprints are completed and one has not had a retro
    When the developer invokes /momentum:retro
    Then the sprint without a retro is identified and presented for confirmation

  Scenario: Retro correlates events across multiple agent logs
    Given the sprint has log files from three different agents
    When the retro runs cross-log discovery
    Then the developer sees a unified timeline with events from all agents ordered by timestamp

  Scenario: Stories not at done status are flagged for developer decision
    Given one story in the sprint has status "in-progress"
    When the retro verifies story completion
    Then the developer is warned about the incomplete story
    And the developer can choose to force-close it as closed-incomplete

  Scenario: Retro produces Momentum triage output with practice improvements
    When the retro completes cross-log discovery
    Then a Momentum triage report is written to the sprint directory
    And it contains practice improvement recommendations based on log patterns

  Scenario: Retro produces Project triage output with code and spec findings
    When the retro completes cross-log discovery
    Then a Project triage report is written to the sprint directory
    And it contains project-specific findings about code or spec gaps

  Scenario: Developer approves story stubs created from findings
    Given the retro has identified actionable findings
    When the retro proposes story stubs for the backlog
    Then each stub is presented to the developer for approval before creation

  Scenario: Sprint is marked complete after retro finishes
    Given all stories are verified and triage outputs are written
    When the developer confirms sprint closure
    Then the sprint status transitions to complete
    And the retro completion timestamp is recorded
