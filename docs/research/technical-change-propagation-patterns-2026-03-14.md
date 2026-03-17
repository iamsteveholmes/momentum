# Change Propagation Patterns for Interconnected Specification Documents

**Date:** 2026-03-14
**Research Type:** Technical Research (Enumerator framing)
**Confidence Baseline:** Each finding rated HIGH/MEDIUM/LOW based on source quality

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Taxonomy of Change Propagation Approaches](#2-taxonomy-of-change-propagation-approaches)
3. [Dependency Graph Patterns (Build Systems, Package Managers, Databases)](#3-dependency-graph-patterns)
4. [Document Dependency Management (Sphinx, Docusaurus, MkDocs)](#4-document-dependency-management)
5. [Event-Driven Document Updates](#5-event-driven-document-updates)
6. [Git-Based Change Detection](#6-git-based-change-detection)
7. [Requirements Management Tools (DOORS, Jama, Polarion)](#7-requirements-management-tools)
8. [AI-Assisted Change Propagation](#8-ai-assisted-change-propagation)
9. [Graph Database Approaches](#9-graph-database-approaches)
10. [Staleness Detection](#10-staleness-detection)
11. [Synthesis: Applicability to Markdown Spec Chains](#11-synthesis-applicability-to-markdown-spec-chains)
12. [Recommended Architecture for Momentum](#12-recommended-architecture-for-momentum)
13. [Sources Index](#13-sources-index)

---

## 1. Executive Summary

This research enumerates all known approaches to propagating changes through interconnected documents, applied to the Momentum use case: a chain of markdown specification documents (Research -> Brief -> PRD -> Architecture -> Epics -> Stories -> Implementation) managed by AI agents in a git repository.

Eight distinct strategy families were identified, each with transferable patterns:

| Strategy Family | Core Mechanism | Applicability to Momentum |
|---|---|---|
| Dependency Graphs (DAG) | Content hashing + topological ordering | HIGH - foundational |
| Document Cross-References | Named targets + build-time validation | MEDIUM - partial fit |
| Event-Driven / CDC | Pub/sub on change events | MEDIUM - for orchestration |
| Git-Based Detection | Diff analysis + hooks | HIGH - native to workflow |
| Requirements Traceability | Suspect links + impact analysis | HIGH - direct analog |
| AI Semantic Analysis | LLM-based change understanding | HIGH - core differentiator |
| Graph Databases | Relationship traversal + impact queries | MEDIUM - modeling power |
| Staleness Detection | Hash comparison + freshness thresholds | HIGH - simple and effective |

The recommended approach for Momentum combines: (1) a lightweight dependency manifest embedded in document frontmatter, (2) git-based change detection via content hashing, (3) a suspect-link mechanism inspired by DOORS/Jama/Polarion, and (4) AI agents performing semantic diff to determine whether upstream changes materially affect downstream documents.

---

## 2. Taxonomy of Change Propagation Approaches

### 2.1 Reactive vs. Proactive

| Dimension | Reactive | Proactive |
|---|---|---|
| **Trigger** | Change occurs, system responds | System scans for potential staleness |
| **Examples** | Git hooks, CDC, event-driven | Scheduled freshness checks, CI validation |
| **Latency** | Near real-time | Periodic (minutes to days) |
| **Momentum fit** | Post-commit hooks trigger agent review | CI pipeline validates spec chain consistency |

**Source:** Reactive vs. proactive document control taxonomy from [DocBoss](https://www.docboss.com/blog/reactive-versus-proactive-document-control/)
**Confidence:** MEDIUM

### 2.2 Automated vs. Manual

| Dimension | Fully Automated | Human-in-the-Loop | Fully Manual |
|---|---|---|---|
| **Mechanism** | Cascading updates auto-applied | AI proposes, human approves | Human reviews and updates |
| **Risk** | Unintended cascade effects | Slower but safer | Inconsistency, missed updates |
| **Examples** | DB CASCADE, Bazel rebuild | DOORS suspect links + review | Ad-hoc document editing |
| **Momentum fit** | Low (specs need human judgment) | HIGH (ideal) | Fallback only |

**Source:** Cascading risks from [StackSync MySQL analysis](https://www.stacksync.com/blog/mysql-cascading-changes-and-best-practices); DOORS suspect link workflow from [IBM DOORS documentation](https://www.ibm.com/docs/en/engineering-lifecycle-management-suite/doors/9.7.2?topic=data-suspect-links-changed-objects)
**Confidence:** HIGH

### 2.3 Content-Aware vs. Content-Agnostic

| Dimension | Content-Agnostic | Content-Aware |
|---|---|---|
| **Mechanism** | Hash/timestamp comparison | Semantic analysis of what changed |
| **Granularity** | "File changed" (binary signal) | "Section X changed, meaning shifted from A to B" |
| **Examples** | Git SHA, Bazel content hash | LLM semantic diff, SemanticDiff tools |
| **Momentum fit** | First-pass filter | Second-pass for material changes |

**Source:** SemanticDiff concepts from [Martin Fowler](https://martinfowler.com/bliki/SemanticDiff.html); content hashing from [Bazel documentation](https://www.gocodeo.com/post/how-bazel-works-dependency-graphs-caching-and-remote-execution)
**Confidence:** HIGH

### 2.4 Push vs. Pull

| Dimension | Push (Notify) | Pull (Query) |
|---|---|---|
| **Mechanism** | Source pushes change events to subscribers | Consumer queries source for changes |
| **Examples** | CDC/Debezium, webhooks, pub/sub | Git diff polling, scheduled CI checks |
| **Momentum fit** | Git hooks push events | Agent queries git log for changes |

**Source:** Debezium CDC architecture from [Debezium.io](https://debezium.io/); event-driven architecture from [TMS Outsource](https://tms-outsource.com/blog/posts/event-driven-architecture/)
**Confidence:** HIGH

---

## 3. Dependency Graph Patterns

### 3.1 Build System Dependency Graphs (Bazel)

**How it works:**

Bazel constructs a Directed Acyclic Graph (DAG) mapping relationships between build targets, their inputs, outputs, tools, and dependencies. During a build of target X, Bazel inspects the entire transitive closure of dependencies to ensure changes are reflected, rebuilding intermediates as needed.

**Change detection mechanism:**

1. Each input file is hashed using cryptographic digests
2. Environment variables and toolchain versions are included in the cache key
3. Outputs are stored in a local Content Addressable Storage (CAS), indexed by content hashes
4. "Action keys" are derived from all inputs; if an action key matches a previous execution, the cached output is reused
5. The in-memory graph tracks dependencies and determines what needs recompilation

**Key optimization:** If the result of rebuilding an intermediate target is identical to the previous output (same content hash), the cascade stops -- downstream targets are not rebuilt. This prevents unnecessary "cascading re-builds" where a whole spine of the tree would be re-evaluated.

**Source:** [How Bazel Works: Dependency Graphs, Caching, and Remote Execution](https://www.gocodeo.com/post/how-bazel-works-dependency-graphs-caching-and-remote-execution); [Bazel Dependencies](https://bazel.build/concepts/dependencies)
**Confidence:** HIGH

**Transferable pattern for Momentum:** Model the spec chain as a DAG. Each document node has a content hash. When a document changes, walk the graph forward (topologically sorted) to identify all downstream dependents. Compare hashes to determine if the upstream change actually produced a materially different output, potentially short-circuiting the cascade.

### 3.2 Package Manager Dependency Resolution (npm, Cargo)

**How it works:**

Package managers resolve version constraints across a dependency tree. npm uses a "Newest Version Selection" strategy by default, while Cargo (like Bazel's Bzlmod) uses Minimal Version Selection (MVS) for deterministic resolution.

**Transitive dependency propagation:** Installing a package pulls in all transitive dependencies. When a transitive dependency has a vulnerability or breaking change, propagation strategies include:
- **Overrides**: Define version overrides in package.json for fine-grained control over transitive dependency versions
- **Hoisting**: Install a desired transitive dependency version as a direct dependency; npm hoists it to override the transitive version
- **Lock files**: package-lock.json / Cargo.lock pin exact versions, making change detection explicit via diff

**Source:** [Understanding the npm dependency model](https://lexi-lambda.github.io/blog/2016/08/24/understanding-the-npm-dependency-model/); [Updating transitive dependencies](https://support.tidelift.com/hc/en-us/articles/26315406262292-Updating-transitive-dependencies)
**Confidence:** HIGH

**Transferable pattern for Momentum:** Lock files provide a versioned manifest of the entire dependency tree. A similar "spec-lock" manifest could record which version (git SHA or content hash) of each upstream document was current when each downstream document was last updated. Diff the manifest to detect staleness.

### 3.3 Database Foreign Key Cascading (SQL)

**How it works:**

Relational databases enforce referential integrity through foreign key constraints with cascading actions:

- **ON UPDATE CASCADE**: When a parent row's primary key changes, all child rows referencing that key are automatically updated
- **ON DELETE CASCADE**: When a parent row is deleted, all child rows referencing it are automatically deleted
- Cascading actions propagate transitively: if cascading referential actions are defined on target tables, the specified cascading actions also apply to affected rows

**Risks identified:**
- Unintended mass deletions resulting in permanent data loss
- Reduced visibility (changes don't appear in binlogs)
- Debugging difficulty when team members are unaware of cascade behavior
- Performance issues from serializable locks

**Recommended alternatives:** Application-level management with explicit transaction control, soft deletes using logical flags, and triggers with logging for audit trails.

**Source:** [MySQL Cascading Changes and Best Practices](https://www.stacksync.com/blog/mysql-cascading-changes-and-best-practices); [Cascading Referential Integrity Constraints (Microsoft)](https://learn.microsoft.com/en-us/previous-versions/sql/sql-server-2008-r2/ms186973(v=sql.105))
**Confidence:** HIGH

**Transferable pattern for Momentum:** The database CASCADE model is a cautionary tale. Fully automated cascading updates to specification documents would be dangerous -- a change to a PRD requirement should NOT auto-rewrite architecture decisions without human review. The "soft delete" / "suspect flag" approach is more appropriate: mark downstream documents as potentially stale rather than auto-modifying them.

### 3.4 DAG Topological Sort for Propagation Ordering

**How it works:**

Topological sorting produces a linear ordering of vertices in a DAG such that for every directed edge u->v, vertex u comes before v. Two standard algorithms exist:

1. **Kahn's Algorithm (BFS)**: Repeatedly select vertices with in-degree zero (no dependencies), process them, reduce in-degree of adjacent vertices
2. **DFS-based**: Perform depth-first search, push each vertex onto a stack after visiting all its neighbors, then reverse

**Application to change propagation:** "An important class of problems concern collections of objects that need to be updated... In these contexts, we use a dependency graph, which has a vertex for each object to be updated, and an edge connecting two objects whenever one of them needs to be updated earlier than the other."

**Source:** [Topological Sorting (Wikipedia)](https://en.wikipedia.org/wiki/Topological_sorting); [DAGs & Scheduling (MIT OCW)](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/mit6_042js15_session17.pdf)
**Confidence:** HIGH

**Transferable pattern for Momentum:** The spec chain (Research -> Brief -> PRD -> Architecture -> Epics -> Stories) is inherently a DAG. Topological sort determines the correct order for propagating changes: always process upstream documents before downstream ones. This ensures an agent updating the Architecture doc sees the already-updated PRD, not the stale version.

---

## 4. Document Dependency Management

### 4.1 Sphinx Cross-Reference System

**How it works:**

Sphinx uses a two-component system: **references** (pointers to other documentation elements) and **targets** (labeled anchors). References use the syntax `:role:\`target\`` and support multiple roles (ref, doc, class, func, etc.). Key capabilities:

- Human-readable names instead of raw URLs
- Portable across output formats (HTML, PDF, ePub)
- Build-time warnings for invalid references
- Cross-project linking via the **intersphinx** extension

**Intersphinx for cross-project dependencies:** Projects specify mapping files in `intersphinx_mapping` config, which resolve otherwise-missing references into links to external documentation. Running `python -m sphinx.ext.intersphinx <url>` displays all available link targets.

**Broken reference detection:** Sphinx emits warnings like "WARNING: py:class reference target not found" during builds. Running in nitpicky mode treats all missing references as errors, enforcing referential integrity.

**Source:** [Sphinx Cross-references](https://www.sphinx-doc.org/en/master/usage/referencing.html); [Sphinx Intersphinx](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html); [Read the Docs Guide](https://docs.readthedocs.com/platform/latest/guides/cross-referencing-with-sphinx.html)
**Confidence:** HIGH

**Transferable pattern for Momentum:** Sphinx's labeled reference system and build-time validation are directly transferable. Markdown documents in the spec chain could use a similar convention: labeled anchors in each document (e.g., `<!-- @ref:PRD-REQ-001 -->`) and explicit cross-references in downstream documents (e.g., `<!-- @depends:PRD-REQ-001 -->`). A validation pass can then check that all referenced targets exist and haven't changed.

### 4.2 Docusaurus Build-Time Link Validation

**How it works:**

Docusaurus detects broken links during production builds (`docusaurus build`). The `onBrokenLinks` config option supports values: `'ignore'`, `'warn'`, `'error'`, `'throw'`. By default, broken links cause the build to fail, ensuring broken links are never shipped.

**Limitations:** Link validation only runs at build time (not in dev mode). Cross-document references use standard markdown link syntax and file paths, without Sphinx-style semantic roles.

**Source:** [Docusaurus Config](https://docusaurus.io/docs/api/docusaurus-config); [Broken link detection issue](https://github.com/facebook/docusaurus/issues/6998)
**Confidence:** HIGH

### 4.3 MkDocs and autorefs Plugin

**How it works:**

MkDocs checks internal links at build time and warns when targets are not found. Using `--strict` mode causes the build to fail on warnings. The **autorefs** plugin (from mkdocstrings) provides automatic cross-page linking. When multiple pages contain identical heading anchors, `resolve_closest` finds the nearest match.

For external link checking, the **mkdocs-linkcheck** plugin validates outbound URLs.

**Source:** [mkdocstrings/autorefs](https://github.com/mkdocstrings/autorefs); [mkdocs-linkcheck](https://pypi.org/project/mkdocs-linkcheck/)
**Confidence:** HIGH

### 4.4 MyST Markdown Cross-References

**How it works:**

MyST Markdown (used with Sphinx) supports cross-referencing with shorthand `@` syntax or standard markdown link syntax `[text](#link)`. It supports cross-references across documents, to specific labels, equations, and figures.

**Source:** [MyST Markdown Cross-references](https://mystmd.org/guide/cross-references); [MyST References & Links](https://mystmd.org/spec/references)
**Confidence:** HIGH

**Transferable pattern for Momentum:** MyST's approach of embedding semantic references in markdown syntax is the closest analog to what Momentum needs. A convention for embedding dependency metadata directly in markdown frontmatter or inline comments would enable automated validation without leaving the markdown ecosystem.

---

## 5. Event-Driven Document Updates

### 5.1 Event Sourcing Pattern

**How it works:**

Instead of storing current state, record the full series of actions (events) in an append-only store. The store acts as the system of record. Current state is derived by replaying events. Key architectural elements:

1. Commands trigger business logic, which raises events
2. Events are persisted to an append-only event store
3. Event handlers listen for events and update read-optimized materialized views
4. State can be reconstructed at any point by replaying the event stream
5. Changes are never updated -- only compensating events are added

**Considerations:**
- Eventual consistency: materialized views may lag behind the event store
- Event versioning: schema changes require supporting multiple event versions
- Ordering: events must maintain causal ordering per entity
- Snapshots: for long event streams, periodic snapshots avoid expensive full replay
- Idempotency: event consumers must handle duplicate delivery

**Source:** [Event Sourcing Pattern (Azure Architecture Center)](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing); [Event Sourcing Pattern (AWS)](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/event-sourcing.html)
**Confidence:** HIGH

**Transferable pattern for Momentum:** Git is already an event store -- each commit is an immutable event recording what changed. The spec chain's change history is naturally captured in git log. Rather than building a separate event store, Momentum can treat git commits as the event stream and derive "materialized views" (e.g., a staleness dashboard or dependency status report) from git history analysis.

### 5.2 Change Data Capture (CDC) with Debezium

**How it works:**

CDC monitors database transaction logs to detect row-level changes (inserts, updates, deletes) and streams them as events. Debezium is an open-source CDC platform that:

1. Reads database transaction logs (not polling tables)
2. Produces change events to Kafka topics
3. Maintains event ordering matching commit order
4. Enables downstream consumers to react: update caches, search indexes, derived views

**Key advantage:** Minimal impact on source system performance since it reads logs rather than querying tables.

**Source:** [Debezium](https://debezium.io/); [CDC with Debezium (Medium)](https://sefikcankanber.medium.com/real-time-data-streaming-with-debezium-and-cdc-change-data-capture-c1aa162585a9)
**Confidence:** HIGH

**Transferable pattern for Momentum:** Git hooks (pre-commit, post-commit) function as a CDC mechanism for the file system. A post-commit hook that identifies which spec documents changed and emits a structured change event (document path, changed sections, diff summary) provides the foundation for downstream propagation workflows.

### 5.3 Reactive Programming (Observable Pipelines)

**How it works:**

Reactive programming treats data as streams of events. Observable pipelines chain operators that transform, filter, and combine streams. When a source value changes, the change propagates automatically through the pipeline to all subscribers.

**Core concepts:**
- **Observable**: represents a stream of values over time
- **Operators**: map, filter, combine, merge streams
- **Subscription**: consumers register interest and receive updates
- **Backpressure**: mechanisms to handle fast producers / slow consumers

**Source:** [ReactiveX Observable](https://reactivex.io/documentation/observable.html); [RxJS Guide (LogRocket)](https://blog.logrocket.com/guide-rxjs-observables/)
**Confidence:** HIGH

**Transferable pattern for Momentum:** The reactive pipeline metaphor maps cleanly to the spec chain. Each document is an Observable; downstream documents are Subscribers. When an upstream document emits a change, the pipeline propagates the notification through the chain. In practice, this would be implemented as a task queue where change events flow through the spec chain in topological order.

### 5.4 Pub/Sub Document Notification Systems

**How it works:**

Document management systems use pub/sub to notify stakeholders of changes. Users subscribe to folders or documents and receive notifications via email, in-app messages, or popup alerts when content changes.

**Source:** [Document Locator Notifications](https://www.documentlocator.com/features/document-notifications/); [Box Document Workflow Automation](https://blog.box.com/document-workflow-automation)
**Confidence:** MEDIUM

---

## 6. Git-Based Change Detection

### 6.1 Git Hooks for Validation and Triggering

**How it works:**

Git hooks are scripts executed before or after events (commit, push, receive). Relevant hooks for change propagation:

- **pre-commit**: Inspects staged snapshot before commit; can validate spec consistency, check cross-references, reject commits with broken dependencies
- **post-commit**: Runs after successful commit; can trigger downstream update workflows, emit change notifications
- **pre-push**: Validates before pushing to remote; can run full spec chain validation

The **pre-commit framework** manages multi-language hooks via `.pre-commit-config.yaml`, supporting plugins for markdown linting, link checking, and custom validation.

**Source:** [Git Hooks (Official)](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks); [pre-commit framework](https://pre-commit.com/); [Automating validation with Git hooks (Gofore)](https://gofore.com/en/automate-validating-code-changes-with-git-hooks/)
**Confidence:** HIGH

### 6.2 Markdown Link Checking via Git Hooks

**How it works:**

**markdown-link-check** validates all hyperlinks in markdown files, determining if they are alive or dead. **linkcheckmd** processes 10,000+ markdown files per second using Python asyncio. Both can be integrated as pre-commit hooks to catch broken internal links at commit time.

**Source:** [markdown-link-check](https://github.com/tcort/markdown-link-check); [linkcheckmd](https://pypi.org/project/linkcheckmd/); [pre-commit markdown linkcheck](https://www.scivision.dev/git-markdown-pre-commit-linkcheck/)
**Confidence:** HIGH

### 6.3 Git Diff for Change Detection

**How it works:**

`git diff` compares file states between commits, branches, or working tree. For document change propagation:

1. `git diff --name-only HEAD~1` identifies which files changed in the last commit
2. `git diff HEAD~1 -- docs/prd.md` shows specific changes to a document
3. `git diff-index --cached HEAD` examines staged changes before commit
4. Content hashes (git blob SHAs) provide instant change/no-change comparison

**DocuWriter.ai approach:** Automated webhook listeners receive git diffs within seconds of push events. AI examines each diff to classify: public API change (requires doc update), internal refactoring (potentially skip), or breaking change (needs migration guide). A single code change can trigger updates across multiple documentation sections simultaneously.

**Source:** [Git Diff Documentation](https://git-scm.com/docs/git-diff); [DocuWriter.ai Git Diff](https://www.docuwriter.ai/guides/understanding-git-diff-documentation)
**Confidence:** HIGH

### 6.4 GitHub Actions Path Filters

**How it works:**

GitHub Actions workflows can trigger conditionally based on which files changed:

- **Built-in path filters**: `on: push: paths: ['docs/prd/**']` triggers only when files in the specified path change
- **dorny/paths-filter action**: Enables conditional execution of individual jobs/steps based on modified files, with support for pull requests, feature branches, and pushed commits
- **Limitation**: Built-in path filters work at the workflow level, not individual job/step level

**Source:** [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions); [dorny/paths-filter](https://github.com/dorny/paths-filter)
**Confidence:** HIGH

**Transferable pattern for Momentum:** A GitHub Actions workflow triggered by changes to spec documents could: (1) identify which documents changed, (2) compute the downstream dependency set, (3) check staleness of each downstream document, and (4) create issues or trigger agent workflows for documents that need updating. Path filters ensure the workflow only runs when spec files are actually modified.

---

## 7. Requirements Management Tools

### 7.1 IBM DOORS: Suspect Links

**How it works:**

DOORS implements a "suspect link" mechanism for change impact analysis:

1. **Detection**: When a requirement object is modified, any objects linked TO the changed object are automatically marked as "suspect" -- but ONLY if the edited attribute has "Affect change dates" enabled (on by default)
2. **Directionality**: The changed object itself is NOT marked suspect; only its linked dependents receive the flag
3. **Bidirectional links**: When both source and target change, the link becomes suspect at both endpoints
4. **Clearing**: Suspect status can be removed individually or in bulk. Clearing at the source automatically clears at the target
5. **Impact analysis**: Teams trace suspect links to identify all affected requirements, performing impact analysis before implementation

**Key mechanism:** Suspect links are an information signal, not an enforcement mechanism. They flag that "an implemented change may have an impact on downstream requirements" and require human review to determine actual impact.

**Source:** [IBM DOORS Suspect Links](https://www.ibm.com/docs/en/engineering-lifecycle-management-suite/doors/9.7.2?topic=data-suspect-links-changed-objects); [DOORS Traceability](https://jazz.net/library/article/88104); [Sodiuswillert DOORS Next Guide](https://www.sodiuswillert.com/en/blog/how-to-set-up-create-and-use-traceability-links-in-ibm-doors-next)
**Confidence:** HIGH

**Transferable pattern for Momentum:** The suspect link mechanism is the single most transferable pattern for the spec chain. When a PRD changes, all Architecture, Epic, and Story documents that reference the changed PRD sections should be flagged as "suspect" -- requiring review but NOT auto-modified. The agent workflow then processes suspect documents in topological order, with AI performing semantic analysis to determine whether the upstream change materially affects each downstream document.

### 7.2 Jama Connect: Live Traceability and Impact Analysis

**How it works:**

Jama Connect provides "Live Traceability" across all items in the development process:

1. **Impact Analysis**: Shows a complete picture of all upstream and downstream related items that might be affected by changes
2. **Suspect flagging**: Upstream changes automatically flag downstream items as suspect
3. **Access**: Available via "Impact Analysis" toolbar button in Single Item View, or through the change request "Items to change" panel
4. **Proactive analysis**: Features allow understanding the scope of a change BEFORE it occurs
5. **Integration**: Connects to Sparx Enterprise Architect, PLM systems, test automation, and task management tools

**Source:** [Jama Impact Analysis](https://help.jamasoftware.com/ah/en/manage-content/coverage-and-traceability/impact-analysis.html); [Jama Best Practices for Change Impact Analysis](https://www.jamasoftware.com/blog/2022/09/12/change-impact-analysis-2/); [Jama All-in-One Solution](https://www.jamasoftware.com/blog/2025/04/25/jama-software-provides-a-single-all-in-one-solution-for-requirements-risk-management-and-validation/)
**Confidence:** HIGH

### 7.3 Siemens Polarion: Suspect Links with Cascading Review

**How it works:**

Polarion's suspect link mechanism adds a cascading review workflow:

1. **Trigger**: When a parent item changes and "Save and Suspect" is clicked (or is enabled globally), all linked child items get the "suspect link" attribute
2. **Cascading**: When child items are reviewed and modified, selecting "Save and Suspect" again propagates suspicion to the NEXT level downstream
3. **Notification**: Assignees of suspected child items are notified and must review them
4. **Resolution**: Reviewers either adapt the item to match the new requirement OR remove the suspect flag if no change is needed
5. **Completeness**: The process continues "until all levels are reviewed by their assignees"

**Unique feature:** Polarion's multi-level cascading suspect mechanism (where reviewing and updating a child triggers suspicion at the grandchild level) closely mirrors the spec chain use case.

**Source:** [Polarion Use Case: Requirement Changes](https://polarion.code.blog/2020/06/28/use-case-a-customer-requirement-changes-impact-analysis-and-staying-consistent/); [Polarion Requirements](https://polarion.plm.automation.siemens.com/products/polarion-requirements)
**Confidence:** HIGH

**Transferable pattern for Momentum:** Polarion's cascading "Save and Suspect" is the exact workflow needed. When an AI agent updates the Architecture doc (because the PRD changed), it should "Save and Suspect" the downstream Epics. When an Epic is updated, it suspects the Stories. This creates a wave of review that moves through the spec chain in order.

### 7.4 LDRA: Requirements Traceability Matrix (RTM)

**How it works:**

The Requirements Traceability Matrix links requirements to downstream artifacts (design, code, tests). When a requirement changes, the RTM row identifies all affected artifacts for impact analysis.

**Source:** [LDRA Requirements Traceability](https://ldra.com/capabilities/requirements-traceability/)
**Confidence:** MEDIUM

---

## 8. AI-Assisted Change Propagation

### 8.1 LLM Semantic Change Detection

**How it works:**

Traditional diff tools are "rather dumb" -- they identify line-by-line alterations without comprehension. A semantic diff "understands the purpose of the change, rather than just the effect" (Martin Fowler). Current tools like SemanticDiff distinguish between relevant changes (functional modifications) and irrelevant ones (whitespace, formatting).

For document specifications, LLMs can perform semantic diff by:
1. Comparing the old and new versions of an upstream document
2. Classifying changes as: cosmetic (no downstream impact), clarifying (minor downstream impact), substantive (requires downstream update), or breaking (requires significant downstream rewrite)
3. Identifying which specific downstream sections reference the changed content

**Source:** [Martin Fowler: Semantic Diff](https://martinfowler.com/bliki/SemanticDiff.html); [SemanticDiff tool](https://semanticdiff.com/)
**Confidence:** HIGH (concept); MEDIUM (LLM implementation -- emerging)

### 8.2 AI Documentation Automation Tools

**How it works (DocuWriter.ai example):**

1. Webhook listeners receive git diffs within seconds of push events
2. AI classifies each diff: public API change (requires doc update), internal refactoring (potentially skip), breaking change (needs migration guide)
3. Multi-page updates: a single code change can trigger updates across API references, getting started guides, integration examples, and changelogs simultaneously
4. Delivery options: direct commits, pull requests for review, or draft versions
5. Claims 97% reduction in documentation effort vs. manual processes

**Source:** [DocuWriter.ai Git Diff Documentation](https://www.docuwriter.ai/guides/understanding-git-diff-documentation)
**Confidence:** MEDIUM (vendor claims, limited independent verification)

### 8.3 AI Documentation Trends (2025-2026)

**Key developments:**

1. **LLMs as documentation consumers**: AI systems now actively crawl and quote documentation, embedding it across interfaces. Documentation must be designed for both human and machine consumption.
2. **llms.txt protocol**: Functions as a sitemap for AI systems, signaling what content to prioritize and how to interpret structure.
3. **Model Context Protocol (MCP)**: Anthropic's open standard enabling AI systems to retrieve real-time structured context from documentation and other sources, moving beyond static embeddings to dynamic querying.
4. **Passage-level indexing**: AI systems break docs into small chunks and return results based on semantic similarity.
5. **Semantic-drift detection**: Continuous monitoring detects when AI-generated answers about a product diverge from documentation, triggering targeted snippet updates.

**Source:** [Mintlify AI Documentation Trends 2025](https://www.mintlify.com/blog/ai-documentation-trends-whats-changing-in-2025); [Anthropic MCP](https://www.anthropic.com/news/model-context-protocol)
**Confidence:** HIGH

### 8.4 Agentic Workflow Patterns for Document Chains

**Key patterns identified:**

1. **Document Agent pattern**: Each document has a dedicated agent for answering questions and summarizing within its scope, coordinated by a Meta-Agent managing cross-document interactions
2. **Sequential pipeline**: Output of one agent becomes input for the next. Critical risk: "chaining error accumulation" where inconsistencies compound
3. **State management**: Google ADK uses `output_key` to write to shared `session.state` so the next agent in the chain knows where to pick up
4. **Knowledge graphs for determinism**: Offer "a structured method to navigate data, ensuring more 'deterministic' outcomes that can be easily traced" -- superior to vector stores for complex document relationships
5. **Human-in-the-loop checkpoints**: Essential for preventing drift across sequential processing

**Source:** [Vellum: 2026 Guide to AI Agent Workflows](https://www.vellum.ai/blog/agentic-workflows-emerging-architectures-and-design-patterns); [Google ADK Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
**Confidence:** HIGH

**Transferable pattern for Momentum:** The Document Agent pattern + Meta-Agent coordinator maps directly to Momentum's needs. Each spec document gets an "owner agent" that understands its content and dependencies. A Meta-Agent (the orchestrator) detects changes, determines impact, and dispatches update tasks to the appropriate document agents in topological order. Knowledge graphs track the relationships, and human-in-the-loop checkpoints prevent error accumulation.

---

## 9. Graph Database Approaches

### 9.1 Neo4j for Requirements Traceability

**How it works:**

ReqView demonstrates using Neo4j for requirements traceability analysis. The property graph model naturally represents document relationships:

- **Nodes**: Documents, Sections, Requirements, Tests, Design Elements
- **Relationships**: DEPENDS_ON, IMPLEMENTS, TESTS, DERIVED_FROM (with properties like creation date, status)
- **Queries**: Cypher queries traverse the graph for upstream/downstream impact analysis

Graph databases naturally connect customer requests to requirements, designs, and tests while enabling efficient upstream and downstream queries for root cause and impact analysis.

**Source:** [ReqView: Requirements Traceability in Neo4j](https://www.reqview.com/blog/requirements-traceability-analysis-neo4j/); [Neo4j Traceability in Manufacturing](https://neo4j.com/developer/industry-use-cases/manufacturing/product-design-and-engineering/engineering-traceability/)
**Confidence:** HIGH

### 9.2 Neo4j Enterprise Content Management Model

**How it works:**

A Neo4j ECM implementation uses these node types and relationships:

- **Nodes**: DOCUMENT, DIRECTORY, VERSION, EMPLOYER, TAG, ACTION
- **Relationships**: HAS_DOCUMENT (directory->document), VERSION (document->version), PERFORMED (employer->action), AFFECTED_VERSION (action->version), CAN_READ/CAN_WRITE (employer->directory)
- **Versioning**: Bidirectional version chains with `starttime`/`endtime` timestamps enable temporal queries ("What was the active version at time T?")
- **Audit trail**: ACTION nodes connected to VERSION nodes via AFFECTED_VERSION create complete history of who changed what and when

**Source:** [Neo4j Enterprise Content Management GraphGist](https://neo4j.com/graphgists/enterprise-content-management-with-neo4j/)
**Confidence:** HIGH

### 9.3 GraphRAG for Document Intelligence

**How it works:**

GraphRAG uses knowledge graphs where entities are modeled as nodes and relationships as edges. The system traverses the graph to gather connected knowledge, enabling multi-hop reasoning and structured querying over complex knowledge bases. Combined with LLMs, this enables intelligent document retrieval that understands document structure and relationships.

**Source:** [GraphRAG Tutorial (Medium)](https://medium.com/@daniel.puenteviejo/graphrag-tutorial-neo4j-llms-47372b71e3fa); [Neo4j Knowledge Graph Extraction](https://neo4j.com/blog/developer/knowledge-graph-extraction-challenges/)
**Confidence:** MEDIUM

**Transferable pattern for Momentum:** A lightweight graph model (implementable as a JSON manifest rather than requiring a full graph database) could represent the spec chain:

```
{
  "nodes": [
    {"id": "prd", "path": "docs/prd.md", "hash": "abc123", "sections": ["REQ-001", "REQ-002"]},
    {"id": "arch", "path": "docs/architecture.md", "hash": "def456", "sections": ["ARCH-001"]}
  ],
  "edges": [
    {"from": "arch#ARCH-001", "to": "prd#REQ-001", "type": "IMPLEMENTS"},
    {"from": "arch#ARCH-001", "to": "prd#REQ-002", "type": "IMPLEMENTS"}
  ]
}
```

This provides the traversal benefits of a graph database without the infrastructure overhead, stored as a trackable JSON file in the git repository.

---

## 10. Staleness Detection

### 10.1 Content Hash Comparison

**How it works:**

Document fingerprinting creates a unique identifier from document content using cryptographic hash functions (SHA-256, MD5). Any change to content produces a different fingerprint. Comparing current fingerprints to previously stored "known-good" values detects modifications.

In git, every blob has a SHA-1 hash computed from its contents. Comparing blob SHAs between commits instantly determines whether a file has changed, without needing to read the file contents.

**Source:** [Git Cryptographic Hashes](https://ericsink.com/vcbe/html/cryptographic_hashes.html); [Digital Fingerprint for Content Verification](https://www.scoredetect.com/blog/posts/digital-fingerprint-for-content-verification-explained)
**Confidence:** HIGH

### 10.2 Freshness Thresholds and Metrics

**How it works:**

Staleness can be measured operationally as:

```
staleness_ratio = time_since_last_update / acceptable_update_frequency
```

For example, if a document should be reviewed within 7 days and was last updated 5 days ago, staleness = 0.71 (71%). If updated 10 days ago, staleness = 1.43 (overdue at 143%).

**Detection approaches:**
- **Document age triggers**: Flag documents exceeding their acceptable staleness window
- **Change detection triggers**: Queue documents for review when source systems publish updates
- **Hybrid indexing**: For stable documents, use change detection and only re-process when actual modifications are detected

**Source:** [Stale Data Detection (Acceldata)](https://www.acceldata.io/blog/how-to-identify-and-eliminate-stale-data-to-optimize-business-decisions); [Data Freshness (Monte Carlo Data)](https://www.montecarlodata.com/blog-data-freshness-explained/); [Freshness Metrics (Validio)](https://docs.validio.io/docs/freshness)
**Confidence:** HIGH

### 10.3 Dependency-Aware Staleness

**How it works (synthesized approach):**

A document is stale if ANY of the following conditions are true:

1. **Source staleness**: An upstream document it depends on has been modified since this document was last updated
2. **Age staleness**: The document hasn't been reviewed within its acceptable freshness window
3. **Transitive staleness**: An upstream document is itself stale (propagated staleness)

Computing transitive staleness requires walking the dependency graph upstream. A document can be "transitively stale" even if its direct parent hasn't changed, if the grandparent changed and the parent hasn't been reviewed yet.

**Source:** [UNVERIFIED - synthesized from multiple patterns above]
**Confidence:** MEDIUM (synthesized pattern, not directly sourced)

**Transferable pattern for Momentum:** Staleness detection for the spec chain should combine:
1. Git blob SHA comparison (instant, zero-cost change detection)
2. A `last_verified_against` field in each document's frontmatter recording the upstream document's hash at time of last review
3. Transitive staleness computation via graph traversal

---

## 11. Synthesis: Applicability to Markdown Spec Chains

### 11.1 What Transfers Directly

| Pattern | Source Domain | Momentum Application | Complexity |
|---|---|---|---|
| DAG + topological sort | Build systems | Order of change propagation through spec chain | Low |
| Content hashing | Bazel, git | Instant change detection via blob SHAs | Low |
| Suspect links | DOORS/Jama/Polarion | Flag downstream docs as needing review | Low |
| Cascading suspect | Polarion | Wave of review moving through chain levels | Medium |
| Pre-commit link check | Git hooks | Validate cross-references at commit time | Low |
| Path-filtered CI | GitHub Actions | Trigger validation only when specs change | Low |
| Semantic diff via LLM | Emerging AI tools | Classify changes as cosmetic vs. substantive | Medium |
| Document Agent pattern | Agentic AI (2025-2026) | Per-document AI agent with Meta-Agent coordinator | High |

### 11.2 What Does NOT Transfer

| Pattern | Why Not |
|---|---|
| Full CASCADE (DB style) | Auto-modifying specs is dangerous; human review required |
| Full event sourcing | Over-engineered; git already provides event history |
| Neo4j graph database | Infrastructure overhead not justified for <100 documents |
| CDC / Debezium | Designed for database replication, not file-based specs |
| Commercial ALM tools (DOORS, Jama) | Cost and complexity disproportionate to markdown files |

### 11.3 Unique Advantages of the Momentum Context

1. **Git is the source of truth**: Every change is already tracked with full history, diffs, and blame
2. **AI agents are first-class**: LLMs can perform semantic analysis that traditional tools cannot
3. **Markdown is structured text**: Frontmatter, headings, and anchors provide parseable structure
4. **Small document count**: Tens of documents, not thousands -- graph operations are trivial
5. **MCP integration**: Anthropic's Model Context Protocol enables AI agents to query document structure dynamically

---

## 12. Recommended Architecture for Momentum

### 12.1 Design Principles

Based on this research, the recommended architecture follows these principles:

1. **Flag, don't auto-modify**: Use suspect links, not cascading updates
2. **Git-native**: Leverage git SHAs, diffs, and hooks rather than external databases
3. **Semantic awareness**: Use LLMs to distinguish cosmetic from substantive changes
4. **Topological ordering**: Process the spec chain upstream-to-downstream
5. **Human-in-the-loop**: AI proposes, human approves (at least initially)

### 12.2 Proposed Components

**Component 1: Dependency Manifest (spec-chain.json)**

A JSON file in the repository root recording the dependency graph:

```
{
  "documents": {
    "research": { "path": "docs/research.md", "depends_on": [] },
    "brief": { "path": "docs/brief.md", "depends_on": ["research"] },
    "prd": { "path": "docs/prd.md", "depends_on": ["brief"] },
    "architecture": { "path": "docs/architecture.md", "depends_on": ["prd"] },
    "epics": { "path": "docs/epics/", "depends_on": ["architecture", "prd"] },
    "stories": { "path": "docs/stories/", "depends_on": ["epics", "architecture"] }
  }
}
```

*Inspired by: Bazel BUILD files, npm package.json, requirements traceability matrices*

**Component 2: Document Frontmatter Metadata**

Each spec document includes frontmatter tracking its upstream dependencies:

```yaml
---
upstream_refs:
  - doc: prd
    sections: [REQ-001, REQ-002, REQ-003]
    verified_hash: "abc123"  # git blob SHA of prd.md at last review
    verified_date: "2026-03-14"
status: current  # or: suspect, stale, updating
---
```

*Inspired by: DOORS suspect links, Sphinx intersphinx mapping, npm lock files*

**Component 3: Change Detection (Git Hook or CI)**

A post-commit hook or CI workflow that:

1. Runs `git diff --name-only HEAD~1` to identify changed spec documents
2. Looks up the dependency manifest to find all downstream documents
3. Compares the `verified_hash` in each downstream document's frontmatter against the current hash of the changed upstream document
4. Marks mismatched documents as `status: suspect` in their frontmatter
5. Creates a summary of suspected documents for agent or human review

*Inspired by: Bazel incremental rebuild, DOORS suspect link auto-flagging, GitHub Actions path filters*

**Component 4: AI Semantic Triage**

An AI agent that processes suspected documents:

1. Retrieves the git diff of the upstream change
2. Performs semantic analysis: "Is this change cosmetic (formatting, typos) or substantive (new requirements, changed constraints)?"
3. If cosmetic: auto-clears the suspect flag and updates `verified_hash`
4. If substantive: generates a specific impact summary ("PRD REQ-002 changed from X to Y; Architecture section ARCH-001 references this requirement and may need updating")
5. For substantive changes: either auto-proposes an update (with human review) or creates an issue for manual resolution

*Inspired by: DocuWriter.ai semantic classification, Martin Fowler's Semantic Diff concept, Polarion cascading suspect review*

**Component 5: Propagation Orchestrator**

A Meta-Agent that coordinates the update wave:

1. Computes topological sort of the dependency graph
2. Processes documents in dependency order (upstream first)
3. For each suspected document, dispatches to the appropriate Document Agent
4. After each document is updated, triggers "Save and Suspect" on its downstream dependents (Polarion pattern)
5. Continues until no more documents are suspected
6. Produces a final consistency report

*Inspired by: Polarion cascading suspect workflow, Vellum Document Agent pattern, Kahn's algorithm for topological sort*

### 12.3 Architecture Diagram (Textual)

```
                    CHANGE DETECTED
                         |
                    [Git Commit]
                         |
                  [Post-Commit Hook]
                         |
              +----------+----------+
              |                     |
        [Identify Changed     [Dependency
         Spec Documents]      Manifest Lookup]
              |                     |
              +----------+----------+
                         |
                  [Compare Hashes]
                  verified_hash vs
                  current blob SHA
                         |
                   +-----+-----+
                   |           |
              [Match]    [Mismatch]
              (no-op)         |
                    [Flag as SUSPECT]
                         |
                  [AI Semantic Triage]
                         |
              +----------+----------+
              |                     |
        [Cosmetic]          [Substantive]
        Auto-clear           |
        suspect flag    [Generate Impact
                         Summary]
                              |
                    [Propose Update or
                     Create Issue]
                              |
                    [Human Review &
                     Approve]
                              |
                    [Update Document,
                     Save and Suspect
                     Downstream]
                              |
                    [Repeat for next
                     level in chain]
```

---

## 13. Sources Index

### Dependency Graph Patterns
- [Bazel Dependencies](https://bazel.build/concepts/dependencies)
- [How Bazel Works: Dependency Graphs, Caching, and Remote Execution](https://www.gocodeo.com/post/how-bazel-works-dependency-graphs-caching-and-remote-execution)
- [Bazel Dependency Management](https://bazel.build/basics/dependencies)
- [Understanding the npm dependency model](https://lexi-lambda.github.io/blog/2016/08/24/understanding-the-npm-dependency-model/)
- [Updating transitive dependencies (Tidelift)](https://support.tidelift.com/hc/en-us/articles/26315406262292-Updating-transitive-dependencies)
- [MySQL Cascading Changes and Best Practices](https://www.stacksync.com/blog/mysql-cascading-changes-and-best-practices)
- [Cascading Referential Integrity Constraints (Microsoft)](https://learn.microsoft.com/en-us/previous-versions/sql/sql-server-2008-r2/ms186973(v=sql.105))
- [ON DELETE CASCADE and ON UPDATE CASCADE (DEV)](https://dev.to/bhanufyi/understanding-on-delete-cascade-and-on-update-cascade-in-sql-foreign-key-relationships-70o)
- [Topological Sorting (Wikipedia)](https://en.wikipedia.org/wiki/Topological_sorting)
- [DAGs & Scheduling (MIT OCW)](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/mit6_042js15_session17.pdf)
- [Topological Sorting Explained (Medium)](https://medium.com/@amit.anjani89/topological-sorting-explained-a-step-by-step-guide-for-dependency-resolution-1a6af382b065)

### Document Dependency Management
- [Sphinx Cross-references](https://www.sphinx-doc.org/en/master/usage/referencing.html)
- [Sphinx Intersphinx Extension](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html)
- [Read the Docs: Cross-referencing with Sphinx](https://docs.readthedocs.com/platform/latest/guides/cross-referencing-with-sphinx.html)
- [Docusaurus Configuration](https://docusaurus.io/docs/api/docusaurus-config)
- [Docusaurus Broken Link Detection (Issue #6998)](https://github.com/facebook/docusaurus/issues/6998)
- [mkdocstrings/autorefs](https://github.com/mkdocstrings/autorefs)
- [mkdocs-linkcheck](https://pypi.org/project/mkdocs-linkcheck/)
- [MyST Markdown Cross-references](https://mystmd.org/guide/cross-references)
- [MyST References & Links Spec](https://mystmd.org/spec/references)
- [DocFX Links and Cross References](https://dotnet.github.io/docfx/docs/links-and-cross-references.html)

### Event-Driven Document Updates
- [Event Sourcing Pattern (Azure Architecture Center)](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
- [Event Sourcing Pattern (AWS)](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/event-sourcing.html)
- [CQRS Pattern (Azure)](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)
- [Event-Driven Architecture (TMS Outsource)](https://tms-outsource.com/blog/posts/event-driven-architecture/)
- [Debezium CDC Platform](https://debezium.io/)
- [CDC with Debezium (Medium)](https://sefikcankanber.medium.com/real-time-data-streaming-with-debezium-and-cdc-change-data-capture-c1aa162585a9)
- [ReactiveX Observable](https://reactivex.io/documentation/observable.html)
- [RxJS Guide (LogRocket)](https://blog.logrocket.com/guide-rxjs-observables/)
- [Reactive vs Proactive Document Control (DocBoss)](https://www.docboss.com/blog/reactive-versus-proactive-document-control/)
- [Document Locator Notifications](https://www.documentlocator.com/features/document-notifications/)
- [Box Document Workflow Automation](https://blog.box.com/document-workflow-automation)

### Git-Based Change Detection
- [Git Hooks (Official Book)](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [Git Hooks Documentation](https://git-scm.com/docs/githooks)
- [Git Diff Documentation](https://git-scm.com/docs/git-diff)
- [pre-commit Framework](https://pre-commit.com/)
- [markdown-link-check](https://github.com/tcort/markdown-link-check)
- [linkcheckmd](https://pypi.org/project/linkcheckmd/)
- [pre-commit Markdown Linkcheck](https://www.scivision.dev/git-markdown-pre-commit-linkcheck/)
- [DocuWriter.ai Git Diff Documentation](https://www.docuwriter.ai/guides/understanding-git-diff-documentation)
- [Automating Validation with Git Hooks (Gofore)](https://gofore.com/en/automate-validating-code-changes-with-git-hooks/)
- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)
- [dorny/paths-filter](https://github.com/dorny/paths-filter)

### Requirements Management Tools
- [IBM DOORS Suspect Links](https://www.ibm.com/docs/en/engineering-lifecycle-management-suite/doors/9.7.2?topic=data-suspect-links-changed-objects)
- [IBM DOORS About Suspect Links](https://www.ibm.com/docs/SSYQBZ_9.7.1/com.ibm.doors.requirements.doc/topics/c_aboutsuspectlinks.html)
- [DOORS Traceability (Jazz.net)](https://jazz.net/library/article/88104)
- [DOORS Linking Guide (Sodiuswillert)](https://www.sodiuswillert.com/en/blog/how-to-set-up-create-and-use-traceability-links-in-ibm-doors-next)
- [Jama Connect Impact Analysis](https://help.jamasoftware.com/ah/en/manage-content/coverage-and-traceability/impact-analysis.html)
- [Jama Best Practices for Change Impact Analysis](https://www.jamasoftware.com/blog/2022/09/12/change-impact-analysis-2/)
- [Jama All-in-One Solution (2025)](https://www.jamasoftware.com/blog/2025/04/25/jama-software-provides-a-single-all-in-one-solution-for-requirements-risk-management-and-validation/)
- [Polarion Use Case: Requirement Changes](https://polarion.code.blog/2020/06/28/use-case-a-customer-requirement-changes-impact-analysis-and-staying-consistent/)
- [Polarion Requirements](https://polarion.plm.automation.siemens.com/products/polarion-requirements)
- [Polarion Traceability Model](https://blogs.sw.siemens.com/polarion/how-to-incorporate-the-correct-traceability-model-into-your-processes/)
- [LDRA Requirements Traceability](https://ldra.com/capabilities/requirements-traceability/)
- [DOORS for Effective Systems Engineering](https://www.numberanalytics.com/blog/doors-for-effective-systems-engineering)

### AI-Assisted Change Propagation
- [Martin Fowler: Semantic Diff](https://martinfowler.com/bliki/SemanticDiff.html)
- [SemanticDiff Tool](https://semanticdiff.com/)
- [Graphtage Semantic Diff (Trail of Bits)](https://blog.trailofbits.com/2020/08/28/graphtage/)
- [Mintlify AI Documentation Trends 2025](https://www.mintlify.com/blog/ai-documentation-trends-whats-changing-in-2025)
- [Anthropic Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
- [MCP Specification](https://www.claudemcp.com/specification)
- [Vellum: 2026 Guide to AI Agent Workflows](https://www.vellum.ai/blog/agentic-workflows-emerging-architectures-and-design-patterns)
- [Google ADK Multi-Agent Patterns](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
- [AFLOW: Automating Agentic Workflow Generation (ICLR 2025)](https://proceedings.iclr.cc/paper_files/paper/2025/file/5492ecbce4439401798dcd2c90be94cd-Paper-Conference.pdf)
- [LLMs in Document Intelligence (ACM Survey)](https://dl.acm.org/doi/10.1145/3768156)
- [UiPath Intelligent Document Processing (2025)](https://www.uipath.com/blog/product-and-updates/intelligent-document-processing-2025-10-release)
- [LlamaIndex Document AI](https://www.llamaindex.ai/blog/document-ai-the-next-evolution-of-intelligent-document-processing)
- [DocuWriter.ai Git Diff Documentation](https://www.docuwriter.ai/guides/understanding-git-diff-documentation)

### Graph Database Approaches
- [Neo4j Getting Started](https://neo4j.com/docs/getting-started/graph-database/)
- [Neo4j Enterprise Content Management GraphGist](https://neo4j.com/graphgists/enterprise-content-management-with-neo4j/)
- [ReqView: Requirements Traceability in Neo4j](https://www.reqview.com/blog/requirements-traceability-analysis-neo4j/)
- [Neo4j Traceability in Manufacturing](https://neo4j.com/developer/industry-use-cases/manufacturing/product-design-and-engineering/engineering-traceability/)
- [GraphRAG Tutorial: Neo4j + LLMs (Medium)](https://medium.com/@daniel.puenteviejo/graphrag-tutorial-neo4j-llms-47372b71e3fa)
- [Neo4j Knowledge Graph Extraction](https://neo4j.com/blog/developer/knowledge-graph-extraction-challenges/)

### Staleness Detection
- [Stale Data Detection (Acceldata)](https://www.acceldata.io/blog/how-to-identify-and-eliminate-stale-data-to-optimize-business-decisions)
- [Data Freshness Explained (Monte Carlo Data)](https://www.montecarlodata.com/blog-data-freshness-explained/)
- [Freshness Metrics (Validio)](https://docs.validio.io/docs/freshness)
- [Stale Data Guide (Atlan)](https://atlan.com/stale-data/)
- [What is Stale Data (Tacnode)](https://tacnode.io/post/what-is-stale-data)
- [Git Cryptographic Hashes (Eric Sink)](https://ericsink.com/vcbe/html/cryptographic_hashes.html)
- [Digital Fingerprint for Content Verification](https://www.scoredetect.com/blog/posts/digital-fingerprint-for-content-verification-explained)
- [Knowledge Decay Problem in RAG (RAGAboutIt)](https://ragaboutit.com/the-knowledge-decay-problem-how-to-build-rag-systems-that-stay-fresh-at-scale/)
