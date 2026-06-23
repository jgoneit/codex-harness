# Plan

## Artifact Metadata

- Harness run id:
- Artifact id:
- Phase: Plan
- Artifact status: draft / accepted / revised / completed / blocked / degraded
- Created at:
- Updated at:
- Source request:
- Related artifacts:

## Task Classification

- Classification: Tiny / Small / Non-trivial
- Required workflow: lightweight Tiny / full loop
- Required subagents:

## Risk Level

- Risk: Low / Medium / High
- Risk drivers:

## Reasoning for classification

- Why this classification applies:
- Why lower classification does not apply:
- Scope or risk triggers:

## In Scope

-

## Out of Scope

-

## Files / Areas to Inspect

-

## Proposed Change Plan

1.
2.
3.

## Verification Plan

- Targeted checks:
- Evidence required:
- Blocked or unsafe checks:
- Verification exception needed? Yes/No:

## Risks / Assumptions

- Risks:
- Assumptions:
- Escalation triggers:

## Approval Gate

- Approval prompt: `Proceed with this Plan? [y/N]`
- Approval semantics: only lowercase `y` approves execution of the accepted Plan; ambiguous natural language means no decision and requires asking again for explicit `y` or `n`; non-approval (`n`, empty response, uppercase variants such as `N`, expanded variants, and any other non-`y` response that is not ambiguous) stops by default and does not trigger implementation, revision, or replanning unless the user explicitly asks to revise/replan; `[y/N]` means No is the default.
- User response: y / n / non-y / pending
- Approval result: approved / not_approved / blocked / pending
- Revised Plan count:
- Additional approval required:
