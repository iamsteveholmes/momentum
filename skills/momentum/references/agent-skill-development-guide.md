# Agent & Skill Development Guide — Claude Code Conventions

## Agent Definition Files (`agents/*.md`)

### Frontmatter Schema
```yaml
---
name: agent-name                    # Required: kebab-case, max 64 chars
description: What + when to use     # Recommended: <250 chars, front-load use case
model: sonnet|haiku|opus            # Optional: model override
effort: low|medium|high|max         # Optional: effort level
maxTurns: N                         # Optional: max turns before stopping
tools: Read Grep Glob               # Optional: space-separated or YAML list
disallowedTools: Write Edit         # Optional: space-separated or YAML list
skills: [skill1, skill2]            # Optional: preload full skill content
---
```

### System Prompt Structure
1. Role statement ("You are...")
2. Scope/constraints ("You focus on...", "You do NOT...")
3. Key behaviors (step-by-step or principle-based)
4. Input format (what the agent receives when spawned)
5. Output format (structured output the orchestrator expects)

### Design Rules
- `description` is the trigger mechanism — Claude uses it to auto-invoke
- Keep description specific and action-oriented ("Security-focused code review. Use when...")
- System prompt (markdown body) is the agent's core instruction
- Agent definitions should be focused — a system prompt, not a full workflow

## SKILL.md Files (`skills/<skill-name>/SKILL.md`)

### Frontmatter Schema
```yaml
---
name: skill-name                    # Optional: defaults to directory name
description: What + when to use     # Recommended: <250 chars
model: haiku|sonnet|opus            # Optional: model override
effort: low|medium|high|max         # Optional: effort override
context: fork                       # Optional: isolated execution
allowed-tools: Read Grep Bash       # Optional: restrict tools
disable-model-invocation: false     # Optional: true = user-only
user-invocable: true                # Optional: false = Claude-only
---
```

### Invocation Control
| Config | User invokes | Claude invokes |
|--------|-------------|---------------|
| Default (neither set) | Yes | Yes |
| `disable-model-invocation: true` | Yes | No |
| `user-invocable: false` | No | Yes |

### Structure Rules
- SKILL.md body under 500 lines
- Detailed material goes in supporting files (reference.md, etc.)
- Use `context: fork` for isolated execution in a subagent

## References
- Subagents: https://code.claude.com/docs/en/sub-agents
- Skills: https://code.claude.com/docs/en/skills
- Plugin components: https://code.claude.com/docs/en/plugins-reference
