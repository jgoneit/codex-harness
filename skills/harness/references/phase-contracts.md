# Phase Contracts

## Gate Matrix

- `Tiny`: concise Plan, Implement, and Completion. Review only when project rules, user instruction, or discovered risk requires it.
- `Small`: planner subagent Plan, domain implementer subagent Implement, clean-context reviewer subagent Review, Repair Plan if needed, Completion.
- `Non-trivial`: planner subagent Plan, one or more domain implementer subagents, clean-context reviewer subagent Review, Repair Plan if needed, Completion.

Only explicit environment, tooling, approval, project, or security constraints can produce `blocked_degraded`.

## Plan

`Tiny` may use an orchestrator-written concise Plan. `Small` and larger tasks require a planner subagent draft, then orchestrator confirmation of acceptance criteria, constraints, verification strategy, and scope boundaries.

Plan output must include classification, requirements, current state, constraints, risks, acceptance criteria, verification strategy, orchestration topology, and this exact prompt:

```text
Proceed with this Plan? [y/N]
```

Only lowercase `y` approves execution of the accepted Plan. Ambiguous natural language means no decision; ask again for explicit `y` or `n`. Non-approval (`n`, empty response, uppercase variants such as `N`, expanded variants, and any other non-`y` response that is not ambiguous) stops by default; do not implement, revise, or replan unless the user explicitly asks to revise/replan. `[y/N]` means No is the default.

## Implement

`Tiny` may be implemented directly by the orchestrator. `Small` and larger tasks require a domain implementer subagent working only inside the accepted Plan and allowed write boundary.

Implement output must include implementer identity/domain, changed files, verification evidence, deviations requiring Review attention, and orchestrator integration summary.

## Review

`Small` and larger tasks always require Review. If Review is entered for `Tiny`, the same rules apply.

Only a clean-context read-only reviewer subagent can complete Review. Reviewer input is limited to the accepted Plan, classification, acceptance criteria, changed files/areas, diff or diff summary, verification results, relevant project rules, and required output format.

Review is complete only when the reviewer returns concrete findings or exactly:

```text
No concrete findings. Residual verification risk:
- ...
```

If the reviewer subagent cannot be used, Review status is `review_blocked_degraded`, not completed.

## Repair Plan

Separate accepted Review findings into fix-now, deferred follow-up, and rejected finding. If a finding requires major scope, contract, data, security, dependency, or deployment change, return to a new Plan loop.

Repair Plan output must include fix scope, expected files, verification, out-of-scope items, escalation conditions, and this exact prompt:

```text
Proceed with this Repair Plan? [y/N]
```

Only lowercase `y` approves execution of the accepted Repair Plan. Ambiguous natural language means no decision; ask again for explicit `y` or `n`. Non-approval (`n`, empty response, uppercase variants such as `N`, expanded variants, and any other non-`y` response that is not ambiguous) stops by default; do not repair, revise, or replan unless the user explicitly asks to revise/replan. `[y/N]` means No is the default.

## Repair Implement

Implement only the accepted Repair Plan. If repair reveals new risk, scope expansion, or unresolved conflict, stop and revise the Repair Plan or start a new Plan loop only when requested or required by a newly approved gate.

## Completion

Report implemented changes, verification, Review status, addressed findings, `blocked_degraded` roles, unresolved risks, and follow-ups.
