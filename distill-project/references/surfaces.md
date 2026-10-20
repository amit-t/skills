# Where the sources and the two files live, by surface

Go by the tools you actually have. Tool names change; match by what a tool does.

Source notes are dated 2026-10-19. Verify the actual fields and tools available at runtime.

## claude.ai Projects (web, desktop, mobile)

- Chats: search or page through project history only if the current surface exposes that access. Search by output titles and topic nouns. If history is unavailable, ask for an export and record the gap.
- Docs: read the project files you can access. Do not assume a project-specific read or write tool exists.
- Memory: account-level and project memory files, if a memory tool exists.
- Outputs: list and read artifacts with available tools or files. Read comments if exposed. Do not assume an account-wide artifact listing exists.
- Destination: save both files as project docs (for example `project-instructions.md` and `project-context.md`) where a write tool exists. Otherwise provide the files for the user to attach. Tell the user to paste the short rules file into project instructions if that field cannot be edited.

## Cowork (Claude desktop agent mode)

- Check available artifact, chat, and memory access rather than assuming the web and desktop tools match. Report Cowork sessions you cannot access from the current project.
- Local folders may hold outputs and notes. Check connected folders before concluding something does not exist.
- Destination: project docs if a project is attached; otherwise files in the working folder the user names.
- Cowork account skill sync is independent of `~/.claude/skills`; use the account Skills interface or upload flow.

## Claude Code (terminal)

- Chats: use readable local session history when available. Otherwise use git history (`git log`, commit messages, PR descriptions), existing `CLAUDE.md`, `.claude/` settings and commands, and notes folders as the record of decisions.
- Personal skills: `~/.claude/skills/<name>/SKILL.md` loads in local terminal sessions from any folder. Cowork and cloud sessions do not read that directory; enable an account skill for those surfaces.
- Outputs: the files in the repo. Generated docs, HTML pages, decks and style files carry the conventions.
- Destination: `CLAUDE.md` at the repo root for the rules (keep it short, link to the context file), and a context file such as `docs/project-context.md`. If `AGENTS.md` exists or other agents use the repo, put the rules there and have `CLAUDE.md` import or point to it so there is one source of truth.

## Codex and other terminal agents

- Same as Claude Code. Codex user skills live in `~/.agents/skills/<name>/SKILL.md`; global instructions are in `$CODEX_HOME/AGENTS.md` (default `~/.codex/AGENTS.md`). Repo `AGENTS.md` files apply from root to working directory; nearer files take precedence.
- Keep the instructions file plain markdown with no tool-specific syntax so any agent can read it.

## ChatGPT Projects

- Chats: ChatGPT can reference chat history inside a project when that setting is on, but there may be no tool to page through it. If the agent cannot read past chats, ask the user to paste or export the key ones, or work from project files and outputs alone and say so.
- Destination: the project's Instructions field (the rules) and an uploaded project file (the context). The project-instruction limit is not publicly documented as of 2026-10-19; verify the actual field before pasting. The 5,000-character paid global custom-instructions limit is not a project limit. Eligible ChatGPT workspaces offer Skills > Create > Upload from your computer. The portable skill archive is a ZIP containing one top-level skill folder with `SKILL.md`; uploading a skill is separate from adding project files.

## When the surface is unclear

Ask one question: where should the two files live? Offer the likely options from what you can see.

## Documentation checked on 2026-10-19

- Claude Code personal and account skill locations: https://code.claude.com/docs/en/skills
- Claude account skill upload: https://support.claude.com/en/articles/12512180-use-skills-in-claude
- Codex skill and `AGENTS.md` discovery: https://developers.openai.com/codex/skills and https://developers.openai.com/codex/guides/agents-md
- ChatGPT project files, history and instructions: https://help.openai.com/en/articles/10169521
- ChatGPT skill availability and upload: https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- OpenAI skill ZIP layout: https://developers.openai.com/api/docs/guides/tools-skills
