# Role Model

Harness workflow loop roles are separated. For `Small` and larger tasks, separation must be implemented through actual subagent orchestration when tooling allows it.

## Orchestrator

The main agent classifies the task, inspects project rules, defines topology, writes bounded briefs, integrates outputs, validates `SubagentStop Summary` evidence, resolves conflicts, controls scope, performs final verification, and owns Completion.

## Planner

The planner analyzes requirements and current state, defines constraints, risks, acceptance criteria, and verification strategy, and drafts a decision-complete Plan. It does not edit code.

## Implementer

The implementer changes only the assigned domain and allowed files/areas under an accepted Plan or Repair Plan. It runs targeted verification and stops on scope drift.

## Repair Implementer

The repair implementer is an implementer constrained to the accepted Repair Plan and approved Review findings. It does not fix unapproved findings or broaden scope.

## Reviewer

The reviewer is a clean-context read-only subagent. It reviews accepted Plan, diff, verification evidence, and project rules for concrete findings.

## Repair Planner

The orchestrator writes Repair Plans by separating fix-now, deferred, and rejected findings. Major scope changes return to a new Plan loop.

## Improver

The improvement artifact is conditional. It records process, template, hook, or orchestration improvement candidates for a future loop without expanding current success criteria.

## Separation Rule

Plan is not Review, Review is not fix, and Completion is not implementation. If required roles collapse into the main agent for `Small` or larger tasks, record the affected role or gate as blocked or degraded. A collapsed reviewer cannot complete Clean-context Review.
