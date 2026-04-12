# HEARTBEAT.md - Ella's Periodic Checks

On each heartbeat, work through this checklist. Skip items checked recently (track in memory/heartbeat-state.json).

## Checks (rotate through, 2-4x per day)

1. **Email triage** — Check Gmail for unread. Classify using scripts/email_triage.py logic. Surface act_now items immediately. Batch act_today for next report.
2. **Calendar lookahead** — Any meetings in the next 2 hours? If external meeting in next 60 min, send meeting prep brief (see templates/meeting_brief.md).
3. **Task sweep** — Run `python scripts/task_manager.py sweep`. Flag anything overdue or stale.
4. **Commitment check** — Scan memory/people/ for overdue commitments from others.

## Scheduled outputs

- **09:00** — Send morning brief (templates/morning_brief.md)
- **18:00** — Send evening wrap (templates/evening_wrap.md)

## When to reach out

- Important email from a VIP (see config/triage_rules.yaml)
- Calendar event coming up (<60 min) that needs prep
- Overdue task or commitment that's been sitting >2 days
- Something genuinely interesting found during research

## When to stay quiet (HEARTBEAT_OK)

- Late night (23:00-08:00) unless urgent
- Human is clearly busy or hasn't responded to last message
- Nothing new since last check
- You just checked <30 minutes ago

## Background work (do silently)

- Update memory files
- Log to daily notes (python scripts/daily_notes.py log "...")
- Organize and clean memory
- **Git sync** — Run `python scripts/git_sync.py sync` on EVERY heartbeat. This keeps laptop and VPS in sync. Do this FIRST before other checks so you have latest state, and LAST after any changes.
