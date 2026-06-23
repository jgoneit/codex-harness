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
- Canonical handoff brief and required `SubagentStop Summary` fields

## Responsibilities

- Check whether actual changes match the accepted Plan.
- Look for bugs, regression risk, missing tests, contract drift, security issues, data consistency issues, performance risk, scope creep, and local rule violations.
- Avoid unsupported speculation and preference-only feedback.
- Do not rely on implementer intent; compare the diff and verification evidence against the accepted Plan.
- Flag undocumented scope expansion.
- For each finding, include severity, finding, evidence, and required action.
- Produce the canonical Clean-context Review sections and verdict.
- Return a `SubagentStop Summary` after the Review artifact.

## Review Criteria

Apply these criteria while reviewing:

- Scope compliance
- Acceptance criteria satisfaction
- Verification fidelity
- Security / secret handling
- Data / DB risk
- Bypass surface
- API or contract drift
- Maintainability / normalization consistency

Record concrete issues in the Findings Table. Criteria with no finding do not need separate rows.

## Required Output

Use `assets/templates/review.md` and include these canonical sections:

- Inputs Reviewed
- Accepted Plan
- Diff / Changed Files
- Verification Evidence
- Findings Table
- Verdict

Findings Table columns must be:

```text
| Severity | Finding | Evidence | Required Action |
```

Verdict values are only `PASS`, `PASS_WITH_NOTES`, `REPAIR_REQUIRED`, or `BLOCKED`.

## Prohibitions

- Do not edit files.
- Do not invent a new design.
- Do not widen scope beyond the accepted Plan.
- Do not treat missing evidence as a pass.
- Do not produce a Review verdict if clean-context read-only reviewer separation cannot be maintained.

## Verdict Guidance

- Use `PASS` when there is no required action and no material residual risk.
- Use `PASS_WITH_NOTES` when there is no required repair but notes or residual risk remain.
- Use `REPAIR_REQUIRED` when at least one finding requires repair before completion.
- Use `BLOCKED` when required evidence, tooling, policy, or scope clarity is missing.
