#!/usr/bin/env bash
# Install the free-pi skill (SKILL.md + scripts/pi_picker.py) into a Hermes Agent home.
# Works from a clone (./SKILL.md, ./scripts/) or via curl | bash (downloads pinned,
# checksum-verified files from the release tag).
set -euo pipefail

REPO_RAW="https://raw.githubusercontent.com/amiador017-commits/free-pi-skill/v2.2.0"
EXPECTED_SKILL_SHA256="e208bc12e0dac4037e1922915d80a5830e8c176e926d13345a16340adc2ee761"
EXPECTED_PICKER_SHA256="44f1f182ac8529823beb219c682669f524434406559367e4d9a7899831040f17"
HERMES_HOME_DIR="${HERMES_HOME:-$HOME/.hermes}"
SKILL_DIR="$HERMES_HOME_DIR/skills/free-pi"
DEST_SKILL="$SKILL_DIR/SKILL.md"
DEST_PICKER="$SKILL_DIR/scripts/pi_picker.py"

sha256_of() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then shasum -a 256 "$1" | awk '{print $1}'
  else echo "ERROR: no sha256sum or shasum available; cannot verify download." >&2; exit 1
  fi
}

TMP_SKILL="$(mktemp)"; TMP_PICKER="$(mktemp)"
trap 'rm -f "$TMP_SKILL" "$TMP_PICKER"' EXIT
mkdir -p "$SKILL_DIR/scripts"

HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"

if [ -f "$HERE/SKILL.md" ] && [ -f "$HERE/scripts/pi_picker.py" ]; then
  cp "$HERE/SKILL.md" "$TMP_SKILL"
  cp "$HERE/scripts/pi_picker.py" "$TMP_PICKER"
else
  curl -fsSL "$REPO_RAW/SKILL.md" -o "$TMP_SKILL"
  curl -fsSL "$REPO_RAW/scripts/pi_picker.py" -o "$TMP_PICKER"
fi

ACTUAL_SKILL="$(sha256_of "$TMP_SKILL")"
ACTUAL_PICKER="$(sha256_of "$TMP_PICKER")"
if [ "$ACTUAL_SKILL" != "$EXPECTED_SKILL_SHA256" ]; then
  echo "ERROR: SKILL.md checksum mismatch. Expected $EXPECTED_SKILL_SHA256, got $ACTUAL_SKILL" >&2
  echo "Refusing to install an unverified file. Report this at the issue tracker." >&2
  exit 1
fi
if [ "$ACTUAL_PICKER" != "$EXPECTED_PICKER_SHA256" ]; then
  echo "ERROR: pi_picker.py checksum mismatch. Expected $EXPECTED_PICKER_SHA256, got $ACTUAL_PICKER" >&2
  echo "Refusing to install an unverified file. Report this at the issue tracker." >&2
  exit 1
fi

grep -q '^name: free-pi' "$TMP_SKILL" || { echo "ERROR: invalid skill frontmatter." >&2; exit 1; }
grep -q 'def classify' "$TMP_PICKER" || { echo "ERROR: picker script looks truncated." >&2; exit 1; }
if ! python3 -m py_compile "$TMP_PICKER" 2>/dev/null; then
  echo "ERROR: pi_picker.py failed to byte-compile (python3 required)." >&2; exit 1
fi
rm -rf "$(dirname "$TMP_PICKER")/__pycache__"

mv "$TMP_SKILL" "$DEST_SKILL"
mv "$TMP_PICKER" "$DEST_PICKER"
chmod +x "$DEST_PICKER"

echo "Installed free-pi skill v2.2.0"
echo "  $DEST_SKILL   (SHA-256 $ACTUAL_SKILL)"
echo "  $DEST_PICKER  (SHA-256 $ACTUAL_PICKER)"
echo "Next: start a NEW Hermes chat session so the skill loads."
