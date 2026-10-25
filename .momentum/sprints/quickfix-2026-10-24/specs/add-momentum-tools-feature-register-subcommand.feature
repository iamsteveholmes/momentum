Feature: Add momentum-tools feature register so features can enter the registry via the sole-writer path

  Background:
    Given the developer is working in a project that uses the feature registry
    And the developer can run the momentum-tools command line

  Scenario: Developer registers the first feature and the registry comes into existence
    Given the project has no feature registry file
    When the developer registers a feature with a valid slug, a name and an acceptance condition
    Then the command succeeds and reports the feature as absent
    And a feature registry file now exists containing only that feature with its name and acceptance condition
    And the entry records no design reference and no epics, and nothing else beyond its slug, name, acceptance condition, status and verification time

  Scenario: Developer registers a second feature alongside the first
    Given one feature is already registered
    When the developer registers another feature with a different slug
    Then both features are present in the registry
    And the first feature's recorded details are exactly as they were before

  Scenario: Developer records optional design reference and epics when registering
    Given the project has a feature registry
    When the developer registers a feature supplying a design reference and a comma-separated list of epics
    Then the registered feature carries the design reference as given and the list of epics
    And an epic name that matches no known epic is still accepted

  Scenario: Newly registered feature has no verdict until the developer verifies it
    Given the developer has registered a feature
    Then the registered feature shows status absent and no verification time
    When the developer records a passing verdict for that feature
    Then the feature shows status passing with a verification time
    And its name and acceptance condition are unchanged

  Scenario: Developer cannot record a verdict for a feature that was never registered
    Given the project has a feature registry that lacks a particular slug
    When the developer records a verdict for that slug
    Then the command is refused and the registry is unchanged

  Scenario: Re-registering an existing feature is refused and nothing changes
    Given a feature is registered and has a verdict of failing
    When the developer registers the same slug again with different text
    Then the command fails with an error naming the slug and its existing status
    And the registry file is byte-for-byte identical to before

  Scenario: Re-registering a feature that is registered but not yet verified is refused
    Given a feature is registered and not yet verified
    When the developer registers the same slug again
    Then the command fails with an error naming the status absent
    And the registry file is byte-for-byte identical to before

  Scenario: Re-registering a passing feature never resets it
    Given a feature is registered and has a verdict of passing
    When the developer registers the same slug again
    Then the command fails with an error naming the status passing
    And the feature is still passing with its original verification time

  Scenario: Developer is refused when the slug is not kebab-case
    Given the project has a feature registry
    When the developer registers a feature whose slug has capitals, underscores, doubled hyphens or a leading hyphen
    Then the command fails with an error naming the slug
    And the registry file is byte-for-byte identical to before

  Scenario: Developer is refused when the name or acceptance condition is blank
    Given the project has no feature registry file
    When the developer registers a feature with a whitespace-only name
    Then the command fails with an error naming the name option
    When the developer registers a feature with an empty acceptance condition
    Then the command fails with an error naming the acceptance condition option
    And no feature registry file has been created

  Scenario: Developer is refused when a required option is omitted
    Given the project has a feature registry
    When the developer registers a feature without supplying an acceptance condition
    Then the command fails and the registry file is byte-for-byte identical to before

  Scenario: Corrupt registry is refused and left untouched
    Given the feature registry file contains text that is not valid JSON
    When the developer registers a valid feature
    Then the command fails with an error naming the registry file
    And the file's contents are byte-for-byte identical to before
    Given the feature registry file contains a JSON list instead of an object
    When the developer registers a valid feature
    Then the command fails and the file is byte-for-byte identical to before

  Scenario: Registered but unverified feature is recorded as absent, not passing
    Given a registry with one passing feature
    When the developer registers a second feature without verifying it
    Then the registry holds two entries in total and exactly one has status passing
    And the new entry has status absent

  Scenario: Closing a sprint that declares a registered but unverified feature is refused
    Given a feature is registered and not yet verified
    And an active sprint declares that feature as a goal condition
    When the developer completes the sprint
    Then the command is refused, listing the feature as unverified
    And the feature registry is unchanged

  Scenario: Tasting status keeps working and does not treat an unverified feature as passing
    Given the developer has registered a feature without verifying it
    When the developer asks for the tasting status
    Then the command succeeds
    And the unverified feature is not reported as passing

  Scenario: Other commands still never create the registry
    Given the project has no feature registry file
    When the developer runs a verdict, a tasting status or a tasting brief command
    Then no feature registry file is created

  Scenario: Developer discovers register from the command help
    When the developer asks for help on the feature command
    Then both verify and register are listed
    And register help describes its name, acceptance condition, design reference and epics options
