---
date: 2026-04-13
file_fixed: raw/gemini-deep-research-output.md
---

# Fix Log — gemini-deep-research-output.md

## FIX 1 — CRITICAL-001: Harness Engineering Term Collision
**Applied.** Added a disambiguation blockquote immediately after the Fowler/Böckeler Harness Engineering section noting that OpenAI independently uses the same term for an agent-first PR workflow, and that these are distinct concepts.

## FIX 2 — CRITICAL-002: AI-DLC Framework Contradiction
**Applied.** Replaced the "Mob Elaboration and Construction" table (which was incorrectly attributed to AI-DLC) with a corrected section. The Thoughtworks 3-3-3 model's mob rituals are now credited correctly. The AWS AI-DLC is described accurately as a three-phase (Inception/Construction/Operations) model where AI proposes plans and humans act as Validators — no mob rituals.

## FIX 3 — CRITICAL-003: Casey West Agentic Manifesto Date and Characterization
**Applied.** Two locations fixed:
- Main body (section "Solving the 'Spec-Correct, Value-Zero' Problem"): changed "early 2026" to "2025"; removed "fundamental shift" framing; recharacterized as an ADLC wrapper around SDLC, not a replacement.
- Follow-Up Q1 entry: changed "early 2026" to "2025"; removed "direct response to Agile friction" and "clean break" language; added accurate ADLC wrapper description.

## FIX 4 — CRITICAL-004: Kinetic Enterprise Doctrine — Hallucinated Attribution
**Applied.** Replaced the "Researchers at Deloitte" attribution with an [UNVERIFIED] blockquote explaining that Deloitte's "Kinetic Enterprise" trademark refers to SAP business transformation, not an AI-Agile doctrine. The conceptual framing bullets are retained but clearly marked as unverified.

## FIX 5 — HIGH-002: Missing Source-Origin Tags on High-Stakes Claims
**Applied.** Tags added to the following claims:
- "2026 Future of Software Development Retreat" consensus → `[UNVERIFIED — no primary source URL provided]` (two occurrences: main body and ceremonies section)
- AI/works™ → `[OFFICIAL — thoughtworks.com]`
- AWS "Zones of Intent" prescriptive guidance → `[OFFICIAL — docs.aws.amazon.com]`
- AWS AI-DLC in Follow-Up Q1 → `[OFFICIAL — docs.aws.amazon.com]`
- Anthropic skill-erosion research claim → `[UNVERIFIED — no primary source URL provided]`
- Comprehension test statistic → `[UNVERIFIED — no study citation provided]`

## FIX 6 — HIGH-004: EARS Notation Missing from Synthesis
**Applied.** Added a new "EARS Notation and Spec-Driven Tooling" subsection within the Specification-Completeness Problem section, immediately before "Encoding Team Standards as Infrastructure." The paragraph describes EARS notation, Amazon Kiro IDE (July 2025), and cross-references `research-acceptance-criteria-ai-literal.md`.

## FIX 7 — HIGH-005: Blind Tester Pattern — Flag Known Gap
**Applied.** Added a "Known Implementation Gap" blockquote immediately after the Context Truncation / Inferential Sensors bullets in Follow-Up Q3, before the Open-Source Tools table. Notes absence of a published open-source concrete pattern and points to Codecentric's Claude Code `.claudeignore`/`settings.json` approach in `research-behavioral-validation-ai-agents.md`.
