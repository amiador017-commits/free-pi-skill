# Security policy

## Supported versions

| Version | Supported |
|---|---|
| 2.0.x | Yes |
| < 2.0 | No |

## Reporting a vulnerability

Open a private security advisory on this repository, or email `amiador017@gmail.com` with:

- affected version
- reproduction steps
- potential impact

Please do not open a public issue for an unpatched vulnerability. You should receive an acknowledgement within 72 hours.

## Scope

This repo contains one Markdown skill file, one Bash installer, an SVG logo, and documentation. It contains no compiled binaries, no runtime dependencies, no build step, and no telemetry.

The skill makes one read-only GET to `https://api.freepi.ai/client-version` per task, authenticated with the user's own locally stored free-pi token. The token is never printed or written elsewhere. The installer verifies a pinned SHA-256 checksum before installing `SKILL.md`.

Out of scope: vulnerabilities in the free-pi CLI or in Hermes Agent itself. Report those to their respective maintainers.
