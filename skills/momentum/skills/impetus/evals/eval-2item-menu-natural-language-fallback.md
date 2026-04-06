# Eval: 2-Item Menu — Natural Language Fallback for Removed Items

## Story

2a-3: Session-Open Menu Redesign

## Setup

- `momentum_completions = 3` (returning user)
- No open threads
- Menu has been displayed (2-item: /create, /develop)
- Developer types: "I want to run quality validation"

## Expected Behavior

1. Input Interpretation gate fires: Impetus confirms extracted intent before dispatching
2. Example confirmation: "Running quality validation — correct?"
3. On developer confirmation (Y), quality validation workflow dispatches
4. The primary menu change (removing item 4) does NOT break natural language access to removed items

## Fail Conditions

- Natural language input for old items 3–6 fails silently
- Input Interpretation gate is bypassed (dispatch fires without confirmation)
- Error occurs when typing "run quality validation" after 2-item menu is shown
- Natural language gate note is absent from SKILL.md happy path and Step 7 of workflow.md
