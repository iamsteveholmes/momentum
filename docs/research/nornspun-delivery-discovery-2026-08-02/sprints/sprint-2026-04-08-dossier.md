# Sprint Dossier — sprint-2026-04-08

**Date compiled:** 2026-08-02
**Role:** Evidence dossier for one sprint within the "why doesn't anything work end-to-end" discovery investigation.

---

## Executive Summary

1. **This sprint's INTENT was explicitly, unusually clearly user-capability-framed.** It was driven by ASR-001 ("Community Readiness & Core Loop Gap Analysis," 2026-04-08), which stated its purpose as "Evaluate whether Nornspun can demonstrate its core value loop (campaign init → session capture → session prep) to the PF2e community" and named the sprint's four new stories verbatim as the "Missing Stories (Not in Backlog)" needed to close that gap. This sprint is a counter-example to "sprints are never framed around capability" — this one explicitly was.
2. **Real, verifiable client-side code shipped on 2026-04-09** for 9 of the 10 stories: Verdandi was genuinely unlocked in the Norn selector (`isComingSoon(VERDANDI) → false`, confirmed still present today), an adventure-upload file picker was wired on Android, campaign_id is genuinely created/persisted across app launches, and five UI/accessibility/polish fixes landed with tests. This is confirmed by direct git commits in `nornspun-client` (e.g. `75afe4f`, `a39fac0`, `a98043d`, `9f3bf5c`) — not by inference from tracker status.
3. **The sprint's retro-transcript-audit.md is not about this sprint.** Every keyword search for this sprint's actual story slugs (`wire-campaign-id-through-client`, `unlock-verdandi-in-client`, `d4-14…`, etc.) returns 0 hits in `audit-extracts/`. The transcript timestamps (Apr 7 23:24 – Apr 8 23:09) and every first_prompt/content match the **`quickfix-epic-story-taxonomy-migration`** work instead (confirmed via literal agent prompts: *"You are the momentum:create-story agent... story spec file for a taxonomy migration"*). The retro doc was created in commit `55dda4e` (2026-04-10) — this was wrong from the moment it was written, not a later archival accident.
4. **In that same commit (`55dda4e`), all 10 stories were bulk-promoted from `review` to `done`** in `stories/index.json` — with zero connection to any transcript evidence of what those stories actually did, because the transcript audit that ostensibly backs the retro is auditing different work entirely. Each story's own file still says `**Status:** review` (one still says `ready-for-dev`) to this day — the promotion only ever touched the index, never the story files.
5. **One story's own Dev Agent Record documents, in real time, that prior "done" stories had no code behind them** — and then built its deliverable in a completely disconnected, non-canonical copy of the repository that was silently deleted seven weeks later. `d4-14-end-to-end-session-loop-integration-test`'s Dev Agent Record states: *"Backend skeleton had no D4 implementation (D4.2, D4.4, D4.5 marked done in stories/index.json but code not present)."* This is **false** for the canonical backend (D4.1–D4.5 commits are real, on `main`, in `~/projects/nornspun-backend`) — the dev agent was reading a stale duplicate directory (`~/projects/nornspun/nornspun-backend/`, "Tree B") nested inside the planning-hub repo. It rebuilt the entire backend infrastructure and the integration test inside Tree B; none of that work — including the test the story exists to deliver — was ever committed to the real backend. Tree B was deleted on 2026-05-29 (`dbc8615`, per assessment ASR-003) as dead weight, with the deletion note flagging its last activity as "~Apr 9" — this sprint's date. **The story's entire claimed acceptance criteria were never met against the real system, and no one caught it for seven weeks.**
6. **Aftermath is genuinely mixed, not uniformly negative.** Verdandi-unlock and 5 of the fix/polish stories hold up under later inspection. Adventure-upload is real but partial — `features.json` (re-verified 2026-06-16, ASR-006) notes it is "done on ANDROID, DESKTOP ABSENT (MainWindow.kt TODO — no JFileChooser)" though the story was marked done without that qualification. The one story whose entire job was to *prove the loop coheres end-to-end* (`d4-14`) is the one that silently produced nothing real.
7. **The sprint's own scope selection reflects sound reasoning, not just task-listing**: 3 of 10 stories are net-new user-facing features (change_type `feature`/`feat`), 5 are fix/polish (`fix`), 1 is a deliberate research spike (scoped down rather than built, a good call per the retro), and 1 is the test-infra story that failed. That is a defensible mix for a "close the wiring gaps before a demo" sprint — the failure here is not scope, it's unverified completion.

---

## 1. INTENT — What was this sprint for?

No `coverage-plan.md` or `plan-gate-decision.md` exists in `.momentum/sprints/sprint-2026-04-08/` — those artifact types postdate this sprint. Intent is reconstructed from the assessment that generated the sprint's stories and from the stories' own framing.

**The motivating assessment: ASR-001 "Community Readiness & Core Loop Gap Analysis"** (`_bmad-output/planning-artifacts/assessments/asr-001-community-readiness-2026-04-08.md`, committed `7b2439d`, same day as the sprint). Its stated Purpose:

> "Evaluate whether Nornspun can demonstrate its core value loop (campaign init → session capture → session prep) to the PF2e community, and identify every gap standing between current state and that goal."

Its method was explicitly built to avoid the "story-vs-functionality" trap this whole investigation is about — Finding 1's own framing: *"The backend is substantially more complete than story status suggests. Real implementations, not stubs."* It found three concrete UI-to-backend wiring gaps and one missing verification step, and named them **as the four stories this sprint would build**, verbatim:

> "**Missing Stories (Not in Backlog)**
> 1. Wire campaign_id through client — FirstLaunch → campaign creation → persist → include in all requests
> 2. Unlock Verdandi in client — flip isComingSoon, wire pip to actual Norn switch
> 3. Adventure upload UI — minimal file picker that POSTs to backend endpoint
> 4. End-to-end session loop integration test — verify the full cycle works across both repos"

This is a **USER CAPABILITY** framing, stated as such, and unusually explicit for this era of the practice: the assessment is *specifically* checking "does the backend's real work reach a user" rather than counting completed tickets. Sprint-2026-04-08 folded these four ASR-001 stories in with six pre-existing fix/polish stories (several inherited from sprint-2026-04-06's backlog — the specs for `onboarding-cta-visibility`, `norn-switch-clears-chat-and-maintains-session`, `fix-skuld-pip-touch-target`, `accessibility-labels-content-descriptions`, and `desktop-window-sizing-and-scroll` also exist verbatim in `.momentum/sprints/sprint-2026-04-06/specs/`, confirming carryover) plus one deliberately-scoped-down item (`sf2e-scoping-spike`, an explicit "let's punt on full Starfinder 2e support and just scope the work" decision).

**Verdict on intent:** genuinely capability-framed, at both the assessment and story level. This sprint is a positive counter-example to a hypothesis that says "sprints never frame around user capability."

---

## 2. PLAN — Stories, waves, team, and story-type mix

**Source:** `.momentum/sprints/index.json`, `completed[]` entry for `sprint-2026-04-08`.

10 stories in 2 waves:

| Wave | Stories | Note |
|---|---|---|
| 1 | `onboarding-cta-visibility`, `norn-switch-clears-chat-and-maintains-session`, `adventure-upload-ui-file-picker-for-pdf-ingestion`, `sf2e-scoping-spike`, `desktop-window-sizing-and-scroll`, `accessibility-labels-content-descriptions`, `fix-skuld-pip-touch-target` | 7 stories, parallel |
| 2 | `wire-campaign-id-through-client`, `unlock-verdandi-in-client`, `d4-14-end-to-end-session-loop-integration-test` | index.json note: "d4-14... moved to Wave 2: its Dev Notes require wire-campaign-id and unlock-verdandi companion stories to be implemented first as context for the full-cycle validation" |

Team: one `dev-frontend` specialist carrying 6 of Wave 1's stories + both Wave 2 client stories; one `general-purpose` agent for the `sf2e-scoping-spike`; one `dev` (backend/pytest) specialist assigned to `d4-14`, explicitly separated from `dev-frontend` per the story's own header (`**Specialist:** dev (backend Python/pytest — NOT dev-frontend)`).

**Story-type mix** (from each story file's `Change Type:` field):

| Change type | Count | Stories |
|---|---|---|
| feature / feat (net-new user capability) | 3 | wire-campaign-id-through-client, unlock-verdandi-in-client, adventure-upload-ui-file-picker-for-pdf-ingestion |
| fix (polish / bug fix, user-visible) | 5 | desktop-window-sizing-and-scroll, accessibility-labels-content-descriptions, fix-skuld-pip-touch-target, onboarding-cta-visibility, norn-switch-clears-chat-and-maintains-session |
| test (infra/verification, no direct user surface) | 1 | d4-14-end-to-end-session-loop-integration-test |
| research/spike (deliberately not implementation) | 1 | sf2e-scoping-spike |

**30% net-new product capability, 50% user-visible fix/polish, 10% test-infra, 10% spike.** By count this reads as capability-heavy for an early sprint — the "fix" stories are themselves user-visible correctness work (touch targets, accessibility labels, CTA visibility), not internal refactors. The one item that is pure infrastructure (`d4-14`) is also the one that failed to land (§5–6).

---

## 3. EXECUTION — What the transcript evidence actually shows (and doesn't)

**The retro-transcript-audit.md at `.momentum/sprints/sprint-2026-04-08/retro-transcript-audit.md` documents a different piece of work than this sprint.** This is the central process-hygiene finding of this dossier and is fully verified, not inferred:

- Its Executive Summary states: *"Sprint-2026-04-08 was a planning and specification sprint — no production code shipped... a full epic taxonomy migration (from sequential numbered identifiers to descriptive categorical slugs), a comprehensive product state assessment... 54 agents."*
- Direct keyword search of `audit-extracts/*.jsonl` (the raw data backing that retro) for every one of this sprint's actual story slugs returns **0 hits** for 8 of 10 slugs, and the 2 non-zero hits are passing mentions in an unrelated priority-evaluation fan-out, not dev-work discussion (verified: `grep -c` for each of `wire-campaign-id-through-client`, `unlock-verdandi-in-client`, `adventure-upload-ui-file-picker-for-pdf-ingestion`, `d4-14-end-to-end-session-loop-integration-test`, `sf2e-scoping-spike`, `desktop-window-sizing-and-scroll`, `onboarding-cta-visibility` = 0; `fix-skuld-pip-touch-target` and `norn-switch-clears-chat-and-maintains-session` = 1 each, both incidental).
- Conversely, `agent-summaries.jsonl` contains a `momentum:create-story` agent prompt reading *"Your job is to create a story spec file for a taxonomy migration... Epics: `epic-d1`, `epic-d2`, ..., `epic-d8`... Stories: `d3-10-norn-switch-clears-chat`..."* and AVFL validator prompts explicitly labeled `task_context: "Quick-fix epic-story-taxonomy-migration"`. A `git error` in `errors.jsonl` shows a rename operation `d3-10-norn-switch-clears-chat-and-maintains-session.feature → norn-switch-clears-chat-and-maintains-session.feature` inside `sprint-2026-04-06/specs/` — this is the taxonomy migration stripping D-numbered prefixes from specs, timestamped inside this transcript window.
- The transcript's own timestamps (2026-04-07 23:24 → 2026-04-08 23:09, `errors.jsonl` + `user-messages.jsonl`) do fall within this sprint's calendar window, and the session IDs referenced (`01ce8756…`, `42c1b4a9…`, `7f8ccec4…`, `bc4bed9c…`) no longer exist as raw transcripts (confirmed: `ls ~/.claude/projects/-Users-steve-projects-nornspun/*.jsonl` shows only 16 files, all dated 2026-07-06 or later). **This means there is no recoverable transcript for how the 10 actual dev stories were executed** — only the git commits themselves (§5) and the story files' own Dev Agent Records survive as evidence of execution.
- This mis-audit is not a later archival-migration side effect (as it was for a sibling sprint, per that sprint's dossier). The file was created directly in commit `55dda4e` (2026-04-10 21:47:57) — the retro was wrong the moment it was written.

**What we do know about execution**, from story-file Dev Agent Records and git commits (§5): the 9 client-facing stories were implemented same-day (2026-04-09) by what git commit trailers identify as "Claude Sonnet 4.6," in a rapid sequence of ~12 commits between 11:02 and 16:05 local time, including at least one immediate same-day fix commit (`c40451f fix(client): wire campaign UUID, fix path prefix, correct min window, persist norn on switch`, 11:58) suggesting a quick review-and-patch cycle rather than a single blind pass. No AVFL/code-review agent activity for this specific work is traceable (the practice's `momentum:conductor` build orchestrator did not exist yet — first live run was 2026-06-09 per prior project memory — so this sprint predates any automated post-merge validation pipeline).

---

## 4. CLAIM — What the sprint asserted at completion

No `sprint-summary.md` exists for this sprint (also postdates this era). The claim has to be read from commit history:

- `d8c0408` (2026-04-09 12:11:39) — *"chore(sprints): complete sprint-2026-04-08 — set status=done, started=2026-04-08, completed=2026-04-09."* This is the sprint-level claim: done, one day turnaround.
- In the **same minute**, `7d4f44f` (2026-04-09 12:11:49) — *"docs(stories): update story statuses to review in index"* — sets all 10 stories to `review`, not `done`, at actual completion time. So the sprint-level "done" and the story-level "review" were simultaneously true on 2026-04-09: the sprint was closed while its stories were still pending sign-off.
- `55dda4e` (2026-04-10 21:47:57) — the retro commit — bulk-promotes all 10 stories from `review` to `done` in `stories/index.json`. This is the actual "claim of complete, verified functionality," and it happens in the same commit that files a retro-transcript-audit auditing unrelated work (§3). **No verification step connects this promotion to any evidence that the stories work.**

---

## 5. REALITY — What actually landed in the code, verified by git history

**Client repo (`nornspun-client`), verified real commits on 2026-04-09** (`git log --since="2026-04-09 00:00" --until="2026-04-09 23:59"`):

| Commit | Message | Maps to story |
|---|---|---|
| `028f30d` | feat(maestro): D3.19 add norn-pip-tap acceptance flow for all three Norn pip taps | fix-skuld-pip-touch-target |
| `eed53c4` | test(desktop): add window sizing contract tests for D3.18 | desktop-window-sizing-and-scroll |
| `8103b29` | test(accessibility): add and fix D3.16 accessibility label tests for both platforms | accessibility-labels-content-descriptions |
| `c8b3c5b` | test(ui): add D3.14 CTA visibility contract tests for Android and Desktop | onboarding-cta-visibility |
| `9f3bf5c` | feat(viewmodel): D3.10 add per-Norn conversation cache for Norn switching | norn-switch-clears-chat-and-maintains-session |
| `75afe4f` | feat(ui): unlock Verdandi norn in client selector (D3.21) | unlock-verdandi-in-client |
| `a39fac0` | feat(ui): ASR-001-C adventure upload — file picker, ViewModel, progress UI | adventure-upload-ui-file-picker-for-pdf-ingestion |
| `a98043d` | feat(client): wire campaign_id through client on first launch and returning sessions (D3.22) | wire-campaign-id-through-client |
| `c40451f` | fix(client): wire campaign UUID, fix path prefix, correct min window, persist norn on switch | same-day follow-up fix |
| `ef4f6cd`, `e44a49b`, `9bd01ce` | desktop window/UI polish fixes, same day | general polish |

Read the full commit bodies for the two feature commits: `a98043d` lists 13 concrete sub-changes (new models, nullable campaign_id fix, view-model wiring on both platforms, 3 new test suites); `75afe4f` lists flipping `isComingSoon(VERDANDI)` to `false` on both platforms plus inverted tests. These are not stub commits — they contain real logic changes and real new/updated tests, verified by reading the diffs (not just the messages).

**Backend repo (`nornspun-backend`) for `d4-14`: nothing landed.** `git log --all --diff-filter=A -- '*session_loop*'` returns zero results; `find . -iname "*session_loop*"` on the current checkout returns nothing; `git fsck --unreachable --no-reflogs` shows no dangling commit matching this work (the one dangling commit found, `70601ce`, is an unrelated March file-relocation commit). The file `tests/integration/test_session_loop_full_cycle.py`, which AC6 of the story requires to exist, has never existed in this repository's history on any branch, tag, or reflog entry.

**Where the `d4-14` work actually went — the "Tree B" discovery.** The `nornspun` planning-hub repo (not `nornspun-backend`) contains commit `0065661` (2026-04-09 11:37:24, same day): *"test(backend): D4.14 end-to-end session loop integration test — Implements the full session loop integration test and the backend infrastructure it depends on (D4.2, D4.4, D4.5 prerequisites were marked done in planning but code was absent from the repo)."* Its diff touches paths like `nornspun-backend/src/agents/verdandi.py`, `nornspun-backend/src/core/dependencies.py`, `nornspun-backend/tests/integration/test_session_loop_full_cycle.py` — **inside the planning-hub repo**, at a nested `nornspun-backend/` subdirectory that is not the real `~/projects/nornspun-backend` repo. Two more commits follow the same day (`ca897ca`, `0d6acbe`) fixing bugs in that same nested copy. This nested directory ("Tree B") sat unreferenced by any real deployment or CI (confirmed later, §6) until it was deleted wholesale on 2026-05-29.

The story's own Dev Agent Record independently confirms the mechanism from the inside: *"Backend skeleton had no D4 implementation (D4.2, D4.4, D4.5 marked done in stories/index.json but code not present). Implemented minimum viable backend infrastructure needed for test to compile and run."* — followed by a File List of ~20 files marked "(created)," including `src/agents/verdandi.py (created)`. This is independently falsifiable against the real backend: `git log --follow` on `src/agents/verdandi.py` in the real `nornspun-backend` repo shows it was substantially implemented on 2026-04-06 (`f2dbfd7`, 108 lines added to an existing file, not a fresh file) — three days before the d4-14 agent said it "created" it. The dev agent for d4-14 was reading and writing to the wrong tree throughout.

**Practical consequence:** the one story in this sprint whose entire purpose was to prove "the three wiring fixes work together end-to-end, before any community demo" never actually ran that proof against the real system. Every task checkbox in the story file's Tasks/Subtasks section is checked `[x]` through Task 6; only 7.2/7.3 (which require a live Postgres) are unchecked. The Completion Notes claim "All 12 existing tests continue to pass (no regressions)" — true only of the phantom Tree B copy, never checked against the real repo.

---

## 6. AFTERMATH — What later inspection found

**The Tree B duplicate was discovered and removed 7 weeks later**, by an unrelated investigation. `docs/assessments/asr-003-urd-agent-drift-directory-confusion-2026-05-28.md` (2026-05-28, retracting a different false "Urd agent never built" claim) documents:

> "Root Cause — Two Backend Trees... Tree B — stale stub copy... Path `~/projects/nornspun/nornspun-backend/`... Git: not a repo... State: D3.2 stub; **last `src` activity ~Apr 9**."

Resolution (2026-05-29, commit `dbc8615`): *"the stale embedded copy at `nornspun/nornspun-backend/` (39 tracked files + an ~83 MB untracked `.venv`/caches) was removed via `git rm -r`... A pre-removal sweep confirmed no active CI/run/build config referenced the nested path — the only hits were an archived 2026-04-09 sprint-status file... and historical 2026-04-12 retro audit records, the latter having already flagged this exact path confusion as a recurring agent problem."* So the confusion was known to have recurred at least once more (2026-04-12) before finally being fixed structurally in late May. **Important nuance for accuracy:** ASR-003's actual subject (the Urd agent, stories D1.2/D1.3) was found to be correctly built in the real repo — ASR-003 is a retraction of a *different*, broader "nothing was built" claim, not a confirmation of the d4-14 problem this dossier identifies. The d4-14-specific failure is this dossier's own finding, cross-checked independently against ASR-003's Tree A/Tree B topology and dated evidence, not something ASR-003 itself calls out by story name.

**The 9 client-side stories hold up reasonably well, with one real caveat.** `features.json` (`last_verified: 2026-06-16`, ASR-006):
- Session-prep feature notes confirm Verdandi's backend is "present" and real (consistent with the unlock story's premise).
- Adventure-upload feature: *"'working' was overstated: adventure-upload-ui-file-picker-for-pdf-ingestion is done on ANDROID, DESKTOP ABSENT (MainWindow.kt TODO — no JFileChooser). REVISE that story or split."* The story was marked fully `done` without a platform qualifier; a later assessment had to add the caveat.
- Direct code check today confirms the Verdandi-unlock and Skuld-pip-touch-target fixes are still present verbatim (`isComingSoon` returns `false` for `VERDANDI`; `zIndex(-1f) // D3.19: render below NornSelector pips` comment intact in `InnerThoughtsIndicator.kt`; `maestro/flows/norn-pip-tap.yaml` still exists).
- None of this sprint's 10 stories are marked `dropped`/`obsolete`/`parked` in the current `stories/index.json` — but 9 of the 10 story **files** still read `**Status:** review` (one `ready-for-dev`) even though the index says `done`; the file-vs-index status split introduced on 2026-04-09/10 was never reconciled.

---

## 7. VERDICT

**"After sprint-2026-04-08, a user could switch to Verdandi as a second, functioning Norn in the selector (previously locked as 'coming soon'), and could upload an adventure PDF via a file picker on Android (not Desktop), and would have their campaign persist automatically across app launches instead of being silently discarded — which they could not do before."**

This verdict is supportable strictly: `isComingSoon(VERDANDI)` genuinely flips to `false` in real, committed, still-present code; the Android adventure-upload file picker genuinely exists and posts to the real backend endpoint; campaign_id is genuinely created and persisted client-side per the diff of `a98043d`. These are not mocked, not behind a flag, not unreachable — they are default, live behavior in the shipped client, independently confirmed by a later assessment (ASR-006) rather than only by the sprint's own claim.

**What the verdict must NOT claim:** that the "core value loop" (campaign init → session capture → session prep, working coherently together) was verified end-to-end by this sprint, despite the sprint's own completion claim and ASR-001's stated goal. The one story built specifically to establish that (`d4-14`) produced no artifact that ever touched the real system — its test, its infrastructure, and its "all tests pass" claim exist only in a directory that was deleted seven weeks later as dead weight. The sprint delivered three of the four ASR-001 gap-closing capabilities for real; the fourth — proof that they cohere — was never actually established, and the tracker said it was.

---

## Counter-evidence & falsifiability

- **Counter to "nothing ships end-to-end":** 9 of 10 stories in this sprint produced real, still-present, independently-reconfirmed (ASR-006) user-facing changes. This sprint is evidence *against* a blanket claim that Momentum sprints never deliver working functionality.
- **Counter to "sprints never frame around capability":** ASR-001's purpose statement and "Missing Stories" section are as clean an example of capability-first framing as exists in this corpus — the assessment explicitly checked delivered state against story status before scoping the sprint.
- **What would prove the d4-14 finding wrong:** if the ~20 files in the d4-14 Dev Agent Record's File List were found merged into the real `nornspun-backend` repo (any branch, any commit, any date) with matching content, or if `test_session_loop_full_cycle.py` were found anywhere reachable. I checked `git log --all`, all branches (`main`, 5 story branches, 2 sprint branches), and `git fsck --unreachable --no-reflogs` in the real backend repo — all came back negative. I also checked the planning-hub repo's own deletion commit (`dbc8615`) to confirm the deleted Tree B file list matches the d4-14 story's claimed File List — it does, file-for-file (`src/agents/verdandi.py`, `src/core/dependencies.py`, `tests/integration/test_session_loop_full_cycle.py`, etc., all present in the `dbc8615` deletion diff).
- **What would prove the "retro audits the wrong sprint" finding wrong:** if any of the 10 story slugs appeared as substantive dev-work content (not incidental mentions) in `audit-extracts/*.jsonl`. I ran exact-string `grep -c` for all 10 slugs plus loosened keyword variants (`campaign-id`, `Spinner`, `campaign_id`, `Wire Campaign`, `Begin with Urd`, `dev-frontend`) — the only matches were incidental (a priority-evaluation fan-out mentioning `fix-skuld-pip-touch-target` by name while rating it, and an unrelated git-rename error touching a `norn-switch...feature` filename during the taxonomy migration).
- **A limitation I could not resolve:** whether the d4-14 dev agent's work was genuinely lost (written to Tree B, never reconciled, then deleted) versus partially fabricated in its own Completion Notes without ever writing working code at all. Both explanations are consistent with the evidence (no trace in either tree's *current* reachable history for the actual test content, since Tree B's blob content is gone with the `git rm -r` and I did not attempt a deep object-hash archaeology of Tree B's now-removed blobs). Either way the observable outcome for a user is identical: the acceptance criteria were never met against the real system.

## Open questions

- Whether the d4-14 dev agent's session (its own transcript, not the mis-filed retro audit) still exists anywhere and would show the exact moment it resolved to the wrong directory — outside the scope of the raw transcripts available (all April/May raw transcripts are gone; only `audit-extracts/` survives, and it does not cover this story per §3).
- Whether any other sprint from this same era (before `momentum:conductor` and before the Tree A/Tree B fix on 2026-05-29) has a similar silently-lost story hiding in Tree B — ASR-003 lists ~17 "done" backend stories that were provisionally flagged suspect and then cleared against Tree A, but that clearance predates my specific d4-14 finding and did not check for the inverse failure (real Tree A prerequisite work, but a *later* story's own deliverable landing only in Tree B). This dossier is scoped to sprint-2026-04-08 only; a cross-sprint sweep for the same failure mode is out of scope here.
- The exact content of the pre-2026-04-26 ASR-001 assessment beyond the four sections quoted (I read it via `git show` at its original commit `7b2439d` in the `nornspun` repo before it was later moved to a sibling `nornspun-community` repo I do not have access to; I did not attempt to retrieve any post-move revisions).
