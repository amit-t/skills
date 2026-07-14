# Review Synthesis Template — Step 5

Disclosed reference for [`SKILL.md`](SKILL.md) — the literal template for `outputs/prds/[prd-name]-review-synthesis.md`, used at Step 5 once all 7 reviews are collected.

```markdown
---
prd: [PRD filename]
review_date: YYYY-MM-DD
stage: [Current PRD stage]
agents: [engineer, designer, executive, legal, uxr, skeptic, customer]
---

# PRD Review Synthesis: [PRD Title]

**Reviewed:** [Date]
**Current Stage:** [Stage]
**Reviewers:** Engineering, Design, Executive, Legal, UXR, Skeptic, Customer Voice

---

## TL;DR

**Overall Assessment:** [Ready to proceed / Needs minor fixes / Requires significant work / Not ready]

**Critical Blockers:** [X]
**Important Gaps:** [Y]
**Conflicting Perspectives:** [Z]

**Recommended Next Step:** [Specific action]

---

## Critical Blockers

[Must be addressed before moving to next stage]

### 1. [Blocker Title]

**Flagged by:** [Agent(s)]
**Issue:** [Description of the problem]
**Impact if not fixed:** [Consequence]
**Recommendation:** [Specific fix]
**Owner:** [Who should address this]

---

### 2. [Blocker Title]

[Same structure]

---

## Important Gaps

[Should be addressed before launch, may not block next stage]

### [Gap Category - e.g., "Missing Technical Specs"]

**Flagged by:** [Agent(s)]
**Gap:** [What's missing]
**Risk:** [What could go wrong]
**Recommendation:** [How to fill the gap]

---

## Enhancements to Consider

[Nice-to-haves that would strengthen the PRD or feature]

**From Engineering:**
- [Suggestion]
- [Suggestion]

**From Design:**
- [Suggestion]

**From Executive:**
- [Suggestion]

**From Legal:**
- [Suggestion]

**From UXR:**
- [Suggestion]

**From Skeptic:**
- [Challenging question or alternative]

**From Customer:**
- [User perspective suggestion]

---

## Conflicting Perspectives

[Where agents disagreed - requires PM judgment]

### Conflict 1: [Topic]

**Perspective A** ([Agent]):
- [Position]
- [Rationale]

**Perspective B** ([Agent]):
- [Opposite position]
- [Rationale]

**Decision needed:**
- [What the PM needs to decide]
- [Trade-offs to consider]
- [Recommendation if any]

---

## Detailed Feedback by Perspective

### Engineering Review

**✅ Strengths:**
- [What looks good technically]

**⚠️ Concerns:**
- [Technical concerns or gaps]

**❌ Blockers:**
- [Technical blockers]

**💡 Suggestions:**
- [Engineering improvements]

**Estimated Complexity:** [S/M/L/XL based on feedback]

---

### Design Review

**✅ Strengths:**
- [UX decisions that work well]

**⚠️ Concerns:**
- [Usability issues]

**❌ Blockers:**
- [UX blockers]

**💡 Suggestions:**
- [Design improvements]

**Usability Risk:** [Low/Medium/High]

---

### Executive Review

**✅ Strengths:**
- [Strategic alignment]

**⚠️ Concerns:**
- [Strategic questions]

**❌ Blockers:**
- [Strategic misalignment]

**💡 Suggestions:**
- [Strategic recommendations]

**Business Impact:** [High/Medium/Low]
**Strategic Fit:** [Strong/Moderate/Weak]

---

### Legal Review

**✅ Strengths:**
- [Legal considerations addressed]

**⚠️ Concerns:**
- [Legal/compliance gaps]

**❌ Blockers:**
- [Legal red flags]

**💡 Suggestions:**
- [Risk mitigation]

**Legal Risk:** [Low/Medium/High]
**Requires Legal Team Review:** [Yes/No]

---

### UX Research Review

**✅ Strengths:**
- [Research-backed decisions]

**⚠️ Concerns:**
- [Unvalidated assumptions]

**❌ Blockers:**
- [Contradicts research]

**💡 Suggestions:**
- [Research needed]

**Research Validation:** [Strong/Moderate/Weak]

---

### Skeptic Review

**🤔 Questions to Answer:**
- [Challenging questions]

**⚠️ Risky Assumptions:**
- [Assumptions that need validation]

**❌ Flawed Logic:**
- [Issues with reasoning]

**💡 Alternatives:**
- [Different approaches to consider]

---

### Customer Voice Review

**✅ User Value:**
- [What users will love]

**⚠️ User Friction:**
- [What might confuse or frustrate]

**❌ User Rejection:**
- [What users might hate]

**💡 Delight Opportunities:**
- [Ways to exceed expectations]

**User Sentiment:** [Would love it / Would use it / Might use it / Would avoid it]

---

## Action Items

**Before Next Review:**
- [ ] [Critical blocker 1] - Owner: [Name]
- [ ] [Critical blocker 2] - Owner: [Name]

**Before Launch:**
- [ ] [Important gap 1] - Owner: [Name]
- [ ] [Important gap 2] - Owner: [Name]

**Decisions Needed:**
- [ ] [Decision on conflict 1] - Owner: PM
- [ ] [Decision on conflict 2] - Owner: PM

---

## Next Steps

1. **Immediate:** [What to do right now]
2. **This week:** [What to tackle soon]
3. **Before next stage:** [What must be done]

**Recommended:**
- Run `/decision-doc` for conflicting perspectives
- Update PRD to address blockers
- Schedule follow-up review after fixes (if needed)

---

*Generated: [Timestamp]*
*Agents used: 7 (Engineering, Design, Executive, Legal, UXR, Skeptic, Customer)*
*Next: Update PRD → Re-review or proceed to next stage*
```
