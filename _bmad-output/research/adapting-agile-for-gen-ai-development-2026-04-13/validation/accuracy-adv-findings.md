# Factual Accuracy — Adversary Findings

**Lens:** Factual Accuracy
**Reviewer framing:** Adversary (intuitive, pattern-aware, hunch-driven)
**Scope:** 9 corpus files in `/raw/`
**Skepticism:** Level 3 (Aggressive)

## Summary

The gemini-deep-research-output.md file is the primary source of suspicious claims — it is littered with named frameworks ("3-3-3 model", "V-Impact Canvas", "Kinetic Enterprise doctrine", "BMAD Quick Flow/Barry", "Silken Net hybrid", "Architect of Intent"), suspiciously convenient attributions, and citations to a "2026 Future of Software Development Retreat" whose specific outputs cannot be corroborated in the per-subagent files. Multiple subagent files invoke Casey West's "Agentic Manifesto," but the framing diverges between files (caseywest.com ADLC vs. an "early 2026" verification-vs-validation manifesto). Statistical claims across all files are numerous and highly precise, with several displaying classic LLM-hallucination signatures (spurious precision, uncorroborated cross-file contradiction, fabricated-sounding study scope).

**Findings by severity:**
- Critical: 3
- High: 10
- Medium: 9
- Low: 3

**Total findings:** 25

---

## Findings

### ACCURACY-001
- **severity:** critical
- **dimension:** traceability
- **location:** gemini-deep-research-output.md:Follow-up Q1 — The Kinetic Enterprise
- **description:** The gemini file attributes a "Kinetic Enterprise doctrine" to "Researchers at Deloitte and others" framing Agile as Labor/CapEx vs AI-native as Compute/OpEx with "fluid Team Topologies" based on real-time telemetry. Deloitte's trademarked "Kinetic Enterprise" concept is about SAP-based business transformation (real-time, intelligent, clean-core ERP), not an AI-native-vs-Agile epistemic doctrine. This appears to be a real brand repurposed to invent a framework.
- **evidence:** Source: "Researchers at Deloitte and others have introduced the Kinetic Enterprise doctrine: From Labor to Compute: Traditional Agile is a Labor-driven (CapEx) model; AI-native engineering is a Compute-driven (OpEx) model." No citation appears in Sources list. Deloitte's public Kinetic Enterprise content is about SAP S/4HANA transformation and does not articulate this labor-vs-compute dichotomy.
- **suggestion:** Remove the Deloitte attribution, or cite the specific Deloitte publication that makes this claim. If unable to find one, mark as "[UNVERIFIED — appears fabricated]."

### ACCURACY-002
- **severity:** critical
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Follow-up Q1 — Shape Up + NASA TRL
- **description:** Claim that "Silken Net" has "completely overhauled" their architecture by abandoning Agile for a hybrid of Shape Up and NASA's Technology Readiness Levels (TRL). No such company or case study is traceable. This reads as a fabricated practitioner example. "Silken Net" does not appear in any verifiable source, and the TRL + Shape Up hybrid is not documented in NASA TRL literature or Shape Up practitioner reports.
- **evidence:** Text: "Teams like Silken Net have 'completely overhauled' their architecture, abandoning Agile for a hybrid of Shape Up and NASA's Technology Readiness Levels (TRL)." No source cited.
- **suggestion:** Remove or verify with a specific URL/case study. If retained, demand a primary source.

### ACCURACY-003
- **severity:** critical
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Follow-up Q2 — Solo Developer frameworks (BMAD Quick Flow / Barry)
- **description:** The gemini output lists "BMAD Quick Flow" as using "'Barry,' an elite solo dev persona." This is inconsistent with known BMAD Method framings (which use various agent personas but no public "Barry"). More critically, the pairing of this "elite solo dev persona Barry" against a "Quick Spec to Quick Dev lean path" appears invented, or reflects confabulation blending BMAD with unrelated persona naming. The user's own environment hosts BMAD skills (`bmad-quick-dev`) but the "Barry" persona is not evidenced.
- **evidence:** Table row: "BMAD Quick Flow | Uses 'Barry,' an elite solo dev persona, to move from a 'Quick Spec' to 'Quick Dev' in a lean path." No source cited in Sources list; nothing corroborates "Barry" in public BMAD documentation.
- **suggestion:** Remove or verify via primary BMAD Method documentation. Flag as likely hallucinated unless direct citation is provided.

### ACCURACY-004
- **severity:** high
- **dimension:** traceability
- **location:** gemini-deep-research-output.md:Frameworks for the Agentic Era — 2026 Future of Software Development Retreat
- **description:** The file asserts a "consensus emergent from the 2026 Future of Software Development Retreat" and references the event multiple times, attributing specific concepts (e.g., "Agent Subconscious," "V-Impact Canvas"). Thoughtworks does host a "Future of Software Development" retreat, but specific 2026 outputs including these named concepts are not cited to any retreat report or article URL. Only a bare `thoughtworks.com` reference appears in the Sources list.
- **evidence:** "The consensus emergent from the 2026 Future of Software Development Retreat is that engineering rigor has not disappeared; it has relocated." Also: "the 2026 Retreat discussed the concept of an 'Agent Subconscious'..." No primary retreat URL or report is cited.
- **suggestion:** Replace with specific URLs or mark all 2026 Retreat claims [UNVERIFIED].

### ACCURACY-005
- **severity:** high
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Solving the 'Spec-Correct, Value-Zero' Problem — Architect's V-Impact Canvas
- **description:** The "Architect's V-Impact Canvas" is presented as a named framework bridging deterministic-vs-probabilistic systems. No public source (InfoQ, Fowler, Thoughtworks) documents a framework by this exact name. The sibling subagent files do not reference it. Reads as invented.
- **evidence:** "The Architect's V-Impact Canvas has been introduced as a stabilizing mechanism for what is termed the 'oil and water' moment in architecture..." Only a generic infoq.com reference is provided in Sources.
- **suggestion:** Provide direct InfoQ article URL. If none exists, remove. Unverifiable — high hallucination risk.

### ACCURACY-006
- **severity:** high
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Frameworks — 3-3-3 Model
- **description:** The "3-3-3 delivery model" (3 days concept → 3 weeks prototype → 3 months MVP) is presented as a Thoughtworks framework associated with AI/works. The research-thought-leader-frameworks file also references it. Thoughtworks' 2026 AI/works announcements do discuss compressed cycles but the specific 3-3-3 numerical schema may be a confabulation or oversimplification. The precise 90-day model with named rituals "Mob Elaboration" and "Mob Construction" at specific phases is claimed without a primary Thoughtworks URL.
- **evidence:** "A central component of this framework is the 3-3-3 delivery model... 3 Days... 3 Weeks... 3 Months." Sources list only thoughtworks.com bare reference.
- **suggestion:** Provide a specific Thoughtworks URL documenting the 3-3-3 schema. If unavailable, label [UNVERIFIED].

### ACCURACY-007
- **severity:** high
- **dimension:** correctness
- **location:** research-thought-leader-frameworks-agile-ai.md:Thoughtworks Looking Glass 2026
- **description:** Five specific "AIFSD" trends are listed with exact names: "Goal-Based Development Environments (GBDEs)", "Continuous Learning Delivery Systems", "Neural Software Twins", "Synthetic Engineers", "Multimodal Collaboration." These read as plausible-sounding but suspiciously packaged. Cannot corroborate whether Thoughtworks Looking Glass 2026 actually enumerates these five trends with these exact names.
- **evidence:** "Five trends under AIFSD: 1. Goal-Based Development Environments (GBDEs)... 2. Continuous Learning Delivery Systems... 3. Neural Software Twins... 4. Synthetic Engineers... 5. Multimodal Collaboration"
- **suggestion:** Quote directly from the Looking Glass 2026 report and verify each term. If any are paraphrases/inventions, mark them.

### ACCURACY-008
- **severity:** high
- **dimension:** correctness
- **location:** research-behavioral-validation-ai-agents.md:Cheating Problem — NIST CAISI cheating rates
- **description:** Claim that CAISI benchmarks showed cheating rates "ranged from 0.1% (SWE-bench Verified) to 4.8% (CVE-Bench)" is suspiciously precise. The NIST CAISI is a real entity (renamed from AI Safety Institute), but precise percentages like 0.1% and 4.8% need primary-source confirmation. The finding that "blocking Hugging Face access reduced model performance by ~15%" attributed to "Scale AI" is also unverified and suspiciously specific.
- **evidence:** "Cheating rates in CAISI benchmarks ranged from 0.1% (SWE-bench Verified) to 4.8% (CVE-Bench)." And: "Scale AI found that blocking Hugging Face access reduced model performance by ~15%, confirming models were looking up benchmark answers"
- **suggestion:** Cite the specific CAISI blog post/study for each percentage; confirm Scale AI attribution with URL. If unverifiable, flag as [UNVERIFIED — precise stats].

### ACCURACY-009
- **severity:** high
- **dimension:** traceability
- **location:** research-work-granularity-ai-speed.md:Upstream Bottleneck — task horizons
- **description:** Claim that ML benchmarks showed "the length of tasks AI can reliably complete has been doubling approximately every four months since 2024 — with supervised autonomous task horizons reaching roughly two hours as of late 2025 and projected to reach four days of unsupervised work by 2027" attributes these numbers to "METR research blog, 2025-07-10; MachineLearningMastery.com agentic trends 2026." METR's actual July 2025 study is on experienced OS developer productivity (found 19% slowdown), not task-horizon doubling curves. The doubling-every-4-months figure is associated with METR's separate "task horizon" analyses from March 2025, not the July 10 study. Citation is incorrect.
- **evidence:** Text attributes the doubling figure to "METR research blog, 2025-07-10" but the 2025-07-10 METR post is specifically about experienced OS developer slowdowns. The METR time-horizons doubling work (https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) is a different post.
- **suggestion:** Correct METR citation to the horizons paper (March 2025), and separate it from the July 2025 developer productivity study (which the research-cognitive-load-inversion.md file correctly characterizes).

### ACCURACY-010
- **severity:** high
- **dimension:** correctness
- **location:** research-cognitive-load-inversion.md:Cognitive Load — LinearB 2026 benchmarks
- **description:** Claims "5.3× longer" idle time, "2.47×" wait differential, "2× faster" review for agentic-AI PRs, sampled across "8.1 million PRs across 4,800 engineering teams in 42 countries." These are unusually precise figures for a benchmarks report. The reference URL is a generic landing page (linearb.io/resources/engineering-benchmarks); without direct citation to the report itself, the specific numbers cannot be corroborated.
- **evidence:** "agentic AI PRs sit idle 5.3× longer before anyone picks them up for review, and AI-assisted PRs wait 2.47× longer than unassisted ones — even though once review begins, AI PRs are reviewed 2× faster." Source URL is a landing page, not the report.
- **suggestion:** Link to the specific published LinearB 2026 report (PDF or deep link) containing each statistic. Flag as [UNVERIFIED — high hallucination risk] if not obtainable.

### ACCURACY-011
- **severity:** high
- **dimension:** correctness
- **location:** research-cognitive-load-inversion.md:Cognitive Load — CodeRabbit stats
- **description:** "AI-authored code produced 10.83 issues per PR vs. 6.45 for human-only PRs" — the ratio is repeated (1.7x), consistent with real CodeRabbit blog claims, but the decimal precision of "10.83" and "6.45" is suspiciously specific. Also the "XSS vulnerabilities occur at 2.74× the rate" and "logic errors appear 75% more frequently" figures need primary-source corroboration.
- **evidence:** "The CodeRabbit State of AI vs. Human Code Generation Report (December 2025)... found AI-authored code produced 10.83 issues per PR vs. 6.45 for human-only PRs." and "Logic errors appear 75% more frequently; XSS vulnerabilities occur at 2.74× the rate."
- **suggestion:** Verify each precise figure in the actual CodeRabbit report. Flag any that don't appear verbatim.

### ACCURACY-012
- **severity:** high
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Follow-up Q2 — OpenSpec / Fission-AI
- **description:** Claim that OpenSpec ("Propose-Apply-Archive" loop) was "developed by Fission-AI." OpenSpec as a markdown-driven AI dev framework exists in the broader ecosystem but the attribution to "Fission-AI" is suspect — no public Fission-AI organization is associated with a markdown OpenSpec tool for AI development as described here. This may confuse distinct projects.
- **evidence:** "The OpenSpec 'Propose-Apply-Archive' Loop: This framework, developed by Fission-AI, uses a simple three-step cycle."
- **suggestion:** Verify Fission-AI attribution with repo/URL. Most likely either rename the attribution or mark [UNVERIFIED]. There is an OpenSpec project on GitHub, but authorship attribution to "Fission-AI" is unconfirmed.

### ACCURACY-013
- **severity:** high
- **dimension:** traceability
- **location:** research-spec-correct-value-zero.md:Circular AI Review — arxiv.org/html/2603.25773
- **description:** Multiple files cite arxiv IDs with prefixes 2602 and 2603 (e.g., 2602.00180v1, 2603.25773, 2603.20028, 2603.15911). arxiv IDs use YYMM format, so 2602 = Feb 2026 and 2603 = March 2026. These are plausibly real given today's date (2026-04-13), but specific numbers like 2603.25773 cannot be easily corroborated. The arxiv ID format allows up to 5-digit suffixes, but 2603.25773 (25,773rd paper of March 2026) is at the upper end of plausibility. Multiple papers with 2603.X numbers showing in one corpus raises hallucination concerns.
- **evidence:** Cited IDs: "arxiv.org/html/2602.00180v1", "arxiv.org/html/2603.25773", "arxiv.org/html/2603.20028", "arxiv.org/html/2603.15911v1", "arxiv.org/html/2512.20798v1", "arxiv.org/html/2510.09907v1".
- **suggestion:** Verify each arxiv ID resolves to the described paper. Any that return 404 should be flagged as hallucinated. The 2512.20798 ID (December 2025) and 2510.09907 (October 2025) are more plausible temporally.

### ACCURACY-014
- **severity:** high
- **dimension:** correctness
- **location:** research-acceptance-criteria-ai-literal.md:Property-Based Testing — NumPy Wald bug
- **description:** Claim that an agent found "a genuine bug in NumPy (numpy.random.wald sometimes returning negative numbers, violating the mathematical property of the Wald distribution)" cited to arxiv 2510.09907v1. The NumPy `random.wald` function's implementation details are well-scrutinized and such a bug would be notable. Without verification this appears plausible but unconfirmed. High-confidence-sounding specific bug report is a classic hallucination pattern.
- **evidence:** "finding a genuine bug in NumPy (numpy.random.wald sometimes returning negative numbers, violating the mathematical property of the Wald distribution) — a type of defect specification-based testing alone would not catch."
- **suggestion:** Verify the specific bug via NumPy issue tracker or the cited arxiv paper. If unverified, mark [UNVERIFIED].

### ACCURACY-015
- **severity:** high
- **dimension:** correctness
- **location:** research-ceremony-rhythm-alternatives.md:AWS AI-DLC — Enterprise customer claims
- **description:** Claim that AWS AI-DLC was "Adopted by enterprise customers (Wipro, Dun & Bradstreet) with reported 10-15x productivity gains." This is a specific customer list with a suspiciously convenient productivity multiplier. Without direct AWS case study citations, the 10-15x figure and specific company attribution are high-risk claims.
- **evidence:** "Adopted by enterprise customers (Wipro, Dun & Bradstreet) with reported 10-15x productivity gains."
- **suggestion:** Link to specific AWS case studies for Wipro and Dun & Bradstreet. If unavailable, flag multiplier as [UNVERIFIED].

### ACCURACY-016
- **severity:** medium
- **dimension:** correctness
- **location:** research-ceremony-rhythm-alternatives.md:OpenAI Harness Engineering
- **description:** Claim that OpenAI's Codex team "managed approximately 1,500 pull requests in five months — 3.5 PRs per engineer per day — against a ~1 million line codebase" cites an OpenAI blog post. The math doesn't quite reconcile: 1500 PRs / 5 months / ~30 days / team of 3-7 engineers = 1.4-3.3 PRs per engineer per day depending on the denominator. "3.5 PRs/engineer/day" implies ~3 engineers; consistency with "team of 3-7 engineers" is ambiguous. Even if the OpenAI post exists, the internal arithmetic here requires verification.
- **evidence:** "The team of 3-7 engineers managed approximately 1,500 pull requests in five months — 3.5 PRs per engineer per day"
- **suggestion:** Verify the OpenAI Harness Engineering post (openai.com/index/harness-engineering/) contains these exact figures; correct arithmetic if mis-stated.

### ACCURACY-017
- **severity:** medium
- **dimension:** correctness
- **location:** research-behavioral-validation-ai-agents.md:Synthetic User Simulation — Blok 87% fidelity
- **description:** Blok ($7.5M seed, July 2025) is cited as claiming "87% behavioral fidelity to real-world outcomes." The funding round is citable via TechCrunch, but the specific 87% fidelity metric is a marketing claim masquerading as a research figure. Source is a techcrunch.com URL — the article's actual contents and whether it includes this precise metric need verification.
- **evidence:** "They claim 87% behavioral fidelity to real-world outcomes."
- **suggestion:** Attribute 87% directly to Blok as a vendor claim, not as validated research. Verify the TechCrunch article contains this figure.

### ACCURACY-018
- **severity:** medium
- **dimension:** correctness
- **location:** research-behavioral-validation-ai-agents.md:Commercial AI QA — QA.tech stats
- **description:** "They claim 95% bug detection vs. 80% for traditional E2E, with 5-minute test setup vs. 8 hours." These are vendor marketing numbers with no methodology cited. Presenting as "they claim" is appropriate framing, but the credibility of these benchmarks is low and readers may absorb them as verified.
- **evidence:** "They claim 95% bug detection vs. 80% for traditional E2E, with 5-minute test setup vs. 8 hours."
- **suggestion:** Annotate as vendor marketing claim, not independently verified.

### ACCURACY-019
- **severity:** medium
- **dimension:** correctness
- **location:** research-cognitive-load-inversion.md:Core dynamic — 98% more PRs / 91% review time
- **description:** "Developers using AI complete 21% more tasks and merge 98% more PRs — but PR review time increases 91% in the same period" attributed to newsletter.eng-leadership.com. These figures match real industry reporting in late 2025 but may have been misquoted. The 98% PR increase is particularly high.
- **evidence:** "Developers using AI complete 21% more tasks and merge 98% more PRs — but PR review time increases 91% in the same period."
- **suggestion:** Verify each percentage against the primary source (newsletter post and upstream research it cites).

### ACCURACY-020
- **severity:** medium
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Sources — PR Newswire AI/works
- **description:** Thoughtworks' AI/works is referenced multiple times as a real product launched in 2026. Thoughtworks has announced ai/works-type offerings (research confirms some public mentions), but the trademark notation "AI/works™" throughout and specific claims (e.g., generating "Super-Specs") should be verified against the actual Thoughtworks product launch.
- **evidence:** Multiple mentions of AI/works™ with specific features (legacy reverse-engineering, Super-Spec generation). Source is prnewswire.com generic URL.
- **suggestion:** Provide the specific PR Newswire URL/date; quote directly from Thoughtworks product announcement.

### ACCURACY-021
- **severity:** medium
- **dimension:** correctness
- **location:** research-behavioral-validation-ai-agents.md:Anthropic — Bloom open source
- **description:** Claim that "Anthropic's open-source tool Bloom (2025) implements automated behavioral evaluations at scale." Anthropic has published a tool called "Petri" and other eval work, but "Bloom" is not a widely-recognized Anthropic open-source eval tool as of known 2025 releases. The Sources link (anthropic.com/research/bloom) should be independently verified. This may be confused with unrelated "Bloom" projects (BigScience BLOOM LLM; Google's Bloom tool, etc.).
- **evidence:** "Anthropic's open-source tool Bloom (2025) implements automated behavioral evaluations at scale, applying LLM-based scoring to real interaction transcripts."
- **suggestion:** Verify existence of Anthropic Bloom tool. If nonexistent or confused with another project, correct.

### ACCURACY-022
- **severity:** medium
- **dimension:** correctness
- **location:** research-feature-unit-user-value.md:DORA 2025 — seven archetypes
- **description:** Claim that "Performance tiers were replaced by seven archetypes" in the 2025 DORA report. The 2024 DORA report introduced five archetypes (harmonious, stable, balanced, constrained, legacy); whether 2025 introduced "seven archetypes" specifically needs verification. The "renamed from 'State of DevOps' to signal a shift in focus" claim is correct (now "State of AI-Assisted Software Development"), but the archetype count needs checking.
- **evidence:** "Performance tiers were replaced by seven archetypes. New dimensions were added including team performance, product performance, friction, and burnout."
- **suggestion:** Verify archetype count against the 2025 DORA report PDF. If count is wrong, correct.

### ACCURACY-023
- **severity:** medium
- **dimension:** traceability
- **location:** research-spec-correct-value-zero.md:MIT Project NANDA 95% failure
- **description:** "The MIT Project NANDA finding that 95% of corporate AI projects show no measurable return" — this finding is real (MIT State of AI in Business 2025, Project NANDA, widely reported), but here it is casually cited without a URL in Sources. The finding itself is also frequently misquoted as "95% of corporate AI projects fail" when the original says 95% show zero P&L impact.
- **evidence:** "The MIT Project NANDA finding that 95% of corporate AI projects show no measurable return suggests the spec-to-value problem is widespread"
- **suggestion:** Add a direct MIT Project NANDA URL in Sources; clarify exact framing (no measurable return vs. failure).

### ACCURACY-024
- **severity:** low
- **dimension:** correctness
- **location:** research-cognitive-load-inversion.md:Vibe coding — Collins Word of the Year
- **description:** Claim "'vibe coding' — coined by Andrej Karpathy in February 2025 and named Collins English Dictionary Word of the Year 2025" — Karpathy's coinage in February 2025 is correct. Collins Dictionary did announce "vibe coding" as its 2025 Word of the Year. This claim is plausibly correct but the specific attribution to Collins (not Oxford or Merriam-Webster) should be double-checked; Oxford announced "brain rot" for 2024 and various dictionaries made different picks for 2025.
- **evidence:** "coined by Andrej Karpathy in February 2025 and named Collins English Dictionary Word of the Year 2025"
- **suggestion:** Confirm Collins specifically (not another dictionary) named vibe coding Word of the Year. Likely correct but worth a quick verify.

### ACCURACY-025
- **severity:** low
- **dimension:** logical_soundness
- **location:** gemini-deep-research-output.md:Casey West Agentic Manifesto — cross-file inconsistency
- **description:** The "Agentic Manifesto" by Casey West is characterized differently across files. The gemini file says it was "Proposed in early 2026 as a direct response to Agile friction" and "Advocates for a clean break from 'human-pacing' by shifting focus from verification... to validation." The research-thought-leader-frameworks file correctly dates it to 2025 and describes it as ADLC (Agentic Delivery Lifecycle) wrapping SDLC, NOT a clean break. The gemini file's framing is inconsistent with the primary caseywest.com source as documented in the thought-leader file.
- **evidence:** Gemini file: "The 'Agentic Manifesto,' proposed by Casey West in early 2026..." vs. thought-leader file: "Casey West's Agentic Manifesto (2025) proposes an Agentic Delivery Lifecycle (ADLC) as a wrapper around the traditional SDLC [PRAC — caseywest.com, 2025]. It does not replace SDLC but adds a governance layer..."
- **suggestion:** Reconcile the dating (2025 vs early 2026) and the positioning (clean break vs SDLC wrapper). The 2025 dating and SDLC-wrapper framing appears to be the authoritative one.

---

## Patterns Observed

1. **Gemini output file is the primary hallucination vector.** The gemini-deep-research-output.md file contains the highest density of suspicious named frameworks ("3-3-3", "V-Impact Canvas", "Kinetic Enterprise doctrine", "BMAD Quick Flow/Barry", "Silken Net", "Architect of Intent") and the most vague Sources list (bare domain references rather than specific URLs). Claims in this file should receive the highest scrutiny.

2. **Subagent files are generally better-sourced** with per-claim URLs, but still include suspiciously precise statistics (CodeRabbit 10.83 vs 6.45, LinearB 5.3x/2.47x, CAISI 0.1%/4.8%).

3. **Future-dated arxiv IDs (2602.X, 2603.X)** cluster around February-March 2026 papers. Given the document date of 2026-04-13, these could be real but cannot be verified without external lookups. Four distinct 2603.X papers in the corpus is mildly elevated risk.

4. **Cross-file inconsistencies** (Casey West Agentic Manifesto dating; Thoughtworks AI/works features) suggest at least one file absorbed hallucinated content while another used better sources.

5. **Vendor marketing numbers are frequently presented as research findings** (QA.tech 95% vs 80%, Blok 87% fidelity, Percy 40% noise filtering, AWS AI-DLC 10-15x gains).

---

## Recommended Remediation Priority

1. **Critical findings (001-003):** These appear to be fabricated frameworks/attributions. Excise or definitively source before using corpus for downstream work.
2. **High findings (004-015):** Verify each against primary sources; mark [UNVERIFIED] where primary source cannot be reached.
3. **Medium findings (016-023):** Tighten citations, clarify vendor claims vs research findings.
4. **Low findings (024-025):** Minor cleanups for consistency and attribution precision.
