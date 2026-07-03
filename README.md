# orchestration-system

Public repository for the `orchestration-system` Codex skill.

This skill helps plan and coordinate complex work across roles, agents, tools, validation gates, and integration checkpoints.

## Contents

- `orchestration-system/` - the current skill package.
- `SKILLS.md` - names of available skills from the creation environment.

## Validation

Validate an orchestration plan with:

```powershell
python orchestration-system\scripts\validate_orchestration_plan.py orchestration-system\examples\valid-plan.json
```
