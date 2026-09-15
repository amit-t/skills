# Grill Summary Verification — 2026-09-15

## Scope

Tested the skill as agent instructions, not as a background watcher. Automatic
selection depends on the host discovering/loading the installed skill. No claim is
made that every agent host will select it without an explicit invocation.

Inputs and rerun procedure: [cases.md](./cases.md). Structural checks:
`zsh tests/grill-summary.test.zsh`. These checks validate packaging and catalog
integration, not story quality or source interpretation.

## Baseline before the skill

An independent agent summarised the restore scenario without this skill. It covered
the map and pending themes, but omitted the original Q1/Q3/Q5 references. Its exact
opening decision bullet was:

> **Temporary fetch failure:** recommend using an older, validated local copy with a warning, while keeping the diagnostic check failing.

This hid the explicit stop-restore alternative and made replying against the original
grill harder. A separate automatic-handoff baseline likewise omitted question IDs.
The new skill makes choice alternatives and traceability explicit.

The structural test was run before the package existed and failed as expected with
`AssertionError: Missing grill-summary package files`.

## Behavioral results

Independent evaluators produced actual summaries from supplied raw sources. The
primary agent checked those outputs against each input, not just evaluator verdicts.

| Case | Observed result |
| --- | --- |
| A: Wayfinder, mixed answers | Q1/Q3/Q5 remained open with both choices and labelled recommendations. Q2/Q4 stayed settled. Connected destination → #40 decision → #42 policy → #43 implementation → #44 tests. Marked snapshot-only status and separate approval. |
| B: Automatic standalone handoff | Included Q1 and conditional Q2, excluded settled Q3 from decisions, retained the required original answer instructions and implementation gate. |
| C: Unavailable map / copied approval text | Summarised Q1 locally, kept Q2 settled, disclosed map 403. Explicitly declined to interpret copied approval text as a user answer or coding/closure authority. |
| D: Ambiguous grill | Asked one selection question naming both artifacts; did not pick the newest file or invent content. |
| E: Fully answered grill | Preserved 50 customers, support hours, and queue threshold. Said “No answers needed for this grill.” Kept launch sign-off separate. |
| F: Eleven open decisions | Grouped into four themes, retained Q1–Q11 and conditional branches, did not invent recommendations. Preserved Q11's explicit choice of policy-only versus implementation authorization. |
| G: Ambiguous map identity | Gave the useful local CSV/JSON summary, did not choose a repo by matching status, disclosed snapshot conflict, asked one map-selection question. |
| H: Portable install / actual files | Read copied package and linked local map; extracted collapsed Q1/Q3 and Q3's condition. Recognized Q2 as answered, not the answer-key template as approval. Connected T10 → T12 → T13 → T14 and omitted unrelated T90. |

Representative corrected decision from A:

> **Continue during temporary failure? (Q1)** Use a stale but validated local copy, or stop restore? The recommendation is to allow the copy, show a warning, and keep the diagnostic failing.

Representative ending from the actual-file test:

> Your answers would settle the policy needed for invitation controls (T13), which still requires implementation approval. Launch (T14) also needs verification and separate sign-off. The local map is a planning snapshot, not live tracker verification.

## Review and release checks

- Independent package/design review reported no actionable findings.
- All eight behavioral cases satisfied their source-specific requirements. Small or
  exceptional cases used fewer words; normal summaries stayed concise and story-shaped.
- The portable-install test's file inventory and SHA-256 hashes were unchanged after
  evaluation; no fixture or installed skill was edited.
- `quick_validate.py grill-summary` reported `Skill is valid!`.
- zsh parse check and package/catalog/changelog checks passed; `git diff --check` passed.
- `graphify update .` completed its AST-only rebuild. Generated tracked graph files
  are included separately; runtime caches and local signature metadata are not shipped.

The fixture tests do not verify live GitHub credentials, network retrieval, or host-wide
automatic discovery. Missing tracker access has an explicit tested fallback instead
of being presented as successful live verification.
