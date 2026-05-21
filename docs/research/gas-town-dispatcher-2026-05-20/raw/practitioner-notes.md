---
content_origin: human
date: 2026-05-20
topic: "Gas Town as dispatcher/coordinator for Momentum"
---

# Practitioner Notes — Phase 4 Q&A

## Q1: CON-001 — Gas Town "poor fit" vs Gas City "right tool"

**Question:** The corpus has directly opposing verdicts. The maturity file says Gas Town is a "poor fit." The adoption file says Gas City is "the right tool." Are these evaluating different products, or an irreconcilable disagreement?

**Answer:** Follow-up research completed (see validation/ follow-up files). Both verdicts are confirmed correct simultaneously — they are evaluating different products.

**Summary of findings:**
- Gas Town (the Gastown Colony topology) = confirmed poor fit. Four hardwired architectural mismatches: fixed Mayor/Polecat/Refinery role taxonomy in Go SDK (not configurable), 20–30 agent colony scale assumption, work model hardwired to PRs + merge queue, directory-as-identity model (Gas City's own docs list this as a mistake to abandon).
- Gas City (the composable SDK) = conditional yes. Resolves all four mismatches: no hardcoded role names in Go, configurable pool sizing, explicit identity from config/metadata, general-purpose Orders system. Gas Town is one optional pack inside Gas City — the quickstart deploys zero Gas Town infrastructure.
- Gas City is independently adoptable: `GC_BEADS=file` removes Dolt dependency entirely for PoC; exec orders invoke `claude -p` as a shell subprocess, bypassing Gas City's deferred MCP runtime support.

**Synthesis recommendation:** Endorse Gas City's Orders system as the dispatcher PoC target; explicitly rule out the Gas Town Gastown pack as the deployment model. Start with `GC_BEADS=file` + exec orders (condition trigger, flag-file based) before committing to Dolt or formula orders.

---

## Q2: CON-006 — Is Beads operationally live in Momentum?

**Question:** The adoption file assumes "Beads is already being adopted." Is Beads deployed and live, or still pre-deployment?

**Answer:** Beads is running, working, and tested — but not fully adopted yet. It is operational (the dual-write spike validated the integration) but the stack has not been committed to as the primary task layer.

**Synthesis implication:** The adoption file's framing ("already adopted") is partially correct but overstated. More accurate: Beads is validated and in active evaluation, not yet the authoritative tracking layer. The Dolt compounded-risk scenario (CON-related to gas city + beads failing together) is real but moderated: Beads has been tested under Momentum's actual usage patterns.
