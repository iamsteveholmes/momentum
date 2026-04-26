# Momentum Workflow

End-to-end view of how work flows through Momentum: from raw signal (research, observations, drift) all the way through grooming, sprint execution, and retro feedback into the practice itself.

> **Status:** Draft v0.1 — expect iteration. Use this doc as the canonical picture; update both the Mermaid diagram and the ASCII fallback when phases shift.

## Phases at a glance

| Phase | Purpose | Primary skills |
|---|---|---|
| **Discovery** | Generate strategic context | `research`, `assessment`, `decision` |
| **Capture** | Convert signal into structured backlog | `intake`, `triage` |
| **Grooming** | Shape backlog into shippable units | `feature-grooming`, `epic-grooming`, `feature-breakdown`, `create-story` |
| **Execution** | Build and merge stories | `sprint-planning`, `sprint-dev`, `dev`, `avfl` |
| **Closure** | Learn and improve the practice | `retro`, `distill` |
| **Cross-cutting** | Hygiene + drift control | `refine`, `architecture-guard`, `upstream-fix`, `feature-status` |

## Mermaid diagram

```mermaid
flowchart TB
    classDef phase fill:#1e293b,stroke:#475569,color:#e2e8f0,stroke-width:2px
    classDef skill fill:#0f172a,stroke:#3b82f6,color:#dbeafe
    classDef artifact fill:#451a03,stroke:#f59e0b,color:#fef3c7
    classDef feedback fill:#14532d,stroke:#22c55e,color:#dcfce7

    %% Discovery
    subgraph DISCOVERY["🔭 DISCOVERY"]
        direction LR
        Research[research]:::skill
        Assessment[assessment]:::skill
        Decision[decision<br/>DEC docs]:::skill
        Research --> Assessment --> Decision
    end
    class DISCOVERY phase

    %% Capture
    subgraph CAPTURE["📥 CAPTURE"]
        direction TB
        Signal[/observations · ideas<br/>bugs · drift · feedback/]:::artifact
        Intake[intake]:::skill
        Triage[triage<br/>6-class]:::skill
        Signal --> Intake --> Triage
    end
    class CAPTURE phase

    %% Grooming
    subgraph GROOMING["🧹 GROOMING"]
        direction TB
        FeatureGroom[feature-grooming]:::skill
        EpicGroom[epic-grooming]:::skill
        Breakdown[feature-breakdown]:::skill
        CreateStory[create-story<br/>+ AVFL]:::skill
        FeatureGroom <--> EpicGroom
        FeatureGroom --> Breakdown
        EpicGroom --> Breakdown
        Breakdown --> CreateStory
    end
    class GROOMING phase

    %% Execution
    subgraph EXECUTION["🛠 EXECUTION"]
        direction TB
        SprintPlan[sprint-planning]:::skill
        SprintDev[sprint-dev<br/>worktree waves]:::skill
        PostAVFL[post-merge AVFL]:::skill
        TeamReview[team review<br/>QA + E2E]:::skill
        SprintPlan --> SprintDev --> PostAVFL --> TeamReview
    end
    class EXECUTION phase

    %% Closure
    subgraph CLOSURE["🔁 CLOSURE"]
        direction TB
        Retro[retro<br/>auditors + findings]:::skill
        Distill[distill<br/>Tier-1 → practice]:::skill
        Retro --> Distill
    end
    class CLOSURE phase

    %% Cross-cutting
    subgraph CROSS["⚙ CROSS-CUTTING"]
        direction LR
        Refine[refine]:::skill
        ArchGuard[architecture-guard]:::skill
        Upstream[upstream-fix]:::skill
        FStatus[feature-status]:::skill
    end
    class CROSS phase

    %% Flow between phases
    Decision -->|adopt| GROOMING
    Triage -->|story| GROOMING
    Triage -->|decision| Decision
    Triage -->|research| Research
    GROOMING --> EXECUTION
    EXECUTION --> CLOSURE

    %% Feedback loops
    Distill -.->|rules · skills · refs| DISCOVERY
    Distill -.->|practice update| GROOMING
    Distill -.->|practice update| EXECUTION
    PostAVFL -.->|root cause| Upstream
    Upstream -.->|fix at source| CLOSURE

    %% Cross-cutting connections
    CROSS -.->|hygiene| GROOMING
    CROSS -.->|drift| EXECUTION
```

## ASCII fallback

```
                          MOMENTUM WORKFLOW
                          ═════════════════

  ┌─────────────────────── DISCOVERY ───────────────────────┐
  │                                                          │
  │   ┌──────────┐      ┌────────────┐      ┌────────────┐  │
  │   │ Research │─────▶│ Assessment │─────▶│ Decisions  │  │
  │   │          │      │            │      │ (DEC docs) │  │
  │   └──────────┘      └────────────┘      └─────┬──────┘  │
  │        ▲                                       │         │
  └────────┼───────────────────────────────────────┼─────────┘
           │                                       │
           │ (open questions)                      │ (adopt)
           │                                       ▼
  ┌────────┴──────────────── CAPTURE ───────────────────────┐
  │                                                          │
  │   observations, ideas, bugs, drift, feedback             │
  │                          │                               │
  │                          ▼                               │
  │                   ┌─────────────┐                        │
  │                   │   Intake    │  (stub → backlog)      │
  │                   └──────┬──────┘                        │
  │                          │                               │
  │                          ▼                               │
  │                   ┌─────────────┐                        │
  │                   │   Triage    │  (classify 6 ways)     │
  │                   └──────┬──────┘                        │
  │           ┌──────────────┼──────────────┐                │
  │           ▼              ▼              ▼                │
  │       [decision]     [research]     [story]              │
  │           │              │              │                │
  └───────────┼──────────────┼──────────────┼────────────────┘
              │              │              │
              └──────────────┘              │
                                            ▼
  ┌────────────────────── GROOMING ─────────────────────────┐
  │                                                          │
  │   ┌──────────────────┐         ┌──────────────────┐     │
  │   │ Feature Grooming │◀───────▶│  Epic Grooming   │     │
  │   │ (taxonomy/value) │         │ (story breakdown)│     │
  │   └────────┬─────────┘         └────────┬─────────┘     │
  │            │                            │                │
  │            └──────────────┬─────────────┘                │
  │                           ▼                              │
  │                  ┌─────────────────┐                     │
  │                  │  Create Story   │  (specs + AVFL)     │
  │                  └────────┬────────┘                     │
  │                           │                              │
  └───────────────────────────┼──────────────────────────────┘
                              │
                              ▼
  ┌────────────────────── EXECUTION ────────────────────────┐
  │                                                          │
  │   ┌──────────────────┐                                   │
  │   │ Sprint Planning  │ (select stories, Gherkin, team)   │
  │   └────────┬─────────┘                                   │
  │            ▼                                              │
  │   ┌──────────────────┐    ┌──────────┐    ┌──────────┐  │
  │   │   Sprint Dev     │───▶│ Post-AVFL│───▶│   Team   │  │
  │   │ (worktree waves) │    │  (fix)   │    │  Review  │  │
  │   └──────────────────┘    └──────────┘    └─────┬────┘  │
  │                                                  │       │
  │                                                  ▼       │
  │                                          ┌──────────────┐│
  │                                          │  Retro       ││
  │                                          │ (auditors,   ││
  │                                          │  findings)   ││
  │                                          └──────┬───────┘│
  └─────────────────────────────────────────────────┼────────┘
                                                    │
                          ┌─────────────────────────┘
                          │ (Tier-1 findings)
                          ▼
                  ┌───────────────┐
                  │    Distill    │──▶ rules / skills / refs
                  └───────┬───────┘     (practice update)
                          │
                          └─────────▶ feeds back into ALL phases
                                      (better next time)

  ─────────────────────────────────────────────────────────
   Cross-cutting: Refine (backlog hygiene) · Architecture
   Guard (drift detection) · Upstream-Fix (root-cause traces)
  ─────────────────────────────────────────────────────────
```

## Notes for iteration

- **Quick-fix path** is not shown — it's a sidecar that bypasses sprint planning for single-story changes (`intake → quick-fix → merge`). Worth adding when we agree on placement.
- **Impetus** is the orchestrator that fronts most of these — show it as a top-level entry point or keep it implicit?
- **Cross-cutting** lane is gestural; if any of those skills become first-class phase participants, promote them.
- Feedback arrows from `distill` are dotted to convey "asynchronous practice update" vs the solid "work flows here next" arrows.
