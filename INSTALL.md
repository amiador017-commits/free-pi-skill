# Agent-facing install instructions

If an agent is given this repository and asked to "install this skill", do exactly this:

1. Run the pinned, checksum-verified installer:

   ```bash
   bash install.sh
   ```

   Or, directly from GitHub without cloning:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/amiador017-commits/free-pi-skill/v2.0.0/install.sh | bash
   ```

   The installer downloads `SKILL.md` from the `v2.0.0` tag and verifies its SHA-256 before writing into the skills directory. A checksum mismatch aborts the install. It writes exactly one persistent file.

2. Verify installation:

   ```bash
   hermes skills list | grep free-pi
   ```

   Expected: a row containing `free-pi` with status `enabled`.

3. Tell the user to start a **new** Hermes chat session. Skills loaded in an existing session are cached; a new session is required.

## Prerequisite

The free-pi CLI is **not** installed by this repo. Before calling the setup complete, check that Node.js 22.15.0+ is present and `npx free-pi-cli@latest --version` works. If it is missing, tell the user to install it with `npm install -g free-pi-cli@latest` and sign in on first run. See the README's Prerequisites section.

## Paths and scope

- Target: `$HERMES_HOME/skills/free-pi/SKILL.md`, or `~/.hermes/skills/free-pi/SKILL.md` when `HERMES_HOME` is unset. Profile-specific homes are respected.
- The skill is plain Markdown instructions. Do not execute its code blocks; they are documentation for the agent that loads it.
- Do not run any file from this repo other than `install.sh`.

## Manual alternative

Copy `SKILL.md` into `~/.hermes/skills/free-pi/SKILL.md`, then start a new session. Verify with `sha256sum SKILL.md`; the expected digest is in `install.sh`.

## Availability

Hermes Agent only for now. Other agents are planned for a later release.
