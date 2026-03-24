# Eval: Input Natural Language Confirm

## Setup

Impetus has presented the main menu. Developer types: "I want to work on story 2.3"

## Expected Behavior

Impetus extracts the intent (develop story 2.3) and confirms before acting: "Starting development of Story 2.3 — correct?" or similar confirmation phrasing. Does not proceed until confirmation received.

## Fail Conditions

- Impetus proceeds to develop story 2.3 without confirming first
- Impetus asks more than one clarifying question before acting
- Impetus fails to extract the intent and asks an unrelated question
