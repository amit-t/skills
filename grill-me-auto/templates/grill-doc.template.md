---
created_at: 2026-05-30T21:14:00+05:30
depth: deep
topic: Rewrite the auth middleware to remove session-token storage
status: open
total_questions: 6
answer_key_marker: "## Answer key"
shortcuts:
  accept_all_recommendations: "accept all my recommendations"
  accept_all_recommendations_alias: "ACCEPT_ALL_RECOMMENDATIONS"
  accept_all_alt_recommendations: "accept all my alt recommendations"
  accept_all_alt_recommendations_alias: "ACCEPT_ALL_ALT_RECOMMENDATIONS"
  per_question_format: "<question_number>: <option_letter|rec|alt>"
---

# Grill: Rewrite the auth middleware to remove session-token storage

> Depth: **deep** · Generated 2026-05-30 21:14 · 6 questions
>
> **How to use this doc:** Read each question. Each has 2–4 options labelled `A` / `B` / `C` / `D`, an agent **Recommendation**, and an **Alt** recommendation. Pick an option per question in the **Answer key** at the bottom, or paste one of the two batch shortcuts and stop there. Reply in chat — the agent will apply your answers in one pass.

## Questions

1. **What is the failure mode that legal flagged?**
2. **Where will session state live after the rewrite?**
3. **Migration strategy for in-flight sessions?**
4. **Rollback story if the new path misbehaves in production?**
5. **Backwards-compat window for old SDK clients?**
6. **Who owns the runbook for the new auth path?**

---

<details>
<summary><strong>1. What is the failure mode that legal flagged?</strong></summary>

- **Why it matters:** If the scope is misread you either over-engineer (rewrite cookie + body + header paths when only cookies were flagged) or under-fix (skip server-side log redaction and ship the same bug).
- **Options:**
  - **1.A** — Tokens persisted in the session DB beyond the legally permitted retention window.
  - **1.B** — Tokens written to access logs in plaintext.
  - **1.C** — Both A and B.
- **Recommendation:** **C** — both surfaces appear in the legal memo (`docs/legal/2026-04-sessions.md`, §2 and §4); fixing only one leaves the other failing the same audit.
- **Alt:** **A** — if the legal memo was actually about retention only, log redaction is already covered by the platform logging policy and doesn't need to be in this rewrite's scope.

</details>

<details>
<summary><strong>2. Where will session state live after the rewrite?</strong></summary>

- **Why it matters:** This is the architectural pivot; everything else (migration, rollback, SDK compat) hangs off it.
- **Options:**
  - **2.A** — Stateless JWT in an HTTP-only cookie, signed with a rotating KMS key.
  - **2.B** — Server-side session ID in Redis with a 15-minute TTL; no token leaves the server.
  - **2.C** — Hybrid — JWT for identity, Redis for revocation list.
- **Recommendation:** **B** — matches CONTEXT.md's "no tokens at rest in primary store" decision (ADR-0014) and lets logout actually invalidate, which JWT-only can't without a denylist.
- **Alt:** **C** — if the team wants the latency win from stateless verification but is willing to run a revocation cache. More moving parts but defensible.

  <details>
  <summary><strong>2a. Redis deployment topology? <em>(conditional on 2 = B or 2 = C)</em></strong></summary>

  - **Conditional on:** `2 in {B, C}`
  - **Why it matters:** A single-node Redis is the implicit SPOF for the whole auth path.
  - **Options:**
    - **2a.A** — Existing platform Redis cluster (multi-AZ, shared).
    - **2a.B** — Dedicated Redis cluster for auth only.
  - **Recommendation:** **A** — the shared cluster already has the operational maturity (HA, monitoring, on-call runbook). Carving a dedicated cluster trades that for an unowned new component.
  - **Alt:** **B** — defensible only if auth-side traffic would noisy-neighbor the rest of the platform. Confirm with capacity team before choosing.

  </details>

</details>

<details>
<summary><strong>3. Migration strategy for in-flight sessions?</strong></summary>

- **Why it matters:** Cutover that invalidates live sessions = mass forced re-login = pageable incident.
- **Options:**
  - **3.A** — Dual-write old + new on issue, dual-read on verify, flip read source after 24h, drop old after 7d.
  - **3.B** — Hard cutover at deploy time; all users re-login.
  - **3.C** — Long-tail expiry — issue new sessions on the new path; let old sessions expire naturally over their existing TTL (90 days).
- **Recommendation:** **A** — preserves user experience, gives a clean rollback window, and the dual-read overhead is bounded.
- **Alt:** **C** — defensible if the team wants zero migration code and is OK with the rewrite being incomplete for 90 days.

</details>

<details>
<summary><strong>4. Rollback story if the new path misbehaves in production?</strong></summary>

- **Why it matters:** "Just revert" is not a plan if the migration has already started writing to the new store.
- **Options:**
  - **4.A** — Feature flag at the verify path; flip back to old store on incident.
  - **4.B** — Forward-fix only; the new store is the source of truth from cutover.
- **Recommendation:** **A** — feature flag is cheap during the dual-write window (option 3.A); ripping it out after the 7-day drop is fine.
- **Alt:** **B** — only defensible if 3 = B (hard cutover) and the team is OK with the operational risk.

</details>

<details>
<summary><strong>5. Backwards-compat window for old SDK clients?</strong></summary>

- **Why it matters:** Pinned SDK versions in the wild will keep sending the old token shape. Window length drives how much shim code lives in production and for how long.
- **Options:**
  - **5.A** — 30 days; aggressive deprecation, force-bump SDKs.
  - **5.B** — 90 days; matches the longest existing session TTL.
  - **5.C** — 12 months; matches the platform SDK support policy.
- **Recommendation:** **B** — aligns with option 3.A's drop date for old sessions; no clients should still be on the old shape after 90 days.
- **Alt:** **C** — defensible if SDK adoption metrics show >5% on pre-rewrite versions at the 90-day mark.

</details>

<details>
<summary><strong>6. Who owns the runbook for the new auth path?</strong></summary>

- **Why it matters:** Unowned runbooks rot; on-call gets paged for the new path with no playbook.
- **Options:**
  - **6.A** — Platform-auth team (current owner of the old path).
  - **6.B** — Identity team (owns CONTEXT.md ADR-0014).
- **Recommendation:** **A** — they already own the deploy, the metrics dashboard, and the existing on-call rotation. Identity team consults on the spec but doesn't take pager duty.
- **Alt:** **B** — defensible if the rewrite is significant enough that ownership should follow the new design rather than the old runbook.

</details>

---

## Answer key

Pick exactly one of three ways to reply. Paste the chosen block back into chat verbatim.

### Option 1 — Accept all my recommendations

```
accept all my recommendations
```

Alias:

```
ACCEPT_ALL_RECOMMENDATIONS
```

### Option 2 — Accept all my alt recommendations

```
accept all my alt recommendations
```

Alias:

```
ACCEPT_ALL_ALT_RECOMMENDATIONS
```

For any question where Alt is `n/a`, the agent will fall back to the primary recommendation and flag it in the summary.

### Option 3 — Copy/paste this in the chat after reading it back to the agent

Replace each `?` with the option letter you want. One question per line. Conditional sub-questions are only required if their parent answer triggers them.

```
1: ?
2: ?
3: ?
4: ?
5: ?
6: ?
```

You can mix and match: copy this block, fill the ones you have opinions on, and write `rec` (use the recommendation) or `alt` (use the alt) for the rest. Example: `5: rec`, `2: alt`, `4: A`.
