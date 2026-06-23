# Escalation Rules

Stop and escalate when:

- Acceptance criteria conflict.
- Local project rules conflict with the user request.
- Required subagents cannot be created and degraded progress is unsafe.
- Progress would require pretending Review is complete without a reviewer subagent.
- Planner, implementer, and reviewer outputs conflict and evidence cannot resolve them.
- Verification repeatedly fails and the cause is unclear.
- Findings do not converge after two repair cycles.
- Secret, credential, destructive operation, or production-impact risk appears.
- The change expands into data, security, dependency, or deployment risk not covered by the Plan.

## Escalation Output

Briefly record what failed, evidence inspected, why continuing is unsafe, needed user/project decision or external state change, completed gates, and blocked or degraded gates.

## Resume Rule

When the user decides or the blocker clears, resume from a new Plan or Repair Plan. Do not hide the prior failure; track it through Completion.
