---
research_date: 2026-03-30
agent_focus: JetBrains AI tooling and MCP integration for Compose Multiplatform
sources_consulted:
  - https://www.jetbrains.com/help/idea/mcp-server.html
  - https://github.com/JetBrains/mcp-jetbrains
  - https://github.com/JetBrains/mcp-server-plugin
  - https://blog.jetbrains.com/idea/2025/05/intellij-idea-2025-1-model-context-protocol/
  - https://www.jetbrains.com/help/ai-assistant/mcp.html
  - https://www.jetbrains.com/help/ai-assistant/acp.html
  - https://www.jetbrains.com/help/ai-assistant/settings-reference-providers-and-api-keys.html
  - https://medium.com/@mirzemehdi/how-to-get-the-most-out-of-junie-in-a-kotlin-multiplatform-project-3ce67d235e0a
  - https://blog.jetbrains.com/ai/2025/12/bring-your-own-ai-agent-to-jetbrains-ides/
  - https://blog.jetbrains.com/fleet/2025/12/the-future-of-fleet/
  - https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/
  - https://www.jetbrains.com/help/air/quick-start-with-air.html
  - https://junie.jetbrains.com/docs/junie-cli.html
  - https://junie.jetbrains.com/docs/junie-headless.html
  - https://blog.jetbrains.com/junie/2026/03/junie-cli-the-llm-agnostic-coding-agent-is-now-in-beta/
  - https://github.com/JetBrains/junie
  - https://blog.jetbrains.com/kotlin/2025/05/kotlinconf-2025-language-features-ai-powered-development-and-kotlin-multiplatform/
  - https://blog.jetbrains.com/kotlin/2025/09/the-kotlin-ai-stack-build-ai-agents-with-koog-code-smarter-with-junie-and-more/
  - https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/
  - https://blog.jetbrains.com/kotlin/2025/08/kmp-roadmap-aug-2025/
  - https://kotlinlang.org/docs/multiplatform/whats-new-compose-110.html
  - https://blog.jetbrains.com/ai/2025/09/introducing-claude-agent-in-jetbrains-ides/
  - https://code.claude.com/docs/en/jetbrains
  - https://github.com/Daghis/teamcity-mcp
  - https://developer.android.com/studio/gemini/add-mcp-server
  - https://android-developers.googleblog.com/2025/06/agentic-ai-takes-gemini-in-android-studio-to-next-level.html
  - https://github.com/JetBrains/koog/
search_queries_used:
  - "JetBrains MCP server Model Context Protocol 2025 2026"
  - "JetBrains AI Assistant API CLI external access 2025"
  - "JetBrains Fleet discontinued status 2025 2026"
  - "IntelliJ HTTP API remote control automation 2025"
  - "KotlinConf 2025 AI Compose Multiplatform announcements keynote"
  - "Compose Multiplatform 2025 release versions tooling testing"
  - "JetBrains mcp-jetbrains GitHub tools list operations exposed"
  - "JetBrains Air agentic IDE 2026 preview headless"
  - "JetBrains Junie agent headless CLI compose multiplatform 2025 2026"
  - "Android Studio Gemini MCP server API external access 2025"
  - "JetBrains Koog Kotlin AI agent framework 2025 MCP"
  - "third party MCP server IntelliJ JetBrains community GitHub 2025"
  - "TeamCity MCP server JetBrains CI build trigger 2025"
  - "Claude Code JetBrains MCP integration setup guide 2025"
  - "Compose Multiplatform 1.9 release 2026 testing preview tooling"
  - "JetBrains gradle build headless CI Compose Multiplatform test results 2025"
  - "JetBrains Compose Multiplatform hot reload stable gradle plugin CLI 2025 2026"
  - "IntelliJ IDEA built-in web server HTTP API automation headless 2025"
  - "JetBrains IDE remote control plugin HTTP API builds tests 2025"
last_verified: 2026-03-30
---

# A3: JetBrains AI Tooling and MCP Integration
## Research Date: March 30, 2026

## Executive Summary

The JetBrains tooling landscape has transformed substantially since 2025. As of March 2026, Claude Code has **four viable integration paths** with JetBrains tooling, with one path being officially first-class:

1. **Built-in IntelliJ MCP Server (since 2025.2)** — Claude Code is explicitly listed as a supported MCP client and can be auto-configured from within IntelliJ IDEA. The IDE must be running, but the connection gives Claude Code 25+ IDE tools including build execution, code analysis, terminal commands, and file operations. This is the highest-value path. [Source: https://www.jetbrains.com/help/idea/mcp-server.html, accessed 2026-03-30]

2. **Junie CLI headless mode (beta, March 2026)** — A standalone JetBrains coding agent that runs from the terminal with no IDE required, supports CI/CD, and is LLM-agnostic (including Anthropic). Claude Code can shell out to Junie CLI as a subprocess. This is useful for delegating JetBrains-specific code generation and analysis tasks. [Source: https://blog.jetbrains.com/junie/2026/03/junie-cli-the-llm-agnostic-coding-agent-is-now-in-beta/, accessed 2026-03-30]

3. **TeamCity MCP Server (community, active)** — A community-built MCP server for JetBrains TeamCity CI that Claude Code can connect to directly using `claude mcp add teamcity`. Enables triggering builds and retrieving test results without any IDE running. [Source: https://github.com/Daghis/teamcity-mcp, accessed 2026-03-30]

4. **Pure Gradle Headless (baseline fallback)** — No JetBrains tooling required. Claude Code can invoke Gradle directly (`./gradlew build`, `./gradlew desktopTest`) for build and test on JVM targets. This is the recommended path for CI environments and Docker containers where no IDE is available.

**Fleet is dead** (discontinued December 22, 2025). JetBrains Central (public preview March 24, 2026) is Fleet's spiritual successor but has no headless API. Gradle-based CLI testing remains the cleanest headless build/test path for Compose Multiplatform.

---

## JetBrains MCP Server

### Background: From Plugin to Built-in

JetBrains shipped MCP support in two phases:

- **IntelliJ IDEA 2025.1** (released May 2025): Added MCP *client* support — the IDE's AI Assistant could consume tools from external MCP servers. [Source: https://blog.jetbrains.com/idea/2025/05/intellij-idea-2025-1-model-context-protocol/, accessed 2026-03-30]
- **IntelliJ IDEA 2025.2** (mid-2025): Added a built-in MCP *server* — external clients including Claude Code can now use the IDE as a tool provider. The separate `mcp-jetbrains` npm package and `mcp-server-plugin` GitHub repository are both deprecated and unmaintained as of 2025.2. [Source: https://github.com/JetBrains/mcp-jetbrains, accessed 2026-03-30]

### What the MCP Server Exposes

The built-in MCP server exposes 25+ tools across five categories [Source: https://www.jetbrains.com/help/idea/mcp-server.html, accessed 2026-03-30]:

**Project & Configuration**
- `get_run_configurations` — list all run configurations in the project
- `execute_run_configuration` — run a named configuration and return exit code, output, and success status
- `get_project_dependencies` — list all project dependencies
- `get_project_modules` — list all project modules
- `get_repositories` — list VCS repository connections

**File Operations**
- `create_new_file`, `get_file_text_by_path`, `replace_text_in_file`
- `find_files_by_glob`, `find_files_by_name_keyword`
- `open_file_in_editor`, `reformat_file`
- `list_directory_tree`, `get_all_open_file_paths`

**Code Analysis & Refactoring**
- `get_file_problems` — run IntelliJ inspections on a file; returns severity, description, location
- `get_symbol_info` — retrieve symbol documentation
- `rename_refactoring` — context-aware rename that updates all references
- `search_in_files_by_regex`, `search_in_files_by_text`

**Terminal & Execution**
- `execute_terminal_command` — run a shell command in the IDE's terminal; output capped at 2000 lines

**Database** (read-only access recommended)
- Connection management, schema browsing, query execution, table preview

### GUI Requirement

The MCP server is **integrated into the IDE**; the IDE must be running for it to serve requests. There is no headless/server mode that runs independently of the GUI. This is the key limitation: it requires an active IntelliJ IDEA (or Android Studio) instance with the project open.

### Claude Code Auto-Configuration

Claude Code is explicitly listed as a supported client. Setup is performed from within IntelliJ IDEA at `Settings | Tools | MCP Server → Enable MCP Server → Auto-Configure → Claude Code`. This updates Claude Code's MCP configuration automatically. The connection supports both SSE and Stdio transports. [Source: https://www.jetbrains.com/help/idea/mcp-server.html, accessed 2026-03-30]

There is also a "brave mode" setting that allows terminal commands and run configuration execution without per-operation confirmation prompts. [Source: https://www.jetbrains.com/help/idea/mcp-server.html, accessed 2026-03-30]

### Assessment for Agent Use

| Criterion | Status |
|---|---|
| (a) Status as of March 2026 | Shipped and active; built-in since 2025.2 |
| (b) Usable without IDE GUI | No — IDE must be running |
| (c) Claude Code can connect | Yes — officially supported and auto-configurable |
| (d) Setup complexity | Low — one-click auto-configure from IDE settings |

**Confidence:** High — Multiple primary sources, official JetBrains documentation, confirmed as shipped feature.

---

## JetBrains AI Assistant (2025-2026)

### Current Capabilities (as of March 2026)

JetBrains AI Assistant has evolved substantially in 2025:

- **Junie** (the agentic component): Handles multi-step tasks across Kotlin server, Android, and Kotlin Multiplatform projects. Introduced as IDE plugin at KotlinConf 2025 (May 2025), with IDE plugin Early Access in mid-2025. [Source: https://blog.jetbrains.com/kotlin/2025/05/kotlinconf-2025-language-features-ai-powered-development-and-kotlin-multiplatform/, accessed 2026-03-30]
- **Claude Agent** (September 2025): JetBrains integrated an Anthropic Claude-powered agent directly into the JetBrains AI chat, available under the JetBrains AI subscription at no extra charge. It runs via the JetBrains MCP server and supports plan mode, multi-file diffs, and approval-based operations. [Source: https://blog.jetbrains.com/ai/2025/09/introducing-claude-agent-in-jetbrains-ides/, accessed 2026-03-30]
- **Agent Client Protocol (ACP)** (fully live as of 25.3, December 2025): An open standard co-developed by JetBrains and Zed that allows any ACP-compatible agent (Junie, Auggie, goose, Kimi CLI) to be plugged into JetBrains IDEs. Claude Code is not listed as a natively supported ACP agent, but can connect headlessly via `acp.json` configuration. [Source: https://www.jetbrains.com/help/ai-assistant/acp.html, accessed 2026-03-30]
- **Third-party models**: AI Assistant supports BYOK (bring your own key) for Anthropic, OpenAI, Google, and other OpenAI-compatible endpoints. [Source: https://www.jetbrains.com/help/ai-assistant/settings-reference-providers-and-api-keys.html, accessed 2026-03-30]
- **Mellum**: JetBrains' in-house LLM open-sourced at KotlinConf 2025, fine-tuned for Kotlin code completion. [Source: https://blog.jetbrains.com/kotlin/2025/05/kotlinconf-2025-language-features-ai-powered-development-and-kotlin-multiplatform/, accessed 2026-03-30]

### Can AI Assistant Be Invoked from Outside the IDE?

No direct external API or CLI invocation path exists for JetBrains AI Assistant itself. It is exclusively a GUI product inside JetBrains IDEs. However: [Source: https://www.jetbrains.com/help/ai-assistant/mcp.html, accessed 2026-03-30]
- The MCP server (described above) gives external agents IDE tool access, which is the closest equivalent.
- Junie CLI (described in a separate section below) is the headless, externally-invocable agent product.

### Compose Multiplatform-Specific Features

JetBrains' AI coding agents (Junie in particular) are documented as supporting Kotlin Multiplatform projects. A community blog post from March 2026 specifically discusses using Junie for KMP development. [Source: https://medium.com/@mirzemehdi/how-to-get-the-most-out-of-junie-in-a-kotlin-multiplatform-project-3ce67d235e0a, accessed 2026-03-30] No IDE-level AI feature specific to Compose Multiplatform preview or testing automation was identified.

### Assessment for Agent Use

| Criterion | Status |
|---|---|
| (a) Status as of March 2026 | Active; Claude Agent + Junie + ACP all shipped or in beta |
| (b) Usable without IDE GUI | No — AI Assistant requires IDE; Junie CLI is the headless equivalent |
| (c) Claude Code can connect | Indirectly via MCP server; via ACP headlessly using acp.json |
| (d) Setup complexity | Medium — BYOK or JetBrains AI subscription required |

**Confidence:** High — Multiple primary sources confirmed.

---

## JetBrains Fleet — Current Status

Fleet was **discontinued on December 22, 2025**. As of that date, Fleet is no longer available for download from JetBrains Toolbox or any other JetBrains channel. No further updates are being released. Users who had already downloaded Fleet may continue using it, though server-dependent features (including AI Assistant within Fleet) are expected to stop working over time. [Source: https://blog.jetbrains.com/fleet/2025/12/the-future-of-fleet/, accessed 2026-03-30]

### Why Fleet Was Discontinued

JetBrains concluded that maintaining two general-purpose IDE families (Fleet + IntelliJ-based IDEs) created user confusion, diluted focus, and did not justify the engineering investment. Rebuilding the full IntelliJ capability set within Fleet did not produce sufficient differentiated value. [Source: https://blog.jetbrains.com/fleet/2025/12/the-future-of-fleet/, accessed 2026-03-30]

### What Replaced Fleet: JetBrains Central

Fleet's technology was not abandoned — it became the platform for **JetBrains Central**, which launched in public preview on March 24, 2026. [Source: https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/, accessed 2026-03-30]

JetBrains Central is described as an "agentic development environment" — not a code editor, but an orchestration layer for running multiple AI agents concurrently on coding tasks. Key characteristics:
- Supports Claude Agent, OpenAI Codex, Gemini CLI, and Junie out of the box
- Uses JetBrains' Agent Client Protocol (ACP) for agent integration
- Execution options: local, Docker containers, or Git worktrees
- macOS only at launch; Windows/Linux planned for 2026
- No headless or API mode documented

**For the purposes of this research**: Fleet is irrelevant. JetBrains Central is UI-only and not programmatically accessible by Claude Code.

### Assessment for Agent Use

| Criterion | Status |
|---|---|
| (a) Status as of March 2026 | Dead (Fleet); JetBrains Central in public preview (macOS only) |
| (b) Usable without IDE GUI | Fleet: N/A. JetBrains Central: No headless mode documented |
| (c) Claude Code can connect | No |
| (d) Setup complexity | N/A |

**Confidence:** High — Official announcement with specific shutdown date confirmed by multiple sources.

---

## IntelliJ Platform Remote/HTTP API

### Built-in Web Server

IntelliJ IDEA includes a built-in web server (historically on port 63342) that has been used for:
- Opening files from external processes
- IDE Remote Control plugin: allows `REST API` calls to open projects, files, and settings [Source: https://plugins.jetbrains.com/plugin/19991-ide-remote-control, accessed 2026-03-30]
- Integration test remote driver: `http://localhost:63343/api/remote-driver/` exposes the IDE's Swing component tree for testing plugin UIs [Source: IntelliJ platform blog on integration tests, accessed 2026-03-30]

This API is primarily intended for plugin developers, not external agent automation. It does not expose build, run, or code analysis operations in a documented, stable form.

### HTTP Client CLI (Separate Product)

IntelliJ IDEA's HTTP Client CLI can execute `.http` request files from the terminal for API testing — it is not an IDE control surface and does not provide a path for agent automation. [Source: https://blog.jetbrains.com/idea/2022/12/http-client-cli-run-requests-and-tests-on-ci/, accessed 2026-03-30]

### MCP Server Supersedes This

As of 2025.2, the built-in MCP server is the sanctioned, documented path for external tool access to the IDE. It is substantially richer than the older built-in HTTP server and is the recommended approach.

### Assessment for Agent Use

| Criterion | Status |
|---|---|
| (a) Status as of March 2026 | Available but limited; MCP server is the preferred path |
| (b) Usable without IDE GUI | HTTP Client CLI: Yes (for API testing). Remote Control: No (IDE must be open) |
| (c) Claude Code can connect | Not designed for Claude Code; MCP server is the right choice |
| (d) Setup complexity | High and not well-documented for agent use |

**Confidence:** Medium — Evidence of the built-in web server and IDE Remote Control plugin is confirmed but the depth of automation surface for builds/tests is limited.

---

## KotlinConf 2025 Key Announcements

KotlinConf 2025 was held in May 2025. The major announcements relevant to this research:

### Compose Multiplatform for iOS — Stable

Compose Multiplatform 1.8.0 (released May 6, 2025) brought Compose Multiplatform for iOS to **stable/production-ready status**. Key capabilities delivered: native-like scrolling, iOS-native text selection, drag-and-drop, variable font support, and natural gestures. [Source: https://blog.jetbrains.com/kotlin/2025/05/compose-multiplatform-1-8-0-released-compose-multiplatform-for-ios-is-stable-and-production-ready/, accessed 2026-03-30]

### Compose Hot Reload

Compose Hot Reload was announced at KotlinConf 2025 as available: make changes to UI code and see them instantly without restarting the app or losing state. It became stable and bundled with the Compose Multiplatform Gradle plugin in the 1.10.0 release (January 2026). [Source: https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/, accessed 2026-03-30]

### AI Tooling Announcements

- **Junie**: Coding agent for complex Kotlin tasks across server, mobile, and KMP projects. IDE plugin Early Access Program announced. [Source: https://blog.jetbrains.com/kotlin/2025/05/kotlinconf-2025-language-features-ai-powered-development-and-kotlin-multiplatform/, accessed 2026-03-30]
- **Koog**: Open-sourced Kotlin-native AI agent framework with MCP integration, A2A protocol support, and multiplatform targets (JVM, Android, iOS, JS/Wasm). [Source: https://github.com/JetBrains/koog/, accessed 2026-03-30]
- **Mellum**: JetBrains' in-house LLM open-sourced; fine-tuned for Kotlin code completion and intelligent assistance. [Source: https://blog.jetbrains.com/kotlin/2025/05/kotlinconf-2025-language-features-ai-powered-development-and-kotlin-multiplatform/, accessed 2026-03-30]

**Confidence:** High — Official JetBrains blog posts confirmed with specific details.

---

## Compose Multiplatform 2025-2026 Tooling

### Release History (2025-2026)

| Version | Release Date | Key Milestone |
|---|---|---|
| 1.7.x | Early 2025 | Pre-stable iOS, incremental improvements |
| **1.8.0** | **May 6, 2025** | **Compose for iOS: Stable** |
| 1.9.0 | September 2025 | Compose for Web: Beta |
| **1.10.0** | **January 2026** | Stable Hot Reload, unified @Preview, Navigation 3 |
| 1.10.3 | ~February 2026 (unverified) | Patch release, minor fixes |

[Sources: https://blog.jetbrains.com/kotlin/2025/05/compose-multiplatform-1-8-0-released-compose-multiplatform-for-ios-is-stable-and-production-ready/, https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/, https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/, all accessed 2026-03-30]

### Key Tooling Features for Agent Use

**Compose Hot Reload (stable in 1.10.0)**
- CLI invocation: `./gradlew :myApp:hotRunJvm --autoReload` or `--auto`
- Bundled with Compose Multiplatform Gradle plugin; no extra configuration needed for Kotlin 2.1.20+
- Does not require IDE — runs via Gradle
- [Source: https://kotlinlang.org/docs/multiplatform/compose-hot-reload.html, accessed 2026-03-30]

**Unified @Preview Annotation (1.10.0)**
- Single `androidx.compose.ui.tooling.preview.Preview` annotation works across all platforms in `commonMain`
- Prior platform-specific annotations deprecated
- Preview rendering requires an IDE (IntelliJ IDEA 2025.2.2+ or Android Studio Otter 2025.2.1+)
- [Source: https://kotlinlang.org/docs/multiplatform/whats-new-compose-110.html, accessed 2026-03-30]

**Testing API (`runComposeUiTest()`)**
- Common test API in 1.9.0 guarantees correct execution across all platforms including web (returns a Promise for Wasm/JS)
- Tests can be run headlessly via Gradle: `./gradlew :myApp:desktopTest` or platform-specific equivalents
- [Source: https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/, accessed 2026-03-30]

**Headless Build/Test Surface (for Claude Code)**

The cleanest path for a Claude Code agent to build and verify Compose Multiplatform apps without any IDE running is pure Gradle:
- `./gradlew build` — compile all targets
- `./gradlew :shared:desktopTest` — run desktop UI tests headlessly
- `./gradlew :shared:jvmTest` — run JVM unit tests
- `./gradlew :shared:hotRunJvm` — start hot reload JVM desktop target
- Android tests require an emulator (cannot be fully headless without AVD setup)
- iOS tests require macOS with Xcode (cannot be headless on non-macOS)

### Assessment for Agent Use

| Criterion | Status |
|---|---|
| (a) Status as of March 2026 | Active; 1.10.x is current stable; iOS and Web both stable/beta |
| (b) Usable without IDE GUI | Yes — via Gradle for build/test; Hot Reload also CLI-driven |
| (c) Claude Code can connect | Yes — Claude Code can shell out to Gradle directly |
| (d) Setup complexity | Low — standard Gradle plugin, no extra agent infrastructure needed |

**Confidence:** High — Confirmed through official JetBrains Kotlin blog posts with version numbers and dates.

---

## Android Studio AI Features

### Gemini in Android Studio

Google's Gemini integration in Android Studio added an "Agent Mode" in 2025, announced with the Android Studio Narwhal Feature Drop Canary release. Agent Mode can interact with external MCP servers (Figma, GitHub, GitLab, Notion, Linear, etc.) to extend its capabilities. [Source: https://android-developers.googleblog.com/2025/06/agentic-ai-takes-gemini-in-android-studio-to-next-level.html, accessed 2026-03-30]

Configuration is performed at `File > Settings > Tools > AI > MCP Servers`, where external `httpUrl`-based MCP server configurations can be added.

### Can Gemini in Android Studio Be Driven from Outside the IDE?

No. Gemini in Android Studio is a GUI-only product. Android Studio does not expose its own MCP server for external consumption. Unlike IntelliJ IDEA 2025.2+, Android Studio does not have a built-in MCP server (as of March 2026; this gap may close as Android Studio is based on IntelliJ and typically adopts IDE features with a lag).

**⚠️ Note**: The exact Android Studio version where built-in MCP server support arrives could not be confirmed from primary sources. IntelliJ IDEA 2025.2 has it; Android Studio's adoption timeline is unconfirmed.

### Assessment for Agent Use

| Criterion | Status |
|---|---|
| (a) Status as of March 2026 | Gemini Agent Mode available in recent Canary/stable builds |
| (b) Usable without IDE GUI | No |
| (c) Claude Code can connect | No — Android Studio does not expose an MCP server to external clients (confirm for latest version) |
| (d) Setup complexity | N/A |

**Confidence:** Medium — Based on Google Android Developers blog posts and official Android Studio docs, confirmed through 2025.

---

## Third-Party MCP Servers for JetBrains

### TeamCity MCP Server (Community)

The most directly useful third-party MCP server for JetBrains CI is `@daghis/teamcity-mcp`. [Source: https://github.com/Daghis/teamcity-mcp, accessed 2026-03-30]

**What it provides:**
- 87 MCP tools in Full Mode (31 in Dev Mode)
- Trigger and monitor builds, fetch build logs, inspect test failures
- Create/clone build configurations, manage VCS roots, agents, parameters
- Build problem identification and test analysis
- Explicit Claude Code integration: `claude mcp add teamcity`

**Setup:**
```bash
# Install and connect (Dev Mode, safe operations only)
TEAMCITY_URL=https://your-tc-instance.com \
TEAMCITY_TOKEN=your-token \
npx -y @daghis/teamcity-mcp
```

**Status:** Community project (MIT license, not official JetBrains). Active as of search date. Not affiliated with JetBrains officially.

**For a Compose Multiplatform workflow**: If your project uses TeamCity CI, this MCP server lets Claude Code trigger a Compose Multiplatform build, wait for it, and pull back test results — entirely programmatically without any IDE running.

### JetBrains-Provided Extension Point

The official `mcp-server-plugin` GitHub repo (deprecated as of 2025.2) documented an extension point system for third-party plugins to add their own MCP tools to the IDE's MCP server. This means IntelliJ plugins can extend the MCP tool surface. [Source: https://github.com/JetBrains/mcp-server-plugin, accessed 2026-03-30]

### Community IntelliJ Index Plugin

`hechtcarmel/jetbrains-index-mcp-plugin` is a community plugin designed to expose IntelliJ's code indexing capabilities to external agents as an MCP server. [Source: https://github.com/hechtcarmel/jetbrains-index-mcp-plugin, accessed 2026-03-30] Maturity and maintenance status were not confirmed.

**Confidence:** High for TeamCity MCP (direct repo review); Medium for community IntelliJ plugins.

---

## Junie CLI — Headless Agent (New Finding, High Relevance)

### What Is Junie CLI?

Junie CLI is a standalone AI coding agent released by JetBrains in beta as of March 2026. It runs entirely from the terminal with no IDE required. [Source: https://blog.jetbrains.com/junie/2026/03/junie-cli-the-llm-agnostic-coding-agent-is-now-in-beta/, accessed 2026-03-30]

Key characteristics:
- **LLM-agnostic**: Supports Anthropic (Claude), OpenAI, Google, xAI, OpenRouter, GitHub Copilot via BYOK
- **BYOK pricing**: No JetBrains platform fee when using your own API keys
- **Multi-environment**: Terminal, IDE plugin (IntelliJ/Android Studio), CI/CD, GitHub/GitLab
- **Headless mode**: Explicitly documented for CI/CD; invocable without interactive UI

### Headless Invocation

```bash
junie --auth="$JUNIE_API_KEY" "Review and fix any code quality issues in the latest commit"
```

[Source: https://junie.jetbrains.com/docs/junie-headless.html, accessed 2026-03-30]

The auth token is separate from LLM API keys; it authenticates to the Junie service at `junie.jetbrains.com/cli`.

### Can Claude Code Invoke Junie CLI?

Yes — as a subprocess via Bash. Claude Code could shell out to Junie CLI to:
- Run a JetBrains-tuned code review on Kotlin/Compose code
- Fix compilation errors using JetBrains' IDE analysis (when configured with IntelliJ backend)
- Trigger CI/CD-style quality checks

This is **delegation**, not integration: Claude Code would use Junie as a specialist tool for JetBrains-specific analysis, not as a direct MCP connection.

### Limitations

- Beta status as of March 2026 — API may change
- Requires separate Junie account and auth token
- Output format for machine consumption is not fully documented from available sources — treat Junie CLI as experimental for programmatic parsing until structured output is documented; workaround is to capture stdout as free-text and parse with heuristics or pass to an LLM for interpretation
- Not an MCP server itself (cannot be registered as an MCP server for Claude Code to call tool-style)

### Assessment for Agent Use

| Criterion | Status |
|---|---|
| (a) Status as of March 2026 | Beta; actively developed |
| (b) Usable without IDE GUI | Yes — designed for headless/CI use |
| (c) Claude Code can connect | Via subprocess invocation (shell-out); not MCP |
| (d) Setup complexity | Medium — Junie account + auth token + BYOK API key configuration |

**Confidence:** High — Official JetBrains blog post and GitHub repository confirmed, beta as of March 2026.

---

## Recommended Approach

For a Claude Code agent that wants to leverage JetBrains tooling to build and verify Compose Multiplatform apps, three approaches are viable depending on the scenario:

### Option A: IntelliJ IDEA as MCP Server (Best for Rich IDE Integration)

**When to use**: When an IntelliJ IDEA instance is available and running (developer machine, CI with virtual display).

**Setup**:
1. Install IntelliJ IDEA 2025.2 or later with the KMP plugin
2. Open the Compose Multiplatform project
3. In IntelliJ: `Settings | Tools | MCP Server → Enable → Auto-Configure → Claude Code`
4. Claude Code gains 25+ IDE tools: execute run configurations, run terminal commands, analyze code, search files, rename refactoring

**What Claude Code can do**:
- Execute Gradle run configurations (build, test, assemble) via `execute_run_configuration`
- Run arbitrary terminal commands via `execute_terminal_command` including `./gradlew test`
- Analyze files for compilation errors via `get_file_problems`
- Inspect project structure, dependencies, modules

**Limitation**: Requires IDE to be running. Not suitable for pure headless CI environments.

### Option B: Pure Gradle Headless (Best for CI / No IDE)

**When to use**: Headless CI environments, Docker containers, automated pipelines.

**Setup**: No JetBrains tooling required — only the Gradle wrapper and appropriate SDKs (JDK, Android SDK for Android targets, Xcode for iOS).

**What Claude Code can do**:
- `./gradlew build` — build all targets
- `./gradlew desktopTest` — run desktop UI tests (fully headless on JVM)
- `./gradlew jvmTest` — run common JVM unit tests
- `./gradlew :app:hotRunJvm` — launch hot reload (requires display for visual validation)
- Parse Gradle test XML output in `build/test-results/` for structured results

**Limitation**: Android instrumented tests require emulator. iOS builds require macOS + Xcode. No IDE-level analysis.

### Option C: TeamCity MCP Server (Best for Teams with JetBrains CI)

**When to use**: Teams already using JetBrains TeamCity as their CI platform.

**Setup**:
```bash
claude mcp add teamcity \
  --env TEAMCITY_URL=https://tc.yourcompany.com \
  --env TEAMCITY_TOKEN=your-token
```

**What Claude Code can do**:
- Trigger Compose Multiplatform build configurations
- Monitor build status and retrieve results
- Inspect test failures from TeamCity's test reports
- All without an IDE running

---

## Gaps and Limitations

1. **No headless IntelliJ**: The built-in MCP server requires a running IDE with GUI. There is no IntelliJ "server mode" that exposes MCP tools without opening the full IDE. This is the single largest gap.

2. **Android Studio MCP server status uncertain**: Android Studio is based on IntelliJ but typically lags on adopting platform features. Whether the built-in MCP server is available in Android Studio as of March 2026 could not be confirmed from primary sources. The official Claude Code docs list Android Studio as a supported IDE for the Claude Code *plugin*, but not specifically for the MCP server.

3. **Fleet is gone**: Any planning work that assumed Fleet as an integration target is obsolete as of December 22, 2025.

4. **JetBrains Central has no API**: JetBrains Central (public preview March 24, 2026) orchestrates agents through a GUI only. No programmatic interface or MCP surface was documented.

5. **Junie CLI output format not fully documented**: While headless invocation is confirmed, the structured output format for machine parsing was not detailed in available documentation as of this research date. Treat Junie CLI as experimental for programmatic use until this is resolved; recommended workaround is to capture stdout as free-text and use an LLM or regex heuristics to extract structured results.

6. **iOS and Android testing remain platform-constrained**: Compose Multiplatform iOS tests require macOS + Xcode; Android instrumented tests require an emulator or real device. No JetBrains tooling changes this constraint.

7. **Koog is an agent framework, not an integration point**: Koog is a Kotlin library for *building* AI agents, not a tool that Claude Code can call. It is relevant if the project itself embeds AI agents, but not as infrastructure for Claude Code's use of JetBrains tooling.

8. **ACP headless path**: The Agent Client Protocol (ACP) that JetBrains Central and JetBrains IDEs use for agent integration is fully live as of 25.3. Claude Code can connect headlessly via `acp.json` configuration, though it is not listed as a natively supported ACP agent. See ACP section above for details.

9. **GitHub Copilot MCP GA (not relevant)**: GitHub Copilot's JetBrains MCP support reached GA in August 2025 but does not provide a path for Claude Code.

---

## Sources

| URL | Source Name | Access Date |
|---|---|---|
| https://www.jetbrains.com/help/idea/mcp-server.html | IntelliJ IDEA MCP Server Documentation | 2026-03-30 |
| https://github.com/JetBrains/mcp-jetbrains | JetBrains mcp-jetbrains GitHub (deprecated) | 2026-03-30 |
| https://github.com/JetBrains/mcp-server-plugin | JetBrains mcp-server-plugin GitHub (deprecated) | 2026-03-30 |
| https://blog.jetbrains.com/idea/2025/05/intellij-idea-2025-1-model-context-protocol/ | IntelliJ IDEA 2025.1 MCP Blog Post | 2026-03-30 |
| https://www.jetbrains.com/help/ai-assistant/mcp.html | AI Assistant MCP Documentation | 2026-03-30 |
| https://www.jetbrains.com/help/ai-assistant/acp.html | AI Assistant ACP Documentation | 2026-03-30 |
| https://www.jetbrains.com/help/ai-assistant/settings-reference-providers-and-api-keys.html | AI Assistant Settings: Providers and API Keys | 2026-03-30 |
| https://blog.jetbrains.com/ai/2025/12/bring-your-own-ai-agent-to-jetbrains-ides/ | Bring Your Own AI Agent Blog Post | 2026-03-30 |
| https://blog.jetbrains.com/fleet/2025/12/the-future-of-fleet/ | The Future of Fleet (Discontinuation Announcement) | 2026-03-30 |
| https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/ | JetBrains Central Launch Blog Post | 2026-03-30 |
| https://www.jetbrains.com/help/air/quick-start-with-air.html | JetBrains Central Quick Start Documentation | 2026-03-30 |
| https://junie.jetbrains.com/docs/junie-cli.html | Junie CLI Documentation | 2026-03-30 |
| https://junie.jetbrains.com/docs/junie-headless.html | Junie Headless Mode Documentation | 2026-03-30 |
| https://blog.jetbrains.com/junie/2026/03/junie-cli-the-llm-agnostic-coding-agent-is-now-in-beta/ | Junie CLI Beta Announcement | 2026-03-30 |
| https://github.com/JetBrains/junie | JetBrains Junie GitHub Repository | 2026-03-30 |
| https://blog.jetbrains.com/kotlin/2025/05/kotlinconf-2025-language-features-ai-powered-development-and-kotlin-multiplatform/ | KotlinConf 2025 Keynote Recap Blog Post | 2026-03-30 |
| https://blog.jetbrains.com/kotlin/2025/09/the-kotlin-ai-stack-build-ai-agents-with-koog-code-smarter-with-junie-and-more/ | Kotlin AI Stack Blog Post (Sept 2025) | 2026-03-30 |
| https://github.com/JetBrains/koog/ | Koog GitHub Repository | 2026-03-30 |
| https://blog.jetbrains.com/kotlin/2026/01/compose-multiplatform-1-10-0/ | Compose Multiplatform 1.10.0 Release Post | 2026-03-30 |
| https://blog.jetbrains.com/kotlin/2025/05/compose-multiplatform-1-8-0-released-compose-multiplatform-for-ios-is-stable-and-production-ready/ | Compose Multiplatform 1.8.0 Release Post | 2026-03-30 |
| https://blog.jetbrains.com/kotlin/2025/09/compose-multiplatform-1-9-0-compose-for-web-beta/ | Compose Multiplatform 1.9.0 Release Post | 2026-03-30 |
| https://blog.jetbrains.com/kotlin/2025/08/kmp-roadmap-aug-2025/ | KMP Roadmap August 2025 | 2026-03-30 |
| https://kotlinlang.org/docs/multiplatform/whats-new-compose-110.html | What's New in Compose Multiplatform 1.10.x | 2026-03-30 |
| https://blog.jetbrains.com/ai/2025/09/introducing-claude-agent-in-jetbrains-ides/ | Claude Agent in JetBrains IDEs Announcement | 2026-03-30 |
| https://code.claude.com/docs/en/jetbrains | Claude Code JetBrains Integration Docs (Official) | 2026-03-30 |
| https://github.com/Daghis/teamcity-mcp | teamcity-mcp Community GitHub Repository | 2026-03-30 |
| https://developer.android.com/studio/gemini/add-mcp-server | Android Studio: Add MCP Server Docs | 2026-03-30 |
| https://android-developers.googleblog.com/2025/06/agentic-ai-takes-gemini-in-android-studio-to-next-level.html | Android Developers Blog: Gemini Agent Mode | 2026-03-30 |
| https://plugins.jetbrains.com/plugin/27310-claude-code-beta- | Claude Code Beta JetBrains Plugin | 2026-03-30 |
| https://github.com/hechtcarmel/jetbrains-index-mcp-plugin | jetbrains-index-mcp-plugin Community GitHub | 2026-03-30 |
| https://medium.com/@mirzemehdi/how-to-get-the-most-out-of-junie-in-a-kotlin-multiplatform-project-3ce67d235e0a | Community: Using Junie for KMP Development (Medium) | 2026-03-30 |
| https://github.blog/changelog/2025-08-13-model-context-protocol-mcp-support-for-jetbrains-eclipse-and-xcode-is-now-generally-available/ | GitHub Copilot MCP GA for JetBrains | 2026-03-30 |
