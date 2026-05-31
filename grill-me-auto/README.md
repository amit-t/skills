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

Open the file in a markdown previewer. Each numbered question is a collapsible `<details>` block carrying the question, *why it matters*, labelled options, the agent's recommendation, and an alt. See [`REFERENCE.md`](./REFERENCE.md#question-block-contract) for the exact block contract and [`templates/grill-doc.template.md`](./templates/grill-doc.template.md) for a filled example.

## Answering

The document ends with three reply paths (canonical phrasing on the left, uppercase alias on the right):

1. `accept all my recommendations` — alias `ACCEPT_ALL_RECOMMENDATIONS`
2. `accept all my alt recommendations` — alias `ACCEPT_ALL_ALT_RECOMMENDATIONS`
3. Filled per-question answer-key block — one `N: <A|B|C|D|rec|alt>` line per question; mix-and-match.

If Alt is `n/a`, option 2 (and the `alt` token) falls back to the primary recommendation and the summary flags it. Full parsing rules and resolved-answer format in [`REFERENCE.md` § Reply parsing contract](./REFERENCE.md#reply-parsing-contract).

## Grill depth

| Depth | Aliases | What you get | Typical count |
| --- | --- | --- | --- |
| `deep` | `3`, `deepest` | Every branch, dependency, edge case, contradiction, code/doc cross-check, and invented boundary scenario. | 20–40+ |
| `standard` | `2`, `medium` | Critical assumptions, main edge cases, and obvious cross-checks. | 15–25 |
| `quick` | `1`, `sharp` | Highest-leverage deal-breakers and dead-on-arrival risks only. | 5–10 |

Depth changes how many branches the skill walks, not how sharp each question is.

## Document naming convention

`.grills/<YYYY-MM-DD-HHMM>-<slug>-<depth>.md` — local time, 2–3 word kebab-case slug, depth `deep` / `standard` / `quick`. Same-minute collisions get `-2`, `-3`.

```text
.grills/2026-05-30-2114-auth-rewrite-deep.md
.grills/2026-05-31-0902-prd-pricing-standard.md
.grills/2026-05-31-1645-migration-rollback-quick.md
```

Exact path rules: [`REFERENCE.md` § File contract](./REFERENCE.md#file-contract). Filled example: [`templates/grill-doc.template.md`](./templates/grill-doc.template.md).

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
