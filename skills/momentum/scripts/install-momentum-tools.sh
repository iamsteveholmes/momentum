#!/usr/bin/env bash
# install-momentum-tools.sh — Install the momentum-tools PATH shim
#
# Places a symlink (or copy) of the momentum-tools wrapper into ~/.local/bin
# so that bare `momentum-tools` resolves in any shell — interactive or not.
#
# Usage:
#   bash skills/momentum/scripts/install-momentum-tools.sh
#
# IMPORTANT: Run this script from a stable checkout (the repo root or a plugin-cache
# copy), NOT from a transient worktree path (e.g. .worktrees/). A worktree-relative
# symlink target will break when the worktree is removed.
#
# Prerequisites:
#   - ~/.local/bin must be on your PATH (it is by default on this machine via ~/.zshrc)
#   - python3 must be available
#
# After running this script, verify with:
#   command -v momentum-tools
#   momentum-tools --help

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WRAPPER="$SCRIPT_DIR/../bin/momentum-tools"
TARGET_DIR="$HOME/.local/bin"
TARGET="$TARGET_DIR/momentum-tools"

# Resolve absolute path to the wrapper
WRAPPER="$(cd "$(dirname "$WRAPPER")" && pwd)/$(basename "$WRAPPER")"

if [ ! -f "$WRAPPER" ]; then
  echo "ERROR: wrapper not found at $WRAPPER" >&2
  exit 1
fi

# Warn if the wrapper resolves inside a transient worktree path
if echo "$WRAPPER" | grep -q '/.worktrees/'; then
  echo "WARNING: wrapper resolves inside a worktree path: $WRAPPER" >&2
  echo "  Worktrees are ephemeral — the symlink will break when the worktree is removed." >&2
  echo "  Run this installer from a stable checkout (repo root or plugin-cache copy)." >&2
fi

if [ ! -x "$WRAPPER" ]; then
  chmod +x "$WRAPPER"
  echo "made $WRAPPER executable"
fi

# Ensure target directory exists
mkdir -p "$TARGET_DIR"

# Install as symlink (preferred — tracks live repo edits)
if [ -L "$TARGET" ]; then
  OLD="$(readlink "$TARGET")"
  if [ "$OLD" = "$WRAPPER" ]; then
    echo "already installed: $TARGET -> $WRAPPER"
    exit 0
  fi
  echo "updating symlink: $TARGET (was $OLD)"
  rm "$TARGET"
elif [ -e "$TARGET" ]; then
  echo "ERROR: $TARGET already exists as a non-symlink file." >&2
  echo "  Remove it manually and re-run: rm $TARGET" >&2
  exit 1
fi

ln -s "$WRAPPER" "$TARGET"
echo "installed: $TARGET -> $WRAPPER"

# Quick smoke-test
if command -v momentum-tools >/dev/null 2>&1; then
  echo "verified: command -v momentum-tools -> $(command -v momentum-tools)"
else
  echo "WARNING: momentum-tools still not found on PATH — you may need to reload your shell or add ~/.local/bin to PATH"
fi
