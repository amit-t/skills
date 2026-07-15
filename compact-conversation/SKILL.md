---
name: compact-conversation
description: Compact a long conversation into a saved progress summary — completed work, key decisions, current state, pending tasks — so a fresh session can pick up without losing context. Fires only as a fallback when the agent has no native /compact command; check for one first. Use when the user says "compact this conversation", "compact the context", "reduce context window", "summarize our progress", or "create a conversation summary".
---

# Compact Conversation Context

## When to Use

Use this skill only as a fallback for agents without a built-in compaction feature. Before proceeding, check whether the agent already offers `/compact` or another native context-management workflow (Claude Code and Aider both do) — if so, use that instead and stop here.

Reach for it when all of these hold:
- The agent has no native `/compact` (or equivalent) command
- The conversation has grown long (10+ messages)
- You are between tasks, not mid-debug or mid multi-step task

## Instructions

When this skill is invoked:

1. **Analyze Current Conversation**
   - Review all messages in the current conversation
   - Identify key decisions, code changes, and outcomes
   - Note any unresolved issues or pending tasks

2. **Create Compact Summary Document**
   - Create or update `.windsurf/conversation-summary.md` with:
     - **Project Context**: Brief description of what we're working on
     - **Completed Work**: Bulleted list of finished tasks and changes
     - **Key Decisions**: Important architectural or implementation choices
     - **Current State**: What's working, what's deployed, what's tested
     - **Pending Tasks**: What still needs to be done
     - **Important Notes**: Any critical context for future sessions

3. **Format Requirements**
   - Use concise bullet points, not paragraphs
   - Include absolute file paths with citations where relevant
   - Keep total summary under 500 lines
   - Use markdown headers for organization
   - Include a timestamp for when the summary was created

4. **After Creating Summary**
   - Inform the user that context has been compacted
   - Suggest they can start a new conversation and reference the summary
   - Provide the path to the summary file

## Example Output Structure

```markdown
# Conversation Summary
*Created: 2026-04-08 10:54 UTC+05:30*

## Project Context
- Working on [brief description]

## Completed Work
- **File**: `@/path/to/file.ts` - [what was done]
- **Feature**: [feature name] - [status]

## Key Decisions
- Chose [technology/approach] because [reason]

## Current State
- ✅ [what's working]
- ⚠️ [what needs attention]

## Pending Tasks
- [ ] [task 1]
- [ ] [task 2]

## Important Notes
- [critical context]
```

## Best Practices

- Include only what's needed in a future session — outcomes, not process or debugging blow-by-blow
- Update the existing summary rather than creating a duplicate
