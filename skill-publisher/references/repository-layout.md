# Skill Repository Layout

## Recommended Structure

Use this layout for a repository that contains one or more Codex skills:

```text
repo-root/
├── README.md
├── SKILLS.md
├── agent.md
└── skill-name/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── references/
    ├── examples/
    └── scripts/
```

Only create resource directories that the skill actually uses.

## Root Files

- `README.md`: repository purpose, skill folder list, and basic validation command.
- `SKILLS.md`: plain list of skill names available in the repository or source environment.
- `agent.md`: maintenance instructions for future agents working in the repo.

## Skill Folder Requirements

- Folder name should match `name` in `SKILL.md`.
- `SKILL.md` frontmatter must include only the fields needed by the skill platform unless repository policy says otherwise.
- `description` should include concrete user trigger phrases.
- The body should be procedural and concise.
- Detailed material should move into `references/`, `examples/`, or `scripts/`.

## Publication Checklist

- Validate every skill folder.
- Check that root indexes mention new skills.
- Run relevant scripts and syntax checks.
- Confirm `git status --short` contains only intended files.
- Commit to the requested branch.
- Push and verify the file exists on GitHub.

## GitHub Checks

After publishing, verify with one of:

```powershell
gh repo view OWNER/REPO --json name,visibility,description,defaultBranchRef,url
gh api repos/OWNER/REPO/contents/path/to/file --jq .html_url
```
