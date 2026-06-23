# Harness Workflow Contract

Harness is an early-stage workflow guardrail for Codex runs that need deliberate scope control, explicit approval, role separation, clean-context review, repair gating, and completion reporting.

Harness is not a sandbox, security boundary, permission system, CI substitute, human review substitute, or guarantee that unsafe actions cannot occur. Repository permissions, least-privilege access, project policy, automated tests, code review, and human judgment remain required.

This contract is authoritative for Harness workflow artifacts and phase gates.

## Why The Workflow Exists

Harness exists to make higher-risk agent work reviewable:

- Planning states the intended scope before edits happen.
- Exact approval gates prevent accidental implementation or repair.
- Implementers work only inside the accepted Plan or accepted Repair Plan.
- Clean-context reviewers compare the diff against the accepted Plan without relying on implementer intent.
- Completion records what happened, what was verified, what was approved, and what remains risky.

Risky multi-file, API, database, security, dependency, deployment, workflow, policy, and contract tasks use the full loop because scope drift or missed verification can affect callers, data, permissions, production behavior, or future Harness runs.

## Task Classification

Every Harness run must classify the task before phase gates.

### Tiny

Use `Tiny` only when the change is narrow, local, and low-risk:

- typo, formatting, comment-only, or short wording cleanup
- one obvious file or area
- no behavior, API, data, dependency, security, workflow, policy, hook, or contract change
- one simple inspection or check is enough

`Tiny` may use lightweight handling: concise Plan, exact Plan approval, direct implementation, and Completion. Review is not required unless user instruction, project policy, discovered risk, or scope growth requires it.

### Small

Use `Small` for local, low-risk work with a clear verification path:

- limited edits inside one feature, module, document area, or test area
- no public contract change, production-impact behavior change, migration, secret handling, deployment change, or dependency change
- success and failure conditions can be stated clearly
- one planner, one implementer, and one clean-context reviewer are enough

`Small` requires the full workflow loop: Plan, exact Plan approval, Implementation Summary, clean-context Review, Repair Plan if needed, exact Repair Plan approval if repair is needed, and Completion.

### Non-trivial

Use `Non-trivial` when risk, blast radius, or coordination cost is meaningful:

- behavior, public API, schema, data, database, security, dependency, deployment, workflow, policy, hook, or contract changes
- multi-file or cross-module implementation changes
- migration, permission, secret, production-impact, or rollback risk
- compound verification or multiple implementation domains
- Harness workflow or artifact contract changes

`Non-trivial` requires the full workflow loop and may require more than one implementer domain. If multiple classifications fit, choose the higher-risk classification.

### Blocked / Degraded

`blocked` and `degraded` are run states, not task sizes.

Use `blocked` when a required gate, approval, clarification, permission, tool, policy condition, or acceptance criterion prevents safe progress. Stop and state what user decision or external state change is required.

Use `degraded` when the run can continue or report outcome only with reduced independence, missing verification, unavailable subagent tooling, or unavailable clean-context review. Degraded execution must be explicit in the Review status, Completion status, and residual risks.

If classification is unclear, required information is missing, or scope has grown beyond the accepted Plan, stop for clarification, replanning, or a Repair Plan as appropriate.

## Required Artifacts

Harness process artifacts normally stay in the conversation. Persist them only when the user or project rules require it.

### Plan

Canonical sections:

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

Only lowercase `y` approves implementation. Any other non-ambiguous response leaves the Plan unapproved and stops execution unless the user explicitly asks to revise or replan.

### Implementation Summary

Canonical sections:

- Accepted Plan Reference
- Changed Files
- Summary of Changes
- Scope Compliance
- Verification Performed
- Deviations from Plan
- Blockers / Residual Risks

Implementation must stay inside the accepted Plan and allowed write boundary. Scope growth, new risk categories, destructive operations, secret access, direct database access, deployment, or production-impact commands require a separate gate.

### Clean-context Review

Canonical sections:

- Inputs Reviewed
- Accepted Plan
- Diff / Changed Files
- Verification Evidence
- Findings Table
- Verdict

Findings Table columns:

```text
| Severity | Finding | Evidence | Required Action |
```

Verdict values:

- `PASS`: no required action and no material residual risk
- `PASS_WITH_NOTES`: no required repair, but notes or residual risk remain
- `REPAIR_REQUIRED`: at least one finding requires repair before completion
- `BLOCKED`: review cannot reach a safe verdict because required evidence, tooling, policy, or scope clarity is missing

The reviewer must be clean-context and read-only. The reviewer must not modify files, must not rely on implementer intent, must compare the diff against the accepted Plan, must flag undocumented scope expansion, and must identify missing or weak verification evidence.

If a clean-context reviewer cannot be used when Review is required, Review is degraded, not completed.

### Repair Plan

Canonical sections:

- Review Findings Addressed
- Repair Scope
- Files Expected to Change
- Verification Required
- Risks
- Repair Approval Gate

Repair must not proceed automatically when Review finds issues requiring repair. Phase 1 defines no automatic file-changing repair exception. The Repair Approval Gate must include this exact prompt:

```text
Proceed with this Repair Plan? [y/N]
```

Only lowercase `y` approves repair implementation. Any other non-ambiguous response leaves repair unapproved and stops repair execution unless the user explicitly asks to revise or replan.

If repair requires major scope, contract, API, data, security, dependency, deployment, or workflow change, return to a new Plan loop instead of using a narrow Repair Plan.

### Completion Report

Canonical sections:

- Status
- Review Status
- Repair Plan Required
- Changed Files
- Verification
- Review Result
- Approval Ledger
- Residual Risks
- Follow-up

Status values:

- `completed`
- `completed_with_residual_risk`
- `blocked`
- `degraded`
- `cancelled`

The Approval Ledger table must use columns exactly:

```text
| Gate | Required? | Requested? | User response | Result | Notes |
```

Minimum ledger gates are Plan approval, Scope expansion approval, Destructive command approval, Secret/config access approval, Direct DB access approval, Repair plan approval, and Verification exception approval. Every cell must be filled; use `not_applicable` where a gate or field does not apply.

## Allowed Exceptions

- `Tiny` tasks may use lightweight handling when no rule or discovered risk requires Review.
- Review may be `review_not_required_tiny_only` only for `Tiny` tasks with no Review-required condition.
- A run may stop after a non-approval response without creating later artifacts.
- A run may complete as `blocked`, `degraded`, or `cancelled` when required gates or evidence are unavailable.

No exception weakens the exact approval prompts, lowercase-`y` semantics, dangerous-operation approvals, secret/config access approval, direct database access approval, or clean-context read-only requirement for Review when Review is required.

## Blocked And Degraded Behavior

When blocked or degraded, record:

- affected role, gate, or phase
- blocker cause or degraded condition
- evidence inspected
- criteria applied
- user decision or external state change needed
- residual risk
- whether Review was completed, not required, blocked, or degraded

Review blocked/degraded statement:

```text
Review blocked/degraded; no clean-context reviewer findings are available.
```
