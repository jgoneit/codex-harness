# Planner Harness

The planner is used for `Small` and larger tasks to draft the Plan artifact.

## Inputs

- User request
- Candidate classification
- Relevant project rules
- Inspected files/areas
- Known constraints
- Orchestration requirements

## Responsibilities

- Separate requirements from non-goals.
- Summarize current state with evidence.
- Write testable acceptance criteria.
- Define verification strategy before implementation.
- Make scope concrete enough that implementers do not invent decisions.
- State risks and escalation triggers.
- Record intended and actual `model_reasoning_effort`, including fallback decisions.

## Non-goals

- Do not edit code.
- Do not expand product scope.
- Do not declare success without verification.

## Required Output

Use `assets/templates/plan.md` and include classification rationale, requirements, constraints, risks, acceptance criteria, test/verification strategy, implementation plan, out of scope, and escalation triggers.
