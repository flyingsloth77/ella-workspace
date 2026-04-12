"""
task_manager.py -- Deterministic task tracking in markdown.

Manages tasks/active.md as the source of truth.
Handles adding, completing, listing, and sweeping tasks.

Usage:
    python scripts/task_manager.py add "task" --priority high --due 2026-04-15
    python scripts/task_manager.py complete <task_id>
    python scripts/task_manager.py list [--overdue] [--due-today] [--stale DAYS]
    python scripts/task_manager.py sweep
"""

import sys
import re
import argparse
from datetime import date, timedelta
from datetime import datetime
from pathlib import Path

TASKS_DIR = Path(__file__).parent.parent / "tasks"
ACTIVE_FILE = TASKS_DIR / "active.md"
COMPLETED_FILE = TASKS_DIR / "completed.md"
DELEGATED_FILE = TASKS_DIR / "delegated.md"


def ensure_files():
    for f, header in [
        (ACTIVE_FILE, "# Active Tasks\n\n"),
        (COMPLETED_FILE, "# Completed Tasks\n\n"),
        (DELEGATED_FILE, "# Delegated Tasks\n\n"),
    ]:
        if not f.exists():
            f.write_text(header, encoding="utf-8")


def generate_id():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def add_task(description, priority="medium", due_date=None, project=None, delegated_to=None):
    ensure_files()
    task_id = generate_id()
    today = date.today().isoformat()

    entry = f"- [ ] **[{task_id}]** {description}\n"
    entry += f"  - Priority: {priority} | Added: {today}"
    if due_date:
        entry += f" | Due: {due_date}"
    if project:
        entry += f" | Project: {project}"
    if delegated_to:
        entry += f" | Delegated to: {delegated_to}"
    entry += "\n"

    target = DELEGATED_FILE if delegated_to else ACTIVE_FILE
    with open(target, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"Added task {task_id}: {description}")


def complete_task(task_id):
    ensure_files()
    content = ACTIVE_FILE.read_text(encoding="utf-8")
    lines = content.split("\n")
    task_lines = []
    found = False
    remaining = []
    i = 0

    while i < len(lines):
        if f"[{task_id}]" in lines[i]:
            found = True
            task_lines.append(lines[i].replace("- [ ]", "- [x]"))
            i += 1
            while i < len(lines) and lines[i].startswith("  "):
                task_lines.append(lines[i])
                i += 1
        else:
            remaining.append(lines[i])
            i += 1

    if not found:
        print(f"Task {task_id} not found")
        return

    ACTIVE_FILE.write_text("\n".join(remaining), encoding="utf-8")
    with open(COMPLETED_FILE, "a", encoding="utf-8") as f:
        for line in task_lines:
            f.write(line + "\n")
        f.write(f"  - Completed: {date.today().isoformat()}\n")
    print(f"Completed task {task_id}")


def sweep():
    ensure_files()
    content = ACTIVE_FILE.read_text(encoding="utf-8")
    today = date.today()
    tomorrow = today + timedelta(days=1)

    overdue, due_soon, stale = [], [], []

    for line in content.split("\n"):
        if not line.startswith("- [ ]"):
            continue
        due_match = re.search(r"Due: (\d{4}-\d{2}-\d{2})", line)
        added_match = re.search(r"Added: (\d{4}-\d{2}-\d{2})", line)

        if due_match:
            d = date.fromisoformat(due_match.group(1))
            if d < today:
                overdue.append(line)
            elif d == tomorrow:
                due_soon.append(line)
        elif added_match:
            a = date.fromisoformat(added_match.group(1))
            if (today - a).days >= 5:
                stale.append(line)

    if overdue:
        print("OVERDUE:")
        for t in overdue:
            print(f"  {t}")
    if due_soon:
        print("\nDUE TOMORROW:")
        for t in due_soon:
            print(f"  {t}")
    if stale:
        print("\nSTALE (>5 days, no due date):")
        for t in stale:
            print(f"  {t}")
    if not overdue and not due_soon and not stale:
        print("All clear.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")

    add_p = sub.add_parser("add")
    add_p.add_argument("description")
    add_p.add_argument("--priority", default="medium")
    add_p.add_argument("--due")
    add_p.add_argument("--project")
    add_p.add_argument("--delegated-to")

    comp_p = sub.add_parser("complete")
    comp_p.add_argument("task_id")

    sub.add_parser("list")
    sub.add_parser("sweep")

    args = parser.parse_args()
    if args.command == "add":
        add_task(args.description, args.priority, args.due, args.project, getattr(args, "delegated_to", None))
    elif args.command == "complete":
        complete_task(args.task_id)
    elif args.command == "sweep":
        sweep()
    else:
        parser.print_help()
