# Eval: Adapter Routing — bmad-code-review Is the Reviewer of Record

## Given
The momentum:code-reviewer skill is invoked with a story diff via the code-reviewer command or
directly by the Conductor. The skill's workflow.md is followed.

## The skill should
Route all review execution to the bmad-code-review adversarial engine (not to any in-house
reviewer body). The findings returned are adapter-normalized: each finding carries
`source=bmad-code-review`, a populated `stakes_class` (one of: security-auth-isolation,
irreversible-destructive, high-blast-radius-architecture, or routine), and the canonical
finding schema fields. No stub output or placeholder text is produced. Disposition and
timing-tier fields are absent (fixer-assigned downstream, not by this adapter).
