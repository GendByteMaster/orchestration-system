---
name: skill-publisher
description: This skill should be used when the user asks to "publish a skill", "prepare skill for repository", "create GitHub repo for a skill", "package Codex skill", "update skill repo", "commit and push skill", or needs a repeatable workflow for validating and publishing Codex skill folders to a GitHub repository.
---

# Skill Publisher

## Overview

Prepare Codex skills for repository publication. Use this skill to package a skill folder, validate its required files, update repository indexes, and publish changes through a clean git workflow.

## Publishing Workflow

### 1. Confirm the Target

Identify the skill folder and destination repository before changing files:

- Skill name and folder path.
- Repository owner/name and branch.
- Publication mode: new repository, new skill in an existing repository, or update to an existing skill.
- Visibility expectation when creating a repository.
- Required root files such as `README.md`, `SKILLS.md`, or `agent.md`.

When the destination is already a git repository, preserve its current branch and remote unless the user explicitly requests a change.

### 2. Validate Skill Shape

Confirm the skill package is self-contained:

- `SKILL.md` exists.
- Frontmatter contains `name` and `description`.
- Skill folder name matches the frontmatter `name`.
- `agents/openai.yaml` exists when repository conventions expect UI metadata.
- Referenced `references/`, `examples/`, `scripts/`, and `assets/` files exist.
- Scripts are syntax-checkable or executable where practical.

Use `scripts/validate_skill_repo.py` for baseline repository checks.

### 3. Prepare Repository Files

Keep the repository minimal and useful:

- Root `README.md` should describe the repository purpose and list skill folders.
- Root `SKILLS.md` should list available skill names.
- Root `agent.md` should document maintenance instructions when agents will work in the repo.
- Each skill should keep detailed guidance inside its own folder.

Avoid adding installation guides, changelogs, or unrelated documentation unless the user asks for them.

### 4. Validate Before Publishing

Run validation before commit:

```powershell
python skill-publisher\scripts\validate_skill_repo.py .
```

Also run any skill-specific validators, examples, or syntax checks. Record commands that cannot run and why.

### 5. Commit and Push

Use a focused git workflow:

1. Check `git status --short`.
2. Stage only intended files.
3. Commit with a concise message.
4. Push to the requested branch.
5. Confirm the remote repository shows the expected files.

Do not rename branches, change remotes, or alter repository visibility unless explicitly requested.

## Decision Rules

Create a new repository when:

- The user asks for a standalone public or private repo.
- The skill is meant to be distributed independently.
- Existing repository scope would become confusing.

Add a skill to an existing repository when:

- The repository already groups related skills.
- The user asks to prepare the skill for the current repo.
- Shared root documentation should index multiple skills.

Update an existing skill in place when:

- The folder already exists.
- The request is about improving triggers, references, scripts, examples, or validation.
- The repository structure already matches the expected publication format.

## Resources

- `references/repository-layout.md` - recommended structure, root files, and release checklist.
- `examples/minimal-skill-repo.json` - example manifest for a minimal skill repository.
- `scripts/validate_skill_repo.py` - validate a repository containing one or more Codex skills.
- `scripts/update_skill_index.py` - regenerate `SKILLS.md` from local skill roots.
