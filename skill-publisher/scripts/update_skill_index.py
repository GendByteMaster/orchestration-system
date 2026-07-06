#!/usr/bin/env python3
"""Generate SKILLS.md from local Codex skill roots."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SkillRoot:
    label: str
    path: Path


@dataclass(frozen=True)
class SkillEntry:
    name: str
    description: str
    source: str
    relative_path: str


def default_roots(repo_root: Path) -> list[SkillRoot]:
    home = Path.home()
    return [
        SkillRoot("repository", repo_root),
        SkillRoot("codex-skills", home / ".codex" / "skills"),
        SkillRoot("agents-skills", home / ".agents" / "skills"),
        SkillRoot("plugin-cache", home / ".codex" / "plugins" / "cache"),
        SkillRoot(
            "understand-anything",
            home / ".understand-anything" / "repo" / "understand-anything-plugin" / "skills",
        ),
    ]


def parse_frontmatter(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return "", ""
    try:
        end = text.index("\n---", 4)
    except ValueError:
        return "", ""

    name = ""
    description = ""
    pending_description = False
    description_lines: list[str] = []

    for raw_line in text[4:end].splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if pending_description:
            if line.startswith(" ") or line.startswith("\t") or stripped.startswith("-"):
                cleaned = stripped.strip('"').strip("'")
                if cleaned and cleaned not in {">-", "|"}:
                    description_lines.append(cleaned)
                continue
            pending_description = False

        if stripped.startswith("name:"):
            name = stripped.split(":", 1)[1].strip().strip('"').strip("'")
        elif stripped.startswith("description:"):
            value = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            if value in {">-", "|"}:
                pending_description = True
                description_lines = []
            else:
                description = value

    if not description and description_lines:
        description = " ".join(description_lines)
    return name, " ".join(description.split())


def collect_entries(roots: list[SkillRoot]) -> list[SkillEntry]:
    entries: list[SkillEntry] = []
    seen: set[tuple[str, str, str]] = set()

    for root in roots:
        if not root.path.exists():
            continue
        for skill_file in sorted(root.path.rglob("SKILL.md")):
            if ".git" in skill_file.parts:
                continue
            name, description = parse_frontmatter(skill_file)
            if not name:
                continue
            relative_path = skill_file.relative_to(root.path).as_posix()
            key = (name.lower(), root.label, relative_path.lower())
            if key in seen:
                continue
            seen.add(key)
            entries.append(
                SkillEntry(
                    name=name,
                    description=description or "No description found.",
                    source=root.label,
                    relative_path=relative_path,
                )
            )

    return sorted(entries, key=lambda item: (item.name.lower(), item.source, item.relative_path.lower()))


def markdown_table(entries: list[SkillEntry]) -> str:
    lines = [
        "# Skills Catalog",
        "",
        "Generated from local `SKILL.md` frontmatter. Paths are normalized by source root so the catalog can be published without local absolute paths.",
        "",
        "## Repository Skills",
        "",
    ]

    repo_skill_names = sorted({entry.name for entry in entries if entry.source == "repository"}, key=str.lower)
    for name in repo_skill_names:
        lines.append(f"- {name}")

    lines.extend(
        [
            "",
            "## All Available Skills",
            "",
            "| Name | Source | Path | Description |",
            "| --- | --- | --- | --- |",
        ]
    )

    for entry in entries:
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_cell(entry.name),
                    escape_cell(entry.source),
                    f"`{escape_cell(entry.relative_path)}`",
                    escape_cell(entry.description),
                ]
            )
            + " |"
        )

    lines.append("")
    return "\n".join(lines)


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SKILLS.md from local skill roots.")
    parser.add_argument("--repo-root", type=Path, default=Path("."), help="Repository root.")
    parser.add_argument("--output", type=Path, default=Path("SKILLS.md"), help="Output markdown file.")
    parser.add_argument("--check", action="store_true", help="Check whether output is current.")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    roots = default_roots(repo_root)
    entries = collect_entries(roots)
    content = markdown_table(entries)
    output = args.output if args.output.is_absolute() else repo_root / args.output

    if args.check:
        current = output.read_text(encoding="utf-8") if output.exists() else ""
        if current == content:
            print("SKILLS.md is current.")
            return 0
        print("SKILLS.md is out of date.")
        return 1

    output.write_text(content, encoding="utf-8", newline="\n")
    print(f"Wrote {output} with {len(entries)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
