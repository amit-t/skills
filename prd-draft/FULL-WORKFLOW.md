# Full PRD Workflow — 7-Step Process

Disclosed reference for [`SKILL.md`](SKILL.md) — the longer, cross-functional PRD process (context gathering, section-by-section enhancement, human review gates, announce template). Reached from the "How It Works" step for PRDs that need the full formal process instead of the 3-step conversational default.

For comprehensive end-to-end PRD creation, follow this 7-step process.

## Step-by-Step Workflow

### Workflow Step 1: Gather Context (10 min)

Before touching AI, collect:

**Research & Data:**
- User research findings (interviews, surveys)
- Analytics data (usage patterns, metrics)
- Support tickets (common issues, requests)
- Competitive analysis

**Strategic Context:**
- How this ladders to OKRs
- Business case (revenue/user impact)
- Strategic importance (why now?)

**Technical Context:**
- Existing architecture constraints
- Integration requirements
- Known dependencies

### Workflow Step 2: Generate First Draft (5 min)

Use the conversational workflow in Step 1-3 above to generate your first draft.

### Workflow Step 3: Enhance Each Section (30-60 min)

**Problem Statement:**
- [ ] Add specific customer quotes
- [ ] Include quantitative data
- [ ] Connect to company strategy

**Solution:**
- [ ] Explain WHY this solution
- [ ] Detail alternatives considered
- [ ] Call out tradeoffs made

**Success Metrics:**
- [ ] Define leading AND lagging indicators
- [ ] Set specific targets
- [ ] Define success criteria

### Workflow Step 4: Multi-Perspective Review (15 min)

Use the multi-agent review in Step 3 above to get feedback from:
- Engineering (feasibility)
- Design (UX)
- Executive (strategy)
- Customer voice (user needs)

### Workflow Step 5: Human Review

**Must review with:**
- Engineering lead
- Design lead
- Your manager

**Should review with:**
- Key stakeholders
- PM peers

### Workflow Step 6: Refine & Ship (30 min)

**Final checklist:**
- [ ] Can someone unfamiliar understand it?
- [ ] All sections complete
- [ ] Dependencies identified
- [ ] Success criteria clear
- [ ] Next steps defined

### Workflow Step 7: Announce

```
Hi team,

I've published the PRD for [Feature Name]: [link]

TL;DR: [One sentence]
Why now: [Strategic rationale]
Timeline: [When we plan to start/ship]

Action needed:
- Engineering: Review technical approach by [date]
- Design: Review UX approach by [date]

Questions? Drop them in [Slack channel].
```
