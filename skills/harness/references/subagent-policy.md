# Subagent Policy

## Principles

- The authoritative handoff contract is `../../../docs/contracts/subagent-handoff.md`.
- `Tiny` may be handled by the main agent.
- `Small` and larger tasks require planner, implementer, and reviewer subagents.
- Explicit `$harness` invocation is policy preauthorization for creating planner, implementer, and reviewer subagents only.
- Policy preauthorization is not approval for destructive commands, secret access, production-impact work, deployment, external network calls, privileged access, or broad rewrites outside the accepted Plan.
- Implementation and repair still require exact `[y/N]` approval gates. Only lowercase `y` approves execution. Ambiguous natural language means no decision; ask again for explicit `y` or `n`. Non-approval (`n`, empty response, uppercase variants such as `N`, expanded variants, and any other non-`y` response that is not ambiguous) stops by default; do not implement, repair, revise, or replan unless the user explicitly asks to revise/replan.
- Every subagent receives a bounded brief.
- Subagent output is evidence; final judgment and integration remain orchestrator responsibility.
- The clean-context reviewer must be read-only, compare the diff against the accepted Plan, flag undocumented scope expansion, and avoid relying on implementer intent.

## Required Topology

- `Small`: one planner, one domain implementer, one reviewer.
- `Non-trivial`: one planner, one or more domain implementers, one reviewer.
- Default upper bound for large/high-risk tasks is four subagents unless the user approves more.

## Reasoning Effort Policy

- See `references/model-policy.md` for the authoritative Harness model and reasoning effort policy.
- Project-level minimum is `model_reasoning_effort = "high"` to prevent silent fallback below high.
- Planner requires high or above and must record intended/actual reasoning effort and fallback decision in the Plan.
- Implementer requires xhigh. If xhigh is unavailable, prefer switching to an xhigh-capable Codex model; if not possible, explicitly record high fallback and either record a blocked or degraded run state, or request user approval before continuing.
- Reviewer requires xhigh. If xhigh is unavailable, prefer switching to an xhigh-capable Codex model; if not possible, explicitly record high fallback and either record `review_blocked_degraded` or request user approval before continuing.
- Do not use medium, low, or minimal reasoning effort for Harness workflow roles.

## Authorization

Use `policy preauthorization` for required Harness subagents unless environment, tooling, security, or project rules require explicit approval. If delegation fails, record the affected role or gate as blocked or degraded.

## Brief Requirements

Each brief must include objective, classification, role/domain, scope, files/areas, non-goals, constraints, allowed tools or prohibited actions, code modification permission, required output format, evidence requirements, and stop conditions.

Default permission is read-only. Only implementer and repair implementer subagents may receive write permission. Implementer write permission is limited to the accepted Plan and specified files/areas; repair implementer write permission is limited to the accepted Repair Plan, approved findings, and specified write boundary.

Briefs must identify whether the handoff is planner, implementer, reviewer, or repair implementer. Repair implementer briefs are narrowed to the accepted Repair Plan and approved findings only.

## SubagentStop Summary

Every planner, implementer, reviewer, and repair implementer subagent must end with the canonical `SubagentStop Summary` fields from `../../../docs/contracts/subagent-handoff.md`:

- Role
- Task / Phase
- Inputs Received
- Actions Completed
- Files Inspected
- Files Changed
- Verification Performed
- Evidence Produced
- Blockers
- Residual Risks
- Required Next Action

## Reviewer Rule

Review is completed only by a clean-context read-only reviewer subagent. Main-agent risk inspection is not Review.

If reviewer role separation collapses, record `review_blocked_degraded` and the required no-review statement instead of producing a Review verdict from main-agent inspection.

## Blocked / Degraded Handling

When a required subagent cannot complete, record:

- affected role or gate
- why subagent creation or completion failed
- authorization request and result, if any
- project/security rule prohibiting delegation, if any
- evidence inspected
- criteria applied
- risk observations or the exact no-review statement
- degraded independence statement
- residual risk and required user decision or external state change

Required no-review statement:

```text
Review blocked/degraded; no clean-context reviewer findings are available.
```
