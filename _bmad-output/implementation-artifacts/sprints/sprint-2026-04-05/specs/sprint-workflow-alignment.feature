Feature: Sprint Workflow Alignment — Fix Slug Extraction and Status Transitions

  Sprint-dev must extract the sprint slug from the active sprint object
  (not treat it as a plain string), and sprint-planning must transition
  through "ready" status before activating a sprint.

  Scenario: Sprint-dev extracts the sprint slug from the active sprint object
    Given a sprints/index.json where active is an object with a slug property
    When sprint-dev reads the active sprint
    Then sprint-dev uses the slug from active.slug as the current sprint identifier

  Scenario: Sprint-dev halts when the active sprint status is not active
    Given a sprints/index.json where active.status is "planning"
    When sprint-dev attempts to start execution
    Then sprint-dev halts with a message explaining the sprint is not in active status

  Scenario: Sprint-planning transitions through ready before activating
    Given a sprint in planning status
    When sprint-planning runs its activation sequence
    Then the sprint status is set to "ready" before it is set to "active"

  Scenario: Sprint-planning produces the full planning-ready-active lifecycle
    Given a newly created sprint in planning status
    When sprint-planning completes the activation sequence
    Then the sprint transitions through planning then ready then active in order
