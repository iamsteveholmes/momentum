#!/usr/bin/env python3
"""
Tests for migrate-features-to-epics.py

Red-green-refactor TDD:
  - Schema shape transform (one feature in → one epic out, all carried fields preserved)
  - stories/index.json round-trip (every story has valid epic_slug; epics.json stories[] match)
  - Archive path creation (features.json → archive/features-pre-2026-05.json, byte-identical, original removed)
  - Idempotency (running twice on same input → same output)
"""

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# We import the module under test — will fail until implemented
sys.path.insert(0, str(Path(__file__).parent))
try:
    from migrate_features_to_epics import (
        REQUIRED_EPIC_FIELDS,
        VALID_AUDIENCES,
        VALID_LIFECYCLES,
        build_epic_from_feature,
        build_migration_log,
        compute_story_counts,
        run_migration,
        validate_epic_schema,
    )
    MODULE_AVAILABLE = True
except ImportError:
    MODULE_AVAILABLE = False


# ──────────────────────────────────────────────────────────────────────────────
# Minimal sample fixtures
# ──────────────────────────────────────────────────────────────────────────────

SAMPLE_FEATURE = {
    "feature_slug": "momentum-sprint-retro",
    "name": "Sprint Retrospective — Transcript Audit and Sprint Closure",
    "type": "flow",
    "description": "momentum:retro conducts a transcript-based sprint review.",
    "acceptance_condition": "A developer can run momentum:retro after a sprint.",
    "value_analysis": "The retro skill works and is actively used.",
    "system_context": "Closes the sprint loop.",
    "status": "working",
    "prd_section": None,
    "stories": ["retro-skill", "retro-workflow-rewrite"],
    "stories_done": 4,
    "stories_remaining": 0,
    "last_verified": "2026-05-03",
    "notes": "All 4 stories done.",
}

SAMPLE_FEATURE_NO_TYPE = {
    "feature_slug": "momentum-agent-role-contracts",
    "name": "Agent Role Contracts",
    "description": "Plugin-shipped role definitions.",
    "acceptance_condition": "A developer can run sprint-dev.",
    "value_analysis": "Agents have base bodies.",
    "system_context": "The agent vocabulary layer.",
    "status": "partial",
    "stories": ["dev-agent-definition-files"],
    "stories_done": 2,
    "stories_remaining": 17,
    "last_verified": "2026-05-14",
    "notes": "Split out from composable-specialist-agents.",
}


SAMPLE_STORIES_INDEX = {
    "retro-skill": {
        "status": "done",
        "title": "Retro Skill",
        "epic_slug": "story-cycles",
        "story_file": True,
        "depends_on": [],
        "touches": [],
        "priority": "low",
    },
    "retro-workflow-rewrite": {
        "status": "done",
        "title": "Retro Workflow Rewrite",
        "epic_slug": "story-cycles",
        "story_file": True,
        "depends_on": [],
        "touches": [],
        "priority": "low",
    },
    "dev-agent-definition-files": {
        "status": "done",
        "title": "Dev Agent Definition Files",
        "epic_slug": "agent-team-model",
        "story_file": True,
        "depends_on": [],
        "touches": [],
        "priority": "medium",
    },
    "orphan-story": {
        "status": "backlog",
        "title": "Orphan Story",
        "epic_slug": "ad-hoc",
        "story_file": True,
        "depends_on": [],
        "touches": [],
        "priority": "low",
    },
}

# Categorical epic dispositions: dissolve or long-lived
SAMPLE_DISPOSITIONS = {
    "story-cycles": {
        "disposition": "dissolve",
        "target_epic": "momentum-sprint-retro",
        "notes": "Dissolved — stories re-homed to retro epic.",
    },
    "agent-team-model": {
        "disposition": "dissolve",
        "target_epic": "momentum-agent-role-contracts",
        "notes": "Dissolved — stories re-homed to agent role contracts epic.",
    },
    "ad-hoc": {
        "disposition": "long-lived",
        "notes": "Canonical residue catcher — kept as long-lived per DEC-034 D2.",
    },
}


# ──────────────────────────────────────────────────────────────────────────────
# Test: Schema shape transform
# ──────────────────────────────────────────────────────────────────────────────

@unittest.skipUnless(MODULE_AVAILABLE, "migrate_features_to_epics module not yet implemented")
class TestBuildEpicFromFeature(unittest.TestCase):
    def test_basic_shape_transform(self):
        """Feature → epic carries all required fields."""
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        for field in REQUIRED_EPIC_FIELDS:
            self.assertIn(field, epic, f"Missing required field: {field}")

    def test_epic_slug_renamed_from_feature_slug(self):
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        self.assertEqual(epic["epic_slug"], "momentum-sprint-retro")

    def test_name_carried_forward(self):
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        self.assertEqual(epic["name"], SAMPLE_FEATURE["name"])

    def test_description_carried_forward(self):
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        self.assertEqual(epic["description"], SAMPLE_FEATURE["description"])

    def test_value_analysis_carried_forward(self):
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        self.assertEqual(epic["value_analysis"], SAMPLE_FEATURE["value_analysis"])

    def test_system_context_carried_forward(self):
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        self.assertEqual(epic["system_context"], SAMPLE_FEATURE["system_context"])

    def test_acceptance_condition_becomes_acceptance_conditions_array(self):
        """acceptance_condition string becomes acceptance_conditions[0]."""
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        self.assertIsInstance(epic["acceptance_conditions"], list)
        self.assertEqual(epic["acceptance_conditions"][0], SAMPLE_FEATURE["acceptance_condition"])

    def test_stories_array_carried_forward(self):
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        self.assertEqual(epic["stories"], SAMPLE_FEATURE["stories"])

    def test_stories_done_carried_forward(self):
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        self.assertEqual(epic["stories_done"], SAMPLE_FEATURE["stories_done"])

    def test_stories_remaining_carried_forward(self):
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        self.assertEqual(epic["stories_remaining"], SAMPLE_FEATURE["stories_remaining"])

    def test_last_verified_carried_forward(self):
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        self.assertEqual(epic["last_verified"], SAMPLE_FEATURE["last_verified"])

    def test_notes_carried_forward(self):
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        self.assertEqual(epic["notes"], SAMPLE_FEATURE["notes"])

    def test_type_carried_when_present(self):
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        self.assertEqual(epic.get("type"), "flow")

    def test_type_omitted_when_absent(self):
        epic = build_epic_from_feature(SAMPLE_FEATURE_NO_TYPE)
        self.assertNotIn("type", epic)

    def test_default_lifecycle_finite_lived(self):
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        self.assertEqual(epic["lifecycle"], "finite-lived")

    def test_default_audience_user(self):
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        self.assertEqual(epic["audience"], "user")

    def test_legacy_fields_dropped(self):
        """feature_slug, status, prd_section must not appear in the epic."""
        epic = build_epic_from_feature(SAMPLE_FEATURE)
        self.assertNotIn("feature_slug", epic)
        self.assertNotIn("status", epic)
        self.assertNotIn("prd_section", epic)


# ──────────────────────────────────────────────────────────────────────────────
# Test: Schema validation
# ──────────────────────────────────────────────────────────────────────────────

@unittest.skipUnless(MODULE_AVAILABLE, "migrate_features_to_epics module not yet implemented")
class TestValidateEpicSchema(unittest.TestCase):
    def _make_valid_epic(self, **overrides):
        base = {
            "epic_slug": "test-epic",
            "name": "Test",
            "description": "Desc",
            "lifecycle": "finite-lived",
            "audience": "user",
            "stories": [],
            "stories_done": 0,
            "stories_remaining": 0,
            "last_verified": "2026-05-01",
            "notes": "ok",
        }
        base.update(overrides)
        return base

    def test_valid_epic_passes(self):
        errors = validate_epic_schema(self._make_valid_epic())
        self.assertEqual(errors, [])

    def test_missing_required_field_fails(self):
        epic = self._make_valid_epic()
        del epic["lifecycle"]
        errors = validate_epic_schema(epic)
        self.assertTrue(any("lifecycle" in e for e in errors))

    def test_invalid_lifecycle_fails(self):
        epic = self._make_valid_epic(lifecycle="permanent")
        errors = validate_epic_schema(epic)
        self.assertTrue(any("lifecycle" in e for e in errors))

    def test_invalid_audience_fails(self):
        epic = self._make_valid_epic(audience="external")
        errors = validate_epic_schema(epic)
        self.assertTrue(any("audience" in e for e in errors))

    def test_stories_must_be_list(self):
        epic = self._make_valid_epic(stories="not-a-list")
        errors = validate_epic_schema(epic)
        self.assertTrue(any("stories" in e for e in errors))


# ──────────────────────────────────────────────────────────────────────────────
# Test: Story count computation
# ──────────────────────────────────────────────────────────────────────────────

@unittest.skipUnless(MODULE_AVAILABLE, "migrate_features_to_epics module not yet implemented")
class TestComputeStoryCounts(unittest.TestCase):
    def test_counts_match_stories_index_distribution(self):
        """done → stories_done; backlog/ready-for-dev/in-progress → stories_remaining."""
        stories = {
            "a": {"status": "done", "epic_slug": "e1"},
            "b": {"status": "done", "epic_slug": "e1"},
            "c": {"status": "backlog", "epic_slug": "e1"},
            "d": {"status": "dropped", "epic_slug": "e1"},  # excluded
        }
        done, remaining = compute_story_counts(["a", "b", "c", "d"], stories)
        self.assertEqual(done, 2)
        self.assertEqual(remaining, 1)

    def test_dropped_excluded(self):
        stories = {"a": {"status": "dropped", "epic_slug": "e1"}}
        done, remaining = compute_story_counts(["a"], stories)
        self.assertEqual(done, 0)
        self.assertEqual(remaining, 0)

    def test_review_not_counted_as_remaining(self):
        """QA AC4: review status is NOT remaining (only backlog/ready-for-dev/in-progress)."""
        stories = {
            "a": {"status": "review", "epic_slug": "e1"},
            "b": {"status": "review", "epic_slug": "e1"},
            "c": {"status": "in-progress", "epic_slug": "e1"},
            "d": {"status": "ready-for-dev", "epic_slug": "e1"},
            "e": {"status": "backlog", "epic_slug": "e1"},
            "f": {"status": "done", "epic_slug": "e1"},
        }
        done, remaining = compute_story_counts(["a", "b", "c", "d", "e", "f"], stories)
        self.assertEqual(done, 1)
        # 9-review analogue: only in-progress + ready-for-dev + backlog count = 3
        self.assertEqual(remaining, 3)

    def test_closed_incomplete_not_counted_as_remaining(self):
        stories = {"a": {"status": "closed-incomplete", "epic_slug": "e1"}}
        done, remaining = compute_story_counts(["a"], stories)
        self.assertEqual(done, 0)
        self.assertEqual(remaining, 0)


# ──────────────────────────────────────────────────────────────────────────────
# Test: Archive path creation
# ──────────────────────────────────────────────────────────────────────────────

@unittest.skipUnless(MODULE_AVAILABLE, "migrate_features_to_epics module not yet implemented")
class TestArchiveCreation(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.artifacts = self.tmp / "_bmad-output" / "planning-artifacts"
        self.artifacts.mkdir(parents=True)
        self.archive = self.artifacts / "archive"
        self.stories_dir = self.tmp / ".momentum" / "stories"
        self.stories_dir.mkdir(parents=True)

        # Write sample features.json
        self.features_path = self.artifacts / "features.json"
        sample = {"feat-a": SAMPLE_FEATURE}
        self.features_path.write_text(json.dumps(sample, indent=2))

        # Write sample stories/index.json
        self.stories_path = self.stories_dir / "index.json"
        self.stories_path.write_text(json.dumps(SAMPLE_STORIES_INDEX, indent=2))

        # Write dispositions YAML
        self.scripts_dir = self.tmp / "skills" / "momentum" / "scripts"
        self.scripts_dir.mkdir(parents=True)
        disp_path = self.scripts_dir / "categorical-epic-dispositions.yaml"
        import yaml
        disp_path.write_text(yaml.dump(SAMPLE_DISPOSITIONS))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_archive_file_created(self):
        run_migration(root=self.tmp)
        archive_file = self.archive / "features-pre-2026-05.json"
        self.assertTrue(archive_file.exists(), "Archive file must be created")

    def test_archive_is_byte_identical_to_original(self):
        original_sha = hashlib.sha256(self.features_path.read_bytes()).hexdigest()
        run_migration(root=self.tmp)
        archive_file = self.archive / "features-pre-2026-05.json"
        archive_sha = hashlib.sha256(archive_file.read_bytes()).hexdigest()
        self.assertEqual(original_sha, archive_sha, "Archive must be byte-identical to original features.json")

    def test_original_features_removed(self):
        run_migration(root=self.tmp)
        self.assertFalse(self.features_path.exists(), "Original features.json must be removed after migration")

    def test_epics_json_created(self):
        run_migration(root=self.tmp)
        epics_path = self.artifacts / "epics.json"
        self.assertTrue(epics_path.exists(), "epics.json must be created")

    def test_epics_json_parses_valid(self):
        run_migration(root=self.tmp)
        epics_path = self.artifacts / "epics.json"
        data = json.loads(epics_path.read_text())
        self.assertIsInstance(data, dict)

    def test_epics_json_contains_migrated_feature(self):
        run_migration(root=self.tmp)
        epics = json.loads((self.artifacts / "epics.json").read_text())
        self.assertIn("momentum-sprint-retro", epics)


# ──────────────────────────────────────────────────────────────────────────────
# Test: stories/index.json round-trip
# ──────────────────────────────────────────────────────────────────────────────

@unittest.skipUnless(MODULE_AVAILABLE, "migrate_features_to_epics module not yet implemented")
class TestStoriesIndexRoundTrip(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.artifacts = self.tmp / "_bmad-output" / "planning-artifacts"
        self.artifacts.mkdir(parents=True)
        self.archive = self.artifacts / "archive"
        self.stories_dir = self.tmp / ".momentum" / "stories"
        self.stories_dir.mkdir(parents=True)

        features = {
            "momentum-sprint-retro": SAMPLE_FEATURE,
            "momentum-agent-role-contracts": SAMPLE_FEATURE_NO_TYPE,
        }
        (self.artifacts / "features.json").write_text(json.dumps(features, indent=2))
        (self.stories_dir / "index.json").write_text(json.dumps(SAMPLE_STORIES_INDEX, indent=2))

        self.scripts_dir = self.tmp / "skills" / "momentum" / "scripts"
        self.scripts_dir.mkdir(parents=True)
        import yaml
        (self.scripts_dir / "categorical-epic-dispositions.yaml").write_text(yaml.dump(SAMPLE_DISPOSITIONS))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_every_story_has_valid_epic_slug_after_migration(self):
        """After migration, every story in index.json has an epic_slug present in epics.json."""
        run_migration(root=self.tmp)
        stories = json.loads((self.stories_dir / "index.json").read_text())
        epics = json.loads((self.artifacts / "epics.json").read_text())
        for sk, sv in stories.items():
            self.assertIn(
                sv["epic_slug"], epics,
                f"Story {sk!r} has epic_slug {sv['epic_slug']!r} not in epics.json",
            )

    def test_bidirectional_invariant(self):
        """
        For every epic in epics.json, its stories[] matches the set of stories in
        stories/index.json whose epic_slug points to it.
        """
        run_migration(root=self.tmp)
        stories = json.loads((self.stories_dir / "index.json").read_text())
        epics = json.loads((self.artifacts / "epics.json").read_text())

        for epic_slug, epic in epics.items():
            if epic_slug == "_migration":
                continue
            members_from_index = {
                sk for sk, sv in stories.items()
                if sv.get("epic_slug") == epic_slug
            }
            members_from_epic = set(epic.get("stories", []))
            self.assertEqual(
                members_from_index, members_from_epic,
                f"Epic {epic_slug!r}: stories[] mismatch.\n"
                f"  index says: {sorted(members_from_index)}\n"
                f"  epic  says: {sorted(members_from_epic)}",
            )

    def test_dissolved_categorical_epic_stories_rehomed(self):
        """Stories from a dissolved categorical epic must be in the target epic."""
        run_migration(root=self.tmp)
        stories = json.loads((self.stories_dir / "index.json").read_text())
        # story-cycles dissolved → momentum-sprint-retro
        for sk, sv in stories.items():
            if sk in ("retro-skill", "retro-workflow-rewrite"):
                self.assertEqual(
                    sv["epic_slug"], "momentum-sprint-retro",
                    f"Story {sk} should be re-homed to momentum-sprint-retro",
                )

    def test_zero_orphans(self):
        """After migration, no story should have an epic_slug absent from epics.json."""
        run_migration(root=self.tmp)
        stories = json.loads((self.stories_dir / "index.json").read_text())
        epics = json.loads((self.artifacts / "epics.json").read_text())
        epic_keys = set(epics.keys()) - {"_migration"}
        orphans = [
            sk for sk, sv in stories.items()
            if sv.get("epic_slug", "") not in epic_keys
        ]
        self.assertEqual(orphans, [], f"Orphan stories found: {orphans}")


# ──────────────────────────────────────────────────────────────────────────────
# Test: Idempotency
# ──────────────────────────────────────────────────────────────────────────────

@unittest.skipUnless(MODULE_AVAILABLE, "migrate_features_to_epics module not yet implemented")
class TestIdempotency(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.artifacts = self.tmp / "_bmad-output" / "planning-artifacts"
        self.artifacts.mkdir(parents=True)
        self.stories_dir = self.tmp / ".momentum" / "stories"
        self.stories_dir.mkdir(parents=True)

        features = {"momentum-sprint-retro": SAMPLE_FEATURE}
        (self.artifacts / "features.json").write_text(json.dumps(features, indent=2))
        (self.stories_dir / "index.json").write_text(json.dumps(SAMPLE_STORIES_INDEX, indent=2))

        self.scripts_dir = self.tmp / "skills" / "momentum" / "scripts"
        self.scripts_dir.mkdir(parents=True)
        import yaml
        (self.scripts_dir / "categorical-epic-dispositions.yaml").write_text(yaml.dump(SAMPLE_DISPOSITIONS))

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_running_twice_produces_same_epics_json(self):
        """
        Second run on an already-migrated state must produce the same epics.json
        (idempotent — no duplicate entries, no crash). The _migration block may
        accumulate counts across runs; we check epic content equality (non-_migration keys).
        """
        run_migration(root=self.tmp)
        first_raw = json.loads((self.artifacts / "epics.json").read_text())
        first = {k: v for k, v in first_raw.items() if k != "_migration"}

        # Run again — features.json is gone, archive exists
        run_migration(root=self.tmp)
        second_raw = json.loads((self.artifacts / "epics.json").read_text())
        second = {k: v for k, v in second_raw.items() if k != "_migration"}

        self.assertEqual(
            first,
            second,
            "Second run should produce identical epic entries in epics.json",
        )

    def test_running_twice_does_not_duplicate_stories(self):
        run_migration(root=self.tmp)
        run_migration(root=self.tmp)
        epics = json.loads((self.artifacts / "epics.json").read_text())
        for slug, epic in epics.items():
            if slug == "_migration":
                continue
            stories_list = epic.get("stories", [])
            self.assertEqual(
                len(stories_list), len(set(stories_list)),
                f"Duplicate stories in epic {slug}: {stories_list}",
            )


# ──────────────────────────────────────────────────────────────────────────────
# Test: Migration log
# ──────────────────────────────────────────────────────────────────────────────

@unittest.skipUnless(MODULE_AVAILABLE, "migrate_features_to_epics module not yet implemented")
class TestBuildMigrationLog(unittest.TestCase):
    def test_migration_log_has_dissolved_section(self):
        log = build_migration_log(
            dissolved={"story-cycles": "momentum-sprint-retro"},
            long_lived={"ad-hoc"},
            rehomed_count=5,
        )
        self.assertIn("dissolved", log)
        self.assertIn("story-cycles", log["dissolved"])

    def test_migration_log_has_long_lived_section(self):
        log = build_migration_log(
            dissolved={},
            long_lived={"ad-hoc"},
            rehomed_count=0,
        )
        self.assertIn("long_lived", log)
        self.assertIn("ad-hoc", log["long_lived"])

    def test_rehomed_count_recorded(self):
        log = build_migration_log(dissolved={}, long_lived=set(), rehomed_count=42)
        self.assertEqual(log["rehomed_story_count"], 42)


if __name__ == "__main__":
    unittest.main(verbosity=2)
