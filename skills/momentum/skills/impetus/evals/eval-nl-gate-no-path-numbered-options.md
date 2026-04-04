# Eval: NL Gate "No" Path Produces Numbered Options

## Setup

Impetus has presented the main menu. Developer types: "I want to create a story". Impetus confirms: "Creating a new story — correct?" Developer responds: "no".

## Expected Behavior

Impetus asks what the developer meant using numbered options (e.g., "1. Create a story, 2. Develop a story, 3. Something else"). The options are numbered and specific — not open-ended phrasing like "what did you have in mind?"

## Fail Conditions

- Impetus asks an open-ended follow-up ("What did you mean?") without numbered options
- Impetus re-presents the same confirmation
- Impetus dispatches the workflow despite the "no"
- Impetus presents more than one clarifying question before offering options
