# Eval: Plugin No Dead References

## Setup
Search all files under skills/momentum/ for path references.

## Expected Behavior
1. No file references `skills/momentum-<name>/` (old satellite path pattern)
2. Every path reference to a skill directory resolves to an existing path
3. momentum-tools.py references point to `skills/momentum/scripts/momentum-tools.py`
4. Plugin-root references (references/, scripts/, hooks/) resolve correctly
