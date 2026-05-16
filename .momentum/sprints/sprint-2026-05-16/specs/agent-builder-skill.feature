Feature: agent-builder — Per-Agent Composition Skill

  Background:
    Given the Momentum plugin is installed
    And the developer has a valid base body file, a constitution excerpt, and role × domain manifesto inputs

  Scenario: Developer receives a composed agent file after invoking agent-builder
    Given the developer provides a base body path, a constitution excerpt, and manifesto inputs for a role and domain
    When the developer invokes momentum:agent-builder with those three inputs
    Then a composed agent file appears at the path derived from the role and domain
    And the file contains content drawn from the base body, the constitution excerpt, and the domain manifesto

  Scenario: Composed agent file meets structural conventions
    Given the developer provides valid inputs for a role and domain
    When the developer invokes momentum:agent-builder and approves the output
    Then the composed agent file includes a frontmatter block with name, description, model, effort, and tools
    And the file includes a large file handling section
    And the file body is under 200 lines

  Scenario: Developer is presented an approval gate before the routing entry is written
    Given agent-builder has completed its autonomous composition loop
    When the composed file and evaluation summary are surfaced to the developer
    Then the developer sees options to approve, request a revision, or abort
    And no routing entry exists in the agents registry until the developer approves

  Scenario: Developer aborts and no routing entry is written
    Given the approval gate is presented with the composed file and eval summary
    When the developer chooses to abort
    Then no routing entry for that role and domain appears in the agents registry
    And no composed file is committed

  Scenario: Developer requests a revision and the gate re-presents
    Given the approval gate is presented with the composed file and eval summary
    When the developer requests a revision with specific feedback
    Then agent-builder runs one improvement pass and surfaces the updated output again
    And the developer is again offered the option to approve, revise, or abort

  Scenario: Routing entry is written to the agents registry on approval
    Given the developer has approved the composed output for a role and domain
    When agent-builder finalizes the invocation
    Then the agents registry contains an entry for that role and domain with a slug, agent path, file patterns, and write permissions

  Scenario: Re-invoking for an existing slug updates the entry rather than duplicating it
    Given a routing entry already exists in the agents registry for a given role and domain slug
    When the developer invokes momentum:agent-builder again with the same role and domain
    And approves the new composed output
    Then the agents registry contains exactly one entry for that slug
    And the entry reflects the updated values

  Scenario: Newly created agents registry has the correct top-level structure
    Given the agents registry file does not yet exist on the project
    When agent-builder writes its first routing entry
    Then the agents registry is created with a defaults block and a project array
    And the project array contains exactly the one new entry

  Scenario: agent-builder scopes each invocation to a single role and domain pair
    Given the developer provides inputs for one role and one domain
    When the developer invokes momentum:agent-builder
    Then exactly one composed agent file is produced
    And exactly one routing entry is added or updated in the agents registry

  Scenario: agent-builder behaves identically whether invoked directly or by an orchestrating agent
    Given valid inputs for a role and domain are supplied
    When momentum:agent-builder is invoked by a developer directly
    Then the composed file, approval gate, and routing entry behavior are the same as when an orchestrating agent invokes it with the same inputs
