---
title: momentum-tools feature verify — human verdict recorder and sole writer of features.json
story_key: momentum-tools-feature-verify-human-verdict-recorder-and
status: ready-for-dev
epic_slug: momentum-feature-taxonomy-maintenance
feature_slug:
story_type: practice
priority: high
change_type:
  - script-cli
verification_method_advisory: bash
depends_on: []
touches:
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
  - .momentum/features.json
---

# momentum-tools feature verify — human verdict recorder and sole writer of features.json

## Story

As a developer,
I want a new `momentum-tools feature verify <feature-slug> --verdict pass|fail --evidence <text> --build <backendSha>:<clientSha>` CLI subcommand that records a HUMAN PASS/FAIL verdict against a feature's acceptance_condition in `.momentum/features.json`,
so that feature completion becomes a real, verified field in the practice's state instead of an orphaned file nobody writes to — closing the gap where 0 of 15 features ever reached done across 10 sprints while story throughput rose.

## Description

This story delivers the write path for the DEC-040 D1 acceptance-testing registry: a new
`feature verify` subcommand on the `momentum-tools` CLI that records a human PASS/FAIL verdict
against a named feature in `.momentum/features.json`, stamping `last_verified` with the date, the
verdict, the human's evidence text, and the paired build SHAs the verdict was observed against.

The registry is failing-by-default. Its status enum is `absent | failing | passing`, and a feature
reaches `passing` only when a human verdict says so against a named build. Nothing infers, derives,
or defaults a feature to `passing`.

This command is the **sole write path to feature status**. No agent, skill, or workflow may write
`status` or `last_verified` in `.momentum/features.json` by any other route (architecture.md
Read/Write Authority, row `momentum-tools feature verify`). The registry is per-project and is
deliberately an acceptance-testing entity, separate from the work-tracking epic layer — features
touch exactly three seams and no others (DEC-040 D1 amending DEC-034).

**Scope boundary — write path only.** This story ships the command. It does not author registry
content, and it does not implement any consumer. The three read-only consumer seams
(sprint-planning `goal_conditions` declaration, sprint-closure verdict requirement, Impetus
N-passing headline report) and the daily tasting brief are separate stories; they must be able to
read the shape this command writes, which is what the schema ACs below pin down. Populating a real
`.momentum/features.json` (the nornspun design reconciliation named in the DEC-040 D1 gate) is
Phase 3 work and is out of scope here — this story's verification runs against fixture registries.

**Pain context:** the Nornspun delivery discovery (`docs/research/nornspun-delivery-discovery-2026-08-02/`)
found 0 of 15 features ever reached done across 10 sprints while story throughput rose. Feature
completion was not a field that existed anywhere in sprint state, and `features.json` was orphaned
with zero workflow references. This command is the motor organ that makes the outcome layer real.

## Acceptance Criteria

1. **The subcommand exists and is invocable.** `momentum-tools feature verify <feature-slug> --verdict pass|fail --evidence <text> --build <backendSha>:<clientSha>` runs from the `momentum-tools` PATH shim. A new `feature` command group is registered alongside the CLI's existing top-level commands, and both `--help` and the module usage docstring document it.

2. **A verdict sets status, and only these two statuses are ever written.** Recording `--verdict pass` sets the target feature's `status` to `passing`; recording `--verdict fail` sets it to `failing`. The command never writes `absent` and never writes any value outside the `absent | failing | passing` enum.

3. **Every recorded verdict stamps a complete `last_verified`.** The target feature's `last_verified` carries the verdict, the ISO date the verdict was recorded, and both paired build SHAs — backend and client kept distinguishable — plus the evidence text as supplied. No field is omitted or left blank. (The first three are D1's schema exactly; `evidence` is a deliberate, flagged extension — see Dev Notes → Decision Authority → "One flagged extension to D1".)

4. **A malformed build pair is rejected before anything is written.** `--build` must be exactly two non-empty commit SHAs separated by a single colon. A single SHA, an empty side, extra colons, or a non-hex value is rejected with a message naming the problem, a non-zero exit, and `.momentum/features.json` left byte-identical.

5. **Empty evidence is rejected before anything is written.** A missing, empty, or whitespace-only `--evidence` value is rejected with a non-zero exit and no change to the registry. A verdict with no observation behind it is not recordable.

6. **An unknown feature slug is rejected and never invented.** If the named slug is not already a key in the registry, the command exits non-zero with a message naming the slug and the registry path, and creates no entry. The command records verdicts against existing features; it does not author the registry.

7. **A missing registry is a clear error, not a silent bootstrap.** If `.momentum/features.json` does not exist, the command exits non-zero with a message naming the expected path and does not create the file.

8. **Failing-by-default holds end to end.** A feature entry with no `last_verified` on record is never `passing`. A feature becomes `passing` only through a recorded `pass` verdict carrying its paired build SHAs, and a subsequent `fail` verdict moves it back to `failing`. There is no path — flag, default, or inference — by which the command reports a feature as passing without a recorded human pass.

9. **The write is surgical.** A successful run modifies exactly two fields (`status` and `last_verified`) on exactly the named feature. Every other field on that entry (`slug`, `name`, `acceptance_condition`, and the optional `epic_slugs` and `design_ref` links) and every other entry in the registry survive unchanged, with key ordering and JSON formatting consistent with how sibling `momentum-tools` commands write state.

10. **Output matches the CLI's existing result contract.** Success and failure both emit the standard `momentum-tools` JSON result envelope (`action`, `success`, plus command detail), exiting 0 on success and 1 on failure — the same shape sibling subcommands produce, so callers parse one format.

11. **Three seams and no fourth.** A run writes to `.momentum/features.json` and nothing else — no `practice-ledger.jsonl` append, no `stories/index.json` or `sprints/index.json` write, no other state file touched. The registry path resolves per-project from the project root exactly as sibling commands resolve their state files.

## Tasks / Subtasks

- [ ] **Task 1 — Register the `feature` command group and `verify` subcommand** (AC1, AC10)
  - [ ] In `build_parser()` in `skills/momentum/scripts/momentum-tools.py`, add a `feature` subparser group with a `feature_action` sub-subparser, following the two-level pattern already used by `sprint`, `agent`, `quickfix`, and `practice-ledger`.
  - [ ] Add the `verify` subcommand with a positional `feature-slug`, and `--verdict` (choices `pass`/`fail`), `--evidence`, and `--build` as required options.
  - [ ] Wire `set_defaults(func=cmd_feature_verify)`.

- [ ] **Task 2 — Add registry path resolution and load helpers** (AC7, AC11)
  - [ ] Add a `features_path(project_dir)` helper returning `.momentum/features.json`, matching the existing `stories_path()` / `sprints_path()` convention.
  - [ ] Resolve the project root via the existing `resolve_project_dir()` so the registry is per-project and honours `CLAUDE_PROJECT_DIR`.
  - [ ] Handle a missing registry as an explicit `error_result` naming the expected path — never create the file.

- [ ] **Task 3 — Implement `cmd_feature_verify`** (AC2, AC3, AC4, AC5, AC6, AC8, AC9)
  - [ ] Validate `--build` parses to exactly two non-empty hex SHAs on a single colon; reject otherwise before any read-modify-write.
  - [ ] Validate `--evidence` is non-empty after stripping; reject otherwise.
  - [ ] Resolve the feature slug against the loaded registry; `error_result` if absent, creating nothing.
  - [ ] Map `pass` → `status: passing` and `fail` → `status: failing`; write `last_verified` with date, verdict, evidence, and both SHAs kept distinguishable.
  - [ ] Mutate only `status` and `last_verified` on the named entry, then persist via the existing `write_json` helper so formatting matches sibling commands.
  - [ ] Emit the JSON result envelope via `result()` with the slug, resulting status, and registry path.

- [ ] **Task 4 — Update the module usage docstring** (AC1)
  - [ ] Add the `feature verify` usage line to the `Usage:` block at the top of `momentum-tools.py`, alongside the existing command lines.
  - [ ] Update the module docstring's sole-writer sentence so it records that this script also owns the feature-status write path.

- [ ] **Task 5 — Extend `test-momentum-tools.py` with `feature verify` coverage** (AC1–AC11)
  - [ ] Add the new tests to the existing suite at `skills/momentum/scripts/test-momentum-tools.py`, following its established subprocess-CLI pattern. Do not create a new test file or framework.
  - [ ] Extend `setup_project()` (or add a sibling fixture helper) so a fixture project can seed `.momentum/features.json` with at least two entries, one carrying `epic_slugs` and `design_ref`.
  - [ ] Exercise the happy path for both verdicts and confirm status, `last_verified` completeness, and exit code.
  - [ ] Exercise each rejection path — malformed build pair, empty evidence, unknown slug, missing registry — asserting non-zero exit AND a byte-identical registry after each.
  - [ ] Compare the whole fixture registry before and after a successful run to prove only the two fields on the one named entry changed (AC9).
  - [ ] Confirm no other state file under `.momentum/` was created or modified during any run (AC11).
  - [ ] Run the full suite and confirm all tests pass, existing ones included.

## Dev Notes

### Decision Authority

`_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md` **D1** is the
schema authority for this story. Implement D1 as written — this design already churned once
(DEC-034 unified features into epics; D1 amends that by separating the outcome layer back out as an
acceptance-testing registry). Do not re-derive the schema, re-litigate features-vs-epics, or extend
the integration surface.

D1's binding points, quoted in substance:

- **Schema:** `slug`, `name`, `acceptance_condition`, `status` (`absent | failing | passing` —
  failing-by-default), `last_verified` {date, build SHAs, verdict}, optional informational
  `epic_slugs` (many-to-many, **never validated, never blocking**) and `design_ref` links.
- **Sole writer:** "the `momentum-tools feature verify` command recording a human verdict."
- **Exactly three seams and no others:** (1) sprint planning declares `goal_conditions`;
  (2) sprint closure records a human PASS/FAIL per named condition against a paired build;
  (3) Impetus reports N passing as the practice's headline number.
- **Why the DEC-034 cost does not return:** no epic-facing skill reads features. The prior failure
  was making features a peer of epics inside every skill. Three seams total is the whole design —
  adding a fourth (a ledger event, an index mirror, an epic cross-check) reintroduces exactly the
  coordination cost DEC-034 killed.

`epic_slugs` being never validated and never blocking is load-bearing: the command must not verify
that a listed epic exists, and must not fail or warn when one doesn't.

Paired build SHAs trace to **DEC-040 D8** (SHA admissibility): nobody may review a build version
control cannot name, and every report cites the two SHAs. That is why `--build` is mandatory and
strictly validated rather than optional metadata.

**One flagged extension to D1.** D1's written schema for `last_verified` is `{date, build SHAs,
verdict}` — three sub-fields, no evidence. This story persists a fourth, `evidence`, and that is a
deliberate extension rather than an oversight. It is grounded: the `--evidence` flag appears in the
underlying research recommendation the decision was built from
(`docs/research/nornspun-delivery-discovery-2026-08-02/synthesis.md` — `momentum-tools feature
verify --verdict --evidence --build <sha>:<sha>`) and in the developer's own captured CLI signature
in the Story statement above. Discarding the human's observation at the moment of recording it would
defeat D4's tasting-brief loop, which needs to know what was actually seen. **Because the downstream
consumer stories read the shape this command writes, this extension is a contract — flag it to the
decision owner for confirmation rather than treating it as settled.** If it is rejected, drop
`evidence` from the persisted object and keep the flag as required-but-unstored input; nothing else
in this story changes. Everything else in the schema is D1 as written — do not extend further.

### Current State of Affected Files

**`skills/momentum/scripts/momentum-tools.py`** (~3,091 lines) — the practice's deterministic CLI.
Relevant existing structure the implementation should follow rather than reinvent:

- `build_parser()` registers top-level groups via `subparsers.add_parser(...)`, each with its own
  `add_subparsers(dest=..., required=True)`. Existing groups: `sprint`, `session`,
  `specialist-classify`, `agent`, `quickfix`, `practice-ledger`, `triage`, `version`, and the flat
  `feature-status-hash`. **There is no `feature` group yet** — this story adds it. Note that the
  existing flat `feature-status-hash` command is a separate, older artifact and is not part of this
  command group.
- Helpers to reuse: `resolve_project_dir()` (honours `CLAUDE_PROJECT_DIR`, else walks up to `.git`),
  `stories_path()` / `sprints_path()` (the naming convention `features_path()` should match),
  `read_json()`, `write_json()` (writes `indent=2, ensure_ascii=False` plus trailing newline),
  `result()` and `error_result()` (the JSON envelope + exit-code contract, exit 0/1).
- `cmd_practice_ledger_append` is a good reference for the validate-then-write shape: it validates
  enum and JSON inputs with `error_result` before touching any file.

**`skills/momentum/scripts/test-momentum-tools.py`** (~210 KB, 209 `test_` functions) — the existing
fixture-driven suite for the script above. Drives the CLI as a subprocess; `setup_project()` creates a
temp project with `.momentum/` and `git init` so project-root resolution works. New tests go here.

**`.momentum/features.json`** — **does not exist yet.** Its absence is expected. This story must not
create it as a side effect; registry content arrives via the DEC-040 Phase 3 design reconciliation.
All verification here runs against fixture registries in temp directories.

**`skills/momentum/bin/momentum-tools`** — bash PATH shim that resolves and execs the Python script;
`~/.local/bin/momentum-tools` symlinks to it. No change needed, but it is how the command is invoked
during verification.

### Architecture Compliance

The architecture spec impact for DEC-040 has already landed (editHistory entry 2026-08-02) — this
story implements against it and should not need to amend it.

- **`.momentum/` State Layout:** `features.json` returns at `.momentum/features.json` as a standalone
  per-project acceptance-testing registry with failing-by-default statuses and human-only verdicts.
  Planning artifacts stay under `_bmad-output/planning-artifacts/`; this registry is operational
  state and correctly lives under `.momentum/`.
- **Read/Write Authority table** already carries the row: `momentum-tools feature verify` →
  `.momentum/features.json`, "**Sole writer of `.momentum/features.json`** (DEC-040 D1) — records
  human PASS/FAIL verdicts with paired-build SHAs; no agent or skill may write feature status by any
  other path. Read-only consumers: sprint-planning (`goal_conditions` declaration), Impetus
  (N-passing headline report), daily tasting-brief generator (DEC-040 D4)."
- **Sole-writer pattern:** consistent with how `momentum-tools` already owns `stories/index.json` and
  `sprints/index.json`. Same discipline — the CLI validates and mutates; skills call the CLI.
- **`epics.json` is untouched.** The epic layer remains the work organizer exactly as DEC-034 left
  it. This command must not read or write `epics.json`.

### Testing Requirements

**Extend the existing suite — do not create a new one.**
`skills/momentum/scripts/test-momentum-tools.py` is the established fixture-driven test suite for
this exact script (~210 KB, 209 `test_` functions, run with `python3 test-momentum-tools.py`, or
`uv run python skills/momentum/scripts/test-momentum-tools.py`). It drives the CLI as a subprocess
against `SCRIPT = Path(__file__).parent / "momentum-tools.py"` and builds throwaway projects with a
`setup_project()` helper that creates a temp dir, lays down `.momentum/`, and runs `git init` so
`resolve_project_dir()` resolves correctly. New `feature verify` tests belong there, following that
same pattern. Sibling DEC-040 stories touching this script extend the same suite.

What is genuinely absent is any *automatic* runner: there is no repo-root `pytest.ini`,
`conftest.py`, `tox.ini`, `mise.toml`, or CI wiring, so the suite is invoked explicitly. Do not
stand up a new framework.

This matches the `script-cli` → `bash` routing in
`skills/momentum/references/rules/verification-standard.md`: run the real command with
representative inputs and observe that output and state match spec.

- Extend `setup_project()` (or add a sibling helper) so a fixture can seed `.momentum/features.json`
  with at least two feature entries, one carrying `epic_slugs` and `design_ref`.
- Drive the CLI as a subprocess, not the Python function, so argparse wiring is exercised.
- Every rejection-path check asserts two things: non-zero exit **and** an unchanged registry. Exit
  code alone does not prove nothing was written.
- Snapshot the fixture registry before and after a successful run and compare — that is the only
  honest check for AC9's surgical-write requirement and AC11's no-fourth-seam requirement.
- The whole suite must still pass end to end; new tests must not regress the existing 209.

### Project Structure Notes

- The command implementation belongs in `skills/momentum/scripts/momentum-tools.py` beside the other
  `cmd_*` functions, with its parser wiring in `build_parser()`. Placing the new `feature` group near
  the existing `feature-status-hash` registration keeps related commands legible.
- The registry it writes is operational state at `.momentum/features.json` — created by a later
  story, never by this command.
- No new skill directory, no new script file, no new rule file, and no new test file. This story is a
  CLI extension in `momentum-tools.py` plus its usage docstring, with new tests added to the existing
  `test-momentum-tools.py` suite beside it.

### References

- DEC-040 D1 — `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md` (schema authority; amends DEC-034)
- DEC-040 D8 — same document (paired-build SHA admissibility — why `--build` is mandatory)
- `_bmad-output/planning-artifacts/architecture.md` — `.momentum/` State Layout (features.json note) and Read/Write Authority table (`momentum-tools feature verify` row), editHistory entry 2026-08-02
- `skills/momentum/references/rules/verification-standard.md` — §1 routing table (`script-cli` → `bash`)
- `skills/momentum/scripts/momentum-tools.py` — target file; `build_parser()`, `resolve_project_dir()`, `read_json`/`write_json`, `result`/`error_result` conventions
- `skills/momentum/scripts/test-momentum-tools.py` — the existing 209-test fixture-driven suite for that script; `setup_project()` helper and subprocess-CLI pattern to follow
- `docs/research/nornspun-delivery-discovery-2026-08-02/` — pain-context research (0 of 15 features done across 10 sprints)
- Epic context: `momentum-feature-taxonomy-maintenance` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2, 3, 4, 5 → `script-cli` (user-facing CLI entry point; TDD-shaped implementation, fixture-driven verification)

---

### script-cli Tasks: Implementation and Verification

`momentum-tools` is a user-facing CLI the developer invokes by hand — it is a `script-cli` change,
not internal `script-code` automation. Note that `references/change-types.md` ships no `script-cli`
injection template; the guidance below adapts the `script-code` TDD template and adds the CLI-surface
requirements that template does not cover. The implementation discipline is the same
red-green-refactor loop, with the CLI surface itself as the unit under test.

1. **Red:** Add the new tests to `test-momentum-tools.py` first (Task 5) — happy path plus every
   rejection path — and confirm they fail against the current CLI, which has no `feature` group at all.
2. **Green:** Implement the parser wiring, helpers, and `cmd_feature_verify` until each check passes.
3. **Refactor:** Fold shared validation into helpers where it reads better, keeping the existing
   `momentum-tools` idiom (validate → `error_result` early, mutate, `result()`).

**CLI-specific requirements beyond standard script DoD:**

- **Envelope parity:** success and failure both emit the standard JSON result envelope via
  `result()` / `error_result()`. Do not print bare strings or invent a new output shape — callers
  parse one format across every subcommand.
- **Validate before mutate:** every rejection path must exit before the registry is opened for
  write. The ACs assert a byte-identical file after each failure, so a partial write is a defect.
- **Docstring is part of the deliverable:** the `Usage:` block at the top of `momentum-tools.py` is
  the CLI's discoverability surface. A subcommand missing from it is incomplete (AC1).
- **Resist scope creep into a fourth seam.** The temptation while implementing will be to also
  append a practice-ledger event, mirror status into an index, or validate `epic_slugs` against
  `epics.json`. All three are explicitly out of bounds under DEC-040 D1. AC11 exists to catch this.

**DoD additions for this story:**

- The command runs end to end against a fixture registry, for both verdicts.
- Every rejection path verified for non-zero exit **and** unchanged registry.
- A before/after comparison of the fixture registry shows exactly two changed fields on exactly one entry.
- No other file under `.momentum/` is created or modified by any run.
- `momentum-tools.py` module docstring lists the new subcommand.
- `python3 skills/momentum/scripts/test-momentum-tools.py` passes in full — new tests added there, no regressions in the existing 209.

**Frozen verification contract:** a frozen contract for this sprint exists at
`.momentum/sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Read the **Part-A header**
(`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signalling
done. Do not read the verifier body (Part B: scenarios, assertion scripts, Gherkin) beyond sections
`how_dev_self_checks` explicitly references.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
