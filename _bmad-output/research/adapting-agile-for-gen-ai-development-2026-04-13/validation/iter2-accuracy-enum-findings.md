# Factual Accuracy — Enumerator Findings (Iteration 2)

**Lens:** Factual Accuracy
**Reviewer:** Enumerator (systematic re-validation after fix pass)
**Skepticism Level:** 2 (Balanced)
**Artifact Stage:** Post-fix re-validation

## Summary

| Fix Verification | Result |
|---|---|
| Casey West date/characterization | Correctly fixed |
| Kinetic Enterprise: Deloitte removed, [UNVERIFIED] added | Correctly fixed |
| MIT NANDA: replaced with [UNVERIFIED] | Correctly fixed |
| METR finding: corrected to "19% longer" | Correctly fixed |
| Anthropic Bloom: changed to [UNVERIFIED] | Correctly fixed |
| Forrester provenance: downgraded to [PRAC] | Correctly fixed |

| Remaining Issue Severity | Count |
|---|---|
| High | 3 |
| Medium | 2 |
| Low | 1 |
| **Total new / unresolved** | **6** |

**Overall assessment:** The fix pass landed all six tracked corrections accurately and without introducing new errors. The Casey West date, Kinetic Enterprise disclaimer, METR correction, MIT NANDA flagging, Bloom flagging, and Forrester provenance downgrade are all present and correctly stated. Six issues remain: three items explicitly held over from iteration 1 that were not addressed, two items from the "also check" list where the concern is confirmed still present, and one new observation arising from the iteration 2 reading. No re-reporting of fixed issues.

---

## Fix Verification Pass

### V-PASS-001 — Casey West date and characterization
**Status: CORRECTLY FIXED**
`gemini-deep-research-output.md` line 194: "Published in 2025 as a proposed governance layer for agentic workflows. Proposes an Agentic Development Lifecycle (ADLC) that wraps the traditional SDLC — not a replacement or clean break." Date is 2025; "clean break" language is absent; "wrapper" characterization is present. Both fix locations (main body and follow-up Q1) are correct.

### V-PASS-002 — Kinetic Enterprise: Deloitte attribution removed, [UNVERIFIED] added
**Status: CORRECTLY FIXED**
`gemini-deep-research-output.md` lines 211–215: The [UNVERIFIED] blockquote is present and correctly states that Deloitte's "Kinetic Enterprise" trademark refers to SAP business transformation, not an AI-Agile doctrine. The conceptual framing bullets are retained but clearly disclaimed. The correction is accurate: Deloitte does have a trademarked "Kinetic Enterprise" concept associated with SAP transformation.

### V-PASS-003 — MIT NANDA: replaced with [UNVERIFIED]
**Status: CORRECTLY FIXED**
`research-spec-correct-value-zero.md` — the MIT NANDA passage now reads as an [UNVERIFIED] blockquote explaining the figure appears in secondary sources but could not be traced to a verifiable primary MIT publication, and directing readers to the BCG "Widening AI Value Gap" report. The BCG report is properly cited as a well-sourced alternative. The correction is complete.

### V-PASS-004 — METR finding: corrected to "19% longer"
**Status: CORRECTLY FIXED**
`research-work-granularity-ai-speed.md` line 14: "METR's July 2025 study of experienced open-source developers found that — counterintuitively — those developers took 19% *longer* to complete tasks when using AI assistance, not faster." The METR attribution tag reads `[OFFICIAL — METR research]`. The prior incorrect claim about "compressing dramatically" is gone. The machine learning benchmark doubling-rate data is correctly separated into its own sentence with its own source citation. The correction is factually accurate.

### V-PASS-005 — Anthropic Bloom: changed to [UNVERIFIED]
**Status: CORRECTLY FIXED**
`research-behavioral-validation-ai-agents.md` line 85: "[UNVERIFIED — 'Bloom' as an Anthropic open-source behavioral evaluation tool could not be independently verified; may be confused with other 'Bloom' projects. Verify at anthropic.com/research/bloom before citing.]" Sources section line 167 also carries the [UNVERIFIED] tag. Both fix locations are present. The disclaimer is appropriately calibrated.

### V-PASS-006 — Forrester provenance: downgraded to [PRAC]
**Status: CORRECTLY FIXED**
`research-thought-leader-frameworks-agile-ai.md` line 199: The Forrester 95% claim now carries `[PRAC: referenced in multiple 2026 Medium articles and InfoQ coverage; direct Forrester primary URL not verified]`. Sources section line 301 adds: `[Forrester 2025 State of Agile — URL unverified; verify at forrester.com before citing as primary source] [UNVERIFIED]`. The fix is accurately applied.

---

## Remaining / New Findings

---

### ACCURACY-N01
- **id:** ACCURACY-N01
- **severity:** high
- **dimension:** traceability
- **location:** `gemini-deep-research-output.md:## Follow-up Q2:## 3. Specialized Solo Frameworks`
- **description:** "BMAD Quick Flow" and its "Barry" persona are presented in a table as a named framework for solo/small-team AI development, with the claim that it "Uses 'Barry,' an elite solo dev persona, to move from a 'Quick Spec' to 'Quick Dev' in a lean path." No source URL, publication, or citation is provided for BMAD Quick Flow or the Barry persona anywhere in the corpus. This is a specific, named commercial or open-source framework presented as if it is an established methodology, but it is unattributed.
- **evidence:** Table row: "BMAD Quick Flow | Uses 'Barry,' an elite solo dev persona, to move from a 'Quick Spec' to 'Quick Dev' in a lean path. | Small to medium features where enterprise ceremony is overkill." No URL or citation follows, and neither BMAD nor Barry appears in any of the 8 subagent research files or their sources sections.
- **suggestion:** Add a citation URL for BMAD Quick Flow (e.g., GitHub repository or product documentation), or add an [UNVERIFIED — no primary source URL provided] tag. Without a source, this entry is unverifiable and potentially a hallucinated framework name.

---

### ACCURACY-N02
- **id:** ACCURACY-N02
- **severity:** high
- **dimension:** traceability
- **location:** `gemini-deep-research-output.md:## Follow-up Q2:## 1. OpenSpec "Propose-Apply-Archive" Loop`
- **description:** The OpenSpec "Propose-Apply-Archive" loop is attributed to "Fission-AI" with no URL, GitHub link, or publication cited. This was flagged in iteration 1 (ACCURACY-011) as needing a citation. The fix pass log does not record any action on this item. It remains uncited. "Fission-AI" as the developer of a tool named "OpenSpec" is a specific, verifiable claim that cannot be confirmed without a source.
- **evidence:** "The OpenSpec 'Propose-Apply-Archive' Loop: This framework, developed by Fission-AI, uses a simple three-step cycle." No URL or source appears in the surrounding text or in the Sources section at the end of the file. The Follow-Up Q3 open-source tools table also lists "OpenSpec" without a URL (the table has no URLs for any tool entry).
- **suggestion:** Provide a URL for OpenSpec (GitHub repository or fission-ai product page), or add [UNVERIFIED — no primary source URL provided] to both occurrences. This was a carried-over finding from iteration 1 that was not addressed in the fix pass.

---

### ACCURACY-N03
- **id:** ACCURACY-N03
- **severity:** high
- **dimension:** traceability
- **location:** `gemini-deep-research-output.md:## Follow-up Q1:## 4. Shape Up as the "New Meta"`
- **description:** The "Silken Net" company and its hybrid Shape Up + NASA TRL methodology remain uncited. This was flagged in iteration 1 (ACCURACY-008) and was not addressed in the fix pass. The claim "Teams like Silken Net have 'completely overhauled' their architecture, abandoning Agile for a hybrid of Shape Up and NASA's Technology Readiness Levels (TRL)" has no source URL.
- **evidence:** "Teams like Silken Net have 'completely overhauled' their architecture, abandoning Agile for a hybrid of Shape Up and NASA's Technology Readiness Levels (TRL)." No citation follows, and "Silken Net" does not appear anywhere else in the corpus. The fix log for gemini-deep-research-output.md does not mention ACCURACY-008.
- **suggestion:** Add a citation URL for the Silken Net case study, or add [UNVERIFIED — no primary source URL provided]. This was a carried-over finding from iteration 1 not addressed in the fix pass.

---

### ACCURACY-N04
- **id:** ACCURACY-N04
- **severity:** medium
- **dimension:** traceability
- **location:** `gemini-deep-research-output.md:## Solving the Spec-Correct, Value-Zero Problem:## The Architect's V-Impact Canvas`
- **description:** The "Architect's V-Impact Canvas" is introduced as a named artifact for managing the "oil and water" moment in architecture. The term "V-Impact Canvas" does not appear in any of the 8 subagent research files. The Gemini sources section lists "infoq.com (The Oil and Water Moment in AI Architecture)" which may be the source, but the specific term "V-Impact Canvas" is not attributed to any named author, organization, or publication. There is no inline citation.
- **evidence:** "the Architect's V-Impact Canvas has been introduced as a stabilizing mechanism for what is termed the 'oil and water' moment in architecture." The Gemini sources list: "https://infoq.com (Does AI Make the Agile Manifesto Obsolete?; The Oil and Water Moment in AI Architecture)" — a domain-level citation only. No specific article URL, author name, or publication date is provided for this tool.
- **suggestion:** Add the specific infoq.com article URL for "The Oil and Water Moment in AI Architecture" inline with the V-Impact Canvas claim, along with the author name. Verify that "V-Impact Canvas" is actually the term used in that article and not a paraphrase introduced by the Gemini synthesis. If it is a paraphrase, note that.

---

### ACCURACY-N05
- **id:** ACCURACY-N05
- **severity:** medium
- **dimension:** traceability
- **location:** `research-thought-leader-frameworks-agile-ai.md:## Dev Community Synthesis:## The Wolfe Synthesis`
- **description:** The "Architect of Intent" role (as the evolved human role in AI-native development, defined as "orchestrating agent fleets while maintaining governance") is attributed to "Wolf Crywolfe" (dev.to, 2025). The URL in the sources section is `dev.to/crywolfe/the-agentic-manifesto-why-agile-is-breaking-in-the-age-of-ai-agents-1939`. The practitioner label indicates this is secondary/opinion content, which is appropriately tagged [PRAC]. However, the term "Architect of Intent" and the four specific replacements (Context Capsules, System Pulse, Continuous Flow, Architect of Intent) are presented as a coherent named framework from a single source with no verification. This is a medium concern because the [PRAC] label is present, but the specificity of the framework terminology suggests it should either be confirmed as Crywolfe's exact language or noted as a synthesis.
- **evidence:** "Architect of Intent as the evolved human role: orchestrating agent fleets while maintaining governance [PRAC — dev.to, 2025]." Four specific named concepts (Context Capsules, System Pulse dashboard, Continuous Flow, Architect of Intent) are all attributed to a single dev.to practitioner article.
- **suggestion:** Verify that "Context Capsules," "System Pulse dashboard," and "Architect of Intent" are the precise terms used in Crywolfe's dev.to article, and not paraphrases or synthesized terms. This is a moderate concern given the [PRAC] tag is present, but specificity of branded terms warrants confirmation.

---

### ACCURACY-N06
- **id:** ACCURACY-N06
- **severity:** low
- **dimension:** traceability
- **location:** `research-cognitive-load-inversion.md:## The Inversion Problem in Concrete Terms`
- **description:** The 98%/91%/21% statistics (merge volume, PR review time, task completion) remain attributed only to a newsletter secondary source (`newsletter.eng-leadership.com`). This was flagged in iteration 1 (ACCURACY-005) as needing a primary citation. The fix log for subagent files does not record any action on this item. The statistics remain with no identified primary source. The severity is low because the PRAC label is present and the newsletter is a plausible aggregator, but the primary research origin (possibly LinearB or GitHub's annual reports) is still unidentified.
- **evidence:** "Developers using AI complete 21% more tasks and merge 98% more PRs — but PR review time increases 91% in the same period. [PRAC: https://newsletter.eng-leadership.com/p/code-review-is-the-new-bottleneck]" No primary research report is identified for these figures.
- **suggestion:** Since the same file cites the LinearB 2026 Engineering Benchmarks Report extensively, confirm whether that report is the primary source for the 98%/91%/21% figures. If so, update the citation. If not, add a parenthetical noting the underlying primary source is unidentified.

---

## Cross-File Consistency Observations (No New Findings)

1. **METR correction is consistent across files.** Both `research-work-granularity-ai-speed.md` (corrected) and `research-cognitive-load-inversion.md` (line 143, which correctly states "took 19% longer") now agree. The internal contradiction identified in iteration 1 is resolved.

2. **Forrester 95% appears in three locations** and is consistently downgraded to [PRAC] in `research-thought-leader-frameworks-agile-ai.md` (body and Sources). The same statistic appears in `research-work-granularity-ai-speed.md` at line 129 with `[PRAC: referenced in multiple 2026 Medium articles and InfoQ coverage]` — already correctly tagged at the time of the fix pass. Consistent across corpus.

3. **The Kinetic Enterprise [UNVERIFIED] note is factually accurate.** Deloitte's "Kinetic Enterprise" is indeed a registered concept tied to SAP transformation and business agility, unrelated to AI development methodology. The correction correctly characterizes the attribution mismatch.

4. **OpenSpec appears in both the Gemini file (uncited) and the behavioral validation file's open-source tools table (also without a URL).** The `research-behavioral-validation-ai-agents.md` sources section does not list OpenSpec. The tool's existence is thus unverified in two corpus locations, not one.
