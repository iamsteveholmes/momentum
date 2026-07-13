---
title: Conduct QA leg executes the story's verification method (smoke), not diff-only review
story_key: conduct-qa-execute-verification-method
status: ready-for-dev
epic_slug: momentum-conductor-core
feature_slug:
story_type: defect
priority: critical
change_type:
  - agent-definition
  - skill-instruction
verification_method_advisory: skill-invoke
depends_on:
  - conduct-qa-reviewer-normalization-adapter
  - conduct-coverage-deferral-preserve-code-review
touches:
  - skills/momentum/agents/qa-reviewer.md
  - skills/momentum/skills/conductor/workflow.md
---

# Conduct QA leg executes the story's verification method (smoke), not diff-only review

## Story

As a developer running a conduct build,
I want the build phase's QA leg to actually execute each story's routed verification method — for `smoke`, that means build + launch + drive on the story's declared targets — instead of degrading to diff-only inspection,
so that "looks done in the diff but doesn't work live" defects are caught per-story during the build, not deferred to the end-gate.

## Description

Root-caused from the nornspun campaign-init sprint (sprint-2026-05-30, conducted by hand
from the conduct RUNBOOK). All 15 stories passed per-story QA, yet the Phase-4 live
walkthrough found the headline feature functionally broken: the campaign-init conversation
was 100% client-local hardcoded copy that never called the backend. Per-story QA was
diff-inspection only — the app-ui code was never compiled or launched until Phase 4.

The decisive detail: the affected story specs **declared** `verification_method: smoke`
and even cited the assessment document ASR-004 verbatim ("the acceptance signal is live
on-device/desktop observation, not scenario pass counts" — 57/71 scenarios "passed" while
the live flow did nothing). The routing existed; the conduct build phase did not honor it.
The QA reviewer verified the diff against the verification contract textually instead of
executing the contract's method.

Scope: the conductor skill's build-phase QA stage (stage-2 REVIEWER A dispatch) and the
`qa-reviewer` agent contract it spawns must route on the frozen contract's
`verification_method` / `harness_profile` and EXECUTE it — `smoke` stories get a real
build + launch + drive pass (or a BLOCKED verdict when the environment cannot support one),
never a silent downgrade to document/diff review. The direct template already exists:
`e2e-validator.md` is a harness-driven, method-polymorphic executor with
BLOCKED-on-absent-harness and BLOCKED-on-startup-failure semantics; the build-phase QA leg
must adopt the same execution model.

**Pain context:** An entire 15-story sprint reached the end-gate "green" while its core
feature didn't work end-to-end; the failure class was already documented in ASR-004 and
named in the story specs, and the engine still skipped the antidote. Every conduct run
inherits this until fixed. Discovered during sprint-2026-05-30 root-cause analysis
(2026-06-10).

## Acceptance Criteria

1. **Routes on the frozen contract.** When the conduct build-phase QA leg runs for a story,
   the `qa-reviewer` reads the story's frozen verification contract Part-A header
   (`verification_method`, `harness_profile`) and resolves the driver + environment from
   `momentum/verification-harness.json`. It selects its execution behavior from the declared
   `verification_method`; it does not default to a test-suite-only or diff-inspection flow
   when the contract declares an executable method. Observable: the QA report names the
   `verification_method` and driver it routed on, and that value equals the contract's
   Part-A `verification_method`.

2. **`smoke` executes build + launch + drive.** For a story whose contract declares
   `verification_method: smoke` in a supporting environment, the QA leg builds the app,
   launches it on the target(s) named by the harness profile — killing and relaunching (or
   reinstalling) to a fresh instance first, never driving a still-running or cached build — and
   drives the story's scenarios live. Each per-AC verdict (VERIFIED / PARTIAL / MISSING) is backed
   by runtime evidence — a build result, a fresh-launch confirmation, and driven-scenario output.
   No `smoke`-story AC is marked VERIFIED on grep / diff / source-inspection evidence alone.

3. **Every executable method executes; only `document-review` inspects.** The QA leg
   executes the routed method for every executable `verification_method`
   (`skill-invoke`, `behavioral-trigger`, `bash`, `curl`, `smoke`) — invoking, triggering,
   running, or driving as the method prescribes — and reserves inspection-only verification
   for `document-review`. Observable: for an executable-method story, every VERIFIED /
   PARTIAL / MISSING verdict cites execution evidence (command output, launch/drive
   observation, invocation result), not a diff line, as its basis.

4. **BLOCKED when the environment can't support execution — never PASSED-by-diff.** When the
   routed method cannot execute — harness absent, no emulator/simulator or backend reachable,
   or the harness `startup` / `readiness_probe` fails after a good-faith startup attempt —
   the `qa-reviewer` returns a BLOCKED verdict naming the missing prerequisite. It never
   substitutes a VERIFIED / PASS verdict derived from diff or document review for an
   executable-method story. (Mirrors `e2e-validator.md` BLOCKED-on-absent-harness and
   BLOCKED-on-startup-failure.)

5. **Conductor silent-downgrade guard.** In conductor stage-2, REVIEWER A return validation
   rejects a `qa-reviewer` report that marks any executable-method AC VERIFIED without
   execution evidence (diff-only / source-only). The rejected leg re-runs once; if the re-run
   still returns VERIFIED-without-execution-evidence while the environment is available, the
   Conductor escalates rather than advancing the story to merge. A BLOCKED verdict (genuine
   environment unavailability with the prerequisite named) is a legitimate outcome and is NOT
   treated as a downgrade.

6. **Reads the routing key before verdicting (observable).** When the QA leg is invoked on a
   story, the `qa-reviewer`'s execution trace shows it reading the frozen contract Part-A header
   (`verification_method`, `harness_profile`) and `momentum/verification-harness.json` *before* it
   emits any per-AC verdict — a run that produces verdicts without first reading the contract header
   and harness config is non-compliant. (The instruction wording that makes this observable —
   generalizing the agent's "Execute the Test Suite" step to "execute the routed verification method"
   and retaining the "reading source is never a substitute for execution" and MISSING-vs-BLOCKED
   constraints — is specified in Task 1.)

7. **No regression to normalization or coverage-deferral.** The stage-2 REVIEWER A → canonical
   finding-schema normalization action and the covered-by-composition deferral branch are
   preserved: BLOCKED findings still normalize to `severity: critical`; on the
   covered-by-composition path REVIEWER A (the dedicated QA run) remains un-dispatched and its
   deferral to the named integration scenario is unchanged. The silent-downgrade guard applies
   only on the dedicated-run path where REVIEWER A actually executes.

## Tasks / Subtasks

- [ ] **Task 1 — Make `qa-reviewer.md` harness-driven and method-polymorphic (AC1, AC2, AC3, AC4, AC6).** `[agent-definition]`
  - [ ] Add a "Load the routing key from the frozen contract" step: read the contract Part-A
        header `verification_method` and `harness_profile`; treat these (not the diff) as the
        routing key for how verification proceeds.
  - [ ] Add a "Resolve driver + environment" step that reads `momentum/verification-harness.json`
        (`defaults.driver_bindings`, `defaults.env.startup`, `defaults.env.readiness_probe`, and any
        `project` override) — mirroring `e2e-validator.md` Environment Setup.
  - [ ] Generalize the current "Execute the Test Suite" step to "Execute the routed verification
        method": a per-method routing block covering `skill-invoke`, `behavioral-trigger`, `bash`,
        `curl`, `smoke` (build + launch + drive), and `document-review` (the only inspect-only method).
  - [ ] For the `smoke` method, drive scenarios only against a freshly (re)launched instance — kill
        and relaunch, or reinstall, the app on a clean state before driving; never a still-running or
        cached build — so a stale cached build cannot masquerade as fresh (the exact nornspun failure
        shape). Borrow the concrete kill+relaunch / reinstall steps from `agent-state-verification-hook`.
  - [ ] State BLOCKED explicitly for harness-absent and startup/readiness-probe-failure after a
        good-faith startup attempt; name the missing prerequisite. Retain the existing MISSING-vs-BLOCKED
        distinction and "reading source is never a substitute for execution."
  - [ ] Preserve the existing single-story scope, seam-story handling, stakes-class assignment,
        read-only constraint, and producer-format output shape unchanged.

- [ ] **Task 2 — Conductor stage-2 REVIEWER A spawn instructs execute-the-routed-method (AC1, AC6 conductor side).** `[skill-instruction]`
  - [ ] In the stage-2 dedicated-run REVIEWER A dispatch, pass the frozen-contract path (already
        passed) AND instruct the agent to route on and execute the contract's
        `verification_method` / `harness_profile` — not to inspect the supplied `story_diff` as its
        verification basis (the diff scopes evidence, it is not the verdict source).

- [ ] **Task 3 — Add the silent-downgrade guard to stage-2 REVIEWER A RETURN VALIDATION; preserve normalization + deferral (AC5, AC7).** `[skill-instruction]`
  - [ ] Extend REVIEWER A RETURN VALIDATION so a report that marks an executable-method AC
        VERIFIED without execution evidence is rejected as a silent downgrade; re-run the leg once;
        escalate on a second downgrade while the environment is available.
  - [ ] Assert BLOCKED (prerequisite named) is exempt from the guard and continues to normalize to
        `severity: critical`; confirm the covered-by-composition branch (REVIEWER A un-dispatched) and
        the REVIEWER A → canonical schema normalization action are unchanged by the guard.

- [ ] **Task 4 — Behavioral evals for the QA leg (AC2, AC4, AC5).** `[agent-definition + skill-instruction]`
  - [ ] Add an eval: `qa-reviewer` invoked against a `smoke`-story fixture with a supporting
        environment produces verdicts backed by build/launch/drive evidence (not diff lines).
  - [ ] Add an eval: `qa-reviewer` against a `smoke` fixture with the environment unavailable returns
        BLOCKED naming the prerequisite — never VERIFIED-by-diff.
  - [ ] Add an eval: the conductor stage-2 guard rejects a diff-only VERIFIED report for an
        executable-method story and re-runs / escalates rather than advancing to merge.

## Dev Notes

### Decision Authority

`skills/momentum/references/rules/verification-standard.md` is the normative source and MUST NOT
be re-authored by this story. It already defines the change_type → method routing table
(§1: `app-ui` → `smoke`; `smoke` = "automated build + launch + drive"), the method-override rule
(§2: substitution requires a contract-frozen *written* justification authored by the story creator,
never the validator), and the harness-profile requirement (§3). This story is **enforcement wiring**
in conductor stage-2 + `qa-reviewer.md`: the silent-downgrade guard is defined as a violation of
verification-standard §1–§3, not as new policy.

### Current State of Affected Files

- **`skills/momentum/agents/qa-reviewer.md`** — Read-only per-story verifier. Today its Review
  Process is test-suite-centric: step 3 "Start Required Services", step 4 "Execute the Test Suite",
  step 5 "Classify Each AC". It has strong BLOCKED semantics (MISSING = tests ran, behavior absent;
  BLOCKED = execution prevented) and "reading source is never a substitute for executing tests," but
  it does **not** read the contract Part-A header (`verification_method` / `harness_profile`) and does
  **not** read `momentum/verification-harness.json` — so for a `smoke` story with no unit-test suite,
  nothing steers it to build + launch + drive. This is the routing-AND-execution gap (see Triage Notes,
  premise correction).
- **`skills/momentum/skills/conductor/workflow.md`** — Stage-2 (`STAGE-2: CODE REVIEW + CONDITIONAL
  QA FAN-OUT`, ~line 632). On the dedicated-run path it spawns REVIEWER A (`qa-reviewer`) with
  `story_slug`, `worktree_path`, `verification_contract` (path), and `story_diff`. REVIEWER A RETURN
  VALIDATION (~line 687) currently checks only that the report is *parseable* — it does not inspect
  whether an executable-method VERIFIED verdict actually carries execution evidence. The NORMALIZE
  REVIEWER A action (~line 697) and the covered-by-composition branch (~line 778) are the sequencing
  dependencies that must not regress (both landed in sprint-2026-06-10).

### Architecture Compliance

- **Reuse, don't duplicate:** `e2e-validator.md` (Team Review) is the direct template for the
  harness-driven, method-polymorphic executor — its Environment Setup, Verification Routing table, and
  BLOCKED-on-absent-harness / BLOCKED-on-startup-failure rules transfer to the build-phase QA leg.
  Author the guard language once; `e2e-validator-black-box-hardening` (backlog) is the same defect class
  in Team Review and should share it.
- **Method tokens are a closed enum** (`skill-invoke | behavioral-trigger | bash | curl | smoke |
  document-review`) equal to the `driver_bindings` keys in `momentum/verification-harness.json`. Use
  these exact tokens; never free-text.
- **Guard boundary:** the silent-downgrade guard fires only on the dedicated-run path where REVIEWER A
  executes; the covered-by-composition path (REVIEWER A deferred to a named integration scenario) is
  untouched.

### Testing Requirements

Verification method for this story (advisory): **`skill-invoke`** — both change types route to it (see
Momentum Implementation Guide). Verify by invoking the QA leg against fixtures and observing behavior,
NOT by reading the edited instructions:
- A `smoke`-story fixture with a supporting environment → verdicts backed by build/launch/drive evidence.
- A `smoke`-story fixture with the environment unavailable → BLOCKED with the prerequisite named.
- A crafted diff-only VERIFIED report for an executable-method story → conductor stage-2 guard rejects it
  and re-runs/escalates.
- Regression: covered-by-composition path still defers REVIEWER A; BLOCKED still normalizes to
  `severity: critical`.

### Project Context Reference

This is enforcement wiring inside the `momentum-conductor-core` epic — the epic's own value analysis
names "verification integrity at the QA/E2E stages (stakes-class validation, verification-method
execution)" among the items that decide whether the practice can trust an autonomous build end-to-end.

### Frozen Contract Note (dev self-check)

A frozen verification contract exists for this sprint at
`.momentum/sprints/{sprint-slug}/specs/conduct-qa-execute-verification-method.*`. Before signaling done,
read only the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as your
self-check. Do NOT read the verifier body (Part B: scenarios, assertion scripts, Gherkin) beyond
sections `how_dev_self_checks` explicitly references — that body is for the verifier agent, not the dev.

### References

- Origin: nornspun sprint-2026-05-30 root-cause analysis (build ledger
  `phase4_live.wiring_6_conclusive`; held finding #6) — campaign-init conversation
  client-faked, undetected by diff-only per-story QA.
- ASR-004 (nornspun assessment document): fixture-drift / scenario-pass-count failure class the story
  specs cited and the engine did not act on.
- Normative rule: `skills/momentum/references/rules/verification-standard.md` (§1 routing table, §2
  method override, §3 harness-profile requirement).
- Reuse template: `skills/momentum/agents/e2e-validator.md` (harness-driven, method-polymorphic executor;
  BLOCKED-on-absent-harness / BLOCKED-on-startup-failure).
- Edit sites: `skills/momentum/agents/qa-reviewer.md`; `skills/momentum/skills/conductor/workflow.md`
  stage-2 (`STAGE-2: CODE REVIEW + CONDITIONAL QA FAN-OUT`, REVIEWER A dispatch + RETURN VALIDATION +
  NORMALIZE REVIEWER A).
- Epic context: `momentum-conductor-core` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → `agent-definition` (verified via `skill-invoke` — invoke the agent, observe behavior)
- Tasks 2, 3 → `skill-instruction` (EDD)
- Task 4 → `agent-definition` + `skill-instruction` (writes the behavioral evals for Tasks 1–3)

---

### agent-definition + skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for `qa-reviewer.md` or `conductor/workflow.md`.** Both are non-deterministic LLM
instruction/agent-definition files — unit tests do not apply. Use EDD, and verify behaviorally by
invoking the leg (the `skill-invoke` method for both `agent-definition` and `skill-instruction`):

**Before writing the changes:**
1. Write 2–3 behavioral evals under `skills/momentum/skills/conductor/evals/` (the conductor's existing
   eval home — it already holds `eval-qa-normalization-*` files), one `.md` per eval, named descriptively
   (e.g., `eval-qa-reviewer-executes-smoke-not-diff.md`,
   `eval-qa-reviewer-blocked-when-environment-absent.md`,
   `eval-stage2-guard-rejects-diff-only-pass.md`). Format each as: "Given [smoke-story fixture + env
   state], the QA leg should [observable behavior — build/launch/drive, or BLOCKED with prerequisite, or
   guard-rejects-and-reruns]." Test behavior and decisions, not exact output text.

**Then implement:**
2. Edit `qa-reviewer.md` (Task 1) and `conductor/workflow.md` stage-2 (Tasks 2–3), anchoring against the
   **post-sprint-2026-06-10 text** — do not regress the NORMALIZE REVIEWER A action or the
   covered-by-composition branch.

**Then verify:**
3. Run evals: for each eval, spawn a subagent (Agent tool) with the eval scenario as its task and the
   edited `qa-reviewer.md` / stage-2 instructions as context; observe whether behavior matches. Invoke the
   `qa-reviewer` against the fixture rather than reading its file for the expected words.
4. All evals match → task complete. Any eval fails → diagnose the instruction gap, revise, re-run
   (max 3 cycles; surface if still failing).

**NFR compliance (skill-instruction / agent-definition):**
- `qa-reviewer.md` and `e2e-validator.md`-style routing tables keep the closed method-token enum.
- Agent/skill frontmatter (`model:`, `effort:`) stays present and correct; do not alter `qa-reviewer`'s
  `tools:` set unless a new capability is genuinely required.
- Keep `qa-reviewer.md` focused; if the method-routing block would push it long, factor shared routing
  into a reference rather than inflating the agent body.

**Additional DoD items (added to standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written under `skills/momentum/skills/conductor/evals/`.
- [ ] EDD cycle ran — smoke-executes, BLOCKED-on-absent-env, and guard-rejects-diff-only behaviors all
      confirmed (or failures documented).
- [ ] `qa-reviewer.md` retains single-story scope, read-only constraint, seam-story handling, and
      stakes-class rubric; only the routing/execution behavior changed.
- [ ] Conductor NORMALIZE REVIEWER A action and covered-by-composition branch confirmed unchanged
      (regression check).
- [ ] AVFL checkpoint on produced artifacts documented (momentum:dev runs this automatically).

## Dev Agent Record

_This section is populated by the dev agent after create-story enrichment._

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List

## Triage Notes — dedup sweep 2026-06-11

Full-backlog dedup sweep (multi-agent, adversarially verified): **no duplicate — genuinely
new work.** Binding constraints for create-story enrichment:

- **Premise correction:** the draft AC claims qa-reviewer "already reads
  verification-harness routing." Not corroborated — `skills/momentum/agents/qa-reviewer.md`
  and `conductor/workflow.md` have zero hits for `verification_method`/`harness_profile`.
  Harness-routed execution exists only in `agents/e2e-validator.md` (Team Review) and the
  rule layer. Rewrite that AC: the gap is routing AND execution in the build-phase QA leg.
- **Normative source exists — don't re-author the rule:**
  `skills/momentum/references/rules/verification-standard.md` already defines smoke =
  build + launch + drive and prohibits method substitution without contract-frozen written
  justification (shipped by `enforced-verification-rule-change-type-method-routing-harness-profile-requirement-adversarial-guard`,
  done). This story is enforcement wiring in conductor stage-2 + qa-reviewer.md; cite the
  rule as normative, define the silent-downgrade guard as a violation of it.
- **Reuse anchors:** `agents/e2e-validator.md` (harness-driven method-polymorphic executor;
  BLOCKED-on-absent-harness, BLOCKED-on-environment-startup-failure) is the direct
  template. qa-reviewer.md:55 already mandates execute-don't-read with BLOCKED semantics
  (lines 59, 109) — extend, don't duplicate. Dev side already reads the contract Part-A
  header (`dev-read-contract-part-a-header`, done) — precedent for the QA side.
  `momentum/verification-harness.json` exists at the repo root.
- **Sequencing (binding):** enrich AFTER sprint-2026-06-10 merges.
  `conduct-qa-reviewer-normalization-adapter` rewrites the REVIEWER A "Returns:" block and
  `conduct-coverage-deferral-preserve-code-review` edits the same stage-2 routing — anchor
  all edits against post-sprint text and do not regress the normalization action.
- **Cross-references to carry:** `qa-reviewer-rescope-per-story-contract` (done — the
  contract being extended; carry its hard constraints forward),
  `e2e-validator-black-box-hardening` (backlog — same defect class in Team Review; author
  the guard language once and share), `widen-document-review-whole-doc-contradiction-scan`
  (backlog — sibling per-method rigor story; keep one coherent per-method rigor table),
  `verification-method-two-column-smoke-ui-model` and
  `re-emit-frozen-app-ui-contracts-via-producer` (upstream enum/data-quality dependencies —
  note their index entries claim story_file:true but no files exist on disk),
  `e2e-client-side-coverage` (shared ASR-004 lineage), `agent-state-verification-hook`
  (borrow its kill+relaunch/reinstall concrete verification steps).
