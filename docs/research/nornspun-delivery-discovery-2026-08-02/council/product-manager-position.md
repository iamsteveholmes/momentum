# The Accountability Vacuum

**Council position paper — nornspun delivery discovery**
**Date:** 2026-08-02
**Seat:** The Product Manager (adversarial)
**Author's stance:** 20 years shipping consumer products. My prior is that delivery failures are
failures of outcome accountability, not engineering. I tested that prior against this evidence base
and re-verified the load-bearing claims myself. It survived, with one correction I record in §3.

---

## 1. Thesis

**Nobody — no human, no agent, no artifact, no CLI command — is accountable for the sentence "a user
can now do X." Every instrument required to hold that accountability already exists in this practice
and every one of them is wired to nothing. Ten sprints of story-level accounting therefore reported
rising throughput against an outcome number that has been zero since April, and nobody noticed,
because no process step was ever obligated to look.**

The developer's instinct — "our sprints focus on delivering stories rather than delivering
functionality" — is correct, and it is more literally true than they suspect. It is not a cultural
tendency. It is a mechanical fact you can grep for. I will show you the grep.

The single sharpest specimen, verified by me directly against source this morning:

> `nornspun-client/shared/src/commonMain/kotlin/NornApiClient.kt:320`
> ```kotlin
> url = "$baseUrl/campaigns/$campaignId/adventures",
> ```
> The backend mounts that route at `/api/campaigns/{id}/adventures`
> (`nornspun-backend/src/routers/adventures.py:49` prefix `/campaigns`, included in
> `src/main.py:45` with `prefix="/api"`). Chat and campaigns in the same file correctly use
> `$baseUrl/api/chat` (line 184) and `$baseUrl/api/campaigns` (lines 248, 282). The upload call
> is missing one path segment. It 404s. It has 404'd since commit `a39fac0`,
> **2026-04-09** — the day the story shipped. It is still broken on `main` **and** on
> `sprint/sprint-2026-07-13`.

That is the entire feature `adventure-upload`. Its only production call path. Meanwhile
`.momentum/features.json` records:

```json
"acceptance_condition": "A developer can upload a text-based PDF adventure via file picker on
  Android, and see Verdandi reference a specific named NPC from that PDF during a subsequent
  session prep conversation — without the GM having to describe the NPC manually.",
"status": "partial", "stories_done": 1, "stories_remaining": 1,
"last_verified": "2026-06-16",
"notes": "Re-verified — ASR-006 (AVFL-verified)."
```

The acceptance condition is *perfect*. It is exactly the sentence a product manager would write. The
registry reports the feature is halfway done and was re-verified two months after it broke, by an
AVFL-validated assessment. The ground-truth agent proved the entire backend half works end-to-end —
PDF upload, ingestion, chunking, and Verdandi citing "Ser Marrow" by name from the document. The
capability is **one path segment** away from working and has been for **116 days**, through 10
sprints, an adversarial code-review regime, a 16-validator AVFL apparatus, a Maestro audit that
re-classified 13 scenarios, and a formal assessment that blessed it.

Every quality instrument in this practice ran over that line of code and passed it. Not one of them
was ever asked the question "can a GM upload their adventure?" — because asking that question is
nobody's job.

That is the whole thesis. The rest of this paper ranks the causes, proves them, and attacks the two
takes I expect from the other seats.

---

## 2. Ranked diagnosis

I am asked to name THE load-bearing cause. I do, in §2.1. The rest are ranked contributors, not
co-equals: fix #1 and #2–#5 become tractable; fix #2–#5 without #1 and you get better-instrumented
failure.

### 2.1 THE load-bearing cause — the outcome instrument exists and is connected to nothing

The practice already owns a feature registry whose every entry is phrased as a user capability with
a checkable acceptance condition. It is orphaned at every layer. I verified this exhaustively
because it is a negative claim and negative claims from audit agents are where false positives live.

**What / Why it matters / Evidence:**

| Layer | Verified state | Command / file |
|---|---|---|
| Sprint planning workflow | `features.json` appears **0 times** — in the version that planned this sprint (v0.31.0, 1,258 lines), in current (v0.32.0, 1,442 lines), and in the repo source of truth | `grep -c 'features\.json'` on `.../skills/sprint-planning/workflow.md` → `0, 0, 0` |
| All Momentum skills | **0** non-eval references anywhere in `skills/momentum/skills/` | `grep -rn 'features\.json' … \| grep -v '/evals/'` → empty |
| Sprint state schema | The `active` sprint object's keys are `approvals, locked, planned, slug, started, status, stories, team, waves`. **No feature field of any kind** | `.momentum/sprints/index.json` |
| Sprint CLI | 16 `momentum-tools sprint` subcommands. All 16 operate on stories, approvals, waves, contracts, priorities. **Zero operate on features** | `momentum-tools sprint --help` |
| The one skill that read it | `momentum:feature-status` — frontmatter: *"Deprecated. Use /momentum:canvas instead. This stub outputs a deprecation message and halts."* Its replacement, `canvas`, contains **zero** references to `features.json` | `skills/momentum/skills/feature-status/SKILL.md`; `grep` over `skills/canvas/` |
| The only CLI hook | `momentum-tools feature-status-hash` — a SHA-256 cache key for the deprecated skill. It reads `_bmad-output/planning-artifacts/features.json`. nornspun's registry was `git mv`'d to `.momentum/` on **2026-05-25** (commit `e9ccdec`) and `_bmad-output/planning-artifacts/` no longer exists | `momentum-tools.py:1793, 1878` |

Run that last one and this is what the practice tells you about the state of its own outcomes:

```
$ cd ~/projects/nornspun && momentum-tools feature-status-hash
{ "action": "feature_status_hash", "success": true,
  "hash_result": { "hash": "", "features_present": false } }
```

**`"success": true` · `"features_present": false`.** The only tooling in the entire practice that
touches the outcome instrument reports success while finding nothing. I can think of no cleaner
epitaph.

And the disconnection is not for want of data. **69 of 302 stories carry a `feature_slug` field**
(`.momentum/stories/index.json`). The link from story to capability is *populated*. It aggregates to
nothing, gates nothing, appears in no report, and blocks no sprint from completing. `epics.json`
likewise carries `acceptance_conditions` arrays written as user sentences ("A Spinner can capture a
completed session with Urd, persisting it into living memory") next to a `current_state` field whose
value is — inevitably — a story count: *"in-progress — 5 stories done, 11 backlog."*

Three separate places in this system know how to phrase a user outcome. Zero places check one.

**The consequence, measured.** Story throughput per sprint of product-capability class runs
3 → 7 → 0 → 5 → 3 → 0 → 5 → 8 → 9 — rising. Features at `working`: **0 of 15** GM-facing, verified
directly against `.momentum/features.json` (statuses: 7 `partial`, 6 `not-started`, 2 `working` —
and both `working` entries are `llm-cost-tracking` and `evals`, operator tooling, not product). The
number that goes up is the number nobody cares about. The number the developer cares about has never
moved, and no artifact in the practice was ever obligated to say so out loud.

`adventure-upload` is what that vacuum produces. So is this, from the same repo:

- **`heroes`**: a full CRUD API exists (`src/routers/heroes.py` — GET/POST/PATCH). **No agent tool
  writes to it** (`grep -rn hero src/tools/*.py` → empty, on `main` *and* on the sprint branch).
  **No client caller invokes it** (grep across `commonMain` → three comments, zero call sites). Urd
  conversationally invites a player to describe their character; nothing on earth writes it down.
  Three layers built by three stories, none connected, and `campaign-init`'s acceptance condition
  ("first prep references the PC's fear") has therefore been unreachable for the product's entire
  life.
- **The client's whole API surface is three calls** — `POST /api/chat`, `POST /api/campaigns`,
  `GET /api/campaigns` — against **23 backend routes**. Twenty routes exist for nobody.
- **`CampaignPickerScreen.kt:87`: `sessionCount = 0,`** hardcoded. Every campaign card in the
  product lies about the user's own history.

None of these is a hard problem. Every one is hours of work. They persist because "hours of work" is
only spent on things someone is accountable for, and the accountable unit here is the story, and
every one of these stories is `done`.

### 2.2 The roadmap was cut along a backend spine that guarantees no capability completes for months — and the product owner signed it

I verified the roadmap text directly (`docs/planning-artifacts/mvp-roadmap-sprints-a-e-2026-07-09.md`):

> **Status:** adopted by product owner 2026-07-09
> *"Dependency spine is sequential: Store A → Store B → capture flows → prep surfaces →
> re-entry/ledger. **Sprints are cut along that spine.**"*
> Sprint A — Memory foundation · Sprint B — Capture depth · Sprint C — Prep surfaces + re-entry ·
> Sprint D — Living Memory ledger + identity · **Sprint E — MVP close-out**

The MVP gate — "Campaign init → adventure ingestion → session prep → post-session capture → living
memory → campaign identity, 'Friends & Family Ready'" — is stated at the top and scheduled to close
at Sprint E. Sprint B's ten stories are, essentially without exception, backend and agent-side work.
The first sprint that puts a *new user-visible surface* in front of a GM is Sprint C. Desktop
adventure upload — the missing UI for the feature whose URL is broken — is scheduled in **Sprint D**.

This is defensible engineering sequencing and indefensible product sequencing, and the document
never once names which capability each sprint completes. There is no feature column. There is no
"after Sprint B a GM can ___" line anywhere in it. The roadmap is a dependency graph wearing a
product roadmap's clothes.

I want to be precise about the charge, because the corpus over-states it slightly and I will not
inherit that. The roadmap does not literally defer *all* value to Sprint E; Sprint C could complete
`session-prep` and Sprint D could complete `living-memory`. What it does is defer the *first
possible* feature completion to sprint three of five — roughly six to nine weeks from adoption —
while providing no mechanism to notice if that slips, and no statement to the owner at signing time
that "for the next two sprints, nothing you can see will change."

An owner who understood that trade would still be entitled to make it. This owner was never shown
it. Which brings us to the moment where it should have been shown.

### 2.3 The product owner is inside the system, and the one gate where outcome accountability was theirs to exercise took three minutes

This is the finding I expect to be least welcome and I am not going to soften it.

I extracted every real user turn from the sprint-2026-07-13 planning session
(`cd4e9d0e-287d-4def-941e-34ca1ff47607.jsonl`) myself. Across a **seven-day**, 1,494-line session
there are **five** user messages, two of which are skill-invocation boilerplate:

```
2026-07-13T17:43:32Z  Please begin planning for this sprint. docs/…/mvp-roadmap-sprints-a-e-2026-07-09.md
2026-07-13T17:43:41Z  Invoke the momentum:sprint-planning skill and follow it exactly. …
2026-07-13T19:06:10Z  Invoke the momentum:avfl skill and follow it exactly. …
2026-07-20T21:19:41Z  [the plan-gate sign-off — full text below]
2026-07-20T21:22:30Z  Please generate a handoff for the next session to run conduct
```

Seven days of silence, then the sign-off, then a handoff request **three minutes later**. Here is
the sign-off in full — the complete product-owner input on a twelve-story keystone sprint that the
roadmap itself calls "the single highest-leverage unblock in the MVP":

> Approve the full 12-story keystone chain in one sprint? Approve as planned
> Keep campaign-picker as a verify-and-close-gaps story? Keep as the verify-and-close-gaps pass
> Sign off the greeting-trim copy direction? Adopt default copy as written
> Ratify "It is written." as the capture close line? I'm accustomed to it is bound but let's ratify
> it is written. Accept draft copy

Four defaults accepted verbatim. The single original human contribution in the entire artifact is a
**preference about a line of dialogue.**

I want to be scrupulously fair here, because this is where the practice deserves credit and the
human deserves the criticism. The anti-rubber-stamp mechanism **worked mechanically** — it forced a
written verdict per fork and one was recorded per fork
(`.momentum/sprints/sprint-2026-07-13/plan-gate-decision.md`). The failure is upstream of the
human: **every fork the gate presented was a scope-mechanics or copy question.** Not one fork asked
"what will a GM be able to do on August 1st that they cannot do today?" The gate extracted a
signature on the only questions it knew how to ask, and the owner answered them faithfully. The
system asked for taste and got taste. It never asked for accountability, so it never got any.

**And when the owner did produce genuine outcome signal, the system dropped it and the owner
ratified the drop.** I extracted the sprint-2026-06-18 end-gate session
(`8cbc4ae0-…jsonl`) directly. The sequence:

| UTC | Developer, verbatim |
|---|---|
| 2026-07-08T02:01 | *"The Desktop App came up in the Salt Road > but clicking that did nothing. And when I typed in a prompt it asked me what campaign I was in."* |
| 2026-07-08T18:09 | *"I'm kind of confused by the request changes. **I mentioned specific problems with both desktop and android but it's not clear you're looking to fix those.**"* |
| 2026-07-09T05:54 | *"END-GATE DECISION for sprint-2026-06-18: **APPROVE**. D1: Option A. D2: Option A. Proceed with merge to main and sprint closure."* |

The owner reported a user-outcome defect, explicitly observed that the fix wave was not addressing
what he reported, and approved the gate anyway eleven hours later. Three weeks later, at the *next*
end-gate, having spent an entire twelve-story sprint on the adjacent subsystem, he reports the same
symptom class: *"the agent doesn't know what campaign I've chosen. If it doesn't know the campaign
I've chosen how can it save anything to that campaign?"* (`20b5f62e`, 2026-07-31T04:34).

That is a closed accountability loop failing on both ends: the process didn't convert the owner's
observation into work, and the owner didn't withhold the signature that was his only lever.

The same pattern shows up wherever the owner's attention is the gating resource, always in the
direction of minimizing it — and always by explicit, verified request:

> *"Please run a retro, **I'd rather we run this basically in Yolo mode**. Use Sonnet agents for your
> subagents, and **get through it asap**. I want to move on to working on the next sprint. …
> **Don't present to me until their is a necessary HITL gate.**"* — `2734df5b`, 2026-07-09T18:32
>
> *"Please run the triage **in yolo mode** using sonnet subagents"* — same session, 2026-07-10T00:22

These are legitimate requests from a solo operator with finite attention. I am not moralizing about
them. I am pointing out the systems consequence: **the three phases whose entire job is to catch
"we shipped stories but not a feature" — planning, retro, and triage — were all explicitly
configured for minimum human presence, and the one activity that catches it every single time is the
one that is never scheduled at all.**

### 2.4 Tasting is the only held-out test in the system, it has a 100% hit rate, and it happens about monthly

Every automated check in this practice is a visible suite: the story wrote it, the story passes it.
The only held-out check — the only test whose content was not authored by the thing being tested —
is a human opening the app. I measured its yield directly from the transcripts:

| Walkthrough | Prompt → first defect reported | Elapsed |
|---|---|---|
| 2026-07-22 | 22:57:27 *"Please restart the apps. I'd like to see how they look"* → 23:12:13 *"Multiple things were problems…"* | **14m 46s** (including build time) |
| 2026-07-31 | 04:28:26 *"I'm supposed to run through the entire app"* → 04:34:47 *"the agent doesn't know what campaign I've chosen"* | **6m 21s** |

Roughly four to five such walkthroughs exist across four months (I verified the three July ones
directly; the corpus documents earlier ones in April and May). **Every single one found a top-tier
defect within minutes.** No other activity in this dataset has that yield. Not AVFL, not adversarial
code review, not E2E, not the 98-subagent conduct build.

And the corroborating evidence for how rarely the product is actually used is the product's own
data. The ground-truth agent found, after four months: **2 campaigns, 1 session (seeded by an
automated E2E run on Jul 22), 0 heroes, 0 adventures, 0 recaps, 0 NPC encounters, 0 divergences, 0
episodes, 0 transcript turns.** I could not independently re-query the database (Docker is broken on
the machine and I am read-only), so I treat those row counts as corpus-reported. But two of the
structural claims underneath them I *did* verify from source, and they are sufficient on their own:
**no agent tool can write a hero** and **the only client upload path 404s**. Those two facts alone
make `0 heroes` and `0 adventures` the *necessary* state of that database regardless of how much
anyone used the product.

The creator of an AI game-master companion has never run a game with it. That is not a moral
failing; it is a diagnostic. A product owner who used the product would have found the upload bug in
April.

### 2.5 The end-gate is honest, advisory, and therefore inert — and the practice's designed response to "the core promise doesn't work" is to ship past it

I verified the end-gate report text directly
(`.momentum/handoffs/sprint-2026-07-13-endgate-report.html`, rendered 2026-07-22). The corpus is
right that it is unusually candid. It leads with:

> *"the sprint's core promise, 'what you tell Urd gets remembered,' is **not yet reliable when a real
> language model drives it**."*

And D5, verbatim from the file:

> **D5 · "It is written." is sometimes a lie — captures narrated but never saved.**
> *Evidence.* Direct database queries during the live run: **~5 of 7 closes → zero rows**; backend
> logs show no exceptions… Unit tests never see this because mocked models always call their tools.
> **Option A (recommended). Approve the merge as-is**, and make a capture-integrity hardening story
> the top of next sprint…
> Option B. Hold the sprint at this gate until the root cause is isolated…
> *My recommendation: Option A — the merge doesn't make this worse…*

Read that as a product manager. The sprint's keystone capability succeeds **2 times in 7**. The
recommended action is *merge and defer*. The same header that carries this text also reads
"blocked / broken stories: 0."

Both statements are true **under story-level accounting**, which is precisely the indictment. No
story is blocked. No story is broken. Every story passed its own contract. And the feature does not
work. A gate that can render those two facts side by side without contradiction is a gate measuring
the wrong thing.

Then: nothing happened. I verified the aftermath myself.

```
nornspun-backend:  git rev-list --left-right --count main...sprint/sprint-2026-07-13  →  1  26
nornspun-client:   git rev-list --left-right --count main...sprint/sprint-2026-07-13  →  0  27
both repos:        git branch --show-current  →  main
both repos:        git merge-base --is-ancestor sprint/… main  →  NOT_MERGED
.momentum/stories/index.json:  302 total — {backlog:150, done:91, dropped:28, obsolete:19,
                               review:12, parked:2}  ← the 12 `review` are this sprint
.momentum/sprints/index.json:  active = sprint-2026-07-13, status "active", locked true
                               planning: null
```

**The mission brief that convened this council states the sprint "finished all the stories" and the
"end-gate approved." That is false, and it is the most consequential unverified claim in the entire
frame.** There is no approval record anywhere. The sprint is still open and locked. Every story is
still `review`. Neither repo's `main` contains a line of it. The developer's experience of "I opened
the app and couldn't do the simplest things" was, in significant part, an experience of running
**pre-sprint code** — a fact nobody in the loop knew at the time, which is itself an accountability
finding: nobody owned knowing what build was in front of the owner.

I will not let the corpus's preferred framing pass either. It calls this a "closure gap" and files it
as a missing automation. **That is a euphemism.** Closure did not happen because closing means a
person declaring "this is, or is not, good enough for a user to touch," and no such role exists here.
Automating the merge would have shipped, faster, a capability the pipeline itself measured at 2-in-7.
The corpus's implicit prescription is a robot that rubber-stamps on schedule.

---

## 3. Independent verification log

The corpus was written by audit agents; audit agents produce confident false positives, especially on
negative claims. Every load-bearing claim in §1–§2 was re-verified by me against raw sources today.
Method and result for each, including failures.

### 3.1 Claims verified — PASSED

| # | Claim | Method | Result |
|---|---|---|---|
| V1 | `features.json` is unreferenced by sprint planning | `grep -c 'features\.json'` on `workflow.md` in plugin cache v0.31.0 (1,258 ln), v0.32.0 (1,442 ln), and repo source | **0 / 0 / 0.** PASS |
| V2 | …and by every Momentum skill | `grep -rn 'features\.json' skills/momentum/skills/ \| grep -v '/evals/'` | Empty. PASS. **Sharpened:** the only skill that ever read it (`feature-status`) is deprecated by its own frontmatter; its replacement `canvas` has zero references |
| V3 | Sprint state has no feature field | Parsed `.momentum/sprints/index.json` | `active` keys = `approvals, locked, planned, slug, started, status, stories, team, waves`. PASS |
| V4 | The sprint is unmerged and undecided | `git rev-list --left-right --count`, `merge-base --is-ancestor`, `branch --show-current` in both repos | backend `1 26`, client `0 27`, both on `main`, `NOT_MERGED` both. PASS |
| V5 | 0 of 15 features at working (GM-facing) | Parsed `.momentum/features.json` | 7 partial, 6 not-started, 2 working (`llm-cost-tracking`, `evals` — both operator-facing). PASS |
| V6 | Registry is stale | `git log -- .momentum/features.json` | Two commits ever: `e9ccdec` (2026-05-25, path move), `0b6b064` (2026-06-16, ASR-006 reconcile). PASS |
| V7 | Roadmap cut along a backend spine, owner-signed, gate at Sprint E | Read `mvp-roadmap-sprints-a-e-2026-07-09.md` in full | *"Sprints are cut along that spine"*; *"adopted by product owner 2026-07-09"*; Sprint E = "MVP close-out". PASS |
| V8 | End-gate recommends approve-and-defer on the broken core promise | Text-extracted the end-gate HTML | D5 Option A verbatim: *"Approve the merge as-is… make a capture-integrity hardening story the top of next sprint"*; *"My recommendation: Option A."* PASS |
| V9 | Planning had ~3 substantive turns over 7 days | Parsed all `type:user` records from `cd4e9d0e-….jsonl` | 5 messages; 2 are skill boilerplate. Gate sign-off at `2026-07-20T21:19:41Z`, handoff request at `21:22:30Z` — **3 minutes.** PASS, and worse than claimed |
| V10 | Yolo-mode retro/triage requested explicitly | Parsed `2734df5b-….jsonl` user turns | Both quotes verbatim. PASS |
| V11 | Owner reported a bug at 06-18 end-gate, then approved | Parsed `8cbc4ae0-….jsonl` user turns | Bug 07-08T02:01; complaint that fixes miss it 07-08T18:09; `APPROVE` 07-09T05:54. PASS |
| V12 | **Adventure upload URL is broken** | Read `NornApiClient.kt:184/248/282/320`; `adventures.py:49`; `main.py:45`; `git log -S` | Client omits `/api` on upload only. Present on `main` **and** sprint branch. Introduced `a39fac0`, **2026-04-09**. Unit tests exist (`AdventureUploadViewModelTest.kt`) and pass against a fake. PASS — this is my own finding, not the corpus's |
| V13 | No hero-persistence agent tool | `grep -rn hero src/tools/*.py` on `main`; `git grep -i hero sprint/… -- src/tools/` | Empty both. CRUD API exists (`routers/heroes.py`); no client caller. PASS |
| V14 | Client API surface vs backend routes | Counted `@router.*` decorators (23) vs `NornApiClient` call sites (3) | 23 vs 3. PASS |
| V15 | Time-to-first-defect on walkthroughs | Timestamp deltas from `20b5f62e-….jsonl` | 14m46s (Jul 22), 6m21s (Jul 31). PASS |
| V16 | `sessionCount` hardcoded | Read `CampaignPickerScreen.kt:87` | `sessionCount = 0,`. PASS |
| V17 | Stories carry `feature_slug` and it aggregates to nothing | Parsed `stories/index.json` keys; `momentum-tools sprint --help` | 69/302 populated; 16 sprint subcommands, all story-scoped. PASS |

### 3.2 Claims that FAILED verification, or that I must correct

**F1 — The mission brief's own premise is false.** The brief states the sprint "finished all the
stories" with the "end-gate approved." Verified: no approval record exists in any artifact, the
sprint is `active`/`locked`, all 12 stories are `review`, and neither repo's `main` contains the
work (V4). The corpus caught this; the framing handed to this council did not. Any council
conclusion that reasons from "approved and shipped, yet broken" is reasoning from a false premise.

**F2 — "Approve the merge as-is" is attributed to both D5 and D6; it appears once.** The
product-truth lens (§2 finding 8) and the retro-loop lens both state the end-gate's recommended
resolution for **D5 and D6** is "Approve the merge as-is." Verified: that exact phrase occurs
**exactly once** in the file, in D5. D6's Option A is *"Fold the isolation investigation into the D5
hardening story as its first task."* The **posture** is identical (proceed, defer) — my §2.5 argument
survives intact — but the quotation is loose, and a paper that quotes it as verbatim from two cards
is over-reaching.

**F3 — Two corpus documents disagree on when `features.json` was last touched.** The
backlog-economics lens says "Last modified 2026-06-16"; the product-truth lens says mtime
"Jul 13 10:55." Both are partly right and neither says so: the last **content** commit is
`0b6b064`, 2026-06-16; the **filesystem mtime** is 2026-07-13 10:55. Immaterial to either
conclusion, but it is exactly the kind of unreconciled duplicate-truth defect the corpus itself
identifies as a systemic pattern — now occurring inside the corpus.

**F4 — Database row counts are corpus-reported, not re-verified by me.** Docker Desktop is broken on
this machine (documented in ground-truth §2) and I am read-only; I did not start the finch VM. The
"2 campaigns / 0 heroes / 0 adventures" figures in §2.4 are inherited. I compensated by verifying
the two structural causes from source (V12, V13), which make those specific zeros necessary
independent of usage. Anyone relying on the *other* row counts (episodes, recaps, divergences)
should re-query before citing.

**F5 — Where my own prior did not survive cleanly.** I expected to find planning that had substituted
task language for capability language. It hadn't. The roadmap states a user-outcome MVP gate
verbatim; the keystone story's AC is a quoted product invariant (*"The model should never ask what
campaign I want to use"*); `features.json`'s acceptance conditions are better written than most
production PRDs I have read. **The language of outcomes is everywhere in this practice. The
accountability for outcomes is nowhere.** That is a meaningfully different diagnosis from the one I
walked in with, and it changes the prescription: this does not need better product writing. It needs
one enforced checkpoint that consumes the writing that already exists.

---

## 4. Anticipatory attacks on the other seats

### 4.1 To the Architect: "fix the seams"

You will say the failure is structural — cross-repo integration with no contract tests, a
verification routing table that maps `change_type: backend → curl` and therefore never drives the
client, horizontal decomposition, no walking skeleton. You will prescribe contract testing, a
journey-level E2E harness, vertical slices.

Every one of those observations is true. Every one of them is causally inert here, and I have the
specimen to prove it.

**The adventure-upload bug is your dream case.** A contract mismatch across a repo boundary. One
path segment. Exactly the class your prescription targets. Now count what ran over it and passed:
the story's own Gherkin ACs; a unit test suite covering success, TOO_LARGE, and NETWORK_FAILURE
(against a mock, so the URL is unobservable); adversarial code review; AVFL with 16 lenses; a Maestro
audit that individually re-classified 13 scenarios and converted 7 to automation; a formal
assessment, ASR-006, "AVFL-verified," which re-blessed `adventure-upload` as `partial, 1/2 done` on
2026-06-16, **68 days after the URL broke.**

Seven quality instruments. Zero catches. **Why?** Not because any of them was badly built. Because
none of them was ever pointed at the question "can a GM upload their adventure?" A seam gets tested
when somebody is accountable for the journey that crosses it. Add contract tests tomorrow and you
will get contract tests for the seams somebody thought to enumerate — which is precisely the set that
already has coverage. You will not get one for `uploadAdventure`, because the reason it has no
coverage is not that contract testing is unavailable; it is that nobody was ever going to ask.

Three further problems with your position, from the evidence:

**Your walking-skeleton prescription misdiagnoses the patient.** Ground truth verified live, on
`main`: launch the desktop app → see real campaigns → chat with Urd or Verdandi → get memory-aware
replies citing real open threads → conversationally create a campaign → upload a PDF via API →
Verdandi cites "Ser Marrow" by name from it. **A skeleton exists and walks.** The deficit is not that
we skipped Slice 0; it is that nobody has walked the slice we have — four to five times in four
months, each time productively (§2.4).

**Your harness has an unmet precondition your own literature can't solve.** Compose desktop is
AX-blind by architectural choice (`verification-harness.json`, `.claude/rules/e2e-validation.md`).
The documented E2E launch command has **never worked on any commit in the repository's history** —
`ui-test-junit4` has been test-classpath-only since the initial client commit. The external research
found no Compose-desktop journey-driving answer anywhere in the field. So "build the journey harness"
is not a Monday action; it is an epic.

**And we already ran your experiment.** The 2026-05-01 retro diagnosed this exact failure —
*"the application was marked 'done' while showing only errors on screen"*; the developer's own phrase
in the audit was **"a status lie"** — and minted three **critical**-priority engineering fixes:
`e2e-pre-flight-gate`, `avfl-fixer-rules-first-and-autonomous`,
`e2e-grading-live-evidence-and-targeted-reruns`. All three are `status: backlog` today, unselected
across four subsequent sprints. Of the 29 stories in the `impetus-core` process epic: **0 done.**
Your prescription has been sitting in the backlog for three months with a `critical` label on it. It
did not fail because it was wrong. It failed because nobody was accountable for it either. Adding a
fourth engineering story to that pile is not a fix; it is a re-enactment.

I will concede one thing to you, and it matters: **the verification routing table is a real
mechanical defect.** `change_type: backend → curl` decides test depth from which files a story
touches instead of where a user meets the behavior. That is a one-table policy change and it should
be made. But note what it is: a rule about *what to verify*. It still requires someone to have
declared the outcome worth verifying. It is downstream of §2.1, not a substitute for it.

### 4.2 To the Super-Senior Developer: "delete the process"

You will point at 302 stories, 47 killed (23 with full specs written before the kill), a 20-story
wizard cluster built and torn out at −3,888 lines, 98 subagents in a single build, a 16-lens AVFL,
600-line plan documents — and conclude that the ceremony is the disease. Just build the thing. Talk
to the code. Ship small.

**Ad-hoc mode is already in this dataset, and it is the worst-performing mode in it.**

On 2026-07-30, with the sprint stuck and the owner unable to use the app, the practice was bypassed:
an ad hoc dynamic workflow patched `main` directly. No story, no plan gate, no code review, no AVFL,
no coverage contract. Result, verified: **F1 lives on `main` alone. F2 and F3 live on the sprint
branch alone. The two histories are still fully divergent** — `main` is 1 ahead / 26 behind. The
"fast fix" manufactured a permanent fork in the product's history that nobody has reconciled.
Earlier, in April, client and backend "fixed" each other's URL contract in uncoordinated same-day
reverts and **broke campaign creation for two months.** And D4.14 rebuilt an entire backend inside a
stale embedded copy of the repo and lost the work.

Ad-hoc did not produce speed here. It produced the untracked patches that made the state
unknowable — which is exactly the condition that let a mission brief tell this council the sprint was
"approved and shipped" when it was neither.

**Your cost model is also empirically wrong.** Planning a twelve-story sprint took **89 minutes** of
wall-clock (21 commits, 10:56am–12:25pm PDT, corroborated by the transcript window). Builds run
**~2 days** once started. The calendar sink is **7 days** (07-13) and **18 days** (06-18) of *human*
gaps around gates that no ceremony causes and no ceremony can shorten. Delete the entire planning
apparatus and you recover 89 minutes and still wait seven days.

Where you are right, and I will say it plainly: **the ceremony bids against tasting for the same
scarce resource, and tasting keeps losing.** Every gate is a document to read. The owner's response
to document load is verifiable and rational — "yolo mode," "get through it asap," "don't present to
me until a necessary HITL gate," a three-minute sign-off. So the ceremony *is* implicated. But the
remedy is not amputation. It is re-pointing: **swap document-review attention for app-driving
attention at a 1:1 ratio.** Thirty minutes driving the app beats thirty minutes reading an end-gate
report by an enormous margin, and I have the yield numbers (§2.4) to defend that claim. That is a
reallocation, not a deletion.

### 4.3 To the corpus itself

The comparison document's headline — *"our pipeline told the truth and nobody acted"* — is the most
seductive sentence in this evidence base and it is a half-truth that will misdirect the council if
left standing.

The pipeline told the truth about **the things it was pointed at.** It said nothing whatsoever about
`uploadAdventure`, about the absent hero tool, about the 20 unreachable routes, about
`sessionCount = 0` — because it was never pointed at a user journey, only at stories. Calling that
"honest" flatters it. A witness who answers every question truthfully and is never asked the material
question is not a good witness; they are a badly conducted examination.

And "nobody acted" is not a closure problem. It is an ownership problem wearing closure's clothes.
Automate the merge and you ship a 2-in-7 capability on schedule. The missing thing is not a button
press. It is a person whose job is to say **no**.

---

## 5. Prescription

Diagnosis and prescription kept separate, as instructed. Concrete enough to start Monday.

### 5.1 Next 30 days

**P1 — Monday morning: the Capability Board (2 hours, one time).**
Take the 15 acceptance conditions already written in `.momentum/features.json`. For each, Steve
personally runs it against a running, correctly-paired build and records **PASS / FAIL + the exact
break point (file:line where reachable)**. The ground-truth agent has already done 14 of 15 — copy
that in as the draft and spot-check it. Publish it as one page.
**The standing rule: a feature is FAIL until a human runs its acceptance condition against a running
build. No agent report, no green suite, and no assessment flips it.** Today's honest baseline is
0 of 15 PASS. That number, not story count, is the only number reported anywhere from Monday on.

**P2 — Re-cut the roadmap so every sprint names the one condition it flips.**
A sprint's title becomes the acceptance condition it will move from FAIL to PASS. Its story list is
whatever that requires, across whatever repos. **If a sprint cannot name a condition it will flip, it
does not get planned.** This rewrites the A–E roadmap by force: Sprint B as currently composed cannot
survive the test, and that is the point. It also fixes the sequencing complaint at the root — the
spine stops being the organizing principle and becomes an implementation detail of whichever
condition is being closed.

**P3 — Spend the first week flipping the four conditions that are hours away, not sprints.**
These are not sprint material. They are an afternoon each, and together they take the board from
0/15 toward 3/15:
(a) `NornApiClient.kt:320` — add the missing `/api` segment; then actually upload a PDF from Android
and ask Verdandi about an NPC in it. That is `adventure-upload`'s acceptance condition, verbatim.
(b) `MainWindow.kt:40` — the desktop upload `TODO`; JFileChooser wiring.
(c) A hero-persistence agent tool — the CRUD API at `routers/heroes.py` already exists and has no
writer. This unblocks `campaign-init`'s acceptance tail.
(d) `CampaignPickerScreen.kt:87` — the `sessionCount = 0` hardcode.
Doing these *first*, before any process change, is also the cleanest test of my thesis (§6).

**P4 — Decide sprint-2026-07-13 this week. Explicitly. In writing.**
Not deciding is currently the operative choice and it is the worst available one: 53 commits stranded,
12 stories frozen, the owner running pre-sprint code without knowing it. My read of the evidence is
that D5's honest answer is **Option B, not the recommended Option A** — a keystone capability that
succeeds 2 times in 7 is not a "documented gap," it is a broken feature, and merging it makes the
board's `session-capture` row a lie in the optimistic direction *again*. Either (i) merge and make
capture-integrity hardening the entire content of the next sprint, or (ii) abandon the branch. Write
the verdict to `.momentum/sprints/sprint-2026-07-13/endgate-decision.md` — the sibling file to
`plan-gate-decision.md` that has never existed for any sprint.

**P5 — Put tasting on the calendar, not in the workflow.**
Two 30-minute slots per week. Steve drives the app against a correctly-paired build. No agent
narrating, no gate document, no report to read. Findings go to intake as stubs afterward. Measured
yield from this dataset: **100% hit rate, median time-to-first-defect ~6 minutes.** This is the
highest-return activity in four months of evidence and the only one that has never been scheduled.
Pay for it by deleting an equivalent amount of document-review time — the end-gate report is the
obvious donor, and the developer already said so himself: *"It's not just about the end-gate document
it's about my review."*

**P6 — One command, one build identity.**
A single `mise run dev` that starts backend and client from the same git ref, prints that ref
prominently at startup, and refuses to run a mismatched pair. The 2026-07-31 walkthrough ran a
sprint-branch client against a `main` backend and produced a diagnosis that was partly an artifact of
the pairing — and neither the human nor the agent knew. Also: the backend `README.md` is empty
(0 bytes). Write five lines in it.

### 5.2 Structural — after the 30 days

**S1 — Make the feature verdict mechanically load-bearing.** `momentum-tools sprint complete` must
refuse to close a sprint without a recorded human PASS/FAIL against the acceptance condition the
sprint named at planning (P2). Add `momentum-tools feature verify <slug> --verdict pass|fail
--evidence <text>`, writing to `.momentum/features.json` with a timestamp and a build ref. Fix
`feature-status-hash` to read `.momentum/features.json` or delete it — a command that returns
`"success": true, "features_present": false` against a live registry is worse than no command.

**S2 — Reconnect planning to the registry.** `sprint-planning` Step 1 reads `features.json` and
opens with the board; Step 2 selection is filtered by "does this move the named condition"; the plan
gate's first fork becomes *"After this sprint a GM will be able to ___ . Approve / change / reject."*
That is the fork that was missing on 2026-07-20, and it is the one fork a three-minute sign-off
cannot answer with a default.

**S3 — Hold the end-gate, don't render it.** The end-gate stops being an HTML artifact reviewed
asynchronously and becomes a live session with the app running, whose first agenda item is the
named acceptance condition demonstrated or not demonstrated. The report becomes the depth-on-demand
backing, not the review surface. This is the only change that structurally prevents a repeat of
07-08 → 07-09 (report a user bug, watch the fix wave miss it, approve anyway).

**S4 — Let retro mint product stories.** Current policy — verified across all 7 retro documents,
65+ spawned items, **0** with a product epic slug — routes every retro finding away from nornspun's
own backlog by design. That policy is right for practice findings and fatal for product findings. A
capability regression found in retro must be allowed, and required, to become a product story in the
product backlog. Otherwise the loop that is supposed to notice "we shipped stories but not a feature"
is structurally forbidden from writing down what it noticed.

---

## 6. Falsifiability

I state these in advance so the council can hold me to them.

**F-A — The strongest test, and it runs this week.** My thesis says the deficit is accountability,
not engineering: capabilities are near-complete and unwatched. Concretely, **I predict that at least
4 of the 15 acceptance conditions flip from FAIL to PASS with less than one day of work each** (P3).
If the Capability Board baseline instead shows that most conditions fail for reasons requiring deep
architectural work — new subsystems, redesigned data flow, unbuilt infrastructure — **then the
Architect is right and I am wrong**, and the correct diagnosis is horizontal decomposition, not
accountability. This is cheap to run and I would rather be corrected by it than argued with.

**F-B** — If someone shows me a sprint in this history where a named *user outcome* was the stated
goal, tracked as the completion criterion, and the sprint still failed to deliver it — then
accountability was not the binding constraint and I have mistaken a symptom for a cause. I searched
for such a sprint and found none: every sprint's recorded outcome is a story list.

**F-C** — If sprint-2026-07-13 is merged with a correctly-paired build and a walkthrough finds the
capture loop reliable, then the failure was substantially bookkeeping and build-identity, my
"nobody owns the outcome" ranking over-claims, and the corpus's closure framing deserves the top
slot instead of the second.

**F-D** — If `features.json` is wired into planning and end-gates (S1/S2) and the next three sprints
still complete zero acceptance conditions, then the instrument is not the lever. The residual
explanation would be product-runtime capability — a ~$0.06/M-token model that will not reliably call
its tools no matter what the process does — and the correct next move is a model-tier decision, not
a process one.

**F-E** — If someone demonstrates that the `uploadAdventure` URL works in production via a proxy,
rewrite rule, or base-URL variant I did not find, my headline specimen collapses and §1 must be
rebuilt on the hero-tool gap instead. I checked: `baseUrl` is `http://localhost:8000` /
`http://10.0.2.2:8000` at all four call sites, the sibling calls in the same file include `/api`
explicitly, and the line is unchanged on both branches since 2026-04-09. I am confident, not certain.

---

## 7. Closing

The developer asked whether the practice is optimizing for the wrong thing. It is — but not in the
way the question implies. This practice did not fail to think about users. Its acceptance conditions
are better written than most funded product organizations manage. It thought about users constantly,
wrote it down beautifully, and then built a machine that measures something else and never once
compared the two.

There is a moment in this evidence base I keep returning to. It is not the broken URL or the
stranded branches. It is 2026-07-08 at 18:09, when the owner writes: *"I mentioned specific problems
with both desktop and android but it's not clear you're looking to fix those."* He had seen it. He
had said it. The system had no slot for it. And eleven hours later he signed the gate anyway,
because the gate asked him about two findings it had chosen, and never asked him about the one he
brought.

Everything downstream of that — the recurrence three weeks later, the 2-in-7 keystone, the
unmerged branch, the app he opened that couldn't do the simplest things — follows from a system in
which the person who knows what the product should do has no mechanism to make that knowledge
binding.

Give him one. It costs a two-hour Monday and one refusal in `momentum-tools sprint complete`.

---

*Verification basis for this document: direct reads and commands against
`/Users/steve/projects/nornspun{,-backend,-client}`, `/Users/steve/projects/momentum/skills/`,
`/Users/steve/.claude/plugins/cache/momentum/momentum/{0.31.0,0.32.0}/`, and targeted parses of
`/Users/steve/.claude/projects/-Users-steve-projects-nornspun/*.jsonl` (user-turn extraction only, no
whole-file reads). All commands and their outputs are reproduced inline above or in §3. Corpus
documents are cited where I inherited a claim rather than re-deriving it, and every inherited claim
is flagged as such.*
