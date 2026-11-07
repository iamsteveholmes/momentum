# Momentum Audit 01b: Gap Addendum (2026-11-07)

Addendum to the Phase 1 capability map and Phase 2 outcomes report. It covers three areas those reports did not map: the vendored BMAD suite, the legacy journal and local install, and the conduct fixtures, generators and CI. All findings are read-only; counts come from grep and git history, not from transcripts of runtime invocation.

## 1. Vendored BMAD suite

### Inventory

| Item | Fact |
|---|---|
| momentum repo `.claude/skills` | 69 `bmad-*` dirs (plus 3 `avfl-*` and `frontend-dev-workspace`); none are symlinks |
| nornspun / chorgi | 69 / 71 `bmad-*` skills |
| nornspun-backend / nornspun-client / global `~/.claude/skills` | 0 / 0 / 0 |
| `_bmad/` runtime tree (momentum) | 167 files, 1.2 MB (bmm 94, tea 32, cis 7, core 2, bmb 2) |
| BMAD version | 6.8.0 per manifests (updated in place, June 2026); 6.2 install date (2026-03-19) comes from git history |
| Momentum skills | 30 dirs; 9 name a BMAD skill (plus `agents/dev.md` and 4 references) |

Most of the 69 vendored skills are unused. Only about 11 are referenced by Momentum at all.

### What Momentum adds, per layer

Momentum wraps three BMAD skills and bypasses the rest.

| Layer | BMAD base | What Momentum adds |
|---|---|---|
| `create-story` (423 lines) | `bmad-create-story` (429) | Enriches intake stubs in place, moves stories to `.momentum/stories/`, classifies change type, injects an EDD/TDD Implementation Guide, runs AVFL validation |
| `dev` (219) | `bmad-dev-story` (500) | No-commit rule (Conductor owns git), self-check against the contract, stakes-driven fix mode, structured completion signal with `file_list` |
| `code-reviewer` (367) | `bmad-code-review` (90 + steps) | Non-interactive, report-only, one story diff at a time; findings normalised to a canonical schema with `stakes_class` |
| `conductor` (3,263 lines) | none | Worktrees, merge, AVFL-on-merge, E2E, single end-gate, resume cards |
| `sprint-planning` (1,672) | `bmad-sprint-planning` (status file only) | Team composition, Gherkin ATDD, plan gate; never invokes the BMAD skill |

By size, the three wrappers total about 1,000 lines. The conductor and sprint-planning total about 4,900 lines of orchestration that BMAD does not have. PRD, architecture and epics creation, UX, retrospective, `tea`, `cis` and the personas are untouched by Momentum and stay pure BMAD.

### Attribution

Nornspun used BMAD before Momentum: BMAD 6.2 was installed 2026-03-19, and PRD, architecture and epics (17 blockers fixed) landed 2026-03-20. Momentum's story machinery arrived about three weeks later (`.momentum/stories` migrated 2026-05-03). So the PRD-to-epics-to-stories decomposition is a BMAD-style inheritance.

Mapping the Phase 2 struggles (S-numbers per audit-02):

- **BMAD-style ceremony component (all shared with Momentum):** S1 (story completion as the unit of progress; BMAD never defines "the feature works"), S6 (spec volume; the 635 KB end-gate HTML is Momentum's), S12 (backlog volume from fine-grained decomposition, multiplied by Momentum intake and retro), S15 (BMAD 6.9/6.10 upgrades broke about 69 hardcoded paths; Momentum's hardcoding, BMAD's trigger).
- **Momentum-specific design:** S2 (agent PASS overstated), S3 (sprint 08-03 failed), S4 (unmerged branches), S7 (loop never closes), S8 (97 subagents for 4 stories), S9 (E2E validator design; Gherkin fits under 5% of stories, a Momentum ATDD choice), S10, S11, S13, S14, S16.
- **Mixed:** S5 (meta-work); some Nornspun docs commits are real BMAD-style product specs, but the commit ratio and 65+ process-shaped retro stories are Momentum's.

Rough split: about 4 of 15 struggles have a BMAD-ceremony component, all shared. About 9 are Momentum-only. The "104 done, 0 of 15 passing" outcome is mostly a Momentum design problem: BMAD supplied the unit of work, Momentum supplied the false-green signal and the overhead around it.

Caveat: references were counted by grep; BMAD base text was not diffed line by line against the wrappers.

## 2. Legacy journal and local install

**The journal is a test fixture, not history.** `.claude/momentum/journal.jsonl` is 5 lines (323 bytes) of synthetic thread events dated 2026-04-05, two deliberately corrupt. `journal-view.md` and `test-bad.json` are the same kind of malformed-input artifact. It contributes no early-era outcome data.

**Real early evidence survives elsewhere:**

- `installed.json` counters: `momentum_completions: 11` (first invocation 2026-04-04) in both the momentum and Nornspun copies. The identical count suggests a shared or copied counter (inference).
- Nornspun sprint logs (56 lines, `.claude/momentum/sprint-logs/`), the only surviving subset. The momentum repo deleted its logs on 2026-05-01 (`333af7cf`, 204 KB), which is why Phase 2 saw no pre-September detail.
  - `sprint-2026-04-05`: 5 stories (d4-1 to d4-5) chosen from a 68-story backlog across 11 epics; closed with "56/71 E2E scenarios pass. 8 runtime bugs found and fixed. 5 deferred."
  - `sprint-2026-04-08`: 10 client-UI stories; AVFL cut 39 claimed spec-impact findings to 11 valid; no completion entry.
  - Epic grooming on 04-08 counted 105 stories across 9 epics.
- `feature-status.md` (2026-05): Momentum 3 working / 14 partial / 4 not-started; Nornspun 15 features with 4 working and 5 partial, derived from story status rather than verification.

**What this adds to Phase 2:**

- The story-versus-feature gap was visible in April: 8 runtime bugs surfaced only at E2E, and the same plan, dev, E2E loop continued.
- A hundred-story backlog existed by early April, well before "104 done".
- In May the Nornspun view showed 4 working, against 0 of 15 verified later. Story-completion tracking overstated progress from the start.
- Early design churn: the Impetus greeting menu design (mockup v8) was abandoned for prose; feature-status was deprecated for the canvas.
- Controls existed but were advisory: `stop-gate.sh` always exits 0; `protected-paths.json` guards acceptance tests and sprint specs; `check-version-bump.sh` is the only mechanical release gate.

Limits: the log is decision-only (no failure, retry or cost events), so friction is read indirectly. No journal transcripts exist. `.claude/momentum/` exists only in momentum and Nornspun (not backend, client or chorgi).

## 3. Conduct fixtures, generators and CI: reproducibility

**Verdict: nothing here reproduces a conductor run end to end.** The only runnable check is a static contract verifier, and it passes.

| Path | Status |
|---|---|
| `.momentum/fixtures/sprint-fixture-conduct-e2e/` | Two trivial stories, frozen sha256 contracts, placeholder approval sha. No `output/` exists, so its smoke script would fail if run (inferred, not executed). |
| `skills/momentum/scripts/verify-sprint-build-consumable.sh` | Ran against the fixture: 2/2 PASS, exit 0. Checks record shape only, not that a build ran. |
| `.momentum/gen-endgate-report.py` | Not re-runnable; reads missing `/private/tmp/...` task outputs. Comment calls it one-off. |
| `.momentum/gen-conduct-runnable-report.py` | Not re-runnable; needs missing `/tmp/story-diffs.json`. Its other inputs exist (25 records in `conduct-runnable-build-results.jsonl`, outcomes unconfirmed). |
| `.momentum/signals/` | Schema README only; no signal files; writers deferred to "follow-up stories". |
| `.github/workflows/` | Only `pages.yml` (deploys `site/`). No test or lint CI. |
| Other | No `tests/` dir, no `package.json` test script. `test-momentum-tools.py` and two live e2e drivers exist but were not run. `.worktrees/` is absent. |

Consequence for the planned rerun: there is no harness to reuse. A Momentum-versus-vanilla comparison must be built fresh, and the conductor's own correctness has never been regression-tested in CI.

## Implications for the verdict

- BMAD ceremony alone did not produce "104 done, 0 of 15 passing"; the false-green signal and process overhead are Momentum's.
- Momentum's BMAD wrappers total about 1,000 lines and are cheap to keep or drop; the 4,900 lines of orchestration are the real cost and the real bet.
- Pivoting away from Momentum leaves PRD, architecture and epics steps (pure BMAD) unaffected.
- A fair comparison needs two arms beyond vanilla: BMAD story files with plain Claude Code, and Momentum on top, to isolate decomposition from conductor and gates.
- Pin models per original story; Nornspun mixed models and a cheap runtime LLM contributed to S1.
- The story-versus-feature gap appears in April evidence (56/71 E2E, 8 late bugs) and in the May 4-working view, so it is original design, not late drift.
- The conductor has no reproducible test or CI; claims about its behaviour rest on one-off reports whose generators no longer run.
- Early-era evidence is thin (journal is a fixture, logs mostly deleted); conclusions about April rest on 56 log lines, counters and git history.
