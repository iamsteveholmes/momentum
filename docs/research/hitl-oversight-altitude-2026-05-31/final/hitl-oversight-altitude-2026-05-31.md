---
title: "The HITL Sweet Spot — Decision Altitude & Review Granularity in Agentic AI"
date: 2026-05-31
type: Technical Research — Consolidated Report
status: Complete
content_origin: claude-code-synthesis
human_verified: false
derives_from:
  - path: raw/workflow-findings.json
    relationship: synthesized_from
  - path: raw/gemini-deep-research-output.md
    relationship: synthesized_from
  - path: raw/gemini-sources.md
    relationship: synthesized_from
  - path: raw/research-sq7-junior-employee-analogy.md
    relationship: synthesized_from
  - path: validation/verify-sq7-junior-employee-analogy.md
    relationship: validated_by
  - path: scope.md
    relationship: scoped_by
---

# The HITL Sweet Spot — Decision Altitude & Review Granularity in Agentic AI

> Evidence notation used throughout: **[OFFICIAL]** vendor/primary-doc or peer-reviewed and verified · **[PRAC]** practitioner/community source with a URL · **[UNVERIFIED]** inferred or weakly sourced · **SUSPECT** flagged by the adversarial verification layer (verdict unsupported/contradicted/outdated, training-data smell, or low reliability). Quantitative claims carry source + date inline.

## Decision Brief

**The posture is defensible — with two hard exceptions.** Treating the LLM like a trusted junior (scan output for high-level issues, converse in principles and summaries, trust sound low-level decisions) is the documented 2025–2026 working practice of named senior engineers (Osmani, 2026-01-04 [PRAC]; Goedecke, 2026-05-17 [PRAC]) and matches how the industry now places oversight. But "trusted" must mean *calibrated*, not *graduated*: an LLM does not learn across sessions the way a junior does, so trust resets each task rather than compounding. And the altitude is set by **stakes**, not by the agent's apparent competence.

**(a) Decide vs. delegate — by reversibility and blast radius.** Both research engines converge on the one-way-door / two-way-door axis as the primary lens (Theory Ventures, 2026-04-13 [PRAC]; Gemini). *You* own irreversible, security-sensitive, wide-blast, regulated, or architecture-defining decisions. *Delegate* bounded, reversible, version-controlled, verifiable work — which is exactly what professional developers already do (Anthropic's "delegation gap": ~60% AI use but only 0–20% full delegation, attributed to judgment not capability — Anthropic 2026 Agentic Coding Trends Report [OFFICIAL]).

**(b) How much review — review intent, not syntax.** The evidence is strong against line-by-line reading of large AI diffs *as the default*: it is the cognitive task that the "verification tax" makes expensive, and the field's real failure is the opposite extreme — 38–61% of agent PRs merge with no recorded human review (MSR/EASE 2026 [OFFICIAL]). Review the **plan** before code and the **behavior** (tests against the spec) after. Reserve exhaustive line-by-line review for the two exceptions: **irreversible state changes** (schema/data migrations, destructive ops) and **security/auth/tenant-isolation logic** — where AI is empirically worse (CodeRabbit: 1.7× more issues, 2.74× more XSS, 2025-12-17 [OFFICIAL]) and the failure passes happy-path tests.

**(c) Decision-grade communication is achievable but is NOT the default.** Use measurable constraints (word/section caps, "executive summary first"), persona + audience framing, plan-before-code gating, and progressive disclosure (summary with detail on demand). Vendor knobs help — OpenAI `verbosity`, Gemini `thinking_level`, Claude `effort` — but the cross-vendor "models are terse by default now" claim is **SUSPECT** (contradicted by YapBench, 2026-01, which found 2025–26 models *more* verbose on average). You must steer explicitly; do not assume.

| Artifact / decision type | Stakes & reversibility | Oversight altitude | Human action |
|---|---|---|---|
| Architecture / design decision | High, shapes everything downstream | **Decide-it** | You make the call; agent advises and drafts options |
| Irreversible / destructive op (schema migration, data delete, force-push, prod deploy) | Critical, one-way door | **Review line-by-line** | Block-gate; verify rollback/compensating action exists |
| Security / auth / tenant-isolation code | Critical, fails silently | **Review line-by-line** | Block-gate; adversarial check; verify defensive posture |
| Core business-logic / API feature code | Medium, two-way door (git) | **Review at behavior level** | Approve plan first; review the tests that prove the spec, not every line |
| A plan / spec | Medium — cheap to change, sets direction | **Review at behavior level** | Read decision-grade summary; approve intent, scope, trade-offs |
| Routine CRUD / scaffolding / unit tests / docs | Low, two-way door | **Spot-check** | Sample; lean on CI/static analysis/type-checks for syntax |
| Exploratory research, log parsing, sandbox prototype | Low, fully reversible | **Trust + monitor** | Read final output async; intervene only if needed |

*Bottom line: keep the junior posture for delegation and communication; drive review depth from stakes; never let a confident summary substitute for line-by-line review where the door is one-way.*

## Executive Summary

This report consolidates two independent research engines on a single question: where should a human make decisions versus delegate to an LLM, and how exhaustively must a human review LLM output (plans, code, specs, designs)? The framing under test is the developer's mental model — working with an LLM like a senior works with a trusted junior. The investigation covered eight sub-questions: autonomy/delegation frameworks, risk-calibrated oversight, reviewing AI-generated artifacts, plan-review altitude, making LLMs communicate at the right altitude, trust-calibration failure modes, the junior-employee analogy, and operationalizing HITL gates.

**Method.** Engine one was a Claude dynamic workflow: eight parallel web-discovery agents (recency-mandated to 2025–2026, every claim traced to a fetched source), each adversarially fact-checked by an independent skeptic agent that re-fetched load-bearing claims and hunted for contradicting evidence. Engine two was an independent Gemini Deep Research report (Gemini Pro) on the same eight questions, used for triangulation. Where the two agree, confidence is high; where they diverge or where the verification layer flagged a claim, this report surfaces it as qualified or open rather than settled.

**Headline findings.** (1) The 2026 consensus is real and cross-engine: oversight altitude is a designable, graduated property keyed to **reversibility and blast radius**, not a binary, and the right move is to shift human attention *left* (to the plan/spec) and *right* (to behavior/tests), away from line-by-line syntax. (2) The single most robust empirical fact is the relocation of the bottleneck from writing to reviewing — the "verification tax" — and the field's dominant *real-world* failure is under-review (silent unreviewed merges), not over-review. (3) AI code is empirically more defect- and security-prone, which makes security/irreversibility the carve-out where exhaustive review still pays. (4) The junior analogy holds as a *delegation and communication posture* but breaks on cross-session learning, calibration, jagged capability, and accountability — the human stays 100% accountable. (5) Decision-grade communication is engineerable through measurable constraints, persona framing, plan-gating, and progressive disclosure, but is not the model's default and must be steered.

**Reliability and divergence.** Overall corpus reliability is **medium-to-high**: SQ1 verified high; the rest medium, dragged down not by wrong conclusions but by single-vendor framings dressed as industry consensus and a handful of misattributed or stale statistics. The two engines agree on every core conclusion. They diverge mainly in that Gemini repeats two specifically-flagged weak claims (the un-caveated METR "19% slower" and the JetBrains "20–25%/44% hallucination split") and includes several vivid but unverifiable named artifacts (a Microsoft "Council"/"Claude Mythos"/"GPT-5.4" feature, "NextAds", "VibeSec", "OpenClaw") that the Claude corpus does not corroborate. Those are noted at each point of use.

**Who it's for.** A solo developer running an LLM-orchestrated engineering practice (Momentum) who needs to know where to place HITL gates, what to always read line-by-line versus trust, and how to get decision-grade output by default.

---

## 1. Autonomy & Delegation Levels — Decision Altitude

**Both engines converge on a graduated, SAE-driving-levels-style ladder, keyed to the human's role.** The strongest academic anchor is Feng, McDonald & Zhang (arXiv 2506.12469 / Knight Columbia, 2025-07-28 [OFFICIAL], verified), which defines five levels by the human's role — **Operator → Collaborator → Consultant → Approver → Observer** — and argues autonomy is "a deliberate design decision, separate from its capability and operational environment." Gemini independently surfaces the same Knight Columbia role framing (operator/collaborator/consultant/approver/observer) and the CSA L0–L5 taxonomy (No Autonomy → Assisted → Supervised → Conditional → High → Full; CSA, 2026-01-28 [OFFICIAL], verified verbatim including "I don't believe Level 5 is appropriate for enterprise deployment today"). This is a high-confidence, triangulated foundation.

**Coding-specific ladders add the decision-altitude mapping.** Swarmia's five levels (Assistive/Conversational/Task Agent/Autonomous Teammate/Agentic Avalanche; 2026-03-19 [PRAC], verified) argue "higher is not always better" — match the level to task ambiguity and verifiability, with most teams' ceiling at Levels 2–3. ASDLC's L1–L5 pairs each level with a human role: Driver → Reviewer → Change Owner → Auditor → Consumer (2026-05-28 [PRAC], low-authority self-published, verified-but-illustrative).

**Task vs. goal delegation is the operational crux, and both engines name it.** Gemini frames the sweet spot as "goal delegation within a Level 2/3 (Supervised/Conditional) altitude" — the human specifies the *what* and *why* and evaluates the plan; the agent owns the *how*. The Claude corpus corroborates with Huang et al. (arXiv 2512.14012, 2025-12-17 [OFFICIAL], abstract-confirmed): professional developers "retain their agency in software design and implementation out of insistence on fundamental software quality attributes." (Caveat: the specific "bounded tasks / architectural decisions" quote strings were not located in the abstract — possible paraphrase-as-quote; **SUSPECT** on wording, not on thesis.)

**Calibrated, not blind, trust — and a key qualifier.** Anthropic's Claude Code telemetry (2026-02-18 [OFFICIAL], all numbers verified) shows experienced users raising auto-approval (~20% → >40%) *and* interrupt rate (5% → 9%) simultaneously — read as a HITL→HOTL migration driven by calibration. **SUSPECT framing:** the verification layer flags that the *same* telemetry is consistent with the competing 2026 "HITL theater / oversight illusion" thesis (MIT Technology Review, 2026-04-16) — rising interrupts could mean users catch *more* problems, not that they trust *better*. The numbers are solid; the "calibrated trust" causal gloss is contestable.

**The delegation gap.** Anthropic's 2026 Agentic Coding Trends Report [OFFICIAL]: developers use AI in ~60% of work but fully delegate only 0–20% of tasks — "the problem isn't capability, it's judgment." (The Claude corpus initially cited a secondary blog; the primary Anthropic report is the better source, and the figure is corroborated across 5+ write-ups. A rival explanation — Osmani's "comprehension debt" — is omitted by the single-cause framing.)

**Open tension:** terminology has *not* converged. Beyond the ladders catalogued, several more incompatible L0/L1–L5 frameworks circulate in 2026; the SAE-J3016 analogy that both engines lean on is itself critiqued in 2026 as leaky (non-linear capability gains, a decade of slipped self-driving "level" promises). Treat "the levels" as a useful shared vocabulary, not a settled standard.

---

## 2. Risk-Calibrated Oversight — Reversibility & Blast Radius

**The central, strongly-triangulated finding: review depth scales with stakes decomposed into reversibility, blast radius, security exposure, and cost of error.** Both engines lead with Amazon's **one-way-door / two-way-door** framing applied to agent tool calls. Theory Ventures (2026-04-13 [PRAC], verified): "software development is made up entirely of systems that make decisions more reversible" (git, code review, transactions, observability) — which is *why* agents work in software — and "for one-way doors no amount of additional verification is excessive." Gemini independently builds its entire section 2 on this exact axis.

**The best primary evidence is a shipped product, not a framework.** Anthropic's Claude Code Auto Mode (2026-03-25 [OFFICIAL], the strongest-verified claim in the corpus): reads and version-controlled in-project edits run freely *because they're reversible via git*; a transcript classifier gates 20+ high-downside categories (force-push, mass deletion, exfiltration, prod deploys), checks intent ("clean up my branches" does not authorize batch deletion), and escalates after 3 consecutive / 20 total denials. Reported 0.4% false-positive vs **17% false-negative** rate on dangerous actions. Gemini's parallel — the "Saga pattern": every mutating step needs a registered compensating action, and only then can a workflow be treated as a two-way door — is a sound architectural complement, though presented by Gemini without a primary citation [UNVERIFIED on attribution, sound in principle].

**Empirical reality check (Claude corpus, verified).** METR's Frontier Risk Report (2026-05-19 [OFFICIAL]) found practitioners *already* loosen by stakes (~40% unrestricted permissions on low-stakes vs <20% high-stakes) but thorough review of low-stakes output is rare, and "we are not aware of any company imposing strict requirements about human oversight of agents" (Feb–Mar 2026). Deloitte: only ~21% of companies have a mature agent-governance model. The tiered-approval frameworks are **aspirational, not adopted**.

**The sharpest tension — security is a separate axis that can override reversibility.** Reversibility logic would spot-check reversible code; the code-review camp insists every line be read because AI code is 1.7× more issue-prone and 2.74× more XSS-prone (CodeRabbit 470-PR study, 2025-12-17 [OFFICIAL], verified — note the original thread mis-attributed this to a thin blog). Resolution: treat security exposure as orthogonal to recovery cost. A reversible *change* can still introduce an *irreversible breach*.

**SUSPECT / single-vendor framings to discount.** Several named patterns both engines repeat are one-vendor coinages dressed as canonical: Baytech's "Helmsman Pattern" + "Blast Radius Containment" with "cryptographic human approval" (single consultancy blog, aspirational); Strata's precise "15s/2min/15min" time-boxed lanes (one vendor's proposal, no evidence of use); Gemini's "Digital Applied Four-Gate Framework" (single vendor's thought-leadership). Use the *shapes* (tiered, time-boxed, reversibility-keyed); do not treat the specific numbers or names as standards.

**Regulatory floor — read carefully.** EU AI Act Article 14 mandates oversight "commensurate with risk, autonomy and context" and requires two-person verification only for biometric ID (in force 2026-08-02) [OFFICIAL on statutory text]. **SUSPECT:** the Claude corpus's claim that the Act "explicitly does NOT require per-decision human review" is the discovery agent's *interpretation*, not statutory text — and other governance readers (BearingPoint) read Art. 14(1) as *requiring* sign-off gates for consequential high-risk actions. Gemini leans harder on the regulatory-mandate reading (EU AI Act fines up to €35M / 7% turnover). Net: regulation pushes toward *more* substantive review in regulated domains than the voluntary practice METR observed.

---

## 3. Reviewing AI-Generated Artifacts — Every Line vs. Sampling

**Triangulated consensus: practitioners do not re-read every AI line; they review at the behavior/acceptance level backed by automated structural gates (static analysis, type-checking, tests), reserving human judgment for requirement fidelity, business logic, architecture, and consequence.** GitHub's official guidance (2026 [OFFICIAL], verified) is an 8-area multi-layered review — explicitly *not* line-by-line — flagging AI-specific pitfalls (hallucinated APIs, deleted/skipped tests). Simon Willison (2025-12-18 [PRAC], verified): "a computer can never be held accountable; that's your job as the human in the loop" — the committing human owns the output.

**The dominant empirical fact across both engines: the bottleneck moved to review (the "verification tax").** Faros AI telemetry on 10,000+ developers (2025-07-28 [OFFICIAL], verified): high AI adoption drove 154% larger PRs, 91% longer review times, 9% more bugs/developer. Even when 73.8% of AI review-bot comments were acted on, PR closure time rose 42%. Gemini reports the same dynamic and the same CodeRabbit defect multipliers — strong agreement.

**The real-world failure is under-review, not over-review (Claude corpus, peer-reviewed, strongly verified).** The 2026 MSR/EASE academic corpus is the most rigorous evidence here:
- 38–61% of agent PRs receive *no recorded human review* (Duma et al., EASE 2026: 61.38% [OFFICIAL]; Ehsani et al., MSR 2026: "Abandoned/Not Reviewed" = 38% of rejections, the top failure mode, vs only 3% "Incorrect Implementation" [OFFICIAL]).
- Humans intervene *less often* on agent PRs (52% vs 84% on human PRs) but at higher per-intervention cost (Khelifi et al., MSR 2026 [OFFICIAL]).
- AI code-review bots are noisy: 60.2% of agent-only-reviewed PRs fall in the lowest signal band; CRA-only PRs merge at 45% vs 68% human-reviewed (Chowdhury et al., MSR 2026 [OFFICIAL]).

This is the report's most important corrective to the developer's mental model: the danger in practice is **rubber-stamping**, not excessive auditing.

**Test-as-trust, with an irreducible human checkpoint.** Acceptance-criteria-driven TDD — humans define testable "done" before AI codes; tests validate the *spec*, not the implementation — is the crystallizing pattern. But the "tautological testing" risk (the same AI generating code *and* tests shares blind spots) makes a human business-logic checkpoint irreducible. (Caveat: the specific "85–90% vs 70–80% coverage" bars are an unsourced blog assertion — **SUSPECT** false precision; the *concept* is corroborated by arXiv 2603.25773.)

**Divergences and SUSPECT items.**
- **METR "19% slower"** appears in both engines as an anchor. It is **outdated/over-generalized**: METR's own 2026-02-24 follow-up found selection bias and now calls 19% a *lower bound*, redesigning the study; only the *expectation gap* generalizes. Gemini presents it un-caveated. (See SQ6, SQ7.)
- **JetBrains "20–25% of hallucinations detectable by static analysis / 44% escape"** is **unsupported** — a provenance failure: the cited arXiv 2409.20550 does not contain those numbers. Gemini does not use it; the Claude thread did. Drop it.
- **DORA 2025 throughput reversal:** AI is now positively linked to delivery *throughput* (reversing 2024) while still negatively linked to *stability*. Both engines kept the stability-negative half; the throughput-positive half is a material qualifier.
- A genuine 2026 expert minority (per the verification layer) still argues for careful per-line reading because logical failures hide under convincing AI code — so the behavior-level consensus is *softer* than "nobody reads every line."

---

## 4. Plan / Spec Review Altitude — Decision-Grade Summaries

**Strongly triangulated: humans should NOT review an agent's plan line-by-line; the agent should present a decision-grade summary with detail expandable on demand — progressive disclosure.** Anthropic codified the three-level model (name/description → full instructions → appendix; 2025-10-16 [OFFICIAL], verified) and Will Larson (2025-12-26 [PRAC]) and Addy Osmani (O'Reilly, 2026-02-20 [PRAC], verified) apply the same summary-first pattern to plans, where Plan Mode is a read-only approval gate before code. Gemini's entire section 4 is built on the identical "progressive disclosure" concept plus dual-track summaries — clean agreement.

**The most operationally concrete pattern: the "evidence pack."** StackAI [PRAC]: concise-by-default with expandable detail, "the difference between a 15-second approval and a 15-minute investigation," reframing the reviewer's job as *verify, not redo*. **SUSPECT:** this exact slogan is vendor marketing rhetoric, not measured data (and the original thread mis-dated the source). Gemini's parallel "judge model" / Microsoft "Council" dual-track concept is directionally aligned but the specific named feature ("Council" running "Claude Mythos" and "GPT-5.4" with a third judge model, 2.5× compute) is **[UNVERIFIED] / likely-confabulated** — it appears only in Gemini and is not corroborated anywhere in the Claude corpus or sources. Treat the *pattern* (parallel models + synthesis for the human) as plausible; treat the named product as unverified.

**The deeper insight both engines reach: the spec/intent — not the code/diff — is the correct unit of review.** Zietsman (arXiv 2603.25773, 2026-03-30 [OFFICIAL on existence], **SUSPECT on "peer-reviewed"** — it is a single-author preprint of three *hypotheses*): reviewing code-against-code is "structurally circular" because generator and reviewer reason from the same artifact; an executable spec provides the external correctness reference and moves the problem (Cynefin) from complex to complicated. Amazon Kiro operationalizes this — "the spec is the unit of work; code is what happens after you sign off on the spec."

**Risk-based gating decides where full detail is warranted:** confirm 100% at risk boundaries (irreversible, costly, regulated, high blast radius); sample or batch low-risk. GitHub's Andrea Griffiths (2026-05-07 [OFFICIAL], the most balanced source, verified) provides a 10-minute risk-ordered review framework but warns the counter-point plainly: **"judgment is the bottleneck, and that's fine"** — summaries can mask "subtle hallucinations" (compiles and passes tests but is wrong) and "agent abandonment."

**Open tension / contradicting evidence.** Spec-first gating is *not* universally beneficial: 2026 critiques (Kent Beck; "waterfall reborn") show it is high-overhead and quality-neutral on small/uncertain work (one cited test: 33 min + 2,577 lines of spec for 689 lines of code, no quality gain). And the vigilance-decrement literature warns that the "15-second approval" decision-grade summary is *exactly* the design that maximizes automation bias — a robust attention finding that "cannot be overcome with simple practice or instructions." Adopt decision-grade summaries *contextually* and pair them with forcing functions on high-stakes gates.

---

## 5. Making LLMs Communicate at the Right Altitude

**Three converging levers (both engines agree on the toolkit):** first-class API verbosity/effort parameters, default model behavior, and prompting/config patterns.

**Parameters (vendor docs, verified [OFFICIAL]).** OpenAI GPT-5 (2025-08-07) shipped a `verbosity` param (low/medium/high) *separate from* `reasoning_effort` — the key 2025 decoupling of how much a model *thinks* from how much it *says*; retained in GPT-5.5 as `text.verbosity` (default medium). Google Gemini 3 uses `thinking_level` (replacing `thinking_budget`; doc updated 2026-05-29). Anthropic Claude Opus 4.8 has **no** verbosity knob — it calibrates length to judged task complexity and exposes an `effort` parameter (low → max). **SUSPECT:** the Claude thread frames low/medium `effort` as a verbosity lever; the verification layer notes `effort` is a cost/intelligence/scope knob, *not* an output-verbosity knob, and Anthropic's docs keep them in separate sections and warn against under-thinking at low effort. Gemini's parameter inventory (OpenAI `reasoning_effort`; Anthropic `budget_tokens` 1,024–128,000; "ultracode" adaptive mode) overlaps but uses older/partly-garbled names (e.g., "Claude 3.7 Sonnet and Opus 4.8" together) — directionally right, specifics **[UNVERIFIED]**.

**Prompting principle (high-confidence, cross-engine).** "Be concise" underperforms *measurable* constraints — word/bullet/section counts, templates — and positive examples of good concision beat negative "don't" instructions (Claude API docs [OFFICIAL]). Both engines independently endorse the senior-briefing pattern: **persona + audience-level + length cap** ("Write for a senior business audience. Keep the answer under 400 words"). Claude Code "output styles" make this a persistent system-prompt setting. **SUSPECT (outdated):** the built-in style list is stale — current docs list four (Default, Proactive, Explanatory, Learning) and the `/output-style` command was deprecated; selection is now via `/config`. The marquee "word limits, bullet counts…" quote is third-party aggregation, not a verbatim vendor quote.

**The biggest cross-engine divergence in the whole report.** Gemini and the Claude thread both assert that the newest models are **terse by default**, so you steer *up* toward chattiness. This is **SUSPECT / contradicted**: YapBench (arXiv 2601.00624, 2026-01, 76 models) found the *opposite* population-level trend — 2025–26 models are on average *more* verbose than 2023–24 models ("length bias is getting worse, not better"); the worst over-generate 10–20×. The "terse-by-default" line is a per-vendor *marketing posture* about their latest flagship, not a measured cross-vendor fact. Corollary: verbosity-compensation persists *even under explicit conciseness instructions* (arXiv 2411.07858), and GPT-5's verbosity param has documented integration failures (Azure, LangChain). **Conclusion: you must steer altitude explicitly and verify it held; do not assume the model defaults to decision-grade.**

---

## 6. Trust Calibration — Automation Bias vs. Verification Fatigue

**Both failure modes are real; calibration (not maximizing or minimizing trust) is the target.**

**Under-reviewing.** Sonar (2026-01-08, 1,100+ devs [OFFICIAL], verified): 96% don't fully trust AI code, yet only 48% always verify it before committing — the "verification gap"/"verification debt" (term per AWS CTO Werner Vogels). The foundational mechanism is automation complacency: operators of constantly-high-reliability automation are ~50% less likely to detect failures, in *both* novices and experts, "not fixed by simple practice" (Parasuraman & Manzey, 2010 [OFFICIAL] — the "50%" figure is a body-of-paper stat, loosely attributed but the mechanism is solid). An Anthropic skill-formation RCT (2026-02 [OFFICIAL], verified) found full delegation cut comprehension ~17 points (50% vs 67%); code-delegators scored <40% vs ≥65% for conceptual users — skill atrophy is conditional on *how* AI is used, not adoption itself. Gemini's parallel (CSET 68–73% of AI code samples contained vulnerabilities; "76% believe AI code is more secure") reinforces the over-trust risk but those specific figures are single-engine **[UNVERIFIED]** here.

**Over-reviewing.** 38% of developers say reviewing AI code is harder than human code (a Sonar figure — **SUSPECT:** the Claude thread mis-attributed this to DORA; it is *contradicted* on the DORA page and confirmed via IT Pro). The resulting "density of work"/decision fatigue makes reviewers sloppy. Gemini adds a JetBrains "PR closure +42%" figure (directionally consistent with the verified 2024 study).

**Where the human adds most value (cross-engine agreement):** intent, business logic, architecture, security posture, compliance — *not* syntax. AI review is reliable mainly for mechanical/pattern defects (security signatures, null safety, style).

**Best mitigations (Claude corpus, verified [OFFICIAL]).** Trust-adaptive interventions fix *both* directions: counter-explanations at high trust + supporting-explanations at low trust yielded up to 38% less inappropriate reliance and a 20% accuracy gain; forced pauses reduce over-reliance (Srinivasan & Thomason, IUI 2026). Under-reliance is equally costly (at low trust, doctors reject correct AI 68% vs 40%). Specification-grounded review breaks the circular AI-reviews-itself loop. (The "90.9% adoption lift" sub-stat is **SUSPECT** — not locatable in the cited paper.)

**The productivity debate, honestly.** METR's RCT (19% slower) vs DORA 2025 (throughput up) vs a "modest gains" cluster (~10% real productivity gain at ~84–93% adoption). **The METR 19% figure is now outdated** — METR's 2026-02-24 follow-up found the *same* developers ~18% *faster* and is redesigning the study for selection bias. Only the **perception gap** (developers feel faster than measured) reliably survives — and that gap is itself the strongest argument for keeping a human review discipline, because confidence does not track correctness.

---

## 7. The "Junior Employee" Analogy — Validity & Limits

This sub-question has the richest evidence (a dedicated raw thread + verification). **The analogy is a useful delegation/communication *posture* but breaks on four load-bearing points** — and both engines agree on the structure of the breakage.

**What transfers (verified [PRAC]).** Leading 2026 practitioners explicitly adopt it: Osmani (2026-01-04) "I treat every AI-generated snippet as if it came from a junior developer: I read through the code, run it, and test it… I remain the accountable engineer"; Goedecke (2026-05-17) uses agents "constantly and with light supervision," makes a ~30-second initial assessment, and "most of the time I reject them entirely." The transferable management theory is genuine: Situational Leadership (Hersey-Blanchard: Tell/Sell/Participate/Delegate) and Appelo's 7 Levels of Delegation say *autonomy granted should match demonstrated readiness*. Gemini cites the same frameworks.

**Where it breaks (each verified against primary sources):**
1. **No cross-session learning.** A junior matures; the bare model starts fresh, so trust resets rather than graduates (Harris, 2026-04-29 [PRAC], verified: "no long-term memory… will face no legal liability"; "Amelia Bedelia and Leonard Shelby from Memento"). **Qualifier (verification layer):** this is true of the *bare* model but increasingly *false* of deployed agent *systems* with engineered memory (Mem0/MCP, AgeMem) — so "trust never compounds" is weaker than stated, though memory staleness/identity remain open. *(Both engines overstate this as a hard invariant.)*
2. **Confidently wrong with no calibration signal.** LLMs emit bugs "with complete conviction" (Willison via Osmani). The BCG/Mollick experiment: on an out-of-frontier task humans were right 84% unaided vs 60–70% *with* AI (foundational 2023, verified — dated as live evidence).
3. **Jagged, "alien" capability.** Google DeepMind's jaggedness paper (2026-01-27 [OFFICIAL], verified verbatim): Gemini 2.5 Pro is +1.99 SD on AIME math (~top 3%) but −1.02 SD on ARC-AGI-1 visual reasoning (~bottom 16%); jaggedness is "a structural property of current architectures" and "alien to our own." *(Caveat the paper itself notes: these numbers are "illustrative of the method," not a capability endorsement.)* You cannot extrapolate competence from one domain to another the way you can with a human.
4. **No accountability.** The human stays 100% accountable (Yamin, 2026-01-25 [PRAC] — vivid but **SUSPECT**: his "90% inflated false positives" and "mathematically unattainable" figures are second-hand citations inside a Medium opinion piece, not independently verified). Gemini's "Phantom Bugs"/"By-The-Book Fixation"/"insecure by dumbness" framings (Ox Security) are single-engine and **[UNVERIFIED]** but rhyme with the verified jaggedness/no-hygiene-reflex point.

**SUSPECT attributions:** the verification layer caught that a tidy four-part contrast and "no learning across sessions" were presented as Osmani/Goedecke *quotes* when they are the discovery agent's synthesis. The ideas are well-grounded; the per-source attribution was loose.

**Net (both engines):** keep the junior analogy for the posture (specs, context, behavior-level review, calibrated oversight); reject the smuggled promises (that trust compounds, that confidence tracks correctness, that capability is human-shaped, that the worker is accountable). And note the analogy has active 2026 *defenders* beyond Osmani/Goedecke — it is a live debate, not a settled refutation.

---

## 8. Operationalizing HITL Gates in Agentic Engineering

**Triangulated direction of travel: from human-IN-the-loop (approve every action) toward human-ON-the-loop (supervise + intervene when it matters), tiered by risk/reversibility.** Both engines describe the same gate vocabulary and the same anti-pattern: "interrupt on everything" destroys agent value and *trains rubber-stamping*; "interrupt on nothing" is unsafe.

**Best-verified primary sources (Claude corpus [OFFICIAL]):**
- **Claude Code Auto Mode** (2026-03-25, verified): in-repo edits run freely; shell/external/out-of-project actions gated against 20+ block rules (destroy/exfiltrate, degrade security, cross trust boundaries, bypass review); escalate after 3 consecutive / 20 total denials. *(SUSPECT: one quote was misattributed to this page vs. the autonomy page — immaterial to the claim.)*
- **GitHub Spec Kit** (open-sourced 2026-05-09, verified, independently corroborated): phase-boundary gates Specify → Plan → Tasks → Implement; "[NEEDS CLARIFICATION]" markers must be resolved by human dialogue; "tests are validated and approved by the user" *before* implementation.
- **The calibration health signal:** a "high but not 100%" approval rate — 100% means the gates have become rubber stamps. Anthropic observed 93% blind approval under manual mode (fatigue evidence).

**Gemini's "Ask / Act / Refuse / Confirm" (CQRS) spectrum** maps cleanly onto the Claude corpus's ask-vs-act / CQRS framing (read operations autonomous; write/state-mutating operations gated). This is a clean cross-engine agreement on the most actionable rule: **gate on the read/write boundary.** Gemini's concrete gate placement (Plan-Approval → Sandbox Execution Loop [HOOTL, allowed to fail/iterate] → Diff-Review → Escalation/Timeout) matches the Claude corpus's three-gate pattern almost exactly.

**SUSPECT framings (both engines repeat single-vendor coinages as "canonical"):**
- The **"3-Checkpoint Framework"** (Plan Review / Findings Review / Diff-Before-Push) is sound but appears *only* on one vendor blog (codeongrass.com/Grass) — not an independently corroborated industry consensus. The gate *content* is good; the "dominant/canonical" elevation is unsupported.
- **Digital Applied's Four-Gate taxonomy** and **ESCALATE.md** are single-vendor/marketing-stage artifacts (ESCALATE.md's domain is even listed for acquisition, no adoption evidence). Gemini presents the Four-Gate framework as if established.
- **METR time-horizon "14.5h at 50% for Opus 4.6"** is **contradicted**: the cited 2026-01-29 page reports Opus 4.5 at ~5.3h; the 14.5h figure is a later measurement mis-pinned to the wrong page/model, and the vivid "silent reconciliation error over three weeks" quote is secondary commentary, not METR. The *insight* (longer horizons make failures rarer but harder to catch, arguing for better-placed gates) is reasonable; the specific number is wrong.

**The honest counter-thesis both engines under-weight:** MIT Technology Review (2026-04-16, a real first-party piece) argues "humans in the loop" can become *theatre* when overseers can't audit model reasoning, work under time pressure, and suffer skill atrophy. Well-placed gates are necessary but not automatically sufficient — gate *design* (forcing functions, independent reviewer, non-100% approval target) matters as much as gate *placement*.

---

## Cross-Cutting Themes

1. **Calibrated trust, not blind trust, and not graduated trust.** The single most consistent theme. The right posture is *per-task calibration to stakes*, not a relationship that matures. The junior analogy's deepest flaw is that it smuggles in graduation; the LLM resets. (SQ1, SQ6, SQ7.)

2. **Review the diff's *intent*, not its *syntax*.** Across SQ3, SQ4, and SQ6, the convergent move is to shift human attention left (plan/spec) and right (behavior/tests) and let CI/static analysis/type-checks own syntax. The spec is the external correctness reference that breaks the circular "AI reviews its own output" loop.

3. **Reversibility is the master axis; security is the orthogonal override.** Reversibility/blast radius decides *default* altitude (SQ2, SQ8). Security exposure and irreversibility are the two carve-outs where line-by-line review still pays even though the artifact looks low-stakes (SQ2, SQ3) — because those failures pass happy-path tests and are catastrophic.

4. **The real-world failure is under-review, not over-review.** The developer's worry ("am I auditing too much?") is the *opposite* of the field's dominant failure (38–61% silent unreviewed merges; 93% blind approval; verification debt). The system to design against is rubber-stamping. (SQ3, SQ6, SQ8.)

5. **Altitude is steerable but not the default.** Decision-grade communication is engineerable (params + measurable constraints + persona + plan-gating + progressive disclosure), but models are *not* reliably terse by default (YapBench contradicts the marketing posture), and verbosity persists even under instruction. Steer explicitly and verify. (SQ4, SQ5.)

6. **Frameworks are proliferating faster than they're adopted.** Most named "frameworks" in both engines are single-vendor coinages (Helmsman, Strata lanes, 3-Checkpoint, Four-Gate, ESCALATE.md, Gemini's "Council"). The *shapes* recur and are trustworthy; the specific names, numbers, and "canonical/consensus" claims are not. ~21% of companies have mature agent governance. (SQ1, SQ2, SQ8.)

---

## Recommendations

For a solo developer running an LLM-orchestrated engineering practice (Momentum):

**Where to place HITL gates (in order of leverage):**
1. **Plan-approval gate before any file mutation.** Require a decision-grade plan (architectural summary, targeted files, behavioral changes, trade-offs) and approve *intent and scope*, not line-by-line. This is the highest-leverage, lowest-cost gate (SQ4, SQ8) and it is where you exercise (a) decide-vs-delegate.
2. **Read/write boundary (CQRS / ask-vs-act).** Let read/exploration and in-repo, version-controlled edits run autonomously; gate anything that leaves the sandbox or mutates external/irreversible state. This is the one rule both engines and Anthropic's shipped product agree on (SQ2, SQ8).
3. **Diff-review gate at the PR/merge boundary** for behavior — review the *tests that prove the spec*, edge cases, security boundaries, and "agent abandonment," not every line.
4. **Hard block gates** on the two carve-outs below, with a forcing function (e.g., require an explicit typed confirmation, a rollback/compensating action, or an adversarial pass).

**Always review line-by-line (the carve-outs):**
- **Irreversible / destructive operations** — schema and data migrations, deletes, force-push, prod deploys. Verify the rollback/compensating action exists and is correct.
- **Security / auth / tenant-isolation / secrets-handling code** — AI is empirically worse here and failures pass happy-path tests (CodeRabbit 2.74× XSS).
- **Architecture and design decisions** — these are *yours to make*, not to review; the agent advises.

**Trust + spot-check (do NOT line-audit):** routine CRUD, scaffolding, generated unit tests, docs, log parsing, exploratory prototypes. Lean on CI, type-checking, and static analysis for syntax; sample for sanity.

**Concrete prompt/config patterns for decision-grade communication by default:**
- **System-prompt persona + altitude clause:** "Act as a trusted senior counterpart. I give intent and constraints; you own execution detail. For anything beyond a single-file edit, output a High-Level Design first (service decomposition, targeted files, trade-offs) and wait for approval before writing code." (Gemini's "Principal Solutions Architect" template and the Claude corpus's persona+audience+length pattern converge on this.)
- **Measurable verbosity constraints, not adjectives:** "Lead with a ≤5-bullet executive summary. Keep the response under 400 words. Show diffs only for complex business logic, security parameters, and data-isolation code; hide boilerplate behind a note I can expand." Prefer positive examples over "don't" prohibitions.
- **Ask-before-acting clause:** "Read operations are autonomous. Pause and request explicit authorization before any write/state-mutating action or anything leaving the repo."
- **Progressive disclosure as a deliverable contract:** require summary-first output with detail on demand (this report is itself the proof-of-concept). Use Claude `effort` for *work depth* and explicit length caps for *output verbosity* — they are different knobs.
- **Calibration guardrails:** target a "high but not 100%" approval rate; if you're approving everything, your gates are theatre. Add a forced pause / counter-explanation on high-stakes gates to counter automation bias.

**Operational hygiene given the evidence:** assume the model is *not* terse by default — verify altitude held. Re-establish trust per task (no graduation). Keep a human business-logic checkpoint even when tests pass (tautological testing). Re-verify any vendor parameter name, default, or time-horizon number against current docs before relying on it — this area churns monthly.

---

## Known Limitations & Open Questions

**Cross-engine divergences (where the two engines disagree or one is unreliable):**
- **The "terse-by-default" claim is contradicted.** Both engines assert newest models are terse and you steer *up*. YapBench (2026-01, 76 models) found the opposite population trend. This directly affects the "can the LLM speak at decision-grade altitude by default?" question: **answer is no — you must steer and verify.** *(Developer should weigh in: is the practice's default-output experience actually terse, or are we fighting verbosity?)*
- **Gemini-only artifacts that the Claude corpus does not corroborate** and that should not be relied on as fact: the Microsoft "Council" feature running "Claude Mythos" + "GPT-5.4" with a judge model at 2.5× compute; "NextAds 2026"; "VibeSec"; "OpenClaw"; CSET "68–73% of AI code vulnerable"; "76% believe AI code more secure." These are plausible-sounding but single-engine and partly likely-confabulated. Verify independently before citing.

**AVFL-flagged claims (do not present as settled):**
- **METR "19% slower"** — outdated; METR walked it back (2026-02-24), now a lower bound, study being redesigned. Only the perception gap survives. Gemini uses it un-caveated.
- **JetBrains "20–25% / 44% hallucination split"** — unsupported provenance failure; drop it.
- **Zietsman's "90.9% adoption lift"** and **Yamin's "90% inflated false positives" / "mathematically unattainable"** — not locatable / not independently verified; illustrative only.
- **"No cross-session learning"** — true of the bare model, increasingly false for deployed agent systems with memory layers. *(Open question for Momentum: should the practice invest in a persistent agent-memory layer so trust can partially compound, accepting staleness/identity risk?)*
- **EU AI Act "doesn't require per-decision review"** — that is interpretation, not statute; the regulatory floor (in force 2026-08-02) may push toward *more* review in regulated work.
- Numerous single-vendor frameworks (Helmsman, Strata time-lanes, 3-Checkpoint, Four-Gate, ESCALATE.md) presented as canonical; treat the shapes as useful, the labels/numbers as unvalidated.

**Thin-evidence areas:**
- The exact *coverage bars* for AI vs human code (85–90% vs 70–80%) are unsourced. No reliable empirical target exists; pick one by risk tier and measure.
- The "calibrated trust" reading of Anthropic's HITL→HOTL telemetry is contested by the "oversight illusion" thesis — the same numbers support both stories. We cannot yet distinguish *better calibration* from *more nominal-only oversight*.
- Whether engineered gate design actually closes the accountability/oversight-theatre gap, or merely documents it, is unresolved (Yamin vs HBR/Microsoft).

**Questions the developer should decide:**
1. Do you want trust to *partially compound* via a persistent memory layer, or to *reset per task* (simpler, safer, the current default)?
2. What is your forced-pause / forcing-function policy on the two hard-block carve-outs (irreversible + security)?
3. What approval-rate band signals healthy gates for your solo workflow (and how would you even measure rubber-stamping on yourself)?

---

## Sources

Deduplicated; only sources actually cited above. Grouped by tier. Dates as reported by the sources.

### Peer-reviewed / academic (verified)
- Feng, McDonald & Zhang — *Levels of Autonomy for AI Agents* — https://arxiv.org/abs/2506.12469 / https://knightcolumbia.org/content/levels-of-autonomy-for-ai-agents-1 — 2025-07-28 *(arXiv/Knight working paper; not demonstrably peer-reviewed)*
- Tomašev, Franklin, Osindero et al. (Google DeepMind) — *Intelligent AI Delegation* — https://arxiv.org/html/2602.11865v1 — 2026-02-12 *(preprint)*
- Huang et al. — *Professional Software Developers Don't Vibe, They Control* — https://arxiv.org/pdf/2512.14012 — 2025-12-17 *(preprint)*
- Duma et al. — *These Aren't the Reviews You're Looking For* (EASE 2026) — https://arxiv.org/html/2605.02273v1 — 2026-05-04
- Ehsani et al. — *Where Do AI Coding Agents Fail?* (MSR 2026) — https://arxiv.org/html/2601.15195 — 2026-04
- Khelifi et al. — *Behind Agentic Pull Requests* (MSR 2026) — https://2026.msrconf.org/details/msr-2026-mining-challenge/26/ — 2026-04-13
- Chowdhury et al. — *From Industry Claims to Empirical Reality: Code Review Agents* (MSR 2026) — https://arxiv.org/html/2604.03196v1 — 2026-04-03
- Zietsman — *The Specification as Quality Gate* — https://arxiv.org/abs/2603.25773 — 2026-03-26 *(single-author preprint; 3 hypotheses, argumentative)*
- Srinivasan & Thomason — *Adjust for Trust* (IUI 2026) — https://arxiv.org/abs/2502.13321 — 2026-01-27
- Morris, Altman, Belfield, Goemans, Iqbal, Burnell, Gabriel, Albanie, Dafoe (Google DeepMind) — *Characterizing Model Jaggedness* — https://cs.stanford.edu/~merrie/papers/jaggedness_preprint.pdf — 2026-01-27
- Parasuraman & Manzey — *Complacency and Bias in Human Use of Automation* — https://journals.sagepub.com/doi/10.1177/0018720810376055 — 2010 *(foundational)*
- *Do People Appropriately Rely on AI-Advice?* (CHI 2026) — https://dl.acm.org/doi/10.1145/3772318.3791467 — 2026-04 *(existence unconfirmed — 403)*
- Caosun & Aral (MIT) — *The Augmentation Trap* — https://arxiv.org/html/2604.03501 — 2026-05-21 *(theoretical model, not empirical)*
- *YapBench* (tabularis.ai) — https://arxiv.org/abs/2601.00624 — 2026-01 *(contradicts "terse-by-default")*
- *Brevity is the soul of sustainability* (ACL 2025 Findings) — https://arxiv.org/abs/2506.08686 — 2025-06
- *Plan-and-Write* (length control) — https://arxiv.org/abs/2511.01807 — 2025-11-03
- *Deterministic Pre-Action Authorization* (Uchibeke) — https://arxiv.org/abs/2603.20953 — 2026-03 *(preprint; core is "Open Agent Passport")*

### Industry reports & vendor docs (verified [OFFICIAL])
- Anthropic — *2026 Agentic Coding Trends Report* — https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf — 2026
- Anthropic — *Measuring AI agent autonomy in practice* — https://www.anthropic.com/research/measuring-agent-autonomy — 2026-02-18
- Anthropic — *How we built Claude Code auto mode* — https://www.anthropic.com/engineering/claude-code-auto-mode — 2026-03-25
- Anthropic — *Equipping agents for the real world with Agent Skills* — https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills — 2025-10-16
- Anthropic — *Prompting best practices (Claude API Docs)* — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices — 2026
- Anthropic — *Output styles (Claude Code Docs)* — https://code.claude.com/docs/en/output-styles — 2025 *(stale specifics)*
- Anthropic skill-formation RCT, via InfoQ — https://www.infoq.com/news/2026/02/ai-coding-skill-formation/ — 2026-02
- Cloud Security Alliance (Reavis) — *Autonomy Levels for Agentic AI* — https://cloudsecurityalliance.org/blog/2026/01/28/levels-of-autonomy — 2026-01-28
- DORA — *State of AI-assisted Software Development 2025* — https://dora.dev/dora-report-2025/ ; Google Cloud announcement — https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report — 2025
- DORA — *Balancing AI tensions* — https://dora.dev/insights/balancing-ai-tensions/ — 2026-03-10
- Faros AI — *Lab vs Reality AI productivity* — https://www.faros.ai/blog/lab-vs-reality-ai-productivity-study-findings — 2025-07-28
- CodeRabbit — *State of AI vs Human Code Generation Report* (470 PRs) — https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report — 2025-12-17
- Sonar — *Verification Gap in AI Coding* — https://www.sonarsource.com/company/press-releases/sonar-data-reveals-critical-verification-gap-in-ai-coding/ — 2026-01-08
- METR — *Frontier Risk Report (Feb–Mar 2026)* — https://metr.org/blog/2026-05-19-frontier-risk-report/ — 2026-05-19
- METR — *Early-2025 AI Experienced OSS Dev Productivity* — https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ — 2025-07-10 *(SUPERSEDED — see walk-back)*
- METR — *Changing our Developer Productivity Experiment Design* — https://metr.org/blog/2026-02-24-uplift-update/ — 2026-02-24
- METR — *Time Horizon 1.1* — https://metr.org/blog/2026-1-29-time-horizon-1-1/ — 2026-01-29 *(14.5h/Opus-4.6 figure mis-cited)*
- GitHub — *Review AI-generated code* — https://docs.github.com/en/copilot/tutorials/review-ai-generated-code — 2026
- GitHub (Griffiths) — *Agent pull requests are everywhere. Here's how to review them.* — https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/ — 2026-05-07
- GitHub — *Spec Kit / spec-driven.md* — https://github.com/github/spec-kit/blob/main/spec-driven.md — 2026-05 *(open-sourced 2026-05-09)*
- OpenAI — *GPT-5 New Params and Tools (Cookbook)* — https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_new_params_and_tools — 2025-08-07
- OpenAI — *Prompt guidance (API Docs)* — https://developers.openai.com/api/docs/guides/prompt-guidance — 2026
- Google — *Gemini 3 Developer Guide* — https://ai.google.dev/gemini-api/docs/gemini-3 — 2026-05-29
- EU AI Act — *Article 14: Human Oversight* — https://artificialintelligenceact.eu/article/14/ — 2024 (in force 2026-08-02)
- MIT Technology Review — *Why having humans in the loop in an AI war is an illusion* — https://www.technologyreview.com/2026/04/16/1136029/humans-in-the-loop-ai-war-illusion/ — 2026-04-16
- JetBrains — *Stop Sending IDE-Catchable AI Code Errors to Review* — https://blog.jetbrains.com/ai/2026/05/stop-sending-ide-catchable-ai-code-errors-to-review/ — 2026-05 *(SUSPECT: 20–25%/44% figures unsupported)*

### Practitioner / blog (verified [PRAC], named experts where noted)
- Addy Osmani — *My LLM coding workflow going into 2026* — https://addyosmani.com/blog/ai-coding-workflow/ — 2026-01-04
- Addy Osmani — *How to Write a Good Spec for AI Agents* (O'Reilly) — https://www.oreilly.com/radar/how-to-write-a-good-spec-for-ai-agents/ — 2026-02-20
- Sean Goedecke — *How I use LLMs as a staff engineer in 2026* — https://www.seangoedecke.com/how-i-use-llms-in-2026/ — 2026-05-17
- Jacob Harris — *The LLM Is Not a Junior Engineer* — https://jacobharr.is/personal/llm-not-junior-engineer — 2026-04-29
- Simon Willison (via Stefan Judis) — *On delivering AI generated code* — https://www.stefanjudis.com/notes/simon-willison-on-delivering-ai-generated-code/ — 2025-12-18
- Simon Willison — *METR study summary* — https://simonwillison.net/2025/Jul/12/ai-open-source-productivity/ — 2025-07-12
- Ethan Mollick — *Centaurs and Cyborgs on the Jagged Frontier* — https://www.oneusefulthing.org/p/centaurs-and-cyborgs-on-the-jagged — 2023-09-16 *(foundational)*
- Theory Ventures — *It's Not Too Late to Roll Back MCP* — https://theoryvc.com/blog-posts/its-not-too-late-to-roll-back-mcp — 2026-04-13
- Will Larson — *Building an internal agent: Progressive disclosure* — https://lethain.com/agents-large-files/ — 2025-12-26
- Swarmia (Holkeri) — *Five levels of AI coding agent autonomy* — https://www.swarmia.com/blog/five-levels-ai-agent-autonomy/ — 2026-03-19
- StackAI — *Human-in-the-Loop AI Agents: Approval Workflows* — https://www.stackai.com/insights/human-in-the-loop-ai-agents-how-to-design-approval-workflows-for-safe-and-scalable-automation — 2026-03-03 *(vendor; "15-second approval" is rhetoric)*
- Amazon Kiro review (chatforest) — https://chatforest.com/reviews/amazon-kiro-aws-agentic-ide-spec-driven-review/ — 2026-05-23 *(third-party review; primary: https://kiro.dev/docs/specs/)*
- Philipp Schmid — *Gemini 3 Prompting Best Practices* — https://www.philschmid.de/gemini-3-prompt-practices — 2025-11-19
- codeongrass (Grass) — *Where to Gate Your AI Coding Agent: 3-Checkpoint Framework* — https://codeongrass.com/blog/where-to-gate-your-ai-coding-agent-3-checkpoint-framework/ — 2026-05-03 *(single-vendor coinage)*
- Tahir Yamin — *The AI Agent Accountability Crisis* — https://tahir-yamin.medium.com/the-ai-agent-accountability-crisis-3917e5b3be85 — 2026-01-25 *(SUSPECT figures)*
- Management 3.0 (Appelo) — *Delegation Poker / 7 Levels of Delegation* — https://management30.com/practice/delegation-poker/ — foundational

### Vendor/consultancy framings used illustratively (treat shapes, not labels, as authoritative)
- Baytech — *Five Engineering Patterns to Secure Agentic AI in 2026* (Helmsman/Blast Radius) — https://www.baytechconsulting.com/blog/engineering-patterns-secure-agentic-ai-2026 — 2026-05-01
- Strata — *Human-in-the-Loop: A 2026 Guide to AI Oversight* (time-lanes) — https://www.strata.io/blog/agentic-identity/practicing-the-human-in-the-loop/ — 2026-05-11
- Digital Applied — *Agentic Workflow Approval Gates: Governance Framework* (Four-Gate) — https://www.digitalapplied.com/blog/agentic-workflow-approval-gate-framework-governance — 2026-04-27
- Waxell — *Human-in-the-Loop vs Human-on-the-Loop* — https://www.waxell.ai/blog/human-in-the-loop-vs-human-on-the-loop-ai-agents — 2026-04-27
- ESCALATE.md — https://escalate.md/ — 2026-03 *(marketing-stage spec; no adoption evidence)*

*Engine-two report (Gemini Deep Research, Gemini Pro, 2026-05-31) was used for triangulation throughout; its source list is in `raw/gemini-sources.md`. Gemini-only named artifacts (Microsoft "Council"/"Claude Mythos"/"GPT-5.4", "NextAds", "VibeSec", "OpenClaw", CSET vulnerability figures) are flagged [UNVERIFIED] at point of use and are not relied upon as fact.*
