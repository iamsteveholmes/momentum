---
id: DEC-016
title: Agent Taxonomy — Two-Tier Model (Abstract Base + Shipped Customs) with Per-Skill Configuration
date: '2026-05-03'
status: decided
source_research:
  - path: "(conversation)"
    type: developer-conversation
    date: '2026-05-03'
prior_decisions_reviewed:
  - DEC-013 (Universal Agent Model — extended: adds tier classification and shipped-custom concept)
  - DEC-008 (Composable Agents Architecture — extended: per-skill agents.md config and N-cardinality slots)
architecture_decisions_affected:
  - DEC-013 D1 — extended: all agent types follow the universal model, now further classified into two tiers
  - DEC-008 — extended: per-skill agents.md manifest adds tier, cardinality, and override metadata
stories_affected:
  - validator-agent-definition (new)
  - enumerator-agent-definition (new)
  - adversary-agent-definition (new)
  - retro-auditor-agent-definition (new)
  - auditor-human-agent-definition (new)
  - auditor-execution-agent-definition (new)
  - auditor-review-agent-definition (new)
  - documenter-agent-definition (new)
  - code-reviewer-agent-definition (new)
  - architect-guard-agent-definition (new)
  - dev-fixer-agent-definition (new)
  - agents-md-manifest-format (updated scope)
---

# DEC-016: Agent Taxonomy — Two-Tier Model (Abstract Base + Shipped Customs) with Per-Skill Configuration

## Summary

Three decisions emerged from a conversation about which agent roles should ship in the Momentum plugin and how they should be classified. D1 establishes a two-tier taxonomy within the universal agent model (DEC-013): Tier A (project-conditioned bases) vs. Tier B (stable-default shipped customs). D2 establishes that Momentum ships both abstract bases AND concrete shipped customs in the plugin — not just bases. D3 establishes per-skill configuration via an `agents.md` manifest with N-instance cardinality support.

---

## D1: Two-Tier Agent Taxonomy

### Decision

Agent roles in the Momentum plugin are classified into two tiers:

**Tier A — Project-conditioned bases:** Roles expected to be composed per-project using build-guidelines. The base body defines the role contract; project composition adds stack-specific guidelines. These are the roles where the build-guidelines pipeline delivers the most value.

Examples: `dev`, `architect`, `qa-reviewer`, `e2e-validator`, `sm`, `pm`, `code-reviewer`, `architect-guard`

**Tier B — Stable-default shipped customs:** Roles whose behavior is unlikely to change across projects. Momentum ships a complete, concrete definition. The base body IS the production definition — project composition is possible but rare. These roles encode workflow patterns, not technology stacks.

Examples: `validator` (abstract base for validation roles), `enumerator`, `adversary`, `retro-auditor` (abstract base for retro auditors), `auditor-human`, `auditor-execution`, `auditor-review`, `documenter`

### Rationale

DEC-013 established one model for all agents. This decision adds classification within that model. The distinction matters for two reasons:
1. **Build-guidelines investment:** Only Tier A roles benefit from the build-guidelines compose pipeline. Tier B roles are stable enough that project composition rarely adds value.
2. **Override semantics:** A project overriding a Tier A base is following the expected path. A project overriding a Tier B shipped custom is making a domain-specific customization choice (e.g., a security-focused project wanting an adversary that knows OWASP patterns).

Both tiers follow the same model — base body in plugin, optional project override. The tier is metadata that guides decisions, not a separate mechanism.

### Consequences

- The `agents.md` manifest format (see D3) includes a `tier` field for each role slot
- build-guidelines' compose pipeline targets Tier A roles; Tier B roles are treated as pass-through
- Documentation and onboarding guides should explain the distinction to help teams decide when to compose vs. accept the default

---

## D2: Momentum Ships Both Abstract Bases and Concrete Shipped Customs

### Decision

The Momentum plugin ships two types of agent definition files:

1. **Abstract bases** (`validator`, `retro-auditor`): Define the role contract — stance, output format, composable interface. Concrete shipped customs inherit this contract. Projects can override at the base level to change behavior across all derivatives.

2. **Concrete shipped customs** (`enumerator`, `adversary`, `auditor-human`, `auditor-execution`, `auditor-review`): Complete production-ready definitions that are Momentum's default implementations. Ship in the plugin. Used as-is by most projects. Can be overridden at the individual role level for domain-specific needs.

This is a departure from the previous implicit model where the plugin only shipped bases. The plugin now ships a full working set of agent definitions — not just the foundations for project composition.

### Rationale

Enumerator and adversary are not customizable in the same way that a dev agent is customizable. A project using AVFL doesn't compose a custom enumerator — it uses Momentum's default. But a security-focused project COULD want a security-adversary that knows OWASP patterns. The shipped custom gives a working default; the override path gives the escape hatch.

The same logic applies to retro auditors: the three auditor roles (human/execution/review) are Momentum's shipped implementation of the retro-auditor contract. They're concrete and complete. Projects rarely need to change them, but a project with a non-standard transcript format (e.g., a different logging system) should be able to override `auditor-human.md` without changing the retro workflow.

### Consequences

- The plugin's `agents/` directory grows beyond just bases — it contains a full working set of agent definitions
- The install footprint increases proportionally; this is acceptable given the value
- Projects that override individual shipped customs do so at their own risk of divergence from future plugin updates

---

## D3: Per-Skill Agent Configuration via agents.md with N-Cardinality Support

### Decision

Each Momentum skill directory includes an `agents.md` manifest that declares:

| Field | Description |
|---|---|
| `role` | The agent role slot name (kebab-case) |
| `default_file` | Path to the default plugin definition file |
| `tier` | `A` (project-conditioned) or `B` (stable-default) |
| `cardinality` | `1` (singleton) or `N` (multiple instances allowed) |
| `override_path` | Where a project places an override file |
| `notes` | Context for when/why to override |

The `cardinality=N` field is specifically motivated by the dev-fixer slot in sprint-dev: a project with separate backend and frontend can configure sprint-dev to spawn two fixers, each with a different composed definition. The slot name (`dev-fixer`) is stable; the number of instances and their definitions are project-configured.

The `agents.md` manifest is the seed list referenced in DEC-013 D3 — it is the minimum known role set for the skill. Sprint-planning reads it to discover roles the project may need to compose.

### Rationale

Without a per-skill manifest, there is no machine-readable way to know: (a) which roles a skill needs, (b) whether the project has composed them, (c) whether N-cardinality slots have been configured. Sprint-planning currently has no mechanism to detect agent coverage gaps before a sprint starts. The manifest fills this gap.

The `cardinality=N` insight comes from observing that a monolithic project and a multi-stack project (backend + iOS + Android) have fundamentally different fixer needs. The slot model accommodates this without requiring changes to the sprint-dev workflow itself — the workflow reads the manifest to determine how many fixers to spawn.

### Alternatives Considered

**Global registry instead of per-skill manifest:** A single file listing all roles for all skills. Rejected: per-skill placement keeps the manifest co-located with the skill it describes, making it easier to maintain and review. The global registry pattern centralizes a concern that is inherently distributed.

**Cardinality handled entirely by project composition:** Projects compose N variants (backend-fixer, frontend-fixer) and the skill auto-discovers them. Rejected: auto-discovery is fragile. Explicit cardinality declaration in the manifest is unambiguous and auditable.

### Consequences

- The `agents-md-manifest-format` story defines the canonical format (YAML or Markdown table)
- Priority skills for initial agents.md population: sprint-dev, retro, avfl, distill
- Sprint-planning workflow needs an update to read agents.md and surface role coverage gaps before sprint activation
