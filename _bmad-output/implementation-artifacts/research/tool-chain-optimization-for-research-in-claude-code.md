# Tool Chain Optimization for Research in Claude Code

**Date:** 2026-04-03
**Type:** Technical Research Report

---

## 1. WebSearch: Capabilities and Limitations

### Search Engine Backend

Claude Code's WebSearch tool is a server-side tool backed by Anthropic's search infrastructure. Internal analysis of the tool's architecture indicates the search backend is "likely powered by Brave Search" ([Quercle Blog](https://quercle.dev/blog/claude-code-web-tools)). The tool uses the `web_search_20250305` (basic) or `web_search_20260209` (with dynamic filtering) server tool versions ([Anthropic API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)).

### How It Works in Claude Code

Within Claude Code specifically, WebSearch operates through a secondary conversation architecture. The main conversation spawns a secondary conversation that calls the server-side `web_search` tool with up to 8 search uses. The secondary conversation processes results and returns approximately 10 links with titles and URLs, along with synthesized text blocks. Critically, Claude Code's WebSearch discards `page_age` and `encrypted_content` fields from results -- it extracts only `url` and `title` ([Mikhail Shilkov](https://mikhail.io/2025/10/claude-code-web-tools/)). This means the agent must explicitly call WebFetch for actual page content.

The secondary conversation enables extended thinking with a ~32K token budget for deeper analysis of results ([Quercle Blog](https://quercle.dev/blog/claude-code-web-tools)).

### Parameters and Filtering

The tool accepts:
- `query` (required): the search query string
- `allowed_domains` (optional): restrict results to specific domains
- `blocked_domains` (optional): exclude specific domains

The API-level tool also supports `max_uses` (limiting searches per request), `user_location` for localization, and domain filtering ([Anthropic API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)).

### Rate Limits and Pricing

WebSearch is priced at **$10 per 1,000 searches** on the API, plus standard token costs for search-generated content. Rate limits operate across three independent, overlapping constraints: requests per minute (RPM), tokens per minute (TPM), and daily quotas ([SitePoint](https://www.sitepoint.com/claude-code-rate-limits-explained/)). When rate limits are hit, the API returns a 200 response with a `too_many_requests` error code inside the response body, not an HTTP error ([Anthropic API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)). A reported bug indicates that WebSearch rate limit errors occur more frequently on Claude subscription plans than with direct API keys ([GitHub #27074](https://github.com/anthropics/claude-code/issues/27074)).

### Query Crafting for Research

The tool uses lexical matching. Effective queries should include specific terms, year references for recency, and quoted phrases for exact matches. Domain filtering via `allowed_domains` is valuable when researching specific documentation sites. The `web_search_20260209` version adds dynamic filtering with Opus 4.6 and Sonnet 4.6, where Claude can write and execute code to filter search results before they reach the context window -- particularly effective for technical documentation research and literature review ([Anthropic API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)).

### Cost in Claude Code

Estimated cost is approximately **$145 per 1,000 WebSearch calls** when the main conversation uses Opus, accounting for cache creation tokens and search overhead in the secondary conversation ([Quercle Blog](https://quercle.dev/blog/claude-code-web-tools)).

---

## 2. WebFetch: Behavior and Content Handling

### Architecture

WebFetch in Claude Code does **not** use Anthropic's server-side web fetch tool. Instead, it fetches pages locally using Axios from the user's machine IP address ([Quercle Blog](https://quercle.dev/blog/claude-code-web-tools), [Mikhail Shilkov](https://mikhail.io/2025/10/claude-code-web-tools/)). The processing pipeline is:

1. Main conversation initiates WebFetch with URL and a prompt
2. Domain validation via `domain_info` API endpoint checking deny-lists
3. Axios performs local HTTP request (max ~10 MB)
4. HTML is converted to Markdown using the Turndown library
5. Content is truncated to ~100 KB of text
6. A secondary conversation with **Claude Haiku 3.5** processes the content with a restrictive prompt enforcing a 125-character maximum for direct quotes
7. Haiku's summarized response becomes the tool result

This architecture means WebFetch returns a **processed summary**, not raw content. The Haiku intermediary acts as both a cost-reduction measure and a security gate ([Mikhail Shilkov](https://mikhail.io/2025/10/claude-code-web-tools/)).

### Content Type Support

**HTML**: Converted to Markdown via Turndown. Approximately 80 documentation domains (github.com, docs.python.org, react.dev, etc.) use simplified processing prompts ([Quercle Blog](https://quercle.dev/blog/claude-code-web-tools)).

**PDFs**: The server-side web fetch tool supports PDFs, returning base64-encoded content with automatic text extraction ([Anthropic API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)). Claude Code's local WebFetch handles PDFs through the same Axios pipeline.

**JavaScript-rendered content**: **Not supported.** WebFetch retrieves raw HTML without executing JavaScript. SPAs and dynamically-generated content return empty or skeleton markup ([Firecrawl comparison](https://www.firecrawl.dev/blog/claude-web-fetch-vs-firecrawl), [GitHub #4597](https://github.com/anthropics/claude-code/issues/4597)).

**Paywalled/authenticated sites**: **Not supported.** WebFetch cannot fill forms, manage cookies, or authenticate. Only publicly accessible URLs work ([AgentPatch](https://agentpatch.ai/blog/claude-code-web-scraping-guide/)).

### Size Limits and Caching

- Maximum fetch size: ~10 MB at fetch time
- Content truncated to ~100 KB of text after conversion
- 15-minute cache TTL per URL (900,000 ms), reducing redundant fetches
- The API-level tool supports `max_content_tokens` to limit context consumption; typical token usage: average web page (~10 KB) = ~2,500 tokens, large documentation page (~100 KB) = ~25,000 tokens, research paper PDF (~500 KB) = ~125,000 tokens ([Anthropic API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool))

### URL Restrictions

Claude Code WebFetch can only fetch URLs that have previously appeared in the conversation context -- user messages, tool results, or previous search/fetch results. It cannot fetch arbitrary URLs that Claude generates ([Anthropic API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)).

### Redirect Handling

Same-host redirects are followed automatically. Cross-host redirects return instructions for manual follow-up requests -- the tool informs you of the redirect URL and you must make a new WebFetch request ([Quercle Blog](https://quercle.dev/blog/claude-code-web-tools)).

### Cost

Estimated at **~$33 per 1,000 requests** for large documents based on Haiku token pricing ([Quercle Blog](https://quercle.dev/blog/claude-code-web-tools)). The server-side API web fetch tool has **no additional charges** beyond standard token costs ([Anthropic API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)).

---

## 3. Grep and Glob for Codebase Research

### Grep (Ripgrep-Based)

Claude Code's Grep tool is powered by ripgrep (`rg`), not GNU grep. By default it uses a bundled version via `@vscode/ripgrep` npm package ([Quercle Blog, AI Free API](https://www.aifreeapi.com/en/posts/claude-code-tool-search)).

**Key parameters:**
- `pattern`: Full regex syntax (ripgrep flavor, not PCRE)
- `path`: File or directory scope (defaults to CWD)
- `output_mode`: `"files_with_matches"` (default, paths only), `"content"` (matching lines), `"count"` (match counts)
- Context flags: `-A` (after), `-B` (before), `-C` (context) -- only with `content` mode
- `-i`: Case-insensitive search
- `-n`: Show line numbers (default true in content mode)
- `multiline`: Enable cross-line pattern matching
- `head_limit`: Restrict result quantity (defaults to 250)
- `glob`: Filter files by pattern (e.g., `"*.ts"`)
- `type`: Filter by file type (e.g., `"js"`, `"py"`)

**Pattern syntax note:** Literal braces must be escaped as `\{` and `\}` -- e.g., `interface\{\}` to find `interface{}` in Go code ([vtrivedy](https://www.vtrivedy.com/posts/claudecode-tools-reference)).

**Output mode strategy:**
- `files_with_matches`: Discovery phase -- where does this pattern appear?
- `count`: Quantification -- how widespread is usage?
- `content` with context: Understanding -- what surrounds the match? ([AI Free API](https://www.aifreeapi.com/en/posts/claude-code-tool-search))

Ripgrep respects `.gitignore` by default and skips binary files, providing natural scope control ([BuildMVPFast](https://www.buildmvpfast.com/blog/ripgrep-10-years-fast-cli-tools-ai-agents-2026)).

### Glob

Glob performs fast file pattern matching using file system indexing. Key behaviors:
- Supports recursive patterns: `**/*.js`, `src/**/*.ts`
- Multi-extension matching: `*.{json,yaml}`
- **Returns results sorted by modification time** -- most recently modified files appear first
- Works efficiently regardless of codebase size
- Faster than `find` or `ls` via Bash ([vtrivedy](https://www.vtrivedy.com/posts/claudecode-tools-reference), [AI Free API](https://www.aifreeapi.com/en/posts/claude-code-tool-search))

**When to use which:**
- Glob: You know the file naming pattern but not the location
- Grep: You know what is inside the file but not which file

---

## 4. Read Tool for Deep Analysis

### Capabilities

The Read tool supports multiple file types:
- **Text files**: Returns content with `cat -n` format (line numbers starting at 1)
- **Images** (PNG, JPG, etc.): Displayed visually -- Claude is multimodal and can analyze image content
- **PDFs**: Supports page-range reading via `pages` parameter (e.g., `"1-5"`). Large PDFs (10+ pages) **require** the `pages` parameter. Maximum 20 pages per request
- **Jupyter notebooks** (.ipynb): Returns all cells with their outputs, combining code, text, and visualizations
- Lines exceeding 2000 characters are truncated ([vtrivedy](https://www.vtrivedy.com/posts/claudecode-tools-reference), [Claude Code Docs](https://code.claude.com/docs/en/tools-reference))

### Line Range Parameters

- `offset`: Starting line number (0-indexed)
- `limit`: Number of lines to read (default: up to 2000 lines from file start)

**Best practice:** When you already know which part of a file you need, read only that part using `offset` and `limit`. This reduces context consumption significantly -- "read only relevant portions rather than loading entire files" ([AI Free API](https://www.aifreeapi.com/en/posts/claude-code-tool-search)).

### Research Strategy

For large files, use a two-phase approach:
1. Use Grep to find line numbers of interest
2. Use Read with `offset` and `limit` to examine specific sections

This pattern avoids loading entire files into context, which is critical since "a single debugging session or codebase exploration might generate and consume tens of thousands of tokens" ([Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)).

---

## 5. Tool Chaining Patterns for Research

### WebSearch to WebFetch Pipeline

The canonical web research pattern:
1. **WebSearch** to find relevant URLs and get an overview
2. **WebFetch** on the most promising URLs to get detailed content
3. Synthesize findings from multiple fetched pages

This is explicitly documented as a "combined search and fetch" workflow where "Claude will use web search to find relevant articles, select the most promising results, use web fetch to retrieve full content, and provide detailed analysis with citations" ([Anthropic API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)).

### Codebase Exploration Pipeline

Effective patterns for codebase research:

1. **Discovery flow**: Glob (find entry points) -> Read (examine configurations) -> Grep (explore subsystems)
2. **Error debugging flow**: Grep (locate error pattern) -> Read (examine context) -> Glob (find related files)
3. **Refactoring assessment**: Grep `count` mode (quantify usage) -> `files_with_matches` (see distribution) -> `content` with context (identify definitions) ([AI Free API](https://www.aifreeapi.com/en/posts/claude-code-tool-search))

### Subagent Delegation for Research

The official best practices recommend using subagents for investigation tasks: "Delegate research with 'use subagents to investigate X'. They explore in a separate context, keeping your main conversation clean for implementation" ([Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)).

Subagents are particularly valuable for research because they run in separate context windows. When researching a codebase, the agent reads many files that consume context. Subagents report back summaries without cluttering the main conversation.

### Skill Chaining

Skills can invoke other skills, creating multi-step workflows. The key pattern is compatible input/output contracts where "one skill's output naturally feeds into the next" ([MindStudio](https://www.mindstudio.ai/blog/claude-code-skill-collaboration-pattern)). For research workflows, structured JSON works best as an intermediate format between chained steps ([MindStudio](https://www.mindstudio.ai/blog/claude-code-skill-collaboration-chaining-workflows)).

---

## 6. Failure Modes and Workarounds

### WebFetch Failures

**Hanging/timeout**: WebFetch can enter a "Fetching..." state and never return with no timeout or error. The entire agent chain hangs, requiring cancellation and context loss ([GitHub #11650](https://github.com/anthropics/claude-code/issues/11650), [GitHub #8980](https://github.com/anthropics/claude-code/issues/8980)).

**Domain blocking**: Many external documentation sites return 403 Forbidden errors. Protected sites explicitly refuse automated access ([GitHub #8331](https://github.com/anthropics/claude-code/issues/8331)).

**Connection failures**: "fetch failed" and "connection timed out" errors with "no more retries left" messages despite failures occurring on initial attempt ([GitHub #8698](https://github.com/anthropics/claude-code/issues/8698)).

**Workarounds:**
- For JavaScript-rendered sites: Use Bash to write and execute Playwright scripts for actual browser control ([MindStudio Playwright guide](https://www.mindstudio.ai/blog/browser-automation-claude-code-playwright))
- For corporate proxy issues: Set `NODE_EXTRA_CA_CERTS` to the corporate CA certificate bundle ([Claude Code Troubleshooting](https://code.claude.com/docs/en/troubleshooting))
- For persistent failures: Fall back to `curl` via Bash tool, or use an MCP-provided web fetch tool if available
- For large/complex sites: Use Firecrawl or Bright Data MCP servers for managed scraping infrastructure ([Medium - Yaron Been](https://medium.com/@yaron.been/my-data-extraction-stack-with-claude-code-a-practical-guide-from-simple-webfetch-to-bright-datas-6b19cc683399))

### WebSearch Quality Issues

- Results may be overly lexical -- exact keyword matching rather than semantic understanding
- WebSearch is unavailable on Bedrock/Vertex platforms ([Mikhail Shilkov](https://mikhail.io/2025/10/claude-code-web-tools/))
- Rate limit errors can be opaque since the API returns 200 with an error inside the body

### Context Window Exhaustion

The most fundamental failure mode: "LLM performance degrades as context fills" and Claude "may start 'forgetting' earlier instructions or making more mistakes" ([Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)). Research tasks are especially prone to this since they involve reading many files and fetching web content.

**Mitigation:** Use `/clear` between unrelated research phases, delegate exploration to subagents, and use Read with `offset`/`limit` instead of reading entire files.

---

## 7. Bash Tool for Research

### When to Use Bash

The Bash tool makes "every CLI tool on your system immediately available" with zero setup ([SysPrompt](https://systemprompt.io/guides/mcp-vs-cli-tools)). It is appropriate for research in these cases:

- **Stateless operations**: `curl`, `git log`, `git diff`, file reads that are inherently one-shot
- **Ad-hoc exploration**: One-off investigations using `curl | jq` pipelines that change every time
- **Git history analysis**: `git log`, `git blame`, `git show` for understanding code evolution
- **Simple text output**: Commands producing a few lines of predictable format

### When to Prefer Dedicated Tools

The Bash tool system prompt explicitly states: "Avoid using this tool to run find, grep, cat, head, tail, sed, awk, or echo commands" when dedicated tools can accomplish the task. The dedicated tools "provide a much better experience" ([Claude Code Docs](https://code.claude.com/docs/en/tools-reference)).

| Task | Use | Avoid |
|------|-----|-------|
| File name matching | Glob | `find`, `ls` via Bash |
| Content searching | Grep | `grep`, `rg` via Bash |
| File reading | Read | `cat`, `head`, `tail` via Bash |
| File editing | Edit | `sed`, `awk` via Bash |

### Bash for Research-Specific Tasks

Bash excels for research tasks that dedicated tools cannot handle:
- `git log --all --oneline --graph` for repository history visualization
- `curl -s <api_endpoint> | jq '.data[]'` for API exploration
- `wc -l`, `sort`, `uniq -c` for statistical analysis of codebase patterns
- `docker logs`, `kubectl logs` for runtime investigation
- Running project-specific CLI tools: `gh`, `aws`, `sentry-cli`, etc. ([Claude Code Best Practices](https://code.claude.com/docs/en/best-practices))

The rule of thumb: "When a bash pattern stabilizes (same command, same parsing, used more than 3 times per week), evaluate whether to promote it to an MCP tool" ([SysPrompt](https://systemprompt.io/guides/mcp-vs-cli-tools)).

---

## 8. Tool Selection Decision Framework

### Primary Decision Tree

```
Research Task
  |
  +-- Need external/web information?
  |     +-- Need search results? --> WebSearch
  |     +-- Have a specific URL? --> WebFetch
  |     +-- URL fails/needs JS? --> Bash (curl, Playwright)
  |
  +-- Need codebase information?
  |     +-- Know the filename pattern? --> Glob
  |     +-- Know what's inside the file? --> Grep
  |     +-- Know the exact file and location? --> Read
  |     +-- Need git history? --> Bash (git log, git blame)
  |     +-- Need type/symbol info? --> LSP tool
  |
  +-- Need multi-step investigation?
  |     +-- Will consume lots of context? --> Agent (subagent)
  |     +-- Simple pipeline? --> Chain tools directly
  |
  +-- Need structured data from APIs?
        +-- One-off query? --> Bash (curl | jq)
        +-- Repeated pattern? --> MCP server
```

### Output Mode Selection for Grep

| Goal | Output Mode | Use Case |
|------|------------|----------|
| Where does X appear? | `files_with_matches` | Initial discovery |
| How widespread is X? | `count` | Impact assessment |
| What does X look like in context? | `content` with `-C` | Deep understanding |

### Context Budget Awareness

Every tool call consumes context. The framework should prioritize:
1. **Start specific, then broaden** -- targeted searches before expanding scope ([AI Free API](https://www.aifreeapi.com/en/posts/claude-code-tool-search))
2. **Use file type filters** (`type: "ts"`) to narrow searches and reduce false positives
3. **Delegate exploration to subagents** to keep main conversation context clean ([Claude Code Best Practices](https://code.claude.com/docs/en/best-practices))
4. **Read partial files** with offset/limit instead of full files
5. **Use `/clear` between phases** of research to reset context

---

## 9. Gaps and Limitations

### WebFetch Fundamental Limitations

- **No JavaScript rendering**: SPAs, React docs, and dynamically-generated pages fail. This is a fundamental architectural limitation of the Axios-based local fetch approach. The workaround (Playwright via Bash) is heavyweight and requires browser installation.
- **Haiku summarization bottleneck**: The 125-character quote limit and Haiku intermediary mean WebFetch can lose important details. "Summary may omit relevant details; conservative quoting approach prioritizes safety over completeness" ([Mikhail Shilkov](https://mikhail.io/2025/10/claude-code-web-tools/)).
- **No authentication support**: No cookies, sessions, or credentials -- a large portion of the web (enterprise docs, internal wikis, authenticated APIs) is inaccessible.

### WebSearch Limitations

- **Lexical matching bias**: Queries work best with exact keywords, not natural language questions.
- **Platform restrictions**: Unavailable on Bedrock/Vertex.
- **US-only availability**: Web search is noted as "only available in the US" in the tool schema.
- **Opaque rate limiting**: Errors embedded inside 200 responses are easy to miss programmatically.

### Grep Limitations

- **Not semantic**: Ripgrep finds text patterns, not code meaning. For semantic code search (e.g., "find all async functions that don't have error handling"), ast-grep is needed but is not a built-in tool ([ast-grep docs](https://ast-grep.github.io/advanced/prompting.html)).
- **No cross-file relationship tracking**: Cannot follow import chains, call graphs, or type hierarchies. The LSP tool handles some of this but requires plugin installation.

### Context Window as the Fundamental Constraint

The single most impactful limitation for research is context window exhaustion. Research tasks inherently involve reading lots of content, and "LLM performance degrades as context fills." There is no way to selectively unload information from context mid-conversation -- the only options are `/clear` (losing everything), `/compact` (lossy summarization), or subagent delegation (which has its own context limits) ([Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)).

### Missing Capabilities for Research

- **No persistent knowledge base**: Research findings from one session cannot be automatically carried to the next beyond what fits in CLAUDE.md or manual notes.
- **No structured citation management**: WebSearch returns URLs but there is no built-in way to track, deduplicate, or organize references across a research session.
- **No differential fetch**: Cannot check if a page has changed since last fetch (beyond the 15-minute cache TTL).
- **No concurrent web requests**: WebSearch and WebFetch execute sequentially. Parallel fetching of multiple URLs would significantly speed up research workflows.

---

## Sources

- [Web search tool - Anthropic API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)
- [Web fetch tool - Anthropic API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)
- [Tools reference - Claude Code Docs](https://code.claude.com/docs/en/tools-reference)
- [Best Practices - Claude Code Docs](https://code.claude.com/docs/en/best-practices)
- [How Claude Code Web Tools Work - Quercle Blog](https://quercle.dev/blog/claude-code-web-tools)
- [Inside Claude Code's Web Tools: WebFetch vs WebSearch - Mikhail Shilkov](https://mikhail.io/2025/10/claude-code-web-tools/)
- [Claude Code Built-in Tools Reference - vtrivedy](https://www.vtrivedy.com/posts/claudecode-tools-reference)
- [Claude Code Tool Search Explained - AI Free API](https://www.aifreeapi.com/en/posts/claude-code-tool-search)
- [Claude Code Rate Limits Explained - SitePoint](https://www.sitepoint.com/claude-code-rate-limits-explained/)
- [MCP Servers vs CLI Tools - SysPrompt](https://systemprompt.io/guides/mcp-vs-cli-tools)
- [WebSearch Rate Limit Bug - GitHub #27074](https://github.com/anthropics/claude-code/issues/27074)
- [WebFetch Hanging Bug - GitHub #11650](https://github.com/anthropics/claude-code/issues/11650)
- [WebFetch Domain Access Bug - GitHub #8331](https://github.com/anthropics/claude-code/issues/8331)
- [WebFetch Timeout Bug - GitHub #8980](https://github.com/anthropics/claude-code/issues/8980)
- [Connection Timeout Bug - GitHub #8698](https://github.com/anthropics/claude-code/issues/8698)
- [JS Rendering Bug - GitHub #4597](https://github.com/anthropics/claude-code/issues/4597)
- [Firecrawl vs Claude Web Fetch](https://www.firecrawl.dev/blog/claude-web-fetch-vs-firecrawl)
- [Claude Code Web Scraping Guide - AgentPatch](https://agentpatch.ai/blog/claude-code-web-scraping-guide/)
- [Data Extraction with Claude Code - Medium/Yaron Been](https://medium.com/@yaron.been/my-data-extraction-stack-with-claude-code-a-practical-guide-from-simple-webfetch-to-bright-datas-6b19cc683399)
- [Browser Automation with Claude Code - MindStudio](https://www.mindstudio.ai/blog/browser-automation-claude-code-playwright)
- [Skill Collaboration Pattern - MindStudio](https://www.mindstudio.ai/blog/claude-code-skill-collaboration-pattern)
- [Chaining Skills Into Workflows - MindStudio](https://www.mindstudio.ai/blog/claude-code-skill-collaboration-chaining-workflows)
- [Ripgrep at 10 Years - BuildMVPFast](https://www.buildmvpfast.com/blog/ripgrep-10-years-fast-cli-tools-ai-agents-2026)
- [ast-grep Prompting Guide](https://ast-grep.github.io/advanced/prompting.html)
- [Claude Code Troubleshooting](https://code.claude.com/docs/en/troubleshooting)
