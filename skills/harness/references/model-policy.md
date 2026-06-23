# Model Policy

Harness reasoning effort is part of the workflow contract.

## Required Effort

- Harness minimum reasoning effort is `high`.
- Planner uses `high` or above.
- Orchestrator uses `high` or above.
- Implementer uses `xhigh`.
- Reviewer uses `xhigh`.
- Improvement uses `high` or above.
- Do not use medium, low, or minimal for `$harness`.

## Fallback

1. If `xhigh` is unsupported, fallback to `high`.
2. Prefer switching to an `xhigh`-capable Codex model.
3. If neither is possible, record a blocked or degraded run state, or `review_blocked_degraded` when specifically reporting unavailable required Review, or ask for user approval.
