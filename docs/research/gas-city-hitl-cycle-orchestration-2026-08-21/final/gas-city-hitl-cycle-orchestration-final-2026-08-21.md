---
title: "Gas City HITL gates and cycle orchestration for Momentum — Research Report"
date: 2026-08-21
type: Technical Research — Consolidated Report
status: Complete
content_origin: claude-code-synthesis
human_verified: true
derives_from:
  - path: raw/research-gate-mechanics-handson.md
    relationship: synthesized_from
  - path: raw/research-human-verdict-patterns.md
    relationship: synthesized_from
  - path: raw/research-notification-watcher-layer.md
    relationship: synthesized_from
  - path: raw/research-cycle-orchestration-fit.md
    relationship: synthesized_from
  - path: raw/research-maturity-open-bugs.md
    relationship: synthesized_from
  - path: raw/research-beads-coupling-dec028.md
    relationship: synthesized_from
  - path: raw/research-hitl-alternative-patterns.md
    relationship: synthesized_from
  - path: raw/research-production-evidence.md
    relationship: synthesized_from
  - path: raw/research-verification-probes.md
    relationship: synthesized_from
  - path: raw/research-dec035-revisit-triggers.md
    relationship: synthesized_from
  - path: raw/gemini-deep-research-output.md
    relationship: synthesized_from
  - path: validation/avfl-final-status.md
    relationship: validated_by
  - path: raw/practitioner-notes.md
    relationship: informed_by
---

# Gas City HITL gates and cycle orchestration for Momentum

## Executive Summary

**DEC-035's deferral of Gas City stands. Do not adopt.** That is the developer's ratified verdict of 2026-08-25 (`raw/practitioner-notes.md`, Fork 1), and this corpus supports it on the evidence rather than merely recording it.

The reason is narrower and sharper than "Gas City is immature." The blocking mechanics Momentum would need are *proven* — reproduced end-to-end, twice, on two independent throwaway cities and two `bd` versions (VERIFIED-EMPIRICAL, `research-gate-mechanics-handson.md`:Q1–Q4). A gate bead blocks; manual closure releases the graph; the close reason persists as an audit trail. That half works today, in the `bd` 1.0.4 Momentum already has installed.

What does not work is the half the developer has since named non-negotiable. **A Gas City human gate blocks correctly and tells nobody.** A formula-cooked gate persists `await_type: null`; both bundled human-gate notification reflexes filter on `await_type == "human"`, so they silently skip every gate a formula creates (VERIFIED-EMPIRICAL for the null, VERIFIED for the filter). And those two reflexes are in **no tagged release** — they landed on `main` 2026-07-23, one day after the v1.4.0 cut, and are 404 at v1.3.5, v1.4.0, and v1.4.1 (VERIFIED-EMPIRICAL). On a `gc` you can actually install, creating a `type=human` gate produces zero notification by any path. Gas City's own order header says so in as many words: *"the human who must resolve it is never told (proven ABSENT in gascity/beads)."*

The developer's requirement, stated verbatim-in-substance at the decision gate: *"It needs better notifications. It's crucial we have back and forth and visibility with me (the HITL)."* That elevates the silent-gate finding from one of three gaps to **the disqualifying gap**. A gate whose mechanics are perfect and whose notification is absent fails the requirement outright, and no amount of proven blocking compensates.

Two further gaps sit behind it, either of which would independently block an out-of-session cycle:

- **The post-fan-out barrier has no reliable declarative expression.** Momentum's results gate is "wait for all of the conduct fan-out, then ask the human." `waits_for` is inert (#2311, open, no fix PR since 2026-05-29); container `needs` does not gate children (#3451, open, maintainer ruling 2026-06-28, still not landed); `[steps.tally]` was removed from the SDK. #3451's prescribed workaround — *enumerate the children explicitly in `needs`* — is unavailable to Momentum, whose story set is runtime-discovered at sprint-planning (VERIFIED). The corpus's own summary is the right line: **gates are fine; barriers are not.**
- **Adoption is a rewrite, not an integration.** The premise the research was commissioned on — chaining phases via `exec` steps running `claude -p /momentum:*` — is refuted. There is no `exec`, `command`, `run`, or `script` key in a v2 formula step, and unknown step keys are *silently ignored* (VERIFIED, `research-cycle-orchestration-fit.md`:§1). Adoption means re-expressing Momentum's phase orchestration as a Gas City pack: on the order of **15–25 days** for the orchestration rewrite, on top of **5.5–9 days** of gate glue that is **for one gate type only** and **excludes the uncosted standup of a live Momentum city**. Both are rough sizings from analogous pack scope — floors for a go/no-go, never committed numbers.

**What would change the verdict.** DEC-035's clause is conditioned on a *goal appearing*, not a capability existing: *"revisit only if/when an out-of-session or multi-Conductor goal appears."* Neither has. If the out-of-session goal ever does appear, the first thing to prove is not the gate — it is the **notification and verdict-return layer**, per the developer's ratified requirement. The pre-flight sequence is in Recommendations: notification layer first, then four named probes, then barrier construction, then a re-estimate.

This corpus files as the evidentiary baseline for that future revisit. It survived four adversarial validate-fix iterations and closes carrying seven honest open items, enumerated in Known Limitations.

---

## 1. What the decision actually turns on

DEC-035 D2 (2026-05-30), verbatim:

> Execution substrate = the in-session dynamic Workflow tool. **Gas City is deferred** — this supersedes DEC-032's adoption of Gas City as *the* dispatcher; revisit only if/when an out-of-session or multi-Conductor goal appears.

Two things follow, both easy to lose (VERIFIED, `research-dec035-revisit-triggers.md`). First, the clause names a *test about Momentum's intentions*, not about Gas City's capabilities. **A capability existing is not a goal appearing.** Ten research files can establish in exhaustive detail whether Gas City would support out-of-session dispatch, and none can fire a clause whose condition is whether the developer wants it. DEC-035 already recorded the position — *"high throughput with deep delegation … and explicitly no out-of-session / away-from-keyboard dispatch yet"* — and nothing since 2026-05-30 records it changing; the developer confirmed it stands on 2026-08-25.

Second — and easily missed — DEC-035's rationale points the **multi-Conductor** trigger at *beads*, not at Gas City: *"Beads' headline win — atomic `--claim` against concurrent dispatchers — only matters out-of-session / multi-Conductor."* If Momentum ever wants two Conductors, the requirement that generates is atomic claim over the story frontier, which DEC-028 already has a spike for. It does not automatically point at an orchestrator.

The corpus was commissioned to produce the evidentiary basis for exercising the clause. What it actually produces is the basis for deciding whether to *pursue* such a goal — the prior question, and the developer's to answer. He answered it: not yet.

---

## 2. Gate mechanics: the half that works

This is the strongest evidence in the corpus, and it is worth stating precisely because everything downstream depends on knowing exactly what was proven.

`gc` 1.4.1 installed cleanly via the mise github backend, artifact attestations verified (VERIFIED-EMPIRICAL, `research-gate-mechanics-handson.md`). A minimal three-step v2 formula (`A → B(gated) → C`) with `[steps.gate] {type="human", id="test-gate"}` compiles to **five** steps — the compiler injects `gate-b` before `b`, rewrites `b`'s needs, and appends a `workflow-finalize` control bead. Then (all VERIFIED-EMPIRICAL):

- **The gate bead is real** — `issue_type: gate`, title exactly `Gate: human test-gate`, matching the compiler source in `internal/formula/compile.go`, with a `BLOCKS` edge to the gated step.
- **The gated step is excluded from `bd ready`, and the gate is the exclusive blocker.** After closing Step A, `bd ready` returned "No ready work found" and `bd blocked` reported exactly one open dependency — the gate. The workflow-root edge is structural, not readiness-blocking.
- **Manual closure releases the graph immediately** — `bd close <gate>`, or the named equivalent `bd gate resolve <id> --reason "…"` — and **the close reason persists on the bead**. That is a directly usable substrate for Momentum's anti-rubber-stamp requirement: the written per-fork verdict lands in the audit trail, not just a chat transcript.
- **The graph drives to completion** — closing each released step in turn walked the whole DAG through `workflow-finalize` to the root.
- **Gate beads are hidden from plain `bd list`** (`bd list --type gate` / `bd gate list` show them). A Momentum surface enumerating work via `bd list` will not see its own gates.

One further property matters for mid-story gates and needs its scoping carried intact. **An open gate also refuses `bd close` on the gated step** — `cannot close … blocked by open issues (use --force to override)`. That is stronger than a readiness filter: an agent cannot self-certify gated work as done without an audit-visible `--force`. But the refusal was reproduced against a **timer** gate, not a human one. The enforcement lives in beads' dependency-closure check, which does not read gate `type`, so the claim is gate-type-agnostic *by code path* — and therefore **INFERRED for `human` gates specifically**, not independently re-run (Q2 bonus finding).

An independent probe corroborates all of it on Momentum's own installed `bd 1.0.4` — `bd gate create --type=human --blocks <story>` removed the story from `bd ready`; `bd gate resolve` returned it (VERIFIED-EMPIRICAL, `research-human-verdict-patterns.md`:§5). **`human` is the default gate type.** One caveat on the rejection path: **reopen is one-shot forward** — reopening a gate after its gated step already closed does not claw the step back, so "reject the plan, send it back" must either reopen gate *and* downstream steps explicitly, or model rejection as a distinct branch.

### The standing prerequisite behind every gate recommendation

This is settled, not open, and it is the single easiest thing to drop when citing this corpus. **A `bd` gate gates only work dispatched through `bd ready`.** Momentum's Conductor computes its frontier from `.momentum/stories/index.json` + `depends_on` under the DEC-028 dual-write spike. An open gate bead would be a real, correctly-blocking bead that the Conductor never consults — it would block nothing the Conductor schedules.

So every "adopt `bd gate --type=human` today, free" recommendation in this corpus is true of the **primitive** and not yet of the **effect**. Making these gates load-bearing requires moving dispatch onto `bd ready` — DEC-028's still-open go/no-go — or adopting Gas City in full, under which the condition holds by construction because phase and story work become city beads dispatched from the bead frontier (VERIFIED, stated at `research-human-verdict-patterns.md`:§5 and §8, `research-hitl-alternative-patterns.md`:§7 preamble).

---

## 3. The notification gap — the disqualifying finding

### What is broken

The `[steps.gate]` `type` vocabulary — `gh:run`, `gh:pr`, `timer`, `human`, `mail` — is doc-comment text in `internal/formula/types.go`. The spec files it under "Accepted But Inert": *"the parser never validates them and no bundled watcher acts on them. Zero bundled formulas use `gate`"* (VERIFIED, formula-spec-v2 §4).

For `type = "human"`, inertness costs nothing at **resolution** — closing the gate bead *is* the approval, and no watcher is wanted (`bd gate check` deliberately never auto-closes human gates, exactly the fail-safe Momentum needs). But **notification is a second, separate consumer of `type`, and there it is not free.** The measurement, same store, two creation paths (VERIFIED-EMPIRICAL, `research-gate-mechanics-handson.md`:"The defect"):

```
formula-cooked:  {"id":"gt-crp","issue_type":"gate","title":"Gate: human test-gate","await_type":null}
bd gate create:  {"id":"gt-cvl","issue_type":"gate","title":"Gate: human","await_type":"human"}
```

The ad-hoc path persists `await_type`; the formula path does not. The compiler *does* carry the values into the recipe, so the loss happens on the cook/materialize path into the bead store, not at compile time (VERIFIED, code-read). `timeout` is lost the same way — a formula-cooked `type="timer" timeout="5s"` gate was still open after seven seconds with `bd gate check` reporting "Checked 0 gates", while an ad-hoc timer gate auto-resolved perfectly.

Both bundled human-gate reflexes filter on the same predicate — `[ "$AWAIT_TYPE" = "human" ] || continue` — so **both silently skip every gate a formula creates**. The one construct that most needs the notify is exactly the construct the notify cannot see.

### The release gap makes it worse

Neither notify order is in a tagged release. Enumerating `internal/bootstrap/packs/core/orders` at v1.4.1 and v1.4.0 returns `gate-sweep.toml` but **not** the two notify orders; raw fetches of both at v1.4.1, v1.4.0, and v1.3.5 all 404 while `gate-sweep.toml` at v1.4.1 returns 200 (VERIFIED-EMPIRICAL). The commit that added them (PR #4553, 2026-07-23) missed the v1.4.0 cut by one day and has not landed in a release since. They ship only in the `edge` rolling-main pre-release the maintainers label *"not for production."*

And `gate-sweep`, the one gate watcher that *does* ship, is two lines: `gc bd gate check --type=timer --escalate` and `--type=gh --escalate`. Human gates are excluded by design — correctly, since they must never auto-close — but it means nothing in a released `gc` observes them at all.

### The last mile stops short even with the orders

Suppose you vendor them. The terminal action is `gc mail send "${GC_ESCALATION_RECIPIENT:-human}"`, which writes a mail bead into a `human` inbox that nothing surfaces outside the city. Gas City's own comment states the constraint: `--notify` *"deliberately skips the tmux-nudge for the `human` recipient (humans have no session to poke)"* (VERIFIED). There is no push, no OS notification, no email/SMS bridge in core. Mail is also **not durable audit** — `gc order sweep-nudge-mail` closes read mail beads past a 1h default TTL, swept every 5 minutes, so a verdict left only in a mail body is gone within the hour (VERIFIED, `research-hitl-alternative-patterns.md`:§3).

Addressee routing is constrained too. Attempting `assignee = "human"` on a gated step fails at cook — *"assignee target 'human' did not resolve to a concrete session"* — so the addressee necessarily falls through to `$GC_ESCALATION_RECIPIENT`, which the mail path treats specially in exactly the way above (VERIFIED-EMPIRICAL).

The dashboard does not fill the gap. It is an SPA compiled into the `gc` binary and served same-origin by the supervisor at `http://127.0.0.1:8372/` — confirmed live, `curl -sI` → 200 (VERIFIED-EMPIRICAL, `research-verification-probes.md`:Probe 4). Its documented surface is agents/sessions, beads, mail, formula runs, health: **no gate view, no blocked-work queue, no alerting surface** (VERIFIED as to docs; INFERRED as to source — no dashboard source path is exposed at the repo root and code search requires auth). And for Momentum the deeper problem is the addressing model, not the missing view: a loopback single-operator dashboard is precisely wrong for a cycle running while the developer is elsewhere.

### The substrate is good; the reflex is missing

What *does* exist defines the build. The event bus is well-specified — a typed envelope with 91 event types, ten of them bead events (VERIFIED, `openapi.json`). There is **no `gate.*` event type**; a gate arrives as an ordinary `bead.created` whose `issue_type` is `gate`, selectable via `gc events --follow --type bead.created --payload-match bead.issue_type=gate`. Resumption is `--after <seq>` / `--after-cursor`; **with neither, streams start at the current event head**, so a watcher that restarts without a persisted cursor silently misses gates created in the gap. Two hops are unavoidable: the `bead.created` payload **omits `await_type`**, so any watcher must re-fetch the bead to learn whether a gate is human — Gas City's own notifier says so in a comment. A long-poll on `GET /beads?type=gate&status=open&index=N&wait=30s` may be simpler for a single-gate watcher; write-back is two authenticated POSTs (`/bead/{id}/update`, then `/bead/{id}/close`) behind an `X-GC-Request` header (VERIFIED).

The upstream notifier is a 222-line shell script and a near-exact template for what Momentum would otherwise write. So the honest gap statement is not "build a watcher." It is **build the last mile and the verdict return path** — and for Momentum's anti-rubber-stamp gate, the return path is the harder half.

Momentum's plan gate today is a rendered HTML page opened as a `file://` URL in a cmux browser surface. Its sign-off block requires a written one-line verdict per genuine fork before the submit button enables — and the button's only action is `navigator.clipboard.writeText(...)`, with the page instructing *"copy and paste the decision text back into the chat"* (VERIFIED-EMPIRICAL, local source: `sprint-planning/references/plan-gate-renderer.md`). **That clipboard-into-a-live-session hop is the thing an out-of-session cycle breaks.** There is no chat to paste into. Everything else — notification, blocking, release — Gas City models; the verdict *return* path does not exist in any form. Re-targeting the renderer from a `file://` clipboard page to a served page issuing two authenticated POSTs is the ~3–5 day core of the glue estimate.

---

## 4. Carrying a human verdict: which primitive, and why the obvious one is wrong

Gas City has two loop primitives, and **only the deprecated one has a human gate** (VERIFIED, `research-human-verdict-patterns.md`:Headline).

**`[steps.check]` / `[template.check]`** is what every maintained pack uses — 57 occurrences across `gascity-packs` against **zero** `[steps.gate]` (VERIFIED-EMPIRICAL). It is a **poll-and-burn** loop: an exec script runs after each attempt; exit 0 stops; exit 1 spawns the next attempt; **exhaustion closes the step failed**. No waiting state, no human affordance.

A check script *can* read a human-recorded verdict — mechanically trivial. The verdict is ordinary bead metadata, and nothing in the read path checks actor provenance; a human-written verdict is indistinguishable from an agent-written one (VERIFIED-EMPIRICAL round trip on `bd` 1.0.4). But **semantically it is the wrong primitive**: the check loop does not wait. If the human has not yet recorded a verdict, the script exits 1 and the orchestrator **respawns another agent iteration of the work** — it redoes the job and asks again. With `max_attempts = 6` and a human on a lunch break, the loop burns its budget and closes the step failed. You can hack a blocking `until` loop into the script, but then you hold a dispatch slot hostage against `check.timeout` (10m in shipped packs), and a timeout is not "keep waiting."

A hard structural constraint compounds this: **`check` must not be combined with `loop`, `on_complete`, `gate`, `expand`, `assignee`, or `retry`.** One step cannot carry both a check loop and a gate, so Momentum's "iterate until the reviewer is satisfied, then ask the human" needs *two* steps: `review-loop` (check, agent verdicts) → `human-gate` (gate, blocks on the person).

**`gc converge --gate manual`** is the genuinely well-built HITL primitive — and it is unreachable. It has everything the check loop lacks: a `waiting_manual` state that parks indefinitely, operator verbs (`approve` / `iterate` / `stop`), built-in actor attribution (`convergence.terminal_actor = "operator:" + username`), a three-value vocabulary, and **fail-closed normalization** — `NormalizeVerdict` maps anything unrecognized, including empty, to `block`. But it accepts only v1 formulas and rejects v2 outright, and a formula must set `convergence = true` to qualify — **zero matches** across both repositories; all 98 shipped formulas are v2 (VERIFIED-EMPIRICAL). Adopting it means authoring v1 formulas from scratch and abandoning the maintained pack ecosystem.

The asymmetry is worth naming plainly: **the v2 check loop is a strict functional regression on human-in-the-loop.** It dropped the waiting state, the operator verbs, the actor attribution, and the fail-closed default. Where converge maps unknown/empty to *block*, check loops map unknown/empty to *iterate* — fail-open into more agent work. For a human gate, fail-closed is the only defensible default, and it is the one v2 dropped.

**Reject is the weak spot everywhere.** Momentum's plan gate and results gate both need a "no, do not proceed" distinct from "the automation broke." The check loop cannot express it — its only terminal-negative outcome is exhausting `max_attempts`, which closes the step *failed*, indistinguishable from the work being broken. `converge stop` can express it; a gate expresses it only as indefinite blockage.

### Three silent-starvation hazards to inherit as design warnings

Two are recorded in the shipped check scripts' own comments; the third was found first-hand. All are the same class: **a gate that silently passes nobody.** (1) A `2>/dev/null` turned a refused metadata read into an empty set, so *"this gate never saw `code_review.verdict` and looped until Ralph ran out of attempts."* (2) Without an explicit `sort_by(.updated_at)` re-sort, *"the gate picks a verdict by id hash and can sit on a stale `iterate` forever while a newer `done` is ignored."* (3) **`--set-metadata` coerces numeric values** — `gc.attempt=0` stores a JSON *number* while every shipped script compares it as a **string**, so the attempt-scoped extractor returns `<none>` (verdict invisible to the gate) while the unscoped read returns `done`; `|tostring` fixes it (VERIFIED-EMPIRICAL, `research-human-verdict-patterns.md`:§7). *Scope caveat:* exercised on the `bd`-direct write path; whether `gc bd update` preserves string typing on a Dolt-backed city was never re-tested.

The rule that falls out: **any Momentum-authored check or gate script must coerce with `|tostring` before comparing, and must never rely on `2>/dev/null` to swallow a failed read** — a swallowed error and a genuine "not approved" are the same empty string.

**And a note on what `interaction_mode` is not.** It is **prompt text read by a language model**, not a control-flow gate — nothing in the runtime validates or blocks against it, and there are zero references to it in any check script (VERIFIED, downgraded during validation). Separately, `review_mode = "interactive"` means the *reviewing agent's write authority*, not human involvement. Neither is a HITL mechanism.

---

## 5. The four gate types, mapped

Momentum has four HITL points. Against the mechanisms above (consolidating `research-gate-mechanics-handson.md`:"What this means", `research-hitl-alternative-patterns.md`:§7, `research-maturity-open-bugs.md`:"Momentum-relevant synthesis"):

| Gate | Verdict | Basis |
|---|---|---|
| **(a) Triage approval** | **Fits.** One gate bead over the batch; approval is one `bd gate resolve` with per-observation dispositions written as metadata beforehand. Payload need is low. Do *not* use per-observation gates — the renudge loop would spam. | Q2/Q3 VERIFIED-EMPIRICAL |
| **(b) Pre-sprint plan gate** | **Fits with a notify bolt-on.** Blocking works; `--reason` persists the written verdict. But nothing tells the developer the gate opened, and the visual companion surface is out of scope for `gc` — gc holds the *state*, Momentum renders the *surface* and enforces anti-rubber-stamp itself. | Q3 VERIFIED-EMPIRICAL + the notification gap |
| **(c) Mid-story tooling gates** | **Best fit for the single-story case.** The close-side refusal is exactly "the agent may not declare done until a human exercised the tool," with `--force` as the audited override — reproduced against a **timer** gate, gate-type-agnostic by code path, **INFERRED for `human` gates specifically**. `bd blocked` gives a standing "what am I holding up" list Momentum lacks today. | Q2 bonus VERIFIED-EMPIRICAL; fan-out half untested |
| **(d) Post-sprint results gate** | **Blocked** — not "fits." The probe was a 3-step linear chain with no exec bodies, no agent, no fan-out, on a city never started; it cannot demonstrate a barrier over a fanned-out phase, which is what a results gate needs. Blocking and release hold *once a barrier construction exists*; the barrier is what is unproven. | Q3 VERIFIED-EMPIRICAL for blocking only; barrier **Blocked** per `research-maturity-open-bugs.md` |

### The design consequence, stated precisely

**Prefer `bd gate create` over `[steps.gate]` — but what that preference buys depends on gate type.** For `timer` / `gh:run` / `gh:pr` gates it is decisive: the persisted `await_type` is what makes them auto-resolvable at all. For `type=human` — all four of Momentum's points — it buys **notifiability, not auto-resolution**, and not today: `bd gate check` and `gate-sweep` skip human gates regardless of whether `type` persists, so the *only* consumers of a persisted `await_type: "human"` are the notify/renudge orders, which are in no tagged release. Net: the ad-hoc path yields a gate a vendored or future notifier can classify; `[steps.gate]` yields a blocker no watcher can classify at all. **Both block correctly; neither notifies out of the box.**

Getting `bd gate create` run inside a formula is itself constrained, and this is where the refuted premise still bites. There is no `exec` step. The construct is a **work step whose `description` instructs the claiming agent** to run `bd gate create --type=human --blocks <downstream-step-bead-id>`, or an **order-level `exec` script** (orchestrator-hosted, no agent, 300s cap). Either way `--blocks` must resolve to the *downstream* step's bead id — not the gate-creating step's own — and that id is knowable only at cook time via `gc.root_bead_id` + `gc.step_ref` metadata, not at authoring time.

The prose-instructed variant carries a silent-failure class worth flagging: **an agent can skip or garble the `bd gate create` call and the step still closes successfully**, leaving no gate and no ask. The following phase's check should verify the gate bead actually exists — not merely that a status key was stamped — or gate creation should move to an order-level `exec`, where execution is guaranteed rather than agent-discretionary.

### The verdict schema needs two key families, not one

The corpus had to correct this twice, and collapsing it produces a broken write-back schema. **Per-fork vocabulary** is `verdict.fork.<slug>=approve|modify|remove`, one key per genuine fork, matching `plan-gate-renderer.md`'s actual options ("Approve as specified" / "Modify scope or sequencing" / "Remove from sprint") — these carry the anti-rubber-stamp verdicts. **Gate-level vocabulary** is **Approve / Modify / Re-run AVFL**, the disposition of the *whole gate*, which is what a downstream step branches on. A complete schema carries both: N per-fork keys plus one gate-level key. "Modify" at gate level means "re-plan this sprint"; on a fork it means "change that one story's scope or sequencing." A gate bead has two terminal states, so Modify and Re-run need a convention — verdict metadata plus a reopen/new-gate cycle, or a labeled close. **No upstream convention exists** (VERIFIED, `research-notification-watcher-layer.md`:gap 6; `research-human-verdict-patterns.md`:§8).

The packs converged on a **triple** worth copying exactly: enum in metadata (for the machine), path in metadata (for the pointer), prose in a file (for the human's actual words). Note also that **attribution is lossy at the event layer** — every `bead.closed` event is attributed to `actor=cache-reconcile`, the real closer unrecoverable (gascity#5214, open). A resolved gate does not prove *who* resolved it; provenance must be written into `--reason`/metadata by the resolver.

### Why the alternatives lose

**Assignee-to-human** is a *hold*, not a dispatch. `gc ready`'s default query carries `--unassigned`, so an assigned bead is filtered out of every agent's claim — Gas City's own source says a human-claimed bead *"stays invisible to the pool's claim filter"* (#1007). It genuinely stops the graph, and it is silent: no notification, no queryable "awaiting human" state, nowhere to put a verdict. Right primitive to *remember exists* when a pipeline mysteriously stalls; wrong one to build a gate on. (Live dispute #4837 argues the checker wrongly retires a bare `human` label into `hold:mayor` — **Momentum should not adopt bare `human` labels.**)

**"Passive wait + mail"** is the *actual* production idiom in `gascity-packs` — park the session with `gc session wait --sleep --on-beads`, send exactly one `gc mail send human`, record exactly one terminal value, *"close fail only for explicit rejection or abort, not for silence."* It is well-designed, and Momentum probably cannot use it: it needs a resumable long-lived session to hold the wait, while a phase's work step claims, executes, and exits. **The correct adaptation is to invert it** — the phase step *creates the gate bead and exits successfully*; the gate blocks the next phase; the human resolves out-of-band; the graph resumes. One further conflict: the pack contract's `interactive` prose mandates *"one material question at a time,"* the opposite of Momentum's ≤7-fork single surface.

---

## 6. Cycle orchestration: adoption is a rewrite

### The premise was wrong

The sub-question assumed phases chained by exec steps running `claude -p /momentum:*`. **That shape does not exist, and the maintainers steer against building it** (VERIFIED, `research-cycle-orchestration-fit.md`:§1).

The v2 step key table is exhaustive — 25 keys, none of them `exec`, `command`, `run`, or `script`. A trap sits directly under it: **"Unknown step keys are silently ignored. A typo like `dependson` produces no diagnostic — the dependency simply vanishes."** So authoring `exec = "claude -p /momentum:triage"` compiles cleanly and does nothing. That is the single highest-risk authoring hazard for anyone arriving with the exec-step mental model.

The execution split is normative: *"The orchestrator executes every control bead… No agent participates in control execution. Agents execute only plain work beads."* The three places a shell command legitimately runs — an order-level `exec` (300s default), `[steps.check].check.path`, and an order `check` condition (10s default, synchronous inside the 30s tick) — are all bounded orchestrator-hosted probes. A 45-minute conduct phase fits none of them.

Gas City knows how to run `claude -p`: the provider config's `print_args = ["-p"]` is literally that, and its only consumers are `gc prompt synth` and title generation — *"no Gas City agent is involved."* It deliberately does not run *work* that way. The packs README says the quiet part out loud: *"if a raw skill says to spawn a subagent, dispatch a task tool, or invoke a plugin command, the pack should model that work as formula steps, expansion children, drains, or fanout/fanin lanes."* A grep of the entire `gascity-packs` corpus finds **zero** invocations of `claude -p`, `claude --print`, or `codex exec` (VERIFIED-EMPIRICAL).

### The shape that does exist is better — and is a rewrite

Claude Code runs as a **long-lived interactive process in a tmux box**, claiming beads in a loop. Momentum's model-tiering rule maps cleanly (per-step `opt_model` metadata overrides the agent default at dispatch), and per-phase routing is native (`gc.run_target` → `gc.routed_to`), so each phase can run on a different agent, model, or harness. `/momentum:*` reaches the agent as **skills, not slash commands** — packs ship a `skills/<name>/SKILL.md` tree that `gc` materializes into `.claude/skills/`, the same sink Momentum's plugin already uses. Watch the **4096-byte cliff**: larger `description_file`s are not inlined, so every step description becomes a *dispatcher* to Momentum's real instructions rather than a carrier of them.

Two orchestration facts are good news. **Order timeouts do not bound the work** — for formula orders the timeout covers only initial dispatch, and *"the order timeout never kills work mid-flight,"* so a phase can take hours as long as it is a formula step. And **duplicate prevention fails closed**: an order with open work is skipped, which for a single-in-flight-sprint cycle is a feature.

One is not. **The event trigger is too coarse for "retro-closed fires next triage"** — an order's only event field is `on = "<event type>"` with **no payload matcher**, while `gc events` *does* have `--payload-match`. Filtering exists on the observation side and is absent on the trigger side, so `on = "bead.closed"` fires on every closed bead in the city. Substitutes: a `condition` trigger with a selective check (precise, but synchronous inside the tick under a 10s default `check_timeout`), or put the phases in one workflow and let `needs` sequence them. The shipped packs answer decisively — **one composed formula spanning the cycle**, assembled from per-phase bases via `extends`, exactly what `bmad-build` does over `build-base`'s nine-step chain.

**The honest characterization: this is not "wrap conduct in a formula." It is "re-express Momentum's phase orchestration as a pack"** — precisely what the bmad, gascity, superpowers, gstack, and pr-pipeline packs are. Five methodologies have walked that path, so it is real and proven. It is also a rewrite of the orchestration layer, with Momentum's skills surviving as the pack's `skills/` payload.

### The failure mode nobody composed

Three facts sit in three different files and, assembled, describe a cycle that stops **permanently and silently** — with one of them calling part of the mechanism "a feature" (VERIFIED, `research-cycle-orchestration-fit.md`:§9a): (1) an order with open work is skipped every tick, even when the trigger says it is due; (2) a formula-cooked gate has no persisted `timeout`, so **every gate a formula creates is permanently manual** (framed elsewhere as fail-safe, which it is, for auto-expiry); (3) no tagged release notifies on a human gate.

Composed: an unresolved gate leaves its order's work open → the chaining order is skipped indefinitely → the cycle stops → nothing tells anyone. Structurally the same signature the wedge-bug class carries: *"the failure mode of this class is silence… cycle stalls will look identical to 'nothing was due.' Any adoption needs an external liveness check."*

**Prescription:** extend that recommendation explicitly to unresolved gates — a Momentum-side sweep of `bd gate list --status open` with an age threshold, run **independently of any `gc order`** so it survives a fully-wedged dispatcher. Different mechanism from the notify/renudge orders: those tell the *human* a gate exists; this tells *Momentum's own tooling* that a cycle has stalled, which is what matters when nobody is watching the clock.

---

## 7. Barriers: the structural blocker for the results gate

**Gates are fine; barriers are not.** Gate (d) — and any gate that must follow a fan-out — has no reliable declarative expression in formulas v2 as of 2026-08-21 (VERIFIED, `research-maturity-open-bugs.md`).

**#2311** — `waits_for = "children-of(X)"` does not gate `bd ready` — OPEN, p2, **last activity 2026-05-29**, no fix PR, no maintainer ruling, no milestone. The tracking edge is created at plan time when no children exist; `bd ready` gates only on `blocks` edges, so the downstream step becomes claimable as soon as the parent closes — and the parent closes when the `on_complete` bond *schedules* the fanout, not when children finish. The failure is silent: no logged error, just a worker failing on missing outputs. Three workarounds were documented and **the best has since regressed** — adding `needs` alongside `waits_for` now fails molecule instantiation outright, because `bd create --graph` drops the edge metadata. For Momentum: "conduct N stories in parallel → human reviews the end-gate report" cannot use `waits_for`; the developer would be asked to approve a report that does not exist yet.

**#3451** — v2 `needs` on a parent does not gate its children — OPEN, p2, opened by `csells`, who calls it *"the one authoring-semantics gap that keeps v2 from being a functional superset of v1."* A **maintainer design decision was recorded 2026-06-28** ("implement implicit parent-gating… Implementation tracking to follow") and **nothing has landed in the ~8 weeks since**; the spec on `main`, modified two days before this research, still carries the tracked-gap language. **This is the load-bearing one**, because the prescribed workaround — *"enumerate the children explicitly in `needs`"* — requires knowing the children at authoring time. Momentum's phase children are produced by sprint-planning at runtime, so the workaround does not apply and a phase-then-gate formula authored in v2 will not wait.

**`[steps.tally]` was removed from the SDK** — any formula declaring it fails fast — removing the obvious primitive for "all N stories completed → one verdict for the results gate." Combined with the 2026-06-28 ruling on #2947: **`drain` is the sanctioned fan-out; there is no first-class aggregate step to close a phase.**

So `drain` + a `check` loop is the only sanctioned barrier construction — a different authoring shape from "phase, then gate," unproven against a runtime-discovered story set, and carrying an unverified failure mode. **No file in the corpus states what happens when such a barrier exhausts `max_attempts` before every child has completed.** A check loop's exhaustion is unconditionally "closes the step as failed," and `bd ready`/`bd blocked` key on open/closed status without being demonstrated to distinguish `closed: done` from `closed: failed`. If closure alone satisfies a downstream edge, an exhausted barrier could release the results gate exactly as a genuine completion would — asking a human to review a report for stories still mid-flight. **Prescription pending verification:** add a completion-assertion bead whose precondition is an explicit count check ("N of N children closed done", not merely "the barrier step closed"), so a failed-exhausted barrier cannot masquerade as a completed one (`research-cycle-orchestration-fit.md`:§9c).

### Orchestration v3 will not rescue this on any announced timeline

#1709 *"Proposal: Orchestration v3"* is OPEN, p2, **no milestone**, **last updated 2026-06-01**. Its HITL requirements map onto Momentum's four gates almost line for line — paused-awaiting-input steps exempt from stale-Run GC, HITL as a runtime disposition, durable notification surviving controller restart, an authorization model with rejection terminating the Run, a pause surviving three days and two controller restarts. It is also honest about the starting point — TC6: *"Humans aren't agents. Today there is no `human` type in the codebase — humans are modeled as agents with a `nudge` field."* Minimum viable HITL is a binary approve/reject request with **a single notification channel (dashboard)**; multi-channel notification, presence detection, and escalation chains are **explicitly deferred**.

The companion tracker #2503 is OPEN, no milestone, **last updated 2026-06-09** — ten weeks stale — and its requirements crosswalk lists **HITL among the remaining integration lanes**. Neither issue appears in the 1.4 or 1.5 milestones. **Do not plan against O3 HITL.** And even shipped, its initial channel is the loopback dashboard — the wrong addressing model for out-of-session, so it would not satisfy the developer's requirement either.

---

## 8. Maturity, and who actually runs human-gated formulas

### Project health: fast, active, and concentrated

Eleven releases in ~14 weeks — one every 9–10 days, four minor bumps in 3.5 months, three carrying Breaking Changes sections. **A fast-moving pre-2.0-behaviour project despite the 1.x version string.** Weekly commits average ~168 over the trailing 12 weeks with no collapse; 2,402 PRs merged since 2026-05-01 (VERIFIED-EMPIRICAL). **Every minor since 1.1 has required `gc doctor --fix` against existing cities** — Pack V2 schema enforcement in v1.2.0, **the Dolt ≥ 2.1.0 floor in v1.2.1**, explicit provider entries in v1.3.0, one store-scoped `control-dispatcher` per graph-owning scope in v1.4.0. Assume a migration chore per minor, not per major.

**Bus factor ≈ 1–2.** `julianknutsen` authors 51.8–52.2% of commits in both sampled recent windows and **66.2%** cumulatively over the repo's 5,437-commit history (windowed-vs-cumulative measures of the same concentration, not contradicting counts); top-3 is 79.9%, and 67 of 165 contributors have exactly one commit. A real adoption risk for a dependency placed at the top of Momentum's cycle.

**Issue backlog: 575 open issues** (search-API `is:issue is:open`, PRs excluded) against 718 closed all-time, so "intake outpaces resolution" does not hold. *Query-method hedge:* the raw query string was not recorded when 718 was taken; the `is:issue is:closed` basis is stated as the method the like-for-like arithmetic requires, not as an observed re-run — INFERRED for 718, VERIFIED-EMPIRICAL for 575. (A separate corpus figure of 1,011 is the repo-endpoint `open_issues_count`, which bundles open PRs in; the two are not in conflict.)

The `1.5` milestone (due 2026-08-04, already past) is dominated by a **"Customer Zero" dogfooding series** recording real operator breakage: dolt port collisions on a second city, `gc status` misreporting healthy cities, macOS supervisor drift auto-restart broken. Simultaneously a good-faith maturity signal and a warning — basic multi-city and macOS operation was still breaking in August 2026, on Momentum's exact platform. **The two dispatcher-wedge bugs are genuinely fixed** (#2131, #2168, both closed in the v1.2 window), though the bug *family* remains live: tracker #2903 is open in 1.5.

### Nobody runs human-gated formulas

**No publicly discoverable Gas City formula — first-party or third-party — uses `[steps.gate]`.** An exhaustive grep of all 315 TOML files in `gascity-packs` returns **zero** occurrences of `steps.gate` and zero of `waits_for` (VERIFIED-EMPIRICAL); the sub-tables actually used are `[steps.check]` × 57, `[steps.drain]` × 25, `[[steps.children]]` × 10, `[steps.expand_vars]` × 1. Forty-one files match the string "gate" and every match is **prose**: the `contributing` and `pr-pipeline` packs implement their advertised "BLOCKING gates" as an ordinary `claude` step whose prompt tells the agent to echo a BLOCKED line, close the root bead, and exit — an *agent-judgment early exit*. **Nothing pauses; nothing waits for a person.**

The phrase "human gate" appears **zero times** anywhere in `docs/`. Across 1,293 issues, exactly **one** mentions `[steps.gate]` — #4399 — and it is a *spec-verification* issue, not a production-failure report: the author verified against `--help` output and the spec, i.e. reading the docs, not hitting the bug in a running city. Auto-triaged p3, still open with **no human maintainer response**. A feature with real users generates real users' bug reports; this one generated a documentation audit.

The registry is 17 packs, 16 first-party; the sole third-party pack has five files and **no formulas, no orders, no gates**, and its publisher is a Customer Zero participant rather than an arm's-length adopter. **Not one Customer Zero issue concerns gates or human approval.** And the **`oversight-rig` pack is the sharpest datapoint**: the pack explicitly about human oversight contains zero gates, escalating outward over Slack alongside a running factory. **Humans *on* the loop, not *in* it.**

### Maintainer direction points away from HITL

Steve Yegge, August 2026: *"code review… will be [gone] by next year. **You can't work at agentic speeds and block everything with human reviews.**"* And: *"crons watch, models act."* His framing of Beads is as a provenance ledger for post-hoc diagnosis, *"not approval authority."* (CITED — 5 commits to the repo, so directional rather than operational.) Marketing runs the other way — gascity.com promises "a human review gate" — but the guide provides no implementation pattern and no worked example. **The gap between the marketing surface and the shipped primitives is the finding.**

The most instructive datapoint: on 2026-08-20 Chris Sells published the *Beads 1.2.1 Incident Report* after an autonomous agent maintainer cut and published a release without authorization. The diagnosis is a direct argument *for* materializing gates as inspectable state — *"a release process that lives only in a human conversation is invisible to an agent"* — and the failure mode was exactly what Momentum's anti-rubber-stamp gate exists to prevent: *"the go I acted on was a one-line conditional approval, relayed through an agent."* **And with that diagnosis in hand, the company chose a GitHub tag-protection ruleset and agent sandboxing.** Their own gate primitives are not mentioned.

One honest counter-signal and its correct reading: the notify/renudge orders exist — but PR #4553 was authored by **a community contributor with 11 commits total**, not the core team, and the core team has left both unreleased for four weeks and counting. The core team's revealed preference is mildly *anti*-HITL, or at best indifferent.

**Adoption scale, bounded correctly.** Homebrew installs (30/90/365 days): gascity 669 / 962 / 1,022 against beads 3,719 / 7,695 / 22,632 — beads is roughly 5–20× more adopted on every non-gameable metric, and the dependency is one-directional. But ~700 monthly macOS installs is **a floor, not a ceiling**: this corpus documents three uncounted channels — the mise/GitHub-backend path (used by this research's own hands-on session), source builds from HEAD (which the project's own docs recommend), and Linux, which Homebrew excludes entirely. The directional conclusion survives fully; the number is not a hard population cap.

**The blunt reading: Momentum would be the first public user of `[steps.gate]`, and would be building the notification and verdict-capture layers itself.**

---

## 9. Beads coupling and what adoption forces on DEC-028

**Gas City does not force Dolt for a city's work ledger in general — but the HITL gate primitives Momentum's four gate points actually need do** (VERIFIED-EMPIRICAL, `research-beads-coupling-dec028.md`:Bottom Line, settled by live probe).

`GC_BEADS=file` is real, documented, and load-bearing — referenced from five independent places in current `main`, including the binary's own error string and the CI/testscript default, and `gc doctor` is provider-aware, reporting every dolt-specific check `✓ skipped (file backend or GC_DOLT=skip)`. Live probe on gc 1.4.1: `gc init` under `GC_BEADS=file` requires **only tmux** as a missing-dependency blocker — not dolt, not bd (VERIFIED-EMPIRICAL, Probe 1).

**And the entire `gc bd` verb family is unconditionally blocked on a file-backed city.** `GC_BEADS=file gc bd gate create --type=human` fails with `gc bd: only supported for bd-backed beads providers`. The full `gc beads` surface there is `list`/`show`/`health`/`city` — no `create`, no `update`, no `set-metadata`, and a scan of every top-level subcommand's `--help` found no metadata-setting verb anywhere (VERIFIED-EMPIRICAL, Probes 2–3). **The gate primitive this entire corpus recommends has no file-store equivalent in 1.4.1** — it cannot be tested for persistence there because it cannot be created there. A related probe relocated a risk rather than resolving it: **FileStore metadata persistence is durable, not a no-op** (a hand-edited custom key round-tripped across two genuinely fresh `gc` invocations), but with no public CLI verb to write arbitrary metadata there, the durability question is settled favorably and is **moot** for Momentum's gate use case.

**The dependency footprint, attributed correctly.** `gc init` — not `gc start` — is the single enforcement point, and under the bd provider it refuses on **tmux, an external `dolt` binary, and `flock`, all three, up front**, even with `--no-start`. The *graph layer* does not: formula compilation, cooking, and all bead/readiness semantics ran fine with the city un-started against a plain `bd init` store using **bd's own embedded Dolt** — the exact backing Momentum's dual-write spike already uses. So "embedded Dolt is sufficient" describes the direct-`bd` graph layer; a `gc`-orchestrated bd-provider *city* still hits the `gc init` check regardless of embedded-vs-external.

**The Dolt operational burden is real at fleet scale and effectively unreachable at Momentum's.** Two runbooks exist because Dolt-backed cities have hurt people — auto-GC triggers only at ~125 MB of new chunks, and `bd`'s auto-backup has *"no retention, rotation, or garbage-collection logic"*, with a documented incident reaching 34 GB and filling a disk. Momentum's actual store: **2.5 MB total, 0.05% of the warn threshold** (VERIFIED-EMPIRICAL). Not a reason to avoid Dolt here — a reason to keep `bd config set backup.enabled false` in reach if a city ever goes Dolt-backed. And note the regime asymmetry: those runbooks assume a managed long-lived Dolt server, while Momentum runs bd's *embedded* Dolt with no server process and no continuous write load.

**The sharpest coupling finding is in the changelog, not the guides: a Dolt-backed city and a standalone `bd dolt` server cannot share a `.beads/dolt`** — they contend on an exclusive write lock. Current `gc` detects it and refuses with a message naming `bd dolt stop`, but the constraint stands, and Momentum's dual-write spike keeps exactly such a store at the repo root. The supported way out is an **externally-bound scope**, where a complete storage binding makes `gc` delegate to a workspace-pinned `bd`.

**Version coupling holds one unpredictable constraint, and it is good news.** Momentum runs `bd` 1.0.4, which is `deps.env`'s `BD_PREV_VERSION` — *the documented floor of Gas City's cross-version contract-test matrix*, explicitly tested rather than merely tolerated. The `BD_VERSION` figures that looked contradictory are both correct for different refs (VERIFIED-EMPIRICAL, Probe 5): the **v1.4.1 tag pins `v1.2.2`**, while current **`main` has since downgraded to `v1.1.0`** — counter-intuitively older-pinned than the shipped tag — with an inline comment explaining that no published beads release carries the `--if-assignee`/`--if-status` CAS precondition flags on the embedded path its contract tests exercise.

**That comment's premise does not fully reconcile, and the gap is decision-bearing.** It calls v1.1.2 "the newest published release," but beads **v1.2.2 was published 2026-08-15 and was downloaded and run by this corpus**, and it postdates `beads#5008` (2026-07-24), the commit that landed the flags — on the comment's own logic, a release cut after #5008 would be expected to *carry* them. Either the comment is stale, or its "newest published" is scoped to the v1.1.x line. **The corpus never ran `bd 1.2.2 update --help` to settle it.** So CAS conditional writes are **VERIFIED unavailable for v1.0.4 (the version Momentum runs) and across the v1.1.x line, and UNVERIFIED for v1.2.2.** One adjacent fact belongs in any DEC-028 re-evaluation alongside it: **beads v1.0.5 was withdrawn for a data-corruption bug** — direct evidence about substrate maturity independent of Momentum's own experience.

### Re-scoring DEC-028's own gates

DEC-028's criterion is 3-of-4 gates positive → flip beads authoritative.

| Gate | New evidence from Gas City | Direction |
|---|---|---|
| **G1** — did `bd ready`/`--claim` simplify scheduling? | `Ready` is on the Store interface every provider implements; `gc hook --claim` supplies atomic claim over *whatever* store, FileStore included | **Weakens** the case for flipping — the win is obtainable without Dolt (city-internal scheduling; the gate-primitive exception above still applies) |
| **G2** — did `discovered-from` eliminate intake-queue triage toil? | Nothing in the researched Gas City surface touches that mechanism | **Neutral** — not evidence either way |
| **G3** — was Dolt sync manageable under git-discipline? | v1.0.5 withdrawn for data corruption; bloat + unbounded-backup runbooks exist; but Momentum's store is 2.5 MB / 0.05% of the warn threshold | **Mixed** — real at fleet scale, negligible at solo scale |
| **G4** — did `--spec-id` linkage hold without in-tree loss? | Unchanged. Gas City stores *its* beads, not Momentum's prose | **Neutral** |
| Multi-agent write safety (D1 rationale) | CAS `--if-assignee`/`--if-status` unavailable in v1.0.4 and across v1.1.x; `conditional_writes` defaults `off`. **[UNVERIFIED for v1.2.2]** | **Weakens on the bd Momentum actually runs**; unsettled as a claim about every published release |

**What adoption forces: not nothing — a scoped, city-local Dolt requirement.** A Gas City orchestrator's own work ledger can run `GC_BEADS=file` and never touch Dolt or Momentum's `.beads/`. But if that city wants to express Momentum's HITL gates as `bd gate` beads, **the city's own store must be bd/Dolt-backed**, because `gc bd` is unconditionally blocked on file. This does not force `.momentum/*/index.json` off its current model and does not decide DEC-028 either way — **but "adopt Gas City for HITL gates, force nothing" is no longer an accurate description of the trade.**

**What adoption unlocks: the "we need Dolt for dispatch" argument dies.** DEC-028 D1's headline win was `bd ready` + atomic `--claim` replacing hand-built dependency logic; if the dependency engine is what Momentum actually wanted, it is reachable without Dolt-authoritative state. The counterweight: if Momentum ever wants one queryable substrate spanning practice work items *and* orchestration state, the aligned configuration is flip-authoritative + `bd` provider + Momentum as a prefix-scoped rig — the only topology where the two ledgers are one.

**Recommended sequencing:** evaluate on `GC_BEADS=file` for non-gate city work as DEC-032 D3 already specified, but **budget for a bd/Dolt-backed city store specifically for the gate primitive** rather than assuming it is avoidable. Treat the city's ledger as disposable orchestration state, and decide DEC-028's question about Momentum's *own* ledger on its own merits.

---

## 10. Multi-Conductor: the evidence weakens the case

The second DEC-035 trigger scores worse than the first (VERIFIED, `research-dec035-revisit-triggers.md`).

**Structurally, concurrent lanes over one rig happen — by accident.** #5511 (OPEN, filed 2026-08-22 against v1.4.1) records one `gc sling` call minting **three complete live workflows**, because a `bd create --graph` subprocess was killed at its client deadline *after* its Dolt transaction had committed and the transient-retry path re-applied the plan twice more. The decisive sentence: *"the pool reconciler spawned three concurrent workers into the same non-isolated checkout, which began editing the same files."*

**But nothing in Gas City is designed for peer orchestrators.** v1.4.0's requirement — one store-scoped `control-dispatcher` per graph-owning scope — is a fan-out of *scopes*, not of orchestrators, and the spec's framing is singular throughout. #3964 reports the core pack ships `max_active_sessions = 1` on the control-dispatcher, tripping Gas City's own singleton advisory once per scope: *"drain-at-zero is the dispatcher's DESIGNED behavior, so the bundled pack ships a permanent advisory against itself in every city."* **One control-dispatcher per graph-owning scope, capped at one active session, by design.** Four adjacent issues show the seam still settling, two updated 2026-08-23 — one day before this research.

**And the one mutual-exclusion primitive did not exclude.** A drain's `member_access = "exclusive"` records a reservation which, in shipped releases, *"was read only by other drains… a fresh/root formula dispatch sailed straight past the reservation. Two lanes then drove one anchor concurrently in one shared build tree… Result: duplicate ~450-line implementations, interleaved commits with unreliable git attribution. **Exclusive did not exclude**"* (#4587, OPEN). The fix is written, reproduction-proven, adversarially reviewed twice — and **not merged** (staged and held; verified `NOT MERGED` 2026-08-24). Its own author names a residual limit even in the fixed world: *"Simultaneous-launch TOCTOU… not full mutual exclusion. A complete fix needs a shared per-member dispatch lock."*

**Multi-city on one machine is still breaking on Momentum's exact platform.** #4526 (Customer Zero #40, OPEN, p2, milestone 1.5 already past due): with one city's managed dolt running, `gc rig add` in a second city dies on a port collision, points at a `dolt.log` never written, and leaves the rig half-added — observed on macOS Apple Silicon. Milestone 1.5 also carries #4521 (supervisor drift auto-restart broken on macOS) and #4522 (`gc status` rendering a healthy city as "0/4 agents running"). Worktree isolation exists but #5511 shows it is configuration, not a guarantee.

**Verdict: NOT FIRED, and the case is weaker than at DEC-035 time.** Per DEC-035's own rationale, if this goal ever does appear the requirement it generates is **atomic claim over the story frontier** — solvable by beads' `--claim` under DEC-028, without importing an orchestrator whose own exclusive-access primitive is unmerged.

---

## Cross-Cutting Themes

**1. The failure mode of every gap here is silence.** A wedged dispatcher does not error — orders simply stop firing. An unnotified gate is indistinguishable from a stalled cycle. A silently-ignored unknown step key makes a dependency vanish with no diagnostic. An exhausted barrier may release its downstream gate exactly as a completion would. A swallowed metadata read and a genuine "not approved" are the same empty string. **Every one of these turns an approval gate into a rubber stamp or a dead cycle, without anything raising a hand.** Any adoption needs external liveness checking that does not depend on the orchestrator to complain — and, per §6, that check must run outside `gc order` so it survives a wedged dispatcher.

**2. The primitive is real; the productization is absent.** `bd gate` is fully implemented and the compiler synthesizes real blocking beads — but zero bundled formulas use gates, zero public formulas use gates, the spec files the type vocabulary under "Accepted But Inert," the tracking issue is p3 with no owner and no maintainer response, and the notification reflex that would make it usable is in no release. Momentum would be the first-party test case for both the primitive and its gap.

**3. Blocking is easy; the return path is hard.** This is the shape of both the cost and the risk. Of ~5.5–9 days of glue *for one gate type*, ~2.5–4 days is shared infrastructure that amortizes across gates and **~3–5 days is per-gate verdict capture and write-back that recurs**. Momentum's plan gate ends in a clipboard paste into a live chat session — the one hop with no out-of-session analogue. Gas City carries paths and enums; the presentation layer and the anti-rubber-stamp enforcement remain entirely Momentum's to build.

**4. Gas City's own maintainers do not want what Momentum wants.** *"You can't work at agentic speeds and block everything with human reviews."* *"Crons watch, models act."* The oversight pack escalates outward rather than blocking inward. When leadership needed a hard human gate after an unauthorized release, they reached for GitHub tag protection. Momentum's practice is built on decision gates that block. **That is a values mismatch, not just a feature gap**, and it predicts which gaps get closed.

**5. Every headline number is a floor.** The 15–25d orchestration rewrite is a rough sizing from analogous pack scope, **against four gates, not the five the corpus later identified**. The 5.5–9d glue figure is **for one gate type** and **excludes the uncosted standup of a live Momentum city**. Neither is bottom-up.

**6. The most-corrected claims cluster where the evidence was documentary rather than reproduced.** Four validation rounds repeatedly moved claims from "the docs say" to "the probe showed," and the direction of correction was consistently toward *narrower* scope: `GC_BEADS=file` exists (correcting a wrong negative) but blocks `gc bd` entirely; FileStore metadata is durable but externally unwritable; CAS is unavailable *for v1.0.4 and v1.1.x*, not for every published release. **[EMPIRICAL] evidence earned its place as the corpus's highest-trust tag for behavioral claims.** Iteration 4 also produced a confident **false positive on a negative claim** — an alleged fabricated quotation that was verified present verbatim at the cited location — the failure mode that most resembles a real finding, and worth carrying as a practice note.

---

## Recommendations

**1. Ratify the deferral and close the question — do not adopt Gas City.** DEC-035 D2 stands unchanged; this corpus files as the evidentiary baseline for any future revisit. The blocking mechanics are proven, but the notification layer that would make them usable is unreleased, unaddressed on any roadmap timeline, and pointed away from by maintainer direction. Nothing here is a reason to revisit before a goal appears.

**2. Treat the notification/verdict-return layer as the gating requirement for any HITL orchestration Momentum runs — Gas City or otherwise.** The developer's requirement is a hard one: rich notification plus genuinely bidirectional back-and-forth. Momentum's *current* in-session plan gate and results gate surfaces already meet that bar. **Any out-of-session design must match it, not lower it.** This is now a standing evaluation criterion, not a Gas City finding.

**3. Adopt the corpus's transferable hazards into Momentum's own gate tooling now, independent of any orchestrator.** Three cost nothing and prevent the exact silent-starvation class documented here: coerce with `|tostring` before comparing metadata values; never swallow a failed read with `2>/dev/null`; and verify a gate *bead exists* rather than trusting that a status key was stamped. Add an age-thresholded sweep of open gates that runs independently of whatever dispatches work, so a stalled cycle is detectable when nobody is watching the clock.

**4. Decide DEC-028 on its own merits — the Gas City argument for it is now weaker, not stronger.** The dispatch-scheduling win (G1) is obtainable without Dolt-authoritative state, since `Ready` and atomic claim work over any provider. Two facts should enter the re-score: the CAS write-safety win is unavailable on the `bd` Momentum runs (v1.0.4) and across v1.1.x — **[UNVERIFIED for v1.2.2]**, settleable with one command — and beads v1.0.5 was withdrawn for data corruption.

**5. If the out-of-session trigger ever fires, run this pre-flight in order — and stop at the first failure.**

- **(i) Prove the notification and verdict-return layer first, before anything else.** Per the developer's Fork 4 requirement, this is the thing that must be proven first rather than built last. Concretely: a real channel the developer actually watches (not a `human` mailbox), and a served plan-gate surface that can write per-fork verdicts back as machine-readable state. If this cannot be demonstrated end-to-end, stop — the rest is irrelevant.
- **(ii) Then close the four open probes.** Each is a single command or a single short run: does `bd 1.2.2` carry the `--if-assignee` CAS flags; do the two notify orders actually fire against a properly-typed `--type=human` gate (and does `--payload-match bead.issue_type=gate` select gate beads at all); what are a `drain`+`check` barrier's failed-close semantics; does a Claude Code session survive a multi-hour step without `idle_timeout` or `claim_holder_stall_timeout` firing, and does `gc session wait --sleep` park it resumably.
- **(iii) Then construct and prove the barrier.** `drain` + a `check` loop is the only sanctioned shape, and it must be demonstrated against a *runtime-discovered* story set with a completion-assertion bead asserting "N of N children closed done" — because #3451's enumerate-the-children workaround is unavailable to Momentum and an exhausted barrier must not masquerade as a completed one.
- **(iv) Then re-estimate cost bottom-up.** Both current figures are floors: 15–25d rewrite scoped to four gates, 5.5–9d glue for one gate type excluding city standup. A real go/no-go needs the five-gate, all-phases, city-included number.

**6. Adopt the stop-before-push contract explicitly, now, so it is not decided by default later.** Per Fork 2: any future out-of-session cycle terminates at "merged locally, ready to push"; push remains a manual, approval-gated session action. **No fifth gate, no rule change.** Record it wherever the out-of-session design would be specified, because the corpus's four-gate design silently collided with Momentum's `git-discipline` push rule and its version-bump-on-release rule, and a default is exactly what that collision would otherwise produce.

---

## Known Limitations

These are **not defects** — they are questions the research could not close, each marked open at its site. Any decision document built on this corpus must treat them as open and must not silently resolve them. The AVFL loop closed by developer direction after iteration 4 under a MAX_ITERATIONS policy, so **iteration 4's fixes ship to synthesis unvalidated by a further adversarial pass.**

1. **`bd` v1.2.2 CAS settling command was never run.** Whether beads v1.2.2 carries the `--if-assignee`/`--if-status` compare-and-swap flags is **UNVERIFIED**; every CAS claim here is scoped to v1.0.4 and the v1.1.x line. The upstream `deps.env` comment generalizes to "no published release," but rests on a "newest published = v1.1.2" premise that v1.2.2 breaks — and on that comment's own logic, a release postdating `beads#5008` would be expected to carry the flags. **Decision-bearing: it feeds the DEC-028 D1 re-score.** One command settles it.

2. **The FileStore write-path question is moot, not answered.** Probe 2 settled that FileStore metadata *is* durable, then relocated the risk: there is no public CLI verb to write arbitrary metadata on a file-backed city in gc 1.4.1 (`gc bd` is blocked wholesale), so durability never becomes load-bearing for Momentum's gate use case. The durability worry is retired; **the write-path absence is the finding.**

3. **Failed-close semantics of a `drain`+`check` barrier are unexercised.** No file states what happens when such a barrier exhausts `max_attempts` before every fanned-out child has completed. Because `bd ready`/`bd blocked` key on open/closed status and were not demonstrated to distinguish `closed: done` from `closed: failed`, an exhausted barrier **may release its downstream results gate exactly as a genuine completion would** — asking a human to review a report for stories still mid-flight. The prescribed guard (a completion-assertion bead asserting "N of N children closed done") is **pending verification, not proven.**

4. **Multi-hour session behavior is open.** Whether a Claude Code session survives a multi-hour step without `idle_timeout` firing, and whether `gc session wait --sleep` parks a session such that an attach/nudge resumes the *same* conversation. The 2026-08-24 probe session installed gc 1.4.1 and exercised it live, but ran no multi-hour step and never exercised `idle_timeout` / `claim_holder_stall_timeout`. Only the "gc is not installed at all" framing is stale; **the questions themselves remain genuinely open.**

5. **Notify-orders-vs-typed-gate behavior is inferred, not run.** That the two core orders would fire on a properly-typed ad-hoc `--type=human` gate is **INFERRED** from reading their `await_type == "human"` filter against the observed persistence — the orders are `main`/`edge` only and were never executed here. Also unexercised: whether `--payload-match bead.issue_type=gate` actually selects gate beads, which the entire watcher design would be built on.

6. **Every cost total is a floor, not an estimate.** The **15–25 day** orchestration-rewrite figure is a rough sizing from analogous pack scope, taken against the corpus's *four* originally-enumerated HITL gates — not the **five** identified once push/merge authority is counted. The **glue estimate** sums to **5.5–9 days** (rounded to 6–9 at citation sites, all hedged), is **for one gate type only**, and **excludes the uncosted standup of a live Momentum city**. Within it, only the ~2.5–4d shared-infrastructure share amortizes across gates; the ~3–5d verdict-capture share recurs per gate. Neither figure is bottom-up.

7. **Push/merge authority had no named gate in the corpus's design — now resolved by developer verdict, but as a contract, not a mechanism.** Momentum's rules require explicit human confirmation before `git push` and mandate a version bump plus push at sprint completion; an unattended cycle collides with both, and the corpus never checked its four HITL gates against them until the fix passes. It deliberately left the choice open between a fifth gate and a stop-before-push termination. **The developer chose stop-before-push (Fork 2, 2026-08-25): an out-of-session run terminates merged-but-unpushed; no fifth gate, no rule change.** The residual limitation is that no cost estimate here was re-scoped against that decision, and nothing mechanically enforces it — it is a contract to be written into any future out-of-session design.

**One further honesty note on the validation lineage.** Iteration scores were −18, −43, −38, and a residual list of 3 genuine majors + 4 minors + 3 lows (≈61/100 on the iteration-2 formula; 53/100 if the disproved item is counted as a major). Both numbers are stated because no fifth round adjudicates the disqualification. The scores do not descend monotonically, and that is expected: each iteration's adversaries probed a *corrected* corpus at deeper seams. Iteration 4's yield — small enough to enumerate exhaustively — is the practical convergence signal.
