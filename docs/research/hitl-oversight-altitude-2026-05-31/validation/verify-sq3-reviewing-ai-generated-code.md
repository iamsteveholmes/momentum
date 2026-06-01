---
content_origin: adversarial-verification
sub_question: sq3-reviewing-ai-generated-code
date: 2026-05-31
---

# Adversarial Verification: Reviewing AI-Generated Code (every line vs. sampling)

Verifier stance: skeptical. Default to unsupported/unverifiable when the cited
source does not independently confirm the claim. Today: 2026-05-31.

## Verdict summary

Most of the load-bearing empirical claims hold up well — notably the four
peer-reviewed MSR/EASE 2026 papers and the Faros telemetry numbers, which I
re-fetched and confirmed to the decimal. The thread's synthesis is broadly
sound. Two material problems:

1. **One fabricated/misattributed statistic.** The JetBrains blog's "20–25% of
   AI hallucinations detectable by static analysis / ~44% escape automated
   detection" is NOT supported by the paper JetBrains cites (arXiv 2409.20550).
   That paper gives a hallucination *type* taxonomy (43.53/31.91/24.56%) and
   only a *qualitative* statement that "some" hallucinations are statically
   detectable while others evade detection — no detectability percentages at
   all. The discovery agent passed these numbers through at "medium" confidence
   without flagging the provenance gap. Mark UNSUPPORTED.

2. **METR 19% slowdown is real but over-generalized.** The slowdown is genuine
   and independently confirmed, but METR itself stresses the slowdown
   *percentage* likely does NOT generalize (narrow population: 16 devs on mature
   codebases they know deeply, exactly where AI helps least), and METR redesigned
   the experiment in Feb 2026 after a follow-up gave unreliable signals. The
   thread leans on a secondary vendor source (Augment Code) and omits these
   caveats. Confirmed-but-qualified.

Minor: the perception gap is "+24% faster" in the primary source, not the
"~20%" stated in one finding line (immaterial). Willison's "typing assistant vs
vibe coding" phrasing is not on the cited Stefan Judis page (it's a Willison
position elsewhere); the accountability + dereliction-of-duty quotes ARE on it.

## Claim-by-claim

### 1. Faros telemetry: 154% PR size / 91% review time / 9% bugs / 98% merged PRs — CONFIRMED
Re-fetched https://www.faros.ai/blog/lab-vs-reality-ai-productivity-study-findings.
All four figures verbatim; "10,000+ developers across 1,255 teams" over "up to
two years" confirmed. Caveat: this is vendor telemetry (correlational, not
causal — high-AI-adoption teams may differ systematically), and Faros has a
commercial interest in the "AI productivity paradox" framing. Numbers are
accurately reported but should be read as observational, not experimental.

### 2. Duma et al. EASE 2026 — 61.38% no review, 71.58% agent comments, 25.92% vs 1.63% steering (V=0.34) — CONFIRMED
Re-fetched https://arxiv.org/html/2605.02273v1. Every figure matches to the
decimal, including raw counts (20,621; 28,004). Title/authors/dataset (AIDev,
33,596 PRs, repos ≥100 stars) confirmed. Strong source.

### 3. Ehsani et al. MSR 2026 — rejection taxonomy 38/23/17/3%, 71.48% merge — CONFIRMED
Re-fetched https://arxiv.org/html/2601.15195. Abandoned/Not Reviewed 228 (38%),
Duplicate 142 (23%), CI/Test 99 (17%), Incorrect Impl 19 (3%); overall merge
71.48% (24,014/33,596). Per-agent breakdown also confirmed (Codex 82.59%,
Copilot 43.04%, Devin 53.76%, Cursor 65.22%, Claude Code 59.04%). Note the
taxonomy percentages are over 562 manually-analyzed rejected PRs, not the full
corpus — the thread states this correctly. Strong source.

### 4. Chowdhury et al. MSR 2026 — 60.2% 0-30% signal, 12/13 CRAs <60%, 45.20% vs 68.37% merge (chi2=83.03, p<0.001) — CONFIRMED
Re-fetched https://arxiv.org/html/2604.03196v1. All figures verbatim. Note the
exact framing is "23.17 percentage points lower" (45.20 vs 68.37). Strong source.

### 5. DORA 2025 — AI as amplifier, 30% distrust, trust-but-verify, negative stability — CONFIRMED (split sourcing)
The dora.dev landing page confirmed the "amplifier" quote verbatim but does NOT
contain the 30%/trust-but-verify/stability figures (those are in the PDF).
Cross-confirmed via Google Cloud blog + multiple independent summaries: "30%
report little or no trust," explicit "trust but verify," negative relationship
with delivery stability. IMPORTANT QUALIFIER the thread omits: DORA 2025 reports
AI is now POSITIVELY linked to throughput — "a positive reversal of last year's
findings." The thread's "negative on stability" is correct but the full DORA
nuance (throughput reversed positive) should be carried.

### 6. JetBrains: 20-25% hallucinations static-detectable / 44% escape — UNSUPPORTED
Re-fetched the JetBrains blog AND its cited source arXiv 2409.20550. The paper
does NOT report these percentages. It gives hallucination-TYPE distribution
(43.53% task-requirement conflicts, 31.91% factual knowledge, 24.56% project
context) and a qualitative-only statement about detectability. The 20-25%/44%
figures are not in the cited paper. This is a provenance failure: the figures
appear fabricated or misattributed by the JetBrains author. The 73.8%-acted-on /
42%-closure-time-increase claim cites a DIFFERENT paper (arXiv 2412.18531) and
is plausibly real, but I did not independently confirm that second paper's
numbers. Treat the hallucination-detectability split as unsupported.

### 7. METR: experienced devs 19% slower, perceived faster, ~9% time reviewing AI — CONFIRMED but OVER-GENERALIZED
Independently confirmed (InfoWorld, arXiv 2507.09089, METR's own blog). 16 devs,
246 tasks. BUT: (a) perceived speedup is +24% in the primary source, not the
"~20%" in the finding; (b) METR explicitly warns the slowdown PERCENTAGE likely
does not generalize — population is unusually narrow (devs with avg 5yr/1,500
commits on mature, high-standard repos where AI is least helpful); (c) METR
changed the experiment design in Feb 2026 after a follow-up produced unreliable
signals (non-participation bias from devs unwilling to work without AI). METR
says the EXPECTATION GAP generalizes, the slowdown number does not. The thread
relies on a secondary vendor source (Augment Code) and omits these caveats.

### 8. ContextQA: AC-TDD, 85-90% vs 70-80% coverage, tautological testing — PARTIALLY SUPPORTED
Re-fetched https://contextqa.com/blog/what-is-ai-generated-code-testing-checklist/.
The "validate the specification not the implementation," "tautological testing,"
and shared-blind-spots framing are all present and accurately quoted. BUT the
85-90% vs 70-80% coverage thresholds are presented as bare assertions with NO
source — training-data-smell. The article sources its other stats (Stack
Overflow, Stanford) but not these. The conceptual claims are reasonable; the
specific numeric bars are ungrounded blog opinion, not evidence.

### 9. Simon Willison — accountability / dereliction of duty — CONFIRMED (one phrase not on this page)
Re-fetched the Stefan Judis notes. "A computer can never be held accountable.
That's your job as the human in the loop" and the "dereliction of duty" / "shifts
the burden of the actual work to whoever is expected to review our code" quotes
are present and accurately attributed (Dec 19, 2025). The "typing assistant vs
vibe coding" characterization is NOT on this page (it is a known Willison
position from elsewhere); minor sourcing slip, not material.

### 10. GitHub Docs — 8-area multi-layer review, AI pitfalls, deleted-tests warning — CONFIRMED
Re-fetched https://docs.github.com/en/copilot/tutorials/review-ai-generated-code.
Eight areas confirmed by name. Hallucinated APIs, deleted/skipped tests, logic
errors, CodeQL + Dependabot, and the "fix the test instead of deleting it"
guidance all present and verbatim. Strong source.

## Training-data smells
- ContextQA "85-90% (AI) vs 70-80% (human)" coverage bars: unsourced numeric
  precision in a vendor blog; reads like plausible-sounding filler.
- JetBrains "20-25% / 44%" hallucination split: precise-looking numbers cited to
  a paper that does not contain them — the worst kind of smell (false precision
  with a fake-looking citation).
- "JiTTests ~4x more useful catches than generic hardening tests" (Meta): carried
  through from a New Stack blog; I did not find a primary Meta source confirming
  the 4x figure. Plausible but unverified — treat as vendor/blog claim.

## Contradicting / qualifying evidence found (2025-2026)
- **Genuine expert split on line-by-line review.** Contra the thread's "almost
  no one argues for reading every line," 2026 practitioners DO insist on careful
  per-line reading because "structural and logical failures are beneath the
  surface" of superficially-convincing AI code (javaworldmag 2026; CIO "Developers
  still don't trust AI-generated code"). The consensus is softer than the thread
  implies.
- **METR self-qualification (Feb 2026).** METR redesigned the productivity
  experiment because the original setting was unrepresentative; the slowdown
  percentage is explicitly not claimed to generalize. This weakens the thread's
  use of "19% slower" as a headline empirical anchor.
- **"Specification as Quality Gate" (arXiv 2603.25773, Jan/Mar 2026).** Independent
  preprint corroborating the tautological-testing concern with a sharper claim:
  deploying AI reviewers without EXECUTABLE specifications is structurally unsound
  because generator and reviewer "reason from the same artifacts and exhibit
  correlated failures." This is a stronger, peer-style source than the ContextQA
  blog the thread used for the same point.
- **DORA throughput reversal.** DORA 2025 now links AI POSITIVELY to throughput
  (reversing 2024). The thread's stability-negative framing is right but the
  throughput-positive reversal is a material qualifier it omits.

## Better sources than the weak ones cited
- For tautological testing / spec-as-trust: arXiv 2603.25773 "The Specification
  as Quality Gate: Three Hypotheses on AI-Assisted Code Review" (peer-style
  preprint) — stronger than contextqa.com blog and thenewstack.io.
- For the hallucination-detectability point: drop the JetBrains 20-25%/44%
  numbers entirely; cite arXiv 2409.20550 only for the QUALITATIVE finding that
  some hallucination classes (incomplete functionality, security) pass static
  checks and tests and thus require human judgment.
- For METR: cite metr.org/blog/2025-07-10 (primary) and metr.org/blog/2026-02-24
  (their own design-change/caveat) rather than the Augment Code secondary.

## Overall reliability: MEDIUM-HIGH
The four peer-reviewed 2026 papers and Faros telemetry are confirmed to the
decimal — the empirical backbone is solid. Downgraded from "high" by: one
unsupported/misattributed statistic (JetBrains hallucination split), an
over-generalized METR anchor, unsourced coverage bars, and an omitted DORA
qualifier (throughput now positive). The thread's core conclusion — review has
shifted to behavior/acceptance level + structural gates, with humans accountable
and "silent unreviewed merges" as the real-world failure mode — is well
supported.
