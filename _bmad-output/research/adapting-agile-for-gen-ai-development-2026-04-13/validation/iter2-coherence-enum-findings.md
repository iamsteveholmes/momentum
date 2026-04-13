# Coherence & Craft — Enumerator Findings (Iteration 2)

**Lens:** Coherence & Craft
**Reviewer:** ENUMERATOR (Skepticism Level 2 — Balanced)
**Stage:** Iteration 2 — Re-validation after fix pass
**Corpus:** 9 files — 1 Gemini Deep Research output + 8 subagent research files
**Date validated:** 2026-04-13

## Summary

Iteration 1 fixes were verified. The AI-DLC vs. 3-3-3 contradiction, the Harness Engineering disambiguation, the EARS addition to Gemini, and the Casey West date correction are all confirmed applied correctly. The leaked editorial note in the ceremony file is removed. These were the most load-bearing structural fixes and they hold.

Seven issues survive the fix pass. Three are unaddressed carryovers from iteration 1 findings (TDA terminology, Bolts attribution, Siderova triple-paraphrase). Three are confirmed-present issues that iteration 1 flagged but the fix pass did not act on (editorial scaffolding leak, AI/works™ promotional language, Silken Net unverified claim). One is a new finding surfaced during close re-reading of the fixed sections (trust-statistic internal inconsistency in cognitive-load file, also flagged by the adversary — confirmed present).

| Severity | Count |
|---|---|
| High | 3 |
| Medium | 3 |
| Low | 1 |
| **Total** | **7** |

---

## Verified Fixes (do not re-report)

The following iteration 1 issues are confirmed resolved:

- **AI-DLC vs. 3-3-3 contradiction** (was COHERENCE-002/ADV-002/ADV-007): Gemini's "Mob Elaboration and Construction" section now correctly attributes mob rituals to Thoughtworks 3-3-3 and describes AI-DLC separately as a three-phase (Inception/Construction/Operations) model. The two frameworks are cleanly separated.
- **Harness Engineering disambiguation** (was COHERENCE-001/ADV-001): Disambiguation note added in Gemini immediately after the Fowler/Böckeler section. The ceremony file also has the note. The fix works, with one residual noted below (COHERENCE-203).
- **EARS section in Gemini** (was ADV-008): New "EARS Notation and Spec-Driven Tooling" subsection is present and coherent with the acceptance-criteria file's coverage.
- **Casey West date** (was COHERENCE-002/ADV-004): Gemini now correctly reads "proposed by Casey West in 2025." Both files now agree.
- **Leaked editorial note in ceremony file** (was COHERENCE-016): The Shape Up section's defensive parenthetical is removed.

---

## Remaining and New Findings

---

- id: COHERENCE-201
- severity: high
- dimension: cross_document_consistency
- location: gemini-deep-research-output.md:Behavioral Validation section / research-behavioral-validation-ai-agents.md (entire document)
- description: The term "Test-Driven AI" (TDA) is introduced in the Gemini file as an established named practice attributed to "Kent Beck and others." The dedicated behavioral-validation subagent file — which is the corpus authority on validation approaches — does not use the term TDA anywhere as a validated concept. It describes the identical practice (write failing test, then implement) but calls it "Red/Green TDA" only when quoting from the Gemini follow-up Q2 section — i.e., it echoes Gemini's own terminology rather than validating it from an independent source. The thought-leader-frameworks file attributes the same practice to Beck as "TDD as a hard constraint" without naming it TDA. This means TDA is a term that exists solely in the Gemini synthesis and its self-referential follow-up, with no independent validation in the subagent corpus. If TDA is an established named practice, the behavioral-validation file should use and source it; if it is Gemini's framing, the synthesis should flag it as such.
- evidence: gemini-deep-research-output.md lines 104–106: "the methodology has evolved into 'Test-Driven AI' (TDA). A critical component of TDA is the 'red' phase..." — research-behavioral-validation-ai-agents.md: TDA does not appear as a standalone term anywhere in the document — only "Red/Green TDA" appears once in Follow-up Q3 context as a citation back to the Gemini section. — research-thought-leader-frameworks-agile-ai.md: describes Beck's practice as "TDD as a hard constraint" with no mention of TDA.
- suggestion: Either (a) add a source citation in the Gemini document identifying where "Test-Driven AI" / "TDA" appears in the primary literature the Gemini research drew from, or (b) add an [UNVERIFIED — term coined in this synthesis; not independently sourced] tag to the TDA label, or (c) reframe the section as "an evolution of TDD sometimes called Test-Driven AI" without asserting TDA as an established named practice.

---

- id: COHERENCE-202
- severity: high
- dimension: cross_document_consistency
- location: gemini-deep-research-output.md:Follow-Up Q1 (Shape Up section) / research-ceremony-rhythm-alternatives.md:Shape Up section
- description: The Gemini follow-up attributes a specific named company (Silken Net) as having "completely overhauled their architecture, abandoning Agile for a hybrid of Shape Up and NASA's Technology Readiness Levels." The ceremony file states directly: "no published practitioner cases as of this research specifically describe applying Shape Up to a human-AI agent team. The fit is structural, not yet empirically validated in that context." These two claims are mutually exclusive. Either Silken Net is a verified adopter (in which case the ceremony file's blanket denial is wrong) or the Silken Net claim is unverified (in which case the Gemini follow-up is asserting as fact something that cannot be found in the published literature). The fix pass did not resolve this conflict.
- evidence: gemini-deep-research-output.md line 206: "Teams like Silken Net have 'completely overhauled' their architecture, abandoning Agile for a hybrid of Shape Up and NASA's Technology Readiness Levels (TRL)." — research-ceremony-rhythm-alternatives.md: "However, no published practitioner cases as of this research specifically describe applying Shape Up to a human-AI agent team. The fit is structural, not yet empirically validated in that context."
- suggestion: Either verify the Silken Net claim and update the ceremony file accordingly, or flag the Gemini claim as [UNVERIFIED — company name and adoption details not independently verified; conflicts with ceremony file's finding of no published cases] and remove the confident assertive framing.

---

- id: COHERENCE-203
- severity: high
- dimension: cross_document_consistency
- location: research-feature-unit-user-value.md:"AI-Native Development: Amplifying the Gap" section / gemini-deep-research-output.md:Harness Engineering disambiguation note
- description: The Harness Engineering disambiguation was fixed in the Gemini file and the ceremony file. However, the feature-unit-user-value subagent file (section 10) attributes "harness engineering" to Red Hat Developer without any disambiguation note — presenting it as a third independent concept under the same label. The Red Hat usage describes acceptance criteria grounded in measurable outcomes, which is a third distinct sense of the term: not Fowler/Böckeler's cybernetic governor, not OpenAI's Codex PR workflow, but a structured checklist pattern for AI-assisted development. The disambiguation fix was partial — it covers two of the three attributions but misses the third.
- evidence: research-feature-unit-user-value.md line 133: "The Red Hat Developer article on harness engineering (April 2026) points toward a specific enforcement mechanism for AI-native development: structured harnesses that require acceptance criteria to be grounded in measurable outcomes..." — The term appears without any note that "harness engineering" as used by Red Hat is a distinct sense from Fowler/Böckeler and OpenAI. The fix in the Gemini file's disambiguation note says there are "distinct uses" by Fowler/Böckeler and OpenAI but does not mention the Red Hat usage.
- suggestion: Either add a brief note in the feature-unit file's Red Hat reference acknowledging that "harness engineering" is being used in yet another sense here, or expand the Gemini disambiguation note to acknowledge three usages: Fowler/Böckeler (cybernetic governor), OpenAI (agent-first PR workflow), and Red Hat (structured acceptance-criteria enforcement pattern).

---

- id: COHERENCE-204
- severity: medium
- dimension: cross_document_consistency
- location: gemini-deep-research-output.md:"Restructuring Work Granularity" section header and Q1 / research-ceremony-rhythm-alternatives.md:AWS AI-DLC section / research-feature-unit-user-value.md:section 10
- description: The term "Bolts" is attributed to AWS AI-DLC official prescriptive guidance in the Gemini file, which uses it as the central naming for the sprint-replacement concept. The ceremony file's dedicated AWS AI-DLC section never uses the word "Bolts" when describing the same framework's three phases (Inception, Construction, Operations). The feature-unit file attributes "bolts" to a DEV Community practitioner article, not to official AWS documentation. The corpus therefore presents a key vocabulary term with three inconsistent attributions: Gemini says it is AWS official terminology, the ceremony file's AI-DLC description omits it entirely, and the feature-unit file traces it to a practitioner blog. A reader cannot determine whether "Bolts" is AWS's official term or community vocabulary that Gemini has mis-attributed to the AWS source.
- evidence: gemini-deep-research-output.md line 199: "AI-DLC officially abandons the sprint in favor of 'Bolts'" [OFFICIAL — docs.aws.amazon.com]. — research-ceremony-rhythm-alternatives.md: AI-DLC section describes Inception/Construction/Operations phases with no mention of "Bolts." — research-feature-unit-user-value.md line 131: "'Traditional 'sprints' are being replaced by 'bolts' — shorter, more intense work cycles'" [PRAC — dev.to/devactivity/...]
- suggestion: Verify whether AWS's official prescriptive guidance at docs.aws.amazon.com uses the term "Bolts" to describe execution cycles. If it does, the ceremony file should include the term in its AI-DLC description and the feature-unit file should upgrade the attribution from PRAC to OFFICIAL. If it does not, the Gemini attribution is incorrect and should be changed to [PRAC] or [UNVERIFIED].

---

- id: COHERENCE-205
- severity: medium
- dimension: cross_document_consistency
- location: research-spec-correct-value-zero.md:The Verification-Validation Collapse / research-work-granularity-ai-speed.md:The Upstream Bottleneck Shift / research-thought-leader-frameworks-agile-ai.md:The InfoQ Debate
- description: The Sonya Siderova quote from the InfoQ Agile Manifesto debate article is presented in three different forms across three files. Two files use the short epigram: "Agile isn't dead. It's optimizing a constraint that moved." The spec-correct file uses a much longer version in quotation marks: "the bottleneck moved from 'how do humans collaborate to build' to 'how do humans decide what to build and validate it actually works.'" This longer version uses quotation marks as if it is a direct quote, but its length and paraphrase-like structure suggest it may be a synthesized paraphrase presented as a verbatim quote. The fix pass did not address this. A reader comparing the three files cannot determine what Siderova actually said.
- evidence: research-work-granularity-ai-speed.md line 26: Siderova quoted as "Agile isn't dead. It's optimizing a constraint that moved." [PRAC: InfoQ] — research-thought-leader-frameworks-agile-ai.md line 197: same short form. — research-spec-correct-value-zero.md line 30: "the InfoQ report on the AI and Agile Manifesto debate quotes Sonya Siderova: 'the bottleneck moved from \"how do humans collaborate to build\" to \"how do humans decide what to build and validate it actually works.\"'"
- suggestion: The third version is almost certainly a paraphrase, not a direct quote. Replace the quotation marks in the spec-correct file with a paraphrase marker: "Siderova has been summarized as arguing that..." or convert to indirect speech. If the longer formulation is actually a second distinct Siderova quote from the same article, cite it as such with a clear attribution that this is a separate statement.

---

- id: COHERENCE-206
- severity: medium
- dimension: clarity
- location: research-feature-unit-user-value.md:Synthesis section (final paragraph)
- description: The file's closing paragraph contains an unresolved editorial scaffolding leak: "This is the gap the researcher's 'Feature' concept addresses directly." The phrase "the researcher's 'Feature' concept" refers to a meta-conversation between the orchestrator and the subagent about a design concept the questioner had in mind. No reader of this document as a research output will know what "the researcher's 'Feature' concept" refers to — the term "Feature" is not defined anywhere in the document, and "the researcher" has no referent. This issue was flagged in the adversary findings (COHERENCE-010) but was not in the fix-log-subagent-files.md and remains present in the current file.
- evidence: research-feature-unit-user-value.md line 162: "This is the gap the researcher's 'Feature' concept addresses directly." The sentence follows two sentences that stand independently and is clearly a subagent note to the orchestrator rather than research content.
- suggestion: Remove the final sentence. The two preceding sentences — "The notable absence in most current practice is a formal 'value validation gate'..." and "Most teams have planning-side outcome statements but no production-side confirmation requirement before closing the feature." — close the section correctly without the meta-reference.

---

- id: COHERENCE-207
- severity: low
- dimension: tonal_consistency
- location: gemini-deep-research-output.md:The Move to 'Super-Specs' and Intent Design section (line 59) / Continuous Regeneration section (line 98)
- description: The Gemini file retains vendor-promotional language for AI/works™ despite iteration 1 identifying this as a tonal inconsistency (adversary finding COHERENCE-009). The trademark symbol (™) appears in the body text at line 59 ("Platforms like AI/works™ generate these specifications...") and line 98 ("Platforms like AI/works™ do not merely 'complete' a project..."). The promotional phrase "grow up instead of grow old" and "ending the multi-million dollar cycle" (line 98) are vendor-framing rather than research analysis. The fix pass addressed other issues but did not strip the ™ marks or promotional phrasing. By contrast, the thought-leader-frameworks subagent file writes "AI/works" without the trademark symbol and in measured analytic terms.
- evidence: gemini-deep-research-output.md line 59: "Platforms like AI/works™ generate these specifications..." — line 98: "Platforms like AI/works™ do not merely 'complete' a project; they continuously regenerate affected components... This ensures that software systems 'grow up instead of grow old,' effectively ending the multi-million dollar cycle of building and then rebuilding systems." — research-thought-leader-frameworks-agile-ai.md: "In early 2026, Thoughtworks launched **AI/works**, an agentic development platform that operationalizes their emerging methodology..." (no ™, neutral description).
- suggestion: Remove ™ marks from the Gemini body text (the Sources list citation of the PR Newswire press release may reasonably retain the trademark as it is a citation of a commercial announcement). Replace vendor phrases like "grow up instead of grow old" with quoted attribution to the Thoughtworks source if it is a genuine quote, or reframe analytically: "Thoughtworks positions the platform as enabling continuous software evolution rather than periodic rebuild cycles."

---

*End of findings. 7 remaining issues: 3 high, 3 medium, 1 low.*

*Primary risks: TDA terminology is unvalidated and appears authoritative in the synthesis; Bolts attribution may mis-credit AWS for community vocabulary; Silken Net claim directly contradicts the ceremony file's finding on published cases.*
