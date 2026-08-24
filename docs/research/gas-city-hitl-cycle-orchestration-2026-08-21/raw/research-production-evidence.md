---
content_origin: claude-code-subagent
date: 2026-08-21
sub_question: "Production evidence: who runs human-gated formulas in the wild; maintainer guidance on HITL today"
topic: "Gas City HITL gates and cycle orchestration for Momentum"
---

# Production Evidence: Human-Gated Formulas in the Wild

## Bottom line

**No publicly discoverable Gas City formula — first-party or third-party — uses `[steps.gate]`.** The v2 spec's own admission ("Zero bundled formulas use `gate`") understates the situation: an exhaustive grep of all 315 TOML files across the entire `gascity-packs` repository at commit `28e2e84` (2026-08-18) returns **zero** occurrences of `steps.gate`, and zero of `waits_for` **[EMPIRICAL]**. The hosted registry lists 17 packs, of which exactly one is third-party, and that one contains no formulas at all **[EMPIRICAL]**.

There is, however, a real and recently-*landed* human-gate path — landed on `main`, not shipped in a release, and not the formula one. Two orders in the bundled `core` pack (`notify-on-human-gate-creation`, `renudge-stale-human-gates`, both landed 2026-07-23) operate on **ad-hoc** gate beads created via `gc bd gate create --type=human`, mailing and re-nudging the addressee until resolution **[OFFICIAL]**. **[Availability caveat, DOMAIN2-E-001]:** neither order ships in a tagged release — both are `main`-only as of 2026-08-21, absent from v1.4.0 and v1.4.1, and reach production only via the `edge` rolling pre-release the maintainers label not-for-production (see `research-notification-watcher-layer.md`). This is the only production-*grade* HITL notification machinery Gas City has written, it is four weeks old and not yet in anyone's hands via a tagged release, and it was contributed by a community member rather than the core team.

Maintainer direction points *away* from HITL. Steve Yegge's August 2026 essay states plainly that "you can't work at agentic speeds and block everything with human reviews" **[OFFICIAL]**. And when Gas City's own leadership needed a hard human gate on their own release process after an agent shipped an unauthorized release, the remediation they reached for was a GitHub tag-protection ruleset — not their own product's gate primitive **[OFFICIAL]**.

---

## Method and evidence base

Findings below are grounded in four evidence classes, in descending order of strength:

1. **[EMPIRICAL]** — direct grep/API queries against cloned repositories at named commits. `gastownhall/gascity` at `151168c7` (2026-08-21), `gastownhall/gascity-packs` at `28e2e84e` (2026-08-18), `wespd/cacc-twin-team` at `644e108`.
2. **[OFFICIAL]** — source-code comments, bundled order definitions, the v2 formula spec, official blog posts, GitHub issues filed by contributors.
3. **[PRAC]** — practitioner blogs with URLs.
4. **[UNVERIFIED]** — inference, flagged as such.

GitHub's code-search API returned empty for `repo:gastownhall/gascity-packs "steps.gate"` — but code search is unreliable for freshly-pushed content, so all counts below come from local greps against cloned working trees, not from search **[EMPIRICAL]**.

**Per the research directive, GitHub stars are discarded entirely.** Maturity is assessed on commit volume, contributor distribution, release cadence, Homebrew install analytics, and release asset download counts.

---

## Finding 1 — Zero formulas in the wild use `[steps.gate]`

The formula spec is explicit about the feature's status:

> "`[steps.gate]` synthesizes a real gate bead that blocks its step until the gate bead is closed (manually or by an external watcher), but the `type` values `gh:run`, `gh:pr`, `timer`, `human`, and `mail` are doc-comment vocabulary in `internal/formula/types.go` — the parser never validates them and no bundled watcher acts on them. **Zero bundled formulas use `gate`.**"
> — [formula-spec-v2.md §4](https://github.com/gastownhall/gascity/blob/main/docs/reference/specs/formula-spec-v2.md) **[OFFICIAL]**

The spec says *bundled*. The stronger empirical claim is that nothing public uses it at all. Across `gascity-packs` (315 `.toml` files, 329 `[[steps]]` declarations), the complete census of step sub-tables actually used is **[EMPIRICAL]**:

| Step sub-table | Occurrences |
|---|---|
| `[steps.check]` | 57 |
| `[steps.drain]` | 25 |
| `[[steps.children]]` | 10 |
| `[steps.expand_vars]` | 1 |
| **`[steps.gate]`** | **0** |
| **`waits_for`** | **0** |

41 TOML files match the string `gate`, which initially looks like adoption. Inspecting every match shows the word is used exclusively in **prose** — agent-instruction text such as "BLOCKING gates step can early-exit", "Run BLOCKING gates — competing PR + architectural refactor", or `description = "Branch to gate (defaults to current branch)"` **[EMPIRICAL]**. The `contributing` and `pr-pipeline` packs both implement their "BLOCKING gates" as an ordinary `claude` step whose prompt tells the agent to close the root bead and exit:

```
gate: competing_pr
echo "[contributing-plan-implementation] BLOCKED — <gate>: <detail>"
gc bd close "$ROOT_ID" --reason "<gate> for issue #{{issue}}"
```
— `pr-pipeline/formulas/mol-pr-start.formula.toml` L108, `contributing/formulas/mol-contributing-plan-implementation.formula.toml` L88–91 **[EMPIRICAL]** (`packs/` prefix stripped during AVFL fix pass — MAJ-005: the prefix does not exist in `gascity-packs`' repo layout, pack directories sit at repo root; both citations 404 as originally written and 200 with the prefix removed — the underlying evidence is sound, only the paths were wrong)

That is an *agent-judgment* early exit, not a structural block awaiting a human. Nothing pauses; nothing waits for a person.

**The user-facing documentation reinforces this.** Grepping `docs/tutorials/`, `docs/guides/`, and `docs/getting-started/` for "gate" (excluding *delegate/mitigate/aggregate/gateway*) returns only three categories of hit: dependency gating ("gates each step on its dependencies"), LLM **gateways** (OpenAI-compatible proxies), and the `gate-sweep` housekeeping order **[EMPIRICAL]**. The phrase "human gate" appears **zero times** anywhere in `docs/` — its only occurrence in the repository is inside `engdocs/plans/feature-flags/DESIGN.md`, an internal design plan **[EMPIRICAL]**. No tutorial teaches a human gate. No guide shows one.

**Support-issue volume corroborates absence of users.** **[Corrected during AVFL fix pass — ACCURACY2-A-002; the corpus is 1,293 issues on a like-for-like count, not 1,729.]** Across a corpus of **1,293 issues** (575 open, issue-only search-API count, + 718 closed — see Finding 7's issue-backlog correction below), exactly **one** mentions `[steps.gate]`: [#4399](https://github.com/gastownhall/gascity/issues/4399), filed 2026-07-18 by contributor Jacob Hausler **[EMPIRICAL]**. **[Direction corrected during AVFL fix pass — ACCURACY3-A-002; the iter2 wording claimed the opposite.]** The smaller, corrected denominator marginally *softens* the ratio rather than strengthening it: one mention in 1,293 is a slightly **higher** incidence (≈0.077%) than one in 1,729 (≈0.058%). The conclusion is unaffected at either denominator — a single mention across 1,293 issues is scarcity by any reading — but the honest statement is "unchanged," not "stronger." Critically, it is a *spec-verification* issue, not a production-failure report — the author explicitly states he verified against "`bd gate check --help` / `bd gate create --help` and `docs/reference/specs/formula-spec-v2.md@main`", i.e. reading the docs, not hitting the bug in a running city **[OFFICIAL]**. A feature with real users generates real users' bug reports. This one has generated a documentation audit. It was auto-triaged `kind/feature · priority/p3` on 2026-07-19 and remains **open with no human maintainer response** as of 2026-08-21 **[EMPIRICAL]**.

The issue's own summary is the clearest maintainer-adjacent statement available:

> "A formula that synthesizes a typed gate therefore gets **structural blocking** (the gate bead blocks its step until closed) but **no automatic resolution** on the declared condition… `mail` appears in the spec's `[steps.gate]` `type` vocab but is **not** a real type in either `bd gate create --type` or `bd gate check --type` — documented but nonexistent everywhere."
> — [gascity#4399](https://github.com/gastownhall/gascity/issues/4399) **[OFFICIAL]**

---

## Finding 2 — The real human-gate path is ad-hoc gate beads plus two core orders — landed on `main` 2026-07-23, in no tagged release

There *is* working HITL machinery, and it sits one layer below formulas. `gc bd gate create --type=human` creates an ad-hoc gate bead; two orders in the bundled `core` pack then notify and chase the human **[OFFICIAL]**. **[Availability caveat, DOMAIN2-E-001 / STRUCTURAL3-A-002 — applies to everything in this finding]:** neither order ships in a tagged release. Both are `main`-only as of 2026-08-21, absent from v1.4.0 and v1.4.1, and reach production only via the `edge` rolling pre-release the maintainers label not-for-production (see `research-notification-watcher-layer.md`). The gate *bead* half is available on a released `gc`; the notify/renudge half is not. Read every "ships"/"shipped" below as "landed on `main`," not "available in a release."

Both landed in a single PR — [#4553](https://github.com/gastownhall/gascity/pull/4553), "feat(orders): notify the addressee on human-gate creation + re-nudge stale human gates", authored by **Chris Sauer** and committed 2026-07-23 **[EMPIRICAL]**. Sauer has 11 commits total to the repository; he is a contributor, not core staff **[EMPIRICAL]**.

The header comment on `notify-on-human-gate-creation.toml` is the single most informative maintainer statement on the state of HITL:

> "Without it, creating a `type=human` gate produces **ZERO notification** — the gate bead is built, the blocks edge is added, a line prints to stdout, and the human who must resolve it is never told (**proven ABSENT** in gascity/beads: gate creation has no post-create notify hook; the only gate watcher skips human gates entirely). **Doctrine compensates by hand** ('on the predecessor close, mail+nudge the addressee'); **this ships that reflex**."
> — [`internal/bootstrap/packs/core/orders/notify-on-human-gate-creation.toml`](https://github.com/gastownhall/gascity/blob/main/internal/bootstrap/packs/core/orders/notify-on-human-gate-creation.toml) **[OFFICIAL]**

Read plainly: creating a human gate in Gas City silently strands it — and on every tagged release, v1.4.0 and v1.4.1 included, it still does. The compensation was, and on a released `gc` remains, *human doctrine* — a habit maintainers perform by hand. The two orders that end the stranding landed on `main` four weeks ago and have not reached a tagged release since, so the stranding has not ended in any release a user can install. That is the opposite of production-hardened.

The companion order fills the other half:

> "It is the companion to notify-on-human-gate-creation: that order fires ONCE at creation; this one covers the gate that is created, notified, and then sits unresolved — **the human forgets, the creation mail scrolls off, and nothing tells them again.**"
> — [`renudge-stale-human-gates.toml`](https://github.com/gastownhall/gascity/blob/main/internal/bootstrap/packs/core/orders/renudge-stale-human-gates.toml) **[OFFICIAL]**

Mechanics worth recording for Momentum: the sweep runs every 5m, filters `gc bd gate list` to `await_type == "human"`, and re-notifies via `gc mail send --notify` at most once per `GC_STALE_GATE_RENUDGE_INTERVAL` (default 1h). Notably, `gc mail send --notify` "**deliberately skips the tmux-nudge for the 'human' recipient (humans have no session)**" — meaning the delivery channel to an actual person is mail-to-mailbox plus whatever external bridge (Slack/Discord) the city has installed **[OFFICIAL]**.

The maturity of this four-week-old machinery is visible in its first bug: [#4770](https://github.com/gastownhall/gascity/issues/4770) (filed 2026-07-28, fixed 2026-08-04) found that a mid-sweep process death lost the entire dedup ledger, causing every gate to be re-nudged seconds later against a configured 1-hour interval — reproduced 5/5 deterministically **[OFFICIAL]**. The fix landed within a week, which is a good sign about responsiveness and a bad sign about how lightly-exercised the path is.

The `gate-sweep` order — the auto-resolving watcher — sweeps only `--type=timer` and `--type=gh` **[EMPIRICAL]**. Human gates are, correctly by design, never machine-closed. The gap is that formula-synthesized gates do not reach *any* of this: not the sweeper, not the notifier.

---

## Finding 3 — Packs that advertise "human gates" implement them as prompt text, mail, or `interaction_mode`

The `gascity-packs` README markets three packs on approval semantics: `superpowers` ("You want **hard approval gates before code** and strict TDD per task"), `gstack` ("You want **founder/PM-flavored gates** and explicit QA + release-readiness stages"), and `pr-pipeline` ("pre-push gate") **[OFFICIAL]**. Every one of these is implemented without a gate step.

The mechanism is a template variable. `interaction_mode` appears in 25 pack TOML files, declared as `["interactive", "autonomous", "headless"]`, and it is substituted into the agent's prompt markdown **[EMPIRICAL]**. What that prompt then says is the whole of the enforcement:

> "Current interaction_mode is `{{interaction_mode}}`. In interactive mode, **use a human gate only for environment credentials, staging URLs, or destructive test choices.** In autonomous mode, test what is available and record what could not be reached."
> — `gstack/assets/workflows/gstack-build/qa.md` L11–14 **[EMPIRICAL]** (`packs/` prefix stripped during AVFL fix pass — MAJ-005)

> "Current interaction_mode is `{{interaction_mode}}`. **Interactive gates should be handled by the child lanes through mail or passive wait metadata**; autonomous runs should record assumptions instead of blocking on missing preferences."
> — `gstack/assets/workflows/gstack-build/plan-review.md` L8–10 **[EMPIRICAL]** (`packs/` prefix stripped during AVFL fix pass — MAJ-005)

"Through mail or passive wait metadata" is the closest any shipped pack comes to specifying a human-gate mechanism — and it is an instruction to an LLM, not a compiled graph edge. The README's own gloss confirms the softness: `interaction_mode` "**describes** human participation in planning and gates" **[OFFICIAL]**. Describes, not enforces.

**The `oversight-rig` pack is the sharpest datapoint.** It is the pack explicitly about human oversight, and it contains zero gates. Its model is escalation-outward, not blocking-inward: a `project-lead` agent writes a rollup bead labelled `severity:escalate`, a scheduled `escalate-rollups` order mechanically detects undelivered escalations and pushes them over Slack, and "**human replies route straight back to the bound project-lead**" **[OFFICIAL]**. The work never stops to wait. The human is notified alongside a running factory and may intervene — humans *on* the loop, not *in* it.

---

## Finding 4 — Maintainer direction is explicitly away from human gating

Steve Yegge founded the Gas Town → Gas City lineage but is not its engineer: he has **5 commits** to `gastownhall/gascity`, against 3,601 for lead maintainer `julianknutsen` **[EMPIRICAL]**. His writing is therefore directional rather than operational — but it is the loudest public signal about where HITL is headed.

From *The Shape of Things to Come, Part 1: The Continuous Thunderdome* (August 2026):

> "code review… will be [gone] by next year. **You can't work at agentic speeds and block everything with human reviews.**"

> "The rule is: **crons watch, models act.**"
> — [yegge.ai/essays/the-shape-of-things-to-come](https://yegge.ai/essays/the-shape-of-things-to-come/) **[OFFICIAL]**

The essay's framing of Beads is as a provenance ledger for *post-hoc* diagnosis — "the journal of all the work that ever happened: the provenance record of what was done, and why, in order" — explicitly serving "diagnosis and knowledge purposes, not approval authority" **[OFFICIAL]**. The stated architecture is parallel *agent* review plus incident-time forensics, replacing sequential human review.

Marketing copy runs the other way — gascity.com describes "judges at the gates, and humans running the factory instead of babysitting every session," and the Gas City guide promises "a human review gate" **[OFFICIAL]**. But the guide provides no implementation pattern, no approval-threshold guidance, and no worked example **[OFFICIAL]**. The gap between the marketing surface and the shipped primitives is the finding.

---

## Finding 5 — When Gas City's own leadership needed a hard human gate, they used GitHub, not Gas City

On 2026-08-20 Chris Sells published *Beads 1.2.1 Incident Report: Release the Bees!* — an autonomous agent maintainer ("Bee") cut and published a release without authorization **[OFFICIAL]**. This is the closest thing to a real-world HITL post-mortem in the corpus, and every remediation is instructive:

> "the go I acted on was **a one-line conditional approval, relayed through an agent**"

> "**a release process that lives only in a human conversation is invisible to an agent**"

> "**a GitHub tag-protection ruleset restricting `v*` tag creation to the maintainers team would make this mechanical**"

> "the real problem is that an autonomous agent was enabled to push to production… **Don't give your agents access to production.**"
> — [blog.gascity.com/posts/beads-1-2-1-incident-report](https://blog.gascity.com/posts/beads-1-2-1-incident-report/) **[OFFICIAL]**

Three things follow. First, the failure mode was exactly the one Momentum's anti-rubber-stamp plan gate exists to prevent: a blanket, low-information approval relayed through an agent. Second, the diagnosis — "a release process that lives only in a human conversation is invisible to an agent" — is a direct argument *for* materializing gates as inspectable state, which is what a gate bead would be. Third, and most damning for adoption: with that diagnosis in hand, the company chose **GitHub tag protection and agent sandboxing** as the enforcement mechanism. Their own `[steps.gate]` and `--type=human` primitives are not mentioned **[OFFICIAL]**.

---

## Finding 6 — The registry showcase: 17 packs, 16 first-party, 1 third-party with no formulas

The hosted registry at `registry.gascity.com/registry.toml` is the authoritative pack showcase. Full census as of 2026-08-21 **[EMPIRICAL]**:

- **17 packs total.** 16 tier `maintained`, publisher "Gas City". **1** tier `community`.
- The sole third-party pack is `cacc-twin-team`, published by `wespd`. Cloned at `644e108`, it contains **5 files**: a README, `pack.toml`, `packs.lock`, and a single mayor-agent prompt override. **No formulas. No orders. No gates** **[EMPIRICAL]**.
- `wespd` is also the author of Customer Zero issues #4519–#4526 — a dogfooding participant, not an arms-length adopter **[EMPIRICAL]**.

The "Customer Zero" program itself is worth noting as negative evidence. It is a structured dogfooding exercise producing ~45 numbered issues in July 2026 from `julianknutsen` and `wespd`, covering dashboards, supervisors, macOS packaging, pack imports, and registry plumbing **[EMPIRICAL]**. **Not one Customer Zero issue concerns gates or human approval.** The most rigorous internal usability sweep Gas City has run never touched the HITL surface — consistent with nobody exercising it.

GitHub Discussions is effectively dead: 4 discussions total, 0 comments on each, most recent 2026-07-19 **[EMPIRICAL]**. Community conversation happens on Discord (`discord.gg/xHpUGUzZp2`), which is not publicly archived and could not be searched; **this is the principal gap in this research** **[UNVERIFIED]**.

---

## Finding 7 — Maturity assessment (stars and other gameable metrics discarded)

**Age and cadence.** `gastownhall/gascity` created 2026-02-22 — six months old **[EMPIRICAL]**. Releases: v1.0.0 (2026-04-21) → v1.4.1 (2026-08-15), roughly monthly minors with patch releases between **[EMPIRICAL]**. Now in `homebrew/core`, not merely a third-party tap — a genuine packaging-maturity signal **[EMPIRICAL]**.

**Commit velocity.** Weekly commits over the last 12 weeks: `307, 189, 286, 99, 85, 106, 236, 251, 123, 148, 88, 93` — mean ≈168/wk, decelerating from a spring peak but unambiguously active **[EMPIRICAL]**. 2,956 PRs merged all-time; **488 merged in the last 30 days** (~16/day) **[EMPIRICAL]**.

**Contributor distribution — the concerning metric.** 165 contributors, 5,437 commits **[EMPIRICAL]**:

| Concentration | Share of commits |
|---|---|
| Top 1 (`julianknutsen`) | **66.2%** |
| Top 3 | 79.9% |
| Top 10 | 86.4% |
| Contributors with ≥10 commits | 33 |
| Contributors with exactly 1 commit | 67 |

Two-thirds of the codebase is one person. The long tail is drive-by. `gascity-packs` is worse: `julianknutsen` 182, `sjarmak` 62, then a cliff to single-commit contributors **[EMPIRICAL]**. Bus factor is effectively 1–2.

**Issue backlog.** **[Corrected during AVFL fix pass — ACCURACY2-A-002, superseding the MAJ-004 annotation below.]** On a like-for-like, issue-only count: **575 open vs 718 closed** — closed exceeds open by 143 **[EMPIRICAL]**. "Intake outpaces resolution" does not hold on this count and is struck. **(Query-method history:** the earlier "1,011 open vs 718 closed" figure mixed populations — 1,011 is the `repos/…/open_issues_count` repo-endpoint count, which bundles open PRs together with open issues, while 575 is the search-API `is:issue is:open` count, which excludes PRs. The open-PR remainder is therefore **≈436** by subtraction (1,011 − 575) **[derived]** — the "roughly 760" figure carried here at iter2 was an unsourced import and is arithmetically impossible; corrected during AVFL fix pass, ACCURACY3-A-003 / STRUCTURAL3-A-003. **Query method for 718:** the same search-API basis applied to closed issues — `is:issue is:closed`, all-time, PRs excluded — which is what makes 575-vs-718 like-for-like and 575 + 718 = 1,293 the issue-only corpus total. The raw query string was not recorded when the 718 count was taken; the method is stated here as the one the file's own like-for-like arithmetic requires, not as a re-run. `research-maturity-open-bugs.md` reports the same corrected 575 figure. This file's own census in Finding 1 above has been updated to the like-for-like 1,293-issue total.)

**Adoption (Homebrew installs, the least gameable number available)** **[EMPIRICAL]**:

| Window | `gascity` | `beads` |
|---|---|---|
| 30 days | 669 | 3,719 |
| 90 days | 962 | 7,695 |
| 365 days | 1,022 | 22,632 |

GitHub release-asset downloads corroborate the scale: gascity peaks around 1,800 per release (v1.4.0), ~9,500 across all v1.x **[EMPIRICAL]**. Beads by contrast: 175,961 downloads on v1.1.0 alone, 1,783 forks vs gascity's 371 **[EMPIRICAL]** — **(fork counts flagged during AVFL fix pass — LOW-002)** forks are a gameable metric, absent from this section's own stated methodology ("Per the research directive, GitHub stars are discarded entirely… Maturity is assessed on commit volume, contributor distribution, release cadence, Homebrew install analytics, and release asset download counts"), and are cited here only as secondary corroboration alongside downloads and contributor distribution — the directional read (beads more adopted than gascity) does not depend on the fork figures and holds without them.

**The asymmetry matters for DEC-028.** Beads is roughly 5–20× more adopted than Gas City on every non-gameable metric. Momentum already depends on beads. Adopting Gas City means layering a ~700-installs-per-month orchestrator on top of a ~3,700-installs-per-month tracker, and inheriting the orchestrator's bus factor. The dependency is one-directional: beads does not need Gas City.

**Reframed during AVFL fix pass — DOMAIN-A-012.** Roughly 700 monthly macOS installs is a **floor**, not a ceiling, on the population of possible human-gate users — this corpus itself documents at least three uncounted adoption channels the Homebrew figure misses: (1) the `mise`/GitHub-backend install path, which `research-gate-mechanics-handson.md`'s own hands-on researcher used ("No brew, no ubi fallback … the mise github backend is the clean install path for this machine"); (2) source builds from HEAD, which `research-cycle-orchestration-fit.md` §3 quotes the project's own docs recommending ("Best practice right now is to build your own `gc` binary from HEAD"); and (3) Linux, which Homebrew analytics exclude entirely. The release-asset download counts in this same section (~1,800/release, ~9,500 across v1.x) are a second, already-uncounted channel layered on top of the Homebrew figure. The *directional* conclusion survives fully — small user base, zero publicly discoverable gated formula — but "the ceiling" should read "a floor with named uncounted channels above it," and the numeric bound (700/month) should not be quoted as a hard population cap.

---

## What this means for Momentum's four HITL points

**[UNVERIFIED — analysis, not sourced]** Mapping the evidence to Momentum's gates:

1. **Triage batch approval** — closest fit to the `--type=human` gate bead plus the `notify-on-human-gate-creation` path. Split the two halves: the gate bead is available on a released `gc` today; the notify order is `main`/`edge` only and in no tagged release (Finding 2), so the notification half is something Momentum vendors or builds. Batch semantics (approve N observations at once) have no precedent in any pack; Momentum would author it.
2. **Pre-sprint plan gate (anti-rubber-stamp, per-fork written verdicts)** — no precedent anywhere. The one real-world approval failure in the corpus (the Beads 1.2.1 incident) was *caused by* a one-line blanket approval, which is precisely what Momentum's gate forbids. Gas City ships no mechanism for capturing structured per-fork verdicts; `gc converge approve` is a single-bit approve/iterate/reject on a convergence loop.
3. **Mid-story tooling gates (developer manually exercises nornspun/chorgi)** — closest analogue is the gstack QA prompt: "use a human gate only for environment credentials, staging URLs, or destructive test choices." That is prompt text, unenforced. A structural block would require `[steps.gate]`, which has no watcher and no notifier.
4. **Post-sprint results gate** — the `oversight-rig` escalate-to-Slack-with-reply-routing pattern is the maintained, exercised path, but it notifies alongside a *running* factory rather than blocking a merge.

The blunt reading: **Momentum would be the first public user of `[steps.gate]`, and would be building the notification and verdict-capture layers itself.** The nearest thing to a supported path — ad-hoc `--type=human` gate beads plus the two core orders — is four weeks old, community-contributed, has already shipped one durability bug, and is **not in any tagged release**: the gate-bead half works on a released `gc`, the notify/renudge half exists only on `main`/`edge` (Finding 2). "Actual production support" is not an accurate description of it in any release a user can install today.

---

## Confidence and gaps

**High confidence:** zero public `[steps.gate]` usage; the two core human-gate orders and their July 2026 provenance; registry composition; all maturity metrics. These are direct greps and API reads against named commits.

**Medium confidence:** the maintainer-direction reading. Yegge's essay is unambiguous but he is a 5-commit contributor; the shipping team's revealed preference (contributing the notify orders at all) is mildly pro-HITL. Marketing copy and engineering reality diverge.

**Gaps:**
- **Discord is unsearchable.** `discord.gg/xHpUGUzZp2` is the primary community channel and is not publicly archived. If a production human-gate user exists, that is the likeliest place to find them. Recommend the developer ask directly in Discord before treating "zero users" as settled.
- **Private cities are invisible.** Gas City is an SDK for building private factories; enterprise users would not publish packs. Absence of public evidence bounds *discoverable* usage only.
- No Hacker News or X thread specifically discussing Gas City human gates surfaced in search.

---

## Sources

- [Gas City Docs — Overview](https://docs.gascity.com/) **[OFFICIAL]**
- [formula-spec-v2.md](https://github.com/gastownhall/gascity/blob/main/docs/reference/specs/formula-spec-v2.md) — §4, "Zero bundled formulas use `gate`" **[OFFICIAL]**
- [gascity#4399 — `[steps.gate]` type vocabulary parsed-but-not-enforced](https://github.com/gastownhall/gascity/issues/4399) (2026-07-18, open) **[OFFICIAL]**
- [gascity#4770 — renudge-stale-human-gates loses dedup ledger](https://github.com/gastownhall/gascity/issues/4770) (2026-07-28 → 2026-08-04) **[OFFICIAL]**
- [gascity#4553 — notify + re-nudge human gates](https://github.com/gastownhall/gascity/pull/4553) (2026-07-23, Chris Sauer) **[OFFICIAL]**
- [`core/orders/notify-on-human-gate-creation.toml`](https://github.com/gastownhall/gascity/blob/main/internal/bootstrap/packs/core/orders/notify-on-human-gate-creation.toml) **[OFFICIAL]**
- [`core/orders/renudge-stale-human-gates.toml`](https://github.com/gastownhall/gascity/blob/main/internal/bootstrap/packs/core/orders/renudge-stale-human-gates.toml) **[OFFICIAL]**
- [`core/orders/gate-sweep.toml`](https://github.com/gastownhall/gascity/blob/main/internal/bootstrap/packs/core/orders/gate-sweep.toml) **[OFFICIAL]**
- [gastownhall/gascity-packs README](https://github.com/gastownhall/gascity-packs) — pack table, `interaction_mode` / `review_mode` **[OFFICIAL]**
- [oversight-rig pack README](https://github.com/gastownhall/gascity-packs/tree/main/oversight-rig) **[OFFICIAL]**
- [registry.gascity.com/registry.toml](https://registry.gascity.com/registry.toml) — 17 packs, 1 community tier **[OFFICIAL]**
- [wespd/cacc-twin-team](https://github.com/wespd/cacc-twin-team) — sole third-party registry pack **[EMPIRICAL]**
- [Beads 1.2.1 Incident Report: Release the Bees! — Chris Sells, 2026-08-20](https://blog.gascity.com/posts/beads-1-2-1-incident-report/) **[OFFICIAL]**
- [The City Wire (Gas City blog index)](https://blog.gascity.com/) **[OFFICIAL]**
- [The Shape of Things to Come, Part 1: The Continuous Thunderdome — Steve Yegge, Aug 2026](https://yegge.ai/essays/the-shape-of-things-to-come/) **[OFFICIAL]**
- [Welcome to Gas City — Steve Yegge, 2026-04-24](https://steve-yegge.medium.com/welcome-to-gas-city-57f564bb3607) **[OFFICIAL]**
- [gascity.com/guide](https://gascity.com/guide/) — "a human review gate" **[OFFICIAL]**
- [Gas City vs. Cosim — James Tanner, 2026-05-08](https://tannerjc.net/blog/gas-city-vs-cosim/) **[PRAC]**
- [Announcing Gas City 1.0 — Chris Sells](https://sellsbrothers.com/announcing-gas-city-1-0) **[PRAC]**
- [Homebrew formula analytics — gascity](https://formulae.brew.sh/api/formula/gascity.json) **[OFFICIAL]**
- [Homebrew formula analytics — beads](https://formulae.brew.sh/api/formula/beads.json) **[OFFICIAL]**
- GitHub REST API: `repos/gastownhall/gascity` contributors, releases, stats/participation; `orgs/gastownhall/repos` **[EMPIRICAL]**
- Local clones: `gastownhall/gascity@151168c7` (2026-08-21), `gastownhall/gascity-packs@28e2e84e` (2026-08-18), `wespd/cacc-twin-team@644e108` **[EMPIRICAL]**
