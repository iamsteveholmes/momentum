# The Owner's Signal Is Downgraded on Entry

**Council rebuttal — nornspun delivery discovery, round 2**
**Date:** 2026-08-02
**Seat:** The Product Manager (adversarial)
**Responding to:** `senior-dev-position.md` ("The Machine Has No Output Shaft"), `architect-position.md` ("There Is No Product to Deliver")

---

## 0. Thesis after contact

My round-1 thesis was: *nobody is accountable for "a user can now do X," and every instrument that could hold that accountability is wired to nothing.* It survives, and one seat handed me a better weapon than I had. But it was **incomplete in a way both other seats exposed**, and I am amending it:

> **The failure is not only that no artifact consumes the outcome instrument. It is that the one place where a real outcome signal enters this system — the owner saying "I cannot do this" — is mechanically downgraded on entry into a low-priority, feature-less, curl-verified backend chore. The instrument isn't just disconnected at the output. The input is lossy too.**

I verified this today, and it is the single sharpest artifact in the whole corpus. The story that fixes the defect the owner reported at **two consecutive end-gates** — *"the agent doesn't know what campaign I've chosen"* — is `.momentum/stories/backend-active-campaign-name-injection-fix.md`, and its frontmatter reads:

```yaml
story_type: bug
priority: low
change_type: [backend]
verification_method_advisory: curl
```

`feature_slug`: **null** (verified against `.momentum/stories/index.json`). Provenance line in the body: *"ex-quick-fix promoted by … mvp-roadmap-sprints-a-e-2026-07-09.md, **Sprint A #10**."*

The product owner's top complaint entered the pipeline as **item #10, priority low, no capability linkage, verified by curl**. Every downstream failure the other two seats describe — the wrong verification driver, the story that never merged, the chimera that produced a false re-diagnosis — is operating on a work item that the system had already decided was tenth-most-important and not attached to any user capability. The Architect wants to re-key the routing table. The Senior Dev wants to auto-merge. Neither touches the moment where the owner's voice was converted into a `low`.

That is the amendment. The rank order is unchanged.

---

## 1. Strongest attacks

### 1.1 Against the Architect — the centerpiece is an epistemics finding wearing a delivery finding's clothes, and I can date it

The Architect's Cause 1 rests on one causal chain (his §2.1, steps 1–7), whose second link is:

> *"The developer ran the backend from `main`, and so saw the raw-UUID behavior. **Correct symptom; wrong tree.**"*

**"Wrong tree" requires that a right tree existed.** On 2026-07-08T02:01Z — the owner's *first* report of this symptom, *"it asked me what campaign I was in"* (session `8cbc4ae0`) — no tree in any repository contained a fix. Verified this round:

```
$ cd ~/projects/nornspun-backend
$ git log --all --reverse --format='%h %ad %s' --date=iso -S 'campaign_name' -- src/agents/urd.py
b45ac78  2026-04-06  feat(capture): implement Urd's post-session capture …
20b7702  2026-04-12  feat(prompts): wire campaign_system into Norn agent prompts
2eef2bf  2026-07-21  fix(backend-active-campaign-name-injection-fix): inject resolved campaign name …
ab2e579  2026-07-30  fix(agents): active-campaign prompt line carries resolved name, not raw UUID

$ git show af88f0f:src/agents/urd.py | sed -n '189,190p'      # main at the merge-base
    if ctx.deps.campaign_id:
        assembled += f"\n\nActive campaign: {ctx.deps.campaign_id}"
```

The first fix in existence anywhere lands **2026-07-21, thirteen days after the owner reported it**. On 07-08 the defect was invariant across every buildable composition of the two repos. There was no right tree to run.

So the chimera explains **the 07-31 re-diagnosis** and nothing before it. What it does not explain — and what the Architect's paper never accounts for — is the 24-day arc from *owner reports it* (07-08) → *story classified `priority: low`, no feature* → *fix committed to a branch* (07-21) → *owner reports it again* (07-31) → *still not in front of the owner* (08-02). Undefined build identity is a real defect that corrupted one diagnosis. It is not what kept a twice-reported, owner-facing product defect off the owner's machine for twenty-four days.

**Three more, in descending order of damage:**

**(a) His own prescription #1 concedes my thesis verbatim.** Architect §5, prescription 1:

> *"resolve `urd.py`/`verdandi.py` by keeping **one** implementation and deleting the other — either is fine, **deciding is the point**."*

A structural thesis whose first, most urgent, "nothing else on this list matters until it is done" prescription is *a person must make a decision, and which way they decide does not matter* has named the missing part, and it is not a referent. It is a decider. He wrote my paper's conclusion into his own action list and ranked its cause fifth.

**(b) He applies one standard to my cause and the opposite standard to his own.** He demotes `features.json` to Cause 5 on this argument (§2.5):

> *"the registry was not wrong … Nobody was told the product worked. … Fixing the tracker changes nothing about the app."*

Then his Cause 3 is *"the pipeline's terminal state is a document, not a release"* — ranked **third**. Both are the identical pathology: an accurate artifact with no mechanical consequence. He is right that an accurate-but-inert registry is inert; that was my finding, not my counter-argument. I never claimed the registry lied. I claimed `momentum-tools sprint --help` has sixteen subcommands and zero of them can read it. An inert output artifact ranks third when it is his and fifth when it is mine.

**(c) A defect invariant across every tree cannot be caused by tree ambiguity.** Re-verified this round, both branches:

| | Path |
|---|---|
| `main:shared/…/NornApiClient.kt:320` | `"$baseUrl/campaigns/$campaignId/adventures"` |
| `sprint/sprint-2026-07-13:…:362` | `"$baseUrl/campaigns/$campaignId/adventures"` |
| sibling calls, both branches | `"$baseUrl/api/chat"`, `"$baseUrl/api/campaigns"` |

There is no composition of the two repositories in which adventure upload works. Same for the hero write path (absent on both), same for the twenty backend routes with no client caller. His §2.2 catches the upload bug and files it under "no enforced contract" — correct mechanism, wrong rank. A contract check finds it in an afternoon; nobody spent the afternoon, for 116 days, because nobody owed anyone that capability.

**(d) The one thing I take from him and use against him.** His prescription #6: *"`features.json` becomes writable **only** by a walkthrough of the assembled artifact."* That is my P1 and S1 with a build-identity precondition bolted on. It is a better version of my prescription. He adopts the outcome-accountability mechanism as prescription #6 while ranking its absence as cause #5. If it's fifth, why is it in the list at all?

---

### 1.2 Against the Senior Developer — his centerpiece is factually false, and his own counterfactual falsifies his load-bearing cause

This is the sharpest thing in this rebuttal, so I will be exact.

**Attack 1 — the "better test than the governed version" claim is false, and he sourced it from the artifact he is celebrating.**

His thesis paragraph:

> *"a fix was on `main`: four files, +111/−4, **including the outcome-level test the governed story never wrote**. Twenty-five minutes and forty-two seconds, with the entire practice bypassed."*

His verification #4: *"Includes the rendered-prompt assertion the governed story lacked."*

That sentence is copied from `ab2e579`'s own commit message: *"the assertion the original story lacked (variable was populated but no template consumed it)."* He did not diff it against the story. I did:

```
$ git show 2eef2bf -- tests/agents/test_urd.py        # 2026-07-21, the GOVERNED story
+    result = await urd_system_prompt(_run_context(deps))
+    assert "Active campaign: The Ashen Coast" in result
+    assert str(campaign_id) not in result
```
```
$ git show 2eef2bf --stat
 src/agents/urd.py             |  3 +-
 src/agents/verdandi.py        |  3 +-
 tests/agents/test_urd.py      | 95 +++++++++
 tests/agents/test_verdandi.py | 97 +++++++++
```

The governed story wrote **192 lines of tests** asserting, against the *rendered system prompt*, that the campaign **name** appears and the **UUID does not** — nine days before the hotfix, plus an id-fallback case the hotfix also duplicates. The Architect found this independently (his verification #3) and it is now confirmed twice.

So the Senior Dev's proof text — the exhibit that carries "the practice's own escape hatch out-delivered the practice by a factor of roughly 500" — is a **redundant re-implementation of a fix that already existed, justified by a commit message that misstates the record, based on a diagnosis made against the wrong build.** He indicts the practice for confident-but-hollow verification, and his indictment rests on an unverified claim he took at face value from an ungoverned commit. That is the exact false-positive class the council brief warned about, committed by the seat arguing for less verification.

**Attack 2 — nobody ever confirmed the hotfix did anything. It is a commit, not a delivery.**

He calls `ab2e579` "the one thing that *did* reach trunk." Verified, session `20b5f62e`:

```
total human turns: 24
last human turn: 2026-07-31T04:52:35.460Z  "Are you planning in Fable but using Sonnet agents…"
commit ab2e579:   2026-07-30 22:00:29 -0700  =  2026-07-31T05:00:29Z
```

The owner's last word in that session is **eight minutes before the commit**, and there is no later turn. Nobody restarted the app. Nobody re-ran the walkthrough. And per the Architect's verification #8, re-confirmed by me — `git rev-list --count origin/main..main` → **23**, `origin/main` last updated **2026-06-11** — that commit is not even pushed. It sits on one laptop, unverified, unpushed, unseen by the user whose complaint produced it.

His delivery exemplar is **commits per minute**. That is a throughput metric with no user on the other end — structurally identical to "91 stories done," which is the thing he is indicting. He replaced one output metric with a faster one.

**Attack 3 — the merge is not the bottleneck. Measured: 46 seconds.**

His Cause 1: *"Delivery is a manual terminal step gated on the system's scarcest resource… there is no expiry, no retry… If the human does not answer, nothing ships — forever."*

Run the clock on the one time the human answered:

| Event | Timestamp (UTC) | Source |
|---|---|---|
| Owner types `END-GATE DECISION for sprint-2026-06-18: APPROVE.` | `2026-07-09T05:54:49.297Z` | session `8cbc4ae0`, user turn |
| Client merge commit `704e63c` "Merge branch 'sprint/sprint-2026-06-18'" | `2026-07-08 22:55:35 -0700` = `05:55:35Z` | `git log -1 main` |
| Owner: `push both` | `2026-07-09T07:20:39Z` | same session |

**Forty-six seconds** from decision to merge commit. Pushed 85 minutes later. The mechanism is not slow, not missing, and not the constraint. The eleven-day stall on 07-13 is not an automation gap; it is **the absence of anyone whose job is to answer**. Automating past that ask does not add a decider — it removes the last place one was required.

**Attack 4 — his counterfactual falsifies his own cause. The sprint that merged delivered zero capability and shipped a lie.**

He writes: *"the difference between the sprint that delivered and the sprint that didn't is not process quality … it is that in July the developer happened to be in the chair."* Enumerate what "the sprint that delivered" delivered:

```
$ git log --oneline 704e63c^1..704e63c^2 | wc -l    →  35 commits, 9 stories
```
`app-scaffold-shared-title-bar-composable` · `zone-a-title-bar-variants` ·
`norn-pip-redesign-glow-scale-inactive-fill-skuld-badge` · `composer-redesign-vellum-surface` ·
`begin-button-cta-token-fix` · `light-theme-enforcement-mvp` ·
`campaign-switcher-tappable-navigation-link` · `campaign-init-picker-screen-and-start-new-campaign-card` ·
(+ 3 AVFL fix iterations)

Nine stories: a title bar, pip glows, a composer surface, a light theme, a CTA token, a picker screen. **Zero acceptance conditions in `.momentum/features.json` changed state** — re-verified: 7 `partial` all stamped `last_verified: 2026-06-16`, 6 `not-started` and 2 `working` stamped `2026-05-03`. Nothing moved after a full merge-and-push on 07-08.

And it is worse than neutral. The hardcode I flagged in round 1 was **introduced by that merge**:

```
$ git log --oneline 704e63c^1..704e63c^2 -S 'sessionCount = 0'
9eac68e feat(campaign-init-picker-screen-and-start-new-campaign-card): … build the campaign picker screen …
$ git show main:shared/src/commonMain/kotlin/com/nornspun/ui/screens/CampaignPickerScreen.kt | grep -n sessionCount
87:                        sessionCount = 0,
```

The sprint that merged, pushed, and closed **shipped to `origin` a campaign card that lies to the user about their own session history** — through Gherkin ACs, adversarial code review, three AVFL fix iterations, and an owner sign-off. Its fix (`session-counter-live-update-on-capture-close`) is `status: review` on the stranded branch.

**Merging is not delivering.** His load-bearing cause predicts that unsticking the merge unsticks capability. The one natural experiment in this dataset says it does not.

**Attack 5 — his prescription #2 cannot be built as specified.** *"Green build merges to `main` automatically; the human's ask becomes 'revert?'… Silence must mean ship."* Applied to 07-13, that auto-merges a sprint whose own E2E measured the keystone capability at roughly **2 successful captures out of 7** (end-gate D5, verified round 1). He sees this and patches it with prescription #5 — one Maestro flow on Android — then writes *"It fails today; that is the point."* So the gate is either **green = unit tests**, in which case it rubber-stamps (unit tests, code review, and AVFL were all green on `9eac68e`, the commit that shipped `sessionCount = 0`), or it is **red forever**, in which case nothing ships and he has rebuilt the stall he is diagnosing. He cannot have both, and neither branch produces delivery.

**Attack 6 — his Attack 3 on me misreads my prescription.** *"Your registry needs a green light it cannot get… There has never been [a journey check] on desktop."* My P1 reads: *"Steve personally runs it against a running, correctly-paired build and records PASS / FAIL."* The green light is **his hands** — the instrument he independently measured at a 100% hit rate across five occasions. He and I prescribe the identical oracle. The only difference between his `BROKEN.md` and my Capability Board is that mine is allowed to **block a sprint from closing** and his is a text file. He is arguing against the enforcement, not the instrument, and then citing the instrument's excellence as the reason enforcement is unnecessary.

**Attack 7 — one number is doing rhetorical work it can't support.** His falsifiability #6 offers the July practice:product ratio falling to 2.1:1 as possible evidence the apparatus is "amortizing." July is the month a twelve-story product sprint was in flight. That is a workload composition artifact, not a trend. Two data points inside one sprint window is not a curve.

---

## 2. Concessions

### To the Architect

**C1 — His verification #3 is a genuine kill, and it lands on evidence I was adjacent to.** The corpus's flagship "hollow verification" example (`backend-active-campaign-name-injection-fix`: *"plumbing tested, outcome not"*, *"`campaign_name` appears in zero prompt templates"*) is **false**. I confirmed his work independently above: the story asserts against the rendered prompt, positively and negatively, in 192 lines of test. The comparison document's §1.1 headline — *"That is Anthropic's sentence, re-enacted"* — inherits the error. I did not cite that example in round 1, but I did not catch it either, and I was reading the same corpus. Anyone reasoning from the corpus's verification-gap section is reasoning from a dead example.

**C2 — The chimera is real, it corrupted the 07-31 diagnosis, and my round-1 framing of it was too soft.** I called it a bookkeeping problem — *"nobody owned knowing what build was in front of the owner."* He showed it propagated a false bug report → a redundant ungoverned commit → a manufactured merge conflict → a false audit finding → a false headline → a false premise in this council. That is a bigger blast radius than I credited, and his six-layer trace is the best single piece of forensic work in this council's output.

**C3 — Build identity as an *admissibility rule* beats my P6.** *"A walkthrough that did not start with that command is inadmissible as evidence, and every bug report cites the two SHAs."* My P6 was "one command, one build identity." His adds the evidentiary teeth. I adopt his wording.

**C4 — I missed the push dimension entirely.** Verified by me this round: backend `main` is **23 commits ahead of `origin/main`, last pushed 2026-06-11**; sprint branches were never pushed. The client is clean (`origin/main == main`). Half the product has existed on exactly one laptop for seven weeks. Neither my paper nor the corpus surfaced this.

**C5 — He is right that a fifth registry is a real risk.** My S2 wires `features.json` into planning. He is correct that four completion registries already disagree because none is derived from anything mechanical. A fifth undisciplined one is a liability. His #6 — make `features.json` writable **only** by a human walkthrough of the assembled artifact — resolves it, and I fold it into my prescription.

### To the Senior Developer

**C6 — His app-launch-frequency finding is better evidence for my §2.4 than what I had.** I had "roughly four to five walkthroughs across four months," of which I verified three. He extracted every `desktopApp:run` / `installDebug` / `maestro test` tool_use across all sixteen transcripts and got **five distinct days — Jul 7, 8, 13, 22, 31 — across a 54-day corpus, every one of them an end-gate or post-build review, never a Tuesday.** That is the number, it is sharper than mine, and it is the strongest empirical support for my P5. Credited.

**C7 — He is right that another honest report changes nothing, and my prescription ordering was wrong.** His Attack 1: *"Adding a seventh honest instrument to a system whose failure mode is that nobody acts on the six it has is not measurement. It is furniture."* The 07-22 end-gate was best-in-class honest and produced no decision. My P1 (a published board) and P2 (a re-cut roadmap) are both documents. The only item in my round-1 list with mechanical teeth was **S1 — `momentum-tools sprint complete` refuses to close without a recorded human PASS/FAIL**, and I put it in the *structural, after 30 days* section. That ordering was wrong and both other seats caught it. S1 moves to position one.

**C8 — `d4-14` is a cleaner specimen than any of mine.** `status: done`, `priority: high`, four dangling `depends_on` entries, and `git log --all` in the backend returns **zero commits ever** for its sole deliverable. A story claiming to prove the end-to-end session loop works, whose artifact has never existed in the repository that runs, `done` for four months. I will use it.

**C9 — The Momentum freeze is worth running.** Verified his inventory myself: momentum has **1,702 commits, 537 stories, 215 `done`** against nornspun's 302/91. The practice repo has more finished stories than the product it serves. I do not accept his causal claim that this is *why* nobody answered the ask — the 46-second merge and the three-minute plan-gate sign-off point at a decision vacuum, not an exhausted one — but a 30-day freeze is free, falsifiable, and I have no argument against running it.

### To myself

**C10 — My round-1 F5 was half the finding.** I concluded *"the language of outcomes is everywhere; the accountability is nowhere."* That is true but passive, and it implies the fix is purely at the output end (wire the registry to a gate). The `priority: low` / `feature_slug: null` frontmatter on the owner's own twice-reported defect shows the loss happens **at intake**, before any gate could consume anything. My round-1 prescription had no item addressing intake. That is a gap in my paper, and §5 fixes it.

---

## 3. Updated position

**Unchanged and hardened:** THE load-bearing cause is that no human, agent, artifact, or command owns the sentence "a user can now do X." Three findings hardened it this round:

1. The merge takes **46 seconds** once someone decides. There is no automation gap at the terminal step — there is a decision gap.
2. The one sprint that **did** merge shipped nine stories, flipped **zero** acceptance conditions, and introduced `sessionCount = 0` to `origin`. Delivery of commits is orthogonal to delivery of capability, empirically, in this dataset.
3. Both other seats' first prescriptions are *"decide"* (Architect #1: "either is fine, deciding is the point") and *"merge or delete"* (Senior Dev #1). Neither is a structural or process fix. Both are a person accepting accountability. They have converged on my cause and disagreed only about what to call it.

**Amended:** the vacuum is bidirectional. Round 1 diagnosed the output side — 69 stories carry `feature_slug` and it aggregates to nothing; `momentum-tools sprint --help` has sixteen story-scoped subcommands and zero feature-scoped ones; `feature-status-hash` returns `"success": true, "features_present": false`. Round 2 adds the **input** side: the owner's direct outcome signal enters as `priority: low`, `feature_slug: null`, `verification_method_advisory: curl`, at position #10. There is no intake path in this practice that preserves "the product owner could not use the product" as a priority signal. That is a smaller, more mechanical, more fixable defect than anything in either rival paper.

**Demoted:** my round-1 §2.5 treated the corpus's "closure gap" framing as the second-ranked cause. The Architect's build-identity work and the 46-second merge measurement together convince me that closure is neither a cause nor an automation gap — it is the *visible symptom* of the decision vacuum, and it should be reported as such, not as its own cause.

**Promoted from the other seats:** two mechanisms enter my prescription that were not in it — the Architect's admissibility rule for walkthrough evidence (C3) and his derived-registry constraint (C5); and the Senior Dev's insistence that only mechanically-binding changes count (C7).

**What I still reject:** "no referent" as the load-bearing cause (it is 12 days old in its worktree form for these repos, and the capability gaps are 116 days old and invariant across every tree), and "invert the gate so silence ships" (it auto-merges a 2-in-7 capability, and the natural experiment says merging delivers nothing anyway).

---

## 4. The decisive test

**Sharpest live disagreement:** *The Architect ranks undefined build identity #1 and outcome accountability #5. I rank them inversely. His centerpiece asserts that the owner's twice-reported campaign-name complaint was a build-identity artifact — "correct symptom; wrong tree."*

**The test:** A "wrong tree" claim requires that a right tree existed at the time of observation. Date the first fix in any ref of either repository against the owner's **first** report of the symptom. If a fixed tree existed on 2026-07-08 and the owner ran an unfixed one, his ranking is right and mine is downstream of his. If no fixed tree existed, the chimera explains only the July-31 *re*-diagnosis, and the twenty-four-day arc from report to still-unshipped fix is an ownership failure that no build-identity fix touches.

**Run:**

```
$ cd /Users/steve/projects/nornspun-backend
$ git log --all --reverse --format='%h %ad %s' --date=iso -S 'campaign_name' -- src/agents/urd.py
b45ac78  2026-04-06 00:43:27 -0700  feat(capture): implement Urd's post-session capture with living memory (D4.4)
20b7702  2026-04-12 23:57:49 -0700  feat(prompts): wire campaign_system into Norn agent prompts
2eef2bf  2026-07-21 08:50:13 -0700  fix(backend-active-campaign-name-injection-fix): inject resolved campaign name …
ab2e579  2026-07-30 22:00:29 -0700  fix(agents): active-campaign prompt line carries resolved name, not raw UUID

$ git show af88f0f:src/agents/urd.py | sed -n '189,190p'
    if ctx.deps.campaign_id:
        assembled += f"\n\nActive campaign: {ctx.deps.campaign_id}"
```

Owner's first report: `2026-07-08T02:01Z` (session `8cbc4ae0`) — *"The Desktop App came up in the Salt Road > but clicking that did nothing. And when I typed in a prompt it asked me what campaign I was in."*

**Result: the test settles against the Architect's ranking.** The earliest fix anywhere is `2eef2bf`, **2026-07-21 — thirteen days after the report**. Every ref in both repositories appended the raw UUID on 07-08. There was no right tree. The chimera is real and it corrupted the 07-31 diagnosis — I concede that fully (C2) — but it cannot be the load-bearing cause of a defect that was invariant across the entire version-control graph, was reported by the owner to the system's face, and is still not in front of him on 08-02.

**Corroborating run — the same test applied to the Senior Dev's counterfactual:**

```
$ cd /Users/steve/projects/nornspun-client
$ git log --oneline 704e63c^1..704e63c^2 | wc -l                       →  35
$ git log --oneline 704e63c^1..704e63c^2 -S 'sessionCount = 0'         →  9eac68e (campaign-init picker screen)
$ git show main:…/CampaignPickerScreen.kt | grep -n sessionCount       →  87:  sessionCount = 0,
$ git rev-list --count origin/main..main                               →  0     (pushed)
$ python3 - <<< "parse .momentum/features.json"                        →  7 partial (last_verified 2026-06-16),
                                                                          6 not-started + 2 working (2026-05-03)
```

**Result:** the sprint that merged, pushed, and closed delivered 35 commits, flipped zero acceptance conditions, and shipped a user-visible lie to `origin`. Unsticking the merge does not unstick capability. Senior Dev's Cause 1 fails its own counterfactual.

**What would have settled it the other way, and did not:** if `2eef2bf` had predated 2026-07-08, or if any of the 06-18 sprint's nine stories had moved a `features.json` entry off `partial`.

---

## 5. Revised prescription

Round-1 items I keep are cited by their original tags. Ordering changed per C7 — the mechanically-binding item is now first, and an intake item is added.

### Next 30 days

**R1 — Make the refusal, first, before any document** *(was S1)*. `momentum-tools sprint complete` refuses to close a sprint without a recorded human PASS/FAIL against a named acceptance condition. Add `momentum-tools feature verify <slug> --verdict pass|fail --evidence <text> --build <sha>:<sha>`. Per the Architect's #6, `.momentum/features.json` becomes writable **only** by that command — no agent, no assessment, no AVFL run may set a feature status. Fix or delete `feature-status-hash`, which currently returns `"success": true, "features_present": false` against a live registry.

**R2 — Fix intake: the owner's word cannot enter as `priority: low`** *(new, from C10)*. Any observation whose source is the product owner driving the app enters the backlog as `priority: critical`, with a mandatory `feature_slug`, and its verification driver is the surface where the owner met it — never `curl`. The specimen is `backend-active-campaign-name-injection-fix`: `priority: low`, `feature_slug: null`, `curl`, Sprint A **#10**. That one frontmatter block is the whole failure in twelve lines of YAML, and it is a validator rule, not a culture change.

**R3 — Decide sprint-2026-07-13 this week, in writing** *(was P4)*. Both other seats independently made this their first prescription; that is three of three. Write the verdict to `.momentum/sprints/sprint-2026-07-13/endgate-decision.md` — the sibling of `plan-gate-decision.md` that has never existed for any sprint. My read is still Option B on D5 (a keystone at 2-of-7 is broken, not "documented"), but the Architect is right that *deciding* outranks *which way*. Then push both repos: backend `main` is 23 commits ahead of an `origin` last touched 2026-06-11.

**R4 — One command that is the product, and an admissibility rule** *(was P6, upgraded per C3)*. `mise run dev` starts db + migrations + backend + client from explicit refs and writes both SHAs to `RUNNING.json`. **A walkthrough that did not start with that command is inadmissible as evidence, and every bug report cites the two SHAs.** This is the precondition for the owner's own oracle to stop producing false diagnoses — which it did on 07-31, at a cost of one redundant commit and one manufactured merge conflict.

**R5 — Two 30-minute tasting slots per week, on the calendar** *(was P5, evidence upgraded per C6)*. Measured yield: five app-launch days in fifty-four, every one an end-gate or post-build review, every one producing a top-priority defect within minutes. Pay for it by deleting equivalent end-gate document-review time. The owner already said it: *"It's not just about the end-gate document it's about my review."*

**R6 — Flip the four conditions that are hours away** *(was P3)*. `NornApiClient.kt` upload URL (one path segment, broken on both branches since 2026-04-09); the desktop upload `TODO`; a hero-write agent tool against the existing `routers/heroes.py`; `sessionCount = 0` (the fix is already written and sitting in `review`). Doing these before any process change is also the cleanest test of my thesis (§6).

### Structural

**S-A — Every sprint names the one acceptance condition it will flip; a sprint that cannot name one is not planned** *(was P2)*. The 06-18 sprint — title bar, pip glow, composer surface, light theme — could not have survived this test, and it consumed a full cycle and shipped a defect.

**S-B — Planning reads the registry; the plan gate's first fork is the capability** *(was S2)*. *"After this sprint a GM will be able to ___. Approve / change / reject."* The 07-20 gate asked four questions: scope mechanics, a verify-and-close-gaps decision, greeting copy, and a line of dialogue. Three minutes later the owner asked for a handoff. That is the fork a three-minute sign-off cannot answer with a default.

**S-C — Hold the end-gate live with the app running** *(was S3)*, first agenda item the named condition demonstrated or not. This is the only change that structurally prevents a repeat of 07-08 → 07-09: report a user defect, watch the fix wave miss it, approve eleven hours later.

**S-D — Retro may mint product stories** *(was S4)*. Verified round 1: 7 retro documents, 65+ spawned items, **0** carrying a product epic slug.

**S-E — Adopted from the other seats.** Re-key `verification-standard.md` from `change_type` to assembled surface (Architect, and I conceded this in round 1). Add reachability to the Definition of Done (Architect). Freeze Momentum commits for 30 days (Senior Dev) — free to run, falsifiable, no argument against it.

---

## 6. Falsifiability, updated

**F-A (unchanged, and it is still the cheapest decisive test in this council).** I predict **at least 4 of 15** acceptance conditions flip from FAIL to PASS with under one day of work each (R6). If the Capability Board baseline instead shows most conditions failing for reasons requiring new subsystems or redesigned data flow, the Architect is right and I am wrong.

**F-B (new, aimed at my own amendment).** If someone shows me an owner-reported product defect in this history that entered the backlog with a `feature_slug` and a priority above `low`, my intake-loss finding is a sample of one and should be demoted to an anecdote. I checked the four campaign-context stories; the one that matters carries `priority: low` and no feature.

**F-C (new, aimed at the Senior Dev).** If sprint-2026-07-13 is merged, pushed, and correctly paired, and the owner's next walkthrough produces no top-tier defect, then merging *does* deliver capability, my §1.2 Attack 4 over-generalizes from one sprint, and his drivetrain framing takes the top slot. He and I should both want this run in week one.

**F-D (retained).** If `features.json` is wired into planning and end-gates and the next three sprints still complete zero acceptance conditions, the instrument is not the lever, and the residual explanation is product-runtime capability — a ~$0.06/M-token model that will not reliably call its tools. That is a model-tier decision, not a process one, and the Architect concedes his thesis does not reach it either.

**F-E (retained, now doubly checked).** If the `uploadAdventure` URL works via a proxy or base-URL variant I did not find, my headline specimen collapses. Re-verified on both branches this round: `main:320` and `sprint:362` both omit `/api`; every sibling call includes it.

---

## 7. The line I want on the record after round two

Three seats walked in with three theories. All three of us, independently, made the same thing our first action item: **someone has to decide.** The Architect wrote *"either is fine, deciding is the point."* The Senior Developer wrote *"merge or delete… accept the loss."* I wrote *"decide sprint-2026-07-13 this week, explicitly, in writing."*

We disagree about the diagnosis and agree about the first move. That is what a missing role looks like from three different angles.

And the artifact I would put in front of the owner is not the broken URL, the stranded branch, or the chimera. It is twelve lines of YAML:

```yaml
story_key: backend-active-campaign-name-injection-fix
priority: low
verification_method_advisory: curl
```
`feature_slug: null` · Sprint A **#10**

He said it out loud, twice, at two end-gates, three weeks apart. The system heard him, wrote it down, and filed it tenth.

---

*Verification basis for this document: direct `git` commands against `/Users/steve/projects/nornspun{,-backend,-client}` and `/Users/steve/projects/momentum`; direct reads of `.momentum/{stories,features}/…`; targeted Python JSON parses of `/Users/steve/.claude/projects/-Users-steve-projects-nornspun/{8cbc4ae0,20b5f62e}*.jsonl` (user-turn and tool_use extraction only, no whole-file reads). All commands and outputs reproduced inline. Claims inherited from another seat's paper are attributed and, where load-bearing, independently re-run.*
