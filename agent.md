# Agent Instructions

## Repository Purpose

Maintain the `orchestration-system` Codex skill. The repository is intentionally small: keep the skill package focused, readable, and easy to install or copy.

## Structure

- `orchestration-system/SKILL.md` - primary skill instructions and trigger metadata.
- `orchestration-system/references/patterns.md` - detailed orchestration patterns and templates.
- `orchestration-system/examples/valid-plan.json` - sample machine-checkable orchestration plan.
- `orchestration-system/scripts/validate_orchestration_plan.py` - JSON plan validator.
- `SKILLS.md` - list of skill names from the creation environment.

## Editing Rules

- Keep `SKILL.md` concise and procedural.
- Move detailed patterns, examples, and edge cases into `references/` or `examples/`.
- Keep filenames and skill names stable unless intentionally migrating the skill.
- Use ASCII text unless a file already requires another character set.
- Avoid adding unrelated documentation or generated artifacts.

## Validation

Run the validator after changing the plan schema, example plan, or validation script:

```powershell
python orchestration-system\scripts\validate_orchestration_plan.py orchestration-system\examples\valid-plan.json
```

For Python syntax checks:

```powershell
python -m py_compile orchestration-system\scripts\validate_orchestration_plan.py
```

## Release Checklist

- Confirm `SKILL.md` frontmatter has `name` and `description`.
- Confirm referenced files exist.
- Confirm the example plan validates.
- Commit changes to `master`.
