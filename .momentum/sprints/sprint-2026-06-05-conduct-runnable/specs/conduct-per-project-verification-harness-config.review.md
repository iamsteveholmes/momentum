# conduct-per-project-verification-harness-config — Document Review Contract

```yaml
story_slug: conduct-per-project-verification-harness-config
verification_method: document-review
harness_profile: document-review
contract_path: .momentum/sprints/sprint-2026-06-05-conduct-runnable/specs/conduct-per-project-verification-harness-config.review.md
how_dev_self_checks: |
  Before you signal done, open the verification-harness configuration file you produced and
  confirm a fresh reader could verify every claim below by reading ONLY that file. Walk the
  checklist: does the file still parse as valid configuration (no syntax error); does it
  document, in a way the developer can follow, how a real product project overrides the
  every-surface-skipped default so that runnable change types (the kind with an app to launch,
  an endpoint to hit, or a script to run) get a real way to run instead of being skipped;
  for each such runnable surface, is a concrete real runner named rather than left as "skip";
  is there a place a project lists itself and the surfaces it turns on, distinct from the
  shared default; is the startup / readiness information those runners need filled in rather
  than left empty; and is it stated plainly that leaving everything skipped is the deliberate
  carve-out for a project with no app to run (so a markdown-only repo is correctly served by
  the default, while a real product repo is not silently skipped)? If a reader cannot confirm
  each of these from the file alone, the configuration scaffolding is not yet complete.
coverage_disposition: dedicated-run
covered_by_scenario: null
acceptance_criteria_ref: .momentum/stories/conduct-per-project-verification-harness-config.md#acceptance-criteria
platforms: [host]
```

**Harness Profile:** document-review

## Document Under Review

`momentum/verification-harness.json` — the verification-harness configuration this story extends so that a real product project can configure runnable execution surfaces instead of having every surface skipped. All claims below are confirmable by reading this file (and confirming it parses) without access to any engine source code.

## Required Claims

- [ ] The file parses cleanly as structured configuration — a reader can load it without a syntax error.
- [ ] The file provides a per-project override path: a project may declare itself and the set of execution surfaces it activates, kept separate from the shared default block (the default is not edited in place to serve one project).
- [ ] For each runnable change type a real product project would exercise (at minimum: an application/UI surface, a backend/endpoint surface, and a script/command surface), the configuration shows a concrete real runner configured for that surface rather than the value `skip`.
- [ ] The application/UI surface names a real UI driver (e.g., a Maestro/Playwright-class runner), not `skip`.
- [ ] The backend/endpoint surface names a real request runner (e.g., a curl/bash-class runner), not `skip`.
- [ ] The script/command surface names a real command runner (e.g., a shell/cmux-class runner), not `skip`.
- [ ] The startup and readiness information the configured runners depend on is filled in (no longer empty) wherever a runnable surface is activated, so a runner knows how to bring the environment up and confirm it is ready before a scenario executes.
- [ ] The configuration states plainly that an all-surfaces-`skip` posture is the deliberate carve-out for a project with no application to run (a markdown/bash-only repo), so the default correctly serves such a repo while a product repo configures real runners.
- [ ] The override is additive: turning on real runners for a product project does not require deleting or breaking the shared default that the no-app repo relies on.

## Required Sections

- [ ] A shared default block that maps execution surfaces to their default disposition.
- [ ] A per-project section where a project declares itself and the execution surfaces it activates with real runners.
- [ ] Startup / readiness environment information populated for the activated runnable surfaces.
- [ ] A stated rationale (inline note or documented intent) that all-surfaces-`skip` is the legitimate carve-out for a no-app repo, distinguishing it from a silent verification gap on a product repo.

## Pass Criteria

- The file parses, and every Required Claim is confirmable by reading the file alone.
- All Required Sections are present.
- At least the three runnable surfaces (app/UI, backend, script) each name a concrete real runner instead of `skip` in the per-project override, with the startup/readiness information they need populated.
- The all-`skip` default is explicitly framed as the intentional carve-out for a no-app repo, not as the only available behavior.

## Fail Criteria

- The file does not parse, or any required claim cannot be confirmed from the file alone.
- A runnable surface (app/UI, backend, or script) for a product project is still left as `skip` with no real runner configured.
- There is no per-project override path — the only way to enable a runner would be to overwrite the shared default that the no-app repo depends on.
- The startup / readiness information remains empty for an activated runnable surface, so a configured runner has no documented way to bring up or confirm its environment.
- The configuration does not state that all-surfaces-`skip` is the deliberate no-app carve-out, leaving a product repo unable to tell an intentional skip from a silent gap.
