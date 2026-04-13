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

### File Modification Safety

After any Write or Edit to a file, re-Read it before making another Write or Edit to the same file. The PostToolUse lint/format hook rewrites files after every modification — your cached read becomes stale immediately, and a subsequent Write without re-reading will fail with a "file modified since read" error.

### Large File Handling (Required Convention)

Every agent definition MUST include a `## Large File Handling` section in its system
prompt body. This is a standard convention — not optional. Sprint retro analysis found
that 33.6% of all tool errors were `file_too_large` errors caused by agents attempting
full reads of large files without offset/limit.

The standard section content (keep it under 20 lines):

```markdown
## Large File Handling

Some project files exceed the Read tool's token limit (10,000 tokens). When you
encounter a file-too-large error or need to read a file known to be large, use
these strategies:

1. **Search before reading** — Use Grep to find the specific section, heading, or
   keyword you need. Note the line number from Grep output, then Read with offset
   and limit targeting that area.
2. **Read in chunks** — Use `offset` and `limit` parameters: `offset=0, limit=200`
   for the first 200 lines, then adjust as needed.
3. **Known large files** — These commonly exceed limits: architecture.md, prd.md,
   epics.md, stories/index.json, and JSONL audit extracts. Never attempt a full
   read of these files.
4. **On error, narrow scope** — If a Read fails with a token-limit error, do not
   retry the same read. Instead, Grep for what you need and read only that section.
```

Placement: after the agent's process/behavior sections, before the output format
section. Only reference tools available to the agent (Read and Grep are in every
agent's tool list and are appropriate for all agents — read-only or read-write).

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
