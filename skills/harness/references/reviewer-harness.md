# Reviewer Harness

The reviewer is the only role that can complete Review. It must be a clean-context read-only subagent.

## Inputs

- Accepted Plan
- Task classification
- Acceptance criteria
- Changed files/areas
- Diff or diff summary
- Verification results
- Relevant project rules
- Required output format

## Responsibilities

- Check whether actual changes match the accepted Plan.
- Look for bugs, regression risk, missing tests, contract drift, security issues, data consistency issues, performance risk, scope creep, and local rule violations.
- Avoid unsupported speculation and preference-only feedback.
- For each finding, include severity, evidence, why it matters, suggested action, and must-fix-now status.
- Produce the required Review Matrix with exact columns and minimum criteria.
- Separate blocking findings from non-blocking findings.

## Review Matrix

Review output must include a table with columns exactly:

```text
| Criterion | Verdict | Evidence | Residual Risk |
```

Minimum criteria:

- Scope compliance
- Acceptance criteria satisfaction
- Test coverage / verification fidelity
- Security / secret handling
- Data / DB risk
- Bypass surface
- API or contract drift
- Maintainability / normalization consistency

Verdict values are only `pass`, `fail`, `unknown`, or `not_applicable`. `unknown` is not a pass and must be treated as residual risk. Every matrix cell must be filled; use `not_applicable` where applicable instead of blanks.

## Prohibitions

- Do not edit files.
- Do not invent a new design.
- Do not widen scope beyond the accepted Plan.

## No-Finding Statement

If there are no concrete findings, include the required Review Matrix and then write exactly:

```text
No concrete findings. Residual verification risk:
- ...
```
