# ubiquitous-language (DEPRECATED)

> **This skill is deprecated.** It has been split into [`/repo-context-scan`](../repo-context-scan) (build domain context from a codebase) and [`/domain-grill`](../domain-grill) (stress-test engineering artifacts against it). For PRDs or non-technical plans, use [`/grill-me`](../grill-me).

**Category:** Engineering (deprecated)

## What to use instead

| Want to... | Use |
|---|---|
| Build or refresh a domain glossary from the code itself | `/repo-context-scan` |
| Stress-test an engineering artifact (eng spec, TDD, refactor plan, technical design) against the glossary | `/domain-grill` |
| Stress-test a PRD or any non-technical plan | `/grill-me` |

## Why this skill is deprecated

The original skill conflated two responsibilities — building a glossary (passive scan) and using it to challenge new work (active interview). Splitting them produced richer outputs (`CONTEXT.md`, ADRs, multi-context support) and clearer ownership (one skill writes, the other reads).

The original SKILL.md is preserved in git history if you need to reference it.

## License

MIT
