Feature: Feature Status Practice Path — Skill Topology and SDLC Coverage Map for Momentum

  Background:
    Given the Momentum project directory with installed skills

  Scenario: Developer sees skill topology and SDLC coverage when running on a practice project
    When the developer invokes momentum:feature-status on the Momentum project
    Then the output includes a topology showing how skills hand off to each other
    And the output includes a table mapping SDLC phases to covering skills

  Scenario: SDLC phases with no skill coverage are flagged
    When the developer invokes momentum:feature-status on the Momentum project
    Then any SDLC phase with no covering skill is labeled as a gap in the coverage table

  Scenario: Practice path output is concise enough to read in under ten seconds
    When the developer invokes momentum:feature-status on the Momentum project
    Then the practice-path section of the output is forty lines or fewer

  Scenario: A newly added skill appears in the topology without any manual update
    Given a new skill directory with a SKILL.md has been added to the project
    When the developer invokes momentum:feature-status
    Then the new skill appears in the skill topology output

  Scenario: Product project rendering is unaffected by the practice path addition
    Given a product project with no installed skills directory
    When the developer invokes momentum:feature-status
    Then the output shows feature type groups with status and gap analysis
    And no skill topology or SDLC coverage table appears in the output
