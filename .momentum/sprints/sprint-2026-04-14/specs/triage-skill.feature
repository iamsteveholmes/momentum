Feature: Triage skill classifies and routes multiple observations in one session

  Background:
    Given the developer is in a Momentum session with observations to process

  Scenario: Developer classifies a batch of observations before anything is written
    Given the developer has several observations ready to triage
    When the developer invokes momentum:triage with those observations
    Then each observation appears in a classification plan labelled with one of ARTIFACT, DISTILL, DECISION, SHAPING, DEFER, or REJECT
    And the developer sees the full plan before any downstream action runs
    And the developer can accept, override, or reclassify any item before confirming

  Scenario: Approved ARTIFACT items become feature-tagged backlog stubs
    Given the triage plan contains ARTIFACT items with their enriched classifications
    When the developer confirms the plan
    Then a new backlog story stub exists for each ARTIFACT item
    And each stub records a feature assignment and a story type matching the triage enrichment

  Scenario: Approved DISTILL items produce immediate practice changes
    Given the triage plan contains DISTILL items
    When the developer confirms the plan
    Then each DISTILL item produces a change to the targeted practice material
    And the change goes through the normal distill approval before it is applied

  Scenario: Approved DECISION items produce decision documents
    Given the triage plan contains DECISION items
    When the developer confirms the plan
    Then a decision document exists for each DECISION item with the captured rationale and verdict

  Scenario: Shape, defer, and reject items are captured and re-surface in future sessions
    Given the triage plan contains SHAPING, DEFER, or REJECT items
    When the developer confirms the plan
    Then those items are recorded in the intake queue with their respective kinds
    And open shape and defer items re-surface at the start of the next triage session alongside new observations

  Scenario: Open items from prior sessions appear with age and classification visible
    Given the intake queue already contains open shape or defer entries written in a prior session
    When the developer starts a new triage session
    Then those prior entries appear in the classification list alongside any new observations
    And each prior entry is visibly tagged with its age and its original classification from the prior session

  Scenario: Triage never writes story stubs or decisions by itself
    Given the triage plan contains ARTIFACT, DISTILL, and DECISION items
    When the developer confirms the plan
    Then the resulting stubs, practice changes, and decision documents are produced through intake, distill, and decision with their usual prompts and approvals

  Scenario: Impetus Triage menu item starts a triage session instead of the old placeholder
    Given the developer is at the Impetus session menu with Triage listed as an option
    When the developer selects Triage
    Then a triage session begins and prompts the developer for observations

  Scenario: Intake captures feature and story type when invoked on its own
    Given the developer invokes intake to capture a single story idea
    When the developer completes the intake prompts
    Then the resulting backlog stub carries both a feature assignment and a story type
