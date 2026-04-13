# Coherence & Craft — Adversary Findings (Iteration 2)

**Lens:** Coherence & Craft (Adversary, Skepticism Level 2 — Balanced)
**Stage:** Re-validation
**Mode:** Corpus (9 files)
**Date:** 2026-04-13

## Summary

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 3 |
| Medium | 4 |
| Low | 2 |
| **Total** | **9** |

Iteration 1 fixes substantively reduced the catastrophic disambiguation issues. The Harness Engineering disambiguation, AI-DLC three-phase correction, Casey West date/characterization, EARS addition, and ATDD/BDD/Gherkin disambiguation are all visible in the corpus. However, the fixes were applied surgically rather than holistically, and several seam-level coherence issues remain or have been newly introduced:

- The Harness Engineering disambiguation note covers Fowler/Böckeler vs. OpenAI but does **not** acknowledge the third use of the term in `research-feature-unit-user-value.md` (Red Hat Developer), so a reader reading all three files still encounters three different originators with only two reconciled.
- The AI-DLC fix added a corrective paragraph to the cognitive-load section (line 120) but left the Q1 description of AI-DLC unchanged — Q1 still says "AI-DLC officially abandons the sprint in favor of 'Bolts'" and "Reversed Direction: AI initiates by proposing plans, humans act as 'Validators'." The Gemini file therefore now contains two distinct AI-DLC descriptions (a corrected three-phase one and the original Bolts/Validators one) that don't reference each other.
- Recommendation #4 still says "Implement Mob Rituals" without distinguishing whether they belong to 3-3-3 or AI-DLC — directly contradicting the just-added correction that AI-DLC has no mob rituals.
- "Test-Driven AI (TDA)" appears in Gemini three times but in zero subagent files. This was a coherence issue in iter1 (implicit) and remains: the synthesis introduces a labeled methodology that the corpus it summarizes does not use.
- The EARS addition reads as a bolted-on editorial note ("The subagent research identifies...") rather than integrated prose, and uses a redundant double-bolded phrase that breaks the section's voice.
- Pre-existing Silken Net contradiction (Gemini Q1 vs. ceremony file) was not addressed by iter1 fixes and persists.

No re-reporting of fixed issues. Findings below are either (a) new discrepancies introduced by the fixes, (b) incomplete fixes that leave reader confusion, or (c) pre-existing coherence problems that were in scope for iter1 but not addressed.

---

## Findings

- id: COHERENCE-101
- severity: high
- dimension: cross_document_consistency
- location: gemini-deep-research-output.md:"Harness Engineering and the Cybernetic Governor" (line 32 disambiguation note) / research-ceremony-rhythm-alternatives.md:"Harness Engineering: A Practitioner Model from OpenAI" (line 119 note) / research-feature-unit-user-value.md:"AI-Native Development: Amplifying the Gap" (line 133)
- description: The iter1 disambiguation note resolves the Fowler/Böckeler vs. OpenAI collision but ignores the third independent use in the feature-unit file (Red Hat Developer's "harness engineering" article from April 2026). A reader who reads all three files still encounters three distinct originators of "Harness Engineering" — only two of which are now reconciled. The disambiguation creates an asymmetric coverage problem: the Gemini and ceremony files acknowledge each other, but neither acknowledges the Red Hat Developer use, and the Red Hat Developer reference in the feature-unit file makes no acknowledgment of either.
- evidence:
  - Gemini line 32: "The term 'Harness Engineering' is also used independently by OpenAI for their agent-workflow operating model. These are distinct uses of the same phrase — the Fowler/Böckeler concept (cybernetic governor pattern) and the OpenAI concept (agent-first PR workflow) are described separately below."
  - Ceremony line 119: "(Note: OpenAI uses 'Harness Engineering' for their agent-workflow operating model — this is a separate use of the term from the Fowler/Böckeler cybernetic governor concept.)"
  - Feature-unit file line 133: "The Red Hat Developer article on harness engineering (April 2026) points toward a specific enforcement mechanism for AI-native development: structured harnesses that require acceptance criteria to be grounded in measurable outcomes..."
  - Feature-unit file Sources line 194: "[Harness Engineering: Structured Workflows for AI-Assisted Development — Red Hat Developer]"
- suggestion: Extend the disambiguation note in Gemini (and ideally the ceremony and feature-unit files) to acknowledge the third use, e.g.: "Note also that Red Hat Developer's April 2026 'harness engineering' article uses the term in a third sense — referring to structured workflow templates that enforce measurable acceptance criteria." Three uses with two reconciled is functionally the same confusion as three uses with none reconciled for any reader who reads all three files.

- id: COHERENCE-102
- severity: high
- dimension: consistency
- location: gemini-deep-research-output.md:"Cognitive Load Inversion" section (lines 116-120) vs "Follow-Up Q1: Arguments for Abandoning Agile Entirely" section 3 (lines 196-201)
- description: The iter1 fix to the AI-DLC contradiction was applied only in the cognitive-load section; the Q1 description was not updated. The Gemini file now contains two distinct AI-DLC descriptions that do not reference each other. The cognitive-load section says AI-DLC is a three-phase model (Inception/Construction/Operations) without mob rituals; Q1 says AI-DLC "officially abandons the sprint in favor of 'Bolts'" and reverses Agile direction with "Validators." A reader cannot tell whether AI-DLC is a phase-based model or a Bolts/Validators model — and the same file gives both answers.
- evidence:
  - Gemini line 120 (post-fix): "The AWS AI-Driven Development Lifecycle (AI-DLC) takes a different approach: it is a three-phase model (Inception, Construction, Operations) where AI proposes plans and humans act as Validators confirming intent and managing risk — not mob-based synchronous rituals."
  - Gemini Q1 line 198-201 (unchanged): "AWS has released prescriptive guidance for the AI-Driven Development Lifecycle (AI-DLC)... From Sprints to Bolts: AI-DLC officially abandons the sprint in favor of 'Bolts' — high-velocity execution cycles measured in hours or days... Reversed Direction: Unlike Agile's 'human-commands, AI-executes' model, AI-DLC operates where AI initiates by proposing plans, humans act as 'Validators'..."
  - Ceremony file lines 75-90 (canonical AWS source description): no mention of "Bolts" anywhere.
- suggestion: Either (a) update Q1's AI-DLC description to align with the corrected line-120 description and explicitly note "Bolts" is community vocabulary, not in the official AWS framework; or (b) add a cross-reference in Q1 stating "see also the corrected AI-DLC description above which describes the three-phase model." Leaving two distinct descriptions of the same framework in the same document defeats the purpose of the iter1 fix.

- id: COHERENCE-103
- severity: high
- dimension: consistency
- location: gemini-deep-research-output.md:"Conclusions and Actionable Recommendations" (line 156) and "Cognitive Load Inversion" (line 116-120)
- description: Recommendation #4 says "Implement Mob Rituals: Replace the 'silent' work of individual coding with high-bandwidth 'Mob Elaboration' and 'Mob Construction' sessions" — without specifying which framework these belong to. The just-fixed cognitive-load section now correctly attributes Mob Elaboration/Construction to Thoughtworks 3-3-3 only and explicitly states AI-DLC has no mob rituals. But the Recommendations section presents Mob Rituals as a generic, framework-agnostic best practice — re-creating exactly the over-generalization that the iter1 fix was meant to correct. A reader skipping to Recommendations will infer that Mob Rituals are universal AI-Agile practice.
- evidence:
  - Gemini line 156: "**Implement Mob Rituals**: Replace the 'silent' work of individual coding with high-bandwidth 'Mob Elaboration' and 'Mob Construction' sessions."
  - Gemini line 118 (post-fix): "The Thoughtworks 3-3-3 model's 'Mob Elaboration' and 'Mob Construction' rituals (described above) are the primary mechanism..."
  - Gemini line 120 (post-fix): "...not mob-based synchronous rituals. The AI-DLC's cognitive-load management comes from its structured phase gates and 'Units of Work' abstraction, not from mob sessions."
- suggestion: Update Recommendation #4 to "Implement 3-3-3-style Mob Rituals (where team-based)" or similar, scoping the recommendation to the framework that prescribes it. Alternatively, replace with a more general "Adopt high-bandwidth collaboration patterns appropriate to your framework — Thoughtworks 3-3-3 uses Mob Elaboration/Construction; AI-DLC uses phase gates with Validator review."

- id: COHERENCE-104
- severity: medium
- dimension: cross_document_consistency
- location: gemini-deep-research-output.md:"Test-Driven AI (TDA) and the 'Red' Phase" (lines 104-106), Q2 (line 241), Q3 (line 274) / all subagent files (zero occurrences)
- description: The Gemini synthesis introduces and labels "Test-Driven AI (TDA)" as a named methodology three times (main body section header, Q2 inline, Q3 inline). No subagent file uses the abbreviation "TDA" or the phrase "Test-Driven AI." The acceptance-criteria, behavioral-validation, and spec-correct-value-zero files all discuss test-first practices but use different terminology (red/green TDD, ATDD, BDD, property-based testing). A reader cross-referencing the synthesis to the corpus will not find "TDA" anywhere and may treat it as an established methodology when it is not corpus-grounded vocabulary.
- evidence:
  - Gemini line 104: "### Test-Driven AI (TDA) and the 'Red' Phase"
  - Gemini line 106: "However, the methodology has evolved into 'Test-Driven AI' (TDA)."
  - Gemini line 241: "**Red/Green TDA:** This is the solo practitioner's primary safety net..."
  - Gemini line 274: "**Red/Green TDA (Test-Driven AI):** The developer writes a high-level functional test..."
  - Subagent files: zero matches for "TDA" or "Test-Driven AI" (only "Test-Driven Development", "TDD", "ATDD", "BDD" appear).
- suggestion: Either remove the "(TDA)" abbreviation and "Test-Driven AI" framing from Gemini and replace with the corpus-aligned terminology (TDD red/green phase applied to AI agents), or add a brief disambiguation that "TDA" is Gemini's gloss on the broader spec-driven testing patterns documented in the subagent files. As written, Gemini coins a methodology label the corpus does not use.

- id: COHERENCE-105
- severity: medium
- dimension: cross_document_consistency
- location: gemini-deep-research-output.md:"Follow-Up Q1: Arguments for Abandoning Agile Entirely" section 4 (line 206) / research-ceremony-rhythm-alternatives.md:"Shape Up as an AI-Compatible Alternative" (line 43)
- description: The pre-existing Silken Net contradiction (originally COHERENCE-003 in iter1 findings) was not addressed by iter1 fixes and remains. Gemini Q1 cites "Silken Net" as a specific company that "completely overhauled their architecture, abandoning Agile for a hybrid of Shape Up and NASA's Technology Readiness Levels." The ceremony file directly contradicts this with "no published practitioner cases as of this research specifically describe applying Shape Up to a human-AI agent team." Both claims cannot be true. Iter1's fix-log-gemini.md does not list this as a fixed issue, and the corpus state confirms it remains.
- evidence:
  - Gemini line 206: "Teams like Silken Net have 'completely overhauled' their architecture, abandoning Agile for a hybrid of Shape Up and NASA's Technology Readiness Levels (TRL)."
  - Ceremony file line 43: "However, no published practitioner cases as of this research specifically describe applying Shape Up to a human-AI agent team. The fit is structural, not yet empirically validated in that context."
- suggestion: Either verify the Silken Net citation and update the ceremony file's "no published cases" claim, or remove/qualify the Silken Net reference in Gemini Q1 with `[UNVERIFIED]`. Carrying both claims forward through iter2 means the corpus still speaks with two voices on this load-bearing question.

- id: COHERENCE-106
- severity: medium
- dimension: clarity
- location: gemini-deep-research-output.md:"EARS Notation and Spec-Driven Tooling" (lines 61-63)
- description: The iter1 EARS addition appears as a single short paragraph that reads as an editorial bolt-on rather than integrated synthesis. The paragraph opens with "**EARS Notation and Spec-Driven Tooling:**" — a bold inline label that duplicates the section header (which is also "EARS Notation and Spec-Driven Tooling"). The paragraph also opens with "The subagent research identifies EARS notation..." — the phrase "the subagent research" is meta-corpus scaffolding that does not appear elsewhere in the Gemini file (which otherwise treats sources as named publishers/authors). And the closing cross-reference "See `research-acceptance-criteria-ai-literal.md` for full coverage" is the only file-path cross-reference in the entire Gemini synthesis — it breaks the document's voice.
- evidence:
  - Gemini line 61: "### EARS Notation and Spec-Driven Tooling"
  - Gemini line 63: "**EARS Notation and Spec-Driven Tooling:** The subagent research identifies EARS notation (Easy Approach to Requirements Syntax — a structured format using 'When/While/If/Where' triggers and 'the system shall' responses) as the most concrete tooling approach to the specification-completeness problem. Amazon's **Kiro IDE** (July 2025) made EARS central to its spec-driven workflow, automatically converting EARS-format specifications into acceptance tests. This provides a practical path from structured intent to executable validation that is absent from higher-level frameworks. See `research-acceptance-criteria-ai-literal.md` for full coverage."
  - Other Gemini sections cite sources via tags like `[OFFICIAL — kiro.dev/docs/specs/]`, not file paths.
- suggestion: Drop the duplicate bold inline label and the "subagent research identifies" framing. Rewrite as integrated prose: "EARS notation (Easy Approach to Requirements Syntax) — a structured 'When/While/If/Where ... the system shall' format — has emerged as the most concrete tooling response to the specification-completeness problem. Amazon's Kiro IDE (public preview July 2025) [OFFICIAL — kiro.dev/docs/specs/] made EARS central to its spec-driven workflow..." Replace the file-path cross-reference with a normal source citation or omit it.

- id: COHERENCE-107
- severity: medium
- dimension: cross_document_consistency
- location: gemini-deep-research-output.md:"Restructuring Work Granularity" section header and intro (lines 34-36) and Q1 section 3 (lines 196-201) / research-ceremony-rhythm-alternatives.md (entire AI-DLC section, lines 75-93)
- description: The Gemini file presents "Bolts" as AWS AI-DLC's official prescriptive vocabulary in two places (the section header "From Sprints to High-Velocity 'Bolts'" and Q1 line 199 "AI-DLC officially abandons the sprint in favor of 'Bolts'"). The ceremony file's canonical AWS AI-DLC section never uses the word "Bolts" while describing the same framework's three phases. The post-iter1 line 120 in Gemini (correctly) describes AI-DLC's units as "Units of Work" and "structured phase gates" — also without "Bolts." This strongly suggests "Bolts" is a community gloss, not AWS's official term, and the section header / Q1 misattribute it. (Pre-existing issue COHERENCE-005 from iter1, not addressed by fixes.)
- evidence:
  - Gemini header line 34: "## Restructuring Work Granularity: From Sprints to High-Velocity 'Bolts'"
  - Gemini Q1 line 199: "**From Sprints to Bolts**: AI-DLC officially abandons the sprint in favor of 'Bolts'..."
  - Gemini line 120 (post-fix, describing AI-DLC): "The AI-DLC's cognitive-load management comes from its structured phase gates and 'Units of Work' abstraction" — no "Bolts."
  - Ceremony file lines 75-93 (canonical AI-DLC section): no occurrence of "Bolts" or "bolts."
  - Feature-unit file line 131 (the only subagent reference to "bolts"): "DEV Community analysis... 'sprints are being replaced by bolts'" — attributes to a community blog post, not AWS.
- suggestion: Either (a) demote "Bolts" in Gemini from "AI-DLC officially abandons" to "community-coined alternative measured in hours or days, sometimes informally called 'Bolts'" and tag with `[PRAC — dev.to community gloss]`; or (b) verify whether AWS's official AI-DLC documentation uses "Bolts" and update the ceremony file accordingly. The current state has Gemini implying AWS uses "Bolts" while the canonical AWS source description (ceremony file) does not.

- id: COHERENCE-108
- severity: low
- dimension: tonal_consistency
- location: gemini-deep-research-output.md:"Follow-up Q2" section 1 (line 232)
- description: The OpenSpec entry in Q2 attributes the framework to "Fission-AI" without source tag or explanation. None of the subagent files mention "Fission-AI" as the originator of OpenSpec; the behavioral-validation file lists OpenSpec generically as a tooling pattern. Introducing an unnamed, untagged organizational attribution in Q2 creates a coherence gap — readers will wonder why this single attribution was singled out and where it came from. (Pre-existing minor issue not flagged in iter1 but visible on re-read.)
- evidence:
  - Gemini line 232: "**The OpenSpec 'Propose-Apply-Archive' Loop:** This framework, developed by Fission-AI, uses a simple three-step cycle..."
  - Gemini line 296 (Q3 OpenSpec table row): no organization attribution, no source tag.
  - Subagent files: "Fission-AI" appears zero times.
- suggestion: Either add a source tag (`[PRAC — fission-ai.com or similar]`) or remove the "developed by Fission-AI" claim. Untagged organizational attributions in a corpus where every other claim carries a tag stand out as unverified.

- id: COHERENCE-109
- severity: low
- dimension: clarity
- location: gemini-deep-research-output.md:"Follow-Up Q2" introduction (line 221)
- description: Q2's question text references "Mob Elaboration, AI/works, AI-DLC" as if all three are framework names of equivalent rank. After the iter1 fix that disentangled Mob Elaboration from AI-DLC, this question framing is now inaccurate — Mob Elaboration is one ritual within Thoughtworks 3-3-3, not a peer-level framework. The question is a verbatim user-provided artifact so changing it may be out of scope, but a parenthetical clarification in the response intro could acknowledge the categorization mismatch.
- evidence:
  - Gemini line 221: "**Question asked:** Almost all the frameworks described (3-3-3, Mob Elaboration, AI/works, AI-DLC) are designed for teams. What about the solo developer or tiny team..."
  - Post-iter1 line 118 correctly scopes Mob Elaboration as a 3-3-3 ritual, not a framework.
- suggestion: Add a one-line response intro acknowledging "(Mob Elaboration here refers to the 3-3-3 ritual rather than a standalone framework — see corrected description above.)" Or accept this as low-impact since the question is preserved verbatim from the original prompt.

---

## Cross-Cutting Observations

1. **Iter1 fixes were surgical, not holistic.** Each fix corrected the exact location flagged by iter1 findings but did not propagate to other locations in the same document where the same concept appears. The clearest example is AI-DLC: the cognitive-load section was corrected, but Q1's AI-DLC description was left intact, creating an internal contradiction within the post-fix Gemini file. The Recommendations section (#4 Mob Rituals) similarly was not updated to reflect the cognitive-load section's correction. This is an iter1 process gap — fixes need to be applied across all document locations referring to the same concept, not just at the originally-flagged line.

2. **The Gemini file remains the principal coherence-debt site.** Of the 9 findings above, 7 are wholly or primarily in the Gemini synthesis. The eight subagent files are largely consistent with each other and with the corpus tagging discipline. The Gemini synthesis continues to introduce vocabulary not in the corpus (TDA, Bolts-as-AWS-term, Silken Net), use editorial seams (the EARS bolt-on note), and mismatch tonally (file-path cross-reference, Fission-AI attribution).

3. **Disambiguation notes work — when applied uniformly.** The Harness Engineering disambiguation note in Gemini and ceremony files is well-crafted and effective for its scope. The problem is the third use (Red Hat Developer in feature-unit) is not covered, so a reader of all three files still encounters un-reconciled triple attribution. Disambiguation notes either need to address all known uses or explicitly say "additional uses may exist."

4. **The ATDD/BDD/Gherkin disambiguation is exemplary.** The blockquote inserted in `research-acceptance-criteria-ai-literal.md` line 86 cleanly distinguishes the three concepts in two sentences. This is the iter1 fix that worked best. No further coherence issues introduced; no missed locations identified.

5. **Casey West fix is clean.** Date is consistently "2025" across the corpus now; characterization as "ADLC wrapper around SDLC" is consistent in Gemini main body, Q1, and frameworks file. No new discrepancies.

6. **EARS coverage is now corpus-consistent on substance, but stylistically discordant in Gemini.** Both Gemini and the acceptance-criteria file describe EARS as the "most concrete tooling approach." Both reference Kiro IDE (July 2025). Both describe the When/shall pattern. The substantive coherence is good. Only the stylistic execution of the Gemini insert needs cleanup (COHERENCE-106).
