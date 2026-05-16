Feature: Beads Dual-Write Proof of Concept

  Background:
    Given the Momentum project is checked out and the developer is on the main branch

  Scenario: Beads CLI is available and the project is initialized without error
    Given the beads CLI has been installed
    When the developer runs `bd list --json` in the project root
    Then the command exits with code 0
    And the output is a valid JSON array

  Scenario: Beads data directory is excluded from version control
    Given beads has been initialized in the project root
    When the developer runs `git status` in the project root
    Then the `.beads/` directory does not appear as tracked or untracked output

  Scenario: Story creation via sprint commands mirrors a bead into the shadow layer
    Given a sprint has been activated with at least one story
    When the developer invokes sprint-manager to activate the sprint
    Then the `.momentum/beads-id-map.json` file contains an entry mapping the story slug to a bead ID
    And running `bd show` with that bead ID exits without error and displays the story title

  Scenario: Bead created for a story links back to its spec file
    Given a story has been mirrored into the beads shadow layer
    When the developer runs `bd show <bead-id>` for that story's bead
    Then the output includes a spec_id field
    And the spec_id value is the path to the story's `.md` file under `.momentum/stories/`

  Scenario: Sprint execution selects unblocked stories using the beads ready queue
    Given a sprint is active with stories that have dependency relationships
    When the developer invokes sprint-dev
    Then the sprint proceeds to execute stories that are unblocked
    And no story with unresolved dependencies is scheduled for execution in the same wave

  Scenario: Sprint execution continues normally when the beads ready queue is unavailable
    Given a sprint is active and the beads layer is not responding
    When the developer invokes sprint-dev
    Then the sprint proceeds using the dependency graph from the JSON index
    And the developer sees a log entry indicating the beads fallback was used
    And all stories in the sprint complete without error

  Scenario: Discovered work captured via intake includes a beads shadow entry
    Given a sprint is active and beads is initialized
    When the developer invokes intake to capture a new story discovered during the sprint
    Then a new entry appears in `intake-queue.jsonl` for the discovered story
    And `.momentum/beads-id-map.json` contains a new entry for the discovered story slug
    And running `bd show` with that entry's bead ID displays the discovered-from relationship

  Scenario: Session startup loads the Momentum protocol without triggering a sync push
    Given the beads SessionStart hook is configured in the project
    When the developer starts a new Claude Code session in the project root
    Then the session output includes Momentum protocol content about git-discipline and sole-writer rules
    And no `bd dolt push` command is executed during session startup

  Scenario: Beads write failure does not abort sprint-manager story registration
    Given a sprint plan is being activated and the beads layer returns an error
    When the developer invokes sprint-manager to activate the sprint
    Then `stories/index.json` and `sprints/index.json` are updated correctly
    And a log entry recording the beads failure is written
    And the sprint activation completes without halting

  Scenario: Research artifact is committed and covers all evaluation criteria
    Given the spike sprint has been executed with the dual-write layer active
    When the developer reviews the committed files in the repository
    Then a research findings file exists under `docs/research/` with a name beginning `beads-dual-write-spike-findings-`
    And the file contains sections addressing dependency scheduling, intake routing, sync manageability, and spec-id linkage
    And the file states a go or no-go recommendation with supporting evidence
    And the file is present in the git history as a committed change
