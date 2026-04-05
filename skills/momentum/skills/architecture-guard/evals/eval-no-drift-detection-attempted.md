# Eval: Architecture Guard Detects Drift When Present

## Given
The momentum:architecture-guard skill is invoked with a codebase that contains changes violating an architecture decision (e.g., a SKILL.md file placed in `agents/` instead of `skills/`).

## The skill should
Read the architecture decisions document, analyze the changes, and produce findings identifying the specific decision violated, the file or pattern involved, evidence, and severity. The output should follow the structured report format with verdict FAIL.
