Feature: Intake Skill — Lightweight Story Capture from Conversation

  Background:
    Given the developer has a story idea from a current conversation

  Scenario: Developer captures a story idea into the backlog without running the full pipeline
    Given no active sprint or Impetus session is running
    When the developer invokes /momentum:intake with a title and conversational context
    Then a stub story file appears in the stories directory with status backlog
    And the stub file contains the captured title, description, user story, and rough acceptance criteria
    And every unpopulated section contains a visible draft marker indicating it requires create-story enrichment
    And a new entry appears in stories/index.json with status backlog, the assigned epic, and story_file true

  Scenario: Developer resolves a slug conflict before the story is saved
    Given a story with a slug derived from the intended title already exists in stories/index.json
    When the developer invokes /momentum:intake with that title
    Then the skill reports the slug conflict and prompts the developer for an alternative
    And no story file is written until the developer provides a non-conflicting title

  Scenario: Developer is prompted to assign an epic when none is determinable from context
    Given the developer provides a story title and description with no clear epic match
    When the developer invokes /momentum:intake
    Then the skill presents the available epics and asks the developer to choose
    And the story is not written to disk until an epic is assigned
