# Subagent Brief

## Role

- Role: planner / implementer / reviewer / repair implementer
- Domain: frontend / backend / ai / infra / data / docs / none
- Task classification:
- Task / Phase:
- Risk level:

## Objective

-

## Scope

- Approved scope:
- In scope:
- Out of scope:
- Disallowed changes:

## Files / Areas

- Allowed:
- Read-only context:
- Do not touch:

## Inputs

- User Request, for planner:
- Accepted Plan or planning context:
- Accepted Repair Plan, for repair implementer:
- Review findings addressed, for repair implementer:
- Local project rules:
- Verification requirements:
- Relevant evidence:

## Non-goals

-

## Constraints

-

## Code Modification Permission

- Permission: read-only / write allowed
- Write boundary:

## Required Output Format

- Required template:
- Required sections:
- planner: use `assets/templates/plan.md`
- implementer: use `assets/templates/implement.md`
- reviewer: use `assets/templates/review.md` and `assets/templates/reviewer-brief.md`
- repair implementer: use `assets/templates/implement.md` with Phase = Repair Implement and the accepted Repair Plan reference
- Expected implementation or repair summary:
- Required `SubagentStop Summary`: Role, Task / Phase, Inputs Received, Actions Completed, Files Inspected, Files Changed, Verification Performed, Evidence Produced, Blockers, Residual Risks, Required Next Action

## Evidence Requirements

- Include verifiable evidence such as files, lines, command output, test result, or project rule.

## Stop Conditions

- Work requires out-of-scope changes.
- Acceptance criteria are unclear or conflicting.
- Required evidence is unavailable.
- Security, data, dependency, or deployment risk appears.
- Clean-context or read-only requirements cannot be maintained for Review.

## SubagentStop Summary

- Role:
- Task / Phase:
- Inputs Received:
- Actions Completed:
- Files Inspected:
- Files Changed:
- Verification Performed:
- Evidence Produced:
- Blockers:
- Residual Risks:
- Required Next Action:
