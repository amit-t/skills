---
name: leadership-update
description: Reformat a status update so leadership remembers you positively. Turn raw notes into outcome-first, three-sentence updates with a clear ask. Use when the user wants to give an update to a manager, exec, or stakeholder, mentions a "status update", "leadership update", "exec update", or pastes raw notes about what they've been working on.
---

# /leadership-update — Outcome-First Status Updates

Turn the user's raw notes into an exec-ready update that makes them remembered, not forgotten.

This skill is based on the framework from Yasar Ahmad's reel (https://www.instagram.com/p/DVtAWlpjU67/): leaders don't remember data — they remember clarity. An update is three things in this order: **outcome → reasoning → next**, finished with **what you need from them**.

## Core principles (do not violate)

1. **Lead with the outcome, not the activity.**
   - Right: "We're on track to cut client onboarding from 14 → 7 days."
   - Wrong: "We've been working on the new client process for three weeks."
2. **Three sentences.** Status. Reasoning. Next step + timeline.
   - Pattern: *"Here's where we are. Here's what informed that. Here's what happens next."*
3. **Blockers come with options, not just problems.**
   - Pattern: *"Hit a blocker on X. Two options: A or B. Leaning A because of Y. Need your input?"*
4. **End with the ask.** Make the leader's role obvious in one line.
   - "Nothing needed — just keeping you informed." OR
   - "I need a decision on X by Thursday to stay on track."
5. **Cut everything else.** No process narration, no apologies, no padding.

## Invocation behavior — auto-detect

When invoked, decide between **reformat-mode** and **interview-mode** based on what the user has already provided.

**Reformat-mode** (default when context is rich): if the user has given enough to fill in status, reasoning, next step, and ask — reformat directly. Don't ask questions.

**Interview-mode** (when notes are thin): if any of the four required slots is missing, ask 1–3 short questions, one at a time, to fill the gaps. Stop asking the moment you have enough. Never ask more than 3.

Required slots:
- **Status / outcome** — where things stand, framed as a result
- **Reasoning** — what informed that status (data, trade-off, decision)
- **Next** — what happens next, with a timeline
- **Ask** — what you need from the leader (or explicit "nothing")

If the user mentions a blocker, also ask for **options** + **lean** — never surface a problem without proposed paths.

## Output format selection

After (or alongside) the auto-detect step, ask the user once:

> "Default output is **verbal/standup script**. Want a different format — Slack/chat, email, or a written status doc block?"

If they say verbal/default, produce just the verbal version. Otherwise produce whichever they pick (one or many). Format specs below.

### 1. Verbal / standup version (default)

A short spoken script the user can read in a 1:1, standup, or hallway check-in. 3–5 sentences. No bullets. No headers. Sounds like talking, not reading.

```
We're on track to cut onboarding from 14 to 7 days. Vendor A beat the others on speed and cost by 30%, so we're moving forward with them. Contract goes out Friday. Need a decision from you on the budget cap by Thursday.
```

### 2. Slack/chat-ready short version

3–5 sentence post optimized for a DM to a manager or exec. Plain text, one paragraph or short stacked lines. No markdown headers. No emoji unless the user uses them. Bold the ask line if formatting is supported.

```
On track to cut onboarding from 14 → 7 days.
Vendor A won on speed + cost (30% better). Contract out Friday.
**Need your sign-off on the budget cap by Thursday.**
```

### 3. Email version

Subject line + body. Body still respects three-sentence structure but can include one supporting line per section if context demands. Ask line is the last sentence. No long sign-off.

```
Subject: Onboarding redesign — on track, need budget call by Thursday

Quick update on the onboarding redesign:

We're on track to cut client onboarding from 14 days to 7. Vendor A came out 30% ahead of the alternatives on speed and cost, so we're moving forward with them — contract goes out Friday.

I need a decision on the budget cap by Thursday to keep the timeline.

— [Name]
```

### 4. Written status doc section

A drop-in block for a weekly update doc. Allowed to use bullets here (the only format that does). Structure:

```
**[Project / Workstream]** — On track
- Status: cutting onboarding from 14 → 7 days, on track for end of month
- What informed it: Vendor A beat the field on speed + cost by 30%
- Next: contract out Friday, kickoff the following Monday
- Ask: decision on budget cap by Thursday
```

## Anti-patterns to refuse

When you see these in the user's raw notes, rewrite them — don't preserve them.

- **Activity dumps.** "I worked on X, then Y, then Z" → collapse to the outcome.
- **Unstructured blockers.** "Stuck on X" → demand options before producing the update.
- **Vague timelines.** "Soon", "later this week" → push for a specific day.
- **Hedging openers.** "Just wanted to share…", "Apologies for the delay…" → delete.
- **Process narration.** "We had a meeting where we discussed…" → cut, keep the decision.
- **Buried asks.** Ask must be the last line, stated directly.

## Edge cases

- **No ask exists.** Use the explicit "Nothing needed — just keeping you informed" line. Don't invent an ask.
- **Multiple workstreams.** Produce one block per workstream; don't merge. Headline the most important first.
- **Bad news.** Lead with the outcome anyway ("We're going to miss the Friday deadline by 3 days"), then reasoning, then the recovery plan as the "next", then the ask. No softening.
- **Pure FYI.** Still use the three-sentence structure. End with "Nothing needed — FYI."

## Quality bar before delivering

Self-check the draft against:
- [ ] First sentence states an outcome, not an activity
- [ ] Three sentences (or three lines, if formatted) cover status / reasoning / next
- [ ] Last line is a clear ask or an explicit "nothing needed"
- [ ] No filler: no apologies, no process narration, no hedges
- [ ] If a blocker exists: options + lean are present

If any box is unchecked, rewrite before showing the user.

## Source

Framework derived from Yasar Ahmad (Leadership Coach, @yasarahmad_), Instagram reel: https://www.instagram.com/p/DVtAWlpjU67/
