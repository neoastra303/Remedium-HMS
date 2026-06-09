#!/usr/bin/env python3
"""
Auto-generate CHANGELOG.md from git log.

Usage:
    python scripts/update_changelog.py              # append new commits since last tag
    python scripts/update_changelog.py --full       # regenerate entire changelog from all commits
"""
import subprocess
import sys
import re
from datetime import datetime
from pathlib import Path

CHANGELOG = Path(__file__).parent.parent / "CHANGELOG.md"

# Conventional commit prefixes → changelog section mapping
SECTION_MAP = {
    "feat": "Added",
    "fix": "Fixed",
    "refactor": "Changed",
    "perf": "Changed",
    "chore": "Changed",
    "docs": "Changed",
    "test": "Changed",
    "ci": "Changed",
    "style": "Changed",
    "revert": "Removed",
}


def git(*args):
    result = subprocess.run(
        ["git"] + list(args), capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def get_commits_since(ref=None):
    """Return list of (hash, subject, date) tuples."""
    range_arg = f"{ref}..HEAD" if ref else "HEAD"
    log = git("log", range_arg, "--pretty=format:%H|%s|%ad", "--date=short")
    if not log:
        return []
    commits = []
    for line in log.splitlines():
        parts = line.split("|", 2)
        if len(parts) == 3:
            commits.append(tuple(parts))
    return commits


def get_latest_tag():
    try:
        return git("describe", "--tags", "--abbrev=0")
    except subprocess.CalledProcessError:
        return None


def parse_commit(subject):
    """Parse conventional commit subject into (type, scope, description)."""
    match = re.match(r"^(\w+)(?:\(([^)]+)\))?!?:\s*(.+)$", subject)
    if match:
        return match.group(1), match.group(2), match.group(3)
    return None, None, subject


def group_commits(commits):
    sections = {}
    for sha, subject, date in commits:
        ctype, scope, desc = parse_commit(subject)
        section = SECTION_MAP.get(ctype, "Changed")
        sections.setdefault(section, [])
        entry = f"- {desc}"
        if scope:
            entry = f"- **{scope}**: {desc}"
        entry += f" ([`{sha[:7]}`])"
        sections[section].append(entry)
    return sections


def format_version_block(version, date, sections):
    lines = [f"## [{version}] - {date}", ""]
    for section in ["Added", "Changed", "Fixed", "Removed"]:
        if section in sections:
            lines.append(f"### {section}")
            lines.extend(sections[section])
            lines.append("")
    return "\n".join(lines)


def update_changelog(full=False):
    latest_tag = get_latest_tag()
    ref = None if full else latest_tag

    commits = get_commits_since(ref)
    if not commits:
        print("No new commits since last tag. Changelog is up to date.")
        return

    sections = group_commits(commits)
    today = datetime.now().strftime("%Y-%m-%d")
    new_block = format_version_block("Unreleased", today, sections)

    if not CHANGELOG.exists():
        header = "# Changelog\n\nAll notable changes are documented here.\n\n---\n\n"
        CHANGELOG.write_text(header + new_block + "\n")
        print(f"Created {CHANGELOG}")
        return

    content = CHANGELOG.read_text(encoding="utf-8")

    # Replace existing [Unreleased] block or prepend after header
    if "## [Unreleased]" in content:
        # Find and replace the unreleased block
        pattern = r"## \[Unreleased\].*?(?=\n## \[|\Z)"
        replacement = new_block + "\n"
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    else:
        # Insert after the first --- separator
        insert_after = content.find("---\n")
        if insert_after != -1:
            pos = insert_after + 4
            content = content[:pos] + "\n" + new_block + "\n" + content[pos:]
        else:
            content = content + "\n" + new_block + "\n"

    CHANGELOG.write_text(content, encoding="utf-8")
    print(f"Updated {CHANGELOG} with {sum(len(v) for v in sections.values())} entries.")


if __name__ == "__main__":
    full = "--full" in sys.argv
    update_changelog(full=full)
