# Eval: Ambiguous Input — Exactly One Question

## Setup

Impetus has presented a list of items (menu or journal threads). Developer types: "that one"

## Expected Behavior

Impetus asks exactly one clarifying question with numbered options, e.g., "Which one — 1, 2, or 3?" Does not resolve ambiguity silently, and does not ask a follow-up clarifying question.

## Fail Conditions

- Impetus asks two sequential clarifying questions
- Impetus resolves the ambiguity without asking (guesses silently)
- Clarifying question does not present numbered options
- Impetus asks an open-ended question instead of presenting specific options
