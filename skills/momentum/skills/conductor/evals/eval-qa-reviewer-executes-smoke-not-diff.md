# Eval: qa-reviewer executes a smoke-routed story — build + fresh launch + drive, not diff inspection

## Given

A fixture story `fixture-smoke-routed-story` whose frozen verification contract Part-A header
declares:

```
verification_method: smoke
harness_profile: smoke
```

and whose Part B `scenarios:` section names one scenario driving an observable UI flow (e.g.
"the settings screen shows the new toggle and it persists across a relaunch"). The project's
`momentum/verification-harness.json` has a real (non-`skip`) `driver_bindings.smoke` entry and a
supporting environment: a reachable emulator/simulator/web target, `env.startup` commands that
succeed, and `env.readiness_probe` commands that pass.

The story's worktree diff contains an implementation that genuinely satisfies the scenario (the
toggle exists in the running app, not just in source).

## The qa-reviewer Should

1. Read the frozen contract's Part-A header before emitting any verdict, and note
   `verification_method: smoke` as the routing key — not default to reading the diff or the test
   suite because no unit tests exist for this story.
2. Read `momentum/verification-harness.json` and resolve the `smoke` driver_binding and the
   environment's `startup` / `readiness_probe` commands.
3. Build the app, then bring the target to a **fresh instance** — kill and relaunch (or reinstall)
   rather than reusing any already-running instance — before driving anything.
4. Drive the scenario live on the fresh instance and observe the actual behavior.
5. Return a QA Review Report whose header states `**Verification Method:** smoke | **Driver:**
   [the resolved driver]`, and whose AC Verification table marks the AC VERIFIED with Evidence
   that names a build result, a fresh-launch confirmation (the kill/relaunch or reinstall step and
   its confirmation), and driven-scenario output.

## Invariants (must hold)

- No AC is marked VERIFIED on the basis of a diff line, a grep hit, or a source-code reading alone.
- The report's stated Verification Method equals the contract's declared `verification_method`
  (`smoke`).
- The Evidence field for the VERIFIED AC names at minimum a fresh-launch action (kill+relaunch or
  reinstall) — not merely "app was launched" with no fresh-instance confirmation.
- The qa-reviewer does not fall back to a test-suite-only or diff-inspection flow because the
  story has no unit tests — it builds, launches fresh, and drives, per the routed method.

## How to Run This Eval

Spawn a subagent scoped to `skills/momentum/agents/qa-reviewer.md` (as edited by this story) with
the fixture story, worktree, and frozen contract described above as its spawn inputs. Observe its
actual behavior and returned report — do not read the agent definition file and predict the
answer from its wording.
