# grill-me-auto

> Batch-mode `grill-me`: all questions in one collapsible markdown document, answered in one reply.

**Category:** Engineering

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill grill-me-auto
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
cp -r grill-me-auto .cognition/skills/grill-me-auto
# or
cp -r grill-me-auto .windsurf/skills/grill-me-auto

# Global
cp -r grill-me-auto ~/.config/cognition/skills/grill-me-auto
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r grill-me-auto .claude/skills/grill-me-auto

# Global
cp -r grill-me-auto ~/.claude/skills/grill-me-auto
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r grill-me-auto .cursor/skills/grill-me-auto
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat grill-me-auto/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat grill-me-auto/SKILL.md >> GEMINI.md
```

</details>

## Usage

Invoke with any of these forms:

```text
/grill-me-auto
/Grill Me Auto
/grill me auto
```

The skill first asks for depth (`quick` / `standard` / `deep`, default `deep`) unless you pre-select it:

```text
/grill-me-auto deep
/grill-me-auto standard
/grill-me-auto quick
```

Then it silently reads the relevant context and writes the full grill to:

```text
.grills/<YYYY-MM-DD-HHMM>-<slug>-<depth>.md
```

Open the file in a markdown previewer. Each numbered question is a collapsible `<details>` block with:

- why the question matters
- 2–4 labelled options (`1.A`, `1.B`, ...)
- the agent's recommendation
- an alt recommendation
- conditional sub-questions nested under their parent

## Answering

The document ends with three easy reply paths:

1. `accept all my recommendations`
2. `accept all my alt recommendations`
3. Copy/paste the filled answer-key block back into chat after reading it.

The uppercase aliases `ACCEPT_ALL_RECOMMENDATIONS` and `ACCEPT_ALL_ALT_RECOMMENDATIONS` also work.

Per-question answers look like this:

```text
1: A
2: rec
3: alt
4: B
```

`rec` means use the recommendation. `alt` means use the alt recommendation; if Alt is `n/a`, the agent falls back to the primary recommendation and tells you.

## Grill depth

| Depth | Aliases | What you get | Typical count |
| --- | --- | --- | --- |
| `deep` | `3`, `deepest` | Every branch, dependency, edge case, contradiction, code/doc cross-check, and invented boundary scenario. | 20–40+ |
| `standard` | `2`, `medium` | Critical assumptions, main edge cases, and obvious cross-checks. | 15–25 |
| `quick` | `1`, `sharp` | Highest-leverage deal-breakers and dead-on-arrival risks only. | 5–10 |

Depth changes how many branches the skill walks, not how sharp each question is.

## Document naming convention

Format: `.grills/<YYYY-MM-DD-HHMM>-<slug>-<depth>.md`

- `YYYY-MM-DD-HHMM` — local time. Same-minute collisions get `-2`, `-3`.
- `<slug>` — 2–3 word kebab-case derived from the topic being grilled.
- `<depth>` — `deep` / `standard` / `quick`.

Examples:

```text
.grills/2026-05-30-2114-auth-rewrite-deep.md
.grills/2026-05-31-0902-prd-pricing-standard.md
.grills/2026-05-31-1645-migration-rollback-quick.md
```

A filled example lives at [`templates/grill-doc.template.md`](./templates/grill-doc.template.md). Additional format rules live in [`REFERENCE.md`](./REFERENCE.md).

## When to use this vs `grill-me`

- **`grill-me`** — interactive, one question at a time.
- **`grill-me-auto`** — batch document, reviewed offline or in a browser/mobile preview, answered once.
- **`domain-grill`** — engineering-only stress-test against `CONTEXT.md` and ADRs; still interactive.

## Credits

Forked from [`grill-me`](../grill-me) in this repo, which is itself a fork of [`grill-me`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md) by [Matt Pocock](https://github.com/mattpocock) ([mattpocock/skills](https://github.com/mattpocock/skills)).

- Matt Pocock's original provides the relentless-interview core.
- The upstream `amit-t/skills` fork adds the `quick` / `standard` / `deep` depth selector.
- This fork adds batch document delivery: collapsible markdown, recommendations + alts, and one-shot answer parsing.

## License

MIT
