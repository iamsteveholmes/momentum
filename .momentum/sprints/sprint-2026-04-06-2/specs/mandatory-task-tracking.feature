Feature: Mandatory Task Tracking — Enforce TaskCreate in Long Sessions

  Background:
    Given a Momentum project with sprint-dev and sprint-planning workflows installed

  Scenario: Sprint-dev creates trackable tasks at session start
    When a user invokes the sprint-dev workflow
    Then the agent creates tasks for each workflow phase using TaskCreate
    And each task is queryable via TaskList

  Scenario: Sprint-dev updates task status as phases progress
    Given a sprint-dev session is running with tasks created
    When the agent begins a new phase
    Then the corresponding task is updated to in_progress
    When the agent completes that phase
    Then the corresponding task is updated to completed

  Scenario: Sprint-dev never relies on ad-hoc summaries for phase tracking
    Given a sprint-dev session has progressed past three phases
    When a user queries task status via TaskList
    Then all completed phases show as completed tasks
    And the active phase shows as an in_progress task
    And no phase status is communicated only through narrative text

  Scenario: Sprint-planning creates trackable tasks at session start
    When a user invokes the sprint-planning workflow
    Then the agent creates tasks for each workflow step using TaskCreate
    And each task is queryable via TaskList

  Scenario: Sprint-planning updates task status as steps progress
    Given a sprint-planning session is running with tasks created
    When the agent begins a new step
    Then the corresponding task is updated to in_progress
    When the agent completes that step
    Then the corresponding task is updated to completed

  Scenario: Sprint-planning never relies on ad-hoc summaries for step tracking
    Given a sprint-planning session has progressed past three steps
    When a user queries task status via TaskList
    Then all completed steps show as completed tasks
    And the active step shows as an in_progress task
    And no step status is communicated only through narrative text

  Scenario: Task tracking survives context compression in long sessions
    Given a sprint-dev session has been running long enough for context compression
    When a user queries task status via TaskList
    Then the task state accurately reflects which phases are completed and which remain
    And the agent does not lose track of progress due to compressed context

  Scenario: Task tracking is consistent across all tracked workflows
    Given a user has run sprint-dev, sprint-planning, and retro workflows
    When task status is queried during each workflow
    Then all three workflows use TaskCreate for initial task setup
    And all three workflows use TaskUpdate to transition tasks through states
