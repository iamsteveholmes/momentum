# The Architect's Position — There Is No Product to Deliver

**Date:** 2026-08-02
**Seat:** The Architect (adversarial)
**Corpus:** `docs/research/nornspun-delivery-discovery-2026-08-02/` — read in full, then re-verified against raw sources
**Verification stance:** 13 load-bearing claims independently re-checked against the repos and raw transcripts. **Two corpus claims failed verification, and one of them is the corpus's own headline example.** See §3.

---

## 1. Thesis

**Nornspun has no artifact that *is* the product.** "The product" is a manual composition of two independently-versioned git trees, selected implicitly and freshly at every launch, with no contract between them, no automated assembly, no forcing function to trunk, and no test anywhere in either repository that crosses the seam where they meet.

Everything the developer experienced follows from that one absence. Not "we plan stories instead of features." Not "the process has too much ceremony." Not "verification is theater." Those are downstream. When there is no defined referent for the word "product," then:

- you cannot **verify** it (you verify diffs and in-process routes instead — §2.4);
- you cannot **ship** it (there is no state transition that means "released" — §2.3);
- you cannot **report** on it (four registries disagree because none of them is reading a product — §2.5);
- and — the finding that decided this paper — you cannot **argue about it correctly**, because even a well-resourced adversarial audit will diagnose the wrong tree and propagate a false conclusion into its own headline (§3.2).

The developer's framing — "we focus on delivering stories rather than delivering functionality" — is the right instinct pointed at the wrong layer. The practice does not fail to define functionality. `features.json` has defined every feature as a plain-language user capability since 2026-05-25, has said `partial` for every user-facing feature continuously since 2026-06-16, and was *correct*. The 07-13 end-gate report defined the outcome and stated in its own hero paragraph that the outcome was not met. **Definition was never the missing ingredient. Referent was.**

A one-sentence version: *you cannot hold a product to a standard when nobody can point at the product.*

---

## 2. Ranked diagnosis

I am naming one load-bearing cause, not five co-equal ones. Causes 2–5 are real and each independently costs delivery, but each is either caused by Cause 1 or rendered unfixable by it.

### Cause 1 — LOAD-BEARING: build identity is undefined, so "the product" is assembled ad hoc at every launch

**What.** There is no command, script, manifest, or container that composes nornspun. The backend and client live in separate repositories with separate branch states, separate worktrees, separate remotes, and separate (or absent) CI. Which pair of commits constitutes "the app" is decided moment-to-moment by whoever types the launch command, and is recorded nowhere.

**The evidence, verified directly from raw transcripts (not from the corpus):**

Every backend launch across both of the developer's review sessions came from the `main` checkout. Every client launch came from the sprint-branch worktree:

| When (UTC) | Client launched from | Backend launched from |
|---|---|---|
| 2026-07-22T18:42:18 | — | `/Users/steve/projects/nornspun-backend` (**main**) |
| 2026-07-22T22:58:47 | `.conduct-wt/nornspun-client/INTEGRATION` (**sprint**) | (same main uvicorn, port 8001) |
| 2026-07-31T04:29:35 | `.conduct-wt/nornspun-client/INTEGRATION` (**sprint**) | — |
| 2026-07-31T05:31:31 | (same) | `/Users/steve/projects/nornspun-backend` (**main**) |

Source: `~/.claude/projects/-Users-steve-projects-nornspun/20b5f62e-79aa-4579-afb8-791c311ff151.jsonl`, `Bash` tool-use records, extracted by targeted JSON parse. There is **no** launch of `.conduct-wt/nornspun-backend/INTEGRATION` anywhere in that session.

At that moment `main` was **26 commits behind** the sprint branch (`git rev-list --left-right --count main...sprint/sprint-2026-07-13` → `1 26`). So the developer's damning walkthrough — the one that produced *"the agent doesn't know what campaign I've chosen. If it doesn't know the campaign I've chosen how can it save anything to that campaign?"* — ran a **July-22 client against a July-8 backend**. That is not the sprint. That is not `main`. That is not any state that has ever existed in version control. It is a chimera.

**Why it is load-bearing — trace the causal chain, every link verified:**

1. The story `backend-active-campaign-name-injection-fix` shipped a real fix on the sprint branch, commit `2eef2bf` (2026-07-21). Verified: on the sprint branch `src/agents/urd.py:189-193` reads `variables["campaign_name"]` and appends `Active campaign: {campaign_name}`. On `main` at the merge-base (`af88f0f`), line 190 appends only `ctx.deps.campaign_id` — the raw UUID.
2. The developer ran the backend from `main`, and so saw the raw-UUID behavior. Correct symptom; wrong tree.
3. A live diagnosis in-session concluded the story's fix was *broken* rather than *absent*, and wrote a **second, independent implementation of the same fix directly onto `main`** — commit `ab2e579` (2026-07-30), outside any sprint, story, review, or conduct pipeline. Its own commit message asserts it adds *"the assertion the original story lacked."*
4. **That assertion is false.** `git show 2eef2bf -- tests/agents/test_urd.py` adds `assert "Active campaign: The Ashen Coast" in result` and `assert str(campaign_id) not in result`, where `result` is the *rendered system prompt*. The story wrote exactly the outcome-level assertion the hotfix claims it lacked.
5. That hotfix is why `main` is now `1` ahead of the sprint branch. Before it, the branches were fast-forwardable. Now merging requires conflict resolution on the same function, in the same file, for the same defect — **the divergence was manufactured by the chimera**.
6. The corpus's verification lens then took the in-session diagnosis at face value and elevated it to its executive-summary finding #5 as *"a concrete instance of hollow verification."* The ours-vs-field comparison document promoted that to its §1.1 headline: *"That is Anthropic's sentence, re-enacted."*
7. This council was briefed on that conclusion.

**Read that chain again.** Undefined build identity did not merely produce a bad walkthrough. It produced a false bug report, a redundant fix committed outside all process, a manufactured merge conflict, a false finding in a multi-agent audit, a false headline in the comparison document, and a false premise in a strategy council. **The defect propagated through six epistemic layers, and each layer added confidence.** That is what a structural failure at a foundation looks like — not one broken feature, but a systematic corruption of everything built on top, including the ability to diagnose it.

No amount of better outcome definition, better slicing, or better verification survives this. Verification of *what*? Slicing produces *which* artifact? The developer taste-tests *which build*? A practice with no defined referent cannot be improved by any change that presupposes one.

---

### Cause 2 — The client/backend seam has no enforced contract, and no test in either repo crosses it

**What.** Two repos, hand-written types on both sides, hand-typed URL strings, and zero mechanical agreement.

**Evidence (verified):**
- **No contract artifact exists.** `grep -ril openapi` across the client returns nothing. `find` for any path containing `contract` across both repos returns nothing. No codegen, no shared schema module, no consumer-driven contract test. The client declares its DTOs by hand in `shared/src/commonMain/kotlin/NornApiClient.kt`; the backend declares its own in `src/models/`.
- **The binding is string literals.** `NornApiClient.kt` uses `"$baseUrl/api/chat"` (:184), `"$baseUrl/api/campaigns"` (:248, :282) — and `"$baseUrl/campaigns/$campaignId/adventures"` (:320). The backend mounts `adventures.router` at `prefix="/api"` (`main.py:45`) atop the router's own `prefix="/campaigns"` (`adventures.py:49`). Live path: `/api/campaigns/{id}/adventures`. **Adventure upload has always 404'd.**
- **No test can see it.** Backend `tests/routers/test_adventures.py` (478 lines) calls the route in-process, so it never sees a client URL. `grep -c uploadAdventure shared/src/commonTest/kotlin/NornApiClientTest.kt` → **0**. That test file's own "real backend" case uses `baseUrl = "http://localhost:1"` — a deliberately dead port. `grep -rl "embeddedServer\|ProcessBuilder"` across the entire client → **no matches**. **Not one test in either repository ever crosses the process boundary between the two halves of the product.**
- **The seam is where the product is missing.** Nine backend routes have zero client callers (heroes ×3, campaign PATCH + flavor ×2, adventures list/get/delete ×3, `GET /tasks/{id}`, `POST /sessions/{id}/resume`). Verdandi's session-prep has a real backend and an empty `SurfaceType` enum for a UI. `ChatViewModel.loadConversationHistory` is a literal empty body (`ChatViewModel.kt:720-722`). `sessionCount = 0` is hardcoded (`CampaignPickerScreen.kt:87`). The settings gear is `onOpenSettings = {}` in both shells (`MainWindow.kt:312,338`; `MainActivity.kt:386,412`).

**Why it ranks second, not first.** Every one of these is a *findable* defect — a contract check would surface them in an afternoon. But you cannot write a contract check against an undefined pair of trees, and a passing contract check tells you nothing if the walkthrough runs a different pair. Cause 2 is the highest-yield fix; Cause 1 is its precondition.

---

### Cause 3 — The pipeline's terminal state is a document, not a release

**What.** Nothing in the practice mechanically transitions code toward users. The end-gate emits HTML.

**Evidence (verified, and partly new — the corpus did not find items 2 and 3):**
1. Sprint 2026-07-13's 26 backend + 27 client commits have sat unmerged since 2026-07-22. All 12 stories are `status: review`; the sprint is `status: active, locked: true`; `planning: null`. The end-gate report's own §07 approve sequence (merge → transition → guard) never executed.
2. **`nornspun-backend`'s `main` is 23 commits ahead of `origin/main`, which was last updated 2026-06-11.** Nearly two months of `main` exists only on this laptop. Sprint branches were never pushed at all.
3. **The client repository has no CI whatsoever** — no `.github` directory. The backend has one `ci.yml` whose first line reads `# stub — full CI pipeline implemented in D6`, and D6 (`cloud-platform`) is explicitly post-MVP. It triggers `on: [push, pull_request]` — so it has not run on any of those 23 commits, nor on any sprint commit, ever.

**Why this is structure and not discipline.** The practice automates story selection, spec generation, worktree creation, dev, code review, AVFL, and E2E — and then hands a human a rendered HTML report and asks them to type `git merge`. It is the single least-automated step in a fully-automated pipeline, and it is the only step that turns work into product. An approval that leaves 26 commits stranded is not an approval; it is an opinion.

---

### Cause 4 — Verification binds to code layer, not to the assembled product

**What.** `verification-standard.md` routes stories to verification drivers by `change_type` — a property of *which files a diff touches* — rather than by where a user encounters the behavior. `backend → curl`, unconditionally.

**Evidence (verified):**
- Sprint 07-13's Scenario A — the one integration scenario, and the mechanism explicitly designed to catch composition gaps — composes four `change_type: backend` stories and therefore runs `platforms: [host]`, `curl`/`bash` only. **No artifact in that sprint drives the multi-turn Urd conversation through the real chat UI.**
- The infrastructure that would have closed this **has never worked on any commit.** `docs/acceptance-testing-runbook.md:43` documents `COMPOSE_UI_TEST_SERVER_ENABLED=true ./gradlew :desktopApp:run`. `runComposeUiTest` is called from `internal/compose-driver/.../RunApplication.kt` (a `desktopMain` dependency), but `ui-test-junit4` is declared only inside the `desktopTest` source set (`desktopApp/build.gradle.kts:33`). `git log --all -S "ui-test-junit4" -- desktopApp/build.gradle.kts` returns **exactly one commit** — the initial client commit `cebf6b6` — where it is already scoped to `desktopTest`. The documented E2E launcher has never been launchable, in the repo's entire history.
- The "golden path E2E" (`ComposeDriverGoldenPathTest.kt`) imports `org.junit.Test`, builds its own throwaway `Box`/`OutlinedTextField`/`Button` composition, and asserts against that — it tests the driver library, not Nornspun. And it never runs: `useJUnitPlatform()` with no vintage engine silently discovers zero JUnit4 classes. This is the *third* sprint in which a suite was green because it did not execute.
- The **Definition of Done** (`docs/planning-artifacts/epics.md`) has seven items — ACs pass, unit tests, integration tests, lint, structured logging, PR review, AC reconciliation. **None requires the feature to be reachable from the application's entry point.** Verified by direct read. A story satisfies all seven while shipping dead code, and `SilenceToggle`, the settings screen, and desktop adventure upload each prove it.

This is the planning lens's mechanism, and it is correct. I restate it structurally because the lever differs: the defect is not "we plan the wrong unit," it is "we route verification by file layer instead of by assembled surface." Change the routing key and the planning unit is irrelevant.

---

### Cause 5 — Four completion registries, no single writer, all optimistic

**What.** `stories/index.json` (12 `review`), `sprints/index.json` (`active`/`locked`), `features.json` (mtime **Jul 13 10:55** — the morning the sprint was *planned*, seven days before it was built), and the per-story `.md` frontmatter (`campaign-init-urd-fills-canvas-from-free-text` says `status: backlog` while the index says `done`). Every historical correction has run in the optimistic direction: ASR-006 found `features.json` fictional in June; it is stale again seven weeks later.

**Why it ranks last.** This is a reporting defect. It corrupts what the developer *knows*; it does not corrupt what *ships*. And critically — **the registry was not wrong in the way the developer's complaint implies.** `features.json` has said every user-facing feature is `partial` since June 16. Nobody was told the product worked. The developer did not open the app expecting success because a tracker lied; they opened it because opening it is the only oracle that has ever worked. Fixing the tracker changes nothing about the app.

I rank this fifth deliberately, and I expect the Product Manager to rank it first. That is our central disagreement.

---

## 3. Independent verification log

Read-only throughout. Method stated for each; failures reported.

| # | Claim | Method | Result |
|---|---|---|---|
| 1 | Sprint 07-13 unmerged: backend 26 behind, client 27 behind, stories `review`, sprint `active` | `git rev-list --left-right --count` in both repos; `git worktree list`; JSON parse of `.momentum/{stories,sprints}/index.json` | **CONFIRMED.** backend `1 26`, client `0 27`; both trees on `main`; counts `{backlog:150, done:91, dropped:28, obsolete:19, review:12, parked:2}`; sprint `active`/`locked:true`, `planning: null` |
| 2 | Developer's walkthrough was a chimera (sprint client + main backend) | Python JSON parse of `20b5f62e…jsonl` and `2a45301c…jsonl`, extracting every `Bash` `tool_use` matching launch patterns | **CONFIRMED, and sharper than the corpus states.** All four launch events tabulated in §2.1. Zero backend launches from the sprint worktree in either session |
| 3 | **Verification lens #5 / §4: `backend-active-campaign-name-injection-fix` is "hollow verification — plumbing tested, outcome not"; `campaign_name` "appears in zero prompt templates"** | `git show sprint/…:src/agents/urd.py`; `git show af88f0f:src/agents/urd.py`; `git show 2eef2bf -- tests/agents/test_urd.py` | **FAILED.** Sprint branch `urd.py:189-193` consumes `variables["campaign_name"]` and appends the name. Pre-hotfix `main:190` appends only the UUID. The story's own test asserts `"Active campaign: The Ashen Coast" in result` **and** `str(campaign_id) not in result` against the *rendered prompt*. The "plumbing tested, outcome not" inference is false; the "zero prompt templates" observation is literally true but immaterial (the name reaches the assembled prompt by direct append) and describes `main`, not the shipped branch. **The corpus's single most-cited example of hollow verification is a build-identity artifact.** |
| 4 | **Comparison lens §1.1/§1.2 headline: "That is Anthropic's sentence, re-enacted" / "a check that passes for the wrong reason"** | Inherits #3 verbatim | **FAILED (derived).** The smoke test passed for the right reason. The `get_campaign` tool-call "confound" theory is unnecessary — the fix works on the branch that was tested. This is the load-bearing example in the comparison document's verification-gap and circular-validation sections |
| 5 | Adventure upload URL bug; no test can see it | `grep -n baseUrl NornApiClient.kt`; `grep include_router main.py`; `grep APIRouter adventures.py`; `grep -c uploadAdventure NornApiClientTest.kt` | **CONFIRMED, extended.** Client `:320` → `/campaigns/…`; all others → `/api/…`; backend mounts `/api` + `/campaigns`. Client-side coverage of `uploadAdventure`: **0**. Client tests use `localhost:1`; `grep -rl "embeddedServer\|ProcessBuilder"` → no matches. **No test in either repo crosses the process boundary** (new finding) |
| 6 | Documented desktop E2E launcher has never worked, on any commit | Read `desktopApp/build.gradle.kts` source-set blocks; `git log --all -S "ui-test-junit4"`; located `runComposeUiTest` call site | **CONFIRMED.** `internal:compose-driver` in `desktopMain`; `ui-test-junit4` in `desktopTest` only; single commit in history = `cebf6b6` (initial), already `desktopTest`-scoped |
| 7 | Golden-path E2E is synthetic and never executes | Read `ComposeDriverGoldenPathTest.kt`; read `useJUnitPlatform()` at `build.gradle.kts:43-46` | **CONFIRMED.** `org.junit.Test`; drives `Box`/`OutlinedTextField`/`Button`; JUnit5 platform, no vintage engine |
| 8 | **CI state** (not in corpus) | `ls -a` all three repos; read `ci.yml`; `git rev-list --count main...origin/main`; `git log -1 origin/main` | **CONFIRMED — NEW.** Client repo has no `.github` at all. Backend `ci.yml` line 1: `# stub — full CI pipeline implemented in D6`. Backend `main` is **23 ahead** of `origin/main`, last pushed **2026-06-11**. CI has therefore not executed on two months of `main` or on any sprint commit |
| 9 | Definition of Done has no reachability requirement | Direct read, `docs/planning-artifacts/epics.md` "Definition of Done" | **CONFIRMED.** Seven items; none mentions entry point, navigation, mounting, or user reachability |
| 10 | `features.json` frozen before the sprint it should describe | `ls -la`; `git log -- .momentum/features.json`; JSON parse | **CONFIRMED.** mtime `Jul 13 10:55`; two commits ever, latest is an *assessment* reconciliation; all MVP entries `last_verified: 2026-06-16`; 7 `partial`, 6 `not-started`, 2 `working` (both operator-facing) |
| 11 | D4.14's deliverable was built into a stale embedded repo copy and lost | `git log --all -- "**/test_session_loop_full_cycle.py"` in real backend; `git show --stat dbc8615` in hub | **CONFIRMED.** Zero hits, ever, in the canonical backend. `dbc8615` (2026-05-29): *"remove stale embedded D3.2-stub backend copy at nornspun/nornspun-backend (39 tracked files)."* Build-identity confusion is recurring, not novel to July |
| 12 | Chimera extends to the database schema (main code vs. sprint-migrated DB) | Compared `alembic/versions` on both branches; read `upgrade()` bodies of 015 and 016 | **PARTIALLY FAILED — my hypothesis, not the corpus's.** Sprint migrations 013–016 do alter `sessions` (`episode_id`, `flavor`, `name`), but **every added column is `nullable=True`**. Main's code runs against a 016-stamped DB without breaking. I went looking for a schema-level chimera failure and there isn't one. Reported because it cuts against my own case |
| 13 | Two separate maestro flow directories | `ls` both | **CONFIRMED (minor).** `nornspun-client/maestro/` and `nornspun/maestro/` both exist — a fifth duplicated source of truth, for E2E flows |

**Failures summary:** one corpus claim failed outright (#3) and one failed by inheritance (#4) — together they are the corpus's headline verification-gap example and the comparison document's lead illustration. One hypothesis of my own failed (#12). Findings #8 and the second half of #5 are new.

---

## 4. Anticipatory attacks

### 4.1 Against the Product Manager

I expect: *the unit of planning is the story, not the feature; adopt vertical slices; wire `features.json` into planning and the end-gate; gate sprints on user-observable outcomes.* The planning and backlog-economics lenses have loaded that case for you. Four objections.

**The registry already exists, already says the right thing, and was already ignored.** `features.json` has phrased every entry as "a user can do X" since 2026-05-25 and has read `partial` for every user-facing feature since 2026-06-16. It was *correct*. Nobody was misled by it. Your fix is to wire an accurate-but-unread artifact into a gate — in a system that already cannot reconcile four completion registries. You would be adding a fifth. Ask yourself why the four existing ones drifted, and you arrive at Cause 1: none of them is derived from anything mechanical.

**Your gate already fired and nothing happened.** The 07-13 end-gate defined the outcome in plain language and reported failure in its hero paragraph: *"the sprint's core promise, 'what you tell Urd gets remembered,' is not yet reliable when a real language model drives it,"* plus an 8-item "Still hollow" table and the sentence *"[approving] does not declare the memory loop trustworthy."* That is a best-in-class outcome gate. Eleven days later: unmerged, undecided, no retro, no hardening story, `planning: null`. **An outcome definition with no mechanical consequence is a poster on a wall.** Your prescription is more posters; the evidence says the wall is the problem.

**Vertical slices do not survive a chimera.** Slice the work however you like. If the acceptance walkthrough runs a July-22 client against a July-8 backend, you did not test the slice. You tested a composition that has never existed. Slicing presupposes a defined artifact — the thing that is missing.

**Your best move is one I will take from you, reframed.** The planning lens's real finding is not "story vs. feature." It is that `verification-standard.md` keys the routing table on `change_type` — a property of the diff — so a user-experienced behavior gets a `curl` driver because its code happens to live in Python. That is a structural defect in a lookup table, and it is fixable by changing the key to "where does a user encounter this" without touching the planning unit at all. Take the mechanism; drop the poster.

**What I concede to you:** the roadmap's explicit choice to cut sprints "along the backend dependency spine" and defer user-observable value to Sprint E is real, is signed, and does mean Sprint A was never intended to be usable standing alone. Nobody said that plainly to the developer at approval time. That is a genuine planning-communication defect, and it is yours.

### 4.2 Against the Super-Senior Developer

I expect: *too many agents, too much ceremony, the pipeline is theater, the runtime model is garbage, ship less process and open the app more.* Five objections.

**Ceremony is orthogonal to structure, and the ceremony produced the best artifact in the corpus.** The E2E validator ran live `SELECT count(*)` queries against Postgres, proved that Urd's confident "It is written." produced **zero rows in ~5 of 7 attempts**, reproduced a fabricated-content capture a second time to test its own hypothesis, and the Conductor recorded `NON_CONVERGENT` rather than burning iterations to force green. Strip the ceremony and you delete the only layer that has ever caught a deep defect — and you still have two repos with no contract, no CI on the client, and a `main` two months unpushed. **Ceremony is not why the app doesn't work. Ceremony is why anyone knows it doesn't.**

**"Just write more tests" is refuted by the test volume that already exists.** `tests/routers/test_heroes.py` is 338 lines. `tests/routers/test_adventures.py` is 478 lines. Both cover endpoints with **zero client callers**. Meanwhile `uploadAdventure` — the one endpoint a user actually needs — has zero client tests and a URL typo that has never worked. The constraint is not test *volume*, it is test *location*: every test in both repositories is intra-process, so tests on either side carry exactly zero information about the seam. Doubling either side's coverage moves nothing.

**"Trust the human walkthrough" is your strongest card and it has a hole in it.** Yes: every manual walkthrough in four months found the top bugs within minutes, and the automated layers didn't. But look at what the 2026-07-31 walkthrough actually produced — a **wrong diagnosis**, a **duplicate fix committed straight to `main` outside every process**, and a **manufactured merge conflict** that made the stranded sprint harder to land. The cheap human oracle is real and undervalued, and it was pointed at a chimera, so it emitted a confident falsehood. **Cheap oracles need a defined artifact just as badly as expensive ones do.** Give me one reproducible launch command and I will agree with you about almost everything else.

**"The runtime model is the problem" over-indexes on the most interesting failure.** The D5/D6 capture-integrity cluster — 5-of-7 silent losses, a persisted session containing a different campaign's fabricated narrative, on a ~$0.06/M-token OpenRouter model — is genuinely the most technically interesting thing in this corpus, and I expect you to lead with it. It explains capture *reliability*. It does not explain the desktop upload button that doesn't exist, the settings gear that has been `{}` for three sprints, the conversation history that never loads, the 404 on every upload, or 26 commits sitting on a branch. Those are the "simplest things" the developer couldn't do.

**What I concede to you:** the corpus's own numbers say the backend spine largely works — 14/20 randomly-sampled `done` stories reachable, 0/20 fabricated, PDF ingestion citing an NPC by name, Verdandi reading real living memory. This is not a "nothing was built" story. My thesis explains why what was built cannot be reached, trusted, or shipped — **not** that it doesn't exist. Anyone arguing wholesale fraud is wrong, and the evidence is on your side of that one.

### 4.3 Against my own seat

**Structure does not explain D5/D6.** A perfectly assembled, perfectly contracted, perfectly CI-gated nornspun would still have a cheap language model narrating "It is written." over zero database rows. That is a product-architecture problem (tool-call reliability, transactional write receipts, no read-back verification after a save) and arguably a model-selection problem. It is the single largest product defect in the corpus and my thesis does not cover it. I will not pretend otherwise.

**I looked for a schema chimera and did not find one** (verification #12). Every sprint-added `sessions` column is nullable; main's code tolerates a 016-stamped database. When I pushed the structural story past where the evidence went, it broke. Noted.

---

## 5. Prescription

Diagnosis and prescription are separate. Everything below is startable Monday and none of it requires a new skill, agent, or process document.

### Next 30 days

**1. Monday morning, before anything else: land or abandon sprint-2026-07-13. Today.**
Merge `sprint/sprint-2026-07-13` → `main` in both repos. The backend needs a real merge (not fast-forward) because `ab2e579` sits on `main`; resolve `urd.py`/`verdandi.py` by keeping **one** implementation and deleting the other — either is fine, *deciding* is the point. Then `git push` both repos. Then remove the `.conduct-wt/*/INTEGRATION` worktrees. Then transition the 12 stories out of `review`. Cost: a few hours. This single act removes the chimera, un-strands 53 commits, and makes every subsequent observation about the app meaningful. Nothing else on this list matters until it is done.

**2. Build one command that *is* the product.**
A `mise` task in the planning hub that: starts the database, runs `alembic upgrade head`, starts the backend from an explicit commit, builds and launches the desktop client from an explicit commit, and writes both SHAs to stdout and to `RUNNING.json`. **Rule with teeth: a walkthrough that did not start with that command is inadmissible as evidence, and every bug report cites the two SHAs.** This is the smallest possible artifact that gives the word "product" a referent. It is also the prerequisite for the developer's own cheap-oracle taste-testing to stop producing false diagnoses.

**3. Generate the client's HTTP surface from the backend's OpenAPI.**
Not full codegen — one generated `Routes.kt` of path constants, plus a check that every URL string literal in `NornApiClient.kt` resolves to one of them. This permanently kills the upload-404 defect class and converts "9 orphaned backend routes" from an archaeology finding into a number printed on every build. Half a day of work against the seam where 100% of the reachability defects live.

**4. Turn CI on in the client repo; un-stub it in the backend; push both on every merge.**
Client: build + `desktopTest` + `shared:desktopTest` + `composeApp:testDebugUnitTest`, with a hard **minimum-executed-test-count assertion per module** — the silent-skip class has now shipped green in three consecutive sprints and human review caught it every time, which means it will eventually not be caught. Backend: require the existing `ci.yml` green before merge. `origin/main` being two months stale means CI is currently decorative regardless of its contents.

**5. Make the end-gate's terminal state a merge, not a report.**
The gate does not complete until `git merge` + `git push` + story transitions have executed. If it cannot merge, it **fails** and says so. An approved gate that leaves 26 commits stranded is not an approval, and the practice should refuse to call it one. This converts the least-automated step in a fully-automated pipeline into the automated one.

**6. Collapse four completion registries to two derived ones.**
`stories/index.json` becomes derived from git (merged to `main` = `done`; nothing else may set it). `features.json` becomes writable **only** by a walkthrough of the assembled artifact from prescription #2. Delete the per-story `.md` status field and the sprint-level story mirror. A registry that is not derived from something mechanical will drift; both of these have, twice, always optimistically.

### Structural, beyond 30 days

- **Re-key the verification routing table** from `change_type` (which files a diff touches) to *assembled surface* (where a user encounters the behavior). A backend story whose behavior is only observable in the chat UI routes to a client-driving driver, or the story is not verifiable and should say so out loud at plan time.
- **Add reachability to the Definition of Done.** One item: *"the capability is reachable from the application's entry point by a user who has read no code."* This one line retires `SilenceToggle`, the settings gear, desktop upload, and the empty `SurfaceType` as a *class*.
- **Fix, or formally retire, the desktop E2E path.** Either move `ui-test-junit4` to `desktopMain` so the documented launcher works, or delete the runbook line and the synthetic golden-path test and declare desktop human-verified-only. What must stop is documenting a command that has never worked on any commit.
- **Treat runtime agent reliability as product architecture, not prompt tuning.** D5/D6 wants a transactional write receipt: Urd does not get to say "It is written" until a read-back confirms rows exist. That is a design change, and it is the one item on this list my structural thesis does not reach.

---

## 6. Falsifiability

What would prove me wrong, in descending order of decisiveness:

1. **Re-run the 2026-07-31 walkthrough with *both* halves on `sprint/sprint-2026-07-13`.** If "the agent doesn't know what campaign I've chosen" still reproduces on desktop, my centerpiece collapses, the verification lens's "hollow verification" reading is right after all, and the Product Manager's case strengthens enormously. This is one hour of work and it should be run before this council's synthesis is written.
2. **Land prescriptions #1 and #2 — merge, push, one launch command — and have the developer walk the app.** If they still say "I can't do the simplest things," structure is not the binding constraint and the Super-Senior Developer's product-quality framing or the PM's slicing framing should take precedence over mine.
3. **Run a contract check across the seam.** If the only defect it finds is the one upload URL, then Cause 2 is a single bug rather than a structural void, and it should drop below Cause 5.
4. **Evidence that the developer knowingly ran `main` as a deliberate pre-sprint baseline.** If the chimera was intentional and understood, then finding #2 collapses from "identity chaos" to "process in flight," and the false-diagnosis chain in §2.1 becomes a one-off communication error rather than a structural signature. I found no such evidence in the transcript, but I did not read all 16 sessions in full.
5. **A green run of the documented desktop compose-driver E2E on any historical commit.** My "never launchable" claim is scoped to the documented `:desktopApp:run` path and rests on a `git log --all -S` search plus source-set reading. A passing transcript against the real app would falsify it.

---

## 7. The line I want on the record

The developer asked whether the practice optimizes for stories instead of functionality. It does — but that is a symptom, and the standard fixes for it (define outcomes, slice vertically, wire the feature registry into the gate) all quietly assume something nornspun does not have: **a thing you can point at and call the product.**

For four months, that thing has been assembled by hand, differently each time, from two repositories that have never been required to agree, never been proven to compose, and never been pushed anywhere a second machine could see them. The most sophisticated multi-agent verification pipeline in this corpus was pointed at that ambiguity and produced a confident false finding. So did the audit of the pipeline. So did the comparison against the field. So, very nearly, did this council.

Give the word "product" a referent. Then define outcomes against it.
