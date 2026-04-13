# Structural Integrity — Adversary Findings

**Lens:** Structural Integrity
**Reviewer framing:** Adversary (pattern-aware, holistic)
**Corpus:** 9 files (1 gemini-deep-research output + 8 claude-code-subagent research files)
**Stage:** Final
**Skepticism level:** 3 (Aggressive)

## Summary by severity

- critical: 0
- high: 3
- medium: 6
- low: 4
- Total: 13

The corpus is structurally sound in the sense that all 9 files have frontmatter, a title, a body, and a Sources section. The adversarial pattern-reading surfaces a consistent class of defect: **metadata/claim/source integrity drifts in ways the files themselves do not flag.** The 8 subagent files disagree with `scope.md` on what the research topic is; one file's source-origin tagging is entirely absent; several load-bearing facts (Forrester 95%, arxiv 2506.16334) are cited without being listed in Sources or are tagged inconsistently across files; and one file's body reference to a Red Hat article dated 2026-04-07 in text is presented as "April 2026" while that date is only six days before corpus creation — a plausibility problem worth flagging. These are all verifiable from the files themselves.

---

## Findings

### STRUCTURAL-001

- id: STRUCTURAL-001
- severity: high
- dimension: structural_validity
- location: `research-acceptance-criteria-ai-literal.md:5`, `research-behavioral-validation-ai-agents.md:5`, `research-ceremony-rhythm-alternatives.md:5`, `research-cognitive-load-inversion.md:5`, `research-feature-unit-user-value.md:5`, `research-spec-correct-value-zero.md:5`, `research-thought-leader-frameworks-agile-ai.md:5`, `research-work-granularity-ai-speed.md:5` (all 8 subagent files, `topic:` field)
- description: All 8 claude-code-subagent research files declare a `topic` in frontmatter that does not match the `topic` in `scope.md`. scope.md is the ground-truth source-of-record, yet every subagent file carries a divergent topic.
- evidence: scope.md line 2: `topic: "Adapting Agile methodologies for Gen AI-assisted development — the granularity, specification, and validation gaps"`. Every subagent file line 5: `topic: "What are the right workflows for AI-native software development"`. Only `gemini-deep-research-output.md` line 4 matches scope.md exactly: `topic: "Adapting Agile methodologies for Gen AI-assisted development — the granularity, specification, and validation gaps"`.
- suggestion: Reconcile all subagent-file `topic:` fields to match scope.md verbatim, or document in scope.md / a manifest that subagents were briefed against a reframed topic. Leaving divergent topics in metadata is a corpus-integrity defect: downstream tooling that joins or indexes files on `topic` will silently mis-group the gemini file from the subagent files.

### STRUCTURAL-002

- id: STRUCTURAL-002
- severity: high
- dimension: structural_validity
- location: `gemini-deep-research-output.md` — entire body (lines 8–299)
- description: The gemini-deep-research file has zero source-origin tags (`[OFFICIAL]`, `[PRAC]`, `[UNVERIFIED]`), while every one of the 8 subagent files applies these tags consistently on factual claims. This is a corpus-level structural inconsistency in the evidence-tagging convention.
- evidence: Grep for `\[UNVERIFIED|\[PRAC|\[OFFICIAL` in `gemini-deep-research-output.md` returns 0 matches. Same grep across the 8 subagent files returns hundreds of matches. E.g., in `gemini-deep-research-output.md:14`: "The consensus emergent from the 2026 Future of Software Development Retreat is that engineering rigor has not disappeared; it has relocated" — no tag. In `research-thought-leader-frameworks-agile-ai.md:20`: same subject matter is tagged `[OFFICIAL]`.
- suggestion: Either retroactively tag factual claims in the gemini file with source-origin markers consistent with the subagent-file convention, or explicitly declare in the corpus README that gemini-origin content uses a different provenance convention. A reader who scans the corpus cannot presently tell which claims in the gemini file are verified vs. speculative vs. practitioner-reported.

### STRUCTURAL-003

- id: STRUCTURAL-003
- severity: high
- dimension: cross_reference_integrity
- location: `research-thought-leader-frameworks-agile-ai.md:199` vs. `research-work-granularity-ai-speed.md:129` and neither file's Sources section
- description: The same empirical claim ("Forrester's 2025 State of Agile Development found 95% of professionals affirm Agile's relevance") is tagged `[OFFICIAL — Forrester, 2025]` in one file and `[PRAC: referenced in multiple 2026 Medium articles and InfoQ coverage]` in the other — contradictory provenance. Worse: neither file's Sources section contains a Forrester URL. The tag `[OFFICIAL — Forrester, 2025]` names a primary source the file does not actually link.
- evidence: `research-thought-leader-frameworks-agile-ai.md:199`: "Forrester's 2025 State of Agile Development found 95% of professionals affirm Agile's relevance... [OFFICIAL — Forrester, 2025]". `research-work-granularity-ai-speed.md:129`: "Forrester's 2025 State of Agile Development report found 95% of professionals still affirm Agile's critical relevance... [PRAC: referenced in multiple 2026 Medium articles and InfoQ coverage]". Sources sections of both files (lines 276–301 and 214–240) contain no `forrester.com` URL or Forrester report citation.
- suggestion: Choose one provenance level — ideally `[OFFICIAL]` if a primary Forrester URL can be located and added to both Sources lists; otherwise downgrade to `[PRAC]` uniformly and flag that the claim is secondhand. Do not leave the same fact tagged inconsistently across the corpus.

### STRUCTURAL-004

- id: STRUCTURAL-004
- severity: medium
- dimension: cross_reference_integrity
- location: `research-ceremony-rhythm-alternatives.md:199` and Sources section (lines 222–251)
- description: Body text cites `arXiv, 2506.16334` as support for a `[PRAC]`-tagged claim about Lean Startup and AI, but this arXiv paper is not listed in the file's Sources section.
- evidence: Line 199: "Lean Startup methodology has been studied in combination with AI (arXiv, 2506.16334) but the research focuses on product validation cycles". The Sources section (lines 222–251) lists 28 sources; none reference arXiv 2506.16334 or link `https://arxiv.org/abs/2506.16334`. Grep for `2506` in the file returns only this single in-text reference.
- suggestion: Add the arXiv paper to the Sources section with its full URL and title, or remove the citation from the body if the paper cannot be located / verified.

### STRUCTURAL-005

- id: STRUCTURAL-005
- severity: medium
- dimension: cross_reference_integrity
- location: `research-acceptance-criteria-ai-literal.md:186` (Sources) — orphan source
- description: The Sources section lists `Agentic AI for Behavior-Driven Development Testing Using Large Language Models — SciTePress` with a URL, but the source is never cited in the body text. It is an orphan reference.
- evidence: Line 186 Sources entry: `- [Agentic AI for Behavior-Driven Development Testing Using Large Language Models — SciTePress](https://www.scitepress.org/Papers/2025/133744/133744.pdf)`. Grep for `scitepress` or `SciTePress` across the body (lines 1–158) returns no other match. The Sources list contains a reference the research never used.
- suggestion: Either cite the SciTePress paper in the body where relevant (BDD and AI discussion in section "BDD and Gherkin: Partial Help, Real Risks", lines 84–96, is the obvious home) or remove it from Sources. An orphan source implies the author compiled references without anchoring them to claims.

### STRUCTURAL-006

- id: STRUCTURAL-006
- severity: medium
- dimension: cross_reference_integrity
- location: `research-acceptance-criteria-ai-literal.md:183` (Sources) — orphan source
- description: The Sources list entry `A Benchmark for Evaluating Outcome-Driven Constraint Violations in Autonomous AI Agents — arxiv` (arxiv.org/html/2512.20798v1) is never cited in the body.
- evidence: Line 183: `- [A Benchmark for Evaluating Outcome-Driven Constraint Violations in Autonomous AI Agents — arxiv](https://arxiv.org/html/2512.20798v1)`. No `2512.20798` or matching title fragment appears in the body text (lines 1–158).
- suggestion: Cite the paper in the body (likely in the negative-constraint / anti-goals discussion at lines 58–60 or 152) or remove from Sources.

### STRUCTURAL-007

- id: STRUCTURAL-007
- severity: medium
- dimension: structural_validity
- location: `gemini-deep-research-output.md:1–6` (frontmatter)
- description: The gemini frontmatter omits `sub_question`, which every subagent file includes. The gemini file is a corpus-level synthesis, so this may be intentional — but no metadata field explicitly signals "corpus-level" vs. "sub-question-level". A consumer of the corpus cannot distinguish the gemini file's role from frontmatter alone without inferring from `content_origin`.
- evidence: Gemini frontmatter lines 1–6: `content_origin`, `date`, `topic`, `method`. Subagent frontmatter (e.g., `research-spec-correct-value-zero.md:1–6`): `content_origin`, `date`, `sub_question`, `topic`. The gemini file addresses all eight sub-questions across its sections but the frontmatter does not declare scope.
- suggestion: Add an explicit scope marker to gemini frontmatter — e.g., `scope: corpus` or `sub_question: "all (corpus synthesis)"` — so automated tooling and human readers can immediately distinguish corpus-level from sub-question-level artifacts.

### STRUCTURAL-008

- id: STRUCTURAL-008
- severity: medium
- dimension: completeness
- location: `research-ceremony-rhythm-alternatives.md:33–43` ("Shape Up as an AI-Compatible Alternative" section)
- description: The section explicitly flags its own empirical incompleteness ("no published practitioner cases as of this research specifically describe applying Shape Up to a human-AI agent team") but provides no `[UNVERIFIED]` marker on the subsequent claims about Shape Up's "fit" for AI teams. The final paragraph concedes "The fit is structural, not yet empirically validated in that context" — yet preceding paragraphs use declarative language ("Shape Up's core properties align well with AI-accelerated development") that is not tagged or hedged.
- evidence: Line 43: "However, no published practitioner cases as of this research specifically describe applying Shape Up to a human-AI agent team. The fit is structural, not yet empirically validated in that context." Lines 34–40 offer multi-bullet declarative "fit" claims without `[UNVERIFIED]`, `[PRAC]`, or any source tag on the AI-relevance claims themselves (the Shape Up methodology description is cited, but the AI-compatibility inferences are not).
- suggestion: Tag the AI-compatibility inferences with `[UNVERIFIED]` consistent with the file's own admission at line 43, or restructure so the admission precedes the bullets as a framing caveat.

### STRUCTURAL-009

- id: STRUCTURAL-009
- severity: medium
- dimension: corpus_completeness
- location: corpus-wide — no single file addresses this
- description: scope.md lists 8 sub-questions. Each is addressed by a corresponding subagent file. But scope.md's `goals` statement calls out three specific gaps — **granularity, specification, validation** — and the corpus has no single file that integrates findings across those three named gaps. The gemini file is the closest thing to an integrator but per STRUCTURAL-002 lacks source tags and per STRUCTURAL-001 uses the scope-aligned topic. There is no "synthesis" artifact that unifies the 8 sub-question files into the three-gap frame demanded by `goals`.
- evidence: scope.md line 3 goals: "Find workable solutions... to: (1) the mismatch between story granularity... (2) the specification-completeness problem... (3) the behavioral validation gap...". No file in the corpus has "granularity / specification / validation" as its top-level organizing structure. The 8 subagent files are organized by sub-question, not by the three named gaps.
- suggestion: Either add a synthesis file that explicitly frames findings under the three goal-gaps, or document in scope.md that the three gaps decompose into the 8 sub-questions and a mapping table lives elsewhere. Without this, a stakeholder reading `goals` cannot find the direct answer.

### STRUCTURAL-010

- id: STRUCTURAL-010
- severity: low
- dimension: cross_reference_integrity
- location: `research-feature-unit-user-value.md:133` and `:194`
- description: The body cites a Red Hat Developer article dated "April 2026" and the URL path is `/articles/2026/04/07/harness-engineering-...`. The corpus date is 2026-04-13 — so the cited article would be six days old at time of research. While this is structurally possible, it bears verification: the content is treated as settled `[OFFICIAL]` prior-art and quoted directly, yet the article (if real) would have had almost no time to be absorbed or cross-cited.
- evidence: Line 133: "The Red Hat Developer article on harness engineering (April 2026) points toward a specific enforcement mechanism... [OFFICIAL — developers.redhat.com/articles/2026/04/07/harness-engineering-structured-workflows-ai-assisted-development]". Line 194: `- [Harness Engineering: Structured Workflows for AI-Assisted Development — Red Hat Developer](https://developers.redhat.com/articles/2026/04/07/harness-engineering-structured-workflows-ai-assisted-development)`.
- suggestion: Verify the article exists at that URL and published on 2026-04-07. If it does, the citation is fine. If not, downgrade to `[UNVERIFIED]` or remove. The plausibility of citing a six-day-old article as settled `[OFFICIAL]` authority warrants a verification pass.

### STRUCTURAL-011

- id: STRUCTURAL-011
- severity: low
- dimension: cross_reference_integrity
- location: `research-spec-correct-value-zero.md:18,52,72,177` — arxiv 2603.25773 cited with no version suffix
- description: Sibling arxiv citations in the same file use `v1` suffix (e.g., `2602.00180v1`) but `2603.25773` is cited without version suffix in both body and Sources. Internal inconsistency in arxiv-ID formatting.
- evidence: Line 18: `[OFFICIAL, arxiv.org/html/2603.25773]`. Line 52: `[OFFICIAL, arxiv.org/html/2603.25773]`. Line 72: `[OFFICIAL, arxiv.org/html/2603.25773]`. Line 177 Sources: `[arxiv — The Specification as Quality Gate: Three Hypotheses on AI-Assisted Code Review (March 2026)](https://arxiv.org/html/2603.25773)` — no `v1` or `v2`. Compare to line 176 Sources: `https://arxiv.org/html/2602.00180v1` (with `v1`).
- suggestion: Add the version suffix for consistency, or drop `v1` from sibling citations. Mixed formats suggest the references were assembled at different times or copy-pasted without normalization.

### STRUCTURAL-012

- id: STRUCTURAL-012
- severity: low
- dimension: structural_validity
- location: `research-ceremony-rhythm-alternatives.md:71`
- description: Two source-origin tags appear back-to-back on the same paragraph, marking different sentences with different provenance levels. This is not prohibited by convention but is structurally ambiguous: which tag governs which claim?
- evidence: Line 71: "[PRAC] The concept of a 'Shadow Meeting'... appears in StandupAlice's reporting as a 2025 innovation. This eliminates the meeting entirely while preserving decision transparency. [UNVERIFIED] This pattern is structurally similar to how modern AI code review works...". The first sentence carries `[PRAC]`, the second carries `[UNVERIFIED]` — but the combined paragraph formatting suggests a single citation block.
- suggestion: Split into two paragraphs or make the tag scoping explicit (e.g., "[PRAC — first claim only]... [UNVERIFIED — analogy that follows]"). The current layout forces the reader to infer scope.

### STRUCTURAL-013

- id: STRUCTURAL-013
- severity: low
- dimension: structural_validity
- location: `research-spec-correct-value-zero.md:4` — frontmatter quoting inconsistency
- description: The file's `sub_question:` value drops the single-quoted phrase markup present in scope.md, subtly altering the identity of the field value.
- evidence: scope.md line 10: `"How are practitioners solving the 'spec-correct, value-zero' problem — where code passes all criteria but delivers no user value because the specification was incomplete?"`. File line 4: `"How are practitioners solving the spec-correct, value-zero problem — where code passes all criteria but delivers no user value because the specification was incomplete?"` — the single-quoted phrase around `spec-correct, value-zero` is missing.
- suggestion: Normalize the `sub_question:` value to match scope.md verbatim so automated indexing / joining by sub_question does not fail or silently produce near-matches. Same check should be applied to any other subagent file (the `feature-unit-user-value` file does preserve its single-quotes correctly).

---

## Re-examination pass

Per skepticism-level-3 protocol, I re-examined the corpus after initial findings to confirm I did not miss structural issues or manufacture false positives.

- Confirmed: all 9 files have required frontmatter delimiters (`---` ... `---`), title, body, and `## Sources` section.
- Confirmed: the topic-divergence (STRUCTURAL-001) is real and affects exactly 8 files; the gemini file is the only one matching scope.md.
- Confirmed: the gemini file has genuinely zero source-origin tags (STRUCTURAL-002) — this is not an artifact of the grep pattern.
- Confirmed: both orphan Sources entries in `research-acceptance-criteria-ai-literal.md` (STRUCTURAL-005, -006) are genuinely uncited in the body.
- Re-checked: the Forrester double-tag (STRUCTURAL-003) is two different files making the same fact claim with contradictory provenance — real defect.
- Did not find additional critical-severity issues. No single structural failure threatens corpus usability, but the accumulation of provenance-drift patterns is itself a structural pattern worth naming.
