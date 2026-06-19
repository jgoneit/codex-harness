# Repair Plan

## Artifact Metadata

- Harness run id:
- Artifact id:
- Phase: Repair Plan
- Artifact status: draft / accepted / revised / completed / blocked_degraded
- Created at:
- Updated at:
- Source request:
- Task classification: Tiny / Small / Non-trivial
- Related artifacts:

## Review Reference

- Review source:
- Reviewer subagent identity:
- Accepted findings:

## Fix Now

1.
2.

## Deferred Follow-ups

-

## Rejected Findings

- Finding:
- Rationale:

## Expected Changes

- Files/areas:
- Implementer domain:
- Scope guard:

## Verification

- Checks to run:
- Required evidence:
- Blocked checks:

## Repair Approval

- Approval prompt: `Proceed with this Repair Plan? [y/N]`
- Approval semantics: only lowercase `y` approves execution of the accepted Repair Plan; ambiguous natural language means no decision and requires asking again for explicit `y` or `n`; non-approval (`n`, empty response, uppercase variants such as `N`, expanded variants, and any other non-`y` response that is not ambiguous) stops by default and does not trigger repair, revision, or replanning unless the user explicitly asks to revise/replan; `[y/N]` means No is the default.
- User response: y / n / non-y / pending
- Approval or revision request:
- Revised Repair Plan count:

## Escalation

- Conditions requiring a new Plan loop:
