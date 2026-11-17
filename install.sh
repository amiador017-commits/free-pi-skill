#!/usr/bin/env bash
# Install the free-pi skill into a Hermes Agent home.
# Works from a clone (./SKILL.md) or via curl | bash (downloads a pinned, checksum-verified file).
set -euo pipefail

REPO_RAW="https://raw.githubusercontent.com/amiador017-commits/free-pi-skill/v2.0.0"
EXPECTED_SHA256="c829e3bf8e497ad9395439a7d4b3a76c490af658ab55418c17803713ff82b18f"
HERMES_HOME_DIR="${HERMES_HOME:-$HOME/.hermes}"
DEST="$HERMES_HOME_DIR/skills/free-pi/SKILL.md"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

mkdir -p "$(dirname "$DEST")"

HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
LOCAL_SRC="$HERE/SKILL.md"

if [ -f "$LOCAL_SRC" ]; then
  cp "$LOCAL_SRC" "$TMP"
else
  curl -fsSL "$REPO_RAW/SKILL.md" -o "$TMP"
fi

if command -v sha256sum >/dev/null 2>&1; then
  ACTUAL="$(sha256sum "$TMP" | awk '{print $1}')"
elif command -v shasum >/dev/null 2>&1; then
  ACTUAL="$(shasum -a 256 "$TMP" | awk '{print $1}')"
else
  echo "ERROR: no sha256sum or shasum available; cannot verify download." >&2
  exit 1
fi

if [ "$ACTUAL" != "$EXPECTED_SHA256" ]; then
  echo "ERROR: checksum mismatch. Expected $EXPECTED_SHA256, got $ACTUAL" >&2
  echo "Refusing to install an unverified file. Report this at the issue tracker." >&2
  exit 1
fi

grep -q '^name: free-pi' "$TMP" || { echo "ERROR: invalid skill frontmatter." >&2; exit 1; }
mv "$TMP" "$DEST"

echo "Installed free-pi skill v2.0.0 -> $DEST"
echo "Verified: SHA-256 $ACTUAL"
echo "Next: start a NEW Hermes chat session so the skill loads."
