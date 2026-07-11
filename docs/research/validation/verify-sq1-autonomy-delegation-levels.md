---
content_origin: adversarial-verification
sub_question: sq1-autonomy-delegation-levels
date: 2026-05-31
---

# Adversarial Verification — Autonomy & Delegation Levels (Decision Altitude)

Reviewer stance: try to refute or qualify. Each load-bearing claim was checked by
re-fetching the cited source. Verdicts are conservative.

## Verdicts on load-bearing claims

### Finding 1 — Five human-role autonomy levels; autonomy as deliberate design choice (Feng, McDonald & Zhang)
- **Verdict: CONFIRMED.**
- arXiv 2506.12469 abstract re-fetched. The five levels (Operator, Collaborator,
  Consultant, Approver, Observer) are present. The exact quote "an agent's level of
  autonomy can be treated as a deliberate design decision, separate from its capability
  and operational environment" is verbatim in the abstract. Authors K.J. Kevin Feng,
  David W. McDonald, Amy X. Zhang. v1 2025-06-14, v2 2025-07-28. Current and accurate.
- Minor note: discovery labels this "peer-reviewed." It is an arXiv working paper /
  Knight First Amendment Institute working paper — not demonstrably peer-reviewed.
  Source-type label is slightly inflated but does not affect the claim.

### Finding 2 — "Autonomy certificates" issued by a third-party governing body, backed by an "autonomy case" analogous to a safety case
- **Verdict: CONFIRMED (with a framing caveat).**
- The arXiv ABSTRACT alone does NOT support the third-party-body language — it only
  "highlights a potential application." But the full Knight Columbia text (Section 4)
  does: "an autonomy certificate to be a digital document that prescribes the maximum
  level of autonomy at which an agent can operate," "issued by a third-party governing
  body to agent developers, and is stored with the agent's metadata," and "Autonomy
  cases can be thought of as analogous to safety cases." All three sub-claims verified.
- Caveat the discovery summary should carry: the paper frames this as ONE EXPLORATORY
  application ("we explore one potential application"), not a finalized proposal. The
  discovery text mostly conveys this, but the confidence:high + "proposes" verb slightly
  overstates how settled the mechanism is.

### Finding 3 — HITL/HOTL/HOOTL risk-tiered with time-boxed decision lanes (Strata)
- **Verdict: CONFIRMED.**
- Strata article (Eric Olden, updated 2026-05-11) re-fetched. HITL = "requires a human
  to approve or authorize an action before the AI system executes it." HOTL = "allows
  the AI to act autonomously while a human monitors outputs and can intervene after the
  fact." Time-boxed lanes verbatim: "15-second lane for low-risk actions, 2-minute lane
  for PII access, 15-minute lane for financial disbursements." HOOTL appears as an
  example phrase but is NOT formally defined in the three-term spectrum. Source is a
  vendor (identity-platform) blog — correctly labeled vendor-docs; treat as practitioner
  opinion, not standard.

### Finding 4 — CSA six-level L0–L5 taxonomy; technically enforced boundaries; L5 inappropriate today
- **Verdict: CONFIRMED.**
- CSA blog (Jim Reavis, 2026-01-28) re-fetched. L3 Conditional definition verbatim.
  "Autonomy boundaries must be technically enforced, not just policy-documented" present.
  "automatically drop to Level 1 if anomalies are detected" present. "I don't believe
  Level 5 is appropriate for enterprise deployment today" present. Fully supported.

### Finding 5 — Swarmia five coding-autonomy levels; higher isn't better; ceiling at L2–3
- **Verdict: CONFIRMED.**
- Swarmia (Miikka Holkeri, 2026-03-19) re-fetched. All five level names match. "It's not
  a ranking, and higher is not always better" present. CEO/intern/middle-schooler quote
  verbatim. Phone/PR Level-3 test verbatim. "most teams hit a ceiling somewhere between
  Level 2 and Level 3" present. Source correctly labeled blog/practitioner.

### Finding 6 — ASDLC L1–L5 with human roles Driver/Reviewer/Change Owner/Auditor/Consumer
- **Verdict: CONFIRMED.**
- ASDLC.io (last updated 2026-05-28) re-fetched. All five role pairings present verbatim
  ("Driver. Hands on wheel 100% of the time," "Change Owner. Async validation of CI/CD
  and intent drift," "Auditor. Post-hoc telemetry analysis," "Consumer. Passive
  beneficiary"). CAVEAT: no named author; self-published knowledge base ("© 2026
  ASDLC.io"). Low authority — fine as an illustrative framework, not as evidence of
  industry consensus. Discovery's confidence:medium is appropriate.

### Finding 7 — Anthropic telemetry: HITL→HOTL migration; auto-approve 20%→40%+, interrupts 5%→9%
- **Verdict: CONFIRMED (numbers); PARTIALLY-SUPPORTED (the "calibrated trust" gloss).**
- Anthropic article (2026-02-18) re-fetched. Auto-approve ~20% (new, <50 sessions) →
  >40% (experienced, ~750 sessions): confirmed. Interrupts 5% (new) → ~9% (experienced):
  confirmed. "80% of tool calls ... at least one kind of safeguard," "73% appear to have
  a human in the loop": confirmed. Turn duration 99.9th pct "under 25 minutes" (Oct 2025)
  → "over 45 minutes" (Jan 2026): confirmed.
- QUALIFICATION: The interpretation "calibrated trust, not blind trust" is the discovery
  agent's gloss, partly Anthropic's own framing. It is a reasonable reading, but the same
  data is equally consistent with the competing 2026 "HITL theater / oversight illusion"
  thesis (see contradicting evidence). Rising interrupts alongside rising auto-approve
  could indicate users catching MORE problems, not necessarily well-calibrated trust. The
  causal/normative spin is softer than the raw telemetry.

### Finding 8 — "Delegation gap": ~60% AI use, 0–20% full delegation; bottleneck = judgment not capability
- **Verdict: CONFIRMED (figures); SOURCING UPGRADE NEEDED.**
- The 60% / 0–20% figures and "the problem isn't capability, it's judgment" framing are
  real and trace to a genuine PRIMARY source: Anthropic's "2026 Agentic Coding Trends
  Report" (resources.anthropic.com/2026-agentic-coding-trends-report; PDF mirror exists).
  Corroborated independently across 5+ secondary write-ups (Pathmode, Clarvia, Context
  Studios, HiveTrail, NYU Shanghai). Discovery cites the Pathmode blog (secondary). The
  citation SHOULD be the primary Anthropic report.
- Minor date wrinkle: the underlying study/report is described elsewhere as published
  January 2026; Pathmode's post is 2026-03-11. Substantively sound.

### Finding 9 — DeepMind "Intelligent AI Delegation": authority transfer; atomic/open-ended/recursive; named concepts
- **Verdict: CONFIRMED.**
- arXiv 2602.11865v1 (2026-02-12) re-fetched (HTML body). Authors Tomašev, Franklin,
  Osindero, affiliation Google DeepMind confirmed in body. Delegation definition verbatim.
  All eight named concepts found in the body with quotes: atomic execution, open-ended
  delegation, recursive delegation, zone of indifference, authority gradient, liability
  firebreaks, privilege attenuation, contract-first decomposition. The single best-sourced
  finding in the set. (Source-type "peer-reviewed" is again slightly inflated — it's a
  preprint — but content is fully verified.)

### Finding 10 — Huang et al.: control-first; delegate bounded tasks, retain architecture/goal decisions
- **Verdict: PARTIALLY-SUPPORTED.**
- arXiv 2512.14012 exists; title and authors match ("Professional Software Developers
  Don't Vibe, They Control," Huang, Reyna, Lerner, Xia, Hempel; submitted 2025-12-16,
  discovery says 2025-12-17 — within revision noise). Core thesis confirmed by abstract:
  developers "retain their agency in software design and implementation out of insistence
  on fundamental software quality attributes." HOWEVER the specific quoted phrase
  "delegate specific, bounded tasks while maintaining control over broader objectives and
  architectural decisions" and "when outcomes significantly impact code quality, system
  architecture, or downstream consequences" were NOT located in the abstract/metadata —
  they may be in the body, or may be discovery-agent paraphrase presented as quotation.
  The CLAIM is supported; the QUOTED EVIDENCE strings are not independently confirmed.
  Treat as supported-in-substance, quotes-unverified. n=13 observations + 99 surveys is
  small — modest empirical weight.

### Findings 11–12 (Berkeley CMR decision rights; SAE J3016 as foundational analogy)
- **Verdict: UNVERIFIABLE / PLAUSIBLE (not independently re-fetched this pass).**
- These are medium-confidence in the discovery set and rest on secondary/blog summaries
  (Berkeley CMR + MachineLearningMastery for 11; TechLife blog for 12). The SAE-J3016-as-
  foundational-analogy claim is corroborated indirectly (my searches surfaced multiple
  independent confirmations that agent ladders borrow from SAE) — but see the major
  contradicting evidence: the SAE analogy is actively CRITIQUED, not just adopted.
  TechLife (Finding 12) is a low-authority blog summarizing HKUST/Tsinghua work; the
  underlying academic paper was not located/verified here.

## Training-data smell test

- No claim reads as pure ungrounded training-data filler — every load-bearing finding
  resolves to a real, datable 2025-2026 artifact, which is a good sign for a fast-moving
  topic.
- Mildest smells: (a) the recurring "peer-reviewed" source-type label on what are arXiv
  PREPRINTS / working papers (Feng et al., DeepMind, Huang et al.) — inflates authority.
  (b) Finding 10's quotation strings could not be matched to the source abstract; possible
  paraphrase-presented-as-quote. (c) The "convergence" narrative in the synthesis ("2025-
  2026 work converges on...") is partly an artifact of selection — the corpus is heavy on
  sources that AGREE; the genuine taxonomy-proliferation and oversight-skeptic literature
  is under-weighted (see below).

## Contradicting / qualifying evidence (my own searches, 2026)

1. **The SAE-J3016 analogy is actively critiqued, not merely adopted.** The interface-eu.org
   classification work and others note the SAE analogy's gains are non-linear and that
   self-driving "level" promises have repeatedly slipped for ~a decade; some argue 3 levels
   (human-controlled / bounded / broad) suffice and that the Parasuraman-Sheridan-Wickens
   10-level model is an older, more granular rival. This undercuts the synthesis framing of
   SAE as a clean "foundational analogy that the agent ladders build on." It is a contested,
   leaky analogy. (interface-eu.org/publications/ai-agent-classification;
   emergentmind.com/topics/levels-of-autonomy-in-ai-agents)

2. **"HITL theater" / oversight-illusion thesis directly challenges the optimistic
   calibrated-trust reading.** MIT Technology Review (2026-04-16, "humans in the loop ... an
   illusion"), Defense News (2026-03-26, military HITL "dangerously misleading"), and
   SiliconANGLE (2026-01-18, "human-in-the-loop has hit the wall") argue human overseers
   often lack the context/visibility to evaluate at machine speed — producing "the illusion
   of oversight rather than the substance." This qualifies Findings 3, 7, and 11: the
   HITL→HOTL migration the thread treats as healthy "calibrated trust" is, in a competing
   2026 reading, a slide toward nominal-only oversight. The thread's Debate #5 mentions AITL
   but UNDER-states how mainstream the oversight-skeptic critique became by mid-2026.

3. **Taxonomy proliferation is itself a finding the thread soft-pedals.** Beyond the five
   ladders catalogued, there are at least several MORE competing L1–L5 frameworks circulating
   in 2026 (OpenDataScience/Datasaur "Agents to Autonomy L1–5," Sean Falconer's "Practical
   Guide to Levels of AI Agent Autonomy"). This corroborates the recency_note's "terminology
   still consolidating" caveat but also weakens any implied "convergence": the field has MANY
   incompatible L0/L1–L5 ladders, not one converging standard.

4. **Competing causal explanation for the delegation gap.** Addy Osmani's "comprehension
   debt" (addyosmani.com/blog/comprehension-debt) frames the limit on full delegation as a
   downstream cost of not understanding AI-generated code — a different mechanism than the
   thread's "missing judgment/context/spec." Not a contradiction of the 60%/0-20% numbers,
   but a rival explanation that the thread's single-cause framing ("the problem isn't
   capability, it's judgment") omits.

## Better-source recommendations

- Finding 8: cite the PRIMARY Anthropic report
  (https://resources.anthropic.com/2026-agentic-coding-trends-report) instead of, or
  alongside, the Pathmode secondary blog.
- Finding 2: cite the Knight Columbia full text
  (https://knightcolumbia.org/content/levels-of-autonomy-for-ai-agents-1) rather than the
  arXiv abstract for the third-party-body / autonomy-case specifics — the abstract alone
  does not support those.
- Findings 7/3/11: add an oversight-skeptic counter-source (MIT Tech Review 2026-04-16) to
  balance the calibrated-trust framing.

## Overall assessment

Reliability: **HIGH** on the descriptive existence and content of named frameworks (Findings
1–6, 9 are solidly verified against primary text; the figures in 7–8 are real and primary-
sourced). Reliability drops to **MEDIUM** on (a) interpretive/normative glosses (calibrated
trust, single-cause delegation gap), (b) the "convergence" narrative, which under-weights
genuine taxonomy proliferation and the substantial 2026 oversight-skeptic / "HITL theater"
literature, and (c) two findings (10's exact quotes, 11–12's secondary sourcing) that are
supported in substance but not in the precise quoted form. Net: trustworthy as a catalogue
of frameworks; treat the synthesis's "convergence" and "calibrated trust" framings as
contestable.
