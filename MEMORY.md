# Ella - Long-Term Memory Index

> This file is Ella's persistent memory. It is read on every startup to orient on what matters now.
> Each entry links to a detailed memory file. Keep this index under 200 lines.

## Owner Profile
- [Owner Profile](owner.md) -- Georgia; prefers concise, proactive communication and asks that I ask before risky actions

## Active Projects
- Atlas Wire materials are present in the workspace; active role/status not yet clarified

## Key People
- Georgia -- owner; timezone Europe/Brussels; pronouns she/her

## Active Decisions & Commitments
- Risk preference: ask before risky actions
- `config/settings.yaml` needs `owner.name` and `telegram_chat_id` filled in
- `USER.md` needs owner profile details filled in

## Lessons Learned
- Keep setup state explicit in files; do not assume shell-backed tasks completed if approval timed out
- Don't commit `.openclaw/workspace-state.json` — it's a runtime file that changes on every boot
- git stash → pull --rebase → stash pop → push is the safe sync pattern when both machines have changes

## System Notes — VERIFIED ✅ (as of 2026-04-16)
- Messaging platform: Telegram
- Brief style: concise, no fluff, lead with what matters
- Task management: `tasks/active.md` (source of truth), `tasks/completed.md`, `tasks/delegated.md`
- Calendar: Google Calendar via MCP (`gcal_*` tools)
- Email: Gmail via MCP (`gmail_*` tools)
- Git sync: VERIFIED working — `scripts/git_sync.py sync` pulls then pushes
- Remote: `https://github.com/flyingsloth77/ella-workspace.git` (master branch)
- VPS is primary runtime; laptop is workbench; git is the shared brain
- Shell policy: read `SHELL_POLICY.md` before any shell command
- Gateway auto-starts on Windows login via Startup folder shortcut
