# AVFL Findings — Coherence & Craft (Adversary Framing) — PARTIAL

**Status:** Validator subagent stalled before completing full output. Partial findings recovered from stream.

**Lens:** Coherence & Craft (COHERENCE) | **Framing:** Adversary | **Skepticism:** 3 (aggressive) | **Stage:** final | **Corpus:** 9 files

---

## COHERENCE-ADV-001 — high — cross_document_consistency

- **location:** `research-feature-parallels.md`:AVFL section AND `research-ecc-superior.md`:adversarial validation section vs `research-momentum-superior.md`:section comparing AVFL
- **description:** The corpus picks two different ECC skills as "the AVFL analogue" without acknowledging both exist. `research-feature-parallels.md` and `research-ecc-superior.md` identify ECC's adversarial-validation analogue as `gan-style-harness` (Generator + Evaluator + Playwright). `research-momentum-superior.md` identifies it as `santa-method` (dual independent reviewers, binary verdict). These are TWO DIFFERENT skills in the ECC repo. `gan-style-harness` does code generation against a live app (not artifact validation). `santa-method` is closer in spirit to AVFL (dual-reviewer validation) but lacks AVFL's lens decomposition, profiles, and benchmarked role tiers.
- **evidence:**
  - `research-feature-parallels.md` cites `gan-style-harness/SKILL.md` as the AVFL analogue.
  - `research-momentum-superior.md` Section "AVFL: multi-agent dual-reviewer validation" cites `santa-method/SKILL.md` as the closer-but-still-inadequate analogue.
  - Both files reference real ECC skills; they're not contradicting on existence, only on which one maps to AVFL.
- **suggestion:** Reconcile in synthesis: ECC has two skills in this neighborhood — `gan-style-harness` (live-app generation+evaluation) and `santa-method` (dual-reviewer artifact validation). Neither is a 1:1 AVFL match; `santa-method` is conceptually closer but still binary and undecomposed. Acknowledge both in the final synthesis to avoid implying ECC has a single AVFL-analogous skill.

---

## Summary

1 finding recovered from partial output (high severity, cross-document inconsistency on ECC's adversarial-validation analogue mapping). Validator stalled before producing more findings; consolidation should treat this lens as undersampled and consider re-running if confidence is needed.
