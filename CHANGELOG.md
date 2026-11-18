# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.1.0] - 2026-11-17

### Added

- Tier-first selection: the first popup now offers **Free Unlimited (0 credit)**, **Free But At Capacity (~0.2x to 5.9x usage)** and **Defense (20x+ usage)**.
- Live catalog discovery groups every model into those three tiers on every task, parsed from the real usage multiplier and section metadata.
- Second popup lists only models from the chosen tier, with their cost label; tiers larger than four choices are fully printed in chat and the "Other" row accepts an exact id.
- Reasoning stays as a separate third popup, so tier, model and reasoning are chosen in a clear order.

### Changed

- The old single two-question popup was replaced by three sequential popups.
- Model discovery no longer filters only free-unlimited models.

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
