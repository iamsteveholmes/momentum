Feature: Routing Table Schema and Implementation

  Background:
    Given the Momentum plugin is installed
    And the agents registry file exists with a defaults block and a project array

  Scenario: Agent registry ships with all nine universal roles in the defaults block
    Given the agents registry has been installed with the plugin
    When the developer inspects the defaults block
    Then it contains entries for architect, pm, ux, analyst, researcher, dev, sm, qa-reviewer, and e2e-validator
    And each entry points to the corresponding agent body file path for that role

  Scenario: Agent registry ships with an empty project array before any composition has run
    Given no project has yet run build-agents
    When the developer inspects the project section of the agents registry
    Then the project array is empty

  Scenario: agent-resolve returns the matching project entry when a path matches a pattern
    Given the agents registry contains a project entry with glob patterns for a specific domain
    When the developer runs momentum-tools agent-resolve with a file path that matches one of those patterns
    Then the command exits successfully and the results include the slug and agent path from that project entry
    And the file path appears in the file scope for that result

  Scenario: agent-resolve falls back to the dev default when no project pattern matches
    Given the agents registry has no project entry whose patterns match the supplied file path
    When the developer runs momentum-tools agent-resolve with that file path
    Then the command exits successfully and the results include the default dev agent path
    And the unmatched file path appears in the file scope of that result

  Scenario: agent-resolve groups multiple paths into distinct results by matching agent
    Given the agents registry contains two project entries with non-overlapping patterns
    When the developer runs momentum-tools agent-resolve with paths that match each entry respectively
    Then the results array contains two objects
    And each object carries only the paths matched by its own patterns in the file scope

  Scenario: agent-resolve result entries include write permissions from the matched project entry
    Given a project entry in the agents registry specifies write permissions for a domain
    When the developer runs momentum-tools agent-resolve with a path that matches that entry
    Then the result for that entry includes the same write permissions
    And read-only roles resolved from the defaults block carry an empty write permissions list

  Scenario: agent-resolve supports role-based lookup for defaults block entries
    Given the agents registry defaults block contains entries for qa-reviewer and e2e-validator
    When the developer runs momentum-tools agent-resolve with a role flag for one of those roles
    Then the command exits successfully and returns the agent path from the defaults block for that role

  Scenario: sprint-dev resolves agents from the routing table during the dev wave
    Given a story has a touches list of file paths
    When sprint-dev processes that story in the dev wave
    Then it runs agent-resolve with the story's touched paths and spawns one agent per result group returned
    And each spawned agent is scoped to the file subset assigned to its group

  Scenario: sprint-dev spawns multiple agents for a story touching multiple domains
    Given the agents registry has project entries for two distinct domains
    And a story touches files that match both domains
    When sprint-dev processes that story
    Then two agents are spawned, each scoped to its matched domain's files and write permissions

  Scenario: sprint-dev falls back to the default dev agent when an agent path does not exist on disk
    Given agent-resolve returns an agent path for a result group
    And that path does not correspond to an existing file
    When sprint-dev processes the story
    Then a warning is surfaced and the default dev agent is used for that group instead

  Scenario: sprint-dev team review agents are resolved from the routing table defaults block
    Given the agents registry defaults block contains entries for qa-reviewer and e2e-validator
    When sprint-dev reaches the team review phase
    Then the qa-reviewer agent path is sourced from the defaults block lookup
    And the e2e-validator agent path is sourced from the defaults block lookup

  Scenario: agent-builder writes only to the project array without altering the defaults block
    Given the agents registry has an established defaults block
    When agent-builder produces a composed agent file and the developer approves it
    Then a new entry appears in the project array for that role and domain
    And the defaults block is unchanged
