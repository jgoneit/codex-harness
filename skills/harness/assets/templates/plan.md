# Plan

## Artifact Metadata

- Harness run id:
- Artifact id:
- Phase: Plan
- Artifact status: draft / accepted / revised / completed / blocked_degraded
- Created at:
- Updated at:
- Source request:
- Task classification: Tiny / Small / Non-trivial
- Related artifacts:

## Goal

- Requested outcome:

## Task Classification

- Classification:
- Rationale:
- Required gates:

## Orchestration

- Required subagents:
- Planned subagents:
- Role/domain assignment:
- Authorization status: policy preauthorization / explicit approval required / blocked
- Blocked_degraded roles:
- Handoff artifacts:
- Intended/actual reasoning effort:
- Fallback decision:

## Requirements

- User-visible requirements:
- Functional requirements:
- Non-functional requirements:
- Non-goals:

## Current State

- Inspected files/modules/docs:
- Existing behavior:
- Local project rules:

## Constraints

- Scope limits:
- Safety or policy constraints:
- Compatibility constraints:
- Approval gates:

## Risks

- Implementation risks:
- Verification risks:
- Orchestration risks:
- Rollback or recovery concerns:

## Acceptance Criteria

### Required Behavior

- [ ]

### Required Non-behavior

- [ ]

### Required Evidence

- [ ]

## Plan Acceptance

- Acceptance source:
- Approval prompt: `Proceed with this Plan? [y/N]`
- Approval semantics: only lowercase `y` approves execution of the accepted Plan; ambiguous natural language means no decision and requires asking again for explicit `y` or `n`; non-approval (`n`, empty response, uppercase variants such as `N`, expanded variants, and any other non-`y` response that is not ambiguous) stops by default and does not trigger implementation, revision, or replanning unless the user explicitly asks to revise/replan; `[y/N]` means No is the default.
- User response: y / n / non-y / pending
- Approval or revision request:
- Revised Plan count:
- Additional project approval required:

## Test / Verification Strategy

- Test-first approach: failing test / explicit verification scenario / not applicable with reason
- Targeted checks:
- Blocked or unsafe checks:

## Implementation Plan

1.
2.
3.

## Out of Scope

-

## Escalation Triggers

-
