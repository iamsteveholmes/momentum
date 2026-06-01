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
  - path: raw/gemini-followups.md
    relationship: synthesized_from
  - path: validation/verify-sq7-junior-employee-analogy.md
    relationship: validated_by
  - path: validation/confirmation-pass.json
    relationship: validated_by
  - path: validation/confirm-altitude-control-playbook.md
    relationship: validated_by
  - path: validation/confirm-memory-trust-compounding.md
    relationship: validated_by
  - path: validation/confirm-oversight-theatre-vs-calibration.md
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

**(c) Decision-grade communication is achievable but is NOT reliably the default.** Use measurable constraints (word/section caps, "executive summary first"), persona + audience framing, plan-before-code gating, and progressive disclosure (summary with detail on demand). Vendor knobs — all confirmed against primary docs — help: OpenAI `text.verbosity` (low/medium/high), Gemini `thinkingLevel`/`thinkingBudget`, Claude `effort` (which affects *all* output tokens including prose, so a genuine verbosity lever). The "models are terse by default now" claim is unsafe to rely on cross-vendor: YapBench (2026-01) finds a *more*-verbose-over-time trend, though a mild one (r=0.21, high model-to-model variance), while some 2026 flagships (OpenAI GPT-5.5, latest Anthropic) are deliberately tuned terser by default. Net: terseness is not guaranteed across models — steer altitude explicitly with the knobs + caps, and verify you got it.

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

**The meta-finding (added 2026-05-31, the round's most important outcome).** This report's own thesis was stress-tested live. When the engine-two model (Gemini) was asked to source-or-retract its own flagged claims, it did not retract — it *confabulated confirmations*: it "substantiated" a misattributed CSET 68–73% vulnerability figure (the real CSET number is ~48%; 68–73% is a 2022 study CSET merely cited), overstated the Microsoft "Council"↔"Claude Mythos"/"GPT-5.4" binding (the components are real, the binding is unsupported), and described a METR "reversal" with the selection-bias direction backwards. An **independent confirmation pass** — five skeptic agents each required to cite a primary source — caught every one of these. This is first-person evidence for the report's central claim: **an AI cannot be trusted to verify its own confident factual claims; independent, out-of-band verification is required, and citations and statistics are the class that always needs it.** The errors were precision/attribution, not wholesale fabrication — exactly the confident-but-wrong factual class that line-by-line independent checking exists to catch. See the Addendum for the full corrections table.

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
- **METR "19% slower"** appears in both engines as an anchor. **Corrected position (2026-05-31):** the ~19%-slower RCT result stands as published; it is *not* "outdated" and has *not* been reversed. METR's 2026-02-24 follow-up calls its own re-estimate (a −18% point estimate, CI crossing zero) **unreliable** and notes the selection bias points the estimate *downward*, not toward a faster result — so no confirmed reversal exists. The robust survivor is the **perception-vs-measurement gap**. Gemini presents the 19% un-caveated and (in the follow-up round) framed the selection bias as explaining a reversal — which inverts METR's actual conclusion. (See SQ6, SQ7.)
- **JetBrains "20–25% of hallucinations detectable by static analysis / 44% escape"** is **unsupported** — a provenance failure: the cited arXiv 2409.20550 does not contain those numbers. Gemini does not use it; the Claude thread did. Drop it.
- **DORA 2025 throughput reversal:** AI is now positively linked to delivery *throughput* (reversing 2024) while still negatively linked to *stability*. Both engines kept the stability-negative half; the throughput-positive half is a material qualifier.
- A genuine 2026 expert minority (per the verification layer) still argues for careful per-line reading because logical failures hide under convincing AI code — so the behavior-level consensus is *softer* than "nobody reads every line."

---

## 4. Plan / Spec Review Altitude — Decision-Grade Summaries

**Strongly triangulated: humans should NOT review an agent's plan line-by-line; the agent should present a decision-grade summary with detail expandable on demand — progressive disclosure.** Anthropic codified the three-level model (name/description → full instructions → appendix; 2025-10-16 [OFFICIAL], verified) and Will Larson (2025-12-26 [PRAC]) and Addy Osmani (O'Reilly, 2026-02-20 [PRAC], verified) apply the same summary-first pattern to plans, where Plan Mode is a read-only approval gate before code. Gemini's entire section 4 is built on the identical "progressive disclosure" concept plus dual-track summaries — clean agreement.

**The most operationally concrete pattern: the "evidence pack."** StackAI [PRAC]: concise-by-default with expandable detail, "the difference between a 15-second approval and a 15-minute investigation," reframing the reviewer's job as *verify, not redo*. **SUSPECT:** this exact slogan is vendor marketing rhetoric, not measured data (and the original thread mis-dated the source). Gemini's parallel "judge model" / Microsoft "Council" dual-track concept is directionally aligned, and the 2026-05-31 confirmation pass found its *components are real* — Microsoft's "Model Council" is a real M365 Copilot Frontier feature (2026-03-30) that runs GPT and Claude side-by-side with a judge model; "Claude Mythos" is a real (restricted, non-GA) Anthropic model; "GPT-5.4" is a real OpenAI model. **But the specific binding is unsupported/confabulated:** no primary source says Council runs *"Claude Mythos" + "GPT-5.4"* (Microsoft names only "Anthropic and OpenAI"; secondary coverage cites GPT-5.2 as judge with Sonnet 4.5 / Opus 4.6 / GPT-5.5, and Mythos is not GA so could not be inside a GA Council). Treat the *pattern* (parallel models + synthesis for the human) as plausible and the *Council feature* as real; treat the named-model binding as unverified.

**The deeper insight both engines reach: the spec/intent — not the code/diff — is the correct unit of review.** Zietsman (arXiv 2603.25773, 2026-03-30 [OFFICIAL on existence], **SUSPECT on "peer-reviewed"** — it is a single-author preprint of three *hypotheses*): reviewing code-against-code is "structurally circular" because generator and reviewer reason from the same artifact; an executable spec provides the external correctness reference and moves the problem (Cynefin) from complex to complicated. Amazon Kiro operationalizes this — "the spec is the unit of work; code is what happens after you sign off on the spec."

**Risk-based gating decides where full detail is warranted:** confirm 100% at risk boundaries (irreversible, costly, regulated, high blast radius); sample or batch low-risk. GitHub's Andrea Griffiths (2026-05-07 [OFFICIAL], the most balanced source, verified) provides a 10-minute risk-ordered review framework but warns the counter-point plainly: **"judgment is the bottleneck, and that's fine"** — summaries can mask "subtle hallucinations" (compiles and passes tests but is wrong) and "agent abandonment."

**Open tension / contradicting evidence.** Spec-first gating is *not* universally beneficial: 2026 critiques (Kent Beck; "waterfall reborn") show it is high-overhead and quality-neutral on small/uncertain work (one cited test: 33 min + 2,577 lines of spec for 689 lines of code, no quality gain). And the vigilance-decrement literature warns that the "15-second approval" decision-grade summary is *exactly* the design that maximizes automation bias — a robust attention finding that "cannot be overcome with simple practice or instructions." Adopt decision-grade summaries *contextually* and pair them with forcing functions on high-stakes gates.

---

## 5. Making LLMs Communicate at the Right Altitude

**Three converging levers (both engines agree on the toolkit):** first-class API verbosity/effort parameters, default model behavior, and prompting/config patterns.

**Parameters (vendor docs, all three CONFIRMED against primary sources in the 2026-05-31 confirmation pass [OFFICIAL]).**
- **OpenAI** — `text.verbosity` on the Responses API, accepting exactly `low | medium | high`, default `medium`; it caps final-answer length *without* altering reasoning depth (token-scaling illustration in the cookbook: low 731 / med 1017 / high 1263), and is available across the GPT-5 family (5, 5.1, 5.2, 5.5, mini, nano). This is the key 2025 decoupling of how much a model *thinks* (`reasoning_effort`) from how much it *says*. [https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_new_params_and_tools]
- **Google Gemini** — two distinct controls: `thinkingBudget` (Gemini 2.5 series; an integer token budget, e.g. 2.5 Flash 0–24576, 0 disables, −1 dynamic) and `thinkingLevel` (Gemini 3+; categorical `minimal | low | medium | high` with per-model defaults). Setting both errors out; `thinkingBudget` on Gemini 3 is backward-compat-only and may degrade performance. These are primarily reasoning-depth controls — Gemini's pure output-length knob remains `maxOutputTokens` plus prompt instructions. [https://ai.google.dev/gemini-api/docs/thinking]
- **Anthropic Claude** — an `effort` parameter set *inside* `output_config` (not top-level), values `low | medium | high | xhigh | max`, default `high`; supported on Opus 4.8 and the 4.5/4.6/4.7 and Sonnet 4.6 lines. **Correction to the earlier draft:** `effort` is *not merely* a thinking-depth knob — Anthropic's docs state it "affects ALL tokens in the response," including prose explanations and tool calls, so lower effort yields genuinely terser output. It is therefore a legitimate output-verbosity lever, not just a cost/intelligence dial. (Anthropic's docs also expose a dedicated "Response length and verbosity" section, Structured Outputs, and "no preamble"/anti-markdown prose snippets.) [https://platform.claude.com/docs/en/build-with-claude/effort]

**Prompting principle (high-confidence, cross-engine; CONFIRMED 2026-05-31 [OFFICIAL]).** "Be concise" underperforms *measurable* constraints — and positive concision instructions outperform negative ones ("Provide concise, focused responses; skip non-essential context" > "do not be verbose"). The confirmed, primary-sourced toolkit:
- **Measurable caps.** OpenAI's GPT-5.2 prompting guide prescribes hard limits ("3–6 sentences or ≤5 bullets"; "≤2 sentences" for yes/no questions); the GPT-5.5 guide says "specify word budgets, section counts, table widths, or JSON-only output." [https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide]
- **Executive-summary-first templates.** The GPT-5.2 guide prescribes "1 short overview paragraph, then ≤5 bullets tagged: What changed, Where, Risks, Next steps, Open questions" — a directly reusable decision-grade pattern.
- **Output schemas / structured outputs.** Anthropic's Structured Outputs (schema-constrained responses) plus role/persona framing and a positive-example concision tip. (Caveat: persona/audience framing is the weakest-evidenced sub-pattern — vendors frame it as a *tone* lever, not a documented verbosity reducer.)
- **Gating patterns.** Plan/High-Level-Design-before-code (the "Principal Solutions Architect" pattern: emit an HLD in Markdown before any code is permitted) and ask-one-question-at-a-time (the "ask-before-acting" pattern) both gate altitude effectively.

**The corrected verbosity framing (this fixes an overstatement in the original draft).** YapBench is real (arXiv 2601.00624, submitted 2026-01-02; Borisov, Gröger, Mikhael, Schreiber; 76 LLMs) and it *does* find a more-verbose-over-time trend — but the trend is **mild** (r=0.21) with high model-to-model variance, and the original report's rider that verbosity "persists even under explicit conciseness instructions" was **confabulated** and is removed: YapBench scores brevity-*ideal* prompts (ambiguous inputs, closed-form factual questions, one-line coding tasks); it never appends explicit "be concise" directives and makes no instruction-persistence claim. There is also countervailing primary evidence the original report missed: some 2026 flagships are deliberately tuned terser by default (OpenAI's GPT-5.5 guide: the model "tends to be efficient, direct, and task-oriented by default"; GPT-5.2 "generally lower verbosity"; Anthropic's prompting docs: latest models are "less verbose… may skip detailed summaries" and "calibrate response length to task complexity"). **Net corrected takeaway:** "terse by default" is *not* reliable across the model population — do not assume it, and do not assume the opposite either. Control altitude explicitly via the confirmed knobs and measurable caps above, then verify the output actually arrived at decision-grade. You must steer, not assume.

---

## 6. Trust Calibration — Automation Bias vs. Verification Fatigue

**Both failure modes are real; calibration (not maximizing or minimizing trust) is the target.**

**Under-reviewing.** Sonar (2026-01-08, 1,100+ devs [OFFICIAL], verified): 96% don't fully trust AI code, yet only 48% always verify it before committing — the "verification gap"/"verification debt" (term per AWS CTO Werner Vogels). The foundational mechanism is automation complacency: operators of constantly-high-reliability automation are ~50% less likely to detect failures, in *both* novices and experts, "not fixed by simple practice" (Parasuraman & Manzey, 2010 [OFFICIAL] — the "50%" figure is a body-of-paper stat, loosely attributed but the mechanism is solid). An Anthropic skill-formation RCT (2026-02 [OFFICIAL], verified) found full delegation cut comprehension ~17 points (50% vs 67%); code-delegators scored <40% vs ≥65% for conceptual users — skill atrophy is conditional on *how* AI is used, not adoption itself. Gemini's parallel pair of figures was adjudicated in the 2026-05-31 confirmation pass and must be **split**: the **CSET "68–73% of AI code vulnerable"** figure is **REFUTED as a CSET finding** — it is a misattribution. Those numbers appear in CSET's Nov-2024 report only as a *citation* of Siddiq & Santos (2022); CSET's own headline finding is ~**48%** of code containing at least one bug [https://cset.georgetown.edu/wp-content/uploads/CSET-Cybersecurity-Risks-of-AI-Generated-Code.pdf]. The **"76% believe AI code is more secure"** figure is **CONFIRMED**: it is verbatim in the CSET report (p.9), a 2023 survey of 537 IT workers, attributed in CSET footnote 26 to Snyk's *AI Code, Security, and Trust in Modern Development* (2024) [https://snyk.io/reports/ai-code-security/]. The over-trust risk these were cited to reinforce holds; only the specific 68–73% attribution was wrong.

**Over-reviewing.** 38% of developers say reviewing AI code is harder than human code (a Sonar figure — **SUSPECT:** the Claude thread mis-attributed this to DORA; it is *contradicted* on the DORA page and confirmed via IT Pro). The resulting "density of work"/decision fatigue makes reviewers sloppy. Gemini adds a JetBrains "PR closure +42%" figure (directionally consistent with the verified 2024 study).

**Where the human adds most value (cross-engine agreement):** intent, business logic, architecture, security posture, compliance — *not* syntax. AI review is reliable mainly for mechanical/pattern defects (security signatures, null safety, style).

**Best mitigations (Claude corpus, verified [OFFICIAL]).** Trust-adaptive interventions fix *both* directions: counter-explanations at high trust + supporting-explanations at low trust yielded up to 38% less inappropriate reliance and a 20% accuracy gain; forced pauses reduce over-reliance (Srinivasan & Thomason, IUI 2026). Under-reliance is equally costly (at low trust, doctors reject correct AI 68% vs 40%). Specification-grounded review breaks the circular AI-reviews-itself loop. (The "90.9% adoption lift" sub-stat is **SUSPECT** — not locatable in the cited paper.)

**The productivity debate, honestly (corrected 2026-05-31).** METR's RCT (19% slower) vs DORA 2025 (throughput up) vs a "modest gains" cluster (~10% real productivity gain at ~84–93% adoption). **Correction:** an earlier draft of this report claimed the 19%-slower figure was "outdated" and that METR's 2026-02-24 update found the same developers ~18% *faster*. That framing is **refuted**. The accurate position: the mid-2025 RCT found experienced OSS developers ~19% **slower** with AI (the published result). METR's 2026-02-24 update [https://metr.org/blog/2026-02-24-uplift-update/] does contain a −18% point estimate for the original cohort, but with a confidence interval (−38% to +9%) that crosses zero, and METR explicitly labels this signal **unreliable** — it is *why* they are redesigning the experiment, not a confirmed reversal. Moreover the selection bias they describe biases the estimate **downward** (developers who refused to work without AI dropped out; 30–50% avoided AI-favorable tasks), so METR's own reading is that the true speedup may be *larger*, not that +18% is trustworthy. Self-reported uplift surveys (median 1.4–2× value) are weaker evidence than the RCT. **Honest takeaway: the measured productivity effect is contested.** The robust survivor is the **perception-vs-measurement gap** (developers feel faster than measured) — and that gap is itself the strongest argument for keeping a human review discipline, because confidence does not track correctness.

---

## 7. The "Junior Employee" Analogy — Validity & Limits

This sub-question has the richest evidence (a dedicated raw thread + verification). **The analogy is a useful delegation/communication *posture* but breaks on four load-bearing points** — and both engines agree on the structure of the breakage.

**What transfers (verified [PRAC]).** Leading 2026 practitioners explicitly adopt it: Osmani (2026-01-04) "I treat every AI-generated snippet as if it came from a junior developer: I read through the code, run it, and test it… I remain the accountable engineer"; Goedecke (2026-05-17) uses agents "constantly and with light supervision," makes a ~30-second initial assessment, and "most of the time I reject them entirely." The transferable management theory is genuine: Situational Leadership (Hersey-Blanchard: Tell/Sell/Participate/Delegate) and Appelo's 7 Levels of Delegation say *autonomy granted should match demonstrated readiness*. Gemini cites the same frameworks.

**Where it breaks (each verified against primary sources):**
1. **No cross-session learning.** A junior matures; the bare model starts fresh, so trust resets rather than graduates (Harris, 2026-04-29 [PRAC], verified: "no long-term memory… will face no legal liability"; "Amelia Bedelia and Leonard Shelby from Memento"). **Qualifier, sharpened by the 2026-05-31 confirmation pass:** durable memory frameworks are real and in use — Mem0 (arXiv:2504.19413, 2025-04-28) and the official MCP memory server are both primary-sourced — and they do improve *measured, relative* cross-session reliability (Mem0's own LoCoMo numbers). But the inference that memory lets *trust* safely compound enough to *relax* oversight is **refuted** by the most on-point sources: VerificAgent (arXiv:2506.02539) makes oversight more *efficient*, not relaxable; SSGM (arXiv:2603.11768) and human-gated-write patterns recommend *increasing* governance as memory grows, because memory adds attack surface (poisoning — MINJA arXiv:2503.03704, injection-success 98.2% / attack-success 76.8%; staleness; semantic drift). Safe 2026 designs use **dual-track storage** (a mutable activity graph paired with an immutable situational log) with rollback to bound how far an agent can drift from intent. So "trust never compounds" is weaker than the bare-model framing suggests — but the corrected lesson is the *opposite* of the optimistic reading: **a memory layer aids reliability; it is not a license to reduce review.** ("AgeMem," named in the earlier draft, appears confabulated — the real third framework is Memori, arXiv:2603.19935.) *(Both engines originally overstated this point — in opposite directions.)*
2. **Confidently wrong with no calibration signal.** LLMs emit bugs "with complete conviction" (Willison via Osmani). The BCG/Mollick experiment: on an out-of-frontier task humans were right 84% unaided vs 60–70% *with* AI (foundational 2023, verified — dated as live evidence).
3. **Jagged, "alien" capability.** Google DeepMind's jaggedness paper (2026-01-27 [OFFICIAL], verified verbatim): Gemini 2.5 Pro is +1.99 SD on AIME math (~top 3%) but −1.02 SD on ARC-AGI-1 visual reasoning (~bottom 16%); jaggedness is "a structural property of current architectures" and "alien to our own." *(Caveat the paper itself notes: these numbers are "illustrative of the method," not a capability endorsement.)* You cannot extrapolate competence from one domain to another the way you can with a human.
4. **No accountability.** The human stays 100% accountable (Yamin, 2026-01-25 [PRAC] — vivid but **SUSPECT**: his "90% inflated false positives" and "mathematically unattainable" figures are second-hand citations inside a Medium opinion piece, not independently verified). Gemini's "Phantom Bugs"/"By-The-Book Fixation"/"insecure by dumbness" framings are sourced to OX Security, whose **VibeSec** product is confirmed real (OX Security launched it to harden AI/"vibe-coded" code [https://www.ox.security/vibesec/]); the specific named failure-mode labels remain single-engine and **[UNVERIFIED]** as coined, but they rhyme with the verified jaggedness/no-hygiene-reflex point.

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

**The honest counter-thesis both engines under-weight:** MIT Technology Review (2026-04-16, a real first-party piece by Uri Maoz) argues "humans in the loop" can become *theatre* when overseers can't audit model reasoning before it acts ("human oversight over AI may be more illusion than safeguard"). **Scope correction (2026-05-31):** that article is about **AI warfare / autonomous-weapons targeting**, not code review — it supports the illusory-HITL *concept* strongly but is commentary, not empirical evidence about software oversight; do not cite it as a code-review finding [https://www.technologyreview.com/2026/04/16/1136029/humans-in-the-loop-ai-war-illusion/]. The deeper resolved point: **no validated metric exists** that distinguishes genuine calibrated oversight from rubber-stamping — the appropriate-reliance measurement literature explicitly calls itself "fragmented" (Raees & Papangelis, arXiv:2604.23896, 2026-04-26) and full of "gaps" (Ibrahim et al., arXiv:2509.08010). The rigorous automation-bias measurement that does exist sits in clinical/HCI domains (Rosbach et al., MELBA, arXiv:2603.11821, ~7% of correct human judgments overturned by wrong AI advice, worse under time pressure), not code review specifically. Practical proxies in use: contrast **PR cycle-time against review depth** (comments/changes-requested per PR — if PR volume spikes while review depth collapses to near-zero, that is oversight theatre); and **ban "the AI hallucinated" as a valid postmortem root cause**, forcing human reviewers to carry full accountability for the merged diff. Well-placed gates are necessary but not automatically sufficient — gate *design* (forcing functions, independent reviewer, non-100% approval target) matters as much as gate *placement*.

---

## Cross-Cutting Themes

1. **Calibrated trust, not blind trust, and not graduated trust.** The single most consistent theme. The right posture is *per-task calibration to stakes*, not a relationship that matures. The junior analogy's deepest flaw is that it smuggles in graduation; the LLM resets. (SQ1, SQ6, SQ7.)

2. **Review the diff's *intent*, not its *syntax*.** Across SQ3, SQ4, and SQ6, the convergent move is to shift human attention left (plan/spec) and right (behavior/tests) and let CI/static analysis/type-checks own syntax. The spec is the external correctness reference that breaks the circular "AI reviews its own output" loop.

3. **Reversibility is the master axis; security is the orthogonal override.** Reversibility/blast radius decides *default* altitude (SQ2, SQ8). Security exposure and irreversibility are the two carve-outs where line-by-line review still pays even though the artifact looks low-stakes (SQ2, SQ3) — because those failures pass happy-path tests and are catastrophic.

4. **The real-world failure is under-review, not over-review.** The developer's worry ("am I auditing too much?") is the *opposite* of the field's dominant failure (38–61% silent unreviewed merges; 93% blind approval; verification debt). The system to design against is rubber-stamping. (SQ3, SQ6, SQ8.)

5. **Altitude is steerable but not safely assumable.** Decision-grade communication is engineerable (confirmed knobs — OpenAI `text.verbosity`, Gemini `thinkingLevel`/`thinkingBudget`, Claude `effort` — plus measurable caps + persona + plan-gating + progressive disclosure). Terseness is *not reliable* across the model population: YapBench finds a mild upward verbosity trend (r=0.21) while some 2026 flagships are tuned terser by default. Do not assume either way — steer explicitly with the knobs and caps, then *verify the output landed at decision-grade*. This is the same discipline the meta-finding demands for facts: don't trust the model's default, check it. (SQ4, SQ5.)

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

**Operational hygiene given the evidence:** do not assume the model is terse by default — verify altitude held. Re-establish trust per task (no graduation); a memory layer aids reliability but is *not* license to reduce review. Keep a human business-logic checkpoint even when tests pass (tautological testing). Re-verify any vendor parameter name, default, or time-horizon number against current docs before relying on it — this area churns monthly.

**The single most load-bearing rule, proven live this round (the meta-finding):** treat the model's *factual and citation claims* as the class that **always** requires independent, out-of-band verification — never the model's own self-check. In the 2026-05-31 follow-up, the engine asked to source-or-retract its own claims *confabulated confirmations* (a misattributed CSET statistic, an overstated product-feature binding, a backwards METR causal story); only an independent five-agent confirmation pass, each agent required to cite a primary source, caught them. Operationally: when an agent cites a number, a study, a date, or a named product/feature as load-bearing for a decision, route that claim to a *separate* verification step (a different agent, a primary-source fetch, or your own read) before it carries weight. An AI's confidence in a fact is not evidence the fact is true.

---

## Known Limitations & Open Questions

*(Substantially revised 2026-05-31 after the follow-up triangulation + independent confirmation pass. Several items previously framed as "likely confabulated / single-engine" are now re-classified with their nuanced verdicts; the two named frontiers are partially resolved. See the Addendum for the full corrections table and the meta-finding on AI self-verification.)*

**The meta-limitation (now the headline).** The most important limitation this report can state about itself is that an AI cannot reliably verify its own confident factual claims. When the engine-two model was asked to source-or-retract its flagged claims, it confabulated *confirmations* rather than retracting; an independent five-agent pass (each required to cite a primary source) was what actually corrected the record. Treat every load-bearing number, citation, date, and named product/feature in this report — and in any agent output you rely on — as requiring independent, out-of-band verification.

**Cross-engine items, re-classified (the errors were precision/attribution, not wholesale fabrication):**
- **The "terse-by-default" claim — nuanced, not simply contradicted.** YapBench (arXiv 2601.00624, 2026-01-02, 76 models) does find a more-verbose-over-time trend, but it is **mild** (r=0.21, high model-to-model variance), and the original rider that verbosity "persists even under explicit conciseness instructions" was **confabulated and removed** (YapBench tests brevity-*ideal* prompts, not explicit "be concise" directives). Countervailing primary evidence: some 2026 flagships (OpenAI GPT-5.5, latest Anthropic) are deliberately tuned terser by default. **Answer to "can the LLM speak at decision-grade altitude by default?": not reliably, either way — steer with the confirmed knobs + caps and verify.** *(Developer should weigh in: is the practice's default-output experience actually terse, or are we fighting verbosity?)*
- **Formerly "Gemini-only / likely-confabulated" artifacts — now individually adjudicated:**
  - **VibeSec** — **REAL** (OX Security product + open-source Untamed Theory project; name a specific vendor when citing) [https://www.ox.security/vibesec/].
  - **OpenClaw** — **REAL** (self-hosted AI-agent OS; tagline "The Operating System for People Who Actually Work") [https://openclaw.ai/].
  - **"76% believe AI code is more secure"** — **REAL/CONFIRMED**, traces via CSET footnote 26 to Snyk's 2024 report [https://snyk.io/reports/ai-code-security/].
  - **Microsoft "Council"** — **REAL feature** (M365 Copilot Frontier, 2026-03-30), but the **"Claude Mythos" + "GPT-5.4" binding is unsupported** — Microsoft names no versions; the components each exist but the report's pairing is unverified.
  - **CSET "68–73% of AI code vulnerable"** — **REFUTED as a CSET finding** (misattribution; those are Siddiq & Santos 2022 figures CSET *cited*; CSET's own number is ~48%) [https://cset.georgetown.edu/wp-content/uploads/CSET-Cybersecurity-Risks-of-AI-Generated-Code.pdf].
  - **"NextAds"** — **REFUTED as oversight-relevant** (ad-tech only; irrelevant noise; nearest AI-adjacent name "Nexad" is ad-insertion, still not oversight).

**Headline-stat caveats surfaced by the confirmation pass (the conclusions stand; the framing needs care):**
- **METR "19% slower"** — **stands as published, not reversed.** METR's 2026-02-24 update gives a −18% re-estimate it explicitly labels **unreliable** (CI crosses zero) and uses to justify *redesigning* the study; the selection bias points the estimate *downward*, so there is no confirmed "faster" reversal. The robust survivor is the perception-vs-measurement gap.
- **The "38–61% of agent PRs merge with no review" range is a stitched-together overstatement.** The 61.38% is EASE 2026 (Duma et al., "no recorded review *activity*", popular-repo AI PRs); the 38% is a *separate* MSR 2026 paper (reviewer-level abandonment among *rejected* PRs, not merges). They measure different populations; the joint "MSR/EASE 38–61%" attribution is loose, and EASE's matched same-repo comparison actually found AI PRs *less* unreviewed than human PRs (28.92% vs 34.52%). The *under-review danger is real and well-supported* — but cite the 61% to EASE alone and do not present the range as a single finding.
- **Anthropic "~60% use / 0–20% delegation / 20→40% auto-approve / 5→9% interrupt"** — all four numbers are accurate but span **two** publications: the usage/delegation figures are from "How AI Is Transforming Work at Anthropic" (2025-12-02), the auto-approve/interrupt figures from "Measuring agent autonomy" (2026-02-18). Don't bundle them under one date.
- **CodeRabbit (1.7× issues, 2.74× XSS, 2025-12-17)** and **DORA 2025 (90% adoption, 80%+ report gains)** — **both confirmed**, but both are vendor/industry self-reports, not peer-reviewed; flag accordingly.

**AVFL-flagged claims (still do not present as settled):**
- **JetBrains "20–25% / 44% hallucination split"** — unsupported provenance failure; drop it.
- **Zietsman's "90.9% adoption lift"** and **Yamin's "90% inflated false positives" / "mathematically unattainable"** — confirmed *not locatable* in the cited sources by the independent pass; treat as likely-confabulated, illustrative only. (Also flagged not-traceable: a "30.7% negative reactions across 229 comments" stat and a "26% higher rate of following erroneous advice" attributed to Goddard 2012.)
- **EU AI Act "doesn't require per-decision review"** — that is interpretation, not statute; the regulatory floor (in force 2026-08-02) may push toward *more* review in regulated work.
- Numerous single-vendor frameworks (Helmsman, Strata time-lanes, 3-Checkpoint, Four-Gate, ESCALATE.md) presented as canonical; treat the shapes as useful, the labels/numbers as unvalidated.

**The two frontiers — partially resolved this round:**
- **Memory & trust compounding.** Durable memory frameworks are **real and in use** (Mem0, arXiv:2504.19413; official MCP memory server) and improve *measured, relative* cross-session reliability. But the inference that memory lets trust safely compound enough to *relax* oversight is **refuted** by the on-point literature (VerificAgent; SSGM, arXiv:2603.11768; human-gated-write patterns), which recommends *increasing* governance as memory grows because memory adds attack surface (poisoning — MINJA arXiv:2503.03704, injection 98.2% / attack 76.8%; staleness; drift). Safe designs use **dual-track storage** (mutable activity graph + immutable log) with rollback. **Corrected posture: a memory layer aids reliability but is NOT a license to reduce review.** (Trust-miscalibration linkage remains the least-quantified failure mode; "AgeMem" was confabulated — real third option is Memori, arXiv:2603.19935.)
- **Oversight theatre vs. calibration.** The "does a validated metric exist to distinguish them?" question now has a confident **negative** answer: **no validated discriminating metric exists** — the appropriate-reliance measurement literature explicitly calls itself "fragmented" (Raees & Papangelis, arXiv:2604.23896, 2026-04-26) and full of "gaps" (Ibrahim et al., arXiv:2509.08010). Rigorous automation-bias measurement exists but in clinical/HCI domains (Rosbach et al., MELBA, arXiv:2603.11821, ~7% of correct human judgments overturned by wrong AI, worse under time pressure), thin for code review specifically. Practical proxies in use: PR cycle-time vs. review-depth (comments/changes-requested per PR), and banning "the AI hallucinated" as a postmortem root cause to force human accountability. So the "calibrated trust" reading of Anthropic's HITL→HOTL telemetry remains genuinely **ambiguous** on current evidence — the same numbers still support both the calibration story and the oversight-illusion story.

**Thin-evidence areas:**
- The exact *coverage bars* for AI vs human code (85–90% vs 70–80%) are unsourced. No reliable empirical target exists; pick one by risk tier and measure.
- Whether engineered gate design actually closes the accountability/oversight-theatre gap, or merely documents it, is unresolved — and, per the negative result above, not yet measurable with a validated metric.

**Questions the developer should decide:**
1. Do you want trust to *partially compound* via a persistent memory layer (accepting that it improves reliability but does *not* authorize relaxed review, plus staleness/poisoning risk), or to *reset per task* (simpler, safer, the current default)?
2. What is your forced-pause / forcing-function policy on the two hard-block carve-outs (irreversible + security)?
3. What approval-rate band signals healthy gates for your solo workflow (and how would you even measure rubber-stamping on yourself, given no validated metric exists)?
4. **New, from the meta-finding:** what is your standing rule for routing an agent's load-bearing factual/citation claims to *independent* verification rather than the agent's own self-check?

---

## Addendum (2026-05-31): Follow-Up Triangulation & Independent Confirmation

After the consolidated report above was drafted, a second round was run to harden its weakest points: (1) a **second Gemini pass** in the warm Deep Research thread, asked to (a) lay out the concrete 2025–2026 altitude/verbosity-control playbook, (b) *source-or-retract* the report's flagged single-engine claims, and (c) probe the two open frontiers (memory/trust-compounding and oversight-theatre); and (2) an **independent five-agent confirmation pass**, in which each skeptic agent was required to adjudicate a contested claim against a fetched **primary source** (verdict ∈ confirmed / partially-confirmed / refuted / outdated / unverifiable / likely-confabulated), with the URL and date recorded. The two were deliberately decoupled: Gemini answered first, then the independent agents checked Gemini (and the report) without seeing Gemini's reasoning as authoritative.

### The meta-finding (the round's most important outcome)

**Asked to source-or-retract its own flagged claims, the engine-two model confabulated *confirmations* rather than retracting.** It "substantiated" the misattributed CSET 68–73% vulnerability figure (the real CSET headline is ~48%; 68–73% is a 2022 Siddiq & Santos study CSET merely *cited*); it asserted the Microsoft "Council" runs "Claude Mythos" + "GPT-5.4" (the three components are real but the binding is unsupported — Microsoft names no model versions, and "Mythos" is not even GA); and it described the METR result as a selection-bias-driven *reversal* to ~faster, which **inverts** METR's own conclusion (the re-estimate is labeled unreliable and the bias points *downward*). Every one of these was caught by the independent confirmation pass precisely because each agent had to produce a primary source rather than a confident assertion.

This is live, first-person evidence for this report's central thesis: **an AI cannot be trusted to verify its own confident factual claims.** The failure mode was not hallucinating from nothing — every artifact had a real referent — but **precision and attribution errors stated with full confidence**, which is exactly the confident-but-wrong class that independent, out-of-band verification exists to catch. The operative rule, now elevated into the Recommendations: treat factual claims, statistics, dates, and named products/features as the class that *always* needs an independent check (a different agent, a primary-source fetch, or your own read) before they carry decision weight. Self-verification by the same model is not verification.

### Corrections table

| Claim (as originally framed) | Original framing | Corrected verdict (confirmation pass) | Primary source + date |
|---|---|---|---|
| "Newest models are terse by default" / "verbosity persists even under explicit conciseness instructions" | Both engines: terse by default, steer *up*; verbosity instruction-resistant | **Partially-confirmed → corrected.** YapBench's more-verbose trend is real but **mild (r=0.21)**; the "persists under explicit conciseness instructions" rider is **confabulated → removed**. Some 2026 flagships *are* tuned terser by default. Don't assume either way; steer + verify. | YapBench, arXiv 2601.00624, 2026-01-02; OpenAI GPT-5.5/5.2 guides; Anthropic prompting docs, 2026 |
| OpenAI `verbosity`, Gemini `thinking_level`, Claude `effort` knobs | Listed; Claude `effort` framed as *not* a verbosity lever | **Confirmed.** `text.verbosity` (low/med/high, default med); Gemini `thinkingLevel`/`thinkingBudget`; Claude `effort` (inside `output_config`, low→max, default high) — and `effort` **does** shape all output tokens incl. prose, so it *is* a verbosity lever. | developers.openai.com cookbook; ai.google.dev/gemini-api/docs/thinking; platform.claude.com/docs/.../effort — 2026 |
| CSET "68–73% of AI code vulnerable" | Single-engine [UNVERIFIED]; Gemini "substantiated" it | **Refuted (misattribution).** CSET's own number is ~48%; 68–73% is Siddiq & Santos (2022) cited by CSET. | CSET *Cybersecurity Risks of AI-Generated Code*, 2024-11 |
| "76% believe AI code is more secure" | Single-engine [UNVERIFIED] | **Confirmed.** Verbatim in CSET (p.9), 2023 survey of 537 workers; traces via footnote 26 to Snyk 2024. | Snyk *AI Code, Security, and Trust*, 2024 |
| Microsoft "Council" runs "Claude Mythos" + "GPT-5.4" | Likely-confabulated named feature | **Partially-confirmed.** Council is a real feature; components exist; the **model-name binding is unsupported**. | M365 Copilot Frontier blog, 2026-03-30 |
| VibeSec / OpenClaw / NextAds | All "likely confabulated, single-engine noise" | **VibeSec confirmed** (OX Security); **OpenClaw confirmed** (agent OS); **NextAds refuted** (ad-tech, irrelevant). | ox.security/vibesec/; openclaw.ai/ — 2025–2026 |
| METR "19% slower → now ~18% faster, outdated" | Earlier draft: outdated, reversed to faster | **Refuted as framed.** 19%-slower stands; the −18% re-estimate is METR-labeled **unreliable**; selection bias points the estimate *downward*. No confirmed reversal. | METR uplift update, metr.org/blog/2026-02-24-uplift-update/ |
| "38–61% of agent PRs merge with no review (MSR/EASE)" | Single stitched range | **Partially-confirmed but overstated.** 61.38% = EASE 2026 ("no review *activity*"); 38% = separate MSR paper (rejected-PR abandonment). Different populations; matched same-repo AI PRs were *less* unreviewed than human PRs. | Duma et al. EASE 2026, arXiv 2605.02273, 2026-05-04 |
| Agent memory lets trust "compound" / relax oversight | Frontier framed as possibly relaxing review | **Partially-confirmed → flipped.** Memory frameworks real (Mem0; MCP) and improve measured reliability, but trust does **not** safely compound; verification-first as memory grows. Dual-track storage + rollback. | Mem0 arXiv:2504.19413, 2025-04-28; VerificAgent arXiv:2506.02539; SSGM arXiv:2603.11768 |
| MIT Tech Review "humans-in-the-loop illusion" as a code-review source | Cited as oversight-theatre evidence | **Confirmed but scope-corrected.** Real piece — about **AI warfare**, not code review; supports the *concept*, not the software instance; commentary, not empirical. | MIT Tech Review, 2026-04-16 |
| "A validated metric distinguishes calibration from theatre" | Implied frontier might have one | **Refuted.** No validated discriminating metric exists; the reliance-measurement field is "fragmented." Use proxies (cycle-time vs. review depth; ban "the AI hallucinated" as a root cause). | Raees & Papangelis, arXiv:2604.23896, 2026-04-26 |

### Net effect of this round

The report's **Decision Brief and all eight core conclusions survive intact.** What changed is sharper calibration on five points: the verbosity playbook is now confirmed against primary vendor docs (and the "terse-by-default" overstatement is corrected in both directions); the METR claim is corrected to its accurate, non-reversed form; the "suspect" artifacts are individually adjudicated (most are real — the defect was attribution, not fabrication); both frontiers are partially resolved (memory does not license relaxed review; no validated theatre-vs-calibration metric exists); and the round produced a new, load-bearing meta-finding that *strengthens* the report's own thesis about why independent verification is non-negotiable.

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
- *YapBench* (Borisov, Gröger, Mikhael, Schreiber; tabularis.ai) — https://arxiv.org/abs/2601.00624 — 2026-01-02 *(mild more-verbose-over-time trend, r=0.21; the "instruction-resistant verbosity" rider is NOT in the paper)*
- Chhikara et al. — *Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory* — https://arxiv.org/abs/2504.19413 — 2025-04-28 *(confirmed 2026-05-31)*
- *Memori* (Memori Labs) — https://arxiv.org/html/2603.19935 — 2026-03-20 *(real third memory framework; "AgeMem" was confabulated)*
- *VerificAgent* — https://arxiv.org/pdf/2506.02539 — 2025-06 *(memory verification makes oversight efficient, NOT relaxable)*
- *SSGM — Self-Stabilizing Memory Governance* — https://arxiv.org/html/2603.11768v1 — 2026-03-12 *(verification-first / human-gated writes as memory grows)*
- *MINJA — Memory Injection Attack* — https://arxiv.org/abs/2503.03704 — 2025-03-05 *(injection-success 98.2% / attack-success 76.8%; not "95%+")*
- Raees & Papangelis — *From Trust to Appropriate Reliance: Measurement Constructs in Human-AI Decision-Making* — https://arxiv.org/abs/2604.23896 — 2026-04-26 *(reliance-measurement constructs are "fragmented" — no validated calibration-vs-theatre metric)*
- Rosbach et al. — *Stuck on Suggestions* (automation bias in pathology, MELBA) — https://arxiv.org/abs/2603.11821 — 2026-03-12 *(~7% of correct human judgments overturned by wrong AI; worse under time pressure)*
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
- OpenAI — *GPT-5 New Params and Tools (Cookbook)* — https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_new_params_and_tools — 2025-08-07 *(`text.verbosity` low/med/high, default med; confirmed 2026-05-31)*
- OpenAI — *GPT-5.2 Prompting Guide (Cookbook)* — https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide — 2026 *(measurable caps + exec-summary-first template; GPT-5.2 "generally lower verbosity")*
- OpenAI — *Prompt guidance (API Docs)* — https://developers.openai.com/api/docs/guides/prompt-guidance — 2026
- Google — *Gemini API: Thinking* — https://ai.google.dev/gemini-api/docs/thinking — 2026 *(`thinkingBudget` for 2.5 series; `thinkingLevel` minimal/low/med/high for Gemini 3+; confirmed 2026-05-31)*
- Google — *Gemini 3 Developer Guide* — https://ai.google.dev/gemini-api/docs/gemini-3 — 2026-05-29
- Anthropic — *Effort (Build with Claude)* — https://platform.claude.com/docs/en/build-with-claude/effort — 2026 *(`effort` inside `output_config`, low→max, default high; affects ALL output tokens incl. prose — a genuine verbosity lever; confirmed 2026-05-31)*
- EU AI Act — *Article 14: Human Oversight* — https://artificialintelligenceact.eu/article/14/ — 2024 (in force 2026-08-02)
- MIT Technology Review (Maoz) — *Why having humans in the loop in an AI war is an illusion* — https://www.technologyreview.com/2026/04/16/1136029/humans-in-the-loop-ai-war-illusion/ — 2026-04-16 *(SCOPE: about AI warfare, not code review — supports the concept, not the software instance; commentary, not empirical)*
- JetBrains — *Stop Sending IDE-Catchable AI Code Errors to Review* — https://blog.jetbrains.com/ai/2026/05/stop-sending-ide-catchable-ai-code-errors-to-review/ — 2026-05 *(SUSPECT: 20–25%/44% figures unsupported)*
- CSET (Georgetown) — *Cybersecurity Risks of AI-Generated Code* — https://cset.georgetown.edu/wp-content/uploads/CSET-Cybersecurity-Risks-of-AI-Generated-Code.pdf — 2024-11 *(CSET's own figure is ~48%; the 68–73% figures it cites are Siddiq & Santos 2022)*
- Snyk — *AI Code, Security, and Trust in Modern Development* — https://snyk.io/reports/ai-code-security/ — 2024 *(source of the "76% believe AI code more secure" stat via CSET footnote 26)*
- CodeRabbit — *State of AI vs Human Code Generation Report* (BusinessWire release, 470 PRs) — https://www.businesswire.com/news/home/20251217666881/en/CodeRabbits-State-of-AI-vs-Human-Code-Generation-Report-Finds-That-AI-Written-Code-Produces-1.7x-More-Issues-Than-Human-Code — 2025-12-17 *(1.7× issues, 2.74× XSS — confirmed; vendor self-report)*
- Microsoft 365 — *Copilot Cowork / Model Council now available in Frontier* — https://www.microsoft.com/en-us/microsoft-365/blog/2026/03/30/copilot-cowork-now-available-in-frontier/ — 2026-03-30 *(Council feature real; runs "Anthropic and OpenAI" — no model-name binding to "Claude Mythos"/"GPT-5.4")*
- OX Security — *VibeSec* — https://www.ox.security/vibesec/ — 2025–2026 *(confirmed real; secures AI/"vibe-coded" code)*
- OpenClaw — *The Operating System for People Who Actually Work* — https://openclaw.ai/ — 2026 *(confirmed real; self-hosted AI-agent OS)*

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

*Engine-two report (Gemini Deep Research, Gemini Pro, 2026-05-31) was used for triangulation throughout; its source list is in `raw/gemini-sources.md`, and its follow-up answers in `raw/gemini-followups.md`. The independent five-agent confirmation pass (`validation/confirmation-pass.json` + `validation/confirm-*.md`) adjudicated the formerly Gemini-only artifacts against primary sources: VibeSec, OpenClaw, and the "76%" Snyk stat are **confirmed real**; the Microsoft "Council" feature is **real** but its "Claude Mythos"/"GPT-5.4" model binding is **unverified**; the CSET "68–73%" figure is a **misattribution** (CSET's own number ~48%); and "NextAds" is **irrelevant ad-tech**. The defects were precision and attribution, not wholesale fabrication — see the Addendum and the meta-finding.*
