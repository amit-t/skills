# Context Map

Use this when the repo has multiple bounded contexts with distinct vocabularies.

## Contexts

- [{Context Name}](./{path}/CONTEXT.md) — {one-sentence responsibility}
- [{Other Context}](./{other-path}/CONTEXT.md) — {one-sentence responsibility}

## Relationships

- **{Context A} → {Context B}**: {integration, event, API, or shared ID relationship}
- **{Context B} → {Context A}**: {reverse relationship, if any}

## Ownership notes

- `/repo-context-scan` owns updates to generated context files.
- `/domain-grill` consumes context files read-only and flags new terms for a later scan.
