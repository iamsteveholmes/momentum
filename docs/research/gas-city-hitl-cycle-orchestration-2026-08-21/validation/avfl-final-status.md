# AVFL Final Status — Gas City HITL / Cycle Orchestration Corpus

**Corpus:** `docs/research/gas-city-hitl-cycle-orchestration-2026-08-21/`
**Closed:** 2026-08-24
**Exit condition:** **developer-directed close after iteration 4 fixes.** MAX_ITERATIONS policy — no fifth validation round runs. The iteration-4 fixes ship to synthesis unvalidated by a further adversarial pass.

---

## Closure record

Four full Adversarial Validate-Fix Loop iterations were run against a 12-file corpus (10 research files, a Gemini deep-research output, and `scope.md`). Each iteration ran 8 agents — an Enumerator and an Adversary across four lenses (Structural Integrity, Factual Accuracy, Coherence & Craft, Domain Expertise) — followed by a consolidation pass and a fix pass.

| Iteration | Score | Findings fixed | Fix log |
|---|---|---|---|
| 1 | **−18** / 100 | 29 | `fix-log-iter1.md` |
| 2 | **−43** / 100 | 27 propagation-sweep fixes, 44 edits across 12 files | `fix-log-iter2.md` |
| 3 | **−38** / 100 | 24 enumerated findings | `fix-log-iter3.md` |
| 4 | residual list below | 11 items (10 fixed, 1 disproved) | `fix-log-iter4.md` |

**On the score trajectory.** The scores do not descend monotonically, and that is expected rather than alarming: each iteration's adversaries were pointed at a *corrected* corpus and probed deeper seams than the last. The iteration-2 dip to −43 reflects a broader net (14 majors, most of them propagation defects that iteration 1's fixes created or exposed), not a corpus that got worse. Iteration 4's yield — 4 majors, of which one proved to be a false positive — is the first pass to return a residual list small enough to enumerate exhaustively, which is the practical convergence signal.

**Iteration 4's residual, scored on the iteration-2 formula** (100 base; −8 major, −3 minor, −1 low): 3 genuine majors + 4 minors + 3 lows = **−39 penalty → 61 / 100**. Counting the disproved M1 as a major would give **53 / 100**. Both numbers are stated because no fifth round adjudicates the disqualification; the evidence for it is in `fix-log-iter4.md` §M1 and is mechanically checkable.

**One finding was rejected rather than fixed.** `ACCURACY4-A-001` alleged a fabricated quotation at `research-cycle-orchestration-fit.md`:219. The quoted text was verified present verbatim, as one continuous sentence, at the cited location (`research-human-verdict-patterns.md`:281, inside §7). The citation was correct and was preserved; the disproof is recorded inline in the corpus so the point cannot be re-litigated downstream. Applying the directed remedy would have degraded an accurate citation. This is worth carrying forward as a practice note: **iteration-4 adversaries produced a confident false positive on a negative claim**, which is the failure mode that most resembles a real finding.

---

## Residual OPEN items the corpus honestly carries

These are **not defects**. They are questions the research could not close, each marked open at its site. Any synthesis or decision document built on this corpus must treat them as open, and must not silently resolve them.

1. **bd v1.2.2 CAS settling command was never run.** Whether beads v1.2.2 (2026-08-15) carries the `--if-assignee`/`--if-status` compare-and-swap precondition flags is **[UNVERIFIED]**. The corpus scopes every CAS claim to v1.0.4 and the v1.1.x line. The upstream `deps.env` comment generalizes to "no published release," but rests on a "newest published = v1.1.2" premise that v1.2.2 breaks — and on that comment's own logic, a release postdating `beads#5008` would be expected to carry the flags. **Decision-bearing: it feeds the DEC-028 D1 re-score.** One command against a v1.2.2 binary settles it.
   *Sites:* `research-beads-coupling-dec028.md`:178, `research-verification-probes.md`:284/:286.

2. **FileStore write-path question is moot, not answered.** Probe 2 settled that FileStore metadata *is* durable, then relocated the risk: there is no public CLI verb to write arbitrary metadata on a file-backed city in gc 1.4.1 (`gc bd` is blocked wholesale), so durability never becomes load-bearing for Momentum's gate use case. The original durability worry is retired; the write-path absence is the finding.
   *Site:* `research-beads-coupling-dec028.md`:70.

3. **Failed-close semantics of a drain+check barrier (§9c).** No file in the corpus states what happens when a `drain` + `check` barrier exhausts `max_attempts` before every fanned-out child has completed. Because `bd ready`/`bd blocked` key on open/closed status and were not demonstrated to distinguish `closed: done` from `closed: failed`, an exhausted barrier may release its downstream results gate exactly as a genuine completion would — asking a human to review a report for stories still mid-flight. No probe exercised this. The prescribed guard (a completion-assertion bead asserting "N of N children closed done") is **pending verification**, not proven.
   *Site:* `research-cycle-orchestration-fit.md` §9c.

4. **Multi-hour session behavior — open questions 1 and 2.** Whether a Claude Code session survives a multi-hour step without `idle_timeout` firing, and whether `gc session wait --sleep` actually parks a session such that an attach/nudge resumes the same conversation. The 2026-08-24 probe session installed `gc` 1.4.1 and exercised it live, but ran no multi-hour step and never exercised `idle_timeout` / `claim_holder_stall_timeout`. Only the "gc is not installed at all" framing is stale; the questions themselves remain genuinely open.
   *Site:* `research-cycle-orchestration-fit.md` §10 Q1–Q2.

5. **Notify-orders-vs-typed-gate behavior is inferred, not run.** That the two core orders (`notify-on-human-gate-creation`, `renudge-stale-human-gates`) would fire on a properly-typed ad-hoc `--type=human` gate is inferred from reading their `await_type == "human"` filter against the observed `await_type` persistence, not from an observed run — the orders are `main`/`edge` only and were never executed here. Related and also unexercised: whether `--payload-match bead.issue_type=gate` actually selects gate beads, which the watcher design would be built on.
   *Sites:* `research-gate-mechanics-handson.md` "The notification gap"; `research-notification-watcher-layer.md` "Confidence and limitations".

6. **Every cost total is a floor, not an estimate.** Both headline numbers are order-of-magnitude sizings with scope limits that must travel with them:
   - The **15–25 day** orchestration-rewrite figure is a rough sizing from analogous pack scope, taken against the corpus's *four* originally-enumerated HITL gates — not the **five** that §9b identifies once push/merge authority is counted.
   - The **glue estimate** sums to **5.5–9 days** from its components (rounded to 6–9 at the citation sites, all hedged), is **for one gate type only**, and **excludes the uncosted standup of a live Momentum city**. Within it, only the ~2.5–4d shared-infrastructure share amortizes across gates; the ~3–5d verdict-capture share recurs per gate.
   Neither figure is bottom-up. Treat both as floors for a go/no-go, never as committed numbers.
   *Sites:* `research-cycle-orchestration-fit.md`:181/:191; `research-notification-watcher-layer.md`:172; `research-dec035-revisit-triggers.md`:49.

7. **Push/merge authority has no named gate (§9b).** Momentum's own rules require explicit human confirmation before `git push` and mandate a version bump plus push at sprint completion. An unattended out-of-session cycle collides with both, and the corpus never checked its four HITL gates against them until the fix passes. Either a fifth gate on the merge/push step, or an explicit statement that an out-of-session run terminates merged-but-unpushed, must be chosen — the corpus deliberately does not choose.
   *Site:* `research-cycle-orchestration-fit.md` §9b.

---

## The standing prerequisite behind every gate recommendation

Not an open question — a settled condition that is easy to drop when citing this corpus, so it is restated here. Every "adopt `bd gate --type=human` today, free" recommendation is true of the **primitive** and not yet of the **effect**: a `bd` gate gates only work dispatched through `bd ready`, and Momentum's Conductor computes its frontier from `.momentum/stories/index.json` + `depends_on` under the DEC-028 dual-write spike. An open gate bead would block nothing the Conductor schedules. Making these gates load-bearing requires moving dispatch onto `bd ready` — **DEC-028's still-open go/no-go** — or adopting Gas City in full, under which the condition holds by construction.

*Stated at:* `research-human-verdict-patterns.md` §5 and §8; `research-hitl-alternative-patterns.md` §7 preamble.

---

## Artifacts

| Artifact | Path |
|---|---|
| Per-lens findings | `validation/findings/` (iter1), `findings-iter2/`, `findings-iter3/`, `findings-iter4/` |
| Consolidated findings | `validation/avfl-consolidated.md`, `-iter2.md`, `-iter3.md` |
| Fix logs | `validation/fix-log-iter1.md` … `fix-log-iter4.md` |
| Annotation conventions (evidence tags, correction markers, finding-ID grammar) | `scope.md` |

**Note on iteration 4:** no consolidated report was produced. The deduped item list lives in `fix-log-iter4.md`, which records all 11 items with before/after text for the two majors that changed prose meaningfully (M1's disproof, M2's primitive inversion).
