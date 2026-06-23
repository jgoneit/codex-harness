# Harness Approval Ledger

Approval entries are historical evidence only. They are not reusable permission. Each new Plan, Repair Plan, scope expansion, destructive command, secret/config access, direct DB access, or verification exception still requires explicit approval when applicable.

## Ledger Metadata

- Project:
- Harness run id:
- Last updated:
- Updated by:
- State status: active / stale / completed / blocked / degraded / cancelled

## Approval Ledger

Use the same columns as the Completion report. Do not leave cells blank; use `not_applicable` where a gate or field does not apply.

| Gate | Required? | Requested? | User response | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| Plan approval | required | requested | pending | pending | Include exact accepted Plan reference. |
| Scope expansion approval | not_applicable | not_applicable | not_applicable | not_applicable | not_applicable |
| Destructive command approval | not_applicable | not_applicable | not_applicable | not_applicable | not_applicable |
| Secret/config access approval | not_applicable | not_applicable | not_applicable | not_applicable | not_applicable |
| Direct DB access approval | not_applicable | not_applicable | not_applicable | not_applicable | not_applicable |
| Repair plan approval | not_applicable | not_applicable | not_applicable | not_applicable | Add one row per repair round when applicable. |
| Verification exception approval | not_applicable | not_applicable | not_applicable | not_applicable | not_applicable |

## Approval Scope Notes

- Exact Plan or Repair Plan tied to approval:
- Scope covered:
- Scope not covered:
- Stale or superseded approvals:

## Security And Privacy Check

- Secrets or credentials recorded? No:
- Sensitive logs or personal data recorded? No:
- Redactions applied:
