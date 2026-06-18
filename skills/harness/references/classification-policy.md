# Classification Policy

Every `$harness` task must be classified as `Tiny`, `Small`, or `Non-trivial` before any phase gate.

## Tiny

Use `Tiny` only for narrow changes that do not affect workflow, policy, contract, or behavior:

- Single-file typo fixes
- Formatting-only changes
- Comment-only changes
- Short wording cleanup that does not change meaning
- Changes where visual inspection or one simple check is enough

If project rules, user instructions, or discovered risk require Review, use the clean-context read-only reviewer rules even for `Tiny`.

## Small

Use `Small` for local, low-risk work with a clear verification path:

- Limited edits inside one feature or document area
- Local behavior fixes without public contract changes
- Success and failure conditions can be stated clearly
- One planner, one implementer, and one reviewer are sufficient

`Small` and larger tasks require multi-agent orchestration and Review.

## Non-trivial

Use `Non-trivial` when risk or coordination cost is meaningful:

- Behavior, API, data, security, dependency, deployment, workflow, policy, or contract changes
- Multi-file or cross-module changes
- Migration, permission, secret, or production-impact risk
- Multiple domain implementers or a compound verification strategy

Workflow, policy, and contract documentation changes are not automatically documentation-only; classify them by scope and risk.

## Tie-Breakers

- If multiple categories fit, choose the higher-risk category.
- If scope grows during implementation, return to Plan or Repair Plan and reclassify.
- If a new risk category appears, reclassify.
- If the planned verification path breaks, reclassify.
- If classification is unclear, choose the higher category or ask for clarification.
