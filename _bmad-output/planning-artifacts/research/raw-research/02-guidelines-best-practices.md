# Best Practices for Writing Effective AI Coding Agent Instructions (2026)

## 1. The Instruction Budget Is Real and Finite

The single most important finding across sources: **frontier LLMs follow approximately 150-200 instructions before compliance degrades**, and this degradation is **uniform** -- adding one low-value rule dilutes compliance probability across ALL rules equally, not just the new one ([HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md), [ShareUHack](https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026)).

For Claude Code specifically, the system prompt already consumes ~50 of those instruction slots, leaving **100-150 slots for your rules**. Anthropic's own best practices page states: "Bloated CLAUDE.md files cause Claude to ignore your actual instructions" ([Anthropic Best Practices](https://code.claude.com/docs/en/best-practices)).

The litmus test for every line: **"Would removing this cause Claude to make mistakes?"** If not, cut it.

## 2. What to Include vs. Exclude

**Include:**
- Bash commands Claude cannot guess (build, test, deploy)
- Code style rules that **differ from defaults** (not standard conventions)
- Testing instructions and preferred runners
- Repository etiquette (branch naming, PR conventions)
- Architectural decisions specific to the project
- Developer environment quirks (required env vars)
- Common gotchas or non-obvious behaviors

**Exclude:**
- Anything Claude can figure out by reading code
- Standard language conventions Claude already knows
- Detailed API documentation (link to docs instead)
- Information that changes frequently
- Long explanations or tutorials
- File-by-file codebase descriptions
- Self-evident practices like "write clean code"

Sources: [Anthropic Best Practices](https://code.claude.com/docs/en/best-practices), [HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md), [Ran Isenberg](https://ranthebuilder.cloud/blog/claude-code-best-practices-lessons-from-real-projects/)

## 3. Structure and Priority Ordering

**Put critical rules first.** AI models apply more attention to content at the beginning and end of a document. The recommended ordering is:

1. Project brief (one paragraph: what it is, tech stack, scale)
2. Critical constraints (NEVER/ALWAYS rules)
3. Tech stack with exact versions
4. Key commands (build, test, lint)
5. Code style conventions
6. File structure
7. Error handling patterns
8. Testing expectations
9. Secondary preferences

Source: [Agent Rules Builder](https://www.agentrulegen.com/guides/how-to-write-ai-coding-rules)

**Use emphatic language for non-negotiables.** ALL-CAPS "NEVER" and "ALWAYS" phrasing, plus markers like "IMPORTANT" and "YOU MUST", meaningfully improve rule adherence in practice ([Agent Rules Builder](https://www.agentrulegen.com/guides/how-to-write-ai-coding-rules), [Anthropic Best Practices](https://code.claude.com/docs/en/best-practices)).

**Use mandatory "must" over advisory "should."** The word "must" produces measurably better compliance than softer phrasing ([tedivm](https://blog.tedivm.com/guides/2026/03/beyond-the-vibes-coding-assistants-and-agents/)).

## 4. Progressive Disclosure Over Monolithic Files

The consensus best practice is a **layered architecture** rather than one massive file:

- **Root CLAUDE.md**: under 200 lines (ideally under 60), only universally-applicable rules
- **Subdirectory CLAUDE.md files**: lazy-loaded when Claude accesses those directories
- **`.claude/rules/` files**: on-demand rule loading
- **Skills (`.claude/skills/`)**: domain knowledge loaded only when relevant
- **Referenced docs**: "When working with the payment system, first read docs/payment-architecture.md" -- Claude reads only when needed

This keeps the instruction budget free for high-priority rules. HumanLayer's own production CLAUDE.md is under 60 lines ([HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)).

Do NOT inline code snippets -- they become outdated quickly. Use `file:line` references to point Claude to authoritative source ([HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md)).

## 5. The AGENTbench Research: Context Files Can Hurt

The ETH Zurich AGENTbench study (January 2026) tested 138 real-world Python tasks across four AI agents and found:

- **LLM-generated context files reduced success rate by 3%** and increased costs by over 20%
- **Human-written context files improved success rate by only 4%** while increasing costs up to 19%
- Architectural overviews and repo structure explanations **did not reduce time spent locating files** -- agents performed unnecessary testing, file reading, and code-quality checks
- Agents followed instructions too thoroughly, doing extra work that didn't improve outcomes

A separate study using OpenAI's Codex found the opposite on efficiency: **28% reduction in wall-clock time** and **16-20% reduction in output tokens** when AGENTS.md was present. The reconciliation: context files help with **efficiency** (speed, tokens) but provide only marginal gains on **effectiveness** (correctness).

**The research recommendation**: Limit human-written instructions to **non-inferable details only** -- specific tooling, custom build commands, and things the agent genuinely cannot derive from reading the code.

Sources: [InfoQ](https://www.infoq.com/news/2026/03/agents-context-file-value-review/), [MarkTechPost](https://www.marktechpost.com/2026/02/25/new-eth-zurich-study-proves-your-ai-coding-agents-are-failing-because-your-agents-md-files-are-too-detailed/)

## 6. Negative Instructions and Counterexamples

Explicitly state what NOT to do. Every AI model has fallback patterns it uses when not told otherwise. Effective negative instructions include specific alternatives:

- "Never use `useEffect` for data fetching -- use `useSWR` instead"
- "Never use `any` type -- use `unknown` and narrow"
- "Do not use `console.log` in production code -- use the logger from `src/lib/logger`"

A single good code example conveys more than paragraphs of prose. Provide one clean example per convention ([Agent Rules Builder](https://www.agentrulegen.com/guides/how-to-write-ai-coding-rules)).

## 7. Declare Exact Versions

"AI models contain knowledge of multiple incompatible versions of the same library. Without version pins, they guess -- and guess inconsistently." Include parenthetical notes answering follow-up questions: `React 18.3 (not 19 -- do not use React 19 APIs like use())` ([Agent Rules Builder](https://www.agentrulegen.com/guides/how-to-write-ai-coding-rules)).

## 8. Hooks for Deterministic Enforcement, Instructions for Judgment

| Mechanism | Nature | Use For |
|---|---|---|
| Linter/CI | Static, deterministic | Formatting, syntax, style |
| Hooks | Mechanical enforcement (shell scripts) | Objectively determinable rules |
| CLAUDE.md | Advisory, ~80% compliance | Architectural intent, business logic, judgment calls |

"CLAUDE.md is advisory and Claude follows it about 80% of the time. Hooks are deterministic, 100%." ([Anthropic Best Practices](https://code.claude.com/docs/en/best-practices), [ShareUHack](https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026))

## 9. XML Tags vs. Markdown for Structure

For Claude specifically, XML tags create **unambiguous boundaries** and Claude was specifically trained to parse them. However, XML consumes ~15% more tokens than equivalent Markdown. The practical recommendation: use Markdown headers for human-readable structure in CLAUDE.md files, and XML tags when constructing programmatic prompts or system-level instructions ([Anthropic docs](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags), [Algorithm Unmasked](https://algorithmunmasked.com/2025/05/14/mastering-claude-prompts-xml-vs-markdown-formatting-for-optimal-results/)).

## 10. Specification-Driven Development

The emerging 2026 consensus is that **the spec is the most important artifact**, not the instructions file. Addy Osmani's workflow and the GitHub spec-kit approach both emphasize:

- Write a real markdown spec before coding (goals, acceptance criteria, technical constraints, implementation notes)
- Break specs into focused sections rather than presenting everything at once
- Use three-tier boundaries: Always do / Ask first / Never do
- Start fresh sessions for implementation (clean context focused on execution)
- A focused 20-minute session with clear instructions outperforms a sprawling 2-hour session

Sources: [Addy Osmani](https://addyosmani.com/blog/ai-coding-workflow/), [GitHub Blog](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-using-markdown-as-a-programming-language-when-building-with-ai/)

## 11. The Mental Model

The most effective framing: write instructions as if briefing **an incredibly capable engineer who has read every programming book but has never seen your project**. They know all the patterns but don't know which ones you've chosen, why, or which tradeoffs you've already resolved ([Agent Rules Builder](https://www.agentrulegen.com/guides/how-to-write-ai-coding-rules)).

## 12. Iterate Based on Corrections

Treat repeated AI mistakes as feedback. "Your rules file should grow every time you correct the AI for the same mistake twice." But also prune: mature projects tend to streamline their rules to focus on essential guidelines rather than expanding them indefinitely ([Agent Rules Builder](https://www.agentrulegen.com/guides/how-to-write-ai-coding-rules), [InfoQ/AGENTbench](https://www.infoq.com/news/2026/03/agents-context-file-value-review/)).

## 13. Diagnostic When Rules Are Ignored

If Claude ignores a rule from CLAUDE.md, paste it directly into the conversation. If Claude follows it there but not from CLAUDE.md, the problem is delivery-layer (file too long, rule buried, relevance judgment). If Claude still ignores it, the rule itself needs rewriting to be more specific ([ShareUHack](https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026)).

## Key Quantitative Benchmarks

| Metric | Value | Source |
|---|---|---|
| Frontier LLM instruction ceiling | 150-200 instructions | HumanLayer |
| Claude Code system prompt consumption | ~50 instruction slots | HumanLayer |
| Available user instruction slots | 100-150 | HumanLayer |
| CLAUDE.md advisory compliance rate | ~80% | Anthropic |
| Hook compliance rate | 100% (deterministic) | Anthropic |
| LLM-generated context file impact on success | -3% | ETH Zurich AGENTbench |
| Human-written context file impact on success | +4% | ETH Zurich AGENTbench |
| Context file impact on agent costs | +19-20% | ETH Zurich AGENTbench |
| AGENTS.md wall-clock time reduction (Codex) | -28% | arxiv study |
| AGENTS.md token reduction (Codex) | -16 to -20% | arxiv study |
| Recommended CLAUDE.md length | Under 200 lines (ideally <60) | HumanLayer, Ran Isenberg |
