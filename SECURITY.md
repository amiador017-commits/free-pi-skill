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

Please do not open a public issue for an unpatched vulnerability. I will respond as soon as I can; no response time is guaranteed.

## Scope

This repo contains one Markdown skill file, one Bash installer, an SVG logo, and documentation. It contains no compiled binaries, no runtime dependencies, no build step, and no telemetry.

The skill's discovery step makes one read-only GET to `https://api.freepi.ai/client-version` per task, authenticated with the user's own locally stored free-pi token. The token is never printed or written elsewhere. The free-pi CLI is a separate prerequisite and is not installed by this repo; it makes its own network calls. The installer verifies a pinned SHA-256 checksum before writing into the skills directory.

Out of scope: vulnerabilities in the free-pi CLI or in Hermes Agent itself. Report those to their respective maintainers.
