---
title: "Live E2E: compose + register + resolve a Gen-2 agent against a real manifest + KB"
story_key: live-e2e-compose-register-resolve-gen-2-agent
status: ready-for-dev
epic_slug: momentum-agent-composition-pipeline
feature_slug:
story_type: exploration
priority: medium
change_type:
  - script-code
  - research-spike
verification_method_advisory: bash
depends_on:
  - manifesto-format-normative-file-pattern-ownership-field
touches:
  - skills/momentum/skills/build-guidelines/e2e/
  - docs/research/
---

# Live E2E: compose + register + resolve a Gen-2 agent against a real manifest + KB

## Story

As a developer,
I want a live, executable E2E that runs the full agent-composition pipeline against a real fixture project,
so that I have running-app proof — not just an instruction trace — that build-guidelines composes, registers (with non-empty `patterns`), and resolves a specialist agent end-to-end against a real manifesto + KB.

## Description

The E2E for sprint-2026-06-18 was an integration-TRACE (walking the build-guidelines skill instructions by hand), not live execution — so there is no running-app proof that build-guidelines actually composes a Tier-2 file, registers it in `momentum/agents.json` with non-empty `patterns[]`, and resolves a specialist agent end-to-end against a real project manifesto + KB.

This story builds a live, executable E2E that runs the agent-composition pipeline against a real fixture (the `nornspun` project — it already carries a real `.claude/guidelines/constitution.md` and a `docs/guidelines/` KB) and asserts the decisive, ordinary-user-observable outcomes: `momentum-tools agent resolve --touches` returns the composed `{role}-{domain}` slug (not the generic `dev` fallback), the registered `agents.json` project entry has non-empty `patterns`, and the composed agent file contains the manifesto diagnostic table plus the base body.

It is sequenced AFTER `manifesto-format-normative-file-pattern-ownership-field` lands, so it exercises the **deterministic** resolution path — `patterns` read verbatim from the manifesto's normative File Ownership field — rather than the legacy best-effort LLM inference from `## Project Stack` prose.

**Pain context:** Surfaced at the sprint-2026-06-18 conduct end-gate as a "still hollow" gap. It is the integration proof that the agent cohort works in practice, and the natural validation once the manifesto File Ownership field makes resolution deterministic. Priority: MEDIUM. This is a real backlog item, NOT a quick-fix.

## Acceptance Criteria

1. **A live E2E runs the real pipeline, then a committed executable assertion driver proves the outcome.** The E2E has two phases against the real `nornspun` fixture (a real manifesto with a populated File Ownership field plus the existing real KB), and is NOT a hand-walked instruction trace:
   - **Composition phase (real pipeline).** The agent-composition pipeline (`momentum:build-guidelines` → `momentum:agent-builder`) is actually run. These are LLM skill invocations with no headless CLI, so this beat is performed by invoking the real skill — an agent/developer step in the E2E procedure; it MAY be driven headlessly (e.g. `claude -p`), with the noted caveat that doing so also exercises Claude, not only the pipeline. It writes the composed `.claude/guidelines/agents/{role}-{domain}.md` and the fixture's `momentum/agents.json` project entry.
   - **Assertion phase (executable driver).** A committed, executable driver (e.g. `skills/momentum/skills/build-guidelines/e2e/live-compose-resolve.sh` or `.py`) — the deterministic part — runs the AC2–AC5 checks against those real outputs. From the composed fixture state it runs to completion, exits `0` when every assertion holds, and exits non-zero (naming the failed assertion) otherwise.
   Running-app proof = the real pipeline ran AND the driver asserted on its real outputs — not a trace.

2. **Deterministic resolution returns the composed slug, not the `dev` fallback (headline proof).** After composition, the driver runs `momentum-tools agent resolve --touches <path matching a declared ownership glob>` **against the fixture's `agents.json`** — it targets the fixture by setting `CLAUDE_PROJECT_DIR` to the `nornspun` fixture root (or running from the fixture cwd), since the resolver loads `resolve_project_dir()/momentum/agents.json`. It asserts the returned `results[0].slug` equals the composed `{role}-{domain}` slug (e.g. `dev-kotlin-compose`) and is NOT `dev`. The match is driven by the manifesto's declared File Ownership field, not by LLM inference.

3. **The registered project entry has non-empty `patterns` equal to the manifesto field verbatim.** The driver asserts the fixture's `momentum/agents.json` gained a `project[]` entry for the composed slug whose `patterns[]` is non-empty and equals the manifesto File Ownership field verbatim — no added, dropped, or reworded globs. This is the G1 reachability contract (DEC-038), observed live.

4. **The composed agent file contains the diagnostic table + base body.** The driver asserts the composed Tier-2 file `.claude/guidelines/agents/{role}-{domain}.md` exists on disk and contains BOTH (a) the base-body content and (b) the `## Diagnostic Table` section from the manifesto — per the composition formula `base_body + constitution_excerpt + manifesto`. Observable by grepping the composed file for the diagnostic-table heading and a base-body marker.

5. **Negative control + wrong-file guard.** Before the negative control, the driver asserts the composed `project[]` entry actually exists in the fixture's `agents.json` — so a mis-targeted resolver (reading the wrong repo's `agents.json`) fails loudly here, rather than AC2 silently falling back to `dev` while this control falsely passes. It then asserts `momentum-tools agent resolve --touches <path NOT matching any declared glob>` returns the generic `dev` fallback — proving the AC2 match is a genuine pattern match, not a vacuous always-match entry.

6. **Committed running-app proof supersedes the integration-TRACE.** The E2E run produces a committed evidence artifact under `docs/research/` (the captured resolve output + the pass/fail of each assertion in AC2–AC5) that constitutes running-app proof, explicitly superseding the sprint-2026-06-18 integration-TRACE. The artifact is regenerable by re-running the driver.

7. **Exercises the deterministic path enabled by the dependency story.** The E2E exercises the deterministic resolution path that `manifesto-format-normative-file-pattern-ownership-field` enables (patterns sourced verbatim from the manifesto File Ownership field). The story declares that dependency and asserts the deterministic-path behavior (`patterns` == field verbatim, AC3), not the legacy `## Project Stack` LLM-inference behavior.

## Tasks / Subtasks

- [ ] **Task 1 — Define the E2E procedure + author the executable assertion driver.** (AC1)
  Create `skills/momentum/skills/build-guidelines/e2e/` with two parts. (a) The **E2E procedure** (a runner/doc) that stages the real `nornspun` fixture (a real manifesto with a populated File Ownership field, the existing `.claude/guidelines/constitution.md`, the `docs/guidelines/` KB) and **runs the real composition pipeline** (`momentum:build-guidelines` → `momentum:agent-builder`). Because those are LLM skill invocations with no headless CLI, pin how the composition beat is triggered — an agent/developer step, or headless via `claude -p` (noting that then partly exercises Claude). (b) The committed **executable assertion driver** (`.sh`/`.py`) — the deterministic part that runs the AC2–AC5 checks against the composed outputs, targeting the **fixture's** `agents.json` by setting `CLAUDE_PROJECT_DIR` to the fixture root (or running from its cwd). The driver is idempotent from a composed fixture state, names each assertion, and exits non-zero on the first failure.

- [ ] **Task 2 — Implement the deterministic-resolution assertions.** (AC2, AC3, AC4, AC5, AC7)
  In the driver (targeting the fixture's `agents.json`): first assert the composed `project[]` entry exists (wrong-file guard, so a mis-targeted resolver fails loudly). Then implement discrete, re-runnable checks: parse the JSON from `momentum-tools agent resolve --touches <owned path>` for `results[0].slug`, assert it equals the expected composed `{role}-{domain}` slug and `!= dev`; assert `project[].patterns` is non-empty and equals the manifesto File Ownership field verbatim (exact list equality — what makes AC7's deterministic-path claim checkable); grep the composed file for `## Diagnostic Table` and a base-body marker; run the negative-control resolve on a non-owned path and assert the `dev` fallback.

- [ ] **Task 3 — Run the live E2E and commit the running-app proof.** (AC1, AC6)
  Run the driver against the real `nornspun` fixture; capture the actual `agent resolve` output and each assertion result; commit the evidence artifact under `docs/research/` as the running-app proof that supersedes the sprint-2026-06-18 integration-TRACE. Record the exact composed slug resolved, the registered `patterns`, and the composed-file content checks.

## Dev Notes

### Decision Authority

- **DEC-038 G1 gate** (build-guidelines `<critical>`): a run is valid only if at least one composed agent file is written to disk AND registered in `momentum/agents.json` with non-empty `patterns[]` AND `momentum-tools agent resolve --touches` returns the composed slug (not the generic `dev` fallback). This story is the **live proof** of that gate end-to-end — it does not relax or redefine it.
- **Composition formula** (`build-guidelines/references/orchestration-guide.md`): `composed_agent = base_body + constitution_excerpt + manifesto (## Diagnostic Table + ## Project Stack)`. AC4 asserts the diagnostic table + base body are present in the composed file — this is the observable contract, not an implementation detail.
- **Dependency — deterministic patterns:** `manifesto-format-normative-file-pattern-ownership-field` adds the normative File Ownership field that build-guidelines reads verbatim into `permissions_scope` → `agents.json` `patterns`. This story must run AFTER it and assert the deterministic behavior (patterns == declared field). Running before it would only exercise the legacy LLM-inference path and would not prove deterministic resolution. The `orchestration-guide.md` `## Known Limitation: patterns Derivation Is Best-Effort` section is closed by that dependency, not by this story.
- **Orchestrator purity (preserved):** the E2E *exercises* the existing pipeline (build-guidelines / agent-builder / `momentum-tools agent resolve`). It must NOT reimplement composition or self-write `agents.json`; it only stages fixture inputs, runs the real pipeline, and asserts on real outputs.

### Current State of Affected Files

- `momentum-tools agent resolve --touches <paths>` (`skills/momentum/scripts/momentum-tools.py`, `cmd_agent_resolve`) — `fnmatch`-matches each touched path against `momentum/agents.json` `project[]` entries (first-match-wins) and falls back to `defaults["dev"]` when nothing matches. Emits JSON: `results[].slug`, `agent_path`, `write_permissions`, `file_scope`. This is the resolver the E2E asserts against. (Not modified by this story.)
- `momentum/agents.json` (in the Momentum repo) — `defaults` holds the generic base agents incl. `dev`; `project[]` is currently empty (a bare resolve returns `dev`). The E2E operates against the **fixture's** `agents.json`, which the pipeline populates during the run.
- `nornspun` fixture (`/Users/steve/projects/nornspun`) — already carries `.claude/guidelines/constitution.md` (Tier 1) and a real `docs/guidelines/` KB (kotlin-kmp, ktor-sse, compose-ui, gradle-agp, kmp-testing). It does **not** yet have `momentum/agents.json` — the pipeline run creates/populates it. A real manifesto with a populated File Ownership field is the fixture input the driver must supply.
- `skills/momentum/skills/build-guidelines/` — the skill under test; composes `.claude/guidelines/agents/{role}-{domain}.md` and validates resolvability via `--touches`. The new `e2e/` harness is added under it.
- Exemplar manifesto shape: `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` (a nornspun artifact, format reference only — never a Momentum agent).

### Architecture Compliance

- **Anti-insider-knowledge guard (verification-standard §4):** every assertion is ordinary-user-observable — `momentum-tools agent resolve` JSON output, the contents of `agents.json`, and the presence of `## Diagnostic Table` / base-body text in the composed file. No assertion may depend on implementation internals (private function names, fixture-internal variables) that an ordinary user could not observe.
- **Deterministic over inferred:** AC3/AC7 assert exact list-equality of `patterns` to the manifesto File Ownership field — this is what distinguishes the deterministic path (the dependency) from the legacy inference path and must be an exact-match assertion, not a fuzzy contains.
- **Sprint invariance (DEC-038 D1):** the manifesto and composed output carry no sprint/story identifier; the fixture manifesto used by the E2E must likewise be standing role×domain data.

### Testing Requirements

- **Verification method: `bash` (headline) — per-task routing per §1.** This story has two `change_type` values: `script-code` (the executable E2E driver + assertions — the primary deliverable) and `research-spike` (the committed running-app-proof artifact). Per `skills/momentum/references/rules/verification-standard.md` §1, a multi-type story **applies each type's method to the task(s) of that type** — a deterministic rule, not an ambiguity: **Tasks 1–2 (`script-code`) → `bash`**, **Task 3 (`research-spike`) → `document-review`**. The single `verification_method_advisory` frontmatter value is the story's **headline** method; `bash` is chosen there because the primary deliverable is an *executable* E2E whose pass/fail is observed by **running it** (resolve returns the composed slug; `patterns` non-empty and verbatim; composed file has the diagnostic table + base body; negative-control falls back to `dev`).
  - **Why `bash` as the headline and not another single method:** `smoke` is not applicable (no built app UI / Maestro/Playwright surface — resolution is a CLI + file assertion); `skill-invoke` is only partially apt (the composition beat invokes a skill, but the decisive repeatable assertions are CLI/file observations `bash` captures directly); and `document-review` as the story's *sole* method would reproduce the "inspect a trace instead of running it" weakness this story exists to eliminate — so `document-review` is **applied to Task 3's artifact**, not made the headline. This written rationale satisfies verification-standard §2 (authored by the story creator, not the validator).
- **EDD vs TDD:** the E2E driver is a script — apply standard executable verification (run it, observe assertions). The one non-deterministic beat is the build-guidelines/agent-builder LLM invocation inside the pipeline; the E2E does not test the skill's internals — it asserts on the skill's *observable outputs* (resolve result + composed file + `agents.json`), which is the correct seam.
- **Harness-profile (verification-standard §3):** a harness-profile reference for the `bash` surface must be declared at sprint-planning contract-freeze. Current state of `momentum/verification-harness.json`: the `defaults.driver_bindings` block is already populated (incl. a `bash` binding → `driver: cmux`), so **no new driver-binding is needed**. What is missing is (a) `defaults.execution_surfaces.script-code` is set to `"skip"`, (b) there is no real `project[]` entry (only a `_template` example), and (c) `defaults.env.readiness_probe` is empty. Contract-freeze must therefore add a real `project[]`/harness-profile entry that activates the `script-code`/`bash` surface for this story — with the `nornspun` fixture readiness probe and platform — not a `bash` driver-binding.

### Project Context Reference

This story closes the "still hollow" residual for the agent composition pipeline by replacing the integration-TRACE with live, executable proof. The reachability contract it proves live is build-guidelines' G1 gate; the deterministic behavior it asserts is enabled by the `manifesto-format-normative-file-pattern-ownership-field` dependency.

### References

- `skills/momentum/scripts/momentum-tools.py` — `cmd_agent_resolve` (`--touches` fnmatch + `dev` fallback); the resolver the E2E asserts against.
- `skills/momentum/skills/build-guidelines/SKILL.md` — orchestrator description + DEC-038 G1 gate ("composed file written AND registered AND resolvable").
- `skills/momentum/skills/build-guidelines/references/orchestration-guide.md` — composition formula, composed-path naming `.claude/guidelines/agents/{role}-{domain}.md`, `## Known Limitation: patterns Derivation Is Best-Effort` (closed by the dependency).
- `skills/momentum/references/manifesto-format.md` — manifesto format; the File Ownership field (added by the dependency) is the deterministic source of `patterns`.
- `skills/momentum/references/rules/verification-standard.md` §1 (change-type → method routing), §2 (override justification), §3 (harness profile), §4 (anti-insider-knowledge).
- `momentum/agents.json` (and the fixture's) — resolver target; `project[].patterns` matched by `--touches`.
- `docs/research/manifesto-cmp-dev-exemplar-2026-06-16.md` — manifesto exemplar shape (nornspun artifact, format reference only).
- Dependency: `manifesto-format-normative-file-pattern-ownership-field` — makes `patterns` deterministic; must land first.
- DEC-038 — `_bmad-output/planning-artifacts/decisions/dec-038-manifesto-diagnostic-table-multi-kb-2026-06-16.md` (manifesto = diagnostic table; G1 gate).
- Epic context: `momentum-agent-composition-pipeline` (from _bmad-output/planning-artifacts/epics.json)

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1, 2 → script-code (executable E2E driver + assertions; primary deliverable)
- Task 3 → research-spike (committed running-app-proof evidence artifact)

Per-task routing (verification-standard §1): Tasks 1–2 (`script-code`) → **`bash`**; Task 3 (`research-spike`) → **`document-review`**. `bash` is the story's headline `verification_method_advisory` (primary deliverable is the executable E2E). See Testing Requirements for the rationale.

---

### script-code Tasks: Executable verification (run the driver; observe assertions)

The E2E driver is executable code under `skills/momentum/skills/build-guidelines/e2e/`. It is verified by **running it** against the real `nornspun` fixture and observing every assertion:

1. **Build a clean, idempotent driver.** From a clean fixture state, the driver stages the manifesto + KB inputs, runs the real pipeline, and asserts. It must name each assertion and exit non-zero on the first failure (exit `0` only when all hold).
2. **Assert on observable outputs only** (anti-insider-knowledge, verification-standard §4): the `momentum-tools agent resolve --touches` JSON (`results[0].slug`), `momentum/agents.json` `project[].patterns`, and the composed-file contents (`## Diagnostic Table` heading + a base-body marker). Do not assert on pipeline internals.
3. **Exact-equality for `patterns`** (AC3/AC7): assert `patterns` equals the manifesto File Ownership field verbatim — this is the check that proves the deterministic path, not the legacy inference path.
4. **Negative control** (AC5): a non-owned path must resolve to `dev`, proving the AC2 match is genuine.

**DoD items for the script-code tasks:**
- [ ] Driver is committed, executable, and idempotent from a clean fixture state
- [ ] Each assertion (AC2–AC5) is discrete, named, and re-runnable; the driver exits non-zero on any failure
- [ ] Assertions read only ordinary-user-observable outputs (resolve JSON, `agents.json`, composed-file text)
- [ ] `patterns` assertion is exact list-equality to the manifesto File Ownership field (AC3/AC7)
- [ ] No regression to `momentum-tools` or the build-guidelines pipeline (the E2E exercises them; it does not modify them)

### research-spike Task: Committed running-app proof (document-review of the evidence)

There is no dedicated injection template for `research-spike`; it is validated like a specification — by inspecting the committed evidence artifact and confirming it satisfies its ACs (verification-standard §1: `research-spike → document-review`). For Task 3:

1. **Run the live E2E** against the real `nornspun` fixture and capture the actual `agent resolve` output and each assertion result.
2. **Commit the evidence artifact** under `docs/research/` as the running-app proof, explicitly noting it supersedes the sprint-2026-06-18 integration-TRACE.
3. **Cross-reference check:** the artifact records the exact composed slug resolved, the registered `patterns`, and the composed-file content checks; all references resolve.

**DoD items for the research-spike task:**
- [ ] Evidence artifact committed under `docs/research/`, regenerable by re-running the driver
- [ ] Artifact records the resolved composed slug, the registered `patterns`, and the composed-file checks (AC6)
- [ ] Artifact states it supersedes the sprint-2026-06-18 integration-TRACE

**Frozen verification contract:** a frozen contract exists per sprint at `sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Dev reads only the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check before signalling done. Dev never reads the verifier body (Part B: scenarios, assertion scripts) beyond sections `how_dev_self_checks` explicitly references.

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
