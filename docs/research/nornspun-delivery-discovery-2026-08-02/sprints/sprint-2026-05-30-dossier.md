# Sprint Dossier — sprint-2026-05-30 ("Campaign-Init Iteration 2")

**Date compiled:** 2026-08-02
**Role:** Evidence dossier for one sprint, produced as part of the nornspun delivery-discovery investigation (why sprint-2026-07-13 shipped 12/12 stories with end-gate approval yet the app "couldn't do even the simplest things"). This document covers sprint-2026-05-30 only.

---

## Executive summary

1. **This sprint is a documented, on-the-record instance of the exact failure pattern under investigation — and it happened *inside* the sprint, not just at the end.** All 15 planned stories passed per-story QA, adversarial code review, and directed fix; all 15 merged across 5 waves. The end-gate report then states plainly: campaign-init "does not function end-to-end: conversation is client-local hardcoded copy, backend prompt work unreachable." (`.momentum/conduct/endgate-report.html`, Decision A; `build-ledger.json:phase4_live.wiring_6_conclusive`)
2. **The root cause is a named, deliberate process choice, not an accident.** The sprint's own runbook states per-story QA was "structured observation of the diff against the .feature scenarios" (i.e., reading the diff, not running the app) and explicitly deferred real execution to a single later live pass: "the real UI execution is the live collaborative Scenario-A walkthrough in Phase 4 — not 11 brittle Maestro flows." (`.momentum/conduct/RUNBOOK.md:149`)
3. **The safety net worked this one time, at a cost of doubling the work.** Phase-4 live driving caught the disconnect before final merge; the developer chose "request-changes" over "accept as-is," and a 5-story, unplanned "CR-wave" (SSE rewire, deterministic PF2e default, phantom-campaign guards, switcher binding, cosmetics) plus a 5-bug live-QA fix loop had to be built same-day (2026-06-11) before a second end-gate approved. (`build-ledger.json:cr_wave`, `endgate.verdict_final: "APPROVED"`)
4. **The intent was framed as a user capability, correctly and explicitly, before the sprint started.** The pre-sprint assessment (ASR-004, 2026-05-29) named a live blocker in plain terms: "a GM types their campaign name, hits send, and nothing happens... they're silently stuck at the very first step." (`docs/assessments/asr-004-campaign-init-completion-audit-2026-05-29.md`, quoted verbatim in `story-review.html`)
5. **The process-level fix for the root cause was captured but never implemented.** A backlog story (`conduct-round-build-smoke-qa-leg`, created 2026-06-10 from this sprint's root-cause analysis) proposes making per-story QA actually build/launch/drive smoke-tagged stories instead of diffing. As of 2026-08-02 (two months and at least two more sprints later) it is still `status: backlog`, never enriched or built.
6. **Four other held findings from this sprint's end-gate are also still unresolved in backlog**, including a confirmed test-harness defect ("3 of 4 backend `.smoke.sh` harnesses... assertions unreachable") that means Scenario B (the backend contract check) never actually ran clean during this sprint, and a confirmed model-reliability gap (name-only PF2e defaulting failed 3/3 live runs on the deployed model) whose recommended model-evaluation follow-up never ran.
7. **The sprint's retro was never run** (`retro_run_at: null` in `.momentum/sprints/index.json`) despite the sprint being locked `status: done`. No `sprint-summary.md`, no `retro-transcript-audit.md`, no `audit-extracts/` exist for it — the only reason this sprint's story is fully reconstructable at all is that `.momentum/conduct/` still held its (un-superseded) `RUNBOOK.md`, `build-ledger.json`, and `endgate-report.html` artifacts, plus git history in both app repos.
8. **All 20 stories (15 planned + 5 CR-wave) remain `status: done` today** with no evidence of reversion; the campaign-init screen/viewmodel files show no further code changes between 2026-06-12 and 2026-07-25 other than an unrelated composer redesign. Whatever shipped appears to have held.
9. **A later assessment (ASR-006, 2026-06-16 — 4 days after this sprint closed) independently confirms collateral damage from the mid-sprint pivot**: "campaign-init's wizard stories are marked done but their canvas files are absent (build artifacts confirm they were built then deleted in the SDR-011 realignment)" — i.e., the master feature tracker (`features.json`) still shows stale, partly-fictional status for this feature area, unrelated to whether the user-facing flow works.
10. **This sprint is evidence *for* the mission hypothesis but with an important qualifier**: the failure mode (stories individually verified, integration never exercised) is real and reproduced here — but this sprint also shows the practice *catching* it (Phase 4) before shipping, unlike the sprint-2026-07-13 pattern the mission is centrally investigating. The open question for the broader investigation is why the Phase-4 backstop that worked here either didn't exist, wasn't run, or didn't catch the equivalent problem in 07-13.

---

## 1. INTENT — what was this sprint for?

**Stated as a user capability, not a task list.** The sprint's own plan-gate document title is *"Sprint sprint-2026-05-30 — Campaign-Init Iter-2 (re-grounded)"* (`.momentum/sprints/sprint-2026-05-30/story-review.html`, `<title>`), and its very first story is framed around a broken user moment, not a technical task:

> "Right now a GM types their campaign name, hits send, and nothing happens — the campaign is never created, so they're silently stuck at the very first step on both Android and Desktop. This is the threshold moment of the whole app, and it's broken."
> — `story-review.html`, story 1 ("Fix campaign creation port mismatch so name-entry actually opens the campaign")

This framing traces directly to the pre-sprint discovery assessment, **ASR-004** (`docs/assessments/asr-004-campaign-init-completion-audit-2026-05-29.md`, dated the day before planning), which was explicitly commissioned to answer three questions before committing scope, the second and third stated as user-observable questions:

> "Does Campaign Init **look** and **work** like the design we captured...? Do we have **enough stories** to get campaign-init to **COMPLETE** in this iteration?"

ASR-004's headline verdict table records: *"Looks / works as designed? **No / No** (static evidence). **A live running-app pass is required** to be sure, and a hard blocker (POST `/campaigns` 404) means campaign creation silently fails today."* — i.e., the intent-setting document *itself* flagged, before the sprint began, that static/per-story verification would be insufficient and a live pass was required. That warning proved prescient (see §3, §5).

The coverage-plan.md's framing is consistent: 15 stories are explicitly treated "as facets of one feature — the campaign-init flow" discharged through two integration scenarios (a client walkthrough and a backend contract run), not as 15 independent checks (`.momentum/sprints/sprint-2026-05-30/coverage-plan.md`).

**Verdict on Q1: user-capability framed, correctly, at both the assessment and story level.** This is not a sprint where the intent itself was mis-stated as tasks/infrastructure — the framing was right. The gap that emerged (§3) was in execution/verification, not intent.

---

## 2. PLAN — stories, waves, team, product-vs-process split

**15 stories, 5 dependency waves**, split across two repos (`.momentum/sprints/index.json`, sprint object with `slug: "sprint-2026-05-30"`):

| Wave | Stories |
|---|---|
| 1 | `remove-5-phase-wizard-from-campaign-init-screen`, `backend-campaign-init-realign-drop-campaign-type-remove-binding-gate`, `fix-post-campaigns-404-campaign-creation-endpoint-missing-or` |
| 2 | `campaign-init-threshold-opening-message-and-system-choice-links`, `backend-campaign-init-add-offered-suggestion-list-copy`, `swap-campaign-switcher-from-no-campaign-on-name-capture`, `apply-horizontal-padding-to-conversation-surface` |
| 3 | `campaign-init-offered-suggestion-list-render-and-routes`, `campaign-init-urd-fills-canvas-from-free-text`, `fix-campaign-switcher-title-bar-truncation` |
| 4 | `campaign-init-hide-pre-init-urd-messages`, `urd-conversational-flavor-turn-before-flavorcanvas-opens`, `strip-trailing-punctuation-from-offered-list-items` |
| 5 | `fix-campaign-name-title-bar-body-font-with-caret`, `apply-type-bold-term-weight-to-readback-committed-values` |

**Product-capability vs. process/infra split:** by count, essentially all 15 are product-capability stories aimed at one user journey (campaign creation via conversation with Urd) — there is no pure test-infra or tooling story in the original 15. Verification method breakdown from `sprints/index.json`'s assignment block: 10 stories `change_type: app-ui` (`verification_method: smoke-ui`), 4 `change_type: backend` (`verification_method: bash`, i.e. `.smoke.sh` contracts), 1 `change_type: app-ui-cross-repo` (`verification_method: observation`). This is the anti-redundancy design the coverage-plan describes: 11 client stories collapse into "Scenario A" (one client walkthrough), 4 backend stories collapse into "Scenario B" (one backend contract run) — 0 dedicated-run stories, "every story appears exactly once."

**Team/build engine:** this sprint predates the released `/momentum:conductor` skill. It was built via a **hand-conducted analog**, documented in `.momentum/conduct/RUNBOOK.md`: *"A plan to build the active sprint... the way the unreleased `/momentum:conduct` skill will work — by acting as the conduct engine ourselves, in-session, driving dynamic Workflows — instead of using the current `/momentum:sprint-dev`."* Five custom Workflow scripts implemented the phases (`.momentum/conduct/workflows/nornspun-round-build.wf.js`, `nornspun-avfl-merge.wf.js`, `nornspun-e2e-consolidation.wf.js`, `nornspun-contract-freeze.wf.js`, `nornspun-endgate-render.wf.js`). The runbook states the same per-story pipeline conduct later formalized: dev → QA ∥ adversarial code-review → directed fix → Conductor merge.

**Plan-gate approvals:** all 15 stories show `decision: "approved"` in `sprints/index.json`, all timestamped identically `2026-06-02T20:33:1[6-7]Z` (a single batch approval event, not sequential per-story review). `story-review.html`'s "Decisions that need you" section for this gate reads: *"None outstanding — the picker, item-2 route, and flavor-canvas calls are settled. Everything below follows the authoritative hi-fi + our standards."* — i.e., zero open forks were escalated to the developer at plan time; the plan was fully defaulted to standards.

**Timeline:** `planned: 2026-05-30`, `started: 2026-06-02`, `completed: 2026-06-12` (12 calendar days, but the 3-day gap between planned and started plus a mid-sprint gap 06-13→06-16 in the git log suggest the actual wall-clock build activity clustered 06-07/06-08 (waves 1–5 merges) and 06-11 (CR-wave + final merge) — a compressed, not continuous, build.

---

## 3. EXECUTION — what happened during the build

**Per-story pipeline ran as designed and caught real defects.** The end-gate report (`.momentum/conduct/endgate-report.html`, §3 "How the build ran") states: *"Real defects caught & fixed by the adversarial layer: a `drop(-1)` recomposition crash hazard; the readback name being italic not bold; an AC6 a11y label clobber; offered-list descriptors never rendering visibly."* It also records three self-repairs of the (new) conduct scripts themselves (a wrong reviewer agent-type, an empty diff-range, and a fixer-failure that had masqueraded as success) and one content-filter fixer crash that required a re-fix out-of-band.

**Wave merges (backend, `nornspun-backend` git log, all commits present and inspected directly):**
```
58c4e33  2026-06-07  merge(sprint): backend campaign-init realign — drop campaign_type + binding gate (wave 1)
e5a996b  2026-06-07  merge(sprint): backend campaign-init add offered-suggestion-list copy (wave 2)
95731ed  2026-06-08  merge(sprint): urd fills name+system from free text (wave 3)
0ea76ae  2026-06-08  merge(sprint): urd conversational flavor turn before flavorcanvas (wave 4)
e12e13e  2026-06-08  merge(sprint): type-bold campaign-name readback (wave 5, cross-repo)
```
**Wave merges (client, `nornspun-client` git log):** 15 corresponding `merge(sprint):` commits 2026-06-07/06-08, e.g. `b48b196 merge(sprint): fix-post-campaigns-404 client port fix (wave 1)`, `89354eb merge(sprint): remove-5-phase-wizard-from-campaign-init-screen (wave 1)`, through `6af5f7e merge(sprint): campaign-name title-bar body font + caret (wave 5)`.

**The critical divergence — AVFL flagged it, Phase 4 confirmed it.** The post-merge AVFL integration scan (read-only, automated) already surfaced the architecture problem before any human drove the app: `build-ledger.json:avfl.findings_architectural` records finding **#6**, severity high: *"client campaign-init CONVERSATION appears client-local: `captureName()` sets state + renders a HARDCODED offered list; flow does not round-trip Urd's responses via the backend chat contract... ARCHITECTURE QUESTION FOR STEVE; validate live in Phase 4."* AVFL's own auto-fix attempt was **discarded**: *"fixer regressed the voice register ('I have it.' which realign removed); held findings for end-gate instead."* (`avfl.fix`)

Phase 4 (the live collaborative walkthrough on Desktop + Android, backend on :8000) then **conclusively confirmed** it:
> `build-ledger.json:phase4_live.wiring_6_conclusive`: "hybrid: creation=backend (POST /api/campaigns, fire-and-forget UUID on first-launch), conversation=100% client-local hardcoded copy. Urd SSE chat NEVER called in campaign-init. Client code labels F3_*/offered-list copy 'fallback ... used when backend payload unavailable'."

The end-gate report's own headline names the mechanism plainly: *"But Phase-4 validation found the two halves are not wired together: the campaign-init conversation renders from client-local hardcoded copy and never calls the backend Urd chat — so the backend prompt work this sprint did is not (yet) what the user sees."*

**Why per-story QA didn't catch it — stated as policy, not discovered as a bug.** `.momentum/conduct/RUNBOOK.md:149` (written *before* the build, as part of the plan): *"D-A · App-UI verification = Gherkin-as-frozen-contract + live observation. Freeze each `.feature`'s SHA as its contract; per-story QA verifies app-ui by structured observation of the diff against the `.feature` scenarios (honest inspection-vs-execution at the end-gate). The real UI execution is the live collaborative Scenario-A walkthrough in Phase 4 — not 11 brittle Maestro flows."* This is an explicit, named trade-off (labeled honestly as "inspection-vs-execution"), not a silent gap — but it is exactly the trade-off that let 11 client stories individually "pass" while the assembled feature didn't work.

**Same failure class had been flagged before this sprint and recurred anyway.** ASR-004's own "Prior-sprint lessons" section (written 2026-05-29, one day before planning) already warned: *"Client interaction flows are invisible to API-level E2E (04-06: 57/71 scenarios passed yet norn-switching did nothing live)"* and *"The visual/E2E validator rubber-stamped real defects... Iter-2 E2E must observe live... not scenario pass counts."* The warning was heeded at the Phase-4 design level (a live walkthrough was scheduled and did run) but not at the per-story level (11 stories still passed on diff-only review) — the same underlying pattern (story-level pass, integration-level failure) reproduced inside a sprint that had explicitly been warned about it.

**Remediation ("CR-wave") — same day, 2026-06-11, before final merge:** The developer's decision, recorded in `build-ledger.json:endgate.verdict` = `"request-changes"`, triggered 5 new stories (not part of the original 15, created ad hoc and later formally filed to `.momentum/stories/`):

| Story | Repo | Commit | Result |
|---|---|---|---|
| `default-system-pf2e-server-side` | backend | `96ef418` | done — tool-layer default; 11 new tests |
| `urd-greeting-guard-no-phantom-campaigns` | backend | `eb42a84` | done — deterministic no-fabrication guards; 20 new tests |
| `backend-campaign-init-emit-campaign-created-event` | backend | `ac1e34b` | done — `campaign.created` SSE event; suite 742 passed |
| `client-campaign-init-conversation-over-sse` | client | `357a2cc` | done — composer now sends live SSE; `createCampaignOnFirstLaunch` and the hardcoded `F3_*` constants **removed** |
| `bind-title-bar-switcher-to-active-campaign` | client | `90616c6` | done |
| `campaign-init-cosmetic-fidelity-batch` | client | `a6dcd27` | done |

The CR story files themselves state the contract was frozen the same day as a formal "Campaign-Init Chat Contract (CR-2026-06-11)" duplicated verbatim in both the backend and client story specs (`.momentum/stories/client-campaign-init-conversation-over-sse.md`, `.momentum/stories/backend-campaign-init-emit-campaign-created-event.md`).

**On top of the CR-wave, a live-QA fix loop found 5 more defects while driving the rewired flow** (`build-ledger.json:cr_wave.live_qa_fix_loop`), including a **high-severity** one only reachable by actually using the app: *"campaign-init had NO scroll surface — threshold+F3 fixed blocks filled phone viewport, conversation clipped invisible, composer overlapped list"* (`6b3901d`), and a **high-severity crash**: *"Retry after streaming timeout crashed app: content-derived LazyColumn key collided when retry re-added the user turn"* (`7451c84`).

---

## 4. CLAIM — what the sprint claimed at completion

There is no `sprint-summary.md` for this sprint (unlike later sprints). The authoritative completion claim is the **end-gate report** (`.momentum/conduct/endgate-report.html`) and its structured twin `.momentum/conduct/build-ledger.json`. Its headline, quoted in full because it is unusually candid for a "done" sprint:

> "All 15 stories built, verified, and merged to the sprint branches (nornspun-client +32 commits, nornspun-backend +15). The client campaign-init UI is hi-fi-accurate (every wave's design direction-guard passed) and the backend realign + Urd-prompt work is done. **But Phase-4 validation found the two halves are not wired together**: the campaign-init conversation renders from client-local hardcoded copy and never calls the backend Urd chat — so the backend prompt work this sprint did is not (yet) what the user sees. That is Decision A below, and it is the crux of this gate."

Stat line from the same report: *"15/15 stories built & merged · 5 waves, 0 stories dropped or stuck · 3/3 direction-guards sound · 11 items held for this gate (3 decisions + cosmetics)."*

The gate presented the developer three explicit decisions (A: wire now / follow-up / accept-as-is; B: PF2e default now / follow-up; C: harness rewrite now / follow-up), plus 5 cosmetic items. Recorded resolution (`build-ledger.json:endgate`):
```
"verdict": "request-changes",
"rationale": "UI is hi-fi-accurate but campaign-init does not function end-to-end...",
"change_set": [5 CR-wave stories — wire now, chosen],
"intaken_for_future": [4 stories — deferred to backlog],
"verdict_final": "APPROVED",
"approved_date": "2026-06-11",
"merged_to_main": {"nornspun-client": "ca3db72", "nornspun-backend": "58e001b"}
```
i.e., the developer chose **"wire it now"** for Decision A and B, deferred Decision C (harness rewrite) and the cosmetics/model-follow-up to backlog, and only then approved the final merge. The final merge commit messages self-document this: `58e001b merge(sprint): sprint-2026-05-30 — campaign-init backend + CR wave (end-gate approved 2026-06-11)` and `ca3db72 merge(sprint): sprint-2026-05-30 — campaign-init iteration 2 + CR wave (end-gate approved 2026-06-11)`.

**No formal retro was ever run.** `.momentum/sprints/index.json`'s sprint object shows `"retro_run_at": null` despite `"locked": true, "status": "done"`. Confirmed absent: `.momentum/sprints/sprint-2026-05-30/` contains only `contract-freeze-baseline.sha256`, `coverage-plan.md`, `specs/`, `story-review.html` — no `sprint-summary.md`, no `retro-transcript-audit.md`, no `audit-extracts/`, no `build-ledger.jsonl` (the sprint-local build ledger convention used by later sprints). Every ledger/report artifact used in this dossier's §3/§4 came instead from the *shared, non-sprint-namespaced* `.momentum/conduct/` directory (`RUNBOOK.md`, `build-ledger.json`, `endgate-report.html`), which happens to still hold sprint-2026-05-30's content because no later sprint using the same hand-conducted mechanism has overwritten it. This is fragile: had a subsequent hand-conducted sprint reused those same three filenames, this sprint's execution record would likely be gone (see Open Questions).

---

## 5. REALITY — what actually landed

**Both repos, full commit trail verified directly via `git log`.** Backend: 19 commits in the window, ending `58e001b` (2026-06-11), the final sprint merge. Client: matching wave-by-wave merges ending `ca3db72` (2026-06-11). Story-index cross-check: all 15 original stories plus all 5 CR-wave stories show `status: "done"` in `.momentum/stories/index.json` as of 2026-08-02 — no drops, no reversions detected in the index.

**Did the landed code change what a user could do?** Yes, but only after the CR-wave, and the change was larger than the original 15-story plan implied:
- **Before this sprint:** per ASR-004 (2026-05-29), campaign creation was silently broken (`POST /campaigns` 404) and the live UI was still the pre-SDR-011 5-phase wizard.
- **After waves 1–5 (2026-06-08), before the CR-wave:** the 404 was fixed and the UI was rebuilt hi-fi-accurate, but the "conversation" was 100% client-side scripted text; the backend was never called for anything except the initial fire-and-forget creation POST. A user could create a campaign (the original blocker was gone) but could not have an actual conversation with Urd during campaign-init — Urd's prompt/copy work shipped this sprint had no path to the user.
- **After the CR-wave (2026-06-11):** campaign creation and the entire campaign-init conversation route through the real backend Urd SSE chat stream; `createCampaignOnFirstLaunch` and the hardcoded Frame-3 copy were deleted outright (not just deprecated) — the client cannot silently fall back to the fake path because the fake path's code was removed.

**Stability since:** `git log` on `CampaignInitScreen.kt` / `CampaignInitViewModel.kt` in `nornspun-client` shows no further commits between 2026-06-12 and 2026-07-25 other than an unrelated composer-redesign commit — i.e., no evidence the CR-wave fix was itself reverted or reworked in the two sprints that followed (06-18, and the run-up to 07-13).

**Cross-check against a later independent assessment.** ASR-006 (2026-06-16, produced 4 days after this sprint closed, "AVFL full-profile pass complete — 8 reviewers... corrected findings") treats the SSE-driven conversational core as pre-existing, working infrastructure for the *next* sprint to build on top of: *"ALREADY DONE — DO NOT REBUILD: Campaign-init's conversational core works: the client consumes the `campaign.created` SSE event... Backend campaign model/migrations/agent are done; the binding gate is removed."* (quoted from session transcript `f076e3f7-368b-4a28-8b02-915e83736ad7.jsonl`, lines ~4416/4443, itself summarizing/citing the live repo state consistent with ASR-006's F1/F2 findings). This is independent corroboration that the CR-wave fix held.

**Collateral finding from the same later assessment (ASR-006, F3):** the master feature tracker was not updated to reflect any of this — *"campaign-init's wizard stories are marked done but their canvas files are absent (build artifacts confirm they were built then deleted in the SDR-011 realignment)"* and *"The real campaign-init corpus is ~22 stories, not the 10 in `features.json`."* `.momentum/features.json`'s `campaign-init` entry today still lists a stale 10-story roster (none of which are the 20 stories this sprint actually built) with `"last_verified": "2026-06-16"` and internal notes acknowledging the mismatch. This doesn't affect whether the user-facing flow works, but it means the practice's own system-of-record for "is this feature done" was already unreliable immediately after this sprint.

---

## 6. AFTERMATH — did anything get dropped, reverted, or left unresolved?

**No story reversions.** All 20 stories tied to this sprint (15 original + 5 CR-wave) remain `status: done`. No evidence found of drop/obsolete/revert for any of them (checked via `.momentum/stories/index.json` status field and via absence of any later commit touching the same files that would indicate a revert).

**But 5 held findings from this sprint's own end-gate remain unresolved backlog stubs, two months later:**

| Backlog story | Status | What it fixes | Why it matters |
|---|---|---|---|
| `conduct-round-build-smoke-qa-leg` | backlog (never enriched) | Makes per-story QA for `verification_method: smoke` stories actually build+launch+drive, instead of diff-review, for the *next* nornspun-local sprint | This is the direct structural fix for the root cause of this sprint's own failure (§3). Its own description says: "the consolidation sprint (BLOCKER priority) runs on this same [unfixed] workflow next." Created 2026-06-10 from this sprint's root-cause analysis; still backlog as of 2026-08-02. |
| `rewrite-backend-smoke-harnesses-temp-file-capture` | backlog | Rewrites 3-of-4 backend `.smoke.sh` contracts that CONFIRMED never execute their assertions (stdin-collision bug) | Means the backend "Scenario B" integration contract for this feature has never actually run clean, then or since. |
| `raise-android-bodylarge-token-15-to-16sp` | backlog | Android body-text token is 1sp off hi-fi spec, flagged "WIDE BLAST RADIUS" (affects every Android body-text surface) | Deliberately NOT folded into the CR cosmetic batch because of that blast radius — needs a dedicated visual-regression pass that never happened. |
| `first-launch-cta-design-gap-designmd-entry` | backlog | Resolves a real design-authority contradiction (DESIGN.md says "sharp 4dp," both live builds + the HTML prototype use a full pill) | Explicitly needs a design decision from the developer, not just a code fix; still open. |
| `route-urd-extraction-to-stronger-model` | backlog | Follow-up on the CONFIRMED model-reliability gap: the deployed model failed AC3 (name-only PF2e default) 3 of 3 live runs, worked around with deterministic server-side backstops rather than fixed at the model layer | The workaround (tool-layer PF2e default, phantom-campaign guards) shipped and likely masks the underlying model unreliability rather than resolving it. |

**No retro was run**, so none of this held-findings backlog was ever synthesized into a findings digest or cross-sprint pattern report through the normal retro mechanism — it survives only because the CR-wave stories and the four intake-queue entries happened to be filed as individual backlog stubs (`.momentum/practice-ledger.jsonl` entries `pl-20260611T...` tagged `"origin": "sprint-2026-05-30 endgate"`) rather than lost.

**No later assessment or decision references this sprint's held findings as a pattern to fix at the process level**, other than the single backlog stub above. The upstream momentum-level equivalent it names (`conduct-qa-execute-verification-method`, in the momentum repo, not nornspun) is out of scope for this dossier but is the more general version of the same fix.

---

## 7. VERDICT

**"After sprint-2026-05-30, a user could complete campaign creation and have an actual Urd-driven conversation during campaign-init (name capture, system choice, and the next-steps offer), which they could not do before — but only counting the CR-wave that landed the same day as the original end-gate, not the 15-story plan as originally scoped."**

Qualifications required for this verdict to be strictly honest:
- If "this sprint" means only the 15 originally-planned, originally-approved stories (waves 1–5, merged 2026-06-07/06-08), the verdict does **not** hold: those 15 stories, taken alone, shipped a UI that looked right and a backend that was individually correct, but the two were not connected — a user would have seen a fully scripted, non-functional-feeling "conversation" with no actual agent behind it, confirmed both by an automated AVFL pass and a live human walkthrough.
- The verdict **does** hold once the same-day CR-wave (5 additional, unplanned stories) is included, because that is what actually shipped to `main` under this sprint's merge commits (`58e001b`, `ca3db72`) before the developer approved.
- The verdict is narrower than "campaign-init is complete": a confirmed backend contract-verification gap (3 of 4 `.smoke.sh` harnesses never execute their assertions) and a confirmed model-reliability gap (PF2e-default failed 3/3 on the deployed model, backstopped rather than fixed) remain open and unaddressed two months later.

---

## Counter-evidence & falsifiability

Evidence that cuts against treating this sprint as a clean instance of "stories pass, functionality fails, and nobody notices":

- **The practice's own tooling caught the problem twice, independently, before shipping**: once via the automated AVFL post-merge scan (finding #6, "ARCHITECTURE QUESTION FOR STEVE; validate live in Phase 4") and once via the scheduled Phase-4 live walkthrough. This is not a sprint where broken functionality slipped through to the developer's own later manual discovery (as the mission context describes for sprint-2026-07-13) — it was caught *inside* the sprint's own gate, before "done" was declared to the developer as final.
- **The developer actively chose the harder, correct remediation** ("wire it now") over the easier options offered ("follow-up story" or "accept as-is") — the process gave a real choice and the harder path was taken.
- **The root-cause trade-off was a named, written-down decision at plan time** (`RUNBOOK.md:149`, "D-A"), not a silent process failure discovered after the fact — the plan's authors were aware per-story QA would not execute the app and explicitly scheduled a later live pass to compensate. That compensating control worked as designed on this occasion.
- **What would prove this dossier's framing wrong:** if the "CR-wave" and "live-QA fix loop" commits were found to have been reverted or bypassed by a later sprint (no evidence of this was found — see §5); or if `conduct-round-build-smoke-qa-leg`'s premise ("the consolidation sprint runs on this same [unfixed] workflow next") turned out to be moot because nornspun's actual next sprints stopped using the hand-conducted workflow and instead used a version of `/momentum:conductor` that already executes smoke stories for real (not verified in this dossier — see Open Questions).

## Open questions

1. **Did `/momentum:conductor`'s real (non-hand-conducted) implementation, once released, actually execute `verification_method: smoke` stories for real (build+launch+drive) rather than diff-review, making `conduct-round-build-smoke-qa-leg` moot for sprints after this one?** Not checked in this dossier — would require reading the conductor skill's QA-stage implementation and/or a later sprint's build-ledger for evidence of live execution per smoke story. If the fix never landed even upstream, that directly connects this sprint's root cause to the 07-13 pattern the broader mission investigates.
2. **Was the backend `.smoke.sh` harness bug (3 of 4 contracts confirmed non-executing) ever fixed in a later sprint, under a different story slug, without closing this specific backlog stub?** Not checked; the stub itself is still open, but it's possible the harnesses were replaced wholesale by later work without formally resolving this ticket.
3. **Exact wall-clock duration and headcount of the build is not fully reconstructable.** No session transcript covers the actual dev/QA/merge work (git commit timestamps 2026-06-07 through 2026-06-11 are the only timing evidence; the one available session transcript from this window, `f076e3f7-...jsonl`, is a concurrent-but-separate UX-audit conversation, not the build itself — the build ran via tool calls not captured in that JSONL, likely visible only in an ephemeral cmux services pane per the user's own layout convention).
4. **Why was this specific sprint's retro skipped**, given every other locked/done sprint in `sprints/index.json` (that this dossier sampled) has a non-null `retro_run_at`? No decision record, ledger entry, or handoff was found explaining the omission — it is treated here as an observed fact, not an explained one.
5. **Fragility of the evidence base itself**: this dossier depends on `.momentum/conduct/{RUNBOOK.md,build-ledger.json,endgate-report.html}` never having been overwritten by a later hand-conducted sprint. Their file mtimes (2026-07-13 10:55, same as many sprint-2026-07-13 artifacts) suggest a git-checkout side effect rather than original authorship, but their *content* is unambiguously sprint-2026-05-30-specific throughout. Confirm this doesn't indicate silent overwriting/loss of an intermediate sprint's equivalent artifacts if this method is reused for other dossiers in this investigation.
