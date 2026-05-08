---
name: ubiquitous-language
description: DEPRECATED. Superseded by /repo-context-scan (build domain context from a codebase scan) and /domain-grill (stress-test engineering artifacts against the resulting CONTEXT.md). Do not invoke. The replacement skills produce richer outputs (CONTEXT.md + ADRs + relationships + multi-context support) and split the build vs grill responsibilities cleanly. Use /repo-context-scan to build, /domain-grill for engineering artifacts, and /grill-me for PRDs or non-technical plans.
---

# ubiquitous-language (DEPRECATED)

This skill has been split into two replacement skills.

## What to use instead

| Want to... | Use |
|---|---|
| Build or refresh a domain glossary from the code itself | [`/repo-context-scan`](../repo-context-scan) |
| Stress-test an engineering artifact (eng spec, TDD, refactor plan, technical design) against the glossary | [`/domain-grill`](../domain-grill) |
| Stress-test a PRD or any non-technical plan | [`/grill-me`](../grill-me) |

## Why the split

The old skill conflated two responsibilities:

1. **Building** a domain glossary (passive scan of the codebase)
2. **Using** the glossary to challenge new work (active interview against an artifact)

These have different cadences (one-shot per repo vs per-feature), different ownership (autonomous vs interactive), and different scopes (writes `CONTEXT.md` vs reads it). Splitting them keeps each skill focused and lets them evolve without entangling the other.

The new pair also produces richer artifacts:

- `CONTEXT.md` (or `CONTEXT-MAP.md` for multi-context repos) instead of a flat `UBIQUITOUS_LANGUAGE.md`
- Seeded `docs/adr/` entries for visibly deliberate decisions
- Bounded-context awareness for monorepos and multi-domain codebases
- A clean separation between *what the domain is* (CONTEXT.md, owned by `/repo-context-scan`) and *how to challenge new work against it* (`/domain-grill`)

## Migration

If you previously ran `/ubiquitous-language` to build a glossary:

```
/repo-context-scan
```

If you previously used the same skill to challenge a draft against your domain language during eng work:

```
/domain-grill
```

If you used it during product or planning work that wasn't code-grounded:

```
/grill-me
```

## Status

This stub remains in the catalog as a redirect so existing references resolve. The original implementation is preserved in git history. New invocations should use the replacement skills above.
