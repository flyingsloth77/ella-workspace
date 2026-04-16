# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Current Known Setup

### Messaging
- Primary messaging surface: Telegram
- OpenClaw gateway on laptop: `ws://127.0.0.1:18789` (loopback, not reachable from VPS)
- OpenClaw gateway on VPS: separate instance, always-on, faces Telegram

### Two-Machine Architecture
- **VPS** = primary runtime (always-on, Telegram-facing, runs cron/heartbeat)
- **Laptop** = workbench (Claude Code runs here, git push → VPS Ella pulls and benefits)
- **Shared brain**: `https://github.com/flyingsloth77/ella-workspace` (git remote for both)
- **Sync mechanism**: `scripts/git_sync.py` — pull-then-push on every heartbeat

### Git / Sync — VERIFIED ✅
- Remote: `https://github.com/flyingsloth77/ella-workspace.git`
- Branch: `master`
- Credentials stored on VPS via `git config credential.helper store`
- Laptop: pushes freely (GitHub token in credential manager)
- VPS: pushes with stored token (in `~/.git-credentials` on VPS, set via `git config credential.helper store`)
- Auto-sync runs via HEARTBEAT.md on every heartbeat cycle

### Laptop as Helper Node (Current State)
- Laptop gateway is loopback-only — VPS cannot call it directly
- Current connection: git-based (laptop Claude Code → push → VPS Ella pulls on heartbeat)
- Future upgrade: enable Tailscale in openclaw.json (`tailscale.mode: "on"`) for real-time node triggers
- To do real-time: `openclaw.json` → `gateway.tailscale.mode: "on"` on both machines

### Atlas Wire (Content Engine Project)
- Atlas Wire files live in `Desktop/Openclaw/` (separate repo, NOT this workspace)
- `.gitignore` excludes all `atlas-wire-*.md` and `flipboard_*` patterns
- Ella can work on Atlas Wire tasks — just point Claude Code at `Desktop/Openclaw/`

## To Fill In
- `config/settings.yaml`: fill in `owner.name` and `telegram_chat_id`
- `USER.md`: fill in owner profile details
- SSH hosts and aliases (for VPS access shortcuts)
- Preferred TTS voice
- Device nicknames
