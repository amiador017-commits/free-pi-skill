# Changelog

All notable changes to this project are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.2.0] - 2026-11-22

### Added

- `scripts/pi_picker.py`: the single sanctioned row generator for the preflight. It does the catalog discovery, the tiering, the sorting, and the rendering, and it asserts `rows == models` before writing anything (exit 3 on disagreement). Modes: `--json`, `--tier T --widget`, `--tier T --table`, `--tier T --shortcuts`.
- Full-tier model picker. On hosts with an inline widget surface (Hermes Desktop) the chosen tier is rendered as one clickable row per model, each row sending `free-pi model: <id>` back to the chat. On other hosts the complete numbered table is printed in chat and only a shortcut popup follows.
- Startup-stall notes: the `npx` "Ok to proceed? (y)" prompt and the 60-90s TUI render window, both of which used to look like hangs.
- Credit accounting section: Daily allowance vs Banked wallet, which models draw from which pool, and why an ultrafast run leaves the daily allowance untouched.
- `deepseek-v4.1-flash-1017-ultrafast` filter row plus the discovery-id vs picker-id mismatch note (`ultrafast` filters to "No matching models"; the picker id is `deepseek-v4.1-flash-600tps`).
- Audit-session additions: a finished audit can leave a stale `Working` spinner (kill rather than wait), self-load flakes from the agent running its own suites in parallel, `vitest` exiting 1 with all tests passed, and the prioritized P0/P1/P2 deliverable shape.

### Fixed

- **The model list was truncated to four entries.** `clarify` caps `choices` at 4, so a 10- or 14-model tier could never be a form; the model step now shows every model of the tier instead of the four lowest-usage ones.
- The model question is never merged with another question (folder, task detail, reasoning) into one form. One question per call, in order.
- Tier descriptions no longer state a fixed "0.2x to 5.9x" range for free-at-capacity; the real boundary is the 20x cutoff, and the current catalog reaches 19x inside that tier.
- Model membership is never hardcoded. The old "Currently ..." lists were stale within days, so they became dated samples with explicit counts, and the discovery output is the only source of rows.
- CLI version is no longer pinned in the text; `free-pi --version` moves fast inside 0.6.x.

### Changed

- The preflight reads "tier (form) → every model of that tier (picker) → reasoning (form)". Hand-writing model rows is forbidden, as is re-implementing discovery inline.
- If discovery fails, the `/model` probe PTY fallback is explicit about the script's exit code 2.

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
