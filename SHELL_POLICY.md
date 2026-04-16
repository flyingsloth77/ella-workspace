# SHELL_POLICY.md — Ella's Shell Access Rules

> Read this before running any shell command. These rules are your operating boundary.

## Freely Allowed (no confirmation needed)

### Workspace file operations
- `rm`, `mv`, `cp` any file **inside** the workspace
- `ls`, `cat`, `head`, `tail`, `find`, `grep` inside the workspace
- `mkdir` inside the workspace

### Git (workspace repo only)
- `git status`
- `git diff`
- `git log`
- `git add -A`
- `git commit -m "..."`
- `git pull --rebase`
- `git branch`, `git remote -v`

### Workspace scripts
- `python scripts/daily_notes.py ...`
- `python scripts/task_manager.py ...`
- `python scripts/memory_manager.py ...`
- `python scripts/email_triage.py ...`
- `python scripts/git_sync.py sync`
- `python scripts/git_sync.py pull`

## Requires Confirmation (ask before running)

### Git push
- `git push` — always ask first, show what will be pushed

### System operations
- `systemctl`, `service` — any service changes
- `apt`, `pip install` — any package installation
- `crontab` — any cron changes

### External / network
- `curl`, `wget` to external URLs
- `ssh` to any host
- Any command that sends data outside the machine

### Destructive operations
- `rm -rf` on directories
- `git reset --hard`
- `git clean -f`
- Any command operating **outside** the workspace

## Never (don't even ask)

- Modifying system files (`/etc/`, `/boot/`, etc.)
- Changing user passwords or SSH keys
- Installing or removing system services
- Modifying firewall rules
- Accessing other users' home directories
- Running anything as root/sudo unless explicitly instructed

## Scope

The workspace is: `~/.openclaw/workspace/`
Everything above is scoped to this directory unless stated otherwise.
