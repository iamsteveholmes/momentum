---
date: 2026-04-13
file_fixed: raw/research-spec-correct-value-zero.md
---

# Fix Log — research-spec-correct-value-zero.md

## FIX 1 — CRITICAL-005: MIT Project NANDA unverifiable claim (APPLIED)

**Location:** "What Practitioners Report Is Not Working" section, under "Treating spec completion as done."

**Original text:** "The MIT Project NANDA finding that 95% of corporate AI projects show no measurable return suggests the spec-to-value problem is widespread at the organizational level, not just the story level."

**Replacement:** Blockquote `[UNVERIFIED]` note explaining the figure appears in secondary sources but could not be traced to a verifiable primary MIT publication, and directing readers to the BCG "Widening AI Value Gap" report as a well-sourced alternative.

---

## FIX 2 — HIGH-001: topic field (SKIPPED — already corrected by prior sed pass)

No action needed. The frontmatter `topic` field was already correct at time of edit.

---

## FIX 3 — HIGH-003: Forrester 95% Agile relevance statistic (NOT PRESENT)

Searched the file for "Forrester" and "95%" patterns. The Forrester 95% statistic tagged `[OFFICIAL — Forrester, 2025]` does not appear in this file. No action taken.

---

## FIX 4 — arxiv contradictory tags (NOT PRESENT)

Searched the file for `[UNVERIFIED]` occurrences. Prior to Fix 1, no `[UNVERIFIED]` tags existed in the file. All three arxiv papers (2602.00180v1, 2603.25773, 2508.20563v1) are tagged `[OFFICIAL]` inline and have full URLs in the Sources section — consistent, no contradiction. No action taken.
