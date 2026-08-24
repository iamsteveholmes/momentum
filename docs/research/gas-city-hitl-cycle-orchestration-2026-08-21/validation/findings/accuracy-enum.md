# Validator: accuracy / Enumerator (sonnet) — 6 findings (2 critical, 1 major, 2 minor, 1 low)

id: ACCURACY-E-001 | severity: critical | dimension: correctness | location: gemini-deep-research-output.md:Follow-Up Q1
description: Gemini claims notify/renudge human-gate orders have "functionally equivalent" substitutes folded into stable-release core pack; two independent hands-on/source checks show the notify/renudge orders are absent from all tagged releases (edge/main only) and gate-sweep deliberately excludes human gates. Provenance claim ("folded from a maintenance pack") also unsupported — actual provenance is community PR #4553 (2026-07-23) directly against core/orders.
evidence: Gemini "functionally equivalent mechanical housekeeping orders in its tagged releases... not restricted to main/edge" vs handson "no notify-on-human-gate-creation and no renudge-stale-human-gates... gate-sweep... exactly two lines: gc bd gate check --type=timer --escalate; gc bd gate check --type=gh --escalate || true" and watcher-layer "Raw fetches... at v1.4.1, v1.4.0, v1.3.5 all return 404... commit 741a2d9d (PR #4553) dated 2026-07-23... missed the v1.4.0 cut... only in edge pre-release ('not for production')".
suggestion: Correct Follow-Up Q1: reflex absent from all tagged releases; shipped 1.4.x orders are not substitutes; affects the ~6-9 day glue estimate assumption.

id: ACCURACY-E-002 | severity: critical | dimension: correctness | location: gemini-deep-research-output.md:Table 3
description: Gemini describes "#2311 / #3200" as a patched Dolt orphan-misclassification bug; actual GitHub #2311 is an unrelated, still-OPEN waits_for barrier-semantics bug (p2, no fix PR, workaround regressed). "#3200" uncorroborated anywhere in corpus.
evidence: Gemini "Barrier Race & False Orphans (#2311 / #3200)... Patched." vs maturity "#2311 waits_for = children-of(X) does not gate bd ready... OPEN... last activity 2026-05-29, no fix PR... workaround... fails molecule instantiation outright... a formula shaped 'phase: conduct N stories in parallel → gate: human reviews' cannot use waits_for as the barrier."
suggestion: Correct #2311 row to OPEN with verified content; drop or independently source "#3200".

id: ACCURACY-E-003 | severity: major | dimension: correctness | location: gemini-deep-research-output.md:Table 3
description: Wedge bugs #2131/#2168 attributed to v1.4.0 fix; actually resolved in v1.2.0 window (2026-05-23/26 via PR #2497 and commit 6c9af50).
evidence: Gemini "Mitigated in v1.4.0" vs maturity "Both are genuinely resolved in the v1.2 window (v1.2.0, 2026-05-29)".
suggestion: Correct attribution to v1.2.0.

id: ACCURACY-E-004 | severity: minor | dimension: correctness | location: gemini-deep-research-output.md:Dashboard Architecture
description: Dashboard described as React 19 SPA on Node 24 backend, port 8082; official docs say compiled into gc Go binary, port 8372.
evidence: Gemini "port 8082... statically served by a Node 24 backend" vs watcher-layer "[OFFICIAL] compiled into the gc binary, served at http://127.0.0.1:8372/".
suggestion: Correct port to 8372 and serving model to gc binary.

id: ACCURACY-E-005 | severity: minor | dimension: correctness | location: gemini-deep-research-output.md:Executive Summary
description: Claims stable release v1.4.0 as of 2026-08-21; three corpus files confirm v1.4.1 (2026-08-15).
evidence: Gemini "operates on the stable v1.4.0 release" vs handson/watcher/maturity "v1.4.1, 2026-08-15".
suggestion: Update to v1.4.1 and check downstream v1.4.0-as-current references.

id: ACCURACY-E-006 | severity: low | dimension: traceability | location: gemini-deep-research-output.md:Status of the Gate Vocabulary
description: [steps.gate] parsing attributed to internal/convergence/formula.go; corpus code-reads place it in internal/formula/{compile.go,types.go}; convergence module is the v1-only converge validator.
evidence: Gemini "internal/convergence/formula.go engine parses the gate constructs" vs handson "RecipeGate... in internal/formula/compile.go".
suggestion: Correct module citation.
