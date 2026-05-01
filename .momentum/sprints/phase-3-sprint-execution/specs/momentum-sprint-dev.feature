Feature: Sprint Dev — Dependency-Driven Execution Loop

  The sprint-dev workflow is Impetus's core execution loop. It reads an activated
  sprint, spawns momentum-dev agents for unblocked stories, tracks progress via
  tasks, handles dependency-driven sequencing, runs post-merge AVFL, executes
  black-box verification, and surfaces a sprint summary.

  Background:
    Given an active sprint exists in sprints/index.json with locked = true
    And the sprint contains team composition and dependency graph
    And stories/index.json contains entries for all sprint stories
    And momentum-tools log subcommand is available

  # --- Initialization ---

  Scenario: Sprint-dev loads from session menu
    Given the developer is at the Mode 1 session menu
    When the developer selects "Continue sprint"
    Then Impetus loads the sprint-dev workflow module
    And reads the active sprint record from sprints/index.json

  Scenario: Sprint validation rejects inactive sprint
    Given no active sprint exists in sprints/index.json
    When sprint-dev attempts to initialize
    Then an error is surfaced explaining no active sprint exists
    And Impetus returns to the session menu without spawning agents

  Scenario: Sprint validation rejects unlocked sprint
    Given an active sprint exists but locked = false
    When sprint-dev attempts to initialize
    Then an error is surfaced explaining the sprint was not properly activated
    And Impetus returns to the session menu

  Scenario: Task list created for all sprint stories
    Given an active sprint with 5 stories
    When sprint-dev initializes
    Then a task is created for each story in the sprint
    And each task description includes the story's dependency list
    And all tasks start in pending status

  Scenario: Sprint start logged
    Given sprint-dev initializes successfully
    Then a log entry is written via momentum-tools log
    And the log entry has agent "impetus" and event "decision"
    And the detail includes the story count and unblocked count

  # --- Team Spawn ---

  Scenario: Unblocked stories spawn immediately
    Given a sprint with stories A, B, and C
    And story A has no dependencies
    And story B has no dependencies
    And story C depends on A
    When sprint-dev begins team spawn
    Then momentum-dev agents are spawned for stories A and B
    And no agent is spawned for story C
    And stories A and B are transitioned to in-progress

  Scenario: Each agent gets its own worktree
    Given story "agent-logging-tool" is unblocked
    When a momentum-dev agent is spawned for it
    Then the agent operates in worktree .worktrees/story-agent-logging-tool
    And the worktree is on branch story/agent-logging-tool

  Scenario: Agents receive role guidelines from sprint record
    Given the sprint record assigns story "agent-logging-tool" to role "dev"
    And role "dev" has guidelines at "path/to/dev-guidelines.md"
    When the momentum-dev agent is spawned
    Then the agent receives the role-specific guidelines

  Scenario: All agents log via momentum-tools
    Given a momentum-dev agent is executing a story
    When the agent makes a decision, encounters an error, or notes a finding
    Then it writes a log entry via momentum-tools log
    And the log entry includes the sprint slug and story slug

  # --- Dependency Resolution ---

  Scenario: Blocked story spawns after dependency merges
    Given story C depends on story A
    And story A's agent has completed and merged
    When sprint-dev checks the dependency graph
    Then story C is identified as newly unblocked
    And a momentum-dev agent is spawned for story C
    And story C is transitioned to in-progress

  Scenario: Story with multiple dependencies waits for all
    Given story D depends on stories A and B
    And story A has merged but story B has not
    When sprint-dev checks the dependency graph after A merges
    Then story D remains blocked
    And no agent is spawned for story D

  Scenario: Story with multiple dependencies spawns when last blocker merges
    Given story D depends on stories A and B
    And both stories A and B have merged
    When sprint-dev checks the dependency graph after B merges
    Then story D is identified as unblocked
    And a momentum-dev agent is spawned for story D

  # --- Merge Flow ---

  Scenario: Merge requires developer confirmation
    Given a momentum-dev agent reports story A as merge-ready
    When sprint-dev proposes the merge
    Then it waits for explicit developer confirmation
    And does not auto-execute the merge

  Scenario: Story status transitions after merge
    Given the developer confirms the merge for story A
    When the merge completes successfully
    Then story A is transitioned to review via momentum-tools sprint status-transition
    And the merge is logged via momentum-tools log

  Scenario: Worktree cleaned up after merge
    Given story A has been merged
    When sprint-dev completes the merge flow
    Then the worktree at .worktrees/story-{slug} is removed
    And the story branch story/{slug} is deleted

  # --- Progress Tracking ---

  Scenario: Task status reflects agent progress
    Given a momentum-dev agent is executing story A
    When the agent begins work
    Then the corresponding task is updated to in_progress
    And when the agent completes, the task is marked complete

  Scenario: Sprint-dev continues until all stories merge
    Given a sprint with 4 stories
    And 3 stories have merged
    When the 4th story's agent completes and merges
    Then sprint-dev proceeds to the post-merge quality gate
    And does not wait for additional stories

  # --- Post-Merge AVFL ---

  Scenario: AVFL runs once after all stories merge
    Given all sprint stories have been merged to main
    When sprint-dev enters the post-merge quality gate
    Then a single AVFL pass is invoked against the full codebase
    And AVFL does not run on individual stories or worktrees

  Scenario: AVFL findings presented to developer
    Given the AVFL pass produces findings
    When the findings are surfaced
    Then the developer reviews and addresses each finding
    And sprint-dev iterates until the developer is satisfied
    And resolved findings are logged

  Scenario: AVFL with no findings proceeds to verification
    Given the AVFL pass produces zero findings
    When the AVFL phase completes
    Then sprint-dev proceeds directly to verification

  # --- Black-Box Verification ---

  Scenario: Verifiers read Gherkin specs from sprint specs directory
    Given Gherkin specs exist at sprints/{sprint-slug}/specs/
    When sprint-dev enters the verification phase
    Then verifiers read .feature files from that directory
    And each scenario is extracted as a verification item

  Scenario: Dev agents never access Gherkin specs
    Given Gherkin specs exist at sprints/{sprint-slug}/specs/
    When momentum-dev agents execute stories during the sprint
    Then no dev agent reads from or references the specs directory
    And story files contain only plain English acceptance criteria

  Scenario: Developer-confirmation checklist presented
    Given 3 feature files with a total of 12 scenarios
    When the verification phase begins
    Then a checklist of 12 items is presented to the developer
    And each item corresponds to a Gherkin scenario name and expected behavior
    And the developer confirms or flags each item

  Scenario: Verification start transitions stories to verify
    Given AVFL has passed
    When the verification phase begins
    Then all sprint stories are transitioned to verify
    And each transition uses momentum-tools sprint status-transition --target verify

  Scenario: All scenarios confirmed transitions stories to done
    Given the developer confirms all verification checklist items
    And all sprint stories have status verify
    When verification completes
    Then all sprint stories are transitioned from verify to done
    And each transition uses momentum-tools sprint status-transition --target done

  Scenario: Unconfirmed verification item logged as finding
    Given the developer flags a verification item as unconfirmed
    When the flagged item is recorded
    Then it is logged as a finding via momentum-tools log
    And the developer is offered the option to create a follow-up story
    And the sprint can still complete with the finding noted

  # --- Sprint Completion ---

  Scenario: Sprint archived on completion
    Given all stories are transitioned to done
    When sprint-dev enters the completion phase
    Then momentum-tools sprint complete is called
    And the sprint moves from active to the completed array in sprints/index.json

  Scenario: Sprint summary surfaced
    Given the sprint has been archived
    When sprint-dev displays the summary
    Then it shows the count and list of completed stories
    And the actual merge order (execution sequence)
    And the number of AVFL findings found and resolved
    And the verification results (confirmed vs. total scenarios)
    And the location of agent logs for retrospective analysis

  Scenario: Retro suggested after completion
    Given the sprint summary has been displayed
    Then sprint-dev suggests running a retrospective
    And does not auto-dispatch to the retro workflow

  # --- Error Handling ---

  Scenario: Agent failure surfaced to developer
    Given a momentum-dev agent fails during story execution
    When the failure is detected
    Then sprint-dev logs the failure via momentum-tools log
    And surfaces the failure to the developer
    And offers retry or skip options
    And does not auto-retry

  Scenario: Merge conflict surfaced to developer
    Given a merge produces conflicts
    When the conflict is detected
    Then sprint-dev surfaces the conflicting files with diff context
    And the developer resolves the conflict manually
    And sprint-dev waits for resolution before proceeding

  Scenario: Stories already done are skipped
    Given a sprint where story A already has status done
    When sprint-dev initializes
    Then story A is not spawned
    And story A is counted as already merged for dependency resolution
    And stories that depend on A are treated as unblocked
