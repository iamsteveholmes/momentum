# External Research: Practitioner Postmortems on Structured Agentic Dev Frameworks

**Date:** 2026-08-02
**Role:** External-research discovery agent — first-person accounts (last ~12 months, older items labeled) from practitioners running structured agentic dev frameworks (BMAD, spec-kit, Kiro, Claude Code multi-agent, Devin, loop engineering) who hit the story-done-but-feature-missing wall or its cousins.

---

## Executive summary

1. **The story-done-but-feature-missing wall is a documented, cross-framework failure mode** — reported first-person on spec-kit ("Not delivering a functional feature - nice spec though!!"), BMAD (dev agent marks tasks complete without running checklists), and by Anthropic's own engineering team ("Claude tended to... fail to recognize that the feature didn't work end-to-end").
2. **The most authoritative account is Anthropic's (Nov 2025):** long-running agents mark features complete after unit tests/curl checks pass; the fix that worked was NOT more process — it was forcing browser-automation testing "as a human user would" plus a feature list where every feature starts as "failing."
3. **Practitioners who abandoned structured frameworks abandoned them for the same reason:** artifacts accumulated, software didn't. Quantified overhead: 5x token usage vs. plain prompting (spec-kit), 3.5 hours human review + 2,577 lines of markdown to get ~700 lines of buggy code (Scott Logic), 12–16 hours before first line of code (BMAD).
4. **Practitioners who succeeded with spec-driven approaches all attribute success to end-to-end acceptance tests as the completion gate** — not to specs, gates, or review agents ("comprehensive end to end acceptance tests... 20x ROI" — HN user canterburry).
5. **Horizontal decomposition is independently identified as the integration-debt engine:** "Integration risk concentrates at the end. All layers... get built before anything runs end-to-end" (superpowers issue #1173, Apr 2026); the proposed cure across sources is vertical slices with a Slice-0 walking skeleton.
6. **The ecosystem trajectory in 2025–2026 is bifurcation, not doubling down:** heavy frameworks (spec-kit 6–7 step flow, BMAD) are being simplified (spec-kit issue #2673 requests a 3-step mode), migrated away from (OpenSpec switchers), or replaced by native harness features (Claude Code plan mode, `/goal` commands).
7. **The counter-trend that gained traction ("Ralph loops"/loop engineering) is radically simpler than Momentum, not more elaborate:** a bash loop, one task per fresh-context iteration, verification backpressure — and its documented failures are spec-quality failures ("the specs were way off base"), not loop failures.
8. **"AI test theater" is a named 2026 concept:** green test suites that verify nothing user-visible; multiple sources warn that agent-written tests reinforce existing behavior rather than verify intended behavior.
9. **Spec drift is reported as intrinsic to iterative multi-story work:** "Story 1.4 task list became outdated based on discoveries from Stories 1.1–1.3" (BMAD issue #446) — matching nornspun's 302-story backlog churn (28 dropped, 19 obsolete).
10. **No practitioner account was found of a solo developer running a practice at nornspun's ceremony level (multi-agent sprints + plan gates + QA/review/E2E agents + transcript-audit retros) and reporting shipped end-to-end features.** The searches run to establish this are listed in "Counter-evidence & falsifiability."

---

## Body

### 1. Direct hits: "all tasks done, nothing works" accounts

#### 1.1 Anthropic engineering — "Effective harnesses for long-running agents" (2025-11-26)

Anthropic's own team, building a claude.ai clone with long-running Claude agents, documented the exact failure mode under investigation, from the builder-of-the-model's vantage point:

> "Claude's tendency to mark a feature as complete without proper testing. Absent explicit prompting, Claude tended to make code changes, and even do testing with unit tests or `curl` commands against a development server, but would fail [to] recognize that the feature didn't work end-to-end."

A second failure mode compounds it across sessions:

> "After some features had already been built, a later agent instance would look around, see that progress had been made, and declare the job done."

What fixed it (OBSERVED in the article; the causal claim is theirs):

- **Browser automation testing as a user:** "Claude mostly did well at verifying features end-to-end once explicitly prompted to use browser automation tools and do all testing as a human user would."
- **A feature list (structured JSON, 200+ features) where every feature starts marked "failing"** — completion is a state transition earned by verification, not an agent's self-report.
- **One feature per session** with mandatory commits and progress-file updates.

Source: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

**Significance for our question:** the fix was verification-shaped, not process-shaped. They did not add more review stages, more specs, or more agents — they changed what "done" means (app behaves correctly under user-level driving) and who is allowed to declare it (a harness-tracked state, not the implementing agent).

#### 1.2 spec-kit Discussion #1482 — TyrelCB abandons spec-kit (2026-01-24)

First-person, dated, verbatim:

> "Not delivering a functional feature - nice spec though!!"
> "Using all my premium tokens - 5x token usage over a vibe code"

TyrelCB discontinued spec-kit and switched to Claude Code's plan mode when it shipped. Source: https://github.com/github/spec-kit/discussions/1482

The same thread carries the maintainer-abandonment subplot: users asking "Is SpecKit *really* maintained?"; maintainer mnriem promised "a flurry of activity" (2026-01-28) and shipped v0.0.91 (2026-02-09). Even GitHub's flagship SDD tool went through a visible confidence crisis in early 2026.

#### 1.3 spec-kit Discussion #1686 — sholtomaud: "great specs - no MVP" (2025-10-30 → abandoned 2026-02-27)

> "after several hours work, I have a wonderfully specified app, but the implementation is poor"

Two structural critiques directly relevant to Momentum:

- **Spec-vs-implementation disambiguation is unsolved:** "is the issue an issue in the specifications or an issue in the implementation?" — no workflow exists to distinguish whether a bug is a spec defect or a codegen defect, so fixes thrash between layers.
- **Cost inversion:** "the $ cost of time writing/rewriting specs is costing me more than the $ cost of writing code."

He explicitly names the MVP risk — extensive specification work without a shippable product ("great specs - no MVP") — and by 2026-02-27 posted that he had **"Abandoned spec-kit"** and was still searching for a repeatable workflow, citing LLM non-determinism. Source: https://github.com/github/spec-kit/discussions/1686

#### 1.4 spec-kit Discussion #1784 — NaikSoftware: "the illusion of work" (2025-09-08)

> SpecKit "creates the illusion of work, generating a bunch of text" — "thousands of lines of instructions" and "hundreds of unnecessary tests, most of which make no sense."

His conclusion: direct LLM prompting beat the whole apparatus for his refactoring work. Notably, the thread contains structured rebuttals (see Counter-evidence): amondnet reports success across 20+ projects with sub-agent patterns; fabiodouek reports first-shot working code *after* an initial spec-tuning investment. Source: https://github.com/github/spec-kit/discussions/1784

#### 1.5 BMAD-METHOD Issue #446 — screwyprof, solo dev, brownfield (2025-08-16/18; ~12.5 months old, labeled)

The closest analog to the Momentum practice in the wild — a solo developer running BMAD's multi-agent pipeline (SM/PO/Dev agents) on a real project. Four findings map one-to-one:

1. **Completion without validation:** "Dev agent acknowledged checklist requirement but then ignored it... attempts to mark tasks complete WITHOUT running checklist."
2. **Agent isolation / orchestration by human relay:** "Agents operate in complete isolation... PO validation invisible to other agents. I must relay all information between agents. No shared context or memory."
3. **Spec drift across a story sequence:** "Story 1.4 task list became outdated based on discoveries from Stories 1.1–1.3."
4. **No feature-level organization:** "forces all requirements into single massive documents" — stories exist, features don't, so nothing in the process owns "the user can do X."
5. **Instruction-following failure:** "Story 1.1 contained explicit link to technical analysis. Dev proceeded without reading referenced documentation."

No maintainer response was recorded on the issue. Source: https://github.com/bmad-code-org/BMAD-METHOD/issues/446

#### 1.6 HN "Spec-Driven Development: The Waterfall Strikes Back" thread (2025-11)

- **thomascountz** (spec-kit): spent "many many hours—tweaking, asking, correcting, analyzing, adapting" pre-code; after the agent produced thousands of lines, realized "it hadn't built the right thing"; the workflow lacked "iterative end-to-end feedback."
- **constantcrying** (systemic): the "tiniest feature... requires extremely complex manipulation of the spec" — SDD replicates waterfall's fatal flaw of "increasing complexity... to keep code and spec consistent."

Source: https://news.ycombinator.com/item?id=45935763

### 2. Quantified overhead accounts

#### 2.1 Scott Logic / Colin Eberhardt — Spec Kit measured end-to-end (2025-11-26)

The only account found with full instrumentation. Rebuilding a previously-deleted ~1,000-line feature (circuit management CRUD + GPS in a PWA) via Spec Kit:

| Stage | Agent time | Human review |
|---|---|---|
| Constitution | 4 min | 5 min |
| Specification | 6 min | 15 min |
| Plan | 8.5 min | **2 hrs** |
| Tasks | 8.5 min | **2 hrs** |
| Implementation | 13.25 min | 30 min |
| **Total** | **33.5 min** | **~3.5 hrs** + 2,577 lines of markdown |

Result: ~700 lines of working code **containing an obvious uninitialized-variable bug**, which he fixed by reverting to iterative chat ("vibe coding"). His baseline iterative approach on the same feature: ~8 min agent time, 15 min review, no bug — **~10x faster**. Verdicts, verbatim:

> "Code is law because it is formal language you can reason about. Specifications lack this formality."
> "Asking an agent to write 1000s of lines of markdown rather than code is a misuse of this technology."

Source: https://blog.scottlogic.com/2025/11/26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html

#### 2.2 Birgitta Böckeler (Thoughtworks, on martinfowler.com) — Kiro, spec-kit, Tessl hands-on (2025-10-15)

- Kiro inflated a minor bug fix into **4 user stories with 16 acceptance criteria** — "using a sledgehammer to crack a nut."
- Abandoned a spec-kit feature mid-implementation, suspecting plain AI coding would have been faster.
- "I'd rather review code than all these markdown files."
- **Structure did not buy determinism:** despite constitutions and checklists, agents ignored instructions, duplicated existing classes, over-executed. She calls the resulting risk profile "inflexibility *and* non-determinism" (the Model-Driven Development failure repeated) and invokes *Verschlimmbesserung* — making something worse by improving it.

Source: https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html

#### 2.3 BMAD on a personal project — Dan Gurgui (dev.to, 2025-12-30)

- **12–16 hours** of planning/docs before the first line of code.
- "Party mode" multi-agent sessions "absolutely exhausted my context window and usage credits."
- A **false-progress loop**: "The assistant made reasonable local code changes that never converged on the real problem" — 6-hour debugging spiral rooted in an architecture choice (NestJS-on-Lambda) the process itself had steered him into.
- Balanced verdict: "patience in exchange for momentum" — he kept BMAD, crediting stories ("once you have good stories, execution becomes much more mechanical") and retrospectives ("stop patching and start diagnosing").

Source: https://dev.to/arch4g/my-experience-using-the-bmad-framework-on-a-personal-project-patience-required-28aa

#### 2.4 BMAD rejected at evaluation — Pete / grid0 (2025-05-28; ~14 months old, labeled)

> BMAD is "brilliant but _way_ too complex. Hundreds of files, state management, complex orchestration... it was fighting against Claude Code's natural abilities instead of embracing them."

He built a ~14KB markdown-guidance alternative (claude-forge) instead. Source: https://grid0.substack.com/p/how-i-turned-claude-code-into-my

#### 2.5 Kiro field reports

- François Dexemple, "Brilliant, Broken, and Frustrating" (dev.to/Medium, 2025): "Tasks frequently get stuck, fail, and require numerous retries." Source: https://dev.to/aws-builders/brilliant-broken-and-frustrating-my-deep-dive-into-amazons-kiro-ai-ide-the-flawed-junior-gn5
- Post-GA (2025-11-17) accounts are more positive ("it's earned a permanent spot in my workflow" — Developers Digest guide), consistent with the pattern that spec-first works better once the tool matured and users scoped it to genuinely new features.

### 3. The integration-debt mechanism: horizontal decomposition

#### 3.1 obra/superpowers Issue #1173 — "Vertical slice development mode for large features" (2026-04-15, author cangencler)

A structured agentic framework (Jesse Vincent's superpowers) formally absorbing the lesson. The motivation section is a clean statement of the mechanism that produces story-done-feature-missing:

> "Integration risk concentrates at the end. All layers (data, logic, API, UI) get built before anything runs end-to-end."

Plus: users can't touch anything until the whole plan executes; monolithic plans exhaust context (issue #1152 burned a 5-hour token budget in one run); wrong architectural assumptions get discovered at 70% completion. The proposed fix: a slicing phase between spec approval and planning, with **"Slice 0: a walking skeleton providing minimal end-to-end functionality through all architectural layers,"** subsequent slices ordered by dependency/value/risk, and re-evaluation after each slice ships. Source: https://github.com/obra/superpowers/issues/1173

#### 3.2 Corroborating vertical-slice-for-agents sources

- Edward Yang's "AI Blindspots — Walking Skeleton": get the thinnest end-to-end system working first, because agents (like juniors) otherwise build layers that have never met. Source: https://ezyang.github.io/ai-blindspots/walking-skeleton/
- Jeremy D. Miller, "The Codebase Is the Prompt" (2026-06-04): vertical-slice architecture as the codebase organization that lets agents load one feature's full stack in-context. Source: https://jeremydmiller.com/2026/06/04/the-codebase-is-the-prompt-wolverine-vertical-slices-and-ai-assisted-development/

**INFERRED:** story decomposition that follows architectural layers or component boundaries (backend endpoints in one story, client screens in another, wiring in a third) reproduces the horizontal anti-pattern *inside* a sprint even when each story has passing Gherkin ACs — because no story's AC is "a user completes the journey."

### 4. What people changed: abandon / simplify / double-down-with-verification

Three distinct trajectories appear in the record. Almost no one's fix was "add more process."

#### 4.1 Abandonment (process → plain iterative agent use)

- Eberhardt (§2.1): rejected Spec Kit, returned to iterative prompting — 10x faster, fewer bugs.
- TyrelCB (§1.2): dropped spec-kit for Claude Code plan mode.
- sholtomaud (§1.3): "Abandoned spec-kit," still searching.
- NaikSoftware (§1.4): direct prompts beat the pipeline.
- Answer.AI on Devin (2025-01-08; **older than 12 months, labeled**): 3/20 tasks succeeded, 14 failed; "the most frustrating aspect wasn't the failures themselves but rather how much time the team spent trying to salvage these attempts." They returned to tighter human-in-loop tools. Source: https://www.answer.ai/posts/2025-01-08-devin.html

#### 4.2 Simplification (heavy framework → lightweight persistent specs)

- **OpenSpec switchers.** RK / ridakaddir (2026-04-04): spec-kit's 7 steps "felt like filling out a permit application to move a chair"; ~800 lines of artifacts to review before coding; switched to OpenSpec's 3-phase flow (propose/apply/archive) with delta specs (ADDED/MODIFIED/REMOVED) and now specs even two-endpoint changes he previously skipped. "The best tool is the one you actually use." Source: https://ridakaddir.com/blog/post/openspec-vs-spec-kit-why-i-switched
- **spec-kit itself capitulating:** Issue #2673 requests optional merged commands compressing the 6-step flow to 3 because OpenSpec migrants find `clarify`/`plan` "redundant, adding unnecessary overhead." Source: https://github.com/github/spec-kit/issues/2673
- **Pete/claude-forge (§2.4):** BMAD → 14KB of markdown guidance.
- **Harness absorption:** by May 2026, Codex/Claude Code/Hermes shipped `/goal`-style commands natively covering what custom orchestration scripts did (Pragmatic Engineer, 2026-07-14). Source: https://newsletter.pragmaticengineer.com/p/what-is-loop-engineering

#### 4.3 Double-down — but on *verification*, not ceremony

- **HN canterburry** (2025-11): stays spec-driven, 2–3 hours per spec emphasizing "acceptance criteria," ships a "working, tested next version" daily; credits "comprehensive end to end acceptance tests" with "20x ROI." The spec investment pays because the completion gate is E2E behavior.
- **Anthropic (§1.1):** kept long-running autonomy, added browser-automation user-level testing + failing-by-default feature list.
- **Geoffrey Huntley** (Aviator podcast, 2026-06-18): "If you run an agent without some form of verification, without backpressure in the inferencing loop, you get slop in, slop out." And on copying elaborate setups: "every company cargo-culted that [the Spotify model] into their organization without considering whether it was the right thing to do... When one of those companies figures out the right thing and publishes a case study, everyone is going to copy it." Source: https://www.aviator.co/podcast/geoffrey-huntley-drak-factory
- **fabiodouek** (spec-kit #1784): success after upfront spec-tuning — subsequent features "first-shot working code."

#### 4.4 The Ralph-loop counter-model (simplicity + fresh context + one task)

Geoffrey Huntley's Ralph technique — "In its purest form, Ralph is a Bash loop: `while :; do cat PROMPT.md | claude-code; done`" — became the viral counter-model to multi-agent orchestration (Pragmatic Engineer, 2026-07-14; HumanLayer "A Brief History of Ralph," 2026-01-06):

- Documented wins: six repos shipped overnight; a React codebase refactored to standards in 6 hours; a toy language ("Cursed Lang") built end-to-end. Named practitioners with outcomes: Paul D'Ambra (PostHog) — 13 flaky-test-stabilization PRs; Ivan Pantić — Sentry-triage loop capped at one concurrent PR; Rafel Mendiola — React→React Native migration via scheduled loops instead of "50–100 traditional tickets."
- Documented failure: a GTD tool "failed because 'the specs were way off base' despite ralph generating both" — i.e., **the loop executes faithfully; spec quality is still the binding constraint.**
- Dex Horthy's sizing principle: "waking up to one small refactor every morning is better than both waking up to none and waking up to 50."
- Criticisms (Pragmatic Engineer): agent drift, human-in-loop outperforming autonomy for some, token cost; Max Kanat-Alexander: "The 'loop' might have just been a temporary hack while harnesses added ability to do same from single prompt."

Sources: https://newsletter.pragmaticengineer.com/p/what-is-loop-engineering ; https://www.humanlayer.dev/blog/brief-history-of-ralph

### 5. "AI test theater" — why passing gates prove little

- Autonoma (2026): "AI test theater is false test coverage: AI-written tests go green while real bugs ship." Source: https://getautonoma.com/blog/what-an-ai-qa-agent-actually-does
- HN "AI agent benchmarks are broken" discussion: agent-generated tests "reinforce the existing behavior of the code" rather than verify intended behavior; "a benchmark that agents can game produces exactly the wrong signal: high scores on tasks that were never genuinely completed." Source: https://news.ycombinator.com/item?id=44531697
- Augment Code, "Why AI Coding Agents Fail E2E Tests": most teams discover the gap "reactively: AI-generated code passes unit tests but violates architectural patterns, breaks API integration contracts" — surfacing only in production. Source: https://www.augmentcode.com/guides/why-ai-coding-agents-fail-e2e-tests

**INFERRED synthesis:** a multi-stage gauntlet (code review agent → QA agent → E2E agent → end-gate) does not defeat test theater if every stage evaluates *artifacts of the story* (diff, ACs, story-scoped tests) rather than *driving the assembled application*. Each stage can honestly pass while the composed system has never been exercised. This is precisely the Anthropic finding: unit tests and curl checks passed; the feature didn't work.

### 6. The waterfall-regression critique (context for why the wall exists)

- fzaninotto, "Spec-Driven Development: The Waterfall Strikes Back" (2025-11): agents rarely produce correct output first try, so the iterate-anyway reality "defeats the purpose" of big design upfront. Source: https://news.ycombinator.com/item?id=45935763
- Jk1484, "The Agentic Waterfall" (HN 2026-02-10): "async workflow = sync workflow + formalization cost + context reload"; if no one who understands the code is in the loop during creation, review happens after the fact — waterfall by construction. Source: https://github.com/Jk1484/agentic-waterfall
- JM del Pino, MakerX (2026-02-11): lands on the hybrid — "vibe my way to a good spec, then let the agent execute it"; agents "just pick one" when ambiguity would make a human ask. Source: https://blog.makerx.com.au/the-agents-are-here-and-were-all-doing-waterfall-again/
- Thoughtworks (2025) framing of why SDD arose at all: intent drift, context decay, unverifiable output. Source: https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices

---

## Resonance with our situation

Mapping the external record to the nornspun capsule (solo dev; Momentum multi-agent sprints; plan gates; Gherkin story specs; QA/code-review/E2E/AVFL agents; retro transcript audits; 10 sprints/4 months; 302 stories, 91 done; no end-to-end feature works; sprint-2026-07-13 finished all 12 stories, end-gate approved, app unusable):

1. **MAPS — the headline failure is the field's headline failure.** "All 12 stories done, end-gate approved, app can't do the simplest things" is TyrelCB's "Not delivering a functional feature - nice spec though!!" and Anthropic's "fail to recognize that the feature didn't work end-to-end," at sprint scale. This is not an idiosyncratic Momentum bug; it is the characteristic failure of story/task-anchored agentic processes whose completion signal is artifact-level.
2. **MAPS — 302 stories / 91 done / 0 working features is "great specs — no MVP" at scale.** sholtomaud's cost inversion (spec effort > code effort) and NaikSoftware's "illusion of work" predict exactly this artifact-rich, capability-poor end state.
3. **MAPS — ceremony level.** Momentum is *heavier* than every framework practitioners abandoned as too heavy: BMAD was rejected as "way too complex" with "hundreds of files"; spec-kit's 6 steps drew a "permit application to move a chair"; Momentum adds plan gates, team composition, AVFL, transcript-audit retros, practice ledgers on top. Every documented simplification pressure applies a fortiori.
4. **MAPS — spec drift.** "Story 1.4 task list became outdated based on discoveries from Stories 1.1–1.3" (BMAD #446) is structurally identical to a 302-story backlog with 28 dropped + 19 obsolete and features.json noting wizard files "built then deleted."
5. **MAPS — the fix direction is convergent and specific.** The three documented cures: (a) completion = user-level E2E behavior, enforced by driving the real app (Anthropic's browser automation; canterburry's E2E acceptance tests; for the Compose client, the analog is the existing maestro/ flows as the story-completion gate, not a post-merge stage); (b) failing-by-default feature registry — a feature is "failing" until verified, never "done because its stories are done" (nornspun's features.json exists but sits at "partial", which is the right artifact with the wrong enforcement); (c) vertical slices with a Slice-0 walking skeleton so something end-to-end works from week one.
6. **PARTIALLY MAPS — "we have E2E agents" is not a defense.** The field evidence says what matters is whether verification *drives the assembled app as a user* and whether its verdict *blocks* story/sprint completion. An E2E stage that runs per-story in a worktree, or that can be waived at an end-gate, is test theater in the §5 sense. (Whether nornspun's E2E stage actually drove the app is for the internal-evidence agents to establish; the external record only says the stage's existence proves nothing.)
7. **DOES NOT MAP — model capability is not the story.** The Devin postmortem (older, Jan 2025) blames raw agent capability (3/20 tasks). Nornspun's stories individually pass review and QA — the 2026 record locates the problem in the completion signal and decomposition, not in the agents' ability to write code.
8. **DOES NOT MAP — total abandonment is not the field's answer for greenfield-scale work.** The successful accounts kept structure (specs, acceptance criteria, loops) and *changed the definition of done*. canterburry and fabiodouek show spec investment paying off — when gated on E2E behavior. The evidence supports a process diet + verification transplant, not process deletion.
9. **MAPS — retro/audit machinery does not catch this failure class.** Nornspun ran retros with transcript audits for 10 sprints while the wall built. Externally, nobody reports their review/retro layer catching story-done-feature-missing — it was always the human opening the app (Eberhardt found the bug by using the feature; the nornspun developer found it by opening the app). Audit layers audit the process; only running the product audits the product.
10. **MAPS (weak signal, worth flagging) — solo + multi-agent compounds the relay problem.** screwyprof: "I must relay all information between agents." A solo developer is the only integration point between agents; every agent-to-agent seam (12 stories × pipeline stages) is a place where system-level intent exists in no agent's context. Momentum's orchestrator (conduct) automates the relay but not the *ownership of the user journey* — no agent's success criterion is "the user can do the thing."

---

## Counter-evidence & falsifiability

**Evidence cutting against "structured agentic frameworks don't deliver":**

- **Successes with the same tools exist and are first-person:** amondnet (spec-kit #1784) — 20+ projects with sub-agent patterns; fabiodouek (same thread) — first-shot working code after spec-tuning investment; canterburry (HN) — daily working versions with production deploys; Dan Gurgui kept BMAD and credits it with rescuing him from a debugging spiral via retro; post-GA Kiro users report it as a permanent workflow fixture. The variable separating success from failure in these accounts is E2E-behavior gating and scoping the ceremony to genuinely new/complex work — not the presence or absence of the framework.
- **Selection bias is severe.** People who hit walls write postmortems; people quietly shipping write less, or write promotional content that is hard to verify. GitHub issues over-sample the frustrated. Counts here are of accounts found, not population rates.
- **Some headline critiques are analytical, not experiential.** The "Agentic Waterfall" HN thread (checked via Algolia API, item 46960638) contained only 4 comments, all structural argument, no first-person workflow experience — I have not treated it as experiential evidence.
- **Tool immaturity confound:** several failure accounts (Kiro preview mid-2025, spec-kit pre-v0.0.91) predate significant tool fixes; the same workflow on 2026 tooling might fare better.

**What would prove this report's thesis wrong:**

1. Multiple verifiable accounts of solo developers running BMAD/Momentum-grade multi-agent ceremony for months and shipping working end-to-end products *without* user-level E2E completion gates — I searched for these (queries below) and found none, but absence of evidence is weak here given selection bias.
2. Internal nornspun evidence showing the E2E/AVFL stages *did* drive the assembled app as a user and passed honestly — that would relocate the failure from "completion signal" to something this external record does not explain (e.g., environment/config drift between validated worktrees and the developer's runtime).
3. Data showing spec-kit/BMAD retention improving through 2026 without simplification — the observed trend (issue #2673, OpenSpec migration, maintainer crisis) currently points the other way.

**Negative-claim search disclosures (the exact searches run):**

- *"No practitioner account found of nornspun-ceremony-level solo practice succeeding":* searched `"multi-agent" coding orchestration "not worth it" OR "went back to" single agent solo developer blog 2026`; `solo founder AI agents months "burned" tokens "nothing to show" OR "no shippable" retrospective 2026`; `r/ClaudeAI OR r/ChatGPTCoding BMAD method review months later "too much process" OR overkill OR "slowed me down"`; `reddit ClaudeAI "BMAD" months "nothing works" OR "still don't have" OR "no working" product`. Found success stories only at lower ceremony levels (single agent + specs, or loops) or in unverifiable promotional content ($1M-ARR listicles).
- *"No maintainer reply on BMAD #446":* per the fetched issue page content as of 2026-08-02.
- *"Agentic Waterfall thread has no experiential comments":* verified by fetching https://hn.algolia.com/api/v1/items/46960638 (4 comments total).
- A targeted Algolia comment search (`bmad stories`, tags=comment) returned only false positives — HN comment-level BMAD experience reports were NOT located beyond the threads cited; the BMAD experiential evidence here rests on GitHub issue #446, dev.to, and Substack accounts.

---

## Open questions

1. **Base rates are unknowable from public accounts.** What fraction of structured-framework users hit the wall vs. ship? No survey data found; only DORA-style vendor claims (e.g., "88% of AI agent projects never reach production" — Enlight Lab, methodology unverified) which I do not endorse as rigorous.
2. **Whether nornspun's E2E stage actually drove the running app** (Maestro flows against the desktop/Android client; browser/API driving for the backend) is the pivotal internal fact this external record cannot supply. The entire resonance argument sharpens or collapses on it.
3. **Long-run outcomes of the simplifiers.** OpenSpec switchers and claude-forge users report early satisfaction (≤ 6 months); no 12-month follow-ups found showing whether lightweight-spec practices scale past the honeymoon.
4. **Tessl's spec-as-source trajectory** — Böckeler flagged it as the boldest and riskiest variant (Oct 2025); I found no 2026 first-person postmortems of Tessl in production, only the company's own content. Unresolved.
5. **Whether native harness features (plan mode, `/goal`) durably replace frameworks** or just reset the complexity cycle — Kanat-Alexander's "temporary hack" hypothesis is plausible but untested; the same completion-signal problem could reappear inside `/goal` loops without user-level verification.

---

*Compiled 2026-08-02 by the external-research discovery agent for the nornspun delivery discovery. All URLs verified reachable on this date except where noted (HN item pages rate-limited; verified via hn.algolia.com API).*
