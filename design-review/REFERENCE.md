# design-review — Reference

Detail behind `SKILL.md`: the exact final review output template.

---

## Review Output Format

```markdown
# Design Review: [Screen Name]
**Date:** [date]
**Brief reference:** [brief filename]

---

## 1. UX Researcher Review

### ✅ What Works
[Specific positive observations]

### ⚠️ UX Concerns
1. **[Concern]** — [Severity: High/Medium/Low]
   [Specific description + why it's a problem]
   Fix: [Specific recommendation]

2. **[Concern]** — [Severity]
   ...

### 💡 Suggestions
- [Actionable suggestion]
- [Actionable suggestion]

### ❓ Validate With Users
- [Question to test in research]

---

## 2. Accessibility Audit

### ✅ Passes
- [WCAG criterion]: [observation]

### ❌ Failures
1. **[Criterion 1.4.3 — Contrast]** — CRITICAL
   Element: [description]
   Current ratio: [x:1] | Required: 4.5:1
   Fix: Change `[current color]` to `[recommended color]`

### 💡 Fixes
```css
/* Fix 1 */
.element { color: #[fix]; }
```

---

## 3. Engineer Review

### ✅ Easy to Implement
[Components that map cleanly to existing patterns]

### ⚠️ Concerns
1. **[Issue]** — [Effort: S/M/L/XL]
   [Description]
   Alternative: [simpler approach]

### 💡 Suggestions
- [Technical suggestion]

---

## 4. Brand Review

### ✅ On-Brand
[What aligns with brand guidelines]

### ⚠️ Deviations
1. **[Deviation]**
   Current: [what's there]
   Brand spec: [what it should be]
   Fix: [specific change]

---

## 5. End User Voice

> "My first reaction: [1-2 sentences as the user]"

😍 **Love:** [What they love]
😕 **Confusing:** [What confuses them]
🤔 **Questions:** [What they're uncertain about]
💬 **Would tell a friend:** "[quote]"

---

## Synthesis

### All 5 Reviewers Agree
[Common feedback points — highest priority to fix]

### Conflicting Perspectives
[Where reviewers disagree, and the trade-off]

### Priority Fix List
1. 🔴 **Critical:** [Fix 1 — must fix before showing stakeholders]
2. 🟡 **High:** [Fix 2]
3. 🟡 **High:** [Fix 3]
4. 🟢 **Nice to have:** [Fix 4]

---

## Recommended Actions
- **Fix now:** [Specific list with implementation notes]
- **Validate with users:** [Questions for research]
- **Defer to v2:** [Items that are improvements but not blockers]
```
