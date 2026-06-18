# Completion Policy

Completion is the final `$harness` reporting gate.

## Required Fields

- task classification
- orchestration topology and spawned subagents
- implemented changes
- verification performed
- Review status
- review findings addressed
- completion status
- `blocked_degraded` roles, if any, with reason and degraded independence
- unresolved risks or follow-ups

## Review Status Enum

- `clean_context_review_completed`: clean-context read-only reviewer completed Review.
- `review_not_required_tiny_only`: `Tiny` task and no Review-required condition.
- `review_blocked_degraded`: reviewer subagent was unavailable and Review is not completed.

## Completion Status Enum

- `completed`: required gates and verification completed with no unresolved risk.
- `completed_with_residual_risk`: change completed with residual verification risk or follow-up.
- `completed_with_degraded_review`: completion reported while Review remains `review_blocked_degraded`.
- `blocked`: required gate or acceptance criteria cannot be safely completed.
- `escalated`: user or project owner decision is required.

## Blocked / Degraded Reporting

If a required role or gate is `blocked_degraded`, include blocked role/gate, blocker cause, evidence inspected, criteria applied, degraded independence, and remaining user decision or external state change.
