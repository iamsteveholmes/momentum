# The Machine Has No Output Shaft

**Date:** 2026-08-02
**Seat:** The Super-Senior Developer (adversarial)
**Council:** Nornspun Delivery Discovery — Round 1 position paper

---

## Thesis

**The product did not fail to get built. It failed to get *shipped* — because Momentum made
"merge to main" a single manual `<ask>` at the terminal end of a multi-day pipeline, and then
spent the developer's entire attention budget upstream of that ask.** Trunk in the client repo
has not moved since 2026-07-08. Fifty-three commits of finished, reviewed, tested work sit on
branches nobody merged. The developer opened the app on 5 days out of 54 and found top-priority
bugs within minutes on every one of them. Meanwhile the practice repo took 1,702 commits and
booked 215 "done" stories — more finished stories than the product it exists to serve.

That is not a planning defect, a spec defect, or an architecture defect. It is a **drivetrain
defect**: an engine with excellent instrumentation, a beautifully honest dashboard, and no
connection to the wheels.

And the proof is the one thing that *did* reach trunk. On 2026-07-31T04:34:47Z the developer
said "the agent doesn't know what campaign I've chosen." At 2026-07-31T05:00:29Z a fix was on
`main`: four files, +111/−4, including the outcome-level test the governed story never wrote.
**Twenty-five minutes and forty-two seconds, with the entire practice bypassed** — no story, no
plan gate, no coverage contract, no AVFL, no end-gate. The identical fix, produced correctly by
the practice nine days earlier, is *still* stranded on a branch as I write this.

The practice's own escape hatch out-delivered the practice by a factor of roughly 500.

---

## Ranked diagnosis

I am naming one load-bearing cause. The other four are real and I can evidence all of them, but
they are downstream, and fixing them without fixing #1 changes nothing.

### 1. LOAD-BEARING — Delivery is a manual terminal step gated on the system's scarcest resource

`skills/momentum/skills/conductor/workflow.md:2593`:

> `<ask>The end-gate report is open in the viewer. Review each section. Acknowledge any decision
> cards in §04. Then approve to merge to main, or request changes.</ask>`

Five lines later, at `:2598`, the merge sequence begins: `git checkout main`. **Everything that
makes the product real sits behind that one prompt.** There is no expiry, no retry, no
re-prompt, no daemon, no "merge if green after N hours." If the human does not answer, nothing
ships — forever.

On 2026-07-22T16:38:28Z the developer's session ended mid-app-launch. Nothing has shipped since.

Verified state, 2026-08-02:

| Check | Backend | Client |
|---|---|---|
| `git rev-list --left-right --count main...sprint/sprint-2026-07-13` | `1  26` | `0  27` |
| `git merge-base --is-ancestor sprint/... main` | FALSE | FALSE |
| `main` HEAD | `ab2e579` (2026-07-30, the ungoverned hotfix) | `704e63c` (2026-07-08, "Merge branch 'sprint/sprint-2026-06-18'") |

The client's trunk is **25 days stale**. Its most recent content is the *previous* sprint. The
backend's trunk contains exactly one thing from this sprint's problem space, and it got there by
going around the practice.

`.momentum/sprints/index.json` still reads `status: "active"`, `locked: true`,
`retro_run_at: null`, `planning: null`. All 12 stories read `status: "review"`.

**Why this is load-bearing and not just one cause among five:** every other failure mode in this
corpus produces *recoverable* damage. A weak spec produces a wrong feature you can fix. A missing
E2E test produces a bug you find later. A stalled merge produces **zero delivered capability
regardless of how well everything upstream performed** — and everything upstream performed. The
backend on the sprint branch is +6,993/−202 lines of real, reviewed, tested code. It might as
well not exist.

And the counterfactual is *in the corpus*: sprint-2026-06-18 merged. Its merge commit is the
client's current trunk. The difference between the sprint that delivered and the sprint that
didn't is not process quality — 07-13 had *better* verification — it is that in July the
developer happened to be in the chair when the ask fired, and in August they weren't.

**A delivery system whose success depends on a human being awake at a specific unpredictable
moment is not a delivery system. It is a lottery.**

---

### 2. The apparatus became a second product, and it outcompeted the first for the only builder

This is why nobody answered the ask. Attention is the binding constraint, and it was spent.

Verified commit counts (`git log --all`, per month):

| Month | momentum (practice) | nornspun (planning hub) | backend | client | **process : product** |
|---|---|---|---|---|---|
| 2026-04 | 597 | 196 | 42 | 95 | **5.8 : 1** |
| 2026-05 | 399 | 144 | 7 | 31 | **14.3 : 1** |
| 2026-06 | 347 | 67 | 19 | 44 | **6.6 : 1** |
| 2026-07 | 139 | 96 | 49 | 64 | **2.1 : 1** |
| **Total** | **1,489** | **503** | **117** | **234** | **5.7 : 1** |

Verified inventory:

| | Momentum (the practice) | Nornspun (the product) |
|---|---|---|
| Stories tracked | **537** | 302 |
| Stories `done` | **215** | 91 |
| Completed sprints | **21** (+9 quickfix dirs) | 8 (+1 stuck) |
| Commits (all refs) | **1,702** | 553 hub + 364 product |
| Markdown | 36,413 lines of skill code | 128,314 lines of planning docs |

Set against **~22,000 lines of actual product** (10,466 Python in `nornspun-backend/src`,
11,590 non-test Kotlin in `nornspun-client`). The story *specifications* alone — 229 files,
44,540 lines — are **twice the size of the entire shipping codebase**.

The tool built to accelerate the product has shipped 2.4× the product's finished stories. In
May 2026 the practice took 543 commits while the product took 38.

And here is the behavioral consequence, which is the single most damning number I found. Across
the whole transcript corpus (2026-06-09 → 2026-08-01, ~54 days), I extracted every `tool_use`
block issuing `desktopApp:run`, `installDebug`, or `maestro test` from the developer's sessions:

**5 distinct days. Jul 7, Jul 8, Jul 13, Jul 22, Jul 31.**

That is it. Four months of development, ~54 days of tracked sessions, and the founder started
their own application on five of them — every one of them an end-gate or a post-build review,
never a Tuesday. On **every single one of those five days**, opening the app produced concrete,
correct, top-priority bug reports within minutes: "clicking that did nothing," "it had no idea
which campaign I was in," "when I chose choose new campaign... it didn't allow me to go back,"
"the agent doesn't know what campaign I've chosen."

The cheapest, highest-yield diagnostic in the entire system was run five times in fifty-four
days, because the developer's time went into producing and reading the documents instead.

---

### 3. Verification routes by code layer, never by user surface — and the one harness that would drive the real app has never worked, on any commit, ever

`verification-standard.md` maps `change_type: backend → curl`. The keystone conversational
stories were typed `backend`, so the sprint's one integration scenario was driven entirely by
`curl`. Nobody drove a conversation through the chat UI.

Worse — and I verified this by reading the source, not by trusting the corpus:

`desktopApp/src/desktopTest/kotlin/ComposeDriverGoldenPathTest.kt` does not test Nornspun. It
calls `setContent { Box { OutlinedTextField(...); Button(...) } }` — it builds a throwaway
three-widget composition and drives *that*. It is the "golden path E2E."

And it never executes. It is an `org.junit.Test` class. `desktopApp/build.gradle.kts:45` sets
`useJUnitPlatform()`; the test dependencies are `kotest-runner-junit5`; and `grep -rn "vintage"`
across the repo returns **zero**. A JUnit4 class under JUnit Platform with no vintage engine is
silently never discovered. The repo's own KDoc admits this failure mode elsewhere.

Meanwhile `ui-test-junit4` is declared only inside `val desktopTest by getting` — the test
classpath — so the documented launcher (`COMPOSE_UI_TEST_SERVER_ENABLED=true ./gradlew
:desktopApp:run`) cannot load `runComposeUiTest` and crashes with `NoClassDefFoundError` on
every commit in the repo's history.

**In four months, this practice has never once driven the real desktop application through a
scripted user journey.** The "held-out test" was always a human, and the human ran five times.

---

### 4. The per-story record is clean when the capability is broken — that is the machine that manufactured "91 done"

The corpus's headline consolation is "the pipeline told the truth." It did — *at the sprint
level*. At the story level it lied, and the story level is where the number 91 comes from.

Verbatim from `build-ledger.jsonl`:

```
story-terminal  session-naming-two-message-close   outcome=merged  findings_summary=[]  escalations=[]
story-terminal  urds-post-session-capture          outcome=merged  findings_summary=[]  escalations=[]
```

Then, from the same ledger, minutes later:

```
coverage-deferral-undischarged  urds-post-session-capture
  "AC3 durable persistence FAILS — fresh conversation reports no sessions after
   confident close; DB count 0 confirms"
coverage-deferral-undischarged  session-naming-two-message-close
  "AC4 two-message rhythm unreliable... AC1/AC3 persistence unconfirmable due to
   silent bind failure"
```

A completely clean terminal record for a story whose core acceptance criterion the very next
phase proved failing against a live database. That clean record is what a status dashboard,
a retro, and a mission brief all read.

The archetype is older than this sprint. `d4-14-end-to-end-session-loop-integration-test`:
`status: done`, `priority: high`, epic `session-loop`. All four of its `depends_on` entries are
dangling — verified by direct lookup against the live index. And its sole deliverable:

```
$ cd nornspun-backend && git log --all --oneline -- '*test_session_loop_full_cycle*' | wc -l
0
```

The story that claims to prove the end-to-end session loop works has never had a file in the
repository that runs. `tests/integration/` contains exactly one file, and it is about something
else. That story has been `done` for four months.

---

### 5. Things get built and never connected, because nobody uses the product, so nothing forces the connection

The corpus says "no hero-persistence tool exists at all." That claim fails verification, and the
truth is worse.

Verified: `src/routers/heroes.py` exposes GET/POST/PATCH on `/campaigns/{campaign_id}/heroes`.
`HeroRepository` exists. `src/agents/hero_context.py` assembles a `## Party Heroes` block for
the prompt. The backend for hero persistence is *built*.

Also verified: `grep -rn "heroes\|Hero" --include='*.kt'` across the client returns **three
hits, all comments** saying the heroes stat was removed from the campaign card. Zero API calls.
And Urd's registered tool list — `create_campaign`, `update_campaign`, `get_campaign`,
`list_campaigns`, `save_session_events`, `update_npc_encounters`, `record_divergence`,
`bind_memories`, `get_session_history` — contains **no hero-write tool**.

A complete API, a repository, and a prompt assembler, with no caller on either side. The
`heroes` table has been empty for the database's entire life.

Same shape, different feature: `campaign_name` is computed in `urd.py` and appears in **zero**
files under `src/prompts/` (verified grep). Computed, never interpolated. That is the bug that
cost the developer two end-gates and generated a full sprint story — and it is six lines.

This is what four months of building without using looks like: 0 heroes, 0 adventures,
0 recaps, 0 divergences, 1 seeded session. **You cannot find integration bugs in a system nobody
integrates with.**

---

## Independent verification log

Everything below was re-checked by me against raw sources. The corpus was written by audit
agents; I assumed nothing.

| # | Claim | Method | Result |
|---|---|---|---|
| 1 | Sprint 07-13 unmerged in both repos | `git rev-list --left-right --count`, `git merge-base --is-ancestor`, `git log -1 main` in both repos | **CONFIRMED.** backend `1 26`/FALSE; client `0 27`/FALSE. Client trunk dated 2026-07-08. |
| 2 | 302 stories / 91 done / 12 review | Python parse of `.momentum/stories/index.json` | **CONFIRMED** exactly: `{backlog:150, done:91, dropped:28, obsolete:19, review:12, parked:2}` |
| 3 | The merge is behind one human ask | `grep` conductor `workflow.md` | **CONFIRMED.** Ask at `:2593`, `git checkout main` at `:2598`. No expiry/retry mechanism found. |
| 4 | The hotfix was ungoverned and on `main` | `git show --stat ab2e579` + full diff | **CONFIRMED.** 4 files, +111/−4, direct to `main`, no story/branch/gate. Includes the rendered-prompt assertion the governed story lacked. |
| 5 | Complaint→fix elapsed time | Transcript timestamp of the user message in `20b5f62e` vs. commit date of `ab2e579` | **CONFIRMED, and sharper than the corpus states.** Complaint `2026-07-31T04:34:47Z`; commit `2026-07-30 22:00:29 -0700` = `2026-07-31T05:00:29Z`. **25m 42s.** |
| 6 | `campaign_name` in zero prompt templates | `grep -rn campaign_name src/prompts/` | **CONFIRMED.** Zero hits. (Templates: `urd_system.md`, `verdandi_system.md`, `skuld_system.md`.) |
| 7 | The golden-path E2E is synthetic and never runs | Read `ComposeDriverGoldenPathTest.kt`; read `desktopApp/build.gradle.kts`; `grep -rn vintage` | **CONFIRMED.** Drives its own `Box`/`OutlinedTextField`/`Button`. `org.junit.Test` + `useJUnitPlatform()` (line 45) + kotest-junit5, zero vintage-engine hits repo-wide. `ui-test-junit4` is in `desktopTest` only. |
| 8 | `features.json` orphaned from planning | `grep -rn features.json` across the whole `sprint-planning` skill (workflow.md, SKILL.md, 20 evals), then all 30 skills | **CONFIRMED, worse than stated.** Zero hits in sprint-planning. Repo-wide, hits only in `feature-status` evals — a skill whose own description reads "Deprecated... outputs a deprecation message and halts" — plus one `create-story` eval. |
| 9 | E2E genuinely caught severe bugs (counter-evidence to my own seat) | Parsed all 156 lines of `build-ledger.jsonl` | **CONFIRMED, and it is real.** INTEG-001 phantom sessions, `stakes_class: high-blast-radius-architecture`, escalated with mechanism and options. A `conductor-warning` records a deliberate refusal to burn iterations forcing green. This is not theater. |
| 10 | The end-gate report is honest | Read `sprint-2026-07-13-endgate-report.html` (460 lines) | **CONFIRMED.** Leads with "the sprint's core promise... is not yet reliable." Also confirmed the self-contradiction: "0 blocked / broken stories" in the same header. |
| 11 | Story-terminal records clean while ACs failed | Parsed `story-terminal` and `coverage-deferral-*` events | **CONFIRMED.** Two stories `findings_summary=[] escalations=[]` then `AC3 durable persistence FAILS — DB count 0 confirms`. |
| 12 | Critical self-fixes never built | Index lookup of the three 05-01 retro stories + all `impetus-core` | **CONFIRMED.** All three `critical`/`backlog`. impetus-core: 29 stories, 24 backlog, 5 obsolete, **0 done.** |
| 13 | d4-14 "done" with no deliverable | Index lookup + `git log --all` in backend + `ls tests/integration/` | **CONFIRMED.** `done`/`high`, 4 dangling deps, 0 commits ever for `test_session_loop_full_cycle`, `tests/integration/` has one unrelated file. |
| 14 | Heroes have no persistence path | `ls src/tools/`, `grep hero` across backend and client, read Urd tool registrations | **CORPUS CLAIM PARTIALLY FAILS — see below.** |
| 15 | Developer app-launch frequency | Python scan of all 16 transcripts for `tool_use` blocks containing `desktopApp:run`/`installDebug`/`maestro test`, grouped by date | **NEW FINDING.** 5 distinct days (Jul 7, 8, 13, 22, 31) across a 54-day corpus; subagents on 3 days. |
| 16 | Practice-vs-product volume | `git rev-list --count --all` × 4 repos; `wc -l` over source and markdown trees; parse of momentum's own `.momentum/` indexes | **NEW FINDING.** Momentum: 1,702 commits, 537 stories, 215 done, 21 completed sprints. |
| 17 | "couldn't do even the simplest things" is verbatim | `grep -ril "couldn't do"` across all 16 transcripts | **CONFIRMED ABSENT** (0 files). The brief's framing is a paraphrase, as cartography said. |

### Corpus claims that failed my verification

**F1 — The 07-13 dossier misdates the decisive walkthrough by two days, and the error hides the
paper's own best evidence.** The dossier states (exec summary #5, §5) that the developer drove
the app on **2026-08-02**. The actual transcript timestamps in session `20b5f62e` are
`2026-07-31T04:28:26Z` and `2026-07-31T04:34:47Z` (= Jul 30 evening PDT). The cartography got
this right; the dossier didn't. **Why it matters:** the dossier presents the hotfix as a separate
later event. It wasn't — it landed 26 minutes after the complaint, in the same session. The
dossier's own headline finding is stronger than the dossier realized.

**F2 — "No hero-persistence tool exists at all" is wrong on mechanism.** The verification lens
(§5, echoed by the comparison doc §1.3) bases this on a grep of `src/tools/`. But
`src/routers/heroes.py` (GET/POST/PATCH), `HeroRepository`, and `src/agents/hero_context.py` all
exist. The grep was scoped to one directory. The *conclusion* (heroes never persist) holds; the
*mechanism* is not absence but **zero callers on either side** — which is a more damning finding
for the practice, because it means the work was done, reviewed, marked done, and never wired.

**F3 — The retro-loop lens says the stories are stuck "three-plus months after end-gate."** The
end-gate was 2026-07-22 and today is 2026-08-02. Eleven days. Its own body says so. A stray
exaggeration in an executive summary, but it is the kind of number that gets quoted onward.

**F4 — The planning lens's "21 planning commits" is 20 across all refs** (8 on the default
branch) in the 2026-07-13 window. The substantive claim verifies precisely: `fb7eed0` at
10:56:02 → `7da4789` at 12:25:22 = **89 minutes 20 seconds**. Count slightly off, conclusion
sound.

**F5 — The mission brief's own framing is wrong twice.** "End-gate approved" for 07-13 is false:
no decision record exists anywhere, and the sprint is still `active`/`locked`. And the "91 done"
figure, while literally in the index, includes at least one story (`d4-14`) whose deliverable has
never existed in the repository that runs.

---

## Anticipatory attacks

### Against the Architect

You will say: horizontal decomposition, no walking skeleton, integration risk deferred to the
end, seam contracts, vertical slices, a proper test pyramid. You will produce a diagram.

**Attack 1 — the skeleton already exists, verified live.** Ground truth started the backend on
`main` and drove it: health, campaign list/create, SSE chat with both Norns, conversational
campaign creation writing a real DB row, Verdandi reading real living-memory events, PDF upload
→ ingestion → chunking → retrieval → Verdandi citing "Ser Marrow" by name. The desktop client
builds clean, launches, renders, and its production `ChatViewModel` completes a live round trip
in ~2 seconds. **You are prescribing foundation work for a building that is standing.**

**Attack 2 — none of the top defects yield to structure.** The three worst product findings are:
a ~$0.06/M-token model failing to call its save tools; a variable computed and never
interpolated into a template; a screen with no back button. There is no architecture that catches
a missing back button. A human opening the app catches it in ninety seconds, and did — four
separate times, in four minutes of cumulative effort, at zero cost.

**Attack 3 — this project's problem is that its existing structure does not execute.**
`.claude/rules/e2e-validation.md` already mandates "Silent failure classifies as FAIL, not PASS."
That is your prescription, already written, already ratified. It never fired, because the
launcher it depended on has never been launchable on any commit in the repo's history. This
codebase carries 36,413 lines of skill markdown and 128,314 lines of planning markdown against
22,000 lines of product. **Structure that cannot execute is decoration, and this project is
already drowning in decoration.**

**The one thing I concede to you:** the verification routing table keying on `change_type`
instead of user surface is a genuine structural defect with a genuine structural fix. It is one
table. Make that edit and stop. If your paper is longer than that table, it is part of the
problem it describes.

### Against the Product Manager / outcome-metrics seat

You will say: output vs. outcome, feature factory, wire `features.json` into the gates, adopt
failing-by-default feature acceptance, instrument user capability.

**Attack 1 — the developer already had an honest outcome scorecard and it changed nothing.** On
2026-07-22 they were handed a 460-line report that led with "the sprint's core promise... is not
yet reliable when a real language model drives it," containing an eight-row *"Still hollow"*
table and six decision cards, three of them about the exact defect that later ruined their
walkthrough. Result: no decision, no merge, no retro, no story. **Adding a seventh honest
instrument to a system whose failure mode is that nobody acts on the six it has is not
measurement. It is furniture.**

**Attack 2 — `features.json` is a live demonstration of your own failure mode.** It exists. It
is correctly worded ("A developer can describe the outcomes of a game session to Urd in 10
conversational turns and see living memory updated..."). It has gone stale twice, both times
optimistically. And I verified the only skill in the entire 30-skill catalog that references it
is **deprecated and halts on invocation.** You are proposing to build a thing that already
exists, in the exact form you want, and that has already failed in exactly the way I predict
your new one will.

**Attack 3 — your registry needs a green light it cannot get.** "A feature is failing until a
journey check flips it" requires a journey check. There has never been one on desktop, and the
harness that would provide one has never started. Without it, your registry is a JSON file that
is permanently red — which is indistinguishable from a JSON file nobody reads.

**Attack 4 — with one developer and zero users, outcome metrics have no coordination function.**
Metrics exist to align many people around a goal none of them can see whole. There is one person
here. He can see the whole thing by double-clicking an icon. The only honest outcome metric in
this system is *"I opened the app today and it annoyed me."* That instrument costs nothing, has a
100% hit rate across every one of the five occasions it was used, and was used five times in
fifty-four days. **Fix the usage rate, not the instrumentation.**

### Against myself — the counter-evidence I have to eat

My seat's instinct is "delete most of the apparatus." On this evidence that is wrong for at least
four components, and I verified each of them:

- **The E2E validator is genuinely good.** It ran live `SELECT count(*)` against Postgres, proved
  Urd's confident "It is written." produced zero rows in ~5 of 7 closes, found a capture holding
  a *different adventure's* content, and then ran a second reproduction specifically to test its
  own hypothesis and flagged that the discriminating test hadn't been run. That is better
  investigative discipline than most human QA organizations.
- **The fresh-context adversarial code reviewer earns its seat.** It caught the kotest-migration
  story's own named proof-case still silently skipped — the exact defect class the story existed
  to end — which stayed green because *other* tests ran.
- **The Conductor's NON_CONVERGENT discipline is right.** It recorded a failure state rather than
  burning three more validator iterations to manufacture a green score. Most teams cannot do this.
- **The end-gate honesty format is real.** "Approving does not declare the memory loop
  trustworthy" is a sentence almost no process ever writes about itself.

So the honest version of my position is not *delete the apparatus*. It is: **the diagnostic
organs work; the motor organs do not exist; and the diagnostics are consuming the fuel the motor
needs.** These four components report to an executive function that has been stalled for eleven
days and a trunk that has been stalled for twenty-five.

I also concede that "merge to main daily" is not free in this shape: two product repos plus a
planning hub, integration worktrees, and a flagship defect that is *runtime model unreliability*,
not code. Daily merge is still right, but naked daily merge just moves the breakage to trunk
faster. It needs one green check attached, and that check has to be on the platform where the
practice's harness has actually driven the real app — Android — not the one where it never has.

---

## Prescription

### Next 30 days — start Monday morning, in this order

1. **Before reading anything else: merge or delete.** `git checkout main && git merge
   sprint/sprint-2026-07-13` in both repos, or delete both branches and accept the loss. Do not
   re-open the end-gate report first. Fifty-three commits of finished work have been in limbo for
   eleven days; the decision cost of continuing to defer now exceeds the risk of merging
   imperfect code. Then `git worktree remove` the two `.conduct-wt/INTEGRATION` trees so there is
   exactly one checkout per repo and "which build is the app" stops being a question.

2. **Invert the conductor gate — a three-line change at `workflow.md:2593`.** Green build merges
   to `main` automatically; the human's ask becomes *"revert?"*, not *"approve?"*, and it does
   not block. Silence must mean ship, not stall. This single edit removes the only single point
   of failure in the entire delivery path, and it is smaller than the report it replaces.

3. **Write `./run.sh` in each product repo, today.** `nornspun-backend/README.md` is zero bytes;
   Docker Desktop is broken on the machine; the finch containers were created four months ago.
   One script: start the db, start uvicorn, start the desktop app. If it doesn't come up, that
   *is* the bug and it outranks every story in the backlog. Ten minutes of work that has not been
   done in four months.

4. **Ten minutes of tasting, every working day, before anything else.** Open the app. Do one
   thing — create a campaign, chat, close a session. Every annoyance goes as one line into a
   single file, `BROKEN.md`. That file is the backlog for the next 30 days. No slugs, no Gherkin,
   no epics, no index. The evidence for this is not ideology: five walkthroughs in four months
   produced five for five hit rates on top-priority defects, and they are the only mechanism in
   this entire corpus with that record.

5. **One green end-to-end check, on Android, on every merge.** Maestro is the only harness in
   this practice that has ever driven the real application. One flow: create campaign → chat →
   capture → assert a `session_events` row exists. It fails today; that is the point. Desktop
   stays human-tasted until someone decides whether a Compose desktop driver is worth building at
   all.

6. **Freeze Momentum for 30 days. Zero commits to the practice repo.** This is the only
   experiment that can falsify cause #2, and it costs nothing to run.

### Structural — after the 30 days, and only if the tasting log justifies it

- **Decide about desktop E2E, then act.** Either move `ui-test-junit4` to `desktopMain` and add
  `junit-vintage-engine` so the JUnit4 classes actually run, or delete
  `ComposeDriverGoldenPathTest.kt` and remove the desktop E2E claim from
  `acceptance-testing-runbook.md`. What is not acceptable is a documented capability that has
  never worked on any commit.
- **Re-key verification routing on user surface, not `change_type`.** One table in
  `verification-standard.md`. A story a user meets in the chat UI gets driven through the chat
  UI, regardless of which files it touches.
- **Collapse to one status system.** There are currently four disagreeing records for the same
  twelve stories. Whichever one the build writes wins; delete the other three. A status that no
  automated step writes is a status that will lie.
- **Cap the backlog at 30 items and delete the rest.** 150 backlog + 28 dropped + 19 obsolete =
  197 items of inventory nobody will ever pull, carrying 44,540 lines of specification. That is
  not an asset; it is a maintenance liability that has already produced phantom slugs and
  dangling dependencies.

---

## Falsifiability

I would be wrong, and would say so, if:

1. **The branches get merged, the build is correctly paired, and the app still can't do the
   simplest things.** Then trunk-freeze was not the load-bearing cause and the runtime-model
   story (a cheap model failing to call its tools) is primary. This is the cheapest test in the
   whole council's prescription list and it should be run first, on Monday, before anyone writes
   another word of process.

2. **A 30-day Momentum freeze produces no measurable increase in product commits or app-run
   days.** Then attention was not being displaced, cause #2 collapses, and the case for the
   apparatus as a competitor rather than a support system fails.

3. **The 30-day `BROKEN.md` log is dominated by defects a spec or architecture review would have
   prevented** — wrong data models, incompatible contracts, structural rework — rather than by
   wiring gaps, missing affordances, and stale state. Then the Architect is right and my
   "diagnostics work, drivetrain doesn't" framing is wrong.

4. **Someone produces a transcript of a passing compose-driver session against the real desktop
   app on any commit.** My "nothing has ever driven the real app" claim collapses, and the
   verification story becomes a maintenance failure rather than a structural one.

5. **`features.json` gets wired into the gate and a sprint is measurably re-scoped as a result.**
   Then instrumentation does change behavior in a one-person system and my "metrics theater"
   attack on the PM seat is wrong. I predict it produces a red row and no re-scoping, exactly as
   it has for the last three months.

6. **The practice-vs-product commit ratio inverts on its own during a period of active product
   development.** July already shows the ratio falling to 2.1:1. If August and September continue
   that trend without intervention, the apparatus was a startup cost that is amortizing, not a
   competitor — and my second cause is a phase, not a pathology.

---

## The sentence I would write on the whiteboard

Ninety-one stories are `done`. Zero user-facing features work. The developer's own database holds
zero heroes, zero adventures, and one seeded session. Fifty-three commits of finished work sit on
branches. The client's trunk is twenty-five days old.

And the only thing that reached trunk in that entire window took twenty-five minutes, went
straight to `main`, skipped every gate, and shipped with a better test than the governed version
it replaced.

**The practice is not failing to find problems. It is failing to be a machine that ships. And its
own escape hatch keeps proving how little of it is load-bearing.**
