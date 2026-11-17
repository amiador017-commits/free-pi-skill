# free-pi skill (Hermes Agent)

A Hermes Agent skill that turns a rough one-line request into one precise, scoped prompt for the [free-pi](https://freepi.ai) CLI. Model and reasoning are picked at runtime through a popup instead of being hardcoded in a prompt.

> **Availability:** Currently available for **Hermes Agent only**. Support for other agents (Claude Code, Codex, opencode) is planned for a later release.

## What it does

1. Discovers the live free-unlimited models from free-pi's own catalog (`/client-version`) on every task.
2. Shows a two-question picker: model + reasoning level.
3. Opens free-pi in a PTY, applies the picks, then submits one precise prompt.
4. Stays in the prompt-engineer lane: it never writes code, edits files, or does the task itself.

## Requirements

- Hermes Agent with skills support, plus the `terminal`, `process_manage` and `clarify` tools.
- The free-pi CLI: `npx free-pi-cli@latest`, signed in. The token lives at `~/.free-pi/agent/credentials.json`.

## Install

One command:

```bash
curl -fsSL https://raw.githubusercontent.com/amiador017-commits/free-pi-skill/main/install.sh | bash
```

Or from a clone: `bash install.sh`.

Then start a **new** Hermes chat session so the skill loads. Verify with `hermes skills list | grep free-pi`.

An agent given this repo can follow `INSTALL.md`, which contains the same steps in agent-facing form.

## Usage

Say `use free-pi to <task>` or `finish/fix/build X with free-pi`. A model/reasoning popup appears before anything runs. General chat questions do not trigger this skill.

## Notes

- No secrets are bundled. The skill reads your own local free-pi token at runtime and never prints it.
- The free-unlimited list is time-limited and can change, so it is re-fetched on every task.
- Valid reasoning levels are `off`, `minimal`, `low`, `medium`, `high`. `high` is the maximum; `max` and `xhigh` are rejected by the CLI.
- `clarify` allows at most four choices, so a fifth model or the `off` level can be entered through its "Other" row.

## License

MIT. See `LICENSE`.
