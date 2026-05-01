Feature: Retire per-sprint JSON state file — align workflows, decision document, and architecture

  # Glossary (for outsider reading only this spec):
  #   "the holistic sprint state file"  = `.momentum/sprints/index.json` — a single canonical
  #                                       file with `active`, `planning`, `completed[]`,
  #                                       `quickfixes[]` sections. The retired pattern
  #                                       (this story's subject) is `.momentum/sprints/{slug}.json`,
  #                                       a per-sprint JSON file that the implementation has
  #                                       never written.

  # AC coverage map (story: fix-per-sprint-json-contract-drift)
  #   AC1 (sprint-dev Phase 1 reads holistic state) ........... covered by Scenario 1
  #   AC2 (wave ordering from active.waves)  ................... covered by Scenario 2
  #   AC3 (<critical> directive content) ....................... verified by inspection + AVFL (no scenario)
  #   AC4 (HALT message references holistic state) ............. covered by Scenario 3
  #   AC5 (sprint-manager removes 3 per-sprint write steps) .... covered by Scenarios 4, 5, 6
  #   AC6 (zero grep matches for sprints/{slug}.json) .......... verified by grep (no scenario)
  #   AC7 (DEC-012 well-formed) ................................ verified by inspection + AVFL (no scenario)
  #   AC8 (architecture.md updates in 3 sections) .............. verified by inspection + AVFL (no scenario)
  #   AC9 (architecture.md editHistory entry) .................. verified by inspection (no scenario)
  #   AC10 (DEC-012 referenced from all 4 enacting artifacts) .. verified by grep (no scenario)
  #   AC11 (behavioral evals in sprint-dev/evals/) ............. covered by EDD evals (separate from this spec)
  #   AC12 (format/NFR compliance across all 4 files) .......... verified by inspection (no scenario)
  #   AC13 (AVFL checkpoint passes) ............................ meta-AC; verified by AVFL run itself

  Background:
    Given the holistic sprint state file is the only sprint state source on disk
    And no per-sprint JSON state file exists for any sprint

  Scenario: sprint-dev orients against the active sprint without a per-sprint state file
    Given an active sprint is recorded in the holistic sprint state file
    When the developer invokes momentum:sprint-dev
    Then sprint-dev identifies the active sprint and proceeds past initialization
    And sprint-dev does not halt looking for a per-sprint state file

  Scenario: sprint-dev derives wave ordering from the active sprint's waves
    Given the active sprint declares two waves with the first wave containing one story and the second wave containing multiple stories
    When the developer invokes momentum:sprint-dev
    Then sprint-dev identifies the wave-one story as ready to start
    And sprint-dev treats the wave-two stories as blocked until the wave-one story reaches done

  Scenario: sprint-dev fails with an actionable diagnostic when the active sprint slug does not match the requested sprint
    Given the holistic sprint state file's active block names a different sprint than the one requested
    When the developer invokes momentum:sprint-dev for a non-active sprint
    Then sprint-dev halts with a message that names the holistic sprint state file as the source to inspect
    And the message does not direct the developer to look for a per-sprint state file

  Scenario: sprint-manager activates a sprint against the holistic state file
    Given a planned sprint exists in the holistic sprint state file with no currently active sprint
    When the developer invokes momentum:sprint-manager to activate the planned sprint
    Then sprint-manager returns a success result
    And the holistic sprint state file shows the sprint in its active block
    And no per-sprint state file is created on disk

  Scenario: sprint-manager completes a sprint against the holistic state file
    Given an active sprint exists in the holistic sprint state file
    When the developer invokes momentum:sprint-manager to complete the active sprint
    Then sprint-manager returns a success result
    And the holistic sprint state file moves the sprint into its completed list with a completion date
    And no per-sprint state file is created on disk

  Scenario: sprint-manager records a sprint plan against the holistic state file
    Given the developer has a set of stories to plan into a new sprint
    When the developer invokes momentum:sprint-manager to record the sprint plan
    Then sprint-manager returns a success result
    And the holistic sprint state file shows the planned sprint in its planning block
    And no per-sprint state file is created on disk
