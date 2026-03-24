# Eval: No Thread ID (T-NNN) Visible in User-Facing Output

## Scenario

Given a session journal with two open threads, where:
- Thread 1 has `thread_id: "T-001"`, `context_summary: "Setting up authentication for the API"`, `context_summary_short: "API auth setup"`
- Thread 2 has `thread_id: "T-002"`, `context_summary: "Refactoring payment module"`, `context_summary_short: "Payment refactor"`

When Impetus displays the session journal (thread list) and any hygiene checks,

Then Impetus should:
1. Display threads using `context_summary_short` values ("API auth setup", "Payment refactor") — never "T-001" or "T-002"
2. In any hygiene warning output referencing a specific thread, use the thread's `context_summary` or `context_summary_short` — never `thread_id`
3. In the workflow resumability step (after thread selection), display the thread using `context_summary` — never `thread_id`
4. No internal identifier in T-NNN format appears anywhere in the response

## What Would Fail This Eval

- Any output containing "T-001", "T-002", or any T-NNN pattern
- Hygiene warnings that say e.g. "! Thread T-001 appears active in another tab"
- Thread list rows showing thread_id values instead of context_summary_short
- The selection confirmation or resumability step referencing a T-NNN identifier
