---
content_origin: avfl-consolidation
date: 2026-05-20
topic: "Gas Town as dispatcher/coordinator for Momentum"
profile: full
corpus_files: 8
validators_run: 8
lenses: [factual-accuracy, completeness, consistency, bias-balance]
total_findings: 35
score: 0
grade: F
score_raw: -32
---

# AVFL Validation Report
## Gas Town / Gas City Dispatcher Research Corpus

**Date:** 2026-05-20
**Profile:** Full (4 lenses × 2 reviewers = 8 validators)
**Corpus:** 8 raw research files + gemini-deep-research-output.md
**Score:** 0/100 (floored from -32) — Grade F

---

## Score Breakdown

| Severity | Count | Weight | Raw Impact |
|---|---|---|---|
| CRITICAL | 1 | -20 | -20 |
| HIGH | 7 | -8 each | -56 |
| MEDIUM | 17 | +0 | 0 |
| LOW | 10 | +0 | 0 |
| **Total raw** | | | **-76** |
| **Score (floored at 0)** | | | **0/100** |

*Note: Score formula applies negative weights only to CRITICAL and HIGH findings. MEDIUM/LOW findings are flagged but do not reduce the score. Raw score floored at 0.*

---

## CRITICAL Findings (1)

### CON-001 — Directly Contradictory Adoption Verdict
**Lens:** Consistency  
**Confidence:** HIGH  
**Source A:** `research-maturity-production-readiness.md:169`  
**Source B:** `research-adoption-path-risks.md:254`

**The contradiction:**

Source A (maturity): *"Gas Town's architectural model is a poor fit. Momentum's orchestration needs are fundamentally different from Git-worktree-parallel software development."*

Source B (adoption): *"Gas City is architecturally the right tool for Momentum's dispatcher gap. The Orders system maps directly to what Momentum needs: event-triggered dispatch of skill formulas without human intervention."*

These are the direct, opposite verdicts from the two files most relevant to the adoption decision. The maturity file evaluates Gas Town (v1.0) and concludes poor fit. The adoption file evaluates Gas City (the SDK successor) and concludes right tool. The corpus does not clarify whether this reflects a genuine Gas Town ↔ Gas City distinction (two different products with different fitness) or an irreconcilable disagreement between researchers.

**Resolution required:** The synthesis must explicitly attribute each verdict to the correct product (Gas Town vs Gas City), clarify why Gas Town is a poor fit while Gas City may not be, and adjudicate the net recommendation. The two verdicts may both be correct if Gas Town = wrong tool and Gas City = right tool, but this must be stated explicitly.

---

## HIGH Findings (7)

### CON-002 — Gas City v1.0.0 Release Date: Three Conflicting Values
**Lens:** Factual Accuracy  
**Confidence:** HIGH  
**Files:**
- `research-maturity-production-readiness.md:42` — April 21, 2026
- `research-gas-city-architecture.md:176` — "announced April 24, 2026"
- `research-adoption-path-risks.md:175` — "Gas City 1.0.0 was released April 27, 2026"

The same repository's v1.0.0 release carries three dates across three files. Note: the architecture file uses the word "announced" rather than "released," which may be a legitimate distinction (announcement post vs. tag date). The maturity file matches the Gas Town v1.0.0 date (April 21), which may indicate a copy error. The synthesis must use a single verified date.

**Recommended resolution:** Treat April 27 as most likely the official v1.0.0 release date based on the adoption file's precision ("Gas City 1.0.0 was released April 27, 2026 — less than one month old as of this writing"). April 21 = Gas Town v1.0.0. April 24 = Gas City announcement blog post. But this should be verified against the GitHub tag.

---

### CON-003 — MEOW Acronym Expansion Wrong in Dispatch File
**Lens:** Factual Accuracy  
**Confidence:** HIGH  
**Source (wrong):** `research-dispatch-routing-primitives.md:168` — "MEOW stack (Molecules, Epics, Orders, Wisps)"  
**Source (canonical):** Multiple files — "Molecular Expression of Work" describes Molecules

The dispatch file attributes a spurious, letter-by-letter expansion to MEOW ("Molecules, Epics, Orders, Wisps"). The canonical expansion from architecture documentation is "Molecular Expression of Work" — describing the encoding format of multi-step agentic work as a molecular metaphor. "Epics" and "Wisps" are not named MEOW components. This is a practitioner-sourced misquote (attributed to Augusteo blog post).

**Resolution:** The dispatch file's MEOW expansion must be corrected. The synthesis should not reproduce "Molecules, Epics, Orders, Wisps."

---

### CON-004 — MEDIUM Escalation Routing: Deacon vs Mayor
**Lens:** Consistency  
**Confidence:** HIGH  
**Sources:**
- `research-dispatch-routing-primitives.md:305` — "MEDIUM (P2): tracked in Beads, surfaced at next patrol" (implies Deacon)
- `research-human-in-loop-oversight.md:58` — "medium: bead + mail to Mayor"
- `research-human-in-loop-oversight.md:22` — "Mayor also receives HIGH and MEDIUM escalations"

Three different targets for the same escalation level. The dispatch file says MEDIUM surfaces at next Deacon patrol (no explicit Mayor mail). The HITL file says MEDIUM goes directly to Mayor by mail. These are meaningfully different from an oversight perspective: in one model the Mayor is not actively notified on MEDIUM; in the other it is.

**Resolution required:** Determine which escalation.json routing is canonical. This affects how the synthesis describes the HITL escalation chain.

---

### CON-005 — Go Minimum Version: 1.23 vs 1.25
**Lens:** Factual Accuracy  
**Confidence:** HIGH  
**Sources:**
- `research-coordination-model-comparison.md:107` — "Go 1.23+"
- `research-gas-city-architecture.md:207` — "Go 1.25+ (95.5%)"
- `research-adoption-path-risks.md:41` — "Go ≥1.25"

The coordination comparison file cites Go 1.23+; the other two files cite 1.25+. The architecture file cites the official GitHub repository as source. 1.25 is the majority position and likely correct — 1.23 appears to be a stale prerequisite from an earlier Gas City release.

**Resolution:** Use Go ≥1.25 as the minimum requirement. Flag the 1.23 figure as likely outdated.

---

### CON-006 — "Beads Already Adopted" Misrepresents Actual Project State
**Lens:** Factual Accuracy  
**Confidence:** HIGH  
**Source (wrong):** `research-adoption-path-risks.md:12` and throughout — "Beads is already being adopted as a task-tracking layer"

**Actual Momentum project state:** The `beads-dual-write-spike` story is at `ready-for-dev` — not deployed, not integrated. Beads is not yet operational in Momentum. This claim materially affects the adoption path analysis: the file reasons about Gas City integration partly on the premise that the Beads layer is "already" present, which would reduce integration complexity. If Beads is not yet deployed, the integration complexity is higher and the Dolt stability risk affects both Beads adoption and Gas City adoption simultaneously.

**Resolution required (human input):** This is a project-state question, not a corpus fact question. Clarification from the practitioner is needed: is Beads operationally live in Momentum? If no, the adoption file's framing of "Beads already adopted" needs to be corrected in synthesis.

---

### CON-007 — Stars Cited Despite Explicit Methodology Rejection
**Lens:** Bias & Balance  
**Confidence:** HIGH  
**Source:** `research-maturity-production-readiness.md:118-121`

The maturity file cites both GitHub star counts (15.5k for Gas Town, 789 for Gas City) and then immediately notes: "Per research methodology, stars are discarded as a maturity signal." Citing then discarding in the same paragraph is contradictory — the data is live in the corpus even if the researcher flagged it. The synthesis must not include star counts. Including them despite the flagging creates a bias risk where readers form impressions from the numbers even when told to discard them.

**Resolution:** Do not include star counts in the final document. The maturity file's note about methodology is correct; execution was inconsistent.

---

### CON-008 — PoC Central Mechanism Requires Deferred MCP Support
**Lens:** Completeness  
**Confidence:** MEDIUM  
**Source A:** `research-adoption-path-risks.md` — PoC plan centered on "Momentum skills as Gas City formulas"  
**Source B:** `raw/gemini-deep-research-output.md` (Follow-up 1) — "Hold off on native MCP integration: Gas City does not yet offer full runtime support for [MCP]"

The adoption file's primary PoC recommendation is to wire Momentum skills (Claude Code-based) as Gas City formula steps. Claude Code skills are invoked via MCP toolchains. Gas City explicitly deferred MCP runtime support from PackV2. This means the recommended PoC's central mechanism depends on infrastructure that doesn't yet exist. The adoption file does not surface this contradiction.

**Resolution:** The synthesis must flag this gap explicitly. The PoC must either: (a) avoid MCP-dependent skill invocations in the initial phase, using shell exec patterns instead; or (b) acknowledge the PoC is blocked until Gas City ships MCP follow-on work.

---

## MEDIUM Findings (17)

*MEDIUM findings are flagged for synthesis attention but do not reduce the score. They represent precision gaps, thin evidence, or areas where the corpus is incomplete rather than wrong.*

### MED-001 — Dolt Concurrency Bug Impact Understated
`research-maturity-production-readiness.md` mentions Dolt Issue #1930 (concurrent writes) as a known bug. The corpus cites "~23,759 restarts over 6 hours" but does not quantify the impact in Momentum-relevant terms. The synthesis should include a concrete risk statement: "Under concurrent multi-agent write patterns, Dolt may require agent restarts at a rate incompatible with automated sprint execution." Downplaying this as a minor note misrepresents the risk.

### MED-002 — GUPP Principle Evidence is Practitioner-Only
The Gas Town Unified Propulsion Principle (GUPP) is described as the core execution mandate — "If there is work on your Hook, YOU MUST RUN IT." This is cited from a practitioner blog (Augusteo) but not from official docs. Accuracy is likely high given Yegge's prior writing, but the synthesis should flag GUPP as practitioner-attributed until confirmed in official documentation.

### MED-003 — NDI (Nondeterministic Idempotence) Mischaracterized as Guarantee
`research-gas-city-architecture.md` describes NDI as a "design goal" in one place and as a property in another. NDI is not a formal guarantee — it is a design principle that the system will retry until acceptance criteria are met. The synthesis must not describe NDI as a reliability guarantee.

### MED-004 — Refinery / Bors-Style Merge Queue Not Addressed for Momentum
The corpus describes Gas Town's Refinery (merge processor using bisection) in detail but does not evaluate whether Momentum's single-developer + `git push requires approval` discipline would conflict with it. This is a completeness gap: Momentum's git discipline requires explicit push approval, while Gas Town's Refinery expects autonomous merge authority. Resolution path is not specified.

### MED-005 — Sprint-Planning and Retro Mapping Thinly Supported
`research-momentum-integration-mapping.md` states sprint-planning and retro map "poorly" to Gas Town but does not specify concrete blockers. The synthesis needs concrete reasons (e.g., retro requires synthesizing conversation history which Gas Town has no primitive for; sprint-planning requires human judgment on scope which the Mayor cannot substitute for).

### MED-006 — Gas City Orders System Cron Support Evidence is Gemini-Only
The follow-up Q&A in `gemini-deep-research-output.md` claims Gas City Orders support cron-like scheduling. This is not confirmed in the 8 subagent research files. The synthesis should flag cron-based ordering as Gemini-attributed pending verification against official docs.

### MED-007 — "Maintains Mode" for Gas Town Overstated
`research-maturity-production-readiness.md:34` says Gas Town "has largely been in maintenance mode." This is Yegge's characterization in a blog post. However, the same maturity file notes 155 open issues and v1.1.0 released May 7 with substantive changes. "Maintenance mode" may not accurately reflect active issue volume. The synthesis should not treat Gas Town as frozen.

### MED-008 — Slack Pack Source Not Independently Verified
`gemini-deep-research-output.md` (Follow-up 3) mentions a "gascity-packs repository includes a slack-pack" for team notifications. This was not found in the 8 subagent research files. The synthesis should caveat this as Gemini-attributed and potentially unverified.

### MED-009 — Moshi iOS App Unverified
`gemini-deep-research-output.md` (Follow-up 3) mentions "Moshi (an iOS terminal built for agentic workflows)" as a community tool for mobile oversight. No other source in the corpus confirms this tool exists. Omit from synthesis or flag as unverified.

### MED-010 — Mayor Reliability Acknowledged but Unquantified
`research-human-in-loop-oversight.md:22` notes "reviewers note the Mayor itself sometimes needs manual prodding, weakening this buffer." This is a reliability concern for the core coordination agent but is not quantified. The synthesis should acknowledge Mayor reliability as an open risk without overstating it.

### MED-011 — Convoy Dashboard Pull-vs-Push Gap Needs More Context
The corpus notes the human gate system is pull-based (developer must poll `bd gate list` or check mail). The gemini Q&A notes `gt dashboard` with auto-refresh. The synthesis should clarify that auto-refresh shows status but does NOT proactively push notifications — the developer still must be watching the dashboard.

### MED-012 — PackV1 Deprecation Timeline Not Clear
`gemini-deep-research-output.md` (Follow-up 1) describes PackV1 as "deprecated" with `gc doctor --fix` migration tooling available. But the corpus does not specify when PackV1 support is fully dropped. The synthesis should not assume immediate PackV1 removal.

### MED-013 — Gas Town "Only Works With Handful of Agents" Not Quantified
`research-maturity-production-readiness.md:93` quotes Yegge: "Gas Town only works with a handful of agents today." Supported agents are listed as Claude Code, GitHub Copilot, and "a small number of others." But Momentum's model uses multiple Claude Code sessions — it's unclear whether running multiple simultaneous Claude Code instances in Gas Town is tested/supported or whether there are per-agent-type constraints.

### MED-014 — Beads CLI Version Requirements Potentially Stale
`research-adoption-path-risks.md:38` lists "bd (Beads CLI) | Yes, ≥1.0.0" as a prerequisite. Beads is at v1.1.0+ as of this writing. The synthesis should use the current Beads version floor rather than ≥1.0.0.

### MED-015 — HITL Gate "No Dashboard" Statement Contradicted by gt dashboard
`research-human-in-loop-oversight.md:44` states Gas Town "does not currently expose a dashboard view that says '3 human approval gates are waiting for you.'" But the gemini output mentions `gt dashboard` with auto-refresh status display. These may both be correct (dashboard shows status but doesn't enumerate pending gate counts), but the synthesis should reconcile this rather than stating a flat "no dashboard."

### MED-016 — Coordination Model Comparison Uses 20-30 Agent Scale Assumption
`research-coordination-model-comparison.md` frames the comparison assuming Gas Town is designed for 20-30 parallel agents. This is the Gas Town design scale. For Momentum (4-8 agents, solo developer), the coordination overhead has different cost characteristics. The synthesis should explicitly note that the "overbuilt" conclusion applies at Momentum's specific scale.

### MED-017 — "gc doctor --fix" Completeness Unclear
`gemini-deep-research-output.md` (Follow-up 1) states "gc doctor --fix migration tooling" converts PackV1 to PackV2 setups. However, the same Q&A notes some PackV2 capabilities were deferred. The synthesis should not imply `gc doctor --fix` is a complete migration path — it converts the directory layout but post-migration work may still be required.

---

## LOW Findings (10)

*LOW findings represent minor precision issues, hedging language, or phrasing recommendations. Not score-affecting.*

### LOW-001 — "Steve Yegge solo" framing in architecture file understates team
Architecture file describes Gas Town as Yegge's project. Maturity file correctly names the full core team (Matt Beane, Chris Sells, Julian Knutsen, Tim Sehn, Brendan Hopper). Synthesis should use the team characterization.

### LOW-002 — "Hacker News discussion" cited as community evidence is weak
Multiple files cite HN discussion as evidence of community reach. This is appropriate context but should not be used as a primary signal of adoption quality.

### LOW-003 — "Nondeterministic Idempotence" phrasing varies
Some files write NDI, others write out "Nondeterministic Idempotence." Synthesis should pick one form and use it consistently.

### LOW-004 — Beads "Molecular" metaphor explanation inconsistent
Architecture file explains Beads' Molecule metaphor clearly; dispatch file uses "Molecule" without explanation. Synthesis should include one consistent explanation.

### LOW-005 — "Convoy" and "Beads convoy" used interchangeably
Some files distinguish Convoys (coordinating envelopes) from Beads (atomic work items); others blur the distinction. Synthesis should define both terms explicitly at first use.

### LOW-006 — `gt sling` vs `bd sling` command form inconsistency
Some files use `gt sling`, others use `bd sling`. These may be aliased or may be different tools. Synthesis should verify and use one consistent command form.

### LOW-007 — "Polecat" plural form varies (Polecats vs Polecat workers)
Cosmetic consistency issue. Not affecting accuracy.

### LOW-008 — Gemini follow-up Q&A appended without heading hierarchy
The gemini output file appends follow-up sections without a clear top-level heading to distinguish them from the main report body. The `## Follow-up` section heading exists but the frontmatter note that "main body was not persisted" is buried. Synthesis agent should read this carefully to avoid treating the Q&A as the primary report.

### LOW-009 — Date-of-writing context missing from adoption file
The adoption file says "less than one month old as of this writing" but doesn't state the writing date. Reader assumes May 2026 based on scope.md, but this should be explicit.

### LOW-010 — "Boot the Dog" phrasing unexplained
Architecture file mentions "Boot the Dog is a specialized Dog that heartbeats the Deacon every 5 minutes." This unexplained idiom may confuse readers. The synthesis should either explain it briefly or omit it.

---

## Corpus Coverage Assessment

| Sub-Question | Coverage | Evidence Quality |
|---|---|---|
| 1. Gas Town/Gas City architecture | High | OFFICIAL + PRAC |
| 2. Gas Town ↔ Beads relationship | High | OFFICIAL + PRAC |
| 3. Dispatch primitives | High | OFFICIAL + PRAC + Gemini |
| 4. HITL oversight | Medium | OFFICIAL + PRAC (some gaps in gate UX) |
| 5. Maturity/production-readiness | High | OFFICIAL + PRAC |
| 6. Momentum workflow mapping | Medium | PRAC (no official validation) |
| 7. Coordination model comparison | Medium | Inference-heavy |
| 8. Adoption path/risks | Medium | Inference-heavy; CON-001 unresolved |

---

## Fixer Action Plan (Pre-Synthesis Mechanical Fixes)

The following findings can be resolved without human input — the Fixer can address them by editing the raw files:

| Finding | File | Fix |
|---|---|---|
| CON-003 | research-dispatch-routing-primitives.md:168 | Replace "MEOW stack (Molecules, Epics, Orders, Wisps)" with "MEOW stack ('Molecular Expression of Work')" |
| CON-005 | research-coordination-model-comparison.md:107 | Change "Go 1.23+" to "Go ≥1.25" |
| CON-007 | research-maturity-production-readiness.md:118-119 | Remove star count citations; retain other metrics |
| LOW-001 | research-gas-city-architecture.md | Add team member names alongside Yegge |

Findings that require human input before synthesis: **CON-001** (verdicts), **CON-006** (Beads adoption state).

---

## Recommendations for Phase 4 Q&A

Present these two questions to the practitioner before synthesis:

1. **CON-001:** The maturity file says Gas Town is a "poor fit" for Momentum; the adoption file says Gas City is "the right tool." Do you read these as evaluating different products (Gas Town ≠ Gas City) or as a genuine disagreement? Should the synthesis recommend Gas City while ruling out Gas Town?

2. **CON-006:** The adoption file assumes "Beads is already being adopted" in Momentum. Is Beads operationally live in the project? Or is the `beads-dual-write-spike` story still at `ready-for-dev`, meaning Beads is not yet deployed?
