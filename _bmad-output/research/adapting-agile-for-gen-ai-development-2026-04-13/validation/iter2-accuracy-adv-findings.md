# Factual Accuracy — Adversary Findings (Iteration 2)

**Lens:** Factual Accuracy
**Reviewer framing:** Adversary (intuitive, pattern-aware, hunch-driven)
**Scope:** 9 corpus files in `/raw/` after iteration-1 fix pass
**Skepticism:** Level 2 (Balanced)
**Mode:** Re-validation — verify fixes did not introduce new accuracy problems; confirm high-risk unfixed claims; do NOT re-report fixed issues.

## Summary

The iteration-1 fix pass closed several CRITICAL findings cleanly: Casey West dating/characterization is now consistent across files; Kinetic Enterprise carries an explicit `[UNVERIFIED]` flag with the SAP-trademark disambiguation; the Harness Engineering / OpenAI naming collision now has a disambiguation note; the AI-DLC three-phase description (Inception/Construction/Operations) is accurate to the AWS public framing; the MIT Project NANDA claim was downgraded with a `[UNVERIFIED]` blockquote pointing to BCG as a stronger alternative; and the METR 19% slowdown correction is accurate. Most `[UNVERIFIED]` tags added in iter-1 are appropriate.

However, several of the original critical/high-severity issues were NOT fixed in this pass and remain in the corpus: **Silken Net** (Shape Up + NASA TRL) is still presented as a real practitioner case with no source; **V-Impact Canvas** is still named as if it were an established framework with no citable origin; **Architect of Intent** persists as a named role in the thought-leader file with no provenance; **OpenSpec / Fission-AI** attribution is still in the body un-flagged despite being unverifiable; and the precision-suspicious **CodeRabbit (10.83 / 6.45)** and **LinearB (5.3× / 2.47× / 8.1M PRs / 4,800 teams / 42 countries)** statistics still cite landing pages or generic blog URLs without primary-report depth links.

The fix pass also introduced **two new accuracy concerns**: (1) the AI-DLC section now repeats an unverified "10-15× productivity gains" claim attributed to Wipro and Dun & Bradstreet without flagging it, even though the original adversary report flagged it; and (2) the new EARS/Kiro paragraph asserts Kiro launched in **July 2025** — consistent with the acceptance-criteria subagent file — but the gemini main body now duplicates this claim without independent sourcing, propagating a date that was originally only inferred.

**Findings by severity:**
- Critical: 0 (all original criticals addressed or properly flagged)
- High: 6 (unfixed from iter-1; one new)
- Medium: 4 (one new fix-introduced)
- Low: 2

**Total findings:** 12

---

## Findings

### ACCURACY-026
- **severity:** high
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Follow-up Q1 — Shape Up section (lines 205-207)
- **description:** ITER-1 did NOT fix the Silken Net hallucination flagged as ACCURACY-002. The text still reads "Teams like Silken Net have 'completely overhauled' their architecture, abandoning Agile for a hybrid of Shape Up and NASA's Technology Readiness Levels (TRL)" with no `[UNVERIFIED]` tag and no citation. The fix log (fix-log-gemini.md) lists only 7 fixes, none addressing this finding. Silken Net remains un-traceable to any public case study; Shape Up + TRL hybrid is not documented anywhere as a methodology.
- **evidence:** Gemini file lines 205-207 unchanged from iter-1: "Teams like Silken Net have 'completely overhauled' their architecture, abandoning Agile for a hybrid of Shape Up and NASA's Technology Readiness Levels (TRL)." No flag added; no source in Sources list.
- **suggestion:** Apply the same `[UNVERIFIED]` blockquote treatment given to Kinetic Enterprise. Either remove the Silken Net example or wrap it in an explicit unverified flag noting that no public case study supports the claim and the Shape Up + TRL hybrid is not a documented practice.

### ACCURACY-027
- **severity:** high
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Solving the 'Spec-Correct, Value-Zero' Problem — V-Impact Canvas section (lines 80-86)
- **description:** ITER-1 did NOT fix the V-Impact Canvas hallucination flagged as ACCURACY-005. The framework is still presented as a real, named artifact ("The Architect's V-Impact Canvas has been introduced as a stabilizing mechanism...") with three named bullets (Architectural Intent, Design Governance, Impact and Value). No `[UNVERIFIED]` flag was added; the Sources list still contains only a bare `infoq.com` reference. The framework name returns no public results in either Thoughtworks, Fowler, or InfoQ archives. This is the highest-density invented-framework risk left in the corpus.
- **evidence:** Lines 80-86 unchanged from iter-1; same text "The Architect's V-Impact Canvas has been introduced..." present without flag. The phrase "oil and water moment in architecture" referenced in iter-1 ACCURACY-005 also still appears unflagged.
- **suggestion:** Apply `[UNVERIFIED]` flag to the entire V-Impact Canvas subsection, or remove it. If retained, demand an InfoQ deep link or Thoughtworks article URL that uses the exact name.

### ACCURACY-028
- **severity:** high
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Follow-up Q2 — BMAD Quick Flow / Barry table row (line 253)
- **description:** ITER-1 did NOT address the BMAD "Barry" persona originally flagged as ACCURACY-003. The table row remains: "BMAD Quick Flow | Uses 'Barry,' an elite solo dev persona, to move from a 'Quick Spec' to 'Quick Dev' in a lean path." This claim is independently checkable against the user's own environment — the available Skill list shows `bmad-quick-dev` as a real BMAD skill, but no public BMAD documentation references a "Barry" persona. The fix-log explicitly does not mention this finding; no `[UNVERIFIED]` tag was added. Given the user's intimate familiarity with BMAD (the corpus is being authored within Momentum, which integrates BMAD), retaining a fabricated persona name is a high-credibility risk for downstream readers.
- **evidence:** Line 253 unchanged: BMAD Quick Flow row attributes "Barry" as elite solo dev persona. No fix log entry; no UNVERIFIED tag. The current Skill list available in this environment includes `bmad-quick-dev` but no Barry persona reference.
- **suggestion:** Either remove the "Barry" attribution and rewrite the row to describe what `bmad-quick-dev` actually does (per the available skill description: "Implements any user intent, requirement..."), or flag the entire row `[UNVERIFIED]` with explicit note that "Barry" persona is not present in public BMAD documentation.

### ACCURACY-029
- **severity:** high
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:Follow-up Q2 — OpenSpec / Fission-AI (line 231) and Q3 OpenSpec table row (line 296)
- **description:** ITER-1 did NOT fix the OpenSpec / Fission-AI attribution flagged as ACCURACY-012. Two body locations still reference OpenSpec without UNVERIFIED tags: line 231 ("This framework, developed by Fission-AI...") and line 296 (table row "OpenSpec | Markdown-driven 'Propose-Apply-Archive' loop..."). The Fission-AI attribution remains unverifiable. There is a real OpenSpec project on GitHub but the "Fission-AI" authorship attribution is the specific fabrication risk.
- **evidence:** Lines 231 and 296 unchanged. Sources list at line 304 does include "infoq.com/news/2026/02/ai-agile-manifesto-debate, sjwiggers.com/2026/02/28/ai-is-reshaping-software-development" but neither resolves the Fission-AI claim.
- **suggestion:** Drop the "developed by Fission-AI" attribution entirely (the framework can be described without specifying who built it), or flag the line `[UNVERIFIED — Fission-AI authorship unconfirmed]`. The OpenSpec table row is less risky (no attribution) and could remain.

### ACCURACY-030
- **severity:** high
- **dimension:** traceability
- **location:** research-cognitive-load-inversion.md:lines 23, 33 (LinearB and CodeRabbit precision stats)
- **description:** ITER-1 did NOT address the precision-statistics provenance issues flagged as ACCURACY-010 and ACCURACY-011. The LinearB claims (8.1 million PRs, 4,800 teams, 42 countries, 5.3×, 2.47×, 2× faster) still cite only the landing page `https://linearb.io/resources/engineering-benchmarks`, not a deep link to the published report. The CodeRabbit precision figures (10.83 vs 6.45, 2.74×, 75%) cite a single blog URL but the "10.83" / "6.45" decimal precision suggests verbatim figures that should be quotable from the report itself. No spot-check confirmation was done in the fix pass.
- **evidence:** Lines 23 ("agentic AI PRs sit idle 5.3× longer..." citing linearb.io landing page) and 33 ("AI-authored code produced 10.83 issues per PR vs. 6.45 for human-only PRs") unchanged from iter-1. Fix logs do not list either statistic as addressed.
- **suggestion:** Either spot-check the underlying CodeRabbit PDF and LinearB report and replace landing-page URLs with deep links + page references, or add `[UNVERIFIED — precise figures not spot-checked against primary report]` annotations. The risk is that downstream consumers will quote these figures as "from research" when they originate from vendor marketing aggregations.

### ACCURACY-031
- **severity:** high
- **dimension:** correctness
- **location:** research-ceremony-rhythm-alternatives.md:line 88 (AWS AI-DLC enterprise customer claim)
- **description:** ITER-1 did NOT address ACCURACY-015. The line "Adopted by enterprise customers (Wipro, Dun & Bradstreet) with reported 10-15x productivity gains" remains unflagged. Notably, the AVFL fix pass for AI-DLC (per fix-log-gemini.md FIX 2) corrected the AI-DLC framework description in the gemini file but did not propagate consistency checks to research-ceremony-rhythm-alternatives.md, which carries the unverified productivity-gain claim. The customer-name + multiplier combination is the classic pattern for hallucinated case studies.
- **evidence:** Line 88 unchanged from iter-1; no `[UNVERIFIED]` tag added. The AWS DevOps blog cited at line 92 is real but does not, on its public face, name Wipro and Dun & Bradstreet with "10-15x" specifically — this requires verification.
- **suggestion:** Either find the specific AWS customer story citing each company + multiplier, or rewrite as `[UNVERIFIED — enterprise adoption examples and productivity multiplier not independently confirmed]`. Drop the specific multiplier if not directly quotable.

### ACCURACY-032 [NEW — INTRODUCED BY ITER-1 FIX]
- **severity:** medium
- **dimension:** correctness
- **location:** gemini-deep-research-output.md:lines 61-63 (new EARS/Kiro paragraph added in FIX 6)
- **description:** The iter-1 fix added a new "EARS Notation and Spec-Driven Tooling" paragraph asserting "Amazon's **Kiro IDE** (July 2025) made EARS central to its spec-driven workflow." The "July 2025" date is consistent with the acceptance-criteria subagent file (which states "Amazon's Kiro IDE, which launched public preview in July 2025"). However, the gemini file is now propagating a date that originated in a sibling subagent file rather than from a primary kiro.dev source. The cross-file propagation of a single dated assertion without independent verification creates a brittle citation chain. Additionally, the new paragraph is tagless — it would benefit from `[CROSS-REF — see research-acceptance-criteria-ai-literal.md, sourced to kiro.dev/blog/introducing-kiro/]` or similar provenance.
- **evidence:** Gemini file lines 61-63 (new in iter-1) state "Amazon's **Kiro IDE** (July 2025)" without source tag. Acceptance-criteria file line 66-68 cites kiro.dev as source for the same date. No verification that "July 2025" is the actual public-preview date appears in either file.
- **suggestion:** Add a source tag to the gemini paragraph (e.g., `[OFFICIAL — kiro.dev]`) and confirm the July 2025 launch date against kiro.dev's introducing-kiro post. If the actual date differs (some sources note Kiro went GA in mid-2025 but exact month varies), correct.

### ACCURACY-033 [NEW — INTRODUCED BY ITER-1 FIX]
- **severity:** medium
- **dimension:** logical_soundness
- **location:** gemini-deep-research-output.md:lines 116-120 (revised "Mob Elaboration and Construction" + AI-DLC paragraph)
- **description:** The iter-1 fix correctly removed the misattribution of mob rituals to AI-DLC and clarified that AI-DLC is a three-phase model (Inception/Construction/Operations). However, the revised paragraph creates a structural inconsistency with the section heading "Mob Elaboration and Construction" — the heading still names mob rituals as the section topic, but the second paragraph describes AI-DLC as explicitly NOT mob-based. A reader scanning by heading will get the misleading impression that mob rituals are the dominant pattern; the heading should be revised to reflect the dual coverage (e.g., "Mob Rituals (Thoughtworks 3-3-3) and Phase Gates (AWS AI-DLC)") or split into two sections. Logical soundness: the heading no longer matches the paragraph content.
- **evidence:** Section heading at line 116 reads "### Mob Elaboration and Construction" but lines 118-120 now devote significant space to explaining AI-DLC's non-mob approach. The section now covers two distinct mechanisms under one mob-titled heading.
- **suggestion:** Rename the section heading to reflect the dual mechanisms covered (mob rituals + phase gates), or split into two subsections. Minor structural cleanup.

### ACCURACY-034
- **severity:** medium
- **dimension:** correctness
- **location:** research-thought-leader-frameworks-agile-ai.md:line 187 (Architect of Intent)
- **description:** Original adversary report flagged "Architect of Intent" implicitly under ACCURACY pattern observations but did not assign a discrete ID. The term appears only in this subagent file (line 187) attributed to Wolf Crywolfe's dev.to article. While Wolf Crywolfe is a real dev.to author and the article URL is plausible, "Architect of Intent" as a named role is not independently corroborated outside that single source. The label "[PRAC — dev.to, 2025]" provides correct provenance, so this is borderline acceptable. No fix needed if the dev.to article actually contains this term — but worth flagging that the term has not propagated beyond a single secondary source.
- **evidence:** Line 187 lists "Architect of Intent as the evolved human role" attributed to the Wolfe Synthesis. No corroborating sources.
- **suggestion:** Spot-check the dev.to article (https://dev.to/crywolfe/the-agentic-manifesto-why-agile-is-breaking-in-the-age-of-ai-agents-1939, source line 295) to confirm it contains the exact phrase "Architect of Intent." If yes, no change needed — provenance is proper. If no, remove or reword.

### ACCURACY-035
- **severity:** medium
- **dimension:** correctness
- **location:** research-thought-leader-frameworks-agile-ai.md:lines 100-106 (Looking Glass 2026 five AIFSD trends)
- **description:** ITER-1 did NOT address ACCURACY-007. The five named AIFSD trends (GBDEs, Continuous Learning Delivery Systems, Neural Software Twins, Synthetic Engineers, Multimodal Collaboration) remain listed verbatim with `[OFFICIAL]` tags pointing to thoughtworks.com/insights/looking-glass/looking-glass-2026/AI-and-software-delivery. The names "Neural Software Twins" and "Synthetic Engineers" in particular have an LLM-coined feel — they should be spot-checked verbatim against the actual Looking Glass report. The deep URL is provided, which is better than iter-1's bare-domain critique, so this drops from HIGH to MEDIUM. But verification was not actually performed.
- **evidence:** Lines 100-106 list five trends unchanged from iter-1. URL provided (line 288) is a deep link, but the verbatim trend names have not been confirmed via fetch.
- **suggestion:** Spot-check the Looking Glass 2026 deep URL. If any trend name is paraphrased rather than verbatim, mark it as such.

### ACCURACY-036
- **severity:** low
- **dimension:** correctness
- **location:** research-cognitive-load-inversion.md:line 12, 33 (other precision figures)
- **description:** Beyond the LinearB/CodeRabbit issues already raised, this file contains additional precision-suspicious figures: "21% more tasks", "98% more PRs", "91% review time increase" (line 12); "4.3 minutes vs 1.2 minutes" senior engineer review times (line 35); "29% trust... down 11 percentage points from 2024" (line 39); "26% of senior engineers... 68% reporting quality improvements" (line 41). These are all attributed to specific URLs (newsletter.eng-leadership.com, blog.logrocket.com, stackoverflow.blog, etc.) but the cumulative density of high-precision percentages from secondary newsletter/blog sources is the classic LLM-aggregation hallucination signature flagged in iter-1's "Patterns Observed" section. Iter-1 specifically called this out as a pattern but did not fix individual instances.
- **evidence:** Multiple precision figures across lines 12, 35, 39, 41. All cite sources but none have been spot-checked.
- **suggestion:** No urgent action required given proper attribution to secondary sources. Recommend a single editor's note at the top of the statistics-heavy sections clarifying that figures are reported as cited and have not been independently verified against primary research.

### ACCURACY-037
- **severity:** low
- **dimension:** correctness
- **location:** research-feature-unit-user-value.md:line 28 (Marty Cagan SVPG attribution)
- **description:** Line 28 carries `[UNVERIFIED — widely attributed to SVPG; svpg.com/product-vs-feature-teams/ returned 403]`. This is appropriate iter-1 hygiene — the UNVERIFIED tag is correct and the reason is documented. Minor observation: the same Cagan body of work IS cited at line 32 via a working age-of-product.com link, so the "product team vs. feature team" distinction is sourceable through that secondary URL even if SVPG's direct page is 403. Optional improvement: cross-reference the working age-of-product.com URL within the line 28 unverified note so readers know an alternative source exists.
- **evidence:** Line 28 has 403 note; line 32 has working age-of-product.com URL for the same conceptual material.
- **suggestion:** Optional — cross-link the working secondary source in the line 28 unverified note. Not blocking.

---

## Patterns Observed in Iteration 2

1. **Critical findings closed cleanly.** Casey West, Kinetic Enterprise, Harness Engineering disambiguation, AI-DLC three-phase correction, MIT NANDA, and METR 19% characterization are all properly addressed. The iter-1 fix pass executed faithfully on the items it took on.

2. **Several high-severity items deferred without flag.** Silken Net (ACCURACY-002), V-Impact Canvas (ACCURACY-005), BMAD Barry (ACCURACY-003), OpenSpec/Fission-AI (ACCURACY-012), and AWS AI-DLC enterprise customer claims (ACCURACY-015) were not addressed in the fix pass and remain in the corpus without `[UNVERIFIED]` flags. These are the highest residual hallucination risks.

3. **Cross-file consistency improved but propagation incomplete.** The AI-DLC fix to gemini did not propagate to research-ceremony-rhythm-alternatives.md, which still carries the suspect Wipro/D&B 10-15× claim. Cross-file consistency checks should be a standard part of fix verification.

4. **New paragraphs introduced in fixes inherit the same provenance hygiene problem they were meant to solve.** The new EARS/Kiro paragraph in gemini lacks a source tag and propagates a date from a sibling subagent file. Fix authoring should apply the same `[OFFICIAL]`/`[UNVERIFIED]` tagging discipline as the original corpus.

5. **Heading vs. content drift.** The iter-1 rewrite of the AI-DLC paragraph left the section heading "Mob Elaboration and Construction" intact while the content now substantially covers a non-mob mechanism. Minor structural cleanup needed.

---

## Recommended Iteration 3 Priorities

1. **Apply the same Kinetic Enterprise treatment to Silken Net, V-Impact Canvas, BMAD Barry, and OpenSpec/Fission-AI** — these were the four most prominent invented-framework concerns in iter-1 and they remain unflagged. A single round of `[UNVERIFIED]` blockquotes or removals would close the residual critical-class risk.
2. **Spot-check the Wipro / Dun & Bradstreet 10-15× claim** in research-ceremony-rhythm-alternatives.md against the linked AWS DevOps blog post. Either confirm verbatim or flag.
3. **Add source tag to the new EARS/Kiro paragraph** in gemini and verify the July 2025 Kiro launch date against kiro.dev.
4. **Rename or split the "Mob Elaboration and Construction" section heading** in gemini to match the dual-mechanism content.
5. **Optional:** cross-check the precision figures in research-cognitive-load-inversion.md (CodeRabbit, LinearB, eng-leadership newsletter) against primary reports, or add a top-of-section note indicating figures are as-cited and not independently verified.
