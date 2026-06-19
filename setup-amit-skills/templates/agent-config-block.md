# amit-t/skills conventions

Use this section when configuring a repo to consume skills from `amit-t/skills`.

## Agent instruction files

- Keep durable repo rules in `AGENTS.md` unless this repo has chosen another canonical agent file.
- If both `AGENTS.md` and `CLAUDE.md` exist, keep shared conventions identical or cross-link them.
- Preserve existing repo-specific rules; append this section instead of replacing user-authored guidance.

## Downstream skill expectations

- `/repo-context-scan` writes and updates `CONTEXT.md` or `CONTEXT-MAP.md` plus ADRs.
- `/domain-grill` reads `CONTEXT.md` / `CONTEXT-MAP.md` and existing ADRs before interviewing.
- `write-a-skill` expects each skill to have `SKILL.md` and `README.md`.
- `docs-from-prs` expects durable docs locations to be explicit in repo instructions.
