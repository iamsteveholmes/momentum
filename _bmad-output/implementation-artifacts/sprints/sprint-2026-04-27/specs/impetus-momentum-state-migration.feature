Feature: Migrate Impetus State Reads to .momentum/

  Background:
    Given the project state has been relocated under .momentum/ as the canonical source

  Scenario: Developer opens a fresh session and Impetus orients against .momentum/ state
    Given .momentum/sprints/index.json and .momentum/stories/index.json hold the current sprint and story state
    And .momentum/signals/ is empty
    When the developer opens a fresh Claude session in the project
    Then Impetus produces a situational report naming the active sprint and outstanding stories that matches the recorded state
    And the orientation completes without error
    And no warning about missing or empty signals appears

  Scenario: Developer inspects sprint state and momentum-tools reports from .momentum/
    Given the developer has not modified sprint or story state since the relocation
    When the developer runs momentum-tools sprint show
    Then the command reports the same active and planning sprints that were recorded before the relocation
    And the command exits successfully

  Scenario: Developer plans a new sprint and the resulting state lands under .momentum/
    Given the developer has approved a set of stories for a new sprint
    When the developer runs sprint planning to activate the sprint
    Then .momentum/sprints/index.json reflects the newly activated sprint
    And .momentum/stories/index.json reflects the updated status of the included stories
    And no sprint or story state appears under _bmad-output/implementation-artifacts/

  Scenario: Developer searches the project and the legacy state directories are absent
    Given the relocation has completed
    When the developer lists the contents of _bmad-output/implementation-artifacts/
    Then no sprints directory is present at that location
    And no stories directory is present at that location
    And no intake-queue file is present at that location

  Scenario: Developer opens a session with no signals recorded and orientation completes cleanly
    Given .momentum/signals/ exists and contains no signal files
    When the developer opens a fresh Claude session in the project
    Then Impetus completes orientation without error
    And the situational report contains no signal-related warnings or notices
