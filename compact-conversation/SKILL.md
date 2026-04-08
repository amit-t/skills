# Compact Conversation Context

## Description
Compacts the current conversation by creating a concise summary and progress document, effectively reducing context window usage while preserving critical information.

**⚠️ IMPORTANT**: Most CLI agents (like Claude Code, Aider, etc.) have a built-in `/compact` command. **NEVER use this skill if the agent already has a native `/compact` command or workflow.** Always check for and prefer the agent's built-in compaction feature first.

## Trigger Phrases
- "compact this conversation"
- "compact the context"
- "reduce context window"
- "summarize our progress"
- "create a conversation summary"

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
   - Use concise bullet points (not paragraphs)
   - Include file paths with citations where relevant
   - Keep total summary under 500 lines
   - Use markdown headers for organization
   - Include timestamps for when summary was created

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
- Only include information that would be needed in future sessions
- Omit verbose explanations or intermediate debugging steps
- Focus on outcomes, not process
- Update existing summary rather than creating duplicates
- Use absolute file paths for all code references

## When NOT to Use
- **NEVER use if the agent has a built-in `/compact` command** (e.g., Claude Code CLI, Aider, etc.) - Always prefer the native command
- Don't compact if conversation is already short (<10 messages)
- Don't compact if actively debugging (preserve full context)
- Don't compact if user is in middle of complex multi-step task

## How to Check for Built-in Compact
Before using this skill, check if the agent supports:
- `/compact` command (most CLI agents)
- Native conversation compaction workflows
- Built-in context management tools

If any of these exist, inform the user to use the native feature instead and DO NOT proceed with this skill.
