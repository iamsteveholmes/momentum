#!/usr/bin/env bash
# b1-epic-schema-migration-define-epicsjson-migrate-features smoke contract
# Harness profile: bash
#
# Black-box verification of the epic-schema migration outcome: epics.json
# exists and is well-formed, all features from the prior layer survive as
# entries, the prior file is archived, and every story currently registered
# in stories/index.json names an epic_slug that resolves to an entry in
# epics.json.
#
# Invocation:
#   bash .momentum/sprints/sprint-2026-05-26/specs/b1-epic-schema-migration-define-epicsjson-migrate-features.smoke.sh

set -euo pipefail

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

EPICS_JSON="_bmad-output/planning-artifacts/epics.json"
FEATURES_JSON="_bmad-output/planning-artifacts/features.json"
FEATURES_ARCHIVE="_bmad-output/planning-artifacts/archive/features-pre-2026-05.json"
STORIES_INDEX=".momentum/stories/index.json"

# --- Files in expected states ------------------------------------------------

test -f "$EPICS_JSON" || {
  echo "FAIL: $EPICS_JSON missing"
  exit 1
}

test ! -e "$FEATURES_JSON" || {
  echo "FAIL: legacy $FEATURES_JSON should be removed (migrated to archive)"
  exit 1
}

test -f "$FEATURES_ARCHIVE" || {
  echo "FAIL: archive $FEATURES_ARCHIVE missing"
  exit 1
}

# --- epics.json parses as JSON object ----------------------------------------

python3 -c "
import json, sys
with open('$EPICS_JSON') as f:
    data = json.load(f)
if not isinstance(data, dict):
    print('FAIL: epics.json root is not an object')
    sys.exit(1)
if len(data) == 0:
    print('FAIL: epics.json contains zero entries')
    sys.exit(1)
" || exit 1

# --- Schema check: every entry has the required fields ----------------------

python3 -c "
import json, sys
with open('$EPICS_JSON') as f:
    data = json.load(f)
REQUIRED = ['epic_slug','name','description','lifecycle','audience','stories','stories_done','stories_remaining','last_verified','notes']
LIFECYCLE = {'finite-lived','long-lived'}
AUDIENCE = {'user','internal'}
errors = []
for slug, entry in data.items():
    if slug == '_migration':
        continue  # reserved provenance key, not an epic entry
    for field in REQUIRED:
        if field not in entry:
            errors.append(f'{slug}: missing {field}')
    if entry.get('lifecycle') not in LIFECYCLE:
        errors.append(f'{slug}: lifecycle={entry.get(\"lifecycle\")!r} not in {LIFECYCLE}')
    if entry.get('audience') not in AUDIENCE:
        errors.append(f'{slug}: audience={entry.get(\"audience\")!r} not in {AUDIENCE}')
    if isinstance(entry.get('stories'), list):
        seen = set()
        for sk in entry['stories']:
            if sk in seen:
                errors.append(f'{slug}: duplicate story {sk!r} in stories[]')
            seen.add(sk)
if errors:
    print('FAIL: schema violations:')
    for e in errors[:20]:
        print('  -', e)
    sys.exit(1)
" || exit 1

# --- Migration of 23 features: every pre-migration feature_slug is an
#     epic_slug in epics.json (read the archive to enumerate them) -----------

python3 -c "
import json, sys
with open('$FEATURES_ARCHIVE') as f:
    features = json.load(f)
with open('$EPICS_JSON') as f:
    epics = json.load(f)
missing = [slug for slug in features.keys() if slug not in epics]
if missing:
    print(f'FAIL: {len(missing)} features did not migrate to epics.json:')
    for slug in missing[:20]:
        print('  -', slug)
    sys.exit(1)
" || exit 1

# --- Every story in stories/index.json has an epic_slug that exists in
#     epics.json (no orphaned epic_slug references) ---------------------------

python3 -c "
import json, sys
with open('$STORIES_INDEX') as f:
    idx = json.load(f)
with open('$EPICS_JSON') as f:
    epics = json.load(f)
orphans = []
missing_epic = []
for story_key, s in idx.items():
    if not isinstance(s, dict):
        continue
    es = s.get('epic_slug')
    if not es:
        orphans.append(story_key)
        continue
    if es not in epics:
        missing_epic.append((story_key, es))
if orphans:
    print(f'FAIL: {len(orphans)} stories missing epic_slug (first 10): {orphans[:10]}')
    sys.exit(1)
if missing_epic:
    print(f'FAIL: {len(missing_epic)} stories reference epic_slug not in epics.json (first 10): {missing_epic[:10]}')
    sys.exit(1)
" || exit 1

# --- ad-hoc accepted as long-lived residue if present ------------------------

python3 -c "
import json, sys
with open('$EPICS_JSON') as f:
    epics = json.load(f)
if 'ad-hoc' in epics:
    if epics['ad-hoc'].get('lifecycle') != 'long-lived':
        print(f'FAIL: ad-hoc epic must be lifecycle=long-lived (got {epics[\"ad-hoc\"].get(\"lifecycle\")!r})')
        sys.exit(1)
" || exit 1

# --- Migration script committed at the expected path -------------------------

test -f "skills/momentum/scripts/migrate-features-to-epics.py" || {
  echo "FAIL: migration script skills/momentum/scripts/migrate-features-to-epics.py missing"
  exit 1
}

# --- Architecture / PRD annotation present ----------------------------------

grep -q 'epics\.json' "_bmad-output/planning-artifacts/architecture.md" || {
  echo "FAIL: architecture.md does not reference epics.json"
  exit 1
}

grep -qiE 'HISTORICAL|SUPERSEDED' "_bmad-output/planning-artifacts/architecture.md" || {
  echo "FAIL: architecture.md does not mark feature-layer decisions HISTORICAL/SUPERSEDED"
  exit 1
}

grep -qiE 'SUPERSEDED|DEC-034' "_bmad-output/planning-artifacts/prd.md" || {
  echo "FAIL: prd.md does not annotate feature-layer FRs as SUPERSEDED"
  exit 1
}

echo "PASS"
