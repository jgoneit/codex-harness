# Completion Report

## Artifact Metadata

- Harness run id:
- Artifact id:
- Phase: Completion
- Artifact status: draft / accepted / revised / completed / blocked / degraded
- Created at:
- Updated at:
- Source request:
- Task classification: Tiny / Small / Non-trivial
- Related artifacts:

## Status

- Status: completed / completed_with_residual_risk / blocked / degraded / cancelled
- Classification:
- Outcome:
- Reason:

## Review Status

- Review status enum: clean_context_review_completed / review_not_required_tiny_only / review_blocked_degraded
- Reviewer subagent used? Yes/No:
- Clean-context and read-only? Yes/No:
- Degraded review reason, if any:

## Repair Plan Required

- Required? Yes/No:
- Reason:
- Repair approval completed? Yes/No/not_applicable:

## Changed Files

-

## Verification

- Commands/checks:
- Results:
- Evidence:
- Blocked or skipped checks:

## Review Result

- Verdict: PASS / PASS_WITH_NOTES / REPAIR_REQUIRED / BLOCKED / not_applicable
- Findings addressed:
- Findings deferred:
- Findings rejected:

## Approval Ledger

Use columns exactly as shown. Do not leave any cells blank; use `not_applicable` where a gate or field does not apply. Add one Repair plan approval row per repair round when multiple rounds occur.

| Gate | Required? | Requested? | User response | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| Plan approval | required | requested | y / non-y stopped / explicit revision or replan requested / blocked | approved / not_approved / blocked | Record exact gate outcome. |
| Scope expansion approval | required / not_applicable | requested / not_applicable | user response / not_applicable | approved / denied / blocked / not_applicable | Required only when scope expansion is needed. |
| Destructive command approval | required / not_applicable | requested / not_applicable | user response / not_applicable | approved / denied / blocked / not_applicable | Required before destructive commands. |
| Secret/config access approval | required / not_applicable | requested / not_applicable | user response / not_applicable | approved / denied / blocked / not_applicable | Required before secret or protected config access. |
| Direct DB access approval | required / not_applicable | requested / not_applicable | user response / not_applicable | approved / denied / blocked / not_applicable | Required before direct database access. |
| Repair plan approval | required / not_applicable | requested / not_applicable | y / non-y stopped / explicit revision or replan requested / not_applicable / blocked | approved / not_approved / not_applicable / blocked | Use one row per repair round. |
| Verification exception approval | required / not_applicable | requested / not_applicable | user response / not_applicable | approved / denied / blocked / not_applicable | Required when completing despite skipped or weakened verification. |

## Residual Risks

-

## Follow-up

-

## Blocked / Degraded Details

Use only when Status is `blocked` or `degraded`, or when Review status is `review_blocked_degraded`.

- Role or gate:
- Blocker or degraded condition:
- Evidence inspected:
- Criteria applied:
- Risk observations:
- User decision or external state change needed:
- Degraded independence statement:
