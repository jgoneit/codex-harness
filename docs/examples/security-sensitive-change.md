# Security-Sensitive Change Demo

This is an illustrative scenario, not an actual execution transcript. Sample user responses, statuses, review evidence, and verification notes below are illustrative only.

This example shows a Non-trivial security-sensitive change with an explicit secret/config access gate. The full Harness loop is Harness Plan -> Execute approval -> Implement -> Clean-context Review -> Repair Plan -> Repair approval -> Repair Implement -> Completion Report; in this illustrative path, Clean-context Review returns `PASS_WITH_NOTES`, so repair phases are recorded as `not_applicable`.

## User Request

```text
Use $harness for this change.

Objective: stop password reset tokens from appearing in request logs.

Constraints:
- Use local fixtures or unit tests for verification.
- Do not read `.env`, production config, credential files, or real logs unless separately approved.
- Do not change database schema, deployment config, release scripts, or packaging.
```

## Task Classification

- Classification: Non-trivial
- Reason: The request changes security-sensitive token handling and logging behavior, and it explicitly controls access to secrets and protected config.
- Required gates: Planner Harness Plan, exact Plan approval, implementer, Clean-context Review, Repair Plan if needed, exact Repair approval if needed, Repair Implement if needed, and Completion Report. Secret/config access requires a separate explicit approval gate before any protected config or credential material is read.

## Harness Plan Shape

Illustrative Harness Plan excerpt:

- Scope: update token redaction in the logging path and add focused fixture-based verification.
- Non-goals: no real secret reads, no production log access, no deployment, no database migration, no packaging.
- Acceptance criteria: reset tokens are redacted in the covered log path, normal request metadata remains available, and verification uses only local fixtures.
- Verification strategy: run or describe focused fixture-based redaction checks and inspect the diff for secret-safe behavior.
- New gate triggers: reading `.env`, credential files, production config, or real logs requires separate secret/config access approval before proceeding.

```text
Proceed with this Plan? [y/N]
```

Only lowercase `y` approves execution of the accepted Plan.

## Approval Gate

Illustrative Plan approval response:

```text
y
```

Result: Plan approved. Any response other than lowercase `y` would leave implementation unapproved.

Illustrative secret/config access gate:

- Gate: Secret/config access approval
- Request: read `.env.production` to compare real token names
- Illustrative user response: `n`
- Result: denied; no protected config, credential file, or real log is read. The accepted Plan continues only because fixture-based verification remains in scope.

## Implementation Summary

Illustrative implementer report shape:

- Changed files: token logging redaction helper and focused fixture-based redaction test.
- Summary: redacted password reset token values before request log emission while preserving non-sensitive metadata.
- Verification: illustrative fixture-based redaction evidence is reported as sample evidence, not as a real local command result.
- Deviations: secret/config access was denied and not used; residual risk is recorded for real-environment naming differences.

## Review Result

Illustrative Findings Table:

| Severity | Finding | Evidence | Required Action |
| --- | --- | --- | --- |
| Note | Fixture-only verification cannot prove every production log format is represented. | Illustrative evidence: no `.env`, credential file, production config, or real log was read after the denied gate; fixture-based verification covered only the targeted token redaction path. | No repair required; request separate approval before inspecting protected config or real logs. |

Illustrative Verdict:

```text
PASS_WITH_NOTES
```

## Repair Plan If Needed

No Repair Plan is needed in this illustrative path.

If Review returned `REPAIR_REQUIRED` for an unredacted token path, Harness would write a Repair Plan before any repair implementation and use this exact prompt:

```text
Proceed with this Repair Plan? [y/N]
```

Only lowercase `y` would approve repair implementation.

## Completion Report Shape

Illustrative Completion excerpt:

- Task classification: Non-trivial
- Review status: `clean_context_review_completed`
- Completion status: `completed_with_residual_risk`
- Findings addressed: `not_applicable`
- Unresolved risks: fixture-only verification leaves residual risk around unrepresented production log formats.

Illustrative partial Approval Ledger:

| Gate | Required? | Requested? | User response | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| Plan approval | required | requested | `y` (illustrative) | approved | Exact prompt was `Proceed with this Plan? [y/N]`; only lowercase `y` approved. |
| Scope expansion approval | not_applicable | not_applicable | not_applicable | not_applicable | No scope expansion requested. |
| Destructive command approval | not_applicable | not_applicable | not_applicable | not_applicable | No destructive command requested. |
| Secret/config access approval | required | requested | `n` (illustrative) | denied | Protected config was not read; fixture-only verification continued inside the accepted Plan. |
| Direct DB access approval | not_applicable | not_applicable | not_applicable | not_applicable | No direct database access requested. |
| Repair plan approval | not_applicable | not_applicable | not_applicable | not_applicable | Review returned `PASS_WITH_NOTES`; no repair was required. |
| Verification exception approval | not_applicable | not_applicable | not_applicable | not_applicable | Residual risk was recorded; no separate exception gate is shown in this illustrative path. |
