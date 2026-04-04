# Eval: Productive Waiting

## Scenario

Given Impetus dispatches a background subagent (e.g., code-reviewer, VFL) using `run_in_background: true`, Impetus must maintain dialogue with the developer while the subagent runs. The dialogue must stay on the topic of the work just completed — never switch to unrelated subjects.

Two patterns are acceptable:

1. **Substantive discussion** — Impetus surfaces an implementation summary, discusses architectural context, reviews acceptance criteria coverage, or previews what comes next
2. **Acknowledged pause** — when no substantive discussion is available, Impetus explicitly acknowledges the wait (e.g., "The review is running — I'll have results shortly") rather than going silent

"Same topic" means: the work just completed, ACs being verified, architectural context, or what comes next in the workflow. Never unrelated subjects.

## Expected Behavior

- After dispatching a background agent, Impetus immediately produces a response to the developer
- The response is on-topic: about the work just completed, the review being run, or what comes next
- Dead air (no response while background task runs) never occurs
- If substantive discussion is available, Impetus offers it rather than just acknowledging the wait
- Context switching to unrelated subjects does not happen during productive waiting

## NOT Expected

- Silence after dispatching a background agent
- Changing subject to something unrelated while waiting
- Only acknowledging the wait when substantive discussion is available
- Presenting unrelated information to "fill time"
