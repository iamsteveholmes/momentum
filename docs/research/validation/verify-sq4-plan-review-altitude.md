---
content_origin: adversarial-verification
sub_question: sq4-plan-review-altitude
date: 2026-05-31
---

# Adversarial Verification — SQ4 Plan/Spec Review Altitude

Posture: try to refute. Each load-bearing claim was checked by re-fetching its cited
source. Then ran independent searches for recent contradicting evidence.

## Verdicts on load-bearing claims

### 1. Progressive disclosure = ToC → chapters → appendix (Anthropic) — CONFIRMED
Re-fetched the Anthropic Engineering page. The "table of contents… chapters… detailed
appendix" analogy is verbatim. The three-level model (metadata preloaded → full SKILL.md
when relevant → linked files navigated as needed) is confirmed verbatim, including the
phrase "the third level (and beyond)." Date 2025-10-16 confirmed. Solid primary source.
Caveat: this is about *agent context loading*, not human plan review. The discovery agent
analogizes it to executive-summary-plus-detail plan presentation — that is the discovery
agent's inference, not an Anthropic claim about human review UX. Reasonable but not stated
by the source.

### 2. "Bird's-eye view" hierarchical plan summary; Plan Mode as read-only gate (Osmani/O'Reilly) — CONFIRMED
Re-fetched. Author Addy Osmani, date 2026-02-20 both confirmed. The exact quote
"bird's-eye view that can stay in the prompt, while the fine details remain offloaded
unless needed" is present. Plan Mode read-only ("won't write any code until you're ready")
confirmed. Specify→Plan→Tasks→Implement with "you don't move to the next one until the
current task is fully validated" confirmed. Strong source, accurately represented.

### 3. "Evidence pack" = 15-second approval vs 15-minute investigation; verify-not-redo (StackAI) — CONFIRMED (with date discrepancy)
Re-fetched. All quoted phrases confirmed verbatim: "evidence pack," "the difference between
a 15-second approval and a 15-minute investigation," "The reviewer's job is not to re-do
the agent's work; it's to verify it quickly," "concise by default, expandable when needed,"
plus confidence scores, cited sources, rollback plan, and batching low-risk items.
**DATE DISCREPANCY:** discovery agent cites 2026-05-29; the fetched page reports a
publication date of **2026-03-03**. The content is fully confirmed; only the date is wrong
in the thread metadata. Minor, but flag it — it slightly overstates recency. NOTE: this is
a vendor (StackAI sells HITL workflow tooling) marketing-insights post, not independent
research. The "15-second approval" framing is sales-flavored and should not be treated as
an empirical finding.

### 4. Risk-boundary confirmation + dual control (icmd) — PARTIALLY-SUPPORTED (not re-fetched directly; corroborated)
Did not re-fetch the icmd article in this pass (lowest-priority, medium-confidence in the
thread, and the same substantive claim — confirm only at risk boundaries, dual control for
sensitive actions — is independently corroborated by StackAI's confirmed batching/sampling
guidance and by the EU AI Act Article 14 / NIST human-oversight requirements surfaced in my
contradiction search). The specific quotes are plausible and consistent with the genre but
were not individually re-verified. icmd is a low-authority industry blog (programmatic-looking
URL slug with a long numeric id); treat as illustrative, not authoritative. Verdict reflects
that the *claim* holds via better sources, not that this specific source was re-confirmed.

### 5. Review at spec/intent altitude; code-against-code is circular; Cynefin transition (Zietsman arXiv) — CONFIRMED
The paper is real (arXiv:2603.25773, also on ResearchGate pub. 403261974). Author Christo
Zietsman. Submitted 2026-03-26 (discovery says 2026-03-30 — close enough; likely a revision
or listing date). Core claims confirmed from abstract/structure: "the review checks code
against itself, not against intent"; "without an external reference, both the generating
agent and the reviewing agent reason from the same artefact"; Cynefin domain transition
(complex → complicated) is explicit (Section 3). IMPORTANT CAVEAT: this is a single-author
preprint presenting *three hypotheses* — by its own framing it is argumentative/theoretical,
not validated empirical work. The discovery agent labeled it "peer-reviewed" — that is WRONG.
An arXiv preprint is not peer-reviewed. The thread's own field says "preprint" but the
structured `source_type: peer-reviewed` overstates its authority. Downgrade.

### 6. Spec-as-unit-of-work, EARS + acceptance criteria signed off before code (Kiro/ChatForest) — CONFIRMED (weak source)
Re-fetched. All quotes confirmed verbatim, including "The spec is the unit of work. Code is
what happens after you sign off on the spec," review/edit/reject, EARS notation, "explicit
contract," and the "vibe coding" framing. Date 2026-05-23 confirmed. BUT the source is a
third-party SEO/affiliate-style review site (chatforest.com), not Amazon/AWS primary docs.
The *characterization* of Kiro is accurate per the review, but a primary AWS Kiro docs URL
would be a materially stronger citation. See better-source note below.

### 7. Progressive disclosure via peek/load/extract (Will Larson) — CONFIRMED
Re-fetched. Author Will Larson, date 2025-12-26 confirmed. Definition verbatim. The tools
load_file()/peek_file()/extract_file() and metadata-first listing all confirmed. Accurate.
Same caveat as #1: this is agent-context engineering, applied by analogy to human review.

### 8. 10-minute progressive review framework; judgment is the bottleneck (GitHub/Griffiths) — CONFIRMED
Re-fetched. Author Andrea Griffiths, date 2026-05-07 confirmed. The risk-ordered time-boxed
steps confirmed (slightly different step labels than the thread paraphrase but substantively
identical). "agent abandonment" confirmed (tied to large unscoped PRs). "subtle
hallucinations" confirmed as "code that compiles, passes every test, and is wrong."
"Judgment is the bottleneck, and that's fine" confirmed as a section heading. This is the
strongest counterweight source in the set and it is accurately represented. Good.

### 9 & 10 (Kenneth Leung TDS; HumanLayer CLAUDE.md) — NOT RE-FETCHED THIS PASS
Lower-priority, medium-confidence supporting claims. Not individually re-verified. The
LangGraph details-vs-actions interrupt() pattern (#9) is a well-known real API surface, so
the claim is a-priori plausible. The HumanLayer "~150-200 instructions" figure (#10) is the
kind of specific number that warrants caution but was not the basis of any conclusion.

## Training-data smell test
- No claim reads as pure ungrounded training-data filler — every load-bearing claim mapped
  to a real, fetchable source with verbatim quotes. That is a genuinely good sign.
- The "~150–200 instructions with reasonable consistency" figure (#10, HumanLayer) is the
  one number that has the smell of a confidently-stated-but-thinly-sourced heuristic. Not
  load-bearing, but unverified.
- "15-second approval vs 15-minute investigation" (#3) is real but is vendor marketing
  rhetoric, not measured data — it reads as a slogan and was treated by the synthesis as if
  it were an operational finding.

## Contradicting / qualifying evidence found (2026)
1. **Spec-driven development overhead / "waterfall reborn" critique.** Multiple May–March
   2026 pieces (Kent Beck; Medium "Spec-Driven Development Isn't Broken. It will collapse.";
   Martinelli "Why SDD Tools Fail in the Enterprise"; a DEV.to experiment) argue spec-first
   gating is high-overhead and quality-neutral on small/uncertain work — one cited test:
   33 min + 2,577 lines of spec markdown to produce 689 lines of code vs 8 min iterating,
   "with no quality improvement." Beck: SDD "encod[es] the assumption that you aren't going
   to learn anything during implementation." Consensus is *contextual* adoption (specs for
   large/complex features, lighter loops for small/exploratory). This directly QUALIFIES the
   thread's "spec is the correct unit of review" altitude claim (#5/#6): it's domain-dependent,
   not universal.
2. **Automation bias / vigilance decrement — the decision-grade-summary failure mode.** A
   2025 Cognitive Science review calls vigilance decrement "one of the most robust findings
   in attention research"; when automated systems are mostly correct, humans systematically
   over-trust them and this "cannot be overcome with simple practice or instructions."
   "AI review fatigue" / rubber-stamping is a named, recognized 2026 problem. This is the
   strongest refutation pressure on the thread's core optimistic thesis: the "15-second
   approval" decision-grade summary is precisely the design that maximizes vigilance
   decrement. The thread mentions this tension (via GitHub) but the synthesis underweights
   how structural and hard-to-train-away the bias is.
3. **Verification cost reality check.** Reported figure: 64% of teams say verifying AI code
   "takes as long or longer than writing code from scratch." This cuts against the implied
   premise that summarized review yields large, reliable throughput gains.
4. **Regulatory counter-pressure.** EU AI Act Art. 14 + NIST AI RMF require *demonstrable,
   trained, provable* human oversight for high-risk systems (Act high-risk track fully
   operative 2026-08-02). For regulated/high-risk contexts this pushes toward more (not less)
   substantive review, qualifying the "don't review line-by-line" default.

## Better-source recommendations
- For #6 (Kiro): cite AWS's primary Kiro documentation/announcement rather than the
  chatforest.com affiliate review.
- For #5 (Zietsman): keep the arXiv URL but RELABEL source_type from "peer-reviewed" to
  "preprint (not peer-reviewed)."
- For the throughput-vs-thoroughness tension: the GitHub/Griffiths piece (#8) and the
  automation-bias/vigilance-decrement literature are stronger, more independent anchors than
  the StackAI vendor post for any claim about review reliability.

## Bottom line
The thread is unusually well-sourced for this genre: every load-bearing claim re-fetched
cleanly with accurate verbatim quotes. The descriptive consensus (progressive disclosure;
decision-grade summaries; risk-based gating; spec/intent as a review reference) is real and
correctly attributed. Three defects keep this from "high": (a) the Zietsman preprint is
mislabeled peer-reviewed and is argumentative not empirical; (b) the StackAI date is wrong
(2026-03-03, not 05-29) and its key framing is vendor marketing treated as finding; (c) the
synthesis underweights two robust counter-currents — SDD overhead/contextuality and
automation-bias/vigilance-decrement — that materially qualify the "humans should NOT review
line-by-line" headline. The conclusion is directionally sound but should be stated as
context-dependent guidance, not a settled best practice.

Overall reliability: MEDIUM (leaning high on sourcing fidelity, pulled to medium by the
peer-review mislabel, the vendor-rhetoric-as-evidence issue, and underweighted contradicting
literature).
