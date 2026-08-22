---
content_origin: claude-code-subagent
date: 2026-08-21
sub_question: "Human-verdict patterns: check-loops/[template.check] with human-recorded verdicts in bead metadata — supported conventions in gascity-packs, converge manual gates, approve/iterate/reject semantics"
topic: "Gas City HITL gates and cycle orchestration for Momentum"
---

## Headline

Gas City has **two mutually exclusive loop primitives**, and only the deprecated one has a human gate.

1. **`[steps.check]` / `[template.check]` (formula contract v2)** — the primitive every maintained pack actually uses. It is a **poll-and-burn** loop: an exec script is run after each attempt, exit 0 stops, exit 1 spawns the next attempt, exhaustion closes the step **failed**. It has **no waiting state and no human affordance whatsoever.**
2. **`gc converge` (formula contract v1 only)** — has a genuine `--gate manual` mode with a `waiting_manual` state and `gc converge approve` / `iterate` / `stop` operator verbs. The v2 spec states outright that converge rejects v2 formulas, and **zero shipped pack formulas enable convergence**, so it is unreachable from any maintained pack.

The bridge between them is **`[steps.gate]`**, which synthesizes a real blocking gate bead. Its `type = "human"` string is inert doc-comment vocabulary — but the *blocking* is real, and for a human gate inertness costs nothing, because closing the bead is the human's job, not a watcher's.

On the narrow question asked: **yes, a check script can read a human-recorded disposition** — the verdict is plain bead metadata written by `gc bd update --set-metadata`, and nothing in the read path records or checks actor provenance. The problem is not authorization; it is that **a check loop polls instead of waiting.**

---

## 1. What `[template.check]` actually is

The canonical instance is `build-basic-review.formula.toml`, the starter review expansion for Gas City's own `build-basic` methodology ([gascity-packs @ 28e2e84](https://github.com/gastownhall/gascity-packs/blob/main/gascity/formulas/build-basic-review.formula.toml)) **[OFFICIAL]**:

```toml
[[template]]
id = "{target}.build-basic-review-loop"
title = "Run build-basic starter review until approved"

[template.check]
max_attempts = 6

[template.check.check]
mode = "exec"
path = ".gc/scripts/checks/implementation-review-approved.sh"
timeout = "10m"
```

The spec defines the keys as: `max_attempts` (total attempts including the first, ≥ 1), `check.mode` (only `"exec"` supported), `check.path`, `check.timeout` ([formula-spec-v2 §3.1](https://docs.gascity.com/reference/specs/formula-spec-v2)) **[OFFICIAL]**. Semantics, quoted:

> `[steps.check]` wraps a step in an inline run/check verification loop: after each iteration closes, the orchestrator runs the configured script; pass closes the step, fail with budget left spawns the next iteration, **exhaustion closes the step as failed**.

`[template.check]` is the same construct inside an `type = "expansion"` formula; `[steps.check]` is the form on a plain step. Materialization emits a `<step>.spec` sidecar, `<step>.iteration.N` beads as the agent-visible work, and keeps the original step ID as a control bead of kind `ralph` **[OFFICIAL]**.

**Hard structural constraint, load-bearing for Momentum:**

> `check` must not be combined with `loop`, `on_complete`, **`gate`**, `expand`, `assignee`, or `retry`.

A single step therefore **cannot** carry both a check loop and a gate. Momentum's "iterate until the reviewer is satisfied, then ask the human" needs *two* steps.

Also note `on_exhausted` (`hard_fail` / `soft_fail`) is a key of **`retry`**, not of `check` ([formula-spec-v2 §3.2](https://docs.gascity.com/reference/specs/formula-spec-v2)) **[OFFICIAL]**. A check loop's exhaustion is unconditionally a failed step — there is no "the human said no, and that's a legitimate outcome" encoding.

---

## 2. How "the verdict travels as bead metadata" works concretely

### The write side

Pack workflow prompts instruct the agent to write the verdict with an ordinary CLI call. From `build-basic-review/{target}.apply-review-findings.md` **[OFFICIAL]**:

```bash
gc bd update "$CLAIMED_BEAD_ID" \
  --set-metadata 'gc.outcome=pass' \
  --set-metadata 'code_review.verdict=done' \
  --set-metadata 'code_review.report_path=<starter review summary path>' \
  --set-metadata 'code_review.output_path=<starter review summary path>'
gc bd close "$CLAIMED_BEAD_ID" --reason 'Build-basic starter review approved.'
```

`adopt-pr-review-approved.sh` documents the same convention in its header comment: *"The apply-fixes step sets this after applying synthesis findings: `gc bd meta set $BEAD_ID review.verdict=done` / `review.verdict=iterate`"* **[OFFICIAL]**.

**This is an ordinary metadata write with no provenance requirement.** There is no signing, no actor field consulted, no "written by agent" flag. Whoever can run `bd update` can set the verdict.

### The read side

`implementation-review-approved.sh` is the reference reader ([gascity-packs](https://github.com/gastownhall/gascity-packs/blob/main/gascity/assets/scripts/checks/implementation-review-approved.sh)) **[OFFICIAL]**. Its shape:

1. Read `GC_BEAD_ID` (required) and `GC_ITERATION` (defaults `"0"`) from the environment.
2. `gc bd show "$ROOT_ID" --json` → resolve `gc.root_bead_id`, `gc.step_id`, `gc.scope_ref`.
3. `gmol()` — fan four concurrent `gc ready --metadata-field "gc.root_bead_id=$root" --status <st>` reads across `open|in_progress|blocked|closed`, union, `unique_by(.id)`, **`sort_by(.updated_at)`**.
4. Extract the newest `code_review.verdict` among members whose `gc.attempt` equals the current attempt.
5. Fall back to three per-lane keys when no top-level verdict exists.

The full metadata key inventory read by the shipped check scripts:

| Key | Read by | Purpose |
|---|---|---|
| `code_review.verdict` | `implementation-review-approved.sh`, `code-review-approved.sh` | Top-level stop/iterate decision |
| `code_review.acceptance_verdict` | `implementation-review-approved.sh` | Lane verdict (acceptance/correctness) |
| `code_review.test_evidence_verdict` | `implementation-review-approved.sh` | Lane verdict (test evidence) |
| `code_review.simplicity_verdict` | `implementation-review-approved.sh` | Lane verdict (simplicity) |
| `code_review.report_path` / `.output_path` / `.review_report_path` | `implementation-review-approved.sh` | Satisfies `review_mode=report` short-circuit |
| `design_review.verdict` | `design-review-approved.sh` | Design-review loop |
| `gap_analysis.verdict` / `.report_path` | `gap-analysis-approved.sh` | Gap-analysis loop |
| `review.verdict` | `adopt-pr-review-approved.sh` | adopt-PR loop |
| `gc.attempt`, `gc.root_bead_id`, `gc.step_id`, `gc.scope_ref`, `gc.step_ref`, `gc.ralph_step_id`, `gc.continuation_group` | all | Scoping — which loop, which iteration |
| `gc.var.review_mode` | `implementation-review-approved.sh` | Mode short-circuit |

The scripts' own comments record two production bugs worth inheriting as design warnings **[OFFICIAL]**: `gc bd list --metadata-field` is *"a collection query carrying no bead id, so on a city that relocates the graph class bd has nothing to route on and refuses the read — and the `2>/dev/null` below turned that refusal into an empty set, so this gate never saw `code_review.verdict` and looped until Ralph ran out of attempts"*; and without the explicit `sort_by(.updated_at)` re-sort, *"the gate picks a verdict by id hash and can sit on a stale `iterate` forever while a newer `done` is ignored."* **Both failure modes are silent-starvation of a gate** — precisely the class of bug that turns an approval gate into a rubber stamp.

### Verdict vocabulary (check loops)

Normalized across the five shipped scripts **[OFFICIAL]**:

| Bucket | Accepted values | Effect |
|---|---|---|
| Stop / approve | `done`, `approved`, `pass` (lane helper also accepts `approve`) | exit 0 — step closes successfully |
| Continue | `iterate`, `fail`, `retry` | exit 1 — next attempt |
| Empty | `""` | exit 1 — treated as "missing verdict" |
| Unknown | anything else | exit 1 — `code-review-approved.sh` logs *"Unknown verdict: $VERDICT — treating as iterate"* |

**There is no reject / block value in this vocabulary.** The only terminal-negative outcome is exhausting `max_attempts`, which the spec says closes the step *failed*.

---

## 3. Can a check script read a **human**-recorded disposition?

**Yes — mechanically trivial, semantically wrong for a blocking gate.** **[EMPIRICAL]** + **[OFFICIAL]**

*Mechanically:* `check.mode = "exec"` runs an arbitrary script. The script is opaque to the orchestrator — it may read bead metadata, a file, a git note, an HTTP endpoint. Nothing in `internal/dispatch/ralph.go` or the check scripts consults who authored a metadata value. I verified the round trip end to end on Momentum's own installed `bd`:

```
$ bd update gatetest-ss3 \
    --set-metadata "code_review.verdict=done" \
    --set-metadata "verdict.actor=human:steve" \
    --set-metadata "verdict.reason=fork-1 adopt; fork-2 change wave order"
✓ Updated issue: gatetest-ss3 — plan-gate demo story

$ bd show gatetest-ss3 --json | jq -r '(if type=="array" then (.[0]//{}) else . end)
    | .metadata["code_review.verdict"] // "<empty>"'
done
```

The extractor used is the exact jq shape from `implementation-review-approved.sh`. A human-written verdict is indistinguishable from an agent-written one. (Recording `verdict.actor` / `verdict.reason` alongside is a Momentum-side convention — no shipped script reads them, but nothing stops you adding keys, and they give the audit trail the anti-rubber-stamp requirement needs.)

*Semantically:* the check loop **does not wait**. The environment handed to a v2 check script (`internal/dispatch/ralph.go` → `convergence.RunCondition`) is `GC_BEAD_ID`, `GC_ITERATION`, `GC_CITY_PATH`, `GC_STORE_PATH`, `GC_WORK_DIR`, `GC_MOLECULE_DIR`, `GC_ARTIFACT_DIR` **[OFFICIAL]** — a one-shot evaluation under a timeout, `retryBudget = 0`. If the human has not yet recorded a verdict, the script exits 1, and the orchestrator **spawns another agent iteration of the work**. It does not pause for the human; it redoes the job and asks again. With `max_attempts = 6` and a human on a lunch break, the loop burns its budget and closes the step failed.

You can hack around this by making the check script block (`until bd show … | grep -q verdict; do sleep 30; done`), but you are then holding a dispatch slot hostage against `check.timeout` (10m in the shipped packs), and timeout is not "keep waiting". **A check loop is the wrong primitive for a human gate.** The right one is `[steps.gate]`.

---

## 4. `gc converge --gate manual` — real, and v1-only

`gc converge create` defaults to the manual gate ([`cmd/gc/cmd_converge.go`](https://github.com/gastownhall/gascity/blob/main/cmd/gc/cmd_converge.go)) **[OFFICIAL]**:

```go
cmd.Flags().StringVar(&gateMode, "gate", "manual", "Gate mode: manual, condition, hybrid")
cmd.Flags().StringVar(&gateTimeoutAction, "gate-timeout-action", "iterate",
    "Action on gate timeout: iterate, retry, manual, terminate")
```

This is a genuinely well-built HITL primitive — everything the check loop lacks:

- **A waiting state.** `convergence.state = waiting_manual`. In `handler.go`: *"Manual mode: no gate evaluation, transition to `waiting_manual`."* The loop parks indefinitely; nothing burns.
- **Operator verbs.** `gc converge approve` ("Approve and close a convergence loop (manual gate)"), `gc converge iterate` ("Force next iteration (manual gate)"), `gc converge stop`.
- **Actor attribution, built in.** `ApproveHandler` stamps `convergence.terminal_actor = "operator:" + username` and `terminal_reason = approved`. The human's identity is a first-class recorded field — not a convention you bolt on.
- **A three-value verdict vocabulary.** `internal/convergence/metadata.go`: `VerdictApprove = "approve"`, `VerdictApproveWithRisks = "approve-with-risks"`, `VerdictBlock = "block"`.
- **Fail-closed normalization.** `NormalizeVerdict` lowercases, trims, maps past tense (`approved`→`approve`, `blocked`→`block`), and **maps anything unrecognized — including empty — to `block`.** Contrast the check scripts, which map unknown to *iterate*.
- **Hybrid mode.** `--gate hybrid` runs a condition script with `GC_AGENT_VERDICT` in the environment; with no condition configured it falls back to `waiting_manual` (`hybrid.go`, `HybridNeedsManual`). This is the closest thing Gas City has to "machine screens, human decides."
- **Timeout escalation to a human.** `--gate-timeout-action manual` parks in `waiting_manual` on gate timeout rather than iterating.

**It is unreachable from v2.** The v2 spec's "Differences from v1" section, verified identically in-repo and on the live docs site **[OFFICIAL]**:

> **`gc converge` accepts only v1 formulas** and rejects v2:
> ```text
> convergence wisps do not support v2 formula "<name>"; use a v1 formula until convergence has an explicit input convoy target
> ```
> The v2 construct for iterate-until-verified semantics is the check loop (section 3.1); `gc converge` is the pre-v2 command for this pattern.

The spec frames this as a gap, not a design commitment ("neither is a design commitment"), but as of 2026-08-21 there is no v2 equivalent of `--gate manual`. **The v2 check loop is a strict functional *regression* on human-in-the-loop**: it dropped the waiting state, the operator verbs, the actor attribution, and the fail-closed default.

**And no shipped pack can use it.** A formula must set `convergence = true` to be valid for converge (`ValidateForConvergence`, `internal/convergence/formula.go`). I grepped every `.toml` in both repositories for `convergence = true` — **zero matches** **[EMPIRICAL]**. All 98 shipped formulas declare `contract = "graph.v2"` or are v2-compiler-gated. Adopting converge means authoring v1 formulas from scratch and abandoning the maintained pack ecosystem.

`ValidateForConvergence` also requires any custom evaluate prompt to contain the literal substrings `bd meta set` and `convergence.agent_verdict` — confirming the verdict write path is, again, an ordinary metadata write a human could perform.

---

## 5. `[steps.gate]` — the actual blocking primitive, and the `bd gate` CLI

This is the finding most useful to Momentum, and it is better than the spec's own caveat makes it sound.

The spec ([formula-spec-v2 §, and formula-spec-v1 §4](https://docs.gascity.com/reference/specs/formula-spec-v2)) **[OFFICIAL]**:

> A `[steps.gate]` table synthesizes a sibling gate bead (type `gate`, title `Gate: <type> <id>`) and a `blocks` edge from the gated step to it: **the step stays blocked until the gate bead is closed.**

And the caveat, stated as a known limitation:

> **Gate `type` vocabulary.** `[steps.gate]` synthesizes a real gate bead that blocks its step until the gate bead is closed (manually or by an external watcher), but the `type` values `gh:run`, `gh:pr`, `timer`, `human`, and `mail` are doc-comment vocabulary in `internal/formula/types.go` — the parser never validates them and **no bundled watcher acts on them. Zero bundled formulas use `gate`.**

**Read that carefully: the blocking is real; only the `type` *string* is inert.** For `gh:run` or `timer`, an inert type is fatal — nothing will ever close the gate. For `type = "human"`, it costs nothing: **closing the gate bead is the human's job by definition.** The one gate type that needs no watcher is the one Momentum needs.

The primitive is exposed directly in `bd`, and — importantly — **`human` is the default type**:

```
Gate types:
  human   - Requires manual 'bd gate resolve' (default)
  timer   - Auto-resolves after --timeout duration
  gh:run  - Waits for GitHub Actions workflow
  gh:pr   - Waits for PR merge
```

I exercised the full block/resolve cycle on Momentum's installed `bd 1.0.4 (ce242a879)` **[EMPIRICAL]**:

```
$ bd q "plan-gate demo story"                    → gatetest-ss3
$ bd ready --json | jq -r '.[].id'               → gatetest-ss3

$ bd gate create --type=human --blocks gatetest-ss3 \
    --reason="Momentum pre-sprint plan gate: developer must record per-fork verdicts"
✓ Created gate gatetest-b34 (type: human)
  Blocks: gatetest-ss3 (plan-gate demo story)
  Resolve with: bd gate resolve gatetest-b34

$ bd ready --json | jq -r '.[].id'               → (empty — story is blocked)

$ bd gate resolve gatetest-b34 --reason "approved by developer"
✓ Gate resolved: gatetest-b34

$ bd ready --json | jq -r '.[].id'               → gatetest-ss3
```

The gate blocks readiness indefinitely, with no attempt budget and no timeout, and resolves on an explicit human command carrying a reason string. **This is exactly the shape of all four Momentum HITL points**, and it works today in the `bd` Momentum already has installed — no Gas City daemon required.

---

## 6. Mapping approve / iterate / reject onto the mechanisms

| Momentum verdict | Check loop (v2 — what packs use) | `gc converge` manual gate (v1) | `[steps.gate]` / `bd gate` |
|---|---|---|---|
| **Approve** | `code_review.verdict=done\|approved\|pass` → exit 0, step closes | `gc converge approve` → `terminal_reason=approved`, `terminal_actor=operator:<user>` | `bd gate resolve <id> --reason "…"` → step unblocks |
| **Request changes / iterate** | `=iterate\|fail\|retry` → exit 1, **respawns the agent work**, decrements budget | `gc converge iterate` → pours next wisp, back to `active`; refuses past `max_iterations` | Not expressible — a gate is binary open/closed. Needs a paired check loop or a re-dispatch |
| **Reject / block** | **No encoding.** Only reachable by exhausting `max_attempts` → step closes *failed* (indistinguishable from the work being broken) | `gc converge stop` → `terminal_reason=stopped`; plus `VerdictBlock` as a first-class agent verdict | Leave the gate open (blocks forever), or close the gated step out-of-band |

Two asymmetries matter:

- **Reject is the weak spot everywhere, and worst in v2.** Momentum's plan gate and results gate both need a "no, do not proceed" that is distinct from "the automation broke." The check loop cannot express it at all; `converge stop` can (`terminal_reason=stopped`, distinct from `approved` and from `no_convergence`); a gate expresses it only as indefinite blockage. **[OFFICIAL]**
- **Default-on-ambiguity is inverted between the two loops.** Check loops treat unknown/empty as *iterate* (fail-open into more agent work). Converge's `NormalizeVerdict` treats unknown/empty as *block* (fail-closed). For a human gate, fail-closed is the only defensible default — and it is the one v2 dropped.

### `interaction_mode` and `review_mode` are not gates

Both are launch variables on the `build-base` contract (`interaction_modes = ["interactive","autonomous","headless"]`, `review_modes = ["report","agent","interactive"]`) **[OFFICIAL]**. Neither is mechanically enforced. `interaction_mode` is stamped to `gc.var.interaction_mode` and read **by agent prompts** — e.g. `github-issue-fix-base/design-review.md`: *"In `headless` mode, never ask…"*. It is an instruction to a language model, not a control-flow gate; I found zero references to it in any check script. And `review_mode=interactive` does not mean "a human participates" — the README defines it as *"an interactive top-level review that **may apply safe fixes**"*, i.e. the reviewing agent's write authority. **Do not mistake either for a HITL mechanism.**

---

## 7. Empirical hazard: `--set-metadata` coerces numeric values, silently breaking attempt scoping

Discovered while reproducing the pack extractors against `bd 1.0.4` **[EMPIRICAL]**. Every shipped check script scopes verdicts by attempt with a **string** comparison:

```jq
select((.metadata["gc.attempt"] // "") == $attempt)   # $attempt passed via --arg (always a string)
```

But `bd update --set-metadata gc.attempt=0` stores a JSON **number**:

```
$ bd show gatetest-ss3 --json | jq -r '… | .metadata | to_entries[]
    | "\(.key)\t\(.value|type)\t\(.value|tostring)"'
gc.attempt              number  0
verdict.actor           string  human:steve
code_review.verdict     string  done

$ bd list --all --json --limit=0 | jq -r --arg a "0" '.[0].metadata["gc.attempt"] as $v
    | "stored=\($v) storedtype=\($v|type) arg=\($a) ==> equal? \($v == $a)"'
stored=0 storedtype=number arg=0 argtype=string  ==> equal? false
```

The attempt-scoped extractor returns `<none>` — **the verdict is invisible to the gate** — while the unscoped `bd show` read returns `done`. Adding `|tostring` fixes it:

```
$ bd list --all --json --limit=0 | jq -r --arg attempt "0" '
   [ .[] | select(((.metadata["gc.attempt"] // "")|tostring)==$attempt)
         | select((.metadata["code_review.verdict"] // "")!="")
         | .metadata["code_review.verdict"] ] | last // "<none>"'
done
```

This is the *exact* silent-starvation failure the pack scripts' own comments describe (*"this gate never saw `code_review.verdict` and looped until Ralph ran out of attempts"*). **Scope caveat:** I exercised the `bd`-direct write path, since `gc` is not installed here; `gc bd update` wraps `bd` and may or may not preserve string typing. Either way, **any Momentum-authored check or gate script must coerce with `|tostring` before comparing**, and must never rely on `2>/dev/null` to swallow a failed read — a swallowed error and a genuine "not approved" are the same empty string, and that is a gate that silently passes nobody.

---

## 8. Implications for Momentum's four HITL points

Against Momentum's gates as specified:

- **(b) Pre-sprint plan gate** and **(d) post-sprint results gate** — these are blocking human decisions with a written verdict per fork. Use **`[steps.gate]` / `bd gate create --type=human`**, not a check loop. The gate blocks indefinitely, resolves on explicit command with a `--reason`, and needs no watcher. Momentum's anti-rubber-stamp requirement (a blanket approve is insufficient) maps to writing one metadata key per fork (`verdict.fork.<slug>=adopt|change|reject` plus a reason) *before* `bd gate resolve` — and to a resolve-time script that refuses if any fork key is missing. **Nothing in Gas City enforces that for you**; it is Momentum-side policy, but it is expressible.
- **(c) Mid-story tooling gates** (developer must exercise nornspun/chorgi by hand) — the cleanest fit of all. A `human` gate bead per tool-exercise step is exactly "block this story until a person does a thing and says so."
- **(a) Triage batch approval** — a single gate over the batch, with per-observation dispositions written as metadata before resolve.
- **The check loop still has a role**, just not as the human gate: it is the right primitive for the *agent-side* review iteration that runs **before** the human is asked. Because `check` cannot be combined with `gate` on one step, the pattern is two steps: `review-loop` (check, agent verdicts) → `human-gate` (gate, blocks on the person).
- **Do not plan around `gc converge`.** Its manual gate is the best-designed HITL surface in the codebase, but it is v1-only, no shipped formula enables it, and adopting it means forgoing the maintained pack ecosystem. Treat it as evidence of *what Gas City knows a human gate needs* — waiting state, operator verbs, actor attribution, fail-closed defaults — and as a checklist for what Momentum must supply itself on top of `bd gate`.

**Bearing on the DEC-028 beads/Dolt go/no-go:** the human-gate primitive lives in `bd`, not in the Gas City daemon, and it worked here against the already-installed `bd 1.0.4`. That decouples "can we express Momentum's HITL gates in beads" from "do we adopt Gas City as the cycle-level layer" — the first is demonstrably yes today. But it does raise the stakes on `.momentum/*/index.json` remaining authoritative: a gate that blocks `bd ready` only gates work that is *dispatched through* `bd ready`, which under dual-write it currently is not.

---

## Sources

Repositories inspected at HEAD on 2026-08-21 (`gascity` @ `151168c7`, 2026-08-21; `gascity-packs` @ `28e2e84e`, 2026-08-18) — both current, well inside the 12–18 month freshness window.

- [gascity-packs — build-basic-review.formula.toml](https://github.com/gastownhall/gascity-packs/blob/main/gascity/formulas/build-basic-review.formula.toml) **[OFFICIAL]**
- [gascity-packs — github-issue-fix-design-review-work.formula.toml](https://github.com/gastownhall/gascity-packs/blob/main/gascity/formulas/github-issue-fix-design-review-work.formula.toml) **[OFFICIAL]**
- [gascity-packs — build-base.formula.toml](https://github.com/gastownhall/gascity-packs/blob/main/gascity/formulas/build-base.formula.toml) **[OFFICIAL]**
- [gascity-packs — implementation-review-approved.sh](https://github.com/gastownhall/gascity-packs/blob/main/gascity/assets/scripts/checks/implementation-review-approved.sh) **[OFFICIAL]**
- [gascity-packs — design-review-approved.sh](https://github.com/gastownhall/gascity-packs/blob/main/gascity/assets/scripts/checks/design-review-approved.sh) **[OFFICIAL]**
- [gascity-packs — gap-analysis-approved.sh](https://github.com/gastownhall/gascity-packs/blob/main/gascity/assets/scripts/checks/gap-analysis-approved.sh) **[OFFICIAL]**
- [gascity-packs — code-review-approved.sh](https://github.com/gastownhall/gascity-packs/blob/main/gastown/assets/scripts/checks/code-review-approved.sh) **[OFFICIAL]**
- [gascity-packs — adopt-pr-review-approved.sh](https://github.com/gastownhall/gascity-packs/blob/main/gastown/assets/scripts/checks/adopt-pr-review-approved.sh) **[OFFICIAL]**
- [gascity-packs — build-basic-review/{target}.apply-review-findings.md](https://github.com/gastownhall/gascity-packs/tree/main/gascity/assets/workflows/build-basic-review) **[OFFICIAL]**
- [gascity-packs — README.md (interaction_mode / review_mode)](https://github.com/gastownhall/gascity-packs/blob/main/README.md) **[OFFICIAL]**
- [Gas City docs — Formula Spec v2 (§3.1 Check, §3.2 Retry, gate synthesis, Differences from v1)](https://docs.gascity.com/reference/specs/formula-spec-v2) **[OFFICIAL]** — fetched live 2026-08-21, matches in-repo copy
- [Gas City docs — Formula Spec v1 (§4 gate synthesis, gate type vocabulary limitation)](https://docs.gascity.com/reference/specs/formula-spec-v1) **[OFFICIAL]**
- [gascity — cmd/gc/cmd_converge.go](https://github.com/gastownhall/gascity/blob/main/cmd/gc/cmd_converge.go) **[OFFICIAL]**
- [gascity — internal/convergence/gate.go](https://github.com/gastownhall/gascity/blob/main/internal/convergence/gate.go) **[OFFICIAL]**
- [gascity — internal/convergence/metadata.go](https://github.com/gastownhall/gascity/blob/main/internal/convergence/metadata.go) **[OFFICIAL]**
- [gascity — internal/convergence/manual.go](https://github.com/gastownhall/gascity/blob/main/internal/convergence/manual.go) **[OFFICIAL]**
- [gascity — internal/convergence/hybrid.go](https://github.com/gastownhall/gascity/blob/main/internal/convergence/hybrid.go) **[OFFICIAL]**
- [gascity — internal/convergence/handler.go](https://github.com/gastownhall/gascity/blob/main/internal/convergence/handler.go) **[OFFICIAL]**
- [gascity — internal/convergence/formula.go (ValidateForConvergence)](https://github.com/gastownhall/gascity/blob/main/internal/convergence/formula.go) **[OFFICIAL]**
- [gascity — internal/convergence/condition.go (script env contract)](https://github.com/gastownhall/gascity/blob/main/internal/convergence/condition.go) **[OFFICIAL]**
- [gascity — internal/dispatch/ralph.go (v2 check env + trusted script roots)](https://github.com/gastownhall/gascity/blob/main/internal/dispatch/ralph.go) **[OFFICIAL]**
- [gascity — internal/formula/types.go (Gate, RalphSpec, RalphCheckSpec, GateRule)](https://github.com/gastownhall/gascity/blob/main/internal/formula/types.go) **[OFFICIAL]**
- `bd 1.0.4 (ce242a879)` local CLI — `bd gate --help`, `bd gate create --help`, `bd update --help`, and the live gate block/resolve and metadata round-trip transcripts in §3, §5, §7 **[EMPIRICAL]**
