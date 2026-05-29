#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""
migrate-features-to-epics — Deterministic migration tool.

Implements DEC-034 D1–D5:
  1. Migrate 23 features from features.json → epics.json (unified epic shape)
  2. Apply categorical epic dispositions (dissolve | long-lived) from config YAML
  3. Re-home stories in stories/index.json to valid epic slugs
  4. Archive features.json to archive/features-pre-2026-05.json (byte-identical)
  5. Write epics.json with _migration provenance key

Usage:
    python3 migrate_features_to_epics.py [--root /path/to/project] [--dry-run]

Idempotent: running on an already-migrated state is a no-op (archive exists,
features.json gone → migration re-reads epics.json and re-syncs counts without
duplicating data).

Author: B1 migration story (sprint-2026-05-26)
"""

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────

REQUIRED_EPIC_FIELDS = [
    "epic_slug",
    "name",
    "description",
    "lifecycle",
    "audience",
    "stories",
    "stories_done",
    "stories_remaining",
    "last_verified",
    "notes",
]

VALID_LIFECYCLES = {"finite-lived", "long-lived"}
VALID_AUDIENCES = {"user", "internal"}

# Fields that MUST NOT be copied from features into epics
DROPPED_LEGACY_FIELDS = {"feature_slug", "status", "prd_section"}


# ──────────────────────────────────────────────────────────────────────────────
# Core transform functions
# ──────────────────────────────────────────────────────────────────────────────


def build_epic_from_feature(
    feature: dict[str, Any],
    lifecycle: str = "finite-lived",
    audience: str = "user",
) -> dict[str, Any]:
    """
    Transform a features.json entry into a unified epics.json entry.

    Rules:
    - feature_slug → epic_slug (direct rename, no mutation)
    - acceptance_condition (string) → acceptance_conditions (list, original as [0])
    - type carried if present, omitted if absent
    - lifecycle defaults to finite-lived, audience defaults to user
    - DROPPED_LEGACY_FIELDS are excluded
    """
    epic: dict[str, Any] = {}

    # Identifier
    epic["epic_slug"] = feature.get("feature_slug") or feature.get("epic_slug", "")

    # Core descriptive fields
    epic["name"] = feature["name"]
    epic["description"] = feature.get("description", "")

    # Classification
    epic["lifecycle"] = lifecycle
    epic["audience"] = audience

    # Value fields
    if "value_analysis" in feature:
        epic["value_analysis"] = feature["value_analysis"]
    if "system_context" in feature:
        epic["system_context"] = feature["system_context"]

    # Rename acceptance_condition → acceptance_conditions[]
    if "acceptance_conditions" in feature:
        # Already migrated or pre-set
        epic["acceptance_conditions"] = feature["acceptance_conditions"]
    elif "acceptance_condition" in feature and feature["acceptance_condition"]:
        epic["acceptance_conditions"] = [feature["acceptance_condition"]]
    else:
        epic["acceptance_conditions"] = []

    # Stories
    epic["stories"] = list(feature.get("stories", []))
    epic["stories_done"] = feature.get("stories_done", 0)
    epic["stories_remaining"] = feature.get("stories_remaining", 0)

    # Timestamps
    epic["last_verified"] = feature.get("last_verified", str(date.today()))

    # Notes
    epic["notes"] = feature.get("notes", "")

    # Optional depends_on
    if "depends_on" in feature:
        epic["depends_on"] = feature["depends_on"]

    # Optional type (flow | connection | quality) — carry only if present
    if "type" in feature:
        epic["type"] = feature["type"]

    return epic


def validate_epic_schema(epic: dict[str, Any]) -> list[str]:
    """
    Validate a single epic entry against the required schema.
    Returns a list of error messages (empty = valid).
    """
    errors: list[str] = []

    for field in REQUIRED_EPIC_FIELDS:
        if field not in epic:
            errors.append(f"Missing required field: {field!r}")

    if "lifecycle" in epic and epic["lifecycle"] not in VALID_LIFECYCLES:
        errors.append(f"Invalid lifecycle {epic['lifecycle']!r} — must be one of {VALID_LIFECYCLES}")

    if "audience" in epic and epic["audience"] not in VALID_AUDIENCES:
        errors.append(f"Invalid audience {epic['audience']!r} — must be one of {VALID_AUDIENCES}")

    if "stories" in epic and not isinstance(epic["stories"], list):
        errors.append(f"Field 'stories' must be a list, got {type(epic['stories']).__name__}")

    return errors


def compute_story_counts(
    story_keys: list[str],
    stories_index: dict[str, Any],
) -> tuple[int, int]:
    """
    Given a list of story_keys and the full stories index, return (done, remaining).
    - done: status == "done"
    - remaining: status in {backlog, ready-for-dev, in-progress} ONLY (per QA AC4)
    - everything else (done, dropped, closed-incomplete, review) is NOT remaining
    """
    REMAINING_STATUSES = {"backlog", "ready-for-dev", "in-progress"}
    done = 0
    remaining = 0
    for sk in story_keys:
        sv = stories_index.get(sk, {})
        status = sv.get("status", "backlog")
        if status == "done":
            done += 1
        elif status in REMAINING_STATUSES:
            remaining += 1
    return done, remaining


EPICS_MD_RESTRUCTURE_NOTE = (
    "epics.md restructure choice: retire-and-stub (per QA AC7). The legacy "
    "feature-organized epics.md is retired and replaced with a stub pointing at "
    "epics.json as the source of truth. Rationale: epics.json is now the canonical, "
    "machine-maintained epic registry (DEC-034); keeping a parallel hand-edited "
    "epics.md narrative would drift and create two competing sources of truth. The "
    "stub preserves the human entry point without duplicating mutable state."
)


def build_migration_log(
    dissolved: dict[str, str],
    long_lived: set[str],
    rehomed_count: int,
) -> dict[str, Any]:
    """
    Build the _migration provenance block embedded at the end of epics.json.

    Args:
        dissolved: {categorical_epic_slug: target_epic_slug}
        long_lived: set of epic slugs kept as long-lived
        rehomed_count: number of stories that had their epic_slug updated
    """
    return {
        "migrated_at": str(date.today()),
        "source": "features.json (archived to archive/features-pre-2026-05.json)",
        "decision": "DEC-034 (Epic-Layer Consolidation)",
        "dissolved": {slug: f"→ {target}" for slug, target in dissolved.items()},
        "long_lived": sorted(long_lived),
        "rehomed_story_count": rehomed_count,
        "epics_md_restructure": EPICS_MD_RESTRUCTURE_NOTE,
        "notes": (
            "This _migration key is reserved provenance metadata. "
            "It is not an epic entry. Tooling that iterates epics.json must skip this key. "
            + EPICS_MD_RESTRUCTURE_NOTE
        ),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Disposition loader
# ──────────────────────────────────────────────────────────────────────────────


def _load_json_or_die(path: Path, label: str) -> Any:
    """
    Parse a JSON file, exiting with a clear message and code 1 on failure.
    Used to guard all external JSON inputs (features.json, stories index, epics.json).
    """
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        print(
            f"ERROR: failed to parse {label} at {path}: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)


def load_dispositions(root: Path) -> dict[str, Any]:
    """
    Load categorical-epic-dispositions.yaml from skills/momentum/scripts/.
    Falls back to an empty dict if the file doesn't exist (no categoricals to process).
    """
    yaml_path = root / "skills" / "momentum" / "scripts" / "categorical-epic-dispositions.yaml"
    if not yaml_path.exists():
        return {}

    if not YAML_AVAILABLE:
        # Parse manually — simple YAML with string values only
        raise RuntimeError(
            "PyYAML not available. Install it with: pip install pyyaml\n"
            "Or: mise use pipx:pyyaml@latest"
        )

    with yaml_path.open() as f:
        return yaml.safe_load(f) or {}


# ──────────────────────────────────────────────────────────────────────────────
# Main migration runner
# ──────────────────────────────────────────────────────────────────────────────


def run_migration(root: Path | str = ".") -> None:
    """
    Execute the full migration. Idempotent.

    Steps:
    1. Check if already migrated (features.json absent, epics.json present → re-sync counts only)
    2. If not migrated: archive features.json, build epics.json from features, evaluate categoricals
    3. Sync stories/index.json epic_slugs for dissolved categoricals
    4. Write back epics.json with consistent stories[] arrays and recalculated counts
    """
    root = Path(root)
    artifacts = root / "_bmad-output" / "planning-artifacts"
    archive_dir = artifacts / "archive"
    features_path = artifacts / "features.json"
    epics_path = artifacts / "epics.json"
    stories_path = root / ".momentum" / "stories" / "index.json"

    dispositions = load_dispositions(root)

    # ── Load or derive epics from features ──────────────────────────────────

    existing_rehomed_count = 0

    if features_path.exists():
        # First run: validate-parse features.json BEFORE writing the archive, so a
        # corrupt input fails loudly without producing a junk byte-identical archive.
        features_raw = _load_json_or_die(features_path, "features.json")

        # Archive is byte-identical (only after a successful parse)
        archive_dir.mkdir(parents=True, exist_ok=True)
        archive_path = archive_dir / "features-pre-2026-05.json"
        archive_path.write_bytes(features_path.read_bytes())

        # Build initial epics from features
        epics: dict[str, Any] = {}
        for fslug, fdata in features_raw.items():
            epic = build_epic_from_feature(fdata)
            epics[epic["epic_slug"]] = epic

        # Remove original features.json
        features_path.unlink()

    elif epics_path.exists():
        # Already migrated — load existing epics for re-sync
        epics_raw = _load_json_or_die(epics_path, "epics.json")
        epics = {k: v for k, v in epics_raw.items() if k != "_migration"}
        # Preserve original rehomed_count from prior migration run (idempotency)
        existing_migration = epics_raw.get("_migration", {})
        existing_rehomed_count = existing_migration.get("rehomed_story_count", 0)
    else:
        # Nothing to migrate — start with empty
        epics = {}

    # ── Load stories index ───────────────────────────────────────────────────

    if stories_path.exists():
        stories: dict[str, Any] = _load_json_or_die(stories_path, "stories/index.json")
    else:
        stories = {}

    # ── Process categorical epic dispositions ────────────────────────────────

    dissolved: dict[str, str] = {}   # old_slug → target_epic_slug
    long_lived_slugs: set[str] = set()

    for cat_slug, disp in dispositions.items():
        disposition = disp.get("disposition", "dissolve")

        if disposition == "long-lived":
            long_lived_slugs.add(cat_slug)
            # Create or update the long-lived epic entry
            if cat_slug not in epics:
                epics[cat_slug] = {
                    "epic_slug": cat_slug,
                    "name": disp.get("name", cat_slug.replace("-", " ").title()),
                    "description": disp.get("description", ""),
                    "lifecycle": "long-lived",
                    "audience": disp.get("audience", "internal"),
                    "acceptance_conditions": [],
                    "stories": [],
                    "stories_done": 0,
                    "stories_remaining": 0,
                    "last_verified": str(date.today()),
                    "notes": disp.get("notes", ""),
                }
            else:
                epics[cat_slug]["lifecycle"] = "long-lived"
                if disp.get("notes"):
                    epics[cat_slug]["notes"] = disp["notes"]

        elif disposition == "dissolve":
            target_slug = disp.get("target_epic", "ad-hoc")
            dissolved[cat_slug] = target_slug

    # ── Re-home stories from dissolved categoricals ──────────────────────────
    # Only count as "rehomed" when the epic_slug actually changes.

    rehomed_count = 0
    for sk, sv in stories.items():
        current_epic = sv.get("epic_slug", "")
        if current_epic in dissolved:
            target = dissolved[current_epic]
            # Ensure target epic exists (fallback to ad-hoc if not)
            if target not in epics and target != "ad-hoc":
                target = "ad-hoc"
            if sv["epic_slug"] != target:
                sv["epic_slug"] = target
                rehomed_count += 1

    # ── Delete dissolved categorical epics still lingering in epics ──────────
    # A dissolved cat_slug that also happens to be a feature/epic key would
    # otherwise survive the re-home loop as an empty zombie entry (code-review F1).
    for cat_slug in dissolved:
        if cat_slug in epics:
            del epics[cat_slug]

    # ── Ensure ad-hoc exists as long-lived ──────────────────────────────────

    if "ad-hoc" not in epics:
        ad_hoc_notes = (
            dispositions.get("ad-hoc", {}).get("notes", "")
            or "Canonical residue catcher — long-lived per DEC-034 D2. Accepts stories that don't fit any finite-lived epic."
        )
        epics["ad-hoc"] = {
            "epic_slug": "ad-hoc",
            "name": "Ad-Hoc Work",
            "description": "Residue catcher for stories that don't belong to a specific finite-lived epic.",
            "lifecycle": "long-lived",
            "audience": "internal",
            "acceptance_conditions": [],
            "stories": [],
            "stories_done": 0,
            "stories_remaining": 0,
            "last_verified": str(date.today()),
            "notes": ad_hoc_notes,
        }
    else:
        epics["ad-hoc"]["lifecycle"] = "long-lived"
        if not epics["ad-hoc"].get("notes"):
            epics["ad-hoc"]["notes"] = "Canonical residue catcher — long-lived per DEC-034 D2."

    # ── Rebuild stories[] arrays in epics from stories/index.json ───────────
    # This ensures the bidirectional invariant: stories/index.json ↔ epics.json

    # Clear existing stories arrays to rebuild from index
    for epic_slug in epics:
        epics[epic_slug]["stories"] = []

    for sk, sv in stories.items():
        original = sv.get("epic_slug", "ad-hoc")
        epic_slug = original
        if epic_slug not in epics:
            # Unknown epic_slug — re-home to ad-hoc
            sv["epic_slug"] = "ad-hoc"
            epic_slug = "ad-hoc"
            # Only count if this was a real change (not already ad-hoc)
            if original != "ad-hoc":
                rehomed_count += 1
        if sk not in epics[epic_slug]["stories"]:
            epics[epic_slug]["stories"].append(sk)

    # ── Recalculate story counts ─────────────────────────────────────────────

    for epic_slug, epic in epics.items():
        done, remaining = compute_story_counts(epic["stories"], stories)
        epic["stories_done"] = done
        epic["stories_remaining"] = remaining

    # ── Validate all epics ───────────────────────────────────────────────────

    errors_found: list[str] = []
    for slug, epic in epics.items():
        errs = validate_epic_schema(epic)
        for e in errs:
            errors_found.append(f"  epic {slug!r}: {e}")

    if errors_found:
        print("VALIDATION ERRORS:", file=sys.stderr)
        for e in errors_found:
            print(e, file=sys.stderr)
        sys.exit(1)

    # ── Build migration log ──────────────────────────────────────────────────

    # On a re-sync run, features.json is gone so no stories actually move and
    # rehomed_count is 0 — carry forward the original count to preserve provenance
    # (code-review F3: existing_rehomed_count was read but never used).
    effective_rehomed_count = max(rehomed_count, existing_rehomed_count)

    migration_log = build_migration_log(
        dissolved=dissolved,
        long_lived=long_lived_slugs | {"ad-hoc"},
        rehomed_count=effective_rehomed_count,
    )

    # ── Write outputs ────────────────────────────────────────────────────────

    # epics.json: epics + _migration block
    output = dict(epics)
    output["_migration"] = migration_log

    artifacts.mkdir(parents=True, exist_ok=True)
    epics_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")

    # stories/index.json: write back with updated epic_slugs
    if stories_path.exists():
        stories_path.write_text(json.dumps(stories, indent=2, ensure_ascii=False) + "\n")

    # ── Summary ─────────────────────────────────────────────────────────────

    print(f"Migration complete.")
    print(f"  Epics written:        {len(epics)}")
    print(f"  Dissolved categoricals: {len(dissolved)}")
    print(f"  Long-lived epics:     {len(long_lived_slugs | {'ad-hoc'})}")
    print(f"  Stories re-homed:     {rehomed_count}")
    if (archive_dir / "features-pre-2026-05.json").exists():
        sha = hashlib.sha256((archive_dir / "features-pre-2026-05.json").read_bytes()).hexdigest()
        print(f"  Archive SHA256:       {sha}")


# ──────────────────────────────────────────────────────────────────────────────
# CLI entry point
# ──────────────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Migrate features.json to epics.json per DEC-034."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done without writing any files",
    )
    args = parser.parse_args()

    if args.dry_run:
        print("Dry-run mode: no files will be written.")
        root = Path(args.root)
        features_path = root / "_bmad-output" / "planning-artifacts" / "features.json"
        epics_path = root / "_bmad-output" / "planning-artifacts" / "epics.json"
        if features_path.exists():
            features = json.loads(features_path.read_text())
            print(f"Would migrate {len(features)} features.")
        elif epics_path.exists():
            print("Already migrated — would re-sync counts only.")
        else:
            print("Nothing to migrate.")
        return

    run_migration(root=args.root)


if __name__ == "__main__":
    main()
