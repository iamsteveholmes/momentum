# Anti-Patterns

Common patterns to avoid in agentic engineering workflows.

## Tool Management

- **Suggesting nvm/fnm/volta/pyenv/rbenv/asdf when mise is available.** mise is the primary tool/runtime manager. Never suggest legacy single-purpose version managers. See the mise rule for the full policy.

## Verification Before Asking

- **Asking the user to confirm factual states that available tools can verify directly.** Before asking the user about a fact (file existence, current config, repo state, etc.), check whether a tool can confirm it. Read, Grep, Glob, Bash, and git commands can resolve most factual questions without user involvement. Ask only when no tool can verify it. This rule does not apply to questions requiring user judgment, decisions, or preferences — those always go to the user.

## Communication

- **Euphemizing failure.** When work didn't achieve its goal, name it plainly — "rewrite", "failed", "did not work" — rather than softening with "iteration", "pivot", "evolved", or similar. Recognizing failure is valuable; obscuring it erodes trust and prevents learning.
