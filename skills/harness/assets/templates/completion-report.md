# Completion Report

## Artifact Metadata

- Harness run id:
- Artifact id:
- Phase: Completion
- Artifact status: draft / accepted / revised / completed / blocked_degraded
- Created at:
- Updated at:
- Source request:
- Task classification: Tiny / Small / Non-trivial
- Related artifacts:

## Summary

- Task classification:
- Outcome:
- Completion status: completed / completed_with_residual_risk / completed_with_degraded_review / blocked / escalated

## Gate Summary

- Classification completed: Yes/No
- Plan approval completed: Yes/No
- Implement completed: Yes/No
- Verification completed: Yes/No
- Review status enum: clean_context_review_completed / review_not_required_tiny_only / review_blocked_degraded
- Repair Plan required: Yes/No
- Repair approval completed: Yes/No/Not required
- Completion report completed: Yes/No

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

## Orchestration Summary

- Required topology:
- Spawned subagents:
- Role/domain assignment:
- Policy preauthorization used? Yes/No:
- Explicit approvals requested:
- Plan approval response: y / non-y stopped / explicit revision or replan requested / blocked
- Repair Plan approval response: y / non-y stopped / explicit revision or replan requested / not required / blocked
- Blocked_degraded roles:
- Integration conflicts:
- Conflict resolution:

## Implemented Changes

-

## Verification Performed

- Commands/checks:
- Results:
- Blocked checks:

## Review Status

- Machine-readable Review status enum is recorded in Gate Summary.
- Required? Yes/No:
- Entered? Yes/No:
- Trigger:
- Reviewer subagent used? Yes/No:
- Reviewer subagent identity:
- Findings addressed:

## Blocked / Degraded Details

Use only when a required role is `blocked_degraded` or Review status is `review_blocked_degraded`.

- Role or gate:
- Fallback condition:
- Reason subagent or clean-context Review was not completed:
- Authorization result or blocker:
- Evidence inspected:
- Criteria applied:
- Risk observations:
- Degraded independence statement:

## Diff Inspection

- Scope match:
- Unexpected changes:
- Risk areas:

## Unresolved Risks

-

## Follow-ups

-

## Persistent Artifact Paths

Use only when persistent artifacts were created.

-
