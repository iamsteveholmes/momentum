#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""
momentum-tools — Deterministic CLI for Momentum sprint and story operations.

Sole writer of stories/index.json and sprints/index.json.
All operations are deterministic state machine validations + JSON mutations.

Usage:
    momentum-tools.py sprint status-transition --story SLUG --target STATUS [--force]
    momentum-tools.py sprint activate
    momentum-tools.py sprint complete
    momentum-tools.py sprint epic-membership --story SLUG --epic SLUG
    momentum-tools.py sprint plan --operation add|remove --stories SLUG[,SLUG,...] [--wave N]
    momentum-tools.py version check
"""

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

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
    return project_dir / "_bmad-output" / "implementation-artifacts" / "stories" / "index.json"


def sprints_path(project_dir: Path) -> Path:
    return project_dir / "_bmad-output" / "implementation-artifacts" / "sprints" / "index.json"


def read_json(path: Path) -> dict:
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def result(action: str, success: bool, **kwargs) -> None:
    """Print JSON result and exit."""
    output = {"action": action, "success": success, **kwargs}
    print(json.dumps(output, indent=2))
    sys.exit(0 if success else 1)


def error_result(action: str, message: str, **kwargs) -> None:
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
    write_json(path, stories)
    result("status_transition", success=True, story=slug, **{"from": current, "to": target})


def cmd_sprint_activate(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    if not sprints.get("planning"):
        error_result("sprint_activate", "No planning sprint exists to activate")
    if sprints.get("active"):
        error_result("sprint_activate", "An active sprint already exists. Complete it first.")

    planning = sprints["planning"]
    planning["locked"] = True
    planning["started"] = date.today().isoformat()
    sprints["active"] = planning
    sprints["planning"] = None
    write_json(path, sprints)

    slug = planning.get("slug", "unknown")
    result("sprint_activate", success=True, sprint=slug, started=planning["started"])


def cmd_sprint_complete(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    if not sprints.get("active"):
        error_result("sprint_complete", "No active sprint to complete")

    active = sprints["active"]
    active["completed"] = date.today().isoformat()
    if "completed" not in sprints:
        sprints["completed"] = []
    sprints["completed"].append(active)
    sprints["active"] = None
    write_json(path, sprints)

    slug = active.get("slug", "unknown")
    result("sprint_complete", success=True, sprint=slug, completed=active["completed"])


def cmd_epic_membership(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = stories_path(project_dir)
    stories = read_json(path)

    slug = args.story
    if slug not in stories:
        error_result("epic_membership", f"Story '{slug}' not found", story=slug)

    old_epic = stories[slug].get("epic_slug", "")
    stories[slug]["epic_slug"] = args.epic
    write_json(path, stories)
    result("epic_membership", success=True, story=slug, from_epic=old_epic, to_epic=args.epic)


def cmd_sprint_plan(args: argparse.Namespace) -> None:
    project_dir = resolve_project_dir()
    path = sprints_path(project_dir)
    sprints = read_json(path)

    # Create planning entry if it doesn't exist
    if not sprints.get("planning"):
        sprints["planning"] = {"locked": False, "stories": [], "waves": []}

    planning = sprints["planning"]
    if planning.get("locked"):
        error_result("sprint_plan", "Cannot modify a locked sprint")

    story_slugs = [s.strip() for s in args.stories.split(",")]

    if args.operation == "add":
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

    elif args.operation == "remove":
        planning["stories"] = [s for s in planning.get("stories", []) if s not in story_slugs]
        for wave in planning.get("waves", []):
            wave["stories"] = [s for s in wave.get("stories", []) if s not in story_slugs]
        # Remove empty waves
        planning["waves"] = [w for w in planning.get("waves", []) if w.get("stories")]

    write_json(path, sprints)
    result("sprint_plan", success=True, operation=args.operation, stories=story_slugs)


# --- Log Command ---

VALID_EVENT_TYPES = {"decision", "error", "retry", "assumption", "finding", "ambiguity"}


def cmd_log(args: argparse.Namespace) -> None:
    event = args.event
    if event not in VALID_EVENT_TYPES:
        error_result("log", f"Invalid event type: '{event}'. Must be one of: {', '.join(sorted(VALID_EVENT_TYPES))}")

    project_dir = resolve_project_dir()

    sprint_slug = args.sprint if args.sprint else "_unsorted"
    log_dir = project_dir / ".claude" / "momentum" / "sprint-logs" / sprint_slug
    log_dir.mkdir(parents=True, exist_ok=True)

    if args.story:
        filename = f"{args.agent}-{args.story}.jsonl"
    else:
        filename = f"{args.agent}.jsonl"

    log_file = log_dir / filename

    entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": args.agent,
        "story": args.story if args.story else None,
        "sprint": args.sprint if args.sprint else None,
        "event": event,
        "detail": args.detail,
    }

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    result("log", success=True, file=str(log_file), entry=entry)


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
    sc = sprint_sub.add_parser("complete", help="Complete the active sprint")
    sc.set_defaults(func=cmd_sprint_complete)

    # sprint epic-membership
    em = sprint_sub.add_parser("epic-membership", help="Change a story's epic")
    em.add_argument("--story", required=True, help="Story slug")
    em.add_argument("--epic", required=True, help="Target epic slug")
    em.set_defaults(func=cmd_epic_membership)

    # sprint plan
    sp = sprint_sub.add_parser("plan", help="Add/remove stories from planning sprint")
    sp.add_argument("--operation", required=True, choices=["add", "remove"], help="Add or remove")
    sp.add_argument("--stories", required=True, help="Comma-separated story slugs")
    sp.add_argument("--wave", type=int, default=None, help="Wave number (for add)")
    sp.set_defaults(func=cmd_sprint_plan)

    # log command group
    log = subparsers.add_parser("log", help="Append structured event to agent log")
    log.add_argument("--agent", required=True, help="Agent role (e.g. dev, pm, architect)")
    log.add_argument("--event", required=True, help="Event type: decision, error, retry, assumption, finding, ambiguity")
    log.add_argument("--detail", required=True, help="Human-readable detail text")
    log.add_argument("--story", default=None, help="Story slug (optional)")
    log.add_argument("--sprint", default=None, help="Sprint slug (optional, defaults to _unsorted)")
    log.set_defaults(func=cmd_log)

    # version command group
    version = subparsers.add_parser("version", help="Version management")
    version_sub = version.add_subparsers(dest="version_action", required=True)

    vc = version_sub.add_parser("check", help="Check version hash")
    vc.set_defaults(func=cmd_version_check)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
