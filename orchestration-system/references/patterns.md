# Orchestration Patterns

## Plan Schema

Use this schema for larger tasks or when outputs will be passed between agents:

```json
{
  "objective": "Concrete end state",
  "assumptions": ["Explicit assumptions"],
  "workstreams": [
    {
      "id": "short-stable-id",
      "role": "mapper|planner|builder|reviewer|verifier|integrator",
      "task": "Bounded task statement",
      "inputs": ["Files, URLs, artifacts, or constraints"],
      "outputs": ["Expected deliverables"],
      "status": "pending|in_progress|blocked|complete"
    }
  ],
  "dependencies": [
    {
      "before": "ws1",
      "after": "ws2",
      "reason": "Why ws2 depends on ws1"
    }
  ],
  "artifacts": ["Patch, report, test log, migration plan"],
  "validation": ["Commands, manual checks, review gates"],
  "risks": ["Known risk or uncertainty"],
  "integration": "How outputs will be merged and conflicts resolved",
  "stop_conditions": ["Conditions that require user input or approval"]
}
```

## Common Patterns

### Scout Then Build

Use when the codebase or domain is unfamiliar.

1. Assign a mapper to inspect structure, conventions, and likely files.
2. Assign a planner to turn findings into a bounded implementation plan.
3. Build only after the likely blast radius is known.
4. Verify with commands mapped to the changed layer.

### Parallel Review

Use when correctness matters more than speed.

1. Builder produces a patch or proposal.
2. Reviewer A checks behavior and edge cases.
3. Reviewer B checks tests, security, or maintainability.
4. Integrator accepts only findings backed by evidence.

### Independent Workstreams

Use when tasks touch separate artifacts.

1. Define one owner per artifact.
2. Give each owner explicit write boundaries.
3. Require outputs in the same format.
4. Integrate after all workstreams pass local validation.

### Research Synthesis

Use when facts must be gathered from multiple sources.

1. Assign source-specific researchers.
2. Require citations or exact source references.
3. Normalize findings into a shared comparison table.
4. Let the integrator separate verified facts from inferences.

## Anti-Patterns

- Parallel edits to the same file without a merge owner.
- Delegating vague tasks such as "look into it" without expected outputs.
- Treating reviewer comments as truth without evidence.
- Starting implementation before constraints and success criteria are known.
- Running destructive or networked actions without approval when the environment requires it.
- Letting subagents inherit hidden conclusions that should be independently verified.

## Delegation Prompt Template

```text
Objective: <overall objective>
Role: <mapper|planner|builder|reviewer|verifier|integrator>
Scope: <files, modules, source set, or artifact boundary>
Task: <specific work to perform>
Inputs: <allowed context and artifacts>
Constraints: <permissions, prohibited actions, style rules, time budget>
Expected output:
- Findings:
- Changed artifacts:
- Validation evidence:
- Open questions:
Stop if: <conditions requiring escalation>
```

## Integration Checklist

- Confirm every workstream produced the requested output.
- Resolve conflicts by source evidence, tests, or user-stated priority.
- Merge duplicate findings.
- Convert open questions into assumptions, blockers, or follow-up tasks.
- Run final validation after integration, not only per-workstream validation.
- Produce a final answer that separates completed work, verification, and residual risk.

## Escalation Guidance

Pause and ask for user input when:

- A required credential, production system, paid service, or destructive action is needed.
- Multiple valid directions would produce materially different outcomes.
- A dependency conflict makes the requested result impossible without changing scope.
- Verification cannot be performed and the remaining risk is high.
