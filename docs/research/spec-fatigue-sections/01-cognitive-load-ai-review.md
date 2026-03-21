# Section 1: Cognitive Load in AI Review Loops

## 1.1 BCG "AI Brain Fry" Study (March 2026)

**Citation:** Bedard, J., Kropp, M., Hsu, M., Karaman, O., Hawes, J., & Kellerman, G. (2026). "When Using AI Leads to 'Brain Fry.'" *Harvard Business Review*, March 2026. Also published via BCG.

**Methodology:** Survey of 1,488 full-time U.S. workers at large companies (48% male, 51% female; 58% individual contributors, 41% leaders). Measured AI usage patterns, work experiences, cognition, and emotional outcomes. Participants self-reported whether they experienced "mental fatigue from excessive use or oversight of AI tools beyond cognitive capacity."

**Key Quantitative Findings:**

- **Prevalence:** 14% of AI-using workers reported AI brain fry. Marketing roles: 26%. Legal roles: 6%. Also high in people operations, engineering, finance, and IT.
- **High AI oversight** (reviewing/interpreting LLM output vs. autonomous agent tasks): **14% more mental effort**, **12% more mental fatigue**, **19% greater information overload**.
- **Decision fatigue:** 33% higher among those experiencing brain fry.
- **Error rates:** 11% increase in minor errors, **39% increase in major errors**.
- **Attrition risk:** Intent to quit rose from 25% to 34% (a 39% relative increase).
- **Tool concurrency threshold:** Productivity gains peaked at 2-3 simultaneous AI tools, then declined beyond 3.
- **Burnout reduction:** 15% lower burnout when AI replaces routine/repetitive tasks (vs. oversight-heavy tasks).

**Mitigation findings:** Manager support correlated with 15% lower mental fatigue. Work-life balance messaging: 28% lower fatigue. Unclear AI strategy: 12% higher fatigue.

**Recommendations:** Cap human-agent oversight at 3 agents; redesign jobs to distinguish AI-replacing-routine from AI-requiring-oversight; build skills in problem framing and strategic prioritization over output review; monitor cognitive load as a workplace risk metric.

**Relevance to spec fatigue:** The study directly quantifies the cost of reviewing AI-generated output. The 14% more mental effort for oversight tasks (reading and interpreting LLM text) maps precisely to the agentic workflow pattern of reviewing generated specs, stories, and code. The 3-tool concurrency ceiling and the 39% major error increase indicate that sustained review degrades quality nonlinearly.

**Sources:**
- [When Using AI Leads to "Brain Fry" (HBR)](https://hbr.org/2026/03/when-using-ai-leads-to-brain-fry)
- [BCG: When Using AI Leads to Brain Fry](https://www.bcg.com/news/5march2026-when-using-ai-leads-brain-fry)
- [Fortune: 'AI brain fry' is real](https://fortune.com/2026/03/10/ai-brain-fry-workplace-productivity-bcg-study/)

---

## 1.2 METR Developer Productivity Study (July 2025)

**Citation:** METR. (2025). "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity." Published July 10, 2025. arXiv: 2507.09089.

**Methodology:** Randomized controlled trial. 16 experienced open-source developers recruited from large repositories (averaging 22,000+ stars, 1M+ lines of code, with years of contribution history). Developers provided 246 real issues (bug fixes, features, refactors) from their own repositories, averaging ~2 hours each. Issues were randomly assigned to AI-allowed or AI-disallowed conditions. Developers recorded screens and self-reported times. Compensation: $150/hour. Primary AI tool: Cursor Pro with Claude 3.5/3.7 Sonnet. Statistical analysis used clustered standard errors.

**Key Quantitative Findings:**

- **Actual effect:** Developers took **19% longer** to complete issues when allowed to use AI tools.
- **Pre-study prediction:** Developers expected AI would speed them up by **24%**.
- **Post-study belief:** After experiencing the slowdown, developers still believed AI had sped them up by **20%**.
- **Perception gap:** A ~39 percentage-point disconnect between perceived and actual productivity.

**Explanations for the slowdown (five factors identified):**

1. **Over-optimistic deployment:** Developers used AI on tasks they could complete faster independently, then spent significant time cleaning up AI-generated code.
2. **Expert developer constraints:** Participants averaged 5 years and 1,500 commits in their codebases, leaving little room for AI to accelerate already-expert performance.
3. **Large codebase complexity:** Repositories with implicit conventions, undocumented rules, and complex dependency graphs are poor environments for current AI tools.
4. **High quality standards:** "Pure software" projects (compilers, libraries) maintain higher quality bars where AI output requires more extensive revision.
5. **Significant idle time:** AI-assisted sessions showed cognitive load redistribution rather than actual time savings -- developers spent time waiting for, reviewing, and correcting AI output.

**Relevance to spec fatigue:** The METR study is the strongest empirical evidence that AI review overhead can exceed AI generation gains. The 39-point perception gap is particularly important: developers cannot self-assess the cost of review. This directly undermines the assumption that "approval is cheap." If experienced developers believe they are faster while actually being slower, they will not voluntarily adopt mitigation strategies.

**Sources:**
- [METR: Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- [arXiv: 2507.09089](https://arxiv.org/abs/2507.09089)
- [Sean Goedecke: METR's AI productivity study is really good](https://www.seangoedecke.com/impact-of-ai-study/)
- [Domenic Denicola: My Participation in the METR Study](https://domenic.me/metr-ai-productivity/)

---

## 1.3 Faros AI Productivity Paradox Report (June 2025)

**Citation:** Faros AI. (2025). "The AI Productivity Paradox." Research report, June 2025.

**Methodology:** Observational study of over 10,000 developers across 1,255 teams. Data integrated from task management systems, IDEs, static code analysis tools, CI/CD pipelines, version control systems, incident management systems, and HR metadata. Covered up to two years of history, aggregated by quarter. Used Spearman rank correlation. Reported metrics from 6+ companies with statistically significant correlations (p < 0.05).

**Key Quantitative Findings:**

- **Individual output:** Developers on high-AI-adoption teams touch **9% more tasks** and **47% more PRs** daily.
- **Team output:** High-AI teams complete **21% more tasks** and merge **98% more PRs**.
- **PR review time:** Increases **91%** on AI-using teams.
- **PR size:** **154% increase** in average PR size.
- **Bug rate:** **9% increase in bugs per developer**.
- **Organizational impact:** No significant correlation between AI adoption and improvements at the company level.

**The review bottleneck cascade:** The study explicitly invokes Amdahl's Law -- AI-driven coding gains evaporate when review, testing, and release pipelines cannot match the new velocity. The system moves only as fast as its slowest link.

**Relevance to spec fatigue:** The 91% increase in PR review time is the quantitative smoking gun for review bottleneck. Combined with 154% larger PRs and 9% more bugs, the cognitive demand on reviewers compounds. The null finding at the organizational level confirms that generation speed without review capacity produces no net gain.

**Sources:**
- [Faros AI: The AI Productivity Paradox Research Report](https://www.faros.ai/blog/ai-software-engineering)
- [Faros AI: AI Productivity Paradox](https://www.faros.ai/ai-productivity-paradox)
- [AI Code Review Bottleneck Kills 40% of Productivity (byteiota)](https://byteiota.com/ai-code-review-bottleneck-kills-40-of-productivity/)

---

## 1.4 Academic Foundations

### 1.4a Vigilance Decrement (Sustained Attention Literature)

**Foundational citation:** Mackworth, N. H. (1948). "The Breakdown of Vigilance During Prolonged Visual Search." *Quarterly Journal of Experimental Psychology*, 1(1), 6-21.

**Recent review:** Hemmerich, K., Luna, F. G., Martín-Arévalo, E., & Lupiáñez, J. (2025). "Understanding Vigilance and Its Decrement: Theoretical, Contextual, and Neural Insights." *Frontiers in Cognition*.

**Key findings:**
- Detection accuracy shows a **steep drop within the first 30 minutes** of monitoring, followed by a more gradual decline (Mackworth's clock test).
- Significant vigilance decrement can emerge **within 10-15 minutes** under high-demand conditions, per the broader sustained attention literature.
- Performance loss manifests as both **slower reaction times** and **reduced detection accuracy**.
- The locus coeruleus-norepinephrine (LC-NE) system governs vigilance; both under- and over-activation impair performance (inverted-U relationship).
- Mind-wandering increases with time-on-task, correlating with decreased accuracy and increased response time variability.
- Two distinct vigilance types are affected differently: arousal vigilance (automatic) and **executive vigilance** (voluntary attention, high cognitive control) -- the latter maps directly to spec/code review.

**Relevance:** Reviewing AI-generated specs and code is an executive vigilance task -- it requires sustained voluntary attention to detect errors in largely correct-looking output. The 10-30 minute decrement window means that review sessions beyond this threshold will miss progressively more defects.

### 1.4b Code Review Effectiveness (Cisco/SmartBear Study)

**Citation:** Cohen, J., Brown, E., DuRette, B., & Teleki, S. (2006). *Best Kept Secrets of Peer Code Review.* SmartBear Software. Based on analysis at Cisco Systems.

**Methodology:** 10 months analyzing 2,500 code reviews covering 3.2 million lines of code at Cisco Systems.

**Key findings:**
- Optimal review: **200-400 LOC** over **60-90 minutes** yields **70-90% defect discovery**.
- Inspection rates below **300 LOC/hour** yield best defect detection; above **450 LOC/hour**, defect density falls below average in **87% of cases**.
- **Total review time should not exceed 60-90 minutes** -- defect detection rates plummet after that.
- Average: 32 defects per 1,000 LOC; 61% of reviews found no defects.

**Relevance:** AI-generated PRs averaging 154% larger (Faros AI data) directly violate the 200-400 LOC optimal window. If AI generates 800+ line PRs, reviewers face both size overload and time-on-task degradation simultaneously. The 87% below-average detection at speeds above 450 LOC/hour means rushed reviews of large AI PRs will miss the majority of defects.

### 1.4c Cognitive Offloading and Skill Degradation

**Citation:** Shen, J. H. & Tamkin, A. (2026). "How AI Impacts Skill Formation." arXiv: 2601.20245. Anthropic Research.

**Methodology:** Randomized experiment with 52 (mostly junior) software engineers learning the Trio async I/O library (a Python library they had not used before). Compared AI-assisted vs. unassisted coding, measuring both task completion and comprehension via quiz.

**Key findings:**
- AI-assisted developers scored **17% lower** on comprehension quizzes (50% vs. 67%).
- Six distinct AI interaction patterns identified: three that preserve learning, three that degrade it.
- Three low-engagement patterns (**AI Delegation**, **Progressive AI Reliance**, **Iterative AI Debugging**): fastest completion, poorest understanding (averaging below 40% quiz scores).
- Three high-engagement patterns (**Generation-Then-Comprehension**, **Hybrid Code-Explanation**, **Conceptual Inquiry**): preserved understanding (averaging 65%+ quiz scores).
- The decisive factor was not AI use itself but **how** participants engaged -- active questioning and comprehension effort preserved cognition, passive delegation degraded it.

**Relevance:** In agentic workflows, the human's role is structurally the delegation/review pattern -- the agent generates, the human approves. This is precisely the interaction mode shown to produce the weakest conceptual understanding. Over time, reviewers who approve AI output without deep engagement lose the domain knowledge needed to evaluate quality, creating a compounding degradation loop.

### 1.4d Decision Fatigue in Approval Workflows

**Key reference:** Danziger, S., Levav, J., & Avnaim-Pesso, L. (2011). "Extraneous Factors in Judicial Decisions." *Proceedings of the National Academy of Sciences*, 108(17), 6889-6892.

**Finding:** Judges' parole approval rates peaked after breaks and dropped sharply as decision fatigue accumulated -- demonstrating that sequential approval decisions degrade in quality over time, independent of case merit.

**Application:** Each spec review, story approval, or PR sign-off in an agentic workflow is a sequential approval decision. The judicial decision fatigue research predicts that approval quality will degrade across a session, with later reviews receiving less scrutiny than earlier ones.

---

## 1.5 Compounding Problem Summary

Synthesizing across studies, the evidence converges on specific thresholds:

| Metric | Threshold | Source |
|---|---|---|
| Vigilance decrement onset | 10-15 minutes (high demand) | Sustained attention literature |
| Steep accuracy drop | 30 minutes | Mackworth (1948) |
| Optimal code review duration | 60-90 minutes max | Cisco/SmartBear |
| Defect detection collapse at speed | >450 LOC/hour, 87% below-average | Cisco/SmartBear |
| Optimal review size | 200-400 LOC | Cisco/SmartBear |
| AI-generated PR size increase | 154% larger than human PRs | Faros AI |
| AI-generated code issue rate | 1.7x more issues per PR | CodeRabbit (Dec 2025) via byteiota |
| PR review time increase with AI | 91% longer | Faros AI |
| Major error increase under AI brain fry | 39% | BCG (2026) |
| Perception-reality gap | 39 percentage points | METR (2025) |

**The compounding problem for agentic workflows:** AI generates more output (154% larger PRs, 47% more PRs/day), each requiring more review effort (91% longer reviews, 1.7x more issues), while the reviewer's capacity declines over time (10-30 minute vigilance decrement, decision fatigue across sequential approvals), and the reviewer cannot accurately self-assess their degradation (39-point perception gap). This creates a structural trap where the human review gate -- intended as a quality safeguard -- becomes progressively less effective precisely as volume increases.

---

## Sources

1. Bedard et al. (2026). "When Using AI Leads to Brain Fry." HBR/BCG.
2. METR (2025). "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity." arXiv: 2507.09089.
3. Faros AI (2025). "The AI Productivity Paradox." Research report.
4. Shen & Tamkin (2026). "How AI Impacts Skill Formation." arXiv: 2601.20245. Anthropic.
5. Cohen et al. (2006). "Best Kept Secrets of Peer Code Review." SmartBear/Cisco.
6. Mackworth (1948). "The Breakdown of Vigilance During Prolonged Visual Search." QJEP.
7. Hemmerich, Luna, Martín-Arévalo, & Lupiáñez (2025). "Understanding Vigilance and Its Decrement." Frontiers in Cognition.
8. Danziger, Levav, & Avnaim-Pesso (2011). "Extraneous Factors in Judicial Decisions." PNAS.
