#!/usr/bin/env bash
# === VERIFICATION HEADER (Part A) ===
# story_slug: base-body-collapse-rollback
# verification_method: bash
# harness_profile: bash
# contract_path: .momentum/sprints/sprint-2026-07-13/specs/base-body-collapse-rollback.smoke.sh
# how_dev_self_checks: Run this script; observe exit 0 and PASS output.
# coverage_disposition: dedicated-run
# covered_by_scenario: null
# acceptance_criteria_ref: .momentum/stories/base-body-collapse-rollback.md#acceptance-criteria
# platforms: [host]

# base-body-collapse-rollback smoke contract
# Harness profile: bash
#
# Invocation:
#   ./base-body-collapse-rollback.smoke.sh
#
# Expected: the plugin ships exactly one dev base body and no pre-shipped dev
# specialist bodies; specialist classification no longer resolves any input to
# a removed specialist body; and dev-role routing-table resolution returns the
# sole surviving dev base body rather than a removed specialist file.

set -euo pipefail

AGENTS_DIR="skills/momentum/agents"
FAIL=0

# Assert: the three pre-shipped dev specialist base-body files no longer exist
for f in dev-frontend.md dev-build.md dev-skills.md; do
  if [ -e "$AGENTS_DIR/$f" ]; then
    echo "FAIL: expected $AGENTS_DIR/$f to be removed but it still exists"
    FAIL=1
  fi
done

# Assert: exactly one dev base body remains, and no dev-* specialist file survives
if [ ! -e "$AGENTS_DIR/dev.md" ]; then
  echo "FAIL: expected $AGENTS_DIR/dev.md to exist but it is missing"
  FAIL=1
fi

DEV_STAR_COUNT=$(ls "$AGENTS_DIR" | grep -c '^dev-' || true)
if [ "$DEV_STAR_COUNT" -ne 0 ]; then
  echo "FAIL: expected zero dev-* specialist files under $AGENTS_DIR, found $DEV_STAR_COUNT"
  FAIL=1
fi

# Assert: specialist classification no longer resolves frontend/build/skill-shaped
# inputs to a pre-shipped dev specialist body
FRONTEND_OUT=$(python3 skills/momentum/scripts/momentum-tools.py specialist-classify --touches "app/src/main/kotlin/ui/HomeScreen.kt")
if echo "$FRONTEND_OUT" | grep -q '"specialist": "dev-frontend"'; then
  echo "FAIL: specialist-classify still resolves a frontend-shaped path to dev-frontend: $FRONTEND_OUT"
  FAIL=1
fi

BUILD_OUT=$(python3 skills/momentum/scripts/momentum-tools.py specialist-classify --touches "build.gradle.kts")
if echo "$BUILD_OUT" | grep -q '"specialist": "dev-build"'; then
  echo "FAIL: specialist-classify still resolves a build-shaped path to dev-build: $BUILD_OUT"
  FAIL=1
fi

SKILLS_OUT=$(python3 skills/momentum/scripts/momentum-tools.py specialist-classify --touches "skills/foo/SKILL.md")
if echo "$SKILLS_OUT" | grep -q '"specialist": "dev-skills"'; then
  echo "FAIL: specialist-classify still resolves a skill-file path to dev-skills: $SKILLS_OUT"
  FAIL=1
fi

# Assert: routing-table resolution for the dev role returns the sole surviving
# dev base body, not a removed specialist file
ROLE_OUT=$(python3 skills/momentum/scripts/momentum-tools.py agent resolve --role dev)
if ! echo "$ROLE_OUT" | grep -q '"agent_path": "skills/momentum/agents/dev.md"'; then
  echo "FAIL: expected agent resolve --role dev to return skills/momentum/agents/dev.md but got: $ROLE_OUT"
  FAIL=1
fi
if echo "$ROLE_OUT" | grep -E -q '"agent_path": "skills/momentum/agents/dev-(frontend|build|skills)\.md"'; then
  echo "FAIL: agent resolve --role dev still points at a removed specialist body: $ROLE_OUT"
  FAIL=1
fi

if [ "$FAIL" -ne 0 ]; then
  exit 1
fi

echo "PASS"
