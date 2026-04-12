"""
daily_notes.py -- Deterministic script for managing daily note files.

Creates today's note file if it doesn't exist.
Appends structured entries to the daily note.
Called by Ella throughout the day to log events.

Usage:
    python scripts/daily_notes.py init          # Create today's file
    python scripts/daily_notes.py log "entry"   # Append a timestamped entry
    python scripts/daily_notes.py read [date]   # Read a day's notes (default: today)
"""

import sys
from datetime import datetime, date
from pathlib import Path

MEMORY_DIR = Path(__file__).parent.parent / "memory" / "daily"


def get_filepath(target_date: str = None) -> Path:
    if target_date:
        return MEMORY_DIR / f"{target_date}.md"
    return MEMORY_DIR / f"{date.today().isoformat()}.md"


def init_daily_note():
    filepath = get_filepath()
    if filepath.exists():
        print(f"Already exists: {filepath}")
        return

    today = date.today()
    content = f"""# Daily Notes -- {today.strftime('%A, %B %d, %Y')}

## Meetings

## Tasks Completed

## Tasks Added

## Decisions Made

## Context & Notes

## Communications
"""
    filepath.write_text(content, encoding="utf-8")
    print(f"Created: {filepath}")


def log_entry(entry: str):
    filepath = get_filepath()
    if not filepath.exists():
        init_daily_note()

    timestamp = datetime.now().strftime("%H:%M")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"\n- [{timestamp}] {entry}\n")
    print(f"Logged to {filepath}")


def read_notes(target_date: str = None):
    filepath = get_filepath(target_date)
    if not filepath.exists():
        print(f"No notes for {target_date or date.today().isoformat()}")
        return
    print(filepath.read_text(encoding="utf-8"))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: daily_notes.py [init|log|read] [args]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "init":
        init_daily_note()
    elif cmd == "log":
        if len(sys.argv) < 3:
            print("Usage: daily_notes.py log 'entry text'")
            sys.exit(1)
        log_entry(" ".join(sys.argv[2:]))
    elif cmd == "read":
        target = sys.argv[2] if len(sys.argv) > 2 else None
        read_notes(target)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
