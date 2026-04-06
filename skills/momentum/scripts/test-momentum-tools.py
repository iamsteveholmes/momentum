#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""
Tests for momentum-tools.py — state machine validation and sprint operations.

Run: python3 test-momentum-tools.py
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).parent / "momentum-tools.py"
PASS_COUNT = 0
FAIL_COUNT = 0


def setup_project(stories: dict | None = None, sprints: dict | None = None) -> Path:
    """Create a temp project directory with stories/index.json and sprints/index.json."""
    tmpdir = Path(tempfile.mkdtemp())
    stories_dir = tmpdir / "_bmad-output" / "implementation-artifacts" / "stories"
    sprints_dir = tmpdir / "_bmad-output" / "implementation-artifacts" / "sprints"
    stories_dir.mkdir(parents=True)
    sprints_dir.mkdir(parents=True)

    # Initialize git so project root resolution works
    subprocess.run(["git", "init", "--quiet", str(tmpdir)], check=True)

    if stories is None:
        stories = {
            "test-story": {
                "status": "backlog",
                "title": "Test Story",
                "epic_slug": "test-epic",
                "story_file": False,
                "depends_on": [],
                "touches": []
            },
            "done-story": {
                "status": "done",
                "title": "Done Story",
                "epic_slug": "test-epic",
                "story_file": False,
                "depends_on": [],
                "touches": []
            }
        }
    (stories_dir / "index.json").write_text(json.dumps(stories, indent=2) + "\n")

    if sprints is None:
        sprints = {"active": None, "planning": None, "completed": []}
    (sprints_dir / "index.json").write_text(json.dumps(sprints, indent=2) + "\n")

    return tmpdir


def run_tool(project_dir: Path, *args: str) -> tuple[int, dict]:
    """Run momentum-tools.py and return (exit_code, parsed_json_output)."""
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(project_dir)}
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, env=env
    )
    try:
        output = json.loads(proc.stdout)
    except json.JSONDecodeError:
        output = {"raw_stdout": proc.stdout, "raw_stderr": proc.stderr}
    return proc.returncode, output


def read_stories(project_dir: Path) -> dict:
    path = project_dir / "_bmad-output" / "implementation-artifacts" / "stories" / "index.json"
    return json.loads(path.read_text())


def read_sprints(project_dir: Path) -> dict:
    path = project_dir / "_bmad-output" / "implementation-artifacts" / "sprints" / "index.json"
    return json.loads(path.read_text())


def assert_eq(test_name: str, actual, expected):
    global PASS_COUNT, FAIL_COUNT
    if actual == expected:
        PASS_COUNT += 1
        print(f"  ✓ {test_name}")
    else:
        FAIL_COUNT += 1
        print(f"  ✗ {test_name}: expected {expected!r}, got {actual!r}")


# --- State Machine Tests ---

def test_valid_forward_transition():
    """Adjacent forward transitions should succeed."""
    print("\n[status-transition] Valid forward transitions")
    transitions = [
        ("backlog", "ready-for-dev"),
        ("ready-for-dev", "in-progress"),
        ("in-progress", "review"),
        ("review", "verify"),
        ("verify", "done"),
    ]
    for current, target in transitions:
        proj = setup_project({"s": {"status": current, "title": "S", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []}})
        code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", target)
        assert_eq(f"{current} -> {target}", code, 0)
        stories = read_stories(proj)
        assert_eq(f"  file updated to {target}", stories["s"]["status"], target)


def test_invalid_non_adjacent_forward():
    """Non-adjacent forward transitions should fail."""
    print("\n[status-transition] Invalid non-adjacent forward")
    proj = setup_project({"s": {"status": "backlog", "title": "S", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []}})
    code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", "done")
    assert_eq("backlog -> done rejected", code, 1)
    assert_eq("  file unchanged", read_stories(proj)["s"]["status"], "backlog")


def test_invalid_backward_transition():
    """Backward transitions should fail."""
    print("\n[status-transition] Invalid backward transition")
    proj = setup_project({"s": {"status": "review", "title": "S", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []}})
    code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", "in-progress")
    assert_eq("review -> in-progress rejected", code, 1)
    assert_eq("  file unchanged", read_stories(proj)["s"]["status"], "review")


def test_terminal_state_blocked():
    """Transitions from terminal states should fail."""
    print("\n[status-transition] Terminal state blocked")
    for state in ["done", "dropped", "closed-incomplete"]:
        proj = setup_project({"s": {"status": state, "title": "S", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []}})
        code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", "backlog")
        assert_eq(f"{state} -> backlog rejected", code, 1)


def test_force_override():
    """Force flag should bypass all validation."""
    print("\n[status-transition] Force override")
    proj = setup_project({"s": {"status": "done", "title": "S", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []}})
    code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", "in-progress", "--force")
    assert_eq("done -> in-progress with --force", code, 0)
    assert_eq("  file updated", read_stories(proj)["s"]["status"], "in-progress")


def test_dropped_from_any_non_terminal():
    """dropped is reachable from any non-terminal state."""
    print("\n[status-transition] Dropped from non-terminal")
    for state in ["backlog", "ready-for-dev", "in-progress", "review", "verify"]:
        proj = setup_project({"s": {"status": state, "title": "S", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []}})
        code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", "dropped")
        assert_eq(f"{state} -> dropped", code, 0)


def test_closed_incomplete_from_any_non_terminal():
    """closed-incomplete is reachable from any non-terminal state."""
    print("\n[status-transition] Closed-incomplete from non-terminal")
    for state in ["backlog", "ready-for-dev", "in-progress", "review", "verify"]:
        proj = setup_project({"s": {"status": state, "title": "S", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []}})
        code, out = run_tool(proj, "sprint", "status-transition", "--story", "s", "--target", "closed-incomplete")
        assert_eq(f"{state} -> closed-incomplete", code, 0)


def test_story_not_found():
    """Transitioning a non-existent story should fail."""
    print("\n[status-transition] Story not found")
    proj = setup_project({})
    code, out = run_tool(proj, "sprint", "status-transition", "--story", "ghost", "--target", "done")
    assert_eq("non-existent story rejected", code, 1)


def test_data_preservation():
    """Status transition should not alter other stories."""
    print("\n[status-transition] Data preservation")
    stories = {
        "a": {"status": "backlog", "title": "A", "epic_slug": "e1", "story_file": True, "depends_on": ["b"], "touches": ["file.md"]},
        "b": {"status": "in-progress", "title": "B", "epic_slug": "e2", "story_file": False, "depends_on": [], "touches": []},
    }
    proj = setup_project(stories)
    run_tool(proj, "sprint", "status-transition", "--story", "a", "--target", "ready-for-dev")
    result = read_stories(proj)
    assert_eq("story a updated", result["a"]["status"], "ready-for-dev")
    assert_eq("story a title preserved", result["a"]["title"], "A")
    assert_eq("story a depends_on preserved", result["a"]["depends_on"], ["b"])
    assert_eq("story a touches preserved", result["a"]["touches"], ["file.md"])
    assert_eq("story b unchanged", result["b"]["status"], "in-progress")
    assert_eq("story b title unchanged", result["b"]["title"], "B")


# --- Sprint Lifecycle Tests ---

def test_sprint_activate():
    """Activating a planning sprint."""
    print("\n[sprint activate] Basic activation")
    sprints = {
        "active": None,
        "planning": {"slug": "test-sprint", "name": "Test Sprint", "locked": False, "stories": ["s1"]},
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "activate")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("active sprint set", result["active"]["slug"], "test-sprint")
    assert_eq("locked", result["active"]["locked"], True)
    assert_eq("started date set", "started" in result["active"], True)
    assert_eq("planning cleared", result["planning"], None)


def test_sprint_activate_already_active():
    """Cannot activate when an active sprint exists."""
    print("\n[sprint activate] Already active")
    sprints = {
        "active": {"slug": "existing", "locked": True},
        "planning": {"slug": "new", "locked": False},
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "activate")
    assert_eq("rejected", code, 1)


def test_sprint_activate_no_planning():
    """Cannot activate when no planning sprint exists."""
    print("\n[sprint activate] No planning sprint")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "activate")
    assert_eq("rejected", code, 1)


def test_sprint_complete():
    """Completing an active sprint."""
    print("\n[sprint complete] Basic completion")
    sprints = {
        "active": {"slug": "test-sprint", "name": "Test Sprint", "locked": True, "started": "2026-04-01"},
        "planning": None,
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "complete")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("active cleared", result["active"], None)
    assert_eq("completed has 1 entry", len(result["completed"]), 1)
    assert_eq("completed sprint slug", result["completed"][0]["slug"], "test-sprint")
    assert_eq("completed date set", "completed" in result["completed"][0], True)


def test_sprint_complete_no_active():
    """Cannot complete when no active sprint."""
    print("\n[sprint complete] No active sprint")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "complete")
    assert_eq("rejected", code, 1)


# --- Epic Membership Tests ---

def test_epic_membership():
    """Change a story's epic."""
    print("\n[epic-membership] Basic change")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "epic-membership", "--story", "test-story", "--epic", "new-epic")
    assert_eq("exit code 0", code, 0)
    result = read_stories(proj)
    assert_eq("epic updated", result["test-story"]["epic_slug"], "new-epic")
    assert_eq("other story unchanged", result["done-story"]["epic_slug"], "test-epic")


def test_epic_membership_not_found():
    """Cannot change epic of non-existent story."""
    print("\n[epic-membership] Story not found")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "epic-membership", "--story", "ghost", "--epic", "e")
    assert_eq("rejected", code, 1)


# --- Sprint Plan Tests ---

def test_sprint_plan_add():
    """Add stories to planning sprint."""
    print("\n[sprint plan] Add stories")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "plan", "--operation", "add", "--stories", "s1,s2", "--wave", "1")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("planning created", result["planning"] is not None, True)
    assert_eq("stories added", set(result["planning"]["stories"]), {"s1", "s2"})
    assert_eq("wave 1 has stories", set(result["planning"]["waves"][0]["stories"]), {"s1", "s2"})


def test_sprint_plan_remove():
    """Remove stories from planning sprint."""
    print("\n[sprint plan] Remove stories")
    sprints = {
        "active": None,
        "planning": {"locked": False, "stories": ["s1", "s2", "s3"], "waves": [{"wave": 1, "stories": ["s1", "s2"]}, {"wave": 2, "stories": ["s3"]}]},
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "plan", "--operation", "remove", "--stories", "s1,s3")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("stories removed", result["planning"]["stories"], ["s2"])
    assert_eq("wave 1 updated", result["planning"]["waves"][0]["stories"], ["s2"])
    assert_eq("empty wave 2 removed", len(result["planning"]["waves"]), 1)


def test_sprint_plan_locked():
    """Cannot modify a locked sprint."""
    print("\n[sprint plan] Locked sprint")
    sprints = {"active": None, "planning": {"locked": True, "stories": []}, "completed": []}
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "plan", "--operation", "add", "--stories", "s1")
    assert_eq("rejected", code, 1)


def test_sprint_plan_no_duplicates():
    """Adding existing stories should not create duplicates."""
    print("\n[sprint plan] No duplicates")
    sprints = {"active": None, "planning": {"locked": False, "stories": ["s1"], "waves": []}, "completed": []}
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "plan", "--operation", "add", "--stories", "s1,s2")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("no duplicate s1", result["planning"]["stories"].count("s1"), 1)
    assert_eq("s2 added", "s2" in result["planning"]["stories"], True)


# --- Log Tests ---

def test_log_with_sprint_and_story():
    """Log with sprint+story creates correct directory and file."""
    print("\n[log] Sprint + story creates correct path")
    proj = setup_project()
    code, out = run_tool(proj, "log", "--agent", "dev", "--event", "decision",
                         "--detail", "chose approach A", "--sprint", "phase-3", "--story", "my-story")
    assert_eq("exit code 0", code, 0)
    log_file = proj / ".claude" / "momentum" / "sprint-logs" / "phase-3" / "dev-my-story.jsonl"
    assert_eq("log file created", log_file.exists(), True)


def test_log_without_story():
    """Log without story creates agent-only filename."""
    print("\n[log] Without story uses agent-only filename")
    proj = setup_project()
    code, out = run_tool(proj, "log", "--agent", "impetus", "--event", "finding",
                         "--detail", "all stories complete", "--sprint", "phase-3")
    assert_eq("exit code 0", code, 0)
    log_file = proj / ".claude" / "momentum" / "sprint-logs" / "phase-3" / "impetus.jsonl"
    assert_eq("agent-only file created", log_file.exists(), True)
    story_file = proj / ".claude" / "momentum" / "sprint-logs" / "phase-3" / "impetus-None.jsonl"
    assert_eq("no None in filename", story_file.exists(), False)


def test_log_without_sprint():
    """Log without sprint falls back to _unsorted."""
    print("\n[log] Without sprint falls back to _unsorted")
    proj = setup_project()
    code, out = run_tool(proj, "log", "--agent", "dev", "--event", "assumption",
                         "--detail", "assuming default config")
    assert_eq("exit code 0", code, 0)
    log_file = proj / ".claude" / "momentum" / "sprint-logs" / "_unsorted" / "dev.jsonl"
    assert_eq("_unsorted file created", log_file.exists(), True)


def test_log_entry_valid_jsonl():
    """Log entry is valid JSONL with correct fields."""
    print("\n[log] Entry is valid JSONL with correct fields")
    proj = setup_project()
    run_tool(proj, "log", "--agent", "architect", "--event", "decision",
             "--detail", "chose microservices", "--sprint", "s1", "--story", "arch-design")
    log_file = proj / ".claude" / "momentum" / "sprint-logs" / "s1" / "architect-arch-design.jsonl"
    line = log_file.read_text().strip()
    entry = json.loads(line)
    assert_eq("has timestamp", "timestamp" in entry, True)
    assert_eq("agent correct", entry["agent"], "architect")
    assert_eq("story correct", entry["story"], "arch-design")
    assert_eq("sprint correct", entry["sprint"], "s1")
    assert_eq("event correct", entry["event"], "decision")
    assert_eq("detail correct", entry["detail"], "chose microservices")


def test_log_multiple_appends():
    """Multiple appends accumulate in the same file."""
    print("\n[log] Multiple appends accumulate")
    proj = setup_project()
    for i in range(3):
        run_tool(proj, "log", "--agent", "dev", "--event", "finding",
                 "--detail", f"finding {i}", "--sprint", "s1", "--story", "acc")
    log_file = proj / ".claude" / "momentum" / "sprint-logs" / "s1" / "dev-acc.jsonl"
    lines = [l for l in log_file.read_text().strip().split("\n") if l]
    assert_eq("3 lines accumulated", len(lines), 3)
    for i, line in enumerate(lines):
        entry = json.loads(line)
        assert_eq(f"  line {i} detail", entry["detail"], f"finding {i}")


def test_log_invalid_event_type():
    """Invalid event type rejected with exit 1."""
    print("\n[log] Invalid event type rejected")
    proj = setup_project()
    code, out = run_tool(proj, "log", "--agent", "dev", "--event", "bogus",
                         "--detail", "should fail")
    assert_eq("exit code 1", code, 1)
    assert_eq("reports failure", out.get("success"), False)


def test_log_missing_required_args():
    """Missing --agent, --event, --detail rejected."""
    print("\n[log] Missing required args rejected")
    proj = setup_project()
    # missing --detail
    code1, _ = run_tool(proj, "log", "--agent", "dev", "--event", "decision")
    assert_eq("missing --detail rejected", code1, 2)
    # missing --event
    code2, _ = run_tool(proj, "log", "--agent", "dev", "--detail", "something")
    assert_eq("missing --event rejected", code2, 2)
    # missing --agent
    code3, _ = run_tool(proj, "log", "--event", "decision", "--detail", "something")
    assert_eq("missing --agent rejected", code3, 2)


def test_log_all_event_types():
    """All 6 valid event types accepted."""
    print("\n[log] All 6 event types accepted")
    proj = setup_project()
    for event_type in ["decision", "error", "retry", "assumption", "finding", "ambiguity"]:
        code, out = run_tool(proj, "log", "--agent", "dev", "--event", event_type,
                             "--detail", f"test {event_type}", "--sprint", "s1")
        assert_eq(f"{event_type} accepted", code, 0)


def test_log_special_characters():
    """Special characters in detail preserved."""
    print("\n[log] Special characters in detail preserved")
    proj = setup_project()
    special_detail = 'quotes "here" and {braces} and <angles> & ampersand'
    code, out = run_tool(proj, "log", "--agent", "dev", "--event", "finding",
                         "--detail", special_detail, "--sprint", "s1")
    assert_eq("exit code 0", code, 0)
    log_file = proj / ".claude" / "momentum" / "sprint-logs" / "s1" / "dev.jsonl"
    entry = json.loads(log_file.read_text().strip())
    assert_eq("special chars preserved", entry["detail"], special_detail)


# --- Helpers for new tests ---

def setup_installed_json(project_dir: Path, data: dict) -> Path:
    """Create .claude/momentum/installed.json in the project dir."""
    installed_dir = project_dir / ".claude" / "momentum"
    installed_dir.mkdir(parents=True, exist_ok=True)
    installed_path = installed_dir / "installed.json"
    installed_path.write_text(json.dumps(data, indent=2) + "\n")
    return installed_path


def read_installed_json(project_dir: Path) -> dict:
    path = project_dir / ".claude" / "momentum" / "installed.json"
    return json.loads(path.read_text())


def setup_versions_json(project_dir: Path, data: dict) -> Path:
    """Create skills/momentum/references/momentum-versions.json."""
    ref_dir = project_dir / "skills" / "momentum" / "references"
    ref_dir.mkdir(parents=True, exist_ok=True)
    versions_path = ref_dir / "momentum-versions.json"
    versions_path.write_text(json.dumps(data, indent=2) + "\n")
    return versions_path


def setup_global_installed(data: dict) -> Path:
    """Create ~/.claude/momentum/global-installed.json (returns path for cleanup)."""
    global_dir = Path.home() / ".claude" / "momentum"
    global_dir.mkdir(parents=True, exist_ok=True)
    global_path = global_dir / "global-installed.json"
    global_path.write_text(json.dumps(data, indent=2) + "\n")
    return global_path


# --- Sprint Status Field Tests ---

def test_sprint_plan_sets_status_planning():
    """sprint plan creates planning entry with status='planning'."""
    print("\n[sprint plan] Sets status planning")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "plan", "--operation", "add", "--stories", "s1")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("status is planning", result["planning"]["status"], "planning")


def test_sprint_activate_sets_status_active():
    """sprint activate sets active.status='active'."""
    print("\n[sprint activate] Sets status active")
    sprints = {
        "active": None,
        "planning": {"slug": "test-sprint", "locked": False, "stories": ["s1"]},
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "activate")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("status is active", result["active"]["status"], "active")


def test_sprint_complete_sets_status_done():
    """sprint complete sets active.status='done' and retro_run_at=None."""
    print("\n[sprint complete] Sets status done and retro_run_at null")
    sprints = {
        "active": {"slug": "test-sprint", "locked": True, "started": "2026-04-01"},
        "planning": None,
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "complete")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("status is done", result["completed"][0]["status"], "done")
    assert_eq("retro_run_at is null", result["completed"][0]["retro_run_at"], None)


# --- Sprint Ready Tests ---

def test_sprint_ready_sets_status_ready():
    """sprint ready sets planning.status='ready'."""
    print("\n[sprint ready] Sets status ready")
    sprints = {
        "active": None,
        "planning": {"slug": "test-sprint", "locked": False, "status": "planning", "stories": ["s1"]},
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "ready")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("status is ready", result["planning"]["status"], "ready")


def test_sprint_ready_no_planning():
    """sprint ready fails when no planning sprint exists."""
    print("\n[sprint ready] No planning sprint")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "ready")
    assert_eq("rejected", code, 1)


# --- Sprint Retro-Complete Tests ---

def test_sprint_retro_complete_basic():
    """sprint retro-complete sets retro_run_at on most recent eligible entry."""
    print("\n[sprint retro-complete] Basic retro completion")
    sprints = {
        "active": None,
        "planning": None,
        "completed": [
            {"slug": "sprint-1", "completed": "2026-03-15", "status": "done", "retro_run_at": "2026-03-16"},
            {"slug": "sprint-2", "completed": "2026-04-01", "status": "done", "retro_run_at": None}
        ]
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "retro-complete")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("sprint-2 retro set", result["completed"][1]["retro_run_at"] is not None, True)
    assert_eq("sprint-1 unchanged", result["completed"][0]["retro_run_at"], "2026-03-16")


def test_sprint_retro_complete_auto_activates():
    """Auto-activates planning sprint when status is 'ready'."""
    print("\n[sprint retro-complete] Auto-activates ready planning sprint")
    sprints = {
        "active": None,
        "planning": {"slug": "next-sprint", "locked": False, "status": "ready", "stories": ["s1"]},
        "completed": [
            {"slug": "sprint-1", "completed": "2026-04-01", "status": "done", "retro_run_at": None}
        ]
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "retro-complete")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("auto_activated", out.get("auto_activated"), True)
    assert_eq("active sprint set", result["active"]["slug"], "next-sprint")
    assert_eq("active status", result["active"]["status"], "active")
    assert_eq("active locked", result["active"]["locked"], True)
    assert_eq("planning cleared", result["planning"], None)


def test_sprint_retro_complete_no_auto_activate_when_planning():
    """Does NOT activate planned sprint when status is 'planning'."""
    print("\n[sprint retro-complete] No auto-activate when status is planning")
    sprints = {
        "active": None,
        "planning": {"slug": "next-sprint", "locked": False, "status": "planning", "stories": ["s1"]},
        "completed": [
            {"slug": "sprint-1", "completed": "2026-04-01", "status": "done", "retro_run_at": None}
        ]
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "retro-complete")
    assert_eq("exit code 0", code, 0)
    result = read_sprints(proj)
    assert_eq("not auto_activated", out.get("auto_activated"), False)
    assert_eq("planning still exists", result["planning"]["slug"], "next-sprint")
    assert_eq("planning still planning", result["planning"]["status"], "planning")
    assert_eq("active still null", result["active"], None)


def test_sprint_retro_complete_no_completed_sprints():
    """Fails when no completed sprint has retro_run_at unset."""
    print("\n[sprint retro-complete] No eligible completed sprints")
    sprints = {
        "active": None,
        "planning": None,
        "completed": [
            {"slug": "sprint-1", "completed": "2026-03-15", "status": "done", "retro_run_at": "2026-03-16"}
        ]
    }
    proj = setup_project(sprints=sprints)
    code, out = run_tool(proj, "sprint", "retro-complete")
    assert_eq("rejected", code, 1)


# --- Sprint Next-Stories Tests ---

def test_next_stories_all_unblocked():
    """Returns all stories as ready when no dependencies."""
    print("\n[sprint next-stories] All unblocked")
    stories = {
        "s1": {"status": "backlog", "title": "S1", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
        "s2": {"status": "ready-for-dev", "title": "S2", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
    }
    sprints = {
        "active": {"slug": "test-sprint", "locked": True, "status": "active", "stories": ["s1", "s2"]},
        "planning": None,
        "completed": []
    }
    proj = setup_project(stories=stories, sprints=sprints)
    code, out = run_tool(proj, "sprint", "next-stories")
    assert_eq("exit code 0", code, 0)
    assert_eq("ready has 2", len(out.get("ready", [])), 2)
    assert_eq("blocked empty", len(out.get("blocked", [])), 0)
    assert_eq("done empty", len(out.get("done", [])), 0)


def test_next_stories_some_blocked():
    """Returns correct ready/blocked split based on depends_on."""
    print("\n[sprint next-stories] Some blocked")
    stories = {
        "s1": {"status": "backlog", "title": "S1", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
        "s2": {"status": "backlog", "title": "S2", "epic_slug": "e", "story_file": False, "depends_on": ["s1"], "touches": []},
        "s3": {"status": "backlog", "title": "S3", "epic_slug": "e", "story_file": False, "depends_on": ["s2"], "touches": []},
    }
    sprints = {
        "active": {"slug": "test-sprint", "locked": True, "status": "active", "stories": ["s1", "s2", "s3"]},
        "planning": None,
        "completed": []
    }
    proj = setup_project(stories=stories, sprints=sprints)
    code, out = run_tool(proj, "sprint", "next-stories")
    assert_eq("exit code 0", code, 0)
    assert_eq("s1 is ready", "s1" in out.get("ready", []), True)
    blocked_slugs = [b["slug"] for b in out.get("blocked", [])]
    assert_eq("s2 is blocked", "s2" in blocked_slugs, True)
    assert_eq("s3 is blocked", "s3" in blocked_slugs, True)
    # Check waiting_on for s2
    s2_blocked = [b for b in out["blocked"] if b["slug"] == "s2"][0]
    assert_eq("s2 waiting on s1", s2_blocked["waiting_on"], ["s1"])


def test_next_stories_done_excluded():
    """Done stories not in ready or blocked lists."""
    print("\n[sprint next-stories] Done excluded")
    stories = {
        "s1": {"status": "done", "title": "S1", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
        "s2": {"status": "backlog", "title": "S2", "epic_slug": "e", "story_file": False, "depends_on": ["s1"], "touches": []},
    }
    sprints = {
        "active": {"slug": "test-sprint", "locked": True, "status": "active", "stories": ["s1", "s2"]},
        "planning": None,
        "completed": []
    }
    proj = setup_project(stories=stories, sprints=sprints)
    code, out = run_tool(proj, "sprint", "next-stories")
    assert_eq("exit code 0", code, 0)
    assert_eq("s1 in done", "s1" in out.get("done", []), True)
    assert_eq("s2 is ready (dep done)", "s2" in out.get("ready", []), True)
    assert_eq("blocked empty", len(out.get("blocked", [])), 0)


def test_next_stories_no_active_sprint():
    """Fails when no active sprint exists."""
    print("\n[sprint next-stories] No active sprint")
    proj = setup_project()
    code, out = run_tool(proj, "sprint", "next-stories")
    assert_eq("rejected", code, 1)


# --- Session Stats-Update Tests ---

def test_session_stats_update_creates():
    """session stats-update creates session_stats when absent."""
    print("\n[session stats-update] Creates session_stats")
    proj = setup_project()
    setup_installed_json(proj, {"version": "1.0.0", "hash": "abc123"})
    code, out = run_tool(proj, "session", "stats-update")
    assert_eq("exit code 0", code, 0)
    data = read_installed_json(proj)
    assert_eq("session_stats created", "session_stats" in data, True)
    assert_eq("completions is 1", data["session_stats"]["momentum_completions"], 1)
    assert_eq("last_invocation set", data["session_stats"]["last_invocation"] is not None, True)


def test_session_stats_update_increments():
    """session stats-update increments momentum_completions."""
    print("\n[session stats-update] Increments completions")
    proj = setup_project()
    setup_installed_json(proj, {
        "version": "1.0.0",
        "session_stats": {"momentum_completions": 5, "last_invocation": "2026-04-01"}
    })
    code, out = run_tool(proj, "session", "stats-update")
    assert_eq("exit code 0", code, 0)
    data = read_installed_json(proj)
    assert_eq("completions incremented", data["session_stats"]["momentum_completions"], 6)


def test_session_stats_update_preserves_data():
    """session stats-update does not alter components or other fields."""
    print("\n[session stats-update] Preserves other data")
    proj = setup_project()
    original = {
        "version": "1.0.0",
        "hash": "abc123",
        "components": {"rules": {"version": "1.0.0"}},
        "session_stats": {"momentum_completions": 2, "last_invocation": "2026-04-01"}
    }
    setup_installed_json(proj, original)
    code, out = run_tool(proj, "session", "stats-update")
    assert_eq("exit code 0", code, 0)
    data = read_installed_json(proj)
    assert_eq("version preserved", data["version"], "1.0.0")
    assert_eq("hash preserved", data["hash"], "abc123")
    assert_eq("components preserved", data["components"], {"rules": {"version": "1.0.0"}})
    assert_eq("completions incremented", data["session_stats"]["momentum_completions"], 3)


# --- Session Greeting-State Tests ---

def test_greeting_state_first_session():
    """Returns 'first-session-ever' when no sprints and completions == 0."""
    print("\n[session greeting-state] First session ever")
    proj = setup_project()
    # No installed.json — completions defaults to 0
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "first-session-ever")
    assert_eq("active_sprint null", out.get("active_sprint"), None)
    assert_eq("completions 0", out.get("momentum_completions"), 0)


def test_greeting_state_active_in_progress():
    """Returns 'active-in-progress' with stories moving."""
    print("\n[session greeting-state] Active in progress")
    stories = {
        "s1": {"status": "in-progress", "title": "S1", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
        "s2": {"status": "backlog", "title": "S2", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
    }
    sprints = {
        "active": {"slug": "test-sprint", "status": "active", "locked": True, "stories": ["s1", "s2"]},
        "planning": None,
        "completed": []
    }
    proj = setup_project(stories=stories, sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 1, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "active-in-progress")
    assert_eq("active_sprint", out.get("active_sprint"), "test-sprint")


def test_greeting_state_active_not_started():
    """Returns 'active-not-started' when all stories ready-for-dev."""
    print("\n[session greeting-state] Active not started")
    stories = {
        "s1": {"status": "ready-for-dev", "title": "S1", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
        "s2": {"status": "backlog", "title": "S2", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
    }
    sprints = {
        "active": {"slug": "test-sprint", "status": "active", "locked": True, "stories": ["s1", "s2"]},
        "planning": None,
        "completed": []
    }
    proj = setup_project(stories=stories, sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 1, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "active-not-started")


def test_greeting_state_active_blocked():
    """Returns 'active-blocked' when story has unmet depends_on."""
    print("\n[session greeting-state] Active blocked")
    stories = {
        "s1": {"status": "backlog", "title": "S1", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
        "s2": {"status": "backlog", "title": "S2", "epic_slug": "e", "story_file": False, "depends_on": ["s1"], "touches": []},
    }
    sprints = {
        "active": {"slug": "test-sprint", "status": "active", "locked": True, "stories": ["s1", "s2"]},
        "planning": None,
        "completed": []
    }
    proj = setup_project(stories=stories, sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 1, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "active-blocked")


def test_greeting_state_done_retro_needed():
    """Returns 'done-retro-needed' when active.status == 'done'."""
    print("\n[session greeting-state] Done retro needed")
    sprints = {
        "active": {"slug": "test-sprint", "status": "done", "locked": True, "stories": ["s1"]},
        "planning": {"slug": "next-sprint", "status": "ready", "locked": False, "stories": ["s2"]},
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 3, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "done-retro-needed")


def test_greeting_state_no_active_nothing_planned():
    """Returns correct state when both null."""
    print("\n[session greeting-state] No active, nothing planned")
    sprints = {
        "active": None,
        "planning": None,
        "completed": [{"slug": "old-sprint", "completed": "2026-03-15"}]
    }
    proj = setup_project(sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 5, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "no-active-nothing-planned")
    assert_eq("last_completed_sprint", out.get("last_completed_sprint"), "old-sprint")


def test_greeting_state_no_active_planned_ready():
    """Returns correct state with ready planning sprint."""
    print("\n[session greeting-state] No active, planned ready")
    sprints = {
        "active": None,
        "planning": {"slug": "next-sprint", "status": "ready", "locked": False, "stories": ["s1"]},
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 2, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "no-active-planned-ready")
    assert_eq("planning_sprint", out.get("planning_sprint"), "next-sprint")
    assert_eq("planning_status", out.get("planning_status"), "ready")


def test_greeting_state_active_planned_needs_work():
    """Returns correct state with planning sprint in 'planning'."""
    print("\n[session greeting-state] Active, planned needs work")
    stories = {
        "s1": {"status": "in-progress", "title": "S1", "epic_slug": "e", "story_file": False, "depends_on": [], "touches": []},
    }
    sprints = {
        "active": {"slug": "test-sprint", "status": "active", "locked": True, "stories": ["s1"]},
        "planning": {"slug": "next-sprint", "status": "planning", "locked": False, "stories": []},
        "completed": []
    }
    proj = setup_project(stories=stories, sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 3, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "active-planned-needs-work")


def test_greeting_state_done_no_planned():
    """Returns 'done-no-planned' when done and no planning sprint."""
    print("\n[session greeting-state] Done, no planned")
    sprints = {
        "active": {"slug": "test-sprint", "status": "done", "locked": True, "stories": ["s1"]},
        "planning": None,
        "completed": []
    }
    proj = setup_project(sprints=sprints)
    setup_installed_json(proj, {"session_stats": {"momentum_completions": 3, "last_invocation": "2026-04-01"}})
    code, out = run_tool(proj, "session", "greeting-state")
    assert_eq("exit code 0", code, 0)
    assert_eq("state", out.get("state"), "done-no-planned")


# --- Session Startup-Check Tests ---

def test_startup_check_all_clean():
    """Returns all false/empty when versions match and no drift."""
    print("\n[session startup-check] All clean")
    proj = setup_project()
    setup_versions_json(proj, {"current_version": "1.0.0", "versions": {}})
    setup_installed_json(proj, {"version": "1.0.0"})
    # Create a temporary global-installed.json for this test
    global_dir = proj / ".claude-global-test"
    # We'll use env override — but startup-check reads ~/.claude/momentum/global-installed.json
    # For testing, we need to ensure global version matches too
    # The simplest approach: backup and create a test global-installed.json
    global_path = Path.home() / ".claude" / "momentum" / "global-installed.json"
    backup = None
    if global_path.exists():
        backup = global_path.read_text()
    global_path.parent.mkdir(parents=True, exist_ok=True)
    global_path.write_text(json.dumps({"version": "1.0.0", "components": {}}, indent=2) + "\n")
    try:
        code, out = run_tool(proj, "session", "startup-check")
        assert_eq("exit code 0", code, 0)
        assert_eq("needs_upgrade false", out.get("needs_upgrade"), False)
        assert_eq("needs_install false", out.get("needs_install"), False)
        assert_eq("hash_drift false", out.get("hash_drift"), False)
        assert_eq("config_gaps empty", out.get("config_gaps"), [])
        assert_eq("installed_version", out.get("installed_version"), "1.0.0")
        assert_eq("current_version", out.get("current_version"), "1.0.0")
    finally:
        if backup is not None:
            global_path.write_text(backup)
        else:
            global_path.unlink(missing_ok=True)


def test_startup_check_needs_upgrade():
    """Returns needs_upgrade: true when version behind."""
    print("\n[session startup-check] Needs upgrade")
    proj = setup_project()
    setup_versions_json(proj, {"current_version": "2.0.0", "versions": {}})
    setup_installed_json(proj, {"version": "1.0.0"})
    global_path = Path.home() / ".claude" / "momentum" / "global-installed.json"
    backup = None
    if global_path.exists():
        backup = global_path.read_text()
    global_path.parent.mkdir(parents=True, exist_ok=True)
    global_path.write_text(json.dumps({"version": "1.0.0", "components": {}}, indent=2) + "\n")
    try:
        code, out = run_tool(proj, "session", "startup-check")
        assert_eq("exit code 0", code, 0)
        assert_eq("needs_upgrade true", out.get("needs_upgrade"), True)
        assert_eq("installed_version", out.get("installed_version"), "1.0.0")
        assert_eq("current_version", out.get("current_version"), "2.0.0")
    finally:
        if backup is not None:
            global_path.write_text(backup)
        else:
            global_path.unlink(missing_ok=True)


def test_startup_check_hash_drift():
    """Returns hash_drift: true when file hash mismatches."""
    print("\n[session startup-check] Hash drift detected")
    proj = setup_project()
    setup_versions_json(proj, {"current_version": "1.0.0", "versions": {}})
    setup_installed_json(proj, {"version": "1.0.0"})

    # Create a target file for hash checking
    target_file = proj / "test-rule.md"
    target_file.write_text("# Original content\n")

    # Get the real hash
    proc = subprocess.run(["git", "hash-object", str(target_file)], capture_output=True, text=True)
    real_hash = proc.stdout.strip()

    # Set up global-installed with a WRONG hash for this file
    global_path = Path.home() / ".claude" / "momentum" / "global-installed.json"
    backup = None
    if global_path.exists():
        backup = global_path.read_text()
    global_path.parent.mkdir(parents=True, exist_ok=True)
    global_path.write_text(json.dumps({
        "version": "1.0.0",
        "components": {
            "test-rule": {"hash": "wrong-hash-value", "target": str(target_file)}
        }
    }, indent=2) + "\n")
    try:
        code, out = run_tool(proj, "session", "startup-check")
        assert_eq("exit code 0", code, 0)
        assert_eq("hash_drift true", out.get("hash_drift"), True)
    finally:
        if backup is not None:
            global_path.write_text(backup)
        else:
            global_path.unlink(missing_ok=True)


def test_startup_check_needs_install():
    """Returns needs_install: true when no installed.json."""
    print("\n[session startup-check] Needs install")
    proj = setup_project()
    setup_versions_json(proj, {"current_version": "1.0.0", "versions": {}})
    # Do NOT create installed.json
    global_path = Path.home() / ".claude" / "momentum" / "global-installed.json"
    backup = None
    if global_path.exists():
        backup = global_path.read_text()
    global_path.parent.mkdir(parents=True, exist_ok=True)
    global_path.write_text(json.dumps({"version": "1.0.0", "components": {}}, indent=2) + "\n")
    try:
        code, out = run_tool(proj, "session", "startup-check")
        assert_eq("exit code 0", code, 0)
        assert_eq("needs_install true", out.get("needs_install"), True)
    finally:
        if backup is not None:
            global_path.write_text(backup)
        else:
            global_path.unlink(missing_ok=True)


# --- Runner ---

def main():
    global PASS_COUNT, FAIL_COUNT

    print("momentum-tools test suite")
    print("=" * 50)

    test_valid_forward_transition()
    test_invalid_non_adjacent_forward()
    test_invalid_backward_transition()
    test_terminal_state_blocked()
    test_force_override()
    test_dropped_from_any_non_terminal()
    test_closed_incomplete_from_any_non_terminal()
    test_story_not_found()
    test_data_preservation()
    test_sprint_activate()
    test_sprint_activate_already_active()
    test_sprint_activate_no_planning()
    test_sprint_complete()
    test_sprint_complete_no_active()
    test_epic_membership()
    test_epic_membership_not_found()
    test_sprint_plan_add()
    test_sprint_plan_remove()
    test_sprint_plan_locked()
    test_sprint_plan_no_duplicates()
    test_log_with_sprint_and_story()
    test_log_without_story()
    test_log_without_sprint()
    test_log_entry_valid_jsonl()
    test_log_multiple_appends()
    test_log_invalid_event_type()
    test_log_missing_required_args()
    test_log_all_event_types()
    test_log_special_characters()

    # Sprint status field tests
    test_sprint_plan_sets_status_planning()
    test_sprint_activate_sets_status_active()
    test_sprint_complete_sets_status_done()

    # Sprint ready tests
    test_sprint_ready_sets_status_ready()
    test_sprint_ready_no_planning()

    # Sprint retro-complete tests
    test_sprint_retro_complete_basic()
    test_sprint_retro_complete_auto_activates()
    test_sprint_retro_complete_no_auto_activate_when_planning()
    test_sprint_retro_complete_no_completed_sprints()

    # Sprint next-stories tests
    test_next_stories_all_unblocked()
    test_next_stories_some_blocked()
    test_next_stories_done_excluded()
    test_next_stories_no_active_sprint()

    # Session stats-update tests
    test_session_stats_update_creates()
    test_session_stats_update_increments()
    test_session_stats_update_preserves_data()

    # Session greeting-state tests
    test_greeting_state_first_session()
    test_greeting_state_active_in_progress()
    test_greeting_state_active_not_started()
    test_greeting_state_active_blocked()
    test_greeting_state_done_retro_needed()
    test_greeting_state_no_active_nothing_planned()
    test_greeting_state_no_active_planned_ready()
    test_greeting_state_active_planned_needs_work()
    test_greeting_state_done_no_planned()

    # Session startup-check tests
    test_startup_check_all_clean()
    test_startup_check_needs_upgrade()
    test_startup_check_hash_drift()
    test_startup_check_needs_install()

    print(f"\n{'=' * 50}")
    print(f"Results: {PASS_COUNT} passed, {FAIL_COUNT} failed")

    sys.exit(1 if FAIL_COUNT > 0 else 0)


if __name__ == "__main__":
    main()
