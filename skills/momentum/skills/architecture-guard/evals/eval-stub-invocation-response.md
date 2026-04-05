# Eval: Architecture Guard Produces Findings on Invocation

## Given
The momentum:architecture-guard skill is invoked directly by a developer outside of a sprint context.

## The skill should
Read the project's architecture decisions document, analyze recent changes (or the current codebase state), and produce a structured findings report identifying any pattern drift. The report should contain a header with verdict, findings grouped by severity, and a summary section. No stub or placeholder text should appear in the output.
