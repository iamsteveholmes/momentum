# Validator: structural / Enumerator (sonnet) — 6 findings (0 critical, 3 major, 2 minor, 1 low)
STRUCTURAL-E-001 | minor | structural_validity | gemini-deep-research-output.md:frontmatter | missing sub_question field; extra method/extracted fields vs corpus schema.
STRUCTURAL-E-002 | major | structural_validity/completeness | gemini-deep-research-output.md:entire body | zero evidence tags ([OFFICIAL]/[PRAC]/[UNVERIFIED]/[EMPIRICAL]) despite dozens of checkable claims; all other files tag nearly every sentence.
STRUCTURAL-E-003 | major | completeness | gemini-deep-research-output.md | no "## Sources" section (only trailing "## Follow-Up"); all 8 other files close with Sources URL list.
STRUCTURAL-E-004 | major | completeness | gemini-deep-research-output.md:Follow-Up Q3 | "### Q3: Dolt operational burden + file-backed beads status" heading followed by NO answer text (EOF); Q1/Q2 have full answers.
STRUCTURAL-E-005 | low | structural_validity | gemini-deep-research-output.md:frontmatter | date: 2026-08-21 vs extracted: 2026-08-24 and mtime Aug 24 — clarify schema meaning or update date.
STRUCTURAL-E-006 | minor | cross_reference_integrity | gemini-deep-research-output.md:Follow-Up Q1 | await_type defect attributed to gastownhall/beads#1467, uncorroborated; four sibling files consistently cite gascity#4399 for the same defect. Verify before relying.
