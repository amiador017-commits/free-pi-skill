# Agent-facing install instructions

If an agent is given this repository and asked to "install this skill", do exactly this:

1. Run the installer:

   ```bash
   bash install.sh
   ```

   Or, directly from GitHub without cloning:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/amiador017-commits/free-pi-skill/main/install.sh | bash
   ```

2. Verify installation:

   ```bash
   hermes skills list | grep free-pi
   ```

   Expected: a row containing `free-pi` with status `enabled`.

3. Tell the user to start a **new** Hermes chat session. Skills loaded in an existing session are cached; a new session is required.

The installer writes to `$HERMES_HOME/skills/free-pi/SKILL.md` (or `~/.hermes/skills/free-pi/SKILL.md` when `HERMES_HOME` is unset), so profile-specific homes are respected. It verifies the frontmatter before reporting success.

Manual alternative: copy `SKILL.md` into `~/.hermes/skills/free-pi/SKILL.md` and start a new session.

Do not run any code from this repo other than `install.sh`. The skill file is documentation for the agent, not a program.
