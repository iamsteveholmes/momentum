Feature: Impetus Session-Start Staleness Check — Detect Plugin Cache Skew and Prompt Update+Restart

  Background:
    Given the Momentum plugin is installed via Claude Code's plugin marketplace
    And the developer is invoking momentum:impetus from inside a momentum source-tree checkout

  Scenario: Developer sees the normal orientation greeting when cache and source agree
    Given the active plugin cache version equals the source-tree plugin manifest version
    When the developer invokes momentum:impetus at session start
    Then the orientation greeting appears
    And no staleness warning appears anywhere in the output

  Scenario: Developer is warned with remedy when the active cache lags behind the source tree
    Given the active plugin cache reports an older version than the source-tree plugin manifest
    When the developer invokes momentum:impetus at session start
    Then a staleness warning appears before the orientation greeting
    And the warning names both the cache version and the source version
    And the warning explains that workflows dispatched in this session will run against stale workflow content
    And the warning instructs the developer to run /plugin marketplace update momentum and start a fresh Claude Code session
    And the warning describes itself as a safety net that reinforces the operator-discipline rule of starting a fresh session before major workflows

  Scenario: Developer is warned to verify the working branch when the cache is ahead of the source
    Given the active plugin cache reports a newer version than the source-tree plugin manifest
    When the developer invokes momentum:impetus at session start
    Then a staleness warning appears before the orientation greeting
    And the warning names both the cache version and the source version
    And the warning indicates the source tree is behind the cache
    And the warning suggests verifying the working branch and pulling the latest source

  Scenario: Developer working outside a plugin install sees the greeting with no warning
    Given the plugin cache directory for momentum does not exist on the developer's machine
    When the developer invokes momentum:impetus at session start
    Then the orientation greeting appears
    And no staleness warning appears
    And no error message appears

  Scenario: Developer invoking impetus outside a momentum checkout sees the greeting with no warning
    Given the developer invokes momentum:impetus from a directory that is not a momentum source-tree checkout
    When the session-start preflight runs
    Then the orientation greeting appears
    And no staleness warning appears
    And no error message appears

  Scenario: Developer with multiple cached versions sees a warning only when the highest cache disagrees with source
    Given the plugin cache directory contains several version subdirectories with the highest equal to the source-tree plugin manifest version
    When the developer invokes momentum:impetus at session start
    Then the orientation greeting appears
    And no staleness warning appears

  Scenario: Corrupt cache manifest does not produce a false-positive warning or crash
    Given the active plugin cache directory contains a plugin manifest that cannot be parsed
    When the developer invokes momentum:impetus at session start
    Then the orientation greeting appears
    And no staleness warning appears
    And no error message appears

  Scenario: Developer can probe staleness directly through the momentum-tools CLI
    Given the developer wants to verify cache and source versions manually
    When the developer runs the momentum-tools session plugin-cache-check command
    Then a JSON object prints to standard output
    And the JSON reports the detected cache version, the detected source version, and a status field
    And the status field takes one of the values match, skew-cache-behind, skew-cache-ahead, no-cache, no-source, or indeterminate
    And the command exits with status code zero regardless of the detected status

  Scenario: Session-start preflight stays fast in the typical hot path
    Given the active plugin cache version equals the source-tree plugin manifest version
    When the developer invokes momentum:impetus at session start
    Then the orientation greeting appears within the latency budget the developer expects from a cold start
    And no network access occurs during the preflight
    And no git operations occur during the preflight

  Scenario: Source plugin.json is missing the version field — silent pass
    Given the source-tree plugin.json exists but contains no version key
    When the developer invokes momentum:impetus at session start
    Then the orientation greeting appears
    And no staleness warning appears
    And no error message appears
    And the momentum-tools session plugin-cache-check command reports a status of indeterminate or no-source

  Scenario: Cache directory has no version subdirectories — silent pass
    Given the path ~/.claude/plugins/cache/momentum/momentum/ exists but contains no version subdirectories
    When the developer invokes momentum:impetus at session start
    Then the orientation greeting appears
    And no staleness warning appears
    And no error message appears
    And the momentum-tools session plugin-cache-check command reports a status of no-cache

  Scenario: Staleness warning instructs the operator-discipline remedy
    Given the active plugin cache reports an older version than the source-tree plugin manifest
    When the developer invokes momentum:impetus at session start
    Then a staleness warning appears before the orientation greeting
    And the warning text instructs the developer to run /plugin marketplace update momentum and start a fresh Claude Code session
    And the warning text states that the fresh-session rule is the primary mitigation and the warning is a safety net
