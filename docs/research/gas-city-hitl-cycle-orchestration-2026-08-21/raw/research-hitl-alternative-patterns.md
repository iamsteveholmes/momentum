---
content_origin: claude-code-subagent
date: 2026-08-21
sub_question: "HITL alternative patterns: assignee-to-human steps, mail-to-human, converge gates — which fits Momentum's plan gate vs results gate vs mid-story tooling gates (human-facing tools like nornspun/chorgi)"
topic: "Gas City HITL gates and cycle orchestration for Momentum"
---

## Bottom line

Gas City has **five distinct human-in-the-loop mechanisms**, and they are not equally real.
Ranked by implementation maturity as of 2026-08-21:

1. **`bd gate --type=human`** — fully implemented *in beads*, not in Gas City's v2 compiler. Parks a step off the ready frontier; closes only via `bd gate resolve`, which takes a free-text `--reason`. This is the load-bearing primitive.
2. **Mail-to-human** — first-class. `human` is a reserved mailbox address with its own inbox; `gc mail send human …` is a documented example, and `gc mail reply` carries free-text payload back into an agent's context via hook injection.
3. **"Passive wait + mail"** — the *actual* production HITL pattern in `gascity-packs`, composed from `gc session wait --sleep --on-beads` + `gc mail send human` + a terminal verdict written to workflow-root bead metadata. Notably it does **not** use `[steps.gate]`.
4. **`gc converge --gate manual`** — a real manual gate with `approve`/`iterate` verbs and a `waiting_manual` state, but **v1-formulas-only** and payload-free.
5. **Assignee-to-human** — *not a dispatch mechanism at all.* Nothing dispatches to a non-agent assignee; a human-assigned bead simply becomes invisible to every agent's claim filter and sits open.

Gas City's own `[steps.gate]` table is the trap: it compiles, it synthesizes a gate bead, and its `type` vocabulary — including `human` and `mail` — is **inert**.

---

## 1. Assignee-to-human: a park, not a dispatch

The v2 formula spec exposes `assignee` as a step field ("Default assignee; supports `{{var}}`") ([formula-spec-v2 §1](https://docs.gascity.com/reference/specs/formula-spec-v2.md)) **[OFFICIAL]**. Nothing in the dispatch section resolves it. The persisted routing key is `gc.routed_to`, derived from `gc.run_target` at dispatch — a separate axis from `assignee` entirely:

> "A step's `gc.run_target` metadata is compile-time routing intent: at dispatch the router resolves it into `gc.routed_to`, the sole persisted routing key" ([formula-spec-v2](https://docs.gascity.com/reference/specs/formula-spec-v2.md)) **[OFFICIAL]**

The decisive evidence is the shape of the default work query. `gc ready` documents the query agents actually run:

```
gc ready --metadata-field "gc.routed_to=$target" --unassigned \
  --exclude-type=epic --exclude-label "hold:mayor" \
  --sort oldest --limit 20 --json
```
([CLI reference — `gc ready`](https://docs.gascity.com/reference/cli.md)) **[OFFICIAL]**

`--unassigned` is in the default. An assigned bead is filtered out of every agent's claim. Gas City's own source states the consequence outright, in the doc comment for `gc sling --reassign`:

> "Reassign clears any existing human assignee on the bead before routing so the target pool/agent can claim it. Without this, a bead claimed by a human (`bd update --claim`) stays invisible to the pool's claim filter even after sling sets `gc.routed_to`. See gastownhall/gascity#1007."
> ([internal/sling/sling.go](https://github.com/gastownhall/gascity/blob/main/internal/sling/sling.go)) **[OFFICIAL]**

**Verdict:** assignee-to-human is a *hold*, and a functional one — a human claim genuinely stops the graph, and `--reassign` is the documented human→pool handoff. But it is silent: no notification, no state anyone queries as "awaiting human", no place to put a verdict. It is the wrong primitive to build a gate on, and the right primitive to remember exists when a human accidentally claims a bead and the pipeline mysteriously stalls.

A second, adjacent axis is the hold-label taxonomy: `hold:mayor` / `hold:external`, with `hold:mayor` excluded by the default work query. Note the live dispute — issue [#4837](https://github.com/gastownhall/gascity/issues/4837) (OPEN, updated 2026-08-14) argues the checker wrongly retires a bare `human` label meaning "a human executes this" into `hold:mayor` meaning "waiting on a decision-maker" **[OFFICIAL]**. Two axes, one label space, unresolved. Momentum should not adopt bare `human` labels.

---

## 2. `[steps.gate]` (Gas City v2) vs `bd gate` (beads): two different things

This is the single most important distinction in this sub-question, and it is easy to miss.

**Gas City's v2 compiler** synthesizes a gate bead from `[steps.gate]`:

> "A `[steps.gate]` table synthesizes a sibling gate bead (type `gate`, title `Gate: <type> <id>`) and a `blocks` edge from the gated step to it: the step stays blocked until the gate bead is closed. … The gate `type` vocabulary and the `waits_for` mode distinction have no runtime consumer."
> ([formula-spec-v2 §2](https://docs.gascity.com/reference/specs/formula-spec-v2.md)) **[OFFICIAL]**

Section 4, "Accepted But Inert," is explicit:

> "**Gate `type` vocabulary.** `[steps.gate]` synthesizes a real gate bead that blocks its step until the gate bead is closed (manually or by an external watcher), but the `type` values `gh:run`, `gh:pr`, `timer`, `human`, and `mail` are doc-comment vocabulary in `internal/formula/types.go` — the parser never validates them and no bundled watcher acts on them. **Zero bundled formulas use `gate`.**"
> ([formula-spec-v2 §4](https://docs.gascity.com/reference/specs/formula-spec-v2.md)) **[OFFICIAL]**

Tracked as [gascity#4399](https://github.com/gastownhall/gascity/issues/4399) — "formulas v2: `[steps.gate]` type vocabulary (timer/gh:run/gh:pr/mail) is parsed-but-not-enforced — no watcher resolves formula-synthesized typed gates" — OPEN, last updated 2026-07-19 **[OFFICIAL]**. I confirmed the "zero bundled formulas" claim independently: a code search for `steps.gate` across `gastownhall/gascity-packs` returns **0 hits** **[EMPIRICAL]** (`gh api -X GET search/code -f q='repo:gastownhall/gascity-packs "steps.gate"'` → `total_count: 0`).

**Beads (`bd`), by contrast, implements the whole gate subsystem** — including `human`:

| Type | Waits for | Closed by |
|---|---|---|
| `human` | a person's decision | `bd gate resolve` only |
| `timer` | a duration after gate creation | `bd gate check` once the timeout elapses |
| `gh:run` | a GitHub Actions workflow to complete successfully | `bd gate check` |
| `gh:pr` | a pull request to merge | `bd gate check` |
| `bead` | a bead in another rig to close | resolve manually |

([beads docs/workflows/gates.md](https://github.com/gastownhall/beads/blob/main/docs/workflows/gates.md)) **[OFFICIAL]**

**Create-vs-check standardization (added during AVFL fix pass — MIN-004):** the row above lists all five types uniformly, but `bd gate create --type=` and `bd gate check --type=` accept different, non-symmetric sets — confirmed against `research-maturity-open-bugs.md`'s citation of #4399: **creatable** via `bd gate create --type=` is `human`, `timer`, `gh:run`, `gh:pr` (not `bead`); **evaluated** by `bd gate check --type=` is `gh`, `gh:run`, `gh:pr`, `timer`, `bead` (not `human`, by design — human gates require manual resolution). So `bead` in the table above is check-only: there is no `bd gate create --type=bead`; a `bead`-type gate is presumably created some other way and only *evaluated* by the checker. Do not read this table as "all five types are symmetric create+check pairs."

The commands are real and reachable from Gas City via the `gc bd` passthrough (`gc bd` forwards all args to `bd` unchanged, per the [CLI reference](https://docs.gascity.com/reference/cli.md)):

```bash
bd gate create --type=human --blocks bd-abc --reason "Design sign-off"
bd gate list --json
bd gate show <gate-id>          # details AND waiters
bd gate resolve <gate-id> --reason "…"
bd ready --gated                # molecules where a gate just closed
bd blocked                      # what's waiting, on which gates
```
([beads docs/cli-reference/gate.md](https://github.com/gastownhall/beads/blob/main/docs/cli-reference/gate.md)) **[OFFICIAL]**

And it is patrolled in production: the `gastown` pack's `deacon` agent prompt lists `gc bd gate check --type=timer --escalate`, `gc bd gate check --type=gh --escalate`, and `gc bd gate list --json` in its command table ([gascity-packs gastown/agents/deacon/prompt.template.md](https://github.com/gastownhall/gascity-packs/blob/main/gastown/agents/deacon/prompt.template.md)) **[OFFICIAL]**. Human gates are deliberately excluded from `bd gate check` — the beads guidance is "keep `human` gates for the decisions that should never auto-close" **[OFFICIAL]**.

**Practical implication for Momentum:** author the human gate against `bd`, not against Gas City's `[steps.gate]`. **[Corrected during AVFL fix pass — CRIT-005; see `research-cycle-orchestration-fit.md` §1.]** This does *not* mean an `exec` step — Gas City v2 formulas have no `exec`, `command`, `run`, or `script` step key; steps are work beads that agents claim and execute inside sessions, and an unknown key like `exec` would compile clean and silently do nothing. The two constructs that actually exist: (1) a work step whose `description`/`description_file` instructs the claiming agent to run `bd gate create --type=human --blocks <downstream-step-bead-id>` as part of its work, or (2) an order-level `exec` script (orchestrator-hosted, no agent involved, capped at 300s by `[orders] max_timeout`). Either way, `--blocks` must resolve to the **downstream** step's bead id (not the gate-creating step's own id), and that id is only discoverable at cook time — via `gc.root_bead_id` + `gc.step_ref` metadata on the materialized beads — not at formula-authoring time.

---

## 3. Mail-to-human: real, threaded, and swept

`human` is a reserved address, not a convention:

> "`gc mail send` — Send a message to a session alias **or human**. … The sender defaults to `$GC_SESSION_ID`, `$GC_ALIAS`, `$GC_AGENT`, or **`"human"`**. … Use `--all` to broadcast to all live sessions **(excluding sender and "human")**."
> Documented example: `gc mail send human "Review needed for PR #42"`
> ([CLI reference — `gc mail send`](https://docs.gascity.com/reference/cli.md)) **[OFFICIAL]**

Every read-side command (`gc mail check`, `count`, `inbox`) defaults its recipient to `"human"` when no session env vars are set — i.e. **when a human runs `gc mail inbox` in their own terminal, they get the human mailbox** **[OFFICIAL]**. Tutorial 04's worked example shows `FROM  human` in the mayor's inbox, confirming the address round-trips ([Tutorial 04](https://docs.gascity.com/tutorials/04-communication.md)) **[OFFICIAL]**.

The return path carries payload. `gc mail reply <id> -m "<body>"` inherits the thread ID, and `--notify` "request[s] a recipient turn (including a managed wake if not running)". Delivery into the agent is automatic: "on each turn, `gc mail check --inject` runs and any unread mail appears as a system reminder in the agent's context" ([Tutorial 04](https://docs.gascity.com/tutorials/04-communication.md)) **[OFFICIAL]**.

**Two caveats that matter for Momentum:**

- **Mail is not durable audit.** `gc order sweep-nudge-mail` closes read mail beads past `--mail-ttl` (default **1h**), and "the controller watchdog also runs this sweep automatically every 5 minutes" ([CLI reference](https://docs.gascity.com/reference/cli.md)) **[OFFICIAL]**. A per-fork verdict left only in a mail body is gone within the hour. Verdicts must be persisted to bead metadata or a Momentum artifact file.
- **Mail alone never wakes anyone.** "Mail does not create wake demand by itself" — `--notify` is required, and in an unmanaged city the nudge only queues ([Tutorial 04](https://docs.gascity.com/tutorials/04-communication.md)) **[OFFICIAL]**.

---

## 4. The production pattern: "passive wait + mail" (and why Momentum probably can't use it)

The packs repo does not use `[steps.gate]` for HITL. It uses a named idiom — **"the passive wait + mail pattern"** — spelled out identically across at least three workflow assets: `gascity/assets/workflows/github-pr-review/human-gate-comment.md`, `gascity/assets/workflows/github-issue-triage-base/human-gate-sensitive-output.md`, and `superpowers/assets/workflows/superpowers-brainstorming/{target}.confirm-design-approval.md` **[OFFICIAL]**.

The recipe, verbatim in structure:

1. Stamp workflow-root metadata `…_gate=waiting-human`, `…_gate_bead_id=<this bead id>`, `…_gate_artifact_path=<path>`.
2. Park the session so idle handling doesn't recycle it:
   ```bash
   gc session wait "$SESSION_TARGET" --sleep --on-beads "$GC_BEAD_ID" \
     --note "Waiting for human approval … Resume with: gc session attach $SESSION_NAME"
   ```
3. Send **exactly one** mail (`gc mail send human …`), idempotent via a `…_gate_mail_sent=true` metadata flag; include artifact paths, the workflow-root id, the bead id, and "requested response options: approve, request changes, or reject."
4. "Wait for explicit human feedback from the active session **or** mail thread. If the session idles, detaches, or restarts before the human responds, do not close this bead."
5. Record **exactly one** terminal metadata value: `approved` | `rejected` | `revision_requested`. "Close fail only for explicit rejection or abort, **not for silence**."

The superpowers variant closes the loop back into the v2 check machinery: it sets `design_review.verdict=done|iterate` on the claimed bead, and `iterate` "re-opens the design loop for another brainstorming pass," with a mandated "concise revision summary that the next attempt can apply directly … must name the specific design sections, assumptions, or unresolved questions that caused the loopback" **[OFFICIAL]**. That is the closest thing in the ecosystem to Momentum's per-fork-verdict requirement.

`gc session wait` and its management surface are documented CLI: `--on-beads`, `--any`, `--note`, `--sleep`; plus `gc wait list/inspect/cancel` and **`gc wait ready <wait-id>`** ("Manually mark a wait ready") as a human release lever ([CLI reference](https://docs.gascity.com/reference/cli.md)) **[OFFICIAL]**.

There is also a notification watchdog for exactly this: a pack order `renudge-stale-human-gates.sh` (introduced in gascity#4553) that periodically re-mails the human about stale open human gates, deduped by a state ledger with `GC_STALE_GATE_RENUDGE_INTERVAL` defaulting to **1h** and a sweep cadence of 5 minutes — evidenced by bug [#4770](https://github.com/gastownhall/gascity/issues/4770) (CLOSED 2026-08-04), which reproduced the ledger being lost on mid-sweep death **[OFFICIAL]**. Human gates therefore have a real, if young, escalation loop behind them **[availability caveat, DOMAIN2-E-001]: this order is not in any tagged release** — it landed on `main` 2026-07-23 and ships only in the `edge` rolling pre-release, absent from v1.4.0 and v1.4.1 (see `research-notification-watcher-layer.md`).

**Why Momentum probably can't use this pattern directly.** The pattern requires a *resumable, long-lived session* to hold the wait. Momentum's proposed Gas City layer would run each phase as a work step claimed inside a session (not `claude -p /momentum:<skill>` as a subprocess — corrected per CRIT-005 above), but the session backing a `headless`-mode phase is still not meant to sit and wait. **[Downgraded during AVFL fix pass — MAJ-010.]** The table below is the packs' own **prompt convention**, read by the language model as instructions — it is not a compiled control-flow gate enforced by Gas City. Nothing in the runtime validates or blocks against these values; `interaction_mode` is stamped to `gc.var.interaction_mode` and read by agent prompts as text.

| `interaction_mode` | Prompt convention (not mechanically enforced) |
|---|---|
| `interactive` | Prose tells the agent it may ask questions and request approvals, one material question at a time with a recommendation. |
| `autonomous` | Prose tells the agent not to block on ordinary planning questions; record assumptions; block only for unsafe actions or missing required evidence. |
| `headless` | Prose tells the agent never to ask questions; missing required input should fail closed with machine-readable blocked reasons. |

([gascity-packs `gascity/REQUIREMENTS.md`](https://github.com/gastownhall/gascity-packs/blob/main/gascity/REQUIREMENTS.md), Mode Contracts) **[OFFICIAL]**

The PR-review asset's prompt text follows this convention: "In `headless` interaction mode, never wait on a human … Stop blocked with a machine-readable `gc.blocked_reason` instead of waiting" **[OFFICIAL]** — again, instruction text a shipped pack's prompt happens to carry, not a mechanism Gas City enforces. A Momentum-authored pack sets its own mode prose and is not bound by another pack's convention.

So a phase's work step — claimed and executed by an agent inside its session, per the corrected shape above, not a `claude -p` subprocess — is structurally `headless`. The correct adaptation for Momentum is to **invert the pattern**: rather than parking a live session, the phase step *creates the gate bead and exits successfully*. The gate blocks the next phase's step; the human resolves it out-of-band; the graph resumes. Session-parking is for always-on agents, not for one-shot phase-step sessions.

Note also that "asks one material question at a time" is a direct architectural conflict with Momentum's plan gate, which presents ≤7 forks at once and demands a written verdict on each.

---

## 5. Converge manual gates — real, but v1-only and payload-free

`gc converge` is a bounded iterative-refinement loop: "A root bead + formula + gate = repeat until the gate passes or max iterations are reached. The controller processes `wisp_closed` events and drives the loop automatically" ([CLI reference](https://docs.gascity.com/reference/cli.md)) **[OFFICIAL]**.

- `--gate` modes: `manual` (**the default**), `condition`, `hybrid`
- `--gate-timeout` default `5m0s`; `--gate-timeout-action` ∈ `iterate | retry | manual | terminate`
- `--max-iterations` default `5`
- Loop state `waiting_manual` is filterable via `gc converge list --state waiting_manual`
- Human verbs: `gc converge approve <bead-id>` and `gc converge iterate <bead-id>`

**[OFFICIAL]**, all from the CLI reference.

This is a genuine, implemented HITL gate with an approve/iterate dichotomy that maps cleanly onto Momentum's plan gate semantics. Two disqualifiers:

1. **v1-only.** "`gc converge` accepts only v1 formulas and rejects v2: `convergence wisps do not support v2 formula "<name>"; use a v1 formula until convergence has an explicit input convoy target`" ([formula-spec-v2 §5](https://docs.gascity.com/reference/specs/formula-spec-v2.md)) **[OFFICIAL]**. Adopting converge means adopting v1 formulas for that phase, forgoing v2's check loops, drains, and per-step routing.
2. **No payload.** Neither `approve` nor `iterate` takes any flag but `--json`. The verdict is a bare verb. Feedback must be smuggled in out-of-band before the verb is issued.

The maintainers' own guidance points away from it: "use `gc converge` when you need the pre-v2 gate-and-evaluate machinery; **otherwise prefer the v2 check loop above**" ([Understanding Formulas](https://docs.gascity.com/guides/understanding-formulas.md)) **[OFFICIAL]**.

The v2 successor is the **check loop with the verdict in bead metadata**: an `[template.check]` with `mode = "exec"` running a script (e.g. `.gc/scripts/checks/implementation-review-approved.sh`) that reads a verdict written by the preceding step. "The verdict travels as bead metadata; no judgment lives in Go" **[OFFICIAL]**. Crucially, an exec check script can read *any* metadata — including metadata a human wrote via `gc bd update --set-metadata` or `gc beads metadata-cas`. **That is the general-purpose v2 human gate with a payload.**

---

## 6. Feedback payload: the four carriers

| Carrier | Command | Payload shape | Durability |
|---|---|---|---|
| Gate resolution reason | `bd gate resolve <id> --reason "…"` | one free-text string, release-only (no reject verb) | on the closed gate bead — durable |
| Bead metadata | `gc bd update <id> --set-metadata k=v`; atomic: `gc beads metadata-cas <id> --key --expected --next --store-ref` | small keyed enums/paths | durable, machine-readable, what check scripts read |
| Artifact file + path in metadata | write file, stamp `…_gate_artifact_path=<abs path>` | unbounded prose — the packs' own choice for revision summaries | durable, and the only place rich per-fork verdicts fit |
| Mail thread | `gc mail reply <id> -m "…" --notify` | free-text, threaded, auto-injected into the agent's next turn | **swept ~1h after read** |

The pattern the packs converged on is a **triple**: enum in metadata (for the machine), path in metadata (for the pointer), prose in a file (for the human's actual words). Momentum should copy this exactly — the enum drives the graph, the file holds per-fork verdicts, and mail is only the doorbell.

---

## 7. Per-gate recommendation for Momentum

### (a) Triage approval — batch-approve classified observations

**Recommended: `bd gate --type=human`, one gate per triage batch, plus `gc mail send human --notify`.**

Triage approval is genuinely batch-shaped and mostly binary (approve the classification set, or send it back). The gate bead parks the `intake`/`decision` downstream steps; the human runs `bd gate list --json` to see it and `bd gate resolve <id> --reason "approved 14, rejected 2 (see triage-2026-08-21.md)"` to release. Payload need is **low** — a `--reason` string plus the existing Momentum triage artifact suffices. Do **not** use per-observation gates; the escalation loop (`renudge-stale-human-gates`, 1h interval — **not in a tagged release as of v1.4.1**, see §4 above) would spam.

### (b) Pre-sprint plan gate — visual companion surface, per-fork written verdicts

**Recommended: v2 check loop + verdict-in-metadata + artifact file. Gate bead only as the parking brake.**

This is the hardest fit, for three reasons:

1. Momentum's plan gate is **anti-rubber-stamp**: a blanket approve is insufficient, and each fork needs a one-line written verdict + reason. No Gas City primitive models an N-verdict payload. `bd gate resolve --reason` is one string; `gc converge approve` is zero.
2. Momentum's surface is a **visual HTML companion decision surface**. Gas City has no rendering or presentation layer for gates; the mail body is plain text. The mail can only carry a `file://` path to the artifact.
3. The pack contract's `interactive` mode mandates "one material question at a time," which is the opposite of a ≤7-fork single surface.

**Concrete shape (corrected during AVFL fix pass — CRIT-005; the original text described the `plan-gate` step as directly "creating" the gate and "exiting," which implied a shell-subprocess exec step that does not exist):** a `plan-gate` work step, claimed and executed by an agent inside its session, writes the HTML surface, stamps `momentum.plan_gate.artifact_path` and `momentum.plan_gate.status=waiting-human` on the workflow root, then — as part of that same claimed work, not a separate exec — runs `bd gate create --type=human --blocks <downstream-conduct-step-bead-id> --reason "Plan gate: <sprint-slug>"` (the downstream bead id resolved at cook time via `gc.root_bead_id`/`gc.step_ref`), mails the human the path + gate id, and closes its own bead. **[DOMAIN2-A-003]** This prose-instructed gate creation carries the same silent-failure class CRIT-005 eliminated for `exec`: an agent can skip or garble the `bd gate create` call and the step still closes successfully, leaving no gate and no ask. The following phase's check script should verify the gate bead actually exists (not merely that `momentum.plan_gate.status` was stamped) before treating the plan gate as pending — or gate creation should move to an order-level `exec` step, where execution is guaranteed rather than agent-discretionary. The developer fills verdicts into a sibling `plan-gate-verdicts.md`, sets `momentum.plan_gate.status=approved|revision_requested`, and resolves the gate. A `[steps.check]` exec script (note: `check` cannot be combined with `gate` on the same step per `research-human-verdict-patterns.md` §1 — this must be a separate step from the one that created the gate) on the following phase reads the status and either proceeds or re-spawns planning. The **anti-rubber-stamp check belongs in Momentum's own script**, not in Gas City — the script should refuse to pass if the verdicts file has fewer written verdicts than declared forks. Gas City can carry the state; it cannot enforce the standard.

### (c) Mid-story tooling gate — human must exercise nornspun/chorgi

**Recommended: `bd gate --type=human`. This is the single cleanest fit in the whole set.**

Here the human's job is to *do* something, not to author a rich verdict, and the outcome is genuinely binary ("I exercised it; it works" / "it doesn't"). `bd gate create --type=human --blocks <story-verify-step> --reason "Exercise nornspun locally: <scenario list>"` parks exactly one story's downstream steps while sibling stories keep running — the gate blocks through an ordinary dependency edge, so the rest of the frontier is untouched ([beads gates.md](https://github.com/gastownhall/beads/blob/main/docs/workflows/gates.md)) **[OFFICIAL]**. `bd gate resolve --reason "exercised 3 flows, cmd palette lag noted"` carries enough payload. `bd gate add-waiter` registers the worker for a wake when it closes. `bd blocked` gives the developer a standing "what am I holding up" list — which is precisely the visibility Momentum's mid-story gates lack today.

Explicitly **do not** use the passive-wait pattern here: parking a live session for the hours or days a manual tool exercise may take is what `--sleep` was built for in always-on cities, and is wasteful and fragile for a one-shot phase-step session that claims, executes, and exits (not a persistent `claude -p` subprocess — see the corrected framing above).

### (d) Post-sprint results gate — end-gate report + retro digest before merge/close

**Recommended: `bd gate --type=human` on the merge/close step, with `--reason` carrying the verdict and the report path in metadata.**

Structurally identical to the triage gate but higher-stakes, and it should be **fail-closed on silence** in the packs' sense: "Close fail only for explicit rejection or abort, not for silence" — i.e. an unresolved results gate must never time out into a merge. Note that `bd gate check` never auto-closes `human` gates, so this is the default behavior, not something to configure **[OFFICIAL]**. If Momentum wants nagging, the `renudge-stale-human-gates` order is the existing precedent (not in a tagged release — see §4); it re-mails rather than releasing.

**Barrier caveat (MERGED-002):** this recommendation covers the gate *primitive* — block on human decision, resolve on explicit command — which is proven (Q3, `research-gate-mechanics-handson.md`). It does **not** cover how conduct's fanned-out story children get drained into one barrier before this gate is even reachable: `waits_for` is inert (#2311) and container `needs` does not gate runtime-discovered children (#3451), with no workaround available to Momentum's sprint-planning-time-unknown story set. `research-maturity-open-bugs.md`'s "Momentum-relevant synthesis" table rates gate (d) **Blocked** on that basis, not "Fits" — the barrier construction (`drain` + a `check` loop), not the gate, is what remains unproven.

### Summary table

| Momentum gate | Mechanism | Payload | Why not the alternatives |
|---|---|---|---|
| Triage approval | `bd gate --type=human` (one per batch) + mail `--notify` | `--reason` string | Converge is v1-only; assignee is silent |
| Plan gate (per-fork verdicts) | verdict-in-metadata + artifact file; gate bead as brake; Momentum-side check script enforces anti-rubber-stamp | metadata enum + `.md` verdicts file | No primitive carries N verdicts; `converge approve` is payload-free; `interactive` mode mandates one-question-at-a-time |
| Mid-story tool exercise | `bd gate --type=human` per story | `--reason` string | Passive-wait burns a session for hours/days; `[steps.gate]` type is inert |
| Results gate | `bd gate --type=human` on merge/close | `--reason` + report path in metadata | Timer/auto-close would defeat the gate; `human` gates never auto-close, which is what we want. **Barrier caveat:** the gate itself is proven; the fan-out barrier feeding it is not — see (d) above |

---

## 8. Risks and open gaps

- **The `[steps.gate]` trap.** A Momentum formula author writing `type = "human"` in a Gas City v2 `[steps.gate]` block gets a gate bead that blocks correctly but has no typed identity, no watcher, and no `bd gate list` visibility as a *human* gate. Route through `bd gate create` instead. ([gascity#4399](https://github.com/gastownhall/gascity/issues/4399), OPEN) **[OFFICIAL]**
- **Beads coupling is real but narrower than "the DEC-028 Dolt go/no-go."** [Reconciled during AVFL fix pass — DOMAIN2-E-002.] Every recommendation above lands in `bd`, not `gc` — the gate state lives in the beads store. That much is true *today*, using the `bd` Momentum already has installed with its existing embedded Dolt, and does not by itself require flipping DEC-028's authoritative-ledger question (see `research-beads-coupling-dec028.md` §7's corrected framing: a scoped, city-local Dolt requirement for the gate primitive, not a decision about `.momentum/*/index.json`). Separately, and still open: whether Momentum's own ledger (`.momentum/*/index.json`) ever *becomes* beads-authoritative is DEC-028's actual go/no-go, and adopting `bd gate` for HITL does not force it either way — though a shared-store future (beads-coupling §7 "Unlocked (b)") would make the two questions converge.
- **No presentation layer.** Gas City carries paths and enums. Momentum's visual companion surface, and the anti-rubber-stamp enforcement, remain entirely Momentum's to build and enforce.
- **Attribution is lossy.** "every `bead.closed` event is attributed to `actor=cache-reconcile` — the real closer is unrecoverable at the event layer" ([gascity#5214](https://github.com/gastownhall/gascity/issues/5214), OPEN, updated 2026-08-13) **[OFFICIAL]**. A resolved gate does not prove *who* resolved it; audit provenance must be written into `--reason`/metadata by the resolver, not inferred from events.
- **Human-gate escalation is young.** `renudge-stale-human-gates` was introduced in #4553 and had a durability bug fixed as recently as 2026-08-04 (#4770). Treat the nag loop as beta.
- **`gc session nudge` / `attach` remain the only "human tells an agent" channel** (Tutorial 03) **[OFFICIAL]** — real and useful for interactive debugging, but not a gate: nudge is fire-and-forget, does not survive a crash, and has no state.

---

## Sources

- https://docs.gascity.com/llms.txt — documentation index **[OFFICIAL]**
- https://docs.gascity.com/reference/specs/formula-spec-v2.md — Formula Specification v2 (last verified 2026-06-12); §2 gates and `waits_for`, §4 Accepted But Inert, §5 converge/v1 compatibility **[OFFICIAL]**
- https://docs.gascity.com/reference/cli.md — CLI Reference: `gc mail`, `gc converge`, `gc ready`, `gc sling`, `gc session wait`, `gc wait`, `gc bd`, `gc beads metadata-cas`, `gc order sweep-nudge-mail` **[OFFICIAL]**
- https://docs.gascity.com/tutorials/03-sessions.md — Tutorial 03: sessions, peek/attach/nudge/logs **[OFFICIAL]**
- https://docs.gascity.com/tutorials/04-communication.md — Tutorial 04: mail vs nudge, `FROM human`, hook injection **[OFFICIAL]**
- https://docs.gascity.com/guides/understanding-formulas.md — check loops, verdict-in-metadata, `review_mode`, converge guidance **[OFFICIAL]**
- https://github.com/gastownhall/beads/blob/main/docs/workflows/gates.md — beads Gates: type table incl. `human`, formula `[steps.gate]`, `bd ready --gated` **[OFFICIAL]**
- https://github.com/gastownhall/beads/blob/main/docs/cli-reference/gate.md — `bd gate create/check/list/resolve/show/add-waiter/discover` flags **[OFFICIAL]**
- https://github.com/gastownhall/gascity-packs/blob/main/gascity/assets/workflows/github-pr-review/human-gate-comment.md — passive wait + mail pattern, headless refusal **[OFFICIAL]**
- https://github.com/gastownhall/gascity-packs/blob/main/gascity/assets/workflows/github-issue-triage-base/human-gate-sensitive-output.md — same pattern, triage variant **[OFFICIAL]**
- https://github.com/gastownhall/gascity-packs/blob/main/superpowers/assets/workflows/superpowers-brainstorming/%7Btarget%7D.confirm-design-approval.md — human gate feeding `design_review.verdict=done|iterate` **[OFFICIAL]**
- https://github.com/gastownhall/gascity-packs/blob/main/gascity/REQUIREMENTS.md — Mode Contracts (`interaction_mode`, `review_mode`), Approval States **[OFFICIAL]**
- https://github.com/gastownhall/gascity-packs/blob/main/gastown/agents/deacon/prompt.template.md — `gc bd gate check --escalate`, `gc bd gate list --json` in production patrol **[OFFICIAL]**
- https://github.com/gastownhall/gascity/blob/main/internal/sling/sling.go — `Reassign` doc comment: human-claimed beads invisible to pool claim filter (#1007) **[OFFICIAL]**
- https://github.com/gastownhall/gascity/issues/4399 — `[steps.gate]` type vocabulary parsed-but-not-enforced (OPEN, 2026-07-19) **[OFFICIAL]**
- https://github.com/gastownhall/gascity/issues/4770 — `renudge-stale-human-gates` ledger loss (CLOSED, 2026-08-04) **[OFFICIAL]**
- https://github.com/gastownhall/gascity/issues/4837 — bare `human` label vs `hold:mayor` axis conflict (OPEN, 2026-08-14) **[OFFICIAL]**
- https://github.com/gastownhall/gascity/issues/5214 — `bead.closed` attributed to `actor=cache-reconcile` (OPEN, 2026-08-13) **[OFFICIAL]**

*Empirical check performed 2026-08-21:* `gh api -X GET search/code -f q='repo:gastownhall/gascity-packs "steps.gate"'` → `total_count: 0`, corroborating the spec's "Zero bundled formulas use `gate`." **[EMPIRICAL]**

*Source currency:* all Gas City docs pages carry recent verification stamps (formula-spec-v2: "Last verified 2026-06-12"); all cited issues were updated between 2026-07-19 and 2026-08-21. No source older than 12 months was used.

**Corpus cross-references (added during AVFL fix pass):** `research-cycle-orchestration-fit.md` §1 (no `exec` step key in v2 formulas) — **[OFFICIAL]**; `research-human-verdict-patterns.md` §1 (`check` cannot combine with `gate` on one step) — **[OFFICIAL]**.
