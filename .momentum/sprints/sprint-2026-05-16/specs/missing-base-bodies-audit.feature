Feature: Missing Base Bodies Audit — Verify DEC-020 Universal Agent Role Coverage

  Background:
    Given the agents directory contains the current set of agent definition files
    And the stories index contains the current set of tracked stories

  Scenario: Audit produces a gap report covering all nine required roles
    Given the nine canonical roles required by DEC-020 are architect, pm, ux, analyst, researcher, dev, sm, qa, and e2e
    When the developer runs the missing base bodies audit
    Then the gap report lists every one of the nine canonical roles
    And each role is classified as either covered by an existing file or tracked by a story

  Scenario: Roles with existing agent files are reported as covered
    Given agent definition files exist for the dev, e2e, and qa roles
    When the developer runs the missing base bodies audit
    Then the gap report marks dev, e2e, and qa as covered
    And no story lookup is required for those roles

  Scenario: Roles without agent files are confirmed as tracked in the stories index
    Given no agent definition file exists for architect, pm, ux, analyst, researcher, or sm
    When the developer runs the missing base bodies audit
    Then the gap report lists each missing role alongside its tracked story slug
    And none of those roles appear as untracked

  Scenario: Audit closes with zero untracked gaps
    Given every role without an agent file has a corresponding story in the stories index
    When the developer runs the missing base bodies audit
    Then the gap report shows an untracked gap count of zero
    And the story status advances to done

  Scenario: Untracked role triggers an intake stub before the audit closes
    Given at least one canonical role has no agent file and no entry in the stories index
    When the developer runs the missing base bodies audit
    Then the gap report flags the untracked role
    And an intake stub story is created for that role before the audit closes
