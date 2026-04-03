# package-scout

> Research, compare, and select the best packages before installing any dependency

**Category:** Engineering

## What It Does

Forces the AI agent to research and compare package alternatives before installing any npm/pnpm/yarn dependency. Instead of blindly running `npm install`, the agent:

1. Clarifies what problem the package solves and any constraints
2. Searches the web for viable candidates (3-5 alternatives)
3. Compares them on stars, downloads, bundle size, vulnerabilities, maintenance activity, and TypeScript support
4. Presents a comparison table so the user can make an informed choice
5. Resolves the latest stable version via web search (never from stale training data)
6. Installs with the correct package manager and version

### When It Triggers

- Scaffolding a new project
- Adding a dependency or devDependency during development
- User asks to install, add, or pick a package
- Choosing between competing libraries

## Install

```bash
npx skills@latest add amit-t/skills --skill package-scout
```

### Manual Installation

<details>
<summary>Devin / Windsurf</summary>

```bash
# Project-level
cp -r package-scout .cognition/skills/package-scout
# or
cp -r package-scout .windsurf/skills/package-scout

# Global
cp -r package-scout ~/.config/cognition/skills/package-scout
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r package-scout .claude/skills/package-scout

# Global
cp -r package-scout ~/.claude/skills/package-scout
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r package-scout .cursor/skills/package-scout
```

</details>

<details>
<summary>Codex</summary>

```bash
cat package-scout/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
cat package-scout/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```text
/package-scout
```

Or simply ask the agent to add a dependency — the skill activates automatically when the agent needs to install a package.

## License

MIT
