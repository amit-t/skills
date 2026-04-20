# skill-sync

> Sync an existing at-skills skill from a source path, or scaffold a new one via `claude` / `codex` / `devin`

**Category:** Agent Behavior

## What It Does

Wraps the `skill-sync` zsh utility (lives in `ai-utils/skill-sync/`) so an agent can sync or scaffold skills inside any at-skills-style repo. Two modes:

- **Sync mode**: pull updates for an existing skill from a source directory (e.g. an upstream copy in another repo). Mirrors the directory and upserts catalog entries in `README.md`, `site.js`, `CHANGELOG.md`, and `skills-lock.json`.
- **Build mode**: scaffold a brand-new skill from a source directory by handing the work to `claude`, `codex`, or `devin` via a runtime prompt.

### When to Use

- You maintain a skill in another repo and want the at-skills copy refreshed.
- You have raw source material (notes, scripts, an existing AGENTS.md fragment) and want an agent to turn it into a polished at-skills skill.
- You are working in `qr-skills` or another at-skills-shaped repo and want the same workflow.

## Install

The companion utility lives in `ai-utils/skill-sync/`. Install it once:

```bash
cd ~/Projects/Tools-Utilities/ai-utils/skill-sync
./install.zsh
```

This symlinks `skill-sync` to `~/.local/bin/skill-sync`. Make sure `~/.local/bin` is on your `$PATH`.

Then add this skill to your agent of choice:

```bash
npx skills@latest add amit-t/skills --skill skill-sync
```

### Manual Installation

<details>
<summary>Devin / Windsurf</summary>

```bash
# Project-level
cp -r skill-sync .cognition/skills/skill-sync
# or
cp -r skill-sync .windsurf/skills/skill-sync

# Global
cp -r skill-sync ~/.config/cognition/skills/skill-sync
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r skill-sync .claude/skills/skill-sync

# Global
cp -r skill-sync ~/.claude/skills/skill-sync
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r skill-sync .cursor/skills/skill-sync
```

</details>

<details>
<summary>Codex</summary>

```bash
cat skill-sync/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
cat skill-sync/SKILL.md >> GEMINI.md
```

</details>

## Usage

```text
/skill-sync <source-path>                    # build new skill (claude default)
/skill-sync <source-path> <skill-name>       # sync existing skill
/skill-sync <source-path> --agent codex      # build via codex
/skill-sync <source-path> --agent devin --yolo  # build via devin, dangerous perms
```

Run from the root of your at-skills (or qr-skills) repo. The utility validates this and aborts with a clear error otherwise.

## License

MIT
