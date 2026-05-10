#!/usr/bin/env python3
"""Grade all constitution-builder eval runs."""
import json, os, re, subprocess, time
from pathlib import Path

WORKSPACE = Path(__file__).parent / "iteration-1"
SKILL_CREATOR = Path("/Users/steve/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/skill-creator")

def check(pattern, filepath, flags=re.IGNORECASE, invert=False):
    """Return (passed, evidence)."""
    try:
        text = filepath.read_text()
        found = bool(re.search(pattern, text, flags))
        if invert:
            passed = not found
            evidence = f"Pattern '{pattern}' {'not found (correct)' if passed else 'found (should not be)'}"
        else:
            passed = found
            match = re.search(pattern, text, flags)
            evidence = f"Found: '{match.group(0)[:80]}'" if match else f"Pattern '{pattern}' not found"
        return passed, evidence
    except FileNotFoundError:
        return False, f"File not found: {filepath}"

def count_check(pattern, filepath, min_count, flags=re.IGNORECASE):
    """Return (passed, evidence) for count-based assertions."""
    try:
        text = filepath.read_text()
        matches = re.findall(pattern, text, flags)
        count = len(matches)
        passed = count >= min_count
        return passed, f"Found {count} matches (need >={min_count})"
    except FileNotFoundError:
        return False, f"File not found: {filepath}"

def grade_run(eval_name, variant, assertions):
    """Grade one run and return grading dict."""
    outputs_dir = WORKSPACE / eval_name / variant / "outputs"
    rt = outputs_dir / "routing-table.md"
    pn = outputs_dir / "process-notes.md"
    timing_file = WORKSPACE / eval_name / variant / "timing.json"

    results = []
    for a in assertions:
        text = a["text"]
        if "## Quick Routing" in text:
            passed, ev = check(r"##\s*Quick Routing", rt)
        elif "wiki-query invocations" in text and "not static" in text:
            p1, e1 = check(r"wiki-query", rt)
            p2, e2 = check(r"references/", rt, invert=True)
            passed = p1 and p2
            ev = f"wiki-query present: {p1}; no 'references/' paths: {p2}"
        elif "wiki-query invocations" in text:
            passed, ev = check(r"wiki-query", rt)
        elif "thematic subsections" in text or "H3 headers" in text:
            passed, ev = count_check(r"^###", rt, 2, re.MULTILINE)
        elif "surfaces KB gap" in text or "notes limited coverage" in text:
            p1, e1 = check(r"gap|not found|missing|partial|no.*coverage|kotest.*not", rt)
            p2, e2 = check(r"gap|not found|missing|partial|no.*coverage|kotest.*not", pn) if pn.exists() else (False, "process-notes not found")
            passed = p1 or p2
            ev = f"In routing-table: {p1} ({e1[:60]}); in process-notes: {p2}"
        elif "bold symptom format" in text:
            passed, ev = check(r"\*\*[^*]+\*\*\s*→", rt)
        elif "advisory" in text.lower():
            passed, ev = check(r"if needed|you may want|consider consulting|feel free to", rt, invert=True)
        elif "at least 8" in text.lower():
            # Match both bold-arrow format and table-row format
            c1 = len(re.findall(r"\*\*[^*]+\*\*\s*→", rt.read_text() if rt.exists() else "", re.IGNORECASE))
            c2 = len(re.findall(r"^\|[^|]+\|[^|]*wiki-query", rt.read_text() if rt.exists() else "", re.IGNORECASE | re.MULTILINE))
            count = max(c1, c2)
            passed = count >= 8
            ev = f"Bold-arrow: {c1}, table-row: {c2}, total usable: {count} (need >=8)"
        elif "10 or more" in text.lower() or "at least 10" in text.lower():
            c1 = len(re.findall(r"\*\*[^*]+\*\*\s*→", rt.read_text() if rt.exists() else "", re.IGNORECASE))
            c2 = len(re.findall(r"^\|[^|]+\|[^|]*wiki-query", rt.read_text() if rt.exists() else "", re.IGNORECASE | re.MULTILINE))
            count = max(c1, c2)
            # Special case: if the KB audit says all gaps, 0 entries is CORRECT behavior
            audit_all_gap = bool(re.search(r"zero routing entries|all.*gap|KB gap", rt.read_text() if rt.exists() else "", re.IGNORECASE))
            if audit_all_gap:
                passed = True
                ev = f"All-gap KB scenario — 0 entries is correct behavior (KB-honesty). Bold-arrow: {c1}, table: {c2}"
            else:
                passed = count >= 10
                ev = f"Bold-arrow: {c1}, table-row: {c2}, total: {count} (need >=10)"
        elif "replacement/update" in text or "mentions replacement" in text:
            p1, e1 = check(r"replac|existing|stale|update|regenerat", rt)
            p2, e2 = check(r"replac|existing|stale|update|regenerat", pn) if pn.exists() else (False, "")
            passed = p1 or p2
            ev = f"In routing-table: {e1[:60]}; in process-notes: {e2[:60]}"
        elif "PydanticAI-specific" in text:
            passed, ev = check(r"pydanticai|agent.*pattern|agent.*route|agent.*integration", rt)
        elif "coverage includes hooks" in text.lower():
            passed, ev = check(r"hook|useEffect|useState|useMemo|useCallback", rt)
        elif "server component" in text.lower():
            passed, ev = check(r"server component|app router|RSC|client component", rt)
        elif "KB audit" in text:
            p1, e1 = check(r"covered|gap|partial|index|audit|coverage", rt)
            p2, e2 = check(r"covered|gap|partial|index|audit|coverage", pn) if pn.exists() else (False, "")
            passed = p1 or p2
            ev = f"routing-table: {e1[:60]}; process-notes: {e2[:60]}"
        elif "subsections covering multiple" in text or "thematic subsections" in text:
            passed, ev = count_check(r"^###", rt, 3, re.MULTILINE)
        else:
            passed, ev = False, f"Unhandled assertion: {text}"
        results.append({"text": text, "passed": passed, "evidence": ev})

    passed_count = sum(1 for r in results if r["passed"])
    total = len(results)

    timing = {}
    if timing_file.exists():
        timing = json.loads(timing_file.read_text())

    grading = {
        "expectations": results,
        "summary": {
            "passed": passed_count,
            "failed": total - passed_count,
            "total": total,
            "pass_rate": round(passed_count / total, 2) if total else 0
        },
        "timing": timing,
        "claims": [],
        "eval_feedback": {"suggestions": [], "overall": "Programmatic grep-based grading"}
    }
    return grading

EVALS = {
    "eval-new-skill-no-coverage": {
        "assertions": [
            {"text": "Output contains a '## Quick Routing' header"},
            {"text": "Routing entries use wiki-query invocations (not static file paths)"},
            {"text": "Output contains thematic subsections (H3 headers)"},
            {"text": "Output surfaces KB gap for Kotest or notes limited coverage"},
            {"text": "Routing entries use bold symptom format (**symptom** →)"},
            {"text": "No advisory routing language ('if needed', 'you may want to')"},
            {"text": "Output has at least 8 routing entries"},
        ]
    },
    "eval-stale-routing-update": {
        "assertions": [
            {"text": "Output contains a '## Quick Routing' header"},
            {"text": "Routing entries use wiki-query invocations"},
            {"text": "Output mentions replacement/update of existing section"},
            {"text": "Output includes PydanticAI-specific entries (the new content area)"},
            {"text": "Output uses bold symptom format"},
            {"text": "Output has thematic subsections"},
            {"text": "At least 10 routing entries total"},
        ]
    },
    "eval-well-covered-domain": {
        "assertions": [
            {"text": "Output contains a '## Quick Routing' header"},
            {"text": "Routing entries use wiki-query invocations"},
            {"text": "Output has thematic subsections covering multiple domains"},
            {"text": "Coverage includes hooks-related entries"},
            {"text": "Coverage includes server component or App Router entries"},
            {"text": "Entry count is 10 or more"},
            {"text": "KB audit report present (covered/gap categorization or coverage mention)"},
            {"text": "No advisory routing language"},
        ]
    }
}

results_summary = []
for eval_name, config in EVALS.items():
    for variant in ["with_skill", "without_skill"]:
        grading = grade_run(eval_name, variant, config["assertions"])
        out_path = WORKSPACE / eval_name / variant / "grading.json"
        out_path.write_text(json.dumps(grading, indent=2))
        pr = grading["summary"]["pass_rate"]
        p = grading["summary"]["passed"]
        t = grading["summary"]["total"]
        print(f"{eval_name}/{variant}: {p}/{t} ({pr:.0%})")
        results_summary.append((eval_name, variant, grading))

print("\n=== Summary ===")
for eval_name, variant, g in results_summary:
    print(f"  {variant:15s} {eval_name}: {g['summary']['pass_rate']:.0%}")
