---
name: orchestration-system
description: This skill should be used when the user asks to "orchestrate work", "coordinate agents", "split a complex task", "run parallel implementation", "design an orchestration system", "create an agent workflow", "manage multi-agent execution", or needs a structured plan for delegating, validating, and integrating complex engineering or research work.
---

# Orchestration System

## Overview

Plan and coordinate complex work across roles, agents, tools, and validation gates. Use this skill to turn a broad objective into a controlled execution system with clear ownership, dependencies, artifacts, and merge criteria.

## Core Workflow

### 1. Define the Mission

Capture the outcome before assigning work:

- Objective: the concrete end state.
- Scope: included and excluded work.
- Constraints: time, permissions, repos, tools, network, deployment, safety, budget.
- Success criteria: observable checks that prove the work is complete.
- Stop conditions: cases where execution must pause for user input.

If the objective is ambiguous, ask only the smallest set of questions needed to prevent incorrect execution. Otherwise make explicit assumptions and continue.

### 2. Decompose the Work

Split work by artifact boundaries, not by vague activity. Prefer units that can be verified independently:

- Discovery: inspect repo, APIs, data, requirements, constraints.
- Design: propose architecture, data flow, interfaces, UX, or migration path.
- Implementation: change a bounded module, feature, script, or document.
- Verification: run tests, review diffs, validate behavior, check edge cases.
- Integration: reconcile outputs, resolve conflicts, produce final handoff.

Avoid parallelizing tasks that write the same files, mutate shared state, depend on each other's unpublished conclusions, or require sequential user approvals.

### 3. Assign Roles

Give each role a narrow charter with inputs and outputs. Good roles include:

- Mapper: builds a codebase or domain map and identifies files to inspect.
- Planner: designs the execution strategy and dependency graph.
- Builder: implements a scoped change.
- Reviewer: looks for bugs, missing tests, regressions, and security risks.
- Verifier: runs commands and records evidence.
- Integrator: merges findings into one coherent final answer or patch set.

Prefer one owner per artifact. Use multiple reviewers only when the risk justifies it.

### 4. Create the Orchestration Plan

Represent the plan as a checklist or JSON object before execution when the task is large, risky, or multi-agent. Include:

- `objective`
- `assumptions`
- `workstreams`
- `dependencies`
- `artifacts`
- `validation`
- `risks`
- `integration`
- `stop_conditions`

For detailed patterns and templates, read `references/patterns.md`.

### 5. Execute in Waves

Run work in waves:

1. Discovery wave: gather facts and identify constraints.
2. Planning wave: decide task graph, owners, and validation gates.
3. Build wave: execute independent workstreams.
4. Review wave: inspect outputs and run verification.
5. Integration wave: combine outputs and produce the final result.

At each wave boundary, update the plan with completed work, changed assumptions, and remaining risks. Do not hide conflicting findings; reconcile them explicitly.

### 6. Control Context and Handoffs

Each delegated workstream should receive only the context needed for its task:

- Objective and local scope.
- Files or artifacts to inspect.
- Expected output format.
- Constraints and prohibited actions.
- Validation commands or review criteria.

Require outputs that are easy to integrate:

- Findings with file and line references.
- Patch summaries with changed files.
- Test evidence with exact commands and outcomes.
- Open questions separated from conclusions.

### 7. Validate Before Completion

Before claiming completion:

- Confirm every success criterion has matching evidence.
- Confirm every changed artifact has an owner and review path.
- Run the relevant validation commands when available.
- Record tests that could not run and why.
- Check unresolved risks and decide whether they block completion.

For machine-checkable plans, use `scripts/validate_orchestration_plan.py`.

## Decision Rules

Use sequential execution when:

- A later task depends on code or decisions from an earlier task.
- Tasks touch the same files or database state.
- User approval is needed between steps.
- The task is small enough that orchestration overhead is wasteful.

Use parallel execution when:

- Workstreams inspect independent areas.
- Outputs can be merged without shared writes.
- Independent review improves confidence.
- Time savings justify coordination overhead.

Escalate to a stronger plan when:

- The work affects production, security, data loss, billing, auth, or migrations.
- More than two modules or systems are involved.
- Requirements are ambiguous and wrong execution would be expensive.
- Multiple agents or tools may produce conflicting outputs.

## Output Formats

### Compact Plan

Use for ordinary complex tasks:

```markdown
Objective:
Assumptions:
Workstreams:
Dependencies:
Validation:
Risks:
Integration:
Stop conditions:
```

### JSON Plan

Use when the plan should be validated or handed to tooling:

```json
{
  "objective": "Ship feature X with tests",
  "assumptions": ["Repo is the source of truth"],
  "workstreams": [
    {
      "id": "ws1",
      "role": "mapper",
      "task": "Inspect routing and data flow",
      "inputs": ["src/routes", "src/api"],
      "outputs": ["route map", "risk list"],
      "status": "pending"
    }
  ],
  "dependencies": [],
  "artifacts": ["patch", "test log", "final summary"],
  "validation": ["npm test", "npm run lint"],
  "risks": ["Auth behavior may be affected"],
  "integration": "Integrator reconciles mapper findings before implementation.",
  "stop_conditions": ["Missing credentials", "destructive migration required"]
}
```

## Resources

- `references/patterns.md` - orchestration patterns, anti-patterns, prompt templates, and escalation guidance.
- `examples/valid-plan.json` - complete JSON plan that can be copied and adapted.
- `scripts/validate_orchestration_plan.py` - validate a JSON orchestration plan for required fields and common structural mistakes.
