---
content_origin: gemini-cli
date: 2026-04-04
topic: "JetBrains Air"
---

# JetBrains Air: Analysis and Integration Patterns
**Date:** 2026-04-04
**Status:** Complete

*This document contains the findings of research into JetBrains Air, focusing on its comparison to and potential integration with Momentum/Claude Code workflows. All claims are supported by sources from early 2026.*

---

## 1. Multi-Agent Task Dispatch vs. Skill Composition

This section compares Air's orchestration model with the skill composition approach used by CLI agents like Claude Code.

### Findings

JetBrains Air introduces a paradigm of **concurrent, multi-agent orchestration**, which is a fundamental departure from the sequential, single-agent skill execution model common in CLI-based tools.

*   **Concurrent Task Execution:** The most significant differentiator is Air's ability to dispatch tasks to multiple, distinct AI agents and have them work in parallel [1, 2]. A developer can assign a bug fix to one agent (e.g., Claude) while another agent (e.g., Gemini) works on generating unit tests for a new feature simultaneously [1].
*   **Isolated Workspaces:** To manage this concurrency safely, Air automatically provisions isolated environments for tasks using technologies like Git worktrees or Docker containers [5]. This prevents parallel agents from creating conflicts on the filesystem, a major challenge that single-threaded CLI agents do not need to account for.
*   **Orchestration Layer:** Air acts as a high-level "agentic development environment" (ADE) or workflow layer [2, 6]. Its primary role is not to be an agent itself, but to manage the lifecycle, context, and review process for a suite of other agents. It is designed around a formal "task" primitive that is assigned to an agent and tracked to completion [6].
*   **Open Agent Ecosystem:** Air's support for multiple agents is enabled by the **Agent Client Protocol (ACP)**, an open standard that allows any compliant agent to be integrated [5, 8]. This contrasts with the closed, proprietary skill ecosystems of many single-agent frameworks.

### What Air Can Orchestrate That Claude Code Cannot

*   **True Parallel Development:** Air can execute multiple independent coding tasks at the same time, limited only by local machine resources. A CLI agent can only execute one skill at a time.
*   **Conflict-Free Concurrency:** Air's automated workspace isolation is a sophisticated orchestration feature that prevents race conditions and conflicting file modifications between agents.
*   **Heterogeneous Agent Delegation:** A developer can choose the best agent for a given task (e.g., use Claude for creative generation and a specialized code analysis agent for another task) and run them concurrently within the same project [1, 3].

---

## 2. IDE-Level Capabilities

This section details the unique, IDE-aware capabilities Air provides to agents.

### Findings

While Air is not a full-featured IDE like IntelliJ IDEA, its foundation on the JetBrains Fleet platform provides agents with deep, structural awareness of the codebase, far surpassing the context available to file-based CLI tools [10, 11].

*   **Deep Symbol Resolution:** Air's core advantage is its code intelligence. It has a structural understanding of the project, allowing developers to provide agents with highly specific, semantic context. Instead of referencing "lines 10-50 of file.py," a developer can assign a task using precise handles to specific classes, methods, interfaces, or even Git commits [16, 20]. This rich context allows agents to generate more accurate and relevant code.
*   **Agent-Delegated Refactoring:** Air does not have its own refactoring engine exposed to the user. Instead, it treats refactoring as a task to be delegated to an agent [17]. The workflow is: 1) Assign a refactoring task to an agent (e.g., "Refactor this class to use the Strategy pattern"). 2) The agent performs the code transformation. 3) Air uses its code intelligence to present a rich, semantically-aware diff for the developer to review and approve [14].
*   **No Interactive Debugger:** Current versions of Air do not include an interactive, step-through debugger [21, 22]. The workflow is focused on agent-driven code generation and review, not traditional debugging. "Debugging" in the context of Air refers to assigning a bug-fixing task to an agent, not using a debugging tool.

### Capabilities Lacking in CLI Tools

*   **Semantic Context:** CLI tools operate on files and text. They lack the project-wide symbol graph and type information that Air provides to agents, making it impossible to reliably reference a specific method or understand its usages across the codebase.
*   **Awareness of Refactoring Impact:** When a CLI tool performs a textual replacement (e.g., renaming a function), it has no awareness of that symbol's other usages. An agent working through Air can be tasked to perform a "rename" refactoring, and it can leverage the underlying code intelligence to update all references correctly.
*   **Integrated, Code-Aware Review:** Reviewing agent output in a CLI tool is typically a simple text diff. Air provides a review interface within the context of the full codebase, with syntax highlighting and semantic understanding, making it easier to validate changes [14, 15].

---

## 3. Coexistence and Integration Patterns

This section provides concrete scenarios for using Air and Momentum/Claude Code together.

### Findings

Coexistence is not only possible but is an intended workflow. Air's support for the open ACP standard and its explicit inclusion of agents like the "Claude Agent" and "Gemini CLI" confirm this [3, 4, 8]. The key is to delegate tasks to the environment best suited for them.

### Actionable Recommendations & Patterns

**Pattern 1: Broad-to-Narrow Implementation**
1.  **Momentum/CLI:** Use the CLI agent for broad, project-level setup.
    *   `claude: "Create a new Spring Boot service for managing user profiles, including a controller, service, and repository layer. Generate basic unit tests for the controller."`
2.  **Air Handoff:** Once the files are scaffolded, delegate the complex "inner loop" work to Air.
    *   *In Air's UI:* Assign a task to the Claude Agent: `"In UserProfileService.java, implement the updateProfile method. It should handle validation, database updates, and return the updated profile. Ensure all exceptions are handled gracefully."`

**Pattern 2: Agent-Powered Debugging & Refactoring**
1.  **Momentum/CLI:** Use the CLI to run tests and identify an issue.
    *   `claude: "Run the test suite. A failure is expected in the user profile tests."`
    *   *Output shows a specific test failing.*
2.  **Air Handoff:** Delegate the fix to an agent in Air, providing the precise test as context.
    *   *In Air's UI:* Assign a task: `"The testUpdateProfile_FailsOnInvalidEmail test is failing. Fix the validation logic in the UserProfileService to ensure it correctly rejects invalid email formats."`

**Pattern 3: Concurrent Workstreams**
1.  **Momentum/CLI:** Kick off a long-running, low-supervision task.
    *   `claude: "Generate comprehensive Javadoc documentation for the entire /com/mycorp/services/ package."`
2.  **Air (Simultaneously):** While the CLI agent works on documentation, use Air for a separate, high-context task.
    *   *In Air's UI:* Assign a task in a new, isolated worktree: `"Spike a new feature: add a Redis cache to the UserProfileService's getProfile method. Show me the required dependency changes and the code modifications."`

---

## 4. Current Limitations and Gaps

*   **No Interactive Debugger:** The lack of a traditional step-through debugger is a significant gap for workflows that require deep inspection of runtime behavior [21, 22].
*   **Dependency on Agent Capabilities:** Air is an orchestrator; the quality of its output is entirely dependent on the intelligence and capabilities of the third-party agents it manages.
*   **Platform Availability:** The initial public preview was released for macOS only, limiting immediate cross-platform adoption [3, 6].
*   **New Protocol:** The Agent Client Protocol (ACP) is new, and its adoption by a wide range of agents is not yet guaranteed [5].

---

### Cited Sources

- [1] medium.com — Multi-agent orchestration analysis
- [2] adtmag.com — Air ADE classification and workflow layer
- [3] jetbrains.com — Official Air documentation and agent support
- [4] techzine.eu — Air integration patterns
- [5] jvm-weekly.com — ACP protocol and isolated workspaces
- [6] theregister.com — Air launch coverage, macOS limitation
- [8] adtmag.com — ACP open standard details
- [10] medium.com — Fleet platform foundation
- [11] medium.com — Code intelligence capabilities
- [14] funblocks.net — Review interface and diff analysis
- [15] jetbrains.com — Code-aware review documentation
- [16] sdtimes.com — Symbol resolution and context handles
- [17] jetbrains.com — Refactoring delegation model
- [20] jetbrains.com — Context specification (commits, methods)
- [21] funblocks.net — Debugger absence
- [22] reddit.com — Community discussion on debugging limitations
