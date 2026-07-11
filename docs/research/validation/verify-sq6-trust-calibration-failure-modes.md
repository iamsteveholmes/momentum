---
content_origin: adversarial-verification
sub_question: sq6-trust-calibration-failure-modes
date: 2026-05-31
---

# Adversarial Verification — Trust Calibration: Automation Bias vs Verification Fatigue

Posture: skeptical. Default to unsupported/unverifiable unless the cited source independently confirms.

## Summary judgment

The thread is unusually well-sourced for a fast-moving 2025–2026 topic. Most load-bearing
numeric claims re-fetch cleanly from their cited primary sources (METR, Sonar, Anthropic/InfoQ,
CodeRabbit, DORA 2025, "Adjust for Trust", Parasuraman & Manzey). Three real problems pull the
overall reliability down from "high" to "medium":

1. **A material recency reversal the thread omits.** METR published a follow-up (2026-02-24) in
   which the SAME developers showed an ~18% *speedup* (vs the original 19% slowdown). METR
   flags it as unreliable (selection bias) and is redesigning the study — but the thread leans
   on the 19%-slowdown headline as a settled tension-pole without disclosing that METR itself
   has walked it back / is re-examining it. This is the single biggest gap.
2. **A mis-attributed statistic.** The "38% say reviewing AI code is harder than human code"
   figure is sourced in the thread (finding #6) primarily to DORA. It is NOT on the dora.dev
   page. It is a Sonar survey figure (confirmed via IT Pro coverage). Real number, wrong source.
3. **One unverifiable internal citation.** Zietsman's "90.9% adoption lift (Wang et al.)" could
   not be found anywhere in the Zietsman paper I fetched. The Zietsman thesis itself (correlated
   errors, circular review) is confirmed; the specific 90.9% figure is the weakest single claim.

No claim was outright fabricated. The arXiv IDs that look suspicious (2502.13321, 2603.25773,
2604.03501, 2601.02410) are consistent with arXiv's YYMM convention for Jan/Mar/Apr 2026 and at
least 2502.13321 and 2603.25773 resolved to real papers with the claimed titles/authors.

## Per-claim verdicts

### 1. METR: experienced devs 19% slower, expected 24% / perceived 20% speedup — CONFIRMED but OUTDATED/qualified
- Re-fetch of https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ confirms
  every figure exactly: 19% slower, expected 24%, perceived 20%, 16 devs, 246 issues, repos
  ~22k stars / 1M+ LOC, Cursor Pro + Claude 3.5/3.7 Sonnet.
- HOWEVER: https://metr.org/blog/2026-02-24-uplift-update/ reports a follow-up where the same
  developers showed ~ -18% (i.e. 18% faster). METR flags severe selection bias (devs refuse to
  work without AI even at $50/hr; 30–50% avoided submitting high-AI-benefit tasks) and is
  redesigning the experiment. Net: the 19%-slowdown number is correctly quoted but is being
  actively re-litigated by its own authors. The thread treats it as a stable counterweight to
  DORA without this caveat. Mark the *claim as quoted* confirmed; the *use of it* is outdated.

### 2. Sonar verification gap (96% distrust / 48% verify / 42% AI code) — CONFIRMED
- Re-fetch of the Sonar press release confirms all three figures verbatim, 1,100+ devs, Jan 8 2026.

### 3. "61% agree AI produces code that looks correct but isn't reliable" — PARTIALLY-SUPPORTED
- Sonar's own press release says "53%" cite "code that looks correct but isn't reliable" as a
  negative impact. IT Pro coverage says "61%" agreed with a (differently-worded) statement.
  These are likely two different survey items. The 61% is supported by the IT Pro source the
  thread cites, but there is an unreconciled internal tension with Sonar's own 53%. Minor.

### 4. "Verification debt" attributed to AWS CTO Werner Vogels — CONFIRMED
- IT Pro confirms: Sonar's framing; term used by Vogels at re:Invent (December). Accurate.

### 5. Anthropic RCT — full delegation cuts comprehension ~17 pts (50% vs 67%; conceptual ≥65% vs delegators <40%) — CONFIRMED
- InfoQ re-fetch confirms: 52 junior engineers, Trio async library, AI group 50% vs manual 67%,
  conceptual ≥65% vs code-delegation <40%, speed gain ~2 min and NOT statistically significant.
  Clean confirmation. (Note: this is a learning/skill-formation study on juniors, not a code-
  review-bias study — the thread uses it appropriately for the skill-atrophy point.)

### 6. CodeRabbit — AI PRs ~1.7x more issues (10.83 vs 6.45), security up to 2.74x, logic +75% — CONFIRMED
- CodeRabbit blog re-fetch confirms 10.83 vs 6.45 (~1.7x), 2.74x security, +75% logic,
  readability >3x, error-handling ~2x. 470 PRs (320 AI-co-authored / 150 human). Published
  Dec 17 2025. IMPORTANT caveat (which the thread under-weights): CodeRabbit admits AI-authorship
  was *inferred from signals*, not confirmed, and cannot guarantee human-labeled PRs were
  human-only. Vendor sells AI review tooling. Directionally credible, magnitudes vendor-favorable.

### 7. Parasuraman & Manzey — operators of high-reliability automation ~50% less likely to detect failures; complacency under multi-task load, naive+expert, not fixed by practice — PARTIALLY-SUPPORTED
- The SagePub abstract confirms "multi-task load," "found in both naive and expert participants,"
  and "cannot be overcome with simple practice" verbatim. BUT the specific "50% less likely to
  detect failures" figure is NOT in the abstract — it is a body-of-paper summary of a specific
  reviewed study, frequently quoted secondhand. The mechanism claim is solid; the 50% number is
  loosely attributed (real but not in the abstract, and arguably a single-study result the review
  cites rather than the review's own headline). Foundational/2010 — correctly flagged as such.

### 8. "Adjust for Trust" (Srinivasan & Thomason) — 38% reduction in inappropriate reliance, 20% accuracy gain; forced pauses; doctors reject correct AI 68% vs 40% at low trust — CONFIRMED (doctor stat unverified-in-abstract)
- arXiv:2502.13321 confirms title, authors (Tejas Srinivasan, Jesse Thomason), and the
  "up to 38% reduction in inappropriate reliance and 20% improvement in decision accuracy" plus
  adaptive forced pauses verbatim from the abstract. The specific "doctors reject 68% vs 40%"
  detail is in the full body, not the abstract — unverified here but plausible and consistent.
  IUI '26 venue plausible. Strong source.

### 9. DORA 2025 — ~90% adoption, throughput UP (reversal), stability DOWN, AI-as-amplifier, 30% little/no trust — CONFIRMED
- Google Cloud DORA blog confirms all: 90% adoption, positive throughput relationship (explicit
  reversal from prior year), continued negative stability relationship, "AI amplifies what's
  already there," 30% little/no trust. Clean confirmation.

### 10. DORA — "38% say reviewing AI code is harder than human code" — CONTRADICTED (mis-sourced)
- The dora.dev/insights/balancing-ai-tensions page does NOT contain the 38% figure. It has the
  "babysitting the AI" and "reviewing another's code is harder than writing it" qualitative
  quotes only. The 38% figure actually comes from Sonar (confirmed via IT Pro). The thread's
  finding #6 attributes 38% to DORA. The number is real but the attribution is wrong.

### 11. Zietsman — spec-grounded review breaks circular loop; 90.9% adoption lift (Wang et al.) — PARTIALLY-SUPPORTED
- arXiv:2603.25773 confirms title ("The Specification as Quality Gate: Three Hypotheses on
  AI-Assisted Code Review"), author (Christo Zietsman), and the correlated-errors / shared-
  training-distribution / circular-review thesis (abstract quote confirms). BUT the "90.9%
  improvement in adoption attributed to Wang et al." could not be located anywhere in the paper.
  This specific number is the weakest claim in the thread — treat as unverified. (It is also a
  preprint/hypothesis paper, not an empirical result; the "three hypotheses" framing means even
  the core thesis is proposed, not demonstrated.)

### 12. CHI 2026 review — over-reliance is the dominant inappropriate-reliance mode — UNVERIFIABLE (paywalled), directionally supported
- dl.acm.org/doi/10.1145/3772318.3791467 returns HTTP 403 (bot block). Could not confirm the
  paper's existence or exact wording directly. Thread already marked confidence "medium." The
  broader literature (independent searches) confirms over-reliance is a heavily documented
  concern, while ALSO confirming under-reliance/algorithm-aversion is co-equal — which the thread
  acknowledges via its calibration framing. The "dominant" characterization is contestable (see
  contradicting evidence), not settled.

### 13. Caosun & Aral "Augmentation Trap" (arXiv 2604.03501) — UNVERIFIED (not independently fetched)
- Not re-fetched in this pass (lower load-bearing; an economic model, not empirical). arXiv ID
  format plausible for Apr 2026. The "rational adoption still erodes skill" claim is a theoretical
  model result, not evidence of real-world deskilling — should be read as a formal argument, not
  data. Thread marks it "medium." Leave as unverified-but-plausible.

## Training-data smell test

- The Zietsman "90.9% adoption lift (Wang et al.)" reads like a precise statistic detached from a
  locatable source — the classic shape of an over-specific, weakly-grounded figure. Not found in
  the cited paper. Highest smell.
- "Vibe-Check Protocol" (Aiersilan, arXiv 2601.02410) appears only in the raw file, not re-fetched;
  the name + framing reads plausibly but is the kind of niche preprint that warrants a direct check
  before being load-bearing. Low-to-moderate smell (not independently confirmed here).
- The Parasuraman "50% less likely to detect failures" is a real but secondhand-feeling summary
  number (not in the abstract) — mild smell of citation telephone, though the underlying paper is
  genuine and foundational.

## Contradicting / qualifying evidence found (2025–2026)

- **METR's own 2026-02-24 follow-up** found the same developers ~18% FASTER, directly tempering
  the 19%-slowdown headline; METR is redesigning the experiment due to selection bias. The thread
  presents the slowdown as a stable pole without this. (metr.org/blog/2026-02-24-uplift-update/)
- **The "modest gains" cluster** (Second Talent: "84% adoption, productivity gains only ~10%";
  philippdubach: "93% adoption, productivity hasn't moved") suggests the real-world net effect is
  small-positive, sitting between METR-slowdown and DORA-throughput — neither extreme dominates.
- **Over-reliance is NOT uncontested as "dominant."** Independent reliance literature (Computers
  in Human Behavior 2024; arXiv 2509.08010; CHI 2025 "To Rely or Not to Rely") treats over- and
  under-reliance (algorithm aversion) as co-equal failure modes, with a dynamic flip: users
  overtrust initially then over-distrust after a visible error. This supports the thread's
  *calibration* framing but undercuts any "over-reliance is THE dominant mode" claim.
- **Skill effect is conditional, not unidirectional.** Multiple 2026 sources (Uvik; Data Science
  Collective; the Anthropic study itself) confirm conceptual/engaged use preserves or builds skill
  while careless delegation erodes it — corroborating the thread's "how, not whether" nuance, and
  arguing against a simple deskilling narrative.

## Better-source notes

- For "38% reviewing AI is harder": cite Sonar / IT Pro
  (https://www.itpro.com/software/development/software-developers-not-checking-ai-generated-code-verification-debt),
  NOT dora.dev. The 38% is confirmed there.
- For the METR productivity tension: pair the original blog with the follow-up
  (https://metr.org/blog/2026-02-24-uplift-update/) so the reversal/redesign is visible.
- For over-reliance-as-failure-mode framing where the CHI '26 DOI is paywalled: the open-access
  arXiv:2509.08010 ("Measuring and mitigating overreliance...") and CHI 2025 doi 10.1145/3706598.3714097
  are fetchable substitutes.
