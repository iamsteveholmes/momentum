# Sprint Dossier — sprint-2026-05-01 ("Campaign Init")

**Date compiled:** 2026-08-02
**Role:** Definitive evidence dossier for the nornspun delivery-discovery investigation — one sprint, evidence-first, OBSERVED vs INFERRED distinguished throughout.

---

## Executive Summary

1. **The wizard this sprint built was rejected by the product owner and fully deleted.** SDR-011 (decided 2026-05-22, the same date the sprint claims completion) rejects the 5-phase wizard model outright ("D1: 5-Phase Sequential Wizard Model — REJECTED"). The teardown commit (`b559f9b`, merged `89354eb`, 2026-06-07 in nornspun-client) deletes all 5 canvas Kotlin files this sprint built plus their tests: net **-3,655 lines**. Verified: none of the 5 files exist in the repo today.
2. **4 of the sprint's 7 stories are now `status: obsolete`** in `.momentum/stories/index.json` (`campaign-init-phases-1-2`, `campaign-flavor-tone-themes-and-world-personality`, `pc-profiles-backstory-goals-fears-and-hooks`, `campaign-init-screen-integration`). `features.json`'s campaign-init notes state this explicitly: "wizard canvas Kotlin files were built then deleted — build artifacts confirm."
3. **Of the 3 stories still marked `done`, 2 are dead code today.** `ToolSurface.kt` (built by `campaign-init-tool-surface-system`) has zero production call sites anywhere in the client — grep for `ToolSurface(` finds only its own definition file. The `SurfaceItemDispatcher` (built by `campaign-init-conversation-scroll-extension`) dispatches over a `SurfaceType` enum that is now **empty** — its `when` body is a comment: "No campaign-init canvas types remain." Only `campaign-init-tokens-and-primitives` (design tokens) has verified ongoing production use, in unrelated UI (`CampaignPickerCard.kt`, `CampaignCard.kt`).
4. **The "screen integration" story's declared scope never included wiring the screen into the app.** Its `touches:` list is `CampaignInitScreen.kt`, `CampaignInitViewModel.kt`, `SessionZeroSeedCanvas.kt`, `CampaignCard.kt` — no `MainActivity.kt`, no `MainWindow.kt`. The Android "New Campaign" entry point landed in a separate, story-untracked commit the **next day** (2026-05-04). The Desktop entry point didn't land until **2026-05-19** — 16 days after all 7 stories were marked done. Desktop users had zero way to reach the built screen for over two weeks post-"done."
5. **The sprint's own retro-transcript-audit independently reached a compatible conclusion**, dated 2026-05-30: "the application was marked 'done' while showing only errors on screen," AVFL "reported 'pass' despite... a crash error," and the user's own words were captured verbatim: *"Now that was some SERIOUS B.S."* and *"a status lie."* The audit produced 13 backlog stories targeting exactly this class of gate failure — the heaviest single-sprint practice-debt output recorded up to that point.
6. **The rejection came from a hands-on product walkthrough, not from the sprint-dev pipeline.** Session transcripts (2026-05-19) show the developer running an ad hoc AVFL of the design against `DESIGN.md` + HTML/CSS + source, surfacing "17 confirmed gaps," and saying of the sprint's E2E harness: *"We honestly don't even know if that code works... We don't know if it works at all."* Three days later SDR-011 formalized the wizard's rejection.
7. **Backend schema/endpoints from 2 of the 4 obsoleted stories survive** (migrations 010/011/012, `heroes.py`, `campaigns.py`, `hero_repo.py`) — `features.json` explicitly says "backend schema KEEP." But the current client makes **no calls** to the hero or flavor endpoints; `CampaignInitViewModel.kt` carries a literal `TODO(route-handoff)` noting the flavor turn "opens no surface" and awaits a sibling story. The backend surface is orphaned today.
8. **A genuine, durable quality win did land**: an IDOR vulnerability in the heroes endpoint (hero_id not scoped to campaign_id) was caught by adversarial review before merge (commit `b4c568d`, 2026-05-03) and the fix is still present in `heroes.py` today. This is real, surviving value — independent of the wizard's fate.
9. **All Maestro E2E flows built during this sprint's "5 rounds" of validation are gone.** The current `maestro/flows/` directory contains only generic flows (smoke, chat, seed-campaign) — no campaign-init-specific flow survives, consistent with the wizard's full teardown.
10. **The sprint's own specs were framed as user capability**, not raw tasks — every `.feature` file in `specs/` opens `Given the Nornspun app is running and the Spinner is in campaign init...`. The failure mode here is not spec-framing divorced from user language; it is (a) scope boundaries that excluded "is this reachable," (b) quality gates that reported pass on broken/garbled output, and (c) a late-discovered product-direction error that made the correctly-built thing the wrong thing to build.

---

## 1. INTENT

**Sprint identity** (`.momentum/sprints/index.json`): `sprint-2026-05-01`, planned 2026-05-01, started 2026-05-02, status `done`. 7 stories, 7 waves (see §2).

**Goal framing — epic level** (`docs/planning-artifacts/epics.json`, OBSERVED): the two epics this sprint's stories belong to are framed as user capability:
- `fantasy-client`: *"A Spinner interacts through a beautiful, accessible fantasy-themed client."*
- `campaign-intelligence`: *"A Spinner's campaign becomes unique — flavor, NPCs, PCs, cross-agent awareness make every interaction feel like a co-GM."*

**Goal framing — story/spec level** (`.momentum/sprints/sprint-2026-05-01/specs/*.feature`, OBSERVED — all 7 files read in full): every feature file's `Background:` is stated in terms of the Spinner (GM) doing something in a running app, e.g.:
- `campaign-init-phases-1-2.feature`: *"Given the Nornspun app is running and the Spinner is on the campaign picker screen"* → *"When the Spinner taps the new campaign entry"* → *"Then... Urd's greeting message appears."*
- `pc-profiles-backstory-goals-fears-and-hooks.feature`: *"Given the Spinner has indicated the party has four heroes"* → *"When the hero profile phase begins"* → *"Then a canvas opens... prompts for the hero's name, class, backstory, goal, fear, and hook."*

**Verdict on intent framing:** the sprint's specs and epic goals were explicitly framed as user capability (Gherkin, Spinner-as-actor), not as internal tasks. This is a notable finding against a naive version of the mission hypothesis — the *specification layer* was not the failure point for this sprint. See §7 and Counter-Evidence for the fuller nuance.

**Feature-level target** (`.momentum/features.json`, OBSERVED): `campaign-init`'s `acceptance_condition` is: *"A GM can start a new campaign from the campaign picker... walk through a conversation with Urd that captures name, game system, party size and starting level, at least one PC with backstory and a fear, and campaign flavor with a tone and one sensory term — then receive a first session prep from Verdandi that references the PC's fear and campaign flavor without re-explaining either."* This acceptance condition describes the **wizard model** this sprint built (5-phase, party/hero/flavor all captured). It was written against the model that SDR-011 later rejected — the feature's own definition-of-done became invalid mid-flight (INFERRED from the fact that D2/D3 of SDR-011 directly contradict the "party size... at least one PC... campaign flavor" required-fields framing).

**No plan-gate artifact exists for this sprint.** `ls` of `.momentum/sprints/sprint-2026-05-01/` shows only `audit-extracts/`, `retro-transcript-audit.md`, `specs/`, `sprint-summary.md` — no `coverage-plan.md`, `plan-gate-decision.md`, or `team-composition.md` (these exist in later sprints per the mission's repo map). OBSERVED via directory listing; this sprint predates that artifact convention.

---

## 2. PLAN

**7 stories, 7 waves, mostly sequential** (`.momentum/sprints/index.json`):

| Wave | Story | Notes field (verbatim) |
|---|---|---|
| 1 | campaign-init-tokens-and-primitives | — |
| 2 | campaign-init-tool-surface-system | "Depends on Wave 1" |
| 3 | campaign-init-conversation-scroll-extension | "Depends on Wave 2" |
| 4 | campaign-init-phases-1-2 | "Depends on Wave 3. Touches campaign.py — must precede campaign-flavor" |
| 5 | campaign-flavor-tone-themes-and-world-personality | "sequenced to avoid merge conflict on campaign.py (not a declared logical dependency)" |
| 6 | pc-profiles-backstory-goals-fears-and-hooks | "sequenced to avoid merge conflict... (not a declared logical dependency on campaign-flavor)" |
| 7 | campaign-init-screen-integration | "depends on... Waves 4, 5, 6 all being merged first" |

Several wave orderings are explicitly file-conflict-driven rather than logical dependencies (waves 5 and 6's own notes say so) — a single-track, low-parallelism plan.

**Product-capability vs. infrastructure split** (read from `.momentum/stories/index.json` + `specs/*.feature`, OBSERVED):
- **Foundational/component-infra (3 of 7):** `campaign-init-tokens-and-primitives` (design tokens: `NornRadii`, `NornColors`, `NornTheme`), `campaign-init-tool-surface-system` (the generic `ToolSurface` canvas component), `campaign-init-conversation-scroll-extension` (plumbing to interleave surfaces into the chat scroll). These stories build reusable machinery; no story's spec describes a GM-visible capability that didn't already exist without them — they are enablers for the 4 stories below.
- **Product-facing feature (4 of 7):** `campaign-init-phases-1-2` (identity + party canvases), `campaign-flavor-tone-themes-and-world-personality`, `pc-profiles-backstory-goals-fears-and-hooks`, `campaign-init-screen-integration` (journey state machine wiring all 5 phases + Phase 5 close/session-zero). These 4 are the stories that got obsoleted (§6).

So structurally: 3/7 stories were infrastructure in service of a specific UX model, and 4/7 were the model's actual expression — and the entire model (the 4, plus the 3's only real consumer) was rejected six weeks later.

**Team composition:** no `team-composition.md` exists for this sprint (see §1). From `audit-extracts/agent-summaries.jsonl` (116 total agent runs across the sprint's full lifecycle including retro), role counts: `general-purpose` 71, `Explore` 20, `momentum:dev-frontend` 15, `momentum:e2e-validator` 7, `momentum:qa-reviewer` 1, `momentum:dev` 2. This mixes sprint-dev execution agents with orientation/discovery and retro-audit agents in one file; it is not a clean per-story team roster (OBSERVED — file structure, not further disaggregated here).

---

## 3. EXECUTION

**Story commits landed quickly** (`nornspun-client` git log, OBSERVED): all 7 stories' primary commits are dated 2026-05-03 (`df7d85a` tokens through `b17f12e` screen-integration), with four same-day fix commits explicitly tagged `— sprint-2026-05-01` (`2f30677`, `0e6806a`, `ac738a2`, `348a5b7`). The backend side (`nornspun-backend`) landed party fields, flavor fields, and the heroes table across three migrations (010, 011, 012) plus an IDOR fix, all dated 2026-05-03.

**But the app-entry-point wiring did not land with the stories:**
- Android "New Campaign" entry point (`MainActivity.kt` `TextButton` + `AppStateViewModel.showCampaignInit`): commit `b5fd2a9`, **2026-05-04** — one day after `campaign-init-screen-integration`'s commit, and **not listed in that story's `touches:` scope** (verified: the story file's touches are `CampaignInitScreen.kt`, `CampaignInitViewModel.kt`, `SessionZeroSeedCanvas.kt`, `CampaignCard.kt` only).
- Desktop entry point (`MainWindow.kt`): commit `8e0501f`, **2026-05-19** — 16 days after the stories were marked done.

Between 2026-05-03 and 2026-05-19, further bug-fix and wiring commits continued landing against this feature (hero-count parsing, starting-level handoff, posture-field interactivity, `POST /campaigns` path correction) — i.e., the feature was still being actively stabilized for over two weeks after its stories reached `done`.

**E2E validation was severe and multi-round.** Per `retro-transcript-audit.md` (`.momentum/sprints/sprint-2026-05-01/retro-transcript-audit.md`, read in full): 5 rounds total. Round 1 found systematic swipe-direction inversion and a non-interactive posture field; Round 2 re-ran the full suite instead of targeted re-runs; Round 3 had Maestro YAML syntax errors; a "Team Review" pass hit 16 errors including OOM (exit 137) and gRPC UNAVAILABLE; Round 5 (targeted) finally stabilized. Root cause per the audit: `evalWithAI`/`compose-ui-test-server` was not functional when E2E was first attempted, and flow authoring ran before implementation was stable.

**Direct evidence of the app being broken while claimed functional**, dated **2026-05-04** (`audit-extracts/user-messages.jsonl`, OBSERVED verbatim, timestamp `2026-05-04T04:45:57.520Z`):
> "I'm fairly sure you're lying to me. I see an error in the emulator window. I am a Customer looking at the demo seeing nothing but errors and you the sales person are lying and gaslighting me into thinking something is happening that is not."

This occurred mid-sprint (day 2-3 of execution), not at final sprint close — worth noting precisely, since the retro's executive summary discusses this alongside "marked done" language without pinning the exact moment; the raw transcript places it early, during active story development, not at the 2026-05-22 completion date.

**The decisive walkthrough, 2026-05-19** (`audit-extracts/user-messages.jsonl`, OBSERVED verbatim; this is the last date with any captured user messages for this sprint — the file's timestamp range is 2026-04-28 to 2026-05-19): the developer runs an ad hoc AVFL comparing `DESIGN.md`, HTML/CSS hi-fi, and source components, surfacing "17 confirmed gaps," then triages them. Two quotes from this session:
> "We honestly don't even know if that code works. I think we went way too far for a repo with 6 stars and 24 commits. We don't know if it works at all" (re: the vendored `compose-driver` E2E harness)

> "So we're done?" ... "It's still open."

The sprint-summary claims completion on 2026-05-22 and SDR-011 is dated 2026-05-22 — three days after the last captured transcript activity. INFERRED (not directly observed in captured data): the SDR-011-triggering "sprint walkthrough session" referenced in the decision doc's Summary is very likely the same 2026-05-19 session or its immediate continuation, given the matching description ("sprint-2026-05-01 walkthrough" appears verbatim in the triage arguments text from that session) — but the actual SDR-011 conversation content itself is not present in the audit-extracts data (source_research lists it as `type: developer-conversation`, `path: "(conversation)"`, not a session file).

**Retro-transcript-audit's own diagnosis** (`retro-transcript-audit.md`, read in full, OBSERVED): 378 user messages, 116 subagents, 272 tool errors, 18 struggles, 8 successes, 26 user interventions, 7 cross-cutting patterns identified. Verbatim executive summary: *"the application was marked 'done' while showing only errors on screen, E2E validation required five full passes to stabilize, an AVFL fixer silently regressed the testing stack, and the user had to personally intervene to re-anchor design authority, E2E strategy, pane hygiene, and feature naming."* Pattern 1 named directly: **"Validation Theater — Gates That Don't Block on Real Failure"** — *"AVFL reported 'pass' on garbled output... E2E validation passed on paper while the app showed errors... Feature completion status was set without demonstrable behavior."* The audit produced **13 backlog stories** (all `impetus-core` epic) targeting E2E pre-flight gates, AVFL fixer rule-reading discipline, and live-screen-evidence requirements — the sprint-summary calls this "the heaviest backlog of practice debt this project has generated from a single sprint."

**What worked, concretely** (retro-transcript-audit.md, OBSERVED): adversarial code review caught a real IDOR vulnerability (heroes endpoint — `hero_id` not scoped to `campaign_id`) before merge; caught `androidx.*` imports in `commonMain` that would have broken the Desktop build; caught a session-zero dead-end where the journey never completed. Sprint-plan validation caught two stale `stories/index.json` entries pre-execution. These are genuine, verified quality-gate successes independent of the wizard's later rejection.

---

## 4. CLAIM

**Sprint-summary.md** (`.momentum/sprints/sprint-2026-05-01/sprint-summary.md`, read in full): "Sprint completed: 2026-05-22." "7/7 stories reached `done`." "campaign-init (`partial`) — All 7 sprint stories completed and E2E validated after 5 rounds on device. Feature remains at `partial` in features.json; promotion to `working` is a candidate for next planning cycle pending a clean end-to-end demo." Five decisions recorded (SDR-007 through SDR-011). 13 practice-improvement stories added to backlog. Narrative explicitly names the 3 root causes (E2E infra readiness, context/compaction fidelity, gates reporting pass on failure) and frames SDR-011 as a codification outcome rather than a reversal of sprint output.

**Notably honest framing:** the sprint-summary does **not** claim the feature is fully working — it explicitly leaves `campaign-init` at `partial` and flags "pending a clean end-to-end demo." This is a genuine point in favor of the practice's self-honesty at the summary layer; the claim was not "done and shippable," it was "stories done, feature partial." The gap between this claim and reality (§6) is that even "partial, pending a clean demo" undersold how much of the 7-story output would be deleted outright within six weeks.

**No end-gate report** exists for this sprint (this predates the single end-gate / Conductor artifact convention noted in later sprints per the mission's repo map) — the sprint-summary and retro-transcript-audit are the terminal claim artifacts. OBSERVED via directory listing (§1).

---

## 5. REALITY

**Client repo** (`nornspun-client`, git log, OBSERVED — commands and output shown in full above): the 7 stories' commits landed 2026-05-03; entry-point wiring landed 2026-05-04 (Android) and 2026-05-19 (Desktop); continued stabilization commits ran through 2026-05-19.

**Backend repo** (`nornspun-backend`, git log, OBSERVED): migrations 010 (party fields), 011 (campaign flavor), 012 (heroes table) plus an IDOR fix, all 2026-05-03.

**Did the landed code change what a user could DO, at the time?** Provisionally yes, for a limited window: an Android user who navigated via the new "New Campaign" button (available from 2026-05-04) could walk through a 5-phase wizard capturing name, system, party size, hero profiles, and campaign flavor — something not previously possible. A Desktop user could not do this until 2026-05-19. This capability existed in a stabilizing, bug-fixed state through roughly 2026-05-04 to 2026-05-22 (Android) and 2026-05-19 onward (Desktop) — a window of days-to-weeks — before being rejected as a product direction (§6). Whether it was ever demonstrated end-to-end cleanly on a real device without errors before the 2026-05-19 walkthrough could not be confirmed from the captured data (see Open Questions).

---

## 6. AFTERMATH

**Story status today** (`.momentum/stories/index.json`, queried directly, OBSERVED):

| Story | Status today |
|---|---|
| campaign-init-tokens-and-primitives | `done` |
| campaign-init-tool-surface-system | `done` |
| campaign-init-conversation-scroll-extension | `done` |
| campaign-init-phases-1-2 | **`obsolete`** |
| campaign-flavor-tone-themes-and-world-personality | **`obsolete`** |
| pc-profiles-backstory-goals-fears-and-hooks | **`obsolete`** |
| campaign-init-screen-integration | **`obsolete`** |

**`features.json` campaign-init notes** (OBSERVED, verbatim): *"OBSOLETE per SDR-011 D1 (wizard): campaign-init-phases-1-2, campaign-init-screen-integration, campaign-flavor-tone-themes-and-world-personality, pc-profiles-backstory-goals-fears-and-hooks (backend schema KEEP; wizard canvas Kotlin files were built then deleted — build artifacts confirm)."*

**The rejection decision — SDR-011** (`docs/decisions/sdr-011-campaign-init-conversational-model-2026-05-22.md`, read in full): dated 2026-05-22 (the sprint's own claimed completion date). D1: *"5-Phase Sequential Wizard Model — REJECTED... The current wizard makes the GM feel like they're filling out a form before they're allowed to use the app. That's the opposite of the product's voice."* D2: a campaign name is the only required input. D3: Urd suggests, never requires. D6: character sheets are imported if desired, never built by Nornspun — this directly invalidates the purpose of `HeroProfileCanvas` (built by `pc-profiles-backstory-goals-fears-and-hooks`).

**The actual deletion — verified via git** (`nornspun-client`, OBSERVED): commit `b559f9b` ("feat(ui): remove 5-phase wizard from CampaignInitScreen — reduce to threshold + suggestion list"), merged via `89354eb`, both dated **2026-06-07** — roughly 5-6 weeks after the sprint's stories were marked done. Diff stat: **19 files changed, 233 insertions(+), 3,888 deletions(-)**. Deletes outright: `CampaignFlavorCanvas.kt` (257 lines), `CampaignIdentityCanvas.kt` (199), `HeroProfileCanvas.kt` (323), `PartyFoundationCanvas.kt` (160), `SessionZeroSeedCanvas.kt` (196), `HeroTransitionMessages.kt` (49), and 4 corresponding test files (`CampaignFlavorCanvasTest.kt`, `CampaignIdentityCanvasTest.kt`, `HeroProfileCanvasTest.kt`, `PartyFoundationCanvasTest.kt` — combined 1,247 more lines). Guts `CampaignInitViewModel.kt` (removes the `CampaignInitPhase` enum and all phase-transition methods) and `CampaignInitScreen.kt` (removes `injectSurfaceForPhase` and the phase re-injection `LaunchedEffect`).

**Confirmed by direct file-existence check** (`find` over the current working tree, OBSERVED): none of the 5 canvas `.kt` files exist anywhere in `nornspun-client` today.

**Note on a metadata discrepancy** (OBSERVED, minor, does not affect the core finding): the removal story's `status_synced` field in `stories/index.json` reads *"merged-to-main sprint-2026-05-30 (commit 8d71f09, end-gate APPROVED)"* — but `git log --all` in `nornspun-client` shows no commit `8d71f09`; the actual, verified merge commits are `b559f9b`/`89354eb`, dated 2026-06-07, not sprint-2026-05-30. The deletion event itself is independently confirmed via the real commits and current file-absence; only the provenance stamp's specific commit hash and sprint attribution appear to be wrong.

**What survives, checked directly against the current codebase (OBSERVED, not inferred):**
- `campaign-init-tokens-and-primitives` — **genuinely alive.** `NornRadii` is referenced in 8 files including active production UI: `CampaignPickerCard.kt`, `CampaignCard.kt`, `SilenceToggle.kt`, `ConversationList.kt`. This is the one story from the sprint with verified ongoing production value — though as a design-token library, not as a user-facing capability in its own right.
- `campaign-init-tool-surface-system` — **dead code.** `grep -rl "ToolSurface(" --include="*.kt" .` (excluding build artifacts) returns only `ToolSurface.kt` itself — zero call sites in any screen or viewmodel. Its only test file, `ToolSurfaceSystemTest.kt`, documents itself as *"pure value/logic tests — no Compose render harness"* — meaning even its test coverage was never a render-level check, let alone a user-facing one.
- `campaign-init-conversation-scroll-extension` — **no-op today.** The `SurfaceItemDispatcher` this story built in `ConversationList.kt` renders a `Box` around an empty `when` body; the current code comment reads: *"All campaign-init canvas SurfaceType values have been removed per SDR-011 D1. This dispatcher shell is retained for future journey canvas types. The `when` expression is exhaustive over the current (empty) `SurfaceType` enum."* Verified: `enum class SurfaceType` in `ConversationItem.kt` has zero entries today. (The surrounding base chat-message scroll — unrelated to this story's specific "interleave tool surfaces" scope — continues to function for ordinary chat.)

**Backend orphaning** (OBSERVED): the heroes and campaign-flavor backend surfaces (`heroes.py`, `campaigns.py`, `hero_repo.py`, migrations 011/012) still exist and presumably still pass their own tests, per `features.json`'s "backend schema KEEP." But the current `CampaignInitViewModel.kt` makes no calls to either — its own doc comment says *"There are NO canvases in campaign-init... no flavor-canvas state,"* and a `TODO(route-handoff)` marks the flavor signal as awaiting a not-yet-landed sibling story to consume it. Grep of `shared/src/commonMain` for `heroes`/`flavor` call sites (excluding tests and comments) turns up none. INFERRED: this backend surface is reachable by nothing in the shipped client today, though it is plausible (not verified) that a future story reconnects it.

**One durable, independently-verified win:** the IDOR fix in `heroes.py` (campaign_id/hero_id ownership check, commit `b4c568d`, 2026-05-03) is present in the router today — confirmed by reading the current file. This protects an endpoint the client doesn't currently call, but the fix itself is real and would matter the moment that endpoint becomes reachable again.

**E2E artifacts:** none of the Maestro flows built/repaired across this sprint's 5 validation rounds exist in the current `maestro/flows/` directory (OBSERVED — directory listing shows only generic flows: `smoke.yaml`, `chat_send_message.yaml`, `00_seed_campaign.yaml`, etc., none scoped to campaign-init phases or canvases).

---

## 7. VERDICT

> "After sprint-2026-05-01, a user could ___ which they could not do before."

**This sentence cannot be honestly completed with a durable claim.** The strongest true statement obtainable from the evidence is conditional and time-boxed:

*"For a window of roughly 2-6 weeks (Android: 2026-05-04 onward; Desktop: 2026-05-19 onward), a GM could tap 'New Campaign' and walk through a 5-phase wizard (identity → party → heroes → flavor → session-zero) capturing structured campaign data that they could not capture before — but the product owner rejected this entire interaction model on first genuine hands-on walkthrough (SDR-011, 2026-05-22), and every line of UI code implementing it was deleted six weeks later (merged 2026-06-07, -3,655 net lines). None of that capability exists in the app today."*

Of the sprint's 7 stories:
- **4/7 (the entire product-facing feature set)** are formally `obsolete`, their code deleted, verified by direct file-absence check.
- **2/7 (infrastructure stories)** are marked `done` but are dead code today — zero production callers, one enum reduced to zero entries.
- **1/7 (design tokens)** has genuine surviving value — but as shared design-system infrastructure consumed elsewhere, not as a GM-facing capability delivered by this sprint.
- **Backend schema for 2 of the obsoleted stories survives** but is currently unreachable from the client (orphaned), with one durable side-benefit (an IDOR fix) that protects a currently-unused endpoint.

By story count, roughly **0 of 7 stories' original user-facing intent survives in the live product today.** The single piece of lasting value (design tokens) was never itself the user-facing deliverable — it was scaffolding for a deliverable that no longer exists.

---

## Counter-Evidence & Falsifiability

Evidence that complicates or cuts against a simple "stories over functionality" reading of this sprint:

1. **Specs were user-capability framed, not task-framed.** Every Gherkin `.feature` file in this sprint's `specs/` opens with the Spinner as the actor performing a concrete in-app action. If the mission hypothesis is "sprints write ACs about tasks, not user capability," this sprint is a counter-example at the specification layer — the failure here is downstream of spec quality (scope boundaries, gate validity, and a late product-direction reversal), not spec framing itself.
2. **The rejection was a legitimate, late-arriving product decision, not obviously a process failure.** SDR-011 reads as the developer directly evaluating a working build and concluding the underlying *product concept* — not the code quality — was wrong ("felt wizardy"). One could argue this is the practice **working as intended**: a real hands-on walkthrough caught a bad direction before it shipped further, and it was corrected via a formal decision document rather than silently. The cost (7 stories' worth of UI work deleted) is real, but the mechanism that caught it (a product walkthrough) is not itself evidence of "stories passing while functionality fails" — it is evidence of "the functionality worked as specified, and the spec turned out to encode the wrong product."
3. **Adversarial review caught real, severe bugs pre-merge** (IDOR vulnerability, Desktop-build-breaking import, a session-zero dead-end) — these are not "validation theater"; they are verified, concrete catches with lasting value (the IDOR fix still guards the endpoint today).
4. **The sprint-summary did not overclaim.** It explicitly left `campaign-init` at `partial` status and called for "a clean end-to-end demo" before promotion — this is a more honest self-report than "shipped and done," even though the actual outcome (near-total deletion) was still far worse than "partial, pending demo" implied.
5. **The sprint's own retro correctly diagnosed much of this** and generated 13 concrete backlog stories targeting E2E pre-flight gates and gate-validity — i.e., the practice's feedback loop identified real root causes at the time, two months before the sprint-2026-07-13 crisis that triggered this broader investigation. Whether those 13 stories were ever built and whether they would have prevented later failures is outside this dossier's scope (see Open Questions and cross-reference the sprint-2026-07-13 dossier).

**What would prove the headline finding wrong:** if the "obsolete" statuses in `stories/index.json` were found to be a labeling error unconnected to actual code removal (ruled out here — verified independently via git diff stats and direct file-absence checks), or if a later sprint's git history showed the deleted canvases being reintroduced under new filenames serving the same user-facing purpose (not checked beyond sprint-2026-05-30's teardown commit and the current-state greps above — a full corpus-wide search for reintroduction was out of scope for this single-sprint dossier).

---

## Open Questions

1. **Was the wizard ever cleanly demonstrated end-to-end on a real device before rejection?** The retro-transcript-audit says "Round 5 (targeted) finally stabilized flows," but the audit-extracts data (user-messages.jsonl) has no captured content after 2026-05-19, and the walkthrough that produced SDR-011 is dated 2026-05-22 with no corresponding session transcript in the audit-extracts (its `source_research` is typed `developer-conversation`, path `"(conversation)"` — not a session file). Whether Round 5's "stabilized" state is the same build the product owner walked through, or whether further changes occurred between 05-19 and 05-22, could not be determined from available data.
2. **Why does the removal story's `status_synced` field cite a non-existent commit (`8d71f09`) and the wrong sprint (`sprint-2026-05-30` vs. the actual 2026-06-07 merge)?** This is a metadata/provenance defect in `stories/index.json`'s bookkeeping, not a finding about the deletion itself (which is independently confirmed). Root cause not investigated — outside this dossier's scope.
3. **Is the orphaned backend surface (heroes/flavor endpoints) actually planned to be reconnected**, or is it dead weight being carried forward? `features.json` notes reference a "critical path: client-campaign-init-conversation-over-sse, blocked on backend-campaign-init-emit-campaign-created-event" and NEW stories for "campaign-identity flavor/party/hero canvases" — suggesting a planned reconnection exists in the backlog, but this dossier did not trace those stories' current status.
4. **Team composition and per-story agent assignment** could not be reconstructed cleanly — no `team-composition.md` exists for this sprint, and `agent-summaries.jsonl` mixes sprint-dev execution with orientation and retro-audit agents in one undifferentiated stream (116 entries, role-tagged but not phase-tagged in a way this dossier's time budget allowed disaggregating further).
