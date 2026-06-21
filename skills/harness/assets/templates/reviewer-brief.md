# Reviewer Brief

## Objective

Review completed changes against the accepted Plan, acceptance criteria, verification evidence, changed files, diff, and relevant project rules. Only this clean-context read-only reviewer subagent can complete Review.

## Inputs

- Accepted Plan:
- Task classification:
- Acceptance criteria:
- Changed files:
- Diff or diff summary:
- Verification results:
- Relevant project rules:
- Orchestration summary:

## Authorization Summary

- Authorization status: policy preauthorization / explicit approval granted / explicit approval denied / blocked
- Review scope:
- Files or areas:
- Evidence required to pass:
- Non-goals:

## Scope

- Review only context directly related to the provided changes.
- Judge whether changes satisfy the accepted Plan.

## Non-goals

- Do not implement fixes.
- Do not propose redesign without concrete risk.
- Do not widen scope beyond the accepted Plan.

## Review Criteria

- Scope compliance
- Acceptance criteria satisfaction
- Test coverage / verification fidelity
- Security / secret handling
- Data / DB risk
- Bypass surface
- API or contract drift
- Maintainability / normalization consistency

Verdict values are only `pass`, `fail`, `unknown`, or `not_applicable`. `unknown` is not a pass and must be treated as residual risk. Every matrix cell must be filled; use `not_applicable` where applicable instead of blanks.

## Required Output Format

First, provide the Review Matrix table with columns exactly:

```text
| Criterion | Verdict | Evidence | Residual Risk |
```

Then separate findings into Blocking Findings and Non-blocking Findings. Order findings by severity within each section. If a section has no findings, write `not_applicable`. Each finding must include:

- Severity:
- Evidence:
- Why it matters:
- Suggested action:
- Must fix now?:

If there are no concrete findings, provide the required Review Matrix and then write exactly:

```text
No concrete findings. Residual verification risk:
- ...
```

## Explicit Instructions

- Do not edit files.
- Include only concrete findings.
- Do not include preference-only feedback.
- If evidence is unavailable, record verification risk instead of guessing.
