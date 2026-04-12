"""
memory_manager.py -- Manage person and project profiles.

Creates and updates structured markdown profiles from templates.
Deterministic file operations; LLM handles content generation.

Usage:
    python scripts/memory_manager.py person create "John Smith" --role "CEO" --org "Acme"
    python scripts/memory_manager.py person log "John Smith" "2026-04-12" "Meeting" "Discussed terms"
    python scripts/memory_manager.py person list
    python scripts/memory_manager.py project create "Alpha" --priority high
    python scripts/memory_manager.py project list
"""

import re
import argparse
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
PEOPLE_DIR = BASE_DIR / "memory" / "people"
PROJECTS_DIR = BASE_DIR / "memory" / "projects"
TEMPLATES_DIR = BASE_DIR / "templates"


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def create_person(name, role="", org="", relationship="", email=""):
    slug = slugify(name)
    filepath = PEOPLE_DIR / f"{slug}.md"
    if filepath.exists():
        print(f"Already exists: {filepath}")
        return

    content = TEMPLATES_DIR.joinpath("person_profile.md").read_text(encoding="utf-8")
    for old, new in {
        "{Full Name}": name,
        "{Job Title}": role or "TBD",
        "{Organization}": org or "TBD",
        "{e.g., LP prospect, portfolio founder, board member, collaborator}": relationship or "TBD",
        "{email}": email or "TBD",
        "{YYYY-MM-DD}": date.today().isoformat(),
        "{what's next with this person}": "TBD",
    }.items():
        content = content.replace(old, new)

    filepath.write_text(content, encoding="utf-8")
    print(f"Created: {filepath}")


def log_interaction(name, interaction_date, interaction_type, summary):
    slug = slugify(name)
    filepath = PEOPLE_DIR / f"{slug}.md"
    if not filepath.exists():
        print(f"No profile for {name}. Create first.")
        return

    content = filepath.read_text(encoding="utf-8")
    entry = (
        f"\n### {interaction_date} -- {interaction_type}\n"
        f"- **Summary:** {summary}\n"
        f"- **They committed to:** TBD\n"
        f"- **We committed to:** TBD\n"
    )

    marker = "## Interaction History"
    if marker in content:
        idx = content.index(marker) + len(marker)
        rest = content[idx:]
        # Skip comment lines
        insert_pos = 0
        for i, line in enumerate(rest.split("\n")):
            if line.strip().startswith("<!--") or line.strip() == "":
                insert_pos = i + 1
            else:
                break
        lines = rest.split("\n")
        lines.insert(insert_pos, entry)
        content = content[:idx] + "\n".join(lines)

    content = re.sub(r"last_touchpoint: .*", f"last_touchpoint: {interaction_date}", content)
    filepath.write_text(content, encoding="utf-8")
    print(f"Logged interaction for {name}")


def list_people():
    for f in sorted(PEOPLE_DIR.glob("*.md")):
        content = f.read_text(encoding="utf-8")
        nm = re.search(r"^name: (.+)$", content, re.MULTILINE)
        rl = re.search(r"^role: (.+)$", content, re.MULTILINE)
        lt = re.search(r"^last_touchpoint: (.+)$", content, re.MULTILINE)
        print(f"  {nm.group(1) if nm else f.stem} | {rl.group(1) if rl else '?'} | Last: {lt.group(1) if lt else '?'}")


def create_project(name, priority="medium", target="", owner=""):
    slug = slugify(name)
    filepath = PROJECTS_DIR / f"{slug}.md"
    if filepath.exists():
        print(f"Already exists: {filepath}")
        return

    content = TEMPLATES_DIR.joinpath("project_profile.md").read_text(encoding="utf-8")
    for old, new in {
        "{Project Name}": name,
        "{active|paused|completed}": "active",
        "{high|medium|low}": priority,
        "{who's responsible}": owner or "TBD",
        "{YYYY-MM-DD}": date.today().isoformat(),
        "{YYYY-MM-DD or ongoing}": target or "ongoing",
    }.items():
        content = content.replace(old, new)

    filepath.write_text(content, encoding="utf-8")
    print(f"Created: {filepath}")


def list_projects():
    for f in sorted(PROJECTS_DIR.glob("*.md")):
        content = f.read_text(encoding="utf-8")
        nm = re.search(r"^name: (.+)$", content, re.MULTILINE)
        st = re.search(r"^status: (.+)$", content, re.MULTILINE)
        print(f"  {nm.group(1) if nm else f.stem} | {st.group(1) if st else '?'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="entity")

    pp = sub.add_parser("person")
    psub = pp.add_subparsers(dest="action")
    pc = psub.add_parser("create")
    pc.add_argument("name")
    pc.add_argument("--role", default="")
    pc.add_argument("--org", default="")
    pc.add_argument("--relationship", default="")
    pc.add_argument("--email", default="")
    pl = psub.add_parser("log")
    pl.add_argument("name"); pl.add_argument("date"); pl.add_argument("type"); pl.add_argument("summary")
    psub.add_parser("list")

    prp = sub.add_parser("project")
    prsub = prp.add_subparsers(dest="action")
    prc = prsub.add_parser("create")
    prc.add_argument("name")
    prc.add_argument("--priority", default="medium")
    prc.add_argument("--target", default="")
    prc.add_argument("--owner", default="")
    prsub.add_parser("list")

    args = parser.parse_args()
    if args.entity == "person":
        if args.action == "create":
            create_person(args.name, args.role, args.org, args.relationship, args.email)
        elif args.action == "log":
            log_interaction(args.name, args.date, args.type, args.summary)
        elif args.action == "list":
            list_people()
    elif args.entity == "project":
        if args.action == "create":
            create_project(args.name, args.priority, args.target, getattr(args, "owner", ""))
        elif args.action == "list":
            list_projects()
    else:
        parser.print_help()
