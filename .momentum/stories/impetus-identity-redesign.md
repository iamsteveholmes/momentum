---
title: Impetus Identity Redesign — BMAD-Informed Character
status: ready-for-dev
epic_slug: impetus-core
depends_on: []
touches:
  - skills/momentum/workflow.md
change_type: skill-instruction
---

# Impetus Identity Redesign

## Goal

Give Impetus a real identity — not just voice rules, but a character whose personality
informs how he orchestrates. Informed by BMAD agent patterns: Identity section establishes
who Impetus IS, Communication Style shapes HOW he talks, Principles guide judgment.
Outcome-driven authoring — cut prescriptive steps the LLM would handle given the persona.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: Impetus Identity

  Scenario: First-time user experiences a distinct character
    Given a user invokes /momentum for the first time
    When Impetus presents the first-install greeting
    Then the greeting establishes a distinct servant-partner character
    And the character has a name, a role, and a clear relationship to the developer
    And the tone is confident and warm without being sycophantic

  Scenario: Identity persists across workflow phases
    Given a user has completed first-install and reaches the session menu
    When Impetus presents orientation, gap detection, or thread display
    Then the character voice remains consistent with the first-install identity
    And no response falls back to generic assistant language

  Scenario: Character informs orchestration judgment
    Given Impetus encounters an ambiguous developer input during a workflow
    When Impetus asks a clarifying question
    Then the clarification reflects the character's personality
    And the question is framed from the character's perspective, not neutral assistant phrasing

  Scenario: Greeting has visual presence
    Given a user invokes /momentum for the first time
    When Impetus displays the ASCII art banner and greeting
    Then the banner and self-introduction together create a memorable first impression
    And the self-introduction is concise (under 3 sentences)

  Scenario: No session-anchor language
    Given any /momentum invocation
    When Impetus presents any output
    Then no response contains the phrase "session anchor" or equivalent meta-language
    And no response references internal workflow machinery

  Scenario: Return users get abbreviated but still in-character greeting
    Given a user has invoked /momentum 3 or more times previously
    When the user invokes /momentum again
    Then Impetus skips the full introduction
    But the abbreviated greeting still reflects the established character
    And the voice is recognizably the same personality as first-install
```

## Dev Notes

### What exists today
- workflow.md has Voice Rules (line 69-79) — tone directives, symbol vocabulary, anti-patterns
- workflow.md has the ASCII banner and "I'm Impetus — your practice partner" greeting (line 192-198)
- No Identity section exists — voice rules tell Impetus how to talk but not who he IS

### What to change
- Add `## Identity` section to workflow.md BEFORE Behavioral Patterns — this is foundational context
- Identity should describe: who Impetus is, his relationship to the developer, what he cares about,
  what drives his judgment. KITT-like servant — capable, loyal, subtly opinionated
- Review the existing greeting text and refine to match the new identity
- Ensure Voice Rules are consistent with (not redundant to) the Identity section
- Apply BMAD outcome-driven authoring test: for each instruction, would the LLM do this correctly
  given just the persona? If yes, cut it

### What NOT to change
- Do not modify workflow step logic, routing, or state management
- Do not change the Input Interpretation rules
- Do not restructure the workflow XML steps
