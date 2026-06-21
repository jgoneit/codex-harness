# API Change Demo

This is an illustrative scenario, not an actual execution transcript. Sample user responses, statuses, review evidence, and verification notes below are illustrative only.

This example shows a Non-trivial public API contract change. The full Harness loop is Plan -> Execute approval -> Implement -> Review -> Repair Plan -> Repair approval -> Repair Implement -> Completion; in this illustrative path, Review finds no must-fix issue, so repair phases are recorded as `not_applicable`.

## User Request

```text
Use $harness for this change.

Objective: add a `request_id` field to the public `GET /v1/orders/{id}` response.

Constraints:
- Update implementation, schema docs, and focused tests only.
- Do not change authentication, database schema, release scripts, or packaging.
- Preserve backward compatibility for existing response fields.
```

## Task Classification

- Classification: Non-trivial
- Reason: Adding a public response field changes an API contract that clients may depend on, even if the change is additive.
- Required gates: Planner Plan, exact Plan approval, one or more implementers, clean-context read-only Review, Repair Plan if needed, exact Repair approval if needed, Repair Implement if needed, and Completion.

## Plan Shape

Illustrative Plan excerpt:

- Scope: add `request_id` to the orders response serializer, API schema, and focused contract tests.
- Non-goals: no authentication changes, no database migration, no release packaging, no deployment.
- Acceptance criteria: existing fields remain unchanged, new field is documented, and focused contract coverage reflects the response shape.
- Verification strategy: run the focused API contract test or, if unavailable in the local environment, record the blocked check and inspect schema/serializer consistency.
- Escalation triggers: any need for database migration, auth behavior change, client SDK generation, broad test rewrites, or release packaging returns to a new approval gate.

```text
Proceed with this Plan? [y/N]
```

Only lowercase `y` approves execution of the accepted Plan.

## Approval Gate

Illustrative user response:

```text
y
```

Result: Plan approved. Any response other than lowercase `y` would leave implementation unapproved.

## Implementation Summary

Illustrative implementer report shape:

- Changed files: order response serializer, OpenAPI schema fragment, and focused contract test file.
- Summary: added the additive `request_id` field while preserving existing response fields.
- Verification: illustrative focused contract verification and schema inspection are reported as sample evidence, not as real local command results.
- Deviations: none in this illustrative scenario.

## Review Result

Illustrative partial Review Matrix:

| Criterion | Verdict | Evidence | Residual Risk |
| --- | --- | --- | --- |
| Scope compliance | pass | Illustrative evidence: changed areas are limited to serializer, schema docs, and focused contract tests. | not_applicable |
| Acceptance criteria satisfaction | pass | Illustrative evidence: `request_id` appears in implementation and schema while existing fields are preserved. | not_applicable |
| Test coverage / verification fidelity | pass | Illustrative evidence: focused contract coverage targets the changed response shape. | Broader client compatibility remains outside this illustrative scope. |
| Security / secret handling | pass | Illustrative evidence: no authentication, authorization, token, or secret handling path changed. | not_applicable |
| Data / DB risk | not_applicable | Illustrative evidence: no database schema, migration, write path, or direct DB access involved. | not_applicable |
| Bypass surface | not_applicable | Illustrative evidence: no guard, hook, approval, or policy bypass surface changed. | not_applicable |
| API or contract drift | pass | Illustrative evidence: API schema and response serializer are aligned for the additive field. | Downstream SDK updates are not covered unless separately approved. |
| Maintainability / normalization consistency | pass | Illustrative evidence: field naming follows existing snake_case response conventions. | not_applicable |

Illustrative reviewer finding summary:

```text
No concrete findings. Residual verification risk:
- This example does not claim real downstream client validation occurred.
```

## Repair Plan If Needed

No Repair Plan is needed in this illustrative path.

If Review found contract drift, Harness would write a Repair Plan before any repair implementation and use this exact prompt:

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
- Unresolved risks: downstream SDK updates require separate approval if they become necessary.

Illustrative partial Approval Ledger:

| Gate | Required? | Requested? | User response | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| Plan approval | required | requested | `y` (illustrative) | approved | Exact prompt was `Proceed with this Plan? [y/N]`; only lowercase `y` approved. |
| Scope expansion approval | not_applicable | not_applicable | not_applicable | not_applicable | No SDK, migration, or release scope expansion requested. |
| Destructive command approval | not_applicable | not_applicable | not_applicable | not_applicable | No destructive command requested. |
| Secret/config access approval | not_applicable | not_applicable | not_applicable | not_applicable | No secret or protected config access requested. |
| Direct DB access approval | not_applicable | not_applicable | not_applicable | not_applicable | No direct database access requested. |
| Repair plan approval | not_applicable | not_applicable | not_applicable | not_applicable | Review produced no must-fix findings. |
| Verification exception approval | not_applicable | not_applicable | not_applicable | not_applicable | No completion-over-skipped-required-check exception requested in this illustrative path. |
