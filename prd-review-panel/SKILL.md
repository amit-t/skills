---
name: prd-review-panel
description: Run a 7-perspective multi-agent PRD review (Engineering, Design, Executive, Legal, UXR, Skeptic, Customer Voice) that catches gaps and surfaces conflicts before stakeholder review. Use when the user wants a PRD reviewed, asks for panel or multi-agent feedback, or runs /prd-review-panel.
---

## Purpose

Runs the 7 reviewers in parallel and explicitly challenges assumptions, not just gaps and conflicts.

## Usage

- `/prd-review-panel` - Review a PRD with all 7 sub-agents
- `/prd-review-panel [prd-name]` - Review specific PRD
- `/prd-review-panel --perspectives "eng,design,exec"` - Review with subset of agents

---

## Context Routing

**Check these files first:**
1. `outputs/prds/` - Active PRDs to review
2. `context-library/prds/` - Reference PRDs and past reviews
3. `sub-agents/` - The 7 reviewer personas
4. `context-library/strategy/` - Strategic context for executive review
5. `context-library/research/` - User research for UXR validation

**Sub-agents available:**
1. **engineer-reviewer.md** - Technical feasibility, complexity, dependencies
2. **designer-reviewer.md** - UX/UI feedback, user experience
3. **executive-reviewer.md** - Strategic alignment, business impact
4. **legal-advisor.md** - Compliance, risk, regulatory concerns
5. **uxr-analyst.md** - User research synthesis, validation
6. **skeptic.md** - Devil's advocate, challenge assumptions
7. **customer-voice.md** - Simulate user perspective

---

## Workflow

### Step 1: PRD Selection

1. **If user specified PRD name:**
   - Look for it in `outputs/prds/` and `context-library/prds/`
   - If found: Proceed
   - If not found: List available PRDs, ask user to choose

2. **If no PRD specified:**
   - Scan `outputs/prds/` for recent PRDs (modified in last 30 days)
   - List them with:
     - File name
     - Title (from content)
     - Last modified date
     - Current stage (if indicated)
   - Prompt: "Which PRD do you want to review?"

3. **Read the full PRD:**
   - Load complete content
   - Note the current stage (Team Kickoff / Planning Review / XFN Kickoff / Solution Review / Launch Readiness)
   - Identify sections present (some PRDs may be incomplete)

---

### Step 2: Review Preparation

**Extract key elements from PRD:**
- **Problem statement** - What user pain are we solving?
- **Hypothesis** - If we build X, then Y will happen because Z
- **Strategic fit** - Why this vs other things?
- **Non-goals** - What's explicitly out of scope?
- **Success metrics** - How we measure success
- **Rollout plan** - A/B test or full launch?
- **Technical approach** - How we'll build it (if specified)
- **UX design** - Mockups, flows, behavior examples
- **Stakeholders** - Who needs to approve/support
- **Risks** - Known concerns or open questions

**Determine review focus based on stage:**

- **Team Kickoff stage:** Focus on problem definition, strategic fit
- **Planning Review stage:** Focus on scope, estimates, prioritization
- **XFN Kickoff stage:** Focus on cross-functional alignment, dependencies
- **Solution Review stage:** Focus on technical approach, UX design, edge cases
- **Launch Readiness stage:** Focus on rollout plan, metrics, compliance

---

### Step 3: Spawn 7 Sub-Agents in Parallel

**CRITICAL: Use single message with multiple Task tool calls for parallel execution.**

For each sub-agent, create a Task using its prompt from [REVIEWER-PROMPTS.md](REVIEWER-PROMPTS.md), with the full PRD text substituted in.

---

### Step 4: Collect & Synthesize Reviews

Once all 7 agents complete (wait for all Task outputs):

**Read each review and extract:**
1. ✅ Strengths (what's working well)
2. ⚠️ Concerns or gaps (important but not blocking)
3. ❌ Blockers (must fix before proceeding)
4. 💡 Suggestions (improvements to consider)

**Identify patterns:**
- **Convergent feedback:** Multiple agents flagging same issue (high priority)
- **Conflicting perspectives:** Agents disagree (requires PM judgment)
- **Blind spots:** Issue only one agent caught (could be critical)

**Categorize all feedback:**

**Critical Blockers** (Must fix before next stage):
- [Issue from Agent X]
- [Issue from Agent Y]
- **Why critical:** [Impact if not addressed]

**Important Gaps** (Address before launch):
- [Gap from Agent X]
- [Gap from Agent Y]
- **Why important:** [Risk or limitation]

**Enhancements** (Consider for v1 or v2):
- [Suggestion from Agent X]
- [Suggestion from Agent Y]
- **Value if added:** [Benefit]

**Conflicting Perspectives** (Requires decision):
- **Agent X says:** [Position]
- **Agent Y says:** [Opposite position]
- **PM decision needed:** [What to prioritize]

---

### Step 5: Generate Review Synthesis

Create file: `outputs/prds/[prd-name]-review-synthesis.md` using the template in [SYNTHESIS-TEMPLATE.md](SYNTHESIS-TEMPLATE.md), with every placeholder filled in.

---

### Step 6: Output & Next Actions

1. **Save review synthesis file**

2. **Display summary:**
   ```
   7-agent review complete for [PRD]!

   ✅ Strong areas: [X]
   ⚠️ Critical blockers: [Y]
   💡 Key recommendations: [Z]

   Overall: [Ready to proceed / Needs work]
   ```

3. **Offer next steps:**
   - If blockers exist: "Want me to help update the PRD to address blockers?"
   - If conflicts exist: "Run `/decision-doc` to document the [Conflict] decision?"
   - If ready: "PRD looks solid! Ready for stakeholder review."
   - Always: "Review synthesis saved to [file path]"

---

## Tips for Best Results

**When to run:**
- After completing first draft (Team Kickoff stage)
- Before stakeholder review (catch gaps privately first)
- After major changes (validate new approach)
- Before committing to build (final gate)

**How to use the output:**
- Fix blockers before proceeding
- Discuss conflicts in next stakeholder meeting
- Park enhancements for v2 (don't let perfect kill good)
- Use as peer review before formal review

**Common patterns:**
- Engineering often conflicts with Design (speed vs polish)
- Executive often conflicts with Customer (business vs user needs)
- Legal often blocks what users want (compliance vs freedom)
- **Your job as PM:** Make the call, document the trade-off

---

## Related Skills

**Before this:**
- `/prd-draft` - Create the PRD
- `/user-interview` / `/user-research-synthesis` - Validate with research
- `/impact-sizing` - Quantify value

**After this:**
- `/decision-doc` - Document key decisions
- `/prd-draft` - Update PRD based on feedback
- `/prototype` - Build based on feedback
- `/launch-checklist` - Prepare for launch

**Complements:**
- `/competitor-analysis` - Inform strategic review
- `/stakeholder-update` - Share review results

**Iterative use:** Run review at each PRD stage (Team Kickoff, Planning, Solution, Launch) — each pass focuses on stage-appropriate concerns.

---

## Output Quality Self-Check

Before presenting output to the PM, verify:

- [ ] **All requested reviewer perspectives included:** The synthesis contains feedback from all 7 sub-agents (or all specifically requested agents), each with their own dedicated section
- [ ] **Each reviewer has specific, actionable feedback:** Every reviewer section contains at least one concrete, actionable item (not generic praise like "looks good" or vague concerns like "needs more detail")
- [ ] **Conflicting perspectives between reviewers explicitly flagged:** Any disagreements between agents (e.g., Engineering wants simplicity while Design wants richness) are called out in the "Conflicting Perspectives" section with both positions stated
- [ ] **Synthesis section prioritizes feedback items:** The TL;DR and summary sections rank issues by severity (Critical Blockers > Important Gaps > Enhancements) with a clear recommended next step
- [ ] **Feedback references specific PRD sections:** Each piece of feedback points to the exact section, requirement, or design element it applies to (e.g., "the rollout plan in Section 5" not "the rollout approach")
