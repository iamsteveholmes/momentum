Feature: Fix retro documenter replication defect (AC4 regression)

  Background:
    Given a sprint has prepared audit extracts available for retrospective

  Scenario: Developer sees exactly one documenter and three distinct auditors after running retro
    Given the developer has a sprint ready for retrospective
    When the developer runs the retro end to end
    Then exactly one documenter agent produces the retro transcript audit
    And exactly three distinct auditor agents run, one each for human, execution, and review
    And every spawned agent in the retro session has a unique identifier with no shared identifier across agents

  Scenario: Rerunning retro on a previously affected sprint produces four agents instead of seventeen
    Given the developer points retro at the sprint that previously spawned seventeen agents
    When the developer reruns the retrospective against that sprint's archived audit extracts
    Then the retrospective spawns exactly four agents in total
    And no two spawned agents produce identical content from a shared single invocation

  Scenario: Retro produces a complete findings document with the documenter as sole author
    Given the developer runs retro against a sprint with auditor findings to collate
    When the retrospective completes
    Then a single retro transcript audit file is written for the sprint
    And the file contains the executive summary, what worked well, what struggled, user interventions, story-by-story analysis, cross-cutting patterns, metrics, and priority action items sections
    And no duplicate retro transcript audit files exist for the sprint
