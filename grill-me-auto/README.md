# grill-me-auto

> Same coverage as `grill-me`, but every question is written to one collapsible markdown document — answer in one batch instead of turn-by-turn.

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

Once installed, invoke in your agent session:

```
/grill-me-auto
```

The agent:

1. Asks for grill depth (`quick` / `standard` / `deep`, default `deep`).
2. Silently reads the codebase, `CLAUDE.md`, `CONTEXT.md`, ADRs, memory — everything an interactive grill would interview you about and could just look up itself.
3. Writes the full grill document to `.grills/<YYYY-MM-DD-HHMM>-<slug>-<depth>.md` at the project root.
4. Tells you the path and stops.

You open the doc in a markdown previewer (GitHub, GitLab, VS Code, Obsidian, anywhere `<details>` blocks render), expand each question, read the options + agent recommendation + alt recommendation, and reply in one shot with **one of three batch shortcuts**.

### Grill depth

| Depth | Aliases | What you get | Typical question count |
| --- | --- | --- | --- |
| `deep` | `3`, `deepest` | Every branch of the decision tree, critical + edge + corner cases, cross-references against code, invented boundary scenarios. | 20–40+ |
| `standard` | `2`, `medium` | Critical assumptions + main edge cases + obvious cross-references. Skip exotic corner cases. | 15–25 |
| `quick` | `1`, `sharp` | Top highest-leverage hard-hitters only. Deal-breaker assumptions and dead-on-arrival risks. | 5–10 |

Pre-select to skip the prompt:

```
/grill-me-auto deep        # default
/grill-me-auto standard
/grill-me-auto quick
```

Depth never lowers rigor on the questions you *do* get — it changes how many branches the skill walks, not how sharp each question is.

### Document layout

Every question is a collapsible `<details>` block:

```markdown
<details>
<summary><strong>3. Migration strategy for in-flight sessions?</strong></summary>

- **Why it matters:** Cutover that invalidates live sessions = pageable incident.
- **Options:**
  - **3.A** — Dual-write old + new, dual-read on verify, flip after 24h, drop old after 7d.
  - **3.B** — Hard cutover; all users re-login.
  - **3.C** — Long-tail expiry — old sessions die over their existing 90d TTL.
- **Recommendation:** **A** — preserves UX, clean rollback window, bounded dual-read overhead.
- **Alt:** **C** — defensible if the team wants zero migration code and is OK with a 90-day tail.

</details>
```

Conditional sub-questions nest inside their parent's block and are tagged `Conditional on: <expr>` — they only need answering if the parent answer triggers them.

A full filled example lives at [`templates/grill-doc.template.md`](./templates/grill-doc.template.md).

### Replying to the grill

The doc ends with an **Answer key** section. Pick one of three:

**1. Accept all agent recommendations:**

```
ACCEPT_ALL_RECOMMENDATIONS
```

**2. Accept all alt recommendations:**

```
ACCEPT_ALL_ALT_RECOMMENDATIONS
```

(Where Alt is `n/a`, the agent falls back to the recommendation and tells you.)

**3. Answer per question** — copy the answer-key block, fill in option letters. Mix and match with `rec` and `alt` if you want most defaults but a few overrides:

```
1: A
2: rec
3: alt
4: A
5: B
6: rec
```

Paste your chosen block back into chat. The agent applies all answers in one pass, summarises the resolved plan in ≤10 bullets, and flags anything where your answers changed direction from your original prompt.

## When to use this vs `grill-me`

- **`grill-me`** — interactive, one question at a time. Right when you and the agent are discovering the plan together.
- **`grill-me-auto`** — batch document. Right when you already know roughly what you think, want to see the full surface in writing, review in a browser preview or on mobile away from the agent, and reply once.
- **`domain-grill`** — engineering-only, stress-test against `CONTEXT.md` and ADRs. Still interactive.

## Document naming convention

Format: `.grills/<YYYY-MM-DD-HHMM>-<slug>-<depth>.md`

- `YYYY-MM-DD-HHMM` — local time. Same minute collisions get `-2`, `-3`.
- `<slug>` — 2–3 word kebab-case derived from the topic being grilled.
- `<depth>` — `deep` / `standard` / `quick`.

Examples:

```
.grills/2026-05-30-2114-auth-rewrite-deep.md
.grills/2026-05-31-0902-prd-pricing-standard.md
.grills/2026-05-31-1645-migration-rollback-quick.md
```

The `.grills/` directory is added to `.gitignore` on first run so grill docs stay out of source control. The skill stages the `.gitignore` change but does not commit on your behalf.

## Credits

Forked from [`grill-me`](../grill-me) in this repo, which is itself a fork of [`grill-me`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md) by [Matt Pocock](https://github.com/mattpocock) ([mattpocock/skills](https://github.com/mattpocock/skills)).

- The relentless-interview core is Matt's original.
- The `quick` / `standard` / `deep` depth selector is the upstream `amit-t/skills` fork.
- This fork adds the batch document delivery mode (collapsible markdown grill doc, three-way answer-key shortcuts, one-pass apply).

## License

MIT
