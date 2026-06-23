# Phase Contracts

The authoritative workflow contract is `docs/contracts/harness-contract.md`. These phase contracts mirror that contract for the skill runtime instructions.

## Gate Matrix

- `Tiny`: concise Plan, exact Plan approval, direct implementation, and Completion. Review only when project rules, user instruction, discovered risk, or scope growth requires it.
- `Small`: planner subagent Plan, exact Plan approval, domain implementer subagent Implementation Summary, clean-context reviewer subagent Review, Repair Plan if needed, exact Repair Plan approval if repair is needed, Completion.
- `Non-trivial`: planner subagent Plan, exact Plan approval, one or more domain implementer subagents, clean-context reviewer subagent Review, Repair Plan if needed, exact Repair Plan approval if repair is needed, Completion.

Only explicit environment, tooling, approval, project, or security constraints can produce blocked/degraded state.

## Plan

`Tiny` may use an orchestrator-written concise Plan. `Small` and larger tasks require a planner subagent draft, then orchestrator confirmation of classification, risk, scope boundaries, and verification strategy.

Plan output must use these canonical sections:

- Task Classification
- Risk Level
- Reasoning for classification
- In Scope
- Out of Scope
- Files / Areas to Inspect
- Proposed Change Plan
- Verification Plan
- Risks / Assumptions
- Approval Gate

The Approval Gate must include this exact prompt:

```text
Proceed with this Plan? [y/N]
```

Only lowercase `y` approves execution of the accepted Plan. Ambiguous natural language means no decision; ask again for explicit `y` or `n`. Non-approval (`n`, empty response, uppercase variants such as `N`, expanded variants, and any other non-`y` response that is not ambiguous) stops by default; do not implement, revise, or replan unless the user explicitly asks to revise/replan. `[y/N]` means No is the default.

## Implementation Summary

`Tiny` may be implemented directly by the orchestrator. `Small` and larger tasks require a domain implementer subagent working only inside the accepted Plan and allowed write boundary.

Implementation Summary output must use these canonical sections:

- Accepted Plan Reference
- Changed Files
- Summary of Changes
- Scope Compliance
- Verification Performed
- Deviations from Plan
- Blockers / Residual Risks

Scope growth, new risk categories, destructive operations, secret access, direct database access, deployment, or production-impact commands require a separate gate.

## Clean-context Review

`Small` and larger tasks always require Review. If Review is entered for `Tiny`, the same rules apply.

Only a clean-context read-only reviewer subagent can complete Review. The reviewer must not modify files, must not rely on implementer intent, must compare the diff against the accepted Plan, must flag undocumented scope expansion, and must identify missing or weak verification evidence.

Review output must use these canonical sections:

- Inputs Reviewed
- Accepted Plan
- Diff / Changed Files
- Verification Evidence
- Findings Table
- Verdict

Findings Table columns are:

```text
| Severity | Finding | Evidence | Required Action |
```

Verdict values are only `PASS`, `PASS_WITH_NOTES`, `REPAIR_REQUIRED`, or `BLOCKED`.

Review criteria must include scope compliance, acceptance criteria satisfaction, verification fidelity, security/secret handling, data/DB risk, bypass surface, API or contract drift, and maintainability/normalization consistency. The findings table may use `not_applicable` where a criterion has no finding.

If the reviewer subagent cannot be used when Review is required, Review status is `review_blocked_degraded`, not completed.

## Repair Plan

Separate accepted Review findings into repair-now, deferred follow-up, and rejected finding. If a finding requires major scope, contract, API, data, security, dependency, deployment, or workflow change, return to a new Plan loop.

Repair Plan output must use these canonical sections:

- Review Findings Addressed
- Repair Scope
- Files Expected to Change
- Verification Required
- Risks
- Repair Approval Gate

Repair must not proceed automatically when Review finds issues requiring repair. Phase 1 defines no automatic file-changing repair exception.

The Repair Approval Gate must include this exact prompt:

```text
Proceed with this Repair Plan? [y/N]
```

Only lowercase `y` approves execution of the accepted Repair Plan. Ambiguous natural language means no decision; ask again for explicit `y` or `n`. Non-approval (`n`, empty response, uppercase variants such as `N`, expanded variants, and any other non-`y` response that is not ambiguous) stops by default; do not repair, revise, or replan unless the user explicitly asks to revise/replan. `[y/N]` means No is the default.

## Repair Implement

Implement only the accepted Repair Plan. If repair reveals new risk, scope expansion, or unresolved conflict, stop and revise the Repair Plan or start a new Plan loop only when requested or required by a newly approved gate.

## Completion Report

Report status, Review status, whether a Repair Plan was required, changed files, verification, Review result, Approval Ledger, residual risks, and follow-up.

Completion status values are only:

- `completed`
- `completed_with_residual_risk`
- `blocked`
- `degraded`
- `cancelled`

The Approval Ledger table must have columns exactly:

```text
| Gate | Required? | Requested? | User response | Result | Notes |
```

Minimum Approval Ledger gates are Plan approval, Scope expansion approval, Destructive command approval, Secret/config access approval, Direct DB access approval, Repair plan approval, and Verification exception approval. Repair plan approval may use one row per repair round. Every ledger cell must be filled; use `not_applicable` where a gate or field does not apply instead of leaving cells blank.
