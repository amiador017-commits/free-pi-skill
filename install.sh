#!/usr/bin/env bash
# Install the free-pi skill into a Hermes Agent home.
# Works from a clone (./SKILL.md) or via curl | bash (downloads from GitHub).
set -euo pipefail

REPO_RAW="https://raw.githubusercontent.com/amiador017-commits/free-pi-skill/main"
HERMES_HOME_DIR="${HERMES_HOME:-$HOME/.hermes}"
DEST="$HERMES_HOME_DIR/skills/free-pi/SKILL.md"

mkdir -p "$(dirname "$DEST")"

HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
LOCAL_SRC="$HERE/SKILL.md"

if [ -f "$LOCAL_SRC" ]; then
  cp "$LOCAL_SRC" "$DEST"
else
  curl -fsSL "$REPO_RAW/SKILL.md" -o "$DEST"
fi

if grep -q '^name: free-pi' "$DEST"; then
  echo "Installed free-pi skill -> $DEST"
  echo "Verified: frontmatter name: free-pi"
  echo "Open a NEW Hermes chat session so the skill loads."
else
  echo "ERROR: installed file failed verification: $DEST" >&2
  exit 1
fi
