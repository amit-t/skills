# two-axis-review

> Review the diff since a fixed point along two independent axes — repo coding standards and spec fidelity — via parallel sub-agents

**Category:** Engineering

Pins a fixed point (commit SHA, branch, tag, `HEAD~5`), takes the three-dot diff against the merge-base, then spawns two parallel sub-agents: **Standards** checks the diff against the repo's documented coding standards plus a fixed baseline of 12 Fowler code smells (_Refactoring_, ch.3), and **Spec** checks it against the originating issue / PRD for missing requirements, scope creep, and wrong implementations. The two reports are presented side by side, never merged or reranked — so code that follows every standard but implements the wrong thing (or vice versa) can't hide.

Ported from [`mattpocock/skills` → `engineering/code-review`](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md) and adapted to this catalog's conventions. Renamed to `two-axis-review` because this catalog already has a [`code-review`](../code-review) skill (interactive GitHub PR review with two-phase approval) — the two are complementary: use `two-axis-review` for a local standards + spec pass, `code-review` to post an approved GitHub Review.

## When to use

- "Review this branch since `main`"
- "Review since `HEAD~5`" / "review since <commit>"
- "Does this change match the issue / PRD?"
- "Two-axis review" — standards conformance and spec fidelity, side by side
- Pre-PR self-review of work-in-progress changes

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill two-axis-review
```

Install all skills from this repository:

```bash
npx skills@latest add amit-t/skills
```

### Manual Installation

<details>
<summary>Devin / Windsurf</summary>

```bash
# Project-level
cp -r two-axis-review .cognition/skills/two-axis-review
# or
cp -r two-axis-review .windsurf/skills/two-axis-review

# Global
cp -r two-axis-review ~/.config/cognition/skills/two-axis-review
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r two-axis-review .claude/skills/two-axis-review

# Global
cp -r two-axis-review ~/.claude/skills/two-axis-review
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r two-axis-review .cursor/skills/two-axis-review
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat two-axis-review/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat two-axis-review/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/two-axis-review main
/two-axis-review HEAD~5
/two-axis-review <commit-sha> docs/specs/feature.md
```

The skill validates the fixed point, locates the spec (commit-message issue refs → passed path → `docs/`/`specs/` match → ask), collects standards sources, runs both sub-agents in parallel, and reports `## Standards` and `## Spec` sections with a per-axis summary. See `SKILL.md` for the full workflow and the smell baseline.

## License

MIT
