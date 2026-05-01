---
title: Session-Open Sprint View — Mode Detection and Fill Bars
status: ready-for-dev
epic_slug: impetus-core
depends_on:
  - momentum-tooling
touches:
  - skills/momentum/workflow.md
change_type: skill-instruction
---

# Session-Open Sprint View

## Goal

Redesign Impetus's session-open (Step 7) to be sprint-aware. Detect the current sprint
state, display per-story progress with 16-block fill bars, and present context-appropriate
menus. Impetus asks about sprint state rather than assuming.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: Session-Open Sprint View

  Scenario: Active sprint with stories in progress
    Given an active sprint exists with stories in various states
    When the user invokes /momentum and reaches session orientation
    Then Impetus displays the sprint name
    And each story in the sprint shows a 16-block fill bar reflecting its status
    And a numbered context menu offers sprint-relevant actions
    And the menu includes an option to continue the sprint

  Scenario: Fill bars reflect story status accurately
    Given an active sprint contains stories with statuses backlog, ready-for-dev,
      in-progress, review, verify, and done
    When the session-open view renders
    Then each story's fill bar corresponds to its status level
    And backlog shows a hatched/empty bar
    And done shows a fully filled bar
    And intermediate statuses show proportional fill

  Scenario: Active sprint complete — all stories done
    Given an active sprint exists where all stories have status done
    When the user invokes /momentum
    Then Impetus indicates the sprint is complete
    And if a planning sprint exists, it is mentioned with story count
    And the menu offers retro, plan activation, or plan adjustment options

  Scenario: No active sprint
    Given no active sprint exists
    When the user invokes /momentum
    Then Impetus shows the overall backlog state (story count across epics)
    And the menu offers sprint planning, backlog refinement, or triage options
    And no sprint-specific UI elements are shown

  Scenario: Sprint state is queried not assumed
    Given any sprint state
    When Impetus presents the session-open view
    Then menu options are phrased as offers, not assumptions
    And Impetus does not auto-dispatch to sprint workflows without developer selection

  Scenario: Sprint view degrades gracefully when files are missing
    Given stories/index.json or sprints/index.json does not exist
    When the user invokes /momentum
    Then Impetus falls back to a non-sprint session menu
    And no error is surfaced to the user

  Scenario: Planning sprint visible when no active sprint
    Given no active sprint exists but a planning sprint exists
    When the user invokes /momentum
    Then Impetus mentions the planning sprint with its name and story count
    And the menu offers to activate or adjust the plan

  Scenario: Story details available on demand
    Given the session-open sprint view is displayed
    When the developer requests more detail about a specific story
    Then Impetus shows the story title, current status, and epic membership
    And does not require navigating away from the session view
```

## Dev Notes

### What exists today
- Step 7 currently renders epic-level progress bars (not story-level)
- Two variants: compressed single-line (experienced users) and verbose multi-line (new users)
- Menu offers `/create` and `/develop` — no sprint awareness
- No sprint-mode detection — always shows the same menu regardless of sprint state

### What to change
- Replace the epic-level bar rendering in Step 7 with sprint-aware rendering
- Add sprint-mode detection: read sprints/index.json for active/planning state
- Implement 3 UI modes per the plan mockups:
  - Mode 1: Active sprint, stories in progress
  - Mode 2: Active sprint complete / planning ready
  - Mode 3: No active sprint
- Add 16-block fill bar rendering per story using the status-to-fill mapping:
  ```
  backlog       ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  (hatched — not in sprint)
  ready-for-dev ░░░░░░░░░░░░░░░░  (empty — waiting)
  in-progress   ████████░░░░░░░░
  review        ████████████░░░░
  verify        ██████████████░░
  done          ████████████████
  ```
- Menu items reference sub-commands that may not exist yet (Phase 3) —
  handle gracefully with "coming soon" or route to available alternatives

### What NOT to change
- Steps 1-6 (install/upgrade flow) remain unchanged
- Steps 9-10 (upgrade and hash drift) remain unchanged
- Journal display (Step 11) remains unchanged — sprint view is BEFORE thread display
- Input Interpretation rules remain unchanged

### Dependencies
- momentum-tooling must be complete (provides sprint state reading infrastructure)
- sprints/index.json and stories/index.json must exist (created in Story 0.2)
