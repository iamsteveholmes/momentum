---
topic: "Feature planning artifact visualization"
goals: "Actionable design decisions for what the feature-status planning artifact should look like, what signals to show, and how to render it in a Claude Code / cmux environment"
profile: light
date: 2026-04-11
sub_questions:
  - "What layout and visual structure works best for a rich, developer-facing feature planning artifact? How do tools like Linear, Productboard, Aha!, FigJam lay out feature status? What signals are prominent? How is 'stories needed to complete this feature' represented visually?"
  - "What are hard-won lessons from teams using feature dashboards and planning views? What information turns out to be noise vs. genuinely decision-driving? What layouts cause cognitive overload and what reduces it?"
  - "How have developer CLI tools and code-adjacent tools solved the 'generated from code, rendered as rich visual' problem? What templating and rendering patterns work when a planning artifact is produced programmatically but consumed visually in a browser pane?"
---

# Research Scope: Feature planning artifact visualization

**Date:** 2026-04-11
**Profile:** light
**Goals:** Actionable design decisions for what the feature-status planning artifact should look like, what signals to show, and how to render it in a Claude Code / cmux environment

## Context (do not re-research)

We already know:
- Tech stack: HTML + Jinja2 + Mermaid.js + cmux browser pane
- Feature artifact schema: features.json with flow/connection/quality types, acceptance_condition, stories array, status (working/partial/not-working/not-started)
- Prior research covered: cognitive load theory, tool landscape survey, feature artifact schema debate, context fragmentation

## Sub-Questions

1. What layout and visual structure works best for a rich, developer-facing feature planning artifact? How do tools like Linear, Productboard, Aha!, FigJam lay out feature status? What signals are prominent? How is "stories needed to complete this feature" represented visually?

2. What are hard-won lessons from teams using feature dashboards and planning views? What information turns out to be noise vs. genuinely decision-driving? What layouts cause cognitive overload and what reduces it?

3. How have developer CLI tools and code-adjacent tools solved the "generated from code, rendered as rich visual" problem? What templating and rendering patterns work when a planning artifact is produced programmatically but consumed visually in a browser pane?
