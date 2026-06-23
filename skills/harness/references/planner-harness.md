# Planner Harness

The planner is used for `Small` and larger tasks to draft the Plan artifact. The Plan must follow the authoritative contract in `docs/contracts/harness-contract.md`.

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
- State task classification, risk level, and reasoning for classification.
- Define in-scope and out-of-scope boundaries before implementation.
- Identify files or areas to inspect.
- Define verification strategy before implementation.
- Make scope concrete enough that implementers do not invent decisions.
- State risks and escalation triggers.
- Record intended and actual `model_reasoning_effort`, including fallback decisions.

## Non-goals

- Do not edit code.
- Do not expand product scope.
- Do not declare success without verification.

## Required Output

Use `assets/templates/plan.md` and include these canonical sections:

- Task Classification
- Risk Level
- Reasoning for classification
- In Scope
- Out of Scope
- Files / Areas to Inspect
- Proposed Change Plan
- Verification Plan
- Risks / Assumptions
- Approval Gate

The Approval Gate must use the exact prompt `Proceed with this Plan? [y/N]`. Only lowercase `y` approves implementation.
