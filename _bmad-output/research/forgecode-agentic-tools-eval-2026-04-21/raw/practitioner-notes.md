---
content_origin: human
date: 2026-04-21
topic: "ForgeCode and agentic tooling evaluation for Momentum"
---

# Practitioner Q&A — AVFL-Derived Questions

Responses from the developer (Steve) resolving the highest-stakes cross-document contradictions and unverified claims surfaced by AVFL corpus validation.

## Q1 — TermBench 2.0 cheating disclosure

**AVFL finding:** DebugML paper ("Finding Widespread Cheating on Popular Agent Benchmarks", debugml.github.io/cheating-agents/) claims ForgeCode's 81.8% score relies on AGENTS.md files containing literal answer keys, with adjusted fair score ~71.7% (14th place).

**Answer:** Mix of (a) and (b) — **the disclosure is part of ForgeCode's merits.** Synthesis should integrate the cheating finding into the overall assessment of ForgeCode's credibility rather than either ignoring it or using it purely as a headline. Treat the 81.8% as a contested claim alongside the 71.7% DebugML-adjusted figure; let the reader weigh both.

**Instruction to synthesis:** Cite DebugML. Present both numbers with context. Let benchmark integrity factor into the credibility/maturity rating.

## Q2 — ForgeCode hooks status

**AVFL finding:** Gemini claims ForgeCode has "native hook systems." Four subagent files say hooks are absent.

**Answer:** ForgeCode is open source — verify this directly by reading the repo, rather than treating it as an unresolved contradiction. Also: **hooks aren't an absolute must** — what matters is how ForgeCode achieves determinism. If it uses a different mechanism (deterministic workflow DSL, planning mode, todo_write enforcement), that may substitute for hooks in Momentum's sense.

**Instruction:** Spawn a verification agent to read `github.com/antinomyhq/forge` (and tailcallhq/forgecode mirror if relevant) for:
1. Hook system presence/absence — search for "hook", "lifecycle", "pre-tool", "post-tool", "on_" event patterns in code, docs, and config
2. Determinism primitives — planning mode, workflow DSL, todo_write enforcement, mandatory-task patterns
3. Current version number (resolve the v0.106.0 vs v2.12.0 dispute)

## Q3 — ForgeCode version discrepancy

**AVFL finding:** Gemini says v0.106.0 (Aug 2025); subagents say v2.12.0 (Apr 2026).

**Answer:** **Flag the discrepancy** in the final document. Direct verification from the repo (per Q2) will resolve which is canonical; synthesis can present whichever the repo tags show as current, with a note about the conflicting source.

## Q4 — OpenCode "opencode-workflows" DAG plugin recommendation

**AVFL finding:** Gemini's recommendation uses a solo-dev plugin for "critical engineering paths" — contradicts the corpus's own governance risk framework.

**Answer:** Option **(b)** — keep the recommendation but attach a governance caveat. Note the solo-developer backing and lack of organizational governance; treat as prototype/experimentation rather than production-critical path.

## Q5 — Goose lifecycle hooks (plus general AVFL follow-up to Gemini)

**AVFL finding:** Gemini's follow-up 2 claims Goose added HTTP hooks (sourced only from a practitioner blog). Subagent research says Goose hooks = Missing.

**Answer:** Send a follow-up to Gemini to verify this one way or another. **Also evaluate other claims in the same vein and ask follow-ups as appropriate** — e.g., Tool-Call Correction Layer / Semantic Entry-Point Discovery (ForgeCode named architecture components), opencode-workflows plugin, Bifrost "Maxim AI" naming + 11µs overhead, "GPT-5.4" and "Claude 4.6 Opus" model names, OpenCode 95K vs 147K stars, VS Code "never" mode.

**Instruction:** Send Gemini follow-up #3 requesting primary-source verification for the above claims; capture the response under `## Follow-Up 3 — Disputed claims verification` in `raw/gemini-deep-research-output.md`.

---

## Disposition

- Direct verification: spawn subagent on `antinomyhq/forge` (Q2, Q3)
- Gemini follow-up #3: verify disputed claims (Q5 + broader)
- AVFL findings stand as logged; synthesis applies corrections in-line using the above responses as authoritative overrides
- Authority precedence for synthesis (implicit): `practitioner-notes.md` > `research-*.md` subagent files > `gemini-deep-research-output.md` main body (follow-ups slightly stronger than main body since they carry citations)
