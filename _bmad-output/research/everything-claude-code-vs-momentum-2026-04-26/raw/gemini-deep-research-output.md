---
content_origin: gemini-deep-research
date: 2026-04-26
topic: "everything-claude-code vs Momentum — comparative analysis"
method: cmux-browser + chrome-mcp (DOM walker markdown reconstruction)
source_url: https://gemini.google.com/app/86668a7bd7fdd717
sub_question: "Baseline triangulation reference (low authority)"
disputed: true
---

> **STATUS — DISPUTED INPUT**
>
> Subagent verification (Phase 2, 2026-04-26) found multiple factual inaccuracies in this file. Do **not** treat body claims as primary source. Specific confirmed errors:
>
> - **`tools/agentshield/` does not exist in ECC.** AgentShield is a sibling npm package (`affaan-m/agentshield`), not an in-repo directory. (CRITICAL-001)
> - **`qflow` MCP server does not exist in ECC.** No match in 2,662-entry recursive tree scan. (CRITICAL-002)
> - **`claude-mem` is not part of ECC.** The most-starred `claude-mem` (`thedotmack/claude-mem`) is a distinct project by a different author; ECC's actual memory system is `continuous-learning-v2`. Claimed 89K stars and Bun/Chroma implementation details are unverified fabrications. (CRITICAL-003)
> - **The `claude-mem` adoption recommendation** (Critical Components §1) is built on the above fabrication and should be disregarded. (CRITICAL-004)
> - **Stale community stats:** "140K+ stars / 21K+ forks / 113 contributors / 768 commits" — live GitHub API 2026-04-26 shows 167,488 / 25,969 / 159 / ~1,465. (HIGH-003, HIGH-016)
> - **Hackathon attribution wrong:** "Anthropic x Forum Ventures hackathon in late 2025" — verified event is Cerebral Valley × Anthropic "Built with Opus 4.6" hackathon, Feb 10–16, 2026. Note: Forum Ventures was the sponsor for Affaan's earlier project `zenith.chat` (Sep 2025), not for ECC. (HIGH-004)
> - **MCP count "14"** is wrong in both directions: `.mcp.json` ships 6 servers; the catalog `mcp-configs/mcp-servers.json` lists 24+. (HIGH-005)
> - **`retro` skill mapped to "Stop hook pattern"** — verified state: ECC has zero retrospective analogue. (HIGH-006)
> - **`avfl` mapped to "AgentShield / Red-Blue Team"** — AgentShield is external; verified ECC analogues are `santa-method` and `verification-loop`. (HIGH-007)
> - **`.opencode/dist/index.js`** does not exist; actual path is `.opencode/index.ts`. (HIGH-013)
> - **`--target opencode`** is not a verified `install.sh` flag; actual targets are `claude`, `cursor`, `antigravity`. (HIGH-015)
>
> **All body claims below are [UNVERIFIED] unless cross-confirmed by a subagent file.**
> Verified findings are in: `research-architecture-capabilities.md`, `research-maturity-community.md`, `research-feature-parallels.md`, `research-ecc-superior.md`, `research-momentum-superior.md`, `research-portability.md`, `research-philosophy.md`, `research-integration-assessment.md`.

# Architectural Evaluation and Comparative Analysis of Agentic Engineering Frameworks: Everything Claude Code vs. Momentum

The landscape of agentic engineering in 2026 has transitioned from experimental prompting to the establishment of robust, production-grade harnesses that govern the behavior of autonomous coding agents. As large language models—specifically the Claude 3.7 and 4.0 iterations—attain greater reasoning density, the primary bottleneck for software development teams has shifted from code generation capability to workflow orchestration, state management, and security enforcement. Within this paradigm, the `affaan-m/everything-claude-code` (ECC) ecosystem has emerged as a dominant, community-driven toolkit, reaching over 140,000 GitHub stars and 21,000 forks. This report provides a comprehensive technical comparison between ECC and Momentum, an opinionated agentic engineering practice module, to determine the strategic feasibility of integration, adaptation, or continued independent trajectory.   

## Technical Architecture and Repository Composition

The `affaan-m/everything-claude-code` repository is characterized by its "Plugin-Everything" architecture, a design philosophy where every capability—from memory management to security scanning—is abstracted behind a modular interface. This structure allows the system to remain agnostic to the specific agentic CLI being utilized, providing a unified surface for Claude Code, Codex, OpenCode, and Cursor.   

### Structural Layout and Language Ecosystems

The ECC repository employs a sophisticated directory structure designed to facilitate selective installation and cross-platform compatibility. Unlike monolithic configurations, ECC utilizes a manifest-driven pipeline where users can install specific components tailored to their technology stack.   

| Directory Path | Contents and Functional Significance | Primary Technology Stack |  |
| `.claude-plugin/` | 

Contains `plugin.json` and `marketplace.json` for integration with the official Claude Code plugin ecosystem. 

 | JSON, Metadata |  |
| `agents/` | 

Houses 48 specialized agent definitions, such as `planner`, `architect`, and `tdd-guide`. 

 | Markdown + YAML Frontmatter |  |
| `skills/` | 

Contains 183 "canonical workflow surface" definitions for tasks like refactoring and testing. 

 | Markdown, Shell Scripts |  |
| `hooks/` | 

Event-driven logic for `PreToolUse`, `PostToolUse`, `SessionStart`, and `SessionEnd`. 

 | Node.js, JSON |  |
| `mcp-configs/` | 

Pre-built Model Context Protocol (MCP) server configurations for 14 external integrations. 

 | JSON |  |
| `scripts/` | 

Installation utilities, package manager detection logic, and cross-platform adapters. 

 | Node.js, Shell |  |
| `tests/` | 

Unit and integration tests for the harness itself, ensuring config stability. 

 | TypeScript, Jest |  |
| `tools/agentshield/` | 

Proprietary security scanning engine with over 1,282 automated tests. 

 | TypeScript, Python |  |

   

The repository relies heavily on Node.js for its internal automation scripts, ensuring that hooks and installation logic remain performant across macOS, Linux, and Windows environments. The selective install system uses a SQLite state store to track installed components, allowing for incremental updates and dependency management across the 12 supported language ecosystems, including TypeScript, Python, Go, Rust, Java, Kotlin, and C++.   

### Core Component Capabilities

At the code level, ECC ships specialized logic that transforms a standard terminal agent into a multi-role engineering team. The `agents/` directory is the most critical folder, containing Markdown files that define the persona, tool access, and model constraints for each subagent. For example, the `planner.md` agent is explicitly instructed to focus on requirement analysis and architecture review before any code is generated, utilizing only `Read`, `Grep`, and `Glob` tools to prevent premature editing.   

The `skills/` directory serves as the "durable logic" layer. While slash commands are often used for quick triggers, ECC advocates for storing broader workflow definitions as skills within `~/.claude/skills/`. These skills often include "codemaps"—structured representations of the codebase that allow the agent to navigate thousands of files without consuming excessive tokens through exploratory searches.   

## Maturity and Community Traction Analysis

The maturity of ECC is reflected not only in its star count but in its contributor velocity and integration into the broader AI developer ecosystem. Since its inception as a winner of the Anthropic x Forum Ventures hackathon in late 2025, the project has maintained a rigorous release cadence.   

### Contributor Velocity and Release History

The project transitioned into a community-led model in early 2026, currently boasting 113 contributors and over 768 commits. The release of version 1.9.0 in March 2026 introduced the "selective-install architecture," which solved the issue of "config bloat" where users were forced to load dozens of unnecessary agents. By April 2026, version 1.10.0 shifted focus toward "Operator Workflows" and the alpha release of ECC 2.0—a Rust-based control plane prototype designed to manage multiple agent sessions simultaneously.   

| Metric | Everything Claude Code (April 2026) | Significance for Momentum |  |
| **Stars** | 

140,000+ 

 | High social proof and community validation. |  |
| **Forks** | 

21,000+ 

 | Significant downstream customization and enterprise adoption. |  |
| **Contributors** | 

113 

 | Diversified maintenance risk; robust peer review. |  |
| **Release Frequency** | 

Monthly Major / Weekly Minor 

 | High velocity; rapid response to Anthropic API updates. |  |
| **Issue Throughput** | 

145 open enhancements 

 | Active community engagement but growing backlog. |  |

   

### Ecosystem Sentiment and Industry Adoption

Community signals suggest that ECC is viewed as a production-grade framework rather than a "README-only" project. It has been cited in blog posts by major AI dev-tool players like Augment Code and Taskade, and it is a recurring topic on Reddit's `/r/AI_Agents` and Hacker News. The project’s security guide and AgentShield tool have specifically garnered attention as a "firewall" against the $25 million problem of autonomous agents deleting production databases or leaking credentials.   

However, the project is not without its limitations. Tech leads have reported that unoptimized setups can lead to agents that are "900x slower" if they rely on text-based grep searches instead of Language Server Protocol (LSP) integrations. This gap indicates that while ECC provides the *harness*, it still requires expert-level configuration of the underlying environment to reach peak efficiency.   

## Direct Feature Parallels with Momentum

Mapping the capabilities of ECC against Momentum reveals a high degree of functional overlap, although the implementation strategies differ between a "toolkit" approach and a "practice" approach.

### Workflow and State Management

Both systems aim to introduce structure to the often-chaotic agentic development cycle. Momentum utilizes a file-based state machine centered on `index.json` files within `sprints/` and `stories/` directories. ECC approaches this through a combination of specialized agents and the `qflow` MCP server.

| Momentum Feature | ECC Equivalent / Analogue | Technical Implementation in ECC |  |
| `sprint-planning` skill | 

`planner` agent 

 | 

Uses `Plan Before Execute` principles to generate Markdown plans. 

 |  |
| `avfl` (Adversarial Loop) | 

`AgentShield` / Red-Blue Team 

 | 

Multi-agent pipeline for adversarial analysis of configurations. 

 |  |
| `retro` skill | 

`Stop` hook pattern 

 | 

Auto-summarization of successes/failures at session end. 

 |  |
| `create-story` command | 

`qflow` MCP server 

 | 

7-state machine and dependency DAG for task management. 

 |  |
| `index.json` state machine | 

`SQLite` state store 

 | Persistent local database for session and task tracking. |  |
| `Gherkin/ATDD` specs | 

`tdd-guide` / Spec-driven tools 

 | 

Mandatory "Red-Green-Improve" cycle for implementation. 

 |  |
| `impetus` orchestrator | 

`opus` coordinator 

 | 

Primary coordinator that delegates to specialized specialists. 

 |  |

   

ECC lacks a direct native equivalent for Momentum's "intake-queue" (intake-queue.jsonl) or the specific "decision document" taxonomy, though these are often handled by community-contributed skills like `prp-plan`. Momentum’s "epic/feature grooming" is mirrored by the `architect` and `planner` agents in ECC, but ECC tends to be less prescriptive about the specific file formats used for these stages.   

### Memory and Persistence Systems

One of the most profound parallels is in memory persistence. Momentum uses a persistent file-based memory at `~/.claude/projects/.../memory/`. ECC has evolved this into `claude-mem`, a plugin that reached 89,000 stars in early 2026. Unlike Momentum’s flat files, `claude-mem` uses a background HTTP API managed by Bun and stores data in a SQLite database with Chroma vector support for semantic search. This allows ECC to implement "Progressive Disclosure," where Claude first loads a compact index of previous sessions and only drills down into specific observation IDs when relevant, saving significant token costs compared to loading full memory files.   

## Superior Features and Ergonomics of Everything Claude Code

While Momentum offers a deep engineering practice, ECC provides several ergonomic and technical features that represent significant UX wins.

### Selective Installation and Onboarding

The most notable UX improvement in ECC is its manifest-driven installation via the Claude Code plugin marketplace. Users can run `/plugin install everything-claude-code@everything-claude-code` to get a baseline setup immediately. The selective install pipeline ensures that a developer working in Rust is not burdened with 30 Python-specific agents or skills, a common failure point in early agentic harnesses that led to context window exhaustion.   

### Hookify and Conversational Configuration

ECC ships the `hookify` plugin, which allows developers to create behavior-enforcing hooks through natural language conversation. Instead of manually editing `settings.json` with complex JSON and shell commands, a user can tell the agent, "I want a hook that runs Pyright every time I edit a Python file and blocks the commit if there are errors". The `hookify` agent then generates and installs the necessary scripts and config. This "natural language to structured config" pattern is a major advantage for onboarding and maintaining team standards.   

### Continuous Learning and Instinct Extraction

ECC’s "Continuous Learning (v2)" system is a standout feature Momentum currently lacks. This system automatically extracts patterns from development sessions into reusable "instincts". These instincts carry confidence scores and can eventually evolve into full-fledged skills. For instance, if the agent repeatedly corrects an error-handling pattern in a specific legacy codebase, the learning system will promote that correction to an "Instinct" that is automatically loaded in future sessions, effectively allowing the agent to "learn" a team’s unique coding conventions without manual documentation updates.   

### Advanced Security and Sandboxing

The security posture of ECC is notably more robust than the standard Claude Code installation or Momentum's current gate-based approach. The inclusion of `AgentShield` and the `--opus` flag for red-teaming allows teams to simulate attacks against their own harness configurations. Furthermore, ECC advocates for "Sandboxed Subagents," where specific tools (like `Edit` or `Bash`) are restricted for certain agents. A `security-reviewer` agent in ECC might be given `Read` and `Grep` access but no ability to modify files, preventing "accidental destructive actions" during an audit.   

## Areas of Momentum Superiority

Despite the breadth of ECC, Momentum maintains a conceptual and implementation depth in specific areas of the professional engineering lifecycle that ECC treats as secondary.

### Engineering Practice Rigor and Methodology

Momentum’s primary advantage is that it is a *practice* first and a *toolkit* second. While ECC provides 48 agents, Momentum provides a structured "Engineering Team" methodology that includes specific gates like `plan-audit` and `avfl` (Adversarial Validate-Fix Loop).

- 

**AVFL Depth:** Momentum’s AVFL is a dedicated multi-agent loop that employs an "enumerator" and an "adversary" lens to validate code [Context on Momentum]. While ECC has red-team/blue-team concepts in `AgentShield`, these are primarily for security configuration, not for the validation of business logic in every feature.   

- 

**Gherkin/ATDD Integration:** Momentum’s reliance on Gherkin for acceptance specs provides a level of behavioral rigor that ECC’s Markdown-based `planner` does not enforce. In Momentum, the spec is the truth, and the agent is bound by it through the state machine.

- 

**Sprint State Machine:** Momentum’s use of `index.json` files for state transitions provides a deterministic audit log of development progress [Context on Momentum]. In ECC, task management is often delegated to an external MCP like `qflow`, which introduces a dependency on a separate repository and may lack the same "file-as-truth" integration that Momentum provides.   

### Taxonomic Clarity in Project Management

Momentum’s taxonomy—specifically the differentiation between "Epic Grooming," "Feature Grooming," and "Intake"—is more aligned with enterprise software development lifecycle (SDLC) standards. ECC’s approach is more role-based (TPM, Designer, Developer) but less process-bound. Momentum’s "Intake Queue" (intake-queue.jsonl) provides an event log of requirements that is superior for teams needing to trace why a specific architectural decision was made months after the fact.   

## Portability Across Agentic CLIs

A critical question for the future of Momentum is how it handles the fragmentation of the agentic CLI market. ECC has a significant lead in this area, having been designed from the outset as a "Cross-Harness" system.   

### The AGENTS.md Standard

ECC is a primary driver of the `AGENTS.md` open standard, which is now used by over 60,000 projects. This standard allows agents to be portable across Claude Code, Codex, and Gemini CLI. ECC provides a "unified identity" layer where the same agent definitions are used regardless of the underlying harness.   

| Harness Support | ECC Implementation Strategy | Portability Status |  |
| **Claude Code** | 

Native plugin marketplace support and `~/.claude/` configs. 

 | Native / Full |  |
| **Cursor** | 

`.cursor/` adapters that reuse Claude Code hook logic. 

 | High (via Adapter) |  |
| **Codex** | 

Dedicated `.codex/` plugin with a "thinner" implementation. 

 | Moderate |  |
| **OpenCode** | 

Supports 11 hook events and 6 native custom tools. 

 | High |  |
| **Aider / Goose** | 

Portable `AGENTS.md` and `SKILL.md` definitions. 

 | Theoretical / Via Standard |  |

   

ECC’s architecture uses a "DRY" (Don't Repeat Yourself) adapter pattern, where hook scripts are written in Node.js and shared across all platforms. This means a team can use Claude Code in the terminal for heavy refactoring and switch to Cursor for UI work without losing their security hooks or custom rules. Momentum’s current strategy is heavily optimized for the Claude Code plugin marketplace, which may limit its reach as developers explore alternatives like OpenCode or Goose to avoid model lock-in.   

## Design Philosophy and Pedagogical Comparison

The divergence between ECC and Momentum is most apparent in their underlying philosophy regarding how humans should interact with AI "workers."

### Toolkit vs. Practice

ECC is fundamentally a **Toolkit**. It assumes the developer is the "manager" who needs a high-performance set of tools to be more effective. Its philosophy is built on "Agent-First" delegation, where work is routed to the appropriate specialist as early as possible. It provides flexibility over convention, encouraging users to "remove what you don't use".   

Momentum is a **Practice**. It teaches a specific way of doing engineering. It treats the AI agents as peers that must be governed by strict protocols (Gherkin, Sprints, AVFL). It is highly opinionated, prioritizing "Process Depth" over "Toolkit Breadth." It focuses on the "Gradual Release of Responsibility" framework, where the AI moves from a "Guide" to a "Peer" as it learns the codebase.   

### Governance and Target Audience

ECC’s governance is community-driven and decentralized. While Affaan Mustafa is the primary maintainer, the 113 contributors and thousands of forks suggest an ecosystem that thrives on diversity of thought. Its target audience is broad, ranging from solo developers and hobbyists to enterprise teams seeking to "harden" their AI setups.   

Momentum targets the "Professional Engineering Team." Its target user is a tech lead or senior developer who wants to implement a standardized, auditable, and repeatable process across a team. Momentum’s pedagogy is explicit: it doesn't just give you a tool to do a retro; it enforces a retro at the end of every sprint because that is what a high-functioning team *does* [Context on Momentum].

## Integration Assessment and Strategic Recommendations

The comparative analysis suggests that while Momentum should remain on its current trajectory as an opinionated engineering practice, there are specific architectural patterns and components from ECC that would significantly enhance Momentum’s utility.

### Critical Components for Adoption

Integrating specific pieces of ECC into Momentum would solve several of the current limitations identified in Momentum’s file-centric architecture.

1. 

**Adopt the `claude-mem` Architecture:** Momentum’s flat-file memory should be upgraded to a SQLite-based system. This would allow Momentum to handle significantly larger projects without hitting context limits. Specifically, Momentum should adopt ECC’s "Three-Layer Retrieval" (Index, Timeline, Full Details) to reduce token consumption.   

1. 

**Fork and Modify `AgentShield` for AVFL:** Momentum’s AVFL could be significantly hardened by integrating the 1,282 security tests from ECC’s `AgentShield`. This would transform AVFL from a "logic validator" into a "security and logic validator".   

1. 

**Implement the `Hookify` Pattern:** Momentum should provide a conversational way for tech leads to define project-specific rules. Integrating a "Momentum-Hook-Agent" that behaves like ECC’s `hookify` would make it easier for teams to enforce their unique coding standards.   

1. 

**Standardize on `AGENTS.md`:** To ensure Momentum is not trapped in the Claude Code ecosystem, it must adopt the `AGENTS.md` standard for its subagents. This will allow Momentum users to carry their "Sprint-Dev" and "Planner" personas into other tools like Cursor or OpenCode.   

### Potential Conflicts and Migration Costs

Integrating ECC as a whole would conflict with Momentum's philosophy. ECC is designed to be a "Performance Optimization System," whereas Momentum is a "Process Management System".   

- 

**Architectural Conflict:** ECC relies on a background worker service (managed by Bun) for its memory and state. Momentum’s "file-as-truth" approach is simpler but less scalable. Moving to a worker service model would increase the "installation surface" and could alienate users who prefer zero-dependency tools.   

- 

**Philosophical Conflict:** ECC’s "Specialist for Everything" (48 agents) contradicts Momentum’s "Core Team" approach. Momentum should resist the urge to add dozens of agents, as this has been shown to confuse routing and deplete context unnecessarily.   

### Concrete Recommendations

| Action | Recommendation | Justification |  |
| **Adopt-as-is** | `AGENTS.md` Root Standard | 

Industry standard for portability; zero cost to implement. 

 |  |
| **Adopt-with-modification** | `claude-mem` SQLite Layer | 

Essential for scaling Momentum to large enterprise codebases. 

 |  |
| **Watch-and-learn** | ECC 2.0 Rust Control Plane | 

If Momentum needs to manage 10+ parallel agents, a Rust daemon will be necessary. 

 |  |
| **Ignore** | 183 General-Purpose Skills | 

Momentum’s opinionated skills are its unique value proposition; "everything" is too much. 

 |  |
| **Fork** | `AgentShield` Ruleset | 

Highly valuable security logic that can be integrated into Momentum’s AVFL. 

 |  |

   

## Honest Assessment of Limitations in Everything Claude Code

While ECC is a tour de force of community engineering, it suffers from several critical gaps that Momentum is well-positioned to fill.

1. 

**Context Exhaustion through Agent Bloat:** Loading 48 agents consumes a massive amount of "routing tokens" before the user even enters a prompt. ECC’s solution is "Selective Installation," but this still requires the user to know which 5-10 agents they need. Momentum’s "Core Team" approach is more predictable and token-efficient.   

1. 

**Invisibility of Server-Side Inflation:** Research into Claude Code v2.1.100 (which many ECC users use) shows that certain versions introduce 20,000 "invisible tokens" on the server side, depleting quotas 40% faster. ECC’s focus on *more* configurations may exacerbate this problem if users are not careful with version pinning.   

1. 

**Lack of Formal Verification:** ECC uses `pass@k` metrics to measure skill effectiveness, but it lacks the "Adversarial Checkpoint" rigor of Momentum’s AVFL. ECC agents often "vibe code"—they follow the instructions but may not verify them against a formal behavioral spec like Gherkin.   

1. 

**Complex Configuration Surface:** Despite the `hookify` and `plugin` systems, ECC is still complex. The longform guide covers "Token Economics" and "Parallelization Strategies" that are daunting for the average developer. Momentum’s "Practice" approach abstracts this complexity into a familiar Sprint workflow.   

## Final Synthesis and Strategic Outlook

The analysis concludes that `affaan-m/everything-claude-code` represents the current pinnacle of **Agentic Tooling Efficiency**, while Momentum represents the pinnacle of **Agentic Engineering Discipline**. For Momentum to remain competitive and relevant in 2026, it must adopt the "Tooling Infrastructure" of ECC—specifically the SQLite memory systems and cross-platform standards—while doubling down on its "Methodological Rigor."

Momentum should view ECC as a source of high-quality "spare parts." By harvesting the memory persistence logic, the security rules, and the conversational configuration patterns from ECC, Momentum can build a "Professional Grade" harness that is both technically superior to standard Claude Code and process-superior to the "Everything" model. The ultimate goal should be a system that provides the *scalability* of ECC with the *certainty* of Momentum. This "Hybrid Strategy" will ensure that Momentum remains the "operating system of choice" for teams that value engineering excellence over sheer quantity of AI capabilities.
## Follow-Up #1 — Verifications request (Gemini sidestepped)

**Question asked:** Verify the metric numbers (140K stars, 21K forks, 113 contributors, 768 commits, 1,282 tests, 48 agents, 183 skills, 14 MCP integrations, 12 language ecosystems) against the actual current state of the affaan-m/everything-claude-code repo. Was the Anthropic x Forum Ventures hackathon a real event?

**Response:**

As requested, here are the canonical source URLs and verification for the specific claims and models referenced in the report:

1. **ForgeCode's "TermBench 2.0" score of 81.8%:**

**URL:** [https://forgecode.dev/](https://forgecode.dev/)

The official ForgeCode homepage lists an 81.8% accuracy rate on TermBench 2.0, identifying it as the top-ranked coding harness on the leaderboard. This score was achieved using both GPT-5.4 and Claude 4.6 Opus.
2. **ForgeCode's ZSH plugin mode with ":" prefix:**

**URL:** [https://github.com/tailcallhq/forgecode](https://github.com/tailcallhq/forgecode)

The official repository documentation details the ZSH Plugin Mode, explaining that lines starting with the `:` prefix are intercepted by the shell and routed directly to the ForgeCode agent.
3. **OpenCode's "75+ providers" claim:**

**URL:** [https://github.com/sst/opencode](https://github.com/sst/opencode)

As the primary repository for the tool, this page hosts the model-agnostic framework that supports 75+ LLM providers, including OpenAI, Anthropic, Google, and various local model endpoints.
4. **The "opencode-workflows" plugin and its JSON-defined DAG workflow support:**

**URL:** [https://github.com/mark-hingston/opencode-workflows](https://github.com/mark-hingston/opencode-workflows)

This official plugin repository specifies support for defining deterministic, multi-step processes (Directed Acyclic Graphs or DAGs) using JSON, YAML, or TypeScript.
5. **The "Bifrost" gateway and its microsecond-level performance claims:**

**URL:** [https://github.com/maximhq/bifrost](https://github.com/maximhq/bifrost)

The official README for the Bifrost gateway highlights its microsecond-level performance, specifically noting that it adds only 11 µs of overhead per request during sustained benchmarks at 5,000 requests per second.

### Verification of Model Releases

Both primary models referenced in the report are actual released models as of today, April 21, 2026:

- **GPT-5.4:** Released by OpenAI on March 5, 2026.
- **Claude 4.6 Opus:** Officially released by Anthropic on February 5, 2026. (Note: Anthropic has since released a successor, Claude Opus 4.7, on April 16, 2026).
**Orchestrator note:** Gemini did NOT verify the ECC numbers in this follow-up. Instead it provided verifications for unrelated tools (ForgeCode, OpenCode, Bifrost) and AI model releases. This strongly suggests the original ECC numbers may be hallucinated. Subagents in Phase 2 must verify against the live GitHub repo.

## Follow-Up #2 — Cross-CLI portability

**Question asked:** Concretely, how does ECC actually support non-Claude-Code agentic CLIs (Codex, OpenCode, Cursor, Goose, Aider)? Is there an explicit adapter, installer flag, or format converter? Please cite specific file paths in the repo.

**Response:**

Concretely, `affaan-m/everything-claude-code` (ECC) supports non-Claude-Code agentic CLIs through a multi-layered technical architecture consisting of a target-aware installer, dedicated tool-specific adapter directories, and a universal configuration standard.

### **1. Target-Aware Installer Flags**

The ECC repository includes an intelligent installer that uses the `--target` flag to remap its directory structure and file formats to match the specific expectations of different agentic CLIs.

- 

**Flag usage:** `./install.sh --target <cli-name>`

- 

**Verified Targets:**

- 

`--target cursor`: Installs configurations into the `.cursor/` directory.

- 

`--target antigravity` (Codex): Remaps ECC components to the `.agent/` directory structure used by Antigravity-based Codex setups.

- 

`--target opencode`: Deploys dedicated plugin files into the `.opencode/` directory.

### **2. Explicit Adapters and File Converters**

ECC is not merely a collection of prompts; it contains functional code designed to bridge the gap between different tool runtimes.

- 

**Cursor Adapter:** The file `.cursor/hooks/adapter.js` is a "DRY adapter" that transforms Cursor's stdin JSON format to match Claude Code's hook format. This allows the same Node.js hook scripts located in `scripts/hooks/*.js` to execute across both tools without modification.

- 

**Format Mapping:** When using the `--target antigravity` flag, the installer automatically performs the following remapping:

- 

ECC `/commands/*.md` are moved to `.agent/workflows/`.

- 

ECC `agents/*.md` definitions are mapped to `.agent/skills/`.

- 

Rules are "flattened" from ECC's nested directory structure (e.g., `rules/common/`) into a flat `.agent/rules/` directory required by Antigravity.

- 

**State Tracking:** The file `ecc-install-state.json` is generated at the project root to track which target is active and manage incremental updates for that specific CLI.

### **3. Explicit Tool-Specific Directories**

The repository structure contains dedicated, hidden directories that house the "thinner" implementations for non-Claude-Code tools :

- 

`.cursor/`: Contains `hooks/adapter.js` and `agents/*.md` specifically for Cursor.

- 

`.opencode/`: Houses the OpenCode-specific plugin entry point (`dist/index.js`) and tool-specific manifests.

- 

`.codex/` and `.codex-plugin/`: Contains configurations and reference tables optimized for the Codex CLI.

- 

`.gemini/`, `.kiro/`, `.trae/`, and `.codebuddy/`: Emerging directories for other 2026-era agentic harnesses.

### **4. Cross-Tool Standards (AGENTS.md)**

ECC relies on the `AGENTS.md` open standard located at the repository root as the "universal cross-tool file." This file is designed to be read by Claude Code, Cursor, Codex, and OpenCode, providing a shared identity and governance layer that functions across all four harnesses.

### **5. Status of Aider and Goose**

While the repository is marketed as "agnostic," support for Aider and Goose is currently described as "aspirational" or "thinner" compared to the core Claude Code and Cursor integrations. These tools primarily receive support through the root-level `AGENTS.md` and `SKILL.md` definitions rather than having dedicated adapter scripts like Cursor.

**Summary of Key File Paths:**

- 

`install.sh`: The main entry point supporting the `--target` flag.

- 

`.cursor/hooks/adapter.js`: The functional bridge for Cursor event hooks.

- 

`.opencode/dist/index.js`: The entry point for OpenCode plugin support.

- 

`AGENTS.md`: The universal cross-CLI instruction file.

- 

`scripts/install-plan.js`: The Node.js logic that handles profile and target resolution.
## Follow-Up #3 — Directory structure verification (skipped)

**Question asked:** Concrete top-level directory listing of the actual repo, with one-line descriptions per top-level item.

**Disposition:** Gemini dropped follow-up #3 into Deep Research plan mode (would have required another full research cycle). Skipped because SQ1 — Architecture & Capabilities subagent has already independently verified the directory structure. See **`research-architecture-capabilities.md` → Directory Layout** for the authoritative enumeration (48 agents, 183 skills, 79 commands, 89 rules, 40 hooks, 6 default MCP servers, parallel manifests for Codex/Cursor/OpenCode/Gemini, plus Rust ECC 2.0 control plane and Python Tkinter dashboard).

---

## Sources

- Gemini Deep Research session: https://gemini.google.com/app/86668a7bd7fdd717 (2026-04-26)
- Follow-Up #1 cited URLs (out-of-scope; included for traceability):
  - https://forgecode.dev/
  - https://github.com/tailcallhq/forgecode
  - https://github.com/sst/opencode
  - https://github.com/mark-hingston/opencode-workflows
  - https://github.com/maximhq/bifrost
- For verified ECC facts, see the subagent research files in this corpus (all dated 2026-04-26).
