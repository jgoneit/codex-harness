# Classification Policy

Every `$harness` task must be classified as `Tiny`, `Small`, or `Non-trivial` before any phase gate. `blocked` and `degraded` are run states, not task sizes.

The authoritative workflow contract is `docs/contracts/harness-contract.md`.

## Tiny

Use `Tiny` only for narrow, local, low-risk changes:

- Single-file typo fixes.
- Formatting-only changes.
- Comment-only changes that do not affect implementation expectations.
- Short wording cleanup that does not change meaning.
- Changes where visual inspection or one simple check is enough.
- No behavior, API, data, dependency, security, workflow, policy, hook, or contract change.

Lightweight handling is acceptable for `Tiny`: concise Plan, exact Plan approval, direct implementation, and Completion. Review is optional only when project rules, user instructions, discovered risk, or scope growth do not require it.

If a `Tiny` task touches misleading security/data/contract wording, changes workflow expectations, or gains more than narrow local scope, reclassify upward.

## Small

Use `Small` for local, low-risk work with a clear verification path:

- Limited edits inside one feature, module, document area, or test area.
- Local behavior or documentation updates without public contract changes.
- Success and failure conditions can be stated clearly.
- One planner, one implementer, and one clean-context reviewer are sufficient.
- Verification can be targeted and does not require broad integration, migration, deployment, or production-like checks.

`Small` requires the full Harness loop: planner Plan, exact Plan approval, implementation, clean-context read-only Review, Repair Plan if needed, exact Repair Plan approval if repair is needed, and Completion.

## Non-trivial

Use `Non-trivial` when risk, blast radius, or coordination cost is meaningful:

- Behavior, API, schema, data, database, security, dependency, deployment, workflow, policy, hook, or contract changes.
- Multi-file or cross-module implementation changes.
- Migration, permission, secret, rollback, or production-impact risk.
- Multiple implementation domains or a compound verification strategy.
- Harness workflow or artifact contract changes, even when the files are documentation or templates.

`Non-trivial` requires the full Harness loop and may require more than one implementer domain.

Risky multi-file, API, database, security, dependency, deployment, workflow, policy, and contract tasks use the full loop because missed scope control or weak verification can affect callers, data, permissions, production behavior, or future Harness runs.

## Blocked / Degraded

Use `blocked` when a required gate, approval, clarification, permission, tool, policy condition, or acceptance criterion prevents safe progress. Stop and state what user decision or external state change is required.

Use `degraded` when the run can continue or report outcome only with reduced independence, missing verification, unavailable subagent tooling, or unavailable clean-context review. Degraded execution must be explicit in Review status, Completion status, and residual risks.

Only explicit environment, tooling, approval, project, or security constraints can produce a blocked/degraded state.

## Stop, Approval, And Clarification Rules

- Do not implement before exact Plan approval.
- Do not repair before exact Repair Plan approval.
- Ask for clarification before planning if the requested outcome, write boundary, or risk acceptance is ambiguous enough that classification cannot be made safely.
- If scope grows during implementation, stop and return to a Plan or Repair Plan gate.
- If Review finds required repair, do not repair automatically.
- If a new risk category appears, reclassify.
- If the planned verification path breaks, record the blocked/degraded condition or request a verification exception approval before completing.

## Tie-Breakers

- If multiple categories fit, choose the higher-risk category.
- If classification is unclear after reasonable inspection, choose the higher category or ask for clarification.
- If a task looks documentation-only but changes workflow, policy, contract, security, API, or data expectations, classify by risk rather than file type.
