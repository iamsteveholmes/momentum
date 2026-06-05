# Eval: Retired Stub — No Standalone Reviewer Body

## Given
The momentum:code-reviewer skill is invoked without following its workflow.md (e.g., the skill
body alone is read and treated as a standalone reviewer instruction set).

## The skill should
Not produce review findings from its body text alone. The skill body explicitly states that the
in-house stub reviewer has been retired and that all review logic runs via workflow.md. Reading
the SKILL.md body produces no findings and no structured report — it is a shim notice, not a
reviewer.
