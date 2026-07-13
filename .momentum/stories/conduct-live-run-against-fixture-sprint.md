---
title: Run the shipped build-guidelines E2E driver live against a populated nornspun fixture (compose→register→resolve seam)
story_key: conduct-live-run-against-fixture-sprint
status: ready-for-dev
epic_slug: momentum-conductor-core
feature_slug:
story_type: feature
priority: high
change_type:
  - config-structure
  - script-code
  - research-spike
verification_method_advisory: bash
depends_on:
  - momentum-knowledge-base-buildout
  - manifesto-builder-skill-generate-then-curate
  - repair-phantom-story-file-entries-and-backfill-live-fixture-scope
touches:
  - docs/research/
---

# Run the shipped build-guidelines E2E driver live against a populated nornspun fixture (compose→register→resolve seam)

## Story

As a developer,
I want the shipped gen-2 live E2E driver — `skills/momentum/skills/build-guidelines/e2e/live-compose-resolve.sh` — executed for real against a populated `nornspun` fixture (its `momentum/agents.json` project entries, its `.claude/manifests/` manifesto instance, and its composed agent files produced via `momentum:build-guidelines`), with the **observed PASS/FAIL output of that execution captured as the verdict**,
so that the compose → register → resolve pipeline the Conductor depends on is proven live — instead of merged "done" on a structured status field that masked a driver which has never actually passed.

## Description

THE proof story for the "cohort goes live" sprint goal. It discharges the one un-executed acceptance clause — the escalated residual from sprint-2026-06-28: the parent story `live-e2e-compose-register-resolve-gen-2-agent` merged `done` with its headline AC1/AC6 unmet — both recorded driver runs died at the very first check (`fixture agents.json not found` / `manifesto not found`; the fixture was never populated), and the same sprint's stage-1 dev agent emitted a structured `outcome: pass` while its own prose admitted the run was deferred. The result: a green ledger over a red reality.

This story closes that gap by doing the one thing that was never done — **running the shipped driver live against a real, populated fixture and reading the verdict off its actual execution.** The driver already exists and is well-formed (it was authored and committed by the parent story); the missing input was always the fixture state. The three fixture-input dependencies (`momentum-knowledge-base-buildout`, `manifesto-builder-skill-generate-then-curate`, `repair-phantom-story-file-entries-and-backfill-live-fixture-scope`) land the KB, the manifesto producer, and the committed live-fixture scope respectively; this story consumes them.

This story does not invoke `/momentum:conduct` directly — every task exercises the **compose → register → resolve seam** (build-guidelines composition, the `.claude/manifests/` manifesto, and the shipped `live-compose-resolve.sh` driver), which is why it is titled for that seam rather than the conduct command. Why an observed driver PASS is nonetheless the "cohort goes live" proof: the driver's headline assertion runs `momentum-tools agent resolve --touches` against the fixture's `momentum/agents.json` — the **same resolve path the Conductor uses to route a story to a composed specialist**. An observed PASS therefore proves that a composed gen-2 agent is reachable through the exact seam a live `/momentum:conduct` build resolves through, not merely that files were written to disk.

**Verification hard rule (developer-directed, from the 2026-07-06 retro — non-negotiable).** This story's acceptance is the **observed driver output**: a PASS/FAIL verdict read from the driver's actual run against the fixture (its stdout `PASS — all assertions hold.` line together with exit code `0`). A structured status field (e.g. `outcome: pass`), a prior "done" marker, an agent self-report, or the mere existence of the evidence file are explicitly **NOT** acceptable evidence — that exclusion is written into the acceptance criteria below, not left implicit. The driver has never passed; only an observed passing run closes this story.

## Acceptance Criteria

1. **Fixture manifesto + agents.json defaults are staged.** The `nornspun` fixture (`~/projects/nornspun`) carries `.claude/manifests/dev-kotlin-compose.md` — a manifesto with a non-empty, well-formed `## File Ownership` section (the `file_ownership:` list that becomes `patterns[]`) — and a pre-created `momentum/agents.json` containing a `defaults` block whose `dev` key points at the composed agent path `.claude/guidelines/agents/dev-kotlin-compose.md`. Observable: both files exist on disk, `agents.json` parses as JSON, and the manifesto's `## File Ownership` field is present and non-empty.

2. **The composition pipeline is run live and produces the composed agent + registered project entry.** `momentum:build-guidelines` (→ `momentum:agent-builder`) is invoked against the fixture and produces (a) the composed Tier-2 file `~/projects/nornspun/.claude/guidelines/agents/dev-kotlin-compose.md` on disk, and (b) a `project[]` entry in `~/projects/nornspun/momentum/agents.json` for slug `dev-kotlin-compose` whose `patterns[]` equals the manifesto `## File Ownership` field verbatim. Observable: the composed file exists; `agents.json project[]` contains the entry with non-empty `patterns`. (This precondition is asserted, and will fail loudly, inside the driver run of AC3 — it is not accepted on a separate self-report.)

3. **The shipped driver is executed live and the acceptance verdict is its OBSERVED console output.** `skills/momentum/skills/build-guidelines/e2e/live-compose-resolve.sh` is run against the populated fixture (from the Momentum repo root, with `FIXTURE_DIR=~/projects/nornspun COMPOSED_SLUG=dev-kotlin-compose MATCH_PATH` set to a path matching a declared ownership glob and `NONMATCH_PATH` set to a non-matching path). Acceptance requires the driver's **actual stdout** to contain the line `PASS — all assertions hold.` **and** the process to exit with status code `0`. **NOT acceptable as evidence for this AC, individually or combined:** a structured status field such as `outcome: pass`; a prior story `status: done` or index `done`; an agent's prose/self-report claiming the run passed; or the presence of the evidence `.md` file without the captured console PASS line + exit `0`. If any of those is the only evidence offered, this AC is UNMET.

4. **Each named assertion passes in the observed run, read from the driver's stdout.** The captured console output shows a `PASS:` line for every one of the driver's four named assertions — AC5-guard (`agents.json` project entry exists with `patterns` == manifesto File Ownership verbatim), AC2 (`resolve --touches <MATCH_PATH>` → `dev-kotlin-compose`, not the generic `dev` fallback), AC4 (composed file contains both the base-body marker and the `## Diagnostic Table` section), and the AC5 negative control (`resolve --touches <NONMATCH_PATH>` → `dev`). Each verdict is read from the driver's printed `PASS:`/`FAIL:` line — never from a structured field or summary table asserted independently of the run.

5. **The observed run output is captured as the story's evidence.** The evidence is the driver-written artifact `docs/research/live-e2e-compose-resolve-evidence.md` (regenerable by re-running the driver) **plus** the captured console transcript of the run showing the terminal `PASS — all assertions hold.` line and the observed exit code `0` (e.g. the command followed by `echo "exit=$?"`). The evidence explicitly records the resolved composed slug, the registered `patterns`, and the composed-file content checks. If the driver instead exits non-zero, the captured `FAIL:` line and the named failing assertion is the recorded verdict, and the story is **not** closeable until a subsequent run produces an observed PASS.

6. **The historical failure mode is gated against, not merely noted.** The story cannot be marked complete on the strength of structured status, a prior `done`, an agent self-report, **or an automated harness result of `skip`/BLOCKED** — closure requires the AC3/AC5 observed-PASS artifacts. This AC exists so that a reviewer checking the story can reject a "done" that lacks the observed console PASS + exit `0`, exactly as the 2026-06-28 close should have been rejected. Explicit harness-skip guard: this repo's `momentum/verification-harness.json` resolves `defaults.execution_surfaces.script-code` to `"skip"` (every surface is `skip`; the sole `project[]` entry is the `example-product-app` template), so an e2e-validator that routed this story through the harness-lookup path would silently SKIP the driver run and report a hollow pass — the exact bypass this story exists to prevent. A `skip`/BLOCKED result is therefore a verification FAILURE for this story, never a pass.

## Tasks / Subtasks

- [ ] **Task 1 — Stage the fixture inputs (manifesto + agents.json defaults).** (AC1)
  Produce `~/projects/nornspun/.claude/manifests/dev-kotlin-compose.md` with a populated `## File Ownership` section. Prefer the real producer now available via the dependency — invoke `momentum:manifesto-builder` (generate-then-curate) so the manifesto is a genuine cohort artifact — using `skills/momentum/skills/build-guidelines/e2e/README.md` § Fixture Setup A as the exact-shape reference (role `dev`, domain `kotlin-compose`, `file_ownership: ["composeApp/**","shared/**"]`, the `## Diagnostic Table` and `## Project Stack` sections). If the producer is unavailable at run time, stage the manifesto verbatim from that README as the fallback. Then pre-create `~/projects/nornspun/momentum/agents.json` with a `defaults` block per README § Fixture Setup B (`defaults.dev` → `.claude/guidelines/agents/dev-kotlin-compose.md`, `project: []`). Verify by inspection: `agents.json` parses; the manifesto File Ownership list is present and non-empty. Keep the manifesto sprint-invariant (DEC-038 D1) — role×domain data only, no sprint/story identifier.

- [ ] **Task 2 — Run the composition pipeline live against the fixture.** (AC2)
  From the fixture (`~/projects/nornspun`), invoke `momentum:build-guidelines` (which loops the manifesto and delegates to `momentum:agent-builder`). It composes `.claude/guidelines/agents/dev-kotlin-compose.md` = `base_body + constitution_excerpt + manifesto` and writes the `project[]` entry into `momentum/agents.json` with `patterns` = the manifesto `## File Ownership` field verbatim (build-guidelines reads the field, never infers). Do NOT hand-write the composed file or the `project[]` entry — the pipeline must produce them (orchestrator purity: this story exercises the pipeline, it does not reimplement it). Confirm the DEC-038 G1 gate observable: at least one composed agent file exists AND is registered with non-empty `patterns[]`.

- [ ] **Task 3 — Execute the shipped driver live and capture the observed verdict.** (AC3, AC4, AC5)
  From the Momentum repo root, run:
  ```bash
  cd ~/projects/momentum
  FIXTURE_DIR=~/projects/nornspun \
  COMPOSED_SLUG=dev-kotlin-compose \
  MATCH_PATH="composeApp/src/commonMain/kotlin/App.kt" \
  NONMATCH_PATH="README.md" \
  bash skills/momentum/skills/build-guidelines/e2e/live-compose-resolve.sh; echo "exit=$?"
  ```
  Capture the full stdout. Acceptance is the observed `PASS — all assertions hold.` line together with `exit=0`. `MATCH_PATH` must match a declared ownership glob (`composeApp/**` matches `composeApp/src/commonMain/kotlin/App.kt`) and `NONMATCH_PATH` must match none (`README.md`); if the manifesto's File Ownership differs from the default globs, set these env vars to match the actual field (see e2e/README § Troubleshooting: "resolve returned 'dev' on matching path"). If the driver exits non-zero, record the named failing assertion, remediate the fixture (Task 1/2), and re-run — do not record a pass until one is observed.

- [ ] **Task 4 — Commit the running-app proof.** (AC5, AC6)
  Commit the driver-generated evidence artifact `docs/research/live-e2e-compose-resolve-evidence.md` (it overwrites the current partial-FAIL artifact on a passing run) and record, alongside it, the captured console transcript showing the terminal PASS line and observed exit `0`. The recorded verdict for the story is this observed output — not a structured field. Confirm the artifact records the resolved slug, the registered `patterns`, and the composed-file checks (AC5), and that closure is gated on the observed PASS (AC6).

## Dev Notes

### Decision Authority

- **Observed-output verification rule (developer-directed, 2026-07-06 retro) — the governing constraint of this story.** Acceptance is the driver's actual execution output (stdout `PASS — all assertions hold.` + exit `0`), never a structured status field, a prior `done`, or an agent self-report. This is not a preference — it is the direct correction of the two named 2026-06-28 defects (see References → ledger entries) and is written into AC3/AC4/AC6 as an explicit exclusion. A dev agent that emits `outcome: pass` without the captured console PASS has NOT satisfied this story.
- **DEC-038 G1 gate** (build-guidelines `workflow.md:12` `<critical>`): a composition run is valid only if at least one composed agent file is written to disk AND registered in `momentum/agents.json` with non-empty `patterns[]` AND `momentum-tools agent resolve --touches` returns the composed slug (not the generic `dev` fallback). This story is the **live proof** of that gate; it neither relaxes nor redefines it.
- **Orchestrator purity (preserved):** the story *exercises* the existing pipeline (`momentum:build-guidelines` / `momentum:agent-builder` / `momentum-tools agent resolve`) and the shipped driver. It must NOT reimplement composition, hand-author the composed file, or self-write the `project[]` entry — it stages fixture inputs, runs the real pipeline, and reads the driver's real output.
- **Sprint invariance (DEC-038 D1):** the fixture manifesto and composed output carry no sprint/story identifier — standing role×domain data only.

### Current State of Affected Files

- **Shipped driver — `skills/momentum/skills/build-guidelines/e2e/live-compose-resolve.sh`** (committed 2026-07-06 by the parent story; NOT modified here). Deterministic assertion phase. Env defaults: `FIXTURE_DIR=~/projects/nornspun`, `COMPOSED_SLUG=dev-kotlin-compose`, `MATCH_PATH=composeApp/src/commonMain/kotlin/App.kt`, `NONMATCH_PATH=README.md`, `EVIDENCE_OUT_DIR=docs/research`. Reads `## File Ownership` verbatim from `${FIXTURE_DIR}/.claude/manifests/${COMPOSED_SLUG}.md`; asserts the `project[]` entry + verbatim `patterns` (AC5-guard) FIRST so a mis-targeted resolver fails loudly, then AC2 resolve, AC4 composed-file content, AC5 negative control; writes `docs/research/live-e2e-compose-resolve-evidence.md`; exits `0` on all-pass (prints `PASS — all assertions hold.`), `1` naming the first failed assertion otherwise.
- **`~/projects/nornspun` fixture (current state — the exact gap this story closes):** HAS `.claude/guidelines/constitution.md` (Tier 1) and `docs/guidelines/` KB (compose-ui, gradle-agp, kmp-testing, kotlin-kmp, ktor-sse + index). MISSING `.claude/manifests/` (no dir), `momentum/agents.json` (absent), and `.claude/guidelines/agents/` (no composed agents). This is precisely the state at which both prior runs died — see `docs/research/live-e2e-compose-resolve-evidence.md`, which currently records `FAIL: fixture agents.json not found` and `FAIL: manifesto not found`.
- **`docs/research/live-e2e-compose-resolve-evidence.md`** (in the Momentum repo) — the driver's fixed-filename artifact; currently holds a partial FAIL record from 2026-07-06. A passing run overwrites it with the full PASS artifact. This is the file committed as AC5/AC6 evidence.
- **`skills/momentum/scripts/momentum-tools.py` `cmd_agent_resolve`** (NOT modified) — `fnmatch`-matches touched paths against `momentum/agents.json project[]` (first-match-wins), falls back to `defaults["dev"]`. Loads `resolve_project_dir()/momentum/agents.json`, so the driver targets the fixture by setting `CLAUDE_PROJECT_DIR=$FIXTURE_DIR`. This is the same resolve seam a live `/momentum:conduct` build uses to route a story to a composed specialist.
- **`momentum:build-guidelines` / `momentum:agent-builder`** (NOT modified) — the composition orchestrator + Tier-2 composer the story runs live in Task 2.

### Architecture Compliance

- **Anti-insider-knowledge guard (verification-standard §4):** every assertion is ordinary-user-observable — the driver's stdout `PASS:`/`FAIL:` lines, the `momentum-tools agent resolve` JSON, the contents of `agents.json`, and the presence of `## Diagnostic Table` / base-body text in the composed file. No acceptance depends on implementation internals an ordinary operator could not observe.
- **Deterministic over inferred:** the AC5-guard asserts exact list-equality of `patterns` to the manifesto File Ownership field — this is the deterministic path enabled by the `manifesto-format-normative-file-pattern-ownership-field` work; the story must exercise it (patterns == field verbatim), not the legacy prose-inference path.
- **Harness profile + skip-bypass guard (verification-standard §2/§3) — decision-relevant:** the `script-code`/`bash` surface is nominally governed by `momentum/verification-harness.json`, but this repo's `defaults.execution_surfaces.script-code` currently resolves to `"skip"` (all ten surfaces are `"skip"`; the only `project[]` entry is the `example-product-app` template, not a momentum/nornspun profile). **Consequence:** an automated e2e-validator that routed this story through the harness-lookup path would resolve `skip` and silently report a pass without ever running the driver — the precise silent-bypass this story exists to eliminate. **Override (authored by the story creator per verification-standard §2, not the validator):** for this story the default harness routing is insufficient; verification is satisfied ONLY by the literal observed driver run per AC3 (stdout `PASS — all assertions hold.` + exit `0`). A harness `skip`/BLOCKED is a verification FAILURE here, not a pass. The fixture readiness probe is the populated fixture (`~/projects/nornspun/momentum/agents.json` + the composed agent file); a run against an un-populated fixture is the historical failure and must be reported as FAIL, not BLOCKED-masked-as-pass. (Standing up a real active `project[]`/harness-profile entry for the `script-code` surface is contract-freeze work at sprint-planning — see the parent story's Testing Requirements — and is a precondition to any harness-routed run; it is not a deliverable of this proof story, which runs the driver directly.)

### Testing Requirements

- **Verification method: `bash` (headline).** This story's primary deliverable is the live, executable driver run whose PASS/FAIL is observed by **running it** — which is precisely the observed-output rule the story enforces. Per `skills/momentum/references/rules/verification-standard.md` §1, per-task routing is: Tasks 1 (`config-structure`) and 4 (`research-spike`) → `document-review`; Tasks 2–3 (the composition + driver execution, `script-code`) → `bash`. The single `verification_method_advisory` frontmatter value is the story's **headline** method — `bash` — because the decisive, story-defining evidence is the driver's observed console verdict. This written rationale, authored by the story creator (not the validator), satisfies verification-standard §2.
- **Why `bash` and not `document-review` as the headline:** making `document-review` the sole method would reproduce the exact "inspect a status/trace instead of running it" weakness this story exists to eliminate — so `document-review` is applied only to the fixture-staging (Task 1) and the evidence artifact (Task 4), never to the driver run. The verdict for Tasks 2–3 must come from `bash` (observed execution), never from inspection of a structured field.
- **Harness-skip override (verification-standard §2):** do NOT accept a harness-routed `skip`/BLOCKED as a pass. This repo's harness resolves `script-code → "skip"` (see Architecture Compliance), so verification is satisfied only by the literal observed driver run per AC3 — a `skip` is a FAILURE for this story. This override is authored here by the story creator, not the validator.
- **EDD vs TDD:** N/A for authoring — the driver is already shipped and is not modified. The one non-deterministic beat is the `build-guidelines`/`agent-builder` LLM invocation in Task 2; the story does not test the skill's internals — it asserts on the skill's observable outputs (composed file + `agents.json` + resolve result) via the shipped driver, which is the correct seam.

### Project Context Reference

This is the last un-executed acceptance clause of the agent-composition/conductor line: the driver was built but never run against a real fixture, and the story that owned it shipped `done` on a structured status that masked the gap. Executing it live — and reading the verdict off the run, not off a field — is what turns "the cohort exists on disk" into "the cohort is reachable through the Conductor's resolve seam." Closing it discharges the sprint-2026-06-28 escalated residual and the two retro ledger findings it spawned.

### References

- Shipped driver executed live: `skills/momentum/skills/build-guidelines/e2e/live-compose-resolve.sh` (deterministic assertion phase; the artifact this story runs).
- Driver run procedure + fixture setup: `skills/momentum/skills/build-guidelines/e2e/README.md` (two-phase E2E; § Fixture Setup A/B for the manifesto + agents.json defaults; § Troubleshooting; § AC-to-driver mapping).
- Parent story (authored the driver; its AC1/AC6 residual is what this discharges): `.momentum/stories/live-e2e-compose-register-resolve-gen-2-agent.md`.
- Composition orchestrator (entry point): `skills/momentum/skills/build-guidelines/SKILL.md`. DEC-038 G1 gate — the `<critical>`-tagged compound definition quoted in Decision Authority (composed file written AND registered with non-empty `patterns[]` AND resolvable via `--touches`): `skills/momentum/skills/build-guidelines/workflow.md:12`.
- Resolver (the Conductor's resolve seam the driver asserts against): `skills/momentum/scripts/momentum-tools.py` — `cmd_agent_resolve` (`--touches` fnmatch + `dev` fallback; `CLAUDE_PROJECT_DIR`-scoped `agents.json`).
- Manifesto format (File Ownership field = deterministic source of `patterns`): `skills/momentum/references/manifesto-format.md`.
- Verification standard: `skills/momentum/references/rules/verification-standard.md` §1 (change-type → method routing), §2 (override justification), §3 (harness profile), §4 (anti-insider-knowledge).
- DEC-038 (manifesto = diagnostic table; G1 reachability gate): `_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md`.
- Prior-run evidence (currently a partial FAIL — both runs died at the first check): `docs/research/live-e2e-compose-resolve-evidence.md`.
- Handoff (observed-output caution): `.momentum/handoffs/next-sprint-cohort-review-2026-07-06.md` §4 Wave 2.
- Ledger — the two 2026-06-28 defects this story corrects: `retro-sprint-2026-06-28-live-e2e-compose-ac1-ac6-unmet-shipped-done`; `retro-sprint-2026-06-28-dev-agent-structured-status-vs-prose-admission-gap`.
- Fixture-scope dependency (defines the live-fixture scope this story consumes): `.momentum/stories/repair-phantom-story-file-entries-and-backfill-live-fixture-scope.md`.
- Epic context: `momentum-conductor-core` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Task 1 → config-structure (stage fixture manifesto + agents.json defaults; verify by inspection)
- Tasks 2, 3 → script-code (run the composition pipeline + execute the shipped driver; verify by `bash` — observed run)
- Task 4 → research-spike (commit the observed-run evidence artifact; verify by document-review)

Per-task routing (verification-standard §1): Tasks 1, 4 → `document-review`; Tasks 2–3 → `bash`. `bash` is the story's headline `verification_method_advisory` because the decisive evidence is the driver's observed console verdict (see Testing Requirements for the rationale, which satisfies verification-standard §2).

---

### config-structure Task: Direct Implementation (verify by inspection)

Task 1 stages structured fixture data — no tests or evals. Implement directly and verify by inspection:

1. **Write the manifesto and the agents.json defaults block** per e2e/README.md § Fixture Setup A/B (prefer `momentum:manifesto-builder` for the manifesto; stage verbatim as fallback).
2. **Verify by inspection:**
   - JSON: `~/projects/nornspun/momentum/agents.json` must parse without error (validate with `python3 -m json.tool` or `jq` — not visual inspection).
   - Required fields: `defaults.dev` present and pointing at `.claude/guidelines/agents/dev-kotlin-compose.md`; `project` present (initially `[]`).
   - Manifesto: `## File Ownership` section present with a non-empty `file_ownership:` list; the globs chosen must include one that `MATCH_PATH` will match and exclude the `NONMATCH_PATH`.
3. **Document** what was staged in the Dev Agent Record.

**DoD additions for the config-structure task:**
- [ ] `agents.json` parses (validated with a tool); `defaults.dev` present with correct path; `project` present
- [ ] Manifesto `## File Ownership` present and non-empty; globs consistent with the chosen `MATCH_PATH` / `NONMATCH_PATH`
- [ ] Fixture staging documented in Dev Agent Record

### script-code Tasks: Executable verification (run it; read the observed output)

Tasks 2–3 are verified by **running** the composition pipeline and the shipped driver against the real fixture and reading the observed output — the driver is NOT modified by this story.

1. **Run the real pipeline (Task 2), not a reimplementation.** Invoke `momentum:build-guidelines` from the fixture; confirm the composed file exists and the `project[]` entry is registered with non-empty `patterns[]` (DEC-038 G1). Assert on observable outputs only (composed file on disk, `agents.json` contents) — never on pipeline internals.
2. **Execute the shipped driver (Task 3) and capture stdout + exit code.** Use the exact invocation in Task 3. Acceptance = observed `PASS — all assertions hold.` line + `exit=0`. Each of the four named assertions must show a `PASS:` line in the captured stdout.
3. **The observed run is the verdict — never a structured field.** Do not record, emit, or accept `outcome: pass` (or any structured status) in place of the captured console PASS + exit `0`. If the driver exits non-zero, record the named failing assertion, fix the fixture, and re-run; a pass is recorded only when observed.

**DoD additions for the script-code tasks:**
- [ ] Composition run live via `momentum:build-guidelines` (not hand-authored); DEC-038 G1 observable confirmed (composed file + non-empty `patterns[]`)
- [ ] Shipped driver executed with the Task-3 invocation; full stdout + exit code captured
- [ ] Observed stdout contains `PASS — all assertions hold.` AND exit code is `0`; a `PASS:` line present for each of the 4 named assertions
- [ ] No structured status field substituted for the observed console output at any point
- [ ] Driver, `momentum-tools`, and the build-guidelines pipeline unmodified (the story exercises them; it does not change them)

### research-spike Task: Committed running-app proof (document-review of the evidence)

There is no dedicated injection template for `research-spike`; it is validated like a specification — by inspecting the committed evidence and confirming it satisfies its ACs (verification-standard §1: `research-spike → document-review`). For Task 4:

1. **Commit the evidence artifact** `docs/research/live-e2e-compose-resolve-evidence.md` (driver-generated; overwrites the prior partial-FAIL record on a passing run) together with the captured console transcript showing the terminal PASS line + observed exit `0`.
2. **Cross-reference check:** the artifact records the resolved composed slug, the registered `patterns`, and the composed-file content checks; all references resolve.
3. **Closure gate:** confirm the story is closeable only on the observed-PASS artifacts (AC6) — not on structured status, a prior `done`, or a self-report.

**DoD additions for the research-spike task:**
- [ ] Evidence artifact committed under `docs/research/`, regenerable by re-running the driver
- [ ] Artifact records the resolved slug, the registered `patterns`, and the composed-file checks
- [ ] Captured console transcript (PASS line + exit `0`) recorded as the story's verdict alongside the artifact

**Frozen verification contract:** a frozen contract exists per sprint at `sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Dev reads only the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signalling done. Dev never reads the verifier body (Part B: scenarios, assertion scripts) beyond sections `how_dev_self_checks` explicitly references.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
