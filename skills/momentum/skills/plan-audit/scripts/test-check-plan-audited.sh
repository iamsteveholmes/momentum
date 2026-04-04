#!/usr/bin/env bash
# Unit tests for check-plan-audited.sh
# Tests three cases: empty dir, plan without Spec Impact, plan with Spec Impact.
#
# Usage: bash skills/momentum-plan-audit/scripts/test-check-plan-audited.sh
# Run from project root.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK_SCRIPT="$SCRIPT_DIR/check-plan-audited.sh"
PASS=0
FAIL=0

run_test() {
  local name="$1"
  local expected_exit="$2"
  local test_dir="$3"

  PLANS_DIR="$test_dir" bash "$CHECK_SCRIPT"
  local actual_exit=$?

  if [ "$actual_exit" -eq "$expected_exit" ]; then
    echo "  PASS  $name (exit $actual_exit)"
    PASS=$((PASS + 1))
  else
    echo "  FAIL  $name (expected $expected_exit, got $actual_exit)"
    FAIL=$((FAIL + 1))
  fi
}

# Setup: create temp directories
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

EMPTY_DIR="$TMPDIR/empty"
NO_IMPACT_DIR="$TMPDIR/no-impact"
WITH_IMPACT_DIR="$TMPDIR/with-impact"

mkdir -p "$EMPTY_DIR" "$NO_IMPACT_DIR" "$WITH_IMPACT_DIR"

# Test 2 setup: plan without Spec Impact
cat > "$NO_IMPACT_DIR/plan.md" << 'EOF'
# Plan: Some work

## Context

Some context here.

## Verification

- Thing works
EOF

# Test 3 setup: plan with Spec Impact
cat > "$WITH_IMPACT_DIR/plan.md" << 'EOF'
# Plan: Some work

## Context

Some context here.

## Spec Impact

**Classification:** substantive

**Go/No-Go:** Proceed.
EOF

echo "Running check-plan-audited.sh unit tests..."
echo ""

run_test "Empty plans directory → exit 0 (allow)" 0 "$EMPTY_DIR"
run_test "Plan without Spec Impact → exit 2 (block)" 2 "$NO_IMPACT_DIR"
run_test "Plan with Spec Impact → exit 0 (allow)" 0 "$WITH_IMPACT_DIR"

echo ""
echo "Results: $PASS passed, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
exit 0
