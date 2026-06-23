# Sub-agent Handoff Contract

This contract is canonical for Harness sub-agent handoffs and `SubagentStop` summaries. It supplements the [Harness workflow contract](harness-contract.md); it does not replace canonical Phase 1 artifact sections, exact approval prompts, Review verdict values, or Completion status values.

## Applicability

- `Tiny` work may be handled by the orchestrator without sub-agent handoff unless user instructions, project rules, discovered risk, or scope growth require Review.
- `Small` and `Non-trivial` work require planner, implementer, and clean-context read-only reviewer sub-agents when tooling allows it.
- Repair implementation uses an implementer handoff constrained to the accepted Repair Plan.
- If required sub-agent tooling is unavailable, the run must record blocked or degraded behavior before continuing or stopping.

## Common Handoff Rules

- The orchestrator writes every sub-agent brief and remains responsible for final integration, conflict resolution, verification, and Completion.
- Each sub-agent receives only the task context needed for its role, including objective, classification, role/domain, scope, files or areas, non-goals, constraints, permissions, required evidence, output format, and stop conditions.
- Default permission is read-only. Only implementer and repair implementer roles may receive write permission, and only inside the accepted scope and write boundary.
- Sub-agent output is evidence, not final authority. The orchestrator must compare it with the accepted Plan, diff, verification evidence, and project rules.
- A sub-agent must stop instead of improvising when inputs are missing, scope drifts, a prohibited action is needed, verification cannot run, or new security, data, dependency, deployment, workflow, or contract risk appears.

## Brief Payload

Every handoff brief must include:

- objective and task or phase
- task classification and risk level
- role and domain
- inputs provided to the sub-agent
- allowed files or areas and read-only context
- out-of-scope files, areas, and decisions
- code modification permission and write boundary
- constraints, prohibited actions, and stop conditions
- required output template or artifact sections
- required verification or evidence
- expected `SubagentStop Summary` fields

## Role Handoffs

### Planner Handoff

The planner handoff occurs before Plan approval. The planner is read-only and receives the user request, relevant project rules, inspected context, candidate classification, constraints, and orchestration requirements.

The planner handoff must include User Request, Task Classification, Risk Level, Constraints, Files / Areas to Inspect, In Scope, Out of Scope, Proposed Change Plan, Verification Plan, Risks / Assumptions, and Approval Gate. The planner must produce a decision-complete Harness Plan for orchestrator review, including concrete scope boundaries, verification strategy, risks, and escalation triggers. The planner must not edit files, approve implementation, silently expand scope, or treat planning as Review.

### Implementer Handoff

The implementer handoff occurs only after the accepted Plan has exact approval. The implementer receives the accepted Plan reference, assigned domain, allowed files or areas, non-goals, local project rules, verification requirements, and write boundary.

The implementer handoff must include Accepted Plan Reference, Approved Scope, Allowed Files / Areas, Disallowed Changes, Required Verification, Stop Conditions, and Expected Implementation Summary.

The implementer may change only the briefed files or areas. It must stop for replanning or a separate gate if the work requires new scope, destructive commands, secret or protected config access, direct database access, deployment, production-impact actions, dependency changes, public contract changes, or other risk categories not authorized by the accepted Plan.

The implementer returns the canonical Implementation Summary and a `SubagentStop Summary`.

### Reviewer Handoff

The reviewer handoff occurs after implementation output and verification evidence are available. The reviewer must be clean-context and read-only. The reviewer receives the accepted Plan, task classification, changed files, diff or diff summary, verification evidence, relevant project rules, and Implementation Summary.

The reviewer handoff must include Accepted Plan, Diff / Changed Files, Verification Evidence, Project Rules / Contract References, Review Criteria, Findings Table, and Verdict.

The reviewer compares the diff and evidence against the accepted Plan, flags undocumented scope expansion, treats missing or weak verification as risk or a finding, and returns the canonical Clean-context Review with one of the existing Review verdict values. The reviewer must not edit files, implement fixes, or rely on implementer intent.

### Repair Implementer Handoff

The repair implementer handoff occurs only after an accepted Repair Plan has exact approval. It is an implementer handoff narrowed to the Review findings selected for repair, the accepted Repair Plan, files expected to change, and required verification.

The repair implementer handoff must include Approved Repair Plan Reference, Review Findings Addressed, Repair Scope, Allowed Files / Areas, Disallowed Changes, Verification Required, Stop Conditions, and Expected Repair Implementation Summary.

The repair implementer must not proceed unless the exact Repair Plan is approved. It must not fix unapproved findings, broaden the Repair Plan, or start a new design. Any new issue outside the approved Repair Plan triggers a new Plan, a revised Repair Plan, or a user decision. Major scope, contract, API, data, security, dependency, deployment, or workflow change returns to a new Plan loop.

### Orchestrator Intake

When a sub-agent stops, the orchestrator must inspect the artifact, `SubagentStop Summary`, files changed, verification evidence, and any blockers before moving to the next phase. Missing required fields are degraded evidence and may block the phase if they prevent safe integration or Review.

## SubagentStop Summary

Every planner, implementer, reviewer, and repair implementer sub-agent must finish with this summary. It is appended after the role's required artifact when an artifact is produced; it does not rename or replace canonical artifact sections.

```text
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
```

Use `none` for fields that do not apply, such as `Files Changed` for planner or reviewer roles. Use `not_run` only for verification that was expected but could not be run, and include the reason in the same field or in `Blockers`.

## Degraded And Role Collapse Behavior

Role collapse means a required planner, implementer, reviewer, or repair implementer cannot run as a separate sub-agent and the orchestrator would have to perform or approximate that role.

- If planner or implementer separation collapses, the orchestrator must record the affected role, reason, evidence available, degraded independence statement, residual risk, and whether continuation is allowed by user instructions and project rules.
- If the clean-context reviewer cannot run, Review is not completed. Record Review status as `review_blocked_degraded` and include this statement:

```text
Review blocked/degraded; no clean-context reviewer findings are available.
```

- Main-agent inspection can inform risk reporting but cannot be labeled Clean-context Review.
- Role collapse never bypasses exact approval gates, write boundaries, destructive-command approval, secret/config approval, direct database approval, or repair approval.
- If degraded execution prevents safe progress or leaves required acceptance criteria unverifiable, stop as blocked rather than completing.

## Conflict And Evidence Handling

- Resolve conflicts between sub-agent outputs with concrete evidence from files, diffs, command output, project rules, or approved artifacts.
- If evidence cannot resolve a conflict, stop and escalate to the user instead of choosing the convenient interpretation.
- Completion must record blocked or degraded roles, handoff gaps, unresolved conflicts, verification gaps, and residual risks.
