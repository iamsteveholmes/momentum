---
content_origin: web-discovery
sub_question: "sq6-trust-calibration-failure-modes"
date: undefined
---

# Trust Calibration: Automation Bias vs Verification Fatigue

## Synthesis

The 2025–2026 evidence converges on a single, sharply-defined problem: AI coding tools shift the bottleneck from *writing* to *judging*, and humans calibrate that judgment badly in both directions. On the UNDER-review side, the foundational human-factors result (Parasuraman & Manzey, 2010) — operators of highly reliable automation are ~50% less likely to detect failures — now reappears in the AI-coding context: Sonar's January 2026 survey of 1,100+ developers found 96% do not fully trust AI code yet only 48% always verify it before committing, a gap AWS CTO Werner Vogels labels "verification debt." A 2026 CHI analytical review and IUI '26 empirical work confirm over-reliance is the dominant inappropriate-reliance failure mode across HCI studies, and an Anthropic RCT (Feb 2026) shows full delegation to AI cuts measured skill/comprehension by ~17 points (50% vs 67% on quizzes), with pure code-generators scoring <40% while conceptual users scored >65%. The OVER-review side is equally real: reviewing AI code is harder than reviewing human code (38% of developers say so), AI produces ~1.7x more issues per PR (CodeRabbit, Dec 2025), and the resulting "density of work" / decision fatigue makes reviewers sloppy precisely when vigilance matters most — and verification fatigue itself feeds back into rubber-stamping.

Where the human adds the most value is now well-characterized and consistent across sources: AI review is reliable for mechanical and pattern-matchable defects (security signatures, null safety, style, code smells) but unreliable for business logic, architecture, system context, and intent — exactly the domains humans must own. Anthropic's 2026 Agentic Coding Trends Report frames this as "human oversight scales through intelligent failures": engineers report being able to "fully delegate" only 0–20% of tasks, keep design-dependent and conceptually difficult work, and delegate freely only what is "easily verifiable" (the "sniff-check on correctness" heuristic). The most actionable mitigations are interventions that calibrate trust to the *specific* output: counter-explanations during high-trust moments and forced pauses reduce over-reliance (38% reduction in inappropriate reliance, 20% accuracy gain in Srinivasan & Thomason 2026); specification-grounded review breaks the "circular" AI-reviews-its-own-output loop (Wang et al., reported 90.9% adoption lift). Sources disagree mainly on net effect: METR's RCT shows experienced devs were 19% *slower* with AI (and misperceived themselves as 20% faster), while the 2025 DORA report finds AI now *raises* throughput — but both agree it raises instability and pushes work downstream into review.

## Key Findings

### UNDER-reviewing: automation bias, complacency, the verification gap

1. **The verification gap: 96% distrust, only 48% verify.** Sonar's State of Code survey (1,100+ developers, released Jan 8 2026): "96% of developers do not fully trust that AI-generated code is functionally correct" yet "only 48% always verify their AI-assisted code before committing." 42% of committed code is AI-produced (expected 65% by 2027). 61% agreed AI "often produces code that looks correct but isn't reliable." — *Sonar press release & IT Pro coverage, Jan 2026.*

2. **"Verification debt" is now a named concept (AWS CTO Werner Vogels).** Fewer than half of developers review AI code before committing; the accumulated burden of unreviewed AI code is termed "verification debt." — *IT Pro, 2026-01-09.*

3. **Foundational automation-complacency result still governs.** Parasuraman & Manzey (2010): "operators of constantly high reliability systems were 50% less likely to detect failures than operators of unreliable systems." Complacency = suboptimal monitoring below a normative rate; occurs under multi-task load; "found in both naive and expert participants and cannot be overcome with simple practice." This is the mechanism underlying rubber-stamping of high-reliability-seeming AI output. *(Foundational; 2025–2026 work extends rather than supersedes it.)* — *Human Factors, 2010.*

4. **Over-reliance is the dominant failure mode in HCI reliance studies.** CHI '26 analytical review (Barcelona, April 2026): "recent empirical studies show critical concerns that people over-rely on AI advice without analytically engaging with it"; "user engagement is a precious commodity... however, it comes at a cost." Metrics in the literature include over-reliance, under-reliance, and Relative AI Reliance (RAIR), most introduced post-2020. — *Proc. CHI 2026.*

5. **Full delegation measurably atrophies skill (~17 points).** Anthropic RCT, 52 junior engineers learning the Trio async library (Feb 2026): "AI group averaged 50% compared to 67% for the manual coding group" on comprehension/debugging quizzes. Those using AI for *conceptual questions* scored ≥65%; those *delegating code generation* scored <40%. Speed gain was ~2 minutes and not statistically significant. — *InfoQ reporting Shen & Tamkin (Anthropic), Feb 2026.*

6. **The "augmentation trap": rational adoption can still erode long-run capability.** Caosun & Aral (MIT), arXiv 2604.03501 (May 21 2026): "even a decision-maker who fully anticipates skill erosion rationally adopts AI when front-loaded productivity gains outweigh long-run skill costs." When β<1 AI substitutes for skill; experienced workers develop fully while less-experienced ones "deskill permanently, widening inequality irreversibly." — *arXiv preprint (economic model), 2026.*

7. **Vibe-checking correlates with reduced comprehension and quality.** "The Vibe-Check Protocol" (Aiersilan, arXiv 2601.02410): accepting AI code "based on intuition rather than analysis" measurably reduces comprehension of the implemented solution and degrades code quality. — *arXiv preprint, 2026.*

### OVER-reviewing: verification fatigue, decision fatigue, throughput loss

8. **Reviewing AI code is harder than reviewing human code.** 38% of developers say reviewing AI-generated code requires more effort than reviewing colleagues' code. The burden falls on reviewers: "Reviewing [another's] code is so much harder than writing it. AI tools are increasing the rate at which people can churn out code that needs to be reviewed." — *Sonar (Jan 2026) and DORA insights (2026-03-10).*

9. **AI PRs produce ~1.7x more issues — more to catch, harder to catch.** CodeRabbit "State of AI vs Human Code Generation" report (470 open-source PRs, Dec 17 2025): AI-co-authored PRs averaged 10.83 issues/PR vs 6.45 for human-only (~1.7x). Logic/correctness issues +75%, readability 3x, security up to 2.74x, error-handling ~2x. "AI optimizes for surface-level correctness, not deep project context." — *CodeRabbit whitepaper / BusinessWire, Dec 2025.*

10. **Decision fatigue makes reviewers sloppy precisely when vigilance is needed.** AI lowered the cost of writing but raised cognitive load at review/verification, creating a "density of work" where devs "make high-stakes judgement calls" more than they code; "this imbalance leads to decision fatigue, increasing the risk of human error when reviewers become sloppy due to burnout." — *Dev|Journal (earezki.com), 2026-05-21 (search-result summary; full page returned 403).*

11. **"Babysitting the AI": creation time falls, auditing time rises.** DORA-cited engineer: "I feel somewhat more productive, but it's at a cost. While I end up spending less time writing code, I spend more time babysitting the AI." — *dora.dev/insights/balancing-ai-tensions, 2026-03-10.*

### Net effect & throughput (where sources diverge)

12. **METR RCT: experienced devs were 19% SLOWER with AI — and misjudged it.** 16 experienced OSS devs, 246 tasks on mature repos (22k+ stars, 1M+ LOC); randomized AI-allowed vs not. Result: +19% time with AI. Perception gap: expected −24% (speedup), still believed −20% afterward. Tools were mainly Cursor Pro + Claude 3.5/3.7 Sonnet. METR cautions this does *not* generalize to most developers or newer models. — *METR, 2025-07-10 (arXiv 2507.09089).*

13. **DORA 2025: AI raises throughput but also instability.** AI adoption ~90% (+14pts YoY); now positively associated with delivery throughput (a reversal) but still negatively associated with delivery *stability*. 30% of developers report little/no trust in AI code. "AI is an amplifier" — it intensifies existing team strengths/weaknesses. — *Google/DORA 2025 report (coverage Dec 2025–Mar 2026).*

### Where the human adds the most value

14. **Humans own intent, architecture, business logic; AI owns mechanical defects.** AI review is "highly accurate for security vulnerabilities and null safety but less reliable for business logic and architectural concerns." Humans remain essential for "business intent, system context, architectural implications, and compliance." 84% of devs use AI, only ~33% trust its accuracy. — *CodeAnt AI (2026-05-29) and 2026 industry review summaries.*

15. **Anthropic: "human oversight scales through intelligent failures" — delegate only the easily verifiable.** Engineers report being able to "fully delegate" only 0–20% of tasks; they keep "conceptually difficult or design-dependent" work and delegate freely only what they "can relatively easily sniff-check on correctness." The role shift is "from writing code to reviewing, prompting, active supervision, validation, and human judgment." Goal: "make human attention count where it matters most" — escalate "novel situations, boundary cases, and strategic decisions" to humans. — *Anthropic, 2026 Agentic Coding Trends Report.*

### Calibrating trust: interventions that work

16. **Trust-adaptive counter-explanations + forced pauses fix BOTH failure modes.** Srinivasan & Thomason, "Adjust for Trust" (IUI '26, Mar 2026): supporting-explanations at low trust and counter-explanations at high trust yield "up to 38% reduction in inappropriate reliance and 20% improvement in decision accuracy"; adaptive forced pauses reduce over-reliance. Counter-explanations adaptively > always-on (13–31% reduction in under-reliance, 9–38% reduction in over-reliance). Evidence of miscalibration: doctors over-rely at high trust, but at low trust "reject correct AI diagnoses 68% of the time, up from 40% otherwise" — under-reliance is just as costly as over-reliance. — *arXiv 2502.13321 / IUI 2026.*

17. **Specification-grounded review breaks the circular "AI reviews its own output" loop.** Zietsman, "The Specification as Quality Gate" (arXiv 2603.25773): homogeneous LLM review pipelines exhibit *correlated errors* (mistakes echo rather than cancel) and *overcorrection bias*; AI-to-AI review "checks code against itself, not against intent." Grounding review in human-authored specifications (Wang et al.) improved developer adoption of suggestions by 90.9% over a baseline LLM reviewer. — *arXiv preprint, 2026.*

## Named Frameworks

- **Automation complacency / automation bias (attentional integration model)** — Parasuraman & Manzey, 2010 (foundational; omission vs commission errors; complacency under multi-task load).
- **Appropriate reliance / over-reliance / under-reliance; Relative AI Reliance (RAIR)** — HCI human-AI decision-making literature, consolidated in CHI 2026 analytical review.
- **Verification gap / verification debt** — Sonar 2026; "verification debt" attributed to AWS CTO Werner Vogels.
- **The Augmentation Trap (α skill-neutral vs β knowledge-complementary gains; steady-state loss; skill divergence)** — Caosun & Aral, 2026.
- **Vibe-Check Protocol** — quantifying cognitive offloading in AI programming (Aiersilan, 2026).
- **Specification as Quality Gate; Correlated Error Hypothesis; Circular Review Problem; overcorrection bias** — Zietsman, 2026.
- **Trust-adaptive explanations / cognitive forcing (forced pauses, counter-explanations)** — Srinivasan & Thomason "Adjust for Trust," 2026.
- **"Human oversight scales through intelligent failures"; delegate-the-sniff-checkable heuristic; fully-delegate 0–20%** — Anthropic 2026 Agentic Coding Trends Report.
- **AI-as-amplifier (throughput up, stability down)** — DORA 2025.

## Debates & Tensions

- **Net productivity: slowdown vs speedup.** METR's RCT found a *19% slowdown* for experienced devs on familiar mature codebases, while DORA 2025 finds AI now *raises throughput* at scale. Reconciliation: both agree AI raises instability and shifts effort downstream into review; METR's population (expert OSS maintainers, high quality bars) is narrow, as METR itself cautions.
- **More AI reviewers as the fix — or a circular trap?** Industry response is to deploy AI reviewers as PR quality gates (CodeRabbit). Zietsman argues homogeneous AI-on-AI review is structurally circular and amplifies correlated errors absent a human-authored specification as ground truth.
- **Is over- or under-reliance the bigger danger?** Most HCI work (CHI '26) frames over-reliance as dominant, but "Adjust for Trust" shows under-reliance is also severe and costly (doctors rejecting correct AI advice 68% of the time at low trust) — arguing the real target is *calibration*, not maximizing or minimizing reliance.
- **Does AI help or hurt skill over time?** Anthropic/Augmentation-Trap show delegation erodes skill, but both also show conceptual/engaged use *preserves or builds* it — the determinant is *how* AI is used (delegation vs cognitive engagement), not adoption per se.
- **Source-type caution:** vendor reports (Sonar, CodeRabbit, CodeAnt, Anthropic) have commercial incentives (they sell review/verification tooling); their directional findings align with independent peer-reviewed/academic work (METR, CHI, IUI, MIT) but exact magnitudes should be read as vendor-favorable.

## Sources

- METR — Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity — https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ — 2025-07-10 — industry-report/peer-reviewed-preprint (arXiv 2507.09089)
- Sonar — "Sonar Data Reveals Critical Verification Gap in AI Coding" — https://www.sonarsource.com/company/press-releases/sonar-data-reveals-critical-verification-gap-in-ai-coding/ — 2026-01-08 — vendor industry-report
- IT Pro — "So much for 'trust but verify': Nearly half of developers don't check AI-generated code" — https://www.itpro.com/software/development/software-developers-not-checking-ai-generated-code-verification-debt — 2026-01-09 — news
- Parasuraman & Manzey — "Complacency and Bias in Human Use of Automation: An Attentional Integration," Human Factors — https://journals.sagepub.com/doi/10.1177/0018720810376055 — 2010 — peer-reviewed (foundational)
- CHI 2026 — "Do People Appropriately Rely on AI-Advice? An Analytical Review of HCI Research on Human-AI Decision-Making" — https://dl.acm.org/doi/10.1145/3772318.3791467 — 2026-04 (CHI '26) — peer-reviewed
- InfoQ — "Anthropic Study: AI Coding Assistance Reduces Developer Skill Mastery by 17%" (reporting Shen & Tamkin, Anthropic) — https://www.infoq.com/news/2026/02/ai-coding-skill-formation/ — 2026-02 — news reporting peer-reviewed RCT
- Caosun & Aral — "The Augmentation Trap: AI Productivity and the Cost of Cognitive Offloading" — https://arxiv.org/html/2604.03501 — 2026-05-21 — peer-reviewed preprint
- Aiersilan — "The Vibe-Check Protocol: Quantifying Cognitive Offloading in AI Programming" — https://arxiv.org/pdf/2601.02410 — 2026-01 — peer-reviewed preprint
- CodeRabbit — "State of AI vs Human Code Generation Report" — https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report — 2025-12-17 — vendor industry-report
- DORA — "Balancing AI tensions: Moving from AI adoption to effective SDLC use" — https://dora.dev/insights/balancing-ai-tensions/ — 2026-03-10 — industry-report
- Google Cloud / DORA — "Announcing the 2025 DORA Report" — https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report — 2025 — industry-report
- CodeAnt AI — "How Accurate Is AI Code Review in 2026?" — https://www.codeant.ai/blogs/ai-code-review-accuracy — 2026-05-29 — vendor blog
- Anthropic — "2026 Agentic Coding Trends Report" — https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf — 2026 — vendor industry-report
- Srinivasan & Thomason — "Adjust for Trust: Mitigating Trust-Induced Inappropriate Reliance on AI Assistance" (IUI '26) — https://arxiv.org/pdf/2502.13321 — 2026-01-27 (IUI '26, Mar 2026) — peer-reviewed
- Zietsman — "The Specification as Quality Gate: Three Hypotheses on AI-Assisted Code Review" — https://arxiv.org/pdf/2603.25773 — 2026 — peer-reviewed preprint
- Dev|Journal (earezki.com) — "Coding Agents Are Giving Everyone Decision Fatigue" — https://earezki.com/ai-news/2026-05-21-coding-agents-are-giving-everyone-decision-fatigue/ — 2026-05-21 — blog (page returned 403; summarized from search index)
