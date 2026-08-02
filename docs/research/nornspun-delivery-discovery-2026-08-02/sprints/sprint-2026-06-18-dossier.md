# Sprint Dossier — sprint-2026-06-18 ("App Shell + Campaign Picker")

**Date compiled:** 2026-08-02
**Role:** Evidence dossier for one sprint, part of the nornspun delivery-discovery investigation into whether Momentum sprints deliver user capability or only story-shaped completion.

---

## Executive Summary

1. **This sprint is the strongest counter-example to the "stories ship, capability doesn't" hypothesis found so far**: it shipped a genuinely new, live-verified user capability — a campaign picker (create a campaign conversationally, see all campaigns newest-first, switch back to the picker) — replacing a hard-wired single-chat entry with no picker at all. The end-gate report's own before/after framing is user-capability language, not task language, and the "create new campaign" path was verified end-to-end against the real backend and a real LLM on a live Android emulator (`.momentum/handoffs/sprint-2026-06-18-endgate-report.html`, §01, §07).
2. **But the other half of the multi-campaign capability — resuming an existing campaign — shipped broken, was caught live at end-gate, was honestly disclosed, and remains unfixed 3+ weeks later.** Tapping an existing campaign's card updates the title bar and Norn pips but does **not** load that campaign's conversation; the underlying session is not scoped by campaign at all (one `session_id` was shared across a live campaign switch, confirmed by the Conductor's own repro). This was found in E2E, presented as end-gate Decision D2, and the developer chose "Accept — promote to Sprint-2 top priority" (endgate report, "D2 · Opening an existing campaign doesn't actually switch the conversation to it").
3. **The "Sprint-2 top priority" promise was only half-kept, and slowly.** The intake stub (`iq-2026070905565505-0bbefdab`, filed 2026-07-09) asked for four things: (a) backend session model keyed by campaign, (b) client cache keyed by (campaign, Norn), (c) wire existing-campaign seating to load history, (d) inject campaign name not UUID into prompts. Only (d) — the cosmetic half — landed, and not until **2026-07-30** (`nornspun-backend` commit `ab2e579`), three weeks after the promise and a week after the "Sprint-2" sprint (2026-07-13) closed. The architectural story `backend-session-model-keyed-by-campaign` remains **status: backlog** as of 2026-08-02 (`.momentum/stories/index.json`), and the client's `nornConversationCache` is still keyed by `ActiveNorn` only, not by campaign (`nornspun-client/composeApp/src/androidMain/kotlin/com/nornspun/ui/viewmodel/ChatViewModel.kt:219`, verified live at HEAD `704e63c`).
4. **Of the 8 stories, only 2 built genuinely new user-observable capability** (the campaign picker screen S6, and the switcher-to-picker navigation S2); the other 6 were chrome/cosmetic work — a shared title-bar extraction (prerequisite refactor), title-bar variant rendering, a composer visual redesign, a Norn-pip visual redesign, a CTA color-token fix, and hardcoding light theme. All 8 are legitimate `app-ui` deliverables and all 8 shipped and remain `status: done` with no later reversal — but 6 of 8 do not, by themselves, let a user do anything new.
5. **Execution was clean by pipeline standards**: 7 of 9 audited work-items converged in a single dev→review→fix→merge cycle; the retro's own count is 41 KEEP findings vs. 32 FIX/INVESTIGATE findings across 73 verified findings. The sprint's dominant defect (a **desktop-test false-green**: `desktopApp/build.gradle.kts` used `useJUnitPlatform()` without `junit-vintage-engine`, so ~29/31 `kotlin.test` files silently never ran while CI reported green) was independently rediscovered in 5 of 9 stories and had already been flagged as a dedup stub on 2026-06-12 — six days *before* this sprint started — yet wasn't fixed until the *next* sprint's wave-1 gatekeeper story, which itself is still `status: review` as of 2026-08-02.
6. **AVFL (diff-level) and E2E (live-app) validation disagreed**: AVFL marked the campaign-picker session-load defect fixed at iteration 4; live E2E on a real Android emulator re-found it. This is a direct, first-hand instance of the exact validator/live-app gap this whole investigation is probing, documented in the sprint's own retro (`retro-transcript-audit.md` line 10, 33).
7. **The end-gate presentation for this sprint was honest and well-instrumented** — it explicitly disclosed two "still hollow" items (existing-campaign seating, and an unreachable settings screen where "the gear renders but deliberately does nothing"), gave the developer a real Approve/Request-changes decision with evidence (screenshots, live LLM transcript, a regression test), and did not claim more than was verified. This is evidence that decision-grade, capability-honest end-gate reporting is achievable in this practice — it happened here, before the sprint-2026-07-13 failure this investigation is centered on.
8. **The settings screen remains entirely unbuilt.** The Zone-A title-bar "settings" variant renders correctly (S8) but no `SettingsScreen.kt` exists anywhere in the client repo as of HEAD `704e63c` (verified by filesystem search) — the gear icon is a dead end for the user.
9. **A near-duplicate story was queued for the following sprint** (`campaign-picker-get-campaigns-client-repo`, sprint-2026-07-13) whose own file opens with a developer-attention flag stating its core deliverable "is already implemented on disk" by this sprint's S6 story — a concrete instance of backlog/planning-artifact drift producing redundant work, caught before execution but evidence that the backlog does not reliably track what has already shipped.
10. **No sprint-2026-06-18 story was later dropped, obsoleted, or reverted** — all 8 remain `status: done` in `.momentum/stories/index.json` as of 2026-08-02. The sprint's residual gaps are tracked (not silently lost): 13 process-improvement stubs plus the campaign-scoping stub were all filed to the backlog/intake queue with rationale.

---

## 1. INTENT — what was this sprint for?

There is **no `plan-gate-decision.md` for this sprint** — that artifact type appears starting with sprint-2026-07-13; sprint-2026-06-18 predates the formal pre-sprint decision-gate instrument. Intent has to be reconstructed from `coverage-plan.md`, `team-composition.md`, the story specs, and (retrospectively) the end-gate report.

**`coverage-plan.md` framing** (title: "Coverage Plan — sprint-2026-06-18 (App Shell + Campaign Picker)") frames the sprint by component, not by user capability: "This sprint's 8 stories are app-shell chrome that all render inside the same shared title bar... each carries a distinct *observable deliverable* (a specific color, a dark-mode behavior, the composer's three elements, the pip treatments, the settings title-bar variant)." That is component/deliverable language.

**But its one named integration scenario is capability language**: "Scenario A — Create a campaign in the picker and switch back to it... With no campaign selected, the Spinner lands on the campaign picker, taps 'Start a new campaign', creates a campaign with Urd, lands in the workspace with the campaign seated, taps the campaign switcher in the title bar, and is returned to the picker." (`coverage-plan.md` lines 11-14). This is the one place pre-sprint planning states a user-observable journey, not a component list.

**`team-composition.md`** frames the sprint by role/shape: "client-only (Compose Multiplatform). Backend work is zero — `GET /campaigns` already exists." (line 3) — an engineering-shape framing, appropriate for team composition but not capability framing.

**Retrospectively, the end-gate report states intent in capability language**: "Before: the app opened into a single hard-wired chat. The top bar was duplicated per platform, dark mode produced an unreviewed look, the first-launch button was off-spec, Skuld looked available, and there was no way to see or reopen past campaigns. After: the app has a real shell... a campaign picker as the home screen (create conversationally with Urd, see past campaigns newest-first, tap the campaign name anytime to return)." (endgate report §01). This before/after language is exactly the "a GM can X" framing the investigation is looking for, but it appears in the *retrospective claim*, not in the *pre-sprint plan artifact* (which didn't exist in this format yet).

**Verdict on INTENT**: mixed. Pre-sprint planning documents frame the work primarily as component/chrome deliverables with one named user scenario; the sprint's own after-the-fact narrative correctly identifies the capability delivered. The capability framing was present and accurate — it just wasn't the primary framing used to select and scope the stories.

---

## 2. PLAN — stories, waves, team, capability fraction

**Stories (8, all `epic_slug: fantasy-client`, all `change_type: app-ui`, all specialist `dev-frontend`):**

| Slug | Story-file classification | Genuinely new user capability? |
|---|---|---|
| `app-scaffold-shared-title-bar-composable` (S1) | Structural prerequisite — extracts a shared `AppScaffold` composable so Android/Desktop stop drawing separate title bars | No — infra/refactor. Enables consistency; adds nothing a user can newly do. |
| `zone-a-title-bar-variants` (S8) | Title-bar rendering variants (workspace / picker / settings) | No — chrome variant rendering, prerequisite for S6. |
| `composer-redesign-vellum-surface` (S5) | Visual redesign of the message composer (vellum surface, Weave-in link, filled-amber Send, per-Norn placeholder) | No — cosmetic; existing composer, new look. |
| `norn-pip-redesign-glow-scale-inactive-fill-skuld-badge` (S4) | Visual redesign of Norn-selector pips (active glow/scale, inactive tonal fill, Skuld coming-soon ring) | No — cosmetic. |
| `campaign-init-picker-screen-and-start-new-campaign-card` (S6) | **Builds the picker screen from scratch** — real `GET /api/campaigns` list, newest-first, empty state, receipt cards, entry into conversational campaign creation | **Yes** — this is the sprint's one clear new-capability story. |
| `campaign-switcher-tappable-navigation-link` (S2) | Makes the campaign-switcher title-bar element tap-navigate back to the picker | **Yes** — new navigation capability (previously nothing to switch back to). |
| `begin-button-cta-token-fix` (S7) | Color/token fix on the first-launch CTA button | No — visual bug fix. |
| `light-theme-enforcement-mvp` (S9) | Hardcodes `NornTheme(useDarkTheme=false)` regardless of OS setting | No — visual/behavioral constraint, not a new capability (arguably removes a broken behavior — unreviewed dark-mode look — rather than adding one). |

**Fraction:** 2 of 8 stories (25%) build genuinely new user-observable capability. 6 of 8 (75%) are chrome refactor, visual redesign, or bug-fix work on the existing surface. Both capability stories (S6, S2) depended on the prerequisite chrome work (S1, S8), so the chrome work was not wasted — it was load-bearing for the capability stories — but it does not itself constitute capability.

**Waves** (`team-composition.md` + `.momentum/sprints/index.json`):
- Wave 1 (parallel, no deps): S1, S7, S9
- Wave 2 (after S1): S8, S5, S4
- Wave 3 (after S1+S8): S6 — also depends on the out-of-sprint, already-shipped `remove-5-phase-wizard-from-campaign-init-screen` keystone (merged sprint-2026-05-30)
- Wave 4 (after S6): S2

**Team:** single role — `dev-frontend` for all 8 stories, plus sprint-wide QA Reviewer, E2E Validator, and Architect Guard (the latter specifically flagged for S1: "introduces a new structural seam... guard against pattern drift" — `team-composition.md` line 12). No backend role; confirmed zero backend commits in the sprint window (Section 5).

**Merge-conflict hotspots were pre-identified** (not discovered mid-flight): `MainActivity.kt`, `MainWindow.kt`, `AppScaffold.kt` were flagged in advance as touched by 3-5 stories each, with an explicit mitigation plan (S1 reduces the shell first; later edits are "smaller wiring"). This level of pre-sprint conflict analysis is a planning strength, not a gap.

---

## 3. EXECUTION — what happened during the build

**Pipeline shape** confirmed from `nornspun-client` git log (`git log --oneline --since=2026-06-17 --until=2026-07-10`): each story ran `feat → fix (stage-3 auto-fixes) → refactor (simplify cleanup) → merge(story)` before a final `Merge branch 'sprint/sprint-2026-06-18'` (commit `704e63c`) plus two post-merge end-gate fix commits (`8fe99b5`, `876b0c0`) and one pre-existing-main fix (`7ec2149`, an SSE HTTP-timeout bug unrelated to this sprint's stories, absorbed via rebase).

**Metrics** (retro-transcript-audit.md, cross-checked directly against the raw audit-extract files — counts match exactly): 416 user messages, 135 agent summaries, 121 tool errors, 246 inter-agent messages, 73 verified findings (41 KEEP / 32 FIX-or-INVESTIGATE).

**Notable defects surfaced during execution** (from `retro-transcript-audit.md` and `build-ledger.jsonl`, both first-hand build records, not post-hoc reconstruction):

- **Desktop-test false-green.** `desktopApp/build.gradle.kts` calls `useJUnitPlatform()` without the `junit-vintage-engine` runtime dependency, so `kotlin.test`/`org.junit.Test` classes are silently never discovered by Gradle — roughly 29 of 31 desktop test files never ran while the build reported green. Rediscovered independently in S1, S4, S6, S7, S9 (`build-ledger.jsonl` lines 16, 60, 66 among others; `retro-transcript-audit.md` lines 9, 31). This was **already a known, deduped backlog stub as of 2026-06-12** — six days before this sprint started (`.momentum/stories/index.json` → `migrate-desktopapp-tests-from-kotlin-test-to-kotest` → `"consolidated_from": ["desktopapp-test-task-silently-skips-junit-classes"], "dedup_at": "2026-06-12"`) — yet the fix did not land as a story until the *next* sprint (2026-07-13, wave-1 gatekeeper), and that story is itself only `status: review` as of 2026-08-02, not done.
- **AVFL/E2E disagreement on the campaign-picker session-load defect.** AVFL (Kotlin-diff-level validation) marked the defect fixed at iteration 4; live E2E (real Android emulator, real backend) re-found it: "Tapping an existing campaign card correctly updates the title bar and footer... but the conversation itself doesn't load that campaign's session" (`retro-transcript-audit.md` line 33, corroborated verbatim in the end-gate report's D2 section). This is the sprint's most decision-relevant execution finding and directly instantiates the diff-vs-live validation gap this whole investigation is examining.
- **AVFL score regression, not monotonic convergence.** Fix-cycle scores went 53→70→59→89; iteration 3 found a critical seed-campaign/port mismatch (ACC3-001, port 8001 vs 8000) that "16 concurrent validators in waves 1-2 missed" (`retro-transcript-audit.md` line 39).
- **Cross-story coordination cost.** S5's testTag rename (`chat_input`→`composer_text_field`, `send_button`→`composer_send_button`) broke 8-9 Maestro E2E flows and forced a semantic rebase in S6; not caught until a dedicated sweep 1h42m later.
- **Environment contamination during end-gate.** A concurrent session silently reinstalled main-branch builds onto the shared Android emulator and desktop app during the end-gate walkthrough, producing false "picker broken" reports that were traced and refuted with evidence (endgate report, "two wrong-build incidents" passage).
- **Process-level friction**: the developer twice invoked binding presentation rules mid-sprint — once for context-free questions (2026-06-17: "can you please check our rules and determine if we allow you to ask me things that I have no idea about without giving me any context?") and once for a 600-line "machine work-list" handed to them as if it were a review surface (2026-06-24) — both are the exact failure modes the `inline-context.md` and `decision-grade-presentation.md` rules (loaded into this very session) exist to prevent. These generated 2 of the 13 process-improvement backlog stubs.

**No stories were blocked, quarantined, or force-closed.** End-gate report banner: "0 blocked / broken / quarantined."

---

## 4. CLAIM — what did the sprint say it delivered?

`sprint-summary.md`: "8 / 8 planned stories reached done. No stories were force-closed or in progress at retro time." Narrative: "This sprint delivered the app-shell redesign wave end to end... All eight stories shipped and the end-gate was approved on 2026-07-08 after one remediation-candidate pass... The practice takeaway: the build pipeline shipped product reliably, but its verification and reporting layers need the hardening work queued above."

The end-gate report (`.momentum/handoffs/sprint-2026-06-18-endgate-report.html`) makes a **more precise and more honest** claim than the summary alone: it explicitly separates "Live and working now" from "Still hollow" (§06):

> **Live and working now:** "Shared title bar on both platforms; picker-first launch routing; conversational campaign creation against the live LLM (verified end-to-end); campaign list newest-first from the real backend; switcher navigation back to the picker (tap + keyboard); light theme under OS dark mode (verified live); redesigned composer incl. send + document picker; pip treatments incl. Skuld coming-soon; send-failure shows a user-visible error with Retry; full 8-flow automated acceptance suite green."
>
> **Still hollow:** "Opening an existing campaign doesn't carry the conversation with it (Decision D2) — chrome updates, session doesn't. Settings screen doesn't exist — the gear renders but deliberately does nothing (story S3, queued; the title-bar settings mode is built and tested, unreachable). Skuld ships as coming-soon only (by design, post-MVP). Desktop was not live-validated this build... Routing logic has no automated net yet (Decision D1). Back-button from campaign creation exits the app — pre-existing, already a backlog story, not from this sprint."

This end-gate report is a positive example within the practice: it presented the developer with a genuine two-decision gate (D1: test-infra sequencing; D2: the campaign-scoping gap) with evidence (screenshots, an LLM transcript, a regression test showing the "stale id" theory was wrong), asked for an explicit choice, and did not claim the sprint delivered more than it verified. The developer chose Option A on both (accept, defer to a properly-specced follow-up) — a defensible call given the alternative (attempting a cross-repo architectural fix as an unbounded end-gate patch) was explicitly disclosed as riskier.

---

## 5. REALITY — what actually landed in the repos

**`nornspun-backend`:** zero commits touch campaign or picker logic in the 2026-06-17→2026-07-10 window; the only commits in that window are model-evaluation work (`git log --oneline --since=2026-06-17 --until=2026-07-10` shows exclusively `feat(evals)`/`chore(evals)` commits plus one `feat(agents): adopt tencent/hy3-preview` and one config commit). This **confirms** `team-composition.md`'s claim that "Backend work is zero — `GET /campaigns` already exists."

**`nornspun-client`:** all 8 stories landed as commits following the `feat → fix → refactor → merge(story)` pattern, merged into `sprint/sprint-2026-06-18`, then merged to `main` via commit `704e63c` (verified `git merge-base --is-ancestor 704e63c main` → `YES`; also present on `origin/main`, confirming the push happened). Diff size: 52 files changed, +3,844/−900 (`git diff --shortstat`), matching the end-gate report's claimed "35 commits (33 sprint + 2 end-gate pass), 51 files changed, +3,805/−900" closely enough to attribute the small discrepancy to baseline-commit choice, not misreporting.

**Did the landed code change what a user could do?** Yes, for campaign creation and picker navigation — confirmed by direct source inspection, not just the story's self-report:
- `NornApiClient.kt:277-291` (as of the merge) adds `listCampaigns(...)` hitting `GET /api/campaigns`, decoding newest-first, returning `emptyList()` on failure — matches AC#4/AC#10 of the S6 story spec exactly.
- The end-gate report states this flow was "exercised live against the real backend and LLM on an Android emulator, including a real campaign creation" — a live verification claim, not a diff-only claim.

**But the existing-campaign resume path is broken at the architecture level, confirmed still true today (2026-08-02):**
- `nornspun-client/composeApp/src/androidMain/kotlin/com/nornspun/ui/viewmodel/ChatViewModel.kt:219` — `private val nornConversationCache = mutableMapOf<ActiveNorn, List<ChatMessage>>()` — keyed by Norn only, not by campaign, at current HEAD (`704e63c`, main, clean working tree, verified with `git branch --show-current` → `main`).
- `nornspun-backend/src/agents/urd.py` — as of the sprint's HEAD, injected the raw campaign UUID into the prompt (`variables["campaign_name"] = ctx.deps.campaign_id`, a fallback path); this specific line was fixed later by commit `ab2e579` ("fix(agents): active-campaign prompt line carries resolved name, not raw UUID"), dated **2026-07-30** — three weeks after the sprint's end-gate and after the sprint-2026-07-13 "Sprint-2" window had already closed.
- The deeper fix — a backend session/conversation model actually keyed by campaign id — was captured as its own story, `backend-session-model-keyed-by-campaign`, and remains `"status": "backlog"` in `.momentum/stories/index.json` as of 2026-08-02 (today). It was never scheduled into sprint-2026-07-13 (its story slug does not appear in that sprint's story list, `.momentum/sprints/index.json` → active.stories).
- The settings screen (S3) is confirmed absent: `find shared composeApp desktopApp -iname "*Settings*"` in `nornspun-client` at HEAD returns only an unrelated SQLDelight key-value table (`Settings.sq`) and its generated code — no `SettingsScreen.kt` composable exists anywhere in the repo.

---

## 6. AFTERMATH — did this sprint's work hold, get reverted, or get papered over?

**No story from this sprint was later dropped, obsoleted, or reverted.** All 8 remain `"status": "done"` in `.momentum/stories/index.json` as of 2026-08-02 — this sprint's work is stable, unlike some other sprints in this investigation where stories were later found to be dead code.

**The sprint correctly generated backlog follow-through for its known gaps** — nothing was silently lost:
- `iq-2026070905565505-0bbefdab` — the campaign-scoping top-priority stub, filed 2026-07-09, `triage_class: ARTIFACT`, `priority: top`, quoting the developer's verbatim product invariant: "The model should never ask what campaign I want to use. The campaign should have been chosen prior to speaking with the Norn." This produced the story `backend-session-model-keyed-by-campaign` — still backlog.
- 13 process-improvement stubs from the transcript audit (AVFL/E2E reconciliation, presentation-rule enforcement, agent-summary JSON serialization, Read-before-Edit enforcement, etc.) — these are the seeds of the `epic impetus-core` process work that later sprints draw on.

**A concrete instance of backlog drift was caught (but shows the underlying risk):** the story `campaign-picker-get-campaigns-client-repo`, planned for and executed in sprint-2026-07-13, opens with its own developer-attention flag: "The core deliverable... **is already implemented on disk**, shipped by this story's own dependency `campaign-init-picker-screen-and-start-new-campaign-card` (status `done`; client commit `9eac68e`, sprint-2026-06-18)... The build is done. This story is therefore reframed as verify-and-close-gaps, not net-new build." This story's current status is `"review"` (not obsolete/dropped) — meaning it ran anyway, in a reframed "verify-and-close-gaps" form, rather than being cancelled outright. This is evidence that redundant work *can* slip past planning into execution even when the redundancy is documented in the story file itself before dev starts.

**The Sprint-2 promise on campaign-scoping was only partially honored, slowly:** see Section 5 — the cosmetic half (name-not-UUID) landed 2026-07-30; the architectural half remains backlog as of 2026-08-02, roughly 5 weeks after the top-priority stub was filed and roughly 4 weeks after the sprint that was supposed to carry it (2026-07-13) began.

---

## 7. VERDICT

**"After sprint-2026-06-18, a user could ___ which they could not do before."**

> **Start a new campaign from a real picker screen — tap "Start a new campaign," go through a live conversation with Urd, and see it appear as a card in a list of all their campaigns (newest-first) — and navigate back to that picker at any time via a tappable campaign-switcher in the title bar. Before this sprint, the only entry point was a bare `TextButton` in the workspace title bar that swapped in a wizard-style init screen in place of chat, with no list of past campaigns and no way to return to a picker (there wasn't one).**

This is a genuine, verified, non-mocked capability addition: it is not behind a flag, it was exercised live against the real backend and a real LLM on a live Android emulator (not just unit-tested or AVFL-diff-verified), and it merged to `main` and stayed there.

**With one load-bearing asterisk that the strict bar in this investigation's framing requires calling out explicitly:** a user **cannot** reliably resume an *existing* campaign and continue its actual conversation — tapping an existing campaign's card updates the chrome (title, Norn pips) but the underlying chat session is not scoped to that campaign; the assistant can end up in another campaign's conversation, or say it doesn't know which campaign it's in. This was caught live, disclosed honestly at end-gate, and explicitly accepted as a known gap with a promised top-priority follow-up — but that follow-up remains architecturally incomplete as of 2026-08-02, roughly five weeks later.

So the honest, complete verdict is two-sided: the **"start something new"** half of the multi-campaign capability is real, live-verified, and holds today. The **"come back to something you already started"** half — arguably the more important half for a campaign-based product where sessions recur over weeks — does not work today, was known not to work at the moment this sprint closed, and still does not work.

---

## Counter-evidence & falsifiability

Evidence that cuts **against** a purely negative "sprints never ship capability" reading:

- The create-and-list-campaigns flow is independently verifiable right now by any reader: `nornspun-client/shared/src/commonMain/kotlin/NornApiClient.kt` contains `listCampaigns(...)` hitting the real `GET /api/campaigns` endpoint, and `nornspun-backend/src/routers/campaigns.py:77-82` confirms that endpoint exists and returns real data (`created_at DESC`) — this is not a mock or a stub.
- The end-gate report for this sprint is the opposite of the "hidden defect" pattern this investigation might expect: it *led with* the two hollow areas as a mandatory developer decision, backed by screenshots and a live-repro transcript, and refused to claim the sprint was "done" on those two fronts. If the goal is to falsify "sprints paper over gaps," this sprint is a clean counter-example — the paper-over risk was explicitly designed against here.
- The desktop-test false-green defect, while not fixed within this sprint, *was* correctly diagnosed, attributed to a single root cause, and cross-referenced across 5 independent stories rather than being treated as 5 separate defects — a sign the retro/audit layer is functioning as intended, even where the underlying fix lagged.

What would prove this dossier's central finding (Section 5/6, campaign-scoping) wrong: if a reader can show (a) `nornConversationCache` (or its Desktop twin) is now keyed by campaign, not just Norn, in a commit dated after 2026-07-30 that this investigation did not see, or (b) `backend-session-model-keyed-by-campaign` has since moved off `backlog` status. Both were checked directly against `.momentum/stories/index.json` and the live repo at the time of writing (2026-08-02); a later reader should re-check both before relying on this claim.

---

## Open questions

- **Why wasn't `backend-session-model-keyed-by-campaign` scheduled into sprint-2026-07-13** given it was filed as `priority: top` on 2026-07-09, four days before that sprint's planning date (2026-07-13)? The sprint's own coverage-plan and story list do not mention it or explain the omission; this dossier could not determine whether it was considered and deprioritized, or simply not surfaced to planning. A planning-artifact-drift investigator should check sprint-2026-07-13's planning transcripts (if any survive) for a decision point on this specific stub.
- **Was the settings screen (S3) ever scheduled in any subsequent sprint?** `.momentum/features.json` and the story index were not searched exhaustively for an S3-equivalent story slug beyond confirming no `SettingsScreen.kt` exists on disk; a dedicated story slug search was out of scope for this sprint-specific dossier.
- **Desktop was never live-validated for this sprint** (end-gate report §06: "Desktop was not live-validated this build — the walkthrough guide in §07 is ready for a 10-minute collaborative pass with you"). This dossier could not determine whether that collaborative pass ever happened, or whether Desktop parity claims for this sprint's stories rest entirely on unit/render tests rather than live observation.
