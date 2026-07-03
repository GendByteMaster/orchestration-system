#!/usr/bin/env python3
"""Validate a repository that contains one or more Codex skills."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT_RECOMMENDED = ("README.md", "SKILLS.md", "agent.md")
RESOURCE_DIRS = ("references", "examples", "scripts", "assets")
REFERENCE_PATTERN = re.compile(r"`((?:references|examples|scripts|assets)/[^`]+)`")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, [f"{path}: missing YAML frontmatter"]
    try:
        end = text.index("\n---", 4)
    except ValueError:
        return {}, [f"{path}: frontmatter is not closed"]

    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"{path}: invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields, errors


def find_skill_dirs(root: Path) -> list[Path]:
    return sorted(
        path.parent
        for path in root.rglob("SKILL.md")
        if ".git" not in path.parts
    )


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    fields, frontmatter_errors = parse_frontmatter(skill_file)
    errors.extend(frontmatter_errors)

    name = fields.get("name")
    description = fields.get("description")
    if not name:
        errors.append(f"{skill_file}: missing frontmatter field: name")
    if not description:
        errors.append(f"{skill_file}: missing frontmatter field: description")
    if name and name != skill_dir.name:
        errors.append(f"{skill_file}: name '{name}' does not match folder '{skill_dir.name}'")
    if description and len(description) < 80:
        errors.append(f"{skill_file}: description is too short to be useful")

    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        errors.append(f"{skill_dir}: missing agents/openai.yaml")

    text = skill_file.read_text(encoding="utf-8")
    for match in REFERENCE_PATTERN.finditer(text):
        rel = match.group(1).replace("/", "\\")
        if not (skill_dir / rel).exists():
            errors.append(f"{skill_file}: referenced file does not exist: {match.group(1)}")

    for resource_dir in RESOURCE_DIRS:
        path = skill_dir / resource_dir
        if path.exists() and path.is_dir() and not any(path.iterdir()):
            errors.append(f"{path}: empty resource directory")

    return errors


def validate_repo(root: Path) -> list[str]:
    errors: list[str] = []
    for filename in ROOT_RECOMMENDED:
        if not (root / filename).exists():
            errors.append(f"Missing recommended root file: {filename}")

    skill_dirs = find_skill_dirs(root)
    if not skill_dirs:
        errors.append("No skill folders found")
        return errors

    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir))

    skills_index = root / "SKILLS.md"
    if skills_index.exists():
        index_text = skills_index.read_text(encoding="utf-8")
        for skill_dir in skill_dirs:
            if f"- {skill_dir.name}" not in index_text:
                errors.append(f"SKILLS.md does not list skill: {skill_dir.name}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Codex skill repository.")
    parser.add_argument("root", nargs="?", default=".", type=Path, help="Repository root.")
    args = parser.parse_args()

    root = args.root.resolve()
    errors = validate_repo(root)
    if errors:
        print("Invalid skill repository:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Valid skill repository.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
