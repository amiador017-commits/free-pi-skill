# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.0.0] - 2026-11-17

### Added

- Live discovery of free-unlimited models from free-pi's `/client-version` catalog on every task.
- Runtime model + reasoning picker (`clarify`) with an agent-facing text fallback.
- Explicit prompt-engineer-only role boundary: no code, no file edits, no task execution by the orchestrating agent.
- Tagged, SHA-256-verified installer.
- Security policy, agent-facing install instructions, and repo documentation.

### Changed

- Model and reasoning are no longer hardcoded in the prompt text.
- Verification is separated from implementation: the orchestrating agent checks results but never writes source.

## [1.0.0]

- Initial private version of the free-pi orchestration skill.
