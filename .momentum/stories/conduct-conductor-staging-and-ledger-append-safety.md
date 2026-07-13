---
title: Conductor staging must see new files, and the ledger append must be shell-safe
story_key: conduct-conductor-staging-and-ledger-append-safety
status: ready-for-dev
epic_slug: momentum-conductor-core
feature_slug:
story_type: defect
priority: high
change_type:
  - skill-instruction
verification_method_advisory: skill-invoke
depends_on: []
touches:
  - skills/momentum/skills/conductor/workflow.md
  - skills/momentum/skills/conductor/references/build-ledger.md
---

# Conductor staging must see new files, and the ledger append must be shell-safe

## Story

As the maintainer of the conduct build engine,
I want the Conductor's commit step to stage newly-created files and its ledger append to be safe against arbitrary prose,
so that green-field stories (the common case) cannot silently lose new files at commit, and the build journal cannot be corrupted by an apostrophe or a crash mid-write.

## Why this exists (two stakes-class escalations from sprint-2026-06-10, end-gate D1 + D2)

These were raised by the build's own stakes-class escalation path and held for the developer; both confirmed real and accepted as fix-next.

**D1 (critical, irreversible-destructive) — `git add -u` is blind to untracked files.** Now that dev agents never commit (DEC-035), the Conductor's `git add -u` is the only staging path — but it ignores brand-new files. A green-field story whose deliverable is a new file (a new skill, reference, or test — the most common shape) would have that file silently dropped at commit and destroyed at worktree cleanup. **Empirically hit during sprint-2026-06-10:** the Conductor compensated by staging new eval/reference files by explicit path. There are **six** `git add -u` commit sites, anchored here by their commit-message label (line numbers drift — grep the label): the story commit `feat({slug}): implement …` (~workflow.md:617), the Stage-3 Phase-B per-finding fix commit `fix({slug}): auto-fix {F.summary}` (~1023), the Phase-C /simplify cleanup commit `refactor({slug}): simplify cleanup pass` (~1086), the AVFL merge-review iteration commit `fix(avfl): resolve integration findings — iteration {N}` (~1768), the E2E routine auto-fix commit `fix(e2e): auto-fix …` (~2135), and the end-gate requested-change commit `fix(endgate): apply requested change — …` (~2511). All six carry the blind-to-untracked-files defect.

**D2 (security-auth-isolation) — the ledger append uses a shell-unsafe `printf`.** `build-ledger.md:23` (and the two workflow.md prescriptions that mirror it) prescribe `printf '%s\n' '{…json…}' >> ledger` with the row JSON in shell single-quotes. Row fields carry free prose (finding summaries, dismissal rationales, developer change-request text); any apostrophe terminates the quoting early (corruption + injection-shaped hazard, since summaries can echo reviewed repo content), and an embedded newline splits one logical row across lines. The rehydration parser at step 2.0 is told only to "parse each line as JSON" with no rule for the partial final line a crash-mid-append leaves — the exact moment the journal must survive. (sprint-2026-06-10 sidestepped this by writing the ledger via a JSON serializer — the safe pattern to codify.)

## Acceptance Criteria

1. **Every Conductor commit site stages newly-created files.** All **six** `git add -u` sites enumerate the worktree change set with `git status --porcelain` (which lists untracked files, unlike `git add -u`) and stage the in-scope paths explicitly, so a brand-new (untracked) in-scope file is committed rather than left behind. The six sites are the story commit (`feat({slug}): implement …`), the Stage-3 Phase-B per-finding fix commit (`fix({slug}): auto-fix …`), the Phase-C /simplify cleanup commit (`refactor({slug}): simplify cleanup pass`), the AVFL iteration commit (`fix(avfl): …`), the E2E auto-fix commit (`fix(e2e): …`), and the end-gate change commit (`fix(endgate): …`).
2. **A green-field story's new file survives to the commit.** A story whose sole deliverable is a new file (a new skill, reference, test, or eval) is committed by the Conductor with that new file present in the commit — demonstrated by an eval or a walked scenario over the story-commit path. (Pre-fix, the new file is absent from the commit and is destroyed at worktree cleanup.)
3. **Each write-scope guard reasons over the enumerated set, and discards out-of-scope files by specific path.** All **three** WRITE-SCOPE COMMIT GUARD blocks — the story commit (guard at ~workflow.md:590, on `git diff --name-only --cached`), the Stage-3 Phase-B fix-loop guard (~1007, on `git diff --name-only`), and the end-gate guard (~2504, on `git diff --name-only`) — evaluate the porcelain-enumerated set (tracked modifications AND untracked new files), not the tracked-only view their current `git diff` enumeration returns. (The Phase-C /simplify commit at ~1086 reuses the Phase-B guard — "the same write-scope guard used in Phase B" — so hardening the ~1007 guard covers it; its staging line is covered by AC 1.) An out-of-scope file is discarded by its specific path — untracked via `git clean -f -- <path>`, tracked via `git checkout -- <path>` / `git restore` — never via a blanket `git clean -f` (which would also delete in-scope new files), and it still emits the existing `conductor-warning` ledger row.
4. **A hostile prose field cannot corrupt a ledger row.** A ledger row whose free-prose field contains an apostrophe, a double-quote, or an embedded newline is written as exactly one valid JSONL line that round-trips through the rehydration parser unchanged — the field does not terminate the shell quoting, corrupt the row, or split across lines. The mandate is codified at all three append-prescription sites: `build-ledger.md` §Append-Only Rules (currently `:23`), the LEDGER-APPEND STANDING RULE (`workflow.md` ~209–217), and the step 2.0 append note (`workflow.md` ~254). The safe construction is: JSON-escape and newline-flatten every free-prose field before interpolation, or compose the row via a quoted heredoc / JSON serializer rather than single-quoted `printf`.
5. **A malformed or partial final line survives rehydration.** The step 2.0 rehydration loop (`workflow.md` ~260 — "Read all lines … Parse each line as a JSON object") handles a line that fails to parse, including the partial final line left by a crash mid-append: it skips that line, appends a `conductor-warning` ledger row naming the unparseable content, and continues rehydration to completion — it never aborts the resume. This warning is a new live event, so it IS a real ledger append; the step-2.0 rehydration-exemption (~217) covers only replayed rows, not this warning.

## Tasks / Subtasks

- [ ] **Task 1 — Porcelain-enumerated staging at all six sites.** Replace `git add -u` with `git status --porcelain` enumeration plus explicit staging of the in-scope paths at all six commit sites (story commit ~617, Stage-3 Phase-B fix ~1023, Phase-C /simplify ~1086, AVFL ~1768, E2E ~2135, end-gate ~2511). Stage the produced file set (the agent/fixer's returned `file_list` where available) rather than blanket-staging all untracked paths, so stray scratch files are not swept in. (AC 1, 2)
- [ ] **Task 2 — Route all three write-scope guards over the enumerated set with path-scoped discards.** At the story-commit guard (~590), the Phase-B fix-loop guard (~1007), and the end-gate guard (~2504), replace the tracked-only `git diff --name-only` enumeration with the porcelain-enumerated set (including untracked new files) and discard out-of-scope files by specific path (`git clean -f -- <path>` for untracked, `git checkout -- <path>` / `git restore` for tracked); preserve the existing `conductor-warning` / scope-revert ledger emissions on an out-of-scope file. The Phase-C /simplify commit (~1086) reuses the Phase-B guard, so it is covered by the ~1007 change; verify no separate hardening is needed there. (AC 3)
- [ ] **Task 3 — Codify shell-safe ledger append at all three prescription sites.** Update `build-ledger.md:23`, the LEDGER-APPEND STANDING RULE (`workflow.md` ~209–217), and the step 2.0 init append note (`workflow.md` ~254) to mandate escape/flatten of free-prose fields or a quoted-heredoc / serializer construction — so an apostrophe or newline in any field cannot corrupt the row or the JSONL contract. Keep the three sites consistent with one another. (AC 4)
- [ ] **Task 4 — Add the malformed/partial-line skip-and-warn rule to step 2.0 rehydration.** At the "Read all lines … Parse each line as a JSON object" loop (~260), specify: on a parse failure (including the partial final line from a crash-mid-append), skip the line, append a `conductor-warning` ledger row naming the unparseable content, and continue — never abort. Note explicitly that this warning is a live append (not covered by the rehydration exemption at ~217). (AC 5)

## Dev Notes

- Both are pre-existing conductor surfaces that this sprint's changes made newly consequential: the no-commit change (DEC-035) surfaced D1 (staging blindness), and introducing the build-ledger (DEC-035/DEC-036) surfaced D2 (append safety). `conduct-dev-commit-authority-reconciliation`'s AC7 was correctly forbidden from touching conductor staging, which is why both findings remained open. (D1/D2 name the two escalation findings throughout this story, not the causal changes.)
- Recommend doing this as the first conduct quick-fix after sprint-2026-06-10 (developer's stated disposition).

### Decision Authority

- **DEC-035** — One human end-gate; dev agents never commit, so the Conductor's staging step is the sole commit path. This is what makes D1 (blind `git add -u`) load-bearing: there is no second staging pass to catch a dropped new file. `build-ledger.md` cites DEC-035 as the decision the ledger makes durable.
- **DEC-036** — Stakes/timing tiers the ledger records (`stakes_class`, `timing_tier`); the free-prose fields whose safety D2 concerns (`summary`, `finding_summary`, `dismissal_rationale`, `evidence`, `suggested_fix`, developer change-request `items`) are the payload that must survive escaping. The mid-flight bar must not be widened by this change — it is a mechanical hardening, not an escalation-policy change.
- The Conductor is the **sole git-mutation authority** (stated at ~workflow.md:616, ~1756, and the GIT WORKING CONTEXT INVARIANT near the end-gate site). Do not introduce any additional commit path; harden the six existing ones in place.

### Current State of Affected Files

- **`skills/momentum/skills/conductor/workflow.md`** (~2500+ lines). **Six** `git add -u` sites, **three** of them behind a WRITE-SCOPE COMMIT GUARD (a fourth, Phase-C, reuses the Phase-B guard):
  - Story commit (~617): preceded by the guard at ~590 which today runs `git diff --name-only --cached` and unstages any staged path not in `{{writable_files}}` — but since `git add -u` never staged the new file, the guard never sees it either. Both staging and guard are blind to untracked files.
  - Stage-3 Phase-B per-finding fix commit (~1023): preceded by the fix-loop guard at ~1007, which enumerates via `git diff --name-only` (working-tree modifications to TRACKED files only) and drives the SCOPE-REVERT path. Because `git diff --name-only` — like `git add -u` — omits untracked files, a new file produced by the Phase-B fixer is invisible to BOTH the guard and the staging. Harden the enumeration to porcelain here.
  - Phase-C /simplify cleanup commit (~1086): the capture-and-commit step at ~1082 says "Apply the same write-scope guard used in Phase B" (i.e., reuses the ~1007 guard) then `git add -u`. Same untracked blindness; hardening ~1007 + the ~1086 staging line covers it.
  - AVFL iteration commit (~1768) and E2E auto-fix commit (~2135): integration-fix commits on the sprint branch, no per-story `writable_files` guard — Task 1 (enumerate + stage produced files) applies; Task 2 (guard) does not.
  - End-gate change commit (~2511): guard at ~2504 uses `git diff --name-only` + `git checkout -- P` for out-of-scope tracked files; same untracked blindness.
  - Note: the two merge-conflict staging sites (~1391, ~1417) already use explicit `git add <resolved-files>` and are out of scope for this story.
  - Ledger-append prescriptions to harden: the LEDGER-APPEND STANDING RULE (~209–217, the `printf '%s\n' '<row-json>' >> {{ledger_path}}` pattern that every build_log site inherits) and the step 2.0 init note (~254). The rehydration parse loop to harden is at ~260.
- **`skills/momentum/skills/conductor/references/build-ledger.md`** (176 lines). Line 23 prescribes the single-quoted `printf` append. The `conductor-warning` event (needed by AC 5) already exists in the controlled event-type set (Conductor-Level Events table, `story_slug` optional, `reason` non-empty) — reuse it; do not add a new event type. The append-only rules (§17–26) and the crash-loss bound ("a crash loses at most the event in flight") are the invariants the escaping and skip-and-warn rules must preserve.

### Architecture Compliance

- **Anchor commit sites by their commit-message label, not by line number** — `grep "add -u"` finds all six; the six labels (`feat({slug}): implement`, `fix({slug}): auto-fix` [Phase-B], `refactor({slug}): simplify cleanup pass` [Phase-C], `fix(avfl): resolve integration findings`, `fix(e2e): auto-fix`, `fix(endgate): apply requested change`) are stable; the line numbers in this story are approximate and will drift.
- Keep the three append-prescription sites (build-ledger.md, standing rule, step 2.0 note) mutually consistent — the standing rule explicitly exists to avoid repeating the append mechanism at ~30 sites, so its single prescription is the one all build_log appends inherit. Changing one site's mechanism without the others reintroduces drift (the exact failure `conduct-ledger-append-site-dedup-guards` and the retro-finding note in build-ledger.md warn against).
- Do not widen the `git clean` blast radius: path-scoped `git clean -f -- <path>` only. A blanket `git clean -f` in a worktree would delete in-scope untracked deliverables — introducing a worse instance of the very defect this story fixes.

### Testing Requirements

- Verification method (advisory): **`skill-invoke`** — invoke the conductor workflow / observe behavior; this is a `skill-instruction` change to `workflow.md` + `references/`. Per the verification standard, the routing key is `change_type`, and the harness derives the method from it.
- AC 2 (green-field staging) is the primary observable: an `evals/*.md` behavioral eval, or a walked scenario, exercising the story-commit path with a story whose deliverable is a single new file, and asserting the new file is in the resulting commit.
- AC 4 (hostile prose) is observable by constructing a row whose prose field contains `'`, `"`, and `\n`, appending it via the codified mechanism, then reading the ledger back with a JSON-per-line parser and asserting exactly one row, byte-faithful.
- AC 5 (partial line) is observable by appending a truncated final line to a fixture ledger, running the rehydration loop, and asserting it completes, skips the bad line, and emits a `conductor-warning`.
- These ACs reference workflow-internal mechanics because the deliverable IS the workflow file; keep the frozen contract's verification steps to ordinary-user-observable outcomes (new file committed; ledger round-trips; resume completes) per the anti-insider-knowledge guard, not to internal symbol assertions.

### Project Context Reference

- Sibling hardening already shipped in this epic: `conduct-ledger-append-site-dedup-guards` (dedup guards across 9 append sites) extended the **duplicate-prevention guard** at `workflow.md:404` (the `{{ledger_seen_events}}` dedup note) — a DIFFERENT construct from the **LEDGER-APPEND STANDING RULE** at `workflow.md:209–217` (the append *mechanism*) that this story hardens. This story is orthogonal to the sibling: append *safety* (shell-escaping) vs. append *dedup*. The "keep consistent" obligation in this story refers to the three append-*mechanism* prescription sites (`build-ledger.md:23`, the ~209 standing rule, the ~254 step-2.0 note) — not the ~404 dedup guard, which this story does not touch.
- This story is one of the operational-hardening items the `momentum-conductor-core` epic tracks as deciding "whether the practice can trust an autonomous build end-to-end."

### References

- Epic context: `momentum-conductor-core` (from _bmad-output/planning-artifacts/epics.json)
- Source: sprint-2026-06-10 end-gate escalations D1 (irreversible-destructive) + D2 (security-auth-isolation).
- Decisions: DEC-035 (one end-gate; dev agents never commit), DEC-036 (stakes/timing tiers).
- Behavioral spec for the ledger: `skills/momentum/skills/conductor/references/build-ledger.md`.

## Momentum Implementation Guide

**Change Types in This Story:**
- Tasks 1–4 → skill-instruction (EDD) — all edits land in `skills/momentum/skills/conductor/workflow.md` and `skills/momentum/skills/conductor/references/build-ledger.md`.

---

### skill-instruction Tasks: Eval-Driven Development (EDD)

**Do NOT use TDD for `workflow.md` / reference files.** Skill instructions are non-deterministic LLM prompts — unit tests do not apply. Use EDD:

**Before writing a single line of the change:**
1. Write 2–3 behavioral evals in `skills/momentum/skills/conductor/evals/` (create `evals/` if it doesn't exist):
   - One `.md` file per eval, named descriptively (e.g., `eval-green-field-new-file-is-committed.md`, `eval-ledger-append-survives-apostrophe.md`, `eval-rehydration-skips-partial-line.md`).
   - Format each eval as: "Given [the input and context], the Conductor should [observable behavior]."
   - Test behaviors and decisions (new file present in commit; ledger row round-trips; resume completes past a bad line), not exact prose of the workflow.

**Then implement:**
2. Edit `workflow.md` (six staging sites, three guards, standing rule ~209–217, step 2.0 note ~254, rehydration loop ~260) and `build-ledger.md:23`. Preserve all surrounding behavior — this is a targeted hardening, not a rewrite.

**Then verify:**
3. Run evals: for each eval, spawn a subagent via the Agent tool, give it the eval scenario plus the relevant workflow section as context, and observe whether behavior matches the expected outcome.
4. All evals match → task complete. Any eval fails → diagnose the gap, revise, re-run (max 3 cycles; surface if still failing).

**NFR compliance — mandatory for skill-instruction work:**
- `workflow.md` has no SKILL.md `description`/frontmatter of its own (it is loaded by `create-story`'s sibling `conductor/SKILL.md`); do not add frontmatter to `workflow.md`. If any edit touches `conductor/SKILL.md`, keep `description` ≤150 chars and `model:`/`effort:` present.
- Keep any single file you edit under the 500-line / 5000-token guidance where practical; `workflow.md` already exceeds this by design (it is the reference body, not a SKILL.md) — do not attempt to shrink it as part of this defect fix; make only the targeted edits.
- Follow `skills/momentum/references/agent-skill-development-guide.md` for skill/workflow conventions (per the dev-skills rule).

**Additional DoD items (added to the standard bmad-dev-story DoD):**
- [ ] 2+ behavioral evals written in `skills/momentum/skills/conductor/evals/` covering AC 2, AC 4, AC 5.
- [ ] EDD cycle ran — all eval behaviors confirmed (or failures documented).
- [ ] All six `git add -u` sites converted to porcelain-enumerated staging (AC 1); all three guard blocks route over the enumerated set with path-scoped discards (AC 3).
- [ ] All three append-prescription sites codify shell-safe construction and remain mutually consistent (AC 4).
- [ ] The step 2.0 rehydration loop carries the skip-and-warn rule and never aborts (AC 5).
- [ ] AVFL checkpoint on the produced artifact documented (momentum:dev runs this automatically — validates the edited workflow against these ACs).

**Frozen verification contract reminder:** A frozen verification contract for this story exists for the sprint at `.momentum/sprints/{sprint-slug}/specs/{story-slug}.{ext}`. Before signaling done, read only the Part-A header (`how_dev_self_checks`, `verification_method`, `harness_profile`) as a self-check. Do NOT read the verifier body (Part B: scenarios, assertion scripts, Gherkin) beyond sections `how_dev_self_checks` explicitly references.

## Dev Agent Record
