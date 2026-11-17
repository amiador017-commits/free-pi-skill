# Contributing

Contributions are welcome. Keep the scope tight: this repo is one skill, not a framework.

## Ground rules

- `SKILL.md` stays a single self-contained file so an agent can install it with one copy.
- No binaries, no build step, no runtime dependencies, no telemetry.
- Never add secrets or print the user's free-pi token.
- Preserve the prompt-engineer-only role boundary. Do not add steps where the orchestrating agent writes or edits source.

## Changing the skill

1. Edit `SKILL.md`.
2. Recompute its SHA-256: `sha256sum SKILL.md`.
3. Update `EXPECTED_SHA256` in `install.sh`.
4. Update `CHANGELOG.md` and bump the version in `SKILL.md` frontmatter.
5. Test locally:

   ```bash
   bash -n install.sh
   TMP=$(mktemp -d); HERMES_HOME="$TMP" bash install.sh; rm -rf "$TMP"
   ```

6. Commit with a descriptive message. A maintainer publishes a matching release tag.

## Reporting issues

Open an issue with the Hermes version, the free-pi CLI version, and the exact prompt used. For security problems, follow [SECURITY.md](SECURITY.md) instead.

## License

By contributing you agree that your work is licensed under MIT.
