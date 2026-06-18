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

- [ ] Bugs
- [ ] Regression risk
- [ ] Missing or weak tests
- [ ] Contract drift
- [ ] Security issues
- [ ] Data consistency issues
- [ ] Performance risk
- [ ] Scope creep
- [ ] Local rule violations
- [ ] Orchestration gaps

Unchecked criteria must be listed under Residual verification risk.

## Required Output Format

Findings first, ordered by severity. Each finding must include:

- Severity:
- Evidence:
- Why it matters:
- Suggested action:
- Must fix now?:

If there are no concrete findings, write exactly:

```text
No concrete findings. Residual verification risk:
- ...
```

## Explicit Instructions

- Do not edit files.
- Include only concrete findings.
- Do not include preference-only feedback.
- If evidence is unavailable, record verification risk instead of guessing.
