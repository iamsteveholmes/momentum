---
content_origin: claude-code-subagent
date: 2026-04-04
sub_question: "What IDE-level capabilities does Air expose to agents that CLI-based tools like Claude Code lack?"
topic: "JetBrains Air"
---

## Executive Summary

JetBrains Air exposes a substantial set of IDE-level capabilities to agents through two complementary mechanisms: (1) its own built-in LSP-backed code intelligence layer providing navigation, symbol resolution, and language-aware features directly in the Air UI, and (2) the IntelliJ MCP Server (integrated since IDE version 2025.2), which surfaces ~25 tools including semantic symbol info, context-aware refactoring, code inspections, run configuration execution, and database access. A third-party Debugger MCP plugin adds 22 more tools for programmatic debugger control. CLI-based tools like Claude Code lack access to all of these capabilities natively -- they operate on raw file text without project model awareness, cannot invoke IDE inspections, and have no structured access to debuggers, run configurations, or semantic symbol resolution.

## Air's Built-In Code Intelligence

### LSP-Backed Language Support

Air uses Language Server Protocol servers to provide code intelligence for supported languages. This is a significant architectural choice -- rather than building proprietary language engines, Air delegates to battle-tested LSP implementations ([JetBrains Air Language Support docs](https://www.jetbrains.com/help/air/supported-languages.html)) **[OFFICIAL]**:

| Language | LSP Server |
|---|---|
| Kotlin | Kotlin Analyzer |
| Go | gopls |
| Rust | rust-analyzer |
| Python | basedpyright |
| C/C++/CUDA | clangd |
| TypeScript/JavaScript | TypeScript language server |
| HTML | VS Code HTML LSP |
| CSS | VS Code CSS LSP |
| Svelte | svelte-language-server |

For these languages, Air provides full code intelligence including:

- **Code completion** -- single-line and block completion
- **Semantic highlighting** -- language-aware syntax coloring beyond regex-based TextMate grammars
- **Quick-fixes** -- automated resolution of common code issues
- **Rename refactoring** -- structural rename across the project
- **Code formatting** -- language-aware formatting

Over 50 additional languages receive TextMate-based syntax highlighting only (no intelligence). Notably, **Java receives only syntax highlighting** despite being a flagship JetBrains language -- full LSP support is marked as "not supported yet." **[OFFICIAL]**

### Navigation Features Exposed in Air

Air's editor provides structured code navigation that agents (and humans) can leverage when reviewing or directing work ([Air Explore Code docs](https://www.jetbrains.com/help/air/explore-projects.html)) **[OFFICIAL]**:

- **Go to Definition** -- jump to symbol declaration
- **Find Usages** -- locate all references to a symbol across the codebase
- **Go to Implementations** -- navigate to all implementations of an interface or abstract method
- **Go to Type Definition** -- access type information for a symbol
- **Go to Problems** -- sequential navigation through code errors and warnings
- **Go to All** -- unified search across files, symbols, actions, tools, and text

These features are **language-dependent** -- they require full LSP support for the target language. For unsupported languages, only basic text search and file browsing are available.

### What CLI Tools Lack Here

Claude Code and similar CLI-based agents navigate codebases using file reads, grep/ripgrep, and AST-level heuristics (when available). They have no access to:

- **Structural symbol resolution** -- CLI tools cannot resolve "what is the type of this variable" or "where is this interface implemented" without parsing the code themselves or relying on the LLM's training-time understanding
- **Cross-file usage tracking** -- finding all usages of a symbol requires text search with manual disambiguation, rather than a language server's indexed semantic graph
- **Language-aware quick-fixes** -- CLI tools can suggest fixes via LLM reasoning, but cannot invoke deterministic IDE inspections

## The IntelliJ MCP Server: IDE Tools Exposed to Agents

Starting with version 2025.2, all JetBrains IDEs include a built-in MCP (Model Context Protocol) server. This server exposes IDE capabilities as structured tools that any MCP-compatible agent can invoke. Air can pass both user-configured MCP servers and the integrated IntelliJ MCP server to installed agents ([JetBrains ACP docs](https://www.jetbrains.com/help/ai-assistant/acp.html)) **[OFFICIAL]**.

The IntelliJ MCP Server provides approximately 25 tools across several categories ([IntelliJ IDEA MCP Server docs](https://www.jetbrains.com/help/idea/mcp-server.html), [Rider MCP Server docs](https://www.jetbrains.com/help/rider/mcp-server.html)) **[OFFICIAL]**:

### Symbol Resolution and Code Analysis

- **`get_symbol_info`** -- Retrieves information about the symbol at a specified position in a file, including name, signature, type, documentation, and declaration snippet. Equivalent to the IDE's Quick Documentation feature. This is a *semantic* operation -- it understands the code's type system, not just text patterns.
- **`get_file_problems`** -- Analyzes a file for errors and warnings using IntelliJ's inspection engine. Returns severity, description, and location. This gives agents access to the same static analysis that powers the IDE's error highlighting -- hundreds of inspections across languages.

### Context-Aware Refactoring

- **`rename_refactoring`** -- Renames a symbol (variable, function, class) with full structural awareness. Unlike text search-and-replace, this tool understands scope, shadowing, and cross-file references. It updates all usages consistently.
- **`reformat_file`** -- Applies the IDE's configured code formatting rules to a file.

### File and Project Navigation

- **`get_file_text_by_path`** -- Retrieves file content with configurable truncation
- **`get_all_open_file_paths`** -- Returns paths of currently open editor files
- **`list_directory_tree`** -- Tree representation of directories
- **`find_files_by_glob`** -- Recursive glob pattern search
- **`find_files_by_name_keyword`** -- Indexed file name search (faster than glob for name matching)
- **`create_new_file`** -- Creates files with optional content
- **`open_file_in_editor`** -- Opens a file in the IDE editor

### Search

- **`search_in_files_by_text`** -- Full-text search using IntelliJ's search engine
- **`search_in_files_by_regex`** -- Regex pattern search across project files

### Text Modification

- **`replace_text_in_file`** -- Find-and-replace with flexible matching options

### Project Model

- **`get_project_modules`** -- Lists all modules with their types (source, test, resource, etc.)
- **`get_project_dependencies`** -- Retrieves all library dependencies defined in the project
- **`get_run_configurations`** -- Lists available run/debug configurations
- **`get_repositories`** -- Identifies VCS roots in multi-repository projects

### Execution

- **`execute_run_configuration`** -- Runs a specific run configuration and returns exit code, output, and success status
- **`execute_terminal_command`** -- Executes shell commands in the IDE's integrated terminal

### Database Access

A full suite of database tools is available for projects with configured data sources:

- **`list_database_connections`**, **`test_database_connection`** -- Connection management
- **`list_database_schemas`**, **`list_schema_object_kinds`**, **`list_schema_objects`** -- Schema exploration
- **`execute_sql_query`**, **`preview_table_data`** -- Query execution
- **`list_recent_sql_queries`**, **`cancel_sql_query`** -- Query management

### What This Means for Agents

An agent running inside Air (or a JetBrains IDE via ACP) can call `get_symbol_info` to understand what a variable is, call `get_file_problems` to check if its edits introduced errors, use `rename_refactoring` for safe structural renames, and run tests via `execute_run_configuration` -- all through structured tool calls with typed responses. A CLI-based agent like Claude Code must approximate all of these through file reads, text manipulation, and shell commands, without the deterministic guarantees of the IDE's language engine.

## Debugger Integration: The Debugger MCP Plugin

The built-in IntelliJ MCP server does **not** include debugger tools. However, a community-developed plugin -- **Debugger MCP Server** -- fills this gap with 22 additional tools ([GitHub: jetbrains-debugger-mcp-plugin](https://github.com/hechtcarmel/jetbrains-debugger-mcp-plugin)) **[PRAC]**:

### Breakpoint Management
- **`list_breakpoints`** -- Display all breakpoints with optional filtering
- **`set_breakpoint`** -- Create line breakpoints with conditions, log messages, and suspend policies
- **`remove_breakpoint`** -- Delete breakpoints by ID or location

### Execution Control
- **`resume_execution`**, **`pause_execution`** -- Continue or halt execution
- **`step_over`**, **`step_into`**, **`step_out`** -- Standard stepping operations
- **`run_to_line`** -- Continue to a specific line

### State Inspection
- **`get_variables`** -- Access all variables in the current stack frame
- **`set_variable`** -- Modify variable values during debugging
- **`evaluate_expression`** -- Execute arbitrary expressions in debug context
- **`get_stack_trace`** -- Retrieve call stack with file, line, and method info
- **`select_stack_frame`** -- Switch debugger context
- **`list_threads`** -- Display all threads with state

### Session Management
- **`list_debug_sessions`**, **`start_debug_session`**, **`stop_debug_session`** -- Lifecycle management
- **`get_debug_session_status`** -- Comprehensive status including variables, stack, and source
- **`list_run_configurations`**, **`execute_run_configuration`** -- Configuration access
- **`get_source_context`** -- Source code surrounding execution point

The plugin is tested on IntelliJ IDEA, PyCharm, WebStorm, GoLand, RustRover, Android Studio, and PhpStorm. **[PRAC]**

### The CLI Gap

CLI-based tools like Claude Code have **zero structured debugger access**. They can invoke a debugger via shell commands (e.g., `gdb`, `lldb`, `node --inspect`), but this requires parsing unstructured text output. The MCP debugger plugin provides typed, structured tool calls that return machine-readable data -- a qualitative difference for agent reliability.

## The Agent Client Protocol (ACP): The Connectivity Layer

ACP is the open protocol that connects agents to IDEs. Built by JetBrains and Zed, it standardizes how coding agents communicate with development environments -- analogous to LSP for language servers, but for AI agents ([JetBrains ACP page](https://www.jetbrains.com/acp/)) **[OFFICIAL]**.

Key architectural points:

- **ACP wraps MCP** -- the IntelliJ MCP server tools described above are surfaced to agents through the ACP channel. ACP configuration can selectively restrict which MCP tools an agent can access via the `idea_mcp_allowed_tools` key.
- **Agent Registry** -- the ACP Agent Registry (launched January 2026) is a curated directory of ACP-compatible agents integrated into JetBrains IDEs and Zed ([ACP Registry blog post](https://blog.jetbrains.com/ai/2026/01/acp-agent-registry/)) **[OFFICIAL]**.
- **Vendor-neutral** -- ACP is designed for interoperability. Cursor joined the ACP Registry in March 2026 ([Cursor ACP blog](https://blog.jetbrains.com/ai/2026/03/cursor-joined-the-acp-registry-and-is-now-live-in-your-jetbrains-ide/)) **[OFFICIAL]**.

CLI tools like Claude Code use MCP directly (connecting to MCP servers configured in the environment) but do not participate in the ACP protocol. This means they cannot receive IDE-provided context (symbol mentions, file selections, project model data) through the structured ACP channel.

## Air's Orchestration Capabilities (Beyond Code Intelligence)

Several Air capabilities represent architectural advantages over CLI tools that go beyond pure code intelligence:

### Multi-Agent Task Isolation

Air runs agents in isolated environments -- Docker containers or Git worktrees -- enabling concurrent task execution without file conflicts. CLI agents operate in a shared working directory; concurrent agent instances would conflict on file writes ([Air launch blog](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/)) **[OFFICIAL]**.

### Contextual Symbol Mentions in Task Definitions

When defining tasks in Air, users can `@`-mention specific symbols (classes, methods, commits, lines) from the project. The agent receives these as resolved references with precise context, rather than requiring the agent to search for and identify the relevant code ([Air Quick Start docs](https://www.jetbrains.com/help/air/quick-start-with-air.html)) **[OFFICIAL]**.

### Diff Review in Codebase Context

Air presents agent-generated changes as diffs within the context of the entire codebase, with gutter-based commenting linked to the agent's chat session. This enables line-by-line review with iterative refinement requests. CLI tools produce diffs that must be reviewed in external tools or with `git diff` ([Air Review docs](https://www.jetbrains.com/help/air/review-and-integrate.html)) **[OFFICIAL]**.

### Built-In Terminal, Git, and Preview

Air integrates terminal, Git client, and live preview into the agent workspace. Agents and users share the same environment context, reducing the disconnect between agent actions and human review **[OFFICIAL]**.

## JetBrains Central: The Coming Semantic Layer

JetBrains Central, announced March 2026 with early access planned for Q2 2026, aims to build "a semantic layer that continuously aggregates and structures information from code, architecture, runtime behavior, and organizational knowledge" ([JetBrains Central announcement](https://blog.jetbrains.com/blog/2026/03/24/introducing-jetbrains-central-an-open-system-for-agentic-software-development/)) **[OFFICIAL]**.

Central adds three enterprise-level capabilities:

1. **Governance and control** -- policy enforcement, identity management, auditability, cost attribution
2. **Agent execution infrastructure** -- cloud runtimes for agent operation
3. **Agent optimization and context** -- shared semantic understanding across codebases, intelligent task routing

This represents a future state where agents operate with organizational-level context (architecture decisions, production behavior, team conventions) that is fundamentally unavailable to any current CLI tool. Central is not yet generally available. **[OFFICIAL]**

## Comparative Summary: Air+IDE vs. Claude Code CLI

| Capability | Air / JetBrains IDE | Claude Code CLI |
|---|---|---|
| **Symbol resolution** | `get_symbol_info` -- typed, semantic, language-aware | LLM inference from file content; no deterministic resolution |
| **Find usages** | IDE-indexed cross-project usage graph | `grep`/`ripgrep` text search with manual disambiguation |
| **Rename refactoring** | `rename_refactoring` -- scope-aware, cross-file | LLM-guided text replacement; no structural guarantee |
| **Code inspections** | `get_file_problems` -- hundreds of IDE inspections | Linters via shell (if configured); no unified inspection API |
| **Debugger control** | 22-tool MCP plugin: breakpoints, stepping, variables, eval | Shell-based debugger invocation; unstructured text output |
| **Run configurations** | `execute_run_configuration` -- named, typed, IDE-managed | Shell commands (`npm test`, `go test`, etc.) |
| **Project model** | `get_project_modules`, `get_project_dependencies` | File system traversal; parse `package.json`/`build.gradle` manually |
| **Database access** | Full SQL tool suite (9 tools) | Shell-based `psql`/`mysql` if available |
| **Multi-agent isolation** | Docker containers, Git worktrees, concurrent tasks | Single working directory; no built-in isolation |
| **Task context** | `@`-mentions resolve to symbols, commits, lines | User pastes text or describes locations |
| **Diff review** | Integrated editor with gutter comments, codebase context | `git diff` in terminal; external review tools |
| **Code completion** | LSP-backed, language-aware | Not applicable (CLI agents don't complete interactively) |
| **Language coverage** | 9 languages with full intelligence; 50+ with syntax only | Language-agnostic text processing (no intelligence layer) |

## Key Limitations and Caveats

1. **Language coverage gaps** -- Air's full intelligence covers only 9 languages. Java, C#, PHP, Ruby, and many others get syntax highlighting only. Claude Code's LLM-based approach is language-agnostic, which can be an advantage for polyglot projects. **[OFFICIAL]**

2. **Air is macOS-only in preview** -- Windows and Linux support is planned but not yet available. **[OFFICIAL]**

3. **Debugger MCP is community-maintained** -- The Debugger MCP Server plugin is not an official JetBrains product. It fills a real gap, but its maintenance and compatibility are not guaranteed. **[PRAC]**

4. **MCP tool access requires IDE** -- The IntelliJ MCP server tools are only available when a JetBrains IDE is running. CLI tools work anywhere without an IDE dependency.

5. **Claude Code can access JetBrains MCP** -- Claude Code supports MCP server connections, so it can theoretically connect to the IntelliJ MCP server when an IDE is running. The gap is that Claude Code does not *natively* include these capabilities and requires external setup.

6. **Air does not replace the IDE** -- Air explicitly positions itself as complementary: "Air handles the agent-powered development; your IDE handles the rest." Deep refactoring features like Extract Method, Inline Variable, and Change Signature remain in the traditional IDE, not exposed to agents via MCP (only Rename is exposed). **[OFFICIAL]**

## Sources

- [JetBrains Air - Official site](https://air.dev/)
- [Air Quick Start documentation](https://www.jetbrains.com/help/air/quick-start-with-air.html)
- [Air Language Support](https://www.jetbrains.com/help/air/supported-languages.html)
- [Air Explore Code (navigation features)](https://www.jetbrains.com/help/air/explore-projects.html)
- [Air Review and Integrate](https://www.jetbrains.com/help/air/review-and-integrate.html)
- [Air Launch Blog Post (March 2026)](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/)
- [Agent Client Protocol (ACP) - Official page](https://www.jetbrains.com/acp/)
- [ACP documentation for AI Assistant](https://www.jetbrains.com/help/ai-assistant/acp.html)
- [ACP Agent Registry announcement (January 2026)](https://blog.jetbrains.com/ai/2026/01/acp-agent-registry/)
- [Cursor joins ACP Registry (March 2026)](https://blog.jetbrains.com/ai/2026/03/cursor-joined-the-acp-registry-and-is-now-live-in-your-jetbrains-ide/)
- [IntelliJ IDEA MCP Server documentation](https://www.jetbrains.com/help/idea/mcp-server.html)
- [Rider MCP Server documentation](https://www.jetbrains.com/help/rider/mcp-server.html)
- [JetBrains Debugger MCP Plugin (GitHub)](https://github.com/hechtcarmel/jetbrains-debugger-mcp-plugin)
- [JetBrains Central announcement (March 2026)](https://blog.jetbrains.com/blog/2026/03/24/introducing-jetbrains-central-an-open-system-for-agentic-software-development/)
- [Bring your own AI agent to JetBrains IDEs (December 2025)](https://blog.jetbrains.com/ai/2025/12/bring-your-own-ai-agent-to-jetbrains-ides/)
- [Junie documentation](https://junie.jetbrains.com/docs/)
