# What Doesn't Work When Providing Guidelines to AI Coding Agents (2026 Evidence)

## 1. The Curse of Instructions: More Rules = Worse Performance

The "Curse of Instructions" paper demonstrates that an LLM's ability to follow all instructions drops exponentially as instruction count rises: **P(all followed) = P(individual)^n**. A follow-up study using the IFScale benchmark found that even frontier models achieve only **68% accuracy at 500 instructions**. Instruction-level chain-of-thought improved GPT-4o from 15% to 31% for following ten simultaneous instructions, and Claude 3.5 Sonnet from 44% to 58%. Three degradation patterns were identified: threshold decay (reasoning models), linear decay (Claude Sonnet, GPT-4.1), and exponential decay (GPT-4o, Llama).

**Implication:** Every rule you add competes with every other rule. A 28-rule file is not 28x better than a 1-rule file — it is measurably worse at any individual rule.

Sources: [Curse of Instructions (OpenReview)](https://openreview.net/forum?id=R6q67CDBCH), [IFScale (arxiv)](https://arxiv.org/html/2507.11538v1)

## 2. LLM-Generated Context Files Make Agents Worse

The ETH Zurich AGENTbench study tested four AI agents across 138 real-world Python tasks:

- **LLM-generated AGENTS.md/context files decreased task success rate by 3%** and increased costs by 20%+
- **Human-written files improved success by only 4%** while increasing costs by 19%
- Agents followed context file instructions "religiously" — performing unnecessary testing, broad file exploration, and code-quality checks
- Architectural overviews and repo structure documentation did NOT reduce time locating files

**Recommendation:** omit LLM-generated context files entirely; limit human-written ones to **non-inferable details only**.

Sources: [InfoQ, March 2026](https://www.infoq.com/news/2026/03/agents-context-file-value-review/), [MarkTechPost](https://www.marktechpost.com/2026/02/25/new-eth-zurich-study-proves-your-ai-coding-agents-are-failing-because-your-agents-md-files-are-too-detailed/)

## 3. Context Rot: Longer Sessions Degrade Output Quality

Research from Chroma tested 18 LLMs:

- Performance degrades non-uniformly as input length grows
- **Claude models showed the largest gap** between focused (~300 token) and full (~113K token) prompts
- **Logically structured haystacks performed worse** than shuffled/randomized ones — models over-indexed on structure
- Distractors compound degradation non-uniformly

Practical thresholds: context rot becomes measurable around **20-30 turns**, accelerates beyond **40 turns**, and doubling task duration **quadruples failure rate**.

Sources: [Chroma Research](https://www.trychroma.com/research/context-rot), [MindStudio](https://www.mindstudio.ai/blog/context-rot-ai-coding-agents-explained)

## 4. Six Named Anti-Patterns That Waste Tokens

From BSWEN's analysis of real-world agent usage:

1. **The Kitchen Sink Session** — mixing requirements, architecture, code, debugging, and review in one conversation
2. **The Abstract Principle Dump** — "clean code," "DRY," "SOLID" without concrete examples
3. **Pushing Through Context Decay** — continuing past 80%+ context window fill
4. **The Mega-Session** — attempting all phases in one session
5. **Log Vomit** — pasting 2000+ lines when the error is in 50 lines
6. **The Verbal Repetition Loop** — restating constraints every session instead of persisting in rules files

Source: [BSWEN: AI Coding Anti-Patterns](https://docs.bswen.com/blog/2026-03-25-ai-coding-anti-patterns/)

## 5. Rules File Bloat: Most Rules Files Are Making Agents Worse

Analysis of dozens of agent rules files found a typical 28-rule file contained:

- **8 redundant rules** (duplicating tsconfig.json, package.json, etc.)
- **7 tooling enforcement rules** (belong in linters/CI)
- **3 essential rules** (actually change agent behavior)
- **10 helpful rules** (save time but agent could discover them)

After trimming to 11 rules, the file shrank 60% with every remaining line actually changing behavior. Three mechanisms of failure:

- **Token waste** — paying for irrelevant instruction parsing
- **Attention dilution** — "lost in the middle" effect buries essential rules
- **Context competition** — bloated rules displace actual code context

Source: [DEV Community](https://dev.to/alexefimenko/i-analyzed-a-lot-of-ai-agent-rules-files-most-are-making-your-agent-worse-2fl)

## 6. Specific Instruction Formats That Fail

**Vague instructions** — "Write clean code and follow best practices" gives infinite valid interpretations.

**Contradictory instructions** — "Use server components by default" + "Always wrap data fetching in useEffect hooks" are incompatible in Next.js.

**Copied style guides** — embedding complete style documentation in rules. Use linters instead.

**Stale content** — copying code examples into rules files rather than referencing files. The copied content becomes outdated.

**Documenting the obvious** — the agent already knows standard tools.

Sources: [Cursor Best Practices](https://cursor.com/blog/agent-best-practices), [Stack Overflow](https://stackoverflow.blog/2026/03/26/coding-guidelines-for-ai-agents-and-people-too/)

## 7. The "Lost in the Middle" Problem

LLM attention is not uniform across context. Information at the beginning and end has the most impact. Information in the middle is de-prioritized or ignored.

- **Critical rules buried in the middle of a long rules file get dropped.**
- Hidden context from tools and configurations pushes conversation into the low-attention middle zone.
- Solution: place critical rules early, keep files short.

Source: [DEV Community](https://dev.to/sachinchaurasiya/the-1-skill-most-developers-miss-when-using-ai-coding-agents-37h0)

## 8. CLAUDE.md Is Advisory, Not Deterministic

- CLAUDE.md is followed **approximately 80% of the time**. It is advisory, not deterministic.
- If something must happen every time, use **hooks** instead.
- Keep CLAUDE.md under **200 lines**. Beyond that, precision degrades.
- Do not treat it like documentation — it is a **context injection file**.
- Avoid instructions that apply to only some sessions.

Sources: [Anthropic Best Practices](https://code.claude.com/docs/en/best-practices), [Anthropic teams PDF](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)

## 9. Examples Help, But Architecture Overviews Don't

- **Concrete code examples showing preferred patterns work well.**
- **Reference files rather than copying content** — keeps rules fresh.
- **Architectural overviews and repo structure documentation do NOT help agents find files faster** (ETH Zurich).
- The most effective specs cover: executable commands, testing frameworks, project structure, code style examples, git workflow, boundary definitions.

Sources: [Addy Osmani](https://addyosmani.com/blog/good-spec/), [Builder.io](https://www.builder.io/blog/agents-md)

## 10. What Actually Works (The Inverse)

- **Explicit prohibitions over aspirational principles** — "Never use `as any`" outperforms "Write type-safe code"
- **Test suites as guardrails** — agents with runnable tests dramatically outperform agents without
- **Short sessions, single purpose** — one task per conversation, fresh context
- **Iterative rule addition** — start with 5, add one per week, prune monthly
- **Three-tier boundary system** — Always do / Ask first / Never do

Sources: [Cursor](https://cursor.com/blog/agent-best-practices), [Stack Overflow](https://stackoverflow.blog/2026/03/26/coding-guidelines-for-ai-agents-and-people-too/), [calv.info](https://calv.info/agents-feb-2026), [Medium](https://medium.com/@martin_50671/how-to-write-a-claude-md-that-actually-works-76a184042444)

## Sources

- [Curse of Instructions (OpenReview)](https://openreview.net/forum?id=R6q67CDBCH)
- [How Many Instructions Can LLMs Follow at Once? (arxiv)](https://arxiv.org/html/2507.11538v1)
- [AGENTS.md Value Reassessed (InfoQ, March 2026)](https://www.infoq.com/news/2026/03/agents-context-file-value-review/)
- [Context Rot Research (Chroma)](https://www.trychroma.com/research/context-rot)
- [Context Rot Explained (MindStudio)](https://www.mindstudio.ai/blog/context-rot-ai-coding-agents-explained)
- [AI Coding Anti-Patterns (BSWEN)](https://docs.bswen.com/blog/2026-03-25-ai-coding-anti-patterns/)
- [Rules Files Analysis (DEV Community)](https://dev.to/alexefimenko/i-analyzed-a-lot-of-ai-agent-rules-files-most-are-making-your-agent-worse-2fl)
- [Coding Guidelines for AI (Stack Overflow Blog)](https://stackoverflow.blog/2026/03/26/coding-guidelines-for-ai-agents-and-people-too/)
- [Agent Best Practices (Cursor)](https://cursor.com/blog/agent-best-practices)
- [Good Spec for AI Agents (Addy Osmani)](https://addyosmani.com/blog/good-spec/)
- [CLAUDE.md That Works (Medium)](https://medium.com/@martin_50671/how-to-write-a-claude-md-that-actually-works-76a184042444)
- [Anthropic Best Practices](https://code.claude.com/docs/en/best-practices)
- [Anthropic Teams PDF](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)
- [Coding Agents Feb 2026 (calv.info)](https://calv.info/agents-feb-2026)
- [Agents.md Guide (Builder.io)](https://www.builder.io/blog/agents-md)
- [Lost in the Middle (DEV Community)](https://dev.to/sachinchaurasiya/the-1-skill-most-developers-miss-when-using-ai-coding-agents-37h0)
- [Cursor Rules Best Practices (Medium)](https://medium.com/elementor-engineers/cursor-rules-best-practices-for-developers-16a438a4935c)
