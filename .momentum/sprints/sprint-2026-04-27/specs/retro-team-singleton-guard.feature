Feature: Retro Team Singleton Guard — Enforce Exactly-One Spawning for Documenter and Auditor Roles

  Background:
    Given the developer has invoked the retro skill on a target sprint

  Scenario: Retro proceeds silently when the spawned team has the intended composition
    Given the retro spawns a team containing one documenter and one each of auditor-human, auditor-execution, and auditor-review
    When the retro reaches the point where the team begins its analysis
    Then the retro continues without halting
    And the auditor team performs its analysis
    And the findings document is written for the target sprint

  Scenario: Retro halts loudly when the spawned team contains duplicate documenters
    Given the retro spawns a team containing multiple documenters alongside the three auditor roles
    When the retro reaches the point where the team would begin its analysis
    Then the retro halts before any auditor performs analysis
    And a diagnostic appears naming the expected composition of one documenter and three distinct auditors
    And the diagnostic reports the actual per-role tally of the spawned team
    And no findings document is written for the target sprint

  Scenario: Retro halts loudly when the spawned team is missing an auditor role
    Given the retro spawns a team that is missing one of the three required auditor roles
    When the retro reaches the point where the team would begin its analysis
    Then the retro halts before any auditor performs analysis
    And a diagnostic appears naming the missing role
    And the developer is not offered a path to continue with the incomplete team
