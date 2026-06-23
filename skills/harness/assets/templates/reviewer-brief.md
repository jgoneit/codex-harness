# Reviewer Brief

## Objective

Review completed changes against the accepted Plan, changed files, diff, verification evidence, and relevant project rules. Only this clean-context read-only reviewer subagent can complete Review.

## Inputs

- Accepted Plan:
- Task classification:
- Risk level:
- Changed files:
- Diff or diff summary:
- Verification evidence:
- Relevant project rules:
- Implementation Summary:

## Authorization Summary

- Authorization status: policy preauthorization / explicit approval granted / explicit approval denied / blocked
- Review scope:
- Files or areas:
- Evidence required to pass:
- Non-goals:

## Scope

- Review only context directly related to the provided changes.
- Judge whether changes satisfy the accepted Plan.
- Compare the diff against the accepted Plan and write boundary.
- Flag undocumented scope expansion.
- Treat missing or weak verification evidence as residual risk or a finding.

## Non-goals

- Do not edit files.
- Do not implement fixes.
- Do not rely on implementer intent.
- Do not propose redesign without concrete risk.
- Do not widen scope beyond the accepted Plan.

## Review Criteria

- Scope compliance
- Acceptance criteria satisfaction
- Verification fidelity
- Security / secret handling
- Data / DB risk
- Bypass surface
- API or contract drift
- Maintainability / normalization consistency

## Required Output Format

Use the canonical Clean-context Review sections:

- Inputs Reviewed
- Accepted Plan
- Diff / Changed Files
- Verification Evidence
- Findings Table
- Verdict

The Findings Table must use columns exactly:

```text
| Severity | Finding | Evidence | Required Action |
```

Verdict values are only `PASS`, `PASS_WITH_NOTES`, `REPAIR_REQUIRED`, or `BLOCKED`.

Use `PASS` only when there is no required action and no material residual risk. Use `PASS_WITH_NOTES` when there is no required repair but notes or residual risk remain. Use `REPAIR_REQUIRED` when at least one finding requires repair before completion. Use `BLOCKED` when required evidence, tooling, policy, or scope clarity is missing.

Append this `SubagentStop Summary` after the Review artifact:

- Role:
- Task / Phase:
- Inputs Received:
- Actions Completed:
- Files Inspected:
- Files Changed:
- Verification Performed:
- Evidence Produced:
- Blockers:
- Residual Risks:
- Required Next Action:
