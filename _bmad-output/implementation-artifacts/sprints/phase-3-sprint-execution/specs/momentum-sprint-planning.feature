Feature: Sprint Planning Workflow
  As a developer using Momentum
  I want a guided sprint planning workflow
  So that I can select stories, generate specs, compose a team, and activate a sprint

  Background:
    Given the Momentum practice module is installed
    And stories/index.json contains stories across multiple epics
    And sprints/index.json exists with no active sprint

  # --- Step 1: Backlog Presentation ---

  Scenario: Backlog displays stories grouped by epic
    Given stories/index.json contains stories in 3 different epics
    When Impetus presents the prioritized backlog
    Then stories are grouped under their epic_slug headings
    And each story shows its title, current status, and dependency list
    And a summary line shows total selectable story count

  Scenario: Terminal-state stories are excluded from the backlog
    Given stories/index.json contains stories with statuses done, dropped, and closed-incomplete
    When Impetus presents the prioritized backlog
    Then no story with a terminal status appears in the backlog display

  Scenario: Stories are sorted by dependency depth within each epic
    Given epic "impetus-core" has stories A (depends on nothing), B (depends on A), and C (depends on B)
    When Impetus presents the prioritized backlog
    Then within "impetus-core", stories appear in order A, B, C
    And leaf stories (no dependencies) appear before dependent stories

  Scenario: Stories with unsatisfied dependencies are visually flagged
    Given story "momentum-sprint-dev" depends on "momentum-sprint-planning" which has status "backlog"
    When Impetus presents the prioritized backlog
    Then "momentum-sprint-dev" is displayed with a dependency warning indicator
    And the warning names the unsatisfied dependency

  # --- Step 2: Story Selection ---

  Scenario: Developer selects stories within valid range
    Given the backlog is displayed with 12 selectable stories
    When the developer selects 5 stories by number
    Then Impetus confirms the selection with story titles
    And the selection count is validated as within the 3-8 range

  Scenario: Selection below minimum is rejected
    When the developer selects 2 stories
    Then Impetus warns that the minimum is 3 stories
    And prompts the developer to select additional stories

  Scenario: Selection above maximum is warned
    When the developer selects 9 stories
    Then Impetus warns that more than 8 stories risks sprint overload
    And asks the developer to confirm or reduce the selection

  Scenario: Dependency chain risk is flagged during selection
    Given story B depends on story A
    And story A has status "backlog" and is NOT in the current selection
    When the developer selects story B
    Then Impetus warns that story B depends on story A which is not in this sprint
    And the developer can acknowledge the risk or add story A

  Scenario: Selected stories are registered in the planning sprint
    Given the developer has selected stories "agent-logging-tool" and "momentum-dev-simplify"
    When the selection is confirmed
    Then momentum-tools sprint plan --operation add is called with the selected slugs
    And sprints/index.json planning section contains the selected stories

  Scenario: Sprint receives a date-based slug
    When a new sprint planning session begins
    Then the sprint is named with format "sprint-YYYY-MM-DD"
    And if a sprint with that slug already exists, a sequence suffix is appended

  # --- Step 3: Story Fleshing-Out ---

  Scenario: Stub stories are fleshed out via momentum-create-story
    Given the sprint includes a story where story_file is false in index.json
    When Impetus processes story fleshing-out
    Then momentum-create-story is spawned for that story
    And the resulting story file contains tasks, plain English ACs, and dev notes
    And Impetus presents the fleshed-out story for developer approval

  Scenario: Already-complete story files skip create-story
    Given the sprint includes a story where story_file is true in index.json
    And the story markdown file has full content (Goal, ACs, Dev Notes sections)
    When Impetus processes story fleshing-out
    Then momentum-create-story is NOT spawned for that story
    And Impetus surfaces the existing story content for developer review

  Scenario: Developer can request revisions to a fleshed-out story
    Given momentum-create-story has produced a story file
    When the developer requests changes to the story
    Then Impetus facilitates the revision
    And the revised story is re-presented for approval
    And the process repeats until the developer approves

  Scenario: All stories must be approved before proceeding
    Given 5 stories are selected for the sprint
    When 4 stories have been approved and 1 has not
    Then Impetus does not proceed to Gherkin generation
    And prompts the developer to review the remaining story

  # --- Step 4: Gherkin Spec Generation ---

  Scenario: Gherkin specs are generated for each approved story
    Given all selected stories have been approved
    When Impetus generates Gherkin specifications
    Then a .feature file is created for each story
    And each file is written to sprints/{sprint-slug}/specs/{story-slug}.feature

  Scenario: Gherkin specs contain detailed behavioral scenarios
    Given a story with acceptance criteria about session orientation
    When the Gherkin spec is generated
    Then the .feature file contains a Feature declaration with descriptive title
    And at least one Scenario per acceptance criterion
    And Given/When/Then steps that encode specific behavioral expectations

  Scenario: Story markdown files are not modified during Gherkin generation
    Given a story file exists with plain English acceptance criteria
    When Gherkin specs are generated for that story
    Then the story markdown file retains its original plain English ACs
    And no Gherkin syntax appears in the story markdown file

  Scenario: Gherkin specs directory is scoped to the sprint
    Given the sprint slug is "sprint-2026-04-03"
    When Gherkin specs are generated
    Then specs are written under sprints/sprint-2026-04-03/specs/
    And the directory is created if it does not exist

  # --- Step 5: Team Composition ---

  Scenario: Agent roles are determined from story metadata
    Given the sprint contains stories with change_type "skill-instruction" and "cli-tool"
    When Impetus builds the team composition
    Then the team includes at minimum a Dev role
    And additional roles are assigned based on change_type and touches analysis

  Scenario: Execution waves group concurrent stories
    Given the sprint contains stories A (no deps), B (no deps), C (depends on A)
    When Impetus builds the dependency graph
    Then Wave 1 contains stories A and B
    And Wave 2 contains story C
    And wave assignments are stored via momentum-tools sprint plan --wave

  Scenario: Two-layer model separates generic roles from project guidelines
    Given a project has stack-specific guidelines for "Frontend Dev"
    When Impetus builds the team composition
    Then the team plan shows the generic Momentum role definition
    And the project-specific guidelines attached to that role
    And both layers are presented to the developer for review

  Scenario: Stories with overlapping touches paths are flagged for merge conflict risk
    Given story A touches "skills/momentum/workflow.md"
    And story B also touches "skills/momentum/workflow.md"
    When Impetus builds the execution plan
    Then stories A and B are flagged as having overlapping touches
    And Impetus recommends sequential execution or careful merge review

  # --- Step 6: AVFL Validation ---

  Scenario: AVFL runs on the complete sprint plan
    Given all stories are approved, Gherkin specs are generated, and team composition is built
    When Impetus runs AVFL validation
    Then AVFL receives all story files, all Gherkin specs, and the team composition as input
    And validation runs as a single pass across the entire plan

  Scenario: AVFL catches cross-story conflicts
    Given two stories have contradictory acceptance criteria
    When AVFL validates the complete sprint plan
    Then the conflict is identified in the AVFL findings
    And the finding references both stories by slug

  Scenario: AVFL results are presented before developer approval
    Given AVFL validation completes with findings
    When Impetus presents the sprint plan for review
    Then AVFL results are included in the review summary
    And critical findings are highlighted for developer attention

  # --- Step 7: Developer Review ---

  Scenario: Complete sprint plan is presented for review
    Given all planning steps are complete
    When Impetus presents the sprint plan
    Then the presentation includes sprint name and total story count
    And a per-story summary with title, wave assignment, and agent role
    And a team composition table showing roles, guidelines, and story assignments
    And a dependency graph showing wave structure and blocking relationships

  Scenario: Developer can adjust the plan before approval
    Given the sprint plan is presented for review
    When the developer requests removing a story
    Then Impetus calls momentum-tools sprint plan --operation remove for that story
    And the plan is re-presented with the adjustment applied

  Scenario: Developer can add stories during review
    Given the sprint plan is presented for review
    When the developer requests adding a story that was not originally selected
    Then the new story goes through the fleshing-out and Gherkin generation steps
    And the team composition and execution waves are recalculated
    And the updated plan is re-presented

  # --- Step 8: Sprint Activation ---

  Scenario: Approved sprint is activated via momentum-tools
    Given the developer approves the sprint plan
    When Impetus activates the sprint
    Then momentum-tools sprint activate is called
    And sprints/index.json shows the sprint as active with a locked flag
    And a start date is recorded in the sprint record

  Scenario: Activation is blocked when another sprint is already active
    Given an active sprint already exists in sprints/index.json
    When the developer attempts to activate a new sprint
    Then momentum-tools sprint activate returns an error
    And Impetus explains that the active sprint must be completed first

  Scenario: Activation confirmation displays sprint summary
    Given the sprint is successfully activated
    When Impetus presents the activation confirmation
    Then the confirmation shows the sprint name, start date, and story count
    And lists the execution waves with story assignments

  # --- Cross-cutting: Agent Logging ---

  Scenario: Planning decisions are logged throughout the workflow
    Given the agent logging tool is available
    When Impetus executes any sprint planning step
    Then planning decisions are logged via momentum-tools log
    And log entries include the agent "impetus", the sprint slug, and event details

  Scenario: Story approvals are logged as decisions
    Given a developer approves a fleshed-out story
    When the approval is recorded
    Then a log entry with event type "decision" is written
    And the detail includes the story slug and approval status

  Scenario: AVFL findings are logged
    Given AVFL completes with findings
    When the findings are processed
    Then each finding is logged with event type "finding"
    And the detail includes the finding severity and affected stories
