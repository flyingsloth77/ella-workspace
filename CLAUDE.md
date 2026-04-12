# Openclaw -- Ella Chief of Staff System

This repository contains the configuration, scripts, templates, and memory for **Ella**, an AI chief of staff built on OpenClaw with Telegram integration.

## Architecture

```
Openclaw/
├── ELLA.md              # Ella's system prompt and personality
├── CLAUDE.md            # This file -- project guide for Claude Code
├── memory/
│   ├── MEMORY.md        # Long-term memory index (read on startup)
│   ├── owner.md         # Owner profile
│   ├── daily/           # Daily notes (YYYY-MM-DD.md)
│   ├── people/          # Per-person relationship profiles
│   ├── projects/        # Per-project tracking
│   └── kaizen/          # Kaizen research notes
├── scripts/
│   ├── daily_notes.py   # Daily note file management
│   ├── task_manager.py  # Task CRUD and sweep operations
│   ├── memory_manager.py# Person/project profile management
│   └── email_triage.py  # Email classification helpers
├── config/
│   ├── settings.yaml    # Main configuration
│   ├── triage_rules.yaml# Email triage rules
│   ├── research_tiers.yaml # Research source configuration
│   └── schedules.yaml   # Cron/scheduled task definitions
├── templates/
│   ├── morning_brief.md # Morning brief format
│   ├── evening_wrap.md  # Evening wrap format
│   ├── meeting_brief.md # Meeting prep brief format
│   ├── person_profile.md# New person profile template
│   ├── project_profile.md # New project profile template
│   ├── kaizen_research.md # Kaizen research format
│   └── research_digest.md # Weekly digest format
└── tasks/
    ├── active.md        # Active task list (source of truth)
    ├── completed.md     # Completed task archive
    └── delegated.md     # Tasks delegated to others
```

## Design Principles

1. **LLMs handle judgment, scripts handle everything else.** Anything deterministic (file I/O, API calls, timestamps) lives in Python. The LLM handles synthesis, prioritization, drafting.
2. **Flat markdown files.** Everything is human-readable, git-trackable, and editable. No databases.
3. **Silence is a feature.** Don't surface noise. If nothing needs attention, say nothing.
4. **Memory compounds.** Every interaction feeds back into the memory layer. The system gets richer over time.
5. **Kaizen.** The system improves itself weekly through structured review.

## Key Integrations

- **Telegram** -- primary messaging interface (via OpenClaw)
- **Google Calendar** -- via MCP tools (gcal_*)
- **Gmail** -- via MCP tools (gmail_*)
- **Python scripts** -- deterministic operations

## For Claude Code Instances

When working on this project:
- Read `ELLA.md` to understand Ella's personality and behavior rules
- Read `memory/MEMORY.md` for current state and context
- Read `config/settings.yaml` for configuration
- Use scripts in `scripts/` for deterministic operations
- Follow templates in `templates/` for output formatting
- Log changes to daily notes via `python scripts/daily_notes.py log "description"`
- Track tasks via `python scripts/task_manager.py`

## Getting Started

1. Fill in `config/settings.yaml` with your details (name, timezone, Telegram chat ID)
2. Fill in `memory/owner.md` with your profile
3. Configure `config/triage_rules.yaml` with your VIP senders and auto-archive patterns
4. Configure `config/research_tiers.yaml` with your tracked sources
5. Set up OpenClaw cron jobs per `config/schedules.yaml`
6. Start interacting -- Ella learns from every conversation
