# Claude Code Guideline Mechanisms: Research (April 2026)

## 1. CLAUDE.md Files: Format, Loading, and Behavior

**No required format.** Anthropic's official documentation states plainly: "There is no required format." The recommendation is to keep the file concise and human-readable, using markdown headers and bullets to group related instructions. ([Official docs: Memory](https://code.claude.com/docs/en/memory), [Blog: Using CLAUDE.md files](https://claude.com/blog/using-claude-md-files))

**Loading behavior.** CLAUDE.md is delivered as a **user message after the system prompt**, not as part of the system prompt itself. Claude Code walks up the directory tree from the current working directory, checking each directory for `CLAUDE.md` and `CLAUDE.local.md` files. All discovered files are **concatenated into context** (not overriding each other). Within each directory, `CLAUDE.local.md` is appended after `CLAUDE.md`. ([Official docs: Memory](https://code.claude.com/docs/en/memory))

**Subdirectory files load lazily.** CLAUDE.md files in subdirectories below the working directory are **not loaded at launch**; they are included on demand when Claude reads files in those subdirectories. Files in ancestor directories above CWD are loaded in full at launch. ([Official docs: Memory](https://code.claude.com/docs/en/memory))

**HTML comments are stripped.** Block-level HTML comments are removed before injection into context, saving tokens. Comments inside code blocks are preserved. ([Official docs: Memory](https://code.claude.com/docs/en/memory))

**Survives compaction.** CLAUDE.md fully survives `/compact`. After compaction, Claude re-reads CLAUDE.md from disk and re-injects it fresh. This is the only content guaranteed to survive compaction. ([Official docs: Memory](https://code.claude.com/docs/en/memory))

**Import syntax.** Use `@path/to/file` to include other files. Relative paths resolve relative to the containing file. Maximum recursion depth: **5 hops**. Both relative and absolute paths work. ([Official docs: Memory](https://code.claude.com/docs/en/memory))

**AGENTS.md compatibility.** Claude Code reads CLAUDE.md, not AGENTS.md. If you have an AGENTS.md, create a CLAUDE.md that imports it with `@AGENTS.md`. ([Official docs: Memory](https://code.claude.com/docs/en/memory))

## 2. Full Loading Hierarchy (Priority Order)

Files load from broadest to most specific scope. **Later-loaded files have higher effective priority** because they are the last thing Claude reads at each level.

| Priority (low to high) | Location | Scope | Can be excluded? |
|---|---|---|---|
| 1 (lowest) | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) or `/etc/claude-code/CLAUDE.md` (Linux) | Managed policy (IT/DevOps) | **No** |
| 2 | `~/.claude/CLAUDE.md` | Personal global | Yes |
| 3 | `~/.claude/rules/*.md` | Personal global rules | Yes |
| 4 | Ancestor `CLAUDE.md` files (root down to CWD) | Project hierarchy | Yes, via `claudeMdExcludes` |
| 5 | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Project instructions | Yes |
| 6 | `./.claude/rules/*.md` (no `paths` frontmatter) | Project rules (unconditional) | Yes |
| 7 | `./CLAUDE.local.md` | Personal project-local | Yes |
| 8 (highest) | `.claude/rules/*.md` with matching `paths:` | Conditional project rules | Yes |

([Official docs: Memory](https://code.claude.com/docs/en/memory), [ClaudeFast: Rules Directory](https://claudefa.st/blog/guide/mechanics/rules-directory))

User-level rules (`~/.claude/rules/`) load **before** project rules, giving project rules higher effective priority. ([Official docs: Memory](https://code.claude.com/docs/en/memory))

## 3. `.claude/rules/` Directory Mechanics

**Automatic recursive discovery.** Every `.md` file in `.claude/rules/` is discovered recursively. No configuration needed. Subdirectories are fully supported for organizational purposes. ([Official docs: Memory](https://code.claude.com/docs/en/memory), [ClaudeFast: Rules Directory](https://claudefa.st/blog/guide/mechanics/rules-directory))

**Unconditional rules** (no `paths` frontmatter) load at launch with the same priority as `.claude/CLAUDE.md`. ([Official docs: Memory](https://code.claude.com/docs/en/memory))

**Path-scoped rules** use YAML frontmatter with glob patterns:

```yaml
---
paths:
  - "src/api/**/*.ts"
  - "lib/**/*.{ts,tsx}"
---
```

These rules trigger **when Claude reads files matching the pattern**, not on every tool use. ([Official docs: Memory](https://code.claude.com/docs/en/memory))

**Symlinks supported.** The directory supports symlinks for sharing rules across projects. Circular symlinks are detected gracefully. ([Official docs: Memory](https://code.claude.com/docs/en/memory))

**Best practice: one concern per file** with descriptive filenames like `testing.md` or `api-design.md`. ([Official docs: Memory](https://code.claude.com/docs/en/memory), [Medium: Rick Hightower](https://medium.com/@richardhightower/claude-code-rules-stop-stuffing-everything-into-one-claude-md-0b3732bca433))

## 4. Size Limits and Recommendations

**Official recommendation: target under 200 lines per CLAUDE.md file.** "Longer files consume more context and reduce adherence." If growing large, split using `@` imports or `.claude/rules/` files. ([Official docs: Memory](https://code.claude.com/docs/en/memory))

**Community benchmarks suggest even shorter.** HumanLayer reports their root CLAUDE.md is under 60 lines. ([HumanLayer Blog](https://www.humanlayer.dev/blog/writing-a-good-claude-md))

**The "priority saturation" problem.** When a single CLAUDE.md exceeds ~400 lines, all instructions compete for attention and effectiveness degrades sharply. ([Medium: Rick Hightower](https://medium.com/@richardhightower/claude-code-rules-stop-stuffing-everything-into-one-claude-md-0b3732bca433))

**Auto memory limit.** MEMORY.md loads only the first **200 lines or 25KB** (whichever comes first). CLAUDE.md files load in full regardless of length, but shorter files produce better adherence. ([Official docs: Memory](https://code.claude.com/docs/en/memory))

## 5. Context Window Budget Impact

**Baseline system prompt overhead: ~14,000-14,300 tokens.** This is a constant tax on every API call, including internal instructions, tool definitions, and safety guidelines. ([DEV.to: Token Tracing](https://dev.to/slima4/where-do-your-claude-code-tokens-actually-go-we-traced-every-single-one-423e))

**MCP server overhead: 5,000-10,000 tokens per 20-tool server.** Each MCP server loads its complete tool schema on every request, on top of the system prompt. ([DEV.to: Token Tracing](https://dev.to/slima4/where-do-your-claude-code-tokens-actually-go-we-traced-every-single-one-423e))

**Total pre-conversation overhead: 30,000-40,000 tokens** including system prompt, tools, MCP schemas, and memory files. ([MorphLLM: CLAUDE.md Examples](https://www.morphllm.com/claude-md-examples))

**Effective instruction budget: ~100-150 distinct instructions.** Research suggests frontier LLMs follow ~150-200 distinct instructions reliably; Claude Code's built-in system prompt already consumes ~50, leaving you 100-150. ([MorphLLM: CLAUDE.md Examples](https://www.morphllm.com/claude-md-examples))

**Prompt caching.** CLAUDE.md content benefits from Anthropic's prompt caching, served at 90% cheaper token cost on subsequent turns within a session. ([DEV.to: Token Tracing](https://dev.to/slima4/where-do-your-claude-code-tokens-actually-go-we-traced-every-single-one-423e))

**Context window sizes:**
- Default: 200K tokens
- With 1M context (Max/Team/Enterprise + Opus 4.6): 1M tokens
- Auto-compaction triggers at 64-75% capacity
- Performance degradation observed around 147K-152K tokens on 200K window

([ClaudeFast: 1M Context](https://claudefa.st/blog/guide/mechanics/1m-context-ga))

## 6. What to Include vs. Exclude

| Include | Exclude |
|---|---|
| Bash commands Claude cannot guess | Anything Claude can infer from reading code |
| Code style rules that differ from defaults | Standard language conventions Claude already knows |
| Testing instructions and preferred test runners | Detailed API documentation (link instead) |
| Repository etiquette (branch naming, PR conventions) | Information that changes frequently |
| Architectural decisions specific to your project | Long explanations or tutorials |
| Developer environment quirks (required env vars) | File-by-file descriptions of the codebase |
| Common gotchas or non-obvious behaviors | Self-evident practices like "write clean code" |

([Official docs: Best Practices](https://code.claude.com/docs/en/best-practices))

**The pruning test:** "For each line, ask: Would removing this cause Claude to make mistakes? If not, cut it." ([Official docs: Best Practices](https://code.claude.com/docs/en/best-practices))

**Emphasis markers work.** Adding "IMPORTANT" or "YOU MUST" improves adherence for critical rules. ([Official docs: Best Practices](https://code.claude.com/docs/en/best-practices))

## 7. CLAUDE.md vs. Hooks vs. Skills

| Mechanism | Enforcement | When loaded | Use for |
|---|---|---|---|
| CLAUDE.md | Advisory (~80% adherence) | Every session, always in context | Broad project conventions |
| `.claude/rules/` | Advisory (same as CLAUDE.md, but scoped) | Every session or on file match | Domain-specific rules |
| Hooks | Deterministic (100%) | Triggered by specific events | Must-happen actions (lint, format, security) |
| Skills | On-demand | When invoked or auto-detected | Reusable workflows, domain knowledge |

([Official docs: Best Practices](https://code.claude.com/docs/en/best-practices), [Official docs: Memory](https://code.claude.com/docs/en/memory))

## 8. Debugging and Observability

- **`/memory` command** lists all loaded CLAUDE.md, CLAUDE.local.md, and rules files in the current session. ([Official docs: Memory](https://code.claude.com/docs/en/memory))
- **`InstructionsLoaded` hook** fires when any CLAUDE.md or rules file is loaded, providing `file_path`, `memory_type`, and `load_reason`. ([Official docs: Hooks](https://code.claude.com/docs/en/hooks))
- **`claudeMdExcludes` setting** in `.claude/settings.local.json` skips irrelevant files by glob pattern. ([Official docs: Memory](https://code.claude.com/docs/en/memory))

## Sources

- [Official: How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [Official: Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [Official: Hooks reference](https://code.claude.com/docs/en/hooks)
- [Anthropic Blog: Using CLAUDE.md files](https://claude.com/blog/using-claude-md-files)
- [ClaudeFast: Rules Directory](https://claudefa.st/blog/guide/mechanics/rules-directory)
- [ClaudeFast: 1M Context Window](https://claudefa.st/blog/guide/mechanics/1m-context-ga)
- [Medium: Stop Stuffing Everything into One CLAUDE.md](https://medium.com/@richardhightower/claude-code-rules-stop-stuffing-everything-into-one-claude-md-0b3732bca433)
- [HumanLayer: Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [DEV.to: Where Do Your Claude Code Tokens Actually Go](https://dev.to/slima4/where-do-your-claude-code-tokens-actually-go-we-traced-every-single-one-423e)
- [MorphLLM: CLAUDE.md Examples and Best Practices 2026](https://www.morphllm.com/claude-md-examples)
- [Builder.io: How to Write a Good CLAUDE.md File](https://www.builder.io/blog/claude-md-guide)
- [How Anthropic teams use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)
