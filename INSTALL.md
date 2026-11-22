# Agent-facing install instructions

If an agent is given this repository and asked to "install this skill", do exactly this:

1. Run the pinned, checksum-verified installer:

   ```bash
   bash install.sh
   ```

   Or, directly from GitHub without cloning:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/amiador017-commits/free-pi-skill/v2.2.0/install.sh | bash
   ```

   The installer downloads `SKILL.md` and `scripts/pi_picker.py` from the `v2.2.0` tag and verifies each file's SHA-256 before writing into the skills directory. A checksum mismatch aborts the install. It writes exactly two persistent files, both under `$HERMES_HOME/skills/free-pi/`.

2. Verify installation:

   ```bash
   hermes skills list | grep free-pi
   python3 "$HERMES_HOME/skills/free-pi/scripts/pi_picker.py" --tier free_unlimited --shortcuts
   ```

   Expected: a row containing `free-pi` with status `enabled`, and a short JSON list of shortcut strings printed by the picker (it reads the live catalog with your own free-pi token).

3. Tell the user to start a **new** Hermes chat session. Skills loaded in an existing session are cached; a new session is required.

## Prerequisite

The free-pi CLI is **not** installed by this repo. Before calling the setup complete, check that Node.js 22.15.0+ is present and `npx free-pi-cli@latest --version` works. If it is missing, tell the user to install it with `npm install -g free-pi-cli@latest` and sign in on first run. See the README's Prerequisites section.

## Paths and scope

- Target: `$HERMES_HOME/skills/free-pi/` (`SKILL.md` plus `scripts/pi_picker.py`), or `~/.hermes/skills/free-pi/` when `HERMES_HOME` is unset. Profile-specific homes are respected.
- The skill is Markdown instructions; `pi_picker.py` is the only executable it ships, and its job is the read-only catalog lookup and the tier rendering. Do not execute other code blocks in `SKILL.md`; they are documentation for the agent that loads the skill.
- Do not run any other file from this repo besides `install.sh`.

## Manual alternative

Copy `SKILL.md` and `scripts/pi_picker.py` into `~/.hermes/skills/free-pi/` (keeping the `scripts/` subdirectory), then start a new session. Verify with `sha256sum SKILL.md scripts/pi_picker.py`; both expected digests are in `install.sh`. A skill installed without `scripts/pi_picker.py` is incomplete: the preflight cannot render a full tier.

## Availability

Hermes Agent only for now. Other agents are planned for a later release.
