"""
git_sync.py -- Auto-commit and push workspace changes to git.

Run this on a schedule (e.g., every 15 minutes) to keep the VPS
and laptop OpenClaw instances in sync via GitHub.

Usage:
    python scripts/git_sync.py push    # Commit local changes and push
    python scripts/git_sync.py pull    # Pull remote changes
    python scripts/git_sync.py sync    # Pull first, then push (safest)
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent


def run(cmd, cwd=None):
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True,
        cwd=cwd or WORKSPACE
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def has_changes():
    code, out, _ = run("git status --porcelain")
    return bool(out.strip())


def push():
    if not has_changes():
        print("No changes to push.")
        return True

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    run("git add -A")
    code, out, err = run(f'git commit -m "auto-sync: {timestamp}"')
    if code != 0:
        print(f"Commit failed: {err}")
        return False

    code, out, err = run("git push")
    if code != 0:
        print(f"Push failed: {err}")
        return False

    print(f"Pushed changes at {timestamp}")
    return True


def pull():
    code, out, err = run("git pull --rebase")
    if code != 0:
        print(f"Pull failed: {err}")
        # Try to recover
        run("git rebase --abort")
        return False
    print(f"Pulled: {out}")
    return True


def sync():
    """Pull remote changes, then push local changes."""
    if not pull():
        print("Pull failed, skipping push to avoid conflicts.")
        return False
    return push()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: git_sync.py [push|pull|sync]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "push":
        push()
    elif cmd == "pull":
        pull()
    elif cmd == "sync":
        sync()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
