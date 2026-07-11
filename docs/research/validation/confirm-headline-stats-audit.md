---
content_origin: independent-confirmation
target: headline-stats-audit
date: 2026-05-31
analyst: independent-confirmation-skeptic
---

# Independent Confirmation: Headline Statistics Audit

Adjudication of the five load-bearing headline numbers in the Decision Brief. Each
verdict is traced to a PRIMARY source (the paper, the vendor's first-party report).
Secondary blogs were used only to locate primaries, never to confirm a figure.

Note: orchestrator passed `date: undefined` and output path `undefined/validation/...`.
Session context fixes today's date at 2026-05-31; file written to the requested literal
path.

---

## Claim 1 — "38-61% of AI-agent-authored PRs merge with NO recorded human review (MSR / EASE 2026)"

**Verdict: PARTIALLY-CONFIRMED (with a misattribution + a conflation of two different statistics).**

What the primaries actually say:

- **61.38%** — Duma et al., *"These Aren't the Reviews You're Looking For: How Humans
  Review AI-Generated Pull Requests"*, **EASE 2026** (30th Intl. Conf. on Evaluation and
  Assessment in Software Engineering, Glasgow). arXiv:2605.02273v1, **May 4, 2026**.
  Exact figure: "61.38% (20,621) receive **no recorded review activity**" in popular
  repositories. Note this is "no recorded review activity," NOT specifically "no human
  review" — a separate 22.6% are reviewed *exclusively by agents*, and 15.9% show human
  participation. Also: in same-repo comparison, AI PRs had LESS no-review (28.92%) than
  human PRs (34.52%), an important nuance the brief omits.
  URL: https://arxiv.org/html/2605.02273v1

- **38%** — a DIFFERENT paper: *"Where Do AI Coding Agents Fail? An Empirical Study of
  Failed Agentic Pull Requests in GitHub"*, **MSR 2026** (Mining Software Repositories).
  arXiv:2601.15195v1. Exact figure: "228 PRs (38%)" = the share of *rejected/failed*
  agentic PRs in the reviewer-level-abandonment category, "left without any meaningful
  human reviewer interaction." This is 38% of REJECTED PRs, not 38% of all merged PRs.
  URL: https://arxiv.org/html/2601.15195v1

Problems with the brief's framing:
1. **"38-61%" is a manufactured range** stitching together two unrelated statistics from
   two different papers measuring two different populations (no-review-activity among
   popular-repo PRs vs. reviewer-abandonment among rejected PRs). They do not bound a
   single quantity.
2. **"MSR / EASE 2026"** — the 61.38% is EASE 2026; the 38% is MSR 2026. Citing them as a
   joint "MSR / EASE" source is loose. The headline 61% figure is EASE, not MSR.
3. **"merge with no review"** — the 61.38% is "no recorded review *activity*," which
   includes PRs that may be auto-merged or never engaged; the brief's gloss "merge with
   NO recorded human review" is directionally fair for that one number but conflates it
   with agent-only review (22.6%).

Bottom line: the 61% number is real and well-sourced (EASE 2026); the 38% number is real
but measures rejected PRs, not merges. The "38-61%" range as stated is misleading.

---

## Claim 2 — "CodeRabbit: AI code ~1.7x more issues, ~2.74x more XSS vulns (~Dec 2025)"

**Verdict: CONFIRMED.**

Primary source: CodeRabbit's own press release on BusinessWire, *"CodeRabbit's 'State of
AI vs Human Code Generation' Report Finds That AI-Written Code Produces ~1.7x More Issues
Than Human Code"*, **December 17, 2025** (first-party vendor announcement).
- "AI-written code produces ~1.7x more issues than human code" — exact, headline figure.
- "2.74x more likely to add XSS vulnerabilities" — confirmed; part of a security
  breakdown also citing 1.88x improper password handling, 1.91x insecure object
  references, 1.82x insecure deserialization.
- Sample: 470 real-world pull requests.
- Corroborated by The Register (2025-12-17) and Cybernews, but the BusinessWire release is
  the first-party primary.
URL: https://www.businesswire.com/news/home/20251217666881/en/CodeRabbits-State-of-AI-vs-Human-Code-Generation-Report-Finds-That-AI-Written-Code-Produces-1.7x-More-Issues-Than-Human-Code

Both numbers and the ~Dec 2025 date are accurate. Caveat for the reader: this is a
vendor's self-published analysis (CodeRabbit sells AI code review), not peer-reviewed —
selection/incentive bias should be flagged, but the figures themselves check out.

---

## Claim 3 — "Anthropic 2026: AI in ~60% of work, fully delegate only 0-20%; auto-approval ~20%->40%+, interrupt 5%->9% with experience (Feb 2026)"

**Verdict: PARTIALLY-CONFIRMED (figures correct; sources and dating conflated).**

The brief blends TWO distinct Anthropic first-party publications and mis-dates one:

- **"How AI Is Transforming Work at Anthropic"** — published **December 2, 2025** (NOT
  Feb 2026). Source of the work-usage + delegation figures:
  - "use Claude in **59%** of their work" (brief rounds to ~60% — acceptable). Up from
    28% twelve months prior.
  - "More than half said they can 'fully delegate' only between **0-20%** of their work."
    CONFIRMED exactly.
  - Data: Aug 2025 survey; Claude Code transcripts Feb 2025 vs Aug 2025; task complexity
    3.2 -> 3.8. (No auto-approve/interrupt figures appear in this article.)
  URL: https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic

- **"Measuring agent autonomy" (a.k.a. agent autonomy research)** — published
  **February 18, 2026**. Source of the auto-approve + interrupt figures:
  - New users (<50 sessions): "~20% of sessions use full auto-approve"; experienced users
    (750+ sessions): "over 40% of sessions." CONFIRMED (20% -> 40%+).
  - New users (~10 sessions): interrupt ~5% of turns; experienced: "around 9% of turns."
    CONFIRMED (5% -> 9%).
  URL: https://www.anthropic.com/research/measuring-agent-autonomy

All four figures are accurate against primaries. The defects are attribution/dating:
"~60%" and "0-20%" come from a **Dec 2025** post, not Feb 2026; only the auto-approve and
interrupt figures are from the Feb 18 2026 publication. The brief bundles them as one
"Feb 2026" Anthropic source, which is imprecise.

---

## Claim 4 — "DORA 2025 State of AI-assisted Software Development: ~90% use AI daily; 80%+ report productivity gains (Sep 2025)"

**Verdict: CONFIRMED (one minor wording caveat).**

Primary source: Google/DORA 2025 report, announced on the Google blog
**September 23, 2025**, and the report site dora.dev.
- "**90%** of software development professionals use AI" — confirmed. Median two hours
  daily working with AI. (Caveat: the headline is "90% use AI," with a median of ~2 hrs/
  day of use; "90% use AI **daily**" is a fair gloss given the daily-usage framing, but
  the strictly stated stat is 90% adoption + median 2 hrs daily.)
- "Over **80%** of respondents indicate AI has enhanced their productivity" — confirmed.
- Sample: nearly 5,000 technology professionals globally; 100+ hours qualitative data.
URL: https://blog.google/innovation-and-ai/technology/developers-tools/dora-report-2025/
URL: https://dora.dev/dora-report-2025/

Numbers, source, and date all hold. Only minor: "daily" vs "use AI / 2 hrs median daily."

---

## Claim 5 — "METR: mid-2025 RCT found experienced devs ~19% SLOWER; Feb 2026 follow-up found same devs ~18% FASTER, attributing reversal partly to selection bias / learning"

**Verdict: REFUTED (as framed) — the number exists but the characterization inverts METR's actual conclusion.**

Primaries:

- Original RCT: METR, *"Measuring the Impact of Early-2025 AI on Experienced Open-Source
  Developer Productivity"*, **July 10, 2025**. Found AI caused a **19% slowdown** (devs
  took 19% longer; CI roughly +2% to +39%), data Feb-June 2025. CONFIRMED.
  URL: https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/

- Follow-up: METR, *"We are Changing our Developer Productivity Experiment Design"*,
  **February 24, 2026** (the brief says "Feb 2026" — close). The headline of THIS post is
  that the new-experiment data is **UNRELIABLE due to selection bias**, NOT a clean
  finding of "18% faster."
  - The -18% speedup estimate for original developers DOES appear (CI -38% to +9% — i.e.,
    crosses zero, not significant), and -4% for new developers.
  - But METR explicitly states: "we believe that the data from our new experiment gives us
    an unreliable signal of the current productivity effect of AI tools."
  - The selection bias METR describes biases the estimate the OPPOSITE way the brief
    implies: developers who refused to work WITHOUT AI dropped out, and 30-50% self-
    selected tasks avoiding ones where AI helps most — both of which METR says "likely
    biases **downwards** our estimate of AI-assisted speedup." So METR thinks the true
    speedup is probably even larger than the unreliable +18%, not that the +18% is a
    trustworthy reversal.
  URL: https://metr.org/blog/2026-02-24-uplift-update/

Why REFUTED as framed:
1. The brief presents +18% faster as a **finding**; METR presents it as an **unreliable
   signal** they explicitly decline to trust, which is why they redesigned the experiment.
2. "Attributed the reversal partly to selection bias / **learning**" — the selection-bias
   part is present (and it pushes the estimate DOWN, not explaining an upward reversal),
   but "learning" is not METR's stated mechanism for the change; the post is about
   methodological invalidity, not a learning-curve explanation.
3. Magnitudes of the raw point estimates (19% slower -> 18% faster) are real, but
   presenting them as a validated before/after reversal contradicts METR's own caveat.

Net: ~19% slower (2025) is solid. The "18% faster" is a point estimate METR labels
unreliable; the brief overstates it as a confirmed reversal and mischaracterizes the
selection-bias direction.

---

## Summary table

| # | Claim | Verdict | Primary | Date |
|---|-------|---------|---------|------|
| 1 | 38-61% AI PRs no human review (MSR/EASE 2026) | partially-confirmed | EASE 2026 arXiv 2605.02273 (61.38%); MSR 2026 arXiv 2601.15195 (38% of *rejected*) | 2026-05-04 / 2026 |
| 2 | CodeRabbit 1.7x issues, 2.74x XSS (Dec 2025) | confirmed | CodeRabbit/BusinessWire release | 2025-12-17 |
| 3 | Anthropic 60% work / 0-20% delegate / 20->40% auto-approve / 5->9% interrupt | partially-confirmed | "How AI Transforms Work" (Dec 2 2025) + "Measuring agent autonomy" (Feb 18 2026) | 2025-12-02 / 2026-02-18 |
| 4 | DORA 2025: 90% use AI, 80%+ productivity (Sep 2025) | confirmed | Google/DORA blog + dora.dev | 2025-09-23 |
| 5 | METR 19% slower -> 18% faster reversal (Feb 2026) | refuted (as framed) | METR Jul 10 2025 + Feb 24 2026 posts | 2025-07-10 / 2026-02-24 |

## Material corrections / newer evidence the brief should incorporate

- The METR +18% is NOT a validated reversal; METR redesigned the study because the data is
  unreliable, and the selection bias biases the estimate DOWNWARD. Brief must soften.
- Anthropic figures span two papers and two dates (Dec 2025 + Feb 2026); not one Feb 2026
  source.
- The "38-61%" range mixes two incommensurable statistics; the clean, defensible figure is
  EASE 2026's 61.38% "no recorded review activity," with the same-repo nuance that AI PRs
  are not reviewed LESS than human PRs in matched repos.
- CodeRabbit and DORA are vendor/industry self-reports (selection/incentive bias) — figures
  correct, but not peer-reviewed; the brief should label them as such.
