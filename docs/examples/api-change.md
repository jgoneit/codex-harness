# API Change Demo

This is an illustrative scenario, not an actual execution transcript. Sample user responses, statuses, review evidence, and verification notes below are illustrative only.

This example shows a Non-trivial public API contract change. The full Harness loop is Harness Plan -> Execute approval -> Implement -> Clean-context Review -> Repair Plan -> Repair approval -> Repair Implement -> Completion Report; in this illustrative path, Clean-context Review returns `PASS_WITH_NOTES`, so repair phases are recorded as `not_applicable`.

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
- Required gates: Planner Harness Plan, exact Plan approval, one or more implementers, Clean-context Review, Repair Plan if needed, exact Repair approval if needed, Repair Implement if needed, and Completion Report.

## Harness Plan Shape

Illustrative Harness Plan excerpt:

- Scope: add `request_id` to the orders response serializer, API schema, and focused contract tests.
- Non-goals: no authentication changes, no database migration, no release packaging, no deployment.
- Acceptance criteria: existing fields remain unchanged, new field is documented, and focused contract coverage reflects the response shape.
- Verification strategy: run the focused API contract test or, if unavailable in the local environment, record the blocked check and inspect schema/serializer consistency.
- New gate triggers: any need for database migration, auth behavior change, client SDK generation, broad test rewrites, or release packaging returns to a new approval gate.

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

Illustrative Findings Table:

| Severity | Finding | Evidence | Required Action |
| --- | --- | --- | --- |
| Note | Downstream client and SDK validation were not performed. | Illustrative evidence: focused contract coverage targets the changed response shape, and SDK updates remain outside this illustrative scope. | No repair required; request separate approval if downstream SDK updates become necessary. |

Illustrative Verdict:

```text
PASS_WITH_NOTES
```

## Repair Plan If Needed

No Repair Plan is needed in this illustrative path.

If Review returned `REPAIR_REQUIRED` for contract drift, Harness would write a Repair Plan before any repair implementation and use this exact prompt:

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
| Repair plan approval | not_applicable | not_applicable | not_applicable | not_applicable | Review returned `PASS_WITH_NOTES`; no repair was required. |
| Verification exception approval | not_applicable | not_applicable | not_applicable | not_applicable | No completion-over-skipped-required-check exception requested in this illustrative path. |
