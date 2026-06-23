# Repair Plan

## Artifact Metadata

- Harness run id:
- Artifact id:
- Phase: Repair Plan
- Artifact status: draft / accepted / revised / completed / blocked / degraded
- Created at:
- Updated at:
- Source request:
- Task classification: Tiny / Small / Non-trivial
- Related artifacts:

## Review Findings Addressed

- Review source:
- Review verdict: REPAIR_REQUIRED / BLOCKED
- Findings accepted for repair:
- Findings deferred:
- Findings rejected with rationale:

## Repair Scope

- Repair objective:
- In scope:
- Out of scope:
- Implementer domain:
- Scope guard:

## Files Expected to Change

-

## Verification Required

- Checks to run:
- Required evidence:
- Blocked or unsafe checks:

## Risks

- Repair risks:
- Escalation triggers requiring a new Plan loop:

## Repair Approval Gate

- Approval prompt: `Proceed with this Repair Plan? [y/N]`
- Approval semantics: only lowercase `y` approves execution of the accepted Repair Plan; ambiguous natural language means no decision and requires asking again for explicit `y` or `n`; non-approval (`n`, empty response, uppercase variants such as `N`, expanded variants, and any other non-`y` response that is not ambiguous) stops by default and does not trigger repair, revision, or replanning unless the user explicitly asks to revise/replan; `[y/N]` means No is the default.
- Automatic repair exception: none for file-changing repair in Phase 1
- User response: y / n / non-y / pending
- Approval result: approved / not_approved / blocked / pending
- Revised Repair Plan count:
