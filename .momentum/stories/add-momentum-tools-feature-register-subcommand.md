---
title: Add momentum-tools feature register so features can enter the registry via the sole-writer path
story_key: add-momentum-tools-feature-register-subcommand
status: ready-for-dev
epic_slug: ad-hoc
feature_slug:
story_type: feature
priority: medium
depends_on: []
touches:
  - skills/momentum/scripts/momentum-tools.py
  - skills/momentum/scripts/test-momentum-tools.py
  - _bmad-output/planning-artifacts/prd.md
  - .claude/rules/impetus.md
change_type:
  - script-code
  - specification
  - rule-hook
surface: cli
verification_method_advisory: bash
---

# Add momentum-tools feature register so features can enter the registry via the sole-writer path

## Story

As a developer,
I want a `momentum-tools feature register` subcommand,
so that new features can legitimately enter `.momentum/features.json` while `feature verify` stays the sole verdict writer.

## Description

From sprint-2026-08-03 end-gate (Option A). The registry is a closed loop: `feature verify` refuses unknown slugs (`cmd_feature_verify`), `feature --help` shows only `verify`, FR146 forbids hand edits, and the greeting eval bars sprint-planning from placeholders. No new feature can enter, so every sprint routes to the maintenance fallback and the DEC-040 loop never engages.

`feature register` is the registry's door and the **sole creator of entries**. `feature verify` remains the **sole writer of `status` and `last_verified`** (verdicts). Register never records a verdict.

**Pain context:** Every sprint routes permanently to the maintenance fallback.

**Command:** `momentum-tools feature register <feature-slug> --name <text> --acceptance-condition <one sentence> [--design-ref <path-or-ref>] [--epic-slugs a,b]`

## Acceptance Criteria

1. **Registers a new entry.** Given a registry with other entries, when `feature register loom-export --name "Loom export" --acceptance-condition "A GM can export a tapestry and open it on a second machine."` runs, it exits 0 with the standard success envelope (`action: feature_register`, `success: true`, `slug`, `status: "absent"`, `path`), and `features.json` gains an entry keyed by the slug with exactly: `slug`, `name`, `acceptance_condition`, `status` = `"absent"`, `last_verified` = `null`, `design_ref` = `null`. No other key is present when the optional flags are omitted.
2. **Optional fields.** When `--design-ref` is given, `design_ref` holds it verbatim; when `--epic-slugs a,b` is given, `epic_slugs` is the list `["a","b"]` (whitespace around items trimmed, empty items dropped). When `--epic-slugs` is omitted the key is absent. Epic slugs are never checked against `epics.json`; an unknown epic slug never causes a refusal.
3. **Creates the registry when absent.** Given no `.momentum/features.json`, registering a valid feature creates the file as a JSON object keyed by slug containing only the new entry. This is the only code path in the tool that creates the file: `feature verify`, `tasting status`, `tasting brief`, sprint planning and sprint closure still never create it when it is absent.
4. **Never overwrites.** Given a slug already registered in any status (`absent`, `failing`, `passing`), registering it again exits non-zero, the error names the slug and its existing status, and the file is byte-identical afterward. A `passing` or `failing` feature is never reset to `absent`.
5. **Rejects invalid slugs.** A slug that is not kebab-case (lowercase letters and digits in hyphen-separated groups, e.g. `Loom_Export`, `loom--export`, `-loom`, empty) exits non-zero naming the slug; the file is byte-identical, and if it was absent it is still not created. A dash-leading slug such as `-loom` typed without `--` is refused by argparse itself (non-zero, usage error, nothing written); it needs `--` to reach the kebab-case message that names the slug.
6. **Rejects empty text.** An empty or whitespace-only `--name` or `--acceptance-condition` exits non-zero naming the offending flag, with the same byte-identical / not-created guarantee. Valid text is persisted as supplied (not stripped or altered).
7. **Rejects a corrupt registry.** A present `features.json` that is invalid JSON or whose top level is not an object exits non-zero with an error naming the path; the file is left byte-identical and is never repaired or replaced.
8. **Missing required flags are refused.** Omitting `--name` or `--acceptance-condition` is an argparse-level refusal (non-zero) that writes nothing.
9. **Verify stays the sole verdict writer.** `feature register` never writes `last_verified` other than `null` and never sets a status other than `"absent"`. After `register` then `verify --verdict pass`, the entry is `passing` with a complete `last_verified`, and the registered `name`, `acceptance_condition`, `design_ref` and `epic_slugs` are preserved. `feature verify` on an unregistered slug is still rejected.
10. **Registering leaves neighbors untouched.** Existing entries in the registry are preserved exactly (values and key order); the new entry is appended.
11. **Consumers keep working.** With a freshly registered (`absent`) entry, the Impetus N-of-M count treats it as part of M and not N; `tasting status` and `tasting brief` run without error and do not claim it; the planning step lists it as a candidate; `sprint complete` with that slug in `goal_conditions` refuses to close, listing it as unverified (reason `no-verdict` — registered but never verified; `missing-entry` is reserved for a slug not in the registry) and leaving the registry unchanged, until `verify` records a pass with build SHAs. N-of-M is computed by the Impetus rule only (no CLI path); the verifiable CLI/file-level check is that after registering, the registry holds one `passing` entry and two entries in total, and the new entry's status is `absent` (the input to the rule's "absent counts toward M, never N" clause). The greeting wording itself is a hands-on drive item.
12. **Discoverable.** `feature --help` lists both `verify` and `register`; `feature register --help` documents every flag; the usage docstring at the top of `momentum-tools.py` lists the command.
13. **Spec and rule wording agree.** FR146 in `prd.md` states that `feature register` is the sole creator of registry entries and the only path that creates the file while `feature verify` remains the sole writer of status and last_verified, and that re-registration is refused; `.claude/rules/impetus.md` no longer implies `feature verify` is the only code that may bring the registry file into existence (Impetus remains read-only).

## Tasks / Subtasks

- [ ] Task 1: Write failing tests in `skills/momentum/scripts/test-momentum-tools.py`, next to the `feature verify` tests, and register them in the main runner list (AC: 1-12)
  - [ ] 1.1 Success: exact entry shape, envelope, defaults (AC 1)
  - [ ] 1.2 Optional `--design-ref` / `--epic-slugs` handling incl. unknown epic slug accepted (AC 2)
  - [ ] 1.3 Creates absent registry; verify/consumers still do not (AC 3)
  - [ ] 1.4 Re-registration refused for absent, failing and passing; error names status; byte-identical (AC 4)
  - [ ] 1.5 Invalid slug, empty name, empty acceptance condition, corrupt JSON, non-object: refused, byte-identical, absent file not created (AC 5, 6, 7)
  - [ ] 1.6 Missing required flags (AC 8)
  - [ ] 1.7 Register then verify round trip; verify unknown slug still rejected; neighbors untouched (AC 9, 10)
  - [ ] 1.8 Consumer compatibility with an `absent` entry: registry file-level N-of-M inputs (status counts), tasting status/brief, `sprint complete` goal_conditions refusal with reason `no-verdict` (AC 11)
  - [ ] 1.9 Help lists both subcommands (AC 12)
- [ ] Task 2: Implement `cmd_feature_register` in `skills/momentum/scripts/momentum-tools.py` and wire the `register` parser under the `feature` group (AC: 1-10, 12)
  - [ ] 2.1 Validate all inputs before any file access; reuse `error_result("feature_register", ...)` and `result(...)` envelope and `write_json` like `cmd_feature_verify`
  - [ ] 2.2 Load existing registry with the same JSON / object checks as verify; absent means start from `{}`
  - [ ] 2.3 Refuse existing slug with status in the message; append entry; `write_json`
  - [ ] 2.4 Update usage docstring and the "sole writer" comments (feature group comment, tasting block comment) to describe creator vs verdict-writer split
- [ ] Task 3: Update FR146 wording in `_bmad-output/planning-artifacts/prd.md` (AC: 13)
- [ ] Task 4: Adjust the registry-creation wording in `.claude/rules/impetus.md` (AC: 13)
- [ ] Task 5: Run the full `test-momentum-tools.py` suite; confirm no regressions (AC: all)

## Dev Notes

### Decision Authority

DEC-040 D1 (`_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`) adopts `.momentum/features.json` as the acceptance-testing registry and names `feature verify` as sole writer. FR146 (`_bmad-output/planning-artifacts/prd.md`) says "every mutation flows through this one subcommand". Both predate any way to add a feature; this story introduces the creation door without relaxing verdict authority. Entry schema is FR146's: slug, name, acceptance_condition, status (absent by default), last_verified, optional informational epic_slugs, design_ref.

### Current State of affected files

- `momentum-tools.py`: `cmd_feature_verify` (about line 2386) validates inputs, loads the registry with JSON and object checks, mutates one entry and calls `write_json`. Envelope via `result()` / `error_result()`. Parser group `feature` with only `verify` (about line 4066). `features_path()`, `_read_json_object()` and read-only consumers (`_load_features_registry`, tasting, goal_conditions, closure) must stay read-only.
- `test-momentum-tools.py`: `setup_features_project`, `features_path_of`, `read_features`, `run_tool` and `FV_*` constants exist; feature verify tests are registered around line 3879.
- Preserve: verify's behavior (including rejecting a missing registry and unknown slugs) must not change.

### Design decisions (resolved, no open questions)

- Register creates the file when absent; verify does not.
- Errors are distinct for invalid JSON vs non-object, mirroring verify.
- Slug regex: `^[a-z0-9]+(-[a-z0-9]+)*$`.
- Key order for the entry: slug, name, acceptance_condition, status, last_verified, design_ref, then epic_slugs if given.
- Atomic/lock-safe writes are out of scope (stub `make-write-json-atomic-and-lock-safe`); use the existing `write_json`.

### Out of scope / follow-ups

- Wiring `feature register` into sprint-planning or any skill (follow-up story).
- `list`, `remove`, `rename` subcommands.
- `write_json` atomicity.

### Architecture Compliance

Registry integration seams stay exactly three (planning, closure, Impetus). Register is a registry-maintenance command, not a fourth consumer. Epic slugs remain informational.

### Testing Requirements

TDD: tests first, all under `test-momentum-tools.py` using the temp-project helpers. Run with `/Users/steve/.local/share/mise/installs/python/latest/bin/python3 skills/momentum/scripts/test-momentum-tools.py` (Python 3.14, not `/usr/bin/python3`). Every refusal test asserts byte-identical file (or still-absent file).

### Project Context Reference

Surface is `cli`; verification is by running the command against a temp project and observing JSON output and file bytes.

### Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2 → script-code (TDD)
- Task 3 → specification (direct authoring with cross-reference verification)
- Task 4 → rule-hook (functional verification)

---

### Universal DoD

- [ ] The capability is reachable from the application's entry point by a user who has read
      no code. (verification-standard.md §5)

---

### script-code Tasks: TDD via bmad-dev-story

1. **Red:** write failing tests first and confirm they fail.
2. **Green:** implement the minimum to pass.
3. **Refactor** while green.

DoD: tests written and passing; no regressions in the existing suite; follow existing script structure.

### specification Tasks: Direct Authoring with Cross-Reference Verification

Update FR146 text; verify references (DEC-040 D1, FR59/FR139/FR54 seams) still resolve and format matches the neighboring FRs.

- [ ] Cross-references resolve
- [ ] Format follows PRD conventions
- [ ] AVFL checkpoint result documented

### rule-hook Tasks: Functional Verification

State the expected behavior ("Impetus reads the registry only and never creates it; `feature register` is the creation path") and confirm the rule file stays internally consistent.

- [ ] Expected behavior documented in Dev Agent Record
- [ ] Format matches existing rule files

A frozen verification contract exists for this sprint (in `sprints/{sprint-slug}/specs/{story-slug}.{ext}`). Dev reads the Part-A header (how_dev_self_checks, verification_method, harness_profile) as a self-check before signaling done, and never reads the verifier body beyond sections explicitly referenced.

### References

- DEC-040 D1: `_bmad-output/planning-artifacts/decisions/dec-040-delivery-loop-closure-2026-08-02.md`
- FR146: `_bmad-output/planning-artifacts/prd.md`
- Related stub: `make-write-json-atomic-and-lock-safe`
- Epic context: `ad-hoc` (from _bmad-output/planning-artifacts/epics.json)
