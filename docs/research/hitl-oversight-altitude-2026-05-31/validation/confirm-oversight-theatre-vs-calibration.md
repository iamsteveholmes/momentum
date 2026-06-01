---
content_origin: independent-confirmation
target: oversight-theatre-vs-calibration
date: 2026-05-31
analyst_role: independent-confirmation-skeptic
---

# Independent Confirmation: Calibrated Oversight vs. "Oversight Theatre"

Target area: The same telemetry (rising auto-approval AND rising interrupts) is read as
healthy calibration by some and as nominal-only "oversight theatre" by others. This note
adjudicates three claims against 2025-2026 PRIMARY sources, and assesses whether anyone has a
validated measure that distinguishes the two readings.

Bottom line up front: All three claims survive scrutiny, but with sharp scoping corrections.
The strongest piece (the MIT Tech Review "illusion" article) is about AI *warfare*, not code or
generic decision review — a misattribution risk if cited as evidence about software oversight.
The empirical automation-bias / rubber-stamping literature is real and robust but lives in
clinical/pathology and HCI domains, not (yet) in agentic-coding telemetry. Most important for
this target: the academic measurement literature explicitly concludes that NO single validated
metric distinguishes calibrated reliance from nominal/over-reliance — the constructs are
"fragmented." So a key claim that the original report needs is the *negative* one, and it holds.

---

## Claim 1 — MIT Technology Review published a 2026 piece arguing human-in-the-loop can be illusory / theatre

Verdict: CONFIRMED (with a scope correction — domain is AI warfare, not code/decision review).

Primary source: Uri Maoz, "Why having 'humans in the loop' in an AI war is an illusion," MIT
Technology Review, April 16, 2026.
https://www.technologyreview.com/2026/04/16/1136029/humans-in-the-loop-ai-war-illusion/

Verbatim passages confirmed on the page:
- "human oversight over AI may be more illusion than safeguard."
- "Keeping a human in the loop may not provide the safeguard people imagine, because the human
  cannot know the AI's intention before it acts."
- "the human overseers have no idea what the machines are actually 'thinking.'"

Mechanism: the article describes an "intention gap" — operators approve based on a surface metric
(e.g., a 92% success rate) while the system has computed hidden factors (collateral damage) the
human never sees. This is precisely the structural shape of "oversight theatre": nominal approval
over an opaque process.

Skeptic's caveat: This is an opinion/commentary piece by a neuroscientist about autonomous
weapons / battlefield targeting — NOT empirical evidence about AI code or developer-decision
review. Citing it as support for "code-review oversight is theatre" is a domain transplant. It
supports the *concept* of illusory HITL strongly; it is not evidence for the software-engineering
instance of it. A related MIT Tech Review piece ("Moltbook was peak AI theater," Feb 6, 2026)
uses "AI theater" language in a different (product hype) sense and should not be conflated.

---

## Claim 2 — Empirical 2025-2026 work measuring automation bias / rubber-stamping in AI code or decision review

Verdict: PARTIALLY-CONFIRMED. Strong, real empirical work exists on automation bias / over-reliance
and on AI code-review reliance — but the rubber-stamping *measurements* are in clinical/pathology
and HCI domains. The cleanest 2026 code-review primary source is a hypotheses/position paper with
only "directional" experiments, not a controlled rubber-stamping study.

Confirmed primary sources:

1. Rosbach, Ammeling, Ganz, Bertram, Conrad, Riener, Aubreville — "Stuck on Suggestions:
   Automation Bias, the Anchoring Effect, and the Factors That Shape Them in Computational
   Pathology," arXiv:2603.11821 (submitted March 12, 2026; accepted to MELBA). Empirical: n=28
   pathology experts, AI-assisted vs. independent. Measured a ~7% automation-bias rate (correct
   independent judgments overturned by incorrect AI advice); time pressure intensified bias
   severity; higher confidence under AI assistance correlated with more reliance.
   This is genuine 2026 empirical measurement of rubber-stamping behavior — but in pathology.

2. Kücking et al. — "Automation Bias in AI-Decision Support: Results from an Empirical Study,"
   Studies in Health Technology and Informatics, Aug 2024 (PubMed 39234734). Empirical: n=210,
   wound-care diagnosis. Measured "agreement rate with wrong AI-enabled recommendations";
   non-specialists most susceptible. Real and on-point for automation bias, but 2024 and clinical.

3. Zietsman — "The Specification as Quality Gate: Three Hypotheses on AI-Assisted Code Review,"
   arXiv:2603.25773 (March 26, 2026). VERIFIED REAL (I worried the future-looking ID was a
   confabulation; the abstract page resolves). This is the most directly relevant code-review
   source: argues deploying AI reviewers is "structurally circular when executable specifications
   are absent... The review checks code against itself, not against intent." This is an
   articulation of code-review "oversight theatre." IMPORTANT: it is a position/hypotheses paper
   with three "contrived experiments" on a planted-bug corpus; the author concedes these are
   "directional evidence, not a controlled demonstration." So: real and highly relevant
   conceptually, but NOT strong empirical proof of rubber-stamping in code review.

4. Microsoft Research — two real first-party syntheses on over-reliance:
   - "Overreliance on AI: Literature review" (Aether, 2022) — the ~60-paper synthesis.
   - Passi, Dhanorkar, Vorvoreanu — "Appropriate reliance on Generative AI: Research synthesis"
     (March 2024). Defines appropriate reliance as "when users accept correct AI outputs and
     reject incorrect ones." These are the canonical conceptual anchors but pre-2025 and
     non-coding.

5. BairesDev Dev Barometer Q4 2025 (Oct 2025; n=501 developers, 19 PMs, 92 projects). ~9% trust
   AI code enough to use without human oversight; 56% call it "somewhat reliable." Real survey,
   but this is *perception/attitude* data, not a behavioral measure of rubber-stamping.

Confabulation / staleness flags caught during verification:
- The search-summary layer fabricated several confident statistics that I could NOT trace to a
  primary source and which should be treated as likely-confabulated unless independently verified:
  a "90.9% relative improvement in adoption from specification-grounded review," a "30.7% negative
  reactions across 229 review comments / 179 GitHub projects," and a clean "26% higher rate" of
  following erroneous automated advice attributed to Goddard 2012. Do not propagate these without
  the underlying paper in hand.
- "Automatic Bias Detection in Source Code Review" (arXiv:2504.18449, Berhanu Alebachew & Brown,
  April 2025) is REAL but is a FALSE FRIEND: it detects *human reviewers' prejudicial bias* via
  eye-tracking — NOT automation bias / rubber-stamping of AI. Do not cite it for claim 2.

---

## Claim 3 — A validated metric distinguishing genuine calibrated oversight from nominal-only review (exists or not)

Verdict: REFUTED as stated (no single validated metric exists) / CONFIRMED in the negative.
The honest answer the target needs: there is an active *measurement literature* with multiple
proxy constructs, but it explicitly reports that the field is fragmented and lacks a validated,
consensus discriminator. No one has a single validated "calibration vs. theatre" metric.

Primary sources:

1. Ibrahim, Collins, Kim, Reuel, Lamparth, Feng, Ahmad, et al. — "Measuring and mitigating
   overreliance to build human-compatible AI," arXiv:2509.08010 (Sept 8, 2025; v2 May 20, 2026).
   The paper's framing is that measurement is inadequate: it "identif[ies] three important gaps
   and propose[s] three promising directions to improve measurement." I.e., it argues a better
   measure is *needed*, which is the opposite of claiming a validated one exists.

2. Raees & Papangelis — "From Trust to Appropriate Reliance: Measurement Constructs in Human-AI
   Decision-Making," arXiv:2604.23896 (April 26, 2026). VERIFIED REAL. Explicitly: "constructs
   for human-AI appropriate reliance are still fragmented in research." Catalogs three competing
   perspectives (Traditional, Appropriateness, Dominance) and *argues for consensus* on objective
   metrics — confirming none yet commands consensus. Also: "trust measurements do not inform
   users' appropriate reliance," so trust scales are not the discriminator either.

3. The available proxy measures (from the appropriate-reliance literature) are real but partial:
   reliance on desirable vs. undesirable AI outputs measured separately; their sum; their ratio;
   a two-dimensional treatment; or outcome-oriented "is human+AI better than human alone." None
   is validated as the canonical calibration-vs-theatre discriminator, and each can be gamed.

4. Industry/observability angle (the agentic-coding telemetry framing in the target): observability
   playbooks (e.g., Arthur "Agentic AI Observability Playbook 2026"; the 2026 Agentic Coding Trends
   material) recommend *recording* guardrail decisions, overrides, and approvals — but they treat
   these as raw telemetry to log, NOT as a validated metric that separates genuine calibration from
   nominal review. I found no primary source proposing or validating a metric keyed to the specific
   "rising auto-approval AND rising interrupts" signature described in the target. Practitioner
   commentary (Microsoft's ~60-paper overreliance synthesis; "rubber stamp problem" essays)
   suggests directional proxies — override-improves-outcome rate, time-to-intervene vs. harm
   window, whether explanations are even opened, escalations dying in a queue — but these are
   proposed practices, not validated instruments.

Conclusion for Claim 3: The strongest, most defensible statement is the *absence* claim. As of
mid-2026 there is no validated metric that cleanly distinguishes calibrated oversight from
oversight theatre; the literature is fragmented and actively calling for one. The rising
auto-approval + rising interrupts telemetry is genuinely *ambiguous* on current evidence — which
is exactly why both readings persist.

---

## Cross-cutting note on the two readings

- "Healthy calibration" reading: appropriate reliance = accept-correct + reject-incorrect (MS
  Research). Rising auto-approval on routine items + rising interrupts on hard/novel items would,
  under this lens, look like reliance tracking AI reliability. But nothing in the verified sources
  validates auto-approval+interrupt *rates* as evidence of this.
- "Oversight theatre" reading: Maoz's "intention gap" and Zietsman's "review checks code against
  itself" both describe nominal approval over opaque process. The pathology study (2603.11821)
  gives the only hard behavioral number close to the question — ~7% of correct human judgments
  overturned by wrong AI advice, worse under time pressure — evidence that interrupts/approvals do
  NOT guarantee genuine scrutiny.
- The discriminator gap is real: to tell the readings apart you need outcome-conditioned override
  quality (do interrupts catch real defects? do approvals pass real defects?), and the verified
  literature says that instrument is not yet validated or standardized.

## Newer / missed evidence the original report may have lacked
- arXiv:2604.23896 (April 2026) is the most current explicit statement that reliance measurement
  constructs are still fragmented — directly load-bearing for Claim 3.
- arXiv:2603.11821 (March 2026, MELBA) provides a current, quantified automation-bias rate under
  time pressure — the freshest hard number for Claim 2.
- arXiv:2509.08010 was revised May 20, 2026 — check the v2 for any sharpened measurement proposals.
