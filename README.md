<div align="center">

<img src="docs/assets/logo.svg" alt="free-pi skill" width="640">

**One prompt in. A precisely scoped prompt out. The agent writes no code.**

<a href="https://github.com/amiador017-commits/free-pi-skill/releases"><img src="https://img.shields.io/github/v/release/amiador017-commits/free-pi-skill?style=flat-square&color=1f6feb" alt="Release"></a>
<img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License: MIT">
<img src="https://img.shields.io/badge/platform-linux%20%7C%20macOS-lightgrey?style=flat-square" alt="Platforms">
<img src="https://img.shields.io/badge/agent-Hermes-orange?style=flat-square" alt="Hermes Agent">
<img src="https://img.shields.io/badge/SHA--256-verified%20install-brightgreen?style=flat-square" alt="Checksum-verified installer">

**[Install](#install) · [Prerequisites](#prerequisites-free-pi-cli) · [Prompt](#prompt) · [How it works](#how-it-works) · [Security](#security-and-privacy) · [Usage](#usage) · [FAQ](#faq)**

</div>

---

> **Availability:** Currently available for **Hermes Agent only**. Support for other agents (Claude Code, Codex, opencode) is planned for a later release.

## The problem

You write a rough one-line prompt. The agent starts coding, picks its own model, guesses your reasoning level, and edits files before you can steer it.

## The fix

This skill puts the agent in one lane: **prompt engineer**. It reads your rough request, lets you pick the model and reasoning from a live list, hands one precise prompt to the [free-pi](https://freepi.ai) CLI, and reports back. It writes no code itself.

| | Without this skill | With this skill |
|---|---|---|
| Model | Chosen silently by the agent | Picked by you from the full live tier list |
| Reasoning | Guessed | Picked by you (`off` to `high`) |
| Prompt | Rough request passed through | Rewritten into one scoped, self-contained prompt |
| Who writes code | The agent, unpredictably | free-pi (by design) |
| Stale model names | Hardcoded in text | Re-discovered on every task |
| Truncated lists | \u2014 | Every model of a tier is one row; the generator asserts the count |

## Prerequisites: free-pi CLI

This skill is only instructions. It does **not** bundle or install the [free-pi CLI](https://freepi.ai). You must install and sign in to the CLI yourself; without it, live model discovery cannot run.

1. **Node.js 22.15.0 or newer** (required by `free-pi-cli`). Check with `node -v`.
2. **Install the CLI:**

   ```bash
   npm install -g free-pi-cli@latest
   ```

   Or run it on demand with `npx free-pi-cli@latest`, which fetches it the first time. This repository does neither; it only installs the skill file.
3. **Verify:** `free-pi-cli --version` (or `npx free-pi-cli@latest --version`).
4. **Sign in:** the first run starts a guest trial and then asks for GitHub sign-in. The token is stored at `~/.free-pi/agent/credentials.json`.

## How it works

1. **Discover** every model from free-pi's own catalog (`/client-version`) and group them into three tiers, with `scripts/pi_picker.py`. No cached list, no guessing, no hand-typed rows.
2. **Ask** in order: tier, then **every** model in that tier, then reasoning level. On Hermes Desktop the tier renders as an inline picker with one clickable row per model; elsewhere the full numbered table is printed in chat.
3. **Launch** free-pi in a PTY, apply your picks, verify the footer and session JSONL.
4. **Submit** one precise prompt built from your rough request.
5. **Report** the result. By design the agent does not write or edit source itself.

The three tiers are **Free Unlimited** (0 credit), **Free But At Capacity** (under 20x usage), and **Defense** (20x+ usage, premium or uncensored). Membership is decided by the live catalog on every task, so counts move between runs; the skill ships no model list. The second step shows the whole chosen tier, and the third picks the reasoning level.

The role boundary is written into the skill, not left to interpretation: zero code, zero file edits, no web search to answer your question, no taking over when free-pi stalls.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/amiador017-commits/free-pi-skill/v2.2.0/install.sh | bash
```

Or clone the repo and run `bash install.sh`. It writes exactly two persistent files, `~/.hermes/skills/free-pi/SKILL.md` and `~/.hermes/skills/free-pi/scripts/pi_picker.py`, and checks each file's SHA-256 before installing. It respects `$HERMES_HOME` for profile-specific installs. It does not install the free-pi CLI; see [Prerequisites](#prerequisites-free-pi-cli).

Then start a **new** Hermes chat session. Skills in an open session are cached. Verify with:

```bash
hermes skills list | grep free-pi
```

Giving this repo to another agent? Point it at [`INSTALL.md`](INSTALL.md), which is the same procedure in agent-facing form.

## Prompt

Copy this whole block and paste it into **any agent chat** (Hermes, Claude Code, Codex, or another agent). It installs and verifies the skill without you running commands yourself.

````text
Install the free-pi skill from https://github.com/amiador017-commits/free-pi-skill into this machine's Hermes Agent skills directory.

Do exactly this:
1. Fetch and read https://raw.githubusercontent.com/amiador017-commits/free-pi-skill/v2.2.0/install.sh. Confirm it only writes ~/.hermes/skills/free-pi/SKILL.md and ~/.hermes/skills/free-pi/scripts/pi_picker.py, and verifies a SHA-256 checksum for each. If it does anything else, stop and report it.
2. Check the free-pi CLI prerequisite with: npx free-pi-cli@latest --version. If it is missing, tell me to install it with `npm install -g free-pi-cli@latest` (Node.js 22.15.0+) and stop. Do not install it for me.
3. Run: curl -fsSL https://raw.githubusercontent.com/amiador017-commits/free-pi-skill/v2.2.0/install.sh | bash
4. Verify with: hermes skills list | grep free-pi
5. Report the installed path, the checksum printed, and tell me to start a NEW Hermes chat session so the skill loads.

Do not modify any other file. This skill is supported by Hermes Agent only for now. If Hermes is not installed here, stop and say so instead of installing anything.
````

## Usage

```
use free-pi to build a small landing page for my portfolio
```

You are asked for the tier, then shown every model in it, then the reasoning level. After you confirm, free-pi does the work with your choices applied.

General chat questions do not trigger this skill.

## Security and privacy

This repo is **plain Markdown plus a small Bash installer**. No compiled binaries, no build step, no telemetry, no dependency installation by this repo. The free-pi CLI is a separate prerequisite; see [Prerequisites](#prerequisites-free-pi-cli).

| Question | Answer |
|---|---|
| Does it contain secrets? | No. No token or API key is bundled. |
| What does the skill read? | Your own `~/.free-pi/agent/credentials.json`, at runtime. |
| Is the token ever printed? | No. It is used only in an Authorization header for the catalog call. |
| Network access from this skill's discovery step | One GET to `https://api.freepi.ai/client-version` per task. The free-pi CLI makes its own network calls once launched; those are its behaviour, not this repo's. |
| Files written by the installer | Two: `SKILL.md` and `scripts/pi_picker.py`, under your Hermes skills directory. |
| What does `pi_picker.py` do? | One read-only GET to the free-pi catalog, then it renders the tier list. It writes no file outside the picker HTML you ask it for, and it never prints your token. |
| How do I verify the download? | The installer pins a tag and verifies SHA-256 before installing. |

Install only from `amiador017-commits/free-pi-skill`. Report anything suspicious through [SECURITY.md](SECURITY.md).

## FAQ

**Why a popup instead of a default in the prompt?**
Because a model that is free today may not be free tomorrow. The list is fetched live on every task.

**Which reasoning levels exist?**
`off`, `minimal`, `low`, `medium`, `high`. `high` is the maximum; the CLI rejects `max` and `xhigh`.

**What if a tier has more than four models?**
It is not a form. `scripts/pi_picker.py` renders one row per model (typically 4, 14 and 10 in the current catalog) and refuses to output a list whose row count does not match the catalog. On hosts without an inline picker the full table is printed in chat and a four-option shortcut form sits on top of it.

**Does Hermes verify the result?**
Yes, with build/test/grep commands. That is checking, not implementing; verification should not turn into Hermes writing code.

## Contributions

Contributions are **closed for now**. Bug reports are welcome through the issue tracker; please do not open pull requests yet.

## License

MIT. See [LICENSE](LICENSE). The skill text is also MIT; free-pi itself is a separate product with its own terms.
