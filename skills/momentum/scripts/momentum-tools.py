#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""
momentum-tools — Deterministic CLI for Momentum sprint and story operations.

Sole writer of stories/index.json and sprints/index.json. Also the sole writer of
feature status and last_verified in features.json (DEC-040 D1 — `feature verify`).
All operations are deterministic state machine validations + JSON mutations.

Usage:
    momentum-tools.py sprint status-transition --story SLUG --target STATUS [--force]
    momentum-tools.py sprint activate
    momentum-tools.py sprint complete  (refuses unless goal_conditions/verified-fix gate passes)
    momentum-tools.py sprint complete --verdict failed --reason "TEXT"  (honest FAILED terminal state)
    momentum-tools.py sprint complete --fix-confirmed "ENTRY_OR_INDEX" [--fix-confirmed ...] --build BACKEND_SHA:CLIENT_SHA  (maintenance sprint, no goal_conditions)
    momentum-tools.py sprint complete --punt-decision REF  (required when a goal-critical story is closed-incomplete/dropped and a condition is not verified-pass)
    momentum-tools.py sprint epic-membership --story SLUG --epic SLUG
    momentum-tools.py sprint plan --operation add|remove --stories SLUG[,SLUG,...] [--wave N] [--slug SPRINT_SLUG]
    momentum-tools.py sprint plan --goal "GOAL TEXT" --goal-conditions "slug-a,slug-b"  (or "" for a maintenance sprint; --operation/--stories optional here)
    momentum-tools.py sprint story-add --slug SLUG --title TITLE --epic EPIC [--priority PRIORITY] [--depends-on SLUG[,SLUG,...]]
    momentum-tools.py sprint story-set-contract --slug SLUG --verification-method METHOD --contract-path PATH --harness-profile PROFILE --coverage-disposition DISPOSITION [--covered-by-scenario SCENARIO] --frozen-sha256 SHA256 --can-merge-independently BOOL
    momentum-tools.py sprint compute-verification-method --story SLUG
    momentum-tools.py specialist-classify --touches "path1,path2,..."  (retired no-op shim — always resolves to dev; use "agent resolve")
    momentum-tools.py agent resolve --touches "path1,path2,..."
    momentum-tools.py agent resolve --role qa-reviewer
    momentum-tools.py quickfix register --slug SLUG --story STORY_KEY
    momentum-tools.py quickfix complete --slug SLUG
    momentum-tools.py practice-ledger append --entity-id ID --event-type TYPE --source SRC --actor ACTOR --payload JSON [--custom-event-type TYPE]
    momentum-tools.py practice-ledger consume --entity-id ID --actor ACTOR [--source SRC] [--outcome-ref REF]
    momentum-tools.py practice-ledger summary [--format json|text]
    momentum-tools.py practice-ledger open
    momentum-tools.py practice-ledger history --entity ID
    momentum-tools.py practice-ledger since ISO_TS
    momentum-tools.py practice-ledger by-source SOURCE
    momentum-tools.py practice-ledger close-stale [--age-days N]
    momentum-tools.py version check
    momentum-tools.py feature verify FEATURE_SLUG --verdict pass|fail --evidence TEXT --build BACKEND_SHA:CLIENT_SHA
    momentum-tools.py tasting brief [--json]  (writes .momentum/tasting/brief-<date>.md; read-only against features.json)
    momentum-tools.py tasting status [--json]  (due-ness, days-since, prominence tier: quiet/insistent/leading)
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import NoReturn

# --- State Machine ---

ORDERED_STATES = ["backlog", "ready-for-dev", "in-progress", "review", "verify", "done"]
TERMINAL_STATES = {"done", "dropped", "closed-incomplete"}
ALL_STATES = set(ORDERED_STATES) | TERMINAL_STATES


def validate_transition(current: str, target: str, force: bool = False) -> str | None:
    """Return error message if transition is invalid, None if valid."""
    if force:
        return None
    if target not in ALL_STATES:
        return f"Unknown target state: {target}"
    if current in TERMINAL_STATES:
        return f"Cannot transition from terminal state '{current}' without --force"
    if target in {"dropped", "closed-incomplete"}:
        return None  # always valid from non-terminal
    if current not in ORDERED_STATES:
        return f"Unknown current state: {current}"
    if target not in ORDERED_STATES:
        return f"Unknown target state: {target}"
    current_idx = ORDERED_STATES.index(current)
    target_idx = ORDERED_STATES.index(target)
    if target_idx != current_idx + 1:
        direction = "backward" if target_idx < current_idx else "non-adjacent forward"
        return f"Invalid {direction} transition: {current} -> {target}. Use --force to override"
    return None


# --- File I/O ---

def resolve_project_dir() -> Path:
    """Resolve project root from env or git."""
    import os
    env_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_dir:
        return Path(env_dir)
    # Walk up to find .git
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".git").exists():
            return parent
    print("Error: Cannot determine project root. Set CLAUDE_PROJECT_DIR or run from a git repo.", file=sys.stderr)
    sys.exit(1)


def stories_path(project_dir: Path) -> Path:
    return project_dir / ".momentum" / "stories" / "index.json"


def sprints_path(project_dir: Path) -> Path:
    return project_dir / ".momentum" / "sprints" / "index.json"


def features_path(project_dir: Path) -> Path:
    return project_dir / ".momentum" / "features.json"


def read_json(path: Path) -> dict:
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def result(action: str, success: bool, **kwargs) -> NoReturn:
    """Print JSON result and exit."""
    output = {"action": action, "success": success, **kwargs}
    print(json.dumps(output, indent=2))
    sys.exit(0 if success else 1)


def error_result(action: str, message: str, **kwargs) -> NoReturn:
    """Print error JSON result and exit with code 1."""
    result(action, success=False, error=message, **kwargs)


# --- Sprint Commands ---

def cmd_status_transition(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = stories_path(project_dir)
    stories = read_json(path)

    slug = args.story
    if slug not in stories:
        error_result("status_transition", f"Story '{slug}' not found in stories/index.json", story=slug)

    current = stories[slug]["status"]
    target = args.target
    err = validate_transition(current, target, args.force)
    if err:
        error_result("status_transition", err, story=slug, current=current, target=target)

    stories[slug]["status"] = target
    ensure_priority(stories[slug])
    write_json(path, stories)
    result("status_transition", success=True, story=slug, **{"from": current, "to": target})


def _compute_story_sha(project_dir: Path, slug: str) -> str | None:
    """Compute SHA-256 of the story file for the given slug.

    Returns the hex digest string, or None if the file does not exist.
    """
    story_file = project_dir / ".momentum" / "stories" / f"{slug}.md"
    if not story_file.exists():
        return None
    return hashlib.sha256(story_file.read_bytes()).hexdigest()


def _verify_approvals(project_dir: Path, sprint: dict) -> list[str]:
    """Check that every story in sprint has an approved entry with a matching SHA.

    Returns a list of story slugs that fail verification (missing or SHA mismatch).
    An empty list means all stories are approved.
    """
    stories = sprint.get("stories", [])
    approvals = sprint.get("approvals", [])

    # Build a lookup: slug -> approval entry
    approval_map = {a["story_slug"]: a for a in approvals if "story_slug" in a}

    missing = []
    for slug in stories:
        entry = approval_map.get(slug)
        if entry is None or entry.get("decision") != "approved":
            missing.append(slug)
            continue
        # Check SHA
        current_sha = _compute_story_sha(project_dir, slug)
        if current_sha is None or current_sha != entry.get("story_file_sha"):
            missing.append(slug)

    return missing


def cmd_sprint_story_approve(args: argparse.Namespace) -> None:
    """Record a per-story approval or rejection in planning.approvals."""
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    if not sprints.get("planning"):
        error_result("sprint_story_approve", "No planning sprint exists")

    planning = sprints["planning"]
    slug = args.slug
    decision = args.decision

    if slug not in planning.get("stories", []):
        error_result("sprint_story_approve",
                     f"Story '{slug}' is not in the planning sprint's stories list",
                     story=slug)

    # Compute SHA
    story_sha = _compute_story_sha(project_dir, slug)
    if story_sha is None:
        # Story file not found at .momentum/stories/{slug}.md — this is expected for
        # rejected decisions where no story file has been written yet. Record an empty
        # SHA explicitly so downstream SHA-match checks will flag this entry as
        # unverifiable rather than silently treating it as valid.
        story_sha = ""

    # Build the new entry
    approved_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_entry = {
        "story_slug": slug,
        "decision": decision,
        "approved_at": approved_at,
        "story_file_sha": story_sha,
    }

    # Initialize approvals array if absent
    if "approvals" not in planning:
        planning["approvals"] = []

    # Replace existing entry for this slug, or append
    existing = planning["approvals"]
    replaced = False
    for i, entry in enumerate(existing):
        if entry.get("story_slug") == slug:
            existing[i] = new_entry
            replaced = True
            break
    if not replaced:
        existing.append(new_entry)

    write_json(path, sprints)
    result("sprint_story_approve", success=True, story=slug, decision=decision,
           story_file_sha=story_sha, approved_at=approved_at, replaced=replaced)


def cmd_sprint_verify_approvals(args: argparse.Namespace) -> None:
    """Verify that all stories in a sprint have matching approved entries."""
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    scope = args.scope  # "planning" or "active"
    sprint = sprints.get(scope)
    if not sprint:
        error_result("sprint_verify_approvals",
                     f"No {scope} sprint exists",
                     scope=scope)

    missing = _verify_approvals(project_dir, sprint)
    if missing:
        error_result("sprint_verify_approvals",
                     f"Stories missing approval: {', '.join(missing)}",
                     scope=scope,
                     missing=missing)

    result("sprint_verify_approvals", success=True, scope=scope, missing=[])


def cmd_sprint_activate(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    if not sprints.get("planning"):
        error_result("sprint_activate", "No planning sprint exists to activate")
    if sprints.get("active"):
        error_result("sprint_activate", "An active sprint already exists. Complete it first.")

    planning = sprints["planning"]

    # Approval verification gate (AC 6)
    missing = _verify_approvals(project_dir, planning)
    if missing:
        error_result("sprint_activate",
                     f"Stories missing approval: {', '.join(missing)}",
                     missing=missing)

    planning["locked"] = True
    planning["started"] = date.today().isoformat()
    planning["status"] = "active"
    sprints["active"] = planning
    sprints["planning"] = None
    write_json(path, sprints)

    slug = planning.get("slug", "unknown")
    result("sprint_activate", success=True, sprint=slug, started=planning["started"])


_UNVERIFIED_REASONS = ("missing-entry", "no-verdict", "no-build-shas")
_DECISIONS_DIR_REL = "_bmad-output/planning-artifacts/decisions"


def _read_json_object(path: Path) -> dict | None:
    """Read a JSON file as a dict. Returns None (never raises) when the file is absent,
    unreadable, or not a JSON object."""
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    return data


def _load_features_registry(project_dir: Path) -> dict | None:
    """Read .momentum/features.json. Returns None (never an implicit pass) when the
    registry is absent, unreadable, or not a JSON object. Read-only — `feature verify`
    is the sole writer (DEC-040 D1)."""
    return _read_json_object(features_path(project_dir))


def _condition_result(slug: str, state: str, *, reason=None, status=None, verdict=None,
                       backend_sha=None, client_sha=None) -> dict:
    """Shared shape for a goal_conditions classification result."""
    return {"slug": slug, "state": state, "reason": reason,
            "status": status, "verdict": verdict,
            "backend_sha": backend_sha, "client_sha": client_sha}


def _unverified_condition(slug: str, reason: str, *, status=None, verdict=None,
                           backend_sha=None, client_sha=None) -> dict:
    """Build an unverified classification result. Guardrail: `reason` must be one of
    the closed-set tokens in `_UNVERIFIED_REASONS` — a caller passing anything else is a
    bug in this module, not a data problem, so it fails loudly rather than emitting a
    fourth reason token silently."""
    assert reason in _UNVERIFIED_REASONS, f"invalid unverified reason token: {reason!r}"
    return _condition_result(slug, "unverified", reason=reason, status=status, verdict=verdict,
                              backend_sha=backend_sha, client_sha=client_sha)


def _classify_goal_condition(registry: dict | None, slug: str) -> dict:
    """Classify one goal_conditions feature slug into verified-pass, recorded-fail, or
    unverified with a closed-set reason token (missing-entry|no-verdict|no-build-shas).
    Read-only — never writes .momentum/features.json (AC 1, 2)."""
    entry = (registry or {}).get(slug)
    if not isinstance(entry, dict) or entry.get("status") == "absent":
        return _unverified_condition(
            slug, "missing-entry",
            status=entry.get("status") if isinstance(entry, dict) else None)

    status = entry.get("status")
    last_verified = entry.get("last_verified")
    if not isinstance(last_verified, dict):
        return _unverified_condition(slug, "no-verdict", status=status)

    verdict = last_verified.get("verdict")
    backend_sha = last_verified.get("backend_sha")
    client_sha = last_verified.get("client_sha")
    has_shas = bool(backend_sha) and bool(client_sha)

    if not has_shas:
        return _unverified_condition(slug, "no-build-shas", status=status, verdict=verdict,
                                      backend_sha=backend_sha, client_sha=client_sha)

    if verdict == "fail":
        return _condition_result(slug, "recorded-fail", status=status, verdict=verdict,
                                  backend_sha=backend_sha, client_sha=client_sha)

    if verdict == "pass" and status == "passing":
        return _condition_result(slug, "verified-pass", status=status, verdict=verdict,
                                  backend_sha=backend_sha, client_sha=client_sha)

    # A complete last_verified block (verdict + both SHAs) in a shape `feature verify`
    # never produces (e.g. verdict "pass" without status "passing"). Never an implicit
    # pass — fall back to the closest unverified reason.
    return _unverified_condition(slug, "no-verdict", status=status, verdict=verdict,
                                  backend_sha=backend_sha, client_sha=client_sha)


def _condition_summary(c: dict) -> str:
    if c["state"] == "verified-pass":
        return f"pass — build {c['backend_sha']}:{c['client_sha']}"
    if c["state"] == "recorded-fail":
        return f"fail — build {c['backend_sha']}:{c['client_sha']}"
    if c["reason"] == "no-build-shas":
        return f"verdict {c['verdict']} recorded without paired build SHAs"
    return "no verdict recorded"


_FIX_LIST_LEAD_IN_RE = re.compile(r"^\s*verified fixes:?\s*$", re.IGNORECASE)


def _parse_verified_fix_list(goal_text: str | None) -> list[str]:
    """Parse the maintenance-sprint verified-fix list out of the free-text `goal`
    string: the '- ' bullet lines after a 'Verified fixes:' lead-in line (AC 6). No
    structured fix-list field exists on the producer side — this is the only parse path."""
    if not goal_text:
        return []
    entries: list[str] = []
    in_list = False
    for line in goal_text.split("\n"):
        stripped = line.strip()
        if not in_list:
            if _FIX_LIST_LEAD_IN_RE.match(stripped):
                in_list = True
            continue
        if not stripped:
            continue
        if stripped.startswith("-"):
            entries.append(stripped[1:].strip())
    return entries


def _resolve_punt_decision(project_dir: Path, ref: str) -> Path | None:
    """Resolve a --punt-decision ref to a file under
    _bmad-output/planning-artifacts/decisions/, or None if it can't be found there."""
    decisions_dir = project_dir / Path(_DECISIONS_DIR_REL)
    rel = ref.strip()
    prefix = f"{_DECISIONS_DIR_REL}/"
    if rel.startswith(prefix):
        rel = rel[len(prefix):]
    for candidate in (decisions_dir / rel, decisions_dir / f"{rel}.md"):
        if candidate.is_file():
            return candidate
    return None


def _punt_decision_required(project_dir: Path, active: dict, condition_results: list[dict]) -> bool:
    """AC 7: a recorded decision is required when the sprint closes while any of its
    stories sits at closed-incomplete/dropped AND at least one declared condition is
    not verified-pass. Vacuously false when zero conditions are declared."""
    if not condition_results or not any(c["state"] != "verified-pass" for c in condition_results):
        return False
    story_slugs = active.get("stories", [])
    if not story_slugs:
        return False
    stories_idx = _read_json_object(stories_path(project_dir))
    if stories_idx is None:
        return False
    for slug in story_slugs:
        entry = stories_idx.get(slug)
        if isinstance(entry, dict) and entry.get("status") in ("closed-incomplete", "dropped"):
            return True
    return False


def cmd_sprint_complete(args: argparse.Namespace) -> None:
    """Sprint closure gate (DEC-040 D2/D3, tier 2): refuses to close a sprint as `done`
    unless every goal_conditions entry carries a recorded human verdict (or, for a
    maintenance sprint, its verified-fix list is confirmed). `--verdict failed` adds an
    honest terminal state that bypasses that requirement but never the punt-decision
    gate (AC 7). See the story's Acceptance Criteria for the full behavior contract."""
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    if not sprints.get("active"):
        error_result("sprint_complete", "No active sprint to complete")

    active = sprints["active"]
    slug = active.get("slug", "unknown")
    verdict = getattr(args, "verdict", None) or "done"
    reason = getattr(args, "reason", None)
    fix_confirmed_args: list[str] = getattr(args, "fix_confirmed", None) or []
    build_arg = getattr(args, "build", None)
    punt_decision_arg = getattr(args, "punt_decision", None)

    goal = active.get("goal")
    raw_conditions = active.get("goal_conditions")
    conditions = raw_conditions if isinstance(raw_conditions, list) else []

    registry = _load_features_registry(project_dir) if conditions else None
    condition_results = [_classify_goal_condition(registry, slug) for slug in conditions]

    fix_list_entries: list[str] = []
    fix_confirmations: list[dict] = []

    if verdict == "failed":
        if not reason or not reason.strip():
            error_result(
                "sprint_complete",
                "FAILED closure requires a non-empty --reason explaining why the sprint's "
                "goal was not verified.",
                slug=slug,
            )
    elif verdict == "done":
        if conditions:
            unverified = [c for c in condition_results if c["state"] == "unverified"]
            if unverified:
                error_result(
                    "sprint_complete",
                    "Cannot close as done: " + "; ".join(
                        f"{c['slug']} is unverified ({c['reason']})" for c in unverified
                    ),
                    blocking_conditions=[
                        {"slug": c["slug"], "reason": c["reason"]} for c in unverified
                    ],
                    slug=slug,
                )
            failed_conditions = [c for c in condition_results if c["state"] == "recorded-fail"]
            if failed_conditions:
                names = ", ".join(c["slug"] for c in failed_conditions)
                error_result(
                    "sprint_complete",
                    f"Cannot close as done: recorded FAIL on {names}. Close FAILED with a "
                    "--reason instead — that is the available honest exit.",
                    failing_conditions=[c["slug"] for c in failed_conditions],
                    slug=slug,
                )
            # Every declared condition is verified-pass — falls through to the punt check.
        else:
            fix_list_entries = _parse_verified_fix_list(goal)
            if not fix_list_entries:
                error_result(
                    "sprint_complete",
                    "Cannot close as done: no goal_conditions declared and no verified-fix "
                    "list found in the sprint's goal. Declare the sprint's conditions with "
                    "sprint plan --goal-conditions, or close FAILED with a --reason instead.",
                    slug=slug,
                )

            if not build_arg:
                error_result(
                    "sprint_complete",
                    "Maintenance closure requires --build <backendSha:clientSha> alongside "
                    "the --fix-confirmed entries.",
                    fix_list=fix_list_entries,
                    slug=slug,
                )
            backend_sha, client_sha, build_error = _parse_build_pair(build_arg)
            if build_error:
                error_result("sprint_complete", build_error, fix_list=fix_list_entries, slug=slug)

            text_to_index: dict[str, int] = {}
            for i, entry_text in enumerate(fix_list_entries):
                text_to_index.setdefault(entry_text, i)

            confirmed_indexes: set[int] = set()
            for raw in fix_confirmed_args:
                token = raw.strip()
                idx = None
                if token.isdigit():
                    candidate = int(token) - 1
                    if 0 <= candidate < len(fix_list_entries):
                        idx = candidate
                if idx is None:
                    idx = text_to_index.get(token)
                if idx is not None:
                    confirmed_indexes.add(idx)

            unconfirmed = [e for i, e in enumerate(fix_list_entries) if i not in confirmed_indexes]
            if unconfirmed:
                error_result(
                    "sprint_complete",
                    "Cannot close as done: unconfirmed verified-fix entries: "
                    + "; ".join(unconfirmed),
                    fix_list=fix_list_entries,
                    unconfirmed=unconfirmed,
                    slug=slug,
                )
            fix_confirmations = [
                {"entry": e, "build": f"{backend_sha}:{client_sha}"} for e in fix_list_entries
            ]
    else:
        error_result("sprint_complete", f"Unknown --verdict '{verdict}'. Must be 'done' or 'failed'.",
                     slug=slug)

    # AC 7 — punt-decision requirement runs on both the done and failed paths.
    if _punt_decision_required(project_dir, active, condition_results):
        if not punt_decision_arg:
            error_result(
                "sprint_complete",
                "This sprint has stories at closed-incomplete or dropped while a declared "
                "condition is not verified-pass — closing requires --punt-decision <ref> "
                "naming the decision document that authorized punting the goal-critical work.",
                slug=slug,
            )
        if _resolve_punt_decision(project_dir, punt_decision_arg) is None:
            error_result(
                "sprint_complete",
                f"--punt-decision '{punt_decision_arg}' does not resolve to a document under "
                f"{_DECISIONS_DIR_REL}/.",
                slug=slug,
            )

    # --- Gate passed: perform the closure (AC 8 — the closure record tells the truth) ---
    active["completed"] = date.today().isoformat()
    active["status"] = "done" if verdict == "done" else "failed"
    active["retro_run_at"] = None
    active["closure"] = {
        "verdict": active["status"],
        "conditions": [
            {**c, "summary": _condition_summary(c)} for c in condition_results
        ],
        "fix_confirmations": fix_confirmations,
        "reason": reason if verdict == "failed" else None,
        "punt_decision": punt_decision_arg or None,
    }

    if "completed" not in sprints:
        sprints["completed"] = []
    sprints["completed"].append(active)
    sprints["active"] = None
    write_json(path, sprints)

    result("sprint_complete", success=True, sprint=slug, status=active["status"],
           completed=active["completed"], closure=active["closure"])


def cmd_epic_membership(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = stories_path(project_dir)
    stories = read_json(path)

    slug = args.story
    if slug not in stories:
        error_result("epic_membership", f"Story '{slug}' not found", story=slug)

    old_epic = stories[slug].get("epic_slug", "")
    stories[slug]["epic_slug"] = args.epic
    ensure_priority(stories[slug])
    write_json(path, stories)
    result("epic_membership", success=True, story=slug, from_epic=old_epic, to_epic=args.epic)


def cmd_sprint_plan(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    if not path.exists():
        # Bootstrap a fresh sprints/index.json — but only inside a project that already has
        # Momentum state (.momentum/stories/index.json present). Gating on that file restores
        # the wrong-cwd tripwire: running `sprint plan` in an arbitrary git repo with no
        # Momentum state at all is refused rather than silently seeding a new sprints file.
        if not stories_path(project_dir).exists():
            error_result(
                "sprint_plan",
                "No .momentum/stories/index.json found — this does not look like a Momentum "
                "project. Refusing to bootstrap .momentum/sprints/index.json in the wrong "
                "directory.",
            )
        path.parent.mkdir(parents=True, exist_ok=True)
        write_json(path, {"active": None, "planning": None, "completed": []})
    sprints = read_json(path)

    # Create planning entry if it doesn't exist
    if not sprints.get("planning"):
        sprints["planning"] = {"locked": False, "status": "planning", "stories": [], "waves": []}

    planning = sprints["planning"]
    if planning.get("locked"):
        error_result("sprint_plan", "Cannot modify a locked sprint")

    sprint_slug_arg = getattr(args, "slug", None)
    if sprint_slug_arg:
        planning["slug"] = sprint_slug_arg

    # goal / goal_conditions declaration (DEC-040 D1/D3) — optional, idempotent, applied
    # before any story add/remove, matching the existing --slug pattern.
    goal_arg = getattr(args, "goal", None)
    goal_conditions_arg = getattr(args, "goal_conditions", None)

    if goal_conditions_arg is not None:
        # dict.fromkeys dedupes while preserving first-seen order.
        parsed_conditions = list(dict.fromkeys(
            s.strip() for s in goal_conditions_arg.split(",") if s.strip()
        ))
    else:
        parsed_conditions = planning.get("goal_conditions", [])

    if goal_arg == "" and parsed_conditions:
        error_result(
            "sprint_plan",
            "--goal cannot be empty when goal_conditions is non-empty — a feature-backed or "
            "maintenance sprint still needs a plain-language goal sentence",
        )

    if goal_arg is not None:
        planning["goal"] = goal_arg

    if goal_conditions_arg is not None:
        planning["goal_conditions"] = parsed_conditions

    story_slugs: list[str] = []
    operation = getattr(args, "operation", None)
    stories_arg = getattr(args, "stories", None)
    wave_arg = getattr(args, "wave", None)
    if operation is None:
        if stories_arg:
            error_result("sprint_plan", "--stories requires --operation to be set (add or remove)")
        if wave_arg is not None:
            error_result("sprint_plan", "--wave requires --operation to be set (add or remove)")
    else:
        if not stories_arg:
            error_result("sprint_plan", "--stories is required when --operation is provided")
        story_slugs = [s.strip() for s in stories_arg.split(",")]

        if operation == "add":
            existing = set(planning.get("stories", []))
            for slug in story_slugs:
                if slug not in existing:
                    planning.setdefault("stories", []).append(slug)
            if args.wave is not None:
                waves = planning.setdefault("waves", [])
                # Find or create wave
                wave_entry = None
                for w in waves:
                    if w.get("wave") == args.wave:
                        wave_entry = w
                        break
                if not wave_entry:
                    wave_entry = {"wave": args.wave, "stories": []}
                    waves.append(wave_entry)
                    waves.sort(key=lambda w: w["wave"])
                existing_wave = set(wave_entry.get("stories", []))
                for slug in story_slugs:
                    if slug not in existing_wave:
                        wave_entry["stories"].append(slug)

        elif operation == "remove":
            planning["stories"] = [s for s in planning.get("stories", []) if s not in story_slugs]
            for wave in planning.get("waves", []):
                wave["stories"] = [s for s in wave.get("stories", []) if s not in story_slugs]
            # Remove empty waves
            planning["waves"] = [w for w in planning.get("waves", []) if w.get("stories")]

    write_json(path, sprints)
    result("sprint_plan", success=True, operation=operation, stories=story_slugs,
           slug=planning.get("slug"), goal=planning.get("goal"),
           goal_conditions=planning.get("goal_conditions"))


def cmd_sprint_story_set_contract(args: argparse.Namespace) -> None:
    """Persist the full contract block + verification_method + can_merge_independently
    into planning.team.story_assignments[slug] in sprints/index.json.

    Called once per story during sprint activation (Step 8 of sprint-planning workflow)
    after frozen contracts are written to disk and checksums computed.

    Required fields:
      --slug                Story slug
      --verification-method Closed-enum token (skill-invoke|behavioral-trigger|bash|smoke|curl|document-review)
      --contract-path       Relative path to the contract file from project root
      --harness-profile     Harness profile name (usually same as verification_method)
      --coverage-disposition  dedicated-run | covered-by-composition
      --covered-by-scenario   Scenario name (or empty/null for dedicated-run)
      --frozen-sha256       SHA-256 hex digest of the contract file at activation time
      --can-merge-independently  true|false (JSON boolean as string)
    """
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    if not sprints.get("planning"):
        error_result("sprint_story_set_contract", "No planning sprint exists")

    planning = sprints["planning"]
    if planning.get("locked"):
        error_result("sprint_story_set_contract", "Cannot modify a locked sprint")

    slug = args.slug
    if slug not in planning.get("stories", []):
        error_result("sprint_story_set_contract",
                     f"Story '{slug}' is not in the planning sprint's stories list",
                     story=slug)

    # Validate verification_method against closed enum — derived from single source of truth
    VALID_VERIFICATION_METHODS = set(SURFACE_TO_VERIFICATION_METHOD.values())
    vm = args.verification_method
    if vm not in VALID_VERIFICATION_METHODS:
        error_result("sprint_story_set_contract",
                     f"Invalid verification_method '{vm}'. Must be one of: "
                     f"{', '.join(sorted(VALID_VERIFICATION_METHODS))}",
                     story=slug)

    # Parse can_merge_independently — accept "true"/"false" strings or JSON booleans
    cmi_raw = args.can_merge_independently
    if isinstance(cmi_raw, bool):
        can_merge = cmi_raw
    elif isinstance(cmi_raw, str):
        if cmi_raw.lower() == "true":
            can_merge = True
        elif cmi_raw.lower() == "false":
            can_merge = False
        else:
            error_result("sprint_story_set_contract",
                         f"Invalid can_merge_independently '{cmi_raw}'. Must be true or false",
                         story=slug)
    else:
        can_merge = bool(cmi_raw)

    # Normalize covered_by_scenario — empty string or "null" → None
    covered_by = args.covered_by_scenario or None
    if covered_by in ("null", ""):
        covered_by = None

    # Build the contract block
    contract_block = {
        "path": args.contract_path,
        "harness_profile": args.harness_profile,
        "coverage_disposition": args.coverage_disposition,
        "covered_by_scenario": covered_by,
        "frozen_sha256": args.frozen_sha256,
    }

    # Ensure team.story_assignments structure exists
    if "team" not in planning:
        planning["team"] = {}
    if "story_assignments" not in planning["team"]:
        planning["team"]["story_assignments"] = {}

    assignments = planning["team"]["story_assignments"]
    if slug not in assignments:
        assignments[slug] = {}

    # Persist the new fields into the existing assignment entry
    assignments[slug]["verification_method"] = vm
    assignments[slug]["can_merge_independently"] = can_merge
    assignments[slug]["contract"] = contract_block

    write_json(path, sprints)
    result("sprint_story_set_contract", success=True,
           story=slug,
           verification_method=vm,
           can_merge_independently=can_merge,
           contract=contract_block)


# Closed enum: assembled surface → verification method token
# Source of truth: skills/momentum/references/rules/verification-standard.md §1
# (DEC-040 D7, amending DEC-029: routing key is now the declared assembled surface;
# change_type is demoted to an inference fallback — see CHANGE_TYPE_TO_SURFACE_INFERENCE
# below. The six-token method enum itself is unchanged.)
SURFACE_TO_VERIFICATION_METHOD: dict[str, str] = {
    "chat-ui": "smoke",
    "application-ui": "smoke",
    "http-endpoint": "curl",
    "cli": "bash",
    "skill-invocation": "skill-invoke",
    "hook-trigger": "behavioral-trigger",
    "artifact": "document-review",
}

# change_type → surface inference fallback. Consulted ONLY when a story declares no
# `surface` — a declared surface always wins and this table is never used to override
# one. Note `backend` infers to `application-ui` (→ smoke), NOT `http-endpoint` (→ curl):
# the old unconditional `backend → curl` mapping is gone. A story whose actual consumer
# is a raw HTTP client must declare `surface: http-endpoint` (or use the §2 override).
CHANGE_TYPE_TO_SURFACE_INFERENCE: dict[str, str] = {
    "skill-instruction": "skill-invocation",
    "agent-definition": "skill-invocation",
    "rule-hook": "hook-trigger",
    "script-code": "cli",
    "script-cli": "cli",
    "backend": "application-ui",
    "app-ui": "application-ui",
    "research-spike": "artifact",
    "specification": "artifact",
    "config-structure": "artifact",
}

# Back-compat derived view: change_type -> verification method, computed through the
# surface re-key above. The six-token *method* enum is unchanged by the re-key — only
# change_type's routing ROLE changed (routing key -> inference fallback). Named
# constant retained per verification-standard.md §1 AC10 (must stay a re-key'd,
# consistent copy alongside compute_verification_method), independent of whether any
# call site currently reads its values.
CHANGE_TYPE_TO_VERIFICATION_METHOD: dict[str, str] = {
    ct: SURFACE_TO_VERIFICATION_METHOD[surface]
    for ct, surface in CHANGE_TYPE_TO_SURFACE_INFERENCE.items()
}

# Multi-change-type precedence order (highest weight first) — consulted only during
# change_type inference (no declared surface).
CHANGE_TYPE_PRECEDENCE: list[str] = [
    "app-ui",
    "script-code",
    "script-cli",
    "backend",
    "agent-definition",
    "skill-instruction",
    "rule-hook",
    "config-structure",
    "specification",
    "research-spike",
]


def infer_surface_from_change_type(change_type_raw) -> str | None:
    """Infer an assembled surface from a story's change_type (inference fallback only).

    Consulted only when a story declares no `surface`. Handles multi-value change_type
    strings (e.g. "skill-instruction + code") by splitting on ' + ' / ',' and applying
    the precedence table to pick the highest-weight type. Tolerates a list/tuple
    change_type (e.g. a story-frontmatter YAML list mistakenly written to the index) by
    coercing it to the canonical "+"-joined string form.

    Returns None when nothing resolvable is found (empty, unknown, or all-unknown
    multi-value input) — callers fall back further (compute_verification_method degrades
    to 'document-review').
    """
    if not change_type_raw:
        return None

    # Defense-in-depth: coerce a list/tuple to the canonical string form before splitting.
    if isinstance(change_type_raw, (list, tuple)):
        change_type_raw = " + ".join(str(p) for p in change_type_raw if str(p).strip())
        if not change_type_raw:
            return None

    # Split on common separators used in the existing data
    import re as _re
    parts = [p.strip() for p in _re.split(r"\s*\+\s*|,\s*", change_type_raw) if p.strip()]

    # Filter to known types
    known = [p for p in parts if p in CHANGE_TYPE_TO_SURFACE_INFERENCE]

    if not known:
        return None

    if len(known) == 1:
        return CHANGE_TYPE_TO_SURFACE_INFERENCE[known[0]]

    # Multi-type: apply precedence order (first match wins)
    for ct in CHANGE_TYPE_PRECEDENCE:
        if ct in known:
            return CHANGE_TYPE_TO_SURFACE_INFERENCE[ct]

    # Unreachable if CHANGE_TYPE_PRECEDENCE covers all known types, but guard anyway
    return CHANGE_TYPE_TO_SURFACE_INFERENCE[known[0]]


def resolve_verification_routing(change_type_raw=None, surface=None) -> tuple[str, str | None, str]:
    """Resolve verification_method plus routing provenance in a single pass.

    Routing key is the declared assembled `surface` (verification-standard.md §1,
    DEC-040 D7). When `surface` is a valid token in the closed enum, its mapped method
    applies unconditionally and change_type is never consulted. Only when no surface is
    declared (or the declared token is not in the closed enum) does change_type supply a
    default inference via `infer_surface_from_change_type`.

    Preserves the pre-re-key graceful-degradation contract: empty, unknown, or
    list-valued change_type input still returns a valid method token ('document-review')
    rather than raising — load-bearing for in-flight sprints (verification-standard.md
    §1 AC11).

    Returns (verification_method, governing_surface, routed_by) so callers needing only
    the method and callers needing full routing visibility (§1 Visibility) share one
    resolution instead of maintaining two independent copies of the same branching.
    """
    if surface and surface in SURFACE_TO_VERIFICATION_METHOD:
        return SURFACE_TO_VERIFICATION_METHOD[surface], surface, "surface"

    inferred_surface = infer_surface_from_change_type(change_type_raw)
    if inferred_surface is not None:
        return SURFACE_TO_VERIFICATION_METHOD[inferred_surface], inferred_surface, "change_type_inference"

    return "document-review", None, "default_fallback"


def compute_verification_method(change_type_raw=None, surface=None) -> str:
    """Compute the closed-enum verification_method — surface-primary, change_type fallback.

    Thin wrapper over `resolve_verification_routing` for callers that only need the
    method token, not the routing provenance.
    """
    return resolve_verification_routing(change_type_raw, surface)[0]


def cmd_sprint_compute_verification_method(args: argparse.Namespace) -> None:
    """Compute verification_method for a story — surface-primary, change_type inference fallback.

    Reads the story's declared `surface` from stories/index.json first (the routing key
    per verification-standard.md §1, DEC-040 D7); falls back to change_type inference
    only when no valid surface is declared. Outputs which one governed (`routed_by`) and
    the resolved `governing_surface` so routing is never silent (§1 Visibility) — used by
    sprint-planning Step 3.5 to populate the Part-A contract header's `surface:` field.
    """
    project_dir = resolve_project_dir()
    path = stories_path(project_dir)
    stories = read_json(path)

    slug = args.story
    if slug not in stories:
        error_result("sprint_compute_verification_method",
                     f"Story '{slug}' not found in stories/index.json", story=slug)

    story = stories[slug]
    change_type = story.get("change_type", "")
    surface = story.get("surface") or None

    vm, governing_surface, routed_by = resolve_verification_routing(change_type, surface)

    result("sprint_compute_verification_method", success=True,
           story=slug,
           change_type=change_type,
           surface=surface,
           governing_surface=governing_surface,
           routed_by=routed_by,
           verification_method=vm,
           harness_profile=vm)  # harness_profile equals verification_method unless overridden


def cmd_sprint_ready(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    if not sprints.get("planning"):
        error_result("sprint_ready", "No planning sprint exists")

    sprints["planning"]["status"] = "ready"
    write_json(path, sprints)

    slug = sprints["planning"].get("slug", "unknown")
    result("sprint_ready", success=True, sprint=slug, status="ready")


def cmd_sprint_retro_complete(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    completed = sprints.get("completed", [])
    target = None
    for entry in reversed(completed):
        if entry.get("retro_run_at") is None:
            target = entry
            break

    if target is None:
        error_result("sprint_retro_complete", "No completed sprint with retro_run_at unset")

    target["retro_run_at"] = date.today().isoformat()

    auto_activated = False
    planning = sprints.get("planning")
    if planning and planning.get("status") == "ready":
        planning["locked"] = True
        planning["started"] = date.today().isoformat()
        planning["status"] = "active"
        sprints["active"] = planning
        sprints["planning"] = None
        auto_activated = True

    write_json(path, sprints)

    slug = target.get("slug", "unknown")
    result("sprint_retro_complete", success=True, sprint=slug,
           retro_run_at=target["retro_run_at"], auto_activated=auto_activated)


PRIORITY_LEVELS = ["critical", "high", "medium", "low"]
PRIORITY_ORDER = {p: i for i, p in enumerate(PRIORITY_LEVELS)}


def ensure_priority(story: dict) -> dict:
    """Return story with 'priority' field, defaulting to 'low' if absent."""
    if "priority" not in story:
        story["priority"] = "low"
    return story


def cmd_sprint_migrate_priority(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = stories_path(project_dir)
    stories = read_json(path)

    migrated = []
    for slug, story in stories.items():
        if "priority" not in story:
            story["priority"] = "low"
            migrated.append(slug)

    write_json(path, stories)
    result("migrate_priority", success=True, migrated=migrated, total=len(stories))


def cmd_sprint_set_priority(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = stories_path(project_dir)
    stories = read_json(path)

    slug = args.story
    if slug not in stories:
        error_result("set_priority", f"Story '{slug}' not found in stories/index.json", story=slug)

    priority = args.priority
    if priority not in PRIORITY_LEVELS:
        error_result("set_priority",
                     f"Invalid priority: '{priority}'. Must be one of: {', '.join(PRIORITY_LEVELS)}",
                     story=slug, priority=priority)

    old_priority = stories[slug].get("priority", "low")
    stories[slug]["priority"] = priority
    write_json(path, stories)
    result("set_priority", success=True, story=slug, old_priority=old_priority, new_priority=priority)


def cmd_sprint_stories(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = stories_path(project_dir)
    stories = read_json(path)

    priority_filter = args.priority

    if priority_filter == "all":
        groups: dict[str, list] = {p: [] for p in PRIORITY_LEVELS}
        for slug, story in stories.items():
            p = story.get("priority", "low")
            entry = {"slug": slug, **story}
            groups.get(p, groups["low"]).append(entry)
        result("sprint_stories", success=True, priority="all", groups=groups)
    else:
        if priority_filter not in PRIORITY_LEVELS:
            error_result("sprint_stories",
                         f"Invalid priority: '{priority_filter}'. Must be one of: {', '.join(PRIORITY_LEVELS)} or 'all'",
                         priority=priority_filter)
        matched = [
            {"slug": slug, **story}
            for slug, story in stories.items()
            if story.get("priority", "low") == priority_filter
        ]
        result("sprint_stories", success=True, priority=priority_filter, stories=matched)


def cmd_sprint_next_stories(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    sp = sprints_path(project_dir)
    st = stories_path(project_dir)
    sprints = read_json(sp)
    stories = read_json(st)

    active = sprints.get("active")
    if not active:
        error_result("sprint_next_stories", "No active sprint exists")

    sprint_stories = active.get("stories", [])
    sprint_slug = active.get("slug", "unknown")

    ready = []
    blocked = []
    done_list = []

    terminal = {"done", "dropped", "closed-incomplete"}

    for slug in sprint_stories:
        story = stories.get(slug, {})
        status = story.get("status", "backlog")

        if status in terminal:
            done_list.append(slug)
            continue

        depends_on = story.get("depends_on", [])
        waiting_on = []
        for dep in depends_on:
            dep_story = stories.get(dep, {})
            if dep_story.get("status") != "done":
                waiting_on.append(dep)

        if waiting_on:
            blocked.append({"slug": slug, "waiting_on": waiting_on})
        else:
            ready.append(slug)

    result("sprint_next_stories", success=True, sprint=sprint_slug,
           ready=ready, blocked=blocked, done=done_list)


# --- Session Commands ---

def cmd_session_stats_update(args: argparse.Namespace) -> None:
    import os

    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", resolve_project_dir()))
    installed_path = project_dir / ".claude" / "momentum" / "installed.json"

    if not installed_path.exists():
        error_result("session_stats_update", f"installed.json not found: {installed_path}")

    data = json.loads(installed_path.read_text(encoding="utf-8"))

    if "session_stats" not in data:
        data["session_stats"] = {"momentum_completions": 0, "last_invocation": None}

    data["session_stats"]["momentum_completions"] = data["session_stats"].get("momentum_completions", 0) + 1
    data["session_stats"]["last_invocation"] = datetime.now().isoformat()

    installed_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    result("session_stats_update", success=True,
           momentum_completions=data["session_stats"]["momentum_completions"],
           last_invocation=data["session_stats"]["last_invocation"])


def cmd_session_greeting_state(args: argparse.Namespace) -> None:
    import os

    project_dir = resolve_project_dir()
    claude_project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", project_dir))

    sp = sprints_path(project_dir)
    st = stories_path(project_dir)
    installed_path = claude_project_dir / ".claude" / "momentum" / "installed.json"

    sprints = read_json(sp) if sp.exists() else {"active": None, "planning": None, "completed": []}
    stories = read_json(st) if st.exists() else {}
    installed = json.loads(installed_path.read_text(encoding="utf-8")) if installed_path.exists() else {}

    session_stats = installed.get("session_stats", {})
    momentum_completions = session_stats.get("momentum_completions", 0)

    active = sprints.get("active")
    planning = sprints.get("planning")
    completed = sprints.get("completed", [])

    active_sprint = active.get("slug") if active else None
    planning_sprint = planning.get("slug") if planning else None
    planning_status = planning.get("status") if planning else None

    last_completed_sprint = completed[-1].get("slug") if completed else None

    no_sprints = active is None and planning is None and len(completed) == 0

    # State detection priority order from story
    if momentum_completions == 0 and no_sprints:
        state = "first-session-ever"
    elif active is None and planning is None:
        state = "no-active-nothing-planned"
    elif active is None and planning and planning.get("status") == "ready":
        state = "no-active-planned-ready"
    elif active and active.get("status") == "done" and planning is None:
        state = "done-no-planned"
    elif active and active.get("status") == "done":
        state = "done-retro-needed"
    elif active and active.get("status") == "active" and planning and planning.get("status") in ("planning", "ready"):
        state = "active-planned-needs-work"
    else:
        # Active sprint exists with status "active" — sub-detection
        sprint_stories = active.get("stories", []) if active else []

        # Check for blocked stories
        has_blocked = False
        all_not_started = True
        for slug in sprint_stories:
            story = stories.get(slug, {})
            status = story.get("status", "backlog")
            if status in ("done", "dropped", "closed-incomplete"):
                continue
            if status not in ("backlog", "ready-for-dev"):
                all_not_started = False
            depends_on = story.get("depends_on", [])
            for dep in depends_on:
                dep_story = stories.get(dep, {})
                if dep_story.get("status") != "done":
                    has_blocked = True

        if has_blocked:
            state = "active-blocked"
        elif all_not_started:
            state = "active-not-started"
        else:
            state = "active-in-progress"

    feature_status = _compute_feature_status(project_dir, claude_project_dir)

    output = {
        "state": state,
        "active_sprint": active_sprint,
        "planning_sprint": planning_sprint,
        "planning_status": planning_status,
        "momentum_completions": momentum_completions,
        "last_completed_sprint": last_completed_sprint,
        "feature_status": feature_status,
    }
    result("session_greeting_state", success=True, **output)


def cmd_session_journal_status(args: argparse.Namespace) -> None:
    import os

    project_dir = resolve_project_dir()
    claude_project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", project_dir))
    journal_path = claude_project_dir / ".claude" / "momentum" / "journal.jsonl"

    if not journal_path.exists():
        result("session_journal_status", success=True,
               exists=False, open_threads=0, last_entry=None)
        return

    # Scan all entries
    total_entries = 0
    parse_errors = 0
    last_entry = None
    # thread_id -> list of events in order
    thread_events: dict[str, list[dict]] = {}

    TERMINAL_EVENTS = {"thread_close", "session_end", "done"}

    for line in journal_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            parse_errors += 1
            continue

        total_entries += 1
        ts = entry.get("timestamp")
        if ts and (last_entry is None or ts > last_entry):
            last_entry = ts

        thread_id = entry.get("thread_id")
        if thread_id:
            thread_events.setdefault(thread_id, []).append(entry)

    # Build thread summary
    thread_summary = []
    open_threads = 0
    for thread_id, events in thread_events.items():
        last_event_entry = events[-1]
        last_event = last_event_entry.get("event", "")
        last_ts = last_event_entry.get("timestamp")
        status = "closed" if last_event in TERMINAL_EVENTS else "open"
        if status == "open":
            open_threads += 1
        thread_summary.append({
            "thread_id": thread_id,
            "status": status,
            "last_event": last_event,
            "last_timestamp": last_ts,
        })

    result("session_journal_status", success=True,
           exists=True,
           open_threads=open_threads,
           last_entry=last_entry,
           total_entries=total_entries,
           parse_errors=parse_errors,
           thread_summary=thread_summary)


def cmd_session_journal_hygiene(args: argparse.Namespace) -> None:
    import os
    import subprocess as sp
    from datetime import timedelta

    project_dir = resolve_project_dir()
    claude_project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", project_dir))
    journal_path = claude_project_dir / ".claude" / "momentum" / "journal.jsonl"

    TERMINAL_EVENTS = {"thread_close", "session_end", "done"}

    suggested_prompts = {
        "concurrent": '!  "{summary}" appears active in another tab ({minutes} minutes ago). Opening here may cause conflicts. Proceed anyway?',
        "dormant": "{summary} — {days} days inactive. Close this thread? [Y] Yes · [N] Keep open",
        "dependency_satisfied": 'The work "{dep_summary}" that "{summary}" was waiting on is complete — ready to continue?',
        "unwieldy": "!  {count} open threads — consider a quick triage before starting new work. Close any that are stale?",
    }

    empty_result = {
        "threads": [],
        "warnings": {
            "concurrent": [],
            "dormant": [],
            "dependency_satisfied": [],
            "unwieldy": None,
        },
        "suppressed_offers": [],
        "suggested_prompts": suggested_prompts,
        "open_count": 0,
        "total_count": 0,
    }

    if not journal_path.exists():
        result("session_journal_hygiene", success=True, **empty_result)
        return

    # Parse journal — group by thread_id, collect all entries in order
    thread_entries: dict[str, list[dict]] = {}
    for line in journal_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        tid = entry.get("thread_id")
        if tid:
            thread_entries.setdefault(tid, []).append(entry)

    # Build thread state — last entry per thread determines current state
    thread_states: list[dict] = []
    for tid, entries in thread_entries.items():
        last = entries[-1]
        last_event = last.get("event", "")
        status = "closed" if last_event in TERMINAL_EVENTS else "open"
        state = {**last, "status": status}
        thread_states.append(state)

    total_count = len(thread_states)

    # Filter to open threads only
    open_threads = [t for t in thread_states if t.get("status") == "open"]

    if not open_threads:
        empty_result["total_count"] = total_count
        result("session_journal_hygiene", success=True, **empty_result)
        return

    # Get current datetime and git hash (once per invocation)
    now = datetime.now()
    git_hash = "unknown"
    try:
        proc = sp.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5, cwd=str(project_dir)
        )
        if proc.returncode == 0:
            git_hash = proc.stdout.strip()
    except (sp.TimeoutExpired, FileNotFoundError):
        pass

    def parse_ts(ts_str: str) -> "datetime | None":
        if not ts_str:
            return None
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%f"):
            try:
                return datetime.strptime(ts_str, fmt)
            except ValueError:
                continue
        try:
            return datetime.fromisoformat(ts_str.replace("Z", "+00:00")).replace(tzinfo=None)
        except (ValueError, AttributeError):
            return None

    def elapsed_label(ts: datetime) -> str:
        delta = now - ts
        total_seconds = delta.total_seconds()
        if total_seconds < 3600:
            mins = max(1, int(total_seconds / 60))
            return f"{mins}m ago"
        if total_seconds < 86400:
            hours = int(total_seconds / 3600)
            return f"{hours}h ago"
        if total_seconds < 172800:
            return "yesterday"
        days = int(total_seconds / 86400)
        return f"{days}d ago"

    # Build enriched thread list with elapsed labels
    enriched: list[dict] = []
    for t in open_threads:
        ts_str = t.get("last_active") or t.get("timestamp", "")
        ts = parse_ts(ts_str)
        label = elapsed_label(ts) if ts else "unknown"
        enriched.append({
            "thread_id": t.get("thread_id", ""),
            "context_summary_short": t.get("context_summary_short", ""),
            "context_summary": t.get("context_summary", ""),
            "phase": t.get("phase", ""),
            "story_ref": t.get("story_ref", ""),
            "last_active": ts_str,
            "elapsed_label": label,
            "status": "open",
            # Internal fields for warning computation — stripped before output
            "_ts": ts,
            "_declined_offers": t.get("declined_offers", []),
            "_depends_on_thread": t.get("depends_on_thread"),
        })

    # Sort by last_active descending (most recent first)
    enriched.sort(key=lambda x: x["_ts"] or datetime.min, reverse=True)

    # Lookup for all thread states by thread_id (for dependency resolution)
    all_states_by_id = {t.get("thread_id", ""): t for t in thread_states}

    # Lookup for most recent context_summary_short per thread across all events
    # (thread_close events often lack context_summary_short; scan all entries)
    context_summary_by_tid: dict[str, str] = {}
    for tid, entries in thread_entries.items():
        for entry in reversed(entries):
            css = entry.get("context_summary_short")
            if css:
                context_summary_by_tid[tid] = css
                break

    # --- Warning computation ---
    concurrent: list[dict] = []
    dormant_raw: list[dict] = []
    dependency_satisfied: list[dict] = []

    thirty_min_ago = now - timedelta(minutes=30)
    three_days_ago = now - timedelta(days=3)

    for t in enriched:
        ts = t["_ts"]
        if ts is None:
            continue

        # Concurrent: active within 30 minutes of now
        if ts >= thirty_min_ago:
            minutes_ago = max(0, int((now - ts).total_seconds() / 60))
            concurrent.append({
                "thread_id": t["thread_id"],
                "context_summary_short": t["context_summary_short"],
                "minutes_ago": minutes_ago,
            })

        # Dormant: inactive more than 3 days
        if ts < three_days_ago:
            days_inactive = int((now - ts).total_seconds() / 86400)
            dormant_raw.append({
                "thread_id": t["thread_id"],
                "context_summary_short": t["context_summary_short"],
                "days_inactive": days_inactive,
                "_declined_offers": t["_declined_offers"],
                "_story_ref": t["story_ref"],
                "_phase": t["phase"],
            })

        # Dependency satisfied
        dep_tid = t["_depends_on_thread"]
        if dep_tid:
            dep_state = all_states_by_id.get(dep_tid)
            if dep_state and dep_state.get("status") == "closed":
                dep_summary = context_summary_by_tid.get(dep_tid, dep_tid)
                dependency_satisfied.append({
                    "thread_id": t["thread_id"],
                    "context_summary_short": t["context_summary_short"],
                    "depends_on_summary": dep_summary,
                })

    # Unwieldy: more than 5 open threads
    open_count = len(enriched)
    unwieldy = {"open_count": open_count} if open_count > 5 else None

    # --- No-Re-Offer suppression for dormant threads ---
    dormant: list[dict] = []
    suppressed_offers: list[dict] = []

    for d in dormant_raw:
        tid = d["thread_id"]
        story_ref = d["_story_ref"]
        phase = d["_phase"]
        context_hash = f"{tid}|{story_ref}|{phase}|{git_hash}"

        suppressed = any(
            offer.get("offer_type") == "dormant-closure"
            and offer.get("context_hash") == context_hash
            for offer in d["_declined_offers"]
        )

        if suppressed:
            suppressed_offers.append({
                "thread_id": tid,
                "offer_type": "dormant-closure",
                "reason": "declined, context unchanged",
            })
        else:
            dormant.append({
                "thread_id": tid,
                "context_summary_short": d["context_summary_short"],
                "days_inactive": d["days_inactive"],
            })

    # Strip internal fields before output
    threads_out = [{k: v for k, v in t.items() if not k.startswith("_")} for t in enriched]

    output = {
        "threads": threads_out,
        "warnings": {
            "concurrent": concurrent,
            "dormant": dormant,
            "dependency_satisfied": dependency_satisfied,
            "unwieldy": unwieldy,
        },
        "suppressed_offers": suppressed_offers,
        "suggested_prompts": suggested_prompts,
        "open_count": open_count,
        "total_count": total_count,
    }
    result("session_journal_hygiene", success=True, **output)


def _regenerate_journal_view(journal_path: Path, view_path: Path) -> None:
    """Regenerate journal-view.md from journal.jsonl."""
    from datetime import timedelta

    TERMINAL_EVENTS = {"thread_close", "session_end", "done"}

    if not journal_path.exists():
        return

    # Read and group by thread_id (last entry wins)
    thread_last: dict[str, dict] = {}
    for line in journal_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        tid = entry.get("thread_id")
        if tid:
            thread_last[tid] = entry

    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)

    def parse_ts_view(ts_str: str) -> "datetime | None":
        if not ts_str:
            return None
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%f"):
            try:
                return datetime.strptime(ts_str, fmt)
            except ValueError:
                continue
        try:
            return datetime.fromisoformat(ts_str.replace("Z", "+00:00")).replace(tzinfo=None)
        except (ValueError, AttributeError):
            return None

    rows = []
    for tid, entry in thread_last.items():
        last_event = entry.get("event", "")
        is_closed = last_event in TERMINAL_EVENTS

        ts_str = entry.get("last_active") or entry.get("timestamp", "")
        ts = parse_ts_view(ts_str)

        # For closed threads: only include if closed within 7 days
        if is_closed:
            if ts is None or ts < seven_days_ago:
                continue

        rows.append({
            "thread": entry.get("context_summary_short", ""),
            "story": entry.get("story_ref", ""),
            "phase": entry.get("phase", ""),
            "last_action": last_event,
            "last_active": ts_str,
            "status": "closed" if is_closed else "open",
            "_ts": ts,
            "_is_closed": is_closed,
        })

    # Sort: open threads first (most recent first), then recent closed (most recent first)
    open_rows = sorted(
        [r for r in rows if not r["_is_closed"]],
        key=lambda r: r["_ts"] or datetime.min,
        reverse=True,
    )
    closed_rows = sorted(
        [r for r in rows if r["_is_closed"]],
        key=lambda r: r["_ts"] or datetime.min,
        reverse=True,
    )
    rows = open_rows + closed_rows

    lines = [
        "# Journal View\n",
        "| Thread | Story | Phase | Last Action | Last Active | Status |",
        "|--------|-------|-------|-------------|-------------|--------|",
    ]
    for r in rows:
        thread = r["thread"].replace("|", "&#124;")
        story = r["story"].replace("|", "&#124;")
        phase = r["phase"].replace("|", "&#124;")
        last_action = r["last_action"].replace("|", "&#124;")
        lines.append(
            f"| {thread} | {story} | {phase} | {last_action} | {r['last_active']} | {r['status']} |"
        )

    view_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_session_journal_append(args: argparse.Namespace) -> None:
    import os

    project_dir = resolve_project_dir()
    claude_project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", project_dir))
    journal_dir = claude_project_dir / ".claude" / "momentum"
    journal_path = journal_dir / "journal.jsonl"
    view_path = journal_dir / "journal-view.md"

    entry_str = args.entry

    # Validate JSON
    try:
        entry_data = json.loads(entry_str)
    except json.JSONDecodeError as e:
        error_result("session_journal_append", f"Invalid JSON: {e}")
        return

    # Ensure journal directory exists
    journal_dir.mkdir(parents=True, exist_ok=True)

    # Atomic append: write to temp file, verify, then append to journal
    tmp_path = journal_dir / "journal.jsonl.tmp"
    line = json.dumps(entry_data, ensure_ascii=False)
    try:
        tmp_path.write_text(line + "\n", encoding="utf-8")
        # Verify temp file is valid JSON
        json.loads(tmp_path.read_text(encoding="utf-8").strip())
        # Append to journal
        with open(journal_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        tmp_path.unlink(missing_ok=True)
    except Exception as e:
        tmp_path.unlink(missing_ok=True)
        error_result("session_journal_append", f"Append failed: {e}")
        return

    # Regenerate journal-view.md
    _regenerate_journal_view(journal_path, view_path)

    result("session_journal_append", success=True,
           journal_path=str(journal_path),
           view_path=str(view_path))


def cmd_session_startup_preflight(args: argparse.Namespace) -> None:
    import os
    import subprocess as sp

    project_dir = resolve_project_dir()
    claude_project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", project_dir))

    versions_path = project_dir / "skills" / "momentum" / "references" / "momentum-versions.json"
    installed_path = claude_project_dir / ".claude" / "momentum" / "installed.json"
    global_installed_path = Path.home() / ".claude" / "momentum" / "global-installed.json"
    journal_path = claude_project_dir / ".claude" / "momentum" / "journal.jsonl"

    # Read versions manifest
    current_version = "0.0.0"
    versions_data: dict = {}
    if versions_path.exists():
        try:
            versions_data = json.loads(versions_path.read_text(encoding="utf-8"))
            current_version = versions_data.get("current_version", "0.0.0")
        except json.JSONDecodeError:
            pass

    # Read installed.json (project-scoped)
    installed_data: dict = {}
    if installed_path.exists():
        try:
            installed_data = json.loads(installed_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    # Read global-installed.json
    global_data: dict = {}
    if global_installed_path.exists():
        try:
            global_data = json.loads(global_installed_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass

    # Per-component version comparison (mirrors workflow Step 1 logic)
    # Collect unique groups and their scopes from the current version's actions
    version_actions = versions_data.get("versions", {}).get(current_version, {}).get("actions", [])
    groups: dict[str, str] = {}  # group_name -> scope
    for action in version_actions:
        group = action.get("group")
        scope = action.get("scope")
        if group and scope and group not in groups:
            groups[group] = scope

    needs_work: list[dict] = []
    for group_name, scope in groups.items():
        if scope == "global":
            group_version = global_data.get("components", {}).get(group_name, {}).get("version")
        else:
            group_version = installed_data.get("components", {}).get(group_name, {}).get("version")

        if group_version is None or group_version < current_version:
            needs_work.append({"group": group_name, "scope": scope, "installed_version": group_version})

    # Determine if any group has a version behind (upgrade) vs absent (first install)
    any_behind = any(g.get("installed_version") is not None for g in needs_work)
    all_absent = all(g.get("installed_version") is None for g in needs_work)
    both_files_empty = not installed_data.get("components") and not global_data.get("components")

    # Hash drift detection — resolve target paths from version manifest actions
    hash_drift = False
    hash_check_errors: list[str] = []
    if not needs_work:  # only check drift when all groups are current
        global_components = global_data.get("components", {})
        for comp_name, comp_info in global_components.items():
            if not isinstance(comp_info, dict):
                continue
            stored_hash = comp_info.get("hash")
            if not stored_hash:
                continue

            # Find the first add/replace action for this group to get the target path
            target = None
            for action in version_actions:
                if action.get("group") == comp_name and action.get("action") in ("add", "replace"):
                    target = action.get("target")
                    break

            if not target:
                continue

            target_path = Path(os.path.expanduser(target))
            if not target_path.exists():
                hash_check_errors.append(f"{comp_name}: target file missing ({target})")
                continue

            try:
                proc = sp.run(
                    ["git", "hash-object", str(target_path)],
                    capture_output=True, text=True, timeout=5
                )
                if proc.returncode == 0:
                    current_hash = proc.stdout.strip()
                    if current_hash != stored_hash:
                        hash_drift = True
                else:
                    hash_check_errors.append(f"{comp_name}: git hash-object failed (rc={proc.returncode})")
            except sp.TimeoutExpired:
                hash_check_errors.append(f"{comp_name}: git hash-object timed out")
            except FileNotFoundError:
                hash_check_errors.append(f"{comp_name}: git not found")

    # Journal thread check
    has_open_threads = False
    if journal_path.exists():
        try:
            threads: dict[str, dict] = {}
            for line in journal_path.read_text(encoding="utf-8").strip().splitlines():
                if not line.strip():
                    continue
                entry = json.loads(line)
                tid = entry.get("thread_id")
                if tid:
                    threads[tid] = entry
            has_open_threads = any(t.get("status") == "open" for t in threads.values())
        except (json.JSONDecodeError, KeyError):
            pass

    # Config gaps
    config_gaps: list[str] = []
    mcp_path = claude_project_dir / ".mcp.json"
    if mcp_path.exists():
        try:
            json.loads(mcp_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            config_gaps.append("invalid .mcp.json")

    # Route determination
    if needs_work and both_files_empty:
        route = "first-install"
    elif needs_work and any_behind:
        route = "upgrade"
    elif needs_work and all_absent:
        route = "first-install"
    elif hash_drift:
        route = "hash-drift"
    else:
        route = "greeting"

    # Inline greeting-state computation when route is "greeting"
    greeting = None
    if route == "greeting":
        _sp = sprints_path(project_dir)
        _st = stories_path(project_dir)
        sprints = read_json(_sp) if _sp.exists() else {"active": None, "planning": None, "completed": []}
        stories = read_json(_st) if _st.exists() else {}
        session_stats = installed_data.get("session_stats", {})
        momentum_completions = session_stats.get("momentum_completions", 0)

        active = sprints.get("active")
        planning = sprints.get("planning")
        completed = sprints.get("completed", [])

        active_sprint = active.get("slug") if active else None
        planning_sprint = planning.get("slug") if planning else None
        planning_status = planning.get("status") if planning else None
        last_completed_sprint = completed[-1].get("slug") if completed else None
        no_sprints = active is None and planning is None and len(completed) == 0

        if momentum_completions == 0 and no_sprints:
            state = "first-session-ever"
        elif active is None and planning is None:
            state = "no-active-nothing-planned"
        elif active is None and planning and planning.get("status") == "ready":
            state = "no-active-planned-ready"
        elif active and active.get("status") == "done" and planning is None:
            state = "done-no-planned"
        elif active and active.get("status") == "done":
            state = "done-retro-needed"
        elif active and active.get("status") == "active" and planning and planning.get("status") in ("planning", "ready"):
            state = "active-planned-needs-work"
        else:
            sprint_stories = active.get("stories", []) if active else []
            has_blocked = False
            all_not_started = True
            for slug in sprint_stories:
                story = stories.get(slug, {})
                status = story.get("status", "backlog")
                if status in ("done", "dropped", "closed-incomplete"):
                    continue
                if status not in ("backlog", "ready-for-dev"):
                    all_not_started = False
                for dep in story.get("depends_on", []):
                    dep_story = stories.get(dep, {})
                    if dep_story.get("status") != "done":
                        has_blocked = True

            if has_blocked:
                state = "active-blocked"
            elif all_not_started:
                state = "active-not-started"
            else:
                state = "active-in-progress"

        # --- Render greeting templates inline (eliminates session-greeting.md read) ---
        _vars = {
            "active_sprint": active_sprint or planning_sprint or "unknown",
            "planning_sprint": planning_sprint or "",
            "last_completed_sprint": last_completed_sprint or "",
        }

        _narratives = {
            "first-session-ever": "I am Impetus. I hold the line on engineering discipline \u2014 sprints, quality, the lifecycle of every story. You build. I make sure nothing falls through the cracks.\n\nThis is the beginning. Let\u2019s forge something worth building.",
            "active-not-started": 'The path is clear. Sprint \u201c{active_sprint}\u201d stands ready \u2014 waiting on you to lead the way.',
            "active-in-progress": 'Sprint \u201c{active_sprint}\u201d is underway \u2014 steady ground, nothing standing in our way.',
            "active-blocked": 'Sprint \u201c{active_sprint}\u201d \u2014 something stands in the way. One story needs you before we can move forward.',
            "active-planned-needs-work": 'Sprint \u201c{active_sprint}\u201d is underway \u2014 holding strong.',
            "done-retro-needed": 'Sprint \u201c{active_sprint}\u201d \u2014 the work is done. Every story carried across the line.',
            "done-no-planned": 'Sprint \u201c{active_sprint}\u201d \u2014 the work is done.',
            "no-active-nothing-planned": 'All still. The last sprint \u2014 \u201c{last_completed_sprint}\u201d \u2014 was carried to completion.',
            "no-active-planned-ready": '\u201c{planning_sprint}\u201d stands ready. The groundwork is laid.',
        }

        _planning_contexts = {
            "active-not-started": '\u201c{planning_sprint}\u201d is taking shape behind it.',
            "active-in-progress": '\u201c{planning_sprint}\u201d is taking shape behind it.',
            "active-blocked": '\u201c{planning_sprint}\u201d is taking shape behind it.',
            "active-planned-needs-work": '\u201c{planning_sprint}\u201d is coming together, but it needs more of your thinking before it\u2019s ready to stand on its own.',
            "done-retro-needed": '\u201c{planning_sprint}\u201d stands ready \u2014 it rises the moment we close this chapter.',
            "done-no-planned": 'Nothing yet follows it. A good moment to look ahead and decide what we build next.',
        }

        _menus = {
            "first-session-ever": ["Plan a sprint", "Refine backlog", "Triage"],
            "active-not-started": ["Run the sprint", "Refine backlog", "Triage"],
            "active-in-progress": ["Continue the sprint", "Refine backlog", "Triage"],
            "active-blocked": ["Continue the sprint", "Refine backlog", "Triage"],
            "active-planned-needs-work": ["Continue the sprint", "Finish planning", "Refine backlog", "Triage"],
            "done-retro-needed": ["Run retro", "Refine backlog", "Triage"],
            "done-no-planned": ["Run retro", "Plan a sprint", "Refine backlog", "Triage"],
            "no-active-nothing-planned": ["Plan a sprint", "Refine backlog", "Triage"],
            "no-active-planned-ready": ["Activate sprint", "Refine backlog", "Triage"],
        }

        _closers = {
            "first-session-ever": "Where do we begin?",
            "active-not-started": "Where do we begin?",
            "active-in-progress": "Lead on.",
            "active-blocked": "Let\u2019s face it together.",
            "active-planned-needs-work": "I\u2019m with you.",
            "done-retro-needed": "One last step to honor the work.",
            "done-no-planned": "The road is open.",
            "no-active-nothing-planned": "When you\u2019re ready, I\u2019m here.",
            "no-active-planned-ready": "Give the word.",
        }

        rendered_narrative = _narratives.get(state, "").format(**_vars)
        rendered_planning_context = (_planning_contexts.get(state) or "").format(**_vars) or None
        rendered_menu = [f"[{i+1}] {item}" for i, item in enumerate(_menus.get(state, []))]
        rendered_closer = _closers.get(state, "")

        feature_status = _compute_feature_status(project_dir, claude_project_dir)

        greeting = {
            "state": state,
            "active_sprint": active_sprint,
            "planning_sprint": planning_sprint,
            "planning_status": planning_status,
            "momentum_completions": momentum_completions,
            "last_completed_sprint": last_completed_sprint,
            "narrative": rendered_narrative,
            "planning_context": rendered_planning_context,
            "menu": rendered_menu,
            "closer": rendered_closer,
            "feature_status": feature_status,
        }

    result("session_startup_preflight", success=True,
           route=route,
           needs_work=[{"group": g["group"], "scope": g["scope"]} for g in needs_work],
           hash_drift=hash_drift,
           hash_check_errors=hash_check_errors,
           has_open_threads=has_open_threads,
           config_gaps=config_gaps,
           greeting=greeting,
           current_version=current_version)


# --- Plugin Cache Staleness Check ---

def _parse_semver(version_str: str) -> tuple:
    """Parse a version string into a comparable tuple with correct pre-release ordering.

    Handles standard MAJOR.MINOR.PATCH versions and pre-release suffixes of the form
    MAJOR.MINOR.PATCH-rcN (e.g. "0.17.0-rc1").

    Pre-release versions sort BEFORE their release counterpart per semver convention:
      0.17.0-rc1 < 0.17.0 < 0.17.1

    Non-conforming version strings (not MAJOR.MINOR.PATCH or MAJOR.MINOR.PATCH-rcN)
    are parsed on a best-effort basis with a stderr note, and pre-release suffixes
    are sorted after their numeric counterparts (legacy behaviour for unknown formats).

    Returns a 4-tuple (major, minor, patch, pre) where:
      pre = (0, rc_number) for pre-release versions (sorts before release)
      pre = (1, 0)         for release versions (sorts after pre-release)
      pre = (2, suffix)    for unrecognised non-numeric suffixes (sorts last)
    """
    import re as _re
    _SEMVER_RE = _re.compile(
        r'^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:-(?P<pre>.+))?$'
    )
    m = _SEMVER_RE.match(version_str)
    if m:
        major = int(m.group("major"))
        minor = int(m.group("minor"))
        patch = int(m.group("patch"))
        pre_str = m.group("pre")
        if pre_str is None:
            # Release version: sorts after any pre-release of the same M.M.P
            pre = (1, 0)
        else:
            rc_m = _re.match(r'^rc(\d+)$', pre_str)
            if rc_m:
                # RC pre-release: sorts before the release (pre-tag = 0)
                pre = (0, int(rc_m.group(1)))
            else:
                # Unknown pre-release tag: sort after release as a string
                pre = (2, pre_str)
        return (major, minor, patch, pre)
    else:
        # Non-conforming version string — fall back to component-wise parse with a note
        import sys as _sys
        print(
            f"_parse_semver: non-standard version '{version_str}' — "
            "sorting may be unreliable for pre-release comparisons",
            file=_sys.stderr,
        )
        parts = []
        for part in version_str.split("."):
            try:
                parts.append((0, int(part)))
            except ValueError:
                parts.append((1, part))
        return tuple(parts)


def cmd_session_plugin_cache_check(args: argparse.Namespace) -> None:
    """Check whether the active Claude Code plugin cache version matches the source-tree version.

    JSON output schema:
    {
      "action": "session_plugin_cache_check",
      "success": true,
      "status": "match" | "skew-cache-behind" | "skew-cache-ahead" | "no-cache" | "no-source" | "indeterminate",
      "cache_version": "<semver string>" | null,
      "source_version": "<semver string>" | null,
      "active_cache_dir": "<path string>" | null,
      "diagnostic": "<description of what failed>" | null  (present only when status is indeterminate)
    }

    Exit code is always 0. Callers parse the JSON to determine whether action is needed.
    """
    import os

    home = Path(os.environ.get("HOME", str(Path.home())))
    cache_root = home / ".claude" / "plugins" / "cache" / "momentum" / "momentum"

    # Resolve source-tree plugin.json
    project_dir = resolve_project_dir()
    source_plugin_path = project_dir / "skills" / "momentum" / ".claude-plugin" / "plugin.json"

    # --- Step 1: Resolve active cache version ---
    cache_version: str | None = None
    active_cache_dir: str | None = None
    cache_diagnostic: str | None = None

    if not cache_root.exists():
        # No cache installed — silent pass
        _result_plugin_cache("no-cache", None, None, None, None)
        return

    # Scan for version subdirectories
    version_dirs = [d for d in cache_root.iterdir() if d.is_dir()]
    if not version_dirs:
        # Cache root exists but is empty — silent pass
        _result_plugin_cache("no-cache", None, None, None, None)
        return

    # Sort descending by semver; pick highest
    try:
        version_dirs_sorted = sorted(version_dirs, key=lambda d: _parse_semver(d.name), reverse=True)
    except Exception:
        version_dirs_sorted = sorted(version_dirs, key=lambda d: d.name, reverse=True)

    active_dir = version_dirs_sorted[0]
    active_cache_dir = str(active_dir)
    cache_plugin_json = active_dir / ".claude-plugin" / "plugin.json"

    if not cache_plugin_json.exists():
        _result_plugin_cache(
            "indeterminate", None, None, active_cache_dir,
            f"cache plugin.json not found at {cache_plugin_json}"
        )
        return

    try:
        cache_data = json.loads(cache_plugin_json.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        _result_plugin_cache(
            "indeterminate", None, None, active_cache_dir,
            f"cache plugin.json parse error: {exc}"
        )
        return

    cache_version = cache_data.get("version")
    if not cache_version:
        _result_plugin_cache(
            "indeterminate", None, None, active_cache_dir,
            "cache plugin.json missing 'version' field"
        )
        return

    # --- Step 2: Resolve source-tree version ---
    if not source_plugin_path.exists():
        _result_plugin_cache("no-source", cache_version, None, active_cache_dir, None)
        return

    try:
        source_data = json.loads(source_plugin_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        _result_plugin_cache(
            "indeterminate", cache_version, None, active_cache_dir,
            f"source plugin.json parse error: {exc}"
        )
        return

    source_version = source_data.get("version")
    if not source_version:
        _result_plugin_cache(
            "indeterminate", cache_version, None, active_cache_dir,
            "source plugin.json missing 'version' field"
        )
        return

    # --- Step 3: Compare versions ---
    try:
        cache_tuple = _parse_semver(cache_version)
        source_tuple = _parse_semver(source_version)
        if cache_tuple == source_tuple:
            status = "match"
        elif cache_tuple < source_tuple:
            status = "skew-cache-behind"
        else:
            status = "skew-cache-ahead"
    except Exception as exc:
        _result_plugin_cache(
            "indeterminate", cache_version, source_version, active_cache_dir,
            f"version comparison error: {exc}"
        )
        return

    _result_plugin_cache(status, cache_version, source_version, active_cache_dir, None)


def _result_plugin_cache(
    status: str,
    cache_version: "str | None",
    source_version: "str | None",
    active_cache_dir: "str | None",
    diagnostic: "str | None",
) -> None:
    """Print the plugin-cache-check JSON result and exit 0."""
    output: dict = {
        "action": "session_plugin_cache_check",
        "success": True,
        "status": status,
        "cache_version": cache_version,
        "source_version": source_version,
        "active_cache_dir": active_cache_dir,
    }
    if diagnostic is not None:
        output["diagnostic"] = diagnostic
    print(json.dumps(output, indent=2))
    sys.exit(0)


# --- Feature Status Cache ---

def _compute_feature_status(project_dir: Path, claude_project_dir: Path) -> dict:
    """Compute feature status dict from cache and hash inputs.

    Returns a dict with a 'state' key — one of:
      - 'no-features': features.json absent
      - 'no-cache':    features.json present but cache missing/unparseable
      - 'fresh':       cache present and hash matches
      - 'stale':       cache present but hash mismatches
    """
    import hashlib

    features_path = project_dir / "_bmad-output" / "planning-artifacts" / "features.json"
    stories_path_val = project_dir / ".momentum" / "stories" / "index.json"
    cache_path = claude_project_dir / ".claude" / "momentum" / "feature-status.md"

    if not features_path.exists():
        return {"state": "no-features"}

    # Read raw content for hashing
    try:
        features_content = features_path.read_text(encoding="utf-8")
    except OSError:
        features_content = ""

    try:
        stories_content = stories_path_val.read_text(encoding="utf-8") if stories_path_val.exists() else ""
    except OSError:
        stories_content = ""

    computed_hash = hashlib.sha256(
        (features_content + ":" + stories_content).encode()
    ).hexdigest()

    # Parse frontmatter from cache file
    frontmatter = _read_frontmatter(cache_path)
    if frontmatter is None:
        return {"state": "no-cache"}

    cached_hash = frontmatter.get("input_hash", "")
    summary = frontmatter.get("summary", "")

    if cached_hash == computed_hash:
        return {"state": "fresh", "summary": summary}
    else:
        return {"state": "stale", "summary": summary}


def _read_frontmatter(path: Path) -> dict | None:
    """Read YAML-style frontmatter from a markdown file.

    Returns None if file is absent, not readable, or has no valid frontmatter block.
    Returns a dict of key: value pairs parsed from the --- block.
    """
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    # Find closing ---
    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return None

    frontmatter: dict = {}
    for line in lines[1:end_idx]:
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            # Strip surrounding quotes if present
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            frontmatter[key] = value

    return frontmatter


def cmd_feature_status_hash(args: argparse.Namespace) -> None:
    """Compute SHA-256 hash of features.json + stories/index.json."""
    import hashlib
    import os

    project_dir = resolve_project_dir()

    features_path = project_dir / "_bmad-output" / "planning-artifacts" / "features.json"
    stories_path_val = project_dir / ".momentum" / "stories" / "index.json"

    if not features_path.exists():
        result("feature_status_hash", success=True,
               hash_result={"hash": "", "features_present": False})
        return

    try:
        features_content = features_path.read_text(encoding="utf-8")
    except OSError:
        features_content = ""

    try:
        stories_content = stories_path_val.read_text(encoding="utf-8") if stories_path_val.exists() else ""
    except OSError:
        stories_content = ""

    combined = features_content + ":" + stories_content
    digest = hashlib.sha256(combined.encode()).hexdigest()

    result("feature_status_hash", success=True,
           hash_result={"hash": digest, "features_present": True})


# --- Feature Verify Command (DEC-040 D1) ---
#
# Sole write path for `status` and `last_verified` in .momentum/features.json.
# Failing-by-default: a feature only reaches `passing` through a recorded human
# `pass` verdict against a named build. No agent, skill, or workflow may write
# feature status by any other route (architecture.md Read/Write Authority).

_BUILD_SHA_RE = re.compile(r"^[0-9a-fA-F]+$")


def _parse_build_pair(build_value: str):
    """Parse a --build backendSha:clientSha value.

    Returns (backend_sha, client_sha, None) on success, or (None, None, message)
    when the value is not exactly two non-empty hex SHAs separated by one colon.
    """
    if build_value.count(":") != 1:
        return None, None, (
            f"Invalid --build value '{build_value}': expected exactly two commit SHAs "
            "separated by a single colon (backendSha:clientSha)"
        )
    backend_sha, client_sha = build_value.split(":", 1)
    if not backend_sha or not client_sha:
        return None, None, (
            f"Invalid --build value '{build_value}': both the backend and client SHA "
            "must be non-empty"
        )
    if not _BUILD_SHA_RE.match(backend_sha) or not _BUILD_SHA_RE.match(client_sha):
        return None, None, (
            f"Invalid --build value '{build_value}': SHAs must be hexadecimal commit SHAs"
        )
    return backend_sha, client_sha, None


def cmd_feature_verify(args: argparse.Namespace) -> None:
    """Record a human PASS/FAIL verdict against a feature's acceptance_condition.

    Sole writer of status/last_verified in .momentum/features.json (DEC-040 D1).
    Validates every input before touching the file; any rejection leaves the
    registry byte-identical.
    """
    project_dir = resolve_project_dir()
    path = features_path(project_dir)

    backend_sha, client_sha, build_error = _parse_build_pair(args.build)
    if build_error:
        error_result("feature_verify", build_error)

    evidence = args.evidence
    if not evidence.strip():
        error_result(
            "feature_verify",
            "Missing or empty --evidence: a verdict with no observation behind it "
            "is not recordable"
        )

    if not path.exists():
        error_result("feature_verify", f"Feature registry not found: {path}")

    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        error_result(
            "feature_verify",
            f"Feature registry at {path} is not valid JSON: {exc}"
        )

    if not isinstance(registry, dict):
        error_result(
            "feature_verify",
            f"Feature registry at {path} must be a JSON object keyed by feature slug"
        )

    slug = args.feature_slug
    if slug not in registry:
        error_result(
            "feature_verify",
            f"Unknown feature slug '{slug}': not present in {path}"
        )

    entry = registry[slug]
    if not isinstance(entry, dict):
        error_result(
            "feature_verify",
            f"Feature entry '{slug}' in {path} must be a JSON object"
        )

    verdict = args.verdict  # argparse choices restrict this to "pass" or "fail"
    status = "passing" if verdict == "pass" else "failing"

    entry["status"] = status
    entry["last_verified"] = {
        "date": date.today().isoformat(),
        "verdict": verdict,
        "backend_sha": backend_sha,
        "client_sha": client_sha,
        "evidence": evidence,
    }

    write_json(path, registry)

    result("feature_verify", success=True, slug=slug, status=status, path=str(path))


# --- Tasting Commands (DEC-040 D4) ---
#
# `tasting brief` and `tasting status` are read-only consumers of
# .momentum/features.json. Neither command opens the registry for writing,
# creates it, or repairs it under any code path — including when it is
# absent, empty, or unparseable. `momentum-tools feature verify` remains the
# sole writer (DEC-040 D1).

TASTING_WINDOW_MAX_DAYS = 14
TASTING_CLAIMS_CAP = 7
TASTING_PROBES_MAX = 3
TASTING_PROBES_MIN = 2
TASTING_QUIET_MAX_DAYS = 3
TASTING_INSISTENT_MAX_DAYS = 7


def tasting_dir(project_dir: Path) -> Path:
    return project_dir / ".momentum" / "tasting"


def _load_features_registry_safe(project_dir: Path) -> dict:
    """Read .momentum/features.json read-only, tolerating every failure mode.

    Absent, empty, unparseable, or non-object content all degrade to an empty
    registry rather than raising. Never writes, never repairs. Reuses
    `_read_json_object` for the exists/parse/shape checks it already covers,
    adding tolerance for the OSError/UnicodeDecodeError it doesn't.
    """
    try:
        return _read_json_object(features_path(project_dir)) or {}
    except (OSError, UnicodeDecodeError):
        return {}


def _parse_iso_date(value) -> "date | None":
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _tasting_claims(registry: dict) -> list[dict]:
    """Passing features with a usable acceptance_condition, newest-verified first.

    Degradation is per-entry: an entry with a missing/invalid date sorts as
    oldest (never crashes), and an entry missing acceptance_condition simply
    is not a quotable claim — it never blocks a sibling entry's claim.
    """
    claims = []
    for slug, entry in registry.items():
        if not isinstance(entry, dict):
            continue
        if entry.get("status") != "passing":
            continue
        cond = entry.get("acceptance_condition")
        if not isinstance(cond, str) or not cond.strip():
            continue
        last_verified = entry.get("last_verified")
        verified_date = None
        if isinstance(last_verified, dict):
            verified_date = _parse_iso_date(last_verified.get("date"))
        name = entry.get("name")
        claims.append({
            "slug": slug,
            "name": name.strip() if isinstance(name, str) and name.strip() else slug,
            "acceptance_condition": cond.strip(),
            "verified_date": verified_date,
        })
    claims.sort(key=lambda c: c["verified_date"] or date.min, reverse=True)
    return claims


def _tasting_window(registry: dict, today: date) -> dict:
    """Derive the walkthrough window from the newest last_verified.date.

    Clamps to the bounded 14-day default whenever no verdict exists at all,
    or the newest verdict predates that bound — never grows without limit.
    """
    newest = None
    for entry in registry.values():
        if not isinstance(entry, dict):
            continue
        last_verified = entry.get("last_verified")
        if not isinstance(last_verified, dict):
            continue
        candidate = _parse_iso_date(last_verified.get("date"))
        if candidate is not None and (newest is None or candidate > newest):
            newest = candidate

    if newest is None:
        return {
            "newest_verified_date": None,
            "days_since_newest": None,
            "window_days": TASTING_WINDOW_MAX_DAYS,
            "window_start": today - timedelta(days=TASTING_WINDOW_MAX_DAYS),
            "explanation": (
                "No recorded verdict exists yet, so this brief uses the bounded "
                f"14-day default window (the last {TASTING_WINDOW_MAX_DAYS} days)."
            ),
        }

    days_since = (today - newest).days
    if 0 <= days_since <= TASTING_WINDOW_MAX_DAYS:
        return {
            "newest_verified_date": newest.isoformat(),
            "days_since_newest": days_since,
            "window_days": max(days_since, 0),
            "window_start": newest,
            "explanation": (
                f"This brief covers the {days_since} day(s) since the last recorded "
                f"verdict on {newest.isoformat()}."
            ),
        }

    if days_since < 0:
        # A future-dated last_verified.date is an anomalous registry state (clock
        # skew, hand-edited fixture, corrupted write) — never treat it as the
        # reassuring "verified recently" case. Fall back to the bounded default
        # window and say plainly that the date is untrustworthy.
        explanation = (
            f"The most recently recorded verdict is dated {newest.isoformat()}, which is "
            "in the future relative to today — an anomalous registry state, not a recent "
            f"verification. This brief falls back to the bounded {TASTING_WINDOW_MAX_DAYS}-day "
            "default window rather than trusting that date."
        )
    else:
        explanation = (
            f"The last recorded verdict was on {newest.isoformat()}, {days_since} "
            "days ago — past the bounded 14-day default window, so this brief "
            f"uses the last {TASTING_WINDOW_MAX_DAYS} days instead."
        )
    return {
        "newest_verified_date": newest.isoformat(),
        "days_since_newest": days_since,
        "window_days": TASTING_WINDOW_MAX_DAYS,
        "window_start": today - timedelta(days=TASTING_WINDOW_MAX_DAYS),
        "explanation": explanation,
    }


def _tasting_tier(days_since) -> str:
    """Prominence tier per AC 9: quiet 1-3, insistent 4-7, leading 8+.

    No recorded verdict at all, or a future-dated (anomalous) verdict, is
    treated as the most urgent case (leading) — a session is always due in
    that state and never gets a reassuring quiet/insistent label.

    days_since == 0 (verified today) is not one of AC 9's three named tiers —
    `due` is already False for that state, so no nudge renders at all. It
    folds into the "quiet" branch below deliberately (the least-alarming
    label) rather than inventing a fourth tier value nothing downstream
    consumes.
    """
    if days_since is None or days_since < 0:
        return "leading"
    if days_since <= TASTING_QUIET_MAX_DAYS:
        return "quiet"
    if days_since <= TASTING_INSISTENT_MAX_DAYS:
        return "insistent"
    return "leading"


def _tasting_probes(claims: list[dict]) -> list[dict]:
    """2-3 probes, never more, never zero when at least one claim exists.

    Draws from the already-capped claims list (most recently verified first).
    A single available claim is probed twice, via distinct actions, rather
    than manufacturing a second feature that was never actually verified.
    """
    if not claims:
        return []
    actions = [
        "Open the running app and exercise this claim through its primary path.",
        "Open the running app and exercise this claim through a secondary or edge-case path.",
        "Open the running app and exercise this claim after a normal day of other usage.",
    ]
    if len(claims) == 1:
        chosen = [claims[0], claims[0]]
    else:
        chosen = claims[:TASTING_PROBES_MAX]
    probes = []
    for i, claim in enumerate(chosen):
        probes.append({
            "slug": claim["slug"],
            "claim": claim["acceptance_condition"],
            "action": actions[i % len(actions)],
        })
    return probes


TASTING_GIT_LOG_LIMIT = 50


def _tasting_merged_since(project_dir: Path, window_start: date) -> "dict | None":
    """Best-effort `git log --since` over the window. None means unavailable.

    Tolerates a missing git binary, a non-repository project directory
    (every fixture in the frozen contract is a bare temp dir with no git
    history at all), and any other subprocess failure — this signal is
    informational only and must never block the brief.

    Fetches one more commit than TASTING_GIT_LOG_LIMIT so a truncated result
    can be reported with open-ended phrasing ("50+ more") rather than a
    remainder count computed from a list that was itself already cut off.
    Returns {"commits": [...], "truncated": bool}.
    """
    try:
        proc = subprocess.run(
            [
                "git", "-C", str(project_dir), "log",
                "--since", window_start.isoformat(),
                "--oneline", "--no-decorate", "-n", str(TASTING_GIT_LOG_LIMIT + 1),
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    truncated = len(lines) > TASTING_GIT_LOG_LIMIT
    return {"commits": lines[:TASTING_GIT_LOG_LIMIT], "truncated": truncated}


def cmd_tasting_brief(args: argparse.Namespace) -> None:
    """Generate the expected-vs-reality tasting brief (DEC-040 D4).

    Read-only against .momentum/features.json on every code path, including
    absent, empty, and unparseable registries — those cases (AC6) always exit
    0. A failure to write the brief's own output file (a separate, unrelated
    failure mode — e.g. .momentum/tasting exists as a file) exits 1 with an
    error_result rather than degrading silently. Regenerates the same day's
    file in place on a same-day rerun.
    """
    project_dir = resolve_project_dir()
    registry = _load_features_registry_safe(project_dir)
    today = date.today()

    claims_all = _tasting_claims(registry)
    display_claims = claims_all[:TASTING_CLAIMS_CAP]
    collapsed_count = max(0, len(claims_all) - TASTING_CLAIMS_CAP)

    window = _tasting_window(registry, today)
    probes = _tasting_probes(display_claims)
    merged_result = _tasting_merged_since(project_dir, window["window_start"])
    merged = merged_result["commits"] if merged_result is not None else None
    merged_truncated = merged_result["truncated"] if merged_result is not None else False

    lines = [
        f"# Daily Tasting Brief — {today.isoformat()}",
        "",
        (
            "Purpose: a short walkthrough brief contrasting what the practice "
            "claims works today against what you actually see in the running "
            "app — no more than ten minutes, run before you trust any of it."
        ),
        "",
        "## What should work today",
    ]
    if not display_claims:
        lines.append(
            "There are no recorded claims to test — the feature registry has "
            "no passing entries yet."
        )
    else:
        for claim in display_claims:
            lines.append(
                f"- **{claim['name']}** (`{claim['slug']}`): "
                f"\"{claim['acceptance_condition']}\""
            )
        if collapsed_count:
            lines.append(
                f"- {collapsed_count} more passing feature(s) not shown above "
                "(see `.momentum/features.json`)."
            )

    lines += ["", "## What changed", window["explanation"]]
    if merged is None:
        lines.append(
            "No merge history is available for this window (no git repository "
            "detected)."
        )
    elif not merged:
        lines.append("Nothing merged in this window.")
    else:
        shown = merged[:TASTING_CLAIMS_CAP]
        lines.extend(f"- {commit}" for commit in shown)
        if merged_truncated:
            # The git log fetch itself hit its cap — the true total beyond what
            # was fetched is unknown, so the remainder is stated open-ended
            # rather than as an exact count computed from truncated data.
            lines.append(
                f"- {TASTING_GIT_LOG_LIMIT}+ more commit(s) not shown above "
                f"(log capped at {TASTING_GIT_LOG_LIMIT})."
            )
        elif len(merged) > TASTING_CLAIMS_CAP:
            lines.append(
                f"- {len(merged) - TASTING_CLAIMS_CAP} more commit(s) not shown above."
            )

    lines += ["", "## Probes to run"]
    if not probes:
        lines.append("No probes — there are no passing claims to test yet.")
    else:
        for i, probe in enumerate(probes, start=1):
            lines.append(
                f"{i}. Feature `{probe['slug']}` — claim: \"{probe['claim']}\". "
                f"Action: {probe['action']}"
            )

    lines += [
        "",
        "## Routing findings",
        (
            "Anything you observe while running these probes enters intake at "
            "**critical** priority with a mandatory feature link — carry the "
            "slug of the probe that surfaced it (DEC-040 D6)."
        ),
        "",
    ]

    out_dir = tasting_dir(project_dir)
    brief_path = out_dir / f"brief-{today.isoformat()}.md"
    content = "\n".join(lines)
    import os
    import tempfile
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(dir=out_dir, prefix=".brief-", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(content)
            os.replace(tmp_name, brief_path)
        except OSError:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
            raise
    except OSError as exc:
        # Not one of the registry-degradation paths AC6 governs — this is a
        # filesystem failure writing our own output (e.g. .momentum/tasting
        # exists as a file, not a directory). Fail loudly rather than silently
        # dropping the brief or crashing with an unguarded traceback.
        error_result(
            "tasting_brief",
            f"Could not write the tasting brief to {brief_path}: {exc}",
        )

    payload = {
        "path": str(brief_path),
        "date": today.isoformat(),
        "claims_shown": len(display_claims),
        "claims_collapsed": collapsed_count,
        "probes": len(probes),
        "window": {
            "days": window["window_days"],
            "newest_verified_date": window["newest_verified_date"],
            "explanation": window["explanation"],
        },
    }
    if getattr(args, "json", False):
        payload["brief"] = {
            "claims": [
                {
                    "slug": c["slug"],
                    "name": c["name"],
                    "acceptance_condition": c["acceptance_condition"],
                }
                for c in display_claims
            ],
            "probes": probes,
            "changed": merged if merged is not None else [],
            "changed_truncated": merged_truncated,
        }

    result("tasting_brief", success=True, **payload)


def cmd_tasting_status(args: argparse.Namespace) -> None:
    """Report tasting due-ness and prominence tier (DEC-040 D4/D5).

    Never fails, blocks, or errors under any input — including a missing
    registry, a malformed registry, or a repository with no git history.
    Escalation is re-surfacing at rising prominence, nothing else.
    """
    project_dir = resolve_project_dir()
    registry = _load_features_registry_safe(project_dir)
    today = date.today()

    window = _tasting_window(registry, today)
    days_since = window["days_since_newest"]
    # None (no verdict) and any negative days_since (future-dated, anomalous)
    # are always due, same as any positive count — only exactly 0 is not due.
    due = days_since != 0
    tier = _tasting_tier(days_since)

    result(
        "tasting_status",
        success=True,
        due=due,
        days_since=days_since,
        tier=tier,
        last_verified_date=window["newest_verified_date"],
    )


# --- Specialist Classify Command (retired — Decision 55 / DEC-023) ---
#
# This command formerly mapped touched paths to a pre-shipped dev specialist
# body (dev-skills / dev-build / dev-frontend) via a hard-coded pattern table.
# That table and the three specialist bodies it resolved to have been retired:
# `momentum-tools agent resolve` against `agents.json` is now the sole
# specialist spawn path (project-composed entries first, then defaults.dev).
# This command is kept as a no-op shim — it always resolves to the base `dev`
# body regardless of input — so existing callers do not break on invocation;
# new callers should use `agent resolve` directly.

def cmd_specialist_classify(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    agent_file = "skills/momentum/agents/dev.md"
    fallback = not (project_dir / agent_file).exists()
    result("specialist_classify", success=True,
           specialist="dev",
           agent_file=agent_file,
           matches={},
           fallback=fallback)


# --- Agent Commands ---

def cmd_agent_resolve(args: argparse.Namespace) -> None:
    """Resolve 1..N agents for a given set of file paths via the routing table.

    --touches: comma-separated file paths (pattern matching against project entries)
    --role:    role slug (bypass pattern matching, return defaults entry for this role)
    """
    from fnmatch import fnmatch

    project_dir = resolve_project_dir()
    agents_json_path = project_dir / "momentum" / "agents.json"

    # Load routing table (graceful fallback if missing)
    if agents_json_path.exists():
        try:
            agents_json = read_json(agents_json_path)
        except Exception:
            agents_json = {"defaults": {}, "project": []}
    else:
        agents_json = {"defaults": {}, "project": []}

    defaults: dict = agents_json.get("defaults", {})
    project_entries: list = agents_json.get("project", [])

    # --role mode: bypass pattern matching, return defaults entry for the named role
    if getattr(args, "role", None):
        role = args.role
        if role not in defaults:
            error_result("agent_resolve", f"Role '{role}' not found in defaults block", role=role)
        agent_path = defaults[role]
        resolved = project_dir / agent_path
        if not resolved.exists():
            error_result(
                "agent_resolve",
                f"Role '{role}' maps to a missing agent body: {agent_path} (resolved: {resolved})",
                role=role,
                agent_path=agent_path,
            )
        result("agent_resolve", success=True,
               results=[{
                   "slug": role,
                   "agent_path": agent_path,
                   "write_permissions": [],
                   "file_scope": [],
               }])
        return

    # --touches mode: pattern match against project entries, fall back to defaults
    touches_raw = getattr(args, "touches", None) or ""
    touches = [p.strip() for p in touches_raw.split(",") if p.strip()]

    def _assert_path_exists(slug: str, agent_path: str) -> None:
        """Fail loudly if an agent body path does not exist on disk."""
        resolved = project_dir / agent_path
        if not resolved.exists():
            error_result(
                "agent_resolve",
                f"Role '{slug}' maps to a missing agent body: {agent_path} (resolved: {resolved})",
                role=slug,
                agent_path=agent_path,
            )

    if not touches:
        # No file paths — return base dev default
        dev_path = defaults.get("dev", "skills/momentum/agents/dev.md")
        _assert_path_exists("dev", dev_path)
        result("agent_resolve", success=True,
               results=[{
                   "slug": "dev",
                   "agent_path": dev_path,
                   "write_permissions": [],
                   "file_scope": [],
               }])
        return

    # Group paths by matching project entry (first-match wins)
    claimed: dict[str, dict] = {}   # slug -> {entry, file_scope}
    unclaimed: list[str] = []

    for path in touches:
        matched = None
        for entry in project_entries:
            patterns = entry.get("patterns", [])
            if any(fnmatch(path, pat) for pat in patterns):
                matched = entry
                break
        if matched:
            slug = matched["slug"]
            if slug not in claimed:
                claimed[slug] = {"entry": matched, "file_scope": []}
            claimed[slug]["file_scope"].append(path)
        else:
            unclaimed.append(path)

    results = []

    # One result per matched project entry
    for slug, group in claimed.items():
        entry = group["entry"]
        agent_path = entry.get("agent", "")
        _assert_path_exists(slug, agent_path)
        results.append({
            "slug": slug,
            "agent_path": agent_path,
            "write_permissions": entry.get("write_permissions", []),
            "file_scope": group["file_scope"],
        })

    # Unclaimed paths fall back to defaults dev entry
    if unclaimed:
        dev_path = defaults.get("dev", "skills/momentum/agents/dev.md")
        _assert_path_exists("dev", dev_path)
        results.append({
            "slug": "dev",
            "agent_path": dev_path,
            "write_permissions": [],
            "file_scope": unclaimed,
        })

    # Empty touches that somehow got here — shouldn't happen, but guard
    if not results:
        dev_path = defaults.get("dev", "skills/momentum/agents/dev.md")
        _assert_path_exists("dev", dev_path)
        results.append({
            "slug": "dev",
            "agent_path": dev_path,
            "write_permissions": [],
            "file_scope": [],
        })

    result("agent_resolve", success=True, results=results)


# --- Quickfix Commands ---

def cmd_quickfix_register(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    slug = args.slug
    story = args.story

    if not story or not story.strip():
        error_result("quickfix_register", "Story key must not be empty", slug=slug)

    if "quickfixes" not in sprints:
        sprints["quickfixes"] = []

    # Auto-increment duplicate slugs
    existing_slugs = {qf["slug"] for qf in sprints["quickfixes"]}
    resolved_slug = slug
    if resolved_slug in existing_slugs:
        counter = 2
        while f"{slug}-{counter}" in existing_slugs:
            counter += 1
        resolved_slug = f"{slug}-{counter}"

    entry = {
        "slug": resolved_slug,
        "story": story,
        "started": date.today().isoformat(),
    }
    sprints["quickfixes"].append(entry)
    write_json(path, sprints)

    result("quickfix_register", success=True, **entry)


def cmd_quickfix_complete(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    slug = args.slug
    quickfixes = sprints.get("quickfixes", [])

    target = None
    for qf in quickfixes:
        if qf["slug"] == slug:
            target = qf
            break

    if target is None:
        error_result("quickfix_complete", f"Quickfix '{slug}' not found", slug=slug)

    target["completed"] = date.today().isoformat()
    write_json(path, sprints)

    result("quickfix_complete", success=True, slug=slug, completed=target["completed"])


# --- Story Commands ---

VALID_PRIORITIES = {"critical", "high", "medium", "low"}


def cmd_story_add(args: argparse.Namespace) -> None:
    """Add a new story entry to stories/index.json."""
    project_dir = resolve_project_dir()
    path = stories_path(project_dir)
    stories = read_json(path)

    slug = args.slug.strip()
    if not slug:
        error_result("story_add", "Slug must not be empty", slug=slug)

    if slug in stories:
        error_result("story_add", f"Story slug '{slug}' already exists in stories/index.json", slug=slug)

    priority = args.priority if args.priority else "low"
    if priority not in VALID_PRIORITIES:
        error_result("story_add", f"Invalid priority '{priority}'. Must be one of: {', '.join(sorted(VALID_PRIORITIES))}", slug=slug)

    VALID_STORY_TYPES = {"feature", "maintenance", "defect", "exploration", "practice"}
    story_type = (args.story_type or "feature").strip().lower()
    if story_type not in VALID_STORY_TYPES:
        error_result("story_add", f"Invalid story_type '{story_type}'. Must be one of: {', '.join(sorted(VALID_STORY_TYPES))}", slug=slug)

    raw_deps = (args.depends_on or "").strip()
    depends_on = [d.strip() for d in raw_deps.split(",") if d.strip()] if raw_deps else []

    # Invariant: story_file must mirror disk truth — true only when the backing
    # .momentum/stories/{slug}.md actually exists. Never hardcode True; a phantom
    # entry (story_file: true with no backing file) crashes downstream consumers
    # like sprint-planning that trust the flag.
    story_file_path = project_dir / ".momentum" / "stories" / f"{slug}.md"
    story_file_exists = story_file_path.is_file()

    entry = {
        "status": "backlog",
        "title": args.title.strip(),
        "epic_slug": args.epic.strip(),
        "story_file": story_file_exists,
        "depends_on": depends_on,
        "touches": [],
        "priority": priority,
        "story_type": story_type,
    }

    feature_slug = (args.feature_slug or "").strip()
    if feature_slug:
        entry["feature_slug"] = feature_slug

    stories[slug] = entry
    write_json(path, stories)

    result("story_add", success=True, slug=slug, **entry)


# --- Triage Commands ---

TRIAGE_STOPWORDS = {
    "the", "a", "an", "is", "in", "of", "to", "for", "and", "with", "by",
    "this", "that", "it", "as", "on", "at", "be", "are", "was", "were",
    "from", "or", "not", "but", "has", "have", "had", "its", "our", "we",
}

TRIAGE_TERMINAL_STATES = {"done", "dropped", "closed-incomplete"}


def _tokenize(text: str) -> list[str]:
    """Lowercase, split on whitespace/punctuation, remove stopwords."""
    import re
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return [t for t in tokens if t not in TRIAGE_STOPWORDS and len(t) > 1]


def _tf_vector(tokens: list[str]) -> dict[str, int]:
    """Return raw term-frequency Counter for a token list."""
    from collections import Counter
    return Counter(tokens)


def _compute_idf(documents: list[list[str]]) -> dict[str, float]:
    """Compute IDF weights from a corpus of token lists."""
    import math
    from collections import Counter
    N = len(documents)
    if N == 0:
        return {}
    df: Counter = Counter()
    for doc in documents:
        for term in set(doc):
            df[term] += 1
    return {term: math.log((N + 1) / (count + 1)) + 1.0 for term, count in df.items()}


def _tfidf_vector(tokens: list[str], idf: dict[str, float]) -> dict[str, float]:
    """Compute TF-IDF vector for tokens given a precomputed IDF table."""
    from collections import Counter
    tf = Counter(tokens)
    total = sum(tf.values()) or 1
    return {term: (count / total) * idf.get(term, 1.0) for term, count in tf.items()}


def _cosine_similarity(vec_a: dict[str, float], vec_b: dict[str, float]) -> float:
    """Cosine similarity between two sparse TF-IDF vectors."""
    import math
    shared = set(vec_a) & set(vec_b)
    if not shared:
        return 0.0
    dot = sum(vec_a[t] * vec_b[t] for t in shared)
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _jaccard_touches(touches_a: list[str], touches_b: list[str]) -> float:
    """Jaccard coefficient on tokenized touches path sets."""
    set_a = set(touches_a)
    set_b = set(touches_b)
    if not set_a and not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


def cmd_triage_prefilter(args: argparse.Namespace) -> None:
    """
    TF-IDF cosine + Jaccard touches prefilter for dedup gate.

    Reads incoming items as JSON array (--items-json) and the stories index
    (--stories-index). For each item, outputs top-K=10 candidate stories ranked
    by combined score. Also outputs NxN intra-batch similarity matrix.

    Output JSON:
    {
      "action": "triage_prefilter",
      "success": true,
      "shortlists": {
        "<item_id>": [
          {"slug": "...", "title": "...", "tfidf_score": 0.0, "jaccard_score": 0.0,
           "epic_boost": 0.0, "combined_score": 0.0},
          ...  (top K=10)
        ]
      },
      "similarity_matrix": [
        {"item_i": "<id>", "item_j": "<id>", "cosine_similarity": 0.0},
        ...
      ]
    }
    """
    # Parse incoming items
    try:
        _raw = json.loads(args.items_json)
        if not isinstance(_raw, list):
            error_result("triage_prefilter", "--items-json must be a JSON array")
        items: list = _raw
    except (json.JSONDecodeError, TypeError) as e:
        error_result("triage_prefilter", f"Invalid --items-json: {e}")

    # Load stories index
    index_path = Path(args.stories_index)
    if not index_path.exists():
        # No backlog — compute item-item cosines from items only; shortlists are empty
        def _item_text_early(item: dict) -> str:
            return (item.get("title", "") + " " + item.get("description", "")).strip()

        item_ids_early = [item.get("id", str(i)) for i, item in enumerate(items)]
        item_token_map_early: dict[str, list[str]] = {
            iid: _tokenize(_item_text_early(item))
            for iid, item in zip(item_ids_early, items)
        }
        idf_early = _compute_idf(list(item_token_map_early.values()))
        item_tfidf_early: dict[str, dict[str, float]] = {
            iid: _tfidf_vector(tokens, idf_early)
            for iid, tokens in item_token_map_early.items()
        }
        shortlists = {iid: [] for iid in item_ids_early}
        matrix: list[dict] = []
        for ii, id_i in enumerate(item_ids_early):
            for jj, id_j in enumerate(item_ids_early):
                sim = 1.0 if ii == jj else _cosine_similarity(
                    item_tfidf_early[id_i], item_tfidf_early[id_j]
                )
                matrix.append({"item_i": id_i, "item_j": id_j,
                                "cosine_similarity": round(sim, 4)})
        result("triage_prefilter", success=True, shortlists=shortlists,
               similarity_matrix=matrix, candidate_count=0, item_count=len(items))
        return

    try:
        stories_index = json.loads(index_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        error_result("triage_prefilter", f"Cannot read stories index: {e}")

    K = 10

    # Filter terminal-status stories
    candidate_stories = {
        slug: meta for slug, meta in stories_index.items()
        if meta.get("status", "backlog") not in TRIAGE_TERMINAL_STATES
    }

    # Build text corpus for IDF: combine item texts + candidate story texts
    def story_text(meta: dict) -> str:
        return (meta.get("title", "") + " " + meta.get("description", "")).strip()

    def item_text(item: dict) -> str:
        return (item.get("title", "") + " " + item.get("description", "")).strip()

    story_token_map: dict[str, list[str]] = {
        slug: _tokenize(story_text(meta)) for slug, meta in candidate_stories.items()
    }

    item_ids = [item.get("id", str(i)) for i, item in enumerate(items)]
    item_token_map: dict[str, list[str]] = {
        iid: _tokenize(item_text(item)) for iid, item in zip(item_ids, items)
    }
    item_meta_map: dict[str, dict] = {
        iid: item for iid, item in zip(item_ids, items)
    }

    # Build IDF from all documents (items + stories)
    all_docs = list(story_token_map.values()) + list(item_token_map.values())
    idf = _compute_idf(all_docs)

    # Compute TF-IDF vectors
    story_tfidf: dict[str, dict[str, float]] = {
        slug: _tfidf_vector(tokens, idf) for slug, tokens in story_token_map.items()
    }
    item_tfidf: dict[str, dict[str, float]] = {
        iid: _tfidf_vector(tokens, idf) for iid, tokens in item_token_map.items()
    }

    # Build shortlists: for each item, score all candidate stories
    shortlists: dict[str, list[dict]] = {}
    for iid, item in item_meta_map.items():
        item_vec = item_tfidf[iid]
        item_touches = item.get("touches", [])
        item_epic = item.get("epic_slug", "")
        item_feature = item.get("feature_slug", "")
        scores = []
        for slug, meta in candidate_stories.items():
            tfidf_score = _cosine_similarity(item_vec, story_tfidf[slug])
            jaccard_score = _jaccard_touches(item_touches, meta.get("touches", []))
            # Epic/feature boost: +0.1 if either epic_slug or feature_slug matches
            story_epic = meta.get("epic_slug", "")
            story_feature = meta.get("feature_slug", "")
            epic_match = (
                (item_epic and item_epic == story_epic) or
                (item_feature and item_feature == story_feature)
            )
            epic_boost = 0.1 if epic_match else 0.0
            combined = min(1.0, 0.6 * tfidf_score + 0.3 * jaccard_score + epic_boost)
            scores.append({
                "slug": slug,
                "title": meta.get("title", ""),
                "tfidf_score": round(tfidf_score, 4),
                "jaccard_score": round(jaccard_score, 4),
                "epic_boost": round(epic_boost, 4),
                "combined_score": round(combined, 4),
            })
        # Sort by combined_score descending, take top K
        scores.sort(key=lambda x: x["combined_score"], reverse=True)
        shortlists[iid] = scores[:K]

    # Build intra-batch similarity matrix (NxN TF-IDF cosine on item pairs)
    matrix: list[dict] = []
    for ii, id_i in enumerate(item_ids):
        for jj, id_j in enumerate(item_ids):
            if ii == jj:
                sim = 1.0
            else:
                sim = _cosine_similarity(item_tfidf[id_i], item_tfidf[id_j])
            matrix.append({
                "item_i": id_i,
                "item_j": id_j,
                "cosine_similarity": round(sim, 4),
            })

    result("triage_prefilter", success=True,
           shortlists=shortlists,
           similarity_matrix=matrix,
           candidate_count=len(candidate_stories),
           item_count=len(items))


# --- Practice Ledger Commands (DEC-033) ---

PRACTICE_LEDGER_EVENT_TYPES = frozenset({
    "created", "updated", "consumed", "rejected",
    "closed_stale", "reopened", "custom",
})
PRACTICE_LEDGER_TERMINAL_TYPES = frozenset({"consumed", "rejected", "closed_stale"})

# Default TTL (in days) after which a non-terminal practice-ledger entity is
# eligible for auto-close. The summary's near_auto_close band tracks this value.
PRACTICE_LEDGER_STALE_TTL_DAYS = 15


def practice_ledger_path(project_dir: Path) -> Path:
    return project_dir / ".momentum" / "practice-ledger.jsonl"


def _generate_event_id() -> str:
    """Generate a unique event_id using timestamp + UUID."""
    import uuid
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    return f"pl-{ts}-{uuid.uuid4().hex[:8]}"


def _parse_iso_ts(ts_str) -> "datetime | None":
    """Parse an ISO-8601 timestamp (tolerating a trailing 'Z').

    Returns the parsed datetime, or None if the input is not a parseable
    timestamp string.
    """
    try:
        return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def _append_ledger_event(ledger_path, *, entity_id, event_type, source, actor,
                         payload, custom_event_type=None) -> str:
    """Build a practice-ledger event, append it (append-only), return event_id."""
    event_id = _generate_event_id()
    event: dict = {
        "event_id": event_id,
        "entity_id": entity_id,
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "event_type": event_type,
        "source": source,
        "actor": actor,
        "payload": payload,
    }
    if custom_event_type:
        event["custom_event_type"] = custom_event_type

    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event, ensure_ascii=False)
    with open(ledger_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    return event_id


def cmd_practice_ledger_append(args: argparse.Namespace) -> None:
    """Append an event to practice-ledger.jsonl (true append-only, O_APPEND)."""
    project_dir = resolve_project_dir()
    ledger_path = practice_ledger_path(project_dir)

    event_type = args.event_type
    if event_type not in PRACTICE_LEDGER_EVENT_TYPES:
        error_result("practice_ledger_append",
                     f"Invalid event_type '{event_type}'. Must be one of: "
                     f"{', '.join(sorted(PRACTICE_LEDGER_EVENT_TYPES))}")
        return

    try:
        payload = json.loads(args.payload) if args.payload else {}
    except json.JSONDecodeError as e:
        error_result("practice_ledger_append", f"Invalid JSON for --payload: {e}")
        return

    custom_event_type = None
    if event_type == "custom":
        custom_event_type = getattr(args, "custom_event_type", None) or None

    event_id = _append_ledger_event(
        ledger_path,
        entity_id=args.entity_id,
        event_type=event_type,
        source=args.source,
        actor=args.actor,
        payload=payload,
        custom_event_type=custom_event_type,
    )

    result("practice_ledger_append", success=True, event_id=event_id,
           entity_id=args.entity_id, ledger_path=str(ledger_path))


def cmd_practice_ledger_consume(args: argparse.Namespace) -> None:
    """Append a consumed event referencing the original entity_id (append-only)."""
    project_dir = resolve_project_dir()
    ledger_path = practice_ledger_path(project_dir)

    entity_id = args.entity_id
    outcome_ref = getattr(args, "outcome_ref", None) or ""

    payload: dict = {}
    if outcome_ref:
        payload["outcome_ref"] = outcome_ref

    event_id = _append_ledger_event(
        ledger_path,
        entity_id=entity_id,
        event_type="consumed",
        source=getattr(args, "source", "momentum-tools-consume"),
        actor=getattr(args, "actor", "unknown"),
        payload=payload,
    )

    result("practice_ledger_consume", success=True, event_id=event_id,
           entity_id=entity_id, ledger_path=str(ledger_path))


def _load_ledger_events(project_dir: Path) -> tuple:
    """Load new-schema ledger events with a pure-Python fold; count archive entries.

    Implementation: glob the .momentum/practice-ledger*.jsonl files, parse each
    line as JSON one at a time, and fold by entity. No DuckDB is involved — this
    is plain stdlib (glob + json + a defaultdict fold downstream). The function
    name historically implied DuckDB; it does not.

    The five fixed reader subcommands (summary/open/history/since/by-source) are
    served entirely by this fold. An arbitrary-SQL-query interface (the actual
    value DuckDB would add) is intentionally DEFERRED to the follow-up story
    `practice-ledger-duckdb-sql-query-command`.

    Returns (new_events_list, archive_count).
    New-schema events have 'event_id' field. Lines missing it are archive entries.
    """
    import glob as _glob

    momentum_dir = project_dir / ".momentum"
    pattern = str(momentum_dir / "practice-ledger*.jsonl")
    files = sorted(_glob.glob(pattern))

    new_events: list = []
    archive_count = 0

    for fpath in files:
        is_archive = "pre-2026-05" in fpath
        try:
            with open(fpath, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        ev = json.loads(line)
                    except json.JSONDecodeError:
                        archive_count += 1
                        continue
                    # New-schema entries have event_id
                    if "event_id" in ev and not is_archive:
                        new_events.append(ev)
                    else:
                        archive_count += 1
        except OSError:
            pass

    return new_events, archive_count


def _event_order_key(ev: dict) -> tuple:
    """Deterministic ordering key for folding/history.

    ts is written at 1-second resolution, so same-second events for one entity
    tie on ts alone and the stable sort then falls back to file insertion order.
    event_id embeds a microsecond timestamp (pl-YYYYMMDDTHHMMSSffffff-<hex>), so
    appending it as a secondary key gives a stable monotonic tiebreak.
    """
    return (ev.get("ts", ""), ev.get("event_id", ""))


def _derive_current_state(events: list) -> dict:
    """Fold events by entity_id to derive current state (last event wins by ts)."""
    from collections import defaultdict
    by_entity: dict = defaultdict(list)
    for ev in events:
        entity_id = ev.get("entity_id")
        if entity_id is None:
            # New-schema lines without entity_id can't be folded; skip defensively
            # rather than crashing the JSON contract with a KeyError traceback.
            continue
        by_entity[entity_id].append(ev)
    current: dict = {}
    for entity_id, evlist in by_entity.items():
        sorted_evs = sorted(evlist, key=_event_order_key)
        last = sorted_evs[-1]
        current[entity_id] = {
            "entity_id": entity_id,
            "last_event_type": last.get("event_type"),
            "last_ts": last.get("ts"),
            "last_event_id": last.get("event_id"),
            "created_ts": sorted_evs[0].get("ts"),
            "event_count": len(sorted_evs),
        }
    return current


def cmd_practice_ledger_summary(args: argparse.Namespace) -> None:
    """summary — counts by event_type, source, age buckets, archive_entries."""
    from collections import defaultdict
    project_dir = resolve_project_dir()
    new_events, archive_count = _load_ledger_events(project_dir)

    by_event_type: dict = defaultdict(int)
    by_source: dict = defaultdict(int)

    now = datetime.now(timezone.utc)

    lt_7d = 0
    d7_30 = 0
    gt_30d = 0
    near_close = 0

    for ev in new_events:
        etype = ev.get("event_type", "unknown")
        src = ev.get("source", "unknown")
        by_event_type[etype] += 1
        by_source[src] += 1

        ev_dt = _parse_iso_ts(ev.get("ts", ""))
        if ev_dt is not None:
            age_days = (now - ev_dt).days
            if age_days < 7:
                lt_7d += 1
            elif age_days <= 30:
                d7_30 += 1
            else:
                gt_30d += 1
            if PRACTICE_LEDGER_STALE_TTL_DAYS - 3 <= age_days < PRACTICE_LEDGER_STALE_TTL_DAYS:
                near_close += 1

    output_fmt = getattr(args, "format", "json")
    summary_data = {
        "new_entries": len(new_events),
        "archive_entries": archive_count,
        "by_event_type": dict(by_event_type),
        "by_source": dict(by_source),
        "age_buckets": {
            "lt_7d": lt_7d,
            "d7_30": d7_30,
            "gt_30d": gt_30d,
            "near_auto_close": near_close,
        },
    }

    if output_fmt == "text":
        lines = [
            f"Practice Ledger Summary",
            f"  new entries:     {len(new_events)}",
            f"  archive entries: {archive_count}",
            f"  by event_type:   {dict(by_event_type)}",
            f"  by source:       {dict(by_source)}",
            f"  age <7d:         {lt_7d}",
            f"  age 7-30d:       {d7_30}",
            f"  age >30d:        {gt_30d}",
            f"  near_auto_close: {near_close}",
        ]
        print("\n".join(lines))
        return

    result("practice_ledger_summary", success=True, **summary_data)


def cmd_practice_ledger_open(args: argparse.Namespace) -> None:
    """open — entities whose last event is non-terminal."""
    project_dir = resolve_project_dir()
    new_events, _ = _load_ledger_events(project_dir)
    current = _derive_current_state(new_events)

    open_entities = [
        v for v in current.values()
        if v["last_event_type"] not in PRACTICE_LEDGER_TERMINAL_TYPES
    ]
    result("practice_ledger_open", success=True, entities=open_entities,
           count=len(open_entities))


def cmd_practice_ledger_history(args: argparse.Namespace) -> None:
    """history --entity <id> — all events for entity, sorted by ts ascending."""
    project_dir = resolve_project_dir()
    entity_id = args.entity
    new_events, _ = _load_ledger_events(project_dir)
    entity_events = [ev for ev in new_events if ev.get("entity_id") == entity_id]
    entity_events.sort(key=_event_order_key)
    result("practice_ledger_history", success=True, entity_id=entity_id,
           events=entity_events, count=len(entity_events))


def cmd_practice_ledger_since(args: argparse.Namespace) -> None:
    """since <iso-ts> — events strictly after the given timestamp."""
    project_dir = resolve_project_dir()
    since_ts = args.ts
    since_dt = _parse_iso_ts(since_ts)
    if since_dt is None:
        error_result("practice_ledger_since",
                     f"Invalid --ts '{since_ts}': must be an ISO-8601 timestamp "
                     f"(e.g. 2026-05-28T12:00:00Z)",
                     since=since_ts)
        return
    new_events, _ = _load_ledger_events(project_dir)
    filtered = []
    for ev in new_events:
        ev_dt = _parse_iso_ts(ev.get("ts", ""))
        if ev_dt is None:
            # Skip events whose ts can't be parsed rather than including/dropping
            # them via lexical comparison against a parsed bound.
            continue
        if ev_dt > since_dt:
            filtered.append(ev)
    result("practice_ledger_since", success=True, since=since_ts,
           events=filtered, count=len(filtered))


def cmd_practice_ledger_by_source(args: argparse.Namespace) -> None:
    """by-source <source> — events whose source matches exactly."""
    project_dir = resolve_project_dir()
    source = args.source
    new_events, _ = _load_ledger_events(project_dir)
    filtered = [ev for ev in new_events if ev.get("source") == source]
    result("practice_ledger_by_source", success=True, source=source,
           events=filtered, count=len(filtered))


def cmd_practice_ledger_close_stale(args: argparse.Namespace) -> None:
    """close-stale — append closed_stale events for non-terminal entities older than TTL."""
    project_dir = resolve_project_dir()
    age_days = int(getattr(args, "age_days", PRACTICE_LEDGER_STALE_TTL_DAYS))

    new_events, _ = _load_ledger_events(project_dir)
    current = _derive_current_state(new_events)

    now = datetime.now(timezone.utc)
    closed_count = 0
    closed_entity_ids = []

    for entity_id, state in current.items():
        if state["last_event_type"] in PRACTICE_LEDGER_TERMINAL_TYPES:
            continue
        created_dt = _parse_iso_ts(state.get("created_ts", ""))
        if created_dt is None:
            continue
        age = (now - created_dt).days
        if age > age_days:
            closed_entity_ids.append((entity_id, age))

    ledger_path = practice_ledger_path(project_dir)
    for entity_id, age in closed_entity_ids:
        _append_ledger_event(
            ledger_path,
            entity_id=entity_id,
            event_type="closed_stale",
            source="momentum-tools-close-stale",
            actor="automation",
            payload={"age_days_at_close": age},
        )
        closed_count += 1

    result("practice_ledger_close_stale", success=True,
           closed_count=closed_count,
           closed_entity_ids=[eid for eid, _ in closed_entity_ids],
           age_days=age_days)


# --- Version Command ---

def cmd_version_check(args: argparse.Namespace) -> None:
    import hashlib
    import os

    project_dir = resolve_project_dir()
    source_skill = project_dir / "skills" / "momentum" / "SKILL.md"
    installed_json = Path(os.environ.get("CLAUDE_PROJECT_DIR", project_dir)) / ".claude" / "momentum" / "installed.json"

    if not source_skill.exists():
        error_result("version_check", f"Source skill not found: {source_skill}")

    source_hash = hashlib.sha256(source_skill.read_bytes()).hexdigest()[:12]

    installed_hash = None
    if installed_json.exists():
        try:
            installed = json.loads(installed_json.read_text(encoding="utf-8"))
            installed_hash = installed.get("hash", None)
        except (json.JSONDecodeError, KeyError):
            installed_hash = None

    matches = source_hash == installed_hash
    result("version_check", success=True, source_hash=source_hash,
           installed_hash=installed_hash, up_to_date=matches)


# --- CLI Parser ---

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="momentum-tools",
        description="Deterministic CLI for Momentum sprint and story operations",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # sprint command group
    sprint = subparsers.add_parser("sprint", help="Sprint and story operations")
    sprint_sub = sprint.add_subparsers(dest="sprint_action", required=True)

    # sprint status-transition
    st = sprint_sub.add_parser("status-transition", help="Transition a story's status")
    st.add_argument("--story", required=True, help="Story slug")
    st.add_argument("--target", required=True, help="Target status")
    st.add_argument("--force", action="store_true", help="Bypass state machine validation")
    st.set_defaults(func=cmd_status_transition)

    # sprint activate
    sa = sprint_sub.add_parser("activate", help="Activate the planning sprint")
    sa.set_defaults(func=cmd_sprint_activate)

    # sprint complete
    sc = sprint_sub.add_parser(
        "complete",
        help="Close the active sprint — a gate, not an unconditional closer (DEC-040 D2/D3)"
    )
    sc.add_argument("--verdict", choices=["done", "failed"], default="done",
                    help="Terminal state to close with (default: done)")
    sc.add_argument("--reason", default=None,
                    help="Required non-empty reason when --verdict failed")
    sc.add_argument("--fix-confirmed", dest="fix_confirmed", action="append", default=[],
                    help="Repeatable: confirm one maintenance verified-fix entry by its text "
                         "or 1-based index (only used when no goal_conditions are declared)")
    sc.add_argument("--build", default=None,
                    help="backendSha:clientSha pair confirming the maintenance verified-fix build")
    sc.add_argument("--punt-decision", dest="punt_decision", default=None,
                    help="Decision document ref under _bmad-output/planning-artifacts/decisions/ "
                         "authorizing closure while goal-critical stories sit at "
                         "closed-incomplete/dropped")
    sc.set_defaults(func=cmd_sprint_complete)

    # sprint epic-membership
    em = sprint_sub.add_parser("epic-membership", help="Change a story's epic")
    em.add_argument("--story", required=True, help="Story slug")
    em.add_argument("--epic", required=True, help="Target epic slug")
    em.set_defaults(func=cmd_epic_membership)

    # sprint plan
    sp = sprint_sub.add_parser("plan", help="Add/remove stories from planning sprint")
    sp.add_argument("--operation", required=False, default=None, choices=["add", "remove"],
                    help="Add or remove (omit when only setting --goal/--goal-conditions/--slug)")
    sp.add_argument("--stories", required=False, default=None,
                    help="Comma-separated story slugs (required when --operation is given)")
    sp.add_argument("--wave", type=int, default=None, help="Wave number (for add)")
    sp.add_argument("--slug", default=None,
                    help="Set the planning sprint's slug (idempotent; the command fails if the sprint is locked)")
    sp.add_argument("--goal", default=None,
                    help="Set the planning sprint's goal text — a plain-language sprint purpose, or "
                         "a verified-fix list for a maintenance sprint (idempotent; fails if locked)")
    sp.add_argument("--goal-conditions", dest="goal_conditions", default=None,
                    help="Comma-separated feature slugs (from .momentum/features.json) whose "
                         "acceptance conditions this sprint intends to flip from failing to passing. "
                         "Empty string persists as [] (maintenance sprint). Idempotent; fails if locked.")
    sp.set_defaults(func=cmd_sprint_plan)

    # sprint ready
    sr = sprint_sub.add_parser("ready", help="Mark planning sprint as ready")
    sr.set_defaults(func=cmd_sprint_ready)

    # sprint retro-complete
    src = sprint_sub.add_parser("retro-complete", help="Mark retro done on most recent completed sprint")
    src.set_defaults(func=cmd_sprint_retro_complete)

    # sprint next-stories
    sns = sprint_sub.add_parser("next-stories", help="List unblocked stories in active sprint")
    sns.set_defaults(func=cmd_sprint_next_stories)

    # sprint migrate-priority
    smp = sprint_sub.add_parser("migrate-priority", help="Add priority=low to any story entry missing the field")
    smp.set_defaults(func=cmd_sprint_migrate_priority)

    # sprint set-priority
    ssp = sprint_sub.add_parser("set-priority", help="Set priority on a story")
    ssp.add_argument("--story", required=True, help="Story slug")
    ssp.add_argument("--priority", required=True, help="Priority level: critical, high, medium, low")
    ssp.set_defaults(func=cmd_sprint_set_priority)

    # sprint story-add
    sta = sprint_sub.add_parser("story-add", help="Add a new story entry to stories/index.json")
    sta.add_argument("--slug", required=True, help="Story slug (kebab-case, unique)")
    sta.add_argument("--title", required=True, help="Human-readable story title")
    sta.add_argument("--epic", required=True, help="Epic slug this story belongs to")
    sta.add_argument("--priority", default="low", help="Priority: critical, high, medium, low (default: low)")
    sta.add_argument("--feature-slug", default="", help="Feature slug this story belongs to (optional)")
    sta.add_argument("--story-type", default="feature", help="Story type: feature, maintenance, defect, exploration, practice (default: feature)")
    sta.add_argument("--depends-on", default="", help="Comma-separated list of story slugs this story depends on")
    sta.set_defaults(func=cmd_story_add)

    # sprint story-approve
    ssa = sprint_sub.add_parser("story-approve", help="Record per-story approval or rejection in planning.approvals")
    ssa.add_argument("--slug", required=True, help="Story slug to approve or reject")
    ssa.add_argument("--decision", required=True, choices=["approved", "rejected"],
                     help="Approval decision: approved or rejected")
    ssa.set_defaults(func=cmd_sprint_story_approve)

    # sprint story-set-contract
    ssc = sprint_sub.add_parser(
        "story-set-contract",
        help="Persist contract block + verification_method + can_merge_independently into planning.team.story_assignments[slug]"
    )
    ssc.add_argument("--slug", required=True, help="Story slug")
    ssc.add_argument("--verification-method", required=True,
                     choices=sorted(set(SURFACE_TO_VERIFICATION_METHOD.values())),
                     help="Closed-enum verification method token")
    ssc.add_argument("--contract-path", required=True,
                     help="Relative path to the contract file from project root")
    ssc.add_argument("--harness-profile", required=True,
                     help="Harness profile name (usually same as verification_method)")
    ssc.add_argument("--coverage-disposition", required=True,
                     choices=["dedicated-run", "covered-by-composition"],
                     help="Coverage disposition for this story")
    ssc.add_argument("--covered-by-scenario", default=None,
                     help="Integration scenario name from coverage-plan.md (null for dedicated-run)")
    ssc.add_argument("--frozen-sha256", required=True,
                     help="SHA-256 hex digest of the contract file at activation time")
    ssc.add_argument("--can-merge-independently", required=True,
                     help="true or false — whether this story can merge without waiting for dependencies")
    ssc.set_defaults(func=cmd_sprint_story_set_contract)

    # sprint compute-verification-method
    scvm = sprint_sub.add_parser(
        "compute-verification-method",
        help="Compute closed-enum verification_method for a story from its change_type"
    )
    scvm.add_argument("--story", required=True, help="Story slug")
    scvm.set_defaults(func=cmd_sprint_compute_verification_method)

    # sprint verify-approvals
    sva = sprint_sub.add_parser("verify-approvals", help="Verify all stories have current approved entries")
    sva.add_argument("--scope", required=True, choices=["planning", "active"],
                     help="Sprint scope to verify: planning or active")
    sva.set_defaults(func=cmd_sprint_verify_approvals)

    # sprint stories
    ss = sprint_sub.add_parser("stories", help="Query stories by priority")
    ss.add_argument("--priority", required=True,
                    help="Priority level (critical, high, medium, low) or 'all' for grouped output")
    ss.set_defaults(func=cmd_sprint_stories)

    # session command group
    session = subparsers.add_parser("session", help="Session management operations")
    session_sub = session.add_subparsers(dest="session_action", required=True)

    # session stats-update
    ssu = session_sub.add_parser("stats-update", help="Increment session stats in installed.json")
    ssu.set_defaults(func=cmd_session_stats_update)

    # session greeting-state
    sgs = session_sub.add_parser("greeting-state", help="Detect greeting state from sprint/story data")
    sgs.set_defaults(func=cmd_session_greeting_state)

    # session startup-preflight
    ssc = session_sub.add_parser("startup-preflight", help="Consolidated startup routing: versions, hash drift, journal, greeting state")
    ssc.set_defaults(func=cmd_session_startup_preflight)

    # session journal-status
    sjs = session_sub.add_parser("journal-status", help="Scan journal for open threads")
    sjs.set_defaults(func=cmd_session_journal_status)

    # session journal-hygiene
    sjh = session_sub.add_parser("journal-hygiene", help="Return structured hygiene data for all open threads")
    sjh.set_defaults(func=cmd_session_journal_hygiene)

    # session journal-append
    sja = session_sub.add_parser("journal-append", help="Atomic append to journal.jsonl and regenerate view")
    sja.add_argument("--entry", required=True, help="JSON string to append as a new journal line")
    sja.set_defaults(func=cmd_session_journal_append)

    # session plugin-cache-check
    spcc = session_sub.add_parser("plugin-cache-check", help="Compare active plugin cache version to source-tree version")
    spcc.set_defaults(func=cmd_session_plugin_cache_check)

    # specialist-classify command (retired no-op shim — always resolves to dev; use "agent resolve")
    sc_parser = subparsers.add_parser("specialist-classify", help="Retired no-op shim — always resolves to dev; use 'agent resolve'")
    sc_parser.add_argument("--touches", required=True, help="Comma-separated file paths (accepted but ignored)")
    sc_parser.set_defaults(func=cmd_specialist_classify)

    # agent command group
    agent = subparsers.add_parser("agent", help="Agent routing table operations")
    agent_sub = agent.add_subparsers(dest="agent_action", required=True)

    # agent resolve
    ar = agent_sub.add_parser("resolve", help="Resolve 1..N agents for given file paths via routing table")
    ar.add_argument("--touches", default=None, help="Comma-separated file paths to match against project entries")
    ar.add_argument("--role", default=None, help="Role slug — return defaults entry for this role (bypasses pattern matching)")
    ar.set_defaults(func=cmd_agent_resolve)

    # quickfix command group
    quickfix = subparsers.add_parser("quickfix", help="Quickfix tracking operations")
    quickfix_sub = quickfix.add_subparsers(dest="quickfix_action", required=True)

    # quickfix register
    qfr = quickfix_sub.add_parser("register", help="Register a new quickfix")
    qfr.add_argument("--slug", required=True, help="Quickfix slug")
    qfr.add_argument("--story", required=True, help="Story key")
    qfr.set_defaults(func=cmd_quickfix_register)

    # quickfix complete
    qfc = quickfix_sub.add_parser("complete", help="Complete a registered quickfix")
    qfc.add_argument("--slug", required=True, help="Quickfix slug")
    qfc.set_defaults(func=cmd_quickfix_complete)

    # practice-ledger command group (DEC-033)
    pl = subparsers.add_parser("practice-ledger",
                               help="Practice-ledger (practice-ledger.jsonl) operations — DEC-033")
    pl_sub = pl.add_subparsers(dest="pl_action", required=True)

    # practice-ledger append
    pla = pl_sub.add_parser("append", help="Append an event to practice-ledger.jsonl")
    pla.add_argument("--entity-id", required=True, help="Logical entity this event is about")
    pla.add_argument("--event-type", required=True,
                     choices=sorted(PRACTICE_LEDGER_EVENT_TYPES),
                     help="Event type (created|updated|consumed|rejected|closed_stale|reopened|custom)")
    pla.add_argument("--source", required=True, help="Originating skill/workflow")
    pla.add_argument("--actor", required=True, help="Human or agent identity")
    pla.add_argument("--payload", default="{}", help="JSON object payload (default: {})")
    pla.add_argument("--custom-event-type", default=None,
                     help="Custom event type name (required when event_type=custom)")
    pla.set_defaults(func=cmd_practice_ledger_append)

    # practice-ledger consume
    plc = pl_sub.add_parser("consume",
                             help="Append a consumed event for an entity (append-only)")
    plc.add_argument("--entity-id", required=True, help="Entity to mark consumed")
    plc.add_argument("--actor", required=True, help="Who is consuming")
    plc.add_argument("--source", default="momentum-tools-consume", help="Source skill")
    plc.add_argument("--outcome-ref", default=None, help="Reference to the outcome")
    plc.set_defaults(func=cmd_practice_ledger_consume)

    # practice-ledger summary
    pls = pl_sub.add_parser("summary", help="Counts by event_type, source, age, archive entries")
    pls.add_argument("--format", choices=["json", "text"], default="json",
                     help="Output format (default: json)")
    pls.set_defaults(func=cmd_practice_ledger_summary)

    # practice-ledger open
    plo = pl_sub.add_parser("open", help="Non-terminal entities (current state is open)")
    plo.set_defaults(func=cmd_practice_ledger_open)

    # practice-ledger history
    plh = pl_sub.add_parser("history", help="Full event chain for one entity")
    plh.add_argument("--entity", required=True, help="Entity ID to query history for")
    plh.set_defaults(func=cmd_practice_ledger_history)

    # practice-ledger since
    plsi = pl_sub.add_parser("since", help="Events strictly after the given ISO-8601 UTC timestamp")
    plsi.add_argument("ts", help="ISO-8601 UTC timestamp (e.g. 2026-01-01T00:00:00Z)")
    plsi.set_defaults(func=cmd_practice_ledger_since)

    # practice-ledger by-source
    plbs = pl_sub.add_parser("by-source", help="Events whose source matches exactly")
    plbs.add_argument("source", help="Source value to filter by")
    plbs.set_defaults(func=cmd_practice_ledger_by_source)

    # practice-ledger close-stale
    plcs = pl_sub.add_parser("close-stale",
                              help="Append closed_stale events for non-terminal entities older than TTL")
    plcs.add_argument("--age-days", type=int, default=PRACTICE_LEDGER_STALE_TTL_DAYS,
                      help=f"Age threshold in days (default: {PRACTICE_LEDGER_STALE_TTL_DAYS})")
    plcs.set_defaults(func=cmd_practice_ledger_close_stale)

    # triage command group
    triage = subparsers.add_parser("triage", help="Triage dedup prefilter operations")
    triage_sub = triage.add_subparsers(dest="triage_action", required=True)

    # triage prefilter
    tp = triage_sub.add_parser("prefilter", help="TF-IDF cosine + Jaccard prefilter for dedup gate")
    tp.add_argument("--items-json", required=True,
                    help="JSON array of incoming items: [{id, title, description, touches, epic_slug, feature_slug}, ...]")
    tp.add_argument("--stories-index", required=True,
                    help="Path to .momentum/stories/index.json")
    tp.set_defaults(func=cmd_triage_prefilter)

    # version command group
    version = subparsers.add_parser("version", help="Version management")
    version_sub = version.add_subparsers(dest="version_action", required=True)

    vc = version_sub.add_parser("check", help="Check version hash")
    vc.set_defaults(func=cmd_version_check)

    # feature command group (DEC-040 D1) — sole writer of feature status/last_verified
    feature = subparsers.add_parser("feature", help="Feature acceptance-registry operations (DEC-040 D1)")
    feature_sub = feature.add_subparsers(dest="feature_action", required=True)

    # feature verify
    fv = feature_sub.add_parser(
        "verify",
        help="Record a human PASS/FAIL verdict against a feature in .momentum/features.json"
    )
    fv.add_argument("feature_slug", metavar="feature-slug",
                    help="Feature slug to record a verdict against (must already exist in the registry)")
    fv.add_argument("--verdict", required=True, choices=["pass", "fail"],
                    help="Human verdict: pass or fail")
    fv.add_argument("--evidence", required=True,
                    help="What the human actually observed (non-empty, non-whitespace)")
    fv.add_argument("--build", required=True,
                    help="Paired build SHAs the verdict was observed against: backendSha:clientSha")
    fv.set_defaults(func=cmd_feature_verify)

    # feature-status-hash command (older, separate artifact — not part of the feature group)
    fsh = subparsers.add_parser("feature-status-hash",
                                help="Compute SHA-256 hash of features.json + stories/index.json")
    fsh.set_defaults(func=cmd_feature_status_hash)

    # tasting command group (DEC-040 D4) — read-only consumer of .momentum/features.json
    tasting = subparsers.add_parser("tasting", help="Daily tasting reminder + brief generator (DEC-040 D4)")
    tasting_sub = tasting.add_subparsers(dest="tasting_action", required=True)

    tb = tasting_sub.add_parser(
        "brief",
        help="Generate today's expected-vs-reality tasting brief at .momentum/tasting/brief-<date>.md"
    )
    tb.add_argument("--json", action="store_true",
                     help="Also print a machine-readable summary of the brief's content to stdout")
    tb.set_defaults(func=cmd_tasting_brief)

    ts = tasting_sub.add_parser(
        "status",
        help="Report whether a tasting session is due, days-since count, and prominence tier"
    )
    ts.add_argument("--json", action="store_true", help="Present for CLI-shape consistency; output is always JSON")
    ts.set_defaults(func=cmd_tasting_status)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
