# orchestration-system

Public repository for Codex skills created in this workspace.

The repository currently contains skills for orchestration planning and skill publication workflows.

## Contents

- `orchestration-system/` - plan and coordinate complex work across roles, agents, tools, validation gates, and integration checkpoints.
- `skill-publisher/` - prepare, validate, commit, and publish Codex skills to GitHub repositories.
- `SKILLS.md` - names of available skills from the creation environment.

## Validation

Validate the repository and included examples with:

```powershell
python skill-publisher\scripts\validate_skill_repo.py .
python orchestration-system\scripts\validate_orchestration_plan.py orchestration-system\examples\valid-plan.json
```
