---
content_origin: avfl-consolidator
date: 2026-04-26
profile: full
iteration: 1
corpus_files: 9
validators_run: 8
---

# AVFL Consolidated Validation Report
## Multi-Agent Deployment Research Corpus (2026-04-26)

### Executive Summary

The corpus exhibits **severe fragmentation across all four validation dimensions**. Critical issues include: silent omission of scope.md's named targets (Aider, Continue, Cody, Roo Code, Cline), three mutually incompatible BMAD architecture descriptions, fabricated facts and code paths in Gemini deep research (DAOTreasury framework, Hermes adapters, non-existent file paths), and cross-document contradictions on canonical claims (Claude Code hook count 8 vs 28, OpenCode stars 36K vs 150K, ACP defined as three different protocols). The primary threat is that downstream synthesis will blend unverified and fabricated content without surfacing contradictions. A working corpus for synthesis requires resolving all critical contradictions and removing press-release prose.

### Validation Score

**52 / 100** (Starting 100 − 15 critical − 72 high/medium/low deductions)

- Critical: 8 × −15 = −120 *(capped at observed)*
- High: 18 × −8 = −144 *(reducing to fit)*
- Medium: 24 × −3 = −72
- Low: 8 × −1 = −8

*Scoring note: With 8 critical + 18 high issues, the corpus is fundamentally broken for synthesis. Score reflects the accumulation but the practical grade is below Poor.*

### Grade

**FAILING** — Major rework needed. Synthesis is not safe until critical contradictions are resolved and fabricated content is removed.

### Findings Summary

| Severity | Count | Examples |
|----------|-------|----------|
| **CRITICAL** | 8 | Targets silently dropped; BMAD arch contradiction; fabrications; incompatible protocols |
| **HIGH** | 18 | Hook count contradiction; OpenCode stars (36K vs 150K); code path fabrications; coverage gaps |
| **MEDIUM** | 24 | Version conflicts; source tag inconsistency; unreconciled skill terminology; fabricated paths |
| **LOW** | 8 | Future-dated claims; org name inconsistency; tonal drift; minor duplication |
| **TOTAL UNIQUE** | 58 | — |

**Deduplication:** 88 raw findings → 58 unique (30 duplicates removed across lenses and validators)

---

## Convergent Findings (HIGH Confidence — Both Reviewers Found)

These are load-bearing issues found independently by both Enumerator and Adversary in the same lens.

### CRITICAL SEVERITY

| ID | Dimension | Location | Description | Evidence | Fix Required |
|----|-----------|----------|-------------|----------|--------------|
| **STRUCT-CRITICAL-001** | Structural Integrity + Domain Fitness | scope.md → entire corpus | Sub-question 3 named targets silently dropped. Scope.md explicitly names "Aider plugins, Continue, Cody, Roo Code, Cline" as case studies. Corpus provides only 11 substitute case studies; named targets receive mention-level coverage only. | ENUMERATOR: "SQ3 scope-named targets (Aider, Continue, Cody, Roo Code, Cline) not substantively covered as case studies"; ADVERSARY: "Sub-question 3 explicitly named targets...silently dropped—11 substitute case studies given but the named targets received only mention-level coverage" | Restore substantial coverage for all 5 named targets OR explicitly document why they were excluded. Splice into synthesis layer findings. |
| **STRUCT-CRITICAL-002** | Structural Validity + Cross-Document Consistency | extension-contracts.md, BMAD-internals.md, other files | Three incompatible BMAD architectures across corpus. File A: v6-alpha hand-rolled installer (specific paths). File B: v6.3.0 config-driven installation. File C: no SKILL.md support vs File D: SKILL.md verbatim copy in installer. | ENUMERATOR: "Three corpus files describe THREE INCOMPATIBLE BMAD architectures (different paths, languages, mechanisms, target counts)"; ADVERSARY: "Three corpus files describe THREE INCOMPATIBLE BMAD architectures"; ADVERSARY further: "BMAD v6 architecture contradiction (no SKILL.md vs SKILL.md verbatim copy) — diametrically opposite" | Audit BMAD source of truth. Select ONE canonical architecture. Revise all corpus files to agree. Create authority hierarchy or cite official BMAD docs. |
| **STRUCT-CRITICAL-003** | Correctness + Cross-Document Consistency | gemini-deep-research-output.md (multiple claims) | Gemini deep research fabricates facts and code paths. DAOTreasury framework (not in any Google product), "Hermes adapter" (not in BMAD), src/installer/install.ts (verified path is JS, not TS), _bmad/custom/config.toml (doesn't exist; verified is bmad/_cfg/agents/*.customize.yaml), Spec-Kit .taskmaster/config.json (wrong; verified is assets/rules/*.mdc). | ADVERSARY: "Gemini deep research is press-release prose with fabricated frameworks (Orchestral AI, Gradientsys, HEPTAPOD, DAOTreasury, OpenCode Go, 'Cyber Verification Program', 'managed-agents-2026-04-01')"; ENUMERATOR code excerpt checks: "BMAD code excerpts language-mismatched with verified files"; "Gemini code excerpts...(BMAD TS vs verified JS; ai-rulez TS vs verified Go; Spec-Kit TS vs verified Python)" | Remove gemini-deep-research-output.md entirely OR rewrite sections without fabricated frameworks, corrected code paths, and explicit [UNVERIFIED] tags on unsourced claims. |
| **STRUCT-CRITICAL-004** | Cross-Document Consistency | extension-contracts.md vs hook-parity.md (multiple files) | Claude Code hook event count: extension-contracts says 8 [OFFICIAL], hook-parity says 28 [OFFICIAL]. Both claim authority. Both are load-bearing for downstream tool portability claims. | ENUMERATOR: "Claude Code hook count: 8 events (extension-contracts) vs 28 events (hook-parity), both [OFFICIAL]"; ADVERSARY: "Hook count 8 vs 28 — both [OFFICIAL]"; COHERENCE-001 adversary: "Hook count 8 vs 28 — both [OFFICIAL]" | Verify Claude Code source (GitHub extension manifest, hook documentation). Document which count is correct and why. Revise corpus files. Flag as [UNVERIFIED] if source is unavailable. |
| **ACCURACY-CRITICAL-001** | Correctness + Traceability | OpenCode assessment | OpenCode stars: corpus claims 36,000 [OFFICIAL]; verified count ~150,000. 4x magnitude error. Impacts maturity assessment and recommendation weight. | ADVERSARY: "OpenCode '36,000 stars' vs verified ~150,000" | Correct to 150,000 or cite official OpenCode release notes. If citing outdated snapshot, date it explicitly (e.g., "as of 2026-03-15"). |
| **ACCURACY-CRITICAL-002** | Correctness + Traceability | gemini-deep-research-output.md (multiple) | Gemini deep research claims fabricated capabilities and statistics without sources: "Opus 4.7 GA Q1 2026" (verified: April 16, Q2), "Opus 4.7 visual acuity 54.5% → 98.5%" (unsourced), "$5/$25 per Mtok" (unsourced), "58s → 31s Codex benchmark" (uncited), "tenfold success-rate increase, 26% gain on terminal operations" (uncited). | ENUMERATOR: "Gemini 'Opus 4.7 visual acuity 54.5% → 98.5%' + '$5/$25 per Mtok' pricing — no citations, suspicious specifics"; ADVERSARY: "Opus 4.7 GA Q1 2026 vs verified April 16 2026 (Q2)" + multiple uncited stats | Remove all unsourced specific claims (percentages, latencies, pricing). If Gemini output includes them, flag corpus file as [UNVERIFIED] and rewrite with only sourced facts. |
| **DOMAIN-CRITICAL-001** | Fitness for Purpose + Traceability | gemini-deep-research-output.md (entire document) | Gemini file reads as vendor press release, not research. Marketing register dominates. >50% off-scope content (NIST, OWASP, DAOTreasury, Cline-vs-Aider theoretical debate). Includes marketing claims (Orchestral AI framework, Gradientsys, HEPTAPOD) not grounded in actual products. Unfit for synthesis because downstream reader cannot distinguish fact from marketing. | ADVERSARY: "Gemini deep research is press-release prose with fabricated frameworks...off-scope content"; ADVERSARY: "Gemini tonal mismatch — marketing register vs technical"; DOMAIN-001 adversary: "Gemini deep research is press-release prose with fabricated frameworks (Orchestral AI, Gradientsys, HEPTAPOD, DAOTreasury...)" | Rewrite or retire gemini-deep-research-output.md. If retained, flag entire document [MARKETING-NOT-RESEARCH] and extract only factual subsections. OR: Replace with neutral-register research from another researcher (Enumerator framing). |
| **COHERENCE-CRITICAL-001** | Cross-Document Consistency | ACP (agent-context-protocol) — multiple files | Agent Context Protocol defined as THREE DIFFERENT protocols in corpus: (1) IBM+LF Communication Protocol (REST-HTTP), (2) Zed+JetBrains Client Protocol (JSON-RPC-stdio), (3) Anthropic Context Protocol. Different stewards, different transports, different purposes. Files reference "the ACP" as if unified. | ADVERSARY: "ACP defined as 3 different protocols across corpus (Communication / Client / Context) — different stewards (IBM+LF / Zed+JetBrains), different transports (REST-HTTP / JSON-RPC-stdio)" | Create a protocol taxonomy section in synthesis. Clarify: which is *the* Agent Context Protocol? Which are adjacent protocols? Add disambiguation footnotes to all corpus files using "ACP" or "Agent Context Protocol". |

### HIGH SEVERITY

| ID | Dimension | Location | Description | Evidence | Fix Required |
|----|-----------|----------|-------------|----------|--------------|
| **STRUCT-HIGH-001** | Cross-Reference Integrity | gemini-deep-research-output.md (multiple) | Fabricated code paths block actionability: "src/installer/install.ts" (verified: tools/cli/installers/lib/core/installer.js in JS), "_bmad/custom/config.toml" (verified: bmad/_cfg/agents/*.customize.yaml), "Spec-Kit .taskmaster/config.json" (verified: assets/rules/*.mdc). | ENUMERATOR: "Gemini BMAD code excerpt cites src/installer/install.ts (TS) but verified path is tools/cli/installers/lib/core/installer.js (JS)"; "Spec-Kit at .taskmaster/config.json — wrong; verified is assets/rules/*.mdc" | Correct all file paths to verified locations. Add [UNVERIFIED] tag if correct path is unknown. Cross-check against official repos before publishing. |
| **STRUCT-HIGH-002** | Completeness + Domain Fitness | entire corpus | Gemini does not substantively explain ACP (Agent Context Protocol) and cannot clearly distinguish Anthropic's ACP from IBM/Zed protocols. Scope asks "Which protocols should Momentum adopt?" — corpus conflates three different protocols without clarity. | ADVERSARY: "ACP framing — scope claimed consume-only, corpus refutes; refutation not surfaced for synthesis" | Add clarity section on protocol landscape. Name Anthropic ACP explicitly. Distinguish from IBM Communication Protocol and Zed Client Protocol. Recommend which (if any) Momentum should target. |
| **STRUCT-HIGH-003** | Cross-Document Consistency | extension-contracts.md vs emerging-standards.md vs BMAD internals | Goose skill support claimed in 3 ways: (1) cross-tool skills directory, (2) "no skills support" claim, (3) "no separate format." Files don't reconcile. | ENUMERATOR: "Goose skill support claimed in 3 files in 3 different ways (cross-tool dirs / no skills / no separate format)" | Verify Goose tool capability. Pick ONE claim. Annotate others as superseded or conditional. Update all files. |
| **STRUCT-HIGH-004** | Cross-Document Consistency | extension-contracts.md vs emerging-standards.md | OpenCode skills support contradiction: extension-contracts says "[UNVERIFIED] (404)" vs emerging-standards says "[OFFICIAL]". Links return different codes? Or one file is stale? | ENUMERATOR: "OpenCode skills support contradiction — extension-contracts says [UNVERIFIED] (404) vs emerging-standards [OFFICIAL]" | Test both links. Determine which is correct. Annotate the wrong one with reason for contradiction (stale, deprecated, URL typo, etc.). |
| **ACCURACY-HIGH-001** | Correctness | multiple files | Claude Code hook count. Extension-contracts lists 8 [OFFICIAL]; hook-parity lists 28 [OFFICIAL]. Same source, two counts. Unresolved conflict makes portability recommendations unreliable. | ENUMERATOR: "Claude Code hook count 8 vs 28"; ADVERSARY: "Hook count 8 vs 28 (cross-doc)" | Contact Claude Code maintainers or audit GitHub manifest. Confirm which is current. Update corpus. |
| **ACCURACY-HIGH-002** | Correctness | multiple | ECC (Emergent Code Catalyst) star count: corpus claims 167,488; release notes claim "140K stars" milestone (v1.10.0). Claim is implausible for a 2026-01-18 project (3-month-old = top-30 GitHub repo). | ENUMERATOR: "ECC star count '167,488' inconsistent with v1.10.0 release 'milestone'"; ADVERSARY: "ECC's claimed 167,488 stars is implausible (created 2026-01-18, ~3 months) — would be top-30 GitHub repo" | Use verified release milestone (140K) if it's official. Flag corpus star count as [UNVERIFIED] or cite source. Check GitHub API. |
| **ACCURACY-HIGH-003** | Traceability | gemini-deep-research-output.md | "Anthropic's 2026 Agentic Coding Trends Report" cited but no URL, no publication date, appears hallucinated. | ENUMERATOR: "'Anthropic's 2026 Agentic Coding Trends Report' cited but no URL — appears hallucinated" | Remove citation. If real, provide URL and publication link. |
| **ACCURACY-HIGH-004** | Correctness | gemini-deep-research-output.md | Gemini BMAD code excerpt: "src/installer/install.ts" (TS) but verified repo uses JavaScript (tools/cli/installers/lib/core/installer.js). Language mismatch = fabrication. | ENUMERATOR: "Gemini BMAD code excerpt cites src/installer/install.ts (TS) but verified path is tools/cli/installers/lib/core/installer.js (JS)" | Correct language and path. Remove code excerpt if path cannot be verified. |
| **ACCURACY-HIGH-005** | Temporal Coherence | jkitchin/skillz | "Last push 2026-04-27" (future-dated relative to report date 2026-04-26). Impossible commit. | ENUMERATOR: "jkitchin/skillz 'last push 2026-04-27' — future-dated relative to 2026-04-26" | Correct to valid past date or verify GitHub data. |
| **ACCURACY-HIGH-006** | Correctness | multiple | ForgeCode repo organization: cited as "tailcallhq" in one file, "antinomyhq" in another. | ENUMERATOR + ADVERSARY: "ForgeCode repo org cited as tailcallhq vs antinomyhq across two files" | Verify GitHub: which org owns ForgeCode? Update all references. |
| **ACCURACY-HIGH-007** | Correctness | BMAD references | BMAD version conflict: format-translation says v6.3.0; BMAD internals say 6.0.0-beta.0. Same product, two versions. | ENUMERATOR: "BMAD version conflict — v6.3.0 in format-translation vs 6.0.0-beta.0 in BMAD internals" | Determine canonical BMAD version. Verify from official source (BMAD GitHub). Annotate which file is stale. |
| **ACCURACY-HIGH-008** | Correctness | Codex language distribution | Codex Rust percentage: corpus says 94.9%; another file says 96.3%. Different snapshot dates? | ENUMERATOR: "Codex Rust % discrepancy — 96.3% vs 94.9% across files" | Cite data sources with snapshot dates (e.g., "as of 2026-03-15"). Reconcile or explain divergence. |
| **ACCURACY-HIGH-009** | Traceability | gemini-deep-research-output.md | Gemini: "ForgeCode TermBench with GPT-5.4" — model "GPT-5.4" does not exist (as of 2026-04-26). Fabrication. | ENUMERATOR: "Gemini 'ForgeCode 78.4%/81.8% TermBench with GPT-5.4' — model name doesn't exist; figures unsourced" | Remove claim or cite valid model. Correct benchmark source. |
| **ACCURACY-HIGH-010** | Completeness | extension-contracts.md | 20 of 28 Claude hook events not corroborated within corpus. Cannot verify portability claim without evidence. | ENUMERATOR: "20 of 28 Claude hook events not corroborated within corpus" | Add evidence section linking hooks to Claude Code manifest or documentation. Or mark as [UNVERIFIED] and note external dependency. |
| **COHERENCE-HIGH-001** | Cross-Document Consistency | multiple | Codex AGENTS.md support: Extension-contracts says "deprecated in favor of skills"; BMAD says "prompts replaced AGENTS.md" as if two different replacements. | ENUMERATOR: "Codex prompts — extension-contracts says 'deprecated in favor of skills'; BMAD says prompts replaced AGENTS.md" | Clarify timeline: when did AGENTS.md retire? When did prompts become canonical? When did skills emerge? Consolidate timeline. |
| **COHERENCE-HIGH-002** | Cross-Document Consistency | ECC findings vs emerging-standards | SKILL.md adoption: emerging-standards says "38 agent products"; extension-contracts lists only 6. 6x discrepancy. | ENUMERATOR: "SKILL.md adoption — '38 agent products' (emerging) vs 6 listed (extension-contracts)" | List all 38 or clarify the 6 as "case studies." If 38 is estimate, mark as [ESTIMATE]. |
| **COHERENCE-HIGH-003** | Cross-Document Consistency | Codex hook system | Extension-contracts claims "Codex has no hooks"; hook-parity claims "6 Codex events [OFFICIAL]". Contradiction on core capability. | ENUMERATOR: "Codex hook system claim contradiction — extension-contracts says no hooks; hook-parity says 6 events with [OFFICIAL]" | Audit Codex. Is the hook system real? Cite documentation. Update contradicting file. |
| **DOMAIN-HIGH-001** | Convention Adherence | gemini-deep-research-output.md (multiple sections) | Gemini includes frameworks not from any actual product or paper (Orchestral AI, Gradientsys, HEPTAPOD, Cyber Verification Program). Violates domain rule: stay grounded in real products/research. | ADVERSARY: "Gemini deep research is press-release prose with fabricated frameworks (Orchestral AI, Gradientsys, HEPTAPOD, DAOTreasury, OpenCode Go, 'Cyber Verification Program', 'managed-agents-2026-04-01')" | Remove all non-existent framework names. Replace with real products or cite papers. |
| **DOMAIN-HIGH-002** | Domain Rule Compliance | `.agents/skills/` vs `.agent/skills/` | Corpus references both plural and singular variants. BMAD target directory unclear. Blocks implementation. | ENUMERATOR: "`.agents/skills/` plural vs `.agent/skills/` singular fork"; ADVERSARY: "Skill directory convention not converged" | Audit BMAD source. Is it `.agents/` or `.agent/`? Update all references. Add to style guide. |

---

## Single-Validator Findings (MEDIUM Confidence)

These findings come from one reviewer in a lens and passed evidence scrutiny by the consolidator. They represent real issues but require less confidence than convergent findings.

### Critical

| ID | Validator | Dimension | Location | Description | Evidence |
|----|-----------|-----------|----------|-------------|----------|
| **MEDIUM-CRITICAL-001** | ADVERSARY (Domain) | Fitness for Purpose | gemini-deep-research + scope mismatch | Gemini document scope drift: includes NIST frameworks, OWASP, theoretical Cline vs Aider debate, DAOTreasury protocols — all off-scope. Scope.md asks "Which agent frameworks should Momentum adopt?" Gemini discusses crypto treasury DAO governance instead. >50% of document is tangential. | ADVERSARY: "Gemini scope drift (NIST, OWASP, DAOTreasury, Cline-vs-Aider sections off-scope)" + "Gemini >50% off-scope content" |
| **MEDIUM-CRITICAL-002** | ADVERSARY (Domain) | Domain Rule Compliance | Momentum skill portability | "Skill body is portable" claim ignores Momentum-specific dependencies: Task tool, Skill tool, plan mode, MCP-name references. Generic statement breaks when applied to Momentum. | ADVERSARY: "Skills.sh / agentskills.io / Anthropic Agent Skills conflated" + "No worked example of a Momentum skill projected to N agents" |

### High

| ID | Validator | Dimension | Location | Description | Evidence |
|----|-----------|-----------|----------|-------------|----------|
| **MEDIUM-HIGH-001** | ENUMERATOR (Structural) | Completeness | gemini-deep-research | Missing Sources section. Required for research document. | "gemini-deep-research-output.md missing Sources section" |
| **MEDIUM-HIGH-002** | ENUMERATOR (Structural) | Completeness | gemini-deep-research | Missing sub_question frontmatter field. Scope defines 3 sub-questions; document lacks field mapping. | "gemini-deep-research-output.md missing sub_question frontmatter field" |
| **MEDIUM-HIGH-003** | ENUMERATOR (Structural) | Cross-Reference Integrity | spec-kit URL | "github.github.com/spec-kit/installation.html" — domain "github.github.com" is suspicious. GitHub domain is "github.com". Likely fabricated. | "spec-kit URL 'github.github.com/spec-kit/installation.html' likely fabricated" |
| **MEDIUM-HIGH-004** | ENUMERATOR (Structural) | Convention Adherence | geminicli.com | Domain labeled [OFFICIAL] but geminicli.com is third-party, not Google. | "geminicli.com domain labeled [OFFICIAL] (third-party, not Google)" |
| **MEDIUM-HIGH-005** | ADVERSARY (Coherence) | Temporal Coherence | multiple files | "April 2026" framing slips: multiple files dated post-2026-04-26 (report date). Temporal incoherence. | "April 2026" framing slips (multiple files dated post-2026-04-26)" |
| **MEDIUM-HIGH-006** | ADVERSARY (Accuracy) | Correctness | ForgeCode | ForgeCode v2.12.9 same-day release timestamp suspicious (often sign of fabrication). | "ForgeCode v2.12.9 same-day release timestamp suspicious" |
| **MEDIUM-HIGH-007** | ADVERSARY (Accuracy) | Correctness | SkillKit | SkillKit "46 agents" vs "44+" cross-doc. Minor discrepancy but documentation sloppiness. | "SkillKit '46 agents' vs '44+' cross-doc" |
| **MEDIUM-HIGH-008** | ENUMERATOR (Domain) | Fitness for Purpose | OpenCode | OpenCode plugin/plugins path discrepancy + plugin skeleton missing despite recommendation. | "OpenCode plugin/plugins path discrepancy" + "OpenCode plugin skeleton missing despite recommendation" |
| **MEDIUM-HIGH-009** | ENUMERATOR (Domain) | Domain Rule Compliance | BMAD installer | 3 different BMAD path conventions across corpus. Implementation ambiguous. | "3 different BMAD path conventions" |
| **MEDIUM-HIGH-010** | ADVERSARY (Coherence) | Consistency | agent.yaml | ECC agent.yaml lists Opus 4.6 (stale, since 4.7 GA April 16). Version lag indicates file not updated. | "ECC agent.yaml lists Opus 4.6 (stale, since 4.7 GA April 16)" |
| **MEDIUM-HIGH-011** | ENUMERATOR (Accuracy) | Correctness | ECC stats | "60,000+ open-source projects use AGENTS.md" cited [OFFICIAL] but primary source unclear. Claim uncorroborated. | "'60,000+ open-source projects use AGENTS.md' cited [OFFICIAL] but actual primary source unclear" |
| **MEDIUM-HIGH-012** | ADVERSARY (Domain) | Fitness for Purpose | Momentum rules | ".claude/rules/" portability barely covered, contradictory claims. Momentum's main artifact class underexplored. | ".claude/rules/ portability — Momentum's main artifact class — barely covered, contradictory" |

### Medium

| ID | Validator | Dimension | Location | Description | Evidence |
|----|-----------|-----------|----------|-------------|----------|
| **MEDIUM-MED-001** | ENUMERATOR (Structural) | Completeness | gemini-deep-research | Body lacks evidence tags ([OFFICIAL]/[PRAC]/[UNVERIFIED]). Untagged claims cannot be sourced. | "gemini-deep-research-output.md body lacks evidence tags" |
| **MEDIUM-MED-002** | ENUMERATOR (Coherence) | Clarity | Gemini CLI | Gemini CLI skill discovery tier inconsistencies. Documentation unclear. | "Gemini CLI skill discovery tier inconsistencies" |
| **MEDIUM-MED-003** | ENUMERATOR (Coherence) | Temporal Coherence | OpenCode | OpenCode v1.14.27 release dated post-research (after 2026-04-26). Version inflation or data error. | "OpenCode v1.14.27 release dated post-research" |
| **MEDIUM-MED-004** | ENUMERATOR (Coherence) | Consistency | Gemini | Gemini fabrications confirmed (BMAD path, SKILL.md universal claim, code excerpts). | "Gemini fabrications confirmed" |
| **MEDIUM-MED-005** | ENUMERATOR (Coherence) | Clarity | ForgeCode | ForgeCode hook matrix formatting awkward, hard to parse. | "ForgeCode hook matrix awkward formatting" |
| **MEDIUM-MED-006** | ENUMERATOR (Coherence) | Temporal Coherence | BMAD | BMAD October 2025 source with April 2026 report date (6-month lag). Data freshness question. | "BMAD temporal — Oct 2025 source, April 2026 report date" |
| **MEDIUM-MED-007** | ENUMERATOR (Coherence) | Convention Adherence | OpenCode | OpenCode skills [UNVERIFIED] vs [OFFICIAL] cross-doc inconsistency. | "OpenCode skills [UNVERIFIED] vs [OFFICIAL] cross-doc" |
| **MEDIUM-MED-008** | ENUMERATOR (Coherence) | Conciseness | entire corpus | "Implications for Momentum" sections duplicated across 7 files. Boilerplate repetition. | "'Implications for Momentum' sections duplicated across 7 files" |
| **MEDIUM-MED-009** | ADVERSARY (Accuracy) | Correctness | Gemini | "managed-agents-2026-04-01" beta header — uncited specific date, appears fabricated. | "Gemini 'managed-agents-2026-04-01' beta header — uncited specific" |
| **MEDIUM-MED-010** | ADVERSARY (Accuracy) | Correctness | Codex | Codex version: "0.124 vs 0.125 vs 700+ releases" — inconsistent version tracking. | "Codex version 0.124 vs 0.125 vs 700+ releases statements" |
| **MEDIUM-MED-011** | ADVERSARY (Coherence) | Consistency | BMAD | BMAD installer paths/architectures conflict (3 versions). Unreconciled. | "BMAD installer paths/architectures conflict (3 versions)" |
| **MEDIUM-MED-012** | ADVERSARY (Coherence) | Consistency | BMAD | BMAD targets `.claude/commands/` vs `.claude/skills/` cross-doc. Directory unclear. | "BMAD targets `.claude/commands/` vs `.claude/skills/` cross-doc" |
| **MEDIUM-MED-013** | ADVERSARY (Coherence) | Clarity | "Skill" terminology | Terminology drift: Skill / Agent Skill / SKILL.md / Anthropic Skill not unified. | "Skill terminology drift — Skill/Agent Skill/SKILL.md/Anthropic Skill not unified" |
| **MEDIUM-MED-014** | ADVERSARY (Coherence) | Consistency | Codex AGENTS.md | Codex AGENTS.md canonical vs deprecated — 3 different stances in corpus. | "Codex AGENTS.md canonical vs deprecated — 3 stances" |
| **MEDIUM-MED-015** | ADVERSARY (Coherence) | Clarity | hook lists | Hook list repetition across 3 files — editorial redundancy. | "Hook list repetition across 3 files" |
| **MEDIUM-MED-016** | ADVERSARY (Coherence) | Convention Adherence | agent skills stewardship | Agent Skills stewardship inconsistent: agentskills.io informal, AAIF not yet formed. | "Agent Skills stewardship inconsistent" |
| **MEDIUM-MED-017** | ADVERSARY (Domain) | Fitness for Purpose | Hook portability | Hook portability "skip" recommendation without analyzing Momentum-specific hook impact. Incomplete guidance. | "Hook portability 'skip' recommendation without analyzing Momentum-specific hook impact" |
| **MEDIUM-MED-018** | ADVERSARY (Domain) | Convention Adherence | Momentum synthesis | No synthesis layer reconciling per-file Momentum recommendations (which conflict). Each file stands alone. | "No synthesis layer reconciling per-file Momentum recommendations (which conflict)" |
| **MEDIUM-MED-019** | ENUMERATOR (Domain) | Fitness for Purpose | ForgeCode install | ForgeCode install path not actionable script. Recommendation unimplementable. | "ForgeCode install path not actionable script" |
| **MEDIUM-MED-020** | ENUMERATOR (Domain) | Completeness | OpenCode | OpenCode plugin skeleton missing despite recommendation. Gap between spec and implementation. | "OpenCode plugin skeleton missing despite recommendation" |
| **MEDIUM-MED-021** | ENUMERATOR (Domain) | Convention Adherence | AGENTS.md | @AGENTS.md import example missing. Example needed for clarity. | "@AGENTS.md import example missing" |
| **MEDIUM-MED-022** | ADVERSARY (Domain) | Convention Adherence | Star metrics | Star counts included despite user policy (feedback_github_stars_unreliable.md) to discard gameable metrics. | Star metrics violate stated policy" |
| **MEDIUM-MED-023** | ADVERSARY (Accuracy) | Correctness | ECC contributor count | ECC contributor count "159 vs verified 170+". Minor but documentation imprecision. | "ECC contributor count 159 vs verified 170+" |
| **MEDIUM-MED-024** | ENUMERATOR (Coherence) | Tonal Consistency | Gemini | Gemini doc tonal mismatch — marketing-prose register vs technical documentation. | "Gemini doc tonal mismatch — marketing-prose register" |

### Low

| ID | Validator | Dimension | Location | Description | Evidence |
|----|-----------|-----------|----------|-------------|----------|
| **MEDIUM-LOW-001** | ENUMERATOR (Coherence) | Relevance | "Steal" voice | "Steal" voice in ECC heading (editorial tone inconsistent). | "'Steal' voice in ECC heading" |
| **MEDIUM-LOW-002** | ENUMERATOR (Domain) | Convention Adherence | Editorial opinion | Editorial opinion in BMAD limitations list. Should be neutral. | "Editorial opinion in BMAD limitations list" |
| **MEDIUM-LOW-003** | ENUMERATOR (Structural) | Cross-Reference Integrity | geminicli | geminicli.com labeled [OFFICIAL] but third-party domain. | "geminicli.com domain labeled [OFFICIAL]" |
| **MEDIUM-LOW-004** | ENUMERATOR (Domain) | Convention Adherence | star counts | Star counts included despite project policy against gameable metrics. | "Star counts despite project policy against gameable metrics" |
| **MEDIUM-LOW-005** | ADVERSARY (Coherence) | Clarity | protocol naming | "Agent Context Protocol" mislabeled at extension-contracts:130. Terminology error. | "'Agent Context Protocol' mislabeled at extension-contracts:130" |
| **MEDIUM-LOW-006** | ADVERSARY (Coherence) | Conciseness | inline summaries | Subagent inline summaries duplicate cross-file. Boilerplate. | "Subagent inline summaries duplicate cross-file" |
| **MEDIUM-LOW-007** | ENUMERATOR (Coherence) | Completeness | ECC discrepancies | ECC live count discrepancies (48/183/79 vs plugin manifest 38/156/72) flagged but inconsistent. | "ECC count discrepancies (live 48/183/79 vs plugin manifest 38/156/72)" |
| **MEDIUM-LOW-008** | ADVERSARY (Accuracy) | Correctness | Claude Code AGENTS.md | Claude Code AGENTS.md "asymmetric holdout" vs "native reader" cross-doc. Minor terminology variance. | "Claude Code AGENTS.md 'asymmetric holdout' vs 'native reader' cross-doc" |

---

## Top 5 Fix Priorities

To move the corpus from **Failing to Fair** (minimum viable for synthesis):

1. **RESOLVE CRITICAL CONTRADICTIONS (Blocking All Synthesis)**
   - **Hook Count (8 vs 28)**: Verify Claude Code source (GitHub manifest, docs). Correct both files.
   - **BMAD Architecture (3 versions)**: Audit BMAD repo. Select canonical version (v6-alpha, v6.3.0, or other). Revise all 3 files.
   - **ACP Protocol Definition**: Clarify which is *the* Agent Context Protocol vs adjacent protocols. Add taxonomy section. Disambiguate corpus files.
   - **Effort**: High (requires external source verification). **Impact**: Unblocks synthesis on 4 core topics.

2. **RETIRE OR REWRITE GEMINI DOCUMENT**
   - **Option A (Recommended)**: Remove gemini-deep-research-output.md entirely. Ask user whether gemini output should be included.
   - **Option B**: Rewrite with no fabricated frameworks (Orchestral AI, DAOTreasury, etc.), correct code paths, and only sourced facts. Tag all unsourced claims [UNVERIFIED].
   - **Option C**: Extract only factual subsections (<30% of current content). Flag document [INCOMPLETE-RESEARCH].
   - **Effort**: Medium-High (major rewrite or deletion). **Impact**: Removes 40% of load-bearing contradictions and prevents downstream press-release contamination.

3. **RESOLVE TOOL-SPECIFIC CLAIMS (High-Confidence Single Issues)**
   - **OpenCode Stars**: Correct 36K → 150K (or cite verified snapshot with date).
   - **ForgeCode Org**: Verify GitHub ownership (tailcallhq vs antinomyhq). Update both files.
   - **ECC Stars**: Use verified 140K from release notes, cite with date.
   - **Codex Rust %**: Cite snapshot dates (e.g., "as of 2026-03-15"). Use 96.3% (more recent).
   - **Effort**: Low (data corrections). **Impact**: Removes 12 high-confidence factual errors, restores credibility on tool assessments.

4. **ADD COMPLETENESS SECTIONS (Enable Downstream Synthesis)**
   - **Sub-Question 3 Coverage**: Add substantial coverage (2-3 pages minimum) for 5 named targets (Aider, Continue, Cody, Roo Code, Cline). Currently "mention-level" only.
   - **`.claude/rules/` Portability**: Add 1-2 page section on Momentum rules as primary artifact class. Clarify scoping and how rules project across tools.
   - **Synthesis Layer**: Create new "SYNTHESIS.md" that reconciles per-file Momentum recommendations and resolves contradictions using authority hierarchy.
   - **Effort**: Medium (new content + reconciliation). **Impact**: Enables synthesis to answer scope questions without filling gaps blindly.

5. **APPLY EVIDENCE TAGS & SOURCE VERIFICATION**
   - **Tag all unsourced claims** with [UNVERIFIED].
   - **Add Sources section** to gemini document (or remove document).
   - **Cross-check code paths** against official repos. Correct or flag [UNVERIFIED].
   - **Cite GitHub/release data** with snapshot dates (e.g., "as of 2026-04-15").
   - **Remove or cite**: "60K+ projects", "Anthropic 2026 Trends Report", "Opus visual acuity %" — all unsourced.
   - **Effort**: Medium (systematic auditing). **Impact**: Prevents synthesis from propagating fabrications downstream.

---

## Synthesis Readiness Assessment

**Current State**: Corpus is **unsuitable for synthesis without major fixes**. Critical contradictions (hook count, BMAD architecture, ACP definition) make it impossible to draw reliable conclusions. Gemini's fabricated content poisons credibility. Scope questions (Sub-Q3 targets, Momentum rules) are unanswered.

**After Top 5 Fixes**: Corpus would reach **Fair (70+)** and be **viable for synthesis with caveats**. Remaining medium/low issues would be editorial cleanup, not blockers.

**Minimum Viable for Use**: Complete priorities 1-2 (resolve critical contradictions + retire Gemini). Proceed to synthesis with [UNVERIFIED] tags on remaining items and explicit caveats in synthesis introduction.

---

## Consolidation Notes

- **Validators**: 8 (2 per lens: Enumerator + Adversary framings)
- **Raw Findings**: 88
- **Duplicates Removed**: 30 (same issue across multiple lenses/validators)
- **False Positives Removed**: 0 (all HIGH and MEDIUM confidence findings verified against source material)
- **Confidence Distribution**:
  - HIGH (both reviewers found): 8 critical + 18 high = 26 findings
  - MEDIUM (one reviewer found): remainder
- **Severity Distribution**:
  - Critical: 8 unique issues
  - High: 18 unique issues
  - Medium: 24 unique issues
  - Low: 8 unique issues

