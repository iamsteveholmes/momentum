Feature: Implement /momentum:distill — Practice Artifact Distillation Skill

  Background:
    Given the Momentum plugin is installed and the developer is in an active session

  Scenario: Skill confirms proposed change before writing anything
    Given the developer has a session learning to capture
    When the developer invokes momentum:distill with the learning description
    Then the skill presents a proposed change and target artifact for the developer to review
    And no files have been modified at the point of confirmation

  Scenario: Developer cancels after seeing the proposed change
    Given the developer has invoked momentum:distill with a learning description
    And the skill has presented a proposed change for review
    When the developer declines the proposed change
    Then no files are written
    And no commit is created

  Scenario: Project-local learning is applied and committed
    Given the developer has invoked momentum:distill with a learning that applies to the current project only
    And the skill has presented the proposed change targeting a project rule file
    When the developer confirms the proposed change
    Then the relevant project rule file reflects the applied learning
    And a conventional commit exists recording the change

  Scenario: Momentum-level learning applied while in the Momentum project
    Given the developer is working inside the Momentum project
    And the developer has invoked momentum:distill with a learning that applies to Momentum's own practice files
    When the developer confirms the proposed change
    Then the relevant Momentum practice file reflects the applied learning
    And the plugin version is incremented
    And a push summary is presented to the developer before any push occurs

  Scenario: Momentum-level learning surfaced while outside the Momentum project offers defer option
    Given the developer is working in a project that is not the Momentum repository
    And the developer has invoked momentum:distill with a learning that applies to Momentum's own practice files
    When the skill completes discovery
    Then the developer is presented with an option to defer the finding to retro
    And the developer is presented with an option to receive a self-contained prompt for applying the change in a Momentum session
    And no Momentum practice files are modified

  Scenario: Developer defers a Momentum-level finding to retro from an external project
    Given the developer is working outside the Momentum project
    And momentum:distill has surfaced a Momentum-level learning
    When the developer chooses to defer the finding to retro
    Then the finding is recorded in the findings ledger with its origin marked as distill
    And no files in the Momentum project are modified

  Scenario: Developer requests a remote prompt for a Momentum-level finding
    Given the developer is working outside the Momentum project
    And momentum:distill has surfaced a Momentum-level learning
    When the developer chooses to generate a remote prompt
    Then the skill produces a self-contained prompt the developer can paste into a Momentum session
    And the prompt contains the proposed change and the target file

  Scenario: Small rule addition is applied immediately and committed
    Given the developer has invoked momentum:distill with a single-sentence rule addition
    And the skill has classified the change as immediately applicable
    When the developer confirms the proposed change
    Then the rule is written to the appropriate practice artifact
    And the developer receives validation output before any commit confirmation is presented
    And the change is committed

  Scenario: Structural change produces a story stub instead of a direct edit
    Given the developer has invoked momentum:distill with a learning that requires multi-file changes
    And the skill has classified the change as requiring structural work
    When the developer confirms the proposed action
    Then a story stub appears in the implementation stories directory
    And the skill's output indicates that a story has been queued rather than applied

  Scenario: AVFL findings are presented for developer decision before committing
    Given the developer has confirmed a Tier 1 change via momentum:distill
    And the post-change validation pass has run and returned findings
    When the validation results are available
    Then the findings are presented to the developer
    And the developer is offered a choice to correct the artifact or commit as-is

  Scenario: Every distill invocation produces a findings ledger entry
    Given the developer has invoked momentum:distill and the skill has completed
    When the skill exits regardless of path taken
    Then the skill's output confirms that the learning has been recorded along with the artifact and path taken

  Scenario: Retro routes a Tier 1 classified finding through distill instead of creating a stub
    Given a retro session has reached the action-item phase
    And a finding is classified as small and immediately applicable with a signal type set
    When the retro processes that finding
    Then the retro reports that the practice artifact was updated for that finding
    And no story stub is created for that finding

  Scenario: Retro routes a Tier 2 finding through the existing stub creation path
    Given a retro session has reached the action-item phase
    And a finding is classified as requiring structural or multi-file changes
    When the retro processes that finding
    Then a story stub is created for that finding
    And the retro reports the finding as queued for a future sprint

  Scenario: Distill AVFL profile is available for post-change validation
    Given the Momentum AVFL framework is configured
    When momentum:distill completes a Tier 1 change
    Then the post-change validation runs using the distill profile on only the modified files
    And the validation output is returned without a fix-loop pass
