---
content_origin: gemini-deep-research
date: 2026-04-04
topic: "JetBrains Air"
method: cmux-browser automation of gemini.google.com Deep Research
sources:
  - https://www.jetbrains.com/help/idea/refactoring-source-code.html
  - https://wavespeed.ai/blog/posts/claude-code-architecture-leaked-source-deep-dive/
---

The Formalization of Agentic Engineering: A Technical Analysis of JetBrains Air and its Role in the 2026 Software Delivery Ecosystem
The transition from traditional tool-assisted development to autonomous agentic engineering represents the most significant shift in software production since the adoption of integrated development environments. By April 2026, the industry has largely moved beyond the era of unstructured interaction with large language models, characterized by the informal and often chaotic practice of "vibe coding," toward a rigorous discipline of "agentic engineering". This evolution is underpinned by the emergence of Agentic Development Environments (ADEs), with JetBrains Air positioned as a primary architectural response to the fragmentation, context loss, and reliability gaps inherent in early CLI-based AI-assisted workflows. The launch of JetBrains Air in March 2026 serves as a definitive milestone where agent orchestration moves from experimental terminal scripts into a governed, semantic, and high-velocity production system.   

Architectural Foundations and the ADE Paradigm Shift
The concept of the Agentic Development Environment is fundamentally distinct from the traditional Integrated Development Environment. While a conventional IDE like IntelliJ IDEA or PyCharm is designed to augment a human developer’s typing and navigation, JetBrains Air is architected to facilitate a developer’s role as an orchestrator of autonomous task loops. This shift acknowledges a reality documented by industry leaders: the mechanical act of writing code is increasingly handled by AI, while the human engineer’s value is repositioned into system design, requirement validation, and the management of multiple specialized agents.   

JetBrains Air is built upon a modernized foundation derived from the discontinued Fleet project, offering a lightweight, distributed architecture that prioritizes agent-centric tooling over the classic editor-first interface. This architectural choice enables Air to provide performance characteristics that align with the high-concurrency needs of parallel agent execution, addressing the "agent sprawl" where developers previously had to juggle dozens of terminal tabs and browser windows for a single complex feature.   

Defining the Agentic Development Environment

The ADE model reverses the hierarchy of traditional AI integration. In an IDE with an AI plugin, the assistant is a guest within the human’s workflow. In an ADE, the agent’s task is the primary unit of work, and the environment provides the necessary sandboxing, context, and review tools for that task to reach completion. This is particularly critical in 2026, where 95% of engineers use AI tools weekly and over half have adopted fully agentic systems.   

Feature Category	Traditional IDE (e.g., IntelliJ IDEA)	Agentic Development Environment (Air)
Primary User Model	Human-centric; AI as an inline assistant.	Agent-centric; Human as a supervisor/reviewer.
Work Unit	Files, lines of code, and single sessions.	Asynchronous, concurrent "Task Loops."
Context Management	Open tabs and recently visited files.	Semantic project maps, symbols, and commits.
Execution Strategy	Synchronous local runs.	Isolated, parallel runs (Docker/Worktrees).
Workflow Goal	Assisting the human in writing code.	Orchestrating agents to deliver outcomes.

The move toward ADEs like Air is driven by the "METR measurement paradox," which identified that while AI tools create a perception of 20% faster coding, they can actually cause a 19% slowdown due to the overhead of fixing subtle errors and managing uncoordinated AI outputs. Air attempts to resolve this by imposing a rigorous "Task View" that maintains state and context for every agent session, preventing the cognitive load associated with fragmented terminal interactions.   

Multi-Agent Orchestration: JetBrains Air vs. Claude Code
A central question in the evaluation of modern engineering tools is how they handle the complexity of multi-agent workflows. JetBrains Air and Anthropic’s Claude Code represent the two dominant philosophies in 2026: centralized, environment-aware task dispatch and decentralized, peer-to-peer agent messaging.

Air's Centralized Task Dispatch and Blackboard Model

JetBrains Air employs what is essentially a centralized orchestration or "blackboard" model. In this configuration, the developer defines a task with precise context—referencing specific classes, methods, or commits—and dispatches it to a selected agent. Air manages the "Task Loop," which consists of planning, execution, and review. The critical difference here is that the developer remains the central hub of coordination. Multiple agents can run concurrently on different tasks (e.g., one agent implementing a backend API while another writes frontend tests), but their outputs are reconciled by the developer within the Air environment’s unified diff and review interface.   

This model allows Air to orchestrate diverse agents that might not natively speak to one another. For example, a developer can run OpenAI Codex for legacy code refactoring and Gemini CLI for deep semantic exploration of a new framework simultaneously. Air provides the "glue" by managing separate isolation environments (like different Docker containers) for each, preventing the branch collisions and dependency conflicts that plague uncoordinated CLI sessions.   

Claude Code's Subagent and Team Composition

In contrast, Claude Code utilizes a more organic, model-centric approach through "Subagents" and "Agent Teams".   

Subagents are primarily used for context compression and isolation. A parent Claude instance can spawn a subagent to perform a specific research task, such as "Identify all occurrences of the Auth singleton in the v2 module." The subagent operates in its own context window, and when finished, it returns only the distilled answer to the parent. This prevents the parent’s context window from becoming cluttered with the subagent’s "thinking" or trial-and-error steps. However, subagents are fire-and-forget; they cannot talk to each other and always report back to the single parent.   

Claude Code "Agent Teams" represent a higher level of autonomy. This peer-to-peer model involves a "Team Lead" spawning "Teammates" that can message each other directly to negotiate contracts and dependencies. For instance, a "Frontend Teammate" can notify a "Backend Teammate" that a specific JSON schema needs an extra field, and the Backend agent can adjust its implementation without the developer or the Team Lead needing to manually relay that information.   

Orchestration Capabilities and Comparison

The functional gap between these two models defines where they are best deployed. JetBrains Air’s strength lies in its ability to orchestrate at the system level—managing environment setup, file locking, and multi-agent concurrency across diverse providers. Claude Code’s strength is at the reasoning level—allowing a highly capable model to self-organize its own sub-tasks.   

Orchestration Aspect	JetBrains Air (ADE Model)	Claude Code (P2P Team Model)
Agent Interoperability	High; dispatches tasks to Codex, Claude, Gemini, Junie.	Limited; primarily Anthropic-family models.
State Management	Externalized; tasks have persistent history and snapshots.	Internal; relies on the parent agent’s context window.
Isolation	Hard; Docker and Git worktrees managed by host.	Soft; logical separation within context windows.
Conflict Resolution	Human-centric; developer merges task outputs.	Agent-centric; agents negotiate dependencies.
Context Limit Handling	Uses persistent specs to resume sessions.	Uses summaries to compress subagent results.

JetBrains Air can orchestrate what Claude Code cannot: a truly heterogeneous agent team. Because Air is built on the Agent Client Protocol (ACP), it can integrate a custom local agent optimized for a company’s proprietary database alongside a frontier model like Claude 4.5. Claude Code is architecturally bound to the Anthropic ecosystem, which, while powerful, creates a single point of failure and vendor lock-in that enterprise architects in 2026 are increasingly wary of.   

IDE-Level Capabilities and Semantic Depth
A primary motivation for the move from CLI tools to Air is the exposure of the "Project Model"—the deep, indexed understanding of a codebase that JetBrains has refined over 26 years. CLI-based agents like Claude Code typically view a repository as a collection of text files. They use grep for searching and ls -R for discovery, but they often lack the ability to understand the true semantic relationship between symbols.   

The Program Structure Interface (PSI) and Symbol Resolution

JetBrains Air exposes its Program Structure Interface (PSI) to agents, a capability that represents a quantum leap over standard RAG (Retrieval-Augmented Generation) techniques. While a CLI agent might find the string UserService in a hundred files, an Air-aware agent understands which specific UserService instance is being injected into a controller, even across complex dependency injection frameworks like Spring or NestJS.   

This symbol resolution allows agents to perform "IDE-aware task definition." When a developer tells an agent to "Refactor the authentication flow," the agent doesn't just look for files with "Auth" in the name; it queries the project model for the actual interface definitions, implementation classes, and usage sites. This depth prevents the "fragmented refactor" error common in CLI tools, where an agent changes a method signature in one file but fails to update its usage in a compiled library or a separate module it didn't "grep" for.   

Refactoring Awareness and Safe Execution

Air allows agents to utilize the same high-level refactoring tools as human developers. Instead of the agent manually deleting lines and typing new ones—which is prone to syntax errors—it can invoke an "Extract Method" or "Rename" action. The IDE engine handles the heavy lifting of ensuring the refactor is "safe," checking for naming collisions and updating all references across the project.   

Capability	CLI-Based Tools (Claude Code)	JetBrains Air (ADE)
File Navigation	Text-based search and path traversal.	Symbol-aware navigation (classes, methods).
Refactoring	Manual text editing of files.	Atomic IDE refactorings (Safe Delete, Rename).
Error Detection	Post-execution (running compiler/tests).	Real-time inspections and "on-the-fly" fixes.
Dependency Analysis	Limited to visible file imports.	Full project-model-aware graph analysis.
Language Support	Model-dependent; generic text parsing.	Deep support via language-specific PSI engines.

Debugger Integration and Feedback Loops

Perhaps the most significant IDE-level capability exposed by Air is the "Integrated Debugger Loop." When an agent implements a change that causes a test failure, a CLI tool typically gives the agent the raw console output or stack trace. In JetBrains Air, the agent can interact with the debugger's execution state.   

This includes access to "Async Stacktraces," which are essential for debugging modern reactive or asynchronous codebases where traditional stack traces are often unhelpful. The agent can "see" the values of variables at the moment of failure and use the IDE’s Data Flow Analysis (DFA) to understand how a null value propagated through the system. This allows the agent to move beyond "vibe-fixing" (guessing a fix based on the error message) to "engineering" a solution based on the actual runtime state.   

Coexistence and Integration Patterns for Agentic Engineering
JetBrains Air does not exist in a vacuum; it is designed to complement existing workflows. In practice, professional engineering teams in 2026 are finding that the most effective approach is a hybrid model that uses Claude Code for planning and JetBrains Air for implementation and verification.   

The "Momentum" Workflow: Claude as Architect, Air as Implementer

The "Momentum" workflow, popularized by frameworks like The Agentic Startup, emphasizes a "Spec-Driven Development" approach. This paradigm splits the development process into two primary phases: Strategic Specification and Tactical Execution.   

Strategic Specification (Claude Code): Claude Code is exceptionally proficient at the reasoning required to transform vague requirements into detailed technical plans. Using the /specify command, a developer can engage Claude in a deep research cycle where it analyzes the codebase to produce a PRD (Product Requirements Document), an SDD (Software Design Document), and a multi-phase implementation plan. Because this phase is largely conversational and research-intensive, Claude Code's terminal-centric, high-reasoning interface is highly efficient.   

Tactical Execution (JetBrains Air): Once the plan.md is generated, the workflow shifts to JetBrains Air for the "heavy lifting" of code generation. The developer dispatches the individual phases of the plan to parallel agents within Air.   

Concrete Scenario: Implementing a Complex Microservice Update

In a real-world scenario, a team needs to migrate a legacy authentication module to a new OAuth 2.1 standard across three microservices.

Step 1: The Planning Phase. The developer runs Claude Code with the Momentum plugin to research the legacy code across the three repositories. Claude identifies the common patterns and potential breaking changes, producing a unified solution.md and a list of specific implementation tasks for each service.   

Step 2: The Parallel Execution Phase. The developer opens the three microservice projects in JetBrains Air. For each project, a separate task is created:

Task 1 (Claude Agent): Implements the new OAuth controller logic in a Git Worktree, ensuring the main branch remains stable during the complex migration.   

Task 2 (Codex Agent): Updates the data schema and migrations in a Docker container, allowing the agent to run actual SQL migrations and verify they work against a temporary database instance without polluting the local dev environment.   

Task 3 (Junie Agent): Generates the updated client-side SDKs and runs the integrated IDE inspections to catch any broken references in downstream modules.   

Step 3: The Verification Phase. Each agent in Air completes its task loop and presents a diff for review. The developer uses Air’s "Unified Diff View" to see how the changes across the three services align with the original solution.md produced by Claude Code.   

Value-Add of Delegation to JetBrains Air

Delegating implementation to Air adds value in three specific areas that CLI tools like Claude Code often struggle with:

Isolation and Concurrency: Running Momentum implementers in Claude Code sequentially can take hours for large features. Air dispatches them to parallel, sandboxed environments, drastically reducing the "time-to-ship".   

Snapshot and Rollback: Air's "Task Snapshot" capability allows a developer to save the state of an agent's work. If an agent goes down a wrong path during a refactor, the developer can roll back the entire workspace state to a previous snapshot—something that is difficult to do in a standard terminal session without manually wrestling with Git.   

Review Quality: Reviewing a 50-file diff in a terminal is error-prone. Air provides a full IDE-grade review experience where the developer can use "Search Everywhere" and "Find Usages" while reviewing the agent's proposed changes.   

Technical Architecture and Governance: JetBrains Central
As agentic work scales from individual developers to entire organizations, the focus shifts from raw productivity to governance, security, and cost management. JetBrains Central serves as the organizational backend for both individual ADEs like Air and the broader engineering system.   

The Role of JetBrains Central in Agentic Engineering

JetBrains Central provides three core "Enterprise-Grade" capabilities that address the risks of autonomous agents in a corporate environment:

Governance and Policy Enforcement: Organizations can define which agents are allowed to access specific repositories and what level of permission they have (e.g., "Auto-Edit" for testing folders vs. "Ask Permission" for core infrastructure code).   

Unified Shared Context: Central connects agents to "corporate context"—internal documentation, APIs, and cross-team knowledge. This prevents the "architectural drift" where agents in different teams suggest incompatible solutions because they lack a shared understanding of the company's broader tech stack.   

Cost Management and Attribution: As organizations move beyond flat subscriptions to usage-based API billing, JetBrains Central provides a single "Console" for monitoring AI spend. It can attribute costs to specific teams, projects, or even individual features, allowing for a clear ROI analysis of agentic engineering.   

The Agent Client Protocol (ACP) Ecosystem

The technical bridge enabling this flexibility is the Agent Client Protocol (ACP), an open standard co-developed by JetBrains and Zed. ACP standardizes how "Editors" (like Air or IntelliJ) communicate with "Agents" (like Claude Code or Gemini CLI), effectively doing for AI agents what the Language Server Protocol (LSP) did for programming languages.   

ACP Component	Function	Enterprise Impact
ACP Registry	A curated list of agents (Gemini, Claude, Cursor, OpenCode).	Allows teams to "swap" models based on cost/performance without re-tooling.
Custom Agent Support	Interface for connecting proprietary in-house agents.	Enables the use of agents trained on internal sensitive data behind a firewall.
Standardized Logging	Unified format for agent "thought processes" and tool calls.	Simplifies auditing and compliance for highly regulated industries.
Tool Orchestration	Standardized way for agents to request terminal/file access.	Provides a consistent security model for granting agent permissions.

Practical Implementation Patterns and Recommendations
For organizations looking to transition from "vibe coding" to "agentic engineering" in 2026, the following patterns are recommended based on current best practices:

Pattern 1: The "Handoff" Integration

This pattern is the most common for teams already using Claude Code.

Action: Use Claude Code for the /specify and /validate commands to build the technical foundation.

Handoff: Export the plan.md into a JetBrains Air Task.

Execution: Assign "high-risk" implementation tasks (e.g., refactoring core libraries) to agents within JetBrains Air using the Docker execution mode to ensure zero side effects on the local machine.   

Pattern 2: Multi-Agent Parallelism for Legacy Modernization

Legacy codebases often require simultaneous updates to documentation, test suites, and the code itself.

Action: Open the legacy project in JetBrains Air.

Execution: Dispatch three parallel tasks:

Agent A (Codex): Analyzes the legacy Java code using Air’s symbol resolution to generate a modern OpenAPI specification.   

Agent B (Claude): Implements the new Kotlin version of the service in a separate Git Worktree.   

Agent C (Junie): Generates integration tests using the IDE’s debugger state to identify edge cases in the legacy data flow.   

Pattern 3: Adversarial Debugging and Verification

For critical security or performance updates, multiple agents should verify each other's work.

Action: Define a "Verification Task" in JetBrains Air.

Execution: Run the task through two different agents (e.g., Claude and Gemini). Air allows you to "compare outputs side-by-side".   

Review: Use the IDE's built-in Static Analysis and Vulnerability Scanning to automatically flag any issues introduced by either agent before they are even presented for human review.   

Honest Assessment: Current Limitations and Gaps
While JetBrains Air and the 2026 agentic ecosystem are transformative, they are not without significant maturity gaps that engineering leaders must account for.

Platform and Reliability Issues

OS Fragmentation: As of early 2026, Air is a macOS-first tool. While Windows and Linux support is planned, many enterprise backend teams remain excluded from the ADE experience in the short term.   

"Fleet" Legacy Concerns: Air inherits its architecture from Fleet, a tool that spent years in preview without ever reaching the stability of the core IntelliJ platform. Some users report that Air can be resource-heavy, with high RAM usage that can impact the performance of other local development tools.   

Agent Failure Modes: Despite the advanced orchestration, agents still fail. "Task Drift" is a common problem where an agent, given a multi-step plan, begins to hallucinate after the fifth or sixth step. Air provides snapshots to help recover, but the human must still be vigilant in identifying when an agent has "lost the plot".   

Economic and Workflow Friction

The "Context Tax": Running multiple sophisticated agents concurrently is expensive. While JetBrains Air’s BYOK model is transparent, the token costs for a complex feature can easily reach hundreds of dollars in a single afternoon if agents enter "infinite loops" of trying to fix unfixable bugs.   

Integration Gaps: Air currently lacks deep integration with non-code tools like Jira, Slack, or Linear. While it supports MCP for external data, the "workflow loop" often breaks down when moving from an issue tracker to the ADE.   

Learning Curve: Transitioning from writing code to orchestrating agents requires a fundamental shift in mindset. Many senior developers find the process of "guiding an agent" to be more frustrating than just doing the work themselves, leading to a "resistance to adoption" in some highly specialized teams.   

Conclusion: The Path Toward Industrialized Software Production
JetBrains Air is more than just a new tool; it is the physical manifestation of the industry's shift toward "agentic engineering". By providing the semantic depth, isolated execution, and centralized orchestration that CLI-based tools lack, Air enables a level of rigor and scale that was previously impossible.   

The analysis concludes that Air is not a replacement for Claude Code, but its essential completion. Claude Code provides the "reasoning" and "planning" necessary to navigate complex human requirements, while JetBrains Air provides the "environment" and "tooling" necessary to execute those plans with the safety and precision required for production-grade software.   

For organizations navigating this transition, the strategy is clear: standardize on the Agent Client Protocol to preserve model flexibility, adopt a "Spec-First" Momentum workflow to ensure intent, and utilize the Agentic Development Environment to move from experimental code generation to industrialized software production. The era of "vibe coding" is over; the era of the agentic system has begun.   


