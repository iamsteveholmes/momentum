Feature: Dev Agent Definition Files — Lightweight Agent for Sprint-Dev Spawning

  Background:
    Given a sprint with unblocked stories ready for implementation
    And the sprint-dev workflow is executing Phase 2

  Scenario: Dev agent accepts a story and sprint context as input
    Given a story file path and sprint slug are provided to the dev agent
    When the dev agent is spawned
    Then it reads the story file to understand what to implement
    And it proceeds with implementation without requesting additional input

  Scenario: Dev agent delegates implementation to bmad-dev-story
    Given the dev agent has received a story file path
    When the agent begins implementation
    Then it delegates the story execution to the bmad-dev-story skill
    And it does not perform story selection, worktree management, or merge operations

  Scenario: Dev agent returns structured completion output
    Given the dev agent has finished implementing a story
    When implementation is complete
    Then it returns structured output containing status, files changed, story key, and test results
    And the output format matches the subagent completion contract expected by sprint-dev

  Scenario: Sprint-dev spawns the dev agent via the Agent tool
    Given Phase 2 of sprint-dev is processing an unblocked story
    When a dev agent is launched for that story
    Then it is spawned via the Agent tool using the dev agent definition file
    And it receives story file path, sprint slug, role, and optional guidelines as input

  Scenario: Direct invocation of momentum:dev skill continues to work
    Given a developer invokes the momentum:dev skill directly
    When the skill is executed
    Then it completes its full workflow without errors
    And no behavior change is observed compared to before this story

  Scenario: Dev agent definition follows established agent schema
    Given the dev agent definition file exists
    When its structure is inspected
    Then it has frontmatter with name, description, model, effort, and tools
    And it contains a role description, critical constraints, input format, process steps, and output format section
