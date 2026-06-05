Invoke the `momentum:code-reviewer` skill — the `bmad-code-review` adapter for conduct's
per-story review leg. The skill drives the `bmad-code-review` adversarial engine non-interactively
against the story diff provided in context and returns adapter-normalized findings (canonical schema
with `stakes_class` populated, `source=bmad-code-review` stamped on every record). Follow the
skill's `workflow.md` exactly — it is the binding execution protocol.

The in-house stub reviewer is retired. No invocation path through this command reaches stub output.
