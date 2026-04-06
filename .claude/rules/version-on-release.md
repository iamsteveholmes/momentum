# Version on Release

When a sprint completes and merges to main:

1. Bump `skills/momentum/.claude-plugin/plugin.json` version
   - Patch (0.x.Y) for bug fixes and minor improvements
   - Minor (0.X.0) for new features, new commands, or behavioral changes
2. Commit: `chore(plugin): bump version to X.Y.Z — brief description`
3. Push includes the version bump commit

This ensures every push to main carries an updated version that downstream projects can pull via `/plugin marketplace update momentum`.
