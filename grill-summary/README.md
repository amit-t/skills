# grill-summary

> Turn a written grill into a short, plain-English story: the bigger goal, why this
> decision matters, what you need to answer, and what your answers enable next.

**Category:** Engineering

## What It Does

- Summarises the current session's written grill, a supplied path, or pasted text.
- Groups unanswered questions into decision themes, preserving original question
  references, meaningful alternatives, and conditional follow-ups.
- Connects Wayfinder grills to the matching map's destination and relevant work
  before/after the current ticket. Marks missing or snapshot-only context honestly.
- Usually returns 120–200 words in chat. Settled answers stay out of your to-do list.
- Reads only: it never answers for you, edits the grill, updates tickets, records
  approval, or starts implementation.

Works with written output from `grill-me`, `grill-me-auto`, `domain-grill`, or an
equivalent decision review, including non-engineering topics. It does not generate
another grill. The original document remains the source for exact options and replies.

## Install as Agent Skill

```zsh
npx skills@latest add amit-t/skills --skill grill-summary
```

Install all skills from this repository:

```zsh
npx skills@latest add amit-t/skills
```

### Manual Installation

From a checkout containing this skill, copy the **whole directory** so the conditional
Wayfinder reference travels with it. Use the appropriate destination:

| Agent | Project directory | Global directory |
| --- | --- | --- |
| Devin / Windsurf | `.cognition/skills/` or `.windsurf/skills/` | `~/.config/cognition/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` | — |
| Codex | `.agents/skills/` | `~/.agents/skills/` |

For example, project-local Codex installation:

```zsh
mkdir -p .agents/skills
cp -R grill-summary .agents/skills/grill-summary
```

For an agent without skill-directory discovery, follow that agent's instruction-loading
mechanism and keep `SKILL.md` and `WAYFINDER.md` together. Do not copy only the entrypoint.

## Usage

```text
/grill-summary
/grill-summary .grills/import-rollout.md
Summarise the grill and explain where it fits in the Wayfinder map.
```

In Codex, explicitly mention `$grill-summary` with an optional path.

The skill also supports automatic selection after a grill is written or materially
updated in the current session. This is an agent instruction, **not a background file
watcher or guaranteed hook**: the host must discover and load the skill. No existing
grilling skills are changed. If your host does not select it automatically, invoke it
explicitly or add this instruction to your session:

> After writing or materially updating a grill, use grill-summary before asking me
> for answers. Keep the original workflow's answer instructions and approval gate.

No duplicate summaries for unchanged content unless requested. If the session has
multiple plausible grills, the agent asks which one rather than guessing by file age.
No map is required for a standalone grill; no GitHub tool is required for local text.

## Output and Verification

See the standalone example in [SKILL.md](./SKILL.md) and the map-context pattern in
[WAYFINDER.md](./WAYFINDER.md). The narrative is factual, not fictional; decision
bullets retain enough detail to help you answer rather than merely list topic names.

Repository checks: `zsh tests/grill-summary.test.zsh`. Behavioral scenarios and observed
results live under `tests/grill-summary/` in the repository, outside the installed skill.

## License

MIT
