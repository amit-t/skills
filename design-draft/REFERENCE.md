# design-draft — Reference

Detail behind `SKILL.md`: the `--from` resume table and the `--list` status output.

---

## Resume and Status

### `--from` flag values

| Flag | Starts at |
|------|-----------|
| `--from interview` | Step 2 — Design Interview |
| `--from flow` | Step 3 — User Flow |
| `--from wireframes` | Step 4 — Wireframes |
| `--from system` | Step 5 — Design System |
| `--from screens` | Step 6 — Hi-Fi Screens |
| `--from review` | Step 7 — Design Review |
| `--from handoff` | Step 8 — Developer Handoff |
| `--from approve` | Step 9 — Approve and Publish |

### `--list` output

Show all approved PRDs and their design status:

```
Approved PRDs — Design Status

  PLAT-01  Authentication & Identity
           Brief ✓  Flow ✓  Wireframes ✓  Screens ✓ (8)  Review ✓  Handoff ✓
           Status: APPROVED — run uxd-approve.zsh to publish

  PLAT-02  Workspace & Team Management
           Brief ✗  Flow ✗  Wireframes ✗  Screens ✗  Review ✗  Handoff ✗
           Status: Not started — run /design-draft PLAT-02 to begin

  ...
```

Detection logic: check for files matching `*[FEATURE-ID]*` in each output folder.
